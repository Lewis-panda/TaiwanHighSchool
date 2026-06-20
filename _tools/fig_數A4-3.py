# -*- coding: utf-8 -*-
"""產生「數A4-3 機率統計」的圖，輸出到該章 sources/。
重繪：  .venv/bin/python _tools/fig_數A4-3.py
本章圖：條件機率（縮小樣本空間的文氏圖）、獨立 vs 互斥對比、
        貝氏樹（全機率／樹狀圖）、疾病篩檢偽陽性（自然頻率方塊圖）。
注意：matplotlib mathtext 不支援 \\dfrac/\\tfrac（用 \\frac）；中文勿放進 $...$。
"""

import os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, FancyArrowPatch, FancyBboxPatch
import figlib as F

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CH = os.path.join(ROOT, "數學", "數學二下（數學A·第四冊）", "數A4-3 機率統計")


# =====================================================================
# 圖一：條件機率 — 已知 B 發生，樣本空間縮小成 B
# =====================================================================
def fig_conditional():
    """左：原樣本空間 U 裡的 A、B；右：已知 B 後，世界縮小成 B，
    在 B 之內 A 佔的比例就是 P(A|B)。"""
    fig, axes = plt.subplots(1, 2, figsize=(11.6, 4.8))

    cA = (-0.45, 0.0)
    cB = (0.55, 0.0)
    rA, rB = 1.15, 1.25
    xs = np.linspace(-2.6, 2.6, 460)
    ys = np.linspace(-2.0, 2.0, 360)
    X, Y = np.meshgrid(xs, ys)
    inA = (X - cA[0]) ** 2 + (Y - cA[1]) ** 2 <= rA**2
    inB = (X - cB[0]) ** 2 + (Y - cB[1]) ** 2 <= rB**2

    # ---- (左) 原本的樣本空間 ----
    ax = axes[0]
    ax.add_patch(Rectangle((-2.4, -1.8), 4.8, 3.6, fill=False, ec=F.INK, lw=1.6))
    ax.text(-2.25, 1.55, "$U$", color=F.INK, fontsize=15, ha="left", va="top")
    ax.add_patch(Circle(cA, rA, fc=F.BLUE, ec=F.BLUE, lw=2.0, alpha=0.14))
    ax.add_patch(Circle(cB, rB, fc=F.RED, ec=F.RED, lw=2.0, alpha=0.14))
    ax.contourf(
        X, Y, (inA & inB).astype(float), levels=[0.5, 1.5], colors=[F.PURPLE], alpha=0.5
    )
    ax.add_patch(Circle(cA, rA, fill=False, ec=F.BLUE, lw=2.2))
    ax.add_patch(Circle(cB, rB, fill=False, ec=F.RED, lw=2.2))
    ax.text(cA[0] - 0.55, 0.9, "$A$", color=F.BLUE, fontsize=15, ha="center")
    ax.text(cB[0] + 0.6, 0.95, "$B$", color=F.RED, fontsize=15, ha="center")
    ax.text(0.12, -0.02, "$A\\cap B$", color="#3a1f6b", fontsize=11.5, ha="center")
    ax.set_title("原本：在整個 $U$ 裡看", fontsize=13)

    # ---- (右) 縮小到 B ----
    ax = axes[1]
    # 灰掉 B 以外的世界
    ax.add_patch(
        Rectangle((-2.4, -1.8), 4.8, 3.6, fc=F.GRID, ec=F.INK, lw=1.6, alpha=0.55)
    )
    # B 變成新的「整個世界」
    ax.add_patch(Circle(cB, rB, fc="white", ec=F.RED, lw=2.6, zorder=3))
    ax.contourf(
        X,
        Y,
        (inA & inB).astype(float),
        levels=[0.5, 1.5],
        colors=[F.PURPLE],
        alpha=0.55,
        zorder=4,
    )
    ax.add_patch(Circle(cB, rB, fill=False, ec=F.RED, lw=2.6, zorder=5))
    ax.text(
        cB[0] + 0.6,
        0.98,
        "新世界 $=B$",
        color=F.RED,
        fontsize=12.5,
        ha="center",
        zorder=6,
    )
    ax.text(
        0.12, -0.02, "$A\\cap B$", color="#3a1f6b", fontsize=11.5, ha="center", zorder=6
    )
    ax.text(
        0.0,
        -2.45,
        "$P(A\\mid B)=\\frac{P(A\\cap B)}{P(B)}$　（$A\\cap B$ 在 $B$ 裡佔多少）",
        color=F.PURPLE,
        fontsize=13.5,
        ha="center",
    )
    ax.set_title("已知 $B$ 發生：世界縮小成 $B$", fontsize=13)

    for ax in axes:
        ax.set_xlim(-2.6, 2.6)
        ax.set_ylim(-2.7, 2.0)
        ax.set_aspect("equal")
        ax.axis("off")

    fig.suptitle("條件機率：把分母從 $U$ 換成 $B$", fontsize=15, y=1.02)
    fig.tight_layout()
    F.save_to(fig, CH, "數A4-3-條件機率")


