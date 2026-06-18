# -*- coding: utf-8 -*-
"""產生「必物-3 物質的組成與交互作用」的圖，輸出到該章 sources/。
重繪：  .venv/bin/python _tools/fig_必物-3.py
"""

import os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon, Circle, FancyBboxPatch
import figlib as F

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CH = os.path.join(ROOT, "物理", "物理一（必修物理）", "必物-3 物質的組成與交互作用")


def fig_hierarchy():
    """物質的組成階層：巨觀→分子→原子→核＋電子→質子中子→夸克，附尺度數量級。"""
    fig, ax = F.schematic(8.6, 5.6)

    rows = [
        ("巨觀物質", "一塊冰、一滴水", r"$\sim 10^{-2}$ m", "#dbe7ff"),
        ("分子", "水分子 H$_2$O", r"$\sim 10^{-9}$ m", "#dbe7ff"),
        ("原子", "氫、氧、碳…", r"$\sim 10^{-10}$ m", "#cfe8d8"),
        ("原子核 ＋ 電子", "核居中，電子在外", r"核 $\sim 10^{-15}$ m", "#ffe2c2"),
        ("質子 ＋ 中子", "組成原子核的核子", r"$\sim 10^{-15}$ m", "#ffe2c2"),
        ("夸克", "u、d 夸克（看不到單獨的）", r"$< 10^{-18}$ m", "#f3d6f0"),
    ]
    n = len(rows)
    y0, dy = 4.7, 0.92
    for i, (name, eg, scale, col) in enumerate(rows):
        y = y0 - i * dy
        ax.add_patch(
            FancyBboxPatch(
                (-3.9, y - 0.32),
                4.4,
                0.64,
                boxstyle="round,pad=0.02,rounding_size=0.12",
                facecolor=col,
                edgecolor=F.INK,
                lw=1.4,
                zorder=3,
            )
        )
        ax.text(-3.6, y, name, ha="left", va="center", fontsize=13, zorder=5)
        ax.text(
            0.62, y, eg, ha="left", va="center", fontsize=10.5, color="#555", zorder=5
        )
        ax.text(
            4.05,
            y,
            scale,
            ha="right",
            va="center",
            fontsize=11.5,
            color=F.RED,
            zorder=5,
        )
        if i < n - 1:
            F.arrow(
                ax,
                (-1.7, y - 0.33),
                (-1.7, y - dy + 0.33),
                color="#6b7280",
                lw=1.8,
                mutation=14,
            )
    ax.text(
        -1.7,
        y0 + 0.62,
        "「放大來看」一層一層拆開",
        ha="center",
        fontsize=12,
        color=F.INK,
    )
    ax.text(4.05, y0 + 0.62, "尺度", ha="right", fontsize=11.5, color=F.RED)
    ax.set_xlim(-4.3, 4.3)
    ax.set_ylim(y0 - (n - 1) * dy - 0.7, y0 + 1.0)
    ax.set_title("物質的組成階層", fontsize=14)
    F.save_to(fig, CH, "必物-3-物質階層")


