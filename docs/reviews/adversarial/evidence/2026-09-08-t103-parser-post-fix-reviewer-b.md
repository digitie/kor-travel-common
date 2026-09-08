# T-103 MDX BOM 보정 독립 사후 리뷰 B

## 판정·실행 기준

- **PASS**. 새 P0/P1/P2/P3 finding 각각 0건. B-P1-30/B-P2-31/B-P2-32의 FIXED 판정은 유지되며, A-P1-38의 BOM 최소 반례도 이번 B 독립 실행에서 해결을 확인했다.
- 실행 ID `T103-PARSER-POST-B-20260908-200114`; 시작 KST `2026-09-08T20:01:14.4637645+09:00`, 제품 검증 종료 KST `2026-09-08T20:04:13.3510487+09:00`.
- 시작·종료 제품 HEAD `49d3867fd8fb941fde260966d2b4b3296c0f3d77`, tree `e2bfb5702ad976bfda5d47ddc6e52f2f735e440b`, detached `review-t103-parser-post-b` worktree. 두 시점과 설치 후 `git status --porcelain`은 빈 출력이다.
- 제품 delta 기준 `31e3f0affd2ce1c32ac912bedf687d82c12ee876`. 제품·시험 변경 4파일 전체를 읽었다: `mdx_mask.mjs`의 7줄 offset 변환, 대조 스크립트, 누적 입력 2개, 회귀 시험 2개. Git 전체 diff에는 앞선 parser manifest 추가 1파일도 포함된다. 제품·manifest·기존 evidence는 수정하지 않고 이 원본 한 파일만 후속 커밋한다.
- `git show ef91306f3c29ec0bd753df4229428b6eb90965c4:docs/reviews/adversarial/evidence/2026-09-08-t103-parser-post-fix-manifest.md`로 공통 요청을 읽었다. manifest blob SHA-256: `9c9ae6ad30768e79d40767d8e80772d57cf8f4c54f5d917c69283b9932e44ad5`.
- source `.git/config` 시작·종료 SHA-256 동일: `0A0F849E7874CF0A25926856F9D2E381CCBF4C2DCB5999869C57B86E0F5BEB5B`. source/consumer 파일·Git 설정은 수정하지 않았다. 이번 상대 원본/결과는 읽거나 요청하지 않았다.

공통 요청 원문:

> 두 reviewer는 위 동일 후보의 별도 detached worktree에서 시작·종료 HEAD/tree·clean을 확인한다. `npm ci --ignore-scripts`로 해당 후보의 의존을 설치하고, 제품과 시험은 수정하지 않는다. 원본 `2026-09-08-t103-parser-post-fix-reviewer-{a,b}.md` 하나만 별도 commit한다. 실행 ID·시각·역할·입력 요청·실제 명령·미실행·verdict를 기록하고 두 원본 확정 전 상대의 이번 결과를 공유하지 않는다.

B는 전체 수정 delta가 Git CLI·실패 처리·누적 B finding·evidence에 미치는 영향을 독립 확인했다. 기준은 [ADR-016](../../../adr/016-mdx-parser-for-ux-lint.md), [T-103](../../../tasks/T-103-kt-contrast-ux-lint.md), [workflow](../../../runbooks/agent-workflow.md)다. 범위는 기존 full 리뷰의 사후 검토이며 제품의 새 요구는 추가하지 않았다.

## 직접 실행 결과

| 검증 | 명령·결과 |
|---|---|
| 설치·환경 | Windows 새 worktree와 WSL 동일 SHA의 임시 `git archive`에서 각각 `npm ci --ignore-scripts`: 113패키지 설치/exit 0. Windows Python 3.14.3·Node 25.9.0·npm 11.12.1, WSL uv Python 3.11.15·Node 22.22.2·npm 11.19.1. Windows Node의 기존 EBADENGINE 경고는 정본 Node 22 실행으로 세지 않는다 |
| 집중 회귀 | `python -B -X utf8 -m unittest tests.test_ux_mdx_context`: 양 OS 8실행·성공/skip 0, Windows 16.292초·WSL 2.041초, exit 0. 제공 시험의 BOM 원문 54경우·18파일 CLI와 누적 자료·delimiter를 포함 |
| 별도 BOM 마스킹 | reviewer가 직접 구성한 90입력에서 원문과 기대 마스크 전체 문자열·길이 일치, 실행 P8 정확히 1건. BOM 0/1/2/3개·공백 뒤 BOM·emoji 뒤 BOM, LF/CRLF/CR, 인접 block/line comment·주석 안 BOM·inline code·fence 포함. 양 OS 불일치 0 |
| 별도 BOM CLI | 위 90파일을 일반 fail-new·신규 추가행·기존행의 세 모드로 검사: 양 OS 각 270관찰. 일반/신규는 P8 90·fail 90/exit 1, 기존행은 P8 90·fail 0/exit 0. 줄 번호 일치, stderr 빈 출력 |
| 기존 B corpus | 108입력 × 3모드, 양 OS 각 324관찰 모두 기존 독립 기대값과 일치. 이전 regex·비교식·URL·apostrophe·JS 주석·컨테이너·CR 계열 회귀 없음 |
| 실제 실패·비실행 | 잘못된 MDX와 정상 파일 혼합의 JSON/Markdown/summary, Node 부재, 파서 부재 모두 exit 2·원문/경로/stack 노출 0·부분 성공 출력 0. MDX 없는 TSX는 Node 없이 보고. 사용자 파일 쓰기 import/ESM·NODE_OPTIONS preload의 표식 파일 생성 0. 양 OS 직접 재실행 |
| AST 기대값 | 양 OS `node tests/verify_mdx_reference.mjs node_modules/@mdx-js/mdx/index.js`: MDX 3.1.1, 498 PASS/실패·제외 0, exit 0 |
| 문서·계획·고지 | 양 OS `validate_document_links.py`: 508문서·2542대상 오류 0, `validate_plan.py`: 106 task 오류 0, `check_spdx.py`: 59파일 오류 0 |
| 정보·diff | Windows `scan_secrets.py --all`, `check_prod_redaction.py --all`: 각 644파일/finding 0. `git diff --check 31e3f0a... 49d3867...`: exit 0 |

