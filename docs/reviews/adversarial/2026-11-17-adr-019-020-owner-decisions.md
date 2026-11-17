# 적대 리뷰: ADR-019·ADR-020과 T-416 결정 반영(2026-11-17)

- review ID: R-2026-11-17-ADR019-020
- 종류: 문서 FULL(결정 기록·task DAG)
- 기준선: 브랜치 `docs/claude-adr-019-020-owner-decisions`의 `aa3e0bc` 대 `origin/main` `18df49a`
- 범위 밖: 패키지 코드·workflow 구현(T-024), Map PR(ADR-124)의 코드, T-486b 영향 자료
- 리뷰어: A(문서·계획 정합·원장 규칙), B(guard workflow·검사기 사실 대조·순서). 서로의 결과를 보지 않고 독립 실행했다. 둘 다 읽기 전용(git show/diff/grep, curl).
- 시각: 2026-11-17, 두 리뷰 모두 같은 세션 안에서 시작·종료

## 결과

| 리뷰어 | verdict | BLOCKER | MAJOR | MINOR |
|---|---|---|---|---|
| A | PASS-with-fixes | 0 | 4 | 8 |
| B | PASS-with-fixes | 0 | 3 | 2 |

두 리뷰가 확인한 사실: nodejs.org 색인의 최신 LTS patch는 26.13.1(Lithium, 2026-11-10, npm 11.20.0)이고 더 새 항목은 `v27.0.0-alpha` 뿐이다. npm 12.0.1의 `engines.node`는 Node 26을 받는다. `97f8ed9` 판 workflow·검사기는 `origin/main`과 같고 정책과 Node/npm 축을 `main`에서 읽는다. pinvi·weather·transport·docker-manager·geo·concierge가 `97f8ed9`, Map이 `55a921b`를 호출한다. `55a921b` 판에는 도구 단계가 없고 검사기가 `engines`·`.nvmrc`를 읽지 않으므로 Map의 Node 26.13.1 핀이 현재 guard를 깨지 않는다. ADR-020은 §1.5의 15행을 빠짐없이 옮겼고 집계(수락 12·보류 2·나눔 1)가 맞다.

## finding과 disposition

| ID | 심각도 | 내용 | disposition |
|---|---|---|---|
| A1 | P1 | T-023을 리뷰 2인·수용 기준 체크 전에 DONE으로 옮김 | FIXED: 두 리뷰 뒤 수용 기준 체크, H1·완료 요약에 날짜·PR, evidence에 이 report |
| A2 | P1 | resume·journal 미갱신 | FIXED |
| A3 | P1 | T-417 본문(고정 결정·구현 범위)이 T-024 채택 커밋을 그대로 가리킴 | FIXED: T-029 병합 커밋(또는 그 뒤 common 지정 커밋)으로, 구현 범위 2는 남은 입력만 |
| A4 / B2 | P1 | T-029가 geo·concierge를 공지로만 다룸. 병합일에 두 저장소 guard가 실패 | FIXED: 외부 선행에 옛 판 호출자 전부의 이전, ADR-019 결정 5·결과 정정 |
| A4 | P1 | 공통 축 상향은 Map 질의에 대한 답을 넘는다 | FIXED: T-029 외부 선행에 소유자 확인 |
| B1 | P1 | "당일 Node 갱신 확인" 우회는 불가능(옛 판은 Node 22.23.1로 실행하고 `--runtime`으로 main 축과 대조) | FIXED: 우회 삭제, 이유를 ADR-019 결정 5와 T-029에 |
| B3 | P1 | guard 자신의 `setup-node 22.23.1`·`npm@12.0.1`이 T-024 범위에 없음 | FIXED: ADR-019 결정 1, T-024 구현 범위 1과 selftest 수용 기준 |
| B4 | P2 | T-029의 T-025 선행 근거가 틀림(Node 축은 `runtime`이라 생성 정책에 없다) | FIXED: 선행 T-024만, 예상 파일·수용 기준 정정 |
| B5 | P2 | `@types/node` 범위 미기재 | FIXED: T-029 범위 밖·고정 결정 |
| A5 | P2 | 호출 SHA = `common-ref`는 workflow가 강제하지 못함 | FIXED: 소비자 수용 기준이 지키고 T-024가 가능하면 확인한다고 정정 |
| A6 | P3 | 옮길 문장에 `check:dependencies` 명령 줄 불변 누락, 대안 4 문구 | FIXED |
| A7 | P2 | ADR-020 Supersedes·모듈 수·보류 조건 부정확 | FIXED: C1~C21 중 해당 14개 모듈만, 보류 행마다 다시 열 조건 |
| A8·A9 | P3 | T-416·소비자 task 4개의 해결된 조건문 잔존 | FIXED |
| A10 | P2 | 계획 머리의 T-486b 문장과 task 파일 불일치 | FIXED 예정: T-486b에 결정 절을 영향 자료와 함께 별도 문서 PR로 넣는다 |
| A11 | P2 | T-029 수용 기준이 guard 자체를 시험하지 않음 | FIXED: Node 26.13.1 ref selftest 항목 |
| A12 | P3 | ADR 색인 갱신일, integration map의 Map ADR-124(병합 전) 표기 | FIXED |

post-fix 재검토: 반영 커밋의 문서 검증(`validate_plan` 오류 0, 링크 오류 0, `git diff --check`)만 다시 실행했다. 두 리뷰어의 post-fix 재검토는 `NOT_RUN(문서 전용 결정 기록, 소유자 지시로 즉시 병합)`이다. 새 규범 문장은 리뷰 지적을 옮긴 것에 한한다.
