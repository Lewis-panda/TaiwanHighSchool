# Bundled fonts

公開 HTML／PDF 不依賴作者電腦的系統字型。產線只允許下列三個內附 family；不可變上游 commit、來源／輸出 SHA-256 與重建指令另見 `provenance.json`。

- `NotoSansTC-Regular.ttf`、`NotoSansTC-Bold.ttf`：以 Google Fonts 官方 `ofl/notosanstc/NotoSansTC[wght].ttf` 為來源，分別固定在 weight 400、700 的靜態 TrueType 實例。使用 HarfBuzz 14.2.0 的 `hb-subset --keep-everything --variations=wght=<weight>` 產生；SHA-256 分別為 `1236fcc65f1ab85f75f98c38b61531de1bca5efb0cc20610f961cecd03af2071`、`8fb290ad6f55d99296d3a2b289bfc7bf45e9febec178e5d65e9caa5f5e783964`，授權見 `NotoSansTC-OFL.txt`。採靜態 TrueType 是為了讓 Chromium 產生可搜尋的 CID TrueType 字型，而不是 Type 3 字形。
- `NotoSansMath-Regular.ttf`：數學與頁碼用字型，授權見 `OFL.txt`。
- `NotoSans-Regular.ttf`：MathML 符號 fallback（目前主要補 `U+203E OVERLINE`），來源為 Noto Fonts 官方 repository 的 `hinted/ttf/NotoSans/NotoSans-Regular.ttf`；SHA-256 為 `b85c38ecea8a7cfb39c24e395a4007474fa5a4fc864f6ee33309eb4948d232d5`，授權同為 OFL 1.1。

更換任一字型都會改變換行、分頁及 PDF hash，必須重新 `release`、`verify`、`review:render`，並逐頁檢視彩色與灰階聯絡表。

`hb-subset` 只用於重建兩個 TC 靜態資產，不是一般作者執行 doctor、build 或 release 的依賴。這兩檔沿用上游 `NotoSansTC-Thin` 內部 family 名稱，但 OS/2 weight、CSS descriptor 與實際輪廓分別固定為 400、700；`pdffonts` 顯示 Thin 不代表正文使用細字重。
