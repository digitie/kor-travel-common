# Common PinVi 채택 후속 검증 (2026-10-05)

최종 Common 제품 `e28559803c1ec1134ef7ba7736b9acf4cadb9a32`/UI dev.6,
이전 cap 표현 제품 `874612052a4f7849074d1775b4a83a8f58a793cf`/UI dev.4, base `c0f5235`.
복구/소비자 계약과 UI/타입의 두 독립 reviewer가 전체 제품 delta를 검토하고 post-fix PASS했다.
[원문 manifest](../common-dagster-2026-10-05/manifest.json)는 최초 조건부 문서 지적과 closure를
UTF-8 원문/SHA256으로 보존한다. nullable schedule callback migration과 runtime cap 미확인 설명을
Breaking/Migration/runbook에 반영했다. 미해결 신규 P0/P1/P2 없음.

UI50/check/build·실제 tarball npm ci/Next smoke PASS. 도구 unittest337 PASS/1 skip,
문서 링크·plan gate PASS. packages CI의 dev.3 fixture 불일치를 dev.4 exact SHA512 lock으로 수정했다.
기존 dev.3 artifact를 바꾸지 않고 최종 dev.6 SHA256
`e4945d01d9eb89ed505a95b551899fd0ecf41be66c9ee6b76246701350447e6d`를 PinVi에 그대로 vendoring했다.

소비자 PinVi 46305d44의 별도 PR #575에서 N150 실제 API/GraphQL/Alembic0102/Chromium·Firefox
최종 dev.6 4건(1.0분) PASS: 로그인/RBAC·오래된 active scope·실행 상세/URL·Dagster webserver stop/start
semantic outage/last-good recovery·390px overflow. 상세/원문/캡처는
[PinVi 검증 기록](https://github.com/digitie/pinvi/blob/codex/common-dagster-recovery/docs/reviews/common-dagster-2026-10-05/README.md).
reviewer 본인의 live 실행으로 집계하지 않는다.

dev.5 mobile min-width가 공통 기본 옵션에서 페이지 전체로 전파되는 P2를 발견해 dev.6에서 grid direct child min-width0로 수정했다. 기존 BLOCK/조건부와 post-fix 원문은 불변 보존했다. N150 실제 설치 컴포넌트 SSR/CSS의 두 옵션×6폭×2브라우저 24조합과 실제 PinVi React UI keyboard2건이 통과했다. 전체 폭/표 scroll/focus·ArrowRight와 후보/artifact/CSS SHA는 [정량 근거](https://github.com/digitie/pinvi/blob/codex/common-dagster-recovery/docs/reviews/common-dagster-2026-10-05/mobile-readability-dev6.json)에 연결한다. SSR layout gate와 실제 API/UI gate를 구분한다. PinVi에서 발견한 Definitions gRPC 중복은 소비자
fix/실제 CLI 회귀로 해결하고 공통 구현 가이드에 예방 gate를 추가했다.

Common CodeGraph index가 비어 semantic 조회를 하지 못해 현재 모듈/호출자 수동 trace로 대체했다.
운영 shared daemon 배포/worker kill/RSS·외부 provider 호출은 NOT_RUN이다. synthetic allocation과
실제 운영 RSS는 구분한다. T-301 원본 worktree는 보존했다. 최종 문서 CI 후 Common #27을 먼저 merge하고
PinVi #575의 최종 ready Aggregate gate를 통과해 merge한다.
