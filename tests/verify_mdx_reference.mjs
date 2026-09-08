// SPDX-License-Identifier: GPL-3.0-or-later
// SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
// 고정 MDX 파서로 회귀 자료의 기대값을 검증한다. 제품도 같은 문법 파서를 쓴다.
import {readFileSync} from 'node:fs';
import {resolve, dirname} from 'node:path';
import {pathToFileURL} from 'node:url';

const entry = resolve(process.argv[2]);
const version = JSON.parse(readFileSync(resolve(dirname(entry), 'package.json'), 'utf8')).version;
if (version !== '3.1.1') throw new Error('참조 파서 버전은 3.1.1이어야 합니다');
const {createProcessor} = await import(pathToFileURL(entry));
const corpus = JSON.parse(readFileSync(new URL('./fixtures/ux/mdx-contexts.json', import.meta.url), 'utf8'));
const results = [];
for (const item of corpus.cases) {
  for (const prefix of item.prefixes ?? ['', '> ', '>> ']) {
    for (const separator of ['\n', '\r\n', '\r']) {
      const source = item.source.split('\n').map(line => prefix + line).join(separator);
      try {
        const tree = createProcessor().parse(source);
        const chars = source.split('');
        function mask(start, end) {
          // 파서가 제외한 첫 BOM 한 문자를 원문 좌표에 반영한다.
          const offset = source.startsWith('\ufeff') ? 1 : 0;
          for (let i = start + offset; i < end + offset; i++) if (!/[\r\n\u2028\u2029]/.test(chars[i])) chars[i] = ' ';
        }
        function visit(value) {
          if (!value || typeof value !== 'object') return;
          if (['code', 'inlineCode'].includes(value.type)) {
            mask(value.position.start.offset, value.position.end.offset);
            return;
          }
          for (const comment of value.comments ?? []) mask(comment.start, comment.end);
          for (const [key, child] of Object.entries(value)) {
            if (key !== 'comments') {
              if (Array.isArray(child)) child.forEach(visit);
              else if (child && typeof child === 'object') visit(child);
            }
          }
        }
        visit(tree);
        const masked = chars.join('');
        const findings = [];
        for (const [id, re] of [['P6', /\boutline-none\b/g], ['P8', /\bwindow\.confirm\b|(?<![.\w])confirm\(/g]]) {
          for (const match of masked.matchAll(re)) findings.push({offset: match.index, id});
        }
        findings.sort((a, b) => a.offset - b.offset);
        const actual = findings.map(f => f.id);
        results.push({id: item.id, prefix, separator, status: JSON.stringify(actual) === JSON.stringify(item.expected) ? 'PASS' : 'MISMATCH', actual});
      } catch (error) {
        results.push({id: item.id, prefix, separator, status: 'INVALID_MDX', reason: error.reason ?? error.message});
      }
    }
  }
}
console.log(JSON.stringify({version, total: results.length, passed: results.filter(r => r.status === 'PASS').length, other: results.filter(r => r.status !== 'PASS')}, null, 2));
process.exitCode = results.some(r => r.status !== 'PASS') ? 1 : 0;
