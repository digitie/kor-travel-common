# Common PR68 독립 적대적 리뷰 — Reviewer B

- 실행 ID: bf7452fc-2743-45e7-a46f-5d64e1032d70
- 역할: B — 소비자 호환성·불변 dist/버전 레지스트리·pack 자산·문서 종료 정합
- 시작 UTC: 2026-11-18T13:19:02.301489+00:00
- 검토 종료 UTC: 2026-11-18T13:21:13.194717+00:00
- base: 55e3e95c9362b64bbeaddf8abaac0247f0a0df6f
- head: f571767711f5e0f7010e070f3c426ed578aacaeb
- manifest: /home/digitie/dev/odroid-disk-remediation-20261117/common-virtual-table-overflow-qa/review-manifest.json
- manifest SHA256: dab874135155a307c2cfd038f7768159a05cef87622df716cb0f92c4b57e61b2
- 격리: commit object-only. 소스는 git show/git diff/ls-tree로만 읽었다. git --no-optional-locks를 사용했고 checkout/reset/install/build/소스 수정을 하지 않았다.
- 시작·종료 HEAD 모두 manifest head와 같고 status --porcelain=v1 --untracked-files=normal 출력은 모두 비었다. manifest 해시도 종료 시 다시 일치했다.
- 다른 리뷰어 파일/결과를 열거나 finding을 교환하지 않았다. 문서 라우터·review archive README의 절차 규칙만 참조했다.

## 판정

**PASS**

이 고정 diff에서 새 P0/P1/P2/P3 결함을 찾지 못했다. PR 검토 판정이며 정식 릴리스·소비자 채택·실배포 완료 판정이 아니다. main 병합 artifact의 실제 bytes/SOURCE_SHA/SHA256SUMS/SRI 확인과 후속 catalog 동결은 부모의 남은 단계다.

| 심각도 | finding |
| --- | --- |
| P0 | 없음 |
| P1 | 없음 |
| P2 | 없음 |
| P3 | 없음 |

## 확인 결과와 공격한 경우

1. **모바일 수정이 공개 API 또는 다른 소비자 동작을 바꾸는 경우.** packages/ui/src/virtual-table.tsx:595의 루트 클래스에 min-w-0만 추가됐다. base 전체 파일에 해당 단일 치환을 적용한 bytes가 head 전체 파일과 정확히 같음을 메모리에서 확인했다. props·export·슬롯·정렬·가상화 기본값·inner scroll/sticky 구조는 그대로다. 이 클래스는 intrinsic min-width 때문에 grid item이 내부 scroller까지 늘어나는 원인과 일치한다.

2. **UI만 올리고 tokens peer/registry/lock/내장 정책이 옛 버전에 남는 경우.** UI0.2.2·tokens0.1.3·toast0.1.2가 각각 package.json, versions.json axes.recommended, frontend-dependencies.json, root workspace lock에서 일치한다. UI의 exact tokens peer와 그 lock도 0.1.3이다. 내장 policy 세 사본은 생성 정본과 byte 동일하다. root lock의 구조적 변경은 세 package version과 UI tokens peer 네 경로뿐이다. policy의 구조적 변경도 세 version 경로뿐이다.

3. **tokens/toast 같은 버전의 새 bytes 재발행 또는 불필요한 런타임 변경.** 두 패키지는 package.json과 dependency-policy.json만 변경됐다. package.json에서는 version 외 값이 같다. policy bytes가 실제 바뀌고 두 패키지의 files에 그 JSON이 포함되므로 patch bump가 필요하며 적용됐다. tokens CSS·생성 입력·toast index.js/index.d.ts·export/dependency/license/file allowlist에는 변경이 없다. 기존 공개 자산을 덮는 파일 변경은 없고 frontend-artifacts.json 전체 bytes는 base와 같다.

4. **새 smoke가 옛 tarball/peer를 검사하거나 overflow:clip만으로 거짓 성공하는 경우.** smoke manifest/lock의 UI0.2.2·tokens0.1.3 file 경로, version, resolved, SRI 존재와 peer를 확인했다. fixture는 실제 공개 VirtualTable import를 쓰고 375/1280×일반/가상 네 경우를 만든다. spec:18–41은 body/main 폭뿐 아니라 scroller client/scroll 폭과 scrollLeft 및 실제 table x 이동을 검사하므로 화면 clip만으로 통과하는 조건을 피한다. 이어 sticky header·virtual row count·RHF와 무관한 폼 검색 유지·pageerror를 검사한다. 새 spec은 기존 packed Next Playwright testMatch에 포함된다. 문서의 실제 RED 2 FAIL/2 PASS→GREEN 4 PASS와 서버 환경 실패를 구분한 설명도 읽었다. 이 리뷰에서 브라우저를 재실행한 것은 아니다.

5. **후보 pack을 이미 main 정본으로 채택하는 경우.** exact-head-packages-ci.json의 head/run/job, SOURCE_SHA 로그와 후보 artifact14429203002를 대조했다. docs run44307749532/job134814414304는 unit101·browser69 PASS와 정확 head 이름의 pack 업로드를 기록한다. manifest도 candidateOnly=true 및 merged=false다. 구 catalog 보존은 새 release/catalog 동결 이전의 의도된 경계이며 이 PR이 새 SRI를 소비자 정본이라고 주장하지 않는다. 이전 head05eba117의 로컬 UI SHA256은 문서에서 그 시점의 기록으로 분명히 구분돼 있다. 실제 소비자는 병합 후 main pack과 후속 canonical catalog/policy 조합을 검증해 받아야 하며 PR 후보/초기 로컬 pack을 사용하면 안 된다.

