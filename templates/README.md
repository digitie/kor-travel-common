# templates — 소비 저장소 배포 템플릿

이 디렉터리는 kor-travel 소비 저장소가 **복사해 쓰는** 파일을 둔다. 규칙의 정본은 [`docs/standards/`](../docs/standards/README.md)이고 여기 파일은 그 규칙을 바로 적용할 수 있는 원문이다. 템플릿을 고치는 것은 규칙 변경이므로 common PR + 2인 리뷰 비면제 대상이다(D-04).

- 정본 지위: 템플릿 파일 목록·배치 경로·판 표기의 정본. 각 파일의 규칙 정본은 표의 "규약" 열.
- 확정 task: T-007(문서), T-107(`eslint/*.mjs` 실물), T-108(`playwright.baseline.ts`), T-011(매니페스트 스키마·초안).
- 마지막 갱신: 2026-09-07.

## 1. 목록과 배치

| 템플릿 | 소비 저장소 경로 | 강도 | 규약 | 비고 |
|---|---|---|---|---|
| [`AGENTS.common.md`](AGENTS.common.md) | `AGENTS.md` 공통 절(마커 사이) | MUST | [agent-conventions](../docs/standards/agent-conventions.md) §2 | 문구 불변. 로컬 절은 끝 마커 뒤 |
| [`CLAUDE.pointer.md`](CLAUDE.pointer.md) | `CLAUDE.md` | MUST | agent-conventions §2.2 | 40줄 이하. 상충 시 `CLAUDE.md`를 고친다 |
| [`agent-config/antigravity.json`](agent-config/antigravity.json) | `antigravity.json` | SHOULD | agent-conventions §2.3 | geo 이식형(`codegraph serve --mcp`, filesystem `"."`) |
| [`agent-config/claude.json`](agent-config/claude.json) | `claude.json` | SHOULD | 〃 | Claude Code의 MCP는 `.mcp.json`이 정본; `claude.json`은 Claude Desktop 계열용 |
| [`agent-config/mcp.json`](agent-config/mcp.json) | `.mcp.json` | SHOULD | 〃 | 파일명 앞에 점을 붙여 배치 |
| [`agent-config/opencode.json`](agent-config/opencode.json) | `opencode.json` | SHOULD | 〃 | `instructions: ["AGENTS.md", "SKILL.md"]` 포함 |
| [`agent-config/codex.config.toml`](agent-config/codex.config.toml) | `.codex/config.toml` | SHOULD | 〃 | |
| [`agent-config/gemini.mcp.json`](agent-config/gemini.mcp.json) | `.gemini/mcp.json` | 선택 | 〃 | ktdm·map·pinvi 관례 |
| [`agent-config/README.md`](agent-config/README.md) | `docs/notices/kor-travel-common-agent-config.md` | 설정 채택 시 필수 | [licensing](../docs/standards/licensing.md) §5 | 아래 동반 출처 기록·라이선스 사본과 함께 배치 |
| [PROVENANCE PV-007~012](../PROVENANCE.md) 중 채택 파일의 행 | `docs/provenance/kor-travel-common-agent-config.md` | 설정 채택 시 필수 | 〃 | 표 머리·원문 행·common 고정 SHA·배치 경로 매핑 보존 |
| [geo 라이선스 원문](../LICENSES/upstream/kor-travel-geo-LICENSE.txt) | `LICENSES/kor-travel-geo-LICENSE.txt` | 설정 채택 시 필수 | 〃 | 원본 바이트 유지 |
| [`consumer-pr.md`](consumer-pr.md) | PR 본문 | MUST(채택·이관 PR) | agent-conventions §10, [design-brief D-24](../docs/plan/design-brief.md) | 6항목 + 되돌리기 명령 + 6폭 시각 diff 표 |
| [`consumer-adoption-checklist.md`](consumer-adoption-checklist.md) | 상세 task 또는 채택 PR 첨부 | MUST(첫 채택) | [consumer adoption runbook](../docs/runbooks/consumer-adoption.md), [versions](../docs/standards/versions.md) §3 | MUST/SHOULD 표기 |
| [`dependabot.yml`](dependabot.yml) | `.github/dependabot.yml` | SHOULD | versions §3.9, O-18 | `directory`만 앱 구조에 맞게 수정. 그룹·ignore는 common 소유 |
| [`kor-travel-common.lock.schema.json`](kor-travel-common.lock.schema.json) | 소비 저장소 `kor-travel-common.lock.json` | MUST | [D-19](../docs/plan/design-brief.md)·T-011 | draft 2020-12 strict schema. `enforce` 금지 |
| [`kor-travel-common.lock.example.json`](kor-travel-common.lock.example.json) | 소비 저장소 매니페스트 작성 참고 | 참고 | T-011 | 실제 소비자 채택·설치 성공을 의미하지 않는 예시 |
| [`manifests/*.lock.json`](manifests) | 소비 저장소별 초기 초안 | 참고 | T-011 | 10개 앱 표면 대응. 소비자 저장소에 자동 복사하지 않음 |
| [`eslint/README.md`](eslint/README.md) | (설명) | 후보 | [frontend-stack](../docs/standards/frontend-stack.md) | `*.mjs` 조각은 T-107 |
| `playwright.baseline.ts` | `tests/visual/baseline.spec.ts`(예) | MUST(토큰·셸 변경 앱 중 Playwright 없는 wx·ktdm) | D-21, T-108 | **미작성**(T-108) |

