# -*- coding: utf-8 -*-
"""產生「選物II-1 動量與角動量」的圖，輸出到該章 sources/。
重繪：  .venv/bin/python _tools/fig_選物II-1.py
"""

import os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon, Circle, FancyArrowPatch
import figlib as F

# numpy 2.x 移除了 np.trapz（改名 np.trapezoid）；兩種環境都可跑
_trapz = getattr(np, "trapezoid", getattr(np, "trapz", None))

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CH = os.path.join(
    ROOT, "物理", "物理二下（選修物理II·力學二，僅力學）", "選物II-1 動量與角動量"
)


def fig_impulse():
    """F–t 圖：曲線下的面積 = 衝量 = 動量變化。右圖對比同 Δp、短碰撞 vs 長緩衝。"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.4, 4.0))

    # 左：一次撞擊的 F–t 曲線，面積 = 衝量
    t = np.linspace(0, 6, 400)
    Fpeak = 9.0
    Fc = Fpeak * np.exp(-((t - 3.0) ** 2) / 0.9)
    ax1.plot(t, Fc, color=F.BLUE, lw=2.6)
    ax1.fill_between(t, 0, Fc, color=F.FILL, alpha=0.16)
    ax1.text(
        3.0,
        3.4,
        "面積\n= 衝量 $J$\n= $\\Delta p$",
        ha="center",
        va="center",
        color=F.BLUE,
        fontsize=12,
    )
    # 平均力虛線
    Favg = _trapz(Fc, t) / 6.0
    ax1.hlines(Favg, 0, 6, color=F.AMBER, lw=1.8, ls="--")
    ax1.text(
        5.85, Favg + 0.35, "平均力 $\\bar F$", color=F.AMBER, ha="right", fontsize=11
    )
    ax1.set_xlim(0, 6)
    ax1.set_ylim(0, 10)
    ax1.set_xlabel("時間 $t$")
    ax1.set_ylabel("作用力 $F$")
    ax1.set_xticks([])
    ax1.set_yticks([])
    ax1.set_title("衝量 = $F$–$t$ 圖下的面積", fontsize=13)
    F.clean_grid(ax1)

    # 右：同樣的 Δp（面積相等），但作用時間長 → 峰值力小（緩衝原理）
    tA = np.linspace(0, 6, 400)
    # 短而猛
    Fshort = 9.0 * np.exp(-((tA - 1.4) ** 2) / 0.10)
    # 長而緩（面積調成相同）
    Flong = np.exp(-((tA - 3.6) ** 2) / 1.6)
    Flong = Flong * (_trapz(Fshort, tA) / _trapz(Flong, tA))
    ax2.plot(tA, Fshort, color=F.RED, lw=2.5, label="硬碰（$\\Delta t$ 短 → $F$ 大）")
    ax2.fill_between(tA, 0, Fshort, color=F.RED, alpha=0.10)
    ax2.plot(tA, Flong, color=F.GREEN, lw=2.5, label="緩衝（$\\Delta t$ 長 → $F$ 小）")
    ax2.fill_between(tA, 0, Flong, color=F.GREEN, alpha=0.12)
    ax2.text(
        3.6,
        1.0,
        "面積相同\n（$\\Delta p$ 一樣）",
        ha="center",
        color=F.INK,
        fontsize=10.5,
    )
    ax2.set_xlim(0, 6)
    ax2.set_ylim(0, 10)
    ax2.set_xlabel("時間 $t$")
    ax2.set_ylabel("作用力 $F$")
    ax2.set_xticks([])
    ax2.set_yticks([])
    ax2.set_title("同樣 $\\Delta p$，拉長時間 → 力變小", fontsize=13)
    ax2.legend(loc="upper right", fontsize=9.5, frameon=False)
    F.clean_grid(ax2)

    fig.tight_layout()
    F.save_to(fig, CH, "選物II-1-動量衝量")


def _ball(ax, x, y, r, color, text=None, tcolor="white"):
    ax.add_patch(Circle((x, y), r, facecolor=color, edgecolor=F.INK, lw=1.4, zorder=4))
    if text:
        ax.text(
            x, y, text, ha="center", va="center", color=tcolor, fontsize=11, zorder=5
        )


def fig_collision():
    """一維碰撞：彈性 vs 完全非彈性，碰前/碰後速度示意。"""
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8.4, 5.4))

    def lane(ax, title):
        ax.axhline(0, color=F.INK, lw=1.4)
        ax.set_xlim(0, 12)
        ax.set_ylim(-2.2, 2.2)
        ax.axis("off")
        ax.text(0.1, 1.9, title, fontsize=12.5, color=F.INK, ha="left", va="top")

    def vlabel(ax, x, y, vx, text, color):
        if abs(vx) > 1e-3:
            F.arrow(ax, (x, y), (x + vx, y), color=color, lw=2.4, mutation=16)
        ax.text(x, y + 0.55, text, ha="center", color=color, fontsize=11)

    # --- 彈性碰撞（等質量交換速度）---
    lane(ax1, "彈性碰撞（動量、動能皆守恆）")
    ax1.text(11.9, 1.55, "碰前", ha="right", color="#888", fontsize=10)
    # 碰前：A 動、B 靜
    _ball(ax1, 2.0, 0.8, 0.42, F.BLUE, "A")
    vlabel(ax1, 2.0, 0.8, 1.4, "$v$", F.BLUE)
    _ball(ax1, 4.4, 0.8, 0.42, F.RED, "B")
    ax1.text(4.4, 1.35, "靜止", ha="center", color=F.RED, fontsize=10)
    # 箭頭分隔
    ax1.annotate(
        "",
        xy=(6.4, 0.0),
        xytext=(5.6, 0.0),
        arrowprops=dict(arrowstyle="-|>", color="#888", lw=1.6),
    )
    # 碰後：A 停、B 走（等質量交換）
    ax1.text(11.9, -1.65, "碰後", ha="right", color="#888", fontsize=10)
    _ball(ax1, 7.7, -0.9, 0.42, F.BLUE, "A")
    ax1.text(7.7, -0.32, "停下", ha="center", color=F.BLUE, fontsize=10)
    _ball(ax1, 9.6, -0.9, 0.42, F.RED, "B")
    vlabel(ax1, 9.6, -0.9, 1.4, "$v$", F.RED)

    # --- 完全非彈性碰撞（黏在一起）---
    lane(ax2, "完全非彈性碰撞（黏在一起，動能損失）")
    ax2.text(11.9, 1.55, "碰前", ha="right", color="#888", fontsize=10)
    _ball(ax2, 2.0, 0.8, 0.42, F.BLUE, "A")
    vlabel(ax2, 2.0, 0.8, 1.4, "$v$", F.BLUE)
    _ball(ax2, 4.4, 0.8, 0.42, F.RED, "B")
    ax2.text(4.4, 1.35, "靜止", ha="center", color=F.RED, fontsize=10)
    ax2.annotate(
        "",
        xy=(6.4, 0.0),
        xytext=(5.6, 0.0),
        arrowprops=dict(arrowstyle="-|>", color="#888", lw=1.6),
    )
    ax2.text(11.9, -1.65, "碰後", ha="right", color="#888", fontsize=10)
    # 黏在一起
    _ball(ax2, 8.3, -0.9, 0.42, F.BLUE, "A")
    _ball(ax2, 8.96, -0.9, 0.42, F.RED, "B")
    vlabel(ax2, 8.96, -0.9, 0.9, "$v'<v$", F.PURPLE)

    fig.suptitle("一維碰撞：碰前後速度（動量都守恆，動能不一定）", fontsize=13.5)
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    F.save_to(fig, CH, "選物II-1-碰撞")


def fig_collision_2d():
    """二維碰撞：左——動量向量守恆（碰前 = 碰後兩動量向量和，x/y 分量各自守恆）；
    右——等質量彈性偏心碰撞，碰後兩速度必成 90 度分開。"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.8, 4.6))

    # ---------- 左：一般二維碰撞，動量向量守恆＋分量 ----------
    ax1.set_aspect("equal")
    ax1.axis("off")
    O = np.array([0.0, 0.0])

    # 碰前：單一入射動量 p（沿 +x）
    p_in = np.array([4.2, 0.0])
    # 碰後：兩動量分向兩側，向量和 = p_in（守恆）
    p1 = np.array([2.7, 1.7])  # 球1 碰後動量（偏上）
    p2 = p_in - p1  # 球2 碰後動量（偏下），確保 p1+p2 = p_in

    # 碰前動量（灰、加粗，當作總動量基準）
    F.arrow(ax1, O, p_in, color="#888", lw=3.0, mutation=20)
    ax1.text(
        p_in[0] + 0.15,
        p_in[1] - 0.42,
        "碰前總動量",
        color="#666",
        fontsize=10.5,
        ha="center",
    )
    ax1.text(
        p_in[0] * 0.5,
        -0.42,
        "$\\vec p$",
        color="#666",
        fontsize=13,
        ha="center",
    )

    # 碰後兩動量（從原點畫出）
    F.arrow(ax1, O, p1, color=F.BLUE, lw=2.6)
    ax1.text(p1[0] - 0.35, p1[1] + 0.30, "$\\vec p_1'$", color=F.BLUE, fontsize=13)
    F.arrow(ax1, O, p2, color=F.RED, lw=2.6)
    ax1.text(p2[0] - 0.55, p2[1] - 0.10, "$\\vec p_2'$", color=F.RED, fontsize=13)

    # 平行四邊形：示意 p1 + p2 = p_in（向量和）
    ax1.plot(
        [p1[0], p_in[0]],
        [p1[1], p_in[1]],
        color=F.BLUE,
        lw=1.1,
        ls="--",
        alpha=0.7,
    )
    ax1.plot(
        [p2[0], p_in[0]],
        [p2[1], p_in[1]],
        color=F.RED,
        lw=1.1,
        ls="--",
        alpha=0.7,
    )

    # y 分量互相抵消的標註（p1 向上、p2 向下，碰前 y 分量為 0）
    ax1.annotate(
        "",
        xy=(p1[0], p1[1]),
        xytext=(p1[0], 0.0),
        arrowprops=dict(arrowstyle="-", color=F.BLUE, lw=1.0, ls=(0, (2, 2))),
    )
    ax1.annotate(
        "",
        xy=(p2[0], p2[1]),
        xytext=(p2[0], 0.0),
        arrowprops=dict(arrowstyle="-", color=F.RED, lw=1.0, ls=(0, (2, 2))),
    )
    ax1.axhline(0, color=F.INK, lw=0.8, alpha=0.4)

    ax1.text(
        2.4,
        -2.05,
        "x 分量：相加守恆      y 分量：上下抵消（碰前為零）",
        color=F.INK,
        fontsize=10.5,
        ha="center",
        va="top",
    )
    ax1.set_xlim(-0.6, 5.4)
    ax1.set_ylim(-2.6, 2.7)
    ax1.set_title("動量向量守恆：分 x、y 各自守恆", fontsize=12.5)

    # ---------- 右：等質量彈性偏心碰撞 → 兩速度成直角 ----------
    ax2.set_aspect("equal")
    ax2.axis("off")
    C = np.array([0.0, 0.0])

    v_in = np.array([3.6, 0.0])  # 母球碰前速度（沿 +x）
    ang1 = np.deg2rad(30.0)  # 母球碰後偏 +30 度
    ang2 = ang1 - np.deg2rad(90.0)  # 目標球碰後偏 -60 度（與母球差 90 度）
    # 等質量彈性：v1'^2 + v2'^2 = v_in^2，且方向正交
    s1 = np.linalg.norm(v_in) * np.cos(ang1)  # 母球碰後速率
    s2 = np.linalg.norm(v_in) * np.sin(ang1)  # 目標球碰後速率
    v1p = s1 * np.array([np.cos(ang1), np.sin(ang1)])
    v2p = s2 * np.array([np.cos(ang2), np.sin(ang2)])

    # 碰前速度（灰）
    F.arrow(ax2, C - np.array([2.2, 0.0]), C, color="#888", lw=2.6, mutation=18)
    ax2.text(
        C[0] - 1.1,
        0.28,
        "碰前 $\\vec v$",
        color="#666",
        fontsize=11,
        ha="center",
    )
    # 碰撞點兩球
    ax2.add_patch(Circle(C, 0.16, facecolor=F.BLUE, edgecolor=F.INK, lw=1.3, zorder=5))

    # 碰後兩速度
    F.arrow(ax2, C, v1p, color=F.BLUE, lw=2.6)
    ax2.text(
        v1p[0] + 0.18,
        v1p[1] + 0.18,
        "$\\vec v_1'$（母球）",
        color=F.BLUE,
        fontsize=12,
        ha="left",
    )
    F.arrow(ax2, C, v2p, color=F.RED, lw=2.6)
    ax2.text(
        v2p[0] + 0.12,
        v2p[1] - 0.30,
        "$\\vec v_2'$（目標球）",
        color=F.RED,
        fontsize=12,
        ha="left",
        va="top",
    )

    # 直角符號（在兩碰後速度之間）
    u1 = v1p / np.linalg.norm(v1p)
    u2 = v2p / np.linalg.norm(v2p)
    d = 0.5
    corner = C + d * u1 + d * u2
    ax2.plot(
        [C[0] + d * u1[0], corner[0]],
        [C[1] + d * u1[1], corner[1]],
        color=F.PURPLE,
        lw=1.4,
    )
    ax2.plot(
        [C[0] + d * u2[0], corner[0]],
        [C[1] + d * u2[1], corner[1]],
        color=F.PURPLE,
        lw=1.4,
    )
    # 角度標註
    F.angle_arc(
        ax2,
        C,
        0.95,
        np.rad2deg(ang2),
        np.rad2deg(ang1),
        color=F.PURPLE,
        text="$90^\\circ$",
    )

    ax2.text(
        1.3,
        -2.35,
        "等質量、彈性、偏心碰撞\n碰後兩速度必成直角",
        color=F.PURPLE,
        fontsize=11,
        ha="center",
        va="top",
    )
    ax2.set_xlim(-2.7, 3.9)
    ax2.set_ylim(-2.9, 2.4)
    ax2.set_title("等質量彈性偏心碰撞：直角分開", fontsize=12.5)

    fig.suptitle("二維碰撞：動量向量守恆（分量各自守恆）", fontsize=13.5)
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    F.save_to(fig, CH, "選物II-1-二維碰撞")


