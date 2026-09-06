# T-430 airport: WIP `codex/shadcn-ui-foundation` 병합(값 유지·`cn`→clsx+twMerge·devDeps 이동·Button D-09 레시피)

- 상태: BLOCKED
- 우선순위: P0
- Gate: frontend CI
- 선행: 없음
- 외부 선행: 현재 airport 기준 SHA·병합된 PR #18/#22·잔여 정렬 및 live-e2e 결과를 해당 저장소 담당자가 확인한다. 과거 WIP 재병합은 하지 않는다.

## 목표

airport main(`2bb1111`, Tailwind 없음, 순수 CSS 1,844행)에 WIP 브랜치 `codex/shadcn-ui-foundation`(`99b3f98`, Tailwind v4.3.3 + shadcn `base-nova` 브릿지)을 값 무변경으로 병합하고, 직후 정렬 PR로 common 정책과 어긋난 4가지(`cn` npm 패키지, `shadcn`/`postcss`/`@tailwindcss/postcss`의 dependencies 위치, `engines` 미선언, Button 레시피)를 맞춘다. 이 task 완료가 airport tokens/ui 채택(T-431·T-432)의 시작점이다.

## 인계 시점 정정

[2026-09-06 직접 재확인](../plan/handoff-verification.md)에서 PR #18과 T-035 PR #22가 이미 병합된 사실을 확인했다. 아래 기존 구현 범위는 과거 WIP 대비 점검 목록으로만 사용한다. 실행 전 현재 `origin/main`의 코드·lock·CI와 각 항목을 대조해 완료 항목은 evidence로 대체하고 잔여만 해당 저장소 후속 PR로 처리한다. PR #22의 live-e2e 실패가 있으므로 병합 사실만으로 이 task를 DONE 처리하지 않는다. 기존 소비자 dirty 변경은 보존한다.

## 고정 결정

- [design-brief](../plan/design-brief.md) D-08 ①(WIP 병합: 값 16/10·alpha line 유지, `cn`→clsx+tailwind-merge, shadcn/postcss devDependencies)·D-09(Button `type="button"` 기본·`loading` 계약·variant 7·size 8)·D-20(airport Admin = 무인증 백업 패널 + collector-status 패널)·O-9(WIP 값 유지 병합).
- ADR-007·ADR-012 — [ADR 색인](../adr/README.md). 정본: [frontend-stack](../standards/frontend-stack.md), [ui-contract](../standards/ui-contract.md).
- 사실: WIP 단일 커밋 61 files(+17,157/−1,999), `tokens.css` 무변경, `--muted`/`--accent`/`--radius` 충돌을 재명명(약 30곳), `frontend/src/lib/utils.ts`가 npm `cn` 0.2.5 재수출, `button.tsx`는 JSX 미사용, `shadcn`·`postcss`·`@tailwindcss/postcss`가 dependencies, `agentRules: false`, PR 개설 여부 미확인 — [inv/kta §3.2·§9](../survey/inventory/kor-travel-airport.md), [vm §5.2](../survey/cross/version-matrix.md), [dt §5-5](../survey/cross/design-tokens.md).
- PR 순서: [judge-migration-feasibility §3.1 airport #0·#1](../plan/design-panel/judge-migration-feasibility.md).

## 구현 범위

- PR 0(사용자 소유): WIP 브랜치를 PR로 열고 frontend CI(vitest·tsc·build) green 확인 후 병합. common 작성자는 병합하지 않고 결과만 기록한다.
- PR 1(정렬, ≤10 파일): `cn` 패키지 제거 → `clsx` + `tailwind-merge`(`lib/utils.ts`), `shadcn`·`postcss`·`@tailwindcss/postcss`를 devDependencies로, `package.json` `engines.node ^22.12.0`(+ `.nvmrc`), `components/ui/button.tsx`를 D-09 레시피(`type="button"` 기본, `loading`=`aria-disabled`+`aria-busy`+spinner+포커스 유지, root opacity 금지)로 수정 — 여전히 JSX 미사용이므로 렌더 영향 0.
- `tokens.css` 값(16/10px radius, alpha line)은 그대로 둔다(수렴 여부는 T-431 baseline에서 판단하지 않음, 열림).

## 범위 밖

토큰 패키지 채택(T-431), 컴포넌트 shadcn 교체(airport T-034, 앱 소유), 모바일 하단 탭바(T-035), ESLint 도입·TS 7 판정(T-433), 백엔드.

## 대상 저장소·브랜치·PR·되돌리기

- 저장소 `digitie/kor-travel-airport`. PR 0 브랜치 = 기존 `codex/shadcn-ui-foundation`; PR 1 브랜치 `codex/T-430-align-common`(airport 규칙 `codex/<topic>` + Draft PR), 병합된 `main`에서 분기. 작업 환경은 airport 정본 WSL2.
- 되돌리기: PR 1은 `git revert <merge-sha>` 1회. PR 0(61 files)은 squash 머지 커밋 1개를 revert하면 main 원상복구(사용자 결정 사항).

## 예상 변경 파일

아래는 이 task가 만들거나 고칠 예정 경로다. 예정 경로는 존재·실행 증거가 아니다.

```text
frontend/src/lib/utils.ts
frontend/src/components/ui/button.tsx
frontend/package.json, frontend/package-lock.json
frontend/.nvmrc
```

## 수용 기준

- [ ] `main`에 `99b3f98`(또는 그 squash)이 포함되고 frontend CI(vitest 10·`tsc --noEmit`·`next build`)가 green이다.
- [ ] `git diff main~1..main -- frontend/src/app/tokens.css` 출력 없음(값 유지).
- [ ] `frontend/package.json`: `cn` 0건, `shadcn`·`postcss`·`@tailwindcss/postcss`가 devDependencies, `engines.node` 선언; `npm ls cn` 빈 결과.
- [ ] `button.tsx`가 D-09 계약 단위 테스트(vitest, `loading` 시 `aria-busy` + `onClick` 차단 + 포커스 유지) 1개 이상을 동반한다.
- [ ] 데스크톱·375px 스크린샷 diff 0(WIP 커밋 메시지의 "픽셀 동일" 주장을 재현해 evidence로 남김; 재현 못 하면 `NOT_RUN`).
- [ ] `check_versions` report에서 airport Tailwind·shadcn 행이 `OK`(TS 7은 T-433 예외 등록 전까지 `NOT_RECOMMENDED`로 남아도 이 task는 통과).

## 검증 명령

```bash
# kor-travel-airport/frontend (WSL2)
npm ci && npx tsc --noEmit && npm test && npm run build
npm ls cn tailwind-merge clsx --depth=0
git diff --stat main~1..main -- src/app/tokens.css
# kor-travel-common
python3 -B -X utf8 tools/check_versions.py --manifest ../kor-travel-airport/frontend/kor-travel-common.lock.json
```

## evidence

PR 0·PR 1 URL과 머지 SHA, CI run URL, 스크린샷 diff 결과를 이 파일 "실행 기록"·`docs/journal.md`에 남긴다. `docs/architecture/adoption-readiness.md` airport gate 행 갱신.

## rollback·release 차단 조건

- PR 0이 열리지 않거나 CI red면 이 task는 `외부 선행` 대기로 남고 T-431·T-432는 BLOCKED 유지; T-212의 airport 대체 경로도 사용 불가.
- PR 1에서 렌더 diff가 생기면(예: `cn` 병합 순서 차이) 원인 특정 전 머지 금지.