별도 BOM 기대값은 후보의 AST offset 보정식을 복제하지 않고 입력에서 명시한 문서/주석 문자열만 공백으로 바꾸어 만들었다. 첫 BOM 이후의 다른 FEFF는 원문 문자로 보존해야 한다. 제품 보정은 첫 문자에 한해 offset 1을 모든 range에 한 번 적용하고, 기존 UTF-16/Unicode 변환과 줄 종결자 보존은 그대로 사용한다. 직접 문자열 일치와 CLI 재현이 이 경계를 확인했다. 대조 스크립트와 제품은 같은 MDX 파서를 쓰므로 498건을 독립된 두 파서의 일치라고 주장하지 않는다.

## finding disposition

| 원 ID·심각도 | 이번 관찰·판정 |
|---|---|
| A-P1-38 | 첫 U+FEFF 뒤 `{window.confirm/* 숨김 */("실행")}`가 P8로 유지된다. 주석 직전 마지막 `m`을 가리지 않으며 BOM/emoji/line comment·fence/inline 변형과 추가행에서도 동일. **독립 재현에서 FIXED 확인**; 원 reviewer의 별도 판정을 대신하지 않는다 |
| B-P1-30 | `in` 뒤 `/}/`와 실행 template P6 유지. 108입력의 일반/추가행/기존행 재실행에서 **FIXED 유지** |
| B-P2-31 | 공백 없는 `<` 비교 뒤 fenced 문서 P8 오탐 0, 공백 대조와 일치. **FIXED 유지** |
| B-P2-32 | airport light 미달 4·신규 0/exit 0, dark 미달 10·신규 6/exit 1을 양 OS에서 다시 확인. 정정 evidence·외부 T-431 gate와 일치. **FIXED 유지** |

기존 B-P1-28/B-P2-27/B-P2-29도 별도 corpus에서 유지됐다. Node adapter·package/lock·CI·문서 정본은 직전 검토와 동일하고, 이번 입력 오류·실행 금지 재현에서도 변경에 의한 회귀를 발견하지 못했다.

## CI·재사용·미실행

- 직접 `gh run view 34218404453 --json headSha,status,conclusion,jobs`로 **completed/success, 6개 job 모두 success**를 확인했다. source는 `ef91306f3c29ec0bd753df4229428b6eb90965c4`다. `git diff --name-only 49d3867... ef91306...`는 앞선 확정 A/B raw와 새 manifest뿐이며 제품·시험 변경은 없다. 이 실행을 코드 SHA 자체의 run이라고 바꾸어 기록하지 않는다.
- **전체 322시험은 이번 reviewer가 재실행하지 않았다.** 작성자가 동일 제품이라고 귀속한 `.git/codex-audit/t103-bom-win-full.log`를 읽어 322 실행/skip 0/190.810초/OK를 확인하고 재사용 evidence로 구분했다. 이전 후보의 reviewer 전체 320시험과 중단된 작성자 WSL 실행을 이번 후보 성공 건수로 세지 않는다.
- `NOT_RUN(Windows 로컬 Python 3.11·Node 22)`: 이번 로컬 Windows 환경과 CI의 별도 지원 환경 검증을 구분한다.
- `NOT_RUN(이번 reviewer의 전체 시험 중복 실행·실제 30초 timeout 대기)`: 집중 시험의 timeout 주입은 실행했다.
- `NOT_RUN(실제 MDX compile/render/browser·소비자 build/e2e·실제 앱 baseline·커스텀 플러그인)`, `NOT_RUN(npm/PyPI·Release 게시·workflow dispatch)`: 외부 gate는 그대로 남는다.

재현 스크립트는 제품 밖 `.git/codex-audit/t103-parser-post-b-bom.py`를 Windows/WSL에서 후보 경로와 OS label로 실행했다. SHA-256 `28eee97f659c15d679242af034b1eff23288e77e98f9aba138328b65e32d8274`. 입력·전체 마스크 비교와 CLI 결과 원본 `t103-parser-post-b-win-bom.json`의 SHA-256은 `c89d305fe82e1c6ef83dca13d87c3cd48a21fda02fb5fdf869c632ff723c9403`, WSL 원본 `t103-parser-post-b-wsl311-bom.json`은 `85a36999a988c1c33e43a775a33442daad12978773bcf095183d5767f7c46bce`다. 기존 B corpus·실패 주입은 이전 독립 보조 스크립트에 이번 후보 경로를 주어 새로 실행했다.

새 수정 요구는 없다. 이 원본만 커밋하고 후보를 고치지 않는다. 현재 PR 병합·다음 task 실행은 수행하지 않았다.
