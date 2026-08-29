# -*- coding: utf-8 -*-
"""產生選物 I-2 章末完整解析使用的五張三欄 SVG。

重繪：.venv/bin/python _tools/fig_content_選物I-2_solutions.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyBboxPatch, Rectangle

import figlib as F


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CH = os.path.join(ROOT, "content", "選修物理I", "選物I-2")
OUTPUT_NAMES = (
    "選物I-2-章末解析01-04",
    "選物I-2-章末解析05-08",
    "選物I-2-章末解析09-11",
    "選物I-2-章末解析12-14",
    "選物I-2-章末解析15-18",
)


def _save(fig, name):
    assert name in OUTPUT_NAMES
    return F.save_to(fig, CH, name, output_subdir="assets", write_pdf=False)


def _sheet(title):
    fig, axes = plt.subplots(1, 3, figsize=(15.2, 5.15))
    fig.suptitle(title, fontsize=16, weight="bold", y=0.985)
    fig.subplots_adjust(left=0.045, right=0.985, top=0.86, bottom=0.13, wspace=0.27)
    return fig, axes


def _panel(ax, label, title, *, grid=False):
    ax.set_title(f"{label}　{title}", fontsize=12.4, weight="bold", loc="left", pad=9)
    ax.set_facecolor("#fbfdff")
    if grid:
        F.clean_grid(ax)
    else:
        for spine in ax.spines.values():
            spine.set_visible(False)


def _axis_arrow(ax, start, end, *, color=F.INK, lw=1.6, mutation=14):
    ax.annotate(
        "",
        xy=end,
        xytext=start,
        arrowprops=dict(arrowstyle="-|>", color=color, lw=lw, mutation_scale=mutation),
    )


def fig_01_04():
    """第 1、2、4 題：路徑、方向判斷與等加速度圖面積。"""
    fig, axes = _sheet("章末解析圖 7｜先把方向、端點與圖形面積畫進列式")

    # 第 1 題：位置數線與實際路徑。
    ax = axes[0]
    _panel(ax, "A｜第 1 題", "頭尾決定位移，分段長度決定路徑長")
    xi, xturn, xf = -2.0, 5.0, 1.0
    first_leg = abs(xturn - xi)
    second_leg = abs(xf - xturn)
    displacement = xf - xi
    assert np.isclose(first_leg, 7.0)
    assert np.isclose(second_leg, 4.0)
    assert np.isclose(displacement, 3.0)
    ax.plot([-2.7, 5.7], [0, 0], color=F.INK, lw=1.5)
    for x, text in ((xi, "$-2$"), (xf, "$1$"), (xturn, "$5$")):
        ax.plot([x, x], [-0.12, 0.12], color=F.INK, lw=1.3)
        ax.scatter([x], [0], s=52, color=F.INK, zorder=5)
        ax.text(x, -0.30, text, ha="center", va="top", fontsize=11.2)
    _axis_arrow(ax, (xi, 0.45), (xturn, 0.45), color=F.BLUE, lw=2.5)
    ax.text((xi + xturn) / 2, 0.61, r"第一段 $7\ \mathrm{m}$", ha="center", color=F.BLUE, fontsize=11.2)
    _axis_arrow(ax, (xturn, -0.52), (xf, -0.52), color=F.RED, lw=2.5)
    ax.text((xturn + xf) / 2, -0.70, r"第二段 $4\ \mathrm{m}$", ha="center", va="top", color=F.RED, fontsize=11.2)
    ax.text(1.5, 1.03, r"$\Delta x=1-(-2)=+3\ \mathrm{m}$", ha="center", fontsize=12.3, weight="bold")
    ax.text(1.5, -1.05, r"$s=7+4=11\ \mathrm{m}$", ha="center", fontsize=12.3, weight="bold")
    ax.set_xlim(-3.0, 6.0)
    ax.set_ylim(-1.30, 1.30)
    ax.axis("off")

    # 第 2 題：速度與加速度方向同異。
    ax = axes[1]
    _panel(ax, "B｜第 2 題", "比較兩支方向箭頭")
    cases = (
        ("甲", +1, +1, "同向｜變快"),
        ("乙", +1, -1, "反向｜變慢"),
        ("丙", -1, -1, "同向｜變快"),
        ("丁", -1, +1, "反向｜變慢"),
    )
    assert [v * a > 0 for _, v, a, _ in cases] == [True, False, True, False]
    for index, (name, v_sign, a_sign, result) in enumerate(cases):
        y = 3.25 - index
        ax.text(-2.08, y, name, fontsize=12, weight="bold", va="center")
        ax.scatter([0], [y], s=28, color=F.INK, zorder=5)
        _axis_arrow(ax, (0, y + 0.14), (1.20 * v_sign, y + 0.14), color=F.BLUE, lw=2.3)
        _axis_arrow(ax, (0, y - 0.14), (1.20 * a_sign, y - 0.14), color=F.RED, lw=2.3)
        ax.text(-1.72, y + 0.14, "$v$", color=F.BLUE, fontsize=11, va="center")
        ax.text(-1.72, y - 0.14, "$a$", color=F.RED, fontsize=11, va="center")
        ax.text(1.58, y, result, fontsize=11.2, va="center")
    ax.text(0, -0.18, r"$v\cdot a>0$：速率增加　　$v\cdot a<0$：速率減小", ha="center", fontsize=11.3)
    ax.set_xlim(-2.35, 3.25)
    ax.set_ylim(-0.55, 3.85)
    ax.axis("off")

    # 第 4 題：v-t 斜率與面積。
    ax = axes[2]
    _panel(ax, "C｜第 4 題", "$v$–$t$ 斜率給加速度，面積給位移", grid=True)
    t = np.array([0.0, 15.0])
    v = np.array([0.0, 18.0])
    acceleration = (v[1] - v[0]) / (t[1] - t[0])
    displacement = 0.5 * (t[1] - t[0]) * v[1]
    assert np.isclose(acceleration, 1.2)
    assert np.isclose(displacement, 135.0)
    ax.plot(t, v, color=F.BLUE, lw=2.8)
    ax.fill_between(t, 0, v, color=F.BLUE, alpha=0.16)
    ax.scatter(t, v, s=55, color=F.BLUE, edgecolors="white", zorder=5)
    ax.plot([15, 15], [0, 18], color="#94a3b8", lw=1.1, ls="--")
    ax.text(7.7, 6.0, r"面積 $=\frac{1}{2}(15)(18)=135\ \mathrm{m}$", fontsize=11.2, ha="center")
    ax.text(5.5, 14.2, r"斜率 $=1.2\ \mathrm{m/s^2}$", fontsize=11.2, color=F.BLUE, rotation=24)
    ax.set_xlim(0, 16.2)
    ax.set_ylim(0, 20.2)
    ax.set_xticks([0, 5, 10, 15])
    ax.set_yticks([0, 6, 12, 18])
    ax.set_xlabel("時間 $t$ (s)")
    ax.set_ylabel("速度 $v$ (m/s)")
    _save(fig, OUTPUT_NAMES[0])


def fig_05_08():
    """第 5、6、8 題：停車兩階段、落體正方向與追車分段。"""
    fig, axes = _sheet("章末解析圖 9｜先分出反應、落下與追近的時間狀態")

    # 第 5 題：反應期矩形 + 煞車期三角形。
    ax = axes[0]
    _panel(ax, "A｜第 5 題", "停止距離是兩塊 $v$–$t$ 面積", grid=True)
    reaction_time = 0.80
    initial_speed = 27.0
    deceleration = -6.0
    brake_time = -initial_speed / deceleration
    stop_time = reaction_time + brake_time
    reaction_distance = initial_speed * reaction_time
    brake_distance = 0.5 * initial_speed * brake_time
    assert np.isclose(brake_time, 4.5)
    assert np.isclose(stop_time, 5.3)
    assert np.isclose(reaction_distance, 21.6)
    assert np.isclose(brake_distance, 60.75)
    ax.plot([0, reaction_time, stop_time], [initial_speed, initial_speed, 0], color=F.INK, lw=2.7)
    ax.fill_between([0, reaction_time], 0, initial_speed, color=F.GREEN, alpha=0.22)
    ax.fill_between([reaction_time, stop_time], [0, 0], [initial_speed, 0], color=F.BLUE, alpha=0.18)
    ax.axvline(reaction_time, color="#64748b", lw=1.1, ls="--")
    ax.text(0.40, 13.5, "$21.6$ m", ha="center", fontsize=11, color=F.GREEN)
    ax.text(2.95, 10.0, "$60.75$ m", ha="center", fontsize=11, color=F.BLUE)
    ax.text(reaction_time, 29.1, "$0.80$ s", ha="center", fontsize=10.8)
    ax.text(stop_time, 1.0, "$5.30$ s", ha="center", fontsize=10.8)
    ax.set_xlim(0, 5.75)
    ax.set_ylim(0, 31.0)
    ax.set_xticks([0, 0.8, 3, 5.3])
    ax.set_yticks([0, 9, 18, 27])
    ax.set_xlabel("時間 $t$ (s)")
    ax.set_ylabel("速度 $v$ (m/s)")

    # 第 6 題：向下正方向。
    ax = axes[1]
    _panel(ax, "B｜第 6 題", "向下為正，位移、速度、加速度同號")
    t_fall, g = 2.0, 9.8
    height = 0.5 * g * t_fall**2
    final_speed = g * t_fall
    assert np.isclose(height, 19.6)
    assert np.isclose(final_speed, 19.6)
    x = 0.0
    ax.plot([x, x], [0.5, 3.65], color="#94a3b8", lw=1.5, ls="--")
    ax.scatter([x, x], [3.55, 0.58], s=[62, 62], color=[F.BLUE, F.RED], zorder=5)
    _axis_arrow(ax, (-1.55, 3.45), (-1.55, 0.65), color=F.INK, lw=1.8)
    ax.text(-1.78, 2.05, "$+y$", fontsize=12, rotation=90, va="center")
    _axis_arrow(ax, (0.35, 2.72), (0.35, 1.70), color=F.RED, lw=2.4)
    ax.text(0.53, 2.25, r"$a=+9.8\ \mathrm{m/s^2}$", color=F.RED, fontsize=11, va="center")
    ax.annotate("", xy=(1.75, 0.58), xytext=(1.75, 3.55), arrowprops=dict(arrowstyle="<->", color=F.PURPLE, lw=1.8))
    ax.text(1.95, 2.06, r"$h=19.6\ \mathrm{m}$", color=F.PURPLE, fontsize=11.2, rotation=90, va="center")
    ax.text(-0.25, 3.82, r"$t=0, v_0=0$", ha="center", fontsize=11.2)
    ax.text(-0.20, 0.18, r"$t=2.0\ \mathrm{s}, v=+19.6\ \mathrm{m/s}$", ha="center", fontsize=11.2)
    ax.set_xlim(-2.15, 2.75)
    ax.set_ylim(0, 4.20)
    ax.axis("off")

    # 第 8 題：相對間距 d(t)。
    ax = axes[2]
    _panel(ax, "C｜第 8 題", "相對速度先決定間距斜率", grid=True)
    initial_gap = 72.0
    relative_speed = 24.0 - 16.0
    catch_time = initial_gap / relative_speed
    switch_time = 3.0
    remaining_gap = initial_gap - relative_speed * switch_time
    assert np.isclose(relative_speed, 8.0)
    assert np.isclose(catch_time, 9.0)
    assert np.isclose(remaining_gap, 48.0)
    ax.plot([0, switch_time], [initial_gap, remaining_gap], color=F.BLUE, lw=3.0)
    ax.plot([switch_time, catch_time], [remaining_gap, 0], color="#94a3b8", lw=2.0, ls="--")
    ax.scatter([0, switch_time, catch_time], [initial_gap, remaining_gap, 0], s=50, color=[F.BLUE, F.RED, "#94a3b8"], zorder=5)
    ax.axvline(switch_time, color=F.RED, lw=1.1, ls=":")
    ax.text(1.3, 64, r"斜率 $=-8\ \mathrm{m/s}$", fontsize=11, color=F.BLUE, rotation=-18)
    ax.text(switch_time + 0.18, remaining_gap + 5, "$d=48$ m", fontsize=10.8, color=F.RED)
    ax.text(6.25, 33, "等速假設的外推", fontsize=10.8, color="#64748b", rotation=-26)
    ax.text(5.85, 70, "$t>3$ s：用新的 $v(t)$\n重建間距函數", fontsize=11.1, ha="center")
    ax.set_xlim(0, 9.7)
    ax.set_ylim(0, 80)
    ax.set_xticks([0, 3, 6, 9])
    ax.set_yticks([0, 24, 48, 72])
    ax.set_xlabel("時間 $t$ (s)")
    ax.set_ylabel("兩車間距 $d$ (m)")
    _save(fig, OUTPUT_NAMES[1])


def fig_09_11():
    """第 9、10、11 題：時刻差、位置函數與分段速度圖。"""
    fig, axes = _sheet("章末解析圖 10｜時間軸、切線與帶號面積對應三種資料")

    # 第 9 題：兩個時刻與列車尺寸。
    ax = axes[0]
    _panel(ax, "A｜第 9 題", "兩時刻相減得到通過時間")
    t_a, t_b, distance = 1.20, 4.70, 105.0
    interval = t_b - t_a
    average_speed = distance / interval
    assert np.isclose(interval, 3.50)
    assert np.isclose(average_speed, 30.0)
    ax.plot([-2.0, 2.0], [0.6, 0.6], color=F.INK, lw=1.5)
    for x, name, time in ((-1.55, "A", t_a), (1.55, "B", t_b)):
        ax.plot([x, x], [0.42, 0.80], color=F.INK, lw=1.5)
        ax.text(x, 0.28, name, ha="center", fontsize=12, weight="bold")
        ax.text(x, 0.03, rf"$t={time:.2f}\ \mathrm{{s}}$", ha="center", fontsize=11)
    _axis_arrow(ax, (-1.55, 1.05), (1.55, 1.05), color=F.BLUE, lw=2.4)
    ax.text(0, 1.25, r"$105\ \mathrm{m}$", ha="center", color=F.BLUE, fontsize=11.5)
    ax.text(0, -0.45, r"$\Delta t=4.70-1.20=3.50\ \mathrm{s}$", ha="center", fontsize=11.7)
    ax.text(0, -0.80, r"$\bar v=105/3.50=30.0\ \mathrm{m/s}$", ha="center", fontsize=11.7, weight="bold")
    ax.add_patch(Rectangle((0.05, 1.62), 1.65, 0.48, facecolor="#dbeafe", edgecolor=F.BLUE, lw=1.3))
    ax.scatter([1.70], [1.86], s=35, color=F.RED, zorder=5)
    ax.text(0.88, 1.86, "列車長度", ha="center", va="center", fontsize=10.7)
    ax.text(1.77, 1.86, "車頭", ha="left", va="center", fontsize=10.5, color=F.RED)
    ax.text(0, 2.32, "整列車通過月臺時需同時追蹤車頭與車尾", ha="center", fontsize=10.8)
    ax.set_xlim(-2.35, 2.55)
    ax.set_ylim(-1.08, 2.58)
    ax.axis("off")

    # 第 10 題：位置函數及兩條切線。
    ax = axes[1]
    _panel(ax, "B｜第 10 題", "$x(t)$ 的切線斜率就是瞬時速度", grid=True)
    t = np.linspace(0, 5, 401)
    x = 4 - 6 * t + t**2
    points_t = np.array([1.0, 3.0, 4.0])
    points_x = 4 - 6 * points_t + points_t**2
    points_v = -6 + 2 * points_t
    assert np.allclose(points_x, [-1.0, -5.0, -4.0])
    assert np.allclose(points_v, [-4.0, 0.0, 2.0])
    ax.plot(t, x, color=F.BLUE, lw=2.7)
    ax.scatter(points_t, points_x, s=56, color=[F.RED, F.PURPLE, F.GREEN], edgecolors="white", zorder=5)
    for t0, x0, slope, color in ((1.0, -1.0, -4.0, F.RED), (4.0, -4.0, 2.0, F.GREEN)):
        tt = np.linspace(t0 - 0.55, t0 + 0.55, 30)
        ax.plot(tt, x0 + slope * (tt - t0), color=color, lw=1.8, ls="--")
    ax.text(0.22, -0.6, "$v(1)=-4$", color=F.RED, fontsize=10.8)
    ax.text(3.13, -6.0, "$t=3$：$v=0$", color=F.PURPLE, fontsize=10.8)
    ax.text(3.65, -2.15, "$v(4)=+2$", color=F.GREEN, fontsize=10.8)
    ax.set_xlim(0, 5)
    ax.set_ylim(-6.5, 5.2)
    ax.set_xticks([0, 1, 2, 3, 4, 5])
    ax.set_yticks([-5, -1, 0, 4])
    ax.set_xlabel("時間 $t$ (s)")
    ax.set_ylabel("位置 $x$ (m)")

    # 第 11 題：分段速度的帶號面積。
    ax = axes[2]
    _panel(ax, "C｜第 11 題", "分段面積分別累加位移與路徑長", grid=True)
    t_nodes = np.array([0.0, 3.0, 5.0, 7.0])
    v_nodes = np.array([4.0, 4.0, -4.0, -4.0])
    acceleration_mid = (-4.0 - 4.0) / (5.0 - 3.0)
    displacement_parts = np.array([4 * 3, 0, -4 * 2], dtype=float)
    distance_parts = np.array([12, 4, 8], dtype=float)
    assert np.isclose(acceleration_mid, -4.0)
    assert np.isclose(displacement_parts.sum(), 4.0)
    assert np.isclose(distance_parts.sum(), 24.0)
    ax.plot(t_nodes, v_nodes, color=F.INK, lw=2.7)
    ax.axhline(0, color=F.INK, lw=1.2)
    ax.fill_between([0, 3], 0, 4, color=F.BLUE, alpha=0.18)
    t_mid = np.linspace(3, 5, 101)
    v_mid = 16 - 4 * t_mid
    ax.fill_between(t_mid, 0, v_mid, where=v_mid >= 0, color=F.GREEN, alpha=0.22)
    ax.fill_between(t_mid, 0, v_mid, where=v_mid <= 0, color=F.RED, alpha=0.20)
    ax.fill_between([5, 7], 0, -4, color=F.RED, alpha=0.20)
    ax.axvline(4, color="#64748b", lw=1.0, ls="--")
    ax.text(1.5, 1.5, "$+12$ m", ha="center", fontsize=10.8, color=F.BLUE)
    ax.text(4.0, 4.65, "$a=-4$", ha="center", fontsize=10.6)
    ax.text(6.0, -2.3, "$-8$ m", ha="center", fontsize=10.8, color=F.RED)
    ax.text(3.98, -5.75, "中段淨面積 0，\n路徑長 4 m", ha="center", fontsize=10.5)
    ax.set_xlim(0, 7.3)
    ax.set_ylim(-6.4, 6.0)
    ax.set_xticks([0, 3, 4, 5, 7])
    ax.set_yticks([-4, 0, 4])
    ax.set_xlabel("時間 $t$ (s)")
    ax.set_ylabel("速度 $v$ (m/s)")
    _save(fig, OUTPUT_NAMES[2])


def fig_12_14():
    """第 12、13、14 題：反求初速、聲音回傳與移動介質速度相加。"""
    fig, axes = _sheet("章末解析圖 11｜同一坐標系中保留斜率、方向與傳播階段")

    # 第 12 題：梯形面積反求初速。
    ax = axes[0]
    _panel(ax, "A｜第 12 題", "位移固定了 $v$–$t$ 梯形的面積", grid=True)
    acceleration, duration, displacement = 1.5, 8.0, 112.0
    v0 = displacement / duration - 0.5 * acceleration * duration
    vf = v0 + acceleration * duration
    area = 0.5 * (v0 + vf) * duration
    assert np.isclose(v0, 8.0)
    assert np.isclose(vf, 20.0)
    assert np.isclose(area, displacement)
    ax.plot([0, duration], [v0, vf], color=F.BLUE, lw=2.8)
    ax.fill_between([0, duration], 0, [v0, vf], color=F.BLUE, alpha=0.17)
    ax.scatter([0, duration], [v0, vf], s=55, color=[F.RED, F.GREEN], zorder=5)
    ax.text(0.25, v0 + 1.2, "$v_0=8.0$", color=F.RED, fontsize=11)
    ax.text(5.95, vf - 2.8, "$v=20.0$", color=F.GREEN, fontsize=11)
    ax.text(4.0, 7.2, r"梯形面積 $=112\ \mathrm{m}$", ha="center", fontsize=11.3)
    ax.text(4.0, 13.3, r"斜率 $a=1.5\ \mathrm{m/s^2}$", ha="center", fontsize=11.1, color=F.BLUE, rotation=22)
    ax.set_xlim(0, 8.6)
    ax.set_ylim(0, 22.5)
    ax.set_xticks([0, 4, 8])
    ax.set_yticks([0, 8, 14, 20])
    ax.set_xlabel("時間 $t$ (s)")
    ax.set_ylabel("速度 $v$ (m/s)")

    # 第 13 題：落體與聲音是先後兩段。
    ax = axes[1]
    _panel(ax, "B｜第 13 題", "先落下，再由撞擊點傳回聲音")
    fall_time, g = 2.5, 9.8
    height = 0.5 * g * fall_time**2
    impact_speed = g * fall_time
    assert np.isclose(height, 30.625)
    assert np.isclose(impact_speed, 24.5)
    top_y, ground_y = 3.55, 0.45
    ax.plot([-1.8, 1.8], [ground_y, ground_y], color=F.INK, lw=2.1)
    ax.scatter([0], [top_y], s=65, color=F.BLUE, zorder=5)
    _axis_arrow(ax, (-0.28, top_y - 0.15), (-0.28, ground_y + 0.18), color=F.RED, lw=2.5)
    ax.text(-0.50, 2.0, r"落體 $t_f=2.5\ \mathrm{s}$", color=F.RED, fontsize=11.2, rotation=90, va="center")
    _axis_arrow(ax, (0.38, ground_y + 0.12), (0.38, top_y - 0.20), color=F.GREEN, lw=2.5)
    ax.text(0.60, 2.0, r"聲音 $t_s=h/c_s$", color=F.GREEN, fontsize=11.2, rotation=90, va="center")
    ax.annotate("", xy=(1.55, ground_y), xytext=(1.55, top_y), arrowprops=dict(arrowstyle="<->", color=F.PURPLE, lw=1.7))
    ax.text(1.75, 2.0, r"$h=30.6\ \mathrm{m}$", color=F.PURPLE, fontsize=11.2, rotation=90, va="center")
    ax.text(0, 3.90, "釋放點／聽者", ha="center", fontsize=11.3)
    ax.text(0, 0.03, r"撞擊：$v=24.5\ \mathrm{m/s}$ 向下", ha="center", fontsize=11.2)
    ax.text(0, -0.52, r"總時間 $t=t_f+t_s$", ha="center", fontsize=12.2, weight="bold")
    ax.set_xlim(-2.20, 2.25)
    ax.set_ylim(-0.78, 4.20)
    ax.axis("off")

    # 第 14 題：對地速度等於相對扶梯速度加扶梯速度。
    ax = axes[2]
    _panel(ax, "C｜第 14 題", "同一向東正方向相加兩個速度")
    belt_speed = 1.0
    a_relative = 1.5
    b_relative = -0.8
    a_ground = belt_speed + a_relative
    b_ground = belt_speed + b_relative
    assert np.isclose(a_ground, 2.5)
    assert np.isclose(b_ground, 0.2)
    ax.plot([-1.8, 1.95], [0, 0], color=F.INK, lw=2.0)
    _axis_arrow(ax, (-1.8, -0.55), (1.70, -0.55), color=F.INK, lw=1.6)
    ax.text(1.78, -0.55, "東（正）", fontsize=10.8, va="center")
    rows = ((2.70, "甲", a_relative, a_ground), (1.30, "乙", b_relative, b_ground))
    for y, name, relative, ground in rows:
        ax.text(-1.98, y, name, fontsize=12.3, weight="bold", va="center")
        _axis_arrow(ax, (-1.25, y + 0.23), (0.35, y + 0.23), color=F.BLUE, lw=2.4)
        ax.text(-0.43, y + 0.43, r"扶梯 $+1.0$", color=F.BLUE, fontsize=10.7, ha="center")
        rel_end = -1.25 + relative / 1.5 * 1.6
        _axis_arrow(ax, (-1.25, y - 0.16), (rel_end, y - 0.16), color=F.RED, lw=2.4)
        ax.text(-0.43, y - 0.42, rf"相對扶梯 ${relative:+.1f}$", color=F.RED, fontsize=10.7, ha="center")
        ground_length = ground / 2.5 * 2.10
        _axis_arrow(ax, (0.55, y), (0.55 + ground_length, y), color=F.GREEN, lw=2.8)
        ax.text(1.62, y + 0.28, rf"對地 ${ground:+.1f}$", color=F.GREEN, fontsize=10.9, ha="center")
    ax.text(0, 3.62, r"人 P、地 G、扶梯 E：$v_{P/G}=v_{P/E}+v_{E/G}$", ha="center", fontsize=12.2, weight="bold")
    ax.text(0, -0.98, "兩個對地結果皆向東，因此都能到達東端", ha="center", fontsize=11.0)
    ax.set_xlim(-2.25, 2.60)
    ax.set_ylim(-1.25, 3.98)
    ax.axis("off")
    _save(fig, OUTPUT_NAMES[3])


def fig_15_18():
    """第 15、16、18 題：速度資料、雙光電閘與變加速度判讀。"""
    fig, axes = _sheet("章末解析圖 12｜資料位置與模型假設都直接標在圖上")

    # 第 15 題：區間平均速度與中央差分速度落在同一直線。
    ax = axes[0]
    _panel(ax, "A｜第 15 題", "兩種速度配置都給出相同斜率", grid=True)
    sample_t = np.array([0.0, 0.2, 0.4, 0.6, 0.8])
    sample_x = np.array([0.000, 0.012, 0.048, 0.108, 0.192])
    interval_dx = np.diff(sample_x)
    interval_v = interval_dx / 0.20
    midpoint_t = (sample_t[:-1] + sample_t[1:]) / 2
    central_t = sample_t[1:-1]
    central_v = (sample_x[2:] - sample_x[:-2]) / 0.40
    expected_dx = np.array([0.012, 0.036, 0.060, 0.084])
    assert np.allclose(interval_dx, expected_dx)
    assert np.allclose(interval_v, [0.06, 0.18, 0.30, 0.42])
    assert np.allclose(central_v, [0.12, 0.24, 0.36])
    assert np.allclose(np.diff(interval_v) / np.diff(midpoint_t), 0.60)
    line_t = np.linspace(0, 0.8, 100)
    ax.plot(line_t, 0.60 * line_t, color=F.INK, lw=1.7, ls="--")
    ax.scatter(midpoint_t, interval_v, s=64, color=F.BLUE, label="區間平均速度", zorder=5)
    ax.scatter(central_t, central_v, s=64, marker="s", color=F.RED, label="中央差分", zorder=5)
    ax.text(0.49, 0.335, r"斜率 $0.60\ \mathrm{m/s^2}$", fontsize=10.8, rotation=24)
    ax.text(
        0.43,
        0.034,
        r"$\Delta x=$ 0.012, 0.036, 0.060, 0.084 m",
        ha="center",
        fontsize=10.2,
        bbox=dict(facecolor="white", edgecolor="none", alpha=0.86, pad=1.5),
    )
    ax.legend(loc="upper left", fontsize=9.5, frameon=False)
    ax.set_xlim(0, 0.82)
    ax.set_ylim(0, 0.53)
    ax.set_xticks([0, 0.2, 0.4, 0.6, 0.8])
    ax.set_yticks([0, 0.12, 0.24, 0.36, 0.48])
    ax.set_xlabel("速度配置時刻 $t$ (s)")
    ax.set_ylabel("速度 $v$ (m/s)")

    # 第 16 題：固定第一閘共用 v0，並把相容範圍畫成線段。
    ax = axes[1]
    _panel(ax, "B｜第 16 題", "共同起點速度與不確定度區間")
    s1, t1, s2, t2 = 0.400, 0.200, 1.200, 0.400
    g = 2 * (s2 * t1 - s1 * t2) / (t1 * t2 * (t2 - t1))
    v0 = (s1 - 0.5 * g * t1**2) / t1
    lower, measured, reference, upper = 9.56, 9.72, 9.81, 9.88
    assert np.isclose(g, 10.0)
    assert np.isclose(v0, 1.0)
    assert lower <= reference <= upper
    track_x = -1.28
    gate_y = np.array([3.38, 2.36, 0.62])
    ax.plot([track_x, track_x], [0.35, 3.72], color="#94a3b8", lw=1.6)
    for y in gate_y:
        ax.plot([track_x - 0.38, track_x + 0.38], [y, y], color=F.BLUE, lw=4.2, solid_capstyle="round")
    ax.text(track_x + 0.52, gate_y[0], r"第一閘：共同 $v_0$", va="center", fontsize=10.6)
    ax.text(track_x + 0.52, gate_y[1], r"$S_1=0.400$ m，$t_1=0.200$ s", va="center", fontsize=10.4)
    ax.text(track_x + 0.52, gate_y[2], r"$S_2=1.200$ m，$t_2=0.400$ s", va="center", fontsize=10.4)
    _axis_arrow(ax, (track_x - 0.56, 3.25), (track_x - 0.56, 0.78), color=F.RED, lw=2.2)
    ax.text(track_x - 0.80, 2.02, r"$+y$", color=F.RED, fontsize=10.8, rotation=90, va="center")
    ax.text(0.08, 3.80, r"計算：$g=10.0\ \mathrm{m/s^2},\ v_0=1.00\ \mathrm{m/s}$", fontsize=10.8, ha="center")
    x0, x1, y_line = -1.70, 1.85, -0.08
    scale = lambda value: x0 + (value - 9.45) / (10.00 - 9.45) * (x1 - x0)
    ax.plot([scale(lower), scale(upper)], [y_line, y_line], color=F.PURPLE, lw=7, solid_capstyle="round", alpha=0.32)
    ax.scatter([scale(measured)], [y_line], s=70, color=F.PURPLE, zorder=5)
    ax.scatter([scale(reference)], [y_line], s=75, marker="D", color=F.GREEN, zorder=5)
    ax.text(scale(lower), y_line - 0.28, "$9.56$", ha="center", fontsize=9.8)
    ax.text(scale(upper), y_line - 0.28, "$9.88$", ha="center", fontsize=9.8)
    ax.text(scale(measured), y_line + 0.25, "量測 9.72", ha="center", fontsize=9.8, color=F.PURPLE)
    ax.text(scale(reference), y_line - 0.58, "參考 9.81", ha="center", fontsize=9.8, color=F.GREEN)
    ax.text(0.08, -0.88, "參考值落在 $k=2$ 的涵蓋區間內", ha="center", fontsize=10.7, weight="bold")
    ax.set_xlim(-2.18, 2.20)
    ax.set_ylim(-1.14, 4.08)
    ax.axis("off")

    # 第 18 題：前段直線、後段彎曲，並把辨識方案標在圖內。
    ax = axes[2]
    _panel(ax, "C｜第 18 題", "斜率改變表示加速度正在改變", grid=True)
    t_early = np.linspace(0, 4, 9)
    v_early = 1.5 + 1.2 * t_early
    t_late = np.linspace(4.5, 8, 8)
    dt = t_late - 4.0
    v_late = 6.3 + 1.2 * dt - 0.18 * dt**2
    linear_extension = 1.5 + 1.2 * t_late
    late_slopes = np.diff(v_late) / np.diff(t_late)
    assert np.allclose(np.diff(v_early) / np.diff(t_early), 1.2)
    assert np.all(np.diff(late_slopes) < 0)
    assert np.all(v_late < linear_extension)
    ax.scatter(t_early, v_early, s=42, color=F.BLUE, zorder=5)
    ax.plot([0, 4], [1.5, 6.3], color=F.BLUE, lw=2.2)
    ax.fill_between(t_early, 0, v_early, color=F.BLUE, alpha=0.12)
    ax.scatter(t_late, v_late, s=42, color=F.RED, zorder=5)
    ax.plot(t_late, v_late, color=F.RED, lw=2.2)
    ax.plot([4, 8], [6.3, 11.1], color="#94a3b8", lw=1.6, ls="--")
    ax.axvline(4, color=F.PURPLE, lw=1.1, ls=":")
    ax.text(1.55, 3.95, "前 4 s：\n斜率求 $a$\n面積求 $\\Delta x$", ha="center", fontsize=10.6)
    ax.text(6.10, 9.55, "直線外推", color="#64748b", fontsize=10.4, rotation=25)
    ax.text(6.25, 6.25, "實測斜率逐漸減小", color=F.RED, fontsize=10.5, rotation=5)
    ax.text(4.20, 0.75, "辨識來源：固定角度改變初速；同步量斜面角度與位置", fontsize=10.4, ha="center")
    ax.set_xlim(0, 8.2)
    ax.set_ylim(0, 11.8)
    ax.set_xticks([0, 2, 4, 6, 8])
    ax.set_yticks([0, 3, 6, 9, 12])
    ax.set_xlabel("時間 $t$ (s)")
    ax.set_ylabel("速度 $v$ (m/s)")
    _save(fig, OUTPUT_NAMES[4])


def main():
    fig_01_04()
    fig_05_08()
    fig_09_11()
    fig_12_14()
    fig_15_18()
    assets = os.path.join(CH, "assets")
    for name in OUTPUT_NAMES:
        svg_path = os.path.join(assets, name + ".svg")
        pdf_path = os.path.join(assets, name + ".pdf")
        assert os.path.isfile(svg_path), svg_path
        assert not os.path.exists(pdf_path), pdf_path


if __name__ == "__main__":
    main()
