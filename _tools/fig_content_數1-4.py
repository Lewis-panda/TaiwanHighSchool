# -*- coding: utf-8 -*-
"""重生「數1-4 直線與圓」學生講義的章內 SVG。"""

if __name__ == "__main__" and __import__("sys").argv[1:]:
    raise SystemExit("本腳本不接受參數；直接執行即可重生數1-4 章內 SVG。")

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, Polygon

import figlib as F


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHAPTER = os.path.join(ROOT, "content", "必修數學", "數1-4")

FIGURE_OUTPUTS = (
    ("fig_slope_triangle", "數1-4-斜率三角形.svg"),
    ("fig_parallel_perpendicular", "數1-4-平行與垂直.svg"),
    ("fig_linear_systems", "數1-4-聯立方程幾何.svg"),
    ("fig_point_line_distance", "數1-4-點線距離.svg"),
    ("fig_half_planes", "數1-4-半平面.svg"),
    ("fig_circle_equation", "數1-4-圓方程式.svg"),
    ("fig_circle_line_positions", "數1-4-圓與直線位置.svg"),
    ("fig_circle_tangents", "數1-4-圓的切線.svg"),
)


def _save(fig, filename):
    stem, extension = os.path.splitext(filename)
    if extension != ".svg" or not stem.startswith("數1-4-"):
        raise AssertionError("輸出檔名必須是數1-4 章內 SVG")
    return F.save_to(fig, CHAPTER, stem, output_subdir="assets", write_pdf=False)


def fig_slope_triangle():
    a = np.array([-2.0, -1.0])
    b = np.array([4.0, 3.0])
    dx, dy = b - a
    slope = dy / dx
    assert np.isclose(slope, 2 / 3)

    fig, ax = plt.subplots(figsize=(8.6, 5.5))
    x = np.linspace(-3, 5, 100)
    ax.plot(x, slope * (x - a[0]) + a[1], color=F.BLUE, lw=2.8)
    ax.scatter([a[0], b[0]], [a[1], b[1]], color=[F.AMBER, F.GREEN], s=80, zorder=5)
    ax.plot([a[0], b[0]], [a[1], a[1]], color=F.GREEN, lw=2)
    ax.plot([b[0], b[0]], [a[1], b[1]], color=F.AMBER, lw=2)
    ax.text(1, -1.45, r"$\Delta x=6$", ha="center", color=F.GREEN, fontsize=12)
    ax.text(4.25, 1, r"$\Delta y=4$", va="center", color=F.AMBER, fontsize=12)
    ax.annotate(r"$m=\dfrac{\Delta y}{\Delta x}=\dfrac{2}{3}$", xy=(1.6, 1.4),
                xytext=(-2.6, 3.7), arrowprops=dict(arrowstyle="->", color=F.BLUE, lw=1.5),
                color=F.BLUE, fontsize=13)
    ax.axhline(0, color=F.INK, lw=1)
    ax.axvline(0, color=F.INK, lw=1)
    ax.set_xlim(-3, 5)
    ax.set_ylim(-2, 4.6)
    ax.set_aspect("equal", adjustable="box")
    ax.set_title("斜率是同一直線上固定的鉛直變化／水平變化", fontsize=15)
    F.clean_grid(ax)
    fig.tight_layout()
    return _save(fig, "數1-4-斜率三角形.svg")


