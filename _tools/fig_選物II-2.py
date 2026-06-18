# -*- coding: utf-8 -*-
"""產生「選物II-2 功與能量」的圖，輸出到該章 sources/。
重繪：  .venv/bin/python _tools/fig_選物II-2.py
"""

import os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon, Arc, Circle, FancyArrowPatch
import figlib as F

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CH = os.path.join(
    ROOT, "物理", "物理二下（選修物理II·力學二，僅力學）", "選物II-2 功與能量"
)


def fig_work_definition():
    """功的定義：力與位移夾角 θ，只有 F cosθ 這個分量做功。"""
    fig, ax = F.schematic(7.2, 4.6)
    # 地面與物體
    ax.plot([-3.4, 3.6], [-1.2, -1.2], color=F.INK, lw=1.6)
    box = Rectangle(
        (-0.7, -1.2), 1.4, 1.0, facecolor="#dbe7ff", edgecolor=F.INK, lw=1.6, zorder=3
    )
    ax.add_patch(box)
    c = np.array([0.0, -0.7])  # 力的作用點（物體中心高度）
    ax.add_patch(Circle(c, 0.05, color=F.INK, zorder=6))

    # 位移向量 d（水平向右）
    F.arrow(ax, (c[0], -1.2), (3.0, -1.2), color="#6b7280", lw=2.2)
    F.label(ax, (3.05, -1.5), r"位移 $\vec d$", color="#6b7280", ha="left")

    # 施力 F（與水平夾角 θ）
    th = np.deg2rad(35)
    Fmag = 2.3
    tip = c + Fmag * np.array([np.cos(th), np.sin(th)])
    F.arrow(ax, c, tip, color=F.BLUE, lw=2.8)
    F.label(ax, tip + np.array([0.12, 0.18]), r"$\vec F$", color=F.BLUE, ha="left")

    # 角 θ
    ax.add_patch(Arc(c, 1.5, 1.5, angle=0, theta1=0, theta2=35, color=F.INK, lw=1.4))
    ax.text(c[0] + 0.95, c[1] + 0.22, r"$\theta$", color=F.INK, fontsize=14)

    # F 的水平分量 F cosθ（做功的分量）
    hx = c + np.array([Fmag * np.cos(th), 0])
    F.arrow(ax, c, hx, color=F.RED, lw=2.6)
    F.label(
        ax,
        (hx[0] + 0.05, c[1] - 0.32),
        r"$F\cos\theta$（真正做功）",
        color=F.RED,
        ha="center",
    )
    # 虛線：從 F 頂點垂直投影到水平分量
    ax.plot([tip[0], hx[0]], [tip[1], hx[1]], color="#999", lw=1.0, ls="--")
    # 鉛直分量 F sinθ（不做功）
    vy = c + np.array([0, Fmag * np.sin(th)])
    F.arrow(ax, c, vy, color=F.GREEN, lw=1.8, ls=":")
    F.label(
        ax,
        (c[0] - 0.15, vy[1] + 0.05),
        r"$F\sin\theta$（不做功）",
        color=F.GREEN,
        ha="right",
    )

    ax.text(
        0.0,
        1.65,
        r"$W=\vec F\cdot\vec d=Fd\cos\theta$",
        ha="center",
        color=F.INK,
        fontsize=15,
    )
    ax.set_title("功：只有「沿位移方向」的力分量才做功", fontsize=13)
    ax.set_xlim(-3.6, 4.0)
    ax.set_ylim(-2.0, 2.3)
    F.save_to(fig, CH, "選物II-2-功的定義")


