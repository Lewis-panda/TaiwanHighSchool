# -*- coding: utf-8 -*-
"""產生「必物-1 科學態度與方法」的圖，輸出到該章 sources/。
重繪：  .venv/bin/python _tools/fig_必物-1.py
"""

import os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, FancyBboxPatch
import figlib as F

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CH = os.path.join(ROOT, "物理", "物理一（必修物理）", "必物-1 科學態度與方法")


def fig_scale():
    """長度數量級對數軸：從原子核 10^-15 m 到可觀測宇宙 ~10^26 m。"""
    fig, ax = F.canvas(9.6, 4.4)

    # (指數, 標籤, 顏色, 文字層級 lev：±1 近、±2 遠；dx：文字水平微調)
    items = [
        (-15, "原子核", F.RED, +1, 0.0),
        (-10, "原子", F.RED, -1, 0.0),
        (-9, "DNA 寬度", F.AMBER, +2, 0.0),
        (-7, "病毒", F.AMBER, -2, 0.0),
        (-5, "紅血球", F.AMBER, +1, 0.0),
        (-3, "螞蟻", F.GREEN, -1, 0.0),
        (0, "人", F.BLUE, +1, 0.0),
        (4, "一座城市", F.BLUE, -1, -0.6),
        (6, "台灣南北長", F.BLUE, +2, 0.0),
        (8, "地球直徑", F.PURPLE, -2, 0.0),
        (9, "太陽直徑", F.PURPLE, +1, 0.4),
        (11, "地球–太陽距離", F.PURPLE, -1, 1.2),
        (16, "最近的恆星", F.INK, +1, 0.0),
        (21, "銀河系直徑", F.INK, -1, 0.0),
        (26, "可觀測宇宙", F.INK, +1, -0.4),
    ]
    ax.set_xlim(-18, 30)
    ax.set_ylim(-2.2, 2.4)

    # 主數線
    ax.annotate(
        "",
        xy=(29.5, 0),
        xytext=(-18, 0),
        arrowprops=dict(arrowstyle="-|>", color=F.INK, lw=2.0),
    )
    # 主要刻度（每 5 個數量級）
    for e in range(-15, 27, 5):
        ax.plot([e, e], [-0.12, 0.12], color=F.INK, lw=1.4)
        ax.text(
            e, -0.42, rf"$10^{{{e}}}$", ha="center", va="top", color=F.INK, fontsize=11
        )

    # 文字基準高度：第 1 層、第 2 層
    ytxt = {1: 0.62, 2: 1.30}
    for e, name, col, lev, dx in items:
        up = 1 if lev > 0 else -1
        ax.plot([e], [0], "o", color=col, ms=7, zorder=5)
        ty = up * ytxt[abs(lev)]
        # 引線從圓點拉到文字附近
        ax.plot([e, e + dx], [0, ty - up * 0.16], color=col, lw=0.9, zorder=3)
        ax.text(
            e + dx,
            ty,
            name,
            ha="center",
            va="bottom" if up > 0 else "top",
            color=col,
            fontsize=11,
            rotation=0,
        )

    ax.text(29.0, -0.78, "長度 (m)", ha="right", va="top", color=F.INK, fontsize=12)
    ax.set_title("大自然的長度尺度（對數軸，每格 = 10 倍）", fontsize=14)
    ax.axis("off")
    fig.tight_layout()
    F.save_to(fig, CH, "必物-1-數量級尺度")


