<!-- SPDX-License-Identifier: GPL-3.0-or-later -->
<!-- SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie) -->
# T-301 post-fix Reviewer A 원본 evidence

- Review ID: `T301-20260909-post-fix`
- 실행 ID: `T301-20260909-post-fix-A-20260909T110816+0900`
- 종류: 백엔드 계약·보안·fail-closed parser 독립 적대 리뷰
- 시작 시각: `2026-09-09T11:08:16+09:00`
- 종료 시각: `2026-09-09T11:10:17+09:00`
- candidate commit: `fedf7f8cbad55302183708aa4c9dd514ffba466d`
- candidate tree: `e40c59e99eb367fb79893587e7dbd7489a7d2ff8`
- base commit: `afc8d1bf166d0ddcbee059252eb5cee245157dcd`
- base tree: `3eddd2ad90d10813bb37cd00f5ac9be5a1ef13ba`
- manifest: `docs/reviews/adversarial/evidence/2026-09-09-t301-post-fix-manifest.md`
- manifest SHA256: `b04e93badcd6cb8b7aa0312e2eb998980aea02e6de3a35d582a424eb78d90c6e`
- 격리: `F:\dev\kor-travel-common-wt\review-t301-post-a`에서 candidate를 detached로 checkout한 뒤 기준선과 clean을 확인했다. 보고서 작성 때만 candidate에서 분기한 evidence branch에 이 파일을 추가했다.
- clean 확인: 시작 `git status --short` 출력 없음; focused·전체 시험 뒤에도 candidate worktree 출력 없음. evidence commit 후 branch clean을 다시 확인한다.
- 독립성: 상대 reviewer 결과와 통합 report는 열지 않았다. 이 파일은 candidate 코드·문서를 읽고 직접 재현한 결과만 기록한다.
- manifest의 파일 자체는 candidate commit에 들어 있지 않았고, 지정된 외부 입력 파일의 hash를 별도로 확인했다.

## 검토 범위와 결론

candidate와 base의 전체 delta, `tools/openapi_exceptions.py`, `tests/test_openapi_exceptions.py`, OpenAPI 정본·ADR-009/D-14 관련 문서, 예외 YAML과 생성 Markdown을 검토했다. malformed/duplicate/escape/date/expiry 입력, task provenance, SHOULD 외부 계약 표면, Markdown 출력, input/output alias와 atomic write 경계를 독립적으로 공격했다.

**최종 verdict: BLOCK**

P1 1건과 P2 2건이 열려 있다. P0은 확인하지 않았고, P3 신규 finding도 확인하지 않았다. P1은 `surface` 정규화·외부 계약 증명 검사가 문자열 우회로 fail-open 되는 문제다. P2는 Unicode 제어·방향 제어 문자가 생성 Markdown까지 통과하는 문제와 task evidence의 stale 수치다.

## Finding

### A-T301-post-P1-01 — SHOULD 외부 계약·앱 전체 표면 검사가 문자열 우회로 통과함

- 심각도: **P1**
- 위치: `tools/openapi_exceptions.py:444-450` (`surface == "*"`와 reason 부분 문자열 검사), 정본 규칙 `docs/standards/openapi.md:185,198`, YAML 안내 `docs/standards/openapi-exceptions.yaml:9`.
- 재현: canonical YAML의 첫 `geo/S1` 항목을 다음처럼 임시 변조했다.
  - `surface: "* "` (끝 공백으로 canonical `*` 비교를 우회)
  - `reason: "외부 계약 동반 PR 근거 없음. T-483."` (외부 계약·동반 PR 문자열만 포함하며 실제 계약 근거는 부정)
  - `python -B -X utf8 -`로 `load_registry(path, as_of=date(2026, 9, 9))`를 호출했을 때 **ACCEPTED: entries=39**, exit `0`이었다.
