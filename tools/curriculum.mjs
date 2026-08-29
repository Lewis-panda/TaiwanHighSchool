import { readFileSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

import { resolveCourseIdentity } from "./course-identity.mjs";

const defaultRepoRoot = resolve(dirname(fileURLToPath(import.meta.url)), "..");

function fail(message) {
  throw new Error(message);
}

function exactKeys(value, expected, label) {
  if (!value || typeof value !== "object" || Array.isArray(value)) fail(`${label} 必須是 object`);
  const actual = Object.keys(value).sort();
  const wanted = [...expected].sort();
  if (JSON.stringify(actual) !== JSON.stringify(wanted)) {
    fail(`${label} 欄位必須精確為 ${wanted.join(", ")}；實際為 ${actual.join(", ")}`);
  }
}

export function loadCurriculum(repoRoot = defaultRepoRoot) {
  const path = join(resolve(repoRoot), "publishing", "curriculum.json");
  let catalog;
  try {
    catalog = JSON.parse(readFileSync(path, "utf8"));
  } catch (error) {
    fail(`publishing/curriculum.json 無法讀取：${error.message}`);
  }
  exactKeys(catalog, ["description", "documents", "schemaVersion"], "curriculum");
  if (catalog.schemaVersion !== 1 || typeof catalog.description !== "string" || !catalog.description) {
    fail("curriculum schemaVersion／description 無效");
  }
  if (!Array.isArray(catalog.documents) || catalog.documents.length === 0) {
    fail("curriculum.documents 必須是非空 array");
  }

  const seenChapters = new Set();
  const seenIds = new Set();
  const documents = catalog.documents.map((document, index) => {
    const label = `curriculum.documents[${index}]`;
    exactKeys(document, ["chapterCode", "courseDirectory", "grade", "title", "volume"], label);
    for (const key of ["chapterCode", "courseDirectory", "title", "volume"]) {
      if (typeof document[key] !== "string" || !document[key] || document[key] !== document[key].normalize("NFC")) {
        fail(`${label}.${key} 必須是非空 NFC 字串`);
      }
    }
    if (![10, 11].includes(document.grade)) fail(`${label}.grade 只允許 10 或 11`);
    const identity = resolveCourseIdentity(document.courseDirectory, document.chapterCode);
    const chapterKey = `${document.courseDirectory}/${document.chapterCode}`;
    if (seenChapters.has(chapterKey)) fail(`curriculum 章節重複：${chapterKey}`);
    if (seenIds.has(identity.idStem)) fail(`curriculum document id stem 重複：${identity.idStem}`);
    seenChapters.add(chapterKey);
    seenIds.add(identity.idStem);
    return Object.freeze({ ...document, identity, chapterKey });
  });

  return Object.freeze({
    schemaVersion: 1,
    description: catalog.description,
    documents: Object.freeze(documents),
  });
}

