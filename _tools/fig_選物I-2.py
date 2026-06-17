# -*- coding: utf-8 -*-
"""產生「選物I-2 直線運動」的圖，輸出到該章 sources/。
重繪：  .venv/bin/python _tools/fig_選物I-2.py
"""

import os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon, Arc, Circle, FancyArrowPatch
import figlib as F

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CH = os.path.join(ROOT, "物理", "物理二上（選修物理I·力學一）", "選物I-2 直線運動")


def fig_vt():
    """v–t 圖：斜率＝加速度、梯形面積＝位移。左圖示意斜率與面積，右圖示意瞬時量＝割線→切線。"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.6, 4.0))

    # ── 左：等加速度 v–t 圖，梯形面積＝位移 ──
    t = np.linspace(0, 5, 200)
    v0, a = 2.0, 1.4
    v = v0 + a * t
    ax1.plot(t, v, color=F.RED, lw=2.8, zorder=5)
    # 梯形面積填色
    ax1.fill_between(t, 0, v, color=F.FILL, alpha=0.13)
    # 斜率三角形
    ax1.plot(
        [3.0, 4.0, 4.0],
        [v0 + a * 3.0, v0 + a * 3.0, v0 + a * 4.0],
        color=F.INK,
        lw=1.2,
        ls="--",
    )
    ax1.text(
        3.5, v0 + a * 3.0 - 0.55, r"$\Delta t$", ha="center", color=F.INK, fontsize=12
    )
    ax1.text(4.12, v0 + a * 3.5, r"$\Delta v$", va="center", color=F.INK, fontsize=12)
    ax1.text(
        1.0, 6.6, r"斜率 $=\dfrac{\Delta v}{\Delta t}=a$", color=F.RED, fontsize=13
    )
    ax1.text(2.0, 2.0, "面積 = 位移", ha="center", color=F.BLUE, fontsize=13)
    # 標出 v0 與 v
    ax1.plot([0], [v0], "o", color=F.RED, ms=6, zorder=6)
    ax1.text(-0.12, v0, r"$v_0$", ha="right", va="center", color=F.RED, fontsize=12)
    ax1.set_xlim(0, 5.2)
    ax1.set_ylim(0, 10)
    ax1.set_xlabel("時間 $t$ (s)")
    ax1.set_ylabel("速度 $v$ (m/s)")
    ax1.set_title("等加速度 v–t 圖")
    F.clean_grid(ax1)

    # ── 右：割線→切線（平均→瞬時）──
    tt = np.linspace(0, 5, 200)
    xx = 0.18 * tt**2 + 0.4 * tt  # 一段曲線（x–t）
    ax2.plot(tt, xx, color=F.BLUE, lw=2.8, zorder=5)
    P = 3.5
    xP = 0.18 * P**2 + 0.4 * P
    # 三條割線（割點越來越靠近 P）→ 切線
    for q, col, al in [
        (1.0, "#bcd0f0", 1.0),
        (2.0, "#7aa7e6", 1.0),
        (2.8, "#3f7fd6", 1.0),
    ]:
        xq = 0.18 * q**2 + 0.4 * q
        m = (xP - xq) / (P - q)
        xs = np.array([q - 0.2, P + 0.4])
        ax2.plot(xs, xq + m * (xs - q), color=col, lw=1.6, zorder=3)
        ax2.plot([q], [xq], "o", color=col, ms=5, zorder=4)
    # 切線（瞬時）
    mt = 2 * 0.18 * P + 0.4
    xs = np.array([P - 1.6, P + 0.7])
    ax2.plot(xs, xP + mt * (xs - P), color=F.RED, lw=2.4, zorder=6)
    ax2.plot([P], [xP], "o", color=F.RED, ms=7, zorder=7)
    ax2.text(
        P + 0.15,
        xP - 0.55,
        "切線斜率\n= 瞬時速度",
        color=F.RED,
        fontsize=11,
        ha="left",
        va="top",
    )
    ax2.text(
        0.7,
        4.6,
        "割線斜率\n= 平均速度",
        color="#3f7fd6",
        fontsize=11,
        ha="left",
        va="center",
    )
    ax2.set_xlim(0, 5.2)
    ax2.set_ylim(0, 6.2)
    ax2.set_xlabel("時間 $t$ (s)")
    ax2.set_ylabel("位置 $x$ (m)")
    ax2.set_title("平均 → 瞬時：割線收斂到切線")
    F.clean_grid(ax2)

    fig.tight_layout()
    F.save_to(fig, CH, "選物I-2-vt圖")


def fig_freefall():
    """鉛直上拋：對稱性、最高點 v=0、各點速度等大反向，加速度恆為 g 向下。"""
    fig, ax = F.schematic(6.2, 5.6)
    g = 10.0
    v0 = 20.0
    H = v0**2 / (2 * g)  # = 20 m
    # 拋體沿一條（略偏）的鉛直線；用 x 表示時間先後，y 表示高度
    ts = np.linspace(0, 2 * v0 / g, 200)
    ys = v0 * ts - 0.5 * g * ts**2
    xs = 0.9 * ts  # 水平展開只為了看清楚，物理上是同一條鉛直線
    ax.plot(xs, ys, color=F.INK, lw=1.4, ls=":", zorder=1)

    # 標記點：t = 0,1,2,3,4 s
    marks = [0, 1, 2, 3, 4]
    for tm in marks:
        ym = v0 * tm - 0.5 * g * tm**2
        xm = 0.9 * tm
        vm = v0 - g * tm
        ax.add_patch(
            Circle(
                (xm, ym), 0.32, facecolor="#dbe7ff", edgecolor=F.INK, lw=1.4, zorder=4
            )
        )
        # 速度箭頭（向上正、向下負），長度比例
        if abs(vm) > 0.1:
            dy = 0.07 * vm
            col = F.BLUE if vm > 0 else F.RED
            F.arrow(ax, (xm, ym), (xm, ym + dy), color=col, lw=2.2, mutation=14, z=6)
            ax.text(
                xm + 0.42,
                ym + dy / 2,
                f"$v={abs(vm):.0f}$",
                color=col,
                fontsize=11,
                ha="left",
                va="center",
            )
        else:
            ax.text(
                xm + 0.42,
                ym,
                "$v=0$",
                color=F.AMBER,
                fontsize=12,
                ha="left",
                va="center",
            )
        ax.text(
            xm,
            ym - 0.62,
            f"$t={tm}$ s",
            color=F.INK,
            fontsize=10,
            ha="center",
            va="top",
        )

    # 最高點標註
    ax.text(
        0.9 * 2,
        H + 0.9,
        "最高點 $v=0$\n（但 $a=g$ 仍向下）",
        color=F.AMBER,
        fontsize=11,
        ha="center",
        va="bottom",
    )
    # 重力加速度箭頭（恆向下）
    F.arrow(ax, (4.05, 14), (4.05, 11), color=F.RED, lw=2.6, mutation=18, z=6)
    ax.text(4.2, 12.5, "$g$", color=F.RED, fontsize=14, ha="left", va="center")
    # 對稱虛線：上升 t=1 與下降 t=3 同高、速率相同
    yA = v0 * 1 - 0.5 * g * 1
    ax.plot([0.9 * 1, 0.9 * 3], [yA, yA], color="#999", lw=1.0, ls="--", zorder=2)
    ax.text(
        0.9 * 2,
        yA - 0.05,
        "同高 ⇒ 速率相同、方向相反",
        color="#666",
        fontsize=10,
        ha="center",
        va="top",
    )

    ax.set_xlim(-0.8, 5.2)
    ax.set_ylim(-1.5, 18.5)
    ax.set_title("鉛直上拋：上下對稱（$v_0=20$ m/s, $g=10$ m/s$^2$）", fontsize=13)
    F.save_to(fig, CH, "選物I-2-自由落體")


def fig_relative():
    """一維相對速度：月台上兩列火車，相對速度＝速度之差。"""
    fig, ax = F.schematic(8.4, 4.2)

    def train(x0, y0, w, h, color, label, vlabel, vdir):
        ax.add_patch(
            Rectangle(
                (x0, y0),
                w,
                h,
                facecolor=color,
                edgecolor=F.INK,
                lw=1.6,
                zorder=3,
                alpha=0.9,
            )
        )
        # 車輪
        for wx in (x0 + 0.5, x0 + w - 0.5):
            ax.add_patch(Circle((wx, y0 - 0.12), 0.18, facecolor=F.INK, zorder=4))
        ax.text(
            x0 + w / 2,
            y0 + h / 2,
            label,
            color="white",
            fontsize=12,
            ha="center",
            va="center",
            zorder=5,
            fontweight="bold",
        )
        # 速度箭頭
        ax.annotate(
            "",
            xy=(x0 + w / 2 + vdir * 1.1, y0 + h + 0.55),
            xytext=(x0 + w / 2, y0 + h + 0.55),
            arrowprops=dict(arrowstyle="-|>", color=color, lw=2.6, mutation_scale=20),
        )
        ax.text(
            x0 + w / 2 + vdir * 0.55,
            y0 + h + 1.0,
            vlabel,
            color=color,
            fontsize=12,
            ha="center",
            va="bottom",
        )

    # 月台（地面）
    ax.add_patch(
        Rectangle(
            (-0.3, -0.55),
            11.6,
            0.35,
            facecolor="#eef1f5",
            edgecolor=F.INK,
            hatch="////",
            lw=1.0,
            zorder=1,
        )
    )
    ax.text(
        10.9,
        -0.78,
        "月台（地面參考系）",
        color=F.INK,
        fontsize=11,
        ha="right",
        va="top",
    )

    # A 車（藍，向右 20）
    train(0.6, 0.2, 3.0, 1.1, F.BLUE, "A", r"$v_A=+20$", +1)
    # B 車（綠，向右 12）— 同向
    train(6.6, 0.2, 3.0, 1.1, F.GREEN, "B", r"$v_B=+12$", +1)

    # 相對速度說明
    ax.text(
        5.5,
        3.0,
        r"A 看 B：$v_{B/A}=v_B-v_A=12-20=-8$ m/s（B 相對 A 向左）",
        color=F.INK,
        fontsize=12,
        ha="center",
    )
    ax.text(
        5.5,
        2.45,
        r"B 看 A：$v_{A/B}=v_A-v_B=+8$ m/s（兩者等大反向）",
        color="#666",
        fontsize=11,
        ha="center",
    )

    ax.set_xlim(-0.5, 11.5)
    ax.set_ylim(-1.4, 3.6)
    ax.set_title("一維相對速度：相對速度 = 兩速度之差", fontsize=14)
    F.save_to(fig, CH, "選物I-2-相對速度")


if __name__ == "__main__":
    fig_vt()
    fig_freefall()
    fig_relative()
    print("done.")
