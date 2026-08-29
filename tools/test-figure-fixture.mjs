import { createHash } from "node:crypto";
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { join } from "node:path";

function sha256Bytes(bytes) {
  return createHash("sha256").update(bytes).digest("hex");
}

function sha256File(path) {
  return sha256Bytes(readFileSync(path));
}

export function writeFigureManifestFixture(root, outputPaths = []) {
  const tools = join(root, "_tools");
  mkdirSync(tools, { recursive: true });
  const figlibPath = join(tools, "figlib.py");
  writeFileSync(figlibPath, "# publication focused-test figure fixture\n", "utf8");

  const generators = [];
  if (outputPaths.length > 0) {
    const scriptRelative = "_tools/fixture_figures.py";
    const scriptPath = join(root, scriptRelative);
    writeFileSync(scriptPath, "# manifest owner only; focused publication tests do not execute this file\n", "utf8");
    generators.push({
      id: "focused-fixture",
      command: ["python", scriptRelative],
      inputs: [{ path: scriptRelative, sha256: sha256File(scriptPath) }],
      outputs: outputPaths.map((path, index) => ({
        path,
        entrypoint: `fixture_${index + 1}`,
        sha256: sha256File(join(root, path)),
      })),
    });
  }

  const manifest = {
    schemaVersion: 1,
    runtime: {
      implementation: "CPython",
      python: "3.14.3",
      numpy: "2.4.6",
      matplotlib: "3.11.0",
      freetype: "2.14.3",
    },
    sharedInputs: [{ path: "_tools/figlib.py", sha256: sha256File(figlibPath) }],
    generators,
  };
  writeFileSync(join(root, "publishing", "figures.json"), `${JSON.stringify(manifest, null, 2)}\n`, "utf8");
}
