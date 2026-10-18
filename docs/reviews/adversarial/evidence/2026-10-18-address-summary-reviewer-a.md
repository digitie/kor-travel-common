# Common40 주소 summary — James 독립 FULL 계약/소비자·UI 리뷰 r1

**판정: PASS (Common source·소유 fixture 범위). OPEN P0=0 / P1=0 / P2=0.**
Transport의 T86-B-P2-02 공통 원인은 아래 재현 범위에서 수정됐다. 소비자 pin/CI/UI 정식 closure 또는 운영 완료를 대신하지 않는다.

- 실행 ID: /root/review_finish_a.
- Base: 33a3382c2f605ca9135da676bed1ff42061d52fb.
- Exact head: 522525aed3db934767c1c9e742b3bfc68e91679c.
- Manifest: /home/digitie/dev/reverse-address-common-summary-review-manifest-20261018-r1.json.
- 실제 manifest SHA256: bcd2525457f337c86432bcabbc91d8dd249f47a84159b6185a3ad1ddf1b853ff.
- 시작 UTC: 2026-10-18T03:37:42.078279+00:00.
- 새 상대 Common40 결과는 보거나 요청하지 않았다.
- 기존 Transport r2 James 원문은 수정하지 않았고 SHA e312cd3fc00977a57c6358e6f8b1e3f320522cbb365b58cce47e336bbb8b28ed를 다시 확인했다. 이번 새 원인 검토를 과거 원문에 소급하지 않는다.

## 범위·규칙·격리

AGENTS, docs/README, 현재 resume 및 agent workflow/관련 reverse-address guide를 읽고 현재 source 계약을 대조했다. base→head **6파일 74+/2-** 전체를 읽었다:
CHANGELOG, journal, resume, guide, reverse_address.py, 그 시험이다. 전체6파일의 path+NUL+해당 head blob SHA256+LF 결박 SHA는 e20f832f88aba22c973354e297b6dc92083c6eeb34a8b6b7bf6c52a15a701425다.

실제 제품 delta는 DatabaseAddressSource.summary의 MAX 쿼리5줄뿐이다. 기존 class/callback/API signature, DTO/table/schema, provider, cache, save/error/reuse, owner/lease/cursor, sensor/scheduler, dependency·SDK pin 및 배포 설정은 변경되지 않는다. AST로 모든 함수 args/returns와 _joined의 동일성을 비교했다.

immutable git show와 소유 TemporaryDirectory/메모리 모듈만 사용했다. 제품/index/branch·다른 작업자의 변경/원문을 수정하지 않았다. 시작·종료 status는 clean이다. 임시 SQLite·pytest source/config는 종료 시 제거했다. 실제 environment/비밀/credentials, provider API/SDK 호출, 운영/SSH/Docker/Daemon은 0이다. SDK가 설치된 dependency interpreter를 사용했으나 이번 source/시험 경로는 실제 Dagster SDK를 import하거나 실행하지 않았다.

## 기존 원인·수정 경계

위치: packages/py/kor-travel-common/src/kortravelcommon/reverse_address.py:536–580, 특히 :551–556.

기존 구현은 entries의 provider_id만 걸고 resolved_at MAX를 구했다. 현재 source SELECT에서 숨기거나 삭제한 위치, 좌표가 바뀌기 전 파생 결과, 더 최근 orphan의 시각까지 “최근 정상 확인”으로 반환했다. items=[]/total0인데 마지막 정상 시각만 남아 무효 legacy 항구가 여전히 정상 확인된 것처럼 보일 수 있었다.

후보는 self._joined()에서 MAX를 구하고 entries.longitude/latitude가 현재 source와 같은 행만 포함한다. _joined():439–447은 provider_id+target_key로 원천에 outer join하는 기존 helper다. 새 where가 현재 좌표를 추가하므로 다른 provider/원천 밖 행/이전 좌표를 제외한다. 일치하는 행이 하나도 없으면 aggregate는 NULL이고 API의 nullable last_resolved_at 계약을 유지한다.

status==ok 조건을 새로 추가하지 않은 것은 의도된 보호다. 같은 좌표에서 재시도 오류가 나도 store.save가 보존한 마지막 정상 resolved_at을 계속 보여야 한다. 반대로 좌표가 달라지면 예전 정상 시각이 있어도 제외해야 한다. 이는 기존 sample/projection의 현재 좌표 경계와도 정합하다.

기존 T86-B-P2-02는 공통 원인 부분을 **FIXED_SOURCE**로 disposition한다. 현재 소비자 저장소는 별도 pin 변경 전까지 이전 c067을 사용하므로 소비자 결함 전체를 이 Common PASS만으로 최종 CLOSED 처리하지 않는다.

## 독립 old→new 실제 코드 matrix

작성자 시험을 재인용하지 않고 별도 fixture를 만들었다. base와 candidate reverse_address 모듈을 각각 불변 source에서 새 namespace로 로드하고 공개 DatabaseAddressSource/Store/refresh API로 과거 파생 결과를 생성했다. source는 key/좌표/active 컬럼의 소유 SQLite table이며 resolver 응답만 주입했다.

