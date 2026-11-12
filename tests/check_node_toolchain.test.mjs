// SPDX-License-Identifier: GPL-3.0-or-later
// SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
import { test } from "node:test";
import assert from "node:assert/strict";
import { mkdtempSync, mkdirSync, writeFileSync, rmSync, symlinkSync, cpSync } from "node:fs";
import { tmpdir } from "node:os";
import { dirname, join, resolve } from "node:path";
import { spawnSync } from "node:child_process";
import { fileURLToPath, pathToFileURL } from "node:url";
import { checkToolchain } from "../tools/check_node_toolchain.mjs";

const node = "22.23.1", npm = "12.0.1", digest = "a".repeat(64);
const checker = resolve(dirname(fileURLToPath(import.meta.url)), "../tools/check_node_toolchain.mjs");
function fixture(t) {
  const root = mkdtempSync(join(tmpdir(), "kt-node-toolchain-"));
  t.after(() => rmSync(root, { recursive: true, force: true }));
  function put(name, data) {
    const path = join(root, name); mkdirSync(dirname(path), { recursive: true });
    writeFileSync(path, typeof data === "string" ? data : JSON.stringify(data));
  }
  const manifest = { private: true, packageManager: "npm@" + npm, engines: { node, npm } };
  put("package.json", manifest); put(".nvmrc", node + "\n"); put(".npmrc", "engine-strict=true\n");
  put("versions.json", { axes: { node: { recommended: node }, npm: { recommended: npm } } });
  const options = { root, registry: join(root, "versions.json") };
  return { root, put, manifest, options, run: extra => checkToolchain({ ...options, ...extra }) };
}
function reject(result, text) { assert.equal(result.ok, false); assert.match(result.errors.join("\n"), text); }

