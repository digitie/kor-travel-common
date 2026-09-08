# T-103 post-fix-31 독립 적대적 리뷰 B 원본

- 실행 ID: `T103-PF31-B-20260908-170405`.
- 시작 KST: `2026-09-08T17:04:05.9264403+09:00`.
- 불변 제품 HEAD: `b2fc22b352a1122f465852737f6f0ae7a228ddae`; tree: `be501ae5592c6c20edc235cc6f3516f8817ce9ac`.
- 격리: `F:/dev/kor-travel-common-wt/review-t103-post31-b` detached checkout, 시작 `git status --porcelain` 출력 없음. 제품·manifest·소비자·기존 evidence·공유 branch를 수정하지 않았다. 보고서 작성 후 이 파일만 별도 branch에서 커밋한다.
- manifest: `910599e`의 `docs/reviews/adversarial/evidence/2026-09-08-t103-post-fix-31-manifest.md`를 `git show`로 읽었다. Git blob SHA-256: `ca16cc86018e014d1c32c0e521af06cfb7ef44818c0955840c1121977c60a95e`.
- delta: `620e477bf841f881e6090cccefcbad81cfffe6e7..b2fc22b352a1122f465852737f6f0ae7a228ddae`. 제품 2파일(`tools/ux_lint.py`, `tests/test_ux_lint.py`) 전체 diff를 읽었다. 다른 3개 변경 경로는 이전 manifest·A/B 원본이며 상대 본문을 읽거나 요청하지 않았다.
- source `.git/config` 시작 SHA-256: `0A0F849E7874CF0A25926856F9D2E381CCBF4C2DCB5999869C57B86E0F5BEB5B`. Git 설정·후보 코드 변경 및 push는 하지 않았다.

## 전달 요청 원문

> post-31 독립 적대 리뷰를 시작해 주세요. immutable candidate b2fc22b352a1122f465852737f6f0ae7a228ddae, tree be501ae5592c6c20edc235cc6f3516f8817ce9ac. manifest 2026-09-08-t103-post-fix-31-manifest.md (commit 910599e). 상대 raw를 읽지 말고 detached clean worktree에서 시작/종료 SHA/tree·clean을 기록하세요. 독립 Markdown parser 대조, 중간 tilde/backtick fence·plain/blockquote/nested·indent/tab-stop·Git added-line/base·오류/redaction을 양 OS에서 점검하세요. 단일 report-only raw commit과 SHA256을 회신하고 후보/manifest/evidence는 수정하지 마세요.

## 판정

**NO-GO**. B-P1-23의 일반 문장 뒤 inline 연결은 남아 있다. 신규 B-P2-25는 정상 인용을 처리하던 입력에 traceback·출력 유실을 일으킨다. P0 및 신규 P1/P3는 발견하지 않았다. 일반 회귀시험 성공과 해당 반례의 실패를 구분한다.

| ID·원 심각도 | disposition | 확인 범위 |
|---|---|---|
| B-P1-23 | OPEN(부분 수정) | invalid-info 뒤 중간 tilde fence는 FIXED. 일반 prose opener는 다음 block fence까지 계속 연결해 P6/P8을 누락한다. |
| B-P2-25 | 신규 OPEN | 1/2자 backtick·tilde 행에서 반환형 계약 위반으로 TypeError 발생. |
| B-P2-13 | FIXED 유지 | 파일 첫/같은 행 및 quoted/nested 4열·tab-stop 정상 inline 대조 통과. |
| B-P3-24 | FIXED | manifest focused 66 표기와 이번 독립 focused 실행 건수가 일치한다. |
| B-P1-01/02/03/04, B-P2-05/06, B-P3-07, B-P1-08/09, B-P2-10, B-P1-11/12/14/15/16, B-P2-17/18/19/20, B-P1-21/22 | FIXED 유지(검증 범위 한정) | 변경 없는 코드 범위는 동일성으로 이전 판정을 재사용하고 이번 full/focused와 직접 corpus를 실행했다. 과거 모든 개별 CLI corpus를 전부 반복했다고 주장하지 않는다. |

### B-P1-23 — 일반 prose inline 경로가 block fence를 넘는 누락

