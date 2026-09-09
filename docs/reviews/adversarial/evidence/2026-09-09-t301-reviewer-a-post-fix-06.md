# T-301 post-fix-06 적대적 리뷰 A 원본

- Review ID: `T301-20260909-post-fix-06-A-20260909T123419+09:00`
- 판정: **BLOCK**
- 검토 방식: 상대 reviewer 결과·통합 report를 읽지 않은 독립 검토. 후보 파일은 수정하지 않았다.

## 불변 입력과 격리 상태

- base commit: `afc8d1bf166d0ddcbee059252eb5cee245157dcd`
- base tree: `3eddd2ad90d10813bb37cd00f5ac9be5a1ef13ba`
- candidate commit: `d88f2a0446e114541f52de169630cd09e27f429a`
- candidate tree: `6702e7f844bf3e3f9112a007351f0183632496a3`
- manifest: `docs/reviews/adversarial/evidence/2026-09-09-t301-post-fix-06-manifest.md`
- manifest SHA-256: `b5b9decc76cecba0e84d7a987443f0549df90174e00ac8d2dd85beb8865d108d`
- detached worktree: `F:\dev\kor-travel-common-wt\review-t301-post-a06`
- candidate checkout 직후 `git status --short --branch`: `## HEAD (no branch)`, 추가·수정 파일 없음.
- candidate/base tree와 manifest SHA를 `git rev-parse`·`git show`·Python SHA-256으로 확인했다. 원본 보고서 작성 전까지 candidate tree는 변경되지 않았다.

## 판정 요약

| 등급 | ID | 결과 |
|---|---|---|
| P0 | — | 재현 finding 없음 |
| P1 | A-P1-01 | SHOULD reason의 부정 의미를 우회해 외부 계약 예외로 등록 가능 — OPEN |
| P1 | A-P1-02 | `M10`·`동반 PR` 증명 token의 Unicode/underscore/punctuation 경계 우회 — OPEN |
| P1 | A-P1-03 | `외부 계약` 긍정 증명이 접미사를 구분하지 않는 substring 검사 — OPEN |
| P2 | A-P2-01 | task ID regex가 실제 파일명 ID 뒤의 비정상 suffix를 허용 — OPEN |
| P2 | A-P2-02 | resume/task/journal이 post-fix-05 수치와 후보를 계속 정본처럼 표시 — OPEN |
| P3 | — | 별도 재현 finding 없음 |

P1이 세 건 남아 있어 로컬·CI green과 무관하게 BLOCK이다.

## Finding

### A-P1-01 — SHOULD reason의 부정 의미가 fail-open

- 근거: `tools/openapi_exceptions.py:65-71`, 검증 적용 `:482-490`.
- 재현: canonical YAML의 첫 S1 `reason`을 다음 문자열로 바꾸고 `M10 동반 PR T-483`을 남긴 뒤 `load_registry(..., as_of=date(2026, 9, 9))`를 호출했다.
- 결과: 아래 모두 **ACCEPT**였다.

  - `소비하는 외부 계약은 미승인이다. M10 동반 PR T-483`
  - `소비하는 외부 계약은 미적용이다. M10 동반 PR T-483`
  - `소비하는 외부 계약은 미지원이다. M10 동반 PR T-483`
  - `소비하는 외부 계약은 미수용이다. M10 동반 PR T-483`
  - `소비하는 외부 계약은 미확정이다. M10 동반 PR T-483`
  - `소비하는 외부 계약은 미존재한다. M10 동반 PR T-483`
  - `소비하는 외부 계약은 미실행이다. M10 동반 PR T-483`
  - `소비하는 외부 계약은 아닐까요? M10 동반 PR T-483`
  - `소비하는 외부 계약은 무관하다. M10 동반 PR T-483`
  - `소비하는 외부 계약은 배제된다. M10 동반 PR T-483`
  - `소비하는 외부 계약은 제외된다. M10 동반 PR T-483`
  - `소비하는 외부 계약 — noncontract 이다. M10 동반 PR T-483`
  - `소비하는 외부 계약 — non_contract 이다. M10 동반 PR T-483`
  - `소비하는 외부 계약 — non‑contract 이다. M10 동반 PR T-483`
  - `소비하는 외부 계약 — neither 이다. M10 동반 PR T-483`
  - `소비하는 외부 계약 — none 이다. M10 동반 PR T-483`

  기존 회귀 시험의 `아니다`, `아닙니다`, `거짓`, `미채택`, `거부`, `무효` 등은 거부하지만, 의미상 동일한 부정 표현의 넓은 집합은 `NEGATED_EVIDENCE_RE`에 없어 우회한다.