test("private root의 정합한 선언과 실제 npm run 식별을 수용한다", t => {
  const f = fixture(t);
  assert.equal(f.run({ runtime: true, nodeVersion: node, npmAgent: `npm/${npm} node/v${node} linux x64` }).ok, true);
});
for (const [field, value] of [["private", false], ["packageManager", "npm@11.19.1"], ["engines", { node: "^22.23.1", npm }]]) {
  test(`root ${field} 오류는 실패한다`, t => {
    const f = fixture(t); f.put("package.json", { ...f.manifest, [field]: value }); reject(f.run(), /private|packageManager|engines/u);
  });
}
for (const value of ["engine-strict=false\n", "engine-strict=true\nengine-strict=false\n", "engine-strict=yes\n", "# engine-strict=true\n"]) {
  test(`engine-strict 비활성 입력 ${JSON.stringify(value)} 거부`, t => {
    const f = fixture(t); f.put(".npmrc", value); reject(f.run(), /engine-strict/u);
  });
}
test("기존 npmrc 설정과 주석을 보존하며 마지막 strict 설정을 읽는다", t => {
  const f = fixture(t); f.put(".npmrc", "fund=false\nengine-strict=false\nengine-strict = true # 적용\n"); assert.equal(f.run().ok, true);
});
test("추가 selector가 정본과 다르면 실패한다", t => {
  const f = fixture(t); f.put(".node-version", "24.15.0\n"); reject(f.run(), /node-version/u);
});
test("workspace 멤버는 private root를 상속하고 공개 library engines는 강제하지 않는다", t => {
  const f = fixture(t); f.put("package.json", { ...f.manifest, workspaces: ["apps/*", "packages/*"] });
  f.put("apps/web/package.json", { private: true });
  f.put("packages/ui/package.json", { name: "@fixture/ui", engines: { node: ">=20" } });
  const result = f.run({ manifests: ["apps/web/package.json", "packages/ui/package.json"] });
  assert.equal(result.ok, true); assert.equal(result.anchors, 1);
});
test("workspace에서 제외된 앱의 별도 anchor도 검사한다", t => {
  const f = fixture(t); f.put("package.json", { ...f.manifest, workspaces: { packages: ["apps/*", "!apps/extra"] } });
  f.put("apps/extra/package.json", { private: true });
  reject(f.run({ manifests: ["apps/extra/package.json"] }), /packageManager|파일/u);
  f.put("apps/extra/package.json", f.manifest); f.put("apps/extra/.npmrc", "engine-strict=true");
  assert.equal(f.run({ manifests: ["apps/extra/package.json"] }).ok, true);
});
test("workspace 자신의 packageManager 불일치도 거부한다", t => {
  const f = fixture(t); f.put("package.json", { ...f.manifest, workspaces: ["apps/*"] });
  f.put("apps/web/package.json", { packageManager: "npm@11.19.1" });
  reject(f.run({ manifests: ["apps/web/package.json"] }), /packageManager/u);
});
for (const extra of [{ manifests: null }, { dockerfiles: null }, { manifests: [] }, { manifests: "package.json" }, { manifests: [null] }, { dockerfiles: "Dockerfile" }, { dockerfiles: [42] }]) {
  test(`목록의 잘못된 타입·빈 manifest 거부 ${JSON.stringify(extra)}`, t => reject(fixture(t).run(extra), /배열/u));
}
for (const path of ["../package.json", "/tmp/package.json", "apps/../../package.json", "C:\\outside\\package.json", "apps\\web\\package.json"]) {
  test(`저장소 경로 경계 ${JSON.stringify(path)} 거부`, t => reject(fixture(t).run({ manifests: [path] }), /경로/u));
}
test("최종 파일과 중간 디렉터리 symlink를 통한 외부 접근은 거부한다", t => {
  const f = fixture(t), other = fixture(t); other.put("package.json", f.manifest);
  try {
    symlinkSync(join(other.root, "package.json"), join(f.root, "linked.json"));
    symlinkSync(other.root, join(f.root, "linked-dir"), "dir");
  } catch (error) {
    if (process.platform === "win32" && ["EPERM", "EACCES", "ENOSYS"].includes(error.code)) {
      throw new Error("NOT_RUN: Windows symlink 권한·기능 부족으로 경계 검증을 실행하지 못했습니다", { cause: error });
    }
    throw error;
  }
  for (const name of ["linked.json", "linked-dir/package.json"]) reject(f.run({ manifests: [name] }), /밖|일반/u);
});
test("Docker의 전역 ARG·platform·stage 별칭과 다른 runtime 이미지를 수용한다", t => {
  const f = fixture(t);
  f.put("Dockerfile", `ARG NODE_VERSION=${node}\nFROM --platform=$BUILDPLATFORM node:${node}-bookworm-slim@sha256:${digest} AS deps\nFROM deps AS build\nFROM nginx:1.29-alpine\n`);
  const r = f.run({ dockerfiles: ["Dockerfile"] }); assert.equal(r.ok, true); assert.equal(r.checkedNodeImages, 1);
  f.put("Dockerfile", `ARG BASE=node:${node}-alpine@sha256:${digest}\nFROM $BASE AS build\nFROM build\n`);
  assert.equal(f.run({ dockerfiles: ["Dockerfile"] }).ok, true);
});
for (const image of [`node:22-alpine@sha256:${digest}`, `node:${node}-alpine`, `node:24.15.0-alpine@sha256:${digest}`, `mirror.example:5000/library/node:${node}@sha256:${digest}`]) {
  test(`정확 버전·digest 또는 지원 이미지 형식 위반 거부 ${image.split("@")[0]}`, t => {
    const f = fixture(t); f.put("Dockerfile", `FROM node:${node}-slim@sha256:${digest} AS build\nFROM ${image}\n`);
    reject(f.run({ dockerfiles: ["Dockerfile"] }), /Node 이미지/u);
  });
}
test("stage 내부 ARG가 다음 FROM의 전역 기본값을 덮지 않는다", t => {
  const f = fixture(t);
  f.put("Dockerfile", `ARG BASE=node:22-alpine@sha256:${digest}\nFROM node:${node}-slim@sha256:${digest} AS build\nARG BASE=node:${node}-alpine@sha256:${digest}\nFROM $BASE\n`);
  reject(f.run({ dockerfiles: ["Dockerfile"] }), /Node 이미지/u);
});
test("동적 이미지·Node 없는 파일·깨진 FROM은 검증된 것으로 세지 않는다", t => {
  const f = fixture(t);
  for (const content of ["FROM ${UNKNOWN}\n", "FROM nginx:1.29\n", `FROM node:${node}-slim@sha256:${digest}\nFROM \\\n  $UNKNOWN\n`]) {
    f.put("Dockerfile", content); assert.equal(f.run({ dockerfiles: ["Dockerfile"] }).ok, false);
  }
});
test("실행 버전과 npm 식별은 선언과 별개로 검사한다", t => {
  const f = fixture(t);
  reject(f.run({ runtime: true, nodeVersion: "22.22.2", npmAgent: `npm/${npm}` }), /실행 Node/u);
  for (const npmAgent of ["", "npm/12.0.10", "yarn/12.0.1", "npm/11.19.1"]) reject(f.run({ runtime: true, nodeVersion: node, npmAgent }), /실행 npm/u);
});
test("live registry의 새 권고값을 사용하며 범위 권고는 거부한다", t => {
  const f = fixture(t);
  f.put("versions.json", { axes: { node: { recommended: "22.24.0" }, npm: { recommended: npm } } }); reject(f.run(), /불일치/u);
  f.put("versions.json", { axes: { node: { recommended: "^22.23.1" }, npm: { recommended: npm } } }); reject(f.run(), /세 자리/u);
});
test("CLI 추가 JSON 입력의 타입·경계를 검사하고 성공/실패 exit을 구분한다", t => {
  const f = fixture(t);
  function cli(args) { return spawnSync(process.execPath, [checker, "--root", f.root, "--registry", f.options.registry, ...args], { encoding: "utf8" }); }
  assert.equal(cli([]).status, 0);
  for (const value of ["not-json", "{}", '["package.json",null]']) assert.equal(cli(["--manifests", value]).status, 2);
  assert.equal(cli(["--manifests", '["../package.json"]']).status, 1);
  assert.equal(cli(["--dockerfiles", '"Dockerfile"']).status, 2);
});


