# Dagster RPC·복구 가이드 최종 리뷰

- Review ID: `2026-10-15-dagster-rpc-recovery-guide`
- 종류: 독립 FULL 2인 및 최종 immutable 확인
- Candidate: `61f93d98d5d7df9b3e597eefd9d7d04e7bbf098b`
- Parent: `ae5ca6c5bfaf6e514cc2d5b41855c14af67d3de7`
- Delta base: `091d4fe1dda8eacf43b453ad39b4f2e42e9e80fc`
- 상태: `COMPLETE`
- 최종 verdict: **PASS / OPEN 0**
- 전문 범위: A SDK·실행 복구 / B 운영 정합·문서 정본·검증 과장
- 실행 시각: A 05:46:42~05:49:45Z 및 05:51:20Z immutable 확인, B 05:50:36~05:51:49Z, 2026-10-15.

[manifest](evidence/2026-10-15-dagster-rpc-recovery-guide-manifest.json),
[A 전체 원문](evidence/2026-10-15-dagster-rpc-recovery-guide-reviewer-a.md),
[A 최종 commit 확인](evidence/2026-10-15-dagster-rpc-recovery-guide-reviewer-a-final.md),
[B 전체·최종 원문](evidence/2026-10-15-dagster-rpc-recovery-guide-reviewer-b.md)을 바이트 그대로 보존한다.
전체 가이드와 새 두 문서 델타를 검토했다. 원문 SHA와 최종 문서 SHA는 manifest에 있다.
이 closure는 검토한 가이드·journal 바이트와 규범·판정을 변경하지 않는다.

## Finding 반영

| ID | 심각도 | 상태 | 반영·검증 |
| --- | --- | --- | --- |
| B-P3-01 | P3 | FIXED | heartbeat tolerance 300/1800과 실제 interval 합산 cutoff를 구분했다. 로컬 SDK 경계를 확인했다. |
| A-P3-01 | P3 | FIXED | 중간 문구의 CLI·GraphQL 오류 평가 차이 주장을 제거했다. 두 실제 wrapper 모두 ignore_errors=True다. |

B의 오류 평가 차이 제안은 잘못된 추정으로 철회됐으며 확정 제품 finding으로 추가 집계하지 않는다.
미해결·연기 finding은 없다. A의 새 정적14·SDK5·문구3 및 별도 heartbeat7조건과
B 최종40조건은 각각의 원문 범위로만 기록하며 서로 합산하거나 운영 건수로 표시하지 않는다.

## 검증과 한계

가이드 수정 뒤 Coordinator의 링크688문서·2797대상 오류0, plan109 오류0,
도구 unittest337실행 중336 PASS·1 SKIP, git diff --check PASS를 확인했다.
최종 heartbeat 문구의 링크 검사도 다시 통과했다. archive 추가 뒤 링크692문서·2802대상 오류0, plan109 오류0, unittest337실행 중336 PASS·1 SKIP, 공백 검사를 다시 통과했다. CI는 최종 PR HEAD로 확인한다.
Python API·패키지·소비자 튜닝 변경은 없다.

두 reviewer는 실제 새 운영 호출 없이 저장된 NOOP 동일 run SUCCESS, 두 sensor SKIPPED/0run,
Janitor fresh start 및 first_cron_observation NOT_RUN을 대조했다. 이는 새 live 시험이 아니다.
최초 Janitor cron·전체 source batch·모든 소비자 이전·CPU/RSS 절감률은 이 문서 PR에서 NOT_RUN이다.
소비자 운영/UI 결과는 해당 소비자 PR의 별도 증거다. 운영 주소·credential·DSN·cookie·원본 로그는 포함하지 않는다.
