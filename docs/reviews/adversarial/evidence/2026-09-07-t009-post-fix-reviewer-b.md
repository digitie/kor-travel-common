# T-009 수정 후 독립 full 리뷰 B 원본

- 실행 ID: `B-T009-PF-20260907-093844-f15072f`.
- 시작: `2026-09-07T09:38:44.6230221+09:00`. 종료 기준선 확인: `2026-09-07T09:42:40.9908475+09:00`.
- Candidate 및 실제 시작·종료 SHA: `f15072f4eb6543ead7636250671e8b12d60776e2`. Delta base: `45c238842a0b8b842ba63e9347b2f7218a3b2f0f`. PR base: `82dec2b939885863100802997f9e7548dffd3c9a`.
- 격리: `review-t009-b` detached worktree, 시작·종료 porcelain 출력 0줄. 재현 입력은 자동 정리되는 임시 fixture에만 작성했다. 제품·소비자·다른 작업자 파일·기존 원본은 수정하지 않았다.
- 입력: [공통 manifest](2026-09-07-t009-post-fix-manifest.md), [최초 B 원본](2026-09-07-t009-reviewer-b.md), 확정된 [최초 통합](../2026-09-07-t009.md)과 A 원본. 상대의 이번 post-fix 원본·결과는 읽지 않았다.
- 범위: 19파일 전체 수정 delta(357줄 추가·10줄 삭제), B 원 finding 4건 및 누적 8개 ID 회귀. 최종 verdict: **PASS**. B 4건 모두 원 ID·심각도로 **FIXED**, 새 finding 0건.

## 전달 요청 원문

> T-009 수정 후 독립 full 리뷰입니다. 공통 새 manifest F:/dev/kor-travel-common/docs/reviews/adversarial/evidence/2026-09-07-t009-post-fix-manifest.md를 읽으세요. Candidate f15072f4eb6543ead7636250671e8b12d60776e2, delta base 45c238842a0b8b842ba63e9347b2f7218a3b2f0f, PR base 82dec2b939885863100802997f9e7548dffd3c9a. 기존 B detached worktree를 새 SHA로 이동 완료했습니다. B 원 ID 4건 + A 정규식 3번 포함 전체 수정 delta 회귀를 확인하되 변경 없는 최초 전체를 다시 통독하지 않아도 됩니다. 이번 원본 소유 경로 docs/reviews/adversarial/evidence/2026-09-07-t009-post-fix-reviewer-b.md 하나입니다. 다른 작업자가 있으므로 다른 파일을 고치거나 되돌리지 마세요. 최초 양 원본은 이미 확정되어 참고 가능하며 이번 상대 post-fix 원본은 확정 전 읽지 마세요. 실제 검증/미실행/재사용을 구분하고 원 반례를 실행해 판단하세요. 현재 후보 및 빈 검증 commit 18b83bd0af84b4e685c4e00108f7104a00900c4a의 PR/release CI를 제가 병행하며 서로 다른 SHA를 혼동하지 마세요. 현재 코드/표준은 검사 명령의 선택 정책과 일치하는 경로를 본문/allowlist와 관계없이 입력 오류 2로 중단합니다. 합성 값 원문/과거 survey 값 출력 금지는 계속 유지합니다.

## 원 finding별 disposition

| 원 ID·심각도 | 수정과 원 반례 재검증 | 판정 |
|---|---|---|
| B-P1-01 · P1 | report step 자체에서 HEAD/source를 대조하고 같은 summary에 SHA를 먼저 쓴다. 서로 다른 이전/current summary 파일로 실제 fixture CLI와 workflow의 Python 블록을 재실행: finding 3개·BELOW_FLOOR 1개·assertion 통과·digest 기록. 실제 candidate CI도 성공 | **FIXED** |
| B-P1-02 · P1 | manifest 기준 parent도 resolve한다. 실제 Win32 `GetShortPathNameW`로 다른 8.3 별칭을 만들고 원 함수 호출: 두 경로 모두 scope 1개·동일 결과. Windows 필수 CI 성공 | **FIXED** |
| B-P2-03 · P2 | 선택 정책에 일치하는 경로를 본문 읽기·발견 출력 전에 거부한다. 두 CLI × 파일/부모 경로 × 안전한 본문/탐지 본문/allowlist × all/staged/base, **36개 전부 exit 2·원문/traceback/발견 JSON 출력 없음**. 앞선 파일에서 누적된 finding도 출력하지 않음 | **FIXED** |
| B-P2-04 · P2 | versions 세 문장이 현행 YAML 미검사와 T-009 범위를 정정했다. T-005c가 구현·수용 기준·담당·시점을 소유하고 BLOCKED/NOT_RUN을 유지한다. 원 workflow 추가 반례는 여전히 finding 3·FLOATING_REF 0이며 이 미구현을 성공으로 표시하지 않음 | **FIXED** |