test("전역 npm pin은 stage 상속 시만 유지하고 새로운 Node FROM은 상속하지 않는다", t => {
  const f = fixture(t);
  const base = `FROM node:${node}-alpine@sha256:${digest} AS deps\nRUN npm install --global npm@${npm} && npm ci --engine-strict\nFROM deps AS build\nRUN npm run build\n`;
  f.put("Dockerfile", base + `FROM node:${node}-alpine@sha256:${digest}\nCMD ["npm","run","start"]\n`);
  reject(f.run({ dockerfiles: ["Dockerfile"] }), /fresh Node stage/u);
  f.put("Dockerfile", base + `FROM node:${node}-alpine@sha256:${digest}\nRUN npm install -g npm@${npm}\nCMD ["npm","run","start"]\n`);
  assert.equal(f.run({ dockerfiles: ["Dockerfile"] }).ok, true);
});
test("단일 npx npm ci는 이후 bare npm을 선택하지 않는다", t => {
  const f = fixture(t);
  const base = `FROM node:${node}-slim@sha256:${digest}\nRUN npx --yes npm@${npm} ci --engine-strict\n`;
  f.put("Dockerfile", base + "RUN npm run build\n"); reject(f.run({ dockerfiles: ["Dockerfile"] }), /fresh Node stage/u);
  f.put("Dockerfile", base + `RUN npx --yes npm@${npm} --workspace apps/web run build\n`);
  assert.equal(f.run({ dockerfiles: ["Dockerfile"] }).ok, true);
});
for (const command of ["CMD [\"npx\",\"next\",\"start\"]", "RUN npm install --global npm@11.19.1", "RUN npx --yes npm@11.19.1 ci --engine-strict", "RUN npm install --global \"$(node -p 'require(\"./package.json\").packageManager')\""]) {
  test(`미선택 runtime·다른 npm·미지원 동적 선택을 거부 ${command}`, t => {
    const f = fixture(t); f.put("Dockerfile", `FROM node:${node}-slim@sha256:${digest}\n${command}\n`);
    reject(f.run({ dockerfiles: ["Dockerfile"] }), /npm|shell/u);
  });
}
test("pin 뒤 npm ci도 명시 strict flag가 필요하며 node 전용 runtime은 허용한다", t => {
  const f = fixture(t);
  f.put("Dockerfile", `FROM node:${node}-alpine@sha256:${digest}\nRUN npm install -g npm@${npm} && npm ci\n`);
  reject(f.run({ dockerfiles: ["Dockerfile"] }), /engine-strict/u);
  f.put("Dockerfile", `FROM node:${node}-slim@sha256:${digest}\nCMD ["node","server.js"]\n`);
  assert.equal(f.run({ dockerfiles: ["Dockerfile"] }).ok, true);
});

