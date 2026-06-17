# -*- coding: utf-8 -*-
"""產生「數1-4 直線與圓」的圖，輸出到該章 sources/。
重繪：  .venv/bin/python _tools/fig_數1-4.py
本章多為座標幾何圖：F.canvas() + ax.plot() + F.clean_grid(ax)，
圓用參數式並 set_aspect("equal") 以免變形。
"""

import os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch
import figlib as F

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CH = os.path.join(ROOT, "數學", "數學一上（必修·第一冊）", "數1-4 直線與圓")


def _axes_through_origin(ax, xlim, ylim):
    """畫過原點的十字座標軸（帶箭頭），並隱藏外框。"""
    ax.annotate(
        "",
        xy=(xlim[1], 0),
        xytext=(xlim[0], 0),
        arrowprops=dict(arrowstyle="-|>", color=F.INK, lw=1.5),
    )
    ax.annotate(
        "",
        xy=(0, ylim[1]),
        xytext=(0, ylim[0]),
        arrowprops=dict(arrowstyle="-|>", color=F.INK, lw=1.5),
    )
    ax.text(xlim[1] - 0.15, -0.35, "$x$", color=F.INK, fontsize=12, ha="right")
    ax.text(0.18, ylim[1] - 0.15, "$y$", color=F.INK, fontsize=12, va="top")
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_aspect("equal")
    ax.axis("off")


def fig_symmetry():
    """一點 P(3,2) 對 x 軸、y 軸、原點、直線 y=x 的對稱點。"""
    fig, ax = F.canvas(6.2, 6.0)
    L = 4.0
    _axes_through_origin(ax, (-L, L), (-L, L))

    # 輔助線 y = x（淡）
    ax.plot([-L, L], [-L, L], color=F.GRID, lw=1.6, ls="--", zorder=1)
    ax.text(3.3, 3.55, "$y=x$", color="#9aa0a6", fontsize=11, ha="left")

    P = np.array([3.0, 2.0])
    pts = {
        "$P(3,\\,2)$": (P, F.INK, (0.25, 0.28), "left"),
        "對 $x$ 軸 $(3,-2)$": (np.array([3.0, -2.0]), F.RED, (0.25, -0.45), "left"),
        "對 $y$ 軸 $(-3,2)$": (np.array([-3.0, 2.0]), F.BLUE, (-0.25, 0.28), "right"),
        "對原點 $(-3,-2)$": (np.array([-3.0, -2.0]), F.PURPLE, (-0.25, -0.45), "right"),
        "對 $y=x$ $(2,3)$": (np.array([2.0, 3.0]), F.GREEN, (-0.25, 0.30), "right"),
    }
    for lab, (pt, col, off, ha) in pts.items():
        ax.add_patch(Circle(pt, 0.10, color=col, zorder=6))
        ax.text(
            pt[0] + off[0],
            pt[1] + off[1],
            lab,
            color=col,
            fontsize=11.5,
            ha=ha,
            va="center",
            zorder=7,
        )

    # 連線示意對稱（P 與各像點之間的虛線，垂直於對稱軸）
    # 對 x 軸：鉛直連線
    ax.plot([3, 3], [2, -2], color=F.RED, lw=1.1, ls=":", zorder=2)
    # 對 y 軸：水平連線
    ax.plot([3, -3], [2, 2], color=F.BLUE, lw=1.1, ls=":", zorder=2)
    # 對 y=x：與 y=x 垂直
    ax.plot([3, 2], [2, 3], color=F.GREEN, lw=1.1, ls=":", zorder=2)
    # 對原點：過原點連線
    ax.plot([3, -3], [2, -2], color=F.PURPLE, lw=1.1, ls=":", zorder=2)
    ax.add_patch(Circle((0, 0), 0.07, color=F.INK, zorder=6))

    ax.set_title("一點對各軸／原點／直線 $y=x$ 的對稱", fontsize=14)
    F.save_to(fig, CH, "數1-4-對稱")


