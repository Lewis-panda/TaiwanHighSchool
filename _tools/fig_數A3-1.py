# -*- coding: utf-8 -*-
"""產生「數A3-1 三角函數」公開講義的 SVG，輸出到 content 章節 assets/。
重繪：  .venv/bin/python _tools/fig_數A3-1.py
函數圖：F.canvas() + ax.plot() + F.clean_grid(ax)；
幾何圖（扇形）用 ax.set_aspect("equal")。
注意：mathtext 不支援 \\dfrac/\\tfrac（用 \\frac）；圖內中文勿放進 $...$。
"""

import os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Wedge, Arc, FancyArrowPatch
import figlib as F

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CH = os.path.join(ROOT, "content", "數學A", "數A3-1")


def _save(fig, name):
    return F.save_to(fig, CH, name, output_subdir="assets", write_pdf=False)


def _pi_ticks(ax, xmax_units, step=0.5):
    """把 x 軸刻度設成 π 的倍數（單位為 π）。xmax_units 以 π 為單位。"""
    locs, labels = [], []
    n = int(round(xmax_units / step))
    for i in range(-n, n + 1):
        v = i * step
        locs.append(v * np.pi)
        if abs(v) < 1e-9:
            labels.append("$0$")
        elif abs(v - 1) < 1e-9:
            labels.append(r"$\pi$")
        elif abs(v + 1) < 1e-9:
            labels.append(r"$-\pi$")
        elif abs(v - round(v)) < 1e-9:
            labels.append(rf"${int(round(v))}\pi$")
        else:
            # 半整數倍：寫成 p/2 π
            num = int(round(v * 2))
            if num == 1:
                labels.append(r"$\frac{\pi}{2}$")
            elif num == -1:
                labels.append(r"$-\frac{\pi}{2}$")
            else:
                labels.append(rf"$\frac{{{num}\pi}}{{2}}$")
    ax.set_xticks(locs)
    ax.set_xticklabels(labels)


def fig_radian_sector():
    """弧度的定義與扇形：半徑 r、圓心角 θ、弧長 s=rθ、扇形面積。"""
    fig, ax = F.canvas(6.4, 6.0)
    r = 1.0
    th0, th1 = 0.0, 65.0  # 度

    # 扇形填色
    ax.add_patch(Wedge((0, 0), r, th0, th1, fc="#eef3fb", ec="none", zorder=1))

    # 兩條半徑
    ax.plot([0, r], [0, 0], color=F.INK, lw=2.4, zorder=4)
    a1 = np.deg2rad(th1)
    ax.plot([0, r * np.cos(a1)], [0, r * np.sin(a1)], color=F.INK, lw=2.4, zorder=4)

    # 弧（紅、加粗）
    arc_t = np.linspace(np.deg2rad(th0), a1, 200)
    ax.plot(r * np.cos(arc_t), r * np.sin(arc_t), color=F.RED, lw=3.2, zorder=5)

    # 圓的其餘部分（淡）
    ft = np.linspace(0, 2 * np.pi, 400)
    ax.plot(r * np.cos(ft), r * np.sin(ft), color=F.GRID, lw=1.4, zorder=0)

    # 角弧（琥珀）
    ax.add_patch(
        Arc(
            (0, 0),
            0.42,
            0.42,
            angle=0,
            theta1=th0,
            theta2=th1,
            color=F.AMBER,
            lw=2.0,
            zorder=4,
        )
    )
    ax.text(0.30, 0.13, r"$\theta$", color=F.AMBER, fontsize=16, ha="center")

    # 半徑標示
    ax.text(0.5, -0.09, "$r$", color=F.INK, fontsize=14, ha="center", va="top")
    midr = np.deg2rad((th0 + th1) / 2)
    ax.text(
        0.52 * np.cos(a1) - 0.10,
        0.52 * np.sin(a1) + 0.04,
        "$r$",
        color=F.INK,
        fontsize=14,
        ha="center",
    )

    # 弧長標示
    am = np.deg2rad((th0 + th1) / 2 + 6)
    ax.text(
        1.16 * np.cos(am),
        1.16 * np.sin(am),
        "弧長",
        color=F.RED,
        fontsize=12.5,
        ha="center",
    )
    ax.text(
        1.20 * np.cos(midr) - 0.06,
        1.20 * np.sin(midr) - 0.18,
        "$s=r\\,\\theta$",
        color=F.RED,
        fontsize=14,
        ha="center",
    )

    # 原點
    ax.add_patch(Circle((0, 0), 0.022, color=F.INK, zorder=6))
    ax.text(-0.07, -0.07, "$O$", color=F.INK, fontsize=12, ha="right", va="top")

    # 定義說明框
    ax.text(
        0.0,
        -1.34,
        r"$\theta=\frac{s}{r}\ \mathrm{(rad)},\quad s=r\theta,\quad "
        r"A=\frac{1}{2}r^2\theta$",
        color=F.INK,
        fontsize=13,
        ha="center",
        va="center",
        bbox=dict(boxstyle="round,pad=0.35", fc="white", ec=F.GRID, lw=1.2),
    )

    ax.set_xlim(-1.25, 1.35)
    ax.set_ylim(-1.55, 1.25)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("弧度的定義與扇形（弧長、面積）", fontsize=14)
    _save(fig, "數A3-1-弧度扇形")


