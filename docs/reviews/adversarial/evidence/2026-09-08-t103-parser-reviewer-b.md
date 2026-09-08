# T-103 실제 MDX 파서 전환 독립 적대적 리뷰 B

## 판정·불변 기준선

- 최종 **PASS**, full review. 새 P0/P1/P2/P3 finding은 각각 0건이다. `B-P1-30`, `B-P2-31`, `B-P2-32`는 원 심각도를 유지하여 **FIXED**로 판정했다.
- 실행 ID `T103-PARSER-B-20260908-194900`; 시작 KST `2026-09-08T19:49:00.9925454+09:00`, 제품 검증 종료 KST `2026-09-08T19:54:58.7725934+09:00`.
- 시작·종료 제품 HEAD `31e3f0affd2ce1c32ac912bedf687d82c12ee876`, tree `249c38a4fab91903f9536c6c7f6c938efeab0445`.
- delta base `196a8a37754848bb3fabef6c5bb9e5c2dd275608`; 18파일 전체 변경(2,288줄 추가·603줄 삭제)을 검토했다. Python adapter·MDX helper·lock·CI·시험·ADR·task·도구/환경 문서·evidence가 포함된다.
- manifest는 `git show 71dc7c2a806caa87738ea9b5da6ab9c896db5980:docs/reviews/adversarial/evidence/2026-09-08-t103-parser-manifest.md`로 읽었다. 해당 Git blob SHA-256은 `9b5dbe67d8a34f58c9b27a02afcfc4fdf373e95da7087e3da54142c7b88c3c6c`이다.
- 격리: `review-t103-parser-b` detached worktree. 시작·설치 후·제품 검증 종료 `git status --porcelain` 모두 빈 출력이다. WSL은 동일 후보의 `git archive`를 별도 임시 디렉터리에 풀어 설치·시험했다. 원본 보고서 한 파일만 후속 커밋한다.
- source `.git/config` 시작·종료 SHA-256 동일: `0A0F849E7874CF0A25926856F9D2E381CCBF4C2DCB5999869C57B86E0F5BEB5B`. Git 설정·제품·manifest·소비자·기존 evidence를 수정하지 않았다. 상대 reviewer의 이번 원본/결과를 읽거나 요청하지 않았다.

공통 전달 요청 원문:

> 36회 반복 원인이던 수동 MDX 파서를 제거하고 실제 구문 분석으로 전환한 전체 delta를 검토한다. 두 reviewer 모두 이 manifest의 동일 불변 후보에서 작업한다. 별도 detached worktree의 시작·종료 HEAD/tree·clean을 확인하고, 그 worktree 루트에서 `npm ci --ignore-scripts`로 잠긴 의존을 설치한다. 제품·시험 파일을 수정하지 않고 한국어 원본 report 하나만 별도 commit한다. 상대의 이번 결과는 두 원본 확정 전 읽거나 전달받지 않는다. 실행 ID·역할·시각·전달 요청·실제 명령·관찰과 미검증을 구분한다.

B 전문 범위는 Node·lock·설치·CI, 실패 exit 2·정보 보호·소스 실행 금지, Git CLI·기존 finding·evidence 정합이다. 현재 [ADR-016](../../../adr/016-mdx-parser-for-ux-lint.md), [T-103](../../../tasks/T-103-kt-contrast-ux-lint.md), [agent workflow](../../../runbooks/agent-workflow.md)를 적용했다.

## 직접 실행

