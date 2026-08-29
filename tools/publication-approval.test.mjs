import assert from "node:assert/strict";
import test from "node:test";
import {
  assertApprovedPdfDigest,
  validateSetDefinition,
} from "./publication.mjs";

const studentDigest = "a".repeat(64);

function documents() {
  return [
    {
      id: "math-a3-9-student",
      audience: "student",
      source: "content/數學A/數A3-9/學生講義.md",
      slug: "數A3-9-測試章-學生講義",
      assets: [],
    },
  ];
}

function reviewSet() {
  return {
    status: "review",
    description: "approval gate review fixture",
    documents: documents(),
  };
}

function publishedSet(overrides = {}) {
  return {
    status: "published",
    description: "approval gate published fixture",
    documents: documents(),
    approval: {
      approvedAt: "2026-08-24",
      artifactPdfSha256: {
        "math-a3-9-student": studentDigest,
      },
    },
    ...overrides,
  };
}

test("student-only review set remains legal and carries no approval", () => {
  const set = reviewSet();
  assert.equal(set.status, "review");
  assert.equal(Object.hasOwn(set, "approval"), false);
  assert.doesNotThrow(() => validateSetDefinition("review-approval-test", set));
});

test("one-line review status flip cannot become published", () => {
  const flipped = { ...reviewSet(), status: "published" };
  assert.throws(() => validateSetDefinition("review-approval-test", flipped));
});

test("status and set-id prefix cannot disagree even with a complete approval", () => {
  assert.throws(
    () => validateSetDefinition("review-approval-test", publishedSet()),
    /set id 必須以 published-/u,
  );
  assert.throws(
    () => validateSetDefinition("published-approval-test", reviewSet()),
    /set id 必須以 review-/u,
  );
});

test("review set rejects an approval field", () => {
  const set = { ...reviewSet(), approval: publishedSet().approval };
  assert.throws(() => validateSetDefinition("review-approval-test", set), /欄位集合無效/u);
});

test("published approval accepts the exact schema and exact PDF digests", () => {
  const set = publishedSet();
  assert.doesNotThrow(() => validateSetDefinition("published-approval-test", set));
  assert.doesNotThrow(() => assertApprovedPdfDigest(
    "published-approval-test",
    set,
    "math-a3-9-student",
    studentDigest,
  ));
});

test("published release/verify digest check rejects a different valid PDF hash", () => {
  const set = publishedSet();
  validateSetDefinition("published-approval-test", set);
  assert.throws(
    () => assertApprovedPdfDigest("published-approval-test", set, "math-a3-9-student", "c".repeat(64)),
    /does not match approval/u,
  );
});

test("published approval rejects a missing document hash", () => {
  const set = publishedSet();
  delete set.approval.artifactPdfSha256["math-a3-9-student"];
  assert.throws(
    () => validateSetDefinition("published-approval-test", set),
    /精確覆蓋 documents ID/u,
  );
});

test("review and published schemas reject teacher documents", () => {
  const teacher = {
    id: "math-a3-9-teacher",
    audience: "teacher",
    source: "content/數學A/數A3-9/教師備課指南.md",
    slug: "數A3-9-測試章-教師備課指南",
    assets: [],
  };
  const review = reviewSet();
  review.documents.push(teacher);
  assert.throws(
    () => validateSetDefinition("review-approval-test", review),
    /audience 必須是 student/u,
  );
  const published = publishedSet();
  published.documents.push(teacher);
  published.approval.artifactPdfSha256[teacher.id] = "b".repeat(64);
  assert.throws(
    () => validateSetDefinition("published-approval-test", published),
    /audience 必須是 student/u,
  );
});

test("published approval rejects an extra or unknown document hash", () => {
  const set = publishedSet();
  set.approval.artifactPdfSha256["math-a3-9-unknown"] = "c".repeat(64);
  assert.throws(
    () => validateSetDefinition("published-approval-test", set),
    /精確覆蓋 documents ID/u,
  );
});

test("published approval rejects unknown schema fields", () => {
  const set = publishedSet();
  set.approval.note = "not in the exact schema";
  assert.throws(
    () => validateSetDefinition("published-approval-test", set),
    /must contain exactly approvedAt and artifactPdfSha256/u,
  );
});

test("published approval rejects an invalid calendar date", () => {
  const set = publishedSet();
  set.approval.approvedAt = "2026-02-29";
  assert.throws(
    () => validateSetDefinition("published-approval-test", set),
    /不是有效曆日/u,
  );
});

test("published approval rejects a non-canonical SHA-256 value", () => {
  const set = publishedSet();
  set.approval.artifactPdfSha256["math-a3-9-student"] = "A".repeat(64);
  assert.throws(
    () => validateSetDefinition("published-approval-test", set),
    /64 位小寫十六進位 SHA-256/u,
  );
});
