# T-011 post-fix-06 독립 적대적 리뷰 B 원본

- 실행 ID: `T011-POST6-B-20260907-210128-KST`
- 판정: **BLOCK**. B-P2-11은 FIXED. 새로 확인한 P1 `B-P1-12` 1건이며, 이는 이번 commit의 신규 회귀가 아니라 이번 요청의 registry/redaction 경계에서 재현한 기존 결함이다.
- candidate SHA: `56d6ae11d5917eb2b2e69f8f26f90b903bacceb6`
- tree: `845442686054c6707bfd1d76bab330e79749b3c1`
- immutable diff base: `3977c00a5b4ffa21a8d29f96dd9531efbe3a0cb5`
- 실제 parent: `5774c28368adac8457e3bbfe9cb4658cd824d46d`
- 최초 조회: `2026-09-07T21:01:24.6386675+09:00`; detached 검증 시작: `2026-09-07T21:01:28.7391213+09:00`; 종료: `2026-09-07T21:05:04.8937749+09:00`.
- 격리: `F:/dev/kor-travel-common-wt/review-t011-post6-b`. 시작·종료 SHA/tree 동일, `git status --porcelain=v1` 모두 빈 출력.
- source `.git/config` 시작·종료 SHA256 동일: `EDF33489791777FC04CB8F11CB627188653B86378FE26FF3B4A6F81179CB897A`. `core.worktree` 등 설정을 변경하지 않았다.
- candidate 소스·문서·시험, 소비자 저장소 쓰기 없음. commit/push/게시 없음. 자체 fixture는 OS 임시 디렉터리에서 실행하고 자체 스크립트·이 원본만 source `.git/codex-audit`에 기록했다.

## 요청과 독립성

> Post-fix-06 독립 적대 리뷰를 시작해줘. 새 후보 SHA는 56d6ae11d5917eb2b2e69f8f26f90b903bacceb6, immutable base는 3977c00a5b4ffa21a8d29f96dd9531efbe3a0cb5. 직전 B finding B-P2-11(빈 lockfiles app 중간 symlink 조기 반환)이 수정됐는지 양 OS에서 직접 재현하고, direct/중간/외부/self symlink, 누락 app/lock/manifest/registry, workspace, requirements recursion, redaction, schema parity 및 기존 corpus를 다시 공격해. 이전 리뷰 원문/상대 결과는 읽지 말고 독립 판단해. Windows/WSL tests와 gates/exact candidate CI를 확인하되 미실행은 NOT_RUN. source .git/config core.worktree를 절대 변경하지 말고 후보 소스/문서/시험은 수정하지 마. 원본은 .git/codex-audit/2026-09-07-t011-post-fix-06-reviewer-b.md에 쓰고 시작/종료 SHA/tree/clean/hash/verdict를 기록해. PASS 조건은 P0/P1/P2 신규 0, 기존 finding 모두 FIXED야.

이전 reviewer 원문·통합 결과·상대 결과는 읽지 않았다. 앞서 직접 확인한 불변 기준선 코드와 새 delta, 현재 파일 및 자체 실행 corpus로 판정했다. 94c445e 이후의 app 존재성 검사 순서·validator registry 경로 변경과 추가 시험·task 문구를 직접 읽었다. immutable base 대비 versions.json/CI/packages 변경 목록은 비어 있다.

## 실행 명령과 결과

Windows Python 3.14.3은 `py -3.14 -B -X utf8`, WSL Ubuntu-26.04 Python 3.11.15는 `/home/digitie/.local/share/uv/python/cpython-3.11-linux-x86_64-gnu/bin/python3.11 -B -X utf8`을 사용했다. WSL 전체 unittest는 `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_COMMON_DIR`로 실행했다. 읽기 전용 WSL validator에만 현재 detached worktree의 Git 경로를 process 환경으로 제공했다. source 설정 파일 수정은 없다.

| 명령 | Windows | WSL |
|---|---|---|
| `-m unittest discover -s tests -q` | 202개, 67.336초, OK, skip 0 | 202개 발견, 41.587초, 200개 성공·2개 skip |
| `tools/validate_plan.py` | task 106, 오류 0 | 동일 |
| `tools/validate_document_links.py` | 문서 344, target 2287, 오류 0 | 동일 |
| `tools/check_spdx.py` | 32개, 오류 0 | 동일 |
| `tools/scan_secrets.py --all` | 434개, 발견 0·예외 0 | 동일 |
| `tools/check_prod_redaction.py --all` | 434개, 발견 0·예외 0 | 동일 |
| `tools/check_versions.py --self-check` | 자체 검사 통과 | 동일 |
| `git diff --check 3977c00a5b4ffa21a8d29f96dd9531efbe3a0cb5 HEAD` | exit 0, 출력 없음 | exit 0, 출력 없음 |

