# -*- coding: utf-8 -*-
"""產生「數1-3 指數與對數」的圖，輸出到該章 sources/。
重繪：  .venv/bin/python _tools/fig_數1-3.py
"""

import os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Arc, Circle, Polygon
import figlib as F

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CH = os.path.join(ROOT, "數學", "數學一上（必修·第一冊）", "數1-3 指數與對數")


def _origin_axes(ax):
    """畫一組過原點的座標軸（數學課常用）。"""
    ax.axhline(0, color=F.INK, lw=1.2, zorder=2)
    ax.axvline(0, color=F.INK, lw=1.2, zorder=2)
    for s in ("top", "right", "left", "bottom"):
        ax.spines[s].set_visible(False)
    ax.grid(True, color=F.GRID, lw=0.8)
    ax.set_axisbelow(True)


def fig_exponential():
    """y = a^x：a>1 成長、0<a<1 衰退，皆過 (0,1)。"""
    fig, ax = F.canvas(6.4, 4.6)
    x = np.linspace(-3, 3, 400)
    # 成長：a = 2
    ax.plot(x, 2.0**x, color=F.BLUE, lw=2.6, label=r"$y=2^{\,x}$（$a>1$，成長）")
    # 衰退：a = 1/2
    ax.plot(
        x, 0.5**x, color=F.RED, lw=2.6, label=r"$y=(\frac{1}{2})^{x}$（$0<a<1$，衰退）"
    )
    # 共同點 (0,1)
    ax.add_patch(Circle((0, 1), 0.06, color=F.INK, zorder=6))
    ax.text(0.18, 1.18, "$(0,\\,1)$", color=F.INK, fontsize=12, ha="left")
    # 漸近線 y=0
    ax.text(2.55, 0.18, "$y=0$（漸近線）", color="#6b7280", fontsize=11, ha="right")

    _origin_axes(ax)
    ax.set_xlim(-3, 3)
    ax.set_ylim(-0.4, 6.2)
    ax.set_xlabel("$x$")
    ax.set_ylabel("$y$")
    ax.set_title(r"指數函數 $y=a^{\,x}$（$a>0,\ a\neq1$）")
    ax.legend(loc="upper center", fontsize=11, frameon=False)
    fig.tight_layout()
    F.save_to(fig, CH, "數1-3-指數函數")


def fig_logarithm():
    """y = a^x 與 y = log_a x 對 y=x 對稱，互為反函數（取 a=2）。"""
    fig, ax = F.canvas(5.6, 5.6, equal=True)
    x = np.linspace(-3, 3.2, 400)
    xp = np.linspace(0.04, 6.0, 400)
    # y = 2^x
    ax.plot(x, 2.0**x, color=F.BLUE, lw=2.6, label=r"$y=2^{\,x}$")
    # y = log_2 x
    ax.plot(xp, np.log(xp) / np.log(2.0), color=F.RED, lw=2.6, label=r"$y=\log_2 x$")
    # 對稱軸 y = x
    ax.plot([-3, 6], [-3, 6], color="#6b7280", lw=1.4, ls="--")
    ax.text(
        3.4,
        4.0,
        "$y=x$",
        color="#6b7280",
        fontsize=12,
        rotation=45,
        ha="center",
        va="center",
    )
    # 對稱點：(0,1) <-> (1,0)
    for px, py in [(0, 1), (1, 0)]:
        ax.add_patch(Circle((px, py), 0.08, color=F.INK, zorder=6))
    ax.text(-0.25, 1.25, "$(0,1)$", color=F.BLUE, fontsize=11, ha="right")
    ax.text(1.25, -0.45, "$(1,0)$", color=F.RED, fontsize=11, ha="left")

    _origin_axes(ax)
    ax.set_xlim(-3, 6)
    ax.set_ylim(-3, 6)
    ax.set_xlabel("$x$")
    ax.set_ylabel("$y$")
    ax.set_title(r"指數與對數互為反函數（對 $y=x$ 對稱）")
    ax.legend(loc="lower right", fontsize=11, frameon=False)
    fig.tight_layout()
    F.save_to(fig, CH, "數1-3-對數函數")


