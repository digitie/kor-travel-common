# T-011 post-fix 독립 리뷰 B 원본

최종 verdict: **BLOCK**. 기존 B-P2-04의 경로 parity 문제가 남고, 재귀 requirements의 root 경계 누락 B-P1-06과 통합 보고서 건수 오기 B-P3-07을 확인했다. 기존 직접 반례 수정과 새 반례를 구분한다.

## 기준선·독립성

- 실행 ID: `T011-POST-B-20260907-195609-KST`.
- candidate: `c781117190b98fbba0036509806a39d50d64e4a3`.
- parent/base: `7f715b0efb7c422f0b6212eea612f0c95dcf6fff`.
- tree: `d9d777cfc93db2ef4e02c4f84b45793aba741462`.
- detached worktree: `F:/dev/kor-travel-common-wt/review-t011-post-b`.
- 시작: `2026-09-07T19:56:09.9924775+09:00`.
- 종료: `2026-09-07T20:00:30.7470705+09:00`.
- 시작·종료 SHA/tree 일치, `git status --porcelain=v1` 출력 없음. 후보 파일을 수정하지 않았다.
- 주 checkout `.git/config`의 시작·종료 SHA256은 모두 `EDF33489791777FC04CB8F11CB627188653B86378FE26FF3B4A6F81179CB897A`다. config를 수정하지 않았다.
- 이전 B 원본과 요청된 pre-fix 통합 보고서만 참고했다. 상대 reviewer의 개별 원본·이번 결과는 읽거나 요청하지 않았다. 변경 코드·schema·tests·규범 문서를 직접 읽었으며 archive의 상대 원본 본문은 제외했다.
- 소비자 저장소 쓰기·commit·push·게시 없음. 합성 입력과 출력은 자동 정리되는 임시 디렉터리에 만들었고, 자체 재현 스크립트와 이 원본만 주 checkout `.git/codex-audit/`에 보존했다.

## 전달 요청 원문

> T-011 post-fix 독립 리뷰를 시작해 주세요. 새 immutable candidate는 c781117 (full c781117c? 먼저 git rev-parse로 확인), parent/base는 7f715b0efb7c422f0b6212eea612f0c95dcf6fff입니다. 이전 B finding B-P1-01~03, P2-04~05와 pre-fix 통합 report의 모든 finding이 닫혔는지 Windows/WSL 반례로 재현하고, 새 P0-P3 finding도 공격해 주세요. 상대 reviewer 결과는 보지 마세요. 시작/종료 SHA/tree/clean·검증 명령·NOT_RUN을 원문 evidence로 남기고 PASS/BLOCK을 확정해 주세요. source checkout의 .git/config나 파일은 수정하지 말고 detached/object-only 읽기 전용 방식으로 진행하세요.

후속 전달된 full SHA는 위 candidate와 일치한다. pre-fix manifest의 SHA를 이번 후보로 재해석하지 않고 이 요청으로 새 기준선을 고정했다.

## 실행 검증

| 검증 | Windows Python 3.14.3 | WSL Python 3.11.15 |
|---|---|---|
| 전체 unittest | 195 tests, 53.647초, OK, skip 0 | 195 tests, 32.420초, OK, skip 0 |
| plan | task 106, 오류 0 | 동일 |
| 문서 링크 | 문서 332·target 2,279, 오류 0 | 동일 |
| SPDX | 32파일, 오류 0 | 동일 |
| secret / production redaction | 각각 422파일, 발견 0·예외 0 | 동일 |
| registry self-check | exit 0 | exit 0 |
| 기존 직접 반례 corpus | 수정 결과 재현 | 동일 |
| 새 직접 반례 corpus | 아래 결과 재현 | CLI 결과 동일, schema는 아래 한계 참고 |

실행 명령은 Windows의 `py -3.14 -B -X utf8`, WSL의 `/home/digitie/.local/share/uv/python/cpython-3.11-linux-x86_64-gnu/bin/python3.11 -B -X utf8` 뒤에 다음을 전달했다.

- `-m unittest discover -s tests -q`.
- `tools/validate_plan.py`, `tools/validate_document_links.py`, `tools/check_spdx.py`, `tools/scan_secrets.py --all`, `tools/check_prod_redaction.py --all`, `tools/check_versions.py --self-check`.
- `.git/codex-audit/review-t011-b-cases.py <이번 candidate worktree>`: 기존 원본의 반례 스크립트를 그대로 이번 후보에 실행.
- `.git/codex-audit/review-t011-post-b-cases.py <이번 candidate worktree>`: schema 제어 문자·선언 전용 앱·Python symlink·민감한 requirements 파일명·재귀 include 반례.

