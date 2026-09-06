# kor-travel-common 에이전트 개발 워크플로

이 문서는 branch, 검증, 독립 적대적 리뷰, PR, merge 정리의 실행 절차 정본이다(브리프 D-03·D-04·D-25, ADR-002·ADR-003). 확정 task는 T-007(문서 확정)이며 패키지 실물(T-101·T-201·T-302)이 생기면 §4의 패키지 명령을 대조해 확정한다. 마지막 갱신 2026-09-06.

배포 단위·계약 설계는 [architecture](../architecture/README.md), 공통 규칙은 [standards](../standards/README.md), 문서 역할과 갱신 규칙은 [documentation maintenance](documentation-maintenance.md)가 정본이다. 소비 저장소 쪽 절차는 [consumer adoption](consumer-adoption.md), 버전 발행은 [release](release.md)를 따른다. 명령은 bash 기준이며 Git Bash에서 동일하게 실행된다(Windows 표기와 경로·도구 프로필은 [개발 환경](../dev-environment.md)에만 둔다).

## 1. 범위와 기준선 확정

작업 시작 시 모든 문서를 통독하지 않는다. 다음 순서로 최소 문맥만 확인한다.

1. `AGENTS.md`, [문서 지도](../README.md), [현재 상태](../resume.md)를 읽는다. `CLAUDE.md`는 포인터이므로 이 순서에 추가하지 않는다.
2. 해당 상세 task가 있으면 그 파일 한 개에서 scope, 선행 조건, `외부 선행`, acceptance, gate를 확인한다. task를 고르는 경우에만 [tasks](../tasks.md)를 연다. 문서·review 전용 요청처럼 task가 없으면 관련 runbook 또는 template을 작업 기준으로 삼는다.
3. 변경 분야의 architecture 또는 standards 문서 한두 개와 관련 ADR만 읽는다. 조사 문서(`docs/survey/`)는 근거 인용이 필요할 때만 절 단위로 연다(규범이 아니다).
4. `git status`, 현재 branch, `origin/main`과의 차이를 확인하고 사용자 변경을 구분한다.
5. common에서 검증할 수 없는 gate(소비자 저장소 빌드·e2e, npm scope·PyPI 가용성, 소비자 CI, 외부 라이선스 결정)와 중요한 가정을 작업 전에 드러낸다. 실행하지 못할 검증은 시작 시점부터 `NOT_RUN(사유)` 후보로 적어 둔다(D-25).

반복 실패가 실제로 발생했을 때만 [failure patterns](agent-failure-patterns.md)를 읽는다.

## 2. Branch와 임시 worktree

정본 개발환경은 Linux/WSL bash이며 CI는 `ubuntu-24.04`다(D-03). Windows는 Tier 2로, `tools/*.py`는 Windows Python 3.11+에서도 동작해야 하지만 패키지 빌드·consumer-smoke는 ubuntu에서만 판정한다. 일반적인 단일 작업은 기본 checkout `F:/dev/kor-travel-common`(WSL `/mnt/f/dev/kor-travel-common`)에서 새 branch를 만들어 수행한다. branch 이름은 `agent/<agent>-<task>`이고 `origin/main`에서 분기한다. `main`에 직접 push하지 않는다.

```bash
cd /mnt/f/dev/kor-travel-common
git fetch origin main
git switch -c agent/<agent>-<task> origin/main
```

다음 중 하나가 실제로 필요할 때만 임시 worktree를 만든다(canview ADR-003 프로필 채택, D-03).

- 서로 다른 변경을 병렬 구현할 때
- dirty checkout과 완전히 격리해야 할 때
- 같은 immutable review 기준선을 전문 리뷰어 서브에이전트가 독립적으로 검사할 때

단순 문서·소규모 수정에는 만들지 않는다. 오래 걸리는 패키지 빌드·tarball 설치는 CI(`packages`·`consumer-smoke`)가 맡으므로 그것만을 이유로 worktree를 만들지 않는다.

```bash
mkdir -p /mnt/f/dev/kor-travel-common-wt
git -C /mnt/f/dev/kor-travel-common worktree add \
  -b agent/<agent>-<task> \
  /mnt/f/dev/kor-travel-common-wt/<agent>-<task> \
  origin/main
cd /mnt/f/dev/kor-travel-common-wt/<agent>-<task>
```

