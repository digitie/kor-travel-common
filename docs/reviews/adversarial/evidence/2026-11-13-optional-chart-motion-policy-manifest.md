# 선택형 차트·애니메이션 정책 검토 입력

- 입력 ID: COMMON-OPTIONAL-CHART-MOTION-20261113-01
- 기준: `2a34d8557ea055d4b7dd4c5d18e858faa901bf4a`
- 불변 검토 기준: 이 파일과 아래 파일을 포함한 PR head 전체 SHA·tree를 검토 요청에 고정한다. 이동 branch 이름으로 검토하지 않는다.
- 범위: 두 선택형 npm 축·생성 JSON·필요 라이브러리 규약과 T-218 수용 기준. 소스·프로필·배포 산출물 변경은 별도다.

## 파일 SHA256

| 파일 | SHA256 |
|---|---|
| `versions.json` | `4a395750e29ff6f823a9a6e6758838e13d6908674727f7e09f14e5fb5ae04a5d` |
| `frontend-dependencies.json` | `62b21a2c207d4d940429d7d50c0be694cb8b28f8b43e6661c1420405c94f46a8` |
| `docs/standards/frontend-libraries.md` | `379df4650d2431308349650cb55d2750fcae38b8ecdd6b96a270f2d860e6ee48` |
| `docs/tasks/T-218-radix-library-unification.md` | `9def4cbed2972f85894ced52130dec1a5aa9d47740379c91ff4f2428aac29c08` |
| `docs/resume.md` | `7af8c81981114e93d328cea47cc2642e04e1e08a08d9a30d35129d33ae58ad5e` |
| `docs/journal.md` | `8829e69b7929e85e083541cbb00dc57feef4e2d508f1c8c8686f9abc7fa28294` |

## 수용·공격 관점

- [라이브러리 규약](../../../standards/frontend-libraries.md)·[T-218](../../../tasks/T-218-radix-library-unification.md)의 선택형 수용 기준을 검사한다. 필수 목록 확대·미사용 앱 설치 강제·C11 동일 버전 재pack을 허용하지 않는다.
- 두 전문 관점의 독립 리뷰는 같은 고정 입력을 사용하며 상대 CURRENT 판정·원문을 열람하지 않는다. 생성 일치·정확 선언/lock·별칭 identity·미사용 web/mobile·기존 범위 보존을 대조한다.
- 공식 npm registry `https://registry.npmjs.org/echarts/latest`·`https://registry.npmjs.org/motion/latest`의 2026-11-13 조회 메타데이터를 기준으로 했으며 기존 소비자의 Motion patch 정렬은 해당 앱 PR의 별도 gate다.

## 직접 검증과 한계

- 기존 정책194개와 문서 생성 계약6개가 통과했다. 실제 중앙 CLI의 선택형8경우/16관찰에서 과거 버전·lock drift·alias 거부, 미사용 web/mobile·정본·무관 의존성 허용을 확인했다. 해당 graph는 fixture이며 실제 앱 설치·실행 증거가 아니다.
- 생성 check·문서 링크·plan·registry 자체 검사·diff check가 통과했다. 로컬 정책/생성 실행 Node22.22.2 결과는 CI의 정본22.23.1/npm12.0.1 결과와 구분한다.
- 전체 잠긴 CI·원2 독립 리뷰·소비자별 버전/참조 전파·이미지·운영 수용은 이 후보의 후속 gate다. 새 패키지 pack·배포·Map 작업·CI 순서 분석은 실행하지 않았다.
