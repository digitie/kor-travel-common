# 경량 HTTP 생존 점검

`kortravelcommon.http_health`는 Web API의 반복 생존 조회에서 큰 HTTP client·TLS·
프레임워크 import를 피하는 core-only 후보다. Weather API와 Transport backend에서
같은 urllib 점검이 반복되는 것이 추출 근거다. provider 수집·DB·Dagster run 상태는
소비자가 따로 확인하며 이 프로브 성공만으로 작업 성공을 선언하지 않는다.

## 호출과 판정

```bash
python -m kortravelcommon.http_health --port 8000 --path /health --timeout-seconds 4
```

함수는 `check_http_health(*, port, path="/health", timeout_seconds=4.0)`다.
port는1~65535 정수, path는2048자 이하 공백 없는 ASCII 절대 경로,
timeout은0초 초과60초 이하의 유한한 수다. 잘못된 함수 인자는 ValueError다.
CLI 종료 코드는 성공0/연결·프로토콜·시간 제한 실패1/잘못된 인자2이며,
응답·오류·경로를 로그로 출력하지 않는다. `--help`는 사용법만 출력한다.

IPv4 loopback에 GET 한 번만 보낸다. DNS·TLS·redirect·재시도는 없고 본문 완료를 기다리지 않는다.
헤더를 받는 마지막 recv에 본문 일부가 포함될 수 있으며 한 번의 수신은최대1KiB다.
연결·전송·헤더 수신이 하나의 monotonic 예산을 공유하며 헤더는최대16KiB다.
HTTP/1.0·1.1의 완전한 헤더와2xx 상태만 성공이다. 헤더 줄 형식과 제어 문자,
중복·모순·잘못된 Content-Length/Transfer-Encoding을 거절한다.
응답 본문이나 앱별 health JSON 의미는 검증하지 않는다.

3xx는 Location 유무와 관계없이 실패다. 기존 redirect 허용 client와 다른
fail-closed 계약이므로 소비자는 같은 컨테이너의 직접 생존 경로를 지정해야 한다.
GET만 허용하는 loopback 경로에 쓰며 인증·provider·DB 호출이 있는 무거운 경로를
새로 연결하지 않는다.

## 소비자 채택

Common pin은 정확한 commit으로 고정하고 lock·이미지에 실제 설치된 코드를 확인한다.
컨테이너의 기존 경로·주기·timeout·재시작 정책은 소비자 PR에서 명시적으로 유지하거나
실측으로 조정한다. 전체 예산은 함수 호출부터 측정하므로 Python 시작·모듈 import와
스케줄 지연은 Docker health timeout에 추가된다. 함수4초가 Docker5초 내 종료를 보장하지 않는다.
점검 실패만으로 실행 중인 Dagster worker를 종료하거나 run을 재시도하지 않는다.

실제 적용 전 exact 이미지의200/non2xx·느린 헤더·연결 종료·과대 헤더·전체 예산·
CLI 종료와 기존 판정을 확인한다. 실제 healthy·CPU·메모리·UI 검증은 해당 소비자 소유다.
이번 Common 소스만으로 운영 지연 해소·절감률·재구축 완료를 선언하지 않는다.

## 실측의 범위

기존 실제 호스트의 urllib 계측 표본은 self CPU 약3초였고,
`-S` 추가만으로 뚜렷한 개선이 없었다. 순수 소켓 상태 줄 prototype의
자식 CPU 단일 표본은2.838705초에서0.996753초였다.
prototype은 이 모듈의 완전한 헤더 검증·CLI와 다른 코드이며 이 모듈의 운영 벤치마크가 아니다.
비통제 작업 부하·단일 표본이므로 평균 절감률·Docker timeout 개선을 보장하지 않는다.
최종 코드의 반복 실측과 소비자 설치·live 수용은 별도로 기록한다.
