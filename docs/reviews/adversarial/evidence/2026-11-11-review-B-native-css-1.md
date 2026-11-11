# NativeCSS 독립 적대리뷰 B — immutable manifest 1

- 실행 ID: `Epicurus-B-native-css-1-20261111T142118Z`
- 시작 UTC: `2026-11-11T14:21:18Z`
- 종료 UTC: `2026-11-11T14:38:46+00:00`
- 역할: 원 리뷰어 B(Epicurus), 패키징·실제 해석 경로·Cargo vendor·라이선스·CI source/binary 연결 전문. 구현 참여 없음.
- 최종 verdict: **BLOCK**
- finding: **P1 1건 / P2 2건, 모두 OPEN**. 확인된 Rust/native/WASM 변환 동작의 신규 실패는 없었다. BLOCK의 직접 근거는 고정 head의 필수 Windows host CI 실패다.

## 불변 범위와 관찰 SHA

manifest는 `/home/digitie/dev/common-unification-20261111/review-manifest-native-css-1.json`이다. 실제 SHA256 `89e7d4e49285e12c289ff124109450cdc1ba75f5a9d0c18ca97c75e726643203`이 요청과 일치한다.

| 구성요소 | base | observed head |
|---|---|---|
| Lightning CSS fork | 1d680fa14e9a089c92dc0929f869d6757ae91c30 | **8a03050a00a30932fe49d2ca98f5f324a7f938a3** |
| serde-content fork | bb5066da57fb0d76a981dbbef04b68f2aff90a3f | **67fe4a9c5b4595433a731b70dbe31412721bea8c** |
| 실제 pack source | 위 Lightning base | **684c528b2d16c581c99cf829f9a4988985488d5f** |

`git rev-parse <sha>^{commit}`, `git show`, `git diff`로 객체를 확인했다. 두 저장소에는 AGENTS.md가 없었고 사용자 요청과 기존 common의 독립 리뷰·증거 규칙을 따랐다. 소스는 `/tmp/review-b-native-lightning-20261111-142118`, `/tmp/review-b-native-serde-20261111-142118`의 detached worktree에서만 읽었다. 시작·종료의 HEAD는 위 SHA이고 `git status --porcelain=v1`은 빈 문자열이다. tracked source를 편집하지 않았다.

공통 source2 보고서 두 개는 별도 불변 원본으로 보존했다. 최초/후속 SHA256은 각각 `520356751417c84ecb0f8d078891556e3533c2b93a9d09184b6260567867ce87`, `45b6aa8bce5f47ce50ce562f6f056eba1213e8860ab1e147ddd765dd7bf59446`이며 종료 전에 재대조했다. peer A의 원문·finding·결과나 통합 report는 열람하지 않았다.

이번 범위는 두 fork, 고정 pack, Cargo source/vendor, compiler fixture 및 CI다. common 후속 policy branch·실제 앱 export/배포·별도 source2 closure는 포함하지 않는다.

## 고정 artifact와 source/binary 대조

파일: `artifacts/native-css-fix/lightningcss-1.33.0+nativecss.fix.3.tgz`

- 크기: **15,309,655 bytes**
- SHA256: `862366190cfecbfbf770a4ef4ca9807a69f14d656f8ab5c9f64e85c428ee875c`
- integrity: `sha512-Q6DDVLGjtJ2zcOkvV2+bKcTAb8dB+HJXgDYAm9mrGL2Og2HBMCRzMaeOpGB8IgAxu11if506Wm6X3Dd+Rk+T7A==`

실제 파일을 직접 해시해 manifest·고정 fixture에 있는 tarball과 일치함을 확인했다. pack의 provenance에 있는 native / WASM / source / Cargo.lock 해시도 각각 일치했다.

