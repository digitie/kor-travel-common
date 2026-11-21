# TabsTrigger 포커스 UI 0.2.4의 main pack catalog 동결

## 고정 출처

- 제품 PR: [Common #79](https://github.com/digitie/kor-travel-common/pull/79)(TabsTrigger 포커스 FS-7.8·UX-G9.1 정합)
- PR 최종 head: a132a8b. 이 head의 PR CI 9개 job(docs·packages·tools ubuntu/windows·check-versions·secret-scan·frontend·recovery 3.11/3.13)이 모두 SUCCESS다. n150 gate에서 새 `tabs-focus.test.tsx`가 옛 0.2.3 `tabs.tsx`로 FAIL(RED), 새 코드로 PASS(GREEN)함을 확인했다.
- main merge/pack source R: 9691080c73d582f581c0c40fd5c300a70c34d326
- main push CI: [docs 44882394234](https://github.com/digitie/kor-travel-common/actions/runs/44882394234), [common frontend 44882394237](https://github.com/digitie/kor-travel-common/actions/runs/44882394237), [python-package 44882394226](https://github.com/digitie/kor-travel-common/actions/runs/44882394226) 모두 SUCCESS.
- main artifact 14698374408: common-release-packs-9691080c73d582f581c0c40fd5c300a70c34d326, ZIP 135928 bytes, digest sha256:cc29aa5effbbb987947282bb7d7efb2a5467a291946ba52d05dab84349f95be2, 만료 2026-12-21T07:58:57Z. PR artifact나 로컬 재pack을 정본으로 쓰지 않았다.

## 원본 pack

artifact의 [SOURCE_SHA](tabs-focus-ui-0.2.4/SOURCE_SHA)·[SHA256SUMS](tabs-focus-ui-0.2.4/SHA256SUMS)·[SRI](tabs-focus-ui-0.2.4/SRI)를 그대로 보존한다. tgz는 CI artifact에 있고 이 PR에서 재생성하지 않는다.

| 패키지 | 버전 | SHA256 |
| --- | --- | --- |
| @kor-travel/ui | 0.2.4 | 6f08e3ef781369de3ab0204c8d625b71b1d6496146b7033a95c39f7592de7799 |
| @kor-travel/tokens | 0.1.5 | cf14ba8cfa34a21e841c7727c89fbfa7fe9aab17ba5448f1a3c8c583c095078a |
| @kor-travel/toast | 0.1.4 | e1dd23b9d3d03babaae7fd97f655cc1b51a84e5c5bbdc98846b57f2404b08ce0 |

확인한 것: 내려받은 세 tgz의 `sha256sum -c SHA256SUMS` OK, SOURCE_SHA = R, 각 tgz `package/package.json`의 name·version, ui의 peer `@kor-travel/tokens` 0.1.5, ui `dist/tabs.js`의 focus-visible 클래스가 `outline-2`·`outline-offset-2`·`outline-kt-focus`뿐(TabsTrigger·TabsContent 각 1회)이고 `ring-[3px]`·`outline-1`·`border-ring`이 없음. 설치본 Next webpack·Turbopack build와 브라우저 smoke, tarball 설치 smoke는 main push docs run의 packages job이 같은 pack으로 실행했다.

## catalog 동결

[frontend-artifacts.json](../../../frontend-artifacts.json)의 UI/tokens/toast 세 entry·candidate·sources.common/kor-travel-toast만 R bytes로 바꾼다. 상태 `CANDIDATE_NOT_RELEASED`, 다른 asset entry·출처, 버전축·package metadata/lock·정책은 그대로다. 소비자는 이 catalog를 포함한 main commit을 `common-ref`로 고정하고 version·filename·integrity를 그대로 옮긴다.

소비자 편집·빌드·배포는 이 PR 범위 밖이다(각 저장소의 이관 PR).
