import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import {
  mkdtempSync,
  mkdirSync,
  readFileSync,
  rmSync,
  symlinkSync,
  writeFileSync,
} from "node:fs";
import { tmpdir } from "node:os";
import { dirname, join } from "node:path";
import test from "node:test";

import {
  createChapter,
  initPrivateEditor,
  lintChapter,
  parseArguments,
  scaffoldResultStatus,
} from "./scaffold-chapter.mjs";

function fixture({ privateIgnore = true } = {}) {
  const root = mkdtempSync(join(tmpdir(), "chapter-scaffold-test-"));
  mkdirSync(join(root, "content", "必修數學"), { recursive: true });
  mkdirSync(join(root, "content", "數學A"), { recursive: true });
  mkdirSync(join(root, "content", "數學B"), { recursive: true });
  mkdirSync(join(root, "content", "選修物理I"), { recursive: true });
  mkdirSync(join(root, "content", "必修物理"), { recursive: true });
  mkdirSync(join(root, "content", "必修化學"), { recursive: true });
  for (const course of ["選修化學I", "選修化學II", "選修化學III", "選修化學IV", "選修化學V"]) {
    mkdirSync(join(root, "content", course), { recursive: true });
  }
  writeFileSync(join(root, ".gitignore"), privateIgnore ? "content/**/編輯判定.md\n" : "", "utf8");
  const git = spawnSync("git", ["init", "-q"], { cwd: root, encoding: "utf8" });
  assert.equal(git.status, 0, git.stderr);
  return root;
}

function cleanup(root) {
  rmSync(root, { recursive: true, force: true });
}

function createMath(root, options = {}) {
  const writeApproved = options.writeApproved ?? (options.dryRun !== true);
  return createChapter({
    repoRoot: root,
    course: "數學A",
    chapterCode: "數A3-9",
    title: "測試章",
    updated: "2026-08-24",
    writeApproved,
    ...options,
  });
}

function createPhysics(root, options = {}) {
  const writeApproved = options.writeApproved ?? (options.dryRun !== true);
  return createChapter({
    repoRoot: root,
    course: "選修物理I",
    chapterCode: "選物I-5",
    title: "測試章",
    updated: "2026-08-24",
    writeApproved,
    ...options,
  });
}

function createChemistry(root, options = {}) {
  const writeApproved = options.writeApproved ?? (options.dryRun !== true);
  return createChapter({
    repoRoot: root,
    course: "選修化學III",
    chapterCode: "選化III-2",
    title: "酸鹼反應",
    updated: "2026-08-29",
    writeApproved,
    ...options,
  });
}

function resolveTodos(path) {
  const body = readFileSync(path, "utf8").replaceAll("TODO(SCAFFOLD):", "已完成：");
  writeFileSync(path, body, "utf8");
}

test("create 只產生學生稿、assets、私有編輯判定與單一 student registry document", () => {
  const root = fixture();
  try {
    const result = createMath(root);
    assert.equal(result.dryRun, false);
    assert.equal(
      scaffoldResultStatus(result),
      "已建立空白骨架；只建骨架，未登記 publishing/sets.json，未發布 PDF",
    );
    assert.deepEqual(result.files.sort(), ["assets/", "學生講義.md", "編輯判定.md"].sort());
    assert.equal(result.registryDocuments.length, 1);
    assert.deepEqual(result.registryDocuments.map((entry) => entry.audience), ["student"]);
    assert.ok(result.registryDocuments.every((entry) => !JSON.stringify(entry).includes("編輯判定")));
    const student = readFileSync(join(root, "content", "數學A", "數A3-9", "學生講義.md"), "utf8");
    assert.match(student, /output_slug: "數A3-9-測試章-學生講義"/u);
    assert.match(student, /原理或推導/u);
    assert.match(student, /實際用途/u);
    assert.doesNotMatch(student, /why\s*(?:→|->)|起點檢查|先備檢核|30\s*秒|停止線/iu);
    assert.doesNotThrow(() => lintChapter({ repoRoot: root, course: "數學A", chapterCode: "數A3-9", allowTodos: true }));
    assert.throws(
      () => lintChapter({ repoRoot: root, course: "數學A", chapterCode: "數A3-9" }),
      /尚有 TODO\(SCAFFOLD\)/u,
    );
  } finally {
    cleanup(root);
  }
});

