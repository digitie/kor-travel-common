# T-011 post-fix-07 독립 적대적 리뷰 A 원본

- 실행 ID: A-T011-POST7-20260907-210744
- 최종 판정: **PASS**. 새 P0/P1/P2 finding 0건, 새 P3 발견 없음. 누적 A 코드 finding은 FIXED이며 기존 문서 finding의 확정 처분은 유지한다.
- immutable candidate: `4680bacdf285f2cc86f1a18cc1de29ff4129f2a8`
- 전체 기준 base: `3977c00a5b4ffa21a8d29f96dd9531efbe3a0cb5`
- tree: `9aaede40d0905e2b989971650a806f1ba7f48aa0`
- 새 격리 경로: `F:/dev/kor-travel-common-wt/review-t011-post7-a`, detached HEAD.
- 시작: 2026-09-07 21:07:44.869 KST. 종료 상태 확인: 2026-09-07 21:11:13.671 KST.
- 시작/종료 HEAD 및 tree는 위 값과 같고 `git status --porcelain=v1`는 두 번 모두 빈 출력(clean).
- 후보 소스·문서·시험과 source `.git/config`/`core.worktree`를 수정하지 않았다. 소비자 쓰기, commit/push, registry 게시 없음. 임시 fixture와 reviewer 소유 `.git/codex-audit/` probe/원본만 작성했다. 상대 reviewer 결과 및 이전 raw/report는 읽지 않았다.

## 요청과 변경 경계

요청한 registry missing/self/intermediate symlink, schema/path/값 redaction, 기존 app/validator 반례, manifest/lock/app/workspace/requirements의 직접·중간·외부 symlink, 출력 채널 및 schema parity를 양 OS에서 재현했다. 이전 결과를 성공 근거로 복사하지 않고 보유 A probe 코드를 새 후보에서 실행했다.

전체 base..candidate는 40파일(+2452/-60)이다. 직전 56d6ae11..candidate는 **tools/check_versions.py와 tests/test_check_versions.py 두 파일(+17/-2)**뿐이며 전체 delta를 직접 읽었다. 제품 변경은 registry 읽기·검증 예외를 원문 없이 같은 일반 오류로 출력하는 것이다. app symlink 처리, manifest schema/validator, task·표준·초안은 직전 코드 후보와 동일하다. 전체 역사 review 본문 재열람은 하지 않았고, 전체 tracked 파일의 정적 gate를 실행했다.

## 실제 실행 검증

Windows Python 3.14.3, WSL uv managed Python 3.11.15. JSON Schema 검사는 jsonschema 4.26.0을 사용했다. WSL 전체·focused 검증은 `uv run --no-project --python 3.11 --with jsonschema==4.26.0 python`으로 실행해 선택 의존성 부재 skip을 없앴다.

| 명령 | Windows | WSL |
|---|---|---|
| `python -B -X utf8 -m unittest discover -s tests -q` | 203 tests, 111.728초, OK, skip 0 | 203 tests, 58.609초, OK, skip 0 |
| `python -B -X utf8 -m unittest discover -s tests -p test_validate_manifest.py -q` | 23 tests, 10.565초, OK, skip 0 | 23 tests, 7.473초, OK, skip 0 |
| `tools/validate_plan.py` | 106 task, 오류 0 | 동일 |
| `tools/validate_document_links.py` | 344 documents, 2287 targets, 오류 0 | 동일 |
| `tools/check_spdx.py` | 32파일, 오류 0 | 동일 |
| `tools/scan_secrets.py --all` | 434파일, 발견 0, 예외 0 | 동일 |
| `tools/check_prod_redaction.py --all` | 434파일, 발견 0, 예외 0 | 동일 |
| `tools/check_versions.py --self-check` | exit 0 | exit 0 |
| `git diff --check 3977c00a5b4ffa21a8d29f96dd9531efbe3a0cb5 HEAD` | exit 0 | exit 0 |

