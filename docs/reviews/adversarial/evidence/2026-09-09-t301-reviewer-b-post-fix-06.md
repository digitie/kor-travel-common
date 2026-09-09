# T-301 post-fix-06 B 원본 적대 리뷰

- Review ID: `T301-20260909-post-fix-06`
- 실행 ID: `T301-20260909-post-fix-06-B-20260909`
- 리뷰어: B — 문서·계약·parser·renderer·재현성
- 시작: 2026-09-09 (세션 시작 시각은 이전 진행분으로 정확히 기록되지 않음, Asia/Seoul)
- 종료: 2026-09-09T12:39:49+09:00
- 기준선(base): `afc8d1bf166d0ddcbee059252eb5cee245157dcd`
- 후보(commit): `d88f2a0446e114541f52de169630cd09e27f429a`
- 후보 tree: `6702e7f844bf3e3f9112a007351f0183632496a3`
- 입력 manifest: `docs/reviews/adversarial/evidence/2026-09-09-t301-post-fix-06-manifest.md`
- manifest SHA-256: `b5b9decc76cecba0e84d7a987443f0549df90174e00ac8d2dd85beb8865d108d`
- 격리: `F:/dev/kor-travel-common-review-b-t301-postfix02`의 detached worktree
- 상대 reviewer 결과와 통합 report: 읽지 않음
- 후보 파일 수정: 없음

## 범위와 판정

후보 전체 diff와 `docs/standards/openapi.md`, ADR-009/D-14, T-301 계약, `tools/openapi_exceptions.py`, 생성 Markdown/YAML, 회귀 시험, 후보 실행 evidence를 확인했다. 외부 소비자 저장소 build/e2e, npm/PyPI build·publish, GitHub Release, actionlint는 manifest가 정한 common 범위 밖이므로 `NOT_RUN(외부 저장소·게시 범위 밖)`이다.

최종 verdict는 **BLOCK**이다.

- P0: 0건
- P1: 1건
- P2: 4건
- P3: 0건

P1이 해결되고 P2가 수정 또는 owner·task·gate·기한이 있는 명시적 disposition으로 연결되기 전에는 merge할 수 없다.

## 기준선·clean 확인

다음 결과로 후보 object/tree와 detached 상태를 확인했다.

```text
git rev-parse HEAD
d88f2a0446e114541f52de169630cd09e27f429a

git rev-parse 'HEAD^{tree}'
6702e7f844bf3e3f9112a007351f0183632496a3

git status --porcelain=v1 --branch
## HEAD (no branch)
```

manifest 파일은 제공된 외부 입력 파일에서 SHA-256 `b5b9decc76cecba0e84d7a987443f0549df90174e00ac8d2dd85beb8865d108d`로 확인했다. 후보 commit 자체에는 post-fix-06 manifest가 아직 들어 있지 않으므로, 이 리뷰의 manifest는 전달된 immutable 입력으로 취급했다.

## 실행한 검증

| 명령 | 결과 |
|---|---|
| `python -B -X utf8 tools/openapi_exceptions.py --check` | exit 0; 예외 39건·Markdown 54줄 |
| `python -B -X utf8 -m unittest discover -s tests -p 'test_openapi_exceptions.py' -v` | exit 0; 28 tests OK |
| `python -B -X utf8 -m unittest discover -s tests -p 'test_*.py' -q` | exit 0; 365 tests OK, 228.570초 |
| `python -B -X utf8 tools/validate_document_links.py .` | exit 0; 539 documents·2583 local targets, errors=0 |
| `python -B -X utf8 tools/validate_plan.py --root .` | exit 0; 상세 task 106, 오류 0 |
| `python -B -X utf8 tools/check_spdx.py --root .` | exit 0; 70 files, 오류 0 |
| `python -B -X utf8 tools/check_prod_redaction.py --root . --patterns .prod-redaction-patterns --all` | exit 0; 690 files, 발견 0 |
| `python -B -X utf8 tools/scan_secrets.py --root . --patterns .secret-scan-patterns --all` | exit 0; 690 files, 발견 0 |
| `git diff --check afc8d1bf166d0ddcbee059252eb5cee245157dcd d88f2a0446e114541f52de169630cd09e27f429a --` | exit 0 |
| `gh run list --repo digitie/kor-travel-common --commit d88f2a0446e114541f52de169630cd09e27f429a` | docs `34306605363` success, selftest `34306605583` success |
| candidate check-runs | 12개 모두 candidate SHA 일치·completed·success |

## 공격 시나리오와 통과한 경계

