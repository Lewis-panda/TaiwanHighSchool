# -*- coding: utf-8 -*-
"""重生「數2-2 數據分析」學生講義的章內 SVG。"""

if __name__ == "__main__" and __import__("sys").argv[1:]:
    raise SystemExit("本腳本不接受參數；直接執行即可重生數2-2 章內 SVG。")

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import matplotlib.pyplot as plt
import numpy as np

import figlib as F


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHAPTER = os.path.join(ROOT, "content", "必修數學", "數2-2")

FIGURE_OUTPUTS = (
    ("fig_mean_balance", "數2-2-平均數平衡.svg"),
    ("fig_percentile_box", "數2-2-百分位數與盒狀圖.svg"),
    ("fig_same_mean_spread", "數2-2-同平均不同分散.svg"),
    ("fig_linear_transform", "數2-2-資料伸縮平移.svg"),
    ("fig_zscore", "數2-2-標準化比較.svg"),
    ("fig_scatter_patterns", "數2-2-散布圖型態.svg"),
    ("fig_least_squares", "數2-2-最小平方法.svg"),
    ("fig_outlier", "數2-2-離群值影響.svg"),
)


def _save(fig, filename):
    stem, extension = os.path.splitext(filename)
    if extension != ".svg" or not stem.startswith("數2-2-"):
        raise AssertionError("輸出檔名必須是數2-2章內 SVG")
    return F.save_to(fig, CHAPTER, stem, output_subdir="assets", write_pdf=False)


def _axis_at_zero(ax):
    ax.axhline(0, color=F.INK, lw=0.9, alpha=0.7)
    ax.axvline(0, color=F.INK, lw=0.9, alpha=0.7)
    F.clean_grid(ax)


def fig_mean_balance():
    values = np.array([2.0, 4.0, 9.0])
    mean = values.mean()
    deviations = values - mean
    assert np.isclose(mean, 5.0)
    assert np.isclose(deviations.sum(), 0.0)

    fig, axes = plt.subplots(2, 1, figsize=(9.4, 5.8), gridspec_kw={"height_ratios": [1.0, 1.35]})
    ax = axes[0]
    ax.scatter(values, np.zeros_like(values), s=95, color=[F.BLUE, F.BLUE, F.BLUE], zorder=5)
    ax.scatter([mean], [0], s=145, marker="D", color=F.AMBER, zorder=6)
    for x in values:
        ax.plot([x, mean], [0.0, 0.0], color=F.GREEN if x < mean else F.BLUE, lw=3, alpha=0.45)
    ax.text(mean, 0.18, r"平均數 $\bar{x}=5$", ha="center", color=F.AMBER, fontsize=13)
    ax.set_xlim(0, 11)
    ax.set_ylim(-0.25, 0.55)
    ax.set_yticks([])
    ax.set_xticks(range(0, 12))
    ax.set_title("三筆資料 2、4、9 的偏差總和為 0", fontsize=14)
    F.clean_grid(ax)

    ax = axes[1]
    labels = ["2−5", "4−5", "9−5"]
    colors = [F.GREEN, F.GREEN, F.BLUE]
    ax.bar(labels, deviations, color=colors, alpha=0.82)
    ax.axhline(0, color=F.INK, lw=1)
    for index, value in enumerate(deviations):
        ax.text(index, value + (0.2 if value >= 0 else -0.45), f"{value:+.0f}", ha="center", fontsize=12)
    ax.text(1, 3.25, r"$(-3)+(-1)+4=0$", ha="center", color=F.AMBER, fontsize=14)
    ax.set_ylim(-4.2, 4.2)
    ax.set_ylabel("相對平均數的偏差")
    F.clean_grid(ax)
    fig.suptitle("算術平均數是帶號偏差的平衡點", fontsize=16)
    fig.tight_layout(rect=(0, 0, 1, 0.93))
    return _save(fig, "數2-2-平均數平衡.svg")


