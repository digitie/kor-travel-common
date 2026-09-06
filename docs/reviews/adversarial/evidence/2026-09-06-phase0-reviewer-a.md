# Phase 0 Reviewer A 독립 적대적 리뷰 원본

- Review ID: `2026-09-06-phase0`
- 실행 ID: `/root/reviewer_a` / `phase0-a-20260906T175945+0900`
- 전문 영역: Python 버전 판정·문서 validator·입력 오류·CI·실패 gate 무결성
- 시작: `2026-09-06T17:59:45.9682076+09:00`
- 종료: `2026-09-06T18:05:10.2843737+09:00`(원본 확정 시 hash·clean 재확인)
- 공통 요청·manifest: [phase0 manifest](2026-09-06-phase0-manifest.md)
- Candidate: `d3712a8c965c3193a5af13cacd6d22c603e0cfe4`
- Base: `b92fabeb1c96a11c1fc9507d93271c1ebeee09b0`
- 격리: `F:/dev/kor-travel-common-wt/review-phase0-a` detached worktree
- 시작·종료 관찰 HEAD: 모두 candidate와 일치. 양쪽 `git status --porcelain=v1` 출력은 빈 문자열.
- 독립성: 상대 reviewer의 원본·finding을 읽거나 요청하지 않았다. 검토·시험은 지정 worktree를 기준으로 했고, 공격 fixture는 OS 임시 디렉터리에서 생성·정리했다. 소유한 이 evidence 파일 외에는 수정하지 않았다.
- 최종 verdict: **BLOCK** — `P1` 5건, `P2` 1건. 정상 회귀시험 성공으로 아래 실패 시나리오를 상쇄할 수 없다.

## 전달받은 review request

> 위 immutable candidate와 base를 확인한 뒤 전문 영역에서 독립 적대적 리뷰한다. 상대 reviewer 결과를 요청하거나 읽지 않는다. 기존 작성자·테스트 성공·accepted 표기만으로 신뢰하지 않는다. 정상 경로뿐 아니라 오입력·누락·실패·잘못된 순서·외부 승인 없이 실행할 때의 문제를 찾는다. finding마다 ID(A/B-Pn-NN), 위치, 근거, 재현 또는 실패 시나리오, 영향, 최소 수정 권고를 기록한다. 취향이나 미래 구현 자체의 부재는 finding으로 만들지 않으며 부재를 성공으로 표시하거나 실행 계획이 막히는 경우는 finding이다.

추가 배정: Python 버전 검사·문서 validator·입력 오류·CI·실패 gate 무결성을 맡고, 이 원본 파일만 작성한다. 다른 편집을 되돌리지 않고 추가 subagent를 생성하지 않는다.

## 검토 범위와 실행 결과

정본 `AGENTS.md`, `docs/README.md`, `docs/resume.md`, T-013, architecture 개요, ADR-008, versions 정책, task 규칙, workflow §5와 리뷰 template을 확인했다. `tools/check_versions.py` 전체·버전 시험, 두 문서 validator와 시험, `.github/workflows/docs.yml`, T-005·T-005a·T-005b를 직접 대조했다. base→candidate의 206개 파일 변경 목록을 확인했으며 전문 영역 밖 27,320행 전체를 줄 단위로 검토했다고 주장하지 않는다.

| 명령·검증 | 실제 결과 |
|---|---|
| `git rev-parse HEAD`, `git status --porcelain=v1` | 시작·종료 모두 candidate·clean |
| `python --version` | Python 3.14.3, Windows |
| `python -B -X utf8 tools/validate_document_links.py` | exit 0, 문서 184개·local target **1648개**·오류 0 |
| `python -B -X utf8 tools/validate_plan.py` | exit 0, 상세 task 93개·오류 0 |
| `python -B -X utf8 -m unittest discover -s tests -p 'test_*.py' -v` | exit 0, 57개 성공·skip 0, 1.271초 |
| `git diff --check b92fabeb1c96a11c1fc9507d93271c1ebeee09b0 HEAD` | exit 0, 출력 없음 |
| 임시 공격 fixture 12개 | 아래 재현 결과. 검사 도구가 성공을 돌려주는 반례를 확인 |
| PR CI 원격 실행 | NOT_RUN(이 리뷰에서 원격 CI를 조회하지 않음); workflow 내용만 확인 |
| Linux/WSL·Python 3.11 실행 | NOT_RUN(이 실행은 Windows Python 3.14.3) |
| 실물 패키지 build·pack/wheel 설치·소비자 build/e2e | NOT_RUN(candidate에 실물 패키지 없음). 해당 패키지·소비자 task의 gate 유지 |

