# 원 reviewer A(Mill) — 최종 소비자7저장소 독립 리뷰1

- Run ID: Mill-A-consumers-final1. 시작 UTC: 2026-11-11T17:30:32.218530+00:00. 원문 확정 UTC: 2026-11-11T18:00:34.836281+00:00.
- 전문: frontend/accessibility·도메인 회귀. 구현에 참여하지 않았으며 다른 reviewer raw/verdict를 읽지 않았다. source diff에서 docs/reviews와 reviewer raw를 제외했다.
- 입력 manifest SHA256 **dec96d31adf89696123a3d6a2d2e65c1f204c6e1f92daaa4b8a4ffac4a4460e7**, 직접 계산 일치.
- **전체 verdict: BLOCK.** Pinvi의 사전 공개 차단을 본인이 재현했다. 별도로 신규 P2 세 건이 OPEN이다.
- 신규: P0=0/P1=0/P2=3/P3=0. 사전 공개·본인 재현 P2=1을 구분한다.
- 이전 common4/Native3/gzip closure 원문은 수정하지 않았다. 공통 source 성공을 앱 승인으로 확대하지 않았다.

root=/home/digitie/dev/common-unification-20261111.
원문=root/review-A-consumers-final-1.md.
영구 evidence=root/review-A-consumers-final-1-evidence/.

## 1. 저장소별 명시 판정

아래 PASS는 **A의 지정 frontend source 검토 범위**다. 미완 중앙 CI·배포·peer gate를 통과시키는 merge/release 승인이 아니다.

| 저장소 | immutable head | A source verdict | 근거·잔여 |
|---|---|---|---|
| Geo | a193fd1762ab7dd1058bf5b85ec2d7c96a1368d1 | **CONDITIONAL** | 단위289 PASS, 설치/guard 일치. A-CONS-P2-03 공통 Button 위임 누락 OPEN |
| Map | 925c48c74d46fa9dbe0de53acc6a1cd60ac64f1a | **CONDITIONAL** | 실제 adapter 집중21 PASS, source/원장/lock 일치. A-CONS-P2-02 variant/size 누락 OPEN |
| Weather | d03c1dcbcda0f9f36fb1f9104ca60544d9e8845a | **PASS** | 직접308 PASS·installed5/guard 일치, 새 finding0. 중앙 CI 재확인 별도 |
| Concierge | bcfc1b80b78a47319ddcf4918698f19331fb8206 | **CONDITIONAL** | 직접394 PASS이나 별도 실제 Chromium에서 A-CONS-P2-01 checkbox focus 유실 재현 |
| Docker Manager | 4f1876b6a03b7c4f326653a4773fe724fae68995 | **PASS** | 직접54 PASS·installed3/guard 일치, frontend 새 finding0. 원격 Chromium 설치 DNS 실패로 browser gate 미완 |
| Pinvi | ada425db9deead43a9416d6c761c3fffadd974c1 | **BLOCK** | 집중74실행=73 PASS/1 FAIL. 원 panel Shift+Tab 차단 OPEN. 미래 Scope/C10 미적용 |
| Transport | b327e2a7a2a0389fe95c8396e1dd7334330f490a | **PASS** | 공개164·관리자356 직접 PASS, 두 frontend 설치/guard 일치. 중앙 CI·backend 완료 별도 |

Map의 후속 e4dfac80fa0afb3b3bc30118462e5485b1786520은 §7의 **bounded merge delta만** 추가 검토했다. 원925 판정을 그 merge 전체 backend 승인으로 바꾸지 않는다. 같은 frontend이므로 Map P2는 e4에도 남는다.

## 2. Immutable source·실제 설치 정합

manifest의 base→head별 diff와 변경 주변 source를 조사했다. Git object에서 frontend·관련 root/workspace 파일 약17MB를 개인 snapshot으로 복사하고, 시험 뒤 291/356/101/183/70/591/287개 실제 Git 파일을 원 head와 다시 대조해 차이0을 확인했다. 생성한 probe/driver와 vendor fixture는 구분했다.

시작 시7checkout은 모두 지정 HEAD/clean이었다. 종료에는 Map이 부모 승인 merge e4로 진행했고, Geo docs/kor-travel-common-library-review.md 및 Manager backend release-candidate 작업이 dirty였다. 이 현재 작업은 보존했고 immutable 앱 검토에 섞지 않았다(observations-start/end.json). root source 코드나 lock을 변경하지 않았다.

