# -*- coding: utf-8 -*-
"""產生「數1-2 多項式函數」的圖，輸出到該章 sources/。
重繪：  .venv/bin/python _tools/fig_數1-2.py
"""

import os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch
import figlib as F

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CH = os.path.join(ROOT, "數學", "數學一上（必修·第一冊）", "數1-2 多項式函數")


def _origin_axes(ax, xlim, ylim):
    """過原點的坐標軸樣式：隱藏外框，畫 x、y 軸線。"""
    ax.axhline(0, color=F.INK, lw=1.3, zorder=1)
    ax.axvline(0, color=F.INK, lw=1.3, zorder=1)
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    for s in ("top", "right", "left", "bottom"):
        ax.spines[s].set_visible(False)
    ax.grid(True, color=F.GRID, lw=0.8)
    ax.set_axisbelow(True)


def fig_completing_square():
    """二次函數配方：由 y=ax^2 平移到 y=a(x-h)^2+k，標出頂點、對稱軸。
    以 y = (x-2)^2 - 3 為例（a=1, h=2, k=-3），同時畫 y=x^2 作對照。"""
    fig, ax = F.canvas(6.6, 5.2)
    x = np.linspace(-4.2, 6.2, 400)
    y0 = x**2  # 基準拋物線 y = x^2
    h, k = 2.0, -3.0
    y1 = (x - h) ** 2 + k  # 平移後 y = (x-2)^2 - 3

    ax.plot(x, y0, color="#9aa4b2", lw=2.0, ls="--", label=r"$y=x^2$（基準）")
    ax.plot(x, y1, color=F.BLUE, lw=2.8, label=r"$y=(x-2)^2-3$")

    # 對稱軸 x = h
    ax.plot([h, h], [k - 0.4, 9.6], color=F.AMBER, lw=1.6, ls=":")
    ax.text(h + 0.12, 8.6, "對稱軸 $x=2$", color=F.AMBER, fontsize=12, ha="left")

    # 頂點
    ax.add_patch(Circle((h, k), 0.12, color=F.RED, zorder=6))
    ax.text(
        h + 0.25,
        k - 0.15,
        "頂點 $(2,\\,-3)$",
        color=F.RED,
        fontsize=12,
        ha="left",
        va="top",
    )
    # 原頂點（原點）
    ax.add_patch(Circle((0, 0), 0.10, color="#6b7280", zorder=6))

    # 平移箭頭：原點 -> 頂點
    arr = FancyArrowPatch(
        (0, 0),
        (h, k),
        arrowstyle="-|>",
        mutation_scale=18,
        lw=2.0,
        color=F.GREEN,
        zorder=5,
        connectionstyle="arc3,rad=-0.25",
        shrinkA=6,
        shrinkB=8,
    )
    ax.add_patch(arr)
    ax.text(
        0.55, -1.7, "右移 2、下移 3", color=F.GREEN, fontsize=12, ha="left", va="center"
    )

    _origin_axes(ax, (-4.2, 6.2), (-4.2, 10.0))
    ax.set_title("配方法：把二次函數化為頂點式 $y=a(x-h)^2+k$", fontsize=13)
    ax.legend(loc="upper left", fontsize=11, framealpha=0.9)
    fig.tight_layout()
    F.save_to(fig, CH, "數1-2-二次函數配方")


