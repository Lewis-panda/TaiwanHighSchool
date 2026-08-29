# -*- coding: utf-8 -*-
"""重生「數A4-2 空間中的平面與直線」學生講義的章內 SVG。"""

if __name__ == "__main__" and __import__("sys").argv[1:]:
    raise SystemExit("本腳本不接受參數；直接執行即可重生數A4-2章內 SVG。")

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Arc, FancyArrowPatch, Polygon, Rectangle
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

import figlib as F


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHAPTER = os.path.join(ROOT, "content", "數學A", "數A4-2")

FIGURE_OUTPUTS = (
    ("fig_plane_normal", "數A4-2-點法式與法向量.svg"),
    ("fig_intercept_plane", "數A4-2-截距式.svg"),
    ("fig_plane_angle", "數A4-2-兩平面夾角.svg"),
    ("fig_point_plane_distance", "數A4-2-點到平面距離.svg"),
    ("fig_parallel_planes", "數A4-2-平行平面距離.svg"),
    ("fig_parametric_line", "數A4-2-直線參數式.svg"),
    ("fig_two_plane_line", "數A4-2-兩面交線.svg"),
    ("fig_line_plane_relations", "數A4-2-直線與平面關係.svg"),
    ("fig_plane_reflection", "數A4-2-平面投影與對稱.svg"),
    ("fig_line_plane_angle", "數A4-2-直線與平面夾角.svg"),
    ("fig_line_relations", "數A4-2-兩直線判別.svg"),
    ("fig_point_line_distance", "數A4-2-點到直線距離.svg"),
    ("fig_skew_distance", "數A4-2-歪斜線距離.svg"),
)


def _save(fig, filename):
    stem, extension = os.path.splitext(filename)
    if extension != ".svg" or not stem.startswith("數A4-2-"):
        raise AssertionError("輸出檔名必須是數A4-2章內 SVG")
    if any(getattr(ax, "name", "") == "3d" for ax in fig.axes):
        with plt.rc_context({"savefig.bbox": None}):
            return F.save_to(fig, CHAPTER, stem, output_subdir="assets", write_pdf=False)
    return F.save_to(fig, CHAPTER, stem, output_subdir="assets", write_pdf=False)


def _view_direction(elev, azim):
    elev_rad = np.deg2rad(elev)
    azim_rad = np.deg2rad(azim)
    return np.array([
        np.cos(elev_rad) * np.cos(azim_rad),
        np.cos(elev_rad) * np.sin(azim_rad),
        np.sin(elev_rad),
    ])


def _assert_plane_projection(normal, elev, azim, min_facing=0.25, max_facing=0.92):
    """確保平面在正交投影中有足夠面積，同時保留法向量的可見長度。"""
    unit_normal = np.asarray(normal, dtype=float)
    unit_normal /= np.linalg.norm(unit_normal)
    facing = abs(unit_normal @ _view_direction(elev, azim))
    assert min_facing <= facing <= max_facing, (
        f"平面投影退化：facing={facing:.3f}, elev={elev}, azim={azim}"
    )


def _style_3d(
    ax,
    limits=(-1.0, 4.5),
    aspect=(1, 1, 0.85),
    *,
    elev=24,
    azim=-57,
    plane_normals=(),
):
    for normal in plane_normals:
        _assert_plane_projection(normal, elev, azim)
    ax.set_xlim(*limits)
    ax.set_ylim(*limits)
    ax.set_zlim(*limits)
    ax.set_box_aspect(aspect)
    ax.set_proj_type("ortho")
    ax.view_init(elev=elev, azim=azim)
    ax.computed_zorder = False
    ax.set_axis_off()


def _right_angle_3d(ax, vertex, direction_a, direction_b, size=0.30):
    a = np.asarray(direction_a, dtype=float)
    b = np.asarray(direction_b, dtype=float)
    a /= np.linalg.norm(a)
    b /= np.linalg.norm(b)
    assert np.isclose(a @ b, 0, atol=1e-10)
    vertex = np.asarray(vertex, dtype=float)
    marker = np.array([
        vertex + size * a,
        vertex + size * (a + b),
        vertex + size * b,
    ])
    ax.plot(*marker.T, color=F.INK, lw=1.5)


def _arrow2(ax, start, end, color=F.BLUE, lw=2.3):
    patch = FancyArrowPatch(start, end, arrowstyle="-|>", mutation_scale=16,
                            linewidth=lw, color=color, shrinkA=0, shrinkB=0)
    ax.add_patch(patch)
    return patch


