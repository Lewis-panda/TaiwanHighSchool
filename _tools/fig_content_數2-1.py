# -*- coding: utf-8 -*-
"""重生「數2-1 數列與級數」學生講義的章內 SVG。"""

if __name__ == "__main__" and __import__("sys").argv[1:]:
    raise SystemExit("本腳本不接受參數；直接執行即可重生數2-1 章內 SVG。")

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Polygon, Rectangle
import numpy as np

import figlib as F


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHAPTER = os.path.join(ROOT, "content", "必修數學", "數2-1")

FIGURE_OUTPUTS = (
    ("fig_sequence_points", "數2-1-數列是離散對應.svg"),
    ("fig_arithmetic_steps", "數2-1-等差位移.svg"),
    ("fig_geometric_steps", "數2-1-等比倍率.svg"),
    ("fig_recurrence_flow", "數2-1-遞迴狀態.svg"),
    ("fig_induction_chain", "數2-1-歸納法鏈條.svg"),
    ("fig_arithmetic_pairing", "數2-1-等差級數配對.svg"),
    ("fig_geometric_cancellation", "數2-1-等比級數錯位相減.svg"),
    ("fig_partial_sums", "數2-1-部分和成長.svg"),
    ("fig_sum_decomposition", "數2-1-拆項求和.svg"),
    ("fig_interest_growth", "數2-1-單利複利比較.svg"),
    ("fig_annuity_timeline", "數2-1-定期存款時間軸.svg"),
)


def _save(fig, filename):
    stem, extension = os.path.splitext(filename)
    if extension != ".svg" or not stem.startswith("數2-1-"):
        raise AssertionError("輸出檔名必須是數2-1 章內 SVG")
    return F.save_to(fig, CHAPTER, stem, output_subdir="assets", write_pdf=False)


def fig_sequence_points():
    n = np.arange(1, 9)
    arithmetic = 2 + 3 * (n - 1)
    geometric = 2 * 1.5 ** (n - 1)
    assert np.all(np.diff(arithmetic) == 3)
    assert np.allclose(geometric[1:] / geometric[:-1], 1.5)

    fig, axes = plt.subplots(1, 2, figsize=(11.0, 4.6))
    for ax, values, title, color in (
        (axes[0], arithmetic, r"$a_n=2+3(n-1)$", F.BLUE),
        (axes[1], geometric, r"$b_n=2(1.5)^{n-1}$", F.GREEN),
    ):
        ax.vlines(n, 0, values, color=F.GRID, lw=1.4)
        ax.scatter(n, values, s=62, color=color, zorder=4)
        ax.plot(n, values, color=color, lw=1.2, alpha=.45, ls="--")
        ax.set_xticks(n)
        ax.set_xlabel("正整數索引 $n$")
        ax.set_ylabel("第 $n$ 項")
        ax.set_title(title, fontsize=13)
        F.clean_grid(ax)
    fig.suptitle("數列把每個正整數索引對應到一個數值", fontsize=15)
    fig.tight_layout(rect=(0, 0, 1, .91))
    return _save(fig, "數2-1-數列是離散對應.svg")


def fig_arithmetic_steps():
    n = np.arange(1, 7)
    a = 5 + (n - 1) * 3
    assert a[-1] == 5 + 5 * 3 == 20

    fig, ax = plt.subplots(figsize=(10.8, 4.3))
    ax.set_xlim(.4, 6.6)
    ax.set_ylim(0, 1.7)
    ax.axis("off")
    for index, (x, value) in enumerate(zip(n, a)):
        box = FancyBboxPatch((x - .35, .55), .7, .48, boxstyle="round,pad=0.04",
                             facecolor="#f4f7fb", edgecolor=F.BLUE, lw=1.8)
        ax.add_patch(box)
        ax.text(x, .79, rf"$a_{{{index+1}}}={value}$", ha="center", va="center", fontsize=12)
        if index < len(n) - 1:
            ax.annotate("", xy=(x + .62, .79), xytext=(x + .38, .79),
                        arrowprops=dict(arrowstyle="->", color=F.GREEN, lw=1.8))
            ax.text(x + .5, 1.15, "$+3$", color=F.GREEN, ha="center", fontsize=11)
    ax.annotate("$5$ 個公差", xy=(6, .25), xytext=(1, .25),
                arrowprops=dict(arrowstyle="<->", color=F.AMBER, lw=1.8),
                ha="center", va="bottom", color=F.AMBER, fontsize=12)
    ax.set_title(r"從 $a_1$ 到 $a_n$ 經過 $n-1$ 次固定加法", fontsize=15)
    fig.tight_layout()
    return _save(fig, "數2-1-等差位移.svg")