def fig_parallel_perpendicular():
    x = np.linspace(-4, 4, 300)
    m = 0.75
    perpendicular = -1 / m
    assert np.isclose(m * perpendicular, -1)

    fig, axes = plt.subplots(1, 2, figsize=(10.8, 4.7))
    axes[0].plot(x, m * x + 2, color=F.BLUE, lw=2.6, label=r"$m_1=3/4$")
    axes[0].plot(x, m * x - 1, color=F.GREEN, lw=2.6, label=r"$m_2=3/4$")
    axes[0].set_title("平行：斜率相等", fontsize=13)
    axes[0].legend(frameon=False)

    axes[1].plot(x, m * x, color=F.BLUE, lw=2.6, label=r"$m_1=3/4$")
    axes[1].plot(x, perpendicular * x, color=F.AMBER, lw=2.6, label=r"$m_2=-4/3$")
    axes[1].scatter([0], [0], color=F.INK, s=45, zorder=5)
    axes[1].set_title(r"垂直：$m_1m_2=-1$", fontsize=13)
    axes[1].legend(frameon=False)

    for ax in axes:
        ax.axhline(0, color=F.INK, lw=1)
        ax.axvline(0, color=F.INK, lw=1)
        ax.set_xlim(-4, 4)
        ax.set_ylim(-5, 5)
        ax.set_aspect("equal", adjustable="box")
        F.clean_grid(ax)
    fig.suptitle("用斜率判斷兩條非鉛垂線的方向關係", fontsize=15)
    fig.tight_layout(rect=(0, 0, 1, 0.91))
    return _save(fig, "數1-4-平行與垂直.svg")


def fig_linear_systems():
    x = np.linspace(-3, 5, 200)
    panels = (
        ((2 * x - 3, -3 * x + 7), "一個交點\n一組解"),
        ((2 * x - 3, 2 * x + 1), "平行\n無解"),
        ((2 * x - 3, 2 * x - 3), "重合\n無限多組解"),
    )
    fig, axes = plt.subplots(1, 3, figsize=(11.2, 4.2), sharex=True, sharey=True)
    for index, (ax, (ys, title)) in enumerate(zip(axes, panels)):
        ax.plot(x, ys[0], color=F.BLUE, lw=2.4)
        ax.plot(x, ys[1], color=F.GREEN, lw=2.4, ls="--" if index == 2 else "-")
        if index == 0:
            solution = (2.0, 1.0)
            assert np.isclose(2 * solution[0] - 3, solution[1])
            assert np.isclose(-3 * solution[0] + 7, solution[1])
            ax.scatter([2], [1], color=F.AMBER, s=70, zorder=5)
            ax.annotate("(2,1)", (2, 1), xytext=(5, 7), textcoords="offset points", color=F.AMBER)
        ax.axhline(0, color=F.INK, lw=1)
        ax.axvline(0, color=F.INK, lw=1)
        ax.set_title(title, fontsize=12)
        ax.set_xlim(-3, 5)
        ax.set_ylim(-7, 9)
        F.clean_grid(ax)
    fig.suptitle("二元一次聯立方程式的解就是兩直線的共同點", fontsize=15)
    fig.tight_layout(rect=(0, 0, 1, 0.89))
    return _save(fig, "數1-4-聯立方程幾何.svg")


def fig_point_line_distance():
    # 直線 3x-4y+11=0，點 P(1,1)，垂足 Q(-0.2,2.6)，距離 2。
    p = np.array([1.0, 1.0])
    normal = np.array([3.0, -4.0])
    value = normal @ p + 11
    q = p - value * normal / (normal @ normal)
    distance = abs(value) / np.linalg.norm(normal)
    assert np.allclose(q, [-0.2, 2.6])
    assert np.isclose(distance, 2)

    x = np.linspace(-4, 4, 300)
    y = (3 * x + 11) / 4
    fig, ax = plt.subplots(figsize=(8.5, 5.8))
    ax.plot(x, y, color=F.BLUE, lw=2.7, label=r"$3x-4y+11=0$")
    ax.plot([p[0], q[0]], [p[1], q[1]], color=F.AMBER, lw=2.3)
    ax.scatter([p[0], q[0]], [p[1], q[1]], color=[F.GREEN, F.AMBER], s=80, zorder=5)
    ax.text(p[0] + 0.12, p[1] - 0.4, "P(1,1)", color=F.GREEN, fontsize=11)
    ax.text(q[0] - 1.25, q[1] + 0.15, "垂足 Q(−0.2,2.6)", color=F.AMBER, fontsize=11)
    ax.text(0.62, 2.0, "距離 2", rotation=53, color=F.AMBER, fontsize=11)
    ax.axhline(0, color=F.INK, lw=1)
    ax.axvline(0, color=F.INK, lw=1)
    ax.set_xlim(-4, 4)
    ax.set_ylim(-1.5, 5.5)
    ax.set_aspect("equal", adjustable="box")
    ax.set_title(r"$d=\dfrac{|ax_0+by_0+c|}{\sqrt{a^2+b^2}}$ 是沿法線方向的最短距離", fontsize=14)
    ax.legend(frameon=False, loc="lower left")
    F.clean_grid(ax)
    fig.tight_layout()
    return _save(fig, "數1-4-點線距離.svg")


