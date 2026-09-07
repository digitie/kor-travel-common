# PROVENANCE

이 문서는 다른 저장소에서 common으로 옮겨 온 파일군의 원천·커밋·경로·라이선스·수정 여부를 파일군 단위로 기록한다(브리프 D-17, ADR-004; 형식은 `docs/survey/cross/licensing.md` §2.3). 고지·검사 구현 task는 T-003이다. 파일 단위 표기는 각 파일의 SPDX 헤더 `Origin:`/`Derived-From:`/`Modified:` 행이 정본이고, 이 표는 그 색인이다. 마지막 갱신 2026-09-07.

## 규칙

1. 코드·문서·CSS를 다른 저장소에서 옮기기 **전에** 이 표에 행을 추가한다. 행이 없는 이식은 리뷰 `P0`(라이선스 위반 후보)다.
2. 원천 커밋은 40자 또는 7자 이상 short hash로 적고, 경로는 원천 저장소 상대 경로다. 여러 파일이면 디렉터리 + 개수.
3. 추출 규칙(D-17): GPL 원천(map·weather·airport)은 그대로 옮기고 `Origin:`을 남긴다. geo(`GPL-3.0-only`) 유래는 헤더에 `GPL-3.0-only`를 병기하고 권리자가 `-or-later`로 재선언하기 전까지 유지한다(O-20). MIT 원천(concierge·docker-manager)은 MIT 고지를 [THIRD_PARTY_NOTICES](THIRD_PARTY_NOTICES.md) 또는 헤더에 보존한다. shadcn CLI 생성물은 MIT 고지(`Derived-From: shadcn/ui`)를 단다.
4. 금지 원천: pinvi 전체(L6 결정 전, B1), pinvi 벤더 tgz·`maplibre-vworld-*` 소스(영구, B2), Hallmark `SKILL.md` 본문(B3), `python-*-api`·`python-kraddr-base` 코드(의존만). concierge `AppShell.tsx`·`globals.css`의 map 참조는 diff로 복사 여부를 확정한 뒤에만 기록한다(B4).
5. 수정 열에는 "없음" 또는 바꾼 점의 요약과 날짜를 적고, 원천이 바뀌어도 이 표의 기존 행은 고치지 않는다(재이식은 새 행).
6. 앱 사본과의 drift 비교는 선두 주석 블록(SPDX·Hallmark 스탬프)을 정규화한 뒤 수행한다(D-17).

## 표

