# T-215 WSL post-fix 공통 manifest

- 종류: full post-fix, CI 설치 절차 변경.
- Candidate: `b4a3a77095f61794eb3ff0a6ade9992bd38ce724`.
- Tree: `0f4fa9195f3c0ba8de2b7bf7caf1a3829db9b075`.
- Delta base/parent: `26c849b17385eee7330a5200af0f8888582ea698`. 최초 제품 후보 `dd084f1a191f04cd17a55065c7ace734e526674a`, PR base `afc8d1bf166d0ddcbee059252eb5cee245157dcd`.
- 요청·정본·범위 밖: [최초 manifest](2026-09-29-t215-wsl-manifest.md)와 동일.
- Delta: 동적 로컬 tarball 2개의 integrity를 생성 바이트로 갱신하는 준비 스크립트, CI 한 줄, 예시 명령/설명. 나머지는 최초 독립 원본·통합 report·task 상태 기록이다.
- 배경: 첫 packages CI에서 WSL tarball digest와 Linux checkout 산출물 digest가 달라 EINTEGRITY. registry 버전/URL/integrity의 변경·검증 완화 없이 실제 생성한 두 로컬 file 항목만 갱신한다.
- 실행 검증: 로컬 두 integrity를 의도적으로 틀린 값으로 바꾸고 준비 스크립트를 실행한 뒤 전체 JSON이 원본과 일치함을 확인했다. registry graph 불변. 실제 npm ci 및 후속 CI는 부모가 최종 확인한다. Python337개 중336성공·Windows전용1skip, shell wrapper 빈 exit 인수 오류는 별도 기록. UI29/tokens7 및 최신 Next 빌드·브라우저 결과는 코드 변경 없이 유지된다.
- 격리: WSL Git object-only, candidate/tree/hash·시작/종료 clean. 각 역할은 자신의 이전 관점과 전체 delta 회귀를 검토한다. 새 상대 결과는 각 원본 확정 전 열람하지 않는다.
- 출력: reviewer별 실행ID·요청·시각·hash·범위·finding·verdict·미실행 범위. 원본은 원 checkout의 test-results/t215-merge/post-fix-reviewer-{a,b}.md에 저장한다.
