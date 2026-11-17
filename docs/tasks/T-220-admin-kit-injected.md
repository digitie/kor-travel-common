# T-220 admin-kit 2차: 사전·링크 주입이 필요한 부품과 폼·오류

- 상태: BLOCKED
- 우선순위: P1
- Gate: UI 단위·타입·pack 설치·2인 리뷰
- 선행: T-219
- 소유 저장소: kor-travel-common
- 병렬: 병렬 없음

출처는 [공통화 재조사·계획(2026-11-17)](../plan/commonization-plan-2026-11-17.md)의 §3.5·§4.8(K-50·K-52)이다. 근거 위치(file:line)와 차이 분석은 그 문서가 정본이며 여기서 반복하지 않는다.

## 목표

T-219에 이어, 앱의 상태 사전(`status-label`)이나 라우터 링크(`next/link`)에 기대던 부품과 폼·오류 부품을 `@kor-travel/admin-kit`에 넣는다. 앱 의존은 prop 주입으로 바꾼다.

## 고정 결정

- T-219와 같다.
- `StatusBadge`·`StatStrip`의 상태 문구와 tone은 앱이 사전을 주입한다(ui-contract의 '사전 주입형'). `status-label.ts`는 앱에 남는다.
- `StatStrip`·`DetailList`의 링크는 `next/link`를 import하지 않고 링크 컴포넌트(또는 render 함수)를 prop으로 받는다. 기본은 `<a>`다.
- `PaginationBar`는 기존 T-208(Pager)과 범위가 겹친다. T-022가 나눈 결과를 따른다.
- `validateForm`은 넣지 않는다(규칙 기반 구현은 map 한 곳, pinvi는 zod 기반).
- 셸 조각은 skip link와 header 띠, 접힘 선호 hook까지다. nav 내용·권한·로그아웃은 앱 소유다([ui-contract](../standards/ui-contract.md) §4.6).

## 구현 범위

1. 원천(map `f1788da9`): `components/status-badge`·`status-badge-variants`, `stat-strip`, `detail-list`, `pagination-bar`, `components/ui/form-field-input`·`form-select`·`form-textarea`·`form-field-shared`, `components/app-error-panel`와 `lib/error-recovery.ts`.
2. `@/lib/status-label` import를 주입 prop으로, `next/link` import를 링크 주입으로 바꾼다. `HelpTip`은 T-219의 것을 쓴다.
3. transport 사본과 다른 파일(`app-error-panel` 16줄, `error-recovery` 2줄)은 차이를 읽고 어느 쪽을 택했는지 PR에 적는다.
4. `AdminSkipLink`, `AdminPageHeader`, 접힘 선호 hook(저장 키는 인자).
5. 단위 시험과 exports 추가. `version`은 그대로.

## 범위 밖

버전 올림과 동결(T-221), 소비자 채택, 앱별 nav·로그아웃, `ConfirmDialog`, `validateForm`.

## 예상 변경 파일

예정 경로는 존재·실행 증거가 아니다.

```text
packages/admin-kit/src/{status-badge,status-badge-variants,stat-strip,detail-list,pagination-bar,form-field-*,form-select,form-textarea,app-error-panel,error-recovery,admin-skip-link,admin-page-header}.ts(x)
packages/admin-kit/test/*.test.tsx, packages/admin-kit/package.json  # exports만
PROVENANCE.md
```

## 수용 기준

- [ ] 부품이 하위 경로로 import되고 빌드·타입 검사가 통과한다.
- [ ] 새 소스에 `next/`와 `@/lib/status-label` import가 없다(grep 0). 사전·링크를 주입하지 않아도 렌더되는 기본 동작 시험이 있다.
- [ ] `AppErrorPanel`이 `role="alert"`와 재시도·이전 화면 동작을 갖는다는 시험이 있다.
- [ ] 기존 세 패키지의 `package.json` 버전과 tarball SHA-256이 바뀌지 않았다.

## 검증 명령

```bash
npm run build --workspace packages/admin-kit && npm test --workspace packages/admin-kit
python3 -B -X utf8 tools/check_spdx.py
```

## evidence

T-219와 같은 형식.

## rollback·release 차단 조건

- `git revert` 1회. 정책에 등록하기 전이라 소비자 영향이 없다.
