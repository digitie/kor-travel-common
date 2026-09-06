# kor-travel-common 반복 실패 패턴과 복구

이 문서는 [runbook 인덱스](README.md)에 속하며, 실제로 반복된 실패의 증상·확인 순서·복구만 적는다. 절차 정본은 [agent workflow](agent-workflow.md), 문서 규칙은 [documentation maintenance](documentation-maintenance.md)다. 실패가 처음 발생했을 때가 아니라 두 번째 발생했을 때 이 표에 행을 추가한다.

| 증상 | 먼저 확인할 것 | 복구 |
|------|----------------|------|
| `validate_document_links.py`가 미작성 문서 링크를 오류로 보고함 | 링크 target이 이번 PR에서 만들 문서인지, 이름만 바뀐 문서인지 | 문서를 같은 PR에서 만들거나 링크를 제거한다. 미래 문서를 가리키는 링크는 남기지 않는다 |
| 링크 검사가 절대 경로(`F:/dev/...`, `/mnt/f/...`)를 오류로 보고함 | 다른 저장소 문서를 복사하며 절대 링크가 따라왔는지 | 저장소 상대 경로로 바꾼다. 다른 저장소 파일은 GitHub URL(커밋 고정)로 인용한다 |
| `validate_plan.py`가 `상세 task 수 불일치`를 보고함 | `docs/tasks.md`의 `N개의 상세 작업` 문구와 `docs/tasks/T-*.md` 파일 수 | 문구의 N을 실제 파일 수로 맞춘다. 문구는 정확히 한 번만 둔다 |
| `validate_plan.py`가 `요약 {필드} 불일치`를 보고함 | 상세 파일의 `상태`·`우선순위`·제목·`선행`과 요약 표 행 | 상세 파일을 정본으로 요약 행을 글자 단위로 맞춘다. 제목에 `\|`를 쓰지 않는다 |
| `validate_plan.py`가 `READY인데 선행 미완료`를 보고함 | 선행 task가 `DONE`인지 | 선행이 남아 있으면 상태를 `BLOCKED`로 둔다. 외부 조건은 `선행`이 아니라 `외부 선행` 줄에 적는다 |
| Windows에서 만든 `.py`·`.md`가 CRLF로 stage됨 | `git ls-files --eol <path>`의 `i/` 값 | `.gitattributes`(`* text=auto eol=lf`)가 정규화한다. `i/crlf`면 `git add --renormalize <path>` 후 다시 확인한다 |
| 소비 앱에서 common 패키지 클래스가 스타일 없이 렌더됨 | 소비 앱 CSS에 `@source "../node_modules/@kor-travel/ui"`가 있는지, `@kor-travel/tokens/theme.css`를 `@import "tailwindcss"` 뒤에 넣었는지 | 누락한 등록을 추가한다. `source(none)`을 쓰는 앱(geo)은 명시 `@source`가 없으면 아무 클래스도 탐지되지 않는다 |
| 소비 앱에서 같은 utility 이름이 두 값으로 해석됨 | `@config tailwind.config.ts`의 `theme.extend`와 `@theme`이 같은 이름을 정의하는지 | config 쪽 정의를 제거한다. common 토큰 도입 앱은 `@config` 없이 CSS-first만 쓴다 |
| `npm pack` tarball 설치 후 타입이나 CSS가 빠짐 | `package.json`의 `files`·`exports`에 `dist`와 `*.css`가 있는지, `sideEffects` 설정 | 누락 항목을 추가하고 `packages` CI job의 tarball 설치 검사로 재확인한다 |
| React 18 앱에서 `@kor-travel/ui` 컴포넌트의 ref가 전달되지 않음 | 소비 앱 React 버전 | `@kor-travel/ui`는 React 19 전용이다. tokens만 먼저 채택하고 React 19 업그레이드 task를 선행한다 |
| GitHub Actions에서 재사용 워크플로 호출이 실패함 | `uses:`가 태그/SHA인지(`@main` 금지), 호출 저장소가 common Actions에 접근 가능한지 | 태그 또는 SHA로 고정한다. 접근 설정은 [ci-deploy 규약](../standards/ci-deploy.md)을 따른다 |
| Python 패키지 설치가 `git` 부재로 실패함(Docker) | Dockerfile 빌드 스테이지에 `git`이 있는지 | 빌드 스테이지에서만 `git`을 설치하거나 wheel 자산 URL 방식으로 바꾼다 |
| `kt-contrast`가 앱 브랜드 오버라이드에서 3:1·4.5:1 미달을 보고함 | 미달 쌍(control-line/page, text-tertiary/page 등) | 값을 재조정한다. 검사를 끄지 않는다. 임시 예외는 owner·기한이 있는 `DEFERRED` finding으로만 둔다 |
| 조사 문서(`docs/survey/`)와 실제 저장소가 다름 | 조사 기준 커밋(`docs/survey/README.md` §2.1)과 현재 커밋 | 조사 본문을 고치지 않는다. 기준 커밋을 갱신한 새 절 또는 새 문서를 만든다 |
| 서브에이전트가 세션 한도로 중단돼 산출물이 절반만 남음 | 산출 파일의 마지막 절이 완결됐는지, 스키마 응답만 실패했는지 | 파일이 완결됐으면 재실행하지 않고 그 파일을 정본으로 쓴다. 미완결이면 해당 에이전트만 다시 실행한다 |
| 임시 worktree가 남아 있음 | `git worktree list`의 `prunable` 표시 | 활성 프로세스·미커밋 변경을 확인한 뒤 `git worktree remove`와 `git worktree prune`을 실행한다 |
| 같은 branch가 두 worktree에 checkout됨 | `git worktree list` | 한쪽을 detach하거나 제거한다. 리뷰 기준선은 `--detach`로만 만든다 |

같은 실패가 반복되면 새 task로 분리하고, 원인·재현 명령·복구·남은 위험을 이 문서 또는 task에 추가한다.
