import { existsSync, readFileSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

import { createChapter } from "./scaffold-chapter.mjs";

const repoRoot = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const writeApproved = process.argv.slice(2).includes("--write-approved");
const unknown = process.argv.slice(2).filter((arg) => arg !== "--write-approved" && arg !== "--dry-run");
if (unknown.length) throw new Error(`無法辨識參數：${unknown.join(", ")}`);
if (writeApproved && process.argv.slice(2).includes("--dry-run")) {
  throw new Error("--write-approved 與 --dry-run 互斥");
}

const catalog = JSON.parse(readFileSync(join(repoRoot, "publishing", "curriculum.json"), "utf8"));
if (catalog.schemaVersion !== 1 || !Array.isArray(catalog.documents)) {
  throw new Error("publishing/curriculum.json schema 不符");
}

let created = 0;
let existing = 0;
for (const document of catalog.documents) {
  const chapter = join(repoRoot, "content", document.courseDirectory, document.chapterCode);
  if (existsSync(chapter)) {
    process.stdout.write(`既存：${document.courseDirectory}/${document.chapterCode}\n`);
    existing += 1;
    continue;
  }
  const result = createChapter({
    repoRoot,
    course: document.courseDirectory,
    chapterCode: document.chapterCode,
    title: document.title,
    updated: "2026-08-29",
    dryRun: !writeApproved,
    writeApproved,
  });
  process.stdout.write(`${writeApproved ? "建立" : "乾跑"}：${document.courseDirectory}/${document.chapterCode}\n`);
  if (!result.dryRun) created += 1;
}

process.stdout.write(`curriculum scaffold：${catalog.documents.length} 章；既存 ${existing}；${writeApproved ? `新建 ${created}` : "未寫入"}\n`);
