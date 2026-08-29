#!/usr/bin/env node

import { spawnSync } from "node:child_process";
import { createHash } from "node:crypto";
import {
  accessSync,
  chmodSync,
  constants,
  copyFileSync,
  existsSync,
  lstatSync,
  mkdirSync,
  mkdtempSync,
  readFileSync,
  readdirSync,
  realpathSync,
  readlinkSync,
  rmSync,
} from "node:fs";
import { tmpdir } from "node:os";
import { basename, delimiter, dirname, isAbsolute, join, relative, resolve, sep } from "node:path";
import { fileURLToPath } from "node:url";

const scriptDir = dirname(fileURLToPath(import.meta.url));
const sourceRoot = realpathSync(resolve(scriptDir, ".."));
const forbiddenTopLevel = new Set([
  ".obsidian",
  ".venv",
  "_課綱",
  "_範本",
  "_tools",
  "數學",
  "物理",
  "講義",
  "高中教材",
  "research",
]);

function fail(message) {
  throw new Error(message);
}

function sha256(path) {
  return createHash("sha256").update(readFileSync(path)).digest("hex");
}

function sorted(values) {
  return [...values].sort((left, right) => left < right ? -1 : left > right ? 1 : 0);
}

function isInside(root, target) {
  const rel = relative(root, target);
  return rel === "" || (!isAbsolute(rel) && rel !== ".." && !rel.startsWith(`..${sep}`));
}

function assertCanonicalDirectory(path, label) {
  const entry = lstatSync(path);
  if (entry.isSymbolicLink() || !entry.isDirectory() || realpathSync(path) !== path) {
    fail(`${label} 必須是 canonical 一般目錄`);
  }
  return { dev: entry.dev, ino: entry.ino };
}

function assertCanonicalFile(path, root, label) {
  const entry = lstatSync(path);
  if (entry.isSymbolicLink() || !entry.isFile() || realpathSync(path) !== path || !isInside(root, path)) {
    fail(`${label} 必須是 repository 內的 canonical 一般檔案`);
  }
  return path;
}

function validateRelativePath(value, label, allowedPrivatePaths = new Set()) {
  if (typeof value !== "string" || !value || value !== value.normalize("NFC")) fail(`${label} 路徑無效`);
  if (isAbsolute(value) || value.includes("\\") || /[\u0000-\u001f\u007f]/u.test(value)) fail(`${label} 路徑不安全`);
  const segments = value.split("/");
  if (segments.some((segment) => !segment || segment === "." || segment === "..")) fail(`${label} 含 dot segment`);
  if (
    (forbiddenTopLevel.has(segments[0]) && !allowedPrivatePaths.has(value))
    || segments.includes("編輯判定.md")
    || segments.includes(".git")
  ) {
    fail(`${label} 指向明確排除的資料：${value}`);
  }
  return value;
}

function readJson(path, label) {
  try {
    return JSON.parse(readFileSync(path, "utf8"));
  } catch (error) {
    fail(`${label} JSON 無效：${error.message}`);
  }
}

function run(command, args, { cwd, env = process.env, quiet = false } = {}) {
  const result = spawnSync(command, args, {
    cwd,
    env,
    encoding: "utf8",
    maxBuffer: 64 * 1024 * 1024,
  });
  if (result.error) fail(`${basename(command)} 無法執行：${result.error.message}`);
  if (result.status !== 0) {
    const detail = [result.stdout, result.stderr].filter(Boolean).join("\n").trim();
    fail(`${basename(command)} 結束碼 ${result.status}${detail ? `：\n${detail}` : ""}`);
  }
  if (!quiet && result.stdout) process.stdout.write(result.stdout);
  return result.stdout ?? "";
}

function treeFingerprint(path) {
  if (!existsSync(path)) return "absent";
  const root = resolve(path);
  const records = [];
  function visit(current) {
    const entry = lstatSync(current);
    const rel = relative(root, current) || ".";
    if (entry.isSymbolicLink()) {
      records.push([rel, "link", readlinkSync(current), entry.mtimeMs, entry.ctimeMs]);
      return;
    }
    if (entry.isDirectory()) {
      records.push([rel, "dir", entry.mode, entry.mtimeMs, entry.ctimeMs]);
      for (const name of sorted(readdirSync(current))) visit(join(current, name));
      return;
    }
    if (entry.isFile()) {
      records.push([rel, "file", entry.mode, entry.size, entry.mtimeMs, entry.ctimeMs, sha256(current)]);
      return;
    }
    records.push([rel, "special", entry.mode, entry.size, entry.mtimeMs, entry.ctimeMs]);
  }
  visit(root);
  return createHash("sha256").update(JSON.stringify(records)).digest("hex");
}

