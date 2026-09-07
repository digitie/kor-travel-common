# T-214 공용 로그인 위젯·상태 계약

- 상태: BLOCKED
- 우선순위: P1
- Gate: UI 단위·접근성·pack 스모크·2인 적대적 리뷰
- 선행: T-210, T-213a

## 목표

`@kor-travel/ui`에 소비자들이 재사용할 수 있는 `LoginForm`·로그인 상태·오류 영역 계약을 구현한다. 공용 위젯은 입력과 접근성·상태 표시를 소유하고 endpoint·IdP·redirect·세션 왕복은 앱 adapter가 주입한다.

## 고정 결정

- [ADR-015](../adr/015-common-shared-systems-scope.md)와 [ui-contract](../standards/ui-contract.md), [ux-guide](../standards/ux-guide.md) UX-G7이 현재 계약의 정본이다.
- 위젯은 GPL-3.0-or-later common 패키지에 포함하고 npm에 게시하지 않는다. 소비자는 고정 Git 태그/tarball을 사용한다.
- 운영 비밀·사용자/세션 저장소·외부 IdP·rate limit·앱별 역할/라우트 정책은 위젯이 직접 읽거나 결정하지 않는다.

## 구현 범위

- `LoginForm`, `LoginStatus`, `LoginError` 컴포넌트와 subpath exports를 추가한다.
- `credentials`, `nextPath`(로컬 경로만), `onSubmit`, `pending`, `error`, `onClearError` 등 주입 계약과 한국어 접근성 문구를 고정한다.
- 항상 존재하는 `role="alert"` 오류 영역, label 연결, submit pending/재시도/포커스, 외부 redirect 차단을 구현한다.
- 소비자 endpoint 호출·IdP adapter 예제는 레지스트리/소비자 task에서 연결하고 패키지에서 네트워크를 호출하지 않는다.

## 범위 밖

인증 서버·사용자/세션 DB·운영 비밀·IdP SDK·세션 폐기·rate limit·RBAC 정책·앱 셸 nav·소비자 저장소 변경·실제 registry/npm 게시.

## 예상 변경 파일

`packages/ui/src/login-form.tsx`, `packages/ui/src/login-status.tsx`, `packages/ui/src/login-error.tsx`, `packages/ui/src/index.ts`, 관련 단위/접근성 시험, `packages/ui/package.json`, `docs/standards/ui-contract.md`, `docs/standards/ux-guide.md`, `CHANGELOG.md`.

## 수용 기준

- 공개 exports·props·`data-slot`·문구·오류/대기 상태가 문서 계약과 일치한다.
- 외부 URL `nextPath`가 `/`로 치환되고 widget이 네트워크·비밀·저장소를 직접 사용하지 않는다.
- unit/axe 시험이 0 test·skip 없이 통과하고 `npm pack` 후 fixture 설치·TypeScript/webpack smoke가 성공한다.
- 변경 후 두 reviewer가 P0/P1 finding 없이 승인한다.

## 검증 명령

```bash
npm run test -w packages/ui -- login-form login-status login-error
npm run build -w packages/ui
npm pack --workspace packages/ui
```

## evidence

T-210/T-213a 완료 후 public API manifest, test count·OS, pack hash, accessibility 결과와 common fixture smoke 결과를 기록한다. 소비자 실제 채택·정식 릴리스는 T-213·T-463·T-422 등에서 별도로 검증한다.

## rollback 또는 release 차단 조건

위젯이 endpoint·비밀·저장소·RBAC 정책을 내장하거나 외부 redirect를 허용하면 release를 차단하고 계약을 수정한다. package 변경은 태그 전에 revert 가능해야 한다.
