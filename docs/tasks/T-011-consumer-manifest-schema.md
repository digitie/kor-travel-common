# T-011 소비자 매니페스트 스키마 `consumer-manifest.v1` + `tools/validate_manifest.py` + 7 소비자 초기 매니페스트 초안

- 상태: DONE
- 우선순위: P1
- Gate: 도구 테스트
- 선행: T-005, T-016

## 목표

소비 저장소가 커밋할 `kor-travel-common.lock.json`의 스키마와 검증 도구를 만들고, 7 소비자의 앱 표면별 초안을 common에 두어 T-403(매니페스트 커밋)과 T-012(통합 지도 생성)가 같은 형식을 쓰게 한다. 초안은 채택·설치·소비자 실행 성공을 의미하지 않는다.

## 고정 결정

- [설계 브리프](../plan/design-brief.md) D-19(필드: `repo`·`app`·`tokens{version,override}`·`ui{version}`·`python{version}`·`lockfiles[]{kind,path,scope}`·`contrast{baseline,dark}`·`ux_gate{baseline}`·`openapi{exceptions}`·`exceptions[]`; `enforce` 없음), D-07(`lockfiles[]`를 `check_versions`가 읽음), D-13(baseline 파일), D-14(`openapi-exceptions.yaml` 참조).
- ADR-010 — [docs/adr/README.md](../adr/README.md).
- [버전 매트릭스](../survey/cross/version-matrix.md) §7.3(strict 파서·미지 필드 거부), [백엔드 조사](../survey/cross/backend.md) §2.1(앱별 lock 종류), [pinvi 인벤토리](../survey/inventory/pinvi.md) §2(모노레포 앱 디렉터리).
- `openapi.exceptions`는 `docs/standards/openapi-exceptions.yaml#<app>` 같은 정본 참조 문자열 배열이다. 최상위 `exceptions[]`는 UX 규칙 예외(`rule`·`surface`·`reason`·`until`·`review`) 또는 버전·포트 예외(`key`·`reason`·`until`·`review`)의 두 형태만 허용하며 `until`·`review`는 유효한 ISO 날짜다.

## 구현 범위

