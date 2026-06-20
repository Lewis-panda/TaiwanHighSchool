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


def fig_xt():
    """如何讀 x–t 圖：水平段＝靜止、斜率正負＝方向、凹凸＝加速度正負、兩線交點＝相遇。"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.8, 4.2))

    # ── 左：一個物體的 x–t 圖，依序示範四種判讀 ──
    # 分段建構：等速上升 → 水平靜止 → 加速（凹上）→ 減速回頭（凹下、斜率轉負）
    seg1_t = np.linspace(0.0, 1.6, 60)  # 等速前進（直線、斜率正）
    seg1_x = 1.0 + 1.6 * seg1_t
    x_a = seg1_x[-1]
    seg2_t = np.linspace(1.6, 2.8, 50)  # 水平段：靜止
    seg2_x = np.full_like(seg2_t, x_a)
    seg3_t = np.linspace(2.8, 4.4, 60)  # 凹口朝上：速度漸增（a>0）
    seg3_x = x_a + 0.9 * (seg3_t - 2.8) ** 2
    x_b = seg3_x[-1]
    v_b = 2 * 0.9 * (4.4 - 2.8)  # 進入第四段的斜率（連續）
    seg4_t = np.linspace(4.4, 6.4, 70)  # 凹口朝下：速度漸減、過頂點後斜率轉負
    seg4_x = x_b + v_b * (seg4_t - 4.4) - 0.85 * (seg4_t - 4.4) ** 2

    ax1.plot(seg1_t, seg1_x, color=F.BLUE, lw=2.8, zorder=5)
    ax1.plot(seg2_t, seg2_x, color=F.AMBER, lw=2.8, zorder=5)
    ax1.plot(seg3_t, seg3_x, color=F.GREEN, lw=2.8, zorder=5)
    ax1.plot(seg4_t, seg4_x, color=F.RED, lw=2.8, zorder=5)

    # 四個判讀標註
    ax1.annotate(
        "斜率正\n往正方向",
        xy=(0.8, 1.0 + 1.6 * 0.8),
        xytext=(0.15, 7.4),
        color=F.BLUE,
        fontsize=10.5,
        ha="left",
        va="center",
        arrowprops=dict(arrowstyle="->", color=F.BLUE, lw=1.3),
    )
    ax1.annotate(
        "水平段\n靜止",
        xy=(2.2, x_a),
        xytext=(1.55, 8.6),
        color=F.AMBER,
        fontsize=10.5,
        ha="center",
        va="center",
        arrowprops=dict(arrowstyle="->", color=F.AMBER, lw=1.3),
    )
    ax1.annotate(
        "凹口朝上\n加速 a>0",
        xy=(3.9, x_a + 0.9 * (3.9 - 2.8) ** 2),
        xytext=(2.95, 9.3),
        color=F.GREEN,
        fontsize=10.5,
        ha="left",
        va="center",
        arrowprops=dict(arrowstyle="->", color=F.GREEN, lw=1.3),
    )
    # 第四段頂點（斜率為零、離原點最遠）
    t_top = 4.4 + v_b / (2 * 0.85)
    x_top = x_b + v_b * (t_top - 4.4) - 0.85 * (t_top - 4.4) ** 2
    ax1.plot([t_top], [x_top], "o", color=F.INK, ms=6, zorder=7)
    ax1.annotate(
        "頂點：斜率=0\n離原點最遠（非速度最大）",
        xy=(t_top, x_top),
        xytext=(3.05, 1.0),
        color=F.INK,
        fontsize=9.5,
        ha="left",
        va="center",
        arrowprops=dict(arrowstyle="->", color=F.INK, lw=1.2),
    )
    ax1.annotate(
        "凹口朝下\n減速 a<0",
        xy=(5.9, x_b + v_b * (5.9 - 4.4) - 0.85 * (5.9 - 4.4) ** 2),
        xytext=(5.0, 9.3),
        color=F.RED,
        fontsize=10.5,
        ha="left",
        va="center",
        arrowprops=dict(arrowstyle="->", color=F.RED, lw=1.3),
    )

    ax1.set_xlim(0, 6.6)
    ax1.set_ylim(0, 10.2)
    ax1.set_xlabel("時間 $t$ (s)")
    ax1.set_ylabel("位置 $x$ (m)")
    ax1.set_title("一張 x–t 圖怎麼讀")
    F.clean_grid(ax1)

    # ── 右：兩條 x–t 線的交點＝相遇 ──
    t = np.linspace(0, 6, 200)
    # A：等速（直線）
    xA = 1.0 + 1.3 * t
    # B：起步較後、速度較快（直線），與 A 交於某時刻
    xB = 7.5 - 0.9 * t
    ax2.plot(t, xA, color=F.BLUE, lw=2.8, zorder=5, label="物體 A")
    ax2.plot(t, xB, color=F.RED, lw=2.8, zorder=5, label="物體 B")
    # 交點
    t_meet = (7.5 - 1.0) / (1.3 + 0.9)
    x_meet = 1.0 + 1.3 * t_meet
    ax2.plot([t_meet], [x_meet], "o", color=F.INK, ms=8, zorder=7)
    ax2.plot([t_meet, t_meet], [0, x_meet], color=F.INK, lw=1.0, ls="--", zorder=3)
    ax2.annotate(
        "交點：同一時刻\n位置相同 → 相遇",
        xy=(t_meet, x_meet),
        xytext=(t_meet + 0.4, x_meet + 2.3),
        color=F.INK,
        fontsize=11,
        ha="left",
        va="center",
        arrowprops=dict(arrowstyle="->", color=F.INK, lw=1.3),
    )
    ax2.text(
        0.2, 1.0 + 1.3 * 0.2 - 0.6, "A", color=F.BLUE, fontsize=13, fontweight="bold"
    )
    ax2.text(
        0.2, 7.5 - 0.9 * 0.2 + 0.3, "B", color=F.RED, fontsize=13, fontweight="bold"
    )
    ax2.text(
        t_meet, -0.55, "相遇時刻", color=F.INK, fontsize=10.5, ha="center", va="top"
    )

    ax2.set_xlim(0, 6.2)
    ax2.set_ylim(0, 10.2)
    ax2.set_xlabel("時間 $t$ (s)")
    ax2.set_ylabel("位置 $x$ (m)")
    ax2.set_title("兩條 x–t 線的交點＝相遇")
    F.clean_grid(ax2)

    fig.tight_layout()
    F.save_to(fig, CH, "選物I-2-xt圖")


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


def fig_uptoss_vt():
    """鉛直上拋的 v–t 圖：由 +v0 線性降到 -v0，過零點＝最高點。
    上方面積（上升、正位移）與下方面積（下降、負位移）大小相等 → 回到拋出點位移為零、
    路程為兩塊絕對值相加。同時示意 v–t 圖的「上方正面積、下方負面積」規則。"""
    fig, ax = F.canvas(6.6, 4.6)
    g = 10.0
    v0 = 20.0
    tT = 2 * v0 / g  # 回到拋出點總時間 = 4 s
    t = np.linspace(0, tT, 200)
    v = v0 - g * t

    # 上升段（v>0，時間軸上方）填正面積；下降段（v<0，下方）填負面積
    up = t <= v0 / g
    ax.fill_between(t[up], 0, v[up], color=F.BLUE, alpha=0.16, zorder=1)
    ax.fill_between(t[~up], 0, v[~up], color=F.RED, alpha=0.16, zorder=1)
    ax.plot(t, v, color=F.INK, lw=2.8, zorder=5)

    # 零軸
    ax.axhline(0, color=F.INK, lw=1.0, zorder=2)

    # 最高點（過零點）
    t_top = v0 / g
    ax.plot([t_top], [0], "o", color=F.AMBER, ms=8, zorder=6)
    ax.annotate(
        "最高點 v=0\n（過零點，a=-g 不變）",
        xy=(t_top, 0),
        xytext=(t_top + 0.15, 9.5),
        color=F.AMBER,
        fontsize=11,
        ha="left",
        va="center",
        arrowprops=dict(arrowstyle="->", color=F.AMBER, lw=1.3),
    )

    # 起點與終點速度標註
    ax.plot([0], [v0], "o", color=F.BLUE, ms=6, zorder=6)
    ax.plot([tT], [-v0], "o", color=F.RED, ms=6, zorder=6)
    ax.text(-0.08, v0, "$+v_0$", ha="right", va="center", color=F.BLUE, fontsize=12)
    ax.text(tT + 0.08, -v0, "$-v_0$", ha="left", va="center", color=F.RED, fontsize=12)

    # 兩塊面積標註
    ax.text(
        t_top * 0.42,
        v0 * 0.30,
        "上升段\n上方面積\n（正位移）",
        ha="center",
        va="center",
        color=F.BLUE,
        fontsize=10.5,
    )
    ax.text(
        t_top + (tT - t_top) * 0.62,
        -v0 * 0.32,
        "下降段\n下方面積\n（負位移）",
        ha="center",
        va="center",
        color=F.RED,
        fontsize=10.5,
    )

    # 對稱說明
    ax.text(
        tT / 2,
        -v0 - 4.5,
        "兩塊面積大小相等 → 回到拋出點位移為零；路程＝兩塊絕對值相加",
        ha="center",
        va="center",
        color="#555",
        fontsize=10,
    )

    ax.set_xlim(-0.4, tT + 0.7)
    ax.set_ylim(-v0 - 7, v0 + 4)
    ax.set_xlabel("時間 $t$ (s)")
    ax.set_ylabel("速度 $v$ (m/s)")
    ax.set_title("鉛直上拋的 v–t 圖（$v_0=20$ m/s, $g=10$ m/s$^2$）", fontsize=13)
    F.clean_grid(ax)
    fig.tight_layout()
    F.save_to(fig, CH, "選物I-2-上拋vt圖")


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
    fig_xt()
    fig_freefall()
    fig_uptoss_vt()
    fig_relative()
    print("done.")
