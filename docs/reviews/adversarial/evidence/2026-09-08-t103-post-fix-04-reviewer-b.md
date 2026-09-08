# T-103 post-fix-04 독립 적대적 리뷰 B 원본

- 실행 ID: `T103-POST4-B-20260908T100728-KST`
- 판정: **NO-GO**. 기존 `B-P1-03`이 미해결이다. P0 0건, P1 1건, 별도 신규 P2/P3 0건이다. 아래의 실행 template 누락과 fence 오탐은 동일한 MDX 실행/인용 구분 계약의 잔여 반례다.
- 검토 시작: `2026-09-08T10:07:28.9705497+09:00`; 제품 검증 종료: `2026-09-08T10:15:50.7681649+09:00`.
- 시작·종료 제품 commit: `1625bf197486448f7dc6b7780a6c4f4c13b01368`.
- 시작·종료 제품 tree: `ee0626eb05e3e8dff3238f0de9ca71c3c2840563`.
- 시작·종료 `git status --porcelain=v1`: 모두 빈 출력, clean. 검증 종료 후 이 원본 하나만 추가하는 별도 branch `codex/review-t103-post4-b`를 만들었다. 보고서 commit은 제품 검증 SHA와 구분한다.
- 격리: `F:/dev/kor-travel-common-wt/review-t103-post4-b`의 detached 후보. 전체 회귀·정적 gate는 후보를 임시 독립 Git 저장소로 복사하고 `GIT_*` 환경을 제거한 뒤 실행했다. 직접 CLI 반례는 별도 임시 입력에만 썼다. 제품 파일·소비자·원본 checkout 설정은 수정하지 않았다.
- source `.git/config` 시작·종료 SHA256 동일: `0A0F849E7874CF0A25926856F9D2E381CCBF4C2DCB5999869C57B86E0F5BEB5B`.
- manifest: commit `8152395679290359c8ca6af2c3bb47903f07b4db`의 `docs/reviews/adversarial/evidence/2026-09-08-t103-post-fix-04-manifest.md`를 `git show`로 읽었다. Git blob SHA256: `cb7e241df7cb662e5a51c600dc8321e6038f69e71f5d3cc0e7b7671b8b84f860`.
- 상대 결과와 이전 post-fix-03 A/B raw는 읽지 않았다. 7파일 delta의 경로를 확인하고 제품 도구 2개·시험 2개를 직접 검토했다. 이전 raw 2개는 비공개 범위로 본문 검토에서 제외했다. 누적 반례는 이번 후보에서 재실행했다.

## 전달 요청 원문과 실행 환경 변경

> post-fix-04 독립 적대 리뷰를 진행하세요. 불변 제품 코드 후보는 `1625bf197486448f7dc6b7780a6c4f4c13b01368`, tree `ee0626eb05e3e8dff3238f0de9ca71c3c2840563`입니다. 기준선 manifest는 commit `8152395679290359c8ca6af2c3bb47903f07b4db`의 `docs/reviews/adversarial/evidence/2026-09-08-t103-post-fix-04-manifest.md`를 git show로 읽으세요. post-fix-03 A/B raw는 상대 결과 비공개 원칙으로 읽지 마세요. CSS 조건 교집합·root.dark·specificity, 깊은 JSON/argparse redaction, MDX tagged/colon/backtick·tilde fence·escaped interpolation, diff +++, symlink·airport 기준을 Windows/WSL Python3.11에서 공격하세요. 제품·소비자·registry·workflow는 수정/호출하지 말고 새 raw 파일 `docs/reviews/adversarial/evidence/2026-09-08-t103-post-fix-04-reviewer-b.md` 하나만 추가해 별도 commit 후 SHA256·verdict를 보내세요.

> Windows Python 3.11은 현재 호스트에 없습니다(py -0p는 3.14/3.10, bundled 3.12). post-fix-04 검증은 Windows 3.14와 WSL uv Python 3.11로 진행하고, Windows 3.11은 NOT_RUN으로 원본 보고서에 기록해 주세요. 최종 raw report를 commit하고 SHA/SHA256/verdict를 보내 주세요.

