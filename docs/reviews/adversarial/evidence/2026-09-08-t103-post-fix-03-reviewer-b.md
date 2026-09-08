# T-103 수정 후 독립 적대적 리뷰 B 원본 03

## 기준선과 격리

- 실행 ID: `T103-POST3-B-20260908-095327-KST`; reviewer `/root/reviewer_b`.
- 시작 KST: `2026-09-08T09:53:27.2535178+09:00`; 코드 검토 종료 KST: `2026-09-08T09:58:54.0932206+09:00`.
- manifest commit: `826f6107fbb3d6a45fce348ad19dc1b25c7cfde7`.
- manifest 경로: `docs/reviews/adversarial/evidence/2026-09-08-t103-post-fix-03-manifest.md`; Git blob SHA256 `9802f23fdf33094b1f5b174fcc2323f1af75e025356d2c4ac27a80f6d03ac4a8`.
- 실제 시작·종료 code SHA: `790bc3ec136b480c9cb95d796990ac1cbb07c596`.
- 실제 시작·종료 tree: `496e44bd27124255437ef265d29e29d680f29e94`.
- 새 detached worktree: `F:/dev/kor-travel-common-wt/review-t103-post3-b`. 시작·종료 `git status --short` 출력 없음. 코드 검토 종료 뒤 `codex/review-t103-post3-b` branch에서 이 원본 한 파일만 기록한다.
- source `.git/config` 시작·종료 SHA256: `0A0F849E7874CF0A25926856F9D2E381CCBF4C2DCB5999869C57B86E0F5BEB5B` 동일. source 파일·제품·`.git/config`를 수정하지 않았다.
- 비교: `f966607..790bc3e`의 누적 제품/시험/문서 delta와 `01c3c3f..790bc3e`의 추가 수정을 읽었다. 이전 post-fix raw와 상대 reviewer 결과는 열람하지 않았다. 파일 목록에 나타난 원본 report 이름을 본 것은 그 내용을 읽은 것이 아니다.
- post-fix-02는 사용자 요청으로 중단됐고 B raw가 없다. 그 후보의 실행 결과·판정을 이번 evidence로 재사용하지 않았다. 아래 시험은 이번 code SHA에서 새로 실행했다.
- 전체 시험·정적 gate는 후보를 별도 임시 디렉터리로 복사한 새 Git 저장소에서 실행했다. 자식 프로세스의 `GIT_*` 환경을 제거했다. 직접 반례도 임시 파일/저장소만 생성했다.

## 전달 요청 원문

> post-fix-03 독립 적대 리뷰를 시작하세요. 제품 코드 불변 후보는 `790bc3ec136b480c9cb95d796990ac1cbb07c596`, tree `496e44bd27124255437ef265d29e29d680f29e94`입니다. 기준선 manifest는 `826f6107fbb3d6a45fce348ad19dc1b25c7cfde7`의 `docs/reviews/adversarial/evidence/2026-09-08-t103-post-fix-03-manifest.md`를 git show로 읽으세요. post-fix-02는 중단되어 raw report가 없으므로 이를 새 결과로 대체합니다. CSS specificity/source order와 not/compound media, nested/string/comment lexer, MDX inline/fenced/executable template·interpolation comments, diff +++, huge JSON/symlink/error redaction, airport task/evidence를 Windows/WSL에서 공격하세요. 제품·소비자·registry·workflow는 수정/호출하지 말고 새 raw 파일 `docs/reviews/adversarial/evidence/2026-09-08-t103-post-fix-03-reviewer-b.md` 하나만 추가해 별도 commit, SHA256·verdict를 보내세요.

manifest의 검증 명령에 따라 제품 도구를 테스트했다. 제품 파일은 변경하지 않았고 소비자·registry·workflow dispatch는 호출하지 않았다.

## 최종 판정

