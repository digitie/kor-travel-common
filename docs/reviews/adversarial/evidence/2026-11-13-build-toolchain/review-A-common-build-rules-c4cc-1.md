# Common build rules c4cc 독립 적대리뷰 A — SOURCE BLOCK

- Execution ID: A-COMMON-BUILD-c4cc-20261112T165112Z
- 원본 고정 UTC: 2026-11-12T17:01:01.947677+00:00
- 리뷰어: Original A/Mill. 구현 비참여, 상대 CURRENT 리뷰/판정 열람 0.
- source: `c4cc78781638808490c0ea540fbb38200b577346`
- base: `678a5bcf0150ac0386bfa86106e7e0f4f77e8639`
- observed tree: `3e7334d476d36c55eaf14b37d32a6f5c9856b5ef`
- immutable manifest: `validation/review-common-build-rules-c4cc-20261113/manifest.json`
- manifest SHA256: `97c799ad0a4da4a2c1ca2056625a19450d894c09f94c5f5c1af0f8ec1883d5d3`
- evidence: `validation/review-A-common-build-rules-c4cc-1-evidence/`. 소스는 Git object에서만 읽었으며 own fixture와 원문은 repo 밖에 저장했다. 끝 관찰 tracked dirty=0이지만 작업트리를 리뷰 입력으로 사용하지 않았다.

## 판정과 disposition

P0 0 / P1 0 / **P2 4 OPEN** / P3 0. **SOURCE BLOCK**: 아래 guard false PASS 네 경로는 수정 및 원 리뷰어 재확인 전 보류한다. P0/P1 수준 운영 장애를 주장하지 않는다. P2의 자동 수용·후속 이관 승인은 없으며, 이 검사기를 새 exact-toolchain 준수 gate로 채택하기 전 수정할 것을 권고한다. 현재 정상 Common 입력이 이 반례를 사용한다는 주장은 아니다.

root metadata·workflow 연결과 공개 파일 불변은 확인했지만, 해석 불가 입력의 거부와 실제 npm 선택/strict 강제를 약속한 범위에 빈틈이 있다. 기존 47 테스트 PASS는 이 반례들을 포함하지 않는다. source 판정은 설치/build/원격 CI/소비자 적용/배포 승인과 별개다.

## A-COMMON-BUILD-P2-01 — `.npmrc force=true`가 strict 검사를 무력화해도 통과

