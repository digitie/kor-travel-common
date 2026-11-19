# 공통 라이브러리 정본과 실제 소비자 수용 — 2026-11-19

필수 사용과 버전 규범은 [라이브러리 규약](../../standards/frontend-libraries.md)과 자동 생성 정책이 소유한다. 이 문서는 선택한 불변 pack과 소비자 source·설치·이미지·실제 기능 검증을 연결한다. [증거 JSON](2026-11-19-consumer-library-adoption.json)의 이전 수용과 후속 상태를 구분하며 자격증명·원본 사용자 데이터는 싣지 않는다.

## 선택한 배포 정본

[AdminShell main pack catalog](admin-shell-ui-0.2.3-catalog.md)의 producer는 `0e2a3f5aa16323df0d009360802661c9bc496dc6`, guard/catalog pin은 `d644632ea9eaf2f6b6baa49305d65fae5bbc0bd4`다. 실제 producer artifact14500111373 ZIP SHA256은 `19881f2c3ed598ed7ec213c559be21ece2be77068bddee6de5bd249b6f8019e1`이다. SOURCE_SHA와 세 pack의 SHA512/SRI를 catalog와 대조했으며 재포장하지 않았다.

| 패키지 | 버전 | SHA256 | 정규 파일 수 |
| --- | --- | --- | --- |
| @kor-travel/ui | 0.2.3 | aa19793165ae37b2214d210692e23235545e1464c4e0059f99d943411fa753d9 | 96 |
| @kor-travel/tokens | 0.1.4 | 33d08d7b37c60d3e319da19608ce05137f6bf587dc8d42e3ce0dfb4b597a61fc | 25 |
| @kor-travel/toast | 0.1.3 | 34b514b270f88fc19c6b411b975d4497f91f3581530f32a39be264874ca09b37 | 8 |

웹에서 UI+tokens는121개, Toast도 사용하는 Geo는129개 정규 파일을 대조한다. 모바일은 tokens25개만 소비하고 DOM UI를 강제하지 않는다. 미사용 Toast·지도·도메인 의존성을 추가하지 않는다. 같은 이름을 사용하는 앱의 버전·pack bytes·lock SRI는 일치시킨다.

## 이전 정본과 실제 실행 근거

UI0.2.2·tokens0.1.3·Geo Toast0.1.2의 [이전 catalog](virtual-table-ui-0.2.2-catalog.md)와 실행 증거는 보존한다. 그것은 UI0.2.3의 설치·배포 검증을 대신하지 않는다. 표의 기존 source와 새 소비자 source·이미지는 각각 결박한다.

| 앱 | 기존 실제 기능 수용 | 새 정본 후속 |
| --- | --- | --- |
| Geo | source96ff, native127·5폭·지도·로그인/로그아웃 검증 | 이관 PR·새 native129·실제 화면/배포 확인 중 |
| Weather | source8a4(PR266), native119·schema43·원24RUN/3STOP·화면/지도 수용 | PR267·COPY PR268과 새 UI/tokens 정본 채택을 결박 |
| Transport | source5a28(PR219), SDK618·스케줄20개 복원·native119·5폭·지도/로그아웃 검증 | 새 UI/tokens 이관과 후속 이미지/성능 검증을 별도 결박 |
| Pinvi | source227, web native119·지도/사용자·로그아웃 검증, 모바일 NativeWind5 RC·Tailwind4 source/CI | 웹 UI/tokens와 모바일 tokens 이관·검증 확인 중; 실기기/EAS/스토어 미실행 |
| Concierge | UI source0c85 native119·5폭·지도·로그아웃 검증, Python source16c846 유지 | 새 UI/tokens 이관과 UI 이미지 검증 확인 중; 무관한 Python 재빌드 없음 |
| Manager | 양쪽 설치 rootEFDA와 frontend617 tree의 UI0.2.2 기능 수용 | 외부 PR619의 source9643은 UI0.2.3을 사용하므로 새 frontend build/native/실제 화면 검증 필요; PR620 SDK 중복 관측 개선은7f07a171e39dc600a7b266da2743bb4327730fcf로 머지, 새 실제 배포 검증은 별도 |

## 성능·신선도와 한계

- Transport PR219의 실제 rail 첫 관측200은3,237ms(app CPU2,055ms·SQL1,442ms/39문), 다음200은390ms,304 다섯 건의p95는90ms였다.304는 각각0byte·page build0·full fingerprint0이다. 첫1초 목표는 미달이며 강제로 cold 상태를 만들지 않았다. 과거 서버18.728초·client15초 timeout과 서로 다른 환경이므로 단순 전후 개선율로 제시하지 않는다.
- Weather PR266 targeted current는 첫20012.59초·다음 큰 페이지2.89초·동일 key30488ms였다. 별도 무프로파일 여섯 프로필의 첫 응답은 모두200이나6.47~17.57초였고 cold 목표와 source 신선도는 미달이다. PR263의27.9초 측정과 같은 입력·환경의 교대 비교가 아니므로 단순 개선율로 제시하지 않는다. 별도 current limit2000 세 건은 승인 세대·계획 존재·활성 시도 metadata 조회 중 SQL57014로503을 반환했다. 단일 누락 index나 host 부하의 인과관계까지 증명한 것은 아니다.
- Map 자연05:30Z 단기예보 적재는42개 요청 모두200·1,452위치·442 delta rows로05:33:52Z SUCCESS였다. 원천 수집 시각은11/18 12:15Z이고 source_status는stale다. 이 성공과 별도 current503을 합쳐 정상/신선으로 표시하지 않는다.
- Weather PR264~267과 Transport PR218~219의 로컬 CPU 개선율은 해당 정규화·직렬화·동시 작업 fixture 범위다. 실제 전체 수집·첫 조회 개선율은 새로운 runtime 측정으로 확인한다. 효과 없는 bulk fetch·multiVALUES·압축 수준·namespace 중복 계산 후보는 제품에 넣지 않았다. COPY PR268은 실제 PostgreSQL16건과 저장 단계5교대 쌍을 통과했으나 전체 수집·첫 조회의 운영 개선율은 미검증이다.

## 최종 출판 조건

새 정본의 소비자별 source/lock·실제121/129/25개 파일·이미지 source·로그인/로그아웃·반응형/지도 검증과 성능 한계를 결박한 뒤 이 기록을 확정한다. 같은 [Geo 단일 보고서 draft PR644](https://github.com/digitie/kor-travel-geo/pull/644)를 갱신하며 다른 Geo 보고서 PR을 만들지 않는다. CI 순서 감사·최적화는 마지막에 수행한다. 현재 기록은 후속 진행 상태이며 새 버전 전체 배포 완료를 뜻하지 않는다.
