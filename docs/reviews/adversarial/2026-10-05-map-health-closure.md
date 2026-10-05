# Map child health 공용 경량 점검 최종 source 리뷰

<!-- latest-runtime-status -->
## 2026-10-06 — 최종 tick·C7 후보 검증 상태

최종 제품 소스는 Common `a960bdb114d99a2ac1b9608a77b240635806e551`, Map `1a3c4673790f51daa1a2f5ccf803d4e31673bad6`, PinVi `0058369c778f8c3357ee393e12e3447d7975cc1f`이다. 전체113파일 [고정 manifest](evidence/map-health-2026-10-05/reviewed-ticks-c7-manifest.json)를 두 독립 리뷰어가 검토했으며 [복구·DB·메모리 FULL PASS](evidence/map-health-2026-10-05/review-ticks-c7-full-recovery.md)와 [UI·인증·빌드 FULL PASS](evidence/map-health-2026-10-05/review-ticks-c7-full-ui.md)를 받았다. 원래 C7 vendor 누락 BLOCK과 후속 수정 판정을 각각 보존한다.

이전 `1ba6/0058` 보호된 재구축은 실제 [성공 receipt](evidence/map-health-2026-10-05/rebuild-builtin-retry1-success.json)와 [설치 코드·여섯 서비스 attestation](evidence/map-health-2026-10-05/operating-runtime-attestation.json)를 확보했다. 같은 실제 Map Dagster 이미지의 격리된 native 실행에서 실패·worker crash·장기 정체의 종료, 동시 정상 job, 수동 재시도 성공과 자동 run monitoring을 [확인](evidence/map-health-2026-10-05/native-operating-evidence.json)했다. 공유 운영 DB/worker 강제 종료 시험은 아니다. 이 native 이미지의 Common/Dagster Python bytes는 최종 후보와 같으며 API tick query와 C7 Dockerfile의 새 bytes를 검증한 증거로 확대하지 않는다.

최종 C7 exact Git archive 빌드와 여섯 서비스 pair 재구축은 실제 완료했다. 새 [재구축 receipt](evidence/map-health-2026-10-05/rebuild-ticks-success.json)와 [설치 코드·서비스 attestation](evidence/map-health-2026-10-05/operating-runtime-ticks-attestation.json)을 독립 리뷰어가 직접 확인했다. native fault 시험은 이전 이미지에서 실행했으며, 새 Map Dagster 이미지의 버전과 관련 코드 bytes가 같다는 별도 [상속 증거](evidence/map-health-2026-10-05/native-final-byte-inheritance.json)를 확보했다. 새 이미지에 fault 시험을 다시 실행했다는 뜻은 아니다.

후속 UI 첫 시도는 PinVi 테스트 target404로 중단됐다. 운영 설정의 canonical 주소로 private 입력을 바로잡은 새 [실제 UI 실행](evidence/map-health-2026-10-05/ui-operating-ticks-retry1-evidence.json)에서 Chromium/Firefox×Map/PinVi 네 사례가 통과했다. 실제 로그인·Secure HttpOnly 세션·실행 상세 identity·조회 실패 뒤 마지막 정상 화면 유지/복구·390px 모바일 문서 폭/키보드 내부 스크롤을 확인했다. Map은 실제 UI 로그아웃200, PinVi는 기존 버튼이 없어 실제 API 테스트 세션 정리204를 확인했다. 브라우저 summary 요청만 중단했으며 공유 서비스/worker를 종료한 시험은 아니다. [독립 영수증·8개 화면 검토](evidence/map-health-2026-10-05/ui-ticks-retry1-actual-visual-review-ui.md)와 [8개 캡처](evidence/map-health-2026-10-05/ui-ticks-retry1-screenshots/capture-manifest.json)를 보존했다.

ACL40건과 [새 D1/D2 실제 수용](evidence/map-health-2026-10-05/chain16-ticks-retry3-operating-evidence.json)이 통과했다. D1 11건 PASS, D2의 새 실행 영수증·실제 API/C7 image identity·정상 mode/attempt0 validator를 확인했다. 소유 fixture만 feature1·field override7 삭제했고 잔존0, ACTIVE/BLOCKED 없음이다. [테스트 ESM 이미지의 실제 추가 layer](evidence/map-health-2026-10-05/c7-esm-ticks-retry3-proof.json)는 frontend package.json의 type=module 한 키만 포함하며 제품 코드113과 운영 이미지6개는 바뀌지 않았다. 두 [실행 하니스 리뷰 A](evidence/map-health-2026-10-05/chain-ticks-retry3-overlay-review-recovery.md)·[B](evidence/map-health-2026-10-05/c7-esm-retry3-final-review-ui.md)가 동일 기준을 확인했다. 최초 후속 영수증 수집기는 canonical validator가 생성한 validation.json을 복사본에서 제외하지 못해 [재검증에 실패](evidence/map-health-2026-10-05/chain-ticks-retry3-collector-negative.json)했다. 두 [수집 절차 보강 리뷰 A](evidence/map-health-2026-10-05/chain-ticks-retry3-validation-closure-review-recovery.md)·[B](evidence/map-health-2026-10-05/chain-ticks-retry3-validation-closure-review-ui.md) 후 실제 재검증은 원본 metadata/전체 bytes를 유지하며 새 validation 출력이 원본과 byte-identical임을 확인했다. D1/D2 실행 실패와 구분한다.