def fig_geometric_steps():
    n = np.arange(1, 6)
    a = 81 * (1 / 3) ** (n - 1)
    assert np.allclose(a, [81, 27, 9, 3, 1])
    assert np.allclose(a[1:] / a[:-1], 1 / 3)

    fig, ax = plt.subplots(figsize=(10.8, 4.4))
    ax.set_xlim(.4, 5.6)
    ax.set_ylim(0, 1.8)
    ax.axis("off")
    sizes = 115 + 3.5 * a
    ax.scatter(n, np.full_like(n, .78, dtype=float), s=sizes, color=F.BLUE, alpha=.88)
    for index, (x, value) in enumerate(zip(n, a)):
        ax.text(x, .78, f"{value:g}", ha="center", va="center", color="white", fontsize=11)
        ax.text(x, .28, rf"$a_{{{index+1}}}$", ha="center", color=F.INK, fontsize=11)
        if index < len(n) - 1:
            ax.annotate("", xy=(x + .72, 1.30), xytext=(x + .28, 1.30),
                        arrowprops=dict(arrowstyle="->", color=F.GREEN, lw=1.8))
            ax.text(x + .5, 1.48, r"$\times\frac{1}{3}$", color=F.GREEN, ha="center", fontsize=11)
    ax.set_title(r"等比數列每一步乘同一倍率；到第 $n$ 項共乘 $n-1$ 次", fontsize=15)
    fig.tight_layout()
    return _save(fig, "數2-1-等比倍率.svg")


def fig_recurrence_flow():
    values = [1]
    for _ in range(4):
        values.append(2 * values[-1] + 1)
    assert values == [1, 3, 7, 15, 31]

    fig, ax = plt.subplots(figsize=(10.8, 4.2))
    ax.set_xlim(.4, 5.6)
    ax.set_ylim(0, 2)
    ax.axis("off")
    for i, value in enumerate(values, start=1):
        box = FancyBboxPatch((i - .34, .62), .68, .54, boxstyle="round,pad=0.05",
                             facecolor="#eef5ff", edgecolor=F.BLUE, lw=1.8)
        ax.add_patch(box)
        ax.text(i, .89, rf"$a_{i}={value}$", ha="center", va="center", fontsize=12)
        if i < len(values):
            ax.annotate("", xy=(i + .62, .89), xytext=(i + .38, .89),
                        arrowprops=dict(arrowstyle="->", color=F.GREEN, lw=1.8))
            ax.text(i + .5, 1.27, r"$\times2,+1$", ha="center", color=F.GREEN, fontsize=10)
    ax.text(.63, .30, "初始值", color=F.AMBER, fontsize=11)
    ax.text(2.25, .30, "同一遞迴規則反覆更新狀態", color=F.INK, fontsize=11)
    ax.set_title(r"$a_1=1, a_n=2a_{n-1}+1$：初始值與規則共同決定數列", fontsize=15)
    fig.tight_layout()
    return _save(fig, "數2-1-遞迴狀態.svg")


def fig_induction_chain():
    fig, ax = plt.subplots(figsize=(11.0, 4.2))
    ax.set_xlim(.3, 6.7)
    ax.set_ylim(0, 2.1)
    ax.axis("off")
    xs = np.arange(1, 7)
    for i, x in enumerate(xs, start=1):
        color = F.AMBER if i == 1 else F.BLUE
        ax.add_patch(Rectangle((x - .16, .47), .32, .86, facecolor=color, edgecolor=F.INK, lw=1.0))
        ax.text(x, .90, rf"$P({i})$", color="white", ha="center", va="center", fontsize=10,
                rotation=90)
        if i < len(xs):
            ax.annotate("", xy=(x + .65, 1.53), xytext=(x + .25, 1.53),
                        arrowprops=dict(arrowstyle="->", color=F.GREEN, lw=1.7))
    ax.text(1, .20, "基礎步：證明 $P(1)$", ha="center", color=F.AMBER, fontsize=11)
    ax.text(4.2, .20, "歸納步：任意 $k$，由 $P(k)$ 推得 $P(k+1)$", ha="center",
            color=F.GREEN, fontsize=11)
    ax.set_title("基礎步提供起點，歸納步把成立範圍逐項推進", fontsize=15)
    fig.tight_layout()
    return _save(fig, "數2-1-歸納法鏈條.svg")


