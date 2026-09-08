# T-103 post-fix-07 독립 적대적 리뷰 B 원본

- 실행 ID: `T103-POST7-B-20260908T105507-KST`.
- 최종 판정: **NO-GO**. 기존 `B-P1-03`이 OPEN이다. P0 0건, P1 1건, 신규 P2/P3 0건. 잔여 반례들은 같은 MDX 실행/인용 구분 계약으로 묶고 신규 ID를 만들지 않았다.
- 시작 KST: `2026-09-08T10:55:07.0702886+09:00`; 제품 검증 종료 KST: `2026-09-08T10:59:19.9819414+09:00`.
- 시작·종료 제품 HEAD: `63fe3d5c969b28bab4d528d3e24a054e3a8e30e6`.
- 시작·종료 제품 tree: `c9fb07160de150d7a4cfbbb31fc226cb6a9fb3af`.
- 시작·종료 `git status --porcelain=v1`: 빈 출력, clean. 검증 종료 뒤 원본 하나를 별도 commit하기 위해 `codex/review-t103-post7-b`를 만들었다. 보고서 commit은 제품 검증 SHA와 다르다.
- 격리: 새 detached worktree `F:/dev/kor-travel-common-wt/review-t103-post7-b`. 전체 시험·정적 gate는 후보를 임시 독립 Git 저장소로 복사하고 `GIT_*` 환경을 제거해 실행했다. 직접 반례는 후보 밖 임시 입력을 사용했다. 제품·소비자·source checkout 파일 수정 없음.
- source `.git/config` 시작·종료 SHA256 동일: `0A0F849E7874CF0A25926856F9D2E381CCBF4C2DCB5999869C57B86E0F5BEB5B`. `core.worktree` 변경 없음.
- manifest는 `git show dbfb036:docs/reviews/adversarial/evidence/2026-09-08-t103-post-fix-07-manifest.md`로 읽었다. 전체 manifest commit: `dbfb036ed054d6f591ad295be4db148177956fd8`; Git blob SHA256: `e32da7314f95d8994b3437468422428515f93a37317178e8e977ce59da18f3f8`.
- 상대 이번/이전 raw는 읽거나 요청하지 않았다. `a40668b..63fe3d5` 변경 경로 7개와 제품 도구 2개·시험 2개 전체 diff를 확인했다. 이전 raw 본문은 제외했다. task·정본·evidence 불변과 현재 `IN_PROGRESS`·후속 gate를 확인했다.

## 전달 요청 원문

> post-fix-07 독립 적대 리뷰를 시작하세요. 불변 코드 후보 `63fe3d5c969b28bab4d528d3e24a054e3a8e30e6`, tree `c9fb07160de150d7a4cfbbb31fc226cb6a9fb3af`; manifest는 `dbfb036`의 `docs/reviews/adversarial/evidence/2026-09-08-t103-post-fix-07-manifest.md`를 git show로 읽으세요. 상대 post-fix-07 raw/이전 상대 raw는 읽지 마세요. 중첩 object·무들여쓰기 ESM·문서 문맥·미종결 span, 빈 selector list와 root descendant 및 누적 모든 반례, CSS/media/JSON/argparse/redaction/diff/symlink/airport를 Windows 3.14·WSL 3.11에서 독립 검증하세요. 새 raw `docs/reviews/adversarial/evidence/2026-09-08-t103-post-fix-07-reviewer-b.md` 하나만 추가해 별도 commit하고 SHA/SHA256/verdict를 보내세요. Windows 3.11은 NOT_RUN로 기록하세요.

## 누적 finding disposition

