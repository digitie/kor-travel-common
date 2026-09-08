# T-103 수정 후 36차 독립 리뷰 A 원본

- 실행 ID: `T103-POST36-A-20260908-184720-KST`; 최종 판정: **NO-GO**.
- 검토 시작: 2026-09-08 18:47:20.898 KST; 제품 검토 종료: 2026-09-08 18:55:59.791 KST.
- 불변 제품 후보: `d8027917e4cb88b72d5d5c98d571ef3522e808c8`; tree: `3e9d2614629eafddd8b2cf126d9e8234d1ab48c8`.
- 수정 대조 기준: `aedfdd659255c27bcc4377bd15b39452c004417d`. manifest는 별도 commit `36f08f2`의 `docs/reviews/adversarial/evidence/2026-09-08-t103-post-fix-36-manifest.md`를 `git show`로 확인했다.
- 격리 경로: `F:/dev/kor-travel-common-wt/review-t103-post36-a`. 시작·제품 검토 종료의 HEAD/tree는 위 값과 같고 `git status --short` 출력은 모두 비어 있었다. 이후 이 원본 파일만 추가한다.
- 요청: 같은 후보에서 일반 문장·fenced MDX·따옴표·중괄호 표현식의 주석·줄바꿈·diff 동작을 독립 검증하고, 후보를 수정하지 않은 채 보고서 한 파일만 커밋한다.
- 독립성: 상대 원본과 post-35 원본을 열람하지 않았다. 자기 fixture 작성·실행 뒤 coordinator가 요청하지 않은 상대 결과 요약을 전송했다. 그 경로를 추가 검증에 채택하지 않았으나, 완전한 결과 비공개 조건이 유지되지는 않았음을 기록한다.

## 검토 범위와 실행 결과

제품 변경인 `tools/ux_lint.py`와 `tests/test_ux_lint.py`의 전체 delta를 읽었다. 나머지 변경은 이전 manifest와 A/B 기록이며 상대 원본 본문은 읽지 않았다. 변경 없는 task·정본의 기존 확인은 재사용했고, 현재 문법 처리와 주석 제외 계약의 일치를 직접 확인했다. 후보·소비자·기존 evidence·git config는 수정하지 않았다. 임시 fixture와 실행 로그는 후보 트리 밖의 자기 audit 경로에 두었다.

| 검증 | Windows Python 3.14.3 | WSL Python 3.11.15 |
|---|---|---|
| 전체 unittest | 314개 통과, skip 0, 332.393초 | 314개 실행 중 313개 통과·Windows 전용 8.3 검사 1개 skip, 123.355초 |
| contrast·UX 집중 unittest | 76개 통과, 163.136초 | 76개 통과, 60.915초 |
| link / plan / SPDX | 499문서·2496대상 / 106 task / 56파일, 오류 0 | 동일 결과 |
| secret / 운영값 redaction / versions self-check | 631파일·finding 0 / 631파일·finding 0 / 성공 | 동일 결과 |
| alias / contrast / UX fixture | CSS 1개·오류 0 / light 27쌍 통과 / 12개 관찰·fail 0 | 동일 결과 |
| 수정 delta `git diff --check` | 오류 0 | 오류 0 |

