# NativeCSS3 원 리뷰어 B 수정 후 재검토 원문

- reviewer: **B / Epicurus**, 구현 비참여. package 실제 사용 경로/Cargo vendor/고지/source↔binary↔CI 연결 담당.
- runid: `Epicurus-B-native3-20261111T170200Z`
- UTC: 시작 `2026-11-11T17:02:00Z`, 종료 `2026-11-11T17:16:06.541031+00:00`.
- manifest: `review-manifest-native-css-3.json`, 실제 SHA256 `d593cc06e3bc9f4562e25c3d019d663d96a7191fa309b620a5c1f993b9a3663f` — 요청과 일치.
- **verdict: PASS — 이번 NativeCSS3 원본·동일 fix4 pack·source/host CI 범위.**
- 이전 source PASS/3건 FIXED 유지. **이전 Mac 조건은 새 입력에서 CLOSED. 신규 P0/P1/P2/P3 없음.**
- **CI-only 분류는 현재 정확한 delta에 대해 ACCEPTABLE.** 아래 세 metadata 파일로 한정한 예외는 producer/runtime byte 검사를 대체하지 않는다. 이 판단을 미래의 임의 workflow/검증기 변경에 대한 자동 승인으로 확대하지 않는다.

## 불변 입력과 실제 관찰

| 항목 | 관찰 SHA/값 |
|---|---|
| Lightning head | `35fc16b023a9cfb75bad7a311f37780c24961724` |
| 이전 head | `748651cbd845971e65c411166ddee101745dab21` |
| original base | `1d680fa14e9a089c92dc0929f869d6757ae91c30` |
| pack source archive revision | `1e94372a6da4a55eac4a6dc3ff9cdeec103e8ac1` |
| 실제 compiled native/raw WASM revision | `684c528b2d16c581c99cf829f9a4988985488d5f` |
| serde head | `18e53fcf6f8ace093a292891b34fa3411192617d` — 불변 |
| serde merge | `21d1c7d3f184e362e0a90905939962d43824e0dd` — 위 head와 실제 tree 동일 |
| reviewer worktree | `/tmp/review-b-native3-20261111-170200`, detached35fc16b |
| fix4 실제 SHA256 | `12c8326428a56e38231f7b5b376df0c6882e3492da794f3499269628edcaccf0` |
| fix4 실제 SHA512 | `sha512-zDQ03VJE37OlyBrLsRcsEdIVu0T4BXJKDH5y9//To6GlGN2UrKQGERFVAFblkPQ5ZEbhuOp5wpXxGARZNdbQLA==` |
| CI 연결 PR head | `35fc16b023a9cfb75bad7a311f37780c24961724` |
| CI **실제 checkout HEAD** | `0e92f62efea7f190ca19828512e994447b55ad96` — PR 합성 merge |

기존 보고서·manifest·fix4 bytes를 수정하지 않았다. A 원문/결론을 사용하지 않았다. Git object/diff와 자체 격리 worktree만 source 기준으로 사용했다. 기존 node_modules/타인의 캐시를 지우지 않았고 신규 install/Rust rebuild를 하지 않았다. 자체 최소 추출물에서 실제 native/WASM 동작을 확인했다. 최종 worktree는 해당 SHA이며 porcelain이 비었다. 증거는 `review-B-native-css-postfix-3-evidence/`에 보존한다.

## CI-only 분류의 독립 판단

748→35 diff는 정확히4개 파일이다.

1. `.github/workflows/fixed-pack.yml`: macos-15를 macos-15-intel로 바꾼 matrix와 이유 주석. check/source/Rust/host 실행 단계의 삭제·완화 없음.
2. `scripts/check-native-css-source.py`: exact3-file CI_METADATA 집합, source byte 비교에서 그 집합만 추가 제외, 각 변경 전후 digest 출력.
3. `scripts/test-native-css-source.py`: exactmetadata 허용 및 이웃 경로/빌드 workflow 거부의 새2개 unit method.
4. `fixtures/nativewind5/README.md`: 호스트 공급·metadata 구분 설명. 기존 fixture 제외 범위 내부다.

