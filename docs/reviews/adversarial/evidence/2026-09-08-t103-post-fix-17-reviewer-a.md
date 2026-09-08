# T-103 수정 후 17 — Reviewer A 독립 원본

- 실행 ID: `reviewer_a-t103-post17-20260908T130421+0900`.
- 판정: **NO-GO**. 기존 A finding 15개 FIXED, 신규 `A-P1-16`(P1) OPEN. 누적 16개 중 15개 FIXED / 1개 OPEN. 신규·잔여 P0/P2/P3 0개.
- 제품 후보 commit: `34c0abfbdf695258d53a1015ff4b73926d1ebcd1`; tree: `8bc05556808a5b970d8f0ac659f7fd934ac88167`.
- 직전 제품 후보: `73b9cf68788066742e8df99dfad2433cbe6bf5fc`. 도구·시험 delta는 `tools/ux_lint.py`, `tests/test_ux_lint.py`이며 전체를 읽었다. AGENTS·문서 라우터·task·standards·runbook의 delta는 없다.
- 공통 manifest: commit `1c6091d7a6ef518764ba58808cae4e4777638c36`의 `docs/reviews/adversarial/evidence/2026-09-08-t103-post-fix-17-manifest.md`를 `git show`로 읽었다. manifest의 과거 원본 메타데이터 외에 상대 원본·이번 결과·미확정 원본을 읽지 않았다.
- 격리: `F:/dev/kor-travel-common-wt/review-t103-post17-a`, 새 detached checkout. 제품·manifest·소비자·Git config는 수정하지 않았다. 새 원본 한 파일만 별도 커밋한다.
- 시작: 2026-09-08 13:04:21.023 KST, 위 SHA/tree, `git status --porcelain=v1` 빈 출력.
- 제품 검토 종료: 2026-09-08 13:08:30.124 KST, 동일 SHA/tree, `git status --porcelain=v1` 빈 출력. 이후 evidence commit/tree는 제품 후보와 구분한다.

## 요청과 검토 범위

Windows Python 3.14와 WSL Python 3.11에서 manifest의 full/focused/static gate 및 누적 CSS/JSON/redaction/diff/symlink/airport corpus를 독립 실행했다. U+2028/U+2029의 줄 주석 종료를 plain TS·MDX·template 보간·중첩 JSX에서 확인하고 CR/LF 및 주석·인용 음성 대조를 함께 실행했다. 이전 Unicode/FEFF/async 반례도 다시 확인했다. 작성자 주장이나 상대 결과를 판정 근거로 사용하지 않았다.

## A-P1-16 — P1 / OPEN: 소스 내부 Unicode 구분자를 Git diff 구조로 오인

- 위치: `tools/ux_lint.py:756`의 `output.splitlines()`, 757~759행의 `@@` header 인식.
- 원인: Git patch는 LF로 구분하는데 `str.splitlines()`가 소스 내용의 U+2028/U+2029까지 새로운 patch 행으로 분리한다. 그 뒤에 있는 문자열 `@@ -0,0 +99,1 @@`를 실제 hunk header로 읽어 추가 행 번호를 99로 바꾼다. 검사기는 실제 2행의 P8을 찾고도 `added: false`로 분류해 fail 대상에서 제외한다.
- 범위: `added_lines`는 이번 수정에서 변하지 않았다. **기존 결함의 새 발견**이며 이번 줄 주석 수정이 도입했다고 주장하지 않는다. 직전 제품 코드 `73b9cf6`의 별도 작업 트리에서도 같은 명령을 양 OS로 실행해 동일 결과를 확인했다. 기존 A-P1-13의 실제 `+++` 추가 행 문제와는 다른 분할 경계이므로 새 ID다.

임시 Git 저장소에 `case.ts`를 아래 두 행으로 커밋한다.

```typescript
const text = "old";
const safe = 1;
```

그 뒤 Python으로 다음 문자열을 생성하여 같은 파일에 쓴다. `separator`는 실제 `"\u2028"` 또는 `"\u2029"` 문자이며 역슬래시 여섯 글자 escape가 아니다.

```python
body = 'const text = "a' + separator + '@@ -0,0 +99,1 @@";\nwindow.confirm("x");\n'
```

명령: 임시 root에서 `python -B -X utf8 <후보>/tools/ux_lint.py --root <임시-root> --base <fixture-commit> --fail-new --json`.

| 입력 | Windows 3.14.3 | WSL 3.11.15 | 기대 |
|---|---|---|---|
| 실제 U+2028 | **exit 0 / PASS / fail_count 0** | 동일 | exit 1 / fail_count 1 |
| 실제 U+2029 | **exit 0 / PASS / fail_count 0** | 동일 | exit 1 / fail_count 1 |
| literal `\\u2028` 대조 | exit 1 / FAIL / fail_count 1 | 동일 | 정상 탐지 |
| literal `\\u2029` 대조 | exit 1 / FAIL / fail_count 1 | 동일 | 정상 탐지 |

