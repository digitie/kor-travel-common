# Common 후보4 — 원 B 독립 재검토

- 실행 ID `B-COMMON-8A2C-20261113-04`; reviewer B/Epicurus, 구현 비참여.
- 시작 UTC `2026-11-12T18:24:25.540858+00:00` / 원문 고정 UTC `2026-11-12T18:31:47.906142+00:00`.
- 불변 manifest `validation/review-common-build-rules-8a2c-20261113/manifest.json`의 SHA256 `116da46fb3b94f0d3c49ec7fdc40e8e993abd719327131ba69d24190392c9e9a` 직접 일치 확인.
- exact source `8a2c7daaf906097937426e81f1bdd69ce0bdd389`; tree `88ed0d5bf807081732ecc6619d8e553b6abd1047`; base `678a5bcf0150ac0386bfa86106e7e0f4f77e8639`.
- previous `404a586ece08ca0050d844cbe0eee4df5a79f899`; 21개 Git blob ID/bytes/SHA를 검산하고 helper/tests/journal의 3경로 delta를 모두 읽었다. working tree/index/branch 편집·전환 0, 상대 reviewer 원문/판정 열람 0.
- 원 404a report를 **먼저** 고정했다: `validation/review-B-common-build-rules-404a-3.md`, SHA256 `d7fd177d748de6ca1d8616321a21cc13743eddfd307b8d8811e62075ec999e5f`, 증거 index `303433b30d4da566611f9f4c58a5a19350b452afb38edc8f57ca05a4952a69c8`. 그 BLOCK은 변경하지 않는다.

## 판정

**CONDITIONAL — 기존 실제 소비자 cache P1 FIXED, 기존 P2 1건 OPEN, 신규 P2 1건 OPEN.** 신규 P0/P1은 없다. OPEN 두 건의 수정 또는 workflow 규칙에 맞는 owner·상세 task·적용 gate·목표 시점의 명시 DEFERRED 처분이 아직 없으므로, 무조건 SOURCE PASS나 최종 merge 승인으로 소비하지 않는다.

## 자기 기존 지적 closure

| ID | 이번 상태 | 직접 증거 |
|---|---|---|
| B-BUILD-P1-02 실제 `.npm` cache 오인식 | **FIXED** | 이전에 SHA/Git 검산한 Geo·Weather·Transport Dockerfile 4개를 같은 정합한 자기 anchor와 재실행하여 모두 성공. 최소 `.npm` mkdir/chown도 성공 |
| B-BUILD-P2-05 뒤 non-npm 구간 background | **OPEN** | 이전 동일 `npm install --global npm@12.0.1 && printf ready & node --version` 및 연속 printf 변형이 여전히 ok:true |
| B-BUILD-P1-01, P2-01/02/03/04 | **FIXED 유지** | 기존 strict 해제·force 인용 key/section·CLI alias·기본 physical registry 반례를 같은 snapshot ini와 다시 실행. 원 음성은 거부, 인용 true 등 정상형은 수용 |

`.npm` 실제 4개 입력 closure는 범위를 분명히 한다. 현재 실제 소비자의 실패는 해소되었지만 모든 cache 경로를 올바르게 분류한다는 뜻은 아니며, 아래 잔존 문제를 P2로 분리한다. 기존 원문 심각도를 소급 변경하지 않았다.

### B-BUILD-P2-05 OPEN의 구체적 이유

위치 `tools/check_node_toolchain.mjs:170`–`:172`, 제어문자 검사는 `:78`.

```dockerfile
RUN npm install --global npm@12.0.1 && printf ready & node --version
RUN npm ci --engine-strict
```

같은 literal RUN의 `&&` 뒤 npm 문자열 없는 segment를 검사하지 않아 `&`를 놓친다. shell의 AND-list 전체가 background 문맥에 있는데도 첫 segment에서 pin을 기록한다. 직접 npm segment의 `&` 거부, 지원 `&&`, JSON literal 제어문자 인수 수용은 유지됐다. 전체 Docker parser를 요구하는 것이 아니라, npm pin 순서에 영향을 주는 외부 연산자 경계의 검증 문제다. 실제 Docker의 race/잘못된 이미지 버전을 실행해 입증한 결과로 확대하지 않는다.

**disposition: OPEN / P2.** 404a 이후 이 부분은 수정되지 않았으며, 수정 또는 정식 후속 처분이 필요하다.

## 신규 B-BUILD-P2-06 — 점 없는 cache 경로는 여전히 실행 파일로 오인