def fig_half_planes():
    x = np.linspace(-1, 6, 400)
    line1 = 4 - 2 * x
    line2 = (6 - x) / 3
    fig, ax = plt.subplots(figsize=(8.5, 6.0))
    ax.plot(x, line1, color=F.BLUE, lw=2.3, label=r"$2x+y=4$")
    ax.plot(x, line2, color=F.GREEN, lw=2.3, ls="--", label=r"$x+3y=6$")
    # 可行域：x>=0, y>=0, 2x+y<=4, x+3y<6。
    polygon = np.array([[0, 0], [0, 2], [1.2, 1.6], [2, 0]])
    for px, py in polygon:
        assert px >= -1e-9 and py >= -1e-9
        assert 2 * px + py <= 4 + 1e-9
        assert px + 3 * py <= 6 + 1e-9
    ax.add_patch(Polygon(polygon, closed=True, facecolor="#bfdbfe", edgecolor="none", alpha=0.75))
    ax.scatter(polygon[:, 0], polygon[:, 1], color=F.AMBER, s=45, zorder=5)
    ax.text(0.55, 0.65, "共同解區域", color=F.BLUE, fontsize=12)
    ax.axhline(0, color=F.INK, lw=1.2)
    ax.axvline(0, color=F.INK, lw=1.2)
    ax.set_xlim(-0.7, 5.5)
    ax.set_ylim(-0.7, 4.5)
    ax.set_aspect("equal", adjustable="box")
    ax.set_title("聯立二元一次不等式取各半平面的交集", fontsize=15)
    ax.legend(frameon=False, loc="upper right")
    F.clean_grid(ax)
    fig.tight_layout()
    return _save(fig, "數1-4-半平面.svg")


def fig_circle_equation():
    center = np.array([1.0, -2.0])
    radius = 3.0
    theta = np.linspace(0, 2 * np.pi, 500)
    x = center[0] + radius * np.cos(theta)
    y = center[1] + radius * np.sin(theta)
    assert np.allclose((x - center[0]) ** 2 + (y - center[1]) ** 2, radius**2)

    point_theta = np.deg2rad(35)
    p = center + radius * np.array([np.cos(point_theta), np.sin(point_theta)])
    fig, ax = plt.subplots(figsize=(7.4, 6.5))
    ax.plot(x, y, color=F.BLUE, lw=2.8)
    ax.plot([center[0], p[0]], [center[1], p[1]], color=F.AMBER, lw=2.2)
    ax.scatter([center[0], p[0]], [center[1], p[1]], color=[F.GREEN, F.AMBER], s=80, zorder=5)
    ax.text(center[0] - 0.8, center[1] - 0.45, "C(1,−2)", color=F.GREEN, fontsize=11)
    ax.text(p[0] + 0.12, p[1] + 0.1, "P(x,y)", color=F.AMBER, fontsize=11)
    ax.text(2.0, -0.7, "CP = 3", color=F.AMBER, rotation=35, fontsize=11)
    ax.axhline(0, color=F.INK, lw=1)
    ax.axvline(0, color=F.INK, lw=1)
    ax.set_xlim(-3, 5.5)
    ax.set_ylim(-6, 3)
    ax.set_aspect("equal", adjustable="box")
    ax.set_title(r"圓的定義直接給出 $(x-1)^2+(y+2)^2=9$", fontsize=15)
    F.clean_grid(ax)
    fig.tight_layout()
    return _save(fig, "數1-4-圓方程式.svg")


