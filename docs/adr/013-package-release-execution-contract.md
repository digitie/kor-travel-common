# ADR-013: 패키지 릴리스 순서·호환 범위·검증 소비자 계약

- 상태: partially superseded by ADR-014
- 날짜: 2026-09-06
- 근거 문서: 브리프 D-09·D-11·D-15·D-16·D-18·D-31, UI 조사 §3.1~§3.4; T-013 독립 적대적 리뷰의 릴리스 교착·누락, AGENTS의 단방향 의존·승인·NOT_RUN 경계
- Supersedes: ADR-005의 "같은 minor" 해석, ADR-007의 helper 의존 시점, ADR-010의 고정 smoke 대상 해석을 부분 대체

## 컨텍스트

초기 계획에는 0.1 발행 전에 다음 minor 코드를 넣는 순서, pinvi 승인과 실제 라이선스 반영의 역순, 후속 Python 모듈의 발행 누락이 있었다. 패키지 번호를 독립적으로 올린다는 원칙과 UI의 tokens peer 설명도 두 가지로 해석됐다. 이 ADR은 초기 후보 계약을 실행 가능한 순서로 구체화한다. 아직 발행한 패키지는 없다.

## 결정

1. 같은 패키지의 다음 minor 구현은 이전 minor 정식 릴리스 완료를 선행으로 한다. UI T-205는 T-212 후, Python T-306·T-307은 T-310 후다. 외부 검증 대기 중에는 다른 패키지·도구의 독립 작업을 선택한다. 기존 태그를 이동하거나 서로 다른 내용물을 같은 버전으로 발행하지 않는다.
2. tokens·ui·py의 버전 숫자는 동기화하지 않는다. UI의 "같은 minor"는 **호환성을 검증한 tokens 한 minor 범위에 peer를 제한한다**는 뜻이다. UI 0.1과 0.2 모두 tokens `~0.1.0`을 기준으로 검증한다. 새 토큰 계약이 필요하면 해당 토큰 minor 발행을 먼저 task로 등록한다.
3. Base UI의 overlay 엔진과 `useRender` 합성 helper를 구분한다. native 요소도 helper를 사용할 수 있으므로 T-201부터 `@base-ui/react` peer와 개발용 설치를 선언한다. T-203은 깨끗한 tarball 설치에서 helper 해석을 검증하고, T-206은 이미 선언한 peer 위에 overlay를 추가한다.
4. 패키지를 설치하는 consumer-smoke는 권리 gate를 닫은 소비자의 immutable pin만 선택한다. tokens는 map·weather, UI는 map·pinvi(L6 실제 반영 후) 또는 airport다. 기존 pinvi 진단을 수행해도 L6 전 common 설치는 하지 않으며, 설치 없는 진단·skip은 필수 smoke 성공을 대신하지 않는다.
5. T-020은 사용자 결정과 pinvi PR 요청 문서를 완료한다. T-420이 실제 반영·merge·권리 정합 evidence를 닫아야 L6의 소비·추출 gate를 해제한다. pinvi UI 채택은 T-422a(0.1) → T-422b(0.2)로 분리하고 부모 T-422는 인계 요약만 소유한다.
6. Python 0.1은 export·health·time·quality다. 0.2는 T-306~T-308의 2·3차 모듈이며 T-311이 발행한다. request-id를 소비하는 task는 T-311 이후 `py-v0.2.0`을 설치한다. 드리프트 워크플로는 T-309가 준비돼야 해당 릴리스 검증에 사용한다.

## 대안 검토

- 릴리스 branch를 별도로 유지하면 병행 구현은 가능하지만 단독 유지자·순차 실행에는 관리 비용이 크다. 이전 minor 발행을 명시 선행으로 두는 최소 구조를 택한다.
- UI와 tokens 번호를 맞추기 위한 내용 변경 없는 tokens 0.2 발행은 독립 버전의 목적과 맞지 않는다. 검증된 peer 범위를 유지한다.
- L6 이전 pinvi 설치를 임시 예외로 허용하지 않는다. 이미 정한 airport 대체 경로를 smoke에도 일관되게 적용한다.

## 결과

릴리스 외부 대기 때문에 같은 패키지 후속 구현은 늦어질 수 있다. 다른 독립 task를 고를 수 있고, 버전별 내용물과 검사 대상을 숨은 branch 규칙 없이 재현할 수 있다. 승인되지 않은 소비자는 대체 경로를 차단하지 않는다.

## 후속·적용 위치

[통합 계획](../plan/integration-plan.md), [패키지 계약](../architecture/packages.md), [릴리스 runbook](../runbooks/release.md), T-010·T-109·T-201·T-205·T-206·T-212·T-213·T-306·T-307·T-310·T-311·T-420·T-422a·T-422b와 Python 소비자 task에 반영한다. 공개 import facade의 소유·wheel 검증은 T-302의 수용 기준에서 확정한다.

후속: [ADR-014](014-common-implementation-without-registry-publishing.md)이 npm/PyPI 미게시·이름 확정과 common 후보 보존 후 구현 순서를 결정한다. 대체 범위 밖의 계약은 유지한다.