| ID | common 파일군 | 원천 저장소 | 커밋 | 원천 경로 | 원천 라이선스 | 수정 | 근거 |
|---|---|---|---|---|---|---|---|
| PV-001 | `tools/validate_plan.py` | canview | `1f93b8adb34a48537db69b950c8a99ce89859760` | `tools/validate_plan.py` | GPL-3.0(원문, 버전 미지정) → common `GPL-3.0-or-later`(권리자 동일) | docstring 1줄("G0–G6 통과" → "gate 통과"), 파서·규칙 무변경 (2026-09-06) | `docs/survey/cross/canview-structure-checklist.md` §1.2 |
| PV-002 | `tools/validate_document_links.py` | canview | `1f93b8a` | `tools/validate_document_links.py` | 동상 | 대상 경로(`docs/`·`packages/`·`tools/`·`templates/`·`tests/`·루트) 변경, 절대 경로 링크를 오류로 판정, 공백 포함 target(산문)·inline code span 제외 — 사실상 재작성 (2026-09-06) | 동상 §1.2·§4.3 |
| PV-003 | `tests/test_plan_validation.py` | canview | `1f93b8a` | `tests/test_plan_validation.py` | 동상 | 모듈명 `canview_plan_validation` → `kor_travel_common_plan_validation`, tempdir prefix; 기존 35 tests 보존 + 완료 날짜·PR 제목 회귀 1건 추가·출처 헤더 (2026-09-06) | 동상 §1.2·§4.2 |
| PV-004 | `docs/reviews/adversarial/TEMPLATE.md` | canview | `1f93b8a` | `docs/reviews/adversarial/TEMPLATE.md` | 동상 | 없음(diff 0) | 동상 §1.2 |
| PV-005 | `docs/tasks-rule.md`, `docs/tasks-done.md`, `docs/tasks/README.md`, `docs/runbooks/README.md`, `docs/runbooks/documentation-maintenance.md`, `docs/runbooks/agent-failure-patterns.md`, `docs/reviews/README.md`, `.gitignore`, `.gitattributes` | canview | `1f93b8a` | 동일 경로 9개 | 동상 | 도메인 치환(ID 대역·5열 문법·standards 행·Node/Python ignore·전역 LF); 변경 줄 수는 checklist §1.2 표 | 동상 §1.2 |
| PV-006 | `docs/runbooks/agent-workflow.md`, `docs/resume.md`(5절 구조), `docs/journal.md`(항목 형식·검증 표), `CHANGELOG.md`(형식), `AGENTS.md`·`SKILL.md`·`docs/README.md`(절 구조) | canview | `1f93b8a` | `docs/runbooks/agent-workflow.md`, `docs/resume.md`, `docs/journal.md`, `CHANGELOG.md`, `AGENTS.md`, `SKILL.md`, `docs/README.md` | 동상 | 절 제목·규칙 어휘만 채택하고 본문은 kor-travel-common으로 전면 치환(2026-09-06) | 동상 §2·§3, `docs/survey/cross/docs-conventions.md` §3 |
| PV-007 | `templates/agent-config/codex.config.toml` | kor-travel-geo | `1d9d74d3a852bbaaa09144b75bb69b99a58a6002` | `.codex/config.toml` | GPL-3.0-only | common 설명·SPDX 헤더 추가, 설정 본문 동일 (2026-09-07 확인) | [설정 고지](templates/agent-config/README.md) |
| PV-008 | `templates/agent-config/antigravity.json` | kor-travel-geo | `1d9d74d3a852bbaaa09144b75bb69b99a58a6002` | `antigravity.json` | GPL-3.0-only | 없음(정규화 JSON 동일) (2026-09-07 확인) | [설정 고지](templates/agent-config/README.md) |
| PV-009 | `templates/agent-config/claude.json` | kor-travel-geo | `1d9d74d3a852bbaaa09144b75bb69b99a58a6002` | `claude.json` | GPL-3.0-only | 없음(정규화 JSON 동일) (2026-09-07 확인) | [설정 고지](templates/agent-config/README.md) |
| PV-010 | `templates/agent-config/mcp.json` | kor-travel-geo | `1d9d74d3a852bbaaa09144b75bb69b99a58a6002` | `.mcp.json` | GPL-3.0-only | 없음(정규화 JSON 동일) (2026-09-07 확인) | [설정 고지](templates/agent-config/README.md) |
| PV-011 | `templates/agent-config/opencode.json` | kor-travel-geo | `1d9d74d3a852bbaaa09144b75bb69b99a58a6002` | `opencode.json` | GPL-3.0-only | instructions 추가·키 정렬 (2026-09-07 확인) | [설정 고지](templates/agent-config/README.md) |
| PV-012 | `templates/agent-config/gemini.mcp.json` | kor-travel-geo | `1d9d74d3a852bbaaa09144b75bb69b99a58a6002` | `antigravity.json` | GPL-3.0-only | filesystem 항목 제거 (2026-09-07 확인) | [설정 고지](templates/agent-config/README.md) |
| PV-013 | `packages/tokens/tokens.css` | kor-travel-map | `c494e227e010565be295de3f9670b2f7c8c20944` | `packages/kor-travel-map-admin/frontend/src/app/globals.css` | GPL-3.0-or-later | semantic 토큰·다크 값·형태·모션 값을 추출해 `--kt-*` 이름과 공개 패키지 계약에 맞게 재구성. 의미·접근성 규칙은 같은 커밋의 `packages/kor-travel-map-admin/frontend/design.md`와 대조 (2026-09-07) | [T-101](docs/tasks/T-101-tokens-package.md), [디자인 토큰 조사](docs/survey/cross/design-tokens.md) §3.2·§3.6 |

### 2026-09-07 출처 대조 정정

고정 canview 원문과 다시 대조한 결과 PV-001의 `validate_plan.py`는 docstring 1줄과 출처 헤더만 다르며, 완료 상세 제목과 archive 제목 일치 검사는 원본에 이미 있다. common이 이 검사를 추가했다는 이전 설명은 오기다. PV-002에는 여러 길이의 inline code backtick 처리, PV-003에는 대응 회귀 시험이 추가되었다. 원천 커밋은 그대로이며 현재 수정 고지는 파일 헤더로 확인한다.

PV-007~012는 T-013에 이미 들어 있던 geo 설정 사본을 원본과 대조해 누락된 출처를 보완한 것이다. 새 소비자 코드를 반입하지 않았다. 주석 불가 JSON의 파일별 고지는 [설정 고지](templates/agent-config/README.md)가 맡는다. 소비 저장소의 제품 코드(tokens·UI·Python)는 아직 없다. 이후 이식은 다음 PV 번호부터 행과 헤더를 함께 추가한다.

검사 대상 소스는 행마다 명시적 common 경로·원천 경로 하나씩 기록한다. `tools/check_spdx.py`는 이 색인과 헤더를 대조한다. 소스 재이식 시 이전 행 원문은 별도 이식 기록 문서에 보존·링크하고 현재 표에 같은 common 경로가 두 번 나오지 않게 한다. 수정 여부를 원격 원본과 자동 비교하거나 미등록 복사를 탐지하는 도구는 아니므로, 원본 diff와 금지 원천 검토는 이식 PR의 2인 리뷰에서 수행한다.
