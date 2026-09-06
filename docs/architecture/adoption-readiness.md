# 채택 준비 기준(adoption readiness)

- 정본 지위: 소비자별 채택 gate 정의와 현재 판정의 추적표(초안). §3 매트릭스는 T-012부터 `tools/collect_manifests.py` 출력으로 갱신하며 §2 gate 정의만 수기로 유지한다. 확정 task: T-008(★이번 PR)·T-012. 마지막 갱신: 2026-09-06.
- 근거: [브리프](../plan/design-brief.md) D-06~D-08·D-16·D-17·D-19·D-21·D-25, O-1·O-2·O-6·O-8·O-9·O-25, `docs/survey/commonality-matrix.md` §3.2·§4.1, `docs/survey/cross/licensing.md` §3.6·§4, `docs/survey/cross/version-matrix.md` §1.1·§2.1·§3.2, `docs/survey/cross/ci-deploy.md` §1.1·§1.2, `docs/survey/cross/design-tokens.md` §3.4.2.

이 문서는 [아키텍처 개요](README.md)의 소비자 경계를 gate와 남은 조건으로 통합한다. 소비자 개요는 [소비자](consumers.md), 개별 채택 범위와 acceptance는 해당 [상세 task](../tasks/)가 정본이다. canview `requirements-coverage.md`의 "요구 → 정본 → task → 검증 상태 → 남은 gate" 형식을 "소비자 → gate → 정본 → task → 현재 상태 → 남은 gate"로 바꾼 것이다.

## 1. 범위와 판정

비교 기준: 조사 기준 커밋(`docs/survey/README.md` §2.1 — kta `2bb1111`/WIP `99b3f98`, ktc `7945305`, ktdm `862562d`, geo `1d9d74d`, map `c494e227`, wx `6003da9`, pinvi `9af25e5`), 2026-09-06. 이 문서는 요구의 새 정본이 아니라 추적표다. 정본(규칙 문서·ADR·`versions.json`)이 바뀌면 해당 행과 상세 task를 같이 대조한다.

**어느 소비자도 채택을 시작하지 않았다. 채택 버전은 전부 "미채택"이며 아래 gate 상태는 조사 사실에서 도출한 초기값이다.** 계획 문서·WIP 브랜치·조사에서 확인한 코드의 존재를 채택 완료로 표시하지 않는다. common에서 실행하지 못한 검증(시각 기준선·소비자 빌드·e2e)은 `NOT_RUN`으로 남기고 DONE 전에 `외부 선행`으로 승격한다(D-25). 0 test·skip을 pass로 집계하지 않는다.

상태 어휘: `PASS`(조건 충족을 근거 절로 확인) · `OPEN`(미충족, 남은 조건 있음) · `EXEMPT`(`versions.json` `exceptions[]` 또는 앱 baseline에 `until`과 함께 등록) · `WAIT`(사용자 확인 O-n 대기) · `N/A`(해당 없음) · `NOT_RUN`(실행 근거 없음).

## 2. gate 정의

