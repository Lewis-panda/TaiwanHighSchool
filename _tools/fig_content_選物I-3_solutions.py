# -*- coding: utf-8 -*-
"""產生選物 I-3 章末題解 SVG。

重繪：.venv/bin/python _tools/fig_content_選物I-3_solutions.py

輸出固定寫入 ``content/選修物理I/選物I-3/assets``，只產生 SVG。
"""

import os
import sys
import tempfile

os.environ.setdefault(
    "MPLCONFIGDIR",
    os.path.join(tempfile.gettempdir(), "highschool-fig-cache"),
)

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import matplotlib.pyplot as plt
import numpy as np

import figlib as F


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CH = os.path.join(ROOT, "content", "選修物理I", "選物I-3")


def _save(fig, name):
    return F.save_to(
        fig,
        CH,
        name,
        output_subdir="assets",
        write_pdf=False,
    )


def _origin_axes(ax, xlim, ylim, *, xlabel="+x", ylabel="+y"):
    """畫出通過原點的局部座標軸。"""
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_aspect("equal", adjustable="box")
    ax.axis("off")
    F.arrow(ax, (xlim[0], 0), (xlim[1] - 0.12, 0), color="#64748b", lw=1.25, mutation=11, z=1)
    F.arrow(ax, (0, ylim[0]), (0, ylim[1] - 0.12), color="#64748b", lw=1.25, mutation=11, z=1)
    ax.text(xlim[1] - 0.16, -0.38, xlabel, color="#64748b", fontsize=9.5, ha="right")
    ax.text(-0.25, ylim[1] - 0.12, ylabel, color="#64748b", fontsize=9.5, ha="right", va="top")


def _vector(ax, start, delta, *, color, label, label_offset=(0.0, 0.0), lw=2.5):
    """由 start 畫出 delta，並在中點標示。"""
    start = np.asarray(start, dtype=float)
    delta = np.asarray(delta, dtype=float)
    end = start + delta
    F.arrow(ax, start, end, color=color, lw=lw, mutation=15)
    midpoint = start + 0.52 * delta + np.asarray(label_offset, dtype=float)
    ax.text(*midpoint, label, color=color, fontsize=10.2, ha="center", va="center")
    return end


