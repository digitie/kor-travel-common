# Common build rules 입력2 — 원 B 독립 재검토

- 실행 ID: `B-COMMON-E1D0-20261113-02`; 원 reviewer B/Epicurus, 구현 비참여.
- 시작 UTC `2026-11-12T17:20:19.489580+00:00` / 원문 고정 UTC `2026-11-12T17:31:06.672511+00:00`.
- 불변 manifest: `validation/review-common-build-rules-e1d0-20261113/manifest.json`.
- 관찰 SHA256 `5b391bc0200766c2cb9ed68fb4940924ccdd2f545b729aa9455e857d8af944f8` 일치.
- source `e1d0f01ef05b913e5f311a4d3ae2922a25a676c3`; tree `aea8c2ad8a7b6ffc6550d7a576c01d50551b8bb1`.
- base `678a5bcf0150ac0386bfa86106e7e0f4f77e8639`; 직전 BLOCK `c4cc78781638808490c0ea540fbb38200b577346`.
- 21개 manifest 경로의 Git blob ID/SHA256/bytes를 직접 검산했다. c4cc 이후 제품 helper/tests와 versions 규약/journal/resume의 정확 5경로 delta만 새 심층 범위다. 이동 중 checkout/index/branch는 기준선으로 사용하거나 변경하지 않았다. 상대 현재 원문/판정 열람 0.
- 기존 원문 `validation/review-B-common-build-rules-c4cc-1.md` SHA256 `1b4cb2d6be65b7c07e5554b5a67bd6ae8a7926edf2943ef3aee7cf3c0abd16f5` 보존·일치 확인.

## 판정

**BLOCK.** 기존 3건 중 **FIXED 2 / OPEN 1**. 신규 **P2 2건**, 신규 P0/P1 0건이다. 기존 force 지적은 단순 원 반례가 거부되지만 유효 force=true의 다른 표기를 여전히 승인하여 닫지 못한다. 부모가 원 세 지적 모두 수정을 필수로 수용하고 defer하지 않기로 했으므로, 이 OPEN을 임의 면제하지 않는다. 신규 P2는 아래와 같이 구체적으로 처분해야 한다. CI 성공과는 별개인 소스 판정이다.

| 기존 ID | 이번 disposition | 직접 근거 |
|---|---|---|
| B-BUILD-P1-01 | **FIXED** | 원 `--engine-strict --no-engine-strict`, `--engine-strict --engine-strict=false` 둘 다 실패. 분리 false·중복 해제도 실패. 정상 strict/등호 true/분리 true는 성공. shell·JSON 음성 대조는 제공 62개에서도 유지됨 |
| B-BUILD-P2-01 | **OPEN — 단순 원 반례만 수정됨** | `force=true`/bare force/따옴표 true 값은 거부하고 마지막 force=false는 수용. 그러나 따옴표 **key** 또는 section으로 유효 force=true를 숨기면 성공. 아래 자체 반례 참조 |
| B-BUILD-P2-02 | **FIXED — 원 무검사 entry 문제** | 같은 잘못된 anchor와 명시 `--registry`에서 직접/alias/`--preserve-symlinks-main` 세 호출 모두 engine-strict 오류 exit1. import-only는 함수만 노출하고 자동 CLI 없이 exit0. 기본 registry의 별도 문제는 신규 P2-04로 분리 |

## 기존 B-BUILD-P2-01이 남는 직접 반례

위치: `tools/check_node_toolchain.mjs:59`–`:67`.

```ini
engine-strict=true
"force"=true
```

그리고 다음 입력도 통과한다.

```ini
engine-strict=true
force=true
[shadow]
force=false
```

exact helper의 결과는 모두 `ok:true`, `errors:[]`다. 실제 로컬 npm `config get engine-strict force`는 모두 **engine-strict=true / force=true**를 반환했다. 첫 입력은 단순/이중 따옴표 key 양쪽에서 재현되며 미지원 key 경고도 없다(force 보호 해제 경고는 있다). 두 번째는 npm이 section 내부의 force=false를 최상위 force 덮어쓰기로 취급하지 않는데 checker가 평탄화해 덮어쓴다. 새 helper는 값의 따옴표는 처리하지만 key의 INI 문법과 section 경계를 처리하지 않는다.

- 영향: 선언·설정 gate의 유효 force=false 보장이 여전히 성립하지 않는다. 현재 저장소의 기본 `.npmrc`가 이미 악성이라는 뜻은 아니다.
- 권고/처분: **OPEN / 수정 필요**. 지원하는 `.npmrc` 문법을 실제 INI 의미와 일치시키거나, 해석할 수 없는 quoted key/section을 명시 거부한다. 임의 레지스트리 인증·peer/lifecycle 설정 전체를 제거하는 방식은 피하고 정상 root 설정을 보존한다. 이 지적은 신규 P2-03과 같은 설정 해석 계열이므로 중복 root cause로 부풀리지 않는다.

