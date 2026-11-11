# 독립 적대리뷰 A(Mill) — NativeCSS source3 CI metadata 재검토

- Run ID: Mill-A-lightning-final4(NativeCSS postfix3).
- 시작 UTC: 2026-11-11T17:02:46.711942+00:00. 종료 관찰은 observations-end.json. 원문 작성 UTC: 2026-11-11T17:12:50.847491+00:00.
- 같은 원 reviewer A, visitor/숫자/실사용/portable runtime 담당. 구현에 참여하지 않았고 다른 reviewer의 raw report·verdict를 검토하지 않았다.
- **Verdict: PASS — 지정 source/동일 fix4/CI metadata delta에 대한 A 독립 재검토 범위.**
- **원 NativeCSS A-P2-01 FIXED 유지. 신규·잔여 P0 0 / P1 0 / P2 0 / P3 0.**
- Mac green만으로 판정하지 않았다. source 제외 규칙을 독립 공격하고 실제 pack bytes·lineage·Node 동작을 다시 확인했다.
- 이전 NativeCSS source2 PASS 원문과 당시 queued 상태 기록은 보존했다. common4의 새 finding은 별도 범위다.

## 1. Immutable 입력·관찰 SHA·dirty 경계

root는 /home/digitie/dev/common-unification-20261111 이다.
manifest: root/review-manifest-native-css-3.json.
실측 SHA256: d593cc06e3bc9f4562e25c3d019d663d96a7191fa309b620a5c1f993b9a3663f, 전달값과 일치.

| 입력 | 고정 SHA |
|---|---|
| Lightning 이전 → 이번 head | 748651cbd845971e65c411166ddee101745dab21 → 35fc16b023a9cfb75bad7a311f37780c24961724 |
| pack 대응 source | 1e94372a6da4a55eac4a6dc3ff9cdeec103e8ac1 |
| native/raw WASM 실제 compile lineage | 684c528b2d16c581c99cf829f9a4988985488d5f |
| serde 원본 head | 18e53fcf6f8ace093a292891b34fa3411192617d, 이전과 동일 |
| pack | artifacts/native-css-fix4/lightningcss-1.33.0+nativecss.fix.4.tgz |

공유 lightningcss-fix checkout은 head35fc이며 시작부터 scripts/__pycache__/가 untracked였다. 이를 삭제하거나 그 내용을 source로 채택하지 않았다. /tmp/review-A-final4/lightning에 detached immutable worktree를 만들어 시작·종료35fc/clean을 확인했다. serde 공유 checkout은18e/clean이었다.

이전 review-A-native-css-postfix-2.md의 SHA256은95f938b907a4123abf6526581af421e25e1b1fafc8012b5b76ba1ddcd3bd7bb8로 전후 일치했다. 최초 원문·manifest·fix3·fix4를 수정하지 않았다.

## 2. 전체 delta와 제외 분류 감사

748→35fc의 tracked 변경은 정확히4파일이다:

- .github/workflows/fixed-pack.yml: macos-15에서 macos-15-intel로 host matrix 한 항목 변경 및 사유 주석.
- scripts/check-native-css-source.py: CI_METADATA exact3경로 분리, archive/checkout 개별 SHA256 출력.
- scripts/test-native-css-source.py: 허용 exact3경로·인접/다른 build 경로 거부2시험 추가.
- fixtures/nativewind5/README.md: 위 경계와 capacity/host 설명.

Production Rust/Cargo/vendor, loader·adapter·pack/build script, 다른 build workflow에는 변경이 없다. source-delta.patch로 독립 확인했다.

same_source는 기존 fixture prefix 외에 다음 exact3파일만 비교에서 제외한다:

~~~text
.github/workflows/fixed-pack.yml
scripts/check-native-css-source.py
scripts/test-native-css-source.py
~~~