| ID / 원 심각도 | 결과 | 이번 후보의 재현 결과 |
|---|---|---|
| B-P1-01 / P1 | FIXED | 외부 `--root`의 Git 추가 행을 사용하며 CWD와 무관하게 exit 1. |
| B-P1-02 / P1 | FIXED | 새 앞 1행 fail, 이동한 기존 3행만 exempt. 새 위반이 baseline 건수를 소비하지 않음. |
| B-P1-03 / P1 | **OPEN** | 기존 단일행·단순 multiline·blockquote JSX·중첩 객체·무들여쓰기 ESM은 P6 exit 1로 수정. 기존 문서 예시·fence·2자 span도 기대값. 아래 주석/인용 문맥·미종결 span 잔여는 실패. |
| B-P1-04 / P1 | FIXED | CSS 값·누락 경로·var·baseline·잘못된 옵션/`--json=`은 generic exit 2, traceback/marker 없음. JSON·Markdown·step summary 경로 redaction 유지. |
| B-P2-05 / P2 | FIXED | 명시적 muted 읽기 표면 31쌍, 1:1 미달 fail, 반복 옵션 중복 없음. |
| B-P2-06 / P2 | FIXED | bool/소수/무한대 count·버전·5,000자리 정수·깊이 2,000 JSON은 exit 2, traceback 없음. |
| B-P3-07 / P3 | FIXED | geo 미달 8건이 CLI와 evidence에 일치. |
| B-P1-08 / P1 | FIXED | `++counter; window.confirm(...)` 추가 행을 헤더로 오인하지 않고 P8 exit 1. |
| B-P1-09 / P1 | FIXED | CSS media 교집합·specificity/source order·root.dark·nested/string/comment 유지. not/복합 media는 exit 2, 공백 유무는 동등. |
| B-P2-10 / P2 | FIXED | Airport 역사 1.15와 현재 1.32 분리, 실측 `1.3209340364487114` 일치. |
| B-P1-11 / P1 | FIXED | `.DARK`, `[data-theme='DARK']`, `[data-theme='d ark']`, 공백 있는 속성 문법의 동일 반례 모두 exit 2. 유효 dark 대조군 정상 적용. |
| B-P1-12 / P1 | FIXED | `:root,`, `,:root`, `:root,,.dark` 모두 exit 2. 정상 `:root,.dark`는 exit 0. |

별도로 `:root .dark`, `:root [data-theme="dark"]`의 토큰 선언은 양 OS exit 2임을 직접 확인했다. 누적 12개 중 11개 FIXED, B-P1-03 OPEN이다. 합성 marker는 `'gh' + 'p_' + 'Z' * 36`으로 조립하고 노출 여부만 기록했다. 실제 비밀·운영 주소 사용 없음.

## B-P1-03 잔여: 주석·문서·span 경계를 실행 문맥과 분리하지 못함

심각도 **P1**, 수정 필요. 위치는 `tools/ux_lint.py:100-128`의 `_has_open_jsx_expression`, 특히 원문 `before`와 주석을 구분하지 않는 balance 계산, `:333-348`의 delimiter 처리다. 계약은 T-103의 실행 MDX 검사와 문서 인용 제외다.

아래 입력들을 각각 별도 임시 `Page.mdx`로 저장해 동일 명령을 실행했다. 모든 실제/기대 대조를 Windows 3.14.3·WSL 3.11.15에서 독립 실행했다.

```text
python -B -X utf8 <후보>/tools/ux_lint.py --root <임시 디렉터리> --fail-new --json
```

### 1. JS 주석 안의 닫는 중괄호가 실행 표현식을 닫음

```mdx
<div className={
 [Object.keys({active:true}), /* } */ `outline-none`].join(" ")
}/>
```

실제 **exit 0, PASS, findings 0**, 기대 **exit 1, P6 1건**. 주석을 `/* 주석 */`으로만 바꾼 대조군은 실제로 exit 1·P6 1건이다. JSX와 런타임 class는 같지만 `_has_open_jsx_expression`이 주석의 `}`를 balance에 반영해 실행 문맥을 잃는다. 큰따옴표/작은따옴표/backtick만 제외하고 JS 주석은 제외하지 않는 원인을 코드에서 확인했다.

### 2. 문서 code span의 JSX 예시가 뒤 인용을 실행 문맥으로 오염