def fig_solutions_1_3():
    """第 1–3 題：分量、向量合成與平面定加速。"""
    # 第 1 題。
    magnitude = 20.0
    theta = np.deg2rad(30.0)
    components = magnitude * np.array([np.cos(theta), np.sin(theta)])
    assert np.allclose(components, [10 * np.sqrt(3), 10])

    # 第 2 題。
    vector_a = np.array([6.0, 2.0])
    vector_b = np.array([-3.0, 4.0])
    vector_c = vector_a + vector_b
    assert np.allclose(vector_c, [3.0, 6.0])
    assert np.isclose(np.linalg.norm(vector_c), 3 * np.sqrt(5))
    assert np.isclose(np.degrees(np.arctan2(vector_c[1], vector_c[0])), 63.4349488)

    # 第 3 題。
    v0 = np.array([2.0, 5.0])
    acceleration = np.array([3.0, -2.0])
    duration = 2.0
    delta_v = acceleration * duration
    final_v = v0 + delta_v
    displacement_uniform = v0 * duration
    displacement_accel = 0.5 * acceleration * duration**2
    displacement = displacement_uniform + displacement_accel
    assert np.allclose(delta_v, [6.0, -4.0])
    assert np.allclose(final_v, [8.0, 1.0])
    assert np.allclose(displacement_uniform, [4.0, 10.0])
    assert np.allclose(displacement_accel, [6.0, -4.0])
    assert np.allclose(displacement, [10.0, 6.0])

    fig, axes = plt.subplots(1, 3, figsize=(12.2, 4.7))

    ax = axes[0]
    _origin_axes(ax, (-2, 21), (-2, 14))
    endpoint = components
    _vector(ax, (0, 0), endpoint, color=F.PURPLE, label=r"$|\vec A|=20$", label_offset=(-0.2, 1.2))
    ax.plot([endpoint[0], endpoint[0]], [0, endpoint[1]], color=F.BLUE, lw=1.5, ls="--")
    ax.plot([0, endpoint[0]], [endpoint[1], endpoint[1]], color=F.RED, lw=1.5, ls="--")
    F.angle_arc(ax, (0, 0), 3.8, 0, 30, color=F.GREEN, text=r"$30^\circ$")
    ax.text(endpoint[0] / 2, -1.15, r"$A_x=20\cos30^\circ=10\sqrt{3}$", color=F.BLUE, fontsize=9.8, ha="center")
    ax.text(endpoint[0] + 0.55, endpoint[1] / 2, r"$A_y=20\sin30^\circ=10$", color=F.RED, fontsize=9.8, rotation=90, va="center")
    ax.set_title("第 1 題｜東、北分量", fontsize=12.8)

    ax = axes[1]
    _origin_axes(ax, (-4.5, 7.5), (-1.5, 7.5))
    end_a = _vector(ax, (0, 0), vector_a, color=F.BLUE, label=r"$\vec A=(6,2)$", label_offset=(0.2, -0.55))
    end_c = _vector(ax, end_a, vector_b, color=F.RED, label=r"$\vec B=(-3,4)$", label_offset=(0.65, 0.25))
    _vector(ax, (0, 0), vector_c, color=F.PURPLE, label=r"$\vec C=(3,6)$", label_offset=(-0.7, 0.15), lw=2.8)
    assert np.allclose(end_c, vector_c)
    ax.plot([vector_c[0], vector_c[0]], [0, vector_c[1]], color="#94a3b8", lw=1.0, ls="--")
    ax.plot([0, vector_c[0]], [vector_c[1], vector_c[1]], color="#94a3b8", lw=1.0, ls="--")
    ax.text(3.0, -1.05, r"$\theta=\tan^{-1}(6/3)=63.4^\circ$", fontsize=9.8, ha="center")
    ax.set_title("第 2 題｜首尾相接得合向量", fontsize=12.8)

    ax = axes[2]
    _origin_axes(ax, (-1.5, 11.5), (-5.5, 11.5), xlabel=r"$x$ 分量", ylabel=r"$y$ 分量")
    velocity_scale = 0.78
    end_v0 = _vector(ax, (0, 0), velocity_scale * v0, color=F.BLUE, label=r"$\vec v_0=(2,5)$", label_offset=(-0.75, 0.0))
    end_v = _vector(ax, end_v0, velocity_scale * delta_v, color=F.RED, label=r"$\Delta\vec v=(6,-4)$", label_offset=(0.35, -0.45))
    _vector(ax, (0, 0), velocity_scale * final_v, color=F.PURPLE, label=r"$\vec v=(8,1)$", label_offset=(0.0, 0.65), lw=2.8)
    assert np.allclose(end_v, velocity_scale * final_v)
    ax.text(5.0, -2.85, r"$\Delta\vec r=(4,10)+(6,-4)$", fontsize=10.0, ha="center")
    ax.text(5.0, -4.10, r"$=(10,6)\ \mathrm{m}$", color=F.GREEN, fontsize=10.8, ha="center")
    ax.set_title("第 3 題｜同一時間的向量更新", fontsize=12.8)

    fig.suptitle("章末題解：方向、分量與向量等式", fontsize=15.5, y=0.985)
    fig.subplots_adjust(left=0.025, right=0.985, top=0.84, bottom=0.07, wspace=0.23)
    _save(fig, "選物I-3-章末題解1-3")


