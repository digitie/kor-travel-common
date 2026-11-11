# 공통 source4의 두 독립 원 리뷰어 정산

입력은 common2ec5192·후보9이며 같은 불변 manifest4를 사용했다. 두 리뷰어는 구현에 참여하지 않았고 상대 원문을 보지 않았다. 이전 source3 BLOCK 원문과 신규 수정본의 판정을 구분한다.

| 원 리뷰어 | source4 판정 | 기존 finding | 신규 finding |
|---|---|---|---|
| A Mill | CONDITIONAL | A-P2-09 FIXED, 이전 FIXED 유지 | A-P2-10 P2 OPEN: 연결된 두 번째 gzip header metadata 미검사 |
| B Epicurus | PASS | B-P1-08·09·10 FIXED, 이전 FIXED 유지 | 없음 |

정확2ec의 frontend·selftest·Python package·docs workflow 전체가 성공했고 docs의 여섯 job 모두 성공했다. 두 원 리뷰어가 실제 CI와 후보9 SRI 일치·packed browser65개를 확인했다. 정책68, Python382실행=381 PASS/1 SKIP, 실제 scanner 발견0은 새 적대적 반례를 해결했다는 뜻이 아니다.

A-P2-10은 현재 고정 vendor에 실제 비밀이 있다는 주장이 아니다. 두 scanner가 정상 tar 뒤의 빈 gzip member에 들어간 금지 metadata를 놓치는 합성 반례다. 수정 후 원 A 재확인을 수행하며 정식 연기 승인으로 처리하지 않는다. 원문 판정은 보존한다. 최종 소비자 리뷰·앱 PR 머지·새 배포는 별도다.

## 원문과 해시

- [review-A-common-postfix-4.md](evidence/2026-11-11-review-A-common-postfix-4.md): SHA256 25df57642d2a8d8cd29d62e8e5aa7707599525a884e629af9d66ad7c6a0396ba
- [review-B-common-postfix-4-publication.md](evidence/2026-11-11-review-B-common-postfix-4-publication.md): 공개용 사본 SHA256 eda110bea6f96e3916c65f32310435680d4eb8a0bc0b70e044f10eb3aed5b081. 원문 SHA256 cf8046ea52667f93158f727dafa0b179f35c8a1a11a2d1a55116253c8be16d22는 [불변 Git 원문](https://github.com/digitie/kor-travel-common/blob/d1fe0a34ed720e4511a0612265e949632623a8dd/docs/reviews/adversarial/evidence/2026-11-11-review-B-common-postfix-4.md)에 byte 동일 보존한다. 원 B가 공개 compiler 상수 리터럴 두 개만 설명으로 바꿨으며 판정·finding은 같다. 새 scanner 예외를 만들지 않았다.
- [review-manifest-common-4.json](evidence/2026-11-11-review-manifest-common-4.json): SHA256 e5c7101e4130b4bf66c90a8ef2e54f3c672c5a79f0eeb8216bfc9ebcaa85c951
