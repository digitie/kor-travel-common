# T-506 분기별 cross-repo drift 감사 runbook + 첫 실행 + 조사 기준 커밋 갱신 절

- 상태: BLOCKED
- 우선순위: P2
- Gate: 문서 검증
- 선행: T-012

## 목표

7개 소비자와 common 사이의 drift(버전 격차·만료 예외·매니페스트 불일치·OpenAPI 예외 review 도래·contrast/ux baseline 잔존·npm 소비자 우회 패치·provider SHA 변화)를 분기마다 같은 절차로 감사하는 runbook을 만들고 첫 실행 결과를 남긴다. 같은 실행에서 조사 문서(`docs/survey/`)의 기준 커밋을 갱신한 새 절을 추가한다(본문 불변).

## 고정 결정

- 조사 문서는 분기 감사(T-506) 때 기준 커밋을 갱신한 **새 절로만** 확장: 브리프 D-33; [documentation maintenance](../runbooks/documentation-maintenance.md) §2 "조사 기준 커밋 갱신" 행; `docs/survey/README.md` §8 갱신 규칙.
- drift·EXEMPT·enforce 전환 수는 분기 보고 지표(D-28); 이 task의 감사 report가 T-503 보고서의 원천이 된다.
- `exceptions[].until` 필수, `EXEMPT_EXPIRED`는 report 모드에서도 `::error::`: 브리프 D-07, [versions 규칙](../standards/versions.md).
- OpenAPI 예외 레지스트리 항목은 `review` 날짜 필수: 브리프 D-14, [openapi 규칙](../standards/openapi.md).
- `docs/integration-map.md`는 `tools/collect_manifests.py` 생성물(수기 편집 금지): 브리프 D-19, ADR-010([ADR 색인](../adr/README.md)).
- 근거: `docs/survey/cross/version-matrix.md` §7.4(봇 부재·수동 갱신 관행), `docs/survey/cross/ci-deploy.md` §4(`consumer-smoke` pinned SHA), 판정 보고서 `docs/plan/design-panel/judge-directive-fidelity.md` M-12(재조사 주기).

## 구현 범위

1. runbook `docs/runbooks/quarterly-drift-audit.md` 신설 + [runbooks README](../runbooks/README.md) 표 행 추가. 절 구성: ① `consumers.pins.json` 각 소비자 SHA를 현재 `main`으로 갱신(PR) ② `collect_manifests.py` → `docs/integration-map.md` 재생성 ③ 소비자 7곳 `check_versions --mode report` JSON 수집 ④ 만료·도래 예외 목록(`versions.json` `exceptions[].until`, `openapi-exceptions.yaml` `review`, `contrast-baseline.json` `until`) ⑤ ux baseline 잔존 수(`ux_lint` 전체 report) ⑥ `ui_drift.py` 우회 패치 수 ⑦ provider SHA 변화(`providers` 절 대조) ⑧ 판정 표 + 후속 task 생성 규칙(만료 예외 = 연장 PR 또는 T-4xx 하위 task) ⑨ 조사 기준 커밋 갱신 절 작성 규칙 ⑩ report 파일 `docs/reports/drift-audit-YYYY-QN.md`.
2. 첫 실행: `docs/reports/drift-audit-2026-Q4.md`(소비자 × 축 판정 표; 실행 못 한 항목 `NOT_RUN(사유)`).
3. `docs/survey/README.md`에 "§2.1 기준 커밋(2026-Q4 감사)" 같은 새 절을 추가해 7 저장소의 감사 시점 커밋을 표로 기록. 기존 절·인벤토리·횡단 문서 본문은 수정하지 않는다.
4. T-503 보고서와의 역할 분리를 runbook에 1문장으로 명시(감사 = 사실 수집, 회수 보고 = 경제성 판정).

## 범위 밖

