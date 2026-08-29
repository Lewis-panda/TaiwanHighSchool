"""
figlib — 全庫共用繪圖樣式與工具。
所有章節的繪圖腳本都 import 這支，確保風格一致。

LEGACY 注意：save_to() 的預設仍是舊 Obsidian `sources/` + companion PDF，
只為既有腳本相容而保留。`content/` 公開新章必須依 content/AUTHORING.md
明確指定 output_subdir="assets", write_pdf=False；不可依賴預設值。

輸出：SVG（向量、放大不糊），文字轉為路徑（svg.fonttype='path'）
故任何裝置都能正確顯示中文，不依賴觀看端字型。

用法：
    import figlib as F
    fig, ax = F.canvas(6, 4)          # 一般作圖
    ax.plot(...)
    # 舊樹維護：預設 sources/ + PDF
    F.save_to(fig, chapter_dir, "必物-2-運動圖形")

    # content/ 公開新章：必須明示 assets/ + SVG-only
    F.save_to(fig, chapter_dir, "章碼-圖名", output_subdir="assets", write_pdf=False)
"""

import os, sys, warnings
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib.patches import (
    FancyArrowPatch,
    Rectangle,
    Polygon,
    Arc,
    Circle,
    Ellipse,
    Wedge,
)

# ---- 中文字型 ----
_FONT_CANDIDATES = [
    os.path.expanduser("~/Library/Fonts/NotoSansCJKtc-Regular.otf"),
    "/System/Library/Fonts/STHeiti Medium.ttc",
    "/System/Library/Fonts/Hiragino Sans GB.ttc",
    "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
    "/Library/Fonts/Arial Unicode.ttf",
    # Linux（TeX Live / Debian）：思源黑體，無 macOS 字型時的回退
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
]
CJK = "sans-serif"
for _p in _FONT_CANDIDATES:
    if os.path.exists(_p):
        try:
            fm.fontManager.addfont(_p)
            CJK = fm.FontProperties(fname=_p).get_name()
            break
        except Exception:
            continue

# ---- 配色（統一視覺語言）----
INK = "#222831"  # 主線、文字
GRID = "#d8dde3"  # 格線
BLUE = "#1f6feb"  # 向量 / 正向力 / 速度
RED = "#d1242f"  # 重力 / 反向
GREEN = "#1a7f37"  # 張力 / 輔助
AMBER = "#bf8700"  # 摩擦力 / 強調
PURPLE = "#8250df"  # 第三量
FILL = "#1f6feb"  # 面積填色（搭配低透明度）

plt.rcParams.update(
    {
        "font.family": CJK,
        "mathtext.fontset": "cm",
        "axes.unicode_minus": False,
        "svg.fonttype": "path",  # 文字→向量路徑，跨裝置可靠
        "svg.hashsalt": "HighSchooContent-v1",  # 固定 SVG element id，減少無意義 hash churn
        "figure.dpi": 120,
        "savefig.dpi": 120,
        "savefig.bbox": "tight",
        "savefig.transparent": False,
        "axes.edgecolor": INK,
        "axes.linewidth": 1.1,
        "axes.titlesize": 14,
        "axes.labelsize": 12,
        "xtick.color": INK,
        "ytick.color": INK,
        "text.color": INK,
        "axes.labelcolor": INK,
        "font.size": 12,
    }
)


def canvas(w=6, h=4, equal=False):
    fig, ax = plt.subplots(figsize=(w, h))
    if equal:
        ax.set_aspect("equal")
    return fig, ax


def schematic(w=6, h=4):
    """無座標軸的示意圖畫布。"""
    fig, ax = plt.subplots(figsize=(w, h))
    ax.set_aspect("equal")
    ax.axis("off")
    return fig, ax


