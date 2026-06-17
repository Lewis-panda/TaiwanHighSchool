# -*- coding: utf-8 -*-
"""產生「選物II-3 牛頓運動定律的應用」的圖，輸出到該章 sources/。
重繪：  .venv/bin/python _tools/fig_選物II-3.py
"""

import os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon, Arc, Circle, FancyArrowPatch
import figlib as F

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CH = os.path.join(
    ROOT,
    "物理",
    "物理二下（選修物理II·力學二，僅力學）",
    "選物II-3 牛頓運動定律的應用",
)


def fig_static_equilibrium():
    """剛體平衡：水平招牌桿，左端鉸接於牆、右端以斜繩懸吊。
    展示兩條件——合力為零、合力矩為零（對支點取矩）。"""
    fig, ax = F.schematic(7.2, 5.0)

    # 牆
    ax.add_patch(
        Rectangle(
            (-4.0, -2.6),
            0.5,
            5.4,
            facecolor="#eef1f5",
            edgecolor=F.INK,
            hatch="\\\\\\",
            lw=1.4,
        )
    )
    ax.plot([-3.5, -3.5], [-2.6, 2.8], color=F.INK, lw=1.8)

    # 招牌桿（水平）
    P = np.array([-3.5, 0.0])  # 支點（鉸接，pivot）
    Q = np.array([2.6, 0.0])  # 桿右端
    ax.plot([P[0], Q[0]], [0, 0], color=F.INK, lw=4.0, solid_capstyle="round", zorder=3)

    # 支點
    ax.add_patch(Circle(P, 0.16, facecolor="white", edgecolor=F.INK, lw=1.8, zorder=5))
    ax.add_patch(Circle(P, 0.05, color=F.INK, zorder=6))
    F.label(ax, P + np.array([0.05, -0.5]), "支點 O", color=F.INK, fs=12)

    # 斜繩：桿右端 → 牆上方
    Wtop = np.array([-3.5, 2.4])
    ax.plot([Q[0], Wtop[0]], [Q[1], Wtop[1]], color=F.GREEN, lw=2.4, zorder=2)

    # 張力 T（沿繩，從桿右端指向牆上）
    tdir = (Wtop - Q) / np.linalg.norm(Wtop - Q)
    F.arrow(ax, Q, Q + tdir * 2.0, color=F.GREEN, lw=2.6)
    F.label(
        ax,
        Q + tdir * 2.0 + np.array([-0.15, 0.28]),
        r"$T$ 張力",
        color=F.GREEN,
        ha="center",
    )

    # 桿自重 W（作用於桿中點，向下）
    Gc = np.array([(P[0] + Q[0]) / 2, 0.0])
    ax.add_patch(Circle(Gc, 0.06, color=F.INK, zorder=6))
    F.arrow(ax, Gc, Gc + np.array([0, -1.8]), color=F.RED, lw=2.6)
    F.label(ax, Gc + np.array([0.0, -2.1]), r"$W=mg$ 桿重", color=F.RED)

    # 招牌負載 Wsign（掛在右端，向下）
    F.arrow(ax, Q, Q + np.array([0, -2.1]), color=F.RED, lw=2.6, ls="--")
    F.label(ax, Q + np.array([0.05, -2.4]), r"$W_2$ 招牌重", color=F.RED)
    # 簡單招牌示意
    ax.add_patch(
        Rectangle(
            (Q[0] - 0.55, Q[1] - 1.65),
            1.1,
            0.5,
            facecolor="#fff3cd",
            edgecolor=F.INK,
            lw=1.2,
            zorder=2,
        )
    )
    ax.text(Q[0], Q[1] - 1.40, "牌", ha="center", va="center", fontsize=11, color=F.INK)

    # 鉸接反力 R（支點處，方向未知，畫示意）
    F.arrow(ax, P, P + np.array([0.9, 1.4]), color=F.BLUE, lw=2.2)
    F.label(
        ax, P + np.array([1.0, 1.55]), r"$R$ 鉸接反力", color=F.BLUE, ha="left", fs=11
    )

    ax.set_title("剛體平衡：合力 = 0 且 合力矩 = 0（對支點 O 取矩）", fontsize=12.5)
    ax.set_xlim(-4.4, 4.0)
    ax.set_ylim(-3.0, 3.1)
    F.save_to(fig, CH, "選物II-3-靜力平衡")