1. `templates/kor-travel-common.lock.schema.json`(문서용 스키마, draft 2020-12 형식) + `templates/kor-travel-common.lock.example.json`.
2. `tools/manifest_schema.py`와 `tools/validate_manifest.py`: stdlib만으로 strict 검증(필수 필드·타입·미지 필드 거부·`exceptions[].until` 날짜 형식·`lockfiles[].kind ∈ {npm, uv, poetry, requirements}`·`enforce` 존재 시 오류·`repo` 값이 `versions.json consumers` 키에 있는지). 출력 오류 목록, exit 0/1.
3. 이미 존재하는 `tools/check_versions.py <consumer-repo-root> --manifest <manifest>` 입력 계약을 새 strict schema와 호환되도록 검증한다. `lockfiles[]` 순회·`scope`별 표·저장소 루트 workflow 검색을 보존하고, 매니페스트 경로·`app` 경로·저장소 경계를 벗어나는 lock path와 workflow 누락을 회귀 시험으로 고정한다. root 없이 호출하는 기존 최소 fixture는 하위 호환으로 읽는다.
4. 다음 **10개** 초안의 repo/app/파일 대응을 고정한다. 실제 소비자 매니페스트는 표의 앱 디렉터리에 놓고, `lockfiles.path`는 **소비자 저장소 루트 기준**으로 해석한다. `app`은 표면 식별자이며 `scope`는 보고 label 겸 npm workspace 선택자다(`root`는 lockfile 루트 package, 그 밖에는 lockfile 기준 workspace 경로). 도구 호출은 `check_versions.py <consumer-repo-root> --manifest <app-dir>/kor-travel-common.lock.json` 형태로 저장소 루트와 manifest를 함께 전달한다.

   | manifest 위치(소비자 저장소 기준) | 파일 | repo | app | 관찰 lock |
   |---|---|---|---|---|
   | `packages/kor-travel-map-admin/frontend/` | `map.lock.json` | `kor-travel-map` | `admin` | root `package-lock.json`(workspace selector) |
   | `packages/kor-travel-weather-admin/frontend/` | `weather.lock.json` | `kor-travel-weather` | `admin` | `packages/kor-travel-weather-admin/frontend/package-lock.json`, root `uv.lock` |
   | `kor-travel-geo-ui/` | `geo.lock.json` | `kor-travel-geo` | `ui` | `kor-travel-geo-ui/package-lock.json` |
   | `frontend/` | `concierge.lock.json` | `kor-travel-concierge` | `frontend` | `frontend/package-lock.json`, requirements files |
   | `frontend/` | `docker-manager.lock.json` | `kor-travel-docker-manager` | `frontend` | `frontend/package-lock.json`, backend `poetry.lock`(미추적이면 null) |
   | `frontend/` | `airport.frontend.lock.json` | `kor-travel-airport` | `frontend` | `frontend/package-lock.json` |
   | `backend/` | `airport.backend.lock.json` | `kor-travel-airport` | `backend` | `backend/uv.lock` |
   | `apps/web/` | `pinvi.apps-web.lock.json` | `pinvi` | `apps/web` | root `package-lock.json`(workspace selector) |
   | `apps/api/` | `pinvi.apps-api.lock.json` | `pinvi` | `apps/api` | `apps/api/uv.lock` |
   | `apps/etl/` | `pinvi.apps-etl.lock.json` | `pinvi` | `apps/etl` | lock 없음(선언만) |

   값은 조사 기준 커밋 현재값(인벤토리 §10)이며 `tokens.version` 등은 미채택이면 `null`.
5. `tests/test_validate_manifest.py`(정상·미지 필드·`enforce`·`until`/`review` 날짜·비ASCII/끝 개행 날짜·kind 오류·workspace·workspace/app/intermediate symlink loop·registry self-symlink·빈 lock 선언·requirements 재귀 root 이탈·self-symlink·제어문자/경계 공백 schema parity·민감한 전이 scope/DEL redaction).

## 반복된 적대적 리뷰 no-go의 원인과 방지

초기 구현은 매니페스트·lock·workspace·app 경계를 각 호출부의 `Path.resolve()`·`is_file()`·`exists()` 조합으로 따로 검사했다. `resolve(strict=False)`의 symlink loop 처리와 누락 leaf의 결과가 Windows와 WSL에서 달랐고, 존재성 조기 반환이 중간 symlink를 검사 전에 지워 버렸다. 그래서 리뷰어가 서로 다른 경로 모양을 제시할 때마다 같은 입력 경계의 변형이 새 P2로 나타났다.

입력 경계는 `_resolve_input_path`와 `_path_contains_symlink`로 한곳에 모으고, lock·동반 선언·app·workspace를 존재성 판단 전에 구성요소 전체로 검사한다. validator registry와 requirements 재귀도 원문 없는 입력 오류로 닫는다. Windows·WSL에서 direct/중간/외부/self-symlink와 누락 경로를 함께 실행하는 회귀 시험을 수용 기준에 고정해, OS별 동작 차이와 조기 반환 재발을 같은 후보에서 발견하도록 했다.

## 범위 밖

- 소비자 저장소에 매니페스트를 커밋하는 일(T-403), `integration-map.md` 생성(T-012), baseline 파일 형식 자체(`contrast-baseline.json`은 T-103, `openapi-exceptions.yaml`은 T-301).

## 예상 변경 파일

예정 경로는 존재·실행 증거가 아니다. `templates/kor-travel-common.lock.schema.json`, `templates/kor-travel-common.lock.example.json`, `templates/manifests/*.lock.json`(10), `tools/manifest_schema.py`, `tools/validate_manifest.py`, `tools/check_versions.py`, `tests/test_validate_manifest.py`, `tools/README.md`(행 추가), `templates/README.md`(행 추가).