- 추가 재현: 정상 geo/S1 항목을 `surface: "/v2/* "`인 두 번째 S1 항목으로 복제하면 의미상 같은 표면인데도 `ACCEPTED entries=40`으로 통과하고 `['/v2/*', '/v2/* ']`를 보존했다.
- 영향: 정본은 S1~S13 예외를 외부 계약의 구체적 표면으로만 허용하고 앱 전체 `*` SHOULD 예외를 금지한다. 그러나 trailing whitespace·임의 문자열을 canonicalize하지 않고 reason의 단어 포함만 확인하므로, 승인되지 않은 전역 SHOULD 예외나 중복 surface가 registry·생성 표에 들어간다. 소비자가 이 표를 예외 허용 목록으로 복사하면 정책 검사가 fail-open 되고 audit 근거가 위조된다.
- 권고: `surface`를 문법적으로 파싱하고 양끝 공백·제어·빈 표면을 거부한 뒤 canonical 비교로 `*`를 차단한다. 동일 표면 identity도 canonical form으로 비교한다. 외부 계약·M10·task를 단순 substring으로 증명하지 말고 구조화한 증거 필드/허용된 contract reference와 task-owner 연계를 검증하거나, 최소한 문장 경계를 포함한 엄격한 형식과 회귀 시험을 추가한다.
- disposition: **OPEN — 수정 후 A/B 원 reviewer 재검토 필요**.

### A-T301-post-P2-02 — Unicode 제어·format 문자가 생성 Markdown에 남음

- 심각도: **P2**
- 위치: `tools/openapi_exceptions.py:68-76`의 `_validate_text`는 C0/DEL과 lone surrogate만 거부하고, `:477-491`의 `_markdown_cell`은 HTML/Markdown 문장부호만 escape한다.
- 재현: 임시 YAML의 첫 reason을 `"bad\\u0080value T-483"`, `"bad\\u2028value T-483"`, `"bad\\u2029value T-483"`, `"bad\\u202evalue T-483"`로 각각 바꿔 `load_registry`와 `render_markdown`을 실행했다. 네 경우 모두 **ACCEPT**했고 출력 Markdown에 해당 문자가 그대로 남았다(`output=True`; U+0080 UTF-8 bytes `c2 80`). U+200B·U+FEFF도 동일하게 통과했다.
- 영향: C1 control, Unicode line separator, bidi/zero-width/format 문자가 사람이 읽는 정본 표와 diff/review UI에 남아 행 경계·표시 방향·문자 존재를 숨길 수 있다. 기존 C0/NUL·surrogate hardening은 동작하지만, 생성 artifact의 audit 표시 안전성은 완결되지 않는다.
- 권고: decoded scalar와 output cell에서 `unicodedata.category`의 Cc/Cf 및 U+2028/U+2029·zero-width/bidi 범위를 명시적으로 거부하거나 안전한 표기로 치환하고, C1·line-separator·bidi 회귀 시험을 추가한다. 출력 시점에 우회되지 않도록 parser와 renderer 양쪽의 invariant를 확인한다.
- disposition: **OPEN — P2 수정 또는 명시적 disposition 필요**.

### A-T301-post-P2-03 — T-301 실행 evidence 수치가 현재 candidate와 stale

- 심각도: **P2**
- 위치: `docs/tasks/T-301-openapi-standard.md:73-75`, `docs/resume.md:11`, `docs/journal.md:7-9`.
- 재현: candidate에서 `python -B -X utf8 tools/openapi_exceptions.py --check`는 `예외 39건·Markdown 54줄`, focused 시험은 `Ran 20 tests ... OK`를 출력했다. task/journal에는 각각 `46건`, `Markdown 61줄`, `8 tests`가 확정 실행값으로 남아 있다.
- 영향: task 수용 근거와 resume/journal 정본 경로가 서로 다른 구현 단계의 수치를 가리킨다. stale 값을 완료 evidence로 사용하면 reviewer가 실제 후보의 검증 범위와 closure를 판정할 수 없고, AGENTS의 stale/미검증 값 금지와 T-301 실행 기록 요구를 위반한다.
- 권고: post-fix candidate의 실제 수치·명령·exit code·전체 시험의 의존성 미설치 사유를 task 실행 기록과 journal/resume에 동기화하고, closure commit 전까지 상태를 `IN_PROGRESS`로 유지한다.
- disposition: **OPEN — 문서 closure에서 수정 필요**.

## 기존 A finding 공격 클래스 재현

상대 결과를 읽지 않았으므로 B reviewer의 ID별 disposition은 판정하지 않는다. 본인이 이전에 검토했던 A 공격 클래스와 전체 delta를 독립적으로 재현한 결과는 다음과 같다.

