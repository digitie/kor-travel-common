# canview 대조표(채택·변형·제외)

- 정본 지위: 사용자 지시 (5) "canview 구조·AGENTS.md 채택"의 검증 수단. `docs/survey/cross/canview-structure-checklist.md` §1(파일 F01~F47)·§2(AGENTS A1.1~A8.5)·§3(규약 R1.1~R6.10)·§4(validator 문법)의 항목 ID별로 common의 판단·사유·대응 파일·상태를 적는다. 확정 task: T-001·T-008(★이번 PR). 마지막 갱신: 2026-09-06.
- 근거: [브리프](../plan/design-brief.md) D-02·D-03·D-04·D-05·D-27, `docs/survey/cross/canview-structure-checklist.md`(canview `1f93b8a`), `docs/survey/cross/docs-conventions.md` §2·§3·§4.

판단 어휘: **채택**(canview 규칙·파일을 그대로), **변형**(역할은 유지하되 내용·경로를 common 용도로 교체), **제외**(하드웨어·차량·firmware·임베디드 전용), **추가**(canview에 없는 common 항목). 상태 어휘: **있음**(작업 트리에 존재), **있음(이번 PR)**(이 PR의 architecture 작성자가 만듦), **작성 예정(T-xxx)**(후속 task), **—**(제외라 대응 파일 없음). 상태는 2026-09-06 작업 트리와 [브리프 §3 파일 지도](../plan/design-brief.md)를 대조한 값이며, 링크 검사(`tools/validate_document_links.py`)와 [문서 지도](../README.md)가 실제 트리의 정본이다.

## 1. 파일 목록(cv §1.1 F01~F47)

