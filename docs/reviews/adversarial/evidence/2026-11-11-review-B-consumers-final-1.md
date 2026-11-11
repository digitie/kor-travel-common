# 최종 소비자7repo 독립 리뷰 B 원문 1

- reviewer: **B / Epicurus**, 구현 비참여. packaging/platform/security/release 및 실제 dependency 해석·CI 연결 담당.
- runid: `Epicurus-B-consumers-final1-20261111T172634Z`
- UTC: 시작 `2026-11-11T17:26:34Z`, 종료 `2026-11-11T17:55:58.818684+00:00`.
- manifest: `review-manifest-consumers-final-1.json`, 직접 확인 SHA256 `dec96d31adf89696123a3d6a2d2e65c1f204c6e1f92daaa4b8a4ffac4a4460e7`.
- **전체 verdict: BLOCK. Map BLOCK / Pinvi BLOCK / 나머지5repo CONDITIONAL.**
- finding: **P1 1건, P2 2건 OPEN**. 다른5repo에서 새 source finding은 발견하지 않았지만 필요한 CI/수용 gate의 실패·미완을 PASS로 바꾸지 않는다.
- 공통/NativeCSS source PASS는 소비자 승인으로 전용하지 않았다. 상대 reviewer raw/verdict를 열거나 사용하지 않았다. 부모가 알려준 Pinvi 실패도 실제 별도 실행으로 재확인했다.

## 1. 불변 기준선과 repo별 명시 판정

| repo | base | 관찰 head |
|---|---|---|
| kor-travel-geo | `eab5f7a7a7f495b32ebffdf201d6326c3ff0034d` | `a193fd1762ab7dd1058bf5b85ec2d7c96a1368d1` |
| kor-travel-map | `32668d003ea6a259468e03970bd167359c19ecdb` | `925c48c74d46fa9dbe0de53acc6a1cd60ac64f1a` |
| kor-travel-weather | `b55857f7e40fc4f649e65a57172beafda4af8b62` | `d03c1dcbcda0f9f36fb1f9104ca60544d9e8845a` |
| kor-travel-concierge | `4438328704be15592c47281cd19b525e91567767` | `bcfc1b80b78a47319ddcf4918698f19331fb8206` |
| kor-travel-docker-manager | `351e15b4d518daca48e83d2436fc8f1bdf39551c` | `4f1876b6a03b7c4f326653a4773fe724fae68995` |
| pinvi | `d42ac95300749df955ce9e2bb63ea62eba36da09` | `ada425db9deead43a9416d6c761c3fffadd974c1` |
| kor-travel-transport | `59e1d8213c09a82a4ed9cc4396a6414ef0332b9c` | `b327e2a7a2a0389fe95c8396e1dd7334330f490a` |

| repo | B verdict | 결정 근거·남은 gate |
|---|---|---|
| kor-travel-geo | **CONDITIONAL** | 검토 범위 source·패키지 연결과 직접26시험에서 추가 finding 없음. 정확head CI/OpenAPI success이나 중앙 정책 run43067676714 failure. foundation main 정책 반영 후 같은 입력의 guard 성공 확인 필요. |
| kor-travel-map | **BLOCK** | B-CONS-P1-01/B-CONS-P2-02. UI adapter 직접18시험/패키지9정책 대조는 성공해도 기존925의 계약검사4개 직접 실패·문서크기 초과가 있다. 추가e4 merge CI에서도7 failures. |
| kor-travel-weather | **CONDITIONAL** | 직접42시험·패키지 대조 및 source 검토에서 추가 finding 없음. 일반 CI43063010163 success, 중앙 정책43063011228 failure 유지. |
| kor-travel-concierge | **CONDITIONAL** | 실제 전체 Vitest29suites/394 PASS 및 패키지·상태·폼 adapter 검토에서 추가 finding 없음. frontend43062445176 success, 중앙 정책43062446275 failure 유지. |
| kor-travel-docker-manager | **CONDITIONAL** | 실제 전체 단위16suites/54 PASS. 정확4f 일반 CI는 build까지 success 후 Chromium 설치의 DNS 실패로 browser skipped. 중앙 workflow도 failure. 인계의 별도2 browser PASS와 원격 CI 실패를 구분한다. 이후 backend/catalog/tests 조치는4f 밖 별도 입력·배포 gate다. |
| pinvi | **BLOCK** | B-CONS-P2-01: frozen ada425의 stock FocusScope1.3.1 조합에서 초기 panel Shift+Tab 계약 직접 실패. 새 수정 pack/c10/이후 설치는 이 판정의 closure가 아니다. |
| kor-travel-transport | **CONDITIONAL** | 두 표면 직접11+34 PASS·정책/SRI/맵 adapter 검토에서 추가 finding 없음. frontend/admin CI jobs success, backend는 조회 시 in_progress, live-e2e skipped; 중앙 정책43067344641 failure. |

