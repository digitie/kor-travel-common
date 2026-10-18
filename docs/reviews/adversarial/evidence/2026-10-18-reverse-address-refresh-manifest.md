# 주소 갱신 독립 리뷰 manifest·실행 기록

## 요청과 수용 범위

Weather·Transport에서 VWorld 우선·Kakao fallback, 위치별 달력 6개월 자동 주소 확인과 Admin 수동 예약을 제공한다. 원천 주소·관리자 좌표·과거 fact를 보존하고, 작은 순차 배치·확인일 보존 캐시·영속 커서·lease fencing·실패 backoff를 공통 Python으로 구현한다. Daemon OFF를 임의로 바꾸지 않는다.

정식 대상은 Common PR39의 전체 변경이다. 소비자 PR111·86은 연결 문맥만 보며 정식 소비자 리뷰·merge·배포 승인은 별도다. 두 리뷰어는 Git object만 읽고 소유 임시 fixture에서 검증하며 상대 새 결과는 최종 확정 전 열람하지 않는다. 실제 키·provider 요청·운영 SSH·운영 DB·Daemon 기동은 범위 밖이다. 기준 규칙은 [agent workflow §5](../../../runbooks/agent-workflow.md#5-전문-리뷰어-서브에이전트-2인-적대적-리뷰), 제품 계약은 [구현 가이드](../../../reverse-address-refresh.md)다.

## 불변 manifest

| 실행 | base → head | 원본·SHA256 |
| --- | --- | --- |
| r1 | c48595880aaad4367802ad71af2525a8a5e17c6a → 812b291659e40564595c3c28b7e8d51cbcc46df9 | [원본 JSON](2026-10-18-reverse-address-refresh-r1-manifest.json), 92f7e3b810c510e5ad26d109e294414ffa44db81ebd2edbe907af0fbf544a486 |
| r2 | 같은 base → 0f768a1974a65bfade4c0fa3c79b897c9663e1a6 | [원본 JSON](2026-10-18-reverse-address-refresh-r2-manifest.json), 3bbc3ae25d6c70a7fb36afc3229c81d411dc3f2c17117ef5386bc4de394d9d91 |

소비자 문맥 SHA는 원본 JSON에 고정돼 있다. r1 최초 전달 메시지의 byte 원본은 별도 저장하지 못했으므로 이 파일이 그 원문이라고 주장하지 않는다. r1의 실제 받은 범위·격리·실행 ID·관측 hash와 시각 한계는 두 원본 보고서에 보존돼 있다. 현재 제품의 전체 재검토는 r2다.

## r2 전달 입력 원문

### A — /root/review_finish_a

Common PR39 수정 후 독립 적대 리뷰 r2를 진행해 주세요. 읽기 전용이며 소비자 저장소는 문맥만 봅니다. /home/digitie/dev/reverse-address-review-manifest-20261018-r2.json (SHA256 3bbc3ae25d6c70a7fb36afc3229c81d411dc3f2c17117ef5386bc4de394d9d91)를 확인하고 Common base c48595880aaad4367802ad71af2525a8a5e17c6a -> head 0f768a1974a65bfade4c0fa3c79b897c9663e1a6의 전체 변경과 이전 본인 지적 해결을 검토해 주세요. 실행 가능한 독립 회귀 검증 및 새로운 신뢰성/보안/재시도 문제를 확인하세요. Common CI14개 성공. 프로덕션/실제 provider 호출/daemon 시작/코드 수정 금지. 소비자 미커밋 타입 보정은 검토 범위 제외하고 immutable git object를 사용하세요. 새 상대 리뷰 결과는 공유하지 않습니다. 원문 보고서를 /home/digitie/dev/reverse-address-review-james-r2.md 에 저장하고 hash, 판정, P0/P1/P2, 검증 한계를 알려 주세요. Windows에서 WSL Ubuntu-26.04로 경로 접근 가능합니다.

### B — /root/review_finish_b

Common PR39 수정 후 독립 적대 리뷰 r2를 진행해 주세요. 읽기 전용이며 소비자 저장소는 문맥만 봅니다. /home/digitie/dev/reverse-address-review-manifest-20261018-r2.json (SHA256 3bbc3ae25d6c70a7fb36afc3229c81d411dc3f2c17117ef5386bc4de394d9d91)를 확인하고 Common base c48595880aaad4367802ad71af2525a8a5e17c6a -> head 0f768a1974a65bfade4c0fa3c79b897c9663e1a6의 전체 변경과 이전 본인 지적 해결을 검토해 주세요. 실행 가능한 독립 회귀 검증 및 새로운 동시성/재시도/누락 문제를 확인하세요. Common CI14개 성공. 프로덕션/실제 provider 호출/daemon 시작/코드 수정 금지. 소비자 미커밋 타입 보정은 검토 범위 제외하고 immutable git object를 사용하세요. 새 상대 리뷰 결과는 공유하지 않습니다. 원문 보고서를 /home/digitie/dev/reverse-address-review-popper-r2.md 에 저장하고 hash, 판정, P0/P1/P2, 검증 한계를 알려 주세요. Windows에서 WSL Ubuntu-26.04로 경로 접근 가능합니다.

## 독립 실행과 원문 무결성

두 실행 ID·역할은 위와 같다. 각 실행의 시작 분·초는 사전 계측하지 않았으며 추정 시각을 만들지 않는다. 종료 UTC, 실제 관측 commit, object-only 격리 및 미추적 작성자 로그 보존은 각 원문에 기록했다. 아래 원문은 byte 그대로 복사하고 SHA256을 대조했다.

| 실행 | 원문 | SHA256 |
| --- | --- | --- |
| A r1 | [James](2026-10-18-reverse-address-refresh-r1-reviewer-a.md) | 287f22c998eb0a38cc8f223de5d88f3848e1cc66a3435dd71f8fcfcde28a4b65 |
| B r1 | [Popper](2026-10-18-reverse-address-refresh-r1-reviewer-b.md) | bba5179c431df1efeaeb6e81ca5904651d4853d8d2b9193fe4abe9bdda10c458 |
| A r2 | [James](2026-10-18-reverse-address-refresh-r2-reviewer-a.md) | 37c24ba0a0412bc1952248e77e65a60c65555153faee1d7c85758117ec4a76db |
| B r2 | [Popper](2026-10-18-reverse-address-refresh-r2-reviewer-b.md) | 40e583ec972b72ec4a311c1ee5106cef2f50b29a0289efda09954adbfa579fc6 |
