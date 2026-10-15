# Common Geo cutover 가이드 post-fix 독립 리뷰 B

Review ID / execution ID: `common-geo-cutover-guide-postfix-20261015-b-030905Z`
Reviewer: B (`/root/review_finish_b`).
격리: **COMMIT_OBJECT_ONLY**. 저장소 문서는 고정 commit object로만 읽었다. moving HEAD/worktree를 기준선으로 사용하지 않았다.
시작 UTC: `2026-10-15T03:09:05.661964+00:00`
종료 UTC: `2026-10-15T03:10:56.886563+00:00`

기준 commit: `7594a7179e6bb7c8f938825fa5d46197f36ddf89`
직전 FULL 리뷰 commit: `3d3ca855f21180e46b5260a2c23b40bd74bd4624`
원래 base: `efcd671207d7f9e2fb01251bab6854a8d543279a`
manifest SHA256: `f55eeb697c0d46a4dd25b5b1df1ccf311fbc25d5fef5ab55370b4b84599ff673`
초기 본인 원문 SHA256: `0a49dd8fe179ba0dd9b06c27c9b9ecfe6b3b92b5ed35d5cc4789cdc706917cb6` (보존).

| 파일 | Git blob 내용 SHA256 |
| --- | --- |
| docs/runbooks/dagster-adoption.md | 11f02a7b0ea20a314b90dcdf35b2f208e5efc7ca5c962d49b050c5ad671beed9 |
| docs/journal.md | 4ba3ce184ff18fc2019fd0a55646d6ea953525c14f6bc00fc944374542df9b7e |

범위: 초기 FULL 리뷰의 두 문서 범위 회귀와 가이드 1파일 post-fix 전체 델타, 두 P3 해결 및 추가 cursor 문구를 독립 검토했다. 제품·공용 API·운영·배포·패키지·workflow 변경은 범위 밖이다.

판정: **PASS / OPEN 0**. 초기 두 P3를 FIXED로 판정한다. 신규 P0/P1/P2/P3는 없다.

## Finding disposition

- **B-P3-01 FIXED**: §12 끝에 공식 Dagster GitHub의 1.13.24 고정 source URL 네 개(proxy servicer, scheduler checkpoint, run-status cursor, workspace reload)가 추가됐다. Common의 외부 원문 version/revision 요구를 충족하고 소비자의 실제 설치 버전 재검증을 명시한다. 로컬 설치 Dagster version.py의 1.13.24와 해당 구현 경로를 대조했다. URL의 실제 원격 열기는 root 제공 확인이며 본 reviewer의 네트워크 검증은 NOT_RUN이다.
- **B-P3-02 FIXED**: 다른 code location 전체 workspace reload와 전체 stack/DB/worker 재시작을 별도 문장으로 분리했다. workspace reload 자체가 DB를 재시작한다는 뜻이 아님을 명시한다. 로컬 SDK WorkspaceProcessContext.reload_workspace의 location 로딩·workspace 교체 구현과 일치한다.

## 검토 근거와 한계

추가 cursor 설명은 유효 RunStatusSensorCursor를 STOPPED 상태에서 저장하고 같은 instance에서 readback한 뒤 public start를 하도록 한다. None/무효 cursor는 첫 tick 시 최신 event를 읽어 초기화하고 return하는 로컬 1.13.24 구현(run_status_sensor_definition.py 700–723행)과 일치한다. 따라서 단순 start가 활성화와 첫 tick 사이 실패를 보호한다는 과장을 제거한다. 확정한 high-water를 활성화 직전에 다시 올리지 않는 기존 경계, 동일 instance cursor 보존 및 일반 retry sensor의 과거 실패 재검색 주의도 유지한다.

Git object를 직접 대조해 post-fix 변경 경로가 가이드 하나임을 확인했다. 전체 PR은 기존 두 문서뿐이고 journal은 초기 FULL 리뷰 commit과 byte 단위 동일하다. base의 기존 가이드 bytes도 그대로 보존된다. 실제 Git blob 내용 SHA는 manifest와 모두 일치하며 base→최종 git diff --check는 직접 exit0을 확인했다.

초기 FULL 리뷰에서 읽은 AGENTS·workflow·문서 유지보수·review 규칙의 소유권 및 정본 경계와 이번 델타를 회귀 검토했다. Common thin library, Manager의 Docker/workspace lifecycle, 앱별 정책·데이터·백업·인증 소유권을 바꾸지 않는다. 새 공용 API나 모든 소비자의 이전 완료를 주장하지 않고 한 소비자의 관찰을 설치 버전별 재검증 절차로 한정한다. journal은 가이드 정본을 링크하며 새 정책을 복제하지 않는다.

새 diff에는 실제 운영 주소·DSN·계정·cookie·token·원본 로그·자격증명이 없다. 공식 upstream URL은 공개 source 근거다. 문서가 실제 queue/cron/batch/RSS 실증을 새로 주장하지 않는다. 작은 문서 수정에 불필요한 새 모델·제품 테스트는 만들지 않았다.

root 제공 link 검사 682/2788 errors0, plan109 errors0, unittest336 PASS/1 SKIP는 이 리뷰에서 재실행하지 않았다. SKIP를 PASS로 합산하지 않았다. root의 공식 네 URL 열기 성공도 제공 증거로만 구분했다. 실제 운영 이전·최초 cron·소비자 E2E 및 메모리 실측은 이 문서 리뷰의 승인 범위가 아니다.

운영·네트워크·SSH·Docker·API·DB 호출 0, 제품·검토 원본 수정 0, 다른 리뷰어 raw NOT_READ. 본인 원문만 새로 작성했으며 초기 원문은 보존했다.
