# T-102 post-fix 독립 적대적 리뷰 B

- 실행 ID: `T102-POST-B-20260907-234353`.
- 요청: immutable `b864eeb`만 대상으로 초기 B parser/VAR/semicolon/import graph/symlink/read/redaction/weather provenance/README finding과 전체 delta의 CI·package·GPL/docs 회귀를 독립 검토. 후보·소비자 수정/commit/push 금지, reviewer A 결과 열람 금지, Git 환경 상속을 제거한 독립 사본에서 실행.
- 시작 KST: `2026-09-07T23:43:53.0510865+09:00`.
- 검증 종료 KST: `2026-09-07T23:52:34.6499826+09:00`.
- 시작/종료 commit: `b864eeb7feb8124aad40c78719da738939e4dcb7`.
- 시작/종료 tree: `b47be30f88648229485482f37234c5c103da8467`.
- 전체 base: `843c404d79fd748cf6f8e40ce3e385fcabb0179f`; 수리 delta 비교: `8bc8179f728de88fd9327f9d4e8159188a95f9c3` → candidate.
- 격리: `F:/dev/kor-travel-common-wt/review-t102-post-b` detached, 시작/종료 `git status --porcelain=v1` 모두 빈 출력. 전체 unittest·정적 gate는 이 후보를 Windows 임시 디렉터리/WSL `/tmp`로 복사하고 `.git`을 제외한 독립 사본에서 실행했다. 사본 안의 별도 Git index만 초기화했고 자식 환경의 모든 `GIT_*` 변수를 제거했다. package pack/install도 별도 임시 사본만 사용했다.
- source `.git/config` 시작/종료 SHA256: `7689A8DF4F1D9EC7C8E237C66B66BF717375A03E248C050692CB4D4BA25A62CF`로 동일. source 설정·후보·소비자 파일에 쓰지 않았다. 초기 리뷰의 오염 실행은 이번 evidence에 재사용하지 않았다.
- 공통 manifest: `docs/reviews/adversarial/evidence/2026-09-07-t102-post-fix-manifest.md`, 읽은 파일 SHA256 `49CB2FBC3A502DE2123ADB067CE793FFAE6ABDB36AE52BE835DD5764325B35DC`.
- 독립성: reviewer A 원본/판정/후속 결과를 읽지 않았다. CI diff-check 오류에 나타난 상대 원본의 파일명·마지막 빈 행 위치만 확인했다. 해당 본문은 읽지 않았다.

## 판정

**BLOCK**. 기존 8건 중 5건 FIXED, 3건 부분 수정 후 OPEN이다. 새 finding 3건을 포함한 미해결은 P1 3건(B-P1-01/02/09), P2 3건(B-P2-06/10/11)이다. P0/P3 신규 0. 로컬 회귀 성공은 exact 후보의 CI 성공이나 소비자 채택 성공으로 대체하지 않았다.

## 실제 검증

아래 helper는 모두 기본 checkout `.git/codex-audit/`에만 보존한 reviewer 소유 임시 검증 코드다. 후보 파일을 바꾸지 않는다. Windows Python은 `py -3.14 -B -X utf8`, WSL Python은 `/home/digitie/.local/share/uv/python/cpython-3.11-linux-x86_64-gnu/bin/python3.11 -B -X utf8`이며 WSL 배포판은 `Ubuntu-26.04`이다. 아래 `<candidate>`는 해당 OS에서 위 detached 후보의 절대 경로다.

