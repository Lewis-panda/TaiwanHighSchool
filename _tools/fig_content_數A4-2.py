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
    return F.save_to(fig, CHAPTER, stem, output_subdir="assets", write_pdf=False)


def _style_3d(ax, limits=(-1.0, 4.5), aspect=(1, 1, 0.85)):
    ax.set_xlim(*limits)
    ax.set_ylim(*limits)
    ax.set_zlim(*limits)
    ax.set_box_aspect(aspect)
    ax.view_init(elev=24, azim=-57)
    ax.grid(False)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_zticks([])
    for axis in (ax.xaxis, ax.yaxis, ax.zaxis):
        axis.pane.set_alpha(0)


def _arrow2(ax, start, end, color=F.BLUE, lw=2.3):
    patch = FancyArrowPatch(start, end, arrowstyle="-|>", mutation_scale=16,
                            linewidth=lw, color=color, shrinkA=0, shrinkB=0)
    ax.add_patch(patch)
    return patch


def fig_plane_normal():
    A = np.array([2.0, 1.0, 1.0])
    n = np.array([1.0, 2.0, 2.0])
    u = np.array([2.0, -1.0, 0.0])
    v = np.array([2.0, 0.0, -1.0])
    B = A + 0.75 * u - 0.25 * v
    assert np.isclose(n @ (B - A), 0)
    assert np.isclose(n @ A, 6)
    vertices = [A - 0.8*u - 0.8*v, A + 0.8*u - 0.8*v,
                A + 0.8*u + 0.8*v, A - 0.8*u + 0.8*v]
    fig = plt.figure(figsize=(9.2, 6.6))
    ax = fig.add_subplot(111, projection="3d")
    ax.add_collection3d(Poly3DCollection([vertices], facecolors="#e5f0ff",
                                         edgecolors="#6f98c5", alpha=0.72))
    ax.scatter(*A, color=F.INK, s=65)
    ax.text(*(A + np.array([0.1, 0.1, 0.1])), "A", fontsize=12)
    ax.plot(*np.array([A, B]).T, color=F.GREEN, lw=2.4)
    ax.quiver(*A, *n, color=F.RED, arrow_length_ratio=0.09, lw=2.7)
    ax.text(*(A + 0.62*n), r"法向量 $\vec n=(a,b,c)$", color=F.RED, fontsize=11)
    ax.text(*(A + 0.55*(B-A) + np.array([0, 0, 0.12])), r"$\overrightarrow{AX}$", color=F.GREEN, fontsize=11)
    ax.text(-0.5, 3.8, 0.0, r"$\vec n\cdot\overrightarrow{AX}=0$", fontsize=13)
    _style_3d(ax, (-1.2, 4.8))
    ax.set_title("平面內位移都垂直法向量，形成點法式", fontsize=15)
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
    for point, label in ((X, "(3,0,0)"), (Y, "(0,4,0)"), (Z, "(0,0,2)")):
        ax.scatter(*point, color=F.AMBER, s=55)
        ax.text(*(point + np.array([0.08,0.08,0.12])), label, fontsize=10)
    ax.text(0.2, 3.7, 3.8, r"$\dfrac{x}{3}+\dfrac{y}{4}+\dfrac{z}{2}=1$", fontsize=14)
    _style_3d(ax, (0, 4.5))
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
    ax.text(-1.7, -2.4, 2.6, r"$\cos\theta=\dfrac{|\vec n_1\cdot\vec n_2|}{|\vec n_1||\vec n_2|}$", fontsize=13)
    _style_3d(ax, (-2.8, 3.0))
    ax.set_title("兩平面的銳夾角等於兩法向量的銳夾角", fontsize=15)
    fig.tight_layout()
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
    ax.scatter(*P, color=F.AMBER, s=65)
    ax.scatter(*Q, color=F.INK, s=55)
    ax.text(*(P + np.array([0.1,0.1,0.12])), "P", fontsize=12)
    ax.text(*(Q + np.array([0.12,0.12,0.12])), "Q", fontsize=12)
    ax.text(2.65, 2.0, 1.6, "最短距離", color=F.RED, fontsize=11)
    ax.text(0.1, 3.7, 3.8, r"$d=\dfrac{|ax_0+by_0+cz_0+d_0|}{\sqrt{a^2+b^2+c^2}}$", fontsize=13)
    _style_3d(ax, (0, 4.6))
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
    ax.scatter(*A, color=F.INK, s=40); ax.scatter(*B, color=F.INK, s=40)
    ax.text(2.2,2.1,2.0,"共同法向距離", color=F.RED, fontsize=11)
    ax.text(0.2,3.8,1.05,r"$E_1:ax+by+cz+d_1=0$", fontsize=11)
    ax.text(0.2,3.8,3.05,r"$E_2:ax+by+cz+d_2=0$", fontsize=11)
    assert np.isclose(np.linalg.norm(B-A), 2.0)
    _style_3d(ax, (0,4.5))
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
    for t,p,c in zip(ts,pts,colors):
        ax.scatter(*p,color=c,s=55)
        ax.text(*(p+np.array([0.08,0.08,0.1])),rf"$t={t:g}$",color=c,fontsize=10)
    ax.quiver(*A,*d,color=F.GREEN,arrow_length_ratio=0.1,lw=2.4)
    ax.text(-0.7,3.7,4.0,r"$X=A+t\vec d$",fontsize=15)
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
    ax.text(1.1,0.15,0.15,r"交線方向 $\vec n_1\times\vec n_2$",color=F.RED,fontsize=11)
    ax.text(-1.9,1.6,0.1,r"$E_1$",color=F.BLUE,fontsize=12)
    ax.text(-1.9,0.1,1.7,r"$E_2$",color=F.GREEN,fontsize=12)
    _style_3d(ax,(-2.8,3.0))
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
            ax.plot([2.8,2.8],[0.1,3.9],color=F.RED,lw=2.5)
            ax.scatter([2.8],[1.9],color=F.AMBER,s=55,zorder=4)
            ax.text(3.0,1.75,"交點",fontsize=10)
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
    for point,label,color in ((P,"P",F.AMBER),(Q,"Q",F.INK),(R,"P'",F.PURPLE)):
        ax.scatter(*point,color=color,s=60); ax.text(*(point+np.array([0.1,0.1,0.1])),label,color=color,fontsize=12)
    ax.text(2.2,2.1,1.2,"PQ",color=F.RED,fontsize=11)
    ax.text(2.2,2.1,-1.4,"QP'",color=F.RED,fontsize=11)
    _style_3d(ax,(-3.0,4.5))
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
    ax.text(2.2,0.55,1.55,r"直線方向 $\vec d$",color=F.BLUE,fontsize=11)
    ax.text(2.0,0.1,0.15,"平面投影",color=F.GREEN,fontsize=11)
    ax.text(0.1,2.5,4.0,r"$\sin\theta=\dfrac{|\vec d\cdot\vec n|}{|\vec d||\vec n|}$",fontsize=13)
    _style_3d(ax,(0,4.8))
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
            ax.plot([0.8,5.0],[0.9,3.4],color=F.BLUE,lw=2.5)
            ax.plot([0.9,4.9],[3.3,1.0],color=F.RED,lw=2.5)
            ax.scatter([2.95],[2.18],color=F.AMBER,s=50,zorder=4)
        else:
            plane=np.array([[0.6,0.6],[4.4,0.6],[5.1,2.0],[1.3,2.0]])
            ax.add_patch(Polygon(plane,closed=True,facecolor="#eef4fa",edgecolor="#9bb0c5"))
            ax.plot([0.9,4.7],[0.9,1.65],color=F.BLUE,lw=2.5)
            ax.plot([1.8,4.8],[3.5,2.65],color=F.RED,lw=2.5)
            ax.plot([1.8,1.8],[3.5,1.3],color=F.RED,lw=1.2,ls="--")
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
    ax.plot([P[0],H[0]],[P[1],H[1]],color=F.RED,lw=2.4,ls="--")
    ax.scatter([P[0],H[0],A[0]],[P[1],H[1],A[1]],color=[F.AMBER,F.INK,F.GREEN],s=60)
    ax.text(P[0]+0.1,P[1]+0.1,"P",fontsize=12); ax.text(H[0]+0.1,H[1]-0.35,"H",fontsize=12)
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
    ax.scatter(*A,color=F.INK,s=50); ax.scatter(*B,color=F.INK,s=50)
    ax.text(*(A+np.array([0.1,0.1,0.1])),"A",fontsize=11); ax.text(*(B+np.array([0.1,0.1,0.1])),"B",fontsize=11)
    ax.text(2.0,0.1,0.1,r"$L_1$",color=F.BLUE,fontsize=12)
    ax.text(1.1,2.2,2.25,r"$L_2$",color=F.GREEN,fontsize=12)
    ax.text(1.15,0.1,1.1,"公垂線段",color=F.RED,fontsize=11)
    ax.text(-1.2,3.5,3.8,r"$d=\dfrac{|\overrightarrow{P_1P_2}\cdot(\vec d_1\times\vec d_2)|}{|\vec d_1\times\vec d_2|}$",fontsize=12)
    _style_3d(ax,(-2.0,4.2))
    ax.set_title("歪斜線的最短連線同時垂直兩條直線",fontsize=15)
    fig.tight_layout()
    return _save(fig,"數A4-2-歪斜線距離.svg")


if __name__ == "__main__":
    for entrypoint, _ in FIGURE_OUTPUTS:
        globals()[entrypoint]()
