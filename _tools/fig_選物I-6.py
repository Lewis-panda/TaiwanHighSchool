# -*- coding: utf-8 -*-
"""產生「選物I-6 萬有引力」的圖，輸出到該章 sources/。
重繪：  .venv/bin/python _tools/fig_選物I-6.py
"""

import os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch, Polygon
import figlib as F

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CH = os.path.join(ROOT, "物理", "物理二上（選修物理I·力學一）", "選物I-6 萬有引力")


def fig_gravitation():
    """兩質量間的萬有引力（成對、等大反向）＋力大小隨 r 的平方反比曲線。"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.6, 4.2))

    # 左：兩質量與一對引力
    ax1.set_aspect("equal")
    ax1.axis("off")
    A = np.array([-2.0, 0.0])
    B = np.array([2.2, 0.0])
    ax1.add_patch(
        Circle(A, 0.55, facecolor="#dbe7ff", edgecolor=F.INK, lw=1.6, zorder=3)
    )
    ax1.add_patch(
        Circle(B, 0.35, facecolor="#ffd9dc", edgecolor=F.INK, lw=1.6, zorder=3)
    )
    ax1.text(A[0], A[1], "$M$", ha="center", va="center", fontsize=15, zorder=4)
    ax1.text(B[0], B[1], "$m$", ha="center", va="center", fontsize=14, zorder=4)
    # 距離線
    ax1.annotate(
        "",
        xy=(A[0], -1.15),
        xytext=(B[0], -1.15),
        arrowprops=dict(arrowstyle="<->", color="#6b7280", lw=1.3),
    )
    ax1.text(0.1, -1.45, "$r$（兩質心距離）", ha="center", color="#6b7280", fontsize=12)
    # 一對引力：m 受向左的力、M 受向右的力（等大反向）
    F.arrow(ax1, (A[0] + 0.75, 0.0), (A[0] + 0.75 + 1.4, 0.0), color=F.RED)
    F.arrow(ax1, (B[0] - 0.55, 0.0), (B[0] - 0.55 - 1.4, 0.0), color=F.RED)
    ax1.text(A[0] + 1.5, 0.42, r"$F_{M\to m}$", color=F.RED, ha="center", fontsize=12)
    ax1.text(B[0] - 1.5, 0.42, r"$F_{m\to M}$", color=F.RED, ha="center", fontsize=12)
    ax1.text(
        0.1,
        1.55,
        r"$F=\dfrac{GMm}{r^{2}}$（等大、反向、沿連線）",
        ha="center",
        color=F.INK,
        fontsize=13,
    )
    ax1.set_xlim(-4.0, 4.4)
    ax1.set_ylim(-2.0, 2.2)
    ax1.set_title("兩質量間的萬有引力", fontsize=13)

    # 右：平方反比 F ∝ 1/r²
    r = np.linspace(1.0, 5.0, 400)
    Fval = 1.0 / r**2
    ax2.plot(r, Fval, color=F.BLUE, lw=2.8)
    for rr in [1, 2, 3]:
        ax2.plot([rr, rr], [0, 1.0 / rr**2], color="#bcc4cf", lw=1.0, ls="--")
        ax2.plot([0, rr], [1.0 / rr**2, 1.0 / rr**2], color="#bcc4cf", lw=1.0, ls="--")
        ax2.plot([rr], [1.0 / rr**2], "o", color=F.BLUE, ms=6)
    ax2.text(2.05, 0.27, "$r$ 變 2 倍 → $F$ 變 1/4", color=F.INK, fontsize=11)
    ax2.text(3.05, 0.13, "$r$ 變 3 倍 → $F$ 變 1/9", color=F.INK, fontsize=11)
    ax2.set_xlim(0, 5.2)
    ax2.set_ylim(0, 1.15)
    ax2.set_xlabel("距離 $r$（任意單位）")
    ax2.set_ylabel("引力大小 $F$（任意單位）")
    ax2.set_title(r"平方反比：$F\propto 1/r^{2}$", fontsize=13)
    F.clean_grid(ax2)

    fig.tight_layout()
    F.save_to(fig, CH, "選物I-6-萬有引力")


def fig_surface_gravity():
    """g 隨離地高度（到地心距離）遞減：g(r)=GM/r²，地表 r=R。"""
    fig, ax = F.canvas(7.0, 4.4)
    Re = 6.37e6
    GM = 3.986e14
    r = np.linspace(Re, 6 * Re, 500)
    g = GM / r**2
    ax.plot((r - Re) / Re * Re / 1e6, g, color=F.BLUE, lw=2.8)
    # 地表 g≈9.8
    ax.axhline(9.81, color="#bcc4cf", lw=1.0, ls="--")
    ax.plot([0], [9.81], "o", color=F.RED, ms=7)
    ax.annotate(
        "地表 $g\\approx 9.8\\ \\mathrm{m/s^2}$（$r=R$）",
        xy=(0, 9.81),
        xytext=(8, 8.4),
        color=F.RED,
        fontsize=11,
        arrowprops=dict(arrowstyle="->", color=F.RED),
    )
    # 標一個高度點（例如 ~一個地球半徑高，g 變 1/4）
    h1 = Re
    g1 = GM / (Re + h1) ** 2
    ax.plot([h1 / 1e6], [g1], "o", color=F.GREEN, ms=7)
    ax.annotate(
        "離地約一個地球半徑高\n$g$ 約剩 1/4（$r=2R$）",
        xy=(h1 / 1e6, g1),
        xytext=(14, 4.6),
        color=F.GREEN,
        fontsize=11,
        arrowprops=dict(arrowstyle="->", color=F.GREEN),
    )
    ax.set_xlim(0, 32)
    ax.set_ylim(0, 11)
    ax.set_xlabel("離地表高度 $h$（$\\times10^{6}$ m，地球半徑約 6.37）")
    ax.set_ylabel("重力加速度 $g$（$\\mathrm{m/s^2}$）")
    ax.set_title(r"地表重力加速度隨高度遞減：$g=\dfrac{GM}{(R+h)^{2}}$")
    F.clean_grid(ax)
    F.save_to(fig, CH, "選物I-6-地表重力")


def fig_satellite():
    """衛星圓軌道：萬有引力＝向心力；不同半徑 → 不同速率（外圈較慢）。"""
    fig, ax = F.schematic(6.4, 6.0)
    # 地球
    Re = 1.0
    ax.add_patch(
        Circle((0, 0), Re, facecolor="#cfe3ff", edgecolor=F.INK, lw=1.8, zorder=2)
    )
    ax.text(0, 0, "地球\n$M$", ha="center", va="center", fontsize=12, zorder=3)
    # 兩條軌道
    for rad, col, name, vlab in [
        (1.9, F.BLUE, "近軌道（快）", "$v$ 大"),
        (2.9, F.GREEN, "遠軌道（慢）", "$v$ 小"),
    ]:
        th = np.linspace(0, 2 * np.pi, 300)
        ax.plot(rad * np.cos(th), rad * np.sin(th), color=col, lw=1.6, ls="--")
        # 衛星位置（右上）
        ang = np.deg2rad(48)
        P = np.array([rad * np.cos(ang), rad * np.sin(ang)])
        ax.add_patch(Circle(P, 0.14, facecolor=col, edgecolor=F.INK, lw=1.2, zorder=5))
        # 萬有引力（指向地心）
        rhat = P / np.linalg.norm(P)
        F.arrow(ax, P, P - rhat * 0.9, color=F.RED, lw=2.0, mutation=14)
        # 速度（切線方向，逆時針）
        that = np.array([-rhat[1], rhat[0]])
        F.arrow(ax, P, P + that * 0.95, color=col, lw=2.0, mutation=14)
        ax.text(
            P[0] + that[0] * 1.25,
            P[1] + that[1] * 1.25,
            vlab,
            color=col,
            ha="center",
            fontsize=11,
        )
        ax.text(
            rad * np.cos(np.deg2rad(-58)),
            rad * np.sin(np.deg2rad(-58)),
            name,
            color=col,
            ha="center",
            fontsize=11,
        )
    # 一個重力箭頭加標籤
    ax.text(2.55, 1.15, "萬有引力\n（向心力）", color=F.RED, ha="center", fontsize=11)
    ax.set_xlim(-3.4, 3.6)
    ax.set_ylim(-3.4, 3.6)
    ax.set_title(r"衛星圓軌道：$\dfrac{GMm}{r^{2}}=\dfrac{mv^{2}}{r}$", fontsize=14)
    F.save_to(fig, CH, "選物I-6-衛星軌道")


def fig_kepler3():
    """由圓軌道導 T²∝r³：左為導出示意，右為 T² 對 r³ 的直線。"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.8, 4.4))

    # 左：圓軌道 + 推導文字
    ax1.set_aspect("equal")
    ax1.axis("off")
    ax1.add_patch(
        Circle((0, 0), 0.6, facecolor="#cfe3ff", edgecolor=F.INK, lw=1.6, zorder=2)
    )
    ax1.text(0, 0, "$M$", ha="center", va="center", fontsize=13, zorder=3)
    th = np.linspace(0, 2 * np.pi, 300)
    R = 1.9
    ax1.plot(R * np.cos(th), R * np.sin(th), color=F.BLUE, lw=1.6, ls="--")
    ang = np.deg2rad(55)
    P = np.array([R * np.cos(ang), R * np.sin(ang)])
    ax1.add_patch(Circle(P, 0.13, facecolor=F.BLUE, edgecolor=F.INK, lw=1.2, zorder=5))
    rhat = P / np.linalg.norm(P)
    that = np.array([-rhat[1], rhat[0]])
    F.arrow(ax1, P, P - rhat * 0.8, color=F.RED, lw=2.0, mutation=13)
    F.arrow(ax1, P, P + that * 0.9, color=F.BLUE, lw=2.0, mutation=13)
    ax1.annotate(
        "",
        xy=(0, 0),
        xytext=P,
        arrowprops=dict(arrowstyle="-", color="#6b7280", lw=1.1, ls="--"),
    )
    ax1.text(P[0] * 0.5 - 0.18, P[1] * 0.5 + 0.12, "$r$", color="#6b7280", fontsize=12)
    ax1.text(
        0,
        -2.45,
        r"$\dfrac{GMm}{r^{2}}=\dfrac{4\pi^{2}}{T^{2}}mr$"
        "\n"
        r"$\Rightarrow\ T^{2}=\dfrac{4\pi^{2}}{GM}\,r^{3}$",
        ha="center",
        va="center",
        color=F.INK,
        fontsize=13,
    )
    ax1.set_xlim(-2.4, 2.4)
    ax1.set_ylim(-3.0, 2.3)
    ax1.set_title("圓軌道：引力＝向心力", fontsize=13)

    # 右：T² 對 r³ 為直線（用太陽系資料示意，任意單位）
    # 取 r（天文單位 AU）與 T（年）：T² = r³ 在這套單位下恰成立
    names = ["水", "金", "地", "火", "木", "土"]
    r_au = np.array([0.39, 0.72, 1.00, 1.52, 5.20, 9.58])
    T_yr = r_au**1.5
    ax2.plot(r_au**3, T_yr**2, "o", color=F.RED, ms=8, zorder=4)
    xline = np.linspace(0, r_au.max() ** 3 * 1.05, 50)
    ax2.plot(xline, xline, color=F.BLUE, lw=2.2, zorder=2)
    for nm, x, y in zip(names, r_au**3, T_yr**2):
        ax2.annotate(
            nm,
            (x, y),
            textcoords="offset points",
            xytext=(6, -10),
            fontsize=10,
            color=F.INK,
        )
    ax2.text(120, 700, r"$T^{2}=k\,r^{3}$（斜率 $=k$）", color=F.BLUE, fontsize=12)
    ax2.set_xlim(0, r_au.max() ** 3 * 1.05)
    ax2.set_ylim(0, T_yr.max() ** 2 * 1.05)
    ax2.set_xlabel(r"$r^{3}$（$\mathrm{AU}^{3}$）")
    ax2.set_ylabel(r"$T^{2}$（年$^{2}$）")
    ax2.set_title(r"太陽系：$T^{2}$ 正比於 $r^{3}$", fontsize=13)
    F.clean_grid(ax2)

    fig.tight_layout()
    F.save_to(fig, CH, "選物I-6-克卜勒推導")