function protectedSourceState() {
  return Object.fromEntries(
    ["dist", "output", "tmp", "node_modules"].map((name) => [name, treeFingerprint(join(sourceRoot, name))]),
  );
}

function assertPhysicalClosure(worktree, expectedPaths) {
  const files = [];
  walkTree(worktree, (path, entry) => {
    if (entry.isSymbolicLink()) fail(`fixture closure 不得含 symlink：${relative(worktree, path)}`);
    if (entry.isFile()) {
      files.push(relative(worktree, path).split(sep).join("/"));
    } else if (!entry.isDirectory()) {
      fail(`fixture closure 不得含特殊檔：${relative(worktree, path)}`);
    }
  });
  if (JSON.stringify(sorted(files)) !== JSON.stringify(sorted(expectedPaths))) {
    fail("fixture 實體一般檔集合不是 manifest 精確 closure");
  }
}

function assertSame(left, right, label) {
  if (JSON.stringify(left) !== JSON.stringify(right)) fail(`${label} 在 smoke test 期間改變`);
}

function ensureDestinationDirectory(root, relativeDirectory) {
  let current = root;
  if (relativeDirectory === ".") return current;
  for (const segment of relativeDirectory.split("/")) {
    const next = join(current, segment);
    if (!existsSync(next)) mkdirSync(next, { mode: 0o700 });
    assertCanonicalDirectory(next, `fixture/${relative(root, next)}`);
    current = next;
  }
  return current;
}

function copyClosureFile(worktree, relativePath, expectedDigest, allowedPrivatePaths) {
  validateRelativePath(relativePath, `closure:${relativePath}`, allowedPrivatePaths);
  const source = assertCanonicalFile(join(sourceRoot, relativePath), sourceRoot, `closure:${relativePath}`);
  if (sha256(source) !== expectedDigest) fail(`baseline hash 已過期：${relativePath}`);
  const parent = ensureDestinationDirectory(worktree, dirname(relativePath));
  const destination = join(worktree, relativePath);
  if (existsSync(destination)) fail(`fixture 目的檔已存在：${relativePath}`);
  copyFileSync(source, destination, constants.COPYFILE_EXCL);
  chmodSync(destination, 0o600);
  assertCanonicalFile(destination, worktree, `fixture:${relativePath}`);
  if (sha256(destination) !== expectedDigest || sha256(source) !== expectedDigest) {
    fail(`copy 前後 hash 不一致：${relativePath}`);
  }
}

function walkTree(root, visit) {
  for (const name of sorted(readdirSync(root))) {
    const path = join(root, name);
    visit(path, lstatSync(path));
    if (lstatSync(path).isDirectory()) walkTree(path, visit);
  }
}

function assertNodeModulesSafe(nodeModules) {
  const root = realpathSync(nodeModules);
  assertCanonicalDirectory(root, "source node_modules");
  const activeDirectories = new Set();

  function audit(path) {
    const originalEntry = lstatSync(path);
    let canonical = path;
    if (originalEntry.isSymbolicLink()) {
      try {
        canonical = realpathSync(path);
      } catch (error) {
        fail(`node_modules 含 broken symlink：${relative(root, path)}（${error.message}）`);
      }
      if (!isInside(root, canonical)) {
        fail(`node_modules symlink 逸出 dependency root：${relative(root, path)}`);
      }
    }

    const entry = lstatSync(canonical);
    if (entry.isFile()) return;
    if (!entry.isDirectory()) {
      fail(`node_modules 含 symlink／一般檔／目錄以外的特殊項目：${relative(root, path)}`);
    }
    const directory = realpathSync(canonical);
    if (!isInside(root, directory)) fail(`node_modules 目錄逸出 dependency root：${relative(root, path)}`);
    if (activeDirectories.has(directory)) fail(`node_modules symlink 形成目錄 loop：${relative(root, path)}`);
    activeDirectories.add(directory);
    try {
      for (const name of sorted(readdirSync(directory))) audit(join(directory, name));
    } finally {
      activeDirectories.delete(directory);
    }
  }

  audit(root);
  return root;
}

