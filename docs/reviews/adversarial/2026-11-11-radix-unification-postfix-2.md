# Radix 공통화 수정 후 독립 적대 리뷰2차

- review ID: 2026-11-11-radix-unification-2
- 종류: FULL 후속
- 기준: common8dad71a50f9f8f12f0e3ba1c913a93e404dabfed / VWorld9a7a348b02d61969b394c681b024d5851eef836b
- verdict: A CONDITIONAL / B CONDITIONAL
- 범위: 공통 UI·tokens·정책·원본 지도 배포물. 소비자 최종 수용·NativeCSS fork·배포는 별도.

동일 [불변 manifest2](evidence/2026-11-11-radix-unification-manifest-2.json)를 두 원 리뷰어에게 전달했다. [A 후속 원문](evidence/2026-11-11-radix-unification-reviewer-a-postfix-2.md)과 [B 후속 원문](evidence/2026-11-11-radix-unification-reviewer-b-postfix-2.md)은 byte 그대로 보존한다. 상대 결과는 각 원문 확정 전 공개하지 않았다. 최초 [리뷰1차](2026-11-11-radix-unification.md)와 그 원문도 그대로 남긴다.

## 원 리뷰어 closure와 새 finding

| 항목 | 원 리뷰어 확인 | 현재 상태 |
|---|---|---|
| 최초 A10건 | P1 두 건과 P2/P3를 포함해 모두 FIXED | 해당 불변 입력에서 closure 확정 |
| 최초 B11건 | P0 한 건·P1 일곱 건·P2 세 건 모두 FIXED | 해당 불변 입력에서 closure 확정 |
| A-P2-08 TableRow focus 색 전환 | 실제 Chromium에서 outline-color150ms 전환 재현 | OPEN, 후속 제품 수정·원 리뷰어 재확인 필요 |
| B2-P3-01 tokens 고지 문구 | MIT CSS 동봉 사실과 과거 무사본 설명 충돌 | OPEN, 후속 고지 수정·원 리뷰어 재확인 필요 |

A는 c7 자체 webpack/Turbopack·실제 Chromium·packed 지도 WebGL과 focus 회귀를 직접 확인했다. B는 c6 기존 브라우저 실측에 더해 설치본·c7 byte 동등성을 직접 확인했다. B의 브라우저 재실행은 자동 승인 검토에서 거부되어 실행하지 않았으며 A의 독립 실제 실행과 구분한다.

UI99·정책21·tokens9가 각각 독립 실행에서 통과했다. Python은340 PASS/1 SKIP이며 skip을 pass에 합산하지 않는다. 요약 manifest의 이전 tokens7 표기보다 원문 실측9가 정확하다.

## CI와 다음 gate

8dad exact-head의 frontend·workflow selftest·Python·문서·버전·secret·도구 검사는 성공했다. packages job130572322451은 Ubuntu apt 저장소 DNS 해석 실패로 Playwright 의존성 설치 단계에서 실패했고 실패 job만 재시도했다. 재시도 완료 결과를 확인하기 전에는 이 head의 전체 CI PASS로 집계하지 않는다.

후속 공통 정책·NativeCSS·focus/고지 수정은 새 불변 manifest에서 두 원 리뷰어가 재확인해야 한다. 이 보고서의 CONDITIONAL을 소비자 PR merge 또는 운영 배포 수용으로 확대하지 않는다.
