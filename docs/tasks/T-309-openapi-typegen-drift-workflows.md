# T-309 재사용 워크플로 2단계(`openapi-drift.yml`·`typegen-drift.yml`) + selftest

- 상태: BLOCKED
- 우선순위: P1
- Gate: selftest
- 선행: T-303, T-010

## 목표

geo·map은 `export_openapi.py --check` 워크플로, weather는 export 후 `git diff --exit-code`, airport는 export만 있고 CI가 없으며 pinvi·concierge·ktdm은 산출물 자체가 없다([oa §2.11](../survey/cross/openapi.md), [be §2.18](../survey/cross/backend.md)). 이 task는 common `.github/workflows/`에 `workflow_call` 재사용 워크플로 2종 — `openapi-drift.yml`(T-303 CLI 또는 앱 명령으로 export → `--check`/`git diff`)과 `typegen-drift.yml`(`openapi-typescript` 7.x `gen:types:check`) — 을 추가하고 `workflows-selftest`가 fixture로 두 워크플로를 실제 호출해 green과 의도적 drift의 red를 모두 증명한다. T-010(1단계 워크플로·selftest fixture·`consumers.pins.json`)이 만든 골격을 확장한다.

## 고정 결정

- [design-brief](../plan/design-brief.md) D-18(재사용 워크플로 Phase 3 = `openapi-drift`·`typegen-drift`; 소비자는 태그/SHA 참조만, job `name:` 입력 개방, 앱 기존 워크플로에 job 추가 방식, 하드닝 5종·액션 SHA 핀), D-14(M1 export+`--check`; pinvi·ktc·ktdm 파이프라인 신설은 Phase 3 앱 task; map 산출물 변경은 pin 갱신 동반), D-03(CI `ubuntu-24.04`). ADR-009·ADR-008 — [ADR 색인](../adr/README.md). 규칙 정본: [ci-deploy](../standards/ci-deploy.md), [openapi](../standards/openapi.md).
- 입력·step 순서는 [ci §2.1](../survey/cross/ci-deploy.md) `openapi-drift.yml` 행(`python-version`, `install-args`, `export-command`, `spec-paths`, `mode` `check|git-diff`)을 따르고, `working-directory`·`installer`(`uv|pip`)·`pre-install`·`job-name`을 추가한다. `typegen-drift.yml`은 `node-version`(기본 22)·`npm-version`·`working-directory`·`typegen-check-command`(기본 `npm run gen:types:check`)·`job-name`.
- cross-repo 호출은 common 공개 전제 — **열림(O-15, 사용자 확인 필요)**; 기본값 = 공개(GPL). 비공개 대안(pinned SHA로 common 체크아웃 후 스크립트 실행)은 `ci-deploy.md`에 fallback 절로 둔다([ci §2.3](../survey/cross/ci-deploy.md)).
- required check 결합: map 8·pinvi 5 required check 이름을 보존하기 위해 job 이름은 입력으로 연다([ci §2.3](../survey/cross/ci-deploy.md)); 판정 보고서 [judge-migration-feasibility §4.2](../plan/design-panel/judge-migration-feasibility.md)대로 앱 CI 전면 대체는 하지 않는다.

## 구현 범위

1. `.github/workflows/openapi-drift.yml`: checkout(PR head SHA) → setup-python → setup-uv(조건) → pre-install → install → `export-command`(기본 `python -m kortravelcommon.openapi export --app ${{ inputs.app }} --output ${{ inputs.spec-path }} --check`) 또는 `mode: git-diff`(export 후 `git diff --exit-code -- <spec-paths>`) → drift 시 `::error::`와 unified diff를 step summary에.
2. `.github/workflows/typegen-drift.yml`: checkout → setup-node(cache npm) → npm 핀(조건) → `npm ci --no-audit --no-fund --ignore-scripts` → `typegen-check-command` → drift 시 diff를 step summary에.
3. 하드닝: `permissions: contents: read`, `concurrency` cancel-in-progress, `timeout-minutes: 20`, `runs-on: ubuntu-24.04`, 모든 `uses:` 40자 SHA + 주석 버전(D-18 값: checkout v7·setup-node v7·setup-python v7·setup-uv v10).
4. selftest fixture: `tests/fixtures/workflows/python-openapi/`(T-303 fixture 앱 + 커밋된 `openapi.json`)와 `tests/fixtures/workflows/node-typegen/`(fixture 스펙 + `openapi-typescript` 7.x `gen:types`/`gen:types:check` + 커밋된 `types.ts`). `workflows-selftest.yml`에 (a) 정상 호출 green, (b) 스펙을 의도적으로 바꾼 뒤 호출 → red를 `continue-on-error: true` + 결과 단언 step으로 확인.
5. `docs/standards/ci-deploy.md` 재사용 워크플로 표에 2행 + 호출 예시(geo `check` 모드, weather `git-diff` 모드, map 3 profile은 `export-command` 3회) — standards-be 소유자와 합의. `docs/runbooks/consumer-adoption.md`의 "drift job 추가" 절 링크(runbooks 소유자와 합의).