CONDITIONAL은 구현 재작업을 임의 요구한다는 뜻이 아니다. 같은 head의 필요한 CI·수용 증거가 남았다는 판정이다. Map/Pinvi의 구체 실패는 별도 수정/불변 delta로 재확인해야 한다. source가 바뀌면 이 보고서가 새 source에 자동 승계되지 않는다.

## 2. 격리·실행 방식

Windows PowerShell workdir C:\에서 wsl.exe bash로 실행했다. 대형 install·build를 피하려 Git branch의 작업트리를 source로 읽지 않고 **각 exact SHA의 Git object를 자체 tmp에 materialize한 파일 집합**을 사용했다. 이는 정식 git worktree가 아닌 제한된 실행 fixture다. Git cat-file batch와 source별 SHA256 inventory로 기준을 고정했다. 원본 repo·package·lock·artifact를 수정하거나 commit하지 않았다. 부모의 이동 중 구현·새 commonRoot FocusScope 설치를 app baseline에 혼합하지 않았다.

위치는 `/tmp/review-b-consumers-final-20261111-172634/<repo>`였다. Vite cache/시험 결과는 자기 node_modules overlay에만 기록했다. 기존 dependency 항목을 개별 symlink로 읽어 재사용했으며 타인 cache를 삭제하지 않았다. 테스트에 필요한 mts/cts 설정·vendor TS source도 Git object에서 보충했다. 초기 누락·도구 설정 오류 로그와 최종 유효 실행을 구분해 보존했다. source·lock hash inventory의 원본 bytes가 보존됨을 마지막에 확인했다.

모든 앱의 root/app AGENTS 지시와 현재 사용자 scope를 적용했다. 문서의 역사적 소비자 제한을 최신 승인 범위보다 우선하지 않았다. 검토 대상은 frontend 공통화와 연결되는 실제 app diff이며 backend/DB/Dagster 운영·새 배포는 실행하지 않았다. Map의 별도 merge 입력은 §7에 범위를 한정한다.

증거: `review-B-consumers-final-1-evidence/`. 원본 manifest, 7개 source inventory, 실제 artifact/lock/설치 해석, 중앙 guard·36공격, 직접시험 로그, 원격 CI 발췌, 인계 evidence 파일 digest, Map 추가 merge proof를 포함한다.

## 3. 구체 findings

### B-CONS-P1-01 — Map 공통화 변경과 기존 backend CI 계약/전체 gate 감사기가 불일치하여 필수 CI가 실패

