# T-005c 문서 종료 gate 수정 후 Reviewer A 원본

- 실행 ID: T005C-A-DOCS-POSTFIX-20260907-172008-7B35FF0
- 최종 verdict: **PASS**
- candidate: `7b35ff07b077cef85d7d0d6e0971cacff210374f`
- tree: `3501ebbacade7244435894bcbb4aea87d463dc25`
- parent: `b7c9b2de89893d3098bf3f84cd7e63bf72387279`
- code baseline: `5807e535c16310c41c21f9efce87b2113aa17ee5`
- 새 detached worktree: `F:/dev/kor-travel-common-wt/review-t005c-docs-post-a`
- 시작: 2026-09-07T17:20:08.9087490+09:00. HEAD/tree/parent 직접 일치, porcelain 출력 0행.
- 종료: Windows 2026-09-07T08:23:12.728793Z, WSL 2026-09-07T08:23:14.227051Z. 양 OS HEAD/tree 일치, porcelain 출력 0행.
- 후보·제품·소비자 파일 수정과 commit/push 없음. 상대 결과·이전 docs raw를 읽지 않았다.

## 요청과 변경 범위

문서 BLOCK 수정의 exact candidate를 detached clean worktree에서 재검토하고 Git blob·원본 manifest 해시, attributes, 다음 시작 파일, link/plan/SPDX/secret/redaction/self-check/diff, 코드·시험·CI·versions 동일성과 소비자/게시 경계를 확인하도록 요청받았다.

parent 대비 변경은 .gitattributes, resume, 최종 통합 report, post3d manifest의 **4파일**뿐이다. 해당 diff 전체를 읽었다. reviewer 원본 A/B·task 원장·완료 원장·T-005c·T-011·journal은 parent와 동일함을 `git diff --quiet`로 확인했고 상대 raw 본문은 열지 않았다.

## 원 finding disposition

| ID | 원 심각도 | 판정 | 새 candidate에서 확인한 결과 |
|---|---|---|---|
| A-P2-09 | P2 | **FIXED** | 통합 report 49행에서 package build/install/publish·npm/PyPI 게시·release push CI를 범위 밖 NOT_RUN으로 분리했다. main CI는 merge 후 확인하는 항목으로 따로 명시된다. 금지된 게시를 T-005c 병합 선행으로 요구하지 않는다. |
| A-P2-10 | P2 | **FIXED** | archive manifest의 실제 Git blob·Windows/WSL worktree SHA256이 원 review manifest의 D1AB 값 및 report 7행과 일치한다. CRLF 1개를 포함한 원본 바이트가 보존된다. |

새 P0/P1/P2/P3 finding은 없다. resume의 다음 한 작업과 시작 파일이 모두 T-011로 일치한다. T-011 READY와 선행 T-005 완료, 전체 102개 중 완료 14개·열린 88개도 유지된다. 소비자 변경은 T-403의 별도 범위이며 이번 수정은 common 문서/evidence만 대상으로 한다.

## 무결성과 attributes

`git cat-file blob HEAD:docs/reviews/adversarial/evidence/2026-09-07-t005c-post3d-manifest.md`의 바이트를 Python subprocess로 받아 직접 SHA256을 계산했다. 셸 문자열 변환이나 개행 정규화 없이 worktree 바이트와 비교했다.

- Git blob ID: `53ddfe35e5ac07886d9210d5bf43b5d671439acd`
- Git blob SHA256 및 양 OS worktree SHA256: `D1AB00A0F4462AEEB1F99E14C6E3FA2C36A5BDD7FA28AE23C6B60278F3C8C451`
- Git blob/worktree 동일: true; 원본 hash/report 기재 hash 일치: true; CRLF: 1개.
- `git check-attr text eol whitespace -- <manifest> <reviewer-b> tools/check_versions.py`: manifest는 text/eol/whitespace unset, B 원본은 text set/eol lf/whitespace `-blank-at-eof`, 제품 Python 파일은 text set/eol lf/whitespace unspecified다.
- B 원본의 예외는 EOF 빈 줄 종류만 제외하도록 좁혀졌다. manifest 예외는 고정된 파일 하나의 원본 바이트 보존에 한정된다. 제품 파일 검사 속성을 바꾸지 않았다.