각 repo vendor의 canonical6 대상 tgz를 immutable Git에서 읽어 중앙 SHA256/SRI와 대조했다. 실제 설치 파일도 archive의 모든 일반 파일과 byte/hash 대조했다:

- Geo/Weather/Concierge/Pinvi web/Transport admin: UI·tokens·core·web·fix4 모두 MATCH.
- Manager/Transport public: UI·tokens·fix4 모두 MATCH.
- Pinvi mobile: tokens·core·RN·web·fix4 모두 MATCH, DOM UI 설치를 요구하지 않았다.
- Map의 WSL 원 설치는 비어 있으므로 actual installed identity를 PASS하지 않았다. vendor/lock/원장과 외부 canonical guard는 직접 PASS, N150의 실제 설치 일치는 인계 evidence다.

모든9표면에 공통 source2c checker와 최신 지정 정본/canonical 인자를 적용한 외부 guard를 private source에서 실행하여 exit0을 확인했다. workflow code pin2c도 확인했다(identity-and-guards.json). Root override·연결 workspace CSS graph·file vendor containment·lock integrity 검사는 이 checker의 실제 실행 범위다. Pinvi web 공식 scope인 admin 외 공개 컴포넌트도 별도 source inspect했다.

C8→C9의117 runtime/CSS/metadata 동일성은 이전 본인 검증을 유지했다. Geo eee413d→a193, Map e3ea216→925, Pinvi f631334→ada425가 frontend runtime이 아닌 workflow/docs 차이임도 Git diff로 직접 확인했다. 앱 자체 변경까지117파일 근거로 면제하지 않았다.

공통 Root 모듈은 부모가 fixed Scope로 변경 중이므로 stock baseline으로 쓰지 않았다. 실제 probe의 UI/React는 소비자 모듈을 사용했다. 여덟 web 표면의 radix-ui→FocusScope 해석 경로와 dist 전파일 hash를 보존된 stock1.3.1 folder와 비교하여 모두 같았다(focus-scope-provenance.json). Map probe의 모듈은 검증된 Geo canonical 설치를 재사용한 fixture임을 별도 표시했다.

## 3. 직접 검증·인계 증거·NOT_RUN

로컬 Node는 실제 v22.22.2였다. CI/N150의22.23.1과 같은 실행환경이라고 주장하지 않는다. Vite cache·출력은 개인 tmp에, 모듈은 기존 설치 읽기 참조로 두었다. fresh install·대형 새 build·앱 데이터 조작은 없었다.

| 직접 실행 | 결과 | evidence |
|---|---|---|
| Geo 전체 단위 | 52파일289 PASS | kor-travel-geo/unit.log |
| Weather 전체 단위 | 27파일308 PASS | kor-travel-weather/unit.log |
| Manager 전체 단위 | 16파일54 PASS | kor-travel-docker-manager/unit.log |
| Concierge 기존 전체 단위 | 29파일394 PASS | kor-travel-concierge/unit-concierge.log |
| Transport 공개 전체 | 16파일164 PASS | kor-travel-transport/unit-transport-public.log |
| Transport 관리자 전체 | 48파일356 PASS | kor-travel-transport/unit-transport-admin.log |
| Map 실제 adoption5파일 | 21 PASS, canonical 재사용 fixture | kor-travel-map/unit-bounded.log |
| Pinvi adapter/로그인/mobile-map 집중12파일 | 73 PASS/1 FAIL, 총74 | pinvi/unit-bounded.log |
| Concierge 실제 source의 본인 DOM 공격 | baseline2 focus 보존/current2 유실 | candidate-focus-direct.log |
| 같은 공격 실제 Chromium158.0.8127.18 | baseline2 보존/current2 BODY, pageerror0, exit1 | candidate-browser-probe.log |
| Map variant/size 독립 SSR 대조 | 공통 직접 호출 정상/Map wrapper metadata·default bg 오류, exit1 | button-forwarding-probe.log |
| 9표면 외부 canonical guard | 모두 exit0 | 각 repo guard-0/1.log |
| actual installed bytes·Scope provenance | 위 범위 MATCH | identity-and-guards.json / focus-scope-provenance.json |

