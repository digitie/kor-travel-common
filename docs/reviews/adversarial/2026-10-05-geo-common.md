<!-- SPDX-License-Identifier: GPL-3.0-or-later -->
<!-- SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie) -->
# Geo 시각 구성·Dagster 복구 최종 판정

- Review ID: GEO-COMMON-20261005-CLOSURE. 종류: FULL·반복 post-fix.
- 상태: COMPLETE. 최종 코드 verdict: PASS. 열린 finding0, DEFERRED0.
- base `589a01ef63ff1ce81960e3d531874b5e4c892995`, 최종 제품 `73e3ff8b9398e533806d2d1a8435292570169de3`.
- UI 고정 제품 `426de4fbad35282bb558712d922c06268e9aba62`; 소비자 Geo `4c59efe3a778fb160b7d0a4fde2ca08967bf1531`.
- 사용자 요청·범위·정본·동일 전달 입력·격리: [manifest](evidence/2026-10-05-geo-common-manifest.md).
- 실제 실행 ID·시각·범위·관찰 hash는 각 원문에 보존한다. reviewer 사이에 원문을 공유하지 않았다.

## 두 독립 최종 원문

| Reviewer | 영역·실행 | 제품 확인 | 최종 verdict | 원문 |
|---|---|---|---|---|
| A James `/root/review_ui` | UI·소비자 계약·접근성·복구 경계 | 73e3ff8 | PASS·열린0 | [원문](evidence/2026-10-05-common-final-evidence-ui.md) |
| B `/root/review_recovery_final` | 복구 정합·race·시간 예산·검사 판별력 | 73e3ff8 | PASS·열린0 | [원문](evidence/2026-10-05-common-final-evidence-recovery.md) |

두 reviewer가 작성자와 별도로 FULL 비면제를 판단했다. 최초 UI426의 두 독립 PASS와
후속 Python 변경 전체의 두 최종 PASS를 연결한다. 이전 reviewer의 실행 실패를 새 PASS로
세지 않는다. 모든 최초 BLOCK/CONDITIONAL·post-fix 원문은 그대로 보존하고
[원문 SHA256 목록](evidence/2026-10-05-geo-common-originals.json)으로 변경 여부를 확인한다.

## Finding 반영

| Finding·원문 단계 | 반영 | 상태·재확인 |
|---|---|---|
| UI569/b2/27: 필터·제어 선택 null·공개 타입·50행 계약/이관 | 전체 입력에서 필터, snapshot 밖 선택 null, 타입 호환, Breaking/Migration 가이드 | UI426 A/B PASS·FIXED |
| 실제 multiprocess 자식 종료가 일반 RUN_EXCEPTION이라 제외됨 | RUN_EXCEPTION/DagsterSubprocessError와 모든 FRAMEWORK_ERROR/ChildProcessCrashException의 명시적 증거 | 실제 os._exit42 fixture와 provider/mixed/unknown 거부·FIXED |
| C-CHILD-P1-01: 느린 100+1 STEP 페이지 반복/늦은 쓰기 | 부분 cursor와 누적 증거 저장·전체10초 및 작업5초 예산 | 독립 재현·FIXED |
| B-C-P1-01 / B-P1-01: 느린 종료/STEP/추가 metadata가 완료 위치를 잃음 | 검증 직후 추가 IO 전에 complete phase 저장, 다음 tick scope·native·예산·중복 재확인 | 실제3.1/5.1/2.1초 조회·FIXED |
| C-PHASE-P1-01: 완료 뒤 provider STEP을 무시함 | 최신 RUN/STEP ID 대조, 새 기록이면 partial로 복귀하여 cursor 이후 재검증 | actual SQLite provider 요청0·태그0·FIXED |
| C-MERGE-P2-01: 늦은 정상 child STEP에서 complete/run/head 순환 | 마지막 검증 STEP storage ID를 저장하고 검증한 최신 STEP 속성을 재확인, 새 기록은 다음 tick에서 재검증 | 같은 새 테스트가 ab21 source2FAIL·73e3 source PASS, 두 원 reviewer 재확인·FIXED |

severity는 원문 그대로다. summary에서 낮추거나 운영 위험 수용으로 닫지 않았다.

## Coordinator가 실행한 gate

