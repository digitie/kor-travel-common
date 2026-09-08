# T-103 수정 후 적대적 리뷰 7 기준선

- 리뷰 단계: post-fix-06 NO-GO finding 수정 후 일곱 번째 독립 재검토
- 불변 코드 후보 commit: `63fe3d5c969b28bab4d528d3e24a054e3a8e30e6`
- 불변 코드 후보 tree: `c9fb07160de150d7a4cfbbb31fc226cb6a9fb3af`
- post-fix-06 기준선 commit: `a40668bfb4ecac66d141da2ff791947d77208bd7`
- post-fix-06 기준선 tree: `9c5cbf93bc6b34c4895c98745404375becbc0b32`
- post-fix-06 manifest commit: `6372b29f40abaf2168594fdf792eb44009264a54`
- post-fix-06 A 원본 report commit: `0e342d44e2ac6e4eb7a1e5432f114298c7a5a538`
- post-fix-06 B 원본 report commit: `e6169d027ddfaada9d1dcb478e8648adf38e5adf`
- post-fix-06 A 원본 report SHA256: `5342B57753AC99432731839B8EB3DDE196ED0A3978A72742EA60E646D65E19AF`
- post-fix-06 B 원본 report SHA256: `8618ce6d31a70dc64866f2bd36ba2458ce995a2a5315aa4a5b74b14bbe1d0413`
- 이번 수정: 중첩 JSX object expression과 들여쓰기 없는 ESM 실행 문맥, 닫히지 않은 inline delimiter 이후 실행 영역, `:root` descendant·빈 selector list 입력을 상태 추적·generic 오류·회귀 시험으로 고정

## 재검토 범위

동일한 두 reviewer가 새 불변 후보에서 CSS selector 정규화·specificity·조건 교집합·빈 목록과 descendant 오류, JSON 숫자·깊이·오류 채널, `--json=` 입력 redaction, MDX inline·blockquote·fenced·tilde·tagged·배열·삼항·중첩 object·다중행·들여쓰기 없는 ESM·escaped template과 보간 주석, Git diff 추가 행, symlink root, airport task/evidence를 Windows Python 3.14와 WSL Python 3.11에서 독립 재현한다. 소비자 저장소, npm/PyPI registry, workflow dispatch와 실제 소비자 build/e2e는 호출하지 않는다.

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
git diff --check 94ca2f1730b270721eb6242bfcdd9362b51d45e5 63fe3d5c969b28bab4d528d3e24a054e3a8e30e6
```

두 reviewer의 post-fix-07 원본 report가 이 기준선 commit/tree와 일치한 뒤 최종 판정을 기록한다. 실행하지 않은 소비자 gate와 registry·게시 검증은 `NOT_RUN`으로 유지한다.
