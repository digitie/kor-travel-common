# T-103 post-fix-06 독립 적대적 리뷰 B 원본

- 실행 ID: `T103-POST6-B-20260908T104137-KST`.
- 최종 판정: **NO-GO**. `B-P1-03` 잔여, `B-P1-12` 신규. P0 0건, P1 2건, 신규 P2/P3 0건이다.
- 시작 KST: `2026-09-08T10:41:37.7710120+09:00`; 제품 검증 종료 KST: `2026-09-08T10:46:06.8200284+09:00`.
- 시작·종료 제품 HEAD: `a40668bfb4ecac66d141da2ff791947d77208bd7`.
- 시작·종료 제품 tree: `9c5cbf93bc6b34c4895c98745404375becbc0b32`.
- 시작·종료 `git status --porcelain=v1`: 빈 출력, clean. 제품 검증 종료 뒤 원본 파일 하나의 별도 commit을 위해 `codex/review-t103-post6-b`를 만들었다.
- 격리: 새 detached worktree `F:/dev/kor-travel-common-wt/review-t103-post6-b`. 전체 시험·정적 gate는 후보를 임시 독립 Git 저장소로 복사하고 `GIT_*` 환경을 제거한 뒤 실행했다. 직접 반례는 후보 밖 임시 파일만 사용했다. 제품·소비자·source checkout 파일은 수정하지 않았다.
- source `.git/config` 시작·종료 SHA256 동일: `0A0F849E7874CF0A25926856F9D2E381CCBF4C2DCB5999869C57B86E0F5BEB5B`. `core.worktree` 변경 없음.
- manifest는 `git show 6372b29:docs/reviews/adversarial/evidence/2026-09-08-t103-post-fix-06-manifest.md`로만 읽었다. manifest 전체 commit: `6372b29f40abaf2168594fdf792eb44009264a54`; Git blob SHA256: `8c29a593a06cd54729d2237893274445ce578b2431659930da6b8e69504c1d80`.
- 상대 이번/이전 raw는 읽거나 요청하지 않았다. `ecad460..a40668b`의 변경 경로 7개와 제품 도구 2개·시험 2개 전체 diff를 확인했다. raw 본문은 읽지 않고 코드·직접 반례로 판단했다. 관련 task·정본·evidence가 이 delta에서 불변임을 확인하고 해당 계약·수치를 다시 대조했다.

## 전달 요청 원문

> post-fix-06 독립 적대 리뷰를 시작하세요. 불변 코드 후보 `a40668bfb4ecac66d141da2ff791947d77208bd7`, tree `9c5cbf93bc6b34c4895c98745404375becbc0b32`; manifest는 `6372b29`의 `docs/reviews/adversarial/evidence/2026-09-08-t103-post-fix-06-manifest.md`를 git show로 읽으세요. 상대 post-fix-06 raw 및 이전 상대 raw는 읽지 마세요. 배열·삼항·임의 tag·다중행·blockquote JSX, fence run/suffix/2자 inline span, selector quoted-space/case를 포함해 전체 누적 반례·CSS cascade/media·JSON/argparse/redaction/diff/symlink/airport를 Windows 3.14·WSL 3.11에서 독립 실행하세요. 새 raw 파일 `docs/reviews/adversarial/evidence/2026-09-08-t103-post-fix-06-reviewer-b.md` 하나만 추가해 별도 commit하고, SHA/SHA256/verdict를 보내세요. Windows 3.11은 NOT_RUN로 명시하세요.

## 누적 finding disposition