def fig_variable_force():
    """變力作功＝F–x 圖面積；以彈簧 F=kx 的三角形面積為例。"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.4, 4.0))

    # 左：一般變力，面積 = 功
    x = np.linspace(0, 5, 200)
    Fx = 1.0 + 0.9 * x - 0.07 * x**2
    ax1.plot(x, Fx, color=F.BLUE, lw=2.6)
    ax1.fill_between(x, 0, Fx, color=F.FILL, alpha=0.14)
    ax1.text(2.5, 1.1, "面積 = 力所做的功 $W$", ha="center", color=F.BLUE, fontsize=12)
    ax1.set_title("變力作功：$F$–$x$ 圖下的面積")
    ax1.set_xlabel("位置 $x$ (m)")
    ax1.set_ylabel("力 $F$ (N)")
    ax1.set_xlim(0, 5)
    ax1.set_ylim(0, 3.6)
    F.clean_grid(ax1)

    # 右：彈簧 F=kx 三角形
    xs = np.linspace(0, 4, 100)
    k = 0.8
    ax2.plot(xs, k * xs, color=F.RED, lw=2.6)
    ax2.fill_between(xs, 0, k * xs, color=F.RED, alpha=0.12)
    # 三角形邊
    ax2.plot([4, 4], [0, k * 4], color=F.INK, lw=1.0, ls="--")
    ax2.text(2.0, 0.55, r"$W=\frac{1}{2} kx^2$", ha="center", color=F.RED, fontsize=14)
    ax2.text(2.6, 3.05, r"$F=kx$", color=F.RED, fontsize=13, rotation=22)
    ax2.annotate(
        r"底 $=x$，高 $=kx$",
        xy=(3.3, k * 3.3),
        xytext=(0.4, 3.0),
        color=F.INK,
        fontsize=11,
        arrowprops=dict(arrowstyle="->", color=F.INK),
    )
    ax2.set_title("彈簧的彈力：三角形面積")
    ax2.set_xlabel("伸長量 $x$ (m)")
    ax2.set_ylabel("彈力 $F=kx$ (N)")
    ax2.set_xlim(0, 5)
    ax2.set_ylim(0, 3.8)
    F.clean_grid(ax2)

    fig.tight_layout()
    F.save_to(fig, CH, "選物II-2-變力作功")


def fig_mechanical_energy():
    """力學能守恆：軌道上 K 與 U 互換，總和不變（雲霄飛車示意）。"""
    fig, ax = F.schematic(8.4, 5.0)

    # 軌道：起點最高(A) → 谷底(B) → 次高(C)，全程落在視窗內
    def yval(xx):
        return 0.9 + 2.6 * np.cos(0.42 * xx) ** 2

    x = np.linspace(0, 8.2, 400)
    ax.plot(x, yval(x), color=F.INK, lw=2.8, zorder=2)
    ax.plot([0, 8.2], [0, 0], color="#999", lw=1.0, ls=":")

    # 三個取樣位置（谷底 B 在 cos=0 處）
    xB = np.pi / 2 / 0.42
    pts = {"A": 0.0, "B": xB, "C": 2 * xB}
    hmax = yval(0.0)  # 起點高度 → 對應最大位能
    Utop = 3.4  # 把 hmax 對應到的位能高度
    Etot = 3.4  # 力學能（總高，定值）；起點靜止 K=0
    bar_w = 0.6
    base = -2.3  # 能量條底線

    for name, xx in pts.items():
        h = yval(xx)
        # 小球放在軌道上
        ax.add_patch(
            Circle((xx, h + 0.20), 0.17, color=F.AMBER, zorder=6, ec=F.INK, lw=1.0)
        )
        # 位能正比於高度；動能 = 總力學能 − 位能
        U = Utop * h / hmax
        Kp = Etot - U
        ax.add_patch(
            Rectangle(
                (xx - bar_w / 2, base),
                bar_w,
                U,
                facecolor=F.RED,
                alpha=0.55,
                ec=F.INK,
                lw=0.9,
                zorder=4,
            )
        )
        ax.add_patch(
            Rectangle(
                (xx - bar_w / 2, base + U),
                bar_w,
                Kp,
                facecolor=F.BLUE,
                alpha=0.55,
                ec=F.INK,
                lw=0.9,
                zorder=4,
            )
        )
        ax.text(xx, base - 0.32, name, ha="center", color=F.INK, fontsize=13)

    # 「力學能（總高）」參考虛線：三條能量條頂端齊平
    ax.plot(
        [pts["A"] - 0.7, pts["C"] + 0.7],
        [base + Etot, base + Etot],
        color=F.INK,
        lw=1.2,
        ls="--",
        zorder=5,
    )
    ax.text(
        pts["C"] + 0.8,
        base + Etot,
        "力學能\n$K+U$（定值）",
        va="center",
        ha="left",
        color=F.INK,
        fontsize=11,
    )

    # 圖例
    lx, ly = 5.7, 4.3
    ax.add_patch(
        Rectangle((lx, ly), 0.36, 0.36, facecolor=F.BLUE, alpha=0.55, ec=F.INK, lw=0.8)
    )
    ax.text(lx + 0.5, ly + 0.18, "動能 $K$", va="center", color=F.INK, fontsize=11)
    ax.add_patch(
        Rectangle(
            (lx, ly - 0.6), 0.36, 0.36, facecolor=F.RED, alpha=0.55, ec=F.INK, lw=0.8
        )
    )
    ax.text(lx + 0.5, ly - 0.42, "位能 $U$", va="center", color=F.INK, fontsize=11)

    ax.text(
        xB,
        base - 1.05,
        "高處 $U$ 大、$K$ 小；谷底 $K$ 大、$U$ 小；三處總高相同",
        ha="center",
        color=F.INK,
        fontsize=12,
    )
    ax.set_title("力學能守恆：$K$ 與 $U$ 互換，總和不變", fontsize=14)
    ax.set_xlim(-1.0, 8.6)
    ax.set_ylim(-3.8, 4.9)
    F.save_to(fig, CH, "選物II-2-力學能守恆")


def fig_conservative():
    """保守 vs 非保守力：左為重力（與路徑無關），右為摩擦（力學能沿路遞減）。"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.6, 4.4))
    ax1.set_aspect("equal")
    ax1.axis("off")
    ax2.axis("off")

    # 左：兩條不同路徑，從 A 到 B，重力做功相同
    A = np.array([0.4, 0.4])
    B = np.array([3.6, 2.6])
    ax1.add_patch(Circle(A, 0.1, color=F.INK))
    ax1.text(A[0] - 0.1, A[1] - 0.35, "A", fontsize=12, ha="center")
    ax1.add_patch(Circle(B, 0.1, color=F.INK))
    ax1.text(B[0] + 0.2, B[1] + 0.15, "B", fontsize=12)
    # 路徑 1：直線
    ax1.add_patch(
        FancyArrowPatch(
            A,
            B,
            arrowstyle="-|>",
            mutation_scale=16,
            color=F.BLUE,
            lw=2.4,
            shrinkA=6,
            shrinkB=6,
        )
    )
    ax1.text(1.6, 1.8, "路徑①", color=F.BLUE, fontsize=11, rotation=33)
    # 路徑 2：折線（先上後右）
    t = np.linspace(0, 1, 100)
    px = A[0] + (B[0] - A[0]) * t
    py = A[1] + (B[1] - A[1]) * (np.sin(np.pi * t) * 0.5 + t)
    py = A[1] + (B[1] - A[1]) * t + 0.9 * np.sin(np.pi * t)
    ax1.plot(px, py, color=F.GREEN, lw=2.4)
    ax1.add_patch(
        FancyArrowPatch(
            (px[-2], py[-2]),
            (px[-1], py[-1]),
            arrowstyle="-|>",
            mutation_scale=16,
            color=F.GREEN,
            lw=2.4,
        )
    )
    ax1.text(2.7, 3.05, "路徑②", color=F.GREEN, fontsize=11)
    # 重力箭頭
    F.arrow(ax1, (3.9, 2.0), (3.9, 1.0), color=F.RED, lw=2.0)
    ax1.text(4.05, 1.5, "$mg$", color=F.RED, fontsize=12, va="center")
    ax1.text(
        2.0,
        -0.35,
        "保守力（重力）：\n兩路徑做的功相同，只看高度差",
        ha="center",
        color=F.INK,
        fontsize=12,
    )
    ax1.set_title("保守力：功與路徑無關", fontsize=13)
    ax1.set_xlim(-0.3, 4.6)
    ax1.set_ylim(-0.9, 3.7)

    # 右：力學能沿路遞減（摩擦把力學能轉成熱）
    s = np.linspace(0, 6, 200)
    Etot = 5.0 - 0.55 * s  # 力學能線性下降
    ax2.plot(s, Etot, color=F.AMBER, lw=2.8)
    ax2.fill_between(s, Etot, 5.0, color=F.AMBER, alpha=0.12)
    ax2.plot([0, 6], [5.0, 5.0], color="#999", lw=1.2, ls="--")
    ax2.text(3.0, 5.2, "若無摩擦：力學能不變", color="#666", fontsize=11, ha="center")
    ax2.annotate(
        "摩擦做負功\n力學能→熱",
        xy=(4.5, 5.0 - 0.55 * 4.5),
        xytext=(2.2, 1.2),
        color=F.AMBER,
        fontsize=11,
        ha="center",
        arrowprops=dict(arrowstyle="->", color=F.AMBER),
    )
    ax2.set_xlim(0, 6.4)
    ax2.set_ylim(0, 6.0)
    ax2.annotate(
        "",
        xy=(6.4, 0),
        xytext=(0, 0),
        arrowprops=dict(arrowstyle="->", color=F.INK, lw=1.3),
    )
    ax2.annotate(
        "",
        xy=(0, 6.0),
        xytext=(0, 0),
        arrowprops=dict(arrowstyle="->", color=F.INK, lw=1.3),
    )
    ax2.text(6.3, -0.35, "滑行距離", ha="right", color=F.INK, fontsize=11)
    ax2.text(0.1, 5.9, "力學能 $K+U$", color=F.INK, fontsize=11)
    ax2.set_title("非保守力：力學能沿路遞減", fontsize=13)

    fig.tight_layout()
    F.save_to(fig, CH, "選物II-2-保守非保守")


