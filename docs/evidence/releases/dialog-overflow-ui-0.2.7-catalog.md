# Dialog·AlertDialog 넓은 본문 가로 넘침 UI 0.2.7의 main pack catalog 동결

## 고정 출처

- 제품 PR: [Common #88](https://github.com/digitie/kor-travel-common/pull/88)(`DialogContent`·`AlertDialogContent` grid 칸 하나를 `grid-cols-[minmax(0,1fr)]`로 명시 — 넓은 표가 좁은 화면에서 모달 칸을 넓혀 머리글·본문이 가로로 넘치던 결함)
- PR 최종 head: b3e2f35. 이 head의 PR CI 9개 job(docs·packages·tools ubuntu/windows·check-versions·secret-scan·frontend·recovery 3.11/3.13)이 모두 SUCCESS다(packages job radix smoke 94 passed/2 skipped, 새 `dialog-overflow-browser.spec.ts` 포함). 로컬 Docker(playwright v1.65.0-noble + node 26.13.1)에서 옛 클래스로 되돌리면 단위 1건·smoke 6건 FAIL(RED), 새 코드로 PASS(GREEN)함을 확인했다. 적대 리뷰 2인 P0/P1 없음, P2를 같은 PR에서 반영했다.
- main merge/pack source R: f159ef3ca2883fae6dd33f0d0d46dc2bf98032e1
- main push CI: [docs 45334069258](https://github.com/digitie/kor-travel-common/actions/runs/45334069258), [common frontend 45334069368](https://github.com/digitie/kor-travel-common/actions/runs/45334069368), [python-package 45334069268](https://github.com/digitie/kor-travel-common/actions/runs/45334069268) 모두 SUCCESS.
- main artifact 14894046767: common-release-packs-f159ef3ca2883fae6dd33f0d0d46dc2bf98032e1, ZIP 137714 bytes, digest sha256:14abf505d78b60e5c45e098ca798a8bc9821dffa1cd9161e7557a2aa7b68d7eb, 만료 2026-12-24T05:47:41Z. PR artifact나 로컬 재pack을 정본으로 쓰지 않았다.

## 원본 pack

artifact의 [SOURCE_SHA](dialog-overflow-ui-0.2.7/SOURCE_SHA)·[SHA256SUMS](dialog-overflow-ui-0.2.7/SHA256SUMS)·[SRI](dialog-overflow-ui-0.2.7/SRI)를 그대로 보존한다. tgz는 CI artifact에 있고 이 PR에서 재생성하지 않는다.

| 패키지 | 버전 | SHA256 |
| --- | --- | --- |
| @kor-travel/ui | 0.2.7 | 739e0e784e7df64500c354f13ebf52d95cf4b1a7ce6db2a17e325c4a57188ec0 |
| @kor-travel/tokens | 0.1.8 | 8784d5ab6f64a4763dbdd6542d0679bcf53a66f674f84364ffcc0b74a5884c0a |
| @kor-travel/toast | 0.1.7 | f37313506acb3193c056cbc3aefb50f1fed60d920ee13d91961aed6c949f0928 |

확인한 것: 내려받은 세 tgz의 `sha256sum -c SHA256SUMS` OK, 세 tgz의 sha512를 다시 계산해 SRI와 일치, SOURCE_SHA = R, ui `package/package.json`의 name·version과 peer `@kor-travel/tokens` 0.1.8, ui `dist/dialog.js`·`dist/alert-dialog.js`에 `grid grid-cols-[minmax(0,1fr)]`, tokens 0.1.8·toast 0.1.7 package version.

## catalog 동결

[frontend-artifacts.json](../../../frontend-artifacts.json)의 UI/tokens/toast 세 entry·candidate·sources.common/kor-travel-toast만 R bytes로 바꾼다. 상태 `CANDIDATE_NOT_RELEASED`, 다른 asset entry·출처, 버전축·package metadata/lock·정책은 그대로다. 소비자는 이 catalog를 포함한 main commit을 `common-ref`로 고정하고 version·filename·integrity를 그대로 옮긴다.

소비자 편집·빌드·배포는 이 PR 범위 밖이다(각 저장소의 이관 PR, R4 작업 뒤).
