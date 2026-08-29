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
  rmSync,
} from "node:fs";
import { tmpdir } from "node:os";
import { basename, dirname, isAbsolute, join, relative, resolve, sep } from "node:path";
import { fileURLToPath } from "node:url";
import {
  FIGURE_MANIFEST_RELATIVE,
  canonicalManifestFile,
  loadFigureManifest,
  sha256File,
} from "./figure-manifest.mjs";

const scriptDir = dirname(fileURLToPath(import.meta.url));
const repoRoot = realpathSync(resolve(scriptDir, ".."));
const registryRelative = "publishing/sets.json";

function fail(message) {
  throw new Error(message);
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

function canonicalJson(relativePath, label) {
  const path = canonicalManifestFile(repoRoot, relativePath, null, label);
  const text = readFileSync(path, "utf8");
  let value;
  try {
    value = JSON.parse(text);
  } catch (error) {
    fail(`${label} 不是合法 JSON：${error.message}`);
  }
  if (text !== `${JSON.stringify(value, null, 2)}\n`) {
    fail(`${label} 必須是 canonical JSON；拒絕 duplicate key 或尾端內容`);
  }
  return value;
}

function registeredFigureClosure(manifestOutputs) {
  const registry = canonicalJson(registryRelative, "publishing registry");
  if (!registry.sets || typeof registry.sets !== "object" || Array.isArray(registry.sets)) {
    fail("publishing registry 缺少 sets object");
  }

  const sources = new Set();
  for (const [setId, set] of Object.entries(registry.sets)) {
    if (!set || !Array.isArray(set.documents)) fail(`${setId}.documents 必須是 array`);
    for (const document of set.documents) {
      if (!document || typeof document.source !== "string") fail(`${setId} document source 無效`);
      sources.add(document.source);
    }
  }
  if (sources.size === 0) fail("publishing registry 沒有 document source");

  const chapterDirectories = new Set();
  const referencedAssets = new Set();
  for (const sourceRelative of sources) {
    if (!sourceRelative.startsWith("content/") || basename(sourceRelative) !== "學生講義.md") {
      fail(`figure gate 只接受 registered 學生稿：${sourceRelative}`);
    }
    const sourcePath = canonicalManifestFile(repoRoot, sourceRelative, null, sourceRelative);
    const chapterRelative = dirname(sourceRelative).split(sep).join("/");
    chapterDirectories.add(chapterRelative);
    const markdown = readFileSync(sourcePath, "utf8");
    const images = [...markdown.matchAll(/!\[[^\]\r\n]*\]\(([^)\r\n]+)\)/gu)];
    for (const match of images) {
      let target = match[1].trim().split(/\s+/u)[0];
      if (target.startsWith("<") && target.endsWith(">")) target = target.slice(1, -1);
      if (!/^assets\/[^/\s]+\.svg$/u.test(target)) {
        fail(`${sourceRelative} 含 figure gate 不接受的圖片目標：${target}`);
      }
      referencedAssets.add(`${chapterRelative}/${target}`);
    }
  }

  const physicalAssets = new Set();
  for (const chapterRelative of chapterDirectories) {
    const assetsPath = join(repoRoot, chapterRelative, "assets");
    assertCanonicalDirectory(assetsPath, `${chapterRelative}/assets`);
    for (const name of sorted(readdirSync(assetsPath))) {
      const assetRelative = `${chapterRelative}/assets/${name}`;
      if (!name.endsWith(".svg")) fail(`registered 章內 assets 只允許 SVG：${assetRelative}`);
      canonicalManifestFile(repoRoot, assetRelative, null, assetRelative);
      physicalAssets.add(assetRelative);
    }
  }

  const manifestAssetSet = new Set(manifestOutputs.map((record) => record.path));
  const expected = JSON.stringify(sorted(manifestAssetSet));
  if (JSON.stringify(sorted(referencedAssets)) !== expected) {
    fail("figures manifest outputs 與 registered 學生稿實際圖片引用不一致");
  }
  if (JSON.stringify(sorted(physicalAssets)) !== expected) {
    fail("figures manifest outputs 與 registered 章內實體 SVG closure 不一致");
  }
  return { sources: sorted(sources), chapterDirectories: sorted(chapterDirectories) };
}

