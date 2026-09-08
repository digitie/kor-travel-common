# T-103 수정 후 31 A 독립 리뷰 원본

- 실행 ID: `T103-POST31-A-20260908-170418-KST`
- 최종 판정: **NO-GO**. 새 finding P0 0건, P1 0건, P2 1건, P3 0건.
- 후보 commit: `b2fc22b352a1122f465852737f6f0ae7a228ddae`
- 후보 tree: `be501ae5592c6c20edc235cc6f3516f8817ce9ac`
- 수정 비교 기준: `620e477bf841f881e6090cccefcbad81cfffe6e7`
- manifest: commit `910599e`의 `2026-09-08-t103-post-fix-31-manifest.md`를 `git show`로 확인했다.
- 격리: `review-t103-post31-a` detached worktree. 시작과 제품 검토 종료의 HEAD/tree는 위 후보와 동일하며 `git status --short`는 모두 빈 출력이었다.
- 시작: 2026-09-08 17:04:18.162 KST. 제품 검토 종료: 2026-09-08 17:11:35.157 KST.
- 상대 reviewer 원본은 열람하지 않았다. 후보·manifest·소비자·기존 evidence·Git 설정은 수정하지 않았다. 이 보고서만 별도 커밋한다.

## 새 finding

**A-P2-27 / P2 / OPEN · FIX_REQUIRED — 정상 inline span 안의 짧은 marker 행에서 CLI가 비정상 종료된다.**

- 위치: `tools/ux_lint.py` 478~479행, 502~504행.
- 재현 요약: 정상 닫힌 3자 또는 4자 backtick inline span 안에 독립된 1자 또는 2자 backtick/tilde 행을 넣고 MDX 파일을 `ux_lint.py --root <임시 fixture> --fail-new --json`으로 검사한다. 잘못된 fence info가 일반 inline span으로 해석되는 입력이다.
- 기대: 인용된 코드가 검사 대상에서 제외되고 exit 0과 빈 finding JSON을 반환한다.
- 실제: `_markdown_fence_start_at_line`의 짧은 marker 분기가 `None` 대신 `False`를 반환한다. 호출자는 이를 튜플로 취급하여 `TypeError: 'bool' object is not subscriptable`이 발생한다. exit 1, traceback 발생, JSON 미출력이다.
- 직접 대조: 각 OS에서 108개 입력을 실행했다. plain/blockquote/nested, 3·4자 run, LF/CRLF/CR, 짧은 marker 4종 조합의 72개 모두 같은 오류였다. 일반 텍스트 행 2종의 36개 음성 대조는 정상 통과했다.
- 영향: 유효한 문서에서 검사 명령과 JSON 소비 계약이 깨진다. 정상 성공으로 누락되는 사례는 아니므로 P2로 분류했다.
- 최소 수정·수용 기준: fence가 없는 반환값을 `None`으로 통일하고, 짧은 marker 행을 포함한 정상 span 대조가 양 OS에서 exit 0·빈 JSON finding·traceback 없음으로 통과해야 한다. 예외를 단순히 입력 오류로 바꾸는 것으로는 정상 입력 수용 기준을 만족하지 않는다.

## 기존 finding 상태

| ID | 원 심각도 | 이번 상태 |
|---|---|---|
| A-P1-01, A-P1-02, A-P1-03, A-P1-04, A-P1-05 | P1 | FIXED 유지: CSS·수학·baseline·Git root 누적 반례 재실행 |
| A-P2-06, A-P2-07, A-P2-08, A-P2-09, A-P2-10, A-P2-11 | P2 | FIXED 유지: 기존 MDX·옵션·경로·JSON·출력·대비 반례 재실행. 새 반환형 오류는 A-P2-27로 분리 |
| A-P3-12 | P3 | FIXED 유지: geo/airport 문서·현재 측정값 경계 확인 |
| A-P1-13, A-P1-16 | P1 | FIXED 유지: diff 구분자 및 CR/LS/PS·가짜 hunk mapping 대조 |
| A-P2-14, A-P2-15, A-P2-19, A-P2-22, A-P2-24 | P2 | FIXED 유지: symlink·깊은 JSON·들여쓰기·container·정상 inline span 대조 |
| A-P1-20, A-P1-21, A-P1-23, A-P1-25 | P1 | FIXED 유지: info string·container 종료·marker 공백/tab·다른 container 대조 |
| A-P1-26 | P1 | FIXED: 중간 tilde/더 긴 backtick fence 72개 대조와 `--base` P6/P8 및 음성 대조 3개가 양 OS에서 기대 결과와 일치 |

## 실제 검증과 한계

- Windows Python 3.14.3: 전체 unittest 304개 통과, skip 0, 200.342초. focused 66개 통과, 68.765초.
- WSL Python 3.11.15: 전체 304개 중 303개 통과, Windows 전용 8.3 API 시험 1개 skip, 77.961초. focused 66개 통과, 26.858초. skip은 통과로 집계하지 않았다.
- 양 OS에서 링크 484문서/2481대상, plan 106 task, SPDX 56파일, 비밀·redaction 각 616파일, registry 자체 검사, alias CSS 1개, 대비 27쌍, UX 예시 12 finding/report 모드 fail 0, 후보 delta의 `git diff --check`가 통과했다.
- 누적 독립 probe 18종을 양 OS에서 재실행했다. CSS·JSON·출력·diff 및 개행 probe 결과는 이전 자기 실행과 동일했다. 4열 indented-code 해석 차이를 가진 기존 참고 입력 3개는 기대값 확정 불가로 성공 집계에서 제외했다. 새 108개 입력의 오류는 위 A-P2-27로 별도 기록했다.
- 정확한 후보의 CI run `34202002476`은 `gh run list --commit`으로 head SHA 일치와 completed/success를 읽기 전용 확인했다. 개별 job 로그 감사는 NOT_RUN이다.
- Windows Python 3.11, 실제 소비자 빌드·e2e·manifest 검증, 실제 MDX compiler/browser 실행, npm/PyPI 설치·게시, workflow dispatch는 NOT_RUN이다. 로컬 시험이나 CI 상태를 이 검증들의 성공으로 대체하지 않는다.
- 보고서 자체 SHA-256과 보고서 전용 commit은 저장 후 계산하여 완료 메시지에 기록한다.
