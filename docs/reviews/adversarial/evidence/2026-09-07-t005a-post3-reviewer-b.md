# T-005a post3 독립 리뷰 B 원본

- 실행 ID: `B-T005A-POST3-20260907-124239-3c5801f`
- 최종 판정: **PASS**. `B-P1-01`·`B-P1-02`·`B-P1-03` 모두 FIXED. 새 finding 없음.
- 시작: 2026-09-07T12:42:39.7713799+09:00. 종료 SHA·clean 확인: 2026-09-07T12:44:32.5453840+09:00.
- candidate: `3c5801f14855a067080f257ec83d2279de32c74a`. 실제 시작·종료 HEAD가 모두 일치한다.
- base: `6e1881b86f017d604ccfa416bd368e5aba24c669`. 이번 delta 기준: `735efed760d2703b3f5769e58270954352566f39`.
- candidate tree: `35a49c903ef02396241d988f8771f71395135b01`.
- 새 detached worktree: `F:/dev/kor-travel-common-wt/review-t005a-post3-b`. 직접 `git worktree add --detach`로 생성했다. 시작·종료 `git status --porcelain=v1` 출력은 비어 있었다.
- 후보·과거 원본·소비자를 수정하지 않았다. 합성 입력만 임시 디렉터리에서 생성·정리했다. 원본 보고서는 지정 `.git/codex-audit` 한 파일에만 작성한다.
- 이전 B 원본·post2 BLOCK을 확인했다. A 결과나 다른 reviewer의 결과를 읽거나 요청·공유하지 않았다.

## 전달 요청 원문

> post3 독립 리뷰를 새 후보에서 진행해 주세요. immutable candidate `3c5801f14855a067080f257ec83d2279de32c74a`, base `6e1881b86f017d604ccfa416bd368e5aba24c669`, detached worktree `F:/dev/kor-travel-common-wt/review-t005a-post3-b`. 이전 B 원본·post2 BLOCK과 이번 3줄 수정만 읽고 A 결과는 읽거나 공유하지 마세요. B-P1-03 rev/tag/topic@ 우회와 branch/%40, tag/rev/normal semantics, 모든 lock SHA/marker, versions 정본, 전체 140 테스트/validators를 Windows/WSL에서 재현하세요. 결과는 `.git/codex-audit/2026-09-07-t005a-post3-reviewer-b.md`에 원본으로 보존하고 정확한 SHA/clean·finding disposition·PASS/BLOCK·NOT_RUN을 보고하세요. 수정은 하지 마세요.

## 검토 범위와 재사용

이번 delta는 `tools/check_versions.py` 3행과 `tests/test_check_versions.py` 회귀 6행, 총 2파일·9행 추가다. 코드와 시험 delta를 전부 읽었다. 변경은 Python Git 선언 URL의 디코딩된 path에 `@`가 정확히 하나일 때만 ref 고정 판정을 계속하도록 제한한다.

`AGENTS.md`, `docs/README.md`, `docs/resume.md`, `versions.json`, 버전 정본, T-005a 상세 task가 post2와 동일함을 `git diff --quiet`로 확인했다. 해당 읽기·정합 대조와 초기 전체 범위의 검토는 앞 B 원본에서 재사용한다. 현재 Python floor 3.11과 알려진 uv lock 형식의 판정 계약은 변경되지 않았다. 반복해서 다른 reviewer 원본이나 변경 없는 조사 문서를 읽지 않았다.

## 실제 검증

| 명령·검사 | 실제 결과 |
|---|---|
| Windows `py -3.14 -B -X utf8 -m unittest discover -s tests -p 'test_*.py'` | Python 3.14.3, 140 tests, 30.819초, OK, skip 0 |
| WSL Python 3.11.15의 같은 unittest 명령 | 140 tests, 14.819초, OK, skip 0 |
| Windows·WSL 각각 `tools/validate_document_links.py` | 각각 272문서·2151대상, 오류 0 |
| Windows·WSL 각각 `tools/validate_plan.py` | 각각 102 task, 오류 0 |
| Windows·WSL 각각 `tools/check_spdx.py` | 각각 20파일, 오류 0 |
| Windows·WSL 각각 `tools/check_versions.py --self-check` | 각각 exit 0 |
| `git diff --check 6e1881b86f017d604ccfa416bd368e5aba24c669 HEAD` | 출력 없음, exit 0 |
| post2와 동일한 독립 합성 CLI 32사례를 양 플랫폼에서 각각 재실행 | 각각 32/32 기대 판정 일치, 불일치 0 |
| Windows에서 추가 `ref_is_pinned` 경계 4개 | SSH authority의 사용자 `@`, subdirectory fragment의 `@`, `py-v0.1.0` 태그 허용; 이중 인코딩된 ref `@`는 차단 |

