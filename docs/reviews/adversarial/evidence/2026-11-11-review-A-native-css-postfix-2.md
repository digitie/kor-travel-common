# NativeCSS 동일 원 reviewer A(Mill) — 수정 후 2차

- Run ID: `Mill-A-native-css-postfix-2-748651c-18e53fc`.
- 시작 UTC: `2026-11-11T15:19:59Z`.
- 종료 UTC: `2026-11-11T15:31:30.727899+00:00`.
- 상태: `COMPLETE`.
- **Reviewer verdict: `PASS` — 라이브러리 소스·pack 및 A finding 재검토 범위 한정.**
- **원 A-P2-01: `FIXED`**, 원 reviewer A가 직접 새 pack으로 red/green 재확인했다.
- **신규 finding: P0 0 / P1 0 / P2 0 / P3 0.** A의 잔여 OPEN0.
- **플랫폼/merge gate는 별도:** 부모가 전달한 exact748 CI의 source-gate·Ubuntu·Windows 성공을 기록했고 macOS는 아직 queued로 전달되었다. 모든 host/CI·채택·앱 export·배포가 완료되었다는 판정이 아니다.
- 다른 reviewer 원문/결과는 열람하지 않았고, 다른 reviewer finding을 대신 closure하지 않았다. 구현에 참여하지 않았으며 코드를 수정하지 않았다.

## 1. Immutable 기준선과 원본 보존

manifest: `/home/digitie/dev/common-unification-20261111/review-manifest-native-css-2.json`.

실제 SHA256: `1215c43638009758821f3ec29bdce037513e5c01f6aa76d3839820802ef5428c`(전달값과 동일).

| 대상 | 이전 원 review | 이번 고정/실제 관찰 SHA |
|---|---|---|
| LightningCSS | `8a03050a00a30932fe49d2ca98f5f324a7f938a3` | `748651cbd845971e65c411166ddee101745dab21` |
| pack 대응 source | `684c528b2d16c581c99cf829f9a4988985488d5f` | `1e94372a6da4a55eac4a6dc3ff9cdeec103e8ac1` |
| serde fork | `67fe4a9c5b4595433a731b70dbe31412721bea8c` | `18e53fcf6f8ace093a292891b34fa3411192617d` |

구현 checkout 두 곳의 시작/종료 HEAD는 위 manifest와 같고 porcelain은 비어 있었다. LightningCSS는 `/tmp/review-A-nativecss-2/lightning-source` detached worktree에서 검사/시험했고 종료에도 clean이다. serde는18e53fc git archive snapshot을 사용하고35파일 모두 종료에 object와 byte 대조했다. 현재 구현 tree나 common 정책 branch의 진행 중 delta를 섞지 않았다.

최초 `review-A-native-css-1.md` SHA256은 시작·종료 모두 `3b6e63edf13661700a71ed823ab05dbafd531083c960f31317ce1059ec626028`이다. 최초 원문·manifest1·fix.3을 수정하지 않았다. common source2/Dialog·소비자 변경도 본 범위에 포함하지 않았다.

## 2. 실제 fix.4 pack과 source/build 연결

사용 파일은 **`artifacts/native-css-fix4/lightningcss-1.33.0+nativecss.fix.4.tgz`**다.

