# -*- coding: utf-8 -*-
"""產生「必物-5 能量」的圖，輸出到該章 sources/。
重繪：  .venv/bin/python _tools/fig_必物-5.py
"""

import os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import figlib as F

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CH = os.path.join(ROOT, "物理", "物理一（必修物理）", "必物-5 能量")


def fig_energy_conversion():
    """各種能量形式互相轉換、總能量守恆的流向圖。"""
    fig, ax = F.schematic(8.4, 5.6)

    # 中央：總能量守恆
    cx, cy = 0.0, 0.0
    ax.add_patch(
        FancyBboxPatch(
            (cx - 1.05, cy - 0.42),
            2.10,
            0.84,
            boxstyle="round,pad=0.02,rounding_size=0.12",
            fc="#eef4ff",
            ec=F.BLUE,
            lw=2.2,
            zorder=2,
        )
    )
    F.label(ax, (cx, cy + 0.10), "總能量", color=F.BLUE, fs=15)
    F.label(ax, (cx, cy - 0.16), "永遠守恆", color=F.BLUE, fs=12)

    # 六種能量形式繞一圈
    forms = [
        ("動能\n（運動）", 90),
        ("位能\n（高度·彈簧）", 30),
        ("熱能\n（分子亂動）", -30),
        ("化學能\n（鍵結）", -90),
        ("電能 / 電磁能\n（電磁場·光）", -150),
        ("核能\n（質量虧損）", 150),
    ]
    R = 2.55
    coords = []
    for text, deg in forms:
        a = np.deg2rad(deg)
        x, y = R * np.cos(a), R * 0.78 * np.sin(a)
        coords.append((x, y))
        ax.add_patch(
            FancyBboxPatch(
                (x - 0.78, y - 0.34),
                1.56,
                0.68,
                boxstyle="round,pad=0.02,rounding_size=0.10",
                fc="#fff8ec",
                ec=F.AMBER,
                lw=1.8,
                zorder=2,
            )
        )
        F.label(ax, (x, y), text, color=F.INK, fs=11)

    # 形式之間互相轉換（雙向箭頭，沿環）
    n = len(coords)
    for i in range(n):
        p, q = np.array(coords[i]), np.array(coords[(i + 1) % n])
        d = q - p
        d = d / np.linalg.norm(d)
        a0 = p + d * 0.95
        a1 = q - d * 0.95
        F.arrow(ax, a0, a1, color=F.GREEN, lw=1.6, mutation=12)
        F.arrow(ax, a1, a0, color=F.GREEN, lw=1.6, mutation=12)

    # 一個具體例子標註：水力發電
    F.label(
        ax,
        (0, -3.15),
        "例：水庫（位能）→ 水流（動能）→ 發電機（電能）→ 燈泡（光＋熱）",
        color="#555",
        fs=11,
    )
    ax.set_xlim(-4.2, 4.2)
    ax.set_ylim(-3.5, 3.2)
    ax.set_title("能量在各種形式間轉換，但總量守恆", fontsize=14)
    F.save_to(fig, CH, "必物-5-能量轉換")