def fig_solutions_6_8():
    """第 6–8 題：非同高斜拋、45 度條件與等時距資料。"""
    gravity = 10.0

    # 第 6 題。
    launch_height = 15.0
    velocity = np.array([12.0, 10.0])
    roots = np.roots([-0.5 * gravity, velocity[1], launch_height])
    positive_roots = roots[np.isreal(roots) & (roots > 0)].real
    assert len(positive_roots) == 1
    flight_time = positive_roots[0]
    landing_x = velocity[0] * flight_time
    assert np.isclose(flight_time, 3.0)
    assert np.isclose(landing_x, 36.0)

    # 第 7 題。
    angles = np.linspace(0.0, 90.0, 361)
    normalized_range = np.sin(np.deg2rad(2 * angles))
    max_index = int(np.argmax(normalized_range))
    assert np.isclose(angles[max_index], 45.0)
    assert np.isclose(normalized_range[max_index], 1.0)

    # 第 8 題。
    dx = np.full(4, 1.2)
    dy = np.array([0.7, 0.3, -0.1, -0.5])
    x_data = np.concatenate([[0.0], np.cumsum(dx)])
    y_data = np.concatenate([[0.0], np.cumsum(dy)])
    second_difference = np.diff(dy)
    assert np.allclose(np.diff(x_data), 1.2)
    assert np.allclose(second_difference, -0.4)
    assert np.allclose(y_data, [0.0, 0.7, 1.0, 0.9, 0.4])

    fig, axes = plt.subplots(1, 3, figsize=(12.2, 4.7))

    ax = axes[0]
    dense_t = np.linspace(0, flight_time, 240)
    dense_x = velocity[0] * dense_t
    dense_y = launch_height + velocity[1] * dense_t - 0.5 * gravity * dense_t**2
    ax.plot(dense_x, dense_y, color=F.PURPLE, lw=2.7)
    ax.axhline(0, color=F.INK, lw=1.2)
    launch = np.array([0.0, launch_height])
    _vector(ax, launch, 0.42 * np.array([velocity[0], 0]), color=F.BLUE, label=r"$v_{0x}=12$", label_offset=(0.0, -0.8))
    _vector(ax, launch, 0.42 * np.array([0, velocity[1]]), color=F.RED, label=r"$v_{0y}=10$", label_offset=(-1.8, 0.0))
    ax.scatter([0, landing_x], [launch_height, 0], s=58, color=F.PURPLE, edgecolors="white", zorder=5)
    ax.plot([0, 0], [0, launch_height], color="#94a3b8", lw=1.1, ls="--")
    ax.text(1.0, 7.0, r"$y=15+10t-5t^2$", fontsize=10.3)
    ax.text(landing_x, 1.2, r"$t=3.0\ \mathrm{s}$", fontsize=10.0, ha="right")
    ax.text(landing_x / 2, -2.1, r"$x=12t=36\ \mathrm{m}$", color=F.BLUE, fontsize=10.3, ha="center")
    ax.set_xlim(-2, 39)
    ax.set_ylim(-3.2, 23)
    ax.set_aspect("equal", adjustable="box")
    ax.axis("off")
    ax.set_title("第 6 題｜起點高度進入鉛直方程", fontsize=12.6)

    ax = axes[1]
    ax.plot(angles, normalized_range, color=F.BLUE, lw=2.7)
    ax.axvline(45, color=F.RED, lw=1.3, ls="--")
    ax.scatter([45], [1], s=68, color=F.RED, edgecolors="white", zorder=5)
    ax.text(45, 0.87, r"$\sin 2\theta=1$", color=F.RED, fontsize=10.3, ha="center")
    ax.text(45, 0.11, r"$R/(v_0^2/g)=\sin2\theta$", color=F.PURPLE, fontsize=10.4, ha="center")
    ax.text(45, -0.23, "同高、無阻力、$v_0$ 與 $g$ 固定", fontsize=10.0, ha="center")
    ax.set_xlim(0, 90)
    ax.set_ylim(-0.30, 1.10)
    ax.set_xticks([0, 15, 30, 45, 60, 75, 90])
    ax.set_xlabel(r"$\theta$ (度)")
    ax.set_ylabel("正規化射程")
    ax.set_title("第 7 題｜45° 是特定模型的極值", fontsize=12.6)
    F.clean_grid(ax)

    ax = axes[2]
    ax.plot(x_data, y_data, color=F.PURPLE, lw=2.3)
    ax.scatter(x_data, y_data, s=58, color=F.PURPLE, edgecolors="white", zorder=5)
    for index in range(len(dx)):
        midpoint = ((x_data[index] + x_data[index + 1]) / 2, (y_data[index] + y_data[index + 1]) / 2)
        ax.text(midpoint[0], midpoint[1] + 0.18, rf"$\Delta y={dy[index]:+.1f}$", color=F.RED, fontsize=9.2, ha="center")
        ax.text(midpoint[0], -0.18, r"$\Delta x=1.2$", color=F.BLUE, fontsize=8.8, ha="center")
    ax.text(2.4, 1.31, r"$\Delta(\Delta y)=-0.4\ \mathrm{m}$ 每段相同", color=F.GREEN, fontsize=10.3, ha="center")
    ax.text(2.4, -0.55, r"需要 $\Delta t$ 才能求 $a_y=-0.4/(\Delta t)^2$", fontsize=9.8, ha="center")
    ax.set_xlim(-0.25, 5.05)
    ax.set_ylim(-0.72, 1.56)
    ax.set_xlabel("x (m)")
    ax.set_ylabel("y (m)")
    ax.set_aspect(2.2, adjustable="box")
    ax.set_title("第 8 題｜二階差分向下且為定值", fontsize=12.6)
    F.clean_grid(ax)

    fig.suptitle("章末題解：起始條件、模型條件與等時距資料", fontsize=15.5, y=0.985)
    fig.subplots_adjust(left=0.04, right=0.985, top=0.84, bottom=0.12, wspace=0.28)
    _save(fig, "選物I-3-章末題解6-8")


