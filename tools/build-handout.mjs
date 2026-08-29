#!/usr/bin/env node

import { spawnSync } from "node:child_process";
import { createRequire } from "node:module";
import {
  existsSync,
  lstatSync,
  mkdirSync,
  readFileSync,
  readdirSync,
  realpathSync,
  statSync,
} from "node:fs";
import { homedir } from "node:os";
import {
  basename,
  delimiter,
  dirname,
  extname,
  isAbsolute,
  join,
  relative,
  resolve,
  sep,
} from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

import { normalizeChromiumPdfFile } from "./normalize-chromium-pdf.mjs";
import {
  assertNoPrivateText as assertNoPrivateTextShared,
  assertSafeCssText,
  assertSafeHtmlText,
  assertSafeSourceText,
  assertSafeSvgText,
  decodeLocalResourceTarget,
  inspectPandocAstSafety,
} from "./publication-safety.mjs";

const require = createRequire(import.meta.url);
const scriptDir = dirname(fileURLToPath(import.meta.url));
const repoRoot = resolve(scriptDir, "..");
const repoRootReal = realpathSync(repoRoot);
const contentRoot = join(repoRootReal, "content");
const markdownFormat = "markdown+yaml_metadata_block+fenced_divs+tex_math_dollars+smart";

function fail(message) {
  process.stderr.write(`錯誤：${message}\n`);
  process.exit(1);
}

function sanitizeDiagnostic(value) {
  return String(value)
    .replaceAll(repoRootReal, "<repo>")
    .replace(/\/Users\/[^/\s]+/g, "/Users/<user>")
    .replace(/[A-Za-z]:\\Users\\[^\\\s]+/g, "C:\\Users\\<user>");
}

function isWithin(root, candidate) {
  const rel = relative(root, candidate);
  return rel === "" || (rel !== ".." && !rel.startsWith(`..${sep}`) && !isAbsolute(rel));
}

function lstatIfPresent(path) {
  try {
    return lstatSync(path);
  } catch (error) {
    if (error?.code === "ENOENT") return undefined;
    throw error;
  }
}

function assertCanonicalDirectory(path, label) {
  const entry = lstatIfPresent(path);
  if (!entry) fail(`${label} 不存在`);
  if (entry.isSymbolicLink() || !entry.isDirectory()) fail(`${label} 必須是一般目錄，不得是 symlink`);
  if (realpathSync(path) !== path) fail(`${label} 的路徑不得經過 symlink`);
  if (!isWithin(repoRootReal, path)) fail(`${label} 必須位於 repository 內`);
  assertNotPrivatePath(path, label);
  return path;
}

function ensureDirectCanonicalDirectory(path, parent, label) {
  if (dirname(path) !== parent || path === parent) fail(`${label} 不是受控 parent 的直接子目錄`);
  assertCanonicalDirectory(parent, `${label} 的 parent`);
  if (!lstatIfPresent(path)) mkdirSync(path, { mode: 0o700 });
  return assertCanonicalDirectory(path, label);
}

function assertCanonicalFile(path, label) {
  const entry = lstatIfPresent(path);
  if (!entry || entry.isSymbolicLink() || !entry.isFile()) fail(`${label} 必須是一般檔案，不得是 symlink`);
  if (realpathSync(path) !== path) fail(`${label} 的路徑不得經過 symlink`);
  if (!isWithin(repoRootReal, path)) fail(`${label} 必須位於 repository 內`);
  assertNotPrivatePath(path, label);
  return path;
}

function displayPath(candidate) {
  const rel = relative(repoRootReal, candidate);
  return isWithin(repoRootReal, candidate) ? rel || "." : basename(candidate);
}

function runSafety(check, ...args) {
  try {
    return check(...args);
  } catch (error) {
    fail(error.message);
  }
}

function assertNoPrivateText(value, label) {
  return runSafety(assertNoPrivateTextShared, value, label);
}

function cleanLocalTarget(raw, label) {
  return runSafety(decodeLocalResourceTarget, raw, label, { allowParentSegments: true });
}

function assertNotPrivatePath(candidate, label) {
  const privateRoot = join(repoRootReal, "高中教材");
  if (isWithin(privateRoot, candidate)) fail(`${label} 指向不公開的高中教材目錄`);
}

