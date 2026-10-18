# 공통 주소 갱신 FULL r3 — 역사적 BLOCK

상태: COMPLETE. **A PASS / B BLOCK — P1 1개·P2 1개 OPEN 당시 판정.**

base c48595880aaad4367802ad71af2525a8a5e17c6a → 제품14115ba99ab5d72d4f381d25b2dca810b24914d6.
[불변 manifest·원문 hash](evidence/2026-10-18-reverse-address-refresh-r3-r4-manifest.md),
[A 원문](evidence/2026-10-18-reverse-address-refresh-r3-reviewer-a.md),
[B 원문](evidence/2026-10-18-reverse-address-refresh-r3-reviewer-b.md).

| Finding | 당시 결과 |
| --- | --- |
| B-P1-03 | 지속 실패 수동 cycle의 cursor 뒤만 조회해 앞쪽 새 위치가 무기한 대기 |
| B-P2-04 | backoff만 남은 경우에도 빈 run 반복 |

이전 수동 실패 재개·비활성 오류 슬롯 문제의 수정은 확인했지만 새 반례가 남아 BLOCK했다.
A의 집중27 PASS와 B의 집중21 PASS·자체19조건은 각각의 범위이며 합산하지 않는다.
[다음 r4 재검증](2026-10-18-reverse-address-refresh-r4-post-fix.md)에서 수정과 원 reviewer의 closure를 기록한다.
