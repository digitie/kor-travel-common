# T-436 transport: guard 호출 SHA를 채택 커밋으로 갱신

- 상태: BLOCKED
- 우선순위: P2
- Gate: 소비자 CI(공통 프론트엔드 정책)
- 선행: T-024
- 소유 저장소: kor-travel-transport
- 병렬: 묶음 B(T-417·T-424·T-436·T-467·T-474 서로 독립)

출처는 [공통화 재조사·계획(2026-11-17)](../plan/commonization-plan-2026-11-17.md)의 §4.1(K-01)이다. 근거 위치(file:line)와 차이 분석은 그 문서가 정본이며 여기서 반복하지 않는다.

## 목표

transport의 guard 호출을 T-024가 지정한 채택 커밋으로 올린다. ADR-019의 권고안이 채택됐다면 그 뒤로 common main의 정책·Node/npm 변경이 이 저장소의 CI를 깨지 않는다. 벤더한 패키지는 바꾸지 않는다.

## 고정 결정

- 호출 SHA는 '최신'이 아니라 T-024가 지정한 채택 커밋 하나다. 그 커밋에서 이 저장소가 걸리는 규칙은 T-024의 evidence에 미리 적혀 있다.
- 호출 SHA와 `common-ref` 입력은 같은 40자리 값이다.
- 이 PR은 재vendor를 하지 않는다. 그 커밋의 정책이 지금 벤더한 버전과 같아야 통과한다. 다르면 재vendor를 같은 PR에 넣는다.
- 이 저장소는 다른 팀이 유지한다. 시점은 그 팀이 정한다.

## 구현 범위

1. `.github/workflows/ci.yml`(PR을 막는 호출)과 `.github/workflows/common-frontend-policy.yml`의 호출 SHA와 `common-ref`를 올린다.
2. T-024의 evidence가 이 저장소에 대해 적은 규칙 위반이 있으면 같은 PR에서 고친다.

## 범위 밖

벤더 패키지 버전, 부품 채택.

## 대상 저장소·브랜치·PR·되돌리기

- 저장소 `digitie/kor-travel-transport`. 이 저장소(common)의 작업이 아니다. 그 저장소의 규칙·리뷰·CI를 따른다.
- 브랜치: `docs/…` 또는 `agent/<agent>-<task>` 형식의 작업 브랜치, `origin/main`에서 분기. PR 1개.
- 되돌리기: `git revert <merge-sha>` 1회.
- 그 저장소의 backlog에는 이 task를 가리키는 포인터 한 줄만 두고 수용 기준을 복제하지 않는다.

## 예상 변경 파일

예정 경로는 존재·실행 증거가 아니다.

```text
.github/workflows/ci.yml, .github/workflows/common-frontend-policy.yml
```

## 수용 기준

- [ ] guard job(두 프론트 항목)가 새 호출 SHA로 통과한다.
- [ ] 호출 SHA와 `common-ref`가 같은 값이고 T-024가 지정한 커밋이다.

## 검증 명령

```bash
gh pr checks <PR>
```

## evidence

PR의 check 결과. common의 지연 보고에 새 ref가 보이는지는 common 쪽에서 확인한다.

## rollback·release 차단 조건

- `git revert` 1회로 옛 호출 SHA로 돌아간다(그 판은 다시 `main` 정책을 읽는다).