function copyDereferencedEntry(source, destination, sourceNodeModules, activeDirectories) {
  const originalEntry = lstatSync(source);
  const canonical = originalEntry.isSymbolicLink() ? realpathSync(source) : source;
  if (!isInside(sourceNodeModules, canonical)) {
    fail(`node_modules copy 來源逸出 dependency root：${relative(sourceNodeModules, source)}`);
  }
  const entry = lstatSync(canonical);
  if (entry.isFile()) {
    if (existsSync(destination)) fail(`node_modules copy 目的項目已存在：${basename(destination)}`);
    copyFileSync(canonical, destination, constants.COPYFILE_EXCL);
    chmodSync(destination, entry.mode & 0o777);
    return;
  }
  if (!entry.isDirectory()) {
    fail(`node_modules copy 拒絕特殊項目：${relative(sourceNodeModules, source)}`);
  }

  const directory = realpathSync(canonical);
  if (activeDirectories.has(directory)) {
    fail(`node_modules copy 偵測到目錄 loop：${relative(sourceNodeModules, source)}`);
  }
  if (existsSync(destination)) fail(`node_modules copy 目的目錄已存在：${basename(destination)}`);
  mkdirSync(destination, { mode: entry.mode & 0o777 });
  chmodSync(destination, entry.mode & 0o777);
  activeDirectories.add(directory);
  try {
    for (const name of sorted(readdirSync(directory))) {
      copyDereferencedEntry(
        join(directory, name),
        join(destination, name),
        sourceNodeModules,
        activeDirectories,
      );
    }
  } finally {
    activeDirectories.delete(directory);
  }
}

export function copyNodeModules(worktree) {
  const source = assertNodeModulesSafe(join(sourceRoot, "node_modules"));
  const destination = join(worktree, "node_modules");
  copyDereferencedEntry(source, destination, source, new Set());
  assertCanonicalDirectory(destination, "fixture node_modules");
  walkTree(destination, (path, entry) => {
    if (entry.isSymbolicLink()) fail(`fixture node_modules 仍含 symlink：${relative(destination, path)}`);
    if (!entry.isFile() && !entry.isDirectory()) {
      fail(`fixture node_modules 含特殊項目：${relative(destination, path)}`);
    }
  });
  const resolved = run(process.execPath, ["-e", "process.stdout.write(require.resolve('playwright'))"], {
    cwd: worktree,
    quiet: true,
  }).trim();
  const canonical = realpathSync(resolved);
  if (!isInside(destination, canonical)) fail("fixture Playwright 未解析到隔離 node_modules");
}

function assertNoForbiddenDirectories(worktree, allowedPrivatePaths) {
  for (const name of forbiddenTopLevel) {
    if (name === "_tools") continue;
    if (existsSync(join(worktree, name))) fail(`fixture 不得包含 ${name}/`);
  }
  const figureTools = join(worktree, "_tools");
  if (existsSync(figureTools)) {
    const actual = [];
    walkTree(figureTools, (path, entry) => {
      if (entry.isSymbolicLink() || (!entry.isFile() && !entry.isDirectory())) {
        fail(`fixture _tools 含非一般檔案：${relative(worktree, path)}`);
      }
      if (entry.isFile()) actual.push(relative(worktree, path).split(sep).join("/"));
    });
    const expected = sorted([...allowedPrivatePaths].filter((path) => path.startsWith("_tools/")));
    if (JSON.stringify(sorted(actual)) !== JSON.stringify(expected)) {
      fail("fixture _tools 不是 figures.json 精確閉包");
    }
  }
  for (const rootName of ["content", "assets", "publishing", "styles", "templates", "tools"]) {
    const root = join(worktree, rootName);
    if (!existsSync(root)) continue;
    walkTree(root, (path) => {
      if (basename(path) === "編輯判定.md") fail("fixture 不得包含 編輯判定.md");
    });
  }
}

function parseCli() {
  const args = process.argv.slice(2);
  let setId;
  for (let index = 0; index < args.length; index += 1) {
    if (args[index] !== "--set" || !args[index + 1]) fail("用法：node tools/isolated-release-smoke.mjs [--set SET_ID]");
    if (setId) fail("--set 不得重複");
    setId = args[index + 1];
    index += 1;
  }
  if (setId && !/^[a-z0-9][a-z0-9._-]*$/u.test(setId)) fail(`不安全的 set id：${setId}`);
  return setId;
}