| gate | 판정 기준 | 정본 | 검사 수단 |
|---|---|---|---|
| G-LIC 라이선스 | 소비자 루트 라이선스가 GPL-3.0-or-later와 정합: L6(pinvi 선언·공개), L8(ktc·ktdm 정렬), L9(map 전문 복원), L10(geo `-only` 병기 또는 재선언), L11(`license` 필드). **코드 링크 전 필수**; 규칙 문서·`tokens.json` 참조는 면제 | [licensing](../standards/licensing.md), [ADR-004](../adr/004-gpl-3-0-or-later-and-provenance-gate.md) | 사용자 결정(O-1·O-2) + 각 저장소 PR 확인 |
| G-REACT React 19 | `react`·`react-dom` 설치본 `^19.0.0` (ui 채택에만 필수; tokens·py는 무관) | `versions.json`, [ADR-007](../adr/007-react-ui-package-delivery.md) | `check_versions` |
| G-LOCK lockfile | `package-lock.json` v3 커밋 + `npm ci`; `uv.lock` 커밋 + CI·Docker `--locked` | [versions](../standards/versions.md), D-07 | `check_versions` `NO_LOCK` |
| G-CI | CI 존재, `check_versions` report job 삽입, 액션 SHA 핀 | [ci-deploy](../standards/ci-deploy.md), D-18 | T-403; `versions-check.yml` |
| G-NODE | CI Node 22(floor 22.12) | D-06 | `check_versions` `NO_ENGINES`/`BELOW_FLOOR` |
| G-TW4 Tailwind v4 | Tailwind ≥4.3.0 설치 + `@config` 없음(CSS-first) | [ADR-012](../adr/012-tailwind-v4-migration-policy.md), [스타일 배포](style-delivery.md) §4 | `check_versions` + 채택 PR 리뷰 |
| G-WIP | airport WIP `codex/shadcn-ui-foundation` 병합(값 유지) | D-08 ①, O-9 | airport PR·CI 확인 |
| G-VIS 시각 기준선 | 6폭(320/375/414/768/1024/1440) 스크린샷 기준선을 착수 전 PR evidence로 캡처 | D-21, `templates/playwright.baseline.ts`(T-108) | T-402(NOT_RUN 허용) |
| G-CONTRAST | 브랜드 오버라이드가 `kt_contrast` light 쌍 통과 또는 `contrast-baseline.json` 등록 | [design-tokens](../standards/design-tokens.md) | `contrast-check.yml`(T-103) |
| G-MANIFEST | `kor-travel-common.lock.json`(`consumer-manifest.v1`) 커밋 | D-19, T-011 | `tools/validate_manifest.py` |
| G-OA OpenAPI 산출물 | export 산출물 커밋 + `--check` CI(M1) 또는 예외 등록 | [openapi](../standards/openapi.md), `openapi-exceptions.yaml` | `openapi-drift.yml`(T-309) |

## 3. 소비자 × gate 매트릭스(초기값, 2026-09-06)

| 소비자 | G-LIC | G-REACT | G-LOCK npm / py | G-CI | G-NODE | G-TW4 | G-WIP | G-VIS | G-CONTRAST | G-MANIFEST | G-OA |
|---|---|---|---|---|---|---|---|---|---|---|---|
| kta | OPEN(루트 GPL 원문은 있음; L11 `license` 필드·`-or-later` 명시) | PASS(19) | PASS / OPEN(CI만 `--locked`, Docker `pip install -e`) | OPEN(3~5종; prod `live-e2e` required 금지 권고) | PASS(22) | OPEN(main 미도입; WIP 4.3.3) | WAIT(O-9) | NOT_RUN | OPEN(alpha line 유지, 미검증) | OPEN | OPEN(export만, CI 없음; 스펙 422 불일치 예외 등록) |
| ktc | WAIT(O-2, L8) | PASS(19) | PASS / OPEN(lock 없음, `requirements.txt` 4벌) | OPEN(CI 없음) | N/A(CI 없음; `engines >=22`) | OPEN(4.x + `@config`, hex fallback 블록) | N/A | NOT_RUN | OPEN(`dt` §3.4.2 미달) | OPEN | OPEN(산출물 없음) |
| ktdm | WAIT(O-2, L8) | OPEN(18.3.1 → T-470) | PASS / OPEN(Poetry lock 없음) | OPEN(2 job; `check_versions` 없음) | OPEN(20) | OPEN(4.3.1 `@theme`; `ops-*` CSS) | N/A | NOT_RUN | OPEN(`dt` §3.4.2 미달) | OPEN | OPEN(산출물 없음) |
| geo | OPEN(`-only` 병기, O-20) | OPEN(18.3.1, ADR-019 → O-25·T-443) | PASS / OPEN(lock 없음) | OPEN(`check_versions` 없음; openapi·typegen drift는 PASS) | OPEN(20) | OPEN(4.3.1 + `@config` 잔존) | N/A | NOT_RUN | OPEN(`outline-color: color-mix` 반투명 기본, 미달) | OPEN | PASS(`--check` + `openapi.yml`; v1 VWorld 예외 등록) |
| map | OPEN(L9 25행 요약본 → 전문 복원, `license` 필드) | PASS(19) | PASS(v3 + `verify:npm-tree`) / OPEN(lock 없음) | OPEN(`check_versions` 없음; 10종+ gate) | PASS(22.23.1; npm 12.0.1 exact는 `EXEMPT` 등록 대상) | PASS(4.x, `@theme inline`, `@config` 없음) | N/A | NOT_RUN | PASS(map만 수치 검증, `dt` §3.4.2) | OPEN | PASS(profile 3종 `--check`; `starlette<1.0` 예외) |
| wx | PASS(GPL-3.0; L11 `license` 필드는 OPEN) | PASS(19) | PASS / PASS(`uv.lock` CI·Docker `--locked`) | OPEN(vitest·mypy 미실행; `check_versions` 없음) | OPEN(20) | OPEN(미도입; Phase 1은 `tokens.css` 교체만이라 tokens 채택에는 N/A) | N/A | NOT_RUN | OPEN(navy 오버라이드 미검증) | OPEN | OPEN(export + `git diff`; `--check` 전환 T-481) |
| pinvi admin | WAIT(O-1, L6; README/AGENTS 상충) | PASS(19.2.6 override) | PASS(`check:lockfile`) / OPEN(`uv.lock` 미소비) | OPEN(`check_versions` 없음; aggregate gate 보전) | PASS(22 + npm 11.19.1) | OPEN(4.x + `@config` v3 preset) | N/A | NOT_RUN | OPEN(admin hex, 미검증) | OPEN | OPEN(산출물 없음; `{error:{}}`·정수 `If-Match` 예외 등록) |
| pinvi 사용자 웹 | WAIT(O-1) | N/A(코드 소비 없음) | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A |
| pinvi 모바일 | WAIT(O-1) | N/A | N/A | N/A | N/A | WAIT(O-8; Tailwind 3.4.19·NativeWind 4) | N/A | N/A | N/A | N/A | N/A |

