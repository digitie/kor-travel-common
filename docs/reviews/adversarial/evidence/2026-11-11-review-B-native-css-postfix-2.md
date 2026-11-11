# NativeCSS 원 리뷰어 B(Epicurus) — 수정 후 immutable manifest 2 재검토

- 실행 ID: `Epicurus-B-native-css-postfix-2-20261111T151958Z`
- 시작 UTC: `2026-11-11T15:19:58Z`
- 종료 UTC: `2026-11-11T15:32:23+00:00`
- 역할: 최초 B와 동일한 packaging / 실제 해석 경로 / Cargo vendor / license / CI source-binary 연결 독립 리뷰어
- 기존 finding: **3건 모두 FIXED** (P1 1건, P2 2건)
- 신규 finding: **없음**
- Source 검토: **PASS**
- 최종 verdict: **CONDITIONAL — exact macOS CI queued. source-gate·Ubuntu·Windows는 SUCCESS**

조건은 정확한 Lightning748 head의 macOS host job 완료와 성공 확인이다. 이 조건을 source defect나 새 Pn finding으로 만들지 않았으며, 대기 상태를 전체 호스트 PASS로 세지 않았다. source 승인 범위는 두 fork와 fix.4 pack이며, common Dialog/모바일 scroll·common 후속 policy·실제 소비자 export·배포는 포함하지 않는다.

## 불변 기준선과 격리

manifest: `/home/digitie/dev/common-unification-20261111/review-manifest-native-css-2.json`

- 직접 관찰 SHA256: **1215c43638009758821f3ec29bdce037513e5c01f6aa76d3839820802ef5428c**, 요청과 일치.
- Lightning observed head: **748651cbd845971e65c411166ddee101745dab21**
- 이전 Lightning review head: **8a03050a00a30932fe49d2ca98f5f324a7f938a3**
- fix.4 source archive revision: **1e94372a6da4a55eac4a6dc3ff9cdeec103e8ac1**
- serde observed head: **18e53fcf6f8ace093a292891b34fa3411192617d**
- 이전 serde review head / vendored production: **67fe4a9c5b4595433a731b70dbe31412721bea8c**

`git rev-parse <sha>^{commit}`, `git show`, `git diff`로 객체와 delta를 확인했다. reviewer 소유 detached worktree는 `/tmp/review-b-native2-lightning-20261111-151958`, `/tmp/review-b-native2-serde-20261111-151958`이다. 시작과 종료 모두 해당 HEAD이고 최종 `git status --porcelain=v1`이 빈 문자열이다. Python 시험이 만든 자체 __pycache__만 정리했다. 원 source 파일은 수정하지 않았다.

원문 `review-B-native-css-1.md`의 SHA256 **e077602b2bfec00c6d498112bc69c4918eded2227137db15b264634ed7bd16fe**, manifest1의89e7d4… 및 fix.3/Q6DD tarball의862366…을 재대조해 보존을 확인했다. 새 report와 evidence만 작성했다. peer의 원문·결과는 열람하지 않았고 구현 handoff에서 제공한 delta를 자체 source·artifact·실행 증거로 대조했다.

증거 디렉터리: `review-B-native-css-postfix-2-evidence/`. metadata에 있던 common 관련 log는 hash만 대조했고 이번 source 판정에 사용하지 않았다.

## 새 pack 및 재사용/재빌드 연결의 독립 검증

파일: `artifacts/native-css-fix4/lightningcss-1.33.0+nativecss.fix.4.tgz`

- 버전: **1.33.0+nativecss.fix.4**
- 실제 크기: **15,376,394 bytes**
- SHA256: **12c8326428a56e38231f7b5b376df0c6882e3492da794f3499269628edcaccf0**
- SRI: `sha512-zDQ03VJE37OlyBrLsRcsEdIVu0T4BXJKDH5y9//To6GlGN2UrKQGERFVAFblkPQ5ZEbhuOp5wpXxGARZNdbQLA==`

직접 계산한 값이 manifest2·manifest-fix4와 모두 일치했다. verification.json이 지정한 evidence hash17개도 일치했다.