A-P1-01/P1·A-P1-02/P1·A-P2-04/P2는 각각 같은 summary·경로·정본 수정의 회귀 없음. A-P2-03/P2의 깊이 700 regex를 양 wrapper에 직접 입력해 **각각 exit 2·traceback 없음·원문 없음**을 확인했다. A 원 reviewer의 독립 판정을 대신하지 않으며 B 관점에서 누적 8개 ID에 새 회귀를 찾지 못했다.

## 실제 실행과 재사용

| 명령·검증 | 결과 |
|---|---|
| `git diff --stat/--name-only <delta base>..HEAD`, 지정 `t009-review-diff.py`와 경로별 현재 파일 읽기 | 전체 19파일 변경·기록 대조. 긴 출력은 관련 파일/절로 나눠 재확인. 과거 민감 원문 출력 없음 |
| `py -3 -B -X utf8 -m unittest discover -s tests -p 'test_*.py'` | Windows Python 3.14.3, **135 tests·skip 0·39.221초**, exit 0 |
| `py -3 -B -X utf8 tools/validate_document_links.py` | **265문서·2131 local target**, 오류 0 |
| `py -3 -B -X utf8 tools/validate_plan.py` | **102 task**, 오류 0 |
| `py -3 -B -X utf8 tools/check_spdx.py` | **18파일**, 오류 0 |
| `py -3 -B -X utf8 tools/scan_secrets.py --all`, `tools/check_prod_redaction.py --all` | 각각 **324파일·발견 0·명시적 예외 0**, exit 0 |
| `git diff --check <delta base>..HEAD` | 오류 0 |
| 임시 fixture에서 실제 CLI·Win32 API·원 workflow Python 블록 실행 | summary·8.3 별칭·경로 36개·깊은 regex 두 wrapper·미지원 YAML 전후의 원 반례를 위 표와 같이 새로 실행. 원문 대신 건수·exit·포함 여부만 출력 |
| `git diff --quiet <delta base>..HEAD -- .prod-redaction-patterns .secret-scan-patterns docs/survey docs/runbooks/branch-protection.md versions.json` | exit 0. 기존 패턴 경계·survey 치환 횟수·ruleset 문서/값 정본 대조를 이 불변 범위에서 재사용. action 핀/ref/권한/trigger는 delta에 변경 없음도 확인 |
| `gh run view 34070365064/34070419969 --json event,headSha,conclusion,jobs`, run 목록·PR 조회 | 아래 세 실제 CI 성공 확인. 다른 SHA와 로컬 성공을 혼동하지 않음 |

경로 비공개 재현은 선택한 정책의 범위에 한정했다. 정규식이 모든 임의의 민감 값을 검출한다는 보증으로 확대하지 않는다. T-005c는 T-005/T-009 선행이며 T-009 완료 전 BLOCKED다. task 수 102·열린 92와 계획/원장이 일치하고, 새로운 파서가 이미 구현된 것처럼 기록되지 않았다. PR template의 자체 작성/이식 헤더 구분도 라이선스 정본에 맞는다.

## 실제 CI와 SHA 구분

- Candidate `f15072f4…`의 [PR run 34070365064](https://github.com/digitie/kor-travel-common/actions/runs/34070365064): **docs·tools (ubuntu-24.04)·tools (windows-2025)·secret-scan·check-versions 모두 success**.
- 검증 commit `18b83bd0…`의 [PR run 34070419814](https://github.com/digitie/kor-travel-common/actions/runs/34070419814) 및 [release push run 34070419969](https://github.com/digitie/kor-travel-common/actions/runs/34070419969): 각각 같은 5 check success.
- 두 commit의 tree는 실제 `git rev-parse <commit>^{tree}`에서 `2230b30b2d088a26dbf57672f796bc8124e5119f`로 같았다. commit SHA는 서로 다르다. 이 review의 시작·종료 HEAD는 계속 candidate다.
- 기존 ec34d6a CI 기록은 그 commit의 역사 evidence로만 읽었다. coordinator가 전한 hosted Python 버전·개별 시험 시간은 본인의 독립 실행 건수에 합산하지 않았다.

## 미실행과 판정 경계

- `NOT_RUN(이번 전체 독립 로컬 시험은 Windows)`: WSL Python 전체 재실행. hosted Linux/Windows CI 성공은 별도의 원격 관찰이다.
- `NOT_RUN(후속/외부 범위)`: T-005c YAML 파서, merge 후 main의 새 run, package build/install, 소비자 검증·변경, 태그·Release, 원격 ruleset 적용.
- `NOT_RUN(사용자 제외)`: npm/PyPI 조회·예약·게시·게시 재평가.

**PASS — B 원 finding 4건 FIXED·새 finding 0건.** 지정 candidate의 T-009 수정 검토 결과이며 후속 파서·패키지·소비자 gate 완료를 뜻하지 않는다. 자기 새 원본만 작성하고 상대 post-fix 결과와 독립적으로 확정했다.
