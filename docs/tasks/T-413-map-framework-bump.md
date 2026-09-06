# T-413 map: Next 16.3·base-ui 1.8·Playwright 1.63 상향(`verify-next-sharp.mjs`·`test_frontend_dependency_security.py`·이미지 동반, 별도 PR)

- 상태: BLOCKED
- 우선순위: P2
- Gate: 전 CI
- 선행: T-005

## 목표

map의 exact 핀 3종을 `versions.json` recommended로 올린다: `next` 16.2.12 → 16.3.4, `@base-ui/react` 1.6 → 1.8.0, `@playwright/test` 1.60.0 → 1.63.x(+ Playwright 컨테이너 이미지 digest). map은 상수 잠금 스크립트와 pytest가 버전을 결박하므로 lock·상수·테스트·이미지를 한 PR에 동반하지 않으면 CI가 red가 된다. common 채택 PR(T-410~412)과는 분리한다.

## 고정 결정

- [design-brief](../plan/design-brief.md) D-06(Next 16.3.4·base-ui 1.8.0·Playwright 1.63.x recommended; map `16.2.12` exact·Playwright 1.60 exact는 예외 등록)·D-07(정확 핀 허용, lock 의무)·D-24(프레임워크 업그레이드 PR과 채택 PR 분리).
- ADR-008 — [ADR 색인](../adr/README.md). 정본: [versions](../standards/versions.md), [frontend-stack](../standards/frontend-stack.md).
- 앱 사실: `next` exact + 루트 `overrides`(postcss 8.5.23, sharp 0.35.3) + `verify-next-sharp.mjs` ABI 스모크 + `tests/unit/test_frontend_dependency_security.py`가 Dockerfile/CI 명령 순서까지 잠금; Playwright 이미지 `mcr.microsoft.com/playwright:v1.60.0-noble@sha256:…` — [inv/map §3.1·§8-23·§9](../survey/inventory/kor-travel-map.md), [vm §3.6·§5.2](../survey/cross/version-matrix.md).
- PR 순서: [judge-migration-feasibility §3.1 map "별도"](../plan/design-panel/judge-migration-feasibility.md).

## 구현 범위

- `packages/kor-travel-map-admin/frontend/package.json`·루트 `package.json` overrides(sharp ABI가 바뀌면 `overrides.next.sharp` 갱신)·`package-lock.json`.
- `scripts/verify-next-sharp.mjs` 상수(next·sharp), `tests/unit/test_frontend_dependency_security.py` 기대값, `docker/frontend.Dockerfile`·`.github/workflows/frontend.yml`의 Playwright 이미지 태그·digest, `playwright*.config.ts` 필요 변경.
- `@base-ui/react` 1.8 상향에 따른 컴포넌트 호출부 영향은 `components/ui/*` 범위에서만 확인(T-412 이후면 shim이라 영향 0 예상).
- 완료 후 common PR: `versions.json` `exceptions[]`의 map Next/Playwright exact 예외 제거.

## 범위 밖

npm 12.0.1 exact 정책 변경(예외 유지, O-10), TS 6.0.3(map-marker-react) 통일, React·Tailwind 상향(이미 기준선 이내), common 패키지 채택.

## 대상 저장소·브랜치·PR·되돌리기

- `digitie/kor-travel-map`, WSL 체크아웃, 브랜치 `agent/<agent>-T-413-next-16-3`, `origin/main`에서 분기. PR 1개(lock 동반).
- 되돌리기 = `git revert <merge-sha>` + `npm ci`. 이미지 digest도 같은 revert에 포함되므로 CI가 자동으로 이전 이미지로 돌아간다.

## 예상 변경 파일

아래는 이 task가 만들거나 고칠 예정 경로다. 예정 경로는 존재·실행 증거가 아니다.

```text
package.json, package-lock.json
packages/kor-travel-map-admin/frontend/package.json
packages/kor-travel-map-admin/frontend/scripts/verify-next-sharp.mjs
tests/unit/test_frontend_dependency_security.py
docker/frontend.Dockerfile
.github/workflows/frontend.yml
packages/kor-travel-map-admin/frontend/playwright.config.ts (+ live config)
kor-travel-common: versions.json   # 예외 제거(후속 PR)
```

## 수용 기준

- [ ] map 전 CI(ci·lint·openapi·frontend·docker-images·postgis-only) green; `verify:npm-tree`·`verify:next-sharp`·`audit:high` 통과.
- [ ] `pytest tests/unit/test_frontend_dependency_security.py` 통과(기대값 갱신 근거를 PR 본문에 기재).
- [ ] Playwright mocked 30 spec green이 새 이미지에서 실행됐다(run 로그의 이미지 digest 확인).
- [ ] `check_versions` report에서 map Next/Playwright 행이 `OK`로 바뀌고 예외 제거 common PR이 열렸다.
- [ ] 6폭 스크린샷 diff 0(프레임워크 상향으로 렌더가 바뀌면 원인 기록 후 별도 판단; 토큰 task 기준선과 혼동 금지).

## 검증 명령

```bash
npx --yes npm@12.0.1 ci --workspaces --include=optional --no-audit --no-fund
npm run verify:npm-tree && npm run verify:next-sharp && npm run audit:high
uv run pytest tests/unit/test_frontend_dependency_security.py -q
npx playwright test -c packages/kor-travel-map-admin/frontend/playwright.config.ts
npm run build -w packages/kor-travel-map-admin/frontend
python3 -B -X utf8 tools/check_versions.py --manifest ../kor-travel-map/packages/kor-travel-map-admin/frontend/kor-travel-common.lock.json
```

## evidence

PR 본문(CI run URL·pytest 결과·이미지 digest 전후), `docs/journal.md`, 이 파일 "실행 기록", `versions.json` 예외 제거 PR 링크.

## rollback·release 차단 조건

- `verify-next-sharp` 실패·CI red면 머지 금지. 머지 후 회귀 시 revert 1회.
- 이 task가 미완이어도 T-410~412는 진행 가능하다(예외 등록 상태). 단 ui v0.2 peer가 base-ui ≥1.8을 요구하면 T-412는 이 task 이후로 순서를 바꾼다.
