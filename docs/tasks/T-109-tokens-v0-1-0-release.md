# T-109 tokens `v0.1.0-rc.1` → map·weather 검증 → `tokens-v0.1.0` 정식 + SHA256SUMS

- 상태: BLOCKED
- 우선순위: P1
- Gate: consumer-smoke
- 선행: T-101, T-102, T-103, T-104

## 목표

토큰 패키지의 첫 릴리스를 D-11 채널(GitHub Release 자산 tarball + `SHA256SUMS`)로 발행한다. `tokens-v0.1.0-rc.1`을 map admin·weather admin의 draft PR에서 값 무변경(6폭 diff 0)으로 검증한 뒤 `tokens-v0.1.0` 정식 태그를 만든다. 정식 태그 이후 T-410·T-461이 소비자 PR을 merge한다.

## 고정 결정

- [설계 브리프](../plan/design-brief.md) D-11(태그 `tokens-vX.Y.Z`·자산 `kor-travel-tokens-X.Y.Z.tgz` + `SHA256SUMS`·lock `integrity`·태그 불변·재발행 금지·`@main` 금지·고지 동봉), D-31(0.x·`-rc` + 소비자 PR 검증 + CHANGELOG), D-16(tokens 1차 map + weather), D-24(이관 PR 규격·파일 상한 tokens 10), D-25(`NOT_RUN`), D-21(6폭 evidence), D-18(`consumer-smoke`).
- ADR-005·ADR-010 — [docs/adr/README.md](../adr/README.md). 절차 정본은 [release runbook](../runbooks/release.md)·[consumer-adoption runbook](../runbooks/consumer-adoption.md)(T-007).
- 소비자 PR 순서·gate는 [판정 보고서](../plan/design-panel/judge-migration-feasibility.md) §3.1 map PR 1(6폭 diff 0·e2e 30·vitest 42·revert + lock 복원)·weather PR 1(6폭 diff 0 수동·font 스택 오버라이드).
- 근거: [map 인벤토리](../survey/inventory/kor-travel-map.md) §3.1·§9(exact 핀·`verify:*` 스크립트·Playwright 1.60), [weather 인벤토리](../survey/inventory/kor-travel-weather.md) §3.1·§8 항목 1·§9(폰트 미로딩·`moduleResolution: node`), [백엔드 조사](../survey/cross/backend.md) §5.2 후보 D(릴리스 자산 + sha256).
- 패키지명이 O-5로 개명됐다면(T-006) 자산 이름도 `kor-travel-tokens-…`를 유지하되 `package.json` `name`만 바뀐다.

## 구현 범위

1. rc 발행: `packages/tokens` `version 0.1.0-rc.1`, `npm pack` 산출 `kor-travel-tokens-0.1.0-rc.1.tgz`, `sha256sum` → `SHA256SUMS`, 태그 `tokens-v0.1.0-rc.1`(annotated), GitHub pre-release에 자산 2개 첨부. tarball 안 `LICENSE`·`NOTICE`·`THIRD_PARTY_NOTICES.md` 확인.
2. map 검증(draft PR, 저장소 kor-travel-map, 브랜치 `agent/<agent>-T-410`, 경로 `packages/kor-travel-map-admin/frontend`): `npm install <release tarball URL>` → lock `integrity` 커밋 → `globals.css`에 `@import "@kor-travel/tokens/theme.css"` + 빈 brand 오버라이드 → 6폭 기준선 diff 0·e2e 30·vitest 42·`verify:*` 통과. 되돌리기 `git revert` 1회 + lock 복원. 파일 수 ≤10.
3. weather 검증(draft PR, kor-travel-weather, `agent/<agent>-T-461`, `packages/kor-travel-weather-admin/frontend`): `app/tokens.css` → 패키지 `tokens.css` + `aliases/map-vocabulary.css` + navy·`--rail`·font 오버라이드 → 6폭 수동 diff 0(Playwright 없음 → T-108 템플릿). 되돌리기 동일.
4. `consumer-smoke` dispatch 실행(map admin·pinvi web pinned SHA에 rc tarball 설치 → `type-check` + `next build` webpack·Turbopack) green.
5. 정식: `version 0.1.0`, 태그 `tokens-v0.1.0`, 자산 재생성·`SHA256SUMS`, `CHANGELOG.md` `## [0.1.0] ### tokens`(Breaking 없음), `docs/architecture/adoption-readiness.md`·`docs/integration-map.md` 갱신(T-012 도구가 있으면 도구로). 두 draft PR은 정식 URL로 갱신 후 T-410·T-461에서 merge.

