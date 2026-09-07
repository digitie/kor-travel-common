# T-005a post2 독립 full 리뷰 B 원본

- 실행 ID: `B-T005A-POST2-20260907-123403-735efed`
- 최종 판정: **BLOCK**. 원 `B-P1-01`·`B-P1-02`는 FIXED, 새 `B-P1-03`은 OPEN이다.
- 시작: 2026-09-07T12:34:03.1845000+09:00. 종료 SHA·clean 재확인: 2026-09-07T12:40:49.1258797+09:00.
- candidate: `735efed760d2703b3f5769e58270954352566f39`.
- base: `6e1881b86f017d604ccfa416bd368e5aba24c669`. post-fix delta 기준: `902750016d157bb195fb05c01358c4b8a6ffe812`.
- 실제 시작·종료 HEAD는 candidate와 일치한다. tree: `46c5019b2c09d2f946b800f13b042ff6029aa46e`.
- 새 detached worktree: `F:/dev/kor-travel-common-wt/review-t005a-post2-b`. 직접 `git worktree add --detach`로 생성했고 시작·종료 `git status --porcelain=v1` 출력은 비어 있었다.
- 후보·소비자·과거 report를 수정하지 않았다. 실제 소비자 저장소 쓰기와 registry 게시를 하지 않았다. 임시 합성 입력·Git 저장소만 생성·정리했다. 원본 보고서는 지정된 `.git/codex-audit` 한 파일에 저장한다.
- B 이전 원본의 반례·disposition을 읽었다. A 결과는 읽거나 요청·공유하지 않았다. candidate의 추가 파일 목록에 A 원본이 포함된 사실만 확인했고 그 내용은 열지 않았다.

## 전달 요청 원문

> 새 수정 후보 `735efed760d2703b3f5769e58270954352566f39`에 대해 T-005a 사후 독립 full 리뷰를 다시 실행해 주세요. base는 `6e1881b86f017d604ccfa416bd368e5aba24c669`, 새 detached worktree는 `F:/dev/kor-travel-common-wt/review-t005a-post2-b`로 고정하세요. 이전 B 원본의 B-P1-02 반례와 이번 수정 delta를 읽고, A 결과는 읽거나 공유하지 마세요. branch=`topic@v1.2.3` 및 %40, tag/rev/normal branch 구분, 모든 lock SHA·marker 순서, URL/group 구조 경계, versions/정본 일치와 최초 모든 반례를 Windows/WSL에서 다시 공격하세요. 전체 140+ 회귀와 validators를 실행하고 consumer write는 하지 마세요. 결과를 `.git/codex-audit/2026-09-07-t005a-post2-reviewer-b.md`에 원본으로 저장해 주세요. 수정은 하지 말고 정확한 SHA/clean 상태·PASS/BLOCK·finding disposition·NOT_RUN을 보고하세요.

## 범위와 재사용

이전 후보 대비 변경 5파일의 경계를 확인했다. 실행 코드·시험 2파일의 전체 delta를 읽었고 나머지 3파일은 이전 리뷰의 manifest·원본 기록이다. A 원본 내용은 독립성 조건에 따라 읽지 않았다. base 대비 구현·규약·task·fixture 전체 범위는 최초 리뷰 및 post-fix 리뷰에서 읽은 결과에 이번 delta를 더해 대조했다.

`AGENTS.md`, `docs/README.md`, `docs/resume.md`, T-005a 상세 task, 버전 정본, `versions.json`이 이전 후보와 동일함을 `git diff --quiet`로 확인했다. 해당 읽기 결과를 재사용한다. Python floor 3.11과 uv floor 0.11/recommended 0.12, 알려진 lock schema와 미지원 입력 오류 정책은 변경되지 않았다. task는 아직 IN_PROGRESS다.

## 실제 검증