`check-native-css-source.py:33`의 세 exact path는 host 검증 workflow·검증기·검증기 unit이며 실제 compiler/loader/adapter/package를 생성하는 입력이 아니다. 현재 diff에 producer 입력 변경이 전혀 없다는 것을 Git과 payload 비교로 확인했기 때문에 이 분류를 수용한다. 대응 source archive를 새 CI 호스트 설정만으로 다시 포장해 같은 버전의 다른 runtime bytes를 만들 필요가 없다.

이것은 검증기의 자기 무결성을 archive 하나가 자동 증명한다는 뜻이 아니다. 세 파일은 byte 동일성 검사의 예외이므로 **이번 리뷰에서 변경 자체를 직접 검사**했다. 집합은 wildcard/전체 workflow/전체 scripts 예외가 아니며, 각 이전·현재 SHA가 출력된다. 출력이 명시하는 차이 자체를 숨기지 않는다.

실제 gate 출력과 B 재계산:

| exact metadata | archive SHA256 | checkout SHA256 |
|---|---|---|
| `.github/workflows/fixed-pack.yml` | `e162db2e92a69fa90bd4a114bad2ec60d9d29616ca4c5e50511745eff4f3b71c` | `961488977e8b798298c3d968aa8ac57fa58a35acd24500aa61d5def3e8979aac` |
| `scripts/check-native-css-source.py` | `da6714109a585e5756b5e460d2585c3b709a63cd6241e8dd5d72b73dca3b2992` | `1a26ff826bfea1d27b2a31467f48c0aa6c8bbd03eb18fdb050b2113c9fb37bb3` |
| `scripts/test-native-css-source.py` | `5be0910fd655abaa80e86fa82be11f9c63216db6544938ff4526ea8adcd13bde` | `de77aa1d7c37f884be3805a19bf390cdcf98b58ceaaf74505f2e9a70e7529821` |

`same_source`의 file-set 비교와 나머지 파일의 byte 비교는 유지된다. Rust/Cargo/vendor 전체 digest와 compiled684 lineage, 현재 loader/adapter inputs, receipt/출력, native/WASM hashes, Cargo.lock, MIT 고지/고정 package.json 검사도 유지된다. 다른 build workflow나 pack script를 수정하면 archive와 다르므로 실패한다.

## 독립 실행·공격과 pack 연결

| 검증 | 실제 B 결과 | 증거 |
|---|---|---|
| source-gate unit | **6 PASS** | native-source-unit6.log |
| actual source-gate | **PASS**, 대응 source284파일, Rust digest 일치 | native-source-gate.log |
| 독립 보호 경로 변조 | **12개 모두 REJECTED** | native-independent-audit.json |
| exactmetadata 변조 대조 | **세 파일만 ALLOWED_METADATA_ONLY** | 같은 JSON |
| fix4 TGZ repo fixture vs artifact directory | bytes 전체 동일, SHA256/SHA512 일치 | 같은 JSON |
| 실제 Linux x64 auto backend | **native**, 순수 visitor10 성공 | native-minimal-probe.log |
| 실제 Linux x64 강제 backend | **wasm**, 순수 visitor10 성공 | 같은 로그 |
| serde merge tree | reviewed18e == merged21d | unchanged-foundation-merges.json |

변조 공격은 파일에 쓰지 않고 actual current/archived byte map을 복사해 수행했다. 대상: Cargo.lock, Cargo.toml, src/lib.rs, vendor/serde-content/src/de/mod.rs, node/index.js, wasm/wasm-node.mjs, wasm/import.meta.url-polyfill.js, scripts/pack-native-candidate.mjs, scripts/build-candidate-wasm.mjs, 다른 `.github/workflows/build.yml`, 그리고 허용 경로 뒤에 `.extra`를 붙인 두 이웃 경로다. 실제 존재하지 않는 보호 경로의 추가도 file-set drift로 거부된다. 구현의 exact-set 분류와 broad-prefix 분류를 구분했다.