현재 정상 위치는 T0=2026-01-01, SELECT 제외 위치는 T1, 삭제될 위치는 T2에 정상 주소를 가진다. 같은 key/좌표에 T3의 다른 provider 결과도 넣었다. 시나리오에 따라 source를 제외/삭제/이동하거나 현재 sidecar를 미확인 상태로 만들었다. 실제 시간·provider 호출 결과가 아닌 소유 aware UTC fixture다.

| 시나리오 | 이전 base | 후보 | 판정 |
| --- | --- | --- | --- |
| 현재 source 필터로 목록 비움 | total0/items0인데 T2 | NULL | RED→GREEN |
| 현재 source 삭제로 목록 비움 | total0/items0인데 T2 | NULL | RED→GREEN |
| 경도 변경 | 이전 T2 | NULL | RED→GREEN |
| 위도 변경 | 이전 T2 | NULL | RED→GREEN |
| 유효 현재 위치 + 더 최근 orphan | T2 | 현재 위치 T0 | RED→GREEN |
| 현재 위치는 미확인, 다른 과거 행만 있음 | T2 | NULL | RED→GREEN |
| 같은 좌표 재실패 + 더 최근 orphan | T2 | 마지막 정상 T0, error/items 유지 | RED→GREEN |
| 더 최근 다른 provider 동일 key/좌표 | T0 | T0 | 기존·후보 양성 유지 |

총8쌍에서 이전7개 오류를 확인하고 후보8개 기대값을 확인했다. 임의 문자열/모의 MAX 값이 아니라 실제 SQL 실행 결과다. provider 격리 양성은 이전에도 맞던 계약이며 새 개선으로 부풀리지 않는다.

각 summary 실행 직전·직후 source/entries/control 전체 snapshot이 같았다. SQLAlchemy statement listener로 summary 및 내부 sample/projections의 모든 실행을 기록했을 때 **SELECT만** 있었다. 과거 행을 지우거나 덮어 결과를 만드는 fix가 아니다. 테스트 setup의 source 상태 변화는 소유 fixture에만 행한 것이다.

## 소비자/UI 계약 직접 smoke

Transport8c89의 실제 models/adapter를 별도로 불변 Git source에서 읽고, 후보 Common을 메모리 namespace에 주입했다. 소비자 파일/pin/index는 바꾸지 않았다.

- 이전 f8 admission 함수로 guideline legacy FerryPort 한 행의 정상 sidecar를 생성했다.
- 현재8c admission으로 같은 DB를 읽으면 total0/items=[]다.
- 후보 Common의 last_resolved_at은 NULL이다.
- 원천 FerryPort 전체 행과 legacy sidecar 전체 행은 그대로다.

현재 Admin date fallback은 NULL을 “미확인”으로 표시한다. 예전처럼 빈 현재 목록의 오래된 정상 확인 시각을 노출하지 않는 형태와 연결된다. 일반 locations/지도 원천 필드를 바꾸거나 frontend에서 legacy provenance를 임의 추정해 숨기는 방식이 아니다.

이것은 Transport source의 최소 in-memory Common 교체 smoke이며 정식 소비자 pin/wheel 설치·CI·실브라우저·native API 배포를 수행한 결과가 아니다. Weather에도 같은 public DatabaseAddressSource와 nullable field 계약을 사용하지만 이번에 Weather 앱을 새로 실행하지는 않았다. 두 소비자 후속 gate는 별도다.

## 고정 시험·회귀·계약 보존

candidate의 실제 test_reverse_address.py와 __init__/reverse_address source를 소유 임시 디렉터리에 추출했다. 별도 config, --noconftest, -p no:cacheprovider, plugin auto-load 비활성화와 Python -I/-B로 실행했다. **28 PASS /0.96초/exit0**.

기존 달력 월말·동일 좌표 재사용·실패/중단·소유권·cursor/retry·수동 auto-off 보호와 추가5회귀가 함께 통과했다. 본인 새 직접 matrix와 이28개 시험의 숫자는 동일 목적 검증을 포함하므로 하나의 full-suite 총수로 합산하지 않는다. 이번 실행 실패·환경 보정은 없었다.

다른 소비자 회귀를 의심하며 다음을 확인했다:
- public signature/추가 인자/반환 필드/type·schema 변경0.
- 기존 provider_id 격리 predicate는 그대로이고 새 MAX가 이를 재사용한다.
- provider/cached result/lease를 쓰는 경로가 아니라 읽기 aggregate만 바뀐다.
- sample50/좌표 해시 projection, 기존 실패 보존, API nullable field, source 자체의 정책 필터를 우회하지 않는다.
- 동일 좌표의 실패는 정상 날짜를 새 오류 시각으로 갱신하지 않는다.
- 새 source/sidecar 정리 DML·네트워크 요청·추가 provider 호출·Daemon start가 없다.

