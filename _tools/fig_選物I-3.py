# -*- coding: utf-8 -*-
"""產生「選物I-3 平面運動」的圖，輸出到該章 sources/。
重繪：  .venv/bin/python _tools/fig_選物I-3.py
"""

import os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon, Arc, Circle, FancyArrowPatch
import figlib as F

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CH = os.path.join(ROOT, "物理", "物理二上（選修物理I·力學一）", "選物I-3 平面運動")


def fig_independence():
    """運動獨立性：頻閃示意——水平等速 + 鉛直等加速 = 拋物線。
    上方顯示等時間間隔的球（頻閃），並把各時刻的 x、y 影子投影到兩軸，
    凸顯「水平等距、鉛直越來越大」。"""
    fig, ax = F.schematic(8.2, 5.2)
    g, vx = 10.0, 2.4
    t = np.linspace(0, 1.0, 200)
    X = vx * t
    Y = 4.6 - 0.5 * g * t**2  # 從高處平拋落下
    # 拋物線軌跡
    ax.plot(X, Y, color=F.INK, lw=1.4, ls="--", zorder=2)
    # 頻閃球（等時間間隔）
    ts = np.linspace(0, 1.0, 6)
    xs = vx * ts
    ys = 4.6 - 0.5 * g * ts**2
    for xi, yi in zip(xs, ys):
        ax.add_patch(Circle((xi, yi), 0.12, color=F.BLUE, zorder=5))
        # 鉛直投影（落到地面前的高度）— 紅色虛線
        ax.plot([xi, xi], [yi, -0.55], color=F.RED, lw=0.9, ls=":", zorder=1)
        # 水平投影到上方 x 標尺 — 藍色虛線
        ax.plot([xi, xi], [yi, 5.05], color=F.BLUE, lw=0.9, ls=":", zorder=1)
    # 水平標尺（等距）
    ax.plot([0, xs[-1]], [5.05, 5.05], color=F.BLUE, lw=1.6)
    for xi in xs:
        ax.plot([xi, xi], [5.0, 5.1], color=F.BLUE, lw=1.6)
    F.label(
        ax, (xs[-1] / 2, 5.45), "水平：等時間 → 等間距（等速度）", color=F.BLUE, fs=12
    )
    # 鉛直標尺（越來越密 / 落差越來越大）放右側
    xr = xs[-1] + 0.55
    ax.plot([xr, xr], [ys[0], -0.55], color=F.RED, lw=1.6)
    for yi in ys:
        ax.plot([xr - 0.05, xr + 0.05], [yi, yi], color=F.RED, lw=1.6)
    ax.plot([xr - 0.05, xr + 0.05], [-0.55, -0.55], color=F.RED, lw=1.6)
    ax.text(
        xr + 0.2,
        2.0,
        "鉛直：等時間 → 落差越來越大\n（等加速度，自由落體）",
        color=F.RED,
        fontsize=12,
        ha="left",
        va="center",
        rotation=0,
    )
    # 地面
    ax.add_patch(
        Rectangle(
            (-0.5, -0.85),
            xs[-1] + 1.8,
            0.3,
            facecolor="#eef1f5",
            edgecolor=F.INK,
            hatch="////",
            lw=1.0,
            zorder=0,
        )
    )
    ax.plot([-0.5, xs[-1] + 1.3], [-0.55, -0.55], color=F.INK, lw=1.4)
    ax.set_title("運動獨立性：水平等速 ＋ 鉛直等加速 ＝ 拋物線", fontsize=14)
    ax.set_xlim(-1.2, xs[-1] + 3.3)
    ax.set_ylim(-1.2, 5.9)
    F.save_to(fig, CH, "選物I-3-運動獨立性")


