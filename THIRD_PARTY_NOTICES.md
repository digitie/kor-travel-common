# 서드파티 고지와 도입 후보 원문

마지막 확인: 2026-09-07, T-003. 현재 실제 이식물과 아직 도입하지 않은 후보를 구분한다. common에는 제품 패키지·lockfile이 아직 없으며 아래 후보 버전은 **고지 원문을 확보한 버전**이다. 설치·채택·최신 버전 판정이 아니다. 채택 PR에서 실제 lock·원천 커밋·파일을 대조해 고지를 갱신한다.

## 현재 이식물

| 구성요소 | 고정 원천 | 라이선스 | 사본·범위 |
|---|---|---|---|
| canview | [1f93b8adb34a48537db69b950c8a99ce89859760](https://github.com/digitie/canview/blob/1f93b8adb34a48537db69b950c8a99ce89859760/LICENSE) | 원천 GPL-3.0 버전 미지정, common 적용은 licensing LIC-34의 -or-later 재선언 | [원문](LICENSES/upstream/canview-LICENSE.txt), 파일별 [PROVENANCE PV-001~006](PROVENANCE.md) |
| kor-travel-geo | [1d9d74d3a852bbaaa09144b75bb69b99a58a6002](https://github.com/digitie/kor-travel-geo/blob/1d9d74d3a852bbaaa09144b75bb69b99a58a6002/LICENSE) | GPL-3.0-only(원천 pyproject.toml 선언, O-20 재선언 없음) | [원문](LICENSES/upstream/kor-travel-geo-LICENSE.txt), [설정 6개 고지](templates/agent-config/README.md), [PROVENANCE PV-007~012](PROVENANCE.md) |

## 도입 후보의 버전별 고지 사본

각 원문 링크는 npm 공식 registry의 해당 버전 배포물이다. 배포물을 실행·설치하지 않고 integrity를 검증한 뒤 라이선스 파일만 읽었다. tarball 내부 경로·전체 integrity·사본 SHA-256은 [sources.json](LICENSES/sources.json)에 있다. 원문에 포함된 모든 저작권 문구와 파생 원천 고지를 그대로 보존했다.

| 구성요소 | 확보 버전 | 원문 라이선스 | 원문 URL | 해당 버전 고지 사본 | common과의 관계 |
|---|---|---|---|---|---|
| shadcn | 4.21.0 | MIT | [공식 배포물](https://registry.npmjs.org/shadcn/-/shadcn-4.21.0.tgz) | [원문 사본](LICENSES/upstream/shadcn-4.21.0.txt) | 컴포넌트 레시피 후보. 기존 생성 시점 미기록 B6는 이 CLI 사본으로 해제하지 않음 |
| @base-ui/react | 1.8.0 | MIT | [공식 배포물](https://registry.npmjs.org/@base-ui/react/-/react-1.8.0.tgz) | [원문 사본](LICENSES/upstream/base-ui-react-1.8.0.txt) | overlay peer 후보 |
| radix-ui | 1.6.0 | MIT | [공식 배포물](https://registry.npmjs.org/radix-ui/-/radix-ui-1.6.0.tgz) | [원문 사본](LICENSES/upstream/radix-ui-1.6.0.txt) | geo 레시피 참조 후보. @radix-ui/* 21종 역추적 B5를 대신하지 않음 |
| class-variance-authority | 0.7.1 | Apache-2.0 | [공식 배포물](https://registry.npmjs.org/class-variance-authority/-/class-variance-authority-0.7.1.tgz) | [원문 사본](LICENSES/upstream/class-variance-authority-0.7.1.txt) | UI 의존 후보 |
| lucide-react | 1.41.0 | ISC + Feather 유래 아이콘 MIT | [공식 배포물](https://registry.npmjs.org/lucide-react/-/lucide-react-1.41.0.tgz) | [원문 사본](LICENSES/upstream/lucide-react-1.41.0.txt) | 인라인 SVG 원천 후보. Feather 파생 MIT 고지도 함께 보존 |
| tailwind-merge | 3.6.0 | MIT | [공식 배포물](https://registry.npmjs.org/tailwind-merge/-/tailwind-merge-3.6.0.tgz) | [원문 사본](LICENSES/upstream/tailwind-merge-3.6.0.txt) | cn 의존 후보 |
| clsx | 2.1.1 | MIT | [공식 배포물](https://registry.npmjs.org/clsx/-/clsx-2.1.1.tgz) | [원문 사본](LICENSES/upstream/clsx-2.1.1.txt) | cn 의존 후보 |
| tw-animate-css | 1.4.0 | MIT | [공식 배포물](https://registry.npmjs.org/tw-animate-css/-/tw-animate-css-1.4.0.tgz) | [원문 사본](LICENSES/upstream/tw-animate-css-1.4.0.txt) | 애니메이션 후보(T-201) |
| maplibre-gl | 5.24.0 | BSD-3-Clause | [공식 배포물](https://registry.npmjs.org/maplibre-gl/-/maplibre-gl-5.24.0.tgz) | [원문 사본](LICENSES/upstream/maplibre-gl-5.24.0.txt) | 버전 정합 대상. common 직접 의존·코드 배포 없음 |
| pretendard | 1.3.9 | OFL-1.1 | [공식 배포물](https://registry.npmjs.org/pretendard/-/pretendard-1.3.9.tgz) | [원문 사본](LICENSES/upstream/pretendard-1.3.9.txt) | 폰트 스택 이름만 참조. 폰트 파일 배포 없음 |
| @tanstack/react-table | 8.21.3 | MIT | [공식 배포물](https://registry.npmjs.org/@tanstack/react-table/-/react-table-8.21.3.tgz) | [원문 사본](LICENSES/upstream/tanstack-react-table-8.21.3.txt) | DataTable 후보 |
| @tanstack/react-virtual | 3.14.0 | MIT | [공식 배포물](https://registry.npmjs.org/@tanstack/react-virtual/-/react-virtual-3.14.0.tgz) | [원문 사본](LICENSES/upstream/tanstack-react-virtual-3.14.0.txt) | 가상화 후보 |
| zod | 4.5.0 | MIT | [공식 배포물](https://registry.npmjs.org/zod/-/zod-4.5.0.tgz) | [원문 사본](LICENSES/upstream/zod-4.5.0.txt) | 검증 후보(T-210) |

`class-variance-authority` 0.7.1의 배포물에는 `package/LICENSE`가 있고 NOTICE 파일은 없다. 동일 버전 [원천 트리 45462dd239546f570bca7821ab56bcef61feb900](https://github.com/joe-bell/cva/tree/45462dd239546f570bca7821ab56bcef61feb900)의 Git tree API `recursive=1` 결과도 `truncated=false`, NOTICE/NOTICE.txt/NOTICE.md 0개였다. 원천 LICENSE와 배포물 LICENSE를 보존하며, 상향 시 NOTICE 유무를 다시 확인한다.

`lucide-react` 원문은 ISC와 Feather MIT를 모두 포함하며 `maplibre-gl` 원문에는 MapLibre·Mapbox 등의 개별 고지가 함께 있다. 목록의 대표 SPDX 하나만 보고 나머지를 삭제하지 않는다. Pretendard 사본은 Reserved Font Name도 포함한다.

## 사본 유지와 배포

[LICENSES 안내](LICENSES/README.md)는 원문 확보·digest·참조용 SPDX 전문을 연결한다. 일반 MIT/ISC 전문의 자리표시자는 각 구성요소의 저작권 고지를 대신하지 않는다. 패키지를 실제로 만들 때 이 문서와 해당 `LICENSES/upstream/*` 사본을 함께 동봉하고 수령자가 상대 링크를 따라갈 수 있는지 tarball·wheel 설치 gate에서 확인한다(T-101·T-201·T-302).

common이 배포하지 않는 provider·지도 공유 라이브러리·외부 스킬 본문은 이식 고지 목록에 포함하지 않는다. 빌드 도구·peer라도 실제 번들에 코드가 포함되면 채택 task가 고지를 추가한다. 추출 허용 여부와 파일 헤더는 [licensing](docs/standards/licensing.md)이 정본이다.