전체 workflow directory나 scripts prefix를 제외하지 않는다. 이 세 파일은 대응 producer1e의 runtime 생성 입력이 아니고, 이번 새 내용은 위 CI/검증기 변경뿐임을 diff로 확인했다. 실제 build script·Rust 입력·adapter input receipt에 대한 검증이 유지된다.

직접 수행한 metadata-adversarial.py는 실제 current287파일과 archived284파일을 불러 baseline을 검사했다. Cargo.toml/Cargo.lock/src/lib.rs/vendor serde, node loader/flags, URL helper, WASM builder, pack script, 별도 build workflow의 변경/추가10개를 거부했다. exact3metadata 변경·부재는 허용하며, suffix/하위 경로처럼 보이는 인접 이름과 fixture-prefix 인접 추가4개는 거부했다.

source gate는 이 제외3파일의 전후 개별 SHA256을 출력하지만 그 출력 자체가 내용을 승인하는 서명은 아니다. 이번35fc의 실제 diff를 독립 검토했기에 허용하는 것이며 후속 verifier/workflow 변경을 자동 승인한 것은 아니다.

## 3. Pack bytes·source/build 연결

actual fix4의 크기15,376,394bytes, SHA256 12c8326428a56e38231f7b5b376df0c6882e3492da794f3499269628edcaccf0, SHA512 SRI를 manifest와 독립 대조하여 일치했다. 이전 본인 private fix4의 pack 일반19파일도 다시 archive와 byte 대조하여 전부 같았다(artifact-check.json).

현재 source gate를 실제 실행하여 다음 연결을 재확인했다:

- pack hash → 동일 provenance → native-source.tar.gz hash 및 git archive1e 전체 bytes.
- archived284파일 ↔ current source의 관련 파일 집합/bytes.
- Rust/Cargo/vendor digest 23cc04bc2587fe044f8e4fdf21690eb8fa7a4ebedbc388a06cb3602aac426c75.
- 같은 digest와 실제 compiled684c의 Rust 입력·lineage.
- native binary·optimized WASM SHA, raw WASM receipt,10 adapter input hash·adapter output hash.
- Cargo.lock hash, napi-wasm 고지와 package declaration의 source/pack 일치.
- source archive의 역사 fixture tgz 재귀 포함 금지.
- 제외3metadata의 archive/checkout hash 차이를 source-gate.log에 명시.

native/Rust/WASM/JS를 새로 전체 빌드하거나 fix4 pack을 재발행한 것이 아니다. 동일 inputs/bytes의 명시적 재사용 검증이다. 이전 A-P2-01의 # 설치경로 수정도 같은 helper/adapter bytes로 남아 있으며 당시 fix3-red/fix4-green 증거를 유지한다.

## 4. 직접 실행과 raw evidence

영구 evidence: root/review-A-native-css-evidence-postfix-3/.

| 검증 | 직접 결과 | evidence |
|---|---|---|
| manifest/pack SHA256·SHA512, 이전 private19파일 | MATCH | artifact-check.json |
| 현재 source gate | PASS, Rust input23cc 동일 | source-gate.log |
| source gate checked-in unit | 6 PASS | source-unit.log |
| 실제 source/archive 기반 제외 규칙 공격 | baseline+10 변경/추가 거부+인접4 거부+exact3 허용 | metadata-adversarial.py / .log |
| 실제 fix4 Node suite Linux 기본 backend | 90 PASS / skip0 | node-native.log |
| 같은 pack forced WASM | 90 PASS / skip0 | node-wasm.log |
| 748→35fc diff --check | PASS | diff-check.log |
| actual source-gate·3host 원격 상태와 Mac 로그 | 직접 API 성공 확인, 아래 정확 ref 구분 | ci-direct-observation.json |

첫 Node driver는 cwd를 저장소가 아닌 위치에 두어 tests/testdata 상대경로가 없어78/90이었다(node-native-first-cwd.log). immutable lightning cwd에서 같은 suite를 재실행하여90/90을 확인했고 WASM도90/90이었다. 이 driver 실패를 제품 finding으로 만들거나 숨기지 않았다.