- 전체 명령: Windows `python -B -X utf8 -m unittest discover -s tests -p 'test_*.py' -v`; WSL `uv run --no-project --python 3.11 --with jsonschema python -B -X utf8 -m unittest discover -s tests`.
- 집중 명령: 각 런타임의 `python -B -X utf8 -m unittest tests.test_kt_contrast tests.test_ux_lint`. Windows TEMP/TMP와 WSL TMPDIR는 자기 임시 경로로 분리했다.
- 정적 gate는 manifest의 link·plan·SPDX·secret·redaction·versions·alias·contrast·UX·diff 명령을 실행했다. 로그: 주 checkout `.git/codex-audit/t103-post36-{win,wsl}-gate-{0..10}-a.log`.
- 기존 직접 corpus는 양 OS에서 360·504·324·36개 매트릭스가 각각 전부 기대와 일치했다. 이전 최소 `--base` 대조 3·9·6개도 모두 기대와 일치했다. 현재 URL·apostrophe·따옴표 원 반례는 수정됐다.
- 새 문법 매트릭스는 양 OS 각각 42개 중 24개 기대 일치, 아래 18개 불일치였다. 직접 CLI 4개와 최소 `--base` 9개도 실행했고 traceback은 없었다.
- 직접 재현 명령: Windows `python -B -X utf8 F:/dev/kor-travel-common/.git/codex-audit/t103-post36-syntax-a.py F:/dev/kor-travel-common-wt/review-t103-post36-a`; 같은 인수의 `t103-post36-base-a.py`. WSL에서는 `/mnt/f/` 경로와 위 uv Python 3.11을 사용했다. fixture는 임시 파일을 바이트로 써서 LF·CRLF·CR를 보존하고, CLI `--root <fixture> --fail-new --json` 및 임시 Git 기준 commit의 `--base <SHA> --json`을 실행한다.
- 현재 로그: `.git/codex-audit/t103-post36-{win,wsl}-7-a.log`, `t103-post36-{win,wsl}-base-a.log`. 이전 제품 대조는 같은 자기 fixture로 실행했으며 `t103-post36-win-before-a.log`에 보존했다.
- 정확한 후보 CI는 `gh run list --commit d8027917e4cb88b72d5d5c98d571ef3522e808c8 --json databaseId,headSha,status,conclusion,url --limit 5`로 조회했다. [run 34211197016](https://github.com/digitie/kor-travel-common/actions/runs/34211197016)의 head 일치·completed/success를 확인했다. 로컬 결과와 CI 결과를 구분한다.

## Finding과 수용 조건

### A-P1-32 — P1, OPEN / FIX_REQUIRED: 일반 본문의 wildcard를 JS 블록 주석으로 처리

- 위치: `tools/ux_lint.py:1054`의 slash-star 주석 진입 분기(1054–1058). 줄 주석과 달리 실제 MDX/JS 문맥 검사가 없다.
- 최소 재현: `prose_glob` fixture. 일반 설명 뒤 1자 backtick과 `src/*`를 두고 같은 줄에 P6 JSX 및 P8 표현식, 다음 줄에는 tilde fence와 이후 backtick을 둔다. 실제 JS 주석을 시작한 문맥은 아니다.
- 기대/실제: LF·CRLF·CR 각각 P6/P8 관찰·exit 1이어야 하지만 관찰 없음·exit 0이다. plain CLI와 `--base` 모두 양 OS에서 재현했다. 이 3개가 새 매트릭스의 실패다.
- 영향·원인 경계: 본문 wildcard 뒤 검사 대상이 누락된다. 이전 제품도 같은 입력에서 실패했으므로 이번 수정의 신규 회귀가 아닌 별도 기존 경계다. URL 원 반례 A-P1-31과 구분한다.
- 최소 수정·수용 조건: 블록 주석도 실제 MDX/JS 문맥에서만 가리고, 일반 wildcard 뒤 P6/P8은 유지한다. 실제 표현식·JSX·ESM 주석 음성 대조는 계속 통과해야 한다.

### A-P2-33 — P2, OPEN / FIX_REQUIRED: 정상 default·named export의 줄 주석을 검사

- 위치: `tools/ux_lint.py:728`의 `_is_mdx_lexical_code`(728–746)와 1047–1053의 줄 주석 조건.
- 최소 재현: `export default Layout`, `export default () => null`, `export { value } from "./module.js";` 뒤의 줄 주석에 P8 시험 문자열을 넣는다. 시험 문자열은 실행식이 아니라 주석 내용이다.
- 기대/실제: 세 export 형식과 세 줄바꿈의 9개 모두 기대 관찰 없음·exit 0이나 실제 P8 관찰·exit 1이다. default 형식의 `--base`도 양 OS 세 줄바꿈에서 동일하다. `export const` 주석 대조는 정상 제외된다.
- 영향·원인 경계: 정상 MDX ESM이 fail-new에서 실패한다. 이전 제품은 이 9개를 정상 제외했으므로 lexical guard 도입에 따른 신규 회귀다.
- 최소 수정·수용 조건: 유효한 ESM default·named export의 문맥과 주석을 처리하고, 일반 문장을 ESM으로 취급하지 않는 양성·음성 대조를 유지한다.

### A-P2-34 — P2, OPEN / FIX_REQUIRED: 빈 줄이 열린 MDX·import 문맥을 끊음

- 위치: `tools/ux_lint.py:658`의 `_has_open_mdx_expression`이 661행에서 문단 시작을 사용하는 경계와 728–746·1047–1053의 lexical guard.
- 최소 재현: 열린 MDX 괄호 표현식 또는 여러 줄 named import 안에 빈 줄을 넣고, 그 다음 식별자 줄의 줄 주석에 P8 시험 문자열을 넣은 뒤 표현식·import를 닫는다.
- 기대/실제: 두 형식과 LF·CRLF·CR의 6개 모두 기대 관찰 없음·exit 0이나 실제 P8 관찰·exit 1이다. 표현식의 `--base`도 양 OS 세 줄바꿈에서 재현했다. 빈 줄 없는 동일 표현식·import와 JSX prop 대조는 정상이다.
- 영향·원인 경계: 합법적인 여러 줄 문법의 주석이 신규 위반으로 오탐된다. 이전 제품은 같은 6개를 통과해 이번 변경의 신규 회귀로 판정한다.
- 최소 수정·수용 조건: 열린 JS/MDX 표현식·선언의 수명은 일반 Markdown 빈 문단과 구분한다. 실제 닫힘까지 주석 상태를 보존하고, 닫힌 뒤 일반 본문은 정상 검사해야 한다.

## Disposition과 한계

- 기존 A-P1-28, A-P2-29, A-P2-30, A-P1-31: 원 반례 범위 **FIXED**. 새 wildcard 경계를 기존 URL finding의 수정 실패로 소급하지 않았다.
- 새 P0 0개, P1 1개(A-P1-32), P2 2개(A-P2-33/34), P3 0개. 세 건 모두 수정과 새 후보 재검증이 필요해 **NO-GO**로 확정한다.
- `NOT_RUN`: Windows Python 3.11(실행 파일 없음), 실제 MDX 컴파일러·브라우저 실행, 소비자 build/e2e·manifest 실측, registry 설치·게시, workflow dispatch, CI 개별 job 로그 감사. 변경 없는 모든 과거 독립 corpus를 새로 전수 실행하지는 않았으며 이번 직접 재현과 checked-in full/focused 회귀를 구분했다.
- 후보 코드·manifest·소비자·기존 evidence와 source `.git/config`는 불변이다. 원본 파일의 SHA256·report-only commit SHA 및 커밋 후 clean 상태는 파일을 확정한 뒤 별도 완료 메시지로 전달한다.
