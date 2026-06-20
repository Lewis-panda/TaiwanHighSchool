# -*- coding: utf-8 -*-
"""產生「選物I-4 牛頓運動定律」的圖，輸出到該章 sources/。
重繪：  .venv/bin/python _tools/fig_選物I-4.py
"""

import os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon, Arc, Circle, FancyArrowPatch
import figlib as F

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CH = os.path.join(ROOT, "物理", "物理二上（選修物理I·力學一）", "選物I-4 牛頓運動定律")


def fig_vector_add():
    """力的合成與分解：平行四邊形法 + 分量。"""
    fig, ax = F.schematic(6.6, 5.0)
    O = np.array([0.0, 0.0])
    F1 = np.array([3.4, 0.6])  # 力 F1
    F2 = np.array([1.1, 2.8])  # 力 F2
    R = F1 + F2  # 合力

    # 平行四邊形（虛線輔助邊）
    ax.plot([F1[0], R[0]], [F1[1], R[1]], color=F.GRID, lw=1.4, ls="--", zorder=1)
    ax.plot([F2[0], R[0]], [F2[1], R[1]], color=F.GRID, lw=1.4, ls="--", zorder=1)

    # 兩分力
    F.arrow(ax, O, F1, color=F.BLUE)
    F.label(ax, F1 + np.array([0.15, -0.32]), r"$\vec F_1$", color=F.BLUE, ha="left")
    F.arrow(ax, O, F2, color=F.GREEN)
    F.label(ax, F2 + np.array([-0.42, 0.10]), r"$\vec F_2$", color=F.GREEN, ha="right")
    # 合力
    F.arrow(ax, O, R, color=F.RED, lw=2.8)
    F.label(
        ax,
        R + np.array([0.20, 0.18]),
        r"$\vec R=\vec F_1+\vec F_2$",
        color=F.RED,
        ha="left",
    )

    F.label(ax, np.array([0.0, -0.45]), "起點 O", color=F.INK, fs=11)
    ax.set_title("力的合成（平行四邊形法）", fontsize=14)
    ax.set_xlim(-1.0, 6.3)
    ax.set_ylim(-1.0, 4.2)
    F.save_to(fig, CH, "選物I-4-力的合成分解")


def fig_decompose():
    """一個斜向力分解成正交分量 Fx, Fy。"""
    fig, ax = F.schematic(5.6, 5.0)
    O = np.array([0.0, 0.0])
    th = np.deg2rad(38)
    Fmag = 3.6
    Fv = np.array([Fmag * np.cos(th), Fmag * np.sin(th)])

    # 分量虛線盒
    ax.plot([Fv[0], Fv[0]], [0, Fv[1]], color=F.GRID, lw=1.4, ls="--", zorder=1)
    ax.plot([0, Fv[0]], [Fv[1], Fv[1]], color=F.GRID, lw=1.4, ls="--", zorder=1)
    # 主力
    F.arrow(ax, O, Fv, color=F.RED, lw=2.8)
    F.label(ax, Fv + np.array([0.15, 0.20]), r"$\vec F$", color=F.RED, ha="left")
    # 分量
    F.arrow(ax, O, np.array([Fv[0], 0]), color=F.BLUE)
    F.label(ax, np.array([Fv[0] / 2, -0.35]), r"$F_x=F\cos\theta$", color=F.BLUE, fs=12)
    F.arrow(ax, O, np.array([0, Fv[1]]), color=F.GREEN)
    F.label(
        ax,
        np.array([-0.25, Fv[1] / 2]),
        r"$F_y=F\sin\theta$",
        color=F.GREEN,
        ha="right",
        fs=12,
    )
    # 角
    ax.add_patch(Arc(O, 1.5, 1.5, angle=0, theta1=0, theta2=38, color=F.INK, lw=1.4))
    ax.text(0.95, 0.30, r"$\theta$", color=F.INK, fontsize=14)

    ax.set_title("力的分解（正交分量）", fontsize=14)
    ax.set_xlim(-0.9, 3.6)
    ax.set_ylim(-0.8, 3.0)
    F.save_to(fig, CH, "選物I-4-力的分解")


