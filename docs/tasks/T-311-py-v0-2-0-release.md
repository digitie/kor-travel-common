# T-311 Python 0.2 모듈 rc 검증·wheel 발행

- 상태: BLOCKED
- 우선순위: P1
- Gate: wheel 설치·소비자 스모크·2인 리뷰
- 선행: T-308, T-309, T-310
- 외부 선행: map-api·weather-api의 rc 검증을 맡을 담당자·실행 환경. rc 결과는 착수 선행이 아니라 정식 발행 gate다. 추가 소비자는 L6/L8 해제 후에만 포함한다.

## 목표

T-306~T-308에서 구현한 settings·db·API key·request-id·metrics 및 3차 API/HTTP/Dagster/testing 모듈을 `py-v0.2.0`으로 발행한다. 구현 완료와 소비 가능한 태그 존재를 구분한다.

## 고정 결정

[ADR-013](../adr/013-package-release-execution-contract.md), [패키지 계약](../architecture/packages.md), [backend-stack](../standards/backend-stack.md), [release](../runbooks/release.md)를 따른다. 기존 `py-v0.1.0` 태그·자산은 변경하지 않는다.

## 구현 범위

1. 0.1 대비 export·extras·import 경로·미들웨어 기본값을 대조하고 CHANGELOG `### Breaking`과 이관 절에 변경/변경 없음 및 근거를 기록한다.
2. `0.2.0-rc.1` wheel을 빌드해 core-only·api·db·http·dagster·testing 설치 조합과 Python 지원 매트릭스를 검증한다. request-id 공개 경로·기본 `trust_incoming=True`와 앱 옵션 `False`를 설치본에서 확인한다.
3. map-api·weather-api 담당자에게 별도 draft 검증 PR을 요청한다. 현재 서비스 계약을 보존하는 opt-in 설정으로 import·health·OpenAPI drift·request-id·metrics를 검증한다. 소비자 변경은 해당 저장소 task가 소유한다.
4. 두 리뷰어·소비자 검증을 통과하면 `py-v0.2.0` wheel·SHA256SUMS와 이관 문서를 발행한다. 실패하면 새 rc 번호를 사용한다.

## 범위 밖

소비자 정식 채택 merge(T-483~T-486), 인증·앱 도메인, 공개 PyPI 게시(T-507).

## 예상 변경 파일

Python 패키지 버전·lock, `CHANGELOG.md`, 릴리스 evidence·통합 지도 입력·`docs/journal.md`. 외부 소비자 검증 PR은 해당 저장소가 소유한다.

## 수용 기준

- rc와 정식 wheel의 실제 모듈 목록이 위 범위·공개 계약과 일치한다.
- 고지 파일·`py.typed`·SHA256SUMS와 wheel 설치 후 공개 import 검사가 통과한다.
- Python 지원·extras·OpenAPI drift와 두 소비자 rc 검증 결과가 실제 로그·commit으로 남는다.
- 리뷰 P0/P1이 원 reviewer 재확인으로 닫히며 실행하지 않은 조합은 NOT_RUN으로 남고 필수이면 발행을 차단한다.

## 검증 명령

```bash
uv sync --locked --all-extras
uv run pytest
uv build
sha256sum -c SHA256SUMS
```

패키지 디렉터리에서 실행하며 exact 스크립트·wheel 설치 명령은 T-302 결과와 release runbook을 따른다. Git Bash에서 동일.

## evidence

rc·정식 tag SHA, wheel digest, extras별 import·시험 수, 두 소비자 PR·drift 결과, 두 리뷰어 report. 현재 NOT_RUN(선행 패키지·릴리스 미구현).

## rollback 또는 release 차단 조건

소비자는 이전 tag·lock으로 revert한다. 발행 태그를 이동·삭제하거나 같은 버전을 재발행하지 않는다. 실패는 새 rc 또는 후속 patch로 수정한다. 소비자 채택 task 완료를 이 rc 검증의 선행으로 삼지 않는다.
