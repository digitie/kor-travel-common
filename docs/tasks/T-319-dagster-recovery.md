# T-319 Dagster 실행 복구 프리미티브

- 상태: IN_PROGRESS
- 우선순위: P1
- Gate: Python 단위·wheel 설치·weather 소비자 회귀·2인 리뷰
- 선행: 없음
- 외부 선행: common·weather PR 병합 및 공유 instance 설정 적용·운영 장애 복구 실측

사용자가 weather의 반복 실패·영구 정지 방지와 transport·map·pinvi·geo로 확산 가능한
Python 공통 코드를 요청했다. 문서의 단계별 Python task 순서보다 이번 사용자 요청을
우선하며 다른 task의 미구현 모듈은 완료로 표시하지 않는다.

## 범위와 근거

| 저장소 | 확인한 main | 가져온 계약 |
|---|---|---|
| weather | `5da6e15` | provider별 job·부분 게시·source lineage·unique key·run monitoring |
| transport | `6b772376` | run group 제한·job의 max runtime 태그 |
| map | `a68c2b7d` | 작업 종류별 슬롯 예약·취소 상한·run 완주 탐침 원칙 |
| pinvi | `80c92b6c` | 비멱등 outbox는 worker 재개/재시도 금지 |
| geo | `3f4ddc2d` | 생존 조회 장애를 worker 사망으로 해석하지 않음·lease와 orchestrator 분리 |

`packages/py/kor-travel-common`만 실행 정책·동기 deadline·중복 예약 방지·주입형 회수 sensor를
소유한다. DB schema·provider·계정·배포 lifecycle은 소비자에 남긴다. UI 추출은
[T-216](T-216-dagster-operations.md)에서 기록한다. transport/map/pinvi/geo 자체 변경은
이번 요청의 후속 확산 대상이며 이번 후보에서 채택 완료로 표시하지 않는다.

## 수용 기준

- [ ] metadata 장애 시 중복 예약을 만들지 않으며 외부 location의 동명 job은 막지 않는다.
- [ ] 멱등성을 명시하지 않은 job은 native 자동 재시도를 상속하지 않는다.
- [ ] deadline 뒤 client 재사용 금지 계약과 daemon/instance 설정 선행을 문서화한다.
- [ ] wheel에서 core-only import·dagster extra·테스트가 동작한다.
- [ ] 두 독립 reviewer가 동일 commit 기준선과 post-fix를 검토한다.

## 검증 기록

실행 결과와 리뷰 disposition은 같은 PR의 journal·리뷰 기록에 남긴다.
운영 장애 주입·shared plane 배포: `NOT_RUN(이번 작업은 코드 보강과 draft PR 범위)`.
