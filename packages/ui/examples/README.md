# 프로젝트별 로그인·메뉴 예시

사용자 요청에 따라 만든 확인용 페이지다. 각 프로젝트의 메뉴 라벨·순서·그룹·경로와 브랜드 색상을 공용 컴포넌트에 주입한다. 메뉴 선택과 로그인 성공/실패는 예시 상태만 바꾸며 실제 인증·세션·운영 API를 호출하지 않는다. 영문 메뉴 라벨은 소비자 원문을 유지한다.

## 리모트 기준

2026-09-29 GitHub 연결로 각 저장소의 최신 기본 브랜치 `main`을 조회하고 다음 커밋에 고정했다. 로컬 checkout의 메뉴는 사용하지 않는다. Geo는 [셸](https://github.com/digitie/kor-travel-geo/blob/b36c9d0ab9a708d7611ec29e65ea688053543d53/kor-travel-geo-ui/components/layout/AppShell.tsx)의 조회·진단 4개 + 관리 홈 + 기능 그룹을 합친다. 숨겨진 레거시 적재 route는 메뉴에 넣지 않는다. Docker Manager의 동작 버튼과 hash 링크도 원문 그대로 구분한다.

| 프로젝트 | 커밋 | 원천 |
|---|---|---|
| map | [f5d60f61](https://github.com/digitie/kor-travel-map/commit/f5d60f61f7634f9ede2aeb7b58912100cf10820b) | [메뉴](https://github.com/digitie/kor-travel-map/blob/f5d60f61f7634f9ede2aeb7b58912100cf10820b/packages/kor-travel-map-admin/frontend/src/components/admin-shell.tsx) · [색상](https://github.com/digitie/kor-travel-map/blob/f5d60f61f7634f9ede2aeb7b58912100cf10820b/packages/kor-travel-map-admin/frontend/src/app/globals.css) |
| weather | [fbb52e8a](https://github.com/digitie/kor-travel-weather/commit/fbb52e8a505113d80fcb77f2dfb7cb67350c59ef) | [메뉴](https://github.com/digitie/kor-travel-weather/blob/fbb52e8a505113d80fcb77f2dfb7cb67350c59ef/packages/kor-travel-weather-admin/frontend/components/admin-shell.tsx) · [색상](https://github.com/digitie/kor-travel-weather/blob/fbb52e8a505113d80fcb77f2dfb7cb67350c59ef/packages/kor-travel-weather-admin/frontend/app/tokens.css) |
| concierge | [ab23bf2a](https://github.com/digitie/kor-travel-concierge/commit/ab23bf2a85df61746a154ae89fc4530cb089c5da) | [메뉴](https://github.com/digitie/kor-travel-concierge/blob/ab23bf2a85df61746a154ae89fc4530cb089c5da/frontend/src/components/AppShell.tsx) · [색상](https://github.com/digitie/kor-travel-concierge/blob/ab23bf2a85df61746a154ae89fc4530cb089c5da/frontend/tokens.css) |
| geo | [b36c9d0a](https://github.com/digitie/kor-travel-geo/commit/b36c9d0ab9a708d7611ec29e65ea688053543d53) | [메뉴](https://github.com/digitie/kor-travel-geo/blob/b36c9d0ab9a708d7611ec29e65ea688053543d53/kor-travel-geo-ui/lib/admin-pages.ts) · [색상](https://github.com/digitie/kor-travel-geo/blob/b36c9d0ab9a708d7611ec29e65ea688053543d53/kor-travel-geo-ui/app/globals.css) |
| transport | [7960785b](https://github.com/digitie/kor-travel-transport/commit/7960785b78fc2177b2eff5488534591bc616d834) | [메뉴](https://github.com/digitie/kor-travel-transport/blob/7960785b78fc2177b2eff5488534591bc616d834/packages/kor-travel-transport-admin/frontend/components/admin-shell.tsx) · [색상](https://github.com/digitie/kor-travel-transport/blob/7960785b78fc2177b2eff5488534591bc616d834/packages/kor-travel-transport-admin/frontend/app/tokens.css) |
| docker-manager | [6af5dd14](https://github.com/digitie/kor-travel-docker-manager/commit/6af5dd147d8e697d4335e351f5d49df83bd325f6) | [메뉴](https://github.com/digitie/kor-travel-docker-manager/blob/6af5dd147d8e697d4335e351f5d49df83bd325f6/frontend/src/components/layout/AppShell.tsx) · [색상](https://github.com/digitie/kor-travel-docker-manager/blob/6af5dd147d8e697d4335e351f5d49df83bd325f6/frontend/tokens.css) |

`projects.json`은 위 원천에서 확인한 메뉴·색상 사실을 담는 예시 데이터이며 소비자의 코드·셸 구현을 이식하지 않는다. 공통 패키지 기본 메뉴나 토큰 정본으로 사용하지 않고 npm tarball에서도 제외한다. 아이콘은 예시의 별도 Lucide 개발 의존을 사용한다.

색상 대비를 위해 Concierge 입력 경계는 원천의 text-secondary `#5f6b63`, 어두운 rail 포커스는 원천 rail-muted `#c4b5fd`를 사용한다. Docker Manager CTA는 원천 brand-ink를 사용한다. 브랜드 계열은 보존하며 원천 색상 조합 자체의 완전한 동일성을 주장하지 않는다. 전체 셸·접힘·drawer는 소비자 소유이므로 여기서는 공용 메뉴의 strip/rail 동작을 보여 준다.

## 실행

`next-app`은 빌드된 공통 UI의 공개 export를 쓰는 최신 Next App Router 시각 예시다. 패키지 설치 계약은 별도 [smoke fixture](../smoke/next-app/package.json)가 검증한다.

```bash
npm ci
npm run build -w packages/ui
npm ci --prefix packages/ui/examples/next-app
npm run dev --prefix packages/ui/examples/next-app
```

주소의 `?project=map`, `weather`, `concierge`, `geo`, `transport`, `docker-manager`로 화면을 선택한다. 현재 설치·실행 여부와 버전은 [T-215 evidence](../../../docs/tasks/T-215-shared-login-menu.md)를 따른다. 최신 버전 기준의 fixture 정의를 최신 버전 빌드 성공으로 보지 않는다.

## 설치 산출물 스모크

```bash
mkdir -p test-results/ui-pack
npm pack -w packages/tokens --pack-destination test-results/ui-pack
npm pack -w packages/ui --pack-destination test-results/ui-pack
npm install --prefix packages/ui/smoke/next-app
npm run build:webpack --prefix packages/ui/smoke/next-app
npm run build --prefix packages/ui/smoke/next-app
```

이 fixture는 `src` 대신 tarball의 `@kor-travel/ui`·tokens를 설치하고 실제 `next/link`·`usePathname`을 사용한다. 소비자 저장소의 실제 build/e2e를 대체하지 않는다.

Geo 입력 경계도 원천의 text-secondary 색을 사용해 3:1 비텍스트 대비를 확보한다. axe의 텍스트 대비 검사와 입력 경계 대비 실측은 별개로 검증한다.
