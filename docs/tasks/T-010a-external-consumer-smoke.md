# T-010a 승인 소비자 2곳의 tokens 후보 dispatch 검증

- 상태: BLOCKED
- 우선순위: P1
- Gate: 외부 소비자 설치·빌드
- 선행: T-010
- 외부 선행: 사용자 범위는 common만 구현이다. 실제 소비자 설치·빌드 실행과 접근 권한·승인 evidence는 해당 저장소 담당자가 제공한다.

## 목표

T-010의 실행기로 승인된 map·weather 고정 커밋에 실제 tokens 후보를 설치해 검증한 evidence를 확보한다. common fixture 성공과 외부 소비자 성공을 분리한다.

## 고정 결정

[ADR-014](../adr/014-common-implementation-without-registry-publishing.md), [consumer adoption](../runbooks/consumer-adoption.md), [release](../runbooks/release.md)를 따른다. 원래 T-010의 실제 소비자 dispatch gate를 이 task로 옮겼으며 삭제하지 않았다.

## 구현 범위

1. T-010에서 검증한 consumers.pins.json의 map·weather source SHA와 권리/승인 상태, tokens 후보 commit·자산 URL·digest를 요청 문서에 기록한다.
2. 담당자가 실제 tarball 설치→type-check→webpack/Turbopack 빌드를 실행한 CI run과 사용한 pin·자산 바이트를 확인한다. 빈 입력·설치 생략·skip은 성공이 아니다.
3. 두 결과와 실패/NOT_RUN·수정 담당을 기록한다. T-109 정식 릴리스는 이 task DONE을 요구한다.

## 범위 밖

common 에이전트의 소비자 저장소 수정·설치·빌드, 실제 채택 PR merge, 미승인 pinvi 설치, npm/PyPI 게시. 승인 여부를 registry 조회 성공으로 대신하지 않는다.

## 예상 변경 파일

common 측 검증 요청·결과 evidence, 이 상세 task·journal·resume. 소비자 변경은 해당 저장소 task/PR이 소유한다.

## 수용 기준

- 승인된 서로 다른 두 소비자에서 같은 고정 후보의 실제 설치·type-check·webpack/Turbopack 빌드가 성공한 CI evidence가 있다.
- 자산 바이트 SHA-256·설치 lock integrity·source pin과 CI 입력을 대조했다.
- 실패와 미실행을 성공으로 표시하지 않고 T-109에 결과를 연결했다. 문서 검증·2인 리뷰를 완료했다.

## 검증 명령

```bash
python3 -B -X utf8 tools/validate_document_links.py
python3 -B -X utf8 tools/validate_plan.py
```

실제 dispatch 명령과 입력은 T-010 구현에서 확정한 인터페이스를 사용하고 실행 주체·run URL을 기록한다.

## evidence

NOT_RUN(소비자 저장소 실행은 현재 사용자 범위 밖, T-010 구현 전). 실행기를 작성하거나 명령을 기록한 것을 성공으로 세지 않는다.

## rollback 또는 release 차단 조건

한 곳이라도 미실행·실패 또는 미승인 소비자면 BLOCKED를 유지한다. 실패 시 새 후보와 재검증을 요청한다. 원천 저장소는 이 task에서 변경하지 않는다.