def fig_plane_normal():
    # 以平面 E 的局部基底作圖；畫面中的 x_E、y_E 不是全域坐標軸。
    # 讓其中一個面內方向與法向量同在投影面上，直角因此能在圖上精確呈現。
    origin = np.array([0.85, 1.05])
    screen_basis = np.array([
        [1.58, 0.00],  # x_E：平面內水平方向
        [0.52, 0.56],  # y_E：平面內深度方向
        [0.00, 1.30],  # n：由平面向上
    ])

    def project(point):
        return origin + np.asarray(point, dtype=float) @ screen_basis

    A = np.array([1.55, 1.25, 0.0])
    X = np.array([3.30, 1.25, 0.0])
    n = np.array([0.0, 0.0, 2.75])
    AX = X - A
    assert np.isclose(n @ AX, 0)

    plane_local = np.array([
        [0.0, 0.0, 0.0],
        [4.0, 0.0, 0.0],
        [4.0, 3.0, 0.0],
        [0.0, 3.0, 0.0],
    ])
    plane_screen = np.array([project(point) for point in plane_local])
    A_screen = project(A)
    X_screen = project(X)
    n_tip = project(A + n)

    fig, ax = plt.subplots(figsize=(9.2, 6.4))
    ax.add_patch(Polygon(
        plane_screen,
        closed=True,
        facecolor="#e5f0ff",
        edgecolor="#6f98c5",
        linewidth=1.8,
        alpha=0.90,
        zorder=1,
    ))

    axis_color = "#64748b"
    x_axis_end = project([0.88, 0.0, 0.0])
    y_axis_end = project([0.0, 0.88, 0.0])
    for end in (x_axis_end, y_axis_end):
        ax.add_patch(FancyArrowPatch(
            origin,
            end,
            arrowstyle="-|>",
            mutation_scale=14,
            linewidth=1.55,
            color=axis_color,
            zorder=3,
        ))
    ax.text(*(x_axis_end + np.array([0.07, -0.20])), r"$x_E$", color=axis_color, fontsize=11.5)
    ax.text(*(y_axis_end + np.array([0.07, 0.07])), r"$y_E$", color=axis_color, fontsize=11.5)

    _arrow2(ax, A_screen, X_screen, color=F.GREEN, lw=2.7).set_zorder(5)
    _arrow2(ax, A_screen, n_tip, color=F.RED, lw=2.9).set_zorder(5)
    ax.scatter(*A_screen, color=F.INK, s=68, zorder=7)
    ax.scatter(*X_screen, color=F.GREEN, s=58, zorder=7)

    marker_size = 0.34
    marker = np.array([
        A_screen + [marker_size, 0.0],
        A_screen + [marker_size, marker_size],
        A_screen + [0.0, marker_size],
    ])
    ax.plot(marker[:, 0], marker[:, 1], color=F.INK, lw=1.55, zorder=6)

    label_box = {"facecolor": "white", "edgecolor": "none", "alpha": 0.88, "pad": 0.8}
    ax.text(*(A_screen + np.array([-0.28, -0.36])), "A", fontsize=12, bbox=label_box, zorder=8)
    ax.text(*(X_screen + np.array([0.10, -0.34])), "X", color=F.GREEN, fontsize=12, bbox=label_box, zorder=8)
    ax.text(*(0.5 * (A_screen + X_screen) + np.array([0.0, -0.38])),
            r"$\overrightarrow{AX}$（平面內位移）", color=F.GREEN, fontsize=11,
            ha="center", bbox=label_box, zorder=8)
    ax.text(*(A_screen + np.array([0.18, 2.15])),
            r"法向量 $\vec n=(a,b,c)$", color=F.RED, fontsize=11,
            bbox=label_box, zorder=8)
    ax.text(*(plane_screen[2] + np.array([-0.40, -0.34])), "平面 E", color=F.BLUE,
            fontsize=11, bbox=label_box, zorder=8)

    ax.set_xlim(0.35, 9.25)
    ax.set_ylim(0.45, 6.20)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("平面內位移與法向量垂直", fontsize=15, pad=12)
    fig.tight_layout()
    return _save(fig, "數A4-2-點法式與法向量.svg")


