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
    fig_action_reaction()
    print("done.")
