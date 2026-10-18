# Common #39 독립 적대적 리뷰 — James r1

- Review ID: COMMON39-JAMES-R1 / 실행 주체 /root/review_finish_a.
- 종류: FULL, 관리자 실행·API/UI 신뢰 경계 및 공개 Python 계약 관점.
- 판정: **BLOCK**. OPEN P0=0 / P1=1 / P2=1 / P3=0.
- 정식 판정 대상: Common base c48595880aaad4367802ad71af2525a8a5e17c6a → head 812b291659e40564595c3c28b7e8d51cbcc46df9.
- Manifest: /home/digitie/dev/reverse-address-review-manifest-20261018-r1.json.
- Manifest SHA256: 92f7e3b810c510e5ad26d109e294414ffa44db81ebd2edbe907af0fbf544a486.
- Weather 3516a89c7d97d2dba008a1d07631b5ccbed6911a / Transport e1e6035468e6e00dfcf7d107a0dce77967dc3703은 통합 맥락만 읽었다. 소비자 CI·배포·브라우저 정식 게이트 판정을 하지 않았다.
- 시작: 2026-10-18 UTC 본 세션(분·초 사전 기록 없음). 종료 시각은 문서 끝에 기록한다.
- 다른 리뷰어 결과·검증 로그는 열람하지 않았다. 작성자 495 PASS/CI green은 의뢰 정보이며, 본인의 새 실행 결과와 합산하지 않는다.

## 격리·검사 범위

AGENTS.md, docs/README.md, docs/resume.md, agent-workflow §5, reviews/README의 기록 규칙을 읽었다. Git commit object의 diff와 git show를 기준으로 Common 변경 11파일 전체를 검토했다. 신규 제품 3모듈(82/211/644줄), 테스트 3개, 가이드, optional extra/lock, CI 연결을 읽었다. CodeGraph 대신 Git/수동 호출 추적/fixture를 사용했다.

처음 Common worktree에는 미추적 .verify-address-common.log가 있었다. 검토 도중 reverse_address.py와 해당 테스트의 다른 작업자 변경이 추가되었다. 모두 보존했으며 최종 대상은 이동 가능한 worktree 내용이 아닌 위 head의 Git object다. 실행 fixture도 git show로 해당 모듈을 메모리 compile하거나 소유 임시 디렉터리에 복사했다. Weather/Transport의 후속 WIP·테스트 결과 파일 역시 읽지 않았다.

운영/SSH/Docker/실제 DB/실제 provider/브라우저/인증정보 접근 또는 Git 변경은 없다. SQLite는 새 in-memory fixture만 사용했다. VWorld SDK 연결 시험은 공개 설치본의 순수 처리 + httpx.MockTransport로 수행했고 socket.connect를 거절했다. Dagster 실제 실행/인스턴스는 만들지 않았다. 임시 fixture는 종료 시 정리했고, 영구 신규 산출물은 이 보고서 하나다.

## A-P1-01 — 정상 VWorld 요청의 HTTPX INFO 로그에 API 키가 노출된다

상태: **OPEN**.

위치:
- packages/py/kor-travel-common/src/kortravelcommon/address_providers.py:73–82, 193–200.
- 명시 계약: docs/reverse-address-refresh.md:34–37.
- 호출되는 고정 의존성: python-vworld-api 3b174abea1a1e734c60a9c2522b2844474a1ec71. 공개 설치본 vworld/_http.py:135,145–148,174–183에서 key를 query에 넣어 HTTPX로 전송한다.

실패 조건은 소비자가 HTTPX INFO 로그를 수집하는 일반적인 로깅 설정이다. reverse()가 정상 결과를 반환해도 HTTPX는 요청 URL 전체를 INFO로 기록한다. URL query에 있는 VWorld key도 그대로 포함된다. Common이 예외를 vworld_failed로 바꾸는 처리는 이미 출력된 정상 요청 로그를 보호하지 못한다. Kakao가 보조인지 여부와도 무관하다.

본인 재현:
1. 위 head의 address_providers/reverse_address를 Git object에서 로드.
2. 공개 VworldClient에 httpx.AsyncClient(MockTransport)를 주입하는 vworld_factory 사용.
3. httpx logger만 INFO + 메모리 StringIO handler로 설정.
4. 가짜 키 OWNED-CANARY-KEY-NEVER-A-REAL-KEY, 고정 좌표, 정상 주소 fixture로 reverse() 실행.
5. socket.connect는 AssertionError로 차단.

