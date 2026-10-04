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

- [x] metadata 장애 시 중복 예약을 만들지 않으며 외부 location의 동명 job은 막지 않는다.
- [x] 멱등성을 명시하지 않은 job은 native 자동 재시도를 상속하지 않는다.
- [x] deadline 뒤 client 재사용 금지 계약과 daemon/instance 설정 선행을 문서화한다.
- [x] wheel에서 core-only import·dagster extra·테스트가 동작한다.
- [x] 두 독립 reviewer가 동일 commit 기준선과 post-fix를 검토한다.

## 검증 기록

실행 결과와 리뷰 disposition은 같은 PR의 journal·리뷰 기록에 남긴다.
운영 장애 주입·shared plane 배포: `NOT_RUN(이번 작업은 코드 보강·UI 검증·PR 병합 범위)`.
소비자 구현 안내는 [Dagster 적용 가이드](../runbooks/dagster-adoption.md)에 둔다.

코드·단위·소비자 live 검증과 2인 review는 완료했다.
[최종 리뷰](../reviews/adversarial/2026-10-04-dagster-recovery.md),
[PR #24](https://github.com/digitie/kor-travel-common/pull/24),
[weather PR #72](https://github.com/digitie/kor-travel-weather/pull/72)에 증거를 보존한다.
IN_PROGRESS는 외부 운영 배포/채택까지 완료로 세지 않기 위해 유지한다.

## 2026-10-05 Geo 채택·최종 코드 검증

[최종 판정](../reviews/adversarial/2026-10-05-geo-common.md)에 fixed73e3ff8/Geo4c59efe, 두 독립 최종 PASS, 최초 BLOCK와 전체 수정 원문·SHA256, Python69/UI48·Geo UI231·실제 PostgreSQL17·Linux Chromium/Firefox13항목씩의 증거를 보존했다. 메모리는 유한 page·응답·동시성 구조를 적용했고 운영 RSS 실측은 NOT_RUN이다. 운영 설정/다른 앱 채택은 완료로 세지 않는다. 가이드를 포함한 common PR26·Geo PR570의 최종 checks PASS 후 merge한다.