| ID | canview 경로 | 판단 | 사유·결정 | common 대응 파일 | 상태 |
|---|---|---|---|---|---|
| F01 | `AGENTS.md` | 변형 | 8절 골격 유지, §1·§6·§7의 차량 항목을 라이브러리 경계로 치환(D-02) | `AGENTS.md` | 있음(이번 PR) |
| F02 | `SKILL.md` | 변형 | 라우터 + 작업별 시작점 표 + 용어를 common 도메인으로 | `SKILL.md` | 있음(이번 PR) |
| F03 | `README.md` | 변형 | "문서"·"저장소 상태" 절만 재사용, 패키지 목록 추가 | `README.md` | 있음(이번 PR) |
| F04 | `CHANGELOG.md` | 채택 | 단일 파일에 패키지별 H3, `### Breaking`(D-18·D-31) | `CHANGELOG.md` | 있음(이번 PR) |
| F05 | `LICENSE` | 채택 | GPL-3.0-or-later 전문(D-17) | `LICENSE` | 있음 |
| F06 | `.gitignore` | 변형 | firmware·KiCad 제거, Node·Python·편집기 추가(cv §1.2) | `.gitignore` | 있음 |
| F07 | `.gitattributes` | 변형 | 전역 `* text=auto eol=lf` + 확장자별 LF, `*.ps1` CRLF(D-03) | `.gitattributes` | 있음 |
| F08 | `tokens.css`(루트) | 변형 | 토큰은 패키지 산출물; 루트에 두지 않음(D-12) | `packages/tokens/tokens.css` | 작성 예정(T-101) |
| F09 | `docs/README.md` | 채택 | 읽기 단계 표 → 정본 관계 트리 → 분야별 표 → 탐색 규칙(R5.7) | `docs/README.md` | 있음(이번 PR) |
| F10 | `docs/resume.md` | 변형 | 상태·다음 한 작업·차단·인계 링크(R5.4) | `docs/resume.md` | 있음(이번 PR) |
| F11 | `docs/journal.md` | 채택 | newest-first(R5.1) | `docs/journal.md` | 있음(이번 PR) |
| F12 | `docs/tasks.md` | 채택 | 5열 표·"N개의 상세 작업"·검증 정본 링크(D-05) | `docs/tasks.md` | 있음(이번 PR) |
| F13 | `docs/tasks-done.md` | 채택 | 5열 고정, 완료 날짜는 제목 괄호(D-05) | `docs/tasks-done.md` | 있음 |
| F14 | `docs/tasks-rule.md` | 변형 | ID 대역을 common 6대역 + §2.1 앱 대역으로(D-05) | `docs/tasks-rule.md` | 있음 |
| F15 | `docs/tasks/README.md` | 채택 | validator 통과 조건 추가 | `docs/tasks/README.md` | 있음 |
| F16 | `docs/tasks/T-*.md` | 변형 | 형식만 채택, 실행 목록은 task 원장 정본 | `docs/tasks/T-*.md` | 있음(원장과 상세 검증) |
| F17 | `docs/adr/README.md` | 채택 | 규칙 5 + 표 `ADR|제목|상태` + 상단 "다음 후보 번호"(D-02, R2.7 보존) | [ADR 색인](../adr/README.md) | 있음(이번 PR) |
| F18 | `docs/adr/001…007-*.md` | 변형 | 형식만; 결정 목록은 ADR 색인 정본 | `docs/adr/NNN-*.md` | 있음(이번 PR) |
| F19 | `docs/decisions.md` | 제외 | 이중 색인 금지. `adr/README.md`가 단일 색인이며 "다음 후보 번호"를 상단에 둠(D-02·D-27, cv Q1) | — | — |
| F20 | `docs/architecture/README.md` | 변형 | 사용법 표 → 범위 → 데이터·의존 흐름 → 책임과 경계 → 릴리스·버전 경계 → 저장소 구조 → 문서 정본 | [아키텍처 개요](README.md) | 있음(이번 PR) |
| F21 | `docs/architecture/{system,features,automation,ota,diagnostic-bridge,controller-can-pipeline}.md`, `protocols/*` | 제외/변형 | 차량·protocol 설계는 제외. 역할만 `packages.md`·`style-delivery.md`·`docs/standards/openapi.md`가 이어받음 | [packages](packages.md), [style-delivery](style-delivery.md), `docs/standards/openapi.md` | 있음(이번 PR) / 있음(이번 PR) |
| F22 | `docs/architecture/implementation-readiness.md` | 변형 | "구현자가 다시 결정하지 않을 사항"·정본과 생성물 역할을 채택 gate 추적표로 | [채택 준비 기준](adoption-readiness.md) | 있음(이번 PR) |
| F23 | `docs/architecture/requirements-coverage.md` | 변형 | 요구→정본→task→검증→남은 gate 형식을 소비자→gate 형식으로 | [채택 준비 기준](adoption-readiness.md) §4 | 있음(이번 PR) |
| F24 | `docs/development/windows.md`, `toolchains.md` | 변형 | Linux/WSL 정본 + Windows Tier 2 절 + 임시 worktree 프로필 1파일(D-03) | `docs/dev-environment.md` | 있음(이번 PR) |
| F25 | `docs/hardware/**`, `docs/vehicle/**`, `docs/images/*.png` | 제외 | 하드웨어·차량. `docs/images/`는 UI 스크린샷이 생기면 선택(현재 없음) | — | — |
| F26 | `docs/ui/design.md` | 변형 | 원칙·정보 구조·토큰 정본 지정 골격을 규칙 문서로 분해(D-13). 루트 `DESIGN.md`는 두지 않음(파일 지도에 없음) | `docs/standards/design-tokens.md`·`ux-guide.md`·`responsive-web.md` | 있음(이번 PR) |
| F27 | `docs/ui/lvgl-demo-review.md` | 제외 | 임베디드 UI | — | — |
| F28 | `docs/runbooks/README.md` | 변형 | consumer-adoption·release 행 추가 | `docs/runbooks/README.md` | 있음 |
| F29 | `docs/runbooks/agent-workflow.md` | 변형 | 8절 유지, OS·worktree 명령을 bash 1벌 + dev-environment 위임(D-03), 검증 사다리를 문서→패키지→tarball→소비자로(R4.6) | `docs/runbooks/agent-workflow.md` | 있음(이번 PR) |
| F30 | `docs/runbooks/documentation-maintenance.md` | 변형 | standards·survey·plan 행 추가, `decisions.md` 언급 제거 | `docs/runbooks/documentation-maintenance.md` | 있음 |
| F31 | `docs/runbooks/agent-failure-patterns.md` | 변형 | 임베디드 12행 제거, 링크·WSL/Windows·worktree 3행 재사용 + 패키징·스타일·소비자 통합 행 | `docs/runbooks/agent-failure-patterns.md` | 있음 |
| F32 | `docs/reviews/README.md` | 채택 | 기록 규칙 9 + 빈 표 + 새 리뷰 시작(D-04) | `docs/reviews/README.md` | 있음 |
| F33 | `docs/reviews/adversarial/TEMPLATE.md` | 채택 | diff 0 | `docs/reviews/adversarial/TEMPLATE.md` | 있음 |
| F34 | `docs/reviews/adversarial/YYYY-MM-DD-<scope>.md` | 변형 | 형식만; post-fix는 별도 `-post-fix.md`(D-04) | 첫 리뷰 시 생성 | — |
| F35 | `docs/reviews/adversarial/evidence/*.md` | 변형 | 디렉터리·명명 규칙만 | `docs/reviews/adversarial/evidence/.gitkeep` | 있음 |
| F36 | `tools/README.md` | 변형 | 문서 검증 도구 설명으로 전면 재작성; check_versions 행은 versions-conventions 작성자가 추가 | `tools/README.md` | 있음 |
| F37 | `tools/validate_document_links.py` | 변형 | 절대 접두 허용 제거(절대 경로는 오류), `packages/**`·`templates/**`·`tests/**` 포함, 산문 오탐 제외(D-02·D-27, cv Q2) | `tools/validate_document_links.py` | 있음 |
| F38 | `tools/validate_plan.py` | 채택 | 무변경(docstring 1줄)(D-05) | `tools/validate_plan.py` | 있음 |
| F39 | `tests/test_plan_validation.py` | 채택 | 35 tests 무변경 | `tests/test_plan_validation.py` | 있음 |
| F40 | `tools/toolchain-versions.json` | 변형 | `versions.json`(schema `kor-travel-common.version-registry.v1`, floor/recommended/exceptions/blocked/enforce)으로 재설계(D-06·D-07, cv Q8) | `versions.json` | 있음(이번 PR) |
| F41 | `tools/environment/setup-windows.ps1`, `tools/hardware/**`, `protocol/**`, `ui/**` | 제외/변형 | SDK·KiCad 제외. "manifest 대조 스크립트" 역할만 `check_versions.py`로 | `tools/check_versions.py` | 있음(이번 PR) |
| F42 | `tests/automation/**`, `lvgl/**`, `ui/**` | 제외 | host C·LVGL·브라우저 시험 | — | — |
| F43 | `dbc/`, `firmware/`, `hardware/`, `protocol/`, `ui/` | 제외/변형 | 제품 소스는 `packages/*`(tokens·ui·py)와 `templates/*`로 | `packages/`, `templates/` | 작성 예정(T-101·T-201·T-302 / 이번 PR) |
| F44 | `.tools/`(gitignore) | 변형 | 로컬 부산물 디렉터리 후보. 현재 `.gitignore`에 없음 — 리뷰 probe 관례가 생길 때 추가(open) | `.gitignore` | 있음(항목 미등록) |
| F45 | (없음) `CLAUDE.md` | 추가 | 40줄 이하 포인터, 읽기 순서에 추가하지 않음(D-02, dc C3) | `CLAUDE.md` | 있음(이번 PR) |
| F46 | (없음) `.editorconfig` | 추가 | utf-8·lf·indent 2(`*.py` 4)·`*.ps1` crlf | `.editorconfig` | 있음 |
| F47 | (없음) `.github/workflows/*` | 추가 | `docs.yml` + T-009 하드닝·`tools` windows 매트릭스 + T-010 재사용 워크플로(D-18) | `.github/workflows/docs.yml` 외 | 있음(docs.yml) / 작성 예정(T-009·T-010) |
| F48 | (없음) `docs/standards/`, `docs/survey/`, `docs/plan/` | 추가 | 규칙 정본·조사·계획 분리(D-02) | 각 디렉터리 | 있음 |
| F49 | (없음) `NOTICE`·`THIRD_PARTY_NOTICES.md`·`PROVENANCE.md`·`CONTRIBUTING.md`·`LICENSES/` | 추가 | 고지·출처 규약(D-17) | 각 파일 | 고지 파일 있음; `LICENSES/` 원문은 T-003 잔여 |
| F50 | (없음) `docs/integration-map.md`, `docs/architecture/{packages,style-delivery,consumers,adoption-readiness,canview-checklist}.md` | 추가 | 소비자 채택 지도·배포 단위·스타일 계약·대조표(D-02) | [통합 지도](../integration-map.md) 외 | 있음(이번 PR) |
| F51 | (없음) `templates/`, `consumers.pins.json`, `.github/pull_request_template.md` | 추가 | 소비자 복사형 파일·smoke pin·PR 본문(D-18·D-24) | 각 파일 | templates·PR 템플릿 있음; pins는 T-010 잔여 |