candidate resume에는 local target 1666개라고 적혀 있으나 이번 immutable 실행은 1648개였다. 최종 인계 수치는 최종 commit에서 다시 실행한 값으로 기록해야 한다. 별도 gate 결함 finding으로 세지는 않았다.

## A-P1-01 파싱 실패한 설치 버전을 OK로 집계한다

- 위치: `tools/check_versions.py:419-425`의 `Checker.judge`, 호출부 `record_axis`.
- 근거: [versions 정책](../../../standards/versions.md) §3.3의 `OK`는 floor·max·recommended 확인 결과이고, AGENTS §6.10은 미검증 값을 정상값으로 표시하지 못하게 한다.
- 재현: 시험의 `npm_fixture`로 `engines.node=">=22.12"`, 선언 `next="^16.3.4"`, lock 설치본 `next="banana"`를 만들고 `app-fail` registry로 CLI 실행.
- 실제: next 행 `installed="banana", verdict="OK", detail="판정 불가(버전 파싱 실패)"`; JSON `OK=2`, `failing=0`, `mode=fail`, exit 0. 상태 값과 설명이 직접 모순된다.
- 영향: 손상됐거나 미지원 형식인 lock이 정상 설치본·승격용 무위반 실행으로 집계된다. 단순히 report 모드라서 생기는 문제가 아니다.
- 최소 수정: 파싱 불가 설치본은 `NO_LOCK` 등 기존 비정상 판정 또는 명시적 입력 오류로 처리하고 fail 모드에서 실패시킨다. 오류·누락·숫자 접미부 경계 fixture를 추가하되 지원하지 않는 형식을 정상화해 삼키지 않는다.

## A-P1-02 검사 범위가 0개여도 fail 모드가 성공한다

- 위치: `tools/check_versions.py:819-851`, `exit_code:724-727`, 빈 findings 출력 `753-754`.
- 근거: versions 정책 §3.2 lock 의무·§3.5 위반 0 실행 2회의 승격 조건, AGENTS §6.4의 0 test·skip 성공 집계 금지.
- 재현 1: 실제 존재하지만 비어 있는 디렉터리를 CLI positional path로 전달하고 `--repo app-fail`.
- 재현 2: `{"schema":"kor-travel-common.consumer-manifest.v1","repo":"app-fail","lockfiles":[]}`를 `--manifest`로 전달.
- 실제: 두 경우 모두 JSON `findings=[]`, 모든 summary 값 0, `mode=fail`, exit 0. 표에는 대상 없음이 나오지만 기계 판정은 성공이다.
- 영향: 잘못된 checkout 위치, manifest의 lockfiles 누락 또는 탐색 대상 제거가 clean run으로 보인다. CI 삽입·승격 도구가 결과를 그대로 소비하면 검사를 수행하지 않고 gate가 녹색이 된다.
- 최소 수정: 명시 입력에서 scope를 찾지 못하면 `NO_LOCK` 또는 입력 오류로 판정한다. JSON에서도 검사하지 않은 상태가 실패 후보 0 성공으로 보이지 않게 하고 빈 루트·빈/누락 lockfiles fixture를 추가한다.

## A-P1-03 OR 범위에서 하한이 없는 가지를 버려 낮은 런타임을 허용한다

- 위치: `tools/check_versions.py:91-130`, 특히 `121-122`.
- 근거: versions 정책 §3.3은 하한 없는 런타임 범위를 `NO_ENGINES`로 정의한다. floor 미만 버전을 허용하는 선언을 `OK`로 판정할 근거가 없다.
- 재현: 정상 next lock과 `engines.node="<22 || >=22.12"`로 fail 모드 실행.
- 실제: `<22` 가지를 버리고 `installed="22.12", verdict="OK", detail="하한 22.12"`, 전체 exit 0.
- 영향: 이 선언은 Node 20도 허용하지만 도구는 floor 22.12가 강제된 것으로 보고한다. 런타임 정렬과 clean-run 증거가 틀린다.
- 최소 수정: OR의 모든 가지가 하한을 증명해야 한다. 한 가지라도 하한이 없거나 파싱할 수 없으면 비정상 범위로 보고한다. AND 조건에서는 교집합의 가장 강한 하한, OR에서는 합집합의 가장 낮은 하한을 계산하도록 분리하고 compound 범위 시험을 추가한다.