function resolveLocalResource(raw, searchRoots, label) {
  const target = cleanLocalTarget(raw, label);

  const candidates = searchRoots.map((root) => resolve(root, target));
  for (const candidate of candidates) {
    if (!isWithin(repoRootReal, candidate)) fail(`${label} 的路徑逸出 repository：${raw}`);
    assertNotPrivatePath(candidate, label);
  }

  const existing = candidates.find((candidate) => existsSync(candidate));
  if (!existing) fail(`${label} 找不到本機資源：${raw}`);
  const real = realpathSync(existing);
  if (!isWithin(repoRootReal, real)) fail(`${label} 經 symlink 指向 repository 外：${raw}`);
  assertNotPrivatePath(real, label);
  if (!statSync(real).isFile()) fail(`${label} 不是一般檔案：${raw}`);
  return real;
}

function inspectPandocAst(ast, inputPath) {
  runSafety(inspectPandocAstSafety, ast, {
    label: `Markdown ${displayPath(inputPath)}`,
    onImage: (target) => {
      const resource = resolveLocalResource(target, [dirname(inputPath), repoRootReal], "圖片");
      if (extname(resource).toLowerCase() === ".svg") {
        runSafety(assertSafeSvgText, readFileSync(resource, "utf8"), `SVG ${displayPath(resource)}`);
      }
    },
  });
}

function inspectHtml(html) {
  runSafety(assertSafeHtmlText, html, "輸出 HTML");
}

function yamlScalar(markdown, key) {
  const frontmatter = markdown.match(/^---\s*\n([\s\S]*?)\n---\s*(?:\n|$)/);
  if (!frontmatter) return undefined;
  const match = frontmatter[1].match(new RegExp(`^${key}:\\s*["']?(.+?)["']?\\s*$`, "m"));
  return match?.[1]?.trim();
}

function sourceDateEpochFromUpdated(markdown) {
  const updated = yamlScalar(markdown, "updated");
  const match = updated?.match(/^(\d{4})-(\d{2})-(\d{2})$/u);
  if (!match) fail("front matter 的 updated 必須是有效 YYYY-MM-DD");
  const [, year, month, day] = match.map(Number);
  const date = new Date(Date.UTC(year, month - 1, day));
  if (
    year < 1970
    || year > 9999
    || date.getUTCFullYear() !== year
    || date.getUTCMonth() !== month - 1
    || date.getUTCDate() !== day
  ) {
    fail("front matter 的 updated 必須是 1970-01-01 至 9999-12-31 的有效曆日");
  }
  return Math.floor(date.getTime() / 1000);
}

function assertFrontmatterKeysUnique(markdown) {
  const frontmatter = markdown.match(/^---\s*\n([\s\S]*?)\n---\s*(?:\n|$)/u);
  if (!frontmatter) fail("來源缺少 YAML frontmatter");
  const keys = new Set();
  for (const line of frontmatter[1].split(/\r?\n/u)) {
    if (!line.trim() || /^\s/u.test(line)) continue;
    const key = line.match(/^([A-Za-z][A-Za-z0-9_-]*):/u)?.[1];
    if (!key) continue;
    if (keys.has(key)) fail(`frontmatter key 重複：${key}`);
    keys.add(key);
  }
}

function run(command, args, options = {}) {
  const result = spawnSync(command, args, {
    cwd: repoRoot,
    encoding: "utf8",
    stdio: "pipe",
    maxBuffer: 64 * 1024 * 1024,
  });
  const commandLabel = basename(command);
  if (result.error) fail(`${commandLabel} 無法執行：${sanitizeDiagnostic(result.error.message)}`);
  if (result.status !== 0) {
    if (result.stderr) process.stderr.write(`${sanitizeDiagnostic(result.stderr).trim()}\n`);
    fail(`${commandLabel} 結束碼 ${result.status}`);
  }
  if (!options.capture && result.stderr) process.stderr.write(sanitizeDiagnostic(result.stderr));
  return result.stdout ?? "";
}

function findCachedChromium() {
  const cacheRoot = join(homedir(), "Library", "Caches", "ms-playwright");
  if (!existsSync(cacheRoot)) return undefined;
  const folders = readdirSync(cacheRoot)
    .filter((name) => /^chromium-\d+$/.test(name))
    .sort((a, b) => b.localeCompare(a, undefined, { numeric: true }));
  for (const folder of folders) {
    const candidate = join(
      cacheRoot,
      folder,
      "chrome-mac-arm64",
      "Google Chrome for Testing.app",
      "Contents",
      "MacOS",
      "Google Chrome for Testing",
    );
    if (existsSync(candidate) && statSync(candidate).isFile()) return candidate;
  }
  return undefined;
}

