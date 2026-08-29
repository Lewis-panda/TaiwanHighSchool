# -*- coding: utf-8 -*-
"""產生選物 I-4 公開學生講義的概念 SVG。

重繪：.venv/bin/python _tools/fig_content_選物I-4.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Arc, Circle, FancyBboxPatch, Polygon, Rectangle

import figlib as F


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CH = os.path.join(ROOT, "content", "選修物理I", "選物I-4")


def _save(fig, name):
    return F.save_to(fig, CH, name, output_subdir="assets", write_pdf=False)


def fig_hooke_calibration():
    """以力—伸長量直線的斜率呈現彈簧力常數。"""
    spring_constant = 200.0
    extension = np.linspace(0.0, 0.04, 200)
    force = spring_constant * extension
    sample_extension = np.array([0.01, 0.03])
    sample_force = spring_constant * sample_extension

    assert np.allclose(sample_force, [2.0, 6.0])
    assert np.isclose(np.diff(sample_force)[0] / np.diff(sample_extension)[0], spring_constant)
    assert np.allclose(force, spring_constant * extension)

    fig, ax = F.canvas(9.4, 4.9)
    ax.plot(extension, force, color=F.BLUE, lw=2.8)
    ax.scatter(sample_extension, sample_force, s=75, color=F.RED, edgecolors="white", zorder=5)
    for x, y in zip(sample_extension, sample_force):
        ax.plot([x, x], [0, y], color="#94a3b8", lw=1.0, ls="--")
        ax.plot([0, x], [y, y], color="#94a3b8", lw=1.0, ls="--")
        ax.text(x + 0.0012, y - 0.45, rf"$({x:.3f}\ \mathrm{{m}},\ {y:g}\ \mathrm{{N}})$", fontsize=10.8)

    triangle_x = np.array([0.01, 0.03, 0.03])
    triangle_y = np.array([2.0, 2.0, 6.0])
    ax.plot(triangle_x, triangle_y, color=F.GREEN, lw=2.0)
    ax.text(0.020, 1.45, r"$\Delta x=0.020\ \mathrm{m}$", color=F.GREEN, ha="center", fontsize=10.8)
    ax.text(0.0315, 4.0, r"$\Delta F=4.0\ \mathrm{N}$", color=F.GREEN, va="center", fontsize=10.8)
    ax.text(0.021, 7.1, r"斜率 $k=\dfrac{\Delta F}{\Delta x}=200\ \mathrm{N/m}$", color=F.INK, fontsize=12.5)

    ax.set_xlim(0, 0.042)
    ax.set_ylim(0, 8.5)
    ax.set_xlabel("伸長量 x (m)")
    ax.set_ylabel(r"平衡外力 $F$ (N)")
    ax.set_title("比例限度內，力—伸長量圖的斜率就是彈簧力常數", fontsize=15, pad=12)
    F.clean_grid(ax)
    fig.subplots_adjust(left=0.11, right=0.97, top=0.84, bottom=0.16)
    _save(fig, "選物I-4-虎克定律斜率")


def _draw_incline(ax, x_offset, scale=0.82):
    """畫共同使用的斜面、物體與局部座標。"""
    offset = np.array([x_offset, 0.0])

    def point(value):
        return offset + scale * np.asarray(value)

    theta_deg = 32
    theta = np.deg2rad(theta_deg)
    u = np.array([np.cos(theta), np.sin(theta)])
    n = np.array([-np.sin(theta), np.cos(theta)])
    assert np.isclose(np.dot(u, n), 0.0)
    assert np.isclose(np.linalg.norm(u), 1.0)
    assert np.isclose(np.linalg.norm(n), 1.0)
    a = point([-2.35, -1.10])
    b = point([2.35, -1.10])
    c = point([2.35, -1.10 + 4.70 * np.tan(theta)])
    ax.add_patch(
        Polygon(
            [a, b, c],
            closed=True,
            facecolor="#eef3f8",
            edgecolor="#64748b",
            lw=1.5,
            zorder=1,
        )
    )

    center = point(np.array([-0.05, 0.33]) + 0.34 * n)
    half_u, half_n = scale * 0.62, scale * 0.38
    corners = [
        center - half_u * u - half_n * n,
        center + half_u * u - half_n * n,
        center + half_u * u + half_n * n,
        center - half_u * u + half_n * n,
    ]
    ax.add_patch(
        Polygon(
            corners,
            closed=True,
            facecolor="#ffd27a",
            edgecolor="#9a4d00",
            lw=1.7,
            zorder=4,
        )
    )
    ax.add_patch(Circle(center, scale * 0.045, color=F.INK, zorder=7))
    ax.add_patch(Arc(a, scale * 1.25, scale * 1.25, theta1=0, theta2=theta_deg, color=F.INK, lw=1.3))
    ax.text(*(a + scale * np.array([0.82, 0.20])), r"$\theta$", fontsize=12, color=F.INK)

    axis_origin = point([1.18, -0.44])
    F.arrow(ax, axis_origin, axis_origin + scale * 0.72 * u, color="#64748b", lw=1.3, mutation=11)
    F.arrow(ax, axis_origin, axis_origin + scale * 0.72 * n, color="#64748b", lw=1.3, mutation=11)
    ax.text(*(axis_origin + scale * 0.84 * u), "$t$", fontsize=10.5, color="#64748b", ha="center")
    ax.text(*(axis_origin + scale * 0.84 * n), "$n$", fontsize=10.5, color="#64748b", ha="center")
    return center, u, n, theta, scale


def fig_free_body_diagram():
    """由斜面方向計算物塊、局部座標與三支真實力。"""
    fig, ax = F.canvas(10.8, 4.7)
    ax.set_aspect("equal")
    ax.axis("off")
    center, tangent, normal, theta, scale = _draw_incline(ax, 0.0, scale=1.08)
    gravity_direction = np.array([0.0, -1.0])
    gravity_length = scale * 1.48
    normal_force = gravity_length * np.cos(theta) * normal
    applied_force = scale * 1.45 * tangent
    gravity_force = gravity_length * gravity_direction

    assert np.isclose(np.dot(normal_force, tangent), 0.0)
    assert np.isclose(
        np.linalg.norm(normal_force) / np.linalg.norm(gravity_force),
        np.cos(theta),
    )
    assert np.isclose(tangent[0] * applied_force[1] - tangent[1] * applied_force[0], 0.0)
    assert np.allclose(gravity_force / np.linalg.norm(gravity_force), gravity_direction)

    F.arrow(ax, center, center + normal_force, color=F.BLUE, lw=3.0, mutation=19)
    F.arrow(ax, center, center + applied_force, color=F.GREEN, lw=3.0, mutation=19)
    F.arrow(ax, center, center + gravity_force, color=F.RED, lw=3.0, mutation=19)
    ax.text(*(center + 1.10 * normal_force), r"正向力 $N$", color=F.BLUE, fontsize=13, ha="center")
    ax.text(*(center + 1.08 * applied_force + np.array([0.0, 0.10])), r"外力 $F$", color=F.GREEN, fontsize=13)
    ax.text(*(center + 1.08 * gravity_force + np.array([0.12, 0.0])), r"重力 $mg$", color=F.RED, fontsize=13, ha="left")
    ax.text(
        3.18,
        0.20,
        "沿斜面取 $t$ 軸\n垂直斜面取 $n$ 軸\n" + r"$\sum F_t=ma_t$" + "\n" + r"$\sum F_n=ma_n$",
        fontsize=12.5,
        linespacing=1.55,
        va="center",
    )
    ax.text(0, -2.02, "光滑斜面只畫已知的外界作用力；若題目給摩擦，再沿接觸面補畫。", fontsize=11.5, ha="center", color="#64748b")
    ax.set_xlim(-3.45, 5.05)
    ax.set_ylim(-2.35, 2.55)
    ax.set_title("自由體圖先限定受力體，再依接觸與遠距作用畫力", fontsize=15, pad=12)
    _save(fig, "選物I-4-受力圖")


def fig_incline_components():
    """把斜面自由體圖與重力投影分成兩個連續步驟。"""
    fig, ax = F.canvas(11.6, 4.9)
    ax.set_aspect("equal")
    ax.axis("off")

    center, u, n, _, scale = _draw_incline(ax, -2.75)
    F.arrow(ax, center, center + scale * 1.30 * n, color=F.BLUE, lw=2.7)
    ax.text(*(center + scale * 1.48 * n), "$N$", color=F.BLUE, fontsize=13.5, ha="center")
    F.arrow(ax, center, center + scale * 1.38 * u, color=F.GREEN, lw=2.7)
    ax.text(*(center + scale * (1.55 * u + np.array([0.0, 0.10]))), "$F$", color=F.GREEN, fontsize=13.5)
    F.arrow(ax, center, center + scale * np.array([0.0, -1.52]), color=F.RED, lw=2.7)
    ax.text(*(center + scale * np.array([0.18, -1.65])), "$mg$", color=F.RED, fontsize=13.5, ha="left")
    ax.text(-2.75, 2.05, "① 先畫真實力", fontsize=13, ha="center")

    center, u, n, theta, scale = _draw_incline(ax, 2.75)
    gravity = scale * np.array([0.0, -1.70])
    along = -scale * 1.70 * np.sin(theta) * u
    normal = -scale * 1.70 * np.cos(theta) * n
    assert np.allclose(along + normal, gravity)
    assert np.isclose(np.dot(along, n), 0.0)
    assert np.isclose(np.dot(normal, u), 0.0)
    F.arrow(ax, center, center + gravity, color=F.RED, lw=2.8)
    ax.text(*(center + gravity + scale * np.array([0.14, -0.03])), "$mg$", color=F.RED, fontsize=13.5, ha="left")
    F.arrow(ax, center, center + along, color=F.AMBER, lw=2.5)
    ax.text(
        *(center + 0.66 * along + scale * np.array([-0.28, 0.12])),
        r"$mg\sin\theta$",
        color=F.AMBER,
        fontsize=12,
        ha="center",
    )
    F.arrow(ax, center, center + normal, color=F.PURPLE, lw=2.5)
    ax.text(
        *(center + 0.63 * normal + scale * np.array([0.27, -0.04])),
        r"$mg\cos\theta$",
        color=F.PURPLE,
        fontsize=12,
        ha="left",
    )
    ax.plot(
        [center[0] + along[0], center[0] + gravity[0]],
        [center[1] + along[1], center[1] + gravity[1]],
        color="#94a3b8",
        lw=1.2,
        ls="--",
    )
    ax.plot(
        [center[0] + normal[0], center[0] + gravity[0]],
        [center[1] + normal[1], center[1] + gravity[1]],
        color="#94a3b8",
        lw=1.2,
        ls="--",
    )
    ax.text(2.75, 2.05, "② 再把重力投影", fontsize=13, ha="center")

    ax.text(
        0,
        -1.95,
        r"沿斜面：$F-mg\sin\theta=ma_t$　　垂直斜面：$N-mg\cos\theta=0$",
        ha="center",
        fontsize=12.5,
        color=F.INK,
    )
    ax.set_xlim(-5.25, 5.25)
    ax.set_ylim(-2.30, 2.55)
    ax.set_title("斜面題的兩步：先判斷力，再沿斜面與垂直斜面列式", fontsize=15, pad=10)
    _save(fig, "選物I-4-斜面重力分解")


def fig_third_law_pair():
    """以兩個受力體清楚呈現第三定律力對。"""
    fig, ax = F.schematic(10.4, 4.6)

    body_a = FancyBboxPatch(
        (-2.4, -0.55),
        2.4,
        1.7,
        boxstyle="round,pad=0.03,rounding_size=0.14",
        facecolor="#dbeafe",
        edgecolor=F.BLUE,
        lw=1.8,
        zorder=2,
    )
    body_b = FancyBboxPatch(
        (0.0, -0.55),
        2.4,
        1.7,
        boxstyle="round,pad=0.03,rounding_size=0.14",
        facecolor="#fee2e2",
        edgecolor=F.RED,
        lw=1.8,
        zorder=2,
    )
    ax.add_patch(body_a)
    ax.add_patch(body_b)
    ax.plot([0, 0], [-0.45, 1.05], color="#64748b", lw=1.2, ls=":", zorder=4)

    ax.text(-1.2, 0.32, "受力體 A", ha="center", va="center", fontsize=17, weight="bold")
    ax.text(1.2, 0.32, "受力體 B", ha="center", va="center", fontsize=17, weight="bold")

    force_on_a = np.array([-2.42, 0.0])
    force_on_b = np.array([2.42, 0.0])
    assert np.allclose(force_on_a, -force_on_b)
    assert np.isclose(np.linalg.norm(force_on_a), np.linalg.norm(force_on_b))
    F.arrow(ax, (-1.20, -0.03), np.array([-1.20, -0.03]) + force_on_a, color=F.PURPLE, lw=3.0, mutation=20)
    F.arrow(ax, (1.20, -0.03), np.array([1.20, -0.03]) + force_on_b, color=F.PURPLE, lw=3.0, mutation=20)
    ax.text(-2.50, -0.55, r"$\vec F_{B\to A}$", color=F.PURPLE, fontsize=15, ha="center")
    ax.text(2.50, -0.55, r"$\vec F_{A\to B}$", color=F.PURPLE, fontsize=15, ha="center")

    ax.text(-1.2, -1.14, r"放進 $\sum\vec F_A$", color=F.BLUE, fontsize=12.5, ha="center")
    ax.text(1.2, -1.14, r"放進 $\sum\vec F_B$", color=F.RED, fontsize=12.5, ha="center")
    ax.text(
        0,
        -1.78,
        r"$\vec F_{A\to B}=-\vec F_{B\to A}$　：交換施力者與受力者，兩力分屬兩張自由體圖",
        ha="center",
        fontsize=13,
        color=F.INK,
        bbox=dict(boxstyle="round,pad=0.35", fc="white", ec="#cbd5e1", lw=1.2),
    )
    ax.set_title("牛頓第三定律：同一交互作用的兩端", fontsize=15, pad=14)
    ax.set_xlim(-4.45, 4.45)
    ax.set_ylim(-2.25, 1.65)
    _save(fig, "選物I-4-第三定律力對")


def fig_circular_projection():
    """區分向心加速度向量與簡諧方向上的 x 分量。"""
    fig, ax = F.canvas(11.2, 5.0)
    ax.set_aspect("equal")
    ax.axis("off")

    center = np.array([-3.25, 0.25])
    radius = 1.55
    phase = np.deg2rad(50)
    radial = np.array([np.cos(phase), np.sin(phase)])
    tangent = np.array([-np.sin(phase), np.cos(phase)])
    point = center + radius * radial
    projection = np.array([point[0], center[1]])
    assert np.isclose(np.dot(radial, tangent), 0.0)
    assert np.isclose(np.linalg.norm(point - center), radius)

    angle = np.linspace(0, 2 * np.pi, 500)
    ax.plot(
        center[0] + radius * np.cos(angle),
        center[1] + radius * np.sin(angle),
        color="#334155",
        lw=2.0,
    )
    ax.plot([center[0] - 1.9, center[0] + 1.9], [center[1], center[1]], color="#64748b", lw=1.4)
    ax.plot([point[0], projection[0]], [point[1], projection[1]], color="#94a3b8", lw=1.4, ls="--")
    ax.plot([center[0], point[0]], [center[1], point[1]], color=F.PURPLE, lw=2.4)
    ax.add_patch(Circle(center, 0.06, color=F.INK, zorder=6))
    ax.add_patch(Circle(point, 0.11, color=F.PURPLE, zorder=6))
    ax.add_patch(Circle(projection, 0.10, color=F.GREEN, zorder=6))

    F.arrow(ax, point, point + 0.95 * tangent, color=F.BLUE, lw=2.7)
    ax.text(*(point + 1.08 * tangent), r"$\vec v$（切線）", color=F.BLUE, fontsize=12, ha="center")
    F.arrow(ax, point, point - 1.05 * radial, color=F.RED, lw=2.8)
    ax.text(
        *(point - 0.60 * radial + np.array([-0.18, 0.18])),
        r"$\vec a$（向圓心）",
        color=F.RED,
        fontsize=11.5,
        ha="right",
    )
    horizontal_component = np.array([-1.05 * np.cos(phase), 0.0])
    full_acceleration = -1.05 * radial
    assert np.isclose(horizontal_component[0], full_acceleration[0])
    assert np.isclose(horizontal_component[1], 0.0)
    F.arrow(ax, point, point + horizontal_component, color=F.AMBER, lw=2.2, ls="--", mutation=14)
    ax.text(
        *(point + 0.52 * horizontal_component + np.array([0.0, 0.20])),
        r"$a_x$",
        color=F.AMBER,
        fontsize=12,
        ha="center",
    )
    ax.text(center[0] - 0.12, center[1] - 0.30, "$O$", fontsize=11.5, color=F.INK)
    ax.text((center[0] + projection[0]) / 2, center[1] - 0.35, "$x$", fontsize=12.5, color=F.GREEN, ha="center")

    plot_left, plot_right = -0.20, 5.45
    plot_mid, amplitude = 0.25, 1.35
    tau = np.linspace(0, 2 * np.pi, 600)
    curve_x = plot_left + (plot_right - plot_left) * tau / (2 * np.pi)
    curve_y = plot_mid + amplitude * np.cos(tau)
    ax.plot([plot_left, plot_right + 0.20], [plot_mid, plot_mid], color="#64748b", lw=1.3)
    ax.plot([plot_left, plot_left], [plot_mid - 1.65, plot_mid + 1.65], color="#64748b", lw=1.3)
    ax.plot(curve_x, curve_y, color=F.GREEN, lw=2.8)
    phase_x = plot_left + (plot_right - plot_left) * phase / (2 * np.pi)
    phase_y = plot_mid + amplitude * np.cos(phase)
    assert np.isclose((phase_y - plot_mid) / amplitude, np.cos(phase))
    ax.plot([phase_x, phase_x], [plot_mid, phase_y], color="#94a3b8", lw=1.2, ls="--")
    ax.scatter([phase_x], [phase_y], s=70, color=F.PURPLE, edgecolors="white", linewidths=1.0, zorder=6)
    ax.text(plot_left - 0.18, plot_mid + amplitude, "$+A$", fontsize=11.5, ha="right", va="center")
    ax.text(plot_left - 0.18, plot_mid - amplitude, "$-A$", fontsize=11.5, ha="right", va="center")
    ax.text(plot_left, plot_mid - 0.30, "$0$", fontsize=11, ha="center")
    ax.text(plot_right, plot_mid - 0.30, r"$2\pi$", fontsize=11, ha="center")
    ax.text(plot_right + 0.15, plot_mid - 0.20, r"$\omega t$", fontsize=12, ha="left")
    ax.text(plot_left - 0.18, plot_mid + 1.70, "$x$", fontsize=12, ha="right")
    ax.text(2.62, 2.05, "餘弦從正端點 $x=+A$ 開始", fontsize=12.5, color=F.INK, ha="center")

    ax.text(
        0.25,
        -2.05,
        r"投影分量：$x=A\cos\omega t$，$v_x=-A\omega\sin\omega t$，$a_x=-\omega^2x$",
        ha="center",
        fontsize=13,
        color=F.INK,
        bbox=dict(boxstyle="round,pad=0.35", fc="white", ec="#cbd5e1", lw=1.2),
    )
    ax.set_xlim(-5.25, 6.25)
    ax.set_ylim(-2.55, 2.75)
    ax.set_title("等速圓周的 x 投影：向心加速度的 x 分量形成簡諧運動", fontsize=15, pad=12)
    _save(fig, "選物I-4-圓周與簡諧")


def fig_newton_second_experiment():
    """用兩組可線性化資料呈現 F–a 與 a–1/M 實驗。"""
    fixed_mass = 2.0
    forces = np.array([0.50, 1.00, 1.50, 2.00, 2.50])
    acceleration_force = forces / fixed_mass
    fixed_force = 1.20
    masses = np.array([4.0, 3.0, 2.0, 1.5, 1.0])
    inverse_mass = 1.0 / masses
    acceleration_mass = fixed_force * inverse_mass

    assert np.allclose(acceleration_force / forces, 1 / fixed_mass)
    assert np.allclose(acceleration_mass / inverse_mass, fixed_force)

    fig, axes = plt.subplots(1, 2, figsize=(11.4, 4.8))
    fig.patch.set_facecolor("white")
    ax_force, ax_mass = axes

    ax_force.plot(forces, acceleration_force, color=F.BLUE, lw=2.6)
    ax_force.scatter(forces, acceleration_force, s=62, color=F.RED, edgecolors="white", zorder=4)
    ax_force.set_xlabel(r"合力 $F_{\rm net}$ (N)")
    ax_force.set_ylabel(r"加速度 $a$ (m/s$^2$)")
    ax_force.set_title(r"固定 $M=2.0\ \mathrm{kg}$：$a\propto F_{\rm net}$", fontsize=13.5)
    ax_force.text(0.72, 1.17, r"斜率 $\Delta a/\Delta F=1/M=0.50\ \mathrm{kg^{-1}}$", fontsize=10.8, color=F.INK)
    ax_force.set_xlim(0, 2.75)
    ax_force.set_ylim(0, 1.42)
    F.clean_grid(ax_force)

    ax_mass.plot(inverse_mass, acceleration_mass, color=F.GREEN, lw=2.6)
    ax_mass.scatter(inverse_mass, acceleration_mass, s=62, color=F.PURPLE, edgecolors="white", zorder=4)
    ax_mass.set_xlabel(r"系統總質量的倒數 $1/M$ (kg$^{-1}$)")
    ax_mass.set_ylabel(r"加速度 $a$ (m/s$^2$)")
    ax_mass.set_title(r"固定 $F_{\rm net}=1.20\ \mathrm{N}$：$a\propto1/M$", fontsize=13.5)
    ax_mass.text(0.31, 1.12, r"斜率 $\Delta a/\Delta(1/M)=F_{\rm net}=1.20\ \mathrm{N}$", fontsize=10.8, color=F.INK)
    ax_mass.set_xlim(0, 1.08)
    ax_mass.set_ylim(0, 1.34)
    F.clean_grid(ax_mass)

    fig.suptitle("牛頓第二定律的實驗檢驗：每次只改變一個量", fontsize=15.5, y=0.98)
    fig.text(0.5, 0.01, r"兩組斜率共同支持 $a=F_{\rm net}/M$；截距偏離 0 時應檢查摩擦、滑輪慣量與傳感器零點。", ha="center", fontsize=11.2, color="#475569")
    fig.subplots_adjust(left=0.08, right=0.98, top=0.82, bottom=0.20, wspace=0.28)
    _save(fig, "選物I-4-牛頓第二定律實驗")


def fig_apparent_weight_connected():
    """以三個自由體圖呈現視重、水平連接體與阿特伍德機。"""
    fig, ax = F.canvas(12.0, 5.2)
    ax.axis("off")
    ax.set_xlim(-6.0, 6.0)
    ax.set_ylim(-2.8, 2.65)

    # 電梯中的人
    ax.add_patch(Rectangle((-5.55, -1.40), 2.75, 3.25, facecolor="#f8fafc", edgecolor="#64748b", lw=1.5))
    person = np.array([-4.18, -0.35])
    ax.add_patch(Circle(person + np.array([0, 0.55]), 0.20, facecolor="#fde68a", edgecolor="#92400e", lw=1.2))
    ax.plot([person[0], person[0]], [person[1] + 0.35, person[1] - 0.42], color=F.INK, lw=2.0)
    ax.plot([person[0] - 0.32, person[0] + 0.32], [person[1] + 0.05, person[1] + 0.05], color=F.INK, lw=1.8)
    ax.plot([person[0], person[0] - 0.28], [person[1] - 0.42, person[1] - 0.92], color=F.INK, lw=1.8)
    ax.plot([person[0], person[0] + 0.28], [person[1] - 0.42, person[1] - 0.92], color=F.INK, lw=1.8)
    F.arrow(ax, person, person + np.array([0, 1.30]), color=F.BLUE, lw=2.8)
    F.arrow(ax, person, person + np.array([0, -1.30]), color=F.RED, lw=2.8)
    F.arrow(ax, (-5.20, 0.55), (-5.20, 1.45), color=F.GREEN, lw=2.3)
    ax.text(-3.95, 1.05, "$N$", color=F.BLUE, fontsize=13)
    ax.text(-3.92, -1.15, "$mg$", color=F.RED, fontsize=13)
    ax.text(-5.05, 1.58, "$a$", color=F.GREEN, fontsize=13)
    ax.text(-4.18, 2.18, r"視重：$N-mg=ma$", ha="center", fontsize=12.8, weight="bold")

    # 水平連接體
    ax.plot([-1.82, 1.75], [-1.15, -1.15], color="#64748b", lw=1.7)
    ax.add_patch(Rectangle((-1.55, -0.65), 1.15, 1.0, facecolor="#dbeafe", edgecolor=F.BLUE, lw=1.5))
    ax.add_patch(Rectangle((0.25, -0.65), 1.15, 1.0, facecolor="#dcfce7", edgecolor=F.GREEN, lw=1.5))
    ax.plot([-0.40, 0.25], [-0.15, -0.15], color=F.PURPLE, lw=2.2)
    F.arrow(ax, (-2.25, -0.15), (-1.55, -0.15), color=F.AMBER, lw=2.7)
    F.arrow(ax, (-0.40, -0.15), (0.05, -0.15), color=F.PURPLE, lw=2.5)
    F.arrow(ax, (0.25, -0.15), (-0.20, -0.15), color=F.PURPLE, lw=2.5)
    F.arrow(ax, (1.40, -0.15), (2.15, -0.15), color=F.GREEN, lw=2.6)
    ax.text(-0.98, -0.15, "$m_1$", ha="center", va="center", fontsize=12.5)
    ax.text(0.82, -0.15, "$m_2$", ha="center", va="center", fontsize=12.5)
    ax.text(-2.05, 0.12, "$F$", color=F.AMBER, fontsize=12.5)
    ax.text(-0.10, 0.12, "$T$", color=F.PURPLE, fontsize=12.5, ha="center")
    ax.text(2.02, 0.12, "$a$", color=F.GREEN, fontsize=12.5)
    ax.text(0, 2.18, r"連接體：整體求 $a$，隔離求 $T$", ha="center", fontsize=12.8, weight="bold")

    # 阿特伍德機
    pulley = np.array([4.25, 0.92])
    ax.add_patch(Circle(pulley, 0.50, facecolor="#f1f5f9", edgecolor="#64748b", lw=1.6))
    ax.plot([3.75, 3.10], [0.92, 0.92], color=F.PURPLE, lw=2.0)
    ax.plot([4.75, 5.35], [0.92, 0.92], color=F.PURPLE, lw=2.0)
    ax.plot([3.10, 3.10], [0.92, -0.55], color=F.PURPLE, lw=2.0)
    ax.plot([5.35, 5.35], [0.92, -1.10], color=F.PURPLE, lw=2.0)
    ax.add_patch(Rectangle((2.67, -1.15), 0.86, 0.60, facecolor="#dbeafe", edgecolor=F.BLUE, lw=1.4))
    ax.add_patch(Rectangle((4.87, -1.85), 0.96, 0.75, facecolor="#fee2e2", edgecolor=F.RED, lw=1.4))
    F.arrow(ax, (3.10, -0.55), (3.10, 0.22), color=F.PURPLE, lw=2.4)
    F.arrow(ax, (3.10, -0.85), (3.10, -1.65), color=F.RED, lw=2.4)
    F.arrow(ax, (5.35, -1.10), (5.35, -0.28), color=F.PURPLE, lw=2.4)
    F.arrow(ax, (5.35, -1.48), (5.35, -2.35), color=F.RED, lw=2.4)
    ax.text(2.92, -0.93, "$m_1$", fontsize=11.8)
    ax.text(5.15, -1.57, "$m_2$", fontsize=11.8)
    ax.text(4.25, 2.18, r"輕繩理想滑輪：$|a_1|=|a_2|$", ha="center", fontsize=12.8, weight="bold")

    ax.text(0, -2.58, "三組圖都先限定受力體；箭頭方向直接決定方程中的正負號。", ha="center", fontsize=11.4, color="#475569")
    ax.set_title("視重與連接體：圖上的每一支力都要進入對應受力體的方程", fontsize=15, pad=10)
    _save(fig, "選物I-4-視重與連接體")


def fig_centripetal_geometry():
    """由位置三角形與速度三角形推導向心加速度。"""
    fig, ax = F.canvas(11.7, 5.1)
    ax.axis("off")
    ax.set_aspect("equal")
    center = np.array([-3.55, -0.10])
    radius = 1.72
    angle1, angle2 = np.deg2rad([52.0, 78.0])
    r1 = radius * np.array([np.cos(angle1), np.sin(angle1)])
    r2 = radius * np.array([np.cos(angle2), np.sin(angle2)])
    p1, p2 = center + r1, center + r2
    theta = angle2 - angle1
    speed = 1.42
    v1 = speed * np.array([-np.sin(angle1), np.cos(angle1)])
    v2 = speed * np.array([-np.sin(angle2), np.cos(angle2)])
    delta_v = v2 - v1
    chord = p2 - p1

    assert np.isclose(np.linalg.norm(r1), radius)
    assert np.isclose(np.linalg.norm(r2), radius)
    assert np.isclose(np.linalg.norm(delta_v) / speed, np.linalg.norm(chord) / radius)
    assert np.isclose(np.linalg.norm(chord), 2 * radius * np.sin(theta / 2))

    ang = np.linspace(0, 2 * np.pi, 500)
    ax.plot(center[0] + radius * np.cos(ang), center[1] + radius * np.sin(ang), color="#94a3b8", lw=1.5)
    ax.plot([center[0], p1[0]], [center[1], p1[1]], color=F.PURPLE, lw=1.8)
    ax.plot([center[0], p2[0]], [center[1], p2[1]], color=F.PURPLE, lw=1.8)
    ax.plot([p1[0], p2[0]], [p1[1], p2[1]], color=F.AMBER, lw=2.2)
    ax.add_patch(Arc(center, 0.90, 0.90, theta1=np.rad2deg(angle1), theta2=np.rad2deg(angle2), color=F.GREEN, lw=1.7))
    ax.text(*(center + 0.66 * np.array([np.cos((angle1 + angle2) / 2), np.sin((angle1 + angle2) / 2)])), r"$\Delta\theta$", color=F.GREEN, fontsize=12)
    F.arrow(ax, p1, p1 + 0.78 * v1, color=F.BLUE, lw=2.6)
    F.arrow(ax, p2, p2 + 0.78 * v2, color=F.BLUE, lw=2.6)
    ax.text(*(p1 + 0.86 * v1), r"$\vec v_1$", color=F.BLUE, fontsize=12)
    ax.text(*(p2 + 0.86 * v2), r"$\vec v_2$", color=F.BLUE, fontsize=12)
    ax.text(-3.55, -2.18, r"位置三角形：$|\Delta\vec r|=2R\sin(\Delta\theta/2)$", ha="center", fontsize=12.2)

    origin = np.array([1.00, -0.82])
    F.arrow(ax, origin, origin + v1, color=F.BLUE, lw=2.7)
    F.arrow(ax, origin, origin + v2, color=F.GREEN, lw=2.7)
    F.arrow(ax, origin + v1, origin + v2, color=F.RED, lw=2.7)
    ax.text(*(origin + 0.52 * v1 + np.array([-0.12, 0.06])), r"$\vec v_1$", color=F.BLUE, fontsize=12)
    ax.text(*(origin + 0.54 * v2 + np.array([0.10, -0.08])), r"$\vec v_2$", color=F.GREEN, fontsize=12)
    ax.text(*(origin + 0.5 * (v1 + v2) + np.array([0.38, 0.05])), r"$\Delta\vec v$", color=F.RED, fontsize=12)
    ax.text(2.25, 1.72, r"速度三角形：$|\Delta\vec v|=2v\sin(\Delta\theta/2)$", ha="center", fontsize=12.2)
    ax.text(2.25, 0.88, r"$\dfrac{|\Delta\vec v|}{v}=\dfrac{|\Delta\vec r|}{R}$", ha="center", fontsize=16, color=F.PURPLE)
    ax.text(2.25, 0.16, r"$\Delta t\to0:\quad a_c=\dfrac{|\Delta\vec v|}{\Delta t}=\dfrac{v}{R}\dfrac{|\Delta\vec r|}{\Delta t}=\dfrac{v^2}{R}$", ha="center", fontsize=13.2, color=F.INK)
    ax.text(2.25, -1.65, r"$\Delta\vec v$ 在極限中指向圓心，所以 $\vec a_c$ 也指向圓心。", ha="center", fontsize=11.7, color="#475569")
    ax.set_xlim(-5.85, 5.85)
    ax.set_ylim(-2.60, 2.70)
    ax.set_title("向心加速度的幾何推導：速率不變，速度向量仍持續改變", fontsize=15, pad=12)
    _save(fig, "選物I-4-向心加速度推導")


def fig_circular_force_models():
    """呈現三種向心合力的實際來源。"""
    fig, ax = F.canvas(12.0, 4.9)
    ax.axis("off")
    ax.set_xlim(-6.0, 6.0)
    ax.set_ylim(-2.6, 2.55)

    centers = [-4.05, 0.0, 4.05]
    titles = ["繩系小球（上視）", "水平彎道（上視）", "鉛直圓底端（側視）"]
    for x, title in zip(centers, titles):
        ax.text(x, 2.10, title, ha="center", fontsize=13, weight="bold")

    # 繩系小球
    c1 = np.array([centers[0], 0.0])
    p1 = c1 + np.array([1.25, 0.62])
    ax.add_patch(Circle(c1, 0.09, color=F.INK))
    ax.plot([c1[0], p1[0]], [c1[1], p1[1]], color="#64748b", lw=2.0)
    ax.add_patch(Circle(p1, 0.16, facecolor="#fde68a", edgecolor="#92400e", lw=1.3))
    F.arrow(ax, p1, p1 + 0.80 * (c1 - p1) / np.linalg.norm(c1 - p1), color=F.RED, lw=2.8)
    F.arrow(ax, p1, p1 + np.array([-0.36, 0.72]), color=F.BLUE, lw=2.5)
    ax.text(-3.62, 0.38, "$T$", color=F.RED, fontsize=12)
    ax.text(-3.42, 1.34, "$v$", color=F.BLUE, fontsize=12)
    ax.text(centers[0], -1.75, r"$T=mv^2/R$", ha="center", fontsize=13.5, color=F.PURPLE)

    # 彎道
    c2 = np.array([centers[1], 0.0])
    p2 = c2 + np.array([1.20, 0.0])
    ax.add_patch(Circle(c2, 1.40, fill=False, edgecolor="#94a3b8", lw=1.5, ls="--"))
    ax.add_patch(Rectangle((p2[0] - 0.30, -0.18), 0.60, 0.36, angle=90, facecolor="#dbeafe", edgecolor=F.BLUE, lw=1.4))
    F.arrow(ax, p2, p2 + np.array([-0.92, 0]), color=F.RED, lw=2.8)
    F.arrow(ax, p2, p2 + np.array([0, 0.88]), color=F.BLUE, lw=2.5)
    ax.text(0.48, 0.18, "$f_s$", color=F.RED, fontsize=12)
    ax.text(1.38, 0.80, "$v$", color=F.BLUE, fontsize=12)
    ax.text(centers[1], -1.75, r"$f_s=mv^2/R$", ha="center", fontsize=13.5, color=F.PURPLE)

    # 鉛直圓底端
    c3 = np.array([centers[2], 0.25])
    radius = 1.35
    p3 = c3 + np.array([0, -radius])
    ax.add_patch(Circle(c3, radius, fill=False, edgecolor="#94a3b8", lw=1.6))
    ax.add_patch(Circle(p3, 0.17, facecolor="#fee2e2", edgecolor=F.RED, lw=1.3))
    F.arrow(ax, p3, p3 + np.array([0, 1.05]), color=F.BLUE, lw=2.8)
    F.arrow(ax, p3, p3 + np.array([0, -0.72]), color=F.RED, lw=2.8)
    F.arrow(ax, p3, p3 + np.array([0.80, 0]), color=F.GREEN, lw=2.5)
    ax.text(4.20, -0.38, "$N$", color=F.BLUE, fontsize=12)
    ax.text(4.20, -1.78, "$mg$", color=F.RED, fontsize=12)
    ax.text(4.80, -1.23, "$v$", color=F.GREEN, fontsize=12)
    ax.text(centers[2], -2.18, r"$N-mg=mv^2/R$", ha="center", fontsize=13.5, color=F.PURPLE)

    ax.text(0, -2.43, "只把真實交互作用畫成力；指向圓心的分量和才是當下的徑向合力。", ha="center", fontsize=11.3, color="#475569")
    ax.set_title("向心合力的來源由實際接觸與遠距作用決定", fontsize=15, pad=10)
    _save(fig, "選物I-4-圓周受力模型")


def fig_shm_phase_states():
    """對齊呈現簡諧運動的空間狀態與 x、v、a 相位。"""
    omega = 2 * np.pi
    time = np.linspace(0, 1, 700)
    x = np.cos(omega * time)
    velocity = -np.sin(omega * time)
    acceleration = -np.cos(omega * time)
    assert np.allclose(acceleration, -x)
    assert np.isclose(x[0], 1.0) and np.isclose(velocity[0], 0.0)

    fig = plt.figure(figsize=(11.6, 6.2), facecolor="white")
    gs = fig.add_gridspec(2, 1, height_ratios=[0.9, 2.0], hspace=0.30)
    ax_state = fig.add_subplot(gs[0])
    ax_state.axis("off")
    ax_state.set_xlim(-1.25, 1.25)
    ax_state.set_ylim(-0.55, 0.62)
    ax_state.plot([-1.05, 1.05], [0, 0], color="#64748b", lw=1.5)
    states = [(-1.0, "$-A$", 1, 0), (0.0, "$0$", 1, 0), (1.0, "$+A$", -1, 0)]
    for pos, label, acc_dir, _ in states:
        ax_state.add_patch(Rectangle((pos - 0.12, -0.12), 0.24, 0.24, facecolor="#fde68a", edgecolor="#92400e", lw=1.3))
        ax_state.text(pos, -0.35, label, ha="center", fontsize=12.5)
        if pos != 0:
            F.arrow(ax_state, (pos, 0.12), (pos + 0.34 * acc_dir, 0.12), color=F.RED, lw=2.2, mutation=13)
            ax_state.text(pos + 0.18 * acc_dir, 0.31, "$a$", color=F.RED, fontsize=11, ha="center")
    F.arrow(ax_state, (-0.10, -0.02), (0.33, -0.02), color=F.BLUE, lw=2.2, mutation=13)
    ax_state.text(0.12, 0.16, r"$v_{\max}$", color=F.BLUE, fontsize=11, ha="center")
    ax_state.text(0, 0.52, r"端點：$v=0,\ |a|$ 最大　　平衡點：$|v|$ 最大, $a=0$", ha="center", fontsize=12.3)

    subgs = gs[1].subgridspec(3, 1, hspace=0.08)
    series = [(x, F.GREEN, r"$x/A$"), (velocity, F.BLUE, r"$v/(A\omega)$"), (acceleration, F.RED, r"$a/(A\omega^2)$")]
    axes = []
    for idx, (values, color, label) in enumerate(series):
        ax = fig.add_subplot(subgs[idx])
        axes.append(ax)
        ax.plot(time, values, color=color, lw=2.4)
        ax.axhline(0, color="#94a3b8", lw=0.9)
        for marker in [0, 0.25, 0.5, 0.75, 1.0]:
            ax.axvline(marker, color="#e2e8f0", lw=0.8, ls="--")
        ax.set_ylim(-1.18, 1.18)
        ax.set_yticks([-1, 0, 1])
        ax.set_ylabel(label, rotation=0, labelpad=28, color=color, fontsize=11.5)
        ax.grid(False)
        if idx < 2:
            ax.set_xticklabels([])
        else:
            ax.set_xticks([0, 0.25, 0.5, 0.75, 1.0], ["0", "$T/4$", "$T/2$", "$3T/4$", "$T$"])
            ax.set_xlabel("時間")
        ax.spines[["top", "right"]].set_visible(False)
    fig.suptitle(r"簡諧運動的狀態與相位：$a=-\omega^2x$，$v$ 較 $x$ 超前四分之一週期", fontsize=15.5, y=0.98)
    fig.subplots_adjust(left=0.12, right=0.98, top=0.88, bottom=0.09)
    _save(fig, "選物I-4-簡諧狀態與相位")


def fig_pendulum_small_angle():
    """呈現單擺的切向受力與小角度近似。"""
    fig, ax = F.canvas(10.6, 5.0)
    ax.axis("off")
    ax.set_aspect("equal")
    pivot = np.array([-1.80, 1.90])
    length = 2.65
    theta = np.deg2rad(24.0)
    radial = np.array([np.sin(theta), -np.cos(theta)])
    tangent_to_equilibrium = np.array([-np.cos(theta), -np.sin(theta)])
    bob = pivot + length * radial
    assert np.isclose(np.linalg.norm(bob - pivot), length)
    assert np.isclose(np.dot(radial, tangent_to_equilibrium), 0.0)

    ax.plot([pivot[0], pivot[0]], [pivot[1], pivot[1] - length], color="#94a3b8", lw=1.3, ls="--")
    ax.plot([pivot[0], bob[0]], [pivot[1], bob[1]], color="#334155", lw=2.2)
    ax.add_patch(Circle(pivot, 0.08, color=F.INK))
    ax.add_patch(Circle(bob, 0.18, facecolor="#fde68a", edgecolor="#92400e", lw=1.4))
    ax.add_patch(Arc(pivot, 1.10, 1.10, theta1=270, theta2=270 + np.rad2deg(theta), color=F.GREEN, lw=1.8))
    ax.text(pivot[0] + 0.48, pivot[1] - 0.62, r"$\theta$", color=F.GREEN, fontsize=13)
    F.arrow(ax, bob, bob - 1.18 * radial, color=F.BLUE, lw=2.7)
    F.arrow(ax, bob, bob + np.array([0, -1.42]), color=F.RED, lw=2.7)
    F.arrow(ax, bob, bob + 1.03 * tangent_to_equilibrium, color=F.PURPLE, lw=2.7)
    ax.text(*(bob - 0.67 * radial + np.array([0.14, 0.05])), "$T$", color=F.BLUE, fontsize=12.5)
    ax.text(*(bob + np.array([0.18, -1.30])), "$mg$", color=F.RED, fontsize=12.5)
    ax.text(*(bob + 0.63 * tangent_to_equilibrium + np.array([-0.08, -0.15])), r"$mg\sin\theta$", color=F.PURPLE, fontsize=12)
    ax.text(-1.80, -1.62, r"切向：$F_t=-mg\sin\theta\approx-mg\theta=-\dfrac{mg}{L}x$", ha="center", fontsize=13, color=F.INK)

    xvals = np.linspace(-0.65, 0.65, 400)
    ax.plot(2.10 + 2.25 * xvals, 0.05 + 1.65 * np.sin(xvals), color=F.BLUE, lw=2.6, label=r"$\sin\theta$")
    ax.plot(2.10 + 2.25 * xvals, 0.05 + 1.65 * xvals, color=F.RED, lw=2.2, ls="--", label=r"$\theta$")
    ax.axvspan(2.10 - 2.25 * 0.20, 2.10 + 2.25 * 0.20, color="#dcfce7", alpha=0.7)
    ax.text(2.10, 1.82, r"小角區：$\sin\theta\approx\theta$", ha="center", fontsize=12.5, weight="bold")
    ax.text(2.10, -1.05, "角度需以弧度代入", ha="center", fontsize=11.5, color="#475569")
    ax.legend(loc="lower right", frameon=False, fontsize=11)
    ax.set_xlim(-4.50, 4.75)
    ax.set_ylim(-2.05, 2.58)
    ax.set_title("單擺的切向回復力：小角度時才近似與位移成正比", fontsize=15, pad=12)
    _save(fig, "選物I-4-單擺小角度")


def _panel_label(ax, label, title):
    ax.text(0.02, 0.96, label, transform=ax.transAxes, va="top", ha="left",
            fontsize=13, weight="bold", color=F.BLUE)
    ax.set_title(title, fontsize=12.2, pad=8)
    ax.set_aspect("equal", adjustable="box")
    ax.axis("off")


def fig_answer_forces():
    """章末 Q1--Q6 的定量向量圖、彈簧方向與自由體圖。"""
    fig, axes = plt.subplots(2, 3, figsize=(12.0, 7.2), facecolor="white")

    ax = axes[0, 0]
    _panel_label(ax, "A｜Q1", "力的分量與合成")
    o = np.array([0.0, 0.0]); f1 = np.array([2.0, 0.0]); f2 = np.array([-np.sqrt(3), 1.0]); fr = f1 + f2
    assert np.allclose(fr, [2 - np.sqrt(3), 1])
    F.arrow(ax, o, f1, color=F.BLUE, lw=2.7); F.arrow(ax, o, f2, color=F.RED, lw=2.7); F.arrow(ax, o, fr, color=F.GREEN, lw=3.0)
    ax.axhline(0, color="#94a3b8", lw=1); ax.axvline(0, color="#94a3b8", lw=1)
    ax.text(1.0, .12, r"$10\,\mathrm{N}$ 東", color=F.BLUE, ha="center", fontsize=10.5)
    ax.text(-1.15, .72, r"$10\,\mathrm{N}$ 北偏西 $60^\circ$", color=F.RED, ha="center", fontsize=9.5)
    ax.text(.42, .72, r"$\vec F_{\rm net}$", color=F.GREEN, fontsize=11)
    ax.set_xlim(-2.3, 2.5); ax.set_ylim(-.5, 1.8)

    ax = axes[0, 1]
    _panel_label(ax, "B｜Q3", r"光滑 $30^\circ$ 斜面")
    th = np.deg2rad(30); u = np.array([np.cos(th), np.sin(th)]); n = np.array([-np.sin(th), np.cos(th)])
    ax.plot([-2.0, 2.0], [-1.0, -1.0 + 4*np.tan(th)], color="#64748b", lw=2)
    p = np.array([0., .2]); F.arrow(ax, p, p + 1.2*n, color=F.BLUE, lw=2.6); F.arrow(ax, p, p + np.array([0,-1.6]), color=F.RED, lw=2.6)
    F.arrow(ax, p, p - .9*u, color=F.AMBER, lw=2.3)
    ax.text(*(p+1.28*n), "$N$", color=F.BLUE, fontsize=11); ax.text(*(p+np.array([.12,-1.55])), "$mg$", color=F.RED, fontsize=11)
    ax.text(*(p-.65*u+np.array([-.15,.12])), r"$mg\sin30^\circ$", color=F.AMBER, fontsize=9.5)
    ax.set_xlim(-2.3,2.3); ax.set_ylim(-1.5,2.0)

    ax = axes[0, 2]
    _panel_label(ax, "C｜Q4", "書、桌面與地球的交互作用")
    pos = {"書": np.array([0.,.5]), "桌面": np.array([0.,-1.0]), "地球": np.array([0.,1.9])}
    for name,p0 in pos.items():
        ax.add_patch(FancyBboxPatch((p0[0]-.55,p0[1]-.22),1.1,.44,boxstyle="round,pad=.04",fc="#f8fafc",ec="#64748b")); ax.text(*p0,name,ha="center",va="center",fontsize=11)
    F.arrow(ax, (-.32,.28), (-.32,-.72), color=F.BLUE, lw=2.3); F.arrow(ax, (.32,-.72), (.32,.28), color=F.BLUE, lw=2.3)
    F.arrow(ax, (-.32,.72), (-.32,1.62), color=F.RED, lw=2.3); F.arrow(ax, (.32,1.62), (.32,.72), color=F.RED, lw=2.3)
    ax.text(-.85,-.18,"接觸力對",color=F.BLUE,fontsize=9); ax.text(.52,1.18,"重力對",color=F.RED,fontsize=9)
    ax.set_xlim(-1.5,1.5); ax.set_ylim(-1.45,2.35)

    ax = axes[1, 0]
    _panel_label(ax, "D｜Q5", "整體求 $a$，隔離右塊求接觸力")
    ax.plot([-2.2,2.2],[-.75,-.75],color="#64748b")
    ax.add_patch(Rectangle((-1.5,-.55),1.2,.8,fc="#dbeafe",ec=F.BLUE)); ax.add_patch(Rectangle((-.3,-.55),1.5,.8,fc="#dcfce7",ec=F.GREEN))
    ax.text(-.9,-.15,r"$2.0\,\rm kg$",ha="center"); ax.text(.45,-.15,r"$3.0\,\rm kg$",ha="center")
    F.arrow(ax, (-2.15,-.15), (-1.5,-.15), color=F.AMBER, lw=2.7); ax.text(-1.92,.1,r"$20\,\rm N$",color=F.AMBER,ha="center",fontsize=10)
    F.arrow(ax, (1.2,-.15),(1.85,-.15),color=F.RED,lw=2.5); ax.text(1.55,.1,"$C$",color=F.RED)
    F.arrow(ax, (1.35,.55),(2.0,.55),color=F.GREEN,lw=2.2); ax.text(1.72,.78,"$a$",color=F.GREEN)
    ax.set_xlim(-2.4,2.4); ax.set_ylim(-1.1,1.1)

    ax = axes[1, 1]
    _panel_label(ax, "E｜Q6", "向上運動、加速度向下")
    p=np.array([0.,0.]); F.arrow(ax,p,p+np.array([0,1.35]),color=F.BLUE,lw=2.7); F.arrow(ax,p,p+np.array([0,-1.65]),color=F.RED,lw=2.7)
    F.arrow(ax,(1.1,.9),(1.1,1.65),color=F.PURPLE,lw=2.2); F.arrow(ax,(1.1,.7),(1.1,-.05),color=F.GREEN,lw=2.2)
    ax.text(.15,1.18,"$N$",color=F.BLUE); ax.text(.15,-1.5,"$mg$",color=F.RED); ax.text(1.28,1.45,"$v$",color=F.PURPLE); ax.text(1.28,.18,"$a$",color=F.GREEN)
    ax.text(0,-2.0,r"向上為正：$N-mg=ma$",ha="center",fontsize=10.5)
    ax.set_xlim(-1.6,1.8); ax.set_ylim(-2.25,2.0)

    ax = axes[1, 2]
    _panel_label(ax, "F｜Q2", "形變帶號決定彈簧力方向")
    ax.axvline(0, color="#94a3b8", lw=1.2, ls="--")
    ax.text(0, 1.25, r"自然長 $20\,\mathrm{cm}$", ha="center", fontsize=10.5, color="#475569",
            bbox=dict(facecolor="white", edgecolor="none", pad=1.2))
    for y, endpoint, color, length_label, force_label in [
        (0.52, 1.25, F.BLUE, r"$23\,\mathrm{cm}$：$x=+0.030\,\mathrm{m}$", r"$F_s=-kx$"),
        (-0.58, -0.82, F.RED, r"$18\,\mathrm{cm}$：$x=-0.020\,\mathrm{m}$", r"$F_s=-kx$"),
    ]:
        ax.plot([-1.65, endpoint], [y, y], color="#64748b", lw=1.3)
        ax.add_patch(Rectangle((endpoint - 0.13, y - 0.17), 0.26, 0.34, fc="#fde68a", ec="#92400e"))
        direction = -0.72 if endpoint > 0 else 0.72
        F.arrow(ax, (endpoint, y + 0.30), (endpoint + direction, y + 0.30), color=color, lw=2.5)
        ax.text(-0.18, y - 0.36, length_label, ha="center", fontsize=9.4)
        ax.text(endpoint + direction / 2, y + 0.51, force_label, ha="center", color=color, fontsize=10.2)
    ax.text(0, -1.50, r"$k=6.0/0.030=200\,\mathrm{N/m}$；壓縮時力向右", ha="center", fontsize=9.8,
            bbox=dict(facecolor="white", edgecolor="none", pad=1.0))
    ax.set_xlim(-1.95, 1.75); ax.set_ylim(-1.75, 1.55)
    fig.suptitle("章末解題圖 I：向量、自由體圖與交互作用", fontsize=16, y=.99)
    fig.tight_layout(rect=[0,.02,1,.96])
    _save(fig, "選物I-4-章末受力解題圖")


def fig_answer_periodic():
    """章末 Q7--Q9、Q15 的角量、狀態與實驗圖。"""
    fig, axes = plt.subplots(2, 2, figsize=(11.4, 7.4), facecolor="white")
    ax=axes[0,0]; _panel_label(ax,"A｜Q7",r"逆時針圓周：$\omega>0$")
    ang=np.linspace(0,2*np.pi,300); ax.plot(np.cos(ang),np.sin(ang),color="#64748b"); p=np.array([np.cos(.7),np.sin(.7)])
    F.arrow(ax,p,p+.75*np.array([-np.sin(.7),np.cos(.7)]),color=F.BLUE,lw=2.7); F.arrow(ax,p,p-.72*p,color=F.RED,lw=2.7)
    ax.add_patch(Arc((0,0),.85,.85,theta1=10,theta2=70,color=F.GREEN,lw=2)); ax.text(.48,.33,r"$+\Delta\theta$",color=F.GREEN,fontsize=10)
    ax.text(-.05,-1.35,r"$v=R|\omega|$；$a_c=R\omega^2$",ha="center",fontsize=11); ax.set_xlim(-1.5,1.5); ax.set_ylim(-1.55,1.5)

    ax=axes[0,1]; _panel_label(ax,"B｜Q8","彈簧簡諧運動的極值位置")
    ax.plot([-1.5,1.5],[0,0],color="#64748b");
    for x,lab in [(-1.2,"$-A$"),(0,"$0$"),(1.2,"$+A$")]: ax.axvline(x,color="#cbd5e1",ls="--",lw=1); ax.text(x,-.28,lab,ha="center")
    ax.add_patch(Rectangle((1.05,-.12),.3,.24,fc="#fde68a",ec="#92400e")); F.arrow(ax,(1.05,.25),(.45,.25),color=F.RED,lw=2.5); ax.text(.72,.4,r"$|a|_{\max}$",color=F.RED,ha="center",fontsize=10)
    F.arrow(ax,(-.35,-.55),(.35,-.55),color=F.BLUE,lw=2.5); ax.text(0,-.78,r"$v_{\max}$",color=F.BLUE,ha="center",fontsize=10)
    ax.text(0,1.0,r"$\omega=\sqrt{k/m}$",ha="center",fontsize=12); ax.set_xlim(-1.7,1.7); ax.set_ylim(-1.0,1.35)

    ax=axes[1,0]; _panel_label(ax,"C｜Q9","單擺模型的條件")
    pivot=np.array([0.,1.15]); th=.28; bob=pivot+1.4*np.array([np.sin(th),-np.cos(th)]); ax.plot([pivot[0],bob[0]],[pivot[1],bob[1]],color="#334155",lw=2); ax.plot([0,0],[1.15,-.35],color="#94a3b8",ls="--")
    ax.add_patch(Circle(bob,.10,fc="#fde68a",ec="#92400e")); F.arrow(ax,bob,bob+np.array([-.75,-.22]),color=F.PURPLE,lw=2.5); ax.text(-.05,-.38,r"$-mg\sin\theta\approx-mg\theta$",ha="center",fontsize=10.5)
    ax.text(0,-.72,r"小角且 $\theta$ 用 rad：$T=2\pi\sqrt{L/g}$",ha="center",fontsize=10.5); ax.set_xlim(-1.4,1.4); ax.set_ylim(-.95,1.5)

    ax=axes[1,1]; _panel_label(ax,"D｜Q15","以 $T^2$--$L$ 斜率估計 $g$")
    L=np.array([.40,.60,.80]); T=np.array([1.27,1.55,1.79]); y=T**2; slope=np.dot(L,y)/np.dot(L,L)
    xx=np.linspace(0,.9,100); ax.plot(xx,slope*xx,color=F.BLUE,lw=2.5); ax.scatter(L,y,color=F.RED,s=60,zorder=4)
    ax.set_aspect("auto"); ax.axis("on"); ax.spines[["top","right"]].set_visible(False); ax.set_xlabel("$L$ (m)"); ax.set_ylabel("$T^2$ (s$^2$)"); ax.grid(alpha=.2)
    ax.text(.08,3.0,rf"斜率 $q\approx {slope:.2f}\ \rm s^2/m$",fontsize=10.5); ax.text(.08,2.55,r"$g=4\pi^2/q$",fontsize=10.5)
    fig.suptitle("章末解題圖 II：角量、週期模型與實驗資料", fontsize=16, y=.99)
    fig.tight_layout(rect=[0,.02,1,.96])
    _save(fig, "選物I-4-章末週期解題圖")


def fig_answer_integrated():
    """整合 1--4 題的專用受力圖與簡諧資料圖。"""
    fig, axes=plt.subplots(2,2,figsize=(11.6,7.7),facecolor="white")
    axes = axes.ravel()
    ax=axes[0]; _panel_label(ax,"A｜整合1","斜面連接體")
    th=np.deg2rad(30); u=np.array([np.cos(th),np.sin(th)]); ax.plot([-1.8,1.8],[-1,-1+3.6*np.tan(th)],color="#64748b",lw=2)
    p1=np.array([-.65,-.2]); p2=p1+.95*u
    n=np.array([-np.sin(th),np.cos(th)])
    for p,m in [(p1,"$m_1$"),(p2,"$m_2$")]:
        ax.add_patch(Rectangle((p[0]-.18,p[1]-.13),.36,.26,angle=30,fc="#fde68a",ec="#92400e")); ax.text(*(p+np.array([.1,.2])),m,fontsize=10)
        F.arrow(ax,p,p+.48*n,color=F.BLUE,lw=1.9); F.arrow(ax,p,p+np.array([0,-.55]),color="#64748b",lw=1.9)
    F.arrow(ax,p1,p1+.55*u,color=F.PURPLE,lw=2.4); F.arrow(ax,p2,p2-.55*u,color=F.PURPLE,lw=2.4); F.arrow(ax,p2,p2+.85*u,color=F.GREEN,lw=2.6)
    F.arrow(ax,p1,p1-.65*u,color=F.RED,lw=2.2); F.arrow(ax,p2,p2-.75*u,color=F.RED,lw=2.2)
    ax.text(*(p1-.42*u+np.array([-.15,.08])),r"$m_1g\sin30^\circ$",color=F.RED,fontsize=8.2,ha="center")
    ax.text(*(p2-.52*u+np.array([-.05,.10])),r"$m_2g\sin30^\circ$",color=F.RED,fontsize=8.2,ha="center")
    ax.text(.85,.95,r"$35\,\rm N$",color=F.GREEN,fontsize=10); ax.text(-.1,.05,"$T$",color=F.PURPLE); ax.set_xlim(-2,2); ax.set_ylim(-1.4,1.7)

    ax=axes[1]; _panel_label(ax,"B｜整合2","彈簧力提供徑向合力")
    ax.add_patch(Circle((0,0),1.05,fill=False,ec="#94a3b8")); p=np.array([1.05,0]); ax.plot([0,p[0]],[0,p[1]],color=F.PURPLE,lw=2); ax.add_patch(Circle(p,.12,fc="#fde68a",ec="#92400e"))
    F.arrow(ax,p,p+np.array([-.8,0]),color=F.RED,lw=2.7); F.arrow(ax,p,p+np.array([0,.75]),color=F.BLUE,lw=2.5); ax.text(.55,.15,"$kx$",color=F.RED); ax.text(1.15,.62,"$v$",color=F.BLUE)
    ax.text(0,-1.38,r"$kx=mv^2/R$",ha="center",fontsize=11); ax.set_xlim(-1.45,1.55); ax.set_ylim(-1.55,1.45)

    ax=axes[2]; _panel_label(ax,"C｜整合3","電梯內的彈簧懸掛")
    ax.plot([0,0],[1.4,.35],color=F.PURPLE,lw=3); ax.add_patch(Rectangle((-.2,.05),.4,.3,fc="#dbeafe",ec=F.BLUE)); p=np.array([0,.2])
    F.arrow(ax,p,p+np.array([0,.9]),color=F.PURPLE,lw=2.7); F.arrow(ax,p,p+np.array([0,-.95]),color=F.RED,lw=2.7); F.arrow(ax,(.8,.2),(.8,1.0),color=F.GREEN,lw=2.4)
    ax.text(.15,.95,"$kx$",color=F.PURPLE); ax.text(.15,-.65,"$mg$",color=F.RED); ax.text(.95,.85,"$a$",color=F.GREEN); ax.text(0,-1.1,r"$kx-mg=ma$",ha="center",fontsize=11)
    ax.set_xlim(-1.2,1.4); ax.set_ylim(-1.3,1.65)

    ax=axes[3]
    ax.text(0.02, 0.96, "D｜整合4", transform=ax.transAxes, va="top", ha="left",
            fontsize=13, weight="bold", color=F.BLUE)
    t_data=np.array([0.00,0.20,0.40,0.60,0.80])
    x_data=np.array([0.040,0.000,-0.040,0.000,0.040])
    t=np.linspace(0,0.80,400)
    x=0.040*np.cos(2.5*np.pi*t)
    assert np.allclose(0.040*np.cos(2.5*np.pi*t_data),x_data,atol=1e-12)
    ax.plot(t,x,color=F.BLUE,lw=2.5)
    ax.scatter(t_data,x_data,color=F.RED,s=48,zorder=4)
    ax.axhline(0,color="#94a3b8",lw=1)
    ax.axvline(0.10,color=F.PURPLE,lw=1.4,ls="--")
    ax.scatter([0.10],[0.040/np.sqrt(2)],color=F.PURPLE,s=46,zorder=5)
    ax.text(0.13,0.030,r"$t=0.10\,s:\ \phi=\pi/4$",fontsize=10.2,color=F.PURPLE)
    ax.text(0.43,0.046,r"$A=0.040\,m,\quad T=0.80\,s$",ha="center",fontsize=10.6)
    ax.text(0.43,-0.052,r"$x(t)=0.040\cos(2.5\pi t)$",ha="center",fontsize=10.8,color=F.BLUE)
    ax.set_title("五筆位移資料固定振幅、週期與初相",fontsize=12.2,pad=8)
    ax.set_xlim(-0.03,0.84); ax.set_ylim(-0.060,0.060)
    ax.set_xlabel("$t$ (s)"); ax.set_ylabel("$x$ (m)")
    ax.grid(alpha=.18)
    fig.suptitle("整合題解題圖：受力箭頭與位移資料直接建立對應方程",fontsize=16,y=.98)
    fig.tight_layout(rect=[0,.02,1,.94],h_pad=1.2,w_pad=1.0)
    _save(fig,"選物I-4-整合題解題圖")


if __name__ == "__main__":
    fig_hooke_calibration()
    fig_free_body_diagram()
    fig_incline_components()
    fig_third_law_pair()
    fig_circular_projection()
    fig_newton_second_experiment()
    fig_apparent_weight_connected()
    fig_centripetal_geometry()
    fig_circular_force_models()
    fig_shm_phase_states()
    fig_pendulum_small_angle()
    fig_answer_forces()
    fig_answer_periodic()
    fig_answer_integrated()
    print("done.")
