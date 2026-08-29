# -*- coding: utf-8 -*-
"""重生「數A4-1 空間向量」學生講義的章內 SVG。"""

if __name__ == "__main__" and __import__("sys").argv[1:]:
    raise SystemExit("本腳本不接受參數；直接執行即可重生數A4-1章內 SVG。")

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Arc, FancyArrowPatch, Polygon, Rectangle
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

import figlib as F


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHAPTER = os.path.join(ROOT, "content", "數學A", "數A4-1")

FIGURE_OUTPUTS = (
    ("fig_line_plane_relations", "數A4-1-直線與平面關係.svg"),
    ("fig_three_perpendiculars", "數A4-1-三垂線定理.svg"),
    ("fig_coordinate_projections", "數A4-1-空間坐標與投影.svg"),
    ("fig_vectors_and_division", "數A4-1-向量坐標與分點.svg"),
    ("fig_dot_product", "數A4-1-內積與夾角.svg"),
    ("fig_projection_decomposition", "數A4-1-正射影分解.svg"),
    ("fig_cauchy", "數A4-1-柯西不等式幾何.svg"),
    ("fig_cross_product", "數A4-1-外積方向與面積.svg"),
    ("fig_triple_product", "數A4-1-三重積與體積.svg"),
    ("fig_determinant", "數A4-1-三階行列式.svg"),
    ("fig_torque", "數A4-1-力矩模型.svg"),
)


def _save(fig, filename):
    stem, extension = os.path.splitext(filename)
    if extension != ".svg" or not stem.startswith("數A4-1-"):
        raise AssertionError("輸出檔名必須是數A4-1章內 SVG")
    return F.save_to(fig, CHAPTER, stem, output_subdir="assets", write_pdf=False)


def _style_3d(ax, lim=(0, 4)):
    ax.set_xlim(*lim)
    ax.set_ylim(*lim)
    ax.set_zlim(*lim)
    ax.set_box_aspect((1, 1, 0.85))
    ax.view_init(elev=24, azim=-58)
    ax.grid(False)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_zticks([])
    for axis in (ax.xaxis, ax.yaxis, ax.zaxis):
        axis.pane.set_alpha(0)


def _arrow2(ax, start, end, color=F.BLUE, lw=2.3):
    arrow = FancyArrowPatch(start, end, arrowstyle="-|>", mutation_scale=16,
                            linewidth=lw, color=color, shrinkA=0, shrinkB=0)
    ax.add_patch(arrow)
    return arrow


def fig_line_plane_relations():
    fig, axes = plt.subplots(2, 2, figsize=(10.2, 7.2))
    panels = (
        ("兩直線相交", "intersect"),
        ("兩直線平行", "parallel"),
        ("兩直線歪斜", "skew"),
        ("直線垂直平面", "normal"),
    )
    plane = np.array([[0.7, 0.8], [4.7, 0.8], [5.6, 3.5], [1.6, 3.5]])
    for ax, (title, kind) in zip(axes.flat, panels):
        ax.add_patch(Polygon(plane, closed=True, facecolor="#eef5ff", edgecolor="#8aa8c7", lw=1.5))
        if kind == "intersect":
            ax.plot([1.2, 5.0], [1.2, 3.1], color=F.BLUE, lw=2.5)
            ax.plot([1.5, 4.9], [3.1, 1.2], color=F.GREEN, lw=2.5)
            ax.scatter([3.15], [2.18], color=F.AMBER, s=55, zorder=4)
            ax.text(3.15, 1.85, "交點", ha="center", fontsize=10)
        elif kind == "parallel":
            ax.plot([1.35, 4.8], [1.45, 2.2], color=F.BLUE, lw=2.5)
            ax.plot([1.7, 5.15], [2.35, 3.1], color=F.GREEN, lw=2.5)
        elif kind == "skew":
            ax.plot([1.25, 4.8], [1.15, 1.9], color=F.BLUE, lw=2.5)
            ax.plot([2.3, 4.7], [3.55, 2.6], color=F.RED, lw=2.5)
            ax.plot([2.3, 2.3], [3.55, 2.1], color=F.RED, lw=1.2, ls="--")
            ax.text(4.6, 3.45, "不同平面", color=F.RED, ha="right", fontsize=10)
        else:
            ax.plot([1.4, 5.0], [1.45, 2.35], color=F.GREEN, lw=2.0)
            ax.plot([1.7, 4.8], [2.8, 1.25], color=F.PURPLE, lw=2.0)
            ax.scatter([3.25], [1.9], color=F.AMBER, s=55, zorder=5)
            _arrow2(ax, (3.25, 1.9), (3.25, 4.55), color=F.BLUE)
            ax.text(3.43, 4.35, "法線", color=F.BLUE, fontsize=10)
            ax.add_patch(Rectangle((3.25, 1.9), 0.28, 0.28, angle=0, fill=False, edgecolor=F.INK, lw=1.2))
        ax.set_title(title, fontsize=13)
        ax.set_xlim(0.3, 6)
        ax.set_ylim(0.2, 4.8)
        ax.set_aspect("equal")
        ax.axis("off")
    fig.suptitle("空間位置關係先看是否共平面，再判斷交點與角度", fontsize=15)
    fig.tight_layout(rect=(0, 0, 1, 0.94))
    return _save(fig, "數A4-1-直線與平面關係.svg")


