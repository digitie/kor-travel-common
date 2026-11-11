# NativeCSS 독립 적대리뷰 A(Mill) 1차

- Run ID: `Mill-A-native-css-1-8a03050-67fe4a9`.
- 역할: 구현에 참여하지 않은 reviewer A. visitor 동작·숫자·NativeCSS 실사용 compiler·portable runtime 우선.
- 시작 UTC: `2026-11-11T14:21:16Z`.
- 종료 UTC: `2026-11-11T14:33:45.929996+00:00`.
- 상태: `COMPLETE`.
- **Verdict: `CONDITIONAL` — 신규 OPEN P0 0 / P1 0 / P2 1 / P3 0.**
- 수정된 null/숫자 경로와 일반 경로의 native/WASM 동등성은 아래 범위에서 확인했다. `#` 설치 경로에서 portable WASM 로드가 실패하는 A-P2-01의 수정 또는 정식 연기 disposition이 남는다.
- 본 보고서는 별도 NativeCSS scope다. common source2 판정·소비 앱·native CSS 정책/배포 승인을 대신하지 않는다. 상대 reviewer 원문·finding은 열람하지 않았다.

## 1. Immutable 입력과 실제 관찰 SHA

manifest: `/home/digitie/dev/common-unification-20261111/review-manifest-native-css-1.json`.

전달/실제 SHA256: `89e7d4e49285e12c289ff124109450cdc1ba75f5a9d0c18ca97c75e726643203`.

| 구성 | base | 고정 검토 commit |
|---|---|---|
| lightningcss-fix | `1d680fa14e9a089c92dc0929f869d6757ae91c30` | `8a03050a00a30932fe49d2ca98f5f324a7f938a3` |
| serde-content-fix | `bb5066da57fb0d76a981dbbef04b68f2aff90a3f` | `67fe4a9c5b4595433a731b70dbe31412721bea8c` |
| 실제 pack 빌드 소스 | 위 LightningCSS base | `684c528b2d16c581c99cf829f9a4988985488d5f` |

최초 source 관찰은 두 manifest HEAD/clean이었다. 이후 구현 checkout은 다른 작업으로 진행되었다. 중간에 serde `deeedcc011e9cf54fc9cbeeb4397c8e843d57be2`를 관찰했고, 이 commit은 manifest67fe 대비 CI 파일만 변경했다. 종료 관찰 HEAD는 LightningCSS `7e88ee204da712049abc1c43b30054b813e2bf24`, serde `18e53fcf6f8ace093a292891b34fa3411192617d`이며 둘 다 clean이었다. **이 이동한 checkout 내용을 이번 고정 소스로 바꾸어 검토하지 않았다.**

모든 source diff는 지정 commit object로 읽었다. Rust 시험용 serde는 `git archive 67fe4a9`의 별도 snapshot을 `/tmp/review-A-nativecss-1/serde-source`에 만들었다. 종료에 tracked34파일을 다시 commit object와 byte 비교해 모두 동일함을 확인했다. LightningCSS Node 시험 입력도8a03050 object에서 추출했고, runtime은 실제 고정 tarball을 별도 경로에 푼 것을 사용했다. 소스를 수정하지 않았다.

pack 빌드684c528→review8a03050의 차이는 CI와 공개 합성 fixture/lock/후보 tgz 추가이며 Rust·Node runtime·WASM adapter·pack scripts의 제품 코드 차이는 없다. pack 내부 source archive는684c528을 담고 있는 것으로 검증했다.

common source2 보고서 `review-A-common-postfix-2.md`는 SHA256 `c74c05a4ae3b4752c38e5fa809e8fda432971fb13f424c7d6a526ad622411891` 그대로 보존했다.

## 2. Pack·source·license 일치 확인

파일: `artifacts/native-css-fix/lightningcss-1.33.0+nativecss.fix.3.tgz`.

