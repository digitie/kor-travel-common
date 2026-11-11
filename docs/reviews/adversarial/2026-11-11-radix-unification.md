# Radix 공통화 독립 적대 리뷰1차

- review ID: 2026-11-11-radix-unification-1
- 종류: FULL
- 범위: common c289b462→789e6d2, 지도 원본9c46c571→7402214
- 전문영역: A frontend·접근성 / B packaging·dependency·CI·license
- 범위 밖: 소비자 최종 이관·운영·이미지 수용
- 상태: 두 독립 원본 확정, 후속 수정·재검토 중
- verdict: A BLOCK / B BLOCK

## 원본과 불변 입력

동일 [manifest1](evidence/2026-11-11-radix-unification-manifest-1.json)을 전달했고 상대 결과 공개 없이 검토했다. [A 원본](evidence/2026-11-11-radix-unification-reviewer-a.md)과 [B 원본](evidence/2026-11-11-radix-unification-reviewer-b.md)은 byte 그대로 보존한다. 실행 ID·시각·관찰 SHA·격리·검증 명령·미실행 범위는 원본에 있다.

## 통합 disposition

| 항목 | 조치 상태 |
|---|---|
| A-P1-01 / B-P1-04 RSC variants | 순수 CVA 정의로 분리, 실제 packed Next 서버 fixture 추가. 원 리뷰어 재확인 대기 |
| A-P1-02 / B-P2-03 forceMount | Map 명시 hidden·일반 Tab 상태 CSS 숨김, 상태 보존·접근성 시험 추가. 재확인 대기 |
| A-P2-01 Progress | value/max 정규화·ARIA/시각 일치 시험 추가. 재확인 대기 |
| A-P2-02 선택 정책 | bulk·체크박스·해제와 controlled 정리 규칙 수정. 재확인 대기 |
| A-P2-03 행 키 | 본행/상세행 JSON 태그 namespace로 분리. 재확인 대기 |
| A-P2-04 공통 클래스 | kt 토큰 유틸로 정렬·CSS 생성 확인. 재확인 대기 |
| A-P2-05 패널 focus | 불투명2px 공통 focus outline·브라우저 시험 추가. 재확인 대기 |
| A-P2-06 / B-P2-02 방향 | Radix orientation 전달·방향키 시험 추가. 재확인 대기 |
| A-P2-07 / B-P1-06 상태 CSS | 공식 shadcn eject CSS·MIT 고지·tw-animate-css 동봉. 재확인 대기 |
| A-P3-01 / B-P1-07 공백·오탐 | 공백 정리·비밀 검사 약화 없이 코드 표현 수정. 재확인 대기 |
| B-P0-01 지도 고지 | 원본 core/RN1.0.1, web미출시1.0.3에 GPL3 전문·NOTICE·src·tsconfig·pack CI 추가. 재확인 대기 |
| B-P1-01 전이 React | 해당 앱의 런타임 그래프·물리 인스턴스 중복 검사와 독립 workspace/devtool 대조 추가. 재확인 대기 |
| B-P1-02 section 덮어쓰기 | 각 선언 구역 검증·중복 거부·runtimeRequired 정책 추가. 재확인 대기 |
| B-P1-03 모바일 버전 | RN 정확 축·required/artifact/forbidden 연결 검증 추가. 재확인 대기 |
| B-P1-05 기존 package CI | fixture·lock·자동 파일명 참조와 packed browser CI 갱신. 재확인 대기 |
| B-P2-01 네이티브 경계 | mobile 프로필의 DOM UI/Radix 직접 설치 금지. 재확인 대기 |

P0/P1을 release 차단 자체로 닫지 않는다. 후속 불변 manifest와 검증을 두 원 리뷰어가 재확인한 뒤 별도 post-fix 보고서에서 최종 verdict를 기록한다. 이 문서는 최초 결과의 역사 기록이며 운영 수용을 뜻하지 않는다.
