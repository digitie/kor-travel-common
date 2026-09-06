# Phase 0 독립 적대적 리뷰 원본 — Reviewer B

- Review ID: 2026-09-06-phase0
- 실행 ID: `/root/reviewer_b`
- 전문 영역: 계획 DAG·순차 인계·숨은 선행·UI/Python 공개 계약·출처·외부 승인·정본 충돌
- 시작: 2026-09-06T18:00:06+09:00
- 종료: 2026-09-06T18:09:04+09:00
- Candidate 실제 관찰: `d3712a8c965c3193a5af13cacd6d22c603e0cfe4`
- Base: `b92fabeb1c96a11c1fc9507d93271c1ebeee09b0`
- Parent: `09104ed0fa7f8564936fbbc3b9c17057f86d3e7c`
- 격리: 지정된 `review-phase0-b` detached worktree. 시작·종료 `git rev-parse HEAD` 일치, `git status --porcelain=v1` 출력 모두 비어 있음.
- 원본 확정 시 상대 reviewer 보고서·finding을 읽거나 요청하지 않았다. 저장소 소스·정책·소비자 파일은 수정하지 않았다.
- 공통 입력: [manifest](2026-09-06-phase0-manifest.md) 전체를 읽었다.
- 최종 verdict: **BLOCK** — P1 6건, P2 2건. 실행한 기계 검사 통과는 아래 의미적 교착·계약 충돌을 검출하지 않는다.

## 전달받은 리뷰 요청

> Reviewer B로 독립 적대적 리뷰를 수행하세요. 공통 manifest는 F:/dev/kor-travel-common/docs/reviews/adversarial/evidence/2026-09-06-phase0-manifest.md 입니다. 반드시 전체를 읽고 그 요청을 따르세요. Immutable candidate d3712a8c965c3193a5af13cacd6d22c603e0cfe4, base b92fabeb1c96a11c1fc9507d93271c1ebeee09b0. 읽기/검증은 F:/dev/kor-travel-common-wt/review-phase0-b detached worktree에서만 합니다. 전문 영역: 계획 DAG/순차 인계/숨은 선행/UI·Python 공개 계약/출처·외부 승인·정본 충돌. 실제로 이 계획을 따라 다른 에이전트가 하나씩 실행할 때 교착이나 오승인·미실행 pass가 생기는지 공격하세요. 원본 evidence 소유 파일은 F:/dev/kor-travel-common/docs/reviews/adversarial/evidence/2026-09-06-phase0-reviewer-b.md 하나입니다. 이 파일만 작성하고 코드나 다른 문서를 수정하지 마세요. 다른 에이전트가 동시에 작업 중이므로 다른 편집을 되돌리지 말고 상대 reviewer 결과는 읽거나 요청하지 마세요. 실행 ID와 시각·hash·clean 상태·재현·검증 결과를 기록하며 최종 verdict와 finding 전부를 제출하세요. 추가 subagent를 생성하지 마세요. 보고서 작성 후 parent에게 완료와 핵심 finding을 알리세요.

## 검토 범위·검증 결과

먼저 AGENTS·docs/README·resume·T-013을 읽고, task 원장·작성 규칙·통합 계획·architecture 개요와 packages/style-delivery/consumers/adoption-readiness, agent-workflow §5·review template을 대조했다. finding 관련 T-003·T-005·T-010·T-020·T-021·T-101·T-103·T-109·T-201·T-203~T-206·T-212·T-213·T-302~T-307·T-310·T-401·T-420·T-422·T-453·T-472·T-483~T-486, ADR-004·005·007·011, backend-stack·ui-contract·licensing·release와 PROVENANCE를 확인했다. survey는 관련 canview·UI 근거의 필요한 절만 읽었고 전체 재조사는 하지 않았다.

| 실행 | 결과 |
|---|---|
| `python --version` | Python 3.14.3, Windows |
| `python -B -X utf8 tools/validate_document_links.py` | 문서 184개·local target 1648개·오류 0 |
| `python -B -X utf8 tools/validate_plan.py` | 상세 task 93개·오류 0; metadata/DAG만 검사 |
| `python -B -X utf8 -m unittest discover -s tests -p 'test_*.py'` | 57 tests, OK, skip 0 |
| `git diff --check b92fabeb1c96a11c1fc9507d93271c1ebeee09b0 HEAD` | 출력 없음, exit 0 |
| Python 메모리 내 순차 선택 시뮬레이션 | metadata에서 선행·우선순위를 추출해 기반→토큰→UI→Python→소비자→운영, P0→P3, ID 순으로 선택. 아래 B-P1-03 순서를 재현 |
| `rg`로 Python 0.2 릴리스 소유 task 제목 검색 | 0건. T-310은 명시적으로 범위 밖 |
| Base UI 공식 `useRender` 문서 조회 | 2026-09-06, 문서 표시 버전 1.8.0, `@base-ui/react/use-render` import 확인. B-P1-06 근거 |