def fig_closed_loop():
    """保守力判準 2：封閉路徑功為零。去程功與回程功大小相等、正負相消。
    以矩形封閉迴路（對應例題 2-8b）為例，標出四段重力做的功。"""
    fig, ax = F.schematic(7.6, 5.0)

    # 矩形迴路四個角（起點 P 在左下）
    P = np.array([0.0, 0.0])
    Q = np.array([0.0, 2.4])  # 上升段終點
    Rr = np.array([3.4, 2.4])  # 第一水平段終點
    S = np.array([3.4, 0.0])  # 下降段終點

    # 重力（恆向下）參考箭頭
    F.arrow(ax, (5.2, 1.7), (5.2, 0.7), color=F.RED, lw=2.2)
    ax.text(5.35, 1.2, r"$mg$", color=F.RED, fontsize=13, va="center")

    # 四段路徑（依箭頭方向 P→Q→R→S→P 繞一圈）
    seg = dict(color=F.BLUE, lw=2.6, mutation=18, z=4)
    # 上升段 P→Q：重力做負功
    F.arrow(ax, P + [0, 0.12], Q - [0, 0.12], **seg)
    # 第一水平段 Q→R：重力做零功
    F.arrow(
        ax, Q + [0.12, 0], Rr - [0.12, 0], color="#6b7280", lw=2.6, mutation=18, z=4
    )
    # 下降段 R→S：重力做正功
    F.arrow(ax, Rr - [0, 0.12], S + [0, 0.12], color=F.GREEN, lw=2.6, mutation=18, z=4)
    # 第二水平段 S→P：重力做零功
    F.arrow(ax, S - [0.12, 0], P + [0.12, 0], color="#6b7280", lw=2.6, mutation=18, z=4)

    # 四角端點
    for pt, nm, dx, dy, hav in [
        (P, "P（起點）", -0.12, -0.34, "right"),
        (Q, "Q", -0.18, 0.0, "right"),
        (Rr, "R", 0.18, 0.0, "left"),
        (S, "S", 0.12, -0.34, "left"),
    ]:
        ax.add_patch(Circle(pt, 0.08, color=F.INK, zorder=6))
        ax.text(
            pt[0] + dx, pt[1] + dy, nm, color=F.INK, fontsize=12, ha=hav, va="center"
        )

    # 每段做功標註
    ax.text(
        -0.25,
        1.2,
        "上升段\n$W_1=-mgh<0$",
        color=F.BLUE,
        fontsize=11,
        ha="right",
        va="center",
    )
    ax.text(1.7, 2.62, "水平段　$W_2=0$", color="#6b7280", fontsize=11, ha="center")
    ax.text(
        3.6,
        1.2,
        "下降段\n$W_3=+mgh>0$",
        color=F.GREEN,
        fontsize=11,
        ha="left",
        va="center",
    )
    ax.text(1.7, -0.34, "水平段　$W_4=0$", color="#6b7280", fontsize=11, ha="center")

    # 結論：去程與回程相消
    ax.text(
        1.7,
        3.5,
        r"$W_{\rm net}=W_1+W_2+W_3+W_4=(-mgh)+0+(+mgh)+0=0$",
        color=F.INK,
        fontsize=13,
        ha="center",
    )
    ax.text(
        1.7,
        -1.15,
        "繞封閉迴路一圈回到起點：上升段的負功與下降段的正功大小相等、正負相消，總功為零",
        color=F.INK,
        fontsize=11,
        ha="center",
    )

    ax.set_title("保守力判準②：封閉路徑做功為零（去程／回程功相消）", fontsize=13)
    ax.set_xlim(-2.2, 5.8)
    ax.set_ylim(-1.6, 3.9)
    F.save_to(fig, CH, "選物II-2-封閉路徑功為零")


