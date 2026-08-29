# -*- coding: utf-8 -*-
"""重生「數2-3 排列組合與機率」學生講義的章內 SVG。"""

if __name__ == "__main__" and __import__("sys").argv[1:]:
    raise SystemExit("本腳本不接受參數；直接執行即可重生數2-3 章內 SVG。")

import itertools
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyBboxPatch, Rectangle
import numpy as np

import figlib as F


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHAPTER = os.path.join(ROOT, "content", "必修數學", "數2-3")

FIGURE_OUTPUTS = (
    ("fig_logic_sets", "數2-3-邏輯與集合運算.svg"),
    ("fig_counting_tree", "數2-3-加法乘法樹.svg"),
    ("fig_inclusion_exclusion", "數2-3-取捨原理.svg"),
    ("fig_permutation_gaps", "數2-3-排列位置與空隙.svg"),
    ("fig_lattice_paths", "數2-3-相同物最短路.svg"),
    ("fig_permutation_combination", "數2-3-排列與組合比較.svg"),
    ("fig_binomial_choices", "數2-3-二項式選因子.svg"),
    ("fig_pascal_triangle", "數2-3-巴斯卡三角形.svg"),
    ("fig_dice_space", "數2-3-骰子樣本空間.svg"),
    ("fig_event_regions", "數2-3-事件區域.svg"),
    ("fig_expectation", "數2-3-期望值分布.svg"),
)


def _save(fig, filename):
    stem, extension = os.path.splitext(filename)
    if extension != ".svg" or not stem.startswith("數2-3-"):
        raise AssertionError("輸出檔名必須是數2-3 章內 SVG")
    return F.save_to(
        fig, CHAPTER, stem, output_subdir="assets", write_pdf=False
    )


def _rounded(ax, xy, width, height, text, *, edge=F.BLUE, face="#f4f7fb", fs=11):
    box = FancyBboxPatch(
        xy, width, height, boxstyle="round,pad=0.04",
        facecolor=face, edgecolor=edge, lw=1.6,
    )
    ax.add_patch(box)
    ax.text(xy[0] + width / 2, xy[1] + height / 2, text,
            ha="center", va="center", fontsize=fs)


def fig_logic_sets():
    universe = set(range(1, 13))
    a = {x for x in universe if x % 2 == 0}
    b = {x for x in universe if x % 3 == 0}
    assert a & b == {6, 12}
    assert len(a | b) == len(a) + len(b) - len(a & b) == 8
    assert universe - (a & b) == (universe - a) | (universe - b)

    fig, axes = plt.subplots(1, 2, figsize=(11.4, 4.8))
    ax = axes[0]
    ax.axis("off")
    ax.set_xlim(0, 6)
    ax.set_ylim(0, 4.2)
    rows = [
        ("敘述", "集合", "成立／落在"),
        (r"$P\wedge Q$", r"$A\cap B$", "同時"),
        (r"$P\vee Q$", r"$A\cup B$", "至少一個"),
        (r"$\neg P$", r"$A^c$", "補集"),
    ]
    for i, row in enumerate(rows):
        y = 3.55 - i * .85
        for j, value in enumerate(row):
            face = "#eaf2ff" if i == 0 else "white"
            ax.add_patch(Rectangle((.25 + 1.85 * j, y - .3), 1.75, .62,
                                   facecolor=face, edgecolor=F.GRID, lw=1.1))
            ax.text(1.12 + 1.85 * j, y, value, ha="center", va="center",
                    fontsize=11, color=F.INK)
    ax.set_title("邏輯連接詞與集合運算使用同一種區域結構", fontsize=14)

    ax = axes[1]
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_xlim(0, 6)
    ax.set_ylim(0, 4.4)
    ax.add_patch(Rectangle((.25, .25), 5.5, 3.65, fill=False, edgecolor=F.INK, lw=1.3))
    ax.add_patch(Circle((2.35, 2.05), 1.35, facecolor=F.BLUE, alpha=.17,
                        edgecolor=F.BLUE, lw=2))
    ax.add_patch(Circle((3.65, 2.05), 1.35, facecolor=F.GREEN, alpha=.17,
                        edgecolor=F.GREEN, lw=2))
    ax.text(1.45, 3.25, r"$A$：2 的倍數", color=F.BLUE, fontsize=11)
    ax.text(3.60, 3.25, r"$B$：3 的倍數", color=F.GREEN, fontsize=11)
    ax.text(1.72, 2.02, "2,4,8,10", ha="center", fontsize=10)
    ax.text(3.00, 2.02, "6,12", ha="center", fontsize=10, color=F.PURPLE)
    ax.text(4.30, 2.02, "3,9", ha="center", fontsize=10)
    ax.text(3.00, .55, "1,5,7,11", ha="center", fontsize=10)
    ax.text(.42, 3.60, r"$U=\{1,2,\ldots,12\}$", fontsize=10)
    ax.set_title(r"$A\cap B=\{6,12\}$，$|A\cup B|=8$", fontsize=14)
    fig.tight_layout()
    return _save(fig, "數2-3-邏輯與集合運算.svg")


