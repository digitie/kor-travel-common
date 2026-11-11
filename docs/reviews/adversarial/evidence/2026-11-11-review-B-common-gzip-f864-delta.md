# B 독립 common gzip 한정 delta

reviewer B / Epicurus, 구현 비참여. runid `Epicurus-B-gzip-consumers-20261111T172634Z`.
UTC 2026-11-11T17:33:10.572048+00:00.

- 기준: common `2ec519255ec1af9fca18856d980e968ee15b80a8` → `f8643d56bd8ce4cc7ff3d730b31173a8583593a4`.
- 검토: Git object에서 읽은 tools/_scan.py와 tests/test_scan_gzip_members.py 두 파일 delta. source 수정 없음, 상대 raw/verdict 미열람.
- **verdict: PASS(한정 source delta).** 신규 B finding 없음. 기존 B-P1-08/09/10 FIXED와 COMMON4 원문 PASS는 당시 불변 관찰로 보존한다.

새 코드는 gzip.GzipFile의 다중 member 자동 해제 대신 zlib 단일 member의 완결 EOF/unused_data/unconsumed_tail을 검사한다. 추가 stream과 후행 padding까지 형식 거부한다. 모든 gzip stream을 지원하면서 header만 건너뛰는 부분 수용이 아니다. CRC/ISIZE/FHCRC와 제한 크기도 검증된다.

자체 입력으로 안전한 첫 tar gzip 뒤에 빈 gzip member를 연결하고 두 번째 member의 FNAME/FCOMMENT/FEXTRA 각각에 canary를 넣었다. 세 경우 모두 기존2ec는 accept·canary 미탐지였고 새f864는 ScanError로 거부했다. 반대로 extra 안 magic과 유효 header CRC를 가진 단일 member는 정상 허용됐다. 실제 값이나 traceback을 출력하지 않는다.

원본 focused scanner 회귀 **62 PASS**. 새9개 gzip method와 기존 scanner/prod 회귀를 포함한다. 연결 gzip·중첩 source·후행 bytes·CRC/크기/headerCRC·정확 한계·digest 예외 경계를 검사했다. 원격 exactf864 CI는 조회 시 연결 PR run이 없었으므로 이 보고서는 CI 전체 PASS가 아니다. UI/CSS/artifact source는 해당 두 파일 diff 밖이며 재포장/새 앱 승인으로 확대하지 않는다.

실행: PowerShell workdir C:\ → wsl.exe. Git show f864:<선택 source>로 자체 snapshot 생성 후 `PYTHONPATH=.:tests python3 -B -m unittest discover -s tests`; `python3 -B gzip-independent.py`. 증거는 review-B-common-gzip-f864-evidence/에 보존한다.
