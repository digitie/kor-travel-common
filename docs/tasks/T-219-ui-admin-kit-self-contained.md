# T-219 관리자 부품 묶음 1차(앱 의존이 없는 부품)를 공통 UI로 이관

- 상태: BLOCKED
- 우선순위: P1
- Gate: UI 단위·타입·pack 설치·2인 리뷰
- 선행: T-022, T-024
- 소유 저장소: kor-travel-common
- 병렬: T-220의 선행. 병렬 없음

출처는 [공통화 재조사·계획(2026-11-17)](../plan/commonization-plan-2026-11-17.md)의 §3.5·§4.8(K-50)이다. 근거 위치(file:line)와 차이 분석은 그 문서가 정본이며 여기서 반복하지 않는다.

## 목표

map·weather·transport 관리자 프론트에 같은 파일 45개(2,076줄)가 byte 단위로 복사돼 있다. 그중 앱 쪽 모듈(`status-label`, `next/link`)에 기대지 않는 부품을 먼저 `@kor-travel/ui`로 옮긴다. 버전은 올리지 않고 소스만 넣는다. 버전과 동결은 T-221이 T-220과 함께 한 번에 한다.

## 고정 결정

- 새 패키지를 만들지 않는다. `@kor-travel/ui`의 하위 경로 export로 넣는다.
- 계약은 [ui-contract](../standards/ui-contract.md) §4가 정본 초안이다. 실물과 다른 곳은 T-022·T-027의 결과를 따른다.
- 토스트는 주입(`onNotify`)이다. 원천 `copy-button`은 `sonner`를 직접 import하므로 그 import를 주입으로 바꾼다(UC-3.7).
- `@kor-travel/ui`에는 `next` peer가 없다. 이 task의 부품은 `next/*`를 import하지 않는다.
- `ConfirmDialog`는 넣지 않는다. [ui-contract](../standards/ui-contract.md)가 엔진 선택을 앱 소유로 두고 공통 API를 T-508로 미뤘다.
- 클래스는 로컬 어휘가 아니라 `--kt-*` 의미 토큰을 쓴다([design-tokens](../standards/design-tokens.md)).

## 구현 범위

1. 원천(kor-travel-map `packages/kor-travel-map-admin/frontend/src/`, 커밋 `f1788da9`): `components/empty-state`, `components/copy-button`, `components/json-viewer`, `components/section-card`, `components/filter-bar`, `lib/format.ts`, 그리고 `components/help-tip`.
2. `help-tip`은 weather·transport 판(서로 동일, map보다 새 것)을 원천으로 한다. `zustand`를 import하므로 `packages/ui`의 의존 선언과 정책을 확인한다.
3. `section-card`·`filter-bar`는 transport 판이 map·weather 판과 다르다(각 2줄·23줄). 차이를 읽고 고른 쪽을 PR에 적는다.
4. 출처 헤더(SPDX, `Origin`·`Modified`)와 `PROVENANCE.md` 행을 추가한다.
5. 각 부품의 단위 시험(vitest+RTL): data-slot, 기본 prop, 접근성 이름, `onNotify` 호출, `HelpTip`의 `도움말: {label}` 이름과 키보드 동작.
6. `packages/ui/package.json` exports에 하위 경로 추가. `version`은 그대로 둔다.

## 범위 밖

앱 사전·링크 주입이 필요한 부품과 폼·오류(T-220), 버전 올림과 동결(T-221), 소비자 채택, `ConfirmDialog`, `status-label.ts`(도메인 사전, 앱 소유).

## 예상 변경 파일

예정 경로는 존재·실행 증거가 아니다.

```text
packages/ui/src/{empty-state,copy-button,json-viewer,section-card,filter-bar,help-tip,format}.ts(x)
packages/ui/test/*.test.tsx
packages/ui/package.json                 # exports(와 필요하면 zustand 의존)만
PROVENANCE.md
```

## 수용 기준

- [ ] 부품 6종과 `format`이 하위 경로로 import되고 `npm run build --workspace packages/ui`가 d.ts를 만든다.
- [ ] 새 소스에 `next/`, `sonner`, `@/lib/status-label` import가 없다(grep 0).
- [ ] 새 단위 시험이 부품당 3개 이상이고 skip 0이다. 기존 UI 시험 수가 줄지 않는다.
- [ ] 소스에 로컬 어휘 클래스(`text-text-secondary`, `rounded-control` 등)가 남아 있지 않다(grep 0).
- [ ] `packages/ui/package.json`의 `version`과 `dependency-policy.json`이 바뀌지 않았다.
- [ ] pack한 tarball을 `packages/ui/smoke/next-app`에 설치해 webpack·Turbopack 빌드가 통과한다.

## 검증 명령

```bash
npm ci --engine-strict && npm run check:toolchain
npm run build --workspace packages/ui && npm test --workspace packages/ui
rg -n "text-text-secondary|rounded-control|from \"next/|from \"sonner\"|status-label" packages/ui/src && exit 1 || true
python3 -B -X utf8 tools/check_spdx.py
```

## evidence

시험 수 전후, pack SHA-256, smoke 빌드 출력. 소비자 화면 비교는 `NOT_RUN(T-415)`.

## rollback·release 차단 조건

- `git revert` 1회. 버전이 오르지 않았으므로 소비자 영향이 없다.
- 출처 헤더와 `PROVENANCE.md` 행이 없으면 병합하지 않는다.