def fig_center_of_mass():
    """兩質點的質心位置（靠近大質量一側），與系統運動。"""
    fig, ax = F.schematic(8.2, 3.6)
    y0 = 0.0
    # 數線
    ax.annotate(
        "",
        xy=(9.5, y0),
        xytext=(-0.4, y0),
        arrowprops=dict(arrowstyle="-|>", color=F.INK, lw=1.6),
    )
    ax.text(9.5, y0 - 0.55, "$x$", color=F.INK, fontsize=12)

    # 質點 1：m1 = 1 在 x=1；質點 2：m2 = 3 在 x=7 → 質心 x_cm = (1*1+3*7)/4 = 5.5
    x1, m1 = 1.0, 1.0
    x2, m2 = 7.0, 3.0
    xcm = (m1 * x1 + m2 * x2) / (m1 + m2)

    for x in (x1, x2, xcm):
        ax.plot([x, x], [y0 - 0.12, y0 + 0.12], color=F.INK, lw=1.3)

    # 兩質點（半徑表大小）
    ax.add_patch(
        Circle((x1, y0), 0.30, facecolor=F.BLUE, edgecolor=F.INK, lw=1.4, zorder=4)
    )
    ax.text(x1, y0 + 0.75, "$m_1$", ha="center", color=F.BLUE, fontsize=13)
    ax.text(x1, y0 - 0.62, "$x_1=1$", ha="center", color=F.INK, fontsize=10.5)

    ax.add_patch(
        Circle((x2, y0), 0.52, facecolor=F.RED, edgecolor=F.INK, lw=1.4, zorder=4)
    )
    ax.text(x2, y0 + 0.95, "$m_2=3m_1$", ha="center", color=F.RED, fontsize=13)
    ax.text(x2, y0 - 0.82, "$x_2=7$", ha="center", color=F.INK, fontsize=10.5)

    # 質心（叉號標記）
    ax.plot([xcm], [y0], marker="x", color=F.PURPLE, ms=14, mew=3, zorder=6)
    ax.text(
        xcm, y0 + 1.15, "質心 $x_{cm}=5.5$", ha="center", color=F.PURPLE, fontsize=12.5
    )
    ax.annotate(
        "",
        xy=(xcm, y0 + 0.65),
        xytext=(xcm, y0 + 1.0),
        arrowprops=dict(arrowstyle="-|>", color=F.PURPLE, lw=1.6),
    )

    # 槓桿平衡提示：到兩質點的距離與質量成反比
    ax.annotate(
        "",
        xy=(x1 + 0.35, y0 - 1.35),
        xytext=(xcm - 0.05, y0 - 1.35),
        arrowprops=dict(arrowstyle="<->", color="#888", lw=1.2),
    )
    ax.text(
        (x1 + xcm) / 2, y0 - 1.62, "$4.5$", ha="center", color="#888", fontsize=10.5
    )
    ax.annotate(
        "",
        xy=(xcm + 0.05, y0 - 1.35),
        xytext=(x2 - 0.55, y0 - 1.35),
        arrowprops=dict(arrowstyle="<->", color="#888", lw=1.2),
    )
    ax.text(
        (xcm + x2) / 2, y0 - 1.62, "$1.5$", ha="center", color="#888", fontsize=10.5
    )
    ax.text(
        xcm,
        y0 - 2.15,
        "距離比 $4.5:1.5=3:1=m_2:m_1$（質心偏向大質量）",
        ha="center",
        color="#666",
        fontsize=11,
    )

    ax.set_xlim(-0.6, 10.0)
    ax.set_ylim(-2.5, 1.7)
    ax.set_title(
        "兩質點的質心：$x_{cm}=\\dfrac{m_1x_1+m_2x_2}{m_1+m_2}$", fontsize=13.5
    )
    F.save_to(fig, CH, "選物II-1-質心")


