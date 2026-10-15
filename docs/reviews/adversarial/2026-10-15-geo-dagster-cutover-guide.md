# Geo Dagster 이전 가이드 FULL 적대적 리뷰

- Review ID: `2026-10-15-geo-dagster-cutover-guide`
- 종류: 독립 전문 reviewer 2인 FULL, commit object-only
- Candidate: `3d3ca855f21180e46b5260a2c23b40bd74bd4624`
- Base: `efcd671207d7f9e2fb01251bab6854a8d543279a`
- 범위: 가이드 §12·journal, 제품·운영 변경 제외
- 사용자 요청: 공통 Dagster 적용 가이드와 2인 적대 리뷰
- Coordinator: Codex `/root`
- 검토 시각: A 02:56:10~02:57:15Z, B 02:56:56~02:59:32Z (2026-10-15)
- 상태: `COMPLETE`
- 최초 verdict: `CONDITIONAL`

## 기준선과 독립 원문

[동일 manifest](evidence/2026-10-15-geo-dagster-cutover-guide-manifest.json)에 두 Git blob의 SHA를 고정했다.
각 reviewer는 immutable Git object로 전체 diff를 읽었으며 운영 호출·원본 수정·상대 raw 읽기는 0이다.
실행 ID·전문 영역·시각·검증 한계는 각 원문에 보존한다.

| Reviewer | 영역 | 원문 | SHA256 |
| --- | --- | --- | --- |
| A | SDK 동작·복구·실패 누락 | [원문 A](evidence/2026-10-15-geo-dagster-cutover-guide-reviewer-a.md) | `34437b6c11eded773c536cfbbf1a14c774195e09ccb327f70528151bb2f6dbae` |
| B | 소유권·정본·검증 주장·비밀 | [원문 B](evidence/2026-10-15-geo-dagster-cutover-guide-reviewer-b.md) | `0a49dd8fe179ba0dd9b06c27c9b9ecfe6b3b92b5ed35d5cc4789cdc706917cb6` |

## 최초 finding과 disposition

두 원본 확정 후 교차 비교했다. reload 표현은 같은 문제를 각 ID로 보존한다.

| ID | 심각도 | 근거·실패 형태·영향 | 조치 |
| --- | --- | --- | --- |
| A-P2-01 | P2 | cursor None 첫 tick이 최신 실패를 건너뛸 수 있는데 prime/readback 순서 미명시 | `FIXED`: STOPPED cursor 저장·readback·public start 및 초기 gap 명시 |
| A-P3-01 | P3 | workspace reload를 DB 재시작과 혼동할 수 있음 | `FIXED`: code reload와 stack·DB 재시작 분리 |
| B-P3-01 | P3 | 고정 SDK 동작의 공식 source URL 누락 | `FIXED`: 공식1.13.24 source4개 추가 |
| B-P3-02 | P3 | workspace reload와 DB 재시작 혼동 | `FIXED`: A-P3-01과 같은 문장 수정 |

수정 commit은 `7594a7179e6bb7c8f938825fa5d46197f36ddf89`다.
최초 원문의 CONDITIONAL/OPEN 기록은 변경하지 않았고 [독립 post-fix 판정](2026-10-15-geo-dagster-cutover-guide-post-fix.md)에 closure를 연결한다.
owner는 Codex이며 DEFERRED 0이다. 이 보고서는 실제 운영 이전·큐·cron·E2E 성공 증거가 아니다.