- 위치 `tools/check_node_toolchain.mjs:168`, `:172`; `(?<![\w.])(?:npm|npx)\b`가 실행 위치와 경로 인수를 구분하지 않는다.
- 정상 예: `RUN mkdir -p /var/cache/npm && chown node:node /var/cache/npm`.
- 직접 결과: canonical FROM/pin/strict ci가 모두 정합한 자기 fixture에서도 `정적으로 검증 가능한 Node npm/npx 명령이 필요합니다` 오류 2개로 거부한다. JSON `RUN ["mkdir","-p","/var/cache/npm"]`도 거부한다.
- 추가 대조 `/tmp/npm-cache`, `/tmp/npx-cache`, `/home/node/.cache/npm`은 shell/JSON 양쪽 모두 잘못 거부한다. `/home/node/.npm`·`/home/node/.npx`는 양쪽 모두 성공한다. 결과는 `cache-variants-results.json`에 기록했다.
- 영향/심각도: 현재 고정 4개 실제 Dockerfile은 dot cache를 써 통과한다. 이 신규 P2는 같은 reusable API의 일반 cache 위치에 대한 잔존 잘못된 거부이며, 8a2c가 새로 만든 회귀 또는 현재 실제 앱 실패라고 주장하지 않는다. 이전 regex 문제의 다른 표기가 남은 것이다.
- 권고: 실행 파일 위치와 인수를 구분한다. **slash까지 무조건 예외 처리**하면 `/usr/local/bin/npm` 실제 호출이 누락될 수 있으므로, 절대 CLI·env/sh wrapper·동적 호출 거부 대조를 유지해야 한다. cache 이름 강제·경로 변경·검사 목록 축소로 회피하지 않는다.
- disposition **OPEN / P2**. 수정 또는 책임자·상세 task·gate·목표 시점이 있는 처분 필요. 임의 DEFERRED/PASS로 처리하지 않는다.

## 직접 검사와 출처

1. root/lock/registry/공식 ini·public policies·4개 workflow는 404a와 Git blob가 동일하다. 허용된 private root ini@7.0.0 1개 외 graph 예외가 늘지 않았다. 이전 독립 root lock deep-equality와 public193/C11 bytes·SRI 보존 증거를 3경로 disjoint delta로 승계한다. 재pack 0이다.
2. 지정 immutable snapshot의 **ini 4파일**을 SHA 검산해 frozen root와 자기 alias fixture의 공통 부모에 사용했다. dependency 없는 실행이라고 하지 않는다.
3. 자기 `node --test frozen/tests/check_node_toolchain.test.mjs` **exit0 / 81PASS / 0FAIL / 0SKIP**, 실제 WSL Node22.22.2. 각 명령의 실제 exit/stdout/stderr를 `own-command-receipt.json`에 따로 기록했다. 원 strict/force/alias/기본 registry probe·background·실제 cache source probe도 각각 exit0로 완료했으며, 이 exit0은 관찰 프로그램 완료이지 각 공격 입력의 승인 여부와 혼동하지 않는다.
4. 제공 81개와 자기 대조로 `.npm/.npx` 정상 및 실제 npm/npx pin/strict, 절대경로 CLI·wrapper·동적 호출의 음성, `&&`·JSON 문자 인수의 양성을 확인했다. 불변 source의 지원 bounded grammar를 넘는 실제 이미지/임의 script body를 검증하지 않았다.
5. canonical81 receipt의 source/lock/module **입력11개**를 exact Git·검증 module에 대조하고, **로그4개**의 SHA와 exit0를 검산했다. 소유자 Node22.23.1/npm12.0.1 runtime·81개 실행은 별도 handoff다. 내가 그 환경에서 새로 재실행한 것으로 주장하지 않는다.
6. receipt reader가 처음 이전 schema를 가정해 KeyError였던 사실은 `receipt-reader-r1.txt`에 남겼다. 올바른 inputHashes/results로 읽기를 복구했으며 source·원 receipt·로그 수정이나 테스트 재시행은 없었다.
7. owner의 before/after **7개 대상(Common 포함)** 기록에서 같은 inputHashes와 after exit0를 검산했다. 이는 전체 앱 7개 runtime 수용이 아니다. 기록에 들어 있는 hash 일치와 부모 실행 보고를 확인한 것이며, 현재 움직이는 모든 소비자 파일을 별도 재검산한 증거로 확대하지 않는다. 자기 직접 재실행은 이전의 **고정 Git Dockerfile 4개 + 최소 anchor**다.
8. 구 common-ref의 script 부재 시 fail-closed, 명시 live registry, 잠긴 dependency 설치를 추가한 consumer-smoke 연결은 unchanged다. 실제 consumer-smoke dispatch/build를 실행하지 않았다. CI 순서/needs/fail-fast 분석·재정렬은 하지 않았다.

## CI·한계·원문 보존

직접 GitHub commit-associated PR runs 관찰 UTC는 `github-ci-observation.json`에 보존했다. **frontend43279055143 / selftest43279055483 / python-package43279055250 SUCCESS**, **docs43279055160 IN_PROGRESS**였다. 다른 head의 성공을 8a2c에 전용하지 않으며 이 시점 상태를 이후 성공으로 덮어쓰지 않는다. CI가 성공하더라도 본 OPEN 반례는 현재 정상 81개 밖에 있다.

**NOT_RUN:** 새 full install/build/browser/Doctor/Python400, Windows 정본 직접 실행, 실제 reusable/consumer-smoke dispatch, image의 실제 버전·cache·race·운영/인증/Map/native 실기기/EAS/store. 기존 정책 차단 Windows fixture 삭제 재시도·외부 process 조작·타인 캐시 삭제 0. 사용자/owner repo·index·branch·소스 편집 0이다.

원문 `validation/review-B-common-build-rules-8a2c-4.md`, 자기 evidence `validation/review-B-common-build-rules-8a2c-4-evidence/`를 별도 고정한다.

**최종: 원 cache P1 FIXED / B-BUILD-P2-05 OPEN / 신규 B-BUILD-P2-06 OPEN / CONDITIONAL.**
