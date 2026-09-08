# T-103 수정 후 적대적 리뷰 23 기준선

- 리뷰 단계: post-fix-22에서 공통으로 확인된 fenced code block 들여쓰기 오판을 수정한 뒤의 독립 재검토
- 불변 코드 후보 commit: `3a8b569889fcaf4429cc70a7bafec779181aac6f`
- 불변 코드 후보 tree: `f72134340a7da31e3ad756bcbde215342fef80fc`
- delta 기준: `61f1cc6a900e25268e0c5eadc32ce1c5ccc9d3f3`
- 이전 manifest: `43d7f530cbe987c89e99ad2f5a6665d65724a78d`의 [post-fix-22 manifest](2026-09-08-t103-post-fix-22-manifest.md)

## 이번 후보의 수정

`tools/ux_lint.py`의 MDX fenced block 열기·닫기 후보가 선행 ASCII space/tab을 무제한 제거하지 않도록 바꿨다. `_markdown_indent_columns`가 공백은 1열, 탭은 다음 4열 정렬 지점까지 확장해 계산하고, CommonMark 허용 상한인 3열을 넘으면 fence 후보로 인정하지 않는다. `tests/test_ux_lint.py`에는 0·1·3열의 유효한 닫힘과 4 space·tab·space+tab의 비닫힘을 고정했다. fence marker 뒤 ASCII space/tab과 LS/PS 접미사, CR/LF/CRLF 경계의 기존 계약은 유지한다.

## 리뷰 요청

두 reviewer는 서로의 결과와 이 manifest 이후의 raw report를 읽지 않고 동일한 immutable 코드 후보를 독립 검증한다. 각자 별도 detached worktree에서 시작·종료 HEAD/tree와 clean 상태를 확인하고, 자신의 원본 report 한 파일만 작성한다. 소비자 저장소나 이 checkout의 제품·문서·기존 evidence를 수정하지 않는다.

- Reviewer A 전문 범위: CommonMark fence indentation/tab-stop, MDX inline·JSX·ESM·Unicode line terminator 경계, 기존 T-103 finding 회귀와 Windows/WSL 재현
- Reviewer B 전문 범위: Git added-line/base 집계, 입력·오류·redaction 경계, fence indentation/suffix·CR/CRLF 재현, 문서·task·소비자 scope 정합
- 원본 산출물: `docs/reviews/adversarial/evidence/2026-09-08-t103-post-fix-23-reviewer-a.md`와 `...-reviewer-b.md`
- verdict 어휘: `PASS` 또는 `NO-GO`; finding ID·심각도·위치·재현·영향·최소 수정·disposition을 기록한다.

## 고정 검증과 관찰

다음은 후보 `3a8b569`에서 coordinator가 실행한 결과다.

```text
Windows Python 3.14: python -B -X utf8 -m unittest discover -s tests       -> 293 OK, skip 0
WSL Python 3.11:     python3 -B -X utf8 -m unittest discover -s tests      -> 293 OK, skip 1
Windows focused:     tests.test_kt_contrast tests.test_ux_lint              -> 55 OK
WSL focused:         tests.test_kt_contrast tests.test_ux_lint              -> 55 OK
validate_document_links.py                                                 -> 460 documents, 2435 targets, errors 0
validate_plan.py                                                           -> 106 tasks, errors 0
check_spdx.py                                                              -> 56 files, errors 0
scan_secrets.py --all / check_prod_redaction.py --all                       -> 592 files, findings 0
check_versions.py --self-check                                              -> registry self-check PASS; consumer check NOT_RUN
check_aliases.py packages/tokens/aliases                                    -> CSS 1, errors 0
kt_contrast.py packages/tokens/tokens.css --json                            -> 27 pairs PASS
ux_lint.py --root tests/fixtures/ux --json                                  -> fail_count 0, checked-in findings 12
git diff --check 61f1cc6 3a8b569                                            -> no output
```

공통 양성·음성 probe와 fence 4열·tab·space+tab, 0~3열, ASCII suffix, LS/PS suffix, LF/CRLF/CR 입력을 양 OS에서 직접 재현한다. checked-in UX fixture의 12개 finding은 report 모드의 의도된 예시이며 fail_count 0으로 집계한다. 리뷰어는 실행한 명령과 실제 결과를 원본에 남긴다.

## 범위 밖과 NOT_RUN

- 실제 소비자 저장소 빌드·타입·e2e와 소비자 manifest 검증: `NOT_RUN` (common checkout만 허용된 범위)
- npm/PyPI registry 설치·게시와 실제 MDX compiler/browser 실행: `NOT_RUN` (이 작업은 라이브러리 게시를 수행하지 않음)
- Windows Python 3.11: `NOT_RUN` (실행 환경 부재; Windows 3.14와 WSL 3.11 결과로 대체 표기하지 않음)
- 실제 CommonMark parser 의존성 추가: 하지 않음. 공식 CommonMark 규격의 3열/4열·tab-stop 계약을 제품 코드에 직접 반영한다.
