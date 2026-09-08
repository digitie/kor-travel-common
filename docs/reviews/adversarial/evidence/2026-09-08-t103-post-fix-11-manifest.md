# T-103 수정 후 적대적 리뷰 11 기준선

- 리뷰 단계: post-fix-10의 MDX 표현식 잔여 finding 수정 후 열한 번째 독립 재검토
- 불변 코드 후보 commit: `c0c93c47e5f25aa0879fd0fb4e56261f6f624138`
- 불변 코드 후보 tree: `f9b16a3d03f3fca49ba8048cc9d0328e78aadda4`
- post-fix-10 기준선 commit: `bd73856ac1d3327b1fe46acc352163eee23ad504`
- post-fix-10 기준선 tree: `a36690082222adae103f10b74d5e38bb0d312782`
- post-fix-10 manifest commit: `bd73856ac1d3327b1fe46acc352163eee23ad504`
- 마지막 완료 raw 기준선(post-fix-08) A commit: `0e9e2dad84759afcd3728756c73f35580054e029`
- 마지막 완료 raw 기준선(post-fix-08) B commit: `0da67bb82a1044c524bafbf413425850bcc61021`
- 마지막 완료 raw 기준선(post-fix-08) A SHA256: `554DDEA89F9B6EAF923294CE4A527CC8FF741A61E64DBDC410EE56B1611EE230`
- 마지막 완료 raw 기준선(post-fix-08) B SHA256: `6eedbb4e8a9169d08b6688bfa1b325e9bac27324578436bb763dc9977d68f1ba`
- post-fix-09 A 원본 report commit: `39d131fe5a3df1b56a0477a73519e8d1818ed393`
- post-fix-09 A 원본 report SHA256: `89D7FEC2A466B660F88707D26DE963358BB07BE8D7427A7AA09215469C379792`
- post-fix-09 B 원본 report: 후보 수정 전에 최종 raw commit이 생성되지 않아 채택하지 않았다.
- post-fix-10 A 원본 report commit: `42ea0ab7a54fd4bdbd15bad0fbaafeb39d240ece`
- post-fix-10 A 원본 report SHA256: `CEA6C9B453F4121ED4B118242B928D0E87277696C2FE92CCF2B9A1A025B2801F`
- post-fix-10 B 원본 report commit: `e4230878a96d9bdd93c837f7303eefea88e2570b`
- post-fix-10 B 원본 report SHA256: `a3b5f2704c9d889c8e9457db0cf480e0f4bfabdedfbf39dfb577e95bd43c4d7e`
- 이번 수정: 미종결 Markdown span 뒤 `{window.confirm(...)}` 같은 MDX 표현식과 여러 줄 JSX 표현식의 시작점을 보존하고, 가려진 이전 span이 이후 JSX template 판정을 오염시키지 않도록 분석용 masked text를 사용한다. 표현식·여러 줄 JSX 최소 반례를 회귀 시험으로 추가했다.

## 재검토 범위

동일한 두 reviewer가 새 불변 후보에서 CSS selector 정규화·specificity·조건 교집합·주석 gap·빈 목록과 descendant 오류, JSON 숫자·깊이·오류 채널, `--json=` 입력 redaction, MDX inline·blockquote·fenced·tilde·tagged·배열·삼항·중첩 object·다중행·들여쓰기 없는 ESM·JS 주석·문단 밖 delimiter·같은 문단의 미종결 span 뒤 HTML/JSX·MDX expression·여러 줄 JSX expression·blockquote 빈 문단·파일 첫 span·3자 inline span·backslash delimiter·escaped template과 보간 주석, Git diff 추가 행, symlink root, airport task/evidence를 Windows Python 3.14와 WSL Python 3.11에서 독립 재현한다. 소비자 저장소, npm/PyPI registry, workflow dispatch와 실제 소비자 build/e2e는 호출하지 않는다.

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
git diff --check bd73856ac1d3327b1fe46acc352163eee23ad504 c0c93c47e5f25aa0879fd0fb4e56261f6f624138
```

두 reviewer는 이 manifest와 candidate commit/tree를 읽은 뒤 상대 결과를 보지 않고 각각 원본 report를 확정한다. 실행하지 않은 소비자 gate와 registry·게시 검증은 `NOT_RUN`으로 유지한다.