def fig_rutherford():
    """拉塞福金箔散射：α 粒子多數穿透、少數大角度反彈 → 核式原子。"""
    fig, ax = F.schematic(8.4, 5.0)

    # 金箔（一排原子，核在中央）
    foil_x = 1.7
    ax.add_patch(
        Rectangle(
            (foil_x - 0.18, -2.3),
            0.36,
            4.6,
            facecolor="#fff2cc",
            edgecolor="#bf8700",
            lw=1.4,
            alpha=0.7,
            zorder=1,
        )
    )
    ax.text(foil_x, 2.55, "金箔", ha="center", fontsize=12, color="#9a6700")
    nuclei_y = [-1.7, -0.85, 0.0, 0.85, 1.7]
    for ny in nuclei_y:
        ax.add_patch(Circle((foil_x, ny), 0.09, color=F.RED, zorder=4))

    # α 射源
    ax.text(
        -3.7,
        0.0,
        r"$\alpha$ 粒子源",
        ha="center",
        va="center",
        fontsize=12,
        color=F.INK,
    )
    ax.add_patch(
        Rectangle(
            (-4.3, -0.45),
            0.95,
            0.9,
            facecolor="#eef1f5",
            edgecolor=F.INK,
            lw=1.3,
            zorder=2,
        )
    )

    # 多數：直直穿透
    for sy in [-1.25, -0.42, 0.42, 1.25]:
        F.arrow(ax, (-3.25, sy), (3.7, sy), color=F.BLUE, lw=1.8, mutation=12)
    ax.text(
        3.3,
        -1.7,
        "絕大多數\n直直穿過",
        color=F.BLUE,
        fontsize=11,
        ha="center",
        va="center",
    )

    # 少數：擊中核 → 大角度偏折／反彈
    F.arrow(ax, (-3.25, 0.0), (foil_x - 0.05, 0.0), color=F.AMBER, lw=2.2, mutation=12)
    F.arrow(ax, (foil_x, 0.0), (foil_x - 2.4, 1.7), color=F.AMBER, lw=2.2, mutation=14)
    ax.text(
        -1.4,
        2.1,
        "極少數\n大角度反彈",
        color=F.AMBER,
        fontsize=11,
        ha="center",
        va="center",
    )
    # 一條中等偏折
    F.arrow(
        ax, (-3.25, 0.85), (foil_x, 0.85), color=F.AMBER, lw=2.0, mutation=12, alpha=0.5
    )
    F.arrow(
        ax, (foil_x, 0.85), (3.4, 2.0), color=F.AMBER, lw=2.0, mutation=14, alpha=0.7
    )

    ax.text(
        foil_x + 0.55,
        -2.55,
        "紅點＝原子核（很小、很重、帶正電，集中了幾乎全部質量）",
        ha="center",
        fontsize=10.5,
        color=F.RED,
    )
    ax.set_xlim(-4.6, 4.2)
    ax.set_ylim(-3.0, 3.0)
    ax.set_title("拉塞福金箔散射 → 核式原子", fontsize=14)
    F.save_to(fig, CH, "必物-3-拉塞福散射")


def fig_four_forces():
    """四種基本交互作用：相對強度（對數）、作用範圍比較。"""
    fig, ax = F.canvas(7.6, 4.6)

    names = ["重力", "弱力", "電磁力", "強力"]
    # 以強力為基準的相對強度（數量級，便於教學）
    rel = [1e-38, 1e-13, 1e-2, 1.0]
    ranges = ["無限遠", r"$\sim10^{-18}$ m", "無限遠", r"$\sim10^{-15}$ m"]
    cols = [F.RED, F.PURPLE, F.BLUE, F.AMBER]

    ypos = np.arange(len(names))[::-1]
    logvals = [np.log10(r) for r in rel]
    base = -40
    bars = [lv - base for lv in logvals]
    ax.barh(ypos, bars, color=cols, alpha=0.85, height=0.55, left=base, zorder=3)

    for y, name, lv, rng in zip(ypos, names, logvals, ranges):
        ax.text(
            base + 0.4,
            y,
            name,
            va="center",
            ha="left",
            fontsize=12.5,
            color="white",
            zorder=5,
            fontweight="bold",
        )
        ax.text(
            lv + 0.6,
            y,
            f"$10^{{{int(round(lv))}}}$",
            va="center",
            ha="left",
            fontsize=12,
            color=F.INK,
            zorder=5,
        )
        ax.text(
            lv + 0.6,
            y - 0.30,
            f"作用範圍：{rng}",
            va="center",
            ha="left",
            fontsize=9.5,
            color="#666",
            zorder=5,
        )

    ax.set_xlim(base, 4)
    ax.set_ylim(-0.7, len(names) - 0.25)
    ax.set_yticks([])
    ax.set_xlabel("相對強度（以強力 = $10^0$ 為基準，橫軸為 10 的次方）")
    ax.set_title("自然界四種基本交互作用：強度天差地遠", fontsize=13.5)
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.set_xticks([-40, -30, -20, -10, 0])
    ax.set_xticklabels(
        ["$10^{-40}$", "$10^{-30}$", "$10^{-20}$", "$10^{-10}$", "$10^{0}$"]
    )
    fig.tight_layout()
    F.save_to(fig, CH, "必物-3-四種交互作用")


