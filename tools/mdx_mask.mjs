// SPDX-License-Identifier: GPL-3.0-or-later
// SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
// 소스는 구문 분석만 한다. 사용자 import·표현식·플러그인을 실행하지 않는다.
import {createProcessor} from '@mdx-js/mdx';

function maskSource(source) {
  const tree = createProcessor().parse(source);
  const ranges = [];
  const pending = [tree];
  while (pending.length) {
    const node = pending.pop();
    if (!node || typeof node !== 'object') continue;
    if (node.type === 'code' || node.type === 'inlineCode') {
      ranges.push([node.position.start.offset, node.position.end.offset]);
      continue;
    }
    for (const comment of node.comments ?? []) ranges.push([comment.start, comment.end]);
    for (const [key, child] of Object.entries(node)) {
      if (key !== 'comments' && child && typeof child === 'object') {
        if (Array.isArray(child)) pending.push(...child);
        else pending.push(child);
      }
    }
  }
  ranges.sort((a, b) => a[0] - b[0]);
  const merged = [];
  for (const range of ranges) {
    const last = merged.at(-1);
    if (last && range[0] <= last[1]) last[1] = Math.max(last[1], range[1]);
    else merged.push([...range]);
  }
  // 파서 offset은 UTF-16, Python 좌표는 Unicode 문자 단위다.
  // 원문 문자마다 한 문자만 출력해 emoji가 가려져도 좌표를 보존한다.
  let offset = 0;
  let cursor = 0;
  const output = [];
  for (const char of source) {
    while (cursor < merged.length && merged[cursor][1] <= offset) cursor++;
    const hidden = cursor < merged.length && merged[cursor][0] <= offset;
    output.push(hidden && !/[\r\n\u2028\u2029]/.test(char) ? ' ' : char);
    offset += char.length;
  }
  return output.join('');
}

try {
  let input = '';
  process.stdin.setEncoding('utf8');
  for await (const chunk of process.stdin) input += chunk;
  const sources = JSON.parse(input);
  if (!Array.isArray(sources) || sources.some(source => typeof source !== 'string')) throw new Error();
  const results = sources.map(source => {
    try { return {masked: maskSource(source)}; }
    catch { return {error: 'INVALID_MDX'}; }
  });
  process.stdout.write(JSON.stringify(results));
} catch {
  // 파서 예외에는 원문·로컬 경로가 포함될 수 있으므로 밖으로 보내지 않는다.
  process.stderr.write('MDX 구문 분석 입력을 처리할 수 없습니다.\n');
  process.exitCode = 2;
}