def fig_three_graphs():
    """y=sin x, y=cos x, y=tan x 三條基本圖形（上下排）。"""
    fig, axes = plt.subplots(3, 1, figsize=(8.2, 9.2))

    x = np.linspace(-2 * np.pi, 2 * np.pi, 2000)

    # --- sin ---
    ax = axes[0]
    ax.plot(x, np.sin(x), color=F.BLUE, lw=2.6)
    ax.axhline(0, color=F.INK, lw=1.0)
    ax.axvline(0, color=F.INK, lw=1.0)
    ax.set_ylim(-1.6, 1.6)
    ax.set_yticks([-1, 0, 1])
    _pi_ticks(ax, 2.0, step=0.5)
    ax.set_xlim(-2 * np.pi - 0.2, 2 * np.pi + 0.2)
    F.clean_grid(ax)
    ax.set_title(
        r"$y=\sin x$　（定義域 $\mathbb{R}$，值域 $[-1,1]$，週期 $2\pi$）", fontsize=13
    )

    # --- cos ---
    ax = axes[1]
    ax.plot(x, np.cos(x), color=F.GREEN, lw=2.6)
    ax.axhline(0, color=F.INK, lw=1.0)
    ax.axvline(0, color=F.INK, lw=1.0)
    ax.set_ylim(-1.6, 1.6)
    ax.set_yticks([-1, 0, 1])
    _pi_ticks(ax, 2.0, step=0.5)
    ax.set_xlim(-2 * np.pi - 0.2, 2 * np.pi + 0.2)
    F.clean_grid(ax)
    ax.set_title(
        r"$y=\cos x$　（定義域 $\mathbb{R}$，值域 $[-1,1]$，週期 $2\pi$）", fontsize=13
    )

    # --- tan ---
    ax = axes[2]
    # 分段畫，避開漸近線
    for k in range(-2, 3):
        xa = np.linspace(
            -np.pi / 2 + k * np.pi + 0.02, np.pi / 2 + k * np.pi - 0.02, 400
        )
        ax.plot(xa, np.tan(xa), color=F.RED, lw=2.6)
    # 漸近線
    for k in range(-2, 3):
        xv = np.pi / 2 + k * np.pi
        if -2 * np.pi - 0.2 <= xv <= 2 * np.pi + 0.2:
            ax.axvline(xv, color="#9aa0a6", lw=1.2, ls="--")
    ax.axhline(0, color=F.INK, lw=1.0)
    ax.axvline(0, color=F.INK, lw=1.0)
    ax.set_ylim(-4.2, 4.2)
    ax.set_yticks([-3, 0, 3])
    _pi_ticks(ax, 2.0, step=0.5)
    ax.set_xlim(-2 * np.pi - 0.2, 2 * np.pi + 0.2)
    F.clean_grid(ax)
    ax.set_title(
        r"$y=\tan x$　（定義域 $x\neq\frac{\pi}{2}+k\pi$，"
        r"值域 $\mathbb{R}$，週期 $\pi$，虛線為漸近線）",
        fontsize=13,
    )

    fig.suptitle("三角函數的基本圖形", fontsize=15, y=1.005)
    fig.tight_layout()
    _save(fig, "數A3-1-三角函數圖")


