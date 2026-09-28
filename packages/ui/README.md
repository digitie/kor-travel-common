# 공용 로그인·탐색 메뉴

React 19용 `@kor-travel/ui` 개발 후보다. 사용자 요청에 따른 [T-215](../../docs/tasks/T-215-shared-login-menu.md)의 최소 구현이며 T-201 전체 기반·T-214 릴리스 gate 완료를 뜻하지 않는다. 실제 채택 전에 [UI 계약](../../docs/standards/ui-contract.md)과 소비자별 React 업그레이드·라이선스·빌드 gate를 확인한다.

## 사용

소비자는 검증한 UI·tokens tarball을 설치한다. 소비자 Tailwind CSS 진입점에서 다음을 포함한다. `@source` 경로는 소비자 CSS 위치에 맞춘다.

```css
@import "tailwindcss";
@import "@kor-travel/tokens/theme.css";
@import "@kor-travel/tokens/base.css";
@source "../node_modules/@kor-travel/ui/dist";
```

인증·redirect는 소비자 콜백이다. `authenticate`는 앱이 구현하고 HTTP 상태를 `getLoginErrorMessage`로 매핑하거나 안전한 한국어 문구를 `error`에 전달한다. 콜백을 Promise로 반환하면 위젯이 기다리는 동안 중복 제출을 막는다.

```tsx
"use client";
import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { AppMenu, LoginForm } from "@kor-travel/ui";
import type { LoginCredentials } from "@kor-travel/ui";

export function Login({ authenticate }: {
  authenticate: (credentials: LoginCredentials) => Promise<void>;
}) {
  const router = useRouter();
  return <LoginForm brand="우리 서비스" nextPath="/admin" onSubmit={async ({ credentials, nextPath }) => {
    await authenticate(credentials);
    router.replace(nextPath);
  }} />;
}

export function Menu() {
  const pathname = usePathname();
  return <AppMenu pathname={pathname} linkComponent={Link} groups={[
    { id: "main", items: [{ id: "home", label: "홈", href: "/" }] },
  ]} />;
}
```

Next의 Server Component에서 콜백을 전달하지 않는다. 위 예처럼 Client Component에서 adapter를 구성한다. Next 의존은 소비자에만 있고 패키지는 서버 순수 함수 subpath(`navigation`, `login-messages`)도 제공한다. 인증 상태·권한은 서버에서 검증하며 `LoginStatus`나 메뉴 숨김은 접근 제어가 아니다.

## 예시·검증

[예시 안내](examples/README.md)의 여섯 프로젝트 데이터는 리모트 `main`의 고정 커밋에서 확인했다. 실제 앱 데이터·인증 서버는 연결하지 않는다. 최신 안정 기준과 실행 한계는 T-215 evidence를 따른다.

```bash
npm run build -w packages/ui
npm run check -w packages/ui
npm test -w packages/ui
npm pack -w packages/ui
```

`LoginForm`은 자체 `h2`를 제공하므로 앱의 페이지 `h1` 아래 배치한다. 메뉴 그룹·항목 ID는 각 배열에서 유일해야 하며 링크 항목 ID는 전체 메뉴에서 유일해야 한다. 앱이 권한에 맞게 필터링한 그룹을 넘긴다. hash/query 라우팅은 `activeItemId`로 판정하며 `null`은 모든 활성 표시를 끈다.
