# T-503 회수 지표 1회차 보고 `docs/reports/adoption-2026-Q4.md` 정리

- 상태: BLOCKED
- 우선순위: P2
- Gate: 문서 검증
- 선행: T-411, T-461

## 목표

common 도입이 실제로 시간을 회수하는지 첫 분기(2026-Q4, 2026-10-01~2026-12-31) 측정치로 보고한다. 측정 항목은 브리프 D-28이 정한 지표이며, 보고서는 "확대/유지/축소" 판정과 그 근거를 담는다. 이 task는 측정과 판정만 하고 범위 축소·배포 방식 재검토 자체는 후속 task(T-507·T-508 또는 신규)로 넘긴다.

## 고정 결정

- 지표: 원본 수정 시간·타 앱 반영 시간·검증 시간·회귀 수·로컬 복사본 수(선행 보고서 §11; `docs/survey/README.md` §2.2 참조) + drift 수·EXEMPT 수·enforce 전환 수. 분기 파일 `docs/reports/adoption-YYYY-QN.md`. 순절감 ≤0 2분기 → 범위 축소, npm 소비자 우회 패치 ≥2 → 배포 방식 재검토: 브리프 D-28.
- 회수 식: 회수 기간(개월) = 초기 이관 시간 ÷ (월간 절감 − 월간 common 유지·릴리스·소비자 갱신 시간). 숫자는 측정값이며 예측으로 쓰지 않는다(선행 보고서 §11).
- 우회 패치 탐지는 `tools/ui_drift.py`(T-211)가 정본; 없으면 grep 대체와 한계 기록: 브리프 D-10, [ui-contract](../standards/ui-contract.md).
- drift·EXEMPT 수는 `check_versions` report JSON과 [integration-map](../integration-map.md)(생성물)에서 읽는다: 브리프 D-07·D-19.
- 단독 유지자 전제(공통 API·릴리스 담당과 소비자 통합 담당 겸임): 브리프 D-33 — 시간 지표는 역할별로 나눠 적는다.
- 근거: `docs/survey/cross/ui-components.md` §2.1(map↔pinvi 27쌍 전부 상이 = 복사본 drift의 기준 상태), 선행 보고서 §3.2(geo 반복 동기화 비용).

## 구현 범위

1. `docs/reports/README.md`(색인 1단락: 파일 명명 `adoption-YYYY-QN.md`·`drift-audit-YYYY-QN.md`, 갱신 규칙) + `docs/reports/adoption-2026-Q4.md`.
2. 측정 방법 정의(보고서 §1): 각 지표의 데이터 원천(소비자 PR 타임스탬프, `docs/journal.md`, CI run, `check_versions` JSON, `ui_drift.py` 출력)과 계산 규칙. 원천이 없는 지표는 `NOT_MEASURED(사유)`.
3. 측정(보고서 §2): 분기 내 common 릴리스 목록(태그), 소비자 채택 PR 목록(T-410·T-411·T-461 등), 각 지표 값과 근거 링크.
4. 판정(보고서 §3): 회수 식 계산(가정 명시), D-28 트리거 2종 대조, 판정 `확대/유지/축소` + 다음 분기 측정 개선 항목.
5. [문서 지도](../README.md)에 `docs/reports/` 행 추가, `docs/runbooks/documentation-maintenance.md` §1 표의 `docs/reports/` 행 추가는 coordinator 소유 파일이므로 open item으로 보고.

## 범위 밖

- 지표 수집 자동화 도구(필요하면 T-506 감사 runbook에서 제안).
- 판정 결과에 따른 범위 축소·배포 방식 변경(별도 task·ADR).
- 소비자 저장소 수정.

## 예상 변경 파일

예정 경로는 존재·실행 증거가 아니다.

```text
docs/reports/README.md                    (신설)
docs/reports/adoption-2026-Q4.md          (신설)
docs/README.md                            (문서 지도 행 추가)
docs/journal.md, docs/resume.md, docs/tasks/T-503-adoption-report-2026-q4.md
```

## 수용 기준

- 보고서에 8개 지표(시간 3·회귀·복사본·drift·EXEMPT·enforce 전환) 각각의 정의·원천·값·근거 링크가 표로 있다. 값이 없는 지표는 `NOT_MEASURED(사유)`이며 0으로 적지 않는다.
- 분기 내 common 태그 목록과 소비자 채택 PR 목록이 저장소·PR 번호·merge 일자와 함께 있다.
- 회수 식 계산에 쓴 가정(초기 이관 시간의 산정 범위, 월 환산)이 명시돼 있고, 결과를 "예측"이 아닌 "1분기 측정"으로 표기한다.
- D-28 트리거 2종(순절감 ≤0, 우회 패치 ≥2)에 대한 충족 여부와 후속 task 제안이 있다.
- `ui_drift.py` 실행 결과(또는 `NOT_RUN(사유)`와 grep 대체 결과)가 첨부돼 있다.
- `docs/reports/`가 문서 지도에 있고 두 validator가 통과한다.
- 보고서는 조사 문서(`docs/survey/`)를 고치지 않는다.

## 검증 명령

```bash
git tag --list 'tokens-v*' 'ui-v*' 'py-v*' --format='%(refname:short) %(creatordate:short)'
gh pr list --repo digitie/kor-travel-map --state merged --search "kor-travel-common" --json number,title,mergedAt
python3 -B -X utf8 tools/check_versions.py --registry versions.json --manifest <consumer>/kor-travel-common.lock.json --mode report --json /tmp/versions-<repo>.json
python3 -B -X utf8 tools/ui_drift.py --pins consumers.pins.json
python3 -B -X utf8 tools/validate_document_links.py
python3 -B -X utf8 tools/validate_plan.py
```

인자 이름은 [tools/README.md](../../tools/README.md)의 최종 인터페이스를 따른다. Git Bash에서 동일하게 실행한다.

## evidence

- 보고서 자체가 evidence다. 원천 링크(PR·run URL·JSON 파일명)를 보고서 안에 둔다.
- `docs/journal.md` 최신 항목에 측정 명령·NOT_MEASURED 목록·도구 버전을 남긴다.

## rollback 또는 release 차단 조건

- 문서 task이므로 코드 rollback은 없다. 측정 오류가 발견되면 보고서를 덮어쓰지 않고 correction note와 날짜를 남긴다([documentation maintenance](../runbooks/documentation-maintenance.md) §5-5와 같은 방식).
- 판정이 "축소"여도 이 task에서 패키지 범위를 바꾸지 않는다. 축소는 ADR + 새 task로만 효력을 가진다.
