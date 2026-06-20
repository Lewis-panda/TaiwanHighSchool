# -*- coding: utf-8 -*-
"""產生「數2-3 排列組合與機率」的圖，輸出到該章 sources/。
重繪：  .venv/bin/python _tools/fig_數2-3.py
本章多為示意圖：文氏圖、樹狀圖、排列組合對照、樣本空間／期望值。
注意：matplotlib mathtext 不支援 \\dfrac/\\tfrac（用 \\frac）；中文勿放進 $...$。
"""

import os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, FancyArrowPatch, FancyBboxPatch
import figlib as F

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CH = os.path.join(ROOT, "數學", "數學一下（必修·第二冊）", "數2-3 排列組合與機率")


# =====================================================================
# 圖一：文氏圖（交集／聯集／餘集 + 取捨原理）
# =====================================================================
def fig_venn():
    """三格文氏圖：A∩B、A∪B、餘集 A^c，並標出取捨原理。"""
    fig, axes = plt.subplots(1, 3, figsize=(12.0, 4.4))

    def draw_universe(ax):
        # 宇集外框
        ax.add_patch(Rectangle((-2.2, -1.8), 4.4, 3.6, fill=False, ec=F.INK, lw=1.6))
        ax.text(-2.05, 1.55, "$U$", color=F.INK, fontsize=14, ha="left", va="top")

    # ---- (1) 交集 A∩B ----
    ax = axes[0]
    draw_universe(ax)
    cA = (-0.55, 0.0)
    cB = (0.55, 0.0)
    rA = rB = 1.15
    # 先填交集（兩圓重疊處）：用 clip 近似，直接畫淡色橢圓重疊區以填色
    ax.add_patch(Circle(cA, rA, fc=F.BLUE, ec=F.BLUE, lw=2.0, alpha=0.16))
    ax.add_patch(Circle(cB, rB, fc=F.RED, ec=F.RED, lw=2.0, alpha=0.16))
    # 交集加深：用兩圓交線範圍的填色（以裁切方式近似——畫一個小區塊）
    th = np.linspace(0, 2 * np.pi, 200)
    ax.add_patch(Circle(cA, rA, fill=False, ec=F.BLUE, lw=2.2))
    ax.add_patch(Circle(cB, rB, fill=False, ec=F.RED, lw=2.2))
    # 標交集區域（畫一塊葉形填色：用兩圓方程式取交集格點）
    xs = np.linspace(-2.2, 2.2, 400)
    ys = np.linspace(-1.8, 1.8, 320)
    X, Y = np.meshgrid(xs, ys)
    inA = (X - cA[0]) ** 2 + (Y - cA[1]) ** 2 <= rA**2
    inB = (X - cB[0]) ** 2 + (Y - cB[1]) ** 2 <= rB**2
    ax.contourf(
        X,
        Y,
        (inA & inB).astype(float),
        levels=[0.5, 1.5],
        colors=[F.PURPLE],
        alpha=0.45,
    )
    ax.text(cA[0] - 0.55, 0.85, "$A$", color=F.BLUE, fontsize=15, ha="center")
    ax.text(cB[0] + 0.55, 0.85, "$B$", color=F.RED, fontsize=15, ha="center")
    ax.text(0.0, -0.02, "$A\\cap B$", color="#3a1f6b", fontsize=12.5, ha="center")
    ax.set_title("交集　$A\\cap B$（同時屬於兩者）", fontsize=12.5)

    # ---- (2) 聯集 A∪B ----
    ax = axes[1]
    draw_universe(ax)
    ax.contourf(
        X, Y, (inA | inB).astype(float), levels=[0.5, 1.5], colors=[F.GREEN], alpha=0.30
    )
    ax.add_patch(Circle(cA, rA, fill=False, ec=F.BLUE, lw=2.2))
    ax.add_patch(Circle(cB, rB, fill=False, ec=F.RED, lw=2.2))
    ax.text(cA[0] - 0.55, 0.85, "$A$", color=F.BLUE, fontsize=15, ha="center")
    ax.text(cB[0] + 0.55, 0.85, "$B$", color=F.RED, fontsize=15, ha="center")
    ax.set_title("聯集　$A\\cup B$（屬於任一者）", fontsize=12.5)

    # ---- (3) 餘集 A^c ----
    ax = axes[2]
    draw_universe(ax)
    # 填整個宇集，再挖掉 A
    inU = np.ones_like(X, dtype=bool)
    ax.contourf(
        X,
        Y,
        (inU & ~inA).astype(float),
        levels=[0.5, 1.5],
        colors=[F.AMBER],
        alpha=0.25,
    )
    ax.add_patch(Circle(cA, rA, fc="white", ec=F.BLUE, lw=2.2, zorder=4))
    ax.text(cA[0], 0.0, "$A$", color=F.BLUE, fontsize=15, ha="center", zorder=5)
    ax.text(1.55, 1.25, "$A^{c}$", color="#8a6200", fontsize=14, ha="center")
    ax.set_title("餘集　$A^{c}$（不屬於 $A$）", fontsize=12.5)

    for ax in axes:
        ax.set_xlim(-2.4, 2.4)
        ax.set_ylim(-2.0, 2.0)
        ax.set_aspect("equal")
        ax.axis("off")

    fig.suptitle(
        "文氏圖與取捨原理：$|A\\cup B| = |A| + |B| - |A\\cap B|$",
        fontsize=14,
        y=1.03,
    )
    fig.tight_layout()
    F.save_to(fig, CH, "數2-3-文氏圖")