function loadBaseline(requestedSetId) {
  const registryPath = join(sourceRoot, "publishing", "sets.json");
  const registry = readJson(registryPath, "publishing registry");
  const setId = requestedSetId ?? registry.defaultSet;
  if (!/^[a-z0-9][a-z0-9._-]*$/u.test(setId ?? "")) fail("default set id 無效");
  const set = registry.sets?.[setId];
  if (!set || !Array.isArray(set.documents) || set.documents.length === 0) fail(`找不到 publication set：${setId}`);
  const distDir = join(sourceRoot, "dist", setId);
  assertCanonicalDirectory(distDir, `baseline dist/${setId}`);
  const manifestPath = assertCanonicalFile(join(distDir, "manifest.json"), sourceRoot, "baseline manifest");
  const sumsPath = assertCanonicalFile(join(distDir, "SHA256SUMS"), sourceRoot, "baseline SHA256SUMS");
  const manifest = readJson(manifestPath, "baseline manifest");
  if (manifest.set !== setId || !Array.isArray(manifest.pipeline) || !Array.isArray(manifest.artifacts)) {
    fail("baseline manifest schema/identity 無效");
  }
  if (manifest.artifacts.length !== set.documents.length) fail("baseline artifact 數量與 registry 不一致");

  const closure = new Map();
  const allowedPrivatePaths = new Set();
  const add = (path, digest, label, { figureInput = false } = {}) => {
    if (figureInput) {
      if (typeof path !== "string" || !path.startsWith("_tools/")) {
        fail(`${label} 必須是 _tools/ 內明列的公開產圖輸入`);
      }
      allowedPrivatePaths.add(path);
    }
    validateRelativePath(path, label, allowedPrivatePaths);
    if (!/^[0-9a-f]{64}$/u.test(digest ?? "")) fail(`${label} SHA-256 無效`);
    const prior = closure.get(path);
    if (prior && prior !== digest) fail(`${label} closure hash 衝突：${path}`);
    closure.set(path, digest);
  };
  for (const entry of manifest.pipeline) {
    if (!entry || Object.keys(entry).sort().join(",") !== "path,sha256") fail("manifest pipeline entry 無效");
    if (closure.has(entry.path)) fail(`manifest pipeline path 重複：${entry.path}`);
    add(entry.path, entry.sha256, `pipeline:${entry.path}`);
  }
  if (!closure.has(".gitignore")) fail("manifest pipeline 必須納入 .gitignore");

  const figureManifest = readJson(join(sourceRoot, "publishing", "figures.json"), "figure manifest");
  const figureInputs = [
    ...(figureManifest.sharedInputs ?? []),
    ...(figureManifest.generators ?? []).flatMap((generator) => generator.inputs ?? []),
  ];
  for (const entry of figureInputs) {
    if (!entry || Object.keys(entry).sort().join(",") !== "path,sha256") {
      fail("figure manifest input 無效");
    }
    add(entry.path, entry.sha256, `figure-input:${entry.path}`, { figureInput: true });
  }

  const artifactsById = new Map(manifest.artifacts.map((artifact) => [artifact.id, artifact]));
  const expectedDistNames = new Set(["manifest.json", "SHA256SUMS"]);
  for (const document of set.documents) {
    const artifact = artifactsById.get(document.id);
    if (!artifact || artifact.audience !== document.audience || artifact.source !== document.source || artifact.slug !== document.slug) {
      fail(`${document.id} baseline artifact 與 registry 不一致`);
    }
    add(document.source, artifact.sourceSha256, `${document.id}.source`);
    const baselineAssets = new Map((artifact.assets ?? []).map((asset) => [asset.path, asset.sha256]));
    if (JSON.stringify(sorted(baselineAssets.keys())) !== JSON.stringify(sorted(document.assets ?? []))) {
      fail(`${document.id} baseline assets 與 registry 不一致`);
    }
    for (const asset of document.assets ?? []) add(asset, baselineAssets.get(asset), `${document.id}.asset`);
    for (const [kind, filename, digest] of [
      ["HTML", artifact.html, artifact.htmlSha256],
      ["PDF", artifact.pdf, artifact.pdfSha256],
    ]) {
      validateRelativePath(filename, `${document.id}.${kind}`);
      if (filename.includes("/")) fail(`${document.id}.${kind} 必須是 dist 第一層檔案`);
      const path = assertCanonicalFile(join(distDir, filename), sourceRoot, `${document.id}.${kind}`);
      if (sha256(path) !== digest) fail(`${document.id}.${kind} 與 baseline hash 不一致`);
      expectedDistNames.add(filename);
    }
  }
  if (artifactsById.size !== set.documents.length) fail("baseline manifest 有未知或重複 artifact id");

  const actualDistNames = new Set(readdirSync(distDir));
  if (JSON.stringify(sorted(actualDistNames)) !== JSON.stringify(sorted(expectedDistNames))) fail("baseline dist 不是精確白名單");
  const expectedSums = `${sorted(manifest.artifacts.flatMap((artifact) => [
    `${artifact.htmlSha256}  ${artifact.html}`,
    `${artifact.pdfSha256}  ${artifact.pdf}`,
  ])).join("\n")}\n`;
  if (readFileSync(sumsPath, "utf8") !== expectedSums) fail("baseline SHA256SUMS 與 manifest 不一致");

  for (const [path, digest] of closure) {
    const source = assertCanonicalFile(join(sourceRoot, path), sourceRoot, `closure:${path}`);
    if (sha256(source) !== digest) fail(`baseline manifest 已 stale：${path}`);
  }
  return { registry, setId, set, distDir, manifest, expectedSums, closure, allowedPrivatePaths };
}