| 항목 | 실제 명령·결과 |
|---|---|
| Windows 환경 | Python 3.14.3, Node 25.9.0, npm 11.12.1. 로컬 Node가 root `engines.node ^22.12.0` 밖이라 `npm ci`에서 EBADENGINE 경고가 났다. 이 실행을 정본 Node 22 실행으로 세지 않는다 |
| WSL 환경 | 명시 경로의 uv Python 3.11.15, Node 22.22.2, npm 11.19.1. Node는 선언 범위 안이다 |
| 설치 | 새 Windows worktree와 WSL 임시 archive 각각 `npm ci --ignore-scripts`: 113패키지 설치, 115 감사, exit 0. 제품 lock 변경 없음 |
| Windows 전체 | `py -3.14 -B -X utf8 -m unittest discover -s tests -p 'test_*.py'`: **320 실행·성공, skip 0**, 242.381초, exit 0 |
| WSL 전체 | `/home/digitie/.local/share/uv/python/cpython-3.11-linux-x86_64-gnu/bin/python3.11 -B -X utf8 -m unittest discover -s tests -p 'test_*.py'`: **320 수집·317 실행·성공, skip 3**, 81.049초, exit 0. skip은 Windows 전용 1·선택 jsonschema 2이며 성공 건수에 포함하지 않는다 |
| AST 기대값 대조 | 양 OS `node tests/verify_mdx_reference.mjs node_modules/@mdx-js/mdx/index.js`: MDX 3.1.1, 492 PASS, 실패·제외 0, exit 0 |
| 별도 CLI 매트릭스 | 이전 B 최소 반례와 정상 대조 12입력 × plain/blockquote/nested × LF/CRLF/CR = 108입력. 일반 fail-new·새 추가행·기존행 3모드, 양 OS **각 324행, 불일치 0**. 기존행 fail 합계 0 |
| 실제 실패 주입 | 잘못된 MDX+정상 파일 혼합, Node 부재, 잠긴 파서 부재: exit 2. 혼합 입력의 JSON/Markdown/summary에서 부분 report·원문·로컬 경로·stack 노출 0. MDX 없는 TSX는 Node 없이 finding 1을 정상 보고 |
| 소스 실행 금지 | 파일 쓰기 import/ESM과 NODE_OPTIONS preload를 포함한 합성 입력: 양 OS 파싱·finding 보고 성공, 표식 파일 생성 0, stderr 빈 출력. NODE_OPTIONS/NODE_PATH 제거 및 compile/evaluate 미호출을 코드로 확인 |
| airport | canonical+airport-overrides+baseline: light 미달 4·신규 0/exit 0; dark 미달 10·신규 6/exit 1. 양 OS 동일 |
| 문서·계획·고지 | 양 OS `validate_document_links.py`: 507문서·2537대상 오류 0, `validate_plan.py`: 106 task 오류 0, `check_spdx.py`: 59파일 오류 0 |
| 정보·정본 | Windows `scan_secrets.py --all`, `check_prod_redaction.py --all`: 각각 643파일/finding 0; `check_versions.py --self-check`: exit 0. 다른 OS의 실제 전체 트리 정보 검사는 아래 CI 결과와 구분한다 |
| diff | `git diff --check 196a8a37754848bb3fabef6c5bb9e5c2dd275608 31e3f0affd2ce1c32ac912bedf687d82c12ee876`: exit 0 |

전체 회귀는 CSS·대비·baseline, redaction·오류, symlink/root, `+++`·CR/CRLF/LS/PS 추가행, 문맥·좌표·실패 주입 시험을 포함한다. 시간 초과는 제공 시험의 `TimeoutExpired` 주입을 실행한 것이며 실제 30초 대기로 재현했다고 세지 않는다. 전체 시험 수를 개별 변형 수와 합산하지 않는다.

## 기존 finding 재판정

| ID·원 심각도 | disposition | 독립 재현 근거 |
|---|---|---|
| B-P1-30 | FIXED | ``{"test" in /}/ && `outline-none`}``의 P6 1건이 일반·추가행에서 검출된다. 정규식 직접 시작 대조도 동일. 각 9개 컨테이너/줄바꿈 변형의 report·추가행·기존행 결과 일치 |
| B-P2-31 | FIXED | `{1<a ? "yes" : "no"}` 뒤 tilde fence의 `window.confirm`을 제외한다. `<` 주위 공백이 있는 정상 대조와 verdict가 같다. 각 9변형에서 오탐 0 |
| B-P2-32 | FIXED | [도구 evidence](../../../evidence/t103-kt-contrast-ux-lint.md)에서 airport dark를 미달 10·baseline 신규 6·exit 1로 정정했다. 후보 CLI 양 OS 재실행과 일치하며 예제 CSS·baseline을 바꾸어 성공시키지 않았다. 실제 dark gate는 T-431 외부 선행으로 유지 |

직전까지 닫은 B-P1-28/B-P2-27/B-P2-29의 URL·apostrophe·실제 JS 주석 대조도 위 108입력 안에서 유지됐다. 더 앞선 누적 문제는 전체 회귀로 확인했으며 과거 모든 raw를 다시 읽거나 각 원문을 수작업으로 재실행했다고 주장하지 않는다. 후보가 바꾼 본문 `const`/`//`, indented code, 잘못된 여러 줄 JSX 기대값은 ADR-016의 실제 MDX 문법 계약에 연결돼 있다. 검사 대상을 삭제한 것으로 해석하지 않았다.

## 설치·신뢰 경계·CI 확인