| 항목 | 검증 결과 |
|---|---|
| native .node | SHA256 `8a38620c1bbf54acfb12f40b3180ce4e8510a5fb952e9173a3b7fe0b676ecbd6` 일치 |
| WASM | SHA256 `4c2a5251dac4f47ebdadce39579febee5e12e00a3c892e5719e2a46ffa535a27` 일치 |
| source archive | SHA256 `ef4e34efadd688ae5d626154811d2da0d726cfaa34ef9832cc9712b16c33e7f2` 일치 |
| Cargo.lock | SHA256 `aa5fe01e8cecd9c200eabdf6f3028bc717b1d1959c4e19b61e05ae7152eb55b2` 일치 |
| archive 재현 | 내장 `native-source.tar.gz`가 **git archive 684c528의 bytes 전체와 동일** |
| vendor | 내장 source의 serde-content source·tests·LICENSE 28개를 별도 fork67fe와 비교해 불일치 0 |
| upstream license | serde의 LICENSE-MIT·LICENSE-APACHE가 base bb5066d 원문 전체와 동일 |

내장 source archive에는 267개 파일이 있었다. root `[patch.crates-io] serde-content = { path = "vendor/serde-content" }`와 path dependency의 lock entry를 확인했다. root workspace에는 napi도 포함되어 있어 patch가 root/napi 양쪽 serde-content 해석에 적용된다. 작업자 로컬 serde checkout이나 미발행 registry crate가 필요한 구조가 아니다.

684c528 이후8a03050의 delta는 CI·합성 fixture·baseline IR·고정 vendor tgz이며 Rust production source는 변하지 않았다. 따라서 이번 기준선에서는 실제 빌드 source684c와 검토 head8a를 구분하는 근거가 있다. 새 Rust 전체 rebuild로 binary를 bit-for-bit 재생성한 것은 아니며, source archive·기록 해시·동작 시험을 대조한 결과다.

## 실제 사용 경로와 최소 동작·공격 검증

새 npm install·cargo download·native/WASM 대형 rebuild는 수행하지 않았다. 전달 pack을 reviewer 소유 `/tmp`에 추출했다. uvu 등 도구와 실제 consumer resolver는 기존 `/tmp/native-css-fix-20261111/` 모듈을 읽기 참조했고, 삭제·재설치는 하지 않았다. Rust는 기존 1.92.0 toolchain/cache를 사용한 **offline** 소규모 시험만 수행했다. 자체 target은 종료 때 정리한다.

| 직접 검증 | 결과 |
|---|---|
| 원본1.33.0 visitor 재현 | 제시된 Rule/StyleSheetExit 실패를 기대대로 확인 |
| 기준1.30.1 | 같은 최소 재현 모두 성공 |
| fix.3 native 최소 재현 | 5 CSS × 2 visitor 성공 |
| fix.3 강제 WASM 최소 재현 | 같은 10회 성공 |
| 전달 pack native Node suite | **90/90 PASS, skip0** |
| 전달 pack 강제 WASM Node suite | **90/90 PASS, skip0** |
| 고정 serde source 전체 suite | **126 PASS** (125 unit/integration + doctest1), Rust1.92.0 / `--cap-lints=warn` 사용 |
| 별도 Rust 공격 | **12 PASS**, 자체 fixture doctest0은 PASS 수에 더하지 않음 |
| 실제 Expo resolver·compiler | 선택된 fix.3 loader/native/WASM/adapter가 전달 pack과 bytes 일치, 공개 synthetic CSS5classes의 전체 IR8cases가 native/WASM 모두1.30.1 baseline과 deepStrictEqual |
| 기존 실제 Pinvi IR 증거 | 보존된 v8 binary를 직접 deserialize/deepStrictEqual: native/WASM 모두8cases·113classes 일치. 새 Pinvi compile/export를 수행한 것으로 세지 않음 |
| 병렬 bundleAsync 공격 | 지연된 두 독립 read Promise의 결과가 native/WASM 모두 각각 올바름 |
| host routing 공격 | 현재 glibc/구 glibc/musl/arm64/macOS/Windows/forced 7개 분기에서 기대 backend 선택 및 최소 변환 성공. **플랫폼 속성 모의 검사이며 실제 각 OS 실행 PASS가 아님** |
| ABI 최소 요구 | 추출한 .node의 readelf 요구 GLIBC 최대2.35 |
| diff whitespace | 두 source delta 모두 exit0 |

