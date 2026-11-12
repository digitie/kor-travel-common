// SPDX-License-Identifier: GPL-3.0-or-later
// SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
// 빌드 도구의 값 정본은 versions.json이다. 공개 UI 패키지와 배포물은 바꾸지 않는다.
import { existsSync, lstatSync, readFileSync, realpathSync } from "node:fs";
import { dirname, isAbsolute, matchesGlob, relative, resolve, sep } from "node:path";
import { parseArgs } from "node:util";
import { fileURLToPath } from "node:url";

class InputError extends Error {}
const object = value => value !== null && typeof value === "object" && !Array.isArray(value);

function regular(path) {
  if (!lstatSync(path).isFile() || lstatSync(path).isSymbolicLink()) throw new InputError("일반 파일만 허용합니다");
  return path;
}

function bounded(root, name) {
  if (typeof name !== "string" || !name || isAbsolute(name) || name.includes("\\") || /^[A-Za-z]:/u.test(name)
    || name.split("/").some(part => !part || part === "." || part === "..") || /[\0-\x1f\x7f]/u.test(name)) {
    throw new InputError("저장소 상대 경로가 필요합니다");
  }
  const path = resolve(root, name);
  for (const candidate of [path, realpathSync(path)]) {
    const rel = relative(root, candidate);
    if (rel === ".." || rel.startsWith(".." + sep) || isAbsolute(rel)) {
      throw new InputError("저장소 밖 검사 경로는 거부합니다");
    }
  }
  return regular(path);
}

function json(path) {
  try {
    const value = JSON.parse(readFileSync(regular(path), "utf8"));
    if (!object(value)) throw new Error();
    return value;
  } catch { throw new InputError("JSON 객체 파일을 읽을 수 없습니다"); }
}

function workspaceMember(rootPackage, folder) {
  if (rootPackage.workspaces === undefined) return false;
  const patterns = Array.isArray(rootPackage.workspaces)
    ? rootPackage.workspaces : rootPackage.workspaces?.packages;
  if (!Array.isArray(patterns) || patterns.some(p => typeof p !== "string" || !p)) {
    throw new InputError("workspace 선언이 올바르지 않습니다");
  }
  let included = false;
  for (const pattern of patterns) {
    const negative = pattern.startsWith("!");
    if (matchesGlob(folder, negative ? pattern.slice(1) : pattern)) included = !negative;
  }
  return included;
}

