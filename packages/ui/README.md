# 공용 로그인·탐색 메뉴·관리자 셸

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

## 관리자 셸

관리자 화면은 `AdminShell`을 레이아웃에 한 번 둔다([ADR-021](../../docs/adr/021-admin-shell-left-drawer-and-single-top-bar.md)). lg(1024px) 이상은 좌측 rail(16rem, 아이콘 4rem 접힘), 그 아래는 한 줄 상단 바 왼쪽 메뉴 버튼으로 여는 좌측 drawer다. 페이지 제목은 상단 바의 `h1` "영역 - 페이지"이고 설명은 같은 줄에 작은 글씨로 말줄임한다. 앱 설명 문구는 넣지 않는다.

```tsx
// app/(admin)/layout.tsx
"use client";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { AdminShell, AppMenu } from "@kor-travel/ui";
import { NAV_GROUPS, pageLabel } from "@/lib/admin-pages"; // 앱 소유 nav 정본

export default function AdminLayout({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  return <AdminShell area="날씨" title={pageLabel(pathname)} brand="날씨" navigationKey={pathname}
    collapsedStorageKey="kor-travel-weather:sidebar-collapsed"
    railFooter={({ collapsed }) => <LogoutButton iconOnly={collapsed} />}
    menu={<AppMenu groups={NAV_GROUPS} pathname={pathname} linkComponent={Link} />}>
    {children}
  </AdminShell>;
}

// app/(admin)/weather/page.tsx 안의 client 컴포넌트
<AdminPageTitle title="날씨지도" description={`활성 위치 카탈로그 ${count}곳`} actions={<RefreshButton />} />
```

- `title`은 페이지 이름(또는 이미 합친 문자열), `area`는 서비스 영역이다. `formatAdminTitle(area, title)`로 document.title도 맞춘다.
- `navigationKey`가 바뀌거나 drawer 안 메뉴를 누르면 drawer가 닫히고 포커스가 `<main id="main-content">`로 간다.
- `AppMenu`는 셸 안에서 자동으로 세로 목록이 된다. 셸 밖 기존 사용은 그대로다.
- 지도처럼 화면 높이를 채우는 페이지는 `fillViewport`와 `mainClassName`으로 본문 스크롤을 직접 다룬다.
- 페이지마다 셸을 감싸는 앱은 `AdminShell`에 `title`·`description`·`actions`를 직접 줘도 된다.
- 모바일 폭(320px)에서 상단 바 `actions`는 아이콘 버튼 1~2개로 둔다. 많으면 본문 툴바로 옮긴다.
- 셸 안의 `AppMenu`에 `orientation`을 직접 주지 않는다(주면 셸의 세로·접힘 배치를 이긴다).
- drawer가 열려 있으면 rail의 메뉴도 DOM에 남으므로 `AppMenu testId`가 두 번 나온다. e2e는 `getByRole("dialog")` 안으로 범위를 좁힌다.
- drawer 움직임은 `@kor-travel/tokens/radix.css`(tw-animate·`data-open` variant)를 불러온 앱에서만 보인다. 없어도 동작은 같다.
- 저장된 접힘 상태는 hydration 뒤 적용되므로 첫 화면에서 rail 폭이 한 번 바뀔 수 있다.

## 예시·검증

`DagsterOperations`는 weather에서 추출한 운영 표시 컴포넌트다. `snapshot`, `onRefresh`,
`runUrl`, `scheduleUrl`을 주입하고 `jobLabel`·`locationUrl`·`loading`·`error`를 선택한다.
`@kor-travel/ui/dagster.css`와 tokens를 로드한다. `dagster-model` subpath는 React 없이
snapshot 타입·시간/주기/상태 표시 함수를 제공한다. 조회·인증·취소/재실행은 소비자 소유다.
실행 상한이 있는 run에는 `maxRuntimeSeconds`를 전달하여 긴 batch의 오탐을 방지한다.
기본 표시 시간대는 Asia/Seoul이다. URL callback은 앱이 검증한 내부 Dagster 링크만 반환한다.

[예시 안내](examples/README.md)의 여섯 프로젝트 데이터는 리모트 `main`의 고정 커밋에서 확인했다. 실제 앱 데이터·인증 서버는 연결하지 않는다. 최신 안정 기준과 실행 한계는 T-215 evidence를 따른다.

```bash
npm run build -w packages/ui
npm run check -w packages/ui
npm test -w packages/ui
npm pack -w packages/ui
```

`LoginForm`은 자체 `h2`를 제공하므로 앱의 페이지 `h1` 아래 배치한다. 메뉴 그룹·항목 ID는 각 배열에서 유일해야 하며 링크 항목 ID는 전체 메뉴에서 유일해야 한다. 앱이 권한에 맞게 필터링한 그룹을 넘긴다. hash/query 라우팅은 `activeItemId`로 판정하며 `null`은 모든 활성 표시를 끈다.
