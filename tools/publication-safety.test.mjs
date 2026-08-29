import assert from "node:assert/strict";
import test from "node:test";

import {
  PublicationSafetyError,
  assertNoPrivateText,
  assertSafeCssText,
  assertSafeHtmlText,
  assertSafePublicLinkTarget,
  assertSafeSourceText,
  assertSafeSvgText,
  decodedSafetyText,
  inspectPandocAstSafety,
} from "./publication-safety.mjs";

function pandocDocument(blocks) {
  return {
    "pandoc-api-version": [1, 23, 1],
    meta: {},
    blocks,
  };
}

function expectUnsafe(action, pattern) {
  assert.throws(action, (error) => {
    assert.ok(error instanceof PublicationSafetyError);
    assert.match(error.message, pattern);
    return true;
  });
}

test("decoded/NFKC private-path scan catches encoded host paths", () => {
  assert.equal(decodedSafetyText("%252Fhome%252Falice%252Fsecret.txt"), "/home/alice/secret.txt");
  expectUnsafe(
    () => assertNoPrivateText("&#x2f;Users&#x2f;alice&#x2f;private", "fixture"),
    /macOS 使用者絕對路徑/u,
  );
  expectUnsafe(
    () => assertSafeSourceText("請讀 /home/alice/secret.txt", "fixture"),
    /Linux 使用者絕對路徑/u,
  );
});

test("public source rejects hidden C0 control characters", () => {
  expectUnsafe(
    () => assertSafeSourceText("H=A+\ffrac{u}{v}", "fixture"),
    /控制字元/u,
  );
  assert.equal(assertSafeSourceText("第一行\n第二行\t欄位", "fixture"), "第一行\n第二行\t欄位");
});

test("public links allow only https, mailto and fragments without secrets", () => {
  assert.equal(assertSafePublicLinkTarget("#section"), "#section");
  assert.equal(assertSafePublicLinkTarget("https://example.edu/chapter"), "https://example.edu/chapter");
  assert.equal(assertSafePublicLinkTarget("mailto:teacher@example.edu"), "mailto:teacher@example.edu");
  expectUnsafe(() => assertSafePublicLinkTarget("http://example.edu"), /不允許 http:/u);
  expectUnsafe(() => assertSafePublicLinkTarget("../legacy/old.html"), /本機相對路徑/u);
  expectUnsafe(() => assertSafePublicLinkTarget("research/notes.md"), /本機相對路徑/u);
  expectUnsafe(() => assertSafePublicLinkTarget("https%3A%2F%2Fexample.edu/file"), /本機相對路徑/u);
  expectUnsafe(() => assertSafePublicLinkTarget("https：／／example.edu/file"), /NFKC/u);
  expectUnsafe(
    () => assertSafePublicLinkTarget("https://example.edu/file?access_token=secret"),
    /憑證或簽章/u,
  );
  expectUnsafe(
    () => assertSafePublicLinkTarget("https://user:password@example.edu/file"),
    /帳號或密碼/u,
  );
  const secret = "DO_NOT_ECHO_THIS_SECRET";
  assert.throws(
    () => assertSafePublicLinkTarget(`https://example.edu/callback#access_token=${secret}`),
    (error) => {
      assert.match(error.message, /憑證或簽章/u);
      assert.ok(!error.message.includes(secret));
      return true;
    },
  );
});

test("Pandoc walk rejects HTTP/local links and active raw HTML", () => {
  const httpLink = pandocDocument([{
    t: "Para",
    c: [{ t: "Link", c: [["", [], []], [{ t: "Str", c: "x" }], ["http://example.com", ""]] }],
  }]);
  expectUnsafe(() => inspectPandocAstSafety(httpLink), /不允許 http:/u);

  const localLink = pandocDocument([{
    t: "Para",
    c: [{ t: "Link", c: [["", [], []], [{ t: "Str", c: "舊稿" }], ["../legacy/old.md", ""]] }],
  }]);
  expectUnsafe(() => inspectPandocAstSafety(localLink), /本機相對路徑/u);

  const rawForm = pandocDocument([{ t: "RawBlock", c: ["html", "<form><input name='x'></form>"] }]);
  expectUnsafe(() => inspectPandocAstSafety(rawForm), /raw HTML 標籤/u);

  const rawBackground = pandocDocument([{ t: "RawBlock", c: ["html", `<table background="https://example.com/x.png">`] }]);
  expectUnsafe(() => inspectPandocAstSafety(rawBackground), /raw HTML 不得自行指定 URL/u);

  const rawRefresh = pandocDocument([{ t: "RawBlock", c: ["html", `<meta http-equiv="refresh" content="0;url=https://example.com">`] }]);
  expectUnsafe(() => inspectPandocAstSafety(rawRefresh), /raw HTML 不得使用 meta refresh/u);
});

test("Pandoc native Attr walk rejects style/events/srcdoc and unknown data attributes", () => {
  for (const key of ["style", "onclick", "srcdoc", "data-source"]) {
    const ast = pandocDocument([{ t: "Div", c: [["", ["concept"], [[key, "unsafe"]]], []] }]);
    expectUnsafe(
      () => inspectPandocAstSafety(ast),
      key === "data-source" ? /未列入安全 allowlist/u : /禁止 attribute/u,
    );
  }
});