| 검사 | 결과 |
|---|---|
| Windows `py -3.14 -B -X utf8 -m unittest discover -s tests -p 'test_*.py'` | Python 3.14.3, 140 tests, 31.801초, OK, skip 0 |
| WSL Python 3.11.15의 같은 unittest 명령 | 140 tests, 14.571초, OK, skip 0 |
| Windows·WSL 각각 `tools/validate_document_links.py` | 각각 272문서·2151대상, 오류 0 |
| Windows·WSL 각각 `tools/validate_plan.py` | 각각 102 task, 오류 0 |
| Windows·WSL 각각 `tools/check_spdx.py` | 각각 20파일, 오류 0 |
| Windows·WSL 각각 `tools/check_versions.py --self-check` | 각각 exit 0 |
| `git diff --check 6e1881b86f017d604ccfa416bd368e5aba24c669 HEAD` | 출력 없음, exit 0 |
| 같은 독립 합성 CLI 32사례를 Windows·WSL에서 각각 실행 | 각 29사례는 기대 판정과 일치, 3사례는 잘못된 OK·exit 0. 결과 차이 없음 |
| 선언과 일치하는 `?rev=topic%40v1.2.3#<전체 SHA>` lock query 추가 대조 | 양 OS 모두 여전히 OK·fail exit 0 |
| WSL 실제 uv 0.11.21의 임시 Git branch/rev 대조 | `uv lock --offline` 성공, branch의 실제 SHA로 lock 생성, rev query 보존 |

양 플랫폼의 140 tests는 같은 시험 집합이며 280개 고유 시험으로 합산하지 않는다. WSL 실행은 `wsl.exe --exec bash -lc`로 `/mnt/f/dev/kor-travel-common-wt/review-t005a-post2-b`에 진입하고 `/home/digitie/.local/share/uv/python/cpython-3.11-linux-x86_64-gnu/bin/python3.11 -B -X utf8 ...`를 사용했다.

독립 32사례는 임시 `pyproject.toml`·`uv.lock`을 구성하고 `tools/check_versions.py <임시 입력> --repo weather --mode fail --no-step-summary --json <임시 보고>`를 subprocess로 호출했다. 합성 SHA는 `'a' * 40`, 두 번째 SHA는 `'b' * 40`으로 만들었다. 원문 URL·경로를 광범위하게 출력하지 않고 case·exit·판정만 출력했다.

| 직접 대조 묶음 | 양 플랫폼 결과 |
|---|---|
| `branch=main`, `branch=v1.2.3`, `branch=topic@v1.2.3`, `branch=topic%40v1.2.3` | 모두 FLOATING_REF·error annotation·exit 1 |
| `tag=v1.2.3`, `rev=<40자리 SHA>` | 모두 OK·exit 0 |
| `rev=main` | FLOATING_REF·exit 1 |
| `rev=topic@v1.2.3`, `rev=topic%40v1.2.3`, `tag=topic@v1.2.3` | 기대와 달리 OK·exit 0, error annotation 없음 |
| Git lock SHA 누락·7자리 SHA | FLOATING_REF·exit 1 |
| 서로 다른 marker의 정상/미고정 Git 항목 순서 교체 | 양 순서에서 OK·FLOATING_REF 각각 남고 exit 1 |
| 두 marker에 서로 다른 전체 SHA | SHA별 OK 두 행·exit 0 |
| URL 호스트 없음·잘못된 port, dependency name 누락·group 숫자 원소, marker 형식 오류, 미지원 revision·lock Python 누락 | 모두 입력 오류·exit 2 |
| group 이름 정규화 | 포함 대상 인식·exit 0 |
| 정규화 후 중복 group, include cycle·미지 키·존재하지 않는 group | 모두 입력 오류·exit 2 |
| manifest/lock Python 3.12/3.10 및 3.10/3.12 | 각각 낮은 쪽이 BELOW_FLOOR·exit 1 |
| manifest/lock Python 3.11/3.11 | OK·exit 0 |
| 미지원 `!=` lock Python 범위 | 입력 오류·exit 2 |
| lock 없음 | NO_LOCK·exit 1 |

## 원 finding disposition

### B-P1-01 — FIXED

원 심각도 P1 유지. 선언의 고정 여부와 lock SHA 확인이 결합되고 모든 동일 이름 Git lock 항목이 검사된다. 누락/짧은 SHA, marker 순서 양방향과 양성 대조를 양 플랫폼에서 다시 실행해 회귀 없음이 확인됐다.

### B-P1-02 — FIXED

원 심각도 P1 유지. `tools/check_versions.py:596`에서 명시적 branch 표식을 검사하여 `topic@v1.2.3`와 `%40`를 포함한 원 반례를 모두 차단한다. 정상 branch·버전처럼 생긴 branch도 차단하고 정상 tag·전체 SHA rev는 허용한다. 아래 신규 finding은 명시적 branch 필드가 아닌 rev/tag 값의 경계를 잃는 별도 공개 입력 경로다.

