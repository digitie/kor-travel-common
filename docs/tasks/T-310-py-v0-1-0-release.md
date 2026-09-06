# T-310 py-v0.1.0(1차) → weather-api·map-api·airport 검증 → 정식(wheel 자산)

- 상태: BLOCKED
- 우선순위: P1
- Gate: 소비자 스모크
- 선행: T-310a
- 외부 선행: 실제 Python 소비자 계약 대조 evidence를 해당 저장소 담당자가 제공한다. common 작업자는 소비자 저장소에 쓰지 않는다.

## 목표

Python 공통 패키지의 첫 릴리스를 낸다: `py-v0.1.0-rc.1` 태그 → 1차 소비자 3곳(weather-api·map-api·airport; D-16)의 pinned checkout에서 rc를 설치해 "계약 무변경"을 확인 → 수정 → `py-v0.1.0` 정식 태그 + GitHub Release 자산(wheel·sdist·`SHA256SUMS`). 이 task는 common 쪽 릴리스와 rc 검증까지이며, 각 앱의 실제 채택 PR은 T-480(map-api)·T-481(weather-api)·T-482(airport)가 이 task의 정식 태그를 선행으로 갖는다. 1차 내용물 = T-302 골격 + T-303 export CLI + T-304 health/time + T-305 quality.

## 고정 결정

- [design-brief](../plan/design-brief.md) D-11(Python = `git+https://github.com/digitie/kor-travel-common.git@py-vX.Y.Z#subdirectory=packages/py/kor-travel-common` + lock sha, wheel 자산 병행, 태그 불변·재발행 금지·`@main` 금지, 고지 파일 동봉), D-16(Python 1차 = map-api·weather-api·airport), D-18(`-rc.N` → 소비자 PR 검증 → 정식, CHANGELOG 단일 파일 + 패키지별 H3), D-24(이관 PR 규격: 한 PR = 한 산출물, py 파일 상한 10, `git revert` 1회), D-25(NOT_RUN), D-31(SemVer 0.x; py 독립 버전; 소비자 범위 `~0.N`), D-17(wheel에 `LICENSE`·`NOTICE`·`THIRD_PARTY_NOTICES.md`). ADR-005·ADR-010·ADR-011 — [ADR 색인](../adr/README.md). 절차 정본: [release runbook](../runbooks/release.md), 소비자 측 절차: [consumer adoption runbook](../runbooks/consumer-adoption.md), PR 본문: [templates/consumer-pr.md](../../templates/consumer-pr.md).
- 공개 여부 전제 **열림(O-15, 사용자 확인 필요)**, 기본값 = 공개. 배포 이름은 ADR-014로 확정했으며 PyPI 가용성 확인을 하지 않는다.
- 앱별 PR 순서·되돌리기: [judge-migration-feasibility §3.1](../plan/design-panel/judge-migration-feasibility.md) map PR 4(export CLI 교체·health 팩토리·ruff extend, 3 profile 무변경 단언 + pinvi/ktdm pin 갱신 요청 링크), weather PR 8(export `--check` 전환·`code` 사전·L15 airkorea 정본), airport PR 4(`code`/`request_id` additive·스펙 422 정합·`--check` CI·`uv sync --locked`). 앱 근거: [inv/map §8](../survey/inventory/kor-travel-map.md) 16·20·22, [§9](../survey/inventory/kor-travel-map.md)(Python lockfile 없음·OpenAPI 3종·CLI argparse), [inv/weather §8](../survey/inventory/kor-travel-weather.md) 11·12·13·17, [§9](../survey/inventory/kor-travel-weather.md)(Python 3.11/3.12/3.13 불일치), [inv/airport §8](../survey/inventory/kor-travel-airport.md) 10·12·15·16, [§9](../survey/inventory/kor-travel-airport.md)(uv.lock CI vs pip Docker).
- PEP 440 버전 문자열은 `0.1.0rc1`, git 태그는 `py-v0.1.0-rc.1`(D-18 표기) — 대응표를 `release.md`에 둔다(runbooks 소유자와 합의).

## 구현 범위

