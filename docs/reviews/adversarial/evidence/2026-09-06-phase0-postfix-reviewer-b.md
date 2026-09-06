# Phase 0 post-fix 독립 적대적 리뷰 — Reviewer B 원본

- 실행 ID: `/root/reviewer_b :: 2026-09-06-phase0-postfix`
- 전문 영역: 계획 DAG·순차 인계·숨은 본문 선행·UI/Python 공개 계약·출처·외부 승인·정본 충돌.
- 요청: [post-fix 공통 manifest](2026-09-06-phase0-postfix-manifest.md)와 그 문서가 참조하는 [최초 공통 manifest](2026-09-06-phase0-manifest.md) 전체를 읽고 원 B finding 전부와 전체 변경의 회귀를 독립 재검토했다.
- 원본: [최초 Reviewer B](2026-09-06-phase0-reviewer-b.md). 상대 reviewer의 post-fix 결과를 읽거나 요청하지 않았다. 추가 subagent를 생성하지 않았다.
- 작업 위치: `F:/dev/kor-travel-common-wt/review-phase0-b`, detached HEAD. 이 보고서만 main checkout의 지정 evidence 경로에 작성했다. 코드·정책·기존 원본·소비자 저장소는 수정하지 않았다.
- 시작: `2026-09-06T18:26:35.5068782+09:00`.
- 검토 종료: `2026-09-06T18:32:34.4884074+09:00`.
- Base: `d3712a8c965c3193a5af13cacd6d22c603e0cfe4`.
- 요청·실제 candidate: `12fb3a816e5ebbdf9822a2c17ea7ad5534195fb9`; 직접 부모 `905779f825651fec1de405b68491da12d2c87a76`.
- PR base: `b92fabeb1c96a11c1fc9507d93271c1ebeee09b0`.
- 시작·종료 `git status --porcelain=v1`: 모두 빈 출력, clean. 시작·종료 HEAD가 요청 candidate와 일치했다.
- 최종 verdict: **PASS**. 원 B P1 6건과 P2 2건은 모두 **FIXED**로 재확인했다. 새로운 actionable finding은 없다. 이는 해당 candidate의 문서·도구·실행 계획 리뷰 결과이며 후속 패키지·소비자·릴리스 gate의 통과를 뜻하지 않는다.

## 원 finding별 disposition

