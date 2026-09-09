# T-301 post-fix-07 적대적 리뷰 A 원본

- Review ID: `T301-20260909-post-fix-07-A-20260909T131241+09:00`
- 판정: **BLOCK**
- 검토 방식: 상대 reviewer 결과와 통합 report를 읽지 않은 독립 검토. 후보 파일은 수정하지 않았다.

## 불변 입력과 격리 상태

- base commit: `afc8d1bf166d0ddcbee059252eb5cee245157dcd`
- base tree: `3eddd2ad90d10813bb37cd00f5ac9be5a1ef13ba`
- candidate commit: `1705a6a10954120b74e59d8611a520e7d9970605`
- candidate tree: `c724361a4eac4c2b3697431e0d9a2baeb74a62ce`
- manifest: `docs/reviews/adversarial/evidence/2026-09-09-t301-post-fix-07-manifest.md`
- manifest blob SHA-256: `601680c947297bca5b3dcf9bc9b5708fba75ab08a9d5b1ea80c357112e15aca8`
- manifest 보존 commit: `8d87af9880c4d13d82c109474b76fa7adb3067f5` (candidate의 docs-only 후속 commit)
- detached worktree: `F:\dev\kor-travel-common-wt\review-t301-post-a07`
- candidate checkout 직후 `git status --short --branch`: `## HEAD (no branch)`, 추가·수정 파일 없음.
- candidate tree에서 전체 검증을 마친 뒤 report branch로 전환했다. candidate 코드·정본 YAML·생성물은 수정하지 않았다.

## 판정 요약

| 등급 | ID | 결과 |
|---|---|---|
| P0 | — | 재현 finding 없음 |
| P1 | A-P1-01 | opener만으로 불완전한 긍정 assertion을 외부 계약 증명으로 ACCEPT — OPEN |
| P1 | A-P1-02 | 유효한 긍정 assertion 뒤의 부정·불확정 자연어가 ACCEPT — OPEN |
| P1 | A-P1-03 | combining mark가 붙은 M10·동반 PR token이 ACCEPT — OPEN |
| P1 | A-P1-04 | YAML 예약 sequence indicator 형태 `- foo`·`? foo`가 ACCEPT — OPEN |
| P2 | A-P2-01 | combining mark가 붙은 task ID suffix가 ACCEPT — OPEN |
| P2 | A-P2-02 | 새 회귀 시험이 앞 단계 검증에서 조기 거부되어 실제 경계를 시험하지 않음 — OPEN |
| P3 | — | 별도 재현 finding 없음 |

P1이 네 건 남아 있어 로컬·CI green과 무관하게 BLOCK이다.

## Finding

### A-P1-01 — 닫히지 않은 opener가 긍정 외부 계약 assertion을 대체함

