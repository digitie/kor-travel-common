# T-502 gate 승격: `check_versions`·`kt_contrast`·`ux_lint`를 소비자별 2회 green 후 `enforce: fail`(common PR) + 승격 절차 runbook

- 상태: BLOCKED
- 우선순위: P2
- Gate: CI
- 선행: T-403, T-103

## 목표

Phase 1~4에서 `report` 모드로 돌던 세 gate(`tools/check_versions.py`, `tools/kt_contrast.py`, `tools/ux_lint.py`)를 소비자별로 `fail`로 승격하는 절차를 runbook으로 고정하고, 승격 조건(해당 소비자 report 2회 연속 위반 0)을 충족한 소비자부터 common `versions.json`의 `consumers.<repo>.enforce`를 바꾸는 PR을 실제로 1회 이상 만든다. 강등(fail → report) 절차도 같은 runbook에 둔다.

## 고정 결정

- 모드 3단 `report → warn → fail`, 승격 권한은 common `versions.json`이 소유하고 앱 자율 선언은 기각: 브리프 D-07·D-30, ADR-008([ADR 색인](../adr/README.md)), [versions 규칙](../standards/versions.md).
- 승격 조건 = 해당 소비자 report 2회 연속 위반 0(D-07). `FLOATING_REF`·`BLOCKED`·`EXEMPT_EXPIRED`는 report 모드에서도 `::error::` 주석.
- `kt_contrast`는 report 기본 + 앱 `contrast-baseline.json`(미달 쌍 + `until`), 승격 후에도 **신규 미달만** fail: 브리프 D-12, [design-tokens 규칙](../standards/design-tokens.md).
- `ux_lint`는 채택 시점부터 `--base <sha>` diff-based fail + 전체 report(D-13·D-30). 이 task에서의 승격 대상은 "전체 report에 남은 baseline 잔존(`window.confirm` 7건 등)의 소진 후 전체 fail 전환" 판정이다: [ux-guide](../standards/ux-guide.md).
- 소비자 워크플로는 common 재사용 워크플로를 태그/SHA로 호출하고 job `name:`을 유지(D-18); 승격은 소비자 워크플로 수정 없이 common 레지스트리 값만 바꿔 전파된다.
- 근거: `docs/survey/cross/version-matrix.md` §7.4(봇 없이 "격차를 실패가 아닌 보고로" 내는 단계가 선행), `docs/survey/inventory/kor-travel-docker-manager.md` §8-18·19(fail-close 레지스트리 선례), 판정 보고서 `docs/plan/design-panel/judge-directive-fidelity.md` O12.

## 구현 범위

1. runbook `docs/runbooks/gate-promotion.md` 신설 + [runbooks README](../runbooks/README.md) 표에 행 추가. 절: 입력(소비자·도구·최근 2회 run URL) → 판정 표(2회 연속 위반 0, 만료 예외 0, `FLOATING_REF`/`BLOCKED` 0) → `versions.json` 변경 diff 규칙(승격 소비자 1곳 또는 도구 1종만) → 승격 PR 본문 항목 → 승격 후 첫 소비자 CI 확인 → 강등 조건·명령.
2. `enforce` 값의 도구별 분리 여부 확인: [versions 규칙](../standards/versions.md)이 정한 스키마를 따르고, 스칼라 1개뿐이면 `enforce.{versions,contrast,ux}` 형태로 확장하는 스키마 minor 변경을 이 task에서 제안한다(열림(사용자 확인 필요); 기본값 = 도구별 키).
3. 첫 승격 PR: 조건을 가장 먼저 충족한 소비자(예상: map 또는 weather — 외부 선행이 없는 트랙, `docs/plan/design-panel/judge-migration-feasibility.md` §3.1)부터 `check_versions` → `kt_contrast` 순으로 승격. 2인 리뷰(`versions.json`은 비면제, D-04).
4. `tests/test_check_versions.py`에 `enforce: fail`일 때 exit 1·`report`일 때 exit 0 회귀 케이스가 없으면 추가.

