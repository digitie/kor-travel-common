# T-005 고정 입력 실측 보고

2026-09-07 실행. common 도구를 7개 소비자의 고정 Git object에서 추출한 manifest/lock 메타데이터에 적용했다. 소비자 작업 트리·branch·원격은 수정하지 않았다. 원본 입력은 common의 무시되는 임시 디렉터리에만 보관하며 이 evidence에는 digest와 버전 판정만 남긴다.

## 입력과 재현

[inputs.json](inputs.json)은 저장소·40자리 commit·파일별 SHA-256·검사기/레지스트리의 LF 정규화 digest를, [reports.json](reports.json)은 전체 판정과 exit를 담는다. 경로 정보만 `versions.json` 및 `<repo>@<commit>`으로 정규화했다. 로컬 절대 경로·비밀·소비자 원문 파일은 커밋하지 않는다.

원천의 해당 commit에서 각 `files[].path`를 `git show <commit>:<path>`로 읽고 digest를 대조한 후 같은 상대 디렉터리를 유지해 common 임시 입력 루트에 둔다. 네트워크와 패키지 설치가 필요 없는 도구이며, 파일을 실행하지 않는다. 다음 명령의 `<repo>`에는 정식 저장소 이름을 넣는다.

```bash
python3 -B -X utf8 tools/check_versions.py <입력-루트> --repo <repo> --today 2026-09-07 --json report.json --quiet --no-step-summary
```

모드는 CLI로 강제하지 않고 registry의 `report`를 사용했다. 모든 report exit는 0이지만 아래 위반이 있으므로 clean run이 아니다. 검사기는 깊이 4의 manifest와 연결 lock을 검사하며, 조사 원천 전체나 배포 환경을 검증하지 않는다.

## 실행 결과

| 소비자 | 입력 commit | OK | BELOW_FLOOR | NOT_RECOMMENDED | NO_LOCK | NO_ENGINES | FLOATING_REF | EXEMPT |
|---|---|---|---|---|---|---|---|---|
| kor-travel-airport | [bb47f10](https://github.com/digitie/kor-travel-airport/tree/bb47f107e26faa98d725ab866fba88bb071ae81d) | 19 | 1 | 2 | 0 | 1 | 0 | 1 |
| kor-travel-concierge | [7945305](https://github.com/digitie/kor-travel-concierge/tree/7945305dd8bcb3eccae54e08b1205d565daa3661) | 7 | 4 | 7 | 14 | 5 | 0 | 1 |
| kor-travel-docker-manager | [862562d](https://github.com/digitie/kor-travel-docker-manager/tree/862562dcbd6a70c5d00e8d1538264fafe5ed5f5c) | 4 | 0 | 1 | 9 | 1 | 0 | 3 |
| kor-travel-geo | [1d9d74d](https://github.com/digitie/kor-travel-geo/tree/1d9d74d3a852bbaaa09144b75bb69b99a58a6002) | 12 | 0 | 6 | 24 | 1 | 0 | 1 |
| kor-travel-map | [c494e22](https://github.com/digitie/kor-travel-map/tree/c494e227e010565be295de3f9670b2f7c8c20944) | 33 | 0 | 4 | 26 | 0 | 0 | 4 |
| kor-travel-weather | [6003da9](https://github.com/digitie/kor-travel-weather/tree/6003da995fa4b35799f9dadc406c6ba2878bfbae) | 37 | 1 | 1 | 0 | 1 | 0 | 2 |
| pinvi | [9af25e5](https://github.com/digitie/pinvi/tree/9af25e58cf77b360188a69e26a36a0588063aa8b) | 54 | 4 | 5 | 9 | 0 | 1 | 0 |

나머지 ABOVE_MAX·BLOCKED·EXEMPT_EXPIRED는 이 입력에서 0이다. 이는 해당 판정의 미검사나 시험 0을 뜻하지 않으며, 회귀 시험은 10개 판정과 3개 모드를 별도로 고정한다. 전체 위반·권장 차이·예외 행의 scope/설치본/근거는 reports.json에 있다.

## 예외 재대조

기존 12개 예외의 숫자 접두·기한·강제 수준은 바꾸지 않았다. 소비자의 실측 설치값은 reports.json, 승인 정책은 versions.json 한 곳에 둔다.

| 대상 | 실측과 처리 |
|---|---|
| map npm·Next·Playwright | 고정 lock/선언에서 예외 접두와 일치. EXEMPT 행 확인 |
| map Starlette | Python lock 없음. NO_LOCK이므로 예외 적용 미검증. T-480 유지 |
| map Alembic | 기존 floor와 선언 상한이 충돌하지 않으며 lock도 없음. 불필요한 예외를 신설하지 않음 |
| geo React | 기존 예외 적용. React 19 채택 승인(T-443)은 별개 |
| docker-manager React·Next·ESLint | 기존 예외 적용. T-470에서 소비자 정렬 |
| weather Next·Vitest | 기존 예외 적용. T-460에서 소비자 정렬 |
| airport TypeScript | 고정 lock과 기존 예외 접두 일치. CI 성공은 미검증(T-433) |
| concierge maplibre | 기존 예외 적용. base-ui 하향 예외는 승인되지 않아 BELOW_FLOOR 유지 |
| pinvi mobile Tailwind | O-8 미승인. BELOW_FLOOR 유지 |

## 검증과 한계

- Windows Python 3.14.3에서 7개 보고 명령을 실행했다. 다른 환경의 동일성·전체 도구 시험·독립 리뷰 결과는 [T-005 evidence](../../tasks/T-005-versions-registry.md#evidence)에 기록한다.
- 이전 검사에서 전이 설치본 누락 때문에 보이지 않던 airport·concierge·pinvi의 BELOW_FLOOR가 추가됐다. 기존 조사 본문을 현재 결과로 덮어쓰지 않았다.
- uv의 marker·workspace 전체 해석은 T-005a, Poetry·requirements 잠금 해석은 T-005b의 잔여다. 현재 Python 값은 지원하는 초안 경로로 읽었으며 NO_LOCK을 설치 성공으로 바꾸지 않는다.
- 입력 manifest/lock 대조는 npm ci·uv sync·제품 build·e2e·소비자 CI 실행의 증거가 아니다. 이 gate는 NOT_RUN(소비자 저장소 실행)이며 해당 이관 task에서 수행한다.
- report 2회 위반 0 조건을 충족하지 않아 7개 소비자 모두 clean_runs 0·report 유지다.


## 리뷰 수정 후 대조

위 원본은 409b95c의 코드에 고정된 기록이다. [수정 코드 digest](post-fix.json)는 리뷰 수정 후 검사기와 동일 입력/전체 보고의 재대조 결과를 기록한다. 원본 입력·보고를 최신 코드의 실행으로 소급 변경하지 않는다.
