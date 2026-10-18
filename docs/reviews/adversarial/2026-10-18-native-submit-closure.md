# 영속 Dagster 제출과 연결 장애 보호 최종 리뷰

상태: COMPLETE. **두 독립 SOURCE PASS, 열린 P0/P1/P2/P3=0.**
기준27cd146ed9e83d3ef481757d2b48e16f232dc88c →
제품89291f36d731ab906161b96757522e1cd833b4ef /
문서7d46df6341b9bc6d5a2bfa69f80e162bebd71422를 검토했다.
[불변 파일 manifest](evidence/2026-10-18-native-submit-manifest.json)를 함께 보존한다.

작성자 A와 별개인 B(/root/review_finish_b, PG·패키징·장애)와
C(/root/geo_timeout_analysis, native 계약·경합·소비자)가 불변 Git 기준으로
독립 검증했다. 각 원문 확정 전 상대 원문은 공유하지 않았다.
최초 BLOCK 및 중간 HOLD는 아래 원문 그대로 유지한다.

| 원 지적 | 최종 처리 | 근거 |
| --- | --- | --- |
| C41-B-P1-01 / C41-C-P1-01: 오래된 NOT_STARTED 제출의 상태 역행 | FIXED | run별 직렬화와 fresh 상태 확인; 동일 요청 replay가 STARTED를 보존 |
| C41-B-P1-02: advisory 연결 소실 뒤 stale enqueue | FIXED | 잠금과 native run 저장을 같은 물리 연결에 결합; 끊긴 연결의 재생성 거절 |
| C41-B-P2-01 / C41-C-P2-02: native statement_timeout 소실 | FIXED | 공식 Pool.recreate로 creator·연결 정책 계승; 실제 SQL 취소 및 원 pool 전량 대여 중 독립성 확인 |

작성자는 양 SDK 집중51개·소유 PG58개씩, 잠긴 전체565개를 통과했다.
C는 SDK1.13.24/SQLAlchemy2.0.54와 1.13.25/2.1.5 각각66개를 직접 통과했다.
B는 정식 1.13.24/2.0.54 및 1.13.25/2.1.3에서 실제 PG timeout·pool·연결 소실을
검증하고 새 policy3개·본인8개씩을 별도 통과했다. B의 전체59개 묶음은 시간 예산
종료로 NOT_COMPLETED다. 정체 지점 단독1개 통과를 전체 통과로 바꾸지 않는다.
서로 다른 실행과 부분 결과를 합산해 하나의 전체 suite PASS로 표시하지 않는다.

정식 wheel은 58,563B, SHA256
14dd0d99c97ad561c529722c9a64a8bf076920e25fc4d722226202980297dfc9다.
B의 독립 빌드와 작성자 산출물이 byte 동일하며 Python14개와 RECORD를 검사했다.
문서7d46 기준 [CI14개 모두 SUCCESS](evidence/2026-10-18-native-submit-source-ci.json)를
merge 담당이 새로 확인했다. 이 후속은 원문·disposition·index만 보존하는 closure이며
사용자의 문서 CI 생략 지시에 따라 별도 CI를 실행하지 않는다.

소비자 최종 pin에서 root의 Weather 집중12·Transport23, 각 앱의 실제 loopback
API/native Dagster 연동 Chromium UI17개 및 12초 지연 재시도1개가 통과했다.
원천 provider는 실행하지 않았으며 이 결과는 운영 UI/배포 수용을 대신하지 않는다.
Transport Docker의 같은 pin 집중23개도 통과했다.
Common38의 daemon-pool은 이 main 기반 wheel에 아직 없으므로 통합 wheel을
검증한 뒤 공용 호스트에 채택한다. daemon OFF 방침을 유지한다.

지원 범위·롤백은 [구현 가이드](../../runbooks/dagster-idempotent-launch.md)가 정본이다.
native eventlog에는 실패한 제출 시도가 먼저 남을 수 있으며 authoritative run 상태와
원자적이지 않다. 임의 custom Engine 이벤트·provider 작업의 exactly-once를 보장하지 않는다.
운영 배포·실제 job/provider·수집 CPU/RSS 개선은 NOT_RUN이며 소비자 후속 범위다.

## 원문 무결성

| 원문 | SHA256 |
| --- | --- |
| [2026-10-18-native-submit-r1-reviewer-b.md](evidence/2026-10-18-native-submit-r1-reviewer-b.md) | 20d729af3e7aeee8b22e2bc0bb1c31ff085f2ee261da46439a14533827d758dc |
| [2026-10-18-native-submit-r2-reviewer-b.md](evidence/2026-10-18-native-submit-r2-reviewer-b.md) | 80821f1e6ca0840ec509456fea0bb86f59e676e2730915b4299e23bd082c4d3d |
| [2026-10-18-native-submit-r3-reviewer-b.md](evidence/2026-10-18-native-submit-r3-reviewer-b.md) | 6328cbc39d0c8e3e9860e4594e4df9028f8a51d72d7b5ed8cb99c46f3e4b8737 |
| [2026-10-18-native-submit-r1-reviewer-c.md](evidence/2026-10-18-native-submit-r1-reviewer-c.md) | 07b3b213cf37470d9185caf3905e045c5f6ad45008fb05c62b74188e7c9d27ae |
| [2026-10-18-native-submit-r2-reviewer-c.md](evidence/2026-10-18-native-submit-r2-reviewer-c.md) | 8f34c78463ca74bb9f39974d9db4857ab2b416e64d5483c301fb675cec157bb9 |
| [2026-10-18-native-submit-r3-reviewer-c.md](evidence/2026-10-18-native-submit-r3-reviewer-c.md) | b91ef738a4b420824e9e7068ec535cd749d6786903a39216b48ad9e830be2df4 |
| [2026-10-18-native-submit-r4-reviewer-c.md](evidence/2026-10-18-native-submit-r4-reviewer-c.md) | 31490bacc198511cd971d80c15488dc515cc167448742bf15848de49b208355f |
| [2026-10-18-native-submit-final-reviewer-c.md](evidence/2026-10-18-native-submit-final-reviewer-c.md) | c6823e58bd8194807d4a815bc383a43b5aa721edd4a143dd46811152cf57748f |
| [2026-10-18-native-submit-r4-reviewer-b.md](evidence/2026-10-18-native-submit-r4-reviewer-b.md) | a5a00903ea0154e9f1d746579a90b6d83cb867666c84f6f2d1ebb98189a9e151 |