function makePrivateOuter() {
  const parent = realpathSync(tmpdir());
  assertCanonicalDirectory(parent, "system temp root");
  if (isInside(sourceRoot, parent)) fail("system temp root 不得位於主 repository 內");
  let root;
  try {
    root = realpathSync(mkdtempSync(join(parent, "highschool-release-smoke-")));
    chmodSync(root, 0o700);
    if (dirname(root) !== parent) fail("smoke temp 不是 temp root 的直接子目錄");
    const identity = assertCanonicalDirectory(root, "smoke temp");
    const mode = lstatSync(root).mode & 0o777;
    if (mode !== 0o700) fail(`smoke temp 權限不是 0700：${mode.toString(8)}`);
    return { parent, root, identity };
  } catch (error) {
    if (root && existsSync(root) && dirname(root) === parent) {
      const entry = lstatSync(root);
      if (!entry.isSymbolicLink() && entry.isDirectory() && realpathSync(root) === root) {
        rmSync(root, { recursive: true, force: false });
      }
    }
    throw error;
  }
}

function safeCleanup(temp) {
  if (!existsSync(temp.root)) return;
  if (dirname(temp.root) !== temp.parent) fail("拒絕清理非 temp 直接子目錄");
  const current = assertCanonicalDirectory(temp.root, "smoke temp cleanup");
  if (current.dev !== temp.identity.dev || current.ino !== temp.identity.ino) fail("smoke temp identity 改變，拒絕清理");
  rmSync(temp.root, { recursive: true, force: false });
}

function initializeSyntheticRepository(worktree, closurePaths, env, outerRoot) {
  const template = join(outerRoot, "empty-git-template");
  mkdirSync(template, { mode: 0o700 });
  const gitEnv = {
    ...env,
    GIT_CONFIG_NOSYSTEM: "1",
    GIT_CONFIG_GLOBAL: "/dev/null",
    GIT_TERMINAL_PROMPT: "0",
    GIT_OPTIONAL_LOCKS: "0",
  };
  run("git", ["init", "-q", `--template=${template}`], { cwd: worktree, env: gitEnv, quiet: true });
  run("git", ["add", "--all", "--", "."], { cwd: worktree, env: gitEnv, quiet: true });
  const tracked = run("git", ["ls-files", "-z"], { cwd: worktree, env: gitEnv, quiet: true })
    .split("\0").filter(Boolean);
  if (JSON.stringify(sorted(tracked)) !== JSON.stringify(sorted(closurePaths))) fail("synthetic Git tracked set 不是精確 closure");
  if (tracked.some((path) => path === "node_modules" || path.startsWith("node_modules/"))) fail("node_modules 不得被 synthetic Git 追蹤");
  run("git", [
    "-c", "user.name=Isolated Release Smoke",
    "-c", "user.email=smoke.invalid@localhost",
    "-c", "commit.gpgsign=false",
    "commit", "-q", "-m", "synthetic working-tree closure",
  ], { cwd: worktree, env: gitEnv, quiet: true });
  if (run("git", ["status", "--porcelain"], { cwd: worktree, env: gitEnv, quiet: true }).trim()) {
    fail("synthetic Git 在 build 前不是 clean");
  }
  return gitEnv;
}

