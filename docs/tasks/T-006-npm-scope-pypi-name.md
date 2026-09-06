# T-006 공개 registry 이름 확보 철회와 패키지 식별자 확정 (2026-09-07, PR #4)

- 상태: DONE
- 우선순위: P1
- Gate: 사용자 범위 변경 기록·문서 검증
- 선행: T-015

## 목표

사용자의 npm/PyPI 미게시 지시에 따라 기존 계정·이름 확보 작업을 철회하고 파일 배포에 사용할 식별자를 확정한다. 기존 조회·예약 acceptance를 실행한 것처럼 완료하지 않는다.

## 고정 결정

[ADR-014](../adr/014-common-implementation-without-registry-publishing.md)가 기존 O-5와 ADR-005의 이름 확보 조건을 대체한다. 이름·배포 단위는 [packages](../architecture/packages.md#1-요약표)에 있고 공개 registry 소유권 확보를 뜻하지 않는다.

## 구현 범위

1. 기존 npm 조직 확보·npm/PyPI 조회·실패 시 개명 범위는 사용자 지시로 철회했음을 기록한다.
2. 현재 architecture·standards·runbook·구현 task에서 이름 확보·자동 개명·소비자 채택 차단 조건을 제거하고 확정 식별자로 연결한다.
3. T-015의 문서 검증·두 독립 리뷰 완료 뒤 이 범위 변경 기록을 종료한다. 기존 ID·파일을 유지하여 과거 참조를 보존한다.

## 범위 밖

npm/PyPI 계정 생성·예약·가용성 검사·게시. package.json·pyproject 실물 생성과 pack/wheel 검증은 T-101·T-201·T-302의 몫이다.

## 예상 변경 파일

T-015에서 수정하는 배포 단위 정본과 관련 규약·task·원장. 이 task는 별도의 registry 실행 파일이나 계정 정보를 만들지 않는다.

## 수용 기준

- 사용자 지시와 ADR-014에 기존 범위 철회·새 식별자 결정이 명시되어 있다.
- 현재 규범과 실행 task에 이름 확보 실패로 개명하거나 첫 소비자 PR을 차단하는 조건이 없다.
- T-015의 문서 검증·두 리뷰가 완료되고 원장이 이를 추적한다. registry 확보/미확보의 조사 결과를 만들어내지 않는다.

## 검증 명령

```bash
python3 -B -X utf8 tools/validate_document_links.py
python3 -B -X utf8 tools/validate_plan.py
```

## evidence

2026-09-07 사용자: “npm pypi 에는 안 올릴꺼야”. 기존 계정 확보 acceptance는 이 지시로 철회했다. npm/PyPI 이름 조회·예약은 NOT_RUN(요청 범위에서 제외)이며 성공으로 판정하지 않는다. T-015의 문서 검증과 [최종 두 독립 PASS](../reviews/adversarial/2026-09-07-t015-post-fix-03.md)를 확인해 변경된 범위의 기록을 종료했다. registry 소유권 확보나 기존 조회 acceptance의 성공을 뜻하지 않는다. 과거 범위는 PR #3 병합 기준의 Git 이력에 보존한다.

## rollback 또는 release 차단 조건

새 사용자 지시 없이 공개 게시·이름 확보 작업을 재개하지 않는다. 현재 채널의 실제 패키지 설치·릴리스 gate는 해당 task에서 별도로 검증한다.
