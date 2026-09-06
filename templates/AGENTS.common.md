<!-- kor-travel-common AGENTS 공통 절 시작 · 판 2026-09 · 정본 templates/AGENTS.common.md · 규약 docs/standards/agent-conventions.md §2 -->
<!-- 이 마커와 "공통 절 끝" 마커 사이는 common이 배포하는 문구이며 저장소는 바꾸지 않는다. 저장소 고유 규칙(목표·식별자·환경·도메인 DO NOT·포트·검증 명령)은 끝 마커 뒤 로컬 절에 둔다. -->

## A. 작업 원칙

### Think Before Coding

- 요청이 모호할 때는 해석을 조용히 정하지 말 것
- 중요한 가정은 숨기지 말고 드러낼 것
- 해석에 따라 구현 방향이 크게 달라지면 그 차이를 먼저 표면화할 것
- 안전하게 진행하기 어려울 정도로 혼란스러우면 추측하지 말고 확인할 것

### Simplicity First

- 요청을 완전히 해결하는 최소한의 코드만 작성할 것
- 요청되지 않은 기능을 추가하지 말 것
- 일회성 용도를 위해 추상화를 만들지 말 것
- 구체적인 필요 없이 설정 가능성이나 유연성을 늘리지 말 것
- 구현이 문제에 비해 커졌다고 느껴지면 줄일 것

### Surgical Changes

- 요청을 처리하는 데 필요한 코드만 변경할 것
- 작업이 요구하지 않으면 주변 로직까지 다시 쓰지 말 것
- 관련 없는 코드의 포맷, 이름, 스타일을 건드리지 말 것
- 사용자가 더 넓은 변경을 원한 것이 아니라면 기존 패턴을 맞출 것
- 관련 없는 문제를 발견하면 패치에 섞지 말고 따로 언급할 것

### Goal-Driven Execution

- 모호한 요청을 구체적이고 검증 가능한 결과로 바꿀 것
- 버그 수정은 재현 없이 바로 신뢰하지 말 것
- 리팩터링은 동작 보존을 전제로 전후 기대를 확인할 것
- 넓고 막연한 점검보다 목적이 분명한 검증을 선호할 것
- 완전한 검증이 불가능하면 무엇이 아직 미검증인지 밝힐 것

### Practical Bias

- 비단순 작업에서는 성급함보다 신중함을 우선할 것
- 변경 내역은 리뷰 가능한 범위와 요청 범위에 가깝게 유지할 것
- 아주 단순하고 명백한 한 줄 작업은 과하게 무겁게 다루지 말 것

## B. Ruthless Review

- 코드가 동작한다는 이유만으로 검증이 끝났다고 여기지 말 것
- 적대적 리뷰어로 세워 숨겨진 취약점과 부작용을 집요하게 찾아낼 것
- 당연하다고 믿은 가정을 의심하고 코드가 실패하는 시나리오를 찾을 것
- 숨겨진 부작용과 취약점이 소명되기 전까지는 완료로 보지 말 것

## C. 문서 언어 정책

모든 Markdown 문서, 코드 주석, docstring, 사용자에게 보이는 문자열은 한국어로 쓴다. 공식 API 필드명, 코드 식별자, 명령어, URL, 패키지명, 라이브러리·제공자 원문, 환경변수, 표준 키워드(ADR·CHANGELOG 절 제목·SemVer 라벨)처럼 그대로 보존해야 하는 값만 영어를 유지한다. 커밋 제목은 Conventional Commits 영어 type 뒤에 한국어 문장을 쓴다.

예외는 세 가지뿐이다.

1. `.claude/`, `.agents/`, `.codex/`, `.opencode/` 아래의 벤더링된 upstream agent/skill 원문(동기화 충실성을 위해 원문 유지).
2. 원 프로젝트에서 가져온 원칙 소제목(Think Before Coding 등).
3. 인용한 reference 원문 — 원문을 유지할 때는 한국어 적용 메모를 반드시 함께 둔다. `design.md`/`DESIGN.md` 본문은 한국어다.

## D. 문서 정본과 우선순위

지시가 충돌하면 다음 순서를 따른다.

1. 사용자 요청
2. 이 `AGENTS.md`(공통 절 + 로컬 절)
3. accepted ADR
4. `SKILL.md`와 `docs/architecture/` 정본
5. 선택한 상세 task(`docs/tasks/T-NNN-*.md`)
6. 그 밖의 `docs/` 문서(공통 규칙은 kor-travel-common `docs/standards/`, 환경은 `docs/dev-environment.md`)
7. 코드와 테스트
8. review·journal 등 역사 기록
9. 최소한의 되돌릴 수 있는 가정

