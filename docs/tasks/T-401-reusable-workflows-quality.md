# T-401 재사용 워크플로 3단계(`node-quality.yml`·`python-quality.yml`) + selftest(concierge CI 신설용)

- 상태: BLOCKED
- 우선순위: P1
- Gate: selftest
- 선행: T-010

## 목표

common `.github/workflows/`에 `workflow_call` 재사용 워크플로 2종(`node-quality.yml`·`python-quality.yml`)을 추가하고 `workflows-selftest`가 두 워크플로를 실제 호출해 green을 증명한다. 1차 소비자는 CI가 전무한 concierge(T-451)이며, 기존 CI가 있는 앱은 "job 추가 방식"으로만 도입한다(D-18, 전면 대체 금지).

## 고정 결정

- [design-brief](../plan/design-brief.md) D-18(재사용 워크플로 단계 배포 Phase 4 = `node-quality`·`python-quality`, job `name:` 입력 개방, 태그/SHA 참조만, 하드닝 5종)·D-03(CI `ubuntu-24.04`)·D-06(Node 22 / Python 이미지 기준선).
- ADR-008(버전 정책)·ADR-002(문서 구조) — [ADR 색인](../adr/README.md). 규칙 정본: [ci-deploy](../standards/ci-deploy.md), [versions](../standards/versions.md).
- 입력·step 순서의 근거는 [ci §2.1](../survey/cross/ci-deploy.md)(`python-quality` 13 inputs, `node-quality` 12 inputs) 표를 따르되, 1차는 concierge가 필요로 하는 부분집합만 구현하고 나머지 입력은 기본값 생략 가능으로 둔다.
- 판정 보고서 [judge-migration-feasibility §4.2](../plan/design-panel/judge-migration-feasibility.md): quality 2종은 Phase 0이 아니라 T-450 직전에 배포한다(map 8·pinvi 5 required check 재구성 회피).

## 구현 범위

- `node-quality.yml`: `node-version`(기본 22)·`npm-version`(빈값이면 동봉)·`working-directory`·`workspaces`·`lockfile-integrity`·`audit-level`·`ignore-scripts`·`lint-max-warnings`(기본 0)·`typegen-check-command`·`test`·`build-env`·`job-name`. step: checkout(PR head SHA) → setup-node(cache npm) → npm 핀(조건) → `npm ci --no-audit --no-fund` → audit(차단/비차단) → typegen drift(조건) → lint → type-check → test(조건) → build.
- `python-quality.yml`: `python-version`(기본 3.12)·`working-directory`·`installer`(`uv`|`pip`)·`install-args`·`pre-install`·`ruff-format`·`mypy-targets`·`import-linter`·`alembic`·`pytest-args`·`db-image`·`db-env`·`job-name`. step: checkout → setup-python → setup-uv(조건) → pre-install → install → `ruff check` → `ruff format --check`(조건) → mypy(조건) → lint-imports(조건) → alembic(조건) → pytest.
- 하드닝 기본값: `permissions: contents: read`, `concurrency` cancel-in-progress, `timeout-minutes: 30`, `runs-on: ubuntu-24.04`, 액션 SHA 핀 + 주석 버전.
- `workflows-selftest.yml`에 fixture 2개(최소 Node 프로젝트·최소 Python 프로젝트)를 추가해 두 워크플로를 호출한다. fixture는 `tests/fixtures/workflows/` 아래에 둔다.
- `docs/standards/ci-deploy.md`의 재사용 워크플로 표에 2행 추가(호출 예시 = concierge).

## 범위 밖

`openapi-drift.yml`·`typegen-drift.yml`(T-309), `docker-build`·`aggregate-gate`·`secret-scan` 재사용 워크플로(미결, Phase 5 재평가), 각 앱의 실제 호출 PR(T-403·T-451), branch protection 갱신(앱 소유).

## 예상 변경 파일

아래는 이 task가 만들거나 고칠 예정 경로다. 예정 경로는 존재·실행 증거가 아니다.

```text
.github/workflows/node-quality.yml
.github/workflows/python-quality.yml
.github/workflows/workflows-selftest.yml
tests/fixtures/workflows/node-minimal/{package.json,package-lock.json,index.test.mjs}
tests/fixtures/workflows/python-minimal/{pyproject.toml,uv.lock,tests/test_ok.py}
docs/standards/ci-deploy.md
```

## 수용 기준

- [ ] 두 워크플로가 `on: workflow_call`만 가지며, 모든 `uses:` 액션이 40자 SHA + 주석 버전으로 핀돼 있다(`grep -E 'uses: .*@[0-9a-f]{40}'` 전수).
- [ ] `job-name` 입력이 실제 job `name:`에 반영돼 소비자가 required check 이름을 보존할 수 있다.
- [ ] `workflows-selftest` 실행 로그에 Node fixture(테스트 1개 이상 실행, 0 test 금지)·Python fixture(pytest 1개 이상 통과)가 각각 green으로 남는다.
- [ ] `ubuntu-24.04`·`permissions`·`concurrency`·`timeout-minutes`가 두 파일 모두에 있다(`actionlint` 또는 YAML 파싱으로 확인).
- [ ] `ci-deploy.md`에 입력 표와 concierge 호출 예시가 있고 `python3 -B -X utf8 tools/validate_document_links.py`가 0 오류다.

## 검증 명령

```bash
python3 -B -X utf8 tools/validate_document_links.py
python3 -B -X utf8 tools/validate_plan.py
python3 - <<'EOF'
import yaml,glob
for p in glob.glob('.github/workflows/*-quality.yml'):
    d=yaml.safe_load(open(p,encoding='utf-8')); assert 'workflow_call' in d[True] or 'workflow_call' in d['on'], p
EOF
gh workflow run workflows-selftest.yml && gh run watch   # selftest 실행(수동 dispatch)
```

## evidence

selftest run URL·run ID·두 fixture job의 테스트 수를 이 파일 하단 "실행 기록"에 남기고 `docs/journal.md`에 1항목 추가. 로컬에서 워크플로를 실행할 수 없으면 `NOT_RUN(GitHub Actions 필요)`로 적고 CI green 전 DONE 금지(D-25).

## rollback·release 차단 조건

- 두 워크플로는 common 내부 파일이라 `git revert` 1회로 원복된다. 소비자가 이미 참조 중이면(T-451 이후) 태그를 옮기지 말고 새 태그로 수정판을 낸다(태그 불변, D-11).
- selftest red 또는 액션 SHA 미핀 상태에서는 소비자 호출 PR(T-451)을 열지 않는다.
