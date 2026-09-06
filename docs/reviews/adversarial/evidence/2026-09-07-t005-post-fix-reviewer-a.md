# T-005 full post-fix 독립 리뷰 — Reviewer A

- 실행 ID: `T005-A-POSTFIX-20260907-072154-f050997`.
- reviewer: `/root/reviewer_a`. 우선 영역: npm 설치·전이·이름·런타임 수치·경로와 Windows/WSL 회귀.
- 입력: [동일 manifest](2026-09-07-t005-post-fix-manifest.md), [최초 A 원본](2026-09-07-t005-reviewer-a.md).
- Candidate: `f0509970b291a4e1f30ac5499150953ca80ab447`.
- Base: `3bec3eb0d17b986a9140c4f8ba876beb596d560a` — 최초 `409b95c`와 같은 트리라는 전달 기준.
- 격리: `F:/dev/kor-travel-common-wt/review-t005-a` detached worktree.
- 시작: `2026-09-07T07:21:54.5812499+09:00`.
- 검증 종료: `2026-09-07T07:24:15.0419746+09:00`.
- 실제 시작·종료 SHA는 위 candidate와 같고 `git status --porcelain=v1 --untracked-files=all` 출력은 각각 0줄이었다.
- 코드·기존 evidence·소비자 저장소를 수정하지 않았다. 임시 fixture와 원천 추출물은 시스템 임시 디렉터리에서 사용 후 정리했다. 작성한 원본은 이 파일 하나다.
- 최초 원본 확정 후 공개된 B의 최초 원본과 통합 report는 전체 delta로 읽었다. B의 **이번 post-fix 결과는 읽거나 요청하지 않고** 독립 확정했다.
- 최종 verdict: **PASS**. 자신의 최초 P1 5개·P2 1개 모두 **FIXED**. 새 finding 없음.

## 전달 요청 원문

> T-005 full post-fix 리뷰 A를 진행하세요. 동일 manifest F:/dev/kor-travel-common/docs/reviews/adversarial/evidence/2026-09-07-t005-post-fix-manifest.md. candidate f0509970b291a4e1f30ac5499150953ca80ab447, base 3bec3eb0d17b986a9140c4f8ba876beb596d560a(최초409와 동일 트리). 기존 detached F:/dev/kor-travel-common-wt/review-t005-a를 candidate로 옮겼습니다. 자신의 6개 최초 ID 원 심각도로 재확인하고 전체 delta 회귀도 검토. 우선 npm/수치/런타임/경로. 다른 reviewer 새 결과는 읽지 마세요. 실제 geo 원천은 F:/dev/kor-travel-geo-fixes의 inputs.json 고정 commit입니다(읽기만). 코드 수정 금지, 자신의 새 원본 F:/dev/kor-travel-common/docs/reviews/adversarial/evidence/2026-09-07-t005-post-fix-reviewer-a.md만 작성. ID/시각/전달원문/SHA/clean/명령/검증/한계/기존disposition/새finding/verdict 포함. 다른 작업자가 있으므로 타인 편집을 되돌리지 마세요. 소비자 저장소 쓰기 금지. 115 tests 성공을 믿고 공격을 생략하지 마세요.

## 범위와 전체 delta 대조

13개 파일, 578줄 추가·47줄 삭제의 전체 delta를 검토했다. [검사기](../../../../tools/check_versions.py), [회귀 시험](../../../../tests/test_check_versions.py), [versions 규약](../../../standards/versions.md), [T-005](../../../tasks/T-005-versions-registry.md), 고정 입력 수정 evidence, resume·journal·리뷰 원본/통합/index가 범위다.

새 `package_identity`·`installed_version`·`npm_entry`, 전이 선언/링크/resolved 순회, 런타임 하한 지원 문법, 차단 이름/수치 분리, 예외 공백 및 차단 숫자 파서 일치를 직접 읽었다. 과거 보고를 덮어쓰지 않고 수정 후 digest를 별도 보존한 구조를 확인했다. T-005는 IN_PROGRESS이며 이번 재검토 전 DONE/merge한 것으로 쓰지 않았다. npm/PyPI 게시 제외와 후속 계획 정리는 사용자 지시의 인계 기록이며 이 후보에서 구현 완료로 선언하지 않았다.

## 실제 실행 명령과 결과

