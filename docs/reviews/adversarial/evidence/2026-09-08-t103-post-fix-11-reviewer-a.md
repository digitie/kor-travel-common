# T-103 post-fix-11 독립 적대적 리뷰 A 원본

- 실행 ID: `reviewer-a-t103-post-fix-11-20260908-114731`.
- 시작: 2026-09-08 11:47:31.868 KST. 제품 검토 종료: 2026-09-08 11:49:53.163 KST.
- 시작·종료 HEAD: `c0c93c47e5f25aa0879fd0fb4e56261f6f624138`; tree: `f9b16a3d03f3fca49ba8048cc9d0328e78aadda4`.
- 시작·종료 `git status --porcelain=v1`: 빈 출력. 별도 detached worktree `review-t103-post11-a`에서 후보를 읽고 시험했다. 원본 한 파일만 별도 immutable commit한다.
- manifest: `f21b2007de2613fb507f8df843ad50125a38b4c3`의 `docs/reviews/adversarial/evidence/2026-09-08-t103-post-fix-11-manifest.md`를 `git show`로 읽었다. manifest의 diff gate 기준은 `bd73856ac1d3327b1fe46acc352163eee23ad504`; 직전 제품 코드와의 비교에는 `f6ea446547c4e71ffb272b9623729396d6ef7185`를 사용했다.
- 요청: 양 OS full/focused/static gates와 누적 CSS/JSON/redaction/diff/symlink/airport corpus, 미종결 1/2자 span 뒤 MDX 표현식·여러 줄 JSX의 양성/음성 대조를 독립 재현한다. Windows Python 3.11은 NOT_RUN이다.
- 상대 이번 결과·raw 및 미확정 raw를 열지 않았다. 자기 누적 실행 helper로 새 후보 CLI를 실행했다. 후보 코드·manifest·소비자 저장소·소스 `.git/config`는 수정하지 않았고 registry·workflow dispatch도 호출하지 않았다.

## 최종 판정

**NO-GO.** 누적 15개 ID 중 14개 FIXED, `A-P2-06`(P2)만 부분 수정 후 잔여 반례로 OPEN이다. 새 ID는 없으며 열린 P0 0건/P1 0건/P2 1건/P3 0건이다. 직전 최소 반례와 여러 줄 JSX는 수정됐지만 표현식의 첫 토큰에 따라 같은 누락이 남는다.

## A-P2-06 / P2 / OPEN — 단항 연산자·주석으로 시작하는 MDX 표현식을 가린다

- 위치: `tools/ux_lint.py:128` `_mask_unclosed_inline_span`, 특히 133–142행 `resume_candidates`의 표현식 시작 정규식과 문단 끝 fallback.
- 아래 세 줄을 각각 별도 임시 `.mdx` 파일로 저장한다.

```mdx
Example ` unmatched {!window.confirm('x')}
```

```mdx
Example `` unmatched {!window.confirm('x')}
```

```mdx
Example ` unmatched {/* note */ window.confirm('x')}
```

- 실행: `python -B -X utf8 tools/ux_lint.py <임시경로>/fixture.mdx --fail-new --json`.
- 실제: Windows 3.14.3와 WSL 3.11.15 모두 세 사례가 exit 0, `status=PASS`, `fail_count=0`, findings 0이다. `window.confirm` 자체를 실행하지 않고 검사기 입력으로만 사용했다.
- 기대: 셋 모두 정상 code span 밖의 실행 MDX 표현식이므로 P8 1건·exit 1이어야 한다. 지원하지 않는 입력이면 일반 오류로 닫아야 한다.
- 양성 대조: `Example {!window.confirm('x')}`는 양 OS에서 P8 1건·exit 1이다. 음성 대조: 같은 표현식을 정상적으로 닫힌 단일 code span 안에 넣으면 findings 0·exit 0이다.
- 원인·영향: 새 정규식은 `{` 다음의 식별자 또는 일부 여는 괄호만 시작점으로 인정한다. 유효한 JavaScript 단항 연산자 `!` 또는 선행 주석 `/`은 제외되어 문단 끝까지 마스킹된다. 호출 앞에 단항 연산자나 주석을 넣는 것만으로 신규 UX gate를 우회한다.
- 수정·수용: 실행 여부를 표현식 첫 토큰의 일부 목록으로 추정하지 않는다. 닫히지 않은 Markdown delimiter를 전체 실행 영역의 제외 근거로 삼지 않고 MDX expression 문맥을 보존한다. 세 반례는 P8 exit 1이어야 하며 정상 span·실제 주석·안전한 JSX의 음성 대조도 유지해야 한다.

