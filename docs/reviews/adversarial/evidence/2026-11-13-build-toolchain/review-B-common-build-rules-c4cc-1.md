# 원 B 독립 적대적 리뷰 — Common build rules c4cc 입력1

- 실행 ID: `B-COMMON-C4CC-20261113-01`; reviewer B/Epicurus, 구현 비참여.
- 시작 UTC: `2026-11-12T16:53:53.093214+00:00`; 종료·원문 고정 UTC: `2026-11-12T17:07:10.110859+00:00`.
- 불변 manifest: `validation/review-common-build-rules-c4cc-20261113/manifest.json`.
- manifest SHA256: `97c799ad0a4da4a2c1ca2056625a19450d894c09f94c5f5c1af0f8ec1883d5d3` — 직접 일치 확인.
- base: `678a5bcf0150ac0386bfa86106e7e0f4f77e8639`.
- source: `c4cc78781638808490c0ea540fbb38200b577346`; tree: `3e7334d476d36c55eaf14b37d32a6f5c9856b5ef`.
- 범위: manifest의 21경로 전체. Node checker·47개 테스트·4개 workflow·private root metadata·버전 규약/ADR/도입 문서·예외 정리. 상대 현재 원문·finding 열람 0.
- 격리: Git object `show/diff/rev-parse`만 사용. 21개 blob ID/SHA256/bytes 직접 검산, 필요한 파일만 자기 evidence에 복사했다. owner의 이동 중 working tree/index/branch는 기준선으로 사용하거나 수정하지 않았다. owner checkout의 clean 상태는 주장하지 않는다.
- **verdict: BLOCK**. 신규 **P1 1건, P2 2건**. P0 0건. P1은 소스 수용 차단이며, P2는 각각 OPEN으로 명시하고 소유자의 수정 또는 구체적 후속 task 처분이 필요하다. 실제 CI 성공으로 지적을 닫지 않는다.

## Findings

### B-BUILD-P1-01 — 상충하는 strict 해제 옵션을 유효한 strict Docker 명령으로 수용

- 위치: `tools/check_node_toolchain.mjs:108` (`npmCommand`), 관련 우회 옵션 검사 `:87`; 규범 `docs/standards/versions.md` §3.1.1.
- 실패 시나리오: 합성 Dockerfile의 canonical Node tag/형식상 digest, `RUN npm install --global npm@12.0.1` 뒤에 `RUN npm ci --engine-strict --no-engine-strict` 또는 `RUN npm ci --engine-strict --engine-strict=false`를 둔다.
- 직접 결과: 두 입력 모두 `ok:true`, `errors:[]`, Node image count 1. 같은 옵션을 로컬 npm `config get engine-strict`로 해석하면 각각 **false**다. 정상 `--engine-strict`는 true/검사 성공, 기존 `--force`·`--legacy-peer-deps` 대조는 검사 실패다.
- 원인: `words.includes('--engine-strict')` 존재만 검사하며 뒤의 부정·상충 설정을 거부하지 않는다. npm stage pin이 맞아도 실제 install engine 검사가 해제된 입력이 중앙 guard를 통과한다.
- 영향: 새 `node-dockerfiles` 입력의 명시적 검사 대상에서 거짓 성공. 실제 어느 소비자가 이런 Dockerfile을 사용한다고 주장하지는 않는다. 합성 digest는 parser 대조용 `a` 64개이며 registry나 이미지를 실행·검증하지 않았다.
- 권고: 지원하는 literal npm 명령의 유효 strict 값을 판정하거나 부정/상충 형태를 보수적으로 거부한다. npm/npx·shell/JSON형에서 뒤집기와 중복을 음성 대조에 넣고 정상형을 유지한다.
- disposition: **OPEN / P1_BLOCKING**. 부모의 기존 force 옵션 수정은 이 경우를 막지 못한다.