| 명령/검증 | 실제 결과 |
|---|---|
| `git rev-parse HEAD`, `git status --porcelain=v1 --untracked-files=all` | 시작·종료 candidate 일치, clean |
| `python -B -X utf8 -m unittest discover -s tests -p 'test_*.py'` | Windows Python 3.14.3, 115 tests, 18.208s, skip 0, exit 0 |
| `wsl -d Ubuntu-26.04 --cd /mnt/f/dev/kor-travel-common-wt/review-t005-a -- /home/digitie/.local/bin/uv run --no-project --python 3.11 python -B -X utf8 -m unittest discover -s tests -p 'test_*.py'` | WSL Python 3.11.15, 115 tests, 13.807s, skip 0, exit 0 |
| `python -B -X utf8 tools/check_versions.py --self-check` | 현재일 자체 검사 exit 0 |
| 전체 unittest의 자체 검사 경계 | 미지 정책·예외 공백·차단 숫자 4/5구간·만료일·10판정/3모드 실제 실행 |
| `python -B -X utf8 tools/check_spdx.py` | 13개 파일, 오류 0, exit 0 |
| `python -B -X utf8 tools/validate_document_links.py` | 232개 문서, 1924개 local targets, 오류 0, exit 0 |
| `python -B -X utf8 tools/validate_plan.py` | 상세 task 96개, 오류 0, exit 0 |
| `git diff --check 3bec3eb0d17b986a9140c4f8ba876beb596d560a HEAD` | 출력 없음, exit 0 |
| 최초 공격·대조군 14개 CLI 재실행 | Windows/WSL 각각 14개. 두 환경의 결과 동일 |
| 수정 인접 경계 16개 CLI | Windows/WSL 각각 16개. 두 환경의 결과 동일 |
| 실제 npm v3 링크 생성·manifest 단독 검사 2개 | Windows npm 11.12.1, 일반 이름과 별칭 이름 모두 NO_LOCK·fail exit 1 |
| 소비자 고정 입력 재추출·digest·report 재생성 | Windows, 7곳 48개 입력·306개 판정 전부 일치 |

고장 주입은 후보 도구를 subprocess로 실행하고 임시 JSON report를 읽었다. 명령 형식은 다음과 같다. 기준 registry를 임시 복사하고 npm `bad >=2` 차단 항목만 fixture용으로 더했다. repo는 `review-fixture`, node 기본 선언은 `>=22.12`다.

```text
python -B -X utf8 tools/check_versions.py <임시-입력> --registry <임시-registry> --repo review-fixture --mode fail --today 2026-09-07 --json <임시-report> --quiet --no-step-summary
```

## 최초 finding별 disposition

| 원 ID·원 심각도 | 후보에서 직접 확인한 결과 | Disposition |
|---|---|---|
| A-P1-01 · P1 | 전이 react 링크와 blocked bad 링크 모두 NO_LOCK·exit 1. npm이 생성한 실제 v3 lock의 root manifest 단독 입력도 react NO_LOCK·exit 1 | FIXED |
| A-P1-02 · P1 | 전이 GitHub main archive와 git main 선언+resolved SHA 모두 FLOATING_REF·error annotation·exit 1. scoped wrapper의 중첩 설치도 같은 결과 | FIXED |
| A-P1-03 · P1 | axes 밖 bad 2.0.0-rc.1 및 broken이 NO_LOCK·exit 1. 안정 2.0.0은 BLOCKED, 1.9.0은 비차단 | FIXED |
| A-P1-04 · P1 | react.dom/react_dom 1.0.0이 React 행을 만들지 않고 exit 0. 원 react 및 명시 원 이름이 있는 npm alias의 floor 대조는 유지 | FIXED |
| A-P1-05 · P1 | ^22.12 <20 및 >22.11이 NO_ENGINES·exit 1. >=22.12 <23은 OK. 지원 문법·미지원 보수 판정이 규약과 일치 | FIXED |
| A-P2-01 · P2 | react 19.2.8+build--, 19.2.8+-, 19.2.8+001.build-x가 안정 수치로 OK·exit 0. prerelease는 NO_LOCK 유지 | FIXED |

A-P1-05는 전체 SemVer 구현을 요구하지 않았다. `>22.11`을 직접 최소 버전으로 계산하는 대신 미지원 문법으로 명확히 제한해 NO_ENGINES로 처리한 것은 최초 권고 범위에 맞는다. 새 숫자 비교 규칙을 실제로 지원한다고 과장하지 않는다.

실제 링크 fixture에서는 root `wrapper=file:packages/wrapper`, wrapper `react=file:../react`, 로컬 react `18.3.1`을 사용했다. 두 번째는 wrapper의 의존성 이름을 `renamed`로 바꿨다. 아래 로컬 명령으로 두 lock을 생성했으며 네트워크·소비자 원문 실행은 없었다.

```text
node "C:/Program Files/nodejs/node_modules/npm/bin/npm-cli.js" install --package-lock-only --ignore-scripts --offline --no-audit --no-fund
python -B -X utf8 tools/check_versions.py --manifest <임시-root>/kor-travel-common.lock.json --mode fail --no-step-summary
```

npm은 별칭의 target 메타데이터에 원 이름 react를 기록했다. 수정 코드는 설치 경로 이름과 target 이름을 모두 대조해 두 경우 각각 react NO_LOCK 1행을 남겼다.

## 인접 경계 16개

이 표의 모든 결과는 Windows·WSL 양쪽에서 실제 실행했다. 최초 14개와 별개의 추가 16개이므로 합계는 환경당 30개 CLI 실행이다.

