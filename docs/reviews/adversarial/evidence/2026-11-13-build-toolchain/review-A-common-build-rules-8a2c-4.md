# Common build rules 8a2c 原A 후보4 독립 재검토 — SOURCE BLOCK

- Execution ID: A-COMMON-BUILD-8a2c-20261112T182614Z
- 원문 고정 UTC: 2026-11-12T18:26:14.297431+00:00
- 원 리뷰어 A/Mill, 구현 비참여. 상대 CURRENT 원문·판정 열람0, 소스/index/branch 편집0.
- exact source: `8a2c7daaf906097937426e81f1bdd69ce0bdd389`
- observed tree: `88ed0d5bf807081732ecc6619d8e553b6abd1047`
- base: `678a5bcf0150ac0386bfa86106e7e0f4f77e8639`; previous BLOCK: `404a586ece08ca0050d844cbe0eee4df5a79f899`.
- manifest: `validation/review-common-build-rules-8a2c-20261113/manifest.json`
- manifest SHA256: `116da46fb3b94f0d3c49ec7fdc40e8e993abd719327131ba69d24190392c9e9a`
- own evidence: `validation/review-A-common-build-rules-8a2c-4-evidence/`.

## 판정·원 finding disposition

**SOURCE BLOCK. P0 0 / P1 0 / P2 OPEN 1 / P3 0. 신규 ID 0.**

A-COMMON-BUILD-P2-01/02/03/04/05는 **FIXED 유지**. A-COMMON-BUILD-P2-06은 **OPEN 유지**: 실제 전달받은 `.npm`/`.npx`와 네 Dockerfile 반례는 해결됐지만, 명령/data 구분이라는 같은 원인이 다른 정상 cache 경로·JSON 인수에서 남는다. 수정·원 리뷰어 재확인 전 보류를 권고하며 예외/후속 이관 승인은 없다. 신규 숫자를 늘려 중복 집계하지 않는다. 추가 사례가 이 commit에서 처음 생겼다고 주장하지도 않는다.

Exact81과 원 consumer 반례 통과, owner canonical81 및 seven-consumer static PASS는 인정한다. 이 사실과 checker의 정상 입력 거부가 남는 source 판정은 구분한다. 원404a 보고서 SHA `07937849d26beb960b2965a375dc0ff10c3a70c9d3ffc009510cedd45ee36c85`는 그대로 보존했다.

## P2-06 잔여 — 점 접두사 제외는 executable/data 구분을 대체하지 못함

- 위치: `tools/check_node_toolchain.mjs:168`, `:172`, 전달된 part의 head를 거부하는 `:84–85`.
- 변경: 기존 word-boundary 감지에 negative lookbehind `(?<![\w.])`가 추가되어 `.npm`/`.npx`는 제외된다. 하지만 슬래시 뒤 `npm`/`npx` 또는 일반 data 문자열은 여전히 실행 파일로 취급한다.
- 본인 최소 직접 재현은 다음 네 가지다. 정본 Node FROM만 두고 npm 명령은 전혀 없어도 각각 **ok:false**와 `정적으로 검증 가능한 Node npm/npx 명령이 필요합니다`를 반환한다.

```dockerfile
RUN mkdir -p /var/cache/npm
RUN ["mkdir","-p","/var/cache/npx"]
CMD ["node","server.js","--cache","/var/cache/npm"]
RUN echo npm
```

위 네 줄은 **각각 독립 fixture**로 실행한 검사 입력이다. 실제 mkdir/node/echo나 Docker 실행을 수행했다는 뜻은 아니다.

