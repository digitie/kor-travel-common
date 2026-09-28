# T-215 WSL post-fix 독립 리뷰 A 원본

- 실행 ID: `/root/review_wsl_security`의 post-fix 실행.
- 전문 영역: 인증·redirect·API 및 설치 검증의 신뢰 경계.
- 시작: 2026-09-29 08:31:44+09:00. 종료: 08:32:23+09:00.
- 코드 리뷰 verdict: **PASS**, 신규·잔여 P0/P1/P2/P3 finding 0건.
- 별도 merge gate: 수정 후 실제 `npm ci`와 필수 원격 CI의 결과를 최종 merge 담당이 확인해야 한다. 이 리뷰는 미완료 CI를 통과로 바꾸지 않는다.

## 전달 요청 원문

> 독립 post-fix 리뷰 A. WSL 동일repo candidate b4a3a77095f61794eb3ff0a6ade9992bd38ce724 tree0f4fa9195f3c0ba8de2b7bf7caf1a3829db9b075 delta base26c849b17385eee7330a5200af0f8888582ea698. manifest는 dc972811e5f83952e2a061ce395608c4dce8cd42:docs/reviews/adversarial/evidence/2026-09-29-t215-wsl-post-fix-manifest.md SHA256804d8422ca8125e9fabf1d771523595352f97b269dc70f759dd80a8a5e5f35f4. 최초 CI packages EINTEGRITY: 동적으로 생성하는 로컬 tarball 체크섬의 환경차이. 수정은 prepare-lock.mjs 두 file 경로만 assert/sha512 갱신, CI한줄+README. 나머지는 이전 raw/기록. 자신의 관점+전체 delta 회귀를 object-only로 확인하고 hash/clean 시작종료 기록. 원본 test-results/t215-merge/post-fix-reviewer-a.md(원checkout)에 저장. 상대 새 결과 열람금지. Python337 중336성공/Win전용1skip 완료. npm ci 재설치/후속CI 진행 예정. 새 코드finding 없으면 명확히 결과 확정해 주세요.

## 기준선·독립성

- Candidate: `b4a3a77095f61794eb3ff0a6ade9992bd38ce724`.
- Tree: `0f4fa9195f3c0ba8de2b7bf7caf1a3829db9b075`.
- Delta base: `26c849b17385eee7330a5200af0f8888582ea698`.
- Manifest commit: `dc972811e5f83952e2a061ce395608c4dce8cd42`.
- Manifest SHA256 직접 확인: `804d8422ca8125e9fabf1d771523595352f97b269dc70f759dd80a8a5e5f35f4`.
- Git object-only로 모든 변경 소스·문서를 읽었다. 시작 HEAD는 manifest-only commit이고 시작·종료 `git status --porcelain=v1` 출력이 비었다. candidate/tree를 종료에 재확인했다.
- 현재 상대 post-fix 결과를 열람하지 않았다. 두 원본이 이미 확정된 최초 통합 report는 이번 delta의 감사 기록으로만 읽었다.
- 최초 A 원본 Git blob SHA256이 `e8ba039ed24303fdf359a16bbbb6a537c77058b317330e6d1269a3cf64854c5c`와 동일하여 원본 보존도 확인했다.

## 검토 범위와 실패 관점

전체 8파일 delta 목록과 실행 변경 3파일(`prepare-lock.mjs`, workflow, 예시 README), task 상태·통합 report·archive 기록을 검토했다. 최초 제품 소스/시험의 `git diff --quiet` exit 0으로 인증·라우팅·비동기 동작에 새 delta가 없음을 확인했다. 기존 규칙·수용 기준은 최초 리뷰와 동일하다.

1. 준비 스크립트가 임의 registry 패키지의 integrity를 승인하는지 확인했다. 두 고정 이름만 순회하고 manifest·lock root dependency·entry.resolved가 정해진 `file:` 문자열과 모두 같아야 진행한다. 실제 bytes에서 SHA512를 계산하여 해당 두 entry.integrity만 바꾼다. registry URL/버전/integrity는 변경하지 않는다.
2. 조작된 manifest/lock 경로나 누락된 tarball에서 잘못된 검증을 성공으로 표시하는지 추적했다. assert/readFileSync가 실패하면 throw하며 최종 write까지 도달하지 않는다. 첫 항목 성공 후 두 번째 실패도 디스크 lock에 부분 기록하지 않는다. tarball 경로는 외부 입력에서 유도되지 않는다.
3. 공급망 검증을 일반적으로 약화하는지 확인했다. 수정은 동일 CI가 직전에 `npm pack`으로 만든 두 개발 산출물만 대상으로 한다. 원격 registry 체크섬이나 게시 패키지 무결성 검증을 우회하지 않으며 README가 적용 범위를 명시한다. CI는 준비 직후 `npm ci`를 실행한다.
4. 기존 UI 보안 계약의 회귀를 확인했다. 제품 소스/시험 변경이 없어 동일 틱 중복 방어·비밀번호 정리·안전한 redirect·서버 원문 오류 차단·메뉴 접근제어 책임은 최초 검토 결과를 유지한다.
5. 실패 evidence를 성공으로 덮는지 확인했다. 최초 packages EINTEGRITY와 당시 merge BLOCK 기록이 보존되고 Python 336성공·1skip 및 wrapper 오류를 구분한다. 새 CI 성공을 미리 주장하지 않는다.

## 실행과 한계

이 reviewer는 Git 객체·hash·clean·delta 검사를 직접 수행했다. object-only 격리를 유지하기 위해 lock을 쓰는 준비 스크립트와 `npm ci`는 독립 실행하지 않았다. 준비 스크립트의 고의 integrity 불일치 복구/registry graph 불변 결과와 Python337개 중336성공·Windows전용1skip은 manifest·부모 전달 evidence이며 독립 실행 성공으로 집계하지 않는다. 수정 후 CI는 이 실행 시점 NOT_RUN(후속 실행 예정)이다.

코드 리뷰 **PASS**. 원격 CI와 실제 설치 검증이 성공한 뒤 최종 merge 판정을 진행할 수 있다. 소비자 저장소 build/e2e·실제 인증·배포·게시 검증은 범위 밖이다.

원본 최종 확정 전 부모 추가 전달: 수정 후 실제 smoke fixture npm ci가 exit 0으로 49개 패키지를 설치했다. 최초 CI는 packages만 EINTEGRITY로 실패하고 docs/tools Ubuntu·Windows/secret/version/selftest는 통과했다. 수정 CI run 36498511136 및 selftest 36498511297은 진행 중이다. 이는 부모 실행 결과로 구분하며 후속 CI 성공은 아직 주장하지 않는다.
