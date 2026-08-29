const privateTextChecks = [
  [/\/Users(?:\/|$)/iu, "macOS 使用者絕對路徑"],
  [/\/home\/[^/\s]+(?:\/|$)/iu, "Linux 使用者絕對路徑"],
  [/[A-Za-z]:[\\/]Users[\\/]/u, "Windows 使用者絕對路徑"],
  [/(?:^|[\s("'`=])~[\\/]/mu, "家目錄縮寫路徑"],
  [/\bfile\s*:/iu, "file: URL"],
  [/\bLocalDocuments\b/iu, "本機 LocalDocuments 路徑"],
  [/高中教材(?:[\\/]|$)/iu, "私有高中教材路徑"],
];

const activeHtmlTags = "script|iframe|frame|frameset|object|embed|applet|base|link|form|input|button|textarea";
const htmlUrlAttributes = "href|src|srcset|poster|action|formaction|xlink:href|background|ping|manifest|lowsrc|dynsrc|usemap|profile|codebase|archive|classid|longdesc";
const allowedPandocKeyValueAttributes = new Set(["data-kind", "width"]);
const allowedDataUrl = /^data:(?:image\/(?:png|jpeg|gif|webp|svg\+xml)|font\/(?:ttf|otf|woff2?)|application\/font-woff);base64,/iu;

export class PublicationSafetyError extends Error {
  constructor(message) {
    super(message);
    this.name = "PublicationSafetyError";
  }
}

function fail(message) {
  throw new PublicationSafetyError(message);
}

function decodePercentRuns(value) {
  return value.replace(/(?:%[0-9a-f]{2})+/giu, (encoded) => {
    try {
      return decodeURIComponent(encoded);
    } catch {
      return encoded.replace(/%([0-9a-f]{2})/giu, (_, hex) => String.fromCharCode(Number.parseInt(hex, 16)));
    }
  });
}

function decodeHtmlEntities(value) {
  const named = new Map([
    ["amp", "&"],
    ["bsol", "\\"],
    ["colon", ":"],
    ["equals", "="],
    ["period", "."],
    ["quest", "?"],
    ["sol", "/"],
  ]);
  return value
    .replace(/&#(?:x([0-9a-f]+)|([0-9]+));?/giu, (entity, hex, decimal) => {
      const codePoint = Number.parseInt(hex ?? decimal, hex ? 16 : 10);
      if (!Number.isInteger(codePoint) || codePoint < 0 || codePoint > 0x10ffff) return entity;
      try {
        return String.fromCodePoint(codePoint);
      } catch {
        return entity;
      }
    })
    .replace(/&(amp|bsol|colon|equals|period|quest|sol);/giu, (_, name) => named.get(name.toLowerCase()));
}

function decodeCssEscapes(value) {
  return value
    .replace(/\\([0-9a-f]{1,6})(?:\r\n|[\t\n\f\r ])?/giu, (escape, hex) => {
      const codePoint = Number.parseInt(hex, 16);
      if (codePoint === 0 || codePoint > 0x10ffff) return "\uFFFD";
      return String.fromCodePoint(codePoint);
    })
    .replace(/\\([^\r\n0-9a-f])/giu, "$1");
}

export function decodedSafetyText(value) {
  let decoded = String(value);
  for (let index = 0; index < 3; index += 1) {
    const next = decodeHtmlEntities(decodePercentRuns(decoded));
    if (next === decoded) break;
    decoded = next;
  }
  return decoded.normalize("NFKC");
}

export function assertNoPrivateText(value, label) {
  const decoded = decodedSafetyText(value);
  for (const [pattern, description] of privateTextChecks) {
    if (pattern.test(decoded)) fail(`${label} 含${description}`);
  }
  return decoded;
}

export function assertSafeSourceText(value, label) {
  const decoded = assertNoPrivateText(value, label);
  const forbiddenTokens = ["obsidian:", "javascript:", "$body$", "$if("];
  for (const token of forbiddenTokens) {
    if (decoded.toLowerCase().includes(token)) fail(`${label} 含禁止字串：${token}`);
  }
  if (/!?\[\[[\s\S]*?\]\]/u.test(decoded)) fail(`${label} 含 Obsidian wikilink／embed`);
  if (/^>\s*\[![A-Za-z][A-Za-z0-9_-]*\]/mu.test(decoded)) fail(`${label} 含 Obsidian callout`);
  if (/<\s*\/?\s*(?:script|iframe|object|embed|base|link)\b/iu.test(decoded)) {
    fail(`${label} 含禁止 HTML 元素`);
  }
  if (/\son[a-z0-9_-]+\s*=/iu.test(decoded)) fail(`${label} 含 HTML event handler`);
  return decoded;
}

export function assertNoUrlSecrets(value, label) {
  let parsed;
  try {
    parsed = new URL(value);
  } catch {
    fail(`${label} 格式無效`);
  }
  if (parsed.username || parsed.password) fail(`${label} 不得在 URL 內嵌帳號或密碼`);
  const assertSafeKeys = (parameters) => {
    for (const key of parameters.keys()) {
      const normalized = key.normalize("NFKC").toLowerCase().replace(/[^a-z0-9]/gu, "");
      if (/(?:accesstoken|apikey|auth|authorization|credential|password|secret|sig|signature|token)$/u.test(normalized)) {
        fail(`${label} 疑似含憑證或簽章參數`);
      }
    }
  };
  assertSafeKeys(parsed.searchParams);
  const decodedHash = decodedSafetyText(parsed.hash.slice(1));
  if (decodedHash.includes("=")) {
    assertSafeKeys(new URLSearchParams(decodedHash));
    const queryLike = decodedHash.includes("?") ? decodedHash.slice(decodedHash.indexOf("?") + 1) : "";
    if (queryLike) assertSafeKeys(new URLSearchParams(queryLike));
  }
  return parsed;
}

export function assertSafePublicLinkTarget(raw, label = "連結") {
  const value = String(raw).trim();
  const decoded = assertNoPrivateText(value, `${label} URL`);
  if (!value) fail(`${label} target 不得為空`);
  if (value.normalize("NFKC") !== value) fail(`${label} URL 結構不得使用會被 NFKC 改寫的相容字元`);
  if (/[\u0000-\u001f\u007f]/u.test(value) || /[\u0000-\u001f\u007f]/u.test(decoded) || value.startsWith("//")) {
    fail(`${label} URL 不安全`);
  }
  if (value.startsWith("#")) return value;

  const scheme = value.match(/^([A-Za-z][A-Za-z0-9+.-]*):/u)?.[1]?.toLowerCase();
  if (!scheme) fail(`${label} 只允許 https、mailto 或 #fragment，不得使用本機相對路徑`);
  if (!new Set(["https", "mailto"]).has(scheme)) fail(`${label} 不允許 ${scheme}: URL`);
  const parsed = assertNoUrlSecrets(value, `${label} URL`);
  if (parsed.protocol !== `${scheme}:`) fail(`${label} URL protocol 無效`);
  if (decoded !== value) assertNoUrlSecrets(decoded, `${label} URL`);
  return value;
}

export function decodeLocalResourceTarget(raw, label, { allowParentSegments = false } = {}) {
  const wrapped = String(raw).trim();
  const unwrapped = wrapped.startsWith("<") && wrapped.endsWith(">") ? wrapped.slice(1, -1) : wrapped;
  const value = assertNoPrivateText(decodedSafetyText(unwrapped), label);
  if (!value || /[\u0000-\u001f\u007f]/u.test(value)) fail(`${label} 的本機資源路徑無效`);
  if (/^[A-Za-z][A-Za-z0-9+.-]*:/u.test(value) || value.startsWith("//")) {
    fail(`${label} 不得引用遠端或 URI 資源：${raw}`);
  }
  if (value.includes("?") || value.includes("#")) fail(`${label} 的本機資源路徑不得含 query／fragment：${raw}`);
  if (/^[\\/]/u.test(value) || /^[A-Za-z]:[\\/]/u.test(value) || /^~[\\/]/u.test(value)) {
    fail(`${label} 不得使用本機絕對路徑：${raw}`);
  }
  if (value.includes("\\")) fail(`${label} 請使用可攜式的正斜線路徑：${raw}`);
  if (value !== value.normalize("NFC")) fail(`${label} 必須使用 NFC Unicode：${raw}`);
  const segments = value.split("/");
  if (segments.some((segment) => !segment || segment === "." || (!allowParentSegments && segment === ".."))) {
    fail(`${label} 含不安全路徑片段：${raw}`);
  }
  return value;
}

export function assertSafeRawHtml(raw, label) {
  const decoded = assertNoPrivateText(raw, label);
  if (/<meta\b[^>]*\bhttp-equiv\s*=\s*["']?refresh\b/iu.test(decoded)) {
    fail(`${label} 的 raw HTML 不得使用 meta refresh`);
  }
  if (new RegExp(`<\\s*\\/?\\s*(?:${activeHtmlTags})\\b`, "iu").test(decoded)) {
    fail(`${label} 含不可執行或可載入外部內容的 raw HTML 標籤`);
  }
  if (/\s(?:on[a-z0-9_-]+|srcdoc)\s*=/iu.test(decoded)) {
    fail(`${label} 含事件處理器或 srcdoc 屬性`);
  }
  if (new RegExp(`\\b(?:${htmlUrlAttributes}|style)\\s*=`, "iu").test(decoded)) {
    fail(`${label} 的 raw HTML 不得自行指定 URL 或 style；請改用標準 Markdown`);
  }
  return decoded;
}

function isPandocAttr(value) {
  return Array.isArray(value)
    && value.length === 3
    && typeof value[0] === "string"
    && Array.isArray(value[1])
    && value[1].every((entry) => typeof entry === "string")
    && Array.isArray(value[2])
    && value[2].every((entry) => Array.isArray(entry)
      && entry.length === 2
      && entry.every((part) => typeof part === "string"));
}

function assertSafePandocAttr(attr, label) {
  const [identifier, classes, keyValues] = attr;
  for (const [kind, value] of [["id", identifier], ...classes.map((name) => ["class", name])]) {
    assertNoPrivateText(value, `${label} ${kind}`);
    if (/[\u0000-\u001f\u007f]/u.test(value)) fail(`${label} ${kind} 含控制字元`);
  }

  const seen = new Set();
  for (const [rawKey, rawValue] of keyValues) {
    const key = rawKey.normalize("NFKC").toLowerCase();
    if (seen.has(key)) fail(`${label} attribute 重複：${rawKey}`);
    seen.add(key);
    if (key === "style" || key === "srcdoc" || key.startsWith("on")) {
      fail(`${label} 含禁止 attribute：${rawKey}`);
    }
    if (!allowedPandocKeyValueAttributes.has(key) || rawKey !== key) {
      fail(`${label} 含未列入安全 allowlist 的 attribute：${rawKey}`);
    }
    const value = assertNoPrivateText(rawValue, `${label} attribute ${key}`);
    if (key === "width" && !/^(?:100|[1-9]?[0-9])(?:\.[0-9]+)?%$/u.test(value)) {
      fail(`${label} width 必須是 0%–100% 的百分比`);
    }
    if (key === "data-kind" && !/^[a-z][a-z0-9-]{0,39}$/u.test(value)) {
      fail(`${label} data-kind 必須是短小寫 ASCII token`);
    }
  }
}

export function inspectPandocAstSafety(ast, { label = "Markdown", onImage } = {}) {
  const images = [];
  function walk(value) {
    if (Array.isArray(value)) {
      if (isPandocAttr(value)) assertSafePandocAttr(value, label);
      value.forEach(walk);
      return;
    }
    if (!value || typeof value !== "object") return;

    if (value.t === "Image") {
      const rawTarget = value.c?.[2]?.[0];
      if (typeof rawTarget !== "string") fail(`${label} 含無效 Image target`);
      const target = decodeLocalResourceTarget(rawTarget, `${label} 圖片`);
      const title = value.c?.[2]?.[1];
      if (typeof title === "string") assertNoPrivateText(title, `${label} 圖片 title`);
      images.push(target);
      onImage?.(target, rawTarget, value);
    }
    if (value.t === "Link") {
      const rawTarget = value.c?.[2]?.[0];
      if (typeof rawTarget !== "string") fail(`${label} 含無效 Link target`);
      assertSafePublicLinkTarget(rawTarget, `${label} 連結`);
      const title = value.c?.[2]?.[1];
      if (typeof title === "string") assertNoPrivateText(title, `${label} 連結 title`);
    }
    if (["RawBlock", "RawInline"].includes(value.t) && /^html[0-9]*$/iu.test(value.c?.[0] ?? "")) {
      assertSafeRawHtml(value.c?.[1] ?? "", label);
    }
    Object.values(value).forEach(walk);
  }
  walk(ast);
  return images;
}

function cssUrlTargets(css, label) {
  const decoded = decodeCssEscapes(assertNoPrivateText(css, label));
  if (/@import\b/iu.test(decoded)) fail(`${label} 不得使用 CSS @import`);
  if (/(?:^|[^A-Za-z0-9_-])(?:-webkit-)?image-set\s*\(/iu.test(decoded)) {
    fail(`${label} 不得使用 CSS image-set()`);
  }
  const targets = [];
  const marker = /\burl\s*\(/giu;
  let match;
  while ((match = marker.exec(decoded)) !== null) {
    let cursor = marker.lastIndex;
    while (/\s/u.test(decoded[cursor] ?? "")) cursor += 1;
    const quote = new Set(["\"", "'"]).has(decoded[cursor]) ? decoded[cursor] : undefined;
    let end;
    if (quote) {
      cursor += 1;
      end = decoded.indexOf(quote, cursor);
      if (end < 0) fail(`${label} 含無法安全解析的 CSS url()`);
      let close = end + 1;
      while (/\s/u.test(decoded[close] ?? "")) close += 1;
      if (decoded[close] !== ")") fail(`${label} 含無法安全解析的 CSS url()`);
      marker.lastIndex = close + 1;
    } else {
      end = decoded.indexOf(")", cursor);
      if (end < 0) fail(`${label} 含無法安全解析的 CSS url()`);
      if (/["'\s]/u.test(decoded.slice(cursor, end))) fail(`${label} 含無法安全解析的 CSS url()`);
      marker.lastIndex = end + 1;
    }
    targets.push(decoded.slice(cursor, end));
  }
  return targets;
}

export function assertSafeCssText(css, label, { allowData = true, onLocalUrl } = {}) {
  const localTargets = [];
  for (const rawTarget of cssUrlTargets(css, label)) {
    const target = decodedSafetyText(rawTarget).trim();
    if (!target) fail(`${label} 含空白 CSS url()`);
    if (target.startsWith("#")) continue;
    if (target.toLowerCase().startsWith("data:")) {
      if (!allowData || !allowedDataUrl.test(target)) fail(`${label} 含未允許的 data: URL`);
      continue;
    }
    const localTarget = decodeLocalResourceTarget(target, `${label} CSS URL`, { allowParentSegments: true });
    localTargets.push(localTarget);
    onLocalUrl?.(localTarget, rawTarget);
  }
  return localTargets;
}

export function assertSafeSvgText(svg, label) {
  const decoded = assertNoPrivateText(svg, label);
  if (!/<svg\b/iu.test(decoded)) fail(`${label} 不是自足 SVG`);
  if (/<\s*\/?\s*(?:script|foreignObject|iframe|object|embed)\b/iu.test(decoded)) {
    fail(`${label} 含 script／foreignObject 或其他主動內容元素`);
  }
  if (/<!ENTITY\b/iu.test(decoded)) fail(`${label} 含 XML entity 宣告`);
  if (/\s(?:on[a-z0-9_-]+|srcdoc)\s*=/iu.test(decoded)) fail(`${label} 含事件處理器或 srcdoc`);

  const hrefPattern = /\b(?:href|xlink:href)\s*=\s*(?:"([^"]*)"|'([^']*)'|([^\s>]+))/giu;
  for (const match of decoded.matchAll(hrefPattern)) {
    const target = (match[1] ?? match[2] ?? match[3] ?? "").trim();
    if (!target.startsWith("#")) fail(`${label} 含外部 href`);
  }
  const localCssTargets = assertSafeCssText(decoded, label, { allowData: false });
  if (localCssTargets.length > 0) fail(`${label} 含外部 CSS url()`);
  return decoded;
}

function assertSafeEmbeddedUrl(raw, attribute, label) {
  const value = String(raw).trim();
  const decoded = assertNoPrivateText(value, `${label} ${attribute}`);
  if (!value) fail(`${label} ${attribute} target 不得為空`);
  if (attribute === "href" || attribute === "xlink:href") {
    return assertSafePublicLinkTarget(value, `${label} ${attribute}`);
  }
  if (attribute === "srcset") fail(`${label} 不允許 srcset；請使用單一已內嵌 src`);
  if (attribute === "usemap") {
    if (!value.startsWith("#")) fail(`${label} usemap 只允許本文件 fragment`);
    return value;
  }
  if ([
    "action",
    "archive",
    "background",
    "classid",
    "codebase",
    "dynsrc",
    "formaction",
    "longdesc",
    "lowsrc",
    "manifest",
    "ping",
    "profile",
  ].includes(attribute)) {
    fail(`${label} 不允許會導致導覽、提交或資源載入的 ${attribute} attribute`);
  }
  if (value.startsWith("#")) return value;
  if (!allowedDataUrl.test(value) || decoded !== value) fail(`${label} ${attribute} 仍有未內嵌或未允許資源 URL`);
  return value;
}

function htmlCssContexts(html, label) {
  const contexts = [];
  const styleOpening = /<style\b[^>]*>/giu;
  const styleClosing = /<\/style\s*>/giu;
  let match;
  let blockCount = 0;
  while ((match = styleOpening.exec(html)) !== null) {
    styleClosing.lastIndex = styleOpening.lastIndex;
    const closing = styleClosing.exec(html);
    if (!closing) fail(`${label} 含未關閉的 style element`);
    contexts.push({ css: html.slice(styleOpening.lastIndex, closing.index), kind: "style element" });
    blockCount += 1;
    styleOpening.lastIndex = styleClosing.lastIndex;
  }
  if ([...html.matchAll(/<\/style\s*>/giu)].length !== blockCount) {
    fail(`${label} 含無法配對的 closing style element`);
  }

  const startTagPattern = /<[A-Za-z][^>]*>/gu;
  const styleAttributePattern = /\bstyle\s*=\s*(?:"([^"]*)"|'([^']*)'|([^\s>]+))/giu;
  for (const tag of html.matchAll(startTagPattern)) {
    for (const attribute of tag[0].matchAll(styleAttributePattern)) {
      contexts.push({ css: attribute[1] ?? attribute[2] ?? attribute[3] ?? "", kind: "style attribute" });
    }
  }
  return contexts;
}

function removeSafePandocCheckboxInputs(html, label) {
  const inputTagPattern = /<\s*(\/?)\s*input\b([^>]*)>/giu;
  return html.replace(inputTagPattern, (tag, closing, rawAttributes) => {
    if (closing) {
      if (rawAttributes.trim()) fail(`${label} 的 closing input tag 不得有 attributes`);
      return "";
    }

    let attributes = rawAttributes.trim();
    if (attributes.endsWith("/")) attributes = attributes.slice(0, -1).trimEnd();
    const entries = [];
    const pattern = /([A-Za-z][A-Za-z0-9:-]*)(?:\s*=\s*(?:"([^"]*)"|'([^']*)'|([^\s"'=<>`]+)))?/gy;
    let cursor = 0;
    while (cursor < attributes.length) {
      while (/\s/u.test(attributes[cursor] ?? "")) cursor += 1;
      if (cursor >= attributes.length) break;
      pattern.lastIndex = cursor;
      const match = pattern.exec(attributes);
      if (!match) fail(`${label} 的 input tag attributes 無法安全解析`);
      cursor = pattern.lastIndex;
      if (cursor < attributes.length && !/\s/u.test(attributes[cursor])) {
        fail(`${label} 的 input tag attributes 無法安全解析`);
      }
      entries.push({
        name: match[1].toLowerCase(),
        value: match[2] ?? match[3] ?? match[4],
      });
    }

    const seen = new Set();
    for (const { name, value } of entries) {
      if (seen.has(name)) fail(`${label} 的 input tag attribute 重複：${name}`);
      seen.add(name);
      if (name === "type") {
        if (value !== "checkbox") fail(`${label} 的 input 只允許 type=checkbox`);
        continue;
      }
      if (["disabled", "checked"].includes(name)) {
        if (value !== undefined && value !== "") fail(`${label} 的 input ${name} 只允許 boolean 空值`);
        continue;
      }
      fail(`${label} 的 checkbox input 含禁止 attribute：${name}`);
    }
    if (!seen.has("type")) fail(`${label} 的 input 必須明確指定 type=checkbox`);
    return "";
  });
}

export function assertSafeHtmlText(html, label = "輸出 HTML") {
  const structural = String(html);
  assertNoPrivateText(structural, label);
  const withoutSafeCheckboxes = removeSafePandocCheckboxInputs(structural, label);
  if (new RegExp(`<\\s*\\/?\\s*(?:${activeHtmlTags})\\b`, "iu").test(withoutSafeCheckboxes)) {
    fail(`${label} 含主動內容或未內嵌資源標籤`);
  }
  if (/\s(?:on[a-z0-9_-]+|srcdoc)\s*=/iu.test(structural)) fail(`${label} 含事件處理器或 srcdoc`);
  if (/<meta\b[^>]*\bhttp-equiv\s*=\s*["']?refresh\b/iu.test(structural)) fail(`${label} 不得使用 meta refresh`);

  const attributePattern = new RegExp(`\\b(${htmlUrlAttributes})\\s*=\\s*(?:"([^"]*)"|'([^']*)'|([^\\s>]+))`, "giu");
  for (const match of structural.matchAll(attributePattern)) {
    assertSafeEmbeddedUrl(match[2] ?? match[3] ?? match[4] ?? "", match[1].toLowerCase(), label);
  }
  for (const { css, kind } of htmlCssContexts(structural, label)) {
    const localCssTargets = assertSafeCssText(css, `${label} ${kind}`, { allowData: true });
    if (localCssTargets.length > 0) fail(`${label} ${kind} 仍有未內嵌資源 URL`);
  }
  return structural;
}
