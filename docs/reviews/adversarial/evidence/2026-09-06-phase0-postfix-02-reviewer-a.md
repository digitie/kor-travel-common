# Phase 0 두 번째 post-fix Reviewer A 독립 원본

- Review ID: `2026-09-06-phase0-postfix-02`
- 실행 ID: `/root/reviewer_a` / `phase0-postfix-02-a-20260906T184019+0900`
- 전문 영역: Python·npm·uv ref 입력 문맥, 실패 gate·registry·문서 validator 회귀
- 시작: `2026-09-06T18:40:19.2350630+09:00`
- 종료 검증: `2026-09-06T18:41:44.9224583+09:00`
- 공통 요청: [두 번째 post-fix manifest](2026-09-06-phase0-postfix-02-manifest.md). 원 A-P1-05 잔여와 원 6 finding 회귀, base→candidate 전체 delta를 독립 재검토한다.
- Candidate: `84759b6611ff2a35d5f62a27e38a2878c14e0eb6`
- Base: `12fb3a816e5ebbdf9822a2c17ea7ad5534195fb9`
- 격리: `F:/dev/kor-travel-common-wt/review-phase0-a` detached worktree. 시작·종료 실제 HEAD가 candidate와 일치하고 `git status --porcelain=v1` 출력은 모두 비었다.
- 독립성: 상대의 이번 원본·finding을 읽거나 요청하지 않았다. 이 evidence 파일만 작성했고 코드·기존 원본·다른 추적 파일을 수정하지 않았다. 공격 fixture는 OS 임시 디렉터리에서 생성·정리했다.
- 최종 verdict: **PASS**. 원 A finding 6건 모두 FIXED. 이번 범위에서 신규 finding은 없다.

## 검토 범위와 판단

`tools/check_versions.py`의 ref 문맥 분리와 호출부, 추가 회귀시험, 정책·T-005 계열의 실제 CLI 입력 설명을 직접 대조했다. Python facade 절 이동, ADR 상태/색인 정합, 출처·추가 시험 표기, canview 대조표 상태, T-106/T-107 선행, 부분 구현 task의 READY/BLOCKED 및 잔여 evidence, 소비자 PR 템플릿의 실행 대상도 delta로 검토했다. 이전 원본·새 원본을 대신하는 편집을 하지 않았다.

Python 선언의 revision은 path의 `@rev`에서만 판정하고 npm 선언은 fragment, uv lock git source는 해석된 전체 SHA fragment로 분리됐다. 이전 우회 두 건은 fail 모드에서 `FLOATING_REF`·exit 1이고 정상 Python SHA/tag/subdirectory·npm SHA/tag·uv 전체 SHA는 유지된다.

T-106은 실제 T-108 캡처 템플릿 대조, T-107은 T-003 SPDX 도구 실행을 선행으로 갖는다. 부분 구현 상태를 작업 완료로 표시하지 않았고 전체 task 96개 DAG 검사도 통과했다. 신규 규칙 확정이나 소비자 설치 결과로 확대 해석하지 않는다.

## 실제 검증

| 명령 | Windows Python 3.14.3 | WSL Ubuntu-26.04 / Python 3.14.4 |
|---|---|---|
| `python[3] -B -X utf8 tools/validate_document_links.py` | exit 0, 문서 197개·target 1711개·오류 0 | 동일 |
| `python[3] -B -X utf8 tools/validate_plan.py` | exit 0, task 96개·오류 0 | 동일 |
| `python[3] -B -X utf8 tools/check_versions.py --self-check` | exit 0, 소비자 검사 미실행 문구 확인 | 동일 |
| `python[3] -B -X utf8 -m unittest discover -s tests -p 'test_*.py'` | `-v` 실행, exit 0, 67 tests·skip 0, 4.454초 | exit 0, 67 tests·skip 0, 3.174초 |
| `git diff --check 12fb3a816e5ebbdf9822a2c17ea7ad5534195fb9 HEAD` | exit 0, 출력 없음 | 별도 반복 안 함 |

WSL 검증은 `wsl -d Ubuntu-26.04 --cd /mnt/f/dev/kor-travel-common-wt/review-phase0-a -- python3 ...`로 동일 candidate에서 수행했다.

## 원 finding disposition

| ID | 판정 | 확인한 근거 |
|---|---|---|
| A-P1-01 | FIXED | 미해석·빈·무관 숫자 접미부 설치 버전의 NO_LOCK/실패 회귀가 양 OS에서 통과 |
| A-P1-02 | FIXED | 빈 실제 scope·빈/누락 lockfiles 입력 오류 exit 2 회귀가 양 OS에서 통과 |
| A-P1-03 | FIXED | 하한 없는 OR·미지원 범위의 NO_ENGINES 및 AND 하한 회귀가 양 OS에서 통과 |
| A-P1-04 | FIXED | enforce/floor/미지 필드 오류 exit 2, 정상 registry self-check가 양 OS에서 통과 |
| A-P1-05 | FIXED | 최초 URL 3건의 음성 회귀와 잔여 Python fragment 2건의 실제 CLI 실패 및 아래 문맥별 양성·음성 fixture 확인 |
| A-P2-01 | FIXED | 동일 완료일·PR 접미부를 상세/원장 양쪽에 넣는 규칙과 검사 fixture가 양 OS에서 통과 |

## 추가 CLI 공격·정상 경계 8건

`tests/test_check_versions.py`의 fixture 생성기로 각 입력을 별도 임시 repo에 만들고 실제 CLI를 `--registry <임시 registry> --repo app-fail --no-step-summary --quiet --json <임시 출력>`으로 실행했다. 함수 반환만 확인한 결과가 아니다.

| 문맥·입력 | 실제 판정 | exit |
|---|---|---|
| Python `git+https://github.com/example/pkg.git@main#v1.2.3` | FLOATING_REF | 1 |
| Python `git+https://github.com/example/pkg.git#v1.2.3` | FLOATING_REF | 1 |
| Python `@py-v0.1.0#subdirectory=src` | OK | 0 |
| Python `@<40자 SHA>#subdirectory=src` | OK | 0 |
| npm `git+https://github.com/example/pkg.git#v1.2.3` | OK | 0 |
| npm `git+https://github.com/example/pkg.git#<40자 SHA>` | OK | 0 |
| uv `https://github.com/example/pkg?rev=main#<40자 SHA>` git source | OK | 0 |
| uv `https://github.com/example/pkg?rev=main#v1.2.3` git source | FLOATING_REF | 1 |

이전 pip resolver 대조에서 Python의 실제 revision이 main/미지정임을 입증한 두 입력이 이제 검사기의 오류 판정과 일치한다. uv의 resolved 전체 SHA는 선언 branch 판정과 다른 문맥임을 양성 fixture로 확인했다.

## 남은 검증 범위

- PR 원격 CI 조회: NOT_RUN(이번 reviewer는 Windows·WSL 실행을 직접 확인). coordinator의 해당 commit CI 증거와 별도 연결한다.
- Python 3.11/3.12/3.13 개별 실행: NOT_RUN(이번 환경은 3.14). 해당 지원 매트릭스는 후속 CI task의 gate다.
- 패키지 build·pack/wheel 설치·소비자 build/e2e: NOT_RUN(실물 패키지 부재). 제품 릴리스·권리 gate의 PASS가 아니다.
- T-005·T-005a·T-005b의 실제 소비자 7곳·지원 parser 확대, 규칙별 개별 확정은 여전히 후속 task다.
- 아직 제출되지 않은 완료 상태 이동 delta는 이 candidate PASS에 포함하지 않는다. 완료 gate·evidence·원장 변경은 별도 검토 대상이다.
