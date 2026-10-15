# Common Geo 이전 가이드 독립 FULL 리뷰 A

- reviewer execution ID: `review_finish_a-common-geo-cutover-guide-3d3ca85-20261015-r1`
- reviewer: `/root/review_finish_a` — Dagster 실제 동작·복구 순서·실패 누락/재생·보장 범위
- 시작: `2026-10-15T02:56:10Z` (immutable hash 확인 시각; 그 전 준비 읽기의 시작 시각은 별도 기록하지 않음)
- 종료: `2026-10-15T02:57:15Z` (고정 대상·근거 검토 종료; 원문 저장은 이후)
- 종류: **FULL**, 문서 전용 commit object-only
- 최종 merge verdict: **CONDITIONAL** — 아래 P2/P3가 현재 commit에서는 OPEN이다. root의 수정 수용은 확인했으나 post-fix commit은 아직 이 실행의 검토 대상이 아니다.

## 요청·기준선·범위

요청은 Common PR #30의 가이드 §12와 journal 두 파일 전체 변경을 독립 적대 검토하고 실제 SDK 동작·복구 순서·missed/replayed failures·잘못된 보장을 확인하는 것이다. 운영·소스 수정·다른 리뷰어 원문 접근은 금지하며 기존 운영 단계 리뷰를 이 문서 리뷰 결과로 재집계하지 않는다.

- repository: `kor-travel-common-codex-cutover`의 로컬 Git object database
- manifest: `common-geo-cutover-guide-20261015.manifest.json`
- manifest SHA-256: `061181adafd87cf4a60ac8039d5a8aec78626023b5a4c0d17daf75417e490210`
- actual commit: `3d3ca855f21180e46b5260a2c23b40bd74bd4624`
- base: `efcd671207d7f9e2fb01251bab6854a8d543279a`

| 검토 파일 | commit blob SHA-256 |
| --- | --- |
| docs/runbooks/dagster-adoption.md | e8308f849808d0098e1bb44fb0c003a48ac6dfb7c8a933b71af63dac07c722dc |
| docs/journal.md | 4ba3ce184ff18fc2019fd0a55646d6ea953525c14f6bc00fc944374542df9b7e |

`git rev-parse <commit>^{commit}`로 기준선을 확인하고 `git show <commit>:<path>`와 `git diff <base> <commit>`로 두 파일의 모든 변경74줄 및 가이드 기존 관련 문맥을 읽었다. 이동 branch/worktree 파일을 기준선으로 사용하지 않았다. 별도 detached checkout을 만들지 않았으므로 checkout clean 상태는 N/A이며 source 변경0이다. Common AGENTS·docs/README·resume·agent-workflow 및 review archive 규칙을 commit object에서 확인했다. 다른 리뷰어의 report/finding 원문은 읽지 않았다.

## Finding

### A-P2-01 — None cursor의 첫 tick 초기화 공백을 복원 절차에 명시해야 함

- 위치: `docs/runbooks/dagster-adoption.md:404`~411
- disposition: **OPEN** — root는 수용했고 post-fix 문서에 반영할 예정이라고 알림. 실제 수정 commit 재검토 전에는 FIXED가 아니다.
- 근거: 문서는 target high-water 기준 복원과 활성화 직전 재상향 금지를 설명하지만, STOPPED 상태에서 유효한 cursor를 저장·readback한 뒤 public start해야 함을 명시하지 않는다. `start_sensor`의 fresh start timestamp 확인만으로 이 공백을 막을 수 없다.
- 실패 시나리오: 새 target의 preseed state가 STOPPED/cursorNone이다. public start_sensor를 호출하고 첫 tick 전에 새 실패가 생긴다. Dagster1.13.24 `run_status_sensor_definition.py:703`~723은 cursorNone/invalid에서 **그 첫 tick 시점**의 최신 해당 run-status event 한 건을 조회해 cursor로 삼고 SkipReason을 반환한다. 그 실패의 callback은 처리하지 않는다. 첫 tick이 오류 없이 끝났다는 검사만으로도 놓친 실패를 정상처럼 볼 수 있다.
- SDK 교차 확인: `scheduling_methods.py`의 public start_sensor는 새 cursor를 prime하지 않으며, 기존 sensor state에서는 기존 data를 기반으로 RUNNING/start 시각을 갱신한다. start timestamp와 cursor는 별도 경계다.
- 영향: 소비자가 이 절의 단계만 구현하면서 초기 cursor를 None으로 남기면 전환/활성화부터 첫 tick 사이의 실패를 놓칠 수 있다. 같은 instance cursor 보존 및 다른 instance cursor 복사 금지 설명은 적절하지만 이 초기화 공백을 해결하지 않는다.
- 권고: 최초 high-water 기준을 미리 고정하고 STOPPED 상태의 유효 RunStatusSensorCursor에 저장·readback한 뒤 public start_sensor를 수행한다고 명시한다. None/invalid 첫 tick의 skip 동작과 직전 기준 재상향 금지를 함께 적고, 같은 storage에서는 기존 cursor/미처리 실패를 보존한다. 정상 첫 tick과 실제 실패 처리 증거를 구분한다.