test("주석 끝의 역슬래시가 다음 Node FROM 검사를 숨기지 않는다", t => {
  const f = fixture(t);
  f.put("Dockerfile", `FROM node:${node}-slim@sha256:${digest} AS build\n# 주석 \\\nFROM node:22-alpine@sha256:${digest}\n`);
  reject(f.run({ dockerfiles: ["Dockerfile"] }), /Node 이미지/u);
});

test("Pinvi fresh runtime의 npx next는 pin 전 실패·명시 전역 pin 후 성공한다", t => {
  const f = fixture(t), from = `FROM node:${node}-bookworm-slim@sha256:${digest}\n`;
  const cmd = 'CMD ["npx","next","start","-p","3000"]\n';
  f.put("Dockerfile", from + cmd); reject(f.run({ dockerfiles: ["Dockerfile"] }), /fresh Node stage/u);
  f.put("Dockerfile", from + `RUN npm install --global npm@${npm}\n` + cmd);
  assert.equal(f.run({ dockerfiles: ["Dockerfile"] }).ok, true);
});

for (const flags of [["--force", "--force=true", "--force=false", "-f"], ["--legacy-peer-deps", "--legacy-peer-deps=true", "--legacy-peer-deps=false"]]) {
  test(`명시 strict 뒤 우회 옵션을 거부 ${flags[0]}`, t => {
    const f = fixture(t);
    for (const flag of flags) {
      f.put("Dockerfile", `FROM node:${node}-slim@sha256:${digest}\nRUN npm install --global npm@${npm}\nRUN npm ci --engine-strict ${flag}\n`);
      reject(f.run({ dockerfiles: ["Dockerfile"] }), /우회 옵션/u);
    }
  });
}


const attackFrom = `FROM node:${node}-alpine@sha256:${digest} AS deps\n`;
const attackPin = `RUN npm install --global npm@${npm}\n`;
for (const [name, docker, npmrc] of [
  ["A-COMMON-P2-01 force 설정", null, "engine-strict=true\nforce=true\n"],
  ["A-COMMON-P2-02 strict false", attackFrom + attackPin + "RUN npm ci --engine-strict --engine-strict=false\n"],
  ["A-COMMON-P2-02 strict 부정", attackFrom + attackPin + "RUN npm ci --engine-strict --no-engine-strict\n"],
  ["A-COMMON-P2-03 heredoc", attackFrom + "RUN <<EOF\nnpm install --global npm@11.19.1\nnpm ci --force\nEOF\n"],
  ["A-COMMON-P2-03 backtick escape", "# escape=`\n" + attackFrom + `FROM \x60\nnode:24.15.0-alpine@sha256:${digest}\n`],
  ["A-COMMON-P2-04 location 재선택", attackFrom + attackPin + "RUN npm install --location=global npm@11.19.1\nRUN npm ci --engine-strict\n"],
  ["A-COMMON-P2-04 npx package 재선택", attackFrom + attackPin + "RUN npx --yes --package=npm@11.19.1 npm ci --engine-strict\n"],
]) {
  test(name, t => {
    const f = fixture(t);
    if (npmrc) f.put(".npmrc", npmrc);
    if (docker !== null) f.put("Dockerfile", docker);
    assert.equal(f.run({ dockerfiles: docker === null ? [] : ["Dockerfile"] }).ok, false);
  });
}


