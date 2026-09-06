# T-009 common CI 하드닝(permissions·concurrency·timeout·ubuntu-24.04·액션 SHA 핀)·`tools` windows 매트릭스·`secret-scan`·`check-versions(report)` job·branch protection 문서·redaction guard

- 상태: BLOCKED
- 우선순위: P1
- Gate: CI
- 선행: T-002

## 목표

common 자체 CI를 D-18 구성으로 재편해, 소비자에게 배포할 재사용 워크플로(T-010)가 따를 하드닝 기본값을 common이 먼저 실천한다. Windows Tier 2 보증(`tools` job 매트릭스), 비밀·운영 정보 유출 guard, 버전 레지스트리 자기 검사를 CI에 넣는다.

## 고정 결정

- [설계 브리프](../plan/design-brief.md) D-18(job 목록·하드닝 항목·redaction 범위 common 전체 트리), D-03(`tools` job ubuntu+windows), D-06(액션: checkout v7·setup-node v7·setup-python v7·setup-uv v10, SHA 핀), O-17, O-23.
- [ci 조사](../survey/cross/ci-deploy.md) §1.3(하드닝 관행: ktdm SHA 핀·ubuntu-24.04, map·pinvi concurrency, pinvi timeout·head SHA checkout), §2.1(`secret-scan` 패턴·`docs-check` redaction), §4(common 자체 CI 제안·branch protection).
- [버전 매트릭스](../survey/cross/version-matrix.md) §4.4(액션 최신 major·SHA), [문서 규약 비교](../survey/cross/docs-conventions.md) §1.16(push 전 보안 감사 grep 패턴)·§2 C14(CI green 전제).
- 현재 상태(사실): `docs.yml` 1개, `actions/checkout@v6`·`setup-python@v6`, `ubuntu-latest`, `permissions`·`concurrency`·`timeout-minutes` 없음.

## 구현 범위

1. `.github/workflows/docs.yml` 재편: job `docs`(link·plan·unittest·`git diff --check`·redaction 전체 트리), `tools`(matrix `ubuntu-24.04` + Windows 러너; `python -B -X utf8`로 validator·unittest·`check_versions --self-check`·`check_spdx`), `secret-scan`(`tools/scan_secrets.py`: `dc` §1.16 패턴 + `.secret-scan-patterns` 프로젝트 패턴, staged/diff·전체 트리), `check-versions`(report; `$GITHUB_STEP_SUMMARY`).
2. 하드닝: 최상위 `permissions: contents: read`, `concurrency: ${{ github.workflow }}-${{ github.ref }}` cancel-in-progress, job별 `timeout-minutes`, `runs-on: ubuntu-24.04`, PR head SHA checkout(`ref: ${{ github.event.pull_request.head.sha || github.sha }}`), 모든 `uses:`를 40자 SHA + `# vX.Y.Z` 주석.
3. `tools/check_prod_redaction.py` + `.prod-redaction-patterns`: 사설 IP 대역·내부 호스트명 형식·운영 도메인 형식을 정규식으로만 정의(실제 운영 값을 패턴 파일에 적지 않음), common 전체 트리 검사(`docs/survey/**` 포함), 예외는 파일 단위 allowlist.
4. `docs/runbooks/branch-protection.md`: required check 이름(`docs`·`tools`·`secret-scan`), PR 필수·linear history·force-push 차단, 이름 변경 시 갱신 절차. runbook 인덱스 행 추가는 coordinator 소유 → open item.
5. `tests/test_scan_secrets.py`·`tests/test_prod_redaction.py`.

## 범위 밖

- 재사용 워크플로(`workflow_call`)·selftest·`consumers.pins.json`·`consumer-smoke`(T-010), `packages`·`python-package` job(T-101·T-302), 소비자 CI 정렬(T-403), 외부 스캐너(gitleaks 등) 채택 판단.

## 예상 변경 파일

예정 경로는 존재·실행 증거가 아니다. `.github/workflows/docs.yml`, `tools/scan_secrets.py`, `tools/check_prod_redaction.py`, `.secret-scan-patterns`, `.prod-redaction-patterns`, `tests/test_scan_secrets.py`, `tests/test_prod_redaction.py`, `docs/runbooks/branch-protection.md`, `tools/README.md`(행 추가).

## 수용 기준

- 워크플로의 모든 `uses:`가 `owner/repo@<40hex> # vX.Y.Z` 형식이고 태그 참조가 0건이다.
- 최상위 `permissions: contents: read`, `concurrency` cancel-in-progress, 모든 job에 `timeout-minutes`, 러너 `ubuntu-24.04`(Windows job 제외).
- `tools` job이 Windows에서 validator 2종·unittest·`check_versions --self-check`·`check_spdx`를 통과한다(CI 실행 링크).
- `secret-scan`이 fixture의 `api_key=…`·`BEGIN … PRIVATE KEY` 패턴을 exit 1로 잡고 저장소 본트리는 exit 0.
- redaction guard가 `docs/survey/**`를 포함한 전체 트리에서 exit 0이며, 패턴 파일에 실제 호스트·IP 값이 없다.
- `check-versions` job이 report 모드로 실행되고 step summary에 표가 붙는다.
- `branch-protection.md`의 required check 이름이 워크플로 job 이름과 일치한다.

## 검증 명령

```bash
rg -n "uses:" .github/workflows | rg -v "@[0-9a-f]{40} # v" || echo "all pinned"
rg -n "permissions:|concurrency:|timeout-minutes:|runs-on:" .github/workflows/docs.yml
python3 -B -X utf8 tools/scan_secrets.py --all; echo "exit=$?"
python3 -B -X utf8 tools/check_prod_redaction.py; echo "exit=$?"
python3 -B -X utf8 -m unittest discover -s tests -p "test_*.py" -v
```

Git Bash에서 동일. CI 결과는 GitHub Actions 실행 링크로 기록한다.

## evidence

- 각 job의 실행 링크·소요 시간·Windows 러너 Python 버전을 이 절과 `docs/journal.md`에 남긴다. 로컬에서 재현하지 못한 job은 `NOT_RUN(CI 전용)`.

## rollback 또는 release 차단 조건

- 워크플로·도구만 바뀌므로 `git revert` 1회로 원복한다.
- SHA 핀이 하나라도 풀리거나 redaction guard가 꺼진 상태로는 merge하지 않는다. `tools` Windows job이 red이면 D-03 Tier 2 위반이므로 `DONE` 금지.
