# Common transport 채택 후보 — Popper 독립 적대적 리뷰 원본

- 실행 ID: POPPER-COMMON-TRANSPORT-20261004-01
- 종류/전문 영역: 전체 후보 delta, 패키징·계약·Python/DB/실제 Dagster instance 경계
- 시작: 2026-10-04T14:34:22.9403022+09:00
- 소스 검토/실행 종료: 2026-10-04T14:36:09.2442021+09:00
- 전달 입력: common Draft PR #25, base `090f98429453d8882150eb9e56ccae98e0e353a2`, candidate `f3e5681fcc751cc2951d74f72f9c90be1f29d670`, readonly 원본 리뷰. 부모는 CI green을 알렸다.
- 실제 관찰 candidate: `git rev-parse` 결과 `f3e5681fcc751cc2951d74f72f9c90be1f29d670`.
- 격리: 모든 소스/규칙은 Windows Git 고정 객체 `show`/`diff`로 읽었다. 변경 중인 작업트리 소스나 다른 리뷰어 원본은 읽지 않았다. checkout clean 상태를 필요로 하지 않는 object-only 방식이며 source/build 수정 없이 이 원본 evidence만 생성한다.
- 적용 규칙: candidate AGENTS.md, docs/README.md, resume, T-216, agent-workflow의 심각도/판정, review archive 기록 규칙을 확인했다.

## 판정

**CONDITIONAL — P0/P1/P2 지적 0개, 작은 공개 helper 주석 오류 P3 1개.** B-P3-01을 수정하거나 정식 DEFERRED(담당/task/gate/목표 시점)를 기록하면 코드 리뷰는 PASS 가능하다. consumer/실제 instance gate의 통과 여부는 이 common 리뷰만으로 승인하지 않는다.

## 범위와 확인 결과

14개 변경 파일 전체 diff(93줄 추가/16줄 삭제)를 읽었다. UI dev.2 버전/lock/smoke fixture, Dagster 표시 함수/표의 keyboard region/CSS, 테스트, CHANGELOG, 채택 가이드와 작업 상태 기록이 대상이다. 관련 공개 export, build/package 검사, TypeScript 설정, 가이드의 기존 복구 코어 책임도 읽었다.

Python 패키지 전체 tree는 base/candidate 모두 `9f0647bf1944cdc5276194c4308ccc2696fcf9dc`로 동일하다. `.github/workflows`, package 검사 및 tsconfig도 diff가 없다. 따라서 transport의 ownership migration/fencing SQL이 common에 새로 구현되었다고 판단하지 않는다. 가이드는 이를 소비자 책임으로 명시하고, shared manager의 실제 YAML과 code-server 전용 YAML을 구별한다. 격리 instance 성공만으로 shared 운영 적용을 완료했다고 보고하지 말라는 문구는 적절하다.

UI 버전은 dev.1→dev.2로 상승하며 root workspace lock, smoke manifest/lock/resolved/version, prepare-lock tarball 이름이 맞는다. public export 경로와 files의 dagster.css 및 라이선스 고지 경로는 유지된다. prepare-lock은 실제 생성 tarball SHA512를 읽으므로 CI가 고정된 과거 압축 artifact digest를 억지로 재사용하는 구조가 아니다. 실행 시 새 artifact의 integrity를 갱신하는 기존 계약도 유지된다. 이 리뷰에서 pack/install 자체를 다시 실행하지는 않았다.

cron 표시는 60분/24시간 경계를 균등하게 나누는 step만 번역하며, 잘못된 범위·0 step·비균등 step·추가 field·다른 day/month/weekday는 원문으로 반환한다. terminal duration은 endTime을 사용하며 STARTED의 NaN 확인 시각을 정상 경과로 표시하지 않는다. isStalledRun의 명시적 STARTED 조건으로 terminal duration 확장이 terminal 정체 집계를 늘리지 않는다. keyboard region은 기존 table slot과 상세/URL 계약을 보존한다.

## 실제 실행한 검증