| 명령/검증 | Windows | WSL/Linux |
|---|---|---|
| `review-t102-b-wsl-unittest.py <candidate>` → 독립 사본에서 `-m unittest discover -s tests -p test_*.py` | exit 0, 225 tests, skip 0, 62.743초 | exit 0, 225 수집 중 223 실행 통과·2 skip, 20.054초 |
| `review-t102-post-b-gates.py <candidate>` → focused `test_check_aliases.py` | 22 tests, skip 0, exit 0 | 22 tests, skip 0, exit 0 |
| `tools/validate_plan.py` | 106 tasks, 오류 0 | 동일 |
| `tools/validate_document_links.py` | 370 문서·2333 target, 오류 0 | 동일 |
| `tools/check_spdx.py` | 45 파일, 오류 0 | 동일 |
| `tools/scan_secrets.py --all` | 485 파일, 발견/예외 0 | 동일 |
| `tools/check_prod_redaction.py --all` | 485 파일, 발견/예외 0 | 동일 |
| `tools/check_versions.py --self-check` | exit 0 | exit 0 |
| `tools/check_aliases.py packages/tokens/aliases` | CSS 1개·오류 0, exit 0 | 동일 |
| `review-t102-b-probe.py <candidate>` 기존 27종 CLI corpus | 모두 실행; 기존 기본 실패 입력은 제어된 exit 1, traceback 없음 | 동일; chmod 읽기 거부도 exit 1 |
| `review-t102-post-b-probe.py <candidate>` 보강 11종 | 아래 반례와 정상 대조 재현 | 동일 |
| `review-t102-post-b-redaction.py <candidate>` 2종 | 두 출력에서 정책 `GITHUB-TOKEN` 일치 | 동일 |
| `review-t102-post-b-short.py <candidate>` | GetShortPathNameW 동일 디렉터리 long exit 0, short exit 1 | Windows API 전용 |
| `node review-t102-post-b-css.cjs` | headless Chromium CSSOM·computed value 확인 | 별도 브라우저 실행 NOT_RUN |

- 정상 대조: 양 모드 문자열 `"var(--kt-missing)"`, 주석 속 가짜 정의는 exit 0. 양 모드 `VAR(--kt-missing)`와 마지막 세미콜론 없는 금지 정의는 exit 1로 올바르게 수정됐다.
- 기존 corpus: one-line/url/media import, import helper의 금지 정의·중복, 누락 dark·빈 alias·root/dark drift, 외부/자기 symlink·필수 tokens 외부 symlink, UTF-8 읽기 실패, 누락 경로·외부 import·값 drift 민감 marker를 확인했다. Windows chmod(0)는 ACL 읽기 거부 재현이 아니므로 그 한 사례를 읽기 거부 검증 성공으로 세지 않았다.
- Windows Node `25.9.0`/npm `11.12.1`, WSL Node `22.22.2`/npm `11.19.1`에서 `review-t101-b-pack.py <candidate>`를 실행했다. `npm ci --ignore-scripts --no-audit --no-fund`, build 전 check, build, check, 7개 Node tests, `npm pack`, 빈 프로젝트의 tgz install, concrete exports 14개 resolve와 tokenValues 44개 import가 모두 성공했다. Windows는 프로젝트 Node engine 밖이어서 EBADENGINE 경고가 있었으며 정본 Node 실행과 같다고 주장하지 않는다.
- 양 tarball은 19개 파일, alias CSS 포함·examples 없음·LICENSE/NOTICE/THIRD_PARTY_NOTICES 포함, LICENSE bytes는 후보 root LICENSE와 일치. tarball SHA256은 Windows `5187b2bf7e703aa7dc58135c11fe515d80d9b238119938283dc42bef2fd0c781`, WSL `d92e86bd46db2b739add5138eefaee18c59cec25a43ba117fbc13f53d4dc43b1`이다. 서로 다른 npm 환경의 동일 바이트를 주장하지 않는다. tgz는 임시 설치 검증 뒤 제거됐으며 발행 자산이 아니다.
- helper의 추가 drift 주입은 build 전 check exit 1을 확인했다. 이후 build/check/test exit 0은 생성물 복구 동작이며 CI 전체 성공으로 해석하지 않았다. 실제 workflow는 build 전에 check하고 빌드 뒤 tracked diff도 검사한다.
- `git diff --check 843c404d79fd748cf6f8e40ce3e385fcabb0179f b864eeb7feb8124aad40c78719da738939e4dcb7` 실패: B-P2-11.
- exact CI: `gh run view 34134500500 --json headSha,status,conclusion,jobs`의 headSha는 후보와 동일, conclusion은 failure. `secret-scan`, `tools (ubuntu-24.04)`, `packages`, `check-versions` 성공; `docs`, `tools (windows-2025)` 실패. `gh run view 34134500500 --log-failed`의 실패 부분을 직접 확인했다. Windows 14 failures·2 skips, docs 공백 검사 실패를 분리했다.
- workflow 전체 base delta는 tools job의 alias checker 호출 1행이며 SHA 고정 checkout/source assertion, 권한, build 전 check, tarball smoke는 유지된다. npm package files/exports에 alias 추가, examples는 제외되어 no-publish/소비자 쓰기 금지 경계에 새 누출은 확인되지 않았다.
- weather 원천 `6003da995fa4b35799f9dadc406c6ba2878bfbae:packages/kor-travel-weather-admin/frontend/app/tokens.css`를 소비자 Git object에서 읽기 전용으로 재확인했다. PV-014·Origin·Modified·예제 README 고정 원천 경로가 일치한다. task는 READY이고 실제 6폭 소비자 diff를 T-461 NOT_RUN으로 남긴다.

