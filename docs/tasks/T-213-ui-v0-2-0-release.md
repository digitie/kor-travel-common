# T-213 ui `v0.2.0`(Button·overlay·Table·DataTable·Pager·Copy/Json/Detail·Header/Form) rc → 정식

- 상태: BLOCKED
- 우선순위: P1
- Gate: consumer-smoke·2인 리뷰
- 선행: T-208, T-209, T-210
- 외부 선행: 검증 소비자 PR은 해당 앱의 ui v0.1 채택(map T-411과 두 번째 소비자 pinvi T-422a 또는 airport T-432)과 `@base-ui/react` ≥ floor 설치 위에서만 가능; pinvi는 L6(O-1), airport는 WIP 병합(O-9)에 묶임

## 목표

v0.2.0은 T-205~T-210의 2차 부품 전부를 담는 첫 minor이며, 0.x 규칙상 v0.1 계약의 파괴 변경이 허용되는 대신 CHANGELOG `Breaking` 절 + 이관 절이 필수다. 정식 조건은 map(ui v0.2 PR) + pinvi admin(또는 airport Button) 검증 green과 2인 리뷰 PASS. v0.2 이후에야 weather 셸·패널·폼 3분할(T-463)과 geo radix→base-ui(T-444)가 시작된다.

## 고정 결정

- ADR-005·ADR-010 — [ADR 색인](../adr/README.md). [브리프](../plan/design-brief.md) D-11(태그 `ui-v0.2.0-rc.N`/`ui-v0.2.0`, 자산·SHA256SUMS·불변), D-18(rc → 소비자 PR → 정식; CHANGELOG H3), D-24(ui 파일 상한 30, 초과 시 분할 — map v0.2 PR은 Checkbox 호출부 3파일 포함), D-31(minor = 파괴 허용 + `-rc` + 소비자 PR 검증 + CHANGELOG `Breaking` 절 + 이관 절; 토큰·data-slot·prop 기본값·정렬 모드 폐기는 1 minor alias), D-04(비면제: `packages/*` 공개 API → full gate 2인 리뷰).
- 절차 정본: [release](../runbooks/release.md), [consumer-adoption](../runbooks/consumer-adoption.md), [consumer PR 템플릿](../../templates/consumer-pr.md), [ui-contract](../standards/ui-contract.md)(v0.2 계약 갱신은 T-204 절차 반복), [리뷰 아카이브](../reviews/README.md).
- 소비자 PR 순서·gate: [판정 보고서](../plan/design-panel/judge-migration-feasibility.md) §3.1 — map PR 3(Button·overlay·Table·DataTable·Pager shim, Checkbox 호출부 3파일 시그니처, `data-table.test.tsx` 175행 이관; e2e 30·vitest 42), pinvi PR 3(overlay `hasUnsavedInput`·`viewportProps` 흡수 확인, Table·DataTable shim, `AdminTable` 어댑터 유지 + `manualSorting={false}` 명시; e2e 5파일 testid 계약·44px 단언), airport(소형 ui PR에 Button 추가). 근거: [map 인벤토리](../survey/inventory/kor-travel-map.md) §3.1(`"use no memo"` 2곳 단언 — shim 후 map 스크립트 갱신은 T-412 책임)·§9, [pinvi 인벤토리](../survey/inventory/pinvi.md) §8-3·§9(테스트 규모 e2e 56·vitest 27), [ui-components](../survey/cross/ui-components.md) §3.3 회귀 위험 표.

## 구현 범위

- `packages/ui/package.json` version `0.2.0-rc.1`; peer 확정(`@kor-travel/tokens ~0.1.0`([ADR-013](../adr/013-package-release-execution-contract.md)), `@base-ui/react ^1.6.0`, optional `@tanstack/react-table ^8.21.0`·`@tanstack/react-virtual ^3.14.0`), `exports` 전체 목록 검토(deep import 없음).
- `CHANGELOG.md` `### @kor-travel/ui 0.2.0`: Added(부품 목록), `Breaking` 절([release](../runbooks/release.md) 형식; v0.1 대비 data-slot·prop·testid 변경 목록 — 없으면 "없음" 명시), 이관 절(map·pinvi shim 예, Checkbox `onCheckedChange(boolean)` 시그니처, 선택 열 셀렉터 `[data-slot=checkbox]`).
- ui-contract v0.2 절 확정(T-204 절차: grep 대조 + 2인 리뷰), 리뷰 report `docs/reviews/adversarial/YYYY-MM-DD-ui-v0-2-0.md`.
- rc 태그·Release 자산·`consumer-smoke` dispatch → map T-412·pinvi T-422b(또는 airport의 별도 0.2 검증 PR) 검증 → 정식 태그.
- 스모크 앱에 v0.2 전 부품 페이지(overlay·table·detail·header) 포함, webpack·Turbopack 빌드.

