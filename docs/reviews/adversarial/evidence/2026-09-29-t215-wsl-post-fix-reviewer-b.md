# T-215 WSL post-fix 독립 리뷰 B 원본

- 실행 ID: `/root/review_wsl_ui` post-fix-01.
- 전문 영역: React UI·접근성·패키징·lock·CI·라이선스·정합.
- 시작: 2026-09-29T08:32:00+09:00.
- 종료: 2026-09-29T08:32:19+09:00.
- candidate: `b4a3a77095f61794eb3ff0a6ade9992bd38ce724`.
- tree: `0f4fa9195f3c0ba8de2b7bf7caf1a3829db9b075`.
- delta base: `26c849b17385eee7330a5200af0f8888582ea698`.
- 최초 제품 후보: `dd084f1a191f04cd17a55065c7ace734e526674a`.
- manifest: `dc972811e5f83952e2a061ce395608c4dce8cd42:docs/reviews/adversarial/evidence/2026-09-29-t215-wsl-post-fix-manifest.md`.
- 직접 확인 manifest SHA256: `804d8422ca8125e9fabf1d771523595352f97b269dc70f759dd80a8a5e5f35f4`.
- 격리: WSL Git object-only. 실제 candidate/tree 일치, 시작·종료 작업 HEAD `dc972811e5f83952e2a061ce395608c4dce8cd42`, 두 시점 porcelain 출력 없음. 후보 수정 없음. 상대 새 리뷰 원본·finding 열람 없음.

## 전달 요청 원문

> 독립 post-fix 리뷰 B. WSL 동일repo candidate b4a3a77095f61794eb3ff0a6ade9992bd38ce724 tree0f4fa9195f3c0ba8de2b7bf7caf1a3829db9b075 delta base26c849b17385eee7330a5200af0f8888582ea698. manifest는 dc972811e5f83952e2a061ce395608c4dce8cd42:docs/reviews/adversarial/evidence/2026-09-29-t215-wsl-post-fix-manifest.md SHA256804d8422ca8125e9fabf1d771523595352f97b269dc70f759dd80a8a5e5f35f4. 최초 CI packages EINTEGRITY: 동적으로 생성하는 로컬 tarball 체크섬의 환경차이. 수정은 prepare-lock.mjs 두 file 경로만 assert/sha512 갱신, CI한줄+README. 나머지는 이전 raw/기록. 자신의 관점+전체 delta 회귀를 object-only로 확인하고 hash/clean 시작종료 기록. 원본 test-results/t215-merge/post-fix-reviewer-b.md(원checkout)에 저장. 상대 새 결과 열람금지. Python337 중336성공/Win전용1skip 완료. npm ci 재설치/후속CI 진행 예정. 새 코드finding 없으면 명확히 결과 확정해 주세요.

## 검토와 공격 시나리오

전체 delta는 8개 파일이다. 기능 변경인 prepare-lock.mjs·CI·README를 전부 읽고 task·archive 기록 변경을 확인했다. 이전 독립 원본과 통합 report 보존 파일은 새로운 기능 변경으로 보지 않는다. 최초 리뷰의 UI source·test·package manifest·3개 lock·versions.json이 그대로임을 `git diff --quiet` exit 0으로 확인했다.

- registry integrity 검증 우회: 준비 스크립트는 명시한 UI·tokens 두 로컬 항목만 접근한다. manifest dependencies·lock root dependencies·resolved가 고정 file 경로와 같은지 assert한다. 다른 npm 버전·resolved·integrity 값을 수정하는 코드가 없다.
- 임의 파일 접근과 경로 혼동: tarball 이름과 상대 경로는 코드 상수이며 외부 입력을 쓰지 않는다. 경로는 process cwd가 아닌 import.meta.url에서 fixture 위치를 기준으로 계산한다. README와 CI의 작업 디렉터리 차이가 해석에 영향을 주지 않는다.
- 실패 중 일부만 기록: 두 항목을 메모리에서 확인·해시한 후 마지막에 한 번 write한다. 누락 파일·불일치 경로·lock entry 누락은 쓰기 전에 예외로 종료한다. CI는 pack 두 번 직후 준비 스크립트를 실행하므로 의도한 최신 생성물에 대해 npm ci를 수행한다.
- digest 신뢰 경계: 같은 checkout에서 방금 생성한 개발 tarball의 설치 시험에만 적용한다. registry 공급망 고정값이나 발행 tarball digest 검증을 완화하지 않으며 README가 이 차이를 명시한다. 기존 커밋 lockfile을 런타임 생성물 digest로 바꾸는 이유가 범위와 맞는다.
- 회귀: 기존 Next 두 빌드·시각 예시·단위 검증의 실행 순서를 유지한다. 고정 action SHA·권한 변경은 없다. SPDX·저작권 헤더가 추가 스크립트에 있고 UI 런타임 파일이나 공개 계약은 바뀌지 않았다.
- 감사성: 기존 packages 실패를 삭제하지 않고 task·archive에 보존했다. Python337개 중336성공·1skip을 전체337 PASS로 세지 않았으며 shell wrapper 실패와 시험 결과를 구분했다.

## 검증과 한계

직접 수행: commit/tree/manifest digest, 시작·종료 clean, 전체 delta 공백 검사, 기존 기능·lock·버전 무변경 검사. 모두 통과했다.

부모가 전달한 Python 결과와 의도적으로 틀린 두 integrity의 복구 검증은 부모 evidence로 구분한다. 이 reviewer는 object-only 방식이므로 새 준비 스크립트 실행·npm ci·후속 CI를 직접 실행하지 않았다: `NOT_RUN(부모 검증 및 CI에서 수행)`.

## Finding과 판정

신규 P0·P1·P2·P3 finding 없음. 최초 리뷰의 코드 PASS 판정이 유지되며 이번 수정에 추가 코드 요구가 없다.

코드 post-fix 판정: PASS.

Merge verdict: CONDITIONAL. 후속 실제 npm ci·필수 CI와 다른 독립 reviewer gate가 통과해야 한다. 이 조건은 수정 코드의 재작성 요구가 아닌 실행 gate다. 제품 변경 없이 결과만 기록하면 closure artifact로 종료할 수 있다.
