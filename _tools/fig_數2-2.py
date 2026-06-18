# -*- coding: utf-8 -*-
"""產生「數2-2 數列與級數」的圖，輸出到該章 sources/。
重繪：  .venv/bin/python _tools/fig_數2-2.py
本章圖以示意/條形/流程為主：F.canvas()/F.schematic()。
注意：matplotlib mathtext 不支援 \\dfrac/\\tfrac（用 \\frac）；中文勿放進 $...$。
"""

import os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import (
    Circle,
    Rectangle,
    FancyArrowPatch,
    FancyBboxPatch,
    Ellipse,
)
import figlib as F

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CH = os.path.join(ROOT, "數學", "數學一下（必修·第二冊）", "數2-2 數列與級數")


def fig_arith_geo():
    """等差數列（線性）與等比數列（指數）的散點對照。"""
    fig, axes = plt.subplots(1, 2, figsize=(11.0, 4.4))

    n = np.arange(1, 8)

    # 等差：a1=2, d=3  → 2,5,8,11,14,17,20
    a = 2 + (n - 1) * 3
    axL = axes[0]
    axL.plot(n, a, color=F.BLUE, lw=1.6, ls="--", zorder=2)
    axL.scatter(n, a, color=F.BLUE, s=70, zorder=4)
    for xi, yi in zip(n, a):
        axL.annotate(
            str(yi),
            (xi, yi),
            textcoords="offset points",
            xytext=(0, 9),
            ha="center",
            color=F.BLUE,
            fontsize=10.5,
        )
    # 標一段公差
    axL.annotate(
        "",
        xy=(3, a[2]),
        xytext=(2, a[1]),
        arrowprops=dict(arrowstyle="-", color=F.AMBER, lw=0),
    )
    axL.plot([2, 3], [a[1], a[1]], color=F.AMBER, lw=1.4)
    axL.plot([3, 3], [a[1], a[2]], color=F.AMBER, lw=1.4)
    axL.text(3.12, (a[1] + a[2]) / 2, "+d", color=F.AMBER, fontsize=12, va="center")
    axL.set_title("等差數列：每次「加」固定公差 d", fontsize=13)
    axL.set_xlabel("項數 $n$")
    axL.set_ylabel("$a_n$")
    axL.set_ylim(0, 24)
    F.clean_grid(axL)

    # 等比：a1=1, r=2  → 1,2,4,8,16,32,64
    g = 1 * 2.0 ** (n - 1)
    axR = axes[1]
    axR.plot(n, g, color=F.RED, lw=1.6, ls="--", zorder=2)
    axR.scatter(n, g, color=F.RED, s=70, zorder=4)
    for xi, yi in zip(n, g):
        axR.annotate(
            str(int(yi)),
            (xi, yi),
            textcoords="offset points",
            xytext=(0, 9),
            ha="center",
            color=F.RED,
            fontsize=10.5,
        )
    axR.plot([2, 3], [g[1], g[1]], color=F.AMBER, lw=1.4)
    axR.plot([3, 3], [g[1], g[2]], color=F.AMBER, lw=1.4)
    axR.text(3.12, (g[1] + g[2]) / 2, "×r", color=F.AMBER, fontsize=12, va="center")
    axR.set_title("等比數列：每次「乘」固定公比 r", fontsize=13)
    axR.set_xlabel("項數 $n$")
    axR.set_ylabel("$a_n$")
    axR.set_ylim(0, 72)
    F.clean_grid(axR)

    fig.suptitle("等差（直線成長） vs 等比（指數成長）", fontsize=14, y=1.02)
    fig.tight_layout()
    F.save_to(fig, CH, "數2-2-等差等比")


def fig_gauss_pairing():
    """等差級數求和的高斯配對：正反兩列相加，每對都等於 a1+an。"""
    fig, ax = F.schematic(8.4, 4.2)

    vals = [1, 2, 3, 4, 5, 6]
    n = len(vals)
    box_w, box_h, gap = 0.95, 0.7, 0.12
    x0 = 0.0
    y_top, y_bot = 2.2, 0.6

    def draw_row(y, seq, color):
        for i, v in enumerate(seq):
            x = x0 + i * (box_w + gap)
            ax.add_patch(
                FancyBboxPatch(
                    (x, y),
                    box_w,
                    box_h,
                    boxstyle="round,pad=0.02,rounding_size=0.08",
                    fc="white",
                    ec=color,
                    lw=1.8,
                    zorder=3,
                )
            )
            ax.text(
                x + box_w / 2,
                y + box_h / 2,
                str(v),
                color=color,
                fontsize=14,
                ha="center",
                va="center",
                zorder=4,
            )

    draw_row(y_top, vals, F.BLUE)  # 正序
    draw_row(y_bot, vals[::-1], F.RED)  # 反序

    # 每一直行相加 = 7
    for i in range(n):
        x = x0 + i * (box_w + gap) + box_w / 2
        ax.text(
            x,
            y_bot - 0.45,
            "7",
            color=F.GREEN,
            fontsize=14,
            ha="center",
            va="center",
            zorder=4,
        )
    ax.text(
        x0 - 0.55,
        y_top + box_h / 2,
        "正",
        color=F.BLUE,
        fontsize=13,
        ha="right",
        va="center",
    )
    ax.text(
        x0 - 0.55,
        y_bot + box_h / 2,
        "反",
        color=F.RED,
        fontsize=13,
        ha="right",
        va="center",
    )
    ax.text(
        x0 - 0.55,
        y_bot - 0.45,
        "和",
        color=F.GREEN,
        fontsize=13,
        ha="right",
        va="center",
    )

    total_w = n * (box_w + gap) - gap
    ax.text(
        x0 + total_w / 2,
        y_bot - 1.15,
        "每行都是 1+6 = 7，共 6 行 → 2S = 6×7，故 S = 6×7÷2 = 21",
        color=F.INK,
        fontsize=12.5,
        ha="center",
        va="center",
    )
    ax.text(
        x0 + total_w / 2,
        y_top + box_h + 0.55,
        "高斯配對法：把級數正著寫一遍、反著再寫一遍",
        color=F.INK,
        fontsize=13,
        ha="center",
        va="center",
    )

    ax.set_xlim(-1.4, total_w + 0.4)
    ax.set_ylim(-1.7, 3.7)
    F.save_to(fig, CH, "數2-2-級數求和")


