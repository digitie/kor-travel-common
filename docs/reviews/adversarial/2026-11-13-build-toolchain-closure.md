# Node/npm 도구 선택 guard의 반복 검토와 closure

[PR51](https://github.com/digitie/kor-travel-common/pull/51)의 제품 기준선은 941d18408c82532e4dc0145daf2f6b3228fd4d4b, tree 7f6684127ee884d0ab98469c15688c23b4c2044f다.
같은 원 A/Mill과 원 B/Epicurus가 매 회차 동일 불변 manifest를 독립 검토했다. 최종 후보5는 **두 bounded SOURCE PASS·신규0·미해결0**이며 자기 지적은 각각 원 reviewer가 재확인했다. 이 문서는 결과·disposition·출처만 정산하며 새 규범이나 source 변경을 포함하지 않는다.

## 원문과 동일 입력

| 입력·source | 원 A | 원 B | 같은 manifest | 해당 source의 실행·CI |
|---|---|---|---|---|
| c4cc · c4cc787 | [A BLOCK](evidence/2026-11-13-build-toolchain/review-A-common-build-rules-c4cc-1.md) | [B BLOCK](evidence/2026-11-13-build-toolchain/review-B-common-build-rules-c4cc-1.md) | [동일 입력](evidence/2026-11-13-build-toolchain/manifest-c4cc.json) | 47 PASS · 4 workflow/15 job SUCCESS |
| e1d0 · e1d0f01 | [A BLOCK](evidence/2026-11-13-build-toolchain/review-A-common-build-rules-e1d0-2.md) | [B BLOCK](evidence/2026-11-13-build-toolchain/review-B-common-build-rules-e1d0-2.md) | [동일 입력](evidence/2026-11-13-build-toolchain/manifest-e1d0.json) | 62 PASS · 4 workflow/15 job SUCCESS |
| 404a · 404a586 | [A BLOCK](evidence/2026-11-13-build-toolchain/review-A-common-build-rules-404a-3.md) | [B BLOCK](evidence/2026-11-13-build-toolchain/review-B-common-build-rules-404a-3.md) | [동일 입력](evidence/2026-11-13-build-toolchain/manifest-404a.json) | 76 PASS · 4 workflow/15 job SUCCESS |
| 8a2c · 8a2c7da | [A BLOCK](evidence/2026-11-13-build-toolchain/review-A-common-build-rules-8a2c-4.md) | [B CONDITIONAL](evidence/2026-11-13-build-toolchain/review-B-common-build-rules-8a2c-4.md) | [동일 입력](evidence/2026-11-13-build-toolchain/manifest-8a2c.json) | 81 PASS · 4 workflow/15 job SUCCESS |
| 941d · 941d184 | [A SOURCE_PASS](evidence/2026-11-13-build-toolchain/reviewer-A-941d-public-note.md) | [B SOURCE_PASS](evidence/2026-11-13-build-toolchain/reviewer-B-941d-public-note.md) | [동일 입력](evidence/2026-11-13-build-toolchain/manifest-941d.json) | 90 PASS · 4 workflow/15 job SUCCESS |

[원문 신원·보존 원장](evidence/2026-11-13-build-toolchain/original-receipts.json)에 원문10개와 manifest5개의 bytes/SHA256을 고정했다.
이전 원문8개는 byte 그대로 공개한다. 최종 원문2개는 진행 중인 별도 프로젝트 검토 관찰·비공개 로컬 수집 참조를 함께 담으므로 원본 SHA와 한국어 메모로 연결한다. 마스킹한 문서를 원문이라고 내놓지 않는다. 원본 영어·한자 표현은 인용으로 보존하며 이 보고서가 한국어 적용 메모다.
각 원문 및 manifest에 남은 당시 pending·NOT_RUN·부분 CI 관찰은 역사적 사실이다. 현재 최종 PASS나 뒤늦은 CI 성공으로 수정하지 않는다.

## 지적별 최종 disposition

| 원 reviewer 지적 | 최종 | 조치·재확인 범위 |
|---|---|---|
| A P2-01 / B P2-01·03 | FIXED | 공식 ini7의 전역 typed boolean으로 force·strict, 인용 key·section shadow·중복·비boolean을 구분한다. |
| A P2-02 / B P1-01 | FIXED | strict 토큰 존재만으로 승인하지 않고 해제·모순·분리 false를 shell/JSON에서 거부한다. |
| A P2-03 | FIXED | 미지원 heredoc·nondefault escape는 추론하지 않고 거부한다. |
| A P2-04 | FIXED | pin 후에도 npm selector·다른 global install·package/location/prefix 재선택을 거부한다. |
| B P2-02 | FIXED | CLI 직접/alias/preserve-main 실행과 API import 무자동 실행을 구분한다. |
| B P2-04 | FIXED | 기본 registry를 physical checker 경로에 고정하며 명시 override는 유지한다. |
| A P2-05 / B P2-05 | FIXED | 공식 shell token으로 npm 구간 선택 전에 전체 RUN의 지원 && 외 제어 연산자를 거부한다. |
| A P2-06 / B P1-02·P2-06 | FIXED | 실행 파일과 cache·node·echo 등의 data를 구분한다. 절대 npm CLI·wrapper·동적 선택의 기존 거부를 유지한다. |

각 ID는 원 reviewer의 이름공간을 따른다. 겹치는 원인이나 여러 회차의 같은 payload를 새로운 고유 결함·테스트 총수로 합산하지 않는다.
A는 자기 여섯 지적, B는 자기 여덟 지적을 최종 FIXED 또는 FIXED 유지로 닫았다. 이전 심각도·BLOCK·CONDITIONAL은 원문 그대로다.
이 범위의 P0/P1 미해결·P2 미해결은0이며 임의 DEFERRED로 닫은 항목은 없다.

## 실행·의존성·CI의 분리

소유자 정본 실행은 Node22.23.1/npm12.0.1에서 runtime gate와 최종90개 모두 PASS/0 SKIP다.
[입력22개·로그4개 결합 증거](evidence/2026-11-13-build-toolchain/runtime90-source-proof.json)는 source7개와 설치 dependency15개(ini4·shell-quote11)의 SHA를 제품 Git bytes와 연결한다.
원 A/B의 직접 구조 검사는 WSL Node22.22.2의 exact90이며, 별도 자체 suite는 각 최종 메모의 범위대로 기록한다. 이를 정본 환경 재실행이나 중복 없는 합계로 확대하지 않는다.
개발 r1/r2, 81 PASS/9 FAIL의 변경 전 반례와 이전 회차 원문은 private 실행 보관소에서 그대로 유지한다.

추가 의존성은 Common private root의 ini7.0.0(ISC)와 shell-quote1.12.0(MIT) 두 도구뿐이다.
[INI 출처](evidence/2026-11-13-build-toolchain/ini-dependency-proof.json)와 [shell-quote SRI·배포11파일](evidence/2026-11-13-build-toolchain/shell-quote-dependency-proof.json)을 연결했다.
새 shell-quote 선언·node를 제외한 기존 lock JSON은 deep-equal이며 소비자/public dependency에 parser를 강제하지 않았다.
[공개193파일 증거](evidence/2026-11-13-build-toolchain/public193-invariance-proof.json)는 packages·vendor·공개 frontend data가 기존 기준선과 같음을 보인다. C11 7종 pack·65버전 정책은 재pack·재발행하지 않았다.
7개 실제 profile의 같은 입력 old/new 정적 대조는 수용됐지만 앱 전체 설치·새 이미지·native ABI·운영 승인은 아니다.

[CI 수집 정산](evidence/2026-11-13-build-toolchain/ci-results.json)은 각5개 source의 실제4 workflow·15 job, attempt, 로그 해시와 synthetic checkout 전체 tree bridge를 구분한다.
최종941d는 모든 job attempt1 SUCCESS이고 Windows 포함 builtin90/0 SKIP, tokens9·UI101·policy175와 packed browser65가 통과했다.
Python3.11·3.13은 각각661 PASS, docs·Ubuntu 도구는 각각400 run/397 PASS/3 SKIP, Windows 도구는400 run/398 PASS/2 SKIP다.
selftest의 task 원장2step SKIP도 따로 유지한다. report 모드 대비 fixture의 job 성공을 모든 pair 통과로 바꾸지 않는다.
최종 소유자 수집45개 raw·15개 job log의 SHA/bytes를 검산했으며, 수집 receipt SHA는 ccab2c055cab87f2148ce6bcbdcb60684320190ba5db3c430c881778b1081eac다.
941d CI synthetic e7d2611e7146a7658e13eb7ab6879145f1e8a16f의 전체 tree는 reviewed941d와 같다. 이전 source의 녹색 CI가 그때의 BLOCK을 소거한 것은 아니다.

## closure와 남은 gate

[agent workflow §5](../../runbooks/agent-workflow.md#5-전문-리뷰어-서브에이전트-2인-적대적-리뷰)와 [리뷰 기록 규칙](../README.md)에 따라 이 정산·원문 보존·index 한 행만의 closure는 같은 review를 재귀적으로 시작하지 않는다.
도구·규범·versions·package/lock·workflow·공개193 code bytes는 제품941d와 동일하게 유지한다.
최종 closure head의 실제 exact CI는 부모 push 뒤 별도로 관찰한다. 제품941d의4/15 성공만으로 closure CI나 PR merge를 이미 완료했다고 적지 않는다.

앱은 실제 merged Common code ref와 최종 functional workflow 경로를 연결하고 자기 source review·설치·build·image/runtime gate를 충족해야 한다.
이 정적 모델은 지정한 literal npm/npx·data utility와 opaque 정적 script 호출의 한정된 입력만 다룬다. 임의 script/Node helper/npm run 본문·전체 Docker 문법·실제 이미지 버전/ABI·운영 인증을 보증하지 않는다.
앱 배포·비밀·계정·native 실기기/EAS/store·Map 작업은 이 closure의 완료 범위가 아니며 추가 운영 실행은0이다. CI 순서/needs/fail-fast 감사·최적화는 마지막 별도 단계로 남긴다.
