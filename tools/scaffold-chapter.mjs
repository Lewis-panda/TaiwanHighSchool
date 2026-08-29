#!/usr/bin/env node

import { spawnSync } from "node:child_process";
import {
  existsSync,
  lstatSync,
  mkdirSync,
  readFileSync,
  readdirSync,
  realpathSync,
  rmSync,
  statSync,
  writeFileSync,
} from "node:fs";
import { dirname, isAbsolute, join, relative, resolve } from "node:path";
import { isProxy } from "node:util/types";
import { fileURLToPath } from "node:url";
import {
  leadingRegisteredChapterCode,
  resolveCourseIdentity,
} from "./course-identity.mjs";
import {
  assertSafeSourceText,
  assertSafeSvgText,
  inspectPandocAstSafety,
} from "./publication-safety.mjs";

const scriptPath = fileURLToPath(import.meta.url);
const defaultRepoRoot = realpathSync(resolve(dirname(scriptPath), ".."));
const markdownFormat = "markdown+yaml_metadata_block+fenced_divs+tex_math_dollars+smart";
const pandoc = process.env.HANDOUT_PANDOC_BIN ?? "pandoc";
const requiredFrontmatterKeys = [
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
const requiredChapterEntries = ["assets", "學生講義.md"].sort();
const optionalLegacyChapterEntries = new Set(["教師備課指南.md"]);
const scaffoldTodo = "TODO(SCAFFOLD):";

function fail(message) {
  throw new Error(message);
}

function compareCodePoints(left, right) {
  return left < right ? -1 : left > right ? 1 : 0;
}

function toPosix(path) {
  return path.split("\\").join("/");
}

function assertCanonicalDirectory(path, label) {
  if (!existsSync(path)) fail(`${label} 不存在：${path}`);
  const entry = lstatSync(path);
  if (entry.isSymbolicLink() || !entry.isDirectory()) fail(`${label} 必須是非 symlink 目錄：${path}`);
  if (realpathSync(path) !== path) fail(`${label} 必須是 canonical 目錄：${path}`);
  return { dev: entry.dev, ino: entry.ino };
}

function assertDirectRegularFile(path, parent, label) {
  assertCanonicalDirectory(parent, `${label} parent`);
  if (dirname(path) !== parent || !existsSync(path)) fail(`${label} 必須是直接存在的檔案：${path}`);
  const entry = lstatSync(path);
  if (entry.isSymbolicLink() || !entry.isFile()) fail(`${label} 必須是非 symlink 一般檔案：${path}`);
  if (realpathSync(path) !== path) fail(`${label} 必須是 canonical 檔案：${path}`);
}

function canonicalRepoRoot(candidate) {
  const resolved = resolve(candidate);
  if (!existsSync(resolved)) fail(`repository root 不存在：${resolved}`);
  const canonical = realpathSync(resolved);
  assertCanonicalDirectory(canonical, "repository root");
  return canonical;
}

function validateDate(value) {
  const match = value?.match(/^(\d{4})-(\d{2})-(\d{2})$/u);
  if (!match) fail("--updated 必須是有效的 YYYY-MM-DD");
  const [, year, month, day] = match.map(Number);
  const parsed = new Date(Date.UTC(year, month - 1, day));
  if (
    parsed.getUTCFullYear() !== year
    || parsed.getUTCMonth() !== month - 1
    || parsed.getUTCDate() !== day
  ) fail("--updated 必須是有效的 YYYY-MM-DD");
  return value;
}

function validateChapterTitle(value) {
  if (typeof value !== "string" || !value || value !== value.trim()) fail("--title 必須是非空且無首尾空白的章名（不要含章碼）");
  if (value !== value.normalize("NFC")) fail("--title 必須使用 NFC Unicode");
  if (/[\\/\u0000-\u001f\u007f]/u.test(value) || value.includes("..") || value.startsWith(".")) {
    fail("--title 含不安全的路徑或控制字元");
  }
  if (/^\s|\s$|\s{2,}/u.test(value)) fail("--title 空白格式不穩定；請只使用單一空白");
  if (leadingRegisteredChapterCode(value)) fail("--title 不得以任何已登記的章碼樣式開頭");
  return value;
}

function chapterIdentity(course, chapterCode) {
  try {
    return resolveCourseIdentity(course, chapterCode);
  } catch (error) {
    fail(`--course／--chapter-code 無效：${error.message}`);
  }
}

function yamlScalar(value) {
  return JSON.stringify(value);
}

function frontmatter(values) {
  return [
    "---",
    `title: ${yamlScalar(values.title)}`,
    `title-prefix: ${yamlScalar(values["title-prefix"])}`,
    `subtitle: ${yamlScalar(values.subtitle)}`,
    `subject: ${yamlScalar(values.subject)}`,
    `course: ${yamlScalar(values.course)}`,
    `audience: ${yamlScalar(values.audience)}`,
    `scope: ${yamlScalar(values.scope)}`,
    `updated: ${yamlScalar(values.updated)}`,
    `output_slug: ${yamlScalar(values.output_slug)}`,
    "---",
  ].join("\n");
}

function publicTemplate(identity, chapterTitle, updated) {
  const title = `${identity.chapterCode} ${chapterTitle}`;
  const prefix = "學生講義";
  const slug = `${title.replace(/\s+/gu, "-")}-${prefix}`;
  const metadata = {
    title,
    "title-prefix": prefix,
    subtitle: `${scaffoldTodo} 用一句話說明學生會理解什麼、為什麼要學與能用在哪裡`,
    subject: identity.subject,
    course: identity.course,
    audience: "學生版｜核心＋理解",
    scope: `${scaffoldTodo} 寫明現行課綱主線與延伸範圍`,
    updated,
    output_slug: slug,
  };
  const sections = [
    "## 1. 本章問題與用途",
    `${scaffoldTodo} 直接說明本章處理的問題、會建立的能力與至少一個具機制連結的實際用途。必要先備知識在首次使用時補足，不另設閱讀指令。`,
    "## 2. 核心概念",
    `${scaffoldTodo} 依情境／圖像 → 定義 → 原理或推導 → 例題 → 練習組織各主節。`,
    "## 3. 代表題與作答留白",
    `${scaffoldTodo} 以現行範圍與診斷目的原創題目，保留可自行作答的空間。`,
    "## 4. 完整詳解",
    `${scaffoldTodo} 對應題號交代推理、條件、單位／幾何意義與合理性檢查。`,
    "## 5. 核心整理",
    `${scaffoldTodo} 只收現行核心；C2–C4 不偽裝成必背考點。`,
  ];
  return `${frontmatter(metadata)}\n\n# ${title}\n\n${sections.join("\n\n")}\n`;
}

function privateEditorTemplate(identity, chapterTitle, updated) {
  return `# ${identity.chapterCode} ${chapterTitle}｜編輯判定（本機內部）

> 本檔由 \`.gitignore\` 排除，永不加入 publication manifest，也不直接輸出到 PDF。

## 版本基準

- 更新日期：${updated}
- ${scaffoldTodo} 記錄現行課綱條目與判定理由。
- ${scaffoldTodo} 記錄本機教材的精確檔名、頁碼、術語與題型校準。
- ${scaffoldTodo} 記錄官方大考固定窗口、逐題覆核狀態與證據限制。

## C0–C4 與呈現決策

${scaffoldTodo} 逐項記錄課綱關係；大考證據必須另軸判斷。

## 舊內容分流

${scaffoldTodo} 說明保留、重寫、降階、隔離或淘汰的理由，不因舊教材篇幅升格為主線。

## 發布前人工覆核

- [ ] 學生講義的核心敘事、檢核、代表題、留白與詳解完整。
- [ ] 學習目的、原理、真實用途與模型限制已直接寫給學生；不依賴另一冊補充。
- [ ] 公開稿不含本機路徑、內部檔名、舊制無標示內容或未覆核的考頻斷言。
`;
}

function strictFrontmatter(markdown, label) {
  const match = markdown.match(/^---\s*\n([\s\S]*?)\n---\s*(?:\n|$)/u);
  if (!match) fail(`${label} 缺少 YAML frontmatter`);
  const values = {};
  for (const [index, rawLine] of match[1].split(/\r?\n/u).entries()) {
    if (!rawLine.trim()) continue;
    if (/^\s/u.test(rawLine)) fail(`${label} frontmatter 第 ${index + 1} 行不得巢狀`);
    const line = rawLine.match(/^([A-Za-z][A-Za-z0-9_-]*):[ \t]*(.*)$/u);
    if (!line) fail(`${label} frontmatter 第 ${index + 1} 行不是單行 scalar`);
    const [, key, raw] = line;
    if (Object.hasOwn(values, key)) fail(`${label} frontmatter key 重複：${key}`);
    let value = raw.trim();
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
    if (typeof value !== "string" || !value) fail(`${label} frontmatter ${key} 不得為空`);
    values[key] = value;
  }
  if (JSON.stringify(Object.keys(values).sort()) !== JSON.stringify(requiredFrontmatterKeys)) {
    fail(`${label} frontmatter 必須恰含：${requiredFrontmatterKeys.join(", ")}`);
  }
  return values;
}

function scanPublicText(text, label, { allowTodos }) {
  try {
    assertSafeSourceText(text, label);
  } catch (error) {
    fail(`${label} 含私有或禁止字串：${error.message}`);
  }
  if (text.toLowerCase().includes("編輯判定.md".toLowerCase())) fail(`${label} 含私有或禁止字串：編輯判定.md`);
  if (!allowTodos && text.includes(scaffoldTodo)) fail(`${label} 尚有 ${scaffoldTodo}，不得登記發布`);
  const visible = stripNonRenderedMarkdown(text);
  const bareSpacingCommand = visible.match(/(?<![A-Za-z\\])(?:qquad|quad)\b/u)?.[0];
  if (bareSpacingCommand) {
    fail(`${label} 含缺少反斜線的 TeX 間距指令：${bareSpacingCommand}`);
  }
}

function validatePublicIdentity(identity, student) {
  const prefix = "學生講義";
  if (!student.title.startsWith(`${identity.chapterCode} `)) fail(`${prefix} title 必須以章碼開頭`);
  validateChapterTitle(student.title.slice(`${identity.chapterCode} `.length));
  if (student["title-prefix"] !== prefix) fail(`${prefix} title-prefix 不一致`);
  if (!student.audience.startsWith("學生版")) fail(`${prefix} audience 不一致`);
  if (student.subject !== identity.subject) fail(`${prefix} subject 應為 ${identity.subject}`);
  if (student.course !== identity.course) fail(`${prefix} course 應為 ${identity.course}`);
  validateDate(student.updated);
  const expectedSlug = `${student.title.replace(/\s+/gu, "-")}-${prefix}`;
  if (student.output_slug !== expectedSlug) fail(`${prefix} output_slug 應為 ${expectedSlug}`);
}

function stripNonRenderedMarkdown(markdown) {
  const noComments = markdown.replace(/<!--[\s\S]*?-->/gu, "");
  let fence;
  return noComments.split(/\r?\n/u).map((line) => {
    const marker = line.match(/^\s*(`{3,}|~{3,})/u)?.[1];
    if (marker) {
      if (!fence) fence = marker[0];
      else if (marker[0] === fence) fence = undefined;
      return "";
    }
    return fence ? "" : line;
  }).join("\n");
}

function pandocInlineText(value) {
  if (Array.isArray(value)) return value.map(pandocInlineText).join("");
  if (!value || typeof value !== "object") return "";
  if (value.t === "Str") return String(value.c ?? "");
  if (["Space", "SoftBreak", "LineBreak"].includes(value.t)) return " ";
  if (value.t === "Code" || value.t === "Math") return String(value.c?.[1] ?? "");
  return pandocInlineText(value.c);
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

function markdownLevelOneHeadings(markdown, label) {
  const result = spawnSync(pandoc, [
    `--from=${markdownFormat}`,
    "--to=json",
  ], {
    input: markdown,
    encoding: "utf8",
    maxBuffer: 64 * 1024 * 1024,
  });
  if (result.error) fail(`${label} 無法執行 Pandoc：${result.error.message}`);
  if (result.status !== 0) fail(`${label} 無法建立 Pandoc AST：${result.stderr?.trim() || `exit ${result.status}`}`);
  let ast;
  try {
    ast = JSON.parse(result.stdout);
  } catch (error) {
    fail(`${label} 的 Pandoc AST 不是有效 JSON：${error.message}`);
  }
  inspectPandocAstSafety(ast, { label });
  const headings = [];
  walkPandoc(ast, (node) => {
    const rawHtml = ["RawBlock", "RawInline"].includes(node.t) && node.c?.[0] === "html"
      ? String(node.c?.[1] ?? "").replace(/<!--[\s\S]*?-->/gu, "")
      : "";
    if (
      rawHtml
      && /<\s*\/?\s*h[1-6]\b/iu.test(rawHtml)
    ) {
      fail(`${label} 含 raw HTML heading；請使用 Markdown heading`);
    }
    if (node.t === "Header" && node.c?.[0] === 1) {
      headings.push(pandocInlineText(node.c?.[2]).replace(/\s+/gu, " ").trim());
    }
  });
  return headings;
}

function validateVisibleH1(markdown, values, label) {
  const headings = markdownLevelOneHeadings(markdown, label);
  const expected = values.title;
  if (headings.length !== 1 || headings[0] !== expected) {
    fail(`${label} 必須恰有一個 H1，且文字必須是：${expected}`);
  }
}

function scanSvg(path, label) {
  const svg = readFileSync(path, "utf8");
  assertSafeSvgText(svg, label);
}

function extractAssets(repoRoot, chapterDir, markdown, label) {
  const visible = stripNonRenderedMarkdown(markdown);
  const assets = [];
  const imagePattern = /!\[[^\]\n]*\]\(([^)\n]+)\)/gu;
  const matches = [...visible.matchAll(imagePattern)];
  const imageMarkers = [...visible.matchAll(/!\[/gu)].length;
  if (matches.length !== imageMarkers) fail(`${label} 含無法辨識或不允許的圖片語法`);
  for (const match of matches) {
    const target = match[1];
    if (!/^(?:assets\/|content\/assets\/)[^()\s]+\.svg$/u.test(target)) {
      fail(`${label} 圖片必須精確使用 assets/<檔名>.svg 或 content/assets/<檔名>.svg：${target}`);
    }
    const segments = target.split("/");
    if (
      target !== target.normalize("NFC")
      || /[\u0000-\u001f\u007f]/u.test(target)
      || segments.some((segment) => !segment || segment === "." || segment === "..")
      || target.includes("\\")
    ) {
      fail(`${label} 圖片路徑含不安全片段：${target}`);
    }
    const absolute = target.startsWith("assets/") ? join(chapterDir, target) : join(repoRoot, target);
    const parent = dirname(absolute);
    assertDirectRegularFile(absolute, parent, `${label} asset`);
    scanSvg(absolute, `${label} asset ${target}`);
    const repoRelative = toPosix(relative(repoRoot, absolute));
    if (isAbsolute(repoRelative) || repoRelative.startsWith("../")) fail(`${label} asset 逃離 repository`);
    if (repoRelative !== repoRelative.normalize("NFC")) fail(`${label} asset 必須使用 NFC Unicode`);
    assets.push(repoRelative);
  }
  return [...new Set(assets)].sort(compareCodePoints);
}

function gitIgnored(repoRoot, repoRelative) {
  const result = spawnSync("git", ["check-ignore", "-q", "--no-index", "--", repoRelative], {
    cwd: repoRoot,
    encoding: "utf8",
  });
  if (result.error) fail(`git check-ignore 無法執行：${result.error.message}`);
  if (![0, 1].includes(result.status)) fail(`git check-ignore 結束碼 ${result.status}：${result.stderr?.trim() ?? ""}`);
  return result.status === 0;
}

function assertPrivacyBoundary(repoRoot, identity, chapterDir, assetPaths) {
  const editor = toPosix(relative(repoRoot, join(chapterDir, "編輯判定.md")));
  if (!gitIgnored(repoRoot, editor)) fail(`${editor} 必須由 Git 明確忽略，避免本機教材路徑公開`);
  const studentPath = toPosix(relative(repoRoot, join(chapterDir, "學生講義.md")));
  if (gitIgnored(repoRoot, studentPath)) fail(`${studentPath} 是公開來源，不得被 Git 忽略`);
  for (const asset of assetPaths) {
    if (gitIgnored(repoRoot, asset)) fail(`${asset} 是公開資產，不得被 Git 忽略`);
  }
  if (!editor.startsWith(`content/${identity.courseDirectory}/${identity.chapterCode}/`)) fail("編輯判定路徑與章節身分不一致");
}

function assertPlannedPrivacyBoundary(repoRoot, identity) {
  const chapterRoot = `content/${identity.courseDirectory}/${identity.chapterCode}`;
  const editor = `${chapterRoot}/編輯判定.md`;
  if (!gitIgnored(repoRoot, editor)) fail(`${editor} 必須先由 Git 明確忽略`);
  for (const publicPath of [
    `${chapterRoot}/學生講義.md`,
    `${chapterRoot}/assets/公開資產.svg`,
  ]) {
    if (gitIgnored(repoRoot, publicPath)) fail(`${publicPath} 是預定公開來源，不得被 Git 忽略`);
  }
}

function registryDocuments(identity, title, studentAssets) {
  const slugStem = title.replace(/\s+/gu, "-");
  const chapterRoot = `content/${identity.courseDirectory}/${identity.chapterCode}`;
  return [
    {
      id: `${identity.idStem}-student`,
      audience: "student",
      source: `${chapterRoot}/學生講義.md`,
      slug: `${slugStem}-學生講義`,
      assets: studentAssets,
    },
  ];
}

function validateMinimumStructure(markdown, label) {
  const headings = [...markdown.matchAll(/^##\s+.+$/gmu)].map((match) => match[0]);
  if (headings.length < 5) fail(`${label} 至少需要五個可線性閱讀的主節`);
  const gimmickHeading = headings.find((heading) => /\bwhy\b|起點檢查|先備檢核|30\s*秒|停止線/iu.test(heading));
  if (gimmickHeading) {
    fail(`${label} 含閱讀指令或標語式標題：${gimmickHeading}`);
  }
  const requiredSignals = [
    ["本章問題與能力", /learning-map|問題地圖|本章問題|本章重點|本章將|核心問題/iu],
    ["原理／因果／推導", /原理|機制|推導|因為|因此|所以|由於/iu],
    ["實際用途／應用邊界", /實際用途|實務|應用|拿來做什麼|用在哪/iu],
    ["練習", /練習|檢核/iu],
    ["核心整理", /核心整理/iu],
    ["代表題", /代表題|整合題/iu],
    ["完整詳解", /詳解|完整解析/iu],
  ];
  for (const [name, pattern] of requiredSignals) {
    if (!pattern.test(markdown)) fail(`${label} 缺少作者規格的最低訊號：${name}`);
  }
}

function validateChapterAt(repoRoot, identity, { allowTodos, requirePrivateEditor }) {
  const contentRoot = join(repoRoot, "content");
  const courseRoot = join(contentRoot, identity.courseDirectory);
  assertCanonicalDirectory(contentRoot, "content root");
  assertCanonicalDirectory(courseRoot, `${identity.courseDirectory} course root`);
  const chapterDir = join(courseRoot, identity.chapterCode);
  assertCanonicalDirectory(chapterDir, `${identity.chapterCode} chapter root`);
  if (dirname(chapterDir) !== courseRoot) fail("章節目錄不是課程目錄的直接子目錄");
  const entries = readdirSync(chapterDir).sort(compareCodePoints);
  const requiredEntries = requirePrivateEditor
    ? [...requiredChapterEntries, "編輯判定.md"].sort(compareCodePoints)
    : requiredChapterEntries;
  const missingEntries = requiredEntries.filter((entry) => !entries.includes(entry));
  const unknownEntries = entries.filter((entry) => !requiredEntries.includes(entry) && !optionalLegacyChapterEntries.has(entry));
  if (missingEntries.length || unknownEntries.length) {
    fail(`${identity.chapterCode} 章根必須包含：${requiredEntries.join(", ")}；只額外容許 optional legacy 教師備課指南.md${missingEntries.length ? `；缺少：${missingEntries.join(", ")}` : ""}${unknownEntries.length ? `；不明項目：${unknownEntries.join(", ")}` : ""}`);
  }
  const assetsDir = join(chapterDir, "assets");
  assertCanonicalDirectory(assetsDir, `${identity.chapterCode} assets`);
  const studentPath = join(chapterDir, "學生講義.md");
  assertDirectRegularFile(studentPath, chapterDir, "學生講義.md");
  const studentMarkdown = readFileSync(studentPath, "utf8");
  scanPublicText(studentMarkdown, "學生講義.md", { allowTodos });
  if (requirePrivateEditor) {
    assertDirectRegularFile(join(chapterDir, "編輯判定.md"), chapterDir, "編輯判定.md");
  }
  const student = strictFrontmatter(studentMarkdown, "學生講義.md");
  validatePublicIdentity(identity, student);
  validateVisibleH1(studentMarkdown, student, "學生講義.md");
  validateMinimumStructure(studentMarkdown, "學生講義.md");
  const studentAssets = extractAssets(repoRoot, chapterDir, studentMarkdown, "學生講義.md");
  if (!allowTodos && ["物理", "化學"].includes(identity.subject) && studentAssets.length < 3) {
    fail(`${identity.subject}學生講義至少需要三張不同 SVG；每個主要模型仍須由人工確認有圖參與推理`);
  }
  let legacyTeacherAssets = [];
  const legacyTeacherPath = join(chapterDir, "教師備課指南.md");
  if (entries.includes("教師備課指南.md")) {
    assertDirectRegularFile(legacyTeacherPath, chapterDir, "optional legacy 教師備課指南.md");
    const legacyTeacherMarkdown = readFileSync(legacyTeacherPath, "utf8");
    scanPublicText(legacyTeacherMarkdown, "optional legacy 教師備課指南.md", { allowTodos: true });
    legacyTeacherAssets = extractAssets(repoRoot, chapterDir, legacyTeacherMarkdown, "optional legacy 教師備課指南.md");
  }
  const usedChapterAssets = new Set([...studentAssets, ...legacyTeacherAssets]
    .filter((path) => path.startsWith(`content/${identity.courseDirectory}/${identity.chapterCode}/assets/`))
    .map((path) => path.slice(path.lastIndexOf("/") + 1)));
  const diskAssets = readdirSync(assetsDir).sort(compareCodePoints);
  for (const filename of diskAssets) {
    const path = join(assetsDir, filename);
    assertDirectRegularFile(path, assetsDir, `${identity.chapterCode} asset ${filename}`);
    if (!filename.endsWith(".svg")) fail(`${identity.chapterCode} assets/ 只允許 SVG：${filename}`);
    if (!usedChapterAssets.has(filename)) fail(`${identity.chapterCode} assets/ 有未被學生稿或 optional legacy 教師稿引用的檔案：${filename}`);
  }
  assertPrivacyBoundary(repoRoot, identity, chapterDir, studentAssets);
  const documents = registryDocuments(identity, student.title, studentAssets);
  if (documents.some((document) => document.source.includes("編輯判定") || document.assets.some((asset) => asset.includes("編輯判定")))) {
    fail("registry documents 不得包含編輯判定");
  }
  return {
    chapter: `${identity.courseDirectory}/${identity.chapterCode}`,
    title: student.title,
    updated: student.updated,
    draftTodosAllowed: allowTodos,
    registryDocuments: documents,
  };
}

export function lintChapter({ repoRoot: root = defaultRepoRoot, course, chapterCode, allowTodos = false }) {
  const repoRoot = canonicalRepoRoot(root);
  const identity = chapterIdentity(course, chapterCode);
  return validateChapterAt(repoRoot, identity, { allowTodos, requirePrivateEditor: true });
}

function generatedFiles(identity, chapterTitle, updated) {
  return new Map([
    ["學生講義.md", publicTemplate(identity, chapterTitle, updated)],
    ["編輯判定.md", privateEditorTemplate(identity, chapterTitle, updated)],
  ]);
}

function safeRemoveOwnedChapter(chapterDir, courseRoot, identity) {
  if (!existsSync(chapterDir)) return;
  const current = lstatSync(chapterDir);
  if (current.isSymbolicLink() || !current.isDirectory() || current.dev !== identity.dev || current.ino !== identity.ino) {
    fail(`拒絕清理由其他程序替換的 scaffold 目錄：${chapterDir}`);
  }
  if (dirname(chapterDir) !== courseRoot || realpathSync(chapterDir) !== chapterDir) fail("拒絕清理非直接 canonical scaffold 目錄");
  rmSync(chapterDir, { recursive: true, force: false });
}

function safeRemoveOwnedFile(path, parent, identity) {
  const current = lstatSync(path, { throwIfNoEntry: false });
  if (!current) return;
  if (current.isSymbolicLink() || !current.isFile() || current.dev !== identity.dev || current.ino !== identity.ino) {
    fail(`拒絕清理由其他程序替換的私有編輯檔：${path}`);
  }
  assertCanonicalDirectory(parent, "private editor parent");
  if (dirname(path) !== parent || realpathSync(path) !== path) fail("拒絕清理非直接 canonical 私有編輯檔");
  rmSync(path, { force: false });
}

function createMode({ dryRun, writeApproved = false }) {
  if (dryRun !== undefined && typeof dryRun !== "boolean") fail("dryRun 必須是 boolean");
  if (typeof writeApproved !== "boolean") fail("writeApproved 必須是 boolean");
  if (dryRun === true && writeApproved) fail("dry-run 與 write-approved 互斥");
  if (dryRun === false && !writeApproved) fail("實際寫檔必須明示 writeApproved: true");
  return { dryRun: !writeApproved };
}

function approvedWriteFromOptions(options) {
  if (options === null || typeof options !== "object" || isProxy(options)) {
    fail("create options 必須是非 Proxy 的 plain 或 null-prototype object");
  }
  const prototype = Object.getPrototypeOf(options);
  if (prototype !== Object.prototype && prototype !== null) {
    fail("create options 必須是 plain 或 null-prototype object；不得以 prototype 繼承寫入授權");
  }
  const descriptor = Object.getOwnPropertyDescriptor(options, "writeApproved");
  if (!descriptor) {
    if ("writeApproved" in options) fail("writeApproved 必須是 own data property，不得繼承");
    return false;
  }
  if (!("value" in descriptor)) fail("writeApproved 必須是 own data property，不得使用 getter／setter");
  if (typeof descriptor.value !== "boolean") fail("writeApproved own data property 必須是 boolean");
  return descriptor.value === true;
}

export function createChapter(options) {
  const writeApproved = approvedWriteFromOptions(options);
  const {
    repoRoot: root = defaultRepoRoot,
    course,
    chapterCode,
    title,
    updated,
    dryRun,
  } = options;
  const mode = createMode({ dryRun, writeApproved });
  const repoRoot = canonicalRepoRoot(root);
  const identity = chapterIdentity(course, chapterCode);
  const chapterTitle = validateChapterTitle(title);
  validateDate(updated);
  const contentRoot = join(repoRoot, "content");
  const courseRoot = join(contentRoot, identity.courseDirectory);
  assertCanonicalDirectory(contentRoot, "content root");
  assertCanonicalDirectory(courseRoot, `${course} course root`);
  const chapterDir = join(courseRoot, identity.chapterCode);
  if (dirname(chapterDir) !== courseRoot) fail("章節目錄不是課程目錄的直接子目錄");
  if (existsSync(chapterDir)) fail(`拒絕覆寫既有章節：${toPosix(relative(repoRoot, chapterDir))}`);
  assertPlannedPrivacyBoundary(repoRoot, identity);
  const files = generatedFiles(identity, chapterTitle, updated);
  const planned = {
    chapter: `${identity.courseDirectory}/${identity.chapterCode}`,
    title: `${identity.chapterCode} ${chapterTitle}`,
    updated,
    dryRun: mode.dryRun,
    files: [...files.keys(), "assets/"],
    registryDocuments: registryDocuments(identity, `${identity.chapterCode} ${chapterTitle}`, []),
  };
  if (mode.dryRun) return planned;
  mkdirSync(chapterDir, { recursive: false, mode: 0o755 });
  const owned = statSync(chapterDir);
  try {
    mkdirSync(join(chapterDir, "assets"), { recursive: false, mode: 0o755 });
    for (const [filename, body] of files) {
      writeFileSync(join(chapterDir, filename), body, { encoding: "utf8", flag: "wx", mode: 0o644 });
    }
    const lint = lintChapter({ repoRoot, course, chapterCode, allowTodos: true });
    return { ...planned, lint };
  } catch (error) {
    safeRemoveOwnedChapter(chapterDir, courseRoot, owned);
    throw error;
  }
}

export function initPrivateEditor({ repoRoot: root = defaultRepoRoot, course, chapterCode }) {
  const repoRoot = canonicalRepoRoot(root);
  const identity = chapterIdentity(course, chapterCode);
  const contentRoot = join(repoRoot, "content");
  const courseRoot = join(contentRoot, identity.courseDirectory);
  assertCanonicalDirectory(contentRoot, "content root");
  assertCanonicalDirectory(courseRoot, `${identity.courseDirectory} course root`);
  const chapterDir = join(courseRoot, identity.chapterCode);
  assertCanonicalDirectory(chapterDir, `${identity.chapterCode} chapter root`);
  if (dirname(chapterDir) !== courseRoot) fail("章節目錄不是課程目錄的直接子目錄");
  const editorPath = join(chapterDir, "編輯判定.md");
  const existingEditor = lstatSync(editorPath, { throwIfNoEntry: false });
  if (existingEditor?.isSymbolicLink()) fail(`拒絕使用 symlink 私有編輯檔：${toPosix(relative(repoRoot, editorPath))}`);
  if (existingEditor) fail(`拒絕覆寫既有私有編輯檔：${toPosix(relative(repoRoot, editorPath))}`);

  const validated = validateChapterAt(repoRoot, identity, { allowTodos: false, requirePrivateEditor: false });
  const titlePrefix = `${identity.chapterCode} `;
  const chapterTitle = validateChapterTitle(validated.title.slice(titlePrefix.length));
  const body = privateEditorTemplate(identity, chapterTitle, validated.updated);
  writeFileSync(editorPath, body, { encoding: "utf8", flag: "wx", mode: 0o644 });
  const owned = lstatSync(editorPath);
  try {
    const lint = lintChapter({ repoRoot, course, chapterCode });
    return {
      ...validated,
      initializedPrivate: toPosix(relative(repoRoot, editorPath)),
      lint,
    };
  } catch (error) {
    safeRemoveOwnedFile(editorPath, chapterDir, owned);
    throw error;
  }
}

function usage() {
  return `用法：
  node tools/scaffold-chapter.mjs create --course <課程> --chapter-code <章碼> --title <不含章碼的章名> --updated YYYY-MM-DD [--dry-run | --write-approved] [--json]
  node tools/scaffold-chapter.mjs init-private --course <課程> --chapter-code <章碼> [--json]
  node tools/scaffold-chapter.mjs lint --course <課程> --chapter-code <章碼> [--allow-todos] [--json]

create 預設只做 dry-run；只有明示 --write-approved 才會建立空白骨架。
課程：必修數學、數學A、數學B、必修物理、選修物理I、必修化學、選修化學I、選修化學II、選修化學III、選修化學IV、選修化學V
`;
}

export function parseArguments(argv) {
  if (argv.length === 1 && ["--help", "-h"].includes(argv[0])) return { command: "help" };
  const [command, ...args] = argv;
  if (!new Set(["create", "init-private", "lint"]).has(command)) fail(usage().trim());
  const values = {
    command,
    dryRun: false,
    writeApproved: false,
    allowTodos: false,
    json: false,
  };
  const valueFlags = new Map([
    ["--course", "course"],
    ["--chapter-code", "chapterCode"],
    ["--title", "title"],
    ["--updated", "updated"],
  ]);
  const booleanFlags = new Map([
    ["--dry-run", "dryRun"],
    ["--write-approved", "writeApproved"],
    ["--allow-todos", "allowTodos"],
    ["--json", "json"],
  ]);
  const seen = new Set();
  for (let index = 0; index < args.length; index += 1) {
    const flag = args[index];
    if (seen.has(flag)) fail(`參數重複：${flag}`);
    seen.add(flag);
    if (booleanFlags.has(flag)) {
      values[booleanFlags.get(flag)] = true;
      continue;
    }
    const key = valueFlags.get(flag);
    if (!key || !args[index + 1] || args[index + 1].startsWith("--")) fail(`無法辨識或缺值參數：${flag}`);
    values[key] = args[index + 1];
    index += 1;
  }
  for (const key of ["course", "chapterCode"]) if (!values[key]) fail(`缺少 --${key === "chapterCode" ? "chapter-code" : key}`);
  if (command === "create") {
    for (const key of ["title", "updated"]) if (!values[key]) fail(`create 缺少 --${key}`);
    if (values.allowTodos) fail("create 不接受 --allow-todos；新骨架會自動以草稿模式自檢");
    if (values.dryRun && values.writeApproved) fail("--dry-run 與 --write-approved 互斥");
    values.dryRun = !values.writeApproved;
  } else if (command === "lint") {
    if (values.title || values.updated || values.dryRun || values.writeApproved) {
      fail("lint 不接受 --title、--updated、--dry-run 或 --write-approved");
    }
  } else if (values.title || values.updated || values.dryRun || values.writeApproved || values.allowTodos) {
    fail("init-private 只接受 --course、--chapter-code 與 --json");
  }
  return values;
}

export function scaffoldResultStatus(result) {
  if (result.initializedPrivate) return `已建立 ${result.initializedPrivate}，正式 lint 通過`;
  if (result.dryRun) return "dry-run 通過，未寫入";
  return "已建立空白骨架；只建骨架，未登記 publishing/sets.json，未發布 PDF";
}

function printResult(result, json) {
  if (json) {
    process.stdout.write(`${JSON.stringify(result, null, 2)}\n`);
    return;
  }
  const status = scaffoldResultStatus(result);
  process.stdout.write(`${result.chapter}：${status}\n`);
  process.stdout.write("publishing/sets.json 的 documents 候選片段：\n");
  process.stdout.write(`${JSON.stringify(result.registryDocuments, null, 2)}\n`);
}

export function main(argv = process.argv.slice(2)) {
  const options = parseArguments(argv);
  if (options.command === "help") {
    process.stdout.write(usage());
    return;
  }
  const result = options.command === "create"
    ? createChapter(options)
    : options.command === "init-private" ? initPrivateEditor(options) : lintChapter(options);
  printResult(result, options.json);
}

const invokedPath = process.argv[1] ? resolve(process.argv[1]) : "";
if (invokedPath === scriptPath) {
  try {
    main();
  } catch (error) {
    process.stderr.write(`scaffold 失敗：${error.message}\n`);
    process.exitCode = 1;
  }
}
