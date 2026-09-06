# Phase 0 post-fix Reviewer A 독립 재검토 원본

- Review ID: `2026-09-06-phase0-postfix`
- 실행 ID: `/root/reviewer_a` / `phase0-postfix-a-20260906T182621+0900`
- 전문 영역: Python 판정·registry/ref 입력 경계·문서 validator·Linux 회귀·실패 gate
- 시작: `2026-09-06T18:26:21.0741866+09:00`
- 종료 검증: `2026-09-06T18:31:46.5477549+09:00`에 HEAD·clean 재확인
- Manifest: [post-fix 공통 요청](2026-09-06-phase0-postfix-manifest.md), [최초 공통 요청](2026-09-06-phase0-manifest.md)
- Candidate: `12fb3a816e5ebbdf9822a2c17ea7ad5534195fb9`
- Base: `d3712a8c965c3193a5af13cacd6d22c603e0cfe4`
- 격리: `F:/dev/kor-travel-common-wt/review-phase0-a` detached worktree. 시작·종료 관찰 HEAD는 candidate와 동일하며 `git status --porcelain=v1` 출력이 모두 비었다.
- 독립성: 상대 post-fix 원본을 읽거나 요청하지 않았다. 소유한 이 evidence 외의 추적 파일은 수정하지 않았다. 공격 fixture는 OS 임시 디렉터리에 생성·정리했다.
- 최종 verdict: **BLOCK**. 기존 `A-P1-05`의 원래 세 fixture는 수정됐지만 Python 선언의 실제 revision을 fragment로 덮는 같은 종류의 우회가 남아 있다. 나머지 원 finding 5건은 FIXED로 확인했다.

## 요청과 검토 범위

원 A finding 전부의 재현과 base→candidate 전체 delta 회귀를 요청받았다. 도구·시험 전체 변경, inline code 처리, registry 값 수정, 완료 제목 규칙, ADR-013과 부분 대체 표시, architecture·standards·runbook, 릴리스·승인·facade·하위 task 변경 및 원장 정합을 검토했다. 보존된 상대 reviewer 원본을 독립 결론의 근거로 삼지 않았다.

UI minor와 tokens peer의 의미, Python 0.2 발행 task와 소비자 선행, facade의 extras 경계, 승인된 패키지별 smoke 대상, airport의 과거 WIP와 현재 상태를 구분하는 변경에서 전문 영역의 새 gate 우회는 발견하지 않았다. 실제 외부 코드·권리·registry 조회를 다시 수행한 검토는 아니다.

## 검증 결과

| 검증 | Windows Python 3.14.3 | WSL Ubuntu-26.04 / Python 3.14.4 |
|---|---|---|
| `python[3] -B -X utf8 tools/validate_document_links.py` | exit 0, 문서 193개·target 1699개·오류 0 | 동일 |
| `python[3] -B -X utf8 tools/validate_plan.py` | exit 0, task 96개·오류 0 | 동일 |
| `python[3] -B -X utf8 -m unittest discover -s tests -p 'test_*.py' -v` | exit 0, 65 tests·skip 0, 3.094초 | exit 0, 65 tests·skip 0, 4.090초 |
| `python[3] -B -X utf8 tools/check_versions.py --self-check` | exit 0, 소비자 검사 미실행 문구 확인 | 동일 |
| `git diff --check d3712a8c965c3193a5af13cacd6d22c603e0cfe4 HEAD` | exit 0, 출력 없음 | 별도 반복 안 함 |

Linux 명령은 `wsl -d Ubuntu-26.04 --cd /mnt/f/dev/kor-travel-common-wt/review-phase0-a -- ...`로 동일 detached checkout에서 실행했다. inline code 안의 `def fn[T](...)`, 중첩 backtick span, 실제 link 보존, angle target와 percent encoding은 양쪽 회귀시험에 포함됐다.

PR 원격 CI 조회는 NOT_RUN(이번 리뷰에서는 local/WSL 실행만 직접 확인). Python 3.11·3.12·3.13 각각의 실행, 패키지 build·wheel·tarball·소비자 e2e는 NOT_RUN(이번 후보의 실물 패키지 부재 및 리뷰 환경 범위). 문서·도구 성공을 해당 gate의 성공으로 확대하지 않는다.

## 원 finding별 재확인

