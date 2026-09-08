# T-103 구조 수정 독립 리뷰 A 원본

- 실행 ID: `T103-ROOT-A-20260908-191849-KST`; 판정: **BLOCK**.
- 시작: 2026-09-08 19:18:49.684 KST; 제품 검토 종료: 2026-09-08 19:25:36.637 KST.
- 불변 제품 HEAD: `b013ab0d2e95e3d892f6dbfa42042389582ea8a9`; tree: `de5b30f25840bd9da19f073f62ae6bc9607fa7ef`.
- delta base: `841ee985db564deb0d571edb6f0f9330311a35d6`. 공통 manifest는 `4ddb9601149a85202486719e7ab16dbb4448b8ac`의 `docs/reviews/adversarial/evidence/2026-09-08-t103-root-fix-manifest.md`를 `git show`로 읽었다.
- 격리: `F:/dev/kor-travel-common-wt/review-t103-root-a`의 detached worktree. 시작·종료 `git rev-parse HEAD HEAD^{tree}`가 위 값과 일치했고 `git status --short`는 비어 있었다. 이후 이 원본만 추가한다.
- 공통 요청: “상태 추정 helper를 상태 스택으로 교체한 전체 delta와 자신의 누적 finding closure를 독립적으로 검사한다.” A 범위는 MDX/JavaScript 문맥 전환, 본문·표현식·ESM·JSX·template 수명, P1 누락·P2 오탐과 좌표 보존이다.
- 이번 상대 raw·결과는 읽거나 요청하지 않았다. 작성자가 전달한 CI 상태와 Airport evidence 오류는 상대 결과가 아니며 직접 확인 후 구분해 기록했다. 후보·manifest·소비자·기존 evidence·git config는 수정하지 않았다.

## 판단과 검증 범위

7파일 delta의 구조 변경, 상세 task의 문맥 표, 누적 자료와 참조 검증기를 대조했다. 상태 추정 helper를 제거한 방향은 기존 문제를 해결했지만, 현재 ESM 종료는 여전히 마지막 토큰의 제한된 목록에 의존한다. JS의 비교 연산자와 JSX 진입도 구분하지 않는다. 아래 정상 MDX 반례의 누락·오탐이 남아 있어 완료 조건을 만족하지 않는다.

| 검증 | 직접 실행 결과 |
|---|---|
| Windows Python 3.14.3 집중 시험 | `python -B -X utf8 -m unittest tests.test_ux_mdx_context tests.test_ux_lint`: 56개 통과, skip 0, 76.551초 |
| WSL Python 3.11 집중 시험 | `bash -lc 'uv run --no-project --python 3.11 python -B -X utf8 -m unittest tests.test_ux_mdx_context tests.test_ux_lint'`: 56개 통과, skip 0, 34.068초 |
| 저장소 참조 대조 | `node tests/verify_mdx_reference.mjs F:/dev/kor-travel-common/.git/codex-audit/mdx-oracle/node_modules/@mdx-js/mdx/index.js`: 고정 3.1.1의 396건 PASS, 호환 문법 2건 NOT_RUN, exit 0 |
| 기존 A 원 반례 | 양 OS 각각 42건 기대 일치, 직접 CLI 4건과 `--base` 9건 기대 일치, traceback 없음 |
| 독립 확장 대조 | 양 OS 각각 90건 전부 참조 MDX parser가 정상 구문으로 인정. 51건 기대 일치·39건 불일치. 마스킹 길이·줄 종결자 위치는 90건 보존 |
| 독립 CLI | 양 OS 각각 7입력×LF/CRLF/CR×plain/base의 42회 실행. 참조 대조의 누락·오탐과 같은 exit·패턴 결과, traceback 없음 |
| 정적 gate | link 503문서·2506대상 오류 0, plan 106 task 오류 0, SPDX 58파일 오류 0, secret/redaction 각 638파일 finding 0, versions self-check PASS, `git diff --check 841ee985 b013ab0` 오류 0 |

