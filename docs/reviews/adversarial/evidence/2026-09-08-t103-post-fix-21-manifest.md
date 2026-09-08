# T-103 수정 후 적대적 리뷰 21 기준선

- 리뷰 단계: post-fix-20에서 재개방한 LS/PS Markdown code span 과오탐을 CommonMark 경계와 ECMAScript 경계로 분리한 뒤 스물한 번째 독립 재검토
- 불변 코드 후보 commit: `7e31b54e92c52e3b859b80c520d7ae88c2522159`
- 불변 코드 후보 tree: `2cd07cf45d1428d1027b6dd647c48353c3bdde59`
- post-fix-20 후보 commit: `dd06f22150d9ac9bed25ee7abc0b65265cdaa651`
- post-fix-20 후보 tree: `184a1755640d78fd52ce1dbeb30897a557a01ece`
- post-fix-20 manifest commit: `358f671`
- post-fix-20 A 원본 report commit: `055ef3a61a6df430e109ff4d1dbe076c498fd378`
- post-fix-20 A 원본 report SHA256: `7B7E5879481DC89B91CE021A2C1270BCA8C5C1988E80EB3FA4C571700F7E1B88`
- post-fix-20 B 원본 report commit: `f4a42ee51082d1f6a8a445ec74e1985d7511d22d`
- post-fix-20 B 원본 report SHA256: `e33b92fbf78879a53be18bcf7b1dd8e44b1201a09c2955942d9858fbca14b912`
- 이번 수정: Markdown 문단·fence·inline span·줄 시작은 CommonMark의 LF·CR·CRLF만 사용하고, JavaScript line comment·expression만 LF·CR·CRLF·U+2028·U+2029를 사용한다. bare CR 문단 뒤 unclosed span에서 ESM 선언을 재개하는 경계도 추가했다. LS/PS가 들어간 1·2·3자 닫힌 Markdown span은 정상 인용으로 남긴다.

## 재검토 범위

동일한 두 reviewer가 새 불변 후보에서 CSS selector 정규화·specificity·조건 교집합·주석 gap·빈 목록과 descendant 오류, JSON 숫자·깊이·오류 채널, `--json=` 입력 redaction, MDX inline·blockquote·fenced·tilde·tagged·배열·삼항·중첩 object·다중행·들여쓰기 없는 ESM·JS 주석·문단 밖 delimiter·같은 문단의 미종결 span 뒤 HTML/JSX/ESM·직접/단항/키워드/논리/숫자/정규식/소수/연산자/유니코드/결합 문자/ZWNJ/ZWJ/Unicode escape/Other_ID_Start·Other_ID_Continue/구버전 Unicode `Cn`/U+FEFF/`async` arrow/CR/LF/CRLF/U+2028/U+2029 줄 종결자/주석 선행 MDX expression·여러 줄 JSX expression·blockquote 빈 문단·파일 첫 span·3자 inline span·backslash delimiter·escaped template과 보간 주석, Git diff 추가행·가짜 hunk 문자열·bare CR/CRLF/LS/PS, symlink root, airport task/evidence를 Windows Python 3.14와 WSL Python 3.11에서 독립 재현한다. 소비자 저장소, npm/PyPI registry, workflow dispatch와 실제 소비자 build/e2e는 호출하지 않는다.

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
git diff --check dd06f22150d9ac9bed25ee7abc0b65265cdaa651 7e31b54e92c52e3b859b80c520d7ae88c2522159
```

Windows 전체 회귀는 291개가 통과했고, WSL Python 3.11 전체 회귀는 291개(환경상 3개 skip), `tests.test_ux_lint`는 30개가 통과했다. 두 reviewer는 이 manifest와 candidate commit/tree를 읽은 뒤 상대 결과를 보지 않고 각각 원본 report를 확정한다. 실행하지 않은 소비자 gate와 registry·게시 검증은 `NOT_RUN`으로 유지한다.