WSL은 `wsl.exe --exec bash -lc`로 `/mnt/f/dev/kor-travel-common-wt/review-t005a-post3-b`에 진입하고 `/home/digitie/.local/share/uv/python/cpython-3.11-linux-x86_64-gnu/bin/python3.11 -B -X utf8 ...`를 실행했다. Windows·WSL의 140 tests는 동일한 집합이므로 280개 고유 시험으로 합산하지 않는다.

32개 독립 사례는 후보의 함수를 단순 모사하지 않고 임시 `pyproject.toml`·`uv.lock`을 생성해 실제 CLI `tools/check_versions.py <임시 입력> --repo weather --mode fail --no-step-summary --json <임시 보고>`를 호출했다. 이전 실패 사례의 기대값을 바꾸지 않았다.

- 명시 branch `main`·`v1.2.3`·`topic@v1.2.3`·`topic%40v1.2.3`: 모두 FLOATING_REF·error annotation·exit 1.
- `rev=topic@v1.2.3`, `rev=topic%40v1.2.3`, `tag=topic@v1.2.3`: 모두 FLOATING_REF·error annotation·exit 1. post2의 잘못된 OK 3건이 해소됐다.
- 정상 `tag=v1.2.3`·40자리 SHA rev는 OK·exit 0이며 `rev=main`은 차단한다.
- lock SHA 누락·7자리 SHA와 marker별 정상/미고정 항목의 두 순서는 모두 차단한다. 서로 다른 전체 SHA를 가진 두 marker는 각각 OK로 보고한다.
- URL 호스트 없음·잘못된 port, dependency/group 원소 구조 오류, marker 형식·미지원 revision·lock Python 누락은 입력 오류 exit 2다.
- group 이름 정규화는 허용하고 정규화 중복·cycle·미지 include 키·누락 include 대상은 exit 2다.
- manifest와 lock의 Python 하한은 양방향으로 독립 대조하며 3.10은 BELOW_FLOOR, 3.11은 OK다. 미지원 `!=` 범위는 입력 오류, lock 부재는 NO_LOCK이다.

## Finding disposition

| 원 ID·심각도 | Disposition | 직접 재검토 근거 |
|---|---|---|
| B-P1-01 / P1 | FIXED | 모든 Git lock SHA·marker 순서 반례를 양 플랫폼에서 재현했다. 누락·짧은 SHA가 정상 선언에 가려지지 않는다. |
| B-P1-02 / P1 | FIXED | 명시적 branch의 버전 모양·`@`·`%40` 반례를 양 플랫폼에서 모두 차단한다. |
| B-P1-03 / P1 | FIXED | URL path를 디코딩한 뒤 ref 구분자가 중복되면 종료하므로 rev/tag의 앞부분을 버리고 마지막 버전 조각만 허용하던 반례가 차단된다. 실제 source 필드로 주입했고 정상 tag·전체 SHA와 함께 검증했다. |

새 finding은 없다. 위 PASS는 검토한 immutable candidate의 코드·규약 및 실행 검증 범위에 대한 판정이다.

## NOT_RUN과 경계

NOT_RUN: 후보의 원격 CI 조회, 실제 소비자 `uv sync --locked`·설치·빌드·e2e·배포·registry 게시, 모든 Git URL·upstream lock 형식의 동등성 시험. 이전 airport 고정 입력 및 post2의 실제 uv 0.11.21 임시 branch/rev 의미 실험은 기록을 재사용했고 이번에는 재실행하지 않았다. 양 플랫폼 전체 시험·validator·32사례는 이번 후보에서 직접 실행했다.

다른 reviewer 결과를 보지 않은 상태로 이 원본을 확정했다. 후보·소비자 원본 및 과거 evidence를 변경하지 않았다. **PASS**.