## 2. AGENTS.md 절별(cv §2 A1.1~A8.5)

대응 파일은 별도 표기가 없으면 `AGENTS.md`(entry 작성자, 있음(이번 PR))이다. 공통 절 A~I는 `docs/survey/cross/docs-conventions.md` §3.1의 배치를 따르며 소비자 배포판은 `templates/AGENTS.common.md`다.

### 2.1 §1 목표와 안전 경계

| ID | canview 규칙(요지) | 판단 | common 내용·사유 | 대응 파일 |
|---|---|---|---|---|
| A1.1 | 첫 문장 제품 정의 1문장 | 변형 | "kor-travel 제품군의 UI·백엔드 공통 코드와 규칙을 정의하는 GPL-3.0-or-later 라이브러리" | `AGENTS.md` §1 |
| A1.2 | 3열 표(장치·하드웨어·책임) | 변형 | 배포 단위 6·소비자 7(+pinvi 표면 3)·책임 표(D-01); kor-travel-airport Admin·PinVi Admin 명시 | `AGENTS.md` §1, [아키텍처 개요](README.md) §1 |
| A1.3 | "DBC에 있다는 이유만으로 확정하지 않는다" | 변형 | "소비자 한 곳에 있다는 이유만으로 공통화하지 않는다"(승격 4조건, [개요](README.md) §3) | `AGENTS.md` §1 |
| A1.4 | 송신 허용 조건·의미 명령만 | 변형 | 공유 라이브러리 중복 금지·소비자 저장소 직접 수정 금지·인증 범위 밖(D-01) | `AGENTS.md` §1 |

