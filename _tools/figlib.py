"""
figlib — 全庫共用繪圖樣式與工具。
所有章節的繪圖腳本都 import 這支，確保風格一致。

輸出：SVG（向量、Obsidian 原生支援、放大不糊），文字轉為路徑（svg.fonttype='path'）
故任何裝置都能正確顯示中文，不依賴觀看端字型。

用法：
    import figlib as F
    fig, ax = F.canvas(6, 4)          # 一般作圖
    ax.plot(...)
    F.save(fig, __file__, "必物-2-運動圖形")   # 存到對應章節的 sources/
"""
import os, sys, warnings
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib.patches import FancyArrowPatch, Rectangle, Polygon, Arc, Circle, Ellipse, Wedge

# ---- 中文字型 ----
_FONT_CANDIDATES = [
    "/System/Library/Fonts/STHeiti Medium.ttc",
    "/System/Library/Fonts/Hiragino Sans GB.ttc",
    "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
    "/Library/Fonts/Arial Unicode.ttf",
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
INK   = "#222831"   # 主線、文字
GRID  = "#d8dde3"   # 格線
BLUE  = "#1f6feb"   # 向量 / 正向力 / 速度
RED   = "#d1242f"   # 重力 / 反向
GREEN = "#1a7f37"   # 張力 / 輔助
AMBER = "#bf8700"   # 摩擦力 / 強調
PURPLE= "#8250df"   # 第三量
FILL  = "#1f6feb"   # 面積填色（搭配低透明度）

plt.rcParams.update({
    "font.family": CJK,
    "mathtext.fontset": "cm",
    "axes.unicode_minus": False,
    "svg.fonttype": "path",      # 文字→向量路徑，跨裝置可靠
    "figure.dpi": 120,
    "savefig.dpi": 120,
    "savefig.bbox": "tight",
    "savefig.transparent": False,
    "axes.edgecolor": INK,
    "axes.linewidth": 1.1,
    "axes.titlesize": 14,
    "axes.labelsize": 12,
    "xtick.color": INK, "ytick.color": INK,
    "text.color": INK, "axes.labelcolor": INK,
    "font.size": 12,
})


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
    a = FancyArrowPatch(xy_from, xy_to, arrowstyle="-|>", mutation_scale=mutation,
                        lw=lw, color=color, linestyle=ls, alpha=alpha, zorder=z,
                        shrinkA=0, shrinkB=0)
    ax.add_patch(a)
    return a


def label(ax, xy, text, color=INK, fs=13, ha="center", va="center", math=False, z=6):
    ax.text(xy[0], xy[1], text, color=color, fontsize=fs, ha=ha, va=va, zorder=z)


def angle_arc(ax, center, r, a1, a2, color=INK, text=None, lw=1.4):
    ax.add_patch(Arc(center, 2*r, 2*r, angle=0, theta1=a1, theta2=a2, color=color, lw=lw))
    if text:
        import numpy as np
        am = np.deg2rad((a1 + a2) / 2)
        ax.text(center[0] + 1.5*r*np.cos(am), center[1] + 1.5*r*np.sin(am),
                text, color=color, fontsize=12, ha="center", va="center")


def clean_grid(ax):
    ax.grid(True, color=GRID, lw=0.9)
    ax.set_axisbelow(True)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)


def save(fig, script_file, name):
    """存到 <該腳本對應章節資料夾>/sources/<name>.svg。
    繪圖腳本放在 _tools/，需傳入該圖所屬章節資料夾；用 save_to 指定。"""
    raise RuntimeError("請改用 save_to(fig, chapter_dir, name)")


def save_to(fig, chapter_dir, name):
    out = os.path.join(chapter_dir, "sources")
    os.makedirs(out, exist_ok=True)
    path = os.path.join(out, name + ".svg")
    fig.savefig(path)
    plt.close(fig)
    print("wrote", path)
    return path


if __name__ == "__main__":
    print("CJK font resolved to:", CJK)