test("force 유효 마지막 값을 읽고 무관한 peer·lifecycle 설정은 보존한다", t => {
  const f = fixture(t);
  for (const rc of [
    "engine-strict=true\nforce=true\nforce=false\n",
    'engine-strict=true\nforce="false"\nlegacy-peer-deps=true\nignore-scripts=true\nfund=false\n',
  ]) { f.put(".npmrc", rc); assert.equal(f.run().ok, true); }
  for (const rc of ["engine-strict=true\nforce=false\nforce=true\n", 'engine-strict=true\nforce="true"\n', "engine-strict=true\nforce\n", "engine-strict=true\nforce=${UNKNOWN}\n"]) {
    f.put(".npmrc", rc); reject(f.run(), /force=false/u);
  }
});
for (const exec of [false, true]) {
  test(`strict 해제·분리 false·중복 해제는 ${exec ? "exec JSON" : "shell"} 모두 거부한다`, t => {
    const f = fixture(t);
    for (const flags of [
      ["--engine-strict", "--engine-strict=false"], ["--engine-strict", "--no-engine-strict"],
      ["--engine-strict", "false"], ["--engine-strict=true", "--engine-strict", "false"],
      ["--engine-strict", "--no-engine-strict=false"], ["--engine-strict", ""], ["--engine-stric=false"],
    ]) {
      const argv = ["npm", "ci", ...flags];
      const command = exec ? JSON.stringify(argv) : argv.map(word => word || "''").join(" ");
      f.put("Dockerfile", attackFrom + attackPin + "RUN " + command + "\n");
      assert.equal(f.run({ dockerfiles: ["Dockerfile"] }).ok, false, JSON.stringify(flags));
    }
  });
}
test("명시 true 동등 표기와 실제 앱 명령의 stage·전달 인수는 수용한다", t => {
  const f = fixture(t);
  for (const flags of ["--engine-strict", "--engine-strict=true", "--engine-strict true", "--engine-strict --engine-strict=true"]) {
    f.put("Dockerfile", attackFrom + attackPin + `RUN npm ci ${flags} --ignore-scripts --no-audit --no-fund\nFROM deps AS build\nRUN npm run build\nCMD ["npm","run","start","--","--hostname","0.0.0.0","--port","12305"]\n`);
    assert.equal(f.run({ dockerfiles: ["Dockerfile"] }).ok, true, flags);
  }
  f.put("Dockerfile", attackFrom + `RUN npx --yes npm@${npm} ci --engine-strict\nRUN npx --yes npm@${npm} --workspace apps/web run build\n`);
  assert.equal(f.run({ dockerfiles: ["Dockerfile"] }).ok, true);
});
test("전역 pin 뒤에도 package·exec·prefix·global selector alias는 거부한다", t => {
  const f = fixture(t);
  for (const command of [
    "npx -p npm@11.19.1 npm ci --engine-strict", "npx --package npm@11.19.1 npm ci --engine-strict",
    "npx --yes --package=npm@11.19.1 npm ci --engine-strict", "npx npm ci --engine-strict",
    "npm exec --package=npm@11.19.1 -- npm ci --engine-strict", "npm x -- npm ci --engine-strict",
    "npm --global install npm@11.19.1", "npm -g install npm@11.19.1", "npm --prefix /tmp/else ci --engine-strict",
    "npm ci --engine-strict --prefix=/tmp/else", "npm ci --engine-strict --userconfig=/tmp/else",
    "npm install --location global npm@11.19.1", "npm ci --engine-strict --loc=global",
  ]) {
    f.put("Dockerfile", attackFrom + attackPin + "RUN " + command + "\n");
    assert.equal(f.run({ dockerfiles: ["Dockerfile"] }).ok, false, command);
  }
});
test("미지원 heredoc·escape를 거부하고 기본 backslash 지시문은 수용한다", t => {
  const f = fixture(t);
  for (const text of [attackFrom + "RUN \\\n <<EOF\nnpm ci\nEOF\n", attackFrom + "RUN <<-EOF\nnpm ci\nEOF\n", attackFrom + "COPY <<EOF /tmp/file\nhello\nEOF\n", "# ESCAPE=`\n" + attackFrom, "# escape=unknown\n" + attackFrom]) {
    f.put("Dockerfile", text); assert.equal(f.run({ dockerfiles: ["Dockerfile"] }).ok, false);
  }
  f.put("Dockerfile", "# escape=\\\n" + attackFrom + attackPin + "RUN npm ci --engine-strict\n");
  assert.equal(f.run({ dockerfiles: ["Dockerfile"] }).ok, true);
});


