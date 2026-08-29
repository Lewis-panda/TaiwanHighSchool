# -*- coding: utf-8 -*-
"""產生選物 I-5 公開學生講義的概念 SVG。

重繪：.venv/bin/python _tools/fig_content_選物I-5.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Ellipse, FancyBboxPatch, Polygon

import figlib as F


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CH = os.path.join(ROOT, "content", "選修物理I", "選物I-5")


def _save(fig, name):
    return F.save_to(fig, CH, name, output_subdir="assets", write_pdf=False)


def fig_center_distance():
    """以同一徑向線區分天體半徑、離地高度與到心距離。"""
    center = np.array([-1.8, -0.10])
    body_radius = 1.35
    height = 0.95
    center_distance = body_radius + height
    phase = np.deg2rad(55.0)
    radial = np.array([np.cos(phase), np.sin(phase)])
    normal = np.array([-radial[1], radial[0]])
    surface = center + body_radius * radial
    satellite = center + center_distance * radial

    assert np.isclose(np.linalg.norm(surface - center), body_radius)
    assert np.isclose(np.linalg.norm(satellite - surface), height)
    assert np.isclose(np.linalg.norm(satellite - center), center_distance)
    assert np.allclose(satellite - center, (body_radius + height) * radial)

    fig, ax = F.canvas(10.8, 4.8)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.add_patch(Circle(center, body_radius, facecolor="#dbeafe", edgecolor=F.BLUE, lw=2.2))
    ax.add_patch(Circle(center, 0.06, color=F.INK, zorder=6))
    ax.add_patch(Circle(satellite, 0.13, facecolor="#f59e0b", edgecolor="#92400e", lw=1.4, zorder=6))
    ax.plot([center[0], satellite[0]], [center[1], satellite[1]], color="#94a3b8", lw=1.3, ls="--")
    ax.text(*(center + np.array([-0.12, -0.28])), "球心", ha="center", fontsize=11.5)
    ax.text(*(satellite + 0.18 * normal), "衛星", fontsize=11.5, ha="center")

    near_offset = 0.24 * normal
    far_offset = -0.34 * normal
    for point in (center, surface, satellite):
        ax.plot(
            [point[0] + far_offset[0], point[0] + near_offset[0]],
            [point[1] + far_offset[1], point[1] + near_offset[1]],
            color="#cbd5e1",
            lw=0.9,
            ls=":",
        )
    ax.annotate("", xy=surface + near_offset, xytext=center + near_offset, arrowprops=dict(arrowstyle="<->", color=F.BLUE, lw=1.8))
    ax.annotate("", xy=satellite + near_offset, xytext=surface + near_offset, arrowprops=dict(arrowstyle="<->", color=F.GREEN, lw=1.8))
    ax.annotate("", xy=satellite + far_offset, xytext=center + far_offset, arrowprops=dict(arrowstyle="<->", color=F.PURPLE, lw=1.9))
    ax.text(*(0.5 * (center + surface) + near_offset + 0.12 * normal), "$R$", color=F.BLUE, fontsize=13, ha="center")
    ax.text(*(0.5 * (surface + satellite) + near_offset + 0.12 * normal), "$h$", color=F.GREEN, fontsize=13, ha="center")
    ax.text(*(0.5 * (center + satellite) + far_offset - 0.13 * normal), "$r$", color=F.PURPLE, fontsize=13, ha="center")

    ax.add_patch(
        FancyBboxPatch(
            (1.25, -0.78),
            3.85,
            1.82,
            boxstyle="round,pad=0.18,rounding_size=0.18",
            facecolor="#f8fafc",
            edgecolor="#cbd5e1",
            lw=1.5,
        )
    )
    ax.text(3.18, 0.60, "引力公式使用到球心的距離", ha="center", fontsize=13.5, weight="bold")
    ax.text(3.18, -0.02, r"$r=R+h$", ha="center", fontsize=18, color=F.PURPLE)
    ax.text(3.18, -0.48, "高度從表面量；$r$ 從球心量", ha="center", fontsize=11.5)
    ax.set_xlim(-3.55, 5.40)
    ax.set_ylim(-2.00, 2.65)
    ax.set_title("離地高度與軌道半徑使用不同起點", fontsize=15, pad=12)
    _save(fig, "選物I-5-高度與中心距離")


def fig_inverse_square_scaling():
    """以曲線與比值法呈現反平方縮放。"""
    fig, ax = F.canvas(11.4, 4.8)
    ax.axis("off")
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 5)

    graph_left, graph_right = 0.85, 7.00
    graph_bottom, graph_top = 0.75, 4.00

    def graph_x(value):
        return graph_left + (value - 1.0) * (graph_right - graph_left) / 2.25

    def graph_y(value):
        return graph_bottom + value * (graph_top - graph_bottom) / 1.10

    ax.plot([graph_left, graph_right], [graph_bottom, graph_bottom], color=F.INK, lw=1.4)
    ax.plot([graph_left, graph_left], [graph_bottom, graph_top], color=F.INK, lw=1.4)
    x = np.linspace(1.0, 3.25, 500)
    ax.plot(graph_x(x), graph_y(1 / x**2), color=F.BLUE, lw=2.8)
    points = [(1, 1, "$F_0$"), (2, 1 / 4, "$F_0/4$"), (3, 1 / 9, "$F_0/9$")]
    assert np.allclose([force for _, force, _ in points], [1.0, 0.25, 1 / 9])
    for distance, force, label in points:
        px, py = graph_x(distance), graph_y(force)
        ax.plot([px, px], [graph_bottom, py], color="#94a3b8", lw=1.1, ls="--")
        ax.plot([graph_left, px], [py, py], color="#94a3b8", lw=1.1, ls="--")
        ax.scatter([px], [py], s=70, color=F.RED, edgecolors="white", linewidths=1.0, zorder=5)
        ax.text(px + 0.12, py + 0.10, label, color=F.RED, fontsize=11.5)
    for distance, label in [(1, "$r_0$"), (2, "$2r_0$"), (3, "$3r_0$")]:
        px = graph_x(distance)
        ax.text(px, graph_bottom - 0.22, label, fontsize=11.5, ha="center", va="top")
    for force, label in [(1 / 9, "$1/9$"), (1 / 4, "$1/4$"), (1, "$1$")]:
        py = graph_y(force)
        ax.text(graph_left - 0.16, py, label, fontsize=11.5, ha="right", va="center")
    ax.text((graph_left + graph_right) / 2, graph_bottom - 0.62, "中心距離 $r$", fontsize=12, ha="center")
    ax.text(0.22, 2.35, r"力的比例 $F/F_0$", fontsize=12, rotation=90, ha="center", va="center")
    ax.text(3.90, 4.28, r"距離放大 $\lambda$ 倍，力縮成 $1/\lambda^2$", fontsize=12.5, ha="center")

    ax.add_patch(
        FancyBboxPatch(
            (7.55, 2.48),
            4.05,
            1.72,
            boxstyle="round,pad=0.18,rounding_size=0.18",
            facecolor="#f8fafc",
            edgecolor="#cbd5e1",
            lw=1.5,
        )
    )
    ax.text(9.58, 3.88, "比值法", ha="center", fontsize=14, weight="bold")
    ax.text(9.58, 3.34, r"$r_2=\lambda r_1$", ha="center", fontsize=14, color=F.BLUE)
    ax.text(9.58, 2.78, r"$\frac{F_2}{F_1}=\left(\frac{r_1}{r_2}\right)^2=\frac{1}{\lambda^2}$", ha="center", fontsize=13.2, color=F.PURPLE)

    rows = [
        ("距離", "$r_0$", "$2r_0$", "$3r_0$"),
        ("引力", "$F_0$", "$F_0/4$", "$F_0/9$"),
    ]
    xcols = [7.78, 8.78, 9.78, 10.82]
    for y, row in zip([1.75, 1.08], rows):
        for xcol, text in zip(xcols, row):
            ax.text(
                xcol,
                y,
                text,
                ha="center",
                va="center",
                fontsize=11.5,
                color=F.INK if xcol == xcols[0] else F.RED if y < 1.5 else F.BLUE,
                weight="bold" if xcol == xcols[0] else "normal",
            )
    ax.plot([7.60, 11.55], [1.42, 1.42], color="#e2e8f0", lw=1.0)
    ax.text(9.40, 0.48, "質量固定：距離倍率平方後取倒數", ha="center", fontsize=11.2, color=F.INK)

    ax.set_title("反平方縮放：用距離倍率直接比較引力或重力加速度", fontsize=15, pad=12)
    _save(fig, "選物I-5-反平方縮放")


def fig_gravity_orbit_chain():
    """以中心距離、切向速度與向心引力建立圓軌道推導鏈。"""
    center = np.array([-3.0, 0.0])
    body_radius = 1.0
    orbit_radius = 2.25
    phase = np.deg2rad(25.0)
    radial = np.array([np.cos(phase), np.sin(phase)])
    tangent = np.array([-np.sin(phase), np.cos(phase)])
    satellite = center + orbit_radius * radial
    gravity_vector = -0.85 * radial
    velocity_vector = 0.95 * tangent

    assert np.isclose(np.linalg.norm(satellite - center), orbit_radius)
    assert np.isclose(np.dot(radial, tangent), 0.0)
    assert np.isclose(radial[0] * gravity_vector[1] - radial[1] * gravity_vector[0], 0.0)
    assert np.dot(radial, gravity_vector) < 0
    assert orbit_radius - np.linalg.norm(gravity_vector) > body_radius

    fig, ax = F.canvas(11.8, 5.2)
    ax.set_aspect("equal")
    ax.axis("off")
    angle = np.linspace(0, 2 * np.pi, 500)
    ax.plot(center[0] + orbit_radius * np.cos(angle), center[1] + orbit_radius * np.sin(angle), color="#94a3b8", lw=1.7, ls="--")
    ax.add_patch(Circle(center, body_radius, facecolor="#dbeafe", edgecolor=F.BLUE, lw=2.2, zorder=2))
    ax.text(*center, "中央天體 $M$", ha="center", va="center", fontsize=14, weight="bold")
    ax.plot([center[0], satellite[0]], [center[1], satellite[1]], color=F.PURPLE, lw=1.5, ls=":")
    radius_label = center + 0.52 * orbit_radius * radial + 0.15 * tangent
    ax.text(*radius_label, "$r$", color=F.PURPLE, fontsize=13, ha="center")
    ax.add_patch(Circle(satellite, 0.13, facecolor="#f59e0b", edgecolor="#92400e", lw=1.4, zorder=6))
    ax.text(*(satellite + np.array([0.18, -0.32])), "衛星 $m$", fontsize=11.5)
    F.arrow(ax, satellite, satellite + gravity_vector, color=F.RED, lw=3.0, mutation=19)
    F.arrow(ax, satellite, satellite + velocity_vector, color=F.GREEN, lw=3.0, mutation=19)
    ax.text(*(satellite + 0.55 * gravity_vector + 0.20 * tangent), r"$\vec F_g$（向心）", color=F.RED, fontsize=11.5, ha="center")
    ax.text(*(satellite + 1.08 * velocity_vector), r"$\vec v$（切線）", color=F.GREEN, fontsize=11.5, ha="center")

    ax.add_patch(
        FancyBboxPatch(
            (0.25, -1.82),
            4.55,
            3.64,
            boxstyle="round,pad=0.18,rounding_size=0.18",
            facecolor="#f8fafc",
            edgecolor="#cbd5e1",
            lw=1.5,
        )
    )
    ax.text(2.52, 1.32, "重力就是圓軌道的徑向合力", ha="center", fontsize=14, weight="bold")
    ax.text(2.52, 0.67, r"$G\frac{Mm}{r^2}=m\frac{v^2}{r}$", ha="center", fontsize=13.5, color=F.RED)
    ax.text(2.52, 0.02, r"$v=\sqrt{GM/r}$", ha="center", fontsize=14.5, color=F.PURPLE)
    ax.text(2.52, -0.61, r"$T=2\pi\sqrt{r^3/(GM)}$", ha="center", fontsize=14.5, color=F.BLUE)
    ax.text(2.52, -1.24, r"$\frac{T^2}{r^3}=\frac{4\pi^2}{GM}$", ha="center", fontsize=13.5, color=F.GREEN)
    ax.text(-3.0, -2.72, "圓軌道模型：中央天體近似固定，並忽略其他作用", ha="center", fontsize=11.3, color="#64748b")
    ax.set_xlim(-5.70, 5.25)
    ax.set_ylim(-3.00, 2.90)
    ax.set_title("同一支萬有引力同時決定重力加速度與圓軌道", fontsize=15, pad=12)
    _save(fig, "選物I-5-引力軌道鏈")


def fig_kepler_third_comparison():
    """同一中央天體的兩軌道週期比。"""
    fig, ax = F.canvas(11.6, 4.9)
    ax.set_aspect("equal")
    ax.axis("off")
    center = np.array([-3.25, 0.0])
    inner, outer = 0.58, 2.32
    period_ratio = (outer / inner) ** 1.5
    assert np.isclose(outer / inner, 4.0)
    assert np.isclose(period_ratio, 8.0)
    ax.add_patch(Circle(center, outer, fill=False, edgecolor="#94a3b8", lw=1.7, ls="--"))
    ax.add_patch(Circle(center, inner, fill=False, edgecolor=F.BLUE, lw=2.2))
    ax.add_patch(Circle(center, 0.21, facecolor="#fbbf24", edgecolor="#b45309", lw=1.4, zorder=4))
    ax.text(*center, "$M$", ha="center", va="center", fontsize=12, weight="bold")

    angle_a = np.deg2rad(15)
    angle_b = np.deg2rad(42)
    pa = center + inner * np.array([np.cos(angle_a), np.sin(angle_a)])
    pb = center + outer * np.array([np.cos(angle_b), np.sin(angle_b)])
    ax.plot([center[0], pa[0]], [center[1], pa[1]], color=F.BLUE, lw=1.3, ls=":")
    ax.plot([center[0], pb[0]], [center[1], pb[1]], color=F.PURPLE, lw=1.3, ls=":")
    ax.add_patch(Circle(pa, 0.10, facecolor=F.BLUE, edgecolor="white", lw=1.0, zorder=5))
    ax.add_patch(Circle(pb, 0.13, facecolor=F.PURPLE, edgecolor="white", lw=1.0, zorder=5))
    ax.text(*(pa + np.array([0.27, -0.18])), "A", color=F.BLUE, fontsize=13, weight="bold")
    ax.text(*(pb + np.array([0.16, 0.16])), "B", color=F.PURPLE, fontsize=13, weight="bold")
    ax.text(-3.92, -0.75, r"$a_A$", color=F.BLUE, fontsize=13)
    ax.text(-5.15, 1.62, r"$a_B=4a_A$", color=F.PURPLE, fontsize=13)
    ax.text(-3.25, -2.68, "兩軌道共用同一中央天體 $M$", fontsize=12, color=F.INK, ha="center")
    ax.text(-3.25, 2.46, "軌道 A、B 的比例常數相同", fontsize=13, ha="center")

    ax.add_patch(
        FancyBboxPatch(
            (0.05, -2.18),
            5.65,
            4.42,
            boxstyle="round,pad=0.18,rounding_size=0.18",
            facecolor="#f8fafc",
            edgecolor="#cbd5e1",
            lw=1.5,
        )
    )
    ax.text(2.88, 1.72, "同一中央天體", fontsize=15, ha="center", weight="bold")
    ax.text(
        2.88,
        0.92,
        r"$\frac{T_A^2}{a_A^3}=\frac{T_B^2}{a_B^3}$",
        ha="center",
        fontsize=16,
        color=F.BLUE,
    )
    ax.text(
        2.88,
        0.05,
        r"$\frac{T_B}{T_A}=\left(\frac{a_B}{a_A}\right)^{3/2}$",
        ha="center",
        fontsize=16,
        color=F.PURPLE,
    )
    ax.text(2.88, -0.73, r"$a_B=4a_A$", ha="center", fontsize=14.5, color=F.RED)
    ax.text(2.88, -1.33, r"$\Rightarrow\quad T_B/T_A=4^{3/2}=8$", ha="center", fontsize=13.5, color=F.RED)
    ax.plot([0.55, 5.20], [-1.68, -1.68], color="#e2e8f0", lw=1.0)
    ax.text(2.88, -1.96, "橢圓軌道用半長軸 $a$；圓軌道時 $a=r$", ha="center", fontsize=10.8)

    ax.set_xlim(-5.80, 5.90)
    ax.set_ylim(-2.90, 2.90)
    ax.set_title("克卜勒第三定律：先確認中央天體相同，再比較半長軸與週期", fontsize=15, pad=10)
    _save(fig, "選物I-5-克卜勒第三定律比較")


def fig_gravity_superposition_zero():
    """以向量合成與一維零場呈現重力場疊加。"""
    fig, ax = F.canvas(11.8, 5.0)
    ax.axis("off")
    ax.set_xlim(-6.0, 6.0)
    ax.set_ylim(-2.55, 2.65)

    # 左：等質量在對稱點的向量疊加
    point = np.array([-3.275, 1.15])
    source_distance = 2.20
    half_angle = np.deg2rad(30.0)
    horizontal_offset = source_distance * np.sin(half_angle)
    vertical_drop = source_distance * np.cos(half_angle)
    mass_a = point + np.array([-horizontal_offset, -vertical_drop])
    mass_b = point + np.array([horizontal_offset, -vertical_drop])
    vec_a = 0.98 * (mass_a - point) / np.linalg.norm(mass_a - point)
    vec_b = 0.98 * (mass_b - point) / np.linalg.norm(mass_b - point)
    vec_sum = vec_a + vec_b
    down = np.array([0.0, -1.0])
    angle_a = np.rad2deg(np.arccos(np.dot(vec_a / np.linalg.norm(vec_a), down)))
    angle_b = np.rad2deg(np.arccos(np.dot(vec_b / np.linalg.norm(vec_b), down)))
    assert np.isclose(angle_a, 30.0)
    assert np.isclose(angle_b, 30.0)
    assert np.isclose(vec_sum[0], 0.0)
    assert np.isclose(np.linalg.norm(vec_sum), 2 * np.linalg.norm(vec_a) * np.cos(half_angle))
    assert vec_sum[1] < 0
    ax.add_patch(Circle(mass_a, 0.30, facecolor="#fbbf24", edgecolor="#92400e", lw=1.5))
    ax.add_patch(Circle(mass_b, 0.30, facecolor="#fbbf24", edgecolor="#92400e", lw=1.5))
    ax.add_patch(Circle(point, 0.11, facecolor="#f8fafc", edgecolor=F.INK, lw=1.2))
    ax.plot([point[0], mass_a[0]], [point[1], mass_a[1]], color="#cbd5e1", lw=1.1, ls="--")
    ax.plot([point[0], mass_b[0]], [point[1], mass_b[1]], color="#cbd5e1", lw=1.1, ls="--")
    F.arrow(ax, point, point + vec_a, color=F.BLUE, lw=2.7)
    F.arrow(ax, point, point + vec_b, color=F.GREEN, lw=2.7)
    F.arrow(ax, point, point + vec_sum, color=F.RED, lw=3.0)
    F.angle_arc(ax, point, 0.48, -120, -90, color=F.PURPLE, text="$30^\\circ$")
    F.angle_arc(ax, point, 0.48, -90, -60, color=F.PURPLE, text="$30^\\circ$")
    ax.text(*(point + 0.58 * vec_a + np.array([-0.12, 0.06])), r"$\vec g_A$", color=F.BLUE, fontsize=12)
    ax.text(*(point + 0.58 * vec_b + np.array([0.07, 0.06])), r"$\vec g_B$", color=F.GREEN, fontsize=12)
    ax.text(*(point + 0.62 * vec_sum + np.array([0.10, 0])), r"$\vec g_{\rm net}$", color=F.RED, fontsize=12)
    ax.text(-3.275, 2.15, "對稱上方：水平分量消去", ha="center", fontsize=13, weight="bold")
    ax.text(-5.0, -1.63, "$M$", ha="center", fontsize=12)
    ax.text(-1.55, -1.63, "$M$", ha="center", fontsize=12)
    ax.text(-3.275, -2.12, r"$\vec g_{\rm net}=\vec g_A+\vec g_B$", ha="center", fontsize=13.5, color=F.PURPLE)

    # 右：4M 與 M 之間的零場點
    left = np.array([0.25, -0.68])
    right = np.array([5.25, -0.68])
    separation = right[0] - left[0]
    zero_x = left[0] + separation * 2 / 3  # 4M/x^2 = M/(d-x)^2
    zero = np.array([zero_x, -0.68])
    d_left = zero_x - left[0]
    d_right = right[0] - zero_x
    assert np.isclose(4 / d_left**2, 1 / d_right**2)
    assert d_right < d_left
    ax.plot([left[0], right[0]], [left[1], right[1]], color="#94a3b8", lw=1.5)
    ax.add_patch(Circle(left, 0.48, facecolor="#fb7185", edgecolor="#9f1239", lw=1.6))
    ax.add_patch(Circle(right, 0.27, facecolor="#93c5fd", edgecolor="#1d4ed8", lw=1.5))
    ax.add_patch(Circle(zero, 0.11, facecolor="white", edgecolor=F.INK, lw=1.3))
    F.arrow(ax, zero, zero + np.array([-0.86, 0]), color=F.RED, lw=2.8)
    F.arrow(ax, zero, zero + np.array([0.86, 0]), color=F.BLUE, lw=2.8)
    ax.text(left[0], -0.73, "$4M$", ha="center", va="center", fontsize=12.5, weight="bold")
    ax.text(right[0], -0.71, "$M$", ha="center", va="center", fontsize=11.5, weight="bold")
    ax.text(zero[0], -0.30, "$P_0$", ha="center", fontsize=12.5)
    ax.annotate("", xy=zero + np.array([0, -0.82]), xytext=left + np.array([0, -0.82]), arrowprops=dict(arrowstyle="<->", color=F.PURPLE, lw=1.5))
    ax.annotate("", xy=right + np.array([0, -0.82]), xytext=zero + np.array([0, -0.82]), arrowprops=dict(arrowstyle="<->", color=F.GREEN, lw=1.5))
    ax.text((left[0] + zero[0]) / 2, -1.78, "$x$", color=F.PURPLE, fontsize=12.5, ha="center")
    ax.text((zero[0] + right[0]) / 2, -1.78, "$d-x$", color=F.GREEN, fontsize=12.5, ha="center")
    ax.text(2.75, 2.15, "兩質量之間：零場點靠近較小質量", ha="center", fontsize=13, weight="bold")
    ax.text(2.75, 1.36, r"$G\dfrac{4M}{x^2}=G\dfrac{M}{(d-x)^2}$", ha="center", fontsize=14, color=F.PURPLE)
    ax.text(2.75, 0.78, r"$x=2(d-x)\Rightarrow x=2d/3$", ha="center", fontsize=13, color=F.INK)
    ax.text(2.75, -2.18, "場為 0 只表示該點的向量和為 0；兩個單獨場都不是 0。", ha="center", fontsize=11.3, color="#475569")
    ax.set_title("重力場遵守向量疊加：先畫每個來源的方向，再做分量合成", fontsize=15, pad=12)
    _save(fig, "選物I-5-重力場疊加與零場")


def _solve_kepler(mean_anomaly, eccentricity, iterations=18):
    """解 E-e sin E=M，用於等時間區間的橢圓位置。"""
    eccentric_anomaly = np.asarray(mean_anomaly, dtype=float).copy()
    for _ in range(iterations):
        eccentric_anomaly -= (
            eccentric_anomaly - eccentricity * np.sin(eccentric_anomaly) - mean_anomaly
        ) / (1 - eccentricity * np.cos(eccentric_anomaly))
    return eccentric_anomaly


def fig_kepler_ellipse_equal_area():
    """以實際橢圓與等平均近點角區間畫出等時等面積。"""
    a, eccentricity = 3.25, 0.45
    c = eccentricity * a
    b = a * np.sqrt(1 - eccentricity**2)
    # E-e sin E=M 的近心點在 E=0，因此焦點取在 +c。
    focus = np.array([c, 0.0])
    delta_mean = 0.68
    intervals_mean = [(-delta_mean / 2, delta_mean / 2), (np.pi - delta_mean / 2, np.pi + delta_mean / 2)]
    intervals_e = [tuple(_solve_kepler(np.array(pair), eccentricity)) for pair in intervals_mean]
    swept_areas = [0.5 * a * b * ((e2 - e1) - eccentricity * (np.sin(e2) - np.sin(e1))) for e1, e2 in intervals_e]
    assert np.isclose(swept_areas[0], swept_areas[1])
    assert np.isclose(c**2, a**2 - b**2)
    perihelion_distance = a - c
    aphelion_distance = a + c
    perihelion_speed = np.sqrt(2 / perihelion_distance - 1 / a)
    aphelion_speed = np.sqrt(2 / aphelion_distance - 1 / a)
    speed_ratio = perihelion_speed / aphelion_speed
    assert np.isclose(speed_ratio, (1 + eccentricity) / (1 - eccentricity))
    arrow_scale = 0.54 / aphelion_speed
    velocity_lengths = [arrow_scale * perihelion_speed, arrow_scale * aphelion_speed]
    assert np.isclose(velocity_lengths[0] / velocity_lengths[1], speed_ratio)

    fig, ax = F.canvas(11.4, 5.3)
    ax.axis("off")
    ax.set_aspect("equal")
    angle = np.linspace(0, 2 * np.pi, 800)
    orbit = np.column_stack([a * np.cos(angle), b * np.sin(angle)])
    ax.plot(orbit[:, 0], orbit[:, 1], color="#334155", lw=2.0)
    ax.add_patch(Circle(focus, 0.18, facecolor="#fbbf24", edgecolor="#b45309", lw=1.4, zorder=5))
    ax.add_patch(Circle(np.array([-c, 0.0]), 0.07, facecolor="white", edgecolor="#94a3b8", lw=1.0, zorder=4))
    ax.text(focus[0], -0.42, "太陽（焦點）", ha="center", fontsize=11.5)
    ax.text(-c, -0.32, "另一焦點", ha="center", fontsize=10.5, color="#64748b")

    colors = [(F.RED, "近日點區間"), (F.BLUE, "遠日點區間")]
    arc_lengths = []
    for (e1, e2), (color, label), velocity_length in zip(intervals_e, colors, velocity_lengths):
        es = np.linspace(e1, e2, 180)
        points = np.column_stack([a * np.cos(es), b * np.sin(es)])
        polygon = np.vstack([focus, points, focus])
        ax.add_patch(Polygon(polygon, closed=True, facecolor=color, edgecolor=color, alpha=0.22, lw=1.7))
        ax.plot(points[:, 0], points[:, 1], color=color, lw=3.0)
        mid = points[len(points) // 2]
        tangent = np.array([-a * np.sin((e1 + e2) / 2), b * np.cos((e1 + e2) / 2)])
        tangent /= np.linalg.norm(tangent)
        F.arrow(ax, mid, mid + velocity_length * tangent, color=color, lw=2.8)
        ax.text(*(mid + velocity_length * tangent + np.array([0, 0.22])), r"$\vec v$", color=color, fontsize=12, ha="center")
        ax.text(mid[0], mid[1] + (0.55 if mid[1] >= 0 else -0.62), label, color=color, fontsize=11.5, ha="center")
        arc_lengths.append(np.sum(np.linalg.norm(np.diff(points, axis=0), axis=1)))
    assert arc_lengths[0] > arc_lengths[1]

    ax.annotate("", xy=(a, -2.55), xytext=(-a, -2.55), arrowprops=dict(arrowstyle="<->", color=F.PURPLE, lw=1.5))
    ax.text(0, -2.45, "$2a$", color=F.PURPLE, fontsize=12.5, ha="center", va="bottom")
    ax.text(0, 2.98, r"$e=c/a=0.45$；兩色區域對應相同 $\Delta t$ 且 $\Delta A_1=\Delta A_2$", ha="center", fontsize=12.5, weight="bold")
    ax.text(0, -3.08, rf"箭長比依速率比繪製：$v_p/v_a=(1+e)/(1-e)={speed_ratio:.2f}$。", ha="center", fontsize=11.3, color="#475569")
    ax.set_xlim(-4.55, 4.55)
    ax.set_ylim(-3.34, 3.38)
    ax.set_title("克卜勒第一、二定律：太陽在焦點，相等時間掃過相等面積", fontsize=15, pad=12)
    _save(fig, "選物I-5-橢圓與等面積")


def fig_kepler_data_linearization():
    """以正規化軌道資料呈現 T² 對 a³ 的直線檢驗。"""
    semimajor = np.array([0.50, 0.80, 1.00, 1.40, 2.00])
    periods = semimajor ** 1.5
    x_values = semimajor**3
    y_values = periods**2
    slope, intercept = np.polyfit(x_values, y_values, 1)
    assert np.isclose(slope, 1.0)
    assert np.isclose(intercept, 0.0, atol=1e-12)

    fig, (ax_table, ax_plot) = plt.subplots(1, 2, figsize=(11.3, 4.8), gridspec_kw={"width_ratios": [0.92, 1.25]})
    fig.patch.set_facecolor("white")
    ax_table.axis("off")
    table_data = [[f"{a:.2f}", f"{t:.3f}", f"{a**3:.3f}", f"{t**2:.3f}"] for a, t in zip(semimajor, periods)]
    table = ax_table.table(cellText=table_data, colLabels=["$a/a_0$", "$T/T_0$", "$(a/a_0)^3$", "$(T/T_0)^2$"], loc="center", cellLoc="center")
    table.auto_set_font_size(False)
    table.set_fontsize(10.8)
    table.scale(1.08, 1.55)
    for (row, col), cell in table.get_celld().items():
        cell.set_edgecolor("#cbd5e1")
        if row == 0:
            cell.set_facecolor("#dbeafe")
            cell.set_text_props(weight="bold")
    ax_table.set_title("同一中央天體的正規化資料", fontsize=13.5, pad=8)
    ax_table.text(0.5, 0.06, r"表中每列均有 $(T/T_0)^2=(a/a_0)^3$", transform=ax_table.transAxes, ha="center", fontsize=11, color="#475569")

    ax_plot.scatter(x_values, y_values, s=72, color=F.RED, edgecolors="white", zorder=4)
    line_x = np.linspace(0, max(x_values) * 1.05, 300)
    ax_plot.plot(line_x, line_x, color=F.BLUE, lw=2.6)
    ax_plot.set_xlabel(r"$(a/a_0)^3$")
    ax_plot.set_ylabel(r"$(T/T_0)^2$")
    ax_plot.set_title(r"線性化檢驗：$T^2$ 對 $a^3$", fontsize=13.5)
    ax_plot.text(0.55, 7.35, "斜率 = 1.000\n截距 = 0.000", fontsize=11.5, color=F.PURPLE)
    ax_plot.set_xlim(0, 8.5)
    ax_plot.set_ylim(0, 8.5)
    F.clean_grid(ax_plot)
    fig.suptitle("克卜勒第三定律的資料檢驗：把冪次關係改畫成直線", fontsize=15.3, y=0.98)
    fig.subplots_adjust(left=0.05, right=0.98, top=0.82, bottom=0.16, wspace=0.24)
    _save(fig, "選物I-5-克卜勒資料線性化")


def _solution_panel(ax, title, xlim, ylim):
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_title(title, fontsize=12.8, pad=8, weight="bold")


def fig_solution_scaling_basics():
    """章末 Q1--Q3、Q9：用幾何尺度先建立比例式。"""
    fig, axes = plt.subplots(2, 2, figsize=(11.4, 7.6))
    fig.patch.set_facecolor("white")

    ax = axes[0, 0]
    _solution_panel(ax, "A｜Q1：質量一次、距離平方", (-3.1, 3.1), (-1.55, 1.80))
    left = np.array([-2.55, 0.68])
    near = np.array([-1.55, 0.68])
    far = np.array([2.45, -0.55])
    source_far = np.array([-2.55, -0.55])
    assert np.isclose(np.linalg.norm(far - source_far), 5 * np.linalg.norm(near - left))
    for p, radius, label, color in [
        (left, 0.26, "$M$", F.BLUE), (near, 0.16, "$m$", F.GREEN),
        (source_far, 0.34, "$3M$", F.BLUE), (far, 0.16, "$m$", F.GREEN),
    ]:
        ax.add_patch(Circle(p, radius, facecolor=color, edgecolor="white", lw=0.9))
        ax.text(*p, label, ha="center", va="center", fontsize=10.5, color="white", weight="bold")
    ax.plot([left[0], near[0]], [left[1], near[1]], color="#94a3b8", lw=1.4)
    ax.plot([source_far[0], far[0]], [source_far[1], far[1]], color="#94a3b8", lw=1.4)
    ax.text(-2.05, 1.10, "$r$", ha="center", fontsize=11.5, color=F.PURPLE)
    ax.text(-0.05, -0.98, "$5r$", ha="center", fontsize=11.5, color=F.PURPLE)
    ax.text(0, 1.52, r"$F\propto Mm/r^2$", ha="center", fontsize=13.5)
    ax.text(0, 0.10, r"$F'/F=3/5^2=3/25$", ha="center", fontsize=14, color=F.RED)

    ax = axes[0, 1]
    _solution_panel(ax, "B｜Q2：表面距離就是半徑", (-3.1, 3.1), (-1.55, 1.80))
    earth = np.array([-1.65, -0.42])
    planet = np.array([1.15, -0.42])
    re = 0.48
    rp = 2 * re
    ax.add_patch(Circle(earth, re, facecolor="#dbeafe", edgecolor=F.BLUE, lw=1.5))
    ax.add_patch(Circle(planet, rp, facecolor="#fee2e2", edgecolor=F.RED, lw=1.6))
    ax.text(*earth, "$M_E,R_E$", ha="center", va="center", fontsize=10.3)
    ax.text(*planet, "$4M_E,2R_E$", ha="center", va="center", fontsize=11)
    for center, radius in [(earth, re), (planet, rp)]:
        top = center + np.array([0.0, radius])
        F.arrow(ax, top + np.array([0.0, 0.16]), top + np.array([0.0, -0.45]), color=F.PURPLE, lw=2.2)
    ax.text(0, 1.40, r"$g'/g_E=4/(2^2)=1$", ha="center", fontsize=14, color=F.RED)
    ax.text(0, 0.92, r"$g=GM/R^2$", ha="center", fontsize=12.8, color=F.PURPLE)

    ax = axes[1, 0]
    _solution_panel(ax, "C｜Q3：同密度球體的半徑倍率", (-3.1, 3.1), (-1.65, 1.75))
    small = np.array([-1.70, -0.55])
    large = np.array([1.05, -0.55])
    r_small = 0.34
    r_large = 3 * r_small
    ax.add_patch(Circle(small, r_small, facecolor="#dbeafe", edgecolor=F.BLUE, lw=1.4))
    ax.add_patch(Circle(large, r_large, facecolor="#dcfce7", edgecolor=F.GREEN, lw=1.6))
    ax.text(*small, "$R$", ha="center", va="center", fontsize=10.5)
    ax.text(*large, "$3R$", ha="center", va="center", fontsize=12)
    ax.text(0, 1.48, r"同密度：$M\propto R^3$", ha="center", fontsize=13.2)
    ax.text(0, 1.00, r"$M_{3R}/M_R=3^3=27$", ha="center", fontsize=13.2, color=F.RED)
    ax.text(0, 0.57, r"$g\propto M/R^2\propto R$，故 $g_{3R}/g_R=3$", ha="center", fontsize=11.7, color=F.PURPLE)

    ax = axes[1, 1]
    _solution_panel(ax, "D｜Q9：$M,R$ 同倍率時 $GM/R$ 不變", (-3.1, 3.1), (-1.65, 1.75))
    body1 = np.array([-1.62, -0.65])
    body2 = np.array([1.10, -0.65])
    r1 = 0.46
    r2 = 2 * r1
    ax.add_patch(Circle(body1, r1, facecolor="#dbeafe", edgecolor=F.BLUE, lw=1.5))
    ax.add_patch(Circle(body2, r2, facecolor="#ede9fe", edgecolor=F.PURPLE, lw=1.6))
    ax.text(*body1, "$M,R$", ha="center", va="center", fontsize=11)
    ax.text(*body2, "$2M,2R$", ha="center", va="center", fontsize=12)
    for center, radius, color in [(body1, r1, F.BLUE), (body2, r2, F.PURPLE)]:
        surface = center + np.array([0.0, radius])
        F.arrow(ax, surface, surface + np.array([0.62, 0.0]), color=color, lw=2.3)
    ax.text(0, 1.48, r"$GM'/R'=G(2M)/(2R)=GM/R$", ha="center", fontsize=12.8, color=F.RED)
    ax.text(0, 1.02, r"$v_\mathrm{orb}=\sqrt{GM/R}$，$v_\mathrm{esc}=\sqrt{2GM/R}$", ha="center", fontsize=11.8)
    ax.text(0, 0.58, r"兩天體的兩種速率相同，且 $v_\mathrm{esc}/v_\mathrm{orb}=\sqrt{2}$", ha="center", fontsize=11.2, color=F.PURPLE)

    fig.suptitle("章末比例題解題圖：先把質量與幾何尺度畫成正確倍率", fontsize=15.2, y=0.985)
    fig.subplots_adjust(left=0.035, right=0.98, top=0.89, bottom=0.05, wspace=0.14, hspace=0.28)
    _save(fig, "選物I-5-解題-基本比例")


def fig_solution_height_orbits():
    """章末 Q4–Q7：高度、圓軌道比例與由軌道反推質量。"""
    fig, axes = plt.subplots(2, 2, figsize=(11.4, 7.6))
    fig.patch.set_facecolor("white")

    # A：h=2R -> r=3R -> g/g_s=1/9
    ax = axes[0, 0]
    _solution_panel(ax, "A｜Q4：高度先轉成中心距離", (-2.45, 2.45), (-1.25, 2.85))
    center = np.array([-0.95, -0.42])
    radius = 0.62
    satellite = center + np.array([0.0, 3 * radius])
    ax.add_patch(Circle(center, radius, facecolor="#dbeafe", edgecolor=F.BLUE, lw=1.8))
    ax.add_patch(Circle(satellite, 0.10, facecolor="#f59e0b", edgecolor="#92400e", lw=1.1))
    ax.plot([center[0], satellite[0]], [center[1], satellite[1]], color="#94a3b8", lw=1.2, ls="--")
    surface = center + np.array([0.0, radius])
    ax.annotate("", xy=surface + np.array([-0.34, 0]), xytext=center + np.array([-0.34, 0]), arrowprops=dict(arrowstyle="<->", color=F.BLUE, lw=1.5))
    ax.annotate("", xy=satellite + np.array([0.34, 0]), xytext=surface + np.array([0.34, 0]), arrowprops=dict(arrowstyle="<->", color=F.GREEN, lw=1.5))
    ax.text(-1.48, -0.10, "$R$", color=F.BLUE, fontsize=12)
    ax.text(-0.47, 0.82, "$h=2R$", color=F.GREEN, fontsize=12)
    ax.text(1.05, 1.15, "$r=R+h=3R$", fontsize=13, color=F.PURPLE, ha="center")
    ax.text(1.05, 0.32, r"$\dfrac{g}{g_s}=\left(\dfrac{R}{3R}\right)^2=\dfrac{1}{9}$", fontsize=14, color=F.RED, ha="center")

    # B：h=R -> r=2R 與圓軌道速率
    ax = axes[0, 1]
    _solution_panel(ax, "B｜Q5：切向速度與徑向重力", (-2.45, 2.45), (-1.25, 2.85))
    center = np.array([-0.95, 0.15])
    radius = 0.62
    orbit_radius = 2 * radius
    satellite = center + np.array([0.0, orbit_radius])
    theta = np.linspace(0, 2 * np.pi, 300)
    ax.add_patch(Circle(center, radius, facecolor="#dbeafe", edgecolor=F.BLUE, lw=1.8))
    ax.plot(center[0] + orbit_radius * np.cos(theta), center[1] + orbit_radius * np.sin(theta), color="#94a3b8", lw=1.2, ls="--")
    ax.add_patch(Circle(satellite, 0.10, facecolor="#f59e0b", edgecolor="#92400e", lw=1.1))
    ax.plot([center[0], satellite[0]], [center[1], satellite[1]], color=F.PURPLE, lw=1.2, ls=":")
    F.arrow(ax, satellite, satellite + np.array([0.88, 0.0]), color=F.GREEN, lw=2.4)
    F.arrow(ax, satellite, satellite + np.array([0.0, -0.62]), color=F.RED, lw=2.4)
    ax.text(-0.60, 0.78, "$r=2R$", color=F.PURPLE, fontsize=12)
    ax.text(0.18, 1.57, r"$\vec v$", color=F.GREEN, fontsize=12)
    ax.text(-1.55, 1.23, r"$\vec g$", color=F.RED, fontsize=12)
    ax.text(1.25, 0.38, r"$v^2=\dfrac{GM}{2R}$", fontsize=13.2, ha="center")
    ax.text(1.25, -0.34, r"$GM=g_0R^2$", fontsize=12.6, ha="center", color=F.BLUE)
    ax.text(1.25, -0.92, r"$v=\sqrt{g_0R/2}$", fontsize=14, ha="center", color=F.RED)

    # C：r 真實依 1:9 當作徑向刻度
    ax = axes[1, 0]
    _solution_panel(ax, "C｜Q6：同一中央天體的倍率", (-2.65, 2.65), (-1.48, 1.70))
    source = np.array([-2.15, -0.10])
    unit_radius = 0.38
    inner = source + np.array([unit_radius, 0.0])
    outer = source + np.array([9 * unit_radius, 0.0])
    ax.add_patch(Circle(source, 0.18, facecolor="#fbbf24", edgecolor="#92400e", lw=1.2))
    ax.plot([source[0], outer[0]], [source[1], outer[1]], color="#94a3b8", lw=1.4)
    for point, color in [(inner, F.BLUE), (outer, F.PURPLE)]:
        ax.add_patch(Circle(point, 0.09, facecolor=color, edgecolor="white", lw=0.8, zorder=4))
    F.arrow(ax, inner, inner + np.array([0.0, 0.86]), color=F.BLUE, lw=2.3)
    F.arrow(ax, outer, outer + np.array([0.0, 0.86 / 3]), color=F.PURPLE, lw=2.3)
    ax.text(source[0] + unit_radius / 2, -0.50, "$r_A$", ha="center", color=F.BLUE, fontsize=11.5)
    ax.text((source[0] + outer[0]) / 2, -0.88, "$r_B=9r_A$", ha="center", color=F.PURPLE, fontsize=12)
    ax.text(inner[0] - 0.18, 1.02, "$v_A$", color=F.BLUE, fontsize=11.5)
    ax.text(outer[0] + 0.14, 0.42, "$v_B=v_A/3$", color=F.PURPLE, fontsize=11.5)
    ax.text(0.15, 1.33, "$T_B/T_A=27$", fontsize=13.2, color=F.RED, ha="center")
    ax.text(0.15, 0.87, "$a_B/a_A=1/81$", fontsize=12.6, color=F.GREEN, ha="center")

    # D：r,T -> M
    ax = axes[1, 1]
    _solution_panel(ax, "D｜Q7：軌道資料反推中央質量", (-2.45, 2.45), (-1.48, 1.70))
    source = np.array([-1.15, -0.02])
    orbit_radius = 1.10
    phase = np.deg2rad(35)
    radial = np.array([np.cos(phase), np.sin(phase)])
    tangent = np.array([-np.sin(phase), np.cos(phase)])
    sat = source + orbit_radius * radial
    theta = np.linspace(0, 2 * np.pi, 300)
    ax.plot(source[0] + orbit_radius * np.cos(theta), source[1] + orbit_radius * np.sin(theta), color="#94a3b8", lw=1.2, ls="--")
    ax.add_patch(Circle(source, 0.22, facecolor="#fbbf24", edgecolor="#92400e", lw=1.2))
    ax.add_patch(Circle(sat, 0.09, facecolor=F.BLUE, edgecolor="white", lw=0.8))
    ax.plot([source[0], sat[0]], [source[1], sat[1]], color=F.PURPLE, lw=1.2, ls=":")
    F.arrow(ax, sat, sat - 0.56 * radial, color=F.RED, lw=2.2)
    F.arrow(ax, sat, sat + 0.58 * tangent, color=F.GREEN, lw=2.2)
    ax.text(-0.55, 0.34, "$r$", color=F.PURPLE, fontsize=12)
    ax.text(-1.15, -1.38, "追蹤得到 $r,T$", ha="center", fontsize=11.5)
    ax.text(1.30, 0.74, r"$G\dfrac{Mm}{r^2}=m\dfrac{4\pi^2r}{T^2}$", ha="center", fontsize=12.7)
    ax.text(1.30, -0.08, r"$M=\dfrac{4\pi^2r^3}{GT^2}$", ha="center", fontsize=14, color=F.RED)
    ax.text(1.30, -0.70, "衛星質量 $m$ 消去", ha="center", fontsize=11.5, color=F.BLUE)

    fig.suptitle("章末解題圖：圖中的中心距離、速度與力直接決定列式", fontsize=15.2, y=0.985)
    fig.subplots_adjust(left=0.04, right=0.98, top=0.90, bottom=0.05, wspace=0.14, hspace=0.28)
    _save(fig, "選物I-5-解題-高度與軌道")


def fig_solution_concepts_superposition():
    """章末 Q8、Q10、Q11：失重、地球靜止與重力場疊加。"""
    fig, axes = plt.subplots(1, 3, figsize=(11.8, 4.6))
    fig.patch.set_facecolor("white")

    # E：失重與地球靜止的兩個必要圖像
    ax = axes[0]
    _solution_panel(ax, "E｜Q8：受力與軌道幾何", (-2.15, 2.15), (-1.85, 1.85))
    cabin = np.array([-1.10, 0.52])
    ax.add_patch(FancyBboxPatch((cabin[0] - 0.55, cabin[1] - 0.32), 1.10, 0.64, boxstyle="round,pad=0.08", facecolor="#f8fafc", edgecolor=F.BLUE, lw=1.3))
    ax.add_patch(Circle(cabin + np.array([-0.18, 0.02]), 0.09, facecolor="#f59e0b", edgecolor="#92400e", lw=0.8))
    F.arrow(ax, cabin + np.array([-0.30, -0.05]), cabin + np.array([-0.30, -0.92]), color=F.RED, lw=2.1)
    F.arrow(ax, cabin + np.array([0.30, -0.05]), cabin + np.array([0.30, -0.92]), color=F.RED, lw=2.1)
    ax.text(-1.10, -0.62, r"$\vec g$：人與艙體同時自由落下", ha="center", fontsize=9.8, color=F.RED)
    ax.text(-1.10, -1.02, r"$N\approx0$", ha="center", fontsize=11.5, color=F.PURPLE)

    earth = np.array([1.03, -0.18])
    earth_r = 0.55
    ax.add_patch(Circle(earth, earth_r, facecolor="#dbeafe", edgecolor=F.BLUE, lw=1.3))
    ax.plot([earth[0] - earth_r, earth[0] + earth_r], [earth[1], earth[1]], color=F.GREEN, lw=1.2)
    sat = earth + np.array([0.0, 1.15])
    ax.add_patch(Circle(sat, 0.08, facecolor=F.PURPLE, edgecolor="white", lw=0.8))
    F.arrow(ax, sat + np.array([-0.38, 0]), sat + np.array([0.38, 0]), color=F.GREEN, lw=2.0)
    ax.text(1.03, 1.38, r"$T=T_{\rm rot}$，同向", ha="center", fontsize=10.3, color=F.GREEN)
    ax.text(1.03, -0.96, "赤道面上的固定經度", ha="center", fontsize=9.5)

    # F：兩等長向量夾 120 度，真正合向量等長
    ax = axes[1]
    _solution_panel(ax, "F｜Q10：$120^\\circ$ 向量疊加", (-1.75, 1.75), (-1.58, 1.85))
    origin = np.array([0.0, -0.72])
    g1 = np.array([np.cos(np.deg2rad(150)), np.sin(np.deg2rad(150))])
    g2 = np.array([np.cos(np.deg2rad(30)), np.sin(np.deg2rad(30))])
    gsum = g1 + g2
    assert np.isclose(np.rad2deg(np.arccos(np.dot(g1, g2))), 120.0)
    assert np.isclose(np.linalg.norm(gsum), 1.0)
    F.arrow(ax, origin, origin + 1.28 * g1, color=F.BLUE, lw=2.7)
    F.arrow(ax, origin, origin + 1.28 * g2, color=F.GREEN, lw=2.7)
    F.arrow(ax, origin, origin + 1.28 * gsum, color=F.RED, lw=3.0)
    F.angle_arc(ax, origin, 0.58, 30, 150, color=F.PURPLE, text="$120^\\circ$")
    ax.text(-1.15, 0.08, r"$\vec g_1$", color=F.BLUE, fontsize=12)
    ax.text(1.12, 0.08, r"$\vec g_2$", color=F.GREEN, fontsize=12)
    ax.text(0.13, 0.90, r"$\vec g_{\rm net}$", color=F.RED, fontsize=12)
    ax.text(0, -1.35, r"$|\vec g_1|=|\vec g_2|=|\vec g_{\rm net}|=g_0$", ha="center", fontsize=10.5)

    # G：9M/M 的零場點
    ax = axes[2]
    _solution_panel(ax, "G｜Q11：零場點的方向與距離", (-2.0, 2.0), (-1.58, 1.85))
    left = np.array([-1.55, -0.25])
    right = np.array([1.55, -0.25])
    zero = left + 0.75 * (right - left)
    ax.plot([left[0], right[0]], [left[1], right[1]], color="#94a3b8", lw=1.4)
    ax.add_patch(Circle(left, 0.36, facecolor="#fb7185", edgecolor="#9f1239", lw=1.3))
    ax.add_patch(Circle(right, 0.20, facecolor="#93c5fd", edgecolor="#1d4ed8", lw=1.2))
    ax.add_patch(Circle(zero, 0.08, facecolor="white", edgecolor=F.INK, lw=1.1))
    F.arrow(ax, zero, zero + np.array([-0.56, 0.0]), color=F.RED, lw=2.4)
    F.arrow(ax, zero, zero + np.array([0.56, 0.0]), color=F.BLUE, lw=2.4)
    ax.text(left[0], -0.28, "$9M$", ha="center", fontsize=11.5, weight="bold")
    ax.text(right[0], -0.27, "$M$", ha="center", fontsize=10.5, weight="bold")
    ax.text(zero[0], 0.10, "$P_0$", ha="center", fontsize=11)
    ax.annotate("", xy=zero + np.array([0, -0.72]), xytext=left + np.array([0, -0.72]), arrowprops=dict(arrowstyle="<->", color=F.PURPLE, lw=1.3))
    ax.annotate("", xy=right + np.array([0, -0.72]), xytext=zero + np.array([0, -0.72]), arrowprops=dict(arrowstyle="<->", color=F.GREEN, lw=1.3))
    ax.text((left[0] + zero[0]) / 2, -1.18, "$3d/4$", ha="center", color=F.PURPLE, fontsize=11)
    ax.text((zero[0] + right[0]) / 2, -1.18, "$d/4$", ha="center", color=F.GREEN, fontsize=11)
    ax.text(0, 1.12, r"$G\dfrac{9M}{(3d/4)^2}=G\dfrac{M}{(d/4)^2}$", ha="center", fontsize=11.2)

    fig.suptitle("章末解題圖：受力、軌道條件與場向量先決定算式", fontsize=15.1, y=0.98)
    fig.subplots_adjust(left=0.025, right=0.99, top=0.85, bottom=0.08, wspace=0.12)
    _save(fig, "選物I-5-解題-概念與疊加")


def fig_solution_source_test_mass():
    """整合題 1：源質量、試驗質量與自由落下的質量消去。"""
    fig, axes = plt.subplots(1, 2, figsize=(11.3, 4.4))
    fig.patch.set_facecolor("white")

    ax = axes[0]
    _solution_panel(ax, "H1｜源質量建立場，試驗質量取樣", (-2.45, 2.45), (-1.65, 1.75))
    source = np.array([-1.30, -0.12])
    point = np.array([1.02, 0.82])
    direction = (source - point) / np.linalg.norm(source - point)
    ax.add_patch(Circle(source, 0.55, facecolor="#fbbf24", edgecolor="#92400e", lw=1.5))
    ax.text(*source, "源質量\n$M$", ha="center", va="center", fontsize=12, weight="bold")
    ax.add_patch(Circle(point, 0.10, facecolor="#f8fafc", edgecolor=F.INK, lw=1.1))
    ax.plot([source[0], point[0]], [source[1], point[1]], color="#94a3b8", lw=1.2, ls="--")
    F.arrow(ax, point, point + 0.78 * direction, color=F.RED, lw=2.6)
    ax.text(1.02, 1.25, "很小的試驗質量 $m_t$", ha="center", fontsize=11)
    ax.text(0.25, 0.22, r"$\vec F_g$", color=F.RED, fontsize=12)
    ax.text(0, -1.03, r"$\vec g=\vec F_g/m_t$", ha="center", fontsize=14, color=F.PURPLE)
    ax.text(0, -1.45, "$m_t$ 只用來取樣，足夠小才不改變源配置", ha="center", fontsize=10.1)

    ax = axes[1]
    _solution_panel(ax, "H2｜整合 1：$4M_E$、$2R_E$ 的表面", (-2.45, 2.45), (-1.65, 1.75))
    earth = np.array([-1.46, -0.34])
    planet = np.array([0.78, -0.34])
    earth_r = 0.42
    planet_r = 0.84
    ax.add_patch(Circle(earth, earth_r, facecolor="#dbeafe", edgecolor=F.BLUE, lw=1.4))
    ax.add_patch(Circle(planet, planet_r, facecolor="#fee2e2", edgecolor=F.RED, lw=1.5))
    ax.text(*earth, "$M_E,R_E$", ha="center", va="center", fontsize=10.5)
    ax.text(*planet, "$4M_E,2R_E$", ha="center", va="center", fontsize=11)
    test_earth = earth + np.array([0.0, earth_r + 0.16])
    test_planet = planet + np.array([0.0, planet_r + 0.16])
    for point, length in [(test_earth, 0.46), (test_planet, 0.46)]:
        ax.add_patch(Circle(point, 0.07, facecolor="#f59e0b", edgecolor="#92400e", lw=0.8))
        F.arrow(ax, point, point + np.array([0.0, -length]), color=F.PURPLE, lw=2.2)
    ax.text(-0.35, 1.35, r"$g'/g_E=4/2^2=1$", ha="center", fontsize=13.5, color=F.RED)
    ax.text(-0.35, 0.88, r"$G\dfrac{Mm}{R^2}=ma$", ha="center", fontsize=12.7)
    ax.text(-0.35, 0.46, r"$a=GM/R^2$", ha="center", fontsize=13.2, color=F.PURPLE)
    ax.text(-0.35, -1.48, "兩個試驗物的質量 $m$ 都在運動方程中消去", ha="center", fontsize=10.3)

    fig.suptitle("整合題 1 解題圖：區分「產生場」與「在場中受力」的角色", fontsize=15.1, y=0.98)
    fig.subplots_adjust(left=0.035, right=0.98, top=0.84, bottom=0.08, wspace=0.16)
    _save(fig, "選物I-5-解題-源與試驗質量")


def fig_solution_kepler_integration():
    """整合題 4：同一太陽、半長軸倍率、焦點與等面積。"""
    fig, axes = plt.subplots(1, 2, figsize=(11.4, 4.8))
    fig.patch.set_facecolor("white")

    ax = axes[0]
    _solution_panel(ax, "I｜第三定律：同一太陽才共用常數", (-3.1, 3.1), (-2.15, 2.15))
    focus = np.array([-1.72, 0.0])
    eccentricity = 0.30
    semimajor_axes = [0.55, 2.20]
    colors = [F.BLUE, F.PURPLE]
    labels = [r"$a_E,\ T_E$", r"$4a_E,\ 8T_E$"]
    theta = np.linspace(0, 2 * np.pi, 500)
    for a, color, label in zip(semimajor_axes, colors, labels):
        c = eccentricity * a
        b = a * np.sqrt(1 - eccentricity**2)
        center = focus + np.array([c, 0.0])
        ax.plot(center[0] + a * np.cos(theta), b * np.sin(theta), color=color, lw=2.0)
        ax.text(center[0] + 0.18, b + 0.17, label, color=color, ha="center", fontsize=11.5)
    ax.add_patch(Circle(focus, 0.12, facecolor="#fbbf24", edgecolor="#92400e", lw=1.1, zorder=5))
    ax.text(focus[0], -0.34, "太陽（共同焦點）", ha="center", fontsize=10.5)
    ax.text(0.35, -1.78, r"$T'/T_E=(a'/a_E)^{3/2}=4^{3/2}=8$", ha="center", fontsize=12.6, color=F.RED)

    ax = axes[1]
    _solution_panel(ax, "J｜第一、二定律：焦點與等時等面積", (-3.1, 3.1), (-2.15, 2.15))
    a = 2.05
    eccentricity = 0.45
    c = eccentricity * a
    b = a * np.sqrt(1 - eccentricity**2)
    focus = np.array([c, 0.0])
    orbit = np.column_stack([a * np.cos(theta), b * np.sin(theta)])
    ax.plot(orbit[:, 0], orbit[:, 1], color="#334155", lw=1.8)
    ax.add_patch(Circle(focus, 0.12, facecolor="#fbbf24", edgecolor="#92400e", lw=1.1, zorder=5))
    delta_mean = 0.60
    intervals_mean = [(-delta_mean / 2, delta_mean / 2), (np.pi - delta_mean / 2, np.pi + delta_mean / 2)]
    intervals_e = [tuple(_solve_kepler(np.array(pair), eccentricity)) for pair in intervals_mean]
    areas = []
    for (e1, e2), color in zip(intervals_e, [F.RED, F.BLUE]):
        es = np.linspace(e1, e2, 120)
        points = np.column_stack([a * np.cos(es), b * np.sin(es)])
        ax.add_patch(Polygon(np.vstack([focus, points, focus]), closed=True, facecolor=color, edgecolor=color, alpha=0.22, lw=1.3))
        areas.append(0.5 * a * b * ((e2 - e1) - eccentricity * (np.sin(e2) - np.sin(e1))))
    assert np.isclose(areas[0], areas[1])
    vp_over_va = (1 + eccentricity) / (1 - eccentricity)
    far_arrow = 0.42
    near_arrow = far_arrow * vp_over_va
    peri = np.array([a, 0.0])
    apo = np.array([-a, 0.0])
    F.arrow(ax, peri, peri + np.array([0.0, near_arrow]), color=F.RED, lw=2.5)
    F.arrow(ax, apo, apo + np.array([0.0, -far_arrow]), color=F.BLUE, lw=2.5)
    ax.text(peri[0] + 0.22, near_arrow / 2, "$v_p$", color=F.RED, fontsize=11.5)
    ax.text(apo[0] - 0.24, -far_arrow / 2, "$v_a$", color=F.BLUE, fontsize=11.5, ha="right")
    ax.text(focus[0], -0.30, "太陽（焦點）", ha="center", fontsize=10.2)
    ax.text(0, 1.78, r"$\Delta A_p=\Delta A_a$ （相同 $\Delta t$）", ha="center", fontsize=11.7)
    ax.text(0, -1.86, rf"$v_p/v_a=(1+e)/(1-e)={vp_over_va:.2f}>1$", ha="center", fontsize=11.7, color=F.PURPLE)

    fig.suptitle("整合題 4 解題圖：三條克卜勒資料規律在同一圖像中連起來", fontsize=15.0, y=0.98)
    fig.subplots_adjust(left=0.035, right=0.98, top=0.84, bottom=0.08, wspace=0.16)
    _save(fig, "選物I-5-解題-克卜勒整合")


if __name__ == "__main__":
    fig_center_distance()
    fig_inverse_square_scaling()
    fig_gravity_orbit_chain()
    fig_kepler_third_comparison()
    fig_gravity_superposition_zero()
    fig_kepler_ellipse_equal_area()
    fig_kepler_data_linearization()
    fig_solution_scaling_basics()
    fig_solution_height_orbits()
    fig_solution_concepts_superposition()
    fig_solution_source_test_mass()
    fig_solution_kepler_integration()
    print("done.")
