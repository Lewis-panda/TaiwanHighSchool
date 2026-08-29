# -*- coding: utf-8 -*-
"""重生「數A3-3 平面向量」新版學生講義的四張章內 SVG。

唯一寫入入口為 ``--content-all``；所有端點均從同一組向量與係數計算，
並在存檔前驗證平行、投影、行列式與克拉瑪關係。
"""

if __name__ == "__main__" and __import__("sys").argv[1:] != ["--content-all"]:
    raise SystemExit("請使用唯一參數 --content-all 重生數A3-3 章內 SVG。")

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Arc, FancyBboxPatch, Polygon

import figlib as F


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CH = os.path.join(ROOT, "content", "數學A", "數A3-3")
TOL = 1e-12


def _cross(u, v):
    return float(u[0] * v[1] - u[1] * v[0])


def _save(fig, name):
    return F.save_to(fig, CH, name, output_subdir="assets", write_pdf=False)


def _vector_axes(ax, xlim, ylim):
    ax.set_aspect("equal")
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.axhline(0, color=F.GRID, lw=0.9, zorder=0)
    ax.axvline(0, color=F.GRID, lw=0.9, zorder=0)
    ax.set_xticks([])
    ax.set_yticks([])
    for side in ("top", "right", "bottom", "left"):
        ax.spines[side].set_visible(False)


def fig_vector_composition_decomposition():
    """左：三角形法與平行四邊形法；右：不平行基底的線性組合。"""
    origin = np.zeros(2)
    a = np.array([3.0, 0.0])
    b = np.array([1.15, 2.0])
    total = a + b
    np.testing.assert_allclose(total, [4.15, 2.0], rtol=0.0, atol=TOL)
    if abs(_cross(a, b)) <= TOL:
        raise AssertionError("合成圖的兩向量不可平行")

    s, t = 0.78, 0.82
    sa = s * a
    tb = t * b
    v = sa + tb
    np.testing.assert_allclose(v, sa + tb, rtol=0.0, atol=TOL)
    if abs(_cross(sa, a)) > TOL or abs(_cross(tb, b)) > TOL:
        raise AssertionError("分解分量必須分別平行於基底向量")

    fig, axes = plt.subplots(1, 2, figsize=(10.8, 5.0))

    ax = axes[0]
    _vector_axes(ax, (-0.45, 4.75), (-0.65, 2.75))
    ax.add_patch(
        Polygon([origin, a, total, b], closed=True, facecolor="#dbeafe", edgecolor="none")
    )
    F.arrow(ax, origin, a, color=F.BLUE, lw=2.8)
    F.arrow(ax, origin, b, color=F.GREEN, lw=2.8)
    F.arrow(ax, a, total, color=F.GREEN, lw=2.5, ls="--")
    ax.plot([b[0], total[0]], [b[1], total[1]], color=F.BLUE, lw=1.8, ls="--")
    F.arrow(ax, origin, total, color=F.AMBER, lw=3.2)
    ax.text(1.55, -0.32, r"$\vec a$", color=F.BLUE, fontsize=15, ha="center")
    ax.text(0.35, 1.15, r"$\vec b$", color=F.GREEN, fontsize=15, ha="center")
    ax.text(2.35, 1.35, r"$\vec a+\vec b$", color=F.AMBER, fontsize=14, ha="center")
    ax.set_title("合成：接箭頭與平行四邊形結果相同", fontsize=12.5)

    ax = axes[1]
    _vector_axes(ax, (-0.45, 4.4), (-0.65, 2.75))
    ax.plot([0, 4.05], [0, 0], color="#94a3b8", lw=1.5, ls="--")
    ax.plot([0, 1.55], [0, 2.70], color="#94a3b8", lw=1.5, ls="--")
    F.arrow(ax, origin, a, color="#64748b", lw=1.8, alpha=0.8)
    F.arrow(ax, origin, b, color="#64748b", lw=1.8, alpha=0.8)
    F.arrow(ax, origin, sa, color=F.BLUE, lw=3.0)
    F.arrow(ax, sa, v, color=F.GREEN, lw=3.0)
    F.arrow(ax, origin, v, color=F.AMBER, lw=3.3)
    ax.plot([0, tb[0]], [0, tb[1]], color=F.GREEN, lw=1.7, ls="--")
    ax.plot([tb[0], v[0]], [tb[1], v[1]], color=F.BLUE, lw=1.7, ls="--")
    ax.text(1.25, -0.32, r"$s\vec a$", color=F.BLUE, fontsize=14, ha="center")
    ax.text(sa[0] + 0.55 * tb[0] + 0.10, 0.55 * tb[1], r"$t\vec b$", color=F.GREEN, fontsize=14)
    ax.text(0.90, 2.38, r"$\vec b$ 方向", color="#64748b", fontsize=11, rotation=60)
    ax.text(v[0] + 0.08, v[1] + 0.10, r"$\vec v=s\vec a+t\vec b$", color=F.AMBER, fontsize=13)
    ax.set_title("分解：兩個分量各自平行於基底方向", fontsize=12.5)

    fig.suptitle("向量合成與線性組合", fontsize=15, y=0.995)
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    return _save(fig, "數A3-3-向量合成與分解")