Windows는 `py -3.14`의 Python **3.14.3**, WSL은 `/home/digitie/.local/share/uv/python/cpython-3.11-linux-x86_64-gnu/bin/python3.11`의 **3.11.15**를 직접 확인했다. WSL 실행 파일은 `uv --offline python find 3.11`로 찾았다. 패키지 설치·registry 조회는 하지 않았다.

## 누적 finding 재판정

| ID / 원 심각도 | disposition | 이번 후보의 직접 관찰 |
|---|---|---|
| B-P1-01 / P1 | FIXED | CWD와 다른 `--root`의 Git 저장소에서 추가 행을 판정한다. 외부 root 반례가 exit 1이다. |
| B-P1-02 / P1 | FIXED | 앞에 새 위반을 삽입해도 과거 baseline 건수를 소비하지 않는다. 새 1행은 fail, 이동한 기존 3행만 exempt다. |
| B-P1-03 / P1 | **OPEN** | 직접 template·`String.raw`·colon 예시·기본 backtick/tilde fence·escaped 보간 반례는 수정됐다. 그러나 아래 배열/삼항식/임의 tag 실행 template 3종은 PASS 0건이고 잘못 닫힌 fence 2종은 오탐이다. |
| B-P1-04 / P1 | FIXED | CSS 값·누락 파일·var 참조·baseline 경로·잘못된 옵션/`--json=`은 exit 2, generic 오류, traceback/합성 marker 없음. JSON·Markdown·step summary의 경로도 marker를 노출하지 않았다. |
| B-P2-05 / P2 | FIXED | `--read-surface muted`로 기본 27쌍에 text 4쌍을 더한 31쌍을 검사한다. 1:1 반례는 fail이며 옵션 반복이 쌍을 중복하지 않는다. |
| B-P2-06 / P2 | FIXED | 잘못된 버전·bool/소수/무한대 count, 5,000자리 정수, 깊이 2,000 JSON은 양 OS exit 2·traceback 없음이다. |
| B-P3-07 / P3 | FIXED | geo 예제 미달 8건이 실제 CLI와 evidence 표에 일치한다. |
| B-P1-08 / P1 | FIXED | 추가 원문이 `++counter; window.confirm(...)`일 때 diff의 `+++`를 파일 헤더로 오인하지 않고 새 2행 P8을 exit 1로 잡는다. |
| B-P1-09 / P1 | FIXED | light/dark 조건 교집합, `:root.dark`, specificity/source order, 문자열·주석을 검증했다. 모순된 nested media는 값에 적용되지 않고 실제 dark 미달은 유지된다. 공백 유무는 동등하며 not/복합 media는 exit 2로 거부한다. |
| B-P2-10 / P2 | FIXED | T-103 수용 기준과 evidence가 역사 조사 1.15와 현재 sRGB 합성 1.32를 구분한다. 직접 airport 실측은 `1.3209340364487114`다. |

합성 비밀 marker는 `'gh' + 'p_' + 'Z' * 36`으로 조립하고 출력 포함 여부만 기록했다. 실제 비밀·운영 주소는 입력이나 보고서에 사용하지 않았다.

## B-P1-03 잔여 최소 재현과 영향

위치: `tools/ux_lint.py:87-96`의 `_is_executable_mdx_template`, `:109-131`의 `_mask_mdx_fence`, `:241`의 실행/문서 선택. 계약 근거는 T-103 구현 범위 2·수용 기준의 `.mdx` 검사 및 `docs/standards/ux-guide.md:206`의 문서 인용 제외다.

원인은 실행 template을 직전 문자 몇 개와 `String.raw` 이름으로 판별하는 데 있다. 실제 JSX 표현식 내부여도 쉼표·물음표·다른 tag 이름 뒤의 template을 문서 인용으로 가린다. 또한 fence 종료를 항상 동일 문자 3개로 시작하는지만 보므로 opening run보다 짧거나 끝에 문자가 붙은 줄을 종료로 받아들인다.

아래 코드는 제품을 수정하지 않고 임시 `Page.mdx`를 생성하는 완전한 CLI 재현이다. 첫 인자는 고정 후보 worktree다. Windows 3.14.3·WSL 3.11.15에서 같은 결과를 얻었다.