- 영향: 외부 소비 계약이 실제로 없다는 reason도 긍정형 substring과 M10 증명만 맞추면 S 계층 예외 레지스트리에 들어간다. 이후 생성 표와 소비자 매니페스트가 허위 예외를 정본처럼 배포한다.
- 권고: substring denylist를 늘리는 방식 대신 외부 계약 assertion을 구조화해 주어·계약 표면·긍정 서술을 분리하고, 부정/불확정/비적용 문장을 fail-closed로 판정한다. 새 한국어 활용·영어 합성어·Unicode punctuation corpus를 회귀 시험에 포함한다.
- disposition: **OPEN / BLOCK**.

### A-P1-02 — `M10`·`동반 PR` 증명 token 경계가 우회됨

- 근거: `tools/openapi_exceptions.py:74-75`, 적용 `:491-492`. lookaround가 ASCII 영숫자만 배제하고 underscore·한국어 문자·점 suffix 등을 token 일부로 취급하지 않는다.
- 재현: 첫 S1의 기존 `map M10과 같은 동반 PR 규칙`을 `map 근거`로 제거해 다른 정상 token이 남지 않게 한 뒤, 외부 계약 문구 뒤에 아래 하나씩만 삽입했다. `load_registry`가 모두 **ACCEPT**했다.

  - `M10_foo`, `M10_`, `M10가`, `M10.1`
  - `동반 PR_foo`, `동반 PR_`, `동반 PR가`, `동반 PR.1`

  `M100`, `M10X`, `미동반 PR`, `동반 PRX`는 기존 시험처럼 거부됐지만, 이 시험 집합은 ASCII 영숫자 suffix만 다룬다.
- 영향: M10 동반 pin PR 또는 동반 PR이라는 실제 증명이 없는 문자열을 evidence token으로 위장할 수 있다. 특히 `동반 PR가`는 한국어 조사/접미사가 붙은 문장이고 `M10_foo`는 식별자이므로 정확한 ID token이 아니다. 허위 cross-repository coordination 근거가 S 예외 승인 조건을 통과한다.
- 권고: ID token을 lookaround substring으로 판정하지 말고 허용된 증명 문법을 파싱한다. 최소한 Unicode letter/number와 underscore를 양쪽 경계에서 배제하고 `M10`의 dot/suffix 및 `동반 PR`의 한국어 suffix를 명시적으로 거부하는 회귀 corpus를 추가한다.
- disposition: **OPEN / BLOCK**.

### A-P1-03 — `외부 계약` 긍정 증명이 접미사 substring에 오염됨

- 근거: `tools/openapi_exceptions.py:65`, 적용 `:485-486`.
- 재현: 첫 S1 reason을 아래처럼 바꾸고 `M10 동반 PR T-483`을 포함했다. 실제 계약을 뜻하는 독립 명사구가 아니어도 **ACCEPT**됐다.

  - `소비하는 외부 계약자이다. M10 동반 PR T-483`
  - `소비하는 외부 계약서이다. M10 동반 PR T-483`
  - `소비하는 외부 계약주의다. M10 동반 PR T-483`
  - `소비되는 외부 계약자다. M10 동반 PR T-483`

- 영향: `소비하는 외부 계약`이라는 positive phrase를 포함하지만 계약자·계약서 등 다른 의미인 문장을 validator가 실제 외부 계약 assertion으로 오인한다. A-P1-01의 부정 corpus와 독립적으로, 부정어가 전혀 없어도 증명 조건을 우회한다.
- 권고: `소비하는|소비되는` 주체와 `외부 계약` 목적어를 구조적으로 파싱하고 허용 조사/서술어를 명시한다. `계약자`, `계약서`, `계약주의` 등 접미사·Unicode letter 경계를 반드시 거부하는 시험을 둔다.
- disposition: **OPEN / BLOCK**.

### A-P2-01 — task reference가 실제 파일명 뒤의 비정상 suffix를 허용

- 근거: `tools/openapi_exceptions.py:44`, 적용 `:477-480`. `_task_ids()` 자체는 `docs/tasks/T-*.md` 파일명에서 ID를 모으지만, reason 추출 regex는 ASCII 영숫자만 경계로 배제한다.
- 재현: 첫 reason의 `T-483`을 다음으로 치환하고 같은 candidate의 `load_registry`를 실행했다. 모든 변형이 **ACCEPT**였다.

  - `T-483_foo`, `T-483가`, `T-483.1`, `T-483-foo`, `T-483/extra`, `T-483:extra`

  실제 `T-483` 파일명이 존재하기 때문에 존재성 검사는 통과하지만, reason의 task reference가 정확한 ID token이라는 보장은 없다.
- 영향: malformed reference가 task provenance처럼 보이는 생성 표·evidence에 기록될 수 있다. 현재는 실제 ID가 prefix로 포함되어 P1보다 낮게 평가한다.
- 권고: task reference도 파일명에서 얻은 canonical ID와 완전 일치하는 token만 허용하고, underscore·Unicode letter·dot/suffix corpus를 reject한다.
- disposition: **OPEN / CONDITIONAL**.

