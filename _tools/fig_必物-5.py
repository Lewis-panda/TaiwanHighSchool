# -*- coding: utf-8 -*-
"""產生「必物-5 能量」的圖，輸出到該章 sources/。
重繪：  .venv/bin/python _tools/fig_必物-5.py
"""

import os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
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


def fig_heat_transfer():
    """傳導／對流／輻射三種傳熱方式並列示意：各一格，標機制與例子，註明只有輻射穿越真空。"""
    fig, axes = plt.subplots(1, 3, figsize=(11.4, 4.7))
    rng = np.random.default_rng(7)

    # ---------- (1) 傳導 conduction ----------
    ax = axes[0]
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    # 一根金屬棒，一端高溫一端低溫；分子排成晶格、靠碰撞接力
    bar_y0, bar_y1 = 0.40, 0.60
    # 漸層底色：左熱右冷
    ngrad = 60
    for k in range(ngrad):
        x0 = 0.08 + 0.84 * k / ngrad
        frac = k / (ngrad - 1)
        col = (
            0.82 + 0.13 * (1 - frac),  # R 高溫偏紅
            0.30 + 0.55 * frac,
            0.30 + 0.55 * frac,
        )
        ax.add_patch(
            plt.Rectangle(
                (x0, bar_y0),
                0.84 / ngrad + 0.002,
                bar_y1 - bar_y0,
                fc=col,
                ec="none",
                zorder=2,
            )
        )
    ax.add_patch(
        plt.Rectangle(
            (0.08, bar_y0),
            0.84,
            bar_y1 - bar_y0,
            fill=False,
            ec=F.INK,
            lw=2.0,
            zorder=4,
        )
    )
    # 晶格分子（固定位置，畫小幅振動箭頭表示原地振動、不整體移動）
    for i in range(7):
        px = 0.16 + i * 0.11
        py = 0.50
        ax.add_patch(plt.Circle((px, py), 0.018, color=F.INK, zorder=5))
        ax.add_patch(FancyArrowPatchSafe(ax, (px - 0.022, py), (px + 0.022, py)))
    # 火源（畫在棒下方，與「高溫」標籤錯開避免重疊）
    ax.text(0.04, 0.50, "火", ha="center", va="center", fontsize=12, color=F.RED)
    F.arrow(ax, (0.055, 0.50), (0.085, 0.50), color=F.RED, lw=2.2, mutation=12)
    # 熱沿棒向右接力
    F.arrow(ax, (0.20, 0.70), (0.80, 0.70), color=F.AMBER, lw=2.6, mutation=18)
    ax.text(0.5, 0.78, "動能逐顆接力傳遞", ha="center", fontsize=10.5, color=F.AMBER)
    ax.text(0.16, 0.345, "高溫", ha="center", fontsize=9.5, color=F.RED)
    ax.text(0.84, 0.345, "低溫", ha="center", fontsize=9.5, color=F.BLUE)
    ax.set_title("傳導（conduction）", fontsize=13)
    ax.text(
        0.5,
        0.16,
        "靠分子／自由電子碰撞接力\n物質本身不整體移動",
        ha="center",
        va="center",
        fontsize=10,
        color=F.INK,
    )
    ax.text(
        0.5,
        0.02,
        "例：鐵湯匙一端泡熱湯、另一端變燙",
        ha="center",
        va="center",
        fontsize=9,
        color="#555",
    )

    # ---------- (2) 對流 convection ----------
    ax = axes[1]
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    # 容器（一鍋水）
    ax.add_patch(
        plt.Rectangle(
            (0.14, 0.30), 0.72, 0.50, fc="#eaf3ff", ec=F.INK, lw=2.0, zorder=2
        )
    )
    # 底部加熱
    ax.add_patch(
        plt.Rectangle(
            (0.14, 0.265), 0.72, 0.035, fc="#fdecec", ec=F.RED, lw=1.5, zorder=3
        )
    )
    ax.text(0.5, 0.235, "加熱", ha="center", fontsize=10, color=F.RED)
    # 循環箭頭：熱流體上升（中央），冷流體下沉（兩側）
    # 中央上升（紅）
    F.arrow(ax, (0.50, 0.36), (0.50, 0.74), color=F.RED, lw=2.6, mutation=16, z=5)
    ax.text(0.50, 0.55, "熱\n上升", ha="center", va="center", fontsize=9.5, color=F.RED)
    # 左側下沉（藍）
    F.arrow(ax, (0.26, 0.74), (0.26, 0.36), color=F.BLUE, lw=2.6, mutation=16, z=5)
    # 右側下沉（藍）
    F.arrow(ax, (0.74, 0.74), (0.74, 0.36), color=F.BLUE, lw=2.6, mutation=16, z=5)
    ax.text(
        0.26, 0.55, "冷\n下沉", ha="center", va="center", fontsize=9.5, color=F.BLUE
    )
    ax.text(
        0.74, 0.55, "冷\n下沉", ha="center", va="center", fontsize=9.5, color=F.BLUE
    )
    # 頂部與底部的橫向流（形成循環）
    F.arrow(ax, (0.47, 0.75), (0.30, 0.75), color="#888", lw=1.6, mutation=11, z=5)
    F.arrow(ax, (0.53, 0.75), (0.70, 0.75), color="#888", lw=1.6, mutation=11, z=5)
    F.arrow(ax, (0.30, 0.345), (0.47, 0.345), color="#888", lw=1.6, mutation=11, z=5)
    F.arrow(ax, (0.70, 0.345), (0.53, 0.345), color="#888", lw=1.6, mutation=11, z=5)
    ax.set_title("對流（convection）", fontsize=13)
    ax.text(
        0.5,
        0.16,
        "靠流體本身整體流動載走熱\n熱流體上升、冷流體下沉成循環",
        ha="center",
        va="center",
        fontsize=10,
        color=F.INK,
    )
    ax.text(
        0.5,
        0.02,
        "例：燒開水、暖氣使房間變暖、海陸風",
        ha="center",
        va="center",
        fontsize=9,
        color="#555",
    )

    # ---------- (3) 輻射 radiation ----------
    ax = axes[2]
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    # 真空背景（深色），標「真空」
    ax.add_patch(
        plt.Rectangle(
            (0.06, 0.28), 0.88, 0.54, fc="#1b2330", ec=F.INK, lw=1.6, zorder=1
        )
    )
    ax.text(0.83, 0.78, "真空", ha="center", fontsize=10, color="#cdd6e3", zorder=6)
    # 熱源（太陽 / 火）放在左
    sun = plt.Circle((0.24, 0.55), 0.085, fc="#ffcf33", ec=F.RED, lw=1.6, zorder=4)
    ax.add_patch(sun)
    ax.text(
        0.24, 0.55, "熱源", ha="center", va="center", fontsize=9, color=F.RED, zorder=6
    )
    # 電磁波（波浪箭頭）向右穿越真空到接收者
    xx = np.linspace(0.345, 0.74, 100)
    for yc, amp in [(0.62, 0.025), (0.55, 0.030), (0.48, 0.025)]:
        yy = yc + amp * np.sin((xx - 0.345) / 0.40 * 4 * np.pi)
        ax.plot(xx, yy, color="#ffd24d", lw=1.8, zorder=5)
    F.arrow(ax, (0.70, 0.55), (0.775, 0.55), color="#ffd24d", lw=2.2, mutation=14, z=6)
    ax.text(0.52, 0.70, "電磁波", ha="center", fontsize=10, color="#ffd24d", zorder=6)
    # 接收者
    ax.add_patch(
        plt.Rectangle(
            (0.80, 0.44), 0.07, 0.22, fc="#fdecec", ec=F.RED, lw=1.6, zorder=4
        )
    )
    ax.text(0.835, 0.40, "受熱", ha="center", fontsize=8.5, color=F.RED, zorder=6)
    ax.set_title("輻射（radiation）", fontsize=13)
    ax.text(
        0.5,
        0.16,
        "靠電磁波傳熱，不需任何介質\n唯一能穿越真空的方式",
        ha="center",
        va="center",
        fontsize=10,
        color=F.INK,
    )
    ax.text(
        0.5,
        0.02,
        "例：太陽橫越真空把熱送到地球、紅外線測溫",
        ha="center",
        va="center",
        fontsize=9,
        color="#555",
    )

    fig.suptitle(
        "熱傳遞的三種方式：傳導、對流、輻射（只有輻射能穿越真空）", fontsize=14
    )
    fig.tight_layout(rect=[0, 0, 1, 0.93])
    F.save_to(fig, CH, "必物-5-三種傳熱")


