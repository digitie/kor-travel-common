# Common40 summary 최소 수정 — Popper 독립 FULL 리뷰

**Verdict: PASS (COMMON_SOURCE_ONLY). OPEN P0=0 / P1=0 / P2=0.**
T86-B-P2-02의 SQL 원인은 이 Common 후보에서 FIXED다. Transport/Weather의 c067 pin과 Transport r2 REQUEST_CHANGES는 이 판정으로 닫지 않는다. 소비자 pin 갱신/정식 재검토·운영 수용은 별도다.

## Manifest·commit·격리

- Base: 33a3382c2f605ca9135da676bed1ff42061d52fb
- Exact head: 522525aed3db934767c1c9e742b3bfc68e91679c
- Manifest: /home/digitie/dev/reverse-address-common-summary-review-manifest-20261018-r1.json
- 관찰 SHA256: bcd2525457f337c86432bcabbc91d8dd249f47a84159b6185a3ad1ddf1b853ff
- 전체6파일/74+/2-를 immutable Git diff로 읽고 _joined/summary/sample/save와 패키지 설정·관련 문서를 연결했다.
- 변경 경로 순서대로 path+NUL+SHA256+LF를 연결한 목록 SHA256: e20f832f88aba22c973354e297b6dc92083c6eeb34a8b6b7bf6c52a15a701425.
- AGENTS/SKILL 라우터·docs README/resume·review template의 독립성/읽기 전용/미실행 분리 기준을 적용했다.
- 소유 TemporaryDirectory에 정확 Git source를 추출하고 sterile env, -I/-B, --noconftest/no cacheprovider로 실행했다. 읽기 전용 Weather dependency interpreter의 SQLAlchemy/pytest를 사용했다. SDK/Dagster를 import하거나 실행하지 않았다.
- 실제 env/비밀/provider/운영/SSH/Docker/Daemon 접근·조작, 소스/index/branch/WIP 변경·되돌림0. 새 상대 Common40 결과를 보거나 요청하지 않았다. 임시 fixture는 종료 때 삭제했다.
- 시작 UTC는 수집하지 않았다. manifest 생성 시각을 내 시작으로 사용하지 않는다. 종료 UTC는 아래에 기록한다.

## P2 disposition

원문: /home/digitie/dev/reverse-address-transport-review-popper-r2.md
SHA256: e3b770f16b506db16483c1c5f2be4098ccf6ad3eaae2ba213f0d7af6ada7e391.
원본 REQUEST_CHANGES 및 T86-B-P2-02 OPEN 기록은 수정하지 않았다.

**원인 위치:** packages/py/kor-travel-common/src/kortravelcommon/reverse_address.py:551–556.
**연결 provider/key 경계:** 같은 파일 :439–447.

기존 MAX는 provider 전체 entries에서 날짜를 읽어 source에서 제외된 legacy/삭제/이동 전 결과까지 최근 정상 확인으로 노출했다. 새 MAX는 기존 _joined()를 사용한다. 이 JOIN에는 provider_id와 target_key의 일치가 이미 있고, 새 WHERE에 경도/위도 일치가 추가됐다.

따라서 현재 source SELECT에 없는 row, 다른 provider, 현재 좌표와 다른 과거 결과는 MAX에 들어가지 않는다. LEFT JOIN의 결측 entries 또는 NULL 좌표는 동등 비교가 UNKNOWN이 되어 통과하지 않는다. 집계 대상이 없어도 MAX가 한 행의 NULL을 반환하므로 scalar_one이 빈 결과 예외를 만들지 않는다.

status=ok 필터를 추가하지 않은 점도 적절하다. 같은 좌표에서 재실패해 status=error가 되어도 save가 보존한 마지막 정상 resolved_at은 현재 위치의 과거 정상일이다. 그 값까지 제거하면 이번 수용 계약의 last-good 보존을 깨뜨린다.

**수정 상태:** Common source candidate5225에서 FIXED / 새 source OPEN0.
**소비자 상태:** Transport/Weather는 아직c067이므로 consumer T86-B-P2-02 OPEN을 자동 CLOSED로 전환하지 않는다. 실제 배포·운영 검증도 하지 않았다.

## 독립 실행

정확 base/new module을 각각 분리하여 소유 SQLite에서 비교했다. 작성자5개 테스트를 단순 재인용하지 않고 새 fixture를 만들었다.

### 본인12개 검사

1. 삭제된 현재 source
2. enabled=False로 제외한 source
3. enabled=NULL로 제외한 source
4. 경도만 이동
5. 위도만 이동
6. 경도=NULL
7. 위도=NULL
8. 경도·위도 둘 다 이동

