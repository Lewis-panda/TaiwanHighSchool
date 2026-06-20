# -*- coding: utf-8 -*-
"""產生「必物-2 物體的運動」的圖，輸出到該章 sources/。
重繪：  .venv/bin/python _tools/fig_必物-2.py
"""

import os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon, Arc, Circle, Ellipse
import figlib as F

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CH = os.path.join(ROOT, "物理", "物理一（必修物理）", "必物-2 物體的運動")


def fig_motion_graphs():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.2, 3.8))
    t = np.linspace(0, 5, 100)

    # x–t 圖
    x = 1.2 * t
    ax1.plot(t, x, color=F.BLUE, lw=2.6)
    ax1.plot([2, 4, 4], [2.4, 2.4, 4.8], color=F.INK, lw=1.2, ls="--")
    ax1.text(3, 2.0, r"$\Delta t$", ha="center", color=F.INK)
    ax1.text(4.18, 3.6, r"$\Delta x$", va="center", color=F.INK)
    ax1.text(1.5, 4.4, "斜率 = 速度", color=F.BLUE, fontsize=12)
    ax1.set_title("位置–時間圖（x–t）")
    ax1.set_xlabel("時間 $t$ (s)")
    ax1.set_ylabel("位置 $x$ (m)")
    ax1.set_xlim(0, 5)
    ax1.set_ylim(0, 6)
    F.clean_grid(ax1)

    # v–t 圖
    v = 2 + 1.2 * t
    ax2.plot(t, v, color=F.RED, lw=2.6)
    ax2.fill_between(t, 0, v, color=F.FILL, alpha=0.12)
    ax2.text(2.5, 3.0, "面積 = 位移", ha="center", color=F.BLUE, fontsize=12)
    ax2.text(1.2, 6.6, "斜率 = 加速度", color=F.RED, fontsize=12)
    ax2.set_title("速度–時間圖（v–t）")
    ax2.set_xlabel("時間 $t$ (s)")
    ax2.set_ylabel("速度 $v$ (m/s)")
    ax2.set_xlim(0, 5)
    ax2.set_ylim(0, 9)
    F.clean_grid(ax2)

    fig.tight_layout()
    F.save_to(fig, CH, "必物-2-運動圖形")


def fig_free_body():
    fig, ax = F.schematic(5.2, 5.2)
    # 接觸面
    ax.add_patch(
        Rectangle(
            (-2.6, -2.2),
            5.2,
            0.5,
            facecolor="#eef1f5",
            edgecolor=F.INK,
            hatch="////",
            lw=1.2,
        )
    )
    ax.plot([-2.6, 2.6], [-1.7, -1.7], color=F.INK, lw=1.6)
    # 物體
    ax.add_patch(
        Rectangle(
            (-0.7, -1.7),
            1.4,
            1.4,
            facecolor="#dbe7ff",
            edgecolor=F.INK,
            lw=1.6,
            zorder=3,
        )
    )
    c = (0.0, -1.0)  # 物體中心（力的作用點）
    ax.add_patch(Circle(c, 0.05, color=F.INK, zorder=6))
    # 四個力
    F.arrow(ax, c, (c[0], c[1] + 2.0), color=F.BLUE)
    F.label(ax, (0.0, 1.25), "$N$ 正向力", color=F.BLUE)
    F.arrow(ax, c, (c[0], c[1] - 1.6), color=F.RED)
    F.label(ax, (0.0, -2.95), "$mg$ 重力", color=F.RED)
    F.arrow(ax, c, (c[0] + 2.1, c[1]), color=F.GREEN)
    F.label(ax, (2.55, -1.0), "$T$ 張力", color=F.GREEN, ha="left")
    F.arrow(ax, c, (c[0] - 1.9, c[1]), color=F.AMBER)
    F.label(ax, (-2.35, -1.0), "$f$ 摩擦力", color=F.AMBER, ha="right")
    ax.set_title("自由體圖（free-body diagram）", fontsize=14)
    ax.set_xlim(-3.4, 3.4)
    ax.set_ylim(-3.3, 2.0)
    F.save_to(fig, CH, "必物-2-自由體圖")


