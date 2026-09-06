# tools — 문서·계획 검증 도구

이 디렉터리에는 저장소 문서의 정합성을 파일 변경 없이 검사하는 스크립트만 둔다. 제품 코드 빌드·테스트는 각 `packages/*`의 도구를 따른다.

| 스크립트 | 검사 내용 | 실행 |
|---|---|---|
| `validate_document_links.py` | `docs/`, `packages/`, `tools/`, `templates/`, `tests/`, 루트 Markdown의 저장소 내부 링크 target 존재 여부. 절대 경로 링크는 오류 | `python3 -B -X utf8 tools/validate_document_links.py` |
| `validate_plan.py` | `docs/tasks/T-NNN-*.md` 상세 task의 metadata(상태·우선순위·Gate·선행)와 `docs/tasks.md`/`docs/tasks-done.md` 요약의 일치, 선행 DAG 사이클 | `python3 -B -X utf8 tools/validate_plan.py` |

두 도구는 canview 저장소의 동명 도구를 kor-travel-common 경로에 맞게 적응한 것이다. 검사 규칙은 [tasks-rule](../docs/tasks-rule.md)과 [documentation maintenance](../docs/runbooks/documentation-maintenance.md)가 정본이며, 도구가 통과했다는 사실은 제품 gate 통과를 뜻하지 않는다.

회귀 시험(Linux/WSL; Git Bash·PowerShell에서는 `python`/`py -3`):

```bash
python3 -B -X utf8 -m unittest discover -s tests -p "test_*.py" -v
```

모든 도구는 Python 3.11+ 표준 라이브러리만 사용하며 Windows Python에서도 동작해야 한다([개발 환경](../docs/dev-environment.md) Tier 2).
