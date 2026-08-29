# -*- coding: utf-8 -*-
"""重生「數1-1 數與式」學生講義的五張章內 SVG。"""

if __name__ == "__main__" and __import__("sys").argv[1:]:
    raise SystemExit("本腳本不接受參數；直接執行即可重生數1-1 章內 SVG。")

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle

import figlib as F


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHAPTER = os.path.join(ROOT, "content", "必修數學", "數1-1")

FIGURE_OUTPUTS = (
    ("fig_real_intervals", "數1-1-實數與區間.svg"),
    ("fig_section_distance", "數1-1-分點與距離.svg"),
    ("fig_absolute_distance", "數1-1-絕對值距離.svg"),
    ("fig_identity_area", "數1-1-乘法公式面積.svg"),
    ("fig_amgm_optimization", "數1-1-算幾最佳化.svg"),
)


def _save(fig, filename):
    stem, extension = os.path.splitext(filename)
    if extension != ".svg" or not stem.startswith("數1-1-"):
        raise AssertionError("輸出檔名必須是數1-1 章內 SVG")
    return F.save_to(fig, CHAPTER, stem, output_subdir="assets", write_pdf=False)


def _number_line(ax, xmin=-6, xmax=8):
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(-0.55, 0.65)
    ax.axhline(0, color=F.INK, lw=1.8)
    ax.set_yticks([])
    ax.set_xticks(range(xmin, xmax + 1))
    ax.tick_params(axis="x", length=4, labelsize=9)
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_visible(False)


def fig_real_intervals():
    fig, axes = plt.subplots(3, 1, figsize=(10.5, 4.8), sharex=True)
    for ax in axes:
        _number_line(ax)

    axes[0].plot([-3, 4], [0, 0], color=F.BLUE, lw=7, solid_capstyle="butt")
    axes[0].scatter([-3], [0], s=85, facecolor="white", edgecolor=F.BLUE, lw=2.2, zorder=5)
    axes[0].scatter([4], [0], s=85, facecolor=F.BLUE, edgecolor=F.BLUE, lw=2.2, zorder=5)
    axes[0].text(0.5, 0.34, r"$(-3,4]$", color=F.BLUE, ha="center", fontsize=13)

    axes[1].plot([-1, 7], [0, 0], color=F.GREEN, lw=7, solid_capstyle="butt")
    axes[1].scatter([-1], [0], s=85, facecolor=F.GREEN, edgecolor=F.GREEN, lw=2.2, zorder=5)
    axes[1].scatter([7], [0], s=85, facecolor="white", edgecolor=F.GREEN, lw=2.2, zorder=5)
    axes[1].text(3, 0.34, r"$[-1,7)$", color=F.GREEN, ha="center", fontsize=13)

    axes[2].plot([-6, -4], [0, 0], color=F.AMBER, lw=7, solid_capstyle="butt")
    axes[2].plot([3, 8], [0, 0], color=F.AMBER, lw=7, solid_capstyle="butt")
    axes[2].annotate("", xy=(-5.95, 0), xytext=(-5.25, 0), arrowprops=dict(arrowstyle="-|>", color=F.AMBER, lw=2.2))
    axes[2].annotate("", xy=(7.95, 0), xytext=(7.25, 0), arrowprops=dict(arrowstyle="-|>", color=F.AMBER, lw=2.2))
    axes[2].scatter([-4], [0], s=85, facecolor="white", edgecolor=F.AMBER, lw=2.2, zorder=5)
    axes[2].scatter([3], [0], s=85, facecolor=F.AMBER, edgecolor=F.AMBER, lw=2.2, zorder=5)
    axes[2].text(-0.5, 0.34, r"$(-\infty,-4)\cup[3,\infty)$", color=F.AMBER, ha="center", fontsize=13)

    fig.suptitle("端點、方向與區間符號", fontsize=15)
    fig.tight_layout(rect=(0, 0, 1, 0.93))
    return _save(fig, "數1-1-實數與區間.svg")


def fig_section_distance():
    a, b, m, n = -4.0, 11.0, 2.0, 3.0
    p = (n * a + m * b) / (m + n)
    assert np.isclose(p, 2.0)
    assert np.isclose((p - a) / (b - p), m / n)

    fig, ax = plt.subplots(figsize=(10.2, 3.4))
    ax.set_xlim(-5.5, 12.5)
    ax.set_ylim(-1.0, 1.2)
    ax.axhline(0, color=F.INK, lw=2)
    ax.plot([a, p], [0, 0], color=F.BLUE, lw=8, solid_capstyle="butt")
    ax.plot([p, b], [0, 0], color=F.GREEN, lw=8, solid_capstyle="butt")
    for x, label, color in ((a, "A(-4)", F.BLUE), (p, "P(2)", F.AMBER), (b, "B(11)", F.GREEN)):
        ax.scatter([x], [0], s=110, color=color, edgecolor="white", lw=1.2, zorder=5)
        ax.text(x, -0.38, label, ha="center", fontsize=12, color=color)
    ax.annotate("", xy=(p, 0.58), xytext=(a, 0.58), arrowprops=dict(arrowstyle="<->", lw=1.8, color=F.BLUE))
    ax.annotate("", xy=(b, 0.58), xytext=(p, 0.58), arrowprops=dict(arrowstyle="<->", lw=1.8, color=F.GREEN))
    ax.text((a + p) / 2, 0.78, "AP = 6（2 份）", ha="center", color=F.BLUE, fontsize=11)
    ax.text((p + b) / 2, 0.78, "PB = 9（3 份）", ha="center", color=F.GREEN, fontsize=11)
    ax.text(3.5, -0.82, r"$x_P=\dfrac{3(-4)+2(11)}{2+3}=2$", ha="center", fontsize=14)
    ax.axis("off")
    ax.set_title("內分點：位置由兩側距離比例決定", fontsize=15)
    fig.tight_layout()
    return _save(fig, "數1-1-分點與距離.svg")


