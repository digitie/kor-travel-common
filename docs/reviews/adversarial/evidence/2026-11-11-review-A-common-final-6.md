# 독립 적대리뷰 A — COMMON6 / 후보 C10

- runid: `Mill-A-common-final6`
- reviewer: 원 reviewer A(Mill), frontend/accessibility. 구현 비참여, 읽기 전용 source 검토. 상대 raw/report/verdict는 열람하지 않았다. `docs/reviews`의 현재 리뷰 자료는 source 감사에서 제외했다.
- 시작 UTC: `2026-11-11T18:11:26.941128+00:00`; 종료 관찰 UTC: `2026-11-11T18:20:42.038693+00:00`.
- immutable manifest: `review-manifest-common-6.json`, 실제 SHA256 `9c4653196c891a4b10b47db5d28c41303ec8617d9a69d064dcabfaaa742d42d4` 일치.
- 대상 common: `2d70461a7873d73ec2b278709cef1fba832134cc`; producer: `55a921b55d248106cbe320e7f5305f3d3cdb60fe`.
- 격리 detached worktree: `/tmp/review-A-common6`. 시작·종료 모두 exact HEAD 및 tracked clean. 공유 checkout도 해당 관찰 시점 exact2d/clean. 이후 부모의 변경을 이 판정에 포함하지 않는다.
- 원문 증거 디렉터리: `review-A-common-final-6-evidence/`. 기존 모든 A raw와 manifest·C9·C10·Scope fix1 산출물은 보존했다. source 수정·구현 commit·새 설치·재포장·타인 cache 삭제 없음.

**Verdict: CONDITIONAL — 새 일반 정책의 기능 검증은 PASS, exact2d 전체 merge gate는 미충족.** 신규 **A-P2-11 OPEN**(required Doctor CI 실패). 별도 Scope1의 **A-SCOPE-P2-01 OPEN**은 fix2 immutable 입력에서 원 reviewer 재확인 필요. 이 원문은 C10을 무조건 병합 승인하지 않는다. 신규 common finding 집계 P0=0 / P1=0 / P2=1 / P3=0. 외부 Scope 잔여 P2는 common 신규 집계와 중복 합산하지 않았다.

## 1. 검토 경계와 실제 변경

이번 검토는 optional `patchedRadixPackages`의 Python schema, 독립 JS generator, 배포 checker, 도달한 managed artifact 그래프, `prepare-lock.mjs` 세 설치 경로, 실제 7개 metadata/lock/bytes를 대상으로 한다. `policy-source-delta.patch`에 source2ec→2d의 관련 diff를 보존했다. source447→2d 변경 목록도 확인했다. 원 UI 전부·각 소비자의 최종 설치/배포를 다시 승인하는 검토가 아니다.

직접 tar member bytes를 비교한 C9→C10 결과:

| 패키지 | regular files | 동일 | 변경 |
|---|---:|---:|---|
| @kor-travel/ui | 94 | 92 | check-dependencies.mjs, dependency-policy.json |
| @kor-travel/tokens | 25 | 23 | check-dependencies.mjs, dependency-policy.json |

합계 **115개 runtime/CSS/meta 파일 동일**, checker/policy 4개 변경. C10 양쪽 shipped checker는 exact2d `tools/check_frontend_dependencies.mjs`, shipped policy는 exact2d `frontend-dependencies.json`과 byte 일치한다. **외부 FocusScope runtime은 stock→fix1로 바뀌므로 위 동일성으로 modal acceptance를 대체하지 않았다.** 새 exact2d packages CI의 실제 packed browser 결과를 아래에서 별도로 확인했다.

producer55a→head2d의 이 검토 관련 코드/설정 경로는 같고, `packages/ui/smoke/next-app/package-lock.json`만 tokens/UI 최종 C10 SRI 2개로 바뀌었다. 이를 전체 source 무차이로 잘못 단순화하지 않는다. `real-seven-audit.json`에 실제 diff가 있다.

## 2. 기능 검토와 독립 공격

