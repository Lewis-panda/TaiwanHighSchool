# -*- coding: utf-8 -*-
"""產生「數A4-1 空間中的平面與直線」的圖，輸出到該章 sources/。
重繪：  .venv/bin/python _tools/fig_數A4-1.py

注意：
- mathtext 不支援 \\dfrac/\\tfrac，圖內一律用 \\frac。
- 圖內中文不要包在 $...$ 裡（mathtext 不含中文字符）。
- 3D 圖用 projection="3d"。
"""

import os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
from mpl_toolkits.mplot3d.proj3d import proj_transform
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401  (註冊 3d 投影)
import figlib as F

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CH = os.path.join(ROOT, "數學", "數學二下（數學A·第四冊）", "數A4-1 空間中的平面與直線")


class Arrow3D(FancyArrowPatch):
    """3D 箭頭（向量／法向量／方向向量）。"""

    def __init__(self, xs, ys, zs, *args, **kwargs):
        super().__init__((0, 0), (0, 0), *args, **kwargs)
        self._verts3d = xs, ys, zs

    def do_3d_projection(self, renderer=None):
        xs3d, ys3d, zs3d = self._verts3d
        xs, ys, zs = proj_transform(xs3d, ys3d, zs3d, self.axes.M)
        self.set_positions((xs[0], ys[0]), (xs[1], ys[1]))
        return np.min(zs)


def arrow3d(ax, p0, p1, color=F.INK, lw=2.4, mutation=16, ls="-", z=6):
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
        ax.xaxis.pane.set_edgecolor((1, 1, 1, 0))
        ax.yaxis.pane.set_edgecolor((1, 1, 1, 0))
        ax.zaxis.pane.set_edgecolor((1, 1, 1, 0))
    except Exception:
        pass


def _plane(ax, point, normal, color, alpha=0.28, span=2.2, n=2):
    """畫一個以 point 為中心、法向量 normal 的平面片。"""
    normal = np.array(normal, dtype=float)
    normal = normal / np.linalg.norm(normal)
    # 找兩個張平面的基底
    a = np.array([1.0, 0.0, 0.0])
    if abs(np.dot(a, normal)) > 0.9:
        a = np.array([0.0, 1.0, 0.0])
    u = np.cross(normal, a)
    u = u / np.linalg.norm(u)
    v = np.cross(normal, u)
    s = np.linspace(-span, span, n + 1)
    S, T = np.meshgrid(s, s)
    P = np.array(point, dtype=float)
    X = P[0] + S * u[0] + T * v[0]
    Y = P[1] + S * u[1] + T * v[1]
    Z = P[2] + S * u[2] + T * v[2]
    ax.plot_surface(
        X, Y, Z, color=color, alpha=alpha, linewidth=0, shade=False, zorder=1
    )


# ---------------------------------------------------------------------------
def fig_plane_normal():
    """平面由一點與一法向量唯一決定：法向量垂直於平面內每一條向量。"""
    fig = plt.figure(figsize=(6.6, 5.4))
    ax = fig.add_subplot(111, projection="3d")

    P0 = np.array([0.0, 0.0, 0.0])
    normal = np.array([0.5, 0.6, 1.0])

    _plane(ax, P0, normal, F.BLUE, alpha=0.25, span=2.4)

    # 法向量
    nlen = 2.0
    nv = normal / np.linalg.norm(normal) * nlen
    arrow3d(ax, P0, P0 + nv, color=F.RED, lw=2.6, mutation=18)
    ax.text(*(P0 + nv * 1.12), "法向量 n", color=F.RED, fontsize=12)

    # 平面內兩個點 A、B，畫 P0->A、P0->B（都垂直於 n）
    a = np.array([1.0, 0.0, 0.0])
    u = np.cross(normal, a)
    u = u / np.linalg.norm(u)
    v = np.cross(normal, u)
    A = P0 + 1.8 * u
    B = P0 + 1.6 * v
    arrow3d(ax, P0, A, color=F.GREEN, lw=2.2, mutation=15)
    arrow3d(ax, P0, B, color=F.GREEN, lw=2.2, mutation=15)
    ax.text(*(A * 1.12), "平面上的向量", color=F.GREEN, fontsize=11)
    ax.scatter(*P0, color=F.INK, s=30, zorder=8)
    ax.text(P0[0] + 0.1, P0[1] + 0.1, P0[2] - 0.35, "P0", color=F.INK, fontsize=12)

    ax.set_xlim(-2.4, 2.4)
    ax.set_ylim(-2.4, 2.4)
    ax.set_zlim(-1.0, 2.6)
    ax.set_box_aspect((1, 1, 0.9))
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_zticks([])
    ax.set_title("平面：定一點 + 一法向量就唯一確定", fontsize=13)
    ax.view_init(elev=20, azim=-58)
    _clean3d(ax)
    F.save_to(fig, CH, "數A4-1-平面法向量")