def fig_percentile_box():
    data = np.array([41, 48, 53, 57, 61, 66, 72, 78, 84, 92], dtype=float)
    # 依 114 課本約定：I=np；非整數取第 ceil(I) 筆，整數取第 I、I+1 筆平均。
    def percentile(p):
        position = len(data) * p
        if np.isclose(position, round(position)):
            index = int(round(position))
            return (data[index - 1] + data[index]) / 2
        return data[int(np.ceil(position)) - 1]

    q1, median, q3 = (percentile(p) for p in (0.25, 0.5, 0.75))
    assert np.allclose([q1, median, q3], [53.0, 63.5, 78.0])
    iqr = q3 - q1
    assert np.isclose(iqr, 25.0)

    fig, axes = plt.subplots(2, 1, figsize=(10.2, 5.4), gridspec_kw={"height_ratios": [1.25, 1]})
    ax = axes[0]
    ax.scatter(data, np.zeros_like(data), color=F.BLUE, s=65, zorder=4)
    for rank, x in enumerate(data, start=1):
        ax.text(x, 0.13, str(rank), ha="center", fontsize=9, color=F.INK)
    for value, label, color in ((q1, "$Q_1$", F.GREEN), (median, "$Q_2$", F.AMBER), (q3, "$Q_3$", F.GREEN)):
        ax.axvline(value, color=color, lw=2, ls="--")
        ax.text(value, -0.22, f"{label}={value:g}", ha="center", color=color, fontsize=11)
    ax.set_ylim(-0.36, 0.42)
    ax.set_yticks([])
    ax.set_title("先排序，再用位置決定百分位數", fontsize=14)
    F.clean_grid(ax)

    ax = axes[1]
    ax.plot([data.min(), q1], [1, 1], color=F.INK, lw=1.8)
    ax.plot([q3, data.max()], [1, 1], color=F.INK, lw=1.8)
    ax.plot([data.min(), data.min()], [0.78, 1.22], color=F.INK, lw=1.8)
    ax.plot([data.max(), data.max()], [0.78, 1.22], color=F.INK, lw=1.8)
    ax.add_patch(plt.Rectangle((q1, 0.7), q3 - q1, 0.6,
                               facecolor="#bfdbfe", edgecolor=F.BLUE, linewidth=2))
    ax.plot([median, median], [0.7, 1.3], color=F.AMBER, lw=2.5)
    ax.set_ylim(0.4, 1.6)
    ax.set_yticks([])
    ax.set_xlabel("資料值")
    ax.set_title(f"盒子的寬度是四分位距 IQR = {iqr:g}", fontsize=13)
    F.clean_grid(ax)
    fig.suptitle("百分位數與盒狀圖保留資料的位置資訊", fontsize=16)
    fig.tight_layout(rect=(0, 0, 1, 0.92))
    return _save(fig, "數2-2-百分位數與盒狀圖.svg")


def fig_same_mean_spread():
    a = np.array([4, 5, 6, 7, 8], dtype=float)
    b = np.array([0, 3, 6, 9, 12], dtype=float)
    assert np.isclose(a.mean(), b.mean()) and np.isclose(a.mean(), 6)
    sd_a = np.sqrt(np.mean((a - a.mean()) ** 2))
    sd_b = np.sqrt(np.mean((b - b.mean()) ** 2))
    assert np.isclose(sd_a, np.sqrt(2))
    assert np.isclose(sd_b, np.sqrt(18))

    fig, ax = plt.subplots(figsize=(9.8, 4.8))
    ax.scatter(a, np.full_like(a, 1), s=90, color=F.GREEN, label=rf"A：$s={sd_a:.2f}$", zorder=4)
    ax.scatter(b, np.full_like(b, 0), s=90, color=F.BLUE, label=rf"B：$s={sd_b:.2f}$", zorder=4)
    ax.axvline(6, color=F.AMBER, lw=2.4, ls="--", label=r"共同平均數 $\bar{x}=6$")
    for y, xs, color in ((1, a, F.GREEN), (0, b, F.BLUE)):
        for x in xs:
            ax.plot([6, x], [y, y], color=color, alpha=0.25, lw=2)
    ax.set_xlim(-1, 13)
    ax.set_ylim(-0.6, 1.6)
    ax.set_yticks([0, 1], ["資料組 B", "資料組 A"])
    ax.set_xlabel("資料值")
    ax.set_title("平均數相同時，標準差區分資料離中心有多遠", fontsize=15)
    ax.legend(frameon=False, ncol=3, loc="upper center")
    F.clean_grid(ax)
    fig.tight_layout()
    return _save(fig, "數2-2-同平均不同分散.svg")