def fig_torque_lever():
    """力矩與力臂：同一支扳手，三種施力比較力臂 d=r sinθ。"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.6, 4.6))
    for ax in (ax1, ax2):
        ax.set_aspect("equal")
        ax.axis("off")

    # ---- 左：開門俯視，力臂 = 到門軸的垂直距離 ----
    hinge = np.array([0.0, 0.0])
    door_end = np.array([3.4, 0.0])
    # 門板
    ax1.add_patch(
        Rectangle((0, -0.12), 3.4, 0.24, facecolor="#dbe7ff", edgecolor=F.INK, lw=1.6)
    )
    # 門軸
    ax1.add_patch(
        Circle(hinge, 0.14, facecolor="white", edgecolor=F.INK, lw=1.8, zorder=5)
    )
    ax1.add_patch(Circle(hinge, 0.05, color=F.INK, zorder=6))
    ax1.text(
        hinge[0] - 0.1, hinge[1] - 0.5, "門軸", ha="center", color=F.INK, fontsize=11
    )

    # 推力 A：在門邊垂直推（力臂最大）
    pA = np.array([3.2, 0.0])
    F.arrow(ax1, pA, pA + np.array([0, 1.5]), color=F.BLUE, lw=2.6)
    F.label(ax1, pA + np.array([0.0, 1.75]), r"$F$（推遠端）", color=F.BLUE, fs=11)
    ax1.annotate(
        "",
        xy=(pA[0], 0),
        xytext=(0, 0),
        arrowprops=dict(arrowstyle="<->", color=F.AMBER, lw=1.6),
    )
    ax1.text(1.6, -0.45, r"力臂 $d$（大）", ha="center", color=F.AMBER, fontsize=11)

    # 推力 B：靠近門軸推（力臂小）
    pB = np.array([1.0, 0.0])
    F.arrow(ax1, pB, pB + np.array([0, 1.1]), color="#9aa4b2", lw=2.2)
    F.label(ax1, pB + np.array([0.0, 1.32]), "靠軸推（費力）", color="#6b7280", fs=10)

    ax1.set_title(r"開門：$\tau=F\,d$，推越遠越省力", fontsize=12.5)
    ax1.set_xlim(-0.8, 4.0)
    ax1.set_ylim(-1.0, 2.4)

    # ---- 右：扳手，力與位置向量夾角 θ，力臂 d=r sinθ ----
    O = np.array([0.0, 0.0])  # 螺帽（轉軸）
    handle = np.array([3.0, 0.6])  # 施力點
    # 扳手柄
    ax2.plot(
        [O[0], handle[0]],
        [O[1], handle[1]],
        color=F.INK,
        lw=5.0,
        solid_capstyle="round",
        zorder=2,
    )
    ax2.add_patch(
        Circle(O, 0.22, facecolor="#eef1f5", edgecolor=F.INK, lw=1.8, zorder=4)
    )
    ax2.add_patch(
        Polygon(
            [
                O + np.array([0.16, 0.10]),
                O + np.array([0.0, 0.22]),
                O + np.array([-0.16, 0.10]),
                O + np.array([-0.16, -0.10]),
                O + np.array([0.0, -0.22]),
                O + np.array([0.16, -0.10]),
            ],
            closed=True,
            facecolor="white",
            edgecolor=F.INK,
            lw=1.4,
            zorder=5,
        )
    )
    ax2.text(O[0], O[1] - 0.55, "螺帽", ha="center", color=F.INK, fontsize=11)

    # 位置向量 r
    rdir = (handle - O) / np.linalg.norm(handle - O)
    F.label(ax2, (O + handle) / 2 + np.array([0.0, 0.42]), r"$r$", color=F.INK, fs=13)

    # 施力 F（與柄夾角 θ）
    Fdir = np.array([np.cos(np.deg2rad(115)), np.sin(np.deg2rad(115))])
    F.arrow(ax2, handle, handle + Fdir * 1.8, color=F.BLUE, lw=2.6)
    F.label(
        ax2, handle + Fdir * 1.8 + np.array([0.1, 0.2]), r"$F$", color=F.BLUE, fs=13
    )

    # 力臂 d = r sinθ：自轉軸對力的作用線作垂線
    # 力作用線：過 handle，方向 Fdir
    # 垂足 = O 在該直線上的投影
    AP = O - handle
    t = np.dot(AP, Fdir)
    foot = handle + Fdir * t
    ax2.plot(
        [handle[0], handle[0] + Fdir[0] * 2.6],
        [handle[1], handle[1] + Fdir[1] * 2.6],
        color=F.GRID,
        lw=1.2,
        ls="--",
        zorder=1,
    )
    ax2.plot([O[0], foot[0]], [O[1], foot[1]], color=F.AMBER, lw=2.0, zorder=3)
    F.label(
        ax2,
        (O + foot) / 2 + np.array([-0.25, -0.05]),
        r"力臂 $d=r\sin\theta$",
        color=F.AMBER,
        fs=11,
        ha="right",
    )

    # 夾角 θ
    ax2.add_patch(
        Arc(
            handle,
            1.0,
            1.0,
            angle=0,
            theta1=np.rad2deg(np.arctan2(-rdir[1], -rdir[0])),
            theta2=115,
            color=F.INK,
            lw=1.4,
        )
    )
    ax2.text(handle[0] - 0.55, handle[1] + 0.42, r"$\theta$", color=F.INK, fontsize=13)

    ax2.set_title(r"扳手：$\tau=r\,F\sin\theta=F\,d$", fontsize=12.5)
    ax2.set_xlim(-1.4, 3.8)
    ax2.set_ylim(-1.0, 2.6)

    fig.tight_layout()
    F.save_to(fig, CH, "選物II-3-力矩力臂")


def fig_stability():
    """重心穩定性與傾倒：傾斜的櫃子，比較重心鉛垂線落在/落出支撐底面。"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.6, 5.0))
    for ax in (ax1, ax2):
        ax.set_aspect("equal")
        ax.axis("off")

    def draw_box(ax, tilt_deg, title, stable):
        th = np.deg2rad(tilt_deg)
        # 地面
        ax.plot([-3.2, 3.2], [0, 0], color=F.INK, lw=2.0)
        ax.add_patch(
            Rectangle(
                (-3.2, -0.45),
                6.4,
                0.45,
                facecolor="#eef1f5",
                edgecolor="none",
                hatch="////",
                lw=0,
            )
        )
        # 箱子（繞右下角 pivot 旋轉）
        w, h = 1.6, 2.8
        pivot = np.array([0.8, 0.0])  # 旋轉支點（右下角）
        # 未旋轉時四角（相對 pivot）
        corners0 = np.array([[-w, 0], [0, 0], [0, h], [-w, h]], dtype=float)
        R = np.array([[np.cos(th), -np.sin(th)], [np.sin(th), np.cos(th)]])
        corners = (corners0 @ R.T) + pivot
        ax.add_patch(
            Polygon(
                corners,
                closed=True,
                facecolor="#dbe7ff",
                edgecolor=F.INK,
                lw=1.8,
                zorder=3,
            )
        )
        # 重心（幾何中心）
        Gc0 = np.array([-w / 2, h / 2])
        Gc = Gc0 @ R.T + pivot
        ax.add_patch(
            Circle(Gc, 0.10, facecolor="white", edgecolor=F.RED, lw=1.8, zorder=6)
        )
        ax.plot(
            [Gc[0] - 0.07, Gc[0] + 0.07],
            [Gc[1] - 0.07, Gc[1] + 0.07],
            color=F.RED,
            lw=1.4,
            zorder=7,
        )
        ax.plot(
            [Gc[0] - 0.07, Gc[0] + 0.07],
            [Gc[1] + 0.07, Gc[1] - 0.07],
            color=F.RED,
            lw=1.4,
            zorder=7,
        )
        F.label(ax, Gc + np.array([0.32, 0.1]), "重心", color=F.RED, fs=11, ha="left")

        # 重力（向下）
        F.arrow(ax, Gc, Gc + np.array([0, -1.3]), color=F.RED, lw=2.4)
        # 重心鉛垂線（虛線到地面）
        ax.plot([Gc[0], Gc[0]], [Gc[1], 0], color=F.RED, lw=1.3, ls=":", zorder=4)
        ax.add_patch(Circle((Gc[0], 0), 0.07, color=F.RED, zorder=6))

        # 支撐底面（左下角到 pivot）
        base_left = corners[0]
        ax.plot(
            [base_left[0], pivot[0]],
            [0, 0],
            color=F.GREEN,
            lw=4.0,
            solid_capstyle="butt",
            zorder=5,
        )
        F.label(
            ax,
            np.array([(base_left[0] + pivot[0]) / 2, -0.65]),
            "支撐底面",
            color=F.GREEN,
            fs=11,
        )
        # pivot 標記
        ax.add_patch(Circle(pivot, 0.06, color=F.INK, zorder=8))

        # 判斷文字
        if stable:
            msg = "重心鉛垂線落在底面內\n→ 回正（穩定）"
            col = F.GREEN
        else:
            msg = "重心鉛垂線落到底面外\n→ 傾倒"
            col = F.RED
        ax.text(
            0.0,
            3.9,
            msg,
            ha="center",
            va="top",
            color=col,
            fontsize=11,
            fontweight="bold",
        )
        ax.set_title(title, fontsize=12.5)
        ax.set_xlim(-3.0, 2.6)
        ax.set_ylim(-0.9, 4.2)

    draw_box(ax1, 14, "傾斜不大", stable=True)
    draw_box(ax2, 38, "傾斜過大", stable=False)

    fig.tight_layout()
    F.save_to(fig, CH, "選物II-3-重心穩定")


