# T-103 수정 후 16 — Reviewer A 독립 원본

- 실행 ID: `reviewer_a-t103-post16-20260908T125256+0900`.
- 판정: **PASS**. 누적 A finding 15개 모두 FIXED. 신규·잔여 P0/P1/P2/P3 각 0개.
- 제품 후보 commit: `73b9cf68788066742e8df99dfad2433cbe6bf5fc`; tree: `70143a39a0ed31dd44a2b28aa81a2a58f23248d3`.
- 직전 제품 후보: `210c2de324b18fcaa4e3f8b18fe5965226cb79d7`. 이번 도구·시험 delta는 `tools/ux_lint.py`, `tests/test_ux_lint.py`이며 전체를 읽었다. AGENTS·문서 라우터·task·standards·runbook의 delta는 없다.
- 공통 manifest: commit `4f3bb3d0b530e9486405a22b879a9786c0913b79`의 `docs/reviews/adversarial/evidence/2026-09-08-t103-post-fix-16-manifest.md`를 `git show`로 읽었다. manifest의 과거 원본 메타데이터 외에 상대 원본·이번 결과·미확정 원본은 읽지 않았다.
- 격리: `F:/dev/kor-travel-common-wt/review-t103-post16-a`, 새 detached checkout. 제품·manifest·소비자·Git config는 수정하지 않았다. 새 원본 한 파일만 별도 커밋한다.
- 시작: 2026-09-08 12:52:56.230 KST, 위 SHA/tree, `git status --porcelain=v1` 빈 출력.
- 제품 검토 종료: 2026-09-08 12:55:33.262 KST, 동일 SHA/tree, `git status --porcelain=v1` 빈 출력. 이후 evidence commit/tree는 제품 후보와 구분한다.

## 요청과 독립 검증

조정자가 지정한 동일 후보에서 Windows Python 3.14와 WSL Python 3.11의 full/focused/static gate 및 누적 CSS/JSON/redaction/diff/symlink/airport corpus를 직접 실행했다. 특히 U+11F02/U+2EBF0 최신 식별자와 U+FEFF 선행·식별자 뒤 공백, 미종결 1/2자 span 및 정상 닫힌/개방 대조를 재현했다. 작성자의 성공 주장이나 상대 결과에 의존하지 않았다.

이번 수정은 구버전 Python이 비ASCII 문자를 `Cn`으로 분류해도 중괄호 실행식 후보로 보존하고, U+FEFF를 표현식 시작·식별자 뒤의 공백 처리에 포함한다. 현재 규칙 문서의 P1~P8 패턴 검사 계약과 이 수정의 문서/실행 코드 구분을 기준으로 검토했다.

## A-P2-06 수정 확인

아래 Python 값으로 실제 문자를 생성해 독립 임시 fixture에 기록했다. 각 expression을 미종결 1자 span, 미종결 2자 span, span 없는 개방 입력, 정상 닫힌 span에 넣어 양 OS에서 각각 20개 결과를 확인했다.

```python
expressions = [
    chr(0x11F02) + " && window.confirm('x')",
    chr(0x2EBF0) + " && window.confirm('x')",
    "\ufeff\u2118 && window.confirm('x')",
    "\u2118\ufeff&& window.confirm('x')",
    "/* note */\ufeff" + chr(0x11F02) + "\ufeff&& window.confirm('x')",
]
```

| 형태 | Windows 3.14.3 | WSL 3.11.15 |
|---|---|---|
| 미종결 1자 span 뒤 expression | 각각 P8 1개 / exit 1 | 동일 |
| 미종결 2자 span 뒤 expression | 각각 P8 1개 / exit 1 | 동일 |
| span 없는 expression | 각각 P8 1개 / exit 1 | 동일 |
| 정상 닫힌 코드 span | 각각 0개 / exit 0 | 동일 |

직전 U+11F02 반례의 WSL 거짓 PASS가 사라졌고 정상 인용 음성 대조는 유지됐다. 기존 `℘`/`Ⅳ`/U+037A/`a·`/`a·`/`async x =>`, 일반 Unicode·결합 문자·ZWNJ/ZWJ·두 escape 형식, 직접/단항/키워드/논리/숫자/정규식/소수/나눗셈/xor/주석 선행 expression도 모두 재현했다. 여러 줄 JSX의 `outline-none`은 P6 1개 / exit 1, `safe`는 0이었다. 파일 첫 span·3자 inline·4자/tilde/suffix fence·blockquote 빈 문단·backslash delimiter·tagged/computed template·배열/삼항·중첩 object·ESM·보간 주석 대조도 유지됐다.

## 누적 finding disposition

