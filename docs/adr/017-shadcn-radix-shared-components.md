# ADR-017: 공통 UI를 shadcn Radix와 TanStack VirtualTable로 통일한다

- 상태: accepted
- 날짜: 2026-11-11
- 결정자: 사용자

## 맥락

관리 UI가 Base UI·Radix·자체 overlay와 표를 각각 유지해 동작·의존성·산출물이 갈라졌다.

## 결정

공유 컴포넌트는 common shadcn/ui Radix로 통일한다. 표는 VirtualTable의 TanStack Table/Virtual 엔진을 사용한다. 이전 Base UI 선택을 해당 범위에서 대체한다. Zod·React Hook Form·Zustand·Pretendard와 ESLint10·React Doctor를 공통 적용하고, Pinvi 모바일도 NativeWind5 RC와 Tailwind4 공통 버전으로 이관한다. 지도는 maplibre-vworld-react GitHub 검증 커밋의 동일 산출물을 소비하고 범용 결함은 upstream에서 수정한다.

## 결과와 검증

버전 정본·산출물 원장·검사기로 drift를 실패시킨다. 대상은 Geo·Map·Weather·Concierge·Docker Manager·Pinvi·Transport다. 도메인/API·인증 저장소 소유 경계는 유지한다. 소비자 gate 완료 전 배포 수용으로 표시하지 않는다.
