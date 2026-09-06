# 에이전트·문서 공통 규약 (agent-conventions)

- 정본 지위: 이 문서는 kor-travel-common이 7개 소비 저장소에 **배포하는** 에이전트·문서 규약의 정본이다. 공통 절의 원문은 [`templates/AGENTS.common.md`](../../templates/AGENTS.common.md), 포인터 원문은 [`templates/CLAUDE.pointer.md`](../../templates/CLAUDE.pointer.md)이며 이 문서는 규칙·적용 범위·대응표만 둔다. common 저장소 **자체**의 규칙은 루트 [`AGENTS.md`](../../AGENTS.md)가 정본이고 이 문서를 인용한다.
- 확정 task: T-007(규약 초기판), T-001(common 자체 진입 문서), T-403(소비자 반영). 이 문서는 정본 초안이며 소비자 첫 채택 PR(T-410·T-461)에서 실물과 대조해 확정한다.
- 마지막 갱신: 2026-09-06. 결정 근거: [설계 브리프](../plan/design-brief.md) D-02·D-03·D-04·D-05·D-24·D-25·D-27·D-32, ADR-002·003([ADR 색인](../adr/README.md)).
- 상위 문서: [standards 색인](README.md). 관련: [agent workflow](../runbooks/agent-workflow.md)(common 자체 절차), [documentation maintenance](../runbooks/documentation-maintenance.md), [tasks-rule](../tasks-rule.md), [review archive](../reviews/README.md), [canview 대조표](../architecture/canview-checklist.md).

## 1. 목적과 적용 범위

canview의 계층형 문서 구조와 `AGENTS.md` 정책 정본 모델(지시 (5))을 kor-travel 7개 저장소에 **공통 절 + 로컬 절** 방식으로 배포한다. 조사 결과 5원칙 문구는 6개 저장소에서 글자 단위로 동일했고([docs-conventions](../survey/cross/docs-conventions.md) §1.4), canview 특유의 읽기 정책·리뷰 gate·기록 규칙은 kor-travel에 없었다(`dc` §1.5·§3.1). 따라서 이미 같은 것은 문구를 고정하고, 없는 것은 추가하며, 저장소마다 다른 것(OS·worktree 프로필·도메인 DO NOT·포트)은 로컬로 남긴다.

| 강도 | 뜻 | 적용 |
|---|---|---|
| MUST | 채택 PR 머지 조건 | 공통 절 문구 불변, `CLAUDE.md` 포인터, 상대 링크, 절대 금지 5 |
| SHOULD | 기록 후 미이행 허용(사유를 `docs/dev-environment.md` 또는 ADR에) | docs 트리 표준, task 원장 4원칙, review gate 채택, archive 규약, 설정 파일 형식 |

common 자체는 canview full gate·5열 원장·`validate_plan.py`를 그대로 채택한다(D-04·D-05). 소비자에게는 그 전부를 요구하지 않는다.

## 2. AGENTS 공통 절 A~I

`AGENTS.md`를 **공통 절**(common이 배포, 문구 고정, 마커 사이)과 **로컬 절**(저장소 소유, 마커 뒤)로 나눈다. 순서·제목은 다음과 같으며 원문은 [`templates/AGENTS.common.md`](../../templates/AGENTS.common.md)다(`dc` §3.1 채택).

