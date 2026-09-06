# T-001 진입 문서·문서 지도·canview 대조표(AGENTS·CLAUDE·SKILL·README·docs/README·dev-environment·canview-checklist·PR 템플릿) (2026-09-06, PR #1)

- 상태: DONE
- 우선순위: P0
- Gate: 문서 검증·2인 리뷰
- 선행: 없음

## 목표

canview 계층(`AGENTS.md` → `docs/README.md` → `docs/resume.md` → 지정 task 1파일)을 kor-travel-common에 세워, 에이전트가 문서 전체를 선제 읽지 않고도 작업을 시작할 수 있게 한다. 이번 PR(2026-09-06)에서 산출되며 2인 리뷰 통과 후 coordinator가 `DONE` 처리한다.

## 고정 결정

- [설계 브리프](../plan/design-brief.md) D-02(저장소 구조·`decisions.md` 미보유·상대 링크만), D-03(정본 Linux/WSL·Windows Tier 2·임시 worktree), D-32(언어), D-33(단독 유지자 역할·긴급 패치 경로).
- ADR-002(canview 계층 채택)·ADR-003(개발 환경) — 색인은 [docs/adr/README.md](../adr/README.md)(T-004).
- 절 구조·규칙 어휘는 [canview 구조 체크리스트](../survey/cross/canview-structure-checklist.md) §2 A1.1~A8.5, §3 R5.4·R5.6~R5.9·R6.1~R6.10을 따르고 내용만 common으로 치환한다.
- 충돌 해결은 [문서 규약 비교](../survey/cross/docs-conventions.md) §2 C1(OS 위임)·C2(worktree 불변 조건)·C3(`CLAUDE.md` 40줄 포인터)·C4(`SKILL.md` 라우터)·C5(우선순위)·C10(언어 예외)·C11(상대 링크만)을 채택.
- Hallmark `SKILL.md` 본문 인용 금지([라이선스 조사](../survey/cross/licensing.md) §4 B3).

## 구현 범위

| 파일 | 요구(체크리스트 ID) |
|---|---|
| `AGENTS.md` | 첫 문장 제품 정의 1문장(A1.1); 배포 단위·소비자 7(airport Admin·PinVi Admin 명시)·책임 표(A1.2); "소비자 한 곳에 있다는 이유만으로 공통화하지 않는다"(A1.3); 기존 공유 라이브러리(`maplibre-vworld-*`·`python-*-api`) 중복 금지·소비자 저장소 직접 수정 금지(A1.4); 작업 원칙 A2.1~A2.7(Ruthless Review 4불릿 원문); 읽기 순서 4단(A3.2)·필요 시 참조 표(A3.4)·특수 참조 5(A3.5)·토큰 절약 5(A3.6); 우선순위 9단에 `docs/standards/`·`docs/dev-environment.md` 삽입(A4.1); 절대 금지 = 공통 5 + 라이브러리 특화 5 이하, 각 항 "…하지 않는다"(A6.16; A6.1·A6.4·A6.9·A6.13·A6.15 변형 채택); 외부 원문 인용(A7.1·A7.4); 완료·push 절(A8.1~A8.5, `git add -A`·`git add .` 금지 문장 그대로); 로컬 절에 단독 유지자 겸임·긴급 패치 경로(D-33) |
| `CLAUDE.md` | 40줄 이하 포인터. 진입 순서와 정본 링크만, 사실 복제 없음(C3) |
| `SKILL.md` | 라우터 + 작업별 시작점 표 + 용어. 정책 복제 금지(A4.2·C4) |
| `README.md` | 문서 지도 + architecture·resume·tasks·adr·reviews·agent-workflow 링크 + 라이선스 절(R5.6, `lic` §3.7 L1) |
| `docs/README.md` | 읽기 단계 표(반드시/필요 시/특수) → 정본 관계 트리 → 분야별 표 → 작업·운영·이력 표(읽는 시점 열) → 탐색 규칙 5(R5.7); 정본 관계 5문장 + "공통 규칙=standards" 1문장(R5.8) |
| `docs/dev-environment.md` | 정본 Linux/WSL bash; Windows Tier 2 절(`py -3 -B -X utf8`, nvm-windows, `.gitattributes` LF, `core.autocrlf=false`); 임시 worktree 프로필 `<repo>-wt/<agent>-<task>`(D-03) |
| `docs/architecture/canview-checklist.md` | `cv` §2·§3 항목별 채택/변형/제외 대조표(D-02) |
| `.github/pull_request_template.md` | task·gate·리뷰어 2인·실패/미실행·evidence·rollback 6항목(R1.14·R4.9) |

