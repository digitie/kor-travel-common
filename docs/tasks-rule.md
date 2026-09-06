# tasks-rule.md — task 문서 작성·유지 규칙

이 문서는 docs/tasks.md, docs/tasks-done.md와 docs/tasks/ 상세 파일의 작성 규약 정본이다. PR·리뷰·병렬 실행 절차는 [agent workflow](runbooks/agent-workflow.md)를 따른다. 기계 검사는 `python3 -B -X utf8 tools/validate_plan.py`가 수행하며, 이 문서의 문법 규칙은 그 검사기가 요구하는 형식과 일치해야 한다.

## 1. 문서 역할

| 문서 | 역할 |
|------|------|
| docs/tasks.md | 열린 task의 요약 backlog와 critical path |
| docs/tasks-done.md | 완료·종료 task의 newest-first archive |
| docs/tasks/T-NNN-*.md | task 하나의 scope·수용 기준·검증·evidence |
| docs/resume.md | 현재 진척과 다음 한 작업 |

## 2. task ID

- T-001~T-099: 저장소 기반·문서 규약·검증 도구·CI·릴리스 파이프라인
- T-100~T-199: 디자인 토큰·스타일 배포·UX 규약 산출물
- T-200~T-299: React UI 패키지(프리미티브·컴포넌트·shadcn registry)
- T-300~T-399: Python 백엔드 공통 패키지·OpenAPI 규약 산출물
- T-400~T-499: 소비 앱 이관(버전 정렬·Tailwind v4 전환·common 채택) — 앱별 하위 범위는 §2.1
- T-500~T-599: 릴리스·소비자 검증·운영·회수

이미 참조된 ID는 재번호하지 않는다. 하위 작업은 `T-NNNa` 형식으로 둔다.

### 2.1 소비 앱 이관 ID 대역

| 대역 | 앱 |
|---|---|
| T-400~T-409 | 공통 이관 절차·측정·회귀 fixture |
| T-410~T-419 | kor-travel-map admin |
| T-420~T-429 | PinVi web admin(사용자 웹·모바일은 별도 판단) |
| T-430~T-439 | kor-travel-airport admin |
| T-440~T-449 | kor-travel-geo ui |
| T-450~T-459 | kor-travel-concierge frontend |
| T-460~T-469 | kor-travel-weather admin |
| T-470~T-479 | kor-travel-docker-manager frontend |
| T-480~T-489 | Python 백엔드 소비(앱별 1 ID, 하위 항목은 `a`~`z` suffix) |

앱 대역(T-410~T-479)에는 버전 정렬·lockfile·CI·토큰·UI 채택만 둔다. Python 공통 모듈 채택은 반드시 T-480~T-489에 둔다.

## 3. 상태

상세 task 상단의 상태는 `READY`, `BLOCKED`, `IN_PROGRESS`, `DONE` 중 하나를 사용한다. 완료된 task는 docs/tasks-done.md로 요약을 옮기고 상세 파일은 유지한다. 외부 저장소의 PR merge·권리 확인·registry 권한 같은 외부 대기는 `BLOCKED`로 유지하고 상세 파일의 `외부 선행` 항목에 적는다.

## 4. 요약 entry

docs/tasks.md와 docs/tasks-done.md의 요약 표는 정확히 5열이며 첫 열은 상세 파일 link다.

```text
| [T-NNN](tasks/T-NNN-slug.md) | READY | P1 | 짧은 제목 | T-001, T-002 |
```

- 2열 상태, 3열 우선순위, 4열 제목, 5열 선행(ID 목록 또는 `없음`)은 상세 파일의 값과 글자 단위로 일치해야 한다.
- docs/tasks.md 본문에는 `N개의 상세 작업`이라는 문구가 정확히 한 번 있어야 하며 N은 docs/tasks/T-*.md 파일 수와 같아야 한다.
- 상세 수용 기준과 명령을 summary에 복제하지 않는다.

## 5. 상세 task 필수 항목

파일명은 `T-NNN-slug.md`(하위 작업은 `T-NNNa-slug.md`), H1은 정확히 하나이며 `# T-NNN 제목` 형식이다. 본문 상단에는 다음 metadata 줄을 각각 정확히 한 번 둔다.

```text
- 상태: READY
- 우선순위: P1
- Gate: 문서 검증·소비자 빌드
- 선행: T-001, T-002
```

- `상태`는 §3의 네 값, `우선순위`는 `P0`~`P3`, `선행`은 `없음` 또는 쉼표로 구분한 task ID 목록만 허용한다. 외부 조건은 `선행`이 아니라 별도 `외부 선행` 줄에 적는다.
- `Gate`는 이 task가 닫아야 하는 검증 계층을 한 줄로 적는다(예: `문서 검증`, `패키지 빌드·tarball 설치`, `소비자 빌드·e2e`, `2인 리뷰`).
- 코드 블록 안의 예시 metadata는 검사 대상이 아니다.

각 상세 파일은 목표, 고정 결정(관련 ADR·규약 문서 링크), 구현 범위, 범위 밖, 예상 변경 파일, 수용 기준, 검증 명령, evidence, rollback 또는 release 차단 조건을 포함한다. 소비 앱 이관 task는 대상 저장소·브랜치·PR 위치와 되돌리기 방법을 반드시 적는다.

`READY` 또는 `DONE` task의 선행은 모두 `DONE`이어야 한다. 선행이 미완료면 `BLOCKED`로 둔다.

## 6. 완료 처리

모든 수용 기준과 검증을 확인하고 비단순 변경이면 전문 리뷰어 서브에이전트 2인 gate를 통과한 뒤 docs/tasks-done.md에 newest-first로 추가한다. 상세 파일의 상태를 `DONE`으로 바꾸고 docs/tasks.md의 요약 행을 docs/tasks-done.md로 옮긴다. 요약 표는 5열 고정이므로 완료 날짜와 PR 번호는 4열 제목 뒤 괄호에 적는다(예: `문서 골격 (2026-09-06, PR #1)`). 실행하지 못한 검증은 `NOT_RUN(사유)`로 남기고 0 test·skip을 통과로 집계하지 않는다. 명령을 적었다는 사실은 실행·성공의 증거가 아니다. 현재 상태가 바뀌면 docs/journal.md와 docs/resume.md도 갱신한다. 실패한 검증이나 미해결 P0/P1 finding을 남긴 채 `DONE`으로 바꾸지 않는다.

리뷰를 수행한 경우 기존 리뷰 문서에 append하지 않고 [review archive](reviews/README.md) 규칙에 따라 새 report를 만든다.
