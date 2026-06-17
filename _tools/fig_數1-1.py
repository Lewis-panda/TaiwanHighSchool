# -*- coding: utf-8 -*-
"""產生「數1-1 數與式」的圖，輸出到該章 sources/。
重繪：  .venv/bin/python _tools/fig_數1-1.py
"""

import os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import figlib as F

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CH = os.path.join(ROOT, "數學", "數學一上（必修·第一冊）", "數1-1 數與式")


def fig_number_line():
    """數線：標出整數、有理數（分數、循環小數）、無理數（√2、π），並示意 √2 的幾何位置。"""
    fig, ax = plt.subplots(figsize=(9.4, 3.6))

    x0, x1 = -1.6, 4.2
    # 主數線
    ax.annotate(
        "",
        xy=(x1, 0),
        xytext=(x0, 0),
        arrowprops=dict(arrowstyle="-|>", color=F.INK, lw=1.8),
    )
    ax.annotate(
        "",
        xy=(x0, 0),
        xytext=(x1, 0),
        arrowprops=dict(arrowstyle="-|>", color=F.INK, lw=1.8),
    )

    # 整數刻度
    for n in range(-1, 5):
        ax.plot([n, n], [-0.10, 0.10], color=F.INK, lw=1.4)
        ax.text(n, -0.40, f"${n}$", ha="center", va="center", color=F.INK, fontsize=12)

    sqrt2 = np.sqrt(2)
    pi = np.pi
    # 有理數點（藍）
    rationals = [
        (-0.5, r"$-\frac{1}{2}$"),
        (1.5, r"$\frac{3}{2}$"),
        (2.333333, r"$2.\overline{3}$"),
    ]
    for x, lab in rationals:
        ax.add_patch(Circle((x, 0), 0.055, color=F.BLUE, zorder=6))
        ax.text(x, 0.34, lab, ha="center", va="bottom", color=F.BLUE, fontsize=12.5)
    # 無理數點（紅）
    irrationals = [(sqrt2, r"$\sqrt{2}$"), (pi, r"$\pi$")]
    for x, lab in irrationals:
        ax.add_patch(Circle((x, 0), 0.055, color=F.RED, zorder=6))
        ax.text(x, 0.34, lab, ha="center", va="bottom", color=F.RED, fontsize=13)

    # 以單位正方形對角線「作出」√2：邊長 1 的正方形，對角線長 √2，旋下數線
    # 正方形畫在數線上方一點點，示意對角線長度
    sq_y = 1.05
    ax.plot(
        [0, 1, 1, 0, 0], [sq_y, sq_y, sq_y + 1, sq_y + 1, sq_y], color=F.GREEN, lw=1.6
    )
    ax.plot([0, 1], [sq_y + 1, sq_y], color=F.AMBER, lw=2.0)  # 對角線
    ax.text(0.5, sq_y - 0.22, "邊長 1", ha="center", color=F.GREEN, fontsize=11)
    ax.text(
        0.30,
        sq_y + 0.62,
        "對角線 = $\\sqrt{2}$",
        ha="left",
        color=F.AMBER,
        fontsize=11.5,
    )
    # 虛線箭頭：把對角線長度「轉」到數線上的 √2 處
    ax.annotate(
        "",
        xy=(sqrt2, 0.0),
        xytext=(1.0, sq_y),
        arrowprops=dict(
            arrowstyle="-|>",
            color=F.AMBER,
            lw=1.2,
            ls="--",
            connectionstyle="arc3,rad=-0.35",
        ),
    )

    # 圖例文字
    ax.text(x0 + 0.05, -0.95, "● 有理數", color=F.BLUE, fontsize=12, ha="left")
    ax.text(x0 + 1.55, -0.95, "● 無理數", color=F.RED, fontsize=12, ha="left")
    ax.text(x1 - 0.05, 0.18, "$x$", color=F.INK, fontsize=12, ha="right")

    ax.set_xlim(x0 - 0.2, x1 + 0.2)
    ax.set_ylim(-1.15, 2.35)
    ax.axis("off")
    ax.set_title("數線：每個實數對應數線上唯一一點", fontsize=14)
    F.save_to(fig, CH, "數1-1-數線實數")


