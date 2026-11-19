# 관리자 셸 UI 0.2.3의 main pack catalog 동결

## 고정 출처

- 제품 PR: [Common #70](https://github.com/digitie/kor-travel-common/pull/70)([T-222](../../tasks/T-222-admin-shell.md), [ADR-021](../../adr/021-admin-shell-left-drawer-and-single-top-bar.md))
- PR 최종 head: 225ddcd(브라우저 smoke 셀렉터 수정). 이 head의 PR CI 9개 job(docs·packages·tools ubuntu/windows·check-versions·secret-scan·frontend·recovery 3.11/3.13)이 모두 SUCCESS다. packages job의 Playwright 72건 PASS, 실패 0.
- main merge/pack source R: 0e2a3f5aa16323df0d009360802661c9bc496dc6
- main push CI: [docs 44459847805](https://github.com/digitie/kor-travel-common/actions/runs/44459847805), [common frontend 44459847788](https://github.com/digitie/kor-travel-common/actions/runs/44459847788), [python-package 44459847792](https://github.com/digitie/kor-travel-common/actions/runs/44459847792) 모두 SUCCESS.
- main artifact 14500111373: common-release-packs-0e2a3f5aa16323df0d009360802661c9bc496dc6, ZIP 135856 bytes, digest sha256:19881f2c3ed598ed7ec213c559be21ece2be77068bddee6de5bd249b6f8019e1, 만료 2026-12-19T04:45:14Z. PR artifact나 로컬 재pack을 정본으로 쓰지 않았다.

## 원본 pack

artifact의 [SOURCE_SHA](admin-shell-ui-0.2.3/SOURCE_SHA)·[SHA256SUMS](admin-shell-ui-0.2.3/SHA256SUMS)·[SRI](admin-shell-ui-0.2.3/SRI)를 그대로 보존한다. tgz는 CI artifact에 있고 이 PR에서 재생성하지 않는다.

| 패키지 | 버전 | SHA256 |
| --- | --- | --- |
| @kor-travel/ui | 0.2.3 | aa19793165ae37b2214d210692e23235545e1464c4e0059f99d943411fa753d9 |
| @kor-travel/tokens | 0.1.4 | 33d08d7b37c60d3e319da19608ce05137f6bf587dc8d42e3ce0dfb4b597a61fc |
| @kor-travel/toast | 0.1.3 | 34b514b270f88fc19c6b411b975d4497f91f3581530f32a39be264874ca09b37 |

확인한 것: 내려받은 세 tgz의 `sha256sum -c SHA256SUMS` OK, SOURCE_SHA = R, 각 tgz `package/package.json`의 name·version, ui의 peer `@kor-travel/tokens` 0.1.4, ui tarball 96개 항목에 `dist/admin-shell.{js,d.ts}`·LICENSE·NOTICE·THIRD_PARTY_NOTICES.md 포함, `dist/button-variants.js`에 `focus-visible:outline-kt-focus`가 있고 클래스 문자열에 `outline-none`·`transition-all`이 없음. 설치본 Next webpack·Turbopack build와 브라우저 smoke, tarball 설치 smoke는 main push docs run의 packages job이 같은 pack으로 실행했다. 별도의 로컬 minimal npm ci는 NOT_RUN(로컬 디스크 보호).

## catalog 동결

[frontend-artifacts.json](../../../frontend-artifacts.json)의 UI/tokens/toast 세 entry·candidate·sources.common/kor-travel-toast만 R bytes로 바꾼다. 상태 `CANDIDATE_NOT_RELEASED`, 다른 asset entry·출처, 버전축·package metadata/lock·정책은 그대로다. 소비자는 이 catalog를 포함한 main commit을 `common-ref`로 고정하고 version·filename·integrity를 그대로 옮긴다.

소비자 편집·빌드·배포는 이 PR 범위 밖이다(각 저장소의 이관 PR).