### A-P2-02 — 최신 candidate 수치와 정본 상태 문서가 stale

- 근거:
  - `docs/resume.md:11`은 `T-301 post-fix-05 후보 준비 중`, focused 27, full 364, 문서 536/2583, redaction 687/0, commit `a8ea51f...`를 현재 상태처럼 표시한다.
  - `docs/tasks/T-301-openapi-standard.md:77`도 post-fix-05와 같은 수치를 실행 기록으로만 구분하지 않고 최신 closure로 남긴다.
  - `docs/journal.md:5-9`의 최신 항목도 post-fix-05와 27/364·536/2583·687/0을 기록한다.
- 대조: manifest `b5b9de...`와 candidate에서 재실행한 post-fix-06은 focused 28, full 365, links 539/2583, plan 106, SPDX 70, redaction/secret 690/0이다. candidate CI는 candidate SHA를 가리키는 두 성공 run이다.
- 영향: resume·task·journal을 읽는 다음 작업자와 merge 담당자가 현재 후보·검증 수치를 오인한다. immutable candidate와 문서 closure가 분리되어 이전 반복 no-go의 stale evidence 원인이 재발한다.
- 권고: candidate closure commit에 post-fix-06 commit/tree, manifest SHA, 실행 ID와 명령/exit를 함께 갱신하고, 이전 post-fix-05 수치는 역사 절로 명시한다. resume의 “다음 한 작업”은 현재 candidate와 일치시킨다.
- disposition: **OPEN / CONDITIONAL**.

## 닫힌 경계와 검증된 항목

- plain scalar 숫자·timestamp 공격 23종(`0xFF__00`, `0xFF_`, `0x__FF`, binary/octal, 반복·끝 underscore, float, sexagesimal, signed 값, short timezone)을 모두 REJECT했다.
- BOM 문서 시작 허용/중간 BOM 거부, Cc/Cf/Zl/Zp·surrogate, duplicate key, unsupported YAML, 7키·rule/date/sunset/alias·atomic output 경계는 focused 28개 시험과 `--check`에서 통과했다.
- renderer 직접 입력의 schema/updated/apps/exceptions/entry 의미 변이는 REJECT했다. Markdown injection(`<img>`, link, backtick, 개행)은 raw markup/표 행을 만들지 않고 escape 또는 안전한 단일 cell로 처리됐다.
- task 파일명 provenance 시험은 본문·요약에만 있는 미등록 ID를 거부했다. 다만 A-P2-01의 suffix 경계는 남았다.
- 소비자 저장소 build/e2e, npm/PyPI build·publish, GitHub Release, actionlint는 manifest 범위 밖이므로 `NOT_RUN(외부 선행/사용자 범위)`이다.

## 실행 명령과 결과

모든 명령은 candidate detached worktree에서 실행했다.

| 명령 | 결과 |
|---|---|
| `python -B -X utf8 tools/openapi_exceptions.py --check` | exit 0, `예외 39건·Markdown 54줄` |
| `python -B -X utf8 -m unittest discover -s tests -p 'test_openapi_exceptions.py' -v` | exit 0, 28 tests |
| `python -B -X utf8 -m unittest discover -s tests -p 'test_*.py' -v` | exit 0, 365 tests, 270.815초, OK |
| `python -B -X utf8 tools/validate_document_links.py` | exit 0, 539 documents / 2583 targets, errors 0 |
| `python -B -X utf8 tools/validate_plan.py` | exit 0, 상세 task 106, 오류 0 |
| `python -B -X utf8 tools/check_spdx.py --root .` | exit 0, 70 files, 오류 0 |
| `python -B -X utf8 tools/check_prod_redaction.py --all` | exit 0, 690 files, 발견 0 |
| `python -B -X utf8 tools/scan_secrets.py --all` | exit 0, 690 files, 발견 0 |
| `git diff --check base candidate` | exit 0 |
| `npm ci --ignore-scripts` | exit 0, Node `v25.9.0`/npm `11.12.1`; package engine `^22.12.0` 경고, 취약점 0 |
| `gh run list --commit d88f2a0446e114541f52de169630cd09e27f429a ...` | candidate SHA의 docs `34306605363` success, workflows selftest `34306605583` success |
| 최종 `git status --short --branch` (원본 report stage 전) | candidate 변경 없음; report branch 전환만 수행 |

`npm ci`의 Node engine 경고는 이 review 환경의 버전 차이이며 full unittest는 성공했다. 소비자 빌드·e2e와 외부 배포는 실행하지 않았고 통과로 집계하지 않았다.