Python 도구는 모두 `-B -X utf8`로 실행했다. 정적 gate harness는 `.git/codex-audit/t011-post7-a-gates.py`이다. WSL의 Git 읽기는 프로세스 환경 `GIT_DIR=/mnt/f/dev/kor-travel-common/.git/worktrees/review-t011-post7-a`, `GIT_WORK_TREE=/mnt/f/dev/kor-travel-common-wt/review-t011-post7-a`로 지정했으며 config를 변경하지 않았다.

정확한 CI는 `gh pr view 10 --repo digitie/kor-travel-common --json headRefOid,statusCheckRollup`로 직접 확인했다. 반환 head는 candidate full SHA와 같았으며 [run 34120043104](https://github.com/digitie/kor-travel-common/actions/runs/34120043104)의 docs, tools(ubuntu-24.04), tools(windows-2025), secret-scan, check-versions 5개가 모두 SUCCESS였다. 위 시험 건수는 원격 추정이 아닌 이번 독립 로컬 실행 결과다.

## 직접 반례와 누적 finding disposition

실행 명령:

```text
Windows cwd: F:/dev/kor-travel-common-wt/review-t011-post7-a
python -B -X utf8 F:/dev/kor-travel-common/.git/codex-audit/t011-post7-a-run.py
python -B -X utf8 F:/dev/kor-travel-common/.git/codex-audit/t011-post7-a-registry.py
python -B -X utf8 F:/dev/kor-travel-common/.git/codex-audit/t011-post7-a-base.py

WSL cwd: /mnt/f/dev/kor-travel-common-wt/review-t011-post7-a
uv run --no-project --python 3.11 --with jsonschema==4.26.0 python -B -X utf8 /mnt/f/dev/kor-travel-common/.git/codex-audit/t011-post7-a-run.py
uv run --no-project --python 3.11 python -B -X utf8 /mnt/f/dev/kor-travel-common/.git/codex-audit/t011-post7-a-registry.py
uv run --no-project --python 3.11 python -B -X utf8 /mnt/f/dev/kor-travel-common/.git/codex-audit/t011-post7-a-base.py
```

### A-T011-P2-15: FIXED — registry 오류 원문 비공개

최소 원 반례는 분할 생성한 비밀형 경로 component 아래 registry를 만들지 않고 `check_versions.py --self-check --registry <missing>`을 실행하는 것이다. 양 OS candidate 결과는 다음과 같다.

```text
missing-sensitive-registry exit 2 traceback False private-marker-leak False
```

추가 registry corpus는 누락, leaf self-symlink, 중간 디렉터리 self-symlink, 디렉터리 입력, 잘못된 JSON, 잘못된 UTF-8, 잘못된 schema 값, 미지 field 이름, 잘못된 axis 값, 최상위 list **10개 음성 입력**이다. 전부 두 OS에서 아래 같은 결과였다.

```text
exit 2 generic True traceback False marker-leak False artifacts []
```

`generic`은 stdout 전체가 `::error title=check_versions::레지스트리 입력 구조 오류` 한 줄인지 대조했다. stdout/annotation·stderr와 명시한 JSON/Markdown/step summary 경로를 검사했고 marker 및 traceback이 없으며 오류 입력은 보고서 파일을 생성하지 않았다. 정상 외부 alias registry와 지원하는 4부분 숫자 floor 대조군 2개는 exit 0을 유지했다.

처음 axis 값으로 쓴 4부분 숫자는 지원 버전 형식이어서 오류가 아니었다. 이를 정상 대조군으로 보존하고 비숫자 접두를 붙인 값을 추가 음성 입력으로 실행했다. 이 fixture 보정은 후보 코드 변경이나 실패 은폐가 아니다.

**원인·수정 기원**: 원 base의 `tools/check_versions.py`를 `git show 3977c00a5b4ffa21a8d29f96dd9531efbe3a0cb5:tools/check_versions.py`로 읽어 임시 파일에서 같은 원 반례를 두 OS에 다시 실행했다.

```text
base-missing-sensitive-registry exit 2 traceback False private-marker-leak True
```

이 누출은 T-011 이전부터 존재했으며 T-011이 만든 회귀로 집계하지 않는다. 후보는 registry 예외 처리의 `{exc}`를 일반 문자열로 교체해 이 경계를 수정했다. 정상 registry 파싱/판정 정책을 바꾸지 않았음을 코드 delta와 정상 대조군으로 확인했다.

### A-T011-P2-13/14: FIXED 유지

- P2-13: 빈 lockfiles + `app=loop/etl`의 중간 self-symlink와 외부 alias 아래 missing app는 양 OS exit 2, traceback/보고서 없음. 정상 내부 app alias는 Python/NO_LOCK을 계속 보고하며 symlink 없는 ordinary missing app 대조군도 보존됐다.
- P2-14: validator의 registry leaf self-symlink는 양 OS exit 1, traceback/runtime-error/path-leak False. validator 자체 계약은 exit 0/1이므로 checker의 exit 2와 혼동하지 않았다.

### 이전 코드 finding: FIXED 유지

- A-T011-P1-01/02/08, A-T011-P2-03/04/05/06/07/10/11/12의 원 반례를 새 후보에서 실행했다. 새 재발 없음.
- 10개 초안의 stdlib/JSON Schema 오류 0. 경로 395 corpus mismatch 0. 제어문자·DEL·경계 공백·절대경로·dot/dotdot·빈 segment와 날짜 9개(윤년·0000/9999·끝 LF·비ASCII)를 포함한다. kind list/dict, enforce, repo alias, 잘못된 app, 미지 key는 일반 오류이며 입력 원문 누출 없음.
- npm workspace selector는 실제 멤버 Node BELOW_FLOOR/React FLOATING_REF를 보고한다. 명시 root selector 대조군 및 autodiscovery와의 관계가 유지됐다. 빈 lockfiles ETL은 Python/NO_LOCK을 root workflow와 함께 보고한다.
- requirements 11형식 × 명시 lock/빈 lock 앱: root 이탈·외부 symlink·순환·누락·self-symlink는 exit 2, traceback/외부 값/보고서 없음. 정상 내부 재귀 include는 보고서 생성.
- direct requirements/npm lock, 동반 package.json/pyproject.toml, 직접 app, workspace, 중간 lock 디렉터리, root/manifest/registry의 checker self-symlink는 양 OS exit 2, traceback/보고서 없음.
- missing manifest/registry 및 중간 manifest/registry loop는 validator exit 1/checker exit 2. 외부 app/lock/workspace는 파일을 읽는 checker에서 exit 2이고 schema validator는 파일 실존 검사가 아닌 형식 검사로 구분했다. 정상 내부 alias 실파일은 처리하고 alias 아래 missing target은 일반 입력 오류로 닫는다.
- 민감한 workspace와 transitive lock 경로 재조합 및 DEL lock path에서 stdout/stderr/JSON/Markdown/step summary에 원문 누출 없음. 시험 marker는 문자열 분할 생성하고 출력에는 포함 여부만 기록했다.
- ordinary missing lock의 report 모드 exit 0 + NO_LOCK은 설치 성공으로 세지 않았다.
- 역사 문서 집계 A-T011-P3-09는 기존 FIXED 처분을 유지한다. 이 원본에서 과거 review 본문의 집계 재감사를 실행했다고 주장하지 않는다.

## 한계·NOT_RUN

- 실제 소비자 build/e2e·npm ci·uv sync·패키지 설치/게시·release는 NOT_RUN(독립 common 읽기·임시 fixture 범위, 소비자 쓰기/게시 금지).
- 원격 CI job 로그의 내부 시험 건수 재집계는 NOT_RUN. exact candidate와 5개 check 성공은 직접 조회했다.
- 역사 review/raw의 finding 집계 재감사는 NOT_RUN(독립성·이전 결과 비열람 유지). 현재 후보의 문서 링크/plan/비밀/redaction gate는 실행했다.
- 이 PASS는 지정 후보의 구현·반례·필수 gate 검토 판정이다. 소비자 채택/설치/외부 gate 성공이나 T-011의 문서 종료 commit을 미리 승인한 것이 아니다.
