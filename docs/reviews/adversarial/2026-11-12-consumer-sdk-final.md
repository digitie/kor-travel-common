# 앱 최종 입력과 Manager UI 교체 기능의 독립 검토 기록

원 A/B는 같은 불변 입력을 각각 검토했고 구현에 참여하지 않았다. 각 원문과 실패를 보존하며 이후 조건 충족은 별도 기록한다. 아래 SOURCE PASS는 해당 소스 범위의 판정이며 운영 배포·로그인 수용과 구분한다.

현재 운영 결과는 [최종 운영 수용 6개 정산](#최종-운영-수용-6개-정산)을 따른다. 아래 입력별 원 검토·CI·운영 후속 문장은 각 시점의 prior history다. 당시의 4개·5개 완료, pending·BLOCK·미실행을 이후 성공으로 바꾸지 않는다.

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

## 문서 출판·규약 입력1의 독립 검토와 실제 배포 후속

원 A/B는 같은1742c375의46개 문서/증거/attributes를 Git object에서 독립 검토하여 두 PASS·신규0으로 판정했다. [원 A](evidence/2026-11-12-review-A-common-final-docs-1.md.txt)·[원 B](evidence/2026-11-12-review-B-common-final-docs-1.md.txt)·[불변 입력](evidence/2026-11-12-review-manifest-common-final-docs-1.json)·[원문 해시](evidence/2026-11-12-common-final-docs-original-receipts.json)를 보존한다. 원문은 당시 네 앱 완료 snapshot을 유지한다. 정확1742의 frontend43111997734·python-package43111997752·docs43111997774와 docs6개 job이 모두 성공했다. Python workflow의 dependency recovery job 성공을 전체 Python 기능 시험 재실행으로 확대하지 않는다.

이후 Geo의 공식 UI 교체와 실제 수용을 완료하여 현재 배포 완료는5개다. [공개 배포 정산 JSON](evidence/2026-11-12-frontend-deployment-receipt.json)에 실제 source/image/common파일·정상 로그인/표/폰트/모바일/지도/로그아웃·미완료·사용자 제외 경계를 기록한다. 비공개 원본 영수증은 파일명·크기·SHA256으로 연결하고 운영 주소·키·계정 값은 출판하지 않는다. 이 후속 사실 delta와 원문 출판은 새로운 문서 입력에서 다시 검토한다. Transport는 진행 중, Map은 사용자/Claude 별도 범위이고 native 기기/EAS/스토어는 NOT_RUN이다.

### 입력2 원 두 검토·CI 조건 정산

79ed906f의 사실 delta10개는 원 A/B 모두 DOCS/PROVENANCE PASS·신규0이며 원본7개와 하위23개 실행 증거의 해시 연결을 각각 확인했다. 당시 원문에 남은 docs CI pending은 보존하고, 이후 정확 frontend43114222024·python-package43114221949·docs43114221873 SUCCESS를 별도로 정산한다. [원문3개 archive](evidence/2026-11-12-common-final-docs2-originals.tar.gz)와 [member/전체 SHA256 원장](evidence/2026-11-12-common-final-docs2-closure-receipts.json)에 두 원문과 불변 입력을 bytes 그대로 동봉했다. gzip·tar 내부도 기존 전체 scanner의 검사 대상이며 새 attributes나 탐지 예외는 추가하지 않는다. 이는 원문·disposition·색인만 추가하는 closure artifact다. 새 운영 사실·규범·코드 승인으로 확대하지 않으며 Transport 최종 수용은 계속 후속이다.

### Manager591 두 UI 선택 원 검토·머지 정산

Transport의 기존 core/admin current에서 UI 하나만 선택하는 최종 e533820은 원 A/B COMBINED SOURCE PASS·신규0이다. 원 두 리뷰어는 SDK503개를 각각 직접 통과하고, A는 추가33개와 실제 Compose/fake Engine raw12값, B는 추가25개와 actual create Env8개 경계 대조를 수행했다. 이전478은 A의 PUBLIC ONLY checkpoint이며 B 완료 승인이나 admin 승인으로 확대하지 않는다. [원문·불변 입력6개 archive](evidence/2026-11-12-manager591-originals.tar.gz)와 [member/전체 해시·판정 원장](evidence/2026-11-12-manager591-closure-receipts.json)에 당시 실패·제한·pending을 byte 그대로 남겼다.

정확 CI43114698062는 backend3979 PASS/40 SKIP·frontend54/browser2·Doctor0·lint/type/build 성공이며 중앙43114698466도 성공했다. [PR591](https://github.com/digitie/kor-travel-docker-manager/pull/591)은508b074c로 머지했고 fetched main 전체 tree98f2fefd가 reviewed e533과 같다. 기본 PUBLIC과 등록된 admin-web 선택은 기존 G/frozen/비선택/health/current 경로를 사용한다. 관리자 release 표시 ENV만 승인 source·OCI·image default Env 일치 때 결박하고 인증·세션·지도·DB 환경은 보존한다. 실제 이미지 생성·trusted 설치·운영 적용·UI/API/DB 수용은 source PASS와 별도다. 이 출판으로 Transport 완료를 추가하지 않는다. backend499/schema0042 보존과 사용자 Map 별도 인계도 유지한다.

### Transport182 기존 관리자 기능 보존의 원 검토·머지 정산

실제 관리자6bd와 공개936의 기능 분기를 대조한 후 [PR182](https://github.com/digitie/kor-travel-transport/pull/182)에서 주차장·철도 시간표와 공식 안내·전화·지도 이동을 유지하고, 원 두 검토의 지적을 수정했다. 원 A의 A-TRANSPORT-P2-01은 미지원 fuel/regions 경로의 허위 성공 시험, A-TRANSPORT-P2-03은 가변 cluster key의 DOM·포커스 손실, A-TRANSPORT-P3-02는 수집 작업 한국어 label 누락이다. 원 B의 B-TR-P2-01은 공식 안내·전화 링크 누락, B-TR-P3-02는 같은 작업 label 누락이다. 입력1의 두 BLOCK을 지우지 않고 입력2에서 각 원 리뷰어가 자기 지적 FIXED·SOURCE PASS·신규0으로 재확인했다. 실행3도 양쪽 PREMERGE SOURCE+QA PASS·신규0이다.

[원문·불변 입력·머지 증거10개 archive](evidence/2026-11-12-transport182-originals.tar.gz)와 [member/전체 해시·판정 원장](evidence/2026-11-12-transport182-closure-receipts.json)에 원문 bytes와 당시 pending을 보존한다. 정확 c3da263 CI43130997296·정책43130998009가 성공했고 backend1548 PASS/2기존 SKIP/6warnings, 공개164·관리자432 PASS와 Doctor0을 확인했다. 별도 native/Alpine 브라우저는 각각 기존18·검토회귀4·기능6, 합계56 PASS이며 skip/flaky/unexpected/report error0이다. workflow의 live-e2e SKIPPED를 PASS로 집계하지 않는다.

실제 merge6b75c3b3의 전체 tree077e7c14는 검토 source와 CI synthetic merge072c51d1의 tree와 같다. 이는 소스·검증·머지 정산이다. 실제 merged source ARM 이미지, 공식 관리자 단독 교체와 정상 계정 UI 수용은 별도 후속이며 이 기록으로 Transport 전체 배포 완료를 추가하지 않는다. backend499/schema0042와 공개936의 보존 경계도 유지한다. 라이브러리·규범·산출물 bytes는 변경하지 않는다.

### Transport183 모바일 메뉴 원문과 머지 정산

[PR183](https://github.com/digitie/kor-travel-transport/pull/183)은 공통 기본 상단 가로 탐색과 1024px 데스크톱 레일, 활성 항목·폰트·폭 변경과 문서 세로 위치, 실제 caller origin의 격리 검사를 다룬다. Geo 드로어는 규약의 허용 옵션으로 유지한다. 원 A의 A-TR-MENU-P2-01은 전역 scrollIntoView가 문서 스크롤·입력 위치를 움직이는 문제, 원 B의 B-MENU-P2-01은 환경변수와 실제 caller baseURL이 다를 때 격리 경계가 어긋나는 문제다. 입력1 두 BLOCK을 보존하고 입력2부터 각 원 reviewer가 자기 지적 FIXED·신규0을 확인했다.

[원문·불변 입력·머지·CI 증거21개 archive](evidence/2026-11-12-transport183-originals.tar.gz)와 [member/전체 해시·판정 원장](evidence/2026-11-12-transport183-closure-receipts.json)에 여섯 번의 두 원문과 추가 시각 관찰을 bytes 그대로 동봉했다. b043의 메뉴5실패, db58의 테스트 타입 오류, ee45의 78개 검사 뒤 발견한 시각 여백과 cd4의 최초 작업자 기동 실패를 성공으로 덮지 않는다. cd4는 설정·단언·pool·제한시간을 바꾸지 않고 대상17개와 전체451개를 각각1회 통과한 명시 복구를 보존했다. 자원 원인은 확정하지 않았다.

최종 cd4의 native·Alpine 브라우저는 각각39개, 합계78 PASS·skip/flaky/unexpected/report errors0이다. 실제 새 native 화면의 메뉴 높이171px는 768px 화면 높이900→1100에서도 유지되고 로고·로그아웃이 정렬됐다. 실행5의 두 FRONTEND EXEC PASS/CI PENDING 원문을 보존하며, CI종료6의 양쪽 PREMERGE PASS·신규0을 별도로 연결한다. 정확 CI43151188851·정책43151189609가 성공했고 공개164·관리자451·백엔드1548 PASS/기존2 SKIP/6 warnings 및 Doctor0을 확인했다. workflow live-e2e SKIPPED는 PASS가 아니다.

실제 merge47a4719a의 전체 tree510888aa는 reviewed cd4와 실제 CI checkout35045758의 tree와 같다. 이는 소스·검증·머지 정산이며 merged M의 ARM 이미지, 공식 관리자 단독 교체와 새 키·정상 운영 수용은 별도 후속이다. 라이브러리 산출물 bytes·규범·backend499/schema0042/공개936 보존 계약을 바꾸지 않는다.

## 최종 운영 수용 6개 정산

[공개 배포 정산](evidence/2026-11-12-frontend-deployment-receipt.json)의 현재 수용 앱은 Manager·Concierge·Pinvi·Weather·Geo·Transport 6개다. Transport 공개936/image3262의 기존 단계별13개·9세션 결과는 유지한다. 최신 관리자 [PR186](https://github.com/digitie/kor-travel-transport/pull/186)의 실제 mergef30dbd82와 ARM64 image0ac648f8을 사용한다. reviewed bd08·실제 CI checkout8303·mergef30의 전체 tree4fec4f76 일치를 확인했다. QA sourceb43과 bd08의 차이는 문서2줄이며 나머지908개 항목은 같다. QA의 전체 source를 merged source로 바꾸어 표기하지 않는다.

사용자가 지정한 Geo형 메뉴는 [PR184](https://github.com/digitie/kor-travel-transport/pull/184)에서 PC 왼쪽256px 세로 메뉴·모바일 왼쪽296px 드로어로 반영했다. [PR185](https://github.com/digitie/kor-travel-transport/pull/185)의 서버 지도 frame·포커스 보존에 이어 PR186에서 앱의 사용자 지정 지도 로더가 padding box 밖에 잘리는 문제를 수정했다. 이전184의 운영8 PASS/1 FAIL(연락처 영역)과 별도 진단 FAIL, 이전185의 운영8 PASS/1 FAIL 및 PNG 진단 FAIL(최초 canvas5초)을 그대로 보존한다. [184 원문](evidence/2026-11-12-transport184-originals.tar.gz)·[184 해시](evidence/2026-11-12-transport184-closure-receipts.json), [185 원문](evidence/2026-11-12-transport185-originals.tar.gz)·[185 해시](evidence/2026-11-12-transport185-closure-receipts.json)에 단계별 실패·미도달·검토·실행 범위를 남긴다.

PR186의 기존 두 리뷰어는 source2·helper3·최종 실행4 모두 각자 PASS·신규0을 확인했다. 입력1의 P3 문서 표현은 bd08의 문서2줄로 수정했고, 미실행59a의 실제 동색 재현을 주장하지 않는다. 정확 bd08의 PR43215261871·push43215254241·정책43215262267은 모두 첫 attempt SUCCESS다. PR/push 각각 공개164·관리자458 PASS·Doctor0, backend1548 PASS/2 기존 SKIP/6 warnings이며 live-e2e 두 SKIPPED는 PASS가 아니다. 최초 b43 CI의 superseded 수동 취소1과 완료된 부분 결과도 보존한다.

격리 b43 검증은 native43·Alpine43 PASS, skip/flaky/unexpected/report errors0이다. 새 NoJS 로더2개는 native43에 포함하며 별도 가산하지 않는다. 이전 M9의 같은 검사는2 FAIL, 새 검사는2 PASS(PC1280·모바일375, 가시 면적 비율1)이고 부모가 두 화면을 직접 확인했다. 실제 지도 수용은 명시적인 새 계약(의미 있는 로딩 피드백5초·최초 전체 bootstrap60초)으로 수행했다. 이전 최초 canvas5초 계약과 동등하지 않으며, 이전 실패를 성공으로 다시 집계하거나 지연 원인을 확정하지 않는다. 실제 관측은 피드백2808.995ms·bootstrap5644.271ms였다.

실제 merged f30의 정상 ARM 빌드는 별도로 완료했고 retag가 아니다. canonical source909·COPY298·공통6패키지263·compiled32·OCI/default release·키와 환경 digest를 검증했다. 부모는 동결16개를 local·remote 모두 SHA256/bytes/mode로 확인했다. producer의 actualMergedNormalBuildCompleted와 operator의 normalDockerBuild 필드 차이는 기존 영수증을 보존한 호환 복사본의 필드1개로 연결했으며 빌드·소스·SDK를 바꾸지 않았다. 이 스키마 차이는 후속 빌드 체계 일관화 대상이다.

공식 SDK508 관리자 단독 dry-run1·confirm1, healthy/current/postproof가 통과했다. 부모는 운영 동결44개 전체를 remote에서, 다운로드한18개를 local에서도 확인했다. 나머지26개는 local 미다운로드이며 전부 local 검증했다고 주장하지 않는다. 선택 Transport current만 최신 관리자 source/image로 갱신했고 공개936/image3262·backend499/schema0042·비선택54·기존 인증/세션/root/pins와 다른 앱 current는 보존했다.

실제 f30 정상 수용은 첫 단일 세션9 PASS·실패0, 로그인1/로그아웃1과 보호 API401→로그인 후200→로그아웃303→401이다. bounded PNG40개(확대 전20·후20)는 승인 키 일치·HTTP200·PNG signature·IHDR256이며 그중 실제 bitmap decode2+2와 camera7→8이 통과했다. 전체 observer112개 중77개는 signature/크기 판정 이미지200·HTTP실패0이고 나머지35개는 미분류다. 40개나77개 전체를 실제 bitmap decode로 확대하지 않는다.

실제9개 폭·왕복11행, 메뉴·표·팝오버·연락처 API200/65개·주차장·철도·Pretendard12행이 통과했다. PC256px 세로 메뉴·모바일296px 왼쪽 드로어, 높이 변화 rail delta0·문서 scroll100→100·포커스 보존을 확인했다. 부모는 실제 지도 전체 화면1개와 PC 메뉴1개·모바일 메뉴2개를 직접 열어 한국 지도 도로·지명·지형과 메뉴 배치를 확인했다. 부모는 최종 동결63개 local SHA256/bytes/mode 전부를 대조했고 browser·프로세스·port·heavy·미정리 decoder0을 확인했다. 추가 로그인·운영 재실행은 없다.

[186 원문·실행 정산48개](evidence/2026-11-12-transport186-originals.tar.gz)와 [전체/member 해시](evidence/2026-11-12-transport186-closure-receipts.json)는 두 원 검토·불변 입력·CI·머지·실제 ARM·SDK·정상 수용·부모 대조를 연결한다. 원문 bytes와 과거 pending/FAIL을 유지하고 비공개 입력과 PNG binary는 출판하지 않는다. 기존47a의 실제 수용은 아래 당시 스냅샷으로 보존한다.

이전 문서 입력3/4의 [원문6개](evidence/2026-11-12-common-final-docs34-originals.tar.gz)와 [해시 원장](evidence/2026-11-12-common-final-docs34-closure-receipts.json)도 별도 보존한다. 당시 판정은 현재 M30 사실 후보의 승인으로 확대하지 않는다.

이는 운영 사실 갱신이며 이 출판 후보의 원 A/B 검토·정확 CI·PR50 머지는 별도 gate다. T-218은 IN_PROGRESS, Map 추가 소스·빌드·이미지·배포는 사용자/Claude 별도 범위, native 실기기/EAS/스토어는 NOT_RUN이다. 다음 순서는 Common50·Geo 단일 MD 마감 → Transport 남은 PR·빌드 체계 → 전체 프로젝트 빌드/CI/테스트 일관화 → CI 실행 순서 최적화(마지막)다. 라이브러리 버전·산출물 bytes·규범·CI·config·scanner 예외는 이번 사실 갱신으로 변경하지 않는다.

### 이전47a 운영 수용 스냅샷

[공개 배포 정산](evidence/2026-11-12-frontend-deployment-receipt.json)의 현재 수용 앱은 Manager·Concierge·Pinvi·Weather·Geo·Transport 6개다. Transport 공개936/image3262는 기존 단계별13개·9세션 결과이며 단일 전체 실행으로 확대하지 않는다. 최종 관리자 [PR183](https://github.com/digitie/kor-travel-transport/pull/183)의 실제 merge47a4719a/tree510888aa로 만든 ARM64 image3f2073의 canonical source907·COPY296·공통6패키지263·compiled32·OCI/default release를 동결 증거로 확인했다. 최초 collector 변수 shadow 실패를 남긴 채 같은 이미지 strict readonly r2가 통과했으며 이를 재빌드·retag로 대체하지 않았다.

정상 SDK508 admin-only dry-run1·confirm1 healthy와 current/postproof를 완료했다. 운영 receipt135fa3ba와 frozen37 member6d375b9f의 실제 해시 불일치0을 확인했다. 선택 Transport current는 새 관리자 source/image로 갱신했으며, 공개 current936/image3262·backend499/schema0042·비선택54·기존 인증/세션/root/pins와 다른 앱 current는 보존했다. 승인된 Geo 실사용 키는 Transport 등록 웹 build 입력에만 반영했다. 초기 operator launcher 문법 오류는 confirm 호출 전이며 실제 confirm은1회다. 키·접속주소·계정·원시 응답본문은 이 문서에 넣지 않는다.

실제 관리자 QA는 단일 정상 세션9 PASS·실패0·로그인1/로그아웃1/303→보호401이다. bounded map phase36개(zoom 전16·후20)는 모두 HTTP200·PNG signature·IHDR256과 승인 키 일치를 확인했고 실제 bitmap decode2+2·camera7→8이 통과했다. 전체 세션 observer96개 중 legacy image 판정68·HTTP실패0을 별도로 남기며 나머지28개를 오류 또는 정상 이미지로 단정하지 않는다. 실제7개 폭/왕복9행의 메뉴·실제 Pretendard·표·팝오버·주차장/철도/연락처, 높이 변화 시 rail delta0·문서 scroll/focus 보존도 통과했다. 실제 운영 screenshot은0이며 native 격리 화면 증거와 구분한다. browser 종료·프로세스/port/heavy0을 확인했다.

Mendel의 동결 actual QA receipte1f61de4·원본13 member23366f0c를 원본/동결26회 대조하고 참조5개 receipt도 확인했다. 운영37개와 QA13개 원문 bytes는 비공개 증거 위치에 보존하며 공개 JSON은 이름·크기·SHA256만 연결한다. 이전6b75 첫76응답은 당시 MIME/signature 미분류이고 후속 정상 Origin36건만 XML InvalidParameterValue/locator=key로 확인했다. ExceptionText 세부 유형은 독립 분류하지 않았다. 이 실패·이전 source/CI/review pending은 명시적 priorHistory로 그대로 남긴다.

이는 실제 운영 수용의 factual closure다. 기존30730650의 review archives·원문과 closure 판정을 변경하지 않는다. 이 facts3 출판 후보의 동일 원 A/B bounded 검토·정확 CI·PR50 머지는 후속이며 T-218은 IN_PROGRESS다. Map은 사용자/Claude 별도 범위, native 실기기/EAS/스토어는 NOT_RUN이고 toolchain·build ecosystem·CI_LAST 후속도 남는다. 규범·패키지·버전·CI·config·scanner 예외와 동결 배포물 bytes는 변경하지 않는다.
