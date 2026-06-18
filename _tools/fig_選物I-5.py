# -*- coding: utf-8 -*-
"""產生「選物I-5 週期運動」的圖，輸出到該章 sources/。
重繪：  .venv/bin/python _tools/fig_選物I-5.py
"""

import os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon, Arc, Circle, FancyArrowPatch
import figlib as F

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CH = os.path.join(ROOT, "物理", "物理二上（選修物理I·力學一）", "選物I-5 週期運動")


def fig_centripetal():
    """等速圓周：速度沿切線、Δv 指向圓心 → 向心加速度。"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.6, 4.6))

    # 左圖：圓周上兩點的速度向量（沿切線）
    R = 1.0
    th = np.linspace(0, 2 * np.pi, 400)
    ax1.plot(R * np.cos(th), R * np.sin(th), color=F.INK, lw=2.0)
    ax1.add_patch(Circle((0, 0), 0.045, color=F.INK, zorder=6))
    a1, a2 = np.deg2rad(55), np.deg2rad(110)
    for a, name in [(a1, "$\\vec v_1$"), (a2, "$\\vec v_2$")]:
        P = np.array([R * np.cos(a), R * np.sin(a)])
        # 切線方向（逆時針運動）= (-sin, cos)
        tdir = np.array([-np.sin(a), np.cos(a)])
        ax1.add_patch(Circle(P, 0.06, color=F.BLUE, zorder=6))
        F.arrow(ax1, P, P + 0.85 * tdir, color=F.BLUE)
        ax1.text(
            *(P + 0.85 * tdir + 0.18 * tdir + np.array([0.05, 0.05])),
            name,
            color=F.BLUE,
            fontsize=13,
            ha="center",
        )
    # 半徑線
    for a in (a1, a2):
        P = np.array([R * np.cos(a), R * np.sin(a)])
        ax1.plot([0, P[0]], [0, P[1]], color="#9aa0a6", lw=1.1, ls="--")
    ax1.text(0.18, -0.05, "$r$", color="#6b7280", fontsize=12)
    ax1.text(
        0,
        -1.42,
        "速率不變（$|\\vec v_1|=|\\vec v_2|$），\n但方向一直在轉",
        ha="center",
        color=F.INK,
        fontsize=11,
    )
    ax1.set_aspect("equal")
    ax1.axis("off")
    ax1.set_xlim(-1.5, 1.5)
    ax1.set_ylim(-1.8, 1.5)
    ax1.set_title("速度沿切線方向", fontsize=13)

    # 右圖：速度向量三角形 v1 + Δv = v2，Δv 指向圓心
    v = 1.2
    a1v = np.array([-np.sin(a1), np.cos(a1)]) * v
    a2v = np.array([-np.sin(a2), np.cos(a2)]) * v
    O = np.array([-0.2, -0.4])
    F.arrow(ax2, O, O + a1v, color=F.BLUE)
    F.arrow(ax2, O, O + a2v, color=F.BLUE)
    F.arrow(ax2, O + a1v, O + a2v, color=F.RED)
    ax2.text(
        *(O + a1v * 0.55 + np.array([0.12, -0.05])),
        "$\\vec v_1$",
        color=F.BLUE,
        fontsize=13,
    )
    ax2.text(
        *(O + a2v * 0.55 + np.array([-0.28, 0.02])),
        "$\\vec v_2$",
        color=F.BLUE,
        fontsize=13,
    )
    mid = O + (a1v + a2v) / 2 + np.array([0.0, 0.18])
    ax2.text(mid[0] + 0.20, mid[1] + 0.18, "$\\Delta\\vec v$", color=F.RED, fontsize=14)
    ax2.text(
        O[0] + 0.05,
        O[1] - 0.45,
        "$\\Delta\\vec v=\\vec v_2-\\vec v_1$ 指向圓心\n→ 加速度指向圓心（向心）",
        ha="center",
        color=F.RED,
        fontsize=11,
    )
    ax2.set_aspect("equal")
    ax2.axis("off")
    ax2.set_xlim(-1.7, 1.4)
    ax2.set_ylim(-1.5, 1.6)
    ax2.set_title("速度的變化 $\\Delta\\vec v$ 指向圓心", fontsize=13)

    fig.suptitle("等速圓周運動：速率不變、方向變 → 有向心加速度", fontsize=14)
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    F.save_to(fig, CH, "選物I-5-向心加速度")


def fig_shm_projection():
    """等速圓周運動投影成簡諧；右側對應的 x–t 餘弦曲線。"""
    fig, (ax1, ax2) = plt.subplots(
        1, 2, figsize=(10.2, 4.4), gridspec_kw={"width_ratios": [1, 1.4]}
    )

    # 左：圓 + 投影到 x 軸
    R = 1.0
    th = np.linspace(0, 2 * np.pi, 400)
    ax1.plot(R * np.cos(th), R * np.sin(th), color="#9aa0a6", lw=1.6)
    phi = np.deg2rad(50)
    P = np.array([R * np.cos(phi), R * np.sin(phi)])
    Px = np.array([R * np.cos(phi), 0.0])
    ax1.add_patch(Circle((0, 0), 0.04, color=F.INK, zorder=6))
    ax1.plot([0, P[0]], [0, P[1]], color=F.PURPLE, lw=2.0)  # 半徑
    ax1.add_patch(Circle(P, 0.07, color=F.PURPLE, zorder=6))  # 圓周上的點
    ax1.plot([P[0], P[0]], [P[1], 0], color=F.INK, lw=1.0, ls=":")  # 投影虛線
    ax1.add_patch(Circle(Px, 0.07, color=F.BLUE, zorder=6))  # 投影點（SHM）
    # 角度弧
    ax1.add_patch(
        Arc((0, 0), 0.7, 0.7, angle=0, theta1=0, theta2=50, color=F.INK, lw=1.2)
    )
    ax1.text(0.45, 0.16, "$\\omega t$", color=F.INK, fontsize=12)
    ax1.axhline(0, color=F.INK, lw=1.2)
    ax1.text(
        P[0] + 0.05, P[1] + 0.12, "圓周運動", color=F.PURPLE, fontsize=11, ha="left"
    )
    ax1.text(
        Px[0], -0.25, "$x=A\\cos\\omega t$", color=F.BLUE, fontsize=12, ha="center"
    )
    ax1.text(1.18, 0.0, "$A$", color="#6b7280", fontsize=12, va="center")
    ax1.set_aspect("equal")
    ax1.axis("off")
    ax1.set_xlim(-1.4, 1.5)
    ax1.set_ylim(-1.4, 1.4)
    ax1.set_title("簡諧 = 圓周在直徑上的投影", fontsize=13)

    # 右：x–t 餘弦曲線，標出對應時刻
    t = np.linspace(0, 2.0, 500)
    x = np.cos(2 * np.pi * t)
    ax2.plot(t, x, color=F.BLUE, lw=2.6)
    ax2.axhline(0, color=F.INK, lw=1.0)
    t0 = phi / (2 * np.pi)
    ax2.plot([t0], [np.cos(2 * np.pi * t0)], "o", color=F.PURPLE, ms=8, zorder=6)
    ax2.plot([t0, t0], [0, np.cos(2 * np.pi * t0)], color=F.INK, lw=1.0, ls=":")
    ax2.axhline(1, color="#9aa0a6", lw=0.8, ls="--")
    ax2.axhline(-1, color="#9aa0a6", lw=0.8, ls="--")
    ax2.text(0.02, 1.05, "$+A$", color="#6b7280", fontsize=11)
    ax2.text(0.02, -1.18, "$-A$", color="#6b7280", fontsize=11)
    ax2.annotate(
        "一個週期 $T$",
        xy=(0, -1.35),
        xytext=(1.0, -1.35),
        color=F.INK,
        fontsize=11,
        ha="center",
        va="center",
        arrowprops=dict(arrowstyle="<->", color=F.INK),
    )
    ax2.plot([0, 1.0], [-1.35, -1.35], color="none")
    ax2.set_xlim(0, 2.0)
    ax2.set_ylim(-1.6, 1.4)
    ax2.set_xlabel("時間 $t$")
    ax2.set_ylabel("位置 $x$")
    ax2.set_xticks([0, 0.5, 1.0, 1.5, 2.0])
    ax2.set_xticklabels(["0", "$T/2$", "$T$", "$3T/2$", "$2T$"])
    ax2.set_yticks([])
    ax2.set_title("位置–時間圖：正弦／餘弦曲線", fontsize=13)
    F.clean_grid(ax2)

    fig.tight_layout()
    F.save_to(fig, CH, "選物I-5-簡諧投影")


def fig_spring():
    """彈簧簡諧：三個位置的回復力，下方對應 x–t 曲線。"""
    fig, (ax1, ax2) = plt.subplots(
        2, 1, figsize=(7.6, 6.2), gridspec_kw={"height_ratios": [1, 1]}
    )

    def spring(ax, x0, y0, x1, n=10, amp=0.12):
        xs = np.linspace(x0, x1, 2 * n + 1)
        ys = np.full_like(xs, y0)
        ys[1:-1:2] += amp
        ys[2:-1:2] -= amp
        ax.plot(xs, ys, color="#6b7280", lw=1.6)

    wall = -2.6
    for y0, xb, lab, col, force in [
        (1.6, -0.6, "壓縮：$x<0$", F.RED, "向右（回正）"),
        (0.0, 0.6, "平衡：$x=0$", F.INK, "無回復力"),
        (-1.6, 1.6, "拉伸：$x>0$", F.BLUE, "向左（回正）"),
    ]:
        ax1.add_patch(
            Rectangle(
                (wall - 0.15, y0 - 0.45),
                0.15,
                0.9,
                facecolor="#cfd4da",
                edgecolor=F.INK,
                lw=1.2,
            )
        )
        spring(ax1, wall, y0, xb)
        ax1.add_patch(
            Rectangle(
                (xb, y0 - 0.32),
                0.62,
                0.64,
                facecolor="#dbe7ff",
                edgecolor=F.INK,
                lw=1.4,
                zorder=3,
            )
        )
        ax1.plot([0.31, 0.31], [y0 - 0.55, y0 + 0.55], color="#9aa0a6", lw=0.9, ls=":")
        # 回復力箭頭
        if xb < 0:
            F.arrow(ax1, (xb + 0.31, y0), (xb + 0.31 + 0.7, y0), color=col)
        elif xb > 0:
            F.arrow(ax1, (xb + 0.31, y0), (xb + 0.31 - 0.7, y0), color=col)
        ax1.text(2.9, y0, lab, color="#444", fontsize=11, va="center", ha="left")
        if xb != 0:
            ax1.text(
                (xb + 0.31), y0 + 0.55, "$F=-kx$", color=col, fontsize=11, ha="center"
            )
    ax1.axvline(0.31, color="#9aa0a6", lw=0.9, ls=":")
    ax1.text(0.31, 2.35, "平衡位置", color="#6b7280", fontsize=10, ha="center")
    ax1.set_xlim(wall - 0.4, 4.5)
    ax1.set_ylim(-2.3, 2.6)
    ax1.set_aspect("equal")
    ax1.axis("off")
    ax1.set_title("水平彈簧：回復力 $F=-kx$ 永遠指回平衡位置", fontsize=13)

    # x–t
    t = np.linspace(0, 2.0, 500)
    x = np.cos(2 * np.pi * t)
    ax2.plot(t, x, color=F.GREEN, lw=2.6)
    ax2.axhline(0, color=F.INK, lw=1.0)
    ax2.set_xlim(0, 2.0)
    ax2.set_ylim(-1.4, 1.4)
    ax2.set_xticks([0, 0.5, 1.0, 1.5, 2.0])
    ax2.set_xticklabels(["0", "$T/2$", "$T$", "$3T/2$", "$2T$"])
    ax2.set_yticks([-1, 0, 1])
    ax2.set_yticklabels(["$-A$", "0", "$+A$"])
    ax2.set_xlabel("時間 $t$")
    ax2.set_ylabel("位置 $x$")
    ax2.set_title(
        "位移隨時間：$x=A\\cos\\omega t$，週期 $T=2\\pi\\sqrt{m/k}$", fontsize=12
    )
    F.clean_grid(ax2)

    fig.tight_layout()
    F.save_to(fig, CH, "選物I-5-彈簧簡諧")


def fig_pendulum():
    """單擺受力分解：重力沿擺線與切線分量，切線分量為回復力。"""
    fig, ax = F.schematic(6.4, 6.0)
    piv = np.array([0.0, 2.4])
    Lpx = 3.6
    ang = np.deg2rad(28)  # 擺角（畫面上往右偏）
    bob = piv + Lpx * np.array([np.sin(ang), -np.cos(ang)])

    # 天花板
    ax.add_patch(
        Rectangle(
            (-1.4, 2.4),
            2.8,
            0.22,
            facecolor="#cfd4da",
            edgecolor=F.INK,
            lw=1.2,
            hatch="////",
        )
    )
    # 擺線
    ax.plot([piv[0], bob[0]], [piv[1], bob[1]], color=F.INK, lw=1.8)
    # 鉛直參考線
    ax.plot(
        [piv[0], piv[0]], [piv[1], piv[1] - Lpx - 0.2], color="#9aa0a6", lw=1.0, ls="--"
    )
    # 擺角弧
    ax.add_patch(
        Arc(
            piv,
            1.6,
            1.6,
            angle=0,
            theta1=-90,
            theta2=-90 + np.rad2deg(ang),
            color=F.INK,
            lw=1.3,
        )
    )
    ax.text(piv[0] + 0.30, piv[1] - 1.0, r"$\theta$", color=F.INK, fontsize=14)
    # 擺錘
    ax.add_patch(
        Circle(bob, 0.30, facecolor="#dbe7ff", edgecolor=F.INK, lw=1.6, zorder=5)
    )

    # 方向：沿擺線向外（從支點指向擺錘）、切線（回復方向）
    radial = np.array([np.sin(ang), -np.cos(ang)])
    tang = np.array([np.cos(ang), np.sin(ang)])  # 與半徑垂直
    g = np.array([0.0, -1.0]) * 2.0  # 重力向量（畫長一點）
    mg_comp_along = np.dot(g, radial) * radial  # 沿擺線分量
    mg_comp_tan = np.dot(g, tang) * tang  # 切線分量（回復力，指向平衡）

    # 重力
    F.arrow(ax, bob, bob + g, color=F.RED)
    ax.text(*(bob + g + np.array([0.18, -0.12])), "$mg$", color=F.RED, fontsize=13)
    # 沿擺線分量（被張力抵消）
    F.arrow(ax, bob, bob + mg_comp_along, color="#6b7280", ls="--")
    ax.text(
        *(bob + mg_comp_along + np.array([0.30, -0.18])),
        "$mg\\cos\\theta$",
        color="#6b7280",
        fontsize=11,
    )
    # 切線回復分量
    F.arrow(ax, bob, bob + mg_comp_tan, color=F.BLUE)
    ax.text(
        *(bob + mg_comp_tan + np.array([-0.30, 0.28])),
        "$mg\\sin\\theta$",
        color=F.BLUE,
        fontsize=12,
        ha="center",
    )
    # 張力
    F.arrow(ax, bob, bob - radial * 1.6, color=F.GREEN)
    ax.text(
        *(bob - radial * 1.6 + np.array([-0.35, 0.05])),
        "$T$",
        color=F.GREEN,
        fontsize=13,
    )

    ax.text(
        0.0,
        -2.0,
        "切線方向回復力 $\\approx mg\\sin\\theta$；小角度時 $\\sin\\theta\\approx\\theta$\n"
        "→ 回復力正比於位移 → 簡諧，$T=2\\pi\\sqrt{L/g}$",
        ha="center",
        color=F.INK,
        fontsize=11,
    )
    ax.set_xlim(-3.0, 3.6)
    ax.set_ylim(-2.6, 3.0)
    ax.set_title("單擺：重力的切線分量提供回復力", fontsize=14)
    F.save_to(fig, CH, "選物I-5-單擺")


def fig_energy():
    """簡諧能量：U=½kx² 上凹、K=½k(A²−x²) 下凹，總和 E 為水平線。"""
    fig, ax = F.canvas(7.4, 4.8)

    A = 1.0
    k = 1.0  # 取 k=1，縱軸用 ½kA² 當單位即可
    E = 0.5 * k * A**2
    x = np.linspace(-A, A, 400)
    U = 0.5 * k * x**2
    K = 0.5 * k * (A**2 - x**2)

    # 位能 U（上凹）、動能 K（下凹）、總能 E（水平線）
    ax.plot(x, U, color=F.RED, lw=2.6, label="位能 U = ½kx²")
    ax.plot(x, K, color=F.BLUE, lw=2.6, label="動能 K = ½k(A²−x²)")
    ax.axhline(E, color=F.GREEN, lw=2.2, ls="--", label="總力學能 E = ½kA²（定值）")

    # 平衡點與兩端點的標示線
    for xv in (-A, 0.0, A):
        ax.axvline(xv, color="#c2c7cd", lw=0.9, ls=":")

    # 交點：U=K 時 x=±A/√2，能量各半
    xc = A / np.sqrt(2)
    for xv in (-xc, xc):
        ax.plot([xv], [0.5 * E], "o", color=F.INK, ms=5, zorder=6)

    # 端點：全位能（右上）；平衡點：全動能（左上）。中文不放 $...$
    ax.annotate(
        "端點 x=±A：\n速度為零\n全為位能 U=E",
        xy=(A, E),
        xytext=(A * 0.62, E * 1.62),
        color=F.RED,
        fontsize=10,
        ha="center",
        va="center",
        arrowprops=dict(arrowstyle="->", color=F.RED, lw=1.2),
    )
    ax.annotate(
        "平衡點 x=0：\n速率最大\n全為動能 K=E",
        xy=(0, E),
        xytext=(-A * 0.60, E * 1.62),
        color=F.BLUE,
        fontsize=10,
        ha="center",
        va="center",
        arrowprops=dict(arrowstyle="->", color=F.BLUE, lw=1.2),
    )
    ax.annotate(
        "U=K，能量各半",
        xy=(xc, 0.5 * E),
        xytext=(xc + 0.05, 0.5 * E - 0.16),
        color=F.INK,
        fontsize=9.5,
        ha="left",
        va="top",
        arrowprops=dict(arrowstyle="->", color=F.INK, lw=1.0),
    )

    ax.set_xlim(-A * 1.18, A * 1.18)
    ax.set_ylim(0, E * 2.0)
    ax.set_xlabel("位置 $x$")
    ax.set_ylabel("能量")
    ax.set_xticks([-A, -xc, 0, xc, A])
    ax.set_xticklabels(["$-A$", "$-A/\\sqrt{2}$", "$0$", "$A/\\sqrt{2}$", "$+A$"])
    ax.set_yticks([0, 0.5 * E, E])
    ax.set_yticklabels(["$0$", "$E/2$", "$E=\\frac{1}{2}kA^2$"])
    ax.legend(
        loc="upper center",
        fontsize=9.5,
        frameon=False,
        ncol=3,
        bbox_to_anchor=(0.5, 1.0),
    )
    ax.set_title("簡諧運動的能量：動能與位能此消彼長，總和守恆", fontsize=13, pad=10)
    F.clean_grid(ax)

    fig.tight_layout()
    F.save_to(fig, CH, "選物I-5-簡諧能量")


if __name__ == "__main__":
    fig_centripetal()
    fig_shm_projection()
    fig_spring()
    fig_pendulum()
    fig_energy()
    print("done.")
