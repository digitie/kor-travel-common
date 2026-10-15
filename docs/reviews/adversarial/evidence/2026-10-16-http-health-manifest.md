# HTTP 생존 점검 독립 리뷰 manifest

- 제품 commit: `10ed1bb968c286a88396ac43ddfa66780f75f9d5` / base `8d04353464ccfb4c1efe5c4725274581e4110600`.
- task: [T-319](../../../tasks/T-319-dagster-recovery.md), [적용 계약](../../../runbooks/http-health-probe.md).
- 두 reviewer는 같은 제품 commit과 이 manifest를 받고 immutable 최종 요청 commit을 Git 객체로 검토한다. 상대 원문은 읽지 않는다.
- A: HTTP 파싱·deadline·메모리·CLI 오류, B: core-only 패키징·소비자 계약·판정 범위. 두 관점 모두 실제 고장 반례를 확인한다.
- 범위: stdlib-only loopback GET 한 번·완전한2xx 헤더·전체 예산·16KiB·quietCLI. 제외: provider/DB/Dagster 상태·재시작·소비자 pin/서비스.

| 파일 | 제품 blob SHA256 |
|---|---|
| `CHANGELOG.md` | `bea084baf534f2aead7f2db42e212a8865593d58c622d0a2b488bc42b3990896` |
| `docs/journal.md` | `429f62000bb16ca78b44ebb77cdd16bc535c221b36a9ac8dc9d8a3f2d8e6bf80` |
| `docs/resume.md` | `f225f03d0842b1d9052dbafd51141eeed72f590607bb6e6a673b9765387d835b` |
| `docs/runbooks/http-health-probe.md` | `6554c78fcf7fa3f08f08370ec38c99d9203741a9d21ec2847304d5189a421e1d` |
| `docs/tasks/T-319-dagster-recovery.md` | `8677638180029f1d6657f3ab2fda613652202240b488782bab3f8aeb0a2eee69` |
| `packages/py/kor-travel-common/README.md` | `d53ed4d141547ae8b70e854b574e6b48a2326a67cdbc2acabdb1bf32067b7cea` |
| `packages/py/kor-travel-common/src/kortravelcommon/http_health.py` | `b397f920b2ad3e535eb0a06019889d9da1d7cc97e54278f065a92c47f73159e9` |
| `packages/py/kor-travel-common/tests/test_http_health.py` | `38f51deec9441eef4f81cee3abb2f959be92e319cd98b50fca15c4e699e2aaf1` |

## 실제 작성자 검증과 한계

- 잠긴 all-extras 환경에서 Python204PASS(신규44포함), Ruff PASS. 초기 E501103자 줄1건은 줄바꿈으로 고친 뒤 신규44와 Ruff를 재확인했다.
- 빈 core-only wheel 정상 설치·pip check·설치 모듈 SHA 동일·실제 loopback CLI200/503. wheel SHA `1fe9b2fef4f2e3e4743a2f5e7d1ad549e8fd20db2293494df5d77e4b733f3769`.
- 문서 링크694/2806targets·plan109오류0·도구337실행/336PASS1SKIP. manifest 추가 뒤 링크/공백 검사는 다시 실행한다.
- 전체 Python 검증 뒤 변경은 조건식 줄바꿈·테스트 한 이름·문서뿐이며 제품 함수 의미 변경은 없다.
- 별도 예약 분산 branch230을 포함하거나 합산하지 않는다. 소비자 통합 pin은 예약 코드를 보존한 commit에서 관련 gate를 다시 수행해야 한다.
- prototype CPU 단일 비통제 표본은 이 구현의 CLI·헤더 검증과 다르며 실제 운영 개선율/메모리·healthy·live는 NOT_RUN.
- 외부 HTTP/SSH/provider/DB/운영 mutation은 작성자 Common 검증에서0이다. loopback socket 시험만 실행했다.