- PyYAML type oracle와 후보 parser를 비교해 숫자·base prefix·float·sexagesimal·날짜·timestamp가 non-string으로 해석되는 경우 후보가 모두 거부되는지 확인했다. 확인한 값에서 non-string 수용 mismatch는 0건이었다.
- `0x_FF`, `0o_10`, `0b_10`, signed/short sexagesimal, short timezone timestamp, fractional timestamp는 거부됐다.
- exact global surface `*`, `/*`, `/**`와 `M100`, `M10X`, `미동반 PR`, `동반 PRX` 증명 토큰은 거부됐다.
- BOM은 문서 시작에서만 허용되고, 내부 BOM 및 Cc/Cf/Zl/Zp 문자는 focused 시험에서 거부됐다.
- task ID가 상세 task 파일명에 없는 `T-034` 참조는 거부됐다.
- renderer에 schema·updated·apps·exceptions를 직접 변조해 넣은 네 가지 경우 모두 `RegistryError`로 거부됐다.

## Findings

### B-P1-01 — 현재 task/resume/journal evidence가 post-fix-05로 stale

- 심각도: **P1**
- disposition: **OPEN**
- 위치:
  - `docs/tasks/T-301-openapi-standard.md:77`
  - `docs/resume.md:11`
  - `docs/journal.md:5-9`
- 근거:
  - 후보 manifest가 현재 후보의 focused 28, full 365, links 539/2583, SPDX 70, redaction/secret 690/0을 선언하고 실제 후보에서 같은 수치를 재현했다.
  - 그러나 T-301 task는 focused 27, full 364, links 536/2583, redaction/secret 687/0을 post-fix-05 현재 실행처럼 기록한다.
  - resume은 “T-301 post-fix-05 후보 준비 중”과 full 364를 현재 다음 작업으로 표시한다.
  - journal의 최신 T-301 항목도 post-fix-05 수치를 현재 candidate evidence로 서술한다.
- 재현:
  1. 위 세 파일을 `rg -n "post-fix-05|364|27개|536/2583|687/0"`로 검색하면 모두 이전 후보 수치가 최신 상태 문맥에 남는다.
  2. 후보에서 위 표의 기준 명령을 실행하면 28/365, 539/2583, 690/0이 나온다.
  3. 따라서 문서 정본과 candidate 실행 결과가 서로 다른 SHA/수치를 가리킨다.
- 영향: merge 담당자와 후속 agent가 T-301의 최신 실행 결과와 review 대상을 잘못 판단한다. stale evidence를 현재 정상값처럼 남기지 말라는 작업 규칙과, review/task/PR의 감사 가능한 immutable 기준선 계약을 깨며, 이번 반복 review의 핵심 gate를 통과한 것으로 오인하게 만든다.
- 권고: post-fix-06 candidate SHA/tree, manifest SHA, 실제 명령·exit code·CI run `34306605363`/`34306605583`, 28/365·539/2583·690/0 수치를 T-301 실행 기록·resume·journal의 최신 항목에 추가한다. 이전 post-fix-05 문단은 역사 기록으로 명시하고 현재 상태 문장과 분리한다. 수정 후 task/resume/journal을 같은 closure commit에 묶어 문서 gate를 재실행해야 한다.

### B-P2-01 — M10·동반 PR 증명 토큰의 underscore 경계 우회

- 심각도: **P2**
- disposition: **OPEN**
- 위치: `tools/openapi_exceptions.py:74-75`, 검증 사용부 `:491`
- 근거: `M10_EVIDENCE_RE`와 `COORDINATED_PR_EVIDENCE_RE`의 lookaround가 ASCII 영숫자만 제외한다. `_`는 identifier continuation인데 경계로 취급된다.
- 재현:
  - canonical S1 reason에서 기존의 정상적인 M10/동반 PR 문구를 제거하고 증명만 각각 `M10_foo`, `동반 PR_foo`로 바꿔 `load_registry(...)`를 실행했다.
  - 결과:
    ```text
    M10_foo => ACCEPT
    동반 PR_foo => ACCEPT
    ```
  - `M100`, `M10X`, `동반 PRX`는 REJECT되어 현재 시험이 underscore 경계를 덮지 못한다.
- 영향: 자유 문자열 reason의 식별자·오타가 exact M10 또는 exact “동반 PR” 증명처럼 인정된다. 외부 계약 SHOULD 예외의 교차 저장소 동반 변경 증거를 위조하거나 누락할 수 있다.
- 권고: exact token grammar를 구조화된 필드로 분리하거나, 최소한 ASCII identifier continuation(`[A-Za-z0-9_]`)을 양쪽 경계에서 차단하고 underscore·하이픈·punctuation 정책을 시험으로 고정한다.

### B-P2-02 — 자연어 부정 evidence 어휘의 미포괄로 positive phrase를 우회