def fig_three_perpendiculars():
    fig = plt.figure(figsize=(9.2, 6.5))
    ax = fig.add_subplot(111, projection="3d")
    A = np.array([0.8, 1.0, 0.0])
    P = np.array([0.8, 1.0, 3.2])
    B = np.array([3.1, 1.0, 0.0])
    C = np.array([3.1, 3.5, 0.0])
    plane = [[(0, 0, 0), (4.4, 0, 0), (4.4, 4.0, 0), (0, 4.0, 0)]]
    ax.add_collection3d(Poly3DCollection(
        plane, facecolors="#e8f3ff", edgecolors="#52606d", alpha=0.38,
    ))
    ax.plot(*np.array([A, P]).T, color=F.BLUE, lw=2.9, ls="-")
    ax.plot(*np.array([A, B]).T, color=F.GREEN, lw=2.9, ls="--")
    ax.plot(*np.array([B, C]).T, color=F.RED, lw=2.9, ls=":")
    ax.plot(*np.array([P, B]).T, color=F.AMBER, lw=2.9, ls="-.")
    for name, point in (("A", A), ("P", P), ("B", B)):
        ax.scatter(*point, s=58, color=F.INK, depthshade=False)
        ax.text(
            *(point + np.array([0.08, 0.08, 0.12])), name,
            color=F.INK, fontsize=12,
            bbox={"facecolor": "white", "edgecolor": "none", "alpha": 0.78, "pad": 0.8},
        )
    ax.text(3.2, 3.45, 0.16, "直線 L（點線）", color=F.INK, fontsize=11)
    ax.text(4.0, 0.25, 0.08, "平面 E", color=F.INK, fontsize=11)
    ax.text(0.25, 0.45, 1.85, "高度 PA（實線）", color=F.INK, fontsize=11)
    ax.text(1.75, 0.55, 0.14, "投影 AB（虛線）", color=F.INK, fontsize=11)
    ax.text(1.35, 0.45, 2.45, "斜線 PB（點畫線）", color=F.INK, fontsize=11)
    assert np.isclose(np.dot(A - B, C - B), 0)
    assert np.isclose(np.dot(P - B, C - B), 0)
    _style_3d(ax, (0, 4.4))
    ax.set_title("三垂線定理把平面內的垂直關係帶到空間斜線", fontsize=15)
    fig.tight_layout()
    return _save(fig, "數A4-1-三垂線定理.svg")