def fig_dropvsproj():
    """平拋對比：同高度，一球平拋、一球自由落下，鉛直方向同步、同時落地。"""
    fig, ax = F.schematic(7.6, 4.8)
    g, vx, H = 10.0, 3.0, 4.2
    ts = np.linspace(0, np.sqrt(2 * H / g), 6)
    # 自由落體球（x 固定）
    x_drop = 0.0
    # 平拋球
    x_proj = vx * ts
    y = H - 0.5 * g * ts**2
    # 平拋軌跡
    tt = np.linspace(0, ts[-1], 100)
    ax.plot(vx * tt, H - 0.5 * g * tt**2, color=F.BLUE, lw=1.3, ls="--", zorder=2)
    # 鉛直落線
    ax.plot([x_drop, x_drop], [H, 0], color=F.RED, lw=1.3, ls="--", zorder=2)
    # 各時刻兩球 + 等高虛線（強調鉛直同步）
    for i, (yi, xpi) in enumerate(zip(y, x_proj)):
        ax.add_patch(Circle((x_drop, yi), 0.13, color=F.RED, zorder=5))
        ax.add_patch(Circle((xpi, yi), 0.13, color=F.BLUE, zorder=5))
        if 0 < i < len(y):
            ax.plot([x_drop, xpi], [yi, yi], color="#9aa0a6", lw=0.8, ls=":", zorder=1)
    # 標籤
    ax.text(x_drop - 0.35, H + 0.25, "自由落下", color=F.RED, ha="center", fontsize=12)
    ax.text(
        x_proj[0] + 0.9, H + 0.25, "水平拋出", color=F.BLUE, ha="center", fontsize=12
    )
    # 地面
    ax.add_patch(
        Rectangle(
            (-1.0, -0.35),
            x_proj[-1] + 2.0,
            0.3,
            facecolor="#eef1f5",
            edgecolor=F.INK,
            hatch="////",
            lw=1.0,
            zorder=0,
        )
    )
    ax.plot([-1.0, x_proj[-1] + 1.0], [-0.05, -0.05], color=F.INK, lw=1.4)
    ax.text(
        (x_proj[-1]) / 2,
        -0.9,
        "兩球的鉛直運動完全相同 → 同時落地",
        ha="center",
        color=F.INK,
        fontsize=12.5,
    )
    ax.set_title("平拋 vs 自由落體：哪個先落地？（同時！）", fontsize=14)
    ax.set_xlim(-1.4, x_proj[-1] + 1.6)
    ax.set_ylim(-1.3, H + 0.9)
    F.save_to(fig, CH, "選物I-3-平拋對比")


