# T-103 수정 후 독립 적대적 리뷰 A 원본 05

- 실행 ID: `A-T103-POST5-20260908-102711`.
- 시작: 2026-09-08 10:27:11.390 KST. 코드 검증 종료: 2026-09-08 10:30:27.319 KST.
- manifest: commit `93b9eb1dfac9a3f2629c04b87e4f3cdb29a59738`의 `docs/reviews/adversarial/evidence/2026-09-08-t103-post-fix-05-manifest.md`를 `git show`로만 읽었다.
- 실제 불변 후보 commit: `ecad460db93a9369d96435a28b6cb48dd7516ace`; tree: `6a903d346072ca951fe5146653addaa250fd44f5`. 대조 기준: `1625bf197486448f7dc6b7780a6c4f4c13b01368`.
- 격리: `F:/dev/kor-travel-common-wt/review-t103-post5-a` detached. 시작·코드 검증 종료 `git rev-parse HEAD HEAD^{tree}`는 위 값과 같고 `git status --porcelain=v1`은 두 번 모두 빈 출력이다. 검증 후 이 원본 한 파일만 추가해 별도 commit한다.
- 요청: A 잔여 selector·unsupported token selector·일반/computed tag·배열·삼항·fence·blockquote를 포함한 전체 코드/계약 회귀를 Windows 3.14와 WSL 3.11에서 독립 검증하고 원본을 반드시 commit하여 SHA256/verdict를 반환한다.
- 상대 결과와 이전 상대 raw는 읽지 않았다. 이번 검증은 자신의 외부 합성 helper를 새 후보에서 재생했고 이전 raw report를 읽지 않았다. 제품·소비자 파일, source `.git/config`는 변경하지 않았다. 소비자·registry·workflow dispatch·배포는 호출하지 않았다.

## 판정과 누적 disposition

**NO-GO**. 기존 15 ID 중 **FIXED 13 / OPEN 2**, 신규 ID는 없다. 미해결 집계는 **P0 0 / P1 1 / P2 1 / P3 0**이다. 직전 구체 반례는 수정됐으나 같은 parser 계약의 경계가 남아 있다.

| 원 ID·심각도 | disposition | 새 후보에서 실행한 검증 |
|---|---|---|
| A-P1-01 / P1 | OPEN, 일부 수정 | `.dark:root`·인용/공백 attribute 동치, specificity·media 교집합·중첩·문자열/주석은 수정. 미지원 selector의 내부 공백 우회와 대소문자 오해석이 남는다. |
| A-P1-02 / P1 | FIXED | OKLCH chroma 25%/0.1 세 채널 동일, 수학 회귀 통과. |
| A-P1-03 / P1 | FIXED | white 20%/black = 1.6620953314177012, `#333` 대조 동일. airport 현재 1.32/역사 1.15 구분 보존. |
| A-P1-04 / P1 | FIXED | 앞 삽입 신규 P6만 added=true·exempt=false·fail=true·exit 1. |
| A-P1-05 / P1 | FIXED | 외부 root의 서로 다른 동명 파일이 충돌하지 않고 위반 1건·exit 1; 외부 Git root 회귀 통과. |
| A-P2-06 / P2 | OPEN, 일부 수정 | 일반/computed tag·한 줄 배열/삼항·4자 fence/suffix·blockquote는 수정. 여러 줄 실행 문맥과 2자 inline code 구분이 남는다. |
| A-P2-07 / P2 | FIXED | `--base=--name-only` 양 OS generic exit 2. |
| A-P2-08 / P2 | FIXED | WSL tab 포함 tracked 파일의 신규 P6 탐지·exit 1. Windows tab 파일명은 NOT_RUN. |
| A-P2-09 / P2 | FIXED | Infinity/NaN/음수/bool/중복 및 400/5000자리 수치 경계 exit 2·traceback 없음. |
| A-P2-10 / P2 | FIXED | 색/var/경로/주소/만료 baseline marker 비공개 유지. 두 CLI `--json=<marker>`도 generic exit 2·marker 없음. |
| A-P2-11 / P2 | FIXED | 추가 muted 읽기 31쌍에서 tertiary/muted 미달 1건·exit 1. |
| A-P3-12 / P3 | FIXED | geo light 미달 8건·baseline 적용 exit 0과 evidence 일치. |
| A-P1-13 / P1 | FIXED | `++counter;` 뒤 신규 P6은 line 3·added=true·fail=true·exit 1. |
| A-P2-14 / P2 | FIXED | Windows/WSL 직접 self-symlink root 생성·검사에서 generic exit 2·traceback 없음. |
| A-P2-15 / P2 | FIXED | 2000중첩 JSON 배열은 두 CLI·양 OS 모두 generic exit 2·traceback 없음. |