## 범위 밖

- runbook 본문(`agent-workflow.md`·`consumer-adoption.md`·`release.md`)·`docs/resume.md`·`docs/journal.md`·`CHANGELOG.md`는 T-007.
- `docs/architecture/*` 나머지는 T-008, ADR 본문은 T-004, 고지 파일은 T-003, validator 정정·`docs.yml`은 T-002·T-009.
- 소비자 배포용 `templates/AGENTS.common.md`·`templates/CLAUDE.pointer.md`는 T-007.

## 예상 변경 파일

예정 경로는 존재·실행 증거가 아니다. `AGENTS.md`, `CLAUDE.md`, `SKILL.md`, `README.md`, `docs/README.md`, `docs/dev-environment.md`, `docs/architecture/canview-checklist.md`, `.github/pull_request_template.md`.

## 수용 기준

- `AGENTS.md`가 위 표의 체크리스트 ID를 모두 충족하고 하드웨어·차량·firmware 항목(A6.2·A6.3·A6.5~A6.8·A6.11·A6.12·A6.14·A7.3)은 없다.
- `CLAUDE.md`는 `wc -l` 결과 40 이하이며 `AGENTS.md`에 없는 규칙을 담지 않는다.
- `docs/README.md`의 정본 관계 트리가 실제 트리(`docs/{adr,architecture,plan,reviews,runbooks,standards,survey,tasks}`)와 일치한다.
- `docs/architecture/canview-checklist.md`가 A1.1~A8.5·R1.1~R6.10 전 항목을 한 행씩 채택/변형/제외 + 근거로 대조한다.
- 모든 링크가 저장소 상대 경로이고 `tools/validate_document_links.py`가 위 8개 파일에서 오류 0(다른 작성자 문서를 가리키는 미존재 링크는 파일 지도 경로와 글자 단위 일치).
- Windows 명령 표기는 `docs/dev-environment.md`에만 있다. 다른 문서는 bash 1벌 + "Git Bash에서 동일" 1줄.
- Hallmark `SKILL.md` 문장 인용이 없다.
- 전문 영역이 다른 리뷰어 2인 독립 리뷰 verdict `PASS`(또는 `CONDITIONAL` + P0/P1 전부 `FIXED`).

## 검증 명령

```bash
python3 -B -X utf8 tools/validate_document_links.py
python3 -B -X utf8 tools/validate_plan.py
wc -l CLAUDE.md
rg -n "git add -A|git add \." AGENTS.md
rg -n "Hallmark" AGENTS.md CLAUDE.md SKILL.md docs/README.md docs/dev-environment.md
git diff --check
```

Git Bash에서 동일(`python` 대체 표기는 [개발 환경](../dev-environment.md)).

## evidence

2026-09-06 완료: CLAUDE 포인터 32줄, 문서 지도 8개 실제 디렉터리, canview A 49개·R 77개 ID 대응을 직접 확인했다. 진입 문서·개발 환경·PR 템플릿을 대조했고 링크 검사를 통과했다.

검증 기준선·CI·2인 gate·원본·실행 수치·NOT_RUN은 [통합 재검토](../reviews/adversarial/2026-09-06-phase0-post-fix-03.md)에 보존한다. 완료 원장 이동과 인계 문서의 후속 delta도 같은 두 리뷰어의 별도 immutable 기준선 검토 대상으로 삼으며 최신 판정은 [리뷰 색인](../reviews/README.md)을 따른다.

## rollback 또는 release 차단 조건

- 문서만 바뀌므로 `git revert` 1회로 원복한다.
- 리뷰 verdict `BLOCK` 또는 P0/P1 finding `OPEN`이면 merge하지 않는다. validator 오류가 남은 채 `DONE`으로 바꾸지 않는다.