def arrow(ax, xy_from, xy_to, color=INK, lw=2.4, ls="-", mutation=18, alpha=1.0, z=5):
    """畫一支實心箭頭（向量／力）。"""
    a = FancyArrowPatch(
        xy_from,
        xy_to,
        arrowstyle="-|>",
        mutation_scale=mutation,
        lw=lw,
        color=color,
        linestyle=ls,
        alpha=alpha,
        zorder=z,
        shrinkA=0,
        shrinkB=0,
    )
    ax.add_patch(a)
    return a


def label(ax, xy, text, color=INK, fs=13, ha="center", va="center", math=False, z=6):
    ax.text(xy[0], xy[1], text, color=color, fontsize=fs, ha=ha, va=va, zorder=z)


def angle_arc(ax, center, r, a1, a2, color=INK, text=None, lw=1.4):
    ax.add_patch(
        Arc(center, 2 * r, 2 * r, angle=0, theta1=a1, theta2=a2, color=color, lw=lw)
    )
    if text:
        import numpy as np

        am = np.deg2rad((a1 + a2) / 2)
        ax.text(
            center[0] + 1.5 * r * np.cos(am),
            center[1] + 1.5 * r * np.sin(am),
            text,
            color=color,
            fontsize=12,
            ha="center",
            va="center",
        )


def clean_grid(ax):
    ax.grid(True, color=GRID, lw=0.9)
    ax.set_axisbelow(True)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)


def save(fig, script_file, name):
    """存到 <該腳本對應章節資料夾>/sources/<name>.svg。
    繪圖腳本放在 _tools/，需傳入該圖所屬章節資料夾；用 save_to 指定。"""
    raise RuntimeError("請改用 save_to(fig, chapter_dir, name)")


def save_to(fig, chapter_dir, name, *, output_subdir="sources", write_pdf=True):
    """輸出章節圖。

    舊教材腳本預設維持 ``sources/`` 與 SVG/PDF 雙輸出；新的 HTML/PDF
    產線可指定 ``output_subdir="assets"``、``write_pdf=False``，讓公開
    Markdown 只攜帶可內嵌的 SVG。
    """
    if (
        not isinstance(output_subdir, str)
        or not output_subdir
        or output_subdir in (".", "..")
        or os.path.basename(output_subdir) != output_subdir
    ):
        raise ValueError("output_subdir 必須是單一安全目錄名稱")
    if (
        not isinstance(name, str)
        or not name
        or name in (".", "..")
        or os.path.basename(name) != name
        or "\x00" in name
    ):
        raise ValueError("name 必須是單一安全檔名且不含副檔名")
    if not isinstance(write_pdf, bool):
        raise TypeError("write_pdf 必須是 bool")
    out = os.path.join(chapter_dir, output_subdir)
    if os.path.lexists(out) and os.path.islink(out):
        raise RuntimeError("拒絕寫入 symlink 圖片目錄")
    os.makedirs(out, exist_ok=True)
    if os.path.dirname(os.path.realpath(out)) != os.path.realpath(chapter_dir):
        raise RuntimeError("圖片目錄必須是章節目錄的直接子目錄")
    path = os.path.join(out, name + ".svg")
    if os.path.lexists(path) and os.path.islink(path):
        raise RuntimeError("拒絕覆寫 symlink SVG")
    fig.savefig(path, metadata={"Date": None})
    # Matplotlib 的 SVG path 會在許多換行前留下空白；它不影響渲染，
    # 卻會讓 git diff --check 產生數千筆雜訊。
    with open(path, encoding="utf-8") as source:
        svg = source.read()
    cleaned_svg = "\n".join(line.rstrip() for line in svg.splitlines()) + "\n"
    with open(path, "w", encoding="utf-8", newline="\n") as target:
        target.write(cleaned_svg)
    extra = ""
    if write_pdf:
        pdf_path = os.path.join(out, name + ".pdf")
        if os.path.lexists(pdf_path) and os.path.islink(pdf_path):
            raise RuntimeError("拒絕覆寫 symlink PDF")
        fig.savefig(pdf_path)
        extra = " (+pdf)"
    plt.close(fig)
    print("wrote", path + extra)
    return path


if __name__ == "__main__":
    print("CJK font resolved to:", CJK)
