# T-505 공유 라이브러리·마커 팔레트 정본 결정 요청 문서(`maplibre-vworld-react` npm·`license`·`vworld-style.ts` 중복·airkorea 이중 경로·kma/kasi SHA·P-01~16 hex)

- 상태: BLOCKED
- 우선순위: P3
- Gate: 문서
- 선행: T-008

## 목표

common 범위 밖이지만 소비자 정렬에 영향을 주는 외부 저장소 결정 6건을 한 문서로 정리해 결정자(사용자·map·weather·pinvi·maplibre-vworld-react)에게 요청한다. common은 결정을 대신 내리지 않으며, 회신 결과를 `versions.json` `providers` 절(보고만)과 규칙 문서 링크에 반영하는 것까지가 이 task다.

## 고정 결정

- common은 지도 엔진(`maplibre-vworld-*`)·provider 라이브러리(`python-*-api`)를 갖지 않는다; `versions.json` `providers` 절은 보고만: 브리프 D-01·D-23·O-16, ADR-001([ADR 색인](../adr/README.md)).
- 마커 팔레트 P-01~16은 common 소유 아님. 16슬롯·라벨 대비 규칙만 [ux-guide](../standards/ux-guide.md)에 두고 hex 정본은 map 확정 요청: 브리프 D-26·O-13.
- 벤더 tgz·`maplibre-vworld-*`·`python-*-api` 추출 영구 금지(B2): 브리프 D-17, [licensing 규칙](../standards/licensing.md).
- airkorea 스냅샷 정본 결정(L15)은 weather 소유이며 T-481과 연동: 브리프 T-481 제목.
- 근거: `docs/survey/cross/ux-patterns.md` §1.10·C22(스타일 빌더 배포 경로 4종), `docs/survey/cross/version-matrix.md` §2.7(kma map `a75d1e1` ≠ weather `0868b76`; kasi airport `51c39c1` vs pinvi etl `@main`), `docs/survey/cross/backend.md` §5.1, `docs/survey/cross/licensing.md` §3.7 L7·L15, `docs/survey/cross/design-tokens.md` §3.5·§5-2, `docs/survey/inventory/kor-travel-weather.md` §4.4·§8-21·§8-22, `docs/survey/inventory/kor-travel-map.md` §7·§8-29(ADR-043 게시 보류), `docs/survey/inventory/pinvi.md` 머리 5.

## 구현 범위

문서 `docs/plan/shared-library-decisions-request.md` 1개. 항목마다 (현황: 사실/추정 구분 + 근거 절) / (요청 문장) / (결정자) / (기본값: 회신 없을 때 common이 취하는 행동) / (common 측 후속) / (회신 기록).

| # | 항목 | 결정자 | 기본값(회신 전) |
|---|---|---|---|
| 1 | `maplibre-vworld-react` npm 게시 + 하위 `package.json` `license` 필드·`LICENSE`(L7) | 사용자·maplibre-vworld-react | 미게시 유지; common은 의존만 |
| 2 | `vworld-style.ts` 중복(map·weather) → 1 게시 후 소비 전환 | map·weather | 각 앱 잔류(중복 허용, common 흡수 금지) |
| 3 | weather `packages/python-airkorea-api` 스냅샷 vs GitHub 원본 정본(L15) | weather | 스냅샷 유지; `providers` 절에 "path" 표기 |
| 4 | `python-kma-api` SHA 정렬(map ≠ weather) | map·weather | 각 SHA를 `providers`에 병기·보고 |
| 5 | `python-kasi-api` pinvi etl `@main` → SHA 핀(airport `51c39c1` 기준 제안) | pinvi | `FLOATING_REF` 보고(T-484에서 제거) |
| 6 | 마커 팔레트 P-01~16 hex 정본(map Tableau vs pinvi Material) + `map-marker-react` 게시 보류(ADR-043) 해제 여부 | 사용자·map | hex 미기록; ux-guide 규칙만 |

문서 말미에 회신 표(항목·회신일·결정·후속 task ID)를 둔다. `versions.json` `providers` 절 갱신은 회신이 온 항목만, `docs/architecture/consumers.md`에는 링크 1줄만.

## 범위 밖

- 외부 저장소 수정, PR 작성(요청 문서에 제안 diff 요지만).
- 마커 hex 값·팔레트 코드를 common 파일에 두는 것(D-26).
- provider SHA를 `floor`/`recommended`로 강제하는 것(D-23: 보고만).

## 예상 변경 파일

예정 경로는 존재·실행 증거가 아니다.

```text
docs/plan/shared-library-decisions-request.md   (신설)
versions.json                                    (providers 절: 회신 항목만)
docs/architecture/consumers.md                   (링크 1줄)
docs/journal.md, docs/resume.md, docs/tasks/T-505-shared-library-marker-palette-request.md
```

## 수용 기준

- 6항목 모두 현황·근거 절·요청·결정자·기본값·후속이 채워져 있고, 현황의 사실/추정 표기가 조사 문서와 일치한다.
- 문서 어디에도 마커 hex 값(`#1f77b4`·`#E53935` 등)이 규범으로 적히지 않는다(인용은 조사 문서 절 번호로 대체).
- `versions.json` diff가 `providers` 절 밖을 바꾸지 않고, 회신 없는 항목은 바꾸지 않는다.
- `rg`로 `packages/`·`docs/standards/`에 `maplibre-vworld`·`python-*-api` 코드 복제·hex 팔레트가 없음을 확인한 결과가 evidence에 있다.
- 두 validator가 통과한다.
- 회신 표에 회신 유무가 항목별로 적혀 있고, 미회신 항목은 `열림(사용자 확인 필요)`으로 남는다.

## 검증 명령

```bash
rg -n "maplibre-vworld|python-[a-z]+-api" packages/ docs/standards/ ; echo "exit=$?"
rg -n "#(1f77b4|E53935|6366f1|757575)" docs/standards/ docs/plan/shared-library-decisions-request.md packages/ ; echo "exit=$?"
python3 -B -X utf8 tools/check_versions.py --registry versions.json --self-check
python3 -B -X utf8 tools/validate_document_links.py
python3 -B -X utf8 tools/validate_plan.py
```

첫 두 명령은 exit 1(불일치 0건)이 기대값이다. Git Bash에서 동일하게 실행한다.

## evidence

- 요청 문서의 회신 표가 evidence다. 요청을 보낸 경로(각 저장소 issue URL 또는 사용자 확인 대화의 날짜)를 항목별로 적는다.
- `docs/journal.md` 최신 항목에 rg 실행 결과와 요청 발송 일자를 남긴다.

## rollback 또는 release 차단 조건

- 문서 task이므로 코드 rollback은 없다. 요청이 기각되면 문서에 disposition(기각·근거·대안)을 남기고 기본값을 유지한다.
- 회신이 없다는 이유로 common이 hex·SHA를 확정값으로 기록하면 이 task는 실패다. `providers` 절은 보고 상태를 유지한다.