def fig_dot_product_projection():
    """內積、帶號投影量與垂足幾何。"""
    origin = np.zeros(2)
    u = np.array([5.0, 0.0])
    v = np.array([2.85, 2.25])
    unit_u = u / np.linalg.norm(u)
    scalar_projection = float(np.dot(v, u) / np.linalg.norm(u))
    projection = float(np.dot(v, u) / np.dot(u, u)) * u
    rejection = v - projection

    np.testing.assert_allclose(projection, scalar_projection * unit_u, rtol=0.0, atol=TOL)
    if abs(float(np.dot(rejection, u))) > TOL:
        raise AssertionError("垂足到原向量的差必須垂直於投影方向")
    if not np.isclose(np.linalg.norm(projection), scalar_projection):
        raise AssertionError("銳角範例的投影長必須等於帶號投影量")

    fig, ax = plt.subplots(figsize=(10.8, 5.0))
    _vector_axes(ax, (-0.55, 10.3), (-1.05, 3.45))
    F.arrow(ax, origin, u, color=F.BLUE, lw=3.0)
    F.arrow(ax, origin, v, color=F.GREEN, lw=3.0)
    ax.plot(
        [v[0], projection[0]],
        [v[1], projection[1]],
        color="#94a3b8",
        lw=2.0,
        ls="--",
    )
    ax.plot([0, projection[0]], [-0.63, -0.63], color=F.AMBER, lw=4.0)
    ax.plot([0, 0], [-0.77, -0.49], color=F.AMBER, lw=2.2)
    ax.plot(
        [projection[0], projection[0]], [-0.77, -0.49], color=F.AMBER, lw=2.2
    )
    ax.scatter(*projection, s=48, color=F.AMBER, zorder=6)
    right_size = 0.22
    ax.add_patch(
        Polygon(
            [
                projection,
                projection + [-right_size, 0],
                projection + [-right_size, right_size],
                projection + [0, right_size],
            ],
            closed=True,
            fill=False,
            edgecolor="#64748b",
            lw=1.2,
        )
    )
    angle = float(np.degrees(np.arctan2(v[1], v[0])))
    ax.add_patch(Arc(origin, 1.55, 1.55, theta1=0, theta2=angle, color=F.AMBER, lw=2.0))
    ax.text(0.92, 0.27, r"$\theta$", color=F.AMBER, fontsize=14)
    ax.text(4.4, -0.35, r"$\vec u$", color=F.BLUE, fontsize=15)
    ax.text(1.25, 1.50, r"$\vec v$", color=F.GREEN, fontsize=15)
    ax.text(
        projection[0] / 2,
        -0.92,
        "帶號投影量 " + r"$=\frac{\vec v\cdot\vec u}{|\vec u|}$",
        color=F.AMBER,
        fontsize=13,
        ha="center",
    )

    card = FancyBboxPatch(
        (5.65, -0.10),
        4.15,
        2.95,
        boxstyle="round,pad=0.18",
        facecolor="#f8fafc",
        edgecolor="#cbd5e1",
        lw=1.5,
    )
    ax.add_patch(card)
    ax.text(7.72, 2.48, "內積的符號讀取夾角", fontsize=13, ha="center", weight="bold")
    ax.text(6.05, 1.88, r"銳角：$\vec v\cdot\vec u>0$", fontsize=12, color=F.GREEN)
    ax.text(6.05, 1.30, r"直角：$\vec v\cdot\vec u=0$", fontsize=12, color=F.INK)
    ax.text(6.05, 0.72, r"鈍角：$\vec v\cdot\vec u<0$", fontsize=12, color=F.RED)
    ax.text(7.72, 0.20, r"前提：$\vec u\ne\vec0$", fontsize=11.5, color="#64748b", ha="center")
    ax.set_title("內積判斷方向關係，投影保留沿目標方向的分量", fontsize=15, pad=12)
    fig.tight_layout()
    return _save(fig, "數A3-3-內積與投影")


