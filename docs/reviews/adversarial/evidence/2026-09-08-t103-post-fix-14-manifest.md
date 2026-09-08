# T-103 수정 후 적대적 리뷰 14 기준선

- 리뷰 단계: post-fix-13에서 확인한 결합 문자·ZWNJ·Unicode escape 식별자 우회 수정 후 열네 번째 독립 재검토
- 불변 코드 후보 commit: `0b2330e93d2b05a954593c82ef0ea230821adf28`
- 불변 코드 후보 tree: `688332816480e217b3615dd6426e063c223e365a`
- post-fix-13 후보 commit: `e8137efd8f4b53465b8cf9a1d333127e4186b73c`
- post-fix-13 후보 tree: `091274064a82897f6f00ec8f3db2a8776379e13d`
- post-fix-13 manifest commit: `6cb95d0`
- post-fix-13 A 원본 report commit: `b5a5063d4fea276b079830287a5917decc15f5d8`
- post-fix-13 A 원본 report SHA256: `27C52DA3B8509A8C3B0927FA681B4A326667AC8497C101A1BFB9FE433C7CFC30`
- post-fix-13 B 원본 report commit: `d13832b7ce71fcf2e722f9d0dcd0ca28e848877c`
- post-fix-13 B 원본 report SHA256: `fe4c5604d178e6314af22df657bfe57e251355417fdc6abf478b924b276fa026`
- 이번 수정: JavaScript 식별자 시작·계속 문자를 직접 스캔해 결합 문자·ZWNJ/ZWJ·Unicode escape(`\\uXXXX`, `\\u{...}`)를 포함한 MDX 표현식도 보존한다. 해당 최소 반례를 회귀 시험으로 고정했다.

## 재검토 범위

동일한 두 reviewer가 새 불변 후보에서 CSS selector 정규화·specificity·조건 교집합·주석 gap·빈 목록과 descendant 오류, JSON 숫자·깊이·오류 채널, `--json=` 입력 redaction, MDX inline·blockquote·fenced·tilde·tagged·배열·삼항·중첩 object·다중행·들여쓰기 없는 ESM·JS 주석·문단 밖 delimiter·같은 문단의 미종결 span 뒤 HTML/JSX·직접/단항/키워드/논리/숫자/정규식/소수/연산자/유니코드/결합 문자/ZWNJ/Unicode escape/주석 선행 MDX expression·여러 줄 JSX expression·blockquote 빈 문단·파일 첫 span·3자 inline span·backslash delimiter·escaped template과 보간 주석, Git diff 추가 행, symlink root, airport task/evidence를 Windows Python 3.14와 WSL Python 3.11에서 독립 재현한다. 소비자 저장소, npm/PyPI registry, workflow dispatch와 실제 소비자 build/e2e는 호출하지 않는다.

## 고정 명령

```text
python -B -X utf8 -m unittest discover -s tests -p "test_*.py" -v
python -B -X utf8 -m unittest tests.test_kt_contrast tests.test_ux_lint -v
python -B -X utf8 tools/validate_document_links.py
python -B -X utf8 tools/validate_plan.py
python -B -X utf8 tools/check_spdx.py
python -B -X utf8 tools/scan_secrets.py --all
python -B -X utf8 tools/check_prod_redaction.py --all
python -B -X utf8 tools/check_versions.py --self-check
python -B -X utf8 tools/check_aliases.py packages/tokens/aliases
python -B -X utf8 tools/kt_contrast.py packages/tokens/tokens.css --json
python -B -X utf8 tools/ux_lint.py --root tests/fixtures/ux --json
git diff --check 6da46d4 0b2330e93d2b05a954593c82ef0ea230821adf28
```

두 reviewer는 이 manifest와 candidate commit/tree를 읽은 뒤 상대 결과를 보지 않고 각각 원본 report를 확정한다. 실행하지 않은 소비자 gate와 registry·게시 검증은 `NOT_RUN`으로 유지한다.
