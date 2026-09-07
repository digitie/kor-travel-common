# T-014 common 테스트 fixture 포트 점검 + ktdm sibling 포트 문서 정합성 요청

- 상태: BLOCKED
- 우선순위: P3
- Gate: 외부 확인
- 선행: 없음
- 외부 선행: ktdm `docs/ports.md` 갱신은 kor-travel-docker-manager 저장소의 결정·PR이다. common은 요청 문서만 만든다.

## 목표

common의 테스트 스모크·fixture가 일시적으로 사용할 포트 값을 점검하고, 포트 정본인 ktdm `docs/ports.md`에 소비자 sibling 대역(airport 140xx·weather 141xx)과 airport 14002 예외를 명시해 달라는 요청 및 `-latest` 컨테이너 접미 질의를 문서로 남긴다. `130xx`는 common 운영 대역이나 common 서비스 소유권으로 등록하지 않는다.

## 고정 결정

- [설계 브리프](../plan/design-brief.md) D-18 포트 절(정본은 ktdm `docs/ports.md`·슬롯 규칙 인용·common fixture 포트는 실행 시 주입·14002 예외·`-latest`는 ktdm 결정), O-24.
- [ci 조사](../survey/cross/ci-deploy.md) §1.9(포트 대역표), §3.1(슬롯 규칙 `12{n}00` DB·`01` API·`02` worker·`05` Web, sibling 등록, `130xx` 후보의 근거와 미확인 영역), §3.2(`container_name` `-latest` 접미 열린 질문).
- [weather 인벤토리](../survey/inventory/kor-travel-weather.md) §8 항목 19(141xx 대역), [airport 인벤토리](../survey/inventory/kor-travel-airport.md) §9(14002·옛 값 drift).
- 운영 호스트·IP는 문서에 적지 않는다(D-18 redaction, [문서 유지보수 runbook](../runbooks/documentation-maintenance.md) §7).

## 구현 범위

1. 로컬 점유 확인(WSL/Linux): `ss -ltnp | grep -E ':130[0-9]{2}\b'` 결과와 조사 저장소 7개의 compose·스크립트 grep(`130[0-9]{2}`) 결과를 evidence로 기록. Windows 보조 명령은 `docs/dev-environment.md`에만.
2. fixture 슬롯은 실행 시 환경변수나 테스트 runner가 임시 주입한다(`13001`·`13005`는 예시 기본값일 뿐 예약·운영 대역이 아니다). `docs/standards/ci-deploy.md`는 ktdm 정본과 fixture 사용 원칙만 인용한다.
3. 요청 문서 `docs/plan/requests/docker-manager-ports.md`: 소비자 sibling 2행(140xx airport·141xx weather), airport 14002 예외 등록(대안 14005 이전 비용 요약), `-latest` 접미 유지/제거 질의(ktdm `docker-targets.yml`·geo `docker_app.sh` 결합 비용 인용), 요청 일자·common 커밋. common `130xx` 운영 등록 행은 만들지 않는다.
4. 답변이 오면 `docs/dev-environment.md`·`ci-deploy.md`의 슬롯 표를 확정 상태로 갱신하고 이 task를 닫는다.

## 범위 밖

- ktdm `docs/ports.md` 직접 수정, airport 포트 이전 실행, 서비스명·컨테이너명 표준 적용(`ci` §3.2는 standards-be 문서), compose 파일 작성.

## 예상 변경 파일

예정 경로는 존재·실행 증거가 아니다. `docs/plan/requests/docker-manager-ports.md`, `docs/dev-environment.md`(슬롯 표), `docs/standards/ci-deploy.md`(포트 절 링크·3행).

## 수용 기준

- evidence에 점유 확인 명령·실행 환경·결과(빈 출력 또는 점유 항목)가 있고 조사 7 저장소 grep 결과가 fixture 예시 포트의 충돌 여부를 보여 준다.
- 요청 문서가 소비자 sibling 2행·14002 예외·`-latest` 질의를 포함하고 운영 호스트·IP 값을 담지 않는다(redaction guard 통과).
- `ci-deploy.md`가 포트 값 정본을 복제하지 않고 ktdm 문서를 인용한다.
- ktdm 회신(수용/변경)을 evidence에 기록한 뒤에만 `DONE`.

## 검증 명령

```bash
ss -ltnp | grep -E ':130[0-9]{2}\b' || echo "130xx free"
rg -n "130[0-9]{2}" docs/plan/requests/docker-manager-ports.md docs/dev-environment.md
python3 -B -X utf8 tools/check_prod_redaction.py; echo "exit=$?"
python3 -B -X utf8 tools/validate_document_links.py
```

Git Bash에서 동일(`ss`는 WSL에서 실행).

## evidence

- 점유 확인 결과·요청 문서 링크·ktdm 회신 일자를 이 절과 `docs/journal.md`에 남긴다. 회신 전은 `NOT_RUN(ktdm 회신 대기)`.

## rollback 또는 release 차단 조건

- 문서만 바뀌므로 `git revert` 1회로 원복한다.
- ktdm이 다른 대역을 지정하면 슬롯 표를 갱신하는 후속 PR로 대응하며 common 코드의 포트 상수는 이 확정 전까지 fixture 설정으로만 둔다.