## 기존 finding disposition

| 원 ID / 심각도 | 판정 | 근거 |
|---|---|---|
| B-P1-01 / P1 | 부분 수정, OPEN | 마지막 세미콜론·대문자 VAR·문자열/주석 반례는 FIXED. CSS escape 식별자·함수는 여전히 금지 정의/미정의 참조 false PASS. 아래 상세 |
| B-P1-02 / P1 | 부분 수정, OPEN | 일반 one-line/url/media/복수 import는 FIXED. escaped at-keyword로 외부 import 검사 전체를 우회 |
| B-P1-03 / P1 | FIXED | 재귀 helper의 금지 --kt·theme 충돌·shadcn 중복·alias drift를 검사; canonical shadcn만 예외. escape 문제는 B-P1-01/02로 기록 |
| B-P2-04 / P2 | FIXED | 필수 tokens의 외부 symlink와 self loop가 양 OS 제어 오류 |
| B-P2-05 / P2 | FIXED | UTF-8 오류·alias self loop·누락·외부 경로에서 traceback 없음; Linux 읽기 거부도 제어 오류. Windows ACL 사례는 NOT_RUN |
| B-P2-06 / P2 | 부분 수정, OPEN | 외부 절대 경로·값 drift 원문은 숨김. 패키지 안 상대 import target 및 property/reference 이름에 포함된 민감 패턴은 그대로 stdout에 노출 |
| B-P1-07 / P1 | FIXED | weather 예제 SPDX/Origin/Modified, PV-014 및 고정 source 경로·commit과 비배포 설명 확인 |
| B-P3-08 / P3 | FIXED | 패키지 README가 실제 aliases 포함 상태·예제 비배포 경계와 일치 |

## 미해결 상세

### B-P1-01 — CSS escape를 사용한 금지 정의·미정의 var가 PASS

- 위치: `tools/check_aliases.py:15`, `:16`, `:320`, `:433`.
- 최소 입력: 정상 `tokens.css`의 `--kt-brand:red`와 필수 theme/shadcn fixture를 둔 뒤 alias에 아래 두 모드를 둔다.

```css
:root { --brand: var(--kt-brand); --\6b t-brand: blue; }
.dark { --brand: var(--kt-brand); --\6b t-brand: blue; }
```

- 명령: `python -B -X utf8 tools/check_aliases.py <fixture>/tokens/aliases` 또는 `review-t102-post-b-probe.py <candidate>`의 `escaped_property`.
- 결과: 양 OS exit 0, `CSS 1개, 오류 0개`. Chromium computed `--kt-brand`는 blue로 실제 정본 토큰을 덮어쓴다.
- 추가 최소 입력: 양 모드 `--brand: v\61r(--kt-missing)`도 exit 0. Chromium은 escaped 함수명을 실제 var로 해석한다. ASCII regex가 escape 식별자를 조용히 누락한다.
- 영향: T-102의 모든 var 대상·금지 --kt 정의 검증과 merge 차단 약속을 우회한다. 단순 표기 차이를 보증 범위 밖으로 문서화하지도 않는다.
- 권고: CSS identifier/function escape를 정확히 tokenize/decode하거나 지원하지 않는 escape가 구조 토큰에 나타나면 fail closed. escaped definition/function/reference 정상·음성 fixture를 함께 고정할 것. 원 P1 유지, 수정 필요.

