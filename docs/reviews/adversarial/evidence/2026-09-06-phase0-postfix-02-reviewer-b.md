# Phase 0 두 번째 post-fix 독립 적대적 리뷰 — Reviewer B 원본

- 실행 ID: `/root/reviewer_b :: 2026-09-06-phase0-postfix-02`.
- 전문 영역: 계획 DAG·순차 인계·부분 구현 상태·규약·출처·UI/Python 공개 계약.
- 요청: [이번 공통 manifest](2026-09-06-phase0-postfix-02-manifest.md) 전체와 그 문서가 지정한 최초 요청을 따랐다.
- Base: `12fb3a816e5ebbdf9822a2c17ea7ad5534195fb9`.
- 요청·실제 candidate: `84759b6611ff2a35d5f62a27e38a2878c14e0eb6`.
- PR base: `b92fabeb1c96a11c1fc9507d93271c1ebeee09b0`.
- 시작: `2026-09-06T18:40:40.3868287+09:00`.
- 검토 종료: `2026-09-06T18:43:40.3938779+09:00`.
- 격리 checkout: `F:/dev/kor-travel-common-wt/review-phase0-b`, detached HEAD. 시작·종료 HEAD 일치, `git status --porcelain=v1` 모두 빈 출력(clean).
- 독립성: 상대 reviewer의 이번 결과는 읽거나 요청하지 않았다. 추가 subagent·소비자 수정·배포·외부 승인·코드 수정을 하지 않았다. main checkout에는 지정된 이 원본 하나만 작성했다. 기존 원본은 수정하지 않았다.
- 최종 verdict: **CONDITIONAL**. 원 B finding 8건은 전부 **FIXED 유지**. 새 **P2 1건(B-P2-09)**의 문서 계약 정정 또는 명시적 disposition이 필요하다. 현재 도구 회귀·기계 검사는 통과하며 P0/P1 새 finding은 없다.

## B-P2-09 — T-005b의 빈 입력 성공 수용 기준이 유지한 CLI 계약과 충돌한다

- 위치: `docs/tasks/T-005b-check-versions-poetry-requirements.md:23`, `:38`, `:43`, `:49`. 관련 정본은 `docs/standards/versions.md:250`과 T-005 23행이다.
- 근거: 이번 변경은 T-005b 검증 지침에서 기존 positional 경로·`--manifest` CLI를 유지하도록 명시하고 앞의 두 명령을 소비자 fixture 디렉터리 입력으로 바꿨다. 그러나 구현 범위 3번과 수용 기준에는 여전히 미지원 `--lock`의 부재를 `NO_LOCK` 1행·report exit 0으로 요구한다. 마지막 명령도 입력 경로 없이 `tools/check_versions.py --repo geo`를 실행한다.
- 직접 재현: 격리 candidate에서 해당 명령을 실행하면 `소비 저장소 경로 또는 --manifest가 필요`로 실패한다. Python `subprocess.run`으로 자식 종료 코드를 따로 확인한 실제 값은 **2**다. `--self-check`는 exit 0이므로 레지스트리 오류로 실패한 것이 아니다.
- 실패 시나리오: 후속 에이전트가 T-005b의 모든 수용 기준을 만족시키려 할 때, 현재의 올바른 빈 입력 오류를 report 성공으로 바꾸거나 해당 명령을 미실행 성공으로 처리하도록 유도된다. 입력이 지정됐지만 lock이 없는 소비자와 검사 대상 자체가 없는 호출은 다른 상태다. 현재 CLI에서는 정상적인 모든 호출도 `--lock` 옵션을 사용하지 않으므로 단순히 "--lock 부재"를 조건으로 삼을 수 없다.
- 영향: 지금 동작하는 도구의 버그는 아니지만, 후속 구현 task가 이번에 고정한 빈 입력 오류 회귀를 다시 뒤집는 계약을 요구한다. 이 task는 BLOCKED인 후속 작업이므로 P2로 판정한다.
- 최소 수정 권고: 구현 범위·수용 기준을 "유효한 소비자 경로/manifest와 선언 파일은 있으나 대응 lock이 없는 fixture → NO_LOCK/report 0"으로 한정한다. 마지막 명령에는 그 fixture 경로를 넣고, 경로·manifest가 아예 없는 호출은 별도 음성 사례로 exit 2를 유지한다고 명시한다. 도구에 `--lock`을 다시 추가할 필요는 없다.
- disposition: **OPEN**. 즉시 문서 정정이면 이 reviewer의 delta 재확인을 받고, 이연한다면 T-005b 구현 담당·관련 gate·착수 전 기한을 정한 disposition이 필요하다.