test("lint 拒絕標語式與閱讀指令式標題", () => {
  const root = fixture();
  try {
    createMath(root);
    const path = join(root, "content", "數學A", "數A3-9", "學生講義.md");
    resolveTodos(path);
    const body = readFileSync(path, "utf8").replace(
      "## 1. 本章問題與用途",
      "## 1. Why → Why → Why｜起點檢查（30 秒）",
    );
    writeFileSync(path, body, "utf8");
    assert.throws(
      () => lintChapter({ repoRoot: root, course: "數學A", chapterCode: "數A3-9" }),
      /閱讀指令或標語式標題/u,
    );
  } finally {
    cleanup(root);
  }
});

test("lint 拒絕缺少反斜線而會印在 PDF 上的 TeX 間距指令", () => {
  const root = fixture();
  try {
    createMath(root);
    const path = join(root, "content", "數學A", "數A3-9", "學生講義.md");
    resolveTodos(path);
    writeFileSync(path, `${readFileSync(path, "utf8")}\n$$p_i\\ge0,qquad p_1+p_2=1.$$\n`, "utf8");
    assert.throws(
      () => lintChapter({ repoRoot: root, course: "數學A", chapterCode: "數A3-9" }),
      /缺少反斜線的 TeX 間距指令/u,
    );
  } finally {
    cleanup(root);
  }
});

test("物理完稿至少需要三張不同且被正文使用的 SVG", () => {
  const root = fixture();
  try {
    createPhysics(root);
    const chapter = join(root, "content", "選修物理I", "選物I-5");
    const student = join(chapter, "學生講義.md");
    resolveTodos(student);
    assert.throws(
      () => lintChapter({ repoRoot: root, course: "選修物理I", chapterCode: "選物I-5" }),
      /至少需要三張不同 SVG/u,
    );
    const svg = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 10 10"><path d="M1 9L9 1"/></svg>\n';
    for (const index of [1, 2, 3]) {
      const name = `選物I-5-圖${index}.svg`;
      writeFileSync(join(chapter, "assets", name), svg, "utf8");
      writeFileSync(student, `${readFileSync(student, "utf8")}\n![圖 ${index}](assets/${name})\n`, "utf8");
    }
    assert.doesNotThrow(
      () => lintChapter({ repoRoot: root, course: "選修物理I", chapterCode: "選物I-5" }),
    );
  } finally {
    cleanup(root);
  }
});

test("化學骨架使用化學身分且可沿用學生單冊完整度檢查", () => {
  const root = fixture();
  try {
    const result = createChemistry(root);
    assert.equal(result.registryDocuments[0].id, "chemistry-i3-2-student");
    const student = join(root, "content", "選修化學III", "選化III-2", "學生講義.md");
    const body = readFileSync(student, "utf8");
    assert.match(body, /subject: "化學"/u);
    assert.match(body, /course: "普通高中選修化學 III"/u);
    assert.doesNotThrow(() => lintChapter({
      repoRoot: root,
      course: "選修化學III",
      chapterCode: "選化III-2",
      allowTodos: true,
    }));
    resolveTodos(student);
    assert.throws(
      () => lintChapter({ repoRoot: root, course: "選修化學III", chapterCode: "選化III-2" }),
      /化學學生講義至少需要三張不同 SVG/u,
    );
    const chapter = dirname(student);
    const svg = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 10 10"><circle cx="5" cy="5" r="3"/></svg>\n';
    for (const index of [1, 2, 3]) {
      const name = `選化III-2-圖${index}.svg`;
      writeFileSync(join(chapter, "assets", name), svg, "utf8");
      writeFileSync(student, `${readFileSync(student, "utf8")}\n![圖 ${index}](assets/${name})\n`, "utf8");
    }
    assert.doesNotThrow(
      () => lintChapter({ repoRoot: root, course: "選修化學III", chapterCode: "選化III-2" }),
    );
  } finally {
    cleanup(root);
  }
});