def fig_incline():
    fig, ax = F.schematic(6.2, 5.0)
    th = np.deg2rad(30)
    A = np.array([-3.2, -1.6])  # 斜角 θ 所在頂點
    B = np.array([3.2, -1.6])  # 直角
    C = np.array([3.2, -1.6 + 6.4 * np.tan(th)])
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
    M = (A + C) / 2  # 斜面中點
    c0 = M + n * 0.45  # 物體中心
    # 物體（沿斜面方向的方塊）
    s, tk = 0.95, 0.62
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
    # 力
    F.arrow(ax, c0, c0 + np.array([0, -2.0]), color=F.RED)
    F.label(ax, c0 + np.array([0.18, -2.25]), "$mg$", color=F.RED, ha="left")
    F.arrow(ax, c0, c0 + n * 1.7, color=F.BLUE)
    F.label(ax, c0 + n * 1.95, "$N$", color=F.BLUE)
    _bb = dict(boxstyle="round,pad=0.12", fc="white", ec="none", alpha=0.9)
    F.arrow(ax, c0, c0 - u * 1.5, color=F.AMBER, ls="--")
    p1 = c0 - u * 1.78 + np.array([0, -0.20])
    ax.text(
        p1[0],
        p1[1],
        r"$mg\sin\theta$",
        color=F.AMBER,
        fontsize=13,
        ha="center",
        va="center",
        bbox=_bb,
        zorder=7,
    )
    F.arrow(ax, c0, c0 - n * 1.45, color="#6b7280", ls="--")
    p2 = c0 - n * 1.55 + np.array([0.62, 0.05])
    ax.text(
        p2[0],
        p2[1],
        r"$mg\cos\theta$",
        color="#6b7280",
        fontsize=13,
        ha="left",
        va="center",
        bbox=_bb,
        zorder=7,
    )
    # 角 θ
    ax.add_patch(Arc(A, 1.8, 1.8, angle=0, theta1=0, theta2=30, color=F.INK, lw=1.4))
    ax.text(A[0] + 1.25, A[1] + 0.30, r"$\theta$", color=F.INK, fontsize=14)
    ax.set_title("斜面上的重力分解（臨界角 $\\tan\\theta_c=\\mu_s$）", fontsize=13)
    ax.set_xlim(-4.0, 4.4)
    ax.set_ylim(-2.4, 3.4)
    F.save_to(fig, CH, "必物-2-斜面分解")


def fig_kepler():
    fig, ax = F.schematic(6.6, 4.6)
    a, b = 3.2, 2.3
    c = np.sqrt(a**2 - b**2)
    th = np.linspace(0, 2 * np.pi, 400)
    ax.plot(a * np.cos(th), b * np.sin(th), color=F.INK, lw=2.0)
    S = np.array([c, 0.0])  # 太陽（焦點）
    ax.add_patch(Circle(S, 0.22, color="#f0a202", zorder=5))
    ax.add_patch(Circle(S, 0.22, fill=False, color="#9a6700", lw=1.2, zorder=6))
    F.label(ax, S + np.array([0, -0.55]), "太陽", color="#9a6700", fs=12)

    def sweep(t1, t2, color):
        ts = np.linspace(t1, t2, 30)
        pts = [S] + [np.array([a * np.cos(t), b * np.sin(t)]) for t in ts]
        ax.add_patch(
            Polygon(
                pts,
                closed=True,
                facecolor=color,
                alpha=0.30,
                edgecolor=color,
                lw=1.0,
                zorder=2,
            )
        )

    # 近日點（右側，角速度大→角寬）；遠日點（左側，角寬小）→ 兩塊面積相等
    sweep(np.deg2rad(-30), np.deg2rad(30), F.RED)
    sweep(np.deg2rad(166), np.deg2rad(194), F.BLUE)
    # 行星與半徑線
    for t, lab, col in [
        (np.deg2rad(0), "近日點\n（較快）", F.RED),
        (np.deg2rad(180), "遠日點\n（較慢）", F.BLUE),
    ]:
        P = np.array([a * np.cos(t), b * np.sin(t)])
        ax.add_patch(Circle(P, 0.13, color=col, zorder=6))
        ax.text(
            P[0] + (0.4 if t == 0 else -0.4),
            P[1] + 0.55,
            lab,
            color=col,
            ha="left" if t == 0 else "right",
            va="bottom",
            fontsize=11,
        )
    ax.text(
        0,
        -2.75,
        "相等時間內，行星與太陽連線掃過的面積相等（等面積定律）",
        ha="center",
        color=F.INK,
        fontsize=12,
    )
    ax.set_title("克卜勒第一、第二定律", fontsize=14)
    ax.set_xlim(-4.2, 4.2)
    ax.set_ylim(-3.2, 3.0)
    F.save_to(fig, CH, "必物-2-克卜勒等面積")