| ID / 원 심각도 | 결과 | 이번 후보의 직접 관찰 |
|---|---|---|
| B-P1-01 / P1 | FIXED | CWD와 다른 `--root`의 Git 추가 행을 사용하며 외부 root 반례 exit 1. |
| B-P1-02 / P1 | FIXED | 새 앞 1행은 fail, 이동한 기존 3행만 exempt. baseline 건수를 새 위반이 소비하지 않는다. |
| B-P1-03 / P1 | **OPEN** | 이전 단일행·단순 multiline·blockquote JSX는 P6 exit 1, fence run/suffix와 2자 inline span은 인용 유지로 수정됐다. 아래 중첩 객체·들여쓰기 없는 ESM 누락과 문서 문맥 오염은 남았다. |
| B-P1-04 / P1 | FIXED | CSS 값·누락 경로·var·baseline·잘못된 옵션/`--json=`은 generic exit 2, traceback/marker 없음. JSON·Markdown·step summary 경로 redaction 유지. |
| B-P2-05 / P2 | FIXED | 명시적 muted 읽기 표면은 31쌍, 1:1 미달 fail, 반복 옵션 중복 없음. |
| B-P2-06 / P2 | FIXED | bool/소수/무한대 count·버전·5,000자리 정수·깊이 2,000 JSON은 exit 2, traceback 없음. |
| B-P3-07 / P3 | FIXED | geo 미달 8건이 실제 CLI와 evidence 표에 일치. |
| B-P1-08 / P1 | FIXED | `++counter; window.confirm(...)` 추가 행을 `+++` 헤더로 오인하지 않고 P8 exit 1. |
| B-P1-09 / P1 | FIXED | 기존 media 조건 교집합·specificity/source order·root.dark·nested/string/comment 반례 유지. not/복합 조건은 exit 2, minified 조건은 공백 표기와 동등. |
| B-P2-10 / P2 | FIXED | Airport 역사 1.15와 현재 1.32가 task/evidence에서 구분됨. 현재 실측 `1.3209340364487114`. |
| B-P1-11 / P1 | FIXED | `.DARK`, `[data-theme='DARK']`, `[data-theme='d ark']`, `[data-theme = 'd ark']` 모두 exit 2. 실제 `.dark`·`[data-theme='dark']` 대조군은 정상 적용. |

즉, 누적 11개 중 10개 FIXED, B-P1-03 OPEN이며 별도 신규 B-P1-12를 추가한다. 합성 marker는 `'gh' + 'p_' + 'Z' * 36`으로 조립하고 노출 여부만 기록했다. 실제 비밀·운영 주소는 사용하지 않았다.

## B-P1-03: 중첩 표현식의 실행 template 누락과 문서 인용의 문맥 오염

심각도 **P1**, 기존 ID 유지. 위치는 `tools/ux_lint.py:123-128`의 원문 전체를 대상으로 한 열린 속성 정규식과 들여쓰기 조건이다. T-103의 실행 MDX 검사·문서 인용 제외 계약을 충족하지 못한다.

각 입력을 별도 임시 `Page.mdx`로 저장하고 다음 명령을 실행했다. 아래 세 가지를 모두 Windows 3.14.3과 WSL 3.11.15에서 재현했다.

```text
python -B -X utf8 <후보>/tools/ux_lint.py --root <임시 디렉터리> --fail-new --json
```

실행 누락 1 — 객체가 포함된 JSX 표현식:

```mdx
<div className={
 [Object.keys({active:true}), `outline-none`].join(" ")
}/>
```

실제 **exit 0, PASS, findings 0**. 이 표현식은 실제 class에 `outline-none`을 넣는다. 같은 JSX 전체를 한 행으로 합친 대조군은 **exit 1, FAIL, P6 1건**이다. 기대는 줄바꿈 유무와 무관한 P6 exit 1이다. 내부 객체의 닫는 중괄호가 `[^{}]*` 조건을 끊으므로 외부 JSX 속성 문맥을 잃는다.

실행 누락 2 — 들여쓰기 없는 ESM 값:

```mdx
export const tokenClass =
`outline-none`;

<div className={tokenClass}/>
```

실제 **exit 0, PASS, findings 0**. 기대는 P6 exit 1이다. ESM template의 실행 여부가 들여쓰기 유무에 의존해서는 안 된다. 선언을 한 줄에 쓴 실행 대조군은 기존 시험/직접 반례에서 검출된다.

문서 오탐 — 인용한 속성 문법이 뒤 문서의 실행 문맥으로 새어 나옴:

```mdx
문법 예시: `className={`

다른 인용: `outline-none`
```

실제 **exit 1, FAIL, P6 1건**. 기대는 **exit 0, findings 0**이다. 두 code span 모두 문서 인용이며 열린 JSX 표현식이 아니다. 첫 span을 가렸어도 `before = text[:start]`가 가리기 전 원문을 다시 읽어 열린 속성으로 오인한다.

이전 제품 `ecad460`과 같은 도구를 갖는 post5 격리 사본에도 동일 probe를 실행했다. 두 실행 누락은 이전부터 잔여이고, 문서 오탐은 이전 exit 0에서 이번 exit 1로 바뀐 새 회귀다. 이전 raw 본문은 읽지 않았다. 보조 `String(...)` probe는 실제 class 영향이 명확한 위 객체 배열 반례로 대체해 finding의 근거로 세지 않았다.

영향: 포매터·객체 옵션·ESM 줄바꿈으로 실제 focus outline 제거가 신규 위반 gate를 통과한다. 반대로 문법을 설명하는 일반 문서가 신규 위반으로 차단된다.

권고: 마스킹한 문서/주석과 실행 영역을 분리한 상태를 사용하고, JSX/ESM 괄호 중첩을 추적한다. 들여쓰기나 중괄호 없는 부분문자열로 실행 문맥을 대신하지 않는다. 위 양성 2개·음성 1개와 기존 단일행/multiline/blockquote/fence corpus를 같은 회귀군으로 고정한 새 후보가 필요하다.

## B-P1-12: 빈 selector list 항목을 버려 무효 CSS로 대비 미달을 PASS 처리

심각도 **P1**, 신규 ID. 위치는 `tools/kt_contrast.py:136`의 `_split_selectors`, `:210-212`의 빈 항목 건너뛰기, `:330`의 `raw_part.strip()` 조건이다. 비어 있는 selector를 입력 오류로 거부하지 않고 나머지만 적용한다.

임시 `override.css`:

```css
:root { --kt-control-line: #000; }
:root, { --kt-control-line: #fff; }
```

실행:

```text
python -B -X utf8 <후보>/tools/kt_contrast.py <후보>/packages/tokens/tokens.css <임시>/override.css --dark --fail-new --json
```

Windows/WSL 모두 **exit 0, PASS**, control-line 4쌍을 통과시킨다. page/subtle/muted/card는 `18.442/16.412/13.097/16.857`이다. 두 번째 selector를 `,:root` 또는 `:root,,.dark`로 바꿔도 동일하다. 이 세 입력은 일반 selector list에 빈 항목이 있는 무효 CSS이므로 그 선언을 유효한 전역 토큰처럼 적용해서는 안 된다. 기대는 generic **exit 2** 입력 오류다.

두 번째 규칙을 제거한 대조군은 실제로 **exit 1**, control-line 4쌍 `1.139/1.280/1.603/1.246` 미달이다. 올바른 `:root` 또는 `:root,.dark`로 바꾼 대조군은 exit 0이 맞다. 무효 목록과 유효 목록을 동일하게 처리하는 것이 문제다.

이전 제품 코드 대조에서도 빈 목록 3종이 PASS라서 이번 수정이 새로 만든 회귀는 아니다. 이번 전체 selector 입력 경계 검토에서 독립 발견한 기존 누락이다.

영향: CSS 오타로 실제 브라우저에서 적용되지 않는 흰 선 선언을 checker가 적용해 3:1 미달을 합격시킨다. 지원 밖 selector 목록을 입력 오류로 닫는 이번 수정의 출구가 완전하지 않다.

권고: 최상위 selector list를 분리한 즉시 모든 항목이 비어 있지 않은지 검증하고, 앞/중간/뒤 빈 항목 중 하나라도 있으면 선언을 적용하기 전에 generic exit 2로 중단한다. 유효 목록 대조군과 빈 항목 3종을 양 OS 시험에 추가한다.

## 실행 명령과 검증 수치

Windows `py -3.14`는 **3.14.3**, WSL `/home/digitie/.local/share/uv/python/cpython-3.11-linux-x86_64-gnu/bin/python3.11`은 **3.11.15**를 직접 확인했다. 아래 `python`은 해당 실행 파일이다. 전체 discovery는 출력량 때문에 manifest의 `-v`만 생략했고 집중 시험은 지정 명령 그대로 실행했다.

| 명령 | Windows | WSL |
|---|---|---|
| `python -B -X utf8 -m unittest discover -s tests -p test_*.py` | 282 실행·통과, 82.174초, skip 0 | 282개 중 279 실행·통과, 23.219초, skip 3 |
| `python -B -X utf8 -m unittest tests.test_kt_contrast tests.test_ux_lint -v` | 44/44, 10.059초, skip 0 | 44/44, 5.764초, skip 0 |
| `python -B -X utf8 tools/validate_document_links.py` | 410문서·2412대상, 오류 0 | 동일 |
| `python -B -X utf8 tools/validate_plan.py` | 106 task, 오류 0 | 동일 |
| `python -B -X utf8 tools/check_spdx.py` | 56파일, 오류 0 | 동일 |
| `python -B -X utf8 tools/scan_secrets.py --all` | 542파일, 발견 0 | 동일 |
| `python -B -X utf8 tools/check_prod_redaction.py --all` | 542파일, 발견 0 | 동일 |
| `python -B -X utf8 tools/check_versions.py --self-check` | exit 0, 소비자 검사 미실행 | 동일 |
| `python -B -X utf8 tools/check_aliases.py packages/tokens/aliases` | CSS 1개, 오류 0 | 동일 |
| 별칭 집중 unittest | 35/35 통과 | 35개 중 34 실행·통과, Windows 전용 1 skip |
| `python -B -X utf8 tools/kt_contrast.py packages/tokens/tokens.css --json` | exit 0, 27쌍 | 동일 |
| `python -B -X utf8 tools/ux_lint.py --root tests/fixtures/ux --json` | report 모드 exit 0, 12건 | 동일 |
| 4앱 예제 + baseline + `--fail-new` | 미달 4/8/8/4건, baseline 적용 exit 0 | 동일 |
| `git diff --check 94ca2f1730b270721eb6242bfcdd9362b51d45e5 a40668bfb4ecac66d141da2ff791947d77208bd7` | exit 0, 출력 없음 | 동일 Git blob 비교 재사용 |

전체 회귀/정적 gate는 후보 밖 helper `review-t102-b-wsl-unittest.py`·`review-t102-post-b-gates.py`로 독립 사본에서 실행했다. 직접 probe는 `.git/codex-audit/`의 `t103-post1-b-originals.py`, `t103-b-edge.py`, `t103-post1-b-new.py`, `t103-post1-b-media.py`, `t103-post3-b-new.py`, `t103-post3-b-smoke.py`, `t103-post4-b-new.py`, `t103-post5-b-new.py`, `t103-post6-b-new.py`다. 이름에 과거 회차가 들어가도 이번 후보 경로를 인자로 넘겨 양 OS에서 새로 실행했다. 마지막 probe의 이전 코드 대조는 Windows에서만 했으며 이전 후보의 새 전체 PASS로 세지 않았다.

기존 CSS 교집합·root.dark와 동치 표기·specificity/source order, not/복합 media 입력 오류, nested/string/comment, 깊은 JSON, argparse, 오류 stdout/stderr 및 정상 JSON/Markdown/step summary redaction, diff `+++`, self-symlink root를 직접 반례와 집중 시험으로 대조했다. task/evidence의 geo 8건·airport 1.32와 `IN_PROGRESS`, 후속 소비자·T-010 gate도 확인했다. GPL/미게시/소비자 경계 문서는 불변이다.

## NOT_RUN과 범위

- `NOT_RUN(Windows Python 3.11)`: 설치되어 있지 않으며 요청자가 Windows 3.14를 지정했다.
- WSL skip 3개: Windows 8.3 API 1개, `jsonschema` 미설치로 JSON Schema parity 2개. 이번에도 `find_spec('jsonschema') is None`을 확인했다. skip을 통과 건수로 세지 않는다. T-103 집중 44개는 양 OS skip 0이다.
- `NOT_RUN(원격 CI 독립 조회)`: 로컬 시험을 원격 CI 성공으로 대신하지 않았다.
- `NOT_RUN(소비자 build/e2e, registry/npm/PyPI 게시, workflow dispatch, MDX compiler/browser 실행)`: 요청 범위 밖. 외부 패키지 설치·소비자 호출·게시는 하지 않았다. 반례는 고정 코드 CLI와 문법 의미를 대조했다.
- 소비자 baseline 채택과 T-010 workflow selftest는 해당 후속 task의 gate다. 제품 후보를 수정하지 않고 원본 한 파일만 별도 commit한다. push하지 않는다.

최종 **NO-GO**. 기존 B-P1-11을 포함한 10건은 FIXED이나 B-P1-03과 신규 B-P1-12가 남아 있으므로 수정 후보의 독립 재검토가 필요하다.