## 변경의 실행 가능성·상태 확인

- T-005·T-105·T-301은 구현물이 일부 있지만 현재 담당자가 작업 중이라는 뜻의 IN_PROGRESS에서 READY로 돌아갔다. 각 파일의 잔여 evidence가 소비자 실제 report, UX 규칙별 근거·예외, OpenAPI 예외 도구·규칙 ID 대조를 미완료로 명시한다. DONE으로 승격하거나 통합 계획 리뷰를 개별 규칙 확정으로 세지 않았다.
- T-106 → T-108과 T-107 → T-003 선행이 원장·상세에서 일치한다. T-106은 실제 캡처 템플릿의 폭 상수를 대조한 뒤 확정하고, T-107은 실제 SPDX 도구로 설정 조각을 검사한 뒤 확정한다. T-108이 현재 RW-3 초안과 폭 값을 맞추는 것은 T-106의 확정 완료를 선행으로 요구하지 않으므로 새 상호 순환은 없다.
- 현재 상세 상태를 직접 집계한 결과 IN_PROGRESS 7, READY 4, BLOCKED 85, DONE 0이다. parent가 예고한 완료 task 종료 delta는 이 candidate에 없으며 검토 결과에 포함하지 않았다.
- T-005의 CI 연결은 수용 기준에서 기존 `docs.yml`에 `--self-check`를 추가하는 경로도 허용하므로, 나중 T-009 전체 완료를 반드시 기다려야 하는 교착은 아니다. T-003 → T-005 잔여 → T-009 순서가 실행 가능하다.
- ADR 13개 본문 `상태`와 색인 상태를 스크립트로 글자 단위 비교해 모두 일치했다. 기본값으로 진행하는 열린 항목과 pinvi mobile 사용자 승인 대기의 구분이 유지됐다.
- packages의 공개 facade 절은 Python 절 아래로 이동했으며 공개 import·extras·root import·0.1/0.2 릴리스 내용은 바뀌지 않았다.
- canview 체크리스트는 존재하는 문서를 "있음"으로 고쳤고 실물 패키지·LICENSES 원문·pins/후속 CI는 잔여로 남겼다. `test_plan_validation.py`의 출처 헤더와 PROVENANCE PV-003이 기존 35 tests 보존·추가 1건을 구분한다. journal 정렬과 runbook의 환경별 실행기 위임은 실제 수행 범위를 확대하지 않는다.
- consumer PR 템플릿은 `.` 대신 실제 소비자 경로를 요구하고 결과 칸의 미리 적힌 exit 0을 제거했다. 이 변화는 미실행 성공 표기를 줄인다. 같은 원칙이 T-005b 마지막 명령에도 필요하다.

## 원 B finding 회귀

[첫 post-fix 원본](2026-09-06-phase0-postfix-reviewer-b.md)의 상세 재현과 판정 근거를 유지하고, 관련 후보 변경·본문·선행과 공개 계약을 다시 확인했다.

| 원 finding | 이번 판정 | 재확인 |
|---|---|---|
| B-P1-01 L6 결정/적용 역전 | FIXED 유지 | T-020 결정 → T-420 실제 반영 evidence → 소비 허용 경계 유지 |
| B-P1-02 pinvi 0.1/0.2 순환 | FIXED 유지 | T-422a → T-213 → T-422b → 부모 T-422 유지 |
| B-P1-03 다음 minor 코드 혼입 | FIXED 유지 | T-212 → T-205, T-310 → T-306·T-307 순서 유지 |
| B-P1-04 Python 0.2 발행 누락 | FIXED 유지 | T-311 발행 책임과 T-483~T-486의 0.2 소비 선행 유지 |
| B-P1-05 승인 전 pinvi smoke 강제 | FIXED 유지 | tokens map·weather, UI map·승인 pinvi/airport 경로 유지 |
| B-P1-06 useRender peer 누락 | FIXED 유지 | T-201 peer·개발 의존, T-203 깨끗한 설치 검사 유지 |
| B-P2-07 공개 facade 단절 | FIXED 유지 | Python 공개 import 절 이동만, T-302/T-304/T-307 책임 유지 |
| B-P2-08 tokens peer minor 모호함 | FIXED 유지 | 독립 버전과 UI 0.1·0.2의 tokens `~0.1.0` 유지 |

