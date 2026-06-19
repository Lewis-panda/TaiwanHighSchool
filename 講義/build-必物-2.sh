#!/usr/bin/env bash
# 編譯「必物-2 物體的運動」學生講義 PDF。
# 需 XeLaTeX（xeCJK+tcolorbox）與 .venv（matplotlib）。
# 用法（在 repo 根目錄）：bash 講義/build-必物-2.sh
set -e
cd "$(dirname "$0")/.."          # repo 根目錄

# 1) 生成圖（svg 給 Obsidian、pdf 給 LaTeX）
.venv/bin/python _tools/fig_必物-2.py

# 2) 複製成 ASCII 檔名到 講義/figs/（preamble 的 \graphicspath 指這裡）
S="物理/物理一（必修物理）/必物-2 物體的運動/sources"
mkdir -p 講義/figs
cp "$S/必物-2-運動圖形.pdf"     講義/figs/m2-motion.pdf
cp "$S/必物-2-自由體圖.pdf"     講義/figs/m2-fbd.pdf
cp "$S/必物-2-斜面分解.pdf"     講義/figs/m2-incline.pdf
cp "$S/必物-2-克卜勒等面積.pdf" 講義/figs/m2-kepler.pdf

# 3) 編譯兩次（版面/參照穩定）
cd 講義
xelatex -interaction=nonstopmode -halt-on-error "必物-2 物體的運動（學生講義）.tex"
xelatex -interaction=nonstopmode -halt-on-error "必物-2 物體的運動（學生講義）.tex"
echo "OK -> 講義/必物-2 物體的運動（學生講義）.pdf"