def fig_coordinate_projections():
    fig = plt.figure(figsize=(9.2, 6.7))
    ax = fig.add_subplot(111, projection="3d")
    P = np.array([3.2, 2.4, 2.8])
    O = np.zeros(3)
    colors = (F.BLUE, F.GREEN, F.RED)
    labels = ("x", "y", "z")
    ends = np.eye(3) * 4.2
    for end, color, label in zip(ends, colors, labels):
        ax.quiver(*O, *end, color=color, arrow_length_ratio=0.08, lw=2.0)
        ax.text(*(end * 1.04), label, color=color, fontsize=13)
    ax.scatter(*P, color=F.AMBER, s=75)
    ax.text(*(P + np.array([0.08, 0.08, 0.15])), r"$P(a,b,c)$", fontsize=12)
    vertices = [
        np.array([P[0], P[1], 0]), np.array([P[0], 0, P[2]]), np.array([0, P[1], P[2]]),
        np.array([P[0], 0, 0]), np.array([0, P[1], 0]), np.array([0, 0, P[2]]),
    ]
    for Q in vertices:
        ax.plot(*np.array([P, Q]).T, color="#7b8794", lw=1.2, ls="--")
        ax.scatter(*Q, color="#7b8794", s=28)
    ax.text(P[0], P[1], 0.15, r"$(a,b,0)$", fontsize=10, ha="center")
    ax.text(P[0], 0.1, P[2], r"$(a,0,c)$", fontsize=10)
    ax.text(0.05, P[1], P[2], r"$(0,b,c)$", fontsize=10)
    assert np.isclose(np.linalg.norm(P), np.sqrt(P @ P))
    _style_3d(ax, (0, 4.4))
    ax.set_title("坐標是沿三條互相垂直軸量出的有向分量", fontsize=15)
    fig.tight_layout()
    return _save(fig, "數A4-1-空間坐標與投影.svg")


def fig_vectors_and_division():
    fig, axes = plt.subplots(1, 2, figsize=(10.4, 5.1))
    ax = axes[0]
    A = np.array([0.5, 1.0])
    B = np.array([5.0, 3.3])
    m, n = 2, 3
    P = (n * A + m * B) / (m + n)
    assert np.isclose(np.linalg.norm(P - A) / np.linalg.norm(B - P), m / n)
    ax.plot([A[0], B[0]], [A[1], B[1]], color=F.BLUE, lw=2.6)
    ax.scatter([A[0], P[0], B[0]], [A[1], P[1], B[1]], color=[F.GREEN, F.AMBER, F.RED], s=65)
    for name, point in (("A", A), ("P", P), ("B", B)):
        ax.text(point[0], point[1] + 0.3, name, ha="center", fontsize=12)
    ax.text(2.75, 0.35, r"$P=\dfrac{nA+mB}{m+n},\quad AP:PB=m:n$", ha="center", fontsize=12)
    ax.set_title("內分點是端點的加權平均", fontsize=13)
    ax.set_xlim(0, 5.5)
    ax.set_ylim(0, 4.3)
    ax.set_aspect("equal")
    ax.axis("off")

    ax = axes[1]
    O = np.array([0.7, 0.8])
    a = np.array([3.2, 0.7])
    b = np.array([1.1, 2.7])
    _arrow2(ax, O, O + a, color=F.BLUE)
    _arrow2(ax, O, O + b, color=F.GREEN)
    _arrow2(ax, O, O + a + b, color=F.PURPLE)
    ax.plot([*(O + a)[0:1], *(O + a + b)[0:1]], [*(O + a)[1:2], *(O + a + b)[1:2]], color="#9aa4af", ls="--")
    ax.plot([O[0] + b[0], O[0] + a[0] + b[0]], [O[1] + b[1], O[1] + a[1] + b[1]], color="#9aa4af", ls="--")
    ax.text(*(O + 0.55 * a + np.array([0.0, -0.28])), r"$\vec a$", color=F.BLUE, fontsize=12)
    ax.text(*(O + 0.55 * b + np.array([-0.25, 0.0])), r"$\vec b$", color=F.GREEN, fontsize=12)
    ax.text(*(O + 0.58 * (a + b) + np.array([0.12, 0.05])), r"$\vec a+\vec b$", color=F.PURPLE, fontsize=12)
    ax.set_title("線性組合逐分量相加", fontsize=13)
    ax.set_xlim(0, 5.5)
    ax.set_ylim(0, 4.8)
    ax.set_aspect("equal")
    ax.axis("off")
    fig.suptitle("空間向量的坐標運算沿用平面向量的平移與平行四邊形法則", fontsize=15)
    fig.tight_layout(rect=(0, 0, 1, 0.92))
    return _save(fig, "數A4-1-向量坐標與分點.svg")


