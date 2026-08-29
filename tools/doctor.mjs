#!/usr/bin/env node

import { spawnSync } from "node:child_process";
import { createHash } from "node:crypto";
import { createRequire } from "node:module";
import {
  accessSync,
  constants,
  existsSync,
  lstatSync,
  readFileSync,
  realpathSync,
  statSync,
} from "node:fs";
import { platform } from "node:os";
import {
  delimiter,
  dirname,
  extname,
  isAbsolute,
  join,
  relative,
  resolve,
} from "node:path";
import { fileURLToPath } from "node:url";

const require = createRequire(import.meta.url);
const scriptDir = dirname(fileURLToPath(import.meta.url));
const repoRoot = resolve(scriptDir, "..");
const failures = [];
const warnings = [];

function print(kind, message) {
  process.stdout.write(`${kind} ${message}\n`);
}

function pass(message) {
  print("✓", message);
}

function warn(message) {
  warnings.push(message);
  print("⚠", message);
}

function fail(message) {
  failures.push(message);
  print("✗", message);
}

function isExecutable(path) {
  try {
    if (!statSync(path).isFile()) return false;
    accessSync(path, platform() === "win32" ? constants.F_OK : constants.X_OK);
    return true;
  } catch {
    return false;
  }
}

function findExecutable(command) {
  if (!command) return undefined;

  const hasPath = isAbsolute(command) || command.includes("/") || command.includes("\\");
  const directories = hasPath
    ? [repoRoot]
    : (process.env.PATH ?? "")
        .split(delimiter)
        .map((entry) => entry.replace(/^"|"$/g, ""))
        .filter(Boolean);

  const windowsExtensions = (process.env.PATHEXT ?? ".COM;.EXE;.BAT;.CMD")
    .split(";")
    .filter(Boolean);
  const extensions = platform() === "win32" && !extname(command)
    ? ["", ...windowsExtensions]
    : [""];

  for (const directory of directories) {
    for (const extension of extensions) {
      const candidate = hasPath
        ? resolve(repoRoot, `${command}${extension}`)
        : join(directory, `${command}${extension}`);
      if (isExecutable(candidate)) return candidate;
    }
  }
  return undefined;
}

function firstOutputLine(result) {
  return `${result.stdout ?? ""}\n${result.stderr ?? ""}`
    .split(/\r?\n/)
    .map((line) => line.trim())
    .find(Boolean);
}

function checkCommand(label, command, args) {
  const executable = findExecutable(command);
  if (!executable) {
    fail(`${label}：PATH 中找不到 ${command}`);
    return undefined;
  }

  const result = spawnSync(executable, args, {
    cwd: repoRoot,
    encoding: "utf8",
    maxBuffer: 4 * 1024 * 1024,
  });
  if (result.error || result.status !== 0) {
    const detail = result.error?.message ?? firstOutputLine(result) ?? `結束碼 ${result.status}`;
    fail(`${label}：無法執行（${detail}）`);
    return undefined;
  }

  pass(`${label}：${firstOutputLine(result) ?? "可執行"}｜${executable}`);
  return executable;
}

function checkCommandPresence(label, command) {
  const executable = findExecutable(command);
  if (!executable) {
    fail(`${label}：PATH 中找不到 ${command}`);
    return undefined;
  }
  pass(`${label}：可執行｜${executable}`);
  return executable;
}

function checkPlaywrightChromium() {
  try {
    const playwrightPackage = require("playwright/package.json");
    const { chromium } = require("playwright");
    const executable = chromium.executablePath();
    if (!executable || !isExecutable(executable)) {
      fail(
        `Playwright Chromium：playwright ${playwrightPackage.version} 已安裝，但找不到瀏覽器；請執行 npx playwright install chromium`,
      );
      return;
    }
    pass(`Playwright Chromium：playwright ${playwrightPackage.version}｜${executable}`);
  } catch (error) {
    fail(`Playwright Chromium：${error.message}`);
  }
}

function checkPillow() {
  const python = findExecutable("python3") ?? findExecutable("python");
  if (!python) {
    warn("Pillow：找不到 Python；只影響聯絡表，不影響 HTML／PDF 建置與機械 QA");
    return;
  }

  const result = spawnSync(
    python,
    ["-c", "from PIL import __version__; print(__version__)"],
    { cwd: repoRoot, encoding: "utf8" },
  );
  if (result.error || result.status !== 0) {
    warn(`Pillow：${python} 未安裝 PIL；只影響聯絡表`);
    return;
  }
  pass(`Pillow：${result.stdout.trim()}｜${python}`);
}

