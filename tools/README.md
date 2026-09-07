# tools — 문서·계획 검증 도구

이 디렉터리에는 저장소 문서의 정합성을 파일 변경 없이 검사하는 스크립트만 둔다. 제품 코드 빌드·테스트는 각 `packages/*`의 도구를 따른다.

| 스크립트 | 검사 내용 | 실행 |
|---|---|---|
| `validate_document_links.py` | `docs/`, `packages/`, `tools/`, `templates/`, `tests/`, `LICENSES/`, 루트 Markdown의 저장소 내부 링크 target 존재 여부. 절대 경로 링크는 오류 | `python3 -B -X utf8 tools/validate_document_links.py` |
| `validate_plan.py` | `docs/tasks/T-NNN-*.md` 상세 task의 metadata(상태·우선순위·Gate·선행)와 `docs/tasks.md`/`docs/tasks-done.md` 요약의 일치, 선행 DAG 사이클 | `python3 -B -X utf8 tools/validate_plan.py` |
| `check_versions.py` | 소비 저장소의 `package.json`/`package-lock.json`(v3)/`pyproject.toml`/`uv.lock`/`poetry.lock`/재귀 `requirements.txt`에서 선언·설치 버전을 읽어 루트 `versions.json`과 대조하고 `OK`~`EXEMPT_EXPIRED` 10종으로 판정(Markdown 표 + JSON + `$GITHUB_STEP_SUMMARY`). Poetry lock은 제한된 package/git 구조를 읽고 requirements는 정확 핀 후보·`NO_LOCK`·`BLOCKED`만 보고한다. 모드는 `versions.json` `consumers.<repo>.enforce`가 소유(`--mode`는 로컬 override). 규칙은 [versions](../docs/standards/versions.md) §3·§8 | `python3 -B -X utf8 tools/check_versions.py <소비 저장소 경로> --repo <repo>` 또는 `--manifest <kor-travel-common.lock.json>` |
| `check_spdx.py` | 소스 선두 SPDX·저작권·Origin/Modified/Derived-From을 PROVENANCE와 대조. 전체 범위·제외·exit code는 [licensing §5.2](../docs/standards/licensing.md#52-검사-범위와-출처-대조) | `python3 -B -X utf8 tools/check_spdx.py` (`--root`로 fixture 지정) |
| `scan_secrets.py` | 자격증명 값 패턴, 파일·행·규칙 ID만 출력. 스냅샷·예외·exit code는 [CI §8.1](../docs/standards/ci-deploy.md#81-검사-범위와-실패-처리) | `python3 -B -X utf8 tools/scan_secrets.py --all` (`--staged`/`--base <commit>`) |
| `check_prod_redaction.py` | 같은 입력 선택기로 전체 트리의 사설 주소·내부 호스트·운영 서비스 형식 검사 | `python3 -B -X utf8 tools/check_prod_redaction.py --all` |

`validate_document_links.py`·`validate_plan.py`는 canview 저장소의 동명 도구를 kor-travel-common 경로에 맞게 적응한 것이다. 검사 규칙은 [tasks-rule](../docs/tasks-rule.md)과 [documentation maintenance](../docs/runbooks/documentation-maintenance.md)가 정본이며, 도구가 통과했다는 사실은 제품 gate 통과를 뜻하지 않는다.

회귀 시험(Linux/WSL; Git Bash·PowerShell에서는 `python`/`py -3`):

```bash
python3 -B -X utf8 -m unittest discover -s tests -p "test_*.py" -v
```

모든 도구는 Python 3.11+ 표준 라이브러리만 사용하며 Windows Python에서도 동작해야 한다([개발 환경](../docs/dev-environment.md) Tier 2).

`check_versions.py --self-check`는 입력 레지스트리만 검사한다. 소비자 실행에서 검사 범위가 없거나 입력 형식이 잘못되면 exit 2이며, 설치 버전을 해석하지 못하면 NO_LOCK이다. 자체 검사 성공은 소비자 버전 정렬 성공이 아니다.
