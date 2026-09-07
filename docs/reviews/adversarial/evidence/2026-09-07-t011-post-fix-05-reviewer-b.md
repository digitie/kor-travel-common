# T-011 post-fix-05 독립 적대적 리뷰 B 원본

- 실행 ID: `T011-POST5-B-20260907-205020-KST`
- 최종 판정: **BLOCK**. 새 P2 1건 `B-P2-11`; 새 P0/P1/P3 없음.
- exact candidate: `94c445ec98aff74acbf1389c46a575dcb2bfa102`
- tree: `a72e4b74fcf565019e3d25120252c7043e75ea98`
- 고정 diff base: `3977c00a5b4ffa21a8d29f96dd9531efbe3a0cb5`
- 직접 parent: `22f9333b5f3b7d61cf7af5d454d396c2b15dc540`
- HEAD 최초 조회: `2026-09-07T20:49:57.9772381+09:00`; 격리 시작: `2026-09-07T20:50:20.9090742+09:00`; 종료: `2026-09-07T20:54:15.3875132+09:00`.
- 격리: `F:/dev/kor-travel-common-wt/review-t011-post5-b`를 exact candidate에서 detached 생성. 시작·종료 `git show -s --format='%H%n%T%n%P' HEAD`의 SHA/tree 동일; `git status --porcelain=v1` 모두 빈 출력.
- source `.git/config`의 시작·종료 SHA256: `EDF33489791777FC04CB8F11CB627188653B86378FE26FF3B4A6F81179CB897A` (동일). `core.worktree`나 다른 Git 설정 수정 없음.
- candidate 소스·문서·테스트, 소비자 저장소 변경 없음. commit/push/게시 없음. 자체 반례는 OS 임시 디렉터리에서 실행했고 스크립트·원본은 기본 checkout `.git/codex-audit`에만 저장했다.

## 전달 요청과 독립성

> Post-fix-05 독립 적대 리뷰를 수행해줘. 후보 HEAD는 94c445e0a1d2? 먼저 git rev-parse HEAD로 확인하고, 기준선은 3977c00a5b4ffa21a8d29f96dd9531efbe3a0cb5로 고정해 diff를 검토해. 이번 수정의 핵심은 tools/check_versions.py의 _path_contains_symlink로 manifest/lock/app/workspace 및 중간 디렉터리 self-symlink를 Windows/WSL 모두 입력 오류(exit 2, traceback 없음)로 통일한 것이다. direct lock, direct manifest, companion pyproject/package, empty-lock app, workspace, intermediate directory symlink loop, external symlink, requirements recursive include와 기존 finding corpus를 모두 공격적으로 시험해. Windows와 WSL 테스트/정적 gate/정확한 후보 CI를 확인하되 실행하지 못한 것은 NOT_RUN으로 명시해. 리뷰 결과는 .git/codex-audit/2026-09-07-t011-post-fix-05-reviewer-b.md에 기록하고, source .git/config의 core.worktree를 변경하지 마. 후보 소스/문서/테스트는 수정하지 말고 시작·종료 SHA/tree도 기록해. 이전 리뷰 결과는 보지 말고 독립적으로 판단해.

추가 전달에서 정확한 SHA `94c445ec98aff74acbf1389c46a575dcb2bfa102`를 확정했다. 이번 실행에서는 이전 reviewer 원본·통합 결과를 읽지 않았다. 기존 자체 실행 corpus를 새 후보에 다시 실행했으며 판정은 현재 코드·문서와 실제 결과에 근거한다.

## 검토와 명령

고정 base에서 후보까지 `tools/check_versions.py`, 새 `manifest_schema.py`·`validate_manifest.py`, `tests/test_validate_manifest.py`, JSON schema·example·10개 draft, 관련 standards/templates/tools 문서 diff 및 T-011 task를 확인했다. 직접 parent에서 후보까지의 helper와 추가 회귀 시험도 별도로 대조했다. base 대비 `versions.json`, `.github`, `packages` 변경 목록은 비어 있다.