로컬 unit6은 새 exactmetadata 허용/다른 build workflow와 이웃 이름 거부뿐 아니라 기존 fixture 허용, Rust/adapter/build script 변경 거부, 추가·삭제 거부, Rust fingerprint 변조를 검증한다. CI source-gate step도 이6개 시험을 실제 호출한 뒤 actual gate를 실행하는 것을 source와 원격 로그 양쪽에서 확인했다.

Rust input digest는 `23cc04bc2587fe044f8e4fdf21690eb8fa7a4ebedbc388a06cb3602aac426c75` 그대로다. native `8a38620c1bbf54acfb12f40b3180ce4e8510a5fb952e9173a3b7fe0b676ecbd6`, WASM `4c2a5251dac4f47ebdadce39579febee5e12e00a3c892e5719e2a46ffa535a27`, adapter `9aacec17ea517e31eaf39cecb60eada7cfa637ec3f4629c04ff0af9e63148d90`도 실제 payload 재계산과 일치한다. source archive는 declared1e의 `git archive` bytes와 같다. Rust/native/raw WASM을35에서 새로 빌드했다는 주장을 하지 않는다.

최소 실제 probe는 동일 fix4 pack에서 source archive만 제외하고 자체 임시 디렉터리에 필요한 runtime 파일을 추출했다. var(), 큰 radius, calc(infinity), env(), @property 다섯 입력에 Rule/StyleSheetExit 왕복10개를 각 backend에서 실행했다. 이 probe는 Node90 전체나 실제 앱 export가 아니다. 기존 numeric overflow/precision·Some(())/opt-in semantics는 변경 없는 production bytes와 이전 원검토 결과를 유지하며 이번 변경에 새 Rust 회귀 위험을 덧붙여 주장하지 않는다.

## 정확한 CI 연결 및 Mac 조건 closure