- 크기15,309,655 bytes, SHA256 `862366190cfecbfbf770a4ef4ca9807a69f14d656f8ab5c9f64e85c428ee875c`.
- SHA512 `Q6DDVLGjtJ2zcOkvV2+bKcTAb8dB+HJXgDYAm9mrGL2Og2HBMCRzMaeOpGB8IgAxu11if506Wm6X3Dd+Rk+T7A==`(npm 접두사 sha512- 포함 대조).
- native binary SHA256 `8a38620c1bbf54acfb12f40b3180ce4e8510a5fb952e9173a3b7fe0b676ecbd6`.
- WASM SHA256 `4c2a5251dac4f47ebdadce39579febee5e12e00a3c892e5719e2a46ffa535a27`.
- source archive SHA256 `ef4e34efadd688ae5d626154811d2da0d726cfaa34ef9832cc9712b16c33e7f2`.
- embedded provenance는 manifest의 provenance 전체와 동일했다. source archive 일반267파일을684c528의 git object와 전부 byte 비교하여 불일치0을 확인했다. archive 안 Cargo.lock도 그 검토 대상에 포함된다.
- vendored serde의 src/tests26파일은67fe4a9 object와 동일했다. 별도 Rust snapshot의 Cargo.lock도67fe4a9와 일치한 채 사용했다.
- serde LICENSE-APACHE 11,357 bytes, LICENSE-MIT 1,023 bytes는 원 base의 전체 파일과 byte 동일했다. LightningCSS의 package LICENSE도 원 base와 byte 동일했다. source vendor의 이 full license 보존을 확인했다.
- bundled napi-wasm에는 출처·버전·상류 MIT 선언을 기록한 NOTICE가 있고, 상류에 독립 LICENSE 파일이 없다는 설명이 있다. 본 A의 검증은 serde full license와 LightningCSS 원 LICENSE 보존을 확인한 것이며, pack 전체에 대한 별도 법무 승인이라고 확대하지 않는다.
- 종료에 tarball의 원래 일반 file member가 추출된 package에서 모두 그대로인지 재확인했다. 시험용 node/test를 추가한 것 외 runtime file은 바뀌지 않았다.

실제 binary를 새로 전부 재빌드해 reproducible build를 증명한 것은 아니다. source/binary/WASM digest와 동작을 검증한 범위를 구분한다.

## 3. 직접 실행한 검증

영구 evidence: `/home/digitie/dev/common-unification-20261111/review-A-native-css-evidence-1/`.