def fig_solutions_9_11():
    """第 9–11 題：向量減法、相對速度與平面定加速。"""
    vector_a = np.array([5.0, 1.0])
    vector_b = np.array([2.0, 5.0])
    minus_b = -vector_b
    difference = vector_a + minus_b
    assert np.allclose(difference, [3.0, -4.0])
    assert np.isclose(np.linalg.norm(difference), 5.0)

    velocity_a = np.array([12.0, 4.0])
    velocity_b = np.array([7.0, -8.0])
    relative = velocity_b - velocity_a
    assert np.allclose(relative, [-5.0, -12.0])
    assert np.isclose(np.linalg.norm(relative), 13.0)

    v0 = np.array([6.0, -2.0])
    acceleration = np.array([-2.0, 4.0])
    final_time = 3.0
    final_position = v0 * final_time + 0.5 * acceleration * final_time**2
    final_velocity = v0 + acceleration * final_time
    assert np.allclose(final_position, [9.0, 12.0])
    assert np.allclose(final_velocity, [0.0, 10.0])

    fig, axes = plt.subplots(1, 3, figsize=(12.2, 4.8))

    ax = axes[0]
    _origin_axes(ax, (-3.5, 6.5), (-5.5, 6.5))
    end_a = _vector(ax, (0, 0), vector_a, color=F.BLUE, label=r"$\vec A=(5,1)$", label_offset=(0.0, -0.55))
    end_d = _vector(ax, end_a, minus_b, color=F.RED, label=r"$-\vec B=(-2,-5)$", label_offset=(0.6, -0.05))
    _vector(ax, (0, 0), difference, color=F.PURPLE, label=r"$\vec A-\vec B=(3,-4)$", label_offset=(-0.75, -0.2), lw=2.8)
    _vector(ax, (0, 0), 0.72 * vector_b, color="#64748b", label=r"$\vec B$", label_offset=(0.35, 0.0), lw=1.5)
    assert np.allclose(end_d, difference)
    ax.text(1.5, -5.0, r"$|\vec A-\vec B|=5$", fontsize=10.2, ha="center")
    ax.set_title("第 9 題｜減法轉成加上反向量", fontsize=12.6)

    ax = axes[1]
    scale = 0.62
    _origin_axes(ax, (-4.5, 9.5), (-8.5, 4.5), xlabel=r"$v_x$", ylabel=r"$v_y$")
    end_a = _vector(ax, (0, 0), scale * velocity_a, color=F.BLUE, label=r"$\vec v_A=(12,4)$", label_offset=(0.0, 0.55))
    end_b = _vector(ax, end_a, scale * relative, color=F.RED, label=r"$\vec v_{B/A}=(-5,-12)$", label_offset=(-0.2, -0.55))
    _vector(ax, (0, 0), scale * velocity_b, color=F.PURPLE, label=r"$\vec v_B=(7,-8)$", label_offset=(0.7, -0.2), lw=2.8)
    assert np.allclose(end_b, scale * velocity_b)
    ax.text(3.3, -7.55, r"$|\vec v_{B/A}|=13\ \mathrm{m/s}$", fontsize=10.2, ha="center")
    ax.set_title(r"第 10 題｜$\vec v_B=\vec v_A+\vec v_{B/A}$", fontsize=12.6)

    ax = axes[2]
    dense_t = np.linspace(0.0, final_time, 260)
    x = v0[0] * dense_t + 0.5 * acceleration[0] * dense_t**2
    y = v0[1] * dense_t + 0.5 * acceleration[1] * dense_t**2
    ax.plot(x, y, color=F.PURPLE, lw=2.7)
    ax.scatter([0, final_position[0]], [0, final_position[1]], s=62, color=F.PURPLE, edgecolors="white", zorder=5)
    _vector(ax, final_position, 0.48 * final_velocity, color=F.GREEN, label=r"$\vec v=(0,10)$", label_offset=(1.25, 0.0))
    ax.plot([final_position[0], final_position[0]], [0, final_position[1]], color="#94a3b8", lw=1.0, ls="--")
    ax.plot([0, final_position[0]], [final_position[1], final_position[1]], color="#94a3b8", lw=1.0, ls="--")
    ax.text(5.0, 2.1, r"$x=6t-t^2$", color=F.BLUE, fontsize=10.1)
    ax.text(5.0, 0.6, r"$y=-2t+2t^2$", color=F.RED, fontsize=10.1)
    ax.text(8.7, 11.1, r"$\vec r(3)=(9,12)\ \mathrm{m}$", fontsize=10.2, ha="right")
    ax.set_xlim(-0.8, 12.8)
    ax.set_ylim(-1.6, 18.0)
    ax.set_aspect("equal", adjustable="box")
    ax.set_xlabel("x (m)")
    ax.set_ylabel("y (m)")
    ax.set_title("第 11 題｜位置與軌跡切向速度", fontsize=12.6)
    F.clean_grid(ax)

    fig.suptitle("章末題解：向量等式決定箭頭如何首尾相接", fontsize=15.5, y=0.985)
    fig.subplots_adjust(left=0.03, right=0.985, top=0.84, bottom=0.08, wspace=0.24)
    _save(fig, "選物I-3-章末題解9-11")