def fig_dihedral_angle():
    """兩平面的夾角 = 兩法向量的夾角（或其補角）。"""
    fig = plt.figure(figsize=(6.8, 5.4))
    ax = fig.add_subplot(111, projection="3d")

    # 兩平面共用一條交線（取 x 軸方向），用不同傾角
    # 平面1 法向量 n1，平面2 法向量 n2
    n1 = np.array([0.0, 0.0, 1.0])
    n2 = np.array([0.0, 0.8, 0.6])
    C = np.array([0.0, 0.0, 0.0])

    _plane(ax, C, n1, F.BLUE, alpha=0.22, span=2.2)
    _plane(ax, C, n2, F.GREEN, alpha=0.22, span=2.2)

    arrow3d(ax, C, C + n1 * 2.0, color=F.BLUE, lw=2.6, mutation=18)
    arrow3d(ax, C, C + n2 * 2.0, color=F.GREEN, lw=2.6, mutation=18)
    ax.text(*(C + n1 * 2.1), "n1", color=F.BLUE, fontsize=12)
    ax.text(*(C + n2 * 2.15), "n2", color=F.GREEN, fontsize=12)

    # 交線（沿 x）
    ax.plot([-2.4, 2.4], [0, 0], [0, 0], color=F.INK, lw=1.6)
    ax.text(2.5, 0, 0, "交線", color=F.INK, fontsize=11)

    ax.text(
        -2.2,
        0,
        2.2,
        "兩平面夾角 = 兩法向量夾角\n（必要時取補角）",
        color=F.INK,
        fontsize=11,
    )

    ax.set_xlim(-2.4, 2.4)
    ax.set_ylim(-2.4, 2.4)
    ax.set_zlim(-1.2, 2.4)
    ax.set_box_aspect((1, 1, 0.9))
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_zticks([])
    ax.set_title("兩平面的夾角", fontsize=13)
    ax.view_init(elev=16, azim=-66)
    _clean3d(ax)
    F.save_to(fig, CH, "數A4-1-兩平面夾角")


def fig_line_param():
    """直線參數式：過定點 A、沿方向向量 d；動點 P = A + t d。"""
    fig = plt.figure(figsize=(6.8, 5.2))
    ax = fig.add_subplot(111, projection="3d")

    A = np.array([-1.2, -1.0, -0.6])
    d = np.array([1.0, 0.8, 1.2])
    d = d / np.linalg.norm(d)

    ts = np.linspace(-1.0, 3.4, 50)
    pts = np.array([A + t * d for t in ts])
    ax.plot(pts[:, 0], pts[:, 1], pts[:, 2], color=F.INK, lw=2.0, zorder=2)

    # 定點 A
    ax.scatter(*A, color=F.RED, s=40, zorder=8)
    ax.text(A[0] - 0.1, A[1] - 0.1, A[2] - 0.45, "定點 A", color=F.RED, fontsize=12)

    # 方向向量 d
    arrow3d(ax, A, A + 1.8 * d, color=F.BLUE, lw=2.6, mutation=18)
    ax.text(*(A + 1.95 * d), "方向向量 d", color=F.BLUE, fontsize=12)

    # 動點 P（某個 t）
    t0 = 2.6
    P = A + t0 * d
    ax.scatter(*P, color=F.GREEN, s=40, zorder=8)
    ax.text(
        P[0] + 0.1,
        P[1] + 0.1,
        P[2] + 0.2,
        "動點 P = A + t d",
        color=F.GREEN,
        fontsize=11,
    )

    ax.set_xlim(-2.0, 2.4)
    ax.set_ylim(-2.0, 2.4)
    ax.set_zlim(-1.4, 2.6)
    ax.set_box_aspect((1, 1, 0.9))
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_zticks([])
    ax.set_title("直線的參數式：過定點、沿方向向量", fontsize=13)
    ax.view_init(elev=18, azim=-60)
    _clean3d(ax)
    F.save_to(fig, CH, "數A4-1-直線參數式")


