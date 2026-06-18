# -*- coding: utf-8 -*-
"""產生「數A3-2 指數與對數函數」的圖，輸出到該章 sources/。
重繪：  .venv/bin/python _tools/fig_數A3-2.py

本章為函數圖：F.canvas() + ax.plot() + F.clean_grid(ax)，座標軸過原點。
注意：mathtext 不支援 \\dfrac/\\tfrac（用 \\frac）；圖內中文勿放進 $...$。
"""

import os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import figlib as F

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CH = os.path.join(ROOT, "數學", "數學二上（數學A·第三冊）", "數A3-2 指數與對數函數")


def _axes_through_origin(ax, xlim, ylim, xlabel="$x$", ylabel="$y$"):
    """畫過原點的十字座標軸（帶箭頭），隱藏外框，淡格線。"""
    ax.axhline(0, color=F.GRID, lw=0.9, zorder=0)
    ax.axvline(0, color=F.GRID, lw=0.9, zorder=0)
    ax.annotate(
        "",
        xy=(xlim[1], 0),
        xytext=(xlim[0], 0),
        arrowprops=dict(arrowstyle="-|>", color=F.INK, lw=1.4),
    )
    ax.annotate(
        "",
        xy=(0, ylim[1]),
        xytext=(0, ylim[0]),
        arrowprops=dict(arrowstyle="-|>", color=F.INK, lw=1.4),
    )
    ax.text(
        xlim[1] - 0.12,
        -0.20 * (ylim[1] - ylim[0]) / 6,
        xlabel,
        color=F.INK,
        fontsize=12,
        ha="right",
        va="top",
    )
    ax.text(
        0.06 * (xlim[1] - xlim[0]) / 6,
        ylim[1] - 0.10,
        ylabel,
        color=F.INK,
        fontsize=12,
        ha="left",
        va="top",
    )
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.axis("off")


# ---------------------------------------------------------------------------
def fig_exponential():
    """y = a^x 的兩種樣貌：a>1 遞增、0<a<1 遞減，皆過 (0,1)、漸近 x 軸。"""
    fig, ax = F.canvas(6.6, 5.4)
    xlim, ylim = (-3.2, 3.2), (-0.8, 6.0)
    _axes_through_origin(ax, xlim, ylim)

    x = np.linspace(-3.1, 3.1, 400)
    # a>1：遞增（a=2）
    ax.plot(x, 2.0**x, color=F.BLUE, lw=2.6, zorder=4)
    # 0<a<1：遞減（a=1/2），等於把 a=2 左右翻轉
    ax.plot(x, (0.5) ** x, color=F.RED, lw=2.6, zorder=4)

    # 共同點 (0,1)
    ax.add_patch(Circle((0, 1), 0.10, color=F.INK, zorder=6))
    ax.text(0.18, 1.32, "$(0,\\,1)$", color=F.INK, fontsize=12, ha="left")

    # 漸近線提示（x 軸）
    ax.text(-3.0, 0.28, "漸近線 y = 0", color="#6b7280", fontsize=11, ha="left")

    # 曲線標籤
    ax.text(2.25, 5.4, "$y=2^{x}$", color=F.BLUE, fontsize=14, ha="center")
    ax.text(
        -2.55,
        5.4,
        "$y=\\left(\\frac{1}{2}\\right)^{x}$",
        color=F.RED,
        fontsize=14,
        ha="center",
    )
    ax.text(2.55, 0.62, "a > 1 遞增", color=F.BLUE, fontsize=12, ha="center")
    ax.text(-2.55, 0.62, "0 < a < 1 遞減", color=F.RED, fontsize=12, ha="center")

    ax.set_title("指數函數 $y=a^{x}$ 的兩種樣貌", fontsize=14)
    F.save_to(fig, CH, "數A3-2-指數函數")