def fig_solutions_12_14():
    """第 12–14 題：平均加速、水平投放與斜拋狀態。"""
    v1 = np.array([8.0, 0.0])
    v2 = np.array([2.0, 6.0])
    dt = 1.5
    delta_v = v2 - v1
    average_a = delta_v / dt
    assert np.allclose(delta_v, [-6.0, 6.0])
    assert np.allclose(average_a, [-4.0, 4.0])
    assert np.isclose(np.linalg.norm(average_a), 4 * np.sqrt(2))

    gravity = 10.0
    drop_height = 125.0
    horizontal_speed = 20.0
    drop_time = np.sqrt(2 * drop_height / gravity)
    drop_range = horizontal_speed * drop_time
    landing_velocity = np.array([horizontal_speed, -gravity * drop_time])
    assert np.isclose(drop_time, 5.0)
    assert np.isclose(drop_range, 100.0)
    assert np.allclose(landing_velocity, [20.0, -50.0])
    assert np.isclose(np.linalg.norm(landing_velocity), 10 * np.sqrt(29))

    launch_velocity = np.array([20.0, 15.0])
    state_time = 1.0
    state_position = np.array([
        launch_velocity[0] * state_time,
        launch_velocity[1] * state_time - 0.5 * gravity * state_time**2,
    ])
    state_velocity = launch_velocity + np.array([0.0, -gravity]) * state_time
    assert np.allclose(state_position, [20.0, 10.0])
    assert np.allclose(state_velocity, [20.0, 5.0])
    assert np.isclose(np.linalg.norm(state_velocity), 5 * np.sqrt(17))

    fig, axes = plt.subplots(1, 3, figsize=(12.2, 4.8))

    ax = axes[0]
    _origin_axes(ax, (-1.5, 9.5), (-1.5, 7.8), xlabel=r"$v_x$", ylabel=r"$v_y$")
    end_v1 = _vector(ax, (0, 0), v1, color=F.BLUE, label=r"$\vec v_1=(8,0)$", label_offset=(0.0, -0.65))
    end_v2 = _vector(ax, end_v1, delta_v, color=F.RED, label=r"$\Delta\vec v=(-6,6)$", label_offset=(-0.3, 0.45))
    _vector(ax, (0, 0), v2, color=F.PURPLE, label=r"$\vec v_2=(2,6)$", label_offset=(-0.55, 0.0), lw=2.8)
    assert np.allclose(end_v2, v2)
    _vector(ax, (5.0, 1.2), (-2.0, 0.0), color=F.AMBER, label=r"$\bar a_\parallel=-4$", label_offset=(0.0, -0.6), lw=1.8)
    _vector(ax, (5.0, 1.2), (0.0, 2.0), color=F.GREEN, label=r"$\bar a_\perp=+4$", label_offset=(1.1, 0.0), lw=1.8)
    ax.text(5.2, 5.4, r"$\bar{\vec a}=\Delta\vec v/1.5=(-4,4)$", fontsize=9.9, ha="center")
    ax.set_title(r"第 12 題｜速度端點的位移是 $\Delta\vec v$", fontsize=12.4)

    ax = axes[1]
    dense_t = np.linspace(0.0, drop_time, 280)
    x = horizontal_speed * dense_t
    y = drop_height - 0.5 * gravity * dense_t**2
    ax.plot(x, y, color=F.PURPLE, lw=2.7)
    ax.axhline(0, color=F.INK, lw=1.2)
    ax.plot([0, 0], [0, drop_height], color="#94a3b8", lw=1.0, ls="--")
    landing = np.array([drop_range, 0.0])
    velocity_scale = 0.62
    _vector(ax, landing, velocity_scale * np.array([landing_velocity[0], 0]), color=F.BLUE, label=r"$v_x=20$", label_offset=(0.0, 3.7))
    _vector(ax, landing, velocity_scale * np.array([0, landing_velocity[1]]), color=F.RED, label=r"$v_y=-50$", label_offset=(-6.8, 0.0))
    _vector(ax, landing, velocity_scale * landing_velocity, color=F.GREEN, label=r"$|\vec v|=10\sqrt{29}$", label_offset=(7.0, -6.0), lw=2.8)
    ax.text(5.0, 63.0, r"$125=\frac{1}{2}gT^2\Rightarrow T=5.0\ \mathrm{s}$", fontsize=9.9)
    ax.text(50.0, -7.0, r"$R=v_xT=100\ \mathrm{m}$", fontsize=10.2, ha="center")
    ax.set_xlim(-5, 123)
    ax.set_ylim(-38, 133)
    ax.set_aspect("equal", adjustable="box")
    ax.axis("off")
    ax.set_title("第 13 題｜落下時間決定釋放距離", fontsize=12.4)

    ax = axes[2]
    full_time = 2 * launch_velocity[1] / gravity
    dense_t = np.linspace(0.0, full_time, 260)
    x = launch_velocity[0] * dense_t
    y = launch_velocity[1] * dense_t - 0.5 * gravity * dense_t**2
    ax.plot(x, y, color=F.PURPLE, lw=2.7)
    ax.axhline(0, color=F.INK, lw=1.2)
    ax.scatter([state_position[0]], [state_position[1]], s=68, color=F.PURPLE, edgecolors="white", zorder=5)
    arrow_scale = 0.65
    _vector(ax, state_position, arrow_scale * np.array([state_velocity[0], 0]), color=F.BLUE, label="")
    _vector(ax, state_position, arrow_scale * np.array([0, state_velocity[1]]), color=F.RED, label="")
    _vector(ax, state_position, arrow_scale * state_velocity, color=F.GREEN, label="", lw=2.6)
    ax.text(26.5, 7.2, r"$v_x=20$", color=F.BLUE, fontsize=9.8, ha="center")
    ax.text(16.0, 13.2, r"$v_y=5$", color=F.RED, fontsize=9.8, ha="center")
    ax.text(32.0, 14.5, r"$\vec v(1)$", color=F.GREEN, fontsize=9.8, ha="center")
    ax.plot([state_position[0], state_position[0]], [0, state_position[1]], color="#94a3b8", lw=1.0, ls="--")
    ax.text(state_position[0], 5.8, r"$\vec r(1)=(20,10)\ \mathrm{m}$", fontsize=9.8, ha="center")
    ax.text(41.0, 2.7, r"$|\vec v(1)|=5\sqrt{17}$", fontsize=10.0, ha="center")
    ax.set_xlim(-2, 63)
    ax.set_ylim(-4, 18)
    ax.set_aspect("equal", adjustable="box")
    ax.set_xlabel("x (m)")
    ax.set_ylabel("y (m)")
    ax.set_title("第 14 題｜同一時刻的位置與速度", fontsize=12.4)
    F.clean_grid(ax)

    fig.suptitle("章末題解：速度變化、共同飛行時間與某時刻狀態", fontsize=15.5, y=0.985)
    fig.subplots_adjust(left=0.03, right=0.985, top=0.84, bottom=0.08, wspace=0.23)
    _save(fig, "選物I-3-章末題解12-14")