| 연결 | 실제 확인 |
|---|---|
| 대응 source archive | `git archive 1e94372 --format=tar.gz` 전체 bytes와 동일, source284개 |
| archive hash | e36a53d7dac040b249399c73d7079d4c9d2769d221746891294e06c46ed14f89 |
| historical tgz | archive 안에0개. `.gitattributes` export-ignore 적용 확인 |
| 현재 head와 archive | source gate가 fixtures/nativewind5의 후속 fixture metadata만 제외하고 파일 집합·내용 동일성 확인 |
| Rust/Cargo/vendor digest | Python gate와 JS helper를 각각 실행해 현재748·내장1e·실제 compiled684의 입력이 모두 `23cc04bc2587fe044f8e4fdf21690eb8fa7a4ebedbc388a06cb3602aac426c75`임을 확인 |
| 기존 native / optimized WASM | fix.3과 실제 bytes 동일. SHA256은 각각8a38620c… /4c2a5251…로 provenance 일치 |
| raw WASM | 기존 raw 파일을 직접 hash해 `d392deef78bf3cd0026c9e05fab68d3b185a561e89240e5e875f5c6a82f8d443` 확인, reuse 계보·adapter receipt와 일치 |
| 새 adapter | SHA256 `9aacec17ea517e31eaf39cecb60eada7cfa637ec3f4629c04ff0af9e63148d90`, receipt·provenance·실제 output 일치 |
| adapter 입력 | helper/runtime/notice/package.json 등10개 경로의 현재 source hash가 receipt와 모두 일치 |
| 실제 빌드 도구·외부 입력 | 기존 도구의 esbuild0.28.2 / napi-wasm1.1.3 MIT를 읽고, napi index.mjs의 `0108dc67…` hash가 receipt와 같은지 직접 확인 |
| Cargo lock | aa5fe01e…로 이전 Rust build와 동일 |
| Node binding/loader | 복사되는 Node 파일이 source와 일치하고 생성 index.js의 wrapper tail·native/WASM 선택문도 현 packer source와 대조됨 |

현재 source와 compiled684의 Rust 입력 동등성을 근거로 native/raw/optimized WASM을 재사용했다. JS adapter만 새로 번들한 계보가 명확하다. 내가 새 native/WASM을 rebuild했다고 주장하지 않는다. 1e94372 이후748의 차이는 새 pack·fixture manifest·fixture dependency/verify 버전 핀이다.

Rust fingerprint는 전체 .rs, Cargo.toml/lock, .cargo, rust-toolchain.toml, serde vendor를 포함한다. 현재 source의 컴파일 시 외부 include_str/include_bytes 자산 경로도 점검했으며 이 delta에서 미포함 입력 때문에 재사용이 틀렸다는 근거는 발견하지 않았다. 현재 receipt의 입력 집합·실제 도구 버전·원천 file hash까지 별도로 대조했으며 self-declared hash 일치만으로 끝내지 않았다.

## 직접 실행한 최소 검증과 추가 공격

새 npm install·crate download·대형 Rust/native build는 **0회**다. 기존 모듈은 읽기 참조했고, pack·시험 파일·출력은 reviewer 소유 `/tmp`에 두었다.

| 검증 | 직접 재실행 결과 | evidence |
|---|---|---|
| source gate | PASS,284files·정확 source·입출력/재사용 digest 연결 | `source-gate.log`, `input-digest-js.log` |
| 기본 gate 회귀 |4 tests PASS | `source-negative4.log` |
| 통합 gate 공격 |7 cases 모두 기대값(양성2, 부정5) | `integrated-source-attacks.py`, `integrated-source-attacks-final.log` |
| 실제 fix.4 native Node |90/90 PASS, skip0 | `node-native90.log` |
| 실제 fix.4 강제 WASM Node |90/90 PASS, skip0 | `node-wasm90.log` |
| 실제 복사 경로4 |space / # / % / 복합 모두 강제 WASM require·identity visitor 성공 | `special-paths4.log` |
| 추가 복사 경로3 |문자열 %2F, 한글·emoji·%·#, %25 복합 모두 성공 | `additional-paths.cjs`, `.log` |
| 실제 Expo compiler 선택·IR |fix.4의 실제 resolver 선택과 loader bytes를 검증, native/WASM 각각8case/5class 전체 IR이 기준1.30.1과 deepStrictEqual | `compiler-native.log`, `compiler-wasm.log` |
| diff whitespace |두 repository delta 모두 exit0 | 직접 immutable diff 확인 |

통합 공격은 실제 source-gate main에 메모리 입력 fault를 넣었다. current Rust 변경, URL helper 변경, build helper 변경, adapter output 변경은 거부됐다. fixture README만 바꾸는 예외는 통과했고 fixture 예외 경로에 새 Rust 파일을 숨기는 경우는 Rust digest에서 거부됐다. source 파일·pack을 물리적으로 수정하지 않았다. 최초 자체 mock 중첩 harness의 경로 처리 오류는 별도 최초 log로 보존했으며 수정된 harness 결과와 구분했다.