앞선 D1 두 번은 host dependency 누락과 Common의 import 전용 ESM export를 CommonJS로 읽는 수집 실패였다. 로그인·브라우저 전의 실패와 D2 미실행은 [첫 기록](evidence/map-health-2026-10-05/chain-ticks-operating-negative.json)·[다음 기록](evidence/map-health-2026-10-05/chain-ticks-retry1-operating-negative.json)에 그대로 보존했다. 별도 테스트 이미지 검사도 Docker Id를 config SHA로 가정해 한 번 중단됐고 [그 실패](evidence/map-health-2026-10-05/chain-ticks-retry2-operating-negative.json)를 보존한다. Docker29의 OCI index/manifest/config/layer digest chain을 검증하도록 수정했다. 실제 제품 재구축·UI4건·D1/D2를 완료했으며 최종 문서 포함 CI와 PR merge가 다음 gate다. 아래 문단은 이전 시점의 이력이며 현재 판정은 이 절을 따른다.
<!-- /latest-runtime-status -->

## 2026-10-06 — 현재 소비자 운영 재시도

[네 번째 실제 실패](evidence/map-health-2026-10-05/rebuild-builtin-fourth-negative.json)와 [실패 독립 확인](evidence/map-health-2026-10-05/review-builtin-operating-build.md)을 보존한다. PinVi ETL의 고정 uv 이미지 metadata 조회가 실패했으나 [이후 같은 digest의 실제 builder registry 조회](evidence/map-health-2026-10-05/builtin-uv-registry-read.json)는 정상이다. 같은 원장·제품 pair의 [표준 재시도 계약](evidence/map-health-2026-10-05/review-retry-admission-recovery.md)을 확인하고 다섯 번째 실행을 시작했다. 현재 RUNNING이며 native/UI/D1/D2/merge는 미완료다. 아래 NOT_RUN은 각 source archive 시점의 기록이다.

제품 source FULL PASS와 별도로, 수집 하니스의 [초기 BLOCK](evidence/map-health-2026-10-05/review-two-collectors-block.md)·[후속 정적 PASS](evidence/map-health-2026-10-05/review-collectors-postfix-ui.md)를 원문 보존했다. 정적 PASS는 실제 운영 테스트 PASS가 아니다.


고정 Common `a960bdb114d99a2ac1b9608a77b240635806e551`, Map
`1ba6ef4c52f64200e3bc3e9a4fee1dd5f8d4e77e`, PinVi
`2a36e8973bb163c68f1a778a0c1215fa8e9d02d4`의 전체111파일을 두 리뷰어가
별도 archive로 검토했고 모두 FULL 연속 PASS다.
[고정 manifest](evidence/map-health-2026-10-05/manifest-health-markers.json)와
[원문 보존 manifest](evidence/map-health-2026-10-05/preservation-manifest.json)를 연결한다.
이 source 판정은 운영 재구축·live 성공 판정과 구분한다. 이 후보의 paired 재구축은 ETL 외부 frontend 종료로 실패했다.
수정 PinVi `0058369c`의 새 재구축과 runtime/native/browser/D1/D2는 아직 NOT_RUN이다.

| 단계 | 복구·DB·메모리 | UI·인증·소비 계약 |
| --- | --- | --- |
| e0b5/6a54/2a36 | [BLOCK H07](evidence/map-health-2026-10-05/review-recovery-health.json) | [PASS](evidence/map-health-2026-10-05/review-ui-health.json) |
| 99d8/b972/2a36 | [BLOCK H08](evidence/map-health-2026-10-05/review-recovery-health-schema.json) | [BLOCK reserved map marker](evidence/map-health-2026-10-05/review-ui-health-schema.json) |
| a960/1ba6/2a36 | [FULL PASS](evidence/map-health-2026-10-05/review-recovery-health-markers.json) | [FULL PASS](evidence/map-health-2026-10-05/review-ui-health-markers.json) |

