# Common7·FocusScope2 최종 독립 검토와 머지

같은 불변 입력을 원 reviewer A/B가 각각 독립 검토했다. 구현자는 판정을 대신하지 않았고 상대 raw를 보지 않았다. Common7과 Scope2는 각각 두 PASS·신규0이다. 앱 최종 수용과 새 Manager SDK 검토·배포는 이 문서의 승인 범위 밖이며 계속 진행한다.

| 범위 | 원 A | 원 B | 최종 소스·결과 |
|---|---|---|---|
| Common7/C11 | [원문](evidence/2026-11-12-review-A-common-final-7.md) | [원문](evidence/2026-11-12-review-B-common-final-7.md) | source2d4579b·producer a354813·PR49 mergee8ed3ae |
| FocusScope2 | [원문](evidence/2026-11-12-review-A-radix-focus-scope-final-2.md) | [원문](evidence/2026-11-12-review-B-radix-focus-scope-final-2.md) | source1752a53·delivery01e8181·PR1 merge408bb40 |

[Common 불변 입력](evidence/2026-11-12-review-manifest-common-7.json), [Scope 불변 입력](evidence/2026-11-12-review-manifest-radix-focus-scope-2.json), [원문 SHA256 receipt](evidence/2026-11-12-common7-scope2-original-receipts.json)를 함께 보존한다. 입력 당시 pending은 그때의 관찰이며 원문을 고치지 않는다. 후속 exact CI는 각 원 reviewer가 직접 로그를 읽어 확인했다. B Scope2 원문 당시 Chromatic 진행 중 상태 이후 실제 SUCCESS를 별도로 관찰했다.

Common frontend43081533300·docs43081533139의6jobs·selftest43081533768·Python43081533181 모두 성공했다. 패키지 job의 실제 C11 tarball SHA512가 frozen 원장과 같고 packed65·Webpack/Turbopack이 통과했다. Doctor80파일0진단·정책175·UI101·tokens9·도구399 PASS/1 SKIP이다. 이전 C10의 Doctor3 warning 실패는 Set/Map helper로 실제 수정했으며 gate를 완화하지 않았다.

Scope 최종 delivery01e의 Build43080256232·집중43080256258·SSR43080255852·Chromatic43080255899 모두 성공했다. source38·source Storybook17·actual packed17은 별도 suite다. 원 A packed20, 원 B 실제 CJS/ESM 각각38도 원문의 실행 범위를 그대로 따른다. source175와 packet1ca0487, 전체 MIT·public API·provenance·고정 복사 recipe를 독립 검증했다. preferred producer와 delivery의 Git tree 경계를 구분한다.

[Common PR49](https://github.com/digitie/kor-travel-common/pull/49)와 [Radix fork PR1](https://github.com/digitie/radix-primitives/pull/1)을 merge 방식으로 머지했다. fetch한 target branch의 전체 tree가 reviewed commit과 각각 같았다. 공통 UI0.2.0·tokens0.1.1 및 Scope1.3.1+kortravel.fix.2의 공개된 bytes는 동결한다. 새 runtime·payload 변경에는 새 고유 버전을 사용한다.

원 Common6/Scope1 실패·조건부 판정 및 원 consumer1 BLOCK을 덮어쓰지 않는다. Geo43·Concierge50·Mapf55 원 A finding은 각 별도 source closure에서 FIXED를 확인했지만, 이 사실을 최종 모든 앱의 무조건 승인으로 확대하지 않는다.