```python
from pathlib import Path
import json, os, subprocess, sys, tempfile

root = Path(sys.argv[1]).resolve()
env = {k: v for k, v in os.environ.items()
       if not k.startswith('GIT_') and k != 'GITHUB_STEP_SUMMARY'}
cases = {
    'array': 'export const X=()=> <div className={["kt", `outline-none`].join(" ")}/>;\n',
    'ternary': 'export const X=()=> <div className={true ? `outline-none` : "kt"}/>;\n',
    'tag': 'export const cls=String.raw;\nexport const X=()=> <div className={cls`outline-none`}/>;\n',
    'direct-control': 'export const X=()=> <div className={`outline-none`}/>;\n',
    'short-close': '````tsx\n```\nwindow.confirm("문서 예시");\n````\n',
    'suffix-close': '```tsx\n```not-a-closing-fence\nwindow.confirm("문서 예시");\n```\n',
    'fence-control': '```tsx\nwindow.confirm("문서 예시");\n```\n',
}
for name, source in cases.items():
    with tempfile.TemporaryDirectory(prefix='t103-post4-b-') as directory:
        path = Path(directory)
        (path / 'Page.mdx').write_text(source, encoding='utf-8')
        p = subprocess.run([sys.executable, '-B', '-X', 'utf8',
            str(root / 'tools/ux_lint.py'), '--root', str(path),
            '--fail-new', '--json'], cwd=path, env=env,
            capture_output=True, text=True, encoding='utf-8')
        result = json.loads(p.stdout)
        print(name, p.returncode, result['status'], len(result['findings']))
