# -*- coding: utf-8 -*-
"""產生「選物I-1 測量與不確定度」的圖，輸出到該章 sources/。
重繪：  .venv/bin/python _tools/fig_選物I-1.py
"""

import os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyBboxPatch, Rectangle
import figlib as F

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CH = os.path.join(
    ROOT, "物理", "物理二上（選修物理I·力學一）", "選物I-1 測量與不確定度"
)


def fig_error_types():
    """系統誤差 vs 隨機誤差：靶心 + 一維分布雙列示意。"""
    rng = np.random.default_rng(11)
    fig, axes = plt.subplots(2, 2, figsize=(8.6, 6.6))

    # 第一列：靶心圖（呼應準確度/精密度）
    # (標題, 偏移 bias, 散布 spread)
    targets = [
        ("只有隨機誤差\n（準但不夠精密）", (0.0, 0.0), 0.62),
        ("有系統誤差\n（精密但不準，整批偏掉）", (0.95, 0.70), 0.16),
    ]
    for ax, (title, bias, spread) in zip(axes[0], targets):
        for r, col in [
            (1.7, "#eef1f5"),
            (1.2, "#dbe7ff"),
            (0.7, "#bcd3ff"),
            (0.2, F.RED),
        ]:
            ax.add_patch(
                Circle((0, 0), r, facecolor=col, edgecolor="#aab4c2", lw=0.8, zorder=1)
            )
        n = 9
        x = rng.normal(bias[0], spread, n)
        y = rng.normal(bias[1], spread, n)
        ax.scatter(
            x, y, s=46, color=F.INK, edgecolors="white", linewidths=0.8, zorder=5
        )
        # 標出平均落點
        ax.scatter(
            [x.mean()],
            [y.mean()],
            s=120,
            marker="+",
            color=F.GREEN,
            linewidths=2.4,
            zorder=6,
        )
        ax.set_xlim(-2.1, 2.1)
        ax.set_ylim(-2.1, 2.1)
        ax.set_aspect("equal")
        ax.set_xticks([])
        ax.set_yticks([])
        for s in ("top", "right", "bottom", "left"):
            ax.spines[s].set_color("#aab4c2")
        ax.set_title(title, fontsize=11.5)

    # 第二列：一維數線上的分布（真值 vs 測量值散布）
    axes_b = axes[1]
    for ax, kind in zip(axes_b, ["random", "systematic"]):
        true_val = 0.0
        if kind == "random":
            data = rng.normal(0.0, 0.75, 200)
            label = "隨機誤差：散開、但對稱地圍著真值"
            mean = data.mean()
        else:
            data = rng.normal(1.1, 0.28, 200)
            label = "系統誤差：整批被推離真值（綠＝量測平均）"
            mean = data.mean()
        ax.hist(
            data,
            bins=22,
            range=(-2.4, 2.4),
            color=F.BLUE,
            alpha=0.35,
            edgecolor="white",
            lw=0.5,
        )
        ax.axvline(true_val, color=F.RED, lw=2.2, label="真值")
        ax.axvline(mean, color=F.GREEN, lw=2.2, ls="--", label="量測平均")
        ax.set_xlim(-2.4, 2.4)
        ax.set_yticks([])
        ax.set_xlabel("測量值")
        ax.set_title(label, fontsize=10.5)
        ax.legend(loc="upper right", fontsize=8.5, frameon=False)
        for s in ("top", "right", "left"):
            ax.spines[s].set_visible(False)

    fig.suptitle(
        "兩種誤差：隨機誤差讓點「散開」，系統誤差讓整批「偏掉」", fontsize=13.5, y=1.0
    )
    fig.tight_layout(rect=[0, 0, 1, 0.97])
    F.save_to(fig, CH, "選物I-1-誤差類型")


def fig_distribution():
    """多次測量的直方圖 + 平均值 ± 標準差。"""
    rng = np.random.default_rng(4)
    # 模擬量某段長度（真值約 10.00 cm），200 次讀數
    data = rng.normal(10.00, 0.08, 200)
    mean = data.mean()
    sd = data.std(ddof=1)

    fig, ax = F.canvas(7.4, 4.4)
    counts, bins, _ = ax.hist(
        data,
        bins=24,
        color=F.BLUE,
        alpha=0.35,
        edgecolor="white",
        lw=0.6,
        label="200 次讀數",
    )
    top = counts.max()

    # 平均值
    ax.axvline(mean, color=F.RED, lw=2.4, label=f"平均值 $\\bar{{x}}$ = {mean:.2f} cm")
    # ±1 標準差帶
    ax.axvspan(mean - sd, mean + sd, color=F.GREEN, alpha=0.12)
    ax.axvline(mean - sd, color=F.GREEN, lw=1.6, ls="--")
    ax.axvline(
        mean + sd,
        color=F.GREEN,
        lw=1.6,
        ls="--",
        label=f"$\\bar{{x}}\\pm s$（$s={sd:.2f}$ cm）",
    )

    # 標準差雙箭頭
    yarr = top * 0.86
    F.arrow(ax, (mean, yarr), (mean + sd, yarr), color=F.GREEN, lw=1.8, mutation=14)
    F.arrow(ax, (mean, yarr), (mean - sd, yarr), color=F.GREEN, lw=1.8, mutation=14)
    ax.text(
        mean, yarr * 1.06, "離散程度 ~ $s$", ha="center", color=F.GREEN, fontsize=11
    )

    ax.set_xlabel("單次測量值 $x_i$ (cm)")
    ax.set_ylabel("出現次數")
    ax.set_title("多次測量的分布：平均值定「中心」，標準差定「寬度」")
    F.clean_grid(ax)
    ax.legend(loc="upper left", fontsize=9.5, frameon=False)
    F.save_to(fig, CH, "選物I-1-多次測量分布")