def fig_incline_fbd():
    """斜面自由體圖：重力分解、正向力、摩擦。"""
    fig, ax = F.schematic(6.6, 5.2)
    th = np.deg2rad(32)
    A = np.array([-3.3, -1.7])  # 斜角 θ 所在頂點
    B = np.array([3.3, -1.7])  # 直角
    C = np.array([3.3, -1.7 + 6.6 * np.tan(th)])
    ax.add_patch(
        Polygon(
            [A, B, C],
            closed=True,
            facecolor="#eef1f5",
            edgecolor=F.INK,
            lw=1.6,
            hatch="\\\\\\",
        )
    )
    u = np.array([np.cos(th), np.sin(th)])  # 沿斜面向上
    n = np.array([-np.sin(th), np.cos(th)])  # 垂直斜面向外
    M = (A + C) / 2
    c0 = M + n * 0.5  # 物體中心
    s, tk = 1.0, 0.66
    corners = [
        c0 - u * s / 2 - n * tk / 2,
        c0 + u * s / 2 - n * tk / 2,
        c0 + u * s / 2 + n * tk / 2,
        c0 - u * s / 2 + n * tk / 2,
    ]
    ax.add_patch(
        Polygon(
            corners, closed=True, facecolor="#dbe7ff", edgecolor=F.INK, lw=1.6, zorder=3
        )
    )
    ax.add_patch(Circle(c0, 0.05, color=F.INK, zorder=6))
    _bb = dict(boxstyle="round,pad=0.12", fc="white", ec="none", alpha=0.9)

    # 重力（紅，向下）
    F.arrow(ax, c0, c0 + np.array([0, -2.1]), color=F.RED)
    F.label(ax, c0 + np.array([0.22, -2.35]), r"$mg$", color=F.RED, ha="left")
    # 正向力（藍，垂直斜面向外）
    F.arrow(ax, c0, c0 + n * 1.8, color=F.BLUE)
    F.label(ax, c0 + n * 2.05, r"$N$", color=F.BLUE)
    # 摩擦（琥珀，沿斜面向上，假設下滑趨勢）
    F.arrow(ax, c0, c0 + u * 1.6, color=F.AMBER)
    pf = c0 + u * 1.85 + np.array([0.0, 0.05])
    ax.text(
        pf[0],
        pf[1],
        r"$f$",
        color=F.AMBER,
        fontsize=13,
        ha="center",
        va="center",
        bbox=_bb,
        zorder=7,
    )
    # 重力沿斜面分量（虛線灰）
    F.arrow(ax, c0, c0 - u * 1.55, color="#6b7280", ls="--")
    p1 = c0 - u * 1.85 + np.array([0.0, -0.18])
    ax.text(
        p1[0],
        p1[1],
        r"$mg\sin\theta$",
        color="#6b7280",
        fontsize=12,
        ha="center",
        va="center",
        bbox=_bb,
        zorder=7,
    )
    # 重力垂直斜面分量（虛線灰）
    F.arrow(ax, c0, c0 - n * 1.5, color="#6b7280", ls="--")
    p2 = c0 - n * 1.6 + np.array([0.70, 0.02])
    ax.text(
        p2[0],
        p2[1],
        r"$mg\cos\theta$",
        color="#6b7280",
        fontsize=12,
        ha="left",
        va="center",
        bbox=_bb,
        zorder=7,
    )
    # 角 θ
    ax.add_patch(Arc(A, 1.8, 1.8, angle=0, theta1=0, theta2=32, color=F.INK, lw=1.4))
    ax.text(A[0] + 1.22, A[1] + 0.32, r"$\theta$", color=F.INK, fontsize=14)

    ax.set_title("斜面上的自由體圖（重力分解 + 正向力 + 摩擦）", fontsize=12.5)
    ax.set_xlim(-4.1, 4.6)
    ax.set_ylim(-2.6, 3.6)
    F.save_to(fig, CH, "選物I-4-斜面自由體圖")