## 수정 확인과 누적 disposition

- 직전 미종결 1/2자 span 뒤 `{window.confirm('x')}`는 양 OS에서 각각 P8 1건·exit 1이다.
- 여러 줄 JSX 대조는 `Example` 뒤 미종결 2자 span 다음 줄에 `<div className={`, 다음 줄에 ``[`outline-none`].join(" ")``, 다음 줄에 `}/>`를 둔다. 양 OS P6 1건·exit 1이며 `outline-none`을 `safe`로 바꾸면 findings 0·exit 0이다.
- 같은 문단 HTML/JSX, 일반·중첩 blockquote 빈 문단, backslash delimiter, 파일 첫 span·3자 inline, JSX 주석·중첩 object·무들여쓰기 ESM·tagged/computed/배열/삼항·보간 주석·escaped interpolation·4자/tilde/suffix fence의 누적 결과도 유지됐다.

| 원 ID | 원 심각도 | 판정 | 직접 확인 |
|---|---|---|---|
| A-P1-01 | P1 | FIXED | comment compound 일반 exit 2; 경계·본문 주석의 정상 root 미달 exit 1; media/specificity 유지 |
| A-P1-02 | P1 | FIXED | OKLCH chroma `25%`와 `0.1` RGB 동일 |
| A-P1-03 | P1 | FIXED | 흰색 20%/검정 source-over와 `#333` 대비 모두 1.6620953314177012 |
| A-P1-04 | P1 | FIXED | 앞 삽입 신규 행은 fail, 기존 행만 baseline exempt |
| A-P1-05 | P1 | FIXED | 외부 root basename 충돌에서도 신규 P6 검출 |
| A-P2-06 | P2 | OPEN | 위 단항 연산자·선행 주석 표현식 누락 |
| A-P2-07 | P2 | FIXED | option 모양 `--base=--name-only` 일반 exit 2 |
| A-P2-08 | P2 | FIXED | WSL Git quoted/tab 파일명 추가 행 검출; Windows는 OS 제한 |
| A-P2-09 | P2 | FIXED | NaN/Infinity/음수/bool/중복 baseline·거대 수 일반 exit 2 |
| A-P2-10 | P2 | FIXED | 입력값·경로·baseline·argparse 합성 marker가 JSON/stderr/summary에 노출되지 않음 |
| A-P2-11 | P2 | FIXED | `--read-surface muted` 31쌍, tertiary/muted 미달 검출 |
| A-P3-12 | P3 | FIXED | geo 8쌍; airport의 현재 1.320934와 역사 1.15 분리 |
| A-P1-13 | P1 | FIXED | `++counter;` 뒤 3행 P6가 Git diff added/fail |
| A-P2-14 | P2 | FIXED | 양 OS self-symlink root 일반 exit 2·traceback 없음 |
| A-P2-15 | P2 | FIXED | 양 도구 깊이 2000 JSON 일반 exit 2·traceback 없음 |

## 실행 명령과 결과

WSL은 `uv run --no-project --python 3.11`을 붙였고 전체 시험에는 `--with jsonschema`를 추가했다. WSL 정적 Git gate만 process `GIT_DIR`/`GIT_WORK_TREE`로 detached metadata를 지정했고 합성 Git 반례에서는 제거했다. 저장소 config는 변경하지 않았다.