위8종에서 base는 옛 START 날짜가 남고 new는 last_resolved_at=None이었다. 양쪽 items=[]도 확인했다. 읽기 전후 source·entries·control의 전체 row snapshot이 동일했다.

9. 현재 a의 정상 START 결과 뒤 동일좌표 실패를 만들고, 같은 provider의 newer orphan과 다른 provider의 동일 key/더 최신 결과를 추가했다. base MAX는 orphan 날짜, new MAX는 현재 a의 START였다. items.status=error와 resolved_at=START가 유지됐다. provider/key 충돌도 결과를 바꾸지 못했다.
10. source SELECT를 UNION ALL로 두 번 포함시켜 MAX가 START로 안정적인지 확인했다. 이 공격은 MAX의 중복 내성을 확인하며, 중복 source의 COUNT 계약을 새로 올바르다고 판정하는 검사는 아니다. 소비자 source 키 유일성은 계속 전제한다. 정확 summary 실행 중 cursor SQL을 수집해 SELECT만 발생함을 확인했고 source/entries/control은 불변이었다.
11. 현재 row는 있지만 다른 provider의 결과만 있거나, 현재 provider에 최초 오류만 있어 resolved_at=NULL이면 last=None이다. source를 비워도 None/total0을 반환했다.
12. orphan 없이 같은 좌표의 정상→200일 뒤 실패에서도 last-good START가 유지됐다.

또한 고정 head의 test_reverse_address.py 전체28개를 소유 src/동일 환경에서 실행했다.
**결과: own12 + pinned28 = 40 passed / 1.35초 / exit0.**
이 묶음의 실행 실패/skip은 없었다. “old 오염→new 정상”을 확인한 실제9상태는 위8종+orphan 경우이며, 전체 suite의 514나 작성자 wheel28을 내가 수행한 숫자에 합산하지 않는다.

## 전체 delta·회귀·packaging/ops 검토

- AST 비교에서 실제 변경된 클래스 메서드는 DatabaseAddressSource.summary 하나다. 외부 함수/API signature·DTO 키·테이블/컬럼·provider·scheduler·lease·cursor·retry·cache·engine 생성/dispose 로직은 바뀌지 않았다.
- _joined가 동일 entries Table/provider/key 경계를 유지한다. 불필요한 별도 FROM/cartesian product를 도입하지 않았고 MAX는 SQL aggregate 한 scalar라 Python에 전체 원천 목록을 적재하지 않는다. 샘플 상한50도 그대로다. 쿼리 성능·PG planner/운영 CPU 개선을 실측한 주장은 하지 않는다.
- 여러 source row가 같은 target_key를 가리켜도 MAX 자체는 동일 날짜의 반복에 영향을 받지 않는다. 실제 두 소비자의 kind:id/위치PK 유일성이나 전체 COUNT의 입력 의미를 이번 변경이 확장하지 않는다.
- 새 조건은 현재 좌표와 동일한 과거 정상일을 집계한다. 원천을 삭제하거나 sidecar를 정리·재작성하는 migration/DML을 추가하지 않았다.
- 패키지 pyproject와 uv.lock이 base와 byte 동일하고 hatch wheel의 src/kortravelcommon 포함 경로도 동일하다. 신규 의존성/버전/extra/entrypoint/동적 배포 로직은 없다. 바뀐 .py가 같은 module 경로로 포장되는 계약이다.
- address_providers.py/address_dagster.py도 byte 동일하다. shared callback/빈 페이지·수동 backoff/lease/timeout 정책을 우회하거나 provider/daemon을 시작하는 코드가 없다.
- CHANGELOG와 guide는 current source·동일좌표/MAX 및 같은좌표 재실패 last-good 보존을 정확히 설명한다. journal/resume는 원래 반례·작성자5FAIL→28PASS와 후속 package/CI/소비자 gate를 구분한다. Track1/2 뒤 수집 CPU/RSS 개선·Daemon OFF를 유지한다.
- git diff --check base..head는 직접 exit0을 확인했다.
- consumer API/표시나 배포를 변경한 파일은 없다. 이후 소비자 pin을 실제 갱신한 immutable head에서 해당 UI/API 날짜 반례를 별도 재검증해야 한다. 이를 신규 사용자 승인 요건으로 요구하는 것은 아니다.

## 증거·CI·미실행 한계

