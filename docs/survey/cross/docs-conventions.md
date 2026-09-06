# 횡단 비교 — 문서·에이전트 규약 비교 (kor-travel 7 + canview)

kor-travel 7개 저장소와 참조 모델 canview의 에이전트 운영·문서 규약을 항목별로 대조하고, canview 구조를 `kor-travel-common`의 기준으로 채택할 때의 충돌과 해결안, common이 배포할 "공통 에이전트/문서 규약" 초안, common 자체 저장소가 가져야 할 파일 목록을 정리한다. 모든 항목은 **사실 / 후보 / 추정 / 미확인**으로 구분한다. 별도 표기가 없는 서술은 조사 커밋에서 직접 확인한 사실이다.

## 기준

| 약칭 | 저장소 | 체크아웃 | 기준 커밋 | 비고 |
|---|---|---|---|---|
| kta | kor-travel-airport | `F:/dev/kor-travel-common-survey/kta-main` | `2bb1111` | 구 parking-radar |
| conc | kor-travel-concierge | `F:/dev/kor-travel-concierge` | `7945305` | TripMate |
| ktdm | kor-travel-docker-manager | `F:/dev/kor-travel-common-survey/ktdm-main` | `862562d` | ktdctl |
| geo | kor-travel-geo | `F:/dev/kor-travel-geo-fixes` | `1d9d74d` | kor-travel-geo-ui 포함 |
| map | kor-travel-map | `F:/dev/kor-travel-common-survey/ktm-main` | `c494e227` | npm workspaces 모노레포 |
| wx | kor-travel-weather | `F:/dev/kor-travel-weather` | `6003da9` | uv 기반 |
| pinvi | pinvi | `F:/dev/kor-travel-common-survey/pinvi` | `9af25e5` | apps/web admin, apps/mobile Expo |
| canview | canview (참조 모델) | `F:/dev/canview` | `d078437` | branch `agent/codex-doc-information-architecture` |
| common | kor-travel-common (새 저장소) | `F:/dev/kor-travel-common` | `b92fabe` (LICENSE만 추적) | 작업 트리에 미추적 scaffold 존재(§4 참고) |

선행 검토 보고서 `kor-travel-geo-fixes/docs/kor-travel-common-library-review.md`(2026-09-05)는 UI 라이브러리 도입 검토가 주제이며, AGENTS/CLAUDE/SKILL·docs 트리·worktree·리뷰 gate 같은 에이전트/문서 규약은 다루지 않는다(사실: `AGENTS|CLAUDE.md|SKILL|worktree` 검색 0건, "규약"은 디자인 토큰 의미 규약 문맥 3건). 따라서 본 문서와 결론이 충돌하는 부분은 없고, 그 보고서 §1의 "코드를 옮기기보다 공유할 규약과 회귀 사례를 먼저 정리"라는 권고를 본 조사가 뒷받침한다.

## 방법

- 각 저장소에서 `git rev-parse --short HEAD`, `git ls-files`(전체·`docs/`·`.agents/.claude/.codex/.opencode/.gemini/.hallmark`·`.github/workflows`)로 파일 존재와 트리를 확인했다. 조사 대상 저장소에는 아무 파일도 만들거나 바꾸지 않았다.
- 진입 파일(`AGENTS.md`, `CLAUDE.md`, `SKILL.md`, `design.md`/`DESIGN.md`, `README.md`, `CHANGELOG.md`)의 줄 수·바이트를 `wc`로 재고, `AGENTS.md`는 8개 전부 전문을 읽었다. `CLAUDE.md`/`SKILL.md`는 제목 구조와 핵심 절(진입 순서, 절대 금지, 체크리스트)을 읽었다.
- canview의 `docs/README.md`, `tasks-rule.md`, `adr/README.md`, ADR-002/003/004, `reviews/README.md`, `reviews/adversarial/TEMPLATE.md`, `runbooks/*.md`, `tasks/README.md`, `tasks.md`·`tasks-done.md`·`journal.md`·`resume.md`·`decisions.md`, `development/windows.md`, `tools/validate_document_links.py`, `tools/validate_plan.py`를 읽었다.
- kor-travel 쪽은 `docs/tasks-rule.md`(kta·geo·map·pinvi), `docs/adr/README.md`(kta·geo·map·wx), `docs/decisions.md` 머리(conc·ktdm·pinvi), `docs/runbooks/README.md`(kta·geo·map·wx·pinvi), `docs/runbooks/hostile-review.md`(kta), `docs/runbooks/agent-workflow.md` 제목(geo·map), `docs/agent-workflow.md`·`docs/agent-guide.md`(pinvi·geo·map 해당 절), `docs/codegraph-worktree.md`(map), ADR-034/041/065(geo), ADR-016/017/021/024/047/051 제목과 ADR-016 본문(pinvi), ADR-33 본문(conc), `docs/tasks.md`·`tasks-done.md`·`journal.md`·`resume.md` 머리, 루트 `antigravity.json`/`claude.json`/`codex.json`/`opencode.json`/`.mcp.json`, `.codex/config.toml`, `.gemini/mcp.json`, `.claude/settings.json`, `.claude/agents/README.md`(kta·map), `.gitignore`·`.gitattributes`, map의 `scripts/task_ledger_lint.py`·`tests/lint/test_task_ledger_conventions.py`·`tests/unit/test_docs_archive_links.py`·`docs/tasks-acceptance.md` 머리를 읽었다.
- `rg`/`grep`으로 적대적 리뷰·심각도·disposition 어휘, `CI green`, `[/]` 마커, 절대 경로 링크(`](</F:/dev/`), Hallmark 언급, worktree 언급을 저장소별로 집계했다.
- 파일 크기는 `wc -c`(KB = 1024 바이트 정수 나눗셈)로 기록했다.

---

## 1. 항목별 비교표

열 순서는 kta · conc · ktdm · geo · map · wx · pinvi · canview. "—"는 해당 없음, "미확인"은 조사에서 확인하지 못한 항목이다.

### 1.1 진입 파일 구성·길이·역할

| 항목 | kta | conc | ktdm | geo | map | wx | pinvi | canview |
|---|---|---|---|---|---|---|---|---|
| `AGENTS.md` 줄 수 | 201 | 200 | 169 | 225 | 330 | 39 | 445 | 130 |
| `CLAUDE.md` 줄 수 | 77 | 288 | 134 | 116 | 101 | — | 222 | — (`.claude/` 자체가 gitignore) |
| `SKILL.md` 줄 수 | 66 | 152 | 146 | 145 | 175 | — | 281 | 66 |
| 루트 디자인 문서 | `design.md` 38 | `design.md` 54 | `DESIGN.md` 139 | `design.md` 54 | — (`docs/architecture/admin-frontend-design-rules.md`) | — | `DESIGN.md` 451 | — (`docs/ui/design.md` + 루트 `tokens.css`) |
| `README.md` 줄 수 | 341 | 205 | 108 | 203 | 215 | 167 | 244 | 71 |
| `CHANGELOG.md` 줄 수 | — | 14 | — | 508 | 4193 | — | 437 | 37 |
| `AGENTS.md` 역할 | 정식 정책 정본(Codex/Antigravity entry) | 원칙·정체성·환경·DO NOT·보안 감사 | 동일 (conc 계열) | 목표·원칙·환경·worktree·DO NOT·보안 감사 | 표준 entry, 정식 정책 정본 | 범위·식별자·개발 규칙·확인 명령만 | "단일 진실"(도구별 진입 표 포함) | 짧은 규칙·금지선 정본 |
| `CLAUDE.md` 역할 | 1쪽 요약("압축 인용", 상충 시 CLAUDE를 고침) | 프로젝트 현황·현재 작업·잔존 부채·환경 레이아웃·ADR 색인 | 프로젝트 현황·디렉터리·명령 | 현재 상태·세션 연속성(정본 표로 위임) | 1쪽 요약(진입 순서·금지 5·체크리스트 1줄) | — | 1쪽 요약(단, 60줄 인용 블록으로 환경·CodeGraph·Telegram 규칙 재기술) | — |
| `SKILL.md` 역할 | 에이전트 매뉴얼(원칙·계층·금지 9·검증 게이트) | 매뉴얼(빠른 시작·DO NOT·자주 묻는 작업·어휘·체크리스트) | 동일 | 동일 + §4 DO NOT이 개발 규칙 정본 | 동일 + §4 26개 DO NOT 정본 | — | 동일 + Telegram MCP·첫 5분 프로토콜 | 작업별 문서 **라우터**(정책 복제 금지) |
| `docs/README.md` 문서 지도 | — | — | — | — | — | — | — | 있음(109줄, 3단계 읽기·정본 관계 트리) |

- 사실: `docs/README.md`(문서 지도)는 canview에만 있다. kor-travel 7개는 `CLAUDE.md`/`AGENTS.md`의 "먼저 읽을 문서" 목록이 그 역할을 대신한다.
- 사실: canview는 SKILL.md를 정책 정본에서 제외한다(ADR-004 §1). kor-travel의 geo·map은 반대로 ADR에서 뺀 개발 규칙을 `SKILL.md` §4로 이관해 SKILL이 규칙 정본이다(`docs/adr/README.md` "→ 개발 규칙" 항목).
- 사실: pinvi ADR-016은 `AGENTS.md`↔`CLAUDE.md` 동기 갱신을 필수로 규정한다. kta는 상충 시 `CLAUDE.md`를 고치는 단방향 규칙이다.
- 사실(계보): canview ADR-002는 "kor-travel-geo의 문서 구조를 적용한다"고 명시한다. map `docs/runbooks/README.md`는 PinVi 본체 runbook 컨벤션을 옮겼다고 적고, pinvi `tasks-rule.md`는 map의 task 분리 정책을 적용했다고 적는다. kta `journal.md` 2026-08-23은 map 문서 구조를 선별 이식(T-028)했으며 "에이전트별 worktree/sandbox·codegraph 게이트·sprint 문서군"은 단일 서비스에 맞지 않아 가져오지 않았다고 기록한다. wx `.gitignore`의 codegraph 주석은 map에서 복사됐다(존재하지 않는 `docs/codegraph-worktree.md`를 참조).