구조적 결정은 ADR, 현재 설계는 architecture, 저장소 간 공통 규칙은 kor-travel-common의 standards, 실행 범위와 수용 기준은 task, 반복 절차는 runbook에 둔다. 같은 규범을 두 문서에 복제하지 않는다. `SKILL.md`는 작업별 문서 라우터이며 도메인 DO NOT 목록만 추가로 가질 수 있다. `CLAUDE.md`는 이 파일을 가리키는 포인터이며 이 파일과 상충하면 `CLAUDE.md`를 고친다.

## E. 문서 읽기 정책

`AGENTS.md`는 모든 작업에 적용되는 짧은 규칙의 정본이고 `docs/README.md`는 상세 문서 라우터다. 문서 전체를 선제적으로 읽지 말고 아래 단계만 따른다.

### 반드시 참조

1. 이 `AGENTS.md`
2. `docs/README.md` — 문서 분류와 정본 위치
3. `docs/resume.md` — 현재 상태, 다음 작업, 차단 조건
4. 구현 task가 정해졌다면 해당 상세 task 한 파일

task를 고르는 작업일 때만 `docs/tasks.md`를 읽는다. 이미 task가 지정됐다면 전체 backlog를 다시 읽지 않는다.

### 필요할 때만 참조

| 상황 | 먼저 읽을 문서 | 다음 문서 |
|---|---|---|
| 구조·책임·데이터 흐름 변경 | `docs/architecture/README.md` | 그 문서가 가리키는 상세 설계 한두 개 |
| branch·검증·PR·merge | `docs/runbooks/agent-workflow.md` | 실패했을 때만 `agent-failure-patterns.md` |
| 개발 환경·worktree·빌드 | `docs/dev-environment.md` | 해당 패키지의 README |
| 공통 토큰·UI·OpenAPI·버전 규칙 | kor-travel-common `docs/standards/README.md` | 해당 규칙 문서 하나 |
| 기존 결정을 변경 | `docs/adr/README.md` | 관련 ADR 본문만 |
| 문서·task·journal 유지 | `docs/runbooks/documentation-maintenance.md` | 필요한 기록 문서만 |

### 특수한 경우에만 참조

- `docs/reviews/`: 적대적 리뷰를 수행하거나 과거 finding을 추적할 때만 읽는다.
- `docs/journal.md`·`docs/archive/`: 과거 작업의 원인·명령·결과를 추적할 때만 `rg`로 검색한다.
- `docs/adr/` 전체: 구조적 결정의 이력을 감사할 때만 읽는다. 보통은 색인에서 관련 ADR 하나만 고른다.
- `docs/tasks/` 전체와 `docs/tasks-done.md`: backlog 감사나 의존성 재설계 때만 읽는다.
- 형제 저장소 원본과 kor-travel-common `docs/survey/`: 계약·근거를 검증할 때만 연다.

### 토큰 절약 규칙

- 인덱스 → 관련 상세 문서 → 필요한 절의 순서로 점진적으로 읽는다.
- `rg`로 제목·식별자·링크를 먼저 찾고, 관련 없는 긴 문서나 과거 로그를 통째로 읽지 않는다.
- 한 문서에서 답이 확인되면 단순 배경 링크를 연쇄적으로 따라가지 않는다.
- review·journal·ADR는 역사 기록이다. 현재 요구사항은 accepted ADR, architecture 정본과 열린 task에서 확인한다.
- 문서가 충돌하면 조용히 선택하지 말고 정본 우선순위와 충돌 위치를 밝힌다.

## F. 절대 하지 말 것 (공통)

1. `main`(trunk)에 직접 push하지 않는다. 모든 변경은 branch와 PR을 거친다.
2. 비밀·자격증명·`.env`·`*.local.md`·운영 호스트 주소·내부 접속정보를 커밋하지 않는다.
3. `git add -A`와 `git add .`을 사용하지 않는다. 파일을 경로별로 명시해 stage한다.
4. 실행하지 못한 gate를 통과로 표시하지 않는다. 0 test·skip을 pass로 집계하지 않으며, 명령을 적었다는 사실은 실행·성공의 증거가 아니다. 미실행은 `NOT_RUN(사유)`로 남긴다.
5. 한 사실을 두 곳에서 독립적으로 선언하지 않는다. 정본 하나를 정하고 나머지는 링크한다.

