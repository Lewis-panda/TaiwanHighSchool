# -*- coding: utf-8 -*-
"""產生必修物理「物體的運動」學生講義所需的 SVG。

重繪：.venv/bin/python _tools/fig_content_必物-3.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, Ellipse, FancyBboxPatch, Polygon, Rectangle

import figlib as F


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CH = os.path.join(ROOT, "content", "必修物理", "必物-3")

# 供章節登錄程式直接取得「入口函式 → 輸出檔名」映射。
FIGURE_OUTPUTS = (
    ("fig_galileo_model", "必物-3-伽利略理想化.svg"),
    ("fig_coordinate_states", "必物-3-等時間位置與座標.svg"),
    ("fig_motion_graphs", "必物-3-運動圖斜率與面積.svg"),
    ("fig_free_fall_states", "必物-3-自由落體時間狀態.svg"),
    ("fig_newton_second_data", "必物-3-牛頓第二定律資料.svg"),
    ("fig_horizontal_fbd", "必物-3-水平面受力圖.svg"),
    ("fig_balance_and_pair", "必物-3-平衡力與第三定律.svg"),
    ("fig_normal_force_cases", "必物-3-正向力三情形.svg"),
    ("fig_friction_response", "必物-3-摩擦力隨外力.svg"),
    ("fig_circular_vectors", "必物-3-圓周速度與向心.svg"),
    ("fig_kepler_laws", "必物-3-克卜勒三定律.svg"),
    ("fig_integrated_problems", "必物-3-章末解題圖.svg"),
)


def _save(fig, filename):
    if not filename.endswith(".svg"):
        raise ValueError("輸出檔名必須以 .svg 結尾")
    return F.save_to(
        fig,
        CH,
        filename[:-4],
        output_subdir="assets",
        write_pdf=False,
    )


def _panel_label(ax, label, title):
    ax.text(
        0.02,
        0.97,
        label,
        transform=ax.transAxes,
        ha="left",
        va="top",
        fontsize=12.5,
        color=F.BLUE,
        weight="bold",
    )
    ax.set_title(title, fontsize=12.8, pad=10)


def _block(ax, center, width=0.86, height=0.58, text="m"):
    x, y = center
    rect = FancyBboxPatch(
        (x - width / 2, y - height / 2),
        width,
        height,
        boxstyle="round,pad=0.02,rounding_size=0.08",
        facecolor="#fde68a",
        edgecolor="#92400e",
        lw=1.7,
        zorder=4,
    )
    ax.add_patch(rect)
    ax.text(x, y, text, ha="center", va="center", fontsize=12, zorder=6)
    return np.array([x, y], dtype=float)


def fig_galileo_model(filename):
    """伽利略從斜面實驗過渡到無阻力的慣性模型。"""
    fig, axes = plt.subplots(1, 3, figsize=(11.4, 4.0), facecolor="white")

    for ax in axes:
        ax.set_aspect("equal")
        ax.axis("off")

    ax = axes[0]
    _panel_label(ax, "A", "真實斜面：耗損機械能")
    ax.plot([-2.0, 0, 2.0], [2.0, 0, 2.0], color="#64748b", lw=2.0)
    ax.add_patch(Circle((-1.55, 1.55), 0.13, fc="#f59e0b", ec="#92400e", zorder=5))
    ax.add_patch(Circle((1.22, 1.22), 0.13, fc="#f59e0b", ec="#92400e", zorder=5))
    ax.plot([-1.55, 0, 1.22], [1.55, 0.05, 1.22], color=F.BLUE, lw=2.1, ls="--")
    ax.plot([-1.82, 1.82], [1.55, 1.55], color="#94a3b8", lw=1.0, ls=":")
    ax.text(0, -0.42, "實際回升高度較低", ha="center", fontsize=11)

    ax = axes[1]
    _panel_label(ax, "B", "降低阻力：回到同高")
    ax.plot([-2.0, 0, 2.0], [2.0, 0, 2.0], color="#64748b", lw=2.0)
    ax.add_patch(Circle((-1.55, 1.55), 0.13, fc="#f59e0b", ec="#92400e", zorder=5))
    ax.add_patch(Circle((1.55, 1.55), 0.13, fc="#f59e0b", ec="#92400e", zorder=5))
    ax.plot([-1.55, 0, 1.55], [1.55, 0.05, 1.55], color=F.BLUE, lw=2.1, ls="--")
    ax.plot([-1.82, 1.82], [1.55, 1.55], color=F.GREEN, lw=1.2, ls=":")
    ax.text(0, -0.42, "理想模型保留初始高度", ha="center", fontsize=11)

    ax = axes[2]
    _panel_label(ax, "C", "右側放平：等速延續")
    ax.plot([-2.0, 0], [2.0, 0], color="#64748b", lw=2.0)
    ax.plot([0, 2.15], [0, 0], color="#64748b", lw=2.0)
    ax.add_patch(Circle((-1.55, 1.55), 0.13, fc="#f59e0b", ec="#92400e", zorder=5))
    for x in (0.50, 1.20, 1.90):
        ax.add_patch(Circle((x, 0.13), 0.10, fc="#dbeafe", ec=F.BLUE, zorder=5))
    F.arrow(ax, (0.25, 0.55), (1.95, 0.55), color=F.BLUE, lw=2.4, mutation=15)
    ax.text(1.10, 0.78, "速度保持", color=F.BLUE, ha="center", fontsize=11)
    ax.text(0, -0.42, "無合力時，水平運動繼續", ha="center", fontsize=11)

    for ax in axes:
        ax.set_xlim(-2.25, 2.25)
        ax.set_ylim(-0.65, 2.35)
    fig.suptitle("理想化把摩擦影響逐步抽離，顯露慣性", fontsize=15.5, y=0.99)
    fig.tight_layout(rect=[0, 0, 1, 0.92], w_pad=1.0)
    _save(fig, filename)


def fig_coordinate_states(filename):
    """座標、時間狀態、位移與路徑長的對照。"""
    times = np.array([0.0, 2.0, 5.0, 7.0])
    positions = np.array([-3.0, 1.0, 4.0, 0.0])
    path_length = np.abs(np.diff(positions)).sum()
    displacement = positions[-1] - positions[0]
    assert np.isclose(path_length, 11.0)
    assert np.isclose(displacement, 3.0)

    fig, ax = F.schematic(10.8, 4.3)
    ax.plot([-4.4, 5.0], [0, 0], color=F.INK, lw=1.7)
    F.arrow(ax, (4.65, 0), (5.05, 0), color=F.INK, lw=1.7, mutation=14)
    for tick in range(-4, 6):
        ax.plot([tick, tick], [-0.10, 0.10], color=F.INK, lw=1.1)
        ax.text(tick, -0.32, f"{tick}", ha="center", va="top", fontsize=10.5)
    ax.text(5.15, -0.05, "$x$ (m)", va="center", fontsize=11.5)

    colors = [F.BLUE, F.GREEN, F.PURPLE, F.RED]
    heights = [1.25, 1.85, 1.25, 0.72]
    for index, (t, x, color, height) in enumerate(zip(times, positions, colors, heights)):
        ax.add_patch(Circle((x, 0), 0.15, fc=color, ec="white", lw=1.2, zorder=6))
        ax.plot([x, x], [0.18, height - 0.18], color=color, lw=1.0, ls=":")
        ax.text(x, height, rf"$t={t:g}\,\mathrm{{s}}$", color=color, ha="center", fontsize=11.3)
        ax.text(x, height - 0.32, rf"$x={x:g}\,\mathrm{{m}}$", color=color, ha="center", fontsize=10.5)
        if index < len(positions) - 1:
            y = 2.42 if index % 2 == 0 else 2.78
            F.arrow(ax, (x, y), (positions[index + 1], y), color=color, lw=2.1, mutation=13)

    ax.text(
        0.3,
        -1.05,
        r"位移 $\Delta x=x_f-x_i=0-(-3)=+3\ \mathrm{m}$"
        + "\n"
        + r"路徑長 $s=4+3+4=11\ \mathrm{m}$",
        ha="center",
        va="center",
        fontsize=12.2,
        linespacing=1.5,
    )
    ax.set_xlim(-4.6, 5.5)
    ax.set_ylim(-1.45, 3.15)
    ax.set_title("位移只比較首尾座標；路徑長累加每段實際路程", fontsize=15, pad=10)
    _save(fig, filename)


def fig_motion_graphs(filename):
    """x–t 圖斜率與 v–t 圖面積的數值對照。"""
    t_position = np.array([0.0, 2.0, 5.0, 8.0])
    x_position = np.array([-2.0, 4.0, 4.0, -2.0])
    slopes = np.diff(x_position) / np.diff(t_position)
    assert np.allclose(slopes, [3.0, 0.0, -2.0])

    t_velocity = np.linspace(0.0, 4.0, 300)
    velocity = 2.0 + t_velocity
    displacement = np.trapezoid(velocity, t_velocity)
    assert np.isclose(displacement, 16.0, atol=2e-4)

    fig, axes = plt.subplots(1, 2, figsize=(11.1, 4.7), facecolor="white")
    ax = axes[0]
    ax.plot(t_position, x_position, color=F.BLUE, lw=2.8, marker="o", ms=7)
    ax.axhline(0, color="#94a3b8", lw=1.0)
    ax.text(0.85, 1.6, r"$v=+3\ \mathrm{m/s}$", color=F.BLUE, fontsize=11)
    ax.text(3.05, 4.45, r"$v=0$", color=F.GREEN, fontsize=11)
    ax.text(6.25, 1.3, r"$v=-2\ \mathrm{m/s}$", color=F.RED, fontsize=11)
    ax.set_xlim(-0.2, 8.4)
    ax.set_ylim(-2.8, 5.2)
    ax.set_xlabel("$t$ (s)")
    ax.set_ylabel("$x$ (m)")
    _panel_label(ax, "A", "$x$--$t$ 圖：割線斜率是速度")
    F.clean_grid(ax)

    ax = axes[1]
    ax.plot(t_velocity, velocity, color=F.RED, lw=2.8)
    ax.fill_between(t_velocity, 0, velocity, color=F.FILL, alpha=0.18)
    ax.plot([0, 4], [2, 2], color=F.GREEN, lw=1.4, ls="--")
    ax.plot([4, 4], [0, 6], color="#94a3b8", lw=1.1, ls=":")
    ax.text(2.0, 1.0, r"長方形 $2\times4=8$", ha="center", color=F.GREEN, fontsize=10.8)
    ax.text(2.7, 4.2, r"三角形 $\frac{1}{2}(4)(4)=8$", ha="center", color=F.RED, fontsize=10.8)
    ax.text(2.0, 6.55, r"$\Delta x=8+8=16\ \mathrm{m}$", ha="center", fontsize=12)
    ax.set_xlim(-0.2, 4.4)
    ax.set_ylim(0, 7.1)
    ax.set_xlabel("$t$ (s)")
    ax.set_ylabel("$v$ (m/s)")
    _panel_label(ax, "B", "$v$--$t$ 圖：帶正負號面積是位移")
    F.clean_grid(ax)

    fig.suptitle("運動圖的幾何量直接對應物理量", fontsize=15.5, y=0.99)
    fig.tight_layout(rect=[0, 0, 1, 0.93], w_pad=1.8)
    _save(fig, filename)


def fig_free_fall_states(filename):
    """自由落體的等時間位置、速度與正向座標。"""
    g = 10.0
    times = np.arange(0.0, 4.0)
    distances = 0.5 * g * times**2
    speeds = g * times
    assert np.allclose(distances, [0.0, 5.0, 20.0, 45.0])
    assert np.allclose(speeds, [0.0, 10.0, 20.0, 30.0])

    fig, ax = F.canvas(7.8, 6.0)
    ax.set_aspect("auto")
    ax.axis("off")
    ax.plot([0, 0], [4, -49], color="#64748b", lw=1.4)
    F.arrow(ax, (0, 2.0), (0, -49.0), color=F.INK, lw=1.5, mutation=14)
    ax.text(0.15, -48.0, "$+y$", fontsize=11.5)

    for t, y, v in zip(times, -distances, speeds):
        ax.add_patch(Circle((0, y), 0.22, fc="#f59e0b", ec="#92400e", zorder=5))
        ax.plot([-0.35, 2.0], [y, y], color="#cbd5e1", lw=0.9, ls=":")
        ax.text(2.2, y, rf"$t={t:g}\,\mathrm{{s}},\ y={-y:g}\,\mathrm{{m}}$", va="center", fontsize=11.3)
        if v > 0:
            length = 0.22 * v
            F.arrow(ax, (0.45, y), (0.45, y - length), color=F.BLUE, lw=2.5, mutation=15)
            ax.text(0.68, y - 0.5 * length, rf"$v={v:g}\,\mathrm{{m/s}}$", color=F.BLUE, va="center", fontsize=10.8)
        else:
            ax.text(0.55, y + 0.2, "$v_0=0$", color=F.BLUE, va="bottom", fontsize=10.8)

    ax.text(
        -2.8,
        -24,
        r"$g=10\ \mathrm{m/s^2}$"
        + "\n"
        + r"$v=gt$"
        + "\n"
        + r"$y=\frac{1}{2}gt^2$",
        fontsize=13,
        linespacing=1.55,
        bbox=dict(boxstyle="round,pad=0.45", fc="#eff6ff", ec="#93c5fd"),
    )
    ax.set_xlim(-3.4, 5.6)
    ax.set_ylim(-51, 6)
    ax.set_title("忽略空氣阻力時，每秒向下增加同樣的速度", fontsize=15, pad=10)
    _save(fig, filename)


def fig_newton_second_data(filename):
    """從可檢驗資料建立合力、質量與加速度的關係。"""
    forces = np.array([0.0, 2.0, 4.0, 6.0])
    a_m1 = forces / 1.0
    a_m2 = forces / 2.0
    masses = np.array([0.5, 1.0, 1.5, 2.0])
    fixed_acceleration = 2.0
    needed_force = masses * fixed_acceleration
    assert np.allclose(a_m1 / np.where(forces == 0, 1, forces), [0, 1, 1, 1])
    assert np.allclose(a_m2[1:] / forces[1:], 0.5)
    assert np.allclose(needed_force / masses, fixed_acceleration)

    fig, axes = plt.subplots(1, 2, figsize=(10.8, 4.6), facecolor="white")
    ax = axes[0]
    ax.plot(forces, a_m1, color=F.BLUE, lw=2.6, marker="o", label="$m=1.0$ kg")
    ax.plot(forces, a_m2, color=F.RED, lw=2.6, marker="s", label="$m=2.0$ kg")
    ax.set_xlabel(r"水平合力 $\Sigma F_x$ (N)")
    ax.set_ylabel(r"加速度 $a_x$ (m/s$^2$)")
    ax.legend(frameon=False, loc="upper left")
    _panel_label(ax, "A", "同一質量：加速度與合力成正比")
    F.clean_grid(ax)

    ax = axes[1]
    ax.plot(masses, needed_force, color=F.GREEN, lw=2.6, marker="o")
    ax.set_xlabel("質量 $m$ (kg)")
    ax.set_ylabel(r"所需合力 $\Sigma F_x$ (N)")
    ax.text(1.25, 3.5, r"斜率 $=a=2.0\ \mathrm{m/s^2}$", ha="center", fontsize=11.2)
    _panel_label(ax, "B", "同一加速度：質量加倍需兩倍合力")
    F.clean_grid(ax)

    fig.suptitle(r"兩組資料合併為 $\sum\vec F=m\vec a$", fontsize=15.5, y=0.99)
    fig.tight_layout(rect=[0, 0, 1, 0.92], w_pad=1.8)
    _save(fig, filename)


def fig_horizontal_fbd(filename):
    """水平面運動例的實體、座標與成比例受力箭頭。"""
    mass = 2.0
    gravity = 10.0
    normal = mass * gravity
    applied = 18.0
    friction = 6.0
    acceleration = (applied - friction) / mass
    assert np.isclose(normal, 20.0)
    assert np.isclose(acceleration, 6.0)

    fig, axes = plt.subplots(1, 2, figsize=(11.0, 4.5), facecolor="white")
    for ax in axes:
        ax.set_aspect("equal")
        ax.axis("off")

    ax = axes[0]
    _panel_label(ax, "A", "限定物體與正方向")
    ax.plot([-2.4, 2.4], [-0.5, -0.5], color="#64748b", lw=2.0)
    center = _block(ax, (0, 0), text="2.0 kg")
    F.arrow(ax, center + np.array([0.55, 0]), center + np.array([2.35, 0]), color=F.GREEN, lw=3.0)
    ax.text(1.55, 0.22, "$18$ N", color=F.GREEN, ha="center", fontsize=11.5)
    F.arrow(ax, center + np.array([-0.55, 0]), center + np.array([-1.15, 0]), color=F.AMBER, lw=3.0)
    ax.text(-0.90, 0.22, "$6$ N", color=F.AMBER, ha="center", fontsize=11.5)
    F.arrow(ax, (-1.9, -1.45), (-0.9, -1.45), color=F.INK, lw=1.5, mutation=13)
    F.arrow(ax, (-1.9, -1.45), (-1.9, -0.65), color=F.INK, lw=1.5, mutation=13)
    ax.text(-0.78, -1.45, "$+x$", fontsize=10.5)
    ax.text(-1.9, -0.52, "$+y$", fontsize=10.5, ha="center")

    ax = axes[1]
    _panel_label(ax, "B", "只留外界對此物體的作用")
    center = np.array([0.0, 0.0])
    ax.add_patch(Circle(center, 0.07, fc=F.INK, zorder=7))
    scale = 0.105
    F.arrow(ax, center, center + np.array([applied * scale, 0]), color=F.GREEN, lw=3.0)
    F.arrow(ax, center, center + np.array([-friction * scale, 0]), color=F.AMBER, lw=3.0)
    F.arrow(ax, center, center + np.array([0, normal * scale]), color=F.BLUE, lw=3.0)
    F.arrow(ax, center, center + np.array([0, -mass * gravity * scale]), color=F.RED, lw=3.0)
    ax.text(1.25, 0.24, "$F=18$ N", color=F.GREEN, ha="center", fontsize=11)
    ax.text(-0.55, 0.24, "$f=6$ N", color=F.AMBER, ha="center", fontsize=11)
    ax.text(0.18, 1.25, "$N=20$ N", color=F.BLUE, fontsize=11)
    ax.text(0.18, -1.45, "$mg=20$ N", color=F.RED, fontsize=11)
    ax.text(0, -2.55, r"$\Sigma F_x=18-6=ma_x\Rightarrow a_x=6.0\ \mathrm{m/s^2}$", ha="center", fontsize=11.7)
    ax.text(0, -2.98, r"$\Sigma F_y=N-mg=0$", ha="center", fontsize=11.7)

    for ax in axes:
        ax.set_xlim(-2.7, 2.7)
        ax.set_ylim(-3.15, 2.65)
    fig.suptitle("受力圖把互動箭頭轉成分方向的合力方程", fontsize=15, y=0.99)
    fig.tight_layout(rect=[0, 0, 1, 0.92], w_pad=1.0)
    _save(fig, filename)


def fig_balance_and_pair(filename):
    """對照同一物體上的平衡力與分屬兩物體的第三定律力對。"""
    fig, axes = plt.subplots(1, 3, figsize=(11.5, 4.2), facecolor="white")
    for ax in axes:
        ax.set_aspect("equal")
        ax.axis("off")

    ax = axes[0]
    _panel_label(ax, "A", "書的自由體圖")
    center = _block(ax, (0, 0), width=1.3, height=0.75, text="書")
    F.arrow(ax, center, center + np.array([0, 1.40]), color=F.BLUE, lw=3.0)
    F.arrow(ax, center, center + np.array([0, -1.40]), color=F.RED, lw=3.0)
    ax.text(0.18, 1.02, r"$\vec N_{T\to B}$", color=F.BLUE, fontsize=11)
    ax.text(0.18, -1.12, r"$\vec W_{E\to B}$", color=F.RED, fontsize=11)
    ax.text(0, -2.0, "兩力在同一物體上\n合力為零", ha="center", fontsize=11, linespacing=1.45)

    ax = axes[1]
    _panel_label(ax, "B", "重力的互動力對")
    earth = Circle((0, -0.65), 0.78, fc="#bfdbfe", ec=F.BLUE, lw=1.6)
    book = Rectangle((-0.34, 1.05), 0.68, 0.42, fc="#fde68a", ec="#92400e", lw=1.5)
    ax.add_patch(earth)
    ax.add_patch(book)
    F.arrow(ax, (0, 1.22), (0, 0.30), color=F.RED, lw=2.8)
    F.arrow(ax, (0, -0.05), (0, 0.87), color=F.PURPLE, lw=2.8)
    ax.text(0.18, 0.72, r"$\vec W_{E\to B}$", color=F.RED, fontsize=10.2)
    ax.text(0.18, 0.06, r"$\vec F_{B\to E}$", color=F.PURPLE, fontsize=10.2)
    ax.text(0, -2.0, "大小相等、方向相反\n分別作用在書與地球", ha="center", fontsize=11, linespacing=1.45)

    ax = axes[2]
    _panel_label(ax, "C", "接觸力的互動力對")
    ax.plot([-1.2, 1.2], [-0.25, -0.25], color="#64748b", lw=5.0)
    ax.add_patch(Rectangle((-0.48, -0.05), 0.96, 0.62, fc="#fde68a", ec="#92400e", lw=1.5))
    F.arrow(ax, (0, 0.15), (0, 1.35), color=F.BLUE, lw=2.8)
    F.arrow(ax, (0, -0.18), (0, -1.38), color=F.GREEN, lw=2.8)
    ax.text(0.16, 1.02, r"$\vec N_{T\to B}$", color=F.BLUE, fontsize=10.2)
    ax.text(0.16, -1.08, r"$\vec N_{B\to T}$", color=F.GREEN, fontsize=10.2)
    ax.text(0, -2.0, "來自同一次書桌接觸\n同時出現在兩個物體", ha="center", fontsize=11, linespacing=1.45)

    for ax in axes:
        ax.set_xlim(-1.65, 1.65)
        ax.set_ylim(-2.35, 2.05)
    fig.suptitle("平衡力回答一個物體的運動；互動力對連接兩個物體", fontsize=15, y=0.99)
    fig.tight_layout(rect=[0, 0, 1, 0.91], w_pad=0.8)
    _save(fig, filename)


def fig_normal_force_cases(filename):
    """根據鉛直平衡方程畫出三種正向力。"""
    weight = 40.0
    extra = 10.0
    cases = (
        ("無額外鉛直力", 0.0, "none", weight),
        ("外力向下 10 N", extra, "down", weight + extra),
        ("外力向上 10 N", extra, "up", weight - extra),
    )
    assert [case[3] for case in cases] == [40.0, 50.0, 30.0]

    fig, axes = plt.subplots(1, 3, figsize=(11.3, 4.3), facecolor="white")
    scale = 0.034
    for index, (title, force, direction, normal) in enumerate(cases):
        ax = axes[index]
        ax.set_aspect("equal")
        ax.axis("off")
        _panel_label(ax, chr(ord("A") + index), title)
        ax.plot([-1.45, 1.45], [-0.55, -0.55], color="#64748b", lw=2.2)
        center = _block(ax, (0, 0), width=1.1, height=0.72, text="4.0 kg")
        F.arrow(ax, center, center + np.array([0, normal * scale]), color=F.BLUE, lw=3.0)
        F.arrow(ax, center, center + np.array([0, -weight * scale]), color=F.RED, lw=3.0)
        ax.text(0.15, 0.62 * normal * scale, rf"$N={normal:g}$ N", color=F.BLUE, fontsize=10.8)
        ax.text(0.15, -0.68 * weight * scale, "$mg=40$ N", color=F.RED, fontsize=10.8)
        if direction == "down":
            F.arrow(ax, (-0.70, 0.85), (-0.70, 0.85 - force * scale), color=F.PURPLE, lw=2.5)
            ax.text(-0.92, 0.52, "$F=10$ N", color=F.PURPLE, fontsize=10.3, ha="right")
            equation = "$N-mg-F=0$"
        elif direction == "up":
            F.arrow(ax, (-0.70, 0.45), (-0.70, 0.45 + force * scale), color=F.PURPLE, lw=2.5)
            ax.text(-0.92, 0.72, "$F=10$ N", color=F.PURPLE, fontsize=10.3, ha="right")
            equation = "$N+F-mg=0$"
        else:
            equation = "$N-mg=0$"
        ax.text(0, -2.05, equation, ha="center", fontsize=11.5)
        ax.set_xlim(-1.7, 1.7)
        ax.set_ylim(-2.25, 2.25)

    fig.suptitle("正向力是接觸面為滿足運動狀態而產生的力", fontsize=15, y=0.99)
    fig.tight_layout(rect=[0, 0, 1, 0.91], w_pad=0.9)
    _save(fig, filename)


def fig_friction_response(filename):
    """靜摩擦調整區、最大靜摩擦與動摩擦的資料圖。"""
    maximum_static = 8.0
    kinetic = 6.0
    applied_static = np.linspace(0.0, maximum_static, 200)
    friction_static = applied_static
    applied_kinetic = np.linspace(maximum_static + 0.18, 14.0, 200)
    friction_kinetic = np.full_like(applied_kinetic, kinetic)
    assert np.allclose(friction_static, applied_static)
    assert kinetic < maximum_static

    fig, ax = F.canvas(9.5, 5.2)
    ax.plot(applied_static, friction_static, color=F.BLUE, lw=3.0)
    ax.scatter([maximum_static], [maximum_static], color=F.BLUE, s=75, zorder=5)
    ax.plot(applied_kinetic, friction_kinetic, color=F.RED, lw=3.0)
    ax.scatter([maximum_static + 0.18], [kinetic], color=F.RED, s=75, zorder=5)
    ax.axvline(maximum_static, color="#94a3b8", lw=1.3, ls="--")
    ax.fill_between(applied_static, 0, friction_static, color=F.BLUE, alpha=0.08)
    ax.text(3.7, 4.4, r"靜止：$|f_s|=|F|$", color=F.BLUE, fontsize=12)
    ax.text(8.35, 8.15, r"$f_{s,\max}=8$ N", color=F.BLUE, fontsize=11.2)
    ax.text(10.7, 6.35, r"滑動：$|f_k|=6$ N", color=F.RED, fontsize=12, ha="center")
    ax.text(9.8, 2.0, "摩擦力方向沿接觸面\n抑制相對滑動或其趨勢", ha="center", fontsize=11.3, linespacing=1.45)
    ax.set_xlim(0, 14.5)
    ax.set_ylim(0, 9.3)
    ax.set_xlabel(r"水平外力大小 $|F|$ (N)")
    ax.set_ylabel(r"摩擦力大小 $|f|$ (N)")
    ax.set_title("推力逐漸增加時，靜摩擦先自動配合，滑動後轉為動摩擦", fontsize=14.5, pad=12)
    F.clean_grid(ax)
    fig.tight_layout()
    _save(fig, filename)


def fig_circular_vectors(filename):
    """等速圓周運動的切向速度與向心加速度。"""
    radius = 1.75
    points = [
        (np.array([radius, 0.0]), np.array([0.0, 1.0])),
        (np.array([0.0, radius]), np.array([-1.0, 0.0])),
        (np.array([-radius, 0.0]), np.array([0.0, -1.0])),
    ]
    for position, tangent in points:
        radial = -position / np.linalg.norm(position)
        assert np.isclose(np.dot(radial, tangent), 0.0)

    fig, axes = plt.subplots(1, 2, figsize=(10.8, 4.8), facecolor="white")
    ax = axes[0]
    ax.set_aspect("equal")
    ax.axis("off")
    ax.add_patch(Circle((0, 0), radius, fill=False, ec="#94a3b8", lw=1.8))
    ax.add_patch(Circle((0, 0), 0.09, fc=F.INK))
    ax.text(0.12, -0.20, "$O$", fontsize=11)
    for position, tangent in points:
        radial = -position / np.linalg.norm(position)
        ax.add_patch(Circle(position, 0.12, fc="#fde68a", ec="#92400e", zorder=5))
        F.arrow(ax, position, position + 0.95 * tangent, color=F.BLUE, lw=2.7, mutation=15)
        F.arrow(ax, position, position + 0.88 * radial, color=F.RED, lw=2.7, mutation=15)
    ax.text(1.95, 0.68, "$\\vec v$", color=F.BLUE, fontsize=12)
    ax.text(0.95, -0.20, "$\\vec a_c$", color=F.RED, fontsize=12)
    ax.text(-0.96, 1.95, "$\\vec v$", color=F.BLUE, fontsize=12)
    _panel_label(ax, "A", "速度永遠沿切線，加速度指向圓心")
    ax.set_xlim(-2.7, 2.7)
    ax.set_ylim(-2.45, 2.55)

    ax = axes[1]
    ax.set_aspect("equal")
    ax.axis("off")
    theta = np.deg2rad(38)
    v1 = np.array([1.45, 0.0])
    v2 = 1.45 * np.array([np.cos(theta), np.sin(theta)])
    delta_v = v2 - v1
    origin = np.array([-0.8, -0.65])
    F.arrow(ax, origin, origin + v1, color=F.BLUE, lw=2.7)
    F.arrow(ax, origin, origin + v2, color=F.PURPLE, lw=2.7)
    F.arrow(ax, origin + v1, origin + v2, color=F.RED, lw=2.7)
    ax.text(*(origin + 0.60 * v1 + np.array([0, -0.22])), "$\\vec v_1$", color=F.BLUE, fontsize=12)
    ax.text(*(origin + 0.57 * v2 + np.array([-0.18, 0.12])), "$\\vec v_2$", color=F.PURPLE, fontsize=12)
    ax.text(*(origin + v1 + 0.52 * delta_v + np.array([0.18, 0])), r"$\Delta\vec v$", color=F.RED, fontsize=12)
    ax.text(0, -1.72, r"$\vec a_{\mathrm{avg}}=\Delta\vec v/\Delta t$", ha="center", fontsize=12.5)
    ax.text(0, -2.12, "速率相同仍有速度方向變化", ha="center", fontsize=11.2)
    _panel_label(ax, "B", "向量差顯示加速度的來源")
    ax.set_xlim(-2.25, 2.25)
    ax.set_ylim(-2.45, 2.45)

    fig.suptitle("圓周運動需要持續指向圓心的合力來改變速度方向", fontsize=15, y=0.99)
    fig.tight_layout(rect=[0, 0, 1, 0.92], w_pad=1.1)
    _save(fig, filename)


def _solve_kepler(mean_anomaly, eccentricity):
    eccentric_anomaly = np.array(mean_anomaly, dtype=float)
    for _ in range(15):
        eccentric_anomaly -= (
            eccentric_anomaly
            - eccentricity * np.sin(eccentric_anomaly)
            - mean_anomaly
        ) / (1.0 - eccentricity * np.cos(eccentric_anomaly))
    return eccentric_anomaly


def _orbit_xy(eccentric_anomaly, semimajor=2.15, eccentricity=0.55):
    semiminor = semimajor * np.sqrt(1.0 - eccentricity**2)
    return np.column_stack(
        (semimajor * np.cos(eccentric_anomaly), semiminor * np.sin(eccentric_anomaly))
    )


def fig_kepler_laws(filename):
    """以焦點、等時間等面積與週期資料呈現克卜勒三定律。"""
    a = 2.15
    e = 0.55
    b = a * np.sqrt(1.0 - e**2)
    c = a * e
    assert np.isclose(c**2, a**2 - b**2)
    # x=a cos E 的近點在右側；用 M=E-e sin E 時對應的中心天體在 +c 焦點。
    focus = np.array([c, 0.0])

    fig, axes = plt.subplots(1, 3, figsize=(12.0, 4.5), facecolor="white")
    for ax in axes[:2]:
        ax.set_aspect("equal")
        ax.axis("off")

    ax = axes[0]
    ax.add_patch(Ellipse((0, 0), 2 * a, 2 * b, fill=False, ec=F.BLUE, lw=2.1))
    ax.add_patch(Circle(focus, 0.16, fc="#f59e0b", ec="#92400e", zorder=5))
    ax.plot([0], [0], marker="+", color="#64748b", ms=10, mew=1.5)
    ax.plot([-c, c], [0, 0], "o", color="#94a3b8", ms=4)
    ax.text(focus[0], -0.36, "太陽（焦點）", ha="center", fontsize=10.3)
    ax.text(0.12, 0.16, "橢圓中心", fontsize=10.3, color="#64748b")
    ax.text(0, -2.15, "行星軌道為橢圓\n太陽位於其中一個焦點", ha="center", fontsize=11.2, linespacing=1.45)
    _panel_label(ax, "A｜第一定律", "軌道幾何")
    ax.set_xlim(-2.65, 2.65)
    ax.set_ylim(-2.35, 2.35)

    ax = axes[1]
    ax.add_patch(Ellipse((0, 0), 2 * a, 2 * b, fill=False, ec="#64748b", lw=1.6))
    delta_mean = 0.46
    intervals = [(-delta_mean / 2, delta_mean / 2), (np.pi - delta_mean / 2, np.pi + delta_mean / 2)]
    colors = [F.RED, F.BLUE]
    polygon_areas = []
    for (m1, m2), color in zip(intervals, colors):
        means = np.linspace(m1, m2, 100)
        eccentric_anomalies = _solve_kepler(means, e)
        points = _orbit_xy(eccentric_anomalies, a, e)
        polygon = np.vstack([focus, points, focus])
        ax.add_patch(Polygon(polygon, closed=True, fc=color, ec=color, alpha=0.24, lw=1.5))
        x = polygon[:, 0]
        y = polygon[:, 1]
        area = 0.5 * abs(np.dot(x, np.roll(y, 1)) - np.dot(y, np.roll(x, 1)))
        polygon_areas.append(area)
    assert np.isclose(polygon_areas[0], polygon_areas[1], rtol=2e-3)
    ax.add_patch(Circle(focus, 0.15, fc="#f59e0b", ec="#92400e", zorder=5))
    ax.text(0, -2.12, "相等時間掃過相等面積\n近日點路程較長，速率較大", ha="center", fontsize=11.2, linespacing=1.45)
    _panel_label(ax, "B｜第二定律", "面積律與速率")
    ax.set_xlim(-2.65, 2.65)
    ax.set_ylim(-2.35, 2.35)

    ax = axes[2]
    radii = np.array([1.0, 1.5, 2.0, 2.5])
    periods = radii ** 1.5
    ax.plot(radii**3, periods**2, color=F.GREEN, lw=2.6)
    ax.scatter(radii**3, periods**2, color=F.RED, s=55, zorder=5)
    for radius, period in zip(radii[:3], periods[:3]):
        ax.text(radius**3 + 0.15, period**2 - 0.45, rf"$a={radius:g},\ T={period:.2f}$", fontsize=9.5)
    ax.set_xlabel(r"$a^3$（距離立方）")
    ax.set_ylabel(r"$T^2$（週期平方）")
    _panel_label(ax, "C｜第三定律", r"同一中心天體：$T^2/a^3$ 固定")
    F.clean_grid(ax)
    ax.text(7.8, 13.8, r"$T^2\propto a^3$", color=F.GREEN, fontsize=12.5)

    fig.suptitle("克卜勒定律將長期天文觀測壓縮成可檢驗的幾何與比例", fontsize=15, y=0.99)
    fig.tight_layout(rect=[0, 0, 1, 0.92], w_pad=1.0)
    _save(fig, filename)


def fig_integrated_problems(filename):
    """章末四題整合題的列式用圖。"""
    fig, axes = plt.subplots(2, 2, figsize=(11.4, 7.6), facecolor="white")
    axes = axes.ravel()

    ax = axes[0]
    reaction_time = 0.75
    initial_speed = 20.0
    braking_time = 4.0
    t = np.array([0.0, reaction_time, reaction_time + braking_time])
    v = np.array([initial_speed, initial_speed, 0.0])
    ax.plot(t, v, color=F.BLUE, lw=2.8, marker="o")
    ax.fill_between(t[:2], 0, v[:2], color=F.GREEN, alpha=0.20)
    t_brake = np.linspace(reaction_time, reaction_time + braking_time, 100)
    v_brake = initial_speed * (1 - (t_brake - reaction_time) / braking_time)
    ax.fill_between(t_brake, 0, v_brake, color=F.RED, alpha=0.18)
    ax.text(0.36, 10, "$15$ m", color=F.GREEN, ha="center", fontsize=11)
    ax.text(2.8, 8, "$40$ m", color=F.RED, ha="center", fontsize=11)
    ax.set_xlim(0, 5.0)
    ax.set_ylim(0, 23)
    ax.set_xlabel("$t$ (s)")
    ax.set_ylabel("$v$ (m/s)")
    _panel_label(ax, "整合 1", "反應與制動距離")
    F.clean_grid(ax)

    ax = axes[1]
    ax.set_aspect("equal")
    ax.axis("off")
    ax.add_patch(Rectangle((-1.45, -1.45), 2.9, 2.9, fill=False, ec="#64748b", lw=1.8))
    center = _block(ax, (0, 0), width=0.95, height=0.62, text="60 kg")
    F.arrow(ax, center, center + np.array([0, 1.25]), color=F.BLUE, lw=3.0)
    F.arrow(ax, center, center + np.array([0, -0.95]), color=F.RED, lw=3.0)
    F.arrow(ax, (1.80, -0.75), (1.80, 0.55), color=F.GREEN, lw=2.6)
    ax.text(0.18, 1.0, "$N=720$ N", color=F.BLUE, fontsize=10.8)
    ax.text(0.18, -0.83, "$mg=600$ N", color=F.RED, fontsize=10.8)
    ax.text(1.98, 0.38, "$a$ 向上", color=F.GREEN, fontsize=10.8)
    ax.text(0, -1.95, r"$N-mg=ma$", ha="center", fontsize=12)
    _panel_label(ax, "整合 2", "電梯秤讀數與加速度")
    ax.set_xlim(-2.2, 2.4)
    ax.set_ylim(-2.2, 2.2)

    ax = axes[2]
    ax.set_aspect("equal")
    ax.axis("off")
    ax.plot([-2.2, 2.2], [-0.6, -0.6], color="#64748b", lw=2.0)
    center = _block(ax, (0, 0), width=1.05, height=0.70, text="2.0 kg")
    F.arrow(ax, center + np.array([0.55, 0]), center + np.array([2.05, 0]), color=F.GREEN, lw=3.0)
    F.arrow(ax, center + np.array([-0.55, 0]), center + np.array([-1.30, 0]), color=F.AMBER, lw=3.0)
    ax.text(1.35, 0.25, "$F$ 逐漸增加", color=F.GREEN, ha="center", fontsize=10.5)
    ax.text(-0.95, 0.25, "$f$ 配合狀態", color=F.AMBER, ha="center", fontsize=10.5)
    ax.text(0, -1.35, r"先比較 $F$ 與 $f_{s,\max}$，再決定 $a$", ha="center", fontsize=11.3)
    _panel_label(ax, "整合 3", "外力、摩擦與運動狀態")
    ax.set_xlim(-2.4, 2.4)
    ax.set_ylim(-1.7, 2.0)

    ax = axes[3]
    ax.set_aspect("equal")
    ax.axis("off")
    star = np.array([0.0, 0.0])
    ax.add_patch(Circle(star, 0.16, fc="#f59e0b", ec="#92400e", zorder=5))
    for radius, color, label in ((0.9, F.BLUE, "A"), (1.8, F.RED, "B")):
        ax.add_patch(Circle(star, radius, fill=False, ec=color, lw=1.8))
        ax.add_patch(Circle((radius, 0), 0.09, fc=color, ec="white", zorder=5))
        ax.text(radius, 0.22, label, color=color, ha="center", fontsize=11, weight="bold")
    ax.text(0, -2.25, r"$R_B=2R_A\Rightarrow T_B/T_A=2^{3/2}$", ha="center", fontsize=11.8)
    _panel_label(ax, "整合 4", "同一恆星的兩顆行星")
    ax.set_xlim(-2.4, 2.4)
    ax.set_ylim(-2.55, 2.2)

    fig.suptitle("整合題先把時間區間、受力體與軌道關係畫出來", fontsize=15.5, y=0.99)
    fig.tight_layout(rect=[0, 0, 1, 0.94], h_pad=1.3, w_pad=1.2)
    _save(fig, filename)


def main():
    for entrypoint, filename in FIGURE_OUTPUTS:
        globals()[entrypoint](filename)
    print("done.")


if __name__ == "__main__":
    main()