def fig_abs_distance():
    """絕對值的幾何意義：|x−a| 為 x 到 a 的距離；並示意 |x−a|<r 的解區間。"""
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(9.0, 4.6))

    # 上：|x − a| = 點 x 到 a 的距離
    for ax in (ax1, ax2):
        ax.set_xlim(-1, 9)
        ax.axis("off")

    def axis(ax, y=0):
        ax.annotate(
            "",
            xy=(9, y),
            xytext=(-1, y),
            arrowprops=dict(arrowstyle="-|>", color=F.INK, lw=1.6),
        )
        for n in range(0, 9):
            ax.plot([n, n], [y - 0.12, y + 0.12], color=F.INK, lw=1.1)
            ax.text(n, y - 0.45, f"${n}$", ha="center", color=F.INK, fontsize=10.5)

    # 上圖
    axis(ax1, 0)
    a, x = 2, 6
    ax1.add_patch(Circle((a, 0), 0.10, color=F.RED, zorder=6))
    ax1.add_patch(Circle((x, 0), 0.10, color=F.BLUE, zorder=6))
    ax1.text(a, 0.50, "$a$", ha="center", color=F.RED, fontsize=13)
    ax1.text(x, 0.50, "$x$", ha="center", color=F.BLUE, fontsize=13)
    ax1.annotate(
        "",
        xy=(x, 1.05),
        xytext=(a, 1.05),
        arrowprops=dict(arrowstyle="<|-|>", color=F.GREEN, lw=2.0),
    )
    ax1.text(
        (a + x) / 2, 1.45, r"$|x-a|=$ 兩點距離", ha="center", color=F.GREEN, fontsize=13
    )
    ax1.set_ylim(-0.8, 2.0)

    # 下圖：|x − a| < r 的解：以 a 為中心、半徑 r 的開區間
    axis(ax2, 0)
    a2, r = 4, 2
    lo, hi = a2 - r, a2 + r
    ax2.plot([lo, hi], [0, 0], color=F.AMBER, lw=5.5, alpha=0.55, zorder=2)
    # 空心端點
    for e in (lo, hi):
        ax2.add_patch(
            Circle((e, 0), 0.13, facecolor="white", edgecolor=F.AMBER, lw=2.2, zorder=6)
        )
    ax2.add_patch(Circle((a2, 0), 0.10, color=F.RED, zorder=6))
    ax2.text(a2, 0.50, "$a$", ha="center", color=F.RED, fontsize=13)
    ax2.annotate(
        "",
        xy=(hi, 1.05),
        xytext=(a2, 1.05),
        arrowprops=dict(arrowstyle="-|>", color=F.INK, lw=1.4),
    )
    ax2.text((a2 + hi) / 2, 1.35, "$r$", ha="center", color=F.INK, fontsize=12)
    ax2.text(
        a2,
        -1.05,
        r"$|x-a|<r \;\Leftrightarrow\; a-r < x < a+r$",
        ha="center",
        color=F.AMBER,
        fontsize=13,
    )
    ax2.set_ylim(-1.4, 1.7)

    ax1.set_title("絕對值＝數線上的距離", fontsize=14)
    fig.tight_layout()
    F.save_to(fig, CH, "數1-1-絕對值距離")


def fig_abs_function():
    """y=|x| 與 y=|x−a| 的 V 形圖。"""
    fig, ax = F.canvas(6.2, 4.6)
    x = np.linspace(-4, 6, 400)
    ax.plot(x, np.abs(x), color=F.BLUE, lw=2.6, label=r"$y=|x|$")
    ax.plot(x, np.abs(x - 2), color=F.RED, lw=2.6, ls="--", label=r"$y=|x-2|$")

    # 過原點座標軸
    ax.axhline(0, color=F.INK, lw=1.3)
    ax.axvline(0, color=F.INK, lw=1.3)

    # 頂點標示
    ax.add_patch(Circle((0, 0), 0.06, color=F.BLUE, zorder=6))
    ax.add_patch(Circle((2, 0), 0.06, color=F.RED, zorder=6))
    ax.text(0.15, -0.55, "頂點 $(0,0)$", color=F.BLUE, fontsize=11, ha="left")
    ax.text(2.15, -0.55, "頂點 $(2,0)$", color=F.RED, fontsize=11, ha="left")

    ax.text(-3.4, 3.6, r"$y=|x|$", color=F.BLUE, fontsize=13)
    ax.text(4.4, 3.6, r"$y=|x-2|$", color=F.RED, fontsize=13, ha="right")

    ax.set_xlim(-4, 6)
    ax.set_ylim(-1.0, 5.0)
    ax.set_xlabel("$x$")
    ax.set_ylabel("$y$")
    ax.set_title("絕對值函數的 V 形圖（平移 $a$ 個單位）", fontsize=13)
    F.clean_grid(ax)
    F.save_to(fig, CH, "數1-1-絕對值函數")


if __name__ == "__main__":
    fig_number_line()
    fig_abs_distance()
    fig_abs_function()
    print("done.")
