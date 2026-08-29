# -*- coding: utf-8 -*-
"""重生「數1-2 指數與常用對數」學生講義的章內 SVG。"""

if __name__ == "__main__" and __import__("sys").argv[1:]:
    raise SystemExit("本腳本不接受參數；直接執行即可重生數1-2 章內 SVG。")

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import matplotlib.pyplot as plt
import numpy as np

import figlib as F


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHAPTER = os.path.join(ROOT, "content", "必修數學", "數1-2")

FIGURE_OUTPUTS = (
    ("fig_integer_exponents", "數1-2-整數指數延伸.svg"),
    ("fig_real_exponent_limit", "數1-2-實數指數逼近.svg"),
    ("fig_scientific_notation", "數1-2-科學記號.svg"),
    ("fig_multiplier_timeline", "數1-2-倍率模型.svg"),
    ("fig_log_scale", "數1-2-常用對數尺度.svg"),
)


def _save(fig, filename):
    stem, extension = os.path.splitext(filename)
    if extension != ".svg" or not stem.startswith("數1-2-"):
        raise AssertionError("輸出檔名必須是數1-2 章內 SVG")
    return F.save_to(fig, CHAPTER, stem, output_subdir="assets", write_pdf=False)


def fig_integer_exponents():
    exponents = np.arange(-3, 4)
    values = 2.0 ** exponents
    assert np.allclose(values, [1 / 8, 1 / 4, 1 / 2, 1, 2, 4, 8])
    assert np.allclose(values[1:] / values[:-1], 2)

    fig, ax = plt.subplots(figsize=(10.4, 4.5))
    ax.plot(exponents, values, color=F.BLUE, lw=2.4, zorder=2)
    ax.scatter(exponents, values, color=F.BLUE, s=58, zorder=3)
    for n, value in zip(exponents, values):
        label = f"$2^{{{n}}}={value:g}$" if value >= 1 else f"$2^{{{n}}}=1/{int(round(1/value))}$"
        offset = 12 if n != 3 else -24
        ax.annotate(label, (n, value), xytext=(0, offset), textcoords="offset points",
                    ha="center", fontsize=10, color=F.INK)
    for n in range(-3, 3):
        ax.annotate("", xy=(n + 0.82, max(values[n + 3], values[n + 4]) * 0.72),
                    xytext=(n + 0.18, max(values[n + 3], values[n + 4]) * 0.72),
                    arrowprops=dict(arrowstyle="->", color=F.GREEN, lw=1.6))
    ax.text(-2.55, 5.7, "指數每增加 1，數值乘 2", color=F.GREEN, fontsize=12)
    ax.set_xticks(exponents)
    ax.set_xlabel("指數 n")
    ax.set_ylabel(r"$2^n$")
    ax.set_ylim(0, 9.2)
    ax.set_title("保持相鄰倍率不變，零次方與負次方就被唯一決定", fontsize=15)
    F.clean_grid(ax)
    fig.tight_layout()
    return _save(fig, "數1-2-整數指數延伸.svg")


def fig_real_exponent_limit():
    target = np.sqrt(2)
    approximations = np.array([1.4, 1.41, 1.414, 1.4142, target])
    values = 2.0 ** approximations
    target_value = 2.0 ** target
    assert abs(target_value - 2.665144142690225) < 1e-12
    assert np.all(np.diff(values) > 0)

    x = np.linspace(1.37, 1.445, 400)
    y = 2.0 ** x
    fig, ax = plt.subplots(figsize=(9.7, 5.1))
    ax.plot(x, y, color=F.BLUE, lw=2.8, label=r"$y=2^x$")
    ax.scatter(approximations[:-1], values[:-1], color=F.GREEN, s=55, zorder=4, label="有理數近似")
    ax.scatter([target], [target_value], color=F.AMBER, s=95, zorder=5, label=r"$x=\sqrt{2}$")
    ax.axvline(target, color=F.GRID, ls="--", lw=1.4)
    ax.axhline(target_value, color=F.GRID, ls="--", lw=1.4)
    ax.annotate(r"$2^{\sqrt{2}}\approx2.665144$", xy=(target, target_value),
                xytext=(1.417, 2.648), arrowprops=dict(arrowstyle="->", color=F.AMBER, lw=1.6),
                color=F.AMBER, fontsize=12)
    ax.set_xlabel("指數 x")
    ax.set_ylabel(r"$2^x$")
    ax.set_title(r"用有理數逐步逼近 $\sqrt{2}$，相應的 $2^x$ 也逼近唯一數值", fontsize=15)
    ax.legend(frameon=False, loc="lower right")
    F.clean_grid(ax)
    fig.tight_layout()
    return _save(fig, "數1-2-實數指數逼近.svg")


