# T-012 tools/collect_manifests.py → `docs/integration-map.md` 생성 + `docs/architecture/adoption-readiness.md` gate 표 갱신

- 상태: BLOCKED
- 우선순위: P2
- Gate: 도구 테스트
- 선행: T-011

## 목표

소비자별 채택 상태(`docs/integration-map.md`)를 사람이 손으로 고치지 않고 매니페스트와 `consumers.pins.json`에서 결정적으로 생성하며, `adoption-readiness.md`의 gate 표 구간도 같은 도구가 갱신하게 한다.

## 고정 결정

- [설계 브리프](../plan/design-brief.md) D-19(`integration-map.md`는 생성물·수기 편집 금지), D-28(분기 보고가 이 지도를 입력으로 씀), D-18(`consumers.pins.json`).
- [문서 유지보수 runbook](../runbooks/documentation-maintenance.md) §3(machine-readable 정본은 값 파일, architecture에는 의미와 불변 조건만).
- [canview 구조 체크리스트](../survey/cross/canview-structure-checklist.md) §2.6 A6.1(생성물과 원본의 수동 불일치 금지).
- 입력 소스: 로컬 체크아웃 경로(`--consumer <repo>=<path>`, `consumer-smoke`가 pinned SHA로 체크아웃한 디렉터리) 또는 `templates/manifests/*`(오프라인 기본). 네트워크 접근 없음.

## 구현 범위

1. `tools/collect_manifests.py`: 입력 매니페스트를 `validate_manifest`로 검증 후 표(저장소·앱·tokens·ui·py·lockfile·baseline·예외 수·`enforce`(`versions.json`에서)·핀 SHA)를 결정적 Markdown으로 출력. 머리에 "생성물 — 수기 편집 금지, 생성 명령·입력 커밋" 1문단. `--check`는 기존 파일과 byte 비교해 drift면 exit 1.
2. `docs/architecture/adoption-readiness.md`에 마커 `<!-- collect_manifests:start -->`/`<!-- collect_manifests:end -->` 구간을 두고 그 사이만 갱신.
3. `docs.yml` `docs` job에 `collect_manifests.py --check`(입력 `templates/manifests/`) 추가; `consumer-smoke`에서는 실제 체크아웃 입력으로 생성해 아티팩트로 첨부.
4. `tests/test_collect_manifests.py`(결정성: 같은 입력 2회 → 동일 바이트; 마커 구간 외 불변; `--check` drift exit 1).

## 범위 밖

- 매니페스트 스키마(T-011), 소비자 저장소 커밋(T-403), 회수 지표 계산(T-503), 분기 감사 runbook(T-506).

## 예상 변경 파일

예정 경로는 존재·실행 증거가 아니다. `tools/collect_manifests.py`, `tests/test_collect_manifests.py`, `docs/integration-map.md`(생성물로 교체), `docs/architecture/adoption-readiness.md`(마커 구간), `.github/workflows/docs.yml`, `tools/README.md`(행 추가).

## 수용 기준

- 같은 입력으로 두 번 생성한 `integration-map.md`가 byte 단위로 같다(정렬 고정·타임스탬프 없음, 입력 커밋만 표기).
- `--check`가 수기 편집을 exit 1로 잡고 `docs` job이 이를 실행한다.
- `adoption-readiness.md`의 마커 밖 본문이 도구 실행 전후로 불변이다.
- 생성 표의 `enforce` 값이 `versions.json consumers.<repo>.enforce`와 같다.
- Linux·Windows 결과 동일(개행 LF 고정).

## 검증 명령

```bash
python3 -B -X utf8 tools/collect_manifests.py --input templates/manifests --write
python3 -B -X utf8 tools/collect_manifests.py --input templates/manifests --check; echo "exit=$?"
python3 -B -X utf8 -m unittest discover -s tests -p "test_collect_manifests.py" -v
git diff --stat -- docs/integration-map.md docs/architecture/adoption-readiness.md
```

Git Bash에서 동일.

## evidence

- 생성 입력 커밋·`--check` exit code·테스트 수를 이 절과 `docs/journal.md`에 남긴다. 실제 소비자 체크아웃 입력으로 생성한 결과는 `consumer-smoke` 아티팩트 링크로 남긴다.

## rollback 또는 release 차단 조건

- 도구·생성물만 바뀌므로 `git revert` 1회로 원복한다.
- 생성물에 수기 편집이 섞인 채로는 T-503 보고를 만들지 않는다.