def fig_nuclear_balance():
    """核內力平衡：質子間電斥力 vs 強力吸引示意。"""
    fig, ax = F.schematic(7.4, 4.6)

    # 兩個質子
    p1 = np.array([-1.25, 0.0])
    p2 = np.array([1.25, 0.0])
    for p, lab in [(p1, "p"), (p2, "p")]:
        ax.add_patch(
            Circle(p, 0.55, facecolor="#ffd9d9", edgecolor=F.RED, lw=2.0, zorder=3)
        )
        ax.text(
            p[0],
            p[1],
            "$p^+$",
            ha="center",
            va="center",
            fontsize=15,
            color=F.RED,
            zorder=5,
        )

    # 中子（在中間偏上，象徵「黏合劑」）
    npos = np.array([0.0, 1.55])
    ax.add_patch(
        Circle(npos, 0.5, facecolor="#e7e7e7", edgecolor="#555", lw=2.0, zorder=3)
    )
    ax.text(
        npos[0],
        npos[1],
        "$n$",
        ha="center",
        va="center",
        fontsize=15,
        color="#444",
        zorder=5,
    )
    ax.text(
        npos[0] + 0.9,
        npos[1] + 0.15,
        "中子：只感受強力、\n不帶電，幫忙「黏」住核",
        ha="left",
        va="center",
        fontsize=10,
        color="#444",
    )

    # 電斥力（向外，紅色）
    F.arrow(ax, p1, p1 + np.array([-1.45, 0]), color=F.RED, lw=2.6)
    F.arrow(ax, p2, p2 + np.array([1.45, 0]), color=F.RED, lw=2.6)
    ax.text(
        0.0,
        -0.95,
        "電力：同號電荷互相排斥（想把核推開）",
        ha="center",
        fontsize=11,
        color=F.RED,
    )

    # 強力（向內，琥珀，較粗→較強）
    F.arrow(
        ax,
        p1 + np.array([0.62, 0.30]),
        np.array([-0.15, 0.30]),
        color=F.AMBER,
        lw=3.4,
        mutation=20,
    )
    F.arrow(
        ax,
        p2 + np.array([-0.62, 0.30]),
        np.array([0.15, 0.30]),
        color=F.AMBER,
        lw=3.4,
        mutation=20,
    )
    ax.text(
        0.0,
        0.78,
        "強力：超近距離的強烈吸引（把核拉住）",
        ha="center",
        fontsize=11,
        color="#9a6700",
    )

    ax.text(
        0.0,
        -1.95,
        "近距離下強力 > 電斥力 → 原子核穩定不炸開（但質子太多時電斥力會贏）",
        ha="center",
        fontsize=10.5,
        color=F.INK,
    )
    ax.set_xlim(-4.0, 4.2)
    ax.set_ylim(-2.5, 2.7)
    ax.set_title("原子核內的拔河：電斥力 vs 強力", fontsize=14)
    F.save_to(fig, CH, "必物-3-核內力平衡")


