# -*- coding: utf-8 -*-
r"""產生「數A3-3 平面向量」的圖，輸出到該章 sources/。
重繪：  .venv/bin/python _tools/fig_數A3-3.py

注意：mathtext 不支援 \dfrac/\tfrac；圖內中文不放在 $...$ 內。
向量圖一律 set_aspect("equal")。
"""

import os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Arc, Circle, FancyArrowPatch
import figlib as F

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CH = os.path.join(ROOT, "數學", "數學二上（數學A·第三冊）", "數A3-3 平面向量")


def fig_operations():
    """向量的加法（三角形 / 平行四邊形）、減法、係數積。"""
    fig, axes = plt.subplots(1, 3, figsize=(12.6, 4.2))

    a = np.array([3.0, 1.0])
    b = np.array([1.0, 2.5])
    O = np.array([0.0, 0.0])

    # --- (1) 加法：三角形法 + 平行四邊形法 ---
    ax = axes[0]
    ax.set_aspect("equal")
    # 平行四邊形（淡填色）
    para = Polygon(
        [O, a, a + b, b],
        closed=True,
        facecolor=F.BLUE,
        alpha=0.08,
        edgecolor="none",
        zorder=1,
    )
    ax.add_patch(para)
    F.arrow(ax, O, a, color=F.BLUE)
    F.arrow(ax, O, b, color=F.GREEN)
    # 三角形法：把 b 接在 a 末端
    F.arrow(ax, a, a + b, color=F.GREEN, ls="--")
    F.arrow(ax, O, a + b, color=F.RED, lw=2.8)
    ax.text(
        a[0] * 0.55, a[1] * 0.55 - 0.30, "a", color=F.BLUE, fontsize=15, ha="center"
    )
    ax.text(
        b[0] * 0.45 - 0.28, b[1] * 0.55, "b", color=F.GREEN, fontsize=15, ha="center"
    )
    ax.text(
        a[0] + b[0] * 0.5 + 0.10,
        a[1] + b[1] * 0.5 - 0.18,
        "b",
        color=F.GREEN,
        fontsize=14,
        ha="left",
    )
    ax.text(
        (a + b)[0] * 0.5 - 0.28,
        (a + b)[1] * 0.5 + 0.28,
        "a + b",
        color=F.RED,
        fontsize=15,
        ha="center",
    )
    ax.set_title("加法：三角形法／平行四邊形法", fontsize=13)
    ax.set_xlim(-0.6, 4.8)
    ax.set_ylim(-0.6, 4.2)
    F.clean_grid(ax)

    # --- (2) 減法：a - b = a + (-b)，指向被減端 ---
    ax = axes[1]
    ax.set_aspect("equal")
    F.arrow(ax, O, a, color=F.BLUE)
    F.arrow(ax, O, b, color=F.GREEN)
    # a - b：從 b 的箭頭尖端指向 a 的箭頭尖端
    F.arrow(ax, b, a, color=F.AMBER, lw=2.8)
    ax.text(
        a[0] * 0.55, a[1] * 0.55 - 0.30, "a", color=F.BLUE, fontsize=15, ha="center"
    )
    ax.text(
        b[0] * 0.5 - 0.30, b[1] * 0.55, "b", color=F.GREEN, fontsize=15, ha="center"
    )
    mid = (a + b) / 2
    ax.text(
        mid[0] + 0.15, mid[1] + 0.20, "a − b", color=F.AMBER, fontsize=15, ha="left"
    )
    ax.text(
        2.55,
        3.55,
        "a − b 由 b 尖端\n指向 a 尖端",
        color=F.AMBER,
        fontsize=11,
        ha="center",
        va="top",
    )
    ax.set_title("減法：a − b（指向被減向量）", fontsize=13)
    ax.set_xlim(-0.6, 4.8)
    ax.set_ylim(-0.6, 4.2)
    F.clean_grid(ax)

    # --- (3) 係數積：2a 與 -a ---
    ax = axes[2]
    ax.set_aspect("equal")
    F.arrow(ax, O, 2 * a, color=F.PURPLE, lw=2.8)
    F.arrow(ax, O, a, color=F.BLUE)
    F.arrow(ax, O, -a, color=F.RED, ls="--")
    ax.text(
        a[0] * 0.5 + 0.05,
        a[1] * 0.5 + 0.28,
        "a",
        color=F.BLUE,
        fontsize=15,
        ha="center",
    )
    ax.text(
        2 * a[0] * 0.78,
        2 * a[1] * 0.78 + 0.30,
        "2a（同向、伸長）",
        color=F.PURPLE,
        fontsize=12,
        ha="center",
    )
    ax.text(
        -a[0] * 0.55 - 0.10,
        -a[1] * 0.55 - 0.32,
        "−a（反向）",
        color=F.RED,
        fontsize=12,
        ha="center",
    )
    ax.set_title("係數積：ka（k 縮放、負號反向）", fontsize=13)
    ax.set_xlim(-3.6, 6.8)
    ax.set_ylim(-1.8, 2.6)
    F.clean_grid(ax)

    fig.tight_layout()
    F.save_to(fig, CH, "數A3-3-向量運算")


