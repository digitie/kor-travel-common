# Common47 병합과 Transport 후보 UI 수용 정산

이 문서는 [T-217](../tasks/T-217-login-hydration-readiness.md)의 구현·CI·소비자 후보 검증 범위를 정산한다. 공개 TLS와 운영 배포의 완료 기록은 아니다.

## Common 제품과 병합

- [PR47](https://github.com/digitie/kor-travel-common/pull/47)의 최종 후보는 `44d7a240ebe82b11389824fd503e33ca4000ddd7`, 병합 main은 `aa232ad5f255233184de80eceaab2e9b6ccb00c9`다. 두 전체 Git tree는 `bb5efc81d04b7e941670ac6a07e9c987abfbd14a`로 동일하다.
- 최종 후보 CI 8개가 모두 SUCCESS다: docs, tools 양 OS, secret-scan, check-versions, packages, recovery Python 3.11/3.13. [문서·패키지 lane](https://github.com/digitie/kor-travel-common/actions/runs/40276870481), [Python lane](https://github.com/digitie/kor-travel-common/actions/runs/40276870435).
- J/W가 제품 전체와 최종 CI 정렬 delta를 각각 독립 검토해 PASS했다. J 원장 SHA256은 `d47cdbf7dea33cdd7661f313dc0f7d5bbd32c6702ff787eddd1e2ee96e37a90a`/`45111a249c0230672083ee1269f6cacf3f331949474503f494519e8ee8be4847`, W는 `6a4de6cf5f2509845915bb00ae7cf3fc91b64b63f1476d5ec414672a86efaa01`/`cf465299a283c6f94ff873aaea2d9f8571173c94d48b60566a34eeeef1566c86`이다.
- 정규 UI `0.1.0-dev.9` tarball은 기존 27파일/SHA256 `b738d8824e36eb6e58d8cc6b78af7dc31233b6763248d634286044def795b403` 그대로다. 이 문서 작업은 제품·tgz·package·lock을 바꾸거나 새 패키지를 만들지 않는다.

## 실제 소비자 후보 검증

Transport 소스는 `6913fc94bb0051a75c7004f4647b7d6e38b7dd04`다. 실제 Next 빌드 성공의 원 UUID는 `6e98370ea8034a02a8444ed9c85a6257`이다. 최종 r12 runtime `45d74c1e09564b41a1a6c7b914eb7fb2`는 그 빌드 산출물과 소스를 새 격리 디렉터리에 복제하고 원 두 build receipt SHA·소스 779개 mode/blob·manifest 4개·static 59개를 전수 재검산한 재실행이다. **새 빌드 성공으로 집계하지 않는다.**

- 실제 Next 후보의 32개 판정이 26.014초에 PASS했다. 새 인증 context의 후보 HTTP 범위이며 API/Dagster는 기존 읽기 경로를 사용했다.
- 초기 script GET 8개를 보류한 상태에서 SSR 입력 두 개·제출 버튼 비활성화를 확인하고, script 해제 후 client handler 준비·실제 로그인 HTTP200을 확인했다.
- 정확 이름·domain·path로 찾은 session cookie의 값 존재·Secure·HttpOnly를 확인했다. 인증 reload 뒤 세션 유지, logout과 쿠키 제거, 보호 화면의 로그인 요구를 확인했다.
- 교통·유가 지도 두 화면에서 실제 tile 응답 합계40·읽기 API 성공10을 확인했다. 도메인 쓰기 요청0, 허용 쓰기는 login/logout뿐이다. 읽기 전용 GraphQL POST 2개는 도메인 쓰기와 구분한다.
- page/console/resource/document/API/tile 오류와 request failure는0이다. 별도 navigation abort15를 이 오류 집계와 합치거나 없었다고 주장하지 않는다.
- 소스·산출물 사후 동일, 자체 browser/container·tunnel/control socket 정리, Next runtime unit inactive·cgroup empty/absent를 확인했다.

수용 원장은 감사 디렉터리의 `transport141-6913-r12-next-live-ui32-root-acceptance-r1.json`, SHA256 `6c3ddf244c33486115808e689d7806db6197687e7ca3e9f7b66531d8e585da35`다. 복제 검산 원장은 `transport141-r12-runtime-artifact-copy-45d74c1e09564b41a1a6c7b914eb7fb2-root-r1.json`, SHA256 `2623fa556b8a140fc7d2c1b886d727a914c1be16c541f6a2449a2e19c1fc5e3a`다.

## 보존한 실패와 남은 범위

원 Common SSR 반례2FAIL과 f0b CI4실패는 보존한다. 최종 CI 성공으로 과거 실패 로그를 바꾸지 않는다. 소비자 원8c82 후보의 cookie 조회 FAIL은 상세 원인 미확정이며, 이후 전체 cookie jar에서 정확 항목을 고르는 관측 수정은 Secure/HttpOnly 요구를 완화하지 않았다. 6913의 stale wrapper pin에 의한 argparse 거부·브라우저 전 FAIL도 별도 보존한다.

공개 HTTPS/TLS, Transport 운영 배포, 운영 CPU/RSS 효과는 NOT_RUN 또는 미수용이다. 다른 소비자 채택과 광역 UI task 완료로 확대하지 않는다. T-217은 이 외부 선행이 남아 IN_PROGRESS이며, 다음 작업은 소비자 소유 공개 TLS·배포 gate 정산이다.