def fig_determinant_area_orientation():
    """行列式的絕對值與符號分別表示面積與定向。"""
    origin = np.zeros(2)
    a = np.array([3.6, 0.0])
    b = np.array([1.15, 2.35])
    determinant = _cross(a, b)
    if determinant <= 0:
        raise AssertionError("左圖必須是正定向的非退化平行四邊形")
    vertices = np.array([origin, a, a + b, b])
    shoelace = 0.5 * abs(
        np.dot(vertices[:, 0], np.roll(vertices[:, 1], -1))
        - np.dot(vertices[:, 1], np.roll(vertices[:, 0], -1))
    )
    np.testing.assert_allclose(shoelace, abs(determinant), rtol=0.0, atol=TOL)

    direction = np.array([2.0, 0.0])
    positive = np.array([-1.0, 1.75])
    negative = np.array([-1.0, -1.75])
    if not (_cross(direction, positive) > 0 and _cross(direction, negative) < 0):
        raise AssertionError("定向圖的正負符號必須與旋轉方向一致")
    positive_angle = float(np.degrees(np.arctan2(positive[1], positive[0])))
    negative_angle = float(np.degrees(np.arctan2(negative[1], negative[0])))

    fig, axes = plt.subplots(1, 2, figsize=(10.8, 5.0))
    ax = axes[0]
    _vector_axes(ax, (-0.55, 5.3), (-0.65, 3.05))
    ax.add_patch(
        Polygon(vertices, closed=True, facecolor="#dbeafe", edgecolor="#93c5fd", lw=1.7)
    )
    F.arrow(ax, origin, a, color=F.BLUE, lw=3.0)
    F.arrow(ax, origin, b, color=F.GREEN, lw=3.0)
    ax.plot([a[0], (a + b)[0]], [a[1], (a + b)[1]], color="#94a3b8", ls="--")
    ax.plot([b[0], (a + b)[0]], [b[1], (a + b)[1]], color="#94a3b8", ls="--")
    ax.text(1.8, -0.32, r"$\vec a$", color=F.BLUE, fontsize=15, ha="center")
    ax.text(0.28, 1.35, r"$\vec b$", color=F.GREEN, fontsize=15)
    ax.text(
        2.55,
        1.18,
        "面積 " + r"$=|\det(\vec a,\vec b)|$",
        color="#1e3a8a",
        fontsize=13.5,
        ha="center",
        bbox=dict(boxstyle="round,pad=0.35", fc="white", ec="#bfdbfe"),
    )
    ax.set_title("絕對值給出平行四邊形面積", fontsize=12.5)

    ax = axes[1]
    _vector_axes(ax, (-2.25, 2.85), (-2.45, 2.55))
    F.arrow(ax, origin, direction, color=F.BLUE, lw=3.0)
    F.arrow(ax, origin, positive, color=F.GREEN, lw=3.0)
    F.arrow(ax, origin, negative, color=F.RED, lw=3.0)
    ax.add_patch(
        Arc(origin, 2.2, 2.2, theta1=0, theta2=positive_angle, color=F.GREEN, lw=2.2)
    )
    ax.add_patch(
        Arc(origin, 1.6, 1.6, theta1=negative_angle, theta2=0, color=F.RED, lw=2.2)
    )
    ax.text(1.15, 0.22, r"$\vec a$", color=F.BLUE, fontsize=14)
    ax.text(-1.88, 1.82, "逆時針：" + r"$\det>0$", color=F.GREEN, fontsize=12)
    ax.text(-1.88, -2.13, "順時針：" + r"$\det<0$", color=F.RED, fontsize=12)
    ax.text(
        0.10,
        -0.30,
        r"$\det=0$：線性相依，面積退化為 $0$",
        color="#64748b",
        fontsize=11.5,
        ha="center",
        bbox=dict(boxstyle="round,pad=0.35", fc="white", ec="#cbd5e1"),
    )
    ax.set_title("正負號保留從第一向量轉向第二向量的方向", fontsize=12.5)

    fig.suptitle("行列式的面積與定向", fontsize=15, y=0.995)
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    return _save(fig, "數A3-3-行列式面積與定向")


