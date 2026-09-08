# T-103 post-fix-09 독립 적대적 리뷰 A 원본

- 실행 ID: `reviewer-a-t103-post-fix-09-20260908-112424`.
- 시작: 2026-09-08 11:24:24.253 KST. 제품 검토 종료: 2026-09-08 11:26:54.833 KST.
- 시작·종료 HEAD: `e4b8fe3ff62c404660363f6751eda52428cf554c`; tree: `fb8f781ce70b89cc95883ef2531625c6259735c0`.
- 시작·종료 `git status --porcelain=v1`: 빈 출력. 새 detached worktree `review-t103-post9-a`에서 읽기·시험만 수행했다. 새 원본 한 파일만 별도 immutable commit한다.
- manifest: `f5f2e7c37188b68efd74fc8a320bee02e99aaa3e`의 `docs/reviews/adversarial/evidence/2026-09-08-t103-post-fix-09-manifest.md`를 `git show`로 읽었다. 수정 delta 기준선: `559a9e8a0e49feca2dab9d59df29039bbb0acfd3`.
- 요청: CSS comment-gap, Markdown 문단 밖 delimiter·파일 첫 span·3자 inline span과 전체 누적 CSS/media/JSON/argparse/redaction/diff/symlink/airport corpus 및 full/focused/static gates를 양 OS에서 독립 검증한다.
- 상대 결과·과거 raw 본문을 열지 않았다. 자기 누적 실행 helper로 반례를 재실행했다. 후보 코드·manifest·소비자 파일·소스 `.git/config`는 변경하지 않았고 registry·workflow dispatch도 호출하지 않았다.

## 판정

**NO-GO.** 누적 15개 ID 중 14개 FIXED, `A-P2-06`(P2)만 잔여 반례로 OPEN이다. `A-P1-01`은 이번 CSS 주석 경계 수정으로 FIXED이다. 새 ID는 없으며 열린 P0 0건/P1 0건/P2 1건/P3 0건이다.

## A-P2-06 / P2 / OPEN — 같은 문단의 inline JSX를 span으로 잘못 가린다

- 위치: `tools/ux_lint.py:108` `_find_inline_span_end`의 115–117행 역슬래시 처리, 402·418행 이후 닫힘 없는 span 분기.
- 아래 두 줄을 각각 별도 임시 `.mdx` 파일로 저장한다. 둘째 줄에는 역슬래시가 정확히 한 개 있다.

```mdx
Example ` unmatched <span className="outline-none" />
```

```mdx
Example `path\`<span className="outline-none" />
```

- 실행: `python -B -X utf8 tools/ux_lint.py <임시경로>/fixture.mdx --fail-new --json`.
- 실제: Windows 3.14.3·WSL 3.11.15 모두 두 경우에서 exit 0, `status=PASS`, `fail_count=0`, findings 0이다.
- 기대: 두 JSX 모두 Markdown code span 밖의 실행 마크업이므로 `outline-none` P6 1건·exit 1이다. 입력을 지원하지 못한다면 일반 입력 오류로 닫아야 한다.
- 첫 원인: 닫힘 없는 delimiter는 일반 문자인데 `end is None`이면 문단 나머지 전체를 마스킹한다. 직전 EOF 마스킹 문제를 문단 단위로 줄였지만 같은 문단 안의 실행 코드는 여전히 숨긴다.
- 둘째 원인: Markdown code span 안의 역슬래시는 일반 내용인데 JavaScript escape처럼 다음 backtick을 건너뛰어 닫힘을 놓친다. 이어서 위 `end is None` 경로가 JSX까지 가린다.
- 보조 대조: 설치된 `marked` lexer를 Windows Node로 실행했다. 첫 사례는 일반 text와 HTML token으로, 둘째는 text·codespan(`path`와 역슬래시)·HTML token으로 분리됐다. 이는 Markdown 인용 경계 대조이며 MDX compiler 실행을 뜻하지 않는다.
- 영향·수용: 같은 JSX 앞의 문구만 바꿔 신규 UX gate를 우회한다. 닫히지 않은 Markdown delimiter는 delimiter 자체만 일반 문자로 처리하고 이후 실제 마크업 검사를 계속한다. Markdown span의 내용 규칙과 JavaScript template의 escape 규칙을 분리한다. 두 사례는 P6 exit 1이어야 하고 정상 인용은 계속 제외해야 한다.
- 이번 정상 결과: 문단 밖 delimiter 사이 JSX는 P6 1건, 파일 첫 정상 span과 3자 inline span은 findings 0이다. JSX line/block 주석·중첩 object·무들여쓰기 ESM·기존 다중행/blockquote/tagged/computed/배열/삼항 template·보간 주석·escaped interpolation·2자 span·4자/tilde/suffix fence도 누적 기대 결과를 유지했다.

## 누적 disposition