| 원 ID | 원 심각도 | 판정 | 이번 후보 직접 검증 |
|---|---|---|---|
| A-P1-01 | P1 | FIXED | CSS root/dark·specificity·media 교집합·unsupported selector·빈 목록·descendant·comment-gap. `.dark/**/.dark`, `.dark/**/:not(.light)` 일반 오류 2, 유효 cascade 미달 1. |
| A-P1-02 | P1 | FIXED | OKLCH chroma `25%`와 `0.1` 변환 RGB 일치. |
| A-P1-03 | P1 | FIXED | 흰색 20% / 검정 sRGB source-over와 `#333` 대비 1.6620953314177012 일치. |
| A-P1-04 | P1 | FIXED | baseline 앞 신규 행만 fail, 기존 등록 행은 면제. |
| A-P1-05 | P1 | FIXED | 같은 basename의 외부 임시 Git root를 후보와 구분. |
| A-P2-06 | P2 | FIXED | 위 최신 Unicode/공백 및 누적 MDX 반례에서 양 OS 탐지·인용 음성 대조 확인. |
| A-P2-07 | P2 | FIXED | `--base=--name-only` 일반 오류 2. |
| A-P2-08 | P2 | FIXED | WSL Git quoting/tab 파일명 추가 행 P6 탐지. Windows 해당 파일명은 NOT_RUN. |
| A-P2-09 | P2 | FIXED | NaN/Infinity/음수/bool/중복 및 400·5000자리 JSON 일반 오류 2. |
| A-P2-10 | P2 | FIXED | 합성 marker가 stderr/JSON/summary/argparse 오류에 평문 노출되지 않음. |
| A-P2-11 | P2 | FIXED | muted 읽기 표면 총 31쌍, 추가 4쌍 및 tertiary/muted 미달 확인. |
| A-P3-12 | P3 | FIXED | geo 미달 8개, airport 현재 1.32(실측 1.320934)와 과거 1.15 구분 유지. |
| A-P1-13 | P1 | FIXED | 실제 `++counter;` 추가 행에서 생기는 diff `+++`를 헤더로 버리지 않고 후속 추가 행 P6 탐지. |
| A-P2-14 | P2 | FIXED | 양 OS self-symlink root 일반 오류 2 / traceback 없음. 초기 helper의 Windows 미지원 표기와 별개로 후속 Windows 직접 링크 probe 실행. |
| A-P2-15 | P2 | FIXED | 깊이 2000 JSON을 두 도구에 입력해 양 OS 일반 오류 2 / traceback 없음. |

## 실제 검증 명령과 결과

Windows Python 3.14.3, WSL은 `uv run --no-project --python 3.11`의 Python 3.11.15다. WSL 전체 시험에는 `--with jsonschema`를 추가했다. WSL Git 정적 gate에만 detached checkout의 `GIT_DIR`/`GIT_WORK_TREE`를 프로세스 환경으로 지정했고 시험/probe에는 주입하지 않았다. Git config는 불변이다.

| Windows 명령(WSL은 위 uv 접두 사용) | Windows | WSL |
|---|---|---|
| `python -B -X utf8 -m unittest discover -s tests -p 'test_*.py'` | 288 실행 / 288 통과 / skip 0, 100.984초 | 288 실행 / 287 통과 / skip 1, 54.669초. skip은 Windows 8.3 전용 |
| `python -B -X utf8 -m unittest tests.test_kt_contrast tests.test_ux_lint` | 50 통과 / skip 0, 14.549초 | 50 통과 / skip 0, 10.044초 |
| `python -B -X utf8 tools/validate_document_links.py` | 문서 439개 / 대상 2418개 / 오류 0 | 동일 |
| `python -B -X utf8 tools/validate_plan.py` | task 106개 / 오류 0 | 동일 |
| `python -B -X utf8 tools/check_spdx.py` | 56개 / 오류 0 | 동일 |
| `python -B -X utf8 tools/scan_secrets.py --all` | 571개 / 발견 0 | 동일 |
| `python -B -X utf8 tools/check_prod_redaction.py --all` | 571개 / 발견 0 | 동일 |
| `python -B -X utf8 tools/check_versions.py --self-check` | exit 0; 소비자 검사 아님 | 동일 |
| `python -B -X utf8 tools/check_aliases.py packages/tokens/aliases` | CSS 1개 / 오류 0 | 동일 |
| `git diff --check a7814d7 73b9cf68788066742e8df99dfad2433cbe6bf5fc` | exit 0 | exit 0 |

직접 probe 명령은 `python -B -X utf8 F:/dev/kor-travel-common/.git/codex-audit/t103-post16-reviewer-a-probe.py F:/dev/kor-travel-common-wt/review-t103-post16-a`다. WSL은 두 경로를 `/mnt/f/...`로 바꾸고 uv 접두로 실행했다. 자신의 누적 A probe만 재사용하며 상대 결과·과거 raw 본문은 읽지 않는다. 후보 밖 helper SHA256은 `F056B8EB7B9C6C66FF963EEFD4106A584D657700F7AB99739D0B60CBF1380861`이며 원본 commit에 포함하지 않는다. 임시 fixture의 subprocess는 그 임시 root를 cwd로 사용한다.

정본 light/dark 각각 27쌍 미달 0. 4앱 예제 light 미달은 docker-manager/concierge/geo/airport 순서로 4/8/8/4이며 baseline의 `--fail-new` exit 0을 미달 없음으로 해석하지 않는다. UX fixture report는 finding 12개 / exit 0이다. 오류 채널의 traceback/합성 marker 부재도 별도 확인했다.

`gh run list --commit 73b9cf68788066742e8df99dfad2433cbe6bf5fc --json databaseId,headSha,status,conclusion,url --limit 5`로 [CI run 34184954582](https://github.com/digitie/kor-travel-common/actions/runs/34184954582)의 exact headSha와 conclusion **cancelled**를 확인했다. 리뷰 PASS를 정확한 후보의 원격 CI 성공으로 바꾸지 않는다. CI/merge gate는 조정자가 별도 확인해야 한다.

## 미실행과 한계

- `NOT_RUN`: Windows Python 3.11. 런타임 부재로 조정자 지정 Windows 3.14 / WSL 3.11을 사용했다.
- `NOT_RUN`: 실제 소비자 build/e2e·adoption gate, registry 조회·게시, workflow dispatch. common 리뷰 범위 밖이다.
- `NOT_RUN`: 이번 후보의 브라우저/MDX compiler 렌더링. 현재 정본의 패턴 검사와 CLI 대조 결과이며 임의의 모든 JavaScript 문법에 대한 compiler 검증을 뜻하지 않는다.
- 원본 추가 후 전체 staged diff·공백·문서 링크·staged 비공개 검사를 확인하여 원본만 커밋한다. 제품·manifest·기존 원본은 변경하지 않는다.