def fig_connected():
    """連接體：桌上物體 m1 經滑輪以繩連到懸掛物 m2。"""
    fig, ax = F.schematic(7.0, 5.0)
    # 桌面
    table_y = 0.6
    ax.add_patch(
        Rectangle(
            (-3.6, table_y - 0.45),
            4.0,
            0.45,
            facecolor="#eef1f5",
            edgecolor=F.INK,
            hatch="////",
            lw=1.2,
        )
    )
    ax.plot([-3.6, 0.4], [table_y, table_y], color=F.INK, lw=1.6)
    # 桌上物體 m1
    m1c = np.array([-1.6, table_y + 0.45])
    ax.add_patch(
        Rectangle(
            (m1c[0] - 0.55, table_y),
            1.1,
            0.9,
            facecolor="#dbe7ff",
            edgecolor=F.INK,
            lw=1.6,
            zorder=3,
        )
    )
    F.label(ax, m1c + np.array([0, 0.02]), r"$m_1$", color=F.INK, fs=14)
    # 滑輪
    pulley = np.array([0.62, table_y + 0.45])
    ax.add_patch(
        Circle(pulley, 0.28, facecolor="white", edgecolor=F.INK, lw=1.8, zorder=4)
    )
    ax.add_patch(Circle(pulley, 0.05, color=F.INK, zorder=5))
    # 繩：m1 → 滑輪（水平段）
    ax.plot(
        [m1c[0] + 0.55, pulley[0]],
        [table_y + 0.45, table_y + 0.45],
        color=F.GREEN,
        lw=2.2,
        zorder=2,
    )
    # 繩：滑輪 → m2（鉛直段）
    m2top = np.array([pulley[0] + 0.28, -1.3])
    ax.plot(
        [pulley[0] + 0.28, pulley[0] + 0.28],
        [table_y + 0.45, m2top[1]],
        color=F.GREEN,
        lw=2.2,
        zorder=2,
    )
    # 懸掛物 m2
    ax.add_patch(
        Rectangle(
            (m2top[0] - 0.5, m2top[1] - 0.95),
            1.0,
            0.95,
            facecolor="#ffe3e3",
            edgecolor=F.INK,
            lw=1.6,
            zorder=3,
        )
    )
    F.label(ax, np.array([m2top[0], m2top[1] - 0.48]), r"$m_2$", color=F.INK, fs=14)

    # m1 上的力標註：張力 T（向右）、摩擦 f（向左）
    F.arrow(ax, m1c, m1c + np.array([1.0, 0]), color=F.GREEN)
    F.label(ax, m1c + np.array([1.25, 0]), r"$T$", color=F.GREEN, ha="left")
    F.arrow(ax, m1c, m1c + np.array([-0.95, 0]), color=F.AMBER)
    F.label(ax, m1c + np.array([-1.2, 0]), r"$f$", color=F.AMBER, ha="right")
    # m2 上的力：張力 T（向上）、重力 m2 g（向下）
    m2c = np.array([m2top[0], m2top[1] - 0.48])
    F.arrow(ax, m2c, m2c + np.array([0, 1.05]), color=F.GREEN)
    F.label(ax, m2c + np.array([0.30, 0.85]), r"$T$", color=F.GREEN, ha="left")
    F.arrow(ax, m2c, m2c + np.array([0, -1.05]), color=F.RED)
    F.label(ax, m2c + np.array([0.30, -0.90]), r"$m_2g$", color=F.RED, ha="left")
    # 加速度方向提示
    F.arrow(
        ax,
        np.array([-2.7, table_y + 0.45]),
        np.array([-1.95, table_y + 0.45]),
        color=F.PURPLE,
        lw=1.8,
    )
    F.label(ax, np.array([-2.35, table_y + 0.78]), r"$a$", color=F.PURPLE, fs=12)

    ax.set_title("連接體：繩 + 滑輪（兩物體共用同一加速度與張力）", fontsize=12)
    ax.set_xlim(-4.0, 2.6)
    ax.set_ylim(-2.7, 1.9)
    F.save_to(fig, CH, "選物I-4-連接體")


