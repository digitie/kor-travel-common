# T-211 레지스트리 채널(셸 골격·로그인 페이지·playwright 기준선 템플릿) + `tools/ui_drift.py`(npm 소비자 로컬 패치 탐지)

- 상태: BLOCKED
- 우선순위: P3
- Gate: selftest
- 선행: T-210

## 목표

npm 패키지로 배포할 수 없는 "앱이 소유해야 하는 템플릿"(셸 골격·로그인 페이지·playwright 기준선)을 shadcn 레지스트리 항목으로 제공하고, npm 소비자가 `@kor-travel/ui`를 로컬에서 우회 패치했는지 탐지하는 `tools/ui_drift.py`를 만든다. 우회 패치 수는 D-28 회수 측정과 "전면 레지스트리 재검토(≥2)" 판단의 입력이다.

## 고정 결정

- ADR-007 — [ADR 색인](../adr/README.md). [브리프](../plan/design-brief.md) D-10: 레지스트리 채널은 앱이 소유해야 하는 템플릿에만, 전면 레지스트리는 Phase 5에서 "npm 소비자 우회 패치 2회 이상"일 때만 재검토. D-11: `@main` 참조 금지, 태그 불변. D-17: 앱 사본 drift 비교는 선두 주석 블록 정규화, shadcn 생성물 MIT 고지(B6). D-21: playwright 기준선 정본은 `templates/playwright.baseline.ts`(T-108). D-28: 로컬 복사본 수·우회 패치 수를 분기 보고. D-03: `tools/*.py`는 Windows Python 3.11+ stdlib에서 동작.
- 규칙 정본: [ux-guide](../standards/ux-guide.md) UX-G1(셸)·G7.1(로그인 단일 가운데 열·타이포 워드마크·오류 live region)·G7.2(오류 코드 → 한국어 맵)·G7.3(`next` 로컬 경로만), [consumer-adoption](../runbooks/consumer-adoption.md)(기준선 캡처 절차), [release](../runbooks/release.md).
- 사실 근거: [ui-components](../survey/cross/ui-components.md) §6.1(`components.json`: map·concierge·airport WIP `base-nova`, geo `radix-nova`, pinvi 없음; `registry.json` 어느 저장소에도 없음), §6.2(방식 A 장단점), §3.4 LoginForm 행(5 구현 리다이렉트 계약 3종), §4.3(AdminShell nav·LoginForm 보류 사유); [ux-patterns](../survey/cross/ux-patterns.md) C4(strip 기본 + drawer 옵션)·C15(로그인 아이콘 타일은 후속 정렬).
- 이 task에서 확정하는 선택(호스팅은 열림, 기본값): 레지스트리 JSON은 `shadcn build`로 생성해 GitHub Release 자산(`ui-vX.Y.Z` 태그, 파일명 `registry-<item>.json`)으로 올리고 소비자 `components.json` `registries`에 태그 고정 URL을 적는다. 로그인 템플릿은 공용 `LoginForm` 계약과 `fetch("/api/auth/login")` 호출·`nextPath` prop 골격을 연결하고, endpoint·IdP·세션·CSRF·rate limit은 앱 소유(T-210·T-312·ADR-015).

## 구현 범위

- `registry/registry.json` + 항목 3종: `admin-shell-skeleton`(rail 16rem/strip 전환 1024/skip link/헤더 슬롯; nav 항목은 `nav.ts` 주입점), `login-page`(G7.1~G7.3), `playwright-baseline`(`templates/playwright.baseline.ts`를 항목으로 포장; 정본은 templates). 각 파일 SPDX + `Derived-From: shadcn/ui (MIT)`(해당 시).
- `tools/ui_drift.py`(stdlib만): 입력은 소비자 체크아웃 경로 목록(`consumers.pins.json` 또는 `--path`). 탐지 (1) `patches/@kor-travel+ui*.patch` 존재 (2) `node_modules/@kor-travel/ui` 설치본 sha256이 `SHA256SUMS`와 불일치 (3) shim 파일이 `export * from "@kor-travel/ui/<x>"` 1행이 아닌 재구현 (4) 레지스트리 항목 사본 vs 원본 diff(선두 주석 블록 정규화). 출력 Markdown 표 + JSON, exit 0(report; fail 승격은 T-502 규칙).
- `tests/test_ui_drift.py` + `tests/fixtures/ui-drift/`(정상·패치·재구현·항목 drift 4 fixture), `tools/README.md` 행 추가, `.github/workflows` `tools` job에 포함(ubuntu+windows).

## 범위 밖

- 전면 레지스트리 전환(T-508), 레지스트리로 primitive 배포, 소비자 `components.json` 신설(앱 이관 task), 인증 서버·사용자 저장소·운영 비밀·앱별 인증 정책, `AdminShell` nav 정본, playwright 기준선 파일 자체(T-108). 공용 로그인 위젯 계약은 T-210에서 다룬다.

## 예상 변경 파일

예정 경로는 존재·실행 증거가 아니다.

```text
registry/registry.json
registry/admin-shell-skeleton/*.tsx  registry/login-page/*.tsx  registry/playwright-baseline/playwright.baseline.ts
tools/ui_drift.py  tools/README.md
tests/test_ui_drift.py  tests/fixtures/ui-drift/**
.github/workflows/packages.yml  (shadcn build + Release 자산)
docs/runbooks/consumer-adoption.md  (레지스트리 설치 절 — 소유자에게 요청)
THIRD_PARTY_NOTICES.md  PROVENANCE.md
```

## 수용 기준

- `npx shadcn build`가 항목 3종 JSON을 생성하고 스모크 앱에서 `npx shadcn add <태그 URL>/registry-login-page.json`이 파일을 설치·빌드된다(webpack·Turbopack).
- 설치된 로그인 템플릿이 G7.1(h1 워드마크, 항상 렌더되는 `role="alert"` 영역)·G7.3(`next`가 외부 URL이면 `/`로 치환) 테스트를 통과한다.
- `ui_drift.py`가 4 fixture에 대해 기대 판정(OK/PATCH/REIMPL/DRIFT)을 내고, 정상 fixture 결과가 빈 표다; ubuntu·windows 양쪽 `unittest` 통과.
- `--json` 출력이 D-28 보고에 쓸 `{repo, kind, path, evidence}` 필드를 갖는다.
- 항목 파일 전부 SPDX 헤더, MIT 유래 표기, `tools/check_spdx.py` 통과(도구 없으면 `NOT_RUN`).

## 검증 명령

```bash
npx shadcn build --cwd registry
python3 -B -X utf8 -m unittest discover -s tests -p "test_ui_drift.py" -v
python3 -B -X utf8 tools/ui_drift.py --path tests/fixtures/ui-drift/ok --json
python3 -B -X utf8 tools/validate_document_links.py
```

## evidence

PR 본문·`docs/journal.md`에 shadcn CLI 버전, 설치 스모크 로그, `unittest` 결과(테스트 수·OS별 exit code), 첫 실측(`consumers.pins.json` 소비자 대상, 없으면 `NOT_RUN`) 표를 남긴다.

## rollback 또는 release 차단 조건

- 레지스트리 자산은 Release 자산 삭제가 아니라 다음 태그로만 교체(태그 불변). 도구·fixture는 revert.
- 차단: 항목이 `@main` URL을 참조, 로그인 템플릿에 세션·비밀 처리 로직 포함, windows `unittest` 실패.
