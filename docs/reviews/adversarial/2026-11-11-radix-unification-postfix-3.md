# 공통 후보8 원 리뷰어 3차 판정과 후속 수정

두 원 리뷰어의 동일 manifest3 기준7e 판정은 BLOCK이며 원문은 수정하지 않는다. 기존 최초21건과 후속 A-P2-08·B2-P3-01은 FIXED를 확인했다.

| 새 finding | 불변7e 판정 | 후속 구현과 현재 상태 |
|---|---|---|
| A-P2-09 금지 경로 재export·literal 지연 로딩 | P2 OPEN | 2c1182e에 CLI 회귀 수정, 원 리뷰어 source4 확인 전 OPEN |
| B-P1-08 MCR checkout Git 신뢰 | P1 OPEN | 00ddd65에서 정확 workspace만 신뢰. 실제 c8 pack SRI·browser65 PASS 직접 관찰, 새 기준선 확인 필요 |
| B-P1-09 압축 vendor와 UTF-8 scanner 충돌 | P1 OPEN | 34043de/97ccc97의 제한된 archive·native ASCII 검사와 정확 member/rule/SHA256 오탐 처분. 새 기준선 확인 필요 |
| B-P1-10 linked workspace 개발 CSS 그래프 | P1 OPEN | 2c1182e에서 도달한 linked workspace 개발 엔진 대조. 원 리뷰어 source4 확인 전 OPEN |

정책 우회는 실패11개와 확장 모듈 실패4개를 보존하고 전체 정책68개를 통과했다. 후보9 UI94/tokens25파일은 후보8과 비교해 checker 두 파일만 바뀌었으며 나머지 실행 코드·CSS·metadata117개는 동일하다. 지도3개와 CSS fix.4의 bytes도 같다. 이 동등성은 원격 CI·소비자 최종 판정을 임의 PASS로 바꾸지 않는다.

97ccc97의 Python 도구379실행은378 PASS/1 SKIP이며 정보 유출 두 검사에서 발견0, 공개 코드·컴파일 상수의 정확 hash/rule 예외32/4를 확인했다. archive 내부의 다른 규칙·헤더·metadata는 계속 검사하고 변경된 member hash는 거부한다. 최종 source4의 두 원 리뷰어·정확 CI·앱·머지·새 배포는 별도다.

## 원문과 해시

- [review-A-common-postfix-3.md](evidence/2026-11-11-review-A-common-postfix-3.md): SHA256 ab02db083de78deb7b514067071d01c715658dd63c988410d6b880e0d67c0037
- [review-A-common-postfix-3-ci-00ddd65.md](evidence/2026-11-11-review-A-common-postfix-3-ci-00ddd65.md): SHA256 66e9ea4fd2937d2dfd408d25d83f7d589c758bb95f4ff37dfdec4748c33350e0
- [review-B-common-postfix-3.md](evidence/2026-11-11-review-B-common-postfix-3.md): SHA256 0351063787a4367e264cf7dce61b521a2e87043edc66a6ed8b03139137e479cc
- [review-manifest-common-3.json](evidence/2026-11-11-review-manifest-common-3.json): SHA256 047ae6686cf8a08515a1e20b97147c218d5278823e976a6022aad34097021cd6