def fig_dot_product():
    """內積的幾何意義：|a||b|cosθ，b 在 a 上的投影。"""
    fig, ax = F.canvas(6.4, 4.8)
    ax.set_aspect("equal")
    O = np.array([0.0, 0.0])
    a = np.array([4.2, 0.0])
    b = np.array([2.4, 2.6])

    # a 與 b
    F.arrow(ax, O, a, color=F.BLUE, lw=2.8)
    F.arrow(ax, O, b, color=F.GREEN, lw=2.8)
    # b 在 a 上的投影長 = |b|cosθ
    ua = a / np.linalg.norm(a)
    projlen = np.dot(b, ua)
    foot = O + projlen * ua
    # 投影線段（粗、琥珀）
    ax.plot(
        [O[0], foot[0]],
        [O[1], foot[1]],
        color=F.AMBER,
        lw=5.0,
        alpha=0.55,
        zorder=2,
        solid_capstyle="butt",
    )
    # 垂足虛線
    ax.plot([b[0], foot[0]], [b[1], foot[1]], color=F.INK, lw=1.2, ls="--", zorder=3)
    # 直角記號
    rs = 0.22
    perp = np.array([0.0, 1.0])
    ax.add_patch(
        Polygon(
            [foot, foot - rs * ua, foot - rs * ua + rs * perp, foot + rs * perp],
            closed=True,
            fill=False,
            edgecolor=F.INK,
            lw=1.0,
        )
    )
    # 夾角弧
    th = np.degrees(np.arctan2(b[1], b[0]))
    ax.add_patch(Arc(O, 1.5, 1.5, angle=0, theta1=0, theta2=th, color=F.INK, lw=1.4))
    ax.text(0.95, 0.42, "θ", color=F.INK, fontsize=15)
    # 標籤
    ax.text(a[0] * 0.6, -0.34, "a", color=F.BLUE, fontsize=16, ha="center")
    ax.text(
        b[0] * 0.5 - 0.30,
        b[1] * 0.5 + 0.10,
        "b",
        color=F.GREEN,
        fontsize=16,
        ha="center",
    )
    ax.text(
        foot[0] * 0.5,
        -0.34,
        "投影長 = |b| cosθ",
        color=F.AMBER,
        fontsize=12,
        ha="center",
    )
    ax.text(2.1, 3.4, "a · b = |a| |b| cosθ", color=F.RED, fontsize=14, ha="center")
    ax.set_title("內積的幾何意義（投影）", fontsize=14)
    ax.set_xlim(-0.8, 5.2)
    ax.set_ylim(-0.9, 3.8)
    F.clean_grid(ax)
    F.save_to(fig, CH, "數A3-3-內積")


