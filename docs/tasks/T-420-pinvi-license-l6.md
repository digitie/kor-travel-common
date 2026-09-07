# T-420 pinvi: L6 결정 반영 PR(루트 LICENSE·README/AGENTS 정합·`apps/api` pyproject·maplibre 문서 정정)

- 상태: BLOCKED
- 우선순위: P0
- Gate: docs
- 선행: T-020
- 외부 선행: T-020 common 결정 완료(2026-09-08). 실제 pinvi 반영은 이 저장소 밖의 PR이다.

## 목표

T-020에서 기록된 사용자 결정(기본값: 공개 + `GPL-3.0-or-later`)을 pinvi 저장소 1 PR로 반영해 차단 B1을 해제한다. 이 PR이 머지되기 전에는 pinvi의 어떤 파일도 common으로 추출하지 않고, common 코드(tokens·ui·py)를 pinvi가 소비하지도 않는다.

## 고정 결정

- [design-brief](../plan/design-brief.md) D-16(pinvi admin tokens/ui 1차는 L6 완료 조건)·D-17(pinvi는 L6 전 추출 금지 B1; 전 앱 `license` 필드 L11)·O-1 채택값(공개 + GPL-3.0-or-later, 1 PR).
- ADR-004(라이선스·출처 gate)·ADR-010 — [ADR 색인](../adr/README.md). 정본: [licensing](../standards/licensing.md).
- 사실: 루트 `LICENSE` 없음, README "비공개(사내)" vs AGENTS "공개" 상충, `apps/api/pyproject.toml` MIT, `docs/integrations/maplibre-vworld.md:23` 라이선스 표기 오류, map 이식 파일 35+(P1)·geo 이식(P2)·GPL tgz 3(P3)·`python-kasi-api` 의존 — [lic §2.1·§2.2 D4·D5·§3.6·§3.7 L6·§4 B1](../survey/cross/licensing.md), [inv/pinvi §9](../survey/inventory/pinvi.md), [cm §4.1 B1](../survey/commonality-matrix.md).
- PR 순서: [judge-migration-feasibility §3.1 pinvi #0](../plan/design-panel/judge-migration-feasibility.md)(3파일 + 문서 1).

## 구현 범위

- 루트 `LICENSE`에 GPL-3.0 전문(674행) 추가, `NOTICE` 또는 README 라이선스 절에 저작권자·연락처.
- `README.md`의 "비공개(사내)" 문구를 결정에 맞게 정정하고 `AGENTS.md`와 일치시킨다.
- `apps/api/pyproject.toml` `license` 필드를 `GPL-3.0-or-later`로, `apps/web/package.json`·`apps/etl/pyproject.toml` 등 모든 패키지 매니페스트에 `license` 필드 추가(L11).
- `docs/integrations/maplibre-vworld.md:23`의 tgz 라이선스 표기를 원천(GPL-3.0)에 맞게 정정(L7은 maplibre-vworld-react 측 별도).
- 사용자가 기본값과 다른 결정(사내 비공개 유지)을 내리면 이 task는 "GPL 코드 P1~P3 제거 또는 별도 허가 재선언" 계획서로 바뀌며 common 소비 트랙(T-421·T-422·T-484)은 취소된다 — 이 경우 open item으로 coordinator에 보고.

## 범위 밖

pinvi 코드 변경, 벤더 tgz 재생성(L7, maplibre-vworld-react 소유), 모바일 앱 스토어 라이선스 고지, common 측 `PROVENANCE.md` 기록(추출이 일어나는 T-2xx에서).

## 대상 저장소·브랜치·PR·되돌리기

- 저장소 pinvi(`F:/dev/kor-travel-common-survey/pinvi`는 shallow clone 조사본이므로 작업은 정본 체크아웃에서), 브랜치 `docs/T-420-license-l6`(pinvi 규칙 `docs/` 접두), `origin/main`에서 분기. PR 1개(docs 라벨).
- 되돌리기 = `git revert <merge-sha>`. 되돌리면 B1이 다시 걸리므로 T-421 이후 PR도 함께 revert해야 한다(순서 역순).

## 예상 변경 파일

아래는 이 task가 만들거나 고칠 예정 경로다. 예정 경로는 존재·실행 증거가 아니다.

```text
LICENSE
NOTICE 또는 README.md(라이선스 절)
README.md, AGENTS.md
apps/api/pyproject.toml, apps/etl/pyproject.toml, apps/web/package.json, packages/*/package.json
docs/integrations/maplibre-vworld.md
```

## 수용 기준

- [ ] 루트 `LICENSE`가 GPL-3.0 전문이고 `README.md`·`AGENTS.md`의 공개/비공개 서술이 같다.
- [ ] 모든 `pyproject.toml`·`package.json`에 `license` 필드가 있고 값이 루트와 같다(`grep -L '"license"' --include=package.json -r .` 0건).
- [ ] `docs/integrations/maplibre-vworld.md`의 tgz 라이선스 표기가 원천과 일치한다.
- [ ] common `docs/architecture/adoption-readiness.md`의 pinvi gate 행이 "L6 완료(PR #, 머지 SHA)"로 갱신됐다(T-012 생성기 또는 수기).
- [ ] pinvi CI(web·api·etl·aggregate)가 green이다(문서 변경만이라 red면 무관 원인).

## 검증 명령

```bash
# pinvi
head -3 LICENSE && wc -l LICENSE
grep -rn --include=package.json --include=pyproject.toml -E '"license"|^license' apps packages
git diff --check
# kor-travel-common
python3 -B -X utf8 tools/validate_document_links.py
```

## evidence

PR URL·머지 SHA·T-020 결정 링크를 이 파일 "실행 기록"과 `docs/journal.md`에 남긴다. 외부 PR evidence 전에는 BLOCKED를 유지한다.

## rollback·release 차단 조건

- 이 PR 머지 전에는 pinvi 대상 common 릴리스 검증(T-212의 pinvi admin 경로)을 airport 대체 경로로 바꾼다(D-16).
- README/AGENTS 상충이 남아 있으면 머지 금지(수령자 권리 불명확, lic §3.6).