- severity **P1**, disposition **OPEN**. repo kor-travel-map. 원925에서도 재현하며 e4 merge-only 수정 때문에만 발생한 것이 아니다.
- 위치: `.github/workflows/frontend.yml:53`, `tests/unit/test_gate_script_mirrors_ci.py:212`, `:406`, `tests/unit/test_frontend_dependency_security.py:100`, `tests/unit/test_c7_prod_live_runner_contract.py:350`, `tests/unit/test_tvn34c_n150_fresh_live_runner.py:84`.
- trigger: root lock/package에 공통 LightningCSS override를 넣고 frontend mandatory `check:dependencies`를 추가한 현재 PR을 전체 CI의 unit/lint 단계에서 검사한다.
- 직접 재현: frozen925의 실제 Python 계약함수4개를 import해 그대로 호출했다. (1) override dict는 기존3개만 예상하여 새 `$lightningcss` 때문에 실패, (2) gate 감사기 `_identifying_fragments`는 새 `npm -w ... run check:dependencies`를 식별하지 못해 실패, (3)(4) 두 runner 계약은 아직 Playwright1.64.1을 예상하지만 실제 immutable Dockerfile은1.65.0이다. 함수 단언을 수정하지 않았으며 전체 backend pytest를 실행했다고 표현하지 않는다.
- 원격: 추가 e4의 CI43070204608에서 Python3.11/3.12/3.13 unit 단계가 모두 failure. 직접 읽은3.11 job130695713425는 **7 failed / 4179 passed / 6 skipped**. 위 항목과 함께 audit control group false, 기존 geo-release UI의 local MISSING_FINGERPRINT_TEXT 추출 실패, 아래 문서크기 실패가 기록됐다. API/Dagster 후속 unit 단계는 skipped다.
- 영향: UI unit432·실제 browser286 인계나 성공한 frontend CI만으로 전체 blocking gate를 충족할 수 없다. gate 감사기의 정상 대조군 자체가 false라 mutation 검출률 근거로도 사용할 수 없다. 중앙 common main의 ENOENT와 구분되는 소비자 고유 통합 결함이다.
- 권고: 새 mandatory 명령의 실제 로컬 mirror와 감사 식별을 추가하고 정상/변조 회귀를 검증한다. exact override·이미지 version/digest·공통 위임 메시지 계약을 현재 정본에 연결한다. 새 명령을 이유 없이 면제하거나 검사를 없애고 frontend success만으로 대체하지 않는다. 다른 root cause인 문서크기는 아래 별도 ID다.
- evidence: `map-ci-contract-repro.py/.json`, `map-merge-ci-failure.json`. Map925 source를 바꾸지 않았고 e4 incoming product가 main과 동일하다는 것과 CI success는 별개다.

### B-CONS-P2-01 — Pinvi stock FocusScope1.3.1에서 panel 초기 focus의 Shift+Tab 순환 실패

- severity **P2**, disposition **OPEN**. repo pinvi. 기능/키보드 계약 결함이며 필수 회귀가 실패하므로 현재 repo verdict는 BLOCK이다.
- 위치: `apps/web/components/ui/Dialog.tsx:101`, `:112`, `apps/web/lib/dialogFocus.ts:37`, `:44`, `apps/web/tests/publicDialog.test.tsx:171`.
- trigger: 공개 Dialog가 열릴 때 첫 입력 대신 `tabIndex=-1` panel을 초기 focus 대상으로 삼는다. panel에 focus한 상태에서 Shift+Tab을 입력한다.
- 직접 재현: frozen ada425 source에서 원본 `publicDialog.test.tsx`를 포함한7개 선택 파일을 실행했다. **49 PASS / 1 FAIL**. 기대한 마지막 button 대신 실제 focus는 panel에 남았다. 첫/마지막 tabbable 사이의 일반 순환과 다른 선택 회귀는 통과한다. B가 실제 browser 밖 focus 유출까지 재현했다고 확대하지 않는다.
- 실제 해석: Pinvi 자체 기존 node_modules의 `@radix-ui/react-focus-scope` version **1.3.1**과 해석 경로를 기록했다. app/common UI runtime93개 member는 c9와 같고 installed checker도 정확 c9다. 다른 repo가 아니라 Pinvi의 실제 stock 설치에서 발생한다.
- 영향: 기본 panel 초기 focus 및 busy 전환으로 panel을 선택하는 경로에서 후진 keyboard 순환이 요구 계약대로 진행되지 않는다. 전체 suite green/앱 수용 완료로 집계할 수 없다.
- 권고: 사용자 지시대로 원 Radix source의 수정·실제 NPM export/pack provenance와 fixed artifact 설치를 별도 불변 입력에서 검증하고 Pinvi에서 해당 회귀 및 실제 browser를 재실행한다. 앱에 자체 trap을 더하거나 단언/기본 focus 계약을 약화하는 것으로 닫지 않는다.
- 부모의520PASS/1FAIL·207PASS/2FAIL/4SKIP 및 새 pack26/9 성공은 인계 정보다. B 직접 결과와 혼합하지 않았다. commonRoot는 이후 패치 중이므로 old stock 증거로 사용하지 않았다. 새 FocusScope manifest/pack/c10은 이번 앱 verdict의 closure로 아직 심사하지 않았다.

### B-CONS-P2-02 — Map 두 기록 문서가 하드 크기 제한을 넘어 문서 계약 CI 실패