두 실패에서 finding은 `file: case.ts`, `line: 2`, `column: 1`, `pattern: P8`, `baseline: 0`, `exempt: false`, **`added: false`, `fail: false`**였다. 대조는 같은 위치에서 `added: true`, `fail: true`였다. Node `v25.9.0`의 `new Function`으로 실제 U+2028/U+2029를 포함한 전체 두 행을 평가한 결과 두 경우 모두 문법 승인 및 로컬 `confirm` stub 호출 1회였다. 실제 브라우저 대화상자는 호출하지 않았다.

- 영향: 변경 파일 내부의 문자열 내용만으로 새 금지 패턴의 diff gate를 거짓 PASS로 만들 수 있다. 전체 report에 위반이 보이더라도 추가 행 fail 계약과 CI 종료 코드가 깨지므로 P1로 분류한다.
- 수정 방향·수용 기준: Git이 정의하는 LF 물리 행과 소스의 ECMAScript 줄 종결자를 분리한다. Git 출력의 원래 행 경계를 보존하고 실제 patch 구조 안에서만 hunk header를 해석한다. 두 반례는 P8 1개 / `added: true` / exit 1이어야 하며 escape 대조, 실제 `+++` 추가 행, 여러 hunk·baseline·CRLF 및 인용 파일명 회귀를 유지한다. Unicode 구분자나 소스 문자열을 patch header로 재해석하는 예외를 추가하지 않는다.

정확한 재현 helper는 후보 밖 `F:/dev/kor-travel-common/.git/codex-audit/t103-post17-diff-a.py`다. `python -B -X utf8 <helper> <후보-worktree>`로 실행했다. helper는 `tempfile` root에서 `git init`, `git add -- case.ts`, `git -c user.name=Review fixture -c user.email=fixture@example.invalid commit -qm fixture`로 시험용 baseline만 만들며 source/소비자 Git config를 쓰지 않는다. WSL은 `/mnt/f/...` 경로와 uv Python 3.11로 같은 명령을 실행했다. 후보 경로를 `review-t103-post16-a`로 바꾼 대조도 양 OS에서 수행했다.

## 줄 주석 수정 및 누적 disposition

LF/CR/U+2028/U+2029 각각 plain TS, plain MDX, 미종결 1자/2자 span 뒤 comment 선행 expression, template 보간, 중첩 JSX, 줄 주석 음성, block comment 음성, 닫힌 span 음성을 실행했다. **각 OS 36개 결과**에서 여섯 양성은 각각 P8 또는 P6 1개 / exit 1, 세 음성은 0개 / exit 0이었다. U+2028/U+2029 뒤 금지 호출이 더 이상 줄 주석 안으로 숨지 않는다.

| 원 ID | 원 심각도 | 판정 | 이번 후보 직접 검증 |
|---|---|---|---|
| A-P1-01 | P1 | FIXED | CSS root/dark·specificity·media 교집합·unsupported selector·빈 목록·descendant·comment-gap. 미지원 형태는 일반 오류 2, 유효 cascade 미달은 1. |
| A-P1-02 | P1 | FIXED | OKLCH chroma `25%`와 `0.1` RGB 일치. |
| A-P1-03 | P1 | FIXED | 흰색 20% / 검정 sRGB source-over와 `#333` 대비 1.6620953314177012 일치. |
| A-P1-04 | P1 | FIXED | baseline 앞 신규 행은 fail, 기존 등록 행은 면제. |
| A-P1-05 | P1 | FIXED | 같은 basename의 외부 임시 Git root 구분. |
| A-P2-06 | P2 | FIXED | 누적 MDX 및 Unicode/FEFF/async 반례에서 양 OS 실행식 탐지·닫힌 인용 음성 대조 유지. |
| A-P2-07 | P2 | FIXED | `--base=--name-only` 일반 오류 2. |
| A-P2-08 | P2 | FIXED | WSL Git quoting/tab 파일명 추가 행 P6 탐지. Windows 해당 파일명은 NOT_RUN. |
| A-P2-09 | P2 | FIXED | NaN/Infinity/음수/bool/중복 및 400·5000자리 JSON 일반 오류 2. |
| A-P2-10 | P2 | FIXED | 합성 marker가 stderr/JSON/summary/argparse 오류에 평문 노출되지 않음. |
| A-P2-11 | P2 | FIXED | muted 읽기 표면 총 31쌍, 추가 4쌍 및 tertiary/muted 미달 확인. |
| A-P3-12 | P3 | FIXED | geo 미달 8개, airport 현재 1.32(실측 1.320934)와 과거 1.15 구분 유지. |
| A-P1-13 | P1 | FIXED | 실제 `++counter;` 추가 행에서 생기는 diff `+++`를 헤더로 버리지 않고 후속 추가 행 P6 탐지. |
| A-P2-14 | P2 | FIXED | 양 OS self-symlink root 일반 오류 2 / traceback 없음. Windows 직접 링크 probe도 실행. |
| A-P2-15 | P2 | FIXED | 깊이 2000 JSON을 두 도구에 입력해 양 OS 일반 오류 2 / traceback 없음. |
| A-P1-16 | P1 | OPEN | U+2028/U+2029 뒤의 소스 문자열을 hunk header로 오인해 신규 P8을 기존 행으로 분류. |

