# T-010 재사용 워크플로 1단계(`versions-check`·`contrast-check`·`docs-check`) + `workflows-selftest` fixture + `consumers.pins.json` + consumer-smoke

- 상태: IN_PROGRESS
- 우선순위: P1
- Gate: selftest
- 선행: T-005, T-009, T-101, T-103

## 목표

소비자 저장소가 `uses: digitie/kor-travel-common/.github/workflows/<name>.yml@<tag|sha>`로 호출할 1단계 재사용 워크플로 3종을 만들고, fixture 기반 selftest와 스모크 실행기 검증을 common에서 완료한다. 승인된 실제 소비자 2곳의 dispatch 성공은 T-010a가 별도로 소유한다(ADR-014).

## 고정 결정

- [설계 브리프](../plan/design-brief.md) D-18(1단계 `versions-check`·`contrast-check`·`docs-check`, `consumer-smoke` dispatch+주간·`consumers.pins.json`, 소비자는 태그/SHA 참조·job `name:` 입력 개방·앱 워크플로에 job 추가 방식), D-07(`enforce`는 `versions.json` 소유), D-13(대비 검사 report 기본), O-15(공개 전제 + 체크아웃 fallback 문서).
- [ci 조사](../survey/cross/ci-deploy.md) §2.1(워크플로 후보·입력·하드닝 기본값), §2.3(cross-repo 호출 제약·required check 이름 결합·`@main` 금지), §4(`workflows-selftest` fixture·`consumer-smoke` pinned SHA), [버전 매트릭스](../survey/cross/version-matrix.md) §7.3(`consumers.pins.json` 형식은 ktdm 핀 레지스트리 계열).
- [실패 패턴](../runbooks/agent-failure-patterns.md) "재사용 워크플로 호출 실패" 행.
- 암묵 의존(사실): `contrast-check.yml`은 `tools/kt_contrast.py`(T-103), `consumer-smoke`의 tarball 설치는 `packages/tokens`(T-101)를 전제한다. T-101·T-103 완료 후 착수한다. [ADR-013](../adr/013-package-release-execution-contract.md)에 따라 미구현·설치 생략을 green으로 집계하지 않는다.

## 구현 범위

1. `.github/workflows/versions-check.yml`(`workflow_call`): inputs `name`, `repo`, `lockfiles`(JSON 목록), `common-ref`; common 체크아웃(태그/SHA) → `check_versions.py` report → step summary.
2. `.github/workflows/docs-check.yml`: inputs `link-check`, `redaction-patterns-file`, `redaction-scope`, `task-ledger`; common 도구를 호출 저장소에서 실행.
3. `.github/workflows/contrast-check.yml`: inputs `override-css`, `baseline`, `dark`; T-103의 실제 검사기를 호출하며 정상·대비 미달 fixture를 모두 실행한다.
4. `tests/fixtures/node-app`·`tests/fixtures/python-app`(최소 `package.json`+lock v3, `pyproject.toml`+`uv.lock`) + `.github/workflows/workflows-selftest.yml`(PR이 `.github/**`·`tools/**`를 바꿀 때 세 워크플로를 `workflow_call`로 호출).
5. `consumers.pins.json`(`"schema": "kor-travel-common.consumer-pins.v1"`, `{role, url, revision(sha), path, package, approval}`; tokens는 map·weather, UI는 map·pinvi admin(L6 완료) 또는 airport) + `.github/workflows/consumer-smoke.yml`(`workflow_dispatch`; 주간 실행 활성화는 T-010a 실제 검증 뒤 별도 PR. pinned SHA 체크아웃 → `npm ci` → 후보 tarball 필수 설치 → `type-check` + `next build` webpack·Turbopack; required check 아님).
6. `docs/standards/ci-deploy.md`의 호출 예시·fallback(비공개 시 체크아웃 방식)은 standards-be 문서에 위임하고 여기서는 selftest 결과만 남긴다.

## 범위 밖

- 2단계(`openapi-drift`·`typegen-drift`, T-309)·3단계(`node-quality`·`python-quality`, T-401), 소비자 저장소에 job을 추가하는 일(T-403), `actionlint` 채택 판단.

## 예상 변경 파일

예정 경로는 존재·실행 증거가 아니다. `.github/workflows/versions-check.yml`, `docs-check.yml`, `contrast-check.yml`, `workflows-selftest.yml`, `consumer-smoke.yml`, `consumers.pins.json`, `tests/fixtures/node-app/*`, `tests/fixtures/python-app/*`, `tests/test_consumer_pins.py`.

## 수용 기준