def fig_collision():
    """一維碰撞：彈性 vs 完全非彈性，比較碰後速度與動能去向。"""
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8.4, 5.6))
    for ax in (ax1, ax2):
        ax.set_aspect("equal")
        ax.axis("off")
        ax.set_xlim(-0.5, 11.5)
        ax.set_ylim(-1.6, 1.8)

    def block(ax, x, label, color, w=1.1):
        ax.add_patch(
            Rectangle(
                (x - w / 2, -0.5),
                w,
                1.0,
                facecolor=color,
                edgecolor=F.INK,
                lw=1.6,
                zorder=3,
            )
        )
        ax.text(x, 0.0, label, ha="center", va="center", fontsize=12, color=F.INK)

    def vel(ax, x, y, vx, color, lab):
        if abs(vx) < 1e-3:
            ax.text(x, y, "靜止", ha="center", color=color, fontsize=10)
            return
        F.arrow(ax, (x, y), (x + vx, y), color=color, lw=2.4)
        ax.text(x + vx / 2, y + 0.28, lab, ha="center", color=color, fontsize=11)

    # ---- 上：彈性碰撞（等質量對撞 → 交換速度）----
    ax1.text(
        -0.3,
        1.5,
        "彈性碰撞（等質量）",
        ha="left",
        fontsize=13,
        color=F.INK,
        fontweight="bold",
    )
    # 碰前
    ax1.text(0.2, 0.9, "碰前", fontsize=10, color="#6b7280")
    block(ax1, 1.4, "A", "#dbe7ff")
    block(ax1, 4.2, "B", "#ffe3e3")
    vel(ax1, 2.0, 0.0, 1.3, F.BLUE, r"$v$")
    vel(ax1, 4.8, 0.0, 0.0, F.INK, "")
    # 箭頭分隔
    ax1.annotate(
        "",
        xy=(7.0, 0.0),
        xytext=(6.0, 0.0),
        arrowprops=dict(arrowstyle="-|>", color=F.PURPLE, lw=2.0),
    )
    # 碰後
    ax1.text(7.4, 0.9, "碰後", fontsize=10, color="#6b7280")
    block(ax1, 8.0, "A", "#dbe7ff")
    block(ax1, 10.6, "B", "#ffe3e3")
    vel(ax1, 8.0, 0.0, 0.0, F.INK, "")
    vel(ax1, 11.0, 0.0, 1.3, F.BLUE, r"$v$")
    ax1.text(
        5.9,
        -1.25,
        r"動量守恆、動能守恆 → 等質量「交換速度」",
        ha="center",
        color=F.GREEN,
        fontsize=11,
    )

    # ---- 下：完全非彈性（黏在一起）----
    ax2.text(
        -0.3,
        1.5,
        "完全非彈性碰撞（碰後黏一起）",
        ha="left",
        fontsize=13,
        color=F.INK,
        fontweight="bold",
    )
    ax2.text(0.2, 0.9, "碰前", fontsize=10, color="#6b7280")
    block(ax2, 1.4, "A", "#dbe7ff")
    block(ax2, 4.2, "B", "#ffe3e3")
    vel(ax2, 2.0, 0.0, 1.3, F.BLUE, r"$v$")
    vel(ax2, 4.8, 0.0, 0.0, F.INK, "")
    ax2.annotate(
        "",
        xy=(7.0, 0.0),
        xytext=(6.0, 0.0),
        arrowprops=dict(arrowstyle="-|>", color=F.PURPLE, lw=2.0),
    )
    ax2.text(7.4, 0.9, "碰後", fontsize=10, color="#6b7280")
    # 黏在一起
    ax2.add_patch(
        Rectangle(
            (8.4, -0.5),
            2.2,
            1.0,
            facecolor="#e7d8ff",
            edgecolor=F.INK,
            lw=1.6,
            zorder=3,
        )
    )
    ax2.text(9.5, 0.0, "A+B", ha="center", va="center", fontsize=12, color=F.INK)
    vel(ax2, 10.7, 0.0, 0.7, F.BLUE, r"$v/2$")
    ax2.text(
        5.9,
        -1.25,
        r"動量守恆，但動能有損失 → 變成熱、聲、形變",
        ha="center",
        color=F.AMBER,
        fontsize=11,
    )

    fig.tight_layout()
    F.save_to(fig, CH, "選物II-3-一維碰撞")


if __name__ == "__main__":
    fig_static_equilibrium()
    fig_torque_lever()
    fig_stability()
    fig_collision()
    print("done.")