- 같은 branch를 여러 worktree에서 checkout하지 않는다.
- 사용자 변경이 있는 checkout을 정리하거나 덮어쓰지 않는다.
- `node_modules/`, `.venv/`, `*.local.md`, `.env`는 worktree마다 따로 존재한다. 새 worktree에서는 `npm ci`·`uv sync --locked`를 다시 실행하고, 로컬 비밀 파일은 복사하지 않는 것을 기본으로 한다.
- worktree는 상시 자원이 아니다. merge 또는 abandon 뒤 활성 process와 미커밋 변경이 없는지 확인한 다음 제거한다.
- 임시 worktree 삭제 전 필요한 commit이 다른 ref 또는 remote에 도달했는지 확인한다. 강제 삭제는 복구 계획 없이 사용하지 않는다.

```bash
git -C /mnt/f/dev/kor-travel-common worktree remove /mnt/f/dev/kor-travel-common-wt/<agent>-<task>
git -C /mnt/f/dev/kor-travel-common worktree prune
```

## 3. CodeGraph 수명주기

CodeGraph가 설치되어 있고 변경 범위 분석에 유용할 때만 사용한다.

1. 새 임시 worktree에서는 최초 한 번 `codegraph init -i`를 실행한다.
2. branch 전환, pull, merge, 대규모 이동 뒤에는 `codegraph sync`를 실행한다.
3. 분석 전후 `codegraph status`로 현재 worktree와 index가 일치하는지 확인한다.
4. 호출자 영향이 넓은 변경 — `packages/ui`의 공개 export·prop 기본값, `packages/tokens`의 토큰 이름, `packages/py`의 공개 모듈 시그니처, `tools/*.py`의 판정 어휘 — 는 편집 전에 `explore` 또는 `impact`로 범위를 확인한다.

도구가 없거나 MCP 연결이 실패하면 설치된 것처럼 기록하지 않는다. `rg`, `tsc --noEmit`, `mypy`, 테스트와 수동 추적으로 대체하고 한계를 journal에 남긴다.

## 4. 구현과 검증

구현은 선택한 task의 acceptance를 만족하는 최소 변경으로 제한한다. 검증은 변경 범위에 맞춰 아래 사다리에서 필요한 계층만 실행한다.

```text
문서 검증 (link · plan · unittest · git diff --check)
  -> 패키지 빌드·타입 (npm build · tsc --noEmit · uv build · mypy)
  -> 단위 (vitest + RTL + jsdom · pytest · tools 자기 테스트)
  -> tarball 설치 (npm pack → 임시 디렉터리 설치 · wheel 설치 → import)
  -> 소비자 빌드·e2e (pinned SHA 소비자에서 next build webpack·Turbopack · playwright)
  -> 소비자 배포 스모크 (소비자 저장소 runbook; common에서는 NOT_RUN)
```