def fig_arithmetic_pairing():
    seq = np.array([2, 5, 8, 11, 14])
    rev = seq[::-1]
    pair = seq + rev
    assert np.all(pair == 16)
    assert seq.sum() == 40 == len(seq) * 16 / 2

    fig, ax = plt.subplots(figsize=(10.5, 4.8))
    ax.axis("off")
    ax.set_xlim(-.7, 5.3)
    ax.set_ylim(-.4, 3.5)
    for j, (row, label, color) in enumerate(((seq, "$S_5$", F.BLUE), (rev, "$S_5$ 反向", F.GREEN))):
        y = 2.55 - j * .85
        ax.text(-.50, y, label, ha="right", va="center", fontsize=12, color=color)
        for i, value in enumerate(row):
            ax.text(i, y, f"{value}", ha="center", va="center", fontsize=15, color=color)
    ax.plot([-.3, 4.3], [1.30, 1.30], color=F.INK, lw=1.5)
    for i, value in enumerate(pair):
        ax.text(i, .88, f"{value}", ha="center", fontsize=15, color=F.AMBER)
    ax.text(2, .23, r"每欄都是 $a_1+a_5=16$，共有 $5$ 欄", ha="center", fontsize=12)
    ax.text(2, 3.15, r"$2S_5=5(2+14)$，所以 $S_5=\frac{5(2+14)}{2}=40$",
            ha="center", fontsize=14)
    fig.tight_layout()
    return _save(fig, "數2-1-等差級數配對.svg")


def fig_geometric_cancellation():
    seq = np.array([3, 6, 12, 24, 48])
    r = 2
    assert seq.sum() == 93
    assert r * seq.sum() - seq.sum() == 96 - 3

    fig, ax = plt.subplots(figsize=(11.0, 4.8))
    ax.axis("off")
    ax.set_xlim(-1.25, 6.1)
    ax.set_ylim(-.3, 3.8)
    xs = np.arange(5)
    ax.text(-.35, 2.72, "$S_5$", ha="right", fontsize=13, color=F.BLUE)
    ax.text(-.35, 1.86, "$2S_5$", ha="right", fontsize=13, color=F.GREEN)
    for x, value in zip(xs, seq):
        ax.text(x, 2.72, f"{value}", ha="center", fontsize=15, color=F.BLUE)
    for x, value in zip(xs + 1, r * seq):
        ax.text(x, 1.86, f"{value}", ha="center", fontsize=15, color=F.GREEN)
    for x in range(1, 5):
        ax.add_patch(Rectangle((x - .30, 1.60), .60, 1.48, facecolor=F.GREEN, alpha=.08,
                               edgecolor="none"))
    ax.plot([-.55, 5.45], [1.33, 1.33], color=F.INK, lw=1.5)
    ax.text(2.5, .87, r"$2S_5-S_5=96-3$", ha="center", fontsize=14, color=F.AMBER)
    ax.text(2.5, .28, r"中間各項因錯位對齊而消去，$S_5=93$", ha="center", fontsize=12)
    ax.set_title("等比級數乘公比後錯開一格，相減只留下首尾", fontsize=15)
    fig.tight_layout()
    return _save(fig, "數2-1-等比級數錯位相減.svg")


def fig_partial_sums():
    n = np.arange(1, 9)
    s_arith = n * (3 * n + 1) / 2
    s_geo = 2 * (2**n - 1)
    assert np.allclose(s_arith, np.cumsum(2 + 3 * (n - 1)))
    assert np.allclose(s_geo, np.cumsum(2 * 2 ** (n - 1)))

    fig, ax = plt.subplots(figsize=(9.8, 5.4))
    ax.plot(n, s_arith, marker="o", lw=2.4, color=F.BLUE,
            label=r"等差：$a_n=3n-1$")
    ax.plot(n, s_geo, marker="o", lw=2.4, color=F.GREEN,
            label=r"等比：$b_n=2^n$")
    ax.set_xticks(n)
    ax.set_xlabel("項數 $n$")
    ax.set_ylabel("部分和 $S_n$")
    ax.legend(frameon=False)
    ax.set_title("部分和把前 $n$ 項累積成另一個數列", fontsize=15)
    F.clean_grid(ax)
    fig.tight_layout()
    return _save(fig, "數2-1-部分和成長.svg")


