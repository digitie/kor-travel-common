# T-002 문서 검증 도구 정정(절대 링크 금지·산문 오탐·Windows 동작·LF)·validator 회귀 테스트·docs.yml 정비

- 상태: IN_PROGRESS
- 우선순위: P0
- Gate: 도구 테스트·CI
- 선행: 없음

## 목표

canview에서 옮겨 온 검증 도구 2종이 common 규칙(절대 링크 금지·상대 링크만)을 그대로 강제하고, Windows Python(Tier 2)에서도 같은 결과를 내며, 회귀 테스트와 `docs.yml`이 그 계약을 고정하게 한다. 이번 PR에서 산출되며 리뷰 통과 후 coordinator가 `DONE` 처리한다.

## 고정 결정

- [설계 브리프](../plan/design-brief.md) D-02(상대 링크만·Python 도구 유지), D-03(`tools/*.py`는 Windows Python 3.11+ stdlib에서 동작), D-05(`validate_plan.py` 무변경), D-27.
- [canview 구조 체크리스트](../survey/cross/canview-structure-checklist.md) §4.1(문법 명세)·§4.2(35 tests 계약)·§4.3(link validator 명세)·§5 Q2(절대 접두 제거)·Q6(`.py` CRLF).
- [문서 규약 비교](../survey/cross/docs-conventions.md) §2 C11(절대 링크는 오류)·C12(실행 명령 `python3`·`uv run` 표기)·C15(`* text=auto eol=lf`).
- 착수 기준(사실, `09104ed`): `tools/validate_document_links.py`는 이미 절대 접두를 오류로 보고하고 공백 포함 target을 산문으로 건너뛴다. `tests/test_document_links.py` 5 tests, `tests/test_plan_validation.py` 35 tests. `.github/workflows/docs.yml`은 `test_plan_validation.py`만 discover하고 `permissions`·`concurrency`·`timeout`이 없다(`cv` §1.3, [ci 조사](../survey/cross/ci-deploy.md) §4).

## 구현 범위

1. `tools/validate_document_links.py`: 규칙 docstring이 [문서 유지보수 runbook](../runbooks/documentation-maintenance.md) §6·§7과 일치하는지 확인하고, 검사 범위(`docs/**`·`packages/**`·`tools/**`·`templates/**`·`tests/**`·루트)를 [tools/README.md](../../tools/README.md) 표와 맞춘다. 절대 접두 허용은 두지 않는다.
2. `tests/test_document_links.py`: 절대 링크 오류·산문 오탐 제외·fence·inline code 무시·`<>` 감싼 target·percent-encoded target·fragment 미검증 사례를 고정한다.
3. LF: `git ls-files --eol`로 추적 `.py`·`.md`·`.yml`이 `i/lf`인지 확인하고 아니면 `git add --renormalize`([실패 패턴](../runbooks/agent-failure-patterns.md) 6행).
4. `.github/workflows/docs.yml`: unittest discover 패턴을 `test_*.py`로 바꿔 두 회귀 모듈을 모두 실행하고 `python -B -X utf8` 표기로 통일한다. 하드닝(permissions·SHA 핀·Windows 매트릭스)은 T-009로 넘긴다.
5. `tools/README.md`·`docs/runbooks/agent-failure-patterns.md`의 관련 행이 도구 동작과 다르면 정정한다(내용 추가는 coordinator 소유이므로 open item으로 보고).

## 범위 밖

- `validate_plan.py` 본문 수정(D-05 무변경). 체크박스 원장 지원(`dc` §3.3-7)은 기각.
- 새 도구(`check_spdx.py`·`check_versions.py`·`validate_manifest.py`)는 T-003·T-005·T-011.
- CI job 분리·액션 SHA 핀·Windows 매트릭스는 T-009.

## 예상 변경 파일

예정 경로는 존재·실행 증거가 아니다. `tools/validate_document_links.py`, `tests/test_document_links.py`, `.github/workflows/docs.yml`, `tools/README.md`(행 정정만).

## 수용 기준

- `python3 -B -X utf8 -m unittest discover -s tests -p "test_*.py"`가 40개 이상 tests, 실패 0, skip 0으로 통과한다(0 test·skip을 통과로 집계하지 않음).
- `tools/validate_document_links.py`가 `F:/…`·`/mnt/…`·`/…` 링크를 `절대 경로 링크 금지`로 보고하고, `[미확인](Tailwind 문서에서 찾지 못했다)` 같은 산문은 링크로 세지 않는다(테스트로 고정).
- `docs/survey/**`가 검사 범위에 포함된다(출력의 `Checked N documents`에 조사 문서 수가 반영).
- Windows Python에서 `py -3 -B -X utf8 tools/validate_document_links.py`와 `validate_plan.py`가 Linux와 같은 오류 목록·exit code를 낸다(실행 evidence; 미실행이면 `NOT_RUN`).
- `git ls-files --eol tools tests docs .github`의 모든 텍스트 파일이 `i/lf`다.
- `docs.yml`이 두 회귀 모듈을 모두 실행하고 `git diff --check`가 통과한다.
- `tools/validate_plan.py`의 diff가 없다.

## 검증 명령

```bash
python3 -B -X utf8 tools/validate_document_links.py
python3 -B -X utf8 tools/validate_plan.py
python3 -B -X utf8 -m unittest discover -s tests -p "test_*.py" -v
git ls-files --eol tools tests docs .github | grep -v "i/lf" || true
git diff --stat HEAD -- tools/validate_plan.py
git diff --check
```

Git Bash에서 동일. Windows 실행 표기는 [개발 환경](../dev-environment.md).

## evidence

- T-013 재검증(2026-09-06): CI run `34023326750`에서 inline code `def fn[T](...)` 오탐으로 Linux 실패를 재현했다. inline code를 제외하고 2개 회귀 시험을 추가했다. Windows Python 3.14.3과 WSL에서 문서 오류 0·DAG 오류 0·전체 unittest 59개 성공·skip 0. `git diff --check`와 추적 파일 `i/lf` 확인 완료. 최신 CI·2인 리뷰는 후속 evidence로 닫는다.

- 테스트 수·exit code·Python 버전(`python3 --version`, Windows `py -3 --version`)을 이 절과 `docs/journal.md`에 남긴다. CI 실행은 PR의 `docs` job 링크로 남긴다.
- 리뷰가 필요한 변경(validator 규칙 변경)은 `docs/reviews/adversarial/2026-09-06-doc-validators.md`에 기록한다.

## rollback 또는 release 차단 조건

- 도구·테스트·워크플로만 바뀌므로 `git revert` 1회로 원복한다.
- 회귀 테스트가 하나라도 실패하거나 Windows 결과가 Linux와 다르면 `DONE`으로 바꾸지 않는다. 절대 링크 접두 허용을 되살리는 변경은 D-02 위반이므로 merge하지 않는다.
