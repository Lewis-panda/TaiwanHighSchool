import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import {
  copyFileSync,
  cpSync,
  mkdirSync,
  mkdtempSync,
  readFileSync,
  realpathSync,
  rmSync,
  symlinkSync,
  writeFileSync,
} from "node:fs";
import { tmpdir } from "node:os";
import { dirname, join, resolve } from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";
import { writeFigureManifestFixture } from "./test-figure-fixture.mjs";

const sourceRoot = realpathSync(resolve(dirname(fileURLToPath(import.meta.url)), ".."));
const setId = "review-student-lifecycle-test";

function run(root, args) {
  return spawnSync(process.execPath, [join(root, "tools", "publication.mjs"), ...args], {
    cwd: root,
    encoding: "utf8",
    maxBuffer: 64 * 1024 * 1024,
  });
}

function fixture() {
  const root = realpathSync(mkdtempSync(join(realpathSync(tmpdir()), "student-only-lifecycle-")));
  for (const directory of ["tools", "styles", "templates", "assets"]) {
    cpSync(join(sourceRoot, directory), join(root, directory), { recursive: true });
  }
  for (const filename of [".gitignore", "package.json", "package-lock.json"]) {
    copyFileSync(join(sourceRoot, filename), join(root, filename));
  }
  symlinkSync(join(sourceRoot, "node_modules"), join(root, "node_modules"), "dir");
  const chapter = join(root, "content", "數學A", "數A3-9");
  mkdirSync(join(chapter, "assets"), { recursive: true });
  writeFileSync(join(chapter, "學生講義.md"), `---
title: 數A3-9 單冊生命週期測試
title-prefix: 學生講義
subtitle: 從問題理解方法、理由與用途
subject: 數學
course: 普通高中數學A 第三冊
audience: 學生版｜核心＋why＋應用
scope: 現行測試範圍
updated: 2026-08-24
output_slug: 數A3-9-單冊生命週期測試-學生講義
---

# 數A3-9 單冊生命週期測試

## 為什麼要學

把規律寫成可檢驗的模型，才能由已知條件推到未知結果。

## 連續追問 why

為什麼要定義？因為需要一致語言。為什麼能推理？因為每一步都保留條件。

## 真實用途

工程設計用模型比較方案；模型超出假設時就停止套用。

## 短檢核

請說出模型的一項條件。

## 代表題

已知條件成立時，判斷結論是否可用。

## 完整詳解

先核對條件，再套用結論；若條件不成立，就不能推出結果。

用簡單關係 $1+1=2$ 檢查數學字型與可搜尋文字層。

## 核心整理

先問問題，再查條件，最後才計算。
`, "utf8");
  mkdirSync(join(root, "publishing"));
  const registry = {
    schemaVersion: 1,
    defaultSet: setId,
    sets: {
      [setId]: {
        status: "review",
        description: "single student artifact lifecycle fixture",
        documents: [{
          id: "math-a3-9-student",
          audience: "student",
          source: "content/數學A/數A3-9/學生講義.md",
          slug: "數A3-9-單冊生命週期測試-學生講義",
          assets: [],
        }],
      },
    },
  };
  writeFileSync(join(root, "publishing", "sets.json"), `${JSON.stringify(registry, null, 2)}\n`, "utf8");
  writeFigureManifestFixture(root);
  const git = spawnSync("git", ["init", "-q"], { cwd: root, encoding: "utf8" });
  assert.equal(git.status, 0, git.stderr);
  const add = spawnSync("git", ["add", "-A"], { cwd: root, encoding: "utf8" });
  assert.equal(add.status, 0, add.stderr);
  const commit = spawnSync(
    "git",
    ["-c", "user.name=Student Fixture", "-c", "user.email=fixture@example.invalid", "commit", "-qm", "fixture"],
    { cwd: root, encoding: "utf8" },
  );
  assert.equal(commit.status, 0, commit.stderr);
  return root;
}

test("student-only set passes preflight, immutable-snapshot release, and verify", { timeout: 120_000 }, () => {
  const root = fixture();
  try {
    for (const command of [["preflight", "--set", setId], ["release", "--set", setId], ["verify", "--set", setId]]) {
      const result = run(root, command);
      assert.equal(result.status, 0, `${command[0]} failed:\n${result.stdout}\n${result.stderr}`);
    }
    const manifest = JSON.parse(readFileSync(join(root, "dist", setId, "manifest.json"), "utf8"));
    assert.equal(manifest.artifacts.length, 1);
    assert.equal(manifest.artifacts[0].id, "math-a3-9-student");
    assert.equal(manifest.artifacts[0].audience, "student");
    assert.ok(!JSON.stringify(manifest).includes("教師備課指南"));
  } finally {
    rmSync(root, { recursive: true, force: true });
  }
});
