# COMMON4 원 리뷰어 B 수정 후 재검토 원문

- reviewer: **B / Epicurus**, 구현 비참여. packaging/dependency/lock/CI/license 관점의 독립 read-only 리뷰.
- runid: `Epicurus-B-common4-20261111T170200Z`
- UTC: 시작 `2026-11-11T17:02:00Z`, 종료 `2026-11-11T17:14:39.013951+00:00`.
- manifest SHA256: `e5c7101e4130b4bf66c90a8ef2e54f3c672c5a79f0eeb8216bfc9ebcaa85c951` — 요청과 실제 일치.
- observed common SHA: `2ec519255ec1af9fca18856d980e968ee15b80a8`.
- **verdict: PASS — 이번 불변 common/VWorld source·c9 artifact·필수 CI 범위.**
- **B-P1-08/09/10 모두 FIXED. 신규 P0/P1/P2/P3 없음.** 기존 원문과 당시 BLOCK/CONDITIONAL은 변경하지 않는다. 소비자 최종 채택·export·배포는 별도다.

## 기준선과 실행 경계

`review-manifest-common-4.json`을 직접 읽고 hash를 확인했다. 이전 head는 `7e3f33e0391990b9312fee513de581e28035aa8b`, 최초 base는 `c289b4624c8640eb918cc915803e72ae754e58fb`다. c9 common producer는 `2c1182e765bb2bc53e01e0962cf2a73683891e1d`, artifact는 `artifacts/integration-9-review`의 CANDIDATE_NOT_RELEASED다. VWorld는 이전과 같은 `9a7a348b02d61969b394c681b024d5851eef836b`이다.

자체 detached worktree `/tmp/review-b-common4-20261111-170200`에서 Git diff/object와 파일을 읽고 테스트했다. 소스·lock·원 artifact를 수정하거나 신규 install하지 않았다. 기존 `/home/digitie/dev/common-unification-20261111/kor-travel-common/node_modules`를 도구 실행에만 참조했다. Python MDX 실행에는 임시 symlink가 필요했으며 종료 전에 제거했다. 최종 HEAD는 요청 SHA, `git status --porcelain=v1`은 빈 문자열이다. 지침은 불변 AGENTS, docs/README, resume, agent-workflow, reviews/README에 따라 적용했다. A 원문을 열거나 A의 결론을 판정 근거로 사용하지 않았다.

증거: `review-B-common-postfix-4-evidence/`. manifest 복사, 실제 로컬 실행 로그, 독립 공격 스크립트/결과, GitHub API/로그 발췌, 기존 원문 hash와 최종 clean 상태를 포함한다.

## 본인 finding closure

| ID | 심각도 | disposition | 본인 재확인 |
|---|---|---|---|
| B-P1-08 | P1 | **FIXED** | `.github/workflows/docs.yml:190`은 정확한 `$GITHUB_WORKSPACE`를 trust에 추가한 뒤 SHA 검사를 유지한다. source3에서 확인한00ddd65 한 줄 수정이2ec에 포함됐다. 이번에는 정확2ec packages130672023061에서 preflight·설치·pack·실제 browser까지 성공함을 직접 확인했다. 과거7e 실패는 보존한다. |
| B-P1-09 | P1 | **FIXED** | `tools/_scan.py:229`의 archive 순회와 `:345`~`:360`의 정확 member/rule/raw SHA256 검증으로 binary UTF-8 실패를 해소했다. 전체 트리 두 scanner를 독립 실행해1352파일, 발견0, 예외32/4를 확인했다. 정확2ec의 secret/docs/tools 양 OS도 성공했다. 아래 독립 hash 변조·member 유실·다른 rule 공격이 거부/탐지된다. |
| B-P1-10 | P1 | **FIXED** | `tools/check_frontend_dependencies.mjs:48`은 link 해석 결과에 workspace 표시를 전파하고 `:99`는 도달한 linked workspace의 devDependencies도 BFS에 넣는다. 자신의 이전 최소 lock fixture를 c9 SRI로 갱신한 뒤 원래 stock dev 엔진 입력이 exit1임을 확인했다. 두 단계 linked dev chain/같은 버전 다른 bytes도 거부한다. canonical bytes, 연결되지 않은 workspace, registry helper의 미설치 devDeps, 별도 dev React18은 기대대로 허용된다. |

B2-P3-01 tokens 고지 FIXED와 최초 B-P0-01/B-P1-01~07/B-P2-01~03의 기존11 FIXED를 유지한다. 새 checker와 policy68에서 이전 React runtime 중복/버전/모바일/금지 import 경계가 재발하지 않았다. source3의 scanner 실패는 당시의 새 결함이었으며 이번 실제 scanner 성공으로09를 닫는다.

## archive 예외와 정책 우회 공격

