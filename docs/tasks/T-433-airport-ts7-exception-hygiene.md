# T-433 airport: TS 7 예외 등록·ESLint 도입 판정·절대 링크 상대화·prod placeholder 치환·`engines` 선언

- 상태: BLOCKED
- 우선순위: P2
- Gate: CI
- 선행: T-005

## 목표

airport의 버전·위생 격차를 common 정책에 맞춘다: (1) `typescript ^7.0.2`를 `versions.json` `exceptions[]`에 `until` 포함 등록(O-6 기본값), (2) ESLint 도입 여부를 판정해 기록(도입 시 `templates/eslint/*.mjs` 조각 사용), (3) 문서의 Windows 절대 경로 링크를 상대 경로로, (4) `README.md`·`AGENTS.md`·`ci.yml`에 노출된 prod 도메인/IP를 placeholder로(소비자 opt-in, O-23), (5) `engines`·`.nvmrc` 선언(T-430 PR 1에서 이미 했으면 확인만).

## 고정 결정

- [design-brief](../plan/design-brief.md) D-06(TS 5.9.3 recommended, airport 7.0.2 예외 `until`: typescript-eslint peer 확장 또는 2026-12 재판정)·D-07(`exceptions[].until` 필수)·D-18(prod redaction 소비자 opt-in)·D-27(상대 링크)·O-6·O-23.
- ADR-008 — [ADR 색인](../adr/README.md). 정본: [versions](../standards/versions.md), [frontend-stack](../standards/frontend-stack.md)(ESLint flat 프리셋 조각), [ci-deploy](../standards/ci-deploy.md).
- 사실: TS 7.0.2는 typescript-eslint 8.69.0 peer `<6.1.0` 밖, tsconfig는 제거 옵션에 걸리지 않음 — [vm §6](../survey/cross/version-matrix.md); ESLint·Prettier·ruff 전무, 문서에 Windows 절대 경로 링크 다수, prod 도메인/IP 17/26 파일 노출 — [inv/kta §9](../survey/inventory/kor-travel-airport.md), [ci §2.2 kta](../survey/cross/ci-deploy.md).
- PR 순서: [judge-migration-feasibility §3.1 airport #5](../plan/design-panel/judge-migration-feasibility.md).

## 구현 범위

- common PR: `versions.json` `exceptions[]`에 `{repo: airport, key: typescript, installed: 7.0.2, reason, until: 2026-12-31, review}` 추가(승인 근거 = O-6 기본값 + 사용자 확인 기록).
- airport PR A(판정·선언): ESLint 도입 판정서를 `docs/adr/` 또는 `docs/decisions.md`(airport 규약)에 1건 — 도입이면 `eslint.config.mjs` + `templates/eslint/` 조각 + CI `lint` job(TS 7과 typescript-eslint peer 충돌 시 `--legacy-peer-deps` 금지, 대신 미도입 + 재판정 기한); `engines`·`.nvmrc` 확인.
- airport PR B(위생): 문서 절대 링크 → 상대 링크(`tools/validate_document_links.py`를 airport 체크아웃에 임시 실행해 0 오류 확인), prod 도메인/IP → `*.example.com`/placeholder + `*.local.md` gitignore(민감 운영 값은 로컬 파일로 이동).

## 범위 밖

TS 5.9 하향 자체(예외로 유지), ruff/mypy 도입(T-482), Tailwind·토큰(T-430·T-431), live-e2e required 여부 결정(권고만).

## 대상 저장소·브랜치·PR·되돌리기

- common: 작업 브랜치에서 `versions.json` 1 PR. airport: `codex/T-433-eslint-decision`·`codex/T-433-doc-hygiene` 2 PR(Draft), `main`에서 분기.
- 되돌리기 = 각 PR `git revert` 1회. placeholder 치환을 되돌리면 prod 값이 다시 노출되므로 revert 전 검토 필수.

## 예상 변경 파일

아래는 이 task가 만들거나 고칠 예정 경로다. 예정 경로는 존재·실행 증거가 아니다.

```text
kor-travel-common: versions.json
frontend/eslint.config.mjs, frontend/package.json, .github/workflows/ci.yml   # 도입 판정 시
docs/adr/NNN-eslint-adoption.md 또는 docs/decisions.md
README.md, AGENTS.md, docs/**/*.md                                              # 절대 링크·placeholder
.gitignore                                                                     # *.local.md
frontend/.nvmrc
```

## 수용 기준

- [ ] `check_versions` report에서 airport TypeScript 행이 `EXEMPT`(만료 전)로 표시되고 `until`이 비어 있지 않다.
- [ ] ESLint 판정이 문서로 남고, 도입한 경우 CI `lint` job green + `--max-warnings=0`; 미도입이면 재판정 기한이 `versions.json` 예외 `review`와 같은 날짜.
- [ ] airport 문서에 `F:/`·`/mnt/`·`C:\` 링크 0건(`validate_document_links.py` 임시 실행 0 오류).
- [ ] `grep -rnE '<실제 prod 도메인/IP 패턴>'`(패턴은 airport `*.local.md`에만 기록) 결과 0건, `.prod-redaction-patterns` 또는 동등 파일이 있으면 `docs-check` opt-in 가능 상태.
- [ ] frontend CI green.

## 검증 명령

```bash
# kor-travel-common
python3 -B -X utf8 tools/check_versions.py --manifest ../kor-travel-airport/frontend/kor-travel-common.lock.json
python3 -B -X utf8 tests/test_check_versions.py    # 또는 unittest discover
# kor-travel-airport
python3 -B -X utf8 ../kor-travel-common/tools/validate_document_links.py .   # 절대 링크 0
npm --prefix frontend ci && npm --prefix frontend run lint   # 도입 시
```

## evidence

common PR·airport PR 2개 URL, `check_versions` 표, 링크 검사 출력, 판정 문서 링크를 이 파일 "실행 기록"·`docs/journal.md`에.

## rollback·release 차단 조건

- 예외 `until` 없이 등록하면 `EXEMPT_EXPIRED`가 아니라 검증 실패이므로 등록 자체를 막는다(check_versions 테스트).
- placeholder 치환 PR은 민감 값이 커밋 이력에 남지 않도록 새 값만 추가하고, 노출 이력 정리는 airport 소유 판단으로 남긴다.