### B-BUILD-P2-01 — project `.npmrc`의 force 설정으로 engine 보호가 무력화되어도 anchor 통과

- 위치: `tools/check_node_toolchain.mjs:55`–`:64`, 사용 지점 `:200`.
- 실패 시나리오: 정합한 private anchor 옆 `.npmrc`를 `engine-strict=true\nforce=true\n`로 둔다.
- 직접 결과: checker `ok:true`; 로컬 npm 유효 설정은 `engine-strict=true`, `force=true`. checker는 engine-strict 행만 읽고 force 행은 무시한다. 로컬 npm의 실제 `npm-install-checks` 구현도 `force`일 때 Node engine 대조 값을 비운다(`npm-engine-check-primary-source.json` 참조).
- 영향: 선언과 보호 설정이 정합하다고 표시되지만 selected anchor에 보존된 force 설정이 설치 보호를 우회할 수 있다. Docker 명령의 `--force` 금지만으로 project 설정까지 보호되지는 않는다. 외부 사용자·global config의 모든 상태를 검증했다는 주장은 하지 않는다.
- 권고: 적어도 검사하는 anchor `.npmrc`의 유효 force/legacy 우회 설정을 명시 처리하고, 허용할 정책이라면 strict 보장과의 예외를 규범에 분리한다. 구성 파일의 부정·중복 설정 대조도 추가한다.
- disposition: **OPEN / P2_FOLLOWUP_REQUIRED**. 현재 source의 root `.npmrc` 자체는 force를 넣지 않았으므로 기존 job이 우회 중이라고 단정하지 않는다. 개별 P2를 임의 면제하거나 task가 이미 있다고 기록하지 않는다.

### B-BUILD-P2-02 — checker symlink 경로 실행은 검사 없이 exit 0

- 위치: `tools/check_node_toolchain.mjs:222`.
- 실패 시나리오: frozen checker를 가리키는 symlink로 CLI를 호출하고, 입력 anchor에는 `engine-strict=false`를 둔다.
- 직접 결과: 실제 파일 경로 호출은 exit **1**·오류 메시지, symlink 경로 호출은 exit **0**·stdout/stderr 공백이다. `resolve(argv[1])`와 Node가 해석한 실제 module URL 경로가 달라 CLI 본문을 건너뛴다.
- 영향: CLI를 alias 경로로 재사용하면 위반·잘못된 인수까지 무검사 성공으로 소비할 수 있다. 현행 GitHub workflow는 regular checker 경로를 직접 실행하므로 이 입력에서 해당 CI가 우회됐다는 finding은 아니다.
- 권고: CLI entry 식별의 실제 경로 처리를 정합하게 하거나 import용 module과 실행 entry를 분리한다. 잘못된 입력의 직접/alias 실행이 모두 nonzero인 회귀를 둔다.
- disposition: **OPEN / P2_FOLLOWUP_REQUIRED**. WSL symlink 직접 재현이다. Windows 대소문자 경로 공격은 양쪽 모두 정상 exit1이어서 Windows case 우회로 확대하지 않는다.

## 직접 검증·반증과 보존