Windows는 Python 3.14.3 (`py -3.14 -B -X utf8`), WSL Ubuntu-26.04는 Python 3.11.15 (`/home/digitie/.local/share/uv/python/cpython-3.11-linux-x86_64-gnu/bin/python3.11 -B -X utf8`)을 사용했다. WSL unittest는 `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_COMMON_DIR`로 Git fixture를 격리했다. WSL 읽기 전용 validator에는 현재 detached worktree의 Git 경로를 실행 환경으로만 전달했다.

| 명령/검사 | Windows | WSL |
|---|---|---|
| `-m unittest discover -s tests -q` | 201개, 53.464초, OK, skip 0 | 201개 발견, 35.497초, 199개 성공·2개 skip |
| `tools/validate_plan.py` | 상세 task 106, 오류 0 | 동일 |
| `tools/validate_document_links.py` | 문서 344·local target 2287, 오류 0 | 동일 |
| `tools/check_spdx.py` | 32개, 오류 0 | 동일 |
| `tools/scan_secrets.py --all` | 434개, 발견 0·예외 0 | 동일 |
| `tools/check_prod_redaction.py --all` | 434개, 발견 0·예외 0 | 동일 |
| `tools/check_versions.py --self-check` | 자체 검사 통과 | 동일 |
| `git diff --check 3977c00a5b4ffa21a8d29f96dd9531efbe3a0cb5 HEAD` | exit 0, 출력 없음 | exit 0, 출력 없음 |

실제 candidate CI도 직접 조회했다. `gh run list --commit <candidate> --json databaseId,headSha,status,conclusion`와 `gh run view 34118599300 --json headSha,conclusion,jobs`에서 head 일치·run success·5개 job 모두 success: tools Ubuntu/Windows, docs, secret-scan, check-versions. URL: https://github.com/digitie/kor-travel-common/actions/runs/34118599300 . 추가 반례가 CI에 포함됐다는 의미는 아니다.

## 직접 corpus 결과

`.git/codex-audit`의 `review-t011-b-cases.py`, `review-t011-post-b-cases.py`, `review-t011-post2-b-cases.py`, `review-t011-post3-b-cases.py`, `review-t011-post4-b-cases.py`를 양 OS에서 이번 worktree 인자로 재실행했다. 이전 보고서는 읽지 않았다.

- 민감 unknown field·scope·전이 lock path는 stdout/JSON/Markdown/step summary에서 원문 미노출. tab/DEL 및 합성 토큰 반례도 동일. kind 배열·객체는 traceback 없이 validator exit 1, check_versions 입력 오류.
- 날짜·제어문자·경계 공백 경로의 schema/stdlib 반례는 기대대로 거부, 내부 정상 공백 경로 허용. 달력 corpus 5,082개 불일치 0(Windows 실제 Draft202012Validator, WSL 정규식만 실행). 10개 draft CLI 검증은 전체 unittest에서 양 OS 통과했다.
- 선택 workspace member의 Node 18 선언은 root 선언에 가려지지 않고 BELOW_FLOOR. 외부 manifest/lock/companion/workflow symlink와 requirements 직접·재귀 root escape는 exit 2이며 외부 선언 report 없음. 정상 root 내부 include 유지.
- 직접 requirements lock, pyproject companion, empty-lock app, 재귀 include self-symlink는 양 OS exit 2, traceback/합성값 누출/report 없음.
- 기존 중간 lock 경로와 npm workspace self-symlink 반례는 fail/report/warn 3모드 모두 양 OS exit 2. 정상 누락 경로와 정상 root 내부 디렉터리 링크 control은 기존 NO_LOCK 판정을 유지한다. 따라서 기존 B-P2-10의 두 원 반례는 FIXED다.

추가 자체 스크립트 `review-t011-post5-b-cases.py`를 두 OS에서 각각 실행했다. 8개 fixture × 3모드 = OS별 24개 CLI 호출. 직접 manifest·manifest 부모·package.json companion·재귀 include 부모 순환은 모두 exit 2, traceback 없음, JSON/Markdown/step summary 미생성이다. 정상 app 내부 링크는 선언을 읽고 NO_LOCK을 보존했다. 아래 두 app 중간 경로 반례만 입력 오류 처리를 우회했다.

## B-P2-11 — 빈 lock app 경로의 early return이 중간 symlink 순환/이탈 검사를 우회