def fig_contact_push():
    """接觸推擠型連接體：外力 F 推 m1、m1 推 m2；下排為 m2 的隔離自由體圖。"""
    fig, ax = F.schematic(7.4, 4.8)

    # ---- 上排：整體情境（F 推兩相貼木塊） ----
    gy = 1.05  # 上排地面高度
    ax.add_patch(
        Rectangle(
            (-3.8, gy - 0.42),
            7.6,
            0.42,
            facecolor="#eef1f5",
            edgecolor=F.INK,
            hatch="////",
            lw=1.1,
        )
    )
    ax.plot([-3.8, 3.8], [gy, gy], color=F.INK, lw=1.4)

    # m1（後塊，較大）與 m2（前塊），前後緊貼
    w1, w2, h = 1.5, 1.1, 1.1
    x1 = -1.2  # m1 左緣
    ax.add_patch(
        Rectangle(
            (x1, gy), w1, h, facecolor="#dbe7ff", edgecolor=F.INK, lw=1.6, zorder=3
        )
    )
    ax.add_patch(
        Rectangle(
            (x1 + w1, gy), w2, h, facecolor="#ffe3e3", edgecolor=F.INK, lw=1.6, zorder=3
        )
    )
    F.label(ax, np.array([x1 + w1 / 2, gy + h / 2]), r"$m_1$", color=F.INK, fs=14)
    F.label(ax, np.array([x1 + w1 + w2 / 2, gy + h / 2]), r"$m_2$", color=F.INK, fs=14)
    # 接觸面（虛線）
    ax.plot(
        [x1 + w1, x1 + w1],
        [gy + 0.05, gy + h - 0.05],
        color=F.INK,
        lw=1.0,
        ls=":",
        zorder=4,
    )

    # 外力 F（推 m1，向右）
    yF = gy + h / 2
    F.arrow(ax, np.array([x1 - 1.35, yF]), np.array([x1, yF]), color=F.PURPLE, lw=2.8)
    F.label(ax, np.array([x1 - 1.5, yF]), r"$F$", color=F.PURPLE, ha="right", fs=14)
    # 共同加速度 a
    F.arrow(
        ax,
        np.array([x1 + w1 + w2 + 0.35, gy + h + 0.32]),
        np.array([x1 + w1 + w2 + 1.15, gy + h + 0.32]),
        color=F.INK,
        lw=1.6,
    )
    F.label(
        ax, np.array([x1 + w1 + w2 + 0.75, gy + h + 0.62]), r"$a$", color=F.INK, fs=13
    )

    ax.text(
        0.0,
        gy - 0.85,
        "整體：外力 F 推動兩相貼木塊一起前進",
        ha="center",
        color=F.INK,
        fontsize=11.5,
    )

    # ---- 下排：m2 的隔離自由體圖 ----
    cy = -1.55
    cx = 1.55
    ax.add_patch(
        Rectangle(
            (cx - w2 / 2, cy - h / 2),
            w2,
            h,
            facecolor="#ffe3e3",
            edgecolor=F.INK,
            lw=1.6,
            zorder=3,
        )
    )
    F.label(ax, np.array([cx, cy]), r"$m_2$", color=F.INK, fs=14)
    ax.add_patch(Circle((cx, cy), 0.045, color=F.INK, zorder=6))
    # m1 推 m2 的接觸力（向右，唯一的水平力）
    F.arrow(ax, np.array([cx, cy]), np.array([cx + 1.6, cy]), color=F.BLUE, lw=2.8)
    F.label(
        ax, np.array([cx + 1.78, cy]), r"$F_{1\to 2}$", color=F.BLUE, ha="left", fs=13
    )
    # 共同加速度 a
    F.arrow(ax, np.array([cx - 1.6, cy]), np.array([cx - 0.9, cy]), color=F.INK, lw=1.6)
    F.label(ax, np.array([cx - 1.75, cy]), r"$a$", color=F.INK, ha="right", fs=13)

    ax.text(
        cx,
        cy - h / 2 - 0.55,
        "隔離 m2：水平只有接觸力 → F(1→2) = m2·a",
        ha="center",
        color=F.INK,
        fontsize=11.5,
    )
    ax.text(
        -3.4,
        cy + 0.05,
        "隔離法",
        ha="left",
        va="center",
        color=F.AMBER,
        fontsize=12,
        fontweight="bold",
    )

    ax.set_title("接觸推擠型連接體（整體法求 a、隔離法求接觸力）", fontsize=12.5)
    ax.set_xlim(-4.2, 4.4)
    ax.set_ylim(-2.7, 2.9)
    F.save_to(fig, CH, "選物I-4-接觸推擠連接體")