Rust 공격은 기본 `Unit → Option<()> = Some(())`, opt-in `Unit → None`, 명시 `Some(Unit)` 보존, 중첩 map/struct, Infinity/NaN/음의0, 유한 f64→f32 overflow, u128MAX→f32 overflow, 큰 signed integer→float, 정수 대상 overflow/음수→unsigned 거부를 포함했다. 정밀도는 **coercion off에서는 큰 정수→f64 거부, on에서는 Rust cast와 같은 명시적 반올림**을 확인했다. 예를 들어9007199254740993이 coercion on에서9007199254740992.0이 된다. 이를 무손실 변환으로 보고하지 않는다.

원래 serde default unit 의미는 보존되고, Lightning의 buffered deserialization 6곳에서만 새 null opt-in을 켰다. 숫자 coercion도 기존 opt-in 경계를 유지한다. serialize/deserialize와 compiler IR 비교는 JSON stringify만 사용하지 않고 v8 serialization과 deepStrictEqual을 사용해 Infinity/NaN이 null로 숨는 문제를 피했다.

보존된 Bookworm/Alpine 실제 실행 로그도 참조했다. 이 리뷰의 플랫폼별 직접 실행 범위는 WSL Linux x64이며, 실제 macOS/Windows/EAS/ARM 테스트 성공으로 확대하지 않는다.

## 실행 명령·증거

세부 로그와 공격 소스는 `review-B-native-css-1-evidence/`에 보존했다. 명령의 실제 경로·run ID는 다음과 같다.

```bash
sha256sum review-manifest-native-css-1.json
# 각 repository에서 git rev-parse/git show/git diff 확인 뒤:
git worktree add --detach /tmp/review-b-native-lightning-20261111-142118 8a03050a00a30932fe49d2ca98f5f324a7f938a3
git worktree add --detach /tmp/review-b-native-serde-20261111-142118 67fe4a9c5b4595433a731b70dbe31412721bea8c

# Python hashlib/tarfile로 manifest/provenance/file 비교 및 git archive bytes 대조
node fixtures/nativewind5/reproduce.cjs /tmp/native-css-fix-20261111/node_modules/lightningcss --expect-failure
node fixtures/nativewind5/reproduce.cjs /tmp/native-css-fix-20261111/consumer-fixture-baseline/node_modules/lightningcss
node fixtures/nativewind5/reproduce.cjs /tmp/review-b-native-runtime-20261111-142118/package
LIGHTNINGCSS_FORCE_WASM=1 node fixtures/nativewind5/reproduce.cjs /tmp/review-b-native-runtime-20261111-142118/package

# cwd는 불변 Lightning worktree. test assets도 이 source에서 읽음.
node /tmp/native-css-fix-20261111/node_modules/uvu/bin.js /tmp/review-b-native-runtime-20261111-142118/package/node/test
LIGHTNINGCSS_FORCE_WASM=1 node /tmp/native-css-fix-20261111/node_modules/uvu/bin.js /tmp/review-b-native-runtime-20261111-142118/package/node/test

# 기존1.92.0 cargo/rustc/rustdoc, 기존 cache, 별도 자체 target을 지정하여:
cargo test --offline --manifest-path /tmp/review-b-native-rust-attacks-20261111-142118/Cargo.toml
RUSTFLAGS=--cap-lints=warn cargo test --offline --manifest-path /tmp/review-b-native-serde-suite-20261111-142118/Cargo.toml

NATIVE_FIX_CONSUMER_ROOT=/tmp/native-css-fix-20261111/consumer-fixture node verify.cjs
LIGHTNINGCSS_FORCE_WASM=1 NATIVE_FIX_CONSUMER_ROOT=/tmp/native-css-fix-20261111/consumer-fixture node verify.cjs
node compare-ir.cjs baseline-compiled-results.bin compiled-results.bin
node parallel-bundle.cjs
LIGHTNINGCSS_FORCE_WASM=1 node parallel-bundle.cjs
node host-routing.cjs
node windows-fixture-key.cjs
LIGHTNINGCSS_FORCE_WASM=1 node windows-fixture-key.cjs
```