def fig_dot_product():
    a = np.array([4.2, 1.7])
    b = np.array([4.5, 0.0])
    theta = np.arccos(a @ b / (np.linalg.norm(a) * np.linalg.norm(b)))
    assert 0 < theta < np.pi / 2
    fig, ax = plt.subplots(figsize=(8.8, 5.4))
    O = np.array([0.7, 0.8])
    _arrow2(ax, O, O + b, color=F.GREEN)
    _arrow2(ax, O, O + a, color=F.BLUE)
    projection = (a @ b / (b @ b)) * b
    ax.plot([O[0] + a[0], O[0] + projection[0]], [O[1] + a[1], O[1] + projection[1]], color=F.RED, ls="--", lw=1.8)
    ax.scatter([O[0] + projection[0]], [O[1] + projection[1]], color=F.AMBER, s=55)
    ax.add_patch(Arc(O, 1.8, 1.8, theta1=0, theta2=np.degrees(theta), color=F.AMBER, lw=1.8))
    ax.text(O[0] + 1.0, O[1] + 0.25, r"$\theta$", color=F.AMBER, fontsize=13)
    ax.text(O[0] + 2.2, O[1] - 0.4, r"$\vec b$", color=F.GREEN, fontsize=12)
    ax.text(O[0] + 2.0, O[1] + 1.15, r"$\vec a$", color=F.BLUE, fontsize=12)
    ax.text(3.1, 4.15, r"$\vec a\cdot\vec b=|\vec a|\,|\vec b|\cos\theta$", ha="center", fontsize=14)
    ax.text(3.1, 3.55, "內積量到的是一向量沿另一方向的有效分量", ha="center", fontsize=12)
    ax.set_xlim(0, 6)
    ax.set_ylim(0, 4.7)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("內積把夾角、垂直與投影連成同一個量", fontsize=15)
    fig.tight_layout()
    return _save(fig, "數A4-1-內積與夾角.svg")


def fig_projection_decomposition():
    a = np.array([4.1, 2.7])
    b = np.array([4.4, 0.8])
    parallel = (a @ b / (b @ b)) * b
    perpendicular = a - parallel
    assert np.isclose(perpendicular @ b, 0)
    fig, ax = plt.subplots(figsize=(9.0, 5.5))
    O = np.array([0.8, 0.8])
    D = O + parallel
    A = O + a
    _arrow2(ax, O, O + b, color=F.GREEN)
    _arrow2(ax, O, A, color=F.BLUE)
    _arrow2(ax, O, D, color=F.PURPLE)
    _arrow2(ax, D, A, color=F.RED)
    ax.plot([O[0] - 0.3, O[0] + 5.0], [O[1] - 0.05, O[1] + 0.91], color="#aab4be", lw=1.0)
    ax.text(*(D + np.array([0.05, -0.35])), "D", fontsize=11)
    ax.text(3.2, 0.35, r"$\operatorname{proj}_{\vec b}\vec a=\dfrac{\vec a\cdot\vec b}{|\vec b|^2}\vec b$", ha="center", fontsize=13)
    ax.text(3.2, 4.4, r"$\vec a=\vec a_{\parallel}+\vec a_{\perp},\quad \vec a_{\perp}\cdot\vec b=0$", ha="center", fontsize=13)
    ax.text(2.6, 1.65, r"$\vec a_{\parallel}$", color=F.PURPLE, fontsize=12)
    ax.text(4.15, 2.5, r"$\vec a_{\perp}$", color=F.RED, fontsize=12)
    ax.set_xlim(0, 6)
    ax.set_ylim(0, 5)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("正射影把向量拆成平行與垂直兩個互不干擾的分量", fontsize=15)
    fig.tight_layout()
    return _save(fig, "數A4-1-正射影分解.svg")


def fig_cauchy():
    fig, axes = plt.subplots(1, 2, figsize=(10.2, 4.8))
    cases = (
        (np.array([3.7, 2.2]), np.array([4.2, 0.0]), "一般情形：投影短於向量"),
        (np.array([3.8, 0.0]), np.array([4.5, 0.0]), "等號情形：兩向量平行"),
    )
    for ax, (a, b, title) in zip(axes, cases):
        O = np.array([0.6, 0.8])
        _arrow2(ax, O, O + b, color=F.GREEN)
        _arrow2(ax, O, O + a, color=F.BLUE)
        proj = (a @ b / (b @ b)) * b
        ax.plot([O[0] + a[0], O[0] + proj[0]], [O[1] + a[1], O[1] + proj[1]], color=F.RED, ls="--", lw=1.6)
        ax.text(2.65, 3.65, r"$|\vec a\cdot\vec b|\leq |\vec a|\,|\vec b|$", ha="center", fontsize=12)
        ax.set_title(title, fontsize=12)
        ax.set_xlim(0, 5.5)
        ax.set_ylim(0, 4.1)
        ax.set_aspect("equal")
        ax.axis("off")
    fig.suptitle("柯西不等式來自投影長不超過原向量長", fontsize=15)
    fig.tight_layout(rect=(0, 0, 1, 0.92))
    return _save(fig, "數A4-1-柯西不等式幾何.svg")