전체 317시험은 이번에 직접 재실행하지 않았다. manifest의 작성자 Windows 317 성공·skip 0, WSL 316 성공·skip 1 evidence를 재사용하며 자기 실행으로 집계하지 않는다. 정확한 제품 후보 CI [34214642467](https://github.com/digitie/kor-travel-common/actions/runs/34214642467)은 Windows job 취소로 전체 cancelled다. 별도 manifest HEAD `4ddb9601149a85202486719e7ab16dbb4448b8ac`의 [34214737342](https://github.com/digitie/kor-travel-common/actions/runs/34214737342)는 6 job success를 조회했다. 두 commit의 차이가 manifest 한 파일뿐임을 `git diff --name-only b013ab0 4ddb960`으로 확인했으며 서로 다른 SHA를 같은 CI 실행으로 표기하지 않는다.

WSL 첫 `uv` 호출은 비로그인 PATH에서 찾지 못해 실행되지 않았다. `bash -lc`에서 경로를 확인하고 위 집중·직접 검증을 정상 실행했다. 임시 Python helper 추가 중 PowerShell 인용 오류 1회는 실행 전 발생했고, helper만 올바르게 작성한 뒤 재실행했다. 제품 실패나 시험 통과로 집계하지 않았다.

## 원 finding disposition

- A-P1-31/A-P1-32: URL·wildcard 본문 뒤 P6/P8을 계속 검사한다. 양 OS 원 반례와 CLI/base로 **FIXED**.
- A-P2-33/A-P2-34: default/named export 주석과 빈 줄을 포함한 열린 MDX/import 주석이 제외된다. 양 OS 원 반례와 CLI/base로 **FIXED**. 아래의 괄호 없는 ESM 줄 연속은 다른 미확인 경계로 분리한다.
- A-P1-28/A-P2-29/A-P2-30: 기존 opener·미종결 span·따옴표/주석 반례는 현재 집중 시험과 누적 자료에서 **FIXED**. 모든 과거 임시 확장 스크립트를 이번에 새로 실행한 것은 아니다.

## 신규 finding

### A-P1-35 — P1, OPEN / FIX_REQUIRED: ESM을 줄 끝에서 조기 종료해 실행 template 누락

- 위치: `tools/ux_lint.py:704`–709. 괄호 스택이 비고 마지막 토큰이 목록 밖이면 다음 줄의 연속 구문을 확인하지 않고 ESM frame을 제거한다.
- 최소 재현: 첫 줄 `export const a = true`, 다음 줄은 삼항식의 참 분기로 P8 시험 문자열을 담은 template, 거짓 분기로 빈 문자열을 둔다. 다른 정상 반례는 첫 줄 `export const a = value` 다음 줄의 `.map(x => template)`, 또는 `instanceof` 다음 줄의 tagged template다.
- 기대/실제: 고정 참조 parser는 세 입력을 유효 ESM으로 받아들이며 해당 template는 문서 인용이 아니므로 P8 하나를 남긴다. 후보는 세 입력 모두 관찰 없음·exit 0이다. LF/CRLF/CR의 plain CLI와 `--base`에서 양 OS 동일하다. 같은 종료 원인은 `instanceof` 다음 줄 주석의 P8 오탐도 만든다.
- 원인 경계: 이전 제품 대조에서 삼항·member 연속은 정상 탐지했으므로 신규 회귀다. `instanceof` tagged template 누락은 이전에도 존재했다. 반례를 같은 종료 유형으로 묶되 이 차이를 보존한다.
- 영향·수용 조건: 정상 실행 template의 필수 패턴 검사가 통과해 버린다. JS 연속 구문과 ESM 블록의 수명을 줄별 마지막 토큰 목록으로 결정하지 말고, 세 정상 입력과 주석 대조를 같은 corpus에 넣어 참조 parser·양 OS CLI에서 일치시켜야 한다.

### A-P2-36 — P2, OPEN / FIX_REQUIRED: 비교 연산자의 `<`를 JSX 시작으로 오인

- 위치: `tools/ux_lint.py:687`–691. 현재 JS frame의 operand 상태와 무관하게 `<` 다음 식별자를 JSX tag로 처리한다.
- 최소 재현: `{a<b /* P8 시험 문자열 */}`. 또는 `{a<b}` 뒤 빈 줄과 P8 문자열을 담은 정상 fenced code를 둔다. `{a<b && b>c /* P8 시험 문자열 */}`도 같은 오류다.
- 기대/실제: 참조 parser는 세 입력을 정상 구문으로 인정하고 주석·fence를 제외해 관찰 없음이다. 후보는 P8을 보고하고 exit 1이다. plain/blockquote/nested와 LF/CRLF/CR 매트릭스에서 27건 불일치, plain CLI/base도 양 OS 재현됐다.
- 원인 경계·영향: 이전 제품은 이 세 입력을 정상 제외했다. 이번 구조 변경의 신규 오탐이며 정상 소비자 코드와 문서가 gate에서 실패한다.
- 최소 수정·수용 조건: 비교 연산자와 JSX가 시작할 수 있는 JS 문맥을 구분한다. 비교식 이후 주석·fence와 실제 JSX 양성 대조가 모두 참조 결과와 일치해야 한다.

### A-P1-37 — P1, OPEN / FIX_REQUIRED: Airport dark evidence가 현재 실패를 성공으로 기록

- 위치: `docs/evidence/t103-kt-contrast-ux-lint.md:13`. dark 미달 4건·baseline exit 0으로 남아 있다. 이 파일은 이번 제품 delta에서 변경되지 않은 기존 기록이다.
- 출처·직접 재현: coordinator의 작성자 종료 점검 통보 뒤, 후보에서 `python -B -X utf8 tools/kt_contrast.py packages/tokens/tokens.css packages/tokens/examples/airport-overrides.css --dark --baseline packages/tokens/examples/airport.contrast-baseline.example.json --fail-new --json`을 실행해 **exit 1 / FAIL / 미달 10건 중 예외 4건·신규 6건**을 확인했다.
- 영향·수용 조건: 실행 가능한 현재 예제의 미달을 통과 evidence로 취급하면 검증·감사 계약을 깨뜨린다. 기존 조사 값과 현재 후보 계산 결과를 구분해 evidence·연결된 성공 주장을 정정해야 한다. 숫자를 맞추기 위한 임의 CSS 변경이나 신규 baseline 예외 추가는 권고하지 않는다. 원본·후보 SHA와 실제 exit를 보존한다.

## 재현 자료·한계·종료

자기 helper와 로그는 주 checkout `.git/codex-audit/`의 `t103-root-a-probe.py`, `t103-root-a-oracle.mjs`, `t103-root-a-matrix.py`, `t103-root-a-{win,wsl}-matrix.log`, `t103-root-a-airport.json`이다. Python probe의 24입력 중 7입력이 불일치하며 matrix가 이를 줄바꿈·container로 확장한다. 참조 parser의 AST code/inlineCode 및 실제 comment offset만 가린 결과와 제품을 비교한다.

- Windows 재현: `python -B -X utf8 F:/dev/kor-travel-common/.git/codex-audit/t103-root-a-matrix.py F:/dev/kor-travel-common-wt/review-t103-root-a`.
- WSL 재현: 로그인 bash의 `uv run --no-project --python 3.11 python -B -X utf8 /mnt/f/dev/kor-travel-common/.git/codex-audit/t103-root-a-matrix.py /mnt/f/dev/kor-travel-common-wt/review-t103-root-a`.
- base 대조에는 제품 코드 동일성을 `git diff --quiet 841ee985 7f2ae593 -- tools/ux_lint.py`의 exit 0으로 확인한 자기 이전 격리 트리를 사용했다. 상대 원본을 읽지 않았다.
- `NOT_RUN`: Windows Python 3.11, 이번 직접 전체 317시험, 실제 MDX compile/render/browser, 소비자 build/e2e·버전 검사, npm/PyPI 게시, CI 개별 job 로그 전수 감사. 참조 파서 구문 수용은 런타임 실행 성공을 뜻하지 않는다.
- 신규 P0 0·P1 2·P2 1·P3 0. P1이 열린 상태이므로 **BLOCK**이며, P2도 수정 권고 상태다. 후보는 불변이고 원본 한 파일만 커밋한다. report-only commit·파일 SHA256·커밋 후 clean 상태는 확정 후 완료 메시지로 전달한다.
