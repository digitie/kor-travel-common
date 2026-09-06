# T-410 map: `globals.css` → `@import "@kor-travel/tokens"` + 빈 brand 오버라이드 + 매니페스트(값 diff 0) + LICENSE 전문 복원(L9)·`license` 필드

- 상태: BLOCKED
- 우선순위: P0
- Gate: e2e 30·vitest 42·시각 diff
- 선행: T-109

## 목표

kor-travel-map admin 프론트가 `@kor-travel/tokens` v0.1.0의 첫 소비자가 된다. map 값이 곧 `tokens.css` 정본(D-12)이므로 이 PR은 렌더 값이 바이트 단위로 바뀌지 않음을 6폭 스크린샷과 e2e·vitest로 증명하는 것이 전부다. 부수로 L9(루트 `LICENSE` 25행 요약본 → GPL 전문)·L11(`license` 필드)을 비차단 별도 PR로 처리한다.

## 고정 결정

- [design-brief](../plan/design-brief.md) D-10(소비자 필수 2줄, `kt-` 유틸리티 무충돌)·D-12(`--kt-*`, shadcn alias 의미 고정, `.dark` 완비)·D-16(tokens 1차 = map + weather)·D-19(매니페스트)·D-21(6폭 기준선)·D-24(한 PR = 한 산출물, tokens PR 파일 상한 10)·D-25(NOT_RUN).
- ADR-006·ADR-010 — [ADR 색인](../adr/README.md). 정본: [design-tokens](../standards/design-tokens.md), [consumer-adoption runbook](../runbooks/consumer-adoption.md), [consumer PR 템플릿](../../templates/consumer-pr.md), [licensing](../standards/licensing.md).
- PR 순서: [judge-migration-feasibility §3.1 map #1·#5](../plan/design-panel/judge-migration-feasibility.md). 앱 사실: [inv/map §8-1·§9](../survey/inventory/kor-travel-map.md)(`globals.css`가 토큰 파일, hairline 2종 `--border`/`--control-line`, `.dark` 정의만·토글 없음, `@custom-variant dark`), [lic §2.2 D1·§3.7 L9·L11](../survey/cross/licensing.md).

## 구현 범위

- `packages/kor-travel-map-admin/frontend/src/app/globals.css`: 자체 `:root`/`.dark`/`@theme inline` 토큰 블록을 `@import "@kor-travel/tokens/tokens.css"; @import "@kor-travel/tokens/theme.css"; @import "@kor-travel/tokens/shadcn.css"; @import "@kor-travel/tokens/dark-class.css";`로 교체. `@custom-variant dark (&:is(.dark *))`와 `@layer base` focus·reduced-motion 레시피는 앱 파일에 유지.
- `src/app/brand.css`(신규, 빈 오버라이드 블록 + 주석 "map 값 = 정본, 오버라이드 없음")를 import.
- `package.json`에 `@kor-travel/tokens` 0.1.0(GitHub Release tarball URL + lock `integrity`, D-11)·`license: "GPL-3.0-or-later"` 추가, `package-lock.json` 동반 커밋. `allowScripts`·`overrides`는 무변경.
- `packages/kor-travel-map-admin/frontend/kor-travel-common.lock.json`에 `tokens{version:"0.1.0", override:"src/app/brand.css"}` 기록(매니페스트가 T-403에서 이미 커밋됐으면 갱신).
- 별도 비차단 PR: 루트 `LICENSE` GPL-3.0 전문 복원 + 기존 25행의 저작권 고지는 `NOTICE`로 이동.

## 범위 밖

UI 컴포넌트 shim(T-411·T-412), Next/base-ui/Playwright 상향(T-413), 다크 토글 도입, `--kt-*` 이름으로 앱 코드 치환(앱 코드는 shadcn alias·기존 유틸리티를 그대로 쓴다), `verify-*.mjs` 상수 변경.

## 대상 저장소·브랜치·PR·되돌리기

- 저장소 `digitie/kor-travel-map`, 작업 위치 WSL(`/mnt/f/dev/kor-travel-map-<agent>`, map 정본 환경 — [inv/map §3.1](../survey/inventory/kor-travel-map.md)). 브랜치 `agent/<agent>-T-410-tokens`(map 로컬 규칙 `feat|chore/<topic>`를 요구하면 `chore/T-410-tokens`), `origin/main`에서 분기.
- PR 2개: (1) tokens 채택(≤10 파일), (2) LICENSE·`license` 필드(docs). 되돌리기 = `git revert <merge-sha>` + `npm ci`로 lock 복원; brand.css는 revert에 포함된다.

## 예상 변경 파일

아래는 이 task가 만들거나 고칠 예정 경로다. 예정 경로는 존재·실행 증거가 아니다.

```text
packages/kor-travel-map-admin/frontend/src/app/globals.css
packages/kor-travel-map-admin/frontend/src/app/brand.css
packages/kor-travel-map-admin/frontend/package.json
package-lock.json
packages/kor-travel-map-admin/frontend/kor-travel-common.lock.json
.github/workflows/frontend.yml                       # versions-check job(T-403 미반영 시)
LICENSE, NOTICE                                      # 별도 PR
```

## 수용 기준

- [ ] 착수 전 6폭(320/375/414/768/1024/1440) 기준선과 완료 후 캡처의 픽셀 diff가 0이다(대표 페이지 4종 이상). diff가 있으면 원인을 토큰 값·cascade 순서 중 하나로 특정하고, 특정 못 하면 revert(D-08 중단 조건).
- [ ] Playwright mocked suite 30 spec·vitest 42 파일이 모두 통과하고 0 test/skip을 통과로 집계하지 않았다.
- [ ] `npm run verify:npm-tree`·`audit:high`·`verify:frontend-eslint`·`type-check`·`next build`(webpack·Turbopack 양쪽, D-10)가 green이다.
- [ ] 빌드 산출 CSS에 `--kt-*` 정의가 존재하고 map 원래 값과 동일하다(`grep -o '\-\-kt-[a-z-]*: *[^;]*'` 대조표 첨부).
- [ ] `check_versions` report에서 map 행이 `OK` 또는 등록된 `EXEMPT`만 보인다.
- [ ] 별도 PR: `LICENSE`가 674행 GPL-3.0 전문이고 `package.json` `license` 필드가 있다.

## 검증 명령

```bash
# kor-travel-map(WSL)
npx --yes npm@12.0.1 ci --workspaces --include=optional --no-audit --no-fund
npm run verify:npm-tree && npm run audit:high && npm run verify:frontend-eslint
npm run type-check -w packages/kor-travel-map-admin/frontend
npm test -w packages/kor-travel-map-admin/frontend                 # vitest 42 파일
npx playwright test -c packages/kor-travel-map-admin/frontend/playwright.config.ts   # mocked 30 spec
npm run build -w packages/kor-travel-map-admin/frontend && npx next build --turbopack   # 양쪽 빌드
# kor-travel-common
python3 -B -X utf8 tools/check_versions.py --manifest ../kor-travel-map/packages/kor-travel-map-admin/frontend/kor-travel-common.lock.json
python3 -B -X utf8 tools/kt_contrast.py --app map
```

## evidence

PR 본문(6폭 diff 캡처·명령 출력·되돌리기 명령), `consumers.pins.json` 머지 SHA 갱신, `docs/integration-map.md` 재생성, `docs/journal.md` 1항목, 이 파일 "실행 기록"(도구 버전·테스트 수·exit code). 미실행은 `NOT_RUN(사유)`.

## rollback·release 차단 조건

- 원인 불명 시각 diff·e2e red·`verify:npm-tree` 실패 중 하나라도 있으면 머지 금지, 머지 후 발견 시 `git revert` 1회.
- 이 PR이 머지되기 전에는 T-109의 `tokens-v0.1.0` 정식 태그를 "첫 소비자 검증 완료"로 표기하지 않는다(rc 상태 유지).
