# T-009 수정 후 독립 full 리뷰 A 원본

- 실행 ID: `T009-A-PF-20260907-093825-f15072f`.
- 판정: **PASS**. A 원 finding 4개와 B 원 finding 4개를 원 ID·심각도로 대조했으며 모두 FIXED, 새 finding 0개다. T-005c 기능 구현은 여전히 미완료이며 문서 계약 충돌의 해소와 구분한다.
- 시작: `2026-09-07T09:38:25.3707421+09:00`; 검사 종료: `2026-09-07T09:42:41.2924310+09:00`.
- candidate: `f15072f4eb6543ead7636250671e8b12d60776e2`; 수정 delta base: `45c238842a0b8b842ba63e9347b2f7218a3b2f0f`; 전체 PR base: `82dec2b939885863100802997f9e7548dffd3c9a`.
- 격리: `F:/dev/kor-travel-common-wt/review-t009-a`, detached. Windows Git의 시작·종료 실제 HEAD가 candidate와 일치했고 `git status --porcelain=v1 --untracked-files=all`은 모두 빈 출력이다.
- 범위: 수정 19파일, 357행 추가·10행 삭제. A 우선 영역인 scanner·정책·경로·실패·비공개 및 전체 수정 delta를 검토했다. [공통 manifest](2026-09-07-t009-post-fix-manifest.md), 확정된 최초 A/B 원본·통합 report를 읽었으며 이번 상대 post-fix 원본은 읽거나 요청하지 않았다.
- 소유 파일은 이 원본 하나다. 격리 코드·문서·다른 원본·소비자 저장소는 수정하지 않았다. 추가 재현은 자동 정리되는 임시 디렉터리와 Git 저장소에만 작성했다.

## 전달 요청 원문

> T-009 수정 후 독립 full 리뷰. 공통 새 manifest F:/dev/kor-travel-common/docs/reviews/adversarial/evidence/2026-09-07-t009-post-fix-manifest.md를 읽으세요. Candidate f15072f4eb6543ead7636250671e8b12d60776e2, delta base45c238842a0b8b842ba63e9347b2f7218a3b2f0f, PR base82dec2b939885863100802997f9e7548dffd3c9a. 기존 A detached worktree를 새 SHA로 이동 완료했습니다. A 원 ID4건 + B 경로명3번 포함 전체 수정 delta 회귀를 확인하되 변경 없는 최초 전체를 다시 통독하지 않아도 됩니다. 이번 원본 소유경로 docs/reviews/adversarial/evidence/2026-09-07-t009-post-fix-reviewer-a.md 하나. 다른 작업자가 있으므로 다른 파일을 고치거나 되돌리지 마세요. 최초 양 원본은 이미 확정되어 참고 가능, 이번 상대 post-fix 원본은 확정 전 읽지 마세요. 실제검증/미실행/재사용을 구분하고 새finding없어도 원반례를 실행해 판단하세요. 현재 후보+빈검증 commit18b83bd0af84b4e685c4e00108f7104a00900c4a의 PR/release CI를 제가 병행하며 서로 다른SHA를혼동하지 마세요. 현재 코드/표준은 검사명령의 선택정책과 일치하는 경로는 본문/allowlist와관계없이 입력오류2로중단합니다. 합성값원문/과거survey값출력금지는계속유지합니다.

manifest의 공통 요청도 적용했다.

> 같은 candidate에서 독립 full post-fix 리뷰를 수행한다. 원 finding ID·심각도를 유지하고 각각 FIXED/OPEN 여부, 원 반례 재검증, 전체 수정 delta의 회귀와 새 finding을 기록한다. T-005c의 미구현을 DONE 또는 CI 실측으로 세지 않는다. 실제 실행과 재사용/미실행을 구분한다. 검토 트리·다른 작업자 파일은 수정하지 않는다. 원문 값은 출력하지 않고 새 결과는 상대 원본과 독립적으로 확정한다.

## 새 실행 결과