## A-P1-01 잔여 — 공백으로 미지원 selector 오류 우회, 클래스 대소문자 변경

- 위치: `tools/kt_contrast.py:171`, `:308`.
- 최소 재현 1: `:root:where( .dark ){--kt-brand:#fff;--kt-brand-foreground:#fff}`를 임시 override에 쓰고 canonical 뒤에 전달한다.
- 명령: `python -B -X utf8 tools/kt_contrast.py packages/tokens/tokens.css <override.css> --dark --fail-new --json`.
- Windows/WSL 실제: **exit 0 / PASS / 27쌍 미달 0**. 괄호 안 공백만 제거한 `:root:where(.dark)`는 **exit 2**다. unsupported guard가 selector의 모든 공백을 하위 요소 선택자로 가정하여, 함수 내부 공백으로 generic 오류 경계를 우회한다.
- 최소 재현 2: 다음 override를 같은 명령으로 실행하면 양 OS **exit 0 / PASS / 27쌍 미달 0**이다.

```css
:root{--kt-brand:#fff;--kt-brand-foreground:#fff;--kt-brand-tint:#fff}
.DARK{--kt-brand:#000}
```

- 실제 CSS 대조: `<!doctype html>` 표준 모드 Chromium, dark OS, `html.dark`에서 두 반례의 foreground/background를 모두 `rgb(255, 255, 255)`로 직접 관찰했다. 실제 대비는 1:1이다. `.DARK`는 `.dark`와 다른 클래스인데 selector 전체를 `.lower()`하여 존재하지 않는 규칙을 적용한다. 초기 doctype 없는 브라우저 관찰은 quirks 모드이므로 이 판정에서 사용하지 않고 표준 모드로 다시 확인했다.
- 영향: 실제 전역 미달을 누락하거나 비활성 규칙으로 덮어 대비 gate를 우회한다.
- 수정 수용: selector의 문법적 공백과 하위 요소 combinator를 동일하게 처리하지 않는다. 지원 밖 전역 token selector를 공백 때문에 무시하지 말고 generic exit 2로 닫는다. 클래스·attribute 값 등 대소문자를 구별하는 부분을 보존하며, 지원하는 문법 토큰만 정규화한다. 위 두 반례가 실제 미달 또는 명시적 입력 오류가 돼야 한다.

## A-P2-06 잔여 — 줄바꿈으로 실행 template 누락, 다중 backtick 인용 오탐

- 위치: `tools/ux_lint.py:73`, `:87`.
- 최소 양성 반례: 별도 `.mdx` 파일에 다음 코드를 저장한다.

```tsx
export const X = () => (
  <div
    className={
      `outline-none`
    }
  />
);
```

- 명령: `python -B -X utf8 tools/ux_lint.py <fixture.mdx> --fail-new --json`.
- Windows/WSL 실제: **exit 0 / PASS / findings 0**. 한 줄의 같은 JSX는 P6을 탐지한다. `_is_executable_mdx_template()`가 현재 줄의 prefix만 보므로 이전 줄에서 열린 JSX expression을 잊는다. `export const classes =` 뒤 다음 줄에 template를 놓은 ESM 선언도 동일하게 0건이다.
- 음성 반례: `"Example: " + chr(96)*2 + " " + chr(96) + "outline-none" + chr(96) + " window.confirm() " + chr(96)*2 + "\n"`으로 2자 backtick code span을 작성하면 양 OS **exit 1 / P8 1건**이다. 실제로는 span 전체가 인용인데 첫 단일 backtick 종료 탐색으로 일부가 실행 코드로 남는다.
- 정상 대조: 한 줄 일반/computed tag 각 P6 1건, 배열·삼항 조합 P6 2건, 4자 fence·suffix fence·blockquote·tilde fence는 0건으로 수정 확인했다.
- 영향: 일반적인 JSX 줄바꿈만으로 금지 클래스가 누락되고 정상 문서의 code span은 실패한다.
- 수정 수용: 파일을 읽는 동안 여러 줄 ESM/JSX 문맥과 열린 expression을 보존한다. inline code opener의 backtick run 길이와 같은 길이의 closer를 사용하고, fence와 template의 상태를 구분한다. 동일 코드의 줄바꿈 전후 판정이 같고 인용은 0건이어야 한다.