`gh run list --commit <candidate>`와 `gh run view 34119572392 --json headSha,conclusion,jobs`를 직접 조회했다. exact SHA 일치, run success, Windows/Ubuntu tools·docs·secret-scan·check-versions 5개 job success. URL: https://github.com/digitie/kor-travel-common/actions/runs/34119572392 . 실제 CI 관찰이며 추가 반례를 CI가 실행했다는 뜻은 아니다.

## 기존 반례 재실행

`.git/codex-audit/review-t011-post6-b-corpus.py <candidate-worktree>`로 기존 자체 스크립트 5개(`review-t011-b-cases.py`, `review-t011-post-b-cases.py`, `review-t011-post2-b-cases.py`, `review-t011-post3-b-cases.py`, `review-t011-post4-b-cases.py`)를 두 OS에서 다시 실행했다. 마지막 스크립트는 fail/report/warn 모두 실행했다. 각 실행 반환은 0이며 내부 CLI의 의도한 exit 1/2와 구분했다.

- B-P1-01/02/03, B-P2-04/05, B-P1-06, B-P2-08, B-P1-09, B-P2-10의 코드 반례는 모두 FIXED 확인: 민감 unknown field·scope·전이 lock 경로 비공개, 외부 companion/manifest/lock/workflow 차단, 실제 workspace member 선택, strict kind/date/path, 재귀 requirements containment, 직접·중간 self-symlink 입력 오류.
- 달력 corpus 5,082개 불일치 0. Windows는 실제 Draft202012Validator, WSL은 정규식 직접 대조만 실행했다. 10개 초안 validator CLI는 전체 unittest에서 양 OS 통과했다.
- tab/DEL 및 합성 토큰이 stdout·JSON(디코딩 값 포함)·Markdown·step summary에 나타나지 않았다. 정상 root 내부 requirements include·디렉터리 symlink와 일반 누락 lock의 NO_LOCK 처리는 유지됐다.
- `review-t011-post5-b-cases.py <candidate-worktree>`를 두 OS에서 재실행했다(8 fixture × 3모드). **B-P2-11의 app 중간 self-symlink와 외부 symlink 아래 없는 app은 모두 exit 2**, traceback 없음, JSON/Markdown/step summary 미생성. 정상 root workflow가 함께 있어도 우회하지 않는다.
- 직접 manifest·manifest 중간 디렉터리·package companion·재귀 include 부모 순환도 3모드 exit 2. 정상 내부 app 링크는 선언을 읽고 NO_LOCK을 보존했다. 일반 누락 app은 workflow가 있으면 workflow만 보고하고, workflow도 없으면 no-scope exit 2로 종료한다(이번 수정은 정상 누락의 정책을 변경하지 않음).

추가 `review-t011-post6-b-cases.py <candidate-worktree>`는 8 fixture × 2 CLI = OS별 16개 호출이다. missing/self manifest는 check_versions exit 2, standalone validator exit 1, traceback/원문 없음. missing lock은 check_versions NO_LOCK/exit 1, standalone validator exit 0(형식 검사). standalone validator는 missing/self/intermediate registry와 잘못된 registry schema를 모두 원문 없는 exit 1로 처리한다. check_versions registry 경로의 잔여 노출은 아래와 같다.

## B-P1-12 — check_versions registry 오류가 민감한 경로·값 원문을 annotation에 출력