const inputArg = process.argv[2];
if (!inputArg) fail("用法：node tools/build-handout.mjs <教材.md>");

const requestedInputPath = resolve(repoRootReal, inputArg);
if (!existsSync(requestedInputPath)) fail(`找不到來源檔：${basename(requestedInputPath)}`);
const standardSourceBasename = "學生講義.md";
if (basename(requestedInputPath) !== standardSourceBasename) {
  fail("新出版產線的標準來源只允許 學生講義.md；教師備課指南屬 legacy，不得由此工具建置");
}
assertCanonicalDirectory(contentRoot, "content");
const inputPath = assertCanonicalFile(requestedInputPath, "來源檔");
const contentRootReal = contentRoot;
if (!isWithin(contentRootReal, inputPath)) fail("來源檔必須位於 repository 的 content/ 目錄內");
if (extname(inputPath).toLowerCase() !== ".md") fail("來源檔必須是 .md");
if (basename(inputPath) !== standardSourceBasename) {
  fail("新出版產線的標準來源只允許 學生講義.md；教師備課指南屬 legacy，不得由此工具建置");
}

const markdown = readFileSync(inputPath, "utf8");
runSafety(assertSafeSourceText, markdown, `Markdown ${displayPath(inputPath)}`);
assertFrontmatterKeysUnique(markdown);
const declaredOutputSlug = yamlScalar(markdown, "output_slug");
if (!declaredOutputSlug) fail("front matter 必須提供 output_slug");
const outputSlug = declaredOutputSlug.normalize("NFC");
if (!/^[\p{L}\p{N}][\p{L}\p{N}._-]{0,119}$/u.test(outputSlug)) {
  fail("output_slug 只能包含 Unicode 字母、數字、點、底線與連字號，且不得含路徑分隔符");
}
const sourceDateEpoch = sourceDateEpochFromUpdated(markdown);

const outputRoot = join(repoRootReal, "output");
const htmlDir = join(outputRoot, "html");
const pdfDir = join(outputRoot, "pdf");
const tmpRoot = join(repoRootReal, "tmp");
const tempDir = join(tmpRoot, "pdfs");
ensureDirectCanonicalDirectory(outputRoot, repoRootReal, "output");
ensureDirectCanonicalDirectory(htmlDir, outputRoot, "output/html");
ensureDirectCanonicalDirectory(pdfDir, outputRoot, "output/pdf");
ensureDirectCanonicalDirectory(tmpRoot, repoRootReal, "tmp");
ensureDirectCanonicalDirectory(tempDir, tmpRoot, "tmp/pdfs");

const htmlPath = join(htmlDir, `${outputSlug}.html`);
const pdfPath = join(pdfDir, `${outputSlug}.pdf`);
const templatePath = join(repoRootReal, "templates", "handout.html");
const cssPath = join(repoRootReal, "styles", "handout.css");
const footerFontPath = join(repoRootReal, "assets", "fonts", "NotoSansMath-Regular.ttf");

for (const outputPath of [htmlPath, pdfPath]) {
  if (existsSync(outputPath) && lstatSync(outputPath).isSymbolicLink()) {
    fail(`拒絕覆寫 symlink 輸出：${displayPath(outputPath)}`);
  }
}

for (const fixedResource of [templatePath, cssPath, footerFontPath]) {
  const real = assertCanonicalFile(fixedResource, basename(fixedResource));
  assertNoPrivateText(readFileSync(real, "utf8"), displayPath(real));
}

const css = readFileSync(cssPath, "utf8");
const footerFontData = readFileSync(footerFontPath).toString("base64");
runSafety(assertSafeCssText, css, "handout.css", {
  onLocalUrl: (target) => resolveLocalResource(target, [dirname(cssPath)], "CSS 資源"),
});

const pandoc = process.env.HANDOUT_PANDOC_BIN ?? "pandoc";
let ast;
try {
  ast = JSON.parse(run(pandoc, [inputPath, `--from=${markdownFormat}`, "--to=json"], { capture: true }));
} catch (error) {
  fail(`無法解析 Pandoc AST：${error.message}`);
}
inspectPandocAst(ast, inputPath);