### B-P1-02 — escaped import가 패키지 경계 검사에 들어오지 않음

- 위치: `tools/check_aliases.py:237`, `:410` 부근 `_collect`.
- 최소 입력: `@\69mport "../../outside.css";` 뒤 줄바꿈을 넣고 정상 :root/.dark 두 블록을 둔다. fixture 밖 파일의 존재 여부와 관계없이 checker는 해당 import를 수집하지 않는다.
- 명령: `review-t102-post-b-probe.py <candidate>`의 `escaped_import`.
- 결과: 양 OS exit 0, 오류 0. 브라우저는 escaped import에서 CSSImportRule 1개를 생성한다. 브라우저 시험은 모든 요청을 abort하여 실제 외부 요청은 하지 않았다.
- 영향: package outside import 차단 및 recursive helper 검사 전체를 우회한다.
- 권고: at-keyword escape를 CSS 규칙대로 해석하거나 명시적으로 제어 오류 처리. 일반 문자열 내부의 escape와 혼동하지 않는 fixture가 필요하다. 원 P1 유지, 수정 필요.

### B-P2-06 — 상대 import/identifier 진단은 민감 입력을 재출력

- 위치: `tools/check_aliases.py:385`, `:501`, `:506`, `:517`.
- 최소 재현: runtime에서 `marker = 'gh' + 'p_' + 'Q' * 36`으로 합성한다. `@import "./" + marker + ".css"`가 가리키는 파일은 만들지 않는다. 또는 alias에 `--kt-` + marker를 property 이름으로 선언한다. 원문 합성 값은 이 보고서/도구 출력에 보존하지 않았다.
- 명령: `review-t102-post-b-redaction.py <candidate>`.
- 결과: 두 OS 모두 두 경우 exit 1, traceback 없음이지만 `marker_exposed=true`; stdout을 후보 `.secret-scan-patterns`로 대조하면 `GITHUB-TOKEN` 일치. import는 `aliases/<marker>.css`를, property는 이름을 그대로 출력한다.
- 영향: CI가 이미 민감한 변경을 차단하더라도 별도 job/CLI가 입력을 로그에 재전송한다. 현재 추가 시험은 패키지 밖 import target만 확인하여 패키지 안 경로 노출을 놓친다.
- 권고: relative path·property/reference 이름도 입력 데이터로 취급하고, 필요한 위치는 안전한 위치 ID/행 번호로 표시하거나 선택 정책으로 가린 후 출력한다. 원 P2 유지, 수정 필요.

### B-P1-09 — 정상 Windows 8.3 경로를 외부 경로처럼 거부하여 필수 CI 실패