현재 소비자가 서로 다른 source SELECT를 쓰더라도 source의 key/longitude/latitude 계약은 이미 공통 연결의 필수 입력이다. 새 hidden global registry나 소비자 전용 상수를 도입하지 않았다. SQL 대상/응답 수가 성능 개선되었다거나 CPU/RSS가 줄었다고 측정하지 않았다.

## 문서·증거 정산

guide:64–66, changelog와 journal/resume는 현재 source·동일 좌표만 MAX라는 의미를 설명하고, 과거 sidecar/동일 좌표 마지막 정상일 보존을 명시한다. 운영 배포/CPU 최적화 완료로 표현하지 않는다. 소비자 pin·CI/UI가 후속임도 명확하다. 기존 실패 원문을 덮지 않고 새 Common 원인과 후속 gate를 구분한다.

Root가 전달한 5 FAIL→28PASS, 전체514PASS/117.23초(소유 Python3.12/Dagster1.13.25), 새 wheel 설치28/source hash 동일, Ruff·도구·link/plan·secret0은 외부 작성자 증거다. 본인 source28/독립8쌍과 합산하지 않는다. 실제 새 wheel을 설치한 검증이나 소비자 SDK1.13.24 환경 gate를 본인 실행했다고 쓰지 않는다. tools334PASS/3SKIP도 skip을 PASS로 바꾸지 않는다.

**Common40 CI는 요청 시 pending이며 PASS가 아니다.** 본인은 새 CI를 실행하거나 완료 상태를 추정하지 않았다. source/fixture PASS와 CI/소비자 gate가 다른 상태다.

추가 본인 정적 확인:
- 전체6파일 diff-check exit0.
- 변경 Markdown 상대 링크131회, 누락0(파일별 전체 링크를 검사했으며 새로 추가된 링크만 센 숫자는 아님).
- 원 Transport r2 보고서 SHA/내용 불변.
- 시작·종료 source worktree clean.
- candidate reverse_address.py SHA256: 3faada7c5099a5a97b0521d5dfa11f86dc817f2846ad3bcc94e37eaefa9fa2d8.

## 최종 판정·미실행 한계

**PASS / OPEN P0/P1/P2=0**, Common exact522525의 source/owned-fixture 범위다. filtered/deleted/빈 source/좌표 이동/새 orphan/provider 격리/동일 좌표 재실패·legacy UI의 재현 가능한 원인을 고쳤고, 이번 렌즈에서 새 차단 결함을 발견하지 못했다.

실제 PG dialect 실행/행락·운영 DB/API/제공자/키·프로덕션 배포·실브라우저·CPU/RSS·새 소비자 pin/wheel/전체 CI는 본인 NOT_RUN이다. root의 기존 별도 위임과 후속 작업을 새 승인 조건으로 바꾸지 않는다. 현재 Transport/Weather 소비자 정식 closure와 운영 완료는 이 보고서로 대체되지 않는다.

## 전달받은 요청 원문

```text
새 Common40 최소 수정의 FULL 독립 A 계약/소비자·UI 표시 렌즈 리뷰를 요청합니다. Transport r2 원문은 그대로 유지합니다. 같은 manifest /home/digitie/dev/reverse-address-common-summary-review-manifest-20261018-r1.json SHA256 bcd2525457f337c86432bcabbc91d8dd249f47a84159b6185a3ad1ddf1b853ff, base33a3382c2f605ca9135da676bed1ff42061d52fb → head522525aed3db934767c1c9e742b3bfc68e91679c, WT /home/digitie/dev/kor-travel-common-codex-address-summary-20261018. 목적은 결함 찾기, 모호하면 지적. 6파일 전체 delta(공통 MAX source+좌표 join·5반례·guide/journal/resume/changelog)를 immutable Git object로 검토. 기존 Transport B T86-B-P2-02의 별도 root 재현은5 FAIL→engine28PASS, 전체514PASS/117.23초, 새wheel설치28PASS/hash동일, Ruff/docslinks761/2956/0/plan109/0/tools334PASS3SKIP(Windows1/jsonschema미설치2)/secret0. CI pending은 PASS 아님. filtered/deleted/좌표이동, source비어있음, provider격리, 현재같은좌표재실패마지막정상시각, invalid legacy UI표시 계약, source/sidecar불변을 공격하고 기존다른consumer회귀 의심. 리뷰어 read-only, source/index/branch 변경·실제provider/env/secret/production/SSH/Docker/daemon 금지, 자기 소유 temp fixture/installed new wheel 또는 exact Git source만 검증. 다른작업자있으니 변경/되돌림 금지. 새 상대 Common40 결과는 둘 다 확정 전 보거나 요청하지 마세요. 원 요청 전문·manifesthash/commit·격리·시각·실패/미실행 한계·file:line/재현/심각도·disposition·PASS/CONDITIONAL/BLOCK와 OPEN P0/P1/P2를 /home/digitie/dev/reverse-address-common-summary-review-james-r1.md 원문으로 저장하고 hash와 verdict 보고. 소비자 pin 갱신/CI/UI는 별도 후속이며 운영완료/CPU절감으로 해석하지 마세요.
```

종료 UTC: 2026-10-18T03:42:26.548761+00:00