## 신규 finding

### B-BUILD-P2-03 — 따옴표 key·section 때문에 유효 strict=false를 true로 승인

- 위치: `tools/check_node_toolchain.mjs:58`–`:65`; 규범 `docs/standards/versions.md:50`의 **유효** strict/force 요구.
- 실패 시나리오:

```ini
engine-strict=true
"engine-strict"=false
```

- 직접 결과: checker **ok:true**; npm의 유효 값은 **engine-strict=false / force=false**, stderr 공백이다. 작은따옴표 key도 같다. 반대로 quoted key만으로 정상 true를 선언하면 checker는 거부하므로 실제 설정과 parser가 양방향으로 어긋난다.
- 다른 경계: `engine-strict=false` 뒤 `[shadow]` 내부의 true, 또는 section 내부 true만 있어도 checker는 성공하지만 로컬 npm의 root strict는 false다. section 대조의 npm11 로그에는 unknown project config 경고가 있으므로 이를 정본 npm12의 동일 경고/허용 결과로 추정하지 않는다. **quoted key 대조는 그 경고가 없다.**
- 영향: 새 규범이 요구하는 유효 anchor 설정을 잘못 승인한다. 실제 install이 명시 `--engine-strict`를 추가하면 이 특정 false 값은 그 CLI로 덮일 수 있으므로, 이것만으로 모든 CI/install의 보호 해제를 주장하지 않는다.
- 권고: 실제로 인식하는 root key 및 section 의미를 반영하거나 지원하지 않는 문법을 실패로 남긴다. quoted true/false key, bare/root 중복, section의 root 비간섭을 음성·양성 대조로 고정한다.
- disposition: **OPEN / P2, 수정 또는 명시 task·범위 처분 필요**. strict 불변식에 대한 신규 지적이며, 원 force 지적과 같은 parser를 공유한다.

### B-BUILD-P2-04 — preserve-main alias에서 기본 registry 출처가 원 common을 떠남

- 위치: `tools/check_node_toolchain.mjs:270`–`:275`, 특히 default registry를 아직 raw `import.meta.url`로 계산하는 `:275`.
- 실패 시나리오: exact checker를 `fixture/bin/checker.mjs`로 symlink한다. 원 frozen common의 registry는 Node22.23.1/npm12.0.1이고, **alias 부모** `fixture/versions.json`만 Node24.15.0/npm11.19.1로 둔다. root anchor도 후자에 맞춘 뒤 `--registry` 없이 같은 checker를 실행한다.
- 직접 결과:

| 실행 | 잘못된 Node24/npm11 anchor | 올바른 Node22/npm12 anchor |
|---|---|---|
| 실제 파일 경로 | exit1 | exit0 |
| 일반 symlink | exit1 | exit0 |
| `--preserve-symlinks-main` symlink | **exit0, Node24/npm11 PASS** | **exit1** |

- 원인: entry 비교는 양쪽 realpath로 고쳤지만, default registry는 보존된 alias URL의 부모에서 선택한다. 명시 override 없이 같은 프로그램의 기본 정책 출처가 변경된다. 이 probe는 metadata CLI이며 `--runtime`을 실행한 actual Node24/npm11 증거가 아니다.
- 영향: 새로 지원한 alias 실행 경로에서 암묵적인 canonical 선택이 원 common Git source와 달라져 false success 또는 false rejection이 생긴다. 현행 reusable consumer guard는 명시 live `--registry`를 전달하므로 **이 경로의 현재 CI 우회라고 확대하지 않는다**.
- 권고: entry와 default data 위치 모두 같은 실제 checker 경로에서 유도하고, 명시 `--registry` override는 그대로 지원한다. alias 부모에 다른/missing registry가 있을 때도 direct/alias/preserve-main 기본 동작이 같다는 양·음성 대조를 추가한다. API import의 무실행 보존도 유지한다.
- disposition: **OPEN / P2, 수정 또는 명시 task·지원 계약 처분 필요**. 기존 무검사 entry 반례 자체의 FIXED는 취소하지 않으며 별도 출처 문제다.

## 독립 실행·회귀·기존 bytes

