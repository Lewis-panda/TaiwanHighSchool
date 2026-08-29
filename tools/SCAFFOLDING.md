# 新章學生單冊骨架工作流

這個工具只建立符合 [`content/AUTHORING.md`](../content/AUTHORING.md) 的章節結構與待辦欄位，不撰寫教材內容、不修改 `publishing/sets.json`，也不發布 PDF。

`create` 預設只做 dry-run。建議仍明寫 `--dry-run` 檢查參數與預計 registry document；章名只填主題，不重複章碼：

```bash
npm run scaffold:chapter -- \
  --course <已登記課程> \
  --chapter-code '<核准的章碼>' \
  --title '<不含章碼的章名>' \
  --updated YYYY-MM-DD \
  --dry-run
```

確認要建立後，改用互斥的 `--write-approved`：

```bash
npm run scaffold:chapter -- \
  --course <已登記課程> \
  --chapter-code '<核准的章碼>' \
  --title '<不含章碼的章名>' \
  --updated YYYY-MM-DD \
  --write-approved
```

`--dry-run` 與 `--write-approved` 不得同時使用；沒有 `--write-approved` 一律不寫檔。成功寫入也只代表建立下列空白骨架：

```text
content/<課程>/<章碼>/
├── 學生講義.md
├── assets/
└── 編輯判定.md
```

學生範本要求作者交代問題、原理、推導條件、實際用途與模型限制。這些內容直接寫成有意義的標題與正文，不在成品印出 `Why → Why → Why`、`起點檢查`、`30 秒檢核` 或 `停止線` 等閱讀指令。

工具拒絕覆寫既有目錄、symlink 課程路徑、未登記課程／錯配章碼及未被 Git 忽略的 `編輯判定.md`。骨架含 `TODO(SCAFFOLD):`，此時可用草稿模式檢查，但不可登記發布：

```bash
npm run lint:chapter -- \
  --course <課程> \
  --chapter-code <章碼> \
  --allow-todos
```

## Fresh clone 的私有檔初始化

`content/**/編輯判定.md` 依設計受 Git 忽略。對已有合法學生稿、但缺少本機編輯檔的章節執行：

```bash
npm run init-private:chapter -- \
  --course <課程> \
  --chapter-code <章碼>
```

`init-private` 會從 `學生講義.md` 讀取章名與更新日期，驗證章根、frontmatter、最低結構、SVG 閉包與 Git 隱私邊界後，以不可覆寫模式補建本機範本並再跑正式 lint。它會拒絕：

- 已存在的 `編輯判定.md`，不論一般檔或 symlink。
- 未登記課程、錯配章碼、symlink 目錄或不符作者規格的學生稿。
- 沒有明確忽略私有檔，或會把學生稿／公開資產一併忽略的 Git 規則。

這只能新建空白本機記錄，不能還原從未納入 Git 的舊頁碼、路徑或編輯決策。

## Optional legacy 教師檔

既有章若仍有 `教師備課指南.md`，lint 容許它原地存在，並只做安全文字與 SVG 引用檢查，讓舊資料不必為遷移而刪除。它不是必需檔：

- scaffold 不建立，init-private／lint 不要求。
- lint 回傳的 registry 候選永遠只有 student。
- `publication.mjs` 對 review 與 published set 都拒絕 teacher document。
- 標準 `build-handout.mjs` 只接受 `學生講義.md`。

## 完稿 lint 與 registry document

移除全部 `TODO(SCAFFOLD):` 後執行：

```bash
npm run lint:chapter -- --course <課程> --chapter-code <章碼>
```

正式 lint 會檢查：

- 學生稿恰有九個 frontmatter key，章碼、課程、科目、日期與 `output_slug` 一致；registry `id` 由課程與 canonical 正整數章碼衍生，結尾固定為 `-student`。
- 恰有一個與 frontmatter `title` 相同的可見 H1；Setext、blockquote 或 raw HTML 不得藏入第二個 H1。
- 本章問題、原理／因果、真實用途／應用邊界、練習、代表題、完整詳解與核心整理訊號存在；標語式標題會被拒絕。
- `assets/` 只含學生稿或 optional legacy 教師稿實際引用的自足 SVG；registry 只列學生稿精確使用的資產閉包。
- `編輯判定.md` 受 Git 忽略且永不出現在 registry。

lint 成功後，把它輸出的唯一 document 加入核准的 student-only review set，再跑權威檢查：

```bash
node tools/publication.mjs preflight --set <set-id>
```

每份 document 必須恰含 `id`、`audience`、`source`、`slug`、`assets`：`audience` 固定 `student`，`source` 固定為該章的 `學生講義.md`，slug 以章碼開頭並以 `-學生講義` 結尾。詳見 [`publishing/SCHEMA.md`](../publishing/SCHEMA.md)。

工具測試：

```bash
npm run test:scaffold
```
