# T-460 weather: Next 16·Vitest 4·Node 22 CI·eslint-config-next 16·`moduleResolution: bundler`·react-query 미사용 정리·CI vitest/mypy 추가(별도 PR)

- 상태: BLOCKED
- 우선순위: P1
- Gate: ci.yml
- 선행: T-005

## 목표

weather admin 프론트를 common 기준선으로 올린다: Next 15.5.24 → 16.3.x, Vitest 3.2.7 → 4.1.x, `eslint-config-next` 15 → 16(+ react-hooks plugin 7), CI Node 20 → 22, tsconfig `moduleResolution: node` → `bundler`, 미사용 `@tanstack/react-query` 제거, CI에 `npm test`(vitest)와 `mypy` 추가. 스타일·토큰은 건드리지 않는다(T-461은 이 task와 독립).

## 고정 결정

- [design-brief](../plan/design-brief.md) D-06(Next 16.2 floor, Vitest 4.1, Node 22, ESLint 9)·D-08 ⑥(weather: `tokens.css` 교체는 Next 버전과 독립 → 그 다음 Next 16·Vitest 4·Node 22)·D-24(프레임워크 PR 분리).
- ADR-008 — [ADR 색인](../adr/README.md). 정본: [versions](../standards/versions.md), [frontend-stack](../standards/frontend-stack.md), [ci-deploy](../standards/ci-deploy.md).
- 사실: Next 15.5.24, vitest 3.2.7(테스트 4개, `--passWithNoTests`), CI Node 20 vs Docker `node:22-alpine`, `moduleResolution: "node"`, react-query import 0건, CI frontend job이 vitest 미실행·mypy 선언만, `middleware.ts`(Next 16은 `proxy` 규약) — [inv/weather §3.1·§6·§9](../survey/inventory/kor-travel-weather.md), [vm §5.2·§5.3](../survey/cross/version-matrix.md)(Async Request API·`next lint` 제거·codemod).
- PR 순서: [judge-migration-feasibility §3.1 weather #2](../plan/design-panel/judge-migration-feasibility.md), §4.2(T-461 선행 아님).

## 구현 범위

- `packages/kor-travel-weather-admin/frontend/package.json`: next 16.3.x, react 19.2.x 확인, vitest 4.1.x, `eslint-config-next` 16, `eslint-plugin-react-hooks` 7, `@types/node` 22 유지, react-query 제거; lock 동반. `npx @next/codemod@canary upgrade latest` 결과를 리뷰해 적용.
- `middleware.ts` → Next 16 `proxy.ts` 규약(인증 bypass 동작·matcher 보존), `cookies()`/`headers()` 동기 접근처 async 전환(grep으로 목록화).
- `tsconfig.json` `moduleResolution: bundler`; `vitest.config.ts` 신설(jsdom 불필요 시 node), `--passWithNoTests` 제거(테스트 4개 실행 강제).
- `.github/workflows/ci.yml`: frontend job Node 22 + `npm test`; python job에 `uv run mypy` 추가(strict 선언과 실행 일치; 위반은 baseline 등록).

## 범위 밖

토큰 교체(T-461), Tailwind 도입(T-462), Python 3.11/3.12/3.13 정합(T-481), 셸 문서-코드 불일치(T-464), `python-airkorea-api` 스냅샷(T-481 L15).

## 대상 저장소·브랜치·PR·되돌리기

- `digitie/kor-travel-weather`, 브랜치 `feat/T-460-next16`(weather CI가 `feat/**` push에도 실행), `origin/main`에서 분기, Draft PR 우선. PR 1개(lock 동반; CI 변경이 커지면 "프론트 업그레이드" / "CI job 추가" 2 PR).
- 되돌리기 = `git revert <merge-sha>` + `npm ci`.

## 예상 변경 파일

아래는 이 task가 만들거나 고칠 예정 경로다. 예정 경로는 존재·실행 증거가 아니다.

```text
packages/kor-travel-weather-admin/frontend/package.json, package-lock.json
packages/kor-travel-weather-admin/frontend/tsconfig.json
packages/kor-travel-weather-admin/frontend/vitest.config.ts
packages/kor-travel-weather-admin/frontend/proxy.ts   # middleware.ts 이름 변경
packages/kor-travel-weather-admin/frontend/app/**     # async request API 전환처
.github/workflows/ci.yml
deploy/Dockerfile.web                                 # Node 22 유지 확인
```

## 수용 기준

- [ ] `ci.yml` green: frontend job(Node 22)에서 `lint`·`type-check`·`test`(vitest 4개 실행, 0 test 금지)·`build` 통과; python job에 mypy step이 있고 통과(baseline 위반 수 기록).
- [ ] `npm ls next vitest eslint-config-next @tanstack/react-query --depth=0`: next 16.3.x, vitest 4.1.x, eslint-config-next 16, react-query 없음.
- [ ] 비-production 인증 bypass·production 403/401 분기가 `proxy.ts`에서 동일 동작(vitest 또는 수동 기록).
- [ ] 6폭 스크린샷 diff 0(프레임워크 상향은 렌더를 바꾸지 않아야 함; diff 시 원인 기록).
- [ ] `check_versions` weather 행 Next/Vitest/Node `OK`.

## 검증 명령

```bash
# kor-travel-weather/packages/kor-travel-weather-admin/frontend
npm ci --ignore-scripts && npm ls next vitest eslint-config-next --depth=0
npm run lint && npm run type-check && npm test && npm run build
# 루트
uv sync --locked --extra dev --extra dagster && uv run mypy src packages
# kor-travel-common
python3 -B -X utf8 tools/check_versions.py --manifest ../kor-travel-weather/packages/kor-travel-weather-admin/frontend/kor-travel-common.lock.json
```

## evidence

PR URL·CI run·`npm ls` 출력·codemod 적용 목록·6폭 diff를 이 파일 "실행 기록"·`docs/journal.md`에, `consumers.pins.json` 갱신.

## rollback·release 차단 조건

- CI red·인증 분기 동작 변화·원인 불명 diff면 머지 금지, 머지 후 회귀 시 revert 1회.
- 이 task가 미완이어도 T-461(순수 CSS)은 진행한다; T-462는 이 task 완료 후에만.