## A-P1-04 잘못된 registry가 강제 수준·floor를 조용히 해제한다

- 위치: `tools/check_versions.py:195-221`의 `Registry.load`, `233-238`의 `enforce`, `424-429`의 floor 파싱.
- 근거: T-005의 strict 스키마·미지 필드 거부 수용 기준과 versions 정책 §3.5의 common 소유 강제 수준. 초기 구현이라도 제공 중인 CLI가 오류 입력을 더 약한 정책으로 바꾸면 안 된다.
- 재현 1: 시험 registry의 `consumers.app-fail.enforce`를 `"FAIL"`로 바꾸고 floor 미만 next 15.0.0 lock 검사.
- 실제 1: registry 오류 없이 `mode=report`, `BELOW_FLOOR=1`, exit 0. fallback이 오입력을 정상 기본 정책으로 둔갑시킨다.
- 재현 2: 정상 fail 모드 registry에서 `axes.next.floor="banana"`, next 15.0.0 lock 검사.
- 실제 2: floor가 사라져 `NOT_RECOMMENDED` 정보 행만 남고 exit 0. 또한 `florr` 같은 미지 필드를 넣어도 로더가 거부하지 않음을 확인했다.
- 영향: 레지스트리 오타가 fail gate를 끄거나 버전 하한을 제거한다. 현재 T-005 잔여를 추적한다는 문구는 이 잘못된 성공 결과를 닫지 못한다.
- 최소 수정: loader에서 알려진 필드·타입·enforce enum·버전/차단 범위·참조 무결성을 검사하고 잘못된 설정은 명시적 오류로 실패시킨다. 미등록 소비자의 의도된 report 기본값과 등록 소비자의 잘못된 설정을 구분한다. `--self-check` 잔여 상태와 실제 검사 범위도 T-005에 정확히 표시한다.

## A-P1-05 불변 ref 검사가 latest 자산과 URL 일부 문자열을 고정으로 오판한다

- 위치: `tools/check_versions.py:277-305`의 `ref_is_pinned`·`is_vcs_spec`, npm 호출 `514-518` 부근.
- 근거: versions 정책 §3.8의 `latest` 태그·branch 금지와 §3.3의 git/URL 의존성 판정.
- 재현 1: npm 직접 의존성 URL `https://github.com/example/pkg/releases/download/latest/pkg.tgz`.
- 실제 1: `/releases/download/` 문자열만으로 `OK`·`git 참조 고정됨`, fail exit 0. tag 이름을 검사하지 않는다.
- 재현 2: `git+https://github.com/example/pkg.git?cache=0123456789012345678901234567890123456789#main`.
- 실제 2: query의 임의 40자 hex가 `SHA_RE.search`에 잡혀 실제 `#main`을 보지 않고 `OK`, fail exit 0.
- 재현 3: `https://example.com/packages/latest.tgz`를 npm 의존성으로 전달.
- 실제 3: host가 github/gitlab이 아니라 ref 검사 자체가 생략되고 node OK 1개만 남는다. fail exit 0.
- 영향: 문서에서 반드시 오류로 드러내도록 정한 움직이는 참조가 정상 ref 또는 검사 대상 외로 처리된다. immutable 배포 계약을 보증하지 못한다.
- 최소 수정: URL·VCS 구조에서 실제 ref 위치를 추출해 검증한다. SHA는 ref 위치에서만 인정하고 release 경로는 tag를 확인한다. 일반 HTTP(S) 직접 의존성도 명시된 immutable 형식 또는 실패 판정을 거치게 한다. 세 fixture를 회귀 시험으로 고정한다.

## A-P2-01 완료 원장 날짜·PR 표기 지침이 제목 일치 검사와 충돌한다

- 위치: `docs/tasks-rule.md:53`, `78`; `tools/validate_plan.py:191-193`.
- 근거: §6은 완료 요약의 4열 제목 뒤에 `(2026-09-06, PR #1)`을 쓰라고 하지만 §4와 validator는 상세 H1 제목과 전체 문자열 일치를 요구한다. 상세 H1에도 완료 이력을 붙이라는 절차는 없다.
- 재현: 기존 `PlanValidationTests` fixture에서 T-001을 DONE으로 변경하고 archive로 이동한 뒤 §6대로 요약 제목만 `기반 (2026-09-06, PR #1)`로 기록.
- 실제: `T-001 요약 제목 불일치` 오류 1개. 완료일이 없는 기존 DONE fixture는 통과한다.
- 영향: 다음 에이전트가 명시된 완료 처리 절차를 그대로 따르면 문서 CI가 실패한다. H1을 임의로 바꾸거나 날짜·PR 기록을 누락해야 한다는 숨은 선택이 생긴다.
- 최소 수정: 제목 일치 의미와 완료 metadata 저장 위치를 하나로 정한다. 예를 들어 날짜·PR은 상세 metadata나 요약 외 별도 행에 두고 제목은 동일하게 유지하거나, 양쪽 제목을 같이 바꾸는 절차를 명시한다. 선택한 완료 형식의 회귀 fixture를 추가한다.