## B-P1-03 — rev/tag 값의 앞부분을 버려 이동 가능한 rev를 고정으로 판정

- 심각도: P1. Disposition: OPEN.
- 위치: `tools/check_versions.py:1032`·`:1033`의 문자열 결합, `:598`의 마지막 `@` 분리, `:775`의 선언 판정.
- 근거: 버전 정본 §3.8은 전체 SHA·버전형 태그만 고정 참조로 허용하고 branch·미고정 참조는 FLOATING_REF로 분류한다. `topic@v1.2.3` 전체는 이 허용 형식이 아니다. 명시적 rev도 ref 전체를 검사해야 한다.
- 최소 재현: `project.requires-python=">=3.12"`, `dependencies=["custom-lib"]`; `tool.uv.sources.custom-lib={git="https://github.com/example/custom-lib.git",rev="topic@v1.2.3"}`. uv lock version 1/revision 3에 해당 package의 source를 같은 URL의 `?rev=topic%40v1.2.3#<40자리 SHA>`로 기록한다.
- 실제 결과: Windows Python 3.14.3·WSL Python 3.11.15 모두 custom-lib OK, `--mode fail` exit 0, error annotation 없음. query가 선언과 일치하는 경우도 별도로 재현했다.
- 원인: 만들어진 `...git@topic@v1.2.3`에서 마지막 `@` 뒤의 `v1.2.3`만 검사한다. `rev=topic%40v1.2.3`도 URL 디코딩 후 동일하다. `tag=topic@v1.2.3` 역시 전체 tag 이름의 버전형 검사를 우회한다.
- 영향: rev가 가리키는 이동 가능한 branch를 정상 고정 참조로 보고해 fail gate를 통과시킨다. 이는 실제 lock 만족 여부를 검사하라는 요구가 아니라 현재 판정 대상인 ref 문자열 자체를 잘못 해석하는 결함이다.

유효성은 실제 uv로 확인했다. WSL 임시 Git 저장소에 정적 `custom-lib` 프로젝트를 만들고 commit 및 `topic@v1.2.3` branch를 생성했다. 임시 앱에서 `git=<임시 저장소 file URL>, rev="topic@v1.2.3"`를 지정하고 다음 명령을 실행했다.

```bash
uv lock --offline --no-python-downloads \
  --python /home/digitie/.local/share/uv/python/cpython-3.11-linux-x86_64-gnu/bin/python3.11 \
  --project <임시 앱>
```

설치된 `uv 0.11.21 (x86_64-unknown-linux-gnu)`에서 exit 0이며 lock이 생성됐다. source.git의 fragment가 생성한 branch의 실제 SHA와 같고 `rev=topic%40v1.2.3` query가 보존됨을 프로그램으로 확인했다. 이 실험은 rev의 Git 의미 검증이며 common checker가 file URL을 지원한다는 주장이 아니다. 네트워크를 사용하거나 패키지를 설치하지 않았다.

권고: `tool.uv.sources`의 원 ref 값 전체를 URL로 합치기 전에 판정하거나, 종류·원문 ref를 별도 값으로 보존한다. URL 문자열에서 마지막 `@` 뒤만 취하는 방식과 branch 문자열에 대한 특수 차단만으로 원 ref 의미를 대신하지 않는다. rev/tag의 `@`·`%40`, 정상 tag·전체 SHA를 함께 회귀 시험으로 고정한다.

## NOT_RUN·최종 경계

NOT_RUN: 이 candidate의 원격 CI 조회, 실제 소비자 `uv sync --locked`·설치·빌드·e2e·배포·registry 게시, 모든 upstream lock 형식 동등성 시험. 이전 airport 고정 입력·외부 원문 대조는 기록을 재사용했고 이번에는 소비자 Git object를 다시 읽지 않았다. 임시 Git/uv lock 의미 실험은 위와 같이 실제 실행했다.

양 플랫폼 회귀와 validator의 통과는 새 P1 반례를 상쇄하지 않는다. 후보·소비자 파일 및 타인의 결과를 변경하지 않았고 독립 원본을 확정했다. **BLOCK**: B-P1-03을 수정하고 새 immutable 후보에서 재확인해야 한다.
