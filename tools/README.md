# tools — 문서·계획 검증 도구

이 디렉터리는 문서·계획·소스 규칙과 대비를 입력 파일 변경 없이 검사한다. 제품 코드 빌드·테스트는 각 `packages/*`의 도구를 따른다.

| 스크립트 | 검사 내용 | 실행 |
|---|---|---|
| `validate_document_links.py` | `docs/`, `packages/`, `tools/`, `templates/`, `tests/`, `LICENSES/`, 루트 Markdown의 저장소 내부 링크 target 존재 여부. 절대 경로 링크는 오류 | `python3 -B -X utf8 tools/validate_document_links.py` |
| `validate_plan.py` | `docs/tasks/T-NNN-*.md` 상세 task의 metadata(상태·우선순위·Gate·선행)와 `docs/tasks.md`/`docs/tasks-done.md` 요약의 일치, 선행 DAG 사이클 | `python3 -B -X utf8 tools/validate_plan.py` |
| `check_versions.py` | 소비 저장소의 지정 `--lockfiles` JSON 배열(또는 일반 탐색 모드)의 `package.json`/`package-lock.json`(v3)/`pyproject.toml`/`uv.lock`/`poetry.lock`/재귀 `requirements*.txt`에서 선언·설치 버전을 읽어 루트 `versions.json`과 대조하고 `OK`~`EXEMPT_EXPIRED` 10종으로 판정(Markdown 표 + JSON + `$GITHUB_STEP_SUMMARY`). 지정 모드는 열거한 lockfile만 읽어 범위가 넓어지지 않는다. 모드는 `versions.json` `consumers.<repo>.enforce`가 소유(`--mode`는 로컬 override). 규칙은 [versions](../docs/standards/versions.md) §3·§8 | `python3 -B -X utf8 tools/check_versions.py <소비 저장소 경로> --lockfiles '["package-lock.json"]' --repo <repo>` 또는 `--manifest <kor-travel-common.lock.json>` |
| `validate_manifest.py` | `consumer-manifest.v1` 필수 필드·미지 필드·`enforce` 금지·lockfile 종류·정규 POSIX 상대 경로·`until`/`review` 유효 날짜·`versions.json consumers` 정식 repo key를 strict 검사(exit 0/1). 오류에는 입력 field 원문을 재출력하지 않는다 | `python3 -B -X utf8 tools/validate_manifest.py <kor-travel-common.lock.json>` |
| `check_spdx.py` | 소스 선두 SPDX·저작권·Origin/Modified/Derived-From을 PROVENANCE와 대조. 전체 범위·제외·exit code는 [licensing §5.2](../docs/standards/licensing.md#52-검사-범위와-출처-대조) | `python3 -B -X utf8 tools/check_spdx.py` (`--root`로 fixture 지정) |
| `scan_secrets.py` | 자격증명 값 패턴, 파일·행·규칙 ID만 출력. 스냅샷·예외·exit code는 [CI §8.1](../docs/standards/ci-deploy.md#81-검사-범위와-실패-처리) | `python3 -B -X utf8 tools/scan_secrets.py --all` (`--staged`/`--base <commit>`) |
| `check_prod_redaction.py` | 같은 입력 선택기로 전체 또는 `--scope` 범위의 사설 주소·내부 호스트·운영 서비스 형식 검사 | `python3 -B -X utf8 tools/check_prod_redaction.py --all [--scope docs/]` |
| `check_aliases.py` | `packages/tokens/aliases`의 `--kt-*` 참조·Tailwind namespace·shadcn 중복·root/dark 완전성·재귀 import와 package/symlink 경계를 검사 | `python3 -B -X utf8 tools/check_aliases.py packages/tokens/aliases` |
| `kt_contrast.py` | canonical `tokens.css`와 순서가 있는 오버라이드의 TK-8 대비 쌍(OKLCH·hex·`var()`·sRGB alpha 합성)을 light/dark로 계산하고 baseline `until`·신규 미달을 판정. `--read-surface muted`로 앱별 추가 읽기 표면을 선언 | `python3 -B -X utf8 tools/kt_contrast.py packages/tokens/tokens.css [override.css ...] [--read-surface muted] [--baseline contrast-baseline.json --fail-new]` |
| `ux_lint.py` | 앱 소스의 UX 금지 규칙 P1~P8(대비 P4a/P4b 포함)을 전체 report하고 `--base` 추가 행·baseline 건수·만료를 판정. `--root`가 지정한 저장소의 Git 기준으로 diff를 계산하며 `--token-files`로 토큰 CSS allowlist를 지정 | `python3 -B -X utf8 tools/ux_lint.py --root <frontend-dir> --baseline ux-baseline.json [--base <sha>] [--token-files tokens.css,brand.css]` |
| `consumer_smoke.py` | `consumers.pins.json`의 소비자 checkout 저장소·40자 SHA·GPL 승인과 후보 npm tarball의 common artifact Release URL·SHA256·GPL metadata·정본 `LICENSE`·`NOTICE`·`THIRD_PARTY_NOTICES.md`·안전한 regular-file archive 구조를 검증. checkout·고정 Node/npm·`npm ci`·type-check·Next webpack/Turbopack 빌드는 workflow가 수행 | `python3 -B -X utf8 tools/consumer_smoke.py --pins consumers.pins.json --role map-tokens --asset candidate.tgz --asset-sha256 <sha256> --asset-url <release-url>` |

`validate_document_links.py`·`validate_plan.py`는 canview 저장소의 동명 도구를 kor-travel-common 경로에 맞게 적응한 것이다. 검사 규칙은 [tasks-rule](../docs/tasks-rule.md)과 [documentation maintenance](../docs/runbooks/documentation-maintenance.md)가 정본이며, 도구가 통과했다는 사실은 제품 gate 통과를 뜻하지 않는다.

MDX UX 검사는 `mdx_mask.mjs`와 잠긴 Node 의존을 함께 사용한다. 파서 미설치·잘못된 MDX는 exit 2이며 원문을 출력하거나 fallback으로 PASS 처리하지 않는다. 분석만 수행하며 사용자 import·표현식·플러그인을 실행하지 않는다. 설치 환경은 [개발 환경](../docs/dev-environment.md#6-검증-명령-사다리), 기존 MDX 호환 동작의 변경은 [ADR-016](../docs/adr/016-mdx-parser-for-ux-lint.md)이 정본이다.

회귀 시험(Linux/WSL; Git Bash·PowerShell에서는 `python`/`py -3`):

```bash
npm ci --ignore-scripts
python3 -B -X utf8 -m unittest discover -s tests -p "test_*.py" -v
```

매니페스트 기반 버전 검사는 소비자 저장소 루트와 매니페스트 경로를 함께 준다. `lockfiles[].path`와 `.github/workflows`는 저장소 루트에서 해석하고 `scope`가 `root`가 아니면 lockfile 기준 workspace 멤버 선언을 선택한다. lock·동반 선언·workspace·workflow·requirements 재귀 include의 최종 경로가 root 밖이면 exit 2다. 전이 lock scope와 경로는 민감한 값이 보고 채널로 재조합되지 않게 비식별화한다.

```bash
python3 -B -X utf8 tools/check_versions.py <consumer-repo-root> \
  --manifest <consumer-repo-root>/<app-dir>/kor-travel-common.lock.json
```

모든 도구는 Python 3.11+ 표준 라이브러리만 사용하며 Windows Python에서도 동작해야 한다([개발 환경](../docs/dev-environment.md) Tier 2).

`check_versions.py --self-check`는 입력 레지스트리만 검사한다. 소비자 실행에서 검사 범위가 없거나 입력 형식이 잘못되면 exit 2이며, 설치 버전을 해석하지 못하면 NO_LOCK이다. 자체 검사 성공은 소비자 버전 정렬 성공이 아니다.
