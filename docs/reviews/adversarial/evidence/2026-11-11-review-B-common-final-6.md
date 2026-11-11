# COMMON6 / C10 — 원 reviewer B 독립 최종 delta 원문

- Reviewer: B / Epicurus. 패키징·dependency 해석·platform·security·license·release/CI 전문, 구현 비참여.
- Run ID: `Epicurus-B-common6-20261111T181021Z`. 시작 UTC `2026-11-11T18:10:21Z`, 종료 UTC `2026-11-11T18:21:45.711742+00:00`.
- 종류: 기존 COMMON4/단일 gzip delta 이후 immutable COMMON6 제한 delta. 상대 reviewer raw 파일은 열지 않았으며 `docs/reviews`는 제품 source 감사에서 제외했다. 필수 README의 기록 규칙만 절차에 적용한다. 기존 원문·manifest·artifact를 수정하지 않았다.
- 입력: `review-manifest-common-6.json`, 관찰 SHA256 `9c4653196c891a4b10b47db5d28c41303ec8617d9a69d064dcabfaaa742d42d4` (시작·종료 동일).
- 관찰 common HEAD `2d70461a7873d73ec2b278709cef1fba832134cc`; producer `55a921b55d248106cbe320e7f5305f3d3cdb60fe`. 이전 full `2ec519255ec1af9fca18856d980e968ee15b80a8`, scanner `f8643d56bd8ce4cc7ff3d730b31173a8583593a4`, 이전 green `447907385d724e9758c511ffc97d39a266262e47`은 대체하지 않았다.
- 격리: 본인 detached worktree `/tmp/review-b-common6-20261111-181021`. 시작/검사 종료 `git status --porcelain` 공백, HEAD exact2d. Git object diff와 해당 immutable checkout만 source로 사용했다. 기존 common modules를 읽기 참조하는 본인 overlay와 본인 fixture만 생성했다. 코드 변경·재pack·install·타인 cache 정리 없음.

## 판정

**BLOCK — 신규 B-P1-11 OPEN 1건.** generic policy/schema/checker, 실제 7개 C10 artifact·원장·lock 및 신규 packed browser 증거는 아래 범위에서 통과했다. 하지만 필수 frontend Doctor gate가 새 helper에서 실제 실패하므로 exact2d를 전체 PASS/merge 승인으로 표시할 수 없다. 기존 B finding closure는 유지한다. Scope fix.2/C11 및 소비자 최종 채택은 별도 입력이며 이 판정에 포함하지 않는다.

## 신규 finding

### B-P1-11 — 새 고정 엔진 helper가 필수 Doctor gate를 실패시킨다