```mdx
문법 예시: `<div className={`

다른 인용: `outline-none`
```

실제 **exit 1, FAIL, P6 1건**, 기대 **exit 0, findings 0**. 두 부분 모두 Markdown code span이다. 첫 span에서 `<div `를 제거한 기존 반례는 이번 후보에서 exit 0으로 수정됐지만, 가리기 전 원문을 다시 검색하는 구조는 남았다. `<div`를 찾는 조건 추가만으로 실제 JSX와 문서 예시를 분리하지 못한다.

### 3. 미종결 단일 backtick이 뒤의 실행 JSX를 숨김

```mdx
Example ` unmatched

export const X=()=> <div className="outline-none"/>;
```

실제 **exit 0, PASS, findings 0**, 기대 **exit 1, P6 1건**. 앞 문서에서 짝 없는 한 문자 delimiter는 뒤의 JSX까지 인용으로 만들 수 없다. 같은 입력의 첫 backtick을 두 개로 바꾼 대조군은 이번 수정으로 exit 1·P6 1건이다. 새 미종결 처리가 `run_length >= 2` 분기에만 있어 1자 분기는 계속 입력 끝까지 가린다.

### 4. 다른 문단에서 찾은 delimiter가 중간 실행 영역을 숨김

```mdx
Example `` unmatched

export const X=()=> <div className="outline-none"/>;

Later `` delimiter
```

실제 **exit 0, PASS, findings 0**, 기대 **exit 1, P6 1건**. 문단을 넘어 뒤의 두 문자 delimiter까지 한 inline span으로 취급해 중간 ESM/JSX를 가린다. 종료 문자가 아예 없는 경우만 고치면 이 반례가 남는다. inline span의 검색 범위도 Markdown 블록 경계에 맞아야 한다.

이전 제품 `a40668b`와 같은 도구를 갖는 post6 사본에 동일 probe를 Windows에서 실행했다. 위 잔여 4개는 이전에도 실패했다. 이번 새 balance 로직은 일반 중첩 객체를 고쳤고 2자 미종결 span도 수정했으나 동일 계약의 주석/문서/1자/문단 경계는 닫히지 않았다. 이전 raw는 읽지 않았다.

영향: 주석·일반 문서 내용에 따라 실행 class의 focus outline 제거를 신규 위반 gate에서 놓치거나 문서 인용을 위반으로 차단한다. 동작과 무관한 문서/주석 편집이 gate 결과를 바꾼다.

권고: 가리기 전 원문에서 JSX 문맥을 재추론하지 말고 주석·문서 영역을 구분한 lexer 상태를 사용한다. 괄호 balance에서 JS 주석을 제외하고, inline span은 delimiter 길이와 블록 경계를 함께 처리하며 미종결 1자/다문자에 같은 원칙을 적용한다. 위 양성·음성·대조군 전체를 기존 corpus와 함께 회귀로 고정한 새 후보가 필요하다.

## 검증 명령과 실제 수치

Windows `py -3.14`의 **3.14.3**, WSL `/home/digitie/.local/share/uv/python/cpython-3.11-linux-x86_64-gnu/bin/python3.11`의 **3.11.15**를 직접 확인했다. 아래 `python`은 각 실행 파일이다. 전체 discovery는 출력량 때문에 manifest의 `-v`만 생략했고 집중 명령은 그대로 실행했다.

| 명령 | Windows | WSL |
|---|---|---|
| `python -B -X utf8 -m unittest discover -s tests -p test_*.py` | 285 실행·통과, 78.570초, skip 0 | 285개 중 282 실행·통과, 23.972초, skip 3 |
| `python -B -X utf8 -m unittest tests.test_kt_contrast tests.test_ux_lint -v` | 47/47, 11.508초, skip 0 | 47/47, 6.966초, skip 0 |
| `python -B -X utf8 tools/validate_document_links.py` | 413문서·2412대상, 오류 0 | 동일 |
| `python -B -X utf8 tools/validate_plan.py` | 106 task, 오류 0 | 동일 |
| `python -B -X utf8 tools/check_spdx.py` | 56파일, 오류 0 | 동일 |
| `python -B -X utf8 tools/scan_secrets.py --all` | 545파일, 발견 0 | 동일 |
| `python -B -X utf8 tools/check_prod_redaction.py --all` | 545파일, 발견 0 | 동일 |
| `python -B -X utf8 tools/check_versions.py --self-check` | exit 0, 소비자 검사 미실행 | 동일 |
| `python -B -X utf8 tools/check_aliases.py packages/tokens/aliases` | CSS 1개, 오류 0 | 동일 |
| 별칭 집중 unittest | 35/35 통과 | 35개 중 34 실행·통과, Windows 전용 1 skip |
| `python -B -X utf8 tools/kt_contrast.py packages/tokens/tokens.css --json` | exit 0, 27쌍 | 동일 |
| `python -B -X utf8 tools/ux_lint.py --root tests/fixtures/ux --json` | report 모드 exit 0, 12건 | 동일 |
| 4앱 예제 + baseline + `--fail-new` | 미달 4/8/8/4건, baseline 적용 exit 0 | 동일 |
| `git diff --check 94ca2f1730b270721eb6242bfcdd9362b51d45e5 63fe3d5c969b28bab4d528d3e24a054e3a8e30e6` | exit 0, 출력 없음 | 동일 Git blob 비교 재사용 |

전체 회귀/정적 gate는 후보 밖 helper `review-t102-b-wsl-unittest.py`·`review-t102-post-b-gates.py`로 독립 사본에서 실행했다. 직접 probe는 `.git/codex-audit/`의 `t103-post1-b-originals.py`, `t103-b-edge.py`, `t103-post1-b-new.py`, `t103-post1-b-media.py`, `t103-post3-b-new.py`, `t103-post3-b-smoke.py`, `t103-post4-b-new.py`, `t103-post5-b-new.py`, `t103-post6-b-new.py`, `t103-post7-b-new.py`다. 과거 회차 이름과 무관하게 이번 후보 경로를 인자로 넘겨 양 OS에서 새로 실행했다. 이전 코드 대조는 Windows에서만 했고 이전 후보 전체를 재승인한 것으로 세지 않았다.

CSS 교집합·root.dark/동치 표기·specificity/source order, not/복합 media 입력 오류, nested/string/comment, 깊은 JSON, argparse, 오류 stdout/stderr 및 정상 JSON/Markdown/step summary redaction, diff `+++`, self-symlink root를 직접 반례와 집중 시험으로 대조했다. task/evidence의 geo 8건·airport 1.32와 미완료 상태, 소비자·T-010 후속 gate를 확인했다. GPL/미게시/소비자 경계 문서는 불변이다.

## NOT_RUN과 한계

- `NOT_RUN(Windows Python 3.11)`: 설치되어 있지 않으며 요청자가 Windows 3.14를 지정했다.
- WSL skip 3개: Windows 8.3 API 1개, `jsonschema` 미설치로 JSON Schema parity 2개. 이번에도 `find_spec('jsonschema') is None`을 확인했다. skip을 통과 건수에 넣지 않는다. T-103 집중 47개는 양 OS skip 0이다.
- `NOT_RUN(원격 CI 독립 조회)`: 로컬 시험을 원격 CI 성공으로 대체하지 않았다.
- `NOT_RUN(소비자 build/e2e, registry/npm/PyPI 게시, workflow dispatch, MDX compiler/browser 실행)`: 요청 범위 밖. 외부 패키지 설치·소비자 호출·게시는 하지 않았다. 반례는 고정 CLI와 문법 의미로 대조했다.
- 소비자 baseline 채택과 T-010 workflow selftest는 해당 후속 task의 gate다. 제품 수정 없이 원본 한 파일만 별도 commit하고 push하지 않는다.

최종 **NO-GO**. B-P1-12와 root descendant 차단은 확인했으나 B-P1-03이 OPEN이므로 수정 후보의 독립 재검토가 필요하다.
