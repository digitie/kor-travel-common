# T005c 문서 종료 gate post-fix — Reviewer B 독립 원본

- 실행 ID: T005C-B-DOCS-POSTFIX-20260907-171958-7B35FF0
- 시작: 2026-09-07T17:19:58.1147528+09:00
- 종료: 2026-09-07T17:21:46.8753589+09:00
- candidate: `7b35ff07b077cef85d7d0d6e0971cacff210374f`
- tree: `3501ebbacade7244435894bcbb4aea87d463dc25`
- 직접 확인한 parent: `b7c9b2de89893d3098bf3f84cd7e63bf72387279`
- code 기준선: `5807e535c16310c41c21f9efce87b2113aa17ee5`
- 격리 worktree: `F:/dev/kor-travel-common-wt/review-t005c-docs-post-b`, 이번 실행에서 새 detached checkout 생성.
- 시작·종료 HEAD/tree는 위 값과 일치했고 `git status --porcelain=v1`은 두 번 모두 빈 출력이었다.
- 최종 verdict: **PASS**. 기존 B-P2-10·B-P2-11·B-P3-12는 모두 FIXED. 이번 delta의 신규 P0/P1/P2/P3 finding 없음.

## 요청과 독립성

전달 요청: “문서 BLOCK finding 수정 후 post-fix 재검토를 수행하세요. exact candidate는 7b35ff07b077cef85d7d0d6e0971cacff210374f, tree 3501ebbacade7244435894bcbb4aea87d463dc25, code baseline 5807e535c16310c41c21f9efce87b2113aa17ee5, parent 7b35ff0^입니다. detached clean worktree에서 변경 4파일을 확인하세요: .gitattributes는 reviewer-B에 whitespace=-blank-at-eof만 적용하고 manifest는 -text -eol -whitespace로 CRLF raw SHA를 보존, final report line 49는 npm/PyPI·package를 범위 밖으로 명시, resume 시작 파일은 T-011입니다. Git blob SHA와 report의 D1AB 해시, 링크/plan/SPDX/secret/redaction/self-check/diff check, code/tests/CI/versions 불변을 확인하세요. 후보 수정·commit/push 금지, 상대 결과/이전 docs raw 비공개. Windows/WSL에서 필요한 검증을 실행하고 .git/codex-audit/2026-09-07-t005c-docs-postfix-reviewer-b.md에 시작/종료 SHA/tree/clean·finding·verdict를 기록하세요. 새 finding 없으면 PASS.”

상대 결과와 이전 docs raw를 열지 않았다. 이전 자기 finding은 대화에 확정된 ID·반례를 기준으로 다시 실행했다. 이번 parent delta 4파일 전체를 읽었고 후보·소비자·다른 원본을 수정하거나 commit/push하지 않았다. 직접 공백 재현은 후보 밖의 자동 정리되는 임시 Git 저장소에서만 실행했다.

## 변경과 기존 finding 재판정

`git diff --stat HEAD^ HEAD`: `.gitattributes`, `docs/resume.md`, 최종 통합 report, 공통 manifest의 4파일이며 7줄 추가·5줄 삭제다.

| 기존 ID·원 심각도 | 판정 | 이번 직접 확인 |
|---|---|---|
| B-P2-10, P2 | FIXED | B raw 경로는 `whitespace=-blank-at-eof`. EOF 빈 줄만 exit 0이며 행 끝 공백·space-before-tab은 exit 2. Windows/WSL 동일. |
| B-P2-11, P2 | FIXED | manifest 원본·Git blob·checkout이 2,107 bytes로 완전히 같고 CRLF 1개를 보존한다. SHA256이 report의 D1AB 해시와 일치한다. |
| B-P3-12, P3 | FIXED | resume 시작 파일 절이 T-011과 통합 계획의 소비자 매니페스트 스키마·validator 계약을 가리킨다. 같은 절에 T-005c 착수 지시가 없다. |

manifest 실제 SHA256: `D1AB00A0F4462AEEB1F99E14C6E3FA2C36A5BDD7FA28AE23C6B60278F3C8C451`. 양 OS에서 `git show HEAD:<manifest path>`를 Python subprocess의 bytes로 받아 SHA256을 계산하고 `.git/codex-audit` 원본 및 worktree bytes와 직접 비교했다.

manifest의 `-text -eol -whitespace`는 그 고정 raw 한 파일의 줄바꿈과 공백을 보존한다고 명시한 예외다. 해당 파일에서는 모든 공백 검사가 꺼지는 사실을 확인했으며, 이를 공백 검사 성공으로 해석하지 않는다. B raw의 EOF 예외와 달리 이 manifest는 원본 bytes 전체를 그대로 보존하는 대상으로 구분되어 있다. 인접 evidence 경로나 일반 Markdown에 예외가 확장되지 않았다.

