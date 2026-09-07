# T-101 CI 표준 한 줄 변경 독립 리뷰 A

- 실행 ID: A-T101-CI-DOCS-20260907-223319
- 판정: PASS. 신규 P0/P1/P2/P3 finding 0건.
- candidate: 6ab650d76c4e40944085a79dde12e016d43e494b
- tree: 2610acbd28f2b80cfc0d52097b3bfe7e25a4b7fc
- parent/base: 0cf352ad4ee6640329dc46a06aa0a88402d42b86
- 격리 worktree: F:/dev/kor-travel-common-wt/review-t101-ci-docs-a, detached.
- 시작: 2026-09-07 22:33:19.239 KST. 종료: 2026-09-07 22:34:24.369 KST.
- 시작·종료 SHA/tree는 위 값과 같고 git status --porcelain=v1은 모두 빈 출력이었다.
- 후보·소비자 파일·source config를 변경하지 않았으며 commit/push하지 않았다. 이번 판정을 위해 초기/상대 원본 보고서는 읽지 않았다.

## 요청과 범위

새 immutable 6ab650d(parent 0cf352a)의 docs/standards/ci-deploy.md packages job 순서 한 줄만 독립 적대적으로 검토한다. 문서 계약·T-101/T-201 범위·실제 CI 순서를 대조하고 verdict와 종료 SHA/tree/clean 및 원본 hash를 남긴다.

git diff로 변경이 docs/standards/ci-deploy.md 1파일의 한 행 교체(+1/-1)뿐임을 확인했다. 현재 후보의 workflow 및 T-101/T-201 구현 범위·수용 기준·package scripts를 직접 확인했다. 과거 코드 리뷰를 다시 판정하거나 task 전체 종료를 승인하는 범위는 아니다.

## 근거와 판단

- ci-deploy.md:233의 필수 순서는 실제 .github/workflows/docs.yml:175부터 이어지는 npm 핀 → npm ci → 커밋 생성물 check → build → check → 생성물 git diff → test → pack → 임시 tarball 설치와 일치한다. Python 인덱스 단언으로 같은 순서를 확인했다.
- 실제 workflow에는 check 전 lint/type-check --if-present도 남아 있다. 현재 tokens package에 두 script가 없어 무동작이므로 변경된 표가 실질적인 필수 실행 단계를 누락하지 않는다. T-201의 별도 tsc --noEmit 수용 기준을 삭제하거나 면제하는 문장도 아니다.
- build 전 check를 명시하므로 생성물을 덮어쓴 뒤 clean 결과만 확인하는 순서로 오해할 여지를 없앤다. build 후 check와 git diff, test/pack/install도 유지한다.
- T-101은 tokens 골격과 tarball 설치까지 소유한다. T-201은 UI 추가 시 기존 packages job에 UI 단계를 추가하고 webpack/Turbopack 두 next build를 요구한다. 새 문장은 이 후속 UI 범위를 현재 토큰 구현에 선행 요구하지 않으면서 그대로 보존한다.
- 실제 workflow는 PR 및 main/codex/release-* push를 선택하고 packages job에 별도 path/PR 제한을 두지 않는다. 표의 trigger·runner·task 소유 표기와 일치한다.
- npm pack/임시 설치는 게시가 아니다. 새 문장은 소비자 저장소 수정·npm/PyPI 게시·독립 서비스 배포를 요구하지 않는다.

## 실행 gate

실행 위치: 위 detached worktree.

    git diff 0cf352ad4ee6640329dc46a06aa0a88402d42b86 HEAD -- docs/standards/ci-deploy.md
    git diff --exit-code 0cf352ad4ee6640329dc46a06aa0a88402d42b86 HEAD -- .github/workflows packages tools tests docs/tasks
    git diff --check 0cf352ad4ee6640329dc46a06aa0a88402d42b86 HEAD
    python -B -X utf8 tools/validate_plan.py
    python -B -X utf8 tools/validate_document_links.py

모두 성공했다. plan은 106 task/오류 0, 링크는 문서 361개·local targets 2323개/오류 0. 별도 Python 단언은 변경 파일 1개·필수 명령 순서·현재 lint/type-check script 부재를 확인해 PASS했다.

탐색 중 PowerShell rg에 T-201* 파일 인수를 직접 전달한 명령은 glob 확장이 없어 실패했다. 이후 rg --files로 실제 T-201-ui-package-skeleton.md를 확인하고 그 정확한 파일을 읽었다. 실패한 탐색을 검증 성공으로 세지 않았다.

## 미실행과 최종 판정

NOT_RUN: 새 후보의 전체 Python/package 테스트·양 OS build/install·실제 CI 재실행. 변경은 규범 표 한 줄뿐이고 workflow/package/tools/tests는 parent 대비 불변이므로 이 리뷰에서 해당 코드를 재실행하지 않았다. 이전 보고서의 성공을 새 SHA 성공으로 옮겨 적지 않는다.

검토한 한 줄에 수정이 필요한 새 finding은 없으며 PASS이다. task 전체 종료와 원격 CI gate 충족 여부는 별도 종료 evidence의 범위다.