H07의 null/미등록 pointer와 executable/entry point 잘못된 타입, H08의
library versions/pointer map 예약 serdes 키 우회는 실제 설치 CLI 반례로 확인했다.
표준 module/file/package profile과 nullable metadata 타입을 검사하고 다섯 reserved
marker를 거부하되 Map default repository 이름 `__repository__`는 허용한다.
stateful/custom typed metadata는 명시적인 공통 profile 확장 전까지 실패로 판정한다.
[채택 가이드 §10](../../runbooks/dagster-adoption.md#10-code-server-자식-로딩을-확인하는-경량-건강-점검)은 지원 범위·15초 health timeout·소비자 재시작 정책 경계를 설명한다.

작성자의 [전체 Python160 PASS](evidence/map-health-2026-10-05/root-common-markers-python160.log),
[health65 PASS](evidence/map-health-2026-10-05/root-common-markers-health65.log), Ruff,
clean wheel/core-only 설치와 [정확 source CI8 PASS](evidence/map-health-2026-10-05/common-markers-exact-ci.json)를 확인했다.
복구 리뷰어는 별도 전체160·Map 봉인10 및 실제 CLI23사례를, UI 리뷰어는
health65·실제 CLI26사례를 직접 실행했다. health65는160의 부분집합이며 서로 다른
작성자·리뷰어 실행 수치를 합산하지 않는다. JSON의 raw UTF-8 원문과 original SHA는
이전 BLOCK을 포함해 불변으로 보존했다.

[같은 Linux venv의 fresh process import 측정](evidence/map-health-2026-10-05/health-markers-import-memory.json)은
경량 점검 import+합성 정상 reply decode 36,976–37,092 KiB, 전체 Dagster import
68,360–68,596 KiB의 최고 RSS를 각각3회 확인했다. 운영 컨테이너/live RPC workload나
provider/PG 메모리 측정은 아니다. 운영의 installed module hash·CLI·native daemon
장애 복구·브라우저 결과는 실제 재구축이 성공한 후 별도 증거로 확정한다.

## 2026-10-06 외부 frontend 의존 축소 후 source 확인

Common `a960bdb1`, Map `1ba6ef4c`, PinVi `0058369c`의
[111파일 manifest](evidence/map-health-2026-10-05/manifest-builtin.json)를
[복구 리뷰어](evidence/map-health-2026-10-05/review-recovery-builtin.json)와
[UI 리뷰어](evidence/map-health-2026-10-05/review-ui-builtin.json)가 각각 FULL 연속 PASS로 판정했다.
Common·Map 제품은 동일하며 PinVi API/ETL Dockerfile 첫 두 줄과 journal만 바뀌었다.
API/ETL은 표준 명령만 사용하므로 BuildKit 내장 parser를 사용하고,
COPY --parents가 필요한 Web은 digest 고정 labs frontend를 유지한다.
내장 parser 버전은 실제 builder 버전에 결합되며 외부 BUILDKIT_SYNTAX override 미사용과
builder 버전을 실제 재구축 기록에서 별도로 검증해야 한다.
[Common 정확 source CI8](evidence/map-health-2026-10-05/common-builtin-exact-ci.json)는 PASS다.
[세 번째 실제 실패](evidence/map-health-2026-10-05/rebuild-markers-third-negative.json)는
기존 운영 6개 서비스와 generation을 유지했다. 실패·소스 PASS는 새 runtime/live PASS로 바꾸지 않는다.

## 최종 CI: 바이너리 캡처 보존 계약

최초 문서 HEAD `a891c08`의 문서 링크·계획·337 도구 테스트는 통과했으나 전체 트리 정보 유출 검사기는 PNG를 UTF-8로 해석할 수 없어 fail-closed했다. 검사기·정책·예외를 완화하지 않고 현재 Common 트리의 중복 PNG만 제거하고 [고정 원본 링크·SHA256 색인](evidence/map-health-2026-10-05/ui-ticks-retry1-screenshots/README.md)과 [8개 바이트 동일성 증명](evidence/map-health-2026-10-05/ui-ticks-retry1-screenshots/storage-proof.json)을 추가했다. Map·PinVi의 원본 PNG와 Common 최초 보존 Git history, 기존 영수증·리뷰 원문·manifest를 보존한다. 제품 코드와 실제 재구축 source는 변경되지 않았다.

보존 위치 변경의 두 좁은 독립 리뷰 [A](evidence/map-health-2026-10-05/final-ci-storage-review-recovery.md)·[B](evidence/map-health-2026-10-05/final-ci-storage-review-ui.md)는 PASS, 새 finding0이다. [최초 실제 CI 실패](evidence/map-health-2026-10-05/final-ci-first-attempt-negative.json)의 source/job/사유·private 원문 digest를 보존했다. 전체 트리 secret/redaction1047파일·발견0, 문서676개/로컬대상2769개·오류0을 root가 실행했다. reviewer의 미실행 CI/머지는 이 수용 범위에 넣지 않는다.
