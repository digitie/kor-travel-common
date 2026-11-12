# Common build rules 404a 原A 후보3 독립 적대리뷰 — SOURCE BLOCK

- Execution ID: A-COMMON-BUILD-404a-20261112T181610Z
- 원문 고정 UTC: 2026-11-12T18:16:10.333272+00:00
- 원래 독립 리뷰어 A/Mill. 구현/소스/index/branch 편집 0. 상대 CURRENT 원문·판정 열람 0.
- exact source: `404a586ece08ca0050d844cbe0eee4df5a79f899`
- observed tree: `1d7fb1c650d0c5d7104aa08277696b56008a1832`
- base: `678a5bcf0150ac0386bfa86106e7e0f4f77e8639`; previous BLOCK: `e1d0f01ef05b913e5f311a4d3ae2922a25a676c3`.
- manifest: `validation/review-common-build-rules-404a-20261113/manifest.json`
- manifest SHA256: `8f490c18ac2db2bbe7249d3b5b1a58f196875ea90300a77e8ad851b23cc56732`
- own evidence: `validation/review-A-common-build-rules-404a-3-evidence/`.
- 입력 21 Git blob/SHA256/bytes, tree, base 대비 경로 집합 및 e1d0 대비 변경12개를 직접 대조해 모두 일치했다. 소스는 Git object와 hash-bound dependency snapshot으로만 읽었다.

## 최종 판정·처리

**SOURCE BLOCK. P0 0 / P1 0 / P2 신규 OPEN 1 / P3 0. 기존 자기 finding 5건은 모두 FIXED.**

공식 INI/쉘 제어문자/physical default registry 수정은 유효하며 기존 공격과 exact76은 통과했다. 그러나 원문 고정 전 전달된 실제 소비자 정적 근거에서 새로운 false reject를 독립 재현했다. 정상 mkdir/chown의 `.npm` 경로를 CLI 호출로 오인하는 **A-COMMON-BUILD-P2-06**은 실제 새 소비자 연결을 막으므로 수정 전 수용 불가를 권고한다. 선행 진행 설명의 잠정 SOURCE PASS 판단은 이 추가 증거를 받기 전이었고, 후보3 원문은 그때 고정하지 않았다. 본 파일이 이 입력의 최종 원본이다. 원 c4cc/e1d0 BLOCK 원문은 그대로 보존한다.

원격 CI green과 이 source 결함은 별개다. P0/P1 운영 사고를 주장하지 않으며, 새 candidate·새 이미지·소비자 앱 운영 승인도 아니다.

## 원 finding별 본인 closure

| ID | disposition | exact404a 직접 근거 |
|---|---|---|
| A-COMMON-BUILD-P2-01 | **FIXED** | `tools/check_node_toolchain.mjs:56–58`이 공식 ini.parse의 전역 typed boolean만 검사한다. 원 literal force, 인용 force, section-only strict 모두 거부. 인용 strict 정상·중복 마지막 false·무관 peer 설정은 수용. own 원 반례/추가13 및 exact76에서 확인. |
| A-COMMON-BUILD-P2-02 | **FIXED 유지** | 원 strict=false/부정·분리 false/exec JSON 거부, true 동등표기 수용. 후보2 이후 해당 유효 옵션 검사가 유지되고 own 원 반례/13 및76 통과. |
| A-COMMON-BUILD-P2-03 | **FIXED 유지** | 원 heredoc/nondefault escape 거부. 연속행 heredoc 및 기본 backslash 정상 대조 통과. full Docker parser라는 확대 보증은 하지 않음. |
| A-COMMON-BUILD-P2-04 | **FIXED 유지** | global location/npx package 등 원 재선택 모두 거부. 정상 stage 상속/run/start 전달 인수 대조 통과. |
| A-COMMON-BUILD-P2-05 | **FIXED** | `:78`에서 shell 단일 &/리다이렉션/제어문자를 npm `--` 이전에 거부. 원 ampersand 재선택은 거부하며 지원 && 및 JSON exec 문자 인수 대조는 통과. |