def fig_oblique():
    """斜拋分解：左圖初速分量 v0cosθ、v0sinθ；右圖不同角度的軌跡與射程。"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.4, 4.4))
    for ax in (ax1, ax2):
        ax.set_aspect("equal")

    # --- 左：初速分解 ---
    th = np.deg2rad(40)
    v0 = 3.2
    O = np.array([0.0, 0.0])
    V = np.array([v0 * np.cos(th), v0 * np.sin(th)])
    ax1.add_patch(
        Rectangle(
            (-1.2, -0.45),
            6.0,
            0.18,
            facecolor="#eef1f5",
            edgecolor=F.INK,
            hatch="////",
            lw=0.9,
        )
    )
    ax1.plot([-1.2, 4.8], [-0.27, -0.27], color=F.INK, lw=1.3)
    # 初速向量
    F.arrow(ax1, O, V, color=F.PURPLE, lw=2.8)
    F.label(ax1, V + np.array([0.15, 0.2]), r"$v_0$", color=F.PURPLE, fs=15)
    # 水平分量
    F.arrow(ax1, O, np.array([V[0], 0]), color=F.BLUE, lw=2.4)
    ax1.text(
        V[0] / 2,
        -0.32,
        r"$v_0\cos\theta$",
        color=F.BLUE,
        ha="center",
        va="top",
        fontsize=13,
    )
    # 鉛直分量（畫在末端）
    F.arrow(ax1, np.array([V[0], 0]), V, color=F.RED, lw=2.4, ls="-")
    ax1.text(
        V[0] + 0.18,
        V[1] / 2,
        r"$v_0\sin\theta$",
        color=F.RED,
        ha="left",
        va="center",
        fontsize=13,
    )
    ax1.plot([V[0], V[0]], [0, V[1]], color=F.RED, lw=0.8, ls=":")
    # 角
    ax1.add_patch(Arc(O, 1.5, 1.5, angle=0, theta1=0, theta2=40, color=F.INK, lw=1.4))
    ax1.text(0.95, 0.28, r"$\theta$", color=F.INK, fontsize=14)
    ax1.set_title(
        "初速分解：水平 $v_0\\cos\\theta$、鉛直 $v_0\\sin\\theta$", fontsize=12.5
    )
    ax1.set_xlim(-1.3, 5.0)
    ax1.set_ylim(-0.9, 3.2)
    ax1.axis("off")

    # --- 右：不同角度的軌跡（同 v0），標 45° 射程最大 ---
    g, v0r = 10.0, 10.0
    colors = {30: F.GREEN, 45: F.RED, 60: F.BLUE}
    for ang, col in colors.items():
        a = np.deg2rad(ang)
        T = 2 * v0r * np.sin(a) / g
        tt = np.linspace(0, T, 120)
        X = v0r * np.cos(a) * tt
        Y = v0r * np.sin(a) * tt - 0.5 * g * tt**2
        lw = 3.0 if ang == 45 else 2.0
        ax2.plot(
            X,
            Y,
            color=col,
            lw=lw,
            label=f"{ang}°" + ("（射程最大）" if ang == 45 else ""),
        )
        R = v0r**2 * np.sin(2 * a) / g
        ax2.add_patch(Circle((R, 0), 0.18, color=col, zorder=5))
    # 互補角同射程提示：30 與 60 落點相同
    ax2.axhline(0, color=F.INK, lw=1.3)
    ax2.add_patch(
        Rectangle(
            (-0.5, -0.7),
            12.5,
            0.45,
            facecolor="#eef1f5",
            edgecolor="none",
            hatch="////",
            lw=0.9,
            zorder=0,
        )
    )
    ax2.text(
        5.0,
        -1.4,
        "30° 與 60° 互補 → 落點（射程）相同",
        ha="center",
        color=F.INK,
        fontsize=11,
    )
    ax2.set_title(
        "同初速、不同角度：$R=\\dfrac{v_0^2\\sin 2\\theta}{g}$，45° 最遠", fontsize=12.5
    )
    ax2.legend(loc="upper right", fontsize=10, frameon=False)
    ax2.set_xlim(-0.5, 11.5)
    ax2.set_ylim(-1.9, 6.2)
    ax2.set_xlabel("水平距離 (m)")
    ax2.set_ylabel("高度 (m)")
    F.clean_grid(ax2)

    fig.tight_layout()
    F.save_to(fig, CH, "選物I-3-斜拋分解")


def fig_parabola():
    """平拋軌跡與速度分量：說明速度水平分量不變、鉛直分量隨時間增大，合速度漸轉向下。"""
    fig, ax = F.canvas(7.4, 4.6)
    g, vx, H = 10.0, 4.0, 5.0
    T = np.sqrt(2 * H / g)
    tt = np.linspace(0, T, 120)
    X = vx * tt
    Y = H - 0.5 * g * tt**2
    ax.plot(X, Y, color=F.INK, lw=2.4, zorder=3)
    # 在三個時刻畫速度分量
    for ti in [0.4, 0.7, 1.0]:
        x0, y0 = vx * ti, H - 0.5 * g * ti**2
        vy = g * ti
        sc = 0.12
        ax.add_patch(Circle((x0, y0), 0.07, color=F.INK, zorder=6))
        F.arrow(
            ax, (x0, y0), (x0 + vx * sc * 1.6, y0), color=F.BLUE, lw=2.0, mutation=14
        )
        F.arrow(ax, (x0, y0), (x0, y0 - vy * sc), color=F.RED, lw=2.0, mutation=14)
        F.arrow(
            ax,
            (x0, y0),
            (x0 + vx * sc * 1.6, y0 - vy * sc),
            color=F.PURPLE,
            lw=2.0,
            mutation=14,
        )
    ax.text(0.55, H + 0.25, r"$v_x=v_0$（不變）", color=F.BLUE, fontsize=12)
    ax.text(2.7, 3.2, r"$v_y=gt$（增大）", color=F.RED, fontsize=12)
    ax.text(4.2, 1.6, r"合速度 $\vec v$", color=F.PURPLE, fontsize=12)
    ax.set_title("平拋的速度：水平分量恆定、鉛直分量越來越大", fontsize=13)
    ax.set_xlabel("水平距離 $x$ (m)")
    ax.set_ylabel("高度 $y$ (m)")
    ax.set_xlim(-0.3, vx * T + 0.5)
    ax.set_ylim(-0.3, H + 1.0)
    F.clean_grid(ax)
    fig.tight_layout()
    F.save_to(fig, CH, "選物I-3-平拋軌跡")


if __name__ == "__main__":
    fig_independence()
    fig_dropvsproj()
    fig_oblique()
    fig_parabola()
    print("done.")
