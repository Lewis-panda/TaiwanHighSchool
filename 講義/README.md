# 學生講義（PDF）建置規格

把 vault 的筆記，編成**給學生看的順序式 PDF 講義**（XeLaTeX）。這份是建置依據；另一台機器照此產出。

## 0. 工具鏈
- 引擎：**XeLaTeX**（中文用 xeCJK）。
- 安裝（macOS，已有 Homebrew）：
  ```bash
  brew install --cask basictex          # 約100MB，需管理員密碼
  eval "$(/usr/libexec/path_helper)"    # 讓本 shell 找到 /Library/TeX/texbin
  sudo tlmgr update --self
  sudo tlmgr install xecjk tcolorbox     # 其餘相依 tlmgr 會自動補
  ```
  （Linux 用 TeX Live 同理：`tlmgr install xecjk tcolorbox`，字型改成系統有的中文字型。）
- 字型：`preamble.tex` 預設 macOS 的 **Songti TC**（內文）＋**Heiti TC**（標題）。換機器若沒有，改成該機器有的中文字型（如思源宋體/黑體 Noto Serif/Sans CJK TC）。

## 1. 圖（先轉成 PDF，再用 ASCII 檔名）
每章的圖由 `_tools/fig_<章代碼>.py` 生成，**會同時輸出 .svg（給 Obsidian）和 .pdf（給 LaTeX）**到該章 `sources/`。
LaTeX 引圖時，因原檔名是中文＋空白＋括號，請**先複製成 ASCII 檔名**到 `講義/figs/`：
```bash
.venv/bin/python _tools/fig_必物-6.py        # 產生 svg+pdf
S="物理/物理一（必修物理）/必物-6 量子現象/sources"
mkdir -p 講義/figs
cp "$S/必物-6-黑體輻射.pdf"   講義/figs/q-blackbody.pdf
cp "$S/必物-6-振動模式.pdf"   講義/figs/q-modes.pdf
cp "$S/必物-6-光電效應.pdf"   講義/figs/q-photoelectric.pdf
cp "$S/必物-6-雙狹縫累積.pdf" 講義/figs/q-doubleslit.pdf
cp "$S/必物-6-氫原子能階.pdf" 講義/figs/q-levels.pdf
```
`.venv` 不在 repo（見 .gitignore）；換機器先建：`python3 -m venv .venv && .venv/bin/pip install matplotlib numpy`。

## 2. 前言與環境（preamble.tex）
`\input{preamble}` 後可用：
- `\begin{補充框}{標題} … \end{補充框}`：**就地補充新概念**（灰底）。
- `\begin{延伸框}{標題} … \end{延伸框}`：深入／開放延伸（紫色左邊條）。
- `\fig{ASCII檔名}{寬度比例}{底下說明}`：例 `\fig{q-blackbody}{0.78}{圖：黑體輻射與紫外災難。}`

## 3. 內容規則（最重要）
講義 ≠ 筆記。筆記是**非線性**（主筆記＋用 `[[連結]]` 跳出去的 background）；講義必須**線性、順序**。

1. **學生視角**：拿掉所有面向老師的敘述——`教學提示`、`回到課堂`、`板書`、`預期追問`、`一句話講法`等一律刪。`常見迷思`改寫成學生看的「注意：…」。
2. **新概念就地補**：每當出現一個課本沒解釋的名詞/公式（黑體、振動模式、能量均分、$kT$、功函數、$\lambda=h/p$ 的由來、能階為何負…），就把對應 background 筆記的**基礎澄清**內容改寫成學生版，**用 `補充框` 放在它首次出現的正下方**——不要用連結跳走。
3. **深入／開放**：background 的深入題、開放問題（如波函數塌縮詮釋、退相干、電子為何不掉進核）改寫成學生版，放 `延伸框` 附在相關段落後。開放問題要明說「目前無定論」。
4. **不放任何題目或例題**（學生另有練習題）。連含詳解的示範例題也不放。
5. 名詞首次出現附英文，例：光子（photon）。

## 4. 每章一個 .tex
檔名 `講義/<章名>（學生講義）.tex`：
```latex
\documentclass[11pt]{article}
\input{preamble}
\begin{document}
\begin{center}{\sffamily\Huge\bfseries 章名}\\[3pt]
{\sffamily\large 普通高中 物理（必修）・學生講義}\end{center}
\vspace{0.6em}
… 內文 …
\end{document}
```
編譯（在 `講義/` 內，跑兩次）：
```bash
cd 講義
/Library/TeX/texbin/xelatex -interaction=nonstopmode "必物-6 量子現象（學生講義）.tex"
/Library/TeX/texbin/xelatex -interaction=nonstopmode "必物-6 量子現象（學生講義）.tex"
```

---

## 附：必物-6 量子現象 —— 逐節編排地圖
（來源筆記在 `物理/物理一（必修物理）/必物-6 量子現象/`，主筆記＋`background/`。照下面順序線性鋪陳，括號內是要「就地補」或「放延伸框」的 background 來源。）

1. **引言**：三個古典算不對的實驗 → 能量量子化。
2. **黑體輻射與量子論的誕生**
   - 〔補充框〕什麼是黑體（← `什麼是「黑體」…`）
   - 古典失敗＝紫外災難；依序〔補充框〕振動模式、能量均分定理、$kT$（← `為什麼古典理論會預測「紫外災難」…`、`什麼是 kT…`）。插圖 `q-modes`、`q-blackbody`。
   - 普朗克量子假設 $E=h\nu$ 如何化解。
   - 〔延伸框〕普朗克「絕望之舉」（← `為什麼能量要「量子化」…`）
3. **光的粒子性：光電效應**
   - 古典波動說的矛盾 → 愛因斯坦光量子 $K_{\max}=h\nu-W$。
   - 〔補充框〕什麼是功函數（← `什麼是功函數…`）。插圖 `q-photoelectric`。生活應用。
4. **物質的波動性：德布羅意波** $\lambda=h/p$
   - 〔補充框〕這條式子的由來（← `德布羅意憑什麼說…由來`）
   - 電子顯微鏡；宏觀為何測不到（數量級）。
   - 〔延伸框〕退相干與大分子干涉前沿（← `為什麼我們感覺不到自己的物質波…`）
5. **波粒二象性與雙狹縫**（插圖 `q-doubleslit`）
   - 〔補充框〕什麼是疊加、疊加≠不知道（← `什麼是量子「疊加」…`）
   - 互補原理。
   - 〔延伸框・開放〕觀測與波函數塌縮、各種詮釋至今無共識（← `「波函數塌縮」是真的嗎…`）
6. **原子光譜與能階**（插圖 `q-levels`）
   - 線狀光譜之謎 → 玻爾能階 $E_n=-13.6/n^2$、躍遷 $h\nu=E_i-E_f$。
   - 〔補充框〕能量為何是負的＝束縛態（← `為什麼能階的能量是負的…`）
   - 古典原子崩潰 → 量子化拯救。
   - 〔延伸框〕為什麼電子不會掉進原子核（含不確定性原理）（← `為什麼電子不會掉進原子核…`、`什麼是「不確定性原理」…`）
7. **重點整理**：公式表一頁（無題目）。