def fig_sine_cosine_graphs():
    """把正弦、餘弦拆成適合 A4 寬度的兩列圖，避免三圖縮得過小。"""
    fig, axes = plt.subplots(2, 1, figsize=(8.4, 5.8))
    x = np.linspace(-2 * np.pi, 2 * np.pi, 2000)

    panels = [
        (axes[0], np.sin(x), F.BLUE, r"$y=\sin x$", r"值域 $[-1,1]$，週期 $2\pi$"),
        (axes[1], np.cos(x), F.GREEN, r"$y=\cos x$", r"值域 $[-1,1]$，週期 $2\pi$"),
    ]
    for ax, y, color, name, note in panels:
        ax.plot(x, y, color=color, lw=2.7)
        ax.axhline(0, color=F.INK, lw=1.0)
        ax.axvline(0, color=F.INK, lw=1.0)
        ax.set_ylim(-1.55, 1.55)
        ax.set_yticks([-1, 0, 1])
        _pi_ticks(ax, 2.0, step=0.5)
        ax.set_xlim(-2 * np.pi - 0.2, 2 * np.pi + 0.2)
        F.clean_grid(ax)
        ax.set_title(f"{name}　（定義域 $\\mathbb{{R}}$，{note}）", fontsize=12.5)

    fig.suptitle(r"正弦與餘弦：同樣的波形，相位相差 $\pi/2$", fontsize=14.5, y=1.005)
    fig.tight_layout()
    _save(fig, "數A3-1-正弦餘弦圖")


def fig_tangent_graph():
    """獨立的正切圖，讓漸近線與週期在 PDF 中保持可讀。"""
    fig, ax = plt.subplots(figsize=(8.4, 3.9))
    xlim = (-2 * np.pi - 0.2, 2 * np.pi + 0.2)
    branch_indices = range(-2, 3)
    branch_bounds = [
        (-np.pi / 2 + k * np.pi, np.pi / 2 + k * np.pi)
        for k in branch_indices
    ]
    if not (
        branch_bounds[0][0] < xlim[0] < branch_bounds[0][1]
        and branch_bounds[-1][0] < xlim[1] < branch_bounds[-1][1]
    ):
        raise AssertionError("正切分段必須覆蓋整個可見 x 範圍")

    for k in branch_indices:
        xa = np.linspace(
            -np.pi / 2 + k * np.pi + 0.025,
            np.pi / 2 + k * np.pi - 0.025,
            500,
        )
        ax.plot(xa, np.tan(xa), color=F.RED, lw=2.7)
    for k in range(-2, 3):
        xv = np.pi / 2 + k * np.pi
        if -2 * np.pi - 0.2 <= xv <= 2 * np.pi + 0.2:
            ax.axvline(xv, color="#8d98a5", lw=1.2, ls="--")
    ax.axhline(0, color=F.INK, lw=1.0)
    ax.axvline(0, color=F.INK, lw=1.0)
    ax.set_ylim(-4.2, 4.2)
    ax.set_yticks([-3, 0, 3])
    _pi_ticks(ax, 2.0, step=0.5)
    ax.set_xlim(*xlim)
    F.clean_grid(ax)
    ax.set_title(
        r"$y=\tan x$：值域 $\mathbb{R}$，週期 $\pi$；虛線是 $x=\frac{\pi}{2}+k\pi$",
        fontsize=12.5,
    )
    fig.tight_layout()
    _save(fig, "數A3-1-正切函數圖")


def fig_transform():
    """y=a sin(bx+c)+d 的四種變換：振幅、週期、相位移、鉛直平移。"""
    fig, axes = plt.subplots(2, 2, figsize=(11.0, 7.4))
    x = np.linspace(-2 * np.pi, 2 * np.pi, 2000)
    base = np.sin(x)

    panels = [
        # (ax, y, color, 標題, 對照說明)
        (
            axes[0, 0],
            2 * np.sin(x),
            F.BLUE,
            r"振幅：$y=2\sin x$",
            "振幅 2（虛線為 $y=\\sin x$）",
        ),
        (
            axes[0, 1],
            np.sin(2 * x),
            F.GREEN,
            r"週期：$y=\sin 2x$",
            "週期變為 $\\pi$（壓縮一半）",
        ),
        (
            axes[1, 0],
            np.sin(x - np.pi / 2),
            F.AMBER,
            r"相位移：$y=\sin\left(x-\frac{\pi}{2}\right)$",
            "向右平移 $\\pi/2$",
        ),
        (axes[1, 1], np.sin(x) + 1, F.PURPLE, r"鉛直平移：$y=\sin x+1$", "整條上移 1"),
    ]

    for ax, y, col, title, note in panels:
        ax.plot(x, base, color="#9aa0a6", lw=1.6, ls="--", zorder=2)
        ax.plot(x, y, color=col, lw=2.8, zorder=3)
        ax.axhline(0, color=F.INK, lw=1.0)
        ax.axvline(0, color=F.INK, lw=1.0)
        ax.set_ylim(-2.6, 2.6)
        ax.set_yticks([-2, -1, 0, 1, 2])
        _pi_ticks(ax, 2.0, step=1.0)
        ax.set_xlim(-2 * np.pi - 0.2, 2 * np.pi + 0.2)
        F.clean_grid(ax)
        ax.set_title(title, fontsize=13)
        ax.text(
            0.02,
            0.96,
            note,
            transform=ax.transAxes,
            fontsize=11,
            color=col,
            ha="left",
            va="top",
            bbox=dict(boxstyle="round,pad=0.25", fc="white", ec=col, lw=1.0, alpha=0.9),
        )

    fig.suptitle(r"$y=a\sin(bx+c)+d$ 的四種變換", fontsize=15, y=1.01)
    fig.tight_layout()
    _save(fig, "數A3-1-圖形變換")