# =====================================================================
# 圖二：獨立 vs 互斥（最常混淆）
# =====================================================================
def fig_indep_vs_exclusive():
    """左：互斥（兩圓不相交，A∩B=∅）；右：獨立（兩圓相交，且重疊比例＝各自比例相乘）。"""
    fig, axes = plt.subplots(1, 2, figsize=(11.6, 5.0))

    # ---- (左) 互斥 ----
    ax = axes[0]
    ax.add_patch(Rectangle((-2.6, -1.9), 5.2, 3.8, fill=False, ec=F.INK, lw=1.6))
    ax.text(-2.45, 1.65, "$U$", color=F.INK, fontsize=14, ha="left", va="top")
    cA = (-1.15, 0.1)
    cB = (1.15, 0.1)
    ax.add_patch(Circle(cA, 0.95, fc=F.BLUE, ec=F.BLUE, lw=2.2, alpha=0.18))
    ax.add_patch(Circle(cA, 0.95, fill=False, ec=F.BLUE, lw=2.2))
    ax.add_patch(Circle(cB, 0.95, fc=F.RED, ec=F.RED, lw=2.2, alpha=0.18))
    ax.add_patch(Circle(cB, 0.95, fill=False, ec=F.RED, lw=2.2))
    ax.text(cA[0], cA[1], "$A$", color=F.BLUE, fontsize=16, ha="center", va="center")
    ax.text(cB[0], cB[1], "$B$", color=F.RED, fontsize=16, ha="center", va="center")
    ax.text(0.0, -1.45, "完全不重疊", color=F.INK, fontsize=12.5, ha="center")
    ax.text(
        0.0,
        -2.35,
        "$A\\cap B=\\varnothing,\\ \\ P(A\\cap B)=0$",
        color=F.AMBER,
        fontsize=13,
        ha="center",
    )
    ax.set_title("互斥（mutually exclusive）", fontsize=13.5)

    # ---- (右) 獨立 ----
    ax = axes[1]
    ax.add_patch(Rectangle((-2.6, -1.9), 5.2, 3.8, fill=False, ec=F.INK, lw=1.6))
    ax.text(-2.45, 1.65, "$U$", color=F.INK, fontsize=14, ha="left", va="top")
    cA = (-0.5, 0.1)
    cB = (0.6, 0.1)
    rA = rB = 1.15
    xs = np.linspace(-2.6, 2.6, 420)
    ys = np.linspace(-1.9, 1.9, 320)
    X, Y = np.meshgrid(xs, ys)
    inA = (X - cA[0]) ** 2 + (Y - cA[1]) ** 2 <= rA**2
    inB = (X - cB[0]) ** 2 + (Y - cB[1]) ** 2 <= rB**2
    ax.add_patch(Circle(cA, rA, fc=F.BLUE, ec=F.BLUE, lw=2.2, alpha=0.14))
    ax.add_patch(Circle(cB, rB, fc=F.RED, ec=F.RED, lw=2.2, alpha=0.14))
    ax.contourf(
        X, Y, (inA & inB).astype(float), levels=[0.5, 1.5], colors=[F.PURPLE], alpha=0.5
    )
    ax.add_patch(Circle(cA, rA, fill=False, ec=F.BLUE, lw=2.2))
    ax.add_patch(Circle(cB, rB, fill=False, ec=F.RED, lw=2.2))
    ax.text(cA[0] - 0.55, 0.95, "$A$", color=F.BLUE, fontsize=15, ha="center")
    ax.text(cB[0] + 0.55, 0.95, "$B$", color=F.RED, fontsize=15, ha="center")
    ax.text(0.05, 0.1, "$A\\cap B$", color="#3a1f6b", fontsize=11, ha="center")
    ax.text(
        0.0,
        -1.45,
        "有重疊，且重疊「比例剛好相乘」",
        color=F.INK,
        fontsize=12,
        ha="center",
    )
    ax.text(
        0.0,
        -2.35,
        "$P(A\\cap B)=P(A)\\,P(B)\\neq 0$",
        color=F.GREEN,
        fontsize=13,
        ha="center",
    )
    ax.set_title("獨立（independent）", fontsize=13.5)

    for ax in axes:
        ax.set_xlim(-2.7, 2.7)
        ax.set_ylim(-2.7, 1.9)
        ax.set_aspect("equal")
        ax.axis("off")

    fig.suptitle(
        "互斥 ≠ 獨立：互斥是「不會同時發生」，獨立是「互不影響」", fontsize=14.5, y=1.03
    )
    fig.tight_layout()
    F.save_to(fig, CH, "數A4-3-獨立vs互斥")