def fig_thermal_equilibrium():
    """熱平衡：熱只從高溫流向低溫，溫度逐漸接近，最終相等、淨熱流停止。"""
    fig, (ax1, ax2) = plt.subplots(
        1, 2, figsize=(9.4, 4.4), gridspec_kw={"width_ratios": [1.05, 1.0]}
    )

    # 左：兩物體接觸，熱由高溫流向低溫
    ax1.set_xlim(0, 1)
    ax1.set_ylim(0, 1)
    ax1.axis("off")
    # 高溫物體（左）
    ax1.add_patch(
        FancyBboxPatch(
            (0.06, 0.34),
            0.32,
            0.40,
            boxstyle="round,pad=0.01,rounding_size=0.03",
            fc="#fdecec",
            ec=F.RED,
            lw=2.2,
        )
    )
    ax1.text(0.22, 0.62, "高溫物體", ha="center", fontsize=12, color=F.RED)
    ax1.text(0.22, 0.46, "80°C", ha="center", fontsize=15, color=F.RED)
    # 低溫物體（右）
    ax1.add_patch(
        FancyBboxPatch(
            (0.62, 0.34),
            0.32,
            0.40,
            boxstyle="round,pad=0.01,rounding_size=0.03",
            fc="#eaf3ff",
            ec=F.BLUE,
            lw=2.2,
        )
    )
    ax1.text(0.78, 0.62, "低溫物體", ha="center", fontsize=12, color=F.BLUE)
    ax1.text(0.78, 0.46, "20°C", ha="center", fontsize=15, color=F.BLUE)
    # 熱流箭頭：高溫→低溫
    F.arrow(ax1, (0.40, 0.56), (0.60, 0.56), color=F.AMBER, lw=3.0, mutation=22)
    ax1.text(0.50, 0.66, "熱", ha="center", fontsize=13, color=F.AMBER)
    # 強調：不會自發逆流
    F.arrow(
        ax1,
        (0.60, 0.44),
        (0.40, 0.44),
        color="#bbb",
        lw=2.0,
        mutation=16,
        ls=(0, (3, 3)),
    )
    ax1.text(0.50, 0.355, "不會自發逆流", ha="center", fontsize=9, color="#999")
    ax1.set_title("熱只從高溫流向低溫", fontsize=13)
    ax1.text(
        0.5, 0.18, "與兩者內能總量無關，只看溫度", ha="center", fontsize=10, color=F.INK
    )

    # 右：溫度隨時間趨近、相等 → 熱平衡
    t = np.linspace(0, 6, 200)
    Teq = 35.0
    Thot = Teq + (80 - Teq) * np.exp(-0.8 * t)
    Tcold = Teq + (20 - Teq) * np.exp(-0.8 * t)
    ax2.plot(t, Thot, color=F.RED, lw=2.6, label="高溫物體")
    ax2.plot(t, Tcold, color=F.BLUE, lw=2.6, label="低溫物體")
    ax2.axhline(Teq, color="#888", lw=1.4, ls=(0, (4, 3)))
    ax2.text(6.05, Teq, "  共同溫度", color="#555", fontsize=10, va="center")
    ax2.annotate(
        "達熱平衡\n淨熱流停止",
        xy=(5.2, Teq),
        xytext=(3.2, 56),
        fontsize=10.5,
        color=F.GREEN,
        ha="center",
        arrowprops=dict(arrowstyle="->", color=F.GREEN, lw=1.6),
    )
    ax2.set_xlim(0, 7.4)
    ax2.set_ylim(10, 90)
    ax2.set_xlabel("時間")
    ax2.set_ylabel("溫度（°C）")
    ax2.set_title("溫度趨於相等即達熱平衡")
    ax2.legend(loc="center right", fontsize=10, frameon=False)
    F.clean_grid(ax2)
    ax2.set_xticks([])

    fig.suptitle("熱平衡：熱由高溫流向低溫，直到兩者同溫、淨熱流停止", fontsize=13.5)
    fig.tight_layout(rect=[0, 0, 1, 0.93])
    F.save_to(fig, CH, "必物-5-熱平衡")


