# T-103 수정 후 적대적 리뷰 17 기준선

- 리뷰 단계: post-fix-16에서 확인한 U+2028/U+2029 ECMAScript 줄 종결자 주석 누락 수정 후 열일곱 번째 독립 재검토
- 불변 코드 후보 commit: `34c0abfbdf695258d53a1015ff4b73926d1ebcd1`
- 불변 코드 후보 tree: `8bc05556808a5b970d8f0ac659f7fd934ac88167`
- post-fix-16 후보 commit: `73b9cf68788066742e8df99dfad2433cbe6bf5fc`
- post-fix-16 후보 tree: `70143a39a0ed31dd44a2b28aa81a2a58f23248d3`
- post-fix-16 manifest commit: `4f3bb3d`
- post-fix-16 A 원본 report commit: `da14cfcb68e0da7fc02c0b887dccfb09b40f57bd`
- post-fix-16 A 원본 report SHA256: `1C4E15ED0680A7A7EC8C502C8B5A6B07DEAC065ED723A1B7FAFD7C5B5D961521`
- post-fix-16 B 원본 report commit: `824c3373ed72ad5e2f0eacaede2511ad1d039ce3`
- post-fix-16 B 원본 report SHA256: `29B030919F8DF77393A83805FDDD25ED445BBA6402B7BA41E2C28E8DE43C2474`
- 이번 수정: ECMAScript 네 가지 줄 종결자(CR/LF/U+2028/U+2029)를 `//` 주석 종료·template 보간·JSX 중첩 스캐너에 공통 적용하고, 해당 경계를 plain TS와 MDX의 회귀 시험으로 고정했다.

## 재검토 범위

동일한 두 reviewer가 새 불변 후보에서 CSS selector 정규화·specificity·조건 교집합·주석 gap·빈 목록과 descendant 오류, JSON 숫자·깊이·오류 채널, `--json=` 입력 redaction, MDX inline·blockquote·fenced·tilde·tagged·배열·삼항·중첩 object·다중행·들여쓰기 없는 ESM·JS 주석·문단 밖 delimiter·같은 문단의 미종결 span 뒤 HTML/JSX·직접/단항/키워드/논리/숫자/정규식/소수/연산자/유니코드/결합 문자/ZWNJ/ZWJ/Unicode escape/Other_ID_Start·Other_ID_Continue/구버전 Unicode `Cn`/U+FEFF/`async` arrow/CR/LF/U+2028/U+2029 줄 종결자/주석 선행 MDX expression·여러 줄 JSX expression·blockquote 빈 문단·파일 첫 span·3자 inline span·backslash delimiter·escaped template과 보간 주석, Git diff 추가 행, symlink root, airport task/evidence를 Windows Python 3.14와 WSL Python 3.11에서 독립 재현한다. 소비자 저장소, npm/PyPI registry, workflow dispatch와 실제 소비자 build/e2e는 호출하지 않는다.

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
git diff --check f2f55b1 34c0abfbdf695258d53a1015ff4b73926d1ebcd1
```

두 reviewer는 이 manifest와 candidate commit/tree를 읽은 뒤 상대 결과를 보지 않고 각각 원본 report를 확정한다. 실행하지 않은 소비자 gate와 registry·게시 검증은 `NOT_RUN`으로 유지한다.
