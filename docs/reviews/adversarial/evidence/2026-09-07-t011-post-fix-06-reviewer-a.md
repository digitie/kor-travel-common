# T-011 post-fix-06 독립 적대적 리뷰 A 원본

- 실행 ID: A-T011-POST6-20260907-210115
- 최종 판정: **BLOCK**. 직전 A-T011-P2-13/14는 FIXED이며, 이번에 새로 확인한 기존 결함 A-T011-P2-15가 OPEN이다. 새 P0/P1 없음. 이번 수정이 새로 만든 회귀라고 주장하지 않는다.
- immutable candidate: `56d6ae11d5917eb2b2e69f8f26f90b903bacceb6`
- 전체 기준 base: `3977c00a5b4ffa21a8d29f96dd9531efbe3a0cb5`
- candidate tree: `845442686054c6707bfd1d76bab330e79749b3c1`
- 격리: `F:/dev/kor-travel-common-wt/review-t011-post6-a`, 새 detached worktree.
- 시작 시각: 2026-09-07 21:01:15.675 KST. 종료 상태 확인: 2026-09-07 21:05:09.315 KST.
- 시작/종료 `git rev-parse HEAD 'HEAD^{tree}'`는 위 SHA/tree와 동일. 시작/종료 `git status --porcelain=v1`는 빈 출력(clean).
- 후보 소스·문서·시험·source `.git/config` 및 `core.worktree`는 수정하지 않았다. 소비자 저장소 쓰기, commit/push, registry 게시 없음. 재현 입력은 임시 디렉터리, 보존 probe/원본은 main `.git/codex-audit/`에만 썼다.
- 이전 리뷰 원문과 상대 reviewer 결과는 열람하지 않았다. 보유 A probe 코드를 새 후보에서 재실행했으며 과거 결과를 성공 근거로 재사용하지 않았다.

## 요청과 검토 범위

정확한 후보와 원 base를 고정하여 직전 A-T011-P2-13(빈 lockfiles app의 중간 symlink 조기 반환), A-T011-P2-14(validator registry self-symlink의 WSL traceback/path leak)를 양 OS에서 직접 재현하고, direct/중간/외부/self symlink, 누락 app/lock/manifest/registry, workspace, requirements recursion, redaction, schema parity 및 기존 corpus를 재검토하도록 요청받았다. PASS 조건은 새 P0/P1/P2 0건과 기존 finding FIXED이며, 미실행은 NOT_RUN으로 남긴다.

원 base..candidate는 39파일(+2435/-58)이다. 직전 코드 후보 94c445ec..candidate의 5파일(+40/-5) delta를 전부 직접 읽었다. 제품 변경은 app의 존재성 검사 이전 symlink 검사, validator registry의 사전 resolve 제거, shared validator의 RuntimeError 포착, 새 회귀 시험, task의 경계 설명이다. 현재 문서 라우터·resume·상세 task·정본 및 전체 변경 목록을 확인했다. 이전 raw/report 본문은 비열람 지시 때문에 다시 읽지 않았고 전체 tracked 파일의 정적 gate는 실행했다.

## 실제 검증

Windows Python 3.14.3, WSL uv managed Python 3.11.15. schema 검증 라이브러리는 jsonschema 4.26.0이다. 후보 루트에서 실행했으며 WSL에는 `uv run --no-project --python 3.11 --with jsonschema==4.26.0 python`을 사용해 선택 의존성 미설치 skip을 없앴다.

| 명령 | Windows | WSL |
|---|---|---|
| `python -B -X utf8 -m unittest discover -s tests -q` | 202 tests, 61.803초, OK, skip 0 | 202 tests, 38.760초, OK, skip 0 |
| `python -B -X utf8 -m unittest discover -s tests -p test_validate_manifest.py -q` | 23 tests, 5.193초, OK, skip 0 | 23 tests, 3.955초, OK, skip 0 |
| `tools/validate_plan.py` | 106 task, 오류 0 | 동일 |
| `tools/validate_document_links.py` | 344 documents, 2287 targets, 오류 0 | 동일 |
| `tools/check_spdx.py` | 32파일, 오류 0 | 동일 |
| `tools/scan_secrets.py --all` | 434파일, 발견 0, 예외 0 | 동일 |
| `tools/check_prod_redaction.py --all` | 434파일, 발견 0, 예외 0 | 동일 |
| `tools/check_versions.py --self-check` | exit 0 | exit 0 |
| `git diff --check 3977c00a5b4ffa21a8d29f96dd9531efbe3a0cb5 HEAD` | exit 0 | exit 0 |