const bundledFonts = Object.freeze({
  "NotoSansTC-Regular.ttf": "1236fcc65f1ab85f75f98c38b61531de1bca5efb0cc20610f961cecd03af2071",
  "NotoSansTC-Bold.ttf": "8fb290ad6f55d99296d3a2b289bfc7bf45e9febec178e5d65e9caa5f5e783964",
  "NotoSansMath-Regular.ttf": "80b61fd613d3519197e64fff6f7e71fdc7f3e6526440ea4115b554ef7fd59af7",
  "NotoSans-Regular.ttf": "b85c38ecea8a7cfb39c24e395a4007474fa5a4fc864f6ee33309eb4948d232d5",
});

function checkBundledFonts() {
  const directory = join(repoRoot, "assets", "fonts");
  for (const [filename, expectedDigest] of Object.entries(bundledFonts)) {
    const path = join(directory, filename);
    if (!existsSync(path)) {
      fail(`內附字型：缺少 ${filename}`);
      return;
    }
    const entry = lstatSync(path);
    if (entry.isSymbolicLink() || !entry.isFile() || realpathSync(path) !== path) {
      fail(`內附字型：${filename} 必須是 canonical 一般檔案，不得是 symlink`);
      return;
    }
    const digest = createHash("sha256").update(readFileSync(path)).digest("hex");
    if (digest !== expectedDigest) {
      fail(`內附字型：${filename} 的 SHA-256 不符固定版本`);
      return;
    }
  }
  for (const license of ["NotoSansTC-OFL.txt", "OFL.txt", "README.md", "provenance.json"]) {
    const path = join(directory, license);
    if (!existsSync(path) || lstatSync(path).isSymbolicLink() || !lstatSync(path).isFile()) {
      fail(`內附字型：缺少一般來源／授權檔 ${license}`);
      return;
    }
  }
  let provenance;
  try {
    provenance = JSON.parse(readFileSync(join(directory, "provenance.json"), "utf8"));
  } catch (error) {
    fail(`內附字型：provenance.json 無法解析（${error.message}）`);
    return;
  }
  if (provenance?.schemaVersion !== 1 || !Array.isArray(provenance.fonts)) {
    fail("內附字型：provenance.json schema 無效");
    return;
  }
  const provenanceHashes = new Map(provenance.fonts.map((font) => [font?.file, font?.sha256]));
  for (const [filename, expectedDigest] of Object.entries(bundledFonts)) {
    if (provenanceHashes.get(filename) !== expectedDigest) {
      fail(`內附字型：provenance.json 與 ${filename} 的固定 SHA-256 不一致`);
      return;
    }
  }
  if (
    provenance.fonts.length !== Object.keys(bundledFonts).length
    || provenanceHashes.size !== Object.keys(bundledFonts).length
  ) {
    fail("內附字型：provenance.json 的字型集合不是固定白名單");
    return;
  }
  pass(`內附字型：${Object.keys(bundledFonts).length} 檔 SHA-256 固定，無需系統中文字型`);
}

function extractImageTargets(markdown) {
  const targets = [];
  const markdownImage = /!\[[^\]]*\]\(\s*(?:<([^>]+)>|([^\s)]+))(?:\s+["'][^"']*["'])?\s*\)/g;
  const htmlImage = /<img\b[^>]*\bsrc\s*=\s*["']([^"']+)["'][^>]*>/gi;

  for (const match of markdown.matchAll(markdownImage)) targets.push(match[1] ?? match[2]);
  for (const match of markdown.matchAll(htmlImage)) targets.push(match[1]);
  return targets;
}

