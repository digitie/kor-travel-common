# Native incarnation 복구 최종 소스·문서 판정

- Review ID: common34-native-incarnation-closure-20261016. 종류: FULL 제품·post-fix·활성화 전제 문서 재검토 통합.
- 제품 기준: `d1aa4bbacab87af9ebae08757bd3fcb80f748fe9`, 최초 base `ad988a5dac252d710d41f9937b6d567c5d3398ae`.
- 문서 기준: `7f915e57f2e7fb2e3442a1346caf5f2cc7f1d633`, 제품 대비 docs5개/46추가줄. 해당 diff SHA256 `cbd87749d9894899fa150eb78bb10c52bbb095c3dc0c00642b3a05c34be23c4f`.
- 작성자 D의 closure는 원문 보관·판정 정산만 수행한다. 독립 reviewer A와 C는 서로의 원문을 읽지 않고 검토했다. 표준 archive 이름의 reviewer-b는 팀 C(`/root/geo_timeout_analysis`)이며 작성자 D의 자체 검증을 두 번째 리뷰로 세지 않는다.
- 원문의 실행 ID·시각·격리·입력·실제 검증·NOT_RUN을 수정하지 않았다. 아래 SHA는 private 전달 원문과 repo 보관본이 같다. 운영 호출/변경0, 제품 변경0.

## 원문과 판정 이력

| 단계 | 원문 | SHA256 | 판정 |
|---|---|---|---|
| A 최초 제품 | [reviewer-a](evidence/2026-10-16-native-incarnation-initial-reviewer-a.md) | `3b54abdf7a2f8c70ae745dfb6b2caa206bf4b9c74084ab7be0fdcd61f5bb441a` | BLOCK / A-P1-01 OPEN |
| A 제품 수정 | [reviewer-a](evidence/2026-10-16-native-incarnation-product-reviewer-a.md) | `c55235ab1f4e3413e0da620c9571ce4c03304714bd876ef38cb6d93622ff1fe0` | PASS / A-P1-01 FIXED |
| C 철회된 최초 초안 | [draft](evidence/2026-10-16-native-incarnation-product-reviewer-b-draft-withdrawn.md) | `61f890a1cda1904922c76755e598cdcad1e3ecc3d0cbaa41b6c52b1d0c5d1ade` | 최초 PASS 문구는 아래 정정으로 대체·최종 승인 집계0 |
| C 제품 정정 | [corrected](evidence/2026-10-16-native-incarnation-product-reviewer-b-corrected.md) | `a506fdd97df15e2e1db6525b45828cce2f169467c8514f3f3cd635c1cb229282` | SOURCE BLOCK / C-P2-01 OPEN |
| A 문서 수정 | [reviewer-a](evidence/2026-10-16-native-incarnation-activation-postfix-reviewer-a.md) | `1245d2ff4622f7e5bb10363a423e1853eb76a7d1e54202748e327b60ea1abf69` | PASS / OPEN P0/P1/P2 0 |
| C 문서 수정 | [reviewer-b](evidence/2026-10-16-native-incarnation-activation-postfix-reviewer-b.md) | `4671f6acf56746d721493dfd2b8eeab75e98b286735c44ad85b840d19d49bd62` | SOURCE PASS / C-P2-01 FIXED / OPEN P1/P2 0 |

최종 소스 판정은 A/C 두 독립 PASS, 열린 P0/P1/P2 0이다. 정정 BLOCK을 과거 PASS 초안으로 대체하지 않는다. closure commit은 이 두 판정의 원문·disposition·색인을 보관하며 규범을 바꾸지 않는다([archive 규칙](../README.md#기록-규칙)).

## Finding disposition

| ID | 심각도·문제 | 수정·재검증 | 최종 상태 |
|---|---|---|---|
| A-P1-01 | 외부 launcher의 생존 worker도 CS init 이전 실행이라는 이유로 실패 처리 | d1aa에서 정확한 DefaultRunLauncher type 및 run별 SDK gRPC 연결 태그를 검사한다. A의 실제 생존 외부 worker 모형이 STARTED/생존/SKIP을 유지했다. root의 동일 finding은 중복 집계하지 않는다. | FIXED |
| C-P2-01 | exact origin/private PID namespace만으로 구 worker 사망을 증명할 수 없는데 활성화 전제가 누락됨 | 7f915의 [가이드 §15](../../runbooks/dagster-adoption.md#15-컨테이너-재시작-뒤-native-실행-정산)에 singleton/exclusive endpoint, overlap 미지원, 구 init/worker/cgroup 소멸 증거·UNKNOWN이면 STOPPED를 명시했다. A 전체 delta PASS와 C 본인 closure PASS가 일치한다. | FIXED |

## 검증 범위와 합산 금지

- A의 제품 수정 기준 실제 Dagster1.13.24 신규83PASS/2.39초,1.13.25 신규83PASS/2.54초, 자체 SDK 모형5조건 PASS는 각 환경·기준선의 독립 실행이다. 최초58개와 더해141개라고 하지 않는다.
- C의 제품 d1aa 실제 Dagster1.13.24 신규83PASS/2.54초와 자체8조건 PASS는 같은 제품 기준의 별도 검증이다. A 결과와 합산해 전체 suite 개수로 표시하지 않는다.
- A/C 문서 재검토는 docs5개 전체 delta·제품 바이트 불변·지원/미지원 경계를 검증했다. 이전83개를 새 문서 HEAD에서 재실행한 것으로 세지 않는다.
- 7f915의 CI8개 SUCCESS를 GH에서 확인했다. closure 후속 commit의 CI는 새 SHA에서 별도로 확인하며 이 결과를 전용하지 않는다.
- 이번 archive의 links/plan/tools/diff와 staged 보안 감사 결과는 같은 PR의 journal·최종 handoff에 기록한다. 문서만 바뀌므로 제품 전체 suite는 새로 실행하지 않는다.

## 남은 gate

기본 STOPPED·소비자 pin/이미지와 제품 바이트는 그대로다. 실제 소비자 singleton/routing·구 init/worker 소멸·센서 활성화·crash/retry·live API/UI·CPU/RSS 효과는 이 소스 판정으로 완료하지 않는다. code-location이 로드되지 않거나 worker가 같은 incarnation에서 멈춘 문제까지 이 센서가 복구하지 않는다. 마지막 상태 재조회와 공식 report_run_failed 사이에는 원자 CAS가 아니므로 외부 수동 경쟁의 잔여 한계를 유지한다. 적용 정본은 [§15](../../runbooks/dagster-adoption.md#15-컨테이너-재시작-뒤-native-실행-정산), 전역 후속은 [T-319](../../tasks/T-319-dagster-recovery.md) IN_PROGRESS다. 병합/운영 변경은 이번 closure에서 수행하지 않는다.