def fig_apparent_weight():
    """電梯視重：同一人在四種電梯狀態下，正向力 N 與重力 mg 的對比。"""
    fig, ax = F.schematic(8.6, 4.4)

    cases = [
        ("靜止 / 等速", "a = 0", "N = mg", 1.0, F.INK),
        ("向上加速", "a 向上", "N > mg（變重）", 1.5, F.RED),
        ("向下加速", "a 向下", "N < mg（變輕）", 0.62, F.BLUE),
        ("自由下墜", "a = g 向下", "N = 0（失重）", 0.0, F.GREEN),
    ]
    cell_w = 4.0
    base_y = -1.7  # 地板高度
    mg_len = 1.55  # 重力箭頭長度（各格相同，因 mg 不變）

    for i, (state, acc, res, nfac, ac) in enumerate(cases):
        x0 = i * cell_w
        cx = x0 + cell_w / 2
        # 電梯廂
        ax.add_patch(
            Rectangle(
                (x0 + 0.55, base_y),
                cell_w - 1.1,
                3.4,
                facecolor="white",
                edgecolor=F.INK,
                lw=1.6,
            )
        )
        # 地板（磅秤）
        ax.add_patch(
            Rectangle(
                (x0 + 0.85, base_y),
                cell_w - 1.7,
                0.28,
                facecolor="#eef1f5",
                edgecolor=F.INK,
                lw=1.2,
                hatch="////",
            )
        )
        # 人（方塊代表）
        pc = np.array([cx, base_y + 0.28 + 0.55])
        ax.add_patch(
            Rectangle(
                (pc[0] - 0.4, pc[1] - 0.55),
                0.8,
                1.1,
                facecolor="#dbe7ff",
                edgecolor=F.INK,
                lw=1.5,
                zorder=3,
            )
        )
        ax.add_patch(Circle(pc, 0.05, color=F.INK, zorder=6))
        # 重力 mg（紅，向下，長度固定）
        F.arrow(ax, pc, pc + np.array([0, -mg_len]), color=F.RED)
        F.label(
            ax, pc + np.array([0.18, -mg_len - 0.18]), r"$mg$", color=F.RED, ha="left"
        )
        # 正向力 N（藍，向上，長度隨 N 變）
        if nfac > 0.01:
            F.arrow(ax, pc, pc + np.array([0, mg_len * nfac]), color=F.BLUE)
            F.label(
                ax,
                pc + np.array([0.18, mg_len * nfac + 0.16]),
                r"$N$",
                color=F.BLUE,
                ha="left",
            )
        else:
            F.label(ax, pc + np.array([0, 0.55]), r"$N=0$", color=F.GREEN, fs=11)
        # 加速度方向標示（廂外右側）
        if acc != "a = 0":
            ay0 = base_y + 1.5
            adir = 1 if "向上" in acc else -1
            F.arrow(
                ax,
                np.array([x0 + cell_w - 0.30, ay0]),
                np.array([x0 + cell_w - 0.30, ay0 + 0.85 * adir]),
                color=F.PURPLE,
                lw=2.0,
            )
            F.label(
                ax,
                np.array([x0 + cell_w - 0.30, ay0 + 1.05 * adir]),
                r"$a$",
                color=F.PURPLE,
                fs=12,
            )
        # 標題與結論文字
        ax.text(cx, base_y + 3.62, state, ha="center", color=F.INK, fontsize=11.5)
        ax.text(cx, base_y - 0.30, res, ha="center", color=ac, fontsize=10.5)

    ax.set_title(
        "電梯中的視重：重力 mg 不變，磅秤讀數（正向力 N）隨加速度改變", fontsize=12.5
    )
    ax.set_xlim(-0.2, 4 * cell_w + 0.2)
    ax.set_ylim(base_y - 0.75, base_y + 4.0)
    F.save_to(fig, CH, "選物I-4-電梯視重")