## 코드 동일성과 직접 검증

`git diff --quiet 5807e535c16310c41c21f9efce87b2113aa17ee5 HEAD -- tools tests packages versions.json .github/workflows`는 exit 0이다. 코드·시험·제품·registry·CI 정의가 불변이므로 기존 code candidate의 양 OS 전체 179개·focused 84개·직접 CLI 116회 PASS를 재사용한다. 새 문서 commit에서 그 시험을 재실행했다고 주장하지 않는다.

Windows Python 3.14.3, WSL Ubuntu-26.04의 uv managed Python 3.11.15에서 다음 validator를 새로 실행했다. 각 Python 명령에 `-B -X utf8`를 썼다. WSL 진입점은 아래와 같다.

```text
wsl -d Ubuntu-26.04 --cd /mnt/f/dev/kor-travel-common-wt/review-t005c-docs-post-a -- /home/digitie/.local/bin/uv run --no-project --python 3.11 python -B -X utf8 ...
```

WSL Git 기반 검사에만 프로세스 안에서 `GIT_DIR=/mnt/f/dev/kor-travel-common/.git/worktrees/review-t005c-docs-post-a`, `GIT_WORK_TREE=/mnt/f/dev/kor-travel-common-wt/review-t005c-docs-post-a`를 지정했다. Git 설정이나 파일을 수정하지 않았다.

| 명령 | Windows 실제 결과 | WSL 실제 결과 |
|---|---|---|
| `tools/validate_document_links.py` | 315문서/2212 target, 오류 0 | 315문서/2212 target, 오류 0 |
| `tools/validate_plan.py` | 102 task, 오류 0 | 102 task, 오류 0 |
| `tools/check_spdx.py` | 29파일, 오류 0 | 29파일, 오류 0 |
| `tools/scan_secrets.py --all` | 390파일, 발견 0, exit 0 | 390파일, 발견 0, exit 0 |
| `tools/check_prod_redaction.py --all` | 390파일, 발견 0, exit 0 | 390파일, 발견 0, exit 0 |
| `tools/check_versions.py --self-check` | exit 0 | exit 0 |
| `git diff --check <parent> HEAD` | exit 0 | exit 0 |
| `git diff --check <code-baseline> HEAD` | exit 0 | exit 0 |

이번 validator 실행에서 실패나 skip은 없었다. Plan 검사는 읽기 전용 metadata/DAG 검증이며 제품 gate 성공으로 세지 않는다.

## 실제 CI

`gh run list --commit 7b35ff07b077cef85d7d0d6e0971cacff210374f --json databaseId,headSha,event,status,conclusion,url`와 `gh run view 34099960667 --json headSha,conclusion,event,jobs,url`로 [PR CI 34099960667](https://github.com/digitie/kor-travel-common/actions/runs/34099960667)의 exact SHA·pull_request·completed/success를 확인했다. docs, tools(Windows/Ubuntu), check-versions, secret-scan 5개 job이 모두 success다. 과거 code/문서 candidate의 CI와 구분했다.

## 미실행과 최종 판정

- NOT_RUN: 새 전체/focused/CLI 회귀. 코드·시험·CI·registry 불변 검증 후 기존 5807e535의 독립 PASS를 재사용했다.
- NOT_RUN: 상대 reviewer 원본/이번 결과 및 이전 docs raw 본문. 독립성 요청에 따라 열람하지 않았다.
- NOT_RUN: 실제 소비자 파일/빌드/e2e, package build/install/publish, npm/PyPI 게시, Docker/Actions 원격 실행, release push CI, merge 후 main CI. 현 문서 검토 범위 밖이며 아직 실행한 것처럼 표시하지 않는다.

**PASS**. A-P2-09/A-P2-10 모두 수정 확인했으며 이번 4파일 delta에서 새 finding은 없다.
