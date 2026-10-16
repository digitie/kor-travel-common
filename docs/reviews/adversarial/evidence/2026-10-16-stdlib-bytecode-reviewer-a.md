# Common37 최종 immutable 독립 검토 A

- 최종 HEAD 344d91c0eec4b605e007e61ce248693a729d692d, 기준200a350101665f44246422c7102c087fdfb3222e.
- 판정 SOURCE_PASS / 열린 P0·P1·P2 0. 범위 FULL5 = 선행 FULL4 + 최종 manifest1 전체 delta.
- 동일 manifest: docs/reviews/adversarial/evidence/2026-10-16-stdlib-bytecode-manifest.md / SHA c4d6b8b0bfa927cafd42591a622174cb25b6c22d763736034e6dadf09e705e18.
- 요청은 root가 보낸 Common37 explicit-build-only/stdlib/checked-hash/workers1/cache containment/exclusions/error/build-tool effectiveness 독립 FULL 요청과 새0845857 및 최종344d91 대상 갱신 메시지다. 상대 D 원문·모형 미열람, 저자 모형 미열람.

## 최종 delta

git object 직접 비교로 parent0845857→344d91은 manifest1개58줄만 추가됐음을 확인했다. helper/tests/가이드/T319 네 blob 및 기존 __init__/pyproject가 선행 격리 archive와 SHA exact다. helper SHA b07c7f94565147f619bffba7f1f9871106c0ee07d3683974393d596ffda5d266. base→084 전체 diff SHA9949db4a1fda6080b660cec21fb02207967629dd54608a64b9b6841434460791도 manifest와 일치한다.

manifest 전체를 읽어 explicit build-only, stdlib 범위, checked-hash optimize0 worker1, fail-closed/부분 pyc 보존, 동시 writer sandbox 아님, 기존 runtime 불변·소비자 성능 NOT_RUN 계약이 선행 검토와 같음을 확인했다. 저자 full476·wheel·docs의 실행 범위를 운영SDK/소비자 효과로 승격하지 않으며 원 docs 실패와 skip도 별도 표기한다. 저자 검증 수를 독립 실행 수로 합산하지 않는다. 새 manifest에는 source 동작·활성화 전제 완화가 없다.

## 계승한 직접 실행

선행 원문 common37-build-bytecode-review-a-r1-20261016.md SHA2e8255102a80f15b14eca883cc788f9a946f37e51ac2db79c84f62b678cb801e의 FULL4와 독립 actual-function tiny fixture22조건(각 Python3.11.15/3.13.14/3.14.4), archive 신규pytest26 PASS, ruff·diff check PASS를 계승한다. 제품 bytes 불변이므로 같은 시험을 manifest 추가만으로 반복하지 않았다. 명령 python3의 실제 버전3.14를 초기 파일명 py311로 잘못 표기한 원문은 보존하고 JSON actualversion으로 구분했으며 별도 real-py311 결과를 확인했다.

실제 stdlib 컴파일·운영·SSH·DB·Docker·SDK·provider·소비자 빌드/성능은 NOT_RUN. 제품/저자 checkout 수정0, 모든 소유 도구 terminal. 이미지 채택 시 동일 interpreter·최종 pyc/hash/optimization mode·Config/Env와 실제 cold/warm 효과를 별도 검증해야 한다.