closure는 이전 보고서를 고쳐 쓰거나 이전 CI를 새 candidate로 전용하는 뜻이 아니다. 본인 원 실패 payload를 현재 exact helper에 다시 적용한 결과다.

## 신규 A-COMMON-BUILD-P2-06 — `.npm` 경로를 npm 실행으로 오인해 정상 Dockerfile 거부

- 심각도/disposition: **P2 OPEN / 수정 필요 / 이관·제외 승인 없음**.
- 위치: `tools/check_node_toolchain.mjs:167`, `:171`; 결과가 발생하는 명령 head 검사 `:84–85`.
- 최소 재현: 정본 Node FROM과 canonical npm pin 뒤 아래 RUN을 둔다.

```dockerfile
RUN mkdir -p /home/node/.npm && chown -R node:node /home/node/.npm
```

- exact checker 결과: **ok:false**, `정적으로 검증 가능한 Node npm/npx 명령이 필요합니다` 2개. 실제 npm 호출은 없다. `.npx` 디렉터리의 mkdir도 같은 오류 1개다.
- 원인: `/\b(?:npm|npx)\b/`가 명령의 executable 위치가 아니라 전체 RUN/분할 part의 문자열 어디에든 적용된다. `/home/node/.npm`의 점/슬래시 경계도 word boundary이므로 mkdir/chown이 npmCommand로 넘어가고 첫 단어가 npm/npx가 아니라는 이유로 거부된다.
- 정상 대조: 같은 mkdir/chown에서 경로만 `/home/node/cache`로 바꾸면 ok:true. 이는 **원인 분리용 대조**이며 캐시 경로 변경을 수정책으로 권고하지 않는다. 실제 `npm ci --engine-strict=false`는 정상 거부되는 음성 대조도 유지했다.
- 실제 소비자 근거: 부모의 read-only r2 receipt는 정정된 반복 `--manifest` 사용, Common404a helper SHA, before/after 입력 hash 안정과 source HEAD를 기록한다. 본인은 아래 **4개 exact Git Dockerfile의 SHA256을 해당 receipt와 직접 대조**한 뒤 각 파일 전체를 own 정상 private-anchor fixture에 넣어 checker를 직접 호출했다. 4개 모두 cache mkdir/chown에 대한 같은 오류 2개만 발생했다.

| repo / exact source | path:line | 증거 |
|---|---|---|
| Geo `f196fee8c2ece62b6ea60b34caeaf1db3650d814` | `kor-travel-geo-ui/Dockerfile:39–40` | `.npm` cache mkdir/chown, SHA `923f3abf66de59cbd7f9460e1093241055afdd85b5d7864dec7dc6c894ef44de` |
| Weather `046e90d878a0331cc495d7ff08110499d29f24aa` | `deploy/Dockerfile.web:46–47` | SHA `f254ac02e4597bdcc8a4c25d0c179f7e313afe775386aeeae76ccab31c79d54f` |
| Transport `bdb2fabfa5067248afd809620c168310ae90cac5` | `frontend/Dockerfile:50–51` | SHA `55b502e67cd8b6a2dc795461977ba447f76642123d0b5d7fd6fd362cfcfa808c` |
| Transport 同上 | `packages/kor-travel-transport-admin/frontend/Dockerfile:37–38` | SHA `930fd53f849fa90538437986185710f9a07239b874010a2dce48a08836094182` |

- 영향: 정상 cache 권한 준비를 포함한 Geo/Weather/Transport의 새 private-toolchain 연결을 중앙 guard가 차단한다. 캐시 경로 이름 변경, Dockerfile 검사 제외, policy suppression으로 회피해서는 안 된다. 부모 r2는 STATIC_WIP_ONLY이며 이들 앱의 최종 source·image·runtime acceptance 승인이 아니다.
- 권고: 지원 bounded grammar에서 executable token과 data argument를 구분해 실제 npm/npx 호출만 버전/옵션 검사에 넘긴다. `.npm`/`.npx` 경로와 `echo npm` 등 데이터는 CLI가 아니다. 동시에 wrapper/shell 안에 숨은 미지원 실행을 조용히 통과시키지 않도록 기존 fail-closed 제어문자·selector·&&·JSON 대조를 보존한다. 이 실제 Dockerfile 패턴을 양성 회귀로 추가한다. 구현에는 참여하지 않았다.
- own proof: `own-consumer-boundary.test.mjs`, `.log`, `consumer-static-input-proof.json`, `consumer-docker-blobs/`.

