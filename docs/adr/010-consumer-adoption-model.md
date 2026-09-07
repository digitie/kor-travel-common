# ADR-010: 소비자 채택 모델(매니페스트·첫 소비자 순서·라이선스 gate·채택 PR 규격·시각 기준선·NOT_RUN)

- 상태: partially superseded by ADR-013
- 날짜: 2026-09-06
- 근거 문서: `docs/plan/design-brief.md` D-16·D-19·D-20·D-21·D-24·D-25·D-28, `docs/survey/cross/licensing.md` §3.6·§4 B1·L6·L8, `docs/survey/inventory/kor-travel-weather.md` §8-1, `docs/survey/inventory/kor-travel-airport.md` §1·§9, 선행 보고서 §1(map↔pinvi 이식 관계)·§11(회수 지표), `docs/survey/cross/canview-structure-checklist.md` R1.12·R1.13

## 컨텍스트

소비자 7개는 라이선스(pinvi 미결, ktc·ktdm MIT)·React 세대(geo·ktdm 18)·lockfile·CI 폭이 달라 한 번에 채택할 수 없다. map admin은 UI 정본이고 weather는 map 값을 그대로 복사한 순수 CSS라 값 무변경 토큰 교체가 가능하다(`inv/kor-travel-weather` §8-1). pinvi admin은 map 이식본이라 ui 채택 가치가 가장 크지만 L6 전에는 추출·소비 모두 막힌다(B1). airport Admin은 무인증 백업 패널이고 WIP 브랜치가 병합 전이다. 시각 회귀 기준선은 어느 앱에도 없고, common에서 소비자 빌드·e2e를 실행할 수 없다.

## 결정

1. 첫 소비자·순서(D-16): L6 결정은 common T-020에서 완료하고, 실제 LICENSE 반영 확인(T-420)을 Phase 0 외부 gate로 둔다. tokens 1차 = map + weather(즉시) + pinvi admin(L6 완료 조건) + airport(WIP 병합 후). ui 1차 = map + pinvi admin(L6); L6가 T-2xx 착수까지 미결이면 airport 소형 부품으로 대체. Python 1차 = map-api·weather-api·airport, 2차 geo, 3차 pinvi·concierge·ktdm(L8 후, breaking 묶음). concierge·ktdm은 L8 전에는 규칙 문서·`tokens.json` 참조까지만.
2. 소비자 매니페스트(D-19): 각 소비 저장소(모노레포는 앱 디렉터리)에 `kor-travel-common.lock.json`(schema `kor-travel-common.consumer-manifest.v1`): `repo`·`app`·`tokens{version,override}`·`ui{version}`·`python{version}`·`lockfiles[]{kind,path,scope}`·`contrast{baseline,dark}`·`ux_gate{baseline}`·`openapi{exceptions}`·`exceptions[]`. `enforce`는 두지 않는다(common `versions.json` 소유). `lockfiles.path`는 소비자 저장소 루트 기준이고 `scope`는 보고 label 겸 npm workspace 선택자이며, 검사 도구는 manifest 경로와 저장소 루트를 함께 받아 루트 workflow를 포함한다(T-011). `docs/integration-map.md`는 `tools/collect_manifests.py`가 `consumers.pins.json`에서 생성한다(수기 편집 금지).
3. airport Admin 정의(D-20): 현 실체 = 무인증 백업 패널 + collector-status 패널 + `/v1/admin/*`. 1차 = tokens + 소형 부품. 셸·로그인 소비는 T-035 라우트 분리 후(O-9).
4. 시각 회귀 기준선(D-21): 토큰·스타일·셸을 바꾸는 소비자 PR은 착수 전 6폭(320/375/414/768/1024/1440) 스크린샷 기준선 + 완료 diff를 **PR evidence**로 남긴다(저장소 파일 아님). Playwright 없는 앱(wx·ktdm)은 `templates/playwright.baseline.ts`.
5. 이관 PR 규격(D-24): 한 PR = 한 산출물, 프레임워크 업그레이드 PR과 분리, `git revert` 1회로 원복, lock 동반 커밋, 본문에 검사 결과·스크린샷·되돌리기 명령, 파일 상한(tokens 10·ui 30·py 10, 초과 시 분할). `templates/consumer-pr.md`.
6. NOT_RUN(D-25): common에서 실행 못 한 검증은 evidence에 `NOT_RUN(사유)`로 남기고 DONE 전 `외부 선행`으로 승격한다. 0 test·skip을 pass로 집계하지 않고, 명령을 적은 것은 실행 증거가 아니다.
7. 회수 측정(D-28): 분기 `docs/reports/adoption-YYYY-QN.md`에 선행 보고서 §11 지표 + drift·EXEMPT·enforce 전환 수. 순절감 ≤0 2분기 → 범위 축소; npm 소비자 우회 패치 ≥2 → 배포 방식 재검토.
8. 소비자 저장소는 직접 수정하지 않는다. 외부 선행(L6·L8·WIP 병합·React 19)은 결정 기록·LICENSE-only PR 요청 문서와 외부 evidence(T-020·T-021·T-420·T-505)로 추적하고, 코드 채택 PR(T-454·T-473)은 그 evidence를 소비한다.