- Python Registry는 목록 부재/빈 목록 호환을 유지하고 공식 scoped 단일 package 이름, 중복, npm exact axis, checked=false, recommended=null, package/artifact 연결을 검사한다. 전체 axis의 기존 exact SemVer 검증도 유지된다. 임의 subpath/wildcard/인접 scope/range 버전으로 예외 범위가 넓어지지 않는다.
- generator는 쓰기 전에 patched 목록과 exact axis 연결을 검사하며 알 수 없는 policy 필드를 거부한다. 기존 profile 필수/runtime/forbidden 연결과 생성 문서 단일 marker 계약도 유지한다. exact source에서 `node tools/sync_frontend_policy.mjs --check` exit0.
- checker의 새 직접 선언 예외는 승인 목록+artifact+정확 버전이 있는 엔진에만 적용된다. 앱 source의 Radix 금지 AST 분기는 계속 별개로 실행한다. 관리 산출물을 root runtime·dev, 도달한 linked workspace dev, optional/peer 그래프에서 확인하며 registry 패키지의 자체 dev 및 무관 workspace는 섞지 않는다. 요청 이름과 alias의 실제 identity 양쪽을 검사한다. 직접 vendor pin, lock 버전/무결성, 파일 SHA512, 중앙 정본 및 lock root 밖 경로·symlink 금지를 유지한다.
- 실제 C10 필수 archives와 별도의 합성 미래 엔진 `@radix-ui/react-presence@1.0.0+future.review.1`을 사용했다. 실제 fork나 원장을 변경하지 않고 별도 alias axis를 추가하자 Python schema와 generator가 성공했다. 단일 FocusScope 이름에 하드코딩된 정책이 아니었다.
- 같은 미래 엔진을 linked workspace dev→optional bridge→alias에 넣고 동일 version/다른 integrity를 주자 exit1; 올바른 bytes는 exit0. 직접 pin을 제거하면 깊은 alias 설치만으로 대체하지 못하고 exit1. 승인 엔진의 re-export/literal require/import type도 각각 exit1. **합성 policy probe 7개 기대 결과 일치**. 이는 새 설치나 미래 패키지의 실제 runtime 실행을 뜻하지 않는다. `future-policy-probe.py/.json`.
- 실제 root/smoke/example package.json·NPM lock을 자기 fixture로 복사하여 helper를 실행했다. CSS fix4+Scope fix1 4개 대상 복사본의 실제 SHA512 일치, 세 lock/manifest pin 불변, exit0. 마지막 example lock에 중첩 stock Scope를 삽입한 공격은 exit1이고, 앞선 두 대상 vendor sentinel과 모든 pin도 불변. 원장을 잘못된 lock 값으로 조용히 재작성하지 않았다. `real-seven-audit.py/.json`.

## 3. 실제 7개 산출물과 모듈 관찰

7개 tarball의 package.json name/version, 실제 SHA512, manifest 및 source `frontend-artifacts.json`, C10 `common-artifacts.json`을 직접 대조했다. 7/7 일치. 각 full SRI와 크기는 `real-seven-audit.json`에 보존한다.

| 패키지 | 버전 | SHA256 |
|---|---|---|
| @kor-travel/ui | 0.2.0 | 2b2d5acca801ff7eb714da8124d279dcf8ff79710337bf713ae3d0e8c89f0f57 |
| @kor-travel/tokens | 0.1.1 | 7ea9bfebbb5ddea4016c87c027bf7338c291aeec0f6e7bfbf57c57d8574388e7 |
| lightningcss | 1.33.0+nativecss.fix.4 | 12c8326428a56e38231f7b5b376df0c6882e3492da794f3499269628edcaccf0 |
| vworld-map-core | 1.0.1 | 36d3ba16a3ba65f7a460db6027c07e29821f2795b15a526413949210f0ce92b6 |
| vworld-map-web | 1.0.3 | 1ab9af8794979a5a19e5ac635cd04a9e87b9847058eaf4e9df743143b8ad4104 |
| vworld-map-rn | 1.0.1 | 352307615edad047cc100cff6a39c625e778f77434b48475c9930e25ca7b6404 |
| @radix-ui/react-focus-scope | 1.3.1+kortravel.fix.1 | f97c1dd4851fd1dc7b75bfbe9ce7e2d68bbd32e225b9ff52954c683fd4c7081d |

테스트 도구는 기존 common modules의 개별 자식을 readonly 참조했다. private node_modules 디렉터리는 별도로 만들고 cache 디렉터리를 공유하지 않았다. 관찰 runtime은 Node22.22.2/Python3.14.4. **현재 commonRoot를 stock Scope baseline으로 사용하지 않았다.** 실제 설치 Scope는 fix1이며 tarball의 15개 파일 모두 일치, 설치 CSS는 fix4이며 19개 파일 모두 일치했다. native 소스/Rust/Node 양쪽 엔진 검토는 기존 Native3 원문 범위 그대로이고 이 검토에서 재빌드하지 않았다.

## 4. 직접 실행과 직접 원격 관찰

