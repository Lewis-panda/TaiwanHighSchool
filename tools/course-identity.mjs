const courseSchemas = Object.freeze({
  必修數學: Object.freeze({
    chapterPattern: /^數([12])-([1-9]\d*)$/u,
    subject: "數學",
    course(match) {
      return `普通高中數學 第${match[1] === "1" ? "一" : "二"}冊`;
    },
    idStem(match) {
      return `math-required-${match[1]}-${match[2]}`;
    },
  }),
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
  數學B: Object.freeze({
    chapterPattern: /^數B([34])-([1-9]\d*)$/u,
    subject: "數學",
    course(match) {
      return match[1] === "3" ? "普通高中數學B 第三冊" : "普通高中數學B 第四冊";
    },
    idStem(match) {
      return `math-b${match[1]}-${match[2]}`;
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
  必修化學: Object.freeze({
    chapterPattern: /^必化-([1-9]\d*)$/u,
    subject: "化學",
    course() {
      return "普通高中必修化學";
    },
    idStem(match) {
      return `chemistry-required-${match[1]}`;
    },
  }),
  選修化學I: Object.freeze({
    chapterPattern: /^選化I-([1-9]\d*)$/u,
    subject: "化學",
    course() {
      return "普通高中選修化學 I";
    },
    idStem(match) {
      return `chemistry-i1-${match[1]}`;
    },
  }),
  選修化學II: Object.freeze({
    chapterPattern: /^選化II-([1-9]\d*)$/u,
    subject: "化學",
    course() {
      return "普通高中選修化學 II";
    },
    idStem(match) {
      return `chemistry-i2-${match[1]}`;
    },
  }),
  選修化學III: Object.freeze({
    chapterPattern: /^選化III-([1-9]\d*)$/u,
    subject: "化學",
    course() {
      return "普通高中選修化學 III";
    },
    idStem(match) {
      return `chemistry-i3-${match[1]}`;
    },
  }),
  選修化學IV: Object.freeze({
    chapterPattern: /^選化IV-([1-9]\d*)$/u,
    subject: "化學",
    course() {
      return "普通高中選修化學 IV";
    },
    idStem(match) {
      return `chemistry-i4-${match[1]}`;
    },
  }),
  選修化學V: Object.freeze({
    chapterPattern: /^選化V-([1-9]\d*)$/u,
    subject: "化學",
    course() {
      return "普通高中選修化學 V";
    },
    idStem(match) {
      return `chemistry-i5-${match[1]}`;
    },
  }),
});

const registeredChapterCodeAtStart = /^(?:數[12]-\d+|數A[34]-\d+|數B[34]-\d+|選物I-\d+|必物-\d+|必化-\d+|選化(?:III|II|IV|I|V)-\d+)/u;

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