층별 명령·CI job 대응표는 [개발 환경 §6](../dev-environment.md#6-검증-명령-사다리)이 정본이며 여기에 복제하지 않는다. 문서 검증 4종(`validate_document_links`·`validate_plan`·`unittest`·`git diff --check`)은 모든 PR에서 실행하고, 패키지 빌드·타입·단위는 `packages/*`·`tools/*` 변경 시, tarball·wheel 설치는 공개 API·CSS·exports 변경과 릴리스 시, 소비자 빌드·e2e는 릴리스 rc와 마크업 계약 변경 시 실행한다. 소비자 배포 스모크는 소비자 저장소 runbook의 몫이며 common에서는 항상 `NOT_RUN(소비자 저장소 실행)`이다.

- 패키지 스크립트 이름과 CI job 이름(`packages`·`python-package`·`consumer-smoke`)은 T-101·T-201·T-302·T-010에서 확정한다. 그 전까지 패키지 명령은 후보이며, 실제 실행한 명령만 evidence에 적는다.
- 생성물(`tokens.json`·`tokens.ts`·`tailwind-preset.cjs`)은 정본 `tokens.css`와 함께 변경하고 빌드 diff 검사로 검증한다(D-12). 정본과 생성물의 수동 불일치는 금지다.
- 소비자 저장소가 필요한 gate를 common 로컬 실행으로 대체해 통과 처리하지 않는다. 실패·미실행 gate는 영향, 이유, 재현 명령과 후속 task를 기록하고, 미실행 검증이 남은 task는 `DONE` 전에 `외부 선행`으로 승격한다(D-25). 0 test·skip을 pass로 집계하지 않으며, 명령을 적은 것은 실행 증거가 아니다.
- 리뷰 finding을 고친 뒤에는 영향받은 검증을 다시 실행한다.

## 5. 전문 리뷰어 서브에이전트 2인 적대적 리뷰

비단순 변경은 PR 전에 전문 영역이 서로 다른 리뷰어 서브에이전트 2명이 독립적으로 적대적 리뷰한다(canview full gate, D-04). light/full 판정 주체는 merge 담당이며 작성자와 판정자는 같은 사람·에이전트일 수 없다.

다음 변경은 면제하지 않는다(D-04 비면제 목록).

- `docs/standards/*` — 토큰·UX·반응형·프런트/백엔드 스택·OpenAPI·CI/배포·라이선스·버전·에이전트 규약
- `versions.json` — floor/recommended/exceptions/blocked/enforce
- `packages/*`의 공개 API·CSS — export, prop 기본값, 정렬 모드, 토큰 이름·의미, `data-slot`·`data-testid`, CSS 파일 경로
- `.github/workflows/*` — common CI와 재사용 워크플로
- `AGENTS.md`, `SKILL.md`, `docs/README.md`, ADR, runbook, task/review 규칙·index·template
- 작업 정책, 품질 gate, 문서 정본 관계의 변경

일반 면제는 다음을 모두 만족할 때만 가능하다.

- 오탈자·공백 또는 의미와 정본 역할이 같은 link의 label/target correction뿐이다.
- source code, 생성물, build/config, 워크플로와 위 비면제 문서를 바꾸지 않는다.
- 동작, 계약, acceptance, gate, 심각도, disposition과 정본 우선순위를 바꾸지 않는다.
- 작성자가 아닌 merge 담당이 diff를 확인하고 면제 근거를 PR에 승인한다.

리뷰 완료 뒤 원본 결과를 그대로 보존하고 통합 report의 disposition·재검증 결과와 archive index 한 행만 갱신하는 **review closure artifact**는 같은 리뷰를 재귀적으로 다시 시작하지 않는다. 이 예외로 규범 문구를 바꾸면 안 되며, 바꾸면 새 기준선으로 2인 리뷰를 다시 수행한다.

소비 저장소에는 공통 절 B(Ruthless Review)와 [review template](../reviews/adversarial/TEMPLATE.md), full/light 표준을 [agent conventions](../standards/agent-conventions.md)로 배포하되 채택은 SHOULD다.

### 5.1 Review manifest와 immutable 기준선

1. 구현과 1차 검증을 마친 review candidate를 commit하고 commit hash를 기록한다.
2. 두 reviewer에게 같은 manifest를 제공한다. manifest에는 기준 commit과 parent/base, task 또는 요청, scope·범위 밖, 관련 architecture·standards·acceptance, 실행 가능한 검증을 넣고 `docs/reviews/adversarial/evidence/YYYY-MM-DD-<scope>-manifest.md`로 보존한다.
3. reviewer 실행 ID·역할·시작 시각과 전달한 review request 원문을 reviewer별 evidence 파일에 기록한다.
4. 각 reviewer는 아래 두 격리 방식 중 하나를 사용하고 실제로 확인한 hash와 clean 상태를 결과에 남긴다. 이동 가능한 branch를 read-only 기준선으로 부르지 않는다.

**Commit object-only 방식**은 빌드가 필요 없는 문서·diff 리뷰에 쓴다. 모든 내용은 plain worktree가 아니라 `git show`와 `git diff`로 읽는다.

```bash
git -C /mnt/f/dev/kor-travel-common cat-file -e "<commit>^{commit}"
git -C /mnt/f/dev/kor-travel-common rev-parse "<commit>^{commit}"
git -C /mnt/f/dev/kor-travel-common diff --find-renames <base> <commit>
git -C /mnt/f/dev/kor-travel-common show <commit>:<path>
```

**Detached worktree 방식**은 빌드·테스트·filesystem tool이 필요할 때 쓴다.

```bash
mkdir -p /mnt/f/dev/kor-travel-common-wt
git -C /mnt/f/dev/kor-travel-common worktree add --detach /mnt/f/dev/kor-travel-common-wt/review-<id> <commit>
git -C /mnt/f/dev/kor-travel-common-wt/review-<id> rev-parse HEAD
git -C /mnt/f/dev/kor-travel-common-wt/review-<id> status --porcelain=v1
```

`HEAD`는 manifest의 commit과 같고 review 시작·종료의 `status --porcelain=v1` 출력은 비어 있어야 한다. `npm ci`·`uv sync`가 만드는 `node_modules/`·`.venv/`는 gitignore 대상이라 porcelain 출력에 나타나지 않지만, 추적 파일이 바뀌면(lockfile 재생성 등) 기준선이 오염된 것이므로 결과를 폐기한다. 종료 뒤 [worktree 정리 절차](#8-merge-또는-abandon-뒤-정리)로 제거한다.

5. 두 reviewer가 각자의 원본 결과를 확정해 저장하기 전에는 상대방의 report나 finding을 보여 주지 않는다.

### 5.2 전문 영역 배정

변경에 맞게 서로 다른 실패 관점을 배정한다. 라이브러리 저장소 기본 배정은 다음과 같다.

| Reviewer | 우선 전문 영역 | 필수 공격 관점 |
|---|---|---|
| A | 소비자 계약·프런트: 토큰 이름·값·계층, Tailwind 클래스 탐지(`@source`), 마크업 계약(`data-slot`·`data-testid`·heading·sr-only), React 19 peer·ref, 접근성, 시각 회귀 | 값 diff, `@source` 누락으로 인한 클래스 미탐지, 별칭·접두 충돌(`--kt-*` vs 앱 접두), e2e 셀렉터 파손, 대비 미달·다크 값 누락, prop 기본값·정렬 모드 변경, alias 없는 토큰 폐기 |
| B | 백엔드·배포·정합: OpenAPI 계약(RFC7807·health 경로·`X-Request-ID`), 버전 레지스트리·판정 어휘, lockfile·태그·자산, CI 워크플로 하드닝, 라이선스 고지·출처, 문서 정본 관계 | 산출물 drift, 같은 버전 재발행·`@main` 참조, lock `integrity` 누락, 액션 핀 해제, SPDX·NOTICE·PROVENANCE 누락, 정본 충돌(브리프 ↔ ADR ↔ standards), 검증 누락·`NOT_RUN` 은폐 |

문서 구조 변경이라면 A는 정보 정본·링크·agent 실행 가능성(읽기 순서대로 따라갔을 때 막히는 곳), B는 규칙 충돌·검사기 문법(`validate_plan.py` 5열·ID)·회귀 검증처럼 영역을 다시 배정한다. Python 전용 변경이라면 A는 계약(pydantic 모델·problem+json·export 결정성·3.11 문법), B는 패키징(extras·`uv.lock`·starlette 매트릭스·wheel 자산)을 맡는다. 두 reviewer 모두 정상 경로 확인에 그치지 않고 숨은 가정, 경계값, 고장 주입, 복구 불가 상태와 다른 소비자의 부작용을 찾는다.

### 5.3 독립 산출물과 심각도

심각도는 다음처럼 판정한다.

| 등급 | 기준 | merge 효과 |
|---|---|---|
| `P0` | 비밀·운영 호스트 유출, 소비자 배포 산출물의 복구 불가 손상, 라이선스 위반(GPL 고지 누락·금지 원천 추출·pinvi L6 전 추출), 태그·릴리스 경계 붕괴(같은 버전 재발행·태그 이동) | 즉시 `BLOCK` |
| `P1` | 정상적인 실패 조건에서 소비자 계약·정합성·필수 gate·감사성을 깨뜨림(토큰 이름 무예고 폐기, `data-testid` 파손, `versions.json` 판정 오류, `NOT_RUN`을 pass로 집계, 정본 충돌) | `BLOCK` |
| `P2` | 기능·검증·유지보수에 실질적 결함이지만 현재 merge 안전 경계를 직접 깨지 않음 | 수정 권고, 조건부 연기 가능 |
| `P3` | 작은 탐색성·표현·비기능 품질 문제 | 수정 또는 명시적 추적 |

각 reviewer는 최소한 다음을 제출한다.

- reviewer execution ID, 시작·종료 시각, 전문 영역
- 전달받은 manifest와 실제 검토한 commit hash, 격리 방식, 파일 범위
- 실행하거나 읽은 검증과 검토하지 못한 범위
- `P0`~`P3` finding: 위치, 근거, 재현 또는 실패 시나리오, 영향, 권고 — ID는 `{A|B}-P{0-3}-{NN}`
- finding이 없더라도 공격한 시나리오와 남은 불확실성
- merge verdict: `BLOCK`, `CONDITIONAL`, `PASS`

주 작업 에이전트는 교차 비교 전에 두 원본 결과를 `docs/reviews/adversarial/evidence/YYYY-MM-DD-<scope>-reviewer-{a,b}.md`에 각각 보존한다. 요약하면서 finding을 삭제하거나 심각도를 낮추지 않는다. 근거 없는 취향 차이는 finding으로 만들지 않지만, 시험하지 않은 계약 가정을 단순히 "문제 없음"으로 닫지도 않는다. 통합 report의 상태 어휘는 `IN_REVIEW` → `COMPLETE` → `POST_FIX_REVIEW`(post-fix 재검토 중)이며, 최종 verdict는 별도 줄에 적는다(D-04).

### 5.4 결과 반영과 gate

두 독립 리뷰가 끝난 뒤에만 주 작업 에이전트가 결과를 교차 검토한다.

1. 매 리뷰 실행마다 [review template](../reviews/adversarial/TEMPLATE.md)으로 `docs/reviews/adversarial/YYYY-MM-DD-<scope>.md`를 새로 만든다. 같은 날 같은 범위를 반복하면 `-02`, `-03`을 붙인다.
2. 통합 report에서 두 원본 evidence를 연결하고 finding을 누락 없이 옮긴다. 중복은 연결하되 원래 ID, 심각도와 관점을 보존한다.
3. 각 finding은 아래 상태 중 하나를 사용한다.

| 상태 | 의미 | 허용 등급 |
|---|---|---|
| `OPEN` | 아직 조치·판정되지 않음 | 전체 |
| `FIXED` | 코드·문서·시험을 수정하고 검증함 | 전체 |
| `REJECTED_WITH_EVIDENCE` | finding 전제가 틀렸음을 근거와 원 reviewer 재확인으로 입증 | 전체 |
| `DEFERRED` | owner·상세 task·gate·기한을 연결해 후속 차단 | `P2`/`P3`만 |

4. `P0`/`P1`은 `FIXED` 또는 `REJECTED_WITH_EVIDENCE`로 원 reviewer가 재확인하기 전 merge하지 않는다. 단순 risk acceptance나 "release 차단" 표시는 P0/P1 closure가 아니다.
5. `P2`/`P3`의 `DEFERRED`는 owner, 상세 task, 적용 gate와 목표 시점이 모두 있어야 하며 열린 위험으로 표시한다.
6. 수정 위치, commit 또는 evidence, 재검증 명령과 결과를 각 finding에 연결한다.
7. 규범·코드 수정 결과를 새 commit으로 만들고 두 reviewer가 그 post-fix commit에서 자신의 finding과 전체 delta의 회귀를 재검토한다. post-fix 재검토는 별도 report `YYYY-MM-DD-<scope>-post-fix.md`와 evidence `…-post-fix-reviewer-{a,b}.md`로 남긴다(D-04).
8. 두 재검토 verdict와 남은 위험을 통합 report, 관련 task와 PR 본문에 반영한다.

과거 review report에 새 실행 결과를 덧붙이지 않는다. 리뷰 파일 명명, correction, archive index 규칙은 [review archive](../reviews/README.md)를 따른다.

## 6. 기록 갱신

변경과 직접 관련된 기록만 갱신한다.

- 현재 상태나 다음 한 작업이 바뀌면 `docs/resume.md`
- task 상태·acceptance·evidence가 바뀌면 `docs/tasks.md`와 해당 상세 task(완료는 `docs/tasks-done.md`로 이동, 날짜·PR은 제목 괄호)
- 구조적 결정이 생기면 새 ADR과 `docs/adr/README.md`(단일 색인, 다음 후보 번호 갱신; `docs/decisions.md`는 두지 않는다)
- 공통 규칙이 바뀌면 해당 `docs/standards/*`와 [consumer adoption](consumer-adoption.md)의 관련 절, `CHANGELOG.md` `### standards`
- 작업 재현 정보가 필요하면 `docs/journal.md` 최상단(도구 fallback·미실행 검증·소비 저장소 상태 포함)
- 소비자 가시 변경이면 `CHANGELOG.md`의 패키지별 절(`tokens`/`ui`/`py`/`standards`)
- 적대적 리뷰를 실행했다면 새 review report와 `docs/reviews/README.md`

상세 형식과 문서 이동 절차는 [documentation maintenance](documentation-maintenance.md)를 따른다.

## 7. Stage, 보안 감사와 PR

파일을 경로별로 명시해 stage한다. `git add .`과 `git add -A`는 사용하지 않는다.

1. `git status`로 사용자 파일, 로컬 파일(`*.local.md`, `.env*`), 빌드 산출물이 섞이지 않았는지 확인한다.
2. `git diff --staged` 전체를 직접 읽는다.
3. secret, private key, API key, 세션·토큰 값, 운영 호스트 주소·IP·도메인, 관리자 자격증명, 개인정보가 없는지 검사한다. common은 prod 값을 가질 이유가 없으므로 전체 트리가 redaction 대상이다(D-18).
4. 생성물·문서 링크·task index가 source와 일치하는지 확인한다(§4 문서 검증 4종). 새 소스 파일에는 SPDX 헤더와 `Origin:` 행이 있어야 한다([CONTRIBUTING](../../CONTRIBUTING.md) §2; `tools/check_spdx.py`는 T-003 잔여).
5. branch를 push하고 `main` 대상 Draft PR을 만든다. `main`에 직접 push하지 않는다. 커밋 제목은 Conventional Commits 영어 type + 한국어 문장이다(D-32).

```bash
git status --short
git diff --staged
git diff --staged | grep -nEi 'api[_-]?key|secret|password|passwd|token|AKIA[0-9A-Z]{16}|BEGIN [A-Z ]*PRIVATE KEY|[0-9]{1,3}(\.[0-9]{1,3}){3}'
git diff --check
python3 -B -X utf8 tools/validate_document_links.py
python3 -B -X utf8 tools/validate_plan.py
```

PR 본문에는 [PR 템플릿](../../.github/pull_request_template.md)의 6항목을 모두 채운다.

- task와 변경 목적
- 통과한 gate와 정확한 실행 명령
- 전문 리뷰어 2명의 영역, report 링크와 최종 disposition(light 판정이면 판정자와 근거)
- 실패 또는 미실행 검증과 남은 위험(`NOT_RUN(사유)` 포함)
- evidence 위치와 digest(tarball·wheel·SHA256SUMS·스크린샷)
- rollback 방법

CI(`docs`·`tools`·`packages`·`python-package`·`secret-scan`·`check-versions`), 필수 reviewer gate와 미해결 `P0`/`P1` 확인이 끝나기 전 merge하지 않는다. 릴리스 태그는 PR merge 뒤 [release](release.md) 절차로만 만든다.

## 8. Merge 또는 abandon 뒤 정리

1. remote의 PR merge 결과와 `origin/main` commit을 확인한다.
2. 기본 checkout을 `main` 또는 다음 작업 branch로 전환하고 최신 상태로 맞춘다.
3. CodeGraph를 사용했다면 `sync` 후 `status`를 확인한다.
4. 임시 구현·리뷰 worktree마다 process, status, 보존할 commit을 확인하고 제거한 뒤 `git worktree prune`을 실행한다. `git worktree list`에 `prunable`이 남아 있으면 정리가 끝나지 않은 것이다.
5. 완료 task, review disposition, 다음 작업을 필요한 기록 문서에 반영한다(§6). 릴리스가 필요한 변경이면 [release](release.md)로 이어 간다.

abandon할 때도 유용한 finding과 재현 근거가 있으면 상세 task나 새 review report에 남기고, 브랜치와 worktree를 제거하기 전에 복구 가능한 remote/ref를 확보한다.