- candidate `dagster-model.ts`를 Git 객체에서 읽고 함수 본문만 메모리에서 추출하여 TypeScript signature만 제거한 Node assert 실험: **38개 사례 PASS**. minute divisors 11개, 불가능/비균등 minute step 6개, hour divisors 8개, invalid/mixed cron 6개, terminal/STARTED/missing/NaN/Infinity/역전 시간 7개다. 이는 full TypeScript/React 테스트의 대체가 아니다.
- candidate Git 객체의 package.json/root lock/smoke manifest/lock을 JSON parse하여 버전·artifact 경로·CSS export를 assert: **PASS**.
- base→candidate `git diff --check`: **PASS**.
- Python 및 CI/build 설정 unchanged 비교와 Python tree hash 동일 확인: **PASS**.
- full UI test/build, npm pack/install/consumer smoke, Python test, CI API, 브라우저/운영 Dagster: **NOT_RUN(부모 진행 검증 및 별도 소비자 gate; source readonly 리뷰)**. 부모가 보고한 CI green은 전달 정보이며 독립 재실행 결과로 합산하지 않는다.

## Finding

### B-P3-01 — 공개 runElapsedSeconds의 설명이 새 terminal 계약과 모순된다

- 위치: `packages/ui/src/dagster-model.ts:26–30`.
- 근거: 바로 위 공개 함수 주석은 STARTED 실행의 경과를 반환하고 그 외는 null이라는 계약을 설명한다. 후보는 startTime/endTime이 유효한 SUCCESS/FAILURE/CANCELED에도 duration을 반환한다. CHANGELOG와 새 테스트는 확장된 구현이 의도임을 확인한다.
- 재현: 고정 candidate 함수에서 `{status:'SUCCESS', startTime:10, endTime:70}`과 now=NaN을 넣어 **60 반환**을 실제 assert했다. 주석대로라면 null이어야 한다.
- 영향: 소비자가 공개 helper를 읽을 때 stale 설명을 계약으로 오해한다. UI 구현/정체 집계에는 결함이 없으며 merge 안전 경계를 직접 깨지 않는 문서 품질 문제다.
- 권고: 인접 주석을 한국어로 갱신하여 STARTED는 nowSeconds, 끝난 실행은 endTime을 사용하고 유효한 시각이 없을 때 null임을 설명한다. 동작을 되돌릴 필요는 없다.
- disposition: OPEN. source 수정은 수행하지 않았다.

## 공격 시나리오와 남은 불확실성

1. cron step 0/7/59/60, hour step 5, minute75/hour25, six-field 및 특정 day expression으로 잘못된 번역을 시도했다. 실행 사례는 원문 fallback으로 수렴했다.
2. terminal run의 오래된 시간/NaN now를 이용해 정체 표시를 오염시키려 했다. duration은 endTime을 사용하며 isStalledRun의 STARTED 선행 조건이 terminal 경고를 막는다. invalid snapshot 날짜의 heading 표시 품질은 변경 전부터 존재하는 별도 소비자 입력 검증 경계다.
3. dev.2 manifest만 상승하고 fixture/lock/tarball명이 dev.1에 남는 실패를 대조했다. 관련 참조는 일치한다. 실제 산출물 bytes와 consumer vendor digest는 소비자 후보에서 별도 확인해야 한다.
4. shared instance가 전용 YAML을 읽지 않는 상황에서 자동 복구가 적용되었다고 오인하는 문서를 찾았다. 새 가이드는 Manager 활성 monitoring/run_retries/tag concurrency를 별도 확인하도록 명시한다.
5. 일반 retry가 KRIC 48h/버스 72h/철도 48h 및 비용 receipt를 우회하는 계약을 찾았다. 가이드는 도메인 정책과 receipt를 소비자에 남기며 제한된 infrastructure retry와 provider Failure를 분리한다. 실제 transport 코드가 이를 지키는지는 PR #67의 고정 후보 후속 리뷰가 필요하다.
6. 가이드의 0024 migration·flush/commit lock·heartbeat CAS·진행 목록 merge·failure event scope는 **소비자 채택 사례의 설명**이다. 이 common diff만으로 SQL 경쟁 안전성, migration 업그레이드, 외부 code location 격리 또는 실제 worker 종료를 실행 증명한 것으로 세지 않는다.

운영 shared instance의 설정/버전/launcher 종료, transport source 구현과 실제 vendor artifact, 작은 viewport/focus 화면 결과는 범위 밖이며 소비자 CI·live E2E 및 후속 immutable review에서 확인해야 한다.
