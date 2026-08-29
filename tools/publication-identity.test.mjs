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
  writeFileSync,
} from "node:fs";
import { tmpdir } from "node:os";
import { dirname, join, resolve } from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";
import { expectedDocumentId, resolveCourseIdentity } from "./course-identity.mjs";
import { writeFigureManifestFixture } from "./test-figure-fixture.mjs";

const repoRoot = realpathSync(resolve(dirname(fileURLToPath(import.meta.url)), ".."));
const setId = "review-identity-test";

function markdown({ h1, extra = "" } = {}) {
  const prefix = "學生講義";
  const title = "數A3-9 測試章";
  const expectedH1 = title;
  return `---
title: ${title}
title-prefix: ${prefix}
subtitle: identity fixture
subject: 數學
course: 普通高中數學A 第三冊
audience: 學生版｜核心＋why＋應用
scope: 現行測試範圍
updated: 2026-08-24
output_slug: 數A3-9-測試章-${prefix}
---

# ${h1 ?? expectedH1}

## Fixture

Identity preflight fixture.
${extra}
`;
}

function registry({ wrongIds = false, includeTeacher = false } = {}) {
  const documents = [
    {
      id: wrongIds ? "physics-i1-9-student" : "math-a3-9-student",
      audience: "student",
      source: "content/數學A/數A3-9/學生講義.md",
      slug: "數A3-9-測試章-學生講義",
      assets: [],
    },
  ];
  if (includeTeacher) {
    documents.push({
      id: "math-a3-9-teacher",
      audience: "teacher",
      source: "content/數學A/數A3-9/教師備課指南.md",
      slug: "數A3-9-測試章-教師備課指南",
      assets: [],
    });
  }
  return {
    schemaVersion: 1,
    defaultSet: setId,
    sets: {
      [setId]: {
        status: "review",
        description: "publication identity focused test",
        documents,
      },
    },
  };
}

function fixture({ wrongIds = false, includeTeacher = false, studentH1, studentExtra = "" } = {}) {
  const root = realpathSync(mkdtempSync(join(realpathSync(tmpdir()), "publication-identity-test-")));
  for (const directory of ["tools", "styles", "templates", "assets/fonts"]) {
    cpSync(join(repoRoot, directory), join(root, directory), { recursive: true });
  }
  for (const filename of [".gitignore", "package.json", "package-lock.json"]) {
    copyFileSync(join(repoRoot, filename), join(root, filename));
  }
  const chapter = join(root, "content", "數學A", "數A3-9");
  mkdirSync(join(chapter, "assets"), { recursive: true });
  writeFileSync(join(chapter, "學生講義.md"), markdown({ h1: studentH1, extra: studentExtra }), "utf8");
  if (includeTeacher) writeFileSync(join(chapter, "教師備課指南.md"), "# legacy\n", "utf8");
  mkdirSync(join(root, "publishing"));
  writeFileSync(join(root, "publishing", "sets.json"), `${JSON.stringify(registry({ wrongIds, includeTeacher }), null, 2)}\n`, "utf8");
  writeFigureManifestFixture(root);
  const git = spawnSync("git", ["init", "-q"], { cwd: root, encoding: "utf8" });
  assert.equal(git.status, 0, git.stderr);
  return root;
}

function preflight(root) {
  return spawnSync(
    process.execPath,
    [join(root, "tools", "publication.mjs"), "preflight", "--set", setId],
    { cwd: root, encoding: "utf8", maxBuffer: 64 * 1024 * 1024 },
  );
}

function cleanup(root) {
  rmSync(root, { recursive: true, force: true });
}

test("course identity derives only the canonical student document id", () => {
  const identity = resolveCourseIdentity("數學A", "數A3-9");
  assert.equal(expectedDocumentId(identity, "student"), "math-a3-9-student");
  assert.throws(() => expectedDocumentId(identity, "teacher"), /只支援 student audience/u);
});

test("publication preflight 接受完整一致的 course/chapter identity", () => {
  const root = fixture();
  try {
    const result = preflight(root);
    assert.equal(result.status, 0, `${result.stdout}\n${result.stderr}`);
  } finally {
    cleanup(root);
  }
});

test("publication preflight 拒絕未由 course/chapterCode 衍生的 document id", () => {
  const root = fixture({ wrongIds: true });
  try {
    const result = preflight(root);
    assert.notEqual(result.status, 0, result.stdout);
    assert.match(result.stderr, /必須由課程、章碼與 audience 衍生/u);
  } finally {
    cleanup(root);
  }
});

test("publication schema 拒絕 teacher artifact，即使既有教師檔仍留在章目錄", () => {
  const root = fixture({ includeTeacher: true });
  try {
    const result = preflight(root);
    assert.notEqual(result.status, 0, result.stdout);
    assert.match(result.stderr, /audience 必須是 student|教師備課指南屬 legacy/u);
  } finally {
    cleanup(root);
  }
});

test("standard build-handout refuses an optional legacy teacher source before rendering", () => {
  const root = fixture({ includeTeacher: true });
  try {
    const result = spawnSync(
      process.execPath,
      [join(root, "tools", "build-handout.mjs"), join(root, "content", "數學A", "數A3-9", "教師備課指南.md")],
      { cwd: root, encoding: "utf8", maxBuffer: 64 * 1024 * 1024 },
    );
    assert.notEqual(result.status, 0, result.stdout);
    assert.match(result.stderr, /標準來源只允許 學生講義\.md.*legacy/u);
  } finally {
    cleanup(root);
  }
});

test("publication preflight 以 Pandoc AST 拒絕與 frontmatter 不一致的 H1", () => {
  const root = fixture({ studentH1: "選物I-1 測量與不確定度" });
  try {
    const result = preflight(root);
    assert.notEqual(result.status, 0, result.stdout);
    assert.match(result.stderr, /必須恰有一個 H1/u);
  } finally {
    cleanup(root);
  }
});

test("publication preflight 以 Pandoc AST 拒絕第二個 Setext H1", () => {
  const root = fixture({ studentExtra: "\nInjected\n========" });
  try {
    const result = preflight(root);
    assert.notEqual(result.status, 0, result.stdout);
    assert.match(result.stderr, /必須恰有一個 H1/u);
  } finally {
    cleanup(root);
  }
});

test("publication preflight 拒絕不會成為 Header node 的 raw HTML heading", () => {
  const root = fixture({ studentExtra: "<h1>Injected</h1>" });
  try {
    const result = preflight(root);
    assert.notEqual(result.status, 0, result.stdout);
    assert.match(result.stderr, /raw HTML heading/u);
  } finally {
    cleanup(root);
  }
});