## 범위 밖

- 소비자 PR merge 자체(T-410·T-461), pinvi admin·airport tokens 채택(T-421·T-431), ui 릴리스(T-212), 공개 npm 게시(T-507), 릴리스 runbook 완주 리허설(T-501).

## 예상 변경 파일

예정 경로는 존재·실행 증거가 아니다. `packages/tokens/package.json`(version), `package-lock.json`, `CHANGELOG.md`, `docs/architecture/adoption-readiness.md`, `docs/integration-map.md`, `docs/journal.md`; 외부: kor-travel-map·kor-travel-weather draft PR(각 ≤10 파일).

## 수용 기준

- 태그 `tokens-v0.1.0-rc.1`·`tokens-v0.1.0`이 존재하고 각 Release에 tarball + `SHA256SUMS`가 있으며 `sha256sum -c` 통과. 같은 버전 재발행·태그 이동 없음.
- 두 tarball 모두 고지 3파일·CSS 7종·`aliases/map-vocabulary.css`·`tokens.json`·`dist/index.d.ts` 포함(T-101 스모크와 동일 검사).
- map draft PR evidence: `npm ls @kor-travel/tokens` = rc 버전, lock `integrity` 존재, 6폭 diff 0 스크린샷, e2e 30 pass·vitest 42 pass(수치는 실행 출력), 변경 파일 ≤10.
- weather draft PR evidence: 6폭 수동 diff 0(스크린샷), 변경 파일 ≤10, 폰트 스택 오버라이드 포함. 실행하지 못한 항목은 `NOT_RUN(사유)`로 적고 `DONE` 전 `외부 선행`으로 승격.
- `consumer-smoke` 실행 링크 green(webpack·Turbopack 양쪽).
- `CHANGELOG.md`에 `### tokens` 0.1.0 항목, `@main` 참조 0건.

## 검증 명령

```bash
npm version 0.1.0-rc.1 --workspace packages/tokens --no-git-tag-version
npm pack --workspace packages/tokens --pack-destination dist-release && (cd dist-release && sha256sum *.tgz > SHA256SUMS && sha256sum -c SHA256SUMS)
tar -tzf dist-release/kor-travel-tokens-0.1.0-rc.1.tgz | grep -E "LICENSE|NOTICE|THIRD_PARTY|aliases/map-vocabulary.css|tokens.json|index.d.ts"
git tag -a tokens-v0.1.0-rc.1 -m "tokens 0.1.0-rc.1" && git tag -v tokens-v0.1.0-rc.1 || git show tokens-v0.1.0-rc.1 --no-patch
gh release create tokens-v0.1.0-rc.1 dist-release/*.tgz dist-release/SHA256SUMS --prerelease --title "tokens 0.1.0-rc.1"
gh workflow run consumer-smoke.yml -f tarball_url=<release asset url>
```

Git Bash에서 동일. 소비자 저장소 명령(`npm install <url>`, `npm run e2e`, `npm test`)은 각 저장소의 `AGENTS.md`를 따른다.

## evidence

- Release URL·자산 sha256·`consumer-smoke` 실행 링크·map/weather draft PR 링크와 검사 수치를 이 절·`docs/journal.md`·`docs/resume.md`에 남긴다.

## rollback 또는 release 차단 조건

- rc 검증 실패 → 원인 수정 후 `-rc.2`(같은 버전 재발행 금지, 태그 삭제 금지). 정식 태그 후 결함 → `0.1.1` patch 발행; 소비자는 `git revert` 1회 + lock 복원.
- 차단: 시각 diff가 원인 불명으로 남음(D-08 중단 조건), tarball 고지 누락, `SHA256SUMS` 불일치, `consumer-smoke` red, map draft PR 파일 수 >10, `kt_contrast` map 기본값 실패.