**NO-GO — 현재 OPEN은 P1 3건(B-P1-03·B-P1-04·B-P1-09), P0/P2/P3 0건.** 누적 B finding 10건 중 7건은 이번 후보에서 FIXED로 재판정한다. 나머지 3건은 원 ID·심각도를 유지한다. 기존 최소 반례가 일부 수정됐어도 같은 계약의 잔여 반례가 재현되어 전체를 FIXED로 올리지 않았다. 별도 신규 ID는 부여하지 않았다.

| 원 ID | disposition | 이번 후보의 양 OS 검증 |
|---|---|---|
| B-P1-01 | FIXED | common CWD/앱 CWD에서 대상 Git root를 사용, 같은 신규 P6 1건·exit 1 |
| B-P1-02 | FIXED | 기존 count 1 앞에 신규 P6 삽입 시 신규 행 fail·기존 행 exempt·exit 1 |
| B-P1-03 | OPEN | 일반 TSX/MDX 실행 template와 단순 보간 주석은 수정. tagged template·colon/fenced 문서는 잔여 |
| B-P1-04 | OPEN | CSS 읽기/var/표면 오류와 경로 JSON/Markdown/summary는 수정. argparse 오류값 echo는 잔여 |
| B-P2-05 | FIXED | muted 선언 시 중복 없이 31쌍, primary/muted 1:1 실패·exit 1 |
| B-P2-06 | FIXED | 1e309·bool·fraction·version/NaN 및 5,000자리 정수·2,000중첩 JSON 모두 입력 오류 exit 2·traceback 없음 |
| B-P3-07 | FIXED | geo 예제 8건 미달과 evidence 일치 |
| B-P1-08 | FIXED | `++counter; window.confirm(...)` 추가 행의 P8을 탐지, added=true·exit 1 |
| B-P1-09 | OPEN | 단순 media의 공백 동등성과 not/compound 거절은 수정. 배타적인 중첩 media는 잔여 |
| B-P2-10 | FIXED | airport 수용 기준·evidence가 현재 1.320934 계산과 역사 1.15를 분리 |

## 실행한 검증과 수치

Windows Python `3.14.3`, WSL Python `3.14.4`. 전체 suite와 gate는 `.git/codex-audit/review-t102-b-wsl-unittest.py`, `review-t102-post-b-gates.py`의 사본 실행을 사용했다. helper 이름과 무관하게 입력은 위 post-fix-03 worktree였다.

```text
python -B -X utf8 -m unittest discover -s tests -p test_*.py
python -B -X utf8 -m unittest tests.test_kt_contrast tests.test_ux_lint -v
python -B -X utf8 tools/validate_document_links.py
python -B -X utf8 tools/validate_plan.py
python -B -X utf8 tools/check_spdx.py
python -B -X utf8 tools/scan_secrets.py --all
python -B -X utf8 tools/check_prod_redaction.py --all
python -B -X utf8 tools/check_versions.py --self-check
python -B -X utf8 tools/check_aliases.py packages/tokens/aliases
python -B -X utf8 -m unittest discover -s tests -p test_check_aliases.py
python -B -X utf8 tools/kt_contrast.py packages/tokens/tokens.css --json
python -B -X utf8 tools/ux_lint.py --root tests/fixtures/ux --json
git diff --check 94ca2f1730b270721eb6242bfcdd9362b51d45e5 790bc3ec136b480c9cb95d796990ac1cbb07c596
```

