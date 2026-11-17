# T-219 선택형 패키지 admin-kit 골격과 앱 의존이 없는 부품

- 상태: BLOCKED
- 우선순위: P1
- Gate: UI 단위·타입·pack 설치·2인 리뷰
- 선행: T-022, T-025
- 소유 저장소: kor-travel-common
- 병렬: T-220의 선행. 병렬 없음

출처는 [공통화 재조사·계획(2026-11-17)](../plan/commonization-plan-2026-11-17.md)의 §3.5·§4.8(K-50)이다. 근거 위치(file:line)와 차이 분석은 그 문서가 정본이며 여기서 반복하지 않는다.

## 목표

map·weather·transport 관리자 프론트에 같은 파일 45개(2,076줄)가 byte 단위로 복사돼 있다. 부품을 쓰지 않는 소비자까지 재vendor시키지 않도록 `@kor-travel/ui`를 키우지 않고 선택형 산출물 패키지 `@kor-travel/admin-kit`를 만든다. 이 task는 패키지 골격과, 앱 쪽 모듈(`status-label`, `next/link`)에 기대지 않는 부품을 넣는다. 정책 등록과 동결은 T-221이 한다.

## 고정 결정

- 새 패키지는 `packages/admin-kit`, 이름 `@kor-travel/admin-kit`이다. `artifactPackages`에는 넣고 프로필 필수 목록에는 넣지 않는다(`@kor-travel/toast`와 같은 자리). 근거는 계획 문서 §4.8의 비교와 ADR-019의 선택형 패키지 원칙이다.
- `@kor-travel/ui`와 `@kor-travel/tokens`는 peer다. peer는 같은 minor 범위로 선언해 `ui` patch마다 이 패키지를 올리지 않게 한다. `next`는 peer로 두지 않는다.
- 토스트는 주입(`onNotify`)이다. 원천 `copy-button`의 `sonner` import를 주입으로 바꾼다([ui-contract](../standards/ui-contract.md) UC-3.7).
- `ConfirmDialog`는 넣지 않는다. ui-contract가 엔진 선택을 앱 소유로 두고 공통 API를 T-508로 미뤘다.
- 클래스는 로컬 어휘가 아니라 `--kt-*` 의미 토큰을 쓴다([design-tokens](../standards/design-tokens.md)).
- T-025가 끝난 뒤에 시작한다. 그 전에는 정책에 이 패키지를 더하는 것만으로 `ui`·`tokens`·`toast`가 다시 pack된다.

## 구현 범위

1. 패키지 골격: `package.json`(ESM, exports 하위 경로, peer), tsconfig, vitest, LICENSE·NOTICE, 내장 검사(자기 peer만, T-025의 방식). 루트 workspace와 lock, `docs.yml`의 packages job이 이 패키지도 build·test·pack하게 한다.
2. 원천(kor-travel-map `packages/kor-travel-map-admin/frontend/src/`, 커밋 `f1788da9`): `components/copy-button`, `components/json-viewer`, `components/section-card`, `components/filter-bar`, `lib/format.ts`, 그리고 `components/help-tip`.
3. `help-tip`은 weather·transport 판(서로 동일, map보다 새 것)을 원천으로 한다. `zustand`를 import하므로 의존 선언과 정책을 확인한다.
4. `section-card`·`filter-bar`는 transport 판이 map·weather 판과 다르다(각 2줄·23줄). 차이를 읽고 고른 쪽을 PR에 적는다.
5. `empty-state`: 공통에 이미 `@kor-travel/ui/empty`가 있다. 로컬 `EmptyState`를 넣지 않고 `Empty`로 대체할 수 있는지 계약(`title`·`description`·`action`·`framed`)을 대조해 정하고, 결정을 [ui-contract](../standards/ui-contract.md)에 적는다.
6. 출처 헤더(SPDX, `Origin`·`Modified`)와 `PROVENANCE.md` 행, 부품별 단위 시험(vitest+RTL).

## 범위 밖

앱 사전·링크 주입이 필요한 부품과 폼·오류(T-220), 정책 등록·동결(T-221), 소비자 채택, `ConfirmDialog`, 앱에 남는 파일(`sonner.tsx`, 로컬 `button.tsx`, `occurrence-key`·`string-list`, `app/error.tsx`·`app/global-error.tsx`, `status-label.ts`).

## 예상 변경 파일

예정 경로는 존재·실행 증거가 아니다.

```text
packages/admin-kit/{package.json,tsconfig.json,vitest.config.ts,LICENSE,NOTICE,README.md}
packages/admin-kit/src/{copy-button,json-viewer,section-card,filter-bar,help-tip,format}.ts(x)
packages/admin-kit/test/*.test.tsx
package.json, package-lock.json, .github/workflows/docs.yml
PROVENANCE.md, docs/architecture/packages.md, docs/standards/ui-contract.md
```

## 수용 기준

- [ ] `npm run build --workspace packages/admin-kit`가 d.ts를 만들고 부품 5종과 `format`이 하위 경로로 import된다.
- [ ] 새 소스에 `next/`, `sonner`, `@/lib/status-label` import가 없다(grep 0). 로컬 어휘 클래스(`text-text-secondary`, `rounded-control` 등)가 없다(grep 0).
- [ ] 새 단위 시험이 부품당 3개 이상이고 skip 0이다.
- [ ] `packages/ui`·`packages/tokens`·`packages/toast`의 `package.json` 버전과 pack한 tarball SHA-256이 이 PR 전과 같다.
- [ ] `EmptyState`와 `Empty` 가운데 무엇을 남기는지와 근거가 PR과 ui-contract에 있다.
- [ ] pack한 tarball을 `packages/ui/smoke/next-app`(또는 같은 구성의 smoke)에 `ui`와 함께 설치해 webpack·Turbopack 빌드가 통과한다.

## 검증 명령

```bash
npm ci --engine-strict && npm run check:toolchain
npm run build --workspaces && npm test --workspaces
rg -n "text-text-secondary|rounded-control|from \"next/|from \"sonner\"|status-label" packages/admin-kit/src && exit 1 || true
npm pack --workspace packages/ui --workspace packages/tokens --workspace packages/toast && sha256sum *.tgz
python3 -B -X utf8 tools/check_spdx.py
```

## evidence

시험 수, 네 tarball의 SHA-256(기존 셋은 전후 동일), smoke 빌드 출력. 소비자 화면 비교는 `NOT_RUN(T-415)`.

## rollback·release 차단 조건

- `git revert` 1회. 정책에 등록하기 전이라 소비자 영향이 없다.
- 기존 세 패키지의 tarball SHA-256이 달라지면 병합하지 않는다(T-025가 덜 된 것이다).