- 심각도: **P2**
- disposition: **OPEN**
- 위치: `tools/openapi_exceptions.py:66-71`, 검증 사용부 `:484-487`; 정본 요구 `docs/standards/openapi.md:198`
- 근거: validator는 positive substring `소비하는 외부 계약`/ `소비되는 외부 계약`과 제한된 `NEGATED_EVIDENCE_RE` 목록을 자유 문자열에서 검색한다. 목록에 없는 부정형은 문장 의미를 반대로 만들어도 통과한다.
- 재현:
  - 정상 S1 문장에서 기존 동반 증명을 제거하고 reason을 `소비하는 외부 계약이 {부정어}이다. M10 동반 PR T-483`로 주입했다.
  - 다음 값이 모두 `ACCEPT`였다: `불채택`, `미적용`, `아닐 수 있다`, `false`, `invalid`, `noncontract`.
  - 이미 목록에 있는 `미채택`, `거짓`, `not` 계열은 거부되지만, 목록 증량 방식의 음성 범위가 닫혀 있지 않다.
- 영향: “부정 표현은 허용하지 않는다”는 정본 계약을 자연어 동의어·활용형·영어 변형 하나로 우회할 수 있다. 유효하지 않은 외부 계약 예외와 동반 PR 증명이 레지스트리에 들어간다.
- 권고: 부정어 목록을 계속 확장하는 대신 `external_contract: true`와 검증 가능한 표면·소비자·동반 PR ID를 구조화하고, reason은 설명용으로만 사용한다. 구조화 전에는 허용 문장 grammar/allowlist를 명시하고 누락·동의어·활용형 회귀 시험을 추가한다.

### B-P2-03 — YAML 예약 indicator를 plain string으로 조용히 수용

- 심각도: **P2**
- disposition: **OPEN**
- 위치: `tools/openapi_exceptions.py:278-294`; 모듈 계약 `:6-10`
- 근거: 도구 docstring은 지원하지 않는 YAML 문법을 입력 오류로 닫는다고 선언하지만 `_scalar`는 `@`, backtick, 단독 `-`, 단독 `?`를 예약/구조 indicator로 거부하지 않는다.
- 재현:
  - canonical YAML의 첫 `owner: kor-travel-geo`를 각각 `owner: @`, `owner: \``, `owner: -`, `owner: ?`로 바꿔 `load_registry(..., as_of=date(2026,9,9))`를 실행했다.
  - 네 입력 모두 `ACCEPT`이고 owner가 해당 문자열로 반환됐다.
  - PyYAML의 동일 plain mapping(`owner: @` 등)은 YAML scanner error로 처리되는 입력이다.
- 영향: custom parser와 표준 YAML resolver 사이의 입력 의미가 달라지고, 잘못된 YAML을 정상 registry로 저장할 수 있다. 이후 다른 YAML 도구나 소비자가 같은 파일을 읽을 때 parse failure/의미 차이가 발생해 재현성과 fail-closed 계약이 깨진다.
- 권고: plain scalar 시작 indicator의 YAML 문법을 명시적으로 구현해 `-?` 단독/공백형, `@`, backtick 및 지원하지 않는 reserved indicator를 모두 거부하고, PyYAML oracle 기반 음성 시험을 추가한다.

### B-P2-04 — task reference도 underscore 연속 문자를 exact ID로 인정

- 심각도: **P2**
- disposition: **OPEN**
- 위치: `tools/openapi_exceptions.py:44`, 검증 사용부 `:477`
- 근거: `TASK_REFERENCE_RE`도 lookaround에서 ASCII 영숫자만 제외한다. 상세 task 파일명 provenance 자체는 확인하지만, reason 문장 안에서 exact task token의 경계는 닫혀 있지 않다.
- 재현:
  - 파일명에서 실제로 존재하는 모든 `T-NNN` 참조에 `_foo`를 붙여 `T-NNN_foo`로 만든 registry를 load했다.
  - 결과는 `ACCEPT`였다. 동일 방식으로 `x`를 붙이면 정의되지 않은 task ID로 REJECT되어 현재 경계가 ASCII 영숫자에만 의존함을 확인했다.
- 영향: 사람이 읽는 evidence가 standalone task ID가 아닌 identifier-like 문자열이어도 provenance 검사를 통과한다. task 링크 자동화·감사 도구가 exact ID를 추출할 때 validator와 서로 다른 결과를 낼 수 있다.
- 권고: task reference를 별도 목록/필드로 파싱하거나 underscore를 포함한 identifier continuation을 경계에서 차단하고, 한국어 조사와 punctuation을 허용할지 명시적인 grammar로 고정한다.

## 결론

코드·문서 전체의 정상 수치와 CI는 재현됐고 renderer semantic mutation, BOM/Unicode, numeric/timestamp, exact wildcard와 기본 task filename provenance의 음성 경계도 통과했다. 그러나 현재 task/resume/journal의 stale evidence가 P1이며, M10/동반 PR·부정 자연어·YAML reserved scalar·task token에 재현 가능한 P2가 남아 있다. 따라서 이 독립 B 리뷰의 verdict는 **BLOCK**이다.