## 공격 fixture 재현 방법

모든 도구 CLI는 `--no-step-summary`로 실행해 외부 summary 파일에 쓰지 않았다. 아래 코드는 candidate root에서 stdin으로 실행한 공격 코드의 핵심이며 `tests/test_check_versions.py`의 고정 fixture 생성기와 실제 CLI를 재사용한다. 테스트 생성기의 존재를 코드 안전성 증거로 쓰지 않고 입력 제작에만 썼다.

```python
import copy, json, pathlib, subprocess, sys, tempfile
sys.path.insert(0, "tests")
import test_check_versions as t

with tempfile.TemporaryDirectory(prefix="review-phase0-a-") as tmp:
    root = pathlib.Path(tmp)
    registry = root / "versions.json"
    registry.write_text(json.dumps(t.REGISTRY), encoding="utf-8")

    def run(repo=None, options=(), reg=registry):
        command = [sys.executable, "-B", "-X", "utf8", str(t.SCRIPT),
                   "--registry", str(reg), "--repo", "app-fail",
                   "--no-step-summary"]
        if repo is not None:
            command.append(str(repo))
        result = subprocess.run(command + list(options), capture_output=True,
                                text=True, encoding="utf-8")
        print(result.returncode, result.stdout, result.stderr)

    empty = root / "empty"
    empty.mkdir()
    run(empty)
    manifest = root / "manifest.json"
    manifest.write_text(json.dumps({"schema": t.CV.MANIFEST_SCHEMA,
                                   "repo": "app-fail", "lockfiles": []}),
                        encoding="utf-8")
    run(options=("--manifest", str(manifest)))
    for label, version, node in [("invalid", "banana", ">=22.12"),
                                 ("union", "16.3.4", "<22 || >=22.12")]:
        repo = root / label
        repo.mkdir()
        t.npm_fixture(repo, deps={"next": "^16.3.4"},
                      engines={"node": node}, installed={"next": version})
        run(repo)
```

A-P1-04는 같은 fixture의 registry 복사본에 `enforce="FAIL"`, `floor="banana"`, 미지 필드 `florr`를 각각 적용해 실행했다. A-P1-05는 위 3개 URL을 `deps={"custom-lib": URL}`, 설치 버전 1.0.0으로 넣어 실행했다. A-P2-01은 기존 plan fixture의 `items[0]["status"]="DONE"` → `write_repo()` 후 done 요약의 `| 기반 |`만 `| 기반 (2026-09-06, PR #1) |`로 바꿔 `PLAN.validate`를 호출했다.

추가로 next `16.2.0-rc.1`을 주입했을 때 숫자 접두 파싱으로 `NOT_RECOMMENDED`·exit 0이 나왔다. 현재 정책이 접두 비교를 명시하고 pre-release 지원 의미를 별도로 정하지 않아 독립 finding으로 세지 않았다. 지원 형식을 정할 때 이 경계도 명시해야 한다.

## 남은 불확실성과 판정 범위

- malformed JSON/TOML의 모든 구조·uv marker/복수 source 조합·PEP 440 전체 문법을 완전 탐색하지 않았다. 실패를 정상값으로 바꾸지 않는 보수적 입력 정책과 음성 fixture가 필요하다.
- `.github/workflows/docs.yml`은 전체 도구 테스트와 base→HEAD whitespace 검사를 실행하도록 바뀌었다. SHA 핀·권한·자체 check-versions job의 미구현은 T-009 잔여로 표시돼 있어 그 부재 자체는 finding으로 세지 않았다.
- 현재 도구 결과는 제품 gate가 아니라는 설명이 있지만, `OK`·`failing=0`·exit 0의 잘못된 판정 자체를 정당화하지는 못한다.
- 원본 finding의 수정·기각은 새 post-fix commit에서 독립 재확인해야 한다. 이 원본을 수정 결과로 덮어쓰지 않는다.