def fig_counting_tree():
    mains = ["飯", "麵"]
    drinks = ["茶", "奶", "水"]
    leaves = list(itertools.product(mains, drinks))
    assert len(leaves) == len(mains) * len(drinks) == 6
    desserts = ["果", "糕"]
    assert len(leaves) + len(desserts) == 8

    fig, axes = plt.subplots(1, 2, figsize=(11.5, 4.8))
    ax = axes[0]
    ax.axis("off")
    ax.set_xlim(0, 6)
    ax.set_ylim(0, 4.4)
    ax.text(.55, 2.2, "套餐", ha="center", va="center", fontsize=12,
            bbox=dict(boxstyle="round,pad=.3", fc="#eef5ff", ec=F.BLUE))
    y_mains = [3.25, 1.15]
    for main, y in zip(mains, y_mains):
        ax.plot([.95, 2.0], [2.2, y], color=F.BLUE, lw=1.5)
        _rounded(ax, (2.0, y - .28), .85, .56, main, edge=F.BLUE)
        for j, drink in enumerate(drinks):
            yy = y + (j - 1) * .62
            ax.plot([2.85, 4.25], [y, yy], color=F.GREEN, lw=1.3)
            _rounded(ax, (4.25, yy - .23), .72, .46, drink, edge=F.GREEN, fs=10)
    ax.text(3.0, .25, r"每個主餐接 3 種飲料：$2\times3=6$", ha="center", fontsize=11)
    ax.set_title("連續完成兩個步驟：乘法原理", fontsize=14)

    ax = axes[1]
    ax.axis("off")
    ax.set_xlim(0, 6)
    ax.set_ylim(0, 4.4)
    _rounded(ax, (.65, 2.65), 1.25, .62, "6 種套餐", edge=F.BLUE)
    _rounded(ax, (.65, 1.25), 1.25, .62, "2 種甜點", edge=F.GREEN)
    ax.annotate("", xy=(4.2, 2.2), xytext=(2.05, 2.96),
                arrowprops=dict(arrowstyle="->", color=F.BLUE, lw=1.7))
    ax.annotate("", xy=(4.2, 2.2), xytext=(2.05, 1.56),
                arrowprops=dict(arrowstyle="->", color=F.GREEN, lw=1.7))
    _rounded(ax, (4.2, 1.86), 1.15, .68, "共 8 種", edge=F.AMBER, face="#fff7df")
    ax.text(3.0, .55, r"兩類選擇互不重疊：$6+2=8$", ha="center", fontsize=11)
    ax.set_title("從互斥類別擇一：加法原理", fontsize=14)
    fig.tight_layout()
    return _save(fig, "數2-3-加法乘法樹.svg")


