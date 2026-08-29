const courseSchemas = Object.freeze({
  數學A: Object.freeze({
    chapterPattern: /^數A([34])-([1-9]\d*)$/u,
    subject: "數學",
    course(match) {
      return match[1] === "3" ? "普通高中數學A 第三冊" : "普通高中數學A 第四冊";
    },
    idStem(match) {
      return `math-a${match[1]}-${match[2]}`;
    },
  }),
  選修物理I: Object.freeze({
    chapterPattern: /^選物I-([1-9]\d*)$/u,
    subject: "物理",
    course() {
      return "普通高中選修物理 I";
    },
    idStem(match) {
      return `physics-i1-${match[1]}`;
    },
  }),
  必修物理: Object.freeze({
    chapterPattern: /^必物-([1-9]\d*)$/u,
    subject: "物理",
    course() {
      return "普通高中必修物理";
    },
    idStem(match) {
      return `physics-required-${match[1]}`;
    },
  }),
});

const registeredChapterCodeAtStart = /^(?:數A[34]-\d+|選物I-\d+|必物-\d+)/u;

function reject(message) {
  throw new Error(message);
}

export function resolveCourseIdentity(courseDirectory, chapterCode) {
  const schema = courseSchemas[courseDirectory];
  if (!schema) reject(`課程尚未登記 schema：${courseDirectory ?? "(missing)"}`);
  if (typeof chapterCode !== "string" || !chapterCode) reject("章碼必須是非空字串");
  if (chapterCode !== chapterCode.normalize("NFC")) reject("章碼必須使用 NFC Unicode");
  const match = chapterCode.match(schema.chapterPattern);
  if (!match) reject(`章碼與 ${courseDirectory} 不一致或不是 canonical 正整數編號：${chapterCode}`);
  return Object.freeze({
    courseDirectory,
    chapterCode,
    subject: schema.subject,
    course: schema.course(match),
    idStem: schema.idStem(match),
  });
}

export function expectedDocumentId(identity, audience) {
  if (!identity?.idStem) reject("章節 identity 缺少 idStem");
  if (audience !== "student") reject(`新出版產線只支援 student audience：${audience}`);
  return `${identity.idStem}-${audience}`;
}

export function leadingRegisteredChapterCode(value) {
  if (typeof value !== "string") return undefined;
  return value.match(registeredChapterCodeAtStart)?.[0];
}