[release §2.1](../runbooks/release.md#21-common-후보-보존과-후속-구현)에 따라 보존 후보에서 분기한 release branch의 PR로 준비한다. 아래 버전·lock 변경은 해당 branch에 적용한다. 후속 minor가 있는 main을 과거 버전으로 내리지 않는다. 소비자 단계는 해당 저장소 담당자에게 요청하는 외부 gate이며 미실행이면 BLOCKED/NOT_RUN을 유지한다.

1. 사전 조건 확인: T-302 `python-package` job green, T-303·T-304·T-305 DONE, `check_spdx` 0 오류, CHANGELOG `## [Unreleased]` → `## [0.1.0]` 아래 `### kor-travel-common (py)` H3.
2. `_version.py` `0.1.0rc1` → 태그 `py-v0.1.0-rc.1` → `uv build` → Release(prerelease) 자산 `kor_travel_common-0.1.0rc1-py3-none-any.whl`·sdist·`SHA256SUMS`.
3. rc 검증 요청(담당자는 각 소비자 저장소): `consumers.pins.json`의 SHA에서 아래 계약을 대조한 evidence를 요청한다. common 작업자는 해당 저장소의 checkout·검증 branch를 만들거나 설치·수정하지 않는다. 담당자가 별도 검증 branch를 사용했다면 해당 저장소의 되돌리기와 정리 evidence를 받는다.
   - map(`F:/dev/kor-travel-common-survey/ktm-main` 또는 pin): `uv pip install "kor-travel-common[api] @ git+https://github.com/digitie/kor-travel-common.git@py-v0.1.0-rc.1#subdirectory=packages/py/kor-travel-common"` → `python -m kortravelcommon.openapi export --app kortravelmap.api.app:create_app --profile admin|user|service --transform <map route-policy 콜백> --check`로 3 profile 바이트 무변경; `health_router(wrap=map envelope)`를 테스트 앱에 마운트해 `/health`·`/version` 본문이 현행과 같음; `ruff check --config templates/python/ruff.base.toml` report(위반 수만 기록, fail 아님).
   - weather-api: 같은 CLI로 `packages/kor-travel-weather-api/openapi.json` 대조(`development` 프로필 강제 사실 확인, M9 미확인 항목 기록); `kortravelcommon.time.kst_now` vs `models.py` 고정 오프셋 차이 기록.
   - airport: `docs/openapi.json` 대조(인메모리 SQLite 설정 export 재현); `/health`의 DB 질의를 `/readyz`로 옮길 때의 응답 차이 기록(additive 판정 근거).
   - Python 3.11·3.12·3.13 설치 가능 확인(map floor 3.11, weather Docker 3.13).
4. rc 결과 반영 후 `0.1.0` → 태그 `py-v0.1.0` → Release 정식 자산 + `SHA256SUMS`; `versions.json` `packages.py`(또는 해당 절) 값 갱신(versions-conventions 소유 파일의 데이터 갱신), `docs/resume.md`·`docs/journal.md`·CHANGELOG 갱신.
5. `consumer-smoke` 워크플로에 Python 소비자 스모크(wheel URL 설치 + `export --check`)를 추가할지 판단해 `release.md`에 기록(ADR-013 consumer-smoke는 패키지별 승인된 npm 소비자 조합).

## 범위 밖

각 앱의 채택 PR 머지(T-480·T-481·T-482), 2차 모듈(T-306~T-308)이 들어가는 `py-v0.2.0`, pinvi·ktdm pin 갱신 PR(T-480 동반), npm/PyPI 게시(사용자 범위 제외)·Renovate 재평가(T-507), 릴리스 runbook 재현성 리허설(T-501은 tokens·ui), weather airkorea 정본 결정 L15(T-481).

## 예상 변경 파일

예정 경로는 존재·실행 증거가 아니다.

```text
packages/py/kor-travel-common/src/kortravelcommon/_version.py
packages/py/kor-travel-common/uv.lock
CHANGELOG.md
versions.json                                   # py 패키지 버전 값(versions-conventions 소유 파일)
docs/runbooks/release.md                        # PEP 440↔태그 대응표(runbooks 합의)
docs/resume.md, docs/journal.md
(git 태그 py-v0.1.0-rc.1, py-v0.1.0; GitHub Release 자산 — 저장소 파일 아님)
```

## 수용 기준

- [ ] Release `py-v0.1.0`에 wheel·sdist·`SHA256SUMS`가 있고 `sha256sum -c SHA256SUMS`가 통과하며 wheel 안에 `LICENSE`·`NOTICE`·`THIRD_PARTY_NOTICES.md`가 있다.
- [ ] `pip install "kor-travel-common[api] @ git+https://…@py-v0.1.0#subdirectory=packages/py/kor-travel-common"`과 wheel URL 설치가 Python 3.11·3.12·3.13 깨끗한 venv에서 모두 성공하고 `kortravelcommon.__version__ == "0.1.0"`.
- [ ] rc 검증 evidence에 3 소비자 각각의 export `--check` 결과(map 3 profile 바이트 동일 또는 diff와 사유), health 본문 대조, ruff report 위반 수가 있다. 3곳 모두 `NOT_RUN`이면 정식 태그 금지; 최소 GPL 소비자 2곳 실측(D-16·판정 §4.2).
- [ ] rc에서 발견한 문제는 rc.2 이상으로만 고치고 같은 태그를 재발행하지 않았다(`git tag -l 'py-v0.1.0*'`와 Release 이력으로 확인).
- [ ] CHANGELOG에 `### kor-travel-common (py)` H3와 `0.1.0` 항목이 있고 `### Breaking`이 없다(1차는 additive만).
- [ ] `versions.json`·`docs/resume.md`·`docs/journal.md`가 갱신됐고 `validate_document_links.py`·`validate_plan.py` 0 오류.

## 검증 명령

```bash
cd packages/py/kor-travel-common && uv build && sha256sum dist/* > dist/SHA256SUMS && sha256sum -c dist/SHA256SUMS
for v in 3.11 3.12 3.13; do uv venv /tmp/ktc-$v --python $v && uv pip install --python /tmp/ktc-$v/bin/python \
  "kor-travel-common[api] @ git+https://github.com/digitie/kor-travel-common.git@py-v0.1.0-rc.1#subdirectory=packages/py/kor-travel-common" \
  && /tmp/ktc-$v/bin/python -c "import kortravelcommon; print(kortravelcommon.__version__)"; done
unzip -l dist/*.whl | grep -E 'LICENSE|NOTICE|THIRD_PARTY_NOTICES'
# 소비자 checkout(pin SHA)에서: python -m kortravelcommon.openapi export --app <factory> --output <spec> --check ; echo "exit=$?"
cd ../../.. && python3 -B -X utf8 tools/validate_document_links.py && python3 -B -X utf8 tools/validate_plan.py
```

## evidence

이 파일 하단 "실행 기록"에 태그·Release URL·자산 sha256·Python 3종 설치 결과·소비자 3곳의 `--check` exit code와 diff 요약·ruff 위반 수·검증 브랜치 삭제 확인을 남긴다. 실행하지 못한 소비자는 `NOT_RUN(사유)`로 적고 DONE 전 `외부 선행`으로 승격(D-25). 2인 리뷰가 필요한 규범 변경(`release.md` 절차 수정)이 있으면 report 경로를 링크한다.

## rollback·release 차단 조건

- 태그는 불변이므로 되돌리기는 "새 버전"이다: 정식 태그 후 결함이 나오면 `0.1.1`(additive 수정) 또는 `0.2.0`(파괴, `-rc` + 이관 절)로 낸다. rc 단계 문제는 rc.N+1. 소비자 검증 브랜치는 병합하지 않으므로 원 저장소 되돌리기가 필요 없다.
- 차단: map 3 profile 산출물이 바뀌는데 pinvi·ktdm pin 갱신 PR 계획이 없음(D-14), wheel 고지 파일 누락, `check_spdx` 실패, starlette 매트릭스 red, 2인 리뷰 미해결 P0/P1, 소비자 실측 2곳 미만.
