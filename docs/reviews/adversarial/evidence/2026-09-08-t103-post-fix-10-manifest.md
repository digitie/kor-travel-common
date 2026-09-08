# T-103 수정 후 적대적 리뷰 10 기준선

- 리뷰 단계: post-fix-09 진행 중 추가 반례 수정 후 열 번째 독립 재검토
- 불변 코드 후보 commit: `f6ea446547c4e71ffb272b9623729396d6ef7185`
- 불변 코드 후보 tree: `f3b3b90d87d758d22917c7e729ec3e25c2fe06c3`
- post-fix-09 기준선 commit: `e4b8fe3ff62c404660363f6751eda52428cf554c`
- post-fix-09 기준선 tree: `fb8f781ce70b89cc95883ef2531625c6259735c0`
- post-fix-09 manifest commit: `f5f2e7c37188b68efd74fc8a320bee02e99aaa3e`
- 마지막 완료 raw 기준선(post-fix-08) A commit: `0e9e2dad84759afcd3728756c73f35580054e029`
- 마지막 완료 raw 기준선(post-fix-08) B commit: `0da67bb82a1044c524bafbf413425850bcc61021`
- 마지막 완료 raw 기준선(post-fix-08) A SHA256: `554DDEA89F9B6EAF923294CE4A527CC8FF741A61E64DBDC410EE56B1611EE230`
- 마지막 완료 raw 기준선(post-fix-08) B SHA256: `6eedbb4e8a9169d08b6688bfa1b325e9bac27324578436bb763dc9977d68f1ba`
- post-fix-09 진행 기록: 후보가 변경되기 전에 raw commit이 생성되지 않아 증거로 채택하지 않고 중단했다.
- 이번 수정: 닫히지 않은 Markdown span이 같은 문단의 HTML/JSX·ESM을 가리지 않도록 실행 시작점을 보존하고, 일반·blockquote 빈 문단을 동일한 경계로 처리하며, backslash가 있는 inline span delimiter를 Markdown 규칙대로 닫는다.

## 재검토 범위

동일한 두 reviewer가 새 불변 후보에서 CSS selector 정규화·specificity·조건 교집합·주석 gap·빈 목록과 descendant 오류, JSON 숫자·깊이·오류 채널, `--json=` 입력 redaction, MDX inline·blockquote·fenced·tilde·tagged·배열·삼항·중첩 object·다중행·들여쓰기 없는 ESM·JS 주석·문단 밖 delimiter·같은 문단의 미종결 span 뒤 HTML/JSX·blockquote 빈 문단·파일 첫 span·3자 inline span·backslash delimiter·escaped template과 보간 주석, Git diff 추가 행, symlink root, airport task/evidence를 Windows Python 3.14와 WSL Python 3.11에서 독립 재현한다. 소비자 저장소, npm/PyPI registry, workflow dispatch와 실제 소비자 build/e2e는 호출하지 않는다.

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
git diff --check 94ca2f1730b270721eb6242bfcdd9362b51d45e5 f6ea446547c4e71ffb272b9623729396d6ef7185
```

두 reviewer의 post-fix-10 원본 report가 이 기준선 commit/tree와 일치한 뒤 최종 판정을 기록한다. 실행하지 않은 소비자 gate와 registry·게시 검증은 `NOT_RUN`으로 유지한다.
