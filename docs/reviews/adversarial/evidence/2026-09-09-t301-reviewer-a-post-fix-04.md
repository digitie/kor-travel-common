<!-- SPDX-License-Identifier: GPL-3.0-or-later -->
<!-- SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie) -->

# T-301 post-fix-04 reviewer A 원본 적대적 리뷰

- 실행 ID: `T301-20260909-post-fix-04-A-20260909T1138+09:00`
- 검토일: `2026-09-09` (Asia/Seoul)
- reviewer: `/root/t010_review_a`
- verdict: **BLOCK**
- 기준선: base commit `afc8d1bf166d0ddcbee059252eb5cee245157dcd`, tree `3eddd2ad90d10813bb37cd00f5ac9be5a1ef13ba`
- 후보: commit `59a0fbc3ae426ec7a166ac34cbacbf2f9d6eaec5`, tree `15c3f3c90f881f4454caa18e24df603c4af52bf5`
- 관계: `git merge-base --is-ancestor afc8d1bf166d0ddcbee059252eb5cee245157dcd 59a0fbc3ae426ec7a166ac34cbacbf2f9d6eaec5` exit 0
- manifest: `docs/reviews/adversarial/evidence/2026-09-09-t301-post-fix-04-manifest.md`, SHA-256 `59bc91d26dbb364644f2c358d387408855f4e749484baba4b656b6fba9ef4547`
- worktree: `F:\dev\kor-travel-common-wt\review-t301-post-a04`
- 시작 상태: 후보를 detached clean worktree로 checkout했으며 `git status --short` 출력이 비어 있었다.
- 종료 상태: 후보 코드는 수정하지 않았고, 이 원본 report만 별도 evidence branch에 추가했다. report commit 이후 worktree도 clean으로 확인한다.
- 독립성: 후보 전체 diff와 `tools/openapi_exceptions.py`, 회귀 시험, 정본 문서와 manifest만 검토했다. 상대 reviewer 원본과 통합 판정은 판정 근거로 사용하지 않았다.

## 판정 요약

P0은 없다. P1 두 건이 아직 입력 검증을 우회해 **BLOCK**이다. P2 두 건도 기록한다. 숫자·timestamp와 SHOULD 예외의 정상 경계 시험은 통과하지만, 아래 추가 입력은 여전히 문자열로 받아들여지거나 부정 근거를 숨길 수 있다.

| ID | 심각도 | 상태 | 영역 | 핵심 근거 |
|---|---:|---|---|---|
| A-P1-01 | P1 | OPEN | YAML plain scalar fail-closed | `0x_FF`, `0b_10`, `0o_10`, `2026-09-06T00:00:00.123+9:00`가 `load_registry()`에서 ACCEPT |
| A-P1-02 | P1 | OPEN | SHOULD 근거 부정문 | `아니지만`·`아닌`·문장부호 뒤 `아니다`·`없다`가 있는 reason이 ACCEPT |
| A-P2-01 | P2 | OPEN | Markdown renderer 경계 | `render_markdown()`에 직접 변조한 `apps`를 주면 개행과 heading이 출력됨 |
| A-P2-02 | P2 | OPEN | 최신 실행 evidence | 문서는 full 362·문서 532·redaction/secret 683을 말하지만 현재 후보는 363·533·684 |
| A-P0-01 | P0 | — | 해당 없음 | 재현되지 않음 |
| A-P3-01 | P3 | — | 해당 없음 | 별도 잔여 P3 없음 |

## Finding A-P1-01 — 숫자·timestamp plain scalar의 표기 변형 우회

- 위치: `tools/openapi_exceptions.py:46-59`의 `PLAIN_NONSTRING_RE`, `:278-280`의 `_scalar()` 판정.
- 재현: 임시 YAML에서 첫 `owner: kor-travel-geo`를 `owner: <token>`으로 치환하고 `load_registry(temp, as_of=date(2026, 9, 9))`를 호출했다.
- 결과:

  ```text
  0x_FF                                      ACCEPT
  0xFF_00                                    REJECT
  0o_10                                      ACCEPT
  0b_10                                      ACCEPT
  1:20                                       REJECT
  1:20:30                                    REJECT
  2026-09-06T00:00:00+09                    REJECT
  2026-09-06T00:00:00+09:00                 REJECT
  2026-09-06T00:00:00.123+9:00              ACCEPT
  2026-09-06 00:00:00 +09:00                REJECT
  2026-09-06T00:00:00Z                       REJECT
  ```