# =====================================================================
# 圖三：貝氏樹（全機率公式 / 樹狀圖）
# =====================================================================
def fig_bayes_tree():
    """機器 A、B 生產，各有不良率；樹狀圖展開全機率公式，葉子是各路徑機率。"""
    fig, ax = F.schematic(8.6, 5.6)

    root = (0.4, 2.6)
    ax.add_patch(Circle(root, 0.09, color=F.INK, zorder=6))
    ax.text(
        root[0] - 0.15,
        root[1],
        "抽一件",
        color=F.INK,
        fontsize=11.5,
        ha="right",
        va="center",
    )

    # 第一層：來自 A 機台 / B 機台
    lvl1 = [
        ("機台 $A$", (2.5, 4.0), F.BLUE, "$P(A)=0.6$"),
        ("機台 $B$", (2.5, 1.2), F.RED, "$P(B)=0.4$"),
    ]
    # 第二層：良品 / 不良
    sub = {
        "機台 $A$": [("不良", 0.05), ("良品", 0.95)],
        "機台 $B$": [("不良", 0.10), ("良品", 0.90)],
    }
    leaf_x = 5.2
    label_x = 6.6
    for name, pos, col, ptxt in lvl1:
        ax.plot([root[0], pos[0]], [root[1], pos[1]], color=col, lw=2.2, zorder=3)
        ax.add_patch(Circle(pos, 0.09, color=col, zorder=6))
        ax.text(
            pos[0],
            pos[1] + 0.26,
            name,
            color=col,
            fontsize=12.5,
            ha="center",
            va="bottom",
        )
        ax.text(
            (root[0] + pos[0]) / 2,
            (root[1] + pos[1]) / 2 + 0.18,
            ptxt,
            color=col,
            fontsize=11,
            ha="center",
            style="italic",
        )
        spread = 0.9
        defl = sub[name]
        sub_ys = [pos[1] + spread, pos[1] - spread]
        for (qname, q), sy in zip(defl, sub_ys):
            spos = (leaf_x, sy)
            lcol = F.AMBER if qname == "不良" else F.GREEN
            ax.plot(
                [pos[0], spos[0]],
                [pos[1], spos[1]],
                color=lcol,
                lw=1.6,
                alpha=0.9,
                zorder=2,
            )
            ax.add_patch(Circle(spos, 0.07, color=lcol, zorder=6))
            ax.text(
                (pos[0] + spos[0]) / 2,
                (pos[1] + sy) / 2 + 0.14,
                f"${q}$",
                color=lcol,
                fontsize=10.5,
                ha="center",
                style="italic",
            )
            pa = 0.6 if "A" in name else 0.4
            joint = pa * q
            mark = "  ←不良" if qname == "不良" else ""
            ax.text(
                label_x,
                sy,
                f"{pa}×{q} = {joint:.3f}{mark}",
                color=F.INK,
                fontsize=10.5,
                ha="left",
                va="center",
            )

    ax.text(
        4.3,
        -0.5,
        "全機率：P(不良) ＝ 0.6(0.05) ＋ 0.4(0.10) ＝ 0.07",
        color=F.PURPLE,
        fontsize=12.5,
        ha="center",
    )
    ax.set_xlim(-0.6, 8.6)
    ax.set_ylim(-0.9, 5.1)
    ax.set_title("貝氏樹：把「先分類、再看結果」攤成樹狀圖", fontsize=14)
    F.save_to(fig, CH, "數A4-3-貝氏樹")


