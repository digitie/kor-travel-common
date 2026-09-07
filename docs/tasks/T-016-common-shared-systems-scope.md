# T-016 공용 시스템 범위 재정의와 전체 계획 동기화

- 상태: IN_PROGRESS
- 우선순위: P0
- Gate: 문서·계획 검증·2인 적대적 리뷰
- 선행: 없음

## 목표

kor-travel-common이 독립 운영 시스템이 아니라 위젯·디자인 토큰·공용 코어 로직·로그인 계층을 함께 제공하는 공용 라이브러리·규칙 저장소라는 사용자 범위를 현재 문서와 순차 task에 반영한다. 공용 인증 프리미티브를 포함하되 인증 서버·사용자 DB·운영 비밀·앱별 정책은 소비자 소유로 남긴다.

## 고정 결정

- [ADR-015](../adr/015-common-shared-systems-scope.md)가 이 task의 구조적 정본이다.
- [범위 재점검](../plan/common-scope-recheck-2026-09-07.md)은 영역별 책임·경계·후속 task의 evidence다.
- 모든 코드·문서·라이브러리의 라이선스는 GPL-3.0-or-later 기준을 유지한다. npm/PyPI에는 게시하지 않는다(ADR-014).
- 소비자 저장소는 수정하지 않고, 소비자 채택은 해당 저장소의 PR에서 수행한다.

## 구현 범위

1. ADR-015, 범위 재점검 문서와 AGENTS/architecture/packages 문구를 동기화한다.
2. UI·backend·OpenAPI·UX standards에서 인증 제외 문구를 공용 프리미티브/앱 소유 경계로 바꾼다.
3. T-011을 T-016 이후로 순서를 조정하고, 매니페스트의 앱/경로/workflow 경계를 명시한다.
4. T-312 Python 인증 프리미티브 task를 만들고 T-210/T-211 및 소비자 이관 task의 obsolete한 인증 제외 문구를 정리한다.
5. T-014와 CI-20/T-108에서 common `130xx`를 운영 대역처럼 해석하지 않도록 fixture 임시 포트와 ktdm 정본 경계를 명시한다.
6. docs/resume·tasks·journal·ADR 색인을 갱신한다.

## 범위 밖

- 로그인·JWT·세션·CSRF·RBAC 구현 코드 자체(T-312, T-201/T-210 후속).
- 인증 서버·사용자 DB·외부 IdP·운영 포트 등록·소비자 저장소 변경.
- npm/PyPI 게시와 소비자 실제 채택 PR.

## 예상 변경 파일

`AGENTS.md`, `docs/adr/015-common-shared-systems-scope.md`, `docs/plan/common-scope-recheck-2026-09-07.md`, `docs/architecture/README.md`, `docs/architecture/packages.md`, `docs/architecture/consumers.md`, `docs/architecture/canview-checklist.md`, `docs/standards/backend-stack.md`, `docs/standards/openapi.md`, `docs/standards/ui-contract.md`, `docs/standards/ux-guide.md`, `docs/tasks.md`, `docs/tasks/T-011-consumer-manifest-schema.md`, `docs/tasks/T-014-ports-130xx.md`, `docs/tasks/T-108-playwright-baseline.md`, `docs/tasks/T-210-ui-core.md`, `docs/tasks/T-211-ui-registry-channel-drift.md`, `docs/tasks/T-302-python-common-package.md`, `docs/tasks/T-306-public-api-key.md`, `docs/tasks/T-308-security-middleware.md`, `docs/tasks/T-311-python-release.md`, `docs/tasks/T-312-auth-core-primitives.md`, `docs/tasks/T-463-weather-shell-panels-forms-login.md`, `docs/tasks/T-484-pinvi-api-adoption.md`, `docs/tasks/T-485-concierge-api-adoption.md`, `docs/tasks/T-486-docker-manager-api-adoption.md`, `docs/plan/design-brief.md`, `docs/resume.md`, `docs/journal.md`, `docs/adr/README.md`.

## 수용 기준

- common의 현재 정본 문서가 공용 위젯·토큰·코어·로그인 계층과 소비자 소유 경계를 같은 말로 설명한다.
- 인증 제외 문구를 찾았을 때 “공용 프리미티브/로그인 UI는 common, 서버·저장소·비밀·앱 정책은 소비자”라는 설명으로 연결되며, 역사 문서와 현재 정본이 구분된다.
- T-011, T-312와 후속 task의 상태·선행·요약이 `tasks-rule.md`와 일치하고 T-011의 manifest 초안 개수·앱 대응표가 일치한다.
- CI-20/T-014/T-108이 common 운영 포트 등록을 요구하지 않고 fixture 임시 설정으로 명시한다.
- `python3 -B -X utf8 tools/validate_plan.py`, `python3 -B -X utf8 tools/validate_document_links.py`, `git diff --check`가 성공한다.
- 두 독립 reviewer가 immutable candidate를 각각 검토하고 모든 P0/P1 finding이 disposition된다. 소비자 빌드·e2e는 `NOT_RUN(소비자 저장소 미수정)`으로 기록한다.

## 검증 명령

```bash
python3 -B -X utf8 tools/validate_plan.py
python3 -B -X utf8 tools/validate_document_links.py
python3 -B -X utf8 tools/check_prod_redaction.py
git diff --check
```

## evidence

- 변경 전 기준선: `c8f81be7e70abbce892417eb0247a5d2337f31`.
- reviewer A/B의 독립 report와 post-fix report를 `docs/reviews/adversarial/`에 추가한다.
- 소비자 저장소 변경·빌드·e2e·registry 게시: `NOT_RUN(공용 범위 동기화 task의 범위 밖)`.

## rollback 또는 release 차단 조건

- 문서·task만 변경하므로 candidate commit을 revert하면 원복한다.
- ADR·architecture·task 간 충돌, 미해결 P0/P1 finding, 검증 실패가 있으면 T-011 또는 T-312로 진행하지 않는다.
