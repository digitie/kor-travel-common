# T-301 독립 적대적 리뷰 B — post-fix-05

- 실행 ID: `T301-20260909-post-fix-05-B`
- 리뷰 종류: post-fix-05 독립 적대적 리뷰 B (문서·계약·parser·renderer·재현성)
- 실행 시각: 2026-09-09 12:01 KST 기준 고정
- 입력 manifest: `docs/reviews/adversarial/evidence/2026-09-09-t301-post-fix-05-manifest.md`
- manifest SHA-256: `03570ff162de9596ad8aa4704b670e99854d70a7eafa57351058355950055cc0`
- base: `afc8d1bf166d0ddcbee059252eb5cee245157dcd`
- candidate: `62d3107967e5f7875024472fc91ded1ac5f7ba50`
- candidate tree: `4cc37b3574a552999e524101e426c4568d3bc3e0`
- 격리: `F:/dev/kor-travel-common-review-b-t301-postfix02` 별도 detached worktree
- candidate 검증 시점 상태: `HEAD (no branch)`, candidate SHA/tree 일치, `git status --porcelain=v1` 출력 없음. 검증 뒤 이 원본 report 파일 하나만 추가했다.
- 독립성: 상대 reviewer 원본과 통합 report를 읽지 않았다. 후보의 코드·정본 문서·task·manifest만 기준으로 삼았다.

## 범위와 실제 검증

base부터 candidate까지의 전체 delta와 `tools/openapi_exceptions.py`, 회귀 시험, OpenAPI 정본·생성물, T-301 task/resume/journal evidence를 확인했다. 소비자 저장소 build/e2e, npm pack/publish, PyPI build/publish, GitHub Release, actionlint는 manifest 범위 밖이므로 `NOT_RUN(외부 선행 또는 범위 밖)`이다.

| 명령 | 결과 |
|---|---|
| `python -B -X utf8 tools/openapi_exceptions.py --check` | exit 0, 예외 39건·Markdown 54줄 |
| `python -B -X utf8 -m unittest discover -s tests -p 'test_openapi_exceptions.py' -v` | exit 0, 27 tests OK |
| `python -B -X utf8 -m unittest discover -s tests -p 'test_*.py' -q` | exit 0, **364 tests OK**, 262.513초 |
| `python -B -X utf8 tools/validate_document_links.py .` | exit 0, 536 documents / 2583 local targets, errors=0 |
| `python -B -X utf8 tools/validate_plan.py --root .` | exit 0, 상세 task 106, 오류 0 |
| `python -B -X utf8 tools/check_spdx.py --root .` | exit 0, 70 files, 오류 0 |
| `python -B -X utf8 tools/check_prod_redaction.py --root . --patterns .prod-redaction-patterns --all` | exit 0, 687 files, 발견 0건 |
| `python -B -X utf8 tools/scan_secrets.py --root . --patterns .secret-scan-patterns --all` | exit 0, 687 files, 발견 0건 |
| `git diff --check afc8d1bf166d0ddcbee059252eb5cee245157dcd 62d3107967e5f7875024472fc91ded1ac5f7ba50 --` | exit 0 |

candidate SHA `62d3107`의 GitHub check-runs도 직접 조회했다. docs·tools(Windows/Ubuntu)·packages·secret-scan·check-versions와 fixture docs/versions/contrast를 포함한 12개 check-run이 모두 `completed/success`였다. 대표 workflow run은 docs `34304849979`, workflows selftest `34304850114`이며 모든 check-run의 `head_sha`가 candidate와 일치한다. 이후 PR 화면에 보인 newer head의 취소/실패 상태를 candidate evidence로 재사용하지 않았다.

## post-fix-04 회귀와 추가 공격

- `0x_FF`, `0o_10`, `0b_10`, `1:2`, `1:2:3`, `-1:20`, `+1:20`, `-1:2:3.4`, `+1:2:3.4`, `123:45`, `2026-09-06T00:00:00.123+9:00`, `2026-09-06T00:00:00+09` plain scalar는 모두 REJECT됐다.
- S surface `*`, `/*`, `/**`는 REJECT됐다. 실험적으로 `/**/`, `/*/`는 ACCEPT됐지만 현재 문서가 전역 wildcard로 정의한 정본 어휘는 `*`·`/*`·`/**`이며, 이를 별도 finding으로 확대하지 않았다.
- `소비하는 외부 계약은 아니다`, `아닌 것으로 확인됐다`, `없다`, `미확인이다`, 영어 `no` 변형은 REJECT됐다.
- 그러나 `소비하는 외부 계약이 미채택/거부/미사용/비채택/불존재/미제공/무효`는 M10·T-483을 함께 두면 ACCEPT됐다.
- `M100`, `M10X`, `미동반 PR`, `동반 PRX`도 M10/동반 PR 근거로 ACCEPT됐다.
- renderer에 schema/updated/apps 문자열의 개행·Markdown heading을 직접 주입하면 출력에는 heading이 남지 않았다. top-level schema/updated/apps/exceptions의 잘못된 타입과 extra key는 RegistryError로 REJECT됐다.
- UTF-8 BOM은 문서 첫 글자만 허용됐고 이후 위치는 REJECT됐다. `Cc`/`Cf`/`Zl`/`Zp`, task 본문만의 `T-034`, 동일 `(app, rule, surface)` 중복, Markdown markup은 모두 기존 회귀와 같이 REJECT/escape됐다.

