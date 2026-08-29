import assert from "node:assert/strict";
import test from "node:test";

import {
  expectedDocumentId,
  leadingRegisteredChapterCode,
  resolveCourseIdentity,
} from "./course-identity.mjs";

const cases = [
  ["必修數學", "數1-4", "數學", "普通高中數學 第一冊", "math-required-1-4-student"],
  ["必修數學", "數2-3", "數學", "普通高中數學 第二冊", "math-required-2-3-student"],
  ["數學A", "數A4-4", "數學", "普通高中數學A 第四冊", "math-a4-4-student"],
  ["數學B", "數B3-2", "數學", "普通高中數學B 第三冊", "math-b3-2-student"],
  ["數學B", "數B4-3", "數學", "普通高中數學B 第四冊", "math-b4-3-student"],
  ["必修物理", "必物-6", "物理", "普通高中必修物理", "physics-required-6-student"],
  ["選修物理I", "選物I-5", "物理", "普通高中選修物理 I", "physics-i1-5-student"],
  ["必修化學", "必化-4", "化學", "普通高中必修化學", "chemistry-required-4-student"],
  ["選修化學I", "選化I-3", "化學", "普通高中選修化學 I", "chemistry-i1-3-student"],
  ["選修化學II", "選化II-3", "化學", "普通高中選修化學 II", "chemistry-i2-3-student"],
  ["選修化學III", "選化III-2", "化學", "普通高中選修化學 III", "chemistry-i3-2-student"],
  ["選修化學IV", "選化IV-2", "化學", "普通高中選修化學 IV", "chemistry-i4-2-student"],
  ["選修化學V", "選化V-2", "化學", "普通高中選修化學 V", "chemistry-i5-2-student"],
];

test("all locally sourced grade 10/11 course identities resolve canonically", () => {
  for (const [directory, chapterCode, subject, course, documentId] of cases) {
    const identity = resolveCourseIdentity(directory, chapterCode);
    assert.equal(identity.subject, subject);
    assert.equal(identity.course, course);
    assert.equal(expectedDocumentId(identity, "student"), documentId);
    assert.equal(leadingRegisteredChapterCode(`${chapterCode} 範例章`), chapterCode);
  }
});

test("course directories reject cross-course and non-canonical chapter codes", () => {
  assert.throws(() => resolveCourseIdentity("數學B", "數A3-1"), /不一致/u);
  assert.throws(() => resolveCourseIdentity("選修化學II", "選化I-1"), /不一致/u);
  assert.throws(() => resolveCourseIdentity("必修化學", "必化-0"), /不一致/u);
  assert.throws(() => resolveCourseIdentity("選修物理II", "選物II-1"), /尚未登記/u);
});

