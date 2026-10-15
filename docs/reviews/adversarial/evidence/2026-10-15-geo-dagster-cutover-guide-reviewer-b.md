# Common Geo cutover 가이드 FULL 독립 리뷰 B

Review ID / execution ID: `common-geo-cutover-guide-20261015-b-025656Z`
Reviewer: B (`/root/review_finish_b`), 백엔드·배포 정합·문서 정본/규칙·실행 주장·비밀 경계.
격리: **COMMIT_OBJECT_ONLY**. moving HEAD/worktree 파일은 기준선으로 사용하지 않았다. 문서 맥락 준비 읽기 이후 formal 판정창 시작은 `2026-10-15T02:56:56Z`이며 hash/diff를 다시 고정했다.
종료 UTC: `2026-10-15T02:59:32.322163+00:00`

기준 commit: `3d3ca855f21180e46b5260a2c23b40bd74bd4624`
base: `efcd671207d7f9e2fb01251bab6854a8d543279a`
manifest SHA256: `061181adafd87cf4a60ac8039d5a8aec78626023b5a4c0d17daf75417e490210`
본인 metadata evidence SHA256: `9f9b613c412d17328401a01c1dfe4ac45444de87831e5e64d21408f21f0778f2`

| 파일 | 실제 Git blob 내용 SHA256 |
| --- | --- |
| `docs/journal.md` | `4ba3ce184ff18fc2019fd0a55646d6ea953525c14f6bc00fc944374542df9b7e` |
| `docs/runbooks/dagster-adoption.md` | `e8308f849808d0098e1bb44fb0c003a48ac6dfb7c8a933b71af63dac07c722dc` |

입력·범위: Common PR #30의 두 문서 전체 변경분 FULL 리뷰. 가이드 전체를 읽고 신규 §12와 기존 공용 API/소비자 튜닝/실측 경계를 대조했다. journal 신규 항목을 읽었고 기존 이력 bytes가 base와 그대로임을 증명했다. packages·workflow·버전·소비자 운영 변경은 범위 밖이다. 사용자 요구는 Common 소유권/규칙 충돌/정본 중복/문서 검증/과장된 실행 주장/비밀 검토다.

판정: **CONDITIONAL**. P0/P1/P2 없음, 아래 P3 두 건 OPEN. 코드·설계·운영 안전 경계를 깨는 변경은 확인하지 않았으나 P3를 수정하거나 정식 owner/task/gate/목표 시점을 가진 disposition 후 최종 merge 판정이 필요하다.

## Finding

### B-P3-01 — §12 외부 SDK 동작의 공식 source URL 누락

- 상태: OPEN.
- 위치: `docs/runbooks/dagster-adoption.md` §12의 proxy GetCurrentRuns 및 STOPPED schedule checkpoint 설명.
- 근거: Common `AGENTS.md` §7 및 `docs/runbooks/documentation-maintenance.md` §7은 외부 원문에 공식 URL과 version/commit/revision을 요구한다. 문구는 Dagster1.13.24를 고정하지만 이 두 고유 동작을 확인할 공식 source URL이 없다.
- 실패 형태/영향: 소비자가 다른 설치 버전으로 재검증할 때 proxy forwarding 및 scheduler checkpoint 구현 위치를 추측해야 한다. 공용 API 신설은 아니지만 반복 절차의 근거 추적성이 약해진다.
- 권고: 해당 버전의 공식 Dagster proxy/server 및 scheduler source reference를 추가한다. 로컬 Markdown 링크 정본 규칙과 충돌하지 않게 출처 URL 표기 형식을 유지한다.

### B-P3-02 — workspace reload와 DB 재시작을 혼동할 수 있는 문장

- 상태: OPEN.
- 위치: `docs/runbooks/dagster-adoption.md` §12 「파일과 코드 등록 순서」의 “다른 location·DB·실행 worker를 함께 재시작하는 전체 workspace reload” 문장.
- 근거: 설치 SDK1.13.24 `WorkspaceProcessContext.reload_workspace`(context.py 1281행 부근)는 각 origin에 `_load_location(reload=True)`를 호출하고 workspace/watch-thread/code-location을 교체한다. DB 서비스 lifecycle 재시작을 수행하는 메서드가 아니다.
- 실패 형태/영향: 소비자가 workspace code reload가 DB 재시작까지 포함하는 기능으로 읽을 수 있다. 실제 영향 범위와 별도 서비스 재시작 금지선을 구분해야 한다.
- 권고: 다른 location 전체 reload 금지와 DB/실행 worker 재시작 범위를 별개 문장으로 나눈다.

## 검토·검증 및 남은 범위

- Git commit/base object 해석과 두 blob의 SHA를 manifest와 직접 대조했다. 변경 경로는 정확히 두 파일이며 guide 기존 본문·journal 기존 이력은 byte 단위로 유지된다. object 간 `git diff --check` exit0을 직접 확인했다.
- AGENTS, 문서 라우터/resume, workflow §5, review archive 규칙, documentation-maintenance를 commit object로 읽었다. nested AGENTS는 없음을 tree metadata로 확인했다. 다른 reviewer raw/evidence는 열지 않았다.
- Common 라이브러리·Manager lifecycle·앱 데이터/백업/인증 소유권 분리는 기존 guide와 충돌하지 않는다. 한 소비자의 관찰을 새로운 공용 API나 모든 소비자 완료로 승격하지 않는다. journal은 가이드 링크와 작업 사실만 적고 독립적인 정책 정본을 만들지 않는다.
- 실패/timeout을 idle/미실행으로 오인하는 경우, checkpoint 정상 갱신과 상태 변경의 혼동, 오래된 bind inode, 기본 RUNNING sensor 중복 발화, retry 과거 실패 재생, repository/HTTP200만으로 daemon PASS 선언, TTL 변경·hardlink 잔존 및 UNKNOWN 재전송 시나리오를 공격적으로 읽었다. 이 문서는 소비자별 재검증과 미관측 범위를 명시하며 실제 운영 완료/최초 cron/전체 batch/RSS 감소율을 주장하지 않는다.
- 신규 diff에 실제 운영 주소·DSN·cookie·token·원본 로그·자격증명 또는 새 제품 구현은 없다. 작은 chunk 메모리 구조와 전체 운영 RSS 증명은 구분된다.
- root 제공 link/plan 검사 errors0 및 unittest336 PASS/1 SKIP는 본 reviewer가 재실행한 결과가 아니다. SKIP를 PASS로 합산하지 않았다. object-only 문서 리뷰이므로 새 모델·제품 테스트·운영 호출은 NOT_RUN이며 불필요한 테스트를 새로 만들지 않았다. 소스 URL의 실제 네트워크 조회도 NOT_RUN이다.

운영/네트워크/SSH/Docker/API/DB 호출 0, 제품·원본/다른 작업자 수정 0. 본인 scratch/raw만 작성했다. 위 finding의 post-fix commit은 원문을 보존한 별도 재검토로 판정한다.
