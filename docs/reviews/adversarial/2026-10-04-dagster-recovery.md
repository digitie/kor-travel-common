# 2026-10-04 Dagster 복구·메모리·공용 UI 적대적 리뷰

- Review ID: DAGSTER-RECOVERY-20261004.
- 종류: 전문 리뷰어 서브에이전트 2인 독립 적대적 리뷰, 원본→post-fix→최종 주석 delta.
- Base: common `be7f21f2a645f4ce882b3d841487e1b40ad23425`,
  weather `5da6e158dccc8ea98e8301078ce9610525da0ebf`.
- 최초 후보: common `270619b` / weather `709dc44`.
- 최종 코드: common `ed47e9af09bcb48ee1507c9a17db392e44e4c3e2`,
  weather `74882e1ef3098ee3b749e3139dabe2dae96136cb`.
- 범위: common Python/UI/가이드·artifact·CI, weather recovery SQL/정책/메모리/소비자 UI.
- 범위 밖: 운영 배포·다른 소비자 실제 이관·provider client 구현.
- 관련: [T-319](../../tasks/T-319-dagster-recovery.md), [T-216](../../tasks/T-216-dagster-operations.md).
- Coordinator: Codex `/root`; 검토 2026-10-04 KST.
- 상태: COMPLETE, 코드 finding 8건 FIXED, 최종 PR closure CI 확인 후 merge.

## 1. 동일 manifest와 독립성

[최초](evidence/2026-10-04-dagster-recovery-manifest.md),
[post-fix](evidence/2026-10-04-dagster-recovery-post-fix-manifest.md),
[최종 delta](evidence/2026-10-04-dagster-recovery-final-delta-manifest.md)를 동일하게 전달했다.
각 단계에서 두 원본을 저장하기 전 상대 finding을 공유하지 않았다.
격리는 immutable Windows Git object-only이며 source checkout/수정·운영 조작이 없다.
full hash 및 clean/diff 검증·실행 ID/시간은 아래 원본을 보존한다.
저장 정규화 note: B post-fix/final-delta 원본의 EOF 빈 줄만 제거했다. 문장·판정은 동일하다.

| reviewer | 전문 영역·실행 | 최초 원본·verdict | post-fix 원본·verdict | 최종 delta |
|---|---|---|---|---|
| A `/root/review_ui` | UI·artifact·소비자 보안/접근성 | [A](evidence/2026-10-04-dagster-recovery-reviewer-a.md) BLOCK | [A post-fix](evidence/2026-10-04-dagster-recovery-post-fix-reviewer-a.md) CONDITIONAL(테스트/CI) | [A final](evidence/2026-10-04-dagster-recovery-final-delta-reviewer-a.md) 코드 PASS |
| B `/root/review_recovery` | lease·회수·멱등성·메모리 | [B](evidence/2026-10-04-dagster-recovery-reviewer-b.md) CONDITIONAL | [B post-fix](evidence/2026-10-04-dagster-recovery-post-fix-reviewer-b.md) PASS | [B final](evidence/2026-10-04-dagster-recovery-final-delta-reviewer-b.md) PASS |

## 2. Findings와 disposition

| ID | 심각도·실패 형태·영향 | 반영 결과 | 재확인 |
|---|---|---|---|
| A-P2-01 | 존재하지 않는 error 토큰으로 실패 색상 누락 | destructive 정본 토큰/존재 검사, FIXED | A post-fix |
| A-P2-02 | 동명 schedule의 repository context 유실로 잘못된 링크/expand | location/repository/name 복합 identity와 context 콜백, FIXED | A post-fix·2repo 회귀 |
| A-P3-01 | public slot/testId·상세 header 부재 | slots/testId/접근 가능한 header/계약 문서, FIXED | A post-fix |
| A-P3-02 | wrapper 추출 뒤 소비자 gutter 누락 | 공용 root를 기존 responsive margin selector에 포함, FIXED | A post-fix·live 모바일 |
| B-P2-01 | 특보 전국 fan-out 전체 fact 누적·앞 notice skip 숨김 | 5000 fact/25 source flush·누적 예산·skip union/게시 집합, FIXED | B post-fix·특보 회귀 |
| B-P2-02 | 앞 100개 생존 run 때문에 뒤 terminal run 회수 기아 | started_at/run_id keyset 순회 및 tie-breaker, FIXED | B post-fix·limit1 동시간 회귀 |
| B-P2-03 | nan/inf/float/bool/문자열 false로 정책 무력화 | 실제 int/non-bool·실제 bool 엄격 검사, FIXED | B AST 직접 실행·8경계 회귀 |
| B-P2-04 | architecture가 새 부분 commit 계약과 충돌 | 부분 게시/누적 예산/역사 메모리 수치·특보 불완전 계약 갱신, FIXED | B post-fix |

P0/P1은 없었다. 원본 finding별 근거·권고는 위 reviewer 원본 그대로다.
여덟 건 모두 원 reviewer가 수정 재확인했고 새 finding은 없다. DEFERRED/기각은 없다.
최초 B의 Dagster1.13.20 표기는 원본을 보존하고 B post-fix에서 실제1.13.24로 정정했다.

## 3. 추가 실측 결함·최종 검증

live Dagster의 로그 서버 상한1000과 기존 UI limit2000 충돌도 수정했다.
cursor/최대20page/20초 다음 요청 시작 예산/각10초 timeout, best-effort 실패 상세를
추가했다. 두 reviewer가 전체 delta를 검토했고 live 실패 원인 표시가 확인되었다.
Origin inline noqa와 tgz integrity의 초기 CI 실패도 수정했다.

전체 회귀·clean artifact·브라우저 증거와 합성 메모리 실측은
[최종 live e2e 기록](evidence/2026-10-04-dagster-live-e2e.md)에 연결한다.
weather345 Python/64 frontend, common21 Python/34 UI, floor21, tarball clean build,
로그인/로그아웃·메뉴·실패 상세·job 상한·모바일·연결 중단/복구를 PASS로 확인했다.

최종 코드 후보 CI 전부 PASS:
[common 검사](https://github.com/digitie/kor-travel-common/actions/runs/37167871221),
[Python matrix](https://github.com/digitie/kor-travel-common/actions/runs/37167871194),
[재사용 workflow](https://github.com/digitie/kor-travel-common/actions/runs/37167871423),
[weather](https://github.com/digitie/kor-travel-weather/actions/runs/37167886226).
이후 evidence-only closure도 PR check를 모두 통과한 뒤 merge한다.

## 4. 최종 판정

- Coordinator verdict: PASS, 코드 finding 열린0. A의 테스트 조건은 실제 회귀/live로 충족했다.
  [A 실행 evidence 재확인](evidence/2026-10-04-dagster-recovery-evidence-reviewer-a.md)도 PASS다.
- reviewer 원본을 수정하지 않으며 코드 PASS와 부모 실행 evidence를 구분한다.
- NOT_RUN: 운영 daemon 적용/launcher crash·hard hang 장애 주입/OS 회수/RSS·다른 앱 채택.
  합성 Python 피크 약97% 감소를 운영 RSS 보증으로 사용하지 않는다.
- 적용 안내: [Dagster 가이드](../../runbooks/dagster-adoption.md).
- PR: [common #24](https://github.com/digitie/kor-travel-common/pull/24),
  [weather #72](https://github.com/digitie/kor-travel-weather/pull/72).
