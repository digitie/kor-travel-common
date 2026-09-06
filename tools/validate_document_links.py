# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
# Origin: canview@1f93b8adb34a48537db69b950c8a99ce89859760 tools/validate_document_links.py
# Modified: 2026-09-07 — common 경로·절대 링크 금지·산문/코드 span 제외·LICENSES 안내 검사
"""저장소 내부 Markdown 링크 target을 네트워크 없이 검사한다.

규칙(docs/runbooks/documentation-maintenance.md §6·§7):
- 문서 링크는 저장소 상대 경로만 허용한다. 절대 경로(`F:/...`, `/mnt/...`, `/...`)는 오류다.
- fenced code block과 inline code span 안의 링크는 검사하지 않는다.
- target에 공백이 있으면 링크가 아니라 산문의 대괄호·소괄호 조합으로 보고 건너뛴다.
- fragment(`#절-제목`)는 검증하지 않는다(파일 존재만 확인).
"""
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
ABSOLUTE_RE = re.compile(r'^([A-Za-z]:[/\\]|/)')
SKIP_PARTS = {'node_modules', '.venv', '.git', '.next', 'dist', 'build'}


def collect_documents(root: Path) -> list[Path]:
    files: list[Path] = []
    for base in ('docs', 'packages', 'tools', 'templates', 'tests', 'LICENSES'):
        files.extend((root / base).rglob('*.md'))
    files.extend(root.glob('*.md'))
    return sorted({f for f in files if not (set(f.relative_to(root).parts) & SKIP_PARTS)})


def validate(root: Path) -> tuple[list[str], int, int]:
    errors: list[str] = []
    count = 0
    files = collect_documents(root)
    for path in files:
        body = re.sub(r'```.*?```', '', path.read_text(encoding='utf-8'), flags=re.S)
        body = re.sub(r'(?<!`)(`+)(?!`).*?(?<!`)\1(?!`)', '', body, flags=re.S)
        for target in re.findall(r'!?\[[^\]\n]*\]\(([^)\n]+)\)', body):
            target = target.strip().strip('<>')
            if not target or any(ch.isspace() for ch in target):
                continue
            if ABSOLUTE_RE.match(target):
                # Windows 드라이브 문자(`F:/`)는 urlsplit이 scheme으로 오인하므로 먼저 판정한다.
                count += 1
                errors.append(f'{path.relative_to(root)} -> {target} (절대 경로 링크 금지)')
                continue
            parsed = urlsplit(target)
            if parsed.scheme or not parsed.path or target.startswith('//'):
                continue
            count += 1
            resolved = (path.parent / unquote(parsed.path)).resolve()
            if not resolved.exists():
                errors.append(f'{path.relative_to(root)} -> {target}')
    return errors, len(files), count


def main(argv: list[str] | None = None) -> int:
    root = Path(argv[0]).resolve() if argv else ROOT
    errors, documents, count = validate(root)
    print(f'Checked {documents} documents, {count} local targets; errors={len(errors)}')
    for error in errors:
        print(error)
    return int(bool(errors))


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