### 2.2 §2 작업 원칙

| ID | canview 규칙 | 판단 | common 내용·사유 | 대응 파일 |
|---|---|---|---|---|
| A2.1 | 모호하면 가정을 드러내고 확인 | 채택 | 공통 절 A | `AGENTS.md` §2, `templates/AGENTS.common.md` |
| A2.2 | 최소 범위 변경 | 채택 | 그대로 | 동일 |
| A2.3 | 사용자 변경·dirty worktree 보존 | 채택 | 그대로 | 동일 |
| A2.4 | 버그=재현+회귀, 리팩터링=보존 근거, 설계=수용 기준 | 채택 | 그대로 | 동일 |
| A2.5 | 미실행 gate를 통과로 표시 금지 | 채택 | `NOT_RUN(사유)` 어휘 추가(D-25) | 동일, `docs/tasks-rule.md` §6 |
| A2.6 | 근거 우선; 사실·후보·실차 evidence 분리 | 변형 | "실차 evidence" → "소비자 저장소 실측(빌드·e2e) evidence"; 조사(`docs/survey/`)는 규범 아님 | `AGENTS.md` §2 |
| A2.7 | Ruthless Review 4불릿 | 채택 | 문구 그대로(공통 절 B, D-04) | `AGENTS.md` §2, `templates/AGENTS.common.md` |

### 2.3 §3 문서 읽기 정책

| ID | canview 규칙 | 판단 | common 내용·사유 | 대응 파일 |
|---|---|---|---|---|
| A3.1 | AGENTS=짧은 정본, docs/README=라우터, 전체 선제 읽기 금지 | 채택 | 그대로 | `AGENTS.md` §3 |
| A3.2 | 반드시 참조 4단계 | 채택 | AGENTS → docs/README → docs/resume → 지정 task 1파일. `CLAUDE.md`는 포인터이며 순서에 넣지 않음(D-02) | `AGENTS.md` §3, `CLAUDE.md` |
| A3.3 | task 고를 때만 tasks.md | 채택 | 그대로 | `AGENTS.md` §3 |
| A3.4 | 필요할 때만 참조 표 6행 | 변형 | "Windows toolchain" → `docs/dev-environment.md`; "하드웨어·차량·UI" → `docs/standards/`·consumer-adoption runbook | `AGENTS.md` §3 |
| A3.5 | 특수 참조 5 | 변형 | 5번째를 "소비자 저장소 원본·조사 문서 전체"로 | `AGENTS.md` §3 |
| A3.6 | 토큰 절약 5 | 채택 | 그대로 | `AGENTS.md` §3 |

### 2.4 §4 문서 정본과 우선순위

| ID | canview 규칙 | 판단 | common 내용·사유 | 대응 파일 |
|---|---|---|---|---|
| A4.1 | 9단계 우선순위 | 변형 | 6단계 "hardware·vehicle·UI·development"를 "standards·dev-environment"로 치환; `SKILL.md`는 라우터라 순위에 넣지 않음 | `AGENTS.md` §4 |
| A4.2 | SKILL은 라우터 | 채택 | 그대로 | `AGENTS.md` §4, `SKILL.md` |
| A4.3 | 결정=ADR, 설계=architecture, 범위=task, 절차=runbook, 복제 금지 | 채택 | "공통 규칙=standards" 1항 추가(`docs/runbooks/documentation-maintenance.md` §1) | `AGENTS.md` §4 |
| A4.4 | Markdown/RST 한글, 공식 원문 영어 | 변형 | RST 삭제, 패키지명·SPDX 키·CHANGELOG 절 제목·원칙 소제목 영어 유지(D-32) | `AGENTS.md` §4 |

### 2.5 §5 개발·worktree·리뷰 진입점

| ID | canview 규칙 | 판단 | common 내용·사유 | 대응 파일 |
|---|---|---|---|---|
| A5.1 | 정본 환경 Windows PowerShell; 상세는 development/windows.md | 변형 | 정본 = Linux/WSL bash, Windows Tier 2; 상세는 `docs/dev-environment.md`에만(D-03, ADR-003) | `AGENTS.md` §5, `docs/dev-environment.md` |
| A5.2 | 기본 메인 checkout; 임시 worktree; 명령은 agent-workflow에만 | 채택 | 불변 조건 그대로, 경로 `<repo>-wt/<agent>-<task>`(D-03) | `AGENTS.md` §5, `docs/runbooks/agent-workflow.md` |
| A5.3 | 비단순 변경은 2인 독립 적대적 리뷰 | 채택 | canview full gate 그대로(D-04) | `AGENTS.md` §5, `docs/runbooks/agent-workflow.md` §5 |

