# T-301 독립 적대적 리뷰 B — post-fix-04

- 실행 ID: `T301-20260909-post-fix-04-B`
- 리뷰 종류: post-fix-04 독립 적대적 리뷰 B (문서·계약·parser·재현성)
- 실행 시각: 2026-09-09 11:37 KST 시작 확인 후 명령 실행
- 입력 manifest: `docs/reviews/adversarial/evidence/2026-09-09-t301-post-fix-04-manifest.md`
- manifest SHA-256: `59bc91d26dbb364644f2c358d387408855f4e749484baba4b656b6fba9ef4547`
- base: `afc8d1bf166d0ddcbee059252eb5cee245157dcd`
- candidate: `59a0fbc3ae426ec7a166ac34cbacbf2f9d6eaec5`
- candidate tree: `15c3f3c90f881f4454caa18e24df603c4af52bf5`
- 격리: `F:/dev/kor-travel-common-review-b-t301-postfix02` 별도 detached worktree
- candidate 검증 시점 상태: `HEAD (no branch)`, candidate SHA/tree 일치, `git status --porcelain=v1` 출력 없음. 검증 뒤 이 원본 report 파일 하나만 추가했다.
- 독립성: 상대 reviewer 원본과 통합 report를 읽지 않았다. 후보의 코드·정본 문서·task·현재 manifest만 기준으로 삼았다.

## 범위와 실제 검증

기준선부터 candidate까지의 전체 변경과 `tools/openapi_exceptions.py`, 회귀 시험, OpenAPI 정본·생성물, T-301 task/resume/journal evidence를 읽었다. 소비자 저장소 build/e2e, npm/PyPI 게시, GitHub Release, 원격 actionlint는 manifest 범위 밖이므로 `NOT_RUN(외부 선행 또는 범위 밖)`이다.

| 명령 | 결과 |
|---|---|
| `python -B -X utf8 tools/openapi_exceptions.py --check` | exit 0, 예외 39건·Markdown 54줄 |
| `python -B -X utf8 -m unittest discover -s tests -p 'test_openapi_exceptions.py' -v` | exit 0, 26 tests OK |
| `npm ci --ignore-scripts --no-audit --no-fund` | exit 0, 113 packages; Node `v25.9.0`에 package engine `^22.12.0` 경고 |
| `python -B -X utf8 -m unittest discover -s tests -p 'test_*.py' -q` | exit 0, **363 tests OK**, 236.782초 |
| `python -B -X utf8 tools/validate_document_links.py .` | exit 0, 533 documents / 2583 local targets, errors=0 |
| `python -B -X utf8 tools/validate_plan.py --root .` | exit 0, 상세 task 106, 오류 0 |
| `python -B -X utf8 tools/check_spdx.py --root .` | exit 0, 70 files, 오류 0 |
| `python -B -X utf8 tools/check_prod_redaction.py --root . --patterns .prod-redaction-patterns --all` | exit 0, 684 files, 발견 0건 |
| `python -B -X utf8 tools/scan_secrets.py --root . --patterns .secret-scan-patterns --all` | exit 0, 684 files, 발견 0건 |
| `git diff --check afc8d1bf166d0ddcbee059252eb5cee245157dcd 59a0fbc3ae426ec7a166ac34cbacbf2f9d6eaec5 --` | exit 0 |
| `gh run list --commit 59a0fbc3ae426ec7a166ac34cbacbf2f9d6eaec5` | docs run `34303194080` 및 workflows selftest `34303194366` 모두 `cancelled` |

PR 화면의 최신 성공 check는 이 immutable candidate가 아니라 newer head `b7562ee764218525837ad220c114a9c8e43cf7b9`의 run `34303220600`/`34303220698`이었다. 따라서 그 성공을 `59a0fbc`의 candidate CI 증거로 재사용하지 않았다.

추가 공격 probe 결과:

- `_FlatYamlParser`에 `1:2`, `1:2:3`, `-1:20`, `+1:20`, `-1:2:3.4`, `+1:2:3.4`, `123:45`를 plain scalar로 넣으면 모두 **ACCEPT**했다. PyYAML 6.0.3의 YAML 1.1 해석에서는 앞 항목들이 int/float로 해석된다.
- UTF-8 BOM은 문서 첫 글자일 때 ACCEPT, 첫 줄 이후일 때 REJECT했다.
- `Cc` U+0080, `Cf` U+200B/U+202E, `Zl` U+2028, `Zp` U+2029는 parser와 Markdown renderer 모두 REJECT했다.
- 본문에만 있는 `T-034`는 파일명이 없어 REJECT했다. 동일 `(app, rule, surface)` 중복은 REJECT했다.
- S1 surface를 `/**`로 바꾸면 ACCEPT했다.
- S1 reason을 `소비하는 외부 계약이 아니다`, `소비하는 외부 계약이 아닌 것으로 확인됐다`, `소비하는 외부 계약이 없다`로 바꾸고 `M10 동반 PR`과 `T-483`을 남기면 모두 ACCEPT했다.

## Findings

### B-P1-01 — 최종 실행 evidence가 candidate와 정합하지 않고 candidate CI도 취소됨

- 심각도: `P1`
- 위치: `docs/tasks/T-301-openapi-standard.md:76`, `docs/resume.md:11`, `docs/journal.md:5`
- disposition: `OPEN` — `BLOCK`
- 근거와 재현:
  1. immutable candidate에서 실제 full unittest는 **363**, task/resume는 **362**라고 단정한다.
  2. 실제 link gate는 **533/2583**, task 문장은 **532/2583**이다.
  3. 실제 redaction/secret scan 대상은 **684/0**, task 문장은 **683/0**이다.
  4. task line 76은 기능 candidate `36509d3`와 post-fix-02/03만 기록하고 현재 docs-only candidate `59a0fbc`/tree를 기록하지 않는다. resume는 여전히 “post-fix-03 후보 준비 중”, journal 최신 제목은 “post-fix-02 수정 준비”다.
  5. `gh run list --commit 59a0fbc...`에서 candidate의 docs/selftest run은 각각 `34303194080`/`34303194366`, 결론 `cancelled`다. PR 화면의 성공 run은 다른 head `b7562ee...`이므로 candidate 검증으로 집계할 수 없다.
- 영향: task·resume·journal이 current candidate의 실행 결과와 상태를 증명하지 못한다. 취소된 다른 SHA의 CI와 잘못된 수치를 통과 evidence처럼 사용하면 필수 gate/감사성을 깨뜨리며, 현재 P1은 merge 전에 원 reviewer 재확인이 필요하다.
- 권고: `59a0fbc`에서 실제 수치(363, 533/2583, 684/0)와 실행 ID·candidate/tree를 task/resume/journal/manifest에 일치시켜 기록하고, 같은 immutable candidate SHA의 docs/tools/selftest CI를 완료한 뒤 링크를 고정한다. 실행하지 못한 run은 `NOT_RUN` 또는 `cancelled`로 남긴다.

### B-P2-01 — signed·short sexagesimal YAML 수가 fail-closed 검사를 우회함

- 심각도: `P2`
- 위치: `tools/openapi_exceptions.py:46-57`, 특히 line 56의 `\d{1,2}:\d{2}`
- disposition: `OPEN` — 수정 권고
- 근거와 재현: 위 probe에서 `owner: 1:2`, `owner: 1:2:3`, `owner: -1:20`, `owner: +1:20`, `owner: -1:2:3.4`, `owner: +1:2:3.4`, `owner: 123:45`가 모두 plain 문자열로 ACCEPT됐다. 반면 PyYAML 6.0.3은 각각 YAML numeric int/float으로 해석한다. 현재 task line 76은 “sexagesimal timestamp도 plain scalar로 거부”한다고 선언한다.
- 영향: 지원하지 않는 YAML 문자열-only 부분집합이 모든 숫자 표기를 fail-closed로 닫지 못한다. 지금 필드가 최종적으로 문자열을 요구해 즉시 실행 코드가 숫자 객체를 받지는 않지만, 표준 YAML 소비자와 도구의 해석 차이가 남고 registry 계약의 금지 우회가 가능하다.
- 권고: YAML 1.1 sexagesimal의 선택 부호, 한 자리 분·초, 분·초 연속 형식을 명시적으로 거부하는 정규식과 회귀 시험을 추가하고, signed/short/decimal sexagesimal oracle 결과를 evidence에 남긴다.

