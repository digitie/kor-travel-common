# 주소 확인 시각 집계 후속 독립 리뷰 종결

상태: COMPLETE. **A/B FULL SOURCE PASS, OPEN P0/P1/P2=0.**
기준33a3382c2f605ca9135da676bed1ff42061d52fb → 제품522525aed3db934767c1c9e742b3bfc68e91679c.
Transport86 r2의 T86-B-P2-02 SQL 원인을 현재 source·동일 좌표 MAX로 수정했다.
원천·과거 파생 행을 삭제하지 않으며 같은 좌표 재실패의 마지막 정상일은 보존한다.

두 리뷰어는 같은 immutable manifest를 독립 검토했고 새 상대 결과는 양쪽 원문 확정 전 비공개였다.
A는 소비자/UI 계약·8쌍 비교·Transport 실제 모델 smoke·엔진28개를, B는 SQL NULL/empty/provider/
중복 MAX·읽기 전용 불변과 40개 묶음을 직접 검사했다. 중복 목적의 숫자는 합산하지 않는다.
원문에 요청 전문·관찰 hash·격리·시각 수집 여부·미실행 한계가 있다.

작성자 반례5 FAIL→엔진28 PASS, 잠긴 Python3.12/Dagster1.13.25 전체514 PASS/117.23초,
새 wheel 설치28 PASS/source SHA 동일, Ruff/link761문서2956target0오류·plan109/0오류·secret1180/0발견을 확인했다.
도구337실행은334PASS/3SKIP(Windows8.3 API1·jsonschema 미설치2)이며 skip은 PASS가 아니다.
제품5225의 현재 CI8개는 모두 SUCCESS다. 이 closure commit은 사용자 문서 CI 생략 지시에 따라 별도 CI를 실행하지 않는다.

소비자 Weather113/Transport86의 새 pin·CI/UI와 운영 migration/provider/배포/실측은 별도다.
옛 c067 소비자에서 열린 지적을 이 Common SOURCE PASS로 소급해 닫지 않는다.
Track1·2 전체 뒤 수집기 CPU/RSS 개선과 Daemon OFF를 유지한다.

## 원문과 무결성

| 원문 | SHA256 |
| --- | --- |
| [2026-10-18-address-summary-reviewer-a.md](evidence/2026-10-18-address-summary-reviewer-a.md) | c8d2899a3fcb0e695f74000198c710a5981df2bc444c4dc1d81327ab316f5d0e |
| [2026-10-18-address-summary-reviewer-b.md](evidence/2026-10-18-address-summary-reviewer-b.md) | a668a5c125f5235bc2fdf71de0f8372d87b1a53ec4641a7966bbe949b044659f |
| [2026-10-18-address-summary-manifest.json](evidence/2026-10-18-address-summary-manifest.json) | bcd2525457f337c86432bcabbc91d8dd249f47a84159b6185a3ad1ddf1b853ff |
| [2026-10-18-address-summary-source-ci.json](evidence/2026-10-18-address-summary-source-ci.json) | d0539dcad2ae7321abfe30bf3c7d3aacac650e55d1aac7025b9df677f88cf0f8 |
| [2026-10-18-address-summary-root-verification.json](evidence/2026-10-18-address-summary-root-verification.json) | 2d98ea577d64ea88c303cf083e04ed8b1a86b70e3579892298c671a2d1ef9c08 |