### 2.6 §6 절대 하지 말 것

| ID | canview 금지 항목 | 판단 | common 대응 | 대응 파일 |
|---|---|---|---|---|
| A6.1 | schema·generator 있는 header와 생성물 수동 불일치 | 변형 | `tokens.css` 정본과 생성물(`tokens.json`·`tokens.ts`·`tailwind-preset.cjs`) 수동 불일치 금지(D-12) | `AGENTS.md` §6 |
| A6.2 | 임의 CAN ID 송신 | 제외 | — | — |
| A6.3 | build mode flag 승격 | 제외 | — | — |
| A6.4 | 단일 capture로 신호 승격 | 변형 | 소비자 1곳 관찰만으로 규칙·컴포넌트 승격 금지 | `AGENTS.md` §6 |
| A6.5 | sender precondition 신뢰 | 제외 | — | — |
| A6.6 | installation-wide 공유 secret | 제외 | — | — |
| A6.7 | GPIO 초기화만으로 안전 주장 | 제외 | — | — |
| A6.8 | 데이터시트 미대조 pin 확정 | 제외 | — | — |
| A6.9 | upstream DBC 원본 수정 금지, profile·evidence 분리 | 변형 | 벤더링 원본(shadcn 생성물·외부 스킬) 수정 시 `Origin:`/`Modified:` 표기; 조사와 규범 분리(D-17) | `AGENTS.md` §6, `docs/standards/licensing.md` |
| A6.10 | VIN·key·capture를 public Git에 | 변형 | 운영 호스트·자격증명·`*.local.md`·`.env`로 치환; prod redaction 전체 트리(D-18, O-23) | `AGENTS.md` §6 |
| A6.11 | 불완전 block diagram 제작용 표시 | 제외 | — | — |
| A6.12 | Bridge TX 권한 | 제외 | — | — |
| A6.13 | stale·candidate 값을 확정값처럼 표시 | 변형 | UX 규칙: 미검증·stale 값을 정상값처럼 렌더링 금지(UX-G5) | `docs/standards/ux-guide.md` |
| A6.14 | observer stream이 safety queue 잠식 | 제외 | — | — |
| A6.15 | wire 변경을 golden·version 시험 없이 완료 | 변형 | 공개 API·OpenAPI·마크업 계약 변경을 계약 시험·버전 표기 없이 완료 금지(D-31) | `AGENTS.md` §6 |
| A6.16 | 번호 목록, "…하지 않는다"로 끝남 | 채택 | 공통 5 + 라이브러리 특화 ≤5(dc §3.1 F) | `AGENTS.md` §6 |

### 2.7 §7 외부 원문과 evidence

| ID | canview 규칙 | 판단 | common 대응 | 대응 파일 |
|---|---|---|---|---|
| A7.1 | 공식 URL + version/commit | 채택 | Tailwind·shadcn·Next·FastAPI 문서 인용에 그대로 | `AGENTS.md` §7 |
| A7.2 | upstream 라이선스·digest 보존 | 변형 | 벤더링 코드 라이선스·원천 commit 기록(`PROVENANCE.md`, SPDX 헤더, D-17) | `AGENTS.md` §7, `PROVENANCE.md` |
| A7.3 | datasheet pin 대조 | 제외 | — | — |
| A7.4 | 네트워크·차량 검증 미실행 사유·gate·후속 task | 변형 | "소비자 저장소·registry·CI 필요 검증"으로 치환, `NOT_RUN(사유)` + `외부 선행` 승격(D-25) | `AGENTS.md` §7 |

### 2.8 §8 완료와 push

| ID | canview 규칙 | 판단 | common 대응 | 대응 파일 |
|---|---|---|---|---|
| A8.1 | 변경 범위에 맞는 host/target/UI/KiCad 검증 | 변형 | 문서 검증 → 패키지 빌드·tarball 설치 → 소비자 스모크(R4.6 사다리) | `AGENTS.md` §8, `docs/runbooks/agent-workflow.md` §4 |
| A8.2 | 비단순 변경은 2인 finding 수정·disposition·재검증 | 채택 | 그대로 | `AGENTS.md` §8 |
| A8.3 | 관련될 때만 resume/tasks/ADR/journal/CHANGELOG | 채택 | +standards | `AGENTS.md` §8, `docs/runbooks/documentation-maintenance.md` §2 |
| A8.4 | staged diff 직접 읽기; `git add -A`·`git add .` 금지 | 채택 | 검사 대상만 치환, 금지 문장 그대로 | `AGENTS.md` §8 |
| A8.5 | 실패 검증·미해결 P0/P1·닫히지 않은 gate 숨긴 완료 금지 | 채택 | 그대로 | `AGENTS.md` §8, `docs/tasks-rule.md` §6 |

