# 공용 범위 재점검 — 2026-09-07

이 문서는 사용자가 확인한 공용 범위를 현재 architecture·standards·task와 대조한 결과다. 규범은 [ADR-015](../adr/015-common-shared-systems-scope.md)와 각 정본 문서이며, 이 문서는 점검 evidence와 후속 연결을 기록한다.

## 확인 결과

| 영역 | 기존 문구/관찰 | 현재 공용 책임 | 소비자에 남는 경계 | 후속 task·근거 |
|---|---|---|---|---|
| 디자인 토큰 | `packages/tokens`와 `tokens.css` 정본 | 의미 토큰·프로필·다크 값·생성물 계약 | 브랜드 값·폰트 로딩·앱별 override | T-101·ADR-006 |
| React 위젯 | `packages/ui` 프리미티브·마크업 계약 | 공용 위젯과 LoginForm 등 로그인 UI 계약 | 도메인 화면·nav 구성·endpoint·IdP 왕복 | T-201·T-210·ADR-015 |
| Python 코어 | health/time/quality 등 얇은 모듈 | 공용 인프라와 주입형 인증 프리미티브 | 사용자 DB·키/비밀·세션 저장·정책·서버 | T-302·T-312·ADR-015 |
| 로그인 규칙 | UX 문서와 앱별 로그인 템플릿이 분리 | 접근성·오류·redirect 계약과 재사용 위젯 | 앱별 provider·라우트·브랜드·운영 rate limit | T-105·T-211·T-312 |
| OpenAPI·버전 | common 도구가 규칙·매니페스트를 검사 | 공용 계약·validator·보고 도구 | 소비자 실제 채택·실행 evidence | T-011·T-012·ADR-014 |
| 운영·배포 | common은 npm/PyPI 미게시 | Git 태그·wheel/tarball 자산과 규칙 제공 | registry 게시·인증 서비스 운영·소비자 배포 | ADR-014·T-501 |
| 포트·fixture | `130xx`가 common 대역처럼 서술됨 | 테스트 fixture에 필요한 임시 포트 설정 | ktdm 운영 포트 정본·sibling 등록은 소비자 | T-014·T-108·CI-20 |

## 범위 판정

- 공용화 근거가 두 곳 이상인 토큰·UI·코어 계약은 common에 둔다. 한 앱의 도메인 화면·지도 엔진·provider·운영 서버는 common에 복사하지 않는다.
- 로그인과 인증은 **공용 라이브러리 계층**으로 포함한다. 인증 서버, 사용자/세션 DB, 운영 비밀, 외부 IdP, 앱별 역할·접근 정책은 포함하지 않는다.
- 소비자 저장소 수정·실제 채택·빌드·e2e는 이 저장소의 완료 evidence가 아니다. 이 점검에서 소비자 실행은 `NOT_RUN(소비자 저장소를 수정하지 않는 범위)`다.
- 현재 문서에 남아 있던 “인증 전체 범위 밖” 문구는 ADR-015와 동기화된 정본에서 공용 프리미티브/앱 소유 경계로 고쳤다. 역사적 survey·review 문구는 사실 기록으로 보존한다.

## 후속 순서

1. T-016에서 이 문서·ADR·architecture·standards·task 의존성을 갱신하고 두 리뷰어의 finding을 반영한다.
2. T-011을 매니페스트 schema/validator 구현으로 진행한다. 초안 통과는 소비자 채택 성공이 아니며 실제 경로·workflow 경계 회귀를 포함한다.
3. T-201/T-210에서 로그인 UI 계약을 구현하고 T-312에서 Python 인증 프리미티브를 별도로 구현한다.
4. 각 소비자 이관 task에서 common API를 채택하고 소비자 저장소의 실제 실행 evidence를 남긴다.
