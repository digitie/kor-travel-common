# T-103 post-fix-30 독립 적대적 리뷰 B 원본

- 실행 ID: `T103-PF30-B-20260908-164615`
- 시작 KST: `2026-09-08T16:46:15.7177582+09:00`; 제품 종료 관찰 KST: `2026-09-08T16:50:44.3658647+09:00`.
- 제품 시작/종료 HEAD: `620e477bf841f881e6090cccefcbad81cfffe6e7`; tree: `ee2964452454b255a47a27aea1edb1a0c5ede2db`; 두 번 모두 `git status --porcelain` 출력 없음.
- 격리: `F:/dev/kor-travel-common-wt/review-t103-post30-b`에 detached checkout. 보고서 작성 때만 `codex/review-t103-post30-b`로 전환했으며 제품 파일은 변경하지 않았다. 커밋은 이 원본 한 파일만 포함한다.
- delta: `9afea549dd81cb23d3297f83d89df4b519734382..620e477bf841f881e6090cccefcbad81cfffe6e7`. 제품 2파일의 전체 diff를 읽었다. 다른 3파일은 이전 manifest와 A/B 원본 추가이며 경로만 확인하고 A 본문은 읽지 않았다.
- manifest: `43d5c3d`의 `docs/reviews/adversarial/evidence/2026-09-08-t103-post-fix-30-manifest.md`를 `git show`로 읽었다. Git blob SHA-256: `a8abf924e4301dab3ea79ebb810c7acb6db277f7fb0b74af8faf783aedcad0a9`.
- source `.git/config` 시작/종료 SHA-256: `0A0F849E7874CF0A25926856F9D2E381CCBF4C2DCB5999869C57B86E0F5BEB5B`. Git 설정·후보·소비자·기존 evidence 수정과 push, registry 호출은 하지 않았다. 상대 이번/과거 raw 본문을 읽거나 요청하지 않았다.

## 전달 요청 원문

> post-30 독립 적대 리뷰를 시작해 주세요. immutable candidate commit 620e477bf841f881e6090cccefcbad81cfffe6e7, tree ee2964452454b255a47a27aea1edb1a0c5ede2db. manifest 2026-09-08-t103-post-fix-30-manifest.md (commit 43d5c3d). 상대 reviewer raw를 읽지 말고 detached clean worktree에서 시작/종료 SHA/tree·clean을 기록하세요. B 범위: 독립 Markdown parser 대조, Git added-line/base, container depth 변화, 4열/tab-stop, 정상 inline false positive·실행식 누락·오류/redaction, plain/blockquote/nested 양 OS. 후보/manifest/소비자/evidence는 수정하지 말고 단일 report-only raw commit을 만들어 verdict·findings·SHA256을 회신하세요.

후속 지시: 현재 findings를 단일 report commit으로 즉시 확정하라는 요청에 따라 추가 탐색을 중단했다. 아래 결과와 명시한 미검증을 구분한다.

## 판정과 disposition

**NO-GO**. B-P1-23이 부분 수정 상태로 남았다. B-P2-13의 quoted 콘텐츠 4열 오검출은 FIXED다. B-P3-24의 manifest focused 건수는 여전히 불일치한다. 신규 P0/P1/P2/P3 ID는 없다.

| ID·원 심각도 | disposition | 이번 후보 확인 |
|---|---|---|
| B-P1-23 | OPEN(부분 수정) | invalid info의 quote 전환은 FIXED. prose opener와 중간 fence를 건너는 inline 검색이 실행식을 가린다. |
| B-P2-13 | FIXED | 파일 첫 동일 행 inline, quoted/nested 콘텐츠 4열·탭 inline을 정상 제외한다. |
| B-P3-24 | OPEN | manifest focused 64 표기, 독립 WSL 실행은 65개·skip 0이다. |
| B-P1-01/02/03/04, B-P2-05/06, B-P3-07, B-P1-08/09, B-P2-10, B-P1-11/12/14/15/16, B-P2-17/18/19/20, B-P1-21/22 | FIXED(아래 실행 corpus 범위) | WSL 누적 원 반례 재현에서 별도 신규 불일치 없음. Windows 전체 직접 corpus가 끝나지 않은 부분은 미검증으로 구분한다. 일반 기능 전체의 무결점 주장이 아니다. |

### B-P1-23 — inline 검색이 Markdown block 경계를 넘어서 실행식 누락