## 직접 실행·dependency 출처

모든 test는 `/usr/local/bin/node --test <own evidence>/...`로 실행했다. 실제 Node **v22.22.2**, runner는 Node 내장이고 **공식 ini@7.0.0 dependency가 존재하는 fixture**다. dependency-free 테스트라고 주장하지 않는다.

| suite | 실제 결과 | raw SHA256 |
|---|---|---|
| exact `fixture/tests/check_node_toolchain.test.mjs` | 76PASS / 0FAIL / 0SKIP, exit0 | `05cec40229fbce975774255c9d9cf441e598d55de5dce29afdc13405042bfd00` |
| `own-seven-closure.test.mjs` (원 확정7 + 대조2) | 9PASS / 0FAIL / 0SKIP, exit0 | `01dee1c5860eb19f6fba7127456e98d07690beba6ca4edb2c97cdc970001cfce` |
| `own-regressions.test.mjs` (후보2 그대로) | 13PASS / 0FAIL / 0SKIP, exit0 | `21396c1626b67da81ac9d3fd48def440b2c4cf64d09bfef14ead910b65f07c9d` |
| `own-consumer-boundary.test.mjs` | **2PASS / 6FAIL / 0SKIP, exit1** | `d14124b3e42eb1c7821f95aee9a43634ceced852a049a6c68a6ae1b512dba668` |

마지막 suite의 6FAIL은 정상 `.npm`/`.npx` 최소2개와 실제 Dockerfile4개가 모두 기대 수용과 달리 거부되는 같은 결함이다. 다른 2개는 path 대조와 실제 잘못된 npm 명령 거부 대조다. 기존 테스트의 green을 상쇄해 숨기지 않았고 실패를 지우거나 기대값을 바꿔 재실행하지 않았다. 여러 suite의 중복 payload를 고유 테스트 총수로 합산하지 않는다.

Dependency는 manifest의 `immutable-3cdaeb79f759/node_modules/ini`에서 README/package/LICENSE/lib 네 파일을 **각 SHA256 검증 후** own fixture에 그대로 복사했다. 같은 registry tgz의 SHA512 SRI도 직접 계산해 lock/manifest와 일치하고 archive 내부 4개 파일의 SHA도 snapshot과 일치했다. 수기 INI lexer/이전 사설 parser/fallback 없이 실제 공식 package import를 실행했다. 설치는 하지 않았다.

- 정확 version: `ini@7.0.0`, Common private root devDependency only, ISC LICENSE 포함.
- SRI: `sha512-ifK0CgjALofS5bkrcTy4RaQ9Vx2Knf/eLeIO+NaswQEpH1UblrtTSCIvN71qQDMq0PeQ/SSPojvEJp9vvvfr+w==`.
- lib SHA256: `007123836ffec243f41c8b35584fb3db0498aa12a440a9e0efc675d0000f4c32`; 이전에 감사한 npm12.0.1 동봉 parser와 동일하다.
- metadata frozen ref SHA `15cacf3f1bc210d92adc057c8477569fe3c01e5696cf823c7442c6236f5c5673`도 일치. 과거 latest 관찰을 현재 registry 재조회 결과로 바꾸어 적지 않는다.

## 불변·규범·caller·canonical 증거