- own evidence: `validation/review-B-common-build-rules-e1d0-2-evidence/`. 핵심 probe 소스/결과: `own-attacks.mjs`/`own-attacks-results.json`, `quoted-key-attacks.mjs`/`quoted-key-results.json`, `alias-default-policy-probe.mjs`/`alias-default-policy-results.json`.
- WSL exact 사본 `node --test frozen/tests/check_node_toolchain.test.mjs`: **62PASS / 0FAIL / 0SKIP**. 실제 Node22.22.2/npm11.19.1에서의 구조 테스트다. npm 유효 설정 조회도 이 npm11.19.1이며 새로운 반례를 정본 npm12에서 직접 실행했다고 기록하지 않는다. 새 install·브라우저·네트워크 테스트는 없다.
- 소유자의 canonical receipt 입력 **7개** SHA를 exact e1d0 Git bytes와 대조하고, **4개** raw log SHA를 검산했다. 이 별도 실행의 Node22.23.1/npm12.0.1/runtime 및 builtin **62PASS/0SKIP**는 handoff 증거다. c4cc47의 재명명이 아니다.
- Windows Node25.9.0에서는 own validation 안의 UNC 사본을 export import하여 실제 Windows path로 root/workspace/독립 중첩 anchor 3개를 수용했다. 원 force=true 거부·마지막 false 수용도 확인했으며, quoted force/strict와 section false 승인은 Windows에서도 재현됐다. import에서 자동 CLI가 실행되지 않았다. 이는 Windows 정본 62개를 내가 재실행했다는 뜻이 아니다.
- source/tests의 shell·JSON strict, npm selector/prefix/exec 거부, heredoc/escape의 fail-closed 범위와 정상 default backslash/실제 run 인수 대조를 읽고 62개 구조 테스트에서 통과를 확인했다. script 내부/실제 이미지 내용은 여전히 정적 보증 범위 밖이다.
- 이전 독립 검증에서 hash-bound한 public/package/vendor/frontend 정책 **193개**는 e1d0 Git tree entry가 c4cc와 모두 같음으로 다시 결박했다. root package/lock/registry와 frontend policy/canonical, 4개 workflow도 c4cc와 byte 동일하다. 따라서 예외 8개 정리·기존 4개 보존과 root engines 외 graph/SRI 불변 증거는 이전 리뷰를 그대로 승계하며 새로 앱 전체를 재감사하지 않았다. 기존 실제 C11 7개 bytes/SRI 검산을 참조하고 재pack 0을 유지한다.
- 소비자 caller의 새 입력/명시 live registry/오류 exit 전파는 unchanged다. 구 common-ref에 script가 없으면 fail-closed로 중단하는 제한을 이번 규범이 명시했다. 구 ref 호환성이 복원되었다는 주장이 아니다. CI 순서/needs/fail-fast 최적화는 수행하지 않았다.

## e1d0 CI 직접 관찰

- read-only GitHub commit-associated PR run 조회: **frontend43268085968 / docs43268085933 / python-package43268085715 / selftest43268086175 모두 completed SUCCESS**. API wrapper의 PR·첫 page 범위를 넘는 실행까지 주장하지 않는다.
- docs의 6 job을 직접 조회했다. Windows tools **131356957498** raw log는 exact e1d0 source/checkout, canonical runtime PASS, **62PASS/0FAIL/0SKIP**를 명시한다. 같은 job의 Python은 **400 run / 398PASS / 2SKIP**다. 이를 전부 무스킵 PASS나 내가 재실행한 전체400으로 바꾸지 않는다.
- 이는 실제 e1d0 관찰이며 c4cc CI를 전용하지 않았다. 현재 정상 62개 CI는 본문 신규 음성 입력을 포함하지 않아 OPEN들을 닫지 못한다. metadata와 필요한 raw line을 `github-ci-observation.json`에 고정했으며 전체 raw log 파일을 보존했다는 주장은 하지 않는다.

## 명령·격리·미실행 경계

핵심 명령은 exact `git show/diff/rev-parse/ls-tree`, builtin `node --test`, 자기 probe의 `node ...`, 설치 없는 `npm config get engine-strict force`, Windows `node --input-type=module -e ...` 및 read-only GitHub runs/jobs/logs API다. 별도 Python builtin hash/JSON 검산으로 manifest와 canonical receipt를 결박했다. 최종 evidence index에 각 자기 파일 SHA/bytes와 symlink 대상을 기록한다.

**NOT_RUN:** 신규 `.npmrc` 공격을 정본 npm12에서 직접 실행, Windows 로컬 정본 62개 전체 재실행, 전체 Python400/앱 단위·Doctor·install/build/browser, 새 reusable guard의 실제 소비자 dispatch, image/registry digest 실체/운영/native 실기기/EAS/store. 기존/새 Windows fixture 삭제를 재시도하지 않았고 외부 process 조작도 없다. 이번 새 fixture·증거 쓰기는 자기 validation 범위 안이며 owner repo/index/branch/source/캐시 수정 0이다.

**최종 disposition: B-BUILD-P1-01 FIXED / B-BUILD-P2-01 OPEN / B-BUILD-P2-02 FIXED / 신규 B-BUILD-P2-03·04 OPEN. 원 B의 source verdict BLOCK.**