def fig_cubic_features():
    """三次函數圖形特徵：對稱中心（點對稱）、大域由最高次項決定、局部近似直線。
    以 f(x) = x^3 - 3x 為例，對稱中心在原點。"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.4, 4.6))

    # 左：整體圖形 + 對稱中心
    x = np.linspace(-2.6, 2.6, 400)
    y = x**3 - 3 * x
    ax1.plot(x, y, color=F.BLUE, lw=2.8)
    # 對稱中心
    ax1.add_patch(Circle((0, 0), 0.11, color=F.RED, zorder=6))
    ax1.text(0.18, 0.5, "對稱中心 $(0,0)$", color=F.RED, fontsize=12, ha="left")
    # 點對稱示意：(1,-2) 與 (-1,2)
    for px, py in [(1.0, -2.0), (-1.0, 2.0)]:
        ax1.add_patch(Circle((px, py), 0.09, color=F.GREEN, zorder=6))
    ax1.plot([1.0, -1.0], [-2.0, 2.0], color=F.GREEN, lw=1.3, ls=":")
    ax1.text(1.05, -2.35, "$(1,-2)$", color=F.GREEN, fontsize=11, ha="left", va="top")
    ax1.text(
        -1.05, 2.35, "$(-1,2)$", color=F.GREEN, fontsize=11, ha="right", va="bottom"
    )
    _origin_axes(ax1, (-2.8, 2.8), (-4.2, 4.2))
    ax1.set_title("整體：關於中心點對稱（$f(x)=x^3-3x$）", fontsize=12.5)

    # 右：大域 vs 局部
    xg = np.linspace(-3.4, 3.4, 400)
    yg = xg**3 - 3 * xg
    ax2.plot(xg, yg, color=F.BLUE, lw=2.6, label="三次函數")
    # 大域：最高次項 x^3 主導（畫 y=x^3 虛線比較）
    ax2.plot(xg, xg**3, color="#9aa4b2", lw=1.8, ls="--", label=r"$y=x^3$（大域趨勢）")
    # 局部：在 x=0 附近近似切線 y = -3x
    xl = np.linspace(-1.0, 1.0, 50)
    ax2.plot(xl, -3 * xl, color=F.AMBER, lw=2.2, label=r"局部切線 $y=-3x$")
    ax2.text(1.6, 7.5, "大域：由 $x^3$ 決定", color="#6b7280", fontsize=11, ha="center")
    ax2.text(-1.7, -7.5, "局部：近似一直線", color=F.AMBER, fontsize=11, ha="center")
    _origin_axes(ax2, (-3.6, 3.6), (-11, 11))
    ax2.set_title("大域看最高次項，局部近似直線", fontsize=12.5)
    ax2.legend(loc="upper left", fontsize=10, framealpha=0.9)

    fig.tight_layout()
    F.save_to(fig, CH, "數1-2-三次函數特徵")


def fig_quadratic_inequality():
    """二次不等式：拋物線與 x 軸交點、解區間上色。
    以 y = x^2 - x - 6 = (x-3)(x+2) 為例，根 x=-2,3。
    左：x^2 - x - 6 > 0（取兩側）；右：x^2 - x - 6 < 0（取中間）。"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.4, 4.6))
    x = np.linspace(-4.0, 5.0, 500)
    y = x**2 - x - 6
    r1, r2 = -2.0, 3.0

    for ax, mode in [(ax1, ">"), (ax2, "<")]:
        ax.plot(x, y, color=F.BLUE, lw=2.8)
        # 根
        for r in (r1, r2):
            ax.add_patch(Circle((r, 0), 0.13, color=F.RED, zorder=6))
        ax.text(r1, -1.1, "$x=-2$", color=F.RED, fontsize=12, ha="center", va="top")
        ax.text(r2, -1.1, "$x=3$", color=F.RED, fontsize=12, ha="center", va="top")

        if mode == ">":
            # y>0：x<-2 或 x>3（曲線在 x 軸上方）
            mask = y > 0
            ax.fill_between(x, 0, y, where=mask, color=F.AMBER, alpha=0.22)
            # 數線解區間（畫在底部）
            yb = -9.5
            ax.plot([-4.0, r1], [yb, yb], color=F.AMBER, lw=4, solid_capstyle="butt")
            ax.plot([r2, 5.0], [yb, yb], color=F.AMBER, lw=4, solid_capstyle="butt")
            ax.add_patch(Circle((r1, yb), 0.16, fill=False, ec=F.AMBER, lw=2, zorder=6))
            ax.add_patch(Circle((r2, yb), 0.16, fill=False, ec=F.AMBER, lw=2, zorder=6))
            ax.set_title(r"$x^2-x-6>0$：取圖形在 $x$ 軸上方", fontsize=12.5)
            ax.text(
                0.5,
                5.5,
                "解：$x<-2$ 或 $x>3$",
                color=F.AMBER,
                fontsize=12.5,
                ha="center",
            )
        else:
            # y<0：-2<x<3（曲線在 x 軸下方）
            mask = y < 0
            ax.fill_between(x, 0, y, where=mask, color=F.GREEN, alpha=0.22)
            yb = -9.5
            ax.plot([r1, r2], [yb, yb], color=F.GREEN, lw=4, solid_capstyle="butt")
            ax.add_patch(Circle((r1, yb), 0.16, fill=False, ec=F.GREEN, lw=2, zorder=6))
            ax.add_patch(Circle((r2, yb), 0.16, fill=False, ec=F.GREEN, lw=2, zorder=6))
            ax.set_title(r"$x^2-x-6<0$：取圖形在 $x$ 軸下方", fontsize=12.5)
            ax.text(0.5, 5.5, "解：$-2<x<3$", color=F.GREEN, fontsize=12.5, ha="center")

        _origin_axes(ax, (-4.0, 5.0), (-10.5, 9.0))

    fig.tight_layout()
    F.save_to(fig, CH, "數1-2-二次不等式")