[run43059600512](https://github.com/digitie/lightningcss/actions/runs/43059600512)의 직접 API 결과:

| job | ID | 상태 |
|---|---|---|
| source-gate |130658227924|**SUCCESS**|
| packed-hosts windows-2025 |130658228329|**SUCCESS**|
| packed-hosts macos-15-intel |130658228472|**SUCCESS**|
| packed-hosts ubuntu-24.04 |130658228591|**SUCCESS**|

Mac 및 source-gate 로그를 직접 읽었다. Mac은 실제 `darwin x64 auto`, Node90 PASS/skip0, 특수 실제 경로4, synthetic IR8/5classes deepStrictEqual, pure visitor10을 통과했다. hash/space/%/복합 경로의 실제 복사 require가 실행됐다. GNU addon을 Mac native로 실행했다고 표현하지 않는다. 현재 loader의 Mac 경로는 bundled WASM이다. source-gate는 unit6, source284/Rust digest, 정확 checkout의 Lightning serde2, vendored integration65(3+28+5+7+22), doctest1 성공을 기록한다. 전체 upstream Rust unit suite라고 확대하지 않는다.

**checkout 구분:** 이 run은35 PR head에 연결되지만 actions/checkout 기본 PR 동작으로 `refs/remotes/pull/1/merge`를 checkout했다. 로그의 실제 HEAD는 `0e92f62efea7f190ca19828512e994447b55ad96`, 메시지는35를 base1d680에 합성한 merge다. B가 GitHub compare API로35→0e92를 조회해 merge_base=35, ahead1/behind0, files=[], too_large=null을 확인했다. 따라서 관련 source/fixture/workflow 내용은 manifest35와 동일하며 이 host/source CI를 이번 입력의 유효 증거로 수용한다. **HEAD 자체가35였다고 잘못 기록하지 않는다.** 비교/checkout 발췌는 native-ci-merge-tree-equivalence.json에 보존했다.

별도 codspeed43059600428은 **SKIPPED**이며 PASS로 집계하지 않는다. fork의 기능/source/host gate와 별개의 성능 서비스다.

이전 원문의 조건은748 macOS job이 queued였다는 당시 사실이었다. 이후 ARM64 두 시도의 미실행 CANCELLED·runner_id0·공급 부족 annotation은 부모가 인계한 인프라 이력이며, 이번에 그것을 성공으로 바꿔 기록하지 않는다. 새35 입력은 Mac Intel 실제 실행을 제공하고 B가 이를 직접 확인했으므로 **새 입력의 Mac host 조건을 닫는다**. Mac ARM64 실기/runner 성공이나 모든 macOS 아키텍처 수용을 뜻하지 않는다.

## 기존 finding disposition과 한계

| 기존 ID/조건 | 이번 상태 | 근거 |
|---|---|---|
| B-NATIVE-P1-01 Windows fixture path | **FIXED 유지** | 변경 없는 testMap normalize와 새 Windows job 성공. |
| B-NATIVE-P2-01 napi-wasm 고지 | **FIXED 유지** | pack bytes 불변, source-gate가 notice 전문·고정 package.json의 source/pack 동일성을 재검증한다. |
| B-NATIVE-P2-02 source/CI 연결 | **FIXED 유지** | 현재 classification 직접 심사, local6+actualgate+독립 변조15, source CI 성공. |
| postfix2 Mac queued 조건 | **CLOSED@Native3** | 같은 pack의 새 Mac Intel 실제 Node/IR/특수 경로 성공과 merge/source 동일성 직접 확인. 이전748 성공으로 소급하지 않음. |

새 Pn finding은 없다. 위 CI-only 분류는 정확3개 metadata에 한정하고 현재 pack/provenance/source 동등성이 유지된다는 조건에서 적합하다. producer/Cargo/vendor/loader/adapter/build script나 binary가 바뀌면 이 승인과 무관하게 새 immutable 입력·artifact 계보 검증이 필요하다.

## 주요 명령과 원문 보존

PowerShell workdir `C:\`에서 `wsl.exe -e bash -lc`로 실행했다.

```bash
sha256sum review-manifest-native-css-3.json
git worktree add --detach /tmp/review-b-native3-20261111-170200 35fc16b023a9cfb75bad7a311f37780c24961724
git diff 748651cbd845971e65c411166ddee101745dab21 HEAD
python3 -B scripts/test-native-css-source.py
python3 -B scripts/check-native-css-source.py
python3 -B <evidence>/audit-native.py
node <evidence>/native-minimal-probe.cjs
LIGHTNINGCSS_FORCE_WASM=1 node <evidence>/native-minimal-probe.cjs
git status --porcelain=v1
```

API: commit_workflow_runs(35), workflow_run_jobs(43059600512), workflow_job_logs(130658228472/130658227924), compare_commits(base35, head0e92). 원격 rerun/수정/댓글/merge를 실행하지 않았다. 원 postfix2 SHA256 `ef761c04ebc2a9610d2b8a5b6dc701fab4230caa7ce17c6371264290d21f0ae4`와 원source1 SHA256 `e077602b2bfec00c6d498112bc69c4918eded2227137db15b264634ed7bd16fe`는 불변이다. 자체 temp만 정리한다.

**최종 PASS는 두 fork의 이번 source/고정 pack/호스트 CI 승인이다.** common4 판단은 별도 원문이며 최종 소비자 review, 앱 export, 기기 실측, 새 배포·릴리스는 이번 범위에서 NOT_RUN이다. 신규 install/Rust 재빌드는 하지 않았다. 별도 serde merge는 reviewed tree 동일성까지만 독립 확인했으며 merge 후 새 테스트를 했다고 표현하지 않는다.