# =====================================================================
# 圖二：樹狀圖（有系統的窮舉，乘法原理）
# =====================================================================
def fig_tree():
    """樹狀圖：兩件上衣 × 三件褲子 = 6 種搭配，示意乘法原理。"""
    fig, ax = F.schematic(7.4, 5.4)

    # 根節點
    root = (0.3, 2.5)
    ax.add_patch(Circle(root, 0.10, color=F.INK, zorder=6))
    ax.text(
        root[0] - 0.15,
        root[1],
        "開始",
        color=F.INK,
        fontsize=12,
        ha="right",
        va="center",
    )

    tops = ["上衣甲", "上衣乙"]
    pants = ["褲 1", "褲 2", "褲 3"]
    top_x = 2.3
    pant_x = 4.6
    top_ys = [3.8, 1.2]
    colors_top = [F.BLUE, F.RED]

    leaf = 1
    for ti, (tname, ty, col) in enumerate(zip(tops, top_ys, colors_top)):
        tpos = (top_x, ty)
        # 根 → 上衣
        ax.plot([root[0], tpos[0]], [root[1], tpos[1]], color=col, lw=2.0, zorder=3)
        ax.add_patch(Circle(tpos, 0.10, color=col, zorder=6))
        ax.text(
            tpos[0],
            tpos[1] + 0.28,
            tname,
            color=col,
            fontsize=12,
            ha="center",
            va="bottom",
        )
        # 三條褲子
        spread = 0.95
        pys = [ty + spread, ty, ty - spread]
        for pj, (pname, py) in enumerate(zip(pants, pys)):
            ppos = (pant_x, py)
            ax.plot(
                [tpos[0], ppos[0]],
                [tpos[1], ppos[1]],
                color=col,
                lw=1.5,
                alpha=0.8,
                zorder=2,
            )
            ax.add_patch(Circle(ppos, 0.08, color=col, zorder=6))
            ax.text(
                ppos[0] + 0.18,
                py,
                f"({tname[-1]},{pname[-1]})",
                color=F.INK,
                fontsize=10.5,
                ha="left",
                va="center",
            )
            leaf += 1

    ax.text(
        3.7,
        -0.55,
        "2 種上衣 × 3 種褲子 ＝ 6 種搭配（乘法原理）",
        color=F.INK,
        fontsize=13,
        ha="center",
    )
    ax.set_xlim(-0.9, 6.6)
    ax.set_ylim(-1.0, 5.0)
    ax.set_title("樹狀圖：有系統地窮舉所有搭配", fontsize=14)
    F.save_to(fig, CH, "數2-3-樹狀圖")