Concierge browser는 실제 두 CandidateTable source와 검증된 c9 UI를 bundle한 작은 fixture다. 원 앱 전체 Next production E2E나 시각 CSS 수용 시험은 아니다. 요청은 loopback만 허용했고 종료 시 자기 browser/server를 닫았다. 확인한 DOM 교체·키보드 focus 회귀에 앱 CSS가 필요하지 않다는 범위를 명시한다.

초기 driver 실패도 숨기지 않는다. Map/Transport snapshot이 source lib/vendor 및 Dockerfile 입력을 빠뜨린 실패는 입력을 추가하고 재실행했다. Concierge의 첫 Vitest DOM driver는 jsdom 미설치 환경 때문에 미실행이었으며, 기존 Manager jsdom과 소비자 React를 사용한 별도 직접 DOM/실제 browser probe로 대체했다. 초기 Pinvi binary 위치도 hoisted root로 교정했다. 원시 로그는 보존하고 제품 finding으로 세지 않았다.

Map 확대 source-all 시도는368 PASS/3 FAIL 및2suite 미수집이었다. 실패3은 개인 frontend-only snapshot의 backend enum fixture 누락, 미수집2는 재사용 모듈에 sonner가 없는 driver 제한이었다. 이것을 Map 전체432 PASS라고 바꾸지 않는다. 유효 집중21과 원본 source/worker432·D286 evidence를 구분한다.

인계 evidence로만 확인한 항목: Geo Chromium27+Firefox27, Map D286 전체 runner/cleanup 성공, Weather browser20+tile5, Manager viewport2, Transport native/Alpine 공개4+admin18, Pinvi full520/1 및207/2/4·특수 mobile exports/fonts. 해당 인계의 정확 tested source와 이후 runtime 불변 근거를 대조했지만 그 전체를 본인이 재실행했다고 하지 않는다.

새 전체 production build·Doctor·전체 browser inventory·Expo export·실기기·EAS·스크린리더 낭독·실제 배포는 NOT_RUN이다. package/engine 원 source 승인도 앱 수용 증거로 합산하지 않았다.

## 4. A-CONS-P2-01 — Concierge 선택 시 checkbox remount와 focus 유실

**OPEN / P2 / 신규 독립 finding.**

- 위치: frontend/src/components/review/CandidateTable.tsx:92, :95, :115, :123.
- 원인: 매 render마다 columns 및 header/cell arrow 함수가 새 component type이 된다. common VirtualTable의 flexRender가 이 함수를 component로 렌더하므로, 선택 state 갱신만으로 기존 Checkbox를 unmount한다. CandidateCell에 memo가 있어도 상위 cell component type이 바뀌면 보호하지 못한다.
- 재현: 실제 CandidateTable에 후보1개와 controlled selected set을 연결한다. 헤더 전체 선택 checkbox 또는 행 checkbox를 focus한 뒤 Space. query data는 안정적으로 유지했다. 기존 base와 current를 같은 canonical UI·동일 fixture에서 대조했다.
- 실제 Chromium: base 두 경우 sameNode=true/oldConnected=true/focusPreserved=true/activeTag=BUTTON. current 두 경우 sameNode=false/oldConnected=false/focusPreserved=false/activeTag=BODY. aria-checked=true로 선택 자체는 반영되며 pageerror0이다.
- 영향: 키보드로 후보를 연속 선택할 때 매번 탐색 위치를 잃는다. 나머지 셀의 입력·버튼도 갱신 때 remount될 수 있으나 실제 입증한 범위는 두 checkbox다.
- 권고: cell/header component 참조를 module scope로 고정하고 갱신 state/action은 table/column meta 또는 row model로 전달한다. body는 common renderCell callback으로 node를 반환하는 방식도 가능하다. selected set을 dependency로 둔 columns useMemo만으로 함수 type을 다시 만들면 같은 문제가 남는다. 실제 키보드/DOM identity 회귀를 유지한다.
- 증거: kor-travel-concierge/candidate-browser-probe.cjs/.log, candidate-browser-runtime.json, candidate-focus-probe.cjs 및 원 baseline source 복사.
- Disposition: 수정·같은 원 reviewer 재확인 또는 owner/task/gate/기한의 정식 P2 disposition. 이 원문은 연기를 승인하지 않는다.

## 5. A-CONS-P2-02 — Map Button이 공통 variant·size를 전달하지 않음

**OPEN / P2 / 신규 독립 finding.**