- severity **P2**, disposition **OPEN**. repo kor-travel-map.
- 위치: `docs/journal.md:1`, `docs/resume.md:1`; 검사 `tests/unit/test_docs_archive_links.py:97`~`:113`, 한계 `:14`.
- 재현: 본문/상대 review를 읽지 않고 불변 Git blob의 실제 byte 크기를 확인했다. 한계225,280 bytes에 대해925는 journal226,356/resume229,265, e4는 journal228,112/resume230,846이다. incoming main41de16d은220,115/223,536으로 한계 안이다.
- 원격 e4 CI에 동일한 두 파일·크기와 failing test가 직접 기록돼 있다. 따라서 당시 merge에서 양쪽 이력을 보존했다는 증거만으로 이 gate가 통과하지 않는다. 925부터 이미 존재하며 merge가 크기를 더 늘렸다.
- 영향: 문서 규약·CI의 필수 검사 실패. 기록 유실 없이 분리해야 한다.
- 권고: 기존 history를 archive로 분리하고 현재 resume를 압축해 링크를 유지한다. limit 상향·test 제외·원문 리뷰 재작성으로 숨기지 않는다. runtime/UI/lock 재포장은 필요 없다.

## 4. 패키지·플랫폼·보안 공통 검증

불변 Git에 담긴 **vendor tgz37개**를 직접 읽어6종 canonical C9 파일의 SHA512/256과 대조했다. 10개 원장의 canonical package 필드도 일치한다. Pinvi mobile의 추가 file 경로 필드는 정본 version/filename/integrity를 바꾸지 않는다. 중앙 checker는 frozen code `2c1182e765bb2bc53e01e0962cf2a73683891e1d`, 정책은 같은 입력, artifact 정본은 manifest가 지정한 C9/d1fe 기준을 사용했다. producer2c의 과거 ledger를 C9 ledger로 오인하지 않았다.

**9개 표면 모두** actual app package/root-or-workspace lock·vendor·source를 함께 넘긴 canonical guard가 exit0이었다. 앱 source를 실행하지 않는 lock/AST 검사임을 구분한다. 고의 lock/선언/source 입력을 별도 임시 파일로 만들고 다음4종×9=**36개 모두 exit1 거부**를 확인했다: React18 혼입, CSS integrity 변경, React section 중복, private 지도 source 재export. 원 package/lock은 손대지 않았다.

실제 설치를 읽을 수 있는7개 웹 표면에서는 app과 common UI가 같은 physical React를 해석하고 UI runtime/CSS/metadata93개가 c9와 동일하며 checker도 C9임을 확인했다. Map은 기존 local node_modules가 없어 Geo의 같은 버전 도구로 제한한 별도 fixture만 실행했다. Map 실제 설치 증거는 worker의 n150 인계와 구분한다. Pinvi mobile에서 root UI가 해석 가능하다는 것은 monorepo web용 설치가 있기 때문이며, mobile의 UI 소비로 세지 않았다. mobile direct DOM UI 금지와 runtime graph는 별도 profile 검사로 판단했다.

Map/private mono-root alias 제거, public core/web/RN imports, React/RHF/Zod/Zustand·font 축, linked workspace dev CSS 탐색, optional/peer 물리 graph, release code pin과 artifact SRI 연결을 확인했다. Font/CSS source scanning 및 불변 common의 RSC/export 결론은 실제 앱의 import/설치/빌드 evidence에 연결했으며 그 자체를 앱 전체 승인으로 사용하지 않았다.

재사용한 common/VWorld/LightningCSS pack은 기존 LICENSE/NOTICE/출처/source 내용의 동일 bytes다. 앱 원본의 기존 license 상태와 타사 package license를 구분했다. 이 검토는 새로운 공개 배포의 모든 고지·소스 제공 절차나 앱 전체의 라이선스 변경을 실행/승인한 것이 아니다. 직접 source diff에서 credential·새 비밀 파일을 넣거나 server auth/proxy 경계를 약화한 변경은 확인하지 못했다. backend의 권한/비밀 처리 전체를 새로 감사한 결과로 확대하지 않는다.

## 5. 실제 앱 diff와 B 직접 실행

