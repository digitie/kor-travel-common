# T-005c POST3D Reviewer A 독립 원본

- 실행 ID: T005C-A-POST3D-20260907-165524-5807E53
- 판정: PASS. 이번 범위에서 미해결 P0/P1/P2/P3 finding 없음.
- candidate: `5807e535c16310c41c21f9efce87b2113aa17ee5`
- tree: `5f5ce75f627c3b786a96c81532044ce100b30a0c`
- parent: `0f55acc2211718d91ce056b096046054b037d7e4`
- 누적 코드 대조 기준: `ae6d25711ac04a03db7b8182bd7ffae4a1b2d852`
- manifest: `.git/codex-audit/2026-09-07-t005c-post3d-manifest.md`
- manifest SHA256 직접 일치: `D1AB00A0F4462AEEB1F99E14C6E3FA2C36A5BDD7FA28AE23C6B60278F3C8C451`
- 새 detached worktree: `F:/dev/kor-travel-common-wt/review-t005c-post3d-a`
- 시작: 2026-09-07T16:55:24.7391523+09:00. HEAD/tree는 위 candidate/tree와 일치, porcelain 출력 0행.
- 종료: Windows 2026-09-07T08:00:14.057621Z, WSL 2026-09-07T08:00:15.956175Z. HEAD/tree 일치, Windows/WSL porcelain 출력 0행.
- 다른 reviewer 결과와 이전 raw/report 미열람. 후보·소비자 파일 수정, commit, push 없음. 보고서는 기본 checkout의 지정된 Git 내부 경로에만 저장했다.

## 전달 요청

> POST3D exact final review를 시작하세요. candidate `5807e535c16310c41c21f9efce87b2113aa17ee5`, tree `5f5ce75f627c3b786a96c81532044ce100b30a0c`, parent `0f55acc2211718d91ce056b096046054b037d7e4`, manifest `.git/codex-audit/2026-09-07-t005c-post3d-manifest.md`, SHA256 `D1AB00A0F4462AEEB1F99E14C6E3FA2C36A5BDD7FA28AE23C6B60278F3C8C451`. 새 detached clean worktree에서 exact SHA만 검토하고 상대 결과·이전 raw/report를 읽지 마세요. 후보 수정/commit/push 금지. parser/YAML quote·indicator·flow/list·run/with·redaction·repo identity·Docker single repository·plain/flow delimiter quote를 재현하고 전체·focused tests/validators를 Windows/WSL에서 실행하세요. raw `.git/codex-audit/2026-09-07-t005c-post3d-reviewer-a.md`에 시작/종료 SHA/tree/clean·NOT_RUN·verdict·hash를 기록하세요.

## 검토와 동일성

parent 대비 변경은 `tools/check_versions.py` 1행과 `tests/test_check_versions.py` 2행 추가다. 전체를 읽었다. 누적 코드 delta는 구현 56행 추가/16행 삭제, 시험 108행 추가/2행 삭제다. quote 문맥·indicator·run/with 자료형·Docker 이름·redaction·repo 원 식별자 사용·mode_source 출력 경계를 대조했다.

AGENTS·문서 라우터·resume·T-005c·versions 정본·registry·CI workflow가 누적 기준과 동일함을 `git diff --quiet`로 확인했다. 이미 읽은 정본의 해석을 재사용하며, 이전 시험 성공은 이번 시험 성공으로 세지 않았다. T-005c와 versions §3.8/§8의 2칸 block map/list·단순 scalar flow sequence·미지원 exit 2 계약을 적용했다. 이전 원본/상대 원본을 포함한 역사 artifact 본문은 읽지 않았다.

## 실행 명령과 결과

Windows Python 3.14.3, WSL Ubuntu-26.04의 uv managed Python 3.11.15에서 새 candidate를 직접 실행했다. 모든 Python 명령은 `-B -X utf8`를 사용했다. WSL은 다음 진입점이다.

```text
wsl -d Ubuntu-26.04 --cd /mnt/f/dev/kor-travel-common-wt/review-t005c-post3d-a -- /home/digitie/.local/bin/uv run --no-project --python 3.11 python -B -X utf8 ...
```

WSL Git 기반 validator에는 해당 프로세스 안에서만 `GIT_DIR=/mnt/f/dev/kor-travel-common/.git/worktrees/review-t005c-post3d-a`, `GIT_WORK_TREE=/mnt/f/dev/kor-travel-common-wt/review-t005c-post3d-a`를 지정했다. 저장소 설정은 변경하지 않았다.

