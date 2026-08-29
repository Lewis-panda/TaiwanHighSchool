#!/usr/bin/env node

import { createHash } from "node:crypto";
import { lstatSync, readFileSync, realpathSync } from "node:fs";
import { dirname, isAbsolute, join, relative, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const moduleRepoRoot = realpathSync(resolve(dirname(fileURLToPath(import.meta.url)), ".."));
export const FIGURE_MANIFEST_RELATIVE = "publishing/figures.json";

const rootKeys = ["generators", "runtime", "schemaVersion", "sharedInputs"];
const runtimeKeys = ["freetype", "implementation", "matplotlib", "numpy", "python"];
const fileKeys = ["path", "sha256"];
const generatorKeys = ["command", "id", "inputs", "outputs"];
const outputKeys = ["entrypoint", "path", "sha256"];

function fail(message) {
  throw new Error(message);
}

function exactKeys(value, expected, label) {
  if (!value || typeof value !== "object" || Array.isArray(value)) fail(`${label} 必須是 object`);
  const actual = Object.keys(value).sort();
  const wanted = [...expected].sort();
  if (JSON.stringify(actual) !== JSON.stringify(wanted)) {
    fail(`${label} 欄位必須精確為 ${wanted.join(", ")}；實際為 ${actual.join(", ")}`);
  }
}

function safeRelativePath(value, label) {
  if (typeof value !== "string" || !value || value !== value.normalize("NFC")) {
    fail(`${label} 必須是非空 NFC path`);
  }
  if (
    isAbsolute(value)
    || /^[A-Za-z]:/u.test(value)
    || value.includes("\\")
    || /[\u0000-\u001f\u007f]/u.test(value)
  ) {
    fail(`${label} 必須是 repository 內 POSIX relative path`);
  }
  const segments = value.split("/");
  if (segments.some((segment) => !segment || segment === "." || segment === "..")) {
    fail(`${label} 含不安全 path segment`);
  }
  return value;
}

function sha256Value(value, label) {
  if (typeof value !== "string" || !/^[0-9a-f]{64}$/u.test(value)) {
    fail(`${label} 必須是小寫 SHA-256`);
  }
  return value;
}

function validateFileRecord(record, label) {
  exactKeys(record, fileKeys, label);
  return {
    path: safeRelativePath(record.path, `${label}.path`),
    sha256: sha256Value(record.sha256, `${label}.sha256`),
  };
}

function validateOutputRecord(record, label) {
  exactKeys(record, outputKeys, label);
  const path = safeRelativePath(record.path, `${label}.path`);
  const parts = path.split("/");
  if (
    parts.length !== 5
    || parts[0] !== "content"
    || parts[3] !== "assets"
    || !parts[4].startsWith(`${parts[2]}-`)
    || !parts[4].endsWith(".svg")
  ) {
    fail(`${label}.path 必須是 content/<課程>/<章碼>/assets/<章碼>-<圖名>.svg`);
  }
  if (typeof record.entrypoint !== "string" || !/^[A-Za-z_][A-Za-z0-9_]*$/u.test(record.entrypoint)) {
    fail(`${label}.entrypoint 必須是 Python identifier`);
  }
  return {
    path,
    entrypoint: record.entrypoint,
    sha256: sha256Value(record.sha256, `${label}.sha256`),
  };
}

function assertUnique(records, selector, label) {
  const seen = new Set();
  for (const record of records) {
    const value = selector(record);
    if (seen.has(value)) fail(`${label} 重複：${value}`);
    seen.add(value);
  }
}

export function parseFigureManifestText(text, label = FIGURE_MANIFEST_RELATIVE) {
  let parsed;
  try {
    parsed = JSON.parse(text);
  } catch (error) {
    fail(`${label} 不是合法 JSON：${error.message}`);
  }
  if (text !== `${JSON.stringify(parsed, null, 2)}\n`) {
    fail(`${label} 必須是 canonical JSON；拒絕 duplicate key、非標準排版或尾端內容`);
  }

  exactKeys(parsed, rootKeys, label);
  if (parsed.schemaVersion !== 1) fail(`${label}.schemaVersion 必須是 1`);

  exactKeys(parsed.runtime, runtimeKeys, `${label}.runtime`);
  const versionPattern = /^[0-9]+(?:\.[0-9]+)+(?:[A-Za-z0-9.+-]*)?$/u;
  if (parsed.runtime.implementation !== "CPython") fail(`${label}.runtime.implementation 必須是 CPython`);
  for (const key of ["python", "numpy", "matplotlib", "freetype"]) {
    if (typeof parsed.runtime[key] !== "string" || !versionPattern.test(parsed.runtime[key])) {
      fail(`${label}.runtime.${key} 必須是精確版本`);
    }
  }
  if (!Array.isArray(parsed.sharedInputs) || parsed.sharedInputs.length === 0) {
    fail(`${label}.sharedInputs 必須是非空 array`);
  }
  const sharedInputs = parsed.sharedInputs.map((record, index) => validateFileRecord(record, `${label}.sharedInputs[${index}]`));
  assertUnique(sharedInputs, (record) => record.path, `${label} shared input path`);
  if (!sharedInputs.some((record) => record.path === "_tools/figlib.py")) {
    fail(`${label}.sharedInputs 必須包含 _tools/figlib.py`);
  }

  if (!Array.isArray(parsed.generators)) fail(`${label}.generators 必須是 array`);
  const generators = parsed.generators.map((generator, generatorIndex) => {
    const generatorLabel = `${label}.generators[${generatorIndex}]`;
    exactKeys(generator, generatorKeys, generatorLabel);
    if (typeof generator.id !== "string" || !/^[a-z0-9]+(?:-[a-z0-9]+)*$/u.test(generator.id)) {
      fail(`${generatorLabel}.id 必須是 kebab-case identifier`);
    }
    if (!Array.isArray(generator.command) || generator.command.length < 2) {
      fail(`${generatorLabel}.command 必須包含 python 與 script`);
    }
    if (generator.command[0] !== "python") fail(`${generatorLabel}.command[0] 必須是 python`);
    const script = safeRelativePath(generator.command[1], `${generatorLabel}.command[1]`);
    if (!script.startsWith("_tools/") || !script.endsWith(".py")) {
      fail(`${generatorLabel}.command[1] 必須是 _tools/ 內 Python script`);
    }
    const options = generator.command.slice(2);
    if (options.some((option) => typeof option !== "string" || !/^--[a-z0-9-]+$/u.test(option))) {
      fail(`${generatorLabel}.command 只允許固定長選項`);
    }
    assertUnique(options, (option) => option, `${generatorLabel} command option`);
    if (!Array.isArray(generator.inputs) || generator.inputs.length === 0) {
      fail(`${generatorLabel}.inputs 必須是非空 array`);
    }
    const inputs = generator.inputs.map((record, inputIndex) => validateFileRecord(record, `${generatorLabel}.inputs[${inputIndex}]`));
    assertUnique(inputs, (record) => record.path, `${generatorLabel} input path`);
    if (!inputs.some((record) => record.path === script)) {
      fail(`${generatorLabel}.inputs 必須包含 command script ${script}`);
    }
    if (!Array.isArray(generator.outputs) || generator.outputs.length === 0) {
      fail(`${generatorLabel}.outputs 必須是非空 array`);
    }
    const outputs = generator.outputs.map((record, outputIndex) => validateOutputRecord(record, `${generatorLabel}.outputs[${outputIndex}]`));
    assertUnique(outputs, (record) => record.path, `${generatorLabel} output path`);
    return { id: generator.id, command: [...generator.command], inputs, outputs };
  });

  assertUnique(generators, (generator) => generator.id, `${label} generator id`);
  assertUnique(generators, (generator) => JSON.stringify(generator.command), `${label} generator command`);
  const allInputs = [...sharedInputs, ...generators.flatMap((generator) => generator.inputs)];
  const allOutputs = generators.flatMap((generator) => generator.outputs);
  assertUnique(allInputs, (record) => record.path, `${label} input owner`);
  assertUnique(allOutputs, (record) => record.path, `${label} output owner`);
  const inputPaths = new Set(allInputs.map((record) => record.path));
  for (const output of allOutputs) {
    if (inputPaths.has(output.path)) fail(`${label} path 同時是 input 與 output：${output.path}`);
  }

  return {
    schemaVersion: 1,
    runtime: { ...parsed.runtime },
    sharedInputs,
    generators,
    allInputs,
    allOutputs,
  };
}

export function sha256File(path) {
  return createHash("sha256").update(readFileSync(path)).digest("hex");
}

export function canonicalManifestFile(repoRoot, relativePath, expectedSha256, label = relativePath) {
  const root = realpathSync(repoRoot);
  const absolute = resolve(root, relativePath);
  const fromRoot = relative(root, absolute);
  if (!fromRoot || fromRoot === ".." || fromRoot.startsWith(`..${process.platform === "win32" ? "\\" : "/"}`)) {
    fail(`${label} 逃離 repository`);
  }
  let stat;
  try {
    stat = lstatSync(absolute);
  } catch (error) {
    fail(`${label} 不存在：${error.message}`);
  }
  if (stat.isSymbolicLink() || !stat.isFile() || realpathSync(absolute) !== absolute) {
    fail(`${label} 必須是 canonical 一般檔案，不得含 symlink`);
  }
  const actualSha256 = sha256File(absolute);
  if (expectedSha256 && actualSha256 !== expectedSha256) {
    fail(`${label} SHA-256 不符：manifest=${expectedSha256} actual=${actualSha256}`);
  }
  return absolute;
}

export function loadFigureManifest(repoRoot = moduleRepoRoot) {
  const root = realpathSync(repoRoot);
  const manifestPath = canonicalManifestFile(root, FIGURE_MANIFEST_RELATIVE, null, FIGURE_MANIFEST_RELATIVE);
  const manifest = parseFigureManifestText(readFileSync(manifestPath, "utf8"));
  for (const record of [...manifest.allInputs, ...manifest.allOutputs]) {
    canonicalManifestFile(root, record.path, record.sha256, record.path);
  }
  return { repoRoot: root, manifestPath, manifest };
}

export function figurePipelineFiles(repoRoot = moduleRepoRoot) {
  const { manifest } = loadFigureManifest(repoRoot);
  return manifest.allInputs.map((record) => record.path);
}