- 위치: `tools/ux_lint.py:433`~449 `_find_inline_span_end`, `:843`~852 일반 다중 backtick 처리. 새 중간 fence 검사는 `:687` 이후 invalid-info fallback에만 연결돼 있다.
- 반례 입력: Python으로 `"Example " + chr(96)*3 + 'literal\n{window.confirm("x")}\n' + chr(96)*3 + "\n"`. UTF-8 SHA-256 `cf380531ead499a71602bc32fff9b0ec5d0343ccf864217a0ead35c9c831c6e7`.
- 기대: 마지막 줄은 새 fenced block이며 앞 두 줄의 실행식은 code span 밖이다. `--fail-new` 및 신규 추가행 `--base`는 P8·exit 1. 실제 두 OS: exit 0, `findings=[]`.
- 재현: `t103-post28-b-new.py` 216교차 중 prose 72개가 실패하고, `t103-post30-b-new.py` 120교차 중 prose 36개가 실패한다. plain/blockquote/nested·3/4자 run·LF/CR/CRLF·전체/`--base`를 포함한다. 이전 중간 tilde 12개는 이번에는 기대대로 검출된다.
- 영향: 소비자 baseline 예외가 없어도 실제 MDX/JSX 신규 금지 패턴이 검사 gate를 통과한다. 기존 원인의 부분 수정이며 별도 신규 P1로 중복 집계하지 않는다.
- 최소 수정: inline 끝 검색이 일반 경로에서도 block 경계를 지키도록 공통 판정을 적용하고, block 시작에서 검색을 끝낸 뒤 실행식 스캔을 이어간다. 정상 같은 문단/4열/tab-stop inline 음성 대조는 보존한다.

### B-P2-25 — 정상 inline의 짧은 marker가 TypeError를 발생시킴

- 위치: `tools/ux_lint.py:452` 반환형 `tuple[int, str] | None`, `:478`~479의 `run < 3: return False`, `:502`~503의 `candidate is not None and candidate[0] < boundary`.
- 최소 입력은 다음 Python 문자열이다. UTF-8 SHA-256 `5491ce3a82968229f808d76f78e7f01d13bfe14953256782ee3684a92fba3675`.

~~~~python
text = '```bad`info\n`\n{window.confirm("x")}\nclose ```\n'
~~~~

- 기대: 같은 문단에서 닫힌 3자 inline code이므로 findings 없음·exit 0·요청한 구조화 출력 생성. 실제: Windows/WSL 모두 exit 1, stdout 비어 있음, stderr `TypeError: 'bool' object is not subscriptable` traceback.
- 원인: 새 helper가 tuple/None 대신 False를 반환한다. 호출자는 False를 None이 아닌 fence 후보로 받아 인덱싱한다. 기존 bool helper에서 tuple helper로 바꾼 이번 delta의 회귀다.
- 직접 72교차/OS: plain/quoted/nested × 내부 1/2자 backtick·tilde × LF/CR/CRLF × 전체/`--base`, 전부 기대 0 대신 위 예외다. 입력 root 문자열 노출은 발견하지 않아 비밀 유출 finding으로 확대하지 않는다.
- 수정 전/후 별도 8관찰/OS: delta base `620e477` 코드에서는 Markdown·JSON·명시적 `--step-summary`·환경 `GITHUB_STEP_SUMMARY` 모두 exit 0, 요청한 summary 생성. 후보는 네 채널 모두 exit 1, stdout 없음·summary 미생성·traceback이다. base 사본의 `tools/ux_lint.py`가 `620e477`과 동일함을 `git diff` 무출력으로 확인했다.
- 영향: 유효한 인용 문서를 위반처럼 종료시키고 JSON 및 CI summary 계약을 깨뜨린다. 일반 입력 오류 exit 2로 바꿀 문제가 아니라 정상 입력의 잘못된 실패다.
- 최소 수정: 해당 helper의 모든 반환 분기를 tuple/None 계약으로 통일한다. 3자 미만 marker는 유효 fence가 아니므로 다음 container 판정 또는 None으로 처리하고, 짧은 marker 4종·양 OS·출력 채널을 회귀 대조한다. 포괄적 예외 처리만 추가해 정상 입력을 계속 실패시키지 않는다.

## 독립 parser와 명령

