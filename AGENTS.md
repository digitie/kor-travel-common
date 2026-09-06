# AGENTS.md

이 문서는 `kor-travel-common` 모든 작업에 적용되는 짧은 규칙의 정본이다. 확정 task: T-001(문서 확정) · 마지막 갱신: 2026-09-07. 결정 근거는 [설계 브리프](docs/plan/design-brief.md)의 결정 레지스터(D-xx)이며, 이 문서는 그 결정을 규칙 문장으로만 옮긴다.

## 1. 목표와 경계

kor-travel-common은 kor-travel 제품군의 UI·백엔드 공통 코드와 공통 규칙(색상 톤·UX·OpenAPI·PC/Mobile Web·라이브러리/플랫폼 버전 일치)을 정의하는 GPL-3.0-or-later 라이브러리다.

| 배포 단위 | 위치·이름 | 책임 |
|---|---|---|
| 디자인 토큰 | `packages/tokens` → npm 형식 `@kor-travel/tokens` | `--kt-*` 의미 토큰·`kt-` 유틸리티·프로필(admin/consumer)·다크 값·별칭 shim. 정본은 `tokens.css` |
| React UI | `packages/ui` → npm 형식 `@kor-travel/ui` | React 19 전용 프리미티브·컴포넌트와 마크업 계약(`data-slot`·testid) |
| Python 공통 | `packages/py/kor-travel-common` → Python 배포 이름 `kor-travel-common`, import `kortravelcommon` | OpenAPI export·health·time·quality 등 얇은 인프라 모듈. 인증은 범위 밖 |
| 규칙 문서 | `docs/standards/*` | 토큰·UX·반응형·프론트/백엔드 스택·UI 계약·OpenAPI·CI·라이선스·버전·에이전트 규약 |
| 템플릿·레지스트리·도구 | `templates/*`, `versions.json`, `tools/*.py` | 소비자 설정 조각, 버전 floor/recommended/exceptions, 검사 도구 |

소비자는 kor-travel-airport(Admin 포함)·kor-travel-concierge·kor-travel-docker-manager·kor-travel-geo·kor-travel-map·kor-travel-weather·pinvi(PinVi Admin 포함; 사용자 웹·모바일은 규칙만) 7개 저장소다. 의존 방향은 앱 → ui → tokens, 앱 → py 단방향이다. 소비자 목록·표면·채택 순서는 [consumers](docs/architecture/consumers.md)가 정본이다.

- 소비자 한 곳에 있다는 이유만으로 공통화하지 않는다. 승격 근거는 조사 문서의 사실(여러 앱의 관찰 또는 저장소 간 계약 비용)과 채택 PR의 실측이다.
- common은 앱 도메인 모듈, 지도 엔진(`maplibre-vworld-react`·`maplibre-vworld-js`), provider 라이브러리(`python-*-api`·`python-kraddr-base`), 인증 서비스(비밀번호·세션·CSRF·JWT·RBAC)를 갖지 않는다. 기존 공유 라이브러리와 중복하지 않고 의존만 한다.
- common 작업 중 소비자 저장소를 직접 수정하지 않는다. 소비자 변경은 해당 저장소의 이관 task와 PR로만 요청한다.
- 유지자는 한 명이며 공통 API·릴리스 담당과 소비자 통합 담당을 겸임한다(D-33). 긴급 패치는 앱에 임시 복사를 허용하되 종료 조건(common 릴리스 버전·제거 task)을 그 앱과 common task에 함께 기록한다.

## 2. 작업 원칙

kor-travel 공통 5원칙의 문구는 소비자 저장소와 글자 단위로 같다(`docs/survey/cross/docs-conventions.md` §1.4). 각 소제목 끝에 있는 추가 불릿은 canview 작업 원칙을 이 저장소에 맞게 더한 것이다.

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
- 사용자의 기존 변경과 dirty worktree를 보존하고, 충돌을 피할 수 없을 때만 사용자에게 알릴 것

### Goal-Driven Execution