function decodedLocalTarget(rawTarget) {
  if (/^(?:data:|https?:|blob:)/i.test(rawTarget)) return undefined;
  const withoutFragment = rawTarget.split(/[?#]/, 1)[0];
  try {
    return decodeURIComponent(withoutFragment);
  } catch {
    return withoutFragment;
  }
}

function resolveImage(sourcePath, target) {
  if (isAbsolute(target)) return existsSync(target) ? target : undefined;
  const candidates = [resolve(dirname(sourcePath), target), resolve(repoRoot, target)];
  return candidates.find((candidate) => existsSync(candidate) && statSync(candidate).isFile());
}

function publicationReviewSources() {
  const registryPath = join(repoRoot, "publishing", "sets.json");
  if (!existsSync(registryPath)) {
    fail("送審 manifest：找不到 publishing/sets.json");
    return { setId: "unknown", sources: [] };
  }
  try {
    const registry = JSON.parse(readFileSync(registryPath, "utf8"));
    const setId = registry.defaultSet;
    const documents = registry.sets?.[setId]?.documents;
    if (!setId || !Array.isArray(documents) || documents.length === 0) {
      fail("送審 manifest：defaultSet 沒有 documents");
      return { setId: setId ?? "unknown", sources: [] };
    }
    const sources = documents.map((document) => document.source);
    if (sources.some((source) => typeof source !== "string" || !source)) {
      fail("送審 manifest：document source 無效");
      return { setId, sources: [] };
    }
    pass(`送審 manifest：${setId}，${sources.length} 份文件`);
    return { setId, sources };
  } catch (error) {
    fail(`送審 manifest：JSON 無法解析（${error.message}）`);
    return { setId: "unknown", sources: [] };
  }
}

function checkReviewImages() {
  const { setId, sources } = publicationReviewSources();
  let totalImages = 0;
  let foundImages = 0;

  for (const source of sources) {
    const sourcePath = resolve(repoRoot, source);
    if (!existsSync(sourcePath)) {
      fail(`送審來源：找不到 ${source}`);
      continue;
    }

    const targets = extractImageTargets(readFileSync(sourcePath, "utf8"));
    let documentImages = 0;
    let documentFound = 0;
    for (const rawTarget of targets) {
      const target = decodedLocalTarget(rawTarget);
      if (!target) {
        warn(`${source}：外部或內嵌圖片未作本機存在性檢查：${rawTarget}`);
        continue;
      }
      documentImages += 1;
      totalImages += 1;
      const imagePath = resolveImage(sourcePath, target);
      if (!imagePath) {
        fail(`${source}：找不到引用圖片 ${target}`);
      } else {
        documentFound += 1;
        foundImages += 1;
      }
    }
    pass(`${source}：本機圖片 ${documentFound}/${documentImages}`);
  }

  if (sources.length > 0 && foundImages === totalImages) {
    pass(`${setId}：${sources.length} 份 Markdown 引用圖片共 ${foundImages} 個，全部存在`);
  }
}

function checkPublicationPreflight() {
  const result = spawnSync(process.execPath, [join(repoRoot, "tools", "publication.mjs"), "preflight", "--all"], {
    cwd: repoRoot,
    encoding: "utf8",
    maxBuffer: 64 * 1024 * 1024,
  });
  if (result.error) {
    fail(`出版 preflight 無法執行：${result.error.message}`);
    return;
  }
  if (result.status !== 0) {
    const detail = [result.stdout, result.stderr].filter(Boolean).join("\n").trim();
    fail(`出版 preflight 未通過${detail ? `：${detail}` : ""}`);
    return;
  }
  const summary = result.stdout.trim().split(/\r?\n/u).at(-1);
  pass(`出版 preflight：${summary || "通過"}`);
}

process.stdout.write("講義 PDF 產線 doctor\n\n");
pass(`Node.js：${process.version}｜${process.execPath}`);
checkCommand("Pandoc", process.env.HANDOUT_PANDOC_BIN ?? "pandoc", ["--version"]);
checkCommand("pdfinfo", "pdfinfo", ["-v"]);
checkCommand("pdffonts", "pdffonts", ["-v"]);
checkCommand("pdftotext", "pdftotext", ["-v"]);
checkCommand("pdftoppm", "pdftoppm", ["-v"]);
checkCommandPresence("pdfdetach", "pdfdetach");
checkPlaywrightChromium();
checkPillow();
checkBundledFonts();
checkPublicationPreflight();

process.stdout.write("\n");
if (failures.length > 0) {
  process.stdout.write(`結果：失敗（${failures.length} 個錯誤，${warnings.length} 個警告）\n`);
  process.exitCode = 1;
} else {
  process.stdout.write(`結果：通過（0 個錯誤，${warnings.length} 個警告）\n`);
}