function comparableManifest(manifest) {
  const copy = structuredClone(manifest);
  delete copy.generatedAt;
  delete copy.repository;
  for (const artifact of copy.artifacts ?? []) delete artifact.pdfSha256;
  return copy;
}

function artifactDifferenceSummary(baselineArtifacts, isolatedArtifacts) {
  const baselineById = new Map((baselineArtifacts ?? []).map((artifact) => [artifact.id, artifact]));
  const isolatedById = new Map((isolatedArtifacts ?? []).map((artifact) => [artifact.id, artifact]));
  const ids = sorted(new Set([...baselineById.keys(), ...isolatedById.keys()]));
  const differences = [];
  for (const id of ids) {
    const baseline = baselineById.get(id);
    const isolated = isolatedById.get(id);
    if (!baseline || !isolated) {
      differences.push(`${id}:${baseline ? "isolated missing" : "baseline missing"}`);
      continue;
    }
    const fields = sorted(new Set([...Object.keys(baseline), ...Object.keys(isolated)]));
    const changed = fields.filter((field) => JSON.stringify(baseline[field]) !== JSON.stringify(isolated[field]));
    if (changed.length > 0) {
      const values = changed.map((field) => {
        const left = baseline[field];
        const right = isolated[field];
        if (/Sha256$/u.test(field) && typeof left === "string" && typeof right === "string") {
          return `${field}[${left.slice(0, 12)}→${right.slice(0, 12)}]`;
        }
        return field;
      });
      differences.push(`${id}:${values.join("|")}`);
    }
  }
  return differences;
}

function rasterFingerprint(root) {
  const records = [];
  walkTree(root, (path, entry) => {
    if (entry.isSymbolicLink() || !entry.isFile()) fail(`PDF 等價檢查產生非一般檔案：${relative(root, path)}`);
    records.push([relative(root, path).split(sep).join("/"), sha256(path)]);
  });
  return records;
}

function assertPdfEquivalent(baselinePdf, isolatedPdf, tempRoot, label) {
  const baselineText = run("pdftotext", ["-bbox-layout", baselinePdf, "-"], { quiet: true });
  const isolatedText = run("pdftotext", ["-bbox-layout", isolatedPdf, "-"], { quiet: true });
  if (baselineText !== isolatedText) fail(`${label} 的文字與逐字座標不一致`);

  const safeLabel = label.replace(/[^a-z0-9._-]+/giu, "-");
  const equivalenceRoot = join(tempRoot, "pdf-equivalence");
  const comparisonRoot = join(equivalenceRoot, safeLabel);
  const baselineRaster = join(comparisonRoot, "baseline");
  const isolatedRaster = join(comparisonRoot, "isolated");
  for (const directory of [equivalenceRoot, comparisonRoot, baselineRaster, isolatedRaster]) {
    mkdirSync(directory, { mode: 0o700 });
    assertCanonicalDirectory(directory, `PDF 等價檢查 ${basename(directory)}`);
  }
  run("pdftoppm", ["-r", "96", "-gray", "-png", baselinePdf, join(baselineRaster, "page")], { quiet: true });
  run("pdftoppm", ["-r", "96", "-gray", "-png", isolatedPdf, join(isolatedRaster, "page")], { quiet: true });
  if (JSON.stringify(rasterFingerprint(baselineRaster)) !== JSON.stringify(rasterFingerprint(isolatedRaster))) {
    fail(`${label} 的 96 dpi 全頁灰階像素不一致`);
  }
}

