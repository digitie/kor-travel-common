// SPDX-License-Identifier: GPL-3.0-or-later
// SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
import test from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { Toast } from "../index.js";
import { Toast as RadixToast } from "radix-ui";

test("공개 Toast namespace와 모든 primitive는 Radix 원본과 동일하다", () => {
  assert.strictEqual(Toast, RadixToast);
  for (const name of ["Provider", "Root", "Title", "Description", "Close", "Viewport", "Action"])
    assert.strictEqual(Toast[name], RadixToast[name]);
});

// toast는 빌드 단계가 없어 정책 사본을 자동 동기화하지 않는다. 지오처럼 toast의 checker를 쓰는 소비자는 이
// 사본으로 검사하므로, 루트 정본과 어긋나면 새 정책(예: vworld-map-web 1.0.4)을 거부한다.
const rootFile = name => new URL("../../../" + name, import.meta.url);
const json = url => JSON.parse(readFileSync(url, "utf8"));

test("배포 정책 사본은 루트 frontend-dependencies.json 정본과 바이트까지 같다", () => {
  assert.equal(readFileSync(new URL("../dependency-policy.json", import.meta.url), "utf8"),
    readFileSync(rootFile("frontend-dependencies.json"), "utf8"));
});

test("Toast 배포물에 제3자 고지 파일을 포함한다", () => {
  const manifest = json(new URL("../package.json", import.meta.url));
  const filename = "THIRD_PARTY_NOTICES.md";
  assert.ok(manifest.files.includes(filename));
  assert.match(readFileSync(new URL("../" + filename, import.meta.url), "utf8"), /Radix UI.*MIT/);
});

test("공통 패키지 metadata 버전은 versions.json 정확 축과 같다", () => {
  const axes = json(rootFile("versions.json")).axes;
  for (const [dir, name] of [["toast", "@kor-travel/toast"], ["ui", "@kor-travel/ui"], ["tokens", "@kor-travel/tokens"]]) {
    const manifest = json(rootFile("packages/" + dir + "/package.json"));
    assert.equal(manifest.name, name);
    assert.equal(manifest.version, axes[name].recommended, name + " metadata 버전과 정본 축 불일치");
  }
  // UI는 tokens를 정확 peer로 요구한다.
  assert.equal(json(rootFile("packages/ui/package.json")).peerDependencies["@kor-travel/tokens"],
    axes["@kor-travel/tokens"].recommended);
});
