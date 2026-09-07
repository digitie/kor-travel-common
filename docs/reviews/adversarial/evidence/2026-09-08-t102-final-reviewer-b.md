# T-102 final 독립 적대적 리뷰 B

- 실행 ID: `T102-FINAL-B-20260908-000607`.
- 전달 요청: 최종 후보 `09162025140991d24775abc76571f35de9974022`(tree `db7e673bbd56191cdd2afdded75fba670e74c6c5`)에서 공통 manifest와 구현을 읽고 이전 B parser/import escape·redaction·Windows 8.3·combined selector·raw evidence 및 전체 delta를 재현. detached clean에서 읽기/시험만 수행하고 후보·소비자 파일 수정 및 commit/push 금지. reviewer A 결과 미열람. 원본과 SHA256·PASS/BLOCK 보고.
- 시작 KST: `2026-09-08T00:06:07.3336198+09:00`.
- 검증 종료 KST: `2026-09-08T00:10:06.1128266+09:00`.
- 시작/종료 SHA: `09162025140991d24775abc76571f35de9974022`.
- 시작/종료 tree: `db7e673bbd56191cdd2afdded75fba670e74c6c5`.
- 전체 base: `843c404d79fd748cf6f8e40ce3e385fcabb0179f`. 직전 B 기준 `b864eeb7feb8124aad40c78719da738939e4dcb7`에서 10파일 delta를 검토했다.
- 격리: `F:/dev/kor-travel-common-wt/review-t102-final-b`, 새 detached worktree. 시작/종료 `git status --porcelain=v1` 빈 출력.
- 전체 unittest와 정적 gate는 후보를 Windows 임시 디렉터리 및 WSL `/tmp`의 독립 사본으로 복사하고 모든 `GIT_*` 환경 변수를 제거하여 실행. 사본 `.git`만 초기화/index 작성했다. source config·후보 파일·소비자 파일 수정 없음. pack/install도 별도 임시 사본만 사용했다.
- source `.git/config` 시작/종료 SHA256: `7689A8DF4F1D9EC7C8E237C66B66BF717375A03E248C050692CB4D4BA25A62CF`로 동일.
- 공통 manifest: `docs/reviews/adversarial/evidence/2026-09-08-t102-final-manifest.md`; 읽은 파일 SHA256 `0501E2045DA888B4A317A10A4794782EF8ABF3BB675BC2F072CEC93D51BBCB2E`.
- 독립성: A 보고서 본문·판정은 열람하지 않았다. manifest의 해시 보존 확인을 위해 과거 raw 네 파일은 Git blob/파일 바이트의 SHA256만 계산했고 본문은 표시하거나 해석하지 않았다.

## 최종 판정

**BLOCK**. 이전 B 최소 반례 11건의 재현은 FIXED다. 다만 같은 검증 계약에서 신규 P1 2건(B-P1-12, B-P1-14), P2 1건(B-P2-13)을 양 OS에서 독립 재현했다. 신규 P0/P3 0. exact CI 성공은 확인했지만 이 반례의 계약 위반까지 해소했다는 뜻은 아니다.

## 실제 검증과 결과

검증 helper는 기본 checkout `.git/codex-audit/`에만 보존했으며 후보 파일을 수정하지 않는다. `<candidate>`는 위 detached 후보의 해당 OS 절대 경로다. Windows 명령 접두사는 `py -3.14 -B -X utf8`, WSL은 `wsl -d Ubuntu-26.04 -- bash -lc` 내부 `/home/digitie/.local/share/uv/python/cpython-3.11-linux-x86_64-gnu/bin/python3.11 -B -X utf8`다.

