# T-103 실제 MDX 파서 전환 독립 리뷰 A 원본

- 실행 ID: `T103-PARSER-A-20260908-194846-KST`; 최종 verdict: **BLOCK**.
- 시작: 2026-09-08 19:48:46.187 KST; 제품 검토 종료: 2026-09-08 19:56:43.607 KST.
- 제품 후보 HEAD: `31e3f0affd2ce1c32ac912bedf687d82c12ee876`; tree: `249c38a4fab91903f9536c6c7f6c938efeab0445`.
- delta base: `196a8a37754848bb3fabef6c5bb9e5c2dd275608`; 공통 manifest: `71dc7c2a806caa87738ea9b5da6ab9c896db5980`의 `docs/reviews/adversarial/evidence/2026-09-08-t103-parser-manifest.md`를 `git show`로 확인했다.
- 격리 경로: `F:/dev/kor-travel-common-wt/review-t103-parser-a`. 시작·종료 HEAD/tree가 위 값과 같고 `git status --short` 출력은 모두 비어 있었다. 이후 원본 한 파일만 추가한다.
- 전달 요청: “36회 반복 원인이던 수동 MDX 파서를 제거하고 실제 구문 분석으로 전환한 전체 delta를 검토한다.” A 범위는 실제 AST 마스킹, Unicode 좌표, 정상 MDX와 기존 시험 기대값 변경 근거 및 자신의 누적 finding이다.
- 이번 상대 결과·raw를 읽거나 요청하지 않았다. 후보·소비자·기존 evidence·manifest·git config를 수정하지 않았다. 검증용 의존과 자기 임시 fixture만 설치·생성했다. 이번 변경은 규범과 실행 의존 및 제품 구현 변경이므로 full review 대상으로 판단했다.

## 계약·구조와 기존 finding

18파일 delta를 구현·시험·의존·문서 단위로 확인했다. ADR-016은 ADR-003의 MDX 실행 요구만 대체하고, Node 요구·잘못된 MDX의 exit 2·수동 fallback 금지·사용자 소스 parse-only를 task·개발 문서·CHANGELOG·CI에 연결한다. 본문 const·행 주석 추정과 CommonMark indented code 가정을 제거한 시험 변경은 명시한 실제 MDX 계약에 따른다. 잘못된 여러 줄 JSX는 ESM 뒤 빈 줄과 quote continuation을 갖춘 입력으로 바뀌었으며 실제 유효 입력의 패턴을 삭제해서 통과시키는 변경은 확인하지 못했다.

제품과 기대값 대조 스크립트가 같은 3.1.1 파서를 사용한다는 한계를 문서가 명시한다. 본 리뷰는 그 두 스크립트의 일치만으로 adapter를 승인하지 않고, 직접 작성한 원문·기대 마스킹과 실제 CLI 좌표를 대조했다. 그 결과 아래 선행 BOM 위치 보정 누락을 발견했다.

| 원 finding | disposition·근거 |
|---|---|
| A-P1-35 | **FIXED**. ESM 다음 줄의 삼항·member 호출·instanceof tagged template를 검사하고 주석은 제외한다. 기존 독립 90변형 및 42 CLI가 현재 모두 기대와 일치한다 |
| A-P2-36 | **FIXED**. 비교 `<`와 실제 JSX를 구별해 주석·후속 fence를 제외한다. 위 기존 독립 변형·CLI 및 저장소 누적 자료로 확인했다 |
| A-P1-37 | **FIXED**. Airport dark 실행은 여전히 10미달·예외4·신규6·exit1이며 evidence는 이 결과를 정확히 기록한다. 조사 예제·baseline을 임의 변경하지 않고 light/dark 실행과 외부 T-431 gate를 구분했다 |
| A-P1-31/32, A-P2-33/34 및 opener·미종결 span·주석 경계 | 현재 누적 자료와 기존 UX 집중 시험의 원 반례는 **FIXED**. 과거 수동 parser의 비표준 MDX 호환 가정은 ADR-016의 문법 변경과 구분하며, 과거 모든 임시 스크립트를 새로 실행했다고 주장하지 않는다 |

