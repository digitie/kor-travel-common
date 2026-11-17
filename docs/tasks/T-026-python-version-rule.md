# T-026 Python 공통 패키지의 버전 올림 규칙

- 상태: READY
- 우선순위: P2
- Gate: 문서 검증·python-package
- 선행: 없음
- 소유 저장소: kor-travel-common
- 병렬: 묶음 A

출처는 [공통화 재조사·계획(2026-11-17)](../plan/commonization-plan-2026-11-17.md)의 §2.1·§4.3(K-04)이다. 근거 위치(file:line)와 차이 분석은 그 문서가 정본이며 여기서 반복하지 않는다.

## 목표

소비자 핀 세 가지(`aa232ad`·`c289b46`·wheel 원천 `b4f7f3d`)는 `packages/py` 내용이 같은데 버전은 어느 커밋에서나 `0.1.0.dev0`이다. 버전으로 내용을 구분할 수 없다. `packages/py`가 바뀔 때 버전을 올리는 규칙을 문서로 정한다.

## 고정 결정

- 소비자의 실제 선언은 40자리 커밋 핀이다(P·M·W·T의 `pyproject.toml`). [backend-stack](../standards/backend-stack.md) BE-29는 `@py-vX.Y.Z` 태그 선언을 규정하지만 py 태그는 하나도 없다. 이 task는 그 불일치를 문서에 사실대로 적고, 태그·wheel 발행 절차 자체는 바꾸지 않는다.
- 새 CI 강제를 넣지 않는다. 규칙은 runbook과 CHANGELOG 절이다.

## 구현 범위

1. [release](../runbooks/release.md)에 'Python 소스가 바뀌는 PR은 `pyproject.toml` 버전의 dev 번호를 올리고 CHANGELOG의 Python 절에 한 줄을 적는다'를 추가한다.
2. [backend-stack](../standards/backend-stack.md) §9(BE-29·BE-30)에 현재 소비 방식(커밋 핀, Manager는 hash 고정 wheel, 태그 없음)을 '현황'으로 적는다. 규칙 문장의 변경은 T-027의 범위와 겹치지 않게 현황 주석만 둔다.
3. 다음 Python 변경(T-313)이 이 규칙의 첫 적용이 되도록 T-313 상세에 연결한다.

## 범위 밖

버전 자동 검사 도구, 태그 발행, 소비자 핀 정렬 PR.

## 예상 변경 파일

예정 경로는 존재·실행 증거가 아니다.

```text
docs/runbooks/release.md
docs/standards/backend-stack.md
docs/journal.md
```

## 수용 기준

- [ ] runbook에 규칙 문장과 예시(`0.1.0.dev0` → `0.1.0.dev1`)가 있다.
- [ ] 문서 검증이 오류 0이다.

## 검증 명령

```bash
python3 -B -X utf8 tools/validate_document_links.py && git diff --check
```

## evidence

PR diff. 첫 적용은 T-313의 PR에서 확인한다.

## rollback·release 차단 조건

- 문서 전용. `git revert` 1회.