최종 report의 변경된 49행은 package build/install/publish, npm/PyPI 게시와 release push CI를 이번 검토 범위 밖 NOT_RUN으로 분리하고 merge 후 main CI만 후속 merge gate로 남긴다. 사용자의 소비자 쓰기·npm/PyPI 게시 금지 경계와 일치한다.

## 실행 명령과 결과

- `git diff HEAD^ HEAD -- .gitattributes docs/resume.md docs/reviews/adversarial/2026-09-07-t005c-post-fix-03.md docs/reviews/adversarial/evidence/2026-09-07-t005c-post3d-manifest.md`: 수정 4파일 전체 확인.
- `git diff --quiet 5807e535c16310c41c21f9efce87b2113aa17ee5 HEAD -- tools tests versions.json .github`: exit 0. `check_versions.py`를 포함한 tools·tests·CI·registry 전부 code 기준선과 동일하다.
- `git diff --check HEAD^ HEAD`와 `git diff --check 5807e535c16310c41c21f9efce87b2113aa17ee5 HEAD`: 각각 exit 0.
- Windows `py -3.14 -B -X utf8`와 WSL Python 3.11.15에서 다음 여섯 validator를 직접 실행했으며 전부 exit 0, 양 OS 건수가 같았다. WSL은 전용 worktree의 `GIT_DIR`·`GIT_WORK_TREE`를 지정했다.

| 명령 | Windows·WSL 결과 |
|---|---|
| `tools/validate_document_links.py` | 문서 315개, local target 2,212개, 오류 0 |
| `tools/validate_plan.py` | 상세 task 102개, 오류 0; 제품 gate 검사는 아님 |
| `tools/check_spdx.py` | 29개 파일, 오류 0 |
| `tools/check_versions.py --self-check` | registry 자체 검사 성공; 소비자 검사 아님 |
| `tools/scan_secrets.py --all` | 390개 파일, 발견 0, 예외 0 |
| `tools/check_prod_redaction.py --all` | 390개 파일, 발견 0, 예외 0 |

공백 직접 재현은 양 OS 각각 12건이다. 임시 Git 저장소에 candidate `.gitattributes`, B raw와 manifest의 동일 경로, 인접 `evidence/control.md` 및 일반 `control.md`를 만들고 clean 한 줄을 명시적으로 stage했다. 각 경로에 EOF 빈 줄·행 끝 공백·space-before-tab 3종을 주입해 `git diff --check -- <path>`를 실행했다. B raw는 0/2/2, manifest는 명시적 원본 보존 예외에 따라 0/0/0, 두 control은 각각 2/2/2였다. 기대값 assertion 12개가 각 OS에서 모두 성공했다. `git check-attr text eol whitespace -- <paths>`로 B raw의 LF와 EOF 예외, manifest의 unset 속성, 두 control의 whitespace unspecified를 확인했다. WSL 임시 Git 실행에서는 상위 worktree의 Git 환경 변수를 제거하여 후보 index를 사용하지 않았다.

`gh run list --commit 7b35ff07b077cef85d7d0d6e0971cacff210374f` 및 `gh run view 34099960667 --json headSha,event,conclusion,jobs,url`로 exact candidate CI를 직접 조회했다. [run 34099960667](https://github.com/digitie/kor-travel-common/actions/runs/34099960667)는 head 일치·pull_request·success이며 docs, check-versions, secret-scan, tools Windows, tools Ubuntu 5개 job 모두 success다. 이전 SHA의 CI를 이번 SHA의 증거로 대체하지 않았다.

## 재사용·NOT_RUN·판정 한계

- 전체/focused unittest 재실행: `NOT_RUN(도구·tests·CI·registry가 code 기준선과 동일; 기존 code candidate 검증 재사용)`. 이전 code 검토의 양 OS 전체 179 tests·focused 84 tests·skip 0을 재사용하며, 이번 exact 문서 candidate CI는 위와 같이 별도로 직접 조회했다.
- 소비자 파일 변경·workflow/CI 실행·build/e2e, package build/install/publish, npm/PyPI 게시, tag/release 생성과 release push CI: `NOT_RUN(이번 문서 검토 범위 밖; 소비자 쓰기·registry 게시 금지 유지)`.
- merge 후 main CI: `NOT_RUN(후속 merge 담당 gate)`.
- 신규 finding 없음. **PASS**는 위 exact 문서 candidate와 검증 범위에 한정하며, manifest 원본의 명시적 공백 예외나 실행하지 않은 외부 gate를 일반 검증 성공으로 바꾸지 않는다.
