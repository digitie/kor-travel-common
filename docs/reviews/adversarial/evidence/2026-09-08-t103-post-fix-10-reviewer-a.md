# T-103 post-fix-10 독립 적대적 리뷰 A 원본

- 실행 ID: `reviewer-a-t103-post-fix-10-20260908-113330`.
- 시작: 2026-09-08 11:33:30.657 KST. 제품 검토 종료: 2026-09-08 11:35:54.460 KST.
- 시작·종료 HEAD: `f6ea446547c4e71ffb272b9623729396d6ef7185`; tree: `f3b3b90d87d758d22917c7e729ec3e25c2fe06c3`.
- 시작·종료 `git status --porcelain=v1`: 빈 출력. 별도 detached worktree `review-t103-post10-a`에서 읽기·시험만 수행했다. 새 원본 한 파일만 별도 immutable commit한다.
- 최신 manifest: `bd73856ac1d3327b1fe46acc352163eee23ad504`의 `docs/reviews/adversarial/evidence/2026-09-08-t103-post-fix-10-manifest.md`를 `git show`로 읽고 검토를 다시 시작했다. 앞서 중단된 manifest를 최종 기준으로 사용하지 않았다. 코드 delta 기준선은 `e4b8fe3ff62c404660363f6751eda52428cf554c`이다.
- 요청: CSS comment-gap, 같은 문단 미종결 1/2자 span 뒤 HTML/JSX, blockquote 빈 문단, 파일 첫 span·3자 inline·backslash delimiter 및 누적 CSS/media/JSON/argparse/redaction/diff/symlink/airport corpus와 full/focused/static gates를 양 OS에서 독립 검증한다.
- 상대 결과·과거 raw 본문을 열지 않았다. 자기 누적 실행 helper만 재사용하여 새 후보 CLI를 실행했다. 후보 코드·manifest·소비자 파일·소스 `.git/config`를 수정하지 않았으며 registry·workflow dispatch도 호출하지 않았다.

## 판정

**NO-GO.** 누적 15개 ID 중 14개 FIXED, `A-P2-06`(P2)만 잔여 반례로 OPEN이다. 새 ID는 없으며 열린 P0 0건/P1 0건/P2 1건/P3 0건이다. 기존 HTML/JSX·blockquote 반례는 수정됐지만 태그 없이 표현식을 실행하는 MDX 문맥이 누락된다.

## A-P2-06 / P2 / OPEN — 미종결 span 뒤 MDX expression을 가린다

- 위치: `tools/ux_lint.py:128` `_mask_unclosed_inline_span`, 특히 133행 `resume_match`와 134행 문단 끝 fallback.
- 아래 각 줄을 별도 임시 `.mdx`로 저장한다. 첫째는 정상 검출 대조군이며 둘째·셋째는 실제 반례이다.

```mdx
Example {window.confirm('x')}
```

```mdx
Example ` unmatched {window.confirm('x')}
```

```mdx
Example `` unmatched {window.confirm('x')}
```

- 실행: `python -B -X utf8 tools/ux_lint.py <임시경로>/fixture.mdx --fail-new --json`.
- 실제: Windows 3.14.3·WSL 3.11.15 모두 대조군은 P8 1건·exit 1이다. 반례 두 개는 exit 0, `status=PASS`, `fail_count=0`, findings 0이다. 호출 자체를 실행하지 않고 검사기 입력으로만 사용했다.
- 기대: 세 경우 모두 `{window.confirm('x')}`는 인용 밖의 MDX 실행 표현식이므로 P8 1건·exit 1이어야 한다. 해석할 수 없는 입력은 일반 오류로 닫아야 하며 PASS로 표시하면 안 된다.
- 원인: 미종결 span 뒤 검사 재개 지점을 HTML/JSX 태그 또는 일부 줄 시작 statement로만 찾는다. `{...}` 실행 표현식은 해당 목록에 없어 문단 끝까지 마스킹된다.
- 영향: 동일한 실행 표현식 앞에 닫히지 않은 backtick 한두 개만 추가하면 신규 UX gate를 우회한다.
- 수정·수용: 닫히지 않은 Markdown delimiter를 실행 영역 전체의 제외 근거로 사용하지 않는다. 태그·특정 keyword뿐 아니라 MDX 표현식 문맥을 보존하고 실제 주석·정상 인용만 제외한다. 반례 두 개가 P8 exit 1이고 기존 정상 code span/fence가 findings 0인 회귀를 함께 확인해야 한다.
- 이번 정상 결과: 같은 문단의 미종결 1/2자 span 뒤 HTML/JSX, 일반·중첩 blockquote 빈 문단, backslash delimiter 뒤 JSX는 각각 P6 1건·exit 1이다. 파일 첫 span·3자 inline은 findings 0이다. 기존 JSX line/block 주석·중첩 object·무들여쓰기 ESM·다중행/blockquote/tagged/computed/배열/삼항 template·보간 주석·escaped interpolation·4자/tilde/suffix fence도 기대 결과를 유지했다.

## 누적 disposition

| 원 ID | 원 심각도 | 판정 | 직접 확인 |
|---|---|---|---|
| A-P1-01 | P1 | FIXED | 누적 comment compound는 일반 exit 2; selector 경계·본문 주석을 둔 정상 root는 미달 exit 1; media/specificity 회귀 유지 |
| A-P1-02 | P1 | FIXED | OKLCH chroma `25%`와 `0.1` RGB 동일 |
| A-P1-03 | P1 | FIXED | 흰색 20%/검정 source-over와 `#333` 대비 모두 1.6620953314177012 |
| A-P1-04 | P1 | FIXED | 앞 삽입 신규 행은 fail, 기존 행만 baseline exempt |
| A-P1-05 | P1 | FIXED | 외부 root basename 충돌에서도 신규 P6 검출 |
| A-P2-06 | P2 | OPEN | 위 MDX expression 누락 |
| A-P2-07 | P2 | FIXED | option 모양 `--base=--name-only` 일반 exit 2 |
| A-P2-08 | P2 | FIXED | WSL Git quoted/tab 파일명 추가 행 검출; Windows는 OS 제한 |
| A-P2-09 | P2 | FIXED | NaN/Infinity/음수/bool/중복 baseline·거대 수 일반 exit 2 |
| A-P2-10 | P2 | FIXED | 입력값·경로·baseline·argparse 합성 marker가 JSON/stderr/summary에 노출되지 않음 |
| A-P2-11 | P2 | FIXED | `--read-surface muted` 31쌍, tertiary/muted 미달 검출 |
| A-P3-12 | P3 | FIXED | geo 8쌍; airport task/evidence의 현재 1.320934와 역사 1.15 분리 |
| A-P1-13 | P1 | FIXED | `++counter;` 뒤 3행 P6가 Git diff added/fail |
| A-P2-14 | P2 | FIXED | 양 OS self-symlink root 일반 exit 2·traceback 없음 |
| A-P2-15 | P2 | FIXED | 양 도구 깊이 2000 JSON 일반 exit 2·traceback 없음 |