function strictEngineConfig(path) {
  let selected;
  for (const raw of readFileSync(path, "utf8").split(/\r?\n/u)) {
    const line = raw.split(/[;#]/u, 1)[0].trim();
    if (!/^engine-strict\s*=/iu.test(line)) continue;
    const match = /^engine-strict\s*=\s*(true|false)\s*$/iu.exec(line);
    if (!match) return false;
    selected = match[1].toLowerCase() === "true";
  }
  return selected === true;
}

function pathList(value, label, nonempty = false) {
  if (!Array.isArray(value) || (nonempty && value.length === 0)
    || value.some(name => typeof name !== "string" || !name)) {
    throw new InputError(label + "는 경로 문자열 배열이어야 합니다");
  }
  return value;
}

function npmCommand(command, stage, npm, label, errors) {
  let words;
  if (command.startsWith("[")) {
    try { words = JSON.parse(command); } catch { errors.push(label + " npm 실행 배열을 해석할 수 없습니다"); return; }
    if (!Array.isArray(words) || words.some(word => typeof word !== "string")) {
      errors.push(label + " npm 실행 배열이 올바르지 않습니다"); return;
    }
  } else {
    // 이 검사는 실제 저장소의 단순 npm/npx 명령만 지원한다. shell 제어·치환은 실행하지 않는다.
    if (/[|;$`]/u.test(command)) { errors.push(label + " npm 명령의 동적 shell 형식은 지원하지 않습니다"); return; }
    words = command.trim().split(/\s+/u).map(word => word.replace(/^(['"])(.*)\1$/u, "$2"));
  }
  if (words.some(word => word === "-f" || /^(?:--force|--legacy-peer-deps)(?:=|$)/u.test(word))) {
    errors.push(label + " force·legacy-peer-deps 우회 옵션은 허용하지 않습니다"); return;
  }
  if (!stage.node || !["npm", "npx"].includes(words[0])) {
    errors.push(label + " 정적으로 검증 가능한 Node npm/npx 명령이 필요합니다"); return;
  }
  const install = words[0] === "npm" && ["install", "i"].includes(words[1])
    && words.some(word => ["-g", "--global"].includes(word));
  if (install) {
    if (words.length !== 4 || !["-g", "--global"].includes(words[2]) || words[3] !== "npm@" + npm) {
      errors.push(label + " 전역 npm 설치는 정본 exact literal만 지원합니다"); return;
    }
    stage.pinned = true; return;
  }
  const explicit = words[0] === "npx" && words.slice(1).find(word => !["--yes", "-y"].includes(word));
  if (explicit && explicit.startsWith("npm@") && explicit !== "npm@" + npm) {
    errors.push(label + " 명시 npm CLI 버전 불일치"); return;
  }
  if (!stage.pinned && explicit !== "npm@" + npm) {
    errors.push(label + " fresh Node stage의 npm/npx 명시 선택이 필요합니다");
  }
  if (words.includes("ci") && !words.includes("--engine-strict")) {
    errors.push(label + " npm ci --engine-strict가 필요합니다");
  }
}

function nodeImages(text, node, npm, label, errors) {
  const args = new Map(), stages = new Map();
  let count = 0, inStage = false, stage = { node: false, pinned: false };
  // FROM의 전역 ARG만 해석한다. stage 내부 ARG는 다음 FROM 기본값을 바꾸지 않는다.
  const lines = text.split(/\r?\n/u).filter(line => !line.trim().startsWith("#"))
    .join("\n").replace(/\\\n/gu, " ").split("\n");
  for (const [index, raw] of lines.entries()) {
    const line = raw.trim();
    if (!line || line.startsWith("#")) continue;
    const arg = /^ARG\s+([A-Za-z_]\w*)(?:=(.*))?$/iu.exec(line);
    if (arg && !inStage) {
      if (arg[2] !== undefined) args.set(arg[1], arg[2].trim().replace(/^(['"])(.*)\1$/u, "$2"));
      continue;
    }
    const run = /^(?:RUN|CMD|ENTRYPOINT)\s+(.+)$/iu.exec(line);
    if (run && /\b(?:npm|npx)\b/u.test(run[1])) {
      const command = run[1].replace(/^(?:--[\w-]+=\S+\s+)+/u, "");
      const commands = command.startsWith("[") ? [command] : command.split(/\s*&&\s*/u);
      for (const part of commands) {
        if (/\b(?:npm|npx)\b/u.test(part)) npmCommand(part, stage, npm, label, errors);
      }
    }
    if (!/^FROM\b/iu.test(line)) continue;
    inStage = true;
    const from = /^FROM\s+(?:--platform=\S+\s+)?(\S+)(?:\s+AS\s+([A-Za-z0-9_.-]+))?$/iu.exec(line);
    if (!from) { errors.push(label + " FROM 형식을 정적으로 검증할 수 없습니다"); continue; }
    const image = from[1].replace(/\$\{([A-Za-z_]\w*)\}|\$([A-Za-z_]\w*)/gu,
      (match, braced, bare) => args.get(braced ?? bare) ?? match);
    stage = { ...(stages.get(image.toLowerCase()) ?? { node: false, pinned: false }) };
    if (image.includes("$")) {
      errors.push(label + " 기본 이미지 ARG 값이 필요합니다");
    } else if (!stages.has(image.toLowerCase()) && image !== "scratch") {
      const repository = image.split("@")[0].replace(/:[^/:]*$/u, "");
      const isNode = /(?:^|\/)node$/u.test(repository);
      if (isNode) {
        stage.node = true;
        count += 1;
        const match = /^(?:docker\.io\/(?:library\/)?|library\/)?node:([^@\s]+)@sha256:([0-9a-f]{64})$/u.exec(image);
        if (!match || match[1].split("-")[0] !== node) {
          errors.push(label + ":" + (index + 1) + " Node 이미지의 정확 버전·digest가 정본과 맞지 않습니다");
        }
      }
    }
    if (from[2]) stages.set(from[2].toLowerCase(), stage);
  }
  if (count === 0) errors.push(label + " 정적으로 검증 가능한 Node 이미지가 없습니다");
  return count;
}

export function checkToolchain(options) {
  const errors = [];
  let node, npm;
  try {
    const registry = json(resolve(options.registry));
    node = registry.axes?.node?.recommended;
    npm = registry.axes?.npm?.recommended;
    if (![node, npm].every(value => typeof value === "string" && /^\d+\.\d+\.\d+$/u.test(value))) {
      throw new InputError("Node/npm 권고값은 정확한 세 자리 버전이어야 합니다");
    }
    const root = realpathSync(options.root);
    const selector = bounded(root, ".nvmrc");
    if (readFileSync(selector, "utf8").trim() !== node) errors.push(".nvmrc Node 버전 불일치");
    if (existsSync(resolve(root, ".node-version"))
      && readFileSync(bounded(root, ".node-version"), "utf8").trim() !== node) {
      errors.push(".node-version Node 버전 불일치");
    }
    const rootName = "package.json";
    const rootPackage = existsSync(resolve(root, rootName)) ? json(bounded(root, rootName)) : {};
    const anchors = new Map();
    for (const name of pathList(options.manifests === undefined ? [rootName] : options.manifests, "manifest", true)) {
      const path = bounded(root, name), manifest = json(path);
      const folder = relative(root, dirname(path)).split(sep).join("/");
      const inherited = path !== resolve(root, rootName) && workspaceMember(rootPackage, folder);
      if (inherited && rootPackage.private !== true) throw new InputError("workspace 도구 정본은 private root여야 합니다");
      const anchor = inherited ? bounded(root, rootName) : path;
      const data = inherited ? rootPackage : manifest;
      anchors.set(anchor, data);
      if (manifest.packageManager !== undefined && manifest.packageManager !== "npm@" + npm) {
        errors.push(name + " packageManager 버전 불일치");
      }
    }
    if (anchors.size === 0) throw new InputError("검사할 manifest가 필요합니다");
    for (const [path, data] of anchors) {
      const name = relative(root, path).split(sep).join("/");
      if (data.private !== true) errors.push(name + " 도구 정본은 private 앱/root여야 합니다");
      if (data.packageManager !== "npm@" + npm) errors.push(name + " packageManager 선언 누락·불일치");
      if (data.engines?.node !== node || data.engines?.npm !== npm) errors.push(name + " engines Node/npm 선언 누락·불일치");
      const config = bounded(root, relative(root, resolve(dirname(path), ".npmrc")).split(sep).join("/"));
      if (!strictEngineConfig(config)) errors.push(name + " engine-strict=true가 필요합니다");
    }
    let checkedNodeImages = 0;
    for (const name of pathList(options.dockerfiles === undefined ? [] : options.dockerfiles, "Dockerfile")) {
      const path = bounded(root, name);
      checkedNodeImages += nodeImages(readFileSync(path, "utf8"), node, npm, name, errors);
    }
    if (options.runtime) {
      if ((options.nodeVersion ?? process.versions.node) !== node) errors.push("실행 Node 버전 불일치");
      const agent = options.npmAgent ?? process.env.npm_config_user_agent ?? "";
      if (typeof agent !== "string" || !agent.startsWith("npm/" + npm + " ") && agent !== "npm/" + npm) {
        errors.push("실행 npm 버전 불일치: npm run check:toolchain으로 실행하세요");
      }
    }
    return { ok: errors.length === 0, errors, node, npm, anchors: anchors.size, checkedNodeImages };
  } catch (error) {
    errors.push(error instanceof InputError ? error.message : "검사 파일·경로를 읽을 수 없습니다");
    return { ok: false, errors, node, npm };
  }
}

if (process.argv[1] && resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  try {
    const { values } = parseArgs({ options: {
      root: { type: "string", default: "." },
      registry: { type: "string", default: resolve(dirname(fileURLToPath(import.meta.url)), "../versions.json") },
      manifest: { type: "string", multiple: true },
      dockerfile: { type: "string", multiple: true },
      manifests: { type: "string", default: "[]" },
      dockerfiles: { type: "string", default: "[]" },
      runtime: { type: "boolean", default: false },
    } });
    const extra = pathList(JSON.parse(values.manifests), "추가 manifest");
    const dockerfiles = pathList(JSON.parse(values.dockerfiles), "Dockerfile");
    const result = checkToolchain({ ...values,
      manifests: [...(values.manifest ?? ["package.json"]), ...extra],
      dockerfiles: [...(values.dockerfile ?? []), ...dockerfiles],
    });
    for (const error of result.errors) process.stderr.write("도구 규칙: " + error + "\n");
    if (result.ok) process.stdout.write("Node " + result.node + " / npm " + result.npm + " 도구 규칙 PASS\n");
    process.exitCode = result.ok ? 0 : 1;
  } catch {
    process.stderr.write("도구 규칙 검사 인수가 올바르지 않습니다\n");
    process.exitCode = 2;
  }
}