최초 harness의 uvu 경로 누락, fixture CWD 누락(78/90), Rust PATH/rustdoc 누락 실패 로그도 보존했다. 환경을 정정한 최종 로그는 `node-native90-final.log`, `node-wasm90-final.log`, `rust-attacks-final.log`, `serde-suite.log`이며 초기 harness 오류를 라이브러리 실패나 성공으로 오인하지 않았다. 전체 serde suite의 기존 Foo/Bar dead-code warnings와 cap-lints 사용도 로그에 명시했다.

주요 evidence: `source-binary-verification.json`, `node-*90-final.log`, `repro-*.log`, `rust-attacks/`, `serde-suite.log`, `actual-consumer-*.log`, synthetic IR binary, `parallel-*.log`, `host-routing.log`, `windows-fixture-key-*.log`, exact Windows CI 원본 log 및 job snapshot.

## Findings

### B-NATIVE-P1-01 — 새 Windows 필수 host CI가 resolver fixture의 경로 키 불일치로 실패한다

- 심각도: **P1**, disposition: **OPEN**
- 위치: **Lightning `node/test/bundle.test.mjs:31`**, `:53`, `:102`; 이를 새 Windows gate로 실행하는 **`.github/workflows/fixed-pack.yml:16`**, `fixtures/nativewind5/test-packed.cjs:38`.
- 관찰: 정확8a head의 [Windows job130579384497](https://github.com/digitie/lightningcss/actions/runs/43037292309/job/130579384497)은 npm ci 성공 후 npm test에서 **88/90**, `resolver`와 `only custom read` 두 시험이 실패했다. log는 `Could not find hello/world.css in foo.css, ... hello/world.css`를 기록한다.
- 원인: Map key는 `hello/world.css` 같은 POSIX 문자열인데 read가 `path.normalize(file)`로 조회한다. Windows에서는 `hello\world.css`가 되어 같은 Map key를 찾지 못한다. 라이브러리 runtime의 Windows 결함으로 단정할 근거는 아니다.
- 독립 재현: 같은 synthetic resolver를 reviewer fixture에서 `path.win32.normalize`로 조회하면 전달 pack의 native/WASM 모두 기대한 조회 실패를 재현한다. fixture의 Map key와 조회를 모두 같은 normalize로 만들면 두 backend 모두 성공한다. 실제 Windows log와 일치하는 시험 이식성 결함이다.
- 영향: 필수 Windows host gate가 항상 실패하고, 뒤의 실제 Expo compiler IR8·최소 재현 단계까지 도달하지 못한다. Linux90 및 속성 모의 routing 성공을 Windows 전체 호환 PASS로 집계할 수 없다.
- 권고: 원본 runtime 변경 없이 시험의 Map key와 조회를 같은 host 규칙으로 맞추고 별도 immutable delta에서 Windows red/green과 후속 compiler IR까지 원 리뷰어가 재확인한다.
- 후속 정보 구분: 사용자가 전달한7e88ee2 수정은 **현재 manifest 밖이며 미검토**다. 이 원문에서 FIXED로 전환하지 않는다.

### B-NATIVE-P2-01 — bundled napi-wasm의 고지는 MIT 식별자만 있고 허가문을 제공하지 않는다

- 심각도: **P2**, disposition: **OPEN**
- 위치: **Lightning `vendor/napi-wasm-NOTICE:3`**, `scripts/build-candidate-wasm.mjs:28`, `:41`; 전달 pack의 `wasm/NAPI-WASM-NOTICE`와 `wasm/wasm-node.cjs`.
- 근거: esbuild가 napi-wasm1.1.3 구현을 self-contained adapter 안에 직접 번들한다. NOTICE는 author·MIT 식별자·source·integrity 및 upstream에 standalone LICENSE가 없다는 사실만 기록한다. 실제 adapter에는 copyright/permission 고지문이 없고, napi-wasm에 해당하는 MIT 전문도 pack에 없다. native-source 안의 serde MIT 전문은 다른 저작권자의 다른 component 고지다.
- 원천 확인: [고정 napi-wasm package.json](https://github.com/devongovett/napi-wasm/blob/bbde4dc54b23d56889e4ca8a23704424df7ae05e/package.json)의 MIT 선언과 author는 직접 조회했다. [MIT 표준문](https://spdx.org/licenses/MIT.html)은 사본에 저작권·허가 고지를 포함하는 조건을 둔다. 현재 NOTICE는 그 허가문을 담지 않는다.
- 재현: 고정 tgz의 파일 목록, `wasm/NAPI-WASM-NOTICE` 전문, `wasm-node.cjs`의 license/copyright/permission 부분을 검사하면 된다. upstream 파일에 없던 고지를 삭제했다는 주장은 하지 않는다.
- 영향: 새로 직접 내장한 JavaScript component에 대한 license evidence가 identifier 수준에서 끝나, 배포 고지 감사를 완결하기 어렵다. 법적 위반이 확정됐다는 P0 판정이 아니라 동봉 고지 보완이 필요한 P2다. serde Apache/MIT 원문 보존은 정상으로 별도 확인했다.
- 권고: upstream의 MIT 선언·권리자 근거를 보존하면서 해당 component의 적용 허가문을 함께 제공하거나 권리자 확인 근거를 마련한다. 추정 저작권 연도·권리자를 만들지 않는다. 변경된 pack은 새 불변 manifest로 검토한다.

### B-NATIVE-P2-02 — release branch의 CI는 고정 pack만 시험하고 현재 Rust source와의 연결을 gate로 검증하지 않는다

- 심각도: **P2**, disposition: **OPEN**
- 위치: **Lightning `.github/workflows/test.yml:6`**, **`.github/workflows/fixed-pack.yml:27`**, `fixtures/nativewind5/test-packed.cjs:26`.
- 근거: 기존 Rust/native/WASM source build 시험의 PR target은 master다. 이번 PR base는 release/1.33.0이므로 이 gate가 실행되지 않는다. 새 fixed-pack workflow는 npm ci 뒤 이미 체크인한 tgz를 시험한다. provenance.revision을 또 다른 고정 manifest 값과 비교하고 내부 해시를 확인하지만, 내장 source를 현재 checkout의 Rust/vendor 내용과 비교하거나 현재 source로 cargo test/build하지 않는다. Rust를 읽는 단계 자체가 없다.
- 실패 시나리오: 같은 branch의 Rust/vendor 수정만 바뀌고 fixture의 고정 tgz/manifest가 남으면 host job은 이전 binary를 계속 시험한다. 새 source의 컴파일·동작 회귀나 source/binary drift가 있어도 동일 host 결과를 낼 수 있다. 현재8a는 production source가684c와 같음을 내가 별도로 증명했으므로 현재 artifact가 잘못된 source라는 finding은 아니다.
- 영향: 새 PR의 녹색 host 결과가 현재 Rust source·추가 test_serde 회귀의 성공을 보증하지 않는다. 이번에는 수동 검증·hash 대조가 이 공백을 보완했지만 자동 감사 연결은 없다.
- 권고: release branch에 source test gate를 연결하고, fixture-only 차이는 허용하되 현재 Rust/Cargo/vendor 파일이 내장 source와 동일한지 확인한다. source 변경 때는 해당 source에서 native/WASM을 재빌드하고 manifest를 함께 갱신하는 gate를 둔다. serde fork의 별도 source CI도 정확 SHA에서 확인한다.
- 후속 정보 구분:18e53fc의 추가 serde 테스트/명시 CI 성공은 사용자 전달 정보이며 **이번 head67fe의 결과로 집계하지 않았다**.

## 원격 CI 최종 관찰과 별도 delta

[Lightning run43037292309](https://github.com/digitie/lightningcss/actions/runs/43037292309)은 정확8a head의 source1 run이다. 초기 queued 상태와 별개로 종료 전 재조회한 결과는 다음과 같다.

| job | 최종 직접 관찰 |
|---|---|
| Ubuntu130579383744 | **success** |
| Windows130579384497 | **failure / 88 of 90**, 후속 IR 미실행 |
| macOS130579384396 | **cancelled**, PASS 아님 |
| codspeed43037292796 | skipped, PASS 수에 포함하지 않음 |

serde67fe는 connector의 PR-triggered run 조회뿐 아니라 `gh api repos/digitie/serde-content/actions/runs?head_sha=67fe4a9c5b4595433a731b70dbe31412721bea8c&per_page=100` 전체 event 조회도 직접 수행해 **total_count0**을 관찰했다. 따라서 해당 head의 원격 source CI 성공을 확인하지 못했다. 이후 별도 head의 CI 결과를 역으로 적용하지 않았다.

사용자 추가 메시지는 아래 **후속 delta 알림**으로만 기록한다.

- 7e88ee204da712049abc1c43b30054b813e2bf24: fixture Map key host-normalize, Windows red/green 및 Linux/IR 재검증을 했다고 전달받음.
- 18e53fcf6f8ace093a292891b34fa3411192617d: serde의 기존 미사용 Foo/Bar를 실제 nested derive roundtrip 시험에 쓰고 cap-lints 제거, source CI 성공을 했다고 전달받음.
- Rust production684c / vendor67fe / Q6DD fix.3 bytes는 변하지 않았다는 전달을 받음.

이 커밋들의 source·CI는 이번 리뷰에서 열어 확인하지 않았다. source1 finding closure는 **OPEN**이고, 새 불변 delta를 받으면 해당 변경과 관련 gate만 독립 재검토할 수 있다. peer의 결과는 계속 비공개로 유지했다.

## 한계·disposition·판정

- Windows fixture P1이 source1에서 재현되고 필수 CI가 실패하므로 **BLOCK**이다. 수정 예정·다른 head 성공은 이 원본 closure가 아니다.
- 두 P2도 현재 OPEN이다. 수정 또는 owner·상세 task·gate·기한을 갖춘 DEFERRED가 필요하며 reviewer가 임의로 연기 승인하지 않는다.
- serde126 직접 재실행은 `--cap-lints=warn` 조건부다. 기존 unused Foo/Bar 두 warning을 숨기지 않았다. 별도 Rust 공격12는 cap-lints 없이 통과했다. 이를 원형 CI 전체 성공으로 확대하지 않는다.
- 현재 Rust source를 사용한 작은 offline serde 시험은 수행했지만 Lightning 전체 native/WASM 재빌드는 **NOT_RUN(저장 공간·대형 build 회피)**이다. source/binary 연결은 deterministic archive·해시·실제 pack 동작·기존 빌드 증거 대조로 확인했다.
- host routing의 OS 속성 모의 성공은 macOS/Windows 실제 실행을 대신하지 않는다. macOS cancelled와 Windows failure를 그대로 남긴다.
- 실제 Pinvi Android/iOS export·EAS·실기기·운영 배포는 **범위 밖 / NOT_RUN**이다. 이 보고서의 compiler IR 성공을 앱 export PASS로 확대하지 않는다.
- NativeCSS manifest/pack/common source2 보고서 원본은 수정하지 않았다. 다른 reviewer 결과는 열람하지 않았다.

**최종 verdict: BLOCK — P1 1건·P2 2건 OPEN.**

종료 시 두 source worktree의 clean 상태를 확인한 뒤 reviewer 소유 worktree·추출본·Rust target·임시 evidence만 정리했다. 기존 모듈/캐시/공유 산출물은 삭제하지 않았다. 보존 evidence와 common source2 원문·manifest·Q6DD pack 해시는 유지했다.