def fig_mechanical_energy():
    """力學能守恆：自由落體三個高度，位能↓、動能↑，總和(力學能)不變。"""
    from matplotlib.patches import Rectangle, Circle

    fig, (ax1, ax2) = plt.subplots(
        1, 2, figsize=(8.6, 4.8), gridspec_kw={"width_ratios": [1, 1.25]}
    )

    # ---- 左：落體三位置 ----
    H = 3.0
    states = [(H, "頂端：靜止"), (H / 2, "中途"), (0.0, "落地：最快")]
    ax1.plot([0.15, 0.15], [0, H], color="#bbb", lw=1.0, zorder=1)
    ax1.plot([-0.25, 0.55], [0, 0], color=F.INK, lw=2.2)  # 地面
    for h, lab in states:
        ax1.add_patch(Circle((0.15, h), 0.16, color=F.BLUE, zorder=4))
        ax1.text(0.42, h, lab, fontsize=10.5, va="center", ha="left", color=F.INK)
    F.arrow(ax1, (0.15, H - 0.35), (0.15, 0.35), color=F.RED, lw=1.6, mutation=12)
    ax1.text(-0.1, H / 2, "$g$", color=F.RED, fontsize=12, va="center", ha="right")
    ax1.set_xlim(-0.5, 2.0)
    ax1.set_ylim(-0.5, H + 0.6)
    ax1.axis("off")
    ax1.set_title("自由落體", fontsize=12)

    # ---- 右：U+K 堆疊長條，總高不變 ----
    Etot = 1.0
    xs = [0, 1, 2]
    labels = ["頂端", "中途", "落地"]
    U = [1.0, 0.5, 0.0]
    K = [0.0, 0.5, 1.0]
    w = 0.55
    for x, u, k in zip(xs, U, K):
        ax2.add_patch(
            Rectangle((x - w / 2, 0), w, u, facecolor=F.BLUE, edgecolor=F.INK, lw=1.0)
        )
        ax2.add_patch(
            Rectangle((x - w / 2, u), w, k, facecolor=F.RED, edgecolor=F.INK, lw=1.0)
        )
        if u > 0.04:
            ax2.text(
                x, u / 2, "位能", color="white", fontsize=10, ha="center", va="center"
            )
        if k > 0.04:
            ax2.text(
                x,
                u + k / 2,
                "動能",
                color="white",
                fontsize=10,
                ha="center",
                va="center",
            )
    ax2.plot([-0.5, 2.5], [Etot, Etot], color=F.GREEN, lw=1.6, ls="--")
    ax2.text(
        2.5,
        Etot + 0.03,
        "力學能 ＝ 動能 ＋ 位能（定值）",
        color=F.GREEN,
        fontsize=10.5,
        ha="right",
        va="bottom",
    )
    ax2.set_xticks(xs)
    ax2.set_xticklabels(labels, fontsize=11)
    ax2.set_yticks([])
    ax2.set_ylim(0, Etot + 0.22)
    ax2.set_xlim(-0.6, 2.6)
    for s in ("top", "right", "left"):
        ax2.spines[s].set_visible(False)
    ax2.set_title("位能↓、動能↑，總和不變", fontsize=12)

    fig.suptitle("力學能守恆（無摩擦時）", fontsize=13)
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    F.save_to(fig, CH, "必物-5-力學能守恆")


def FancyArrowPatchSafe(ax, p0, p1):
    """小幅雙向振動標記（原地振動，不整體移動）。"""
    a = FancyArrowPatch(
        p0,
        p1,
        arrowstyle="<->",
        mutation_scale=7,
        lw=1.1,
        color="#888",
        zorder=5,
        shrinkA=0,
        shrinkB=0,
    )
    ax.add_patch(a)
    return a


if __name__ == "__main__":
    fig_energy_conversion()
    fig_binding_energy()
    fig_internal_energy()
    fig_heat_engine()
    fig_heat_transfer()
    fig_thermal_equilibrium()
    fig_mechanical_energy()
    print("done.")
