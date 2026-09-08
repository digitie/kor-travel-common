# T-103 수정 후 적대적 리뷰 24 기준선

- 리뷰 단계: post-fix-23에서 확인된 backtick fence info string 오판을 수정한 뒤의 독립 재검토
- 불변 코드 후보 commit: `535beecaeaf06296df3c8c1e108c1b86564e48d7`
- 불변 코드 후보 tree: `7934214ea8584500670a7808ebb68b53dec29d63`
- delta 기준: `3a8b569889fcaf4429cc70a7bafec779181aac6f`
- 이전 manifest: `b68c07be7e1fec924ee85e5a1f7c155cb276c17b`의 [post-fix-23 manifest](2026-09-08-t103-post-fix-23-manifest.md)
- 직전 raw 원본: [A](2026-09-08-t103-post-fix-23-reviewer-a.md), [B](2026-09-08-t103-post-fix-23-reviewer-b.md)

## 이번 후보의 수정

`tools/ux_lint.py`의 Markdown fence opener가 marker 길이와 들여쓰기만 보고 fenced block으로 진입하던 경계를 보완했다. CommonMark는 backtick fence의 info string에 backtick을 허용하지 않으므로, opener 뒤 같은 줄에 backtick이 있으면 fence가 아니라 inline span 경로로 처리한다. tilde fence에는 이 제한을 적용하지 않는다. `tests/test_ux_lint.py`에는 LF·CRLF·CR의 잘못된 backtick opener 뒤 P8 검사와 backtick을 포함한 tilde info string의 fenced code 제외를 고정했다.

## 리뷰 요청

두 reviewer는 동일한 immutable 코드 후보에서 서로의 post-fix-24 원본을 읽지 않고 독립 실행한다. 별도 detached worktree에서 시작·종료 HEAD/tree와 clean을 확인하고, 자신의 원본 report 한 파일만 작성한다. 제품·manifest·소비자·기존 evidence는 수정하지 않는다.

- Reviewer A 전문 범위: CommonMark backtick/tilde opener info string, 3·4자 delimiter, 0~3열·tab-stop, CR/LF/CRLF, inline·fence·MDX JSX/ESM/Unicode 경계와 누적 finding 회귀
- Reviewer B 전문 범위: Git added-line/base·입력/오류/redaction·문서/task/scope 정합과 fence opener/suffix/indentation 교차 재현
- 원본 산출물: `docs/reviews/adversarial/evidence/2026-09-08-t103-post-fix-24-reviewer-a.md`와 `...-reviewer-b.md`
- verdict 어휘: `PASS` 또는 `NO-GO`; finding ID·심각도·위치·재현·영향·최소 수정·disposition을 기록한다.

## 고정 검증과 관찰

다음은 후보 `535beec`에서 coordinator가 실행한 결과다.

```text
Windows Python 3.14: python -B -X utf8 -m unittest discover -s tests       -> 295 OK, skip 0
WSL Python 3.11:     python3 -B -X utf8 -m unittest discover -s tests      -> 295 collected, 294 OK, skip 1
Windows focused:     tests.test_kt_contrast tests.test_ux_lint              -> 57 OK
WSL focused:         tests.test_kt_contrast tests.test_ux_lint              -> 57 OK
validate_document_links.py                                                 -> 463 documents, 2440 targets, errors 0
validate_plan.py                                                           -> 106 tasks, errors 0
check_spdx.py                                                              -> 56 files, errors 0
scan_secrets.py --all / check_prod_redaction.py --all                       -> 595 files, findings 0
check_versions.py --self-check                                              -> registry self-check PASS; consumer check NOT_RUN
check_aliases.py packages/tokens/aliases                                    -> CSS 1, errors 0
kt_contrast.py packages/tokens/tokens.css --json                            -> 27 pairs PASS
ux_lint.py --root tests/fixtures/ux --json                                  -> fail_count 0, checked-in findings 12
git diff --check 3a8b569 535beec                                            -> no output
```

리뷰어는 3·4자 backtick/tilde, opener info string의 backtick·ASCII/Unicode suffix, 0~3열과 4열·tab·space+tab, LF/CRLF/CR, fenced block 내부 P6/P8와 inline span 뒤 실행식 P8을 양 OS에서 직접 재현한다. checked-in UX fixture의 12개 finding은 report 모드의 의도된 예시이며 fail_count 0으로 집계한다.

## 범위 밖과 NOT_RUN

- 실제 소비자 저장소 빌드·타입·e2e와 소비자 manifest 검증: `NOT_RUN` (common checkout만 허용된 범위)
- npm/PyPI registry 설치·게시와 실제 MDX compiler/browser 실행: `NOT_RUN` (라이브러리 게시를 수행하지 않음)
- Windows Python 3.11: `NOT_RUN` (실행 파일 부재; Windows 3.14와 WSL 3.11 결과로 대체 표기하지 않음)