예외 수32/4를 예외 항목 수와 혼동하지 않았다. 실제 TOML은 secrets24개 member/rule 항목, prod4개 항목이며 secrets의 여러 일치 행이32건으로 집계된다. 28개 항목 모두 raw member digest를 직접 재계산했다.

- secrets의 허용 대상 실제 일치 구문은 Token/visitor/parser 변수·타입 참조다. 일치하는 원문 행을 공개 base `1d680fa14e9a089c92dc0929f869d6757ae91c30`의 해당 행과 직접 대조했다. 전체 파일이 수정된 경우에는 파일 전체가 upstream과 동일하다고 주장하지 않고 해당 일치 행의 동일성만 확인했다.
- native/WASM의 INTERNAL-HOST 일치는 공개 compiler 오류 문장 경계에서 생긴 `consumed.internal error` 및 `selector order.local(` 상수 인접 배치다. 실제 고정 binary member를 확인했고 운영 hostname으로 판정할 근거가 없다. 원문 값은 보고서에 옮기지 않았다.
- 예외는 exact outer/member, 단일 rule, 원문 SHA256에 묶인다. glob/전체 archive·전체 규칙 예외를 추가하지 않았다. gzip/tar header metadata와 다른 rule은 계속 검사한다. 알 수 없는 binary·서명 불일치·잘못된 UTF-8, link/sparse/중복/경로 탈출, 압축 크기/깊이/항목 수 한계도 회귀에서 실패 처리된다.
- B 독립 공격4개: 실제 허용 member는 허용; 새 비밀이 없어도 member byte 변경은 reject; member 유실은 reject; 허용 member 옆의 다른 rule PRIVATE-KEY는 탐지. `common-independent-attacks.json`과 재현 스크립트에 보존했다.
- B 독립 lock 공격7개: 원 stock/같은 버전 다른 bytes/두 linked helper chain 거부3개; canonical bytes/무관 workspace/registry dev/별도 dev React18 허용4개. 원 source3의 false PASS가 사라졌다. 이 최소 lock 모델은 신규 npm ci로 생성한 전체 설치가 아니며, 앱 export 성공을 뜻하지 않는다.

React 탐색은 기존처럼 현재 앱 runtime graph에 한정되고 workspace dev 표시가 CSS 탐색에만 사용되는 것을 확인했다. public registry의 devDeps까지 일괄 포함하는 과도한 검사를 추가하지 않았다. module AST 확장과 MJS/CJS/MTS/CTS, 정적 재export/외부 TS import/타입 import/literal require·import 회귀도68개에 포함돼 있다. 정적 리터럴 검사이며 모든 동적 JavaScript 로딩을 증명하는 도구라고 확대하지 않는다.

## artifact·라이선스·문서 정합

6개 실제 tgz SHA512가 manifest4와 모두 일치한다. c8와 c9를 member 단위로 직접 비교했다. UI94개 중 `package/check-dependencies.mjs` 하나만 변경, tokens25개 중 동일 checker 하나만 변경했다. 나머지 **117개 runtime/CSS/metadata bytes가 동일**하다. 두 tgz의 새 checker는 불변2ec tools 및 두 package checker 사본과 정확히 같다. 2c→2ec에서 packages, frontend-dependencies.json, checker source에 diff가 없음도 확인했다. c9는 unreleased candidate이므로 과거 후보와 bytes가 다르다는 사실을 숨기거나 발행된 버전 재게시로 표현하지 않는다.

VWorld3개와 NativeCSSfix4는 이전 승인 bytes 그대로이며 hash를 다시 확인했다. VWorld9a와 merged ae1e209967b3be7a3918f44e4df278add9f1376c의 tree 동일성도 독립 확인했다. serde18e와 merged21d1c7d3f184e362e0a90905939962d43824e0dd의 tree 동일성은 별도 Native3 evidence에 있다. 이번에 VWorld/Rust를 새로 빌드했다고 주장하지 않는다.

`tools/sync_frontend_policy.mjs`가 버전 표의 단일 marker 구간을 versions.json에서 생성하고 JSON과 문서를 함께 check한다. 단독 문서 drift/registry 변경/marker 유실의 새3개 테스트가 실제 통과했다. AGENTS의 현재 7repo·9surface 범위와 consumers §0은 현재 승인 범위, 기존 §§1~7은 역사 조사·당시 선행 조건으로 명시해 현재 Pinvi 모바일·Transport 승인을 과거 문구로 차단하지 않는다. 실제 앱별 수용·배포를 승인하는 문구로 확대하지 않았다.

## 실행과 정확2ec CI