| 절 | 제목 | 요지 | 출처·근거 |
|---|---|---|---|
| A | 작업 원칙 | Think Before Coding / Simplicity First / Surgical Changes / Goal-Driven Execution / Practical Bias 5블록. 문구는 6개 저장소 동일본 그대로 | `dc` §1.4(kta·conc·ktdm·geo·map·pinvi 동일). geo의 Goal-Driven 추가 불릿 2개는 **열림(사용자 확인 필요)** — 기본값 미포함(5개 저장소 문구 변경 회피, `dc` §5 Q1) |
| B | Ruthless Review | 4개 불릿. 리뷰 gate의 태도 근거 | canview `AGENTS.md` §2([canview 체크리스트](../survey/cross/canview-structure-checklist.md) A2.7) |
| C | 문서 언어 정책 | 한국어 기본 + 영어 유지 목록 + 예외 3종(§7) + 커밋 제목 형식 | D-32; `dc` §1.3·§2 C10 |
| D | 문서 정본과 우선순위 | 9단계(§2.1) + 정본 분리(ADR/architecture/standards/task/runbook) + 복제 금지 + SKILL 라우터 + CLAUDE 포인터 | `dc` §2 C4·C5; canview A4.1~A4.3 |
| E | 문서 읽기 정책 | 반드시 4 / 필요할 때 표 / 특수 5 / 토큰 절약 5 | canview A3.1~A3.6(경로만 치환) |
| F | 절대 하지 말 것(공통 5) | main 직접 push · 비밀·`*.local.md`·`.env` 커밋 · `git add -A/.` · 미실행 gate 통과 표시(0 test·skip pass 금지, 명령≠증거) · 한 사실 두 곳 선언 | 각 저장소 DO NOT 교집합(`dc` §3.1 F), ktdm DO NOT 15, D-25, canview A6.10·A8.4 |
| G | 완료와 push | 검증 계층 → 2인 리뷰(full/light) → 기록 갱신 → 보안 감사 5단계(grep 패턴 포함) → PR 6항목 → merge 조건(CI 없는 저장소 조항 포함) | canview A8.1~A8.5; `dc` §1.16(conc·ktdm·pinvi 절차 + geo `/security-review`); `dc` §2 C14 |
| H | 기록 갱신 | 5종(ADR+색인 / resume / journal 최상단 / tasks·tasks-done·상세 / CHANGELOG) "직접 관련된 것만" + journal 불변 + archive 링크 | geo/map agent-guide + canview documentation-maintenance §2(`dc` §3.1 H) |
| I | 개발 환경·worktree·CodeGraph 진입점 | OS 미규정, 프로필은 `docs/dev-environment.md`가 선언; 불변 조건 5; 리뷰 기준선은 object-only 또는 detached | D-03; `dc` §2 C1·C2; canview A5.1~A5.3·R4.4·R4.5 |

규칙:

- MUST 공통 절은 마커(`<!-- kor-travel-common AGENTS 공통 절 시작 … -->` / `끝`) 사이에 **그대로** 넣는다. 저장소는 문구를 바꾸지 않고, 바꾸고 싶으면 common PR을 낸다. 판(`판 2026-09`)이 바뀌면 소비자는 채택 PR로 갱신한다(drift 비교는 마커 사이 텍스트 diff; 선두 주석 블록 정규화, D-17).
- MUST 로컬 절에 두는 것: 목표·역할·식별자 표, 개발 환경 프로필과 경로, 도메인 DO NOT, 포트, provider·형제 라이브러리 원칙, 검증 명령, 배포·prod 규칙, 완료 알림(Telegram). 로컬 절이 공통 절과 충돌하면 공통 절이 이기며 충돌은 열린 질문으로 common에 보고한다.
- MUST 지시 우선순위(§2.1)는 로컬에서 재정의하지 않는다. pinvi의 "accepted ADR > AGENTS" 관행(`dc` §1.2)은 **열림(사용자 확인 필요)** — 기본값은 공통 순위 채택이며 pinvi ADR-016 갱신 PR을 요청한다.
- SHOULD `SKILL.md`는 canview식 작업별 시작점 표(라우터)를 갖되, geo·map처럼 이미 도메인 DO NOT을 SKILL §4에 둔 저장소는 재이관하지 않는다(`dc` §2 C4).

### 2.1 지시 우선순위(9단계)

1. 사용자 요청 → 2. `AGENTS.md`(공통 절 + 로컬 절) → 3. accepted ADR → 4. `SKILL.md`·`docs/architecture/` → 5. 선택한 상세 task → 6. 그 밖의 `docs/`(common `docs/standards/`·`docs/dev-environment.md` 포함) → 7. 코드·테스트 → 8. review·journal(역사) → 9. 최소한의 되돌릴 수 있는 가정. canview A4.1의 6단계 "hardware·vehicle·UI·development"를 "standards·dev-environment"로 치환했다(`cv` A4.1).

### 2.2 `CLAUDE.md` 포인터(MUST)

- 40줄 이하. 진입 순서 4단계와 정본 링크 표만 둔다. 규칙·현황·사실을 복제하지 않는다(D-02; `dc` §2 C3). 원문 [`templates/CLAUDE.pointer.md`](../../templates/CLAUDE.pointer.md).
- `AGENTS.md`와 상충하면 `CLAUDE.md`를 고친다(kta 규칙 채택). pinvi ADR-016의 양방향 동기 부담은 포인터화로 해소한다.
- `.claude/`는 gitignore하되 `CLAUDE.md`는 추적한다.

### 2.3 에이전트 설정 파일(SHOULD)