### 1.2 지시 우선순위

| 순위 | kta | conc | ktdm | geo | map | wx | pinvi | canview |
|---|---|---|---|---|---|---|---|---|
| 1 | 사용자 요청 | 사용자 요청 | 사용자 요청 | 사용자 요청 | 사용자 요청 | (목록 없음) | **accepted ADR**(`docs/decisions.md`) | 사용자 요청 |
| 2 | AGENTS.md | AGENTS.md | AGENTS.md | AGENTS.md | AGENTS.md | | AGENTS.md | AGENTS.md |
| 3 | SKILL.md | SKILL.md | SKILL.md | SKILL.md | SKILL.md | | SKILL.md | accepted ADR |
| 4 | architecture·adr/README·data-model·test-strategy·runbooks/testing | architecture.md·decisions.md | architecture.md·decisions.md | architecture 4종·adr/README·agent-guide·external-apis | architecture 4종·adr/README·test-strategy·agent-guide·provider-contract | | docs/agent-guide.md | architecture/README + 상세 |
| 5 | README + 나머지 docs | tasks·journal·README | tasks·journal·README | README + 나머지 docs | README + 나머지 docs | | sprints/SPRINT-N | 선택한 상세 task |
| 6 | 기존 코드·테스트 | 기존 코드·테스트 | 기존 코드·테스트 | 기존 코드·테스트 | 기존 코드·테스트 | | 개별 문서 | hardware·vehicle·UI·development 문서 |
| 7 | 최소·되돌릴 수 있는 가정 | — | — | 최소·되돌릴 수 있는 가정 | 최소·되돌릴 수 있는 가정 | | journal.md | 코드·테스트 |
| 8–9 | | | | | | | | review·journal(역사) → 최소 가정 |

- 사실: pinvi만 ADR을 AGENTS.md 위에 둔다. canview는 AGENTS 아래·architecture 위에 둔다. 나머지는 ADR을 4순위 문서군에 포함한다.
- 사실: canview만 "review·journal은 역사 기록"이라는 순위를 명시한다.

### 1.3 언어 정책

| 항목 | kta | conc | ktdm | geo | map | wx | pinvi | canview |
|---|---|---|---|---|---|---|---|---|
| 기본 | 모든 Markdown 한국어 | 모든 Markdown 한글 "예외 없음" | 동일(conc) | 모든 Markdown/RST 한글 | 모든 Markdown/RST 한국어 | 문서·주석 한국어 기본(1줄) | 모든 Markdown 한국어 | 모든 Markdown/RST 한글 |
| 영어 유지 목록 | 필드명·식별자·명령·URL·라이브러리/제공자 원문·환경변수 | 식별자·명령/경로·공식 용어·벤더명·표준 keyword(ADR/CHANGELOG/semver 라벨)·shell 출력 | conc와 동일 | 필드명·식별자·명령·URL·제공자 원문 | kta와 동일 | 식별자·URL·provider 원문 | kta와 동일 | geo와 동일 |
| 벤더링 원문 예외 | 명시(`.claude/`, `.codex/`, `.agents/skills/`) | 미명시(벤더링 디렉터리는 존재) | 미명시 | 미명시 | 명시(ADR-059, `.claude/agents/README.md`) | — | 미명시 | — (벤더링 없음) |
| 원칙 제목 영어 예외 | 명시("Think Before Coding" 등 원 프로젝트 제목 유지) | 암묵(H2 영어 제목) | 암묵 | 암묵 | 암묵 | — | 암묵 | 해당 없음(한국어 제목) |
| 위반 관찰 | `design.md` 본문 영어(Hallmark 기록) | — | — | — | — | `docs/dev-environment.md` 제목 "Development environment", `docs/runbooks/README.md` 항목 영어 | `DESIGN.md` 본문 영어(Airbnb reference) + 한국어 적용 메모 | — |

### 1.4 행동 원칙 블록

| 항목 | kta | conc | ktdm | geo | map | wx | pinvi | canview |
|---|---|---|---|---|---|---|---|---|
| Think Before Coding / Simplicity First / Surgical Changes / Goal-Driven Execution / Practical Bias | `## 행동 원칙` 아래 H3 5개, 제목에 한국어 부제 병기 | H2 5개(파일 상단, 목표 다음) | H2 5개(파일 최상단) | H2 5개 | H2 5개 | — | H2 5개(파일 최상단) | `## 2. 작업 원칙` 6개 불릿으로 재서술(영어 제목 없음) |
| 본문 문구 | 기준 문구 | 기준 문구 | 기준 문구 | 기준 + Goal-Driven에 2개 장문 불릿 추가(테스트가 실제로 실패함을 먼저 확인, 가드 추가 전 실측) | 기준 문구 | — | 기준 문구 | "도구·SDK·하드웨어가 없어 실행하지 못한 gate를 통과로 표시하지 않는다", "근거 우선·사실/후보/evidence 상태 분리" 추가 |
| Ruthless Review 블록 | 없음(runbook으로 대체) | 없음 | 없음 | 없음 | 없음 | 없음 | 없음 | `### Ruthless Review` 4개 불릿 |

- 사실: 5개 원칙의 불릿 문구는 kta·conc·ktdm·geo·map·pinvi 6개에서 글자 단위로 동일하다(geo만 추가 불릿). 공통 절로 그대로 배포 가능한 가장 강한 후보다.
- 사실: canview의 6개 불릿은 5원칙을 한국어로 압축한 것이며 문구가 다르다.

### 1.5 Ruthless/적대적 리뷰 정책