| 원 ID | 원 심각도 | 판정 | 직접 확인 |
|---|---|---|---|
| A-P1-01 | P1 | FIXED | `.dark/**/:not(.light)`·`.dark/**/.dark`·root 주석과 다중행 comment compound 모두 일반 exit 2; selector 경계·본문 주석을 둔 정상 root는 미달 exit 1 |
| A-P1-02 | P1 | FIXED | OKLCH chroma `25%`와 `0.1` RGB 동일 |
| A-P1-03 | P1 | FIXED | 흰색 20%/검정 source-over와 `#333` 대비 모두 1.6620953314177012 |
| A-P1-04 | P1 | FIXED | 앞 삽입 신규 행은 fail, 기존 행만 baseline exempt |
| A-P1-05 | P1 | FIXED | 외부 root basename 충돌에서도 신규 P6 검출 |
| A-P2-06 | P2 | OPEN | 위 같은 문단의 inline JSX 누락 |
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
| `python -B -X utf8 -m unittest discover -s tests -p 'test_*.py'` | 287 통과·skip 0, 83.337초 | 287 실행·286 통과·skip 1, 48.974초; Windows 8.3 API 제외 |
| `python -B -X utf8 -m unittest tests.test_kt_contrast tests.test_ux_lint` | 49 통과, 12.191초 | 49 통과, 7.098초 |
| `python -B -X utf8 tools/validate_document_links.py` | 419 문서·2412 대상·오류 0 | 동일 |
| `python -B -X utf8 tools/validate_plan.py` | 106 task·오류 0 | 동일 |
| `python -B -X utf8 tools/check_spdx.py` | 56 파일·오류 0 | 동일 |
| `python -B -X utf8 tools/scan_secrets.py --all` | 551 파일·발견 0 | 동일 |
| `python -B -X utf8 tools/check_prod_redaction.py --all` | 551 파일·발견 0 | 동일 |
| `python -B -X utf8 tools/check_versions.py --self-check` | exit 0 | exit 0 |
| `python -B -X utf8 tools/check_aliases.py packages/tokens/aliases` | CSS 1개·오류 0 | 동일 |
| `git diff --check 94ca2f1730b270721eb6242bfcdd9362b51d45e5 e4b8fe3ff62c404660363f6751eda52428cf554c` | exit 0 | exit 0 |
| canonical tokens CLI light/dark | 각각 27쌍 미달 0·exit 0 | 동일 |
| 4앱 예제·baseline CLI | 미달 4/8/8/4건; 등록 baseline exit 0 | 동일 |
| `ux_lint.py --root tests/fixtures/ux --json` | 보고 12건·기본 report 모드 exit 0 | 동일; 위반 0건을 뜻하지 않음 |
| 누적 독립 CLI corpus | 위 정상·잔여 반례 재현 | 동일; tab 파일명도 실행 |

- 제품 delta 두 도구·두 시험 파일 101행 추가/20행 삭제를 전체 읽었다. task/evidence는 직전 코드 대비 동일하며 airport 수용 기준·역사 값 분리도 직접 확인했다.
- probe: `python -B -X utf8 F:/dev/kor-travel-common/.git/codex-audit/t103-post9-reviewer-a-probe.py F:/dev/kor-travel-common-wt/review-t103-post9-a`; WSL은 `/mnt/f/...`와 uv Python. 자기 누적 실행 helper를 순차 호출하며 임시 fixture만 사용했다. SHA256: `FE77B1AB32ED435A02CC141D43D5A69FE14E0AC6AE1B979AAE464F26380F0192`.
- Markdown 대조: `node F:/dev/kor-travel-common/.git/codex-audit/t103-post9-reviewer-a-markdown.cjs`; SHA256: `C2D02DCD694C0F3B2237AFAC10A0F37FB7B42D22A78ADD4833915A1D99554BDE`. 설치된 `marked`를 사용했고 registry 접근·설치하지 않았다.
- exact CI: `gh run list --commit e4b8fe3ff62c404660363f6751eda52428cf554c --json databaseId,headSha,status,conclusion,url --limit 5`로 [run 34179854916](https://github.com/digitie/kor-travel-common/actions/runs/34179854916)의 head SHA 일치 및 `completed/cancelled`를 확인했다. 다른 SHA의 성공을 대신 집계하지 않았다.

## NOT_RUN 및 한계

- Windows Python 3.11 실행 파일 부재. Windows tab 파일명은 OS 제한이며 WSL에서 실행했다. Windows self-symlink는 helper의 초기 플랫폼 안내와 별개로 후속 실제 생성·CLI 실행을 수행해 일반 exit 2를 확인했다.
- 이번 CSS 브라우저 재대조·WSL Markdown lexer·별도 MDX compiler: NOT_RUN. CSS 반례는 이번 후보에서 일반 입력 오류로 닫힘을 CLI로 확인했고 새 CSS 렌더링 주장은 하지 않는다. Markdown 보조 대조는 Windows이다.
- 소비자 build/e2e, npm/PyPI registry·게시, workflow dispatch, T-010 플랫폼 검사: NOT_RUN(범위 밖). exact 후보 CI 성공은 취소로 미완료다. 원본-only commit은 후보 수정 또는 이후 코드 재검토를 뜻하지 않는다.