- 심각도: **P1**, disposition: **수정 필요**. 이번에 새로 발견한 기존 결함으로, 신규 코드 회귀와 구분한다.
- 위치: `tools/check_versions.py:2858`의 registry 오류 `{exc}` 출력. `Registry.load` (`:252` 이후)는 여러 오류에 raw path/값을 포함하고, missing 파일의 OSError도 원문 경로를 포함한다.
- 최소 반례 A: 정상 manifest와 consumer root를 지정하고, 존재하지 않는 `--registry` 파일명의 일부에 합성 민감 토큰 문자열을 넣는다. 토큰은 스크립트에서 조각을 결합해 생성하며 이 보고서에는 평문을 기록하지 않는다.
- 최소 반례 B: 일반 이름의 registry JSON에 `schema` 값으로 같은 합성 민감 문자열을 넣는다. `axes`는 빈 객체다. Registry.load의 schema 오류가 그 값을 그대로 반환한다.
- 추가 반례 C/D: registry 자체 또는 registry 중간 디렉터리가 self-symlink인 경우 Windows의 느슨한 resolve 후 파일 I/O 오류가 원문 경로를 포함한다. WSL은 앞선 resolve에서 일반 오류로 전환한다.

| check_versions 반례 | Windows 3.14.3 | WSL 3.11.15 |
|---|---|---|
| missing registry | exit 2, stdout 원문 포함 | exit 2, stdout 원문 포함 |
| 잘못된 registry schema 값 | exit 2, stdout 원문 포함 | exit 2, stdout 원문 포함 |
| registry self-symlink | exit 2, stdout 원문 포함 | exit 2, 원문 없음 |
| registry 부모 self-symlink | exit 2, stdout 원문 포함 | exit 2, 원문 없음 |
| traceback / JSON·Markdown·summary 파일 | 모두 없음 | 모두 없음 |

영향: 파일 읽기/형식 실패에서 검사 모드와 상관없이 stdout의 GitHub error annotation에 입력 경로 또는 값이 재노출된다. report 파일이 생성되지 않고 exit 2여도 CI 로그와 annotation의 비공개 계약은 보장되지 않는다. standalone validator의 동일 입력은 원문을 출력하지 않아 두 CLI의 오류 경계가 다르다.

재현 명령:

```text
py -3.14 -B -X utf8 F:/dev/kor-travel-common/.git/codex-audit/review-t011-post6-b-cases.py F:/dev/kor-travel-common-wt/review-t011-post6-b
wsl.exe -d Ubuntu-26.04 /home/digitie/.local/share/uv/python/cpython-3.11-linux-x86_64-gnu/bin/python3.11 -B -X utf8 /mnt/f/dev/kor-travel-common/.git/codex-audit/review-t011-post6-b-cases.py /mnt/f/dev/kor-travel-common-wt/review-t011-post6-b
```

출력은 `stdout_marker=true/false`, `stderr_marker`, `traceback`, exit와 생성 파일 여부만 기록하여 재현 자체에서도 민감 문자열 원문을 노출하지 않았다.

기준선 대조: `git show 3977c00a5b4ffa21a8d29f96dd9531efbe3a0cb5:tools/check_versions.py`를 임시 디렉터리 파일로 추출해 Windows에서 `--registry <fixture> --self-check`로 실행했다. A/B 모두 baseline에서도 exit 2·stdout_marker=true·traceback=false였다. 따라서 이 결함이 post-fix-06에서 유입됐다고 주장하지 않는다. 다만 이번 요청이 missing registry와 redaction을 직접 검토 범위로 지정했고 P1 미해결 상태이므로 PASS로 표시하지 않는다.

최소 수정 권고: registry 로딩/검증 실패를 원문 없는 고정 오류로 변환하거나 중앙 출력 단계에서 경로·값을 완전히 비공개 처리한다. missing/self/중간 registry 및 malformed schema/미지 필드를 두 CLI·양 OS에서 함께 회귀로 고정한다. exit 2와 유효 registry의 자체 검사 성공은 유지한다.

## NOT_RUN과 최종 판정

- NOT_RUN: WSL 외부 jsonschema 엔진 2개 시험(모듈 미설치); skip을 pass로 집계하지 않았다. Windows의 실제 엔진 검사와 WSL 정규식 corpus는 각각 실행했다.
- NOT_RUN: 이전 리뷰 원본·통합 결과의 집계(B-P3-07 등) 재검사(요청에 따라 미열람). 과거 기록을 재승인하지 않으며 코드 반례 결과와 구분했다.
- NOT_RUN: 소비자 실제 채택·빌드/e2e·package/registry 게시(범위 밖). 소비자 저장소 쓰기 없음.
- 코드 반례 B-P2-11 및 이전 경로/manifest corpus는 수정 확인. 신규 회귀는 발견하지 않았지만 명시된 registry/redaction 경계의 기존 P1 B-P1-12가 남아 **BLOCK**으로 확정한다.