def fig_binding_energy():
    """每核子束縛能 vs 質量數曲線，標出鐵峰、融合與分裂釋能方向。"""
    fig, ax = F.canvas(7.6, 4.8)
    # 以幾個代表性核種的「每核子束縛能（MeV）」實測值近似畫出曲線
    A = np.array(
        [1, 2, 3, 4, 6, 7, 9, 12, 16, 20, 27, 40, 56, 75, 100, 140, 180, 209, 238]
    )
    B = np.array(
        [
            0.0,
            1.11,
            2.83,
            7.07,
            5.33,
            5.61,
            6.46,
            7.68,
            7.98,
            8.03,
            8.33,
            8.55,
            8.79,
            8.70,
            8.50,
            8.33,
            8.00,
            7.83,
            7.57,
        ]
    )
    # 平滑插值
    from numpy import interp

    Af = np.linspace(1, 238, 500)
    Bf = interp(Af, A, B)
    ax.plot(Af, Bf, color=F.INK, lw=2.6, zorder=3)
    ax.scatter(A, B, s=16, color=F.INK, zorder=4)

    # 標出鐵峰
    ax.scatter([56], [8.79], s=90, facecolor=F.RED, edgecolor="white", lw=1.5, zorder=6)
    ax.annotate(
        "$^{56}$Fe（鐵）\n最穩定·峰頂",
        xy=(56, 8.79),
        xytext=(92, 7.35),
        color=F.RED,
        fontsize=11,
        ha="center",
        arrowprops=dict(arrowstyle="->", color=F.RED, lw=1.6),
    )

    # 標幾個重點核種
    for a, b, name, dx, dy in [
        (1, 0.0, "$^{1}$H", 4, 0.35),
        (2, 1.11, "$^{2}$H", 4, -0.55),
        (4, 7.07, "$^{4}$He", -3, 0.55),
        (235, 7.59, "$^{235}$U", 0, -0.7),
    ]:
        F.label(ax, (a + dx, b + dy), name, fs=10, color="#444")

    # 融合方向（左側向上）
    F.arrow(ax, (3, 2.6), (10, 6.4), color=F.BLUE, lw=2.2, mutation=16)
    ax.text(
        2.5,
        3.4,
        "輕核融合\n（往峰頂爬→釋能）",
        color=F.BLUE,
        fontsize=11,
        ha="left",
        va="center",
    )
    # 分裂方向（右側向上爬向峰）
    F.arrow(ax, (235, 7.0), (130, 8.25), color=F.GREEN, lw=2.2, mutation=16)
    ax.text(
        176,
        6.55,
        "重核分裂\n（往峰頂爬→釋能）",
        color=F.GREEN,
        fontsize=11,
        ha="center",
        va="center",
    )

    ax.set_xlim(0, 245)
    ax.set_ylim(0, 9.6)
    ax.set_xlabel("質量數 $A$（核子數）")
    ax.set_ylabel("每核子平均束縛能（MeV）")
    ax.set_title("束縛能曲線：往「鐵峰」靠攏就會釋放能量")
    F.clean_grid(ax)
    F.save_to(fig, CH, "必物-5-束縛能曲線")


