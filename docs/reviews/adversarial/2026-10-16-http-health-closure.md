# HTTP 생존 점검 최종 리뷰 판정

- Review ID: common32-http-health-closure-20261016.
- 종류: 전문 리뷰어 2인의 독립 FULL 및 post-fix 재검토.
- 초기 review commit: c7b55aec8e2de6ac70b8f2ef21e2fc18df87c0ce / 제품10ed1bb968c286a88396ac43ddfa66780f75f9d5 / base8d04353464ccfb4c1efe5c4725274581e4110600.
- 수정 제품: 001b03eb9a6b85bb7921d4d55a7f7fdf265c1160 / 최종 review commit: b483f5fc02f524f3c3aa6ea90f029835bdc9fcfd.
- 요청·범위: [T-319](../../tasks/T-319-dagster-recovery.md)의 core-only HTTP 함수·CLI. [초기 manifest](evidence/2026-10-16-http-health-manifest.md)의9파일, [수정 manifest](evidence/2026-10-16-http-health-post-fix-manifest.md)의5파일+manifest delta.
- 범위 밖: 소비자 pin/이미지/서비스 변경, provider·DB·Dagster run 판정, 재시작 정책, 실제 운영 CPU·메모리·UI 검증.
- Coordinator: root. 이 closure는 확정 원문·disposition·검증 범위·index만 보존하며 제품·규범을 바꾸지 않는다.
- 상태: COMPLETE. **최종 verdict: PASS / 양쪽 새 열린 finding0.**

## 독립 기준선과 원문

두 reviewer는 같은 immutable manifest로 검토했고 최초 원문과 post-fix 원문이 각각 고정되기 전에는 상대 원문·모형을 읽지 않았다. 아래5파일은 private 원본과 SHA256이 동일한 바이트로 복사했다. B 최초 원문의 기존 파일 이름 열거 오류는 원본을 보존하고 별도 정정본으로 연결한다. 판정·finding·기계적 blob 대조 결과는 바뀌지 않았다.

| 단계·원문 | 실행 ID·전문 영역 | 격리·시간(UTC) | verdict·SHA256 |
| --- | --- | --- | --- |
| [초기 A](evidence/2026-10-16-http-health-reviewer-a.md) | common32-http-health-review-a-20261016 / HTTP 파싱·deadline·메모리·CLI | c7b Git 객체+별도 archive, 원 WT 전후 clean / 17:40:01~17:42:45 | CONDITIONAL / bac15d53e67843aaaf66b0be8582211ad8f17e16040484d2eb5f24144fa15849 |
| [초기 B 원문](evidence/2026-10-16-http-health-reviewer-b-original.md)·[정정본](evidence/2026-10-16-http-health-reviewer-b.md) | common32-http-health-review-b-20261016 / core-only 패키징·소비자·CLI | c7b detached WT 전후 clean / 17:38:49~17:43 이후 | CONDITIONAL / 원문79e701971b4a54cfe4460f3b55deb38fd057c33ee7ad2d6eafa744166579893d / 정정b0479f7df5750235095d73c8b66ec190912fcc7a7a3eeeb07defb59c406dfa68 |
| [수정 후 A](evidence/2026-10-16-http-health-post-fix-reviewer-a.md) | common32-http-health-postfix-review-a-20261016 / HTTP·deadline·메모리·CLI | b483 Git 객체+별도 archive, 원 WT 전후 clean / 17:59:16~18:00:03 | PASS / 04c8bead8d6854b17730005782a7fd8ee5c368f3f4239a88794021744bc6ca17 |
| [수정 후 B](evidence/2026-10-16-http-health-post-fix-reviewer-b.md) | common32-http-health-post-fix-review-b-20261016 / 패키징·소비자·CLI | b483 새 detached WT 전후 clean / 17:59:37~18:00:29 이후 | PASS / 8aa8abae5130bbd05bb7a7ae37e8bdafb08bcac016003a932947b63347019a0b |

날짜는 표의 모든 시각에서2026-10-15 UTC이며 문서 날짜2026-10-16 KST와 같은 실행이다. 측정하지 않은 선행 읽기 시각은 원문 한계대로 남겼다. 각 원문에 전달 요청·실제 관찰 commit·시험·미실행 범위를 보존한다.

## Finding과 disposition

| ID | 심각도·근거 | 영향·권고 | 상태·수정·원 reviewer 재확인 |
| --- | --- | --- | --- |
| A-P2-01 | http_health.py 상태 줄 split의2요소 허용. 실제 HTTP/1.1 200 및 HTTP/1.0 204 뒤 필수 SP 없는 응답을 True로 판정 | malformed 응답의 fail-closed 누락.3요소 요구, 빈 이유문구의 SP 유지 | FIXED / 001b03e의 조건1개+회귀4개 / 최종 A가 실제 동일 반례2개 거부·빈 이유2개 유지·CLI 거부 확인 |
| B-P2-01 | 같은 상태 줄 경계. 실제 Python3.11 core-only 설치 함수가 누락 SP를 True로 판정 | 일반 HTTP 수신자의 관대한 파싱을 보안 결함으로 확대하지 않고 이 task의 완전 헤더 계약 기준으로 수정 권고 | FIXED / 같은001b03e / 최종 B가 독립 설치 모형의 초기15PASS1FAIL→수정16PASS0FAIL 확인 |