def fig_atwood():
    """阿特午德機：理想滑輪兩側懸掛 m1、m2，各畫自由體圖。"""
    fig, ax = F.schematic(6.4, 5.4)

    # 天花板與支架
    ax.add_patch(
        Rectangle(
            (-2.4, 3.0),
            4.8,
            0.3,
            facecolor="#eef1f5",
            edgecolor=F.INK,
            hatch="////",
            lw=1.2,
        )
    )
    ax.plot([-2.4, 2.4], [3.0, 3.0], color=F.INK, lw=1.5)
    # 滑輪
    pulley = np.array([0.0, 2.55])
    ax.plot([0, 0], [3.0, pulley[1] + 0.35], color=F.INK, lw=1.5)
    ax.add_patch(
        Circle(pulley, 0.35, facecolor="white", edgecolor=F.INK, lw=1.8, zorder=4)
    )
    ax.add_patch(Circle(pulley, 0.06, color=F.INK, zorder=5))

    xL, xR = -0.35, 0.35
    # 繩
    ax.plot([xL, xL], [pulley[1], 0.7], color=F.GREEN, lw=2.2, zorder=2)
    ax.plot([xR, xR], [pulley[1], 1.5], color=F.GREEN, lw=2.2, zorder=2)
    # 繩跨過滑輪頂端
    th = np.linspace(np.pi, 0, 40)
    ax.plot(
        pulley[0] + 0.35 * np.cos(th),
        pulley[1] + 0.35 * np.sin(th),
        color=F.GREEN,
        lw=2.2,
        zorder=3,
    )

    # m1（左，較重，較低）
    m1c = np.array([xL, 0.7 - 0.5])
    ax.add_patch(
        Rectangle(
            (m1c[0] - 0.5, m1c[1] - 0.5),
            1.0,
            1.0,
            facecolor="#dbe7ff",
            edgecolor=F.INK,
            lw=1.6,
            zorder=3,
        )
    )
    F.label(ax, m1c, r"$m_1$", color=F.INK, fs=14)
    # m2（右，較輕，較高）
    m2c = np.array([xR, 1.5 - 0.45])
    ax.add_patch(
        Rectangle(
            (m2c[0] - 0.45, m2c[1] - 0.45),
            0.9,
            0.9,
            facecolor="#ffe3e3",
            edgecolor=F.INK,
            lw=1.6,
            zorder=3,
        )
    )
    F.label(ax, m2c, r"$m_2$", color=F.INK, fs=14)

    # m1 的力：張力向上、重力向下
    F.arrow(ax, m1c, m1c + np.array([0, 1.0]), color=F.GREEN)
    F.label(ax, m1c + np.array([-0.22, 0.85]), r"$T$", color=F.GREEN, ha="right")
    F.arrow(ax, m1c, m1c + np.array([0, -1.25]), color=F.RED)
    F.label(ax, m1c + np.array([-0.22, -1.1]), r"$m_1g$", color=F.RED, ha="right")
    # m2 的力
    F.arrow(ax, m2c, m2c + np.array([0, 1.0]), color=F.GREEN)
    F.label(ax, m2c + np.array([0.22, 0.85]), r"$T$", color=F.GREEN, ha="left")
    F.arrow(ax, m2c, m2c + np.array([0, -1.05]), color=F.RED)
    F.label(ax, m2c + np.array([0.22, -0.9]), r"$m_2g$", color=F.RED, ha="left")
    # 加速度方向（m1 下、m2 上）
    F.arrow(ax, np.array([-1.45, 0.6]), np.array([-1.45, -0.1]), color=F.PURPLE, lw=2.0)
    F.label(ax, np.array([-1.7, 0.25]), r"$a$", color=F.PURPLE, fs=12)
    F.arrow(ax, np.array([1.45, 0.7]), np.array([1.45, 1.4]), color=F.PURPLE, lw=2.0)
    F.label(ax, np.array([1.7, 1.05]), r"$a$", color=F.PURPLE, fs=12)

    ax.text(
        0.0,
        -1.55,
        "重者下降、輕者上升，共用同一加速度 a 與張力 T",
        ha="center",
        color=F.INK,
        fontsize=11,
    )
    ax.set_title("阿特午德機（理想滑輪兩側懸掛兩物體）", fontsize=12.5)
    ax.set_xlim(-2.6, 2.6)
    ax.set_ylim(-1.9, 3.6)
    F.save_to(fig, CH, "選物I-4-阿特午德機")


