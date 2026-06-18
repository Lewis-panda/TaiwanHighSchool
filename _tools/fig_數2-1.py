# -*- coding: utf-8 -*-
"""產生「數2-1 三角比」的圖，輸出到該章 sources/。
重繪：  .venv/bin/python _tools/fig_數2-1.py
幾何圖：F.canvas() + ax.plot() + F.clean_grid(ax)；
單位圓 / 三角形用 ax.set_aspect("equal")。
注意：mathtext 不支援 \\dfrac/\\tfrac（用 \\frac）；圖內中文勿放進 $...$。
"""

import os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Polygon, Arc, FancyArrowPatch
import figlib as F

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CH = os.path.join(ROOT, "數學", "數學一下（必修·第二冊）", "數2-1 三角比")


def _right_angle_mark(ax, corner, d1, d2, s=0.18, color=F.INK, lw=1.2):
    """在 corner 處畫直角小方框，d1、d2 為兩條邊的單位方向。"""
    d1 = np.array(d1, float)
    d1 = d1 / np.hypot(*d1)
    d2 = np.array(d2, float)
    d2 = d2 / np.hypot(*d2)
    p0 = np.array(corner, float)
    p1 = p0 + s * d1
    p2 = p0 + s * d1 + s * d2
    p3 = p0 + s * d2
    ax.plot([p1[0], p2[0]], [p1[1], p2[1]], color=color, lw=lw, zorder=5)
    ax.plot([p2[0], p3[0]], [p2[1], p3[1]], color=color, lw=lw, zorder=5)


def fig_right_triangle():
    """直角三角形的三角比：標出對邊、鄰邊、斜邊與角 θ。"""
    fig, ax = F.canvas(6.4, 5.0)
    # 直角在 C(0,0)，B 在 (4,0)，A 在 (0,3)
    C = np.array([0.0, 0.0])
    B = np.array([4.0, 0.0])
    A = np.array([0.0, 3.0])
    tri = Polygon([C, B, A], closed=True, fc="#eef3fb", ec=F.INK, lw=2.2, zorder=2)
    ax.add_patch(tri)

    # 三邊上色
    ax.plot([C[0], B[0]], [C[1], B[1]], color=F.BLUE, lw=3.0, zorder=3)
    ax.plot([C[0], A[0]], [C[1], A[1]], color=F.RED, lw=3.0, zorder=3)
    ax.plot([B[0], A[0]], [B[1], A[1]], color=F.GREEN, lw=3.0, zorder=3)

    # 角 θ 在 B（終邊 BA 與 BC 之間，BA 方向約 143.13°）
    ax.add_patch(
        Arc(
            B,
            1.3,
            1.3,
            angle=0,
            theta1=143.13,
            theta2=180,
            color=F.AMBER,
            lw=2.0,
            zorder=4,
        )
    )
    ax.text(2.95, 0.33, r"$\theta$", color=F.AMBER, fontsize=16, ha="center")

    # 直角符號在 C
    _right_angle_mark(ax, C, [1, 0], [0, 1], s=0.30)

    # 頂點標示
    for P, name, off in [
        (C, "C", (-0.20, -0.28)),
        (B, "B", (0.22, -0.28)),
        (A, "A", (-0.22, 0.18)),
    ]:
        ax.add_patch(Circle(P, 0.06, color=F.INK, zorder=6))
        ax.text(P[0] + off[0], P[1] + off[1], f"${name}$", fontsize=13, ha="center")

    # 邊名稱（中文不放進 $...$）
    ax.text(2.05, -0.42, "鄰邊", color=F.BLUE, fontsize=13, ha="center")
    ax.text(-0.45, 1.5, "對邊", color=F.RED, fontsize=13, ha="center", rotation=90)
    ax.text(
        2.45, 1.85, "斜邊", color=F.GREEN, fontsize=13, ha="center", rotation=-36.87
    )

    # 公式說明
    ax.text(
        2.75,
        2.75,
        r"$\sin\theta=\frac{\mathrm{opp}}{\mathrm{hyp}},\ "
        r"\cos\theta=\frac{\mathrm{adj}}{\mathrm{hyp}},\ "
        r"\tan\theta=\frac{\mathrm{opp}}{\mathrm{adj}}$",
        color=F.INK,
        fontsize=12,
        ha="center",
        va="center",
        bbox=dict(boxstyle="round,pad=0.35", fc="white", ec=F.GRID, lw=1.2),
    )

    ax.set_xlim(-1.0, 5.2)
    ax.set_ylim(-1.0, 3.6)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("直角三角形的三角比", fontsize=14)
    F.save_to(fig, CH, "數2-1-直角三角比")