def fig_linear_transform():
    x = np.array([2, 4, 5, 7, 12], dtype=float)
    y = 1.5 * x + 10
    assert np.isclose(y.mean(), 1.5 * x.mean() + 10)
    assert np.isclose(np.std(y), 1.5 * np.std(x))

    fig, axes = plt.subplots(1, 2, figsize=(10.6, 4.5))
    axes[0].scatter(x, np.zeros_like(x), s=85, color=F.BLUE)
    axes[0].axvline(x.mean(), color=F.AMBER, lw=2, ls="--")
    axes[0].set_xlim(0, 14)
    axes[0].set_title(r"原資料 $x$：$\bar{x}=6$", fontsize=13)
    axes[0].set_xlabel(r"$x$")
    axes[0].set_yticks([])

    axes[1].scatter(y, np.zeros_like(y), s=85, color=F.GREEN)
    axes[1].axvline(y.mean(), color=F.AMBER, lw=2, ls="--")
    axes[1].set_xlim(10, 30)
    axes[1].set_title(r"新資料 $y=1.5x+10$：$\bar{y}=19$", fontsize=13)
    axes[1].set_xlabel(r"$y$")
    axes[1].set_yticks([])
    for ax in axes:
        ax.set_ylim(-0.4, 0.45)
        F.clean_grid(ax)
    fig.suptitle("平移改變中心；伸縮同時改變中心距離與標準差", fontsize=16)
    fig.tight_layout(rect=(0, 0, 1, 0.91))
    return _save(fig, "數2-2-資料伸縮平移.svg")


def fig_zscore():
    exams = [(72, 60, 8, "甲科"), (82, 70, 6, "乙科")]
    z = [(score - mean) / sd for score, mean, sd, _ in exams]
    assert np.allclose(z, [1.5, 2.0])

    fig, ax = plt.subplots(figsize=(9.2, 4.7))
    base = np.linspace(-3.2, 3.2, 400)
    curve = np.exp(-base**2 / 2)
    curve /= curve.max()
    ax.plot(base, curve, color=F.INK, lw=2)
    ax.fill_between(base, 0, curve, color="#e5e7eb", alpha=0.7)
    colors = [F.BLUE, F.GREEN]
    for value, color, (_, _, _, label) in zip(z, colors, exams):
        height = np.exp(-value**2 / 2)
        ax.scatter([value], [height], color=color, s=95, zorder=5)
        ax.axvline(value, color=color, lw=1.8, ls="--")
        ax.text(value, height + 0.12, f"{label} z={value:g}", ha="center", color=color, fontsize=12)
    ax.axvline(0, color=F.AMBER, lw=2)
    ax.text(0, 1.07, "群體平均", ha="center", color=F.AMBER, fontsize=12)
    ax.set_xlim(-3.2, 3.2)
    ax.set_ylim(0, 1.28)
    ax.set_xlabel("離平均數幾個標準差（z 分數）")
    ax.set_yticks([])
    ax.set_title("標準化把不同單位或不同難度的資料放到同一尺度", fontsize=15)
    F.clean_grid(ax)
    fig.tight_layout()
    return _save(fig, "數2-2-標準化比較.svg")