- 세 재사용 워크플로가 `on: workflow_call`이고 `name`·`common-ref` 입력을 받으며 T-009 하드닝 기본값(permissions·timeout·ubuntu-24.04·SHA 핀)을 갖는다.
- `workflows-selftest`가 fixture 2종에서 green이고, `versions-check`는 fixture의 `BELOW_FLOOR`를 report(exit 0)로 표시한다.
- `consumers.pins.json`의 `revision`이 40자 SHA이고 `tests/test_consumer_pins.py`가 스키마·SHA 형식을 고정한다.
- `consumer-smoke` 실행기의 입력 pin·자산 digest·승인 조건·설치 실패/누락 처리를 common fixture에서 검증한다. 로컬 tarball을 실제 설치하는 정상 fixture와 의도적 digest/승인/설치 실패 fixture가 있어야 한다. 실제 소비자 2곳 dispatch·주간 활성화는 T-010a에 남기고 이 task의 성공으로 세지 않는다. 실행기는 자산·도구 부재나 미승인 입력을 실패로 종료하며 L6 미완료 pinvi를 제외한다.
- 어떤 예시·문서에도 `@main` 참조가 없다.

## 검증 명령

```bash
rg -n "workflow_call" .github/workflows/*.yml
rg -n "uses:.*@main" .github/workflows docs/standards docs/runbooks templates || echo "no moving workflow ref"
python3 -B -X utf8 -m unittest discover -s tests -p "test_consumer_pins.py" -v
python3 -B -X utf8 -c "import json;d=json.load(open('consumers.pins.json',encoding='utf-8'));print(d['schema'],len(d['sources']))"
```

Git Bash에서 동일. selftest·consumer-smoke 결과는 Actions 실행 링크로 남긴다.

## evidence

- 구현 기준선(로컬 branch `codex/t010-reusable-workflows`):
  - `versions-check.yml`이 node·Python fixture를 고정 common ref로 검사하고 각각 `BELOW_FLOOR`를 report(exit 0)로 출력한다. node는 React 18.3.1, Python은 Python 3.10/FastAPI 0.114.0을 의도적으로 사용한다.
  - `contrast-check.yml`은 canonical tokens와 정상·의도적 미달 override를 report 모드로 실행한다. `docs-check.yml`은 link·redaction scope·선택 task ledger를 caller checkout에서 실행한다.
  - `consumer_smoke.py`와 `tests/test_consumer_pins.py`가 정상 tarball 실제 npm 설치, digest 불일치, 승인 거부, 누락 자산, engine-strict 설치 실패를 재현한다. `consumers.pins.json`은 map·weather tokens와 map·airport UI의 조사 기준 SHA만 승인하고 L6 미완료 pinvi는 제외한다.
- 로컬 검증: `python -B -X utf8 -m unittest discover -s tests -p 'test_*.py'` 337 tests OK(2026-09-09), `validate_document_links.py` 520 documents/2568 targets 오류 0, `validate_plan.py` 106 tasks 오류 0, `check_spdx.py` 68 files 오류 0, `check_prod_redaction.py --all` 669 files/발견 0, `git diff --check` OK.
- 최종 후보 `f220bb5`(tree `68c8a8f19517dacf0a53d86e1efb5d85e22f464f`, 기능 후보 `54b5ac4`)의 focused `test_consumer_pins` 10건·`test_check_versions` 88건과 전체 unittest 337건이 Windows에서 모두 성공했다. `npm pack ./packages/tokens` 실제 산출물은 common artifact repository와 정본 GPL `LICENSE`, `NOTICE`, `THIRD_PARTY_NOTICES.md`를 통과했고, 미등록 repo fail-closed와 common selftest fixture의 base/caller/common 저장소 일치 조건을 회귀 시험·selftest로 확인했다.
- 기능 후보의 `workflows-selftest`는 [Actions run 34288106079](https://github.com/digitie/kor-travel-common/actions/runs/34288106079), docs·tools·packages·check-versions·secret-scan은 [Actions run 34288105963](https://github.com/digitie/kor-travel-common/actions/runs/34288105963)에서 모두 성공했다. 상세 리뷰 기준은 [최종 manifest](../reviews/adversarial/evidence/2026-09-09-t010-final-manifest.md)이며 docs-only closure 후보의 최신 CI와 두 독립 reviewer 최종 판정을 추가한다. 실제 map·weather consumer dispatch, 주간 활성화, 소비자 build/e2e, npm/PyPI 게시·Release는 `NOT_RUN(외부 소비자·사용자 범위; T-010a)`로 유지한다.

## rollback 또는 release 차단 조건

- 워크플로·fixture만 바뀌므로 `git revert` 1회로 원복한다.
- selftest red 상태로는 소비자에게 호출 예시를 배포(T-403)하지 않는다. 재사용 워크플로의 job `name:` 입력이 없으면 map 8·pinvi 5 required check가 깨지므로 merge 차단.
