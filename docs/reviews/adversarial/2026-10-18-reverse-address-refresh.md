# 공통 주소 갱신 최초 독립 FULL 리뷰

상태: COMPLETE. 당시 verdict는 **A BLOCK / B CONDITIONAL**이다. 과거 실패를 최종 PASS로 덮어쓰지 않는다.

기준선은 Common c4859588 → 812b2916이다. 두 실행 ID·불변 manifest·전달 범위·격리·byte 원문 hash는 [evidence](evidence/2026-10-18-reverse-address-refresh-manifest.md)에 보존했다. [A 원문](evidence/2026-10-18-reverse-address-refresh-r1-reviewer-a.md), [B 원문](evidence/2026-10-18-reverse-address-refresh-r1-reviewer-b.md)을 수정하지 않았다.

| ID | 심각도 | 당시 finding | 당시 상태 |
| --- | --- | --- | --- |
| A-P1-01 | P1 | 정상 VWorld 요청의 HTTPX INFO 로그에 키·URL 노출 | OPEN |
| A-P2-02 | P2 | 완료 후 release 전 중단·만료 owner가 영구 진행 상태로 표시됨 | OPEN |
| B-P2-01 | P2 | VWorld 오류 뒤 Kakao 정상 무결과가 오류/backoff로 남음 | OPEN |
| B-P2-02 | P2 | 동일 좌표의 정상 무결과가 재사용되지 않아 위치마다 재호출함 | OPEN |

작성자는 별도로 batch_size=1에서 반복 실패 위치가 새 위치를 막는 ROOT-P1-01을 재현했다. 이는 독립 리뷰 지적으로 계상하지 않는다. 수정 commit과 최종 두 재검토 verdict는 [post-fix closure](2026-10-18-reverse-address-refresh-post-fix.md)에 기록한다.