## 2. 사용법

1. 파일을 복사한다. 마커·판 주석(`kor-travel-common … 판 2026-09`)은 지우지 않는다 — drift 대조 기준이다.
2. 소비자 경로가 다르면(모노레포 앱 디렉터리) 배치만 바꾸고 내용은 바꾸지 않는다. 바꿔야 한다면 common PR로 제안한다.
3. 규약 PR(AGENTS·CLAUDE·설정 파일·dependabot)은 코드 채택 PR과 분리한다(D-24: 한 PR = 한 산출물).
4. 판이 올라가면 `CHANGELOG.md`(common)에 `### Changed` 항목이 생기고, 소비자는 다음 채택 PR에서 갱신한다. 분기 감사(T-506)가 마커 사이 텍스트를 대조한다.

에이전트 설정을 채택할 때는 표의 동반 파일 3종도 배치한다. 출처 기록은 common `PROVENANCE.md` 표 머리와 채택한 파일의 PV-007~012 행을 원문 그대로 복사하고, 확보한 common의 전체 commit SHA와 `common 파일 → 소비자 배치 경로`를 덧붙인다. 수정 요약·날짜·원천 SHA와 경로를 링크만으로 대신하지 않는다. 동반 기록은 고정 common 원문의 배포 사본이며 별도의 정책 정본이 아니다. 소비자 PR에서 고지에 적힌 두 상대 경로의 파일과 해당 PV 행이 실제 존재하는지 확인한다. common 작업에서는 이 전달 절차만 작성하며 소비 저장소를 직접 수정하지 않는다.

## 3. 템플릿 안의 경로·링크

템플릿 본문은 소비 저장소 기준 경로를 **backtick 경로**로 적고 Markdown 링크를 쓰지 않는다. common의 `tools/validate_document_links.py`가 `templates/**/*.md`도 검사하므로, 소비자 경로를 링크로 쓰면 common에서 깨진 링크로 잡힌다(agent-conventions §8). 소비자는 복사 후 필요하면 링크로 바꿔도 된다.

## 4. 범위 밖

- 재사용 워크플로(`.github/workflows/*.yml`, T-010·T-309·T-401)는 템플릿이 아니라 common 워크플로를 태그/SHA로 호출한다([ci-deploy](../docs/standards/ci-deploy.md)).
- Python 품질 베이스(ruff `extend`·mypy·import-linter·pre-commit)는 `packages/py/kor-travel-common` C20 산출물(T-305).
- 소비자 매니페스트 `kor-travel-common.lock.json` 초안과 schema는 T-011이 `tools/validate_manifest.py`와 함께 관리한다.