첫 post-fix 원본에 기록한 메모리 내 순차 선택 코드를 현재 candidate에서 재실행했다. 해당 코드 블록을 읽어 T-108 → T-106, T-003 → T-107 assertion을 추가했고, metadata 외에 T-212의 선행 tokens 채택과 T-213의 기존 UI 0.1 채택 간선을 유지했다. 다른 외부 gate는 향후 충족된다는 구조적 가정이며 실제 승인·gate 성공 증거는 아니다.

- pinvi 경로: 93개 선택, 의도한 airport T-430·T-431·T-432만 차단. **18개 순서 assertion 통과**.
- airport 경로: 89개 선택, L6 미결로 T-020·T-420·T-421·T-422·T-422a·T-422b·T-484만 차단. **14개 순서 assertion 통과**.

## 직접 실행한 검증

모두 지정된 detached checkout, Windows Python 3.14.3에서 실행했다.

| 명령·검사 | 결과 |
|---|---|
| `git diff --stat 12fb3a8..HEAD`, `--name-only`, 관련 전체 delta·본문 읽기 | 26개 파일, 379 insertions/86 deletions. 이번 상대 reviewer 원본은 미열람 |
| `py -3 -B -X utf8 -m unittest discover -s tests -p "test_*.py"` | 67 tests, 3.644초, OK, skip 0, exit 0 |
| `py -3 -B -X utf8 tools/validate_document_links.py` | 197 documents, 1711 local targets, errors 0, exit 0 |
| `py -3 -B -X utf8 tools/validate_plan.py` | 상세 task 96, 오류 0, exit 0; 제품 gate 아님 |
| `py -3 -B -X utf8 tools/check_versions.py --self-check` | 레지스트리 자체 검사만 성공, exit 0; 소비자 검사 미실행 문구 확인 |
| `git diff --check 12fb3a816e5ebbdf9822a2c17ea7ad5534195fb9..84759b6611ff2a35d5f62a27e38a2878c14e0eb6` | 빈 출력, exit 0 |
| 원 순차 선택 코드 + 새 선행 assertion | pinvi 18·airport 14, 합계 32개 통과 |
| ADR 본문/색인 상태 직접 비교 | 13개 일치 |
| T-005b의 `check_versions.py --repo geo` | 기대를 충족하지 않음: 자식 exit 2, 입력 경로/manifest 요구 오류. B-P2-09 재현이며 성공으로 집계하지 않음 |

B-P2-09 종료 코드 확인은 PowerShell 래퍼 상태 대신 다음 Python 호출의 `returncode`를 사용했다.

```python
import subprocess
p = subprocess.run(
    ['py', '-3', '-B', '-X', 'utf8', 'tools/check_versions.py', '--repo', 'geo'],
    capture_output=True, text=True, encoding='utf-8',
)
assert p.returncode == 2
print(p.stderr.splitlines()[-1])
```

**NOT_RUN**: 이 reviewer의 Linux/WSL·원격 CI 재실행, 소비자 현재값·설치·e2e·시각 검증, npm pack/wheel·공개 facade/Base UI 실제 설치, 라이선스 승인·외부 반영·Release 발행. 패키지 실물과 소비자 변경은 이번 범위에 없고 Windows 실행을 해당 gate의 성공으로 확대하지 않았다.

## 후속 종료 delta와 판정 경계

parent가 예고한 T-001/002/004/007/008/013의 완료 처리는 아직 적용되지 않았다. 그 task들의 수용 기준을 읽었으며 parent가 이미 지적한 T-007 resume 구조와 T-008 인벤토리 링크 정정 외에 이번 조사에서 별도의 새 종료 차단 finding을 확정하지 않았다. 실제 종료 후보는 기록·최종 SHA·원장 이동·CI·review disposition과 함께 별도 재확인해야 한다.

**CONDITIONAL — candidate `84759b6611ff2a35d5f62a27e38a2878c14e0eb6` 한정. B-P2-09 OPEN 1건, 기존 8건 FIXED 유지.**
