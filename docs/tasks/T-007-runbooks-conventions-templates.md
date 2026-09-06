# T-007 runbook 본문(agent-workflow·consumer-adoption·release)·`docs/standards/agent-conventions.md`·templates/ (2026-09-06, PR #1)

- 상태: DONE
- 우선순위: P0
- Gate: 문서 검증·2인 리뷰
- 선행: 없음

## 목표

[runbook 인덱스](../runbooks/README.md)가 이미 가리키는 3개 runbook과 진척·이력 파일, 소비자에게 배포할 공통 규약·템플릿을 채워 링크 검사 실패를 없애고 "에이전트가 바로 이어갈" 절차를 완성한다. 이번 PR에서 산출되며 2인 리뷰 통과 후 coordinator가 `DONE` 처리한다.

## 고정 결정

- [설계 브리프](../plan/design-brief.md) D-03(worktree 프로필·명령 표기), D-04(full/light gate·상태 어휘·post-fix report), D-05(소비자 원장 SHOULD·대응표), D-11(태그·자산·SHA256SUMS), D-19(매니페스트), D-21(6폭 기준선 = PR evidence), D-24(이관 PR 규격·파일 상한), D-25(`NOT_RUN`), D-31(SemVer 0.x·`-rc`), D-33(역할·긴급 패치).
- ADR-002·003·005·010 — [docs/adr/README.md](../adr/README.md).
- 형식은 [canview 구조 체크리스트](../survey/cross/canview-structure-checklist.md) §3.3 R3.5~R3.17, §3.4 R4.2~R4.12, §3.5 R5.1~R5.5; 공통 절 배치는 [문서 규약 비교](../survey/cross/docs-conventions.md) §3.1(A~I)·§3.3·§3.4·§2 C6·C7·C9·C13·C14·C16.
- 재사용 워크플로 호출 규칙·secret-scan 패턴은 [ci 조사](../survey/cross/ci-deploy.md) §2.1·§2.3, 보안 감사 절차는 `dc` §1.16.

## 구현 범위

| 파일 | 요구 |
|---|---|
| `docs/runbooks/agent-workflow.md` | 8절(R4.2): 범위·기준선 / branch `agent/<agent>-<task>`·worktree `<repo>-wt/<agent>-<task>`·리뷰용 `review-<id>`(R4.3·R4.4) / CodeGraph(R4.5) / 구현·검증 사다리 6층: 문서 → 패키지 빌드·타입 → 단위 → tarball 설치 → 소비자 빌드·e2e → 소비자 배포 스모크(R4.6 변형) / §5.1~§5.4 2인 리뷰(manifest·immutable 기준선 object-only 4명령·detached worktree, P0~P3, disposition 4종, verdict 3종, post-fix `-post-fix.md`; [리뷰 아카이브](../reviews/README.md)와 [TEMPLATE](../reviews/adversarial/TEMPLATE.md)가 링크하는 앵커 `#5-…`·`#51-…` 유지) / 기록 갱신 6조건 / stage·보안·PR(`git add -A`·`git add .` 금지, PR 6항목) / 정리. bash 표기 1벌 + "Git Bash에서 동일" |
| `docs/runbooks/consumer-adoption.md` | 이관 순서(D-16), 필수 2줄 `@import "@kor-travel/tokens/theme.css"` + `@source`(모노레포 상대 경로 표), 매니페스트 커밋, 6폭 기준선 절(T-108 연결), 검증 계층, 되돌리기(`git revert` 1회 + lock 복원), PR 본문(`templates/consumer-pr.md`), 앱별 순서는 [판정 보고서](../plan/design-panel/judge-migration-feasibility.md) §3.1 링크 |
| `docs/runbooks/release.md` | 태그 `tokens-vX.Y.Z`·`ui-vX.Y.Z`·`py-vX.Y.Z`, 자산 `kor-travel-<pkg>-X.Y.Z.tgz` + `SHA256SUMS`, `-rc.N` → 소비자 PR 검증 → 정식, 태그 불변·재발행 금지·`@main` 금지, CHANGELOG 패키지별 H3, 되돌리기(patch 발행) |
| `docs/resume.md` | 5절(R5.4) + "다음 한 작업" 3불릿 |
| `docs/journal.md` | H1 `# kor-travel-common 작업 일지`, H2 `## YYYY-MM-DD (agent[, 주제])` newest-first(R5.1) |
| `CHANGELOG.md` | `## [Unreleased]` + `### tokens`/`### ui`/`### py` H3, `### Breaking` 규칙(D-31) |
| `docs/standards/agent-conventions.md` | 소비자 공통 절 A~I 규범(진입 순서·언어·리뷰 SHOULD·원장 SHOULD·상태 대응표·보안 감사·worktree 불변 조건) |
| `templates/` | `README.md`, `AGENTS.common.md`, `CLAUDE.pointer.md`, `agent-config/*`(geo 형식 이식형), `consumer-pr.md`(검사 결과·스크린샷·되돌리기 명령·파일 상한), `consumer-adoption-checklist.md`, `dependabot.yml`, `eslint/README.md` |

