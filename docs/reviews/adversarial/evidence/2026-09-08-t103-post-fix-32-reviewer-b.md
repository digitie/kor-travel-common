# T-103 post-fix-32 독립 적대적 리뷰 B 원본

- 실행 ID: `T103-PF32-B-20260908-172231`; 시작 KST `2026-09-08T17:22:31.8161544+09:00`.
- 제품 후보 HEAD `2375c8b052c94ec8982e0a4be294a747e75835b1`, tree `21a1ca16b806149842777f6c8f597cab5c0433fa`.
- `F:/dev/kor-travel-common-wt/review-t103-post32-b`에 detached checkout했다. 시작 status는 clean이다. 제품·manifest·소비자·기존 evidence·Git 설정을 수정하지 않았다. 이 원본 파일만 별도 커밋한다.
- manifest는 `19afe59`의 `docs/reviews/adversarial/evidence/2026-09-08-t103-post-fix-32-manifest.md`를 `git show`로 읽었다. blob SHA-256 `5439dd52bb0938a7777c0aeaffe53b4a846569bcf7b57a3e4042efd0397f8100`.
- `b2fc22b..2375c8b`의 제품 2파일 전체 diff를 읽었다. 나머지 변경 3파일은 이전 manifest·A/B 원본의 추가 경로만 확인했다. 요청대로 post31 양측 원본과 상대 결과는 읽거나 요청하지 않았다.
- 범위: 독립 Markdown parser, Git 추가행/`--base`, 중간 tilde/backtick, plain/quoted/nested, indent/tab-stop, 오류·redaction, 양 OS. source `.git/config` 시작 SHA-256은 `0A0F849E7874CF0A25926856F9D2E381CCBF4C2DCB5999869C57B86E0F5BEB5B`이다.

## 판정과 disposition

**NO-GO**. B-P1-23은 **부분 수정 OPEN**이다. 3·4자 반례를 수정했지만 1·2자 inline 경로에 같은 누락이 남았다. 신규 ID/P0~P3는 추가하지 않는다.

| ID·심각도 | disposition | 근거 |
|---|---|---|
| B-P1-23 | 부분 수정 OPEN | 기존 3·4자 prose/중간 fence는 FIXED. 1·2자 span이 다음 fence 안의 backtick까지 연결돼 실행식을 숨긴다. |
| B-P2-25 | FIXED | 내부 짧은 marker 72교차와 JSON·Markdown·명시적/환경 step summary 대조에서 TypeError가 사라지고 정상 출력·exit 0. |
| B-P2-13 | FIXED 유지 | 같은 행/같은 문단 인용과 quoted/nested 4열·tab-stop 대조. |
| B-P3-24 | FIXED 유지 | manifest focused 67 표기를 실제 실행과 대조. |
| B-P1-01/02/03/04, B-P2-05/06, B-P3-07, B-P1-08/09, B-P2-10, B-P1-11/12/14/15/16, B-P2-17/18/19/20, B-P1-21/22 | FIXED 유지(검증 범위 한정) | 변경 없는 코드의 이전 검증을 동일성으로 재사용하고 이번 full/focused 및 선택한 직접 corpus를 실행했다. 이전 모든 개별 CLI를 전수 재실행했다고 주장하지 않는다. |

## B-P1-23 최소 재현·영향·수정 방향

위치: `tools/ux_lint.py:433`~449의 `_find_inline_span_end`, `:839`의 3자 이상 분기, `:845`~854의 2자 경로, `:859` 이후 1자 경로. 새 fence 검사는 `_mask_mdx_fence`에 있지만 1·2자 경로는 이 함수를 거치지 않는다.

~~~~python
text = 'Example ' + chr(96) + 'literal\n{window.confirm("x")}\n~~~js\nclose ' + chr(96) + '\n~~~\n'
~~~~