def fig_angular_momentum():
    """溜冰選手收手：I 變小 → ω 變大（角動量守恆）。左定義 L=r×p，右收手加速。"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.6, 4.4))

    # 左：L = r × p 的定義示意
    ax1.set_aspect("equal")
    ax1.axis("off")
    O = np.array([0.0, 0.0])
    P = np.array([2.6, 1.4])
    ax1.add_patch(Circle(O, 0.08, color=F.INK, zorder=6))
    ax1.text(O[0] - 0.25, O[1] - 0.05, "$O$", ha="right", fontsize=13)
    # r 向量
    F.arrow(ax1, O, P, color=F.GREEN, lw=2.4)
    ax1.text(1.2, 0.95, "$\\vec r$", color=F.GREEN, fontsize=14)
    # 質點與動量 p（與 r 不共線）
    ax1.add_patch(Circle(P, 0.16, facecolor=F.BLUE, edgecolor=F.INK, lw=1.4, zorder=5))
    pvec = np.array([1.6, -0.5])
    F.arrow(ax1, P, P + pvec, color=F.RED, lw=2.4)
    ax1.text(
        P[0] + 1.7,
        P[1] - 0.95,
        "$\\vec p=m\\vec v$",
        color=F.RED,
        fontsize=13,
        ha="center",
    )
    ax1.text(P[0] + 0.1, P[1] + 0.35, "$m$", color=F.BLUE, fontsize=12)
    # L 出紙面符號
    ax1.add_patch(Circle((0.55, 2.05), 0.28, fill=False, edgecolor=F.PURPLE, lw=1.8))
    ax1.add_patch(Circle((0.55, 2.05), 0.05, color=F.PURPLE))
    ax1.text(
        1.05,
        2.05,
        "$\\vec L=\\vec r\\times\\vec p$（出紙面）",
        color=F.PURPLE,
        fontsize=12,
        va="center",
    )
    ax1.set_xlim(-1.0, 4.6)
    ax1.set_ylim(-1.3, 2.6)
    ax1.set_title("角動量 $\\vec L=\\vec r\\times\\vec p$", fontsize=13.5)

    # 右：溜冰選手收手 I↓ → ω↑
    def skater(ax, cx, arm, omega_label, col, sub):
        # 身體
        ax.add_patch(
            Circle((cx, 1.7), 0.22, facecolor=col, edgecolor=F.INK, lw=1.3, zorder=4)
        )  # 頭
        ax.add_patch(
            Rectangle(
                (cx - 0.13, 0.4),
                0.26,
                1.15,
                facecolor=col,
                edgecolor=F.INK,
                lw=1.3,
                zorder=3,
            )
        )  # 軀幹
        # 手臂（arm = 伸展長度）
        ax.plot(
            [cx, cx - arm],
            [1.35, 1.35 + 0.15],
            color=F.INK,
            lw=3.0,
            solid_capstyle="round",
            zorder=5,
        )
        ax.plot(
            [cx, cx + arm],
            [1.35, 1.35 + 0.15],
            color=F.INK,
            lw=3.0,
            solid_capstyle="round",
            zorder=5,
        )
        # 手上的點
        ax.add_patch(Circle((cx - arm, 1.5), 0.10, color=F.AMBER, zorder=6))
        ax.add_patch(Circle((cx + arm, 1.5), 0.10, color=F.AMBER, zorder=6))
        # 旋轉箭頭
        ax.annotate(
            "",
            xy=(cx + 0.55, 0.05),
            xytext=(cx - 0.55, 0.05),
            arrowprops=dict(
                arrowstyle="-|>",
                color=F.PURPLE,
                lw=2.0,
                connectionstyle="arc3,rad=-0.5",
            ),
        )
        ax.text(cx, -0.35, omega_label, ha="center", color=F.PURPLE, fontsize=13)
        ax.text(cx, 2.25, sub, ha="center", color=F.INK, fontsize=11)

    ax2.set_aspect("equal")
    ax2.axis("off")
    skater(ax2, 1.6, 1.15, "$\\omega$ 小", F.BLUE, "張開手臂\n$I$ 大")
    skater(ax2, 5.0, 0.42, "$\\omega$ 大", F.RED, "收回手臂\n$I$ 小")
    ax2.annotate(
        "",
        xy=(3.75, 1.0),
        xytext=(2.95, 1.0),
        arrowprops=dict(arrowstyle="-|>", color=F.INK, lw=1.8),
    )
    ax2.text(3.35, 1.35, "收手", ha="center", color=F.INK, fontsize=11)
    ax2.text(
        3.3,
        -1.05,
        "$L=I\\omega$ 守恆：$I\\downarrow \\Rightarrow \\omega\\uparrow$",
        ha="center",
        color=F.INK,
        fontsize=12.5,
    )
    ax2.set_xlim(0.0, 6.6)
    ax2.set_ylim(-1.5, 2.7)
    ax2.set_title("溜冰選手收手轉更快（角動量守恆）", fontsize=13.5)

    fig.tight_layout()
    F.save_to(fig, CH, "選物II-1-角動量")


if __name__ == "__main__":
    fig_impulse()
    fig_collision()
    fig_collision_2d()
    fig_center_of_mass()
    fig_angular_momentum()
    print("done.")
