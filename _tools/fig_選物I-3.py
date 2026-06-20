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


def fig_boat():
    """河中行船的速度向量三角形：左圖「船頭垂直對岸（最快渡河）」、
    右圖「垂直抵達正對岸」。每張都把船速、水流速、合速度頭尾相接成三角形，
    並標出直角／偏角，凸顯兩種問法的差異。"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.6, 5.0))
    for ax in (ax1, ax2):
        ax.set_aspect("equal")
        ax.axis("off")

    # 共用尺度（v=船速、u=水流）：取 v=5、u=3，與例題 3-8 一致（3-4-5 直角三角形）
    v, u = 5.0, 3.0

    # ===== 左：問法一 船頭垂直對岸（最快渡河）=====
    O = np.array([0.0, 0.0])
    # 河岸（上下兩條水平線）與水流方向（向右）
    bank_w = 7.2
    for yb in (0.0, 6.0):
        ax1.plot([-0.6, bank_w], [yb, yb], color=F.INK, lw=1.6, zorder=1)
    ax1.add_patch(
        Rectangle(
            (-0.6, 6.0),
            bank_w + 0.6,
            0.5,
            facecolor="#eef1f5",
            edgecolor="none",
            hatch="////",
            lw=0.8,
            zorder=0,
        )
    )
    ax1.add_patch(
        Rectangle(
            (-0.6, -0.5),
            bank_w + 0.6,
            0.5,
            facecolor="#eef1f5",
            edgecolor="none",
            hatch="////",
            lw=0.8,
            zorder=0,
        )
    )
    F.label(ax1, (bank_w - 1.0, 5.68), "對岸", color=F.INK, fs=11, ha="center")
    F.label(ax1, (bank_w - 1.0, 0.34), "出發岸", color=F.INK, fs=11, ha="center")
    # 水流方向小箭頭（背景，沿河岸向右）
    for xb in (1.2, 3.2, 5.2):
        F.arrow(
            ax1, (xb, 3.0), (xb + 0.9, 3.0), color="#9aa0a6", lw=1.2, mutation=12, z=1
        )
    F.label(ax1, (4.6, 3.32), "水流方向", color="#9aa0a6", fs=10, ha="center")

    # 向量三角形（頭尾相接）：船速（向上，垂直對岸）＋ 水流（向右）＝ 合速度（斜向右上）
    vb = np.array([0.0, v])  # 船對水：垂直指向對岸
    vu = np.array([u, 0.0])  # 水對地：沿河岸
    res = vb + vu  # 船對地：合速度
    # 船速向量
    F.arrow(ax1, O, vb, color=F.BLUE, lw=3.0, mutation=18)
    ax1.text(-0.25, v / 2, "船速 v", color=F.BLUE, fontsize=13, ha="right", va="center")
    # 水流向量（接在船速末端）
    F.arrow(ax1, vb, vb + vu, color=F.RED, lw=3.0, mutation=18)
    ax1.text(
        vb[0] + u / 2,
        v + 0.28,
        "水流 u",
        color=F.RED,
        fontsize=13,
        ha="center",
        va="bottom",
    )
    # 合速度（對地航跡）
    F.arrow(ax1, O, res, color=F.PURPLE, lw=3.0, mutation=20)
    ax1.text(
        res[0] / 2 + 0.45,
        res[1] / 2 - 0.35,
        "合速度",
        color=F.PURPLE,
        fontsize=12.5,
        ha="left",
        va="center",
    )
    ax1.text(
        res[0] / 2 + 0.45,
        res[1] / 2 - 0.95,
        "（被沖向下游）",
        color=F.PURPLE,
        fontsize=10.5,
        ha="left",
        va="center",
    )
    # 直角標記（船速與水流垂直）
    rs = 0.42
    ax1.plot([0, rs], [v, v], color=F.INK, lw=1.2)
    ax1.plot([rs, rs], [v, v - rs], color=F.INK, lw=1.2)
    # 漂移距離標示（沿對岸從正對點到實際登岸點）
    ax1.plot([res[0], res[0]], [v, 6.0], color=F.PURPLE, lw=0.8, ls=":")
    ax1.set_title("問法一：船頭垂直對岸（渡河最快，但被沖下游）", fontsize=12)
    ax1.set_xlim(-1.4, bank_w + 0.3)
    ax1.set_ylim(-0.9, 6.9)

    # ===== 右：問法二 垂直抵達正對岸 =====
    # 船速朝上游偏 θ，使 v sinθ 抵消水流 u；合速度垂直對岸
    # sinθ = u/v = 3/5 → θ=37°，v cosθ = 4
    O2 = np.array([0.0, 0.0])
    vcos = np.sqrt(v**2 - u**2)  # =4，垂直分量（合速度大小）
    vb2 = np.array([-u, vcos])  # 船對水：朝左上（上游側）
    vu2 = np.array([u, 0.0])  # 水對地：向右
    res2 = vb2 + vu2  # 合速度：純向上（垂直對岸）
    for yb in (0.0, 6.0):
        ax2.plot([-2.4, 5.4], [yb, yb], color=F.INK, lw=1.6, zorder=1)
    ax2.add_patch(
        Rectangle(
            (-2.4, 6.0),
            7.8,
            0.5,
            facecolor="#eef1f5",
            edgecolor="none",
            hatch="////",
            lw=0.8,
            zorder=0,
        )
    )
    ax2.add_patch(
        Rectangle(
            (-2.4, -0.5),
            7.8,
            0.5,
            facecolor="#eef1f5",
            edgecolor="none",
            hatch="////",
            lw=0.8,
            zorder=0,
        )
    )
    F.label(ax2, (4.4, 5.68), "對岸", color=F.INK, fs=11, ha="center")
    F.label(ax2, (4.4, 0.34), "出發岸", color=F.INK, fs=11, ha="center")
    for xb in (-1.6, 0.4, 2.4):
        F.arrow(
            ax2, (xb, 3.0), (xb + 0.9, 3.0), color="#9aa0a6", lw=1.2, mutation=12, z=1
        )
    F.label(ax2, (1.4, 3.32), "水流方向", color="#9aa0a6", fs=10, ha="center")
    # 船速向量（朝上游偏）
    F.arrow(ax2, O2, vb2, color=F.BLUE, lw=3.0, mutation=18)
    ax2.text(
        vb2[0] - 0.2,
        vb2[1] / 2 + 0.2,
        "船速 v",
        color=F.BLUE,
        fontsize=13,
        ha="right",
        va="center",
    )
    ax2.text(
        vb2[0] - 0.2,
        vb2[1] / 2 - 0.4,
        "（朝上游偏）",
        color=F.BLUE,
        fontsize=10,
        ha="right",
        va="center",
    )
    # 水流向量（接在船速末端）
    F.arrow(ax2, vb2, vb2 + vu2, color=F.RED, lw=3.0, mutation=18)
    ax2.text(
        vb2[0] + u / 2,
        vb2[1] + 0.28,
        "水流 u",
        color=F.RED,
        fontsize=13,
        ha="center",
        va="bottom",
    )
    # 合速度（純向上，垂直對岸）
    F.arrow(ax2, O2, res2, color=F.PURPLE, lw=3.0, mutation=20)
    ax2.text(
        res2[0] + 0.2,
        res2[1] / 2,
        "合速度（正對對岸）",
        color=F.PURPLE,
        fontsize=12,
        ha="left",
        va="center",
    )
    # 偏角 θ（合速度鉛直 vs 船速）
    ang = np.degrees(np.arctan2(vb2[0], vb2[1]))  # 與鉛直的夾角（負值朝左）
    ax2.add_patch(
        Arc(O2, 1.6, 1.6, angle=0, theta1=90, theta2=90 - ang, color=F.INK, lw=1.4)
    )
    ax2.text(-0.42, 1.05, "θ", color=F.INK, fontsize=14, ha="center", va="center")
    # 直角標記（合速度與河岸垂直）
    rs2 = 0.42
    ax2.plot([0, rs2], [0, 0], color=F.INK, lw=1.2, zorder=2)  # 沿河岸短段
    ax2.plot([rs2, rs2], [0, rs2], color=F.INK, lw=1.2, zorder=2)
    ax2.set_title("問法二：垂直抵達正對岸（船頭朝上游偏 θ）", fontsize=12)
    ax2.set_xlim(-2.6, 5.6)
    ax2.set_ylim(-0.9, 6.9)

    fig.suptitle("河中行船的速度向量三角形：對地 ＝ 船對水 ＋ 水對地", fontsize=13.5)
    fig.tight_layout(rect=(0, 0, 1, 0.96))
    F.save_to(fig, CH, "選物I-3-行船向量三角形")


def fig_monkey():
    """猴子與獵人：水平瞄準的子彈與同時放手的猴子，鉛直方向以同一個 g 下墜，
    必相撞。左：無重力的直線瞄準路徑；右：加上重力後兩者的實際拋物線／落線，
    並用等高虛線標出同一時刻兩者位於同一高度。"""
    fig, ax = F.schematic(8.6, 5.2)
    g = 10.0
    # 槍口在左下，猴子原位在右上；子彈水平速度沿瞄準線方向
    gun = np.array([0.0, 0.6])
    monkey0 = np.array([7.4, 4.2])  # 猴子原本掛的位置
    dx, dy = monkey0 - gun
    L = np.hypot(dx, dy)
    # 子彈速率設定，使其在合理時間抵達猴子水平位置
    Tend = 1.0
    vb = L / Tend  # 沿瞄準線的速率
    ux, uy = dx / L, dy / L  # 瞄準線單位向量
    speed_x = vb * ux  # 子彈水平分速
    speed_y = vb * uy  # 子彈鉛直分速（向上）

    # 瞄準線（無重力時的直線路徑）— 灰色虛線
    ax.plot(
        [gun[0], monkey0[0]],
        [gun[1], monkey0[1]],
        color="#9aa0a6",
        lw=1.4,
        ls="--",
        zorder=2,
    )
    F.label(
        ax,
        ((gun[0] + monkey0[0]) / 2 + 0.2, (gun[1] + monkey0[1]) / 2 + 0.45),
        "瞄準線（無重力時的直線）",
        color="#9aa0a6",
        fs=10.5,
        ha="center",
    )

    ts = np.linspace(0, Tend, 100)
    # 子彈實際軌跡（拋物線）
    bx = gun[0] + speed_x * ts
    by = gun[1] + speed_y * ts - 0.5 * g * ts**2
    ax.plot(bx, by, color=F.BLUE, lw=2.2, zorder=3)
    # 猴子實際軌跡（自由落下，x 固定）
    mx = np.full_like(ts, monkey0[0])
    my = monkey0[1] - 0.5 * g * ts**2
    ax.plot(mx, my, color=F.RED, lw=2.2, ls="-", zorder=3)

    # 幾個同時刻的位置 + 等高虛線
    for tk in (0.45, 0.7, 1.0):
        bxx = gun[0] + speed_x * tk
        byy = gun[1] + speed_y * tk - 0.5 * g * tk**2
        myy = monkey0[1] - 0.5 * g * tk**2
        ax.plot(
            [bxx, monkey0[0]], [byy, myy], color="#c9ccd1", lw=0.8, ls=":", zorder=1
        )
        ax.add_patch(Circle((bxx, byy), 0.10, color=F.BLUE, zorder=5))
        ax.add_patch(Circle((monkey0[0], myy), 0.13, color=F.RED, zorder=5))
        # 標出「同一時刻兩者掉的高度相同」
        if tk == 0.7:
            ax.annotate(
                "",
                xy=(monkey0[0] + 0.5, monkey0[1]),
                xytext=(monkey0[0] + 0.5, myy),
                arrowprops=dict(arrowstyle="<->", color=F.INK, lw=1.0),
            )
            ax.text(
                monkey0[0] + 0.65,
                (monkey0[1] + myy) / 2,
                r"下墜 $\frac{1}{2}gt^2$",
                color=F.INK,
                fontsize=10.5,
                ha="left",
                va="center",
            )

    # 相撞點（t=Tend）
    hitx = gun[0] + speed_x * Tend
    hity = gun[1] + speed_y * Tend - 0.5 * g * Tend**2
    ax.add_patch(
        Circle(
            (hitx, hity), 0.18, facecolor="none", edgecolor=F.AMBER, lw=2.2, zorder=6
        )
    )
    F.label(ax, (hitx - 0.2, hity - 0.5), "相撞！", color=F.AMBER, fs=12.5, ha="center")

    # 槍口與猴子標記
    F.label(ax, (gun[0] - 0.1, gun[1] - 0.45), "槍口", color=F.BLUE, fs=11, ha="center")
    F.label(
        ax,
        (monkey0[0] + 0.1, monkey0[1] + 0.35),
        "猴子原位",
        color=F.RED,
        fs=11,
        ha="center",
    )
    F.label(ax, (2.1, 1.0), "子彈實際軌跡", color=F.BLUE, fs=11, ha="center")

    # 地面
    ax.add_patch(
        Rectangle(
            (-0.6, -0.85),
            9.6,
            0.3,
            facecolor="#eef1f5",
            edgecolor=F.INK,
            hatch="////",
            lw=1.0,
            zorder=0,
        )
    )
    ax.plot([-0.6, 9.0], [-0.55, -0.55], color=F.INK, lw=1.4)

    ax.set_title("猴子與獵人：子彈與猴子鉛直方向同步下墜 → 必相撞", fontsize=13.5)
    ax.set_xlim(-0.9, 9.4)
    ax.set_ylim(-1.2, 5.3)
    F.save_to(fig, CH, "選物I-3-猴子與獵人")


def fig_relvel():
    """一般平面相對速度：兩物體沿不同方向運動時，B 相對於 A 的速度＝向量相減。
    以「雨中行人」為例——雨鉛直落下、人水平前進，從人看雨是斜向迎面而來。
    左：地面看到的兩速度向量；右：以 vB − vA 合成出相對速度三角形。"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.6, 4.8))
    for ax in (ax1, ax2):
        ax.set_aspect("equal")
        ax.axis("off")

    vrain = np.array([0.0, -3.0])  # 雨對地：鉛直向下
    vperson = np.array([2.0, 0.0])  # 人對地：水平向前

    # ===== 左：地面參考系看到的兩速度 =====
    O = np.array([0.0, 0.0])
    F.arrow(ax1, O, vrain, color=F.BLUE, lw=3.0, mutation=18)
    ax1.text(
        vrain[0] - 0.25,
        vrain[1] / 2,
        "雨對地",
        color=F.BLUE,
        fontsize=12,
        ha="right",
        va="center",
    )
    F.arrow(ax1, O, vperson, color=F.GREEN, lw=3.0, mutation=18)
    ax1.text(
        vperson[0] / 2,
        vperson[1] + 0.25,
        "人對地",
        color=F.GREEN,
        fontsize=12,
        ha="center",
        va="bottom",
    )
    ax1.set_title("地面看：雨鉛直落、人水平走", fontsize=12)
    ax1.set_xlim(-1.6, 3.0)
    ax1.set_ylim(-3.8, 1.2)

    # ===== 右：相對速度 v(雨/人) = v雨 − v人 =====
    # 作圖：v雨 + (−v人) 頭尾相接
    O2 = np.array([0.0, 0.0])
    neg_p = -vperson
    rel = vrain - vperson
    # v雨
    F.arrow(ax2, O2, vrain, color=F.BLUE, lw=3.0, mutation=18)
    ax2.text(
        vrain[0] - 0.25,
        vrain[1] / 2,
        r"$\vec v_{r}$",
        color=F.BLUE,
        fontsize=14,
        ha="right",
        va="center",
    )
    # −v人（接在 v雨 末端）
    F.arrow(ax2, vrain, vrain + neg_p, color=F.GREEN, lw=3.0, mutation=18)
    ax2.text(
        vrain[0] + neg_p[0] / 2,
        vrain[1] - 0.28,
        r"$-\vec v_{p}$",
        color=F.GREEN,
        fontsize=14,
        ha="center",
        va="top",
    )
    # 合成的相對速度（從 O2 指到末端）
    F.arrow(ax2, O2, rel, color=F.PURPLE, lw=3.0, mutation=20)
    ax2.text(
        rel[0] / 2 - 0.3,
        rel[1] / 2 + 0.1,
        r"$\vec v_{r/p}$",
        color=F.PURPLE,
        fontsize=14,
        ha="right",
        va="center",
    )
    ax2.text(
        rel[0] / 2 - 0.3,
        rel[1] / 2 - 0.5,
        "雨對人（斜向迎面）",
        color=F.PURPLE,
        fontsize=10.5,
        ha="right",
        va="center",
    )
    ax2.set_title(
        r"從人看：$\vec v_{r/p}=\vec v_{r}-\vec v_{p}$（向量相減）", fontsize=12
    )
    ax2.set_xlim(-3.0, 1.4)
    ax2.set_ylim(-3.8, 1.2)

    fig.suptitle("一般平面相對速度：B 相對 A 的速度＝向量相減", fontsize=13.5)
    fig.tight_layout(rect=(0, 0, 1, 0.95))
    F.save_to(fig, CH, "選物I-3-相對速度合成")


if __name__ == "__main__":
    fig_independence()
    fig_dropvsproj()
    fig_oblique()
    fig_parabola()
    fig_boat()
    fig_monkey()
    fig_relvel()
    print("done.")