def fig_point_to_plane():
    """點到平面的距離 = 連線在法向量方向的投影長。"""
    fig = plt.figure(figsize=(6.8, 5.4))
    ax = fig.add_subplot(111, projection="3d")

    normal = np.array([0.3, 0.4, 1.0])
    nhat = normal / np.linalg.norm(normal)
    O = np.array([0.0, 0.0, 0.0])  # 平面上一點
    _plane(ax, O, normal, F.BLUE, alpha=0.24, span=2.4)

    # 平面外一點 P
    dist = 2.0
    P = O + dist * nhat + 0.8 * np.array([1.0, -0.6, 0.0])
    # 垂足 Q = P - (P·n) n  （O 在原點）
    Q = P - np.dot(P, nhat) * nhat

    ax.scatter(*P, color=F.RED, s=45, zorder=9)
    ax.text(P[0] + 0.1, P[1] + 0.1, P[2] + 0.2, "點 P", color=F.RED, fontsize=12)
    ax.scatter(*Q, color=F.INK, s=35, zorder=9)
    ax.text(Q[0] + 0.05, Q[1] + 0.05, Q[2] - 0.4, "垂足 Q", color=F.INK, fontsize=11)

    # 垂線 PQ（虛線）= 距離
    ax.plot(
        [P[0], Q[0]],
        [P[1], Q[1]],
        [P[2], Q[2]],
        color=F.AMBER,
        lw=2.4,
        ls="--",
        zorder=7,
    )
    mid = (P + Q) / 2
    ax.text(mid[0] + 0.15, mid[1] + 0.15, mid[2], "距離 d", color=F.AMBER, fontsize=12)

    # 法向量（在垂足處）
    arrow3d(ax, Q, Q + 1.4 * nhat, color=F.GREEN, lw=2.2, mutation=15)
    ax.text(*(Q + 1.5 * nhat), "n", color=F.GREEN, fontsize=12)

    ax.set_xlim(-2.4, 2.4)
    ax.set_ylim(-2.4, 2.4)
    ax.set_zlim(-1.0, 3.0)
    ax.set_box_aspect((1, 1, 0.95))
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_zticks([])
    ax.set_title("點到平面距離 = 連線在法向量上的投影", fontsize=12)
    ax.view_init(elev=18, azim=-56)
    _clean3d(ax)
    F.save_to(fig, CH, "數A4-1-點到平面距離")