정확한 실행 명령/환경은 `commands.txt`, `special-path-command.txt`, 실행 스크립트에 있다. Windows tool workdir `C:\`에서 `wsl.exe --exec`로 실행했다. WSL Node22.22.2와 기존 Node22.23.1 Docker images를 사용했다. 대형 npm 설치·LightningCSS native 재빌드는 하지 않았다. 기존 모듈과 crate cache는 읽기 참조하고 Rust 출력은 자기 `/tmp/review-A-nativecss-1/rust-target`에 격리했다. 다른 agent cache는 삭제하지 않았다.

| 직접 실행 | 결과 | Raw evidence |
|---|---|---|
| 고정 serde67fe offline/locked 전체 Rust suite+doctest | **126 PASS / 0 FAIL / 0 IGNORE**.60+3+28+5+7+22+1. | `rust-tests.log` |
| 별도 Rust 숫자/null 공격 harness | 기본 Some(()), opt-in None, 명시 Some(Unit) 보존; finite f64 overflow 거부, NaN/±Infinity opt-in, unsigned/signed 범위 검사 PASS | `rust-attacks.rs`, `rust-attacks.log` |
| 실제 pack의 upstream Node suite/native | **90 PASS / 0 SKIP** | `node-native-90.log` |
| 동일 pack 강제 WASM Node suite | **90 PASS / 0 SKIP** | `node-wasm-90.log` |
| 제공된 원본1.33.0 baseline.node에 최소 repro | var/env/100000/Infinity/property의 Rule·StyleSheetExit **10개 기대 실패를 직접 확인** | `reproduce-original133.log` |
| 같은 최소 repro/new native·WASM | 각각10 PASS | `reproduce-fixed-native.log`, `reproduce-fixed-wasm.log` |
| 추가 visitor 공격7입력×2visitor +4연속패스, 단일/동시2 bundleAsync | native/WASM PASS | `node-attacks.cjs`, `node-attacks-native.log`, `node-attacks-wasm.log` |
| 실제 NativeCSS compiler+실제 Pinvi CSS의 전체 IR 8입력 | 새 native·WASM·stock1.30.1 모두 기준 v8 IR과 deepStrictEqual | `nativecss-ir.cjs`, `private-ir-native.log`, `private-ir-wasm.log`, `private-ir-stock130.log` |
| 기존 고정 Bookworm image/native | glibc2.36, backend=native, identity visitor PASS | `bookworm-native.log` |
| 같은 Bookworm/강제WASM | backend=wasm, identity visitor PASS | `bookworm-wasm.log` |
| 기존 Alpine image/자동 선택 | glibc 없음, backend=wasm, identity visitor PASS | `alpine-auto.log` |
| `readelf --version-info` | native가 요구하는 GLIBC 최대값2.35 확인 | 도구 관찰 및 provenance 정책과 대조 |
| `#`가 있는 실제 package 설치 경로/강제WASM | **FAIL exit1, 잘린 위치의 .wasm을 찾다가 ENOENT** | `wasm-special-path-package.log`, `special-path-command.txt` |

Rust suite는 상류 기존 unused test type의 deny(warnings) 때문에 제출자와 같이 `--cap-lints=warn`을 사용했다. source 오류를 무시한 성공으로 요약하지 않으며, 이 옵션과 기존 warning을 raw log에 보존했다.

Docker는 기존 image만 `--pull=never --network none --read-only`로 실행하고 private package를 read-only bind했다. Alpine 실제 image ID는 `sha256:16e22a550f3863206a3f701448c45f7912c6896a62de43add43bb9c86130c3e2`, Bookworm은 manifest의 `sha256:6c74791e557ce11fc957704f6d4fe134a7bc8d6f5ca4403205b2966bd488f6b3`다. 새로운 image pull은 없었다.

원본1.33.0 재현은 handoff가 제공한 baseline.node를 읽어 실행한 것이다. 이 원본 binary를 본 reviewer가 새로 registry 설치하거나 재빌드하지는 않았다. 이번 candidate 자체는 manifest의 실제 tarball에서 추출한 code/binary/WASM을 썼다.

## 4. Visitor·숫자·NativeCSS 실사용 판단

### Null/기본 unit 의미

serde `src/de/mod.rs`의 coerce_unit_to_none는 default=false인 opt-in이며, Unit을 option에서만 None으로 본다. map/seq/tuple/struct/enum의 하위 Deserializer에 flag가 전달되는 source 경로와 전체126 suite를 확인했다. 별도 harness에서도 default Value::Unit→Some(()), opt-in Value::Unit→None, 명시 Value::Option(Some(Unit))→Some(())가 모두 유지되었다.

LightningCSS의 buffered AST 역직렬화6곳에만 이 opt-in이 사용된 것을 확인했다(napi4·rule1·property1). 단순 identity visitor에서도 실패하던 Specifier/env 경로가 new native/WASM에서 통과했다.

### 숫자 범위와 정밀도

finite f64 중 f32 범위 밖 값은 여전히 거부되며 u128::MAX→f32도 거부된다. 명시 coerce_numbers를 켠 경우에만 ±Infinity/NaN 변환과 큰 정수→float가 허용되는 것을 직접 시험했다. U64(256)→u8 및 I64(-1)→u64 overflow/sign 검사도 유지되었다.