# ---------------------------------------------------------------------------
def fig_logarithm():
    """y = log_a x 兩種底，且與 y = a^x 對 y=x 對稱。"""
    fig, ax = F.canvas(6.8, 6.4)
    L = 5.2
    xlim, ylim = (-1.6, L), (-1.6, L)
    _axes_through_origin(ax, xlim, ylim)

    # 對稱軸 y = x
    ax.plot(
        [-1.4, L - 0.2], [-1.4, L - 0.2], color="#9aa0a6", lw=1.4, ls="--", zorder=1
    )
    ax.text(4.2, 4.55, "$y=x$", color="#9aa0a6", fontsize=12, ha="left")

    # 指數 y = 2^x（淡藍）與其反函數 y = log_2 x（藍）
    xe = np.linspace(-1.5, 2.35, 300)
    ax.plot(xe, 2.0**xe, color=F.BLUE, lw=1.8, ls=":", alpha=0.7, zorder=3)
    ax.text(2.05, 4.7, "$y=2^{x}$", color=F.BLUE, fontsize=12, ha="left")

    xl = np.linspace(0.04, L - 0.1, 400)
    ax.plot(xl, np.log(xl) / np.log(2.0), color=F.BLUE, lw=2.6, zorder=4)
    ax.text(4.5, 1.55, "$y=\\log_{2}x$", color=F.BLUE, fontsize=13, ha="left")

    # 0<a<1：y = log_{1/2} x（紅，遞減）
    ax.plot(xl, np.log(xl) / np.log(0.5), color=F.RED, lw=2.6, zorder=4)
    ax.text(4.5, -1.15, "$y=\\log_{1/2}x$", color=F.RED, fontsize=13, ha="left")

    # 共同點 (1,0)
    ax.add_patch(Circle((1, 0), 0.10, color=F.INK, zorder=6))
    ax.text(1.05, -0.42, "$(1,\\,0)$", color=F.INK, fontsize=12, ha="left")

    ax.text(
        -1.45,
        4.9,
        "對 y = x 對稱（互為反函數）",
        color="#444",
        fontsize=11.5,
        ha="left",
    )

    ax.set_title("對數函數 $y=\\log_{a}x$，與 $y=a^{x}$ 對 $y=x$ 對稱", fontsize=13.5)
    F.save_to(fig, CH, "數A3-2-對數函數")


# ---------------------------------------------------------------------------
def fig_growth_decay():
    """左：指數成長（複利）；右：指數衰退（半衰期）。"""
    fig, axes = plt.subplots(1, 2, figsize=(11.6, 4.6))

    # --- 左：複利成長 A = P(1+r)^t ---
    ax = axes[0]
    t = np.linspace(0, 30, 300)
    P, r = 1.0, 0.06
    ax.plot(t, P * (1 + r) ** t, color=F.BLUE, lw=2.6, zorder=4)
    # 對照線性成長（單利）
    ax.plot(t, P * (1 + r * t), color="#9aa0a6", lw=1.8, ls="--", zorder=3)
    ax.text(
        20.5,
        1.0 * (1 + r * 20.5) + 0.15,
        "單利（線性）",
        color="#6b7280",
        fontsize=11,
        ha="center",
    )
    ax.text(22, 5.0, "複利（指數）", color=F.BLUE, fontsize=12.5, ha="center")
    ax.text(14.0, 1.2, "$A=P(1+r)^{t}$", color=F.BLUE, fontsize=13, ha="center")
    ax.add_patch(Circle((0, 1), 0.18, color=F.INK, zorder=6))
    ax.set_xlabel("時間 t（年）", fontsize=11.5)
    ax.set_ylabel("本利和 A", fontsize=11.5)
    ax.set_xlim(0, 30)
    ax.set_ylim(0, 6.2)
    F.clean_grid(ax)
    ax.set_title("按比例成長：複利", fontsize=13, color=F.BLUE)

    # --- 右：半衰期衰退 N = N0 (1/2)^(t/T) ---
    ax = axes[1]
    T = 1.0  # 半衰期
    t2 = np.linspace(0, 5, 300)
    N0 = 1.0
    ax.plot(t2, N0 * (0.5) ** (t2 / T), color=F.RED, lw=2.6, zorder=4)
    # 標出每過一個半衰期剩一半
    for k in range(0, 5):
        y = N0 * 0.5**k
        ax.plot([k, k], [0, y], color="#9aa0a6", lw=1.0, ls=":", zorder=2)
        ax.plot([0, k], [y, y], color="#9aa0a6", lw=1.0, ls=":", zorder=2)
        ax.add_patch(Circle((k, y), 0.05, color=F.RED, zorder=6))
    ax.text(
        2.2, 0.62, "每過一個半衰期\n數量減半", color=F.RED, fontsize=11.5, ha="left"
    )
    ax.text(
        2.7,
        0.18,
        "$N=N_{0}\\left(\\frac{1}{2}\\right)^{t/T}$",
        color=F.RED,
        fontsize=13,
        ha="center",
    )
    ax.set_xlabel("時間 t（單位：半衰期 T）", fontsize=11.5)
    ax.set_ylabel("剩餘量 N", fontsize=11.5)
    ax.set_xlim(0, 5)
    ax.set_ylim(0, 1.08)
    F.clean_grid(ax)
    ax.set_title("按比例衰退：半衰期", fontsize=13, color=F.RED)

    fig.suptitle("指數模型：成長（左）與衰退（右）", fontsize=14, y=1.02)
    fig.tight_layout()
    F.save_to(fig, CH, "數A3-2-成長衰退")