def fig_skew_lines():
    """兩歪斜線：既不平行也不相交；公垂線段長即其距離。"""
    fig = plt.figure(figsize=(7.0, 5.4))
    ax = fig.add_subplot(111, projection="3d")

    # 線 L1：沿 x 方向，在 z=0 平面、y=-0.9
    A1 = np.array([-2.2, -0.9, 0.0])
    d1 = np.array([1.0, 0.0, 0.0])
    # 線 L2：沿 y 方向，在 z=1.4、x=0.6
    A2 = np.array([0.6, -2.2, 1.4])
    d2 = np.array([0.0, 1.0, 0.0])

    t = np.linspace(0, 4.4, 30)
    L1 = np.array([A1 + ti * d1 for ti in t])
    L2 = np.array([A2 + ti * d2 for ti in t])
    ax.plot(L1[:, 0], L1[:, 1], L1[:, 2], color=F.BLUE, lw=2.4)
    ax.plot(L2[:, 0], L2[:, 1], L2[:, 2], color=F.GREEN, lw=2.4)
    ax.text(
        L1[-1, 0] + 0.1, L1[-1, 1], L1[-1, 2] - 0.3, "L1", color=F.BLUE, fontsize=12
    )
    ax.text(
        L2[-1, 0] + 0.1, L2[-1, 1], L2[-1, 2] + 0.2, "L2", color=F.GREEN, fontsize=12
    )

    # 公垂線：方向 d1 x d2 = (0,0,1)x? 這裡 d1=(1,0,0), d2=(0,1,0) => n=(0,0,1)
    # L1 上的點 (x, -0.9, 0)，L2 上的點 (0.6, y, 1.4)；公垂線沿 z。
    # 取 x=0.6（與 L2 的 x 對齊）、y=-0.9（與 L1 的 y 對齊）
    Q1 = np.array([0.6, -0.9, 0.0])
    Q2 = np.array([0.6, -0.9, 1.4])
    ax.plot(
        [Q1[0], Q2[0]],
        [Q1[1], Q2[1]],
        [Q1[2], Q2[2]],
        color=F.AMBER,
        lw=2.6,
        ls="--",
        zorder=8,
    )
    ax.scatter(*Q1, color=F.AMBER, s=30, zorder=9)
    ax.scatter(*Q2, color=F.AMBER, s=30, zorder=9)
    mid = (Q1 + Q2) / 2
    ax.text(
        mid[0] + 0.2,
        mid[1] + 0.1,
        mid[2],
        "公垂線段 = 距離 d",
        color=F.AMBER,
        fontsize=11,
    )

    ax.set_xlim(-2.4, 2.6)
    ax.set_ylim(-2.4, 2.6)
    ax.set_zlim(-0.6, 2.2)
    ax.set_box_aspect((1, 1, 0.7))
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_zticks([])
    ax.set_title("兩歪斜線與其距離（公垂線段）", fontsize=13)
    ax.view_init(elev=20, azim=-52)
    _clean3d(ax)
    F.save_to(fig, CH, "數A4-1-歪斜線距離")


def fig_line_plane_relation():
    """直線與平面的三種關係：相交於一點 / 平行 / 在平面上。"""
    fig = plt.figure(figsize=(11.0, 4.2))

    normal = np.array([0.0, 0.0, 1.0])  # 取水平平面方便看
    O = np.array([0.0, 0.0, 0.0])

    cases = [
        ("相交於一點", np.array([0.6, 0.4, 1.0]), np.array([-1.0, -0.8, 1.2]), F.RED),
        ("與平面平行", np.array([1.0, 0.4, 0.0]), np.array([-1.4, -0.8, 1.3]), F.BLUE),
        (
            "直線在平面上",
            np.array([1.0, 0.6, 0.0]),
            np.array([-1.4, -0.9, 0.0]),
            F.GREEN,
        ),
    ]

    for i, (title, d, A, col) in enumerate(cases):
        ax = fig.add_subplot(1, 3, i + 1, projection="3d")
        _plane(ax, O, normal, "#9db8e6", alpha=0.30, span=2.0)
        d = np.array(d, dtype=float)
        d = d / np.linalg.norm(d)
        ts = np.linspace(-0.5, 3.0, 30)
        pts = np.array([A + t * d for t in ts])
        ax.plot(pts[:, 0], pts[:, 1], pts[:, 2], color=col, lw=2.6, zorder=5)
        ax.set_xlim(-2.2, 2.2)
        ax.set_ylim(-2.2, 2.2)
        ax.set_zlim(-0.4, 2.0)
        ax.set_box_aspect((1, 1, 0.7))
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_zticks([])
        ax.set_title(title, fontsize=12)
        ax.view_init(elev=16, azim=-60)
        _clean3d(ax)

    fig.suptitle("直線與平面的三種位置關係", fontsize=13)
    fig.tight_layout()
    F.save_to(fig, CH, "數A4-1-直線與平面關係")


if __name__ == "__main__":
    fig_plane_normal()
    fig_dihedral_angle()
    fig_line_param()
    fig_point_to_plane()
    fig_skew_lines()
    fig_line_plane_relation()
    print("done.")