def fig_si():
    """SI 七個基本量與單位的列表示意。"""
    fig, ax = F.schematic(8.6, 5.2)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 8.6)

    rows = [
        ("長度", "length", "公尺", "m"),
        ("質量", "mass", "公斤", "kg"),
        ("時間", "time", "秒", "s"),
        ("電流", "electric current", "安培", "A"),
        ("溫度", "temperature", "克耳文", "K"),
        ("物量", "amount of substance", "莫耳", "mol"),
        ("發光強度", "luminous intensity", "燭光", "cd"),
    ]
    colmap = [F.BLUE, F.RED, F.GREEN, F.AMBER, F.PURPLE, "#0e7490", "#9a6700"]

    # 標題列
    y0 = 7.7
    ax.text(
        2.0, y0, "基本物理量", ha="center", fontsize=13, color=F.INK, fontweight="bold"
    )
    ax.text(
        6.4, y0, "SI 基本單位", ha="center", fontsize=13, color=F.INK, fontweight="bold"
    )
    ax.text(8.6, y0, "符號", ha="center", fontsize=13, color=F.INK, fontweight="bold")
    ax.plot([0.3, 9.7], [7.35, 7.35], color=F.INK, lw=1.6)

    dy = 0.95
    for i, (zh, en, uzh, usym) in enumerate(rows):
        yy = 6.7 - i * dy
        col = colmap[i]
        # 量名色塊
        ax.add_patch(
            FancyBboxPatch(
                (0.45, yy - 0.32),
                3.1,
                0.64,
                boxstyle="round,pad=0.02,rounding_size=0.10",
                facecolor=col,
                edgecolor="none",
                alpha=0.13,
                zorder=1,
            )
        )
        ax.text(0.7, yy, zh, ha="left", va="center", fontsize=13, color=col, zorder=2)
        ax.text(
            3.45,
            yy - 0.02,
            en,
            ha="right",
            va="center",
            fontsize=8.5,
            color="#888",
            zorder=2,
        )
        ax.text(6.4, yy, uzh, ha="center", va="center", fontsize=12.5, color=F.INK)
        ax.add_patch(
            Circle((8.6, yy), 0.30, facecolor=col, alpha=0.16, edgecolor=col, lw=1.2)
        )
        ax.text(
            8.6,
            yy,
            usym,
            ha="center",
            va="center",
            fontsize=12.5,
            color=col,
            fontweight="bold",
        )

    ax.set_title("國際單位制（SI）的七個基本量與基本單位", fontsize=14)
    fig.tight_layout()
    F.save_to(fig, CH, "必物-1-SI基本量")


def fig_accuracy():
    """準確度 vs 精密度：四象限靶心圖。"""
    rng = np.random.default_rng(3)
    fig, axes = plt.subplots(1, 4, figsize=(10.2, 3.2))

    # (標題, 偏移(bias), 散布(spread))
    cases = [
        ("低準確度\n低精密度", (1.05, 0.75), 0.55),
        ("高準確度\n低精密度", (0.0, 0.0), 0.62),
        ("低準確度\n高精密度", (1.0, 0.7), 0.13),
        ("高準確度\n高精密度", (0.0, 0.0), 0.13),
    ]
    for ax, (title, bias, spread) in zip(axes, cases):
        # 靶環
        for r, c in [
            (1.6, "#eef1f5"),
            (1.1, "#dbe7ff"),
            (0.6, "#bcd3ff"),
            (0.18, F.RED),
        ]:
            ax.add_patch(
                Circle((0, 0), r, facecolor=c, edgecolor="#aab4c2", lw=0.8, zorder=1)
            )
        # 彈著點
        n = 7
        x = rng.normal(bias[0], spread, n)
        y = rng.normal(bias[1], spread, n)
        ax.scatter(
            x, y, s=42, color=F.INK, edgecolors="white", linewidths=0.8, zorder=5
        )
        ax.set_xlim(-2.0, 2.0)
        ax.set_ylim(-2.0, 2.0)
        ax.set_aspect("equal")
        ax.set_xticks([])
        ax.set_yticks([])
        for s in ("top", "right", "bottom", "left"):
            ax.spines[s].set_color("#aab4c2")
        ax.set_title(title, fontsize=11.5)

    fig.suptitle("準確度（離靶心多近）vs 精密度（彼此多集中）", fontsize=14, y=1.04)
    fig.tight_layout()
    F.save_to(fig, CH, "必物-1-有效數字")


if __name__ == "__main__":
    fig_scale()
    fig_si()
    fig_accuracy()
    print("done.")
