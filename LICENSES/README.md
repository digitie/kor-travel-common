# 라이선스 원문 사본

T-003에서 2026-09-07 확보했다. 원문을 번역·수정하지 않았으며 파일별 출처·버전/커밋·tarball 내부 경로·SHA-256은 [sources.json](sources.json)에 기록했다. 이 JSON은 확보 evidence이며 제품 의존 버전 레지스트리가 아니다.

- [GPL-3.0-or-later](GPL-3.0-or-later.txt), [MIT](MIT.txt), [Apache-2.0](Apache-2.0.txt), [ISC](ISC.txt), [BSD-3-Clause](BSD-3-Clause.txt), [OFL-1.1](OFL-1.1.txt)은 SPDX license-list-data v3.26.0, commit `8a04f0303d95c4f932210b118588c662665bd383`의 참조용 전문이다.
- 실제 저작권자·연도·복합 고지·Reserved Font Name은 `upstream/`의 프로젝트별 사본에 보존한다. 대응 관계와 현재 도입 상태는 [서드파티 목록](../THIRD_PARTY_NOTICES.md)을 따른다.
- npm 공식 버전 tarball은 registry integrity의 알고리즘과 base64 digest를 대조한 뒤 라이선스 멤버만 읽었다. tarball과 실행 코드는 저장소에 넣지 않았다. canview·geo는 고정 Git object의 LICENSE를 읽었다.
- 사본과 원본의 바이트는 동일하다. 재확보 시 원천 URL과 digest를 함께 갱신하고 실제 채택 버전과 일치하는지 리뷰한다. 검증된 과거 버전 고지를 미래 버전에 자동 재사용하지 않는다.
- 일부 원문에 후행 공백이 있어 `.gitattributes`·`.editorconfig`는 이 디렉터리의 txt 사본만 공백 정리를 제외한다. 원문의 바이트와 digest를 보존하기 위한 예외이며 다른 파일의 공백 검사는 유지한다.

로컬 사본 무결성 확인(Python 3.11+, 저장소 루트):

```bash
python3 -B -X utf8 -c 'import hashlib,json,pathlib; rows=json.loads(pathlib.Path("LICENSES/sources.json").read_text())["files"]; assert rows; bad=[r["file"] for r in rows if hashlib.sha256(pathlib.Path(r["file"]).read_bytes()).hexdigest()!=r["sha256"]]; print("사본",len(rows),"불일치",bad); raise SystemExit(bool(bad))'
```