function isolatedEnvironment(worktree, runtimeHome, runtimeTmp, runtimeCache, browserReal, browserCacheRoot) {
  const env = { ...process.env };
  for (const key of Object.keys(env)) {
    if (
      key === "OLDPWD"
      || key === "NODE_OPTIONS"
      || key === "NODE_PATH"
      || key === "INIT_CWD"
      || key === "PANDOC_DATA_DIR"
      || key.startsWith("HANDOUT_")
      || key.startsWith("GIT_")
      || key.startsWith("npm_")
    ) delete env[key];
  }
  env.PATH = (process.env.PATH ?? "")
    .split(delimiter)
    .filter(Boolean)
    .filter((entry) => {
      const resolved = resolve(entry);
      if (isInside(sourceRoot, resolved)) return false;
      try {
        return !isInside(sourceRoot, realpathSync(resolved));
      } catch {
        return true;
      }
    })
    .join(delimiter);
  return {
    ...env,
    PWD: worktree,
    HOME: runtimeHome,
    TMPDIR: runtimeTmp,
    TMP: runtimeTmp,
    TEMP: runtimeTmp,
    XDG_CACHE_HOME: runtimeCache,
    ...(browserCacheRoot ? { PLAYWRIGHT_BROWSERS_PATH: browserCacheRoot } : {}),
    PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD: "1",
    HANDOUT_CHROME_BIN: browserReal,
  };
}

function currentBrowserForBaseline(baseline) {
  const playwrightBrowser = run(
    process.execPath,
    ["-e", "process.stdout.write(require('playwright').chromium.executablePath())"],
    { cwd: sourceRoot, quiet: true },
  ).trim();
  const candidates = [
    process.env.HANDOUT_CHROME_BIN,
    playwrightBrowser,
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
  ].filter(Boolean);
  for (const candidate of candidates) {
    try {
      accessSync(candidate, constants.X_OK);
      const canonical = realpathSync(candidate);
      if (sha256(canonical) === baseline.manifest.tools?.chromiumExecutableSha256) return canonical;
    } catch {
      // Try the next production-priority candidate.
    }
  }
  fail("找不到與 baseline tools hash 相同的 Chromium executable");
}