def fig_circle_line_positions():
    radius = 2.0
    distances = (1.2, 2.0, 2.8)
    relations = ("d<r：兩交點", "d=r：相切", "d>r：不相交")
    fig, axes = plt.subplots(1, 3, figsize=(11.2, 4.3))
    theta = np.linspace(0, 2 * np.pi, 400)
    for ax, d, relation in zip(axes, distances, relations):
        ax.plot(radius * np.cos(theta), radius * np.sin(theta), color=F.BLUE, lw=2.6)
        ax.axhline(d, color=F.GREEN, lw=2.4)
        ax.plot([0, 0], [0, d], color=F.AMBER, lw=1.8, ls="--")
        ax.scatter([0], [0], color=F.INK, s=40)
        if d < radius:
            x0 = np.sqrt(radius**2 - d**2)
            ax.scatter([-x0, x0], [d, d], color=F.AMBER, s=55, zorder=5)
        elif np.isclose(d, radius):
            ax.scatter([0], [d], color=F.AMBER, s=55, zorder=5)
        ax.set_xlim(-2.8, 2.8)
        ax.set_ylim(-2.6, 3.3)
        ax.set_aspect("equal", adjustable="box")
        ax.set_title(relation, fontsize=12)
        ax.axis("off")
    assert distances[0] < radius and np.isclose(distances[1], radius) and distances[2] > radius
    fig.suptitle("比較圓心到直線的距離 d 與半徑 r", fontsize=15)
    fig.tight_layout(rect=(0, 0, 1, 0.9))
    return _save(fig, "數1-4-圓與直線位置.svg")


def fig_circle_tangents():
    radius = 3.0
    p_on = np.array([3.0, 0.0])
    p_out = np.array([0.0, 5.0])
    tangent_x = radius * np.sqrt(p_out[1] ** 2 - radius**2) / p_out[1]
    tangent_y = radius**2 / p_out[1]
    t1 = np.array([tangent_x, tangent_y])
    t2 = np.array([-tangent_x, tangent_y])
    assert np.isclose(np.dot(t1, p_out - t1), 0)
    assert np.isclose(np.linalg.norm(t1), radius)

    fig, axes = plt.subplots(1, 2, figsize=(10.8, 5.0))
    theta = np.linspace(0, 2 * np.pi, 400)
    for ax in axes:
        ax.plot(radius * np.cos(theta), radius * np.sin(theta), color=F.BLUE, lw=2.6)
        ax.scatter([0], [0], color=F.INK, s=40)
        ax.set_xlim(-4.5, 4.5)
        ax.set_ylim(-3.8, 6.0)
        ax.set_aspect("equal", adjustable="box")
        ax.axis("off")

    axes[0].scatter([p_on[0]], [p_on[1]], color=F.AMBER, s=65)
    axes[0].plot([0, p_on[0]], [0, p_on[1]], color=F.AMBER, lw=2)
    axes[0].axvline(p_on[0], color=F.GREEN, lw=2.4)
    axes[0].text(-2.9, 4.8, "圓上一點：\n半徑垂直切線", color=F.INK, fontsize=11)

    axes[1].scatter([p_out[0]], [p_out[1]], color=F.GREEN, s=65)
    axes[1].plot([p_out[0], t1[0]], [p_out[1], t1[1]], color=F.AMBER, lw=2.3)
    axes[1].plot([p_out[0], t2[0]], [p_out[1], t2[1]], color=F.AMBER, lw=2.3)
    axes[1].plot([0, t1[0]], [0, t1[1]], color=F.GRID, lw=1.5, ls="--")
    axes[1].plot([0, t2[0]], [0, t2[1]], color=F.GRID, lw=1.5, ls="--")
    axes[1].scatter([t1[0], t2[0]], [t1[1], t2[1]], color=F.AMBER, s=55)
    axes[1].text(-3.0, -3.35, "圓外一點：通常有兩條切線", color=F.INK, fontsize=11)

    fig.suptitle("切點處的半徑與切線垂直", fontsize=15)
    fig.tight_layout(rect=(0, 0, 1, 0.91))
    return _save(fig, "數1-4-圓的切線.svg")


if __name__ == "__main__":
    for entrypoint, filename in FIGURE_OUTPUTS:
        output = globals()[entrypoint]()
        if os.path.basename(output) != filename:
            raise AssertionError(f"{entrypoint} 輸出與 FIGURE_OUTPUTS 不一致")