- Severity `P1`, disposition **OPEN**.
- 위치: `packages/ui/smoke/prepare-lock.mjs:33`, `:34`, `:36`; gate 연결 `.github/workflows/frontend.yml:32`, `packages/ui/package.json:236`.
- 증거: 패치 목록 loop 안에서 `artifactPackages.includes`, `packages.includes`, axis package 목록 `includes`를 수행하며 React Doctor 0.9.22가 `react-doctor/js-set-map-lookups` 경고 3건을 낸다. package script는 `--blocking warning`이므로 종료 코드 1이다.
- 직접 재현: exact2d worktree `packages/ui`에서 `node <기존 common node_modules>/react-doctor/bin/react-doctor.js --scope full --no-score --no-telemetry --blocking warning .` → 80 files scanned, warnings 3, exit 1. `doctor.log` 참조.
- 원격 재현: [common frontend run 43074529818 / job 130710770267](https://github.com/digitie/kor-travel-common/actions/runs/43074529818/job/130710770267), contract step FAILURE. 같은 3개 위치와 exit 1을 로그에서 직접 읽었다. 정책175/UI101 등 앞선 검사는 통과했으며 Doctor 뒤의 example 검사 등은 이 step에서 진행하지 못한다.
- CI checkout은 PR 합성 merge `077a0d65bb4e2667a387fdf23ca958f935930351`이다. GitHub compare `2d...077a`는 ahead1/behind0/files0이며 merge base exact2d다. 이동하는 branch나 다른 source 성공을 exact2d 결과로 대입하지 않았다.
- 영향: 정상 후보가 repository 필수 frontend gate를 통과하지 못해 merge/release 수용 기준을 충족하지 못한다. 작은 목록의 조회를 사용자 성능 장애·보안 취약점으로 확대하지 않는다. 심각도는 agent workflow의 필수 gate 파손 기준에 따른다.
- 권고: gate를 약화하지 말고 조회 Set/Map 등을 loop 밖에서 준비하는 방식으로 helper를 정리한 뒤 정책/prepare 회귀, Doctor 및 exact 새 head CI를 재검증한다. 본 reviewer는 구현하지 않았으며 미래 C11/수정 상태를 선반영하지 않는다.

## 직접 검증과 독립 공격

| 검사 | 본인 관찰 |
|---|---|
| dependency + native CSS/engine prepare 정책 | **175 PASS, 0 FAIL, 0 SKIP**, exact source의 두 node test 파일 실행 |
| Python 도구·schema·문서 회귀 | **400 실행 / 399 PASS / 1 SKIP**, 74.863초. skip은 pass에 포함하지 않음 |
| policy 생성 정합성 | `sync_frontend_policy.mjs --check` exit0 |
| root/smoke/example 실제 helper | `prepare-lock.mjs --css-only` exit0; 3경로 Scope/CSS의 선언 section·중복 금지·override·root lock 선언·전이 version/SRI/resolved를 실제 JSON으로 추가 대조 |
| 실제 7개 tgz | 전부 manifest SRI·name·version 일치. artifact directory 원장과 exact2d `frontend-artifacts.json`의 packages도 manifest와 동일 |
| 별도 실제 bytes 기반 정책 probe | **29개 기대 결과 일치**: 7개 모두의 양성 metadata fixture 1, 각 package별 direct lock 변조·local ledger+lock 동시 위조·nested optional 변조·peer alias identity 변조 28개 거부 |
| UI/tokens 빌드·package 검사·example types | 직접 exit0. 재pack 하지 않음 |
| UI unit / tokens unit | **101 PASS / 9 PASS**. UI 최초 own 환경의 미빌드 self-import 실패는 로그에 보존하고, own workspace link + 정식 build 후 전체 재실행하여 해소 |
| secrets / 운영정보 scanner | 1366 files 각각 findings0. digest-bound 명시 예외 secrets32 / prod4. 원시 상수나 비밀값은 보고서에 복사하지 않음 |
| Doctor | **FAIL**, 위 신규 P1 |

`artifact-probe.py`는 실제 C10 tgz를 본인 임시 vendor에 복사하고 metadata/lock을 구성하는 제한 fixture다. 실제 앱 설치·배포 검증이라는 뜻이 아니다. 정상 입력은 원본 SRI 그대로 사용하며 mutation별 새 manifest/lock/ledger를 생성했다. 각 결과와 diagnostics는 `artifact-probe.json`에 보존했다.

독립 source 감사에서 확인한 계약:

- optional `patchedRadixPackages`의 생략 시 기존 동작, 공식 Radix package stem·중복·자료형, npm axis의 단일 package identity/`checked:false`/`exact`/`recommended:null`, artifact/packages 연결을 Python과 generator 경로 및 실제 registry로 확인했다. Python의 공통 axis validator가 exact와 recommended의 병존도 거부하므로 새 patched loop만 보고 누락으로 오판하지 않았다.
- 개별 primitive 직접 선언 허용은 명시 등록된 고정 artifact에 한정되고, 앱의 개별 Radix import/require/re-export 금지는 그대로다. web Scope는 dependencies runtimeRequired이며 모바일에 web UI를 끌어들이지 않는다.
- managed artifact 검사는 runtime뿐 아니라 도달 가능한 빌드 그래프와 연결 workspace의 dev graph까지 적용된다. requested name과 alias actual identity를 함께 본다. stock/wrong-byte nested copy, 직접 pin 누락, unresolved managed edge를 거부한다. registry 도구의 미설치 devDependencies와 도달하지 않는 다른 workspace는 제외한다. React 물리 중복 판정은 기존 runtime 그래프를 유지한다.
- helper는 root·smoke·example의 모든 고정 엔진 bytes/원장/lock을 먼저 검사한 후 두 Next vendor에 복사한다. root Scope는 dev, 두 Next Scope는 runtime, CSS는 세 경로 dev 계약이며 기존 pin/SRI를 임의로 고치지 않는다. `--css-only`는 모든 고정 엔진을 준비하는 호환 명칭이다.
- source/두 배포 checker와 두 policy JSON이 정본과 일치한다. producer와 exact2d의 관련 코드·schema·helper·policy 10개 파일 bytes가 같다. producer→head smoke lock의 UI/tokens SRI 변경은 C10 원장에 맞는 동결 metadata 변경이다.

## Artifact·license·실제 runtime 경계

본인이 C9/C10 tar member를 다시 비교했다. UI94 중92, tokens25 중23, 합계 **115개 파일 bytes 동일**이고 각 package에서 `check-dependencies.mjs`, `dependency-policy.json`만 다르다. 이를 외부 Scope runtime 동일성 주장으로 사용하지 않았다.

C10 LightningCSS fix.4/VWorld core1.0.1·web1.0.3·RN1.0.1 네 tgz는 C9와 byte-identical이다. 이전 독립 source/license/NOTICE 검증과 동일 artifact 연결을 유지한다. Scope tgz는 원 Scope1 검토의 고유 fix.1 `f97c1dd4851fd1dc7b75bfbe9ce7e2d68bbd32e225b9ff52954c683fd4c7081d`와 byte-identical이며 재발행되지 않았다. 7개 manifest SRI 전체는 `artifact-probe.json`에 수록했다.

현재 빌려 읽은 common module의 Scope는 **1.3.1+kortravel.fix.1**이고 dist 6파일 모두 frozen f97 member와 hash/bytes가 같다. 이를 stock1.3.1 baseline으로 쓰지 않았다. Scope source R706/source-pack PASS와 CI conditional의 원 Scope1 보고서는 그대로 보존한다. 사용자에게 전달받은 disabled-fieldset 문제 및 예정 fix.2는 이번에 본인이 재현·폐쇄하지 않았으며 새 artifact/manifest에서 별도 검증한다.

## Exact CI 직접 관찰

최종 API 재조회 결과:

| workflow/job | exact2d 결과 |
|---|---|
| common frontend run43074529818/job130710770267 | **FAILURE** — B-P1-11 |
| docs run43074529633 | **SUCCESS** |
| docs130710769963 / Win tools130710770367 / Linux tools130710770404 | 모두 SUCCESS |
| secret130710770503 / versions130710770518 / packages130710770572 | 모두 SUCCESS |
| workflows selftest run43074529670 | SUCCESS |
| python-package run43074529681 | SUCCESS |

[packages job130710770572](https://github.com/digitie/kor-travel-common/actions/runs/43074529633/job/130710770572)의 실제 로그에서 checkout HEAD exact2d, source SHA 강제 확인, 공식 MCR Playwright1.65/Chromium158.0.8127.18 launch, UI101/policy175/tokens9, 실제 webpack/Turbopack build와 **65 passed (40.5s)** browser 결과를 직접 확인했다. 전체 tokens SRI `sha512-ope7vHGRynjiTDllGJj/qqVz6kmQ/NIsQr4+GnFmyh7jB2rdoTJI3UXU7S+CN5Z8sDMamQ1ez253+Y3ShXoqeQ==`, UI SRI `sha512-avvikdgmPcgNQ8otiKOPRb/fCRSLRIEyV1dudqM4BsKfExScssK+NM7IirvH78lekd7xtEduReQ8/pyqD1BdNg==`가 실제 생성·smoke 준비 출력에 나타나 C10 bytes와 일치한다. 새 Scope를 쓰는 새 실행이므로 과거 c8/c9 browser 결과의 재사용이 아니다. 이는 **원격 실제 실행 로그의 직접 관찰**이며 본인 로컬 browser 실행으로 표시하지 않는다.

## 기존 finding closure·범위 밖·인계

초기 B finding 11 FIXED, own tokens 고지 P3 FIXED, B-P1-08(git trust)·09(고정 예외/유한 archive scanner)·10(linked workspace dev graph) FIXED, f864 concatenated-gzip delta PASS는 원문대로 유지한다. 이 변경에서 scanner source는 이전 green447과 달라지지 않았고 실제 전체 scanner도 통과했다. Doctor 실패는 새 helper의 신규 finding이며 과거 finding 재개봉이 아니다.

B 소비자1의 Map 계약/문서 크기와 Pinvi focus finding 3건은 후속 exact delta 본인 재검증 전까지 OPEN이다. 다른 소비자의 새 문제나 peer 결과는 이 보고서에서 판정하지 않는다. 최종7개 앱 export/배포, 새 fix.2/C11 engine metadata, Scope 최신 fork metadata/producer/recipe, 실제 production lifecycle은 **범위 밖/NOT_RUN**이다. npm clean install·새 브라우저 설치·앱 전체 재실행도 본인 로컬에서는 NOT_RUN이다.

증거는 `review-B-common-final-6-evidence/`에 별도 보존했다. `commands.txt`에 재현 명령과 실행 조정을, `github-observations.json`/`github-final.json`에 직접 API/log 발췌와 합성 merge 비교를, `isolation-and-engine.json`에 HEAD/clean/manifest/borrowed runtime 확인을, `provenance-and-preserved-reports.json`에 producer 정합성 및 기존 본인 raw 12개의 SHA256을 기록했다. `SHA256SUMS.json`은 증거 파일별 hash다. 기존 raw/manifest는 다시 쓰지 않았고 새 파일만 생성했다.