def fig_inclusion_exclusion():
    n_a, n_b, n_ab = 30, 20, 10
    regions = (n_a - n_ab, n_ab, n_b - n_ab)
    assert regions == (20, 10, 10)
    assert sum(regions) == n_a + n_b - n_ab == 40

    fig, ax = F.schematic(9.8, 5.0)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5)
    ax.add_patch(Rectangle((.4, .35), 9.2, 4.2, fill=False, edgecolor=F.INK, lw=1.3))
    ax.add_patch(Circle((4.1, 2.4), 1.65, facecolor=F.BLUE, alpha=.18,
                        edgecolor=F.BLUE, lw=2.2))
    ax.add_patch(Circle((5.9, 2.4), 1.65, facecolor=F.GREEN, alpha=.18,
                        edgecolor=F.GREEN, lw=2.2))
    ax.text(3.25, 3.63, "4 的倍數：30 個", color=F.BLUE, fontsize=12, ha="center")
    ax.text(6.75, 3.63, "6 的倍數：20 個", color=F.GREEN, fontsize=12, ha="center")
    ax.text(3.45, 2.35, "20", ha="center", va="center", fontsize=18, color=F.BLUE)
    ax.text(5.00, 2.35, "10", ha="center", va="center", fontsize=18, color=F.PURPLE)
    ax.text(6.55, 2.35, "10", ha="center", va="center", fontsize=18, color=F.GREEN)
    ax.text(5.00, .72, r"交集是 12 的倍數；聯集 $=30+20-10=40$", ha="center", fontsize=12)
    ax.set_title("1 到 120 中，能被 4 或 6 整除的整數", fontsize=15)
    fig.tight_layout()
    return _save(fig, "數2-3-取捨原理.svg")


def fig_permutation_gaps():
    boys = 4
    girls = 3
    gaps = boys + 1
    arrangements = math.factorial(boys) * math.comb(gaps, girls) * math.factorial(girls)
    assert gaps == 5
    assert arrangements == 1440

    fig, ax = F.schematic(11.2, 4.3)
    ax.set_xlim(-.5, 10.5)
    ax.set_ylim(0, 4.2)
    bx = [1.6, 3.8, 6.0, 8.2]
    for i, x in enumerate(bx, start=1):
        _rounded(ax, (x - .38, 1.55), .76, .72, f"男{i}", edge=F.BLUE)
    gapx = [.45, 2.7, 4.9, 7.1, 9.35]
    for i, x in enumerate(gapx, start=1):
        ax.plot([x, x], [1.28, 2.55], color=F.AMBER, lw=2.4)
        ax.text(x, 2.78, f"空隙{i}", ha="center", color=F.AMBER, fontsize=10)
    ax.text(5, 3.55, r"先排 4 位男生：$4!$；再從 5 個空隙選 3 個並排列女生", ha="center", fontsize=13)
    ax.text(5, .72, r"$4!\binom{5}{3}3!=1440$ 種，女生自然兩兩不相鄰", ha="center", fontsize=13)
    fig.tight_layout()
    return _save(fig, "數2-3-排列位置與空隙.svg")