- 위치: `tools/check_node_toolchain.mjs:55–64`, 호출 `:200–201`.
- 재현: 정본 `.nvmrc`, private packageManager/engines를 둔 fixture의 `.npmrc`를 `engine-strict=true\nforce=true\n`로 둔다. Dockerfile 없이 `checkToolchain` 호출 시 **`ok:true, errors:[]`**. own `npmrc-force` 사례.
- 원인/영향: engine-strict 행만 선택하고 나머지 설정을 무조건 무시한다. force 설정은 engines 부적합 설치도 허용하므로 strict=true의 선언만 있고 보호는 해제된 private anchor를 정상 판정한다. CLI `--force`만 금지해도 이 입력 경로는 남는다. npm의 force/engine-strict 동작은 [공식 npm 12 설정](https://docs.npmjs.com/cli/v12/using-npm/config/#force)에 명시되어 있다.
- 권고: anchor `.npmrc`의 유효 force 설정을 함께 검사해 활성 우회를 거부하고, 같은 입력을 음성 테스트로 고정한다. 이때 registry/peer/lifecycle의 무관한 정상 설정을 일괄 금지하지 않는다.
- disposition: **OPEN / 수정 요청**.

## A-COMMON-BUILD-P2-02 — strict 토큰의 존재만 검사하여 뒤의 해제 옵션 허용

- 위치: `tools/check_node_toolchain.mjs:108–110`, 관련 옵션 검사 `:87–89`.
- 재현: 정본 Node tag+형식상 digest FROM과 `RUN npm install --global npm@12.0.1` 다음에 각각 `RUN npm ci --engine-strict --engine-strict=false`, `RUN npm ci --engine-strict --no-engine-strict`를 둔다. 두 경우 모두 **`ok:true, errors:[]`**. own `strict-false`, `strict-negated`.
- 원인/영향: `words.includes('--engine-strict')`만으로 충분하다고 판단해 반대 옵션을 놓친다. 검사기는 명시 strict ci로 승인하지만 명령은 strict를 해제하도록 구성된다. 정상 `.npmrc`와 정본 npm 선택만으로 Docker 명령의 이 우회를 막지 못한다.
- 권고: 지원하는 literal 문법에서 strict의 유효값/반대 옵션을 검증하거나 모순되는 모든 표기를 거부한다. 등호·분리값·부정·중복 옵션과 JSON exec-form에도 같은 규칙을 적용하는 음성 대조가 필요하다.
- disposition: **OPEN / 수정 요청**.

## A-COMMON-BUILD-P2-03 — Docker heredoc/escape 지시문을 해석하지 않으면서 PASS

- 위치: `tools/check_node_toolchain.mjs:117–138`.
- 재현 A: 정본 FROM 다음에 `RUN <<EOF`, 본문 `npm install --global npm@11.19.1` 및 `npm ci --force`, `EOF`를 둔다. **`ok:true`**. RUN 첫 행에 npm이 없고 본문은 RUN으로 시작하지 않아 모두 검사에서 빠진다.
- 재현 B: 첫 행 `# escape=` 뒤에 backtick을 둔 유효 Docker 지시문, 정상 Node stage, 이후 `FROM ` + backtick + 개행 + `node:24.15.0-alpine@sha256:` + 64자리 digest를 둔다. **`ok:true`, checkedNodeImages=1**. 지시문을 주석으로 삭제하고 backslash만 연결하므로 마지막 잘못된 Node stage를 보지 못한다. 한 행으로 쓴 같은 잘못된 FROM은 정상 거부되는 대조도 확인했다.
- 영향: 문서의 ‘해석 불가 입력/해석할 수 없는 FROM은 실패’와 달리 미지원 문법을 정상으로 통과시킨다. 이는 컨테이너 내부 임의 스크립트를 감사하라는 요구가 아니라 제출된 Dockerfile instruction 경계를 정확히 인식하거나 거부하라는 요구다. [Docker 공식 reference](https://docs.docker.com/reference/dockerfile/)는 escape 지시문의 개행 의미와 RUN heredoc 본문 실행을 규정한다.
- 권고: 최소 범위라면 지원하지 않는 escape 지시문과 heredoc을 명시적으로 거부한다. 지원을 늘리려면 instruction 단위로 먼저 정규화하고 본문/주석 경계를 보존한다. 이 두 반례를 기존 comment-continuation 대조와 함께 고정한다.
- disposition: **OPEN / 수정 요청**. Docker build를 실행한 증거는 아니다.

## A-COMMON-BUILD-P2-04 — stage pin 이후 다른 npm을 선택하는 옵션이 우회

- 위치: `tools/check_node_toolchain.mjs:93–107`.
- 공통 전제: 정본 Node FROM, `RUN npm install --global npm@12.0.1`로 stage.pinned=true.
- 재현 A: `RUN npm install --location=global npm@11.19.1` 후 `RUN npm ci --engine-strict`가 **`ok:true`**. `-g`/`--global`만 재설치로 인식하므로 다른 global 선택을 놓치고 pinned=true를 유지한다.
- 재현 B: `RUN npx --yes --package=npm@11.19.1 npm ci --engine-strict`도 **`ok:true`**. 첫 비-yes 토큰은 `--package=...`여서 npm@ 버전 검사를 벗어나며, 이미 pinned된 stage라 최종 거부도 없다.
- 영향: 처음 pin한 사실이 이후 npm 재선택까지 보증하지 않는다. 잘못된 도구로 설치/build하는 명령이 exact CLI 선택을 통과한다. [npm location](https://docs.npmjs.com/cli/v12/using-npm/config/#location), [npm exec/npx](https://docs.npmjs.com/cli/v12/commands/npm-exec/)의 공식 옵션 의미와 충돌한다.
- 권고: 지원 literal의 허용 문법을 명확히 제한하여 다른 selector 형식을 거부하거나 모든 재선택을 추적한다. 특히 pinned 이후에도 명시 selector를 검사해야 한다. 모든 npx를 단순히 기존 stage pin으로 승인하지 않는다.
- disposition: **OPEN / 수정 요청**.

## 직접 실행과 원시 증거

- `/usr/local/bin/node --test <own evidence>/fixture/tests/check_node_toolchain.test.mjs`: **47 PASS / 0 FAIL / 0 SKIP / 0 cancelled**, exit 0. exact Git tool/tests/versions를 복사했고 TMPDIR/TMP/TEMP를 own evidence 내부로 한정했다. 기존 fixture cleanup 후 own tmp 잔여 0.
- 실제 로컬 Node는 **v22.22.2**다. 구조·입력 검사의 직접 실행이며 Node22.23.1/npm12.0.1의 actual runtime gate 실행으로 바꾸어 적지 않는다.
- `/usr/local/bin/node --test <own evidence>/own-attacks.test.mjs`: **2 PASS / 8 FAIL / 0 SKIP**, exit 1. 정상 입력과 직접 잘못된 Node FROM의 두 대조는 기대대로 동작했다. 나머지 8개는 기대 거부와 달리 checker가 ok:true를 반환한 raw 그대로다.
- 이 중 `.npmrc legacy-peer-deps=true` 단독은 **탐색 관찰만 유지**한다. 현재 문서의 기존 peer flag 보존 범위와 경계가 있어 독립 결함으로 세지 않았다. 초기 상태보고의 ‘잘못된 입력 8개’ 중 **7개를 4 finding의 확정 근거**로 채택했다. 테스트 실패를 숨기거나 재실행해 녹색으로 만들지 않았다.
- original47 log SHA256: `fe3757c12eecf7dd22ceaae7def408e9725b934ffa1847c47f561ea8a4825cbc`.
- attacks log SHA256: `0997bae8cca24d58e53a85c651832c9847f5bb60ee142f614543781860f27200`.
- `own-attacks.test.mjs`, `own-inputs/`, `attack-dispositions.json`에 정확한 payload와 반환값이 있다. digest의 반복 a는 정적 형식 fixture이며 실제 이미지 digest/tag 관계를 증명하지 않는다. npm/Docker install/build는 수행하지 않았다.

## 확인한 비회귀·정책/caller 경계

1. `git show`, `git rev-parse`, `git diff --name-only base head`: 21개 경로 집합, 각 blob SHA1/SHA256/bytes, source tree와 immutable manifest가 전부 일치한다. `object-validation.json` 참고.
2. base/head의 공개 package/vendor/frontend policy 파일 **193/193** raw bytes와 이전 hash를 직접 대조했다. root lock은 root engines 변경을 원복하면 JSON 전체가 동일하므로 dependency graph/version/SRI 변경은 없다. 다른 축과 Node/npm floor(22.12/10.9)는 유지된다. C11 pack의 새 설치나 재pack 증거로 확장하지 않는다.
3. 예외 8개 제거를 diff로 확인했다. Geo/Manager/Weather/Concierge의 기록된 exact HEAD package Git blob·SHA256·정본 dependency 필드를 직접 확인했다. Map npm은 12.0.1 정본화이며 나머지 Map 3개/airport 1개 예외는 기존 값 그대로다. Python 축도 변경 없다. 현재 움직이는 앱 HEAD나 작업트리로 대체하지 않았다.
4. standalone private anchor/workspace 상속/잘못된 배열/상위·절대·Windows형 경로/외부 symlink·ancestor symlink/live policy mismatch/runtime mismatch의 기존 음성 테스트를 직접 실행했다. Windows 상대경로의 `/` 정규화는 `:184`, `:196`, `:200`에서 정적으로 확인했다. **Windows OS 실제 실행은 NOT_RUN**.
5. reusable guard는 optional 배열 기본값 `[]`를 유지하고 기존 frontend package를 반드시 manifest로 넘긴다. JSON 입력은 env→spawn argv→parseArgs로 전달되며 shell command로 재해석하지 않는다. consumer root와 live registry 경로는 common cwd로 바꾸기 전 절대경로로 만든다. npm script의 --runtime이 실제 checker 호출까지 유지된다. CLI의 반복/JSON 인수, 빈 목록, bad JSON exit2 및 경로 거부 exit1의 기존 테스트를 확인했다. 기존 code ref가 새 optional input을 제공한다는 보장은 없으므로 문서대로 **새 입력을 실제 지원하는 merged immutable ref**로 소비자 연결해야 한다.
6. Common frontend/docs/consumer-smoke의 명시 npm12 선택과 strict 명령, runtime gate 연결을 Git diff로 읽었다. `npm --prefix .kor-travel-common run check:toolchain`은 검사 script 위치 기준 registry를 사용한다. 기존 CI 단계의 상대 순서를 보존하며 CI-order/needs/failfast 최적화 감사는 수행하지 않았다.
7. parent canonical-final47 receipt의 source input 7개와 log 4개 SHA를 직접 검증했다. node-version log22.23.1/npm-version12.0.1/runtime PASS/builtin47PASS가 일치한다. 이는 **기존 owner 실행 증거의 정합성 감사**이며 own canonical runtime 실행이 아니다. 400 Python tests=399PASS/1SKIP는 인계된 사실이며 본인이 재실행하지 않았다.

## 범위·NOT_RUN

own Git/object/47 pure/작은 공격 fixture 검증만 수행했다. canonical 실제 npm 런타임, Windows 실행, GitHub Actions exact-head 상태 조회/실행, 전체 400 Python 테스트, install/whole build/browser/Docker/image registry 조회, 소비자 변경·새 코드핀 적용·production/로그인/배포/Map 작업은 **NOT_RUN**이다. digest 형식 검사는 실제 이미지 내용을 보증하지 않으며 임의 shell script의 실행까지 정적 검사가 보증한다고 주장하지 않는다. 현재 소스에서 미지원 literal instruction을 PASS로 분류하는 네 결함과 이 보증 한계는 구분한다.

소스/index/branch/owner cache 변경 0, repo 안 생성 출력 0. own evidence 외 fixture 생성 0. 상대 CURRENT 결과 열람 0. 후속 수정은 새 immutable 입력으로만 원 finding을 재확인하며 본 원문은 그대로 보존한다.