1. `git show <head>:<path>`, `git diff <base> <head>`, `git rev-parse`로 exact 21개 blob 및 변경 범위를 검증했다. public/package/vendor/frontend 정책 **193개**는 base/head Git bytes와 기존 SHA가 모두 같다. root lock은 `packages[""].engines` 외 deep-equal이며 dependency graph/version/SRI 변화가 없다. Node/npm 외 registry axes와 남은 Map next/Playwright/Starlette·airport TypeScript 예외 4개도 그대로다.
2. 제거된 예외 8개를 독립 산출했다. 그중 7개는 제공된 4개 앱의 **고정 Git commit package blob** SHA와 정확 dependency 필드로 대조했다. 나머지 Map npm 12.0.1 예외는 새 canonical npm과 일치하여 불필요해진 항목이다. 이를 Map 소스 수정이나 새로운 Map 실행 검증으로 확대하지 않는다.
3. `artifacts/integration-11-review` 실제 tarball **7개**의 bytes/SHA256을 직접 읽고, SHA512 SRI를 계산하여 exact Git `frontend-artifacts.json`과 모두 일치시켰다. 공개 package manifest·vendor·C11 payload 변경 또는 재pack은 없다. 이 새 root toolchain 후보를 새로운 C11 producer나 공개 패키지 릴리스로 간주하지 않는다.
4. WSL `node --test frozen/tests/check_node_toolchain.test.mjs`: **47PASS/0FAIL/0SKIP**, Node **22.22.2**, npm **11.19.1**. Windows에 exact SHA의 checker/tests만 복사하여 같은 builtin 실행: **47PASS/0FAIL/0SKIP**, Node **25.9.0**. 이는 구조·경로 테스트이지 내 정본 runtime 실행 PASS가 아니다. Windows의 workspace 상속·중첩 anchor의 내부 relative path와 symlink 경계 테스트도 이 47개에 포함된다.
5. 부모 `canonical-final47-receipt.json`의 입력 7개 SHA를 exact Git와 대조하고 네 raw log SHA를 검산했다. 그 별도 실행의 actual Node22.23.1/npm12.0.1, runtime PASS, builtin **47PASS/0FAIL/0SKIP**는 handoff 증거로 수용한다. 초기 34/36/43/44/45개 실행이나 주입된 version control을 최종 47개/실제 runtime으로 바꾸어 기록하지 않았다. candidate evidence index의 참조 **19개**도 bytes/hash 검산했다.
6. 자체 공격 `node attacks.mjs`와 `npm config get ...`는 위 세 반례를 생성했다. 실제 npm 옵션의 유효 값 확인은 설치 없는 로컬 npm11.19.1 config 조회이며, npm12에서 직접 같은 CLI를 재실행한 결과로 부풀리지 않는다. parser 자체의 canonical 값은 exact frozen registry이다.
7. 경로·목록 거부, workspace 상속, fresh stage 재선택, per-call npx 이후 bare npm 거부, 동적 shell/비정합 이미지 거부, force·legacy 옵션 거부는 47개에서 유지됐다. Windows case spelling 변경은 잘못된 anchor를 정상 거부했다. 최초 Windows UNC 직접 실행은 파일을 열지 못한 launcher **NOT_RUN**이며, 그 로그를 보존한 뒤 Windows 자기 사본에서 실제 47개를 실행했다.
8. 4개 workflow의 기존 named step/action 순서를 base/head에서 비교해 동일함을 확인했다. optional JSON 입력은 실제 frontend package와 함께 args 배열로 전달되고 parse/경로 실패는 nonzero로 전파된다. live registry가 잘못되거나 canonical과 다르면 실패하며, 이를 과거 floor 호환성 실패와 혼동하지 않는다. CI 순서/needs/fail-fast 최적화는 수행하지 않았다.

## 구 common-ref와 재사용 workflow 경계

- `consumer-smoke.yml:126`은 **선택한 common-ref의** `check:toolchain` script를 반드시 실행한다. base678의 package만 격리한 `npm --prefix <oldref> run check:toolchain`은 **exit1 / Missing script**였다. 구 SHA/tag를 받아들이는 입력 형식이 구 ref와 실행 호환됨을 보장하지 않는다. 새 script가 없는 ref에서 실패하는 **fail-closed 호환성 중단**이며 fallback/`--if-present` 성공은 없다.
- 같은 제한은 새 reusable guard code에 old common-ref를 섞을 때도 적용된다. 지원 script·manifest schema·toolchain이 있는 리뷰·머지된 불변 code ref로 소비자 pin을 함께 이관해야 한다. 해당 smoke의 과거 common-ref 재실행 지원을 계속 광고하려면 지원 범위를 명시해야 한다. 과거 ref에 새 script를 섞어 출처를 흐리는 수정은 권고하지 않는다.
- 새 guard는 지정된 frontend package와 선택한 추가 manifest/Dockerfile만 검사한다. 전체 Dockerfile 발견, 임의 script 내부, 실제 build context, digest가 가리키는 이미지의 실제 Node/npm은 보증하지 않는다. 실제 소비자 호출 및 앱별 install/build 승인은 별도다. selftest의 다른 reusable fixture 성공을 새 frontend guard의 실제 소비자 호출 성공으로 치환하지 않는다.

