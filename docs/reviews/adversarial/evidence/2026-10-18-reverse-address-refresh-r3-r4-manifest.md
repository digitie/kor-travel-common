# 주소 갱신 r3·r4 불변 evidence

정식 범위는 Common PR39 전체이며 소비자 formal review와 운영 승인을 대체하지 않는다.
base c48595880aaad4367802ad71af2525a8a5e17c6a에서 r3 제품14115ba99ab5d72d4f381d25b2dca810b24914d6,
r4 제품c067a7f6a11b106931a73cd7465503d90e54d976을 Git object로 읽기 전용 검토했다.
작성자 미추적 검증 로그는 원본을 보존했고 review 기준에 포함하지 않았다.
A /root/review_finish_a는 신뢰 경계·실제 source 계약, B /root/review_finish_b는 DB·복구·누락 관점이다.
서로의 새 결과는 양쪽 최종 원문 확정 전 공개하지 않았다. 시작 정밀 시각은 사전 계측하지 않았으며
추정하지 않는다. 실제 관찰 hash·격리·종료 시각·실행 한계는 아래 원문에 있다.

| 실행 | 원문 | SHA256 |
| --- | --- | --- |
| r3 a | [2026-10-18-reverse-address-refresh-r3-reviewer-a.md](2026-10-18-reverse-address-refresh-r3-reviewer-a.md) | 431e8c192ee782abc5cae3228cb5969b852cecd1ddc925002360e081a7723806 |
| r3 b | [2026-10-18-reverse-address-refresh-r3-reviewer-b.md](2026-10-18-reverse-address-refresh-r3-reviewer-b.md) | 92fb8818a8bbb4b6dd9786c0c6226933fea7f3b9c48c75c1421e02ab4edb0f09 |
| r3 manifest | [2026-10-18-reverse-address-refresh-r3-manifest.json](2026-10-18-reverse-address-refresh-r3-manifest.json) | 90eb2c39add81093deee1cc4ff84a9bf4655a8c4852e6333a18bf00018a3047e |
| r4 a | [2026-10-18-reverse-address-refresh-r4-reviewer-a.md](2026-10-18-reverse-address-refresh-r4-reviewer-a.md) | 4e0844faf69451940284cff8e54b0fde3a098e06ea2d30970248bdd792fdbe6c |
| r4 b | [2026-10-18-reverse-address-refresh-r4-reviewer-b.md](2026-10-18-reverse-address-refresh-r4-reviewer-b.md) | e49c27d070cc6f8dd30a87ea19299534da25f819d1cdd59db7d089223138a6b3 |
| r4 manifest | [2026-10-18-reverse-address-refresh-r4-manifest.json](2026-10-18-reverse-address-refresh-r4-manifest.json) | 509036aca1b4d83ce190a42317cb007c3ca6515d3c7a225ae8151b89eb20659f |

원문은 byte 그대로 복사하고 SHA256을 대조했다. r3 BLOCK은 덮어쓰지 않고 보존한다.
전달 요청은 아래 reviewer가 대화의 NEW_TASK Payload를 그대로 보존한 별도 원문에 있다. 시작/수신 UTC 미수집은 그대로 남겼다.

- [a 전달 원문](2026-10-18-reverse-address-refresh-r3-r4-request-a.md) SHA256 baec296a867617c7b5d5fb30b4ac761ddc210d8e806728f1152d4d3c394df75a

- [b 전달 원문](2026-10-18-reverse-address-refresh-r3-r4-request-b.md) SHA256 5bd94da9557231dcb5024477ba630c241c045415209dfea92899876954225ee3