특수 경로 시험은 symlink가 아닌 실제 package 복사로 실행했다. 이때 borrowed node_modules를 복사하지 않도록 runtime 도구 symlink를 붙이기 전에4개 시험을 실행했고 추가3개 시험 전에는 해제했다. URL helper는 Node branch에서 pathToFileURL(__filename).href를 사용하며 old fix.3의 #/% 경로 문제와 구분된다.

로컬 compiler 실행에 사용한 기존 `consumer-fixture-fix4`의 실제 loader·adapter·WASM·provenance·receipt가 이번 추출 pack과 동일한 bytes인지 먼저 확인했다. 기존 dependencies 참조이므로 clean install 증거는 아니다. private113 CSS나 실제 앱 export를 새로 실행한 것으로 확대하지 않는다.

### 주요 실행 명령

```bash
sha256sum review-manifest-native-css-2.json review-B-native-css-1.md
git worktree add --detach /tmp/review-b-native2-lightning-20261111-151958 748651cbd845971e65c411166ddee101745dab21
git worktree add --detach /tmp/review-b-native2-serde-20261111-151958 18e53fcf6f8ace093a292891b34fa3411192617d
python3 scripts/test-native-css-source.py
python3 scripts/check-native-css-source.py
# JS rustInputs/inputHashes를 현재 head와 compiled684에 각각 실행해 대조
# Python hashlib/tarfile와 git archive로 pack/source/receipt를 직접 대조

# cwd는 불변 Lightning worktree이며 uvu는 기존 도구를 읽기 참조
node /tmp/native-css-fix-20261111/node_modules/uvu/bin.js /tmp/review-b-native2-runtime-20261111-151958/package/node/test
LIGHTNINGCSS_FORCE_WASM=1 node /tmp/native-css-fix-20261111/node_modules/uvu/bin.js /tmp/review-b-native2-runtime-20261111-151958/package/node/test
# 고정 test-special-paths.cjs 함수로 실제 pack의4개 복사 경로 실행
node additional-paths.cjs
python3 integrated-source-attacks.py
NATIVE_FIX_CONSUMER_ROOT=/tmp/native-css-fix-20261111/consumer-fixture-fix4 node verify.cjs
LIGHTNINGCSS_FORCE_WASM=1 NATIVE_FIX_CONSUMER_ROOT=/tmp/native-css-fix-20261111/consumer-fixture-fix4 node verify.cjs
node compare-ir.cjs baseline-compiled-results.bin compiled-results.bin
```

## 기존 finding closure

| 원 ID | 원 심각도 | disposition | 원 리뷰어의 재확인 |
|---|---|---|---|
| **B-NATIVE-P1-01** | P1 | **FIXED** | `node/test/bundle.test.mjs:47`, `:98`에서 두 in-memory Map의 key도 host path.normalize로 통일됐다. Linux의 native/WASM90을 직접 통과했고, 정확748의 **Windows130613790166이90/90·skip0·IR8·특수 실제 복사4까지 성공**했음을 원격 로그로 직접 확인했다. 이전7e의 Windows green도 별도 이력이며748 결과를 대신하지 않았다. |
| **B-NATIVE-P2-01** | P2 | **FIXED** | `vendor/napi-wasm-NOTICE`에 MIT 허가·조건·면책 전문이 들어갔다. 고정 upstream author/license package.json 사본도 repo/source archive/npm wasm에 같이 포함되고 bytes가 일치했다. upstream에 없는 copyright 연도/권리자를 추정해 추가하지 않았다는 설명이 명확하다. serde의 기존 MIT/Apache 원문도 보존돼 있다. |
| **B-NATIVE-P2-02** | P2 | **FIXED** | `.github/workflows/fixed-pack.yml`에 release PR에서도 실제 source-gate job이 추가됐다. current checkout↔archive↔compiled Rust digest↔native/WASM↔adapter receipt를 검증하고, exact checkout의 Rust 회귀도 실행한다. 로컬 기본4+통합7 공격을 통과했다. 정확748의 **source-gate130613789086 SUCCESS**에서 Lightning test_serde2, vendor integration65, doctest1을 실제 확인했다. |