| 명령 | Windows 실제 결과 | WSL 실제 결과 |
|---|---|---|
| `python -B -X utf8 -m unittest discover -s tests -p 'test_*.py'` | 179개, 60.020초, OK, skip 0 | 179개, 34.987초, OK, skip 0 |
| `python -B -X utf8 -m unittest discover -s tests -p 'test_check_versions.py'` | 84개, 26.881초, OK, skip 0 | 84개, 26.072초, OK, skip 0 |
| `python -B -X utf8 tools/validate_document_links.py` | 311문서/2202 target, 오류 0 | 311문서/2202 target, 오류 0 |
| `python -B -X utf8 tools/validate_plan.py` | 102 task, 오류 0 | 102 task, 오류 0 |
| `python -B -X utf8 tools/check_spdx.py` | 29파일, 오류 0 | 29파일, 오류 0 |
| `python -B -X utf8 tools/scan_secrets.py --all` | 386파일, 발견 0 | 386파일, 발견 0 |
| `python -B -X utf8 tools/check_prod_redaction.py --all` | 386파일, 발견 0 | 386파일, 발견 0 |
| `python -B -X utf8 tools/check_versions.py --self-check` | exit 0, registry 자체 검사 | exit 0, registry 자체 검사 |
| `git diff --check <parent> HEAD` | exit 0 | exit 0 |

Windows의 누적 기준 대비 `git diff --check`도 exit 0이다. Plan 검사는 읽기 전용 metadata/DAG 검사이며 제품 gate로 세지 않았다.

## 직접 CLI 공격과 누적 disposition

두 OS 각각 116회 CLI를 실행해 exit·finding·행/경로·출력 비공개를 직접 대조했다. 원래 77개 반례/대조군, checked-in fixture와 manifest 9개, symlink 3개, plain/Docker/repo 정책 15개, flow colon 4개, 추가 flow 조합 8개다. 임시 디렉터리와 기존 시험 registry를 사용했고 실제 소비자를 읽거나 쓰지 않았다. 합성 비밀·사설 주소는 조각으로 생성하고 원문 stdout을 출력하지 않았다. stdout(annotations 포함)·stderr·JSON·Markdown·step summary를 캡처해 원문 잔류 여부를 대조했다.

기본 실행은 `python -B -X utf8 <candidate>/tools/check_versions.py <temporary-root> --registry <temporary-registry> --repo app-a --mode fail --json <temporary-json> --markdown <temporary-md>`이며 `GITHUB_STEP_SUMMARY`를 별도 임시 파일로 지정했다. manifest/정책 대조는 아래 기록처럼 인자를 바꿨다.

| 원 ID | 원 심각도 | 현재 disposition | 직접 확인한 경계 |
|---|---|---|---|
| A-P1-01 | P1 | FIXED | secret ref/Node/경로, password assignment·접두어·quoted assignment·private IPv4/IPv6·password hash의 출력 원문 잔류 0 |
| A-P1-02 | P1 | FIXED | 잘못된 colon/alias/quote/flow 닫힘, 예약 indicator를 모두 exit 2로 닫음 |
| A-P2-03 | P2 | FIXED | 빈/missing/operationless job·step, 정상 step과 섞인 빈 구조, run list/null/빈 문자열, step/reusable job with list/null 모두 exit 2 |
| A-P2-04 | P2 | FIXED(계약 명시 포함) | with-first 2칸 구조가 실제 Node/uses 행으로 보고됨. 4칸·indentless·trailing separator는 명시된 미지원 subset으로 exit 2 |
| A-P2-05 | P2 | FIXED | plain apostrophe/double quote/공백, YAML escape, comma/colon/bracket 뒤 plain quote, flow의 colon 및 뒤 인용 hash 조합을 보존 |
| A-P2-06 | P2 | FIXED | 공백이 붙은 setup-node 참조에서도 Node 18을 BELOW_FLOOR로 탐지 |
| A-P2-07 | P2 | FIXED | high/low surrogate를 traceback·UnicodeEncodeError 없이 exit 2로 닫음. 정상 Unicode 경계는 유지 |
| A-P2-08 | P2 | FIXED | workflow file/directory 및 local action의 root 밖 symlink 3종을 두 OS 모두 exit 2로 닫음 |