관측:
    {"result_provider":"vworld","request_url_logged":true,
     "key_canary_logged":true,"socket_connects_allowed":false}

핵심 재현 형태(키는 실재 자격이 아닌 canary):
    class Factory:
        def __init__(self, **kwargs):
            self.session = httpx.AsyncClient(
                transport=httpx.MockTransport(handler), trust_env=False)
            self.real = VworldClient(**kwargs, session=self.session)
        async def __aenter__(self):
            return self.real
        async def __aexit__(self, *args):
            await self.session.aclose()

    # handler는 {"response":{"status":"OK","result":[
    #   {"type":"road","text":"fixture road"}]}}를 반환한다.
    logger = logging.getLogger("httpx")
    logger.setLevel(logging.INFO)
    logger.handlers = [logging.StreamHandler(sink)]
    logger.propagate = False
    resolver = VworldKakaoAddressResolver(
        vworld_key=CANARY, kakao_key=None, vworld_factory=Factory)
    assert resolver.reverse(AddressTarget("fixture",127,37))["provider"] == "vworld"
    assert CANARY in sink.getvalue()

영향: 별도 SDK 내부 재시도나 provider 오류 없이도 서버 자격 및 요청 좌표/URL이 서비스 로그 수집 경계를 넘어간다. 실제 운영 로깅 설정이나 실제 키 노출을 확인했다는 뜻은 아니다. 그러나 “키·요청 URL을 로그에 남기지 않는다”는 Common 공개 계약은 지원 가능한 정상 로깅 설정에서 깨진다.

권고: 기존 public SDK 사용을 유지하면서 해당 요청의 URL/key가 로그에 들어가지 않도록 호출 경계 또는 SDK의 지원 가능한 로깅 경로를 보호하고, 정상 응답과 오류/보조 fallback 모두에 canary 로그 비노출 회귀를 추가한다. 공유 전역 logger를 잠시 껐다 켜는 방식은 다른 동시 요청의 기록 정책까지 바꾸므로 그 부작용도 검사해야 한다. 가이드 문구만 약화하는 조치는 권고하지 않는다.

## A-P2-02 — 만료된 마지막 owner가 관리자 상태를 무기한 진행/재개 대기로 남긴다

상태: **OPEN**.

위치:
- packages/py/kor-travel-common/src/kortravelcommon/reverse_address.py:484–512, 특히 509–510.
- 관련 완료/해제 경계: :220–242, :637–644.
- 불일치하는 pending 판단: :462–481.
- 통합 맥락: 두 소비자의 components/address-refresh.tsx:57은 in_progress를 “배치 진행 또는 재개 대기”로 표시한다.

실패 조건: 마지막 결과와 complete_cycle() 커밋은 성공했지만 finally의 release() 전에 worker가 죽는 정상적인 crash 경계다. control.cursor는 빈 문자열, force_refresh는 False, 대상은 모두 다음 갱신일 전이다. 90초 lease가 만료되어도 summary는 lease_until을 보지 않고 owner 문자열만으로 in_progress=True를 반환한다. 반면 has_work()는 False이므로 sensor가 이 유령 상태를 해소할 새 run도 만들지 않는다. 다음 실제 갱신/수동 실행까지 수개월간 완료된 배치를 진행/재개 대기로 표시할 수 있다.

본인 실제 함수 재현:
- 새 in-memory SQLite에 Common 선언 테이블과 위치 1개 생성.
- claim → prepare → save(정상 주소) → advance → complete_cycle을 실행.
- release를 생략하여 crash를 모형화하고 lease_until만 현재보다 과거로 설정.
- summary()/has_work()를 실제 함수로 호출.

관측 및 assertion:
    total == 1
    due == 0
    cursor == ""
    force_refresh is False
    lease_until < now
    summary["in_progress"] is True
    source.has_work(now) is False

영향: 원천/파생 데이터 손상은 없지만 Common의 사용자용 상태 projection이 실제 실행도, 재개할 남은 작업도 없는 상태를 실행/재개 대기로 전달한다. 두 소비자가 같은 필드를 그대로 사용한다는 연결만 확인했으며 소비자 제품의 정식 판정을 추가한 것은 아니다.

