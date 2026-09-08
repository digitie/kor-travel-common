# T-103 post-fix-05 독립 적대적 리뷰 B 원본

- 실행 ID: `T103-POST5-B-20260908T102655-KST`.
- 판정: **NO-GO**. 잔여 `B-P1-03`과 신규 `B-P1-11`이 있다. P0 0건, P1 2건, 신규 P2/P3 0건이다.
- 시작 KST: `2026-09-08T10:26:55.9813881+09:00`; 제품 검증 종료 KST: `2026-09-08T10:31:13.1575780+09:00`.
- 시작·종료 제품 HEAD: `ecad460db93a9369d96435a28b6cb48dd7516ace`.
- 시작·종료 제품 tree: `6a903d346072ca951fe5146653addaa250fd44f5`.
- 시작·종료 `git status --porcelain=v1`: 빈 출력, clean. 제품 검증 종료 후 원본 보고서 하나를 커밋하기 위해 `codex/review-t103-post5-b`를 만들었다. 보고서 commit은 제품 검증 SHA와 구분한다.
- 격리: 새 detached worktree `F:/dev/kor-travel-common-wt/review-t103-post5-b`. 전체 회귀·정적 gate는 후보를 임시 독립 Git 저장소로 복사하고 `GIT_*` 환경을 제거해 실행했다. 반례 입력은 후보 밖 임시 디렉터리에서 생성했다. 제품·소비자·source checkout 파일은 수정하지 않았다.
- source `.git/config` 시작·종료 SHA256 동일: `0A0F849E7874CF0A25926856F9D2E381CCBF4C2DCB5999869C57B86E0F5BEB5B`. `core.worktree`를 변경하지 않았다.
- manifest는 `git show 93b9eb1:docs/reviews/adversarial/evidence/2026-09-08-t103-post-fix-05-manifest.md`로만 읽었다. 전체 manifest commit: `93b9eb1dfac9a3f2629c04b87e4f3cdb29a59738`; Git blob SHA256: `56493a54da711e8232d578914c36eb1a0b9a6303202deaa5dac75e2050364b97`.
- 상대 이번/이전 raw를 읽거나 요청하지 않았다. `1625bf1..ecad460`의 7개 변경 경로와 도구 2개·시험 2개 전체 diff를 검토했으며 이전 상대 raw 본문은 제외했다. task·정본·evidence가 이 delta에서 불변임을 확인하고 관련 계약을 다시 대조했다.

## 전달 요청 원문

> 새 immutable post-fix-05 후보를 독립 적대 리뷰하세요. 코드 후보 commit `ecad460db93a9369d96435a28b6cb48dd7516ace`, tree `6a903d346072ca951fe5146653addaa250fd44f5`; 기준선 manifest는 `93b9eb1`의 `docs/reviews/adversarial/evidence/2026-09-08-t103-post-fix-05-manifest.md`를 git show로만 읽으세요. 상대 post-fix-05 raw와 이전 상대 raw는 읽지 마세요. B 잔여(배열/삼항/임의 tagged template 실행, opening run보다 짧거나 suffix가 붙은 fence의 조기 종료)를 포함해 CSS selector/media/specificity/JSON/argparse/redaction/diff/symlink/airport와 전체 회귀를 Windows 3.14 및 WSL 3.11에서 독립 검증하세요. 제품·소비자·registry·workflow는 수정/호출하지 말고, 새 raw 파일 `docs/reviews/adversarial/evidence/2026-09-08-t103-post-fix-05-reviewer-b.md` 하나만 추가해 별도 commit하세요. 시작/종료 HEAD/tree/status와 Windows 3.11 NOT_RUN을 기록하고, commit SHA·SHA256·verdict를 보내 주세요. 원본은 PASS일 때도 반드시 commit하세요.

## 누적 finding disposition

