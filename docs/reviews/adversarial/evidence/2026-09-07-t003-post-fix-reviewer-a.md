# T-003 post-fix Reviewer A 독립 재검토 원본

- Review ID: `2026-09-07-t003-post-fix`
- 실행 ID: `/root/reviewer_a` / `t003-postfix-a-20260907T064506+0900`
- 전문 영역: 경로 동일성·SPDX·Python·실패 gate·회귀
- 시작: `2026-09-07T06:45:06.4750902+09:00`
- 검토 종료: `2026-09-07T06:46:37.8700990+09:00`
- Candidate: `951b4432bc8eb4391caf15ad0eb2e8f8f58eb02a`
- Base: `017fef1ca0aa8ca28d0ccf8cfc35fffa71149e64`
- 격리: `F:/dev/kor-travel-common-wt/review-t003-a` detached. 시작·종료 실제 `git rev-parse HEAD`는 candidate와 같고 `git status --porcelain=v1` 출력은 모두 비었다.
- 독립성: 최초 확정 원본은 교차 대조했으며 상대의 이번 post-fix 결과는 읽거나 요청하지 않았다. 이 원본 하나만 주 checkout에 작성했다. 코드·정책·기존 원본·소비자·다른 에이전트 변경은 보존했고 추가 subagent를 만들지 않았다.
- 최종 verdict: **BLOCK — A-T003-P1-01 OPEN 유지**. 나머지 A finding 2건은 FIXED. 별도 신규 ID의 finding은 없다.

## 요청 원문

> T-003 post-fix 독립 재검토를 시작하세요. 공통 manifest F:/dev/kor-travel-common/docs/reviews/adversarial/evidence/2026-09-07-t003-post-fix-manifest.md, candidate 951b4432bc8eb4391caf15ad0eb2e8f8f58eb02a, base 017fef1ca0aa8ca28d0ccf8cfc35fffa71149e64. 기존 review-t003-a detached가 candidate로 전환되어 있습니다. 자기 3 finding 수정과 전체 15파일 delta를 확인하고 새 결과는 상대와 공유하기 전에 독립 확정하세요. 최초 A/B 원본은 모두 확정되어 교차 대조 가능합니다. A 우선 영역은 경로·SPDX·Python·회귀입니다. 자기 원본 docs/reviews/adversarial/evidence/2026-09-07-t003-post-fix-reviewer-a.md 한 파일만 주 checkout에 작성하세요. 다른 에이전트도 작업 중이니 코드/문서·소비자·기존 원본을 수정하거나 되돌리지 마세요. 실행 ID·요청 원문·시각·시작/종료 SHA와 clean·검증·원 finding별 disposition·새 finding·미검증·verdict를 포함하세요. 사본은 변경 없으므로 지난 원천 대조는 재사용하고 실제 변경 및 재현 회귀에 집중하세요.

[공통 manifest](2026-09-07-t003-post-fix-manifest.md)와 전체 15파일 delta를 읽었다. 검사기·회귀 시험은 전체 코드를 대조했고 licensing 계약·PROVENANCE 정정·고지 전달 절차·task evidence·journal·리뷰 보존을 확인했다. 최초 원본은 [A](2026-09-07-t003-reviewer-a.md)·[B](2026-09-07-t003-reviewer-b.md)다.

## 원 finding별 disposition

| Finding | 판정 | 근거 |
|---|---|---|
| A-T003-P1-01 경로 별칭 | **OPEN 유지** | `./`·중복 구분자·디렉터리/파일 stem 대소문자는 거부하지만 확장자 대소문자는 `is_source`에서 먼저 제외되어 우회가 남음. 아래 재현 |
| A-T003-P1-02 qualified geo | **FIXED** | owner/repo의 마지막 이름을 casefold하고 색인의 -only 요구를 보존. qualified geo·대문자 geo·다른 repo의 -only 원천 각각에서 잘못된 SPDX exit 1, 올바른 -only/AND exit 0을 실제 확인 |
| A-T003-P2-03 PV 행 공백 | **FIXED** | 공백 1개·3개·tab 각각에서 누락 Origin은 exit 1, 정상 Origin은 exit 0. source 행을 조용히 버리거나 정상 Origin을 미등록으로 오인하지 않음 |

qualified/대문자 geo 및 색인의 -only 검사 9개와 들여쓰기 정상/음성 검사 6개, 총 15개 CLI 사례가 모두 기대값과 일치했다. 각 사례는 독립 `TemporaryDirectory`에서 생성했으며 Windows Python으로 실제 CLI를 호출했다. 해당 새 회귀 시험도 양 OS 전체 시험 안에서 실행됐다.

## A-T003-P1-01 잔여: 확장자의 대소문자는 실제 경로 확인 전에 제외됨

- 위치: [check_spdx.py](../../../../tools/check_spdx.py) **111~112행**. 117~118행의 실제 source_names 대조가 그 뒤에 있다.
- 원인: `is_source(Path(name))`가 대소문자를 구별하는 suffix 집합으로 먼저 제외한다. `tools/sample.PY`는 `False`가 되어 실제 소스 경로 대조에 도달하지 않는다. 실제 파일 `tools/sample.py`는 enumeration으로 검사되지만 출처 entry가 없어 자체 작성 파일처럼 처리된다.
- 계약: 수정된 licensing §5.2는 실제 파일과 다른 대소문자 별칭을 오류로 명시한다. 기존 P1의 모든 대소문자 경계를 해결한 것이 아니다.