| 원 finding | 판정 | candidate에서 직접 확인한 근거·재현 결과 |
|---|---|---|
| B-P1-01 L6 결정/실제 적용 역전 | FIXED | `docs/tasks/T-020-pinvi-license-l6.md:25`가 결정·요청 문서·리뷰 완료로 T-020 DONE → T-420 READY를 허용한다. 실제 L6 소비·추출 해제는 T-420의 merge SHA·LICENSE·문구·필드 정합 확인 뒤다. 같은 파일 55행에서 실제 반영 SHA가 T-020 완료 선행이 아님을 명시한다. 결정 후 실제 적용 전의 중간 상태를 소비 허가로 오인하는 경로도 ADR-013 18행이 차단한다. |
| B-P1-02 pinvi UI 0.1/0.2 숨은 순환 | FIXED | T-422a는 T-212·T-421 뒤의 0.1 채택만, T-422b는 T-213·T-422a 뒤의 0.2 채택만 소유한다. 부모 T-422는 두 자식 종료 후 요약한다. T-213 7행의 기존 0.1 선행은 부모 대신 T-422a로 연결됐다. 본문 선행을 추가한 시뮬레이션에서 T-422a → T-213 → T-422b → T-422가 실제 선택된다. |
| B-P1-03 이전 릴리스 전 다음 minor 코드 혼입 | FIXED | accepted ADR-013 14행과 원장·상세 metadata가 T-205에 T-212, T-306·T-307에 T-310을 추가한다. 엄격 순차 선택에서 UI 0.1 발행 전 T-205~T-210 구현, Python 0.1 발행 전 T-306~T-308 구현이 선택되지 않는다. 외부 UI 검증 대기 중 독립 Python 작업으로 진행해도 동일 패키지의 릴리스 내용물은 분리된다. |
| B-P1-04 Python 0.2 발행 책임·소비 버전 누락 | FIXED | T-311이 T-308·T-309·T-310 이후 0.2 rc/wheel·실제 모듈 목록·extras 설치·소비자 검증·정식 발행을 소유한다. T-483~T-486의 선행과 설치 버전이 T-311·`py-v0.2.0`으로 정렬됐다. T-310은 0.1 범위를 유지하며 T-309의 drift 도구가 릴리스보다 먼저 준비된다. 두 경로에서 request-id 소비 task가 T-311보다 먼저 선택되지 않는다. |
| B-P1-05 승인 전 pinvi smoke 강제 | FIXED | ADR-013 17행, T-010, T-109·T-212·T-213, dev-environment·ci-deploy·release가 패키지별 승인 조합을 사용한다. tokens는 map·weather, UI는 map·실제 L6 완료 pinvi 또는 airport다. `consumers.pins.json`에 package·approval을 기록하며 자산·승인 부재 또는 설치 생략을 green으로 세지 않는다. T-010은 T-101 후보 pack의 commit·digest를 사용하므로 T-109 정식 태그를 거꾸로 요구하지 않는다. L6 차단 시 airport 경로가 UI 0.2까지 진행된다. |
| B-P1-06 useRender 사용 전 Base UI peer 부재 | FIXED | T-201 22행이 `@base-ui/react ^1.6.0` peer와 개발 설치를 골격부터 요구하고 1.6·1.8 helper 호환 검증을 둔다. T-203 50행은 workspace hoist가 없는 tarball 설치에서 모든 해당 subpath의 import·타입·렌더 검사를 요구한다. T-206은 이미 선언한 peer에 overlay를 추가하며 rollback 때 helper peer를 제거하지 않는다. 원 실패 경로의 선언 순서가 해소됐다. 실제 helper 호환성은 T-201/T-203의 실행 gate로 남아 있다. |
| B-P2-07 Python 공개 import와 내부 구현 단절 | FIXED | packages 151행, T-302 25~26행이 공개 `kortravelcommon.health`·`request_id`·`metrics` facade와 내부 `api.*`, extras 경계를 명시한다. root `__init__` eager import를 금지하고 core-only·api 설치 검사를 분리한다. T-304·T-307 45행이 내부 구현과 공개 재수출을 함께 완성할 책임을 갖는다. 전체 패키지를 core로 지정해 facade까지 금지하는 import-linter 구성도 명시적으로 배제한다. |
| B-P2-08 독립 버전과 tokens 같은 minor의 모호함 | FIXED | ADR-013 15행이 버전 숫자를 동기화하지 않고 호환 tokens 한 minor만 허용한다고 확정한다. UI 0.1·0.2 모두 `~0.1.0`이며 새 토큰 계약에는 별도 토큰 minor task가 선행한다. architecture·standards·release·T-201·T-212·T-213의 실질 peer 범위가 일치한다. 과거 ADR-005·007·010은 부분 대체와 새 ADR 링크를 기록했다. |

## 순차 실행 공격

원장 metadata만 검사하는 DAG 통과와 구분하기 위해 `docs/tasks.md`의 96개 행에서 분류·우선순위·선행을 추출하고, 기반 → 토큰 → UI → Python → 소비자 → 운영, P0 → P3, ID 순으로 매번 선행이 충족된 한 작업만 선택했다. 본문에만 있는 T-212의 tokens 채택과 T-213의 기존 UI 0.1 채택을 추가 간선으로 넣었다. 아직 없는 실제 승인을 부여한 것이 아니라, 선택한 경로의 외부 담당자·승인·검증이 나중에 제공된다는 가정에서 구조적 도달 가능성을 검사했다.