def fig_cross_product():
    a = np.array([3.1, 0.2, 0.0])
    b = np.array([0.8, 2.4, 0.0])
    cross = np.cross(a, b)
    assert np.isclose(cross @ a, 0) and np.isclose(cross @ b, 0)
    fig = plt.figure(figsize=(9.2, 6.7))
    ax = fig.add_subplot(111, projection="3d")
    O = np.zeros(3)
    vertices = [O, a, a + b, b]
    ax.add_collection3d(Poly3DCollection([vertices], facecolors="#dff3e5", edgecolors=F.GREEN, alpha=0.72))
    ax.quiver(*O, *a, color=F.BLUE, arrow_length_ratio=0.08, lw=2.4)
    ax.quiver(*O, *b, color=F.GREEN, arrow_length_ratio=0.08, lw=2.4)
    scaled_cross = cross / np.linalg.norm(cross) * 3.0
    ax.quiver(*O, *scaled_cross, color=F.RED, arrow_length_ratio=0.09, lw=2.7)
    ax.text(*(a * 0.65 + np.array([0, -0.15, 0.12])), r"$\vec a$", color=F.BLUE, fontsize=12)
    ax.text(*(b * 0.7 + np.array([-0.15, 0, 0.12])), r"$\vec b$", color=F.GREEN, fontsize=12)
    ax.text(*(scaled_cross * 0.8 + np.array([0.1, 0.1, 0])), r"$\vec a\times\vec b$", color=F.RED, fontsize=12)
    ax.text(1.25, 1.2, 0.15, r"面積 $=|\vec a\times\vec b|$", fontsize=12)
    _style_3d(ax, (-0.4, 4.0))
    ax.set_title("外積方向依右手定則，長度等於張成的平行四邊形面積", fontsize=15)
    fig.tight_layout()
    return _save(fig, "數A4-1-外積方向與面積.svg")


def fig_triple_product():
    a = np.array([2.8, 0.2, 0.0])
    b = np.array([0.7, 2.1, 0.0])
    c = np.array([0.6, 0.5, 2.5])
    volume = abs(np.dot(a, np.cross(b, c)))
    assert volume > 0
    fig = plt.figure(figsize=(9.3, 6.8))
    ax = fig.add_subplot(111, projection="3d")
    O = np.zeros(3)
    points = [O, a, b, c, a + b, a + c, b + c, a + b + c]
    edges = ((0,1),(0,2),(0,3),(1,4),(1,5),(2,4),(2,6),(3,5),(3,6),(4,7),(5,7),(6,7))
    for i, j in edges:
        ax.plot(*np.array([points[i], points[j]]).T, color=F.BLUE if (i,j) in ((0,1),(0,2),(0,3)) else "#6b7785", lw=2.0)
    ax.add_collection3d(Poly3DCollection([[O, a, a + b, b]], facecolors="#dff3e5", edgecolors=F.GREEN, alpha=0.65))
    foot = np.array([c[0], c[1], 0.0])
    ax.plot(*np.array([c, foot]).T, color=F.RED, lw=2.0, ls="--")
    ax.text(*(0.55 * a + np.array([0, -0.1, 0.08])), r"$\vec a$", fontsize=12, color=F.BLUE)
    ax.text(*(0.55 * b + np.array([-0.15, 0, 0.08])), r"$\vec b$", fontsize=12, color=F.GREEN)
    ax.text(*(0.62 * c + np.array([0.12, 0.05, 0])), r"$\vec c$", fontsize=12, color=F.PURPLE)
    ax.text(*(0.5 * (c + foot) + np.array([0.08, 0.08, 0])), "高", color=F.RED, fontsize=11)
    ax.text(0.2, 3.25, 3.25, r"$V=|\vec a\cdot(\vec b\times\vec c)|$", fontsize=14)
    _style_3d(ax, (-0.3, 4.0))
    ax.set_title("三重積是底面積乘上第三向量的垂直高度", fontsize=15)
    fig.tight_layout()
    return _save(fig, "數A4-1-三重積與體積.svg")