| 명령·대상 | Windows Python 3.14.3 | WSL Python 3.11.15 |
|---|---|---|
| `python -B -X utf8 -m unittest discover -s tests -p 'test_*.py'` | 287 통과·skip 0, 80.359초 | 287 실행·286 통과·skip 1, 52.019초; Windows 8.3 API 제외 |
| `python -B -X utf8 -m unittest tests.test_kt_contrast tests.test_ux_lint` | 49 통과, 15.725초 | 49 통과, 8.197초 |
| `python -B -X utf8 tools/validate_document_links.py` | 424 문서·2412 대상·오류 0 | 동일 |
| `python -B -X utf8 tools/validate_plan.py` | 106 task·오류 0 | 동일 |
| `python -B -X utf8 tools/check_spdx.py` | 56 파일·오류 0 | 동일 |
| `python -B -X utf8 tools/scan_secrets.py --all` | 556 파일·발견 0 | 동일 |
| `python -B -X utf8 tools/check_prod_redaction.py --all` | 556 파일·발견 0 | 동일 |
| `python -B -X utf8 tools/check_versions.py --self-check` | exit 0 | exit 0 |
| `python -B -X utf8 tools/check_aliases.py packages/tokens/aliases` | CSS 1개·오류 0 | 동일 |
| `git diff --check bd73856ac1d3327b1fe46acc352163eee23ad504 c0c93c47e5f25aa0879fd0fb4e56261f6f624138` | exit 0 | exit 0 |
| canonical tokens CLI light/dark | 각각 27쌍 미달 0·exit 0 | 동일 |
| 4앱 예제·baseline CLI | 미달 4/8/8/4건, 등록 baseline exit 0 | 동일 |
| `ux_lint.py --root tests/fixtures/ux --json` | 보고 12건·기본 report 모드 exit 0 | 동일; 위반 0건을 뜻하지 않음 |
| 누적 독립 CLI corpus | 위 정상·잔여 반례 재현 | 동일; tab 파일명도 실행 |

- 제품 delta는 UX 도구·시험 파일 23행 추가/3행 삭제로 전체 읽었다. CSS 도구·시험과 task/evidence는 직전 제품 코드 대비 동일하며 airport 수용 기준·역사 값 분리도 직접 확인했다.
- probe: `python -B -X utf8 F:/dev/kor-travel-common/.git/codex-audit/t103-post11-reviewer-a-probe.py F:/dev/kor-travel-common-wt/review-t103-post11-a`; WSL은 `/mnt/f/...`와 uv Python. 자기 누적 실행 helper를 순차 호출하며 임시 fixture만 사용했다. SHA256: `D72D86C702DF8364CE8B15C52261C0CC5C50A51F4145B9DFC8B213369FD684B8`.
- exact CI: `gh run list --commit c0c93c47e5f25aa0879fd0fb4e56261f6f624138 --json databaseId,headSha,status,conclusion,url --limit 5`로 [run 34181153434](https://github.com/digitie/kor-travel-common/actions/runs/34181153434)의 head SHA 일치 및 `completed/success`를 확인했다. 개별 job 로그는 이번 리뷰에서 재독하지 않았다.

## NOT_RUN 및 한계

- Windows Python 3.11 실행 파일 부재. Windows tab 파일명은 OS 제한이며 WSL에서 실행했다. Windows self-symlink는 helper의 초기 플랫폼 안내와 별개로 후속 실제 생성·CLI 실행을 수행해 일반 exit 2를 확인했다.
- 이번 CSS 브라우저·Markdown lexer·별도 MDX compiler: NOT_RUN. 판정은 후보 CLI·코드·합성 입력에 기반하며 실제 소비자 렌더링 성공을 주장하지 않는다.
- 소비자 build/e2e, npm/PyPI registry·게시, workflow dispatch, T-010 플랫폼 검사: NOT_RUN(범위 밖). 원본-only commit은 제품 후보 변경 또는 이후 코드 재검토를 뜻하지 않는다.