A-P2-05의 마지막 반례는 다음 job 일부로 재현했다. 이번에는 양 OS에서 exit 0과 checkout uses OK, 원본 uses 10행을 얻었다. 같은 두 번째 항목을 double quote로 바꾼 경우도 동일하다.

```yaml
jobs:
  build:
    strategy:
      matrix:
        target: ['a: b', ' #tag']
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
```

위 예시의 행 번호는 별도의 name/on 두 줄을 앞에 넣은 실제 fixture의 10행을 뜻한다. 추가로 plain quote colon, quoted bracket, doubled single quote colon을 섞은 4개 정상 값은 exit 0, 닫히지 않은 마지막 quote·중복/말미 separator·flow mapping 4개는 exit 2였다. plain `Build, 'test`, `foo:'bar`, `a[ 'b`도 각각 exit 0이다. YAML 1.2.2 §7.3.3의 plain 문맥과 인용 문맥을 구분해 기대값을 정했다([공식 규격 revision 1.2.2](https://yaml.org/spec/1.2.2/#733-plain-style), 조회 2026-09-07).

Docker 단일 repository `a.b_c:1.2`, double underscore와 연속 dash는 OK, 연속 dot와 triple underscore는 FLOATING_REF를 유지했다. registry port·digest 대조도 유지했다. 단일 이름과 registry/remote 이름 구분은 [Distribution reference v0.6.0 regexp.go](https://github.com/distribution/reference/blob/v0.6.0/regexp.go)와 [normalize.go](https://github.com/distribution/reference/blob/v0.6.0/normalize.go)를 근거로 대조했다(조회 2026-09-07). 이미지 존재 여부는 검사하지 않았다.

표시용으로 가려지는 합성 이름을 디렉터리 이름과 consumers key로 사용하고 `--repo`·`--mode`를 생략했다. `--today 2026-09-07`에서 원 repo의 fail 정책이 유지되며 만료 예외는 EXEMPT_EXPIRED/exit 1, 유효 예외는 EXEMPT/exit 0, 예외 없는 Node 18은 BELOW_FLOOR/exit 1이었다. repo/roots/mode_source를 포함한 모든 캡처 채널에서 합성 원문 잔류는 0이다.

checked-in static fixture는 report 모드 5 finding(uses 10·12·15·17행, Node 14행), dynamic fixture는 4 finding(uses 15·18행, NO_ENGINES 17·20행)이었다. malformed fixture 4종은 exit 2였다. 빈 lockfiles manifest의 root workflow 이동 ref를 report/warn/fail로 실행해 세 모드 모두 7행 FLOATING_REF가 추가되고 exit는 각각 0/0/1이었다.

## 실제 CI 관찰

`gh run list --commit 5807e535c16310c41c21f9efce87b2113aa17ee5 --json databaseId,headSha,event,status,conclusion,url`와 `gh run view 34097813843 --json headSha,conclusion,event,jobs,url`로 exact SHA를 확인했다. [PR run 34097813843](https://github.com/digitie/kor-travel-common/actions/runs/34097813843)은 pull_request/completed/success다. docs·check-versions·secret-scan·tools(ubuntu-24.04)·tools(windows-2025) 5개 job이 모두 success이며, 마지막 Windows job 종료는 2026-09-07T07:55:31Z다. 위 로컬 시험 건수와 CI 성공은 별개 증거로 기록했다.

## 새 finding·미검증·최종 판정

새 P0/P1/P2/P3 finding 없음. 위 누적 A finding은 모두 수정 확인했다. 최종 PASS는 이 immutable candidate와 문서에 명시된 제한 입력 범위에 대한 독립 판정이다.

- NOT_RUN: release push CI 별도 실행, 원격 Actions 설치/실행·실제 major 조회, Docker pull/inspect. manifest 범위 밖이며 로컬 판정으로 대체하지 않았다.
- NOT_RUN: 소비자 실측·소비자 빌드/e2e·패키지 build/install/publish·npm/PyPI 게시. common fixture 검증만 수행했다.
- NOT_RUN: CI job 로그의 개별 시험 건수/checkout 내부 로그 재감사. API의 exact head SHA·job 결론을 직접 확인한 범위만 주장한다.
- 재사용: 변경 없는 정본과 입력 fixture의 기존 독립 해석. 시험·validator·CLI 결과는 전부 이번 candidate에서 새로 실행했다.
