# 선택 칸 터치 영역·아코디언 포커스·Dialog 긴 제목 UI 0.2.6의 main pack catalog 동결

## 고정 출처

- 제품 PR: [Common #83](https://github.com/digitie/kor-travel-common/pull/83)(VirtualTable md 미만 선택 칸 44×44px로 체크박스 터치 영역이 이웃 행·칸과 겹치지 않음, AccordionContent `overflow: clip` + clip-margin 4px로 안쪽 포커스 outline 보임, Dialog 닫기 버튼이 있을 때 제목 `pr-7`·`wrap-anywhere`)
- PR 최종 head: 4248b03. 이 head의 PR CI 9개 job(docs·packages·tools ubuntu/windows·check-versions·secret-scan·frontend·recovery 3.11/3.13)이 모두 SUCCESS다. n150 gate에서 새 단위 시험·320/390/1440 smoke 브라우저 시험이 옛 `accordion.tsx`·`dialog.tsx`·`virtual-table.tsx`로 FAIL(RED), 새 코드로 PASS(GREEN)함을 확인했다. 독립 적대 리뷰 1회의 P1 2건·P2를 같은 PR에서 반영했다.
- main merge/pack source R: 05d7f91a4151a69d72b8bf1dc0007291c6ab2a61
- main push CI: [docs 45141922011](https://github.com/digitie/kor-travel-common/actions/runs/45141922011), [common frontend 45141922245](https://github.com/digitie/kor-travel-common/actions/runs/45141922245), [python-package 45141922005](https://github.com/digitie/kor-travel-common/actions/runs/45141922005) 모두 SUCCESS.
- main artifact 14803131043: common-release-packs-05d7f91a4151a69d72b8bf1dc0007291c6ab2a61, ZIP 137357 bytes, digest sha256:76ba4636db7cc2deeaff2ec059820981da0e4619597155eb345f70b5c93ca54a, 만료 2026-12-23T08:56:28Z. PR artifact나 로컬 재pack을 정본으로 쓰지 않았다.

## 원본 pack

artifact의 [SOURCE_SHA](touch-focus-ui-0.2.6/SOURCE_SHA)·[SHA256SUMS](touch-focus-ui-0.2.6/SHA256SUMS)·[SRI](touch-focus-ui-0.2.6/SRI)를 그대로 보존한다. tgz는 CI artifact에 있고 이 PR에서 재생성하지 않는다.

| 패키지 | 버전 | SHA256 |
| --- | --- | --- |
| @kor-travel/ui | 0.2.6 | 14e9853ceb720b6db4a173ee3411bb07e9d3d9c445c3f8bb45719499d4036110 |
| @kor-travel/tokens | 0.1.7 | a0422f551331e521cfdc819d1edd0bca0b90f33507a178ab2d8baea3256e8b53 |
| @kor-travel/toast | 0.1.6 | 62e7bdf09629369bdaf62c754421146659f5741f9201dfcbbdd225ca38c3e8c2 |

확인한 것: 내려받은 세 tgz의 `sha256sum -c SHA256SUMS` OK, SOURCE_SHA = R, ui `package/package.json`의 name·version과 peer `@kor-travel/tokens` 0.1.7, ui `dist/virtual-table.js`에 `max-md:h-11 max-md:w-11 max-md:min-w-11 max-md:p-0`, `dist/accordion.js`에 `overflow-clip`·`[overflow-clip-margin:4px]`, `dist/dialog.js`에 `pr-7`·`wrap-anywhere`.

## catalog 동결

[frontend-artifacts.json](../../../frontend-artifacts.json)의 UI/tokens/toast 세 entry·candidate·sources.common/kor-travel-toast만 R bytes로 바꾼다. 상태 `CANDIDATE_NOT_RELEASED`, 다른 asset entry·출처, 버전축·package metadata/lock·정책은 그대로다. 소비자는 이 catalog를 포함한 main commit을 `common-ref`로 고정하고 version·filename·integrity를 그대로 옮긴다.

소비자 편집·빌드·배포는 이 PR 범위 밖이다(각 저장소의 이관 PR, R4 작업 뒤).