| 경로·공격 조건 | 결과 |
|---|---|
| pinvi 선택, airport T-430은 계속 차단 | 93개 선택. 미선택은 의도한 airport T-430·T-431·T-432뿐. T-020 → T-420 → T-421 → T-212 → T-205~T-210 → T-411 → T-422a → T-213 → T-422b → T-422. 순서 assertion 16개 통과. |
| airport 선택, L6 결정 T-020은 계속 차단 | 89개 선택. 미선택은 T-020·T-420·T-421·T-422·T-422a·T-422b·T-484뿐. T-430 → T-431 → T-212 → T-205~T-210 → T-411·T-432 → T-213. 순서 assertion 12개 통과. |
| 두 경로 공통 Python·도구 | T-010 → T-109, T-012 → T-212; T-302 → T-303·T-304·T-305 → T-309 → T-310 → T-306·T-307 → T-308 → T-311 → 해당 T-483~T-486. 이전 minor 내용물 오염이나 없는 0.2 자산 설치가 선택되지 않음. |

추가로 다음 회귀 경계를 직접 읽었다.

- T-010은 T-101·T-103의 실제 산출물 이후이고, T-103은 워크플로 활성화를 T-010에 맡긴다. T-012는 pins를 만드는 T-010 이후다. 고정 후보 pack 검증은 정식 채택 task DONE을 요구하지 않는다.
- T-422 자식의 0.1/0.2 범위가 부모의 과거 통합 지침보다 우선한다. 아직 없는 T-211 자동 drift 검사를 앞선 minor의 필수 성공으로 표시하지 않고 수동 shim/patch evidence를 구분한다.
- airport T-432에서 0.1에 없는 Button을 제거했고, T-213은 별도의 0.2 Button 검증 PR을 요청한다. 인계 재확인 문서는 이미 merge된 WIP와 최신 live-e2e 실패를 구분한다. 과거 WIP를 다시 merge하거나 과거 테스트 개수만으로 현재 성공을 주장하지 않도록 T-430이 현재 SHA 대조를 요구한다.
- T-311은 소비자 정식 채택 DONE과 rc 검증 요청을 구분한다. map-api·weather-api 검증 결과는 정식 발행 gate이며 T-483~T-486의 완료를 먼저 요구하지 않는다.
- T-003의 upstream 고지 파일은 실제 존재·원문 확인으로 연결된다. 이 candidate에서 라이선스 원문 확보·소비자 설치·전체 버전 검증의 잔여 작업을 완료로 처리하지 않는다.
- base→candidate의 문서·도구·테스트 변경을 확인했다. 코드의 입력 오류/범위/ref 처리와 link/code-span 처리, 완료 원장 문법 변경을 읽고 전체 회귀를 실행했다. parser 전문 리뷰어의 재현·판정을 대신하지 않는다.

재현 핵심은 다음과 같다. 실제 실행은 같은 Python 코드를 PowerShell here-string에서 `py -3 -B -X utf8 -`로 전달했고 임시 파일이나 candidate 변경을 만들지 않았다.

```python
import re
from pathlib import Path

rows = {}
section = -1
for line in Path('docs/tasks.md').read_text(encoding='utf-8').splitlines():
    if line.startswith('## ') and line != '## 실행 대기열':
        section += 1
    if not line.startswith('| [T-'):
        continue
    fields = [x.strip() for x in line.strip('|').split('|')]
    tid = re.search(r'T-\d+[a-z]?', fields[0]).group()
    rows[tid] = (section, int(fields[2][1:]),
                 set(re.findall(r'T-\d+[a-z]?', fields[-1])))
assert len(rows) == 96
for route, blocked, hidden in (
    ('pinvi', {'T-430'}, {'T-212': {'T-410', 'T-421'},
                        'T-213': {'T-411', 'T-422a'}}),
    ('airport', {'T-020'}, {'T-212': {'T-410', 'T-431'},
                          'T-213': {'T-411', 'T-432'}}),
):
    done = []
    while True:
        ready = [k for k, v in rows.items()
                 if k not in done and k not in blocked
                 and (v[2] | hidden.get(k, set())) <= set(done)]
        if not ready:
            break
        done.append(min(ready, key=lambda k: (rows[k][0], rows[k][1], k)))
    checks = [('T-212', 'T-205'), ('T-310', 'T-306'),
              ('T-310', 'T-307'), ('T-308', 'T-311'),
              ('T-311', 'T-483'), ('T-311', 'T-485'),
              ('T-311', 'T-486'), ('T-010', 'T-109'),
              ('T-012', 'T-212'), ('T-411', 'T-213')]
    checks += ([('T-020', 'T-420'), ('T-420', 'T-421'),
                ('T-422a', 'T-213'), ('T-213', 'T-422b'),
                ('T-422b', 'T-422'), ('T-311', 'T-484')]
               if route == 'pinvi'
               else [('T-430', 'T-431'), ('T-432', 'T-213')])
    for first, second in checks:
        assert done.index(first) < done.index(second), (route, first, second)
    print(route, len(done), sorted(set(rows) - set(done)), len(checks))
```