Windows glob 인자를 직접 전달한 한 `rg` 호출(`docs/tasks/T-30*.md`)은 경로 문법 오류였다. 이후 실제 파일 경로와 디렉터리 검색으로 재확인했으며 실패한 검색을 성공 검증으로 세지 않았다.

NOT_RUN: Linux/WSL 직접 재실행, PR CI 원격 조회, 실물 패키지 빌드·tarball/wheel 설치, 소비자 빌드·e2e·시각 검증, 소비자 라이선스 승인·현재 원천 재조사. 패키지 구현·승인 자체의 부재는 finding이 아니다. 아래 항목은 그 부재를 해결할 실행 계획의 교착 또는 서로 다른 계약 지시를 대상으로 한다.

## B-P1-01 — L6를 적용할 T-420의 READY 전환이 이미 적용된 L6를 요구한다

- 위치: `docs/tasks/T-020-pinvi-license-l6.md:25`, `docs/tasks/T-420-pinvi-license-l6.md:6`, 같은 파일 `:10`, `:22`.
- 근거: T-420이 루트 LICENSE와 공개·라이선스 정합을 실제 pinvi PR에 반영한다. 그런데 T-020 구현 범위 3은 pinvi main의 GPL LICENSE 커밋 SHA를 기록하고 L6를 해제한 **뒤** T-420을 READY로 전환하라고 한다. T-420은 metadata에서도 T-020을 선행으로 둔다.
- 실패 시나리오: O-1에 공개 GPL 승인이 도착했지만 아직 pinvi main에 LICENSE가 없는 정상 초기 상태를 가정한다. 결정·요청 문서를 작성해도 명시된 READY 전환 조건을 충족할 수 없다. 그 조건을 만드는 유일한 작업 T-420은 시작하지 못한다. T-020을 결정 문서만으로 완료할 수 있다고 해석하더라도 `L6 해제 → T-420 READY` 지시는 여전히 역순이다.
- 영향: pinvi 모든 채택 트랙이 교착되거나, 이를 풀려고 실제 반영 전 L6를 해제하는 오승인이 생긴다. metadata DAG 검사는 이 본문 의존을 보지 못한다.
- 최소 수정: T-020 완료·T-420 READY는 사용자 결정과 검토된 요청 문서까지만 요구한다. L6의 코드 소비·추출 gate 해제는 T-420 merge SHA와 LICENSE/공개 문구/패키지 필드 정합 evidence를 확인한 뒤로 분리한다. 결정 승인과 라이선스 반영 완료를 서로 다른 상태로 기록한다.

## B-P1-02 — pinvi UI v0.1·v0.2를 한 task에 묶어 v0.2 릴리스와 숨은 순환이 남는다

- 위치: `docs/tasks/T-213-ui-v0-2-0-release.md:7`, `docs/tasks/T-422-pinvi-admin-ui.md:6`, `:21`, `:22`; `docs/plan/integration-plan.md:14`~`:18`.
- 근거: T-213의 pinvi rc 검증은 ui v0.1 채택(T-422) 위에서만 가능하다. T-422는 v0.1 PR A와 v0.2 PR B를 동시에 소유하고 선행에 T-213을 둔다. 통합 계획은 선행 완료 전 의존 작업을 시작하지 못하게 한다.
- 실패 시나리오: L6·tokens 채택은 완료, airport WIP는 외부 대기인 상태에서 pinvi를 두 번째 GPL 검증 소비자로 선택한다. T-213은 pinvi v0.1 채택을 기다리고, 그 PR A를 시작할 T-422는 T-213 정식 릴리스를 기다린다. 통합 계획 §4의 'rc 검증은 정식 채택 DONE을 요구하지 않음'은 T-213의 **이전 minor가 이미 채택되어 있어야 한다**는 조건을 제거하지 않는다. '착수 전에 하위 task로 분할'이라는 일반 규칙만으로는 현재 blocked task의 실행 가능한 선행이 생기지 않는다.
- 영향: 허용된 pinvi 경로로 v0.2를 발행할 수 없고, airport 대기까지 겹치면 UI 이후 트랙이 막힌다.
- 최소 수정: 지금 T-422a(v0.1, T-212·T-421 이후)와 T-422b(v0.2, T-213·T-422a 이후)를 만들고 T-213 검증 선행은 T-422a로 연결한다. 원장·상세·소비자 표를 함께 맞춘다.

