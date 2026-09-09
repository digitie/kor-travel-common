<!-- SPDX-License-Identifier: GPL-3.0-or-later -->
<!-- SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie) -->

# T-301 post-fix-05 reviewer A 원본 적대적 리뷰

- 실행 ID: `T301-20260909-post-fix-05-A-20260909T1204+09:00`
- 검토일: `2026-09-09` (Asia/Seoul)
- reviewer: `/root/t010_review_a`
- verdict: **BLOCK**
- base commit: `afc8d1bf166d0ddcbee059252eb5cee245157dcd`
- base tree: `3eddd2ad90d10813bb37cd00f5ac9be5a1ef13ba`
- candidate commit: `62d3107967e5f7875024472fc91ded1ac5f7ba50`
- candidate tree: `4cc37b3574a552999e524101e426c4568d3bc3e0`
- manifest: `docs/reviews/adversarial/evidence/2026-09-09-t301-post-fix-05-manifest.md`
- manifest SHA-256: `03570ff162de9596ad8aa4704b670e99854d70a7eafa57351058355950055cc0`
- worktree: `F:\dev\kor-travel-common-wt\review-t301-post-a05`
- 관계: `git merge-base --is-ancestor afc8d1bf166d0ddcbee059252eb5cee245157dcd 62d3107967e5f7875024472fc91ded1ac5f7ba50` exit 0
- 시작 상태: 후보를 별도 detached clean worktree로 만들고 `git status --short`가 비어 있음을 확인했다.
- 후보 보호: 후보 소스·문서·시험 파일은 수정하지 않았다. 이 report만 review 완료 후 별도 evidence branch에 추가한다.
- 독립성: 이번 판정은 후보 전체 diff, 외부로 제공된 post-fix-05 manifest, 관련 코드·시험·정본 문서를 새로 읽고 직접 실행한 결과다. 상대 reviewer 원본과 통합 report는 판정에 사용하지 않았다.

## 판정 요약

정확한 global wildcard와 Markdown 구조 주입은 닫혔고, 문서 실행 수치도 현재 후보와 일치했다. 그러나 숫자 resolver의 반복·후행 underscore 변형과 SHOULD reason의 한국어·영어 부정 활용이 여전히 문자열로 수용된다. 두 P1 때문에 **BLOCK**이다.

| ID | 심각도 | 상태 | 영역 | 결과 |
|---|---:|---|---|---|
| A-P1-01 | P1 | OPEN | YAML 숫자 plain scalar | 반복·후행 underscore가 있는 int/float/sexagesimal 표기가 ACCEPT |
| A-P1-02 | P1 | OPEN | SHOULD 부정 근거 | `아닙니다`, `isn't`, `can't`, `non-contract`, `absent` 등이 ACCEPT |
| A-P2-01 | P2 | OPEN | renderer semantic top-level 계약 | 직접 전달한 잘못된 schema/apps/entry를 Markdown으로 생성 |
| A-P0-01 | P0 | — | 해당 없음 | 재현되지 않음 |
| A-P3-01 | P3 | — | 해당 없음 | 별도 잔여 P3 없음 |

## Finding A-P1-01 — 숫자 표기의 반복·후행 underscore 우회

- 위치: `tools/openapi_exceptions.py:46-56`의 `PLAIN_NONSTRING_RE`, `:281`의 plain scalar 판정.
- 재현: 임시 YAML에서 첫 `owner: kor-travel-geo`를 아래 값으로 치환하고 `load_registry(temp, as_of=date(2026, 9, 9))`를 실행했다. 후보 parser는 모든 값을 **ACCEPT**했다.

  ```text
  0xFF__00   0xFF_   0x__FF
  0b1__0     0b1_    0b__10
  1__000     1__     1._0
  1.0__0     1.0_    1__0.0
  1__0:20    1_:20   +0x__FF
  -0xFF_     -1__000 +1.0_
  ```