def fig_amgm():
    """算幾不等式幾何示意：半圓中，半徑（=算術平均）≥ 半弦（=幾何平均）。"""
    fig, ax = F.schematic(7.0, 4.2)
    a, b = 4.6, 1.8  # 兩段長 a、b
    R = (a + b) / 2.0  # 半徑 = 算術平均 (a+b)/2
    O = np.array([0.0, 0.0])  # 圓心
    A = np.array([-R, 0.0])  # 直徑左端
    B = np.array([R, 0.0])  # 直徑右端
    # 分點 D：使 AD = a、DB = b（D 在圓心右側 (a-b)/2 處）
    D = np.array([(a - b) / 2.0, 0.0])
    h = np.sqrt(a * b)  # 垂線高 = 幾何平均 √(ab)
    H = np.array([D[0], h])  # 半圓上的點

    th = np.linspace(0, np.pi, 200)
    ax.plot(R * np.cos(th), R * np.sin(th), color=F.INK, lw=2.0)  # 半圓
    ax.plot([A[0], B[0]], [0, 0], color=F.INK, lw=2.0)  # 直徑

    # a、b 兩段
    ax.plot([A[0], D[0]], [0, 0], color=F.AMBER, lw=5, solid_capstyle="butt", zorder=3)
    ax.plot([D[0], B[0]], [0, 0], color=F.GREEN, lw=5, solid_capstyle="butt", zorder=3)
    ax.text((A[0] + D[0]) / 2, -0.42, "$a$", color=F.AMBER, fontsize=15, ha="center")
    ax.text((D[0] + B[0]) / 2, -0.42, "$b$", color=F.GREEN, fontsize=15, ha="center")

    # 半徑 R = (a+b)/2（算術平均）：從圓心拉到圓上一點
    Pr = np.array([R * np.cos(np.deg2rad(125)), R * np.sin(np.deg2rad(125))])
    ax.plot([O[0], Pr[0]], [O[1], Pr[1]], color=F.BLUE, lw=2.4, zorder=4)
    ax.text(
        (O[0] + Pr[0]) / 2 - 0.15,
        (O[1] + Pr[1]) / 2 + 0.28,
        r"$R=\frac{a+b}{2}$",
        color=F.BLUE,
        fontsize=14,
        ha="center",
        va="bottom",
    )

    # 垂線 h = √(ab)（幾何平均）
    ax.plot([D[0], H[0]], [0, H[1]], color=F.RED, lw=2.6, zorder=4)
    ax.text(
        H[0] + 0.18,
        H[1] / 2,
        r"$h=\sqrt{ab}$",
        color=F.RED,
        fontsize=14,
        ha="left",
        va="center",
    )

    # 標點
    for P, lab, dy in [(A, "$A$", -0.45), (B, "$B$", -0.45), (D, "$D$", -0.45)]:
        ax.add_patch(Circle(P, 0.07, color=F.INK, zorder=6))
        ax.text(P[0], P[1] + dy, lab, color=F.INK, fontsize=12, ha="center")
    ax.add_patch(Circle(O, 0.07, color=F.INK, zorder=6))
    ax.text(O[0] - 0.05, -0.45, "$O$", color=F.INK, fontsize=12, ha="center")
    ax.add_patch(Circle(H, 0.07, color=F.RED, zorder=6))

    ax.text(
        0,
        R + 0.55,
        r"半徑 $\geq$ 半弦：$\frac{a+b}{2}\geq\sqrt{ab}$（等號於 $a=b$）",
        ha="center",
        color=F.INK,
        fontsize=13,
    )
    ax.set_title("算幾不等式的幾何解釋（半圓中的高與半徑）", fontsize=14)
    ax.set_xlim(-R - 0.8, R + 0.8)
    ax.set_ylim(-1.0, R + 1.1)
    F.save_to(fig, CH, "數1-3-算幾不等式")


if __name__ == "__main__":
    fig_exponential()
    fig_logarithm()
    fig_amgm()
    print("done.")
