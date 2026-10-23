# Workspace metadata 갱신 주기 — 소스 검증 정산

- 제품 검토: `89ea368b47f2eec8886c0ff1d720edd843e65e52`, base `e746e4b`.
- 분류: FULL. 작성자가 아닌 A가 SDK private 상수/장애 판단 변경을 검토해 FULL에 동의했다.
- 범위: daemon 진입점60/180초 opt-in·240초 실패 유예·원 CLI/pool/환경 원복.
- 범위 밖: 소비자 pin·설정·운영 배포·실제 SIGTERM·같은 입력 CPU/RAM·신선도 효과.
- 최종 A/B 모두 SOURCE PASS, OPEN P0/P1/P2 0. 별도 원문 확정 전에 상대 결과는 전달하지 않았다.
- 격리: 고정 gitshow/diff object-only. 원본 F드라이브의 미커밋 변경은 사용하지 않았다.

## 원문과 기준선

[manifest](evidence/2026-10-23-workspace-refresh-manifest.md),
[A 원문](evidence/2026-10-23-workspace-refresh-reviewer-a.md),
[B 최초 원문](evidence/2026-10-23-workspace-refresh-reviewer-b.md),
[B 후속 원문](evidence/2026-10-23-workspace-refresh-reviewer-b-postfix.md).

manifest의46b3 후보에 최종89ea의fixture 인증값 제거1줄을 같은 지시문으로 추가했다.
실행 제품 소스 tree는 둘이 같으며 두 reviewer 모두89ea를 최종 확인했다.
시작 시각은 별도로 기록하지 않았고 종료 시각은 원문에 보존했다.
A에게 전달한 핵심은 실행·장애계약·프로세스범위·예외/중첩/환경/CLI/pool 수명,
B에게 전달한 핵심은 SDK private 상수/설치profile·wheel·입력 거부·문서/유예 경계다.

## 검증과 실패 보존

- 작성자 잠긴Python3.12 전체661 PASS160.00초, 별도Python3.13 전체661 PASS155.87초.
  fixture 최종1줄 수정 뒤 집중52 PASS4.46초. 제품 소스는 같고 최종CI도 아래 정확89ea다.
- Ruff·문서783개/3001targets·plan109 오류0. wheel 별도 설치에서 모듈경로/CLI metadata,
  실제 SDK180초 profile/원복 PASS. wheel SHA256은 B 원문에 보존했다.
- 최초46b3 CI secret-scan/tools 실패는 새 테스트의합성URL-CREDENTIAL 규칙 위반이었다.
  예외/스캔완화 없이 인증값 없는 fixture로 고쳐89ea CI8개 모두 SUCCESS를 확인했다.
  [문서·양OS 도구·스캔·packages CI](https://github.com/digitie/kor-travel-common/actions/runs/39925414740),
  [Python3.11/3.13 CI](https://github.com/digitie/kor-travel-common/actions/runs/39925414822).
- CI의 도구 unittest는337실행/334PASS/3SKIP다. 로컬 NTFS의 같은 검사는 진행중인 다른
  검증의IO를 줄이기 위해 CI양OS 성공 확인 뒤 중단했다. 로컬 도구 전체PASS로 세지 않는다.
- 이 closure는 원문/정산/색인만 추가한다. 제품·정책·수용 조건은 변경하지 않는다.

## 외부 gate

소비자의 immutable wheel pin/설정·실제 daemon drain/시작/정상종료·기존 작업과
heartbeat/sensor·배포 반영 지연·동일 조건3쌍 CPU/RAM 검증은 NOT_RUN이다.
소스 검증을 전체CPU저감이나 Track1/2 완료·운영 활성화 승인으로 확대하지 않는다.