def fig_sum_decomposition():
    k = np.arange(1, 11)
    square = k**2
    linear = 2 * k
    total = k * (k + 2)
    assert np.all(square + linear == total)
    assert total.sum() == 495

    fig, ax = plt.subplots(figsize=(10.2, 5.4))
    ax.bar(k, square, color=F.BLUE, label=r"$k^2$")
    ax.bar(k, linear, bottom=square, color=F.GREEN, label=r"$2k$")
    ax.set_xticks(k)
    ax.set_xlabel("第 $k$ 項")
    ax.set_ylabel(r"$k(k+2)$")
    ax.legend(frameon=False)
    ax.text(1.0, 105, r"$\sum_{k=1}^{10}k(k+2)=\sum k^2+2\sum k=495$",
            fontsize=13, color=F.INK)
    ax.set_title("先拆成平方和與一次和，再套用基本公式", fontsize=15)
    F.clean_grid(ax)
    fig.tight_layout()
    return _save(fig, "數2-1-拆項求和.svg")


def fig_interest_growth():
    principal, rate = 100000.0, .02
    n = np.arange(0, 21)
    simple = principal * (1 + n * rate)
    compound = principal * (1 + rate) ** n
    assert np.isclose(simple[10], 120000)
    assert np.isclose(compound[10], 121899.44199947573)
    assert np.all(compound[2:] > simple[2:])

    fig, ax = plt.subplots(figsize=(9.8, 5.4))
    ax.plot(n, simple, marker="o", ms=4, color=F.BLUE, lw=2.4, label="單利")
    ax.plot(n, compound, marker="o", ms=4, color=F.GREEN, lw=2.4, label="複利")
    ax.scatter([10, 10], [simple[10], compound[10]], color=[F.BLUE, F.GREEN], s=65, zorder=5)
    ax.annotate("第 10 期差額約 1,899 元", xy=(10, compound[10]), xytext=(11.2, 116000),
                arrowprops=dict(arrowstyle="->", color=F.AMBER), color=F.AMBER, fontsize=10)
    ax.set_xlabel("期數 $n$")
    ax.set_ylabel("本利和（元）")
    ax.legend(frameon=False)
    ax.set_title("單利每期增加固定利息；複利每期乘固定倍率", fontsize=15)
    F.clean_grid(ax)
    fig.tight_layout()
    return _save(fig, "數2-1-單利複利比較.svg")


def fig_annuity_timeline():
    periods = 5
    rate = .02
    factors = (1 + rate) ** np.arange(periods, 0, -1)
    assert np.allclose(factors[1:] / factors[:-1], 1 / (1 + rate))
    assert np.isclose(factors.sum(), (1 + rate) * ((1 + rate)**periods - 1) / rate)

    fig, ax = plt.subplots(figsize=(11.0, 4.6))
    ax.set_xlim(-.4, 5.6)
    ax.set_ylim(-.45, 2.3)
    ax.axis("off")
    ax.annotate("", xy=(5.35, .50), xytext=(-.10, .50),
                arrowprops=dict(arrowstyle="->", color=F.INK, lw=1.8))
    for month in range(periods + 1):
        ax.plot([month, month], [.40, .60], color=F.INK, lw=1.2)
        ax.text(month, .20, f"{month}", ha="center", fontsize=10)
    for deposit in range(periods):
        duration = periods - deposit
        ax.annotate("存入 $P$", xy=(deposit, .64), xytext=(deposit, 1.02 + .18 * (deposit % 2)),
                    ha="center", arrowprops=dict(arrowstyle="->", color=F.BLUE, lw=1.3),
                    color=F.BLUE, fontsize=10)
        ax.annotate("", xy=(periods, 1.55), xytext=(deposit, 1.55),
                    arrowprops=dict(arrowstyle="->", color=F.GREEN, lw=1.4))
        ax.text((deposit + periods) / 2, 1.66,
                rf"$P(1+r)^{{{duration}}}$", ha="center", fontsize=9, color=F.GREEN)
    ax.text(5.0, 2.08, r"期末合計 $P[(1+r)+(1+r)^2+\cdots+(1+r)^5]$",
            ha="right", fontsize=12, color=F.AMBER)
    ax.text(2.5, -.25, "每期初存款；越早存入，計息期數越多", ha="center", fontsize=11)
    ax.set_title("固定存款的終值是依計息期數排列的等比級數", fontsize=15)
    fig.tight_layout()
    return _save(fig, "數2-1-定期存款時間軸.svg")


if __name__ == "__main__":
    for entrypoint, filename in FIGURE_OUTPUTS:
        output = globals()[entrypoint]()
        if os.path.basename(output) != filename:
            raise AssertionError(f"{entrypoint} 輸出與 FIGURE_OUTPUTS 不一致")