def fig_pe_zero():
    """重力位能可正可負：以一把鉛直「位能尺」呈現零點上方 U>0、下方 U<0。"""
    fig, ax = F.schematic(7.2, 5.2)

    x0 = 0.0  # 尺的水平位置
    y_zero = 0.0  # 零點所在高度
    top, bot = 2.7, -2.7

    # 上方（U>0）與下方（U<0）色帶
    ax.add_patch(
        Rectangle(
            (x0 - 0.28, y_zero),
            0.56,
            top,
            facecolor=F.BLUE,
            alpha=0.12,
            ec="none",
            zorder=1,
        )
    )
    ax.add_patch(
        Rectangle(
            (x0 - 0.28, bot),
            0.56,
            -bot,
            facecolor=F.RED,
            alpha=0.12,
            ec="none",
            zorder=1,
        )
    )

    # 尺身與零點線
    ax.plot([x0, x0], [bot, top], color=F.INK, lw=2.0, zorder=3)
    ax.plot(
        [x0 - 1.7, x0 + 2.6], [y_zero, y_zero], color=F.INK, lw=1.6, ls="--", zorder=3
    )
    ax.text(
        x0 - 1.75,
        y_zero,
        "零點\n$h=0$，$U_g=0$",
        color=F.INK,
        fontsize=11,
        ha="right",
        va="center",
    )

    # 刻度
    for h in [-2, -1, 1, 2]:
        ax.plot([x0 - 0.14, x0 + 0.14], [h, h], color=F.INK, lw=1.2, zorder=4)

    # 上方物體：h>0、U>0
    yA = 2.0
    ax.add_patch(
        Rectangle(
            (x0 + 0.5, yA - 0.22),
            0.5,
            0.44,
            facecolor="#dbe7ff",
            ec=F.INK,
            lw=1.4,
            zorder=5,
        )
    )
    F.arrow(ax, (x0 + 0.28, yA), (x0 + 0.46, yA), color=F.INK, lw=1.4, mutation=12)
    ax.text(
        x0 + 1.15,
        yA,
        "零點上方：$h>0$，$U_g=mgh>0$",
        color=F.BLUE,
        fontsize=12,
        ha="left",
        va="center",
    )

    # 下方物體：h<0、U<0
    yB = -2.0
    ax.add_patch(
        Rectangle(
            (x0 + 0.5, yB - 0.22),
            0.5,
            0.44,
            facecolor="#ffe0e0",
            ec=F.INK,
            lw=1.4,
            zorder=5,
        )
    )
    F.arrow(ax, (x0 + 0.28, yB), (x0 + 0.46, yB), color=F.INK, lw=1.4, mutation=12)
    ax.text(
        x0 + 1.15,
        yB,
        "零點下方：$h<0$，$U_g=mgh<0$",
        color=F.RED,
        fontsize=12,
        ha="left",
        va="center",
    )

    # 高度座標方向
    F.arrow(ax, (x0 - 1.2, -1.6), (x0 - 1.2, 1.6), color="#6b7280", lw=1.6, mutation=14)
    ax.text(
        x0 - 1.35,
        1.7,
        "高度座標 $h$",
        color="#6b7280",
        fontsize=11,
        ha="center",
        va="bottom",
    )

    ax.text(
        0.45,
        -3.35,
        "零點可任意選；換零點只改變各處位能的數值，不改變物理上有意義的位能差",
        color=F.INK,
        fontsize=11,
        ha="center",
    )
    ax.set_title("重力位能可正可負：零點上方為正、下方為負", fontsize=13)
    ax.set_xlim(-2.6, 4.6)
    ax.set_ylim(-3.7, 3.4)
    F.save_to(fig, CH, "選物II-2-重力位能正負")


if __name__ == "__main__":
    fig_work_definition()
    fig_variable_force()
    fig_mechanical_energy()
    fig_conservative()
    fig_closed_loop()
    fig_pe_zero()
    print("done.")