- 위치: `tools/ux_lint.py:433`~449의 `_find_inline_span_end`, `:667`~674의 invalid-info fallback, `:819`~828의 일반 다중 backtick 처리.
- 반례 1 입력을 Python 문자열로 정확히 쓰면 `'Example ' + '`' * 3 + 'literal\n{window.confirm("x")}\n' + '`' * 3 + '\n'`이다. UTF-8 SHA-256은 `cf380531ead499a71602bc32fff9b0ec5d0343ccf864217a0ead35c9c831c6e7`이다.
- 기대: 마지막 줄은 새 fenced block opener이고 첫 두 줄은 닫힌 code span이 아니다. P8을 line 2에서 검출하고 `--fail-new`와 신규 파일의 `--base` 모두 exit 1이어야 한다. 실제: 두 OS 모두 exit 0, `findings=[]`, traceback 없음.
- 반례 2 입력: `'```bad`info\n~~~\ndocumentation\n~~~\n{window.confirm("x")}\nclose ```\n'`. SHA-256은 `232ce0a257a729facbdc49f52cf56d186e36bf34c571b42f62726c92cb4e1844`이다. 중간 tilde fence가 첫 문단을 끝내고 실행식은 뒤 문단에 놓인다. 기대 P8/exit 1, 실제 두 OS exit 0/빈 findings다.
- 현재 변경은 닫힘 후보 위치에서만 새 fence 여부를 확인한다. 일반 prose 경로는 그 검사도 호출하지 않으며, invalid-info 경로에서도 opener와 closing 사이의 다른 block을 보지 않는다. 이는 기존 B-P1-23의 남은 동일 원인이다. 수정 전/후 일반 경로가 그대로임을 전체 delta와 재실행으로 확인했다.
- 새 독립 120개 CLI 교차/OS: plain·quoted·nested prose 36개와 중간 tilde 12개, 합계 48개가 누락됐다. 3/4자 run × LF/CR/CRLF × 전체/`--base`를 포함한다. 다른 72개는 기대와 일치한다. 별도 기존 prose corpus 216개/WSL 중 72개도 같은 누락이다.
- 영향: 문서의 실제 MDX 실행식 또는 JSX 금지 패턴이 새 Git 추가행이어도 fail gate를 통과한다. baseline/소비자 승인과 무관한 입력 파싱 결함이다.
- 최소 수정: 일반/invalid-info inline 경로가 동일한 Markdown block 경계를 사용하게 하고, 닫힘 위치뿐 아니라 중간 block 시작에서 검색을 종료한다. 종료 뒤 실행식 스캔을 계속하며 정상 같은 문단 inline·4열 closing 음성 대조를 보존한다.

### B-P3-24 — focused 실행 건수 불일치

- 위치: manifest `43d5c3d`의 고정 검증 표 Windows/WSL focused 두 행.
- 이번 후보는 unittest 한 개를 추가했다. 독립 `python -B -X utf8 -m unittest tests.test_kt_contrast tests.test_ux_lint` WSL 결과는 `Ran 65 tests ... OK`, skip 0이다. manifest의 64와 다르다.
- 영향: gate 실행 증거의 검증 단위 수를 잘못 전달한다. 제품 결함과 별도 P3이며, 0 test/skip을 PASS로 세었다는 finding은 아니다.
- 권고: 불변 manifest 원본을 덮어쓰지 않고 후속 manifest/종료 evidence에서 실제 65와 OS별 skip을 기록한다.

## 독립 parser 대조와 재현 명령