test("programmatic create 預設只 dry-run，dryRun false 不能取代明示寫入授權", () => {
  const root = fixture();
  try {
    const options = {
      repoRoot: root,
      course: "數學A",
      chapterCode: "數A3-7",
      title: "預設乾跑章",
      updated: "2026-08-24",
    };
    const result = createChapter(options);
    assert.equal(result.dryRun, true);
    assert.equal(scaffoldResultStatus(result), "dry-run 通過，未寫入");
    assert.equal(spawnSync("test", ["-e", join(root, "content", "數學A", "數A3-7")]).status, 1);

    assert.throws(
      () => createChapter({ ...options, dryRun: false }),
      /必須明示 writeApproved: true/u,
    );
    assert.equal(spawnSync("test", ["-e", join(root, "content", "數學A", "數A3-7")]).status, 1);
    assert.throws(
      () => createChapter({ ...options, dryRun: true, writeApproved: true }),
      /互斥/u,
    );
  } finally {
    cleanup(root);
  }
});

test("programmatic create 拒絕從 prototype 繼承 writeApproved", () => {
  const root = fixture();
  try {
    const options = Object.assign(Object.create({ writeApproved: true }), {
      repoRoot: root,
      course: "數學A",
      chapterCode: "數A3-6",
      title: "繼承授權章",
      updated: "2026-08-24",
    });
    assert.throws(() => createChapter(options), /不得以 prototype 繼承寫入授權/u);
    assert.equal(spawnSync("test", ["-e", join(root, "content", "數學A", "數A3-6")]).status, 1);
  } finally {
    cleanup(root);
  }
});

test("programmatic create 拒絕 writeApproved getter，且不執行 getter", () => {
  const root = fixture();
  try {
    let getterReads = 0;
    const options = {
      repoRoot: root,
      course: "數學A",
      chapterCode: "數A3-6",
      title: "Getter 授權章",
      updated: "2026-08-24",
    };
    Object.defineProperty(options, "writeApproved", {
      configurable: true,
      enumerable: true,
      get() {
        getterReads += 1;
        return true;
      },
    });
    assert.throws(() => createChapter(options), /own data property.*getter／setter/u);
    assert.equal(getterReads, 0);
    assert.equal(spawnSync("test", ["-e", join(root, "content", "數學A", "數A3-6")]).status, 1);
  } finally {
    cleanup(root);
  }
});

test("programmatic create 拒絕 Proxy 合成 writeApproved descriptor", () => {
  const root = fixture();
  try {
    let trapCalls = 0;
    const target = {
      repoRoot: root,
      course: "數學A",
      chapterCode: "數A3-6",
      title: "Proxy 授權章",
      updated: "2026-08-24",
    };
    const options = new Proxy(target, {
      get(object, property, receiver) {
        trapCalls += 1;
        if (property === "writeApproved") return true;
        return Reflect.get(object, property, receiver);
      },
      getOwnPropertyDescriptor(object, property) {
        trapCalls += 1;
        if (property === "writeApproved") {
          return { configurable: true, enumerable: true, value: true, writable: true };
        }
        return Reflect.getOwnPropertyDescriptor(object, property);
      },
    });
    assert.throws(() => createChapter(options), /非 Proxy/u);
    assert.equal(trapCalls, 0);
    assert.equal(spawnSync("test", ["-e", join(root, "content", "數學A", "數A3-6")]).status, 1);
  } finally {
    cleanup(root);
  }
});

test("dry-run 完整驗證但不建立章目錄", () => {
  const root = fixture();
  try {
    const result = createMath(root, { chapterCode: "數A3-8", dryRun: true });
    assert.equal(result.dryRun, true);
    assert.equal(spawnSync("test", ["-e", join(root, "content", "數學A", "數A3-8")]).status, 1);
  } finally {
    cleanup(root);
  }
});