- 모호한 요청을 구체적이고 검증 가능한 결과로 바꿀 것
- 버그 수정은 재현 없이 바로 신뢰하지 말 것
- 리팩터링은 동작 보존을 전제로 전후 기대를 확인할 것
- 넓고 막연한 점검보다 목적이 분명한 검증을 선호할 것
- 완전한 검증이 불가능하면 무엇이 아직 미검증인지 밝힐 것
- 설계·계약 변경은 검증 가능한 수용 기준(task·ADR)을 먼저 둘 것
- 도구·소비자 저장소·registry가 없어 실행하지 못한 gate를 통과로 표시하지 말고 `NOT_RUN(사유)`로 남길 것
- 구현보다 근거를 우선할 것. 확인된 사실, 후보 해석, 소비자 저장소 실측(빌드·e2e) evidence를 서로 다른 상태로 관리할 것

### Practical Bias

- 비단순 작업에서는 성급함보다 신중함을 우선할 것
- 변경 내역은 리뷰 가능한 범위와 요청 범위에 가깝게 유지할 것
- 아주 단순하고 명백한 한 줄 작업은 과하게 무겁게 다루지 말 것

### Ruthless Review

- 코드가 동작한다는 이유만으로 검증이 끝났다고 여기지 말 것
- 적대적 리뷰어로 세워 숨겨진 취약점과 부작용을 집요하게 찾아낼 것
- 당연하다고 믿은 가정을 의심하고 코드가 실패하는 시나리오를 찾을 것
- 숨겨진 부작용과 취약점이 소명되기 전까지는 완료로 보지 말 것

## 3. 문서 읽기 정책

`AGENTS.md`는 모든 작업에 적용되는 짧은 규칙의 정본이고, [docs/README.md](docs/README.md)는 상세 문서 라우터다. `CLAUDE.md`는 이 순서를 가리키는 포인터일 뿐 읽기 단계에 더하지 않는다. 문서 전체를 선제적으로 읽지 말고 아래 단계만 따른다.

### 반드시 참조

저장소 작업을 시작할 때 다음만 먼저 읽는다.

1. 이 `AGENTS.md`
2. [docs/README.md](docs/README.md) — 문서 분류와 정본 위치
3. [docs/resume.md](docs/resume.md) — 현재 상태, 다음 작업, 차단 조건
4. 구현 task가 정해졌다면 해당 `docs/tasks/T-NNN-*.md` 한 파일

task를 고르는 작업일 때만 [docs/tasks.md](docs/tasks.md)를 읽는다. 이미 task가 지정됐다면 전체 backlog를 다시 읽지 않는다.

### 필요할 때만 참조

| 상황 | 먼저 읽을 문서 | 다음 문서 |
|---|---|---|
| 배포 단위·의존 방향·소비자 채택 상태 변경 | [architecture/README.md](docs/architecture/README.md) | 그 문서가 가리키는 packages·style-delivery·consumers 중 한두 개 |
| branch·검증·PR·merge | [agent-workflow.md](docs/runbooks/agent-workflow.md) | 실패했을 때만 failure patterns |
| 개발 환경·패키지 빌드·Windows | [dev-environment.md](docs/dev-environment.md) | 패키지가 정해졌을 때만 [packages.md](docs/architecture/packages.md) |
| 규칙 산출물(토큰·UX·반응형·UI 계약·OpenAPI·버전·스택) | [standards/README.md](docs/standards/README.md) | 해당 규칙 문서 하나 |
| 소비자 이관·릴리스 | [consumer-adoption.md](docs/runbooks/consumer-adoption.md) | [release.md](docs/runbooks/release.md) |
| 기존 결정을 변경 | [ADR 색인](docs/adr/README.md) | 관련 ADR 본문만 |
| 문서·task·journal 유지 | [documentation-maintenance.md](docs/runbooks/documentation-maintenance.md) | 필요한 기록 문서만 |

### 특수한 경우에만 참조

- `docs/reviews/`: 적대적 리뷰를 수행하거나 과거 finding을 추적할 때만 읽는다.
- `docs/journal.md`: 과거 작업의 원인·명령·결과를 추적할 때만 검색한다. 일반 작업 전부를 읽지 않는다.
- `docs/adr/` 전체: 구조적 결정의 이력을 감사할 때만 읽는다. 보통은 색인에서 관련 ADR 하나만 고른다.
- `docs/tasks/` 전체와 `docs/tasks-done.md`: backlog 감사나 의존성 재설계 때만 읽는다.
- 소비자 저장소 원본과 `docs/survey/` 전체: 규칙·계약의 근거를 재검증하거나 조사 기준 커밋을 갱신할 때만 연다. 조사 문서는 근거이지 규범이 아니다.