## B-P1-03 — 정해 둔 순차 선택 규칙이 0.1 릴리스 전에 0.2 코드를 같은 패키지에 넣는다

- 위치: `docs/tasks.md:11`, `docs/plan/integration-plan.md:15`, `:20`; `docs/tasks/T-205-ui-button-error-panel.md:6`, `:10`; `docs/tasks/T-212-ui-v0-1-0-release.md:11`; `docs/tasks/T-306-settings-db-api-key.md:6`, `docs/tasks/T-307-request-id-and-metrics.md:6`; `docs/tasks/T-310-py-v0-1-0-release.md:10`, `:33`.
- 근거·재현: 외부 선행이 모두 충족되었다고 두고 원장 metadata의 DAG·우선순위로 정렬했다. UI 순서는 `T-201 → T-203 → T-204 → T-205 → T-206 → T-208 → T-212 → T-209 → T-210 → T-213 → T-211`, Python 순서는 `T-301 → T-302 → T-303 → T-304 → T-305 → T-306 → T-307 → T-309 → T-310 → T-308`이다. 이 순서는 명시된 선택 규칙을 준수한다.
- 실패 시나리오: 각 task의 PR을 정상적으로 반영한 뒤 다음 작업으로 이동하면 T-212를 시작할 때 이미 Button·overlay·DataTable이 같은 `packages/ui`에 존재한다. T-212가 요구하는 '소형 13종만 담은 0.1'을 현재 HEAD에서 pack할 수 없다. T-310도 명시적 1차 구성에 포함하지 않은 settings·db·request-id·metrics가 들어간 소스를 0.1 태그로 묶게 된다. 릴리스용 고정 소스 commit/별도 maintenance branch/내용물 선택 절차도 없다.
- 영향: 문서대로 태그를 만들면 릴리스 내용물·공개 계약·소비자 검증 범위가 불일치한다. 외부 검증 대기로 릴리스 task가 BLOCKED인 동안 다음 minor 구현을 진행할 때도 같은 문제가 생긴다.
- 최소 수정: 0.1 릴리스 완료를 다음 minor 구현의 명시 선행으로 두거나, 릴리스 task가 어떤 immutable 소스 commit을 어떤 branch에서 pack하는지 명시하고 그 기준선을 후속 구현과 분리한다. 숫자 순서 설명만 고치지 말고 선택 규칙으로 해당 순서를 실제 재현하는지 확인한다.

## B-P1-04 — Python 2차 모듈을 소비하도록 계획했지만 그것을 발행하는 task가 없다

- 위치: `docs/tasks/T-310-py-v0-1-0-release.md:10`, `:33`; `docs/tasks/T-484-pinvi-py-lock-export-drift.md:6`, `:22`, `:23`; `docs/tasks/T-485-concierge-py-first.md:6`, `:22`, `:23`; `docs/tasks/T-483-geo-py-second.md:6`, `:21`; `docs/tasks/T-486-ktdm-py-second.md:6`, `:22`.
- 근거: accepted ADR-011과 T-310은 0.1을 export·health·time·quality로 한정하며 request-id는 T-307의 2차 모듈이다. T-310은 `py-v0.2.0`을 명시적으로 범위 밖에 둔다. 93개 상세 task 중 이를 발행하는 소유 task가 없다.
- 실패 시나리오: T-310을 계약대로 완료해 0.1을 발행해도 T-484·T-485는 0.1 태그를 설치한 뒤 그 태그에 없는 `request_id`를 import하도록 지시한다. T-483·T-486은 구현 task 완료만 선행으로 두고 아직 발행 책임이 없는 `py-v0.2.x`를 설치한다. T-307을 나중에 merge해도 기존 immutable 0.1 태그에는 모듈이 생기지 않는다.
- 영향: 한 에이전트가 원장대로 완료해도 소비자 설치·import gate를 닫을 수 없다. 이미 발행한 0.1 태그 이동/재발행으로 우회하면 태그 불변 정책까지 깨진다.
- 최소 수정: 2차/3차 중 실제 첫 배포 범위를 결정한 Python 후속 릴리스 task를 추가한다. request-id 채택은 그 릴리스 선행과 정확한 태그로 이동하고, export만 먼저 가능한 부분은 하위 task로 분리한다. drift 워크플로(T-309) 사용 task의 배포 선행도 함께 명시한다.

## B-P1-05 — L6 대체 경로를 허용해도 필수 consumer-smoke는 pinvi 설치를 강제한다

