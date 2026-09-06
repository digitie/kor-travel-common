# T-013 인계 시점 재확인

이 문서는 2026-09-06 인계 과정에서 기존 초안의 불확실한 주장을 다시 확인한 evidence다. 전체 재조사가 아니며 과거 [조사 기준](../survey/README.md#21-조사-정본-체크아웃-로컬-원본-경로)을 대체하지 않는다. 실행 순서는 [통합 계획](integration-plan.md), 현재 상태는 [resume](../resume.md)을 따른다.

## 1. airport의 기준선 변화

직접 조회한 [PR #18](https://github.com/digitie/kor-travel-airport/pull/18)은 2026-09-06 01:09:49 UTC에 `67e9199afaa23e6d0e47235b1ed02444d7102aa7`로 병합됐다. 초안이 대기 중이라고 적은 shadcn 기반 작업이다. [PR #22](https://github.com/digitie/kor-travel-airport/pull/22)의 T-035 라우트 셸도 같은 날 07:58:00 UTC에 `0f157514aee5d9d4fa2792754055b82d9dbb9485`로 병합됐다.

- 조회한 로컬 `origin/main`: `0f157514aee5d9d4fa2792754055b82d9dbb9485`.
- 로컬 작업 HEAD: `2e114b0a0530b32b72cca035ad0366ddb93c6cd2`, branch `docs/t035-completion`, dirty 4건. 파일·branch를 변경하지 않았다.
- PR #22 조회 결과: backend·frontend 성공, live-e2e 실패. 병합을 전체 검증 성공으로 취급하지 않는다.
- `frontend/package.json` 선언: Next `^16.3.2`, React `^19.2.8`, TypeScript `^7.0.2`, Tailwind `^4.3.3`, Base UI `^1.8.0`. 설치본·실행값의 증거가 아니다.

판정: T-430에서 과거 WIP를 다시 병합하지 않는다. 현재 기준 SHA와 이미 반영된 항목을 대조하고 잔여 정렬·CI 실패만 해당 저장소 task·PR로 요청한다. T-431·T-432의 common 채택은 여전히 미실행이다. 현 Admin 범위도 현재 라우트 코드에서 다시 정하되 common의 도메인·인증 경계는 유지한다.

## 2. 다른 소비자 점검 범위

| 대상 | 직접 확인한 HEAD | checkout 상태 | 확인한 범위 |
|---|---|---|---|
| map 조사 checkout | `c494e227e010565be295de3f9670b2f7c8c20944` | clean | admin manifest의 선언·engines |
| weather | `6003da995fa4b35799f9dadc406c6ba2878bfbae` | clean | admin manifest의 선언·engines 미선언 |
| geo | `1d9d74d3a852bbaaa09144b75bb69b99a58a6002` | clean | 기준 commit·상태 |

소비자 빌드·설치·e2e는 NOT_RUN(이번 작업에서 실행하지 않음). 전체 소비자 설치 버전 보고는 T-005 잔여다. shallow clone·고정 조사 checkout의 HEAD가 실제 서비스 최신 버전임을 뜻하지 않는다.

## 3. 공식 버전 메타데이터

조회일 2026-09-06. 공식 npm 메타데이터에서 [Next 16.3.4](https://registry.npmjs.org/next/16.3.4), [React 19.2.8](https://registry.npmjs.org/react/19.2.8), [TypeScript 7.0.2](https://registry.npmjs.org/typescript/7.0.2)의 존재를 재확인했다. 전체 축을 다시 검증한 결과가 아니며 공통 권장값 변경도 아니다. 값 정본은 [`versions.json`](../../versions.json)이고 실제 소비자 적용 가능성은 lock·빌드 evidence로 별도 검증한다.

## 4. 재현 명령

```bash
gh pr view 18 --repo digitie/kor-travel-airport --json state,mergedAt,mergeCommit,url
gh pr view 22 --repo digitie/kor-travel-airport --json state,mergedAt,mergeCommit,statusCheckRollup,url
git -C <airport-checkout> rev-parse HEAD origin/main
git -C <airport-checkout> status --porcelain=v1
git -C <airport-checkout> show HEAD:frontend/package.json
```

Git Bash에서 동일. 로컬 경로는 [조사 checkout 표](../survey/README.md)에만 둔다. 작업 중인 소비자 파일이나 운영 정보를 evidence로 복사하지 않는다.
