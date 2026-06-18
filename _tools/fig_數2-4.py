# -*- coding: utf-8 -*-
"""產生「數2-4 數據分析」的圖，輸出到該章 sources/。
重繪：  .venv/bin/python _tools/fig_數2-4.py
資料圖：F.canvas() + ax.scatter/ax.bar + F.clean_grid(ax)。
注意：mathtext 不支援 \\dfrac/\\tfrac（用 \\frac）；圖內中文不要放 $...$。
"""

import os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import matplotlib.pyplot as plt
import figlib as F

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CH = os.path.join(ROOT, "數學", "數學一下（必修·第二冊）", "數2-4 數據分析")


def fig_std():
    """兩組平均數相同但離散程度不同的資料，並標出各自的標準差範圍。"""
    fig, axes = plt.subplots(1, 2, figsize=(11.2, 4.4), sharey=True)

    # 兩組資料：平均數都是 50
    A = np.array([48, 49, 50, 51, 52])  # 集中
    B = np.array([30, 40, 50, 60, 70])  # 分散
    groups = [
        (axes[0], A, F.BLUE, "甲組：集中"),
        (axes[1], B, F.RED, "乙組：分散"),
    ]

    for ax, data, col, name in groups:
        mean = data.mean()
        sd = data.std()  # 母體標準差
        x = np.arange(1, len(data) + 1)
        ax.bar(x, data, color=col, alpha=0.30, width=0.55, zorder=2)
        ax.scatter(x, data, color=col, s=55, zorder=4)
        # 平均線
        ax.axhline(mean, color=F.INK, lw=1.8, zorder=3)
        ax.text(
            len(data) + 0.35,
            mean,
            "平均 50",
            color=F.INK,
            fontsize=11,
            ha="left",
            va="center",
        )
        # 標準差帶 mean ± sd
        ax.axhspan(mean - sd, mean + sd, color=col, alpha=0.10, zorder=1)
        ax.axhline(mean + sd, color=col, lw=1.2, ls="--", zorder=3)
        ax.axhline(mean - sd, color=col, lw=1.2, ls="--", zorder=3)
        ax.text(
            0.6,
            mean + sd + 1.5,
            "標準差 s = %.1f" % sd,
            color=col,
            fontsize=11.5,
            ha="left",
            va="bottom",
        )
        ax.set_xticks(x)
        ax.set_xlim(0.3, len(data) + 1.4)
        ax.set_ylim(20, 80)
        ax.set_xlabel("資料編號")
        ax.set_title(name, fontsize=12.5, color=col)
        F.clean_grid(ax)

    axes[0].set_ylabel("數值")
    fig.suptitle("平均數相同，標準差量「離散程度」", fontsize=14, y=1.02)
    fig.tight_layout()
    F.save_to(fig, CH, "數2-4-標準差")


def fig_scatter_corr():
    """正相關、負相關、無相關三張散布圖。"""
    rng = np.random.default_rng(7)
    n = 30
    x = rng.uniform(2, 18, n)

    pos = x * 0.9 + rng.normal(0, 1.6, n) + 2  # 正相關
    neg = -x * 0.9 + rng.normal(0, 1.6, n) + 20  # 負相關
    non = rng.uniform(2, 18, n)  # 無相關

    fig, axes = plt.subplots(1, 3, figsize=(12.6, 4.2), sharex=True, sharey=True)
    cases = [
        (axes[0], pos, F.BLUE, "正相關 r > 0", "x 增大，y 傾向增大"),
        (axes[1], neg, F.RED, "負相關 r < 0", "x 增大，y 傾向減小"),
        (axes[2], non, F.AMBER, "近乎無相關 r ≈ 0", "看不出隨 x 的趨勢"),
    ]
    for ax, y, col, name, sub in cases:
        ax.scatter(x, y, color=col, s=42, alpha=0.85, zorder=4)
        ax.set_xlim(0, 20)
        ax.set_ylim(0, 22)
        ax.set_xlabel("x")
        ax.set_title(name + "\n" + sub, fontsize=12, color=col)
        F.clean_grid(ax)
    axes[0].set_ylabel("y")
    fig.suptitle("散布圖：點的「整體走向」就是相關的方向", fontsize=14, y=1.04)
    fig.tight_layout()
    F.save_to(fig, CH, "數2-4-散布圖相關")