def fig_projection():
    """一向量在另一向量上的正射影向量。"""
    fig, ax = F.canvas(6.4, 4.8)
    ax.set_aspect("equal")
    O = np.array([0.0, 0.0])
    a = np.array([4.4, 0.0])
    b = np.array([2.2, 2.8])

    ua = a / np.linalg.norm(a)
    projlen = np.dot(b, ua)
    foot = O + projlen * ua

    F.arrow(ax, O, a, color=F.BLUE, lw=2.6)
    F.arrow(ax, O, b, color=F.GREEN, lw=2.8)
    # 正射影向量（沿 a 方向，紅色粗箭頭）
    F.arrow(ax, O, foot, color=F.RED, lw=3.0)
    # 從 b 尖端垂下的虛線
    ax.plot([b[0], foot[0]], [b[1], foot[1]], color=F.INK, lw=1.3, ls="--", zorder=3)
    # 直角記號
    rs = 0.22
    perp = np.array([0.0, 1.0])
    ax.add_patch(
        Polygon(
            [foot, foot - rs * ua, foot - rs * ua + rs * perp, foot + rs * perp],
            closed=True,
            fill=False,
            edgecolor=F.INK,
            lw=1.0,
        )
    )
    ax.text(a[0] * 0.82, -0.34, "a", color=F.BLUE, fontsize=16, ha="center")
    ax.text(
        b[0] * 0.5 - 0.30,
        b[1] * 0.5 + 0.10,
        "b",
        color=F.GREEN,
        fontsize=16,
        ha="center",
    )
    ax.text(
        foot[0] * 0.5, 0.28, "b 在 a 上的正射影", color=F.RED, fontsize=12, ha="center"
    )
    ax.text(
        3.1, 3.2, "投影向量 = (a·b / |a|²) a", color=F.RED, fontsize=12, ha="center"
    )
    ax.set_title("正射影向量", fontsize=14)
    ax.set_xlim(-0.8, 5.4)
    ax.set_ylim(-0.9, 3.8)
    F.clean_grid(ax)
    F.save_to(fig, CH, "數A3-3-正射影")


def fig_determinant_area():
    """二階行列式 = 平行四邊形面積。"""
    fig, ax = F.canvas(6.2, 5.0)
    ax.set_aspect("equal")
    O = np.array([0.0, 0.0])
    a = np.array([3.6, 0.8])
    b = np.array([1.2, 2.8])

    para = Polygon(
        [O, a, a + b, b],
        closed=True,
        facecolor=F.BLUE,
        alpha=0.16,
        edgecolor=F.INK,
        lw=1.4,
        zorder=1,
    )
    ax.add_patch(para)
    F.arrow(ax, O, a, color=F.BLUE, lw=2.8)
    F.arrow(ax, O, b, color=F.GREEN, lw=2.8)
    # 對邊（淡虛線提示平行四邊形）
    F.arrow(ax, a, a + b, color=F.GREEN, ls="--", lw=1.6)
    F.arrow(ax, b, a + b, color=F.BLUE, ls="--", lw=1.6)

    ax.text(
        a[0] * 0.55,
        a[1] * 0.55 - 0.32,
        r"$a=(x_1,\,y_1)$",
        color=F.BLUE,
        fontsize=14,
        ha="center",
    )
    ax.text(
        b[0] * 0.45 - 0.55,
        b[1] * 0.55,
        r"$b=(x_2,\,y_2)$",
        color=F.GREEN,
        fontsize=14,
        ha="center",
    )
    mid = (a + b) / 2
    ax.text(mid[0], mid[1] + 0.18, "面積", color=F.INK, fontsize=13, ha="center")
    ax.text(
        mid[0],
        mid[1] - 0.30,
        r"$=|x_1 y_2 - x_2 y_1|$",
        color=F.INK,
        fontsize=13,
        ha="center",
    )
    ax.set_title("二階行列式 = 平行四邊形面積", fontsize=14)
    ax.set_xlim(-0.6, 5.4)
    ax.set_ylim(-0.6, 4.2)
    F.clean_grid(ax)
    F.save_to(fig, CH, "數A3-3-行列式面積")


if __name__ == "__main__":
    fig_operations()
    fig_dot_product()
    fig_projection()
    fig_determinant_area()
    print("done.")