- 첫 두 사례는 정상 cache 경로이며 원 `.npm` 경로와 명령 의미가 같다. 세 번째는 실제 executable이 node이고 cache는 data인 명시적 JSON exec-form이다. 네 번째의 `npm`도 echo의 data다. 임의 shell script 내부를 해석하거나 완전한 Docker parser를 구현하라는 요구가 아니라, 지원하는 instruction/JSON argv에서 executable 위치와 data를 구분하라는 요구다.
- 실패 이유: `run[1]`과 `part` 전체 어디에든 matching substring이 있으면 npmCommand를 호출한다. 이 함수는 실제 head가 mkdir/node/echo임을 보고 거부하므로 canonical npm pin/strict 위반과 무관한 false reject가 된다.
- 영향: 현재 전달된 7개 profile의 `.npm` 배치는 해결했지만 checker의 유효 cache 경로·node runtime 명령 수용은 여전히 이름에 좌우된다. 일반 Node Dockerfile gate에서 정상 경로/인수를 바꿔야만 통과하는 제약은 선언된 bounded grammar의 명시적 제한이 아니며, `node`만 실행하는 runtime에는 npm 설치를 요구하지 않는다는 기존 규약과도 맞지 않는다. 현재 7개 profile에서 이 새 경로를 사용한다는 주장은 아니다.
- 권고: cache 이름의 점 접두사만 예외로 더하는 대신 명령 위치와 data argument를 구분한다. 동시에 실제 npm/npx, 절대 CLI·wrapper·dynamic 명령에 대한 기존 거부와 stage pin/strict 검사를 유지한다. JSON 명시 argv, 정상 cache 경로, echo data, 실제 wrapper/CLI를 서로 양·음성 대조로 고정한다. 경로 이름 변경·검사 제외·policy suppression을 권고하지 않는다.
- disposition: **A-COMMON-BUILD-P2-06 P2 OPEN**. 기존 literal `.npm` 실패가 해결된 사실은 보존하면서 root cause closure는 보류한다.

## 원 반례 수정과 정상·음성 회귀 직접 확인

| 범위 | 실제 결과 |
|---|---|
| exact Git `tests/check_node_toolchain.test.mjs` + ini7 | **81PASS/0FAIL/0SKIP**, exit0 |
| 원 `own-consumer-boundary` (최소 .npm/.npx 2 + 원 exact Dockerfile4 + 대조2) | **8PASS/0FAIL/0SKIP**, exit0 |
| 후보2 `own-regressions` payload 그대로 | **13PASS/0FAIL/0SKIP**, exit0 |
| 원 확정7 + 정상/잘못된 FROM 대조2 | **9PASS/0FAIL/0SKIP**, exit0 |
| 새 `own-lexical-regressions` | **10PASS/4FAIL/0SKIP**, exit1 |

마지막 4FAIL이 위 네 정상 입력의 false reject다. 대조10개는 `.npm` 수용, 절대 npm·env wrapper·dynamic shell·strict 해제·fresh npm/npx 거부, pinned npx 수용, pin+ci `&&` 수용, JSON 문자 `&`/`>`/`|` 수용이다. 실패를 지우거나 기대값을 바꿔 녹색으로 만들지 않았다. 같은 원인을 여러 신규 finding으로 세지 않았고 중복 payload를 고유 테스트 총수로 합산하지 않았다.

기존 네 소비자 파일은 A3에서 Git blob/SHA를 고정한 readonly source 입력을 그대로 재사용했다. checker import는 **이번 exact8a2c** fixture로 바뀌고 payload bytes는 동일하다. 이것은 해당 앱 현재 moving tree나 새 build/image 승인 검사가 아니다. 본인이 7개 앱 전체의 WIP source를 다시 실행한 것으로 확대하지 않는다.

실제 테스트 환경은 **Node v22.22.2 + manifest hash-verified ini@7.0.0**이다. manifest dependencySnapshot의 README/package/LICENSE/lib 네 파일 각각의 SHA를 다시 확인해 own fixture에 복사했다. root package/lock도 exact Git 사본이며 dependency-free 실행이라고 주장하지 않는다. fresh install은 수행하지 않았다. Node 내장 runner에서 구조/입력 테스트를 수행한 것으로, own canonical22.23.1/npm12 runtime gate PASS가 아니다.

주요 raw SHA256:

- exact81.log: `b0284302f0202fac93d3d694385474828b1f767247ccd6f81ee58025792a55d1`
- own-consumer-boundary.log: `1765a42bb9b3bc513e14a94f2f4eabb73c4c5b7ba8ec6754d398d52daad3fb85`
- own-regressions.log: `1fd08fb45c0e24df098006c237a687992a47e50cd61ff5b4078f26ab4a7b15ac`
- own-seven-closure.log: `abf11f8c5490d8b1ea481b53ab7bde43c6b44c6f7e9aff237462ca2c44ac969a`
- own-lexical-regressions.log: `b0e10e6b7d864693c66c63c3b776297efbf2e004fc2444c84a7905cd4ed2d1b7`

## Exact input・변경 범위·owner 실행 증거 감사

1. Manifest SHA, tree, 전체21경로의 Git blob/SHA256/bytes를 직접 검증해 일치했다. base 대비 경로 집합도 일치한다. 404a→8a2c delta는 **helper/tests/journal 3개**뿐이며 full diff를 읽었다. 변경 없는18경로는 모두 byte-equal이다. INI lock/공식 package/정책/workflow/public source/vendor를 다시 바꾼 부분은 없다.
2. 원404a에서 직접 확인한 public193/SRI 및 private root ini1개 외 lock deep equality 검토를 변경집합으로 연결한다. 새 공개 pack이나 consumer graph 변경은 없다. source-only followup의 3경로 어느 것도 public193 목록에 포함되지 않으며 전체 build/설치로 새로 검증했다는 주장은 하지 않는다.
3. journal은 기존 actual `.npm` 소비자 거부와 원 BLOCK을 보존하고, 제한된 기존 검사의 수정·81/7static·canonical·리뷰·새 CI를 구분한다. 규범은 바뀌지 않았고 full Docker parser/실제 image 보증으로 확장하지 않는다.
4. `canonical81-receipt.json`의 exact source7 + installed INI4 **입력11 SHA가 모두 일치**하고 node/npm/runtime/builtin **log4 SHA도 일치**한다. owner actual Node22.23.1/npm12.0.1/runtime PASS/81PASS의 content가 현재 immutable Git/snapshot과 연결된다. 원 receipt가 commit 전 worktree followup 관찰임을 content equality로 검증한 것이며 본인의 canonical runtime 실행 또는 exact GitHub CI 기록으로 바꾸지 않는다.
5. `seven-consumers-before.json`/`after.json`의 **7개 inputHashes가 각 before/after 동일**, 각 stable=true, after exit 모두0을 확인했다. Geo/Weather/Transport의 before1→after0과 나머지0→0이 일치한다. 이 owner read-only static 입력에 새 runtime/build acceptance 의미를 추가하지 않는다.
6. `canonical-invariance-proof.json`에 각 비교·receipt SHA를 저장했다. canonical receipt SHA `5d71205c2cfb7c62b192280a4a2756ccfbb5d637af6217c8a102b656fba53066`, seven after SHA `920acb38938d52737bed27ab1b2084f85b45eb29f43b3ce39fbc75709a13aad7`.

## Commands·NOT_RUN·보존

Object 검증은 `git show <exact>:<path>`, `git rev-parse <exact>^{tree}`, `git diff 404a..8a2c` 및 SHA256 비교다. 직접 tests는 `/usr/local/bin/node --test <own evidence>/<suite>.test.mjs`이고 TMPDIR/TMP/TEMP는 own validation 하위다. 기존 fixture가 own TMPDIR 안에서 종료 후 자동 정리되는 것 외 타 owner/cache cleanup0, B의 차단 cleanup 재시도0. 실제 소스·앱/index/branch·production 변경0.

**NOT_RUN/NOT_QUERIED**: 본인 canonical npm runtime, Windows OS, 새 exact8a2c 원격 CI, consumer-smoke dispatch, fresh install/full build/전체 Python400/browser/Docker/image/API/auth/prod/Map 작업. 기존 404a/canonical 성공을 새 CI PASS로 전용하지 않는다. CI 순서/needs/failfast 분석은 시작하지 않았다. 본 원문과 이전 세 원문은 불변이며, 다음 immutable 입력에서 P2-06만 필요한 범위로 재검토한다. SOURCE BLOCK은 새 이미지·운영 재검증 지시가 아니다.