| 검증 | Windows | WSL |
|---|---|---|
| 전체 unittest | 268개 통과, skip 0, 81.399초 | 267개 통과·Windows 8.3 전용 1개 skip, 27.407초 |
| T-103 focused | 30개 통과·skip 0, 7.365초 | 30개 통과·skip 0, 4.276초 |
| links | 401문서·2,412대상·오류 0 | 동일 |
| plan | 106 task·오류 0 | 동일 |
| SPDX | 56파일·오류 0 | 동일 |
| secret·운영값 각각 | 533파일·발견 0·예외 0 | 동일 |
| versions 자체 검사 | exit 0, 소비자 검사는 아님 | 동일 |
| aliases | CSS 1개·오류 0 | 동일 |
| aliases focused | 35개 통과 | 34개 통과·Windows 전용 1개 skip |
| canonical light/dark CLI | 각각 27/27·exit 0 | 동일 |
| UX fixture report CLI | finding 12·exit 0 | 동일 |
| 4앱 example baseline + fail-new | 모두 exit 0 | 동일 |
| 후보 diff check | exit 0 | 별도 명령 NOT_RUN; 같은 object diff의 Windows 결과만 사용 |

4앱 light 미달은 docker-manager 4·concierge 8·geo 8·airport 4다. airport `control-line/surface-page`는 양 OS에서 `1.3209340364487114`로 task와 evidence에 적힌 현재 기준에 부합한다. 역사 조사 값을 덮어쓰지 않았다.

직접 반례는 `.git/codex-audit/`의 `t103-post1-b-originals.py`, `t103-b-edge.py`, `t103-post1-b-new.py`, `t103-post1-b-media.py`, `t103-post3-b-new.py`, `t103-post3-b-smoke.py`를 이번 후보 경로로 양 OS에서 실행했다. helper는 결과 report commit에 포함하지 않는다. 합성 marker는 `'gh' + 'p_' + 'Z' * 36`으로 생성하고 출력 포함 여부만 boolean으로 관찰했다.

추가 정상/음성 대조: 높은 specificity `:root:root`가 뒤의 `:root`보다 우선했고 같은 specificity는 뒤 선언이 우선했다. CSS 문자열 속 주석/위조 선언은 값에 영향을 주지 않았다. 닫히지 않은 주석, 중첩 selector 블록, 지원하지 않는 not/compound media는 exit 2였다. 임시 self-symlink root도 양 OS에서 exit 2·traceback 없음이었다.

## OPEN B-P1-03 — MDX 문서와 실행 tagged template의 구분 실패

- 위치: `tools/ux_lint.py:66-88`, `:144-201`.
- 최소 실행 반례: `Page.mdx`에 다음을 쓰고 `ux_lint.py Page.mdx --fail-new --json`을 실행한다.

```tsx
export const Widget = () => <div className={String.raw`outline-none`}/>;
```

- 양 OS 결과: finding 0·PASS·exit 0. 바로 앞 문자가 `w`여서 executable 분기에서 제외된다. 일반 JSX의 template class는 탐지하지만, 실제 class 문자열을 만드는 표준 JavaScript tagged template는 문서 인용처럼 마스킹한다.
- 반대 방향 반례: MDX 본문의 ``문서 예시: `outline-none` ``은 P6 1건·FAIL·exit 1이다. 콜론을 JSX/JS 실행의 충분조건으로 오인한다. 콜론 없는 일반 inline code span은 정상 제외된다.
- fenced 반례: 아래 전체는 문서 코드 블록인데 P6 1건·exit 1이다. backtick fence 안의 template backtick에서 문서 범위가 깨진다.

````mdx
```tsx
export const Widget = () => <div className={`outline-none`}/>;
```
````

- tilde fence(`~~~tsx`, `window.confirm("doc");`, `~~~`)도 P8 1건·exit 1이었다. 단순 backtick fence에 template가 없는 대조 입력은 제외된다.
- 영향: 실제 실행 금지 패턴의 false PASS와 정상 문서의 false FAIL이 함께 남는다. MDX/문서 code span·fence와 JSX/ESM 실행 영역은 단일 앞 문자 heuristic으로 구분할 수 없다.
- 권고: 먼저 Markdown inline/fenced 영역을 안정적으로 분리하고 JSX/ESM 영역 안에서 template·tagged template·중첩 보간을 추적한다. 위 네 반례와 기존 보간 주석 음성을 모두 회귀에 둔다.

## OPEN B-P1-04 — argparse가 합성 입력값을 stderr에 재출력