### 토큰 절약 규칙

- 인덱스 → 관련 상세 문서 → 필요한 절의 순서로 점진적으로 읽는다.
- `rg`로 제목·식별자·링크를 먼저 찾고, 관련 없는 긴 문서나 과거 로그를 통째로 읽지 않는다.
- 한 문서에서 답이 확인되면 단순 배경 링크를 연쇄적으로 따라가지 않는다.
- review·journal·ADR·survey는 역사·근거 기록이다. 현재 요구사항은 accepted ADR, architecture·standards 정본과 열린 task에서 확인한다.
- 문서가 충돌하면 조용히 선택하지 말고 정본 우선순위와 충돌 위치를 밝힌다.

## 4. 문서 정본과 우선순위

지시 우선순위는 다음과 같다.

1. 사용자 요청
2. 이 `AGENTS.md`
3. accepted ADR
4. `docs/architecture/README.md`와 관련 상세 architecture 문서
5. 선택한 상세 task
6. 관련 `docs/standards/*`·`docs/dev-environment.md` 문서
7. 코드와 테스트
8. review·journal·survey 등 역사·근거 기록
9. 최소한의 되돌릴 수 있는 가정

`SKILL.md`는 작업별 문서 라우터이며 별도의 정책 정본이 아니다. 구조적 결정은 ADR, 현재 설계는 architecture, 소비 저장소 전체가 따르는 공통 규칙은 standards, 실행 범위와 수용 기준은 task, 반복 절차는 runbook에 둔다. 같은 내용을 여러 문서에 복제하지 않는다. ADR 색인은 `docs/adr/README.md` 하나뿐이며 `docs/decisions.md`는 두지 않는다. 문서 링크는 저장소 상대 경로만 쓴다.

모든 Markdown 문서와 코드 주석·docstring·사용자 문자열은 한국어로 작성한다. 공식 필드명, 코드 식별자, 명령어, URL, 패키지명, 제공자 원문은 필요한 범위에서 영어를 유지한다. 예외는 세 가지다: 벤더링 원문, 원칙 소제목(Think Before Coding 등), 인용 reference(원문 유지 시 한국어 적용 메모 필수). 커밋 제목은 Conventional Commits 영어 type + 한국어 문장이다.

## 5. 개발·worktree·리뷰 진입점

- 정본 개발 환경은 Linux/WSL bash이고 CI는 ubuntu이며 Windows는 Tier 2(도구·validator 동작 보증)다. 도구 설치·경로 표기·Windows 절·검증 명령 사다리는 [개발 환경](docs/dev-environment.md)에만 둔다.
- 기본은 메인 checkout(`F:/dev/kor-travel-common`, WSL `/mnt/f/dev/kor-travel-common`)의 작업 branch다. 병렬 작업·격리·독립 리뷰가 실제로 필요할 때만 임시 worktree를 만들고, merge 또는 abandon 뒤 제거하고 prune한다. 같은 branch를 두 worktree에서 checkout하지 않는다. 명령과 CodeGraph 수명주기는 [agent workflow](docs/runbooks/agent-workflow.md)에만 둔다.
- 비단순 변경은 전문 영역이 다른 리뷰어 서브에이전트 2인의 독립 적대적 리뷰(동일 manifest·immutable 기준선·상대 결과 비공개)와 finding 반영을 거친다. 비면제 대상(`docs/standards/*`, `versions.json`, `packages/*` 공개 API·CSS, `.github/workflows/*`, `AGENTS.md`·`SKILL.md`·`docs/README.md`·ADR·runbook·task/review 규칙), 심각도·disposition·verdict 어휘, light/full 판정(작성자가 아닌 merge 담당)은 [agent workflow](docs/runbooks/agent-workflow.md)와 [review archive](docs/reviews/README.md)를 따른다.

## 6. 절대 하지 말 것