| 항목 | kta | conc | ktdm | geo | map | wx | pinvi | canview |
|---|---|---|---|---|---|---|---|---|
| 정책 문서 | `docs/runbooks/hostile-review.md`(92줄) | 없음(사실). `docs/pr-review-2026-06.md`는 결과 문서 | 없음. journal·tasks-done·decisions에 "적대 리뷰 2인" 실행 흔적(#315 5건 반영) | 없음. journal·resume·tasks-done에 "두 독립 적대적 리뷰"(T-304) 흔적, `docs/postmerge-review-fixups-*.md` 14건 | 없음. `docs/reports/`·lint docstring에 "적대 리뷰 R2-S2" 등 흔적 | 없음 | 없음. `docs/reviews/`(사후 PR 리뷰 종합 5건), `runbooks/pr-review-sprint4.md`, CI 리마인더 워크플로 | `AGENTS.md` §2·§5·§8 + `runbooks/agent-workflow.md` §5 + `reviews/README.md` + `TEMPLATE.md` |
| 리뷰어 구성 | 서브에이전트 2개 페르소나 James(frontend/live UI)·Popper(backend/PG/ops), read-only | 미확인 | 미확인(2인) | 미확인(2인) | 미확인 | — | Codex/Claude 상호 사후 리뷰 | 분야가 다른 전문 리뷰어 서브에이전트 2인, 상대 결과 비공개 |
| 독립성·기준선 | 서로 결과 미공유, 동일 diff | — | — | — | — | — | — | 동일 manifest + immutable 기준선(commit object-only 또는 detached worktree), 실제 관찰 hash·clean 검증 기록 |
| 심각도 | P0/P1/P2 | (문서 내 P0~ 언급은 로드맵 용어) | — | — | — | — | — | P0~P3, merge 효과 표(P0/P1 BLOCK) |
| disposition 어휘 | 없음(P0/P1 전부 수정, P2는 journal에 근거) | 없음 | 없음 | 없음 | reports에 `FIXED` 157회·`DEFERRED` 6회 사용(규정 없음) | — | 없음 | `OPEN`/`FIXED`/`REJECTED_WITH_EVIDENCE`/`DEFERRED`(P2/P3만, owner·task·gate·기한 필수) |
| evidence 보존 | journal/tasks-done에 리뷰어명·반영 요약·candidate SHA | — | — | — | — | — | — | `reviews/adversarial/evidence/YYYY-MM-DD-<scope>-reviewer-{a,b}.md` + 통합 report + index 표 |
| 면제 규칙 | main 머지 전부 적용 | — | — | — | — | — | — | 비면제 목록 + 일반 면제 조건 4개 + closure artifact 예외 |
| 재검토 | 필요 시 재실행 | — | — | — | — | — | — | post-fix commit을 두 reviewer가 재검토, verdict BLOCK/CONDITIONAL/PASS |

### 1.6 docs/ 트리 구성

| 요소 | kta | conc | ktdm | geo | map | wx | pinvi | canview |
|---|---|---|---|---|---|---|---|---|
| `docs/README.md` | — | — | — | — | — | — | — | 있음 |
| `resume.md` | 있음(7KB) | — (`CLAUDE.md` 현황 절이 대체) | — (journal이 정본) | 있음(192KB) | 있음(3KB) | — | 있음(400KB) | 있음(4KB) |
| `tasks.md` / `tasks-done.md` | 있음/있음 | 있음/— (완료 절 내장) | 있음/있음(번호순, ID 재사용 경고) | 있음/있음 | 있음/있음 + `tasks-acceptance.md` | —/— | 있음/있음 | 있음/있음(비어 있음) |
| `tasks-rule.md` | 12줄 | — | — | 78줄 | 82줄 | — | 109줄 | 46줄 |
| `tasks/T-NNN-*.md` 상세 | — | — | — | — (`docs/t2NN-*.md` 보고서가 루트에 산재) | — (`docs/execplan/` 없음, reports 94) | — | — (`docs/execplan/` 29건) | 46건 + `tasks/README.md` |
| ADR 저장 | `adr/README.md` + 001~007 | `decisions.md` 단일(1445줄) | `decisions.md` 단일(2806줄) | `adr/` 65파일 + README, `decisions.md` stub | `adr/` 57파일 + README, `decisions.md` 1KB 미만 | `adr/` 3파일(map 번호 미러) + README, `decisions.md` 색인 | `decisions.md` 단일(3263줄) | `adr/` 001~007 + README + `decisions.md` 색인 |
| `journal.md` | 19KB | 367KB | 564KB | 590KB | 95KB(archive 분리 후) | — | 777KB | 15KB |
| `runbooks/` | README + 9 | — | — (flat) | README + agent-workflow·agent-failure-patterns·restore-drill | README + 13 | README + docker-app | README + 24 | README + agent-workflow·documentation-maintenance·agent-failure-patterns |
| agent-workflow | — | — | — | runbooks/ | runbooks/ | — | `docs/agent-workflow.md` | runbooks/ |
| agent-failure-patterns | runbooks/ | — | — | runbooks/ | runbooks/ | — | `docs/agent-failure-patterns.md` | runbooks/ |
| documentation-maintenance | — | — | — | — | — | — | — | runbooks/ |
| agent-guide.md(진입·기록 5종·ADR 규약·journal/resume 형식·PR 워크플로) | — | — | — | 있음 | 있음 | — | 있음 | — (tasks-rule + documentation-maintenance + agent-workflow로 분할) |
| `reviews/` | — | — | — | — | — | — | 5건(사후 PR 리뷰 종합) | README + adversarial/ + evidence/ |
| `reports/` | 1(hallmark 감사) | 루트에 e2e-report·pr-review 산재 | 루트에 audit 산재 | 루트에 t-NNN·postmerge-review 산재 | 94 | — | `audit/` 2 | — |
| `archive/` | — | — | — | — | 18(journal/resume/tasks-done 분할) | — | — | — |
| `sprints/` | — | — | — | — | 6 | — | 7 | — |
| `architecture/` | README + 8 | `architecture.md` 단일 | `architecture.md` 단일 | 7 | 23 | 7 | `architecture.md` + 15 | README + 8 + protocols/ |
| 기타 고유 | `current-state.md`, `project-brief.md`, `openapi.json` | `list-api-contract.md`, `provider-policy.md` | `bindings.md`, `ports.md`, `DESIGN-RULES.md`, `design-system.md` | `api-reference/`, `codegraph-worktree.md`, `ports.md`, `windows-reinstall-recovery.md` | `integration-map.md`, `codegraph-worktree.md`, `etl/`, `removal-manifests/` | `integration-map.md`, `migrations/`, `weather-api.md` | `api/`, `compliance/`, `legal/`, `conventions/`, `integrations/`, `spec/`, `design/` | `development/`, `hardware/`, `vehicle/`, `ui/`, `images/` |

### 1.7 task ID 체계와 상태 어휘

| 항목 | kta | conc | ktdm | geo | map | wx | pinvi | canview |
|---|---|---|---|---|---|---|---|---|
| ID 형식 | `T-NNN` | `T-NNN` | 활성 항목은 ID 없이 제목(`M05 …`, `GM-17`); 완료 이력은 `T-NNN`(T-013~018 재사용) | `T-NNN`, `T-NNN<letter>`, `T-NNN <식별구>`, `종료(no-go/no-action)`; 번호대 T-1xx/T-2xx(ADR-050) | `T-NNN`, `T-NNN<letter>`, `T-NNN-<slug>`, `T-RV-NN`, 주제 ID(`T-VN-M05-ACTIVATION`, `T-FE-…`) | — | `T-NNN`, `T-NNN<letter>`, `T-NNN-<slug>`, `T-VN-*`, `T-ADM-*` | `T-NNN`, 하위 `T-NNNa`; 번호대 000/100/200/300/400/500 = 서브시스템 |
| 상태 마커 | `[ ]`/`[x]` | `[ ]`/`[x]` + 절(진행 중/대기/완료) | `[ ]`/`[/]`(7건)/`[x]` | `[ ]`/`[x]`/`[~]` + ✅/취소선 | `[ ]`/`[x]`/`[~]`; lint 파서는 `[/]`도 허용, 변형 표기는 오류(fail-closed) | — | `[ ]`/`[x]`/`[~]` 규정, 실제 `[/]` 4건 사용 | `READY`/`BLOCKED`/`IN_PROGRESS`/`DONE` + 우선순위 P0~P3 + Gate G0~G6 |
| 요약 형식 | 산문 + 체크리스트 | `- [ ] **T-NNN**: …` | 한 줄 산문(30줄 이내) | `- [ ] **T-NNN** — 제목` + 1~3문장 | 평면 한 줄(30줄) + 해제 조건은 `tasks-acceptance.md` | — | 평면 한 줄(23줄) | 5열 표(ID/상태/우선순위/작업/선행) |
| 상세 정본 | — | — | journal | `docs/t2NN-*.md` 보고서(비정형) | `tasks-acceptance.md` | — | `execplan/<task>.md`(다중 경계 변경 시) | `tasks/T-NNN-*.md`(목표·고정 결정·범위·범위 밖·변경 파일·수용 기준·검증 명령·evidence·rollback) |
| 완료 처리 | `[x]` 후 같은 커밋에서 tasks-done 이동 | 완료 절 상단 누적 | tasks-done(번호순) | tasks-done 상단 + journal + resume | tasks-done 상단 + journal + resume; 삭제 게이트 | — | 7단계(구현→검증→PR→CI/live→머지→3문서 갱신→리뷰 코멘트 재확인) | 수용 기준·검증·2인 gate 통과 후 tasks-done newest-first |
| 기계 검사 | — | — | — | — | `tests/lint/test_task_ledger_conventions.py`, `scripts/task_ledger_lint.py`, `scripts/check_task_ledger_deletions.py` | — | — | `tools/validate_plan.py`(상태·우선순위 집합, 선행 DAG, 요약-상세 정합) |

- 사실: map은 2026-08-27 `6d671ef1` 평면화가 열린 항목의 acceptance criteria를 지웠고 다음 날 조건 없이 완료 처리된 사고(`docs/tasks-acceptance.md` 서두, lint 테스트 docstring)를 겪은 뒤 기계 검사를 도입했다. canview의 `validate_plan.py`도 "명령을 적었다는 사실은 실행 증거가 아니다"라는 같은 계열의 규칙을 문서 metadata 검사로 강제한다.

### 1.8 ADR 형식과 번호 규칙

| 항목 | kta | conc | ktdm | geo | map | wx | pinvi | canview |
|---|---|---|---|---|---|---|---|---|
| 파일 | `adr/NNN-<slug>.md` | `decisions.md` `## ADR-N:` | `decisions.md` `## ADR-N:` | `adr/NNN-<slug>.md` | `adr/NNN-<slug>.md` | `adr/NNN-<slug>.md`(map 번호 그대로 072/074/089) | `decisions.md` `## ADR-NNN:` | `adr/NNN-<slug>.md` |
| 번호 | 3자리, 다음 = 008 명시 | 무패딩 1~45 | 무패딩 1~43 | 3자리 001~067(결번 있음), 다음 = 068 명시 | 3자리 001~097, 다음 = 098 명시 | map 번호 이어 ADR-101 자체 발급(추정) | 3자리 001~067 | 3자리 001~007, 다음 = 008(`decisions.md`) |
| 필드 | 상태·날짜·결정자·컨텍스트·결정·근거·결과(긍정)·결과(부정)·후속 (불릿, 굵은 라벨) | 상태·날짜·결정자 불릿 + `###` 컨텍스트/결정/근거/결과(긍정)/결과(부정) | 동일 + `### 후속 (open)` | 상태·날짜·결정자 불릿 + `##` 컨텍스트/결정/근거/결과(긍정)/결과(부정) | kta와 동일(굵은 라벨 불릿) | 산문 단락만(상태·날짜 없음) | kta와 동일 | 상태·날짜(·결정자·Supersedes) 불릿 + `##` 컨텍스트(또는 문맥)/결정/결과/대안 검토/적용 위치/대체 |
| 상태 어휘 | proposed / accepted / superseded by | accepted / superseded by / 채택 | proposed / accepted / superseded by | accepted / superseded by / partially superseded / amended by | 동일 + `→ 이관`, `→ 개발 규칙`, `~~(삭제됨)~~` | — | accepted / superseded by | accepted / superseded by / partially superseded by |
| 범위 규칙 | "프로그램 핵심 구조"만, 프로세스 규칙은 AGENTS/SKILL/runbooks | 전 결정 시간순 누적 | 동일 | 핵심 구조만, 개발 규칙은 SKILL §4로 이관 | 동일 | 구현 적용 ADR만 발췌 | 전 결정 누적, map ADR과 상호 참조 | 여러 subsystem 영향 결정만 |
| 색인 | README 표(제목·상태) | 문서 말미 요약 절 | 상단 표준 형식 블록 | README 표(제목·위치) | README 표 | README 표(적용 내용) | 없음(끝을 기준으로 다음 번호) | README 표 + `decisions.md` 표(상태·제목·위치) |

- 사실: kta의 ADR·runbook 링크는 `](</F:/dev/kor-travel-airport/...>)` 절대 경로다(추적 md 17개). canview `validate_document_links.py`는 `/mnt/f/dev/canview/`·`F:/dev/canview/` 접두를 인식해 해석하지만, 다른 체크아웃 경로(예: `kta-main`)에서는 깨진다.
- 사실(drift): geo `docs/runbooks/README.md` §4는 "main 직접 push 금지 … ADR-021"이라고 인용하지만 geo의 ADR-021은 "도로명주소 일변동 ZIP …"이다. map의 ADR-021이 "main 직접 push 금지"이므로 map 문서를 복사하며 번호가 따라온 것으로 추정한다.

### 1.9 journal/resume 갱신 규칙과 분리(archive)

| 항목 | kta | conc | ktdm | geo | map | wx | pinvi | canview |
|---|---|---|---|---|---|---|---|---|
| journal 제목 형식 | `## YYYY-MM-DD` + 불릿 | `## YYYY-MM-DD: 제목` | `## YYYY-MM-DD — 제목` 산문 | `## YYYY-MM-DD (제목, by agent)` | `## YYYY-MM-DD — 제목` | — | `## YYYY-MM-DD (agent) — T-NNN: 제목` | `## YYYY-MM-DD (agent, 제목)` + 작성자 실제 검증 표 |
| journal 필드 규약 | 없음 | 없음 | 없음 | agent-guide §4: 작업/변경 파일/결정/발견/다음 | 동일 | — | 동일 | documentation-maintenance §4: 도구 fallback·미실행 검증·사용자 변경 보존 여부 |
| 기존 항목 수정 | — | — | — | "절대 수정하지 않는다" | — | — | — | 사실 오류 correction 외 금지 |
| resume 형식 | `## 현재 상태` 불릿 | — | — | `## 현재 진척도 (날짜, by)` 항목당 ✅ 장문 | `## 날짜 — 제목` + 표 + `### 다음 한 작업` | — | `## 날짜 (agent) — 제목` + "다음에 만질 사람이 알아야 할 것" + `**다음 한 작업**` | `현재 진척도 / 다음 한 작업 / 현재 열린 핵심 경로 / 알려진 차단 조건 / 문서 정본` |
| 갱신 트리거 | 작업 후 체크리스트(항상) | journal·tasks(항상), CHANGELOG(배포 시) | journal·tasks(항상) | 결정·기록 5종 중 관련된 것 | 동일 | — | 동일 + 문서만 바꿔도 3문서 중 관련 것 | "직접 관련된 기록만"(표로 조건 명시) |
| archive 규약 | — | — | — | — | tasks-rule §8: 경계 2026-07-26, `archive/{resume,journal,tasks-done}-YYYY-MM[a\|b\|c].md`, 220 KiB 상한, live 상단 색인 표, `tests/unit/test_docs_archive_links.py` | — | — | — |
| 256KB 초과 파일(사실) | — | journal 367KB | journal 564KB | journal 590KB | (분리 후 없음) | — | journal 777KB, resume 400KB | — |

- 사실: map은 archive 규칙 도입 시점 실측(journal 1046KB, resume 287KB)이 에이전트 read 한도 256KB를 넘어 통째로 읽히지 않았다고 기록한다. 현재 conc·ktdm·geo·pinvi가 같은 상태다.

### 1.10 CHANGELOG 규약

| 항목 | kta | conc | ktdm | geo | map | wx | pinvi | canview |
|---|---|---|---|---|---|---|---|---|
| 존재 | — | 있음 | — | 있음 | 있음 | — | 있음 | 있음 |
| 형식 | — | 날짜 절 `## 2026-09-01` + Added/Changed | — | Keep a Changelog + SemVer 명시, `[Unreleased]` | Keep a Changelog 명시, `[Unreleased]` 아래 날짜 H3 | — | `## Unreleased` 불릿 목록 | `[Unreleased]` + Added/Changed, "사용자에게 보이는 변경" |
| 갱신 조건 | — | 사용자 가시 변경(배포 시) | — | 사용자 가시 변경 | 사용자 가시 변경 | — | 사용자 가시 변경 | 사용자 가시 변경 |

### 1.11 개발 환경 정본

| 항목 | kta | conc | ktdm | geo | map | wx | pinvi | canview |
|---|---|---|---|---|---|---|---|---|
| 정본 | WSL2(1차 셸, 2차 WSL2+Docker); Windows PowerShell은 배포 스크립트·원격 확인 보조 | Linux Docker 전용 런타임(ADR-23) + 모든 개발·git·gh·codegraph 명령 WSL2 bash(ADR-33) | Linux/WSL 전용(git·CodeGraph 포함), PowerShell/CMD 금지 | Linux-only(ADR-065), NTFS worktree `/mnt/f/…` + WSL ext4 테스트 미러 | Linux/WSL(git·gh·codegraph 포함), NTFS는 보관 위치 | 미명시(README 빠른 시작이 `/mnt/f/dev/kor-travel-weather`, CI ubuntu) → 후보: Linux/WSL | Linux worktree = source of truth(ADR-051; ADR-024 미러 모델·ADR-017 Windows git 수정안 supersede) | **Windows PowerShell + native 도구**(ADR-003/005), WSL은 보조 |
| Playwright | WSL2 기준, Chromium 불가 시 PowerShell 대체 허용 | n150 live/Linux 우선, 불가 시 Windows fallback(사유 기록) | n150 우선, 불가 시 Windows 예외(사유 기록) | n150 우선, 불가 시 Windows fallback(사유·명령 기록) | n150 우선, 불가 시 Windows 브라우저 fallback | 미확인 | **N150 전용**, 불가 시 Windows 우회 없이 gate 중단 | Playwright+Edge 오프라인(Windows) |
| 줄바꿈 | `*.sh` LF 강제(주석: n150 배포 시 CRLF 사고) | `* text=auto eol=lf` | `* text=auto eol=lf`(2026-08-31 579줄→30,240줄 diff 사고 주석) | 확장자별 LF | `* text=auto eol=lf` | `* text=auto eol=lf` | `* text=auto eol=lf` | hardware 파일만 LF 지정 |
| 환경 문서 | `docs/dev-environment.md`(실행 위치 표) | `docs/dev-environment.md` | `docs/dev-environment.md` + SKILL §2 표 | `docs/dev-environment.md`, `codegraph-worktree.md`, `windows-reinstall-recovery.md` | 동일 | `docs/dev-environment.md`(명령만) | `docs/dev-environment.md`, `runbooks/codegraph-worktrees.md` | `docs/development/windows.md`, `toolchains.md`, `tools/toolchain-versions.json` |

### 1.12 worktree 정책

| 항목 | kta | conc | ktdm | geo | map | wx | pinvi | canview |
|---|---|---|---|---|---|---|---|---|
| 모델 | 없음(메인 체크아웃 + `codex/` 브랜치; journal이 map 패턴 도입 거부 기록) | AGENTS에 규정 없음. 루트 json 4개의 `cwd`가 `F:\dev\kor-travel-concierge-{claude,codex,antigravity,opencode}`를 가리켜 고정 worktree 4개가 **암묵** | 에이전트별 고정 worktree 3개(`…-antigravity/-claude/-codex`) + `opencode.json` filesystem `…-opencode` | 고정 worktree 3개 `/mnt/f/dev/kor-travel-geo-{codex,claude,antigravity}` + idle 브랜치 `agent/<agent>-idle` + ext4 미러 | 고정 worktree 3개 `F:\dev\kor-travel-map-<agent>` + `sandbox/<agent>` 동기 브랜치, trunk는 사람 전용 | 없음 | 고정 worktree 3개 `/mnt/f/dev/pinvi-<agent>` + idle 브랜치, trunk 편집 금지 | **임시 worktree**(ADR-003): 기본은 `F:/dev/canview` 작업 브랜치, 병렬·격리·독립 리뷰 때만 `F:/dev/canview-wt/<agent>-<task>`, merge/abandon 후 제거 + `git worktree prune` |
| 리뷰용 worktree | — | — | — | — | — | — | — | `worktree add --detach F:/dev/canview-wt/review-<id> <commit>` |
| 로컬 파일 복사 | — | `*.local.md`를 각 worktree에 수동 복사 | 동일 | 동일(+`.env`, `settings.local.json`) | 동일 | — | 동일(+`.env.mcp-telegram`) | — |

### 1.13 codegraph 사용 규칙

| 항목 | kta | conc | ktdm | geo | map | wx | pinvi | canview |
|---|---|---|---|---|---|---|---|---|
| 채택 | 미채택(설정 파일에 codegraph 없음) | MCP(`npx @colbymchenry/codegraph serve --mcp`, worktree별 `cwd`) | `init -i` 1회, 작업 시작 `sync`, Linux에서만 | `init -i` 1회, branch 전환·pull·merge 후 `sync`→`status`, UI primitive 수정 전 `codegraph_explore` | 시그니처 변경 전 영향도 평가 **필수**(`explore`/`callers`/`impact`), `docs/codegraph-worktree.md` §7 | 미채택(gitignore 주석만 map 복사) | `codegraph_explore` 선평가 **필수**, 명령 표, Linux native 강제(PATH shim 검사) | "설치되어 있고 유용할 때만", 임시 worktree에서 `init -i`, 전환 후 `sync`, 분석 전후 `status`; 없으면 `rg`로 대체하고 한계 기록 |
| `.codegraph/` gitignore | — | 있음 | 있음(DO NOT 6) | 있음 | 있음 | 있음 | 있음 | 있음 |
| MCP 등록 | — | 4개 json + `.codex/config.toml` | 4개 json + `.codex/config.toml` + `.gemini/mcp.json` | `antigravity.json`·`opencode.json`·`.mcp.json`·`.codex/config.toml`(`codegraph` 바이너리, cwd `.`) | `.mcp.json`(Claude, cwd `F:\dev\kor-travel-map-claude`), codex `--no-watch` + cwd `/mnt/f/…` | — | 3개 json + `.codex/config.toml` + `.gemini/mcp.json` | 없음 |

### 1.14 브랜치/PR 명명

| 항목 | kta | conc | ktdm | geo | map | wx | pinvi | canview |
|---|---|---|---|---|---|---|---|---|
| 브랜치 | `codex/<topic>` + Draft PR | feature 브랜치(접두 규칙 미명시) | `agent/<topic>` from main | `agent/<agent>-<task>` from `origin/main` | `feat\|fix\|chore\|docs\|refactor\|adr/<topic>` + `sandbox/<agent>` | feature 브랜치, Draft PR 우선, CI는 `feat/**` push에도 실행 | `feat/ fix/ chore/ docs/ refactor/ adr/ agent/<agent>-<topic>` | `agent/<agent>-<task>` from `origin/main` |
| merge 방식 | squash(journal 기록) | 미확인 | 미확인 | 미확인 | 미확인 | 미확인 | Squash and merge 권장, 브랜치 삭제 | 미확인 |
| PR 본문 | 미규정 | 미규정 | 미규정 | agent-guide §7.5.3(추정: map과 동일 템플릿) | 동기/변경/영향/검증/문서/관련 | 미규정 | 동기/변경/영향/검증/문서/관련 | task·목적 / gate+명령 / 2인 리뷰 영역·report·disposition / 실패·미실행 검증 / evidence·digest / rollback |

### 1.15 CI green + review 승인 규칙

| 항목 | kta | conc | ktdm | geo | map | wx | pinvi | canview |
|---|---|---|---|---|---|---|---|---|
| 워크플로 | `ci.yml`(3 job) | **없음**(`.github` 미추적) | `ci.yml` | `ci.yml`, `openapi.yml` | 6개(ci·lint·openapi·frontend·docker-images·postgis-only) | `ci.yml` | 8개(api·web·etl·aggregate-ci 필수 gate·docker-images·codex-pr-review·codex-pr-monitor·README) | **없음**(T-001이 `ci.yml` 계획) |
| merge 조건 | CI + James/Popper + live E2E; branch protection은 문서만 있고 미적용(`404 Branch not protected`, 2026-08-23) | PR 후 머지 | fast lint·build 통과 | CI green 후 머지(ADR-021 인용은 drift, §1.8) | CI green + **1 review approval**(ADR-038), `runbooks/branch-protection.md` | PR 필수 | aggregate-ci 통과; 단일 작성자라도 PR 화면 확인 후 머지; CI 리마인더 봇(외부 LLM key 없음) | CI·필수 reviewer gate·미해결 P0/P1 확인 전 merge 금지 |

### 1.16 push 전 보안 감사 절차

| 항목 | kta | conc | ktdm | geo | map | wx | pinvi | canview |
|---|---|---|---|---|---|---|---|---|
| 절차 | 없음(금지 5 중 "백업 파일·SQLite·.env·API key 미추가") | 5단계: staged 파일 점검 → diff grep(공통 패턴) → `.env.example` placeholder → 신규 파일 비밀 운반체 점검 → 통과 시 push | conc와 동일(+`docker-compose.override.yml`) | 6단계: `git diff --staged` 직접 읽기 → grep → 로컬 비밀 파일 확인 → **`git add -A/.` 금지** → 인증·세션 변경 시 `/security-review` → 의심 시 사용자 확인 | 4단계: staged 점검 → grep → `scripts/check_prod_redaction.py`(pre-commit·CI) → 프로젝트별 민감값 grep | 없음 | conc와 동일 4단계 + ADR-047(공개 repo, 도메인 비노출) | §8 + runbook §7: 경로별 명시 stage, **`git add -A/.` 금지**, staged diff 직접 읽기, secret·VIN·key·private material 검사, 생성물·링크·index 정합 |
| grep 패턴 | — | `api[_-]?key\|secret\|password\|passwd\|token\|pbkdf2_sha256\|AKIA…\|BEGIN … PRIVATE KEY` | 동일 | 프로젝트별 패턴은 `deploy-runbook.local.md` §6 | conc와 동일 + redaction 스크립트 | — | conc와 동일 | 패턴 미명시 |
| 완료 알림 | — | — | — | — | — | — | `mcp-telegram` `send_message`로 PR 링크 발송(모든 agent) | — |

### 1.17 `*.local.md` / `.env` 취급

| 항목 | kta | conc | ktdm | geo | map | wx | pinvi | canview |
|---|---|---|---|---|---|---|---|---|
| `.gitignore` | `.env`, `.env.*`, `!.env.example`, `!.env.server14.example`, `.claude/settings.local.json`; **`*.local.md` 없음** | `.env*` 계열, `.codegraph/`, `.local/`, `*.local.md` | `.env*`, `.codegraph/`, `.local/`, `*.local.md`, `*.local.sh` | `.env`, `.env.*`, `!.env.*.example`, `.codegraph/`, `*.local.md`(+`.git/info/exclude`) | `.env*`, `.codegraph/`, `*.local.md`, `docs/deploy-runbook.local.md`, `docs/prod-access.local.md`, `.security-audit-patterns.local` | `.env*`, `deploy/*.env`, `.codegraph/`, `*.local.md`, `docs/deploy-runbook.local.md`, `docs/prod-access.local.md` | `.env`, `.env*.local`, `.env.prod`, `.env.production`, `.env.mcp-telegram`, `*.local.md`, `.local/`, `.codegraph/` | `.claude/`, `.codegraph/`, `.env`, `.env.*`, `!.env.example`, `*.local.md`, `.tools/`, `evidence/private/` |
| 로컬 정본 문서 | — | `docs/deploy-runbook.local.md`(prod 절차·민감정보) | 동일 | 동일 + `docs/prod-access.local.md` | 동일 2개 | (gitignore만 복사) | 동일 + `m05-e2e-analysis.local.md` | — |

### 1.18 벤더링 스킬 디렉터리와 설정 파일 관례

| 항목 | kta | conc | ktdm | geo | map | wx | pinvi | canview |
|---|---|---|---|---|---|---|---|---|
| `.agents/skills/` | postgres 계열 8개(23파일) | 동일 | 동일 | 동일 | 동일 | — | 동일 | — |
| `.claude/` | `agents/`(5 + README) + `skills/`(8) | `agents/` + `skills/` | 동일 | 동일 + `settings.json`(statusLine `python-kraddr-geo` — 옛 이름) | `agents/`(+README) + `skills/` | — | `agents/` + `skills/` + `settings.json`(expo plugin) + `scheduled_tasks.lock` | 전체 gitignore |
| `.codex/` | `agents/`(6 toml) + `config.toml`(playwright·sequential-thinking만) | `agents/` + `config.toml`(codegraph cwd `F:\…-codex`) | 동일 | `config.toml`(`codegraph` 바이너리, filesystem `.`) | `config.toml`(codegraph `--no-watch`, cwd `/mnt/f/…-codex`; filesystem은 `F:\…`) | — | `config.toml`(+`mcp-telegram` `C:\Python314\python.exe`) | — |
| `.opencode/` | — | `agent/`(6) + `skills/`(8) | 동일 | `agent/` + **`skill/`**(단수 디렉터리명) | `agent/`(6)만 | — | — | — |
| `.gemini/mcp.json` | — | — | 있음 | — | 있음 | — | 있음 | — |
| 루트 설정 | 없음 | `antigravity.json`·`claude.json`·`codex.json`·`opencode.json`(worktree별 절대 `cwd`) | 동일 4개 | `antigravity.json`·`claude.json`·`opencode.json`·`.mcp.json`(이식 가능한 `.`/바이너리 형식) | `antigravity.json`·`claude.json`·`opencode.json`(`instructions: ["AGENTS.md","SKILL.md"]`)·`.mcp.json` | 없음 | `antigravity.json`·`claude.json`·`codex.json`(Telegram 포함) | 없음 |
| `.hallmark/` | `log.json`, `preflight.json` | — | `log.json` | `log.json`, `preflight.json` | — | — | `log.json`, `preflight.json` | — |

- 사실: pinvi는 Linux-only(ADR-051)이지만 세 설정 파일이 `C:\Python314\python.exe`와 `F:\dev\pinvi-<agent>`를 가리킨다. map도 `.mcp.json`은 `F:\…`, codex는 `/mnt/f/…`로 혼재한다. geo만 경로 비의존 형식이다.

### 1.19 문서 검증 도구

| 항목 | kta | conc | ktdm | geo | map | wx | pinvi | canview |
|---|---|---|---|---|---|---|---|---|
| 링크 검사 | — | — | — | — | `tests/unit/test_docs_archive_links.py`(markdown-it, archive 한정, 220KiB 상한) | — | — | `tools/validate_document_links.py`(docs·hardware·루트 md 전체, 절대 접두 2종 해석, fence 제외) |
| task 원장 검사 | — | — | — | — | `scripts/task_ledger_lint.py` + `tests/lint/test_task_ledger_conventions.py` + `scripts/check_task_ledger_deletions.py` | — | — | `tools/validate_plan.py` + `tests/test_plan_validation.py` |
| 민감정보 검사 | — | grep 절차(수동) | grep(수동) | grep(수동) + `/security-review` | `scripts/check_prod_redaction.py`(pre-commit·CI) | — | grep(수동) | 수동 |
| 중복 선언 검사 | — | — | `docs/bindings.md` 등록부(DO NOT 15 유도→결박→탐지) | — | — | — | — | — |
| cross-repo drift | `runbooks/cross-repo-audit-checklist.md` | `docs/cross-repo-consistency-actions-*.md` | — | — | `runbooks/cross-repo-audit-checklist.md`(분기 1회 4-repo) + `integration-map.md` | `integration-map.md` | `docs/reviews/…cross-repo-decisions.md` | — |

### 1.20 design.md와 디자인 규칙 문서

| 항목 | kta | conc | ktdm | geo | map | wx | pinvi | canview |
|---|---|---|---|---|---|---|---|---|
| 루트 파일 | `design.md`(영어, Hallmark 2026-08-22, OKLCH 토큰 `frontend/src/app/tokens.css`) | `design.md`(한국어, map admin `Rail-Workbench` 기준, 보라 브랜드 유지) | `DESIGN.md`(한국어, Hallmark 2026-08-13, Ember 테마, Rail-Workbench) | `design.md`(한국어, editorial-utilitarian Workbench, `app/globals.css` OKLCH 청색) | — | — | `DESIGN.md`(Airbnb reference 영어 + 한국어 적용 메모, `docs/design/styleseed-rules.md`) | — (`docs/ui/design.md`, `tokens.css`) |
| 보조 | `docs/reports/hallmark-audit-2026-08-22.md` | — | `docs/DESIGN-RULES.md`, `docs/design-system.md` | — | `docs/architecture/admin-frontend-design-rules.md` | — | `docs/design/marker-palette.md`, `packages/design-tokens` | `docs/ui/lvgl-demo-review.md` |

- 사실: conc·ktdm·geo `design.md`는 모두 "map admin의 Rail-Workbench 구조를 가져오되 자기 색상톤은 유지"를 명시한다. 색상 톤·UX 가이드가 이미 저장소 간 참조 관계로 존재하며 common의 "규칙 산출물" 전제와 부합한다.

---

## 2. canview 구조를 common 기준으로 채택할 때의 충돌과 해결 제안

| # | 충돌 항목 | canview | kor-travel 관례(근거) | 해결 제안(후보) |
|---|---|---|---|---|
| C1 | 개발 환경 정본 | Windows PowerShell native(ADR-003/005) | 7개 중 6개가 Linux/WSL: conc ADR-23/33, ktdm AGENTS·SKILL §2, geo ADR-065, map AGENTS, pinvi ADR-051, kta WSL2 테스트 기준; wx는 미명시(Linux 추정) | common 공통 절은 **OS를 규정하지 않고** "정본 환경은 저장소 `docs/dev-environment.md`와 ADR이 선언"으로 위임. 공통 runbook의 명령 예시는 bash 기본으로 쓰고 PowerShell 블록은 두지 않는다. common 자체 저장소는 Linux/WSL을 정본으로 채택(다수·CI ubuntu·Node 툴체인). canview ADR-003의 논거 중 OS와 무관한 부분(장기 worktree 정리 누락)은 C2로 분리 |
| C2 | worktree 모델 | 임시 worktree, merge/abandon 후 제거 | 고정 worktree 3~4개: ktdm, geo(ADR-034→041→065), map(`codegraph-worktree.md`), pinvi(ADR-017/051); conc는 설정 파일로 암묵; kta·wx 없음 | 두 프로필을 모두 허용하는 공통 불변 조건만 규정: (1) 같은 브랜치를 두 worktree에서 checkout 금지, (2) trunk는 사람 전용, (3) 브랜치 `agent/<agent>-<task>`, (4) worktree별 CodeGraph 수명주기, (5) merge/abandon 후 임시 worktree 제거·prune. 저장소는 "고정 프로필" 또는 "임시 프로필"을 `dev-environment.md`에 선언. common 자체는 임시 프로필(작은 라이브러리) |
| C3 | `CLAUDE.md` 존재 | 없음(`.claude/` 전체 gitignore) | 6개가 보유. 두 유형: 1쪽 요약(kta·map·pinvi) / 현황·컨텍스트(conc·ktdm·geo). pinvi ADR-016은 양방향 동기 필수 | 공통 표준: `AGENTS.md`가 단일 정책 정본, `CLAUDE.md`는 **40줄 이하 포인터**(진입 순서와 정본 링크만, 사실 복제 금지). kta의 "상충 시 CLAUDE.md를 고친다" 규칙을 채택하고 pinvi ADR-016의 양방향 동기 부담은 포인터화로 해소. `.claude/`는 gitignore 하되 `CLAUDE.md`는 추적 |
| C4 | `SKILL.md` 역할 | 라우터, 정책 복제 금지(ADR-004) | 매뉴얼 + DO NOT 정본(geo·map은 ADR에서 SKILL §4로 이관 완료) | 공통 절대 금지(≤5)는 `AGENTS.md`에, 도메인 DO NOT은 `SKILL.md` §4에 유지(이관 churn 회피). SKILL에 "작업별 시작점 표"(canview §2)를 추가해 라우터 기능을 흡수. 정책 문장을 두 파일에 복제하지 않는 규칙만 공통화 |
| C5 | 지시 우선순위 | 사용자 > AGENTS > accepted ADR > architecture > task > 분야 문서 > 코드 > 역사 > 가정 | pinvi만 ADR > AGENTS; 나머지는 AGENTS > SKILL > 문서군 | 공통 순위: 사용자 > `AGENTS.md`(공통 절+로컬 절) > accepted ADR > `SKILL.md`·architecture > 상세 task > 나머지 docs > 코드·테스트 > review·journal(역사) > 최소 가정. pinvi는 ADR 1순위를 로컬 ADR로 유지할지 결정 필요(열린 질문 Q3) |
| C6 | task 원장 형식 | 5열 표 + `READY/BLOCKED/IN_PROGRESS/DONE` + P0~P3 + 상세 파일 필수 | 체크박스 한 줄 원장(`[ ]/[x]/[~]/[/]`), 상세는 `tasks-acceptance.md`(map)·`execplan/`(pinvi)·보고서(geo) | 공통 원장은 체크박스 형식(다수)으로 하고 상태 대응표를 둔다: `[ ]`=READY 또는 BLOCKED(보류 사유 1줄), `[/]`=IN_PROGRESS, `[~]`=부분 완료, `[x]`=DONE(map lint 파서가 이미 4종 허용). 비단순 task는 `docs/tasks/T-NNN-*.md` 상세 파일(canview 필수 항목 9개)을 요구하고 `tasks-acceptance.md`·`execplan/`은 그 파일로 수렴. 우선순위 P0~P3와 선행 열은 표 대신 entry 꼬리표 `(P1, 선행 T-012)`로 |
| C7 | 리뷰 gate | 2인 독립 + immutable 기준선 + evidence 파일 + P0~P3 + disposition 4종 + archive | kta James/Popper(P0~P2, journal 기록); 나머지는 실행 흔적만 | 공통 gate를 2단계로: **full**(정책·계약·인증·공용 UI primitive·common 배포물 변경)은 canview 형식 그대로; **light**(그 외 비단순 변경)는 2인 독립 리뷰 결과를 PR 본문과 journal에 요약(kta 방식). 심각도 P0~P3와 disposition 어휘(`OPEN/FIXED/REJECTED_WITH_EVIDENCE/DEFERRED`)는 두 단계 공통. James/Popper 같은 페르소나명은 로컬 |
| C8 | ADR 저장·번호 | 파일당 1개 3자리 + README + decisions.md 색인 | 단일 `decisions.md`(conc·ktdm·pinvi, 무패딩 포함), 파일당 1개(kta·geo·map·wx) | 공통 표준은 파일당 1개 `docs/adr/NNN-<slug>.md` + `docs/adr/README.md` 색인(다음 번호 명시). 단일 파일 저장소는 재번호 없이 유지하고 신규 ADR부터 파일 분리(선택). cross-repo 참조는 `<repo> ADR-NNN` 표기(pinvi 관례). wx처럼 타 저장소 번호를 미러하는 방식은 금지(common ADR은 001부터) |
| C9 | journal/resume 비대화 | 작음 | conc·ktdm·geo·pinvi가 256KB 초과, map만 archive 규약 | map `tasks-rule.md` §8(220KiB, `archive/…-YYYY-MM[a\|b\|c].md`, 색인 표, 링크 테스트)을 공통 규약으로 채택. canview `documentation-maintenance.md` §4의 "resume는 짧게" 원칙을 병합 |
| C10 | 언어 예외 | 벤더링 없음 | 벤더링 영어 예외(kta·map 명시, 4개 암묵), 원칙 제목 영어(kta 명시), design 문서 영어 2건, wx 영어 제목 | 공통 언어 절에 예외 3종 명시: 벤더링 원문, 원칙 소제목, 인용 reference(원문 유지 시 한국어 적용 메모 필수). `design.md`는 한국어 본문을 요구(kta·pinvi는 이행 대상) |
| C11 | 링크 표기 | 상대 링크 + 검증 도구가 절대 접두 2종 허용 | kta 17개 md가 `</F:/dev/kor-travel-airport/...>` 절대 링크 | 공통 규칙: 저장소 상대 링크만 허용, 절대 경로 링크 금지. 검증 도구는 절대 링크를 오류로 보고(canview 도구의 접두 허용은 common에서 제거) |
| C12 | 검증 도구 언어 | Python `tools/*.py` + `py -3` | map은 pytest 기반, 나머지 없음 | Python 스크립트를 유지하되 실행 명령은 `python3`/`uv run`로 표기. common은 Tailwind/React 라이브러리지만 저장소 도구는 Python으로 두어도 소비자 7개 전부 Python을 보유하므로 장벽 없음(wx는 uv). 대안: Node 스크립트 — 미결(열린 질문 Q5) |
| C13 | 설정 파일 경로 | 없음 | worktree별 절대 `cwd`(conc·ktdm·map·pinvi), 이식형(geo) | 공통 관례: geo 형식(`codegraph serve --mcp`, filesystem `.`)을 표준으로, 절대 경로는 로컬 override. `opencode.json`의 `instructions: ["AGENTS.md","SKILL.md"]`(map)를 표준 포함 |
| C14 | CI green 전제 | 워크플로 없음(계획) | conc도 없음; 나머지 있음 | "CI green"은 필수 체크가 존재하는 저장소에서만 gate이며, 없는 저장소는 로컬 4 게이트 결과를 PR 본문에 기록하고 `runbooks/branch-protection.md`에 required check 이름을 등록할 때까지 미적용 상태를 명시 |
| C15 | `.gitattributes` | hardware만 LF | 6개가 `* text=auto eol=lf` 또는 확장자별 LF(사고 기록 2건) | 공통: `* text=auto eol=lf` + 바이너리 목록 |
| C16 | 문서 유지 규칙 위치 | `runbooks/documentation-maintenance.md` 단독 | `agent-guide.md`(geo·map·pinvi)에 진입·기록 5종·ADR 규약·journal/resume 형식·PR 워크플로 통합 | 공통은 canview 분할(tasks-rule / documentation-maintenance / agent-workflow)을 채택하고, `agent-guide.md`는 세 문서로의 포인터 stub로 전환(삭제 아님) |

---

## 3. common이 배포할 "공통 에이전트/문서 규약" 초안

### 3.1 각 저장소가 그대로 채택할 `AGENTS.md` 공통 절

`AGENTS.md`를 "공통 절(common이 배포, 문구 고정)"과 "로컬 절(저장소 소유)"로 나눈다. 공통 절은 아래 순서·제목으로 배포하고, 저장소는 문구를 바꾸지 않고 로컬 절만 추가한다.

| 순서 | 공통 절 제목 | 내용 출처 | 채택 근거 |
|---|---|---|---|
| A | 작업 원칙 — Think Before Coding / Simplicity First / Surgical Changes / Goal-Driven Execution / Practical Bias | 6개 저장소 동일 문구(§1.4) + geo의 2개 추가 불릿(테스트 실패 선확인, 가드 실측) 채택 여부는 열린 질문 Q1 | 문구 동일 |
| B | Ruthless Review 4개 불릿 | canview §2 | 리뷰 gate의 태도 근거 |
| C | 문서 언어 정책 + 예외 3종 | kta·map 예외 문구 + conc 영어 유지 목록 | §1.3 |
| D | 지시 우선순위(9단계) | C5 | |
| E | 문서 읽기 정책(반드시 / 필요할 때 / 특수) + 토큰 절약 규칙 | canview §3 | kor-travel에 없음 |
| F | 절대 하지 말 것 — 공통 5: main 직접 push, 비밀·`*.local.md`·`.env` 커밋, `git add -A/.`, 미실행 gate를 통과로 표시, 한 사실 두 곳 독립 선언(ktdm DO NOT 15) | 각 저장소 DO NOT 교집합 | 도메인 DO NOT은 SKILL 로컬 |
| G | 완료와 push — 검증·2인 리뷰·기록 갱신·보안 감사 5단계(grep 패턴 포함)·머지 조건 | canview §8 + conc/ktdm/pinvi 절차 + geo `git add -A` 금지·`/security-review` | §1.16 |
| H | 기록 갱신 규칙(결정·기록 5종: ADR / resume / journal / tasks+tasks-done / CHANGELOG, "직접 관련된 것만") | geo agent-guide §2 + canview documentation-maintenance §2 표 | |
| I | 개발 환경·worktree·CodeGraph 진입점(프로필 선언은 `docs/dev-environment.md`) | C1·C2 | |

로컬 절(저장소 소유): 목표·역할·식별자 표, 개발 환경 프로필과 경로, 도메인 DO NOT, 포트, provider/형제 라이브러리 원칙, 검증 명령, 배포·prod 규칙, 완료 알림(Telegram) 등.

### 3.2 `docs/` 트리 표준

| 경로 | 필수 | 정본 역할 | 출처 |
|---|---|---|---|
| `docs/README.md` | 필수 | 문서 지도(3단계 읽기, 정본 관계 트리) | canview |
| `docs/resume.md` | 필수 | 현재 상태·다음 한 작업·차단 조건(짧게) | canview §4 + geo/map 형식 |
| `docs/journal.md` | 필수 | 역시간순 일지, 5필드(작업/변경/결정/발견/다음), 기존 항목 불변 | geo/map agent-guide §4 |
| `docs/tasks.md`, `tasks-done.md`, `tasks-rule.md` | 필수 | §3.3 | |
| `docs/tasks/T-NNN-*.md` + `tasks/README.md` | 비단순 task | 상세 명세 9항목 | canview |
| `docs/adr/README.md` + `NNN-<slug>.md` | 필수 | 구조 결정, 다음 번호 명시 | kta·geo·map·canview |
| `docs/architecture/README.md` + 상세 | 필수 | 현재 설계 정본 | |
| `docs/dev-environment.md` | 필수(로컬) | OS·worktree 프로필·명령 | 6개 저장소 보유 |
| `docs/runbooks/README.md`, `agent-workflow.md`, `agent-failure-patterns.md`, `documentation-maintenance.md` | 필수 | 절차 정본 | canview + geo/map |
| `docs/reviews/README.md`, `adversarial/TEMPLATE.md`, `adversarial/evidence/` | 필수 | 리뷰 archive | canview |
| `docs/archive/` | 조건부(220KiB 초과 시) | resume/journal/tasks-done 분리 | map §8 |
| `docs/reports/`, `docs/sprints/`, `docs/execplan/`, `integration-map.md`, `ports.md` | 선택(로컬) | | map·pinvi·ktdm |
| 루트 `CHANGELOG.md` | 필수 | Keep a Changelog 한국어, `[Unreleased]`, 사용자 가시 변경만 | geo·map·canview |
| 루트 `DESIGN.md` | UI 보유 저장소 필수 | 색상 톤·구조·토큰 위치(한국어) | conc·ktdm·geo |

### 3.3 `tasks-rule.md` 공통 규약

1. 역할: `tasks.md`(열린 항목만) / `tasks-done.md`(newest-first) / `resume.md`(진척 정본) / `tasks/T-NNN-*.md`(상세) / `archive/`(분리 이력).
2. ID: `T-NNN` 연번, 하위 `T-NNN<letter>`, 파생 `T-NNN-<slug>`; 참조된 ID 재번호 금지(geo·map·pinvi·ktdm 공통), 번호대 예약은 로컬 선택.
3. 마커: `[ ]` 열림(보류 사유 1줄 허용) / `[/]` 진행 중 / `[~]` 부분 완료 / `[x]` 완료; 변형 표기는 오류(map lint 규칙).
4. entry: `- [ ] **T-NNN** — 제목 (P1, 선행 T-012)` + 1~3문장; 수용 기준은 상세 파일이 소유하고 요약에 복제하지 않는다.
5. 완료: 수용 기준·검증·(비단순이면) 2인 gate 통과 → tasks-done 상단 + journal + resume; 실패 검증·미해결 P0/P1을 남기고 DONE 금지.
6. archive: map §8 그대로.
7. 기계 검사: `tools/validate_plan.py`(canview) 규칙을 체크박스 원장에 맞게 이식한 `validate_task_ledger.py`(후보)로 요약-상세 정합·마커·ID 재사용을 검사.

### 3.4 review gate 공통 규약

- 대상·면제: canview `agent-workflow.md` §5 비면제 목록에서 하드웨어·차량 항목을 제거하고 "공용 UI primitive·디자인 토큰·OpenAPI 계약·인증·정책 문서(`AGENTS.md`·`SKILL.md`·`docs/README.md`·ADR·runbook·task/review 규칙)"로 치환.
- 실행: 전문 영역이 다른 리뷰어 2인 독립, 상대 결과 비공개, 동일 manifest, immutable 기준선(object-only 또는 detached worktree), verdict `BLOCK/CONDITIONAL/PASS`.
- 심각도 P0~P3 표, disposition `OPEN/FIXED/REJECTED_WITH_EVIDENCE/DEFERRED`(P2/P3만, owner·task·gate·기한).
- 기록: full 단계는 `docs/reviews/adversarial/YYYY-MM-DD-<scope>.md` + evidence 파일 + index 한 행; light 단계는 PR 본문 + journal. 과거 report에 append 금지, closure artifact 예외.
- post-fix 재검토 2인, P0/P1은 원 reviewer 재확인 전 merge 금지.

### 3.5 로컬로 유지할 항목(공통화하지 않음)

| 항목 | 이유 |
|---|---|
| 개발 환경 OS·worktree 프로필·경로·포트 | 저장소 ADR로 이미 확정(C1·C2) |
| 도메인 DO NOT(geo 11·map 26·pinvi 22·kta 9) | 도메인 종속 |
| provider·형제 라이브러리 원칙, 의존 방향 | 저장소별 |
| 리뷰어 페르소나명(James/Popper), Telegram 완료 알림, `deploy-runbook.local.md`, prod 검증 항목 | 운영 종속·민감 |
| sprints/, execplan/, reports/, integration-map.md, ports.md, bindings.md | 저장소 운영 도구 |
| `.hallmark/` 산출물 취급 | 목적 미확인(열린 질문 Q6) |
| ADR 번호 이력(단일 파일 저장소의 기존 번호) | 재번호 금지 |

---

## 4. kor-travel-common 자체 저장소가 가져야 할 파일 목록 (canview 대응표)

관찰(사실): `F:/dev/kor-travel-common` `b92fabe`는 `LICENSE`만 추적하지만 작업 트리에 미추적 파일이 있다 — `.editorconfig`, `.gitattributes`, `.gitignore`, `.github/workflows/docs.yml`, `docs/reviews/README.md`, `docs/reviews/adversarial/TEMPLATE.md`, `docs/reviews/adversarial/evidence/.gitkeep`, `docs/runbooks/README.md`, `docs/runbooks/documentation-maintenance.md`, `docs/tasks-done.md`, `docs/tasks-rule.md`, `docs/tasks/README.md`, `tests/test_plan_validation.py`, `tools/README.md`, `tools/validate_document_links.py`, `tools/validate_plan.py`, 빈 디렉터리 `docs/adr`, `docs/architecture`, `docs/plan`, `docs/standards`, `docs/survey`. 본 조사는 이 파일들의 내용을 검토하지 않았다(범위 밖). 아래 표의 "상태" 열은 존재 여부만 반영한다.

| canview 파일 | common 대응 파일 | 판단 | 상태 | 비고 |
|---|---|---|---|---|
| `AGENTS.md` | `AGENTS.md` | 변형 | 없음 | §3.1 공통 절 + common 로컬 절(라이브러리 경계: `maplibre-vworld-react`·`maplibre-vworld-js`·`python-*-api`·`python-kraddr-base` 중복 금지, 소비자 7개 목록, 버전 일치 정책 링크) |
| `SKILL.md` | `SKILL.md` | 변형 | 없음 | 라우터 + 작업별 시작점 표 + 용어(토큰·shadcn·OpenAPI·PC/Mobile 규칙) |
| (없음) | `CLAUDE.md` | 추가 | 없음 | 40줄 이하 포인터(C3) |
| `README.md` | `README.md` | 필요 | 없음 | 문서 지도 링크·패키지 목록 |
| `CHANGELOG.md` | `CHANGELOG.md` | 필요 | 없음 | 라이브러리 릴리스와 직결 |
| `LICENSE` | `LICENSE` | 필요 | 있음(GPL-3.0) | |
| `.gitignore`, `.gitattributes` | 동일 | 필요 | 있음(미검토) | `* text=auto eol=lf`, `.codegraph/`, `*.local.md`, `.env*` |
| `tokens.css`(루트) | `packages/<tokens>/…` | 변형 | 없음 | 토큰은 패키지 산출물로, 루트에 두지 않음 |
| `docs/README.md` | `docs/README.md` | 필요 | 없음 | |
| `docs/resume.md`, `journal.md`, `tasks.md` | 동일 | 필요 | 없음 | |
| `docs/tasks-rule.md`, `tasks-done.md`, `tasks/README.md` | 동일 | 필요 | 있음(미검토) | §3.3 반영 여부 확인 필요 |
| `docs/tasks/T-NNN-*.md` | 동일 | 필요 | 없음 | 부트스트랩 task부터 |
| `docs/adr/README.md` + `NNN-*.md` | 동일 | 필요 | 디렉터리만 | 001부터 |
| `docs/decisions.md` | — | 불필요 | 없음 | `adr/README.md` 색인으로 충분(geo·map은 stub) |
| `docs/architecture/README.md`, `system.md`, `features.md`, `automation.md` | `docs/architecture/README.md`, `packages.md`, `consumers.md` | 변형 | 디렉터리만 | 패키지 경계·소비자 채택 상태 |
| `docs/architecture/protocols/` | `docs/standards/openapi.md`(후보) | 변형 | `docs/standards` 디렉터리만 | 규칙 산출물(OpenAPI 규약)의 위치 후보 |
| `docs/architecture/implementation-readiness.md`, `requirements-coverage.md` | `docs/architecture/adoption-readiness.md` | 변형 | 없음 | 저장소별 채택 gate(Tailwind v4 전환·버전 일치) 추적표 |
| `docs/development/windows.md`, `toolchains.md` | `docs/dev-environment.md` | 변형 | 없음 | Linux/WSL 정본(후보), 임시 worktree 프로필 |
| `tools/toolchain-versions.json` + `tools/environment/setup-windows.ps1` | `versions.json`(후보 이름) + `tools/check_versions.py` | 변형 | 없음 | "라이브러리/플랫폼 버전 일치" 정책의 기계 판독 정본 |
| `docs/ui/design.md`, `lvgl-demo-review.md` | 루트 `DESIGN.md` + `docs/standards/{color-tone,ux-guide,responsive-web}.md` | 변형 | 없음 | 규칙 산출물(색상 톤·UX·PC/Mobile Web) |
| `docs/hardware/`, `docs/vehicle/`, `docs/images/` | — | 불필요 | — | `docs/images/`는 UI 스크린샷 필요 시 선택 |
| `docs/runbooks/README.md`, `agent-workflow.md`, `documentation-maintenance.md`, `agent-failure-patterns.md` | 동일 | 필요 | README·documentation-maintenance 있음(미검토), 나머지 없음 | agent-workflow는 C1·C2 반영 |
| `docs/reviews/README.md`, `adversarial/TEMPLATE.md`, `evidence/` | 동일 | 필요 | 있음(미검토) | |
| `tools/validate_document_links.py`, `validate_plan.py`, `tests/test_plan_validation.py` | 동일 | 변형 | 있음(미검토) | 절대 링크 접두 허용 제거(C11), 체크박스 원장 지원(§3.3-7) |
| `.tools/`(gitignore) | — | 불필요 | — | |
| `firmware/`, `hardware/`, `protocol/`, `dbc/`, `ui/`, `tests/`(host) | `packages/*`, `examples/`, 패키지별 `tests` | 변형 | 없음 | 라이브러리 구조는 별도 조사 문서 범위 |
| (없음) | `.agents/`, `.claude/agents+skills`, `.codex/`, `.opencode/` 벤더링 + `antigravity.json`·`claude.json`·`codex.json`·`opencode.json`·`.mcp.json` 템플릿 | 추가 | 없음 | `templates/agent-config/`에 이식형(geo 형식) 템플릿으로 배포(후보) |
| (없음) | `docs/runbooks/branch-protection.md`, `cross-repo-audit-checklist.md` | 추가 | 없음 | kta·map 관례; common은 7개 소비자 drift 점검 주체 |
| (없음) | `docs/integration-map.md` | 추가 | 없음 | 소비자별 채택 버전·패키지 표 |
| (없음) | `.github/workflows/ci.yml` | 추가 | `docs.yml`만 있음(미검토) | 문서 검증 + 패키지 빌드 |

---

## 5. 열린 질문

- Q1. 공통 절 A에 geo의 Goal-Driven 추가 불릿 2개(테스트 실패 선확인, 가드 실측)를 포함할지. 포함하면 5개 저장소의 AGENTS 문구가 바뀐다.
- Q2. `SKILL.md`를 canview식 라우터로 바꿀지(C4). geo·map은 ADR을 SKILL §4로 이관한 이력이 있어 재이관 비용이 있다.
- Q3. pinvi의 "accepted ADR > AGENTS.md" 우선순위를 공통 순위(C5)로 바꿀지, 로컬 예외로 둘지.
- Q4. 리뷰 gate의 full/light 경계(C7)를 누가 판정하는지 — 작성자 자율 판정이면 우회 가능성이 있다.
- Q5. 문서 검증 도구 언어(Python 유지 vs Node)와 실행 명령 표기(`python3` / `uv run` / `py -3`).
- Q6. `.hallmark/log.json`·`preflight.json`(kta·ktdm·geo·pinvi)의 용도와 추적 필요 여부 — 미확인.
- Q7. wx의 개발 환경 정본과 문서 언어(일부 영어) 정비 시점 — AGENTS.md 39줄로 가장 얇아 공통 절 도입 효과가 가장 크다.
- Q8. conc의 CI 부재와 고정 worktree 암묵 규정 — 공통 절 도입 시 `dev-environment.md`에 프로필을 명시해야 한다.
- Q9. 단일 `decisions.md` 저장소(conc·ktdm·pinvi)의 ADR 파일 분리 여부와 시점.
- Q10. kta 절대 경로 링크 17개 파일의 상대 링크 전환 시점.
- Q11. common 작업 트리의 미추적 scaffold(§4)가 본 조사 결론과 정합하는지 별도 검토 필요.

---

## 근거 파일 목록

경로는 저장소 상대 경로, 괄호는 저장소 약칭과 기준 커밋이다.

1. `AGENTS.md` (kta 2bb1111 / conc 7945305 / ktdm 862562d / geo 1d9d74d / map c494e227 / wx 6003da9 / pinvi 9af25e5 / canview d078437)
2. `CLAUDE.md` (kta·conc·ktdm·geo·map·pinvi)
3. `SKILL.md` (kta·conc·ktdm·geo·map·pinvi·canview)
4. `design.md` (kta·conc·geo), `DESIGN.md` (ktdm·pinvi)
5. `CHANGELOG.md` (conc·geo·map·pinvi·canview)
6. `README.md` (canview·wx)
7. `.gitignore`, `.gitattributes` (8개 전부)
8. `antigravity.json`, `claude.json`, `codex.json`, `opencode.json` (conc·ktdm·pinvi 해당분), `.mcp.json` (geo·map), `.codex/config.toml` (kta·conc·ktdm·geo·map·pinvi), `.gemini/mcp.json` (ktdm·map·pinvi), `.claude/settings.json` (geo·pinvi), `.claude/agents/README.md` (kta·map)
9. `docs/README.md` (canview)
10. `docs/tasks-rule.md` (kta·geo·map·pinvi·canview)
11. `docs/tasks.md`, `docs/tasks-done.md` (kta·conc·ktdm·geo·map·pinvi·canview)
12. `docs/tasks-acceptance.md` (map), `docs/tasks/README.md`, `docs/tasks/T-001-host-toolchain-ci.md` (canview)
13. `docs/journal.md`, `docs/resume.md` (kta·geo·map·pinvi·canview), `docs/journal.md` (conc·ktdm)
14. `docs/adr/README.md` (kta·geo·map·wx·canview), `docs/decisions.md` (conc·ktdm·pinvi·wx·canview)
15. `docs/adr/001-postgresql-as-primary-db.md` (kta), `docs/adr/001-postgres-postgis-primary-store.md` (geo), `docs/adr/001-v1-branch-preserve-main-orphan-v2.md` (map), `docs/adr/072-weather-bitemporal.md` (wx)
16. `docs/adr/002-documentation-and-task-structure.md`, `003-windows-development-and-ephemeral-worktrees.md`, `004-layered-documentation-and-review-archive.md` (canview)
17. `docs/adr/034-ai-agent-fixed-worktree-codegraph.md`, `041-ntfs-main-repo-wsl-ext4-test-mirror.md`, `065-linux-only-development-environment.md` (geo)
18. `docs/decisions.md` ADR-016·017·021·024·047·051 (pinvi), ADR-18·23·33·36 (conc)
19. `docs/runbooks/README.md` (kta·geo·map·wx·pinvi·canview)
20. `docs/runbooks/hostile-review.md`, `branch-protection.md`, `agent-failure-patterns.md`, `cross-repo-audit-checklist.md` (kta)
21. `docs/runbooks/agent-workflow.md`, `documentation-maintenance.md`, `agent-failure-patterns.md` (canview)
22. `docs/runbooks/agent-workflow.md` (geo·map), `docs/agent-workflow.md`, `docs/agent-failure-patterns.md` (pinvi)
23. `docs/agent-guide.md` (geo·map·pinvi)
24. `docs/codegraph-worktree.md` (map), `docs/runbooks/codegraph-worktrees.md` (pinvi, 참조만)
25. `docs/reviews/README.md`, `docs/reviews/adversarial/TEMPLATE.md`, `docs/reviews/adversarial/evidence/*` (canview)
26. `docs/reviews/2026-06-10-claude-pr-review.md` (pinvi), `docs/postmerge-review-fixups-*.md` (geo, 14건 존재 확인)
27. `docs/sprints/README.md` (map·pinvi), `docs/archive/*` (map, 18건), `docs/reports/*` (map 94건·kta 1건)
28. `docs/dev-environment.md` (kta·wx), `docs/development/windows.md` (canview), `docs/bindings.md` (ktdm)
29. `docs/integration-map.md` (map·wx, 존재 확인)
30. `tools/validate_document_links.py`, `tools/validate_plan.py`, `tests/test_plan_validation.py` (canview)
31. `scripts/task_ledger_lint.py`, `scripts/check_task_ledger_deletions.py`, `scripts/check_prod_redaction.py`, `tests/lint/test_task_ledger_conventions.py`, `tests/unit/test_docs_archive_links.py` (map)
32. `.github/workflows/*` (kta 1·ktdm 1·geo 2·map 6·wx 1·pinvi 8, conc·canview 0), `.github/workflows/README.md` (pinvi)
33. `.agents/skills/*`, `.claude/skills/*`, `.opencode/*`, `.hallmark/*` (존재·개수 확인)
34. `docs/kor-travel-common-library-review.md` (geo, 선행 보고서 — 규약 주제 미포함 확인)
35. `F:/dev/kor-travel-common` 작업 트리 파일 목록 (b92fabe, 미추적 scaffold 존재 확인)
