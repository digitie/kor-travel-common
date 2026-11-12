# Common build rules 후보3 — 원 B 독립 적대적 재검토

- 실행 ID `B-COMMON-404A-20261113-03`; reviewer B/Epicurus, 구현 비참여.
- 시작 UTC `2026-11-12T18:10:17.866673+00:00` / 원문 고정 UTC `2026-11-12T18:21:37.165622+00:00`.
- manifest `validation/review-common-build-rules-404a-20261113/manifest.json`; 직접 관찰 SHA256 `8f490c18ac2db2bbe7249d3b5b1a58f196875ea90300a77e8ad851b23cc56732` 일치.
- source `404a586ece08ca0050d844cbe0eee4df5a79f899`; tree `1d7fb1c650d0c5d7104aa08277696b56008a1832`.
- base `678a5bcf0150ac0386bfa86106e7e0f4f77e8639`; 이전 BLOCK `e1d0f01ef05b913e5f311a4d3ae2922a25a676c3`.
- 격리: 21경로의 Git blob ID/SHA256/bytes를 직접 검산하고 e1d0 이후 정확 12경로 delta를 읽었다. Git object와 자기 validation 사본만 검토했다. owner checkout/index/branch 편집·전환 0, 상대 현재/이전 원문 열람 0.
- 자기 이전 원문 SHA256 `93035c446b6cc75dca38e4170328e51cc9c342ddfc3400180de9a6aa84f3b00d` 보존·일치 확인. 과거 BLOCK/CI/62개 이력을 덮어쓰지 않는다.

## 판정과 기존 finding closure

**BLOCK — 기존 B finding 5건 모두 FIXED, 신규 P1 1건/P2 1건 OPEN.** 신규 P1은 부모의 실제 소비자 정적 검사 전달 후 원 B가 exact Git 파일과 최소 입력에서 독립 재현했다. 신규 P2는 자체 추가 공격이다. CI·정본 정상 76개 통과가 신규 반례를 소거하지 않는다.

| 원 finding | disposition | 직접 확인 |
|---|---|---|
| B-BUILD-P1-01 strict 해제 옵션 | **FIXED 유지** | 원 두 flag 반례와 분리 false·중복 해제는 모두 거부. 정상 strict/등호 true/분리 true는 수용 |
| B-BUILD-P2-01 force 설정 | **FIXED** | 직접·bare·따옴표 값·인용 key force=true 및 root true를 section false로 숨기는 원 반례가 모두 거부됨. root 마지막 force=false는 정상 수용 |
| B-BUILD-P2-02 무검사 symlink CLI | **FIXED 유지** | 직접/일반 alias/preserve-main 모두 같은 잘못된 anchor를 exit1로 거부하고 import-only는 자동 CLI 없이 함수만 노출 |
| B-BUILD-P2-03 유효 strict=false 승인 | **FIXED** | 단/이중 인용 strict false key, section-only 및 root false를 section true로 가리는 입력은 거부. 인용 true key의 정상 입력은 수용 |
| B-BUILD-P2-04 alias 기본 registry 출처 | **FIXED** | 원 default-policy probe에서 Node24/npm11 anchor는 direct/alias/preserve 모두 exit1, Node22/npm12 anchor는 모두 exit0. fake registry 누락·명시 override 대조도 제공 76개에서 통과 |

자체 원 반례는 이전 evidence의 세 probe 소스를 새 exact checker 및 검증된 **실제 ini@7.0.0 module 사본과 함께** 다시 실행했다. 실행 시 bare import가 해결되도록 frozen root와 자기 alias fixture 공통 부모에 같은 검증 module을 뒀다. 의존성 없는 builtin 실행이라고 주장하지 않는다.

## 신규 B-BUILD-P1-02 — `.npm` 경로를 npm 호출로 오인하여 실제 소비자 Dockerfile 거부

- 위치: `tools/check_node_toolchain.mjs:167`, `:171`의 `\b(?:npm|npx)\b` 검사와 `:84`–`:85`의 실행 파일명 검사.
- 최소 실패 시나리오: 정상 canonical Node FROM·npm12 pin·strict ci 사이에 다음 정상 cache 준비 줄이 있다.

```dockerfile
RUN mkdir -p /home/node/.npm && chown node:node /home/node/.npm
```

- 직접 결과: checker는 이 줄의 mkdir와 chown을 각각 npm 호출 후보로 보내 **오류 2개 / ok:false**를 반환한다. `.npm`은 경로 구성요소인데 정규식 word boundary에 걸린다. 자기 비교 fixture에서 동일 mkdir/chown의 일반 경로를 사용하면 성공해 오인식 원인을 분리했다. 이는 실제 cache 경로 변경을 제안하거나 owner 소스를 바꾼 대조가 아니다.
- 부모 추가 자료 `validation/phase2-build-toolchain-20261113/parent-404a-all-seven-static-toolchain-r2.json` SHA256 **8e888437be7f71b23cd6a338ab8cb78dfaf17bb0882db2b601a6a4b4364c7164**와 checker SHA를 직접 검산했다. 다음 source에서 Dockerfile을 **git show**로 읽어 r2 input SHA와 일치시킨 뒤, 자기 정합한 private anchor와 반복 가능한 명시 manifest로 실행하여 각각 같은 오류 2개를 재현했다.