- 위치: `tools/ux_lint.py:459-473`, `tools/kt_contrast.py:615-635`.
- 최소 반례: 위 분할식으로 marker를 만들고 각 CLI에 단일 인자 `--json=<marker>`를 넘긴다. UX에는 임시 root도 전달한다. stdout/stderr를 캡처해 marker 포함 여부만 검사한다.
- 양 OS 결과: 두 도구 모두 exit 2·traceback 없음이지만 stderr marker 포함은 `true`다. 기본 argparse가 값 없는 flag에 전달된 값을 진단에 echo한다.
- 원인: 개별 CSS/JSON/표면 오류는 generic으로 수정됐지만 `parse_args()` 자체의 출력 경로는 그대로다.
- 영향: 입력 오류에 있던 자격증명 형태 값이 CI 로그에 복제되는 원 finding이 완전히 닫히지 않았다.
- 권고: 각 입력 분기를 개별 예외 처리하는 데 그치지 말고 두 CLI의 argparse 오류 메시지까지 원문 없는 진단으로 통일한다. unknown option·flag에 잘못된 값·인자 누락 등 공통 경로를 같은 캡처 검사로 검증한다.

## OPEN B-P1-09 — 배타적인 중첩 media가 미달을 통과로 바꿈

- 위치: `tools/kt_contrast.py:247-254`.
- 최소 반례: canonical 뒤에 아래 override를 넣고 `kt_contrast.py <canonical> <override> --dark --fail-new --json`을 실행한다.

```css
.dark { --kt-control-line:#000; }
@media (prefers-color-scheme: light) {
  @media (prefers-color-scheme: dark) {
    :root { --kt-control-line:#fff; }
  }
}
```

- 양 OS 결과: 27/27 PASS·exit 0. control/page는 흰색을 사용해 `18.442`로 계산된다. 중첩 media를 제거한 대조는 control 4쌍 모두 FAIL·exit 1, control/page `1.139`다.
- 원인: 재귀 호출이 상위 `parent_mode`와 하위 조건을 함께 평가하지 않고 하위 모드로 덮어쓴다. 같은 시점에 light와 dark를 모두 만족할 수 없으므로 내부 선언은 적용될 수 없지만 검사기는 유효한 dark 선언으로 승격한다.
- 영향: CSS specificity/source order 자체의 수정과 별개로, 실행 불가능한 조건 안의 값을 사용해 실제 활성 dark 미달을 PASS로 바꿀 수 있다.
- 권고: 중첩 조건은 상위/하위의 교집합으로 처리하거나 지원 밖 중첩 media를 입력 오류로 거절한다. 상충 조건·동일 조건·단계별 중첩과 selector specificity/source order를 함께 검증한다.

## 범위와 미실행

- T-103 상세 task·task 원장·resume은 IN_PROGRESS다. 후행 T-010 workflow selftest를 실행 완료로 올리지 않았다. GPL-3.0-or-later·stdlib 경계와 실제 소비자 비수정 범위는 유지된다.
- `NOT_RUN(소비자 저장소 build/e2e·실제 앱 baseline 등록·npm/PyPI registry·게시·workflow dispatch)`: 명시 금지 또는 소비자/후행 task 범위.
- `NOT_RUN(exact candidate 원격 CI 독립 조회)`: 이 원본의 로컬 결과를 CI 성공으로 간주하지 않는다.
- `NOT_RUN(브라우저·MDX 컴파일·screenshot 실측)`: 해당 구문을 입력으로 준 CLI 결과와 소스의 분기/조건을 대조했다. 브라우저나 실제 앱에서 렌더링했다고 주장하지 않는다.
- 중단된 post-fix-02 결과와 이전 raw를 재사용하지 않았다. 상대 결과를 읽지 않고 독립 판정을 확정했다. 세 OPEN finding을 수정한 새 immutable 후보에서 재검토가 필요하다.