# ---------------------------------------------------------------------------
def fig_log_scale():
    """對數尺度的威力：把橫跨多個數量級的量壓進一張圖（pH / 芮氏 / 分貝意象）。"""
    fig, axes = plt.subplots(1, 2, figsize=(11.6, 4.4))

    # 左：線性 y 軸放不下指數成長
    ax = axes[0]
    x = np.linspace(0, 7, 200)
    ax.plot(x, 10.0**x, color=F.PURPLE, lw=2.6)
    ax.set_xlabel("x", fontsize=11.5)
    ax.set_ylabel("$y=10^{x}$（線性軸）", fontsize=11.5)
    ax.set_xlim(0, 7)
    ax.set_ylim(0, 1.05e7)
    F.clean_grid(ax)
    ax.set_title("線性軸：小的全被壓在底部看不見", fontsize=12.5)

    # 右：同資料改用對數 y 軸 → 變一條直線
    ax = axes[1]
    ax.plot(x, 10.0**x, color=F.PURPLE, lw=2.6)
    ax.set_yscale("log")
    ax.set_xlabel("x", fontsize=11.5)
    ax.set_ylabel("$y=10^{x}$（對數軸）", fontsize=11.5)
    ax.set_xlim(0, 7)
    ax.set_ylim(1, 1e7)
    ax.grid(True, which="both", color=F.GRID, lw=0.8)
    ax.set_axisbelow(True)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.text(
        1.0, 1e5, "取 log 後\n成等差（直線）", color=F.PURPLE, fontsize=11.5, ha="left"
    )
    ax.set_title("對數軸：每格 ×10，跨數量級也看得清", fontsize=12.5)

    fig.suptitle("對數尺度：為什麼 pH、芮氏規模、分貝都用對數", fontsize=14, y=1.02)
    fig.tight_layout()
    F.save_to(fig, CH, "數A3-2-對數尺度")