def fig_scientific_notation():
    samples = (15200000.0, 0.0010246)
    coefficients = (1.52, 1.0246)
    powers = (7, -3)
    assert np.isclose(coefficients[0] * 10 ** powers[0], samples[0])
    assert np.isclose(coefficients[1] * 10.0 ** powers[1], samples[1])

    fig, axes = plt.subplots(2, 1, figsize=(10.4, 4.6))
    entries = (
        ("15,200,000", r"$1.52\times10^7$", 7, F.BLUE),
        ("0.0010246", r"$1.0246\times10^{-3}$", -3, F.GREEN),
    )
    for ax, (raw, scientific, power, color) in zip(axes, entries):
        ax.set_xlim(-5, 9)
        ax.set_ylim(-0.55, 0.85)
        ax.axhline(0, color=F.INK, lw=1.8)
        ax.set_xticks(range(-5, 10))
        ax.set_yticks([])
        for side in ax.spines.values():
            side.set_visible(False)
        ax.scatter([power], [0], s=105, color=color, zorder=4)
        label_x = power - 1.5 if power > 0 else power + 3.0
        ax.annotate("小數點移動的位數", xy=(power, 0), xytext=(label_x, 0.30),
                    ha="center", arrowprops=dict(arrowstyle="->", color=color, lw=1.5),
                    color=color, fontsize=10)
        ax.text(-4.8, 0.67, f"{raw}  =  {scientific}", fontsize=14, color=F.INK, va="center")
    axes[1].set_xlabel("10 的指數 n（數值落在 $[10^n,10^{n+1})$）")
    fig.suptitle(r"科學記號 $a\times10^n$：$1\leq |a|<10$，指數記錄數量級", fontsize=15)
    fig.tight_layout(rect=(0, 0, 1, 0.91))
    return _save(fig, "數1-2-科學記號.svg")


def fig_multiplier_timeline():
    q0, factor, period = 80.0, 1.5, 2.0
    times = np.arange(-4, 9, 2)
    quantities = q0 * factor ** (times / period)
    assert np.isclose(quantities[times.tolist().index(0)], q0)
    assert np.allclose(quantities[1:] / quantities[:-1], factor)

    fig, ax = plt.subplots(figsize=(10.6, 4.5))
    ax.plot(times, quantities, color=F.BLUE, lw=2.6)
    ax.scatter(times, quantities, color=F.BLUE, s=62, zorder=4)
    for t, q in zip(times, quantities):
        ax.annotate(f"{q:.1f}", (t, q), xytext=(0, 9), textcoords="offset points",
                    ha="center", fontsize=9)
    ax.axvline(0, color=F.GRID, ls="--", lw=1.3)
    ax.text(0.15, 35, "基準時刻\n$Q_0=80$", color=F.AMBER, fontsize=11)
    ax.text(-3.8, 315, r"$Q(t)=80(1.5)^{t/2}$", color=F.BLUE, fontsize=14)
    ax.set_xlabel("時間 t（日）")
    ax.set_ylabel("數量 Q(t)")
    ax.set_title("固定時間間隔乘同一倍率：整數、負數與分數指數共用一個模型", fontsize=15)
    F.clean_grid(ax)
    fig.tight_layout()
    return _save(fig, "數1-2-倍率模型.svg")


def fig_log_scale():
    raw = 10.0 ** np.arange(-4, 5)
    logs = np.log10(raw)
    assert np.allclose(logs, np.arange(-4, 5))
    assert np.allclose(raw[1:] / raw[:-1], 10)

    fig, ax = plt.subplots(figsize=(10.6, 4.5))
    ax.set_xlim(-4.5, 4.5)
    ax.set_ylim(-0.2, 2.2)
    ax.axhline(0.45, color=F.INK, lw=2)
    ax.axhline(1.55, color=F.INK, lw=2)
    for x, value in zip(logs, raw):
        ax.plot([x, x], [0.36, 0.54], color=F.INK, lw=1.3)
        ax.plot([x, x], [1.46, 1.64], color=F.INK, lw=1.3)
        raw_label = rf"$10^{{{int(x)}}}$" if int(x) != 0 else "$1$"
        ax.text(x, 0.16, raw_label, ha="center", fontsize=10)
        ax.text(x, 1.78, f"{int(x)}", ha="center", fontsize=10, color=F.BLUE)
    ax.text(-4.45, 0.78, "原始正數 N：相鄰刻度相差 10 倍", color=F.INK, fontsize=11)
    ax.text(-4.45, 2.05, r"常用對數 $\log N$：相鄰刻度相差 1", color=F.BLUE, fontsize=11)
    ax.annotate("乘 10", xy=(2, 1.18), xytext=(1, 1.18),
                arrowprops=dict(arrowstyle="<->", color=F.GREEN, lw=1.8),
                ha="center", va="bottom", color=F.GREEN, fontsize=11)
    ax.axis("off")
    ax.set_title("常用對數把倍率轉成加法距離", fontsize=15)
    fig.tight_layout()
    return _save(fig, "數1-2-常用對數尺度.svg")


if __name__ == "__main__":
    for entrypoint, filename in FIGURE_OUTPUTS:
        output = globals()[entrypoint]()
        if os.path.basename(output) != filename:
            raise AssertionError(f"{entrypoint} 輸出與 FIGURE_OUTPUTS 不一致")