| ID / 원 심각도 | 결과 | 이번 후보에서 다시 실행한 관찰 |
|---|---|---|
| B-P1-01 / P1 | FIXED | 외부 `--root`의 Git 저장소를 기준으로 추가 행을 판정한다. CWD가 common이어도 exit 1이다. |
| B-P1-02 / P1 | FIXED | 새 앞 행이 과거 baseline 건수를 소비하지 않는다. 추가 1행은 fail, 이동한 기존 3행만 exempt다. |
| B-P1-03 / P1 | **OPEN** | 이전 단일행 배열/삼항/임의 tag는 각각 P6·exit 1, 짧거나 suffix가 붙은 fence는 인용 유지·exit 0으로 수정됐다. 그러나 아래 multiline 실행 template과 blockquote JSX는 PASS 0건이다. |
| B-P1-04 / P1 | FIXED | CSS 값·누락 경로·var 참조·baseline·잘못된 옵션과 `--json=` 입력은 generic exit 2, traceback/marker 없음. stdout JSON·Markdown·step summary 경로 redaction도 유지된다. |
| B-P2-05 / P2 | FIXED | 명시적 muted 읽기 표면을 더하면 31쌍이며 1:1 미달은 fail, 반복 옵션은 중복하지 않는다. |
| B-P2-06 / P2 | FIXED | bool/소수/무한대 count·버전·5,000자리 정수·깊이 2,000 JSON 경계가 exit 2·traceback 없음이다. |
| B-P3-07 / P3 | FIXED | geo 미달 8건이 CLI와 evidence에 일치한다. |
| B-P1-08 / P1 | FIXED | diff에서 `++counter; window.confirm(...)` 추가 행을 헤더로 오인하지 않고 P8·exit 1로 판정한다. |
| B-P1-09 / P1 | FIXED | 기존 media 교집합·specificity/source order·root.dark·nested/string/comment 반례가 유지된다. not/복합 조건은 exit 2이며 minified 조건은 공백 표기와 동등하다. 별도 selector 정규화 결함은 B-P1-11이다. |
| B-P2-10 / P2 | FIXED | Airport task 수용 기준·evidence는 역사 조사 1.15와 현재 sRGB 합성 1.32를 분리한다. 직접 실측 `1.3209340364487114`와 일치한다. |

합성 marker는 `'gh' + 'p_' + 'Z' * 36`으로 조립하고 노출 여부만 확인했다. 실제 비밀·운영 주소는 사용하지 않았다.

## B-P1-03: 실행 문맥을 현재 행으로 잘라 multiline·blockquote JSX를 누락

- 심각도: **P1**, 기존 ID 유지, 수정 필요.
- 위치: `tools/ux_lint.py:90-93`. `prefix`를 현재 행 시작부터 자르고 비었거나 `>`로 시작하면 즉시 문서 인용으로 처리한다.
- 계약: T-103의 `.mdx` 금지 패턴 검사, 실행 template 보존과 문서 인용 제외.
- 아래 입력을 각각 임시 `Page.mdx`로 저장하고 `python -B -X utf8 <후보>/tools/ux_lint.py --root <임시 디렉터리> --fail-new --json`을 실행했다.

```mdx
export const X=()=> (
<div className={
 `outline-none`
}/>
);
```

동등한 추가 반례 두 개도 각각 별도 파일로 실행했다.

```mdx
export const X=()=> <div className={true ?
 `outline-none` : "kt"}/>;
```

```mdx
> <div className={`outline-none`} />
```

Windows 3.14.3·WSL 3.11.15에서 3개 모두 **exit 0, PASS, findings 0**. 첫 입력에서 JSX를 한 행으로 합친 대조군은 **exit 1, FAIL, P6 1건**이다. 순수 blockquote code span은 기대대로 PASS 0건이다.

영향: 포매터가 JSX 속성 값을 다음 행으로 옮기는 것만으로 실제 focus outline 제거를 탐지하지 못한다. Markdown blockquote 안의 JSX도 실행 가능하므로 단순 `>` 접두어만으로 전부 인용 처리하면 안 된다.

원인·수정 경계: 이전 제품 `1625bf1`과 동일한 도구를 갖는 post4 격리 사본에 같은 probe를 실행하면 첫 multiline class와 blockquote JSX는 각각 exit 1이었다. 이번 행 단위 절단·`>` 조기 반환으로 두 반례가 회귀했다. multiline 삼항식은 이전에도 남아 있던 누락이다. 제품 코드 비교만 수행했고 이전 raw는 읽지 않았다.