## 직접 GitHub 관찰 — CI 성공과 finding은 별개

- commit `c4cc`로 connector의 commit-associated PR runs API를 직접 조회했다. **frontend 43262390894 / docs 43262391046 / python-package 43262390921 / workflows-selftest 43262391314: 모두 completed SUCCESS**. 이 API wrapper의 PR/첫 page 범위를 넘는 전역 workflow 수는 주장하지 않는다.
- docs jobs 6개(Windows·Ubuntu tools 포함), frontend job, selftest jobs를 직접 조회했다. Windows tools **131336841554** raw log는 checkout/source `c4cc`를 명시하고 canonical runtime PASS 및 builtin **47PASS/0SKIP**를 보여 준다. 같은 log의 Python은 **400 run / 398PASS / 2SKIP**다. 부모 로컬 **399PASS/1SKIP** 기록과 합쳐 새로운 무스킵/전부 PASS로 만들지 않는다.
- frontend **131336839840** raw log도 canonical runtime PASS, builtin47·tokens9·policy175 PASS를 보여 준다. 실제 checkout은 synthetic **99155e3234a38e7c7240d27aaaab3bc481dad51d**(c4cc를678로 병합)이다. 그 whole-tree 동등성은 로컬 object가 없어 이 리뷰에서 추가 입증하지 않았다. docs Windows exact source 실행 증거와 구분했다.
- CI metadata와 선택 raw line은 자기 evidence에 고정했다. 전체 remote log를 별도 파일로 보존했다는 주장은 하지 않는다. 정상 입력 CI 성공은 발견한 음성 입력의 false-positive를 소거하지 않는다.

## 명령·증거·제한

- 증거: `validation/review-B-common-build-rules-c4cc-1-evidence/`; 최종 `evidence-index.json`은 각 자기 파일의 SHA256/bytes 및 symlink 대상을 기록한다.
- 핵심 실행: `node --test frozen/tests/check_node_toolchain.test.mjs`; Windows exact 사본의 `node --test`; `node attacks.mjs`; `npm config get engine-strict [옵션]`; `npm config get force`; 구 ref script probe; builtin Python을 통한 Git blob·deep JSON·SHA256/SHA512 검산. GitHub는 read-only commit runs/jobs/logs API만 사용했다.
- **NOT_RUN**: 내가 정본 Node22.23.1/npm12.0.1에서 재실행한 runtime/negative CLI, 전체 Python400 재실행, 전체 install/build/browser/Doctor, reusable 새 소비자 실제 dispatch, image pull/build/digest 실체 검증, 실제 앱·배포·native/실기기/EAS/store. 새 install·repack·운영/Map 작업 0.
- owner repo와 기존 raw/manifest/cache 수정·삭제 0. Windows 자기 fixture 정리 명령은 자동 승인 검토에서 실행 전 `blocked by policy`로 거부되어 **보존**했다. 다른 cache/owner 파일을 대신 삭제하지 않았고 freed bytes 0이다. 로그와 exact 입력은 WSL 자기 evidence에도 보존했다.

**최종: BLOCK — B-BUILD-P1-01 OPEN, B-BUILD-P2-01/02 OPEN. 후속 exact manifest에서 원 B가 자기 반례를 다시 확인하기 전에는 FIXED로 닫지 않는다.**