# =====================================================================
# 圖三：排列 vs 組合（順序差異）示意
# =====================================================================
def fig_perm_comb():
    """從 {A,B,C} 取 2 個：排列（看順序，6 種）vs 組合（不看順序，3 種）。"""
    fig, axes = plt.subplots(1, 2, figsize=(11.0, 4.6))

    def chip(ax, x, y, txt, col):
        ax.add_patch(
            FancyBboxPatch(
                (x - 0.28, y - 0.28),
                0.56,
                0.56,
                boxstyle="round,pad=0.02,rounding_size=0.1",
                fc=col,
                ec=F.INK,
                lw=1.2,
                alpha=0.85,
                zorder=4,
            )
        )
        ax.text(
            x,
            y,
            txt,
            color="white",
            fontsize=13,
            ha="center",
            va="center",
            zorder=5,
            fontweight="bold",
        )

    cmap = {"A": F.BLUE, "B": F.RED, "C": F.GREEN}

    # ---- 排列：6 種有序對 ----
    ax = axes[0]
    perms = ["AB", "BA", "AC", "CA", "BC", "CB"]
    for i, p in enumerate(perms):
        row = i // 2
        colp = i % 2
        x0 = 0.6 + colp * 2.4
        y0 = 3.2 - row * 1.2
        chip(ax, x0, y0, p[0], cmap[p[0]])
        # 箭頭表示「有先後」
        ax.add_patch(
            FancyArrowPatch(
                (x0 + 0.32, y0),
                (x0 + 0.78, y0),
                arrowstyle="-|>",
                mutation_scale=14,
                lw=1.6,
                color=F.INK,
                zorder=3,
            )
        )
        chip(ax, x0 + 1.1, y0, p[1], cmap[p[1]])
    ax.text(
        2.0,
        4.2,
        "排列 $P^3_2 = 6$　（順序不同算不同）",
        color=F.INK,
        fontsize=13,
        ha="center",
    )
    ax.set_xlim(-0.2, 4.6)
    ax.set_ylim(-0.4, 4.7)

    # ---- 組合：3 種無序對 ----
    ax = axes[1]
    combs = ["AB", "AC", "BC"]
    for i, c in enumerate(combs):
        y0 = 3.0 - i * 1.1
        x0 = 1.2
        chip(ax, x0, y0, c[0], cmap[c[0]])
        chip(ax, x0 + 0.9, y0, c[1], cmap[c[1]])
        # 大括號示意「一組」
        ax.text(x0 - 0.7, y0, "{", color=F.INK, fontsize=22, ha="center", va="center")
        ax.text(x0 + 1.6, y0, "}", color=F.INK, fontsize=22, ha="center", va="center")
    ax.text(
        1.65,
        4.0,
        "組合 $C^3_2 = 3$　（順序不同算同一組）",
        color=F.INK,
        fontsize=13,
        ha="center",
    )
    ax.text(
        1.65,
        -0.05,
        "$C^3_2 = \\frac{P^3_2}{2!} = \\frac{6}{2} = 3$",
        color=F.PURPLE,
        fontsize=13.5,
        ha="center",
    )
    ax.set_xlim(-0.4, 3.6)
    ax.set_ylim(-0.6, 4.5)

    for ax in axes:
        ax.set_aspect("equal")
        ax.axis("off")

    fig.suptitle("排列與組合的差別：在於「順序算不算」", fontsize=14.5, y=1.02)
    fig.tight_layout()
    F.save_to(fig, CH, "數2-3-排列組合")