## 4. 소비자 → 배포 단위별 남은 gate

| 소비자 | 배포 단위 | 정본 | task | 현재 상태 | 남은 gate |
|---|---|---|---|---|---|
| map | tokens | ADR-006, style-delivery | T-410 | 미채택 | T-109 정식 → G-VIS(6폭 diff 0) → G-MANIFEST; L9·`license` 필드 동반 |
| map | ui | ADR-007, ui-contract | T-411·T-412 | 미채택 | T-212·T-213 → `@source` → e2e 30·vitest 42 green |
| map | py | ADR-011, openapi | T-480 | 미채택 | T-310 → `openapi.yml` 무변경 또는 pinvi·ktdm pin 갱신 PR 동반 |
| wx | tokens | ADR-006, ADR-012 ⑥ | T-461 | 미채택 | T-109·T-102 shim → 6폭 diff 0(수동 evidence) |
| wx | ui | ADR-007 | T-463 | 미채택 | T-460(Next 16·Vitest 4·Node 22) → T-462(v4 도입) → T-213 |
| wx | py | ADR-011 | T-481 | 미채택 | T-310 → `--check` 전환 → L15 airkorea 정본 |
| kta | tokens | ADR-006, D-20 | T-431 | 미채택 | G-WIP(T-430, O-9) → T-109 → 320px 게이트 |
| kta | ui(소형) | ADR-007 | T-432 | 미채택 | T-431·T-212 |
| kta | py | ADR-011, ADR-009 | T-482 | 미채택 | T-310 → `code`/`request_id` additive → 스펙 422 정합 |
| pinvi admin | tokens | ADR-006, D-29 | T-421 | 미채택 | G-LIC(L6, T-020·T-420) → T-109 → 사용자 표면 무변경 e2e |
| pinvi admin | ui | ADR-007 | T-422 | 미채택 | T-421·T-213 → `AdminTable` 어댑터 유지·44px 예외 등록(O-21) |
| pinvi | py | ADR-011 | T-484 | 미채택 | T-310·T-420 → `uv.lock` 소비·etl `@main` 제거 |
| geo | tokens | ADR-006, ADR-012 ③ | T-441 | 미채택 | T-109 → `@config` 실효값 빌드 검증 → `@theme` 단일화 → G-CONTRAST baseline |
| geo | ui | ADR-007 | T-444 | 미채택 | G-REACT(T-443, O-25) → radix→base-ui 12파일·`asChild` 17곳 → T-213 |
| geo | py | ADR-011 | T-483 | 미채택 | T-308·T-440 → health alias 병행·securitySchemes |
| ktc | tokens | ADR-006, ADR-012 ④ | T-453 | 미채택 | T-451(CI 신설)·T-109 → hex fallback·`@config` 제거 |
| ktc | ui | ADR-007 | T-454 | 미채택 | G-LIC(L8, T-021, O-2) → T-453·T-213 |
| ktc | py | ADR-011 | T-485 | 미채택 | T-451·T-310 → features export 계약(map provider 동시 수정) |
| ktdm | tokens | ADR-006, ADR-012 ② | T-472 | 미채택 | T-470(Next 16·React 19·ESLint 9·Node 22) → T-109 |
| ktdm | ui(부분) | ADR-007 | T-473 | 미채택 | G-LIC(L8) → T-472·T-213 |
| ktdm | py | ADR-011 | T-486 | 미채택 | T-471·T-307 → `trust_incoming=False` |
| 전 소비자 | 규칙 문서 | standards | — | 참조 가능 | 없음(G-LIC 면제) |
| 전 소비자 | CI·매니페스트 | ADR-008, ADR-010 | T-403 | 미채택 | T-010·T-011 → Node 22·SHA 핀·report job·매니페스트 커밋 |