kor-travel-common 소비자 권고(SHOULD): `@main`·branch 참조로 패키지·워크플로를 설치하지 않는다(태그 또는 SHA). 패키지에서 온 `tokens.css`·컴포넌트 사본을 앱에서 고치지 않고 오버라이드 파일 또는 common PR로 해결한다. 도메인 DO NOT은 `SKILL.md` §4 로컬 목록에 둔다.

## G. 완료와 push

1. 변경 범위에 맞는 검증 계층(문서 검증 → 단위 → 빌드·타입 → e2e → 배포 스모크)만 실행하고 결과·명령·exit code를 남긴다.
2. 비단순 변경은 전문 영역이 다른 리뷰어 서브에이전트 2인의 독립 적대적 리뷰(full 또는 light)를 거치고 finding을 `FIXED`/`REJECTED_WITH_EVIDENCE`/`DEFERRED`로 disposition한 뒤 영향받은 검증을 다시 실행한다.
3. H의 기록 갱신 규칙에 따라 직접 관련된 기록만 갱신한다.
4. push 전 보안 감사: `git status`로 사용자·로컬 파일 혼입 확인 → `git diff --staged` 전체를 직접 읽기 → `api[_-]?key|secret|password|passwd|token|pbkdf2_sha256|AKIA[0-9A-Z]{16}|BEGIN [A-Z ]*PRIVATE KEY` grep → `.env.example`은 placeholder만인지 확인 → 신규 파일이 비밀 운반체가 아닌지 점검 → 인증·세션·권한을 바꿨다면 보안 리뷰를 추가로 요청.
5. PR 본문에는 task와 목적 / 통과한 gate와 정확한 명령 / 리뷰어 2인의 영역·report·disposition / 실패·미실행 검증과 남은 위험 / evidence 위치와 digest / rollback 방법을 적는다.
6. 필수 check가 있는 저장소는 CI green, 리뷰 gate, 미해결 `P0`/`P1` 없음이 확인되기 전 merge하지 않는다. CI가 없는 저장소는 로컬 gate 결과를 PR 본문에 기록하고 `docs/runbooks/branch-protection.md`에 required check가 등록될 때까지 "미적용"을 명시한다.

## H. 기록 갱신

변경과 직접 관련된 기록만 갱신한다.

- 구조적 결정이 생기면 새 ADR과 `docs/adr/README.md` 색인(다음 후보 번호 갱신).
- 현재 상태나 다음 한 작업이 바뀌면 `docs/resume.md`.
- 작업 재현 정보(명령·결과·도구 fallback·미실행 검증·소비 저장소 상태)가 필요하면 `docs/journal.md` 최상단. 기존 항목은 사실 오류 correction 외에 고치지 않는다.
- task 상태·acceptance·evidence가 바뀌면 `docs/tasks.md`와 상세 task, 완료는 `docs/tasks-done.md`.
- 사용자 가시 변경이면 `CHANGELOG.md`.

journal·resume가 220 KiB에 근접하면 `docs/archive/` 분리 규약(kor-travel-common `docs/standards/agent-conventions.md` §9)을 따른다.

## I. 개발 환경·worktree·CodeGraph 진입점

- 정본 OS·셸·경로·worktree 프로필(고정 또는 임시)은 이 저장소의 `docs/dev-environment.md`와 ADR이 선언한다. 이 절은 OS를 규정하지 않는다.
- 불변 조건: 같은 branch를 두 worktree에서 checkout하지 않는다 · trunk는 사람 전용이며 branch 이름은 `agent/<agent>-<task>`(저장소가 다른 접두를 쓰면 로컬 절이 정본) · worktree마다 CodeGraph 수명주기를 따른다(최초 `codegraph init -i`, 전환·pull·merge 뒤 `sync`, 분석 전후 `status`; 없으면 `rg`·compiler·test로 대체하고 한계를 기록) · 임시 worktree는 merge 또는 abandon 뒤 활성 프로세스·미커밋 변경을 확인하고 `git worktree remove`·`git worktree prune`으로 제거한다.
- 리뷰 기준선은 이동 가능한 branch가 아니라 commit object-only(`git show`/`git diff`) 또는 `git worktree add --detach`로 만든다.

<!-- kor-travel-common AGENTS 공통 절 끝 · 아래부터 로컬 절 -->
