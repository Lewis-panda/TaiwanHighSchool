# -*- coding: utf-8 -*-
r"""產生「數A3-4 空間向量」的圖，輸出到該章 sources/。
重繪：  .venv/bin/python _tools/fig_數A3-4.py

本章多為 3D 幾何圖：fig.add_subplot(projection="3d")，
用 ax.quiver / ax.plot 畫向量與線；2D 示意（三垂線俯視、外積右手定則）用 F.schematic。
注意：mathtext 不支援 \dfrac/\tfrac；3D 圖內中文標籤不放 $...$。
"""

import os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Polygon, Arc
from mpl_toolkits.mplot3d import proj3d
import figlib as F

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CH = os.path.join(ROOT, "數學", "數學二上（數學A·第三冊）", "數A3-4 空間向量")


class Arrow3D(FancyArrowPatch):
    """3D 箭頭：給座標軸與向量用。"""

    def __init__(self, xs, ys, zs, *args, **kwargs):
        super().__init__((0, 0), (0, 0), *args, **kwargs)
        self._verts3d = xs, ys, zs

    def do_3d_projection(self, renderer=None):
        xs3d, ys3d, zs3d = self._verts3d
        xs, ys, _ = proj3d.proj_transform(xs3d, ys3d, zs3d, self.axes.M)
        self.set_positions((xs[0], ys[0]), (xs[1], ys[1]))
        return float(np.min(zs3d))


def _arrow3d(ax, p0, p1, color=F.INK, lw=2.2, mutation=14, z=5, ls="-"):
    a = Arrow3D(
        [p0[0], p1[0]],
        [p0[1], p1[1]],
        [p0[2], p1[2]],
        arrowstyle="-|>",
        mutation_scale=mutation,
        lw=lw,
        color=color,
        linestyle=ls,
        zorder=z,
    )
    ax.add_artist(a)
    return a


def _clean3d(ax):
    ax.grid(False)
    try:
        ax.xaxis.pane.set_visible(False)
        ax.yaxis.pane.set_visible(False)
        ax.zaxis.pane.set_visible(False)
    except Exception:
        pass
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_zticks([])


def _axes3d(ax, L=4.2):
    """畫過原點的 x, y, z 三軸（帶箭頭）。"""
    _arrow3d(ax, (0, 0, 0), (L, 0, 0), color=F.INK, lw=1.4, mutation=12, z=2)
    _arrow3d(ax, (0, 0, 0), (0, L, 0), color=F.INK, lw=1.4, mutation=12, z=2)
    _arrow3d(ax, (0, 0, 0), (0, 0, L), color=F.INK, lw=1.4, mutation=12, z=2)
    ax.text(L + 0.2, 0, 0, "x", color=F.INK, fontsize=12)
    ax.text(0, L + 0.2, 0, "y", color=F.INK, fontsize=12)
    ax.text(0, 0, L + 0.2, "z", color=F.INK, fontsize=12)