| 고정 source | 실제 파일·문제 줄 |
|---|---|
| Geo `f196fee8c2ece62b6ea60b34caeaf1db3650d814` | `kor-travel-geo-ui/Dockerfile:39`–`:40` |
| Weather `046e90d878a0331cc495d7ff08110499d29f24aa` | `deploy/Dockerfile.web:46`–`:47` |
| Transport `bdb2fabfa5067248afd809620c168310ae90cac5` | `frontend/Dockerfile:50`–`:51` |
| 위 Transport 같은 source | `packages/kor-travel-transport-admin/frontend/Dockerfile:37`–`:38` |

- 영향/심각도: 새 reusable guard에 실제 선택한 Node Dockerfile을 전달하면 정상 cache 디렉터리 설정만으로 Geo·Weather·Transport 검사가 중단된다. 필수 소비자 CI 통합을 막는 **P1**이다. 실제 앱·이미지·운영이 실패했다는 주장이 아니라 새 checker API의 재현 가능한 잘못된 거부다. 부모 r1의 잘못된 기본 manifest 선택을 원인으로 사용하지 않았으며, dirty 상태였던 다른 앱들의 PASS를 불변 Git 전체 수용으로 확대하지 않았다.
- 권고: 실제 npm/npx 실행 위치와 경로·문자 인수를 구분해 판정한다. 동시에 npm을 호출하는 미지원 wrapper/selector가 무조건 무시되는 구멍을 만들지 않는다. 실제 4개 파일/최소 mkdir·chown 양성 대조와 진짜 npm 오선택 음성 대조를 함께 보존한다. **cache 경로 이름 변경·Dockerfile 목록 축소·guard 제외로 우회하지 않는다.**
- disposition **OPEN / P1_BLOCKING**, 수정 후 원 B 재검토 필요.

## 신규 B-BUILD-P2-05 — `&&` 뒤 비-npm 구간의 `&`가 shell 경계 검사를 회피

- 위치: `tools/check_node_toolchain.mjs:169`–`:171` 및 `:78`.
- 최소 반례:

```dockerfile
FROM node:22.23.1-alpine@sha256:<합성 64자리 digest>
RUN npm install --global npm@12.0.1 && printf ready & node --version
RUN npm ci --engine-strict
```

- 직접 결과: exact checker는 **ok:true / errors:[]**다. `&& printf ready && printf next & node --version` 변형도 통과한다. 직접 npm segment 안의 `&`는 정상 거부되며, 순차 `&&` 양성과 JSON exec-form의 literal `&`/`>`/`|` 인수 양성은 유지된다.
- 원인: 먼저 `&&`로 나눈 뒤 npm 문자열이 있는 segment에만 제어문자 검사를 수행한다. 비-npm segment 안의 `&`가 누락되지만 shell에서는 앞의 `npm install ... && printf ready` **AND-list 전체**가 background 문맥에 놓인다. 따라서 명시적으로 지원하지 않는 비순차 제어를 통과시키면서 첫 segment에서 `stage.pinned=true`로 기록한다.
- 영향/한계: 새 규범의 single `&` fail-closed 약속과 pin 순서 모델을 위반한다. 이 관찰은 **정적 parser 재현**이며, Docker/실제 npm install의 race나 특정 실제 이미지의 잘못된 npm 버전을 실행해 증명한 결과가 아니다. 임의 script body 지원을 요구하는 지적도 아니다. 같은 literal RUN의 npm pin 의미에 영향을 주는 외부 연산자 경계다.
- 권고: pin 순서에 영향을 주는 shell 제어 유효성은 npm segment 선택과 `--` 전달 처리보다 앞에서 검증한다. 지원 `&&`, 올바른 비-npm 일반 명령, JSON literal 인수를 보존하면서 `&`가 뒤 segment에 있는 음성 대조를 추가한다. 전체 Docker parser 구현을 요구하지 않는다.
- disposition **OPEN / P2**. 수정 또는 책임자·근거가 있는 명시 후속 task 처분이 필요하며, 임의 면제하지 않는다. 위 P1과 root command 분류를 함께 고칠 때 이 false success가 새로 생기거나 남지 않는지 확인해야 한다.

## 의존성·lock·license·public artifact 경계