def fig_general_angle():
    """廣義角與單位圓：標準位置角，終邊上一點 P(x,y)，r、象限。"""
    fig, ax = F.canvas(6.4, 6.2)
    L = 1.55

    # 坐標軸
    ax.annotate(
        "",
        xy=(L, 0),
        xytext=(-L, 0),
        arrowprops=dict(arrowstyle="-|>", color=F.INK, lw=1.4),
    )
    ax.annotate(
        "",
        xy=(0, L),
        xytext=(0, -L),
        arrowprops=dict(arrowstyle="-|>", color=F.INK, lw=1.4),
    )
    ax.text(L - 0.05, -0.18, "$x$", fontsize=12, ha="right")
    ax.text(0.14, L - 0.05, "$y$", fontsize=12, va="top")

    # 單位圓
    th = np.linspace(0, 2 * np.pi, 400)
    ax.plot(np.cos(th), np.sin(th), color=F.GRID, lw=1.6, zorder=1)

    # 廣義角 θ = 125°，終邊上一點 P 在單位圓上
    ang = np.deg2rad(125)
    Px, Py = np.cos(ang), np.sin(ang)

    # 始邊（x 軸正向，加粗一小段）
    ax.plot([0, 1.0], [0, 0], color=F.INK, lw=2.4, zorder=3)
    ax.text(0.62, -0.16, "始邊", color=F.INK, fontsize=11, ha="center")

    # 終邊
    ax.plot([0, Px * 1.18], [0, Py * 1.18], color=F.BLUE, lw=2.6, zorder=4)
    ax.text(
        Px * 1.18 - 0.30,
        Py * 1.18 + 0.10,
        "終邊",
        color=F.BLUE,
        fontsize=11,
        ha="center",
    )

    # 旋轉角弧（逆時針為正）
    ax.add_patch(
        Arc(
            (0, 0),
            0.9,
            0.9,
            angle=0,
            theta1=0,
            theta2=125,
            color=F.AMBER,
            lw=2.0,
            zorder=3,
        )
    )
    ax.text(0.30, 0.46, r"$\theta$", color=F.AMBER, fontsize=15, ha="center")

    # 點 P 與投影
    ax.add_patch(Circle((Px, Py), 0.045, color=F.RED, zorder=7))
    ax.text(Px + 0.02, Py + 0.16, "$P(x,\\,y)$", color=F.RED, fontsize=12, ha="center")
    # 鉛直投影段 → y（紅虛線）
    ax.plot([Px, Px], [0, Py], color=F.RED, lw=1.3, ls=":", zorder=2)
    ax.text(Px - 0.07, Py / 2, "$y$", color=F.RED, fontsize=12, ha="right")
    # 水平投影段 → x（綠，沿 x 軸由原點到 Px，因第二象限 x<0）
    ax.plot([0, Px], [0, 0], color=F.GREEN, lw=2.6, zorder=2)
    ax.text(Px / 2, -0.16, "$x$", color=F.GREEN, fontsize=12, ha="center")
    # r 標在終邊中段
    ax.text(
        Px * 0.55 - 0.10, Py * 0.55 + 0.06, "$r$", color=F.BLUE, fontsize=13, ha="right"
    )

    # 象限標籤
    for qx, qy, t in [
        (1.25, 1.25, "I"),
        (-1.25, 1.25, "II"),
        (-1.25, -1.25, "III"),
        (1.25, -1.25, "IV"),
    ]:
        ax.text(qx, qy, t, color="#9aa0a6", fontsize=12, ha="center", va="center")

    # 定義說明
    ax.text(
        0.0,
        -1.42,
        r"$\sin\theta=\frac{y}{r},\quad \cos\theta=\frac{x}{r},"
        r"\quad \tan\theta=\frac{y}{x}$",
        color=F.INK,
        fontsize=12.5,
        ha="center",
        va="center",
    )

    ax.set_xlim(-1.7, 1.7)
    ax.set_ylim(-1.75, 1.7)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("廣義角與單位圓（標準位置）", fontsize=14)
    F.save_to(fig, CH, "數2-1-廣義角")


