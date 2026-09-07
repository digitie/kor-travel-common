# T-403 공통 CI 정렬: Node 20→22(ktdm·geo·wx)·액션 SHA 핀·`check_versions` report job 삽입·매니페스트 커밋(7 저장소)

- 상태: BLOCKED
- 우선순위: P1
- Gate: 각 저장소 CI
- 선행: T-010, T-011

## 목표

7개 소비 저장소에 (1) `kor-travel-common.lock.json` 매니페스트 초안(T-011) 커밋, (2) common `versions-check.yml` 재사용 워크플로 호출 job(report 모드) 삽입, (3) CI Node 20을 22로 상향(ktdm·geo·weather), (4) GitHub Actions 참조 SHA 핀을 저장소당 1 PR로 적용한다. 코드·스타일은 건드리지 않으므로 L6/L8과 무관하게 진행할 수 있다(규칙 참조 단계, D-16).

## 고정 결정

- [design-brief](../plan/design-brief.md) D-06(Node floor 22.12, Node 20 CI는 이 task)·D-07(report 모드 기본, `enforce`는 common 소유)·D-18(태그/SHA 참조만, job 추가 방식, 운영 호출 job required 금지 권고)·D-19(매니페스트 필드).
- ADR-008·ADR-010 — [ADR 색인](../adr/README.md). 정본: [versions](../standards/versions.md), [ci-deploy](../standards/ci-deploy.md), [consumer-adoption runbook](../runbooks/consumer-adoption.md), [consumer PR 템플릿](../../templates/consumer-pr.md).
- 사실 근거: CI Node 20 사용처 = ktdm·geo·weather, Node 20 EOL 2026-04-30 — [vm §1.1·§3.2](../survey/cross/version-matrix.md); 액션 SHA 핀 선례 = ktdm — [ci §1.3](../survey/cross/ci-deploy.md); 앱별 도입 변경점 — [ci §2.2](../survey/cross/ci-deploy.md).
- 판정 보고서 [judge-migration-feasibility §4.2](../plan/design-panel/judge-migration-feasibility.md): Phase 0 재사용 워크플로는 `versions-check`·`contrast-check`만; quality 2종은 T-401.

## 구현 범위

| 저장소 | 이 PR에서 할 것 | 하지 않을 것 |
|---|---|---|
| map | 매니페스트(`packages/kor-travel-map-admin/frontend/` 기준 lockfiles 2종) + `versions-check` job 추가 | required check 8개 이름 변경, npm 12.0.1 강제 변경(예외 등록으로 처리) |
| pinvi | `apps/web`·`apps/api` 매니페스트 + job | aggregate-ci 규칙 변경, L6 관련 파일 |
| airport | 매니페스트 + job + `engines` 없음 상태 유지(선언은 T-433) | `live-e2e` 변경 |
| geo | 매니페스트 + job + CI Node 20→22 | `uv.lock` 도입(T-440), pre-commit |
| weather | 매니페스트 + job + CI Node 20→22 | vitest/mypy job 추가(T-460) |
| ktdm | 매니페스트 + job + CI Node 20→22(기존 SHA 핀 유지) | Next/React 업그레이드(T-470) |
| concierge | 매니페스트만(CI 없음) | 워크플로 파일(T-451) |

액션 SHA 핀은 이미 핀된 ktdm을 제외한 6곳에서 `actions/checkout`·`setup-node`·`setup-python`·`setup-uv` 등 현행 major를 유지한 채 SHA + 주석 버전으로 바꾼다(D-06 "소비자: 현행 major 유지 + SHA 핀 권고").

## 범위 밖

`enforce: warn/fail` 승격(T-502), 라이브러리 버전 상향(T-413·T-460·T-470 등), Python lockfile 도입(T-440·T-450·T-471), 프로덕션 도메인 redaction(소비자 opt-in, O-23).

## 대상 저장소·브랜치·PR·되돌리기

- 7개 PR. 브랜치는 각 저장소 `origin/main`에서 `agent/<agent>-T-403-ci-align`(앱 로컬 접두 규칙이 있으면 그 접두 사용, 예: airport `codex/`).
- PR 본문은 `templates/consumer-pr.md`(검사 결과·되돌리기 명령). 되돌리기 = `git revert <merge-sha>` 1회; 매니페스트 파일은 삭제돼도 다른 파일이 참조하지 않는다.
- 머지 순서: geo·weather·ktdm(Node 22 상향이 있어 CI 신호가 큼) → map·pinvi → airport → concierge.

## 예상 변경 파일

아래는 이 task가 만들거나 고칠 예정 경로다. 예정 경로는 존재·실행 증거가 아니다.

```text
<repo>/kor-travel-common.lock.json                 # 모노레포는 앱 디렉터리(pinvi apps/web·apps/api, map admin frontend)
<repo>/.github/workflows/ci.yml                    # Node 22, SHA 핀, versions-check job
kor-travel-common: consumers.pins.json             # 7 저장소 머지 SHA 갱신
kor-travel-common: docs/integration-map.md         # tools/collect_manifests.py 재생성(수기 편집 금지)
```

## 수용 기준

- [ ] 7 저장소 각각에 `schema: kor-travel-common.consumer-manifest.v1` 매니페스트가 있고 `python3 -B -X utf8 tools/validate_manifest.py <path>`가 0 오류다.
- [ ] 6 저장소(concierge 제외) CI에 `versions-check` job이 report 모드로 실행돼 `$GITHUB_STEP_SUMMARY`에 판정 표가 남고, `FLOATING_REF`·`BLOCKED`·`EXEMPT_EXPIRED` 외 항목은 job을 실패시키지 않는다.
- [ ] geo·weather·ktdm CI의 `node-version`이 22이고 기존 job이 green이다(Node 22에서 새로 red가 나면 원인 기록 후 해당 저장소 PR만 보류).
- [ ] 소비자 워크플로의 `uses:` 참조가 SHA 핀이며 common 참조는 태그 또는 SHA다(`@main` 0건).
- [ ] map·pinvi required check 이름이 머지 전후 동일하다(branch protection 화면 캡처 또는 `gh api` 출력).

## 검증 명령

```bash
# common
python3 -B -X utf8 tools/validate_manifest.py ../kor-travel-map/packages/kor-travel-map-admin/frontend/kor-travel-common.lock.json
python3 -B -X utf8 tools/check_versions.py <consumer-repo-root> --manifest <app-dir>/kor-travel-common.lock.json --mode report   # lock path는 저장소 루트 기준
python3 -B -X utf8 tools/collect_manifests.py && git diff --stat docs/integration-map.md
# 각 소비 저장소
grep -nE 'uses: .*@(main|v[0-9]+)$' .github/workflows/*.yml   # 0건이어야 함
gh pr checks <pr-number>
```

## evidence

PR 7개 URL·머지 SHA·`versions-check` step summary 캡처를 이 파일 "실행 기록"에, 요약을 `docs/journal.md`에 남긴다. `consumers.pins.json` 갱신 커밋이 evidence의 일부다. 실행 못 한 저장소는 `NOT_RUN(사유)`.

## rollback·release 차단 조건

- 각 저장소 PR은 독립 revert 단위다. Node 22 상향으로 red가 나면 그 저장소만 revert하고 `versions.json` `exceptions[]`에 `until` 포함 예외를 등록한 뒤 재시도한다.
- 매니페스트가 잘못돼 `check_versions`가 파싱 실패하면 report 모드라도 `::error::`가 남으므로, 파싱 실패 상태로는 T-502 승격 후보에 넣지 않는다.
