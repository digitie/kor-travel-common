<!-- kor-travel-common templates/consumer-adoption-checklist.md 판 2026-09. 소비 저장소가 common을 처음 채택하거나 버전을 올릴 때 상세 task 또는 PR에 복사해 채운다. MUST는 채택 PR 머지 조건, SHOULD는 기록 후 미이행 허용. 정본: docs/standards/agent-conventions.md §11, docs/standards/versions.md, docs/runbooks/consumer-adoption.md. -->

# common 채택 체크리스트 — `<repo>` / `<app>` / `<산출물 vX.Y.Z>`

## 0. 채택 gate(착수 전)

- [ ] MUST 라이선스 gate: 저장소 루트 `LICENSE`가 GPL-3.0-or-later(또는 호환)이고 `license` 필드가 있다. pinvi는 L6(O-1), ktc·ktdm은 L8(O-2) 결정 전에는 규칙 문서·`tokens.json` 참조까지만.
- [ ] MUST lockfile: `package-lock.json`(v3)·`uv.lock`이 커밋돼 있고 CI·Docker가 `npm ci` / `uv sync --locked`로 소비한다. Poetry·`requirements.txt`는 uv 전환 task를 먼저 만든다.
- [ ] MUST 버전 대조 report: common 체크아웃에서 `python3 -B -X utf8 tools/check_versions.py <repo 경로> --repo <repo>`를 실행하고 `BLOCKED`·`FLOATING_REF`·`EXEMPT_EXPIRED`가 0이다. `BELOW_FLOOR`·`NO_ENGINES`는 예외 등록 또는 선행 task ID를 적는다.
- [ ] MUST `engines.node`(`>=22.12`) 또는 `requires-python`(`>=3.11`)이 선언돼 있다. Node 20 CI는 22로 올린다(T-403).
- [ ] SHOULD `@main`·branch 참조(패키지·워크플로·provider)가 없다(D-11).

## 1. 문서·에이전트 규약

- [ ] MUST `AGENTS.md`에 공통 절 A~I를 마커 사이에 그대로 넣고 로컬 절을 뒤에 둔다(`templates/AGENTS.common.md`).
- [ ] MUST `CLAUDE.md`는 40줄 이하 포인터다(`templates/CLAUDE.pointer.md`). 상충 시 `CLAUDE.md`를 고친다.
- [ ] MUST 링크는 저장소 상대 경로만 쓴다. 절대 경로 링크(`F:/…`, `/mnt/…`)를 제거했다.
- [ ] SHOULD `docs/README.md`(문서 지도)·`docs/dev-environment.md`(OS·worktree 프로필 선언)·`docs/adr/README.md`(다음 번호 명시)가 있다.
- [ ] SHOULD task 원장은 ID 재번호 금지·완료 시 evidence 보존·요약에 acceptance 복제 금지·비단순 task는 상세 파일 4원칙을 따른다(체크박스 원장 허용, 상태 대응표 §4).
- [ ] SHOULD 에이전트 설정 파일은 경로 비의존 형식(`templates/agent-config/`)이며 절대 경로는 로컬 override다.
- [ ] SHOULD `.github/dependabot.yml`을 `templates/dependabot.yml` 기준으로 둔다(디렉터리만 수정).

## 2. 매니페스트·시각 기준선

- [ ] MUST `kor-travel-common.lock.json`(`consumer-manifest.v1`)을 앱 디렉터리에 두고 `lockfiles[]`가 실제 lock 경로를 가리킨다(`enforce`는 두지 않는다 — common `versions.json` 소유).
- [ ] MUST(토큰·스타일·셸 변경 시) 착수 전 6폭(320/375/414/768/1024/1440) 스크린샷 기준선을 PR evidence로 확보했다(D-21). Playwright 없는 앱은 `templates/playwright.baseline.ts`(T-108).
- [ ] MUST 소비자 필수 2줄: `@import "@kor-travel/tokens/theme.css"` + `@source "../node_modules/@kor-travel/ui"`(경로는 앱 구조에 맞게; 모노레포 표는 `docs/runbooks/consumer-adoption.md`).

## 3. 채택 PR 규격(D-24)

- [ ] MUST 한 PR = 한 산출물. 프레임워크 업그레이드 PR과 분리. 4단 순서: 설정만 → 토큰만 → 컴포넌트(각 별도 PR).
- [ ] MUST PR 본문은 `templates/consumer-pr.md` 6항목을 모두 채웠다(되돌리기 명령·시각 diff 표 포함).
- [ ] MUST lock 동반 커밋, `git revert` 1회로 원복 가능.
- [ ] MUST 파일 상한(tokens 10·ui 30·py 10) 이내. 초과 시 분할.
- [ ] MUST 실행 못 한 검증은 `NOT_RUN(사유)`로 남겼고 0 test·skip을 pass로 집계하지 않았다(D-25).

## 4. 검증·리뷰·기록

- [ ] MUST 변경 범위에 맞는 gate 실행(단위·빌드·e2e·대비·UX lint) 결과와 exit code를 PR에 기록했다.
- [ ] MUST 비단순 변경은 2인 독립 리뷰(full/light는 merge 담당이 판정). P0/P1 미해결 없이 머지.
- [ ] MUST 시각 diff가 원인 불명으로 남으면 해당 단계를 revert했다(D-08 중단 조건).
- [ ] SHOULD journal에 명령·결과·NOT_RUN·소비 저장소 상태(커밋·브랜치·dirty)를 남겼다.
- [ ] SHOULD 완료 후 common `docs/architecture/adoption-readiness.md` 갱신을 common PR로 요청했다(생성물 `docs/integration-map.md`는 수기 편집 금지).

## 5. 되돌리기 리허설(첫 채택 시 1회)

- [ ] SHOULD 로컬에서 `git revert <sha>` 후 `npm ci && next build`(또는 `uv sync --locked && pytest`)가 통과함을 확인하고 결과를 journal에 남겼다.