`antigravity.json`·`claude.json`·`opencode.json`·`.mcp.json`·`.codex/config.toml`·`.gemini/mcp.json`은 geo 이식형(`codegraph serve --mcp`, filesystem `"."`)을 표준으로 하고 worktree별 절대 `cwd`는 로컬 override로만 둔다(`dc` §1.18·§2 C13). `opencode.json`은 `"instructions": ["AGENTS.md", "SKILL.md"]`를 포함한다(map 관례). 예시는 [`templates/agent-config/`](../../templates/README.md).

## 3. `docs/` 트리 표준(SHOULD)

`dc` §3.2 채택. 필수 표기는 "채택 PR에서 만들거나 stub으로 두는 것"이며 내용 형식은 canview를 따른다(`cv` §3.5 R5.1~R5.9).

| 경로 | 필수 | 정본 역할 | 출처 |
|---|---|---|---|
| `docs/README.md` | 필수 | 문서 지도(읽기 단계 표 → 정본 관계 트리 → 분야별 표 → 작업·운영·이력 표 → 탐색 규칙) | canview R5.7·R5.8 |
| `docs/resume.md` | 필수 | 현재 진척도 / 다음 한 작업(시작 문서·확인 대상·완료 조건) / 열린 핵심 경로 / 차단 조건 / 문서 정본. 짧게 유지 | canview R5.4 + geo/map 형식 |
| `docs/journal.md` | 필수 | newest-first, H2 `## YYYY-MM-DD (agent[, 주제])`, 5필드(작업/변경/결정/발견/다음) 또는 굵은 라벨 불릿, 기존 항목 불변 | geo/map agent-guide §4 + canview R5.1~R5.3 |
| `docs/tasks.md`·`tasks-done.md`·`tasks-rule.md` | 필수 | §4 | |
| `docs/tasks/T-NNN-*.md` + `tasks/README.md` | 비단순 task | 상세 9항목(목표·고정 결정·구현 범위·범위 밖·예상 변경 파일·수용 기준·검증 명령·evidence·rollback/release 차단 조건) | canview R1.11 |
| `docs/adr/README.md` + `NNN-<slug>.md` | 필수 | 파일당 1개, 3자리, H1 `# ADR-NNN: 제목`, 상태 어휘 `accepted`/`superseded by ADR-XXX`/`partially superseded by ADR-XXX`, 색인 상단에 "다음 후보 번호는 ADR-NNN". `decisions.md` 이중 색인은 두지 않는다(D-02·D-27) | canview R2.1~R2.10; `dc` §2 C8. 단일 `decisions.md` 저장소(conc·ktdm·pinvi)는 재번호 없이 유지하고 신규 ADR부터 파일 분리(선택); 타 저장소 번호 미러(wx) 금지 |
| `docs/architecture/README.md` + 상세 | 필수 | 현재 설계 정본(사용법 표·범위·흐름·경계·저장소 구조·정본) | canview F20 골격 |
| `docs/dev-environment.md` | 필수(로컬) | OS·셸·worktree 프로필(고정/임시)·명령·Playwright 실행 위치 | 6개 저장소 보유(`dc` §1.11) |
| `docs/runbooks/README.md`·`agent-workflow.md`·`agent-failure-patterns.md`·`documentation-maintenance.md` | 필수 | 절차 정본. README는 `문서|읽는 시점|책임` 표. `agent-guide.md`(geo·map·pinvi)는 세 문서로의 포인터 stub으로 전환(삭제 아님) | canview R4.1·R4.2; `dc` §2 C16 |
| `docs/reviews/README.md`·`adversarial/TEMPLATE.md`·`adversarial/evidence/` | full gate 채택 시 필수 | §5 | canview R3 |
| `docs/archive/` | 조건부(220 KiB 초과) | §9 | map tasks-rule §8 |
| `docs/reports/`·`sprints/`·`execplan/`·`integration-map.md`·`ports.md`·`bindings.md` | 선택(로컬) | | map·pinvi·ktdm |
| 루트 `CHANGELOG.md` | 필수 | Keep a Changelog, `## [Unreleased]` + `### Added`/`### Changed`, 사용자 가시 변경만, 한국어(절 제목 영어) | geo·map·canview R5.5 |
| 루트 `design.md`/`DESIGN.md` | UI 보유 저장소 필수 | 색상 톤·구조·토큰 위치, **본문 한국어**(kta·pinvi·wx 이행 대상, D-32) | conc·ktdm·geo |