# =====================================================================
# 圖四：機率（樣本空間與事件 + 期望值長條）
# =====================================================================
def fig_prob():
    """左：擲一顆骰子的樣本空間與事件 A={2,4,6}；右：期望值＝以機率加權的平均。"""
    fig, axes = plt.subplots(1, 2, figsize=(11.4, 4.6))

    # ---- (左) 樣本空間方格 ----
    ax = axes[0]
    ax.add_patch(Rectangle((0.0, 0.0), 6.6, 2.0, fill=False, ec=F.INK, lw=1.8))
    ax.text(
        0.15,
        2.18,
        "樣本空間 $S=\\{1,2,3,4,5,6\\}$",
        color=F.INK,
        fontsize=12.5,
        ha="left",
        va="bottom",
    )
    faces = [1, 2, 3, 4, 5, 6]
    for i, f in enumerate(faces):
        x0 = 0.25 + i * 1.05
        even = f % 2 == 0
        col = F.BLUE if even else "white"
        ax.add_patch(
            FancyBboxPatch(
                (x0, 0.45),
                0.85,
                1.1,
                boxstyle="round,pad=0.02,rounding_size=0.08",
                fc=col,
                ec=F.INK,
                lw=1.4,
                alpha=0.85 if even else 1,
            )
        )
        ax.text(
            x0 + 0.42,
            1.0,
            str(f),
            color="white" if even else F.INK,
            fontsize=18,
            ha="center",
            va="center",
            fontweight="bold",
        )
    ax.text(
        3.3,
        -0.55,
        "事件 $A$＝「出現偶數」$=\\{2,4,6\\}$，　$P(A)=\\frac{3}{6}=\\frac{1}{2}$",
        color=F.BLUE,
        fontsize=12.5,
        ha="center",
    )
    ax.set_xlim(-0.3, 7.0)
    ax.set_ylim(-1.0, 2.7)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("樣本空間與事件（古典機率）", fontsize=13)

    # ---- (右) 期望值：加權平均 ----
    ax = axes[1]
    # 一個遊戲：得 0、10、50 元，機率 0.5、0.3、0.2
    vals = [0, 10, 50]
    probs = [0.5, 0.3, 0.2]
    xpos = np.arange(len(vals))
    bars = ax.bar(
        xpos, probs, width=0.55, color=[F.GRID, F.BLUE, F.RED], ec=F.INK, lw=1.3
    )
    for x, v, p in zip(xpos, vals, probs):
        ax.text(x, p + 0.02, f"$p={p}$", ha="center", fontsize=11, color=F.INK)
        ax.text(x, -0.05, f"{v} 元", ha="center", fontsize=12, color=F.INK, va="top")
    EV = sum(v * p for v, p in zip(vals, probs))
    ax.axhline(0, color=F.INK, lw=1.2)
    ax.text(
        1.0,
        0.62,
        f"期望值 $E = 0(0.5)+10(0.3)+50(0.2) = {EV:.0f}$ 元",
        color=F.PURPLE,
        fontsize=12.5,
        ha="center",
    )
    ax.text(
        1.0, 0.54, "（以機率為權重的平均）", color=F.PURPLE, fontsize=11, ha="center"
    )
    ax.set_xlim(-0.7, 2.7)
    ax.set_ylim(-0.25, 0.72)
    ax.set_xticks([])
    ax.set_yticks([0, 0.2, 0.4])
    ax.set_ylabel("機率", fontsize=11)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.set_title("期望值＝加權平均", fontsize=13)

    fig.tight_layout()
    F.save_to(fig, CH, "數2-3-機率")