Windows에 이미 있는 `markdown-it-py 4.2.0`의 `MarkdownIt('commonmark')`로 새 12종 AST를 확인했다. B-P2-25 입력은 plain/quoted/nested 모두 단일 `code_inline`이며 내부 짧은 marker는 fence가 아니다. B-P1-23은 paragraph `[0,2]` 뒤 fence `[2,3]`이고 실행식이 code span에 속하지 않는 기존 독립 parser 결과와 동일한 입력/규약이다. [CommonMark 0.31.2](https://spec.commonmark.org/0.31.2/#precedence)의 block 우선 및 [code span](https://spec.commonmark.org/0.31.2/#code-spans) 기준으로 판단했다. 실제 MDX compiler 실행으로 기록하지 않는다.

`ROOT`는 위 격리 worktree, `AUDIT`는 source `.git/codex-audit`이며 probe/로그는 후보 밖에만 저장했다. Windows `py -3.14 -B -X utf8`, WSL `/home/digitie/.local/share/uv/python/cpython-3.11.15-linux-x86_64-gnu/bin/python3.11 -B -X utf8`를 사용했다. 환경 `GIT_*`를 제거한 임시 Git 사본/합성 저장소에서만 fixture를 썼다.

```text
python AUDIT/t103-post31-b-run.py ROOT win|wsl tests
  -> review-t102-b-wsl-unittest.py ROOT (임시 독립 사본 unittest discover)
  -> python -m unittest tests.test_kt_contrast tests.test_ux_lint
  -> review-t102-post-b-gates.py ROOT (임시 독립 사본 static/aliases focused)
python AUDIT/t103-post31-b-run.py ROOT win|wsl corpus
  -> t103-post26/27/28/29/30-b-new.py, t103-post9-b-corpus.py
python AUDIT/t103-post31-b-new.py ROOT OUTPUT.json
python AUDIT/t103-post31-b-new.py ROOT unused oracle
python AUDIT/t103-post31-b-channels.py ROOT BASE_ROOT OUTPUT.json
python ROOT/tools/ux_lint.py --root TEMP --fail-new --json [--base BASE]
git diff --check 620e477 b2fc22b
```

`TEMP`는 합성 `Page.mdx`에 `safe\n`을 기록해 그 파일만 add/commit한 임시 저장소이며 `BASE`는 그 commit이다. 입력을 위 반례로 바꾸고 CLI를 실행한다. 새 경계 스크립트는 subprocess의 stderr/exit/summary를 직접 수집했으며 제품 코드나 registry를 변경하지 않는다.

## 검증 범위와 NOT_RUN

- exact CI를 직접 `gh run list --commit b2fc22b352a1122f465852737f6f0ae7a228ddae` 및 `gh run view 34202002476 --json headSha,status,conclusion,jobs`로 조회했다. [run 34202002476](https://github.com/digitie/kor-travel-common/actions/runs/34202002476)은 정확한 후보 headSHA, PR/completed/success, 6개 job과 각 source SHA 확인 step success다. 전체 job 로그 다운로드는 NOT_RUN.
- `git diff --check 620e477 b2fc22b`: Windows exit 0, 출력 없음. WSL 별도 diff 명령은 NOT_RUN.
- task/resume/규범·패키지·라이선스·버전·CI·소비자 경계는 이번 delta에 변경이 없어 이전 확인을 동일성으로 재사용한다. T-103은 IN_PROGRESS이며 소비자 baseline 등록/워크플로 T-010 실행을 common 구현 완료로 대신하지 않는다.
- NOT_RUN: Windows Python 3.11(부재), 실제 소비자 build/type/e2e·manifest, npm/PyPI 설치·게시, workflow dispatch, MDX compiler/browser, WSL 독립 Markdown parser, 이번 범위 밖의 이전 모든 개별 probe 전수 재실행. 선택 skip을 실행 성공으로 세지 않는다.
- 이 원본의 검증은 오직 명시한 immutable 후보에 귀속된다. 새 수정 후보의 통과 증거로 전용할 수 없다. 실제 완료 건수와 종료 상태는 아래에 기록한다.

## 실행 완료 기록

| 검증 | Windows Python 3.14.3 | WSL Python 3.11.15 |
|---|---|---|
| 전체 unittest | 304개 실행, skip 0, 164.883초, exit 0 | 304개 수집/301개 실행, skip 3, 34.272초, exit 0 |
| contrast/UX focused | 66개, skip 0, 47.690초, exit 0 | 66개, skip 0, 25.582초, exit 0 |
| aliases focused | 35개, skip 0, 1.677초, exit 0 | 35개 수집/34개 실행, skip 1, 0.169초, exit 0 |
| plan / links | 106 task 오류 0 / 484문서·2481대상 오류 0 | 동일 |
| SPDX / secrets / redaction | 56파일 오류 0 / 각각 616파일 발견·예외 0 | 동일 |
| versions self-check / aliases | exit 0(consumer NOT_RUN) / CSS 1 오류 0 | 동일 |

WSL 전체의 skip 3은 Windows 8.3 전용 1개와 선택 jsonschema 부재 2개다. 통과 개수로 포함하지 않았다. CI의 Windows/Ubuntu 결과와 이 WSL 로컬 의존성 차이를 구분한다.

직접 결과는 각 OS 785행이다: 기존 26/27/28/29/30 corpus 각각 72/144/216/48/120행, 초기 원본 경계 corpus 105행, 신규 72행, base/candidate 출력 채널 8행이다. 양 OS의 8개 JSON 파일이 모두 동일하다. 28그룹 72행 및 30그룹 36행은 B-P1-23, 신규72행은 B-P2-25이며 채널8행 중 후보4행은 같은 P2의 별도 출력 관찰이다. 나머지 명시적 기대 불일치는 없다. 이 수치는 중복 없는 테스트 개수나 모든 개별 입력의 무결점 보증이 아닌 실행 관찰 행 수다.

종료 관찰 KST `2026-09-08T17:10:02.5030033+09:00`: HEAD/tree는 위 제품 후보와 동일하다. status는 자신의 새 원본 한 파일만 untracked이고 제품 파일 변경은 없다. `.git/config` 종료 SHA-256도 시작 값과 같다. 보고서-only 커밋 뒤 clean과 raw tree, 파일/Git blob 동일 SHA-256을 확인해 완료 메시지로 전달한다.
