# T-103 수정 후 적대적 리뷰 15 기준선

- 리뷰 단계: post-fix-14에서 확인한 ECMAScript Unicode 식별자 경계와 `async` arrow 표현식 누락 수정 후 열다섯 번째 독립 재검토
- 불변 코드 후보 commit: `210c2de324b18fcaa4e3f8b18fe5965226cb79d7`
- 불변 코드 후보 tree: `58418960efa7e486d60fa95d9a3e7f335e0ad74b`
- post-fix-14 후보 commit: `0b2330e93d2b05a954593c82ef0ea230821adf28`
- post-fix-14 후보 tree: `688332816480e217b3615dd6426e063c223e365a`
- post-fix-14 manifest commit: `507328aa615f68b7828e9da543f80a6c805c4d3a`
- post-fix-14 A 원본 report commit: `c3abbdeb3f58be59cde0cd2fcf0a8436dec4a950`
- post-fix-14 A 원본 report SHA256: `0C5C8242ADFB8C9A656574E595D059CD9CA64598BBE6484595C4695CE3365A39`
- post-fix-14 B 원본 report commit: `3ce1303932de138d15674483c0a0310695f44a74`
- post-fix-14 B 원본 report SHA256: `95069872633cb436740cc09f431344088863ef73d2a0921a0b39dc71c279c794`
- 이번 수정: Python XID·`isalpha` 분기 대신 ECMAScript ID_Start/ID_Continue 경계를 사용하고, Other_ID_Start/Other_ID_Continue와 `async x =>` arrow 표현식을 보존한다. U+2163·U+2118·U+037A·U+00B7·U+0387 및 1/2자 미종결 span 회귀 시험을 추가했다.

## 재검토 범위

동일한 두 reviewer가 새 불변 후보에서 CSS selector 정규화·specificity·조건 교집합·주석 gap·빈 목록과 descendant 오류, JSON 숫자·깊이·오류 채널, `--json=` 입력 redaction, MDX inline·blockquote·fenced·tilde·tagged·배열·삼항·중첩 object·다중행·들여쓰기 없는 ESM·JS 주석·문단 밖 delimiter·같은 문단의 미종결 span 뒤 HTML/JSX·직접/단항/키워드/논리/숫자/정규식/소수/연산자/유니코드/결합 문자/ZWNJ/ZWJ/Unicode escape/Other_ID_Start·Other_ID_Continue/`async` arrow/주석 선행 MDX expression·여러 줄 JSX expression·blockquote 빈 문단·파일 첫 span·3자 inline span·backslash delimiter·escaped template과 보간 주석, Git diff 추가 행, symlink root, airport task/evidence를 Windows Python 3.14와 WSL Python 3.11에서 독립 재현한다. 소비자 저장소, npm/PyPI registry, workflow dispatch와 실제 소비자 build/e2e는 호출하지 않는다.

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
git diff --check 9f7dcf7 210c2de324b18fcaa4e3f8b18fe5965226cb79d7
```

두 reviewer는 이 manifest와 candidate commit/tree를 읽은 뒤 상대 결과를 보지 않고 각각 원본 report를 확정한다. 실행하지 않은 소비자 gate와 registry·게시 검증은 `NOT_RUN`으로 유지한다.