## 직접 실행·재사용·미완료

- `npm ci --ignore-scripts`: 성공, 113개 설치. lock delta는 신규 항목112개와 root devDependency 변경이고 기존 비-root 항목 변경은 없었다. 신규 외부 항목의 integrity 누락0, `@mdx-js/mdx`는 3.1.1이다. 로컬 Windows Node v25.9.0/npm11.12.1은 engine `^22.12.0` 경고를 냈다. 이 실행을 지원 Node22 검증으로 표시하지 않는다. WSL 직접 실행은 Node v22.22.2·Python3.11.15였다.
- Windows Python3.14.3: `python -B -X utf8 -m unittest tests.test_ux_lint tests.test_ux_mdx_context` **59개 성공·skip0·142.910초**.
- `node tests/verify_mdx_reference.mjs node_modules/@mdx-js/mdx/index.js`: **492 PASS·제외0·exit0**. 이는 같은 파서로 저장소 기대값을 대조한 결과다.
- 이전 독립 `t103-root-a-matrix.py`를 Windows에서 새 후보 대상으로 실행: **90/90 문법·패턴 대조 일치**, plain/base CLI42회 기대 일치. WSL에서 이 이전 전체 matrix를 별도 재실행하지 않았다.
- 독립 Unicode fixture: 양 OS 각각 **120개 원문 중111개 정확한 마스킹·9개 BOM 범위 불일치**. BMP·astral emoji·결합문자·ZWJ·FEFF와 inline/fence/comment/속성/ESM/template/줄 주석·LF/CRLF/CR를 조합했다. 120파일의 batch CLI에서는135 finding의 파일·행·열·패턴이 기대와 일치했고 summary가 생성됐다. 이 fixture의 범위 불일치를 패턴 누락으로 확대한 별도 시험은 다음 항목이다.
- 독립 BOM fixture: 양 OS 각각 **18입력**(BOM0/1/2×줄바꿈3×주석2), **36회 plain/base CLI**. BOM 없는6입력은P8·exit1, BOM 있는12입력은P8누락·exit0이다. 결과는 한 finding으로 묶었다. traceback은 없다.
- 정적 gate 직접 실행: link507문서·2537대상 오류0, plan106 task 오류0, SPDX59파일 오류0, secret/redaction 각643파일 finding0, versions self-check PASS, `git diff --check 196a8a3 31e3f0a` 오류0.
- Airport 직접 명령: `python -B -X utf8 tools/kt_contrast.py packages/tokens/tokens.css packages/tokens/examples/airport-overrides.css --dark --baseline packages/tokens/examples/airport.contrast-baseline.example.json --fail-new --json`; **exit1**, 현재 정정 evidence와 일치한다.
- WSL59 집중 시험은 NTFS Node 의존 로딩으로 장시간 실행돼 중단했다. 자기 격리 cwd와 정확한 unittest 인수를 확인한 해당 프로세스에만 SIGINT를 전달했고 종료exit1·KeyboardInterrupt는 리뷰어 중단 결과다. **NOT_RUN(완료되지 않은 중복 집중 시험)**이며 성공 건수로 집계하지 않는다. 양 OS의 위 Unicode·BOM 직접 검증은 중단 전에 완료됐다.

