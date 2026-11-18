# Common PR68 — Reviewer A 독립 원본 검토

- 실행 ID: reviewer-a-f571767711f5-e88f0ee10006
- 역할: A — 컴포넌트 동작·접근성·반응형 layout·회귀 타당성
- 시작 등록 시각: 2026-11-18 13:19:23 UTC
- 종료 시각: 2026-11-18 13:24:47 UTC
- base: 55e3e95c9362b64bbeaddf8abaac0247f0a0df6f
- head 및 시작/종료 HEAD: f571767711f5e0f7010e070f3c426ed578aacaeb
- manifest: /home/digitie/dev/odroid-disk-remediation-20261117/common-virtual-table-overflow-qa/review-manifest.json
- manifest SHA256(시작·종료 동일): dab874135155a307c2cfd038f7768159a05cef87622df716cb0f92c4b57e61b2
- 격리: commit object-only. source 본문은 고정 hash의 git show/diff로만 읽음.
- 시작·종료 status --porcelain=v1: 빈 출력(clean).
- 현재 PR68 상대 reviewer 원문/중간 결과 열람·finding 교환 없음.
- source 수정·설치·브라우저/전체 suite 재실행·운영 호출 없음.

## 판정

PASS — Reviewer A 범위에서 actionable P0/P1/P2/P3 finding 없음.
이는 common canonical main-merge artifact의 발행·소비자 채택·운영 수용 완료 판정이 아니다.
상대 reviewer와 부모 merge/release gate는 별도다.

| 등급 | finding 수 |
| --- | ---: |
| P0 | 0 |
| P1 | 0 |
| P2 | 0 |
| P3 | 0 |

## 확인한 동작과 공격 시나리오

1. 좁은 grid의 intrinsic min-width:auto: 실제 제품 변경은
   packages/ui/src/virtual-table.tsx:595의 루트 min-w-0 한 줄이다. 내부 TableSurface는
   table.tsx:15-28의 w-full/overflow-x-auto 표면을 유지하므로 outer root가 grid 폭으로
   줄고 수평 이동은 내부 표면이 맡는다. 폭100% 강제나 소비자 전용 CSS를 추가하지 않았다.
2. 바깥 clipping으로 가짜 PASS: browser.spec.ts:17-38은 body/main/right 폭과
   scrollWidth>clientWidth를 검사하고 scrollLeft>0 및 실제 table x 이동을 함께 요구한다.
   html/body overflow-x:clip만 붙이거나 내부 scroller를 intrinsic 폭으로 남기는 변형으로
   회귀를 가릴 수 있는 시험 구조가 아니다. producer RED의 모바일2 FAIL/desktop2 PASS는
   증거 문서에서 읽었으며 reviewer가 새로 실행한 결과로 세지 않는다.
3. 일반/가상 표와 desktop:375/1280 두 폭×semantic/virtualized4조합, desktop fill,
   검색 후 마지막80번째 행 접근, 가상 행 수와 sticky header 위치·pageerror를 검사한다.
   min-width 축소가 column 데이터·정렬·행 identity·virtualizer 상태를 바꾸는 코드는 없다.
4. 접근성/키보드 표면: table/caption/aria-label·row/colcount·aria-sort와 row key handler,
   scroller의 기본 tabIndex0/role group/접근성 이름은 변경되지 않았다. focus ring의 inset
   처리와 bulk action flex-wrap도 유지한다. 새 overflow:hidden으로 콘텐츠·focus를 자르지 않는다.
5. Tailwind 누락/원본 import 우회: smoke app globals.css의 @source는 설치 UI dist를
   탐지한다. docs.yml:252-267은 실제 npm pack → 별도 임시 설치 트리 → webpack/Turbopack
   build → 새 spec이 포함된 playwright.radix.config를 실행한다. source-only import로
   누락된 배포 class를 대신 공급하는 경로가 아니다.
6. 같은 버전 다른 bytes: UI0.2.2/tokens0.1.3/toast0.1.2와 UI의 tokens exact peer,
   versions.json·workspace lock·세 내장 dependency-policy가 일치함을 객체에서 비교했다.
   tokens/toast 변경 파일은 package.json/policy뿐이고 runtime/CSS·기존 tgz 변경은 없다.
   일반 peer/산출물 심층 감사는 B 범위이며 canonical merge artifact는 부모 후속이다.
7. 회귀 gate 약화/문서로 실행 위장: validator·guard·CI workflow 변경은 diff에 없다.
   T-416 제목, T-419 제목/종료 선행, tasks-done의 정합 변경은 기존 T-417에 의한 대상 없음
   종료를 유지한다. T-025나 소비자 재vendor를 새로 실행했다고 닫지 않는다.