- 비교 근거: 같은 문자열을 PyYAML 6.0.3 YAML resolver에 넣으면 각각 int/float로 해석된다. 예를 들어 `0xFF__00`→`int 65280`, `1__000`→`int 1000`, `1._0`→`float 1.0`, `1__0:20`→`int 620`이다. PyYAML은 후보 runtime 의존성이 아니라 YAML resolver 의미를 확인하는 독립 reference로만 사용했다.
- 영향: 후보가 금지하려는 YAML numeric plain scalar의 일부 표기만 거부하고, underscore를 반복·끝에 둔 동일 계열을 문자열로 통과시킨다. 실제 YAML 해석기와 이 부분집합 parser의 타입 계약이 달라져 fail-closed 경계를 우회한다.
- 권고: YAML resolver가 허용하는 underscore grammar를 전부 거부하는 reject grammar를 두고 base prefix·decimal·float·sexagesimal 각 위치의 반복/후행 underscore를 회귀 시험에 추가한다. 허용 YAML dialect를 고정하고 그 resolver의 전체 표를 기준으로 시험해야 한다.

## Finding A-P1-02 — SHOULD reason의 부정 활용 우회

- 위치: `tools/openapi_exceptions.py:60-63`의 `NEGATED_EVIDENCE_RE`, `:474-484`의 S 예외 검증.
- 재현: 첫 S1 reason의 `소비하는 외부 계약이다.`를 다음 값으로 바꾸고 `load_registry()`를 실행했다. 모두 **ACCEPT**였다.

  ```text
  소비하는 외부 계약은 아닙니다. M10 동반 PR T-483.
  소비하는 외부 계약은 부정된다. M10 동반 PR T-483.
  소비하는 외부 계약이라는 주장은 거짓이다. M10 동반 PR T-483.
  소비하는 외부 계약 — isn't one; M10 동반 PR T-483.
  소비하는 외부 계약 — it isnt one; M10 동반 PR T-483.
  소비하는 외부 계약 — cannot be one; M10 동반 PR T-483.
  소비하는 외부 계약 — it can't be one; M10 동반 PR T-483.
  소비하는 외부 계약 — a non-contract; M10 동반 PR T-483.
  소비하는 외부 계약 — absent; M10 동반 PR T-483.
  소비하는 외부 계약 — absence of a contract; M10 동반 PR T-483.
  소비하는 외부 계약 — doesn't apply; M10 동반 PR T-483.
  ```

- 영향: 긍정 문구의 substring은 유지되지만 `아닙니다`의 `아닙` 활용, `부정된다`·`거짓이다`, 영어 contraction·`non-*`·`absent`는 현재 정규식에 없다. 실제로 계약이 없거나 부정된 reason을 긍정 외부 계약 증명처럼 등록할 수 있어 문서가 주장한 한국어·영어 fail-closed 정책을 우회한다.
- 권고: 자연어 부정 정규식의 누락 목록을 계속 확장하는 방식보다 긍정 근거를 구조화한 enum/필드로 바꾸고, reason에는 그 식별자와 task/동반 PR만 허용한다. 구조를 유지한다면 활용·contraction·`non-*`·부정 명사까지 회귀 corpus로 고정하고, 검증은 허용 목록 방식으로 닫아야 한다.

## Finding A-P2-01 — renderer는 안전하게 escape하지만 의미 계약은 직접 우회됨

- 위치: `tools/openapi_exceptions.py:530-575`.
- 확인한 수정: `schema`, `updated`, `apps`에 개행·heading·link·backtick을 넣어도 `_markdown_cell()`이 줄바꿈을 공백으로 바꾸고 Markdown 문자를 escape했다. `\n## injected`, `[x](https://evil)`, `` `tick` ``의 raw 구조는 출력되지 않았다. 이전 top-level Markdown injection은 **FIXED**로 disposition한다.
- 잔여 재현: `load_registry()` 결과를 복사해 다음 값만 직접 변조한 뒤 `render_markdown()`을 호출했다. 모두 **ACCEPT**했고 Markdown이 생성됐다.

  ```text
  registry["schema"] = "not-the-canonical-schema"
  registry["updated"] = "not-a-date"
  registry["apps"] = ["evil"]
  registry["exceptions"][0] = {
      "app": "evil", "rule": "BAD", "surface": "*", "reason": "fake",
      "sunset": None, "review": "not-date", "owner": "evil"
  }
  ```

  결과 예: schema 값은 `not-the-canonical-schema`로, entry 행은 `| evil | BAD | ... | not-date | evil |`로 생성됐다.