- manifest가 지정한 `immutable-3cdaeb79f759/node_modules/ini` 배포 파일 **4개**(package.json·lib/ini.js·README·LICENSE)의 SHA256을 직접 검산해 자기 사본에 사용했다. ini package는 **7.0.0 / ISC / runtime dependency 없음**이며, parser 파일 SHA256은 `007123836ffec243f41c8b35584fb3db0498aa12a440a9e0efc675d0000f4c32`다. 모듈의 devDependencies까지 설치·사용하지 않았다.
- 공식 registry metadata 원문 SHA256 `15cacf3f1bc210d92adc057c8477569fe3c01e5696cf823c7442c6236f5c5673`을 검산했다. metadata·lock의 정확 version·tarball URL·SRI·ISC가 일치한다. module bytes는 manifest의 승인된 배포 사본으로 검증했으며, tarball을 새로 다운로드·설치·재pack해 검증했다는 주장은 하지 않는다.
- root package에서 `devDependencies.ini` 한 항목, lock에서 root devDependency 한 항목과 `node_modules/ini` 한 node만 제거하면 **e1d0와 전체 JSON deep-equal**이다. ini는 `dev:true`이며 root private임을 확인했다. Common private tool graph는 **실제로 1개 늘었고**, 예전 root graph 전체 불변 주장을 그대로 재사용하지 않는다.
- 이 허용 예외를 ADR/규범/개발·task·tools 문서가 명시한다. 공개 package·vendor·frontend policy **193개 Git entry는 e1d0와 동일**하다. 기존 C11 7개 whole bytes/SRI 검증과 unchanged canonical을 승계하며 public·소비자 package graph에 ini가 추가된 것으로 해석하지 않는다. 다른 owner의 현재 소비자 working tree 전체 graph를 검사했다는 주장은 없다.

## 실행·provenance와 caller 통합

- 자기 exact source + 검증된 ini module로 생성한 builtin log: **76PASS / 0FAIL / 0SKIP**, 실제 WSL Node22.22.2/npm11.19.1. 이는 구조 테스트이며 정본 runtime PASS로 표시하지 않는다.
- 첫 결합 명령의 마지막 Python 결과 요약에 괄호 오타가 있어 전체 도구 호출은 exit1이었다. 앞서 생성된 76개 log/세 probe JSON을 그대로 보존하고 읽기만으로 요약을 복구했다. **이 harness 오류를 제품 실패 또는 숨긴 재시도로 바꾸지 않았고, 이 결합 명령 전체 exit0을 주장하지 않는다.** `own-summary-harness-r1.*`에 구분 기록했다.
- canonical receipt의 source/lock/module **입력 11개**와 raw **로그 4개**를 직접 SHA 검산했다. 소유자 실제 Node22.23.1/npm12.0.1의 **76PASS/0SKIP 및 runtime PASS**는 별도 handoff다. receipt의 npm12 selected config 대조도 보존되며, 이를 내가 정본 npm12를 새로 실행한 것으로 주장하지 않는다.
- 3cda→404의 Git diff가 **consumer-smoke 한 경로 한 줄**임을 확인했다. canonical 76의 source/test/lock/module inputs는 404와 동일하지만 그 이전 실행을 404 consumer-smoke dispatch 실적으로 확대하지 않는다.
- 추가 `npm --prefix .kor-travel-common ci --ignore-scripts --engine-strict`는 이미 npm12를 선택하는 step 안에서 check:toolchain보다 먼저 실행된다. 새 private ini를 잠긴 root 설치로 제공하는 연결은 적절하다. 새 별도 step/needs 재정렬이나 소비자 graph 재작성은 없다. **실제 consumer-smoke dispatch/install/build는 NOT_RUN**이다.
- 구 common-ref는 여전히 script·schema가 있어야 하며, 없는 ref에서 fallback 없이 실패한다. SHA/tag 입력 허용을 과거 ref 실행 호환성 보장으로 바꾸지 않았다. reusable frontend guard는 이미 Common locked ci가 있는 unchanged caller를 사용하지만, 선택한 Dockerfile 오인식 때문에 위 실제 소비자 정적 입력은 실패한다.

## CI 관찰·미실행·원문 보존

직접 read-only commit-associated PR run API 관찰(`github-ci-observation.json`의 UTC 기준): **frontend43276647780 / selftest43276648117 / python-package43276647744 SUCCESS**, **docs43276647768 IN_PROGRESS**. 다른 head/e1d0 CI를 404의 결과로 대체하지 않는다. connector의 PR/첫 page 범위를 넘는 전역 완료 수를 주장하지 않는다. 이 소스 BLOCK을 닫으려고 CI 종료를 기다릴 이유는 없다.

**NOT_RUN:** 새 full install/build/browser/Doctor/Python400, Windows 정본 76개 직접 실행, 실제 reusable/consumer-smoke dispatch, Docker/image의 실제 Node/npm·cache·race, registry tarball 재다운로드, 앱 배포/운영/인증/Map/native 실기기/EAS/store. CI 순서/needs/fail-fast 분석·최적화도 수행하지 않았다. Windows 정책 차단 fixture 삭제 재시도·경로 확대·외부 process 조작·타인 캐시 정리 0이다.

원문과 별도 자기 evidence는 `validation/review-B-common-build-rules-404a-3.md` 및 `validation/review-B-common-build-rules-404a-3-evidence/`에 고정한다. 최종 index는 파일 SHA/bytes·symlink 대상·원문 SHA를 기록한다.

**최종: 기존 원 B 5건 FIXED / 신규 B-BUILD-P1-02 OPEN·B-BUILD-P2-05 OPEN / BLOCK. 실제 앱·릴리스·운영 승인은 아니다.**