# =====================================================================
# 圖四：疾病篩檢偽陽性（自然頻率方塊圖）
# =====================================================================
def fig_screening():
    """10000 人方塊圖：盛行率 1%，敏感度 99%，特異度 95%。
    陽性裡真正得病的比例（後驗）遠低於直覺。"""
    fig, ax = F.schematic(8.8, 6.0)

    # 參數
    N = 10000
    prev = 0.01  # 盛行率
    sens = 0.99  # 敏感度：得病且驗出陽性
    spec = 0.95  # 特異度：沒病且驗出陰性
    sick = int(N * prev)  # 100
    well = N - sick  # 9900
    TP = round(sick * sens)  # 99
    FN = sick - TP  # 1
    FP = round(well * (1 - spec))  # 495
    TN = well - FP  # 9405

    # 100x100 格，每格代表 1 人。先排得病者，再排沒病者。
    n_side = 100
    grid = np.zeros(
        (n_side, n_side)
    )  # 0 沒病陰性, 1 沒病陽性(偽陽), 2 得病陽性(真陽), 3 得病陰性(偽陰)
    flat = grid.reshape(-1)
    idx = 0
    flat[idx : idx + TP] = 2
    idx += TP
    flat[idx : idx + FN] = 3
    idx += FN
    flat[idx : idx + FP] = 1
    idx += FP
    flat[idx:] = 0
    grid = flat.reshape(n_side, n_side)

    cmap = {0: F.GRID, 1: F.AMBER, 2: F.RED, 3: "#7a1018"}
    # 畫格子（用 imshow 近似太密，改逐格小方塊但只描關鍵；這裡用 pcolormesh 上色）
    color_grid = np.empty((n_side, n_side, 3))

    def hex2rgb(h):
        h = h.lstrip("#")
        return tuple(int(h[i : i + 2], 16) / 255 for i in (0, 2, 4))

    rgb = {k: hex2rgb(v) for k, v in cmap.items()}
    for k, c in rgb.items():
        mask = grid == k
        for ch in range(3):
            color_grid[..., ch] = (
                np.where(mask, c[ch], color_grid[..., ch])
                if k != 0
                else color_grid[..., ch]
            )
    # 初始化底色為類別 0
    base = np.array(rgb[0])
    color_grid[:] = base
    for k in (1, 2, 3):
        mask = grid == k
        color_grid[mask] = rgb[k]

    ax.imshow(
        color_grid, origin="upper", extent=[0, 10, 0, 10], interpolation="nearest"
    )
    ax.add_patch(Rectangle((0, 0), 10, 10, fill=False, ec=F.INK, lw=1.6))
    ax.set_xlim(-0.4, 10.4)
    ax.set_ylim(-2.6, 10.7)
    ax.set_aspect("equal")
    ax.axis("off")

    ax.text(
        5,
        10.35,
        "10000 人（每格 1 人），盛行率 1%",
        color=F.INK,
        fontsize=12.5,
        ha="center",
    )

    # 圖例
    legend = [
        (F.RED, f"真陽性（得病，驗出）：{TP}"),
        ("#7a1018", f"偽陰性（得病，沒驗出）：{FN}"),
        (F.AMBER, f"偽陽性（沒病，誤判陽性）：{FP}"),
        (F.GRID, f"真陰性（沒病，驗陰）：{TN}"),
    ]
    for i, (c, t) in enumerate(legend):
        y = -0.7 - i * 0.52
        ax.add_patch(Rectangle((0.3, y - 0.16), 0.36, 0.36, fc=c, ec=F.INK, lw=1.0))
        ax.text(0.85, y, t, color=F.INK, fontsize=11.5, ha="left", va="center")

    ax.text(
        5.6, -0.7, f"驗出陽性者共 {TP + FP} 人，", color=F.INK, fontsize=11.5, ha="left"
    )
    ax.text(5.6, -1.3, f"其中真得病只 {TP} 人", color=F.RED, fontsize=11.5, ha="left")
    post = TP / (TP + FP)
    ax.text(
        5.6,
        -1.95,
        f"P(病｜陽) ＝ {TP}/{TP + FP} ≈ {post * 100:.0f}%",
        color=F.PURPLE,
        fontsize=13,
        ha="left",
    )

    ax.set_title("篩檢陽性 ≠ 真的得病：偽陽性把後驗機率壓低", fontsize=13.5)
    F.save_to(fig, CH, "數A4-3-篩檢")