## 5. 초기 발견과 처리

| 발견 | 처리 | 확인 경계 |
|---|---|---|
| Python lockfile을 CI·Docker 양쪽에서 `--locked`로 소비하는 곳은 weather뿐(`vm` §2.1) | G-LOCK을 py 채택 gate로 고정; geo·map·ktdm·ktc는 lock 도입 task(T-440·T-410·T-471·T-450) 선행 | lock 존재 ≠ 소비; pinvi `apps/api/uv.lock`은 미소비 상태 |
| Node 20 CI 3곳(ktdm·geo·wx)은 EOL(2026-04-30) | G-NODE, T-403 | floor 22.12 |
| 라이선스 결정이 pinvi 전 트랙과 ktc·ktdm 코드 채택을 막음 | L6·L8을 Phase 0 외부 확인(T-020·T-021)으로 승격; 규칙 참조는 면제 | 사용자 결정(O-1·O-2) 없이는 gate를 닫지 않음 |
| 대비 수치 검증은 map만(`dt` §3.4.2) | G-CONTRAST는 report 기본 + 앱 baseline; 신규 미달만 fail | 초기 baseline 등록은 채택 PR에서 |
| 시각 기준선은 어느 앱도 없음 | G-VIS는 `NOT_RUN`으로 두고 T-402·각 채택 PR evidence에서 닫음 | 저장소 파일이 아닌 PR evidence(D-21) |
| airport Admin 정의(D-20)와 WIP 병합(O-9) | tokens + 소형 부품 범위; 셸·로그인 소비는 T-035 라우트 분리 후 | 사용자 확인 |
| pinvi mobile Tailwind 3 | O-8 사용자 승인 전 `exceptions` 미등록, `WAIT` | 지시 (1) 축소 항목 |

## 6. 갱신 규칙

- §2 gate 정의는 수기이며 규칙 문서·ADR이 바뀔 때만 고친다.
- §3·§4의 상태 셀은 T-012 이후 `tools/collect_manifests.py`가 매니페스트·`check_versions` 결과에서 생성한다. 그 전까지는 채택 PR이 머지될 때 해당 행만 수기로 갱신하고 근거(PR·evidence)를 적는다.
- 상태를 `PASS`로 바꿀 때는 근거 절 또는 PR·CI run을 함께 적는다. 근거 없는 `PASS`는 D-25 위반이다.
- 분기 감사(T-506)에서 조사 기준 커밋을 갱신하면 §1의 비교 기준을 새 절로 추가한다.