## Findings

### B-P2-01 — SHOULD 부정 근거 어휘가 여전히 substring 우회됨

- 심각도: `P2`
- 위치: `tools/openapi_exceptions.py:60-63`, `tools/openapi_exceptions.py:474-484`
- disposition: `OPEN` — 수정 권고
- 근거와 재현: 현재 `NEGATED_EVIDENCE_RE`는 `아니|아님|없|않|못|불가|미확인|부재|불가능`과 일부 영어 부정어만 찾는다. 첫 S1 reason을 다음과 같이 바꾸고 positive phrase, `M10`, `T-483`을 유지하면 모두 ACCEPT됐다: `소비하는 외부 계약이 미채택이다`, `... 거부`, `... 미사용`, `... 비채택`, `... 불존재`, `... 미제공`, `... 무효`.
- 영향: 외부 계약을 채택하지 않았다는 부정 문장이 SHOULD 예외의 긍정 증명으로 등록될 수 있다. 이번 candidate 문서는 한국어·영어 부정 근거를 fail-closed로 닫았다고 기록하지만, 자유 자연어의 미등록 활용형으로 우회된다.
- 권고: 자연어 substring을 증명으로 사용하지 말고 `external_contract: true` 같은 구조화된 필드와 허용된 근거 토큰을 분리한다. 당장 구조 변경이 어렵다면 현행 정본 reason에 등장하는 `미채택`과 충돌하지 않도록 문맥을 분리한 parser를 만들고 부정 활용형 corpus를 회귀 시험에 추가한다.

### B-P2-02 — M10·동반 PR 증명이 토큰 경계 없는 substring 검사임

- 심각도: `P2`
- 위치: `tools/openapi_exceptions.py:483-484`
- disposition: `OPEN` — 수정 권고
- 근거와 재현: `if "M10" not in entry["reason"] and "동반 PR" not in entry["reason"]`는 exact token이 아닌 substring을 허용한다. 다음 reason들이 모두 ACCEPT됐다.
  - `소비하는 외부 계약이다. M100 근거. T-483`
  - `소비하는 외부 계약이다. M10X 근거. T-483`
  - `소비하는 외부 계약이다. 미동반 PR 근거. T-483`
  - `소비하는 외부 계약이다. 동반 PRX 근거. T-483`
- 영향: 존재하지 않는 규칙 ID 또는 동반하지 않은 PR 문장을 근거로 위장할 수 있어 SHOULD 예외의 감사 추적성이 약해진다.
- 권고: `M10`은 식별자 boundary를 갖는 정규식으로, 동반 PR은 허용된 phrase/token grammar로 검증하고 `미동반`·접미 문자를 거부한다. 이 입력을 회귀 시험에 고정한다.

## Finding summary

| 등급 | 신규·잔여 | disposition |
|---|---:|---|
| P0 | 0 | — |
| P1 | 0 | — |
| P2 | 2 | OPEN |
| P3 | 0 | — |

BOM·Unicode·YAML numeric/base/sexagesimal/timezone·task filename provenance·renderer top-level·exact wildcard·duplicate·candidate SHA CI·문서 수치는 이번 candidate에서 재현 결과 정합했다. 이는 위 P2 finding을 닫지 않는다.

## Verdict

**CONDITIONAL**. P0/P1과 stale evidence는 없고 candidate SHA의 필수 check-run은 성공했지만, 자유 문자열 SHOULD 증명에 재현 가능한 부정어·근거 token boundary 우회가 남아 있다. merge/closure 전에 B-P2-01~02를 구조화된 증명 또는 명시된 owner·후속 task·gate·기한으로 disposition하고, 수정 candidate에서 B가 재검토해야 한다.

소비자 저장소 build/e2e, npm/PyPI/Release 게시, actionlint는 `NOT_RUN(이 common task의 외부 선행 또는 범위 밖)`이다.