## 3. 규약(cv §3 R1~R6)

### 3.1 task 규약(R1)

| ID | 규약 | 판단 | common 상태·사유 | 대응 파일 |
|---|---|---|---|---|
| R1.1 | 요약/완료/상세/진척 위치 | 채택 | `docs/tasks-rule.md` §1 | 있음 |
| R1.2 | ID `T-NNN[a]`, 재번호 금지 | 채택 | 대역은 common 6대역 + 앱 대역 §2.1(D-05) | 있음 |
| R1.3 | 상태 4값 | 채택 | | 있음 |
| R1.4 | 우선순위 P0~P3 | 채택 | `docs/tasks-rule.md` §5 명문화 | 있음 |
| R1.5 | metadata 4필드 각 1줄 | 채택 | | 있음 |
| R1.6 | 선행 문법, 외부 조건은 `외부 선행` | 채택 | | 있음 |
| R1.7 | 요약 5열, 글자 단위 일치 | 채택 | canview 체크박스 예시를 5열 표로 교체(cv Q3 해소) | 있음 |
| R1.8 | "N개의 상세 작업" 1회 | 채택 | | 있음(문구는 `docs/tasks.md`, 작성 예정) |
| R1.9 | READY/DONE 선행 모두 DONE | 채택 | | 있음 |
| R1.10 | DAG 사이클 없음 | 채택 | | 있음 |
| R1.11 | 상세 9항목 | 채택 | + 이관 task 필수 기재(대상 저장소·브랜치·되돌리기) | 있음 |
| R1.12 | 미래 경로·명령은 증거 아님 | 채택 | `docs/tasks-rule.md` §6에 명문화(D-25) | 있음 |
| R1.13 | 실행 기록 tool version·exit code·digest, NOT_RUN, 0 test 금지 | 채택 | §6 명문화 | 있음 |
| R1.14 | PR Task/Gate/Risk/Tests/Evidence/Rollback | 채택 | `.github/pull_request_template.md`, agent-workflow §7 | 있음(이번 PR) |
| R1.15 | 완료 시 이동 + journal·resume | 채택 | 완료 날짜는 제목 괄호(5열 고정) | 있음 |
| R1.16 | 요약·상세 같은 PR | 채택 | `docs/tasks/README.md` | 있음 |
| R1.17 | tasks.md §2 검사 명령 3개 + "제품 gate 아님" | 변형 | 원장은 선행·상태, 명령은 dev-environment·각 task 정본으로 연결 | 있음(이번 PR) |
| R1.18 | 우선순위 열 `---:` | 채택 | `docs/tasks-done.md` | 있음 |

### 3.2 ADR·결정 색인(R2)

| ID | 규약 | 판단 | common 상태·사유 | 대응 파일 |
|---|---|---|---|---|
| R2.1 | 파일당 1개, `NNN-<slug>.md` | 채택 | 001~012 | 있음(이번 PR) |
| R2.2 | H1 `# ADR-NNN: 제목` | 채택 | | 있음(이번 PR) |
| R2.3 | 머리 불릿 `상태`·`날짜` 필수, 선택 항목 | 채택 | + `근거 문서`(브리프 D-xx·조사 절) 관례화 | 있음(이번 PR) |
| R2.4 | 상태 어휘 accepted/superseded/partially superseded + ` — ` 보충 | 채택 | + `proposed`(ADR-012 O-8 대기) | [ADR 색인](../adr/README.md) |
| R2.5 | 절 컨텍스트→결정→결과 + 선택 절 | 채택 | 컨텍스트/결정/대안 검토/결과/후속·적용 위치 5절 고정 | 있음(이번 PR) |
| R2.6 | 뒤집을 때 새 ADR, 삭제 금지 | 채택 | | [ADR 색인](../adr/README.md) 규칙 3 |
| R2.7 | 다음 번호 = decisions.md 최댓값+1 | 변형 | decisions.md 없음 → `adr/README.md` 상단 "다음 후보 번호는 ADR-013"(D-02) | [ADR 색인](../adr/README.md) |
| R2.8 | ADR과 코드·문서·테스트 같은 PR | 채택 | | 규칙 4 |
| R2.9 | 여러 subsystem 영향 결정만 | 채택 | "여러 소비 저장소" | 규칙 1·2 |
| R2.10 | `adr/README.md` 표 `ADR|제목|상태`; decisions.md 표 | 변형 | 전자만 | [ADR 색인](../adr/README.md) |

### 3.3 review 규약(R3)