| 명령 | Windows | WSL |
|---|---|---|
| `review-t102-b-wsl-unittest.py <candidate>` → 독립 사본에서 `-m unittest discover -s tests -p test_*.py` | exit 0, 234 tests, skip 0, 66.110초 | exit 0, 234 수집 중 231 통과·3 skip, 17.409초 |
| `review-t102-post-b-gates.py <candidate>` → focused `test_check_aliases.py` | 31 tests 통과, skip 0 | 30 통과·Windows 전용 1 skip |
| `tools/validate_plan.py` | 106 tasks, 오류 0 | 동일 |
| `tools/validate_document_links.py` | 373 문서·2333 target, 오류 0 | 동일 |
| `tools/check_spdx.py` | 45 파일, 오류 0 | 동일 |
| `tools/scan_secrets.py --all` | 488 파일, 발견/예외 0 | 동일 |
| `tools/check_prod_redaction.py --all` | 488 파일, 발견/예외 0 | 동일 |
| `tools/check_versions.py --self-check` | exit 0 | 동일 |
| `tools/check_aliases.py packages/tokens/aliases` | CSS 1개, 오류 0, exit 0 | 동일 |
| `review-t102-b-probe.py <candidate>` | 이전 27종 실행 | 동일 |
| `review-t102-post-b-probe.py <candidate>` | 이전 보강 11종 실행 | 동일 |
| `review-t102-post-b-redaction.py <candidate>` | 두 합성 민감 패턴 모두 출력 미노출 | 동일 |
| `review-t102-post-b-short.py <candidate>` | 실제 8.3 경로 생성·samefile true, long/short 모두 exit 0 | OS 전용이므로 해당 없음 |
| `review-t102-final-b-probe.py <candidate>` | 새 경계 11종 실행, 아래 finding 재현 | 동일 |
| `node review-t102-final-b-css.cjs` | Chromium에서 실제 CSS 의미 확인 | 별도 브라우저 NOT_RUN |

