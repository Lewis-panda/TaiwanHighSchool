#!/usr/bin/env node

import assert from "node:assert/strict";
import test from "node:test";
import { parseFigureManifestText } from "./figure-manifest.mjs";

const digest = "0".repeat(64);

function fixture() {
  return {
    schemaVersion: 1,
    runtime: {
      implementation: "CPython",
      python: "3.14.3",
      numpy: "2.4.6",
      matplotlib: "3.11.0",
      freetype: "2.14.3",
    },
    sharedInputs: [{ path: "_tools/figlib.py", sha256: digest }],
    generators: [
      {
        id: "math-a3-1",
        command: ["python", "_tools/figure.py", "--content-all"],
        inputs: [{ path: "_tools/figure.py", sha256: digest }],
        outputs: [
          {
            path: "content/數學A/數A3-1/assets/數A3-1-測試.svg",
            entrypoint: "fig_test",
            sha256: digest,
          },
        ],
      },
    ],
  };
}

function canonical(value) {
  return `${JSON.stringify(value, null, 2)}\n`;
}

test("accepts an exact canonical figure manifest", () => {
  const manifest = parseFigureManifestText(canonical(fixture()), "fixture");
  assert.equal(manifest.allInputs.length, 2);
  assert.equal(manifest.allOutputs.length, 1);
});

test("rejects duplicate JSON keys through canonical representation", () => {
  const text = canonical(fixture()).replace('"schemaVersion": 1,', '"schemaVersion": 1,\n  "schemaVersion": 1,');
  assert.throws(() => parseFigureManifestText(text, "fixture"), /canonical JSON/u);
});

test("rejects unknown fields", () => {
  const value = fixture();
  value.generators[0].shell = true;
  assert.throws(() => parseFigureManifestText(canonical(value), "fixture"), /欄位必須精確/u);
});

test("rejects duplicate output ownership", () => {
  const value = fixture();
  value.generators.push({
    id: "math-a3-2",
    command: ["python", "_tools/other.py"],
    inputs: [{ path: "_tools/other.py", sha256: digest }],
    outputs: structuredClone(value.generators[0].outputs),
  });
  assert.throws(() => parseFigureManifestText(canonical(value), "fixture"), /output owner 重複/u);
});

test("rejects unsafe paths and duplicate command options", () => {
  const unsafe = fixture();
  unsafe.generators[0].outputs[0].path = "../outside.svg";
  assert.throws(() => parseFigureManifestText(canonical(unsafe), "fixture"), /不安全 path segment|content\/.*assets/u);

  const duplicate = fixture();
  duplicate.generators[0].command.push("--content-all");
  assert.throws(() => parseFigureManifestText(canonical(duplicate), "fixture"), /command option 重複/u);
});