Python 도구에는 모두 `-B -X utf8`를 사용했다. 정적 gate harness는 `.git/codex-audit/t011-post6-a-gates.py`이다. WSL에서 Git을 읽는 도구에는 프로세스 환경으로만 `GIT_DIR=/mnt/f/dev/kor-travel-common/.git/worktrees/review-t011-post6-a`, `GIT_WORK_TREE=/mnt/f/dev/kor-travel-common-wt/review-t011-post6-a`를 설정했다.

`gh pr view 10 --repo digitie/kor-travel-common --json headRefOid,statusCheckRollup`의 head가 정확한 후보와 일치했다. 처음에는 일부 실행 중이었고 최종 조회에서는 [CI run 34119572392](https://github.com/digitie/kor-travel-common/actions/runs/34119572392)의 docs, tools(ubuntu-24.04), tools(windows-2025), secret-scan, check-versions 5개가 모두 SUCCESS였다. 위 시험 건수는 원격 추정이 아닌 독립 로컬 실행 결과다.

## 반례 재현과 disposition

실행한 보존 harness:

```text
Windows cwd: F:/dev/kor-travel-common-wt/review-t011-post6-a
python -B -X utf8 F:/dev/kor-travel-common/.git/codex-audit/t011-post6-a-run.py

WSL cwd: /mnt/f/dev/kor-travel-common-wt/review-t011-post6-a
uv run --no-project --python 3.11 --with jsonschema==4.26.0 python -B -X utf8 /mnt/f/dev/kor-travel-common/.git/codex-audit/t011-post6-a-run.py
```

- **A-T011-P2-13 FIXED**: 빈 lockfiles + `app=loop/etl`, 중간 디렉터리 self-symlink는 양 OS `exit 2, traceback False, report False`다. 외부 symlink 아래 missing app도 동일하다. 새 helper가 존재성 조기 반환보다 먼저 호출되는 것을 코드로 확인했다.
- **A-T011-P2-14 FIXED**: 정상 초안 + validator registry self-symlink는 양 OS `exit 1, traceback False, runtime-error False, path-leak False`다. registry의 사전 resolve를 제거하고 파일 읽기 오류를 일반 진단으로 포착했다.
- **A-T011-P2-12 FIXED 유지**: workspace/중간 lock 디렉터리 loop는 양 OS exit 2, traceback/보고서 없음.
- **A-T011-P1-01/02/08, A-T011-P2-03/04/05/06/07/10/11 FIXED 유지**: 아래 corpus를 새 후보에서 실행해 원 코드 경계의 재발을 찾지 못했다.
- 문서 집계 A-T011-P3-09의 과거 disposition 재감사는 NOT_RUN(이전 리뷰 원문 비열람). 과거 기록의 판정을 새 코드 시험으로 재인증하지 않는다.

실제 corpus 결과:

- 초안 10개는 stdlib/JSON Schema 오류 0. 경로 395 corpus mismatch 0, 공백·제어문자·DEL·절대경로·dot/dotdot·빈 segment를 포함한다. 날짜 9개(윤년·0000/9999·끝 LF·비ASCII), 잘못된 review 날짜, kind list/dict, enforce, 잘못된 repo/app, 미지 key는 기대대로 처리됐다.
- npm workspace 선택은 멤버 Node BELOW_FLOOR와 React FLOATING_REF를 보고한다. 명시 root selector 대조군과 autodiscovery도 유지됐다. 빈 lockfiles ETL은 Python 및 NO_LOCK을 root workflow와 함께 보고한다.
- requirements 11형식 × 명시 lock/빈 lock 앱: root 이탈·외부 symlink·순환·누락·self-symlink는 exit 2, traceback/외부 값/보고서 없음. 정상 root 내부 include는 exit 0 보고서 생성.
- 민감한 workspace를 transitive lock 경로에 합친 경우와 DEL lock path에서 stdout/stderr/JSON/Markdown/step summary의 값 누출 없음.
- direct requirements/npm lock, 동반 package.json/pyproject.toml, 직접 app, workspace, 중간 lock 디렉터리, root/manifest/registry의 checker self-symlink는 양 OS exit 2, traceback/보고서 없음.
- 이번 추가 boundary probe 9형식 × 두 CLI: missing manifest/registry 및 중간 manifest/registry loop는 validator exit 1/checker exit 2, traceback 없음. 외부 app/lock/workspace는 schema validator에서 형식상 exit 0, 파일을 읽는 checker에서는 exit 2다. 정상 내부 alias가 가리키는 실파일은 보고를 유지한다. 내부 alias 아래 missing app/lock은 입력 오류로 닫는다.
- symlink 없는 ordinary missing app는 workflow만 보고할 수 있고, ordinary missing lock은 report 모드 exit 0 + NO_LOCK이다. 이를 설치본 성공으로 세지 않았다.

## A-T011-P2-15 — 누락 registry의 OSError 원문이 비밀형 경로를 출력

- 심각도: **P2**. disposition: **OPEN**, 수정 또는 명시적 범위 처분 필요. 요청의 새 P2 0건 조건에는 부합하지 않는다.
- 위치: `tools/check_versions.py:253`의 Registry.load 파일 읽기와 `tools/check_versions.py:2857-2858`의 registry 예외 출력.
- 최소 재현: 임시 디렉터리 아래 비밀형 경로 component를 문자열 분할로 생성하고 해당 `versions.json`을 만들지 않는다. `check_versions.py --self-check --registry <temp>/<비밀형 component>/versions.json`을 실행한다.
- 후보 직접 재현 파일: `.git/codex-audit/t011-post6-a-disclosure.py`. 위 두 OS 명령에서 harness 경로를 이 파일로 바꾸면 된다. 입력 marker 원문은 출력하지 않고 포함 여부만 출력한다.
- 양 OS 실제 결과:

```text
missing-sensitive-registry exit 2 traceback False private-marker-leak True
```

- 원인: Registry.load의 OSError에 파일 경로가 들어 있고 CLI가 이를 그대로 `{exc}`로 출력한다. symlink resolve 실패의 일반 메시지나 manifest validator의 일반 오류 경로와 달리, 단순 누락 registry 읽기 실패는 비식별화하지 않는다. 정상 경로의 포함 여부만 관찰한 단계에서 멈추지 않고 비밀형 component로 두 OS를 다시 재현했다.
- 영향: 잘못된 로컬/CI registry 인자의 비밀형 경로가 오류 annotation/stdout 로그에 재게시된다. validator의 같은 누락 registry는 일반 오류만 출력해 누출하지 않는다. 입력 거부 숫자 2는 맞으나 출력 비공개 계약은 지키지 못한다.
- **변경 기원 구분**: T-011이 새로 만든 회귀는 아니다. 원 base의 `tools/check_versions.py`를 `git show 3977c00a5b4ffa21a8d29f96dd9531efbe3a0cb5:tools/check_versions.py`로 읽어 임시 파일에 보존한 뒤 동일 반례를 두 OS에서 실행했다. `.git/codex-audit/t011-post6-a-base.py` 결과는 다음과 같아 base부터 존재함을 확인했다.

```text
base-missing-sensitive-registry exit 2 traceback False private-marker-leak True
```

- 권고: registry의 I/O 예외를 원문 없는 일반 오류로 출력하거나, 파일 경로가 포함된 예외 메시지를 비밀형 값 검사 후 비식별화한다. 누락·디렉터리·권한 오류 및 민감한 경로 대조를 양 OS에 추가한다. 원 base부터 있던 문제임을 보존하여 이번 app/validator 수정의 회귀로 집계하지 않는다.

## NOT_RUN과 한계

- 실제 소비자 저장소 build/e2e·npm ci·uv sync·패키지 설치/게시·release는 NOT_RUN(독립 common 읽기/임시 fixture 검토 범위, 소비자 쓰기·게시 금지).
- 원격 CI job 로그의 내부 시험 건수 재집계는 NOT_RUN. exact candidate의 5개 check 최종 성공은 직접 확인했다.
- 이전 raw/report 재열람 및 문서 finding 집계 재판정은 NOT_RUN(비열람 지시). 전체 문서 링크/plan/비밀 gate는 새로 실행했다.
- probe runner exit 0은 각 CLI의 기대 결과를 자동 보증하지 않는다. 개별 코드·traceback·보고서·누출 boolean을 직접 판독했고, 현재 요청에 포함된 누락 registry/redaction의 새 발견 때문에 BLOCK을 남긴다.
