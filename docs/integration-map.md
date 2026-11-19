# 통합 지도(integration map)

- 정본 지위: 소비자별 채택 버전·매니페스트·워크플로·강제 수준의 지도. **T-012 이후 `tools/collect_manifests.py`가 `consumers.pins.json`과 각 소비자 `kor-travel-common.lock.json`에서 생성하는 생성물로 전환되며 그 뒤에는 수기 편집을 금지한다(D-19).** 전환 전까지는 이 초기판(수기, 전 셀 "미채택")이 자리표시자다. 확정 task: T-008(설계 초기판)·T-011·T-012. 마지막 갱신: 2026-09-06.
- 근거: [브리프](plan/design-brief.md) D-07·D-16·D-19·D-30, [소비자](architecture/consumers.md), [채택 준비 기준](architecture/adoption-readiness.md).

이 문서는 [문서 지도](README.md)에 속하며 "지금 어느 소비자가 common의 무엇을 어느 버전으로 쓰는가"만 답한다. 왜·어떤 순서로 채택하는가는 [소비자](architecture/consumers.md), gate는 [채택 준비 기준](architecture/adoption-readiness.md), 규칙은 [standards](standards/README.md)가 정본이다.

현재 실제수용은 [§5 불변 산출물 채택과 운영 수용](#5-불변-산출물-채택과-운영-수용2026-11-19)에 기록한다. 초기판은 당시 조사 기록이다.

## 1. 생성 규칙(T-012)

| 입력 | 출력 열 | 비고 |
|---|---|---|
| `consumers.pins.json`(`role`·`url`·`revision`) | 저장소·기준 커밋 | consumer-smoke가 쓰는 pinned SHA와 동일 파일 |
| 소비자 `kor-travel-common.lock.json`(`consumer-manifest.v1`) | `tokens.version`·`tokens.override`·`ui.version`·`python.version`·`lockfiles[]`·`contrast`·`ux_gate`·`openapi.exceptions`·`exceptions[]` | 매니페스트에 `enforce`는 없다(common `versions.json` 소유) |
| `versions.json` `consumers.<repo>.enforce` | 강제 수준 | `report`/`warn`/`fail`; 승격은 common PR |
| `tools/check_versions.py` 최근 report | 판정 요약(위반 수·`EXEMPT` 수) | JSON 출력 |
| 소비자 워크플로의 `uses: digitie/kor-travel-common/...@<ref>` | 재사용 워크플로 채택 여부·ref | `@main`은 `FLOATING_REF`로 표시 |

생성물 머리에는 생성 시각·common 커밋·입력 파일 해시를 넣는다. 수기 수정이 필요하면 입력 파일(매니페스트·`versions.json`)을 고치고 다시 생성한다.

## 2. 채택 지도(초기판, 2026-09-06)

기준 커밋은 조사 기준(`docs/survey/README.md` §2.1)이며 `consumers.pins.json`이 생기면 그 값으로 대체된다.

| 저장소 | 앱·표면 | 기준 커밋 | tokens | ui | python | 규칙 문서 | 매니페스트 | 재사용 워크플로 | enforce |
|---|---|---|---|---|---|---|---|---|---|
| kor-travel-map | admin | `c494e227` | 미채택 | 미채택 | 미채택 | 참조 가능 | 없음 | 없음 | report |
| kor-travel-map | api | `c494e227` | — | — | 미채택 | 참조 가능 | 없음 | 없음 | report |
| kor-travel-map | dagster | `c494e227` | — | — | 미채택 | 참조 가능 | 없음 | 없음 | report |
| kor-travel-weather | admin | `6003da9` | 미채택 | 미채택 | — | 참조 가능 | 없음 | 없음 | report |
| kor-travel-weather | api | `6003da9` | — | — | 미채택 | 참조 가능 | 없음 | 없음 | report |
| kor-travel-airport | admin(백업·collector 패널) | `2bb1111`(WIP `99b3f98`) | 미채택 | 미채택 | — | 참조 가능 | 없음 | 없음 | report |
| kor-travel-airport | api | `2bb1111` | — | — | 미채택 | 참조 가능 | 없음 | 없음 | report |
| kor-travel-geo | ui | `1d9d74d` | 미채택 | 미채택(React 18) | — | 참조 가능 | 없음 | 없음 | report |
| kor-travel-geo | api·dagster | `1d9d74d` | — | — | 미채택 | 참조 가능 | 없음 | 없음 | report |
| kor-travel-concierge | frontend | `7945305` | 미채택 | 미채택(L8 대기) | — | 참조 가능(L8 전 이것까지) | 없음 | 없음(CI 없음) | report |
| kor-travel-concierge | backend | `7945305` | — | — | 미채택(L8 대기) | 참조 가능 | 없음 | 없음 | report |
| kor-travel-docker-manager | frontend | `862562d` | 미채택 | 미채택(React 18·L8 대기) | — | 참조 가능(L8 전 이것까지) | 없음 | 없음 | report |
| kor-travel-docker-manager | backend | `862562d` | — | — | 미채택(L8 대기) | 참조 가능 | 없음 | 없음 | report |
| pinvi | apps/web admin | `9af25e5` | 미채택(L6 대기) | 미채택(L6 대기) | — | 참조 가능(L6 전 이것까지) | 없음 | 없음 | report |
| pinvi | apps/web 사용자 | `9af25e5` | — (규칙만) | — | — | consumer 프로필 | 없음 | 없음 | report |
| pinvi | apps/mobile | `9af25e5` | — (O-8 대기) | — | — | consumer 프로필 | 없음 | 없음 | report |
| pinvi | apps/api·apps/etl | `9af25e5` | — | — | 미채택(L6 대기) | 참조 가능 | 없음 | 없음 | report |

범례: `미채택` = 매니페스트 없음 또는 해당 버전 필드 없음 · `—` = 해당 배포 단위가 이 표면에 적용되지 않음 · `참조 가능` = 코드 링크 없이 규칙 문서를 따를 수 있음(라이선스 gate 면제) · `없음` = 파일·호출 미확인.

## 3. 열림

| # | 항목 | 기본값 |
|---|---|---|
| O-1 | pinvi 라이선스·공개(L6) | 공개 + GPL-3.0-or-later; 전까지 pinvi 행은 "대기" |
| O-2 | ktc·ktdm GPL 정렬(L8) | GPL 정렬; 전까지 규칙 참조까지만 |
| O-8 | pinvi mobile Tailwind 3 | 사용자 승인 대기; `exceptions` 미등록 |
| O-15 | common 공개·cross-repo 워크플로 호출 | 공개 전제 + 체크아웃 fallback |

## 4. 결정 기록(수기)

| 날짜 | 저장소 | 결정 | 근거 |
|---|---|---|---|
| 2026-11-17 | kor-travel-map | 정확 Node/npm 핀 채택. Node 26.13.1(최신 LTS 26의 최신 patch), npm 12.0.1(공통 축). guard 호출은 공통 축이 26.13.1인 커밋(T-029) 뒤에 올린다(T-417). 그 전까지 `55a921b` | [T-416](tasks/T-416-map-exact-node-npm-pin-decision.md), Map ADR-124(Map PR, 병합 전) |
| 2026-11-17 | 전체 소비자 | guard는 정책과 Node/npm 축을 호출자의 `common-ref`에서 읽는다(구현 T-024 전까지 옛 동작) | [ADR-019](adr/019-frontend-policy-guard-model.md) |
| 2026-11-18 | 전체 소비자 | 공통 Node 축 26.13.1(T-029). 병합 커밋 `0dec9543c8c8730ce7b05837f2fbe6c31d4ede65`. 이 커밋으로 호출 SHA와 `common-ref`를 올리는 소비자는 같은 PR에서 `.nvmrc`(·`.node-version`)·정확 `engines.node`·CI Node·모든 Node `FROM`(`node:26.13.1-<배포판>@sha256:…`)을 26.13.1로 옮긴다. npm 12.0.1 그대로. Map은 T-417에서 이 커밋으로 옮긴다 | [T-029](tasks/T-029-node-axis-to-latest-lts.md), [evidence](evidence/t029-node-axis.md) |
| 2026-11-18 | 전체 소비자 | ADR-019 판 guard 구현. 호출 SHA와 `common-ref`를 T-024 채택 커밋 `e18d1892dcc3915a5e6e57ccad550a852b793780`으로 함께 올린 소비자만 새 동작을 얻고, 옛 판 호출자는 그대로다. 지연은 주간 보고 | [T-024](tasks/T-024-guard-model-implementation.md), [evidence](evidence/t024-guard-model.md) |
| 2026-11-18 | kor-travel-map | guard 호출 SHA와 `common-ref`를 `55a921b` → `0dec9543c8c8730ce7b05837f2fbe6c31d4ede65`(T-029)로 함께 올림, 도구 규칙 입력(`toolchain-manifests`·`node-dockerfiles`) 채움. map은 새 guard(ADR-019)로 옮겼다 | [T-417](tasks/T-417-map-guard-ref-toolchain.md), map PR #1511(`7dc2af7`) |

## 5. 불변 산출물 채택과 운영 수용(2026-11-19)

실제 source·이미지·검증 결과는 [불변 산출물·실제 수용 기록](evidence/releases/2026-11-19-consumer-library-adoption.md)과 [비민감 증거 JSON](evidence/releases/2026-11-19-consumer-library-adoption.json)에 기록한다. 초기판·이전 정본의 수용과 새 정본 후속을 구분한다. T-012 생성기나 root consumers.pins.json의 고정 smoke fixture를 이번 runtime 관측 때문에 바꾸지 않는다.

선택한 producer는 `0e2a3f5aa16323df0d009360802661c9bc496dc6`, guard/catalog pin은 `d644632ea9eaf2f6b6baa49305d65fae5bbc0bd4`다. UI0.2.3·tokens0.1.4와 실제 사용하는 Geo Toast0.1.3의 동일 pack bytes/SRI를 소비한다. canonical 파일 수는 UI+tokens121, Geo+toast129, 모바일 tokens25다. 각 앱의 새 source·설치·이미지·화면 수용은 후속 기록에 결박하며 미완료를 완료로 합산하지 않는다.

Manager의 PR619는 이 정본을 채택했으며 frontend가 바뀌었다. 따라서 기존617 frontend tree 보존 증거로 최신 Manager 화면을 수용하지 않는다. Geo·Weather·Transport·Pinvi·Concierge도 같은 정본으로 맞춘다. Map은 별도 Claude 소유라 이 작업의 코드·CI·빌드·배포 변경 대상에서 제외한다. CI 순서 감사·최적화는 마지막에 수행한다.
