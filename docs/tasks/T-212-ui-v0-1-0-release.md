# T-212 ui `v0.1.0` rc → map + pinvi admin(L6) 또는 airport 검증 → 정식

- 상태: BLOCKED
- 우선순위: P1
- Gate: consumer-smoke
- 선행: T-212a, T-109
- 외부 선행: T-020(pinvi L6, 사용자 O-1) 또는 T-430(airport WIP 병합, 사용자 O-9) 중 하나 완료; 검증 소비자 PR은 해당 앱의 tokens 채택(map T-410·pinvi T-421·airport T-431, 모두 tokens-v0.1.0 = T-109 이후) 위에서만 가능

## 목표

소형 13종만 담은 `@kor-travel/ui` 첫 릴리스를 `-rc.N` → 소비자 PR 검증 → 정식 순서로 발행한다. 정식 조건은 GPL 소비자 map + (pinvi admin 또는 airport) 두 곳에서 rc 설치본으로 CI green. 이 task는 common 측 릴리스 작업이며 소비자 PR 자체는 T-411(map)·T-421→T-422(pinvi)·T-432(airport)가 소유한다.

## 고정 결정

- ADR-005·ADR-010 — [ADR 색인](../adr/README.md). [브리프](../plan/design-brief.md) D-11(태그 `ui-v0.1.0-rc.1`/`ui-v0.1.0`, 자산 `kor-travel-ui-0.1.0.tgz` + `SHA256SUMS`, lock `integrity`, 태그 불변·같은 버전 재발행 금지, tarball에 LICENSE·NOTICE·THIRD_PARTY_NOTICES 동봉), D-16(ui 1차 = map + pinvi admin(L6); L6 미결이면 airport 소형 부품으로 대체), D-18(`-rc.N` → 소비자 PR 검증 → 정식, CHANGELOG 단일 파일 패키지별 H3), D-24(한 PR = 한 산출물, ui 파일 상한 30, revert 1회), D-25(NOT_RUN), D-31(0.x; ui는 호환 tokens 한 minor를 peer(ADR-013); 소비자 범위 `~0.1`).
- 절차 정본: [release](../runbooks/release.md), [consumer-adoption](../runbooks/consumer-adoption.md), [consumer PR 템플릿](../../templates/consumer-pr.md), [adoption-readiness](../architecture/adoption-readiness.md) gate 표.
- 소비자 PR 순서·되돌리기: [판정 보고서](../plan/design-panel/judge-migration-feasibility.md) §3.1 — map PR 2(shim 9 파일 `export * from "@kor-travel/ui/<x>"` + `@source` 1줄; gate e2e 30·vitest 42·`verify:frontend-eslint` lint 대상 집합 갱신; revert), pinvi PR 2(15 shim + `@/lib/admin/cn` → `@kor-travel/ui/cn` 재수출; gate e2e 56·vitest 27·webpack 빌드), airport PR 3(백업·collector 패널에 Alert·StatStrip·SectionCard·EmptyState; gate build·vitest). 앱별 근거: [map 인벤토리](../survey/inventory/kor-travel-map.md) §8-10·§9(exact 핀·ESLint 검증 스크립트), [pinvi 인벤토리](../survey/inventory/pinvi.md) §8-1·§9(webpack 강제·두 UI 스택 경계), [airport 인벤토리](../survey/inventory/kor-travel-airport.md) §8·§9("Admin"의 실체 = 백업 패널; Button은 v0.2에서).
- 릴리스 차단 사실: T-201 base-ui 3건 확인, T-204 ui-contract 확정 — [ui-components](../survey/cross/ui-components.md) §5.4 미확인 목록.

## 구현 범위

