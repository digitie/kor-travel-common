# NativeCSS 원본 수정의 두 독립 재검토 정산

대상은 Lightning748651c·serde18e53fc·수정 pack1.33.0+nativecss.fix.4다. 동봉 대응 source1e94372와 실제 Rust 입력이 같은 native/WASM 재사용, 새 JS 어댑터 재빌드를 구분한다. common과 앱의 구현·운영 수용을 대신하지 않는다.

| 원 리뷰어 | 원문 판정 | 본인 최초 finding 재확인 | 신규 finding |
|---|---|---|---|
| A Mill | 소스·pack 범위 PASS | A-P2-01 FIXED | 없음 |
| B Epicurus | Source PASS, 최종 CONDITIONAL | B-NATIVE-P1-01·B-NATIVE-P2-01·B-NATIVE-P2-02 FIXED | 없음 |

첫 리뷰의 조건부/차단 판정과 수정 후 원문, 같은 입력의 manifest1/2는 아래 파일에 byte 동일하게 보존한다. 두 원 리뷰어는 구현에 참여하지 않았고 상대 결과를 보지 않은 상태에서 본인 finding을 다시 검사했다. 위 표는 원 판정의 범위를 확장하지 않는다.

## 확인된 수정과 남은 gate

A는 실제 특수문자 경로4개·native/WASM 각각90개·IR8·원본 serde127개와 대응 source를 확인했다. B는 Windows fixture 복구, MIT 허가문, 현재 checkout/archive/binary 연결과 실제 source gate를 재검토했다. 정확 Lightning748의 source-gate·Ubuntu·Windows CI는 성공했다. macOS 최초 job은 대기 후 취소되었고 해당 job만 재실행을 요청했으며 아직 성공으로 집계하지 않는다.

실제 앱의 Android/iOS·웹·강제 WASM iOS export 이전 증거는 fix.3이다. 후보8에 fix.4를 설치한 소비자의 새 export·브라우저·CI와 각 PR 머지·새 배포는 별도 후속 gate다. 두 원문의 당시 queued 기록은 수정하지 않고 이후 원격 관찰과 구분한다.

## 원문과 해시

- [review-A-native-css-1.md](evidence/2026-11-11-review-A-native-css-1.md): SHA256 3b6e63edf13661700a71ed823ab05dbafd531083c960f31317ce1059ec626028
- [review-B-native-css-1.md](evidence/2026-11-11-review-B-native-css-1.md): SHA256 e077602b2bfec00c6d498112bc69c4918eded2227137db15b264634ed7bd16fe
- [review-manifest-native-css-1.json](evidence/2026-11-11-review-manifest-native-css-1.json): SHA256 89e7d4e49285e12c289ff124109450cdc1ba75f5a9d0c18ca97c75e726643203
- [review-A-native-css-postfix-2.md](evidence/2026-11-11-review-A-native-css-postfix-2.md): SHA256 95f938b907a4123abf6526581af421e25e1b1fafc8012b5b76ba1ddcd3bd7bb8
- [review-B-native-css-postfix-2.md](evidence/2026-11-11-review-B-native-css-postfix-2.md): SHA256 ef761c04ebc2a9610d2b8a5b6dc701fab4230caa7ce17c6371264290d21f0ae4
- [review-manifest-native-css-2.json](evidence/2026-11-11-review-manifest-native-css-2.json): SHA256 1215c43638009758821f3ec29bdce037513e5c01f6aa76d3839820802ef5428c

공통 후보8의 실제 동일 UI/tokens pack·브라우저65개 성공은 별도 [packages CI 관찰](evidence/2026-11-11-common-c8-packages-ci.json)이며 NativeCSS host 판정을 대신하지 않는다.

## 후속 원격 관찰 — 2026-11-12

serde18e는 PR1에서21d1c7로 merge했고 main tree 동일성을 확인했다. Lightning748의 macOS arm64 두 취소는 hosted runner 공급 부족이며, 동일 pack의 후속 CI35fc16b는 macOS15 Intel·Windows·Ubuntu·source-gate 모두 성공했다. 바뀐 것은 CI 호스트와 검증 metadata 분류이며 Rust/JS/binary/pack bytes는 같다. 이 후속 입력은 별도 manifest3로 두 원 리뷰어 재확인을 받으며 위 원문·당시 CONDITIONAL을 덮어쓰지 않는다.