## 범위 밖

- 진입 문서(T-001), ADR(T-004), architecture(T-008), `templates/eslint/*.mjs`·tsconfig·postcss·components.json 조각(T-107), `templates/playwright.baseline.ts`(T-108), `templates/manifests/*`(T-011).
- 소비자 저장소에 템플릿을 적용하는 일(T-403).

## 예상 변경 파일

예정 경로는 존재·실행 증거가 아니다. 위 표의 파일 전부, 그리고 `docs/runbooks/README.md`는 수정하지 않는다(coordinator 소유; 행 추가가 필요하면 open item).

## 수용 기준

- `docs/runbooks/README.md`의 5개 링크와 `docs/reviews/README.md`·`TEMPLATE.md`의 agent-workflow 앵커 대상 절이 존재한다.
- `agent-workflow.md` §5에 R3.9(DEFERRED는 P2/P3만 + owner·task·gate·기한)·R3.12(독립·동일 manifest·immutable)·R3.14(object-only 4명령·`worktree add --detach`·`status --porcelain=v1` 시작·종료 빈 출력)·R3.15 비면제 목록(D-04)·R3.17(post-fix)이 있다.
- `release.md`에 "같은 버전 재발행 금지·태그 삭제 금지·`@main` 참조 금지" 3문장이 있고, 소비자 lock `integrity` 확인 명령이 있다.
- `consumer-adoption.md`가 D-24 파일 상한(tokens 10·ui 30·py 10)과 `NOT_RUN` 규칙을 담고, 이관 PR과 프레임워크 업그레이드 PR 분리를 명시한다.
- `templates/consumer-pr.md`가 검사 결과·6폭 스크린샷·되돌리기 명령·`git revert` 대상 필드를 갖는다.
- Windows 표기는 없다(`docs/dev-environment.md`로 위임). 링크는 상대 경로만, validator 오류 0.
- 리뷰어 2인(문서 규약 · 릴리스/CI) 독립 리뷰 verdict `PASS`.

## 검증 명령

```bash
python3 -B -X utf8 tools/validate_document_links.py
rg -n "^## 5|^### 5\.1" docs/runbooks/agent-workflow.md
rg -n "git add -A|git add \." docs/runbooks/agent-workflow.md
rg -n "@main|재발행|태그 삭제" docs/runbooks/release.md
rg -n "py -3|PowerShell" docs/runbooks docs/standards templates || echo "no windows notation"
git diff --check
```

Git Bash에서 동일.

## evidence

2026-09-06 완료: runbook 5개 링크와 리뷰 앵커, immutable·detached·clean·disposition·post-fix 규칙을 대조했다. 릴리스 태그 불변·재발행 금지·integrity, 소비자 파일 상한·업그레이드 PR 분리·6폭·rollback 필드가 존재한다. Windows 실행기 표기는 개발 환경 문서에 위임했다. 패키지 명령의 실제 완주와 소비자 템플릿 적용은 T-101·T-201·T-302·T-403·T-501에서 검증한다.

검증 기준선·CI·2인 gate·원본·실행 수치·NOT_RUN은 [통합 재검토](../reviews/adversarial/2026-09-06-phase0-post-fix-03.md)에 보존한다. 완료 원장 이동과 인계 문서의 후속 delta도 같은 두 리뷰어의 별도 immutable 기준선 검토 대상으로 삼으며 최신 판정은 [리뷰 색인](../reviews/README.md)을 따른다.

## rollback 또는 release 차단 조건

- 문서·템플릿만 바뀌므로 `git revert` 1회로 원복한다.
- agent-workflow §5 없이는 다른 task의 "2인 리뷰" gate를 닫을 수 없으므로, 이 task의 리뷰 P0/P1 `OPEN` 상태에서 T-001·T-004·T-008을 `DONE`으로 바꾸지 않는다.
