# ADR-014: npm·PyPI 미게시와 common 구현·외부 릴리스 분리

- 상태: accepted
- 날짜: 2026-09-07
- 근거 문서: 사용자 지시(common만 작성·구현까지 순차 완주·npm/PyPI 미게시), [T-015](../tasks/T-015-common-delivery-plan.md)
- Supersedes: ADR-005의 공개 registry 게시 재평가·이름 확보 조건과 ADR-013 결정 1의 이전 minor 정식 릴리스 선행을 부분 대체

## 컨텍스트

기존 계획은 npm·PyPI 이름 확보와 게시 재평가를 남겼고 이전 minor 정식 발행을 다음 구현의 선행으로 삼았다. 사용자는 npm·PyPI에 게시하지 않고 common 저장소만 구현하도록 범위를 정했다. 외부 소비자 검증까지 묶인 선행을 유지하면 UI·Python 후속 구현을 끝낼 수 없다. 이미 검증한 버전의 소스와 산출물을 보존하면서 구현과 릴리스의 완료를 구분해야 한다.

## 결정

1. npm·PyPI에는 게시하지 않는다. 이름 예약·계정 확보·가용성 확인·게시 재평가도 현재 계획에서 제외한다. 식별자는 `@kor-travel/tokens`, `@kor-travel/ui`, Python 배포 이름 `kor-travel-common`·import `kortravelcommon`으로 확정한다. 이는 공개 registry 소유권 확보를 뜻하지 않는다. 설치·로컬 검증은 common이 만든 tarball/wheel을 명시해 공개 registry의 동명 패키지로 대체되지 않게 한다.
2. GitHub Release의 tgz·wheel·sdist와 고정 Git 태그 채널은 유지한다. npm pack·uv build는 빌드/설치 검증이며 registry 게시가 아니다. 공개 범위나 외부 소비자의 권리 상태를 이 결정으로 변경하지 않는다.
3. common 자체 구현·검증을 마친 0.1 후보를 각각 T-109a(tokens), T-212a(UI), T-310a(Python)에서 보존한다. 이 하위 task가 DONE이면 다음 common 구현을 시작할 수 있다. T-201은 T-109a, T-205는 T-212a, T-306·T-307은 T-310a를 선행으로 한다. 이전 정식 릴리스는 구현 선행에서 제외한다. 0.2 후보의 보존은 T-213(UI)·T-311(Python)의 릴리스 준비 범위가 소유하며, 각 task가 검증한 해당 minor 전체 소스에서 새 후보를 만든다. 0.1 후보의 버전만 0.2로 바꾸지 않는다.
4. 후보에는 40자리 source commit, package/lock·툴체인, 실제 검증 결과, 산출물 이름·SHA-256을 기록한다. 검증한 commit을 원격 불변 annotated tag `candidate-<pkg>-<X.Y.Z>-<N>`으로 보존하고 원격 tag object와 peeled commit을 확인한다. 후보 tag는 Release 완료나 소비자 승인 표시가 아니다. 로컬 산출물을 재빌드해 digest를 대조하고, 검증한 바이트의 CI artifact 위치·만료도 기록한다. artifact가 만료되면 고정 source에서 재검증해 만들며 이전 바이트와 다르면 같은 evidence를 재사용하지 않는다.
5. 초기 구현의 미발행 `0.1.0` metadata로 로컬 pack/wheel 검증은 가능하다. 다음 minor 코드를 넣기 전에 main 개발 버전을 UI `0.2.0-dev.0`, Python `0.2.0.dev0`로 먼저 바꾼다. 이전 후보의 commit·tag·digest를 이동/덮어쓰지 않는다. 후보를 수정하면 번호를 올리고 해당 버전의 검증을 다시 실행한다.
6. 외부 rc·정식 릴리스는 보존 후보에서 분기한 패키지별 release branch에서 PR로 준비한다. 버전 metadata·lock·릴리스 기록만 변경한 rc도 build·설치·고지 검증을 다시 수행한다. 정식은 검증한 rc의 같은 소스에서 버전 metadata만 바꿔 만든다. 코드가 달라지면 새 rc와 소비자 재검증이 필요하다. main의 후속 구현을 과거 버전으로 내리거나 같은 공개 버전·태그·자산을 교체하지 않는다. 변경·병합은 PR을 거친다. 실행 상태의 정본은 현재 main 원장이다. release branch의 task 원장은 후보 시점의 역사 기록으로 유지하고 상태를 진전시키지 않는다. 준비 때 현재 main의 선행 완료·외부 evidence를 40자리 commit으로 고정해 릴리스 evidence에 연결한다. 발행 뒤에는 main 대상 문서 전용 PR로 완료 상태·evidence를 반영하며, 이전 패키지/lock 또는 release branch 전체를 main에 합치지 않는다. 상세 절차는 release §2.2를 따른다.
7. T-010은 재사용 워크플로·스모크 실행기와 common fixture 검증을 소유하고, 실제 외부 소비자 2곳 dispatch는 T-010a로 분리하고 T-109a의 보존 후보를 입력으로 요구한다. T-109는 T-109a·T-010a와 실제 map/weather 검증, T-212는 T-212a·정식 tokens와 실제 UI 소비자 검증, T-310은 T-310a와 실제 Python 소비자 검증을 요구한다. 후속 정식 T-213·T-311은 이전 정식 릴리스와 해당 소비자 채택/검증 조건을 계속 요구한다.
8. 외부 소비자 저장소에는 쓰지 않는다. 외부 gate는 담당 저장소·필요 evidence·후속 task가 있는 BLOCKED/NOT_RUN으로 남긴다. common fixture 성공은 소비자 성공을 대신하지 않는다. 라이선스·고지·불변 태그·승인 소비자·호환 peer·계약 시험·CHANGELOG와 이관 절 조건은 유지한다.

## 대안 검토

이전 minor 정식 발행을 기다리면 사용자가 지정한 common 구현 범위를 끝낼 수 없다. 외부 gate를 삭제하면 미검증 라이브러리를 검증된 것으로 표시하게 된다. 후보 보존과 별도 release branch는 관리 항목을 늘리지만, 버전별 결과를 잃지 않고 구현을 이어갈 수 있다. 공개 registry의 이름 확인은 이 채널에 필요하지 않다.

## 결과

common 구현 완료·후보 검증 완료·rc 검증·정식 발행·소비자 채택이 서로 다른 상태로 기록된다. 모든 common 코드가 구현돼도 외부 릴리스/채택 task가 BLOCKED일 수 있다. 이를 전체 제품의 출시 완료라고 표현하지 않는다.

## 후속·적용 위치

[패키지 계약](../architecture/packages.md), [릴리스 절차](../runbooks/release.md), [통합 계획](../plan/integration-plan.md), T-006·T-010/010a·T-109/109a·T-201·T-205·T-212/212a·T-213·T-306·T-307·T-310/310a·T-311·T-507을 동기화한다. T-006의 기존 계정 확보 범위는 사용자 지시로 철회되었으며 조회 성공으로 완료하지 않는다. 게시 정책을 재개하려면 새로운 사용자 지시와 ADR이 필요하다.