## 범위 밖

`node-quality`·`python-quality`(T-401), 1단계 워크플로·`consumers.pins.json`·selftest 골격(T-010), 각 앱 호출 PR(T-480~T-485; pinvi·concierge·ktdm은 export 파이프라인 신설과 함께), pinvi Zod 일치 테스트(O-14, T-484), `docker-build`·`aggregate-gate`·`secret-scan` 재사용 워크플로(미결), branch protection·required check 갱신(앱 소유).

## 예상 변경 파일

예정 경로는 존재·실행 증거가 아니다.

```text
.github/workflows/openapi-drift.yml
.github/workflows/typegen-drift.yml
.github/workflows/workflows-selftest.yml                   # T-010 파일에 job 2개 추가
tests/fixtures/workflows/python-openapi/{pyproject.toml,uv.lock,app.py,openapi.json}
tests/fixtures/workflows/node-typegen/{package.json,package-lock.json,openapi.json,src/api/types.ts}
docs/standards/ci-deploy.md
docs/runbooks/consumer-adoption.md                          # drift job 절 링크(runbooks 합의)
```

## 수용 기준

- [ ] 두 워크플로가 `on: workflow_call`만 가지며 모든 `uses:`가 40자 SHA + 주석 버전이다(`grep -E 'uses: .*@[0-9a-f]{40}'` 전수, 미핀 0건).
- [ ] `job-name` 입력이 실제 job `name:`에 반영되고, `mode: check`·`mode: git-diff` 두 경로가 selftest에서 각각 실행된다.
- [ ] selftest 로그에 정상 호출 2건 green과 의도적 drift 2건(openapi·typegen)이 red로 감지된 뒤 단언 step이 green으로 끝난 기록이 있다(부정 시험 필수).
- [ ] drift 시 step summary에 unified diff가 있고 exit code가 1이다.
- [ ] `typegen-drift`가 `openapi-typescript` 7.x 정확 minor를 fixture lock에서 설치하고 `--ignore-scripts`로 `npm ci`한다.
- [ ] `ci-deploy.md`에 입력 표·호출 예시 3종(geo·weather·map)이 있고 `python3 -B -X utf8 tools/validate_document_links.py`가 0 오류다.

## 검증 명령

```bash
python3 -B -X utf8 tools/validate_document_links.py
python3 -B -X utf8 tools/validate_plan.py
grep -nE 'uses: [^ ]+@' .github/workflows/openapi-drift.yml .github/workflows/typegen-drift.yml | grep -vE '@[0-9a-f]{40}' ; echo "unpinned=$?"   # 1이면 미핀 0건
cd tests/fixtures/workflows/python-openapi && uv run python -m kortravelcommon.openapi export --app app:app --output openapi.json --check
cd ../node-typegen && npm ci --ignore-scripts && npm run gen:types:check
gh workflow run workflows-selftest.yml && gh run watch          # GitHub Actions 필요
```

## evidence

selftest run URL·run ID·정상/의도적 drift 4건의 결과를 이 파일 하단 "실행 기록"에 남기고 `docs/journal.md`에 1항목 추가. 로컬에서 워크플로를 실행할 수 없으면 `NOT_RUN(GitHub Actions 필요)`로 적고 CI green 전 DONE 금지(D-25). 소비자 호출 검증은 T-48x evidence.

## rollback·release 차단 조건

- 워크플로·fixture는 common 내부 파일이라 `git revert` 1회로 원복된다. 소비자가 참조를 시작한 뒤에는 태그를 옮기지 말고 새 태그로 수정판을 낸다(D-11 태그 불변).
- selftest에서 의도적 drift가 red로 잡히지 않으면(부정 시험 실패) 소비자 호출 PR(T-480 이후)을 열지 않는다. 액션 SHA 미핀 상태도 차단.