- 위치: packages/kor-travel-map-admin/frontend/src/components/ui/button.tsx:71 부근.
- wrapper가 variant/size를 destructure한 뒤 지역 CVA에만 사용하고 ButtonPrimitive(현재 @kor-travel/ui/button)에 props로 넘기지 않는다. 기존 raw/Base UI primitive를 공통 styled Button으로 바꾼 뒤 default recipe가 추가로 남는 형태다.
- 재현: 실제 wrapper의 ghost/link/outline 및 icon-xs를 renderToStaticMarkup하여 같은 c9 CommonButton 직접 호출과 대조한다.
- 실제: Map은 요청 variant와 관계없이 data-variant=default, size=icon-xs 요청도 data-size=default다. ghost/link에는 bg-primary가 남는다. CommonButton 직접 ghost/link는 올바른 data-variant와 icon-xs이며 bg-primary가 없다. 지역 ghost/link recipe에는 기본 배경 override가 없어 공통 default의 채움이 유지된다.
- 영향: 투명/링크 역할 버튼이 primary 채움으로 렌더되고 variant/size metadata 계약이 깨진다. 실제 pixel contrast 전체를 측정했다고 주장하지 않으며 생성된 root class와 잘못된 전달 경로로 판별했다.
- 권고: 공통 Button에 variant={variant}, size={size}를 전달하고 실제 투명/링크·아이콘 크기 browser/markup 회귀를 추가한다. 지역 전체 recipe 중복은 공통 props와 최소 domain class mapping으로 줄인다. 기존 loading 포커스·label 유지 정책을 보존한다.
- 증거: kor-travel-map/button-forwarding-probe.cjs/.log.
- 925→e4의 frontend가 동일하므로 이 finding은 merge delta에도 남는다. 현재 OPEN이다.

## 6. A-CONS-P2-03 / A-CONS-P2-04

### Geo 공통 Button 위임 누락 — A-CONS-P2-03

**OPEN / P2 / 신규 source 채택 계약 finding. 기능 회귀 재현과 구분한다.**

위치: kor-travel-geo-ui/components/ui/button.tsx:8〜22 및 button-variants.ts:3.
Button은 @kor-travel/ui/button을 사용하지 않고 radix-ui Slot.Root 또는 raw button을 직접 만들며 지역 CVA 전체 recipe를 계속 소유한다. 변경은 React19 ref 전달 보강이고 공통 primitive 위임이 아니다. 따라서 UI/tokens 설치·타 primitive 채택·guard 성공만으로 이 공용 Button까지 실제 공통 구현을 소비했다고 볼 수 없다.

재현/확인: immutable source의 Button import/반환 경로와 그 지역 variant 모듈을 추적했다. Geo 호출부의 이 Button 경로는 공통 Button의 loading/disabledReason 및 후속 공통 수정 계약을 공유하지 않는다. 현재 앱이 loading prop을 실제 넘겨 실패했다고 주장하지 않는다. 이는 공통화 요청의 구현 누락이며 새 runtime 오류 finding은 아니다.

권고: 공통 Button에 위임하고 필요한 기존 브랜드 표현만 얇은 props/class mapping으로 보존한다. pure variant helper도 공통 소유 모듈로 연결하거나 예외 범위·사유를 정식 disposition한다. React19 ref/asChild·Dialog trigger 동작은 기존289 및 실제 focus probe로 보존해야 한다.

### Pinvi 초기 panel Shift+Tab — A-CONS-P2-04

**OPEN / P2 / 사전 공개 차단·원 A 직접 재현. Pinvi verdict BLOCK.**

위치: apps/web/tests/publicDialog.test.tsx:171〜175, components/ui/Dialog.tsx의 onOpenAutoFocus, lib/dialogFocus.ts 및 stock FocusScope1.3.1 루프 처리.
실제 source12파일 집중시험에서 같은 기대가 실패했다. panel을 focus한 뒤 Shift+Tab하면 last button으로 가야 하는데 panel에 남는다. 본인이 background로 실제 누출됐다고 확대하지 않는다.

모듈은 stock registry1.3.1 dist와 hash 일치한다. 앱의 사본 Tab trap·단언 하향으로 닫지 않는다. 부모가 준비한 source/fixed package는 이 소비자 manifest에 없으므로 미래 fix.1의 source unit/browser 성공을 현재 Pinvi 승인으로 대신하지 않는다. 고정 새 artifact/lock/input 뒤 재확인이 필요하다.