### A-P3-01 — workspace reload와 DB/전체 stack 재시작 표현을 분리

- 위치: `docs/runbooks/dagster-adoption.md:386`~387
- disposition: **OPEN** — root 수정 수용, post-fix 미검토.
- 근거: “다른 location·DB·실행 worker를 함께 재시작하는 전체 workspace reload”라는 문장은 GraphQL/workspace reload 자체가 DB를 재시작하는 것으로 읽힐 수 있다. 실제 SDK `WorkspaceProcessContext.reload_workspace`는 `_origins`의 각 location을 reload=True로 로드하고, 외부 gRPC origin은 `reload_code`를 호출한다. DB 컨테이너 재시작과는 다른 경로다.
- 영향: 적용자가 실제 영향 범위와 회피해야 할 동작을 잘못 이해할 수 있다. 현재 문구의 보수적인 회피 방향 자체는 유익하며 즉각적인 안전 경계 파괴로 보지는 않는다.
- 권고: 불필요한 전체 stack/DB 재시작을 피한다는 규칙과, 다른 location의 code reload를 유발할 수 있는 workspace reload를 피한다는 설명을 분리한다.

## 공격 관점과 나머지 검토

- proxy GetCurrentRuns UNIMPLEMENTED를 idle로 인정하지 않는 설명, 실제 child/metadata/tick·child 교체/오류 차단 및 기존 load health 유지가 설치1.13.24 동작과 맞는다.
- STOPPED schedule checkpoint가 최초/interval 이후 갱신될 수 있다는 설명은 실제 scheduler 경로와 맞다. 상태·cron/start를 유지하며 한 필드만 finite/비역행/관측창으로 구분하고 DB를 되돌리지 않도록 한다.
- 실제 file bind inode와 host 파일 구분, 대상 예약 중지 준비→원본 예약 중지·drain·정상 종료→새 workspace 등록→native loading→큐 실제 실행→instigation 복원 순서는 동시 자동 실행과 등록만으로 daemon 성공을 주장하는 위험을 줄인다. partial write 관측·scope·기존 host 정본 재기동 방지도 포함한다.
- retry sensor가 fresh cursor로도 과거 실패를 검색할 수 있음을 기존 §8 이력 설명과 교차 확인했다. Noop 후보는 실제 설정·출력·DB/artifact 무변경을 요구하고 운영 설정을 임의 변경하지 않는다. HTTP200/등록 상태/다음 cron 계산을 실제 실행 증거로 과장하지 않는다.
- backup catalog와 실제 파일·expires_at/최소 보존/allowroot/UID 분리, 작은 고정 chunk checksum과 no-clobber 공개·private hardlink 공간 회수 추적은 적절하다.
- journal은 가이드 추가 사실만 기록하고 새 Python API·앱 tuning·모든 소비자 채택 완료를 주장하지 않는다. 범위 밖 배포 결과와 최초 cron/전체 batch는 소비자 검증으로 남긴다. 공개 변경에 운영 주소·DSN·cookie·credential 값은 없다.

## 실행·미실행과 한계

- 실행: 두 Git blob/manifest SHA·commit/base 확인, 전체 두 파일 diff와 관련 문맥 정적 검토, `git diff --check <base> <head>` EXIT0, 실제 설치1.13.24의 run-status initialization/public start/scheduler checkpoint/workspace reload/gRPC reload source 확인.
- 새 모형/운영 테스트: **0**. 작은 문서 검토이므로 새 모형이 필요하지 않았고, 과거 운영 단계·기존33개 리뷰·이전 모형/실측 수를 문서 리뷰의 새 실행 결과로 집계하지 않는다.
- `NOT_RUN`: Common 전체 link/plan/unittest 도구·CI·소비자 build/e2e·live UI·운영 배포. reviewer는 object-only source 검토자이며 root의 별도 gate가 필요하다. 이 원문은 그 결과를 PASS로 대신하지 않는다.
- 운영 SSH/Docker/DB/API/browser/network 호출 **0**, 제품/문서/controller 수정 **0**, 다른 리뷰어 raw **NOT_READ**. A 원문만 작성한다.

남은 불확실성은 다른 Dagster 버전/launcher/소비자의 동일 동작 여부이며 문서는 재검증을 요구한다. 이 리뷰의 CONDITIONAL을 merge PASS로 바꾸려면 같은 수정 candidate의 독립 post-fix 검토와 Common 필수 gate 결과가 필요하다.