def fig_circular_orbit():
    """圓軌道：萬有引力提供向心力，速度沿切線。"""
    fig, ax = F.schematic(5.4, 5.0)
    R = 2.3
    Sun = np.array([0.0, 0.0])
    th = np.linspace(0, 2 * np.pi, 400)
    # 軌道圓
    ax.plot(R * np.cos(th), R * np.sin(th), color=F.INK, lw=1.8, ls="--", zorder=1)
    # 太陽（中心）
    ax.add_patch(Circle(Sun, 0.28, color="#f0a202", zorder=5))
    ax.add_patch(Circle(Sun, 0.28, fill=False, color="#9a6700", lw=1.2, zorder=6))
    F.label(ax, Sun + np.array([0, -0.62]), "太陽 $M$", color="#9a6700", fs=12)
    # 行星位置（右上）
    a0 = np.deg2rad(40)
    P = R * np.array([np.cos(a0), np.sin(a0)])
    ax.add_patch(Circle(P, 0.18, color=F.BLUE, zorder=6))
    F.label(ax, P + np.array([0.42, 0.22]), "行星 $m$", color=F.BLUE, fs=12, ha="left")
    # 半徑線 r
    ax.plot([Sun[0], P[0]], [Sun[1], P[1]], color="#6b7280", lw=1.2, ls=":", zorder=2)
    F.label(ax, 0.5 * P + np.array([-0.28, 0.30]), "$r$", color="#6b7280", fs=13)
    # 向心力（沿半徑指向太陽）
    rhat = -P / np.linalg.norm(P)
    F.arrow(ax, P, P + rhat * 1.25, color=F.RED, z=7)
    F.label(
        ax,
        P + rhat * 1.25 + np.array([0.34, -0.42]),
        r"$F=\frac{GMm}{r^2}$",
        color=F.RED,
        fs=13,
        ha="left",
    )
    # 速度（沿切線方向，逆時針）
    that = np.array([-np.sin(a0), np.cos(a0)])
    F.arrow(ax, P, P + that * 1.35, color=F.GREEN, z=7)
    F.label(
        ax,
        P + that * 1.35 + np.array([0.05, 0.30]),
        "$v$（切線方向）",
        color=F.GREEN,
        fs=12,
        ha="center",
    )
    ax.set_title("圓軌道：萬有引力扮演向心力", fontsize=14)
    ax.set_xlim(-3.0, 4.3)
    ax.set_ylim(-3.0, 3.6)
    F.save_to(fig, CH, "必物-2-圓軌道向心力")


if __name__ == "__main__":
    fig_motion_graphs()
    fig_free_body()
    fig_incline()
    fig_kepler()
    fig_circular_orbit()
    print("done.")