| repo/표면 | 실제 살펴본 app 연결 | 직접 유효 실행 |
|---|---|---|
| Geo | VirtualTable 열/정렬/검색/row id·DOM 보존 adapter, AppShell context와 auth 문서 이동, public 지도 imports·alias 제거, Docker lifecycle 패치 삭제, globals/font/source 경로 | 원본 config 선택3suites **26 PASS** |
| Map | loading/disabled activation을 보존하는 Button, 단일 Dialog content·close 기본값 adapter, NativeSelect·shared DataTable, marker workspace/public VWorld, RHF·선택 상태·image/test helpers | 대체 alias fixture4suites **18 PASS**; 원본 config는 vite-tsconfig-paths 부재로 local NOT_RUN |
| Weather | 공통 Login status mapping/sanitize next, weather-detail 분리 모델/비가상표·marker budget, VWorld/style·font·popup, GET annotation의 실제 무부작용 경계 | 원본 config 선택4suites **42 PASS** |
| Concierge | native coarse picker와 빈값 Radix mapping, instance-local Zustand 폼/error·query cache/로그인 next, review selection/undo/reprocessing 상태 및 public 지도 | 원본 config 전체29suites **394 PASS** |
| Manager | OpsDialog·useConfirm의 동시요청/세션·unmount 취소, RHF field array, container tabs·WebSocket dispose·redaction 표시, common style/font | 원본 config 전체16suites **54 PASS** |
| Pinvi web/admin/mobile | public/admin Dialog·busy·opener 복귀/disabled/scroll, common login, public 지도·worker check, mobile NativeWind5 Metro/Babel·tokens/font·native/web map/SSR·storage failure | web/admin 선택 **49 PASS/1 FAIL**, mobile platform 별도3suites **4 PASS**, styling check exit0 |
| Transport public/admin | app/src private package export와 linked source, fee/history/RHF, admin Login status, journey/map marker/reference adapters·font/CSS·Docker copies 및 proxy 경계 | public **11 PASS**, admin **34 PASS** |

대체 Map fixture는 원래 tsconfig `@/*→src/*`와 원본 Vite setup/deps/exclude를 명시적으로 유지하고, actual marker workspace source를 연결했다. assertions/timeout/제품 code를 바꾸지 않았다. 그래도 원본 config·원 설치·새 production build 전체를 B가 실행했다고 주장하지 않는다.

초기 시험의 오류도 보존했다. mts 설정/vendor source를 빠뜨린 복사본, runner loader의 __dirname 부재, 불충분한 borrowed dev 도구 때문에 환경 실패가 있었다. source Git object를 빠짐없이 보충하고 원본 config의 bundle loader로 유효 실행을 다시 했다. Pinvi의 FocusScope 실패는 이러한 준비 오류와 달리 모든 source·설치 bytes를 확인한 뒤 남은 실제 단언 실패다. 신규 install 없이 유효한 회귀만 표의 PASS로 집계했다.

## 6. 인계 증거와 원격 CI — 직접 실행과 분리

검증 원문/JSON을 읽고 SHA256을 남겼다. 인계상 Geo C8 Chromium27+Firefox27, Map unit432/reporter37/D286 strict·skip0, Weather unit308/browser20+tile5, Manager2 browser, Transport public164/admin356와 native/Alpine browser4/18 등이 있다. 이는 B 직접 재실행 수치가 아니다. C8→C9 UI/tokens는 checker 두 파일만 달라 runtime/CSS/metadata117개가 같다는 기존 증거와 본인의 artifact/실제 설치 비교를 연결했다. Geo WSL .next는 옛 C6라는 인계도 보존하고 새 production artifact로 취급하지 않았다. QA 이미지·단계 검증은 운영 배포가 아니다.

Map 실제 full-runner source e3ea216c128c3e7ef5346b17db6d4ec3fd5272a0→925는 docs4개+workflow뿐임을 직접 Git diff로 확인했다. Pinvi product f631334의 full SHA와 ada425 사이도 workflow/doc 두 파일뿐이다. 이 동일성은 source 연결 근거이며 green을 만들어내는 근거가 아니다.

직접 GitHub API에서 본 상태:

- Geo: 일반 CI/OpenAPI success, common-policy failure. geo job130686869627 로그의 실제 원인은 현재 중앙 main에 frontend-dependencies.json이 없다는 ENOENT다.
- Weather/Concierge: 일반 CI 또는 frontend success, common-policy failure.
- Manager: general CI43060803657 failure. frontend130662522580의 install/guard/type/lint/Doctor/unit/build는 success이고 apt DNS 오류로 Chromium 설치 failure, browser skipped다. worker의2개 browser PASS를 이 원격 skipped의 성공으로 바꾸지 않는다.
- Transport: 일반43067343703의 frontend/admin success, backend는 조회 시 in_progress, live-e2e skipped. common-policy failure.
- 원925/Pinvi ada425: commit_workflow_runs 도구는 PR-triggered 첫 페이지 한정이며 결과가 비어 있었다. 이를 전체 GitHub에 CI가 없다는 증거로 사용하지 않는다.
- 추가 Map e4: frontend/docker-images/openapi/lint success여도 general ci는 failure, common-policy도 failure다. 특히 general ci의7개 실패를 중앙 정책 실패에 합쳐 숨기지 않는다.