## 실제 검증

Windows Python 3.14.3, WSL은 `uv run --no-project --python 3.11`의 Python 3.11.15다. WSL 전체 시험에는 `--with jsonschema`를 추가했다. WSL Git 정적 gate에만 detached checkout의 `GIT_DIR`/`GIT_WORK_TREE`를 프로세스 환경으로 지정했고 시험/probe에는 주입하지 않았다. diff fixture helper도 해당 환경을 제거한다.

| Windows 명령(WSL은 위 uv 접두 사용) | Windows | WSL |
|---|---|---|
| `python -B -X utf8 -m unittest discover -s tests -p 'test_*.py'` | 289 실행 / 289 통과 / skip 0, 83.045초 | 289 실행 / 288 통과 / skip 1, 49.820초. skip은 Windows 8.3 전용 |
| `python -B -X utf8 -m unittest tests.test_kt_contrast tests.test_ux_lint` | 51 통과 / skip 0, 13.878초 | 51 통과 / skip 0, 7.481초 |
| `python -B -X utf8 tools/validate_document_links.py` | 문서 442개 / 대상 2420개 / 오류 0 | 동일 |
| `python -B -X utf8 tools/validate_plan.py` | task 106개 / 오류 0 | 동일 |
| `python -B -X utf8 tools/check_spdx.py` | 56개 / 오류 0 | 동일 |
| `python -B -X utf8 tools/scan_secrets.py --all` | 574개 / 발견 0 | 동일 |
| `python -B -X utf8 tools/check_prod_redaction.py --all` | 574개 / 발견 0 | 동일 |
| `python -B -X utf8 tools/check_versions.py --self-check` | exit 0; 소비자 검사 아님 | 동일 |
| `python -B -X utf8 tools/check_aliases.py packages/tokens/aliases` | CSS 1개 / 오류 0 | 동일 |
| `git diff --check f2f55b1 34c0abfbdf695258d53a1015ff4b73926d1ebcd1` | exit 0 | exit 0 |

누적 probe 명령은 `python -B -X utf8 F:/dev/kor-travel-common/.git/codex-audit/t103-post17-reviewer-a-probe.py F:/dev/kor-travel-common-wt/review-t103-post17-a`다. WSL은 두 경로를 `/mnt/f/...`로 바꾸고 uv 접두로 실행했다. 자신의 A probe만 재사용하며 상대 결과·과거 raw 본문은 읽지 않는다. 두 helper는 후보 밖에 있으며 원본 commit에 포함하지 않는다.

- 누적 helper SHA256: `5BD8D4EE576AF80F2A19A8C95D3A5B5942FCA287548E62998C5A6B6ECB9DF2B5`.
- diff helper SHA256: `167426897851CA0B3510BD49A6364A81DBC70CCC31677047EA6419D675AE6E4E`.

정본 light/dark 각각 27쌍 미달 0. 4앱 예제 light 미달은 docker-manager/concierge/geo/airport 순서로 4/8/8/4이며 baseline의 `--fail-new` exit 0을 미달 없음으로 해석하지 않는다. UX fixture report는 finding 12개 / exit 0이다. 오류 채널의 traceback/합성 marker 부재도 별도 검증했다.

`gh run list --commit 34c0abfbdf695258d53a1015ff4b73926d1ebcd1 --json databaseId,headSha,status,conclusion,url --limit 5`로 [CI run 34185592718](https://github.com/digitie/kor-travel-common/actions/runs/34185592718)의 exact headSha와 conclusion **cancelled**를 확인했다. 로컬 회귀 성공을 이 후보의 원격 CI 성공으로 바꾸지 않는다.

## 미실행과 한계

- `NOT_RUN`: Windows Python 3.11. 런타임 부재로 조정자 지정 Windows 3.14 / WSL 3.11을 사용했다.
- `NOT_RUN`: 실제 소비자 build/e2e·adoption gate, registry 조회·게시, workflow dispatch. common 리뷰 범위 밖이다.
- `NOT_RUN`: 이번 후보의 브라우저/MDX compiler 렌더링. CLI 대조와 Node 문법 검증은 실제 소비자 빌드 성공을 뜻하지 않는다.
- 원본 추가 후 전체 staged diff·공백·문서 링크·staged 비공개 검사를 확인하여 원본만 커밋한다. 제품·manifest·기존 원본은 변경하지 않는다.