def fig_point_line_distance():
    """點 P 到直線 L 的距離：垂足、垂線段 d，標出公式。"""
    fig, ax = F.canvas(6.6, 5.4)

    # 直線 L: 3x + 4y - 12 = 0  →  y = (12 - 3x)/4
    def Ly(x):
        return (12 - 3 * x) / 4.0

    xs = np.array([-1.0, 6.0])
    ax.plot(xs, Ly(xs), color=F.INK, lw=2.4, zorder=3)
    ax.text(
        5.0, Ly(5.0) + 0.30, "$L:\\;3x+4y-12=0$", color=F.INK, fontsize=12, ha="right"
    )

    # 點 P(5, 5)
    P = np.array([5.0, 5.0])
    # 垂足 Q：把 P 投影到 L。法向量 n=(3,4)/5
    a, b, c = 3.0, 4.0, -12.0
    t = (a * P[0] + b * P[1] + c) / (a * a + b * b)
    Q = P - t * np.array([a, b])

    ax.add_patch(Circle(P, 0.12, color=F.BLUE, zorder=6))
    ax.text(
        P[0] + 0.2,
        P[1] + 0.15,
        "$P(x_0,\\,y_0)$",
        color=F.BLUE,
        fontsize=12.5,
        ha="left",
    )
    ax.add_patch(Circle(Q, 0.10, color=F.INK, zorder=6))
    ax.text(
        Q[0] - 0.2, Q[1] - 0.35, "$Q$（垂足）", color=F.INK, fontsize=11.5, ha="right"
    )

    # 垂線段 d（紅）
    ax.plot([P[0], Q[0]], [P[1], Q[1]], color=F.RED, lw=2.4, zorder=4)
    mid = (P + Q) / 2
    ax.text(
        mid[0] + 0.30,
        mid[1] + 0.20,
        "$d$",
        color=F.RED,
        fontsize=15,
        ha="left",
        va="center",
    )

    # 直角符號
    nhat = np.array([a, b]) / np.hypot(a, b)  # 沿垂線方向（指向 L）
    lhat = np.array([b, -a]) / np.hypot(a, b)  # 沿 L 方向
    s = 0.32
    c1 = Q + s * (-nhat) + s * lhat
    c2 = Q + s * lhat
    c3 = Q
    c4 = Q + s * (-nhat)
    ax.plot([c1[0], c2[0]], [c1[1], c2[1]], color=F.INK, lw=1.1)
    ax.plot([c1[0], c4[0]], [c1[1], c4[1]], color=F.INK, lw=1.1)

    # 公式框
    ax.text(
        0.4,
        5.5,
        r"$d=\dfrac{|ax_0+by_0+c|}{\sqrt{a^2+b^2}}$",
        color=F.RED,
        fontsize=14,
        ha="left",
        va="center",
        bbox=dict(boxstyle="round,pad=0.3", fc="white", ec=F.RED, lw=1.3),
    )

    ax.set_xlim(-1.2, 6.4)
    ax.set_ylim(-0.6, 6.2)
    ax.set_aspect("equal")
    ax.axhline(0, color=F.GRID, lw=1.0)
    ax.axvline(0, color=F.GRID, lw=1.0)
    F.clean_grid(ax)
    ax.set_xticks(range(0, 7))
    ax.set_yticks(range(0, 7))
    ax.set_title("點到直線的距離", fontsize=14)
    F.save_to(fig, CH, "數1-4-點到直線距離")


def fig_line_circle():
    """直線與圓三種位置關係：d>r 相離、d=r 相切、d<r 相交。"""
    fig, axes = plt.subplots(1, 3, figsize=(11.4, 4.2))
    th = np.linspace(0, 2 * np.pi, 400)
    r = 1.5
    cx, cy = 0.0, 0.0

    cases = [
        (axes[0], 2.35, F.BLUE, "相離", "$d>r$：無交點"),
        (axes[1], r, F.GREEN, "相切", "$d=r$：一個交點（切點）"),
        (axes[2], 0.75, F.RED, "相交", "$d<r$：兩個交點"),
    ]

    for ax, d, col, name, sub in cases:
        # 圓
        ax.plot(cx + r * np.cos(th), cy + r * np.sin(th), color=F.INK, lw=2.2)
        ax.add_patch(Circle((cx, cy), 0.05, color=F.INK, zorder=6))
        ax.text(
            cx + 0.12, cy - 0.02, "$O$", color=F.INK, fontsize=12, ha="left", va="top"
        )
        # 半徑 r（水平虛線）
        ax.plot([cx, cx + r], [cy, cy], color="#9aa0a6", lw=1.4, ls="--", zorder=3)
        ax.text(cx + r / 2, cy + 0.16, "$r$", color="#6b7280", fontsize=12, ha="center")

        # 水平直線 y = d（圓心到它的距離正好是 d）
        xline = np.array([-2.6, 2.6])
        ax.plot(xline, [d, d], color=col, lw=2.4, zorder=4)
        # 圓心到直線的距離段 d（鉛直）
        ax.annotate(
            "",
            xy=(cx, d),
            xytext=(cx, cy),
            arrowprops=dict(arrowstyle="<|-|>", color=col, lw=1.8),
        )
        ax.text(
            cx - 0.18, d / 2, "$d$", color=col, fontsize=13, ha="right", va="center"
        )

        # 交點
        if d < r - 1e-9:
            xint = np.sqrt(r * r - d * d)
            for sx in (-xint, xint):
                ax.add_patch(Circle((cx + sx, d), 0.09, color=col, zorder=7))
        elif abs(d - r) < 1e-9:
            ax.add_patch(Circle((cx, d), 0.10, color=col, zorder=7))

        ax.set_xlim(-2.7, 2.7)
        ax.set_ylim(-2.0, 3.0)
        ax.set_aspect("equal")
        ax.axis("off")
        ax.set_title(f"{name}　{sub}", fontsize=12.5, color=col)

    fig.suptitle(
        "直線與圓：比較「圓心到直線的距離 $d$」與「半徑 $r$」", fontsize=14, y=1.02
    )
    fig.tight_layout()
    F.save_to(fig, CH, "數1-4-直線與圓")


if __name__ == "__main__":
    fig_symmetry()
    fig_point_line_distance()
    fig_line_circle()
    print("done.")