def fig_scatter_patterns():
    rng = np.random.default_rng(20260829)
    x = np.linspace(1, 10, 14)
    datasets = (
        (x + rng.normal(0, 0.65, x.size), "強正相關"),
        (-0.8 * x + rng.normal(0, 0.75, x.size), "強負相關"),
        (rng.normal(0, 2.8, x.size), "線性相關接近 0"),
        ((x - 5.5) ** 2 + rng.normal(0, 1.2, x.size), "曲線關係；r 接近 0"),
    )
    fig, axes = plt.subplots(2, 2, figsize=(10.2, 7.2))
    for ax, (y, title) in zip(axes.flat, datasets):
        r = np.corrcoef(x, y)[0, 1]
        if "接近 0" in title:
            assert abs(r) < 0.35
        ax.scatter(x, y, color=F.BLUE, s=48, alpha=0.9)
        ax.set_title(f"{title}（r={r:.2f}）", fontsize=12)
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        F.clean_grid(ax)
    fig.suptitle("相關係數只概括線性方向與緊密程度", fontsize=16)
    fig.tight_layout(rect=(0, 0, 1, 0.94))
    return _save(fig, "數2-2-散布圖型態.svg")


def fig_least_squares():
    x = np.array([1, 2, 3, 4, 5, 6], dtype=float)
    y = np.array([2, 3, 5, 4, 7, 8], dtype=float)
    slope = np.cov(x, y, bias=True)[0, 1] / np.var(x)
    intercept = y.mean() - slope * x.mean()
    prediction = intercept + slope * x
    residuals = y - prediction
    assert np.isclose(residuals.sum(), 0)
    assert np.isclose(slope, np.corrcoef(x, y)[0, 1] * np.std(y) / np.std(x))
    assert np.isclose(intercept + slope * x.mean(), y.mean())

    fig, ax = plt.subplots(figsize=(9.2, 6.1))
    xx = np.linspace(0.6, 6.4, 200)
    ax.plot(xx, intercept + slope * xx, color=F.BLUE, lw=2.7,
            label=rf"$\hat y={intercept:.2f}+{slope:.2f}x$")
    ax.scatter(x, y, color=F.AMBER, s=80, zorder=5, label="觀測值")
    for xi, yi, pi in zip(x, y, prediction):
        ax.plot([xi, xi], [pi, yi], color=F.GREEN, lw=2, ls="--")
    ax.scatter([x.mean()], [y.mean()], color=F.INK, marker="D", s=80, zorder=6,
               label=rf"$(\bar x,\bar y)=({x.mean():g},{y.mean():g})$")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title("最小平方直線讓鉛直殘差平方和最小", fontsize=15)
    ax.legend(frameon=False, loc="upper left")
    F.clean_grid(ax)
    fig.tight_layout()
    return _save(fig, "數2-2-最小平方法.svg")


def fig_outlier():
    x = np.arange(1, 9, dtype=float)
    y = 2 * x + np.array([0.2, -0.5, 0.4, -0.2, 0.5, -0.3, 0.1, -0.4])
    out_x = np.append(x, 10.0)
    out_y = np.append(y, 0.0)
    r_clean = np.corrcoef(x, y)[0, 1]
    r_out = np.corrcoef(out_x, out_y)[0, 1]
    assert r_clean > 0.99
    assert r_out < 0.45

    fig, axes = plt.subplots(1, 2, figsize=(10.6, 4.7), sharex=True, sharey=True)
    axes[0].scatter(x, y, color=F.BLUE, s=65)
    axes[0].set_title(f"原資料：r={r_clean:.2f}", fontsize=13)
    axes[1].scatter(x, y, color=F.BLUE, s=65)
    axes[1].scatter([10.0], [0.0], color=F.AMBER, s=105, marker="D")
    axes[1].annotate("高影響點", (10.0, 0.0), xytext=(6.2, 4.0),
                     arrowprops=dict(arrowstyle="->", color=F.AMBER), color=F.AMBER, fontsize=11)
    axes[1].set_title(f"加入一點：r={r_out:.2f}", fontsize=13)
    for ax in axes:
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.set_xlim(0, 10.8)
        ax.set_ylim(0, 18)
        F.clean_grid(ax)
    fig.suptitle("散布圖能揭露單一資料點對相關係數的影響", fontsize=16)
    fig.tight_layout(rect=(0, 0, 1, 0.91))
    return _save(fig, "數2-2-離群值影響.svg")


if __name__ == "__main__":
    for entrypoint, _ in FIGURE_OUTPUTS:
        globals()[entrypoint]()