공통49·정책 main 반영 뒤 동일 입력의 중앙 guard 재실행이 필요하다는 부모의 계획을 확인했지만 아직 성공으로 표시하지 않았다. Manager 후속 backend/catalog/tests는 사용자 지정 별도 delta이며 4f의 이 보고서에서 구현·검증한 것이 아니다. 실제 UI-only release 경로·공식 catalog/receipt·배포 승격은 남은 외부 gate다.

## 7. 별도 Map merge delta / common gzip delta

추가 입력 e4dfac80fa0afb3b3bc30118462e5485b1786520의 부모를 직접 확인했다:925 +41de16d8169c2f59d2973d26caf1a0a7be657a83. frontend 전체·root package/lock/vendor는925와 diff0. 변경된12개 product file은 incoming main과 bytes 전부 같다. 부모 JSON만 믿지 않고 각각 재계산했다. 따라서 **프론트·패키지에 한정한 merge-content 보존은 PASS**다. incoming main의 backend 의미 전체나 적용 migration을 B가 재실행한 것이 아니며, parent의 targeted171/ruff/migration graph PASS는 인계 증거다. DB/API/Dagster lifecycle은 실행하지 않았다. CI7실패와 문서크기 문제 때문에 merge delta 전체를 PASS로 승인하지 않는다.

common `f8643d56bd8ce4cc7ff3d730b31173a8583593a4` 한정 gzip delta는 별도 원문 `review-B-common-gzip-f864-delta.md`에 **source PASS**로 제출했다. 집중62 PASS, 세 second-header canary의 old2ec false accept/newf864 reject 및 유효 single-member 대조를 직접 확인했다. 기존 COMMON4 raw·manifest·publication은 수정하지 않았다. 이 검증도 앱 승인이나 새 common remote CI 전체 PASS를 대신하지 않는다.

## 8. 명령·보존·최종 경계

주요 명령/방법:

```bash
sha256sum review-manifest-consumers-final-1.json
git rev-parse <각 head>^{commit}
git diff <각 base> <각 head> -- <source/config paths>
git cat-file --batch  # exact head:path source bytes, 개별 SHA256 inventory
node <frozen2c checker> --policy <frozen policy> --canonical <C9> --package <app> --lock <root lock> --workspace <relative path> --profile <web/mobile> --artifacts <app ledger> --source <actual source>
python3 -B check-artifacts.py
python3 -B consumer-guard-attacks.py
node <borrowed consumer vitest> run <선택 tests> --configLoader bundle --no-cache --fsModuleCachePath <own tmp> --no-file-parallelism --maxWorkers 1
node --experimental-import-meta-resolve installed-identity.mjs
node scripts/check-mobile-styling.mjs
python3 -B map-ci-contract-repro.py
```

실제 전체 argv·초기/최종 로그와 source/probe 제한은 evidence에 남겼다. GitHub는 commit_workflow_runs, workflow_run_jobs, workflow_job_logs만 읽기 조회했다. 원격 댓글/rerun/merge/배포·source implementation commit은 하지 않았다. 기존 원문8개 SHA는 old-raw-sha256.json에 보존한다. reviewer 소유 tmp/overlay/cache만 제거하고 타인 원본 모듈·캐시/부모의 증거는 보존한다.

**최종 명시 판정: Geo CONDITIONAL / Map BLOCK / Weather CONDITIONAL / Concierge CONDITIONAL / Manager CONDITIONAL / Pinvi BLOCK / Transport CONDITIONAL.** Source 구현·package 연결에 대한 검토를 완료했으며, Map2 finding과 Pinvi1 finding은 OPEN이다. 실제 소비자 production build/image 배포·앱 기기 실행·전체 backend 재실행·새 FocusScope pack/c10·이후 Manager delta는 NOT_RUN/별도 입력이다. 미래 수정이나 parent의 예비 성공 정보로 원 불변 verdict를 덮어쓰지 않는다.