def fig_intercept_plane():
    X = np.array([3.0, 0.0, 0.0])
    Y = np.array([0.0, 4.0, 0.0])
    Z = np.array([0.0, 0.0, 2.0])
    assert np.isclose(X[0]/3 + X[1]/4 + X[2]/2, 1)
    assert np.isclose(Y[0]/3 + Y[1]/4 + Y[2]/2, 1)
    assert np.isclose(Z[0]/3 + Z[1]/4 + Z[2]/2, 1)
    fig = plt.figure(figsize=(9.0, 6.4))
    ax = fig.add_subplot(111, projection="3d")
    ax.add_collection3d(Poly3DCollection(
        [[X, Y, Z]], facecolors="#e2f3e7", edgecolors=F.INK,
        linewidths=1.6, alpha=0.42,
    ))
    O = np.zeros(3)
    for end, color, label in ((np.array([4.2,0,0]), F.BLUE, "x"),
                              (np.array([0,4.2,0]), F.GREEN, "y"),
                              (np.array([0,0,4.2]), F.RED, "z")):
        ax.quiver(*O, *end, color=color, arrow_length_ratio=0.08, lw=2.0)
        ax.text(*(1.04*end), label, color=color, fontsize=12)
    label_box = {"facecolor": "white", "edgecolor": "none", "alpha": 0.84, "pad": 0.7}
    for point, label, offset in (
        (X, "(3,0,0)", np.array([0.12, -0.18, 0.18])),
        (Y, "(0,4,0)", np.array([-0.25, 0.08, 0.18])),
        (Z, "(0,0,2)", np.array([0.12, 0.12, 0.18])),
    ):
        ax.scatter(*point, color=F.AMBER, s=55, depthshade=False)
        ax.text(*(point + offset), label, fontsize=10, bbox=label_box)
    ax.text2D(0.08, 0.78, r"$\dfrac{x}{3}+\dfrac{y}{4}+\dfrac{z}{2}=1$", transform=ax.transAxes, fontsize=14)
    _style_3d(ax, (0, 4.5), plane_normals=((1/3, 1/4, 1/2),))
    ax.set_title("截距式直接標出平面與三條坐標軸的交點", fontsize=15)
    fig.tight_layout()
    return _save(fig, "數A4-2-截距式.svg")