하위 디렉터리 README는 서두 1단락에서 상위 인덱스와 자기 책임을 밝힌다(R5.9).

## 4. `tasks-rule` 공통 규약(SHOULD)

common 자체는 5열 표 + `READY/BLOCKED/IN_PROGRESS/DONE` + P0~P3 + `validate_plan.py`를 쓴다([tasks-rule](../tasks-rule.md), D-05). 소비자 원장 **형식은 규정하지 않는다**. 체크박스 원장(`- [ ] **T-NNN** — 제목 (P1, 선행 T-012)`, 다수 관행 `dc` §1.7)을 허용하고 다음만 배포한다.

1. 참조된 ID는 재번호하지 않는다(`T-NNN`, 하위 `T-NNN<letter>`, 파생 `T-NNN-<slug>`; ktdm의 ID 재사용 이력은 재발 금지 대상).
2. 완료 시 evidence(실행 명령·결과·NOT_RUN·PR)를 보존한다. map 2026-08-27 평면화 사고(acceptance 삭제 후 조건 없는 완료, `dc` §1.7)의 재발 방지.
3. 요약 entry에 acceptance·명령을 복제하지 않는다. 수용 기준은 상세 파일(또는 `tasks-acceptance.md`·`execplan/`)이 소유한다.
4. 비단순 task(다중 경계 변경·계약 변경·이관)는 `docs/tasks/T-NNN-*.md` 상세 파일(§3의 9항목)을 만든다. `tasks-acceptance.md`·`execplan/`은 그 파일로 수렴(시점은 로컬).

상태 대응표(체크박스 원장 ↔ common 어휘; map lint 파서가 4종을 허용 — `dc` §2 C6):

| 체크박스 | common 상태 | 비고 |
|---|---|---|
| `[ ]` | `READY` 또는 `BLOCKED` | 보류 사유 1줄을 entry 꼬리에(`(BLOCKED: 외부 선행 L6)`) |
| `[/]` | `IN_PROGRESS` | |
| `[~]` | 부분 완료 | common에는 없는 상태. 상세 파일에 남은 acceptance를 적고 `IN_PROGRESS`로 보고 |
| `[x]` | `DONE` | tasks-done newest-first 이동 + journal + resume |

우선순위 P0~P3와 선행은 표 대신 entry 꼬리표 `(P1, 선행 T-012)`로 둔다. 외부 대기(다른 저장소 PR·권리 확인·registry 권한)는 `외부 선행:`으로 표기하고 선행 ID에 섞지 않는다. 기계 검사(`validate_task_ledger.py`, `dc` §3.3-7)는 **후보**이며 이번 PR 범위 밖이다(common은 `validate_plan.py`만 보유).

## 5. review gate 공통 규약(SHOULD)

`dc` §3.4 + D-04. 두 단계로 배포한다.

| 단계 | 대상 | 산출물 |
|---|---|---|
| **full** | 정책 문서(`AGENTS.md`·`SKILL.md`·`docs/README.md`·ADR·runbook·task/review 규칙), 공용 UI primitive·디자인 토큰·OpenAPI 계약·인증·권한, common 배포물 채택 PR | `docs/reviews/adversarial/YYYY-MM-DD-<scope>.md`(TEMPLATE) + `evidence/…-reviewer-{a,b}.md` + `reviews/README.md` 표 1행 |
| **light** | 그 밖의 비단순 변경 | 2인 독립 리뷰 결과를 PR 본문 §3과 journal에 요약(kta hostile-review 방식) |

두 단계 공통:

- 전문 영역이 다른 리뷰어 2인 독립, 상대 결과 비공개, 동일 manifest, immutable 기준선(commit object-only 4명령 또는 `worktree add --detach`; `cv` R3.12·R3.14), verdict `BLOCK`/`CONDITIONAL`/`PASS`.
- 심각도 P0~P3(P0·P1 `BLOCK`), disposition `OPEN`/`FIXED`/`REJECTED_WITH_EVIDENCE`/`DEFERRED`(P2/P3만, owner·task·gate·기한 필수). P0/P1은 원 reviewer 재확인 전 merge 금지; risk acceptance·"release 차단" 표시는 closure가 아니다.
- post-fix commit을 두 reviewer가 자신의 finding + 전체 delta 회귀로 재검토. full은 별도 `-post-fix.md` report(같은 날 같은 범위 반복은 `-02`), 상태 어휘 `IN_REVIEW`/`COMPLETE`/`POST_FIX_REVIEW`(D-04; canview 미정본 Q5의 common 확정값).
- **full/light 판정 주체는 merge 담당(작성자 ≠ 판정자)**이다(`dc` §5 Q4 해소). 면제는 오탈자·동의 링크 수정뿐이고 작성자가 아닌 merge 담당이 PR에서 승인한다.
- 과거 report에 append 금지, correction note만 허용, closure artifact(원본 보존 + disposition·재검증 + index 1행)는 재귀 리뷰를 시작하지 않는다(`cv` R3.4·R3.16).