test("B-BUILD-P2-02 direct·symlink·preserve-symlinks-main CLI는 모두 같은 잘못된 anchor를 거부한다", t => {
  const f = fixture(t); f.put(".npmrc", "engine-strict=false\n");
  cpSync(resolve(dirname(fileURLToPath(import.meta.url)), "../node_modules/ini"), join(f.root, "node_modules/ini"), { recursive: true });
  const alias = join(f.root, "checker-alias.mjs");
  try { symlinkSync(checker, alias); }
  catch (error) { throw new Error("NOT_RUN: CLI alias 경계 시험에 symlink 기능이 필요합니다", { cause: error }); }
  const results = [];
  for (const [flags, entry] of [[[], checker], [[], alias], [["--preserve-symlinks-main"], alias]]) {
    const q = spawnSync(process.execPath, [...flags, entry, "--root", f.root, "--registry", f.options.registry], { encoding: "utf8", cwd: f.root });
    results.push({ status: q.status, strictError: q.stderr.includes("engine-strict") });
  }
  assert.deepEqual(results, Array.from({ length: 3 }, () => ({ status: 1, strictError: true })));
});
test("checker API import는 잘못된 cwd에서도 자동 CLI 검사를 실행하지 않는다", t => {
  const f = fixture(t); f.put(".npmrc", "engine-strict=false\n");
  f.put("import-only.mjs", `import { checkToolchain } from ${JSON.stringify(pathToFileURL(checker).href)};\nif (typeof checkToolchain !== "function") throw Error("API");\nprocess.stdout.write("IMPORTED\\n");\n`);
  const q = spawnSync(process.execPath, [join(f.root, "import-only.mjs")], { cwd: f.root, encoding: "utf8" });
  assert.equal(q.status, 0); assert.equal(q.stdout, "IMPORTED\n"); assert.equal(q.stderr, "");
});


