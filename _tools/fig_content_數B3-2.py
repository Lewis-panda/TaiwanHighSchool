# -*- coding: utf-8 -*-
"""重生「數B3-2 按比例成長模型」學生講義的章內 SVG。"""

if __name__ == "__main__" and __import__("sys").argv[1:]:
    raise SystemExit("本腳本不接受參數；直接執行即可重生數B3-2 章內 SVG。")

import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle
import numpy as np

import figlib as F


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHAPTER = os.path.join(ROOT, "content", "數學B", "數B3-2")

FIGURE_OUTPUTS = (
    ("fig_fixed_change_ratio", "數B3-2-固定差與固定倍率.svg"),
    ("fig_exponential_family", "數B3-2-指數成長與衰退.svg"),
    ("fig_base_comparison", "數B3-2-指數底數比較.svg"),
    ("fig_exponential_roots", "數B3-2-指數換元與交點.svg"),
    ("fig_growth_decay_data", "數B3-2-成長衰退資料.svg"),
    ("fig_simple_compound", "數B3-2-單利與複利.svg"),
    ("fig_log_definition", "數B3-2-指數與對數對照.svg"),
    ("fig_log_laws", "數B3-2-對數律刻度.svg"),
    ("fig_e_convergence", "數B3-2-複利頻率與常數e.svg"),
    ("fig_log_scales", "數B3-2-對數尺度.svg"),
    ("fig_log_family", "數B3-2-對數成長與衰退.svg"),
    ("fig_log_equation", "數B3-2-對數方程與定義域.svg"),
    ("fig_inverse_reflection", "數B3-2-指數對數互為反函數.svg"),
    ("fig_log_linear_data", "數B3-2-指數資料取對數.svg"),
)


def _save(fig, filename):
    stem, extension = os.path.splitext(filename)
    if extension != ".svg" or not stem.startswith("數B3-2-"):
        raise AssertionError("輸出檔名必須是數B3-2 章內 SVG")
    return F.save_to(
        fig, CHAPTER, stem, output_subdir="assets", write_pdf=False
    )


def _box(ax, xy, width, height, text, *, color=F.BLUE, face="white", fs=12):
    patch = FancyBboxPatch(
        xy, width, height, boxstyle="round,pad=0.06",
        facecolor=face, edgecolor=color, lw=1.7,
    )
    ax.add_patch(patch)
    ax.text(xy[0] + width / 2, xy[1] + height / 2, text,
            ha="center", va="center", fontsize=fs, color=F.INK)


def fig_fixed_change_ratio():
    n = np.arange(0, 7)
    linear = 100 + 20 * n
    exponential = 100 * 1.2 ** n
    assert np.allclose(np.diff(linear), 20)
    assert np.allclose(exponential[1:] / exponential[:-1], 1.2)
    assert math.isclose(exponential[-1], 298.5984)

    fig, axes = plt.subplots(1, 2, figsize=(11.5, 4.8))
    ax = axes[0]
    ax.plot(n, linear, marker="o", lw=2.3, color=F.BLUE, label=r"$Q_n=100+20n$")
    for i in range(3):
        ax.annotate("+20", xy=(i + 1, linear[i + 1]),
                    xytext=(i + .5, linear[i] + 27), ha="center", color=F.BLUE,
                    arrowprops=dict(arrowstyle="->", color=F.BLUE))
    ax.set_title("固定增加：相鄰差固定")
    ax.set_xlabel("期數 $n$")
    ax.set_ylabel("數量")
    ax.legend(loc="upper left")
    F.clean_grid(ax)

    ax = axes[1]
    ax.plot(n, exponential, marker="o", lw=2.3, color=F.RED,
            label=r"$Q_n=100(1.2)^n$")
    for i in range(3):
        ax.annotate(r"$\times1.2$", xy=(i + 1, exponential[i + 1]),
                    xytext=(i + .5, exponential[i] + 42), ha="center", color=F.RED,
                    arrowprops=dict(arrowstyle="->", color=F.RED))
    ax.set_title("固定倍率：相鄰比固定")
    ax.set_xlabel("期數 $n$")
    ax.legend(loc="upper left")
    F.clean_grid(ax)
    fig.suptitle("相同起始值，更新規則決定線性或指數模型", fontsize=15)
    fig.tight_layout()
    return _save(fig, "數B3-2-固定差與固定倍率.svg")