test("Pandoc native Attr allowlist preserves current fenced-div and image attributes", () => {
  const images = [];
  const ast = pandocDocument([
    { t: "Div", c: [["why-this-works", ["teacher-note"], [["data-kind", "scope"]]], []] },
    {
      t: "Para",
      c: [{
        t: "Image",
        c: [["", [], [["width", "96%"]]], [{ t: "Str", c: "圖" }], ["assets/figure.svg", ""]],
      }],
    },
  ]);
  assert.deepEqual(inspectPandocAstSafety(ast, { onImage: (target) => images.push(target) }), ["assets/figure.svg"]);
  assert.deepEqual(images, ["assets/figure.svg"]);
});

test("SVG rejects active/external resources but permits local fragment paint servers", () => {
  const safe = `<svg xmlns="http://www.w3.org/2000/svg"><defs><clipPath id="p"/></defs><path clip-path="url(#p)"/></svg>`;
  assert.equal(assertSafeSvgText(safe, "fixture"), safe);
  expectUnsafe(
    () => assertSafeSvgText(`<svg><path fill="url(https://example.com/pattern.svg#p)"/></svg>`, "fixture"),
    /不得引用遠端|外部 CSS/u,
  );
  expectUnsafe(
    () => assertSafeSvgText(`<svg><style>@import "https://example.com/x.css";</style></svg>`, "fixture"),
    /@import/u,
  );
  expectUnsafe(() => assertSafeSvgText(`<svg onload="alert(1)"/>`, "fixture"), /事件處理器/u);
});

test("CSS rejects @import and remote URLs while reporting safe local dependencies", () => {
  expectUnsafe(
    () => assertSafeCssText(`@import "https://example.com/x.css";`, "fixture"),
    /@import/u,
  );
  expectUnsafe(
    () => assertSafeCssText(`.x { background: url(https://example.com/x.png); }`, "fixture"),
    /不得引用遠端/u,
  );
  for (const functionName of ["image-set", "-webkit-image-set"]) {
    expectUnsafe(
      () => assertSafeCssText(`.x { background: ${functionName}("https://example.com/one.png" 1x); }`, "fixture"),
      /image-set/u,
    );
  }
  const seen = [];
  const targets = assertSafeCssText(
    `@font-face { src: url("../assets/fonts/font.ttf") format("truetype"); }`,
    "fixture",
    { onLocalUrl: (target) => seen.push(target) },
  );
  assert.deepEqual(targets, ["../assets/fonts/font.ttf"]);
  assert.deepEqual(seen, targets);
});

test("final HTML requires embedded resources and applies public-link policy", () => {
  const safe = `<html><body><a href="#part">段落</a><img src="data:image/png;base64,AA=="></body></html>`;
  assert.equal(assertSafeHtmlText(safe, "fixture"), safe);
  expectUnsafe(
    () => assertSafeHtmlText(`<html><a href="legacy/old.html">舊稿</a></html>`, "fixture"),
    /本機相對路徑/u,
  );
  expectUnsafe(
    () => assertSafeHtmlText(`<html><img src="https://example.com/x.png"></html>`, "fixture"),
    /未內嵌/u,
  );
  expectUnsafe(
    () => assertSafeHtmlText(`<html><a href="https%3A%2F%2Fexample.com">encoded</a></html>`, "fixture"),
    /本機相對路徑/u,
  );
  expectUnsafe(
    () => assertSafeHtmlText(`<html><a href="https：／／example.com">fullwidth</a></html>`, "fixture"),
    /NFKC/u,
  );
  expectUnsafe(
    () => assertSafeHtmlText(`<html><table background="https://example.com/x.png"></table></html>`, "fixture"),
    /background attribute/u,
  );
});

test("final HTML narrowly permits Pandoc task-list checkbox variants", () => {
  const currentTeacherHtml = `<html><body><ul class="task-list">
    <li><label><input type="checkbox"></input>未勾選</label></li>
    <li><label><input type="checkbox" disabled="" />disabled</label></li>
    <li><label><input type="checkbox" disabled checked="" />checked</label></li>
  </ul></body></html>`;
  assert.equal(assertSafeHtmlText(currentTeacherHtml, "fixture"), currentTeacherHtml);
  for (const attribute of [
    `class="task-list-item-checkbox"`,
    `name="leak"`,
    `value="secret"`,
    `form="external"`,
    `id="box"`,
    `style="background:red"`,
    `onclick="alert(1)"`,
    `src="https://example.com/x"`,
  ]) {
    expectUnsafe(
      () => assertSafeHtmlText(`<html><input type="checkbox" ${attribute}></html>`, "fixture"),
      /checkbox input 含禁止 attribute|事件處理器/u,
    );
  }
  expectUnsafe(() => assertSafeHtmlText(`<html><input type="radio"></html>`, "fixture"), /只允許 type=checkbox/u);
  expectUnsafe(() => assertSafeHtmlText(`<html><input type="checkbox" disabled="false"></html>`, "fixture"), /boolean 空值/u);
});

test("final HTML scans CSS only in style elements and style attributes", () => {
  const prose = `<html><body><code>@import "https://example.com/x.css"; url(https://example.com/x.png)</code></body></html>`;
  assert.equal(assertSafeHtmlText(prose, "fixture"), prose);
  expectUnsafe(
    () => assertSafeHtmlText(`<html><style>@import "https://example.com/x.css";</style></html>`, "fixture"),
    /@import/u,
  );
  expectUnsafe(
    () => assertSafeHtmlText(`<html><div style="background:url(https://example.com/x.png)">x</div></html>`, "fixture"),
    /不得引用遠端/u,
  );
});