for (const [name, rc] of [
  ["A2 인용 force key", 'engine-strict=true\n"force"=true\n'],
  ["A2 작은따옴표 force key", "engine-strict=true\n'force'=true\n"],
  ["A2 section 내부 strict만 존재", "[unrelated]\nengine-strict=true\n"],
  ["B2 인용 strict false", 'engine-strict=true\n"engine-strict"=false\n'],
  ["B2 작은따옴표 strict false", "engine-strict=true\n'engine-strict'=false\n"],
  ["B2 section은 root force를 덮지 않음", "engine-strict=true\nforce=true\n[shadow]\nforce=false\n"],
  ["B2 section은 root strict를 덮지 않음", "engine-strict=false\n[shadow]\nengine-strict=true\n"],
]) {
  test(name, t => { const f = fixture(t); f.put(".npmrc", rc); assert.equal(f.run().ok, false); });
}
for (const [name, tail] of [
  ["A2 shell background", "& npm install --global npm@11.19.1"],
  ["A2 shell redirection", "> /tmp/ignored"],
  ["A2 shell 제어 문자", "\x01"],
]) {
  test(name, t => {
    const f = fixture(t); f.put("Dockerfile", attackFrom + attackPin + "RUN npm run build -- " + tail + "\nRUN npm ci --engine-strict\n");
    assert.equal(f.run({ dockerfiles: ["Dockerfile"] }).ok, false);
  });
}
test("B2 alias default registry는 실제 checker 데이터에 고정하고 명시 override는 유지한다", t => {
  const f = fixture(t), alias = join(f.root, "alias-site/bin/checker.mjs");
  cpSync(resolve(dirname(fileURLToPath(import.meta.url)), "../node_modules/ini"), join(f.root, "node_modules/ini"), { recursive: true });
  mkdirSync(dirname(alias), { recursive: true });
  try { symlinkSync(checker, alias); }
  catch (error) { throw new Error("NOT_RUN: default registry alias 시험에 symlink 기능이 필요합니다", { cause: error }); }
  const other = { axes: { node: { recommended: "24.15.0" }, npm: { recommended: "11.19.1" } } };
  const variants = [[[], checker], [[], alias], [["--preserve-symlinks-main"], alias]];
  const results = [];
  for (const fakeExists of [true, false]) {
    if (fakeExists) f.put("alias-site/versions.json", other);
    else rmSync(join(f.root, "alias-site/versions.json"));
    for (const good of [true, false]) {
      const selected = good ? { node, npm } : { node: "24.15.0", npm: "11.19.1" };
      f.put("package.json", { private: true, packageManager: "npm@" + selected.npm, engines: selected }); f.put(".nvmrc", selected.node);
      results.push(variants.map(([flags, entry]) => spawnSync(process.execPath, [...flags, entry, "--root", f.root], { encoding: "utf8", cwd: f.root }).status));
    }
  }
  assert.deepEqual(results, [[0,0,0],[1,1,1],[0,0,0],[1,1,1]]);
  f.put("alias-site/versions.json", other);
  for (const [flags, entry] of variants) {
    const q = spawnSync(process.execPath, [...flags, entry, "--root", f.root, "--registry", join(f.root, "alias-site/versions.json")], { encoding: "utf8", cwd: f.root });
    assert.equal(q.status, 0);
  }
});


test("공식 INI 전역 boolean·인용 key·section 비간섭과 중복을 수용한다", t => {
  const f = fixture(t);
  for (const rc of [
    '"engine-strict"=true\n"force"=false\n', "'engine-strict'=true\n'force'=false\n",
    "engine-strict=true\nforce=false\n[unrelated]\nengine-strict=false\nforce=true\n",
    "engine-strict=false\nengine-strict=true\nforce=true\nforce=false\nlegacy-peer-deps=true\nignore-scripts=true\n",
  ]) { f.put(".npmrc", rc); assert.equal(f.run().ok, true); }
});
test("공식 INI의 배열·객체·null·비boolean 값은 strict/force로 승인하지 않는다", t => {
  const f = fixture(t);
  for (const rc of ["engine-strict[]=true\n", "[engine-strict]\nvalue=true\n", "engine-strict=null\n", "engine-strict=yes\n", "engine-strict=true\nforce[]=false\n", "engine-strict=true\n[force]\nvalue=false\n", "engine-strict=true\nforce=null\n", "engine-strict=true\nforce=unknown\n"]) {
    f.put(".npmrc", rc); assert.equal(f.run().ok, false);
  }
});
test("지원 && 연결은 유지하고 JSON exec의 제어기호 인수는 shell로 재해석하지 않는다", t => {
  const f = fixture(t);
  f.put("Dockerfile", attackFrom + `RUN npm install --global npm@${npm} && npm ci --engine-strict && npm run build -- --flag\n`);
  assert.equal(f.run({ dockerfiles: ["Dockerfile"] }).ok, true);
  f.put("Dockerfile", attackFrom + attackPin + 'RUN ["npm","run","build","--","&",">","|","literal"]\n');
  assert.equal(f.run({ dockerfiles: ["Dockerfile"] }).ok, true);
});