# =====================================================================
# 圖五：三集合取捨原理（三圓相交的文氏圖，標各區塊被加減的次數）
# =====================================================================
def fig_venn3():
    """三集合文氏圖：左圖標各區塊在『加單、減雙、加三』下被淨數幾次，
    右圖以『$2,3,5$ 的倍數』實例對照（例題 3-3b）。"""
    fig, axes = plt.subplots(1, 2, figsize=(12.4, 5.6))

    # 三圓中心（正三角形排列）與半徑
    R = 1.35
    cA = (-0.78, 0.46)
    cB = (0.78, 0.46)
    cC = (0.0, -0.92)
    circ = [(cA, F.BLUE), (cB, F.RED), (cC, F.GREEN)]

    def draw_three_circles(ax, fill_alpha=0.12):
        for c, col in circ:
            ax.add_patch(Circle(c, R, fc=col, ec=col, lw=2.2, alpha=fill_alpha))
        for c, col in circ:
            ax.add_patch(Circle(c, R, fill=False, ec=col, lw=2.2))

    # 各區塊的代表座標（七個區塊：三單、三雙、一三）
    # 只在 A、只在 B、只在 C
    pA = (cA[0] - 0.62, cA[1] + 0.30)
    pB = (cB[0] + 0.62, cB[1] + 0.30)
    pC = (cC[0], cC[1] - 0.66)
    # 恰兩兩交（不含三交）
    pAB = ((cA[0] + cB[0]) / 2, cA[1] + 0.56)
    pBC = (0.56, -0.42)
    pCA = (-0.56, -0.42)
    # 三交
    pABC = (0.0, 0.04)

    def set_labels(ax):
        for c, col, name, dx, dy in [
            (cA, F.BLUE, "$A$", -1.06, 0.92),
            (cB, F.RED, "$B$", 1.06, 0.92),
            (cC, F.GREEN, "$C$", 0.0, -1.30),
        ]:
            ax.text(
                c[0] + dx,
                c[1] + dy,
                name,
                color=col,
                fontsize=16,
                ha="center",
                va="center",
                fontweight="bold",
            )

    # ---- (左) 標「淨數幾次」----
    ax = axes[0]
    draw_three_circles(ax)
    set_labels(ax)
    # 三單區：加單一次 → 淨 +1
    for p in (pA, pB, pC):
        ax.text(p[0], p[1], "$+1$", color=F.INK, fontsize=13, ha="center", va="center")
    # 三雙區：加單兩次、減雙一次 → 2-1 = +1
    for p in (pAB, pBC, pCA):
        ax.text(
            p[0], p[1], "$2-1$", color="#8a3b00", fontsize=12, ha="center", va="center"
        )
    # 三交區：加單三次、減雙三次、加三一次 → 3-3+1 = +1
    ax.text(
        pABC[0],
        pABC[1] + 0.05,
        "$3-3+1$",
        color=F.PURPLE,
        fontsize=11.5,
        ha="center",
        va="center",
        fontweight="bold",
    )
    ax.set_title("每個區塊最後都「淨數恰好 1 次」", fontsize=13.5)

    # ---- (右) 以 1~100 中 2、3、5 的倍數實例對照（例題 3-3b）----
    ax = axes[1]
    draw_three_circles(ax)
    # 以 A=2 的倍數、B=3 的倍數、C=5 的倍數標各區個數
    # 三交 |A∩B∩C|=3；兩兩交（含三交）：AB=16, BC=6, CA=10
    # 恰兩兩交（不含三交）：AB' = 16-3=13, BC'=6-3=3, CA'=10-3=7
    # 三單（恰一）：A 只=50-13-7-3=27, B 只=33-13-3-3=14, C 只=20-7-3-3=7
    ax.text(
        cA[0] - 0.96,
        cA[1] + 1.18,
        "$A$：2 的倍數",
        color=F.BLUE,
        fontsize=11.5,
        ha="center",
    )
    ax.text(
        cB[0] + 0.96,
        cB[1] + 1.18,
        "$B$：3 的倍數",
        color=F.RED,
        fontsize=11.5,
        ha="center",
    )
    ax.text(
        cC[0], cC[1] - 1.34, "$C$：5 的倍數", color=F.GREEN, fontsize=11.5, ha="center"
    )
    nums = {pA: "27", pB: "14", pC: "7", pAB: "13", pBC: "3", pCA: "7", pABC: "3"}
    for p, n in nums.items():
        ax.text(p[0], p[1], n, color=F.INK, fontsize=12.5, ha="center", va="center")
    ax.set_title("實例：$1\\sim100$ 中 2、3、5 的倍數個數", fontsize=13.5)
    ax.text(
        0.0,
        -2.62,
        "$|A\\cup B\\cup C|=27+14+7+13+3+7+3=74$",
        color=F.PURPLE,
        fontsize=12.5,
        ha="center",
    )

    for ax in axes:
        ax.set_xlim(-2.5, 2.5)
        ax.set_ylim(-2.9, 2.2)
        ax.set_aspect("equal")
        ax.axis("off")

    fig.suptitle(
        "三集合取捨原理：$|A\\cup B\\cup C|=\\sum|A|-\\sum|A\\cap B|+|A\\cap B\\cap C|$"
        "（加單、減雙、加三）",
        fontsize=14,
        y=1.02,
    )
    fig.tight_layout()
    F.save_to(fig, CH, "數2-3-三集合取捨")