- 근거: `tools/openapi_exceptions.py:65-70`, 적용 `:490-500`.
- `EXTERNAL_CONTRACT_RE`는 `계약` 뒤에 `(`, `[`, `{`, `<`, backtick 중 하나가 오면 바로 성공한다. opener의 짝·내용·문장 종결을 검증하지 않는다.
- 재현: 첫 S1의 reason을 다음으로 치환하고, 증명은 정상 standalone `M10`, task는 `T-483`만 남긴 뒤 `load_registry(..., as_of=date(2026, 9, 9))`를 실행했다. 모두 **ACCEPT**였다.

  - `소비하는 외부 계약[ M10 T-483`
  - `소비하는 외부 계약(foo M10 T-483`
  - `소비하는 외부 계약{foo M10 T-483`
  - `소비하는 외부 계약<foo M10 T-483`
  - `소비하는 외부 계약`foo M10 T-483`

- 영향: 정확한 긍정 assertion이 없는 malformed reason이 외부 계약 SHOULD 예외와 cross-repository 증명 조건을 통과한다. 현재 정본의 `계약(docs/...)` 표기를 허용해야 한다는 요구가 있더라도, 닫히지 않은 delimiter와 빈 opener는 별도 fail-closed 경계가 필요하다.
- 권고: opener 종류별 balanced syntax와 비어 있지 않은 citation/object를 파싱하거나, 허용할 정본 문법을 하나로 제한한다. opener만 있는 입력과 짝이 맞지 않는 입력을 회귀 시험에 추가한다.
- disposition: **OPEN / BLOCK**.

### A-P1-02 — 유효한 assertion 뒤의 부정·불확정 자연어가 fail-open

- 근거: `tools/openapi_exceptions.py:71-79`, 적용 `:490-495`.
- 이번에는 external assertion 자체가 유효하도록 `소비하는 외부 계약이다.`로 끝낸 뒤, 그 다음 문장에 부정·불확정 표현을 넣었다. 첫 S1의 다른 M10 근거를 제거하고 `M10 T-483`만 남겨 parser를 통과시키는 방식으로 격리했다.
- 다음 reason이 모두 **ACCEPT**였다.

  - `소비하는 외부 계약이다. 미 승인이다. M10 T-483`
  - `소비하는 외부 계약이다. 불확실하다. M10 T-483`
  - `소비하는 외부 계약이다. 불승인이다. M10 T-483`
  - `소비하는 외부 계약이다. 부적합이다. M10 T-483`
  - `소비하는 외부 계약이다. 거절이다. M10 T-483`
  - `소비하는 외부 계약이다. 무의미하다. M10 T-483`
  - `소비하는 외부 계약이다. notapplicable. M10 T-483`
  - `소비하는 외부 계약이다. not_applicable. M10 T-483`
  - `소비하는 외부 계약이다. no_contract. M10 T-483`
  - `소비하는 외부 계약이다. noncompliant. M10 T-483`
  - `소비하는 외부 계약이다. falsehood. M10 T-483`
  - `소비하는 외부 계약이다. none_value. M10 T-483`
  - `소비하는 외부 계약이다. neither_one. M10 T-483`
  - `소비하는 외부 계약이다. unsupported_status. M10 T-483`
  - `소비하는 외부 계약이다. non compliant. M10 T-483`

- 영향: validator가 reason 전체를 부정·불확정 증거로 fail-closed해야 하는 계약을 부분 어휘 목록의 빈틈으로 통과시킨다. 허위 SHOULD 예외가 생성 표와 소비자 매니페스트에 들어간다.
- 권고: 자연어 denylist를 계속 확장하기보다 reason을 구조화된 assertion과 별도 상태 필드로 분리한다. 기존 자유문자열을 유지해야 한다면 Unicode·공백·underscore를 포함한 합성어·활용형 corpus를 계속 fail-closed로 유지하고, 위 입력처럼 유효한 positive assertion 뒤의 문장도 검사한다.
- disposition: **OPEN / BLOCK**.

### A-P1-03 — combining mark가 exact evidence token 경계를 우회함

- 근거: `tools/openapi_exceptions.py:82-83`, 적용 `:499-500`. Python `\w`는 combining mark를 identifier 문자로 취급하지 않는다.
- 재현: 유효한 `소비하는 외부 계약이다.` 뒤에 아래 token을 하나만 넣고, 다른 동반 PR 근거는 제거했다. 모두 **ACCEPT**였다.

  - `M10\u0301foo`
  - `M10\uFE0Ffoo`
  - `동반 PR\u0301foo`
  - `동반 PR\uFE0Ffoo`

  이 값들은 화면상 토큰에 붙은 accent/variation selector가 뒤의 문자열을 감추는 형태이며 standalone `M10` 또는 standalone `동반 PR`이 아니다. 기존 `_`·한국어·dot·ASCII suffix 시험은 통과했지만 Unicode mark 경계는 다루지 않는다.
- 영향: invisible/combining Unicode를 이용해 실제 증명이 아닌 token을 조건에 맞는 것처럼 보이게 할 수 있다. M10 증명 위조는 S 예외 등록의 cross-repository coordination gate를 우회한다.
- 권고: 정규식 lookaround 대신 Unicode `L/N/M/connector`를 포함하는 scanner로 token을 추출하거나, token 주변의 모든 Unicode identifier/mark를 경계에서 배제한다. combining mark·variation selector를 반드시 reject하는 회귀 시험을 추가한다.
- disposition: **OPEN / BLOCK**.

### A-P1-04 — YAML 예약 sequence indicator 뒤의 공백 형태를 문자열로 수용

- 근거: `tools/openapi_exceptions.py:286-302`. 단독 `-`·`?`는 거부하지만 `- `·`? `로 시작하는 scalar는 거부하지 않는다.
- 재현: canonical YAML의 첫 `owner`를 unquoted `- foo`, `? foo`, `-  foo`, `?  foo`로 각각 치환하고 `load_registry`를 실행했다. 모두 **ACCEPT**되어 `owner`가 그대로 문자열로 들어갔다. 같은 방식으로 첫 S1의 `surface`를 `- foo` 또는 `? foo`로 바꿔도 registry가 **ACCEPT**됐다.
- 비교: standard YAML resolver(PyYAML `safe_load`)에서는 각각 sequence entry/mapping key indicator로 `ScannerError`가 발생한다. 이 도구는 PyYAML을 사용하지 않더라도 문서·코드가 말하는 YAML 부분집합에서 malformed reserved indicator를 fail-closed로 처리해야 한다.
- 영향: YAML 문법 오류가 정상 registry 값으로 변환된다. 특히 `surface`·`owner`는 별도 semantic restriction이 약해 malformed source가 생성 표와 downstream contract 입력으로 유입된다.
- 권고: plain scalar가 `-` 또는 `?` 다음 YAML whitespace로 시작하면 즉시 거부하고, reserved indicator 표를 code/test에 명시한다. mapping/sequence indicator를 직접 구현하기보다 지원 범위를 더 좁히는 것이 안전하다.
- disposition: **OPEN / BLOCK**.

### A-P2-01 — combining mark가 task ID standalone 경계를 우회함

- 근거: `tools/openapi_exceptions.py:44`, 적용 `:485-489`.
- 재현: 실제 파일명으로 존재하는 `T-483` 뒤에 `\u0301foo` 또는 `\uFE0Ffoo`를 붙인 `T-483\u0301foo`, `T-483\uFE0Ffoo`를 reason에 넣었다. 두 입력 모두 **ACCEPT**였다.
- 영향: 실제 파일명 provenance는 확인되지만 reason에는 standalone task ID가 아닌 malformed token이 남는다. P1 token 증명보다 직접 영향이 작아 P2로 판정한다.
- 권고: task ID scanner도 combining mark를 identifier suffix로 취급해 exact canonical ID만 허용한다.
- disposition: **OPEN / CONDITIONAL**.

### A-P2-02 — 새 회귀 시험의 여러 corpus가 앞 predicate에서 조기 거부됨

- 근거: `tests/test_openapi_exceptions.py:113-159`, `:167-212`와 현재 코드 `tools/openapi_exceptions.py:65-70`.
- 재현: 새 부정 시험 대부분은 `소비하는 외부 계약은 ...` 또는 `소비하는 외부 계약 — ...`을 사용한다. post-fix-07 assertion regex는 `계약` 뒤에 `이다`·`임`·opener만 허용하므로, 이 fixture는 `NEGATED_EVIDENCE_RE`에 도달하기 전에 external assertion predicate에서 거부된다. exact token 시험은 `계약. M10_foo`를 사용해 같은 이유로 거부되고, exact contract assertion 시험도 `계약자` suffix가 assertion predicate에서 먼저 거부된다.
- 실제 유효 assertion `소비하는 외부 계약이다.` 뒤의 A-P1-02·A-P1-03 corpus와 combining token은 ACCEPT되어 시험의 green 결과가 해당 경계를 증명하지 못함을 확인했다.
- 영향: 31개 focused test와 CI가 통과해도 부정 자연어·token scanner의 실제 fail-closed 동작을 보장하지 않는다. 이번 반복 no-go의 stale/부분 검증 원인을 회귀 시험 자체가 재현한다.
- 권고: 각 predicate를 통과하는 baseline reason을 만든 뒤 한 predicate만 변형하는 mutation test로 분리한다. `이다.` assertion을 고정하고 negative/token corpus를 실행하며, malformed opener/YAML indicator도 직접 입력 시험으로 추가한다.
- disposition: **OPEN / CONDITIONAL**.

## stale evidence 및 닫힌 경계 확인

- stale finding은 재현하지 않았다. `docs/resume.md:11`은 post-fix-07과 31/368·542/2584·693/0을 표시하고, `docs/tasks/T-301-openapi-standard.md:79`와 `docs/journal.md:5-9`도 post-fix-07 기능 commit·gate 수치를 기록한다.
- plain scalar 숫자·timestamp·`.inf`·`.nan`·YAML booleans·BOM 시작/중간·Cc/Cf/Zl/Zp·surrogate·duplicate key·7키·rule/date/sunset·alias·atomic output은 focused/full 및 별도 probe에서 기대대로 거부됐다.
- renderer 직접 입력의 schema/updated/apps/exceptions 의미 변이, Markdown markup escape, Unicode format control rejection은 focused 31개에서 통과했다.
- `M100`, `M10X`, underscore·한국어·dot/ASCII suffix와 task `_`·한국어·dot/`-`·`/`:` suffix는 새 시험에서 거부됐다. combining mark 경계만 A-P1-03/A-P2-01로 남았다.
- 소비자 저장소 export/build/e2e, npm pack/publish, PyPI build/publish, GitHub Release, actionlint는 manifest 범위 밖이므로 `NOT_RUN(외부 선행/사용자 범위)`이다.