def fig_sum_diff_circle():
    """和差角公式的單位圓推導：P=(cosA,sinA)、Q=(cosB,sinB)，
    夾角 A-B，弦長 PQ 用兩種方式算 → cos(A-B)=cosAcosB+sinAsinB。"""
    fig, ax = F.canvas(6.6, 6.6)
    r = 1.0
    A = np.deg2rad(72.0)
    B = np.deg2rad(26.0)

    # 單位圓
    ft = np.linspace(0, 2 * np.pi, 400)
    ax.plot(r * np.cos(ft), r * np.sin(ft), color=F.GRID, lw=1.6, zorder=0)

    # 兩個半徑 OP、OQ
    Px, Py = np.cos(A), np.sin(A)
    Qx, Qy = np.cos(B), np.sin(B)
    ax.plot([0, Px], [0, Py], color=F.INK, lw=2.0, zorder=4)
    ax.plot([0, Qx], [0, Qy], color=F.INK, lw=2.0, zorder=4)

    # 弦 PQ（紅、加粗）
    ax.plot([Px, Qx], [Py, Qy], color=F.RED, lw=3.0, zorder=5)

    # 夾角 A-B 弧（琥珀）
    ax.add_patch(
        Arc(
            (0, 0),
            0.66,
            0.66,
            angle=0,
            theta1=np.rad2deg(B),
            theta2=np.rad2deg(A),
            color=F.AMBER,
            lw=2.4,
            zorder=4,
        )
    )
    amid = (A + B) / 2
    ax.text(
        0.46 * np.cos(amid),
        0.46 * np.sin(amid),
        r"$A-B$",
        color=F.AMBER,
        fontsize=14,
        ha="center",
        va="center",
    )

    # A、B 角（自 x 軸量起，淡藍細弧）
    ax.add_patch(
        Arc(
            (0, 0),
            0.34,
            0.34,
            angle=0,
            theta1=0,
            theta2=np.rad2deg(B),
            color=F.BLUE,
            lw=1.6,
            zorder=4,
        )
    )
    ax.text(
        0.255 * np.cos(B / 2),
        0.255 * np.sin(B / 2) - 0.02,
        "$B$",
        color=F.BLUE,
        fontsize=12.5,
        ha="center",
        va="center",
    )
    ax.add_patch(
        Arc(
            (0, 0),
            0.96,
            0.96,
            angle=0,
            theta1=0,
            theta2=np.rad2deg(A),
            color=F.GREEN,
            lw=1.6,
            zorder=4,
        )
    )
    ax.text(
        0.56 * np.cos(A - 0.18),
        0.56 * np.sin(A - 0.18),
        "$A$",
        color=F.GREEN,
        fontsize=12.5,
        ha="center",
        va="center",
    )

    # 點 P、Q（紅點，名稱併入下方坐標標籤避免重疊）
    ax.add_patch(Circle((Px, Py), 0.026, color=F.RED, zorder=6))
    ax.add_patch(Circle((Qx, Qy), 0.026, color=F.RED, zorder=6))
    ax.text(
        Px - 0.02,
        Py + 0.09,
        r"$P=(\cos A,\ \sin A)$",
        color=F.RED,
        fontsize=12,
        ha="center",
        va="bottom",
    )
    ax.text(
        Qx + 0.10,
        Qy + 0.02,
        r"$Q=(\cos B,\ \sin B)$",
        color=F.RED,
        fontsize=12,
        ha="left",
        va="center",
    )

    # 半徑長度 1 標示
    ax.text(
        0.5 * np.cos(A) - 0.10,
        0.5 * np.sin(A) + 0.02,
        "$1$",
        color=F.INK,
        fontsize=12,
        ha="center",
    )
    ax.text(
        0.5 * np.cos(B) + 0.02,
        0.5 * np.sin(B) - 0.11,
        "$1$",
        color=F.INK,
        fontsize=12,
        ha="center",
    )

    # 原點與 x 軸
    ax.axhline(0, color=F.INK, lw=1.0, zorder=1)
    ax.add_patch(Circle((0, 0), 0.022, color=F.INK, zorder=6))
    ax.text(-0.06, -0.08, "$O$", color=F.INK, fontsize=12, ha="right", va="top")
    ax.text(1.16, 0.0, "$x$", color=F.INK, fontsize=12, ha="left", va="center")

    # 兩種算弦長的對照框
    ax.text(
        0.0,
        -1.46,
        r"距離公式：$\overline{PQ}^2=2-2(\cos A\cos B+\sin A\sin B)$"
        "\n"
        r"餘弦定理：$\overline{PQ}^2=2-2\cos(A-B)$"
        "\n"
        r"$\Rightarrow\ \cos(A-B)=\cos A\cos B+\sin A\sin B$",
        color=F.INK,
        fontsize=12,
        ha="center",
        va="center",
        linespacing=1.6,
        bbox=dict(boxstyle="round,pad=0.4", fc="white", ec=F.GRID, lw=1.2),
    )

    ax.set_xlim(-1.25, 1.45)
    ax.set_ylim(-1.85, 1.25)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("和差角公式的單位圓推導：弦長算兩次", fontsize=14)
    _save(fig, "數A3-1-和差角推導")