- 영향: 부분집합 parser가 문자열로 남겨 둔 값이 YAML 구현의 숫자·timestamp scalar 해석과 달라진다. 특히 base prefix 직후 underscore와 한 자리 timezone offset을 이용하면 manifest가 요구한 “모든 YAML numeric/timestamp plain scalar 거부”를 우회한다. 레지스트리 계약의 fail-closed 경계가 입력 표기에 따라 달라진다.
- 권고: base prefix 직후 underscore를 포함한 숫자 변형과 timezone offset 표기를 명시적으로 모두 거부하는 표준 resolver/완전한 reject grammar를 사용하고, 각 변형을 회귀 시험에 추가한다. 허용할 YAML 버전을 정한다면 그 버전의 resolver와 동일한 표를 고정해야 한다.

## Finding A-P1-02 — SHOULD reason의 부정문 우회

- 위치: `tools/openapi_exceptions.py:60-61`의 `EXTERNAL_CONTRACT_RE`·`NEGATED_EVIDENCE_RE`, `:471-481`의 S 예외 검증.
- 재현: 첫 S1 reason의 `소비하는 외부 계약이다.`를 다음 값으로 각각 바꾸고 같은 `load_registry()`를 호출했다. 네 경우 모두 ACCEPT였다.

  ```text
  소비하는 외부 계약은 아니지만 동반 PR 근거 T-483.
  소비하는 외부 계약이 아닌 문자열이다. 동반 PR 근거 T-483.
  소비하는 외부 계약이다; 그러나 외부 계약이 아니다. 동반 PR T-483.
  소비하는 외부 계약이 없다. 동반 PR T-483.
  ```

- 영향: `EXTERNAL_CONTRACT_RE`가 긍정 문구의 부분 문자열만 확인하고, 부정 정규식은 `없음|아님|미확인|불가`만 특정 문맥에서 찾는다. 따라서 계약이 없다는 문장을 긍정 근거처럼 등록할 수 있어 SHOULD 예외의 핵심 정책이 fail-open이다.
- 권고: 자연어 substring 판정 대신 긍정 근거를 구조화한 필드/허용 enum으로 옮기거나, 부정 접속·활용·문장부호 경계를 포함하는 fail-closed grammar를 정의하고 광범위한 한국어 변형을 회귀 시험으로 고정한다.

## Finding A-P2-01 — renderer의 직접 입력 경계에서 Markdown 주입