def fig_propagation():
    """不確定度傳遞：加減（絕對相加）vs 乘除（相對相加）兩格示意。"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.6, 4.4))

    # ---- 左：加減，絕對不確定度相加（數線上區間相加）----
    ax1.set_xlim(0, 12)
    ax1.set_ylim(0, 6)
    ax1.axis("off")
    ax1.set_title("加減法：絕對不確定度相加", fontsize=12.5)

    def bar(ax, y, x0, val, unc, color, name):
        ax.plot(
            [x0 + val - unc, x0 + val + unc],
            [y, y],
            color=color,
            lw=3.0,
            solid_capstyle="butt",
        )
        ax.plot([x0 + val, x0 + val], [y - 0.18, y + 0.18], color=color, lw=2.4)
        for e in (-unc, unc):
            ax.plot(
                [x0 + val + e, x0 + val + e], [y - 0.13, y + 0.13], color=color, lw=2.0
            )
        ax.text(x0 + val, y + 0.42, name, ha="center", color=color, fontsize=11)

    bar(ax1, 5.0, 1.0, 3.0, 0.6, F.BLUE, "$A = 3.0 \\pm 0.6$")
    bar(ax1, 3.6, 1.0, 4.0, 0.8, F.RED, "$B = 4.0 \\pm 0.8$")
    ax1.plot([0.6, 11.4], [2.6, 2.6], color="#cbd2da", lw=1.0)
    bar(ax1, 1.7, 1.0, 7.0, 1.4, F.GREEN, "$A+B = 7.0 \\pm 1.4$")
    ax1.text(
        6.0,
        0.65,
        r"$\Delta(A{+}B)=\Delta A+\Delta B=0.6+0.8=1.4$",
        ha="center",
        color=F.INK,
        fontsize=10.5,
    )

    # ---- 右：乘除，相對不確定度相加（圓餅式條形）----
    ax2.set_xlim(0, 10)
    ax2.set_ylim(0, 6)
    ax2.axis("off")
    ax2.set_title("乘除法：相對不確定度相加", fontsize=12.5)

    def relbar(ax, y, frac, color, name):
        x0, w = 1.0, 7.0
        ax.add_patch(
            Rectangle(
                (x0, y - 0.22),
                w,
                0.44,
                facecolor="#eef1f5",
                edgecolor="#aab4c2",
                lw=0.8,
            )
        )
        ax.add_patch(
            Rectangle(
                (x0, y - 0.22),
                w * frac,
                0.44,
                facecolor=color,
                alpha=0.55,
                edgecolor="none",
            )
        )
        ax.text(
            x0 + w + 0.2, y, name, ha="left", va="center", color=color, fontsize=10.5
        )

    relbar(ax2, 5.0, 0.05, F.BLUE, "$\\dfrac{\\Delta A}{A}=5\\%$")
    relbar(ax2, 3.8, 0.04, F.RED, "$\\dfrac{\\Delta B}{B}=4\\%$")
    ax2.plot([0.7, 9.3], [3.0, 3.0], color="#cbd2da", lw=1.0)
    relbar(ax2, 2.0, 0.09, F.GREEN, "$\\dfrac{\\Delta(AB)}{AB}=9\\%$")
    ax2.text(
        5.0,
        0.7,
        r"$\frac{\Delta(AB)}{AB}=\frac{\Delta A}{A}+\frac{\Delta B}{B}=5\%+4\%=9\%$",
        ha="center",
        color=F.INK,
        fontsize=10.5,
    )

    fig.suptitle(
        "不確定度怎麼「傳遞」：加減看絕對量、乘除看相對量（百分比）", fontsize=13, y=1.0
    )
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    F.save_to(fig, CH, "選物I-1-不確定度傳遞")


if __name__ == "__main__":
    fig_error_types()
    fig_distribution()
    fig_propagation()
    print("done.")