## 범위 밖

- 소비자 저장소 워크플로 파일 수정(재사용 워크플로 호출 자체는 T-403).
- `exceptions[]` 신규 등록·`until` 연장 판단(분기 감사 T-506, 재평가 T-507).
- ux baseline 잔존 항목의 실제 코드 수정(각 앱 T-4xx).

## 예상 변경 파일

예정 경로는 존재·실행 증거가 아니다.

```text
docs/runbooks/gate-promotion.md            (신설)
docs/runbooks/README.md                    (행 추가)
versions.json                              (consumers.<repo>.enforce 값만)
docs/standards/versions.md                 (enforce 키 형태를 바꿀 때만)
tools/check_versions.py, tests/test_check_versions.py   (enforce 키 형태를 바꿀 때만)
docs/journal.md, docs/resume.md, docs/tasks/T-502-gate-promotion-enforce-fail.md
```

## 수용 기준

- runbook에 승격 판정 표·PR 본문 항목·강등 절차·"승격은 common PR만" 문장이 있고 다른 문서(D-07 정본)를 복제하지 않는다.
- 첫 승격 PR의 `versions.json` diff가 `consumers.<repo>.enforce` 값 외의 줄을 바꾸지 않는다.
- 승격된 소비자·도구마다 직전 2회 연속 위반 0인 CI run URL 2개가 evidence에 있다(같은 커밋의 재실행은 1회로 센다).
- 승격 후 해당 소비자 CI가 fail 모드로 1회 green이고 run URL이 evidence에 있다.
- 로컬에서 `check_versions.py --mode fail`이 해당 소비자 lockfile에 대해 exit 0이다.
- `EXEMPT_EXPIRED`·`FLOATING_REF`·`BLOCKED`가 승격 소비자에서 0이다.
- `kt_contrast` 승격 소비자는 `contrast-baseline.json`이 매니페스트 `contrast.baseline`에 등록돼 있고 신규 미달 0이다.
- 2인 리뷰 report가 [review archive](../reviews/README.md)에 있다.

## 검증 명령

```bash
python3 -B -X utf8 tools/check_versions.py --registry versions.json --manifest <consumer>/kor-travel-common.lock.json --mode fail; echo "exit=$?"
python3 -B -X utf8 tools/kt_contrast.py --tokens <consumer>/<override>.css --baseline <consumer>/contrast-baseline.json --mode fail; echo "exit=$?"
python3 -B -X utf8 -m unittest discover -s tests -p "test_check_versions.py"
gh run list --repo digitie/<consumer> --workflow versions-check -L 3 --json conclusion,url,headSha
python3 -B -X utf8 tools/validate_document_links.py
python3 -B -X utf8 tools/validate_plan.py
```

인자 이름은 [tools/README.md](../../tools/README.md)의 최종 인터페이스를 따른다. Git Bash에서 동일하게 실행한다.

## evidence

- 이 파일 하단 표: 소비자 × 도구 × (run URL 1·2, 승격 PR, 승격 후 run URL, exit code).
- `docs/journal.md` 최신 항목에 실행 명령·도구 버전·NOT_RUN 목록. 실행하지 못한 소비자는 `NOT_RUN(사유)`로 남기고 승격하지 않는다.

## rollback 또는 release 차단 조건

- 승격 후 첫 소비자 CI가 fail이면 `versions.json`의 해당 값을 `report`로 되돌리는 common PR을 즉시 만든다(`git revert` 1회). 소비자 저장소는 손대지 않는다.
- 2회 연속 green evidence가 없는 소비자를 승격한 PR은 merge하지 않는다.
- `enforce` 키 형태를 바꾸는 변경은 스키마 minor 상향 + `tests/test_check_versions.py` 통과 전에는 merge하지 않는다.