- 이전 정상 대조 문자열/주석 속 var는 exit 0, uppercase VAR 미정의 및 마지막 세미콜론 없는 금지 정의는 exit 1이다. escaped property/reference/function/import는 명시적 지원 불가 오류 exit 1이다. 주석 속 backslash와 minified 정상 import는 exit 0이다.
- 기존 import helper 금지 정의·theme/shadcn 중복·외부/자기 symlink·필수 tokens 탈출·UTF-8/누락/read failure는 제어 오류이며 traceback/marker 노출 없음. Windows chmod(0)는 ACL 거부와 같지 않아 권한 거부 검증 성공으로 세지 않았다. Linux chmod 거부는 exit 1이었다.
- `review-t101-b-pack.py <candidate>`: 양 OS `npm ci --ignore-scripts --no-audit --no-fund`, build 전 check → build → check, Node tests 7개, pack, 빈 프로젝트의 tgz install, concrete exports 14개 resolve·tokenValues 44개 import 모두 성공. helper의 별도 drift 주입은 build 전 check exit 1이었다.
- Windows Node 25.9.0/npm 11.12.1은 engine 경고가 있는 추가 실행이며 정본 Node 보증으로 세지 않는다. WSL Node 22.22.2/npm 11.19.1에서 실행했다.
- 양 tarball은 19 파일, alias 포함·examples 제외·GPL LICENSE/NOTICE/THIRD_PARTY_NOTICES 포함. LICENSE bytes는 후보 root LICENSE와 일치. Windows tgz SHA256 `725fd590b9bcbd361b9a798aaa99187cf86812ecba64004e110adeee9686c409`, WSL `4a6cde260c32248d10a6bfc51fe6e14e265c6295bb8967fa5cda2024a17a487a`. 임시 설치 후 제거했으며 발행 자산이 아니다.
- `git diff --check 843c404d79fd748cf6f8e40ce3e385fcabb0179f HEAD`: exit 0.
- `gh run view 34136465020 --json headSha,status,conclusion,jobs`: head SHA가 정확히 후보, completed/success. [exact CI](https://github.com/digitie/kor-travel-common/actions/runs/34136465020)의 `docs`, `tools (windows-2025)`, `tools (ubuntu-24.04)`, `secret-scan`, `check-versions`, `packages` 6 job 모두 성공을 직접 확인했다. 다른 SHA의 CI를 합치지 않았다.
- 직전 후보 대비 workflow·package.json·versions·PROVENANCE·package 고지는 불변이다. 현재 코드 delta는 checker·회귀 시험이며 CSS alias radius와 비배포 weather 예제 변경, task/예제 문서, raw 보존/manifest를 검토했다.
- weather 원천 고정 Git object `6003da995fa4b35799f9dadc406c6ba2878bfbae:packages/kor-travel-weather-admin/frontend/app/tokens.css`의 radius-md panel 및 단일 light shadow 선언을 읽기 전용으로 확인했다. 예제의 panel 재선언·dark light-shadow 보존과 일치한다. PV-014/Origin 고지는 유지되며 소비자 시각 검증은 T-461 NOT_RUN이다.
- raw SHA 보존은 `review-t102-final-b-hashes.py <candidate>`로 Git blob과 checkout 파일을 해시했다. manifest의 초기 A/B·post-fix A/B 네 SHA와 전부 일치. 새 attribute는 지정 raw 파일에만 적용되고 `tools/check_aliases.py`에는 whitespace 예외가 없다. 제품 파일 전체를 공백 검사에서 제외하지 않는다.

## 이전 B finding disposition

| 원 ID / 심각도 | 판정 | 실제 근거 |
|---|---|---|
| B-P1-01 / P1 | 이전 반례 FIXED | 세미콜론/VAR/문자열/주석·escape 정의/함수/참조 재현. 별도 신규 Unicode 경계는 B-P1-14 |
| B-P1-02 / P1 | FIXED | escaped import·url/media/one-line/복수 import와 외부 경계 재현 |
| B-P1-03 / P1 | FIXED | 비정본 재귀 helper 금지 정의·중복 정책 유지. 신규 both 중복 집계는 B-P2-13 |
| B-P2-04 / P2 | FIXED | 필수 tokens 외부/self symlink 거부 유지 |
| B-P2-05 / P2 | FIXED | alias UTF-8/self/누락/read failure 제어 오류; OS 권한 한계 별도 |
| B-P2-06 / P2 | FIXED | 상대 import 및 identifier의 합성 민감 패턴 stdout/stderr 미노출 |
| B-P1-07 / P1 | FIXED | 고정 weather Origin/PV-014/Modified/비배포 고지 유지 |
| B-P3-08 / P3 | FIXED | packaged README aliases 설명 유지·tarball 실제 확인 |
| B-P1-09 / P1 | FIXED | 실제 Windows 8.3 동일 디렉터리 long/short 모두 성공, exact Windows CI 성공 |
| B-P2-10 / P2 | FIXED | `:root,.dark` 정상 CSS가 양 OS exit 0 |
| B-P2-11 / P2 | FIXED | raw 해시 보존과 지정 attribute 확인, diff-check·exact docs CI 성공 |

## 신규 finding

### B-P1-12 — 상위 조건·중첩 selector를 무시하여 선언이 적용되지 않아도 두 mode PASS

- 위치: `tools/check_aliases.py:116`–`135`, 특히 `:119`–`125`; manifest의 직접 selector만 인정하고 후손·조건부를 fail closed 한다는 수정 기준.
- 최소 입력:

```css
@media (max-width: 1px) {
  :root { --brand: var(--kt-brand); }
  .dark { --brand: var(--kt-brand); }
}
```

- 정상 필수 tokens/theme/shadcn fixture를 둔 뒤 `python -B -X utf8 tools/check_aliases.py <fixture>/tokens/aliases` 실행. `review-t102-final-b-probe.py`의 `conditional_media`, `conditional_supports`, `nested_selector`가 이를 보존한다.
- 실제 결과: 세 경우 양 OS 모두 exit 0, `CSS 1개, 오류 0개`. `@supports (display: impossible)` 및 `.shell { :root ... .dark ... }`도 동일하다.
- Chromium 직접 대조: 정상 뷰포트의 조건부 변수 및 `.shell` 내부 :root 변수의 computed value는 빈 값. 필수 mode 선언이 실제 적용되는 것과 검사 결과가 다르다.
- 원인: `_scope`가 innermost :root/.dark만 반환하고 바깥 stack의 조건/selector를 검사하지 않는다. `candidate.startswith('@')`를 건너뛰는 것으로 조건부 context가 사라진다.
- 영향: 빈 화면 범위의 alias를 완전한 root/dark 계약으로 승인한다. 이번 명시적 fail-closed 수용 기준을 충족하지 못한다.
- 권고: 전체 ancestor context를 검사하여 지원하지 않는 조건·중첩 scope는 제어 오류로 거부한다. 지원할 무조건 at-rule이 필요하다면 그 종류를 명시하고 조건부 블록과 분리한다. P1 OPEN, 수정 필요.

### B-P2-13 — both scope를 root/dark 중복 집계에 펼치지 않아 중복을 놓침

- 위치: `tools/check_aliases.py:579`–`586`.
- 최소 입력:

```css
:root, .dark { --brand: var(--kt-brand); }
:root { --brand: var(--kt-brand); }
```

- 명령: `review-t102-final-b-probe.py <candidate>`의 `both_and_root_duplicate`/`both_and_dark_duplicate`.
- 실제 결과: 양 OS exit 0. 두 번째 selector를 `.dark`로 바꿔도 exit 0. 대조군인 root 선언 두 번은 exit 1이다. Chromium CSSOM에서도 중복 선언 rule 2개를 확인했다.
- 원인: 집합 완전성 검사는 `both`를 양 모드로 취급하지만 중복 dict key는 `(both,name)`를 `(root,name)`/`(dark,name)`와 별개로 저장한다.
- 영향: 동일 mode에 한 번이라는 checker 계약이 selector 표기 차이에 따라 우회된다.
- 권고: 중복 집계에서 `both`를 root/dark 두 scope에 확장해 같은 identity로 검사한다. both+root/both+dark/정상 both 대조 시험을 둔다. P2 OPEN, 수정 필요.

### B-P1-14 — 비ASCII custom property·var 이름은 여전히 검사에서 사라짐

- 위치: `tools/check_aliases.py:15`–`16`, `:339`, `:472`.
- 최소 입력 1: 정상 양 모드 `--brand:var(--kt-brand)`에 `--kt-한글:blue` 선언을 각각 추가한다.
- 최소 입력 2: 정본에 없는 `--kt-한글`을 `:root{--brand:var(--kt-한글)} .dark{--brand:var(--kt-한글)}`로 참조한다.
- 명령: `review-t102-final-b-probe.py <candidate>`의 `unicode_kt_property`/`unicode_missing_reference`.
- 실제 결과: 둘 다 양 OS exit 0, `CSS 1개, 오류 0개`. Chromium은 `--kt-한글`을 실제 custom property로 보존하고 정상 정의가 있는 대조에서 var 참조를 blue로 해석했다.
- 원인: escape를 거부하는 새 guard와 별개로 ASCII 전용 이름 regex는 비ASCII 식별자를 소비하거나 명시적으로 거부하지 않는다. 금지 `--kt-*` 정의·모든 `var(--kt-…)` 대상 검증에서 조용히 빠진다.
- 영향: T-102의 namespace 금지와 미정의 참조 검증 약속이 여전히 불완전하다. 기존 escape 최소 반례는 닫혔으므로 새 경계로 별도 기록한다.
- 권고: CSS identifier 전체를 지원해 검사하거나, 이 도구가 지원하지 않는 비ASCII 구조 식별자/var 이름을 fail closed로 거부한다. 식별자 이외의 한국어 주석·문자열까지 금지하는 것은 피한다. P1 OPEN, 수정 필요.

## NOT_RUN 및 경계

- WSL Windows 8.3 전용 test 1개는 플랫폼상 skip. Windows에서 실제 short spelling 생성·samefile·CLI를 실행했으므로 Windows 보증 공백은 아니다.
- WSL jsonschema parity 2개: `NOT_RUN(jsonschema 미설치)`. WSL 234개 모두 pass라고 집계하지 않았다. Windows 전체는 skip 0이다.
- Windows ACL 읽기 거부: `NOT_RUN(chmod는 ACL과 다름)`. Linux 권한 거부 및 양 OS UTF-8/누락/symlink 경계는 실행했다.
- Linux Chromium 별도 실행: `NOT_RUN`; CSS 의미는 Windows Chromium에서 직접 확인하고 CLI 판정은 양 OS 실행했다. 브라우저 외부 요청은 전부 abort했다.
- 소비자 build/e2e/6폭 visual diff: `NOT_RUN(T-461 등 소비자 이관 task)`. 고정 weather Git object만 읽었고 소비자에 쓰지 않았다.
- npm/PyPI/Release/tag: `NOT_RUN(이번 범위 밖)`. 임시 common tarball 설치 외 발행·태그·소비자 설치 없음.
- 이 원본은 정확한 0916202 후보에만 귀속한다. 다른 reviewer 판정이나 미래 수정·CI를 현재 검증으로 세지 않았다.

후속 조치: 신규 세 finding을 수정한 immutable 후보에서 반례와 필수 gate를 다시 확인해야 한다.
