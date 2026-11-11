# 앱 최종 입력과 Manager UI 교체 기능의 독립 검토 기록

원 A/B는 같은 불변 입력을 각각 검토했고 구현에 참여하지 않았다. 각 원문과 실패를 보존하며 이후 조건 충족은 별도 기록한다. 아래 SOURCE PASS는 해당 소스 범위의 판정이며 운영 배포·로그인 수용과 구분한다.

| 입력 | 원 A | 원 B | 현재 판정 |
|---|---|---|---|
| C11 소비자1 | [원문](evidence/2026-11-12-review-A-consumers-c11-batch-1.md.txt) | [원문](evidence/2026-11-12-review-B-consumers-c11-batch-1.md.txt) | Geo·Map·Weather·Manager·Transport source/package PASS, 신규0 |
| C11 소비자2 | [원문](evidence/2026-11-12-review-A-consumers-c11-batch-2.md.txt) | [원문](evidence/2026-11-12-review-B-consumers-c11-batch-2.md.txt) | Concierge PASS. 당시 Pinvi 신규 지적은 원문 보존 |
| Pinvi528 후속 | [원문](evidence/2026-11-12-review-A-consumers-528-followup.md.txt) | [원문](evidence/2026-11-12-review-B-consumers-528-followup.md.txt) | 둘 다 PASS·신규0, provenance·dead-trigger 자기 지적 FIXED |
| Map7ce main 통합 | [원문](evidence/2026-11-12-review-A-map-c11-7ce-main-supplement.md.txt) | [원문](evidence/2026-11-12-review-B-map-c11-7ce-main-supplement.md.txt) | 둘 다 source-merge PASS·신규0. 정확 CI는 별도 |
| Transport4e25 test/docs | [원문](evidence/2026-11-12-review-A-transport-c11-4e25-supplement.md.txt) | [원문](evidence/2026-11-12-review-B-transport-c11-4e25-supplement.md.txt) | 둘 다 source/test PASS·신규0, 실제44개 브라우저 증거 수용. 정확 CI는 별도 |
| Manager SDK 입력1/df376 | [원문](evidence/2026-11-12-review-A-manager-component-ui-final-1.md.txt) | [원문](evidence/2026-11-12-review-B-manager-component-ui-final-1.md.txt) | 당시 SOURCE PASS. 소비자 운영 전제 후속은 입력2 |
| Manager SDK 입력2/71550 | [원문](evidence/2026-11-12-review-A-manager-component-ui-final-2.md.txt) | [원문](evidence/2026-11-12-review-B-manager-component-ui-final-2.md.txt) | 둘 다 BLOCK: raw 달러와 Compose 정규화 표현의 경계 결함 |
| Manager SDK 입력3/e798 | [원문](evidence/2026-11-12-review-A-manager-component-ui-final-3.md.txt) | [원문](evidence/2026-11-12-review-B-manager-component-ui-final-3.md.txt) | 둘 다 PASS·신규0, 자기 달러 지적 FIXED |
| Manager Mounts/ac4 | [원문](evidence/2026-11-12-review-A-manager-mount-order-final-1.md.txt) | [원문](evidence/2026-11-12-review-B-manager-mount-order-final-1.md.txt) | 둘 다 SOURCE PASS·신규0, 순서 오탐 FIXED·전체 객체/중복/부재/null 보호 유지 |

원문은 bytes가 같은 .md.txt로 보존한다. 원문 안의 상대 evidence 경로는 당시 검토 환경 기준이다. 운영값을 포함할 수 있는 원시 실행 로그는 비공개 작업 위치에 보존하며 공개 원문을 실행 로그 자체로 오인하지 않는다. [원문 SHA256 원장](evidence/2026-11-12-consumer-sdk-original-receipts.json)은 원본 이름·게시 경로·크기·해시를 연결한다.

입력 JSON:

- [review-manifest-consumers-c11-batch-1.json](evidence/2026-11-12-review-manifest-consumers-c11-batch-1.json)
- [review-manifest-consumers-c11-batch-2.json](evidence/2026-11-12-review-manifest-consumers-c11-batch-2.json)
- [review-manifest-map-c11-main1497-supplement-7ce.json](evidence/2026-11-12-review-manifest-map-c11-main1497-supplement-7ce.json)
- [review-manifest-transport-c11-delta-4e25c98.json](evidence/2026-11-12-review-manifest-transport-c11-delta-4e25c98.json)
- [review-manifest-manager-component-ui-1.json](evidence/2026-11-12-review-manifest-manager-component-ui-1.json)
- [review-manifest-manager-component-ui-2.json](evidence/2026-11-12-review-manifest-manager-component-ui-2.json)
- [review-manifest-manager-component-ui-3.json](evidence/2026-11-12-review-manifest-manager-component-ui-3.json)
- [review-manifest-manager-mount-order-1.json](evidence/2026-11-12-review-manifest-manager-mount-order-1.json)

Manager 최종 e798의 backend3846 PASS/40 SKIP/1 warning, frontend54 PASS·browser2 PASS·type/lint/Doctor/build 및 중앙 정책이 성공했다. 실제 CI checkout7f44759의 전체 tree가 e798과 같았다. [PR589](https://github.com/digitie/kor-travel-docker-manager/pull/589)는 af413443으로 머지했고 target main의 전체 tree도 확인했다. 현재 환경은 G 아래 보존하고 raw 값은 component 경계에서 한 번 인코딩한다. 기존 Map escaper·paired 검사·manifest schema와 공통 배포물은 유지한다.

현재 앱 머지는 [Geo631](https://github.com/digitie/kor-travel-geo/pull/631), [Weather226](https://github.com/digitie/kor-travel-weather/pull/226), [Concierge265](https://github.com/digitie/kor-travel-concierge/pull/265), [Manager588](https://github.com/digitie/kor-travel-docker-manager/pull/588), [Pinvi732](https://github.com/digitie/pinvi/pull/732)다. Pinvi는 저장소 정책에 따른 squash dd3bcd18이며 reviewed528과 target main의 전체 tree가 같았다. [Map1496](https://github.com/digitie/kor-travel-map/pull/1496)은 최종 정확 CI 6개 성공 후 f347b353으로, [Transport181](https://github.com/digitie/kor-travel-transport/pull/181)은 최종 정확 CI 2개 성공 후 936fdb90으로 머지했다. 두 앱 모두 target main의 전체 tree와 최종 검토 입력이 같았다.

실제 Weather 공식 dry-run에서 발견한 Mounts 최상위 열거 순서 오탐은 별도 [PR590](https://github.com/digitie/kor-travel-docker-manager/pull/590)으로 수정했다. 기존432와 신규85가 모두 통과했고 원 A는 추가48을 포함한565 PASS, 원 B는517 및 추가24개 공격을 확인했다. 정확 CI43106671432는 backend3931 PASS/40 SKIP, frontend54·browser2 PASS이며 중앙 정책43106671905도 성공했다. CI synthetic merge d4e25bc의 전체 tree와 reviewed ac4가 같다. 최종 merge ca1d32b의 fetched main 전체 tree도 같았다. 이 source 판정과 실제 SDK 설치·Weather UI 수용은 구분한다.

이 출판 정리는 C11의 UI0.2.0·tokens0.1.1 및 동결한 7종 산출물을 다시 만들지 않는다. 앱별 새 이미지와 실제 운영 수용의 최종 결과는 통합 배포 기록에서 별도로 확정한다.