function snapshotFiles(paths) {
  return Object.fromEntries(sorted(paths).map((path) => {
    const absolute = canonicalManifestFile(repoRoot, path, null, path);
    const stat = lstatSync(absolute);
    return [path, { mode: stat.mode, size: stat.size, sha256: sha256File(absolute) }];
  }));
}

function makePrivateTemp() {
  const parent = realpathSync(tmpdir());
  assertCanonicalDirectory(parent, "system temp root");
  if (isInside(repoRoot, parent)) fail("system temp root 不得位於 repository 內");
  let root;
  try {
    root = realpathSync(mkdtempSync(join(parent, "highschool-figure-repro-")));
    chmodSync(root, 0o700);
    if (dirname(root) !== parent) fail("figure repro temp 不是 system temp 的直接子目錄");
    const identity = assertCanonicalDirectory(root, "figure repro temp");
    if ((lstatSync(root).mode & 0o777) !== 0o700) fail("figure repro temp 權限必須是 0700");
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
  if (dirname(temp.root) !== temp.parent) fail("拒絕清理非 system temp 直接子目錄");
  const identity = assertCanonicalDirectory(temp.root, "figure repro cleanup");
  if (identity.dev !== temp.identity.dev || identity.ino !== temp.identity.ino) {
    fail("figure repro temp identity 改變，拒絕清理");
  }
  rmSync(temp.root, { recursive: true, force: false });
}

function ensureDirectory(root, relativeDirectory) {
  let current = root;
  if (!relativeDirectory || relativeDirectory === ".") return current;
  for (const segment of relativeDirectory.split("/")) {
    const next = join(current, segment);
    if (!existsSync(next)) mkdirSync(next, { mode: 0o700 });
    assertCanonicalDirectory(next, `fixture/${relative(root, next)}`);
    current = next;
  }
  return current;
}

function copyClosureFile(worktree, relativePath, expectedSha256) {
  const source = canonicalManifestFile(repoRoot, relativePath, expectedSha256, relativePath);
  const before = sha256File(source);
  ensureDirectory(worktree, dirname(relativePath).split(sep).join("/"));
  const destination = join(worktree, relativePath);
  if (existsSync(destination)) fail(`fixture 目的檔重複：${relativePath}`);
  copyFileSync(source, destination, constants.COPYFILE_EXCL);
  chmodSync(destination, 0o600);
  const entry = lstatSync(destination);
  if (entry.isSymbolicLink() || !entry.isFile() || realpathSync(destination) !== destination) {
    fail(`fixture copy 不是 canonical 一般檔案：${relativePath}`);
  }
  if (sha256File(destination) !== before || sha256File(source) !== before) {
    fail(`copy 前後 hash 不一致：${relativePath}`);
  }
}

function walkFixture(root) {
  const files = [];
  const directories = [];
  function visit(directory) {
    for (const name of sorted(readdirSync(directory))) {
      const path = join(directory, name);
      const entry = lstatSync(path);
      const rel = relative(root, path).split(sep).join("/");
      if (entry.isSymbolicLink()) fail(`fixture 不得含 symlink：${rel}`);
      if (entry.isDirectory()) {
        if (realpathSync(path) !== path) fail(`fixture 目錄不是 canonical：${rel}`);
        directories.push(rel);
        visit(path);
      } else if (entry.isFile()) {
        if (realpathSync(path) !== path) fail(`fixture 檔案不是 canonical：${rel}`);
        files.push(rel);
      } else {
        fail(`fixture 不得含特殊檔：${rel}`);
      }
    }
  }
  visit(root);
  return { files: sorted(files), directories: sorted(directories) };
}

function expectedDirectories(paths) {
  const directories = new Set();
  for (const path of paths) {
    const segments = dirname(path).split("/").filter((segment) => segment && segment !== ".");
    let current = "";
    for (const segment of segments) {
      current = current ? `${current}/${segment}` : segment;
      directories.add(current);
    }
  }
  return sorted(directories);
}

function assertPhysicalClosure(worktree, expectedFiles) {
  const tree = walkFixture(worktree);
  const files = sorted(expectedFiles);
  if (JSON.stringify(tree.files) !== JSON.stringify(files)) {
    fail(`fixture 一般檔集合不是精確 closure：\nexpected=${files.join("\n")}\nactual=${tree.files.join("\n")}`);
  }
  const directories = expectedDirectories(files);
  if (JSON.stringify(tree.directories) !== JSON.stringify(directories)) {
    fail("fixture 目錄集合不是精確 closure");
  }
}

function run(command, args, { cwd, env, quiet = false } = {}) {
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

function pythonExecutable() {
  const candidate = join(repoRoot, ".venv", "bin", "python");
  let canonical;
  try {
    canonical = realpathSync(candidate);
    accessSync(canonical, constants.X_OK);
  } catch (error) {
    fail(`figure repro 需要 repository .venv/bin/python：${error.message}`);
  }
  if (!lstatSync(canonical).isFile()) fail("figure Python runtime 必須解析到一般檔案");
  // Execute through the venv path so Python retains its pyvenv.cfg/site-packages.
  return candidate;
}

function isolatedEnvironment(runtimeRoot, worktree) {
  if (!existsSync(runtimeRoot)) mkdirSync(runtimeRoot, { mode: 0o700 });
  assertCanonicalDirectory(runtimeRoot, "figure runtime root");
  const paths = {};
  for (const name of ["tmp", "xdg", "mpl"]) {
    paths[name] = join(runtimeRoot, name);
    mkdirSync(paths[name], { mode: 0o700 });
    assertCanonicalDirectory(paths[name], `runtime ${name}`);
  }
  return {
    // Figure output is intentionally verified only for this machine/runtime.
    // Keep the real HOME so figlib resolves the same local font candidate used
    // by the committed SVGs; caches and temporary writes remain isolated.
    ...(process.env.HOME ? { HOME: process.env.HOME } : {}),
    TMPDIR: paths.tmp,
    TMP: paths.tmp,
    TEMP: paths.tmp,
    XDG_CACHE_HOME: paths.xdg,
    MPLCONFIGDIR: paths.mpl,
    MPLBACKEND: "Agg",
    PYTHONDONTWRITEBYTECODE: "1",
    PYTHONNOUSERSITE: "1",
    PYTHONHASHSEED: "0",
    PYTHONSAFEPATH: "1",
    SOURCE_DATE_EPOCH: "0",
    TZ: "UTC",
    LANG: "C.UTF-8",
    LC_ALL: "C.UTF-8",
    PWD: worktree,
    ...(process.env.SYSTEMROOT ? { SYSTEMROOT: process.env.SYSTEMROOT } : {}),
  };
}

function probeRuntime(python, runtime, runtimeRoot) {
  const probeWorktree = runtimeRoot;
  const env = isolatedEnvironment(join(runtimeRoot, "probe-runtime"), probeWorktree);
  const program = [
    "import json, platform",
    "import matplotlib, numpy",
    "from matplotlib import ft2font",
    "print(json.dumps({'implementation': platform.python_implementation(), 'python': platform.python_version(), 'numpy': numpy.__version__, 'matplotlib': matplotlib.__version__, 'freetype': ft2font.__freetype_version__}, sort_keys=True))",
  ].join("; ");
  const stdout = run(python, ["-c", program], { cwd: probeWorktree, env, quiet: true }).trim();
  let actual;
  try {
    actual = JSON.parse(stdout);
  } catch {
    fail(`figure runtime probe 非 JSON：${stdout}`);
  }
  const expected = Object.fromEntries(["implementation", "python", "numpy", "matplotlib", "freetype"].map((key) => [key, runtime[key]]));
  if (Object.keys(expected).some((key) => actual[key] !== expected[key]) || Object.keys(actual).length !== Object.keys(expected).length) {
    fail(`figure runtime 版本不符：manifest=${JSON.stringify(expected)} actual=${JSON.stringify(actual)}`);
  }
}

function runRound(label, temp, python, manifest) {
  const roundRoot = join(temp.root, label);
  const worktree = join(roundRoot, "worktree");
  const runtimeRoot = join(roundRoot, "runtime");
  mkdirSync(roundRoot, { mode: 0o700 });
  mkdirSync(worktree, { mode: 0o700 });
  mkdirSync(runtimeRoot, { mode: 0o700 });
  assertCanonicalDirectory(worktree, `${label} worktree`);
  assertCanonicalDirectory(runtimeRoot, `${label} runtime`);

  const manifestSha256 = sha256File(join(repoRoot, FIGURE_MANIFEST_RELATIVE));
  copyClosureFile(worktree, FIGURE_MANIFEST_RELATIVE, manifestSha256);
  for (const input of manifest.allInputs) copyClosureFile(worktree, input.path, input.sha256);

  const initialFiles = [FIGURE_MANIFEST_RELATIVE, ...manifest.allInputs.map((record) => record.path)];
  assertPhysicalClosure(worktree, initialFiles);
  const env = isolatedEnvironment(runtimeRoot, worktree);

  for (const generator of manifest.generators) {
    process.stdout.write(`${label}：${generator.id}\n`);
    run(python, generator.command.slice(1), { cwd: worktree, env, quiet: true });
  }

  const finalFiles = [...initialFiles, ...manifest.allOutputs.map((record) => record.path)];
  assertPhysicalClosure(worktree, finalFiles);
  for (const input of manifest.allInputs) {
    if (sha256File(join(worktree, input.path)) !== input.sha256) fail(`${label} generator 修改 input：${input.path}`);
  }
  const outputs = new Map();
  for (const output of manifest.allOutputs) {
    const path = join(worktree, output.path);
    const text = readFileSync(path, "utf8");
    if (!text.startsWith("<?xml") || !text.includes("<svg") || /<(?:script|foreignObject)\b/iu.test(text)) {
      fail(`${label} 產生非安全自足 SVG：${output.path}`);
    }
    if (
      text.includes(repoRoot)
      || text.includes(temp.root)
      || /(?:href|src)\s*=\s*["'](?:file:|https?:\/\/)/iu.test(text)
    ) {
      fail(`${label} SVG 含外部／本機資源：${output.path}`);
    }
    outputs.set(output.path, readFileSync(path));
  }
  return outputs;
}

function compareOutputs(first, second, manifest) {
  for (const output of manifest.allOutputs) {
    const firstBytes = first.get(output.path);
    const secondBytes = second.get(output.path);
    if (!firstBytes?.equals(secondBytes)) fail(`兩輪 SVG 不是 byte-identical：${output.path}`);
    const actualSha256 = createHash("sha256").update(firstBytes).digest("hex");
    if (actualSha256 !== output.sha256) {
      fail(`重生 SVG 與 manifest/committed bytes 不同：${output.path} expected=${output.sha256} actual=${actualSha256}`);
    }
    if (!firstBytes.equals(readFileSync(join(repoRoot, output.path)))) {
      fail(`重生 SVG 與 committed asset 不同：${output.path}`);
    }
  }
}

function parseCli() {
  if (process.argv.length !== 2) fail("用法：node tools/figure-repro.mjs（不接受參數）");
}

function main() {
  let operationError;
  let cleanupError;
  let sourceError;
  let temp;
  let protectedPaths;
  let protectedBefore;
  try {
    parseCli();
    const { manifest } = loadFigureManifest(repoRoot);
    const coverage = registeredFigureClosure(manifest.allOutputs);
    protectedPaths = new Set([
      FIGURE_MANIFEST_RELATIVE,
      registryRelative,
      ...coverage.sources,
      ...manifest.allInputs.map((record) => record.path),
      ...manifest.allOutputs.map((record) => record.path),
    ]);
    protectedBefore = snapshotFiles(protectedPaths);
    const python = pythonExecutable();
    temp = makePrivateTemp();
    probeRuntime(python, manifest.runtime, temp.root);
    process.stdout.write(`figure repro：${coverage.chapterDirectories.length} 章／${manifest.allOutputs.length} SVG／${manifest.generators.length} generators\n`);
    const first = runRound("round-1", temp, python, manifest);
    const second = runRound("round-2", temp, python, manifest);
    compareOutputs(first, second, manifest);
    process.stdout.write(`figure repro 通過：${manifest.allOutputs.length} SVG 兩輪與 committed bytes 完全一致\n`);
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
    if (protectedPaths && protectedBefore) {
      try {
        const protectedAfter = snapshotFiles(protectedPaths);
        if (JSON.stringify(protectedBefore) !== JSON.stringify(protectedAfter)) {
          fail("figure repro 期間主 repository closure 改變");
        }
      } catch (error) {
        sourceError = error;
      }
    }
  }

  const errors = [operationError, cleanupError, sourceError].filter(Boolean);
  if (errors.length > 0) {
    process.stderr.write(`figure repro 失敗：${errors.map((error) => error.message).join("\n")}\n`);
    process.exit(1);
  }
}

if (process.argv[1] && realpathSync(process.argv[1]) === fileURLToPath(import.meta.url)) main();