- 심각도: **P2**. disposition 권고: **수정 필요**.
- 위치: `tools/check_versions.py:1839` (`_manifest_declaration_scopes`), 관련 검사 `:1841`~`:1845`.
- 최소 입력: `templates/manifests/pinvi.apps-etl.lock.json`과 같은 정상 strict manifest(`app="apps/etl"`, `lockfiles=[]`)를 임시 root의 `manifest.json`에 저장한다. `root/apps`를 자기 자신으로 향하는 디렉터리 symlink로 만든다. root workflow에는 정상 SHA 형태로 고정한 checkout 참조 하나를 둔다.
- 보조 반례: `root/apps`가 root 외부 디렉터리를 향하고, 외부에 `etl`이 없게 한다. 최종 경로 containment 확인 전 같은 분기를 탄다. 외부 파일 읽기는 관찰되지 않았다.
- 원인: `not candidate.exists() and not candidate.is_symlink()`에서 마지막 `apps/etl`은 직접 symlink가 아니며 exists도 false여서 `return []`한다. 새 `_path_contains_symlink(candidate)`와 resolve/containment 검사에 도달하지 않는다.
- 영향: 구조적으로 해석 불가능한 app 입력을 일반 누락으로 취급하고 앱 범위 없이 workflow만 보고한다. 정상 root workflow가 있으면 fail 모드에서도 exit 0·OK만 반환해 해당 경로 입력 검사가 끝난 것처럼 보인다. 현재 경로 오류 exit 2 계약 및 이번 통일 목적을 충족하지 못한다.

| 반례 | Windows 3.14.3 | WSL 3.11.15 |
|---|---|---|
| app 중간 self-symlink, fail/report/warn | 모두 exit 0, OK github-action만, 세 report 채널 생성 | 동일 |
| app 중간 외부 symlink + 없는 마지막 경로, fail/report/warn | 모두 exit 0, OK github-action만, 세 report 채널 생성 | 동일 |
| traceback | 없음 | 없음 |

재현 명령:

```text
py -3.14 -B -X utf8 F:/dev/kor-travel-common/.git/codex-audit/review-t011-post5-b-cases.py F:/dev/kor-travel-common-wt/review-t011-post5-b
wsl.exe -d Ubuntu-26.04 /home/digitie/.local/share/uv/python/cpython-3.11-linux-x86_64-gnu/bin/python3.11 -B -X utf8 /mnt/f/dev/kor-travel-common/.git/codex-audit/review-t011-post5-b-cases.py /mnt/f/dev/kor-travel-common-wt/review-t011-post5-b
```

해당 fixture 출력: `case=app_parent_loop` 및 `case=app_parent_external_missing`, 각 mode별 `exit=0`, `traceback=false`, `channels_exist=[true,true,true]`, `verdicts=[OK]`, `ecosystems=[github-action]`.

최소 수정 권고: 일반 app 누락을 반환하기 전에 중간 구성 요소의 symlink와 resolve/containment를 확인한다. 실제 내부 누락·정상 내부 symlink control은 보존한다. 두 반례에 정상 root workflow를 동반해 검증 오류가 단순 `no scopes` 오류에 가려지지 않도록 양 OS·3모드 회귀로 고정한다.

## 미검증과 최종 판정

- NOT_RUN: WSL 외부 jsonschema 엔진 2개 시험(모듈 미설치). 2 skip을 성공 건수로 계산하지 않았다. Windows 실제 schema 검사 및 WSL 직접 정규식 corpus는 각각 실행했다.
- NOT_RUN: 이전 리뷰 원본·통합 결과의 집계/서술 재검사(요청대로 미열람). 기존 코드 반례는 재실행했으나 과거 기록의 disposition을 이번에 재승인하지 않는다.
- NOT_RUN: 소비자 실제 채택·빌드/e2e·패키지 배포·npm/PyPI 게시(범위 밖). source/소비자 쓰기 없음.
- 새 P0/P1/P3 없음. 직접 경로와 기존 중간 lock/workspace 수정은 유효하지만 B-P2-11이 양 OS에서 재현되어 **BLOCK**으로 확정한다.
