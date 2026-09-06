# T-003 post-fix 독립 적대적 리뷰 B 원본

- 실행 ID: `B-T003-PF-20260907-064511-951b443`
- 시작: `2026-09-07T06:45:11.9192698+09:00`
- 검토 종료: `2026-09-07T06:46:12.0103297+09:00`
- Candidate 및 실제 시작·종료 HEAD: `951b4432bc8eb4391caf15ad0eb2e8f8f58eb02a`
- Base: `017fef1ca0aa8ca28d0ccf8cfc35fffa71149e64`
- 격리: `review-t003-b` detached worktree. 시작·종료 `git status --porcelain` 출력 0줄. 검토 대상 파일·소비자 파일을 수정하지 않았다.
- [공통 manifest](2026-09-07-t003-post-fix-manifest.md), [최초 B 원본](2026-09-07-t003-reviewer-b.md), [최초 통합 리뷰](../2026-09-07-t003.md).
- 결과: **PASS**. B 원 finding 3개 모두 **FIXED**, 새 finding 0개. 이번 상대 reviewer 결과를 읽기 전에 이 원본을 확정했다.

## 전달 요청 원문

> T-003 post-fix 독립 재검토를 시작하세요. 공통 manifest F:/dev/kor-travel-common/docs/reviews/adversarial/evidence/2026-09-07-t003-post-fix-manifest.md, candidate 951b4432bc8eb4391caf15ad0eb2e8f8f58eb02a, base 017fef1ca0aa8ca28d0ccf8cfc35fffa71149e64. 기존 review-t003-b detached가 candidate로 전환되어 있습니다. 자기 3 finding 수정과 전체 15파일 delta를 확인하고 새 결과는 상대와 공유하기 전에 독립 확정하세요. 최초 A/B 원본은 모두 확정되어 교차 대조 가능합니다. B 우선 영역은 출처·고지 전달·정본·evidence입니다. 자기 원본 docs/reviews/adversarial/evidence/2026-09-07-t003-post-fix-reviewer-b.md 한 파일만 주 checkout에 작성하세요. 다른 에이전트도 작업 중이니 코드/문서·소비자·기존 원본을 수정하거나 되돌리지 마세요. 실행 ID·요청 원문·시각·시작/종료 SHA와 clean·검증·원 finding별 disposition·새 finding·미검증·verdict를 포함하세요. 사본은 변경 없으므로 지난 원천 대조는 재사용하고 실제 변경 및 재현 회귀에 집중하세요.

## 원 finding별 disposition

| Finding | 판정 | 수정과 독립 재현 |
|---|---|---|
| B-P1-01 — qualified geo의 -only 누락 통과 | **FIXED** | `provenance()`가 원천의 -only 여부를 보존하고 `check_file()`이 이를 확인한다. 저장소명도 owner/repo의 마지막 이름을 casefold하여 판단한다. 실제 candidate 파일을 읽되 메모리에서 SPDX·Origin·PV 값만 대체하여 CLI 진입점 `main()`을 실행했다. bare geo의 잘못된 식별자, qualified geo의 잘못된 식별자, 다른 repo이지만 색인 원천이 -only인 잘못된 식별자 모두 반환 1·오류 1이다. qualified geo의 -only와 AND, 다른 repo의 올바른 -only는 반환 0·오류 0이다. 총 6경로, 파일 쓰기 없음 |
| B-P2-02 — validate_plan 수정 이력 오기 | **FIXED** | PROVENANCE 정정 절이 제목 일치 검사는 원본에 이미 있었다고 바로잡았다. Modified도 docstring·출처 헤더만 변경하고 검사 로직은 같다고 기록한다. 이번 코드 delta가 해당 헤더 1행뿐임을 확인했으며, 최초 원문 비교에서 확인한 실제 diff와 일치한다. PV-003의 추가 회귀 시험 설명은 유지되어 로직과 시험을 구분한다 |
| B-P2-03 — JSON 고지 전달에서 출처 기록 누락 | **FIXED** | 템플릿 색인에 고지·PV 기록·라이선스 3종과 각각의 소비자 목적지가 추가되었다. 사용법은 표 머리·채택한 원문 PV 행·확보한 common 전체 SHA·배치 매핑 보존을 요구한다. 전달 고지는 소비자 안의 출처 기록과 라이선스 경로를 안내한다. 메모리의 목적지 경로→바이트 사전으로 설정 6개 전체와 codex/gemini 2개만 채택하는 두 경우를 구성했다. 각각 PV 6행/2행, 전체 산출물 9개/5개, 원천 SHA·라이선스·수정 내용·common SHA·파일 매핑을 보존하고 고지의 두 경로가 실제 전달 목록에 존재했다 |

B-P1-01 재현은 선택적 Origin 라이선스 괄호를 제거하고 PV의 `GPL-3.0-only`는 유지했다. 따라서 기존 괄호 기반 대조군이 성공한 것을 수정 확인으로 오인하지 않았다. 정상 3경로와 실패 3경로에서 실제 common 검사 대상은 모두 13개였다.