def fig_kepler_laws():
    """克卜勒三大定律三聯圖：
    左——第一定律：橢圓軌道、太陽在一焦點（另一焦點空著）。
    中——第二定律：等面積（相等時間內掃過面積相等，故近日快、遠日慢）。
    右——第三定律：T² 正比於 a³（半長軸）。
    """
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(13.2, 4.5))

    # 橢圓參數（兩圖共用）：a 半長軸、b 半短軸、c 焦距
    a, b = 2.3, 1.65
    c = np.sqrt(a**2 - b**2)  # 焦點離中心的距離
    th = np.linspace(0, 2 * np.pi, 400)
    ex, ey = a * np.cos(th), b * np.sin(th)

    # ---- 左：第一定律（橢圓軌道、太陽在焦點）----
    ax1.set_aspect("equal")
    ax1.axis("off")
    ax1.plot(ex, ey, color=F.BLUE, lw=2.2, zorder=2)
    # 太陽在右焦點 (+c, 0)；左焦點 (-c, 0) 為空焦點
    Fsun = np.array([c, 0.0])
    Fempty = np.array([-c, 0.0])
    ax1.plot([Fsun[0]], [Fsun[1]], "o", color=F.AMBER, ms=16, zorder=4)
    ax1.plot([Fempty[0]], [Fempty[1]], "x", color="#6b7280", ms=9, mew=2, zorder=4)
    ax1.text(
        Fsun[0] + 0.12,
        Fsun[1] - 0.18,
        "太陽（焦點）",
        ha="left",
        va="top",
        color=F.AMBER,
        fontsize=11,
    )
    ax1.text(
        Fempty[0],
        Fempty[1] + 0.18,
        "空焦點",
        ha="center",
        va="bottom",
        color="#6b7280",
        fontsize=10,
    )
    # 中心
    ax1.plot([0], [0], "+", color="#6b7280", ms=8, mew=1.4, zorder=4)
    ax1.text(0.05, 0.16, "中心", ha="left", va="bottom", color="#6b7280", fontsize=9)
    # 一顆行星
    pang = np.deg2rad(118)
    P = np.array([a * np.cos(pang), b * np.sin(pang)])
    ax1.add_patch(Circle(P, 0.13, facecolor=F.RED, edgecolor=F.INK, lw=1.2, zorder=5))
    ax1.text(
        P[0] - 0.1,
        P[1] + 0.2,
        "行星",
        ha="center",
        va="bottom",
        color=F.RED,
        fontsize=11,
    )
    # 半長軸 a（中心到左頂點，畫在離太陽較遠的一側避免重疊）
    ax1.annotate(
        "",
        xy=(-a, -0.0),
        xytext=(0, -0.0),
        arrowprops=dict(arrowstyle="<->", color=F.GREEN, lw=1.4),
    )
    ax1.text(
        -a * 0.5, -0.26, "半長軸 a", ha="center", va="top", color=F.GREEN, fontsize=11
    )
    # 近日點 / 遠日點（相對太陽焦點；太陽在右焦點，故右頂點離太陽最近＝近日點）
    ax1.text(a + 0.06, 0.18, "近日點", ha="left", va="bottom", color=F.INK, fontsize=10)
    ax1.text(
        -a - 0.06, 0.18, "遠日點", ha="right", va="bottom", color=F.INK, fontsize=10
    )
    ax1.set_xlim(-a - 0.9, a + 0.9)
    ax1.set_ylim(-b - 1.0, b + 0.7)
    ax1.set_title("第一定律：橢圓軌道，太陽在焦點", fontsize=12)

    # ---- 中：第二定律（等面積）----
    ax2.set_aspect("equal")
    ax2.axis("off")
    ax2.plot(ex, ey, color=F.BLUE, lw=2.2, zorder=2)
    Fsun2 = np.array([c, 0.0])
    ax2.plot([Fsun2[0]], [Fsun2[1]], "o", color=F.AMBER, ms=15, zorder=4)
    ax2.text(
        Fsun2[0],
        Fsun2[1] - 0.4,
        "太陽",
        ha="center",
        va="top",
        color=F.AMBER,
        fontsize=11,
    )

    def sector(t0, t1):
        """以太陽焦點為頂點，橢圓弧 t0→t1 之間圍成的扇形 Polygon 頂點。"""
        ts = np.linspace(t0, t1, 80)
        arc = np.column_stack([a * np.cos(ts), b * np.sin(ts)])
        return np.vstack([Fsun2, arc])

    def poly_area(pts):
        x, y = pts[:, 0], pts[:, 1]
        return 0.5 * abs(np.dot(x, np.roll(y, -1)) - np.dot(y, np.roll(x, -1)))

    # 太陽在右焦點：右端為近日點（靠太陽）、左端為遠日點（離太陽遠）
    # 近日點側（右端，靠太陽）：相同時間走得快、掃角大
    near = sector(np.deg2rad(-42), np.deg2rad(42))
    target = poly_area(near)
    # 遠日點側（左端，離太陽遠）：求出與近日點側等面積的較小掃角
    half = np.deg2rad(2.0)
    for _ in range(60):  # 二分逼近，使兩扇形面積相等（克卜勒第二定律）
        far = sector(np.pi - half, np.pi + half)
        if poly_area(far) < target:
            half += np.deg2rad(0.5)
        else:
            half -= np.deg2rad(0.25)
        if half <= np.deg2rad(0.5):
            half = np.deg2rad(0.5)
            break
    far = sector(np.pi - half, np.pi + half)
    ax2.add_patch(
        Polygon(
            near,
            closed=True,
            facecolor=F.RED,
            alpha=0.30,
            edgecolor=F.RED,
            lw=1.4,
            zorder=3,
        )
    )
    ax2.add_patch(
        Polygon(
            far,
            closed=True,
            facecolor=F.BLUE,
            alpha=0.30,
            edgecolor=F.BLUE,
            lw=1.4,
            zorder=3,
        )
    )
    # 兩塊面積相等的標註（紅＝近日點側、藍＝遠日點側）
    ax2.text(
        a - 0.95,
        0.0,
        "面積\n相等",
        ha="center",
        va="center",
        color=F.RED,
        fontsize=10,
        zorder=6,
    )
    ax2.text(
        -a + 0.62,
        0.0,
        "面積\n相等",
        ha="center",
        va="center",
        color=F.BLUE,
        fontsize=10,
        zorder=6,
    )
    # 兩端弧長對比：近日點走的弧長（快）vs 遠日點走的弧長（慢）
    ax2.annotate(
        "近日點\n走得快（弧長）",
        xy=(a, 0.0),
        xytext=(a + 0.2, b + 0.5),
        ha="center",
        va="bottom",
        color=F.RED,
        fontsize=10,
        arrowprops=dict(arrowstyle="->", color=F.RED),
    )
    ax2.annotate(
        "遠日點\n走得慢（弧短）",
        xy=(-a, 0.0),
        xytext=(-a - 0.2, b + 0.5),
        ha="center",
        va="bottom",
        color=F.BLUE,
        fontsize=10,
        arrowprops=dict(arrowstyle="->", color=F.BLUE),
    )
    ax2.set_xlim(-a - 0.9, a + 0.9)
    ax2.set_ylim(-b - 0.7, b + 1.05)
    ax2.set_title("第二定律：相等時間掃過相等面積", fontsize=12)

    # ---- 右：第三定律 T²∝a³（半長軸的立方）----
    names = ["水", "金", "地", "火", "木", "土"]
    a_au = np.array([0.39, 0.72, 1.00, 1.52, 5.20, 9.58])
    T_yr = a_au**1.5  # 在 AU、年 的單位下 T² = a³
    ax3.plot(a_au**3, T_yr**2, "o", color=F.RED, ms=8, zorder=4)
    xline = np.linspace(0, a_au.max() ** 3 * 1.05, 50)
    ax3.plot(xline, xline, color=F.BLUE, lw=2.2, zorder=2)
    for nm, x, y in zip(names, a_au**3, T_yr**2):
        ax3.annotate(
            nm,
            (x, y),
            textcoords="offset points",
            xytext=(6, -11),
            fontsize=10,
            color=F.INK,
        )
    ax3.text(120, 700, r"$T^{2}=k\,a^{3}$", color=F.BLUE, fontsize=12)
    ax3.text(120, 470, "斜率 $k=\\dfrac{4\\pi^{2}}{GM}$", color=F.BLUE, fontsize=11)
    ax3.set_xlim(0, a_au.max() ** 3 * 1.05)
    ax3.set_ylim(0, T_yr.max() ** 2 * 1.05)
    ax3.set_xlabel(r"半長軸立方 $a^{3}$（$\mathrm{AU}^{3}$）")
    ax3.set_ylabel(r"週期平方 $T^{2}$（年$^{2}$）")
    ax3.set_title("第三定律：$T^{2}$ 正比於 $a^{3}$", fontsize=12)
    F.clean_grid(ax3)

    fig.tight_layout()
    F.save_to(fig, CH, "選物I-6-克卜勒三定律")


if __name__ == "__main__":
    fig_gravitation()
    fig_surface_gravity()
    fig_satellite()
    fig_kepler3()
    fig_kepler_laws()
    print("done.")