| 공격 클래스 | 결과 |
|---|---|
| 미래 `updated` | `RegistryError(미래일 수 없음)`으로 거부. focused test 통과 |
| raw HTML/Markdown markup | `<img>`, link, backtick 등은 generated cell에서 escape. focused test 통과 |
| C0/DEL 및 lone surrogate | parser에서 거부. 단, P2-02의 C1/format 확장 경계는 남음 |
| input/output 동일 경로·hardlink alias | `RegistryError`로 거부. 기존 output 보존 atomic 시험 통과 |
| single-quote doubled escape와 comment scanner | 정상 decode 및 registry load 통과 |
| malformed/duplicate/unsupported YAML, unquoted number/date/time, expired/future 경계 | 모두 fail-closed 또는 날짜 계약 오류로 처리 |

## 검증 기록

### 기준선·격리

- `git rev-parse HEAD` → `fedf7f8cbad55302183708aa4c9dd514ffba466d`
- `git rev-parse 'HEAD^{tree}'` → `e40c59e99eb367fb79893587e7dbd7489a7d2ff8`
- base tree → `3eddd2ad90d10813bb37cd00f5ac9be5a1ef13ba`
- `git merge-base --is-ancestor afc8d1bf166d0ddcbee059252eb5cee245157dcd HEAD` → exit `0`
- 지정 manifest `Get-FileHash -Algorithm SHA256 ...` → `B04E93BADCD6CB8B7AA0312E2EB998980AEA02E6DE3A35D582A424EB78D90C6E`

### 실행 명령과 결과

| 명령 | 결과 |
|---|---|
| `python -B -X utf8 tools/openapi_exceptions.py --check` | exit `0`; 39건·Markdown 54줄 |
| `python -B -X utf8 -m unittest discover -s tests -p 'test_openapi_exceptions.py' -v` | exit `0`; 20 tests, skip 0 |
| `python -B -X utf8 tools/validate_document_links.py` | exit `0`; 527 documents, 2582 local targets, errors 0 |
| `python -B -X utf8 tools/validate_plan.py` | exit `0`; 106 상세 task, errors 0 |
| `python -B -X utf8 tools/check_spdx.py --root .` | exit `0`; 70 files, errors 0 |
| `python -B -X utf8 tools/check_prod_redaction.py --base afc8d1bf166d0ddcbee059252eb5cee245157dcd` | exit `0`; 16 files, 0 findings |
| `python -B -X utf8 tools/scan_secrets.py --base afc8d1bf166d0ddcbee059252eb5cee245157dcd` | exit `0`; 16 files, 0 findings |
| `git diff --check afc8d1bf166d0ddcbee059252eb5cee245157dcd HEAD` | exit `0` |
| 전체 `python -B -X utf8 -m unittest discover -s tests -p 'test_*.py' -v` | exit `1`; 357 tests 중 38 failures·3 errors. 모두 `ux_lint` MDX parser가 없어 `npm ci` 필요하다는 환경 오류로 발생. T-301 focused 판정에 사용하지 않음 |
| S surface/Unicode 임시 변조 focused scripts (`python -B -X utf8 -`) | exit `0`; 위 P1/P2 재현 |

### 범위 밖

7개 소비자 저장소 build/e2e, npm/PyPI 게시, GitHub Release, 원격 CI 재실행과 `actionlint`는 manifest에 따라 `NOT_RUN(이 common review 범위 밖)`이다. 전체 unittest의 MDX parser 의존성도 설치하지 않았으므로 해당 범위는 `NOT_RUN(설치 선행 없음)`으로 별도 기록한다.

## 최종 판정

- verdict: **BLOCK**
- P0: 0
- P1: 1 (`A-T301-post-P1-01`)
- P2: 2 (`A-T301-post-P2-02`, `A-T301-post-P2-03`)
- P3: 0 신규
- 남은 불확실성: 상대 reviewer 결과는 독립성 때문에 읽지 않았으며 B finding ID별 closure는 통합 report에서 두 원본을 대조해야 한다. consumer build/e2e·release는 실행하지 않았다.
- 원본 파일: `docs/reviews/adversarial/evidence/2026-09-09-t301-reviewer-a-post-fix.md`
