# 통합 지도(integration map)

- 정본 지위: 소비자별 채택 버전·매니페스트·워크플로·강제 수준의 지도. **T-012 이후 `tools/collect_manifests.py`가 `consumers.pins.json`과 각 소비자 `kor-travel-common.lock.json`에서 생성하는 생성물로 전환되며 그 뒤에는 수기 편집을 금지한다(D-19).** 전환 전까지는 이 초기판(수기, 전 셀 "미채택")이 자리표시자다. 확정 task: T-008(설계 초기판)·T-011·T-012. 마지막 갱신: 2026-09-06.
- 근거: [브리프](plan/design-brief.md) D-07·D-16·D-19·D-30, [소비자](architecture/consumers.md), [채택 준비 기준](architecture/adoption-readiness.md).

이 문서는 [문서 지도](README.md)에 속하며 "지금 어느 소비자가 common의 무엇을 어느 버전으로 쓰는가"만 답한다. 왜·어떤 순서로 채택하는가는 [소비자](architecture/consumers.md), gate는 [채택 준비 기준](architecture/adoption-readiness.md), 규칙은 [standards](standards/README.md)가 정본이다.

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