function runIsolated(baseline, temp) {
  const worktree = join(temp.root, "worktree");
  mkdirSync(worktree, { mode: 0o700 });
  assertCanonicalDirectory(worktree, "fixture worktree");
  for (const [path, digest] of baseline.closure) {
    copyClosureFile(worktree, path, digest, baseline.allowedPrivatePaths);
  }
  assertPhysicalClosure(worktree, baseline.closure.keys());
  assertNoForbiddenDirectories(worktree, baseline.allowedPrivatePaths);
  copyNodeModules(worktree);
  assertNoForbiddenDirectories(worktree, baseline.allowedPrivatePaths);

  const runtimeHome = join(temp.root, "runtime-home");
  const runtimeTmp = join(temp.root, "runtime-tmp");
  const runtimeCache = join(temp.root, "runtime-cache");
  for (const directory of [runtimeHome, runtimeTmp, runtimeCache]) mkdirSync(directory, { mode: 0o700 });

  const browserReal = currentBrowserForBaseline(baseline);
  const revisionDirectory = browserReal.split(sep).findIndex((segment) => /^chromium-\d+$/u.test(segment));
  const browserCacheRoot = revisionDirectory > 0
    ? browserReal.split(sep).slice(0, revisionDirectory).join(sep) || sep
    : undefined;
  const env = isolatedEnvironment(
    worktree,
    runtimeHome,
    runtimeTmp,
    runtimeCache,
    browserReal,
    browserCacheRoot,
  );
  const gitEnv = initializeSyntheticRepository(worktree, sorted(baseline.closure.keys()), env, temp.root);
  const publication = join(worktree, "tools", "publication.mjs");
  process.stdout.write(`隔離建置：${baseline.setId}，${baseline.closure.size} 個 closure 檔案\n`);
  run(process.execPath, [publication, "preflight", "--set", baseline.setId], { cwd: worktree, env: gitEnv });
  run(process.execPath, [publication, "release", "--set", baseline.setId], { cwd: worktree, env: gitEnv });
  run(process.execPath, [publication, "verify", "--set", baseline.setId], { cwd: worktree, env: gitEnv });

  if (run("git", ["status", "--porcelain"], { cwd: worktree, env: gitEnv, quiet: true }).trim()) {
    fail("synthetic Git 在 release/verify 後不是 clean");
  }
  const isolatedDist = join(worktree, "dist", baseline.setId);
  const isolatedManifest = readJson(join(isolatedDist, "manifest.json"), "isolated manifest");
  if (JSON.stringify(Object.keys(isolatedManifest.repository ?? {}).sort()) !== JSON.stringify(["commit", "dirty"])) {
    fail("isolated release manifest repository schema 無效");
  }
  const isolatedHead = run("git", ["rev-parse", "HEAD"], { cwd: worktree, env: gitEnv, quiet: true }).trim();
  if (isolatedManifest.repository.commit !== isolatedHead || isolatedManifest.repository.dirty !== false) {
    fail("isolated release manifest 必須綁定 synthetic HEAD 且記錄 dirty=false");
  }
  const isolatedComparable = comparableManifest(isolatedManifest);
  const baselineComparable = comparableManifest(baseline.manifest);
  if (JSON.stringify(isolatedComparable) !== JSON.stringify(baselineComparable)) {
    const changed = sorted(new Set([
      ...Object.keys(isolatedComparable),
      ...Object.keys(baselineComparable),
    ])).filter((key) => JSON.stringify(isolatedComparable[key]) !== JSON.stringify(baselineComparable[key]));
    const artifactDetail = changed.includes("artifacts")
      ? artifactDifferenceSummary(baselineComparable.artifacts, isolatedComparable.artifacts)
      : [];
    const detail = artifactDetail.length > 0 ? `（${artifactDetail.join(", ")}）` : "";
    fail(`isolated manifest 除 generatedAt/repository 外與 baseline 語義不一致：${changed.join(", ")}${detail}`);
  }
  const isolatedExpectedSums = `${sorted(isolatedManifest.artifacts.flatMap((artifact) => [
    `${artifact.htmlSha256}  ${artifact.html}`,
    `${artifact.pdfSha256}  ${artifact.pdf}`,
  ])).join("\n")}\n`;
  if (readFileSync(join(isolatedDist, "SHA256SUMS"), "utf8") !== isolatedExpectedSums) {
    fail("isolated SHA256SUMS 與 isolated manifest 不一致");
  }
  for (const artifact of baseline.manifest.artifacts) {
    const baselineHtml = readFileSync(join(baseline.distDir, artifact.html));
    const isolatedHtml = readFileSync(join(isolatedDist, artifact.html));
    if (!baselineHtml.equals(isolatedHtml)) fail(`${artifact.html} 不是 byte-identical`);

    const baselinePdf = join(baseline.distDir, artifact.pdf);
    const isolatedPdf = join(isolatedDist, artifact.pdf);
    if (!readFileSync(baselinePdf).equals(readFileSync(isolatedPdf))) {
      assertPdfEquivalent(baselinePdf, isolatedPdf, temp.root, artifact.id);
    }
  }
  assertNoForbiddenDirectories(worktree, baseline.allowedPrivatePaths);
  process.stdout.write(`通過：${baseline.manifest.artifacts.length} 份 HTML 均 byte-identical；PDF 均 byte-identical 或逐字座標與全頁像素一致\n`);
}

function main() {
  let operationError;
  let cleanupError;
  let protectedError;
  let closureError;
  let temp;
  let baseline;
  const protectedBefore = protectedSourceState();
  try {
    baseline = loadBaseline(parseCli());
    temp = makePrivateOuter();
    runIsolated(baseline, temp);
  } catch (error) {
    operationError = error;
  } finally {
    if (temp) {
      try {
        safeCleanup(temp);
      } catch (error) {
        cleanupError = error;
      }
    }
    try {
      assertSame(protectedBefore, protectedSourceState(), "主 repository 的 dist/output/tmp/node_modules");
    } catch (error) {
      protectedError = error;
    }
    if (baseline) {
      try {
        for (const [path, digest] of baseline.closure) {
          if (sha256(join(sourceRoot, path)) !== digest) fail(`主 repository closure 在 smoke 期間改變：${path}`);
        }
      } catch (error) {
        closureError = error;
      }
    }
  }

  const errors = [operationError, cleanupError, protectedError, closureError].filter(Boolean);
  if (errors.length > 0) {
    process.stderr.write(`isolated release smoke 失敗：${errors.map((error) => error.message).join("\n")}\n`);
    process.exit(1);
  }
}

if (process.argv[1] && realpathSync(process.argv[1]) === fileURLToPath(import.meta.url)) main();