def fig_solutions_16_18():
    """第 16–18 題：速度資料、非同高設計與模型偏離。"""
    measured_v = np.array([[2.0, 1.0], [4.0, 0.0], [6.0, -1.0]])
    delta_v = np.diff(measured_v, axis=0)
    predicted_v = measured_v[-1] + delta_v[-1]
    assert np.allclose(delta_v, [[2.0, -1.0], [2.0, -1.0]])
    assert np.allclose(predicted_v, [8.0, -2.0])

    gravity = 10.0
    launch_height = 15.0
    launch_velocity = np.array([16.0, 10.0])
    roots = np.roots([-0.5 * gravity, launch_velocity[1], launch_height])
    flight_time = roots[np.isreal(roots) & (roots > 0)].real.item()
    landing_position = np.array([launch_velocity[0] * flight_time, 0.0])
    landing_velocity = launch_velocity + np.array([0.0, -gravity]) * flight_time
    landing_angle = np.degrees(np.arctan2(abs(landing_velocity[1]), landing_velocity[0]))
    assert np.isclose(flight_time, 3.0)
    assert np.allclose(landing_position, [48.0, 0.0])
    assert np.allclose(landing_velocity, [16.0, -20.0])
    assert np.isclose(landing_angle, 51.3401917)

    # 第 18 題的方向檢核：下降時阻力與速度反向。
    descending_velocity = np.array([4.0, -3.0])
    drag = -descending_velocity / np.linalg.norm(descending_velocity)
    gravity_vector = np.array([0.0, -1.0])
    assert drag[0] < 0 and drag[1] > 0
    assert gravity_vector[1] < 0
    assert 2.5 * drag[1] < abs(2.6 * gravity_vector[1])
    rightward_velocity = np.array([1.0, 0.0])
    leftward_velocity = -rightward_velocity
    drag_rightward = -rightward_velocity
    drag_leftward = -leftward_velocity
    sidewind_acceleration = np.array([1.0, 0.0])
    assert np.allclose(drag_rightward, -drag_leftward)
    assert sidewind_acceleration[0] > 0

    fig, axes = plt.subplots(1, 3, figsize=(12.2, 4.9))

    ax = axes[0]
    all_v = np.vstack([measured_v, predicted_v])
    _origin_axes(ax, (-0.8, 9.3), (-3.0, 2.8), xlabel=r"$v_x$", ylabel=r"$v_y$")
    ax.plot(all_v[:, 0], all_v[:, 1], color=F.PURPLE, lw=2.2, ls="--")
    colors = [F.BLUE, F.BLUE, F.BLUE, F.GREEN]
    for index, (point, color) in enumerate(zip(all_v, colors)):
        ax.scatter([point[0]], [point[1]], s=68, color=color, edgecolors="white", zorder=5)
        ax.text(point[0], point[1] + 0.35, rf"$t={index}$", fontsize=9.8, ha="center")
    for index in range(3):
        _vector(ax, all_v[index], all_v[index + 1] - all_v[index], color=F.RED, label=r"$\Delta\vec v=(2,-1)$", label_offset=(0.0, -0.45), lw=1.9)
    ax.text(4.8, -2.55, r"$\vec a=(2,-1)\ \mathrm{m/s^2}$", fontsize=10.1, ha="center")
    ax.set_title("第 16 題｜速度空間的等步更新", fontsize=12.5)

    ax = axes[1]
    dense_t = np.linspace(0.0, flight_time, 260)
    x = launch_velocity[0] * dense_t
    y = launch_height + launch_velocity[1] * dense_t - 0.5 * gravity * dense_t**2
    ax.plot(x, y, color=F.PURPLE, lw=2.7)
    ax.axhline(0, color=F.INK, lw=1.2)
    ax.plot([0, 0], [0, launch_height], color="#94a3b8", lw=1.0, ls="--")
    landing = landing_position
    velocity_scale = 0.42
    _vector(ax, landing, velocity_scale * np.array([landing_velocity[0], 0]), color=F.BLUE, label="")
    _vector(ax, landing, velocity_scale * np.array([0, landing_velocity[1]]), color=F.RED, label="")
    _vector(ax, landing, velocity_scale * landing_velocity, color=F.GREEN, label="", lw=2.8)
    ax.text(53.0, 3.3, r"$v_x=16$", color=F.BLUE, fontsize=9.8, ha="center")
    ax.text(43.3, -4.8, r"$v_y=-20$", color=F.RED, fontsize=9.8, ha="center")
    ax.text(55.0, -8.6, rf"${landing_angle:.1f}^\circ$", color=F.GREEN, fontsize=9.8, ha="center")
    ax.text(3.0, 7.0, r"$0=15+10t-5t^2$", fontsize=10.0)
    ax.text(45.5, 2.0, r"$t=3.0\ \mathrm{s}$", fontsize=9.8, ha="right")
    ax.text(24.0, -2.2, r"$x=16t=48\ \mathrm{m}$", fontsize=10.0, ha="center")
    ax.set_xlim(-2, 59)
    ax.set_ylim(-11, 23)
    ax.set_aspect("equal", adjustable="box")
    ax.axis("off")
    ax.set_title("第 17 題｜非同高軌跡的落地狀態", fontsize=12.5)

    ax = axes[2]
    ax.set_xlim(-0.5, 10.5)
    ax.set_ylim(-0.5, 9.5)
    ax.set_aspect("equal", adjustable="box")
    ax.axis("off")
    point = np.array([2.2, 7.3])
    _vector(ax, point, 1.05 * descending_velocity, color=F.BLUE, label=r"$\vec v$", label_offset=(0.2, 0.55), lw=2.6)
    _vector(ax, point, 2.5 * drag, color=F.RED, label=r"$\vec a_D$", label_offset=(-0.35, 0.5), lw=2.6)
    _vector(ax, point, 2.6 * gravity_vector, color=F.PURPLE, label=r"$\vec g$", label_offset=(0.55, 0.0), lw=2.6)
    ax.text(4.8, 7.8, r"下降：$a_{Dx}<0, a_{Dy}>0$", fontsize=9.8)
    ax.text(4.8, 6.8, r"因此 $v_x$ 減少、$|a_y|<g$", fontsize=9.8)

    y_rows = [4.15, 1.55]
    for y_row, velocity_direction, label in [
        (y_rows[0], rightward_velocity, r"$v_x>0$"),
        (y_rows[1], leftward_velocity, r"$v_x<0$"),
    ]:
        origin = np.array([2.0, y_row])
        _vector(ax, origin, 1.8 * velocity_direction, color=F.BLUE, label=label, label_offset=(0.0, 0.45), lw=2.1)
        drag_direction = -velocity_direction
        _vector(ax, origin + np.array([3.2, 0]), 1.45 * drag_direction, color=F.RED, label=r"阻力 $a_{Dx}$", label_offset=(0.0, 0.45), lw=2.1)
        _vector(ax, origin + np.array([6.3, 0]), 1.45 * sidewind_acceleration, color=F.GREEN, label=r"側風 $a_w$", label_offset=(0.0, 0.45), lw=2.1)
    ax.text(5.1, 0.15, "改變發射方向：阻力分量反轉，側風方向保持", fontsize=9.4, ha="center")
    ax.set_title("第 18 題｜由加速度方向分辨模型", fontsize=12.5)

    fig.suptitle("章末題解：用速度空間、軌跡與加速度方向檢驗模型", fontsize=15.5, y=0.985)
    fig.subplots_adjust(left=0.025, right=0.985, top=0.84, bottom=0.06, wspace=0.22)
    _save(fig, "選物I-3-章末題解16-18")


if __name__ == "__main__":
    fig_solutions_1_3()
    fig_solutions_6_8()
    fig_solutions_9_11()
    fig_solutions_12_14()
    fig_solutions_16_18()
    print("done.")
