import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import { mkdirSync, mkdtempSync, realpathSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import test from "node:test";

import {
  assertRepositoryPrivacyBoundary,
  RepositoryPrivacyError,
} from "./repository-privacy.mjs";

function runGit(root, args) {
  const result = spawnSync("git", args, { cwd: root, encoding: "utf8" });
  assert.equal(result.status, 0, result.stderr);
}

function fixture(ignore = "高中教材/\ncontent/**/編輯判定.md\ncontent/**/教師備課指南.md\n") {
  const root = realpathSync(mkdtempSync(join(tmpdir(), "repository-privacy-test-")));
  runGit(root, ["init", "-q"]);
  writeFileSync(join(root, ".gitignore"), ignore, "utf8");
  return root;
}

function cleanup(root) {
  rmSync(root, { recursive: true, force: true });
}

test("接受已忽略且未追蹤的本機教材、編輯判定與教師指南", () => {
  const root = fixture();
  try {
    mkdirSync(join(root, "高中教材"));
    writeFileSync(join(root, "高中教材", "參考.pdf"), "local-only", "utf8");
    mkdirSync(join(root, "content", "數學A", "數A3-1"), { recursive: true });
    writeFileSync(join(root, "content", "數學A", "數A3-1", "編輯判定.md"), "local-only", "utf8");
    writeFileSync(join(root, "content", "數學A", "數A3-1", "教師備課指南.md"), "local-only", "utf8");
    assert.deepEqual(assertRepositoryPrivacyBoundary(root), {
      trackedPrivatePaths: [],
      missingIgnoreRules: [],
    });
  } finally {
    cleanup(root);
  }
});

test("即使使用 force add，也拒絕 Git 已追蹤的高中教材", () => {
  const root = fixture();
  try {
    mkdirSync(join(root, "高中教材"));
    writeFileSync(join(root, "高中教材", "參考.pdf"), "must-not-publish", "utf8");
    runGit(root, ["add", "-f", "--", "高中教材/參考.pdf"]);
    assert.throws(
      () => assertRepositoryPrivacyBoundary(root),
      (error) => error instanceof RepositoryPrivacyError && /Git 已追蹤.*高中教材\/參考\.pdf/u.test(error.message),
    );
  } finally {
    cleanup(root);
  }
});

test("即使使用 force add，也拒絕 Git 已追蹤的編輯判定", () => {
  const root = fixture();
  try {
    mkdirSync(join(root, "content", "選修物理I", "選物I-1"), { recursive: true });
    writeFileSync(join(root, "content", "選修物理I", "選物I-1", "編輯判定.md"), "must-not-publish", "utf8");
    runGit(root, ["add", "-f", "--", "content/選修物理I/選物I-1/編輯判定.md"]);
    assert.throws(
      () => assertRepositoryPrivacyBoundary(root),
      (error) => error instanceof RepositoryPrivacyError && /Git 已追蹤.*編輯判定\.md/u.test(error.message),
    );
  } finally {
    cleanup(root);
  }
});

test("即使使用 force add，也拒絕 Git 已追蹤的教師備課指南", () => {
  const root = fixture();
  try {
    mkdirSync(join(root, "content", "選修物理I", "選物I-1"), { recursive: true });
    writeFileSync(join(root, "content", "選修物理I", "選物I-1", "教師備課指南.md"), "must-not-publish", "utf8");
    runGit(root, ["add", "-f", "--", "content/選修物理I/選物I-1/教師備課指南.md"]);
    assert.throws(
      () => assertRepositoryPrivacyBoundary(root),
      (error) => error instanceof RepositoryPrivacyError && /Git 已追蹤.*教師備課指南\.md/u.test(error.message),
    );
  } finally {
    cleanup(root);
  }
});

test("拒絕缺少任一本機資料 ignore 規則", () => {
  for (const ignore of [
    "高中教材/\ncontent/**/編輯判定.md\n",
    "高中教材/\ncontent/**/教師備課指南.md\n",
    "content/**/編輯判定.md\ncontent/**/教師備課指南.md\n",
    "",
  ]) {
    const root = fixture(ignore);
    try {
      assert.throws(
        () => assertRepositoryPrivacyBoundary(root),
        (error) => error instanceof RepositoryPrivacyError && /.gitignore 缺少本機資料邊界/u.test(error.message),
      );
    } finally {
      cleanup(root);
    }
  }
});