# ---------------------------------------------------------------------------
def fig_inequality_flip():
    """底數 0<a<1 時，遞減函數讓不等號反向的圖解。
    左：指數不等式——自變數 f<g，但 a^f > a^g。
    右：對數不等式——真數 A<B，但 log_a A > log_a B。
    """
    fig, axes = plt.subplots(1, 2, figsize=(11.6, 4.9))

    # --- 左：指數 y=(1/2)^x 遞減 → a^f > a^g 雖然 f<g ---
    ax = axes[0]
    x = np.linspace(-0.3, 3.3, 300)
    y = (0.5) ** x
    ax.plot(x, y, color=F.RED, lw=2.6, zorder=4)

    xf, xg = 1.0, 2.5  # f < g
    yf, yg = 0.5**xf, 0.5**xg
    # 對應的投影虛線
    for xv, yv in ((xf, yf), (xg, yg)):
        ax.plot([xv, xv], [0, yv], color="#9aa0a6", lw=1.0, ls=":", zorder=2)
        ax.plot([0, xv], [yv, yv], color="#9aa0a6", lw=1.0, ls=":", zorder=2)
        ax.plot(xv, yv, marker="o", ms=7, color=F.RED, zorder=6)

    ax.text(xf, -0.075, "f", color=F.INK, fontsize=13, ha="center", va="top")
    ax.text(xg, -0.075, "g", color=F.INK, fontsize=13, ha="center", va="top")
    ax.text(2.95, 0.40, "f < g", color=F.INK, fontsize=12.5, ha="left")
    ax.text(-0.12, yf, "$a^{f}$", color=F.RED, fontsize=13, ha="right", va="center")
    ax.text(-0.12, yg, "$a^{g}$", color=F.RED, fontsize=13, ha="right", va="center")
    # 反向箭頭：函數值大小相反
    ax.annotate(
        "",
        xy=(-0.05, yf - 0.02),
        xytext=(-0.05, yg + 0.02),
        arrowprops=dict(arrowstyle="-|>", color=F.RED, lw=1.6),
    )
    ax.text(1.55, 0.78, "$a^{f} > a^{g}$（反向）", color=F.RED, fontsize=13, ha="left")
    ax.text(2.15, 0.93, "$y=a^{x},\\ 0<a<1$", color=F.RED, fontsize=12, ha="center")
    ax.set_xlim(-0.55, 3.4)
    ax.set_ylim(0, 1.06)
    F.clean_grid(ax)
    ax.set_title("指數不等式：底數 < 1 → 不等號反向", fontsize=12.5, color=F.RED)

    # --- 右：對數 y=log_{1/2} x 遞減 → log_a A > log_a B 雖然 A<B ---
    ax = axes[1]
    xl = np.linspace(0.06, 6.2, 400)
    yl = np.log(xl) / np.log(0.5)
    ax.plot(xl, yl, color=F.RED, lw=2.6, zorder=4)

    xA, xB = 1.5, 4.0  # A < B
    yA, yB = np.log(xA) / np.log(0.5), np.log(xB) / np.log(0.5)
    for xv, yv in ((xA, yA), (xB, yB)):
        ax.plot([xv, xv], [0, yv], color="#9aa0a6", lw=1.0, ls=":", zorder=2)
        ax.plot([0, xv], [yv, yv], color="#9aa0a6", lw=1.0, ls=":", zorder=2)
        ax.plot(xv, yv, marker="o", ms=7, color=F.RED, zorder=6)

    ax.axhline(0, color=F.GRID, lw=0.9, zorder=1)
    ax.text(xA, 0.18, "A", color=F.INK, fontsize=13, ha="center", va="bottom")
    ax.text(xB, 0.18, "B", color=F.INK, fontsize=13, ha="center", va="bottom")
    ax.text(2.55, 0.30, "A < B", color=F.INK, fontsize=12.5, ha="left")
    ax.text(0.12, yA, "$\\log_a A$", color=F.RED, fontsize=12.5, ha="left", va="center")
    ax.text(0.12, yB, "$\\log_a B$", color=F.RED, fontsize=12.5, ha="left", va="center")
    ax.annotate(
        "",
        xy=(0.05, yA - 0.05),
        xytext=(0.05, yB + 0.05),
        arrowprops=dict(arrowstyle="-|>", color=F.RED, lw=1.6),
    )
    ax.text(
        3.2,
        1.35,
        "$\\log_a A > \\log_a B$\n（反向）",
        color=F.RED,
        fontsize=12.5,
        ha="left",
    )
    ax.text(4.9, 2.05, "$y=\\log_a x,\\ 0<a<1$", color=F.RED, fontsize=12, ha="center")
    ax.set_xlim(0, 6.4)
    ax.set_ylim(-2.4, 2.4)
    F.clean_grid(ax)
    ax.set_title("對數不等式：底數 < 1 → 不等號反向", fontsize=12.5, color=F.RED)

    fig.suptitle(
        "為什麼底數 < 1 要把不等號反過來：遞減函數讓大小關係對調", fontsize=13.5, y=1.02
    )
    fig.tight_layout()
    F.save_to(fig, CH, "數A3-2-不等式變號")


if __name__ == "__main__":
    fig_exponential()
    fig_logarithm()
    fig_growth_decay()
    fig_log_scale()
    fig_inequality_flip()
    print("done.")