1. `main`에 직접 push하지 않는다. 모든 변경은 branch와 PR을 거친다.
2. 비밀, 운영 호스트 주소, 자격증명, `.env`, `*.local.md`를 커밋하거나 문서에 적지 않는다.
3. `git add -A`와 `git add .`을 사용하지 않는다. 파일을 경로별로 명시해 stage한다.
4. 실행하지 못한 검증·gate를 통과로 표시하지 않는다. 0 test·skip을 pass로 집계하지 않는다.
5. 한 사실을 두 곳에서 독립 선언하지 않는다. 정본 하나와 링크만 둔다(버전은 `versions.json`, 토큰 값은 `tokens.css`, ADR 색인은 `docs/adr/README.md`).
6. 토큰 정본 `tokens.css`와 생성물(`tokens.json`·`tokens.ts`·`tailwind-preset.cjs`)을 수동으로 불일치하게 만들지 않는다.
7. 소비자 1곳의 관찰만으로 규칙·컴포넌트·모듈을 공통으로 승격하지 않는다.
8. 벤더링 원본(shadcn 생성물·외부 스킬)을 출처·변경 표기(SPDX·`Origin`/`Derived-From`/`Modified`) 없이 수정하지 않고, pinvi(L6 확정 전)·벤더 tgz·`maplibre-vworld-*`·`python-*-api` 코드를 common으로 복사하지 않으며, 조사 문서(`docs/survey/`)를 규범으로 인용하지 않는다.
9. 토큰 이름·의미, `data-slot`/testid, prop 기본값, 정렬 모드, CSS 파일 경로, OpenAPI 계약을 계약 시험·CHANGELOG `### Breaking`·이관 절 없이 바꾸지 않고, 배포 참조에 `@main` 같은 이동 ref를 쓰지 않는다.
10. stale·미검증·추정 값(후보 버전, 실행하지 못한 검증, 로딩·오류 중인 데이터, 조사의 "추정"·"미확인")을 UI·문서·evidence에서 확정값·정상값처럼 표시하지 않는다.

## 7. 외부 원문과 evidence

- Tailwind·shadcn/ui·Base UI·Next.js·React·FastAPI·Starlette·pydantic 등 외부 원문은 공식 URL과 version/commit 또는 문서 revision을 기록한다. 최신 버전 조사에는 조회일을 적는다.
- 벤더링·이식 코드는 파일 헤더 SPDX와 `Origin`/`Derived-From`/`Modified` 행, `PROVENANCE.md`(원천 저장소·커밋·경로·라이선스·수정)로 출처를 보존한다. 규칙은 [licensing](docs/standards/licensing.md)이 정본이다.
- 소비자 저장소·registry·CI가 필요한 검증을 common에서 실행하지 못했으면 evidence에 `NOT_RUN(사유)`, 영향받는 gate, 후속 task 또는 `외부 선행`을 기록한다. 명령을 적었다는 사실은 실행·성공의 증거가 아니다.
- 조사 문서(`docs/survey/*`)는 기준 커밋에 고정된 스냅샷이다. 본문을 고치지 않고 재조사 시 기준 커밋을 갱신한 새 절을 만든다. 오기 정정 값은 `docs/survey/README.md` §6.2를 따른다.

## 8. 완료와 push

- 변경 범위에 맞는 검증을 수행한다: 문서 검증(link·plan·unittest·`git diff --check`) → 패키지 빌드·타입 검사·단위 테스트 → `npm pack`/`uv build` 산출물 설치 → 소비자 스모크. 사다리와 명령은 [개발 환경](docs/dev-environment.md)에 있다.
- 비단순 변경은 리뷰어 2인의 finding을 수정, ADR 또는 task로 disposition하고 필수 검증을 다시 실행한다. post-fix commit은 두 리뷰어가 재검토한다.
- 관련될 때만 `docs/resume.md`, `docs/tasks.md`, 상세 task, ADR과 색인, `docs/standards/*`, `docs/journal.md`, `CHANGELOG.md`를 갱신한다.
- push 전 `git diff --staged` 전체를 직접 읽고 비밀·운영 호스트·자격증명·`.env`·`*.local.md`·소비자 저장소 로컬 파일이 포함되지 않았는지 확인한다. `git add -A`와 `git add .`은 사용하지 않는다.
- 실패한 검증, 미해결 P0/P1 finding, 닫히지 않은 gate(예외 미등록 `BELOW_FLOOR`, 대비 미달, OpenAPI drift)를 숨긴 채 완료·release 가능으로 표시하지 않는다. 릴리스 절차는 [release](docs/runbooks/release.md)를 따른다.