- 위치: `docs/tasks/T-010-reusable-workflows-stage1.md:25`, `docs/tasks/T-109-tokens-v0-1-0-release.md:25`, `:42`; `docs/tasks/T-212-ui-v0-1-0-release.md:25`, `:50`; `docs/runbooks/release.md:103`; `docs/adr/004-gpl-3-0-or-later-and-provenance-gate.md:29`; `docs/tasks/T-420-pinvi-license-l6.md:10`, `:74`.
- 근거: L6 전에는 pinvi의 common 코드 소비가 차단되고, T-420은 pinvi 릴리스 검증을 airport로 바꾸도록 한다. 그러나 필수 consumer-smoke의 두 대상은 map admin·pinvi web으로 고정되어 있고, T-109는 그 두 pinned checkout에 rc tarball을 설치해 양쪽 빌드가 green이어야 한다. T-212도 airport 대체를 선택한 뒤 별도로 같은 고정 consumer-smoke green을 요구한다.
- 실패 시나리오: L6가 미결이어도 승인된 map·weather 토큰 검증 또는 map·airport UI 검증을 마쳤다. 현재 규칙대로라면 pinvi에 common을 설치해 G-LIC를 우회하거나, 설치를 생략하고 필수 검증을 green으로 해석하거나, 승인과 무관한 전체 릴리스를 L6 때문에 중단해야 한다.
- 영향: 사용자에게 보장한 'L6 대기 시 airport 대체'가 실제 발행 gate에서는 작동하지 않는다. 이는 법률 판단이 아니라 저장소가 스스로 정한 외부 승인·코드 소비 경계의 충돌이다.
- 최소 수정: consumer-smoke 대상은 승인 evidence가 있는 소비자 pin으로 선택하도록 정본을 고치고 tokens는 map·weather, UI는 map·승인된 pinvi 또는 airport 경로를 명시한다. L6 이전 pinvi를 검사했다면 설치 없는 기존 앱 진단과 패키지 소비 smoke를 서로 다른 결과로 기록하고 필수 gate를 대체하지 않도록 한다.

## B-P1-06 — 첫 UI 13종은 useRender가 필수인데 Base UI 의존 추가는 T-206까지 금지되어 있다