def fig_superpose():
    """正餘弦疊合：a sinθ + b cosθ 合成單一正弦波。"""
    fig, ax = F.canvas(8.4, 5.0)
    x = np.linspace(0, 2 * np.pi, 2000)

    a, b = 3.0, 4.0  # 3 sinx + 4 cosx = 5 sin(x+φ), R=5, tanφ=b/a
    R = np.hypot(a, b)
    phi = np.arctan2(b, a)

    y1 = a * np.sin(x)
    y2 = b * np.cos(x)
    ysum = a * np.sin(x) + b * np.cos(x)
    combined = R * np.sin(x + phi)
    np.testing.assert_allclose(ysum, combined, rtol=0.0, atol=1e-12)
    if not np.isclose(R, 5.0):
        raise AssertionError("合成振幅必須是 sqrt(3^2+4^2)=5")

    ax.plot(
        x,
        y1,
        color=F.BLUE,
        lw=1.8,
        ls=(0, (7, 3)),
        marker="o",
        markevery=200,
        ms=3.2,
        label=r"$3\sin x$",
    )
    ax.plot(
        x,
        y2,
        color=F.GREEN,
        lw=1.8,
        ls=(0, (2, 2)),
        marker="s",
        markevery=200,
        ms=3.0,
        label=r"$4\cos x$",
    )
    ax.plot(x, ysum, color=F.RED, lw=3.0, label=r"$3\sin x+4\cos x=5\sin(x+\varphi)$")

    # 振幅 R 標示
    ax.axhline(R, color="#9aa0a6", lw=1.0, ls=":")
    ax.axhline(-R, color="#9aa0a6", lw=1.0, ls=":")
    ax.text(
        0.15,
        R + 0.12,
        "$R=5$",
        color=F.RED,
        fontsize=12,
        ha="left",
        va="bottom",
    )

    ax.axhline(0, color=F.INK, lw=1.0)
    ax.axvline(0, color=F.INK, lw=1.0)
    ax.set_ylim(-5.8, 6.4)
    ax.set_yticks([-5, 0, 5])
    _pi_ticks(ax, 2.0, step=0.5)
    ax.set_xlim(-0.1, 2 * np.pi + 0.1)
    F.clean_grid(ax)
    ax.legend(loc="upper right", fontsize=11, framealpha=0.95)
    ax.set_title("正餘弦的疊合：兩同頻波合成單一正弦波", fontsize=14)
    _save(fig, "數A3-1-疊合")


if __name__ == "__main__":
    fig_radian_sector()
    fig_sine_cosine_graphs()
    fig_tangent_graph()
    fig_transform()
    fig_sum_diff_circle()
    fig_superpose()
    print("done.")
