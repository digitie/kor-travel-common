# kor-travel-common 작업 일지

이 문서는 작업 재현 정보(기준선·명령·결과·미실행·도구 fallback·소비 저장소 상태)의 역시간순 기록이다([documentation maintenance §4](runbooks/documentation-maintenance.md)). 최신 항목을 위에 추가하고 기존 항목은 사실 오류 correction 외에 수정하지 않는다. 현재 상태와 다음 작업은 [resume](resume.md)가 정본이다.

## 2026-09-06 (claude, 저장소 부트스트랩·조사·설계·계획)

기준선 `b92fabeb1c96a11c1fc9507d93271c1ebeee09b0`(Initial commit, 추적 파일 `LICENSE` 1개)에서 브랜치 `feat/bootstrap-survey-and-integration-plan`을 만들어 작업했다. 사용자 dirty 변경은 없었다. 환경은 Windows 11(Git Bash, Tier 2), Python 3.14.3(Windows), 원격 `origin = https://github.com/digitie/kor-travel-common.git`이다. CodeGraph MCP는 연결에 실패해 사용하지 않았고 `rg`·직접 읽기·validator로 대체했다.

**작업**

- canview(`F:/dev/canview` `1f93b8a`, 읽기 전용) 구조를 대조해 scaffold를 만들었다: `tools/validate_plan.py`·`tools/validate_document_links.py`(대상 경로·절대 링크 오류·산문 오탐 제외로 재작성)·`tests/test_plan_validation.py`·`tests/test_document_links.py`(신규 5건), `docs/tasks-rule.md`(common ID 대역·5열 문법 명문화), `docs/tasks-done.md`, `docs/tasks/README.md`, `docs/runbooks/{README,documentation-maintenance,agent-failure-patterns}.md`, `docs/reviews/README.md`, `docs/reviews/adversarial/TEMPLATE.md`(diff 0), `.gitignore`·`.gitattributes`·`.editorconfig`·`.github/workflows/docs.yml`. 출처는 `PROVENANCE.md`에 기록했다.
- 조사 워크플로: 7개 소비 저장소를 기준 커밋 단위로 고정해 인벤토리 7편 + 횡단 비교 10편 + README·공통화 매트릭스를 `docs/survey/`에 작성했다(서브에이전트 병렬). 17개 산출물 중 14개는 파일이 완결된 상태로 세션 한도(스키마 응답만 실패)에 걸렸고, 완결 여부를 마지막 절로 확인한 뒤 재실행하지 않았다. 나머지 3개는 미완결이어서 해당 에이전트만 다시 실행해 완결했다. 문서 간 불일치 19건은 `docs/survey/README.md` §6.2에 재확인 값과 함께 남겼다.
- 설계 판정: coordinator 초안 레지스터 + 독립 설계안 2(risk-first·velocity-first) + 판정 3(fact-consistency·migration-feasibility·directive-fidelity)을 실행하고 원본을 `docs/plan/design-panel/`(7파일)에 보존했다. 합의 문안을 채택해 `docs/plan/design-brief.md`(결정 D-01~D-33, 열린 결정 O-1~O-25, 파일 지도, ADR 12, task 92)를 확정했다.
- `09104ed0fa7f8564936fbbc3b9c17057f86d3e7c` "docs: bootstrap kor-travel-common with survey, design brief, validators"(2026-09-06 17:01 KST)를 커밋·push하고 [Draft PR #1](https://github.com/digitie/kor-travel-common/pull/1)을 열었다(base `main`).
- Phase 0 문서군(entry·runbooks·architecture·standards-fe·standards-be·versions-conventions·task 5·ledger)을 파일 지도의 소유자별로 병렬 작성했다. 이 항목 작성 시점에는 미커밋이며 상호 링크는 파일 지도 경로를 따른다.

**결정**: 브리프 D-01~D-33 채택(canview 계층·5열 원장·`decisions.md` 미보유·저장소 상대 링크만·Python 도구·GPL-3.0-or-later·tarball 배포·SemVer 0.x·`--kt-*`). 열린 결정 O-1~O-25는 사용자 확인 전까지 기본값으로 진행하고 문서에는 "열림(사용자 확인 필요)"로 적는다. 사용자 지시 완화로 보일 수 있는 항목은 pinvi mobile Tailwind 3 예외(O-8)뿐이며 "승인 대기"로만 적었다.

**검증(작성자 실제 실행, `09104ed` 기준)**

| 명령/환경 | 결과 |
|---|---|
| `python -B -X utf8 tools/validate_plan.py` (Windows, Python 3.14.3) | 오류 3: `docs/tasks: 상세 task 파일이 없음`, `docs/tasks.md: 읽기 실패`, `상세 task 수 불일치 (실제 0)` — 원장(ledger) 산출 전이므로 **통과 아님**, 문서군 완성 후 재실행 필요 |
| `python -B -X utf8 tools/validate_document_links.py` | 36 문서·60 local target·오류 19 — 전부 미작성 문서(`agent-workflow.md`·`consumer-adoption.md`·`release.md`·`docs/README.md`·`docs/tasks.md`·`docs/dev-environment.md`·`docs/standards/*`·`docs/architecture/README.md`)를 가리키는 링크. 산문 오탐은 도구 정정 후 0. **통과 아님** |
| `python -B -X utf8 -m unittest discover -s tests -p "test_*.py"` | 40 tests OK(plan validator 35 + link validator 5), 1.3s |
| `git diff --check HEAD~1 HEAD` | trailing whitespace 1건 `docs/plan/design-panel/register-coordinator-draft.md:77`(exit 2) — 판정 원본 파일, 미수정 |
| 조사 워크플로(서브에이전트 17) | 14 완결 + 3 재실행 후 완결 → `docs/survey/` 19파일 |
| 설계 판정 워크플로(설계자 2·판정자 3) | `docs/plan/design-panel/` 7파일 + `docs/plan/design-brief.md` |
| `gh pr create --draft` | PR #1 생성(2026-09-06T08:01:57Z UTC), CI `docs` run `34020728074` `validate-docs` **failure**(위 두 validator 오류와 동일 원인) |

**미실행(NOT_RUN)**: 패키지 빌드·타입 검사(패키지 미존재), `npm pack`·tarball 설치, wheel 빌드·설치, 소비자 빌드(`consumer-smoke`)·e2e, 브라우저·시각 기준선 캡처, `check_versions.py`·`kt_contrast.py`·`ux_lint.py`(미작성), 2인 독립 적대적 리뷰. 어느 것도 통과로 집계하지 않았고 task는 모두 `IN_PROGRESS`/`READY`/`BLOCKED`로 둔다.

**환경·fallback**: Windows에서 작성한 `.py`·`.md`는 `.gitattributes`(`* text=auto eol=lf`)가 add 시 LF로 정규화한다는 전제이며 첫 add에서 `git ls-files --eol`로 확인해야 한다(canview checklist Q6). 조사 대상 저장소와 canview에는 아무 파일도 쓰지 않았고 실행 전후 `git status`로 부산물이 없음을 확인했다(`docs/survey/README.md` §2.3).

**소비 저장소 상태(조사 기준, `docs/survey/README.md` §2.1)**: airport `2bb1111`(clean, WIP `codex/shadcn-ui-foundation` `99b3f98`), concierge `7945305`, docker-manager `862562d`, geo `1d9d74d`, map `c494e227`, weather `6003da9`, pinvi `9af25e5`(shallow clone). 어느 저장소도 수정하지 않았다.

**다음**: [resume](resume.md) "다음 한 작업" — 2인 적대적 리뷰 → task `DONE` → PR #1 본문 갱신·머지.