[release §2.1](../runbooks/release.md#21-common-후보-보존과-후속-구현)에 따라 보존 후보에서 분기한 release branch의 PR로 준비한다. 아래 버전·lock 변경은 해당 branch에 적용한다. 후속 minor가 있는 main을 과거 버전으로 내리지 않는다. 소비자 단계는 해당 저장소 담당자에게 요청하는 외부 gate이며 미실행이면 BLOCKED/NOT_RUN을 유지한다.

- `packages/ui/package.json` version `0.1.0-rc.1`, peer `@kor-travel/tokens ~0.1.0`; `CHANGELOG.md` `### @kor-travel/ui 0.1.0` 초안(Added 13종, 계약 링크).
- 태그 `ui-v0.1.0-rc.1` + GitHub Release(prerelease) 자산 tgz + `SHA256SUMS`; 소비자 설치 URL과 `integrity` 값을 Release 본문에 기록.
- 소비자 검증 요청: map(T-411)·pinvi(T-422a) 또는 airport(T-432) 브랜치에서 rc URL 설치 → 각 앱 CI green → PR 본문 검사 결과·스크린샷·되돌리기 명령(D-24) 확인.
- `consumer-smoke` 워크플로(T-010, `consumers.pins.json`의 UI 승인 조합: map + pinvi admin(L6 완료) 또는 airport) rc 태그로 dispatch.
- 정식: version `0.1.0`, 태그 `ui-v0.1.0`, 자산·SHA256SUMS 재생성(rc 자산은 유지), CHANGELOG 확정, 소비자 PR은 정식 URL로 lock 갱신 후 머지.
- `docs/integration-map.md`는 `tools/collect_manifests.py`(T-012)로만 갱신(수기 편집 금지, D-19).

## 범위 밖

- 소비자 PR 작성·머지(T-411·T-422·T-432), Button 이후 부품(T-213), npm/PyPI 게시(사용자 범위 제외), tokens 릴리스(T-109), 릴리스 runbook 완주 검증(T-501).

## 예상 변경 파일

예정 경로는 존재·실행 증거가 아니다.

```text
packages/ui/package.json  package-lock.json
CHANGELOG.md
.github/workflows/release.yml  (태그 → build → pack → SHA256SUMS → Release 자산; T-109가 만든 흐름 재사용)
docs/integration-map.md  (생성물)
docs/journal.md  docs/resume.md
```

## 수용 기준

- rc 태그·Release 자산·`SHA256SUMS`가 존재하고 `sha256sum -c`가 통과한다; tarball 안에 `LICENSE`·`NOTICE`·`THIRD_PARTY_NOTICES.md`·`dist/`가 있고 `license` 필드가 `GPL-3.0-or-later`.
- map 검증 PR이 rc 설치본으로 e2e 30·vitest 42·`verify:frontend-eslint` green이고 shim 외 페이지 파일 무변경(diff 파일 수 ≤ 30).
- pinvi admin(L6 완료 시) 또는 airport 검증 PR이 각 gate green; pinvi는 webpack 빌드·`app-shell-mobile` e2e(사용자 표면 무변경) 포함.
- `consumer-smoke` dispatch green(워크플로 미완이면 `NOT_RUN(T-010 미완료)`로 기록하고 DONE 전 해소).
- 정식 태그 후 `npm view`가 아닌 Release URL 설치로 스모크 앱 `next build --webpack`·`next build` 통과, lock `integrity`와 SHA256SUMS를 각각 동일 자산 바이트에 대해 검증(해시 알고리즘이 다르면 문자열 비교 금지).
- CHANGELOG에 `### @kor-travel/ui 0.1.0`·소비자 필수 2줄(`@import`·`@source`)·계약 링크가 있다.

## 검증 명령

릴리스 source 확인·버전 전환·빌드·설치·태그·발행·dispatch는 [release §3.1~3.5](../runbooks/release.md#31-준비)의 단일 절차를 따른다. 패키지는 `ui`, 버전은 `0.1.0-rc.N`/`0.1.0`으로 설정하고 검증한 준비 PR merge commit을 사용한다. source·태그·push·원격 peeled SHA·발행 검증 중 하나라도 실패하면 후속 명령을 중단한다.

아래는 §3.2에서 생성한 자산의 체크섬과 내용 확인이다. 파일 목록을 이 task의 tarball 수용 기준과 대조하며, rc 번호와 정식 버전이 바뀌면 파일명도 실제 산출물에 맞춘다.

```bash
(cd dist/release && sha256sum -c SHA256SUMS) || exit 1
tar -tzf dist/release/kor-travel-ui-0.1.0-rc.1.tgz || exit 1
```

## evidence

`docs/journal.md`와 Release 본문에 태그·자산 sha256·소비자 PR 링크와 각 CI run URL·테스트 수·exit code, `consumer-smoke` run URL을 남긴다. 검증 소비자가 한 곳뿐이면 정식 태그를 만들지 않고 사유를 적는다.

## rollback 또는 release 차단 조건

- rc 자산·태그는 삭제하지 않는다(불변). 문제가 있으면 `-rc.2`로 재발행. 정식 태그 후 결함은 `0.1.1`(additive) 또는 `0.2.0`으로만 고친다.
- 소비자 되돌리기: 소비자 PR `git revert` 1회 + lock 복원(D-24).
- 차단: base-ui 3건 미확인(T-201), ui-contract 미확정(T-204), 검증 소비자 GPL 2곳 미만, 우회 패치(`patches/`·shim 재구현) 발견, tokens-v0.1.0 미발행.
