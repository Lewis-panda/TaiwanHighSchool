#!/usr/bin/env node

import { spawnSync } from "node:child_process";
import { createHash } from "node:crypto";
import {
  chmodSync,
  constants as fsConstants,
  copyFileSync,
  existsSync,
  lstatSync,
  mkdtempSync,
  mkdirSync,
  readFileSync,
  readdirSync,
  realpathSync,
  renameSync,
  rmSync,
  statSync,
  writeFileSync,
} from "node:fs";
import { release as osRelease } from "node:os";
import { basename, dirname, isAbsolute, join, relative, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import {
  expectedDocumentId,
  leadingRegisteredChapterCode,
  resolveCourseIdentity,
} from "./course-identity.mjs";
import { loadFigureManifest } from "./figure-manifest.mjs";
import {
  assertSafeCssText,
  assertSafeHtmlText,
  assertSafeSourceText,
  assertSafeSvgText,
  inspectPandocAstSafety,
} from "./publication-safety.mjs";
import { assertRepositoryPrivacyBoundary } from "./repository-privacy.mjs";

const scriptDir = dirname(fileURLToPath(import.meta.url));
const repoRoot = realpathSync(resolve(scriptDir, ".."));
const registryPath = join(repoRoot, "publishing", "sets.json");
const markdownFormat = "markdown+yaml_metadata_block+fenced_divs+tex_math_dollars+smart";
const pandoc = process.env.HANDOUT_PANDOC_BIN ?? "pandoc";
const verificationModel = "current-source-and-pipeline-consistency-not-a-digital-signature";
const artifactKeys = [
  "assets",
  "audience",
  "html",
  "htmlSha256",
  "id",
  "pages",
  "pdf",
  "pdfSha256",
  "slug",
  "source",
  "sourceSha256",
  "title",
].sort();
const manifestKeys = [
  "artifacts",
  "description",
  "generatedAt",
  "pipeline",
  "repository",
  "schemaVersion",
  "set",
  "status",
  "tools",
  "verificationModel",
].sort();
const pipelineBaseFiles = [
  ".gitignore",
  "tools/course-identity.mjs",
  "tools/figure-manifest.mjs",
  "tools/figure-manifest.test.mjs",
  "tools/figure-repro.mjs",
  "tools/publication.mjs",
  "tools/build-handout.mjs",
  "tools/publication-safety.mjs",
  "tools/normalize-chromium-pdf.mjs",
  "tools/check-handout.mjs",
  "tools/repository-privacy.mjs",
  "publishing/sets.json",
  "publishing/figures.json",
  "templates/handout.html",
  "styles/handout.css",
  "assets/fonts/README.md",
  "assets/fonts/provenance.json",
  "assets/fonts/NotoSansTC-OFL.txt",
  "assets/fonts/OFL.txt",
  "package.json",
  "package-lock.json",
];
const frontmatterKeys = [
  "audience",
  "course",
  "output_slug",
  "scope",
  "subject",
  "subtitle",
  "title",
  "title-prefix",
  "updated",
].sort();

function fail(message) {
  throw new Error(message);
}

function run(command, args, { quiet = false, includeStderr = false } = {}) {
  const result = spawnSync(command, args, {
    cwd: repoRoot,
    encoding: "utf8",
    maxBuffer: 64 * 1024 * 1024,
  });
  if (result.error) fail(`${command} 無法執行：${result.error.message}`);
  if (result.status !== 0) {
    const detail = [result.stdout, result.stderr].filter(Boolean).join("\n").trim();
    fail(`${command} 結束碼 ${result.status}${detail ? `：\n${detail}` : ""}`);
  }
  if (!quiet && result.stdout) process.stdout.write(result.stdout);
  return includeStderr
    ? `${result.stdout ?? ""}${result.stderr ?? ""}`
    : (result.stdout ?? "");
}

function commandVersion(command, args) {
  try {
    return run(command, args, { quiet: true, includeStderr: true }).trim().split("\n")[0] || "unknown";
  } catch {
    return "unavailable";
  }
}

function toolState() {
  let playwrightVersion = "unavailable";
  let playwrightChromium;
  try {
    playwrightVersion = run(process.execPath, ["-e", "process.stdout.write(require('playwright/package.json').version)"], { quiet: true }).trim();
    playwrightChromium = run(process.execPath, ["-e", "process.stdout.write(require('playwright').chromium.executablePath())"], { quiet: true }).trim();
  } catch {
    // build-handout 會在缺少 Playwright 時拒絕建置；這裡只產生可比較的狀態。
  }
  const chromiumExecutable = [
    process.env.HANDOUT_CHROME_BIN,
    playwrightChromium,
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
  ].find((candidate) => candidate && existsSync(candidate));
  const chromiumRevision = chromiumExecutable
    ? chromiumExecutable.split(/[\\/]/u).find((segment) => /^chromium-\d+$/u.test(segment)) ?? "custom"
    : "unavailable";
  let chromiumExecutableSha256 = "unavailable";
  if (chromiumExecutable) {
    try {
      const canonical = realpathSync(chromiumExecutable);
      if (lstatSync(canonical).isFile()) chromiumExecutableSha256 = sha256(canonical);
    } catch {
      // 建置工具本身會對不可用的瀏覽器 fail closed；這裡保留可比較狀態。
    }
  }
  return {
    node: process.version,
    platform: `${process.platform}-${process.arch}`,
    osRelease: osRelease(),
    git: commandVersion("git", ["--version"]),
    pandoc: commandVersion(pandoc, ["--version"]),
    poppler: commandVersion("pdfinfo", ["-v"]),
    playwright: playwrightVersion,
    playwrightChromiumRevision: chromiumRevision,
    chromium: chromiumExecutable
      ? commandVersion(chromiumExecutable, ["--version"])
      : "unavailable",
    chromiumExecutableSha256,
  };
}

function repositoryState() {
  return {
    commit: commandVersion("git", ["rev-parse", "HEAD"]),
    dirty: run("git", ["status", "--porcelain"], { quiet: true }).trim().length > 0,
  };
}

function findPillowPython() {
  const candidates = [...new Set([
    process.env.HANDOUT_PYTHON_BIN,
    "python3",
    "python",
  ].filter(Boolean))];
  for (const candidate of candidates) {
    const result = spawnSync(candidate, ["-c", "import PIL"], {
      cwd: repoRoot,
      encoding: "utf8",
    });
    if (!result.error && result.status === 0) return candidate;
  }
  fail("review:render 需要可匯入 Pillow 的 Python；請安裝 Pillow 或設定 HANDOUT_PYTHON_BIN");
}

function sha256(path) {
  return createHash("sha256").update(readFileSync(path)).digest("hex");
}

function compareCodePoints(left, right) {
  return left < right ? -1 : left > right ? 1 : 0;
}

function parseJsonWithoutDuplicateKeys(text, label) {
  let index = 0;

  function syntax(message) {
    fail(`${label} JSON 無效（位置 ${index}）：${message}`);
  }

  function skipWhitespace() {
    while (index < text.length && /\s/u.test(text[index])) index += 1;
  }

  function parseString() {
    if (text[index] !== '"') syntax("預期字串");
    const start = index;
    index += 1;
    let closed = false;
    while (index < text.length) {
      const character = text[index];
      index += 1;
      if (character === '"') {
        closed = true;
        break;
      }
      if (character === "\\") {
        if (index >= text.length) syntax("字串 escape 不完整");
        index += 1;
      }
    }
    if (!closed) syntax("字串未結束");
    try {
      return JSON.parse(text.slice(start, index));
    } catch (error) {
      syntax(error.message);
    }
  }

  function parseArray() {
    index += 1;
    skipWhitespace();
    if (text[index] === "]") {
      index += 1;
      return;
    }
    while (index < text.length) {
      parseValue();
      skipWhitespace();
      if (text[index] === "]") {
        index += 1;
        return;
      }
      if (text[index] !== ",") syntax("陣列預期逗號或右括號");
      index += 1;
      skipWhitespace();
    }
    syntax("陣列未結束");
  }

  function parseObject() {
    index += 1;
    skipWhitespace();
    const keys = new Set();
    if (text[index] === "}") {
      index += 1;
      return;
    }
    while (index < text.length) {
      const key = parseString();
      if (keys.has(key)) syntax(`物件 key 重複：${key}`);
      keys.add(key);
      skipWhitespace();
      if (text[index] !== ":") syntax("物件 key 後缺少冒號");
      index += 1;
      parseValue();
      skipWhitespace();
      if (text[index] === "}") {
        index += 1;
        return;
      }
      if (text[index] !== ",") syntax("物件預期逗號或右括號");
      index += 1;
      skipWhitespace();
    }
    syntax("物件未結束");
  }

  function parseValue() {
    skipWhitespace();
    const character = text[index];
    if (character === '"') {
      parseString();
      return;
    }
    if (character === "{") {
      parseObject();
      return;
    }
    if (character === "[") {
      parseArray();
      return;
    }
    for (const literal of ["true", "false", "null"]) {
      if (text.startsWith(literal, index)) {
        index += literal.length;
        return;
      }
    }
    const number = text.slice(index).match(/^-?(?:0|[1-9]\d*)(?:\.\d+)?(?:[eE][+-]?\d+)?/u)?.[0];
    if (!number) syntax("無法辨識 value");
    index += number.length;
  }

  parseValue();
  skipWhitespace();
  if (index !== text.length) syntax("根 value 後仍有資料");
  try {
    return JSON.parse(text);
  } catch (error) {
    syntax(error.message);
  }
}

function isInside(root, target) {
  const rel = relative(root, target);
  return rel === "" || (!isAbsolute(rel) && rel !== ".." && !rel.startsWith(`..${process.platform === "win32" ? "\\" : "/"}`));
}

function lstatIfPresent(path) {
  try {
    return lstatSync(path);
  } catch (error) {
    if (error?.code === "ENOENT") return undefined;
    throw error;
  }
}

function assertDirectChild(root, target, label) {
  if (dirname(target) !== root || target === root) fail(`${label} 不是受控 root 的直接子項目`);
}

function assertCanonicalDirectory(path, label) {
  const entry = lstatIfPresent(path);
  if (!entry) fail(`${label} 不存在`);
  if (entry.isSymbolicLink() || !entry.isDirectory()) fail(`${label} 必須是一般目錄，不得是 symlink`);
  if (realpathSync(path) !== path) fail(`${label} 不是預期 canonical 目錄`);
  return { dev: entry.dev, ino: entry.ino, mode: entry.mode };
}

function ensureDirectCanonicalDirectory(path, parent, label, { create = false, mode = 0o700 } = {}) {
  assertDirectChild(parent, path, label);
  assertCanonicalDirectory(parent, `${label} 的 parent`);
  if (!lstatIfPresent(path)) {
    if (!create) fail(`${label} 不存在`);
    try {
      mkdirSync(path, { mode });
    } catch (error) {
      if (error?.code !== "EEXIST") throw error;
    }
  }
  return assertCanonicalDirectory(path, label);
}

function sameIdentity(left, right) {
  return left.dev === right.dev && left.ino === right.ino;
}

function assertDirectoryIdentity(path, identity, label) {
  const current = assertCanonicalDirectory(path, label);
  if (!sameIdentity(current, identity)) fail(`${label} identity 已改變，拒絕繼續`);
  return current;
}

function assertAbsent(path, label) {
  if (lstatIfPresent(path)) fail(`${label} 已存在；拒絕覆寫未知項目`);
}

function safeRemoveOwnedDirectory(path, root, identity, label) {
  assertDirectChild(root, path, label);
  assertCanonicalDirectory(root, `${label} 的受控 root`);
  if (!lstatIfPresent(path)) return;
  assertDirectoryIdentity(path, identity, label);
  rmSync(path, { recursive: true, force: false });
}

function assertRegularDirectFile(path, root, label) {
  assertDirectChild(root, path, label);
  const entry = lstatIfPresent(path);
  if (!entry || entry.isSymbolicLink() || !entry.isFile()) fail(`${label} 必須是一般檔案，不得是 symlink`);
  if (realpathSync(path) !== path) fail(`${label} 不是 canonical 檔案`);
  return path;
}

function validateRelativePath(value, label, { mustExist = true } = {}) {
  if (typeof value !== "string" || !value) fail(`${label} 必須是非空字串`);
  if (value !== value.normalize("NFC")) fail(`${label} 必須使用 NFC Unicode：${value}`);
  if (isAbsolute(value) || value.includes("\\")) fail(`${label} 必須是 repo-relative POSIX 路徑：${value}`);
  if (/[\u0000-\u001f\u007f]/u.test(value)) fail(`${label} 含控制字元`);
  const segments = value.split("/");
  if (segments.some((part) => !part || part === "." || part === "..")) fail(`${label} 含不安全片段：${value}`);
  if (segments[0] === "高中教材") fail(`${label} 不得指向本機參考教材：${value}`);
  const resolved = resolve(repoRoot, value);
  if (!isInside(repoRoot, resolved)) fail(`${label} 逃離 repository：${value}`);
  if (mustExist) {
    if (!existsSync(resolved)) fail(`${label} 不存在：${value}`);
    const real = realpathSync(resolved);
    if (!isInside(repoRoot, real)) fail(`${label} 的 symlink 逃離 repository：${value}`);
    if (real !== resolved) fail(`${label} 的路徑含 symlink 或非 canonical 片段：${value}`);
    const privateRoot = join(repoRoot, "高中教材");
    if (existsSync(privateRoot) && isInside(realpathSync(privateRoot), real)) {
      fail(`${label} 不得指向本機參考教材：${value}`);
    }
  }
  return resolved;
}

function strictFrontmatter(markdown, label) {
  const frontmatter = markdown.match(/^---\s*\n([\s\S]*?)\n---\s*(?:\n|$)/u);
  if (!frontmatter) fail(`${label} 缺少 YAML frontmatter`);
  const values = {};
  for (const [index, rawLine] of frontmatter[1].split(/\r?\n/u).entries()) {
    if (!rawLine.trim()) continue;
    if (/^\s/u.test(rawLine)) fail(`${label} frontmatter 第 ${index + 1} 行不得使用巢狀 YAML`);
    const match = rawLine.match(/^([A-Za-z][A-Za-z0-9_-]*):[ \t]*(.*)$/u);
    if (!match) fail(`${label} frontmatter 第 ${index + 1} 行不是單行 scalar`);
    const [, key, rawValue] = match;
    if (Object.hasOwn(values, key)) fail(`${label} frontmatter key 重複：${key}`);
    let value = rawValue.trim();
    if (value.startsWith('"') || value.endsWith('"')) {
      if (!(value.startsWith('"') && value.endsWith('"'))) fail(`${label} frontmatter ${key} 引號不完整`);
      try {
        value = JSON.parse(value);
      } catch {
        fail(`${label} frontmatter ${key} 的雙引號字串無效`);
      }
    } else if (value.startsWith("'") || value.endsWith("'")) {
      if (!(value.startsWith("'") && value.endsWith("'"))) fail(`${label} frontmatter ${key} 引號不完整`);
      value = value.slice(1, -1).replaceAll("''", "'");
    }
    if (!value) fail(`${label} frontmatter ${key} 不得為空`);
    values[key] = value;
  }
  if (JSON.stringify(Object.keys(values).sort()) !== JSON.stringify(frontmatterKeys)) {
    fail(`${label} frontmatter 必須恰含：${frontmatterKeys.join(", ")}`);
  }
  return values;
}

function pandocInlineText(value) {
  if (Array.isArray(value)) return value.map(pandocInlineText).join("");
  if (!value || typeof value !== "object") return "";
  if (value.t === "Str") return String(value.c ?? "");
  if (["Space", "SoftBreak", "LineBreak"].includes(value.t)) return " ";
  if (value.t === "Code" || value.t === "Math") return String(value.c?.[1] ?? "");
  return pandocInlineText(value.c);
}

function pandocMetaScalars(meta, label) {
  if (!meta || typeof meta !== "object" || Array.isArray(meta)) fail(`${label} Pandoc metadata 無效`);
  const values = {};
  for (const [key, entry] of Object.entries(meta)) {
    if (entry?.t === "MetaString") values[key] = String(entry.c ?? "");
    else if (entry?.t === "MetaInlines") values[key] = pandocInlineText(entry.c).replace(/\s+/gu, " ").trim();
    else fail(`${label} frontmatter ${key} 必須是單行 scalar`);
  }
  if (JSON.stringify(Object.keys(values).sort()) !== JSON.stringify(frontmatterKeys)) {
    fail(`${label} Pandoc metadata 欄位集合與作者 schema 不一致`);
  }
  return values;
}

function scanPublicText(text, label) {
  assertSafeSourceText(text, label);
}

function walkPandoc(value, visit) {
  if (Array.isArray(value)) {
    value.forEach((item) => walkPandoc(item, visit));
    return;
  }
  if (!value || typeof value !== "object") return;
  visit(value);
  Object.values(value).forEach((item) => walkPandoc(item, visit));
}

function decodeLocalImageTarget(raw, sourceLabel) {
  let value = String(raw).replace(/^<|>$/gu, "");
  for (let index = 0; index < 2; index += 1) {
    try {
      const decoded = decodeURIComponent(value);
      if (decoded === value) break;
      value = decoded;
    } catch {
      fail(`${sourceLabel} 有無法 URL-decode 的圖片路徑：${value}`);
    }
  }
  value = value.normalize("NFC");
  if (/^[a-z][a-z0-9+.-]*:/iu.test(value) || value.startsWith("//")) {
    fail(`${sourceLabel} 不得引用遠端或 URI 圖片：${value}`);
  }
  if (isAbsolute(value) || value.includes("\\") || /[\u0000-\u001f\u007f]/u.test(value)) {
    fail(`${sourceLabel} 的圖片路徑不是安全 repo-relative POSIX 路徑：${value}`);
  }
  if (value.includes("?") || value.includes("#")) fail(`${sourceLabel} 的圖片路徑不得含 query／fragment：${value}`);
  return value;
}

function extractMarkdownState(sourcePath, sourceLabel) {
  let ast;
  try {
    ast = JSON.parse(run(pandoc, [
      sourcePath,
      `--from=${markdownFormat}`,
      "--to=json",
    ], { quiet: true }));
  } catch (error) {
    fail(`${sourceLabel} 無法建立 Pandoc AST：${error.message}`);
  }
  const assets = [];
  const levelOneHeadings = [];
  inspectPandocAstSafety(ast, {
    label: sourceLabel,
    onImage: (target) => assets.push(decodeLocalImageTarget(target, sourceLabel)),
  });
  walkPandoc(ast, (node) => {
    const rawHtml = ["RawBlock", "RawInline"].includes(node.t) && node.c?.[0] === "html"
      ? String(node.c?.[1] ?? "").replace(/<!--[\s\S]*?-->/gu, "")
      : "";
    if (
      rawHtml
      && /<\s*\/?\s*h[1-6]\b/iu.test(rawHtml)
    ) {
      fail(`${sourceLabel} 含 raw HTML heading；請使用 Markdown heading`);
    }
    if (node.t === "Header" && node.c?.[0] === 1) {
      levelOneHeadings.push(pandocInlineText(node.c?.[2]).replace(/\s+/gu, " ").trim());
    }
  });
  return {
    assets: [...new Set(assets)].sort(compareCodePoints),
    levelOneHeadings,
    meta: pandocMetaScalars(ast.meta, sourceLabel),
  };
}

function scanSvg(path, label) {
  const text = readFileSync(path, "utf8");
  scanPublicText(text, label);
  assertSafeSvgText(text, label);
  return text;
}

function resolveAsset(reference, sourcePath, label) {
  const candidates = [resolve(dirname(sourcePath), reference), resolve(repoRoot, reference)];
  const found = candidates.find((candidate) => existsSync(candidate));
  if (!found) fail(`${label} 引用不存在的圖片：${reference}`);
  if (!isInside(repoRoot, found) || !isInside(repoRoot, realpathSync(found))) fail(`${label} 圖片逃離 repository：${reference}`);
  if (!statSync(found).isFile()) fail(`${label} 圖片不是檔案：${reference}`);
  return found;
}

function checkHtml(path, label) {
  const html = readFileSync(path, "utf8");
  scanPublicText(html, label);
  assertSafeHtmlText(html, label);
  return html;
}

function pdfMetadata(path, label) {
  const info = run("pdfinfo", [path], { quiet: true });
  const title = info.match(/^Title:\s*(.+)$/mu)?.[1]?.trim();
  const pages = Number.parseInt(info.match(/^Pages:\s*(\d+)$/mu)?.[1] ?? "", 10);
  if (!title || !Number.isInteger(pages) || pages < 1) fail(`${label} metadata 無效`);
  return { title, pages };
}

function loadRegistry() {
  if (!existsSync(registryPath)) fail(`找不到 ${relative(repoRoot, registryPath)}`);
  const registry = parseJsonWithoutDuplicateKeys(readFileSync(registryPath, "utf8"), "publishing registry");
  if (!registry || typeof registry !== "object" || Array.isArray(registry)) fail("publishing registry 根必須是 object");
  if (JSON.stringify(Object.keys(registry).sort()) !== JSON.stringify(["defaultSet", "schemaVersion", "sets"])) {
    fail("publishing registry 欄位集合無效");
  }
  if (registry.schemaVersion !== 1) fail("不支援的 publishing schemaVersion");
  if (!registry.sets || typeof registry.sets !== "object" || Array.isArray(registry.sets)) fail("publishing registry 的 sets 必須是 object");
  validateRegistryDefinition(registry);
  return registry;
}

function parseCli(registry) {
  const [command, ...args] = process.argv.slice(2);
  if (!new Set(["preflight", "release", "verify", "render"]).has(command)) {
    fail("用法：node tools/publication.mjs <preflight|release|verify|render> [--set SET_ID]");
  }
  let setId = registry.defaultSet;
  let all = false;
  let explicitSet = false;
  for (let index = 0; index < args.length; index += 1) {
    if (args[index] === "--all") {
      if (command !== "preflight" || explicitSet) fail("--all 只適用於未指定 --set 的 preflight");
      all = true;
      continue;
    }
    if (args[index] !== "--set" || !args[index + 1] || all) fail(`無法辨識參數：${args[index]}`);
    setId = args[index + 1];
    explicitSet = true;
    index += 1;
  }
  if (all) return { command, all, registry };
  if (!/^[a-z0-9][a-z0-9._-]*$/u.test(setId ?? "")) fail(`不安全的 set id：${setId}`);
  const set = registry.sets[setId];
  if (!set) fail(`找不到 publication set：${setId}`);
  return { command, setId, set, all: false, registry };
}

function documentChapterIdentity(document) {
  const match = document.source?.match(/^content\/([^/]+)\/([^/]+)\/(學生講義)\.md$/u);
  if (!match) fail(`${document.id} source 必須是直接位於 content/<課程>/<章碼>/ 的學生講義.md；教師備課指南屬 legacy，不得進入新 publication set`);
  const courseIdentity = resolveCourseIdentity(match[1], match[2]);
  return {
    ...courseIdentity,
    chapterRoot: `content/${match[1]}/${match[2]}`,
    sourceKind: match[3],
  };
}

function validateRegistryDefinition(registry) {
  if (typeof registry.defaultSet !== "string" || !registry.sets[registry.defaultSet]) {
    fail("publishing registry 的 defaultSet 無效");
  }
  const globalSlugs = new Map();
  for (const [setId, set] of Object.entries(registry.sets)) {
    if (!/^[a-z0-9][a-z0-9._-]*$/u.test(setId)) fail(`不安全的 set id：${setId}`);
    validateSetDefinition(setId, set);
    for (const document of set.documents) {
      const signature = JSON.stringify({
        source: document.source,
        audience: document.audience,
        assets: document.assets,
      });
      const prior = globalSlugs.get(document.slug);
      if (prior && prior.signature !== signature) {
        fail(`不同 publication 文件不得共用 slug：${document.slug}（${prior.setId}／${setId}）`);
      }
      globalSlugs.set(document.slug, { signature, setId });
    }
  }
}

function assertValidCalendarDate(value, label) {
  const match = typeof value === "string"
    ? value.match(/^([0-9]{4})-([0-9]{2})-([0-9]{2})$/u)
    : undefined;
  if (!match) fail(`${label} 必須是 YYYY-MM-DD`);
  const year = Number(match[1]);
  const month = Number(match[2]);
  const day = Number(match[3]);
  const leap = year % 4 === 0 && (year % 100 !== 0 || year % 400 === 0);
  const daysInMonth = [31, leap ? 29 : 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];
  if (year < 1 || month < 1 || month > 12 || day < 1 || day > daysInMonth[month - 1]) {
    fail(`${label} 不是有效曆日`);
  }
  return value;
}

function validateApprovalDefinition(setId, set, documentIds) {
  const approval = set.approval;
  if (!approval || typeof approval !== "object" || Array.isArray(approval)) {
    fail(`${setId} published set 缺少 approval`);
  }
  if (JSON.stringify(Object.keys(approval).sort()) !== JSON.stringify(["approvedAt", "artifactPdfSha256"])) {
    fail(`${setId} approval must contain exactly approvedAt and artifactPdfSha256`);
  }
  assertValidCalendarDate(approval.approvedAt, `${setId}.approval.approvedAt`);
  const digests = approval.artifactPdfSha256;
  if (!digests || typeof digests !== "object" || Array.isArray(digests)) {
    fail(`${setId}.approval.artifactPdfSha256 必須是 document ID 對應 PDF SHA-256 的 object`);
  }
  const expectedIds = [...documentIds].sort(compareCodePoints);
  const approvedIds = Object.keys(digests).sort(compareCodePoints);
  if (JSON.stringify(approvedIds) !== JSON.stringify(expectedIds)) {
    fail(`${setId}.approval.artifactPdfSha256 必須精確覆蓋 documents ID，不得缺少或多出`);
  }
  for (const id of expectedIds) {
    if (!/^[0-9a-f]{64}$/u.test(digests[id] ?? "")) {
      fail(`${setId}.approval.artifactPdfSha256.${id} 必須是 64 位小寫十六進位 SHA-256`);
    }
  }
}

export function validateSetDefinition(setId, set) {
  if (!set || typeof set !== "object" || Array.isArray(set)) fail(`${setId} set 定義無效`);
  if (!new Set(["review", "published"]).has(set.status)) fail(`${setId} status 只允許 review 或 published`);
  const expectedSetKeys = set.status === "published"
    ? ["approval", "description", "documents", "status"]
    : ["description", "documents", "status"];
  if (JSON.stringify(Object.keys(set).sort()) !== JSON.stringify(expectedSetKeys)) {
    fail(`${setId} set 欄位集合無效`);
  }
  const requiredPrefix = `${set.status}-`;
  if (!setId.startsWith(requiredPrefix) || setId.length === requiredPrefix.length) {
    fail(`${setId} 的 status 是 ${set.status}，set id 必須以 ${requiredPrefix} 開頭且帶有後綴`);
  }
  if (typeof set.description !== "string" || !set.description) fail(`${setId} description 無效`);
  if (!Array.isArray(set.documents) || set.documents.length === 0) fail(`${setId} 沒有 documents`);
  const ids = new Set();
  const slugs = new Set();
  const sources = new Set();
  const chapterAudiences = new Map();
  for (const document of set.documents) {
    if (!document || typeof document !== "object" || Array.isArray(document)) fail(`${setId} 有無效 document`);
    if (JSON.stringify(Object.keys(document).sort()) !== JSON.stringify(["assets", "audience", "id", "slug", "source"])) {
      fail(`${setId} document 欄位集合無效：${document.id ?? "unknown"}`);
    }
    if (!/^[a-z0-9][a-z0-9._-]*$/u.test(document.id ?? "")) fail(`${setId} 有不安全 document id`);
    if (ids.has(document.id)) fail(`${setId} document id 重複：${document.id}`);
    ids.add(document.id);
    if (document.audience !== "student") fail(`${document.id} audience 必須是 student；教師 artifact 不屬於新出版標準`);
    if (typeof document.slug !== "string" || !document.slug || document.slug !== document.slug.normalize("NFC")) fail(`${document.id} slug 無效`);
    if (/[/\\\u0000-\u001f\u007f]/u.test(document.slug) || document.slug.includes("..") || document.slug.startsWith(".")) fail(`${document.id} slug 不安全`);
    if (slugs.has(document.slug)) fail(`${setId} slug 重複：${document.slug}`);
    slugs.add(document.slug);
    const chapter = documentChapterIdentity(document);
    const expectedId = expectedDocumentId(chapter, document.audience);
    if (document.id !== expectedId) fail(`${document.id} 必須由課程、章碼與 audience 衍生：${expectedId}`);
    if (sources.has(document.source)) fail(`${setId} source 重複：${document.source}`);
    sources.add(document.source);
    const expectedSourceKind = "學生講義";
    if (chapter.sourceKind !== expectedSourceKind) fail(`${document.id} audience 與 source 檔名不一致`);
    const expectedSlugSuffix = "-學生講義";
    if (!document.slug.startsWith(`${chapter.chapterCode}-`) || !document.slug.endsWith(expectedSlugSuffix)) {
      fail(`${document.id} slug 必須以章碼 ${chapter.chapterCode} 開頭並以 ${expectedSlugSuffix} 結尾`);
    }
    const audiences = chapterAudiences.get(chapter.chapterRoot) ?? new Set();
    if (audiences.has(document.audience)) fail(`${setId} 的 ${chapter.chapterCode} 有重複 audience：${document.audience}`);
    audiences.add(document.audience);
    chapterAudiences.set(chapter.chapterRoot, audiences);
    if (!Array.isArray(document.assets)) fail(`${document.id} assets 必須是陣列`);
    const chapterAssetPrefix = `${chapter.chapterRoot}/assets/`;
    for (const asset of document.assets) {
      if (typeof asset !== "string" || !asset.toLowerCase().endsWith(".svg")) {
        fail(`${document.id} 公開資產必須是 SVG：${asset}`);
      }
      if (!asset.startsWith(chapterAssetPrefix) && !asset.startsWith("content/assets/")) {
        fail(`${document.id} 公開資產必須位於同章 assets/ 或 content/assets/：${asset}`);
      }
    }
  }
  for (const [chapterRoot, audiences] of chapterAudiences) {
    if (audiences.size !== 1 || !audiences.has("student")) {
      fail(`${setId} 的 ${chapterRoot} 必須恰有一份 student document`);
    }
  }
  if (set.status === "published") validateApprovalDefinition(setId, set, ids);
}

export function assertApprovedPdfDigest(setId, set, documentId, actualDigest) {
  if (set.status !== "published") return;
  if (!/^[0-9a-f]{64}$/u.test(actualDigest ?? "")) {
    fail(`${documentId} actual PDF SHA-256 format is invalid`);
  }
  const approvedDigest = set.approval?.artifactPdfSha256?.[documentId];
  if (actualDigest !== approvedDigest) {
    fail(`${documentId} actual PDF SHA-256 does not match approval; content or pipeline changes require renewed approval`);
  }
}

function validateDocumentFrontmatterIdentity(document, markdown, pandocMeta) {
  const chapter = documentChapterIdentity(document);
  const values = strictFrontmatter(markdown, document.source);
  if (pandocMeta) {
    for (const key of frontmatterKeys) {
      if (values[key] !== pandocMeta[key]) {
        fail(`${document.source} frontmatter ${key} 與 Pandoc 實際 metadata 不一致`);
      }
    }
  }
  const expectedPrefix = "學生講義";
  const expectedAudiencePrefix = "學生版";
  if (values["title-prefix"] !== expectedPrefix) fail(`${document.source} title-prefix 與 audience 不一致`);
  if (!values.audience.startsWith(expectedAudiencePrefix)) fail(`${document.source} audience 與 manifest 不一致`);
  if (!values.title.startsWith(`${chapter.chapterCode} `)) fail(`${document.source} title 必須以章碼 ${chapter.chapterCode} 開頭`);
  const chapterTitle = values.title.slice(`${chapter.chapterCode} `.length);
  if (!chapterTitle || leadingRegisteredChapterCode(chapterTitle)) {
    fail(`${document.source} title 的章名不得為空或再次以章碼開頭`);
  }
  const expectedSlug = `${values.title.replace(/\s+/gu, "-")}-${expectedPrefix}`;
  if (values.output_slug !== document.slug || values.output_slug !== expectedSlug) {
    fail(`${document.source} output_slug 必須由 title 與版別一致衍生：${expectedSlug}`);
  }
  if (values.course !== chapter.course) fail(`${document.source} course 應為 ${chapter.course}`);
  if (values.subject !== chapter.subject) fail(`${document.source} subject 應為 ${chapter.subject}`);
  assertValidCalendarDate(values.updated, `${document.source} updated`);
  return { chapter, values };
}

function validateDocumentHeading(document, values, levelOneHeadings) {
  const expected = values.title;
  if (levelOneHeadings.length !== 1 || levelOneHeadings[0] !== expected) {
    fail(`${document.source} 必須恰有一個 H1，且文字必須是：${expected}`);
  }
}

function validateSetFrontmatterIdentity(setId, set) {
  const chapters = new Map();
  for (const document of set.documents) {
    const sourcePath = validateRelativePath(document.source, `${document.id}.source`);
    const markdown = readFileSync(sourcePath, "utf8");
    scanPublicText(markdown, document.source);
    const identity = validateDocumentFrontmatterIdentity(document, markdown);
    const reference = chapters.get(identity.chapter.chapterRoot);
    const shared = {
      title: identity.values.title,
      subject: identity.values.subject,
      course: identity.values.course,
      updated: identity.values.updated,
    };
    if (reference) fail(`${setId} 的 ${identity.chapter.chapterCode} 不得重複登記章節`);
    chapters.set(identity.chapter.chapterRoot, shared);
  }
}

function collectDocumentState(document, { requireOutputs = true } = {}) {
  const sourcePath = validateRelativePath(document.source, `${document.id}.source`);
  if (lstatSync(sourcePath).isSymbolicLink()) fail(`${document.id}.source 不得是 symlink`);
  const markdown = readFileSync(sourcePath, "utf8");
  scanPublicText(markdown, document.source);
  const parsedMarkdown = extractMarkdownState(sourcePath, document.source);
  const identity = validateDocumentFrontmatterIdentity(document, markdown, parsedMarkdown.meta);
  validateDocumentHeading(document, identity.values, parsedMarkdown.levelOneHeadings);

  const references = parsedMarkdown.assets;
  for (const reference of references) {
    const isChapterLocal = reference.startsWith("assets/");
    const isShared = reference.startsWith("content/assets/");
    const segments = reference.split("/");
    if ((!isChapterLocal && !isShared) || segments.some((segment) => !segment || segment === "." || segment === "..")) {
      fail(`${document.source} 圖片必須字面使用 assets/... 或 content/assets/...，且不得含 dot segment：${reference}`);
    }
  }
  const resolvedReferencePaths = references.map((reference) => resolveAsset(reference, sourcePath, document.source));
  const actualAssets = resolvedReferencePaths
    .map((path) => relative(repoRoot, path).split(process.platform === "win32" ? "\\" : "/").join("/"))
    .sort(compareCodePoints);
  const manifestAssets = [...document.assets].sort(compareCodePoints);
  if (JSON.stringify(actualAssets) !== JSON.stringify(manifestAssets)) {
    fail(`${document.id} 圖片閉包與 manifest 不一致\n實際：${actualAssets.join(", ")}\nmanifest：${manifestAssets.join(", ")}`);
  }
  const assets = manifestAssets.map((asset) => {
    const assetPath = validateRelativePath(asset, `${document.id}.asset`);
    if (lstatSync(assetPath).isSymbolicLink()) fail(`${document.id}.asset 不得是 symlink：${asset}`);
    scanSvg(assetPath, asset);
    return { path: asset, sha256: sha256(assetPath) };
  });

  const state = {
    id: document.id,
    audience: document.audience,
    source: document.source,
    sourceSha256: sha256(sourcePath),
    slug: document.slug,
    assets,
  };
  if (!requireOutputs) return state;

  const htmlRelative = `output/html/${document.slug}.html`;
  const pdfRelative = `output/pdf/${document.slug}.pdf`;
  const htmlPath = validateRelativePath(htmlRelative, `${document.id}.html`);
  const pdfPath = validateRelativePath(pdfRelative, `${document.id}.pdf`);
  assertRegularDirectFile(htmlPath, dirname(htmlPath), `${document.id}.html`);
  assertRegularDirectFile(pdfPath, dirname(pdfPath), `${document.id}.pdf`);
  checkHtml(htmlPath, htmlRelative);
  const { title, pages } = pdfMetadata(pdfPath, pdfRelative);
  return {
    ...state,
    html: htmlRelative,
    htmlSha256: sha256(htmlPath),
    pdf: `${document.slug}.pdf`,
    pdfSource: pdfRelative,
    pdfSha256: sha256(pdfPath),
    title,
    pages,
  };
}

function cssLocalDependencies(cssRelative) {
  const cssPath = validateRelativePath(cssRelative, `pipeline-css:${cssRelative}`);
  const css = readFileSync(cssPath, "utf8");
  const dependencies = [];
  assertSafeCssText(css, cssRelative, {
    onLocalUrl: (reference, raw) => {
      const dependencyPath = resolve(dirname(cssPath), reference);
      if (!isInside(repoRoot, dependencyPath) || !lstatIfPresent(dependencyPath)) {
        fail(`${cssRelative} 引用的 pipeline 資源不存在或逃離 repository：${raw}`);
      }
      if (realpathSync(dependencyPath) !== dependencyPath || !lstatSync(dependencyPath).isFile()) {
        fail(`${cssRelative} 引用的 pipeline 資源必須是 canonical 一般檔案：${raw}`);
      }
      dependencies.push(relative(repoRoot, dependencyPath).split(process.platform === "win32" ? "\\" : "/").join("/"));
    },
  });
  return dependencies;
}

function pipelineFileList() {
  // figures.json is itself a pipeline-hashed file and contains exact hashes for
  // every generator/input/output. Validate those bindings here without adding
  // legacy/private `_tools/` files to the production publication closure.
  loadFigureManifest(repoRoot);
  return [...new Set([
    ...pipelineBaseFiles,
    ...cssLocalDependencies("styles/handout.css"),
  ])].sort(compareCodePoints);
}

function pipelineState() {
  return pipelineFileList().map((path) => ({
    path,
    sha256: sha256(validateRelativePath(path, `pipeline:${path}`)),
  }));
}

function assertPublishedInputsReady(setId, set) {
  assertRepositoryPrivacyBoundary(repoRoot);
  if (set.status !== "published") return;
  const inputs = [...new Set([
    ...set.documents.flatMap((document) => [document.source, ...document.assets]),
    ...pipelineFileList(),
  ])].sort(compareCodePoints);
  run("git", ["ls-files", "--error-unmatch", "--", ...inputs], { quiet: true });
  const changedInputs = run("git", ["status", "--porcelain", "--", ...inputs], { quiet: true }).trim();
  if (changedInputs) fail(`${setId} 是 published，所有來源／資產／產線檔案必須 tracked 且 clean`);
  if (repositoryState().dirty) fail(`${setId} 是 published，repository 必須完整 clean`);
}

function assertSnapshotEqual(before, after, label) {
  if (JSON.stringify(before) !== JSON.stringify(after)) fail(`${label} 在操作期間改變；拒絕發布混合版本`);
}

function ensureRelativeDirectory(root, relativeDirectory, label) {
  if (relativeDirectory === "." || relativeDirectory === "") return root;
  let current = root;
  for (const segment of relativeDirectory.split("/")) {
    if (!segment || segment === "." || segment === "..") fail(`${label} 含不安全目錄片段`);
    const next = join(current, segment);
    ensureDirectCanonicalDirectory(next, current, `${label}/${segment}`, { create: true });
    current = next;
  }
  return current;
}

function createBuildSnapshot(setId) {
  const tmpRoot = join(repoRoot, "tmp");
  ensureDirectCanonicalDirectory(tmpRoot, repoRoot, "tmp", { create: true });
  const snapshotParent = join(tmpRoot, "publication-build");
  ensureDirectCanonicalDirectory(snapshotParent, tmpRoot, "tmp/publication-build", { create: true });
  const snapshotPath = mkdtempSync(join(snapshotParent, `.${setId}-`));
  assertDirectChild(snapshotParent, snapshotPath, `${setId} build snapshot`);
  const identity = assertCanonicalDirectory(snapshotPath, `${setId} build snapshot`);
  if ((identity.mode & 0o077) !== 0) fail(`${setId} build snapshot 權限必須限制為 0700`);
  return { path: snapshotPath, parent: snapshotParent, identity };
}

function withBuildSnapshot(setId, operation) {
  const snapshot = createBuildSnapshot(setId);
  let result;
  let operationError;
  try {
    result = operation(snapshot);
  } catch (error) {
    operationError = error;
  }
  try {
    safeRemoveOwnedDirectory(snapshot.path, snapshot.parent, snapshot.identity, `${setId} build snapshot`);
  } catch (cleanupError) {
    if (operationError) {
      process.stderr.write(`警告：${setId} build snapshot 清理失敗：${cleanupError.message}\n`);
    } else {
      operationError = cleanupError;
    }
  }
  if (operationError) throw operationError;
  return result;
}

function snapshotExpectedFiles(inputStates, pipeline) {
  const expected = new Map();
  const add = (path, digest, label) => {
    const prior = expected.get(path);
    if (prior && prior.digest !== digest) fail(`${label} 在同一 snapshot 有矛盾 hash：${path}`);
    expected.set(path, { digest, label });
  };
  for (const state of inputStates) {
    add(state.source, state.sourceSha256, `${state.id}.source`);
    for (const asset of state.assets) add(asset.path, asset.sha256, `${state.id}.asset`);
  }
  for (const file of pipeline) add(file.path, file.sha256, `pipeline:${file.path}`);
  return expected;
}

function populateBuildSnapshot(snapshot, setId, set, inputStates, pipeline) {
  for (const [relativePath, expected] of snapshotExpectedFiles(inputStates, pipeline)) {
    const source = validateRelativePath(relativePath, expected.label);
    const parent = ensureRelativeDirectory(snapshot.path, dirname(relativePath), `${setId} snapshot`);
    const destination = join(snapshot.path, relativePath);
    assertDirectChild(parent, destination, `${setId} snapshot/${relativePath}`);
    copyFileSync(source, destination, fsConstants.COPYFILE_EXCL);
    assertRegularDirectFile(destination, parent, `${setId} snapshot/${relativePath}`);
    if (sha256(destination) !== expected.digest) {
      fail(`${expected.label} 在建立 immutable snapshot 時改變；拒絕混合版本`);
    }
    chmodSync(destination, 0o400);
  }

  const snapshotRegistryPath = join(snapshot.path, "publishing", "sets.json");
  const snapshotRegistry = parseJsonWithoutDuplicateKeys(
    readFileSync(snapshotRegistryPath, "utf8"),
    `${setId} snapshot registry`,
  );
  const snapshotSet = snapshotRegistry.sets?.[setId];
  if (JSON.stringify(snapshotSet) !== JSON.stringify(set)) {
    fail(`${setId} registry 在 CLI 載入與 snapshot 捕捉間改變`);
  }
  validateSetDefinition(setId, snapshotSet);
}

function collectSnapshotOutputState(snapshot, inputState) {
  const htmlRelative = `output/html/${inputState.slug}.html`;
  const pdfRelative = `output/pdf/${inputState.slug}.pdf`;
  const htmlPath = join(snapshot.path, htmlRelative);
  const pdfPath = join(snapshot.path, pdfRelative);
  assertRegularDirectFile(htmlPath, dirname(htmlPath), `${inputState.id} snapshot HTML`);
  assertRegularDirectFile(pdfPath, dirname(pdfPath), `${inputState.id} snapshot PDF`);
  checkHtml(htmlPath, `${inputState.id} snapshot HTML`);
  const { title, pages } = pdfMetadata(pdfPath, `${inputState.id} snapshot PDF`);
  return {
    ...inputState,
    html: `${inputState.slug}.html`,
    htmlSource: htmlRelative,
    htmlSha256: sha256(htmlPath),
    pdf: `${inputState.slug}.pdf`,
    pdfSource: pdfRelative,
    pdfSha256: sha256(pdfPath),
    title,
    pages,
    buildHtmlPath: htmlPath,
    buildPdfPath: pdfPath,
  };
}

function installSnapshotFile(source, destination, expectedDigest, nonce, label) {
  const parent = dirname(destination);
  assertCanonicalDirectory(parent, `${label} parent`);
  assertDirectChild(parent, destination, label);
  if (lstatIfPresent(destination)) assertRegularDirectFile(destination, parent, label);
  const temporary = join(parent, `.${basename(destination)}.install-${nonce}`);
  assertDirectChild(parent, temporary, `${label} temporary`);
  assertAbsent(temporary, `${label} temporary`);
  try {
    copyFileSync(source, temporary, fsConstants.COPYFILE_EXCL);
    assertRegularDirectFile(temporary, parent, `${label} temporary`);
    if (sha256(temporary) !== expectedDigest) fail(`${label} temporary hash 不一致`);
    renameSync(temporary, destination);
    assertRegularDirectFile(destination, parent, label);
    if (sha256(destination) !== expectedDigest) fail(`${label} 安裝後 hash 不一致`);
  } finally {
    if (lstatIfPresent(temporary)) rmSync(temporary, { force: true });
  }
}

function installSnapshotOutputs(snapshot, states) {
  const outputRoot = join(repoRoot, "output");
  ensureDirectCanonicalDirectory(outputRoot, repoRoot, "output", { create: true });
  const htmlRoot = join(outputRoot, "html");
  const pdfRoot = join(outputRoot, "pdf");
  ensureDirectCanonicalDirectory(htmlRoot, outputRoot, "output/html", { create: true });
  ensureDirectCanonicalDirectory(pdfRoot, outputRoot, "output/pdf", { create: true });
  const nonce = basename(snapshot.path).slice(1);
  for (const state of states) {
    installSnapshotFile(
      state.buildHtmlPath,
      join(htmlRoot, `${state.slug}.html`),
      state.htmlSha256,
      nonce,
      `${state.id} HTML`,
    );
    installSnapshotFile(
      state.buildPdfPath,
      join(pdfRoot, `${state.slug}.pdf`),
      state.pdfSha256,
      nonce,
      `${state.id} PDF`,
    );
  }
}

function inputStateFromCompleteState(state) {
  return {
    id: state.id,
    audience: state.audience,
    source: state.source,
    sourceSha256: state.sourceSha256,
    slug: state.slug,
    assets: state.assets,
  };
}

function assertExactDirectoryEntries(directory, expectedNames, label) {
  assertCanonicalDirectory(directory, label);
  const entries = readdirSync(directory, { withFileTypes: true });
  if (entries.some((entry) => !entry.isFile())) fail(`${label} 不得含 symlink、子目錄或特殊檔案`);
  const actualNames = new Set(entries.map((entry) => entry.name));
  if (expectedNames.size !== actualNames.size || [...expectedNames].some((name) => !actualNames.has(name))) {
    fail(`${label} 不是精確白名單`);
  }
  for (const name of expectedNames) assertRegularDirectFile(join(directory, name), directory, `${label}/${name}`);
}

function acquireSetLock(distParent, setId) {
  const lockPath = join(distParent, `.${setId}.lock`);
  assertDirectChild(distParent, lockPath, `${setId} lock`);
  assertAbsent(lockPath, `${setId} lock`);
  try {
    mkdirSync(lockPath, { mode: 0o700 });
  } catch (error) {
    if (error?.code === "EEXIST") fail(`${setId} 已有 release/render 執行中或殘留 lock`);
    throw error;
  }
  const identity = assertCanonicalDirectory(lockPath, `${setId} lock`);
  if ((identity.mode & 0o077) !== 0) fail(`${setId} lock 權限必須限制為 0700`);
  return { path: lockPath, identity };
}

function withSetLock(setId, operation) {
  const distParent = join(repoRoot, "dist");
  ensureDirectCanonicalDirectory(distParent, repoRoot, "dist", { create: true });
  const lock = acquireSetLock(distParent, setId);
  let result;
  let operationError;
  try {
    result = operation(distParent);
  } catch (error) {
    operationError = error;
  }
  try {
    safeRemoveOwnedDirectory(lock.path, distParent, lock.identity, `${setId} lock`);
  } catch (cleanupError) {
    if (operationError) {
      process.stderr.write(`警告：${setId} lock 清理失敗：${cleanupError.message}\n`);
    } else {
      operationError = cleanupError;
    }
  }
  if (operationError) throw operationError;
  return result;
}

function withGlobalBuildLock(operation) {
  const distParent = join(repoRoot, "dist");
  ensureDirectCanonicalDirectory(distParent, repoRoot, "dist", { create: true });
  const lock = acquireSetLock(distParent, "global-build");
  let result;
  let operationError;
  try {
    result = operation();
  } catch (error) {
    operationError = error;
  }
  try {
    safeRemoveOwnedDirectory(lock.path, distParent, lock.identity, "global build lock");
  } catch (cleanupError) {
    if (operationError) {
      process.stderr.write(`警告：global build lock 清理失敗：${cleanupError.message}\n`);
    } else {
      operationError = cleanupError;
    }
  }
  if (operationError) throw operationError;
  return result;
}

function createExclusiveStaging(distParent, setId) {
  assertCanonicalDirectory(distParent, "dist");
  const staging = mkdtempSync(join(distParent, `.${setId}.staging-`));
  assertDirectChild(distParent, staging, `${setId} staging`);
  const identity = assertCanonicalDirectory(staging, `${setId} staging`);
  if ((identity.mode & 0o077) !== 0) fail(`${setId} staging 權限必須限制為 0700`);
  return { path: staging, identity };
}

function preflightSet(setId, set) {
  validateSetDefinition(setId, set);
  validateSetFrontmatterIdentity(setId, set);
  assertPublishedInputsReady(setId, set);
  const states = set.documents.map((document) => collectDocumentState(document, { requireOutputs: false }));
  const pipeline = pipelineState();
  for (const state of states) {
    process.stdout.write(`${state.id}：來源與 ${state.assets.length} 個 SVG 資產閉包通過\n`);
  }
  process.stdout.write(`${setId}：${states.length} 份學生講義、frontmatter 身分與 ${pipeline.length} 個產線檔案通過 preflight\n`);
}

function releaseSet(setId, set) {
  validateSetDefinition(setId, set);
  validateSetFrontmatterIdentity(setId, set);
  assertPublishedInputsReady(setId, set);
  return withGlobalBuildLock(() => withSetLock(setId, (distParent) => withBuildSnapshot(setId, (snapshot) => {
    const beforeInputs = set.documents.map((document) => collectDocumentState(document, { requireOutputs: false }));
    const beforePipeline = pipelineState();
    populateBuildSnapshot(snapshot, setId, set, beforeInputs, beforePipeline);

    const snapshotBuilder = join(snapshot.path, "tools", "build-handout.mjs");
    for (const document of set.documents) {
      process.stdout.write(`\n從 immutable snapshot 建置 ${document.id}\n`);
      run(process.execPath, [snapshotBuilder, join(snapshot.path, document.source)]);
    }

    const snapshotHtmlRoot = join(snapshot.path, "output", "html");
    const snapshotPdfRoot = join(snapshot.path, "output", "pdf");
    assertExactDirectoryEntries(
      snapshotHtmlRoot,
      new Set(set.documents.map((document) => `${document.slug}.html`)),
      `${setId} snapshot HTML`,
    );
    assertExactDirectoryEntries(
      snapshotPdfRoot,
      new Set(set.documents.map((document) => `${document.slug}.pdf`)),
      `${setId} snapshot PDF`,
    );

    const states = beforeInputs.map((state) => collectSnapshotOutputState(snapshot, state));
    for (const state of states) {
      assertApprovedPdfDigest(setId, set, state.id, state.pdfSha256);
    }
    const snapshotChecker = join(snapshot.path, "tools", "check-handout.mjs");
    run(process.execPath, [snapshotChecker, ...states.map((state) => state.buildPdfPath)]);
    assertSnapshotEqual(
      beforeInputs,
      set.documents.map((document) => collectDocumentState(document, { requireOutputs: false })),
      `${setId} source/assets snapshot`,
    );
    assertSnapshotEqual(beforePipeline, pipelineState(), `${setId} pipeline snapshot`);
    installSnapshotOutputs(snapshot, states);
    run(process.execPath, [
      join(repoRoot, "tools", "check-handout.mjs"),
      ...states.map((state) => state.pdfSource),
    ]);
    assertSnapshotEqual(
      beforeInputs,
      set.documents.map((document) => collectDocumentState(document, { requireOutputs: false })),
      `${setId} source/assets snapshot`,
    );
    assertSnapshotEqual(beforePipeline, pipelineState(), `${setId} pipeline snapshot`);
    run(process.execPath, [join(repoRoot, "tools", "check-handout.mjs"), ...states.map((state) => state.pdfSource)]);

    const distDir = join(distParent, setId);
    const staging = createExclusiveStaging(distParent, setId);
    const stagingSuffix = basename(staging.path).slice(`.${setId}.staging-`.length);
    const backup = join(distParent, `.${setId}.backup-${stagingSuffix}`);
    assertDirectChild(distParent, backup, `${setId} backup`);

    let oldIdentity;
    let oldMoved = false;
    let newInstalled = false;
    let transactionError;
    try {
      assertAbsent(backup, `${setId} backup`);
      for (const state of states) {
        for (const [kind, source, filename, digest] of [
          ["HTML", state.buildHtmlPath, state.html, state.htmlSha256],
          ["PDF", state.buildPdfPath, state.pdf, state.pdfSha256],
        ]) {
          const destination = join(staging.path, filename);
          assertDirectChild(staging.path, destination, `${state.id} staging ${kind}`);
          copyFileSync(source, destination, fsConstants.COPYFILE_EXCL);
          assertRegularDirectFile(destination, staging.path, `${state.id} staging ${kind}`);
          if (sha256(destination) !== digest) fail(`${state.id} staging ${kind} copy hash 不一致`);
        }
      }

      const releaseManifest = {
        schemaVersion: 1,
        set: setId,
        status: set.status,
        description: set.description,
        generatedAt: new Date().toISOString(),
        verificationModel,
        repository: repositoryState(),
        tools: toolState(),
        pipeline: beforePipeline,
        artifacts: states.map(({ htmlSource, pdfSource, buildHtmlPath, buildPdfPath, ...state }) => state),
      };
      const manifestText = `${JSON.stringify(releaseManifest, null, 2)}\n`;
      scanPublicText(manifestText, "release manifest");
      writeFileSync(join(staging.path, "manifest.json"), manifestText, {
        encoding: "utf8",
        flag: "wx",
        mode: 0o600,
      });
      const sums = states
        .flatMap((state) => [
          `${state.htmlSha256}  ${state.html}`,
          `${state.pdfSha256}  ${state.pdf}`,
        ])
        .sort(compareCodePoints)
        .join("\n");
      writeFileSync(join(staging.path, "SHA256SUMS"), `${sums}\n`, {
        encoding: "utf8",
        flag: "wx",
        mode: 0o600,
      });

      const expectedNames = new Set([
        "manifest.json",
        "SHA256SUMS",
        ...set.documents.flatMap((document) => [`${document.slug}.html`, `${document.slug}.pdf`]),
      ]);
      assertExactDirectoryEntries(staging.path, expectedNames, `${setId} staging`);
      assertSnapshotEqual(beforeInputs, set.documents.map((document) => collectDocumentState(document, { requireOutputs: false })), `${setId} source/assets snapshot`);
      assertSnapshotEqual(beforePipeline, pipelineState(), `${setId} pipeline snapshot`);

      const existingDist = lstatIfPresent(distDir);
      if (existingDist) {
        oldIdentity = assertCanonicalDirectory(distDir, `${setId} current dist`);
        renameSync(distDir, backup);
        oldMoved = true;
        assertDirectoryIdentity(backup, oldIdentity, `${setId} backup`);
      }

      renameSync(staging.path, distDir);
      newInstalled = true;
      assertDirectoryIdentity(distDir, staging.identity, `${setId} promoted dist`);
      verifySet(setId, set, { locked: true });
    } catch (error) {
      transactionError = error;
    }

    if (transactionError) {
      const rollbackErrors = [];
      if (newInstalled && lstatIfPresent(distDir)) {
        try {
          safeRemoveOwnedDirectory(distDir, distParent, staging.identity, `${setId} failed promoted dist`);
          newInstalled = false;
        } catch (error) {
          rollbackErrors.push(`移除失敗的新 dist：${error.message}`);
        }
      }
      if (oldMoved && lstatIfPresent(backup)) {
        try {
          if (lstatIfPresent(distDir)) fail(`${setId} rollback 目標已被占用`);
          assertDirectoryIdentity(backup, oldIdentity, `${setId} backup`);
          renameSync(backup, distDir);
          assertDirectoryIdentity(distDir, oldIdentity, `${setId} restored dist`);
          oldMoved = false;
        } catch (error) {
          rollbackErrors.push(`還原舊 dist 失敗：${error.message}`);
        }
      }
      if (lstatIfPresent(staging.path)) {
        try {
          safeRemoveOwnedDirectory(staging.path, distParent, staging.identity, `${setId} staging`);
        } catch (error) {
          rollbackErrors.push(`清理 staging 失敗：${error.message}`);
        }
      }
      if (rollbackErrors.length > 0) {
        fail(`${transactionError.message}\nrollback 未完整完成：${rollbackErrors.join("；")}`);
      }
      throw transactionError;
    }

    if (oldMoved && lstatIfPresent(backup)) {
      try {
        safeRemoveOwnedDirectory(backup, distParent, oldIdentity, `${setId} obsolete backup`);
      } catch (error) {
        process.stderr.write(`警告：新 dist 已通過驗證，但舊 backup 無法清理：${error.message}\n`);
      }
    }
    process.stdout.write(`\n發布 staging 已建立：${relative(repoRoot, distDir)}\n`);
  })));
}

function verifySet(setId, set, { locked = false } = {}) {
  if (!locked) return withSetLock(setId, () => verifySet(setId, set, { locked: true }));
  validateSetDefinition(setId, set);
  validateSetFrontmatterIdentity(setId, set);
  assertPublishedInputsReady(setId, set);
  const distParent = join(repoRoot, "dist");
  ensureDirectCanonicalDirectory(distParent, repoRoot, "dist");
  const distDir = join(distParent, setId);
  const distIdentity = ensureDirectCanonicalDirectory(distDir, distParent, `${setId} staging`);

  const expectedNames = new Set([
    "manifest.json",
    "SHA256SUMS",
    ...set.documents.flatMap((document) => [`${document.slug}.html`, `${document.slug}.pdf`]),
  ]);
  assertExactDirectoryEntries(distDir, expectedNames, `${setId} staging`);
  const manifestPath = assertRegularDirectFile(join(distDir, "manifest.json"), distDir, `${setId}/manifest.json`);
  const sumsPath = assertRegularDirectFile(join(distDir, "SHA256SUMS"), distDir, `${setId}/SHA256SUMS`);
  const manifestText = readFileSync(manifestPath, "utf8");
  scanPublicText(manifestText, `${setId}/manifest.json`);
  const manifest = parseJsonWithoutDuplicateKeys(manifestText, `${setId}/manifest.json`);

  if (!manifest || typeof manifest !== "object" || Array.isArray(manifest)) fail(`${setId} manifest 格式無效`);
  if (JSON.stringify(Object.keys(manifest).sort()) !== JSON.stringify(manifestKeys)) fail(`${setId} manifest 欄位集合無效`);
  if (manifest.schemaVersion !== 1 || manifest.set !== setId) fail(`${setId} manifest identity 無效`);
  if (manifest.status !== set.status || manifest.description !== set.description) fail(`${setId} status/description 與 registry 不一致`);
  if (manifest.verificationModel !== verificationModel) fail(`${setId} verification model 無效`);
  if (typeof manifest.generatedAt !== "string" || Number.isNaN(Date.parse(manifest.generatedAt))) fail(`${setId} generatedAt 無效`);
  if (!Array.isArray(manifest.artifacts) || manifest.artifacts.length !== set.documents.length) fail(`${setId} artifact 數量錯誤`);
  if (JSON.stringify(manifest.tools) !== JSON.stringify(toolState())) fail(`${setId} 工具版本與 release 時不同`);
  if (
    !manifest.repository
    || typeof manifest.repository !== "object"
    || Array.isArray(manifest.repository)
    || JSON.stringify(Object.keys(manifest.repository).sort()) !== JSON.stringify(["commit", "dirty"])
    || !/^[0-9a-f]{40,64}$/u.test(manifest.repository.commit ?? "")
    || typeof manifest.repository.dirty !== "boolean"
  ) fail(`${setId} repository provenance 無效`);
  if (set.status === "published" && JSON.stringify(manifest.repository) !== JSON.stringify(repositoryState())) {
    fail(`${setId} published provenance 與目前 clean commit 不一致`);
  }

  const expectedIds = new Set(set.documents.map((document) => document.id));
  const artifactById = new Map();
  for (const artifact of manifest.artifacts) {
    if (!artifact || typeof artifact !== "object" || Array.isArray(artifact)) fail(`${setId} 有無效 artifact`);
    if (JSON.stringify(Object.keys(artifact).sort()) !== JSON.stringify(artifactKeys)) fail(`${setId} artifact 欄位集合無效：${artifact.id ?? "unknown"}`);
    if (!expectedIds.has(artifact.id)) fail(`${setId} manifest 有未知 artifact：${artifact.id}`);
    if (artifactById.has(artifact.id)) fail(`${setId} manifest artifact id 重複：${artifact.id}`);
    artifactById.set(artifact.id, artifact);
  }
  if (artifactById.size !== expectedIds.size || [...expectedIds].some((id) => !artifactById.has(id))) {
    fail(`${setId} manifest artifact id 不是 registry 精確集合`);
  }

  const inputSnapshot = set.documents.map((document) => collectDocumentState(document, { requireOutputs: false }));
  const currentStates = new Map(inputSnapshot.map((state) => [state.id, state]));
  const currentPipeline = pipelineState();
  if (JSON.stringify(manifest.pipeline) !== JSON.stringify(currentPipeline)) fail(`${setId} 產線檔案已變更，需重新 release`);

  const pdfs = [];
  const verifiedOutputs = [];
  const expectedSums = [];
  for (const document of set.documents) {
    const artifact = artifactById.get(document.id);
    const current = currentStates.get(document.id);
    for (const key of ["id", "audience", "source", "sourceSha256", "slug"]) {
      if (artifact[key] !== current[key]) fail(`${document.id} ${key} 與目前來源不一致`);
    }
    if (JSON.stringify(artifact.assets) !== JSON.stringify(current.assets)) fail(`${document.id} assets hash 與目前來源不一致`);

    const expectedHtml = `${document.slug}.html`;
    if (artifact.html !== expectedHtml) fail(`${document.id} HTML 檔名不符 slug`);
    const htmlPath = assertRegularDirectFile(join(distDir, expectedHtml), distDir, `${document.id} HTML`);
    checkHtml(htmlPath, `${setId}/${expectedHtml}`);
    if (sha256(htmlPath) !== artifact.htmlSha256) fail(`${document.id} HTML SHA-256 不符`);

    const expectedPdf = `${document.slug}.pdf`;
    if (artifact.pdf !== expectedPdf) fail(`${document.id} PDF 檔名不符 slug`);
    const pdfPath = assertRegularDirectFile(join(distDir, expectedPdf), distDir, `${document.id} PDF`);
    const digest = sha256(pdfPath);
    assertApprovedPdfDigest(setId, set, document.id, digest);
    if (digest !== artifact.pdfSha256) fail(`${artifact.pdf} SHA-256 不符`);
    const metadata = pdfMetadata(pdfPath, artifact.pdf);
    if (metadata.title !== artifact.title || metadata.pages !== artifact.pages) fail(`${document.id} title/pages 與實際 PDF 不一致`);
    expectedSums.push(`${artifact.htmlSha256}  ${artifact.html}`, `${digest}  ${artifact.pdf}`);
    pdfs.push(pdfPath);
    verifiedOutputs.push({
      htmlPath,
      htmlSha256: artifact.htmlSha256,
      pdfPath,
      pdfSha256: artifact.pdfSha256,
    });
  }
  if (new Set(pdfs).size !== set.documents.length) fail(`${setId} PDF canonical path 不唯一`);

  const sumText = readFileSync(sumsPath, "utf8").trim();
  if (sumText !== expectedSums.sort(compareCodePoints).join("\n")) fail(`${setId} SHA256SUMS 不一致`);
  run(process.execPath, [join(repoRoot, "tools", "check-handout.mjs"), ...pdfs]);
  assertSnapshotEqual(inputSnapshot, set.documents.map((document) => collectDocumentState(document, { requireOutputs: false })), `${setId} verify source/assets snapshot`);
  assertSnapshotEqual(currentPipeline, pipelineState(), `${setId} verify pipeline snapshot`);
  assertDirectoryIdentity(distDir, distIdentity, `${setId} verified dist`);
  if (readFileSync(manifestPath, "utf8") !== manifestText) fail(`${setId} manifest 在 verify 期間改變`);
  if (readFileSync(sumsPath, "utf8").trim() !== sumText) fail(`${setId} SHA256SUMS 在 verify 期間改變`);
  for (const output of verifiedOutputs) {
    if (sha256(output.htmlPath) !== output.htmlSha256 || sha256(output.pdfPath) !== output.pdfSha256) {
      fail(`${setId} HTML/PDF 在 verify 期間改變`);
    }
  }
  process.stdout.write(`${setId}：${pdfs.length} 份唯一 PDF，白名單、來源／資產／產線 hash 與 PDF QA 全部通過\n`);
  process.stdout.write("注意：verify 證明與目前 source/pipeline 的一致性，不是數位簽章或外部信任錨。\n");
}

function renderSet(setId, set) {
  validateSetDefinition(setId, set);
  validateSetFrontmatterIdentity(setId, set);
  return withSetLock(setId, (distParent) => {
    verifySet(setId, set, { locked: true });
    const pillowPython = findPillowPython();
    const distDir = join(distParent, setId);
    const tmpRoot = join(repoRoot, "tmp");
    ensureDirectCanonicalDirectory(tmpRoot, repoRoot, "tmp", { create: true });
    const reviewParent = join(tmpRoot, "review");
    ensureDirectCanonicalDirectory(reviewParent, tmpRoot, "tmp/review", { create: true });
    const reviewRoot = join(reviewParent, setId);
    const stagingPath = mkdtempSync(join(reviewParent, `.${setId}.staging-`));
    assertDirectChild(reviewParent, stagingPath, `${setId} review staging`);
    const stagingIdentity = assertCanonicalDirectory(stagingPath, `${setId} review staging`);
    if ((stagingIdentity.mode & 0o077) !== 0) fail(`${setId} review staging 權限必須限制為 0700`);
    const suffix = basename(stagingPath).slice(`.${setId}.staging-`.length);
    const backup = join(reviewParent, `.${setId}.backup-${suffix}`);
    assertDirectChild(reviewParent, backup, `${setId} review backup`);

    let oldIdentity;
    let oldMoved = false;
    let newInstalled = false;
    let operationError;
    try {
      const artifacts = [];
      for (const document of set.documents) {
        const pdf = assertRegularDirectFile(join(distDir, `${document.slug}.pdf`), distDir, `${document.id} render PDF`);
        const metadata = pdfMetadata(pdf, `${document.id} render PDF`);
        const documentDir = join(stagingPath, document.id);
        ensureDirectCanonicalDirectory(documentDir, stagingPath, `${document.id} review`, { create: true });
        const modes = {};
        for (const mode of ["color", "grayscale"]) {
          const modeDir = join(documentDir, mode);
          ensureDirectCanonicalDirectory(modeDir, documentDir, `${document.id}/${mode}`, { create: true });
          const pageDir = join(modeDir, "pages");
          ensureDirectCanonicalDirectory(pageDir, modeDir, `${document.id}/${mode}/pages`, { create: true });
          const args = mode === "grayscale"
            ? ["-gray", "-png", "-r", "120", pdf, join(pageDir, "page")]
            : ["-png", "-r", "120", pdf, join(pageDir, "page")];
          run("pdftoppm", args, { quiet: true });
          const pageNames = readdirSync(pageDir).filter((name) => name.endsWith(".png")).sort(compareCodePoints);
          if (pageNames.length !== metadata.pages) fail(`${document.id}/${mode} render 頁數不符`);
          for (const name of pageNames) assertRegularDirectFile(join(pageDir, name), pageDir, `${document.id}/${mode}/${name}`);
          run(pillowPython, [
            join(repoRoot, "tools", "make-contact-sheets.py"),
            pageDir,
            join(modeDir, "contact"),
          ]);
          const contacts = readdirSync(modeDir)
            .filter((name) => /^contact-\d+\.png$/u.test(name))
            .sort(compareCodePoints)
            .map((name) => {
              const path = assertRegularDirectFile(join(modeDir, name), modeDir, `${document.id}/${mode}/${name}`);
              return { path: `${document.id}/${mode}/${name}`, sha256: sha256(path) };
            });
          if (contacts.length === 0) fail(`${document.id}/${mode} 沒有 contact sheet`);
          modes[mode] = { pages: pageNames.length, contacts };
        }
        artifacts.push({
          id: document.id,
          pdf: `${document.slug}.pdf`,
          pdfSha256: sha256(pdf),
          pages: metadata.pages,
          modes,
        });
      }

      const reviewManifest = {
        schemaVersion: 1,
        set: setId,
        generatedAt: new Date().toISOString(),
        artifacts,
      };
      writeFileSync(join(stagingPath, "review-manifest.json"), `${JSON.stringify(reviewManifest, null, 2)}\n`, {
        encoding: "utf8",
        flag: "wx",
        mode: 0o600,
      });

      assertAbsent(backup, `${setId} review backup`);
      if (lstatIfPresent(reviewRoot)) {
        oldIdentity = assertCanonicalDirectory(reviewRoot, `${setId} review root`);
        renameSync(reviewRoot, backup);
        oldMoved = true;
        assertDirectoryIdentity(backup, oldIdentity, `${setId} review backup`);
      }
      renameSync(stagingPath, reviewRoot);
      newInstalled = true;
      assertDirectoryIdentity(reviewRoot, stagingIdentity, `${setId} review root`);
    } catch (error) {
      operationError = error;
    }

    if (operationError) {
      const rollbackErrors = [];
      if (newInstalled && lstatIfPresent(reviewRoot)) {
        try {
          safeRemoveOwnedDirectory(reviewRoot, reviewParent, stagingIdentity, `${setId} failed review root`);
          newInstalled = false;
        } catch (error) {
          rollbackErrors.push(`移除失敗的新 review：${error.message}`);
        }
      }
      if (oldMoved && lstatIfPresent(backup)) {
        try {
          if (lstatIfPresent(reviewRoot)) fail(`${setId} review rollback 目標已被占用`);
          assertDirectoryIdentity(backup, oldIdentity, `${setId} review backup`);
          renameSync(backup, reviewRoot);
          assertDirectoryIdentity(reviewRoot, oldIdentity, `${setId} restored review`);
          oldMoved = false;
        } catch (error) {
          rollbackErrors.push(`還原舊 review 失敗：${error.message}`);
        }
      }
      if (lstatIfPresent(stagingPath)) {
        try {
          safeRemoveOwnedDirectory(stagingPath, reviewParent, stagingIdentity, `${setId} review staging`);
        } catch (error) {
          rollbackErrors.push(`清理 review staging 失敗：${error.message}`);
        }
      }
      if (rollbackErrors.length > 0) fail(`${operationError.message}\nreview rollback 未完整完成：${rollbackErrors.join("；")}`);
      throw operationError;
    }

    if (oldMoved && lstatIfPresent(backup)) {
      try {
        safeRemoveOwnedDirectory(backup, reviewParent, oldIdentity, `${setId} obsolete review backup`);
      } catch (error) {
        process.stderr.write(`警告：新 review 已建立，但舊 backup 無法清理：${error.message}\n`);
      }
    }
    process.stdout.write(`視覺檢查圖已建立並綁定 PDF hash：${relative(repoRoot, reviewRoot)}\n`);
  });
}

if (process.argv[1] && resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  try {
    const registry = loadRegistry();
    const { command, setId, set, all } = parseCli(registry);
    if (command === "preflight" && all) {
      for (const [candidateId, candidateSet] of Object.entries(registry.sets)) preflightSet(candidateId, candidateSet);
    }
    if (command === "preflight" && !all) preflightSet(setId, set);
    if (command === "release") releaseSet(setId, set);
    if (command === "verify") verifySet(setId, set);
    if (command === "render") renderSet(setId, set);
  } catch (error) {
    process.stderr.write(`publication 失敗：${error.message}\n`);
    process.exit(1);
  }
}