FIXED는 manifest2에 대한 원 리뷰어의 source/artifact/실제 실행 근거를 바탕으로 한 closure다. 아직 queued인 macOS 전체 host gate의 PASS를 뜻하지 않는다.

## 새 delta coverage 및 source CI 확인

Lightning delta는20파일이다. source gate·packaging helpers·receipt·MIT 고지·URL polyfill·special-paths fixture·export-ignore·host-normalized resolver·fix.4 핀과 source2의 fixture-only 차이를 확인했다. serde delta는 CI2파일과 src/tests.rs의 새 nested derive roundtrip 시험이다.

serde18은 Foo/Bar를 실제 Foo(Bar(Value::Unit))의 Serialize/Deserialize 왕복에 사용한다. production deserializer와 Lightning vendor67fe는 변하지 않았으며 cap-lints로 경고를 억제하지 않는다. 정확18의 [기존 CI43038941237](https://github.com/digitie/serde-content/actions/runs/43038941237)의 Check/Test와 [명시 Rust 회귀43038941426](https://github.com/digitie/serde-content/actions/runs/43038941426)의 regressions가 모두 SUCCESS임을 직접 API 조회했다.

정확748의 source-gate 원격 log에서 다음 명령과 성공 수를 직접 확인했다.

```bash
python3 scripts/test-native-css-source.py                     #4 tests
python3 scripts/check-native-css-source.py                    #PASS,284files
cargo +1.92.0 test --locked --test test_serde --features serde  #2 PASS
cargo +1.92.0 test --locked -p serde-content --test attributes --test errors --test newtype --test numbers --test roundtrip  #3+28+5+7+22=65 PASS
cargo +1.92.0 test --locked -p serde-content --doc              #1 PASS
```

이를 로컬 Rust 재빌드나 vendor 전체126 unit 성공으로 바꾸어 세지 않았다. source-gate는 경고 완화 flag 없이 실행되며, serde18의 일반/명시 CI 성공은 그 별도 repository의 exact18 증거다. 새로운 Lightning 전체 all-features suite가 실행됐다고 확대하지 않는다.

신규 P0/P1/P2/P3 finding은 발견하지 않았다. 기존 parser 기본 unit Some(())와 numeric coercion production source는 Rust digest가 compiled684와 동일하므로 source1에서 확인한 의미를 유지한다. fix.4 변경의 핵심인 JS adapter 경로·packaging·source 연결은 이번 probe와 새 CI로 추가 검증했다.

## exact CI 미완료 경계와 최종 판정

[Lightning run43047084671](https://github.com/digitie/lightningcss/actions/runs/43047084671)은 이번 **748** head의 exact run이다. 원격 jobs와 원본 log를 직접 조회했다.

| job | 관찰 결과 |
|---|---|
| source-gate130613789086 | **SUCCESS** — source/receipt/부정회귀4/Rust2/vendor65/doctest1 |
| Ubuntu130613790164 | **SUCCESS** — native90/WASM90, 각IR8, 실제 복사 경로4 |
| Windows130613790166 | **SUCCESS** — 자동 WASM90, IR8, 실제 복사 경로4 |
| macOS130613789629 | **queued**, 최종 조회 시 미완료 |
| codspeed43047084763 | skipped, PASS 수에 포함하지 않음 |

evidence의 `remote-exact-ci.json`에 run/job ID·관찰 UTC·관련 원본 log 발췌를 보존했다. parent의 같은 상태 전달과 별개로 reviewer가 직접 조회한 결과다.

**최종 verdict: CONDITIONAL. 기존3건 모두 FIXED, 신규0, source 검토 PASS.** 정확748의 macOS job이 queued이므로 전체 host matrix/merge gate가 완료됐다고 승인하지 않는다. macOS가 실패하면 해당 exact 실패 원인을 별도 후속 검토하고, source/pack이 바뀌면 새 불변 manifest를 받아 재검토한다.

common의 새 Dialog/mobile-scroll·후속 policy·소비자 채택·Pinvi 실제 export·이미지·운영 배포는 이번 범위 밖이다. 이 report의 source/pack/IR 성공을 그 gate의 PASS로 확대하지 않는다. 원문 source1·manifest1·fix.3와 peer 비공개를 유지했다.

종료 시 두 reviewer 소유 worktree와 추출/공격용 임시 디렉터리를 정리했다. 기존 모듈·캐시·artifact·원문은 삭제하지 않았다. 최종 원본/manifest 해시와 clean 격리 증거는 evidence에 보존했다.
