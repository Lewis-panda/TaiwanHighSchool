#!/usr/bin/env node

import assert from "node:assert/strict";
import { mkdtempSync, readFileSync, realpathSync, rmSync, symlinkSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import {
  normalizeChromiumPdfBytes,
  normalizeChromiumPdfFile,
  PdfNormalizationError,
  pdfDateFromSourceDateEpoch,
} from "./normalize-chromium-pdf.mjs";

const epoch = 1_787_529_600;
const expectedDate = "D:20260824000000+00'00'";

function fixture(date, additions = {}) {
  const infoExtra = additions.info ?? "";
  const catalogExtra = additions.catalog ?? "";
  const beforeXref = `%PDF-1.4\n1 0 obj\n<</Title (fixture)\n/Creator (Mozilla/5.0 HeadlessChrome/145.0.0.0 Safari/537.36)\n/Producer (Skia/PDF m145)\n${infoExtra}/CreationDate (${date})\n/ModDate (${date})>>\nendobj\n2 0 obj\n<</Type /Catalog${catalogExtra}>>\nendobj\n`;
  const trailerExtra = additions.trailer ?? "";
  return Buffer.from(`${beforeXref}xref\n0 3\n0000000000 65535 f \n0000000009 00000 n \n0000000200 00000 n \ntrailer\n<</Size 3\n/Root 2 0 R\n/Info 1 0 R${trailerExtra}>>\nstartxref\n${Buffer.byteLength(beforeXref, "latin1")}\n%%EOF\n`, "latin1");
}

function mustReject(bytes, pattern) {
  assert.throws(
    () => normalizeChromiumPdfBytes(bytes, epoch),
    (error) => error instanceof PdfNormalizationError && pattern.test(error.message),
  );
}

assert.equal(pdfDateFromSourceDateEpoch(epoch), expectedDate);
const first = fixture("D:20260823210052+00'00'");
const second = fixture("D:20260823235959+00'00'");
const normalizedFirst = normalizeChromiumPdfBytes(first, epoch);
const normalizedSecond = normalizeChromiumPdfBytes(second, epoch);
assert.equal(normalizedFirst.bytes.length, first.length);
assert.equal(normalizedSecond.bytes.length, second.length);
assert.deepEqual(normalizedFirst.bytes, normalizedSecond.bytes);
assert.equal(normalizedFirst.bytes.toString("latin1").split(expectedDate).length - 1, 2);
assert.equal(normalizeChromiumPdfBytes(normalizedFirst.bytes, epoch).changed, false);

mustReject(fixture("D:20260823210052+00'00'", { trailer: "\n/ID [<00><00>]" }), /\/ID/u);
mustReject(fixture("D:20260823210052+00'00'", { info: "/ByteRange [0 1 2 3]\n" }), /簽章/u);
mustReject(fixture("D:20260823210052+00'00'", { catalog: "\n/Metadata 9 0 R" }), /XMP/u);
mustReject(fixture("D:20260823210052Z"), /CreationDate/u);
mustReject(Buffer.from(first.toString("latin1").replace("/ModDate", "/BadDate"), "latin1"), /ModDate/u);

const directory = realpathSync(mkdtempSync(join(tmpdir(), "chromium-pdf-normalizer-test-")));
try {
  const pdf = join(directory, "fixture.pdf");
  writeFileSync(pdf, first);
  const result = normalizeChromiumPdfFile(pdf, epoch);
  assert.equal(result.normalizedPdfDate, expectedDate);
  assert.deepEqual(readFileSync(pdf), normalizedFirst.bytes);
  const link = join(directory, "fixture-link.pdf");
  symlinkSync(pdf, link);
  assert.throws(() => normalizeChromiumPdfFile(link, epoch), /symlink/u);
} finally {
  rmSync(directory, { recursive: true, force: true });
}

process.stdout.write("normalize-chromium-pdf：正向、idempotence、/ID、簽章、XMP、日期格式與 symlink 測試通過\n");