def fig_best_fit():
    """散布點加上最適直線（最小平方迴歸線），標出殘差。"""
    x = np.array([1, 2, 3, 4, 5, 6, 7, 8], dtype=float)
    y = np.array([2.1, 3.9, 4.2, 6.1, 5.8, 7.9, 8.2, 9.5])

    # 最小平方迴歸線
    xb, yb = x.mean(), y.mean()
    b = ((x - xb) * (y - yb)).sum() / ((x - xb) ** 2).sum()
    a = yb - b * xb
    yhat = a + b * x

    fig, ax = F.canvas(7.2, 5.2)
    # 殘差（垂直虛線）
    for xi, yi, yh in zip(x, y, yhat):
        ax.plot([xi, xi], [yi, yh], color=F.AMBER, lw=1.3, ls=":", zorder=2)
    # 資料點
    ax.scatter(x, y, color=F.BLUE, s=58, zorder=5, label="資料點")
    # 迴歸線
    xs = np.array([0.4, 8.6])
    ax.plot(xs, a + b * xs, color=F.RED, lw=2.4, zorder=4, label="最適直線")
    # 平均點
    ax.scatter([xb], [yb], color=F.INK, s=70, marker="X", zorder=6)
    ax.text(xb + 0.15, yb - 0.7, "平均點", color=F.INK, fontsize=11, ha="left")
    # 方程式標註（mathtext 用 \frac 不可用 \dfrac；此處純文字即可）
    ax.text(
        0.6,
        8.7,
        "y = %.2f + %.2fx" % (a, b),
        color=F.RED,
        fontsize=13,
        ha="left",
        va="center",
        bbox=dict(boxstyle="round,pad=0.3", fc="white", ec=F.RED, lw=1.3),
    )
    ax.text(
        5.2,
        2.0,
        "橘色虛線 = 殘差\n(點到直線的鉛直距離)",
        color=F.AMBER,
        fontsize=10.5,
        ha="left",
        va="center",
    )
    ax.set_xlim(0, 9)
    ax.set_ylim(0, 11)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.legend(loc="lower right", frameon=False, fontsize=11)
    ax.set_title("最適直線：使「殘差平方和」最小", fontsize=14)
    F.clean_grid(ax)
    F.save_to(fig, CH, "數2-4-最適直線")


def fig_boxplot():
    """盒鬚圖：以例題 4-2a 的 11 筆資料標出 Q1、Q2、Q3、IQR 與全距的對照。"""
    data = np.array([3, 5, 6, 8, 9, 10, 12, 13, 15, 18, 21], dtype=float)
    q1, q2, q3 = 6.0, 10.0, 15.0  # 高中作法（中位數切半、左右半取中位數）
    lo, hi = data.min(), data.max()  # 3, 21
    iqr = q3 - q1  # 9
    rng = hi - lo  # 18

    fig, ax = F.canvas(9.4, 4.6)

    yc = 0.0  # 盒鬚圖中心高度
    bh = 0.42  # 盒子半高

    # ---- 盒子（Q1 到 Q3）----
    from matplotlib.patches import Rectangle

    ax.add_patch(
        Rectangle(
            (q1, yc - bh),
            iqr,
            2 * bh,
            facecolor=F.BLUE,
            alpha=0.18,
            edgecolor=F.BLUE,
            lw=1.8,
            zorder=3,
        )
    )
    # 中位數線（Q2）
    ax.plot([q2, q2], [yc - bh, yc + bh], color=F.RED, lw=2.6, zorder=5)
    # ---- 鬚（whisker）到最小、最大值 ----
    ax.plot([lo, q1], [yc, yc], color=F.INK, lw=1.6, zorder=4)
    ax.plot([q3, hi], [yc, yc], color=F.INK, lw=1.6, zorder=4)
    for xv in (lo, hi):
        ax.plot(
            [xv, xv], [yc - bh * 0.55, yc + bh * 0.55], color=F.INK, lw=1.6, zorder=4
        )

    # ---- 原始資料點（沿底部排開，看出盒鬚圖如何摘要）----
    ax.scatter(
        data, np.full_like(data, yc - 1.05), color=F.INK, s=30, alpha=0.7, zorder=4
    )
    for xv in data:
        ax.plot([xv, xv], [yc - 1.0, yc - bh], color=F.GRID, lw=0.8, ls=":", zorder=1)
    ax.text(
        lo,
        yc - 1.42,
        "原始 11 筆資料（由小到大）",
        color=F.INK,
        fontsize=10.5,
        ha="left",
        va="top",
    )

    # ---- 五數標註（最小、Q1、Q2、Q3、最大）----
    marks = [
        (lo, "最小 3", F.INK),
        (q1, "Q1 = 6", F.BLUE),
        (q2, "Q2（中位數）= 10", F.RED),
        (q3, "Q3 = 15", F.BLUE),
        (hi, "最大 21", F.INK),
    ]
    for i, (xv, txt, col) in enumerate(marks):
        dy = bh + 0.22 if i % 2 == 0 else bh + 0.72
        ax.text(xv, yc + dy, txt, color=col, fontsize=11, ha="center", va="bottom")
        ax.plot(
            [xv, xv], [yc + bh, yc + dy - 0.05], color=col, lw=0.8, ls="--", zorder=2
        )

    # ---- IQR 區間標尺（盒子下方）----
    ybar = yc - 0.62
    ax.annotate(
        "",
        xy=(q1, ybar),
        xytext=(q3, ybar),
        arrowprops=dict(arrowstyle="<->", color=F.BLUE, lw=1.6),
    )
    ax.text(
        q2,
        ybar - 0.04,
        "IQR = Q3 − Q1 = 9",
        color=F.BLUE,
        fontsize=11,
        ha="center",
        va="top",
    )

    # ---- 全距標尺（最上方）----
    ytop = yc + bh + 1.18
    ax.annotate(
        "",
        xy=(lo, ytop),
        xytext=(hi, ytop),
        arrowprops=dict(arrowstyle="<->", color=F.AMBER, lw=1.6),
    )
    ax.text(
        (lo + hi) / 2,
        ytop + 0.04,
        "全距 = 最大 − 最小 = 18",
        color=F.AMBER,
        fontsize=11,
        ha="center",
        va="bottom",
    )

    ax.set_xlim(0, 24)
    ax.set_ylim(yc - 1.75, ytop + 0.6)
    ax.set_yticks([])
    ax.set_xlabel("數值")
    ax.spines["left"].set_visible(False)
    ax.set_title("盒鬚圖：用五個數摘要一組資料的分布與離散", fontsize=14)
    ax.grid(True, axis="x", color=F.GRID, lw=0.9)
    ax.set_axisbelow(True)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    F.save_to(fig, CH, "數2-4-盒鬚圖")