| 실제 명령·검사 | 결과 |
|---|---|
| Windows `python -B -X utf8 -m unittest discover -s tests -p 'test_*.py'` | Python 3.14.3, **135 tests·skip 0**, 37.323초, exit 0 |
| WSL `uv run --no-project --python 3.11 python -B -X utf8 -m unittest discover -s tests -p 'test_*.py'` | Python 3.11.15, **135 tests·skip 0**, 29.821초, exit 0 |
| `python -B -X utf8 tools/validate_document_links.py` | 265문서·2131대상, 오류 0 |
| `python -B -X utf8 tools/validate_plan.py` | task 102개, 오류 0 |
| `python -B -X utf8 tools/check_spdx.py` | 18파일, 오류 0 |
| `python -B -X utf8 tools/scan_secrets.py --all` | 324파일, 발견 0·예외 0, exit 0 |
| `python -B -X utf8 tools/check_prod_redaction.py --all` | 324파일, 발견 0·예외 0, exit 0 |
| `python -B -X utf8 tools/check_versions.py --self-check` | 레지스트리 자체 검사 exit 0. 소비자 판정으로 세지 않음 |
| `git diff --check <수정 delta base> HEAD` 및 `<전체 PR base> HEAD` | 각각 exit 0, 빈 출력 |
| 양 OS에서 별도 scanner 공격 스크립트 | **각 30사례**, 모두 exit 2·traceback 없음·합성 표식 없음·finding JSON 출력 없음 |
| 정규/상대 별칭 manifest 비교 | 양 OS에서 같은 scope 1개. Windows 실제 8.3 별칭도 동일 |
| 실제 checker report와 candidate workflow의 Python 블록 | 양 OS에서 모두 exit 0, finding 3개·BELOW_FLOOR 1개, 같은 step summary에 source·report digest 존재 |
| 이동 workflow 참조를 추가한 전후 보고 | 양 OS에서 finding 배열 동일, FLOATING_REF 0. 현재 미지원 사실을 재확인 |

별도 scanner 공격은 기존 `RepositoryCase`로 정책·파일을 만드는 Python stdin 스크립트이며 실제 candidate CLI를 호출했다. 두 wrapper × 파일명/부모 디렉터리 × 안전한/탐지 본문 × `--all`/`--staged`/`--base`의 24사례를 실행했다. 각 파일은 해당 규칙의 정확한 allowlist에도 넣고, 정렬상 먼저 읽히는 안전한 경로의 다른 파일에 발견을 만들어 두었다. 경로 오류가 allowlist보다 우선하고 앞서 모은 finding도 출력하지 않는지 확인했다. 두 wrapper × 세 모드의 깊은 regex 6사례를 더해 OS별 총 30사례다. 표식은 조각을 합쳐 생성하고 출력에는 일치 여부만 기록했다.

step summary 재현은 이전 step의 파일을 사용하지 않고 현재 report step의 source 기록부터 독립 파일에 구성했다. 실제 고정 fixture를 checker로 실행한 뒤 candidate workflow의 `import hashlib`부터 `PY` 전까지 블록을 그대로 추출·실행했다. 현재 report 파일의 SHA256과 기록된 summary를 대조했다. 이는 workflow 전체를 로컬 Actions 실행으로 간주한 결과가 아니다.

## 원 finding 재판정

| 원 ID | 원 심각도 | disposition | 새 근거 |
|---|---|---|---|
| A-P1-01 | P1 | **FIXED** | report step 자체에서 checkout SHA를 확인하고 summary에 먼저 기록한다. 서로 다른 step 파일을 가정한 원 반례가 양 OS에서 성공하며 실제 candidate PR의 check-versions도 success다 |
| B-P1-01 | P1 | **FIXED** | 같은 step 분리 반례와 실제 CI로 교차 확인. 두 ID를 병합하지 않음 |
| A-P1-02 | P1 | **FIXED** | `manifest_path.parent.resolve()`로 기준 경로와 대상 경로가 일치한다. Windows `GetShortPathNameW`로 실제로 다른 8.3 별칭을 얻어 정규 경로와 같은 반환값을 확인했다 |
| B-P1-02 | P1 | **FIXED** | 같은 별칭 반례 및 mandatory Windows tools의 실제 success를 확인. 양 OS의 `..` 별칭 회귀도 성공 |
| A-P2-03 | P2 | **FIXED** | 컴파일의 `RecursionError`를 `ScanError`로 변환한다. 깊이 700 regex를 양 wrapper·세 스냅샷 모드·양 OS에서 실행해 exit 2·traceback 없음·원문 없음 확인 |
| B-P2-03 | P2 | **FIXED** | 선택 정책에 일치하는 경로를 본문 읽기 전에 거부한다. 안전/탐지 본문, 파일/부모 이름, 정확한 allowlist, 앞서 수집한 발견이 있는 모든 반례에서 경로 원문·finding 목록 없이 exit 2 |
| A-P2-04 | P2 | **FIXED** | 버전 정본 세 위치가 현재 미지원과 T-005c 소유를 명시한다. 상세 task에 선행·담당·시점·입력/오류/양 OS 수용 기준이 있고 원장은 BLOCKED다. 원 반례의 미탐을 성공 기능으로 바꾸어 적지 않음 |
| B-P2-04 | P2 | **FIXED** | 정본·T-009 범위·T-005c·task 원장·통합 계획을 대조했다. 자동 YAML 보고와 현재 common 자체 CI 검증의 완료 범위가 구분됨 |