def fig_lattice_paths():
    steps = "RRRUU"
    paths = {"".join(p) for p in itertools.permutations(steps)}
    assert len(paths) == math.factorial(5) // (math.factorial(3) * math.factorial(2)) == 10

    fig, ax = plt.subplots(figsize=(8.8, 5.7))
    ax.set_aspect("equal")
    for x in range(4):
        ax.plot([x, x], [0, 2], color=F.GRID, lw=1.2)
    for y in range(3):
        ax.plot([0, 3], [y, y], color=F.GRID, lw=1.2)
    sample = "RURRU"
    x, y = 0, 0
    coords = [(x, y)]
    for step in sample:
        x += step == "R"
        y += step == "U"
        coords.append((x, y))
    xs, ys = zip(*coords)
    ax.plot(xs, ys, color=F.BLUE, lw=3.2, marker="o", zorder=3)
    for (x0, y0), step in zip(coords[:-1], sample):
        dx, dy = ((.5, .13) if step == "R" else (.14, .5))
        ax.text(x0 + dx, y0 + dy, step, color=F.AMBER, fontsize=11)
    ax.scatter([0, 3], [0, 2], s=90, color=[F.GREEN, F.RED], zorder=4)
    ax.text(-.18, -.20, "A", color=F.GREEN, fontsize=13)
    ax.text(3.08, 2.06, "B", color=F.RED, fontsize=13)
    ax.set_xlim(-.45, 3.45)
    ax.set_ylim(-.42, 2.48)
    ax.set_xticks(range(4))
    ax.set_yticks(range(3))
    ax.set_xlabel("向右共 3 步")
    ax.set_ylabel("向上共 2 步")
    ax.set_title(r"最短路徑是 R,R,R,U,U 的不同排列：$\frac{5!}{3!2!}=10$")
    fig.tight_layout()
    return _save(fig, "數2-3-相同物最短路.svg")


def fig_permutation_combination():
    people = "ABCD"
    unordered = list(itertools.combinations(people, 2))
    ordered = list(itertools.permutations(people, 2))
    assert len(unordered) == math.comb(4, 2) == 6
    assert len(ordered) == math.perm(4, 2) == 12
    assert len(ordered) == len(unordered) * math.factorial(2)

    fig, ax = plt.subplots(figsize=(10.8, 5.2))
    ax.axis("off")
    ax.set_xlim(0, 10.8)
    ax.set_ylim(0, 5.2)
    ax.text(2.2, 4.65, "選 2 人：組合", ha="center", fontsize=14, color=F.BLUE)
    ax.text(7.9, 4.65, "選正、副代表：排列", ha="center", fontsize=14, color=F.GREEN)
    for i, pair in enumerate(unordered):
        y = 4.0 - i * .58
        _rounded(ax, (.75, y - .20), 1.15, .42, "{" + ",".join(pair) + "}", edge=F.BLUE, fs=10)
        ax.annotate("", xy=(5.1, y), xytext=(2.05, y),
                    arrowprops=dict(arrowstyle="->", color=F.AMBER, lw=1.4))
        _rounded(ax, (5.2, y - .20), 1.25, .42, pair[0] + "→" + pair[1], edge=F.GREEN, fs=10)
        _rounded(ax, (7.05, y - .20), 1.25, .42, pair[1] + "→" + pair[0], edge=F.GREEN, fs=10)
    ax.text(9.55, 2.25, "每一組有\n$2!$ 種職務次序", ha="center", va="center", fontsize=10)
    ax.text(5.4, .20, r"$P^4_2=\binom{4}{2}\,2!=12$", ha="center", fontsize=14, color=F.PURPLE)
    fig.tight_layout()
    return _save(fig, "數2-3-排列與組合比較.svg")


def fig_binomial_choices():
    pairs = list(itertools.combinations(range(1, 6), 2))
    assert len(pairs) == math.comb(5, 2) == 10
    assert all(len(set(pair)) == 2 for pair in pairs)

    fig, ax = plt.subplots(figsize=(11.2, 5.2))
    ax.axis("off")
    ax.set_xlim(0, 11.2)
    ax.set_ylim(0, 5.2)
    ax.text(5.6, 4.65, r"在 $(x+y)^5$ 中形成 $x^3y^2$：選 2 個因子提供 $y$", ha="center", fontsize=14)
    for i in range(5):
        face = "#fff1c7" if i in (1, 4) else "#eaf2ff"
        edge = F.AMBER if i in (1, 4) else F.BLUE
        _rounded(ax, (1.05 + i * 1.85, 3.45), 1.25, .65,
                 f"因子 {i+1}\n" + ("取 y" if i in (1, 4) else "取 x"),
                 edge=edge, face=face, fs=10)
    for index, pair in enumerate(pairs):
        row, col = divmod(index, 5)
        text = f"{pair[0]},{pair[1]}"
        _rounded(ax, (1.0 + col * 1.85, 2.25 - row * .75), 1.10, .46,
                 text, edge=F.PURPLE, face="#f5f0ff", fs=10)
    ax.text(5.6, .30, r"兩個位置的選法共有 $\binom{5}{2}=10$，所以 $x^3y^2$ 的係數是 10",
            ha="center", fontsize=13)
    fig.tight_layout()
    return _save(fig, "數2-3-二項式選因子.svg")