def fig_determinant():
    matrix = np.array([[2, 1, 0], [1, 3, 2], [0, 1, 4]])
    determinant = round(np.linalg.det(matrix))
    assert determinant == 16
    fig, axes = plt.subplots(1, 2, figsize=(10.4, 5.3))
    ax = axes[0]
    ax.text(0.5, 0.82, "三階行列式", ha="center", fontsize=14)
    rows = [["2", "1", "0", "2", "1"], ["1", "3", "2", "1", "3"], ["0", "1", "4", "0", "1"]]
    for i, row in enumerate(rows):
        for j, value in enumerate(row):
            ax.text(0.18 + 0.16*j, 0.66 - 0.18*i, value, ha="center", va="center", fontsize=13,
                    color=F.INK if j < 3 else "#8793a1")
    for j in range(3):
        ax.plot([0.18+0.16*j, 0.18+0.16*(j+2)], [0.66, 0.30], color=F.BLUE, lw=1.6)
        ax.plot([0.18+0.16*j, 0.18+0.16*(j+2)], [0.30, 0.66], color=F.RED, lw=1.6)
    ax.text(0.5, 0.12, "右下乘積相加，右上乘積相減", ha="center", fontsize=11)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    ax = axes[1]
    ax.text(0.5, 0.82, "列向量的幾何意義", ha="center", fontsize=14)
    ax.text(0.5, 0.63, r"$\det(\vec a,\vec b,\vec c)=\vec a\cdot(\vec b\times\vec c)$", ha="center", fontsize=13)
    ax.text(0.5, 0.47, r"$|\det|=$ 平行六面體體積", ha="center", fontsize=12, color=F.BLUE)
    ax.text(0.5, 0.33, r"$\det=0\Longleftrightarrow$ 三向量共面", ha="center", fontsize=12, color=F.RED)
    ax.text(0.5, 0.16, rf"本例 $\det={determinant}$", ha="center", fontsize=13, color=F.GREEN)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    fig.suptitle("行列式把坐標運算與有向體積連在一起", fontsize=15)
    fig.tight_layout(rect=(0, 0, 1, 0.92))
    return _save(fig, "數A4-1-三階行列式.svg")


def fig_torque():
    r = 4.2
    force = 2.8
    theta_deg = 55
    torque = r * force * np.sin(np.deg2rad(theta_deg))
    assert np.isclose(torque, 9.633, atol=0.01)
    fig, ax = plt.subplots(figsize=(9.0, 5.5))
    O = np.array([0.8, 1.0])
    end = O + np.array([r, 0.0])
    ax.plot([O[0], end[0]], [O[1], end[1]], color=F.BLUE, lw=5, solid_capstyle="round")
    ax.scatter([O[0]], [O[1]], color=F.INK, s=90, zorder=4)
    _arrow2(ax, end, end + force*np.array([np.cos(np.deg2rad(theta_deg)), np.sin(np.deg2rad(theta_deg))]), color=F.RED)
    ax.add_patch(Arc(end, 1.3, 1.3, theta1=0, theta2=theta_deg, color=F.AMBER, lw=1.8))
    ax.text(end[0] + 0.65, end[1] + 0.25, rf"${theta_deg}^\circ$", color=F.AMBER, fontsize=12)
    ax.text(2.8, 0.55, r"位置向量 $\vec r$", color=F.BLUE, ha="center", fontsize=12)
    ax.text(6.05, 2.75, r"施力 $\vec F$", color=F.RED, fontsize=12)
    ax.text(3.5, 4.1, r"$\vec\tau=\vec r\times\vec F,\quad |\tau|=rF\sin\theta$", ha="center", fontsize=14)
    ax.text(3.5, 3.55, "只有垂直於槓桿的分力造成轉動", ha="center", fontsize=12)
    ax.set_xlim(0, 7.2)
    ax.set_ylim(0, 4.7)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("外積在力矩中同時記錄轉動強度與轉軸方向", fontsize=15)
    fig.tight_layout()
    return _save(fig, "數A4-1-力矩模型.svg")


if __name__ == "__main__":
    for entrypoint, _ in FIGURE_OUTPUTS:
        globals()[entrypoint]()