| ID | 규약 | 판단 | common 상태·사유 | 대응 파일 |
|---|---|---|---|---|
| R3.1 | report 경로·`-02` suffix | 채택 | `docs/reviews/README.md` 규칙 1 | 있음 |
| R3.2 | post-fix 별도 report 관행 | 채택(명문화) | post-fix는 별도 `-post-fix.md`, 같은 날 같은 범위 반복은 `-02`(D-04, cv Q5 해소) | `docs/reviews/README.md`, `docs/runbooks/agent-workflow.md` §5 |
| R3.3 | evidence 명명 `-reviewer-{a,b}` | 채택 | 규칙 5만; 변형 표기(`-postfix-`) 금지 | 있음 |
| R3.4 | 과거 report append 금지 | 채택 | | 있음 |
| R3.5 | 머리 불릿 11 | 채택 | TEMPLATE diff 0 | 있음 |
| R3.6 | 상태 어휘 미정본 | 채택(명문화) | `IN_REVIEW/COMPLETE/POST_FIX_REVIEW`, verdict `BLOCK/CONDITIONAL/PASS`(D-04) | `docs/runbooks/agent-workflow.md` §5 |
| R3.7 | finding ID·표 6열 | 채택 | | 있음 |
| R3.8 | 심각도 P0~P3 정의 | 채택 | | `docs/runbooks/agent-workflow.md` §5.3 |
| R3.9 | disposition 4종, DEFERRED는 P2/P3만 | 채택 | | §5.4·TEMPLATE |
| R3.10 | P0/P1 재확인 전 merge 금지 | 채택 | | 있음 |
| R3.11 | verdict 3값 | 채택 | | §5.3 |
| R3.12 | 전문 영역 다른 2인·같은 manifest·immutable 기준선·상대 결과 비공개 | 채택 | | 있음 |
| R3.13 | manifest·evidence 필수 항목 | 채택 | | §5.1 |
| R3.14 | object-only 명령 4개 / detached worktree | 채택 | bash 표기 1벌 | §5.1 |
| R3.15 | 비면제 8종·면제는 오탈자만·비작성자 승인 | 변형 | 비면제 = standards·versions.json·packages 공개 API/CSS·workflows·AGENTS/SKILL/docs README/ADR/runbook/task·review 규칙(D-04); light/full 판정 주체 = merge 담당 | §5 |
| R3.16 | closure artifact는 재귀 리뷰 아님 | 채택 | | 있음 |
| R3.17 | post-fix 2인 재검토 | 채택 | | 있음 |
| R3.18 | README 표 5열, 최신 위 | 채택 | 빈 표 | 있음 |

### 3.4 runbook·workflow 규약(R4)

| ID | 규약 | 판단 | common 상태·사유 | 대응 파일 |
|---|---|---|---|---|
| R4.1 | runbooks에는 절차만; README 표 | 채택 | 행 추가(consumer-adoption·release) | 있음 |
| R4.2 | agent-workflow 8절 | 채택 | | 있음(이번 PR) |
| R4.3 | 브랜치 `agent/<agent>-<task>`, main 직접 push 금지 | 채택 | | 있음(이번 PR) |
| R4.4 | worktree 경로·이중 checkout 금지·prune | 채택 | 경로 `<repo>-wt/<agent>-<task>`(D-03) | 있음(이번 PR) |
| R4.5 | CodeGraph 설치 시만; 없으면 `rg`·compiler·test 대체 | 채택 | | 있음(이번 PR) |
| R4.6 | 검증 사다리 7층 | 변형 | 문서 → 패키지 빌드·타입 → 단위 → tarball 설치 → 소비자 빌드·e2e → 소비자 배포 스모크; host simulation으로 실물 gate 대체 금지 → "common 스모크로 소비자 e2e 대체 금지" | 있음(이번 PR) |
| R4.7 | 기록 갱신 6조건 | 변형 | decisions.md 제외, standards·CHANGELOG 추가 | `docs/runbooks/documentation-maintenance.md` §2 |
| R4.8 | stage 경로별 명시, `git add .`·`-A` 금지, staged diff 읽기 | 채택 | | 있음(이번 PR) |
| R4.9 | PR 본문 6항목 | 채택 | + 소비자 PR 규격(D-24, `templates/consumer-pr.md`) | 있음(이번 PR) |
| R4.10 | CI·reviewer gate·P0/P1 확인 전 merge 금지 | 채택 | | 있음(이번 PR) |
| R4.11 | failure patterns 단일 표, 반복 시 task | 채택 | | 있음 |
| R4.12 | 문서 이동 7단계 | 채택 | `documentation-maintenance.md` §6 | 있음 |

### 3.5 journal·resume·CHANGELOG·README·docs 지도(R5)