B-P2-03의 전달 라이선스 SHA-256은 두 경우 모두 `3972dc9744f6499f0f9b2dbf76696f2ae7ad8af9b23dde66d6af86c9dfb36986`으로 원본 사본과 같았다. 실제 소비자 checkout이나 디스크 fixture를 만들지 않았으며, 문서에 적힌 파일·행·목적지 전달 계약을 메모리에서 검증한 결과다.

## 전체 delta와 검증

15개 변경 파일을 확인했다. 실행 코드의 변화는 출처 경로·표 공백·원천 라이선스 대조와 Modified 오기 정정이다. templates의 동반 전달 절차, licensing의 검사 문법, task·journal·CHANGELOG, 최초 리뷰 원본·통합 기록·색인을 함께 대조했다. 고정 라이선스 사본·제품 구현·소비자·CI workflow는 변경되지 않았다.

| 명령·검토 | 실제 결과 |
|---|---|
| `git diff --stat 017fef1ca0aa8ca28d0ccf8cfc35fffa71149e64..HEAD` 및 전체 delta 읽기 | 15개 파일, 351줄 추가·11줄 삭제 |
| `py -3 -B -X utf8 -m unittest discover -s tests -p 'test_*.py'` | Windows Python 3.14.3, 98 tests 성공, skip 0, exit 0. SPDX 시험은 기존 26개 + 신규 4개이며 각 subTest를 별도 test로 부풀리지 않음 |
| `py -3 -B -X utf8 tools/check_spdx.py` | 13개 파일, 오류 0, exit 0 |
| `py -3 -B -X utf8 tools/validate_document_links.py` | 219개 문서, 1860개 로컬 target, 오류 0, exit 0 |
| `py -3 -B -X utf8 tools/validate_plan.py` | 상세 task 96개, 오류 0, exit 0. 제품 gate 판정 아님 |
| `git diff --check 017fef1ca0aa8ca28d0ccf8cfc35fffa71149e64..HEAD` | 출력 없음, exit 0 |
| `git diff --quiet 017fef1ca0aa8ca28d0ccf8cfc35fffa71149e64 HEAD -- LICENSES` | exit 0, 원문 사본·확보 목록 불변. 최초 B의 원격 원문 21개·npm integrity 13개 대조를 재사용 |
| B-P1-01 메모리 고장 주입 | 음성 3개 실패·양성 3개 성공, 기대 일치. `Path.read_text` 대체와 `sys.argv` 고정으로 실제 `main()` 실행 |
| 전달 계약 메모리 시뮬레이션 | 전체 6개·부분 2개 채택 모두 출처·고지·원문 보존 |
| `gh pr view 2 --json number,isDraft,state,headRefOid,statusCheckRollup` | [PR #2](https://github.com/digitie/kor-travel-common/pull/2) OPEN·draft·candidate head 일치. `validate-docs` SUCCESS, [run 34061977516](https://github.com/digitie/kor-travel-common/actions/runs/34061977516) |
| 시작·종료 `git rev-parse HEAD`, `git status --porcelain` | candidate 일치, 두 번 모두 clean |

최초 A 원본도 허용된 범위에서 교차 대조했다. A-T003-P1-01의 비정규 경로·대소문자와 중복 등록, A-T003-P2-03의 선행 공백을 신규 시험이 다루고 현재 98개 시험에서 성공한다. A-T003-P1-02는 B-P1-01과 같은 원인의 독립 재현으로 수정 확인했다. A의 최종 disposition은 A 원 reviewer의 이번 판정을 대체하지 않는다.

검토된 원본·통합 report는 최초 BLOCK과 OPEN을 역사 기록으로 보존하고 post-fix 전 PASS로 올리지 않았다. T-003도 IN_PROGRESS로 유지한다. 전달 PV 기록은 고정 common 정본의 사본으로 명시되어 새 정책 정본을 만들지 않으며, 채택 subset을 지원한다. 새 finding은 없다.

## 미검증과 판정 범위

- `NOT_RUN(이번 reviewer의 WSL/Linux·Python 3.11 직접 실행 없음)`: 작성자의 WSL 98개 성공 주장을 독립 실행으로 합산하지 않았다.
- `NOT_RUN(원문 사본 불변)`: npm·SPDX·Git 원문을 이번에 다시 내려받지 않았다. 변경 없음 확인과 최초 B의 실제 원격 바이트 검증을 재사용했다.
- `NOT_RUN(사용자 경계)`: 실제 소비자 저장소 복사·빌드·smoke 없음. 메모리 전달 검사와 소비자 실행을 구분한다.
- `NOT_RUN(후속 task)`: 제품 build·npm pack·wheel/sdist 설치는 T-101·T-201·T-302, SPDX 필수 CI·Windows matrix는 T-009 범위다. 원격 성공은 현재 `validate-docs` check 하나다.
- **PASS는 이 immutable post-fix delta와 B findings의 수정 판정이다.** 두 reviewer 결과를 통합한 뒤 T-003 종료 상태와 실제 evidence를 갱신해야 하며, 제품 gate·릴리스 완료를 뜻하지 않는다.