def fig_internal_energy():
    """溫度↑→分子運動更劇烈（微觀動能）示意。"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8.6, 4.4))
    rng = np.random.default_rng(5)

    def draw_box(ax, T_label, speed, col, n=14):
        # 容器
        ax.add_patch(plt.Rectangle((0, 0), 1, 1, fill=False, ec=F.INK, lw=2.2))
        pos = rng.uniform(0.12, 0.88, size=(n, 2))
        ang = rng.uniform(0, 2 * np.pi, size=n)
        for (px, py), a in zip(pos, ang):
            ax.add_patch(plt.Circle((px, py), 0.035, color=col, zorder=3))
            vx, vy = speed * np.cos(a), speed * np.sin(a)
            F.arrow(
                ax, (px, py), (px + vx, py + vy), color=col, lw=1.4, mutation=8, z=4
            )
        ax.set_xlim(-0.1, 1.1)
        ax.set_ylim(-0.25, 1.18)
        ax.set_aspect("equal")
        ax.axis("off")
        ax.text(0.5, 1.08, T_label, ha="center", fontsize=13)

    draw_box(ax1, "低溫", 0.09, F.BLUE)
    ax1.text(0.5, -0.16, "分子慢·動能小", ha="center", color=F.BLUE, fontsize=11)
    draw_box(ax2, "高溫", 0.20, F.RED)
    ax2.text(0.5, -0.16, "分子快·動能大", ha="center", color=F.RED, fontsize=11)

    # 中間箭頭
    fig.text(
        0.5,
        0.52,
        "加熱\n$T\\uparrow$",
        ha="center",
        va="center",
        fontsize=13,
        color=F.AMBER,
    )
    fig.suptitle(
        "溫度是分子「亂動劇烈程度」的量度（理想氣體：內能 $\\propto T$）", fontsize=13
    )
    fig.tight_layout(rect=[0, 0, 1, 0.94])
    F.save_to(fig, CH, "必物-5-內能溫度")


def fig_heat_engine():
    """功→熱容易、熱→功有限（熱機效率/第二定律）示意。"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.0, 4.6))

    # 左：功 100% 變熱
    ax1.axis("off")
    ax1.set_xlim(0, 1)
    ax1.set_ylim(0, 1)
    ax1.add_patch(
        FancyBboxPatch(
            (0.30, 0.74),
            0.40,
            0.16,
            boxstyle="round,pad=0.01,rounding_size=0.03",
            fc="#eef4ff",
            ec=F.BLUE,
            lw=2,
        )
    )
    ax1.text(0.5, 0.82, "功 W", ha="center", fontsize=13, color=F.BLUE)
    F.arrow(ax1, (0.5, 0.72), (0.5, 0.36), color=F.AMBER, lw=3, mutation=22)
    ax1.text(0.58, 0.54, "摩擦·攪拌", fontsize=11, color=F.AMBER, ha="left")
    ax1.add_patch(
        FancyBboxPatch(
            (0.28, 0.14),
            0.44,
            0.18,
            boxstyle="round,pad=0.01,rounding_size=0.03",
            fc="#fdecec",
            ec=F.RED,
            lw=2,
        )
    )
    ax1.text(0.5, 0.23, "熱 Q（100%）", ha="center", fontsize=13, color=F.RED)
    ax1.set_title("功 → 熱：可以 100% 轉換", fontsize=13)

    # 右：熱機 熱→功 有限
    ax2.axis("off")
    ax2.set_xlim(0, 1)
    ax2.set_ylim(0, 1)
    # 高溫源
    ax2.add_patch(
        FancyBboxPatch(
            (0.06, 0.74),
            0.34,
            0.18,
            boxstyle="round,pad=0.01,rounding_size=0.03",
            fc="#fdecec",
            ec=F.RED,
            lw=2,
        )
    )
    ax2.text(0.23, 0.83, "高溫源 $T_H$", ha="center", fontsize=12, color=F.RED)
    # 引擎
    ax2.add_patch(plt.Circle((0.23, 0.5), 0.10, fc="#eef4ff", ec=F.INK, lw=2))
    ax2.text(0.23, 0.5, "熱機", ha="center", va="center", fontsize=12)
    # 低溫源
    ax2.add_patch(
        FancyBboxPatch(
            (0.06, 0.06),
            0.34,
            0.16,
            boxstyle="round,pad=0.01,rounding_size=0.03",
            fc="#eef4ff",
            ec=F.BLUE,
            lw=2,
        )
    )
    ax2.text(0.23, 0.14, "低溫源 $T_C$", ha="center", fontsize=12, color=F.BLUE)

    F.arrow(ax2, (0.23, 0.73), (0.23, 0.61), color=F.RED, lw=3, mutation=20)
    ax2.text(0.40, 0.67, "吸熱 $Q_H$", fontsize=11, color=F.RED, ha="left")
    F.arrow(ax2, (0.23, 0.39), (0.23, 0.23), color=F.BLUE, lw=3, mutation=20)
    ax2.text(0.40, 0.30, "排熱 $Q_C$（一定 >0）", fontsize=11, color=F.BLUE, ha="left")
    F.arrow(ax2, (0.33, 0.5), (0.62, 0.5), color=F.GREEN, lw=3, mutation=20)
    ax2.text(0.74, 0.58, "作功 $W$", fontsize=12, color=F.GREEN, ha="center")
    ax2.text(0.74, 0.42, "$<Q_H$", fontsize=12, color=F.GREEN, ha="center")
    ax2.set_title("熱 → 功：一定有 $Q_C$ 排掉，效率 < 100%", fontsize=13)

    fig.suptitle(
        "能量「品質」有方向性：功可全變熱，熱不能全變功（第二定律）", fontsize=13
    )
    fig.tight_layout(rect=[0, 0, 1, 0.93])
    F.save_to(fig, CH, "必物-5-熱機方向")


if __name__ == "__main__":
    fig_energy_conversion()
    fig_binding_energy()
    fig_internal_energy()
    fig_heat_engine()
    print("done.")