## 읽거나 실행한 검증

- manifest hash, 두 commit object 존재, 시작·종료 HEAD/clean,23 changed path==manifest scope,
  git diff --check를 로컬 실행했다.
- registry/package/lock/embedded-policy의 새3개 버전과 UI exact tokens peer를 JSON으로
  객체에서 대조했다. frontend-dependencies와 내장3 policy는 byte 동일하다.
- 사용자 제공 immutable manifest의 정확 head CI green을 입력 사실로 사용했다.
  지정된 producer exact-head-packages-ci.json에서 같은 head/source SHA·packages success·
  unit101/browser69·candidate artifact14429203002 연결을 읽었다. reviewer 실행으로 합산하지 않는다.
- AGENTS.md, docs/README.md, docs/resume.md, runbook §5.1~5.4와 review archive의 형식
  인덱스를 참조했다. 현재 상대 검토서 및 역사 review 원문은 열지 않았다.
- 추가 문맥: packages/ui/src/table.tsx, smoke next-app/app/globals.css,
  .github/workflows/docs.yml:237-271.

## 실제 확인한 변경 파일

- CHANGELOG.md
- docs/evidence/virtual-table-grid-overflow.md
- docs/journal.md
- docs/resume.md
- docs/standards/frontend-libraries.md
- docs/tasks-done.md
- docs/tasks/T-416-map-exact-node-npm-pin-decision.md
- docs/tasks/T-419-map-ui-tokens-revendor-on-t025.md
- frontend-dependencies.json
- package-lock.json
- packages/toast/dependency-policy.json
- packages/toast/package.json
- packages/tokens/dependency-policy.json
- packages/tokens/package.json
- packages/ui/dependency-policy.json
- packages/ui/package.json
- packages/ui/smoke/next-app/app/virtual-table-contracts/page.tsx
- packages/ui/smoke/next-app/package-lock.json
- packages/ui/smoke/next-app/package.json
- packages/ui/smoke/playwright.radix.config.ts
- packages/ui/smoke/virtual-table-browser.spec.ts
- packages/ui/src/virtual-table.tsx
- versions.json

## 한계와 남은 gate

- object-only 검토이므로 새 npm 설치/build/browser/axe·screen reader·touch/RTL/zoom을
  실행하지 않았다(NOT_RUN: 지정된 독립 소스 검토 범위).375/1280 밖 모든 폭/브라우저의
  시각 수용을 이 결과로 주장하지 않는다.
- canonical main-merge artifact와 SOURCE_SHA/SHA256SUMS/SRI 검산, 네 소비 표면의
  UI/tokens/Toast 버전/설치/실제 화면 채택은 부모가 수행한다.
- exact-head-packages-ci.json과 manifest는 producer evidence이며 새 독립 CI 재실행은 없다.
- Weather RO catalog proof는 수정하지 않았고 후속 Weather 조사를 실행하지 않았다.

## 요청 원문

아래는 독립 범위·격리·금지를 고정하기 위한 사용자 원문 인용이다.

Independent bounded review of Common PR68. SAME immutable manifest /home/digitie/dev/odroid-disk-remediation-20261117/common-virtual-table-overflow-qa/review-manifest.json SHA256 dab874135155a307c2cfd038f7768159a05cef87622df716cb0f92c4b57e61b2; base55e3e95c9362b64bbeaddf8abaac0247f0a0df6f headf571767711f5e0f7010e070f3c426ed578aacaeb. Repo /home/digitie/dev/odroid-disk-remediation-20261117/common-virtual-table-overflow-source. Object-only git show/diff isolation; no source edits, no installs or broad audit. Read AGENTS141/runbook review relevant; verify objects+clean. Scope min-w-0 VirtualTable fix, regression proof, ui0.2.2/tokens0.1.3/toast0.1.2 immutable bumps+versions.json+three inherited doc metadata repairs. All exact-head CIs green; don't rerun full suite. Do not read other reviewer output or exchange findings. Save original review under /home/digitie/dev/odroid-disk-remediation-20261117/common-virtual-table-overflow-qa/ independent reviewer file. Include execution id/times/head/manifest/isolation/checked files/attack cases/limits/P0-P3 findings/PASS|CONDITIONAL|BLOCK. Aim one bounded pass within minutes; source not change. You are Reviewer A: component behavior/accessibility/responsive layout/regression validity. Save reviewer-a.md. Weather257 has merged e6a5676194eda2cc9b9ade6d010bf66704f949d1; preserve RO artifact catalog proof, pause further Weather investigation for this bounded review.