# ---------------------------------------------------------------------------
def fig_space_coords():
    """空間直角坐標系：原點、三軸、一點 P 及其投影、兩點距離。"""
    fig = plt.figure(figsize=(7.6, 6.2))
    ax = fig.add_subplot(111, projection="3d")
    _axes3d(ax, L=4.4)

    P = np.array([3.0, 2.5, 3.0])
    # 點 P
    ax.scatter([P[0]], [P[1]], [P[2]], color=F.RED, s=42, zorder=8)
    ax.text(
        P[0] + 0.15, P[1] + 0.1, P[2] + 0.25, "P(a, b, c)", color=F.RED, fontsize=12
    )

    # 投影虛線（投到 xy 平面，再投到各軸）
    Pxy = np.array([P[0], P[1], 0.0])
    ax.plot(
        [P[0], Pxy[0]], [P[1], Pxy[1]], [P[2], Pxy[2]], color=F.GREEN, lw=1.3, ls="--"
    )
    ax.plot([Pxy[0], P[0]], [Pxy[1], 0], [0, 0], color=F.GREEN, lw=1.1, ls="--")
    ax.plot([Pxy[0], 0], [Pxy[1], P[1]], [0, 0], color=F.GREEN, lw=1.1, ls="--")
    # 投影盒（虛線方框，標示 a, b, c）
    ax.plot([0, P[0]], [0, 0], [0, 0], color=F.BLUE, lw=1.0, ls=":")
    ax.plot([P[0], P[0]], [0, P[1]], [0, 0], color=F.BLUE, lw=1.0, ls=":")
    ax.scatter([Pxy[0]], [Pxy[1]], [0], color=F.GREEN, s=20)
    ax.text(
        Pxy[0] + 0.1,
        Pxy[1] + 0.1,
        -0.15,
        "P′（xy 平面投影）",
        color=F.GREEN,
        fontsize=10,
    )
    ax.text(P[0] / 2, -0.45, -0.1, "a", color=F.BLUE, fontsize=11)
    ax.text(P[0] + 0.15, P[1] / 2, -0.1, "b", color=F.BLUE, fontsize=11)
    ax.text(P[0] + 0.15, P[1] + 0.05, P[2] / 2, "c", color=F.GREEN, fontsize=11)

    # 第二點 Q 與兩點距離線
    Q = np.array([1.0, 3.6, 1.2])
    ax.scatter([Q[0]], [Q[1]], [Q[2]], color=F.PURPLE, s=40, zorder=8)
    ax.text(Q[0] - 0.2, Q[1] + 0.2, Q[2] + 0.2, "Q", color=F.PURPLE, fontsize=12)
    ax.plot([P[0], Q[0]], [P[1], Q[1]], [P[2], Q[2]], color=F.AMBER, lw=2.2)
    mid = (P + Q) / 2
    ax.text(mid[0] - 0.1, mid[1] + 0.2, mid[2] + 0.25, "PQ", color=F.AMBER, fontsize=11)

    ax.set_box_aspect((1, 1, 1))
    ax.set_xlim(0, 4.6)
    ax.set_ylim(0, 4.6)
    ax.set_zlim(0, 4.6)
    _clean3d(ax)
    ax.view_init(elev=16, azim=-58)
    ax.set_title("空間直角坐標系：點的坐標、投影與兩點距離", fontsize=13)
    F.save_to(fig, CH, "數A3-4-空間坐標")


