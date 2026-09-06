# T-470 ktdm: Next 16·React 19·ESLint 9·Node 22 CI 업그레이드(재포맷 금지, recharts 3·`target es5` 실검증, 별도 PR)

- 상태: BLOCKED
- 우선순위: P1
- Gate: vitest 8·build
- 선행: T-005

## 목표

docker-manager 프론트를 Next 14.2.35 → 16.3.x, React 18.3.1 → 19.2.x, ESLint 8(`.eslintrc.json`) → 9 flat(`eslint-config-next` 16), CI Node 20 → 22로 올린다. 업그레이드 사유 문서가 없으므로 ktdm `docs/decisions.md`에 ADR 1건을 남기고, 위험 요소(recharts 3 + React 19 peer, tsconfig `target: es5`, `next lint` 제거)를 실제 빌드·테스트로 검증한다. 대규모 재포맷은 금지(ktdm 규칙).

## 고정 결정

- [design-brief](../plan/design-brief.md) D-06(Next 16.2 floor, React 19.0 floor, ESLint 9 floor, Node 22; ktdm Next 14·React 18·ESLint 8은 Phase 4)·D-08 ②(ktdm은 업그레이드 PR을 먼저 별도로)·D-16(React 18 앱은 tokens부터; ktdm은 L8 전 규칙 참조까지 — 이 task는 common 코드 무관)·D-24.
- ADR-008 — [ADR 색인](../adr/README.md). 정본: [versions](../standards/versions.md), [frontend-stack](../standards/frontend-stack.md)(ESLint flat 조각).
- 사실: Next 14.2.35/React 18.3.1/eslint 8/`.eslintrc.json`, `lint: next lint`, tsconfig `target: es5`, recharts 3.8.1(`next/dynamic` 지연 로드), vitest 4.1.11 + jsdom 27 + Vite 8(8 파일, 31 passed), `ruff format` 전체 실행 금지 관행, CI SHA 핀 + `--max-warnings=0` — [inv/ktdm §3.1·§9·§11-1](../survey/inventory/kor-travel-docker-manager.md), [vm §5.2·§5.3](../survey/cross/version-matrix.md)(Async Request API·`proxy` 규약·codemod), [ci §2.2 ktdm](../survey/cross/ci-deploy.md).
- PR 순서: [judge-migration-feasibility §3.1 ktdm #1](../plan/design-panel/judge-migration-feasibility.md).

## 구현 범위

- ktdm ADR: "Next 16 / React 19 / ESLint 9 채택" 결정·근거(Node 20 EOL, common 기준선, ADR-17 프리미티브 미도입 유지).
- `frontend/package.json`: next 16.3.x, react/react-dom 19.2.x, `@types/react*` 19, `eslint` 9.x + `eslint-config-next` 16, `eslint-plugin-react-hooks` 7, lucide 0.363 유지(1.x는 T-507 재평가); `lint: eslint . --max-warnings=0`; `next lint` 제거 대응. lock 동반.
- `.eslintrc.json` → `eslint.config.mjs`(common `templates/eslint/` 조각 + ktdm 로컬 규칙 이관, 규칙 세트 변경 최소).
- `tsconfig.json` `target: es5` → `ES2022`(Next 16 제거 옵션 대응) — 빌드 산출 차이는 SWC가 처리하므로 런타임 영향 없음을 `next build` + vitest로 확인.
- Async Request API 전환처 grep(`cookies()`·`headers()`·`params`), `middleware` → `proxy`(Next 측 서버 코드 0이므로 해당 없음 예상, 확인 기록).
- recharts 3 + React 19: `DashboardClient.tsx` 차트 렌더 vitest 또는 수동 스모크 기록.
- `.github/workflows/ci.yml` Node 22(SHA 핀 유지).

## 범위 밖

Poetry → uv(T-471), 토큰(T-472), UI 부품(T-473), 프리미티브 도입(ADR-17 유지), `ruff format`, lucide 1.x.

## 대상 저장소·브랜치·PR·되돌리기

- `digitie/kor-travel-docker-manager`, 작업은 ktdm 정본 Linux/WSL, 브랜치 `agent/T-470-next16-react19`(ktdm 규칙 `agent/<topic>`), `main`에서 분기. PR 1개(lock 동반) + ADR 커밋.
- 되돌리기 = `git revert <merge-sha>` + `npm ci`. 운영은 rsync 소스 배포(systemd + `npm run start`)이므로 revert 후 재배포 절차(ktdm `docs/prod-deployment.md`) 동반.

## 예상 변경 파일

아래는 이 task가 만들거나 고칠 예정 경로다. 예정 경로는 존재·실행 증거가 아니다.

```text
docs/decisions.md 또는 docs/adr/*            # ktdm ADR 형식
frontend/package.json, frontend/package-lock.json
frontend/eslint.config.mjs (신규), frontend/.eslintrc.json (삭제)
frontend/tsconfig.json
frontend/src/app/**                           # async request API 전환처(있다면)
.github/workflows/ci.yml
```

## 수용 기준

- [ ] vitest 8 파일 green(31 passed 수준, 실측 기록), `next build` green, `eslint . --max-warnings=0` green.
- [ ] `npm ls react react-dom next eslint recharts --depth=0`: 19.2.x / 16.3.x / 9.x / 3.8.x, peer 경고 0.
- [ ] 차트 패널(recharts)·로그 모달·명령 팔레트가 로컬 스모크에서 렌더된다(스크린샷 또는 vitest).
- [ ] `git diff --stat`에서 재포맷성 변경(공백·따옴표만) 파일 0(리뷰어 확인).
- [ ] 6폭 스크린샷 diff 0(수동, Playwright 없음 → common 템플릿 외부 실행; 실행 못 하면 `NOT_RUN`).
- [ ] `check_versions` ktdm 행 Next/React/ESLint/Node `OK`.

## 검증 명령

```bash
# kor-travel-docker-manager/frontend (Linux/WSL)
npm ci && npm ls react react-dom next eslint recharts --depth=0
npm run lint && npm run type-check && npm test && npm run build
grep -rn 'cookies()\|headers()\|draftMode()' src | wc -l
BASELINE_APP=ktdm BASELINE_URL=http://127.0.0.1:12905 npx playwright test -c ../../kor-travel-common/templates/playwright.baseline.ts
# kor-travel-common
python3 -B -X utf8 tools/check_versions.py --manifest ../kor-travel-docker-manager/frontend/kor-travel-common.lock.json
```

## evidence

PR URL·CI run·`npm ls`·vitest 수·스모크 캡처·ADR 링크를 이 파일 "실행 기록"·`docs/journal.md`에, `consumers.pins.json` 갱신.

## rollback·release 차단 조건

- peer 경고·빌드 실패·차트 렌더 실패면 머지 금지; 머지 후 회귀 시 revert + 재배포.
- 이 task 미완이면 T-472(tokens)를 열지 않는다(D-08 ② 순서).