- 15,376,394 bytes, SHA256 `12c8326428a56e38231f7b5b376df0c6882e3492da794f3499269628edcaccf0`.
- SRI `sha512-zDQ03VJE37OlyBrLsRcsEdIVu0T4BXJKDH5y9//To6GlGN2UrKQGERFVAFblkPQ5ZEbhuOp5wpXxGARZNdbQLA==`.
- provenance 전체는 manifest와 동일하다.
- native binary `8a38620c1bbf54acfb12f40b3180ce4e8510a5fb952e9173a3b7fe0b676ecbd6`, optimized WASM `4c2a5251dac4f47ebdadce39579febee5e12e00a3c892e5719e2a46ffa535a27`은 fix.3과 동일하다.
- 새 adapter `9aacec17ea517e31eaf39cecb60eada7cfa637ec3f4629c04ff0af9e63148d90`과 source archive `e36a53d7dac040b249399c73d7079d4c9d2769d221746891294e06c46ed14f89`는 새 bytes다.
- embedded source archive를 `git archive --format=tar.gz 1e94372...`와 **gzip 전체 byte 동일**로 확인했다. 일반 source284파일이며 역사 tgz member0이다.
- 현 checkout→archive→기존 compiled684c의 Rust/Cargo/vendor 입력 digest `23cc04bc2587fe044f8e4fdf21690eb8fa7a4ebedbc388a06cb3602aac426c75`가 같은 것을 source gate 직접 실행으로 확인했다.
- ADAPTER-BUILD.json과 provenance adapterBuild가 동일하고10개 입력 source hash·실제 adapter hash·WASM hash를 직접 대조했다. raw WASM 실제 cached file의 SHA256도 `d392deef78bf3cd0026c9e05fab68d3b185a561e89240e5e875f5c6a82f8d443`으로 확인했다.

**독립 JS adapter 재번들도 수행했다.** 기존 Binaryen132/esbuild0.28.2/napi-wasm1.1.3을 읽기 참조하고, 현 고정 build script와 raw WASM으로 자기 디렉터리에 재생성했다.10개 입력 hash, upstream napi input hash, tool version, raw/optimized WASM hash가 pack receipt와 같고 optimized WASM은 byte 동일했다. esbuild의 source 경로 주석이 달라 재생성 JS 전체 byte/hash까지 같지는 않다. 두 JS를 동일 esbuild parser로 주석 제거/공백 정규화한 결과는 완전히 동일했으며 SHA256은 `a0749d8ad6dbd02853ed2b2e944c64d1b76cfd8afa80d66e33bd4c1f6796318e`였다. 이를 byte-for-byte reproducible JS build라고 과장하지 않는다.

Rust/native/raw WASM 자체를 이번에 새로 전부 빌드한 것은 아니다. **동일 입력 digest에 따른 명시적 재사용**과 새 JS adapter build를 구분한다.

## 3. 직접 실행과 raw evidence

evidence: `/home/digitie/dev/common-unification-20261111/review-A-native-css-evidence-postfix-2/`.