- UTF-8 SHA-256: `1ab3683fcb583fb9cd9f8202ca546fe88d70c2fe779565567b0c68de09d1875c`.
- 임시 Git 저장소의 `Page.mdx`를 `safe\n`으로 커밋해 BASE를 만든 뒤 위 입력으로 바꾼다. `python tools/ux_lint.py --root TEMP --fail-new --json`과 여기에 `--base BASE`를 추가한 명령을 각각 실행했다.
- 기대: 실행식은 line 2의 새 추가행이고 문서 code span 밖이므로 P8·exit 1. 실제 양 OS: exit 0, `findings=[]`, traceback 없음.
- 독립 `markdown-it-py 4.2.0`의 `MarkdownIt('commonmark')` AST는 paragraph `[0,2]` + fence `[2,5]`다. 실행식은 일반 text 노드에 있고 뒤 backtick은 다른 fenced block 내용이다. 같은 문단에 정상 닫힌 대조는 `code_inline`이다. [CommonMark 0.31.2 block 우선](https://spec.commonmark.org/0.31.2/#precedence)·[code span](https://spec.commonmark.org/0.31.2/#code-spans) 기준으로 판정했다. 실제 MDX compiler 실행은 하지 않았다.
- 새 216교차/OS: plain/quoted/nested × 1/2/3/4자 run × 중간 tilde/더 긴 backtick/정상 닫힘 × LF/CR/CRLF × 전체/`--base`. 1·2자와 중간 fence의 조합 72개만 누락되고, 나머지 144개는 기대와 일치한다. Windows와 WSL을 별도로 실행했다.
- 영향: 신규 MDX 실행식에 baseline 예외가 없어도 소비자 fail gate가 통과한다. 인용 제외 규칙 자체를 없애거나 false positive로 해결할 문제가 아니다.
- 최소 수정: `_find_inline_span_end` 또는 모든 inline 경로가 공통의 block 경계 판정을 쓰도록 통일한다. 1·2·3·4자 모두 첫 유효 fence 앞에서 검색을 중단하고 뒤 실행식 스캔을 이어간다. 정상 닫힌 span, 4열/tab-stop, quoted/nested 및 `--base` 대조를 보존한다. 원인은 기존 B-P1-23과 같아 부분 수정 OPEN으로 남기며 새 P1로 중복 집계하지 않는다.

## 명령·검증 범위

Windows는 `py -3.14 -B -X utf8`, WSL은 `/home/digitie/.local/share/uv/python/cpython-3.11.15-linux-x86_64-gnu/bin/python3.11 -B -X utf8`를 사용했다. ROOT는 위 격리 worktree, AUDIT는 source `.git/codex-audit`이며 모든 임시 fixture와 결과 로그는 후보 밖에만 저장했다. 도구 실행 환경의 `GIT_*`를 제거했다.

```text
python AUDIT/t103-post32-b-run.py ROOT win|wsl tests
  -> 임시 독립 사본 unittest discover / contrast·UX focused / static·aliases focused
python AUDIT/t103-post32-b-run.py ROOT win|wsl corpus
  -> t103-post26/27/28/29/30/31-b-new.py 및 초기 경계 t103-post9-b-corpus.py
python AUDIT/t103-post32-b-new.py ROOT OUTPUT.json
python AUDIT/t103-post32-b-new.py ROOT unused oracle
python AUDIT/t103-post31-b-channels.py ROOT BASE_ROOT OUTPUT.json
git diff --check b2fc22b 2375c8b
```

base/candidate 출력 채널 8관찰/OS에서 B-P2-25 입력은 이전 코드의 네 채널 모두 exit 1/traceback에서 현재 네 채널 모두 exit 0/정상 출력으로 바뀌었다. 명시적·환경 summary가 요청됐을 때 생성됐고 입력 root 문자열 노출은 없었다. BASE_ROOT의 도구가 `b2fc22b` 코드와 같음을 `git diff` 무출력으로 확인했다.

exact 후보 CI는 `gh run list --commit 2375c8b052c94ec8982e0a4be294a747e75835b1`, `gh run view 34203724686 --json headSha,status,conclusion,jobs`로 직접 읽었다. [run 34203724686](https://github.com/digitie/kor-travel-common/actions/runs/34203724686)은 후보 headSHA, PR/completed/success, 6개 job과 각 source SHA 확인 step success다. 전체 job 로그는 NOT_RUN이다.

NOT_RUN: Windows Python 3.11(부재), 실제 소비자 build/type/e2e·manifest, npm/PyPI 설치·게시, workflow dispatch, MDX compiler/browser, WSL 독립 Markdown parser, WSL 별도 `git diff --check`, 이전 모든 개별 probe 전수 재실행. 문서/규범/task·패키지·버전·CI 경계는 이번 delta에서 불변이므로 이전 확인을 동일성으로 재사용했다. T-103은 IN_PROGRESS이며 소비자 gate를 완료로 대신하지 않는다.

## 실행 결과와 종료 상태

| 검증 | Windows Python 3.14.3 | WSL Python 3.11.15 |
|---|---|---|
| 전체 unittest | 305개 실행, skip 0, 226.003초, exit 0 | 305개 수집/302개 실행, skip 3, 43.688초, exit 0 |
| contrast/UX focused | 67개, skip 0, 57.504초, exit 0 | 67개, skip 0, 35.270초, exit 0 |
| aliases focused | 35개, skip 0, 1.419초, exit 0 | 35개 수집/34개 실행, skip 1, 0.273초, exit 0 |
| plan / links | 106 task 오류 0 / 487문서·2484대상 오류 0 | 동일 |
| SPDX / secrets / redaction | 56파일 오류 0 / 각각 619파일 발견·예외 0 | 동일 |
| versions self-check / aliases | exit 0(consumer NOT_RUN) / CSS 1 오류 0 | 동일 |

WSL skip 3은 Windows 8.3 전용 1개와 선택 jsonschema 부재 2개이며 성공한 시험으로 세지 않았다. Windows 첫 static helper가 작성 중인 본인 raw까지 복사한 488문서/620파일 결과는 후보 검증에서 폐기했다. 고정 SHA의 `git archive --format=zip 2375c8b...`만 별도 임시 경로로 추출해 `t103-post32-b-exact-gates.py ROOT`로 다시 실행한 487문서/619파일 결과만 위 표에 사용했다. 제품 파일은 바뀌지 않았다.

각 OS 1,001관찰 행을 수집해 9개 JSON 파일을 비교했고 모두 동일하다. 기존 26/27/28/29/30/31 그룹과 초기 경계 corpus는 72/144/216/48/120/72/105행(총777행), 새 교차는216행, 출력 채널 대조는8행이다. 기존 반례는 기대대로 수정됐고 새216행 중72개가 B-P1-23의 짧은 span 잔여다. 이 행 수는 중복 없는 테스트 수나 모든 과거 반례의 전수 검증을 뜻하지 않는다.

종료 결과 수집 KST `2026-09-08T17:30:04.0693138+09:00`. 제품 HEAD/tree는 위 후보와 동일하며 종료 status는 본인 raw 한 파일만 untracked, 제품 변경 없음이다. source `.git/config` 종료 해시도 시작 값과 같다. 원본 파일만 포함한 커밋 후 clean·raw tree·파일/Git blob 동일 SHA-256을 확인해 완료 메시지로 전달한다.