## 수용 기준

- 스키마 필드 집합이 D-19와 글자 단위로 같고 `enforce`를 넣은 fixture는 exit 1.
- `validate_manifest.py`가 10개 초안 전부 exit 0, 미지 필드·`until` 누락·잘못된 `kind` fixture는 exit 1(테스트로 고정).
- `check_versions.py <fixture-repo-root> --manifest <fixture-repo-root>/templates/manifests/map.lock.json`이 저장소 루트의 shared lock과 root workflow를 읽어 표를 낸다. lock/workflow가 fixture로 없으면 각각 `NO_LOCK`/빈 workflow로 명시한다.
- npm `scope`가 workspace 경로면 해당 멤버 선언을 읽고, lock 옆 동반 선언의 root 밖 symlink는 exit 2로 닫는다. 빈 lock 목록의 선언 전용 앱은 `NO_LOCK` 행을 낸다.
- validator·check_versions의 오류·보고 채널은 미지 field와 민감한 scope 원문을 재출력하지 않는다. JSON Schema와 stdlib validator의 상대 경로·제어문자·날짜 음성 corpus가 같은 결과를 내며, requirements 재귀 include도 소비자 root 밖으로 나가지 않는다.
- 초안의 10개 `repo`·`app` 값이 `versions.json consumers` 키·인벤토리 앱 경로와 일치하고 대응표와 파일 수가 같다.
- Linux·Windows 결과 동일.

## 검증 명령

```bash
python3 -B -X utf8 -m unittest discover -s tests -p "test_validate_manifest.py" -v
for f in templates/manifests/*.lock.json; do python3 -B -X utf8 tools/validate_manifest.py "$f" || echo "FAIL $f"; done
python3 -B -X utf8 tools/check_versions.py <fixture-repo-root> --manifest <fixture-repo-root>/templates/manifests/map.lock.json
python3 -B -X utf8 tools/validate_document_links.py
```

Git Bash에서 동일.

## evidence

- 최종 candidate `4680bacdf285f2cc86f1a18cc1de29ff4129f2a8`을 PR #10에 push했고 exact CI `34120043104`의 docs·tools(ubuntu-24.04)·tools(windows-2025)·secret-scan·check-versions 5개 job이 성공했다.
- Windows Python 3.14.3·WSL Python 3.11.15에서 전체 203 tests, focused 23 tests를 실행했다. WSL은 선택 jsonschema 엔진 2개를 skip으로 별도 기록했으며 성공으로 세지 않았다. `validate_plan`(106/오류0), 문서 링크(353/2304/오류0), SPDX(32/오류0), secret/redaction(443/발견0), `check_versions --self-check`도 통과했다.
- 독립 적대 리뷰 post-fix-07에서 A/B 모두 PASS, 신규 P0–P3 0건, 누적 T011-R17~R20 모두 FIXED다([통합 리뷰](../reviews/adversarial/2026-09-07-t011-post-fix-07.md), [A 원본](../reviews/adversarial/evidence/2026-09-07-t011-post-fix-07-reviewer-a.md), [B 원본](../reviews/adversarial/evidence/2026-09-07-t011-post-fix-07-reviewer-b.md)).
- 소비자 저장소 build/e2e·npm ci·uv sync·패키지 build/pack/install·release·npm/PyPI 게시·소비자 채택은 `NOT_RUN(이번 범위 밖)`이다.

## rollback 또는 release 차단 조건

- 도구·템플릿만 바뀌므로 `git revert` 1회로 원복한다.
- 스키마 변경은 `consumer-manifest.v2`로만 하며 v1 검증기를 유지한다. 초안이 검증기를 통과하지 못하면 T-403을 착수하지 않는다.