6. **완료하지 않은 작업을 metadata 수정으로 완료 처리하는 경우.** T-416 상세 제목을 기존 채택 결정/완료 원장과 맞추고, T-419 상세 제목·원장의 predecessor를 대상 없음 종료 근거 T-417로 맞췄다. T-419 본문은 재vendor 미실행과 T-025 일반 채택의 후속 경계를 보존한다. 실제 docs/tasks/T-025-decouple-embedded-policy.md는 base/head byte 동일(SHA256 dbb885d84bdb6940913159691ccba3455404c502a293f8f660d3d1fd3bdd0a18)이며 validator·guard 코드도 변경되지 않았다. ae2124e3d6ff5b813034956918623ba2391e365f→head의 packages/versions.json/frontend-dependencies.json/package-lock.json diff도 비어 있다. 최종 metadata 수리가 제품 pack 입력을 다시 바꾸지 않았다.

## 읽거나 실행한 검증

- AGENTS.md(독립 리뷰 규칙 포함), docs/README.md, docs/resume.md 변경 부분, docs/runbooks/agent-workflow.md §5, docs/runbooks/release.md 관련 릴리스/자산 원칙, docs/reviews/README.md 절차 규칙.
- git cat-file로 base/head commit 객체 확인; git diff --name-only 집합과 manifest.scope 23개 정확 일치 확인.
- Python 표준 라이브러리로 git show bytes/JSON을 메모리에서 대조했다. repository 스크립트 실행이나 파일 생성 없이 axis/lock/peer/policy/scope/단일 런타임 치환을 assert했다.
- 정확-head CI green은 제공 manifest와 기존 exact-head pack 증거를 사용했다. full suite를 재실행하지 않았다.
- GitHub plugin의 artifact 단일 metadata GET은 허용 endpoint 제한으로 거부됐다. 따라서 원격 metadata/digest 독립 확인은 완료로 세지 않는다. gh fallback·download·설치는 하지 않았다.

## checked files

manifest의 다음 23개를 모두 immutable diff로 확인했다.

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

보조 object 대조: frontend-artifacts.json, tools/validate_plan.py, tools/check_frontend_dependencies.mjs, tools/check_node_toolchain.mjs, docs/tasks/T-025-decouple-embedded-policy.md. 실행 증거는 명시된 exact-head-packages-ci.json만 읽었다.

## 한계와 남은 단계

- 실제 후보 ZIP/tarball payload를 내려받거나 npm pack을 새로 만들지 않았다. smoke lock의 SRI를 실제 candidate tgz에 직접 재해시한 결과로 주장하지 않는다.
- tokens/toast tar entry의 두 파일만 달라졌다는 기존 evidence를 읽었고 source 변경 범위를 독립 확인했다. 실제 tar entry 전체 bytes 재대조는 이번 object-only 검토에서 NOT_RUN이다.
- 실제 소비자 build/모바일 장치/운영 UI·Node·이미지·auth·배포는 NOT_RUN(범위 밖). canonical main pack과 catalog가 확정될 때까지 adoption은 대기 상태다.
- CI 실행 순서나 폭넓은 저장소 감사는 하지 않았다. 소스 수정·install·전체 시험 재실행 없음.
- 종료 후 허용된 유일한 쓰기는 이 reviewer-b.md 원본 저장이다. 후속 adoption helper 프로토콜 수정은 이 고정 리뷰와 별도 작업으로 취급한다.

## 전달된 리뷰 요청 원문

아래는 원문 인용이며 영어는 사용자 요청 보존을 위한 것이다.

> Independent bounded review of Common PR68. SAME immutable manifest /home/digitie/dev/odroid-disk-remediation-20261117/common-virtual-table-overflow-qa/review-manifest.json SHA256 dab874135155a307c2cfd038f7768159a05cef87622df716cb0f92c4b57e61b2; base55e3e95c9362b64bbeaddf8abaac0247f0a0df6f headf571767711f5e0f7010e070f3c426ed578aacaeb. Repo /home/digitie/dev/odroid-disk-remediation-20261117/common-virtual-table-overflow-source. Object-only git show/diff isolation; no source edits, no installs or broad audit. Read AGENTS141/runbook review relevant; verify objects+clean. Scope min-w-0 VirtualTable fix, regression proof, ui0.2.2/tokens0.1.3/toast0.1.2 immutable bumps+versions.json+three inherited doc metadata repairs. All exact-head CIs green; don't rerun full suite. Do not read other reviewer output or exchange findings. Save original review under /home/digitie/dev/odroid-disk-remediation-20261117/common-virtual-table-overflow-qa/ independent reviewer file. Include execution id/times/head/manifest/isolation/checked files/attack cases/limits/P0-P3 findings/PASS|CONDITIONAL|BLOCK. Aim one bounded pass within minutes; source not change. You are Reviewer B: consumer compatibility/immutable dist/version registry/pack artifacts/document closure. Save reviewer-b.md. Latest release versions changed to UI0.2.2 tokens0.1.3 toast0.1.2; adoption remains waiting actual main canonical pack. Pause prep briefly for this bounded review.
