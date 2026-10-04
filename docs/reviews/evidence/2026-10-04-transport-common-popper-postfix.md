# Common transport 후보 post-fix — Popper 독립 원본

- 실행 ID: POPPER-COMMON-TRANSPORT-POSTFIX-20261004-01
- 종류/전문 영역: 독립 post-fix delta, 계약·패키징·복구 경계
- 시작: 2026-10-04T14:49:22.1425893+09:00
- 소스 검토/검증 종료: 2026-10-04T14:49:49.1677618+09:00
- 원래 base: `090f98429453d8882150eb9e56ccae98e0e353a2`
- 직전 검토 candidate: `f3e5681fcc751cc2951d74f72f9c90be1f29d670`
- 전달 및 실제 관찰 post-fix candidate: `9da188982ccbe65adc0c69607b8e598e607931c0`
- 격리: Windows Git 고정 객체 show/diff/Node 메모리 검증만 사용했다. 작업트리 소스, 다른 리뷰어 원본을 읽거나 수정하지 않았다. 추가된 상대 evidence는 diff 파일 목록만 확인하고 본문은 열지 않았다. 기존 원본은 그대로 보존하며 이 evidence만 생성한다.
- 부모 전달 상태: common 후보 CI green. transport backend CI는 진행 중이다. 이 리뷰가 해당 외부 실행을 독립 검증한 것으로 세지 않는다.

## 판정

**PASS.** B-P3-01은 FIXED. 신규/잔여 P0/P1/P2/P3는 0개다. common 코드 리뷰의 판정이며 transport SQL·migration·실제 shared instance·live UI gate를 승인하는 결과가 아니다.

## Closure와 검증

`packages/ui/src/dagster-model.ts:26`의 공개 helper 주석이 한국어로 실제 계약에 맞춰 수정되었다. 진행 중 실행은 확인 시각, 종료 실행은 종료 시각까지의 경과 초를 반환하고 유효한 시각이 없으면 null이라는 설명이 구현 및 이전에 실행한 SUCCESS(start10,end70,nowNaN)→60 사례와 일치한다. B-P3-01의 stale STARTED-only 설명이 제거되어 **FIXED**다.

소스/패키지 post-fix delta는 이 주석 한 줄과 smoke lock UI SHA512 한 줄이다. 그 밖에는 리뷰 원본 evidence 추가만 있다. Node가 양쪽 고정 객체를 읽어 JSDoc을 제거한 전체 dagster-model.ts가 동일함을 assert했다. 따라서 runtime 행동은 직전 리뷰의 38개 함수 경계 사례 결과와 같은 코드다. 기존 verdict를 막았던 구현 결함은 없었고 이번 수정은 계약 설명을 바로잡는다.

smoke lock 두 JSON을 parse하고 `node_modules/@kor-travel/ui.integrity`만 제거한 뒤 deepEqual을 실행하여 다른 version/resolved/dependency/registry 값이 바뀌지 않았음을 확인했다. 새 integrity는 SHA512 형식이고 Base64 decode 결과 64bytes다. UI/tokens tarball 이름·공개 export·CSS 경로·Python/DB 책임은 그대로다. 압축 artifact를 재생성할 때 digest가 변하는 것은 정상이며, 실제 현재 bytes와 digest 일치는 pack/install CI가 확인하는 별도 실행이다.

- 주석 제거 후 runtime source 동일 assertion: **PASS**.
- lock integrity 외 JSON 동일 및 새 SHA512 형식 assertion: **PASS**.
- 직전 후보→post-fix `git diff --check`: **PASS**.
- full build/test/pack/install/CI API/live UI/실제 운영 worker 종료: **NOT_RUN(부모와 소비자 gate 소유; read-only delta 리뷰)**.

## 공격 시나리오와 불확실성

주석만 고친다고 주장하면서 duration/cron 동작이 함께 바뀌는 경우를 객체 본문 비교로 검사했고 동일했다. tarball integrity 갱신에 registry dependency/버전/경로가 섞이는 경우를 JSON 비교로 검사했고 없었다. 공개 helper의 STARTED-only stale 설명이 남는 경우도 제거됨을 직접 읽었다.

이 작은 delta에는 Python/collector SQL 또는 daemon 설정 변경이 없다. 실제 transport 소유권 fence/heartbeat CAS/receipt 보호와 shared manager 활성 YAML, 산출물 설치/live 브라우저는 다음 transport immutable candidate 및 부모 실행 evidence에서 확인할 범위다. 이전 common 원본의 해당 외부 불확실성을 완료로 전환하지 않는다.
