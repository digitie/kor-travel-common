# ADR-008: 라이브러리·플랫폼 버전 일치 정책(floor/recommended/exceptions·lockfile 의무·판정 어휘·승격 권한)

- 상태: accepted — O-6·O-7·O-10·O-17·O-18은 기본값으로 진행
- 날짜: 2026-09-06
- 근거 문서: `docs/plan/design-brief.md` D-06·D-07·D-30·O-6·O-7·O-10, `docs/survey/cross/version-matrix.md` §1~§7·열린 질문, `docs/survey/cross/backend.md` §2.1·§5.1·§5.3, `docs/survey/inventory/kor-travel-map.md` §9, `docs/survey/inventory/kor-travel-concierge.md` §4.1, `docs/survey/inventory/kor-travel-docker-manager.md` §8-18·19, `docs/survey/README.md` §6.2(Node 22 동봉 npm 10.9.8·Python floor 3.11)

## 컨텍스트

사용자는 라이브러리/플랫폼 버전 일치 정책을 common에 포함하도록 지시했다(지시 (2)). 조사 결과 선언과 설치의 괴리가 크고(ktdm react-query `^5.28` 등), Node 20 CI가 3곳(EOL 2026-04-30), Python lockfile은 3곳에만 있으며 CI·Docker 양쪽 `--locked` 소비는 weather뿐이다(`vm` §1.1·§2.1). concierge는 lock 없이 `mcp` 2.x가 설치되어 2026-09-04 사고를 겪었고, pinvi etl은 `@main`을 참조한다. map은 npm 12.0.1 exact·Next 16.2.12 exact·Playwright 1.60 exact와 검증 스크립트로 가장 강한 핀을 쓰고, airport는 TS 7.0.2로 typescript-eslint peer 밖이다(`vm` §6). ktdm의 runtime pin registry(schema·`blocked_pinsets`·fail-close)는 형식 선례다(`vm` §7.3). Renovate 설치 여부는 미확인이다. 판정 3인 모두 coordinator의 단일 정확값 표를 기각했다.

## 결정

1. 레지스트리 `versions.json`(schema `kor-travel-common.version-registry.v1`)의 각 축은 `floor`(위반 시 fail 후보)/`recommended`/소비자 `exceptions[]{repo,key,installed,reason,until,review}`로 표현한다. 2026-09 기준선의 주요 값: Node 22.12/22.23.x, npm 10.9/11.19.x, Next 16.2/16.3.4, React 19.0/19.2.8, TypeScript 5.9/5.9.3, Tailwind 4.3.0/4.3.3, @base-ui/react 1.6/1.8.0, ESLint 9.0/10.x, Vitest 4.1, Playwright 1.60/1.63.x, Python(common) 3.11 호환, uv 0.11/0.12.x, FastAPI 0.115/0.141.x, pydantic 2.9/2.13.x, SQLAlchemy 2.0.35/2.0.52 등(전체 표는 `docs/plan/design-brief.md` D-06과 `docs/standards/versions.md`). PostgreSQL/PostGIS는 별도 트랙, provider `python-*-api` SHA는 `providers` 절에 보고만.
2. 핀 정책은 계층별 하이브리드다: common 자체 패키지는 정확 핀 + 루트 lockfile; 소비자는 선언 형식 자유이되 **lockfile 의무**(`package-lock.json` v3, `uv.lock`)와 설치본 대조. Poetry(ktdm)·requirements.txt(ktc)는 uv 전환 task.
3. `tools/check_versions.py`는 매니페스트의 `lockfiles[]`를 읽고 npm lock v3·`uv.lock`·`poetry.lock` 파서로 설치본을 `versions.json`과 대조해 `OK/BELOW_FLOOR/ABOVE_MAX/NOT_RECOMMENDED/NO_LOCK/NO_ENGINES/FLOATING_REF/BLOCKED/EXEMPT/EXEMPT_EXPIRED`로 판정한다. 출력은 Markdown 표 + JSON + `$GITHUB_STEP_SUMMARY`.
4. 강제 수준은 `report`(기본, exit 0; `FLOATING_REF`·`BLOCKED`·`EXEMPT_EXPIRED`는 `::error::` 주석) → `warn` → `fail`(exit 1) 3단이며, **모드는 common `versions.json` `consumers.<repo>.enforce`가 소유**한다. 승격 조건(해당 소비자 report 2회 연속 위반 0)을 충족하면 common PR로 전환한다. 앱 자율 선언은 기각한다.
5. `blocked[]`(예: `mcp>=2`)와 `exceptions[].until`은 필수다. 초기 예외: map npm 12.0.1·Next 16.2.12·Playwright 1.60 exact, airport TS 7.0.2(`until`: typescript-eslint peer 확장 또는 2026-12), geo·ktdm React 18.3.1(Phase 4 전), ktc maplibre-gl 6.0, map `starlette<1.0`(T-480 전). pinvi mobile Tailwind 3은 O-8 승인 전 미등록.
6. GitHub Actions: 소비자는 현행 major 유지 + SHA 핀 권고; common 내부는 checkout v7·setup-node v7·setup-python v7·setup-uv v10, SHA 핀. Renovate 미확인이므로 `templates/dependabot.yml`.

## 대안 검토

- **P1 전면 정확 핀**: 선언과 설치가 1:1이지만 봇 없이 갱신 PR을 유지할 수 없다(7개 저장소 모두 봇 없음).
- **P2 caret + lockfile만(현행 다수)**: 변경 최소이지만 매니페스트만 봐서는 일치 여부를 판단할 수 없다. lockfile 대조를 의무로 더했다.
- **단일 정확값 표 강제**: 판정 3인 모두 기각. map exact 핀·airport TS 7처럼 근거 있는 예외를 수용할 수 없다.
- **앱이 `enforce`를 자율 선언**: 지시 (2)를 완화하는 결과가 되므로 common 소유로 둔다.
- **Python floor 3.12**: airport·geo·pinvi는 3.12이나 map·weather·ktdm이 3.11이다. common은 3.11 호환으로 두고 앱 상향은 Phase 4 앱 결정(O-7).

## 결과

- 첫 단계는 격차 보고이며 어느 소비자도 즉시 CI red가 되지 않는다. fail 승격은 2회 green 후 common PR로만 이뤄진다(T-502).
- 이동 참조·차단 버전·만료 예외는 report에서도 `::error::`로 드러난다.
- 소비자는 lockfile 도입 task(geo T-440·map T-410·ktdm T-471·ktc T-450)가 선행이다.
- `check_versions`는 Windows Python stdlib에서 동작해야 하며(ADR-003) 파서별 task(T-005a·T-005b)가 남는다.

## 후속·적용 위치

- 정본: `versions.json`, `docs/standards/versions.md`(T-005)
- 도구: `tools/check_versions.py`, `tests/test_check_versions.py`(T-005·T-005a·T-005b), `tools/validate_manifest.py`(T-011)
- 워크플로: `versions-check.yml`(T-010), 소비자 삽입 T-403
- 승격·재평가: T-502(fail 승격), T-507(Node 24/26·Vitest 5·react-table 9·TS 7 재평가)