def fig_standardize():
    """標準化示意：原始分布與標準化後（平均0、標準差1）的對照，標出 z 分數。"""
    fig, axes = plt.subplots(1, 2, figsize=(11.4, 4.4))

    # 左：原始資料的直方圖（平均 70、標準差 8）
    rng = np.random.default_rng(3)
    raw = rng.normal(70, 8, 400)
    ax = axes[0]
    ax.hist(raw, bins=18, color=F.BLUE, alpha=0.35, zorder=2)
    ax.axvline(70, color=F.INK, lw=1.8, zorder=3)
    ax.text(
        70.5,
        ax.get_ylim()[1] * 0.92,
        "平均 70",
        color=F.INK,
        fontsize=11,
        ha="left",
        va="top",
    )
    # 標一個原始分數 86
    ax.axvline(86, color=F.RED, lw=2.0, zorder=4)
    ax.text(
        86.5,
        ax.get_ylim()[1] * 0.70,
        "x = 86",
        color=F.RED,
        fontsize=11.5,
        ha="left",
        va="top",
    )
    ax.set_xlabel("原始分數")
    ax.set_ylabel("人數")
    ax.set_title("原始分布：平均 70、標準差 8", fontsize=12)
    F.clean_grid(ax)

    # 右：z 分數軸（標準化後），標出對應位置
    ax = axes[1]
    z = (raw - 70) / 8
    ax.hist(z, bins=18, color=F.GREEN, alpha=0.35, zorder=2)
    ax.axvline(0, color=F.INK, lw=1.8, zorder=3)
    ax.text(
        0.08,
        ax.get_ylim()[1] * 0.92,
        "平均 0",
        color=F.INK,
        fontsize=11,
        ha="left",
        va="top",
    )
    ax.axvline(2, color=F.RED, lw=2.0, zorder=4)
    ax.text(
        2.08,
        ax.get_ylim()[1] * 0.70,
        "z = +2",
        color=F.RED,
        fontsize=11.5,
        ha="left",
        va="top",
    )
    ax.set_xlabel("標準分數 z")
    ax.set_ylabel("人數")
    ax.set_xlim(-3.5, 3.5)
    ax.set_title("標準化後：平均 0、標準差 1", fontsize=12)
    F.clean_grid(ax)

    fig.suptitle(
        "標準化：z = (x − 平均) / 標準差，把不同尺度化為同一把尺", fontsize=13.5, y=1.03
    )
    fig.tight_layout()
    F.save_to(fig, CH, "數2-4-標準化")


if __name__ == "__main__":
    fig_std()
    fig_scatter_corr()
    fig_best_fit()
    fig_standardize()
    fig_boxplot()
    print("done.")
