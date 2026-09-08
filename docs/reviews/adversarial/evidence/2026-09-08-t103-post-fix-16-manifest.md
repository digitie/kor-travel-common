# T-103 수정 후 적대적 리뷰 16 기준선

- 리뷰 단계: post-fix-15에서 확인한 Python Unicode DB 차이와 ECMAScript U+FEFF 공백 누락 수정 후 열여섯 번째 독립 재검토
- 불변 코드 후보 commit: `73b9cf68788066742e8df99dfad2433cbe6bf5fc`
- 불변 코드 후보 tree: `70143a39a0ed31dd44a2b28aa81a2a58f23248d3`
- post-fix-15 후보 commit: `210c2de324b18fcaa4e3f8b18fe5965226cb79d7`
- post-fix-15 후보 tree: `58418960efa7e486d60fa95d9a3e7f335e0ad74b`
- post-fix-15 manifest commit: `e72b746`
- post-fix-15 A 원본 report commit: `fe08a3087cb1e42ecc393bbf1d766d1daf6b3c27`
- post-fix-15 A 원본 report SHA256: `ED426158170D22458C6F3ACEEADBC30ABF64E5B42D1E0B00255B293CF292EED7`
- post-fix-15 B 원본 report commit: `fbe2cc0a6f64fd305976d94792e06822631b93ad`
- post-fix-15 B 원본 report SHA256: `be5978aba63a68a04566351c043735308943489f859672bd58f6a8b0d9b7a0f0`
- 이번 수정: Python 구버전에서 최신 ECMAScript 식별자가 `Cn`으로 보이더라도 미종결 span 뒤 실행식 후보로 보존하고, U+FEFF를 ECMAScript 공백으로 건너뛴다. U+11F02·U+2EBF0과 U+FEFF 선행·식별자 뒤 경계를 양 span 길이로 회귀 시험에 추가했다.

## 재검토 범위

동일한 두 reviewer가 새 불변 후보에서 CSS selector 정규화·specificity·조건 교집합·주석 gap·빈 목록과 descendant 오류, JSON 숫자·깊이·오류 채널, `--json=` 입력 redaction, MDX inline·blockquote·fenced·tilde·tagged·배열·삼항·중첩 object·다중행·들여쓰기 없는 ESM·JS 주석·문단 밖 delimiter·같은 문단의 미종결 span 뒤 HTML/JSX·직접/단항/키워드/논리/숫자/정규식/소수/연산자/유니코드/결합 문자/ZWNJ/ZWJ/Unicode escape/Other_ID_Start·Other_ID_Continue/구버전 Unicode `Cn`/U+FEFF/`async` arrow/주석 선행 MDX expression·여러 줄 JSX expression·blockquote 빈 문단·파일 첫 span·3자 inline span·backslash delimiter·escaped template과 보간 주석, Git diff 추가 행, symlink root, airport task/evidence를 Windows Python 3.14와 WSL Python 3.11에서 독립 재현한다. 소비자 저장소, npm/PyPI registry, workflow dispatch와 실제 소비자 build/e2e는 호출하지 않는다.

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
git diff --check a7814d7 73b9cf68788066742e8df99dfad2433cbe6bf5fc
```

두 reviewer는 이 manifest와 candidate commit/tree를 읽은 뒤 상대 결과를 보지 않고 각각 원본 report를 확정한다. 실행하지 않은 소비자 gate와 registry·게시 검증은 `NOT_RUN`으로 유지한다.
