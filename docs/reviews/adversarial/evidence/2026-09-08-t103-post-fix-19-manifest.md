# T-103 수정 후 적대적 리뷰 19 기준선

- 리뷰 단계: post-fix-18에서 확인한 bare CR universal newline 변환 수정 후 열아홉 번째 독립 재검토
- 불변 코드 후보 commit: `415984bf7cb450d44d7661424884d6641fef8309`
- 불변 코드 후보 tree: `9c07d86aea28e130ad58b912d72ad99152795c31`
- post-fix-18 후보 commit: `31ad7a5876ff0d5714d4094cb4a402718d02a33f`
- post-fix-18 후보 tree: `60bbe9546e1561aa5aee4f0bfbdd834fdd9cf58c`
- post-fix-18 manifest commit: `64ad465`
- post-fix-18 A 원본 report commit: `2cd9e2bd544f32eeb790e191e781fd433ce84ea2`
- post-fix-18 A 원본 report SHA256: `A74CB44C82A966AED96B4EC427937322D0A6AAB0FB6518494AA97A3956B448F9`
- post-fix-18 B 원본 report commit: `0183ad1193c1631bb3bf1293766f8cb8ad6efc3c`
- post-fix-18 B 원본 report SHA256: `8CA4BAC8D328945F109447C46DF9EF679BA3C68BE7288214E8ECDFE6D4669430`
- 이번 수정: 소스 파일을 `newline=""`로 읽고 Git 출력을 bytes에서 UTF-8로 직접 디코딩해 bare CR/CRLF/Unicode 줄 종결자를 보존한다. LF만 Git diff 행 구분자로 사용하며 실제 CR 바이트를 포함한 `--base` 회귀를 고정했다.

## 재검토 범위

동일한 두 reviewer가 새 불변 후보에서 CSS selector 정규화·specificity·조건 교집합·주석 gap·빈 목록과 descendant 오류, JSON 숫자·깊이·오류 채널, `--json=` 입력 redaction, MDX inline·blockquote·fenced·tilde·tagged·배열·삼항·중첩 object·다중행·들여쓰기 없는 ESM·JS 주석·문단 밖 delimiter·같은 문단의 미종결 span 뒤 HTML/JSX·직접/단항/키워드/논리/숫자/정규식/소수/연산자/유니코드/결합 문자/ZWNJ/ZWJ/Unicode escape/Other_ID_Start·Other_ID_Continue/구버전 Unicode `Cn`/U+FEFF/`async` arrow/CR/LF/U+2028/U+2029 줄 종결자/주석 선행 MDX expression·여러 줄 JSX expression·blockquote 빈 문단·파일 첫 span·3자 inline span·backslash delimiter·escaped template과 보간 주석, Git diff 추가행·가짜 hunk 문자열·bare CR/CRLF, symlink root, airport task/evidence를 Windows Python 3.14와 WSL Python 3.11에서 독립 재현한다. 소비자 저장소, npm/PyPI registry, workflow dispatch와 실제 소비자 build/e2e는 호출하지 않는다.

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
git diff --check 538fc42 415984bf7cb450d44d7661424884d6641fef8309
```

두 reviewer는 이 manifest와 candidate commit/tree를 읽은 뒤 상대 결과를 보지 않고 각각 원본 report를 확정한다. 실행하지 않은 소비자 gate와 registry·게시 검증은 `NOT_RUN`으로 유지한다.