- 위치: `tools/openapi_exceptions.py:527-540`, 특히 `:539`의 `registry['apps']` 직접 보간.
- 재현:

  ```python
  registry = load_registry(Path("docs/standards/openapi-exceptions.yaml"))
  registry["apps"][0] = "bad\n\n## injected"
  output = render_markdown(registry)
  ```

  함수는 예외 없이 반환했고 출력은 다음과 같았다.

  ```text
  9:'- apps: `bad'
  10:''
  11:'## injected`, `concierge`, `ktdm`, `geo`, `map`, `weather`, `pinvi`'
  ```

- 영향: 정상 CLI 흐름에서는 `load_registry()`가 고정 앱 목록을 검사하므로 바로 도달하지 않지만, 공개 함수에 검증된 dict라는 전제만 둔 직접 호출·향후 도구 변경·시험 fixture가 Markdown 구조를 주입할 수 있다. renderer가 모든 출력 필드를 안전하게 만들지 않는다는 경계 결함이다.
- 권고: renderer 안에서 전체 registry 계약을 다시 검증하거나, schema·updated·apps를 `_markdown_cell()`과 동일한 출력 경계로 검증/escape하고 typed immutable 결과만 받는다. 전제 조건을 유지할 경우 호출 계약과 회귀 시험을 명시하되, 현재처럼 raw interpolation을 두지 않는다.

## Finding A-P2-02 — post-fix-04 최신 evidence가 없음

- 위치: `docs/tasks/T-301-openapi-standard.md:76`, `docs/resume.md:11`.
- 문서 주장: focused 26, full unittest 362, 문서 `532/2583`, plan 106, SPDX 70, redaction/secret `683/0`, 기능 후보는 post-fix-03 `36509d3...`.
- 현재 후보에서 직접 재실행한 결과:

  ```text
  tools/openapi_exceptions.py --check       exit 0; 예외 39건·Markdown 54줄
  test_openapi_exceptions.py                exit 0; Ran 26 tests; OK
  unittest discover test_*.py               exit 0; Ran 363 tests; OK
  validate_document_links.py                exit 0; 533 documents, 2583 local targets
  validate_plan.py                          exit 0; 상세 task=106, 오류=0
  check_spdx.py --root .                    exit 0; 70개 파일, 오류 0개
  check_prod_redaction.py --all             exit 0; 684개 파일, 발견 0건
  scan_secrets.py --all                     exit 0; 684개 파일, 발견 0건
  git diff --check base candidate            exit 0
  ```

  전체 unittest는 처음에는 `node_modules`가 없어 MDX 관련 38 failures/3 errors가 났다. manifest의 로컬 의존성 조건을 충족하기 위해 detached worktree에서 `npm ci --ignore-scripts`를 exit 0으로 실행한 뒤 같은 명령을 다시 실행해 363 tests/OK를 확인했다. npm은 Node `v25.9.0`이 package engine `^22.12.0`과 다르다는 warning을 냈으므로 지원 runtime 검증은 별도 확인이 필요하다.

- 영향: 문서가 가리키는 최신 기능 후보·실행 수치와 현재 docs-only candidate의 실제 tree가 다르다. review closure가 362/532/683을 현재 후보의 evidence처럼 제시해 재현성과 감사 추적을 깨뜨린다.
- 권고: post-fix-04 candidate/tree와 manifest를 task·resume에 추가하고 현재 수치 363/533/684를 반영하거나, 과거 post-fix-03 수치라는 표기를 더 명확히 분리한다. 지원 Node runtime에서의 full 결과와 CI run도 같은 immutable candidate에 연결해야 한다.

## 닫힌 것으로 확인한 경계

- UTF-8 BOM은 문서 첫 위치만 ACCEPT하고 newline 이후·주석 내부·선행 공백·문서 끝 BOM은 `registry에 제어·format 문자가 있음`으로 REJECT했다.
- U+0080(Cc), U+202E(Cf), U+2028/Zl, U+2029(Zp), zero-width/format 입력은 parser에서 REJECT했다.
- task 본문에만 둔 `T-034`는 `정의되지 않은 task ID`로 REJECT했고, `_task_ids()`는 `docs/tasks/T-*.md` 파일명만 수집한다.
- duplicate identity `('geo', 'M3', '/v1/*')`는 REJECT했고, surface 양끝 공백도 REJECT했다.
- canonical registry `--check`, focused 26 tests, full 363 tests는 모두 exit 0이다. 이는 위 P1 우회 입력을 시험하지 않는 기존 regression suite의 성공이며, P1을 해소하지 않는다.

## 실행 범위와 미실행 gate

- 실행: 후보/base/tree/ancestry 확인, focused/full unittest, registry check, document link/plan/SPDX/redaction/secret gate, `git diff --check`, 위 malformed/duplicate/BOM/Unicode/task provenance/SHOULD/renderer adversarial probes.
- `npm ci --ignore-scripts`는 로컬 MDX 의존성 설치에만 사용했다. npm pack/publish/registry 검증은 하지 않았다.
- 소비자 저장소 build/e2e, npm pack·publish, PyPI build/publish, GitHub Release, actionlint, 외부 CI exact run 확인은 `NOT_RUN`이다. 이 review는 common 후보의 로컬 계약만 판정한다.

## 원본 보존

후보 파일은 수정하지 않았다. 이 문서는 review 완료 뒤 별도 branch `codex/t301-review-a-post-fix-04-evidence`에서 추가·커밋하며, 커밋 SHA와 이 파일 SHA-256은 최종 메시지로 전달한다.
