# T-312 Python 공용 인증 코어 프리미티브

- 상태: BLOCKED
- 우선순위: P1
- Gate: Python 단위·계약 시험·2인 적대적 리뷰
- 선행: T-016, T-302

## 목표

`kortravelcommon`에 저장소·운영 서비스와 독립적인 인증 공용 코어를 추가한다. 비밀번호 해시, 세션/토큰 수명, CSRF 검증, JWT 검증, RBAC 정책 인터페이스를 재사용 가능한 순수 함수·타입·주입형 어댑터로 제공하고 소비자별 사용자 저장소와 정책을 계속 분리한다.

## 고정 결정

- [ADR-015](../adr/015-common-shared-systems-scope.md)가 인증 공용화와 서비스 경계의 정본이다.
- Python 패키지 구조·extras·지원 버전은 [backend-stack](../standards/backend-stack.md)과 T-302를 따른다.
- 키·비밀·사용자/세션 저장소·외부 IdP·rate limit 운영·라우트별 권한 결정은 소비자가 주입한다.
- GPL-3.0-or-later, npm/PyPI 미게시, 소비자 저장소 직접 수정 금지를 유지한다.

## 구현 범위

- 위협 모델과 API 계약(입력·출력·오류·만료·알고리즘 제한)을 먼저 고정한다.
- 표준 라이브러리 우선 비밀번호 해시/검증, 세션·CSRF 토큰 생성/검증, JWT 서명 알고리즘·키 resolver 인터페이스, RBAC policy protocol을 구현한다.
- 테스트에서 결정론적 clock·키 resolver·store double을 주입하고 replay·만료·alg 혼동·권한 거부를 검증한다.
- FastAPI route, DB model, 사용자 가입/복구, IdP 연동과 운영 비밀 로딩은 구현하지 않는다. 로그인 위젯은 T-214가 담당한다.

## 범위 밖

인증 서버·사용자/세션 DB·운영 비밀·외부 IdP·앱별 역할 매핑·rate limit 배포·로그인 화면(UI는 T-214)·소비자 저장소 변경.

## 예상 변경 파일

`packages/py/kor-travel-common/src/kortravelcommon/auth/`, `packages/py/kor-travel-common/tests/`, Python package metadata·문서·CHANGELOG. 실제 경로는 T-302 패키지 골격 확인 후 확정한다.

## 수용 기준

- 명시된 알고리즘·만료·오류 계약에 대한 단위·property 경계 시험이 통과한다.
- 비밀·저장소·외부 네트워크를 기본값으로 만들지 않으며 import graph가 consumer/provider를 끌어오지 않는다.
- 공개 API·문자열·라이선스·SPDX·CHANGELOG가 문서 계약과 일치하고 두 reviewer가 P0/P1 finding 없이 승인한다.
- 소비자 빌드·e2e는 `NOT_RUN(소비자 task에서 수행)`으로 기록한다.

## 검증 명령

```bash
uv run --project packages/py/kor-travel-common pytest packages/py/kor-travel-common/tests -k auth -q
python3 -B -X utf8 tools/check_spdx.py
python3 -B -X utf8 tools/validate_document_links.py
```

## evidence

T-016 완료 이후 T-302 패키지 골격, 위협 모델, 테스트 결과, reviewer report를 기록한다.

## rollback 또는 release 차단 조건

기본값이 서버·저장소·비밀을 도입하거나 인증 알고리즘 계약이 불명확하면 구현을 중단하고 ADR을 갱신한다. 패키지 변경은 태그·릴리스 전에 revert 가능해야 한다.