def fig_pascal_triangle():
    rows = [[math.comb(n, k) for k in range(n + 1)] for n in range(7)]
    for n, row in enumerate(rows):
        assert sum(row) == 2 ** n
        if n >= 2:
            assert all(row[k] == rows[n - 1][k - 1] + rows[n - 1][k]
                       for k in range(1, n))

    fig, ax = plt.subplots(figsize=(9.4, 6.3))
    ax.axis("off")
    ax.set_xlim(-7, 7)
    ax.set_ylim(-6.7, .8)
    for n, row in enumerate(rows):
        for k, value in enumerate(row):
            x = 2 * k - n
            y = -n
            face = "#fff1c7" if (n, k) in {(5, 2), (4, 1), (4, 2)} else "#eef5ff"
            edge = F.AMBER if (n, k) in {(5, 2), (4, 1), (4, 2)} else F.BLUE
            ax.add_patch(Circle((x, y), .37, facecolor=face, edgecolor=edge, lw=1.3))
            ax.text(x, y, str(value), ha="center", va="center", fontsize=10)
        ax.text(-n - .72, -n, f"n={n}", ha="right", va="center", fontsize=9, color=F.INK)
    ax.plot([-2, -1], [-4.35, -4.65], color=F.AMBER, lw=1.8)
    ax.plot([0, -1], [-4.35, -4.65], color=F.AMBER, lw=1.8)
    ax.text(4.0, .15, r"$\binom{5}{2}=\binom{4}{1}+\binom{4}{2}=4+6=10$",
            ha="center", fontsize=10, color=F.AMBER)
    ax.set_title("巴斯卡三角形：上方相鄰兩數之和形成下一列", fontsize=15)
    fig.tight_layout()
    return _save(fig, "數2-3-巴斯卡三角形.svg")


def fig_dice_space():
    outcomes = [(i, j) for i in range(1, 7) for j in range(1, 7)]
    target = [(i, j) for i, j in outcomes if i + j == 7]
    assert len(outcomes) == 36
    assert len(target) == 6

    fig, ax = plt.subplots(figsize=(7.6, 6.5))
    for i, j in outcomes:
        face = F.BLUE if i + j == 7 else "#f7f9fb"
        ax.add_patch(Rectangle((i - .5, j - .5), 1, 1,
                               facecolor=face, edgecolor=F.GRID, lw=1.0))
    for i, j in outcomes:
        color = "white" if i + j == 7 else F.INK
        ax.text(i, j, f"({i},{j})", ha="center", va="center", fontsize=9, color=color)
    ax.set_xticks(range(1, 7))
    ax.set_yticks(range(1, 7))
    ax.set_xlim(.5, 6.5)
    ax.set_ylim(.5, 6.5)
    ax.set_xlabel("第一顆骰子")
    ax.set_ylabel("第二顆骰子")
    ax.set_title(r"兩顆公平骰子的 36 個等可能樣本點；點數和 7 有 6 點")
    ax.set_aspect("equal")
    fig.tight_layout()
    return _save(fig, "數2-3-骰子樣本空間.svg")