- 위치: `docs/tasks/T-201-ui-package-skeleton.md:22`, `docs/tasks/T-203-ui-small-components.md:17`, `:21`, `:51`, `docs/tasks/T-206-ui-overlay-table-checkbox.md:24`; `docs/architecture/packages.md:63`.
- 근거: T-201은 Base UI를 넣지 않고 'T-206에서 peer 추가'로 고정한다. T-203은 Badge·Input·Textarea·NativeSelect·Separator의 `useRender` 합성과 관련 테스트를 필수로 지정하지만 의존 추가는 없다. T-206은 T-203 이후에야 시작할 수 있다. Base UI 공식 문서의 `useRender`는 `@base-ui/react/use-render` import다([공식 useRender 문서](https://base-ui.com/react/utils/use-render), 2026-09-06 조회, 페이지 표시 버전 1.8.0, 문서 예시 103행). 1.6/1.8의 나머지 API 호환성은 이번에 검증하지 않았다.
- 실패 시나리오: T-201이 지정한 dependency/peer만 설치된 깨끗한 T-203 tarball 소비 환경에서 명시된 useRender 구현을 추가한다. helper 모듈을 resolve할 수 없고 첫 13종 빌드·설치 gate를 통과하지 못한다. 앱에 우연히 Base UI가 이미 설치되어 있거나 workspace hoist가 되어 있으면 누락을 가릴 수 있다.
- 영향: 첫 UI 배포 task가 후행 overlay task의 의존 설정을 요구한다. '비-overlay는 native 요소'라는 사실이 helper 패키지 의존이 없다는 뜻으로 잘못 적용됐다.
- 최소 수정: Base UI primitive 엔진 사용과 useRender helper 의존을 구분하고 T-203 또는 T-201에서 필요한 peer/dependency를 선언한다. T-206의 '처음 추가' 지침과 정본 표현을 맞추고 깨끗한 tarball 소비 fixture에서 dependency 완결성을 확인하도록 한다. 자체 helper로 바꾸려면 그것을 명시적으로 결정하고 render/ref/event 합성 계약을 보존해야 한다.

## B-P2-07 — Python 공개 import 경로와 구현 경로의 연결 책임이 없다

- 위치: `docs/architecture/packages.md:103`, `docs/standards/backend-stack.md:112`~`:115`; `docs/tasks/T-304-health-and-time.md:21`, `docs/tasks/T-307-request-id-and-metrics.md:22`; `docs/tasks/T-302-python-package-skeleton.md:25`~`:29`.
- 근거: architecture 공개 경로와 사용 예·소비자 task는 `kortravelcommon.health`, `kortravelcommon.request_id` 등을 사용한다. 구현 task는 `kortravelcommon/api/health.py`, `api/request_id.py`만 만들고, T-302는 프레임워크 의존 허용 예외를 `api` 등 하위 패키지에만 둔다. 최상위 public facade를 만들지, 공개 경로를 `.api.*`로 통일할지 어느 task에도 수용 기준이 없다.
- 실패 시나리오: T-304·T-307 구현을 지시한 경로대로 완료해 내부 단위 테스트가 통과해도 소비자 예시 import는 존재하지 않는다. 임의로 facade를 추가하면 T-302가 만든 import-linter 경계와 함께 다시 판단해야 한다.
- 영향: 패키지 실물 대조 전에 각 에이전트가 다른 공개 경로를 선택할 수 있다. 예시는 후보로 표시되어 있고 아직 실물이 없으므로 현재 런타임 실패로 단정하지 않고 P2로 판정한다.
- 최소 수정: T-302에 공개 import 경로 결정과 wheel 설치본의 해당 경로 import 검사를 수용 기준으로 넣고, T-304·T-307·소비자 task가 그 결정만 참조하도록 한다. facade 채택 시 import-linter에서 공개 facade와 내부 core를 명시적으로 구분한다.

## B-P2-08 — 독립 버전과 'tokens 같은 minor' 규칙이 UI 0.2의 peer 선택을 결정하지 못한다

- 위치: `docs/adr/005-release-channel-immutable-tags-semver-0x.md:16`, `docs/architecture/packages.md:13`, `:78`, `docs/runbooks/release.md:11`; `docs/tasks/T-201-ui-package-skeleton.md:22`, `docs/tasks/T-213-ui-v0-2-0-release.md:21`.
- 근거: 세 패키지는 독립 버전인 동시에 UI는 tokens의 '같은 minor'를 peer로 요구한다. T-201은 `~0.1.0`을 선언하지만 T-213의 0.2 peer 확정에는 tokens 범위가 없다. 계획의 토큰 발행은 0.1 하나뿐이다.
- 실패 시나리오: 'UI와 tokens의 minor 숫자가 같아야 한다'로 읽으면 UI 0.2 발행에 tokens 0.2가 필요한데 이를 소유한 task가 없다. '호환 가능한 tokens의 하나의 minor 범위에 고정한다'로 읽으면 UI 0.2 + tokens 0.1이 가능하지만 그 해석이 정본에 적혀 있지 않다.
- 영향: 서로 다른 에이전트가 필요 없는 tokens 릴리스를 만들거나 기존 ADR과 다르게 peer를 유지할 수 있다. 의미가 두 가지로 읽히는 계획 결함이므로 P2다.
- 최소 수정: 독립 버전의 의미와 UI 0.1/0.2 각각의 tokens 호환 minor를 구체적으로 결정한다. 숫자 동기화가 의도라면 tokens 0.2 릴리스 선행을 추가하고, 호환 범위 고정이 의도라면 accepted ADR의 후속 기록과 task에 그 의미를 명시한다.

## 반증한 위험·남은 불확실성

- 일반적인 rc 검증과 정식 채택 사이의 순환은 통합 계획 §4가 별도 외부 검증 요청으로 해소한다. 이 일반 규칙 자체를 finding으로 만들지 않았다. B-P1-02는 이전 minor의 정식 채택이 별도로 선행인 경로다.
- concierge·ktdm 토큰/Python task는 L8을 metadata 선행에서 빠뜨렸어도 상세 외부 선행에 명시하고 있다. 이 부분을 승인 우회로 보고하지 않았다.
- pinvi 확장 prop을 재구현한다는 T-203·T-206의 명시는 확인했다. 코드 복사 증거가 없어 L6 전 금지 원천 추출을 단정하지 않았다.
- 실물 없음·T-003 고지 도구 미완·T-005 실제 현재값 미등록은 resume와 후속 task가 미완으로 표시한다. 이 부재를 이번 PR의 숨겨진 성공 처리라고 주장하지 않는다.
- task의 구체적인 테스트 개수는 착수 시 재확인하라는 통합 계획과 함께 읽었다. 소비자 현재 테스트 수를 이번 실행값으로 재사용하지 않았다.
- 읽기·검증 종료 HEAD는 candidate와 일치하고 worktree는 clean이었다. 본 원본 외에 파일을 쓰지 않았다. P1 수정 후에는 새 immutable commit에서 원 finding과 전체 delta의 회귀를 다시 확인해야 한다.