## 실행한 검증과 한계

- Windows Python 3.14.3 전체: `python -B -X utf8 -m unittest discover -s tests -p 'test_*.py'` → **279 PASS / skip 0 / 73.590초**.
- WSL Python 3.11.15 전체: `uv run --no-project --with jsonschema --python 3.11 python -B -X utf8 -m unittest discover -s tests -p 'test_*.py'` → **279개 발견 / 278 PASS / Windows 전용 1 skip / 47.490초**. skip을 성공으로 세지 않았다.
- 집중: `python -B -X utf8 -m unittest tests.test_kt_contrast tests.test_ux_lint -v` → Windows **41 PASS / 11.420초**, WSL uv Python 3.11 동일 모듈 **41 PASS / 6.300초**. 둘 다 skip 0.
- 양 OS 정적 gate: `tools/validate_document_links.py` 문서 407·target 2412·오류 0; `tools/validate_plan.py` task 106·오류 0; `tools/check_spdx.py` 소스 56·오류 0; `tools/scan_secrets.py --all`·`tools/check_prod_redaction.py --all` 각각 539개·발견 0; `tools/check_versions.py --self-check` exit 0; `tools/check_aliases.py packages/tokens/aliases` CSS 1개·오류 0; `git diff --check 94ca2f1730b270721eb6242bfcdd9362b51d45e5 HEAD` exit 0.
- WSL 정적 gate에서만 process `GIT_DIR=/mnt/f/dev/kor-travel-common/.git/worktrees/review-t103-post5-a`, `GIT_WORK_TREE=/mnt/f/dev/kor-travel-common-wt/review-t103-post5-a`를 사용했다. source 설정 파일은 바꾸지 않았고 합성 Git probe·unittest에는 이 환경을 넘기지 않았다.
- 직접 CLI: canonical light/dark 각 27쌍 PASS, 추가 muted 31쌍 중 1건 미달·exit 1, 4앱 light 미달 4/8/8/4건 및 각 baseline 적용 exit 0. UX checked-in fixture 기본 report 12건·fail 0·exit 0은 위반 0으로 세지 않았다.
- 코드/문서 delta: 직전 후보와 현재의 두 도구·두 시험 전체 변경을 읽었다. airport task/evidence는 변경 없고 1.32 현재 수용 기준/1.15 역사 값 구분을 유지한다. 상대 raw와 역사 report의 내용은 읽지 않았다.
- 합성 helper: `python -B -X utf8 F:/dev/kor-travel-common/.git/codex-audit/t103-post5-reviewer-a-probe.py F:/dev/kor-travel-common-wt/review-t103-post5-a`; WSL은 경로를 `/mnt/f/...`로 바꾸고 uv Python 3.11로 실행했다. SHA256 `DBCC191FF20193DF2E8388D31E020809E92B7A031AEA61CA88FF4145E147AA15`. 자신의 이전 helper corpus를 호출하지만 raw report는 읽지 않으며 합성값 원문 대신 exit/건수/포함 여부만 출력한다.
- 브라우저: `node F:/dev/kor-travel-common/.git/codex-audit/t103-post5-reviewer-a-browser.cjs`, SHA256 `55686F7288CFD3A370D52FF15CAA062AC9E6F48DFAAC6F437B39EE6C1FAB9899`. Windows bundled Playwright의 표준 모드 headless Chromium에서 두 CSS 반례를 검증했다. 제품 의존성은 추가하지 않았다.
- 원격 읽기: `gh run list --commit ecad460db93a9369d96435a28b6cb48dd7516ace --json databaseId,headSha,status,conclusion,url --limit 5` → exact SHA [run 34176604888](https://github.com/digitie/kor-travel-common/actions/runs/34176604888)는 completed/cancelled였다. 다른 SHA의 성공을 이 후보의 직접 성공으로 기록하지 않았다.
- NOT_RUN: Windows Python 3.11(미설치), Windows tab 파일명, WSL 브라우저, MDX 소비자 build/e2e, exact code SHA의 성공 CI, 소비자·registry·배포·workflow dispatch·후행 T-010 workflow selftest.
- 이 원본 한 파일만 commit한다. 미해결 두 ID의 수정과 새 불변 후보의 독립 재검토 전에는 완료를 승인하지 않는다.