Root의 전체514PASS/117.23초/lockedDagster1.13.25, 새 wheel 설치28PASS/설치 source SHA 일치, Ruff·문서761/2956·plan109·도구334PASS3SKIP·secret0는 manifest로 전달받은 별도 작성자 증거다. 직접 새 wheel을 빌드/설치하거나 전체514·도구·문서 사다리를 재실행하지 않았다. 본인은 허용된 exact Git source 방식으로 SQL regression을 실행했다.

Manifest 작성 당시 Common40 CI pending은 PASS가 아니다. 이후 본인 공개 GH read-only snapshot에서 head5225 PR40 OPEN의 rollup8개(docs/recovery3.11/recovery3.13/tools Ubuntu/tools Windows/secret-scan/check-versions/packages)가 completed/SUCCESS임을 관찰했다. 이는 그 snapshot8개 metadata 확인이며 전체 required/중복 workflow의 최종 merge 게이트를 독자적으로 완결했다는 판정은 아니다. 새 CI는 실행하지 않았다.

실제 PostgreSQL DB/동시 transaction·query plan, native wheel 설치/소비자 runtime, provider/권한/외부 UI·배포/CPU/RSS는 NOT_RUN이다. summary 여러 SELECT를 하나의 serializable snapshot으로 만들었다고 주장하지 않는다. 기존 read-only 관측의 격리 수준 계약을 바꾸는 패치는 아니다.

소비자 현재 pin은c067이다. 이 SOURCE 판정을 실제 consumer P2 closure/운영 수용으로 확대하지 않는다.

## 주요 SHA256

| 파일 | SHA256 |
|---|---|
| reverse_address.py | 3faada7c5099a5a97b0521d5dfa11f86dc817f2846ad3bcc94e37eaefa9fa2d8 |
| test_reverse_address.py | e6bb3f794a0020c83667544d1357cfaa0f4208d894b3aca58046a7cb42130d9f |
| guide | 3db7381764c10e09a4ed8684f2a1aab002970bf6c6d331d61353b9079d13e90a |
| CHANGELOG.md | 0aa6bd7066c966cdc71adca92f4a843a7e452ea52296ac7459a552aac4c0f05f |

## 실제 전달받은 요청 전문

parent NEW_TASK payload를 그대로 보존한다. 메시지 자체의 UTC timestamp는 제공되지 않았다.

```text
새 Common40 최소 수정의 FULL 독립 B Backend/SQL·정합·packaging/ops 렌즈 리뷰를 요청합니다. 기존 Transport r2 REQUEST_CHANGES와 T86-B-P2-02는 그대로 보존. 같은 manifest /home/digitie/dev/reverse-address-common-summary-review-manifest-20261018-r1.json SHA256 bcd2525457f337c86432bcabbc91d8dd249f47a84159b6185a3ad1ddf1b853ff, base33a3382c2f605ca9135da676bed1ff42061d52fb → head522525aed3db934767c1c9e742b3bfc68e91679c, WT /home/digitie/dev/kor-travel-common-codex-address-summary-20261018. 통과보다 결함 찾기가 목적, 모호하면 지적. 6파일 전체 delta(공통 MAX source+좌표 join·5반례·guide/journal/resume/changelog)를 immutable Git object로 검토. 새 P2 수정은 root5 FAIL→engine28PASS, 전체514PASS/117.23초/lockedDagster1.13.25, 새wheel설치28PASS/hash동일, Ruff/docslinks761/2956/0/plan109/0/tools334PASS3SKIP(Windows1/jsonschema미설치2)/secret0. CI pending은 PASS 아님. 자신의 P2를 current source/coords 범위, SQL NULL/empty/source filters/provider collision/동일좌표 실패lastgood보존/소스sidecar불변에서 실제 재검증하고 join cardinality/MAX 의미·consumer함께영향·추가회귀를 공격. reviewer read-only, source/index/branch 편집·실제provider/env/secret/production/SSH/Docker/daemon 금지, 자기 소유 temp fixture/installed new wheel 또는 exact Git source만 검증. 다른작업자있으니 변경/되돌림 금지. 새 상대 Common40 결과는 둘 다 확정 전 보거나 요청하지 마세요. 실제 이 요청 전문·manifesthash/commit·격리·시각·실패/미실행 한계·file:line/재현/심각도·P2 disposition·PASS/CONDITIONAL/BLOCK와 OPEN P0/P1/P2를 /home/digitie/dev/reverse-address-common-summary-review-popper-r1.md 원문으로 저장하고 hash와 verdict 보고. 아직 Transport/Weather는c067pin이므로 Common SOURCE closure와 소비자P2 closure/운영수용은 구분하세요.
```

보고서 종료 UTC: 2026-10-18T03:42:22.946987+00:00