**무손실 정수 변환까지 보장하는 API는 아니다.** opt-in U64(9007199254740993)→f64는 IEEE/Rust cast대로9007199254740992가 된다. 이 rounding을 실제 확인하고 기록했다. 이번 변경의 명시 coercion 정책과 기존 float narrowing 성격에 부합하는 것으로 보았으며 별도 defect로 올리지 않았다. 숫자검증 PASS를 모든 큰 정수의 exact precision 보장이라고 해석하면 안 된다.

첫 공격 harness는 CSS를4번 serialize/reparse한 결과가 최초 출력과 byte 동일해야 한다고 과하게 가정해 Infinity의 CSS 표기에서 실패했다. reparse 자체의 정상화와 visitor 효과를 분리하여, 같은 횟수의 non-visitor pipeline과 비교하도록 보정했고 candidate native/WASM은 통과했다. 이 스트레스 시험을 stock1.30.1에 추가 실행했을 때는 큰 수가 있는 반복 visitor의 기존 출력 차이가 남았다(`node-attacks-stock130.log`). 따라서 모든 CSS의 다중 재직렬화 동등성을1.30.1까지 증명했다고 주장하지 않는다. 아래 실제8입력 full IR 비교는 별도로 세 실행 모두 통과했다.

### 실제 compiler IR

Pinvi CSS input14,772 bytes의 SHA256은 `ac88ed642e3f71b9ea9f66810221f5fe520b3e3025931c60c67791a57ee1b0ed`이며 native style113개를 생성했다. var/env/nativeMapping 등을 포함한8입력 전체 IR을 v8.deserialize+deepStrictEqual로 비교해 NaN/Infinity가 JSON null로 숨지 않도록 했다. rounded-full borderRadius도 기준값9007199254740990으로 동일했다.

대규모 설치 없이 private pack만 대상으로 하기 위해 본 reviewer의 별도 Node process 안에서 lightningcss module resolution을 private package로 연결했다. 공유 node_modules 파일은 수정하지 않았다. **이는 실제 compiler와 후보 pack의 결합 동작 검증이며 새 clean install이나 최종 Expo/Metro resolver 채택 검증은 아니다.** 기존1.30.1도 같은 compiler 입력으로 직접 실행해 reference IR을 재확인했다.

공개 fork의 regression CSS는 변수·환경·큰 수·Infinity를 쓰는 합성5클래스 fixture다. 본 reviewer는 실제 Pinvi CSS를 공개 fork에 복사하지 않았다. private IR 입력과 공개 합성 입력을 구분했다.

## 5. Finding

### A-P2-01 — `#`가 포함된 설치 경로에서 portable WASM 초기 로드 실패

- 상태: **OPEN**.
- 위치: `lightningcss-fix/wasm/import.meta.url-polyfill.js:5`, `lightningcss-fix/scripts/build-candidate-wasm.mjs:38`, backend 적용 지점 `lightningcss-fix/scripts/pack-native-candidate.mjs:49`.
- packed 결과 위치: `wasm/wasm-node.cjs:44`의 import_meta_url 생성, `:1842`의 WASM readFileSync.
- 원인: CJS adapter의 file URL을 `'file:' + __filename` 문자열로 만든다. 파일명 안의 `#`가 URL fragment로 해석되어 실제 설치 경로가 잘린다. 이 helper는 상류 파일에서 온 것이지만, 이번 candidate가 다른 Node host의 기본 backend로 이 adapter를 선택하므로 후보의 portable runtime 계약에서 실질적으로 드러난다.
- 재현: 실제 pack의 JS/WASM 파일을 **symlink가 아닌** `/tmp/review-A-nativecss-1/path#withhash`에 배치하고 `LIGHTNINGCSS_FORCE_WASM=1 node -e "require('/tmp/review-A-nativecss-1/path#withhash')"` 실행. private 일반 경로의 같은 파일은 native/WASM 모두 정상이다.
- 실제: 모듈 초기화가 ENOENT로 실패하고 `/tmp/review-A-nativecss-1/lightningcss_node.wasm`을 열려고 한다. 실제 파일은 `path#withhash/wasm/lightningcss_node.wasm`이다. 직접 adapter 호출과 package entry 호출에서 각각 재현했다.
- 영향: 유효한 프로젝트/설치 경로에 `#`가 있으면 빌드 도구를 import하는 단계에서 실패한다. 자동 WASM을 쓰는 host와 강제 WASM 경로가 영향을 받는다. 일반 GNU native 경로 전체가 깨진다고 주장하지 않는다. 실제 macOS/Windows에서 실행한 결과로 확대하지 않는다.
- 권고: Node branch에서 `pathToFileURL(__filename).href`처럼 OS path를 정식 file URL로 인코딩하는 helper를 사용하고 adapter를 다시 빌드·재포장한다. 공백/`#`/`%` 설치 경로에서 새pack을 실제 require하는 host 회귀를 추가한다. filename 치환으로 provenance만 갱신하거나 기존 pack hash를 재사용하지 않는다.
- 근거: `wasm-special-path-package.log`, `wasm-special-path.log`, `special-path-command.txt`.
- disposition: 아직 `OPEN`. 수정된 immutable source+새 pack/manifest에서 원 reviewer 재확인 또는 owner·task·gate·기한을 갖춘 P2 DEFERRED 절차가 필요하다. 본 report에서 연기 승인하지 않았다.