Windows에 이미 설치된 `markdown-it-py 4.2.0`의 `MarkdownIt('commonmark')`로 새 10종 입력 AST를 직접 확인했다. 반례 1은 `paragraph [0,2]` + `fence [2,3]`, 반례 2는 `paragraph [0,1]` + tilde `fence [1,4]` + `paragraph [4,6]`이고 실행식은 `code_inline`에 속하지 않는다. quoted 4열/tab-stop 정상 대조는 하나의 `code_inline`이다. [CommonMark 0.31.2 precedence](https://spec.commonmark.org/0.31.2/#precedence), [fenced code blocks](https://spec.commonmark.org/0.31.2/#fenced-code-blocks), [code spans](https://spec.commonmark.org/0.31.2/#code-spans)를 조회해 block 먼저 결정하는 기준과 대조했다. 실제 MDX compiler 실행으로 표기하지 않는다.

공통 명령의 `ROOT`는 위 격리 worktree, `AUDIT`는 source의 `.git/codex-audit`이다. Windows는 `py -3.14 -B -X utf8`, WSL은 `/home/digitie/.local/share/uv/python/cpython-3.11.15-linux-x86_64-gnu/bin/python3.11 -B -X utf8`로 실행했다. 환경의 `GIT_*`를 제거한 임시 Git 저장소에 합성 파일만 썼다.

```text
python AUDIT/review-t102-b-wsl-unittest.py ROOT
python -m unittest tests.test_kt_contrast tests.test_ux_lint
python AUDIT/review-t102-post-b-gates.py ROOT
python AUDIT/t103-post30-b-run.py ROOT win|wsl corpus
python AUDIT/t103-post30-b-new.py ROOT AUDIT/t103-post30-b-OS-new30.json
python AUDIT/t103-post30-b-new.py ROOT unused oracle
python ROOT/tools/ux_lint.py --root TEMP --fail-new --json
python ROOT/tools/ux_lint.py --root TEMP --fail-new --json --base BASE
```

`TEMP`는 `git init` 후 `Page.mdx`에 `safe\n`을 기록하고 그 파일만 add/commit한 독립 합성 저장소다. `BASE`는 그 commit이며 위 반례로 해당 파일을 바꿔 두 CLI를 실행한다. 제품/소비자 Git 설정·파일을 바꾸지 않는다. probe와 로그는 후보 밖에만 보관하며 제품 커밋에는 넣지 않는다.

## 실행 결과와 한계

- Windows Python 3.14.3 full: 303개 실행, skip 0, 201.333초, exit 0. WSL Python 3.11.15 full: 303개 수집/300개 실행, skip 3, 34.500초, exit 0. WSL skip은 Windows 8.3 전용 1개와 선택 jsonschema 의존성 부재 2개이며 성공한 시험으로 세지 않는다.
- WSL focused: 65개, skip 0, 27.112초, exit 0. WSL static: plan 106 오류 0; link 481문서/2478대상 오류 0; SPDX 56 오류 0; secrets/redaction 각 613파일 발견·예외 0; versions self-check exit 0(consumer 검사 NOT_RUN); aliases CSS 1 오류 0. aliases focused는 35개 수집/34개 실행/skip 1, exit 0.
- WSL 누적 원본 corpus 1743행 + 이번 직접 120행을 실행했다. `new28` 72건과 `new30` 48건이 위 P1이며 다른 명시적 기대 exit 불일치는 없다. 기존 oracle의 기대 미정 12행은 성공으로 집계하지 않는다. `corpus/late/latest/new18..new29/repro24`에는 CSS cascade·selector/media·deep/huge JSON·argparse·오류 redaction·symlink·Git diff `+++`/CR/LS/PS·MDX Unicode·fence suffix/container·4앱 사례가 포함된다.
- Windows 누적 corpus의 완료분 및 나머지 gate는 아래 확정 부록에 기록한다. 새 120개 Windows/WSL JSON은 완전히 동일하다. 이미 완료된 corpus/late/new18..21도 동일하며 latest의 차이는 Python Unicode DB 버전 metadata다. 아직 실행 완료를 확인하지 않은 그룹은 parity PASS로 표시하지 않는다.
- `git diff --check 9afea549 620e477`: Windows exit 0, 출력 없음. WSL 별도 diff check는 NOT_RUN. 단계별 helper는 후보를 외부 임시 디렉터리로 복사하고 자체 Git index를 생성한다.
- exact 후보 CI: `gh run list --commit 620e477bf841f881e6090cccefcbad81cfffe6e7` 및 `gh run view 34200652371 --json headSha,status,conclusion,jobs` 직접 조회. [run 34200652371](https://github.com/digitie/kor-travel-common/actions/runs/34200652371)의 headSHA가 후보와 같고 PR event/completed/success, packages·secret-scan·check-versions·tools Windows·tools Ubuntu·docs 6개 job 및 각 source SHA 확인 step 모두 success. 전체 job 로그 다운로드는 NOT_RUN.
- task T-103은 IN_PROGRESS, 소비자 baseline과 워크플로 T-010 후속 소유를 유지한다. 문서 라우터·resume·상세 task를 대조했고 이번 제품 delta에 패키지/버전/라이선스/소비자 코드 변경은 없다. 실패를 완료/릴리스 가능으로 표기하지 않는다.
- NOT_RUN: Windows Python 3.11(부재), 실제 소비자 build/type/e2e 및 manifest 검사, npm/PyPI 게시·설치, workflow dispatch, MDX compiler/browser, WSL 독립 Markdown parser, 비UTF-8 Git 출력의 별도 신규 주입. 검증 실행은 고정 후보에만 귀속되며 이후 수정 후보의 결과로 사용할 수 없다.

## 원본 확정 부록

- `2026-09-08T16:53:25.5468212+09:00`까지 수집한 Windows 결과: focused 65개·skip 0·49.464초·exit 0. 위 7종 static gate는 WSL과 건수/오류가 같고 모두 exit 0이다. aliases focused는 35개·skip 0·1.872초·exit 0이다. 따라서 B-P3-24는 두 OS 모두 64 표기가 실제 65와 어긋난다.
- Windows 누적 corpus는 `corpus/late/latest/new18..new27` 1467행까지 완료됐으며 이번 `new30` 120행을 합해 1587행의 결과를 수집했다. 명시적 기대와 다른 것은 새 48행의 B-P1-23이다. WSL 대응 그룹과 JSON을 비교했고 `latest`의 Unicode DB 버전 metadata 외에는 동일하다.
- Windows 잔여 `new28/new29/repro24`의 완전한 결과 수집은 `NOT_RUN(원본 즉시 확정 지시에 따른 실행 미완료/중단)`으로 남긴다. WSL 해당 그룹은 완료됐다. 이 미완료를 0건/성공으로 세지 않는다. 새120개 양 OS 직접 재현과 WSL 전체 corpus로 위 NO-GO 및 B-P2-13 수정 판정을 내렸으며, 미실행 Windows 잔여 때문에 NO-GO를 약화하지 않는다.
- 이 파일은 수정 후보·통합 판정이 아닌 고정 후보에 대한 독립 원본이다. 보고서-only commit SHA와 이 파일의 파일/Git blob 동일 SHA-256은 커밋 후 완료 메시지로 전달한다.