# ---------------------------------------------------------------------------
def fig_cross_product():
    """外積：a×b 垂直於 a, b 構成的平面；長度＝平行四邊形面積；右手定則。"""
    fig = plt.figure(figsize=(8.8, 5.2))

    # 左：3D 幾何
    ax = fig.add_subplot(1, 2, 1, projection="3d")
    a = np.array([3.0, 0.6, 0.0])
    b = np.array([0.8, 2.8, 0.0])
    n = np.cross(a, b)
    n = n / np.linalg.norm(n) * 3.0  # 視覺長度

    # a, b 構成的平行四邊形
    O = np.array([0, 0, 0.0])
    quad = np.array([O, a, a + b, b])
    poly = [(p[0], p[1], p[2]) for p in quad]
    from mpl_toolkits.mplot3d.art3d import Poly3DCollection

    pc = Poly3DCollection([poly], facecolor=F.BLUE, alpha=0.18, edgecolor=F.BLUE)
    ax.add_collection3d(pc)

    _arrow3d(ax, O, a, color=F.BLUE, lw=2.6, z=6)
    _arrow3d(ax, O, b, color=F.GREEN, lw=2.6, z=6)
    _arrow3d(ax, O, n, color=F.RED, lw=2.8, z=7)
    ax.text(a[0] + 0.1, a[1], a[2] + 0.1, "a", color=F.BLUE, fontsize=13)
    ax.text(b[0], b[1] + 0.15, b[2] + 0.1, "b", color=F.GREEN, fontsize=13)
    ax.text(n[0] + 0.1, n[1], n[2] + 0.2, "a × b（法向量）", color=F.RED, fontsize=11)
    ax.text(
        (a[0] + b[0]) / 2,
        (a[1] + b[1]) / 2 + 0.2,
        -0.55,
        "面積 = |a × b|",
        color=F.BLUE,
        fontsize=10,
    )

    ax.set_xlim(-0.5, 3.8)
    ax.set_ylim(-0.5, 3.6)
    ax.set_zlim(0, 3.4)
    ax.set_box_aspect((1, 1, 0.95))
    _clean3d(ax)
    ax.view_init(elev=20, azim=-62)
    ax.set_title("a × b ⊥ a, b 所在平面", fontsize=12)

    # 右：右手定則示意（2D）
    ax2 = fig.add_subplot(1, 2, 2)
    ax2.set_aspect("equal")
    ax2.axis("off")
    O2 = (0, 0)
    F.arrow(ax2, O2, (2.4, 0.5), color=F.BLUE, lw=2.6)
    F.arrow(ax2, O2, (0.5, 2.4), color=F.GREEN, lw=2.6)
    F.label(ax2, (2.55, 0.55), "a（四指起始）", color=F.BLUE, fs=11, ha="left")
    F.label(ax2, (0.55, 2.6), "b（四指彎向）", color=F.GREEN, fs=11, ha="left")
    # 旋轉弧（a 轉向 b）
    ax2.add_patch(
        Arc((0, 0), 2.6, 2.6, angle=0, theta1=12, theta2=78, color=F.AMBER, lw=2.0)
    )
    F.arrow(ax2, (1.55, 1.05), (1.35, 1.25), color=F.AMBER, lw=1.6, mutation=14)
    # 拇指（出平面，畫圈點）
    ax2.add_patch(plt.Circle((0, 0), 0.16, fill=False, color=F.RED, lw=2.2))
    ax2.scatter([0], [0], color=F.RED, s=18)
    F.label(
        ax2, (-0.15, -0.45), "拇指 = a × b（指向你）", color=F.RED, fs=11, ha="left"
    )
    ax2.set_xlim(-1.6, 4.2)
    ax2.set_ylim(-1.0, 3.4)
    ax2.set_title("右手定則：四指 a 彎向 b，拇指指 a × b", fontsize=12)

    fig.suptitle("外積 a × b：方向（右手定則）與長度（平行四邊形面積）", fontsize=13)
    F.save_to(fig, CH, "數A3-4-外積")


# ---------------------------------------------------------------------------
def fig_parallelepiped():
    """三向量決定的平行六面體：體積 = |三階行列式| = |(a×b)·c|。"""
    fig = plt.figure(figsize=(7.6, 6.2))
    ax = fig.add_subplot(111, projection="3d")

    a = np.array([3.0, 0.4, 0.0])
    b = np.array([0.8, 2.8, 0.0])
    c = np.array([0.7, 0.9, 3.0])
    O = np.array([0, 0, 0.0])

    verts = {
        "O": O,
        "a": a,
        "b": b,
        "c": c,
        "ab": a + b,
        "ac": a + c,
        "bc": b + c,
        "abc": a + b + c,
    }
    from mpl_toolkits.mplot3d.art3d import Poly3DCollection

    faces = [
        [O, a, a + b, b],  # 底
        [c, a + c, a + b + c, b + c],  # 頂
        [O, a, a + c, c],
        [b, a + b, a + b + c, b + c],
        [O, b, b + c, c],
        [a, a + b, a + b + c, a + c],
    ]
    pc = Poly3DCollection(
        [[(p[0], p[1], p[2]) for p in f] for f in faces],
        facecolor=F.BLUE,
        alpha=0.10,
        edgecolor=F.INK,
        lw=1.2,
    )
    ax.add_collection3d(pc)

    _arrow3d(ax, O, a, color=F.BLUE, lw=2.6, z=8)
    _arrow3d(ax, O, b, color=F.GREEN, lw=2.6, z=8)
    _arrow3d(ax, O, c, color=F.PURPLE, lw=2.6, z=8)
    ax.text(a[0] + 0.15, a[1], a[2] + 0.1, "a", color=F.BLUE, fontsize=13)
    ax.text(b[0] - 0.15, b[1] + 0.2, b[2], "b", color=F.GREEN, fontsize=13)
    ax.text(c[0] - 0.1, c[1], c[2] + 0.2, "c", color=F.PURPLE, fontsize=13)

    ax.text(2.4, 2.0, 3.6, "體積 = |(a × b)·c|", color=F.RED, fontsize=12)

    ax.set_xlim(0, 4.2)
    ax.set_ylim(0, 4.2)
    ax.set_zlim(0, 4.2)
    ax.set_box_aspect((1, 1, 1))
    _clean3d(ax)
    ax.view_init(elev=18, azim=-52)
    ax.set_title("平行六面體：三向量決定的體積 = |三階行列式|", fontsize=13)
    F.save_to(fig, CH, "數A3-4-平行六面體")


