# T-005c workflow 고정 참조·CI Node 선언의 정적 보고 (2026-09-07, PR #8)

- 상태: DONE
- 우선순위: P2
- Gate: 도구 테스트·두 OS CI·2인 리뷰
- 선행: T-005, T-009

## 목표

T-009의 common 자체 workflow 검증과 구분해, 버전 검사기가 아직 읽지 않는 소비자 workflow 참조·Node 선언을 common의 로컬 fixture로 검사한다. 원격 실행 버전이나 SHA로 고정된 액션의 실제 major를 추정하지 않는다.

## 고정 결정

- [버전 규약](../standards/versions.md) §3.8의 고정 참조·§8의 미지원 한계, [CI 규약](../standards/ci-deploy.md) §4의 하드닝이 정본이다. 수치와 `actions.checked`는 `versions.json`만 소유한다.
- T-009 리뷰에서 확정된 범위 정정이다. 기존 checker에는 YAML 파서가 없으므로 이 task 전에는 자동 검사 성공으로 세지 않는다.
- common만 수정하며 Python 3.11 표준 라이브러리·기존 positional/manifest 입력을 유지한다. 소비자 변경은 T-403의 별도 PR이다.
- 제한 YAML parser의 block map/list는 2칸씩 증가하는 들여쓰기만, flow sequence는 scalar와 trailing separator 없는 형태만 지원한다. 그 밖의 YAML 표기는 전체 YAML 호환을 주장하지 않고 exit 2로 닫는다.

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

구현·fixture·정본 문서·두 OS 검증을 완료했다. 최종 code candidate `5807e535c16310c41c21f9efce87b2113aa17ee5`의 PR CI `34097813843`에서 5개 job이 성공했고, 두 독립 reviewer가 누적 finding을 모두 FIXED로 확인해 PASS했다. 이후 문서 수정 candidate `7b35ff07b077cef85d7d0d6e0971cacff210374f`도 PR CI `34099960667`의 5개 job과 두 독립 docs reviewer PASS를 확인했다. 최종 통합 evidence는 [T005c 최종 리뷰](../reviews/adversarial/2026-09-07-t005c-post-fix-03.md), [문서 post-fix 판정](../reviews/adversarial/2026-09-07-t005c-docs-post-fix.md)과 [post-fix-03d manifest](../reviews/adversarial/evidence/2026-09-07-t005c-post3d-manifest.md)다. Windows/WSL 전체 179개·focused 84개 테스트, 문서·계획·SPDX·secret/redaction·self-check validator가 모두 skip/오류 없이 통과했다. 소비자 저장소·npm/PyPI는 건드리거나 게시하지 않았다.

실행 결과와 두 reviewer의 원본은 최종 리뷰 report와 evidence에 보존한다. 패키지 build/install, 실제 소비자 workflow·CI·e2e, 원격 action major·Docker image 조회는 범위 밖이며 `NOT_RUN(사유)`다. 다음 순차 task는 T-011이다.

## rollback 또는 release 차단 조건

기존 판정이 바뀌거나 미지원 입력을 정상으로 보고하면 merge하지 않는다. 도구 변경은 revert PR로 되돌릴 수 있으며 소비자 파일을 변경하지 않는다.
