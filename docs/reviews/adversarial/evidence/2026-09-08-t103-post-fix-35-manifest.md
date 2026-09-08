# T-103 수정 후 적대적 리뷰 35 기준선

- 리뷰 단계: post-fix-34에서 반복된 주석 우회와 닫힘 없는 span의 주석 내부 재개를 상태 전이로 통합한 뒤의 독립 재검토
- 불변 코드 후보 commit: `aedfdd659255c27bcc4377bd15b39452c004417d`
- 불변 코드 후보 tree: `4bb189dddeab51d3cd0222d0ab50bef17a84ad99`
- delta 기준: `888fbbc2e943eab4198cf19a4dda6d88ce24b933`
- 이전 manifest: `de0c3ef9fb21d69458a50ba2c64fc4097f978396`의 [post-fix-34 manifest](2026-09-08-t103-post-fix-34-manifest.md)
- 직전 raw 원본: [A](2026-09-08-t103-post-fix-34-reviewer-a.md), [B](2026-09-08-t103-post-fix-34-reviewer-b.md)

## 이번 후보의 수정

Markdown inline span이 block fence에서 중단되면 줄 끝으로 건너뛰지 않고 delimiter 뒤에서 즉시 기존 lexer를 재개한다. 따라서 같은 줄의 JavaScript 주석과 실제 실행식이 각각 정상적으로 제외·검사된다. 닫힘 없는 span의 재개 후보는 주석을 먼저 마스킹한 텍스트에서 찾고, 첫 block fence 위치에서 탐색을 끝내 fence 내부를 문서 실행식으로 오인하지 않는다. 1·2·3·4자 run, 같은 줄·다음 줄 주석, 주석 밖 실행식, LF/CRLF/CR 회귀시험을 추가했다.

## 리뷰 요청

두 reviewer는 동일한 immutable 코드 후보에서 post-fix-34 원본을 기준으로 독립 재검토하되 상대 reviewer의 새 결과·raw를 읽지 않는다. 별도 detached worktree에서 시작·종료 HEAD/tree와 clean을 확인하고 자신의 원본 report 한 파일만 작성한다. 제품·manifest·소비자·기존 evidence는 수정하지 않는다.

- Reviewer A 전문 범위: delimiter 뒤 lexer 재개·같은 줄 주석·닫힘 없는 span·재개 후보·P6/P8·문단/줄바꿈·container
- Reviewer B 전문 범위: 독립 Markdown parser 대조·`--base` 추가행·짧은 run·tilde/backtick·plain/blockquote/nested·indent/tab-stop·오류/redaction
- 원본 산출물: `docs/reviews/adversarial/evidence/2026-09-08-t103-post-fix-35-reviewer-a.md`와 `...-reviewer-b.md`
- verdict 어휘: `PASS` 또는 `NO-GO`; finding ID·심각도·위치·재현·영향·최소 수정·disposition을 기록한다.

## 고정 검증과 관찰

다음은 후보 `aedfdd6`에서 coordinator가 실행한 결과다.

```text
Windows Python:      py -3 -B -X utf8 -m unittest discover -s tests -p "test_*.py" -> 310 OK, skip 0
WSL Python 3.11:     python3 -B -X utf8 -m unittest discover -s tests -p "test_*.py" -> 310 OK, skip 1
Windows focused:     tests.test_kt_contrast tests.test_ux_lint -> 72 OK
WSL focused:         tests.test_kt_contrast tests.test_ux_lint -> 72 OK
validate_document_links.py -> 496 documents, 2493 targets, errors 0
validate_plan.py           -> 106 tasks, errors 0
check_spdx.py              -> 56 files, errors 0
scan_secrets.py --all / check_prod_redaction.py --all -> 628 files, findings 0
check_versions.py --self-check -> registry self-check PASS; consumer check NOT_RUN
check_aliases.py packages/tokens/aliases -> CSS 1, errors 0
kt_contrast.py packages/tokens/tokens.css -> 27 pairs PASS
ux_lint.py --root tests/fixtures/ux --json -> fail_count 0, checked-in findings 12
git diff --check aedfdd6 -> no output
```

리뷰어는 fence 중단 뒤 같은 줄 주석·실행식, 닫힘 없는 span의 주석·fence 전후, 정상 닫힘·4열/tab-stop·container·run 길이·줄바꿈과 `--base`가 일관되는지 양 OS에서 직접 재현한다. checked-in UX fixture의 12개 finding은 report 모드의 의도된 예시이며 fail_count 0으로 집계한다.

## 범위 밖과 NOT_RUN

- 정확한 후보 원격 CI: manifest 작성 시점에는 `NOT_RUN(실행 중)`; merge 전 PR head SHA와 6개 job을 다시 확인한다.
- 실제 소비자 저장소 빌드·타입·e2e와 소비자 manifest 검증: `NOT_RUN` (common checkout만 허용된 범위)
- npm/PyPI registry 설치·게시와 실제 MDX compiler/browser 실행: `NOT_RUN` (라이브러리 게시를 수행하지 않음)
- Windows Python 3.11: `NOT_RUN` (실행 파일 부재; Windows와 WSL 결과로 대체 표기하지 않음)