def fig_induction_dominoes():
    """數學歸納法的骨牌示意：第一張倒（基底）+ 每張倒會推倒下一張（遞推）。"""
    fig, ax = F.schematic(9.0, 3.6)

    n_dom = 7
    w, h, gap = 0.32, 1.5, 0.85
    base_y = 0.0

    for i in range(n_dom):
        x = i * gap
        if i == 0:
            # 第一張已倒下（基底）：畫成傾倒的矩形
            cx, cy = x + 0.5, base_y + w / 2
            rect = Rectangle(
                (x - 0.2, base_y),
                h,
                w,
                angle=0.0,
                fc=F.BLUE,
                ec=F.INK,
                lw=1.4,
                alpha=0.85,
                zorder=3,
            )
            ax.add_patch(rect)
            ax.text(
                x + h / 2 - 0.2,
                base_y + w + 0.28,
                "倒",
                color=F.BLUE,
                fontsize=12,
                ha="center",
            )
        else:
            color = F.GREEN if i < n_dom - 1 else F.AMBER
            ax.add_patch(
                Rectangle((x, base_y), w, h, fc="white", ec=color, lw=1.8, zorder=3)
            )
            ax.text(
                x + w / 2,
                base_y + h + 0.22,
                str(i + 1),
                color=color,
                fontsize=12,
                ha="center",
            )

    # 推倒箭頭
    for i in range(1, n_dom - 1):
        x = i * gap
        ax.annotate(
            "",
            xy=(x + gap - 0.05, base_y + h * 0.75),
            xytext=(x + w + 0.05, base_y + h * 0.75),
            arrowprops=dict(arrowstyle="-|>", color=F.RED, lw=1.6),
        )

    ax.text(
        0.55,
        base_y - 0.55,
        "① 基底：第 1 張倒下",
        color=F.BLUE,
        fontsize=12.5,
        ha="left",
    )
    ax.text(
        (n_dom - 1) * gap,
        base_y - 0.55,
        "② 遞推：第 k 張倒 ⇒ 第 k+1 張也倒",
        color=F.RED,
        fontsize=12.5,
        ha="right",
    )
    ax.text(
        (n_dom - 1) * gap / 2,
        base_y + h + 0.95,
        "兩件事都成立 → 所有骨牌都會倒（對所有 n 成立）",
        color=F.INK,
        fontsize=13,
        ha="center",
    )

    ax.set_xlim(-0.6, (n_dom - 1) * gap + 0.8)
    ax.set_ylim(-1.0, h + 1.5)
    F.save_to(fig, CH, "數2-2-數學歸納法")


def fig_suff_nec():
    """充分／必要條件的範圍包含：p 的範圍 ⊆ q 的範圍 ⇒ p 是 q 的充分條件。"""
    fig, ax = F.schematic(7.4, 5.2)

    # 大圈 q，小圈 p（p ⊆ q）
    big = Ellipse((0, 0), 5.2, 3.8, fc="#e9f0fb", ec=F.BLUE, lw=2.0, zorder=2)
    small = Ellipse((-0.6, -0.1), 2.4, 1.7, fc="#fdeaea", ec=F.RED, lw=2.0, zorder=3)
    ax.add_patch(big)
    ax.add_patch(small)

    ax.text(
        -0.6, -0.1, "$p$", color=F.RED, fontsize=18, ha="center", va="center", zorder=5
    )
    ax.text(
        1.7, 1.0, "$q$", color=F.BLUE, fontsize=18, ha="center", va="center", zorder=5
    )

    ax.text(
        0,
        -2.45,
        "$p$ 的範圍包含於 $q$ 的範圍內　（$p \\Rightarrow q$）",
        color=F.INK,
        fontsize=13,
        ha="center",
    )
    ax.text(
        0,
        -3.05,
        "小圈 p 是「充分」（夠了就行）；大圈 q 是「必要」（非有不可）",
        color=F.INK,
        fontsize=12.5,
        ha="center",
    )
    ax.text(
        0, 2.55, "範圍小 = 條件強 = 充分條件", color=F.RED, fontsize=12.5, ha="center"
    )

    ax.set_xlim(-3.4, 3.4)
    ax.set_ylim(-3.4, 3.1)
    F.save_to(fig, CH, "數2-2-充分必要")


if __name__ == "__main__":
    fig_arith_geo()
    fig_gauss_pairing()
    fig_induction_dominoes()
    fig_suff_nec()
    print("done.")