# =====================================================================
# 圖五：相對次數的穩定（頻率觀的客觀機率／大數法則直覺）
# =====================================================================
def fig_relative_frequency():
    """模擬擲一顆「尖朝上機率 0.63 的圖釘」，畫出累計相對次數隨試驗次數的變化：
    次數少時劇烈跳動（不能定機率），次數多時逐漸穩定在 0.63（這個穩定值才是機率）。"""
    rng = np.random.default_rng(20240618)
    p_true = 0.63
    N = 1000
    outcomes = (rng.random(N) < p_true).astype(float)  # 1 = 尖朝上
    n = np.arange(1, N + 1)
    rel = np.cumsum(outcomes) / n  # 累計相對次數

    fig, ax = F.canvas(8.6, 4.8)
    F.clean_grid(ax)

    # 真值水平線
    ax.axhline(p_true, color=F.RED, lw=1.8, ls="--", zorder=3)
    ax.text(
        N * 1.005,
        p_true,
        "穩定值 0.63\n（這才是機率）",
        color=F.RED,
        fontsize=11,
        ha="left",
        va="center",
    )

    # 相對次數曲線
    ax.plot(n, rel, color=F.BLUE, lw=1.6, zorder=4)

    # 「少數幾次劇烈跳動」的警示區（前 50 次）
    ax.axvspan(1, 50, color=F.AMBER, alpha=0.12, zorder=1)
    ax.text(
        26,
        0.96,
        "次數少：劇烈跳動\n不能當機率",
        color=F.AMBER,
        fontsize=10.5,
        ha="center",
        va="top",
    )
    ax.annotate(
        "次數越多越穩定",
        xy=(720, rel[719]),
        xytext=(430, 0.30),
        color=F.INK,
        fontsize=11,
        ha="center",
        arrowprops=dict(arrowstyle="->", color=F.INK, lw=1.3),
    )

    ax.set_xlim(1, N)
    ax.set_ylim(0.0, 1.0)
    ax.set_xlabel("試驗次數 $n$")
    ax.set_ylabel("累計相對次數")
    ax.set_title("相對次數逐漸穩定：頻率觀下的客觀機率", fontsize=14)
    fig.tight_layout()
    F.save_to(fig, CH, "數A4-3-相對次數")