test("init-private 在 fresh clone 式章節補建私有檔，公開稿不變且正式 lint 可過", () => {
  const root = fixture();
  try {
    createMath(root);
    const chapter = join(root, "content", "數學A", "數A3-9");
    const studentPath = join(chapter, "學生講義.md");
    const editorPath = join(chapter, "編輯判定.md");
    resolveTodos(studentPath);
    const publicBefore = readFileSync(studentPath, "utf8");
    rmSync(editorPath);

    assert.throws(
      () => lintChapter({ repoRoot: root, course: "數學A", chapterCode: "數A3-9" }),
      /章根必須包含/u,
    );
    const result = initPrivateEditor({ repoRoot: root, course: "數學A", chapterCode: "數A3-9" });

    assert.equal(result.initializedPrivate, "content/數學A/數A3-9/編輯判定.md");
    assert.match(readFileSync(editorPath, "utf8"), /^# 數A3-9 測試章｜編輯判定（本機內部）/mu);
    assert.match(readFileSync(editorPath, "utf8"), /- 更新日期：2026-08-24/u);
    assert.deepEqual(
      readFileSync(studentPath, "utf8"),
      publicBefore,
    );
    assert.doesNotThrow(() => lintChapter({ repoRoot: root, course: "數學A", chapterCode: "數A3-9" }));
  } finally {
    cleanup(root);
  }
});

test("init-private 拒絕覆寫與 symlink，並保留原始內容", (context) => {
  if (process.platform === "win32") return context.skip("symlink fixture is POSIX-only");
  const root = fixture();
  try {
    createMath(root);
    const chapter = join(root, "content", "數學A", "數A3-9");
    const editorPath = join(chapter, "編輯判定.md");
    const original = readFileSync(editorPath, "utf8");
    assert.throws(
      () => initPrivateEditor({ repoRoot: root, course: "數學A", chapterCode: "數A3-9" }),
      /拒絕覆寫/u,
    );
    assert.equal(readFileSync(editorPath, "utf8"), original);

    rmSync(editorPath);
    const outside = join(root, "outside-private.md");
    writeFileSync(outside, "keep", "utf8");
    symlinkSync(outside, editorPath, "file");
    assert.throws(
      () => initPrivateEditor({ repoRoot: root, course: "數學A", chapterCode: "數A3-9" }),
      /symlink/u,
    );
    assert.equal(readFileSync(outside, "utf8"), "keep");
  } finally {
    cleanup(root);
  }
});

test("init-private 拒絕未 ignore、錯課程章碼與不合法公開章", () => {
  const root = fixture();
  try {
    createMath(root);
    const chapter = join(root, "content", "數學A", "數A3-9");
    const editorPath = join(chapter, "編輯判定.md");
    resolveTodos(join(chapter, "學生講義.md"));
    rmSync(editorPath);
    assert.throws(
      () => initPrivateEditor({ repoRoot: root, course: "數學A", chapterCode: "選物I-9" }),
      /不一致/u,
    );
    writeFileSync(join(root, ".gitignore"), "", "utf8");
    assert.throws(
      () => initPrivateEditor({ repoRoot: root, course: "數學A", chapterCode: "數A3-9" }),
      /必須由 Git 明確忽略/u,
    );

    writeFileSync(join(root, ".gitignore"), "content/**/編輯判定.md\n", "utf8");
    writeFileSync(join(chapter, "unexpected.txt"), "keep", "utf8");
    assert.throws(
      () => initPrivateEditor({ repoRoot: root, course: "數學A", chapterCode: "數A3-9" }),
      /章根必須包含/u,
    );
  } finally {
    cleanup(root);
  }
});

test("lint 完稿後列出學生稿精確使用的 SVG，且不含私有檔或 teacher document", () => {
  const root = fixture();
  try {
    createMath(root);
    const chapter = join(root, "content", "數學A", "數A3-9");
    const studentPath = join(chapter, "學生講義.md");
    resolveTodos(studentPath);
    writeFileSync(
      join(chapter, "assets", "數A3-9-示意.svg"),
      '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 10 10"><path d="M0 0L10 10"/></svg>\n',
      "utf8",
    );
    writeFileSync(studentPath, `${readFileSync(studentPath, "utf8")}\n![示意](assets/數A3-9-示意.svg)\n`, "utf8");
    const result = lintChapter({ repoRoot: root, course: "數學A", chapterCode: "數A3-9" });
    assert.deepEqual(result.registryDocuments[0].assets, ["content/數學A/數A3-9/assets/數A3-9-示意.svg"]);
    assert.equal(result.registryDocuments.length, 1);
    assert.equal(result.registryDocuments[0].audience, "student");
    assert.ok(!JSON.stringify(result.registryDocuments).includes("編輯判定"));
  } finally {
    cleanup(root);
  }
});

test("lint 容許既有教師備課指南作 optional legacy，但永不輸出 teacher registry document", () => {
  const root = fixture();
  try {
    createMath(root);
    const chapter = join(root, "content", "數學A", "數A3-9");
    resolveTodos(join(chapter, "學生講義.md"));
    writeFileSync(
      join(chapter, "教師備課指南.md"),
      "# 歷史教師檔\n\n此檔只保留作 legacy 參考，不是新出版 artifact。\n",
      "utf8",
    );
    const result = lintChapter({ repoRoot: root, course: "數學A", chapterCode: "數A3-9" });
    assert.deepEqual(result.registryDocuments.map(({ audience }) => audience), ["student"]);
    assert.ok(!JSON.stringify(result.registryDocuments).includes("教師備課指南"));
  } finally {
    cleanup(root);
  }
});

test("optional legacy 教師檔仍必須是章根內的 canonical regular file", (context) => {
  if (process.platform === "win32") return context.skip("symlink fixture is POSIX-only");
  const root = fixture();
  try {
    createMath(root);
    const chapter = join(root, "content", "數學A", "數A3-9");
    resolveTodos(join(chapter, "學生講義.md"));
    const outside = join(root, "legacy-teacher.md");
    writeFileSync(outside, "# outside legacy\n", "utf8");
    symlinkSync(outside, join(chapter, "教師備課指南.md"), "file");
    assert.throws(
      () => lintChapter({ repoRoot: root, course: "數學A", chapterCode: "數A3-9" }),
      /optional legacy 教師備課指南.*非 symlink/u,
    );
  } finally {
    cleanup(root);
  }
});

test("拒絕未登記課程、章碼錯配、危險章名與無效日期", () => {
  const root = fixture();
  try {
    assert.throws(() => createMath(root, { course: "化學" }), /尚未登記 schema/u);
    assert.throws(() => createMath(root, { chapterCode: "選物I-9" }), /不一致/u);
    assert.throws(() => createMath(root, { chapterCode: "數A3-02" }), /canonical 正整數/u);
    assert.throws(
      () => createChapter({
        repoRoot: root,
        course: "選修物理I",
        chapterCode: "選物I-0",
        title: "測試章",
        updated: "2026-08-24",
        dryRun: true,
      }),
      /canonical 正整數/u,
    );
    assert.throws(() => createMath(root, { title: "../逃逸" }), /不安全/u);
    assert.throws(() => createMath(root, { title: "數A3-1 三角函數" }), /不得以任何已登記的章碼/u);
    assert.throws(() => createMath(root, { updated: "2026-02-30" }), /有效/u);
  } finally {
    cleanup(root);
  }
});

test("lint 拒絕與 frontmatter identity 不一致的可見 H1，並忽略 comment／code fence 內的假 H1", () => {
  const root = fixture();
  try {
    createMath(root);
    const chapter = join(root, "content", "數學A", "數A3-9");
    const studentPath = join(chapter, "學生講義.md");
    resolveTodos(studentPath);
    const validStudent = readFileSync(studentPath, "utf8");
    writeFileSync(
      studentPath,
      validStudent.replace(/^# 數A3-9 測試章$/mu, "# 選物I-1 測量與不確定度"),
      "utf8",
    );
    assert.throws(
      () => lintChapter({ repoRoot: root, course: "數學A", chapterCode: "數A3-9" }),
      /必須恰有一個 H1/u,
    );

    writeFileSync(studentPath, `${validStudent}\nInjected\n========\n`, "utf8");
    assert.throws(
      () => lintChapter({ repoRoot: root, course: "數學A", chapterCode: "數A3-9" }),
      /必須恰有一個 H1/u,
    );

    writeFileSync(studentPath, `${validStudent}\n> # Injected\n`, "utf8");
    assert.throws(
      () => lintChapter({ repoRoot: root, course: "數學A", chapterCode: "數A3-9" }),
      /必須恰有一個 H1/u,
    );

    writeFileSync(studentPath, `${validStudent}\n<h1>Injected</h1>\n`, "utf8");
    assert.throws(
      () => lintChapter({ repoRoot: root, course: "數學A", chapterCode: "數A3-9" }),
      /raw HTML heading/u,
    );

    writeFileSync(
      studentPath,
      `${validStudent}\n<!-- # 註解內不是標題；<h1>也不是</h1> -->\n\n\`\`\`text\n# code fence 內不是標題\n<h1>code fence 內也不是</h1>\n\`\`\`\n`,
      "utf8",
    );
    assert.doesNotThrow(() => lintChapter({ repoRoot: root, course: "數學A", chapterCode: "數A3-9" }));
  } finally {
    cleanup(root);
  }
});

test("拒絕覆寫既有章，既有 sentinel 保持不變", () => {
  const root = fixture();
  try {
    const target = join(root, "content", "數學A", "數A3-9");
    mkdirSync(target);
    writeFileSync(join(target, "sentinel"), "keep", "utf8");
    assert.throws(() => createMath(root), /拒絕覆寫/u);
    assert.equal(readFileSync(join(target, "sentinel"), "utf8"), "keep");
  } finally {
    cleanup(root);
  }
});

test("拒絕沒有私有 ignore 邊界的 repository", () => {
  const root = fixture({ privateIgnore: false });
  try {
    assert.throws(() => createMath(root), /必須先由 Git 明確忽略/u);
  } finally {
    cleanup(root);
  }
});

test("dry-run 也拒絕會把公開來源一併忽略的過寬規則", () => {
  const root = fixture();
  try {
    writeFileSync(join(root, ".gitignore"), "content/**\n", "utf8");
    assert.throws(() => createMath(root, { dryRun: true }), /預定公開來源，不得被 Git 忽略/u);
    assert.equal(spawnSync("test", ["-e", join(root, "content", "數學A", "數A3-9")]).status, 1);
  } finally {
    cleanup(root);
  }
});

test("拒絕經 symlink 的課程目錄", (context) => {
  if (process.platform === "win32") return context.skip("symlink fixture is POSIX-only");
  const root = fixture();
  try {
    const outside = join(root, "outside-course");
    mkdirSync(outside);
    rmSync(join(root, "content", "數學A"), { recursive: true });
    symlinkSync(outside, join(root, "content", "數學A"), "dir");
    assert.throws(() => createMath(root), /非 symlink 目錄/u);
  } finally {
    cleanup(root);
  }
});

test("lint 拒絕公開稿洩漏本機教材、frontmatter 漂移與危險 SVG", () => {
  const root = fixture();
  try {
    createMath(root);
    const chapter = join(root, "content", "數學A", "數A3-9");
    const student = join(chapter, "學生講義.md");
    resolveTodos(student);
    writeFileSync(student, `${readFileSync(student, "utf8")}\n高中教材/秘密.pdf\n`, "utf8");
    assert.throws(() => lintChapter({ repoRoot: root, course: "數學A", chapterCode: "數A3-9" }), /私有或禁止字串/u);
    writeFileSync(student, readFileSync(student, "utf8").replace("高中教材/秘密.pdf\n", "").replace('subject: "數學"', 'subject: "物理"'), "utf8");
    assert.throws(() => lintChapter({ repoRoot: root, course: "數學A", chapterCode: "數A3-9" }), /subject 應為/u);
    writeFileSync(student, readFileSync(student, "utf8").replace('subject: "物理"', 'subject: "數學"'), "utf8");
    writeFileSync(join(chapter, "assets", "bad.svg"), '<svg><script>alert(1)</script></svg>', "utf8");
    writeFileSync(student, `${readFileSync(student, "utf8")}\n![bad](assets/bad.svg)\n`, "utf8");
    assert.throws(() => lintChapter({ repoRoot: root, course: "數學A", chapterCode: "數A3-9" }), /script／foreignObject/u);
  } finally {
    cleanup(root);
  }
});

test("lint 拒絕多餘章根檔、未引用 asset 與忽略公開來源", () => {
  const root = fixture();
  try {
    createMath(root);
    const chapter = join(root, "content", "數學A", "數A3-9");
    resolveTodos(join(chapter, "學生講義.md"));
    writeFileSync(join(chapter, "notes.txt"), "unexpected", "utf8");
    assert.throws(() => lintChapter({ repoRoot: root, course: "數學A", chapterCode: "數A3-9" }), /章根必須包含/u);
    rmSync(join(chapter, "notes.txt"));
    writeFileSync(join(chapter, "assets", "unused.svg"), '<svg xmlns="http://www.w3.org/2000/svg"/>\n', "utf8");
    assert.throws(() => lintChapter({ repoRoot: root, course: "數學A", chapterCode: "數A3-9" }), /未被學生稿或 optional legacy 教師稿引用/u);
    rmSync(join(chapter, "assets", "unused.svg"));
    writeFileSync(join(root, ".gitignore"), "content/**/編輯判定.md\ncontent/**/學生講義.md\n", "utf8");
    assert.throws(() => lintChapter({ repoRoot: root, course: "數學A", chapterCode: "數A3-9" }), /公開來源，不得被 Git 忽略/u);
  } finally {
    cleanup(root);
  }
});

test("CLI parser 拒絕重複、未知及命令不相容參數", () => {
  assert.deepEqual(
    parseArguments(["init-private", "--course", "數學A", "--chapter-code", "數A3-9", "--json"]),
    {
      command: "init-private",
      dryRun: false,
      writeApproved: false,
      allowTodos: false,
      json: true,
      course: "數學A",
      chapterCode: "數A3-9",
    },
  );
  const createArgs = [
    "create",
    "--course", "數學A",
    "--chapter-code", "數A3-9",
    "--title", "測試",
    "--updated", "2026-08-24",
  ];
  const defaultCreate = parseArguments(createArgs);
  assert.equal(defaultCreate.dryRun, true);
  assert.equal(defaultCreate.writeApproved, false);
  const explicitDryRun = parseArguments([...createArgs, "--dry-run"]);
  assert.equal(explicitDryRun.dryRun, true);
  assert.equal(explicitDryRun.writeApproved, false);
  const approvedWrite = parseArguments([...createArgs, "--write-approved"]);
  assert.equal(approvedWrite.dryRun, false);
  assert.equal(approvedWrite.writeApproved, true);
  assert.throws(() => parseArguments([...createArgs, "--dry-run", "--write-approved"]), /互斥/u);
  assert.throws(() => parseArguments(["create", "--course", "數學A", "--course", "數學A"]), /參數重複/u);
  assert.throws(() => parseArguments(["create", "--course", "數學A", "--chapter-code", "數A3-9", "--title", "測試", "--updated", "2026-08-24", "--force"]), /無法辨識/u);
  assert.throws(() => parseArguments(["lint", "--course", "數學A", "--chapter-code", "數A3-9", "--dry-run"]), /lint 不接受/u);
  assert.throws(() => parseArguments(["lint", "--course", "數學A", "--chapter-code", "數A3-9", "--write-approved"]), /lint 不接受/u);
  assert.throws(() => parseArguments(["init-private", "--course", "數學A", "--chapter-code", "數A3-9", "--allow-todos"]), /init-private 只接受/u);
  assert.throws(() => parseArguments(["init-private", "--course", "數學A", "--chapter-code", "數A3-9", "--write-approved"]), /init-private 只接受/u);
});