| 검증 | 관찰 결과 | 근거 |
|---|---|---|
| source policy/prepare node tests | **175 PASS / 0 FAIL / 0 SKIP**, 26.210초 | policy-tests.log |
| Python 전체 | **400 실행 / 399 PASS / 1 SKIP / 0 FAIL**, 74.795초 | python-tests.log |
| Python skip | Windows 8.3 path API 필요, Linux에서 미실행 | observations-end.json |
| generator --check | exit0 | commands.txt |
| 실제7 bytes·C9/C10 비교·실제3 lock prepare/negative | PASS | real-seven-audit.json |
| 미래 engine/schema/generator/깊은 alias/source 금지 | 7/7 기대 결과 | future-policy-probe.json |
| source447→2d diff --check, docs/reviews 제외 | exit0 | commands.txt |
| local exact2d Doctor | **exit1, 3 warnings** | doctor-local.log |

Python 전체400에는 새 schema/generator 및 gzip regression도 포함된다. 초기 미래 probe driver에서 Python module 검색 경로를 지정하지 않아 import 실패한 것은 driver에서 sys.path를 추가해 바로잡았다. source는 바꾸지 않았다. 초기 producer 동일성 검사도 smoke lock 2개 최종 SRI 변경을 발견하여 실제 bounded delta로 기록했다. 테스트 실패를 source 수정으로 감추지 않았다.

원격 결과는 부모 설명만 받아 적은 것이 아니라 GitHub 도구로 exact2d commit runs→job 목록→해당 job log를 직접 읽었다. `ci-observation.json`, `ci-packages.log`, `ci-frontend.log`에 저장했다. 로그의 checkout/SOURCE_SHA도 exact `2d70461...`이다.