# =====================================================================
# 圖六：環狀排列（旋轉視為同一種，n! 收成 (n-1)!）
# =====================================================================
def fig_circular():
    """以 4 人圍圓桌示意：同一圈坐法旋轉 4 個位置看起來不同，其實算同一種，
    故環狀排列數＝直線排列 4! 再除以 4 ＝ (4-1)! = 3!。"""
    fig, axes = plt.subplots(1, 2, figsize=(11.0, 4.8))
    people = ["甲", "乙", "丙", "丁"]
    cols = [F.BLUE, F.RED, F.GREEN, F.AMBER]

    def draw_round_table(ax, start, title):
        # 圓桌
        ax.add_patch(Circle((0, 0), 0.62, fc="#f3f4f6", ec=F.INK, lw=1.6, zorder=1))
        n = 4
        for k in range(n):
            ang = np.pi / 2 - 2 * np.pi * k / n  # 從正上方開始、順時針
            x, y = 1.25 * np.cos(ang), 1.25 * np.sin(ang)
            idx = (start + k) % n
            ax.add_patch(Circle((x, y), 0.30, fc=cols[idx], ec=F.INK, lw=1.4, zorder=4))
            ax.text(
                x,
                y,
                people[idx],
                color="white",
                fontsize=14,
                ha="center",
                va="center",
                fontweight="bold",
                zorder=5,
            )
        ax.set_xlim(-1.9, 1.9)
        ax.set_ylim(-1.9, 1.9)
        ax.set_aspect("equal")
        ax.axis("off")
        ax.set_title(title, fontsize=12.5)

    # 左：同一圈坐法旋轉後的三個樣子，用一張代表 + 旋轉箭頭
    ax = axes[0]
    draw_round_table(ax, 0, "圍圓桌：只看「誰在誰旁邊」")
    # 旋轉箭頭
    ax.add_patch(
        FancyArrowPatch(
            (1.55, 0.55),
            (0.55, 1.55),
            arrowstyle="-|>",
            mutation_scale=16,
            lw=1.8,
            color=F.PURPLE,
            connectionstyle="arc3,rad=-0.35",
            zorder=6,
        )
    )
    ax.text(1.55, 1.62, "整桌旋轉", color=F.PURPLE, fontsize=11, ha="center")

    # 右：說明文字（公式推導）
    ax = axes[1]
    ax.axis("off")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    lines = [
        ("直線排列：4 個位置有頭有尾", F.INK, 0.86, 12.5),
        ("$4! = 24$ 種", F.INK, 0.76, 14),
        ("但圍成圈後，同一種坐法", F.INK, 0.60, 12.5),
        ("整體旋轉到 4 個位置都「一樣」", F.INK, 0.52, 12.5),
        ("（左右鄰居都沒變）", "#6b7280", 0.44, 11),
        ("被重複算了 4 次，要除掉：", F.RED, 0.30, 12.5),
        (r"$\frac{4!}{4} = (4-1)! = 3! = 6$ 種", F.PURPLE, 0.16, 15),
    ]
    for txt, col, y, fs in lines:
        ax.text(0.5, y, txt, color=col, fontsize=fs, ha="center", va="center")
    ax.set_title("環狀排列：旋轉視為同一種", fontsize=12.5)

    fig.suptitle(
        "環狀排列：$n$ 人圍圓桌 $=(n-1)!$（整體旋轉算同一種）",
        fontsize=14,
        y=1.02,
    )
    fig.tight_layout()
    F.save_to(fig, CH, "數2-3-環狀排列")


if __name__ == "__main__":
    fig_venn()
    fig_tree()
    fig_perm_comb()
    fig_prob()
    fig_venn3()
    fig_circular()
    print("done.")
