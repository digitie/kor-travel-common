# 연결 gzip 검사 수정의 원 A 재확인

동일 원 reviewer A Mill이 f8643d5 scanner와 d1fe 문서 snapshot에서 A-P2-10 FIXED·scanner delta PASS·신규0을 확인했다. 원 반례와 focused9의 수정 전16실패 subcase, 수정 후9 PASS 및 전체391실행(390 PASS/1 SKIP)을 직접 재검증했다. 단일 완결 gzip만 지원하며 후행 stream/padding·CRC/ISIZE/FHCRC/trailer와 확장량 경계를 거부한다.

당시 d1fe의 공개 compiler 상수 인용 문서1건과 새 CI는 별도 gate로 남겼다. 이후 부모4479073에서 B의 publication 사본을 명시해 전체 secret/prod0·정확 예외32/4, 문서819/링크3138오류0을 확인했다. 현재447 정확CI와 후속 Radix 원본 수정·소비자 최종 수용은 별도다. 당시 raw를 뒤늦은 성공으로 덮어쓰지 않는다.

- [원 A 재확인](evidence/2026-11-11-review-A-common-gzip-postfix-5.md): SHA256 d907177b6ddcbc599d4fc9ee641ca7ac370cf48d84a8e3f44ac0a17b67c8b65f

원 B Epicurus도 두 파일의 한정 delta를 독립 PASS·신규0으로 확인했다. focused scanner62 PASS와 자체 연결 metadata 공격을 직접 실행했다. [B 한정 원문](evidence/2026-11-11-review-B-common-gzip-f864-delta.md): SHA256 eff85aabe699edfb58e47addf9dc7fcd9e75cb80cd5d13a9a973d11c316d9a8c. 이후 exact447 docs6개 job 모두 SUCCESS를 부모가 직접 조회했다. 이는 후속 후보10의 새 정책·Scope engine을 승인한 판정이 아니다.