- [docs run43074529633](https://github.com/digitie/kor-travel-common/actions/runs/43074529633): 최종 직접 관찰 **6 jobs 전부 SUCCESS**. docs130710769963, Windows tools130710770367, Linux tools130710770404, secret130710770503, versions130710770518, packages130710770572.
- [packages job130710770572](https://github.com/digitie/kor-travel-common/actions/runs/43074529633/job/130710770572): 공식 Playwright1.65.0 / Chromium158.0.8127.18 launch 성공. UI101, 정책175, webpack 및 Turbopack build, **실제 packed browser65 PASS(40.5초)**. 이후 독립 example Turbopack build도 성공. 이 기록을 별도 10개 browser 실행으로 부르지 않는다.
- 같은 job에서 출력한 UI full SRI는 `sha512-avvikdgmPcgNQ8otiKOPRb/fCRSLRIEyV1dudqM4BsKfExScssK+NM7IirvH78lekd7xtEduReQ8/pyqD1BdNg==`, tokens는 `sha512-ope7vHGRynjiTDllGJj/qqVz6kmQ/NIsQr4+GnFmyh7jB2rdoTJI3UXU7S+CN5Z8sDMamQ1ez253+Y3ShXoqeQ==`. 정확히 C10 bytes. 고정 CSS+Scope 준비도 성공했다. C9 browser 결과를 새 Scope acceptance로 재사용하지 않았다.
- selftest43074529670 SUCCESS, python-package43074529681 SUCCESS.
- [common frontend43074529818 / job130710770267](https://github.com/digitie/kor-travel-common/actions/runs/43074529818/job/130710770267): **FAILURE**. type/build/unit/policy 뒤 required Doctor에서 실패. 아래 신규 finding. docs/packages 성공으로 이 실패를 덮지 않는다.

여기서 local reviewer가 common full Next browser65를 실행한 것은 **NOT_RUN**이다. 위65는 직접 확인한 새 exact CI 실행이다. 자기 Scope1 minimal packed browser9 PASS와 현재 common65를 혼동하지 않는다. 특정 앱의 actual export/deployment나 Pinvi composite scenario가 성공했다는 결론도 아니다.

## 5. 신규 A-P2-11 — 새 prepare helper가 required Doctor gate를 실패시킴

- 심각도: **P2**, disposition **OPEN / 수정 및 원 A 재확인 필요**, confidence 높음.
- 위치: `packages/ui/smoke/prepare-lock.mjs:33`, `:34`, `:36`; blocking 계약 `packages/ui/package.json`의 doctor script와 frontend workflow.
- 재현: exact2d에서 기존 고정 dependencies로 `npm run doctor --workspace packages/ui`. 원 reviewer 로컬 exit1. exact2d frontend CI도 같은 세 위치와 rule로 exit1.
- raw evidence:

```text
React Doctor — @kor-travel/ui
3 issues
Performance: 3 warnings
Array lookup inside a loop ×3
react-doctor/js-set-map-lookups
smoke/prepare-lock.mjs:33
smoke/prepare-lock.mjs:34
smoke/prepare-lock.mjs:36
npm error command sh -c react-doctor --scope full --no-score --no-telemetry --blocking warning .
```

- 원인/영향: 새 patched-engine loop의 artifactPackages/includes, packages/includes, axes filter/includes가 현재 필수 scanner 계약에 걸린다. **적은 엔진 목록의 lookup으로 실제 브라우저 성능 저하가 입증되었다고 주장하지 않는다.** 확인된 결함은 exact 후보의 필수 CI가 실패하여 merge gate를 충족하지 못하는 것이다. 부모 인계의 type/build PASS만으로 Doctor0을 추론할 수 없다.
- 수정 권고: helper의 허용 package/artifact 집합과 package→axis lookup을 loop 밖에서 구성하여 현재 membership 및 중복 axis 거부 의미를 유지한다. 또는 근거와 승인된 정책 변경이 필요하다. 전체 rule/gate를 조용히 비활성화하지 않는다. 이후 exact 새 source에서175 policy·실제3 locks·Doctor exit0 및 원격 frontend SUCCESS를 원 reviewer가 재확인한다. checker/policy 변경이 없으면 이 helper 수정만으로 runtime 재포장을 요구하는 주장은 하지 않는다.

## 6. 원 A finding disposition

| finding | 이번 상태 | 확인 경계 |
|---|---|---|
| A-P1-01 variants RSC | FIXED 유지 | 원 A source2 closure; 이번 UI runtime bytes 동일 |
| A-P1-02 forceMount map hidden | FIXED 유지 | 원 A source2 closure; 이번 해당 bytes 동일 |
| A-P2-01 Progress ARIA/max | FIXED 유지 | 동일 runtime |
| A-P2-02 table selection predicate | FIXED 유지 | 동일 runtime |
| A-P2-03 row/detail key namespace | FIXED 유지 | 동일 runtime |
| A-P2-04 kt table tokens | FIXED 유지 | 동일 runtime/CSS |
| A-P2-05 Tabs focus outline | FIXED 유지 | 동일 runtime/CSS |
| A-P2-06 Tabs orientation | FIXED 유지 | 동일 runtime |
| A-P2-07 official CSS variants | FIXED 유지 | 동일 CSS |
| A-P3-01 whitespace | FIXED 유지 | 현재 delta diff-check exit0 |
| A-P2-08 Table outline transition | FIXED 유지 | source3 원 A closure; 동일 runtime/CSS |
| A-P2-09 source AST import 경로 | FIXED 유지 | source4 원 A red/green; 새175에서 export/literal/TS/type/module extension 회귀 통과, patched 엔진도 source 금지 직접 확인 |
| A-P2-10 gzip 후속 member header | FIXED 유지 | 원 A f864 closure; exact2d scanner와 focused9 test source가 f864와 byte 동일, 전체400 regression PASS |
| A-SCOPE-P2-01 disabled fieldset edge | **OPEN, 별도 Scope 입력** | 원 Scope1에서 stock/fix1 양쪽 직접 재현. 현 C10의 f97 bytes 동일. 부모의 fix2 예정은 closure가 아님 |
| A-P2-11 Doctor gate | **OPEN, 신규 common P2** | 이번 exact2d 로컬/원격 실패 재현 |

과거 source4 CONDITIONAL, gzip 별도 PASS, consumer1 BLOCK, Scope1 CONDITIONAL 원문은 그대로 둔다. 이전 UI broad attacks 전부를 이번에 다시 실행했다는 뜻은 아니다. consumer1의 Geo/Map/Concierge 수정·Pinvi gate 및 consumer C10 migration은 후속 immutable input별로 본인 재확인해야 한다.

## 7. 결론과 미완료 경계

일반화 정책의 기능 범위에서 새 우회/회귀를 재현하지 못했다. 실제7 원장·byte·source 연결, 신규 정책175, 도구399/skip1, 자기 미래-engine 공격 및 새 exact CI packed65는 위 경계 내에서 성공했다. 그러나 **A-P2-11의 required frontend CI 실패는 남아 있으므로 COMMON6 CONDITIONAL**이다. 외부 Scope residual도 REQUIRED 수정으로 수락되었으며 새 version/code/pack input 전에는 FIXED 처리하지 않는다. 예정 C11 또는 새 Scope metadata/recipe/e2e를 현재 manifest의 결과로 승인하지 않는다. consumer 최종 병합·이미지 배포·backend lifecycle 승인은 별도다.