## 대안 검토

- **pinvi admin을 1차에서 제외하고 L6를 기다리지 않음**: 지시 (3)(PinVi Admin 포함)을 충족하지 못한다. L6를 Phase 0 외부 확인으로 승격하고 대체 경로(airport 소형)를 둬 지연을 흡수한다.
- **매니페스트에 `enforce` 포함**: 앱 자율 선언이 되어 지시 (2)를 완화한다(ADR-008).
- **시각 기준선을 저장소 파일로 커밋**: 스크린샷 바이너리가 저장소를 비대하게 하고 기준 폭·브라우저가 바뀌면 stale이 된다. PR evidence로 둔다.
- **여러 산출물을 한 PR로**: 원인 불명 diff의 revert 단위가 커진다. 한 PR = 한 산출물.

## 결과

- 채택은 map·weather에서 시작되어 값 무변경(시각 diff 0)으로 첫 회수 지표를 만든다.
- pinvi·ktc·ktdm 트랙은 common 결정이 완료됐지만 각 소비자 LICENSE PR evidence 전에는 `adoption-readiness.md`에서 외부 반영 대기 `OPEN`으로 둔다.
- 모든 소비자 PR이 6폭 evidence·되돌리기 명령을 요구하므로 채택 PR의 리드타임이 길어지지만 revert 1회 원복이 보장된다.
- `integration-map.md`는 T-012 전까지 수기 초기판이며 그 뒤 생성물로 전환된다.

## 후속·적용 위치

- 현재 설계: `docs/architecture/consumers.md`, `docs/architecture/adoption-readiness.md`, `docs/integration-map.md`
- 절차: `docs/runbooks/consumer-adoption.md`(T-007), `templates/consumer-pr.md`·`templates/consumer-adoption-checklist.md`
- 도구: T-011(매니페스트 스키마·`validate_manifest`), T-012(`collect_manifests`), T-108(playwright 기준선), T-402(기준선 초기 캡처)
- 외부 확인: T-420(pinvi LICENSE), T-021의 concierge·docker-manager license-only evidence, T-430(airport WIP), T-443(geo React 19)
- 보고: T-503(회수 1회차), T-506(분기 감사)

후속: [ADR-013](013-package-release-execution-contract.md)이 릴리스 실행·peer 호환·검증 소비자에 관한 위 일부 조항을 구체화한다. 나머지 결정은 유지한다.

## 라이선스 결정 갱신(2026-09-08)

O-1·O-2는 사용자의 GPLv3 통일 지시로 common 결정이 완료됐다. adoption-readiness의 pinvi·concierge·docker-manager 셀은 WAIT에서 외부 반영 대기 OPEN으로 바꾸며, 실제 소비자 PR과 SHA가 없는 상태에서 G-LIC를 PASS로 표시하지 않는다. common은 소비자 저장소를 수정하지 않는다.
