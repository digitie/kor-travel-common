# T-103 수정 후 적대적 리뷰 25 기준선

- 리뷰 단계: post-fix-24에서 확인된 blockquote 내부 fenced code 오검출을 수정한 뒤의 독립 재검토
- 불변 코드 후보 commit: `155941045a077529cb12f875cad5ab2b2f7639da`
- 불변 코드 후보 tree: `4fb87fcc870402df48ac3f336f5f9c2a6ede7767`
- delta 기준: `535beecaeaf06296df3c8c1e108c1b86564e48d7`
- 이전 manifest: `4fac62b3b40f7cd36a7e3b80e399611b0aa30fff`의 [post-fix-24 manifest](2026-09-08-t103-post-fix-24-manifest.md)
- 직전 raw 원본: [A](2026-09-08-t103-post-fix-24-reviewer-a.md), [B](2026-09-08-t103-post-fix-24-reviewer-b.md)

## 이번 후보의 수정

`tools/ux_lint.py`의 MDX fence 판정이 일반 들여쓰기와 blockquote 컨테이너를 구분하도록 바꿨다. opener 앞의 `>` 깊이를 기록하고 같은 깊이의 인용 prefix가 있는 줄에서만 closing marker를 인정한다. 인용 fence 안의 빈 `>` 줄과 body는 가리며, 인용 prefix가 없는 비공백 줄을 만나면 미종결 fence를 그 위치에서 끝내 외부 MDX 실행식을 계속 검사한다. `tests/test_ux_lint.py`에는 LF·CRLF·CR의 tilde blockquote fence, 빈 quoted backtick fence, 인용 블록 밖 P8 경계를 고정했다.

## 리뷰 요청

두 reviewer는 동일한 immutable 코드 후보에서 서로의 post-fix-25 원본을 읽지 않고 독립 실행한다. 별도 detached worktree에서 시작·종료 HEAD/tree와 clean을 확인하고, 자신의 원본 report 한 파일만 작성한다. 제품·manifest·소비자·기존 evidence는 수정하지 않는다.

- Reviewer A 전문 범위: CommonMark blockquote/fence 컨테이너, nested `>` 깊이, 빈 quoted 행, plain/CR/LF/CRLF 경계, inline·JSX·ESM·Unicode 및 누적 finding 회귀
- Reviewer B 전문 범위: Git added-line/base·입력/오류/redaction·문서/task/scope 정합과 quoted fence opener/closer·container boundary·P6/P8 재현
- 원본 산출물: `docs/reviews/adversarial/evidence/2026-09-08-t103-post-fix-25-reviewer-a.md`와 `...-reviewer-b.md`
- verdict 어휘: `PASS` 또는 `NO-GO`; finding ID·심각도·위치·재현·영향·최소 수정·disposition을 기록한다.

## 고정 검증과 관찰

다음은 후보 `1559410`에서 coordinator가 실행한 결과다.

```text
Windows Python 3.14: python -B -X utf8 -m unittest discover -s tests       -> 297 OK, skip 0
WSL Python 3.11:     python3 -B -X utf8 -m unittest discover -s tests      -> 297 collected, 296 OK, skip 1
Windows focused:     tests.test_kt_contrast tests.test_ux_lint              -> 59 OK
WSL focused:         tests.test_kt_contrast tests.test_ux_lint              -> 59 OK
validate_document_links.py                                                 -> 466 documents, 2446 targets, errors 0
validate_plan.py                                                           -> 106 tasks, errors 0
check_spdx.py                                                              -> 56 files, errors 0
scan_secrets.py --all / check_prod_redaction.py --all                       -> 598 files, findings 0
check_versions.py --self-check                                              -> registry self-check PASS; consumer check NOT_RUN
check_aliases.py packages/tokens/aliases                                    -> CSS 1, errors 0
kt_contrast.py packages/tokens/tokens.css --json                            -> 27 pairs PASS
ux_lint.py --root tests/fixtures/ux --json                                  -> fail_count 0, checked-in findings 12
git diff --check 535beec 1559410                                           -> no output
```

리뷰어는 plain/blockquote/nested blockquote fence, marker 뒤 ASCII·Unicode suffix, 0~3열·4열·tab·space+tab, 빈 quoted 행, 인용 블록 종료 뒤 외부 P6/P8, LF/CRLF/CR, `--base`를 양 OS에서 직접 재현한다. checked-in UX fixture의 12개 finding은 report 모드의 의도된 예시이며 fail_count 0으로 집계한다.

## 범위 밖과 NOT_RUN

- 실제 소비자 저장소 빌드·타입·e2e와 소비자 manifest 검증: `NOT_RUN` (common checkout만 허용된 범위)
- npm/PyPI registry 설치·게시와 실제 MDX compiler/browser 실행: `NOT_RUN` (라이브러리 게시를 수행하지 않음)
- Windows Python 3.11: `NOT_RUN` (실행 파일 부재; Windows 3.14와 WSL 3.11 결과로 대체 표기하지 않음)