```

실제 출력: `array 0 PASS 0`, `ternary 0 PASS 0`, `tag 0 PASS 0`, `direct-control 1 FAIL 1`, `short-close 1 FAIL 1`, `suffix-close 1 FAIL 1`, `fence-control 0 PASS 0`.

기대: 실행 class인 처음 3개도 direct 대조군처럼 P6 1건·exit 1이어야 한다. 문서 fence 2개는 유효한 종료까지 인용으로 유지되어 exit 0이어야 한다. 일반 fence 대조군은 실제로 exit 0이다. 실행 template 안의 escaped `${...}` 내용은 실행 주석으로 잘못 가리지 않고 P6을 검출하는 수정도 확인했다.

영향: MDX의 실제 focus outline 제거가 신규 위반 gate를 통과한다. 문서에 중첩 fence 사용법이나 delimiter 뒤 텍스트를 적으면 반대로 P8 신규 위반으로 차단된다. 단순 prefix/tag 허용 목록 확대만으로는 동등한 실행 문법의 누락을 닫기 어렵다.

권고: MDX의 ESM/JSX 표현식과 Markdown 영역을 먼저 구분해 실행 영역의 모든 template을 보존하고, fence는 여는 문자·run 길이·닫는 줄의 허용 suffix를 추적한다. 위 3개 실행 사례와 2개 인용 사례를 양 OS 회귀에 추가한 새 immutable 후보로 재리뷰해야 한다. 현재 후보에서는 FIXED 또는 완료 처리할 수 없다.

## 실제 검증 명령과 결과

명령의 `python`은 위에 고정한 각 OS 실행 파일이다. 독립 사본 helper는 `.git/codex-audit/review-t102-b-wsl-unittest.py`와 `review-t102-post-b-gates.py`다. helper 이름에 과거 task가 들어가지만 이번에 넘긴 입력은 오직 post-fix-04 worktree였다. 전체 회귀는 manifest 명령과 같은 discovery/패턴을 실행하되 출력량 제한을 위해 `-v`를 생략했다. 집중 명령은 지정된 `-v`를 그대로 실행했다.

| 명령 | Windows 3.14.3 | WSL 3.11.15 |
|---|---|---|
| `python -B -X utf8 -m unittest discover -s tests -p test_*.py` | exit 0, 275/275 실행·통과, 66.504초, skip 0 | exit 0, 275개 중 272 실행·통과, 18.207초, skip 3 |
| `python -B -X utf8 -m unittest tests.test_kt_contrast tests.test_ux_lint -v` | 37/37, 8.701초, skip 0 | 37/37, 5.070초, skip 0 |
| 같은 두 모듈을 각각 `discover -p test_kt_contrast.py` / `test_ux_lint.py -v` | 19+18 통과 | 19+18 통과 |
| `python -B -X utf8 tools/validate_document_links.py` | 404문서·2412대상, 오류 0 | 동일 |
| `python -B -X utf8 tools/validate_plan.py` | 106 task, 오류 0 | 동일 |
| `python -B -X utf8 tools/check_spdx.py` | 56파일, 오류 0 | 동일 |
| `python -B -X utf8 tools/scan_secrets.py --all` | 536파일, 발견 0 | 동일 |
| `python -B -X utf8 tools/check_prod_redaction.py --all` | 536파일, 발견 0 | 동일 |
| `python -B -X utf8 tools/check_versions.py --self-check` | exit 0, 소비자 검사 미실행 | 동일 |
| `python -B -X utf8 tools/check_aliases.py packages/tokens/aliases` | CSS 1개, 오류 0 | 동일 |
| 별칭 집중 unittest | 35/35 통과 | 35개 중 34 통과·Windows 전용 1 skip |
| `python -B -X utf8 tools/kt_contrast.py packages/tokens/tokens.css --json` | exit 0, 27쌍 | 동일 |
| `python -B -X utf8 tools/ux_lint.py --root tests/fixtures/ux --json` | report 모드 exit 0, 12건 | 동일 |
| 4앱 예제 + 각 baseline + `--fail-new` | 미달 4/8/8/4건, baseline 적용 exit 0 | 동일 |
| `git diff --check 94ca2f1730b270721eb6242bfcdd9362b51d45e5 1625bf197486448f7dc6b7780a6c4f4c13b01368` | exit 0, 출력 없음 | 같은 Git blob 비교로 재사용 |

추가 직접 실행은 후보 밖의 독립 probe `t103-post1-b-originals.py`, `t103-b-edge.py`, `t103-post1-b-new.py`, `t103-post1-b-media.py`, `t103-post3-b-new.py`, `t103-post3-b-smoke.py`, `t103-post4-b-new.py`에 이번 후보 경로를 전달했다. 명칭과 무관하게 Windows와 WSL에서 모두 새로 실행했다. 위 disposition과 MDX 표는 이 실제 출력이다. 새로운 source 값과 Git diff를 직접 읽고, task·evidence의 airport/geo 값과 상태 `IN_PROGRESS`를 대조했다. 시험 성공을 T-103 완료나 소비자 gate 통과로 해석하지 않았다.

## NOT_RUN과 한계

- `NOT_RUN(Windows Python 3.11)`: 실행 파일 미설치. 요청자가 Windows 3.14 사용을 명시했다. Windows 3.11 통과 주장 없음.
- WSL 전체 skip 3개: Windows 8.3 API 전용 1개, `jsonschema` 미설치로 JSON Schema parity 2개. WSL에서 `find_spec('jsonschema') is None`을 확인했다. 이 3개를 실행 성공으로 세지 않는다. T-103 집중 37개는 skip 0이다.
- `NOT_RUN(원격 CI 독립 조회)`: 원격 CI 결과를 로컬 성공으로 대체하지 않았다. 이 보고서는 로컬 양 OS 후보 검증이다.
- `NOT_RUN(소비자 build/e2e, registry/npm/PyPI 게시, workflow dispatch)`: 요청 범위 밖. 실제 소비자 baseline 채택·T-010 workflow selftest는 해당 후속 task의 별도 gate다.
- `NOT_RUN(MDX compiler/browser 실행)`: 외부 패키지 설치 없이 CLI 반례·소스와 문법을 검토했다. 위 JSX/ESM 최소 입력과 문서 fence는 개별 파일로 분리했다.
- 제품·소비자 변경이나 push는 하지 않았다. 이 독립 원본만 별도 commit한다. 제품 기준선의 시작·종료 SHA/tree/clean은 위와 같다.

최종 **NO-GO**: 9개 누적 finding은 FIXED이나 `B-P1-03`의 실행 template 누락이 남았다. 수정 후보와 두 독립 재검토 전 T-103 종료를 승인하지 않는다.
