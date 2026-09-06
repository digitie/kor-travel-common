# T-011 소비자 매니페스트 스키마 `consumer-manifest.v1` + `tools/validate_manifest.py` + 7 소비자 초기 매니페스트 초안

- 상태: BLOCKED
- 우선순위: P1
- Gate: 도구 테스트
- 선행: T-005

## 목표

소비 저장소가 커밋할 `kor-travel-common.lock.json`의 스키마와 검증 도구를 만들고, 7 소비자의 초안을 common에 두어 T-403(매니페스트 커밋)과 T-012(통합 지도 생성)가 같은 형식을 쓰게 한다.

## 고정 결정

- [설계 브리프](../plan/design-brief.md) D-19(필드: `repo`·`app`·`tokens{version,override}`·`ui{version}`·`python{version}`·`lockfiles[]{kind,path,scope}`·`contrast{baseline,dark}`·`ux_gate{baseline}`·`openapi{exceptions}`·`exceptions[]`; `enforce` 없음), D-07(`lockfiles[]`를 `check_versions`가 읽음), D-13(baseline 파일), D-14(`openapi-exceptions.yaml` 참조).
- ADR-010 — [docs/adr/README.md](../adr/README.md).
- [버전 매트릭스](../survey/cross/version-matrix.md) §7.3(strict 파서·미지 필드 거부), [백엔드 조사](../survey/cross/backend.md) §2.1(앱별 lock 종류), [pinvi 인벤토리](../survey/inventory/pinvi.md) §2(모노레포 앱 디렉터리).

## 구현 범위

1. `templates/kor-travel-common.lock.schema.json`(문서용 스키마, draft 2020-12 형식) + `templates/kor-travel-common.lock.example.json`.
2. `tools/validate_manifest.py`: stdlib만으로 strict 검증(필수 필드·타입·미지 필드 거부·`exceptions[].until` 날짜 형식·`lockfiles[].kind ∈ {npm, uv, poetry, requirements}`·`enforce` 존재 시 오류·`repo` 값이 `versions.json consumers` 키에 있는지). 출력 오류 목록, exit 0/1.
3. `tools/check_versions.py`에 `--manifest <path>` 입력 연결(`lockfiles[]`를 순회, `scope`별 표).
4. `templates/manifests/<repo>[.<app>].lock.json` 초안: map(admin), weather(admin), geo(ui), concierge(frontend), docker-manager(frontend), airport(frontend·backend), pinvi(`apps/web`·`apps/api`·`apps/etl`). 값은 조사 기준 커밋 현재값(인벤토리 §10)이며 `tokens.version` 등은 미채택이면 `null`.
5. `tests/test_validate_manifest.py`(정상·미지 필드·`enforce`·`until` 누락·kind 오류).

## 범위 밖

- 소비자 저장소에 매니페스트를 커밋하는 일(T-403), `integration-map.md` 생성(T-012), baseline 파일 형식 자체(`contrast-baseline.json`은 T-103, `openapi-exceptions.yaml`은 T-301).

## 예상 변경 파일

예정 경로는 존재·실행 증거가 아니다. `templates/kor-travel-common.lock.schema.json`, `templates/kor-travel-common.lock.example.json`, `templates/manifests/*.lock.json`(9), `tools/validate_manifest.py`, `tools/check_versions.py`, `tests/test_validate_manifest.py`, `tools/README.md`(행 추가), `templates/README.md`(행 추가).

## 수용 기준

- 스키마 필드 집합이 D-19와 글자 단위로 같고 `enforce`를 넣은 fixture는 exit 1.
- `validate_manifest.py`가 9개 초안 전부 exit 0, 미지 필드·`until` 누락·잘못된 `kind` fixture는 exit 1(테스트로 고정).
- `check_versions.py --manifest templates/manifests/map.lock.json`이 `lockfiles[]`를 읽어 표를 낸다(lock 파일이 fixture로 없으면 `NO_LOCK`).
- 초안의 `repo`·`app` 값이 `versions.json consumers` 키·인벤토리 앱 경로와 일치한다.
- Linux·Windows 결과 동일.

## 검증 명령

```bash
python3 -B -X utf8 -m unittest discover -s tests -p "test_validate_manifest.py" -v
for f in templates/manifests/*.lock.json; do python3 -B -X utf8 tools/validate_manifest.py "$f" || echo "FAIL $f"; done
python3 -B -X utf8 tools/check_versions.py --manifest templates/manifests/map.lock.json
python3 -B -X utf8 tools/validate_document_links.py
```

Git Bash에서 동일.

## evidence

- 테스트 수·exit code·초안 9개 검증 결과를 이 절과 `docs/journal.md`에 남긴다.

## rollback 또는 release 차단 조건

- 도구·템플릿만 바뀌므로 `git revert` 1회로 원복한다.
- 스키마 변경은 `consumer-manifest.v2`로만 하며 v1 검증기를 유지한다. 초안이 검증기를 통과하지 못하면 T-403을 착수하지 않는다.