실행 명령은 `commands.txt`, 각 script/receipt/log에 기록했다. PowerShell workdir은 `C:\`, WSL에서 실행했다. npm install/image pull/타인 cache 삭제는 하지 않았다. Rust/adapter 출력은 자기 `/tmp/review-A-nativecss-2`에 격리했다.

| 직접 실행 | 결과 | Raw evidence |
|---|---|---|
| 새 source gate 현재 checkout/archive/lineage 감사 | PASS, source284·Rust input digest 일치 | `source-gate.log` |
| 변경/추가/삭제/fixture 예외·Rust fingerprint 부정 시험 |4 PASS | `source-negative.log` |
| 실제 fix.4 물리 복사 특수경로 | 공백/#/%/복합4 PASS | `special-paths.log`, `test-special-paths.cjs` |
| 실제 fix.3의 물리 # 경로 음성 대조 | require 실패 exit1(원 버그 유지) | `special-path-fix3-red.log` |
| fix.4 Node upstream suite native/WASM | 각각90 PASS / skip0 | `node-native.log`, `node-wasm.log` |
| serde18e full suite+doctest | **127 PASS /0 FAIL /0 IGNORE**, RUSTFLAGS/cap-lints 없음 | `serde-full-no-cap.log` |
| 현 LightningCSS test_serde.rs 새 test harness compile/link+실행 |2 PASS | `lightning-exact-rust-compile.log`, `lightning-exact-rust-tests.log` |
| 현 vendored serde integration 지정5 suite |65 PASS | `vendor-integration.log` |
| 현 vendored serde doctest |1 PASS | `vendor-doctest.log` |
| 현 source JS adapter 재번들 및 입력·출력 대조 | PASS(위 byte/정규화 경계 참조) | `adapter-rebuild.log`, `adapter-rebuild-receipt.json`, `adapter-normalized-match.log` |
| 실제 RC compiler 합성 CSS full IR8 | native/WASM 각각1.30.1 기준 deepStrictEqual,5클래스 | `ir-native.log`, `ir-wasm.log` |
| var/env/large number/Infinity/property 최소 visitor repro | native/WASM 각각10 PASS | `repro-native.log`, `repro-wasm.log` |
| 기존 pinned Bookworm native·강제WASM | 둘 다 PASS, Node22.23.1/glibc2.36 | `bookworm-native.log`, `bookworm-wasm.log` |
| 기존 Alpine 자동WASM | PASS, Node22.23.1/glibc 없음 | `alpine-auto.log` |
| LightningCSS post-fix delta diff-check | PASS | tool 관찰, clean 종료값 `observations-end.json` |

현재 LightningCSS test_serde **시험 파일 자체를 새로 compile/link**했지만, library/dependency rlib는 기존 build cache를 읽기 참조했다. 이 rlib를 포함한 Rust runtime 전체를 새로 빌드했다고 주장하지 않는다. 현 checked-in Rust 입력과 reused lineage의 동일성은 source gate로 따로 확인했다. 부모의 exact source-gate CI 성공 관찰은 아래 별도 출처로 기록한다.

vendored integration65+doctest1을 vendor의 full unit126 성공이라고 바꾸어 표현하지 않았다. 별도 fork18e의 full suite는 신규 nested derive testcase가 추가되어61+3+28+5+7+22+1=127개다. 이 full suite는 offline/locked 자기 output으로 이번에 직접 빌드했고 경고 완화가 없다.

compiler 검증은 react-native-css와 @expo/metro-config 원본의 별도 copy, 나머지 기존 의존성 읽기 symlink, private fix.4를 정상 Node resolution으로 연결한 작은 consumer에서 실행했다. 공식 loader가 실제 private fix.4 transform을 선택하는 identity assert가 통과했다. process module resolver monkeypatch는 사용하지 않았다. fresh npm ci 또는 실제 앱 설치/Expo export 성공을 증명한 것은 아니다.

Docker도 기존 image만 `--pull=never --network none --read-only`와 private package readonly bind로 실행했다. live 서비스/네트워크/운영 데이터는 건드리지 않았다.

## 4. 최초 A finding 원 reviewer closure

### A-P2-01 — FIXED

- 최초 원문: `review-A-native-css-1.md`의 # 설치경로 portable WASM 초기화 실패.
- 수정 위치: `wasm/import.meta.url-polyfill.js:5`의 `pathToFileURL(__filename).href`; 새 build script/adapter input receipt와 실제 fix.4 JS에 반영됨.
- 본인 재확인: symlink가 아닌 실제 물리 package copy 네 경로에서 forced WASM package require와 identity visitor가 통과했다. 같은 # 형태의 fix.3은 모듈 로드 단계에서 ENOENT로 실패했다.
- 대응 pack: 새 version4, SHA256 `12c832...accf0`, SRI zDQ03...를 실제 계산해 고정했다. old fix.3/Q6DD hash를 재사용한 것이 아니다.
- **Disposition: FIXED(원 reviewer A 직접 확인).** 이 NativeCSS 범위의 A 잔여 P1/P2는 없다.

## 5. 전체 delta와 추가 coverage 검토

- **Windows resolver fixture:** 두 inMemoryFs의 key도 조회부와 동일하게 path.normalize하도록 바뀐 것을 확인했다. library public runtime 변경으로 포장하지 않았다. current Node90 native/WASM을 직접 실행했고 Windows actual90 결과는 부모의 exact CI 관찰로 구분했다.
- **serde fixture 경고:** Foo/Bar를 ignore하거나 cap-lints로 숨기는 대신, derive된 nested Value를 실제 serialize→deserialize하여 비교하는 testcase가 추가됐다.18e full127을 완화 flag 없이 직접 통과시켰다. production source/기존 visitor 숫자 수정은 변하지 않았다.
- **source gate/CI:** 현재 source file set/bytes, Rust fingerprint, compiled revision의 Rust 입력, native·WASM digest, adapter input/output receipt를 연결하는 code를 읽고 실제 gate/부정4시험을 실행했다. source-gate job이 exact checkout에서 test_serde2와 vendor integration65/doc1을 실행하며 실패 허용/cap-lints를 사용하지 않는 것을 확인했다. self-declared receipt 대조만으로 신규 native build를 주장하지 않는다.
- **고지:** napi-wasm1.1.3의 고정 package.json author/license 선언과 MIT 허가·조건·면책 전문이 vendor/archive/pack에 반영된 것을 확인했다. upstream에 없는 권리자 연도를 새로 가정한 수정은 없다. 다른 reviewer의 finding disposition을 대신 확정한 것은 아니다.
- **archive 재귀:** .gitattributes에서 fixtures/nativewind5/vendor/*.tgz를 export-ignore하여 기존·신규 fixture binary를 corresponding source archive에 반복 포함시키지 않는다. 실제 archive284파일에 .tgz0을 확인했고 current source gate도 통과했다.
- **runtime 회귀:** helper URL 변경 외 production Rust/native/optimized WASM은 동일한 입력/bytes로 재사용된다. 그럼에도 실제 새 pack의 Node90·IR8·minimal visitor·GNU/musl backend를 다시 검증했다. 숫자 coercion을 모든 큰 정수의 무손실 변환으로 재해석하지 않는다.

추가 source/pack/runtime 회귀 finding은 발견하지 않았다. A의 원 finding 이외의 reviewer 지적은 제출된 구현 범위로만 살폈고 그 reviewer의 closure 권한을 행사하지 않았다.

## 6. CI 상태의 출처와 미완 경계

아래는 **부모가 본 대화에서 exact API 관찰로 전달한 값**이다. 본 reviewer가 원격 API를 새로 조회했다고 주장하지 않는다. `parent-ci-observation.json`에 출처를 보존했다.

| repository / exact commit | run/job | 부모 전달 상태 |
|---|---|---|
| LightningCSS748651c | run43047084671 / source-gate130613789086 | SUCCESS |
| 같은748651c | Ubuntu130613790164 | SUCCESS |
| 같은748651c | Windows130613790166 | SUCCESS |
| 같은748651c | macOS130613789629 | **queued** |
| serde18e53fc | 기존 CI+명시 Rust CI | 부모가 앞서 SUCCESS 직접 관찰하여 전달 |

구 fix.3/구 head7e88의 CI와 이번748 CI를 섞지 않았다. macOS가 끝났거나 모든 플랫폼 matrix가 PASS라고 표기하지 않는다. 이 source review PASS가 pending host CI를 대신 통과시키지 않는다.

common 정책 branch·Dialog 모바일 scroll·모든 소비자 채택·최종 Pinvi export·EAS·실기기·배포는 **NOT_RUN(별도 scope/후속 gate)**다. 이번 합성5클래스/IR8을 실제 Pinvi113클래스의 새 export 증거로 확대하지 않았다. 최초113클래스 검증은 이전 원문/pack의 역사 증거로 남는다.

## 7. 최종 판정과 보존

- **PASS: 본 고정 source/pack에 대한 A 독립 재검토와 A-P2-01 closure.**
- A 잔여/new finding: P0=0, P1=0, P2=0, P3=0.
- **모든 host/merge/release gate 완료 판정은 아님:** macOS actual CI는 위 전달상 queued이고 그 완료 확인이 별도로 필요하다. peer reviewer의 disposition도 본인이 소유한다.
- 새 원문: `/home/digitie/dev/common-unification-20261111/review-A-native-css-postfix-2.md`.
- evidence: `/home/digitie/dev/common-unification-20261111/review-A-native-css-evidence-postfix-2/`.
- 시작/종료 SHA·clean·원본 보존: `observations-start.json`, `observations-end.json`.
- code/pack/기존 원문은 수정하지 않았다. 자기 immutable snapshot·소규모 시험/재번들 출력과 report/evidence만 만들었고 타인 cache는 삭제하지 않았다.
