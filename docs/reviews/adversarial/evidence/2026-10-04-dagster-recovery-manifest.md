# Dagster 복구·공용 UI review manifest

사용자 요청: 최신 weather 기준 Dagster 실패 전파·영구 정지 방지, 재시도/복구, 메모리 감소,
transport/map/pinvi/geo의 좋은 계약 비교, 공통 Python과 weather 운영 UI 추출, 공통 로그인/메뉴
채택. 사용자 추가 승인: 독립 2인 리뷰와 live UI e2e 후 common·weather PR 병합.

| 저장소 | base | immutable candidate |
|---|---|---|
| common | `be7f21f` | `270619bd98c21ead62d077bf46f09c92dd946a59` |
| weather | `5da6e15` | `709dc44cf2661ab546a6b126ce06fcea00d666c0` |

격리: commit object-only. Windows Git로 cat-file/rev-parse/diff/show만 읽는다.
common checkout은 `F:/dev/kor-travel-common-recovery`, weather는 `F:/dev/kor-travel-weather`.
worktree 내용/이동 branch 대신 위 commit 객체를 읽고 source를 수정하지 않는다.
다른 reviewer 결과는 원본 report 확정 전 공유하지 않는다.

A: 소비자/UI 계약·접근성·로그인/메뉴·shared scope·오류/정체 표시·CSS 통합·API 안전성.
B: Dagster 생존/취소/재시도·SQL CAS/lease·메모리·부분 게시/멱등성·패키징/CI·출처.
양쪽 모두 변경 전체 delta를 검토하고 정상 실패 조건과 복구 불가 경계를 공격한다.

수용 기준: 앱 DB/provider/auth는 소비자 소유, 살아 있는 worker와 metadata 장애 보호,
terminal/만료 lease 회수, 제한된 멱등 재시도, 동명 foreign job scope, raw lineage와 전체
예산 유지, UI 주입 계약, immutable Python SHA와 npm archive digest.
common T-319/T-216·AGENTS·agent-workflow·ui-contract가 관련 정본이다.

실행 evidence: weather 전체 Python 338 passed(추가 raw/재게시 예산 시험 3 passed), ruff PASS;
frontend type/lint·63 tests·Next build PASS. common Python13/UI32 tests·type/build·tarball
Next smoke PASS, core-only wheel import PASS, tools337 중336 pass/Windows1skip.
link545/2618·plan109·SPDX102 PASS. 합성192000fact tracemalloc 446740271→12766381 bytes.
live browser e2e와 최종 CI는 진행 중이며 통과로 주장하지 않는다.
운영 배포·shared daemon 설정 적용·운영 장애 주입·다른 소비자 채택은 NOT_RUN.

산출물: execution ID/시각/실제 hash/격리 방식·범위·시도한 공격·미검토 경계,
finding `{A|B}-P{0-3}-{NN}` 위치·재현·영향·권고, verdict BLOCK/CONDITIONAL/PASS.