| 확인 | 결과 | evidence |
|---|---|---|
| 정책 회귀 | **68 PASS, skip0** | common-policy.log |
| Python 전체, 기존 MDX deps 연결 후 | **382 실행, 381 PASS / 1 SKIP** | common-tools-with-borrowed-deps.log |
| policy JSON·문서 생성 check | exit0 | common-policy-sync.log |
| secrets/prod 전체 | **1352파일, 발견0, 예외32/4**, exit0 | common-secrets.log, common-redaction.log |
| B 독립 공격 | policy7 / scanner4 모두 기대값 | common-independent-attacks.json |
| 6개 SRI·c8/c9·예외 digest | 성공 | common-artifacts-allowance-audit.json |
| Git diff 공백 | exit0 | 명령 직접 실행 |

첫 Python 전체 실행은 NODE_PATH만으로 ESM MDX 모듈을 찾지 못해 **382개 중 failures38/errors3/skipped1**이었다. 이 환경 실패 로그 `common-tools-full.log`를 보존했다. 기존 node_modules 경로를 symlink로 연결한 뒤 동일 불변 source에서 전체 재실행이 성공했다. 신규 설치나 코드 변경으로 덮어 해결한 것이 아니다. 부모의 이전379개 집계를 이번382개로 무비판적으로 복사하지 않았다.

GitHub를 직접 읽기 조회해 `2ec519255ec1af9fca18856d980e968ee15b80a8`의4개 workflow success를 확인했다.

| workflow/run | 상태 |
|---|---|
| docs43063412925 | **SUCCESS**, 하위6개 모두 success |
| common frontend43063413154 | SUCCESS |
| workflows selftest43063413011 | SUCCESS |
| python-package43063413008 | SUCCESS |

하위 job: docs130672022639, check-versions130672022818, secret130672022896, tools Windows130672022977, packages130672023061, tools Ubuntu130672023089. packages/secret/tools Ubuntu/docs의 원문 로그를 직접 읽었다. checkout과 SOURCE_SHA가2ec임을 확인했으며 source3/00ddd CI로 대체하지 않았다.

[packages130672023061](https://github.com/digitie/kor-travel-common/actions/runs/43063412925/job/130672023061)은 Playwright1.65.0/Chromium158.0.8127.18 실행, UI101, tokens9, policy68, webpack/Turbopack와 **실제 packed browser65 PASS(40.7s)**를 통과한다. pack의 전체 UI SRI `buhlDym3/Id355Cse+lwBsFk3G1nz3dY2XviAA+X82TZPXmcujYGxItRZafsY0t4xsWkiQ3jAxtCYjFZ7JsbEQ==`, tokens `+JglXOZhP11afRr/upKHWz7cjsj4IPIKYkoVh8lq9IcJTKU8zIHA8pirC1IOS1++gqOmMCnPkj1oi8EzJsTUyQ==`가 c9와 정확히 일치한다. runtime 동일성 추론만으로 browser PASS를 대신하지 않았다.

원격 docs/tools의 Python은 **Ran382, skipped3**이며 로컬381PASS/1SKIP과 구분한다. remote-exact 증거에 각 job status·실제 checkout/전체 SRI·테스트 수·scanner 수치를 보존했다.

## 명령·보존·판정 한계

Windows PowerShell workdir `C:\`에서 `wsl.exe -e bash -lc`로 실행했다. 주요 명령:

```bash
sha256sum review-manifest-common-4.json
git worktree add --detach /tmp/review-b-common4-20261111-170200 2ec519255ec1af9fca18856d980e968ee15b80a8
git diff 7e3f33e0391990b9312fee513de581e28035aa8b HEAD -- <검토 파일>
python3 -B -X utf8 tools/scan_secrets.py --all
python3 -B -X utf8 tools/check_prod_redaction.py --all
NODE_PATH=<기존 common node_modules> node --test packages/ui/test/dependency-policy.node.test.mjs packages/ui/test/native-css-policy.node.test.mjs
python3 -B -X utf8 -m unittest discover -s tests
node tools/sync_frontend_policy.mjs --check
python3 -B <evidence>/audit-common.py
python3 -B <evidence>/independent-common-attacks.py
git diff --check 7e3f33e HEAD
git status --porcelain=v1
```

GitHub 호출은 commit_workflow_runs(2ec), workflow_run_jobs(43063412925), workflow_job_logs(위4개 job)이다. rerun·원격 댓글·merge·소스 수정은 실행하지 않았다. 이전 원문5개의 SHA는 final-provenance.json에 보존했으며 source3 원문 SHA는 `0351063787a4367e264cf7dce61b521a2e87043edc66a6ed8b03139137e479cc` 그대로다. 자체 임시 worktree/fixture/추출물만 정리한다.

**최종 PASS는 이 manifest의 공통 원본·후보 artifact·CI gate에 한정한다.** 추가 신규 finding 없음. 최종 소비자 독립 리뷰, 전체 앱 export, 새 이미지/배포, native 앱 기기 실행·릴리스는 NOT_RUN/별도 gate다. NativeCSS3 판단은 별도 B 원문으로 제출한다.