## 6. Limits와 verdict 경계

- 소스·tarball·GNU/WASM 일반 동작은 위 범위에서 확인했다. 새 finding은 P2 한 건이며 P0/P1은 발견하지 않았다.
- macOS·Windows·EAS actual host/실기기, Pinvi Android/iOS export, 앱 배포는 **NOT_RUN(후속/별도 범위)**이다. Linux forced WASM과 Alpine 성공을 이들 host의 actual PASS로 확대하지 않는다.
- remote CI는 manifest 작성 시 LightningCSS matrix queued, serde run 조사 중으로 제공되었다. 본 reviewer는 remote API의 최신 상태를 새로 조회하지 않았고 이를 통과로 집계하지 않는다. platform CI와 별도 reviewer/merge 담당의 gate 정산이 남는다.
- license 확인은 위에 명시한 실제 source/full-text 보존 범위다. binary/source의 완전 재현 빌드 또는 전체 법무 감사까지 수용한 것은 아니다.
- 최초 common source2 보고서·정책 branch·소비 앱/CSS fork 최종 review 결과는 이번 범위에 섞지 않았다.
- **최종 CONDITIONAL.** A-P2-01의 수정 재확인 또는 정식 연기 disposition 없이 무조건 PASS로 요약하지 않는다. 실제 app export/deploy PASS가 아니다.

## 7. 보존 산출물

- 새 raw report: `/home/digitie/dev/common-unification-20261111/review-A-native-css-1.md`.
- evidence: `/home/digitie/dev/common-unification-20261111/review-A-native-css-evidence-1/`.
- `observations-start.json`, `observations-end.json`: 입력/관찰SHA·archive267파일·종료 snapshot34파일·pack 원 member 불변·common source2 report hash.
- `vendor-source-check.json`, `license-retention.json`: vendor26파일과 원 full license 대조.
- `rust-tests.log`, `rust-attacks.*`, `node-*-90.log`, `reproduce-*.log`, `node-attacks*.log`: 실제 시험/경계 공격 원문.
- `nativecss-ir.cjs`, `private-ir-*.log`: 실제 compiler IR 비교, 입력은 공개 fork에 복사하지 않음.
- `runtime-probe.cjs`, `bookworm-*.log`, `alpine-auto.log`: 기존 read-only/network-none Docker 실행.
- `wasm-special-path*.log`, `special-path-command.txt`: 신규 finding 재현.

자기 격리 snapshot·시험 파일과 report/evidence만 생성했다. 구현 저장소·후보 tarball·공통 원문·타 agent cache를 수정/삭제하지 않았다.