새 finding은 없다. T-005c의 문서 수용 기준은 후속 구현에 필요한 계약이며 그 기능이 구현됐다는 판정은 아니다. PR template의 SPDX·저작권/이식 Origin 구분도 기존 라이선스 정본과 일치한다. 완료 10개·열린 92개·전체 102개의 원장 상태와 T-009 IN_PROGRESS가 유지돼 재검토 전에 task를 닫지 않는다.

## 실제 원격 관찰과 SHA 구분

읽기 전용으로 `gh run view <ID> --repo digitie/kor-travel-common --json headSha,event,status,conclusion,jobs`를 실행해 다음을 직접 확인했다.

| run | 실제 head SHA·사건 | 관찰 |
|---|---|---|
| [candidate PR 34070365064](https://github.com/digitie/kor-travel-common/actions/runs/34070365064) | `f15072f4eb6543ead7636250671e8b12d60776e2`, pull_request | completed/success. docs·tools (ubuntu-24.04)·tools (windows-2025)·secret-scan·check-versions 모두 success |
| [release push 34070419969](https://github.com/digitie/kor-travel-common/actions/runs/34070419969) | `18b83bd0af84b4e685c4e00108f7104a00900c4a`, push | completed/success. 같은 필수 check 5개 모두 success |

`git rev-parse '<candidate>^{tree}' '<검증 commit>^{tree}'`의 두 결과는 모두 `2230b30b2d088a26dbf57672f796bc8124e5119f`다. 두 commit SHA는 다르며 tree 동일성을 근거로 동일 코드의 release push 경로 실행을 확인했다. coordinator가 추가 전달한 검증 commit의 PR run `34070419814`, hosted Python 버전·시험 시간·각 job source 로그는 본인이 다시 조회하지 않았으며 위 직접 관찰과 구분한다.

## 재사용·미실행·한계

- **재사용**: 최초 review의 변경 없는 스냅샷 선택·비밀 패턴·출처 검토 및 survey 치환 대조. `git diff --quiet <최초 candidate> HEAD -- AGENTS.md docs/README.md tools/scan_secrets.py tools/check_prod_redaction.py .secret-scan-patterns .prod-redaction-patterns docs/survey tests/fixtures/version-report`가 exit 0임을 새로 확인했다. 전체 회귀 시험·원 반례·변경된 규범은 재사용으로 대체하지 않고 위와 같이 새로 검증했다.
- **환경 오류와 재실행**: WSL 추가 스크립트의 30사례는 성공했으나 이어진 `git rev-parse HEAD`가 Windows에서 생성한 worktree 메타데이터 경로를 WSL Git으로 해석하지 못해 exit 128이었다. 해당 스크립트 전체를 성공으로 집계하지 않았다. report 부분만 Windows Git에서 확인한 candidate SHA를 명시적으로 전달해 다시 실행했고 성공했다. 실제 시작·종료 SHA/clean 검사는 Windows Git으로 수행했다.
- **NOT_RUN(Windows 전용)**: WSL에서 Win32 8.3 API 실행. Windows에서는 실제 별칭 반례를 실행했다.
- **NOT_RUN(후속 구현)**: T-005c의 자동 YAML 정적 보고와 소비자 CI 실측. parser의 현재 미지원은 위 반례로 확인했으며 DONE으로 세지 않는다.
- **NOT_RUN(범위 밖/병합 후)**: main 병합 후 CI, 원격 ruleset 변경, 소비자 변경·실행, npm/PyPI 게시, 태그·GitHub Release 생성. 현재 PASS는 이 immutable 수정 후보의 리뷰 판정이다.
- 과거 survey 값·합성 탐지 값은 출력하지 않았고 규칙에 없는 모든 비밀 탐지까지 보증하지 않는다. 새 상대 post-fix 원본을 보지 않은 상태로 이 원본을 확정했다.

최종 **PASS — 원 8개 ID 모두 FIXED, 새 finding 0개**.