- 영향: 정상 `generate()`는 `load_registry()`를 먼저 호출하므로 canonical YAML 경로에서는 도달하지 않는다. 하지만 renderer의 “검증된 registry” 전제가 public dict 호출 경계에만 남아 있어, 직접 호출자나 향후 도구가 semantic-invalid top-level/entry를 읽기 전용 표로 확정할 수 있다. 이는 injection은 아니지만 renderer semantic contract의 방어 결함이다.
- 권고: renderer가 canonical schema/date/apps/entry key·rule·task·surface 계약을 다시 검증하거나, `load_registry()`가 반환하는 불변 typed value만 받도록 API를 좁힌다. 현재의 Markdown escaping은 유지해야 한다.

## 재현해 닫힘을 확인한 경계

- post-fix-04의 대표 numeric/base/sexagesimal/timezone 값 `0x_FF`, `0b_10`, `0o_10`, `1:2`, `1:2:3.4`, `2026-09-06T00:00:00.123+9:00`, `+0x_FF`는 현재 REJECT됐다. 반복·후행 underscore 변형만 위 P1로 잔류한다.
- S surface의 정확한 전역 wildcard `*`, `/*`, `/**`는 `GLOBAL_SURFACE_RE`에 의해 REJECT됐다. `/v2/**` 같은 비전역 경로 wildcard는 현재 문서의 “전역 wildcard” 정의 밖으로 구분했다.
- UTF-8 BOM은 문서 시작만 ACCEPT하고 내부 BOM은 REJECT했다. Cc/Cf/Zl/Zp·surrogate 입력은 REJECT됐다.
- task 본문에만 있는 ID는 REJECT되고, task ID 수집은 `docs/tasks/T-*.md` 파일명에서만 수행됐다. duplicate identity와 surface 양끝 공백도 REJECT됐다.
- focused regression 27개는 모두 통과했지만, 위 반복 underscore와 부정 활용·semantic-invalid renderer corpus는 기존 시험에 없다.

## 실행 결과

| 명령 | 결과 |
|---|---|
| `python -B -X utf8 tools/openapi_exceptions.py --check` | exit 0; 예외 39건·Markdown 54줄 |
| `python -B -X utf8 -m unittest discover -s tests -p 'test_openapi_exceptions.py' -v` | exit 0; 27 tests, OK |
| `npm ci --ignore-scripts` | exit 0; Node `v25.9.0`가 package engine `^22.12.0`과 달라 warning, 의존성 설치 완료 |
| `python -B -X utf8 -m unittest discover -s tests -p 'test_*.py' -v` | exit 0; 364 tests, OK |
| `python -B -X utf8 tools/validate_document_links.py` | exit 0; 536 documents, 2583 targets |
| `python -B -X utf8 tools/validate_plan.py` | exit 0; 상세 task 106, 오류 0 |
| `python -B -X utf8 tools/check_spdx.py --root .` | exit 0; 70개 파일, 오류 0 |
| `python -B -X utf8 tools/check_prod_redaction.py --all` | exit 0; 687개 파일, 발견 0 |
| `python -B -X utf8 tools/scan_secrets.py --all` | exit 0; 687개 파일, 발견 0 |
| `git diff --check afc8d1bf166d0ddcbee059252eb5cee245157dcd 62d3107967e5f7875024472fc91ded1ac5f7ba50` | exit 0 |

## 후보 SHA CI

후보 SHA로 직접 조회한 run만 evidence로 집계했다.

- [docs run 34304849979](https://github.com/digitie/kor-travel-common/actions/runs/34304849979): `headSha=62d3107967e5f7875024472fc91ded1ac5f7ba50`, completed/success.
- [workflows selftest run 34304850114](https://github.com/digitie/kor-travel-common/actions/runs/34304850114): `headSha=62d3107967e5f7875024472fc91ded1ac5f7ba50`, completed/success.

PR #22의 현재 화면에 보이는 별도 run은 head `6305bd50018a50929e575092cd9ddaec68fe07b8`였으므로 후보 evidence로 섞지 않았다. exact candidate SHA run만 판정에 사용했다.

## 실행하지 않은 gate

소비자 저장소 export/build/e2e, npm pack·publish·registry 검증, PyPI build·publish, GitHub Release, actionlint는 manifest 범위에 따라 `NOT_RUN(범위 밖)`이다. `npm ci`는 common full unittest의 MDX 의존성 설치에만 사용했다.

## 원본 보존

이 파일은 review 완료 후 `codex/t301-review-a-post-fix-05-evidence` branch에서 단독 추가·커밋한다. commit SHA와 report SHA-256은 최종 메시지로 전달한다.