def fig_action_reaction():
    """作用與反作用：兩物體互推，力作用在不同物體上。"""
    fig, ax = F.schematic(7.0, 4.0)
    # 物體 A
    A = Rectangle(
        (-2.7, -0.7), 1.4, 1.4, facecolor="#dbe7ff", edgecolor=F.INK, lw=1.8, zorder=3
    )
    ax.add_patch(A)
    F.label(ax, np.array([-2.0, 0]), "A", color=F.INK, fs=16)
    # 物體 B
    Bp = Rectangle(
        (1.3, -0.7), 1.4, 1.4, facecolor="#ffe3e3", edgecolor=F.INK, lw=1.8, zorder=3
    )
    ax.add_patch(Bp)
    F.label(ax, np.array([2.0, 0]), "B", color=F.INK, fs=16)
    # 接觸面
    ax.plot([0.0, 0.0], [-0.95, 0.95], color=F.INK, lw=1.0, ls=":")

    # A 對 B 的力（作用在 B，向右）
    F.arrow(ax, np.array([0.05, 0.32]), np.array([1.25, 0.32]), color=F.BLUE, lw=2.8)
    F.label(ax, np.array([0.65, 0.72]), r"$\vec F_{A\to B}$", color=F.BLUE, fs=12)
    # B 對 A 的力（作用在 A，向左）
    F.arrow(ax, np.array([-0.05, -0.32]), np.array([-1.25, -0.32]), color=F.RED, lw=2.8)
    F.label(ax, np.array([-0.65, -0.74]), r"$\vec F_{B\to A}$", color=F.RED, fs=12)

    ax.text(
        0.0,
        -1.75,
        "大小相等、方向相反，但作用在不同物體上 ⇒ 不會抵消",
        ha="center",
        color=F.INK,
        fontsize=12,
        fontweight="bold",
    )
    ax.set_title("作用力與反作用力（牛頓第三定律）", fontsize=14)
    ax.set_xlim(-3.6, 3.6)
    ax.set_ylim(-2.2, 1.6)
    F.save_to(fig, CH, "選物I-4-作用反作用")


if __name__ == "__main__":
    fig_vector_add()
    fig_decompose()
    fig_incline_fbd()
    fig_connected()
    fig_contact_push()
    fig_apparent_weight()
    fig_atwood()
    fig_action_reaction()
    print("done.")