# ---------------------------------------------------------------------------
def fig_three_perpendicular():
    """三垂線定理：PA⊥平面E，AB⊥L 於 B，則 PB⊥L。"""
    fig = plt.figure(figsize=(7.8, 6.2))
    ax = fig.add_subplot(111, projection="3d")

    # 平面 E（z=0）的一塊
    from mpl_toolkits.mplot3d.art3d import Poly3DCollection

    plane = [(-0.5, -0.5, 0), (4.5, -0.5, 0), (4.5, 3.5, 0), (-0.5, 3.5, 0)]
    pc = Poly3DCollection(
        [plane], facecolor=F.GRID, alpha=0.45, edgecolor=F.INK, lw=1.0
    )
    ax.add_collection3d(pc)
    ax.text(4.2, -0.4, 0.05, "平面 E", color=F.INK, fontsize=11)

    # 直線 L 在平面 E 上
    L0 = np.array([0.2, 3.0, 0.0])
    L1 = np.array([4.2, 0.6, 0.0])
    ax.plot([L0[0], L1[0]], [L0[1], L1[1]], [0, 0], color=F.PURPLE, lw=2.4)
    ax.text(L1[0] + 0.1, L1[1], 0.05, "L", color=F.PURPLE, fontsize=12)

    A = np.array([1.4, 1.0, 0.0])  # 垂足（P 在平面上的投影）
    P = np.array([1.4, 1.0, 3.0])  # P 在平面外
    # B：A 到直線 L 的垂足
    d = L1 - L0
    d = d / np.linalg.norm(d)
    B = L0 + np.dot(A - L0, d) * d
    B[2] = 0.0

    # PA ⊥ 平面
    ax.plot([P[0], A[0]], [P[1], A[1]], [P[2], A[2]], color=F.RED, lw=2.6)
    ax.scatter(*P, color=F.RED, s=42)
    ax.scatter(*A, color=F.INK, s=30)
    ax.text(P[0] + 0.1, P[1], P[2] + 0.15, "P（面外一點）", color=F.RED, fontsize=11)
    ax.text(A[0] + 0.1, A[1] - 0.25, 0.05, "A（PA⊥平面E）", color=F.INK, fontsize=10)

    # AB ⊥ L
    ax.plot([A[0], B[0]], [A[1], B[1]], [0, 0], color=F.BLUE, lw=2.2)
    ax.scatter(*B, color=F.GREEN, s=30)
    ax.text(B[0] + 0.05, B[1] + 0.15, 0.05, "B（AB⊥L）", color=F.GREEN, fontsize=10)

    # PB（斜線投影），結論 PB ⊥ L
    ax.plot([P[0], B[0]], [P[1], B[1]], [P[2], 0], color=F.AMBER, lw=2.4)
    midPB = (P + B) / 2
    ax.text(
        midPB[0] + 0.1,
        midPB[1],
        midPB[2] + 0.15,
        "PB ⊥ L（結論）",
        color=F.AMBER,
        fontsize=11,
    )

    ax.set_xlim(-0.5, 4.6)
    ax.set_ylim(-0.5, 3.6)
    ax.set_zlim(0, 3.4)
    ax.set_box_aspect((1.3, 1.1, 1))
    _clean3d(ax)
    ax.view_init(elev=20, azim=-66)
    ax.set_title("三垂線定理：PA⊥面、AB⊥L，則 PB⊥L", fontsize=13)
    F.save_to(fig, CH, "數A3-4-三垂線")


if __name__ == "__main__":
    fig_space_coords()
    fig_cross_product()
    fig_parallelepiped()
    fig_three_perpendicular()
    print("done.")