| ID | 규약 | 판단 | common 상태·사유 | 대응 파일 |
|---|---|---|---|---|
| R5.1 | journal H1·H2 형식·newest-first·수정 금지 | 채택 | | 있음(이번 PR) |
| R5.2 | journal 본문 라벨 불릿 또는 검증 표 | 변형 | + 소비 저장소 상태(커밋·브랜치·dirty) | `docs/runbooks/documentation-maintenance.md` §4 |
| R5.3 | 도구 fallback·미실행 검증·사용자 변경 보존 | 채택 | | 있음 |
| R5.4 | resume 5절 + 다음 한 작업 3불릿 | 변형 | 상태·다음 한 작업·차단·인계 링크, 시작 파일·검증은 해당 절에서 연결 | 있음(이번 PR) |
| R5.5 | CHANGELOG Keep a Changelog 계열, 사용자 가시 변경만 | 변형 | 패키지별 H3 + `### Breaking` + 이관 절(D-18·D-31) | 있음(이번 PR) |
| R5.6 | 루트 README "문서" 절 링크 6 | 변형 | decisions 링크 → ADR 색인 | 있음(이번 PR) |
| R5.7 | docs/README 5부 구성 | 채택 | | 있음(이번 PR) |
| R5.8 | 정본 관계 5문장 | 채택 | + standards 1문장 | 있음(이번 PR) |
| R5.9 | 하위 README 서두 1단락 | 채택 | architecture·runbooks·reviews·tasks·adr 모두 | 있음 / 있음(이번 PR) |

### 3.6 언어·링크·Git·파일(R6)

| ID | 규약 | 판단 | common 상태·사유 | 대응 파일 |
|---|---|---|---|---|
| R6.1 | 본문 한글, 공식 원문 영어 | 채택 | + 패키지명·SPDX 키(D-32) | `documentation-maintenance.md` §7 |
| R6.2 | 상대 링크; 절대 접두 2종 해석 | 변형 | 절대 경로는 오류(접두 허용 제거, D-27, cv Q2) | `tools/validate_document_links.py` |
| R6.3 | fence 안 링크 미검사 | 채택 | | 있음 |
| R6.4 | 이동 후 link·plain path 검사 | 채택 | | 있음 |
| R6.5 | 사실·후보·추정·미검증 구분 | 채택 | + 조사 커밋 명시 | 있음 |
| R6.6 | 외부 원문 URL+version | 채택 | | 있음 |
| R6.7 | `.gitignore` 최소 집합 | 채택 | `.claude/ .codegraph/ .env .env.* !.env.example *.local.md` 유지(+`*.local.sh`) | 있음 |
| R6.8 | `.gitattributes` LF 고정·바이너리 | 채택(전역화) | `* text=auto eol=lf` | 있음 |
| R6.9 | 로컬 부산물은 `.tools/` | 후보 | `.gitignore`에 `.tools/` 없음; 리뷰 probe 관례 도입 시 추가(open) | `.gitignore` |
| R6.10 | `F:/`·`/mnt/f/` 공존 시 Windows 정본 | 변형 | Linux/WSL 정본(`/mnt/f/dev/kor-travel-common`), Windows는 Tier 2(D-03, cv Q4) | `docs/dev-environment.md` |

## 4. validator 문법(cv §4)

| 항목 | 판단 | 비고 |
|---|---|---|
| `validate_plan.py` 상세·요약 문법(§4.1) | 채택(무변경) | 5열 표·`fullmatch` 규칙 그대로; `docs/tasks-done.md`에 날짜 열을 추가하지 않음(제목 괄호) |
| `tests/test_plan_validation.py` 35 tests(§4.2) | 채택 | 오류 메시지 부분 문자열 계약 유지 |
| `validate_document_links.py`(§4.3) | 변형 | 대상 `docs/**`·`packages/**`·`tools/**`·`templates/**`·`tests/**`·루트; 절대 경로 오류; target 공백은 산문으로 건너뜀; fragment 미검증 유지 |
| `tests/test_document_links.py` | 추가 | 상대 링크만 허용·절대 링크 오류·산문 오탐 제외 회귀. `docs.yml`은 현재 `test_plan_validation.py`만 실행 — T-002에서 `test_*.py` 전체로 정비(open) |

## 5. 열림·후속

| 항목 | 상태 | 담당 |
|---|---|---|
| `.tools/` gitignore 등록(R6.9·F44) | 후보(미등록) | coordinator(`.gitignore`) |
| `docs.yml`의 unittest 범위를 `test_*.py`로 확장(§4) | T-002 | coordinator |
| AGENTS §6 추상화 재사용 항목(A6.1·A6.4·A6.9·A6.13·A6.15)을 공통 절 F에 둘지 `SKILL.md` 로컬 DO NOT에 둘지(cv Q9) | 기본값: 공통 5는 절 F, 라이브러리 특화는 AGENTS §6 로컬 ≤5 | entry |
| review 상태 어휘·post-fix 명명(R3.2·R3.6) | D-04로 확정; `agent-workflow.md` §5에 명문화 | runbooks |
| `docs/images/`(F25) | UI 스크린샷은 PR evidence로만(D-21); 디렉터리 두지 않음 | — |
