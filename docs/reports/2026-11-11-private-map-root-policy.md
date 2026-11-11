# 옛 private 지도 root 재도입 차단

Geo의 node_modules/maplibre-vworld-react/packages/* Next alias 제거는 부모가 소유한다. 이 별도 정책 분기는 versions.json.frontendPolicy.forbidden에 maplibre-vworld-react를 추가하고 root/배포 policy를 재생성했다. 기존 직접 의존성 검사로 web/mobile의 직접 설치를 막는다.

기존 TypeScript import AST에도 같은 canonical forbidden 목록의 정확 package root 또는 root/ 하위 경로를 적용했다. 새 parser·별도 registry는 추가하지 않았다. 공개 core/web/RN 배포물이 정본이다.

회귀1개에서 web/mobile 직접 선언, root import, packages/web/src private import 거부와 유사하지만 다른 package 이름의 허용 경계를 확인했다. 전체 정책 Node41 PASS/skip0 및 영향 schema3 PASS를 [원본 로그](evidence/2026-11-11-native-css-fix4-policy/fix4-common-map-policy.log)에 보존했다. CSS pack/lock/원장 bytes와 지도 제품 코드는 바꾸지 않았다. 소비자 source alias 제거·webpack/build 검증은 부모가 수행한다.
