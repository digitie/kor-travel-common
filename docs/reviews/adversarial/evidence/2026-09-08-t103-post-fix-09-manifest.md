# T-103 수정 후 적대적 리뷰 9 기준선

- 리뷰 단계: post-fix-08 NO-GO finding 수정 후 아홉 번째 독립 재검토
- 불변 코드 후보 commit: `e4b8fe3ff62c404660363f6751eda52428cf554c`
- 불변 코드 후보 tree: `fb8f781ce70b89cc95883ef2531625c6259735c0`
- post-fix-08 기준선 commit: `559a9e8a0e49feca2dab9d59df29039bbb0acfd3`
- post-fix-08 기준선 tree: `322fb840ac458c8fc7a0c69f90b0d1bdb77495d6`
- post-fix-08 manifest commit: `5c91168b9a594039bbfcd0dfae0cdf89519ae434`
- post-fix-08 A 원본 report commit: `0e9e2dad84759afcd3728756c73f35580054e029`
- post-fix-08 B 원본 report commit: `0da67bb82a1044c524bafbf413425850bcc61021`
- post-fix-08 A 원본 report SHA256: `554DDEA89F9B6EAF923294CE4A527CC8FF741A61E64DBDC410EE56B1611EE230`
- post-fix-08 B 원본 report SHA256: `6eedbb4e8a9169d08b6688bfa1b325e9bac27324578436bb763dc9977d68f1ba`
- 이번 수정: CSS selector 주석 gap을 별도 상태로 보존해 지원 밖 compound를 fail closed하고, Markdown inline span의 닫힘 탐색·열린 상태 추적을 문단 경계와 파일 시작까지 동일하게 적용

## 재검토 범위

동일한 두 reviewer가 새 불변 후보에서 CSS selector 정규화·specificity·조건 교집합·주석 gap·빈 목록과 descendant 오류, JSON 숫자·깊이·오류 채널, `--json=` 입력 redaction, MDX inline·blockquote·fenced·tilde·tagged·배열·삼항·중첩 object·다중행·들여쓰기 없는 ESM·JS 주석·문단 밖 delimiter·파일 첫 span·3자 inline span·escaped template과 보간 주석, Git diff 추가 행, symlink root, airport task/evidence를 Windows Python 3.14와 WSL Python 3.11에서 독립 재현한다. 소비자 저장소, npm/PyPI registry, workflow dispatch와 실제 소비자 build/e2e는 호출하지 않는다.

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
git diff --check 94ca2f1730b270721eb6242bfcdd9362b51d45e5 e4b8fe3ff62c404660363f6751eda52428cf554c
```

두 reviewer의 post-fix-09 원본 report가 이 기준선 commit/tree와 일치한 뒤 최종 판정을 기록한다. 실행하지 않은 소비자 gate와 registry·게시 검증은 `NOT_RUN`으로 유지한다.
