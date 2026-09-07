# T-005c workflow 고정 참조·CI Node 선언의 정적 보고

- 상태: READY
- 우선순위: P2
- Gate: 도구 테스트·두 OS CI·2인 리뷰
- 선행: T-005, T-009

## 목표

T-009의 common 자체 workflow 검증과 구분해, 버전 검사기가 아직 읽지 않는 소비자 workflow 참조·Node 선언을 common의 로컬 fixture로 검사한다. 원격 실행 버전이나 SHA로 고정된 액션의 실제 major를 추정하지 않는다.

## 고정 결정

- [버전 규약](../standards/versions.md) §3.8의 고정 참조·§8의 미지원 한계, [CI 규약](../standards/ci-deploy.md) §4의 하드닝이 정본이다. 수치와 `actions.checked`는 `versions.json`만 소유한다.
- T-009 리뷰에서 확정된 범위 정정이다. 기존 checker에는 YAML 파서가 없으므로 이 task 전에는 자동 검사 성공으로 세지 않는다.
- common만 수정하며 Python 3.11 표준 라이브러리·기존 positional/manifest 입력을 유지한다. 소비자 변경은 T-403의 별도 PR이다.

## 구현 범위

1. `.github/workflows/*.yml`·`*.yaml`의 job/step `uses`와 `actions/setup-node`의 `node-version` 선언을 읽고 기존 보고서에 위치와 판정을 연결한다. 구현 전에 지원 YAML 문법과 미지원 표현의 판정을 버전 규약에 명시한다.
2. SHA·버전형 태그·이동 ref·local action·Docker action을 구분한다. 재사용 workflow의 이동 ref는 `FLOATING_REF`; 로컬 파일 참조는 존재 여부를 검증한다. SHA의 실제 액션 버전은 네트워크로 조회하거나 주석에서 추정하지 않는다.
3. 정적 Node 선언은 registry 하한과 비교한다. matrix·expression·파일 참조 등 해석하지 못한 Node 값은 `NO_ENGINES`로 남긴다. 지원 밖 참조 형태는 미확인 진단을 남기고 정상 고정으로 표시하지 않는다. 잘못되거나 지원하지 않는 구조를 조용히 건너뛰지 않는다.
4. 안전한 고정 참조·이동 참조·하한 미달·동적 값·인용·잘못된 YAML의 fixture와 회귀를 추가한다. manifest 입력에서도 저장소 루트의 workflow를 같은 방식으로 검사한다.

## 범위 밖

전체 YAML 해석기, 원격 CI 실행·설치 버전·액션 major 실측, Docker 이미지 버전 파싱, 소비자 저장소 수정·registry 게시. `actions.checked`를 근거 없이 활성화하지 않는다.

## 예상 변경 파일

`tools/check_versions.py`, 필요할 때 내부 파서 모듈, `tests/test_check_versions.py`, `tests/fixtures/versions/workflows/*`, `docs/standards/versions.md`.

## 수용 기준

- 동일 manifest/lock에 workflow 이동 참조를 추가하면 해당 경로·행의 `FLOATING_REF`가 실제 보고에 추가되고 모드 규칙을 따른다.
- 알려진 정적 Node 하한 미달은 `BELOW_FLOOR`, 동적/미지원 값은 `NO_ENGINES`이며 실제 설치본이라고 표기하지 않는다.
- 정적 참조·local 참조·미지원 구조를 구분한 테스트와 문법 계약이 일치하고 빈 범위·파싱 오류를 PASS로 집계하지 않는다.
- Windows/Linux의 판정이 같고 기존 npm·Python parser 회귀가 없다. 오류와 진단에 비밀·운영 값이 노출되지 않는다.
- 미구현 한계·자동 보고 범위·소비자 T-403의 실제 CI evidence가 서로 구분된다.

## 검증 명령

```bash
python3 -B -X utf8 -m unittest discover -s tests -p 'test_check_versions.py'
python3 -B -X utf8 tools/validate_document_links.py
python3 -B -X utf8 tools/validate_plan.py
git diff --check
```

Git Bash에서 동일. fixture CLI와 실제 결과를 구현 후 evidence에 추가한다.

## evidence

NOT_RUN(미구현). T-009의 버전 fixture CI는 현재 npm 입력 보고만 검증한다. 원본 finding A-P2-04·B-P2-04의 범위 충돌은 이 task와 정본 한계의 연결로 정정하며 기능 구현은 아직 완료하지 않았다. 담당은 common 유지자/이 task 실행 에이전트, 목표 시점은 기반 단계에서 T-005a/b 다음·T-011 이전이다.

## rollback 또는 release 차단 조건

기존 판정이 바뀌거나 미지원 입력을 정상으로 보고하면 merge하지 않는다. 도구 변경은 revert PR로 되돌릴 수 있으며 소비자 파일을 변경하지 않는다.