def fig_laws():
    """正弦定理與餘弦定理示意：一般三角形，標 a,b,c 與角 A,B,C 及高。"""
    fig, ax = F.canvas(7.2, 5.0)
    # 頂點：A 左下、B 右下、C 上方（一般三角形）
    A = np.array([0.0, 0.0])
    B = np.array([5.0, 0.0])
    C = np.array([1.4, 3.2])
    tri = Polygon([A, B, C], closed=True, fc="#eef3fb", ec=F.INK, lw=2.2, zorder=2)
    ax.add_patch(tri)

    # 頂點標示
    for P, name, off in [
        (A, "A", (-0.28, -0.28)),
        (B, "B", (0.22, -0.28)),
        (C, "C", (0.0, 0.26)),
    ]:
        ax.add_patch(Circle(P, 0.06, color=F.INK, zorder=6))
        ax.text(P[0] + off[0], P[1] + off[1], f"${name}$", fontsize=14, ha="center")

    # 邊名稱：a 對 A（BC）、b 對 B（CA）、c 對 C（AB）
    midBC = (B + C) / 2
    midCA = (C + A) / 2
    midAB = (A + B) / 2
    ax.text(midBC[0] + 0.30, midBC[1] + 0.12, "$a$", color=F.RED, fontsize=14)
    ax.text(midCA[0] - 0.30, midCA[1] + 0.05, "$b$", color=F.BLUE, fontsize=14)
    ax.text(midAB[0], midAB[1] - 0.36, "$c$", color=F.GREEN, fontsize=14)

    # 從 C 作高到 AB
    foot = np.array([C[0], 0.0])
    ax.plot([C[0], foot[0]], [C[1], foot[1]], color=F.AMBER, lw=1.8, ls="--", zorder=3)
    ax.text(C[0] + 0.16, 1.5, "$h$", color=F.AMBER, fontsize=13, ha="left")
    _right_angle_mark(ax, foot, [-1, 0], [0, 1], s=0.20, color=F.AMBER)

    # 公式框（兩條定理）
    ax.text(
        6.45,
        2.55,
        r"$\frac{a}{\sin A}=\frac{b}{\sin B}=\frac{c}{\sin C}=2R$",
        color=F.INK,
        fontsize=12,
        ha="center",
        va="center",
        bbox=dict(boxstyle="round,pad=0.30", fc="white", ec=F.BLUE, lw=1.2),
    )
    ax.text(
        6.45,
        1.45,
        r"$c^2=a^2+b^2-2ab\cos C$",
        color=F.INK,
        fontsize=12,
        ha="center",
        va="center",
        bbox=dict(boxstyle="round,pad=0.30", fc="white", ec=F.RED, lw=1.2),
    )

    ax.set_xlim(-0.9, 8.5)
    ax.set_ylim(-0.8, 3.8)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("解三角形：正弦定理與餘弦定理", fontsize=14)
    F.save_to(fig, CH, "數2-1-正餘弦定理")


def fig_polar():
    """極坐標與直角坐標互換：點 P，標 r、θ、x、y。"""
    fig, ax = F.canvas(6.4, 5.4)
    L = 4.0

    ax.annotate(
        "",
        xy=(L, 0),
        xytext=(-0.7, 0),
        arrowprops=dict(arrowstyle="-|>", color=F.INK, lw=1.4),
    )
    ax.annotate(
        "",
        xy=(0, 3.6),
        xytext=(0, -0.7),
        arrowprops=dict(arrowstyle="-|>", color=F.INK, lw=1.4),
    )
    ax.text(L - 0.05, -0.30, "$x$", fontsize=12, ha="right")
    ax.text(0.16, 3.5, "$y$", fontsize=12, va="top")
    ax.text(0.32, -0.36, "極軸", color="#6b7280", fontsize=10.5, ha="left")
    ax.text(-0.18, -0.30, "$O$", fontsize=12, ha="right")

    # 點 P(3, 2.2)
    P = np.array([3.0, 2.2])
    # x 投影段（綠，畫在底）
    ax.plot([0, P[0]], [0, 0], color=F.GREEN, lw=3.0, zorder=3)
    # 鉛直投影（紅虛線）
    ax.plot([P[0], P[0]], [0, P[1]], color=F.RED, lw=1.6, ls=":", zorder=2)
    # r 線段（藍）
    ax.plot([0, P[0]], [0, P[1]], color=F.BLUE, lw=2.6, zorder=4)

    ax.add_patch(Circle(P, 0.07, color=F.INK, zorder=7))
    ax.text(
        P[0] + 0.12,
        P[1] + 0.18,
        "$P(x,\\,y)=(r,\\,\\theta)$",
        color=F.INK,
        fontsize=12.5,
        ha="left",
    )

    # 角 θ
    ax.add_patch(
        Arc(
            (0, 0),
            1.5,
            1.5,
            angle=0,
            theta1=0,
            theta2=np.rad2deg(np.arctan2(P[1], P[0])),
            color=F.AMBER,
            lw=2.0,
            zorder=3,
        )
    )
    ax.text(0.95, 0.34, r"$\theta$", color=F.AMBER, fontsize=15, ha="center")

    # 邊標示
    ax.text(
        P[0] * 0.5 - 0.12,
        P[1] * 0.5 + 0.20,
        "$r$",
        color=F.BLUE,
        fontsize=14,
        ha="right",
    )
    ax.text(P[0] / 2, -0.34, "$x$", color=F.GREEN, fontsize=13, ha="center")
    ax.text(P[0] + 0.16, P[1] / 2, "$y$", color=F.RED, fontsize=13, ha="left")

    # 直角符號在 (P[0], 0)
    _right_angle_mark(ax, np.array([P[0], 0.0]), [-1, 0], [0, 1], s=0.20)

    # 互換公式
    ax.text(
        1.55,
        3.10,
        r"$x=r\cos\theta,\ \ y=r\sin\theta$",
        color=F.INK,
        fontsize=12.5,
        ha="center",
        va="center",
        bbox=dict(boxstyle="round,pad=0.30", fc="white", ec=F.GRID, lw=1.2),
    )

    ax.set_xlim(-0.9, L)
    ax.set_ylim(-0.9, 3.7)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("極坐標與直角坐標互換", fontsize=14)
    F.save_to(fig, CH, "數2-1-極坐標")


if __name__ == "__main__":
    fig_right_triangle()
    fig_general_angle()
    fig_laws()
    fig_polar()
    print("done.")