### B-P2-02 — SHOULD reason 부정 표현 우회

- 심각도: `P2`
- 위치: `tools/openapi_exceptions.py:60-61`, `471-481`
- disposition: `OPEN` — 수정 권고
- 근거와 재현: `NEGATED_EVIDENCE_RE`가 `없음|아님|미확인|불가`만 찾는다. 첫 S1 reason을 다음과 같이 바꾸고 M10·동반 PR·T-483을 유지하면 모두 ACCEPT됐다.
  - `소비하는 외부 계약이 아니다. M10 동반 PR 근거. T-483`
  - `소비하는 외부 계약이 아닌 것으로 확인됐다. M10 동반 PR 근거. T-483`
  - `소비하는 외부 계약이 없다. M10 동반 PR 근거. T-483`
- 영향: 긍정 계약 phrase와 task/M10 토큰만 채운 부정 문장이 SHOULD 예외로 등록된다. registry 독자가 계약 사실로 오인할 수 있고, post-fix-02가 약속한 “긍정적인 ... 근거·부정 근거” fail-closed 경계가 어휘 변형으로 우회된다.
- 권고: 자연어 부분 문자열을 증명으로 사용하지 말고 positive evidence를 구조화된 필드/허용된 근거 토큰으로 분리한다. 최소한 `아니다|아닌|없다` 등 부정 활용형을 reject하고 부정 문장 회귀 시험을 추가한다.

### B-P2-03 — `/**` 전역 wildcard가 구체 surface 검사를 우회함

- 심각도: `P2`
- 위치: `tools/openapi_exceptions.py:471-479`
- disposition: `OPEN` — 수정 권고
- 근거와 재현: S1의 `surface: "/v2/*"`를 `surface: "/**"`로만 바꾼 임시 registry를 `load_registry`에 넣었고 ACCEPT됐다. 현재 검사는 정확히 `surface == "*"`만 거부한다.
- 영향: `/**`처럼 모든 경로를 덮는 global wildcard가 “구체적인 외부 계약 표면”으로 등록될 수 있다. 작성자가 `*`를 피하는 표기만으로 SHOULD 예외 범위를 전체 API로 확장한다.
- 권고: surface 문법을 정본에 두고 전역 wildcard(`*`, `/**`, 동등 표현)를 거부하며, 허용할 version prefix wildcard와 단일 operation/field 표면을 구분하는 회귀 시험을 추가한다.

## Finding summary

| 등급 | 신규·잔여 | disposition |
|---|---:|---|
| P0 | 0 | — |
| P1 | 1 | OPEN |
| P2 | 3 | OPEN |
| P3 | 0 | — |

통과한 경계는 BOM 시작 위치, Unicode `Cc/Cf/Zl/Zp` parser·renderer, task 파일명 provenance, 정확한 identity 중복, Markdown markup escaping, 생성물 drift와 atomic/alias 검사다. 이는 위 finding을 닫지 않는다.

## Verdict

**BLOCK**. B-P1-01이 candidate의 필수 실행·감사 evidence를 깨뜨리고, B-P2-01~03은 parser와 SHOULD 예외 계약에 재현 가능한 우회가 남아 있다. P1은 원 reviewer의 재확인 전 merge할 수 없으며, P2는 수정·회귀 시험·동일 candidate CI 재실행 후 post-fix-05에서 다시 검토해야 한다.

소비자 저장소 build/e2e, registry 게시, npm/PyPI 게시, GitHub Release, 원격 actionlint는 `NOT_RUN(이 common task의 외부 선행 또는 범위 밖)`이다.