- 위치: `tools/check_aliases.py:358`–`381`, `:448`.
- 최소 재현: 정상 fixture alias 디렉터리의 `GetShortPathNameW` 결과를 CLI 인수로 준다. `Path(short).samefile(long)`은 true이며 파일 내용은 동일하다.
- 명령: Windows `py -3.14 -B -X utf8 .git/codex-audit/review-t102-post-b-short.py <candidate>`.
- 결과: long path exit 0; short path exit 1, `별칭 경로를 읽을 수 없음`. `_safe_real`이 resolve 후 long 경로를 resolve 전 root 문자열과 비교한다.
- 원격 근거: [exact Windows job](https://github.com/digitie/kor-travel-common/actions/runs/34134500500/job/101782212673)의 alias test 14 failures. 정상 fixture도 같은 generic 경로 오류를 반환한다. 원격 path alias 원인을 직접 로그가 전부 노출한 것은 아니지만, 동일 제어 흐름의 독립 Windows 최소 반례가 이를 재현한다.
- 영향: T-102 Windows/Linux 동일 결과 수용 기준 및 필수 Windows 도구 job을 충족하지 못한다.
- 권고: root를 한 번 안전하게 canonicalize하고 경계 비교는 동일 표현의 canonical path끼리 수행하되 lexical traversal/외부 symlink 검사는 유지한다. 8.3 alias를 fixture에서 실제 생성해 회귀 시험한다. P1, 수정 필요.

### B-P2-10 — root/dark 합동 selector를 단일 모드로 잘못 판정

- 위치: `tools/check_aliases.py:116`–`124`, `:513`–`525`.
- 최소 입력: `:root, .dark { --brand: var(--kt-brand); }`.
- 명령: `review-t102-post-b-probe.py <candidate>`의 `combined_modes`.
- 결과: 양 OS exit 1, `별칭 :root 블록이 없음`/`:root 선언 누락`. 브라우저는 root에 정상 값을 적용한다. 동일 선언이 두 selector에 적용되지만 `_scope`가 `.dark`를 먼저 찾고 단일 문자열만 반환한다.
- 영향: root/dark 값이 같은 정상 CSS를 검사가 거부한다. 현재 도구가 필요한 mode 집합과 CSS의 실제 적용 범위를 혼동한다.
- 권고: selector별 scope 집합을 반환하거나 지원 문법을 명확하게 제한하고 그 제한을 task/tool 계약에 합의해야 한다. 두 selector·개별 selector를 동일 의미로 확인할 회귀 필요. P2, 수정 필요.

### B-P2-11 — archival evidence 마지막 빈 줄이 exact CI 공백 gate를 실패시킴

- 위치: `docs/reviews/adversarial/evidence/2026-09-07-t102-initial-reviewer-a.md:118` (본문 미열람, diff-check 위치만 확인).
- 명령: `git diff --check <base> <candidate>` 및 `gh run view 34134500500 --log-failed`.
- 결과: `new blank line at EOF`; [exact docs job](https://github.com/digitie/kor-travel-common/actions/runs/34134500500/job/101782212667) 공백 step exit 2. Windows failure와 별개다.
- 영향: 필수 CI가 실패한 후보를 PASS/merge 가능으로 표시할 수 없다.
- 권고: 이미 확정한 raw bytes/hash를 보존할 필요가 있으면 해당 raw 한 파일에만 최소 whitespace attribute 예외를 적용하고 수정 SHA에서 diff check/CI를 재실행한다. 넓은 path 전체 whitespace 검사 제외는 피한다. 후보에는 그 후속 수정이 없으므로 P2 OPEN이다.

## 한계와 NOT_RUN

- WSL 두 jsonschema parity test: `NOT_RUN(jsonschema 미설치)`. 225 전부 통과로 세지 않았다. Windows 225에는 skip이 없다.
- Windows 실제 ACL 읽기 거부: `NOT_RUN(chmod는 동일 의미가 아님)`; 양 OS UTF-8/self-loop/누락 읽기 경계와 Linux 권한 거부는 실행했다.
- 별도 Linux Chromium 시각/계산 시험: `NOT_RUN`; CSS 해석 근거는 Windows Chromium 직접 실행이며 checker는 양 OS 재현했다.
- 소비자 build/e2e/6폭 visual diff: `NOT_RUN(T-461 등 소비자 이관 task, 이번 common review 범위 밖)`. 원천 Git object 읽기 외 소비자 접근·쓰기 없음.
- npm/PyPI 게시·Release·tag·소비자 설치: `NOT_RUN(요청 범위 밖)`. 임시 common tarball 설치만 수행했다.
- CI rerun·후속 commit·상대 reviewer 판정은 이번 리뷰에 포함하지 않았다. 부모의 수정 예정 안내를 실제 수정 evidence로 세지 않았다.
- helper 생성 첫 시도의 PowerShell quoting 오류, WSL PATH 문자열 구문 오류, unquoted `HEAD^{tree}` 명령 오류는 검증 성공으로 세지 않았다. 수정한 helper와 명시적으로 인용한 Git 명령의 성공 결과만 위에 기록했다. 후보 및 source config는 보존됐다.

최종 결론: 위 6개 미해결 finding을 수정한 새 immutable 후보에 대한 두 독립 reviewer 재검토와 exact CI 성공이 필요하다. 이 원본은 b864eeb에만 귀속한다.
