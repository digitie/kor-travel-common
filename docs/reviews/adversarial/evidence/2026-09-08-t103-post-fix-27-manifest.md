# T-103 수정 후 적대적 리뷰 27 기준선

- 리뷰 단계: post-fix-26에서 확인된 blockquote marker 선택 공백과 콘텐츠 들여쓰기 혼합을 수정한 뒤의 독립 재검토
- 불변 코드 후보 commit: `009ec5dcf70e55b6c736ccaeabbfeb71a08836f6`
- 불변 코드 후보 tree: `f521d07dd7566744659522186a4add8f01d7150b`
- delta 기준: `2a32dc7e07a4c36e2b0e92402f05019b31f6c3cb`
- 이전 manifest: `af9ffdce3e9edc107572b050576a6735f0c3bdb8`의 [post-fix-26 manifest](2026-09-08-t103-post-fix-26-manifest.md)
- 직전 raw 원본: [A](2026-09-08-t103-post-fix-26-reviewer-a.md), [B](2026-09-08-t103-post-fix-26-reviewer-b.md)

## 이번 후보의 수정

`tools/ux_lint.py`가 blockquote의 `>` 뒤 선택 공백 한 열을 marker 구분자로 소비하고, 남은 공백·탭을 절대 tab-stop 기준 콘텐츠 열로 계산한다. 따라서 `>    ~~~`·`>\t~~~`·`> \t~~~`를 콘텐츠 0~3열의 유효한 opener/closer로 인식하고 `>     ~~~`·`>\t\t~~~`는 콘텐츠 4열 이상 body로 남긴다. nested marker 사이의 과도한 들여쓰기도 같은 경계로 거부한다. 회귀시험은 P6/P8, backtick/tilde, 공백·탭·space+tab, nested marker를 고정한다.

## 리뷰 요청

두 reviewer는 동일한 immutable 코드 후보에서 post-fix-26 원본을 기준으로 독립 재검토하되 상대 reviewer의 새 결과·raw를 읽지 않는다. 별도 detached worktree에서 시작·종료 HEAD/tree와 clean을 확인하고 자신의 원본 report 한 파일만 작성한다. 제품·manifest·소비자·기존 evidence는 수정하지 않는다.

- Reviewer A 전문 범위: CommonMark blockquote marker 선택 공백·tab-stop, fence opener/closer 콘텐츠 0~3열·4열, nested container·depth 감소·빈 줄·CR/LF/CRLF와 P6/P8 회귀
- Reviewer B 전문 범위: 위 경계의 독립 CommonMark 대조와 Git added-line/base, 오류/redaction, plain/blockquote·nested·`--base` 교차
- 원본 산출물: `docs/reviews/adversarial/evidence/2026-09-08-t103-post-fix-27-reviewer-a.md`와 `...-reviewer-b.md`
- verdict 어휘: `PASS` 또는 `NO-GO`; finding ID·심각도·위치·재현·영향·최소 수정·disposition을 기록한다.

## 고정 검증과 관찰

다음은 후보 `009ec5d`에서 coordinator가 실행한 결과다.

```text
Windows Python 3.14: python -B -X utf8 -m unittest discover -s tests       -> 300 OK, skip 0
WSL Python 3.11:     uv run --no-project --python 3.11 --with jsonschema ... -> 300 OK, skip 1
Windows focused:     tests.test_kt_contrast tests.test_ux_lint              -> 62 OK
WSL focused:         tests.test_kt_contrast tests.test_ux_lint              -> 62 OK
validate_document_links.py                                                 -> 472 documents, 2458 targets, errors 0
validate_plan.py                                                           -> 106 tasks, errors 0
check_spdx.py                                                              -> 56 files, errors 0
scan_secrets.py --all / check_prod_redaction.py --all                       -> 604 files, findings 0
check_versions.py --self-check                                              -> registry self-check PASS; consumer check NOT_RUN
check_aliases.py packages/tokens/aliases                                    -> CSS 1, errors 0
kt_contrast.py packages/tokens/tokens.css --json                            -> 27 pairs PASS
ux_lint.py --root tests/fixtures/ux --json                                  -> fail_count 0, checked-in findings 12
git diff --check 11d4eab 009ec5d                                            -> no output
```

리뷰어는 plain/blockquote/nested blockquote fence, depth 감소·인용되지 않은 빈 줄·새 quote block, marker 뒤 ASCII/Unicode suffix, 0~3열·4열·tab·space+tab, LF/CRLF/CR, `--base`와 외부 P6/P8을 양 OS에서 직접 재현한다. checked-in UX fixture의 12개 finding은 report 모드의 의도된 예시이며 fail_count 0으로 집계한다.

## 범위 밖과 NOT_RUN

- 정확한 후보 원격 CI: manifest 작성 시점에는 `NOT_RUN(실행 중)`; merge 전 PR head SHA와 6개 job을 다시 확인한다.
- 실제 소비자 저장소 빌드·타입·e2e와 소비자 manifest 검증: `NOT_RUN` (common checkout만 허용된 범위)
- npm/PyPI registry 설치·게시와 실제 MDX compiler/browser 실행: `NOT_RUN` (라이브러리 게시를 수행하지 않음)
- Windows Python 3.11: `NOT_RUN` (실행 파일 부재; Windows 3.14와 WSL 3.11 결과로 대체 표기하지 않음)
