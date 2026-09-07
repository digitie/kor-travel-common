# T-009 common CI 하드닝(permissions·concurrency·timeout·ubuntu-24.04·액션 SHA 핀)·`tools` windows 매트릭스·`secret-scan`·`check-versions(report)` job·branch protection 문서·redaction guard

- 상태: IN_PROGRESS
- 우선순위: P1
- Gate: CI
- 선행: T-002, T-003

## 목표

common 자체 CI를 D-18 구성으로 재편해, 소비자에게 배포할 재사용 워크플로(T-010)가 따를 하드닝 기본값을 common이 먼저 실천한다. Windows Tier 2 보증(`tools` job 매트릭스), 비밀·운영 정보 유출 guard, 버전 레지스트리 자기 검사를 CI에 넣는다.

## 고정 결정

- [설계 브리프](../plan/design-brief.md) D-18(job 목록·하드닝 항목·redaction 범위 common 전체 트리), D-03(`tools` job ubuntu+windows), D-06(액션: checkout v7·setup-node v7·setup-python v7·setup-uv v10, SHA 핀), O-17, O-23.
- [ci 조사](../survey/cross/ci-deploy.md) §1.3(하드닝 관행: ktdm SHA 핀·ubuntu-24.04, map·pinvi concurrency, pinvi timeout·head SHA checkout), §2.1(`secret-scan` 패턴·`docs-check` redaction), §4(common 자체 CI 제안·branch protection).
- [버전 매트릭스](../survey/cross/version-matrix.md) §4.4(액션 최신 major·SHA), [문서 규약 비교](../survey/cross/docs-conventions.md) §1.16(push 전 보안 감사 grep 패턴)·§2 C14(CI green 전제).
- 착수 기준(82dec2b의 사실): `docs.yml` 1개, `actions/checkout@v6`·`setup-python@v6`, `ubuntu-latest`, `permissions`·`concurrency`·`timeout-minutes` 없음.

## 구현 범위

