# T-008 docs/architecture/*(README·packages·style-delivery·consumers·adoption-readiness)·`docs/integration-map.md` 초기판 (2026-09-06, PR #1)

- 상태: DONE
- 우선순위: P0
- Gate: 문서 검증·2인 리뷰
- 선행: 없음

## 목표

현재 설계(배포 단위·의존 방향·스타일 배포 형태·소비자 7·채택 gate)를 현재형 architecture 문서로 고정하고, 소비자별 채택 상태 표의 초기판을 둔다. 이번 PR에서 산출되며 2인 리뷰 통과 후 coordinator가 `DONE` 처리한다.

## 고정 결정

- [설계 브리프](../plan/design-brief.md) D-01(배포 단위·금지 경계·의존 방향), D-09·D-10(UI 배포 방식), D-12(토큰 배포 형태), D-16(첫 소비자·순서), D-19(`integration-map.md`는 생성물·수기 편집 금지), D-20(airport Admin 정의), D-29(pinvi 사용자 표면).
- ADR-001·006·007·010 — [docs/adr/README.md](../adr/README.md).
- [문서 유지보수 runbook](../runbooks/documentation-maintenance.md) §1·§3(architecture는 현재형, machine-readable 정본은 값 파일, 연혁 금지), [canview 구조 체크리스트](../survey/cross/canview-structure-checklist.md) §3.5 R5.8·R5.9, [문서 규약 비교](../survey/cross/docs-conventions.md) §4(대응표: `packages.md`·`consumers.md`·`adoption-readiness.md`·`integration-map.md`).
- 근거: [디자인 토큰 조사](../survey/cross/design-tokens.md) §3.6.3(배포 산출물 표), [UI 컴포넌트 조사](../survey/cross/ui-components.md) §4.1~§4.3·§6.2, [공통화 매트릭스](../survey/commonality-matrix.md) §1·§3.3(전환 트랙), [판정 보고서](../plan/design-panel/judge-migration-feasibility.md) §3.1(앱별 PR 순서).

## 구현 범위

| 파일 | 내용 |
|---|---|
| `docs/architecture/README.md` | 서두 1단락(상위 인덱스·책임), 문서 표, 정본 관계(값 파일 정본: `versions.json`·`tokens.css`·`openapi-exceptions.yaml`) |
| `docs/architecture/packages.md` | 3 패키지(tokens·ui·py) 경계·`exports`·peer·의존 방향 앱 → ui → tokens, 앱 → py; 만들지 않는 것(config 패키지·api-client-core·인증·지도 엔진·provider); 패키지명 잠정(O-5) |
| `docs/architecture/style-delivery.md` | 토큰 파일 6종 + 생성물 3종, `kt-` 유틸리티 네임스페이스, 소비자 필수 2줄, `base.scoped.css` 스코프, 다크 활성화 파일, 레지스트리 채널 범위(셸·로그인·playwright 템플릿만) |
| `docs/architecture/consumers.md` | 7 소비자 × 표면(pinvi admin/사용자 웹/모바일) × 채택 대상(tokens·ui·py·규칙만) × 외부 선행(L6·L8·WIP·React 19) × 인벤토리 §8/§9 링크, 첫 소비자 순서(D-16) |
| `docs/architecture/adoption-readiness.md` | 앱별 gate 표: 라이선스·React·Tailwind·lockfile·Node CI·CI 유무·`enforce` 모드; 갱신 규칙(T-012 생성 구간은 마커 사이만) |
| `docs/integration-map.md` | 초기판(수기). 머리에 "T-012 이후 `tools/collect_manifests.py` 생성물로 대체, 그 뒤 수기 편집 금지" 1문장 |

`docs/architecture/canview-checklist.md`는 T-001 범위.

## 범위 밖

- 규칙 본문(`docs/standards/*`), ADR 본문, task 순서(`docs/plan/integration-plan.md`), 생성기(T-012), 회수 지표 보고(T-503).

## 예상 변경 파일

예정 경로는 존재·실행 증거가 아니다. `docs/architecture/README.md`, `docs/architecture/packages.md`, `docs/architecture/style-delivery.md`, `docs/architecture/consumers.md`, `docs/architecture/adoption-readiness.md`, `docs/integration-map.md`.

## 수용 기준

- 다섯 문서가 현재형이며 시간순 연혁·task 순서·acceptance를 담지 않는다(standards·ADR·task로 링크).
- `packages.md`의 금지 경계가 D-01과 글자 단위로 같고(`lucide-react` peer 없음, `maplibre-vworld-*`·`python-*-api`·인증 미포함), 의존 방향이 단방향으로 그려져 있다.
- `consumers.md` §1의 7개 저장소 행 각각에 인벤토리 §8·§9 링크가 있고 §3의 같은 저장소 행에 외부 선행이 대응한다. airport Admin 정의(D-20)·pinvi 사용자 표면 제외(D-29)가 반영된다.
- `adoption-readiness.md`의 gate 열이 `versions.json consumers.<repo>.enforce`·매니페스트 유무와 대응한다.
- `integration-map.md`에 생성물 대체 예고 문장이 있고 수기 값은 조사 기준 커밋을 명시한다.
- validator 오류 0, 리뷰어 2인(패키지 경계 · 소비자 이관) verdict `PASS`.

## 검증 명령

```bash
python3 -B -X utf8 tools/validate_document_links.py
rg -n "lucide-react|api-client-core|maplibre-vworld|python-\*-api" docs/architecture/packages.md
rg -n "collect_manifests" docs/integration-map.md
git diff --check
```

Git Bash에서 동일.

## evidence

2026-09-06 완료: 패키지 경계·릴리스별 공개 계약·외부 선행을 ADR-013과 함께 재검토했다. 소비자 7곳의 조사 §8·§9 링크 14개와 외부 선행 대응을 확인했다. 채택 지도는 기준 커밋을 명시한 미채택 초기판이며 생성기 T-012·실물 패키지 대조는 미완료로 유지한다. 조사 수치를 최신 소비자 실행으로 세지 않는다.

검증 기준선·CI·2인 gate·원본·실행 수치·NOT_RUN은 [통합 재검토](../reviews/adversarial/2026-09-06-phase0-post-fix-03.md)에 보존한다. 완료 원장 이동과 인계 문서의 후속 delta도 같은 두 리뷰어의 별도 immutable 기준선 검토 대상으로 삼으며 최신 판정은 [리뷰 색인](../reviews/README.md)을 따른다.

## rollback 또는 release 차단 조건

- 문서만 바뀌므로 `git revert` 1회로 원복한다.
- architecture가 ADR·브리프와 어긋난 채로는 T-101·T-201·T-302를 착수하지 않는다(D-01 경계가 코드에 먼저 들어가는 상황 방지).