# =====================================================================
# 圖六：乘法公式 — 不放回連抽的樹狀圖（例題 3-5）
# =====================================================================
def fig_multiplication():
    """袋中 5 紅 3 白，不放回連抽兩顆。樹狀圖把每條路徑的條件機率連乘，
    強調「第二次的機率被第一次改變」（不放回 ⇒ 不獨立）。"""
    fig, ax = F.schematic(8.8, 5.4)

    root = (0.5, 2.3)
    ax.add_patch(Circle(root, 0.09, color=F.INK, zorder=6))
    ax.text(
        root[0] - 0.15,
        root[1],
        "袋中\n5 紅 3 白",
        color=F.INK,
        fontsize=11,
        ha="right",
        va="center",
    )

    # 第一層：第一顆 紅 / 白
    lvl1 = [
        ("第一顆紅", (2.7, 3.9), F.RED, "5/8"),
        ("第一顆白", (2.7, 0.7), F.GREEN, "3/8"),
    ]
    # 第二層條件機率（已抽走一顆，分母變 7）
    sub = {
        "第一顆紅": [("第二顆紅", "4/7", F.RED), ("第二顆白", "3/7", F.GREEN)],
        "第一顆白": [("第二顆紅", "5/7", F.RED), ("第二顆白", "2/7", F.GREEN)],
    }
    p1map = {"第一顆紅": (5, 8), "第一顆白": (3, 8)}
    q2map = {
        "第二顆紅": {"第一顆紅": (4, 7), "第一顆白": (5, 7)},
        "第二顆白": {"第一顆紅": (3, 7), "第一顆白": (2, 7)},
    }
    leaf_x = 5.4
    label_x = 6.5
    for name, pos, col, ptxt in lvl1:
        ax.plot([root[0], pos[0]], [root[1], pos[1]], color=col, lw=2.2, zorder=3)
        ax.add_patch(Circle(pos, 0.09, color=col, zorder=6))
        ax.text(
            pos[0],
            pos[1] + 0.24,
            name,
            color=col,
            fontsize=11.5,
            ha="center",
            va="bottom",
        )
        ax.text(
            (root[0] + pos[0]) / 2,
            (root[1] + pos[1]) / 2 + 0.16,
            f"${ptxt}$",
            color=col,
            fontsize=11,
            ha="center",
            style="italic",
        )
        spread = 0.9
        sub_ys = [pos[1] + spread, pos[1] - spread]
        for (qname, qtxt, qcol), sy in zip(sub[name], sub_ys):
            spos = (leaf_x, sy)
            ax.plot(
                [pos[0], spos[0]],
                [pos[1], spos[1]],
                color=qcol,
                lw=1.6,
                alpha=0.9,
                zorder=2,
            )
            ax.add_patch(Circle(spos, 0.07, color=qcol, zorder=6))
            ax.text(
                (pos[0] + spos[0]) / 2,
                (pos[1] + sy) / 2 + 0.13,
                f"${qtxt}$",
                color=qcol,
                fontsize=10.5,
                ha="center",
                style="italic",
            )
            an, ad = p1map[name]
            bn, bd = q2map[qname][name]
            jn, jd = an * bn, ad * bd
            mark = "  ←兩顆都紅" if (name == "第一顆紅" and qname == "第二顆紅") else ""
            ax.text(
                label_x,
                sy,
                f"${an}/{ad}$×${bn}/{bd}$ = ${jn}/{jd}${mark}",
                color=F.INK,
                fontsize=10.5,
                ha="left",
                va="center",
            )

    ax.text(
        4.2,
        -0.55,
        "乘法公式：P(兩顆都紅) ＝ 5/8 × 4/7 ＝ 5/14（第二步分母變 7：不放回⇒不獨立）",
        color=F.PURPLE,
        fontsize=11.5,
        ha="center",
    )
    ax.set_xlim(-0.7, 8.8)
    ax.set_ylim(-1.0, 4.9)
    ax.set_title("乘法公式：沿路徑把每一步的條件機率連乘", fontsize=14)
    F.save_to(fig, CH, "數A4-3-乘法公式")


if __name__ == "__main__":
    fig_conditional()
    fig_indep_vs_exclusive()
    fig_bayes_tree()
    fig_screening()
    fig_relative_frequency()
    fig_multiplication()
    print("done.")
