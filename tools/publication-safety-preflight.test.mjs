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
import { writeFigureManifestFixture } from "./test-figure-fixture.mjs";

const repoRoot = realpathSync(resolve(dirname(fileURLToPath(import.meta.url)), ".."));
const setId = "review-safety-test";

function markdown(extra = "") {
  const prefix = "學生講義";
  const title = "數A3-9 測試章";
  return `---
title: ${title}
title-prefix: ${prefix}
subtitle: safety fixture
subject: 數學
course: 普通高中數學A 第三冊
audience: 學生版｜核心＋why＋應用
scope: 現行測試範圍
updated: 2026-08-24
output_slug: 數A3-9-測試章-${prefix}
---

# ${title}

## Fixture

基準內容。

${extra}
`;
}

function registry({ studentAssets = [] } = {}) {
  return {
    schemaVersion: 1,
    defaultSet: setId,
    sets: {
      [setId]: {
        status: "review",
        description: "publication safety focused test",
        documents: [
          {
            id: "math-a3-9-student",
            audience: "student",
            source: "content/數學A/數A3-9/學生講義.md",
            slug: "數A3-9-測試章-學生講義",
            assets: studentAssets,
          },
        ],
      },
    },
  };
}

function fixture({ studentExtra = "", svg, cssSuffix = "" } = {}) {
  const root = realpathSync(mkdtempSync(join(realpathSync(tmpdir()), "publication-safety-test-")));
  for (const directory of ["tools", "styles", "templates", "assets/fonts"]) {
    cpSync(join(repoRoot, directory), join(root, directory), { recursive: true });
  }
  for (const filename of [".gitignore", "package.json", "package-lock.json"]) {
    copyFileSync(join(repoRoot, filename), join(root, filename));
  }
  const chapter = join(root, "content", "數學A", "數A3-9");
  mkdirSync(join(chapter, "assets"), { recursive: true });
  const studentAssets = [];
  let extra = studentExtra;
  if (svg !== undefined) {
    const assetRelative = "content/數學A/數A3-9/assets/數A3-9-fixture.svg";
    writeFileSync(join(root, assetRelative), svg, "utf8");
    studentAssets.push(assetRelative);
    extra += "\n![fixture](assets/數A3-9-fixture.svg){width=96%}\n";
  }
  writeFileSync(join(chapter, "學生講義.md"), markdown(extra), "utf8");
  mkdirSync(join(root, "publishing"));
  writeFileSync(join(root, "publishing", "sets.json"), `${JSON.stringify(registry({ studentAssets }), null, 2)}\n`, "utf8");
  writeFigureManifestFixture(root, studentAssets);
  if (cssSuffix) {
    const cssPath = join(root, "styles", "handout.css");
    writeFileSync(cssPath, `${readFileSync(cssPath, "utf8")}\n${cssSuffix}\n`, "utf8");
  }
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

function expectPreflightFailure(options, pattern) {
  const root = fixture(options);
  try {
    const result = preflight(root);
    assert.notEqual(result.status, 0, result.stdout);
    assert.match(result.stderr, pattern);
  } finally {
    rmSync(root, { recursive: true, force: true });
  }
}

test("preflight rejects an http Markdown link before build", () => {
  expectPreflightFailure({ studentExtra: "[不安全連結](http://example.com)" }, /不允許 http:/u);
});

test("preflight does not promote a percent-encoded scheme to https", () => {
  expectPreflightFailure({ studentExtra: "[encoded](https%3A%2F%2Fexample.com)" }, /本機相對路徑/u);
});

test("preflight does not promote a fullwidth scheme to https through NFKC", () => {
  expectPreflightFailure({ studentExtra: "[fullwidth](https：／／example.com)" }, /NFKC/u);
});

test("preflight rejects active raw HTML before build", () => {
  expectPreflightFailure({ studentExtra: "<form><input name='x'></form>" }, /raw HTML 標籤/u);
});

test("preflight rejects legacy fetching attributes in raw HTML", () => {
  expectPreflightFailure(
    { studentExtra: `<table background="https://example.com/x.png"><tr><td>x</td></tr></table>` },
    /raw HTML 不得自行指定 URL/u,
  );
});

test("preflight rejects raw HTML meta refresh", () => {
  expectPreflightFailure(
    { studentExtra: `<meta http-equiv="refresh" content="0;url=https://example.com">` },
    /raw HTML 不得使用 meta refresh/u,
  );
});

test("preflight rejects decoded private host paths before build", () => {
  expectPreflightFailure({ studentExtra: "本機參考：%2Fhome%2Falice%2Fsecret.txt" }, /Linux 使用者絕對路徑/u);
});

test("preflight rejects Pandoc-normalized native style attributes", () => {
  expectPreflightFailure({ studentExtra: `<div style="color:red">x</div>` }, /禁止 attribute：style/u);
});

test("preflight rejects SVG external CSS resources", () => {
  expectPreflightFailure(
    { svg: `<svg xmlns="http://www.w3.org/2000/svg"><path fill="url(https://example.com/p.svg#p)"/></svg>` },
    /不得引用遠端|外部 CSS/u,
  );
});

test("preflight rejects CSS @import while computing the pipeline closure", () => {
  expectPreflightFailure({ cssSuffix: `@import "https://example.com/print.css";` }, /@import/u);
});

test("preflight rejects CSS image-set while computing the pipeline closure", () => {
  expectPreflightFailure(
    { cssSuffix: `.fixture { background-image: image-set("https://example.com/one.png" 1x); }` },
    /image-set/u,
  );
});