실제 재현은 다음 두 파일의 임시 fixture에서 `python -B -X utf8 <candidate>/tools/check_spdx.py --root <fixture>`를 실행했다.

```text
PROVENANCE.md:
| PV-001 | `tools/sample.PY` | canview | `1234567890abcdef1234567890abcdef12345678` | `src/sample.py` | GPL-3.0-or-later | changed | evidence |

tools/sample.py:
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2026 Author
```

| 입력 경로 | Windows 실제 경로 존재 | Windows exit | WSL exit |
|---|---|---|---|
| `tools/sample.py` | True | 1, Origin·Modified 누락 | 1, 같은 누락 |
| `./tools/sample.py` | True | 1, 비정규 경로 | 1, 비정규 경로 |
| `tools//sample.py` | True | 1, 비정규 경로 | 1, 비정규 경로 |
| `TOOLS/sample.py` | True | 1, 실제 대소문자 불일치 | 1, 파일 없음 |
| `tools/Sample.py` | True | 1, 실제 대소문자 불일치 | 별도 실행 안 함 |
| `tools/sample.PY` | **True** | **0, 1개 파일·오류 0** | **0, 행의 경로가 없어도 제외됨** |
| `tools/SAMPLE.PY` | **True** | **0, 1개 파일·오류 0** | 별도 실행 안 함 |

Windows에서는 `.PY`가 동일한 실제 파일을 가리킨다는 `Path.is_file() == True`도 확인했다. WSL은 `.PY` 경로가 존재하지 않는데 출처 행 자체를 제외해 0이 된다. 문제를 재현하는 데 파일·Origin·수정 고지를 바꾸거나 소비자 원본을 읽을 필요가 없다.

필수 Origin·Modified 누락을 성공으로 세는 기존 P1의 영향이 유지된다. **대소문자 별칭을 source 제외 판정 전에 검증**하거나 동일성을 확인한 실제 파일을 기준으로 분류하고, 확장자 대소문자도 회귀에 넣어야 한다. 현재 추가 시험은 `TOOLS/sample.py`·`tools/Sample.py`까지만 포함한다. 새 ID로 중복 집계하지 않고 A-T003-P1-01을 OPEN으로 유지한다.

## 검증 결과

| 환경·명령 | 결과 |
|---|---|
| Windows `python --version` | Python 3.14.3 |
| WSL Ubuntu-26.04 `sys.version` | Python 3.14.4, GCC 15.2.0 |
| Windows `python -B -X utf8 -m unittest discover -s tests -p 'test_*.py'` | 98 tests, 6.349초, OK, skip 0 |
| WSL 같은 `python3` 명령 | 98 tests, 6.439초, OK, skip 0 |
| 양 OS `tools/check_spdx.py` | exit 0, 13개 파일·오류 0 |
| 양 OS `tools/validate_document_links.py` | exit 0, 219개 문서·1860개 local target·오류 0 |
| 양 OS `tools/validate_plan.py` | exit 0, 96개 상세 task·오류 0 |
| `git diff --check 017fef1ca0aa8ca28d0ccf8cfc35fffa71149e64 HEAD` | exit 0, 오류 없음 |
| `git diff --quiet <base> HEAD -- LICENSES .github` | exit 0, 사본·CI 변경 없음 |
| Windows 독립 공격 CLI | 경로 7개 + geo/색인 라이선스 9개 + 공백 6개 = 22개 |
| WSL 독립 경로 공격 CLI | 5개, 위 표의 실제 결과 |
| `gh pr view 2 --json number,isDraft,headRefOid,statusCheckRollup` | [PR #2](https://github.com/digitie/kor-travel-common/pull/2) draft·candidate head 일치. [CI run 34061977516](https://github.com/digitie/kor-travel-common/actions/runs/34061977516) validate-docs SUCCESS |

## 전체 delta와 미검증

15파일의 변경은 351 insertions/11 deletions다. `validate_plan.py`는 Modified 설명만 정정하며 검사 로직 변경이 없다. PROVENANCE는 원본에 이미 있던 제목 검사를 common 추가로 잘못 설명한 부분을 정정한다. 최초 B 원본의 원문 대조를 재사용하며 이번에는 원천을 다시 다운로드하지 않았다.

템플릿 인덱스는 고지·PV 사본·geo LICENSE의 목적지와 common 고정 SHA·파일 배치 매핑 보존을 명시한다. 전달 고지는 소비자 경로를 backtick으로 표기하고 원천 고지를 유지하도록 바뀌었다. 실제 전달 fixture 재실행은 **NOT_RUN(A 역할에서는 변경 지침만 대조)**이며 B-P2-03의 최종 재확인은 원 B reviewer가 소유한다. 이전 원본은 추가 기록으로 보존되고 task는 IN_PROGRESS·finding은 재확인 전 OPEN이다.

사본은 불변이므로 최초 A의 로컬 21개 digest 확인 및 확정한 B의 고정 원문 대조를 재사용한다. Python 3.11 직접 실행·Windows ACL/링크 경계의 추가 실행·SPDX 필수 CI/Windows matrix(T-009)·패키지 build/pack/wheel·소비자 설치/e2e/배포는 **NOT_RUN**이며 이전 사유가 유지된다. 이번 성공한 CI를 후속 SPDX 필수 단계의 성공으로 확대하지 않는다.

**BLOCK. A-T003-P1-01 잔여를 수정한 immutable candidate의 재확인이 필요하다.**