권고: 문맥을 행마다 초기화하지 말고 MDX ESM/JSX 표현식의 열림·닫힘과 Markdown 인용을 추적한다. 실행 여부 판정을 식별자/문자 몇 개의 허용 목록에 계속 추가하는 방식으로 종료하지 말고 multiline·blockquote JSX와 순수 code span을 함께 회귀로 고정해야 한다.

## B-P1-11: selector 정규화가 문자열 공백·대소문자를 바꿔 잘못된 대비 PASS

- 심각도: **P1**, 신규 ID, 수정 필요.
- 위치: `tools/kt_contrast.py:171`의 selector 전체 `.lower()` 및 `:196`의 전체 공백 제거. 문법 공백과 리터럴의 데이터를 구별하지 않는다.
- 최소 입력은 임시 `override.css`의 다음 두 선언이다.

```css
:root { --kt-control-line: #000; }
[data-theme='d ark'] { --kt-control-line: #fff; }
```

실행: `python -B -X utf8 <후보>/tools/kt_contrast.py <후보>/packages/tokens/tokens.css <임시>/override.css --dark --fail-new --json`.

Windows와 WSL 모두 **exit 0, PASS**이며 control-line 4쌍을 전부 통과시켰다. page/subtle/muted/card 비율은 각각 `18.442/16.412/13.097/16.857`이다. 두 번째 선언을 제거하면 **exit 1, FAIL**, 동일 4쌍은 `1.139/1.280/1.603/1.246`으로 모두 미달이다.

`d ark`는 `dark`와 다른 속성값이다. 입력의 두 번째 selector가 정상 dark 루트에 적용되는 것처럼 값 `#fff`를 사용해서는 안 된다. 제한된 지원 문법 정책상 generic exit 2로 거부하거나, 지원하기로 한 실제 의미에 따라 적용 범위를 구별해야 한다. 현재 PASS는 어느 쪽도 아니다.

추가 동형 입력 `[data-theme = 'd ark']`, `[data-theme='DARK']`, `.DARK`도 같은 잘못된 PASS다. 대조군인 `[data-theme='dark']`, `.dark`는 실제 dark 규칙이므로 PASS가 맞다. 클래스와 `data-*` 값은 임의로 소문자화할 수 없다.

원인·수정 경계: 같은 probe를 이전 제품 코드에서 실행하면 `d ark` 두 표기는 exit 1로 원래 control-line 미달을 유지했다. 이번 전체 공백 제거가 새 회귀다. `.DARK`/`DARK` 소문자화는 이전부터 존재한 별도 동형 누락이며, 이번 독립 조사에서 함께 발견했다.

영향: 실제 앱 dark 테마의 3:1 미달을 관련 없는 selector의 흰 선 값으로 덮어써 WCAG gate를 통과시킨다. 토큰 값 자체가 바뀌지 않아도 selector 정규화만으로 잘못된 합격이 가능하다.

권고: selector를 토큰화해 문법상 허용된 바깥 공백·인용 방식만 정규화하고, 클래스·속성 문자열의 대소문자·내부 공백은 보존한다. 지원하지 않는 selector는 정본 정책에 맞게 명시적으로 거부한다. 올바른 dark 대조군과 세 종류의 비동치 문자열을 한 시험군으로 고정한다.

## 검증 명령과 실제 결과

Windows 실행 파일은 `py -3.14`의 **3.14.3**, WSL은 `/home/digitie/.local/share/uv/python/cpython-3.11-linux-x86_64-gnu/bin/python3.11`의 **3.11.15**를 직접 확인했다. 아래 `python`은 이 실행 파일이다. 전체 discovery는 출력량을 제한하려고 manifest의 `-v`만 생략했다. 집중 시험은 지정 명령 그대로다.

