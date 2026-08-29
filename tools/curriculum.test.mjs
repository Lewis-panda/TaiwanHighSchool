import assert from "node:assert/strict";
import test from "node:test";

import { loadCurriculum } from "./curriculum.mjs";

test("本機高一、高二課程清單固定為 48 章且章節身分唯一", () => {
  const catalog = loadCurriculum();
  assert.equal(catalog.documents.length, 48);
  const subjectCounts = Object.groupBy(catalog.documents, (document) => document.identity.subject);
  assert.deepEqual(
    Object.fromEntries(Object.entries(subjectCounts).map(([subject, documents]) => [subject, documents.length])),
    { 數學: 21, 物理: 11, 化學: 16 },
  );
  assert.equal(new Set(catalog.documents.map((document) => document.chapterKey)).size, 48);
  assert.equal(new Set(catalog.documents.map((document) => document.identity.idStem)).size, 48);
});