const resourcePath = [dirname(inputPath), repoRootReal].join(delimiter);
run(pandoc, [
  inputPath,
  `--from=${markdownFormat}`,
  "--to=html5",
  "--standalone",
  "--mathml",
  "--embed-resources",
  `--resource-path=${resourcePath}`,
  `--template=${templatePath}`,
  `--css=${cssPath}`,
  `--output=${htmlPath}`,
]);
inspectHtml(readFileSync(htmlPath, "utf8"));

let chromium;
try {
  ({ chromium } = require("playwright"));
} catch {
  fail("缺少 Playwright。請先執行 npm install，再執行 npx playwright install chromium。");
}

const configuredChrome = process.env.HANDOUT_CHROME_BIN;
const playwrightChrome = chromium.executablePath();
const systemChrome = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome";
const executablePath = [configuredChrome, playwrightChrome, systemChrome, findCachedChromium()]
  .find((candidate) => candidate && existsSync(candidate));

let browser;
try {
  browser = await chromium.launch({
    headless: true,
    ...(executablePath ? { executablePath } : {}),
  });
} catch {
  fail("Chromium 無法啟動；請檢查 Playwright 安裝或 HANDOUT_CHROME_BIN 設定");
}

let browserFailure;
try {
  const page = await browser.newPage({
    viewport: { width: 1280, height: 900 },
    javaScriptEnabled: false,
  });
  const htmlUrl = pathToFileURL(htmlPath).href;
  const blockedRequests = [];
  await page.route("**/*", async (route) => {
    const url = route.request().url();
    if (url === htmlUrl || url.startsWith("data:") || url === "about:blank") {
      await route.continue();
      return;
    }
    blockedRequests.push(url);
    await route.abort("blockedbyclient");
  });
  await page.goto(htmlUrl, { waitUntil: "networkidle" });
  if (blockedRequests.length > 0) {
    throw new Error(`輸出 HTML 嘗試載入 ${blockedRequests.length} 個非內嵌資源`);
  }
  await page.evaluate(async () => {
    await document.fonts.ready;
  });
  await page.emulateMedia({ media: "print" });

  const overflow = await page.evaluate(() =>
    [...document.querySelectorAll("body *")]
      .filter((element) => {
        const overflowX = getComputedStyle(element).overflowX;
        return !["hidden", "clip"].includes(overflowX)
          && element.scrollWidth > element.clientWidth + 2;
      })
      .slice(0, 8)
      .map((element) => ({
        tag: element.tagName,
        className: element.className,
        preview: element.textContent?.trim().slice(0, 80),
      })),
  );
  if (overflow.length > 0) {
    process.stderr.write(`警告：偵測到可能的水平溢位：${JSON.stringify(overflow, null, 2)}\n`);
  }

  const printOptions = {
    format: "A4",
    printBackground: true,
    margin: { top: "17mm", right: "17mm", bottom: "18mm", left: "17mm" },
    preferCSSPageSize: true,
  };

  await page.pdf({
    ...printOptions,
    path: pdfPath,
    displayHeaderFooter: true,
    headerTemplate: "<div></div>",
    footerTemplate: `<style>@font-face{font-family:HandoutFooter;src:url(data:font/ttf;base64,${footerFontData}) format('truetype');font-style:normal;font-weight:400}</style><div style="box-sizing:border-box;width:calc(100% - 34mm);margin:0 17mm;color:#7a8695;font-family:HandoutFooter,sans-serif;font-size:7.5pt;text-align:right;"><span class="pageNumber"></span></div>`,
    tagged: true,
    outline: true,
  });
  normalizeChromiumPdfFile(pdfPath, sourceDateEpoch);
} catch (error) {
  browserFailure = error;
} finally {
  try {
    await browser.close();
  } catch (error) {
    browserFailure ??= error;
  }
}
if (browserFailure) {
  const summary = sanitizeDiagnostic(browserFailure.message).split("\n", 1)[0];
  fail(`HTML/PDF 建置失敗：${summary}`);
}

process.stdout.write(`${JSON.stringify({
  html: relative(repoRootReal, htmlPath),
  pdf: relative(repoRootReal, pdfPath),
}, null, 2)}\n`);