1. Root package는 ini exact devDependency 추가만이고, e1d0 lock에서 root의 ini 선언과 `node_modules/ini` 새 entry를 제거하면 **기존 lock JSON 전체 deep-equal**. 새 entry의 dependency 추가분은 단일 ini이며 공식 SRI/dev/license/Node engine이 일치한다. 일반 floor·다른 축·예외는 versions bytes 동일로 유지된다.
2. Public source/vendor/frontend policy **193/193** 이전 SHA와 일치. e1d0 대비 변경 없는9개 경로도 bytes 동일. 소비자 repo를 수정한 사실은 0이며 이 감사가 각 앱 WIP의 전체 graph/새 image acceptance를 새로 승인하지 않는다. 공개 C11/193 불변과 승인된 private root graph1 추가를 명확히 구분한다.
3. docs/ADR/T218/dev/tools가 예전 metadata-only·dependency 없이 실행한다는 문구를 현재 승인 범위로 고쳤다. 한정된 shell grammar이며 실제 image/임의 shell script 실행의 보증이 아님을 유지한다. native/EAS/store 및 T218 완료 주장 없고 CI 순서 최적화는 시작하지 않았다.
4. own `physical site#%`/`alias site#%`에서 direct/alias/preserve-symlinks-main 3형식이 모두 physical default registry로 canonical fixture를 수용했다. alias 옆 다른 registry가 default를 바꾸지 않았고, explicit override를 주면 그 값으로 대조해 불일치 exit1을 반환했다. 각 위치에 동일 hash의 INI 의존성을 제공했으며 dependency 없는 실행으로 바꾸어 적지 않는다. import-only 비자동 CLI 실행은 exact76 대조를 확인했다.
5. 404a는 3cda에서 `.github/workflows/consumer-smoke.yml:126`에 **기존 npm pin step 내부**의 `npm --prefix .kor-travel-common ci --ignore-scripts --engine-strict` 한 줄만 추가했다. immutable common checkout 경로와 pinned npm 후, guard 전에 dependency를 준비한다. 실제 Git diff로 helper/tests/root manifest/lock 불변을 확인했다. Step 순서 최적화 감사나 실제 manual workflow dispatch PASS는 아니다. old common-ref script/지원 입력이 없는 버전은 fallback 없이 실패한다는 기존 제한도 유지된다.
6. canonical-runtime receipt의 source7 + dependency4 **입력11개**, node/npm/runtime/builtin **log4개 SHA를 직접 검증**했다. Node22.23.1/npm12.0.1/runtime PASS/76PASS가 exact404a helper/tests/lock와 연결된다. 이는 owner의 기존 실행 근거 감사이며 본인의 canonical 실제 npm runtime 실행은 아니다. 404a 한 줄의 consumer-smoke 실제 install 성공으로 확장하지 않는다.
7. own prior c4cc report SHA `87ceded53ac283ec11a6f39092778c8279dc0a1489b12abd23ff82eb876fbff2`, e1d0 report SHA `2946611646e7b69de45ef4d8373228da7daff215e6b25a434f6d5c2f18d0856b` 그대로다.

## 추가 소비자 입력·NOT_RUN 경계

부모 제공 r2: `validation/phase2-build-toolchain-20261113/parent-404a-all-seven-static-toolchain-r2.json`, SHA `8e888437be7f71b23cd6a338ab8cb78dfaf17bb0882db2b601a6a4b4364c7164`. own evidence에도 bytes를 보존했다. r1의 잘못된 additive/default-root harness 이력은 부모 원문대로 남으며 이 finding의 재현 근거로 사용하지 않았다. r2는 actual app 실행·이미지 수용이 아니라 read-only 정적 시도다. 본인은 해당 repo의 움직이는 working tree 대신 receipt에 기록된 exact Git Dockerfile 4개를 읽었다.

본인 canonical Node22.23.1/npm12 실제 runtime, Windows OS, exact404a 원격 CI 상태 조회/실행, consumer-smoke dispatch/locked install의 실제 workflow 실행, 전체 Python400/전체 build/browser/Docker/registry image/운영 auth/배포/Map ops는 **NOT_RUN 또는 NOT_QUERIED**. 새 CI 성공을 가정하지 않았고 과거 green도 전용하지 않는다. B의 차단된 cleanup job 재시도0/상대 CURRENT raw 열람0. 테스트는 own TMPDIR 안의 종료 fixture만 자동 정리하며 타 owner/cache/경로 삭제0, 증거는 보존한다. 구현 소스와 앱 repo에 생성 출력0. 후속 immutable 입력에서 신규 P2-06만 필요한 범위로 원 리뷰어가 재확인한다.