| 추가 입력 | 관찰 |
|---|---|
| 기본 npm registry의 버전 tarball | 위반 없음, exit 0 |
| mirror.example의 미지원 registry tarball | FLOATING_REF, exit 1. 규약에 명시한 한계와 같음 |
| GitHub v1.0.0 Release 자산 | 위반 없음, exit 0 |
| scoped alias link → react target | NO_LOCK, exit 1 |
| scoped wrapper의 git main 선언과 nested resolved SHA | FLOATING_REF 1행, exit 1 |
| 19.2.8+- | react OK, exit 0 |
| 19.2.8+001.build-x | react OK, exit 0 |
| 19.2.8-rc.1 | react NO_LOCK, exit 1 |
| 차단 bad 2.0.0 | BLOCKED, exit 1 |
| 비차단 bad 1.9.0 | 위반 없음, exit 0 |
| 차단 대상 bad broken | NO_LOCK, exit 1 |
| >=22.12 <23 또는 >=24의 OR | node OK, exit 0 |
| >=22.12 또는 *의 OR | NO_ENGINES, exit 1 |
| >=22.12 <22.12 | NO_ENGINES, exit 1 |
| >=22.12 <=24 | NO_ENGINES, exit 1 |
| >=22.12-slim | NO_ENGINES, exit 1 |

직접·전이 React floor 위반과 alias 원 이름 대조는 최초 14개 대조군에서 계속 검출됐다. 새 실패나 회귀 finding은 발견하지 않았다.

## 고정 원천과 보고 재현

[post-fix.json](../../../evidence/t005/post-fix.json)의 checker·registry·inputs·reports SHA-256 네 값이 실제 candidate 파일의 LF/UTF-8 digest와 모두 같았다.

[inputs.json](../../../evidence/t005/inputs.json)의 40자리 commit·경로를 사용해 `git -C <소비자-원천> show <commit>:<path>` bytes를 읽고 48개 파일 SHA-256을 확인했다. geo만 안내된 `F:/dev/kor-travel-geo-fixes`를 사용했다. 소비자의 현재 HEAD·dirty 파일은 입력에 사용하지 않았다.

| 소비자 | 원본 digest | 전체 report 일치 |
|---|---:|---:|
| airport | 4/4 | 24행 |
| concierge | 8/8 | 38행 |
| docker-manager | 3/3 | 18행 |
| geo | 4/4 | 44행 |
| map | 8/8 | 67행 |
| weather | 7/7 | 42행 |
| pinvi | 14/14 | 73행 |
| 합계 | 48/48 | 306행 |

각 임시 루트에 후보 검사기를 `--repo <정식 이름> --today 2026-09-07 --json <임시-report> --quiet --no-step-summary`로 실행했다. 전부 registry의 report 모드·exit 0이다. 문서에 허용한 roots와 registry.path만 정규화한 뒤 findings의 모든 필드와 report metadata 전체가 기존 reports.json과 일치했다. 이 결과는 위반 0 또는 소비자 제품 gate 성공을 뜻하지 않는다. 최초 A 리뷰의 geo NOT_RUN은 이번 독립 실행으로 해소됐으며 과거 원본은 수정하지 않았다.

## 한계와 최종 판정

- NOT_RUN(범위 밖): 소비자 npm ci·uv sync·제품 build/e2e·배포·npm/PyPI 게시. 입력/lock 대조를 이 gate의 성공으로 사용하지 않는다.
- NOT_RUN(이번 reviewer 환경): 실제 npm 링크 생성의 WSL npm 실행. Windows npm 생성 2개와 양 OS의 합성 CLI 30개씩을 구분했다.
- NOT_RUN(중복 실행 불필요): 이번 원천 7곳의 WSL report 재생성. Windows에서 원천부터 전체 구조를 재검증했고 WSL에서는 전체 시험·동일 공격 입력을 실행했다. 작성자의 WSL 원천 재현 주장을 자신의 실행으로 합산하지 않았다.
- NOT_RUN(후속 task): uv/Poetry/requirements 전체 의미, consumer-manifest 정식 스키마, T-009 CI 전체 하드닝. 이 후보가 바꾼 공통 설치 수치/차단 경로의 회귀는 전체 suite에서 실행했다.
- 전체 SemVer/PEP 440 해석을 보증하지 않는다. 미지원 런타임 연산자·사설 registry/mirror의 보수 판정이 현재 규약에 드러나 있음을 확인했다.
- 원격 CI·PR metadata는 직접 재조회하지 않았다. 후보 로컬 검증 결과와 구분한다.

**PASS**는 위 immutable 후보의 T-005 수정에 대한 A의 독립 판정이다. A의 최초 6개 ID는 원 심각도를 유지해 FIXED로 재확인했고 새 finding은 없다. 상대 reviewer의 이번 판정과 필수 절차를 대신하지 않는다.
