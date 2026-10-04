# Dagster 최종 메타데이터 delta manifest

기준·scope·격리는 [post-fix manifest](2026-10-04-dagster-recovery-post-fix-manifest.md)를 유지한다.
동일 고정 객체를 두 reviewer가 독립 확인한다.

| 저장소 | 최종 코드 후보 | 이전 재검토 후보 |
|---|---|---|
| common | `ed47e9af09bcb48ee1507c9a17db392e44e4c3e2` | `50d2db4c7c7e0154dd863defb62d4b9fa3b5bec3` |
| weather | `74882e1ef3098ee3b749e3139dabe2dae96136cb` | `1218c8f656408d04f745bf5773ec910a36538bc5` |

common CI에서 SPDX Origin 행 끝의 noqa가 출처 형식으로 해석되어 실패했다.
출처 행은 정본 원천 경로만 남기고 ruff E501 예외를 별도 주석으로 분리했다.
실행 코드는 동일하다. weather는 Python dependency와 lock의 common SHA만 재고정했다.
UI archive는 원래 검토된 `50d2db4`와 동일하며 새 UI source/build 변경은 없다.

직접 실행: common ruff/SPDX PASS; weather 전체 pytest 345 PASS(453.69초),
frontend clean install/type-check/64 tests/lint/production build PASS, common clean tarball
소비자 production build/webpack PASS. 라이브 UI 로그인 실패·성공·로그아웃, 실패 상세,
job별 정체 판정·스케줄 상세·모바일 overflow·오류 색상, Dagster 중단/복원 후 재시도는
최종 evidence에 기록한다. 마지막 메타데이터 delta CI는 진행 중이다.

새 source finding과 이전 review 조건 충족을 확인하고 별도 final-delta 원본을 저장한다.
상대 final-delta 결과는 두 보고서 확정 전 공유하지 않는다. 운영 배포/RSS 실측은 범위 밖이다.