## 범위 밖

- 소비자 PR 작성·머지(T-412·T-422·T-432), weather 3분할(T-463)·geo 이관(T-444)·ktdm 부분 채택(T-473), 레지스트리 채널(T-211; 별도 릴리스 가능), 보류 항목 재평가(T-508), 1.0 판단.

## 예상 변경 파일

예정 경로는 존재·실행 증거가 아니다.

```text
packages/ui/package.json  package-lock.json
CHANGELOG.md
docs/standards/ui-contract.md  (v0.2 절)
docs/reviews/adversarial/YYYY-MM-DD-ui-v0-2-0.md  + evidence/…-reviewer-{a,b}.md
docs/reviews/README.md
packages/ui/smoke/next-app/app/**
docs/integration-map.md  (생성물)  docs/journal.md  docs/resume.md
```

## 수용 기준

- rc 태그·자산·`SHA256SUMS` 존재, `sha256sum -c` 통과, tarball 라이선스 파일 3종 동봉.
- v0.1 대비 공개 API diff(`exports`·d.ts·data-slot·testid·prop 기본값)가 표로 정리되고 CHANGELOG `Breaking` 절과 1:1 대응한다; 폐기 항목은 alias가 1 minor 동안 남는다.
- map v0.2 검증 PR: e2e 30·vitest 42 green, `data-table.test.tsx` 이관본 통과, `manualSorting` 기본값 무변경으로 페이지 파일 무변경.
- pinvi 검증 PR(L6 완료 시): `AdminTable` 어댑터 유지 상태에서 e2e 5파일 testid 계약·44px 단언 green, webpack 빌드; 미완이면 airport Button PR green으로 대체하고 사유 기록.
- 2인 리뷰 verdict `PASS`(P0/P1 0), `consumer-smoke` green(미완이면 `NOT_RUN` + DONE 전 해소).
- base-ui 1.6.0·1.8.0 매트릭스(T-206)와 TanStack peer 미설치 시 `./data-table` 외 subpath가 정상 import되는 스모크 통과.

## 검증 명령

```bash
npm run build -w packages/ui && npm run test -w packages/ui && npx tsc --noEmit -p packages/ui
node packages/ui/scripts/check-directives.mjs && node packages/ui/scripts/check-kt-classes.mjs && node packages/ui/scripts/check-contract-doc.mjs
npm pack -w packages/ui --pack-destination dist/release && (cd dist/release && sha256sum kor-travel-ui-0.2.0-rc.1.tgz > SHA256SUMS)
git tag -a ui-v0.2.0-rc.1 -m "ui 0.2.0-rc.1" && git push origin ui-v0.2.0-rc.1
gh release create ui-v0.2.0-rc.1 --prerelease dist/release/kor-travel-ui-0.2.0-rc.1.tgz dist/release/SHA256SUMS
gh workflow run consumer-smoke.yml -f tag=ui-v0.2.0-rc.1
python3 -B -X utf8 tools/validate_document_links.py
```

## evidence

`docs/journal.md`·Release 본문에 태그·sha256·소비자 PR 링크·CI run URL·테스트 수·exit code, 리뷰 report 경로, API diff 표를 남긴다. 실행 못 한 소비자 검증은 `NOT_RUN(사유)`.

## rollback 또는 release 차단 조건

- rc·정식 태그와 자산은 불변; 결함은 `0.2.1`(additive) 또는 `0.3.0`으로만. 소비자는 PR `git revert` 1회 + lock 복원(D-24)로 v0.1로 돌아간다.
- 차단: 리뷰 P0/P1 미해결, `Breaking` 절 누락 상태의 계약 변경, map 검증 PR에서 페이지 파일 수정 필요(호출부 전수 수정 회피 원칙 위반), 우회 패치 발견(`tools/ui_drift.py`가 있으면 실행), GPL 검증 소비자 2곳 미만.