형식 정본은 common의 [review archive](../reviews/README.md)와 [TEMPLATE](../reviews/adversarial/TEMPLATE.md)이며 소비자는 복사해 쓴다. 리뷰어 페르소나명(James/Popper)은 로컬이다.

## 6. 로컬로 유지할 항목(공통화하지 않음)

`dc` §3.5 그대로.

| 항목 | 이유 |
|---|---|
| 개발 환경 OS·worktree 프로필·경로·포트 | 저장소 ADR로 확정(conc ADR-23/33, ktdm, geo ADR-065, pinvi ADR-051; `dc` §2 C1·C2) |
| 도메인 DO NOT(geo 11·map 26·pinvi 22·kta 9) | 도메인 종속 |
| provider·형제 라이브러리 원칙, 의존 방향 | 저장소별 |
| 리뷰어 페르소나명, Telegram 완료 알림, `deploy-runbook.local.md`, prod 검증 항목 | 운영 종속·민감 |
| `sprints/`·`execplan/`·`reports/`·`integration-map.md`·`ports.md`·`bindings.md` | 저장소 운영 도구 |
| `.hallmark/` 산출물 취급 | 목적 미확인(`dc` §5 Q6); common 파일에는 Hallmark 스탬프 없음(D-13) |
| ADR 번호 이력(단일 파일 저장소의 기존 번호) | 재번호 금지 |

## 7. 언어 정책과 예외 3종(MUST)

D-32. 한국어 기본(Markdown·코드 주석·docstring·사용자 문자열). 영어 유지: 식별자·SPDX/Origin 헤더 키·CHANGELOG 절 제목·공식 필드명·명령·URL·패키지명·벤더링 원문·원칙 소제목. 커밋 제목은 Conventional Commits 영어 type + 한국어 문장.

| 예외 | 조건 | 근거 |
|---|---|---|
| 벤더링 원문 | `.claude/`·`.agents/`·`.codex/`·`.opencode/` 아래 upstream agent/skill 원문(동기화 충실성) | kta·map 명시, 4개 암묵(`dc` §1.3); map ADR-059 |
| 원칙 소제목 | Think Before Coding 등 원 프로젝트 제목 | kta 명시 |
| 인용 reference | 원문 유지 시 **한국어 적용 메모 필수**. `design.md`/`DESIGN.md` 본문은 한국어 | kta·pinvi `design.md` 영어 본문은 이행 대상(`dc` §1.3 위반 관찰) |

## 8. 링크 규칙(MUST)

- 저장소 상대 경로만 쓴다. 절대 경로 링크(`F:/…`, `/mnt/f/…`, `/…`)는 금지이며 common의 [`tools/validate_document_links.py`](../../tools/validate_document_links.py)가 오류로 잡는다(D-27; canview 접두 허용은 제거 — `dc` §2 C11, `cv` Q2). kta의 절대 링크 17개 파일은 T-433에서 상대화.
- 다른 저장소 파일은 GitHub URL(커밋 고정)로 인용한다. fenced code block 안의 링크는 검사하지 않으며, `#fragment`는 검증하지 않는다(`cv` §4.3).
- 이동·이름 변경 시 Markdown 링크뿐 아니라 backtick·plain path 참조를 `rg -n "old-name\.md|docs/old/path" -g "*.md"`로 검색하고 label도 새 역할로 고친다([documentation maintenance](../runbooks/documentation-maintenance.md) §6).
- 템플릿 파일(`templates/*.md`) 안의 소비자 경로는 링크가 아니라 backtick 경로로 적는다(common에서 링크 검사가 오탐하지 않도록).

## 9. archive 규약(SHOULD; map tasks-rule §8)

conc·ktdm·geo·pinvi의 journal이 256 KB(에이전트 read 한도)를 넘는다(`dc` §1.9). map §8을 공통 규약으로 채택한다.