def fig_event_regions():
    space = {(i, j) for i in range(1, 7) for j in range(1, 7)}
    a = {(i, j) for i, j in space if i + j == 7}
    b = {(i, j) for i, j in space if i % 2 == 0}
    region_counts = (len(a - b), len(a & b), len(b - a), len(space - (a | b)))
    assert region_counts == (3, 3, 15, 15)
    assert sum(region_counts) == 36
    assert len(a | b) == len(a) + len(b) - len(a & b) == 21

    fig, ax = F.schematic(9.8, 5.1)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5)
    ax.add_patch(Rectangle((.35, .35), 9.3, 4.25, fill=False, edgecolor=F.INK, lw=1.4))
    ax.add_patch(Circle((4.1, 2.45), 1.62, facecolor=F.BLUE, alpha=.18,
                        edgecolor=F.BLUE, lw=2.1))
    ax.add_patch(Circle((5.9, 2.45), 1.62, facecolor=F.GREEN, alpha=.18,
                        edgecolor=F.GREEN, lw=2.1))
    ax.text(3.22, 3.68, r"$A$：點數和 7", color=F.BLUE, ha="center", fontsize=12)
    ax.text(6.78, 3.68, r"$B$：第一顆為偶數", color=F.GREEN, ha="center", fontsize=12)
    for x, text, color in ((3.42, "3", F.BLUE), (5.0, "3", F.PURPLE), (6.58, "15", F.GREEN)):
        ax.text(x, 2.40, text, ha="center", va="center", fontsize=18, color=color)
    ax.text(5.0, .58, "兩事件之外：15", ha="center", fontsize=12)
    ax.text(5.0, 4.82, r"$|A\cup B|=3+3+15=21$；$P(A\cup B)=21/36$", ha="center", fontsize=13)
    fig.tight_layout()
    return _save(fig, "數2-3-事件區域.svg")


def fig_expectation():
    payouts = np.array([-2, 2, 8], dtype=float)
    probabilities = np.array([1 / 2, 1 / 3, 1 / 6], dtype=float)
    contributions = payouts * probabilities
    assert math.isclose(probabilities.sum(), 1.0)
    assert math.isclose(contributions.sum(), 1.0)

    fig, axes = plt.subplots(1, 2, figsize=(11.0, 4.9))
    ax = axes[0]
    colors = [F.RED, F.BLUE, F.GREEN]
    ax.bar(["−2 元", "2 元", "8 元"], probabilities, color=colors, alpha=.82)
    for i, value in enumerate(probabilities):
        ax.text(i, value + .025, [r"$1/2$", r"$1/3$", r"$1/6$"][i], ha="center", fontsize=11)
    ax.set_ylim(0, .62)
    ax.set_ylabel("機率")
    ax.set_title("一次試驗的報酬分布")
    F.clean_grid(ax)
    ax = axes[1]
    ax.axis("off")
    ax.set_xlim(0, 5)
    ax.set_ylim(0, 4.2)
    lines = [
        (r"$(-2)\times\frac{1}{2}$", "= −1"),
        (r"$2\times\frac{1}{3}$", r"$=\frac{2}{3}$"),
        (r"$8\times\frac{1}{6}$", r"$=\frac{4}{3}$"),
    ]
    for i, (left, right) in enumerate(lines):
        y = 3.35 - i * .86
        ax.text(.45, y, left, fontsize=14, ha="left")
        ax.text(3.05, y, right, fontsize=14, ha="left", color=colors[i])
    ax.plot([.35, 4.55], [.78, .78], color=F.INK, lw=1.2)
    ax.text(2.5, .36, r"$E(X)=-1+\frac{2}{3}+\frac{4}{3}=1$ 元", ha="center", fontsize=15, color=F.PURPLE)
    ax.set_title("報酬乘機率後相加")
    fig.tight_layout()
    return _save(fig, "數2-3-期望值分布.svg")


def main():
    expected = {filename for _, filename in FIGURE_OUTPUTS}
    assert len(expected) == len(FIGURE_OUTPUTS) == 11
    written = set()
    for function_name, filename in FIGURE_OUTPUTS:
        function = globals().get(function_name)
        if not callable(function):
            raise AssertionError(f"找不到圖形入口：{function_name}")
        path = function()
        assert os.path.basename(path) == filename
        written.add(os.path.basename(path))
    assert written == expected


if __name__ == "__main__":
    main()