WSL 전체 시험은 `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_COMMON_DIR`로 실행해 임시 Git 저장소에 source Git 환경을 전파하지 않았다. Git 읽기가 필요한 validator subprocess에만 detached worktree의 Linux Git 경로를 전달했다.

- `git diff --check HEAD^ HEAD`: exit 0.
- Windows jsonschema 4.26.0의 `Draft202012Validator`로 실제 schema를 대조했고 초기 10개 초안은 모두 통과했다.
- `gh run view 34113919728 --json headSha,conclusion,jobs`: exact candidate, 5개 job success. [CI 실행](https://github.com/digitie/kor-travel-common/actions/runs/34113919728).
- 정상 시험·CI 성공은 다음 실패 재현을 해결했다는 증거로 세지 않는다.

## 기존 finding disposition

| 원 ID | 원 심각도 | 판정·재현 |
|---|---:|---|
| B-P1-01 | P1 | FIXED. 미지 field의 합성 비밀 이름은 두 CLI 출력에서 사라졌다. 민감한 scope는 stdout·JSON·Markdown·step summary 전부 원문 미포함. 민감한 requirements 파일명을 추가한 새 선언 전용 경로도 네 채널에서 미포함 |
| B-P1-02 | P1 | FIXED(원 반례). root 밖 package.json symlink는 exit 2·보고서 없음. 선언 전용 Python 앱의 root 밖 pyproject.toml symlink도 exit 2. manifest/lock/workflow의 외부 경로 음성 대조도 exit 2. 재귀 requirements는 아래 새 B-P1-06 |
| B-P1-03 | P1 | FIXED. 선택한 apps/web package.json을 읽고 멤버 Node >=18.0.0을 BELOW_FLOOR, fail exit 1로 보고한다. map·pinvi web 초안 scope도 실제 workspace 경로로 수정됨 |
| B-P2-04 | P2 | **OPEN(일부 수정)**. review 비날짜·불가능한 날짜, 기존 Windows 절대 경로·중복 구분자·끝 slash 반례는 수정됐다. 새 제어 문자 경로 corpus에서 schema/stdlib parity가 여전히 깨진다 |
| B-P2-05 | P2 | FIXED. kind 배열/객체는 오류 목록과 CLI exit 1을 내며 traceback 없음. 추가 타입 회귀도 전체 시험에서 통과 |

pre-fix 통합 ID로는 R01/R02/R03/R04/R06이 수정됐고 R05가 남았다. R07도 직접 확인했다. 빈 lockfiles의 apps/etl에 pyproject.toml 선언만 있으면 Python OK와 **NO_LOCK** 2행, fail exit 1을 낸다. 선언 없이 workflow만 검사한 성공으로 세지 않는다.

## B-P2-04 — 남은 schema/stdlib 경로 parity

- 심각도: 기존 P2 유지. disposition: OPEN, 수정 필요.
- 위치: `templates/kor-travel-common.lock.schema.json:11`, `:16`; `tools/manifest_schema.py:65`, `:72`.
- 최소 재현: 정상 pinvi ETL manifest의 `app`을 `'apps/' + chr(9) + '/etl'`, `chr(10)`, `chr(127)`을 넣은 경로로 바꾼다. Windows Draft202012Validator는 세 경우 모두 **통과**, stdlib validator는 모두 **거절**한다. WSL에서는 같은 schema pattern을 직접 실행해 통과를, stdlib에서 거절을 확인했다.
- 추가 경계: `' /etc/fixture'`도 schema 통과/stdlib 거절이다. `'apps/etl' + chr(10)`은 양쪽이 통과한다. stdlib은 `strip()` 후 검사해 원문 끝 제어 문자를 제거하고, schema는 전체 문자열 끝까지 제한하지 않는다.
- 영향: T-011 수용 기준의 같은 경로 음성 corpus 계약을 충족하지 못하며, Windows에서 파일 경로로 사용할 수 없는 제어 문자를 schema가 승인한다. 끝 제어 문자는 strict validator도 승인한다.
- 권고: raw 문자열의 제어 문자·경계 공백 정책을 먼저 고정하고 동일하게 검사한다. JSON Schema의 pattern을 전체 문자열에 적용하고 금지 제어 문자 범위를 맞춘다. 기존 `test_schema_path_edge_cases_are_rejected`는 이름과 달리 stdlib만 실행하므로 schema parity 증거로 쓰지 않는다.

## B-P1-06 — 재귀 requirements가 소비자 root 밖 입력을 계속 읽음

- 심각도: P1. disposition: OPEN, 수정 필요.
- 위치: `tools/check_versions.py:1812`, `:2513`, `:668`–`:706`.
- 최소 재현 구조: 임시 디렉터리 아래 `repo/apps/etl/requirements.txt`에 `-r ../../../outside-requirements.txt`를 쓰고, `repo` 밖의 해당 파일에는 `fastapi==0.1.0`을 둔다. 소비자 root는 `repo`, app은 `apps/etl`, lockfiles는 빈 배열이다.
- `check_versions.py <repo> --manifest <repo>/apps/etl/manifest.json --mode fail --json <out>` 실행 결과는 Windows/WSL 모두 **exit 1**, 외부 fastapi 설치 후보 0.1.0의 BELOW_FLOOR·NO_ENGINES·NO_LOCK 3행이다. 외부 파일을 실제로 읽었음을 보고서에서 확인했다. 기대되는 root 경계 입력 오류 **exit 2가 아니다**.
- 빈 목록 대신 `lockfiles=[{kind: requirements, path: apps/etl/requirements.txt, scope: apps/etl}]`로 명시해도 같은 결과다. root 내부 shared requirements로 include를 바꾼 대조군은 정상적인 NO_LOCK 판정을 냈다.
- 원인: 첫 requirements 파일은 `_safe_declared_file` 또는 scope 생성에서 root 경계를 확인하지만 `read_requirements()`는 재귀 include마다 resolve만 하고 소비자 root를 전달받지 않는다. 예전 recursive parser에서 있던 경계 누락이 이번 strict root 계약과 새 선언 탐색 경로에도 남았다.
- 영향: 명시한 소비자 저장소 밖 파일로 판정·보고서가 구성된다. 이는 이번 `versions.md`의 resolved root 밖 입력은 exit 2라는 계약과 충돌한다. 이 반례는 실제 설치나 코드 실행을 주장하지 않는다.
- 권고: 검사 root를 Scope/Checker에서 requirements 재귀 호출까지 전달하고 모든 include의 resolved 경로에 동일한 containment 검사를 적용한다. 앱 밖이어도 소비자 root 안인 공유 requirements는 허용하고 root 밖·밖을 가리키는 symlink는 읽기 전에 exit 2로 닫는다.

## B-P3-07 — 통합 finding 건수와 표의 합계가 다름

- 심각도: P3. disposition: OPEN, 문서 정정 필요.
- 위치: `docs/reviews/adversarial/2026-09-07-t011.md:11`.
- 근거: 본문은 중복을 합친 결과가 P1 3건·P2 5건이라고 기록하지만 R01–R07 표는 P1 3행·P2 4행, 총 7건이다.
- 영향: 종료 evidence에서 전체 finding 수와 disposition 합계가 맞지 않는다.
- 권고: 실제 통합 ID 표와 같은 P1 3건·P2 4건으로 고치거나 빠진 ID가 있다면 근거와 함께 표에 복원한다. 상대 원본은 읽지 않았으므로 존재하지 않는 여덟 번째 finding을 추정하지 않았다.

## NOT_RUN과 범위

- NOT_RUN: WSL 외부 jsonschema 엔진(설치되어 있지 않음). WSL pattern/stdlib 대조와 Windows 전체 schema 엔진 대조를 구분했다.
- NOT_RUN: 소비자 저장소 build/e2e/설치, 공용 패키지 build/install, 릴리스 tag/asset, npm/PyPI 게시. 요청 범위 밖이며 소비자 저장소를 수정하지 않았다.
- 기존 duplicate JSON key/lock scope 허용은 변하지 않았다. 최초 원본과 같이 명시적인 중복 금지 계약이 없어 추가 finding으로 집계하지 않았다.
- 후보의 규범·코드와 직접 반례가 기준이며 다른 reviewer 결과나 작성자의 성공 설명을 판정 근거로 대체하지 않았다.

위 잔여 P2와 새 P1을 수정한 immutable 후보의 post-fix 재검토가 필요하다. 이 후보는 BLOCK이다.