- 분리 경계: 백로그 구조가 새로 성립한 시점 이전 기록을 `docs/archive/`로 옮긴다. 그 이후만 `resume.md`/`journal.md`에 남긴다.
- 파일명 `archive/{resume,journal,tasks-done}-YYYY-MM[a|b|c].md`. 한 파일이 **220 KiB(225,280 bytes)**를 넘으면 같은 달 안에서 `a`/`b`/`c`로 쪼개 모든 파일이 단독으로 읽히게 한다.
- live 문서 상단 "과거 기록 아카이브" 표(파일·기간·엔트리 수·크기) 필수. 과거 검색은 `rg <패턴> docs/archive/`.
- 새 엔트리는 항상 live 문서 상단. 아카이브는 읽기 전용이며 예외는 깨진 상대 링크 재기준화와 220 KiB 초과 해소뿐(본문 바이트 보존, 근거를 live 문서에 기록).
- 아카이브의 상대 링크는 `docs/archive/` 기준으로 실제 파일에 도달해야 하며 링크 검사(map `tests/unit/test_docs_archive_links.py` 또는 common validator)를 통과한다.
- live 문서가 200 KB에 근접하면 다음 경계를 잡아 분리하고 바이트 단위 보존 근거를 PR에 남긴다.

## 10. 기록 갱신·완료와 push 요약

공통 절 G·H가 정본이다. 요지: 직접 관련된 기록 5종만 갱신 · 검증 계층은 범위에 맞게 · 보안 감사 5단계 · PR 본문 6항목([`templates/consumer-pr.md`](../../templates/consumer-pr.md)) · `NOT_RUN(사유)` 표기와 0 test·skip pass 금지(D-25) · CI 없는 저장소는 required check 등록 전 "미적용" 명시(`dc` §2 C14). common 자체의 상세 절차는 [agent workflow](../runbooks/agent-workflow.md).

## 11. 채택 절차

1. 라이선스·lockfile·버전 gate 확인 — [`templates/consumer-adoption-checklist.md`](../../templates/consumer-adoption-checklist.md) §0, [versions](versions.md) §3.2.
2. `AGENTS.md` 공통 절 삽입 + `CLAUDE.md` 포인터 + 설정 파일 이식형 전환 + `dependabot.yml`(하나의 규약 PR; 코드 채택 PR과 분리).
3. `docs/` 트리 필수 항목 stub 생성(`docs/README.md`·`dev-environment.md`·`adr/README.md` 다음 번호).
4. review gate 채택 여부와 단계를 `docs/dev-environment.md` 또는 ADR에 선언.
5. 이후 코드 채택 PR은 [`templates/consumer-pr.md`](../../templates/consumer-pr.md) 규격(D-24)과 [consumer adoption runbook](../runbooks/consumer-adoption.md)을 따른다.

drift 점검: 분기 감사(T-506)에서 마커 사이 텍스트·`CLAUDE.md` 줄 수·절대 링크·`decisions.md` 이중 색인을 대조한다.

## 12. 열린 결정(사용자 확인 필요; 기본값으로 진행)

| # | 결정 | 기본값 |
|---|---|---|
| Q1(`dc` §5) | 공통 절 A에 geo Goal-Driven 추가 불릿 2개 포함 여부 | 미포함(6개 저장소 동일 문구 유지) |
| Q3(`dc` §5) | pinvi "accepted ADR > AGENTS" 우선순위 | 공통 순위 채택, pinvi ADR-016 갱신 요청 |
| Q9(`dc` §5) | 단일 `decisions.md` 저장소의 ADR 파일 분리 시점 | 신규 ADR부터 파일 분리(선택), 기존 번호 유지 |
| O-17 | Windows 지원 tier | Tier 2(도구·validator Windows 동작); 소비자 공통 절은 OS 미규정 |
| O-19 | 코드 주석·커밋 언어 | 한국어 기본 |

## 13. 근거

- 결정: [design-brief](../plan/design-brief.md) D-02·D-03·D-04·D-05·D-17·D-24·D-25·D-27·D-32·D-33, §2 O-17·O-19.
- 조사: [docs-conventions](../survey/cross/docs-conventions.md) §1.1~§1.20·§2 C1~C16·§3.1~§3.5·§5, [canview-structure-checklist](../survey/cross/canview-structure-checklist.md) §2(A1.1~A8.5)·§3(R1~R6)·§4·§5, [commonality-matrix](../survey/commonality-matrix.md) §1.5·§2.5·§4.2 D26~D30, [licensing](../survey/cross/licensing.md) B3.