## 실행 명령과 결과

모든 명령은 candidate detached worktree에서 실행했다.

| 명령 | 결과 |
|---|---|
| `python -B -X utf8 tools/openapi_exceptions.py --check` | exit 0, `예외 39건·Markdown 54줄` |
| `python -B -X utf8 -m unittest discover -s tests -p 'test_openapi_exceptions.py' -v` | exit 0, 31 tests, 3.970초 |
| `python -B -X utf8 -m unittest discover -s tests -p 'test_*.py' -v` | exit 0, 368 tests, 262.686초, OK |
| `python -B -X utf8 tools/validate_document_links.py` | exit 0, 542 documents / 2584 targets, errors 0 |
| `python -B -X utf8 tools/validate_plan.py` | exit 0, 상세 task 106, 오류 0 |
| `python -B -X utf8 tools/check_spdx.py --root .` | exit 0, 70 files, 오류 0 |
| `python -B -X utf8 tools/check_prod_redaction.py --all` | exit 0, 693 files, 발견 0 |
| `python -B -X utf8 tools/scan_secrets.py --all` | exit 0, 693 files, 발견 0 |
| `git diff --check afc8d1b..1705a6a` | exit 0 |
| `npm ci --ignore-scripts` | exit 0, Node `v25.9.0`/npm `11.12.1`; package engine `^22.12.0` 경고, 취약점 0 |
| `gh run list --commit 1705a6a10954120b74e59d8611a520e7d9970605 ...` | candidate SHA의 docs `34308915146` success, workflows selftest `34308915282` success |
| candidate checkout·전체 시험 후 `git status --short --branch` | report 작성 전까지 candidate 변경 없음 |

`npm ci`의 Node engine 경고는 review 환경의 버전 차이이며 full unittest는 성공했다. 외부 build/e2e·배포 검증은 실행하지 않았고 통과로 집계하지 않았다.