def fig_exponential_family():
    x = np.linspace(-4, 4, 1201)
    growth = 2.0 ** x
    decay = .5 ** x
    assert np.allclose(decay, 2.0 ** (-x))
    assert math.isclose(growth[len(x) // 2], 1)
    assert np.all(growth > 0) and np.all(decay > 0)

    fig, ax = plt.subplots(figsize=(10.8, 5.3))
    ax.plot(x, growth, color=F.BLUE, lw=2.7, label=r"$y=2^x$")
    ax.plot(x, decay, color=F.RED, lw=2.7, label=r"$y=(1/2)^x=2^{-x}$")
    ax.axhline(0, color=F.AMBER, ls="--", lw=1.4, label="水平漸近線 $y=0$")
    ax.scatter([0], [1], color=F.INK, s=70, zorder=5)
    ax.text(.12, 1.15, "共同點 $(0,1)$")
    ax.set_xlim(-4, 4)
    ax.set_ylim(-.3, 10)
    ax.set_xlabel("$x$")
    ax.set_ylabel("$y$")
    ax.legend(loc="upper center", ncol=3, fontsize=10)
    F.clean_grid(ax)
    ax.set_title("底數大於 1 時遞增；底數介於 0 與 1 時遞減")
    fig.tight_layout()
    return _save(fig, "數B3-2-指數成長與衰退.svg")


def fig_base_comparison():
    bases = (1.5, 2.0, 3.0)
    x = np.linspace(-2.2, 2.2, 1000)
    values_pos = [base for base in bases]
    values_neg = [1 / base for base in bases]
    assert values_pos[0] < values_pos[1] < values_pos[2]
    assert values_neg[0] > values_neg[1] > values_neg[2]

    fig, ax = plt.subplots(figsize=(10.6, 5.3))
    colors = (F.GREEN, F.BLUE, F.RED)
    for base, color in zip(bases, colors):
        ax.plot(x, base ** x, lw=2.4, color=color, label=fr"$y={base:g}^x$")
        ax.scatter([-1, 1], [base ** -1, base], color=color, s=38, zorder=4)
    ax.axvline(-1, color=F.GRID, ls="--")
    ax.axvline(1, color=F.GRID, ls="--")
    ax.text(-1, 6.8, "$x=-1$：底數越大，倒數越小", ha="center", fontsize=10)
    ax.text(1, 6.8, "$x=1$：函數值等於底數", ha="center", fontsize=10)
    ax.set_xlim(-2.2, 2.2)
    ax.set_ylim(0, 7.4)
    ax.set_xlabel("$x$")
    ax.set_ylabel("$y$")
    ax.legend(loc="upper left")
    F.clean_grid(ax)
    ax.set_title("比較不同底數時，$x$ 的正負會改變大小次序")
    fig.tight_layout()
    return _save(fig, "數B3-2-指數底數比較.svg")


def fig_exponential_roots():
    x = np.linspace(-1.5, 3.0, 1500)
    y = 4.0 ** x - 5 * 2.0 ** x + 4
    roots = np.array([0.0, 2.0])
    x_min = math.log(2.5, 2)
    y_min = 2.5 ** 2 - 5 * 2.5 + 4
    assert np.allclose(4 ** roots - 5 * 2 ** roots + 4, 0)
    assert math.isclose(y_min, -2.25)

    fig, ax = plt.subplots(figsize=(10.5, 5.2))
    ax.plot(x, y, color=F.BLUE, lw=2.6,
            label=r"$y=4^x-5\cdot2^x+4$")
    ax.axhline(0, color=F.INK, lw=1.2)
    ax.scatter(roots, [0, 0], color=F.RED, s=65, zorder=5)
    ax.scatter([x_min], [y_min], color=F.GREEN, s=65, zorder=5)
    ax.annotate("$x=0$", (0, 0), xytext=(-.35, 2.2),
                arrowprops=dict(arrowstyle="->", color=F.RED), color=F.RED)
    ax.annotate("$x=2$", (2, 0), xytext=(2.15, 2.2),
                arrowprops=dict(arrowstyle="->", color=F.RED), color=F.RED)
    ax.annotate(r"令 $t=2^x$，最低點對應 $t=5/2$", (x_min, y_min),
                xytext=(-.8, -5.1), arrowprops=dict(arrowstyle="->", color=F.GREEN),
                color=F.GREEN)
    ax.set_xlim(-1.5, 3)
    ax.set_ylim(-5.8, 16)
    ax.set_xlabel("$x$")
    ax.set_ylabel("函數值")
    ax.legend(loc="upper left")
    F.clean_grid(ax)
    ax.set_title("同時出現 $4^x$ 與 $2^x$ 時，以 $t=2^x>0$ 化為二次式")
    fig.tight_layout()
    return _save(fig, "數B3-2-指數換元與交點.svg")


def fig_growth_decay_data():
    t_growth = np.arange(0, 7)
    growth = 500 * 1.06 ** t_growth
    t_decay = np.arange(0, 31, 6)
    decay = 240 * .75 ** (t_decay / 6)
    assert np.allclose(growth[1:] / growth[:-1], 1.06)
    assert np.allclose(decay[1:] / decay[:-1], .75)
    assert math.isclose(decay[-1], 240 * .75 ** 5)

    fig, axes = plt.subplots(1, 2, figsize=(11.6, 5.0))
    ax = axes[0]
    ax.plot(t_growth, growth, marker="o", color=F.BLUE, lw=2.4)
    ax.set_xlabel("時間（小時）")
    ax.set_ylabel("數量")
    ax.set_title(r"每小時增加 6%：$N=500(1.06)^t$")
    F.clean_grid(ax)
    ax = axes[1]
    ax.plot(t_decay, decay, marker="o", color=F.RED, lw=2.4)
    ax.set_xlabel("時間（小時）")
    ax.set_ylabel("藥量（mg）")
    ax.set_title(r"每 6 小時保留 75%：$M=240(0.75)^{t/6}$")
    F.clean_grid(ax)
    fig.suptitle("固定時間間隔內的倍率保持不變", fontsize=15)
    fig.tight_layout()
    return _save(fig, "數B3-2-成長衰退資料.svg")


def fig_simple_compound():
    principal, rate = 100000.0, .03
    n = np.arange(0, 31)
    simple = principal * (1 + rate * n)
    compound = principal * (1 + rate) ** n
    assert math.isclose(simple[0], compound[0])
    assert np.all(compound[2:] > simple[2:])
    assert math.isclose(compound[20], principal * 1.03 ** 20)

    fig, ax = plt.subplots(figsize=(10.8, 5.2))
    ax.plot(n, simple, color=F.BLUE, lw=2.5, marker="o", markevery=5,
            label=r"單利 $P(1+nr)$")
    ax.plot(n, compound, color=F.RED, lw=2.5, marker="o", markevery=5,
            label=r"複利 $P(1+r)^n$")
    ax.fill_between(n, simple, compound, color=F.AMBER, alpha=.17,
                    label="利息加入本金後累積的差額")
    ax.scatter([20, 20], [simple[20], compound[20]], color=[F.BLUE, F.RED], s=55)
    ax.text(20.5, compound[20], f"複利 {compound[20]:,.0f} 元", color=F.RED)
    ax.text(20.5, simple[20] - 3500, f"單利 {simple[20]:,.0f} 元", color=F.BLUE)
    ax.set_xlabel("期數 $n$")
    ax.set_ylabel("本利和（元）")
    ax.legend(loc="upper left")
    F.clean_grid(ax)
    ax.set_title("本金 100,000 元、每期利率 3%：線性累積與倍率累積")
    fig.tight_layout()
    return _save(fig, "數B3-2-單利與複利.svg")


def fig_log_definition():
    examples = [(2, 3, 8), (10, -2, .01), (.5, 3, .125)]
    for base, exponent, value in examples:
        assert math.isclose(base ** exponent, value)
        assert math.isclose(math.log(value, base), exponent)

    fig, ax = F.schematic(11.2, 5.3)
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 5.2)
    _box(ax, (.5, 3.35), 3.4, 1.05, r"指數式 $a^b=r$", color=F.BLUE, face="#eef5ff", fs=16)
    _box(ax, (7.1, 3.35), 3.4, 1.05, r"對數式 $b=\log_a r$", color=F.RED, face="#fff1f1", fs=16)
    ax.annotate("同一個關係，改問指數 $b$", xy=(7.0, 3.88), xytext=(4.0, 3.88),
                arrowprops=dict(arrowstyle="->", color=F.AMBER, lw=2),
                color=F.AMBER, ha="left")
    rows = [
        (2.55, r"$2^3=8$", r"$\log_2 8=3$"),
        (1.55, r"$10^{-2}=0.01$", r"$\log 0.01=-2$"),
        (.55, r"$(1/2)^3=1/8$", r"$\log_{1/2}(1/8)=3$"),
    ]
    for y, left, right in rows:
        _box(ax, (.9, y), 2.9, .68, left, color=F.BLUE, fs=13)
        _box(ax, (7.2, y), 2.9, .68, right, color=F.RED, fs=13)
        ax.annotate("", xy=(7.05, y + .34), xytext=(3.95, y + .34),
                    arrowprops=dict(arrowstyle="<->", color=F.GRID, lw=1.5))
    ax.set_title(r"條件：$a>0, a\ne1, r>0$", fontsize=15)
    fig.tight_layout()
    return _save(fig, "數B3-2-指數與對數對照.svg")


def fig_log_laws():
    r, s = 4.0, 25.0
    lr, ls = math.log10(r), math.log10(s)
    assert math.isclose(lr + ls, math.log10(r * s))
    assert math.isclose(lr - ls, math.log10(r / s))
    assert math.isclose(3 * lr, math.log10(r ** 3))

    fig, axes = plt.subplots(1, 2, figsize=(11.5, 4.8))
    ax = axes[0]
    ax.set_xlim(-.15, 2.15)
    ax.set_ylim(-.4, 1.3)
    ax.axhline(0, color=F.INK, lw=1.4)
    points = [(0, "1"), (lr, "4"), (ls, "25"), (2, "100")]
    for x0, label in points:
        ax.scatter([x0], [0], s=55, color=F.BLUE if label in ("4", "25") else F.RED)
        ax.text(x0, -.18, label, ha="center")
    ax.annotate(r"$\log4$", xy=(lr, .46), xytext=(0, .46), ha="center",
                arrowprops=dict(arrowstyle="<->", color=F.BLUE), color=F.BLUE)
    ax.annotate(r"$\log25$", xy=(2, .82), xytext=(lr, .82), ha="center",
                arrowprops=dict(arrowstyle="<->", color=F.GREEN), color=F.GREEN)
    ax.text(1, 1.08, r"$\log4+\log25=\log100=2$", ha="center", fontsize=13)
    ax.set_xticks([0, .5, 1, 1.5, 2])
    ax.set_yticks([])
    ax.set_xlabel("常用對數刻度")
    ax.set_title("相乘對應刻度相加")
    ax.spines[["top", "right", "left"]].set_visible(False)

    ax = axes[1]
    ax.axis("off")
    ax.set_xlim(0, 6)
    ax.set_ylim(0, 4.4)
    formulas = [
        (3.35, r"$\log(rs)=\log r+\log s$", F.BLUE),
        (2.25, r"$\log(r/s)=\log r-\log s$", F.GREEN),
        (1.15, r"$\log(r^t)=t\log r$", F.PURPLE),
    ]
    for y, formula, color in formulas:
        ax.text(3, y, formula, ha="center", fontsize=15,
                bbox=dict(boxstyle="round,pad=.32", fc="white", ec=color), color=color)
    ax.text(3, .32, r"成立條件：$r>0, s>0$；$t$ 為實數", ha="center", fontsize=11)
    ax.set_title("指數律轉寫成對數律")
    fig.tight_layout()
    return _save(fig, "數B3-2-對數律刻度.svg")


def fig_e_convergence():
    n = np.array([1, 2, 5, 10, 100, 1000, 10000, 1000000], dtype=float)
    values = (1 + 1 / n) ** n
    assert np.all(np.diff(values) > 0)
    assert np.all(values < math.e)
    assert abs(values[-1] - math.e) < 2e-6

    fig, ax = plt.subplots(figsize=(10.7, 5.1))
    ax.semilogx(n, values, marker="o", color=F.BLUE, lw=2.5,
                label=r"$(1+1/n)^n$")
    ax.axhline(math.e, color=F.RED, ls="--", lw=2,
               label=fr"$e\approx {math.e:.6f}$")
    for n0, y0 in zip(n[[0, 3, -1]], values[[0, 3, -1]]):
        ax.text(n0, y0 - .055, f"n={int(n0):,}\n{y0:.6f}", ha="center", fontsize=9)
    ax.set_ylim(1.9, 2.76)
    ax.set_xlabel("一年分成的複利期數 $n$（對數刻度）")
    ax.set_ylabel("一年後倍率")
    ax.legend(loc="lower right")
    F.clean_grid(ax)
    ax.set_title("年利率 100% 分得越細，一年後倍率趨近常數 $e$")
    fig.tight_layout()
    return _save(fig, "數B3-2-複利頻率與常數e.svg")


def fig_log_scales():
    db = np.array([60.0, 80.0])
    relative_intensity = 10 ** (db / 10)
    assert math.isclose(relative_intensity[1] / relative_intensity[0], 100)
    ph = np.array([3.0, 5.0])
    concentration = 10 ** (-ph)
    assert math.isclose(concentration[0] / concentration[1], 100)

    fig, axes = plt.subplots(1, 2, figsize=(11.5, 4.9))
    ax = axes[0]
    ax.bar(["交談\n60 dB", "室外噪音\n80 dB"], np.log10(relative_intensity),
           color=[F.BLUE, F.RED], alpha=.8)
    ax.text(.5, 7.05, "分貝差 20 dB\n強度比 $10^{20/10}=100$", ha="center",
            bbox=dict(boxstyle="round,pad=.28", fc="white", ec=F.AMBER))
    ax.set_ylabel(r"$\log_{10}(I/I_0)$")
    ax.set_ylim(0, 9)
    ax.set_title(r"聲音：$D=10\log(I/I_0)$")
    F.clean_grid(ax)

    ax = axes[1]
    ax.bar(["pH 3", "pH 5"], -np.log10(concentration),
           color=[F.RED, F.GREEN], alpha=.8)
    ax.text(.5, 3.2, "pH 差 2\n氫離子濃度比 $10^2=100$", ha="center",
            bbox=dict(boxstyle="round,pad=.28", fc="white", ec=F.AMBER))
    ax.set_ylabel(r"$-\log_{10}[H^+]$")
    ax.set_ylim(0, 6)
    ax.set_title(r"酸鹼度：$\mathrm{pH}=-\log[H^+]$")
    F.clean_grid(ax)
    fig.suptitle("對數刻度把倍率轉成差值", fontsize=15)
    fig.tight_layout()
    return _save(fig, "數B3-2-對數尺度.svg")


def fig_log_family():
    x = np.geomspace(.04, 12, 1400)
    growth = np.log2(x)
    decay = np.log(x) / math.log(.5)
    assert np.allclose(decay, -growth)
    assert math.isclose(np.log2(1), 0)

    fig, ax = plt.subplots(figsize=(10.7, 5.3))
    ax.plot(x, growth, color=F.BLUE, lw=2.7, label=r"$y=\log_2x$")
    ax.plot(x, decay, color=F.RED, lw=2.7, label=r"$y=\log_{1/2}x$")
    ax.axvline(0, color=F.AMBER, ls="--", lw=1.5, label="鉛直漸近線 $x=0$")
    points = [(1, 0), (2, 1), (.5, -1)]
    ax.scatter([p[0] for p in points], [p[1] for p in points], color=F.INK, s=55, zorder=5)
    for px, py in points:
        ax.text(px + .12, py + .12, f"({px:g},{py:g})", fontsize=9)
    ax.set_xlim(-.4, 12)
    ax.set_ylim(-4.2, 4.2)
    ax.set_xlabel("$x$")
    ax.set_ylabel("$y$")
    ax.legend(loc="lower right")
    F.clean_grid(ax)
    ax.set_title("對數函數定義域為正實數，兩類底數決定遞增或遞減")
    fig.tight_layout()
    return _save(fig, "數B3-2-對數成長與衰退.svg")


def fig_log_equation():
    x = np.linspace(1.001, 5.5, 1400)
    left = np.log10((x - 1) * (2 * x + 1))
    target = math.log10(20)
    root = 3.5
    assert math.isclose((root - 1) * (2 * root + 1), 20)
    assert math.isclose(np.log10((root - 1) * (2 * root + 1)), target)

    fig, ax = plt.subplots(figsize=(10.6, 5.2))
    ax.plot(x, left, color=F.BLUE, lw=2.6,
            label=r"$y=\log((x-1)(2x+1))$")
    ax.axhline(target, color=F.RED, lw=2, label=r"$y=\log20$")
    ax.axvline(1, color=F.AMBER, ls="--", lw=1.4, label="合併後採用的定義域 $x>1$")
    ax.scatter([root], [target], color=F.GREEN, s=70, zorder=5)
    ax.annotate(r"交點 $x=7/2$", (root, target), xytext=(4.05, .65),
                arrowprops=dict(arrowstyle="->", color=F.GREEN), color=F.GREEN)
    ax.set_xlim(.7, 5.5)
    ax.set_ylim(-2.3, 2)
    ax.set_xlabel("$x$")
    ax.set_ylabel("$y$")
    ax.legend(loc="lower right", fontsize=9)
    F.clean_grid(ax)
    ax.set_title("對數方程先取真數條件，再由交點保留合法解")
    fig.tight_layout()
    return _save(fig, "數B3-2-對數方程與定義域.svg")


def fig_inverse_reflection():
    base = 2.0
    x_exp = np.linspace(-3.2, 2.35, 1000)
    y_exp = base ** x_exp
    x_log = np.geomspace(.05, 5.2, 1000)
    y_log = np.log2(x_log)
    paired = [(-1, .5), (0, 1), (1, 2), (2, 4)]
    for px, py in paired:
        assert math.isclose(py, base ** px)
        assert math.isclose(np.log2(py), px)
    x_min = math.log(1 / math.log(base), base)
    min_gap = base ** x_min - x_min
    assert min_gap > 0

    fig, ax = plt.subplots(figsize=(8.4, 7.0))
    ax.plot(x_exp, y_exp, color=F.BLUE, lw=2.7, label=r"$y=2^x$")
    ax.plot(x_log, y_log, color=F.RED, lw=2.7, label=r"$y=\log_2x$")
    diagonal = np.linspace(-3.2, 5.2, 300)
    ax.plot(diagonal, diagonal, color=F.INK, ls="--", lw=1.6, label=r"$y=x$")
    for px, py in paired:
        ax.scatter([px, py], [py, px], color=[F.BLUE, F.RED], s=42, zorder=5)
        ax.plot([px, py], [py, px], color=F.GRID, lw=1.0)
    ax.text(-2.85, 4.35, "每組 $(u,v)$ 與 $(v,u)$\n分居 $y=x$ 兩側", fontsize=10,
            bbox=dict(boxstyle="round,pad=.3", fc="white", ec=F.AMBER))
    ax.set_xlim(-3.2, 5.2)
    ax.set_ylim(-3.2, 5.2)
    ax.set_aspect("equal", adjustable="box")
    ax.set_xlabel("$x$")
    ax.set_ylabel("$y$")
    ax.legend(loc="lower right")
    F.clean_grid(ax)
    ax.set_title("互換輸入與輸出形成鏡射；兩曲線本身不必碰到 $y=x$")
    fig.tight_layout()
    return _save(fig, "數B3-2-指數對數互為反函數.svg")


def fig_log_linear_data():
    t = np.arange(0, 7)
    quantity = 300 * 1.5 ** t
    log_quantity = np.log10(quantity)
    slope, intercept = np.polyfit(t, log_quantity, 1)
    assert math.isclose(slope, math.log10(1.5), abs_tol=1e-12)
    assert math.isclose(intercept, math.log10(300), abs_tol=1e-12)
    assert np.allclose(log_quantity, intercept + slope * t)

    fig, axes = plt.subplots(1, 2, figsize=(11.6, 5.0))
    ax = axes[0]
    ax.plot(t, quantity, marker="o", color=F.BLUE, lw=2.5)
    ax.set_xlabel("時間 $t$")
    ax.set_ylabel("數量 $Q$")
    ax.set_title(r"原資料：$Q=300(1.5)^t$")
    F.clean_grid(ax)

    ax = axes[1]
    ax.scatter(t, log_quantity, color=F.RED, s=55, zorder=4)
    ax.plot(t, intercept + slope * t, color=F.RED, lw=2.2)
    ax.text(.25, log_quantity[-1] - .18,
            r"$\log Q=\log300+t\log1.5$" + f"\n斜率 = {slope:.4f}",
            fontsize=10, bbox=dict(boxstyle="round,pad=.3", fc="white", ec=F.RED))
    ax.set_xlabel("時間 $t$")
    ax.set_ylabel(r"$\log Q$")
    ax.set_title("取常用對數後：資料落在直線上")
    F.clean_grid(ax)
    fig.tight_layout()
    return _save(fig, "數B3-2-指數資料取對數.svg")


def main():
    functions = {name: globals()[name] for name, _ in FIGURE_OUTPUTS}
    assert len(functions) == len(FIGURE_OUTPUTS)
    outputs = []
    for function_name, filename in FIGURE_OUTPUTS:
        path = functions[function_name]()
        assert os.path.basename(path) == filename
        outputs.append(path)
    assert len(outputs) == len(set(outputs)) == len(FIGURE_OUTPUTS)
    print(f"verified {len(outputs)} chapter SVG files; write_pdf=False")


if __name__ == "__main__":
    main()