def fig_absolute_distance():
    center, radius = 2.0, 3.0
    left, right = center - radius, center + radius
    assert np.isclose(abs(left - center), radius)
    assert np.isclose(abs(right - center), radius)

    fig, axes = plt.subplots(2, 1, figsize=(10.3, 4.2), sharex=True)
    for ax in axes:
        _number_line(ax, -3, 7)
        ax.scatter([center], [0], s=70, color=F.INK, zorder=5)
        ax.text(center, -0.38, "中心 2", ha="center", fontsize=11)

    axes[0].plot([left, right], [0, 0], color=F.BLUE, lw=8, solid_capstyle="butt")
    axes[0].scatter([left, right], [0, 0], s=90, facecolor=F.BLUE, edgecolor=F.BLUE, zorder=6)
    axes[0].text(center, 0.38, r"$|x-2|\leq3\ \Longleftrightarrow\ -1\leq x\leq5$", ha="center", color=F.BLUE, fontsize=13)

    axes[1].plot([-3, left], [0, 0], color=F.AMBER, lw=8, solid_capstyle="butt")
    axes[1].plot([right, 7], [0, 0], color=F.AMBER, lw=8, solid_capstyle="butt")
    axes[1].annotate("", xy=(-2.95, 0), xytext=(-2.35, 0), arrowprops=dict(arrowstyle="-|>", color=F.AMBER, lw=2.2))
    axes[1].annotate("", xy=(6.95, 0), xytext=(6.35, 0), arrowprops=dict(arrowstyle="-|>", color=F.AMBER, lw=2.2))
    axes[1].scatter([left, right], [0, 0], s=90, facecolor="white", edgecolor=F.AMBER, lw=2.2, zorder=6)
    axes[1].text(center, 0.38, r"$|x-2|>3\ \Longleftrightarrow\ x<-1\ \mathrm{or}\ x>5$", ha="center", color=F.AMBER, fontsize=13)

    fig.suptitle("絕對值條件就是離中心的距離條件", fontsize=15)
    fig.tight_layout(rect=(0, 0, 1, 0.92))
    return _save(fig, "數1-1-絕對值距離.svg")


def fig_identity_area():
    a, b = 3.2, 1.8
    total = (a + b) ** 2
    pieces = a * a + 2 * a * b + b * b
    assert np.isclose(total, pieces)

    fig, ax = F.schematic(7.2, 6.0)
    ax.set_xlim(-0.8, a + b + 0.8)
    ax.set_ylim(-0.8, a + b + 1.0)
    blocks = (
        (0, 0, a, a, "#dbeafe", r"$a^2$"),
        (a, 0, b, a, "#dcfce7", r"$ab$"),
        (0, a, a, b, "#dcfce7", r"$ab$"),
        (a, a, b, b, "#fef3c7", r"$b^2$"),
    )
    for x, y, w, h, color, label in blocks:
        ax.add_patch(Rectangle((x, y), w, h, facecolor=color, edgecolor=F.INK, lw=1.5))
        ax.text(x + w / 2, y + h / 2, label, ha="center", va="center", fontsize=17)
    ax.text(a / 2, -0.35, r"$a$", ha="center", fontsize=13)
    ax.text(a + b / 2, -0.35, r"$b$", ha="center", fontsize=13)
    ax.text(-0.35, a / 2, r"$a$", ha="center", fontsize=13)
    ax.text(-0.35, a + b / 2, r"$b$", ha="center", fontsize=13)
    ax.text((a + b) / 2, a + b + 0.48, r"$(a+b)^2=a^2+2ab+b^2$", ha="center", fontsize=16)
    ax.set_title("面積分割推導平方公式", fontsize=15)
    fig.tight_layout()
    return _save(fig, "數1-1-乘法公式面積.svg")


def fig_amgm_optimization():
    total = 18.0
    x = np.linspace(0.2, total - 0.2, 400)
    product = x * (total - x)
    peak_x = total / 2
    peak_y = peak_x**2
    assert np.isclose(product.max(), peak_y, atol=0.02)

    fig, ax = plt.subplots(figsize=(9.2, 5.2))
    ax.plot(x, product, color=F.BLUE, lw=2.8, label=r"$xy=x(18-x)$")
    ax.axvline(peak_x, color=F.GRID, lw=1.4, ls="--")
    ax.axhline(peak_y, color=F.GRID, lw=1.4, ls="--")
    ax.scatter([peak_x], [peak_y], color=F.AMBER, s=85, zorder=5)
    ax.annotate("x = y = 9\n最大乘積 81", xy=(peak_x, peak_y), xytext=(12.0, 67),
                arrowprops=dict(arrowstyle="->", color=F.AMBER, lw=1.8), color=F.AMBER, fontsize=12)
    ax.set_xlim(0, 18)
    ax.set_ylim(0, 90)
    ax.set_xlabel("第一個正數 x（第二個為 18−x）")
    ax.set_ylabel("乘積 xy")
    ax.set_title("固定和 18：兩數相等時乘積最大", fontsize=15)
    F.clean_grid(ax)
    fig.tight_layout()
    return _save(fig, "數1-1-算幾最佳化.svg")


if __name__ == "__main__":
    for entrypoint, filename in FIGURE_OUTPUTS:
        output = globals()[entrypoint]()
        if os.path.basename(output) != filename:
            raise AssertionError(f"{entrypoint} 輸出與 FIGURE_OUTPUTS 不一致")