새 로컬 Rust 전체 build·adapter 재번들·Docker GNU/musl 검증은 NOT_RUN(동일 bytes/입력, 이전 본인 증거 유지). 이번 변경 없는 runtime 검증을 새 compiler build로 과장하지 않는다. 대규모 install·다른 agent cache 삭제 없이 기존 uvu와 본인 private pack을 읽기 참조했다.

## 5. 원격 CI 직접 확인과 정확한 checkout ref

[run43059600512](https://github.com/digitie/lightningcss/actions/runs/43059600512)의 jobs와 source-gate/MacIntel 전체 로그를 GitHub connector로 직접 조회했다. source-gate130658227924, Windows130658228329, macOS Intel130658228472, Ubuntu130658228591 모두 completed SUCCESS였다.

중요한 ref 구분: 이 PR run의 실제 checkout은 head35fc 자체가 아니라 GitHub PR merge ref **0e92f62efea7f190ca19828512e994447b55ad96**이다. 로그가35fc를 base1d680fa에 합친 commit임을 표시한다. GitHub compare로35fc→0e92f62가 ahead1 / files0임을 직접 확인했다. 따라서 지정 head와 파일 내용은 같지만 서로 같은 commit SHA라고 표현하지 않는다.

source-gate 실제 로그는 unit6, Lightning serde2, vendor integration3+28+5+7+22=65, doctest1 성공과 Rust input23cc를 보인다. 경고 완화 flags 없이 지정 checkout의 시험을 실행하는 workflow를 확인했다.

MacIntel 실제 로그는 auto 모드 Node90/skip0, 합성 full IR8 deepStrictEqual/5 app classes, visitor 및 forced WASM 물리 특수경로4 성공을 보인다. Mac에서 forced 모드 Node90을 별도로 두 번 실행한 것으로 세지 않는다. macOS의 정상 fallback은 bundled WASM이다. Linux GNU native를 macOS native binary로 해석하지 않는다. 다른 두 host의 SUCCESS는 직접 jobs API로 확인했으며 이 원문이 모든 host의 전체 로그를 재분석했다는 뜻은 아니다.

구748의 macOS ARM 두 시도는 manifest상 runner_id0의 실행 전 CANCELLED다. 이를 PASS로 세지 않는다. 새 Intel 실행 성공은 ARM 실기기/runner 성공의 증거가 아니다. 과거 NativeCSS2의 queued 기록을 덮어쓰지 않는다.

manifest에 내포된 구 verification.pending은 fix4 작성 당시 상태다. 이번 head35fc CI jobs의 직접 관찰 결과와 구분했다. serde18e의 merge21d tree 일치는 전달 manifest의 별도 근거이며 이번에 serde full127을 새로 빌드하지 않았다.

## 6. 원 finding·신규 finding·판정 경계

- NativeCSS A-P2-01: **FIXED 유지.** 이전 원 reviewer의 fix3-red/fix4 물리 특수경로4-green, 동일 pack/19파일 bytes·helper/adapter 입력 확인, 새 source gate/Node90각 재검증이 근거다. 이번에 특수경로4를 로컬에서 새로 전부 복사 실행했다고 주장하지 않는다.
- 신규/잔여 A finding: P0=0/P1=0/P2=0/P3=0.
- CI metadata3제외가 임의 production 변경을 허용하는 회귀는 이번 head에서 발견하지 못했다. Mac 성공만으로 내린 판정이 아니다.
- **PASS는 지정 source/동일 fix4/위 CI metadata delta 범위다.** COMMON4·consumer 최종 CSS fork·실제 앱 export·ARM host·이미지 배포·출시 수용은 별도 gate이며 대신 PASS하지 않는다.

구현 source·pack·이전 raw를 수정하지 않았고 검사 전후 SHA/clean/원문 보존을 observations-start/end.json에 남겼다. 새 원문만 별도로 저장한다.
