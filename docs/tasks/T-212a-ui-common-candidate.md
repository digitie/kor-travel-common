# T-212a UI 0.1 common 검증 후보 보존

- 상태: BLOCKED
- 우선순위: P1
- Gate: UI 타입·단위·접근성·pack 설치·후보 보존
- 선행: T-203, T-204, T-109a

## 목표

소형 13종과 공개 UI 계약을 검증한 UI 0.1 후보를 보존한다. 실제 map과 승인된 두 번째 앱 검증은 T-212에 남는다.

## 고정 결정

[ADR-014](../adr/014-common-implementation-without-registry-publishing.md)의 후보 보존·후속 구현 경계를 따른다. 구체적 tag·버전 전환·release branch 절차는 [release §2.1](../runbooks/release.md#21-common-후보-보존과-후속-구현)이 정본이다. 실제 소비자 gate와 라이선스 조건을 대체하지 않는다.

## 구현 범위

1. 선행 task의 후보 코드·계약·시험을 대조하고 아래 common 검증을 실행한다.
2. source commit·lock·툴체인·검증 결과·산출물 digest와 CI artifact/만료를 evidence에 기록한다. 같은 입력의 두 빌드 digest가 일치해야 한다.
3. 검증 PR merge 뒤 원격 후보 tag object와 peeled commit을 확인해 보존한다. 아직 이 태그나 산출물이 존재한다는 뜻은 아니다.
4. T-205의 다음 minor 구현은 이 task DONE 뒤 개발 버전부터 변경한다. T-212는 정식 tokens·실제 소비자 evidence를 계속 요구한다.

## 범위 밖

npm/PyPI 게시, 실제 소비자 저장소 수정·설치·빌드·배포, rc·정식 GitHub Release 발행. 해당 항목은 외부 릴리스 task에 남긴다.

## 예상 변경 파일

후보 evidence와 해당 패키지 검증·기록, CHANGELOG·task·journal·resume. 검증 결함을 수정하면 실제 변경 파일과 새 candidate를 명시한다. 원격 candidate tag와 CI artifact는 저장소 파일이 아니다.

## 수용 기준

- T-203 단위·접근성 시험과 T-204 마크업 계약, T-201의 지시문·타입·subpath·고지·webpack/Turbopack pack 설치 검증을 후보에서 실행한다. tokens peer는 T-109a에서 보존한 tarball을 함께 명시 설치하며 registry의 동명 패키지를 사용하지 않는다.
- 공통 후보 보존 절차의 모든 evidence와 원격 tag 확인이 존재하고 두 빌드의 digest가 같다.
- 실행하지 않은 소비자 검증은 NOT_RUN으로 외부 task에 연결한다. 후보 검증을 정식 발행이나 소비자 채택으로 표시하지 않는다.
- 문서 검증·해당 패키지 CI·독립 2인 리뷰를 마치고 미해결 P0/P1이 없다.

## 검증 명령

실제 패키지 빌드·시험·설치 명령은 선행 구현 task에서 확정한 명령을 후보 commit에서 실행해 evidence에 기록한다. 존재하지 않는 스크립트명을 성공한 명령으로 기록하지 않는다.

```bash
python3 -B -X utf8 tools/validate_document_links.py
python3 -B -X utf8 tools/validate_plan.py
git diff --check
```

## evidence

NOT_RUN(패키지 구현·선행 검증 전). source commit·tag object/peeled commit·도구 버전·CI run·시험 수/skip·두 산출물 digest·artifact 만료·외부 gate를 실행 후 기록한다.

## rollback 또는 release 차단 조건

후보를 바꾸려면 새 번호와 재검증을 사용한다. tag를 이동하거나 같은 evidence의 digest를 덮어쓰지 않는다. 설치·계약·고지·두 빌드 digest 또는 필수 리뷰가 실패하면 DONE으로 바꾸지 않는다. 외부 릴리스 gate는 별도 task에서 닫는다.
