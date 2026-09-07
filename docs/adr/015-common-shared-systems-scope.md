# ADR-015: 공용 시스템 범위(위젯·토큰·코어 로직·로그인)

- 상태: accepted
- 날짜: 2026-09-07
- 근거 문서: 사용자 범위 재확인, [T-016](../tasks/T-016-common-shared-systems-scope.md), [ADR-001](001-purpose-boundary-and-deliverables.md), [ADR-011](011-python-common-package.md)
- Supersedes: ADR-001·ADR-011의 인증 프리미티브·로그인 위젯 제외 부분

## 컨텍스트

기존 설계는 common을 UI·백엔드 공통 코드와 규칙을 모아 두는 저장소로 정의하면서도 비밀번호·세션·CSRF·JWT·RBAC과 로그인 폼을 모두 소비자에 남겼다. 이 문구는 사용자가 확인한 목표인 “위젯, 디자인 토큰, 공용 코어 로직, 로그인과 같은 공용 시스템을 하나로 모으는 것”과 충돌한다. 동시에 common을 인증 서버나 운영 시스템으로 해석하면 소비자 저장소를 수정하거나 운영 책임을 common에 부여하게 된다.

## 결정

1. kor-travel-common은 독립적으로 실행되는 제품·인증 서버·데이터베이스·배포 환경이 아니라 kor-travel 제품군이 공유하는 GPL-3.0-or-later 라이브러리·규칙·템플릿·검사 도구 저장소로 유지한다.
2. 공용 배포 단위는 디자인 토큰(`packages/tokens`), React 위젯·컴포넌트와 로그인 UI 계약(`packages/ui`), Python 공용 코어와 주입형 인증 프리미티브(`packages/py/kor-travel-common`), 규칙·템플릿·검사 도구다. 로그인은 레지스트리 템플릿만의 기능으로 제한하지 않고 재사용 가능한 위젯과 계약을 common에서 제공한다.
3. 인증 공용 코어가 제공할 수 있는 것은 비밀번호 해시·세션/토큰·CSRF·JWT 검증·RBAC 정책을 위한 순수 함수, 타입, 어댑터 인터페이스와 검증 규칙이다. 저장소, 키·비밀, 사용자·조직 데이터, 외부 IdP, 세션 폐기 저장소, 라우트별 접근 정책, rate limit 운영, 인증 서버와 배포는 소비자가 소유한다. 공용 코어는 기본 저장소·운영 호스트·비밀을 내장하지 않는다.
4. `@kor-travel/ui`는 `LoginForm`·로그인 상태·오류 영역 등 공통 UI 계약을 제공할 수 있고, 소비자는 endpoint·identity provider·success redirect·브랜드 오버라이드를 주입한다. 셸 nav·RBAC의 앱별 구성과 인증 왕복은 소비자에 남긴다.
5. common 작업 중 소비자 저장소를 직접 수정하지 않는다. 소비자 채택은 앱별 task와 PR에서 수행하며, common에서 소비자 빌드·e2e를 실행하지 못하면 `NOT_RUN(소비자 저장소/환경 없음)`으로 기록한다. npm·PyPI에는 게시하지 않는다.
6. 공용 인증 API를 추가하거나 계약을 바꿀 때는 별도 task와 공개 API 계약 시험, CHANGELOG의 breaking 판정, 두 명의 적대적 리뷰를 거친다. 이 ADR은 인증 구현 자체를 완료한 것으로 보지 않는다.

## 대안 검토

- **인증을 계속 소비자에만 둔다**: 로그인·비밀번호·세션 구현이 여러 저장소에 반복되고 공용 규칙과 계약을 검증할 수 없으므로 사용자 목표를 충족하지 못한다.
- **common을 인증 서비스로 만든다**: 서버·DB·운영 비밀·배포 책임이 생기고 common의 라이브러리 경계를 깨므로 채택하지 않는다.
- **공용 프리미티브와 UI 계약을 라이브러리로 제공한다**: 재사용·검증 비용을 common에 모으면서 소비자별 저장소와 운영 정책을 보존하므로 채택한다.

## 결과와 후속

- [T-016](../tasks/T-016-common-shared-systems-scope.md)은 이 결정에 맞춰 현재 문서·task·책임표를 동기화한다.
- [T-210](../tasks/T-210-ui-admin-header-form.md)·[T-211](../tasks/T-211-ui-registry-channel-drift.md)은 공용 로그인 UI 계약과 앱 소유 인증 왕복을 구분한다.
- [T-312](../tasks/T-312-auth-core-primitives.md)은 Python 인증 프리미티브의 API·위협 모델·계약 시험을 구현한다.
- T-463·T-484·T-485·T-486 등 소비자 이관 task는 common 프리미티브를 선택적으로 채택하되 사용자 저장소·IdP·정책은 앱에 둔다.
- 기존 ADR-001·ADR-011의 역사적 결정 문구는 보존하고 인증 제외 부분만 이 ADR로 부분 대체한다.
