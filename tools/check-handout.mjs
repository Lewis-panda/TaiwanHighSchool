#!/usr/bin/env node

import { spawnSync } from "node:child_process";
import { existsSync, lstatSync, realpathSync, statSync } from "node:fs";
import { basename, dirname, extname, join, relative, resolve, sep } from "node:path";
import { fileURLToPath } from "node:url";

const scriptDir = dirname(fileURLToPath(import.meta.url));
const repoRoot = resolve(scriptDir, "..");
const repoRootReal = realpathSync(repoRoot);
const pdfRoot = join(repoRootReal, "output", "pdf");
const distRoot = join(repoRootReal, "dist");

function fail(message) {
  process.stderr.write(`PDF QA 失敗：${message}\n`);
  process.exitCode = 1;
}

function sanitizeDiagnostic(value) {
  return String(value)
    .replaceAll(repoRootReal, "<repo>")
    .replace(/\/Users\/[^/\s]+/g, "/Users/<user>")
    .replace(/[A-Za-z]:\\Users\\[^\\\s]+/g, "C:\\Users\\<user>");
}

function decodedValue(value) {
  let decoded = String(value);
  for (let index = 0; index < 2; index += 1) {
    decoded = decoded
      .replace(/%25/gi, "%")
      .replace(/%2f/gi, "/")
      .replace(/%5c/gi, "\\")
      .replace(/%3a/gi, ":");
    try {
      const next = decodeURIComponent(decoded);
      if (next === decoded) break;
      decoded = next;
    } catch {
      break;
    }
  }
  return decoded
    .replace(/&#x0*2f;|&#0*47;/gi, "/")
    .replace(/&#x0*5c;|&#0*92;/gi, "\\")
    .replace(/&#x0*3a;|&#0*58;/gi, ":");
}

function decodedForScan(value) {
  return decodedValue(value).normalize("NFKC");
}

function checkSensitive(raw, label) {
  const decoded = decodedForScan(raw);
  const forbidden = [
    [/\/Users(?:\/|$)/i, "macOS 使用者絕對路徑"],
    [/\/home\/[^/\s]+(?:\/|$)/i, "Linux 使用者絕對路徑"],
    [/[A-Za-z]:[\\/]Users[\\/]/i, "Windows 使用者絕對路徑"],
    [/(?:^|[\s("'`=])~[\\/]/m, "家目錄縮寫路徑"],
    [/\bfile\s*:/i, "file: URL"],
    [/\bLocalDocuments\b/i, "本機 LocalDocuments 路徑"],
    [/高中教材(?:[\\/]|$)/i, "私有高中教材路徑"],
  ];
  forbidden.forEach(([pattern, description]) => {
    if (pattern.test(decoded)) fail(`${label} 含${description}`);
  });
}

function checkUrls(raw, label) {
  checkSensitive(raw, `${label} URL 清單`);
  for (const line of raw.split("\n").slice(1)) {
    const match = line.match(/^\s*\d+\s+\S+\s+(.+?)\s*$/);
    if (!match) continue;
    const value = decodedForScan(match[1].trim());
    const scheme = value.match(/^([A-Za-z][A-Za-z0-9+.-]*):/)?.[1]?.toLowerCase();
    if (!["https", "mailto"].includes(scheme)) {
      fail(`${label} 含未允許的 PDF URL scheme：${scheme ?? "unknown"}`);
    }
    if (/[?&](?:access_?token|api_?key|secret|auth|authorization|password|signature|sig)=/i.test(value)) {
      fail(`${label} 的 PDF URL 疑似含憑證或簽章參數`);
    }
    try {
      const parsed = new URL(value);
      if (parsed.username || parsed.password) fail(`${label} 的 PDF URL 不得內嵌帳號或密碼`);
    } catch {
      fail(`${label} 含格式無效的 PDF URL`);
    }
  }
}

function run(command, args) {
  const result = spawnSync(command, args, {
    cwd: repoRoot,
    encoding: "utf8",
    maxBuffer: 32 * 1024 * 1024,
  });
  const commandLabel = basename(command);
  if (result.error) throw new Error(`${commandLabel} 無法執行：${sanitizeDiagnostic(result.error.message)}`);
  if (result.status !== 0) {
    throw new Error(`${commandLabel} 結束碼 ${result.status}：${sanitizeDiagnostic(result.stderr).trim()}`);
  }
  return result.stdout;
}

function infoFields(raw) {
  return Object.fromEntries(
    raw
      .split("\n")
      .map((line) => line.match(/^([^:]+):\s*(.*)$/))
      .filter(Boolean)
      .map((match) => [match[1].trim(), match[2].trim()]),
  );
}

function checkFonts(raw, label) {
  if (/\bType 3\b/.test(raw)) fail(`${label} 含 Type 3 字型`);

  let cjkFontFound = false;
  for (const line of raw.split("\n").slice(2)) {
    if (!line.trim()) continue;
    const fontName = line.trim().split(/\s+/u)[0];
    const normalizedName = fontName.replace(/^[A-Z]{6}\+/u, "");
    if (
      !normalizedName.startsWith("NotoSansTC")
      && !normalizedName.startsWith("NotoSansMath")
      && normalizedName !== "NotoSans-Regular"
    ) {
      fail(`${label} 含未釘選字型：${fontName}`);
    }
    if (normalizedName.startsWith("NotoSansTC")) cjkFontFound = true;
    const flags = line.match(/\s+(yes|no)\s+(yes|no)\s+(yes|no)\s+\d+\s+\d+\s*$/);
    if (!flags) continue;
    const [, embedded, , unicode] = flags;
    if (embedded !== "yes") fail(`${label} 有未嵌入字型：${line.trim()}`);
    if (unicode !== "yes") fail(`${label} 有不可對應 Unicode 的字型：${line.trim()}`);
  }
  if (!cjkFontFound) fail(`${label} 未嵌入釘選的 Noto Sans TC`);
}

function checkAttachments(raw, label) {
  checkSensitive(raw, `${label} 附件清單`);
  const match = raw.match(/^\s*(\d+) embedded files?\s*$/imu);
  if (!match) {
    fail(`${label} 無法辨識 pdfdetach 附件清單`);
    return;
  }
  const count = Number.parseInt(match[1], 10);
  if (count !== 0) fail(`${label} 含 ${count} 個嵌入附件`);
}

function checkPageGeometry(raw, label, pageCount) {
  const sizes = [...raw.matchAll(/^Page\s+(\d+)\s+size:\s+([0-9.]+)\s+x\s+([0-9.]+)\s+pts(?:\s+\([^\r\n]*\))?\s*$/gmu)];
  const rotations = [...raw.matchAll(/^Page\s+(\d+)\s+rot:\s+(-?\d+)\s*$/gmu)];
  if (sizes.length !== pageCount || rotations.length !== pageCount) {
    fail(`${label} 無法逐頁確認全部 ${pageCount} 頁的尺寸與旋轉`);
    return;
  }
  sizes.forEach((match, index) => {
    const page = Number.parseInt(match[1], 10);
    const width = Number.parseFloat(match[2]);
    const height = Number.parseFloat(match[3]);
    if (page !== index + 1 || Math.abs(width - 594.96) > 0.75 || Math.abs(height - 841.92) > 0.75) {
      fail(`${label} 第 ${page} 頁不是直式 A4（${width} x ${height} pts）`);
    }
  });
  rotations.forEach((match, index) => {
    const page = Number.parseInt(match[1], 10);
    const rotation = Number.parseInt(match[2], 10);
    if (page !== index + 1 || rotation !== 0) fail(`${label} 第 ${page} 頁旋轉角不是 0`);
  });
}

function checkGeneratorMetadata(info, label) {
  if (!/^Skia\/PDF(?:\s+m\d+)?$/u.test(info.Producer ?? "")) {
    fail(`${label} Producer 不是允許的 Skia/PDF 產線：${info.Producer || "missing"}`);
  }
  if (!/\bHeadlessChrome\/\d/u.test(info.Creator ?? "")) {
    fail(`${label} Creator 不是允許的 HeadlessChrome 產線：${info.Creator || "missing"}`);
  }
}

function checkText(raw, label, pageCount) {
  const forbidden = [
    "�",
    "Abstract",
    "$if",
    "$body",
    "undefined",
    "NaN",
  ];
  for (const token of forbidden) {
    if (raw.includes(token)) fail(`${label} 的可搜尋文字含禁止字串：${token}`);
  }
  checkSensitive(raw, `${label} 的可搜尋文字`);

  const pages = raw.replace(/\f\s*$/, "").split("\f");
  if (pages.length !== pageCount) {
    fail(`${label} 的文字頁數 ${pages.length} 與 PDF 頁數 ${pageCount} 不符`);
  }
  pages.forEach((page, index) => {
    if (!page.trim()) fail(`${label} 第 ${index + 1} 頁沒有可搜尋文字`);
  });
}

function resolveAllowedPdf(requestedPath, label) {
  if (lstatSync(requestedPath).isSymbolicLink()) {
    fail(`${label} 不得是 symlink`);
    return undefined;
  }
  const real = realpathSync(requestedPath);

  if (dirname(requestedPath) === pdfRoot) {
    if (!existsSync(pdfRoot) || lstatSync(pdfRoot).isSymbolicLink() || !lstatSync(pdfRoot).isDirectory()) {
      fail("output/pdf 必須是 repository 內的一般目錄，不得是 symlink");
      return undefined;
    }
    const pdfRootReal = realpathSync(pdfRoot);
    if (pdfRootReal !== pdfRoot || dirname(real) !== pdfRootReal) {
      fail(`${label} 不在 canonical output/pdf root 內`);
      return undefined;
    }
    return real;
  }

  const distRelative = relative(distRoot, requestedPath);
  const segments = distRelative.split(sep);
  if (segments.length !== 2 || segments.some((segment) => !segment)) {
    fail(`${label} 只允許位於 output/pdf 或 dist/<set-id>/ 的第一層`);
    return undefined;
  }
  const [setId] = segments;
  if (!/^[a-z0-9][a-z0-9._-]*$/.test(setId)) {
    fail(`${label} 的 dist set-id 不安全`);
    return undefined;
  }
  if (!existsSync(distRoot) || lstatSync(distRoot).isSymbolicLink()) {
    fail("dist 必須是 repository 內的一般目錄");
    return undefined;
  }
  const distRootReal = realpathSync(distRoot);
  if (distRootReal !== distRoot) {
    fail("dist 必須是 repository 內的 canonical 目錄，不得經 symlink 轉向");
    return undefined;
  }
  const setDir = join(distRoot, setId);
  if (!existsSync(setDir) || lstatSync(setDir).isSymbolicLink()) {
    fail(`${label} 的 dist set 目錄不存在或是 symlink`);
    return undefined;
  }
  const setDirReal = realpathSync(setDir);
  if (dirname(setDirReal) !== distRootReal || basename(setDirReal) !== setId) {
    fail(`${label} 的 dist set 目錄不是安全單層 canonical root`);
    return undefined;
  }
  if (dirname(real) !== setDirReal) {
    fail(`${label} 不得位於 dist set 的子目錄或經 symlink 逸出`);
    return undefined;
  }
  return real;
}

const inputs = process.argv.slice(2);
if (inputs.length === 0) {
  process.stderr.write("用法：node tools/check-handout.mjs <講義.pdf> [更多 PDF]\n");
  process.exit(1);
}

for (const input of inputs) {
  const requestedPath = resolve(repoRootReal, input);
  const label = basename(requestedPath);
  if (!existsSync(requestedPath)) {
    fail(`找不到 ${label}`);
    continue;
  }

  const pdfPath = resolveAllowedPdf(requestedPath, label);
  if (!pdfPath) continue;
  if (!statSync(pdfPath).isFile() || extname(pdfPath).toLowerCase() !== ".pdf") {
    fail(`${label} 不是一般 PDF 檔案`);
    continue;
  }

  try {
    const defaultMetadata = run("pdfinfo", [pdfPath]);
    const info = infoFields(defaultMetadata);
    const pageCount = Number.parseInt(info.Pages, 10);
    if (!Number.isInteger(pageCount) || pageCount < 1) fail(`${label} 頁數無效`);
    if (info.Tagged !== "yes") fail(`${label} 不是 Tagged PDF`);
    if (info.Encrypted !== "no") fail(`${label} 不應加密`);
    if (info.Suspects !== "no") fail(`${label} 被標記為 suspects`);
    if (info.JavaScript !== "no") fail(`${label} 不得含 PDF JavaScript`);
    if (info.Form !== "none") fail(`${label} 不得含互動表單`);
    if (!info.Title) fail(`${label} 缺少 Title metadata`);
    checkGeneratorMetadata(info, label);

    checkPageGeometry(
      run("pdfinfo", ["-f", "1", "-l", String(pageCount), "-box", pdfPath]),
      label,
      pageCount,
    );

    checkSensitive(defaultMetadata, `${label} metadata`);
    checkSensitive(run("pdfinfo", ["-custom", pdfPath]), `${label} custom metadata`);
    checkSensitive(run("pdfinfo", ["-meta", pdfPath]), `${label} XMP metadata`);
    checkUrls(run("pdfinfo", ["-url", pdfPath]), label);
    checkAttachments(run("pdfdetach", ["-list", pdfPath]), label);

    checkFonts(run("pdffonts", [pdfPath]), label);
    checkText(
      run("pdftotext", ["-layout", pdfPath, "-"]),
      label,
      pageCount,
    );

    if (!process.exitCode) {
      process.stdout.write(`${label}：${pageCount} 頁，逐頁 A4、無附件、Tagged、字型與文字層 QA 通過\n`);
    }
  } catch (error) {
    fail(`${label}：${error.message}`);
  }
}
