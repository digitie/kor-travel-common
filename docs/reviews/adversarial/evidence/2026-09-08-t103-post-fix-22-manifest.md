# T-103 수정 후 적대적 리뷰 22 기준선

- 리뷰 단계: post-fix-21에서 재개방한 Markdown fence 뒤 LS/PS 접미사 과오탐을 수정한 뒤 스물두 번째 독립 재검토
- 불변 코드 후보 commit: `61f1cc6a900e25268e0c5eadc32ce1c5ccc9d3f3`
- 불변 코드 후보 tree: `bab9313184719713bc96fcb455b38b121f8db0f5`
- post-fix-21 후보 commit: `7e31b54e92c52e3b859b80c520d7ae88c2522159`
- post-fix-21 후보 tree: `2cd07cf45d1428d1027b6dd647c48353c3bdde59`
- post-fix-21 manifest commit: `6bd3e44`
- post-fix-21 A 원본 report commit: `ec499dadd3fb08501b3979040b69a4e3010e19e9`
- post-fix-21 A 원본 report SHA256: `EBBC114C59222655F4AF92890D664E238867887AE299FCCA01BB20FF101EBAF0`
- post-fix-21 B 원본 report commit: `422edcd1fca2619c7369060dfc3e5141a3af9b47`
- post-fix-21 B 원본 report SHA256: `53f2afd0c34e4c9c9b7c70140bf6a313cdeddcf7ede3bcdf62fa8621148b6015`
- 이번 수정: Markdown fence의 시작·내용·닫힘 후보에서 Python 전체 Unicode 공백을 사용하지 않고 CommonMark가 허용하는 ASCII space/tab만 인정한다. 따라서 fence marker 뒤 LS/PS는 닫힘이 아니며, 실제 다음 닫힘까지 내부 JSX를 계속 가린다. Markdown 경계와 ECMAScript 줄 주석 경계의 분리는 유지한다.

## 재검토 범위

동일한 두 reviewer가 새 불변 후보에서 CSS selector 정규화·specificity·조건 교집합·주석 gap·빈 목록과 descendant 오류, JSON 숫자·깊이·오류 채널, `--json=` 입력 redaction, MDX inline·blockquote·fenced·tilde·tagged·배열·삼항·중첩 object·다중행·들여쓰기 없는 ESM·JS 주석·문단 밖 delimiter·같은 문단의 미종결 span 뒤 HTML/JSX/ESM·직접/단항/키워드/논리/숫자/정규식/소수/연산자/유니코드/결합 문자/ZWNJ/ZWJ/Unicode escape/Other_ID_Start·Other_ID_Continue/구버전 Unicode `Cn`/U+FEFF/`async` arrow/CR/LF/CRLF/U+2028/U+2029 줄 종결자/주석 선행 MDX expression·여러 줄 JSX expression·blockquote 빈 문단·파일 첫 span·1·2·3자 inline span·backslash delimiter·escaped template과 보간 주석, fence marker의 ASCII space/tab/LS/PS 접미사·Git diff 추가행·가짜 hunk 문자열·bare CR/CRLF/LS/PS, symlink root, airport task/evidence를 Windows Python 3.14와 WSL Python 3.11에서 독립 재현한다. 소비자 저장소, npm/PyPI registry, workflow dispatch와 실제 소비자 build/e2e는 호출하지 않는다.

## 고정 명령

```text
python -B -X utf8 -m unittest discover -s tests -p "test_*.py" -v
python -B -X utf8 -m unittest tests.test_kt_contrast tests.test_ux_lint -v
uv run --no-project --python 3.11 python -B -X utf8 -m unittest discover -s tests
uv run --no-project --python 3.11 python -B -X utf8 -m unittest tests.test_ux_lint
python -B -X utf8 tools/validate_document_links.py
python -B -X utf8 tools/validate_plan.py
python -B -X utf8 tools/check_spdx.py
python -B -X utf8 tools/scan_secrets.py --all
python -B -X utf8 tools/check_prod_redaction.py --all
python -B -X utf8 tools/check_versions.py --self-check
python -B -X utf8 tools/check_aliases.py packages/tokens/aliases
python -B -X utf8 tools/kt_contrast.py packages/tokens/tokens.css --json
python -B -X utf8 tools/ux_lint.py --root tests/fixtures/ux --json
git diff --check 7e31b54e92c52e3b859b80c520d7ae88c2522159 61f1cc6a900e25268e0c5eadc32ce1c5ccc9d3f3
```

Windows 전체 회귀는 292개가 통과했고, WSL Python 3.11 전체 회귀는 292개(환경상 3개 skip), `tests.test_ux_lint`는 31개가 통과했다. 두 reviewer는 이 manifest와 candidate commit/tree를 읽은 뒤 상대 결과를 보지 않고 각각 원본 report를 확정한다. 실행하지 않은 소비자 gate와 registry·게시 검증은 `NOT_RUN`으로 유지한다.