| 원 ID | disposition | 직접 재현 결과 |
|---|---|---|
| A-P1-01 | FIXED | lock next `banana`가 `NO_LOCK`, fail exit 1. 숫자 뒤 무관 문자열·빈 버전 회귀도 통과 |
| A-P1-02 | FIXED | 빈 실제 디렉터리와 빈 manifest lockfiles 모두 입력 오류 exit 2. no-scope를 clean run으로 출력하지 않음 |
| A-P1-03 | FIXED | node `<22 || >=22.12`는 `NO_ENGINES`, fail exit 1. 하한 없는/미지원 OR와 AND의 가장 강한 하한 시험 통과 |
| A-P1-04 | FIXED | `enforce=FAIL`, `floor=banana`, 미지 필드 `florr` 모두 명시적 registry 오류 exit 2. 정식 registry self-check는 양 OS에서 성공 |
| A-P1-05 | **OPEN** | 최초 latest release·query SHA+main·일반 latest URL 3개는 FLOATING_REF/exit 1. 아래 Python 선언 fragment 우회는 여전히 OK/exit 0 |
| A-P2-01 | FIXED | 상세 H1과 done 요약 양쪽에 동일 날짜·PR 접미부를 넣으라는 규칙과 fixture가 일치. 직접 만든 DONE fixture의 `PLAN.validate` 결과 `([], 3)` |

입력 오류 fixture는 모두 기존 시험 모듈의 `npm_fixture`/`python_fixture`와 임시 registry 복사본으로 생성하고 실제 `tools/check_versions.py` CLI를 호출했다. `--no-step-summary`로 외부 summary 파일 변경을 막았다.

## A-P1-05 잔여: Python VCS 선언은 fragment를 revision으로 사용하지 않는다

- 위치: `tools/check_versions.py:361-364`, `Checker.record_ref:526-528`.
- 원인: `ref_is_pinned`가 생태계와 선언/lock의 문법을 구분하지 않고 fragment를 path의 `@rev`보다 먼저 확인한다. npm의 `#ref` 문법을 Python 직접 VCS 의존성에도 적용한다.
- 재현 입력 1: `custom-lib @ git+https://github.com/example/pkg.git@main#v1.2.3`.
- 재현 입력 2: `custom-lib @ git+https://github.com/example/pkg.git#v1.2.3`.
- fixture: `requires-python=">=3.12"`, 위 문자열 하나를 project dependency로 사용, `python_fixture(..., locked={})`로 프로젝트 자체가 존재하는 uv lock 생성, registry의 `app-fail`로 검사.
- 실제 CLI: 두 입력 모두 Python runtime과 custom-lib 두 행을 **OK**로 집계하고 `mode=fail findings=2 failing=0 exit=0`; custom-lib 설명은 `git 참조 고정됨`.
- 독립 resolver 대조: 로컬 **pip 26.0.1**의 `pip._internal.vcs.git.Git().get_url_rev_and_auth(URL)`을 네트워크·설치 없이 호출했다. 입력 1은 `('https://github.com/example/pkg.git', 'main', (None, None))`, 입력 2는 `('https://github.com/example/pkg.git', None, (None, None))`를 반환했다. 실제 revision은 각각 움직이는 main과 미지정이며 `v1.2.3`이 아니다.
- 영향: 이 finding에서 요구한 실제 ref 위치 검증이 Python 직접 선언에서는 아직 이뤄지지 않는다. 문서의 branch·미고정 참조 금지와 fail gate를 그대로 우회한다.
- 최소 수정: `record_ref`가 이미 받는 ecosystem 및 선언/uv lock source 종류를 사용해 실제 문법별 revision을 해석한다. Python 직접 VCS 선언의 `@rev`와 `#subdirectory=...`, npm의 `#ref`, uv lock source의 resolved SHA를 구분한다. 단순히 path 우선으로 바꾸는 것만으로는 입력 2의 미지정 revision 우회가 닫히지 않는다. 두 음성 fixture와 정상 Python `@<sha|tag>#subdirectory=...`, npm `#<sha|tag>`, uv resolved SHA 양성 fixture를 함께 고정한다.

재현 핵심:

```python
import json, pathlib, subprocess, sys, tempfile
sys.path.insert(0, "tests")
import test_check_versions as t
from pip._internal.vcs.git import Git

with tempfile.TemporaryDirectory(prefix="review-phase0-post-a-ref-") as tmp:
    root = pathlib.Path(tmp)
    registry = root / "versions.json"
    registry.write_text(json.dumps(t.REGISTRY), encoding="utf-8")
    for index, url in enumerate([
        "git+https://github.com/example/pkg.git@main#v1.2.3",
        "git+https://github.com/example/pkg.git#v1.2.3",
    ]):
        repo = root / str(index)
        repo.mkdir()
        t.python_fixture(repo, requires=">=3.12",
                         deps=["custom-lib @ " + url], locked={})
        result = subprocess.run([
            sys.executable, "-B", "-X", "utf8", str(t.SCRIPT), str(repo),
            "--registry", str(registry), "--repo", "app-fail", "--no-step-summary",
        ], capture_output=True, text=True, encoding="utf-8")
        print(Git().get_url_rev_and_auth(url))
        print(result.returncode, result.stdout)
```

이는 최초 A-P1-05와 같은 판정 결함의 남은 범위이므로 별도 중복 ID를 만들지 않았다. 원래 세 반례의 수정은 인정하되 finding 전체는 다음 immutable candidate에서 닫아야 한다. 다른 원 finding을 되돌리거나 신규 정책·기능을 요구하는 판정은 아니다.