권고: 살아 있는 lease의 owner와 영속 cursor/manual-cycle 잔여를 구분하여 in_progress를 계산한다. 만료 owner + cursor 없음 + force False + due0은 False, 유효 lease나 실제 잔여 cursor/manual-cycle은 True인 회귀가 필요하다. 단순히 owner를 읽을 때 무조건 삭제하여 다른 worker를 방해하는 조치는 피한다.

## 실행한 검증과 공격한 경계

| 검증 | 결과 | 범위/한계 |
| --- | --- | --- |
| Manifest SHA 및 3개 고정 commit 존재 확인 | 일치 | branch 최신 상태의 승격 판정 아님 |
| Common Git object의 reverse_address/provider 기존 집중 테스트 독립 실행 | 17 PASS, 0.67초 | 소유 임시 복사, --noconftest, -p no:cacheprovider, Python -I -B; 실제 네트워크 차단 |
| 공개 VWorld SDK + HTTPX INFO canary | 비노출 기대에 대한 반례 확정 | 정상 응답 fixture, 실제 키/외부 요청0 |
| 완료 후 release 전 crash/lease expiry | 상태 진실성 반례 확정 | in-memory SQLite, 실제 함수 사용 |
| 정상 무결과 projection 조사 | not_found/stale=True, due0 관측 | 보수적인 “주소 미보장” 표시일 수도 있어 독립 finding으로 중복 계상하지 않음 |
| 주입 resolver의 ReverseAddressError 문자열 조사 | 임의 문자열이 error_code로 전달됨 | 현재 내장 adapter는 유한 코드로 정리하므로 별도 운영 유출 finding으로 계상하지 않음 |

17개 기존 테스트는 정상 주소 변경, 달력/KST 월말, 수동 cycle 재개, 좌표 동일 재사용일 보존, 실패 후 마지막 주소 보존, 만료 owner의 늦은 쓰기/다른 owner 해제 방지, 이동 좌표의 이전 주소 비노출, provider 변경만으로 변경 집계 안 함, Kakao 보조/응답 크기·slow-drip deadline 등을 포함한다. 이는 작성자 전체 495 PASS의 대체가 아니다.

관리자 실행 맥락에서는 고정 자기 location/job의 수동 force config, session+same-origin BFF, requestId 재조회/기존 활성 run 차단, queued 성공과 완료 구분 문구를 읽었다. Common 자체가 Daemon을 start하는 경로는 없다. RUNNING 기본 sensor 등록은 Daemon OFF를 실제로 켜는 동작이 아니다. 이 결과로 소비자 인증/실제 예약/브라우저가 통과했다고 주장하지 않는다.

주소 원천 경계는 Common이 별도 entries/control만 쓰고 DatabaseAddressSource는 읽기 SELECT를 소유한다. 두 소비자는 원천 좌표 SELECT를 연결한다. 현재 좌표 key가 바뀌면 예전 좌표 projection을 제외하며, 실패 시 동일 좌표의 마지막 정상 payload/확인일은 유지한다. VWorld 우선, 실패·정상 무결과 시 Kakao 보조, 위치별 달력 6개월, 관리자 수동 예약이라는 요청의 구조는 존재한다. 위 두 결함은 그 구조의 로그 비밀 경계와 사용자 상태 진실성에 대한 반례다.

## 미검증·판정 한계

- 실제 provider 요청/이용조건/키 권한/쿼터, 운영 migration/DB dialect·동시성, 운영 로깅 sink는 NOT_RUN.
- 실제 Dagster job/sensor/Daemon, 소비자 CI 최종 결과, 실제 Admin 예약·브라우저·배포는 NOT_RUN.
- 소비자 Weather/Transport의 새 WIP는 범위 밖이며 고정 manifest consumer head만 연결 참고했다.
- Common 전체 495 테스트를 다시 실행한 것이 아니다. address_dagster의 테스트는 정적 검토만 했다.
- 코드·Git·운영 수정 및 Daemon 시작은 하지 않았다. 해결 여부는 새 고정 commit에서 독립 재검토해야 한다.

종료 UTC: 2026-10-18T01:31:30.903777+00:00