docs·tools(두 OS)·secret-scan·check-versions job은 [ci-deploy §9](../standards/ci-deploy.md#9-common-자체-ci)에 따라 PR과 main·codex/release-* push에서 실행한다. release push의 github.sha를 checkout하고 필수 job을 path/PR 조건으로 생략하지 않는다. run·산출물 source SHA를 기록한다. 후보 보존 전에 이 실행 경로를 포함해야 한다.

1. `.github/workflows/docs.yml` 재편: job `docs`(link·plan·unittest·`git diff --check`·redaction 전체 트리), `tools`(matrix `ubuntu-24.04` + Windows 러너; `python -B -X utf8`로 validator·unittest·`check_versions --self-check`·`check_spdx`), `secret-scan`(`tools/scan_secrets.py`: `dc` §1.16 패턴 + `.secret-scan-patterns` 프로젝트 패턴, staged/diff·전체 트리), `check-versions`(report; `$GITHUB_STEP_SUMMARY`).
2. 하드닝: 최상위 `permissions: contents: read`, `concurrency: ${{ github.workflow }}-${{ github.ref }}` cancel-in-progress, job별 `timeout-minutes`, `runs-on: ubuntu-24.04`, PR head SHA checkout(`ref: ${{ github.event.pull_request.head.sha || github.sha }}`), 모든 `uses:`를 40자 SHA + `# vX.Y.Z` 주석.
3. `tools/check_prod_redaction.py` + `.prod-redaction-patterns`: 사설 IP 대역·내부 호스트명 형식·운영 도메인 형식을 정규식으로만 정의(실제 운영 값을 패턴 파일에 적지 않음), common 전체 트리 검사(`docs/survey/**` 포함), 예외는 파일 단위 allowlist.
4. `docs/runbooks/branch-protection.md`: required check 이름(`docs`·`tools`·`secret-scan`), PR 필수·linear history·force-push 차단, 이름 변경 시 갱신 절차. 실제 matrix check 이름은 runbook에서 대조하며 인덱스에 연결한다. 원격 ruleset 설정은 적용하지 않는다.
5. `tests/test_scan_secrets.py`·`tests/test_prod_redaction.py`, `tests/fixtures/version-report`의 비설치용 report 입력.

## 범위 밖

- 재사용 워크플로(`workflow_call`)·selftest·`consumers.pins.json`·`consumer-smoke`(T-010), `packages`·`python-package` job(T-101·T-302), 소비자 CI 정렬(T-403), 외부 스캐너(gitleaks 등) 채택 판단.

## 예상 변경 파일

예정 경로는 존재·실행 증거가 아니다. `.github/workflows/docs.yml`, `tools/scan_secrets.py`, `tools/check_prod_redaction.py`, 공통 입력 선택기 `tools/_scan.py`, `.secret-scan-patterns`, `.prod-redaction-patterns`, `tests/test_scan_secrets.py`, `tests/test_prod_redaction.py`, `docs/runbooks/branch-protection.md`, `tools/README.md`(행 추가).

## 수용 기준

- main·codex/release-* push 사건의 모든 필수 job 선택을 검증하고, common의 임시 release 검증 branch에 코드 변경 없는 검증 commit을 push한 실제 CI run으로 head/source SHA 일치를 확인한다. 태그·GitHub Release 생성은 필요 없다. 이 검증 branch는 PR 또는 보존 ref로 commit 도달성을 확보하고 작업 뒤 정리한다. 검사기를 통과한 PR head 결과를 다른 merge SHA 결과로 대신 기록하지 않는다.

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

첫 실제 [PR CI](https://github.com/digitie/kor-travel-common/actions/runs/34069260693)와 [release push CI](https://github.com/digitie/kor-travel-common/actions/runs/34069314480)에서 두 실패를 확인했다. report는 이전 step의 summary에 source가 있다고 잘못 가정했고, Windows Python 3.11.9는 TEMP의 짧은 경로 별칭과 해석한 긴 경로를 상대화하다 실패했다. GitHub의 [변수 문서](https://docs.github.com/en/actions/reference/workflows-and-actions/variables)(조회일 2026-09-07)의 step별 summary 경로 계약에 맞춰 report step 자체에서 source를 확인·기록했다. manifest의 기준 경로도 resolve하고 별칭 경로 회귀 시험이 수정 전 실패함을 재현했다. 수정 후 실제 CI 결과는 뒤 검증으로 구분한다.

2026-09-07 재개: PR #4 merge `82dec2b939885863100802997f9e7548dffd3c9a`와 main CI 34066384346 성공을 확인했다. [PR #5](https://github.com/digitie/kor-travel-common/pull/5)에서 구현한다. 공식 [checkout v7.0.1](https://github.com/actions/checkout/releases/tag/v7.0.1)·[setup-python v7.0.0](https://github.com/actions/setup-python/releases/tag/v7.0.0)의 release/tag API를 조회해 workflow의 40자 commit과 일치함을 확인했다(조회일 2026-09-07). 실제 값은 workflow가 정본이다.

검사기와 CI를 구현했고 [조사 보안 정정](../survey/README.md#9-t-009-보안-정정)을 기록했다. 전체 현재 트리 319파일에서 비밀·운영 주소 발견 0, 명시적 예외 0이며 SPDX 18파일 오류 0이다. Git index/commit 스냅샷·정책 읽기, 값 비공개, 실패 종료와 주소 경계를 회귀 검증한다. 첫 시험에서 Windows Git의 금지 파일명 생성 실패·fixture 패턴의 자기 일치·내부 호스트 뒤 문장부호 누락을 확인하고, 경로 파서 직접 시험·정규식 수정으로 대응했다. Windows Python 3.14.3에서 전체 131 tests·skip 0(29.892초), WSL Python 3.11.15에서 131 tests·skip 0(13.107초)을 새로 실행해 성공했다. link260문서·2107대상과 plan101·diff 오류 0이다. 실제 CI·임시 release push·두 독립 리뷰는 아직 수행 전이며 완료로 판정하지 않는다.

2026-09-06 종료 재검토: 필수 Windows tools job이 T-003의 check_spdx.py를 실행하므로 해당 task를 내부 선행으로 명시했다. T-003이 DONE이 되기 전에는 직접 지정받아도 착수하지 않는다. T-005 전체 완료는 현재 checker 자체 검사의 기술적 선행과 구분하며 기본 실행 대기열은 T-003 → T-005 → T-009를 유지한다.

- 각 job의 실행 링크·소요 시간·Windows 러너 Python 버전을 이 절과 `docs/journal.md`에 남긴다. 로컬에서 재현하지 못한 job은 `NOT_RUN(CI 전용)`.

## rollback 또는 release 차단 조건

- 워크플로·도구만 바뀌므로 `git revert` 1회로 원복한다.
- SHA 핀이 하나라도 풀리거나 redaction guard가 꺼진 상태로는 merge하지 않는다. `tools` Windows job이 red이면 D-03 Tier 2 위반이므로 `DONE` 금지.