## 실행 검증·한계

| 직접 실행 | 결과 |
|---|---|
| `git rev-parse HEAD`, `git rev-parse HEAD^`, `git status --porcelain=v1` | 위 실제 hash·clean 확인 |
| `git diff --name-only d3712a8..HEAD` 및 관련 전체 diff·본문 읽기 | 67개 변경 파일 목록 확인. 현재 후보 이후 main checkout의 정리 delta는 읽거나 검토 결과에 섞지 않음 |
| `py -3 --version` | Python 3.14.3, Windows Tier 2 |
| `py -3 -B -X utf8 -m unittest discover -s tests -p "test_*.py"` | 65 tests, 3.334초, OK, skip 0, exit 0 |
| `py -3 -B -X utf8 tools/validate_document_links.py` | 193 documents, 1699 local targets, errors 0, exit 0 |
| `py -3 -B -X utf8 tools/validate_plan.py` | 상세 task 96, 오류 0, exit 0; 제품 gate가 아닌 읽기 전용 metadata/DAG 검사 |
| `py -3 -B -X utf8 tools/check_versions.py --self-check` | 레지스트리 자체 검사만 통과, exit 0. 도구가 소비자 버전 검사를 실행하지 않았다고 명시 |
| `git diff --check d3712a8..HEAD` | 빈 출력, exit 0 |
| 위 메모리 내 순차 선택 시뮬레이션 | pinvi 16개·airport 12개 순서 assertion 통과, exit 0 |

탐색 중 post-fix manifest를 candidate 내부에서 찾은 명령은 파일 부재로 실패했다. manifest는 후보 확정 후 main evidence에 생성된 별도 요청 자료이므로 지정된 main 경로에서 다시 읽었다. PowerShell에서 `rg tools/*.py` 경로 glob도 실패해 실제 문서 경로·파일명을 사용했다. 이 탐색 실패를 검증 성공으로 집계하지 않았다.

- **NOT_RUN(이 reviewer는 Windows 격리 checkout에서 실행)**: Linux/WSL·원격 Actions. candidate의 기존 CI 기록을 이 실행의 성공으로 재집계하지 않았다.
- **NOT_RUN(패키지 실물 미구현)**: npm pack·Next webpack/Turbopack·Base UI 1.6/1.8 설치본·wheel/core-only/api/extras·공개 facade 실제 import. 각각 T-101/T-201/T-203/T-302/T-304/T-307 및 해당 release task의 필수 gate다.
- **NOT_RUN(소비자 수정·승인·배포는 이번 범위 밖)**: 실제 L6/L8 적용·소비자 rc/정식 설치·e2e·시각 비교·태그/Release 발행. 시뮬레이션 성공은 해당 gate를 해제하지 않는다.
- parent가 알린 아직 미커밋인 추가 인계 정리는 이 candidate에 포함되지 않는다. 그 변경 또는 다른 post-fix commit에는 별도 재확인이 필요하다.

## 새 finding과 최종 판정

새 finding 없음. 원 B finding 8건 전부 FIXED. **PASS — candidate `12fb3a816e5ebbdf9822a2c17ea7ad5534195fb9` 한정**.
