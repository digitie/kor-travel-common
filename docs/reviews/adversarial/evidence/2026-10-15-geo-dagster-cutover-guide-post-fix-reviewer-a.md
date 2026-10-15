# Common Geo 이전 가이드 독립 FULL post-fix 리뷰 A

- reviewer execution ID: `review_finish_a-common-geo-cutover-guide-7594a717-20261015-r2`
- reviewer: `/root/review_finish_a` — Dagster 동작·복구 순서·missed/replayed failures·보장 범위
- 시작: `2026-10-15T03:04:51Z`
- 종료: `2026-10-15T03:05:17Z` (대상·근거 검토 종료; 원문 저장은 이후)
- 격리: **commit object-only**. `git show`/`git diff`로만 Common 내용을 읽었으며 별도 checkout은 없어 clean 상태 N/A, source 수정0이다.
- merge verdict: **PASS** — 문서 리뷰 finding 모두 FIXED, 신규·잔여 OPEN0. root의 별도 Common 필수 검사/CI·PR gate 실행을 대신하는 판정은 아니다.

## 요청·기준선·전체 범위

요청은 초기 원문을 보존하고 같은 두 문서 범위에서 post-fix19줄과 회귀를 독립 재검토하는 것이다. 다른 리뷰어 raw 접근·운영·source 변경은 금지한다.

- repository: `kor-travel-common-codex-cutover` Git object database
- manifest: `common-geo-cutover-guide-postfix-20261015.manifest.json`
- manifest SHA-256: `f55eeb697c0d46a4dd25b5b1df1ccf311fbc25d5fef5ab55370b4b84599ff673`
- actual head: `7594a7179e6bb7c8f938825fa5d46197f36ddf89`
- previous head: `3d3ca855f21180e46b5260a2c23b40bd74bd4624`
- original base: `efcd671207d7f9e2fb01251bab6854a8d543279a`

| 파일 | commit blob SHA-256 |
| --- | --- |
| docs/runbooks/dagster-adoption.md | 11f02a7b0ea20a314b90dcdf35b2f208e5efc7ca5c962d49b050c5ad671beed9 |
| docs/journal.md | 4ba3ce184ff18fc2019fd0a55646d6ea953525c14f6bc00fc944374542df9b7e |

전체 두 파일의 원래 base 대비 범위와 candidate §12를 다시 읽고 previous→head delta를 검토했다. journal은 previous와 bytes 불변이다. 초기 FULL 원문 `common-geo-cutover-guide-review-a-20261015.md` SHA `34437b6c11eded773c536cfbbf1a14c774195e09ccb327f70528151bb2f6dbae`는 변경하지 않았다. Common AGENTS/workflow에서 요구한 finding·판정 어휘와 object-only 절차를 이어 적용했다.

## Finding disposition

### A-P2-01 — **FIXED**

`docs/runbooks/dagster-adoption.md:405`~410에 확정한 high-water의 **유효 RunStatusSensorCursor를 STOPPED 상태로 저장→같은 instance에서 readback→public start_sensor** 순서를 추가했다. None/invalid cursor이면 첫 tick 당시 최신 event에서 초기화할 수 있으므로 public start만으로 활성화~첫 tick 사이 실패가 보호되지 않는다는 경고도 명시했다. 활성화 직전 기준 재상향 금지·같은 instance cursor/미처리 실패 보존·다른 instance cursor 복사 금지를 유지한다.

이는 초기 리뷰에서 읽은 실제1.13.24 run-status 초기화 분기(최신 event/SkipReason/return)와 start_sensor가 cursor를 prime하지 않는 동작을 구분한다. 초기 실패 시나리오를 문서가 직접 다루므로 닫는다. 모든 실패의 자동 복구나 실제 실패 처리 완료를 새로 보장하지 않는다.

### A-P3-01 — **FIXED**

`docs/runbooks/dagster-adoption.md:386`~389에 다른 code location 전체를 reload하는 workspace reload와 전체 stack/DB/worker 재시작의 범위를 분리했다. workspace reload 자체가 DB를 재시작한다는 뜻이 아님을 명시한다. 실제 `reload_workspace`의 location reload 경로와 맞으며 잘못된 결합 표현을 제거했으므로 닫는다.

## 전체 델타 회귀와 근거

- 새 공식 원문 링크4개는 Dagster **1.13.24** release ref의 proxy/scheduler/run-status/workspace source 경로를 가리킨다. 초기 독립 검토의 실제 설치 source 경로와 주제에 대응한다. 공식 링크를 추가해 다른 소비자가 설치 버전과 원문을 재검증할 수 있다. 다른 리뷰어 원문은 읽지 않았고 그 finding closure를 대신 판정하지 않는다. 외부 URL의 HTTP 성공 여부는 이 실행에서 조회하지 않았다.
- proxy UNIMPLEMENTED≠idle, child/metadata/tick 확인, STOPPED checkpoint 한 필드 제한, 실제 bind inode 확인, 원본 drain→정상 종료→새 등록→큐 실행→instigation 복원 순서는 그대로다.
- Noop 실제 설정/출력/DB·artifact 무변경, backup/catalog·expires_at·keep-min·allowroot·UID·일정 메모리 chunk checksum·hardlink 정리, partial/UNKNOWN 무재전송도 보존한다.
- journal은 새 API/앱 tuning/전 소비자 채택 완료를 주장하지 않는다. 최초 cron·소비자 운영 결과를 별도 검증으로 남긴다. 공개 host/DSN/cookie/secret 값이 추가되지 않았다.
- 관측하지 않은 실제 cron/전체 batch/운영 RSS·모든 버전 안전성을 성공으로 표시하는 회귀는 없다. 다른 Dagster/consumer에서의 동작은 여전히 재검증 대상이다.

## 실행·미실행

실행: `git rev-parse <head>^{commit}`, manifest/두 blob SHA, 이전·원래 base 대비 object diff와 candidate 본문 검토, `git diff --check <previous> <head>` 및 `git diff --check <base> <head>` 모두 EXIT0, journal 불변 확인. 새 모형0, 이전 운영 단계/33개 리뷰/다른 모형 수 재집계0이다.

`NOT_RUN`: Common 전체 link/plan/unittest 도구·CI·소비자 build/e2e/live UI/배포 및 외부 URL network 조회. 이 source 리뷰의 PASS는 별도 실행 gate를 통과로 표시하지 않는다. 기존 SDK 근거는 초기 리뷰에서 실제 설치 source를 읽은 범위에 한정하며 운영 환경을 새로 조회하지 않았다.

운영 SSH/Docker/DB/API/browser/network 호출 **0**, Common source·문서·controller 수정 **0**, 다른 리뷰어 raw **NOT_READ**. A 새 원문만 작성했다. **최종 verdict: PASS / OPEN0**.
