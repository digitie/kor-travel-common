# 다중 job 재시도 최종 소스 리뷰

- Review ID: `common35-multi-job-retry-03396709-20261016`.
- 종류: 전문 리뷰어 서브에이전트 2인 독립 FULL9 delta.
- Candidate: `03396709ce2d81644a6ceb1bd12021a0b4014df2`; 제품 `1b599c4663737c468ce163af03d446beb3d210fc`.
- Base: `d1aa4bbacab87af9ebae08757bd3fcb80f748fe9`.
- 상태: `COMPLETE`; 최종 verdict **PASS / OPEN0**.
- 범위 밖: 소비자 pin·센서 전이·native 설정·운영 이미지/worker·복구/CPU/RSS/live. Common34 제품은 새 독립 리뷰 수에 포함하지 않는다.
- Coordinator: root; 원문 보존·문서 종결 담당 D.

[동일 manifest](evidence/2026-10-16-multi-job-retry-manifest.md),
[A 원문](evidence/2026-10-16-multi-job-retry-reviewer-a.md),
[B 원문](evidence/2026-10-16-multi-job-retry-reviewer-b.md)을 보존한다.
archive B는 팀 D(`/root/review_finish_b`)의 독립 실행이며 원문 header·bytes를 바꾸지 않았다.
D는 Common34 작성자였으나 Common35의 새9파일 delta를 작성하지 않았다.
두 원문이 각각 동결되고 root가 FULL 읽은 뒤에만 이번 교차 통합을 시작했다.

## 기준선과 독립 검증

| 항목 | Reviewer A | Reviewer B(팀 D) |
|---|---|---|
| 실행 ID | common35-A-03396709-20261016T020746Z | common35-review-finish-b-d-03396709-20261016 |
| 시각 | 02:07:46Z~02:12:08Z 이후 고정 | 검증02:01:27Z~02:04:58Z, 이후 core import·원문 기록 |
| 격리 | exact Git archive/object | detached worktree/object, 전후 clean |
| 실제 HEAD | 03396709ce2d81644a6ceb1bd12021a0b4014df2 | 동일 |
| 전문 영역 | SDK·실패 분류·인계/예산 | 다중 귀속·cursor·실제 SQLite·단일 API/JobSnap |
| 본인 검증 | SDK1.13.24 standalone32조건, DB/network 금지 모형 | SDK1.13.24 단일+다중78PASS14.44초, 추가 SQLite12조건·core lazy import |
| verdict | PASS / OPEN0 | PASS / OPEN0 |
| 원문 SHA256 | 70ee68cb33414ee64207c187a7a3784bbce305edd73a68404ee04247851db44e | 2200623b5baf2a8ece67d4a97c01f6a9e8b206408650150334fd03a549adc702 |

## Finding과 disposition

두 reviewer 모두 P0/P1/P2/P3 신규 finding0이다. 수정·기각·연기할 finding이 없으므로
제품 post-fix도 없다. 두 실행의 조건·시험 수를 독립 누적 테스트 수로 합산하지 않는다.
기존 단일 판정 body·job별 policy/config·최대100 초기 page/공유 cursor·협력5초/외부10초·
최대1요청·partial/provider/unknown 거부·native/pending/child/active·소비자 전이 한계를 각각 검토했다.
단일 job_name=None과 다중 job_name 명시, JobDefinition 보존도 원문 근거를 따른다.

## 검증 범위와 최종 gate

작성자443/관련78/별도161·wheel은 작성자 evidence이며 reviewer 결과로 재집계하지 않는다.
review fixture/명령 오류와 수정 경위는 각 원문에 남겼으며 제품 실패로 숨기거나 세지 않았다.
candidate03396709의 CI8개(docs·recovery3.11/3.13·tools Ubuntu/Windows·secret-scan·
check-versions·packages)가 모두 SUCCESS임을 문서 종결 전 실제 GH에서 확인했다.
[문서/도구 CI](https://github.com/digitie/kor-travel-common/actions/runs/38837256748),
[Python CI](https://github.com/digitie/kor-travel-common/actions/runs/38837256602).
이 문서 종결 commit의 CI는 최종 HEAD에서 다시 확인하며 기존 성공을 전용하지 않는다.

이번 commit은 원문/통합 disposition·색인과 관련 상태 기록만 바꾼 closure이며
agent workflow의 closure 예외를 적용한다. source·테스트·의존성·규범 계약은 바꾸지 않는다.
소비자 등록/이전 센서 중지·pending 정산·이미지·실제 worker 유실 뒤 완주·운영 CPU/RSS·
live E2E는 NOT_RUN/외부 선행이다. T-319 전역 IN_PROGRESS와 소비자 소유권을 유지한다.
[PR35](https://github.com/digitie/kor-travel-common/pull/35)의 최종 CI/병합 판단은 별도다.