전체 E2E207PASS/2FAIL/4SKIP과 관리자 단독8.7초 PASS는 인계 수치로 보존한다. 종합 시나리오30초 초과를 단독 성공으로 지우지 않았고 별도 제품 finding으로 중복 채번하지 않았다.

## 7. Map e4 bounded merge delta

추가 입력 e4dfac80fa0afb3b3bc30118462e5485b1786520의 부모는925와 main41de16d다. frontend/root package·lock·marker package/vendor diff0을 직접 확인했다.

merge-content-proof의 incoming12파일을 e4 Git blob·41de16d blob·선언 SHA256과 독립 대조하여 모두 정확히 같았다(bounded-merge-delta-proof.json). 검색 migration450/backend search 변경은 이 frontend delta가 아니다. 실제 backend171/ruff/migration graph는 worker 인계 증거이고 본인이 실행하거나 semantic backend 승인한 것이 아니다. DB/API/Dagster lifecycle은 수행하지 않았다.

따라서 frontend에 별도 merge 회귀는 발견하지 못했지만 기존 Map P2-02는 그대로 OPEN이다. 전체 merge/deploy 가능 판정이 아니다.

## 8. 직접 API로 관찰한 CI·배포 경계

exact manifest head를 인자로 GitHub connector의 workflow-runs를 직접 조회했다(ci-direct-observation.json). 이 endpoint는 PR-triggered 첫 page 범위다. 빈 결과를 모든 종류 CI가 없다고 단정하지 않는다.

- Geo a193: CI43067675972/OpenAPI43067675821 SUCCESS, 중앙 policy43067676714 FAILURE.
- Weather d03: CI43063010163 SUCCESS, 중앙 policy43063011228 FAILURE.
- Concierge bcfc: frontend43062445176 SUCCESS, 중앙 policy43062446275 FAILURE.
- Manager4f: CI43060803657 FAILURE. jobs/log 직접 확인상 backend와 frontend 타입/lint/Doctor/unit/build는 SUCCESS, Chromium --with-deps 설치 중 Ubuntu mirror DNS 실패(exit100)로 browser step SKIPPED다. 이를 UI 제품 실패로 채번하지 않으나 CI/browser gate 미완은 유지한다. 중앙 reusable workflow43060804091도 FAILURE다.
- Transport b327: run43067343703의 admin/public frontend job은 각각 SUCCESS, backend pytest는 관찰 시 in_progress, live-e2e SKIPPED다. 중앙 policy43067344641 FAILURE.
- Map925·Pinviada425: 해당 API에서 workflow run 목록은 빈 값. Map e4의 새 CI는 부모 전달 상태이며 원925 CI로 바꾸어 쓰지 않는다.

중앙 main에 새 정책 데이터가 없다는 부모의 공통 선행 설명과 앱 개별 CI를 구분한다. Manager DNS 실패까지 같은 중앙 policy 실패로 묶지 않는다. foundation merge 이후 정확한 소비자 pin/CI 재수용이 필요하며 이 원문이 rerun·merge·배포를 실행하지 않는다.

Manager 현재 새 backend/public release-candidate 작업은 승인 대상4f frontend와 별개다. Map의 정식 UI-only 배포 경로·catalog/CLI 수용도 별도 gate다. 해당 미완 작업을 이번4f source PASS로 승인하지 않는다.

## 9. 마무리와 범위

Weather/Manager/Transport에서 본 담당 범위의 신규 source finding은 없다. Geo/Map/Concierge의 P2는 각각 명시한 범위로 OPEN이며 미해결 P0/P1로 부풀리지 않는다. Pinvi는 실제 미해결 계약과 부모의 no-approval 지시 때문에 BLOCK으로 남긴다.

새 Scope/공통 C10·미래 앱 source·policy delta는 아직 승인하지 않았다. 그 검토는 별도 immutable input/raw에서 수행한다. 이전 원문과 manifest는 그대로 보존했고 구현 source/모듈/lock·타인 cache를 수정하지 않았다. 모든 앱의 실제 API·DB·운영 lifecycle과 이미지 배포도 실행하지 않았다.

**Geo CONDITIONAL / Map CONDITIONAL / Weather PASS / Concierge CONDITIONAL / Manager PASS / Pinvi BLOCK / Transport PASS.**
**전체 BLOCK; 신규 P2 세 건 + 사전 공개 재현 P2 한 건 OPEN.**
