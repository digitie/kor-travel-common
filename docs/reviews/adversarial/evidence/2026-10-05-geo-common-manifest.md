<!-- SPDX-License-Identifier: GPL-3.0-or-later -->
<!-- SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie) -->
# Geo 대시보드·Dagster 복구 최종 리뷰 manifest

- Review ID: GEO-COMMON-20261005-FINAL.
- 사용자 요청: Geo 시각 구성을 공용 dashboard에 반영하고 common Python 복구·로그인·메뉴를 Geo에 채택한다. 두 독립 적대 리뷰, 실제 Linux UI E2E, common·Geo PR 머지.
- common base: `589a01ef63ff1ce81960e3d531874b5e4c892995`; 최종 제품 `73e3ff8b9398e533806d2d1a8435292570169de3`.
- Geo base: `3f4ddc2dac3f31634a23ef0e9592f419e29e7d14`; 최종 제품 `4c59efe3a778fb160b7d0a4fde2ca08967bf1531`.
- UI tarball 소스 고정 후보: common `426de4fbad35282bb558712d922c06268e9aba62`. 후속 common 변경은 Python 복구·테스트·가이드이며 UI tarball을 같은 버전으로 다시 만들지 않았다.
- 범위: UNKNOWN 격리, run/lease CAS, worker·root 게시 검증, step/retry 예산, 유한 keyset cursor, provider 오류 거부, native/fallback 중복 방지, 공용 UI의 선택·검색·필터·pagination·tick·마크업·인증·모바일 계약.
- 범위 밖: 운영 daemon/queue 설정 전환, 비멱등 적재·복원 자동 재시도, 데이터 전체 재적재, 운영 worker kill, RSS 실측, map·pinvi의 실제 채택.
- 정본: [common AGENTS](../../../../AGENTS.md), [workflow](../../../runbooks/agent-workflow.md), [T-216](../../../tasks/T-216-dagster-operations.md), [T-319](../../../tasks/T-319-dagster-recovery.md), [Dagster 가이드](../../../runbooks/dagster-adoption.md). Geo ADR-068과 각 저장소 AGENTS를 적용한다.
- 판정 수용 기준: P0/P1 미해결0, 기존 재현의 수정 전 FAIL/수정 후 PASS, 공통 공개 API/CSS 및 vendor provenance 보존, 오류 시 마지막 snapshot·복구, 표 50행과 유한 응답, 두 독립 reviewer의 최종 판정과 실제 소비자 E2E.
- Reviewer A: `/root/review_ui`, James, UI·소비 계약·접근성과 복구 경계.
- Reviewer B: `/root/review_recovery_final`, 복구 정합·race·시간 예산. 기존 `/root/review_recovery`의 완료 원문도 보존하며, 후속 실행 실패를 새 PASS로 집계하지 않는다.
- 격리: 고정 SHA를 source archive 또는 Git 객체로 확인, 원래 dirty checkout과 다른 reviewer 원문은 읽지 않는다. 제품 파일을 변경하지 않고 본인 SQLite/SQL 기록 fixture만 실행한다. 정확한 명령·시각·관찰 SHA·미실행 범위는 각 원문에 기록한다.
- 동일 최종 전달 요청: 위 두 SHA에서 기존 재현과 전체 delta 회귀를 독립 재검토하고, 완료 검증의 최신 failure evidence 확인/추가 IO 전 checkpoint 저장, radius parts 별도 commit의 owner guard 전달·검증을 확인한다. 원문과 SHA256을 새 파일로 남기고 다른 리뷰 결과는 읽지 않는다.
- 실행 가능한 검증: common `ruff check src tests`, `pytest -q`(Dagster1.13.24); UI `npm run build`, `npm run check`, `npm test`; Geo `ruff check .`, `mypy src/kortravelgeo scripts/export_openapi.py`, `lint-imports`, `pytest -q`, UI lint/type-check/test/build. 외부 PostgreSQL와 Linux live는 coordinator가 별도 수행하며 reviewer의 본인 PASS와 합산하지 않는다.

최종 전달 delta: 검증한 STEP storage ID를 포함한 6필드 checkpoint, 최신 failure ID 변경 시 partial phase로 복귀, 이전 3/5필드 재검증. RUN_FAILURE 뒤/완료 phase 뒤의 정상 child crash도 유한 tick에1회 복구되어야 하고 provider는 거부한다. common69PASS와 동일 테스트의 ab21 source2FAIL을 별도 원문으로 재확인한다. 두 reviewer에게 같은 fixed SHA와 delta를 전달했다.
