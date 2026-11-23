# 입력·선택 컨트롤 포커스 UI 0.2.5의 main pack catalog 동결

## 고정 출처

- 제품 PR: [Common #81](https://github.com/digitie/kor-travel-common/pull/81)(입력·선택·체크·스위치 등 포커스 FS-7.8·UX-G9.1 정합, 체크박스·스위치 md 미만 터치 영역 44px)
- PR 최종 head: 036584f. 이 head의 PR CI 9개 job(docs·packages·tools ubuntu/windows·check-versions·secret-scan·frontend·recovery 3.11/3.13)이 모두 SUCCESS다. n150 gate에서 새 `field-focus.test.tsx`가 옛 `input.tsx`·`checkbox.tsx`로 FAIL(RED), 새 코드로 PASS(GREEN)함을 확인했다. 독립 적대 리뷰 2인 P0/P1 없음, P2는 같은 PR에서 반영했다.
- main merge/pack source R: fe141143cc8ba75e8fd0b6134e1c9e518e294fa2
- main push CI: [docs 45095095376](https://github.com/digitie/kor-travel-common/actions/runs/45095095376), [common frontend 45095095455](https://github.com/digitie/kor-travel-common/actions/runs/45095095455), [python-package 45095095427](https://github.com/digitie/kor-travel-common/actions/runs/45095095427) 모두 SUCCESS.
- main artifact 14782962353: common-release-packs-fe141143cc8ba75e8fd0b6134e1c9e518e294fa2, ZIP 135986 bytes, digest sha256:065bfbdfed8a81c4538371d0515f2ff23cc5b67826f8d1f42a7db1431408ab72, 만료 2026-12-23T01:36:29Z. PR artifact나 로컬 재pack을 정본으로 쓰지 않았다.

## 원본 pack

artifact의 [SOURCE_SHA](field-focus-ui-0.2.5/SOURCE_SHA)·[SHA256SUMS](field-focus-ui-0.2.5/SHA256SUMS)·[SRI](field-focus-ui-0.2.5/SRI)를 그대로 보존한다. tgz는 CI artifact에 있고 이 PR에서 재생성하지 않는다.

| 패키지 | 버전 | SHA256 |
| --- | --- | --- |
| @kor-travel/ui | 0.2.5 | 6f365a12f966d1b33d06219e003c30bf15eedf965d100543f2b2e06acf67d2f1 |
| @kor-travel/tokens | 0.1.6 | 4a3256fa17f72ef3677b9c7e9489e8b27d566a3244b3dad1b3a672333a544be5 |
| @kor-travel/toast | 0.1.5 | efe0dc563eab02f69f07a679010b7cd4134aa5016b6d3263e21b168e8ab82e4f |

확인한 것: 내려받은 세 tgz의 `sha256sum -c SHA256SUMS` OK, SOURCE_SHA = R, ui `package/package.json`의 name·version과 peer `@kor-travel/tokens` 0.1.6, ui `dist/{input,textarea,native-select,select,checkbox,switch}.js`의 focus-visible 클래스가 `outline-2`·`outline-offset-2`·`outline-kt-focus`뿐이고 `focus-visible:ring`·`focus-visible:border-ring`이 없음(남은 ring은 의도적으로 유지한 `aria-invalid` 표시), `checkbox.js`에 `max-md:after:-inset-[15px]`, `switch.js`에 `max-md:after:-inset-y-4`.

## catalog 동결

[frontend-artifacts.json](../../../frontend-artifacts.json)의 UI/tokens/toast 세 entry·candidate·sources.common/kor-travel-toast만 R bytes로 바꾼다. 상태 `CANDIDATE_NOT_RELEASED`, 다른 asset entry·출처, 버전축·package metadata/lock·정책은 그대로다. 소비자는 이 catalog를 포함한 main commit을 `common-ref`로 고정하고 version·filename·integrity를 그대로 옮긴다.

소비자 편집·빌드·배포는 이 PR 범위 밖이다(각 저장소의 이관 PR, 첫 소비자는 concierge 모바일 UI 수정).