def fig_interval_extremum():
    """閉區間 [p,q] 上的二次極值：對稱軸落在區間內 vs 區間外。
    用例題 2-6.5 的同一函數 f(x)=x^2-4x+1=(x-2)^2-3，頂點 (2,-3)，開口向上。
    左：區間 [0,3]，對稱軸 x=2 在區間內 → 最小值在頂點、最大值在較遠端點 x=0。
    右：區間 [3,5]，對稱軸 x=2 在區間外（左側）→ 區段單調，最值都在兩端點。"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.4, 4.6))
    h, k = 2.0, -3.0  # 頂點

    def f(t):
        return (t - h) ** 2 + k

    xfull = np.linspace(-1.0, 6.0, 500)
    yfull = f(xfull)

    for ax, (p, q), inside in [(ax1, (0.0, 3.0), True), (ax2, (3.0, 5.0), False)]:
        # 整條拋物線（淡色），凸顯定義域外不算
        ax.plot(xfull, yfull, color="#9aa4b2", lw=1.6, ls="--", zorder=2)
        # 區間 [p,q] 上的圖形（粗藍實線）
        xs = np.linspace(p, q, 300)
        ax.plot(xs, f(xs), color=F.BLUE, lw=3.0, zorder=4)

        # 對稱軸 x=h
        ax.plot([h, h], [-4.0, 9.0], color=F.AMBER, lw=1.5, ls=":", zorder=3)
        ax.text(h + 0.1, 8.4, "對稱軸 $x=2$", color=F.AMBER, fontsize=11.5, ha="left")

        # 區間端點鉛直虛線 + 區間底部標示
        for r in (p, q):
            ax.plot([r, r], [-4.0, f(r)], color="#6b7280", lw=1.0, ls=":", zorder=3)
        yb = -5.4
        ax.plot([p, q], [yb, yb], color=F.GREEN, lw=4, solid_capstyle="butt", zorder=4)
        for r in (p, q):
            ax.add_patch(Circle((r, yb), 0.10, color=F.GREEN, zorder=6))
        ax.text(
            (p + q) / 2,
            yb - 0.9,
            "定義域 $[%d,\\,%d]$" % (int(p), int(q)),
            color=F.GREEN,
            fontsize=11.5,
            ha="center",
            va="top",
        )

        # 端點函數值的點
        for r in (p, q):
            ax.add_patch(Circle((r, f(r)), 0.11, color=F.INK, zorder=6))

        if inside:
            # 頂點是最小值
            ax.add_patch(Circle((h, k), 0.13, color=F.RED, zorder=7))
            ax.text(
                h + 0.2,
                k - 0.2,
                "最小值 $f(2)=-3$",
                color=F.RED,
                fontsize=11.5,
                ha="left",
                va="top",
            )
            # 最大值在較遠端點 x=0（距軸 2 > x=3 距軸 1）
            ax.add_patch(
                Circle((p, f(p)), 0.15, fill=False, ec=F.RED, lw=2.2, zorder=7)
            )
            ax.text(
                p + 0.15,
                f(p) + 0.4,
                "最大值 $f(0)=1$\n（離軸較遠端）",
                color=F.RED,
                fontsize=11,
                ha="left",
                va="bottom",
            )
            ax.text(
                3.0,
                6.6,
                "對稱軸在區間內\n頂點即最小值",
                color=F.INK,
                fontsize=11.5,
                ha="center",
                va="center",
            )
            ax.set_title("對稱軸落在區間內（$[0,3]$）", fontsize=12.5)
        else:
            # 區間單調遞增，最值都在端點
            ax.add_patch(
                Circle((p, f(p)), 0.15, fill=False, ec=F.RED, lw=2.2, zorder=7)
            )
            ax.text(
                p - 0.15,
                f(p) - 0.3,
                "最小值 $f(3)=-2$",
                color=F.RED,
                fontsize=11,
                ha="right",
                va="top",
            )
            ax.add_patch(
                Circle((q, f(q)), 0.15, fill=False, ec=F.RED, lw=2.2, zorder=7)
            )
            ax.text(
                q - 0.1,
                f(q) + 0.3,
                "最大值 $f(5)=6$",
                color=F.RED,
                fontsize=11,
                ha="right",
                va="bottom",
            )
            ax.text(
                4.0,
                -2.2,
                "對稱軸在區間外\n區段單調，最值都在端點\n（頂點取不到）",
                color=F.INK,
                fontsize=11,
                ha="center",
                va="center",
            )
            ax.set_title("對稱軸落在區間外（$[3,5]$）", fontsize=12.5)

        _origin_axes(ax, (-1.2, 6.2), (-6.6, 9.0))

    fig.tight_layout()
    F.save_to(fig, CH, "數1-2-區間極值")


if __name__ == "__main__":
    fig_completing_square()
    fig_cubic_features()
    fig_quadratic_inequality()
    fig_interval_extremum()
    print("done.")
