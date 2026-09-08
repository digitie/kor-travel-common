# T-103 수정 후 적대적 리뷰 33 기준선

- 리뷰 단계: post-fix-32에서 남은 1·2자 inline span의 중간 block fence 누락을 수정한 뒤의 독립 재검토
- 불변 코드 후보 commit: `9ae2b6de962bf42baea23e481e57e60be9c7bf47`
- 불변 코드 후보 tree: `125095a9ad9af4979cec6e784bd2e781c69de662`
- delta 기준: `2375c8b052c94ec8982e0a4be294a747e75835b1`
- 이전 manifest: `19afe59c5b8efcc3f0a84d5dc70026f8ed68913a`의 [post-fix-32 manifest](2026-09-08-t103-post-fix-32-manifest.md)
- 직전 raw 원본: [A](2026-09-08-t103-post-fix-32-reviewer-a.md), [B](2026-09-08-t103-post-fix-32-reviewer-b.md)

## 이번 후보의 수정

`tools/ux_lint.py`의 1·2자 Markdown inline span 경로도 3·4자 경로와 같은 `_markdown_has_fence_before` 경계를 사용한다. inline 닫힘보다 먼저 유효한 plain·blockquote·중첩 block fence가 나오면 opener 줄만 가리고 다음 줄에서 실행식 검사를 재개한다. 1·2·3·4자 run, tilde·더 긴 backtick, 일반·중첩 blockquote, LF/CRLF/CR와 4열 들여쓰기 경계를 회귀시험으로 고정했다.

## 리뷰 요청

두 reviewer는 동일한 immutable 코드 후보에서 post-fix-32 원본을 기준으로 독립 재검토하되 상대 reviewer의 새 결과·raw를 읽지 않는다. 별도 detached worktree에서 시작·종료 HEAD/tree와 clean을 확인하고 자신의 원본 report 한 파일만 작성한다. 제품·manifest·소비자·기존 evidence는 수정하지 않는다.

- Reviewer A 전문 범위: 1·2자 inline 반환·문단/실행 문맥·중간 fence·marker/container·P6/P8·줄바꿈
- Reviewer B 전문 범위: 독립 Markdown parser 대조·`--base` 추가행·tilde/backtick·plain/blockquote/nested·indent/tab-stop·오류/redaction
- 원본 산출물: `docs/reviews/adversarial/evidence/2026-09-08-t103-post-fix-33-reviewer-a.md`와 `...-reviewer-b.md`
- verdict 어휘: `PASS` 또는 `NO-GO`; finding ID·심각도·위치·재현·영향·최소 수정·disposition을 기록한다.

## 고정 검증과 관찰

다음은 후보 `9ae2b6d`에서 coordinator가 실행한 결과다.

```text
Windows Python:      py -3 -B -X utf8 -m unittest discover -s tests -p "test_*.py" -> 307 OK, skip 0
WSL Python 3.11:     python3 -B -X utf8 -m unittest discover -s tests -p "test_*.py" -> 307 OK, skip 1
Windows focused:     tests.test_kt_contrast tests.test_ux_lint -> 69 OK
WSL focused:         tests.test_kt_contrast tests.test_ux_lint -> 69 OK
validate_document_links.py -> 490 documents, 2487 targets, errors 0
validate_plan.py           -> 106 tasks, errors 0
check_spdx.py              -> 56 files, errors 0
scan_secrets.py --all / check_prod_redaction.py --all -> 622 files, findings 0
check_versions.py --self-check -> registry self-check PASS; consumer check NOT_RUN
check_aliases.py packages/tokens/aliases -> CSS 1, errors 0
kt_contrast.py packages/tokens/tokens.css -> 27 pairs PASS
ux_lint.py --root tests/fixtures/ux --json -> fail_count 0, checked-in findings 12
git diff --check 9ae2b6d -> no output
```

리뷰어는 post-32의 1·2자 inline span 반례가 중간 fence 뒤 실행식을 계속 검사하는지, 정상 닫힘 span과 4열·tab-stop은 계속 인용으로 가리는지, container·run 길이·줄바꿈과 `--base`가 일관되는지 양 OS에서 직접 재현한다. checked-in UX fixture의 12개 finding은 report 모드의 의도된 예시이며 fail_count 0으로 집계한다.

## 범위 밖과 NOT_RUN

- 정확한 후보 원격 CI: manifest 작성 시점에는 `NOT_RUN(실행 중)`; merge 전 PR head SHA와 6개 job을 다시 확인한다.
- 실제 소비자 저장소 빌드·타입·e2e와 소비자 manifest 검증: `NOT_RUN` (common checkout만 허용된 범위)
- npm/PyPI registry 설치·게시와 실제 MDX compiler/browser 실행: `NOT_RUN` (라이브러리 게시를 수행하지 않음)
- Windows Python 3.11: `NOT_RUN` (실행 파일 부재; Windows와 WSL 결과로 대체 표기하지 않음)