def fig_plane_angle():
    theta = np.deg2rad(55)
    n1 = np.array([0.0, 1.0, 0.0])
    n2 = np.array([0.0, np.cos(theta), np.sin(theta)])
    assert np.isclose(n1 @ n2, np.cos(theta))
    x = np.array([-2.0, 2.0, 2.0, -2.0])
    p1 = [np.array([xv, 0.0, z]) for xv, z in zip(x, [-1.6,-1.6,1.6,1.6])]
    direction2 = np.array([0.0, -np.sin(theta), np.cos(theta)])
    p2 = [np.array([xv, 0.0, 0.0]) + s*direction2
          for xv, s in zip(x, [-1.6,-1.6,1.6,1.6])]
    fig = plt.figure(figsize=(9.2, 6.6))
    ax = fig.add_subplot(111, projection="3d")
    ax.add_collection3d(Poly3DCollection([p1], facecolors="#dfeeff", edgecolors=F.BLUE, alpha=0.55))
    ax.add_collection3d(Poly3DCollection([p2], facecolors="#e2f3e7", edgecolors=F.GREEN, alpha=0.55))
    ax.plot([-2.4,2.4],[0,0],[0,0], color=F.INK, lw=2.4)
    origin = np.zeros(3)
    tip1 = 2.2 * n1
    tip2 = 2.2 * n2
    ax.quiver(*origin, *tip1, color=F.BLUE, arrow_length_ratio=0.1, lw=3.0)
    ax.quiver(*origin, *tip2, color=F.RED, arrow_length_ratio=0.1, lw=3.2)
    ax.scatter(*tip1, marker="o", s=52, facecolor="white", edgecolor=F.BLUE,
               linewidth=1.8, depthshade=False)
    ax.scatter(*tip2, marker="^", s=62, facecolor="white", edgecolor=F.RED,
               linewidth=1.8, depthshade=False)
    label_box = {"facecolor": "white", "edgecolor": "none", "alpha": 0.82, "pad": 0.8}
    ax.text(0.1, 1.6, 0.1, r"$\vec n_1$（圓點）", color=F.INK, fontsize=12,
            bbox=label_box)
    ax.text(0.1, 1.0, 1.6, r"$\vec n_2$（三角）", color=F.INK, fontsize=12,
            bbox=label_box)
    arc_angle = np.linspace(0, theta, 60)
    arc = 0.82 * np.column_stack((
        np.zeros_like(arc_angle),
        np.cos(arc_angle),
        np.sin(arc_angle),
    ))
    ax.plot(*arc.T, color=F.AMBER, lw=2.1)
    ax.text(*(arc[len(arc)//2] + np.array([0.04, 0.04, 0.04])), r"$\theta$", color=F.AMBER, fontsize=12)
    ax.text2D(
        0.03, 0.77,
        r"$\cos\theta=\dfrac{|\vec n_1\cdot\vec n_2|}{|\vec n_1||\vec n_2|}$",
        transform=ax.transAxes,
        fontsize=13,
    )
    _style_3d(ax, (-2.8, 3.0), elev=25, azim=35, plane_normals=(n1, n2))
    ax.set_title("兩平面的銳夾角等於兩法向量的銳夾角", fontsize=15)
    inset = fig.add_axes([0.71, 0.11, 0.23, 0.25])
    origin2 = np.array([0.0, 0.0])
    tip1_2d = np.array([1.0, 0.0])
    tip2_2d = np.array([np.cos(theta), np.sin(theta)])
    assert np.isclose(tip1_2d @ tip2_2d, np.cos(theta))
    _arrow2(inset, origin2, tip1_2d, color=F.BLUE, lw=2.1)
    _arrow2(inset, origin2, tip2_2d, color=F.RED, lw=2.1)
    inset.add_patch(Arc(origin2, 0.86, 0.86, theta1=0, theta2=np.degrees(theta), color=F.AMBER, lw=1.8))
    inset.text(0.62, -0.17, r"$\vec n_1$", color=F.BLUE, fontsize=10)
    inset.text(0.30, 0.72, r"$\vec n_2$", color=F.RED, fontsize=10)
    inset.text(0.45, 0.18, r"$\theta$", color=F.AMBER, fontsize=10)
    inset.set_title("法向量剖面", fontsize=10)
    inset.set_xlim(-0.12, 1.18); inset.set_ylim(-0.22, 1.10)
    inset.set_aspect("equal"); inset.axis("off")
    fig.subplots_adjust(left=0.03, right=0.97, bottom=0.04, top=0.90)
    return _save(fig, "數A4-2-兩平面夾角.svg")


def fig_point_plane_distance():
    P = np.array([2.4, 2.0, 3.2])
    Q = np.array([2.4, 2.0, 0.0])
    assert np.isclose(np.linalg.norm(P-Q), 3.2)
    plane = [[(0,0,0),(4.5,0,0),(4.5,4.2,0),(0,4.2,0)]]
    fig = plt.figure(figsize=(9.0, 6.4))
    ax = fig.add_subplot(111, projection="3d")
    ax.add_collection3d(Poly3DCollection(plane, facecolors="#e5f0ff", edgecolors="#6f98c5", alpha=0.72))
    ax.plot(*np.array([P,Q]).T, color=F.RED, lw=2.7)
    ax.scatter(*P, color=F.AMBER, s=65, depthshade=False)
    ax.scatter(*Q, color=F.INK, s=55, depthshade=False)
    ax.text(*(P + np.array([0.1,0.1,0.12])), "P", fontsize=12)
    ax.text(*(Q + np.array([0.12,0.12,0.12])), "Q", fontsize=12)
    ax.text(2.65, 2.0, 1.6, "法向距離", color=F.RED, fontsize=11)
    _right_angle_3d(ax, Q, (1, 0, 0), (0, 0, 1), size=0.30)
    ax.text2D(
        0.04, 0.78,
        r"$d=\dfrac{|ax_0+by_0+cz_0+d_0|}{\sqrt{a^2+b^2+c^2}}$",
        transform=ax.transAxes,
        fontsize=13,
    )
    _style_3d(ax, (0, 4.6), plane_normals=((0, 0, 1),))
    ax.set_title("點到平面的最短路徑沿法向量", fontsize=15)
    fig.tight_layout()
    return _save(fig, "數A4-2-點到平面距離.svg")


def fig_parallel_planes():
    lower = [[(0,0,1),(4,0,1),(4,4,1),(0,4,1)]]
    upper = [[(0,0,3),(4,0,3),(4,4,3),(0,4,3)]]
    fig = plt.figure(figsize=(9.0, 6.5))
    ax = fig.add_subplot(111, projection="3d")
    ax.add_collection3d(Poly3DCollection(lower, facecolors="#dfeeff", edgecolors=F.BLUE, alpha=0.55))
    ax.add_collection3d(Poly3DCollection(upper, facecolors="#e2f3e7", edgecolors=F.GREEN, alpha=0.55))
    A = np.array([2.0,2.0,1.0]); B = np.array([2.0,2.0,3.0])
    ax.plot(*np.array([A,B]).T, color=F.RED, lw=2.7)
    ax.scatter(*A, color=F.INK, s=40, depthshade=False); ax.scatter(*B, color=F.INK, s=40, depthshade=False)
    label_box = {"facecolor": "white", "edgecolor": "none", "alpha": 0.88, "pad": 0.8}
    ax.text(2.45,1.25,2.05,"共同法向距離", color=F.RED, fontsize=11, bbox=label_box)
    ax.text(0.15,0.15,0.78,r"$E_1:ax+by+cz+d_1=0$", fontsize=11, bbox=label_box)
    ax.text(0.2,3.8,3.18,r"$E_2:ax+by+cz+d_2=0$", fontsize=11, bbox=label_box)
    assert np.isclose(np.linalg.norm(B-A), 2.0)
    _right_angle_3d(ax, A, (1, 0, 0), (0, 0, 1), size=0.26)
    _right_angle_3d(ax, B, (1, 0, 0), (0, 0, -1), size=0.26)
    _style_3d(ax, (0,4.5), plane_normals=((0, 0, 1), (0, 0, 1)))
    ax.set_title("平行平面的距離沿共同法向量量測", fontsize=15)
    fig.tight_layout()
    return _save(fig, "數A4-2-平行平面距離.svg")


def fig_parametric_line():
    A = np.array([1.0,1.0,1.0]); d = np.array([1.8,0.9,1.2])
    ts = np.array([-0.5,0.0,0.8,1.5])
    pts = A + ts[:,None]*d
    assert np.allclose(pts[2], A + 0.8*d)
    fig = plt.figure(figsize=(9.2,6.4))
    ax = fig.add_subplot(111, projection="3d")
    grid = np.linspace(-0.8,1.8,30)
    line = A + grid[:,None]*d
    ax.plot(*line.T, color=F.BLUE, lw=2.7)
    colors = [F.PURPLE,F.GREEN,F.AMBER,F.RED]
    label_box = {"facecolor": "white", "edgecolor": "none", "alpha": 0.82, "pad": 0.6}
    for t,p,c in zip(ts,pts,colors):
        ax.scatter(*p,color=c,s=55,depthshade=False)
        label = r"$A\;(t=0)$" if np.isclose(t, 0) else rf"$t={t:g}$"
        ax.text(*(p+np.array([0.08,0.08,0.1])),label,color=c,fontsize=10,bbox=label_box)
    direction_start = A + 0.12*d
    direction = 0.62*d
    ax.quiver(*direction_start,*direction,color=F.GREEN,arrow_length_ratio=0.16,lw=2.5)
    ax.text(*(direction_start + 0.58*direction + np.array([0.05, 0.05, 0.10])), r"$\vec d$", color=F.GREEN, fontsize=12, bbox=label_box)
    ax.text2D(0.08,0.78,r"$X=A+t\vec d$",transform=ax.transAxes,fontsize=15)
    _style_3d(ax, (-1.0,5.0))
    ax.set_title("參數 $t$ 改變時，點沿固定方向向量在直線上移動", fontsize=15)
    fig.tight_layout()
    return _save(fig, "數A4-2-直線參數式.svg")


def fig_two_plane_line():
    plane1 = [[(-2,-2,0),(2,-2,0),(2,2,0),(-2,2,0)]]
    plane2 = [[(-2,0,-2),(2,0,-2),(2,0,2),(-2,0,2)]]
    n1=np.array([0,0,1.0]); n2=np.array([0,1.0,0]); d=np.cross(n1,n2)
    assert np.allclose(np.abs(d),np.array([1,0,0]))
    fig=plt.figure(figsize=(9.0,6.5)); ax=fig.add_subplot(111,projection="3d")
    ax.add_collection3d(Poly3DCollection(plane1,facecolors="#dfeeff",edgecolors=F.BLUE,alpha=0.55))
    ax.add_collection3d(Poly3DCollection(plane2,facecolors="#e2f3e7",edgecolors=F.GREEN,alpha=0.55))
    ax.plot([-2.5,2.5],[0,0],[0,0],color=F.RED,lw=3.0)
    ax.quiver(2.3,0,0,-4.6,0,0,color=F.RED,arrow_length_ratio=0.08,lw=2.8)
    origin = np.zeros(3)
    ax.quiver(*origin,*n1,color=F.BLUE,arrow_length_ratio=0.16,lw=2.4)
    ax.quiver(*origin,*n2,color=F.GREEN,arrow_length_ratio=0.16,lw=2.4)
    label_box = {"facecolor": "white", "edgecolor": "none", "alpha": 0.84, "pad": 0.8}
    ax.text(1.1,0.15,0.15,r"交線方向 $\vec n_1\times\vec n_2$",color=F.RED,fontsize=11,bbox=label_box)
    ax.text(0.08,0.08,0.72,r"$\vec n_1$",color=F.BLUE,fontsize=11,bbox=label_box)
    ax.text(0.08,0.72,0.08,r"$\vec n_2$",color=F.GREEN,fontsize=11,bbox=label_box)
    ax.text(-1.9,1.6,0.1,r"$E_1$",color=F.BLUE,fontsize=12)
    ax.text(-1.9,0.1,1.7,r"$E_2$",color=F.GREEN,fontsize=12)
    _style_3d(ax,(-2.8,3.0),elev=28,azim=-35,plane_normals=(n1,n2))
    ax.set_title("兩相交平面的公共點形成直線，方向垂直兩個法向量",fontsize=15)
    fig.tight_layout()
    return _save(fig,"數A4-2-兩面交線.svg")


def fig_line_plane_relations():
    fig,axes=plt.subplots(1,3,figsize=(11.0,4.3))
    cases=(("相交：一個參數解","intersect"),("平行：沒有參數解","parallel"),("包含：所有參數皆成立","contained"))
    plane=np.array([[0.5,0.8],[4.5,0.8],[5.2,2.7],[1.2,2.7]])
    for ax,(title,kind) in zip(axes,cases):
        ax.add_patch(Polygon(plane,closed=True,facecolor="#e5f0ff",edgecolor="#6f98c5",lw=1.5))
        if kind=="intersect":
            intersection_x, intersection_y = 2.8, 1.9
            lower_x, upper_x = 2.17, 3.50
            ax.plot([lower_x,intersection_x],[0.1,intersection_y],
                    color=F.RED,lw=2.5,ls=(0,(4,3)),dash_capstyle="round",zorder=3)
            ax.plot([intersection_x,upper_x],[intersection_y,3.9],
                    color=F.RED,lw=2.5,solid_capstyle="round",zorder=3)
            ax.scatter([intersection_x],[intersection_y],color=F.AMBER,s=55,zorder=4)
            ax.text(intersection_x+0.18,intersection_y+0.08,"交點",fontsize=10,zorder=5)
        elif kind=="parallel":
            ax.plot([1.0,4.8],[3.35,3.35],color=F.GREEN,lw=2.5)
        else:
            ax.plot([1.1,4.7],[1.25,2.2],color=F.BLUE,lw=2.5)
        ax.set_title(title,fontsize=11)
        ax.set_xlim(0,5.6); ax.set_ylim(0,4.1); ax.set_aspect("equal"); ax.axis("off")
    fig.suptitle("把直線參數式代入平面方程式，解的個數就是幾何交集",fontsize=15)
    fig.tight_layout(rect=(0,0,1,0.9))
    return _save(fig,"數A4-2-直線與平面關係.svg")


def fig_plane_reflection():
    P=np.array([2.0,2.0,2.6]); Q=np.array([2.0,2.0,0.0]); R=np.array([2.0,2.0,-2.6])
    assert np.allclose(Q,(P+R)/2)
    plane=[[(0,0,0),(4,0,0),(4,4,0),(0,4,0)]]
    fig=plt.figure(figsize=(9.0,6.5)); ax=fig.add_subplot(111,projection="3d")
    ax.add_collection3d(Poly3DCollection(plane,facecolors="#e5f0ff",edgecolors="#6f98c5",alpha=0.65))
    ax.plot(*np.array([P,R]).T,color=F.RED,lw=2.4,ls="--")
    label_box = {"facecolor": "white", "edgecolor": "none", "alpha": 0.84, "pad": 0.7}
    point_labels = (
        (P,"P",F.AMBER,np.array([0.18,0.12,0.18])),
        (Q,"Q",F.INK,np.array([0.35,0.18,0.08])),
        (R,"P'",F.PURPLE,np.array([0.22,0.14,-0.14])),
    )
    for point,label,color,offset in point_labels:
        ax.scatter(*point,color=color,s=60,depthshade=False)
        ax.text(*(point+offset),label,color=color,fontsize=12,bbox=label_box)
    ax.text(2.35,2.12,1.35,"PQ",color=F.RED,fontsize=11)
    ax.text(2.35,2.12,-1.35,"QP'",color=F.RED,fontsize=11)
    for z in (1.3, -1.3):
        ax.plot([1.84,2.16],[2.0,2.0],[z,z],color=F.RED,lw=2.0)
    _right_angle_3d(ax, Q, (1, 0, 0), (0, 0, 1), size=0.28)
    _style_3d(ax,(-3.0,4.5),plane_normals=((0,0,1),))
    ax.set_title("投影點是原點與平面對稱點的中點",fontsize=15)
    fig.tight_layout()
    return _save(fig,"數A4-2-平面投影與對稱.svg")


def fig_line_plane_angle():
    d=np.array([3.6,0.0,2.4]); proj=np.array([3.6,0.0,0.0])
    theta=np.arctan2(d[2],np.linalg.norm(proj))
    assert np.isclose(np.sin(theta),d[2]/np.linalg.norm(d))
    plane=[[(0,-1,0),(4.7,-1,0),(4.7,2.8,0),(0,2.8,0)]]
    fig=plt.figure(figsize=(9.0,6.4)); ax=fig.add_subplot(111,projection="3d")
    ax.add_collection3d(Poly3DCollection(plane,facecolors="#e5f0ff",edgecolors="#6f98c5",alpha=0.68))
    O=np.array([0.4,0.4,0.0]); ax.quiver(*O,*d,color=F.BLUE,arrow_length_ratio=0.09,lw=2.6)
    ax.quiver(*O,*proj,color=F.GREEN,arrow_length_ratio=0.09,lw=2.3)
    ax.plot(*np.array([O+d,O+proj]).T,color=F.RED,lw=1.8,ls="--")
    normal_base=np.array([0.9,2.0,0.0]); normal=np.array([0.0,0.0,1.7])
    ax.quiver(*normal_base,*normal,color=F.RED,arrow_length_ratio=0.13,lw=2.3)
    ax.text(2.2,0.55,1.55,r"直線方向 $\vec d$",color=F.BLUE,fontsize=11)
    ax.text(2.0,0.1,0.15,"平面投影",color=F.GREEN,fontsize=11)
    ax.text(4.15,0.15,1.15,"法向分量",color=F.RED,fontsize=11)
    ax.text(*(normal_base+0.72*normal+np.array([0.08,0.05,0.0])),r"法向量 $\vec n$",color=F.RED,fontsize=11)
    _right_angle_3d(ax,normal_base,(1,0,0),normal,size=0.26)
    angle_values = np.linspace(0, theta, 50)
    arc = O + 0.85*np.column_stack((
        np.cos(angle_values),
        np.zeros_like(angle_values),
        np.sin(angle_values),
    ))
    ax.plot(*arc.T,color=F.AMBER,lw=2.2)
    ax.text(*(arc[len(arc)//2] + np.array([0.05,0.04,0.05])),r"$\theta$",color=F.AMBER,fontsize=12)
    _right_angle_3d(ax, O+proj, (-1,0,0), (0,0,1), size=0.28)
    ax.text2D(
        0.04,0.78,
        r"$\sin\theta=\dfrac{|\vec d\cdot\vec n|}{|\vec d||\vec n|}$",
        transform=ax.transAxes,
        fontsize=13,
    )
    _style_3d(ax,(0,4.8),plane_normals=((0,0,1),))
    ax.set_title("線面角由直線方向在法向量上的分量決定",fontsize=15)
    fig.tight_layout()
    return _save(fig,"數A4-2-直線與平面夾角.svg")


def fig_line_relations():
    fig,axes=plt.subplots(2,2,figsize=(9.8,7.0))
    cases=(("重合：方向平行且有共同點","same"),("平行：方向平行且無共同點","parallel"),
           ("相交：方向不平行且聯立有解","intersect"),("歪斜：方向不平行且聯立無解","skew"))
    for ax,(title,kind) in zip(axes.flat,cases):
        if kind=="same":
            ax.plot([0.8,5.0],[1.0,3.3],color=F.BLUE,lw=4.0)
            ax.plot([1.4,4.3],[1.33,2.92],color=F.GREEN,lw=1.5,ls="--")
        elif kind=="parallel":
            ax.plot([0.8,4.8],[1.0,2.1],color=F.BLUE,lw=2.5)
            ax.plot([1.1,5.1],[2.2,3.3],color=F.GREEN,lw=2.5)
        elif kind=="intersect":
            p1=np.array([0.8,0.9]); p2=np.array([5.0,3.4])
            q1=np.array([0.9,3.3]); q2=np.array([4.9,1.0])
            parameters=np.linalg.solve(
                np.column_stack((p2-p1,-(q2-q1))),
                q1-p1,
            )
            intersection=p1+parameters[0]*(p2-p1)
            assert np.allclose(intersection,q1+parameters[1]*(q2-q1))
            ax.plot([p1[0],p2[0]],[p1[1],p2[1]],color=F.BLUE,lw=2.5)
            ax.plot([q1[0],q2[0]],[q1[1],q2[1]],color=F.RED,lw=2.5)
            ax.scatter([intersection[0]],[intersection[1]],color=F.AMBER,s=50,zorder=4)
        else:
            plane=np.array([[0.6,0.6],[4.4,0.6],[5.1,2.0],[1.3,2.0]])
            ax.add_patch(Polygon(plane,closed=True,facecolor="#eef4fa",edgecolor="#9bb0c5"))
            ax.plot([0.9,4.7],[0.9,1.65],color=F.BLUE,lw=2.5)
            ax.plot([1.8,4.8],[3.5,2.65],color=F.RED,lw=2.5)
            ax.text(4.85,3.38,"不同平面",color=F.RED,fontsize=10,ha="right")
        ax.set_title(title,fontsize=11)
        ax.set_xlim(0.3,5.5); ax.set_ylim(0.3,3.8); ax.set_aspect("equal"); ax.axis("off")
    fig.suptitle("方向向量先分流，再由參數聯立判斷共同點",fontsize=15)
    fig.tight_layout(rect=(0,0,1,0.93))
    return _save(fig,"數A4-2-兩直線判別.svg")


def fig_point_line_distance():
    A=np.array([0.8,0.9]); d=np.array([4.5,1.0]); P=np.array([3.4,3.8])
    t=(P-A)@d/(d@d); H=A+t*d
    assert np.isclose((P-H)@d,0)
    fig,ax=plt.subplots(figsize=(8.8,5.2))
    line=np.array([A-0.15*d,A+1.15*d]); ax.plot(line[:,0],line[:,1],color=F.BLUE,lw=2.6)
    direction_start=A+0.12*d; direction_end=A+0.48*d
    _arrow2(ax,direction_start,direction_end,color=F.GREEN,lw=2.2)
    ax.plot([P[0],H[0]],[P[1],H[1]],color=F.RED,lw=2.4,ls="--")
    ax.scatter([P[0],H[0],A[0]],[P[1],H[1],A[1]],color=[F.AMBER,F.INK,F.GREEN],s=60)
    ax.text(P[0]+0.1,P[1]+0.1,"P",fontsize=12); ax.text(H[0]+0.1,H[1]-0.35,"H",fontsize=12)
    ax.text(A[0]-0.25,A[1]-0.35,"A",color=F.GREEN,fontsize=12)
    ax.text(*(direction_start+0.54*(direction_end-direction_start)+np.array([0.0,0.25])),r"$\vec d$",color=F.GREEN,fontsize=12)
    ax.text(2.7,2.5,r"$\overrightarrow{PH}\perp\vec d$",color=F.RED,fontsize=12)
    ax.text(3.0,4.55,r"$H=A+\dfrac{\overrightarrow{AP}\cdot\vec d}{|\vec d|^2}\vec d$",ha="center",fontsize=13)
    ax.set_xlim(0,6); ax.set_ylim(0,5); ax.set_aspect("equal"); ax.axis("off")
    ax.set_title("點到直線的距離是扣除平行投影後的垂直分量",fontsize=15)
    fig.tight_layout()
    return _save(fig,"數A4-2-點到直線距離.svg")


def fig_skew_distance():
    p1=np.array([-1.5,0.0,0.0]); d1=np.array([4.5,0.0,0.0])
    p2=np.array([1.0,-1.5,2.2]); d2=np.array([0.0,4.5,0.0])
    A=np.array([1.0,0.0,0.0]); B=np.array([1.0,0.0,2.2]); common=B-A
    assert np.isclose(common@d1,0) and np.isclose(common@d2,0)
    fig=plt.figure(figsize=(9.0,6.5)); ax=fig.add_subplot(111,projection="3d")
    ax.plot(*np.array([p1,p1+d1]).T,color=F.BLUE,lw=2.8)
    ax.plot(*np.array([p2,p2+d2]).T,color=F.GREEN,lw=2.8)
    ax.plot(*np.array([A,B]).T,color=F.RED,lw=2.6,ls="--")
    ax.scatter(*A,color=F.INK,s=50,depthshade=False); ax.scatter(*B,color=F.INK,s=50,depthshade=False)
    ax.text(*(A+np.array([0.1,0.1,0.1])),"A",fontsize=11); ax.text(*(B+np.array([0.1,0.1,0.1])),"B",fontsize=11)
    ax.text(2.0,0.1,0.1,r"$L_1$",color=F.BLUE,fontsize=12)
    ax.text(1.1,2.2,2.25,r"$L_2$",color=F.GREEN,fontsize=12)
    ax.text(1.15,0.1,1.1,"公垂線段",color=F.RED,fontsize=11)
    _right_angle_3d(ax,A,(1,0,0),(0,0,1),size=0.25)
    _right_angle_3d(ax,B,(0,1,0),(0,0,-1),size=0.25)
    ax.text2D(
        0.03,0.78,
        r"$d=\dfrac{|\overrightarrow{AB}\cdot(\vec d_1\times\vec d_2)|}{|\vec d_1\times\vec d_2|}$",
        transform=ax.transAxes,
        fontsize=12,
    )
    _style_3d(ax,(-2.0,4.2))
    ax.set_title("歪斜線的最短連線同時垂直兩條直線",fontsize=15)
    fig.tight_layout()
    return _save(fig,"數A4-2-歪斜線距離.svg")


if __name__ == "__main__":
    for entrypoint, _ in FIGURE_OUTPUTS:
        globals()[entrypoint]()
