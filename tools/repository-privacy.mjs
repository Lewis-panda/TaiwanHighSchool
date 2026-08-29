#!/usr/bin/env node

import { spawnSync } from "node:child_process";
import { lstatSync, realpathSync } from "node:fs";
import { resolve } from "node:path";

export class RepositoryPrivacyError extends Error {}

function reject(message) {
  throw new RepositoryPrivacyError(message);
}

function runGit(repoRoot, args, { allowNotIgnored = false } = {}) {
  const result = spawnSync("git", args, {
    cwd: repoRoot,
    encoding: "utf8",
    maxBuffer: 64 * 1024 * 1024,
  });
  if (result.error) reject(`git ${args[0]} 無法執行：${result.error.message}`);
  if (allowNotIgnored && result.status === 1) return result;
  if (result.status !== 0) {
    const detail = [result.stdout, result.stderr].filter(Boolean).join("\n").trim();
    reject(`git ${args[0]} 結束碼 ${result.status}${detail ? `：${detail}` : ""}`);
  }
  return result;
}

function canonicalRepositoryRoot(candidate) {
  const root = resolve(candidate);
  const entry = lstatSync(root);
  if (entry.isSymbolicLink() || !entry.isDirectory() || realpathSync(root) !== root) {
    reject(`repository root 必須是 canonical 一般目錄：${root}`);
  }
  const gitRoot = realpathSync(runGit(root, ["rev-parse", "--show-toplevel"]).stdout.trim());
  if (gitRoot !== root) reject(`repository root 與 Git top-level 不一致：${root}`);
  return root;
}

export function privateTrackedPathReason(path) {
  const segments = path.split("/");
  if (segments.includes("高中教材")) return "本機高中教材";
  if (path.startsWith("content/") && path.endsWith("/編輯判定.md")) return "本機編輯判定";
  return undefined;
}

const ignoreProbes = Object.freeze([
  Object.freeze({
    label: "高中教材/",
    path: "高中教材/__privacy-boundary-probe__.pdf",
  }),
  Object.freeze({
    label: "content/**/編輯判定.md",
    path: "content/__privacy-course__/__privacy-chapter__/編輯判定.md",
  }),
]);

export function repositoryPrivacyState(candidateRoot) {
  const repoRoot = canonicalRepositoryRoot(candidateRoot);
  const tracked = runGit(repoRoot, ["ls-files", "-z"]).stdout
    .split("\0")
    .filter(Boolean);
  const trackedPrivatePaths = tracked
    .filter((path) => privateTrackedPathReason(path))
    .sort((left, right) => left < right ? -1 : left > right ? 1 : 0);
  const missingIgnoreRules = ignoreProbes
    .filter(({ path }) => runGit(
      repoRoot,
      ["check-ignore", "-q", "--no-index", "--", path],
      { allowNotIgnored: true },
    ).status !== 0)
    .map(({ label }) => label);
  return { trackedPrivatePaths, missingIgnoreRules };
}

export function assertRepositoryPrivacyBoundary(repoRoot) {
  const state = repositoryPrivacyState(repoRoot);
  if (state.trackedPrivatePaths.length > 0) {
    const details = state.trackedPrivatePaths
      .map((path) => `${path}（${privateTrackedPathReason(path)}）`)
      .join("、");
    reject(`Git 已追蹤不得公開的本機資料：${details}`);
  }
  if (state.missingIgnoreRules.length > 0) {
    reject(`.gitignore 缺少本機資料邊界：${state.missingIgnoreRules.join("、")}`);
  }
  return state;
}
