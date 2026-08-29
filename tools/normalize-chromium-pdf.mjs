#!/usr/bin/env node

import {
  closeSync,
  fsyncSync,
  lstatSync,
  openSync,
  readFileSync,
  realpathSync,
  renameSync,
  statSync,
  unlinkSync,
  writeSync,
} from "node:fs";
import { randomUUID } from "node:crypto";
import { basename, dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

export class PdfNormalizationError extends Error {}

function reject(message) {
  throw new PdfNormalizationError(message);
}

function exactlyOneMatch(text, expression, label) {
  const matches = [...text.matchAll(expression)];
  if (matches.length !== 1) reject(`${label} 必須恰好出現一次`);
  return matches[0];
}

export function pdfDateFromSourceDateEpoch(value) {
  const raw = String(value);
  if (!/^(?:0|[1-9]\d*)$/u.test(raw)) reject("SOURCE_DATE_EPOCH 必須是非負整數秒");
  const seconds = Number(raw);
  if (!Number.isSafeInteger(seconds)) reject("SOURCE_DATE_EPOCH 超出安全整數範圍");
  const date = new Date(seconds * 1000);
  const year = date.getUTCFullYear();
  if (Number.isNaN(date.getTime()) || year < 1970 || year > 9999) {
    reject("SOURCE_DATE_EPOCH 必須落在 1970-01-01 到 9999-12-31");
  }
  const pad = (number) => String(number).padStart(2, "0");
  return `D:${String(year).padStart(4, "0")}${pad(date.getUTCMonth() + 1)}${pad(date.getUTCDate())}${pad(date.getUTCHours())}${pad(date.getUTCMinutes())}${pad(date.getUTCSeconds())}+00'00'`;
}

export function normalizeChromiumPdfBytes(input, sourceDateEpoch) {
  if (!Buffer.isBuffer(input)) reject("PDF 輸入必須是 Buffer");
  const text = input.toString("latin1");
  if (!text.startsWith("%PDF-")) reject("輸入不是 PDF");
  if ((text.match(/\bstartxref\b/gu) ?? []).length !== 1 || (text.match(/%%EOF/gu) ?? []).length !== 1) {
    reject("只接受單一 xref／EOF、未做 incremental update 的 Chromium PDF");
  }
  if (/\/ByteRange\s*\[|\/Type\s*\/Sig\b|\/FT\s*\/Sig\b/u.test(text)) {
    reject("拒絕修改含數位簽章或簽章欄位的 PDF");
  }
  if (/\/Type\s*\/Metadata\b|\/Metadata\s+\d+\s+\d+\s+R\b/u.test(text)) {
    reject("拒絕修改另含 XMP metadata stream 的 PDF");
  }

  const trailerMatches = [...text.matchAll(/^trailer\b/gmu)];
  if (trailerMatches.length !== 1) reject("只接受單一 classic PDF trailer");
  const trailerAt = trailerMatches[0].index;
  const trailerMatch = text.slice(trailerAt).match(/^trailer\s*<<([\s\S]*?)>>\s*startxref\s*(\d+)\s*%%EOF\s*$/u);
  if (!trailerMatch) reject("PDF trailer／startxref 格式不是受支援的 Chromium 輸出");
  const trailer = trailerMatch[1];
  if (/\/ID\s*\[/u.test(trailer)) reject("PDF trailer 含 /ID；拒絕留下未正規化的識別碼");
  if (/\/Encrypt\b/u.test(trailer)) reject("拒絕修改加密 PDF");
  const startXref = Number(trailerMatch[2]);
  if (!Number.isSafeInteger(startXref) || text.slice(startXref, startXref + 4) !== "xref") {
    reject("startxref 未指向 classic xref table");
  }

  const infoReference = exactlyOneMatch(trailer, /\/Info\s+(\d+)\s+(\d+)\s+R\b/gu, "trailer /Info reference");
  const objectNumber = infoReference[1];
  const generation = infoReference[2];
  const escapedObject = `${objectNumber}\\s+${generation}\\s+obj\\b`;
  const objectMatches = [...text.matchAll(new RegExp(`(^|[\\r\\n])(${escapedObject})`, "gmu"))];
  if (objectMatches.length !== 1) reject("trailer /Info 必須指向唯一的直接 object");
  const objectStart = objectMatches[0].index + objectMatches[0][1].length;
  const bodyStart = objectStart + objectMatches[0][2].length;
  const endObject = text.indexOf("endobj", bodyStart);
  if (endObject < 0 || endObject >= startXref) reject("/Info object 未在 xref 前正常結束");
  const infoBody = text.slice(bodyStart, endObject);
  if (!/^\s*<<[\s\S]*>>\s*$/u.test(infoBody) || /\bstream\b/u.test(infoBody)) {
    reject("/Info 必須是未壓縮的直接 dictionary");
  }
  if (!/\/Producer\s*\(Skia\/PDF(?:\s+m\d+)?\)/u.test(infoBody) || !infoBody.includes("HeadlessChrome/")) {
    reject("/Info provenance 不是允許的 Skia/PDF + HeadlessChrome");
  }

  for (const key of ["CreationDate", "ModDate"]) {
    if ((text.match(new RegExp(`/${key}\\b`, "gu")) ?? []).length !== 1) {
      reject(`/${key} 必須只存在於 /Info 且恰好一次`);
    }
  }
  const creation = exactlyOneMatch(infoBody, /\/CreationDate\s*\((D:\d{14}\+00'00')\)/gu, "/Info /CreationDate");
  const modification = exactlyOneMatch(infoBody, /\/ModDate\s*\((D:\d{14}\+00'00')\)/gu, "/Info /ModDate");
  if (creation[1] !== modification[1]) reject("Chromium CreationDate 與 ModDate 原值不一致");

  const replacement = Buffer.from(pdfDateFromSourceDateEpoch(sourceDateEpoch), "ascii");
  const normalized = Buffer.from(input);
  for (const match of [creation, modification]) {
    const relativeValueAt = match.index + match[0].indexOf(match[1]);
    const valueAt = bodyStart + relativeValueAt;
    if (Buffer.byteLength(match[1], "ascii") !== replacement.length) reject("日期正規化不得改變 PDF byte length");
    replacement.copy(normalized, valueAt);
  }
  if (normalized.length !== input.length) reject("日期正規化意外改變 PDF byte length");
  return {
    bytes: normalized,
    changed: !normalized.equals(input),
    originalPdfDate: creation[1],
    normalizedPdfDate: replacement.toString("ascii"),
  };
}

function sameFileIdentity(before, after) {
  return before.dev === after.dev && before.ino === after.ino && before.size === after.size;
}

export function normalizeChromiumPdfFile(pdfPath, sourceDateEpoch) {
  const absolute = resolve(pdfPath);
  const entry = lstatSync(absolute);
  if (entry.isSymbolicLink() || !entry.isFile() || realpathSync(absolute) !== absolute) {
    reject("PDF 必須是 canonical 一般檔案，不得是 symlink");
  }
  const before = statSync(absolute);
  const original = readFileSync(absolute);
  const result = normalizeChromiumPdfBytes(original, sourceDateEpoch);
  if (!result.changed) return { ...result, pdf: basename(absolute) };

  const current = statSync(absolute);
  if (!sameFileIdentity(before, current)) reject("PDF 在正規化期間已被替換或改變");
  const temporary = resolve(dirname(absolute), `.${basename(absolute)}.normalize-${process.pid}-${randomUUID()}`);
  let descriptor;
  try {
    descriptor = openSync(temporary, "wx", before.mode & 0o777);
    let offset = 0;
    while (offset < result.bytes.length) offset += writeSync(descriptor, result.bytes, offset);
    fsyncSync(descriptor);
    closeSync(descriptor);
    descriptor = undefined;
    const latestEntry = lstatSync(absolute);
    if (
      latestEntry.isSymbolicLink()
      || !latestEntry.isFile()
      || !sameFileIdentity(before, statSync(absolute))
      || !readFileSync(absolute).equals(original)
    ) reject("PDF 在 atomic replace 前已被替換或改變");
    renameSync(temporary, absolute);
  } catch (error) {
    if (descriptor !== undefined) closeSync(descriptor);
    try {
      unlinkSync(temporary);
    } catch (cleanupError) {
      if (cleanupError?.code !== "ENOENT") throw cleanupError;
    }
    throw error;
  }
  return { ...result, pdf: basename(absolute) };
}

const invokedAsScript = process.argv[1] && resolve(process.argv[1]) === fileURLToPath(import.meta.url);
if (invokedAsScript) {
  const [pdfPath, sourceDateEpoch, ...rest] = process.argv.slice(2);
  if (!pdfPath || sourceDateEpoch === undefined || rest.length > 0) {
    process.stderr.write("用法：node tools/normalize-chromium-pdf.mjs <PDF> <SOURCE_DATE_EPOCH>\n");
    process.exit(2);
  }
  try {
    const { bytes, ...summary } = normalizeChromiumPdfFile(pdfPath, sourceDateEpoch);
    process.stdout.write(`${JSON.stringify(summary)}\n`);
  } catch (error) {
    process.stderr.write(`錯誤：${error.message}\n`);
    process.exit(1);
  }
}