두 finding은 같은 근본 원인의 독립 재현이지만 ID·심각도·초기 CONDITIONAL 원문을 각각 유지한다. P0/P1은 최초·최종 모두0, 새 P2/P3와 DEFERRED/OPEN은0이다.

## 검증 계보

숫자는 독립 실행별 결과이며 서로 합산하지 않는다.

| 수행자·단계 | 실제 검증 | 결과와 범위 |
| --- | --- | --- |
| 작성자 초기 | 잠긴 all-extras Python·신규 회귀·Ruff·core-only wheel 설치·CLI | 전체204/신규44 PASS, 초기 wheel1fe9b2fef4f2e3e4743a2f5e7d1ad549e8fd20db2293494df5d77e4b733f3769. 초기 Ruff103자1건 실패 후 줄바꿈하고 재검증 |
| 작성자 수정 | uv run --no-sync pytest -q / ruff check . / 빈 core-only 설치·pip check·실제 CLI | 전체208/신규48 PASS·102.11초, wheel b0efb0f0cbb3a0b772fb205af4ef1dc8a8d690d28ed0dfa1ee61a3edcf8f3096,200/503/누락SP CLI0/1/1 |
| 작성자 문서 도구 | 링크·plan·도구 unittest | 수정 문서 링크695/2809targets·plan109오류0. 도구337실행 중336PASS1SKIP는 코드 수정 전의 별도 실행이며 skip을 PASS에 넣지 않음 |
| 독립 A 초기→수정 | Python3.11.15 archive 실제 loopback·deadline 대역·CLI | 초기29검증군+별도 malformed2 RED, 수정32검증군 PASS. 헤더16KiB/총예산/연결 정리/quiet CLI·누락SP2 거부. 전체208·wheel 설치를 본인 실행으로 합산하지 않음 |
| 독립 B 초기 | immutable source 경로 확인 후 전체 Python·Ruff·빈3.11 core-only 설치 | 전체204PASS102.28초. 모형15PASS1FAIL. 최초44의 잘못된 import 경로 실행은 독립 gate로 제외한 원문 보존 |
| 독립 B 수정 | 새 immutable source 대상48·Ruff·새3.11 wheel 일반 설치·pip check·실제 모형 | 48PASS0.29초·모형16PASS0FAIL. 설치 모듈 SHA dafb57227662e1298675017be9de04ad602cbeb1a383dcb029e387792c9ec4f6, Common distribution만 설치·선택 의존 import0 |

기존5개 Python 파일과 py.typed·pyproject/uv.lock의 바이트를 유지했다. 새 모듈은 stdlib-only이며 기존 Dagster·HTTP extra를 eager import하지 않는다. 본문 의미·전체 Python RSS16KiB 보장·운영 worker 성공을 선언하지 않는다. 모듈 호출 예산4초와 Python 시작/import·Docker 전체 timeout도 구분한다.

## Closure 문서 확인

이 원문·disposition·index 기록 뒤 실제 문서 링크702개/로컬 대상2820개 오류0, task109개 metadata/DAG 오류0, 도구337시험 중336PASS/1SKIP(73.780초), git diff --check를 통과했다. 작성자 초기 도구 실행과 별도인 closure 실행이며 skip을 PASS에 합산하지 않는다. 제품 코드·시험·설정은 이 commit에서 변경하지 않았다.

## 외부 선행과 원본 보존

[적용 가이드](../../runbooks/http-health-probe.md)의 소비자 exact pin·lock·이미지 설치 source 검증과 직접 생존 경로·실제 healthy·반복 CPU/메모리·live UI는 NOT_RUN이다. prototype의 단일 비통제 CPU 표본은 이 완전한 헤더/CLI 구현의 운영 개선율이 아니다. 이 PR은 운영에 아직 배포하지 않았다.

Common32의 기준 main8d043은 별도 Common31 phase 예약 개선을 포함하지 않는다. 소비자 통합 시 두 후보를 보존한 commit으로 pin하고 관련 예약·패키징·소비자 회귀를 다시 수행해야 한다. 이 closure나 PASS는 Common31 merge·소비자 채택 완료를 뜻하지 않는다.

원문은 비밀/자격·운영 호스트/로그 원문을 포함하지 않는지 직접 읽었다. 포함된 외부 링크는 RFC 공식 문서이며 주소 리터럴은 loopback 시험용127.0.0.1뿐이다. 로컬 reviewer 경로·실행 ID·검증 한계는 원형대로 보존했다. 제품 수정·운영 변경·자동 재시도·브라우저/SSH/외부 API 호출은 이 closure 작업에서0이다. exact source CI와 최종 merge는 PR #32의 별도 gate다.