`package.json`의 루트 개발 의존 `@mdx-js/mdx`는 exact 3.1.1이고 lock과 설치본이 같다. lock의 외부 112패키지 모두 registry.npmjs.org의 고정 resolved·integrity·dev 표시가 있으며 install script 표시는 0개다. 라이선스 필드는 MIT·ISC·BSD-3-Clause이고 제품 helper는 GPL-3.0-or-later 고지를 갖는다. 기존 workspace 링크는 로컬 tokens다. `package-lock.json` SHA-256은 `a0433e458da574cda6fec93e89bcdb3f3afdcb3e89136d7a73adcf715e77ed43`이다.

Python은 MDX 파일이 있을 때만 Node를 한 번 호출하여 stdin에 소스 배열을 전달한다. helper는 고정 `createProcessor().parse`만 호출하고 사용자 파일의 import를 resolve/evaluate하지 않는다. adapter는 실행 실패·JSON 형식·항목 수·error·문자 수·줄 종결자 보존을 검사한 뒤에만 report를 만든다. Node 실패 stderr를 공개 출력으로 전달하지 않는다. 실제 부재/문법 오류 주입과 전체 시험의 비정상 반환·timeout 주입이 이 경계를 확인했다.

`gh run view <run> --json headSha,status,conclusion,jobs`로 직접 관찰했다.

- 코드 SHA `31e3f0a...`의 run `34217256747`: **cancelled**. packages/secret-scan/check-versions 성공, docs/양 OS tools 취소. 전체 PASS가 아니다.
- manifest SHA `71dc7c2...`의 run `34217374527`: **completed/success**, 6개 job 모두 success. `git diff --name-only 31e3f0a... 71dc7c2...`는 manifest 한 파일 추가뿐이다. 이 CI를 코드 SHA 자체의 완료 run으로 바꾸어 표시하지 않는다.
- workflow는 고정 setup-node SHA·`.nvmrc`·npm 11.19.1 설치·`npm ci --ignore-scripts`를 Python 전체 시험 전에 실행한다. source SHA 확인·read 권한·credentials 미보존 계약은 유지한다. CI 시험 수는 로컬 실행 결과와 합산하지 않는다.

정본 Node 22의 Windows 로컬 실행은 하지 않았다. 해당 경계는 같은 제품/시험의 CI Windows Node 설치와 성공으로 확인했고, WSL은 선언 범위의 Node 22로 직접 실행했다. MDX 파서는 이제 제품과 기대값 대조가 함께 쓰는 의존이므로 492건 결과를 서로 다른 두 파서의 독립 일치로 주장하지 않는다. reviewer가 별도 입력·실패 주입·adapter·기대값을 독립 검토했다.

## 재현 자료·미실행

제품 바깥 `.git/codex-audit/t103-parser-b-probe.py`를 Windows에서는 `py -3.14 -B -X utf8 ... <review worktree> win`, WSL에서는 명시적 Python 3.11과 같은 후보의 임시 archive를 인자로 실행했다. 보조 스크립트는 임시 Git 저장소의 빈 파일 commit → 입력 추가 → 현재 입력 commit을 만들어 세 모드를 비교하고, 별도 임시 root에서 실패·비실행·airport 대조를 수행한다. source/consumer 설정은 변경하지 않는다.

| 자료 | SHA-256 |
|---|---|
| `t103-parser-b-probe.py` | `c5941249f619c360a96e4ef8f80da9660754c98e1a41082b44349f251a410f7a` |
| `t103-parser-b-win-probes.json` | `cc58e142624320fe85dd7666d2f88980d4a3221c384e6823a739be5a6d5e653b` |
| `t103-parser-b-wsl311-probes.json` | `053331c7c57700a4052f61e774476728a6c05a6c2270b0195bd0464f45e85011` |

- `NOT_RUN(Windows Python 3.11 로컬 실행 파일 부재)`, `NOT_RUN(Windows 로컬 Node 22 실행)`: CI 실행과 구분했다.
- `NOT_RUN(WSL jsonschema 2시험, Windows 전용 1시험)`: skip을 성공으로 세지 않았다. 로컬 Windows 전체는 skip 0이다.
- `NOT_RUN(실제 MDX compile/render/browser·소비자 build/e2e·커스텀 플러그인·실제 앱 baseline 채택)`: T-103 도구 검증으로 외부 gate를 닫지 않는다.
- `NOT_RUN(npm/PyPI 게시·Release 게시·workflow dispatch)`: 사용자 범위 밖이며 수행하지 않았다. 공용 라이브러리 소비 자체에 이 도구의 Node 의존을 추가하지 않는다.

현재 범위에서 수정이 필요한 신규 finding은 없다. 이 원본은 해당 immutable 후보의 full review PASS이며, PR 병합이나 다음 task 착수를 수행했다는 기록이 아니다.