def fig_beta_decay():
    """β 衰變：核內一個中子變質子＋電子（＋反微中子），Z＋1、A 不變 → 變成另一種元素。"""
    fig, ax = F.schematic(8.8, 4.8)

    def draw_nucleus(cx, cy, protons, neutrons, special=None):
        """畫一團核子；protons/neutrons 為座標列表，special=該位置畫成轉變中的核子。"""
        for i, (dx, dy) in enumerate(protons):
            col_f, col_e = "#ffd9d9", F.RED
            if special == ("p", i):
                col_f, col_e = "#fff0c2", F.AMBER
            ax.add_patch(
                Circle(
                    (cx + dx, cy + dy),
                    0.30,
                    facecolor=col_f,
                    edgecolor=col_e,
                    lw=1.8,
                    zorder=4,
                )
            )
            ax.text(
                cx + dx,
                cy + dy,
                "$p$",
                ha="center",
                va="center",
                fontsize=11,
                color=col_e,
                zorder=6,
            )
        for i, (dx, dy) in enumerate(neutrons):
            col_f, col_e = "#e7e7e7", "#555"
            if special == ("n", i):
                col_f, col_e = "#fff0c2", F.AMBER
            ax.add_patch(
                Circle(
                    (cx + dx, cy + dy),
                    0.30,
                    facecolor=col_f,
                    edgecolor=col_e,
                    lw=1.8,
                    zorder=4,
                )
            )
            ax.text(
                cx + dx,
                cy + dy,
                "$n$",
                ha="center",
                va="center",
                fontsize=11,
                color=col_e,
                zorder=6,
            )

    # 核子相對位置（母核：2 質子 3 中子；子核：3 質子 2 中子，A=5 不變）
    P = [(-0.34, 0.36), (0.34, 0.36)]
    N3 = [(-0.34, -0.30), (0.34, -0.30), (0.0, 0.92)]
    # 母核（左）：標出「即將轉變」的那個中子
    cxL, cyL = -2.9, 0.4
    draw_nucleus(cxL, cyL, P, N3, special=("n", 0))
    ax.text(cxL, cyL + 1.6, "母核（衰變前）", ha="center", fontsize=11.5, color=F.INK)
    ax.text(
        cxL,
        cyL - 1.35,
        "原子序 $Z$、質量數 $A$",
        ha="center",
        fontsize=10.5,
        color="#555",
    )
    ax.text(
        cxL - 1.45,
        cyL + 0.05,
        "中子過多、\n不夠穩定",
        ha="right",
        va="center",
        fontsize=9.5,
        color=F.AMBER,
    )
    ax.annotate(
        "",
        xy=(cxL - 0.62, cyL - 0.18),
        xytext=(cxL - 1.4, cyL + 0.0),
        arrowprops=dict(arrowstyle="->", color=F.AMBER, lw=1.3),
        zorder=6,
    )

    # 子核（右）：3 質子 2 中子，多一個質子
    P3 = [(-0.34, 0.36), (0.34, 0.36), (0.0, -0.30)]
    N2 = [(-0.34, -0.30), (0.0, 0.92)]
    cxR, cyR = 2.9, 0.4
    draw_nucleus(cxR, cyR, P3, N2, special=("p", 2))
    ax.text(cxR, cyR + 1.6, "子核（衰變後）", ha="center", fontsize=11.5, color=F.INK)
    ax.text(
        cxR,
        cyR - 1.35,
        "原子序 $Z+1$、質量數 $A$ 不變",
        ha="center",
        fontsize=10.5,
        color=F.GREEN,
    )

    # 中央：轉變大箭頭
    F.arrow(
        ax,
        (cxL + 1.15, cyL + 0.2),
        (cxR - 1.15, cyL + 0.2),
        color=F.INK,
        lw=2.4,
        mutation=18,
    )
    ax.text(
        0.0,
        cyL + 0.62,
        "弱力作用：一個中子變質子",
        ha="center",
        fontsize=11,
        color=F.PURPLE,
    )

    # 放出電子（β 射線）與反微中子，往右下／右上射出
    F.arrow(ax, (0.0, cyL - 0.15), (1.55, -2.05), color=F.BLUE, lw=2.0, mutation=15)
    ax.text(
        1.7,
        -2.05,
        "電子 $e^-$\n（β 射線）",
        ha="left",
        va="center",
        fontsize=10,
        color=F.BLUE,
    )
    F.arrow(
        ax,
        (0.0, cyL - 0.15),
        (-1.55, -2.05),
        color="#888",
        lw=1.6,
        mutation=13,
        ls="--",
    )
    ax.text(
        -1.7,
        -2.05,
        "反微中子\n（幾乎不帶能量痕跡）",
        ha="right",
        va="center",
        fontsize=9.5,
        color="#888",
    )

    # 底部反應式（純文字，避免 mathtext 缺字）
    ax.text(
        0.0,
        2.45,
        "中子 → 質子 ＋ 電子 ＋ 反微中子",
        ha="center",
        fontsize=12,
        color=F.INK,
    )

    ax.set_xlim(-5.6, 5.0)
    ax.set_ylim(-2.7, 2.9)
    ax.set_title("β 衰變：中子變質子，原子核變成另一種元素", fontsize=14)
    F.save_to(fig, CH, "必物-3-貝他衰變")


if __name__ == "__main__":
    fig_hierarchy()
    fig_rutherford()
    fig_four_forces()
    fig_nuclear_balance()
    fig_beta_decay()
    print("done.")