- common Python: ruff PASS, Dagster1.13.24에서69 PASS. 실제 자식 os._exit42 포함.
- UI48 PASS, build/type/examples/pack PASS; 설치한 tarball의 Webpack·Turbopack Next smoke PASS.
- 문서 validator·task/DAG validator PASS; 도구337 tests 실행(1 SKIP, PASS로 집계하지 않음).
- Geo: ruff·mypy166 files·lint-imports PASS, 전체1787 PASS/111 SKIP, 집중153 PASS.
- Geo UI lint/type/build·231 tests PASS; React Doctor90점(기존 baseline 이슈 포함).
- 기존 PostgreSQL의 별도 UUID schema에서 실제 owner·MV swap·반경 TRUNCATE/INSERT rollback17 PASS.
  이 테스트는 geometry 실행계획 대신 실제 transaction 경계를 검증한다. DB/RustFS 서비스를 변경하지 않았다.
- Linux n150 Chromium·Firefox가 실제 읽기 전용 API·Dagster를 사용하여 각각13항목 PASS,
  pageerror0. 로그인/로그아웃·scope·선택/검색/필터·키보드·모바일·실제 API 중단/마지막 결과/복구를 확인했다.
  [결과](evidence/2026-10-05-geo-live-results.json), [Chromium](https://github.com/digitie/kor-travel-geo/blob/main/docs/reviews/evidence/2026-10-05-geo-live-chromium-desktop.png),
  [Firefox](https://github.com/digitie/kor-travel-geo/blob/main/docs/reviews/evidence/2026-10-05-geo-live-firefox-desktop.png), [모바일](https://github.com/digitie/kor-travel-geo/blob/main/docs/reviews/evidence/2026-10-05-geo-live-chromium-mobile.png).
- 제품 후보 CI8개 PASS: [docs/packages/tools](https://github.com/digitie/kor-travel-common/actions/runs/37242161698),
  [Python3.11/3.13](https://github.com/digitie/kor-travel-common/actions/runs/37242161740).
  문서 closure를 포함한 PR 최종 head도 필수 checks 전부 PASS 후 merge한다.

검증자의 본인 PASS와 coordinator의 외부 PG/live PASS를 합산하지 않는다.
로그·스크린샷과 정확한 hash는 [검증 기록](evidence/2026-10-05-verification.json)에 남긴다.

## 미실행·적용·롤백

운영 daemon/queue 설정 전환·운영 worker 강제 종료·전체 provider/geometry 재적재·실측 RSS는
NOT_RUN이다. 단일 storage 호출이10초를 넘는 경우 metadata가 정상화될 때까지 재시도 판단을
보류하며 Python thread를 강제로 중단할 수 있다는 보장은 없다. 50행은 DOM 상한이고
서버 snapshot 자체를50건으로 잘라 집계한다는 뜻은 아니다. 다른 map/pinvi의 채택은 후속이다.

[Dagster Python·UI 적용 가이드](../../runbooks/dagster-adoption.md)를 PR에 함께 올린다.
[common PR26](https://github.com/digitie/kor-travel-common/pull/26),
[Geo PR570](https://github.com/digitie/kor-travel-geo/pull/570).
rollback은 소비자의 immutable Python pin/UI tarball을 이전 검증판으로 되돌린다. schema migration은 없다.
이 후속 commit은 원문·disposition·검증 근거·현재 기록·index만 추가한다. 제품 tree는 위 후보와 같다.

## 원문 bytes와 Git 표시본

[Canonical 원문 JSON](evidence/2026-10-05-review-originals.json)은 reviewer가 저장한 UTF-8/BOM/CRLF·말단 공백·빈 줄까지 그대로 보존한다. Git 공백 검증과 text 변환 때문에 Markdown 표시본만 LF·말단 공백/빈 줄을 정규화했다. finding·severity·verdict·본문 내용은 바꾸지 않았다. JSON의 sha256은 JSON raw_utf8를 UTF-8로 encode한 원본 bytes, display_sha256은 표시본 hash다. 모든 JSON 복원 원본의 hash를 생성 후 재확인했다. 원본을 수정한 것으로 오해하지 않도록 이 차이를 명시한다.

Common은 전체 Git text 스캔을 유지하므로 binary 스크린샷은 소비자 Geo PR570에 보존하고 링크한다. 원문 archive도 UTF-8 JSON으로 저장해 스캔을 우회하지 않는다.