## 실행 명령과 결과

WSL은 `uv run --no-project --python 3.11`을 붙였고 전체 시험에는 `--with jsonschema`를 추가했다. WSL 정적 Git gate에만 process `GIT_DIR`/`GIT_WORK_TREE`로 detached metadata를 지정했고 합성 Git 반례에서는 제거했다. 저장소 config는 수정하지 않았다.

| 명령·대상 | Windows Python 3.14.3 | WSL Python 3.11.15 |
|---|---|---|
| `python -B -X utf8 -m unittest discover -s tests -p 'test_*.py'` | 287 통과·skip 0, 93.608초 | 287 실행·286 통과·skip 1, 56.231초; Windows 8.3 API 제외 |
| `python -B -X utf8 -m unittest tests.test_kt_contrast tests.test_ux_lint` | 49 통과, 13.745초 | 49 통과, 8.758초 |
| `python -B -X utf8 tools/validate_document_links.py` | 420 문서·2412 대상·오류 0 | 동일 |
| `python -B -X utf8 tools/validate_plan.py` | 106 task·오류 0 | 동일 |
| `python -B -X utf8 tools/check_spdx.py` | 56 파일·오류 0 | 동일 |
| `python -B -X utf8 tools/scan_secrets.py --all` | 552 파일·발견 0 | 동일 |
| `python -B -X utf8 tools/check_prod_redaction.py --all` | 552 파일·발견 0 | 동일 |
| `python -B -X utf8 tools/check_versions.py --self-check` | exit 0 | exit 0 |
| `python -B -X utf8 tools/check_aliases.py packages/tokens/aliases` | CSS 1개·오류 0 | 동일 |
| `git diff --check 94ca2f1730b270721eb6242bfcdd9362b51d45e5 f6ea446547c4e71ffb272b9623729396d6ef7185` | exit 0 | exit 0 |
| canonical tokens CLI light/dark | 각각 27쌍 미달 0·exit 0 | 동일 |
| 4앱 예제·baseline CLI | 미달 4/8/8/4건, 등록 baseline exit 0 | 동일 |
| `ux_lint.py --root tests/fixtures/ux --json` | 보고 12건·기본 report 모드 exit 0 | 동일; 위반 0건을 뜻하지 않음 |
| 누적 독립 CLI corpus | 위 정상·잔여 반례 재현 | 동일; tab 파일명도 실행 |

- 제품 delta는 UX 도구·시험 파일 30행 추가/17행 삭제로 전체 읽었다. CSS 도구·시험 및 task/evidence는 직전 코드 대비 동일하며 airport 수용 기준·역사 값 분리도 직접 확인했다.
- probe: `python -B -X utf8 F:/dev/kor-travel-common/.git/codex-audit/t103-post10-reviewer-a-probe.py F:/dev/kor-travel-common-wt/review-t103-post10-a`; WSL은 `/mnt/f/...` 경로와 uv Python. 자기 누적 실행 helper를 순차 호출하며 임시 fixture만 사용했다. SHA256: `39CB249B30E4BB1C6E72240285D6B5A20EB52F8C0B139DA191CCB75014BCF5F0`.
- exact CI: `gh run list --commit f6ea446547c4e71ffb272b9623729396d6ef7185 --json databaseId,headSha,status,conclusion,url --limit 5`로 [run 34180282181](https://github.com/digitie/kor-travel-common/actions/runs/34180282181)의 head SHA 일치 및 `completed/cancelled`를 확인했다. 다른 SHA의 성공으로 대체하지 않았다.

## NOT_RUN 및 한계

- Windows Python 3.11 실행 파일 부재. Windows tab 파일명은 OS 제한이며 WSL에서 실행했다. Windows self-symlink는 helper의 초기 플랫폼 안내와 별개로 후속 실제 생성·CLI 실행을 수행해 일반 exit 2를 확인했다.
- 이번 CSS 브라우저·Markdown lexer·별도 MDX compiler 실행: NOT_RUN. 검증은 후보 CLI·코드·합성 입력에 기반하며 실제 소비자 렌더링 성공을 주장하지 않는다.
- 소비자 build/e2e, npm/PyPI registry·게시, workflow dispatch, T-010 플랫폼 검사: NOT_RUN(범위 밖). exact 후보 CI 성공은 취소로 미완료다. 원본-only commit은 후보 변경 또는 이후 코드 재검토를 뜻하지 않는다.