- 발견된 drift의 실제 해소(각 앱 T-4xx, 승격 T-502, 재평가 T-507).
- 조사 문서 본문 재작성·수치 정정(README §6.2 정정 기록 방식만).
- 감사 자동화 워크플로(첫 실행은 수동; 자동화는 2회차 이후 판단).

## 예상 변경 파일

예정 경로는 존재·실행 증거가 아니다.

```text
docs/runbooks/quarterly-drift-audit.md     (신설)
docs/runbooks/README.md                    (행 추가)
docs/reports/drift-audit-2026-Q4.md        (신설; docs/reports/README.md는 T-503과 먼저 끝나는 쪽이 만든다)
docs/survey/README.md                      (새 절 추가만)
consumers.pins.json                        (SHA 갱신)
docs/integration-map.md                    (생성물 재생성)
docs/journal.md, docs/resume.md, docs/tasks/T-506-quarterly-drift-audit.md
```

## 수용 기준

- runbook의 10개 절 각각에 입력·명령·판정 기준·출력 위치가 있고, 규범(D-07·D-14·D-19)을 복제하지 않고 링크한다.
- 첫 실행 report에 7 소비자 × 7 축(버전·매니페스트·versions 예외·openapi 예외·contrast·ux·우회 패치) 표가 있고 각 셀이 값 또는 `NOT_RUN(사유)`다. 0건은 실행 증거(JSON 파일명·run URL)와 함께만 적는다.
- 만료·30일 내 도래 예외마다 후속(연장 PR 또는 task ID)이 적혀 있다.
- `git diff --stat -- docs/survey/`가 `docs/survey/README.md` 1파일만 보여 주고, 그 diff는 새 절 추가뿐이다.
- `docs/integration-map.md`가 재생성물이며 수기 diff가 없다(`collect_manifests.py` 재실행 시 diff 0).
- `consumers.pins.json` 갱신 후 `consumer-smoke` 1회 green run URL이 있다(실패면 report에 기록하고 pin을 되돌린다).
- 두 validator가 통과한다.

## 검증 명령

```bash
python3 -B -X utf8 tools/collect_manifests.py --pins consumers.pins.json --out docs/integration-map.md && git diff --exit-code -- docs/integration-map.md
for m in <consumer-checkout>/*/kor-travel-common.lock.json; do python3 -B -X utf8 tools/check_versions.py --registry versions.json --manifest "$m" --mode report --json "/tmp/drift-$(basename $(dirname "$m")).json"; done
python3 -B -X utf8 tools/ux_lint.py --root <consumer-checkout> --report
python3 -B -X utf8 tools/ui_drift.py --pins consumers.pins.json
git diff --stat -- docs/survey/
gh workflow run consumer-smoke.yml && gh run list --workflow consumer-smoke.yml -L 1
python3 -B -X utf8 tools/validate_document_links.py
python3 -B -X utf8 tools/validate_plan.py
```

인자 이름은 [tools/README.md](../../tools/README.md)의 최종 인터페이스를 따른다. 소비자 체크아웃은 읽기 전용이며 파일을 만들지 않는다. Git Bash에서 동일하게 실행한다.

## evidence

- `docs/reports/drift-audit-2026-Q4.md`가 evidence다. JSON 출력은 저장소에 넣지 않고 report에 요약·파일명·실행 일시를 적는다.
- `docs/journal.md` 최신 항목에 소비자 체크아웃 커밋 7개·실행 명령·NOT_RUN 목록·도구 버전을 남긴다.

## rollback 또는 release 차단 조건

- `consumers.pins.json` 갱신으로 `consumer-smoke`가 실패하면 pin을 직전 SHA로 되돌리는 커밋을 같은 PR에 넣고, 실패 원인은 report의 후속 task로 남긴다.
- 조사 문서 본문에 diff가 생기면 그 변경을 되돌린다(정정은 `docs/survey/README.md` §6.2 방식만).
- `NOT_RUN`이 남은 축이 있으면 DONE 전 `외부 선행`으로 승격하고, report의 판정 열은 비워 둔다.
