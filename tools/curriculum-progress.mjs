#!/usr/bin/env node

import { resolve } from "node:path";

import { loadCurriculum } from "./curriculum.mjs";
import { lintChapter } from "./scaffold-chapter.mjs";

const args = process.argv.slice(2);
const allowed = new Set(["--json", "--strict"]);
const unknown = args.filter((arg) => !allowed.has(arg));
if (unknown.length) throw new Error(`無法辨識參數：${unknown.join(", ")}`);
if (new Set(args).size !== args.length) throw new Error("參數不得重複");

const repoRoot = resolve(process.cwd());
const catalog = loadCurriculum(repoRoot);
const rows = [];

for (const document of catalog.documents) {
  try {
    const lint = lintChapter({
      repoRoot,
      course: document.courseDirectory,
      chapterCode: document.chapterCode,
    });
    rows.push({
      chapter: document.chapterKey,
      subject: document.identity.subject,
      status: "complete",
      assets: lint.registryDocuments[0].assets.length,
      detail: "lint passed",
    });
  } catch (error) {
    rows.push({
      chapter: document.chapterKey,
      subject: document.identity.subject,
      status: "draft",
      assets: 0,
      detail: String(error.message).split("\n", 1)[0],
    });
  }
}

const complete = rows.filter((row) => row.status === "complete").length;
const summary = { total: rows.length, complete, draft: rows.length - complete, rows };

if (args.includes("--json")) {
  process.stdout.write(`${JSON.stringify(summary, null, 2)}\n`);
} else {
  for (const row of rows) {
    process.stdout.write(`${row.status === "complete" ? "完成" : "草稿"}\t${row.chapter}\tSVG ${row.assets}\t${row.detail}\n`);
  }
  process.stdout.write(`curriculum progress：${complete}/${rows.length} 完成；${rows.length - complete} 仍為草稿\n`);
}

if (args.includes("--strict") && complete !== rows.length) process.exitCode = 1;