def fig_cramer_linear_combination():
    """克拉瑪公式的向量線性組合觀點。"""
    origin = np.zeros(2)
    a = np.array([3.25, 0.18])
    b = np.array([0.90, 2.30])
    x_value, y_value = 0.92, 0.76
    xa = x_value * a
    yb = y_value * b
    c = xa + yb

    delta = _cross(a, b)
    delta_x = _cross(c, b)
    delta_y = _cross(a, c)
    if abs(delta) <= TOL:
        raise AssertionError("克拉瑪範例的主行列式必須非零")
    np.testing.assert_allclose(c, xa + yb, rtol=0.0, atol=TOL)
    if abs(_cross(xa, a)) > TOL or abs(_cross(yb, b)) > TOL:
        raise AssertionError("克拉瑪圖的倍數向量必須平行於原向量")
    np.testing.assert_allclose(delta_x / delta, x_value, rtol=0.0, atol=TOL)
    np.testing.assert_allclose(delta_y / delta, y_value, rtol=0.0, atol=TOL)

    fig, (ax, info) = plt.subplots(
        1,
        2,
        figsize=(10.8, 5.0),
        gridspec_kw={"width_ratios": [1.65, 0.85]},
    )
    _vector_axes(ax, (-0.55, 4.35), (-0.65, 2.75))
    ax.plot([0, 3.95], [0, 3.95 * a[1] / a[0]], color="#94a3b8", lw=1.4, ls="--")
    ax.plot([0, 1.05], [0, 1.05 * b[1] / b[0]], color="#94a3b8", lw=1.4, ls="--")
    F.arrow(ax, origin, a, color="#64748b", lw=1.8, alpha=0.8)
    F.arrow(ax, origin, b, color="#64748b", lw=1.8, alpha=0.8)
    F.arrow(ax, origin, xa, color=F.BLUE, lw=3.0)
    F.arrow(ax, xa, c, color=F.GREEN, lw=3.0)
    F.arrow(ax, origin, c, color=F.AMBER, lw=3.3)
    ax.plot([0, yb[0]], [0, yb[1]], color=F.GREEN, lw=1.7, ls="--")
    ax.plot([yb[0], c[0]], [yb[1], c[1]], color=F.BLUE, lw=1.7, ls="--")
    ax.text(1.50, -0.32, r"$x\vec a$", color=F.BLUE, fontsize=14, ha="center")
    ax.text(xa[0] + 0.50 * yb[0] + 0.08, xa[1] + 0.50 * yb[1], r"$y\vec b$", color=F.GREEN, fontsize=14)
    ax.text(c[0] + 0.08, c[1] + 0.10, r"$\vec c$", color=F.AMBER, fontsize=15)
    ax.text(2.10, 2.48, r"$\vec c=x\vec a+y\vec b$", fontsize=13.5, ha="center")
    ax.set_title("兩個係數向量精確相加成目標向量", fontsize=12.5)

    info.axis("off")
    info.set_xlim(0, 1)
    info.set_ylim(0, 1)
    info.text(0.5, 0.93, r"主行列式 $\Delta$", fontsize=14, weight="bold", ha="center")
    info.text(
        0.5,
        0.69,
        r"$\Delta\ne0$" + "\n兩個基底方向不平行\n唯一解",
        color="#1e3a8a",
        fontsize=12.5,
        ha="center",
        va="center",
        linespacing=1.5,
        bbox=dict(boxstyle="round,pad=0.65", fc="#eff6ff", ec="#bfdbfe", lw=1.5),
    )
    info.text(
        0.5,
        0.25,
        r"$\Delta=0$" + "\n兩個基底方向線性相依\n再檢查常數是否相容\n無解或無限多解",
        color="#475569",
        fontsize=11.5,
        ha="center",
        va="center",
        linespacing=1.45,
        bbox=dict(boxstyle="round,pad=0.60", fc="#f8fafc", ec="#cbd5e1", lw=1.5),
    )
    fig.suptitle("克拉瑪公式：求出兩個基底向量的倍數", fontsize=15, y=0.995)
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    return _save(fig, "數A3-3-克拉瑪線性組合")


def main():
    fig_vector_composition_decomposition()
    fig_dot_product_projection()
    fig_determinant_area_orientation()
    fig_cramer_linear_combination()
    print("done.")


if __name__ == "__main__":
    main()
