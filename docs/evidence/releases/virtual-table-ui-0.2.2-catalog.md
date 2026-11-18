# VirtualTable UI 0.2.2의 main pack 취득과 catalog 동결 후보

## 고정 출처

- 제품 PR: [Common #68](https://github.com/digitie/kor-travel-common/pull/68)
- 독립 리뷰 head: f571767711f5e0f7010e070f3c426ed578aacaeb
- 실제 main merge/pack source R: 706aaa7821588dfca72f660c9161f56be2d0445f
- source tree: d8e2209d10930e4ccc199fffee3f7cc508ee3718 — 검토 head와 R이 동일하다.
- main push CI: [docs 44313659808](https://github.com/digitie/kor-travel-common/actions/runs/44313659808), [common frontend 44313659675](https://github.com/digitie/kor-travel-common/actions/runs/44313659675), [python-package 44313659817](https://github.com/digitie/kor-travel-common/actions/runs/44313659817) 모두 SUCCESS.
- 실제 [main artifact 14430019630](https://github.com/digitie/kor-travel-common/actions/runs/44313659808/artifacts/14430019630): common-release-packs-706aaa7821588dfca72f660c9161f56be2d0445f.
- ZIP bytes: 127611, SHA256 f6f8d7832426a6b5a76c6a300583550fe56fb6be7d8d6738397c4fbf29322700.
- 만료: 2026-12-18T13:30:19Z. PR artifact나 로컬 재pack을 배포 정본으로 사용하지 않았다.
- GitHub plugin의 artifact file reference를 로컬에 materialize했고 API archive digest와 일치했다. 인증 값·서명 download URL은 기록하지 않는다.

## 원본 pack과 실제 설치

원본 bundle의 [SOURCE_SHA](virtual-table-ui-0.2.2/SOURCE_SHA), [SHA256SUMS](virtual-table-ui-0.2.2/SHA256SUMS), [SRI](virtual-table-ui-0.2.2/SRI)를 그대로 보존한다. [취득 receipt](virtual-table-ui-0.2.2/acquisition-receipt.json)와 [실제 설치 receipt](virtual-table-ui-0.2.2/installed-receipt.json)는 실행 결과다. tgz 자체는 CI artifact에 보존하며 이 PR에서 재생성하거나 다른 bytes로 교체하지 않는다.

| 패키지 | 버전 | SHA256 | 실제 설치 regular file 대조 |
| --- | --- | --- | --- |
| @kor-travel/ui | 0.2.2 | 76ecace688c061b2dd8dc49b5a18b7acf37e7e4c6bbdec71fe863187483c7033 | 94개 동일 |
| @kor-travel/tokens | 0.1.3 | e6a0eca29bb1568bc7b858dc15cb1d41ea6c264c0e02be3209db094b08e8f464 | 25개 동일 |
| @kor-travel/toast | 0.1.2 | 133e2815053544997197e65a201a65c688bc0ae0a57fe604569bc720831da36f | 8개 동일 |

로컬 외부 helper의 실제 명령은 아래와 같다. ROOT는 작업 전용 /home/digitie/dev/odroid-disk-remediation-20261117이며 원본 Geo cwd는 사용하지 않았다.

    python3 -B "$ROOT/common-main-artifact-acquisition/acquire-main-release.py" --merge-sha 706aaa7821588dfca72f660c9161f56be2d0445f --out "$ROOT/common-main-release-706aaa7821588dfca72f660c9161f56be2d0445f" --archive "$ROOT/common-main-artifact-acquisition/downloaded-main-706aaa-packs.zip"
    python3 -B "$ROOT/common-main-artifact-acquisition/verify-actual-install.py" --acquired "$ROOT/common-main-release-706aaa7821588dfca72f660c9161f56be2d0445f" --allow-network

취득은 main push/source tree·CI·artifact 이름/digest·SOURCE_SHA·각 tar SHA256/SRI·npm identity/version·source R의 frontend-dependencies.json과 각 embedded policy bytes·실제 VirtualTable dist의 min-w-0을 확인했다.

Node 26.13.1/npm 12.0.1의 새 minimal fixture에서 npm install --package-lock-only 후 실제 npm ci를 실행했다. --ignore-scripts·--no-audit·--no-fund·--engine-strict·--prefer-offline을 사용했고 peer/engine guard를 우회하지 않았다. 설치본 전체 regular file bytes·lock version/SRI·exports 파일과 UI VirtualTable/tokens/Toast 실제 JS import가 PASS다. Next/Docker 무거운 로컬 빌드는 실행하지 않았다.

첫 --offline 시도는 Pretendard registry metadata ENOTCACHED로 중단됐다. 원본 실패 log를 보존하고 성공으로 세지 않았다. 별도 minimal install 디렉터리의 prefer-offline 재시도가 exit 0이었다. 기존 Next node_modules를 복제하지 않았다.

## 순환 없는 catalog 동결

[정본 정책 생성기](../../../tools/sync_frontend_policy.mjs)는 versions.json만 읽어 frontend-dependencies.json과 버전 표를 생성한다. [UI 동기화](../../../packages/ui/scripts/sync-policy.mjs)와 [tokens 동기화](../../../packages/tokens/scripts/sync-policy.mjs)는 생성 정책과 dependency checker를 복사한다. frontend-artifacts.json·SOURCE_SHA·현재 시각은 이 producer 입력이 아니다. catalog-only 변경으로 embedded policy를 다시 바꾸지 않는다.

[생산 workflow](../../../.github/workflows/docs.yml)는 실제 Next webpack/Turbopack/browser 검증에 설치한 UI/tokens pack과 정규 Toast pack을 source별 artifact에 보관한다. 이번 후보는 그 R bytes로 [frontend-artifacts.json](../../../frontend-artifacts.json)의 UI/tokens/toast 세 entry·candidate·sources.common/kor-travel-toast만 갱신한다. 다른 asset entry와 출처, CANDIDATE_NOT_RELEASED 상태, 버전축·package metadata/lock·policy·배포 파일은 유지한다.

후속 catalog merge를 P라고 한다. pack_source_sha=R, catalog_sha=P, 소비자가 고정할 policy_sha는 P 또는 같은 frozen catalog를 읽는 후속 main commit이다. R의 이전 catalog를 새 pack의 자기 catalog로 비교하지 않는다. 소비자 helper는 R package별 embedded policy와 P catalog의 실제 filename/version/SRI를 각각 확인한다.

P merge와 P main push CI/pack 비교는 현재 NOT_RUN(부모 merge 소유)이다. P의 동일 버전 세 tgz가 R과 전체 bytes 동일함을 확인하기 전 채택 완료로 표시하지 않는다. 다르면 기존 버전 bytes를 덮어쓰지 않고 중단한다. 외부 verify-catalog-policy.py가 이 대조를 수행한다.

## 원본 리뷰와 남은 단계

[두 원본·manifest·최종 disposition](../../reviews/adversarial/2026-11-18-common-virtual-table-overflow.md)을 archive한다. 두 PASS·P0~P3 각 0이며 원본 bytes를 바꾸지 않는다. closure 자료만으로 같은 리뷰를 재귀 실행하지 않는다.

소비자 편집·빌드·운영 배포·SDK·Map/N150·T-025 설계는 이 PR 범위 밖이다. 이 문서는 artifact catalog 후보의 실제 취득/설치 evidence이며 정식 Release 발행이나 소비자·운영 수용 완료 선언이 아니다.