전체320시험은 이번 직접 실행으로 세지 않는다. manifest의 작성자 Windows320성공·skip0을 재사용한다. coordinator가 통보한 CI Windows318성공+2skip, Ubuntu317성공+3skip도 자기 실행 수와 구분한다. CI의 정확한 후보 [34217256747](https://github.com/digitie/kor-travel-common/actions/runs/34217256747)은 cancelled였고, manifest HEAD `71dc7c2a806caa87738ea9b5da6ab9c896db5980`의 [34217374527](https://github.com/digitie/kor-travel-common/actions/runs/34217374527)은 직접 조회한6 job 모두success다. `git diff --name-only 31e3f0a 71dc7c2`로 차이가 manifest 한 파일뿐임을 확인했다. 개별 CI 시험 수는 coordinator 통보이며 이 리뷰에서 전체 job 로그를 다시 감사하지 않았다.

## A-P1-38 — P1, OPEN / FIX_REQUIRED: 선행 BOM과 AST offset의 기준 차이로 실제 P8 누락

- 위치: `tools/mdx_mask.mjs:7`의 parse와 13–17행의 AST 범위 수집, 32–42행의 원문 offset 적용. 파서가 소비한 선행 BOM을 원문 좌표로 보정하지 않는다. Python adapter의 길이·줄 종결자 검사만으로는 범위의 한 문자 이동을 찾지 못한다.
- 최소 입력: 선행 **U+FEFF** 한 문자 뒤 `{window.confirm/* sample */("live")}`. UTF-8 BOM을 갖는 정상 MDX이며 실제 사용자 코드를 실행하지 않고 parse·검사만 했다. 줄 주석을 넣고 다음 줄에서 호출 괄호를 여는 정상 입력도 동일하다.
- 실제 AST 관찰: BOM0의 원문 주석start15/AST15, BOM1의 원문start16/AST15, BOM2의 원문start17/AST16이다. 고정 parser는 세 입력을 모두 정상으로 받아들이며 선행 BOM 하나를 제외한 좌표를 반환한다.
- 기대/실제: 주석만 가리고 `window.confirm`을 보존해P8·exit1이어야 한다. 현재는 주석 시작보다 한 문자 앞의 마지막 `m`을 가려 `window.confir`로 바꾸고 주석 끝 일부를 남긴다. 그 결과 finding0·exit0이다. BOM1/2·LF/CRLF/CR·block/line 주석의12입력과 plain/base24회에서 양 OS 동일하게 재현했다. BOM0의6입력·12회 CLI는 정상 대조다.
- 영향: 실제 코드의 필수 UX 패턴 검사가 조용히 통과한다. 이모지 자체의 UTF-16/Unicode 길이 환산은 대체로 맞지만, 파서 입력 전처리와 원문 좌표의 차이는 별도 계약이다.
- 최소 수정·수용 조건: 파서가 소비한 선행 BOM을 명시적으로 처리하고 모든 code/inlineCode/comment 범위를 원문 기준으로 변환한다. 원문 BOM을 유지할 때의 좌표와 BOM 없는 입력을 함께 검증한다. 정상·이중 FEFF·주석 바로 앞 패턴·AST 범위 경계·Unicode 혼합 fixture를 원문 마스킹 기대값과 CLI/base까지 검사해야 한다. BOM 파일을 통째로 제외하거나 조용히 PASS 처리하는 방법은 수용하지 않는다.

## 재현 자료와 종료

자기 외부 자료는 주 checkout `.git/codex-audit/`의 `t103-parser-a-unicode.py`, `t103-parser-a-bom.py`, `t103-parser-a-bom-ast.mjs`, `t103-parser-a-{win,wsl}-bom.log`, `t103-parser-a-{win,wsl}-tests.log`, `t103-parser-a-win-old-matrix.log`, `t103-parser-a-airport.json`에 있다. Windows 명령은 `python -B -X utf8 <helper.py> F:/dev/kor-travel-common-wt/review-t103-parser-a`, WSL은 로그인 bash의 `uv run --no-project --python 3.11 python -B -X utf8 <동일 helper의 /mnt/f 경로> /mnt/f/dev/kor-travel-common-wt/review-t103-parser-a`다. `node <t103-parser-a-bom-ast.mjs>`가 위 원문/AST 주석 offset 세 건을 출력한다.

- `NOT_RUN`: 로컬 Windows Node22·Python3.11, 직접 전체320시험, 중단한 WSL59 집중 시험, 소비자 build/e2e·버전 검사, 실제 MDX compile/render/browser, npm/PyPI 게시. CI의 Node22 성공을 로컬 실행으로 대체 표기하지 않는다.
- 신규 P0 0·P1 1(A-P1-38)·P2 0·P3 0. 기존 세 finding의 FIXED와 별도로 새 P1이 있으므로 최종 **BLOCK**이다. 후보는 불변이며 원본 보고서 한 파일만 커밋한다. commit SHA·파일 SHA256·최종 clean 상태는 완료 메시지로 전달한다.