| 명령 | Windows | WSL |
|---|---|---|
| `python -B -X utf8 -m unittest discover -s tests -p test_*.py` | 279 실행·통과, 73.373초, skip 0 | 279개 중 276 실행·통과, 20.179초, skip 3 |
| `python -B -X utf8 -m unittest tests.test_kt_contrast tests.test_ux_lint -v` | 41/41, 8.996초, skip 0 | 41/41, 5.283초, skip 0 |
| `python -B -X utf8 tools/validate_document_links.py` | 407문서·2412대상, 오류 0 | 동일 |
| `python -B -X utf8 tools/validate_plan.py` | 106 task, 오류 0 | 동일 |
| `python -B -X utf8 tools/check_spdx.py` | 56파일, 오류 0 | 동일 |
| `python -B -X utf8 tools/scan_secrets.py --all` | 539파일, 발견 0 | 동일 |
| `python -B -X utf8 tools/check_prod_redaction.py --all` | 539파일, 발견 0 | 동일 |
| `python -B -X utf8 tools/check_versions.py --self-check` | exit 0, 소비자 검사 미실행 | 동일 |
| `python -B -X utf8 tools/check_aliases.py packages/tokens/aliases` | CSS 1개, 오류 0 | 동일 |
| 별칭 집중 unittest | 35/35 통과 | 35개 중 34 실행·통과, Windows 전용 1 skip |
| `python -B -X utf8 tools/kt_contrast.py packages/tokens/tokens.css --json` | exit 0, 27쌍 | 동일 |
| `python -B -X utf8 tools/ux_lint.py --root tests/fixtures/ux --json` | report 모드 exit 0, 12건 | 동일 |
| 4앱 예제 + baseline + `--fail-new` | 미달 4/8/8/4건, baseline 적용 exit 0 | 동일 |
| `git diff --check 94ca2f1730b270721eb6242bfcdd9362b51d45e5 ecad460db93a9369d96435a28b6cb48dd7516ace` | exit 0, 출력 없음 | 동일 Git blob 비교 재사용 |

전체 시험/정적 gate는 후보 밖 helper `review-t102-b-wsl-unittest.py`·`review-t102-post-b-gates.py`로 격리 사본에서 실행했다. 직접 probe는 `.git/codex-audit/`의 `t103-post1-b-originals.py`, `t103-b-edge.py`, `t103-post1-b-new.py`, `t103-post1-b-media.py`, `t103-post3-b-new.py`, `t103-post3-b-smoke.py`, `t103-post4-b-new.py`, `t103-post5-b-new.py`다. 이름에 과거 task/회차가 들어가도 매번 이번 후보 경로를 인자로 넘겨 양 OS에서 새로 실행했다. 마지막 probe의 이전 코드 대조 실행은 Windows에서만 했고 이전 후보에 대한 새 전체 PASS로 세지 않았다.

CSS 조건 교집합, `.dark:root`·인용 방식 동치, 높은 specificity·source order, not/복합 media 거부, nested/string/comment 경계, 깊은 JSON, argparse 값, 오류 stdout/stderr와 정상 JSON/Markdown/step summary redaction, diff `+++`, self-symlink root를 직접 반례와 focused 시험으로 대조했다. 문서·GPL 범위·미게시·소비자 경계는 불변이며 task/resume의 `IN_PROGRESS`와 미실행 후속 gate를 완료로 해석하지 않았다.

## NOT_RUN과 판정 범위

- `NOT_RUN(Windows Python 3.11)`: 호스트에 설치되어 있지 않으며 요청자는 Windows 3.14 사용을 지정했다.
- WSL skip 3개는 Windows 8.3 API 1개와 `jsonschema` 미설치로 JSON Schema parity 2개다. 이번에도 `find_spec('jsonschema') is None`을 확인했다. 실행 성공 건수에 넣지 않는다. T-103 집중 41개는 양 OS skip 0이다.
- `NOT_RUN(원격 CI 독립 조회)`: 로컬 성공을 원격 CI 성공으로 세지 않는다.
- `NOT_RUN(소비자 build/e2e, registry/npm/PyPI 게시, workflow dispatch, MDX compiler/browser 실행)`: 요청 범위 밖이며 패키지 설치나 외부 실행은 하지 않았다. MDX/CSS 반례는 고정 코드의 CLI와 의미를 대조했다.
- 소비자 baseline·T-010 workflow selftest는 해당 후속 task가 소유한다. 이 보고서만 별도 commit하며 제품 변경·push는 하지 않는다.

최종 **NO-GO**. 기존 단일행/fence 수정은 확인했지만 B-P1-03의 실행 문맥 누락과 B-P1-11의 잘못된 대비 PASS가 남았다. 새 후보의 수정과 독립 재검토가 필요하다.
