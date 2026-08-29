# -*- coding: utf-8 -*-
"""重生「數2-4 三角比」學生講義的章內 SVG。"""

if __name__ == "__main__" and __import__("sys").argv[1:]:
    raise SystemExit("本腳本不接受參數；直接執行即可重生數2-4章內 SVG。")

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Arc, Circle, Polygon

import figlib as F


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHAPTER = os.path.join(ROOT, "content", "必修數學", "數2-4")

FIGURE_OUTPUTS = (
    ("fig_similar_ratios", "數2-4-相似三角形邊比.svg"),
    ("fig_special_angles", "數2-4-特殊角三角形.svg"),
    ("fig_unit_circle", "數2-4-廣義角與單位圓.svg"),
    ("fig_identity", "數2-4-平方關係與象限.svg"),
    ("fig_line_polar", "數2-4-斜角與極坐標.svg"),
    ("fig_projection_area", "數2-4-正射影與面積.svg"),
    ("fig_sine_law", "數2-4-正弦定理推導.svg"),
    ("fig_ssa_cases", "數2-4-SSA解的個數.svg"),
    ("fig_cosine_law", "數2-4-餘弦定理坐標推導.svg"),
    ("fig_triangulation", "數2-4-基線三角測量.svg"),
)


def _save(fig, filename):
    stem, extension = os.path.splitext(filename)
    if extension != ".svg" or not stem.startswith("數2-4-"):
        raise AssertionError("輸出檔名必須是數2-4章內 SVG")
    return F.save_to(fig, CHAPTER, stem, output_subdir="assets", write_pdf=False)


def _segment(ax, p, q, **kwargs):
    ax.plot([p[0], q[0]], [p[1], q[1]], **kwargs)


def fig_similar_ratios():
    theta = np.deg2rad(35)
    scales = (2.8, 5.0)
    fig, ax = plt.subplots(figsize=(9.4, 5.4))
    colors = (F.GREEN, F.BLUE)
    hypotenuse_label_positions = (0.42, 0.72)
    for scale, color, label_position in zip(scales, colors, hypotenuse_label_positions):
        adjacent = scale * np.cos(theta)
        opposite = scale * np.sin(theta)
        assert np.isclose(opposite / scale, np.sin(theta))
        assert np.isclose(adjacent / scale, np.cos(theta))
        a = np.array([0.0, 0.0])
        b = np.array([adjacent, 0.0])
        c = np.array([adjacent, opposite])
        ax.add_patch(Polygon([a, b, c], closed=True, fill=False, edgecolor=color, linewidth=2.5))
        ax.text(adjacent / 2, -0.35, f"鄰邊 {adjacent:.2f}", ha="center", color=color, fontsize=10)
        ax.text(adjacent + 0.15, opposite / 2, f"對邊 {opposite:.2f}", va="center", color=color, fontsize=10)
        ax.text(adjacent * label_position, opposite * label_position,
                f"斜邊 {scale:g}", rotation=35, color=color, fontsize=10)
    ax.add_patch(Arc((0, 0), 1.6, 1.6, theta1=0, theta2=35, color=F.AMBER, lw=2))
    ax.text(1.0, 0.25, r"$\theta=35^\circ$", color=F.AMBER, fontsize=12)
    ax.text(0.15, 3.75, r"兩個三角形的對邊／斜邊都等於 $\sin35^\circ$",
            color=F.INK, fontsize=13)
    ax.set_xlim(-0.4, 5.5)
    ax.set_ylim(-0.7, 4.4)
    ax.set_aspect("equal", adjustable="box")
    ax.axis("off")
    ax.set_title("同一銳角形成的直角三角形互相相似", fontsize=15)
    fig.tight_layout()
    return _save(fig, "數2-4-相似三角形邊比.svg")


def fig_special_angles():
    fig, axes = plt.subplots(1, 2, figsize=(10.2, 4.8))
    # 45-45-90
    tri1 = np.array([[0, 0], [3, 0], [3, 3]])
    axes[0].add_patch(Polygon(tri1, closed=True, facecolor="#dbeafe", edgecolor=F.BLUE, lw=2.4))
    axes[0].text(1.5, -0.35, "1", ha="center", fontsize=12)
    axes[0].text(3.18, 1.5, "1", va="center", fontsize=12)
    axes[0].text(1.25, 1.75, r"$\sqrt{2}$", rotation=45, fontsize=12)
    axes[0].text(0.38, 0.18, r"$45^\circ$", color=F.AMBER, fontsize=12)
    axes[0].set_title(r"$45^\circ$：$1:1:\sqrt{2}$", fontsize=13)
    # 30-60-90
    tri2 = np.array([[0, 0], [np.sqrt(3) * 1.7, 0], [np.sqrt(3) * 1.7, 1.7]])
    axes[1].add_patch(Polygon(tri2, closed=True, facecolor="#dcfce7", edgecolor=F.GREEN, lw=2.4))
    axes[1].text(np.sqrt(3) * 0.85, -0.35, r"$\sqrt{3}$", ha="center", fontsize=12)
    axes[1].text(np.sqrt(3) * 1.7 + 0.16, 0.85, "1", va="center", fontsize=12)
    axes[1].text(1.25, 1.08, "2", rotation=30, fontsize=12)
    axes[1].text(0.45, 0.15, r"$30^\circ$", color=F.AMBER, fontsize=12)
    axes[1].set_title(r"$30^\circ$：$1:\sqrt{3}:2$", fontsize=13)
    assert np.isclose(np.hypot(1, 1), np.sqrt(2))
    assert np.isclose(np.hypot(1, np.sqrt(3)), 2)
    for ax in axes:
        ax.set_xlim(-0.4, 3.6)
        ax.set_ylim(-0.6, 3.5)
        ax.set_aspect("equal")
        ax.axis("off")
    fig.suptitle("特殊角的三角比來自兩個可重建的邊長比例", fontsize=16)
    fig.tight_layout(rect=(0, 0, 1, 0.9))
    return _save(fig, "數2-4-特殊角三角形.svg")


def fig_unit_circle():
    theta_deg = 140
    theta = np.deg2rad(theta_deg)
    point = np.array([np.cos(theta), np.sin(theta)])
    assert point[0] < 0 < point[1]
    assert np.isclose(np.dot(point, point), 1)
    reference = 180 - theta_deg
    fig, ax = plt.subplots(figsize=(7.6, 6.6))
    ax.add_patch(Circle((0, 0), 1, fill=False, edgecolor=F.BLUE, lw=2.4))
    _segment(ax, (0, 0), point, color=F.AMBER, lw=2.6)
    _segment(ax, point, (point[0], 0), color=F.GREEN, lw=2, ls="--")
    ax.scatter([point[0]], [point[1]], s=90, color=F.AMBER, zorder=5)
    ax.add_patch(Arc((0, 0), 0.72, 0.72, theta1=0, theta2=theta_deg, color=F.AMBER, lw=2))
    ax.add_patch(Arc((0, 0), 0.45, 0.45, theta1=theta_deg, theta2=180, color=F.GREEN, lw=2))
    ax.text(-0.27, 0.48, r"$140^\circ$", color=F.AMBER, fontsize=12)
    ax.text(-0.45, 0.08, rf"參考角 ${reference}^\circ$", color=F.GREEN, fontsize=11)
    ax.text(point[0] - 0.12, point[1] + 0.12,
            rf"$P(\cos140^\circ,\sin140^\circ)$", ha="center", fontsize=11)
    ax.text(-1.18, -1.1, r"同界角：$140^\circ+360^\circ k$（$k$ 為整數）", fontsize=11)
    ax.axhline(0, color=F.INK, lw=1)
    ax.axvline(0, color=F.INK, lw=1)
    ax.set_xlim(-1.35, 1.35)
    ax.set_ylim(-1.25, 1.25)
    ax.set_aspect("equal")
    F.clean_grid(ax)
    ax.set_title("單位圓把廣義角的三角比變成坐標", fontsize=15)
    fig.tight_layout()
    return _save(fig, "數2-4-廣義角與單位圓.svg")


def fig_identity():
    angles = np.deg2rad([35, 145, 215, 325])
    points = np.c_[np.cos(angles), np.sin(angles)]
    assert np.allclose(np.sum(points**2, axis=1), 1)
    fig, ax = plt.subplots(figsize=(7.7, 6.6))
    ax.add_patch(Circle((0, 0), 1, fill=False, edgecolor=F.BLUE, lw=2.2))
    labels = ["I：sin, cos, tan +", "II：sin +", "III：tan +", "IV：cos +"]
    colors = [F.BLUE, F.GREEN, F.AMBER, "#9333ea"]
    for (x, y), label, color in zip(points, labels, colors):
        _segment(ax, (0, 0), (x, y), color=color, lw=1.8)
        ax.scatter([x], [y], color=color, s=70)
        ax.text(1.08 * x, 1.08 * y, label, ha="left" if x > 0 else "right",
                va="bottom" if y > 0 else "top", color=color, fontsize=10)
    ax.text(0, -1.23, r"$\cos^2\theta+\sin^2\theta=x^2+y^2=1$", ha="center", fontsize=13)
    ax.axhline(0, color=F.INK, lw=1)
    ax.axvline(0, color=F.INK, lw=1)
    ax.set_xlim(-1.55, 1.55)
    ax.set_ylim(-1.35, 1.35)
    ax.set_aspect("equal")
    F.clean_grid(ax)
    ax.set_title("平方關係由單位圓方程式得到；正負由象限決定", fontsize=14)
    fig.tight_layout()
    return _save(fig, "數2-4-平方關係與象限.svg")


def fig_line_polar():
    theta = np.deg2rad(32)
    slope = np.tan(theta)
    r = 4.2
    x, y = r * np.cos(theta), r * np.sin(theta)
    assert np.isclose(y / x, slope)
    assert np.isclose(np.hypot(x, y), r)
    fig, axes = plt.subplots(1, 2, figsize=(10.7, 4.8))
    ax = axes[0]
    xx = np.linspace(-1, 5, 100)
    ax.plot(xx, slope * xx, color=F.BLUE, lw=2.5)
    ax.add_patch(Arc((0, 0), 1.4, 1.4, theta1=0, theta2=32, color=F.AMBER, lw=2))
    ax.text(0.9, 0.2, r"$\theta=32^\circ$", color=F.AMBER, fontsize=11)
    ax.text(2.0, 2.3, r"斜率 $m=\tan\theta$", color=F.BLUE, fontsize=12)
    ax.set_title("直線斜角")
    ax.set_xlim(-0.8, 5)
    ax.set_ylim(-0.8, 4)
    ax.set_aspect("equal")
    ax.axhline(0, color=F.INK, lw=1)
    ax.axvline(0, color=F.INK, lw=1)
    F.clean_grid(ax)

    ax = axes[1]
    ax.scatter([x], [y], color=F.AMBER, s=90)
    _segment(ax, (0, 0), (x, y), color=F.BLUE, lw=2.5)
    _segment(ax, (0, 0), (x, 0), color=F.GREEN, lw=1.8)
    _segment(ax, (x, 0), (x, y), color=F.GREEN, lw=1.8)
    ax.text(x / 2, y / 2 + 0.25, r"$r=4.2$", rotation=32, fontsize=11)
    ax.text(x, y + 0.2, rf"$P({x:.2f},{y:.2f})$", ha="center", fontsize=11)
    ax.text(0.75, 0.18, r"$\theta$", color=F.AMBER, fontsize=12)
    ax.set_title(r"極坐標：$x=r\cos\theta,\ y=r\sin\theta$")
    ax.set_xlim(-0.6, 5)
    ax.set_ylim(-0.6, 3.6)
    ax.set_aspect("equal")
    ax.axhline(0, color=F.INK, lw=1)
    ax.axvline(0, color=F.INK, lw=1)
    F.clean_grid(ax)
    fig.suptitle("方向由角度表示；大小由斜率或半徑表示", fontsize=16)
    fig.tight_layout(rect=(0, 0, 1, 0.91))
    return _save(fig, "數2-4-斜角與極坐標.svg")


def fig_projection_area():
    a, b, c_angle = 5.0, 4.2, np.deg2rad(55)
    A = np.array([0.0, 0.0])
    B = np.array([a, 0.0])
    C = np.array([b * np.cos(c_angle), b * np.sin(c_angle)])
    foot = np.array([C[0], 0.0])
    area = 0.5 * a * b * np.sin(c_angle)
    assert np.isclose(area, 0.5 * a * C[1])
    fig, ax = plt.subplots(figsize=(9.0, 5.5))
    ax.add_patch(Polygon([A, B, C], closed=True, facecolor="#dbeafe", edgecolor=F.BLUE, lw=2.4))
    _segment(ax, C, foot, color=F.AMBER, lw=2.1, ls="--")
    _segment(ax, A, foot, color=F.GREEN, lw=3)
    ax.text((A[0] + foot[0]) / 2, -0.38, r"正射影 $b\cos C$", ha="center", color=F.GREEN, fontsize=11)
    ax.text(C[0] + 0.15, C[1] / 2, r"高 $b\sin C$", va="center", color=F.AMBER, fontsize=11)
    ax.text(a / 2, -0.7, r"底 $a$", ha="center", fontsize=11)
    ax.text(0.6, 0.22, r"$C=55^\circ$", color=F.AMBER, fontsize=11)
    ax.text(3.5, 2.7, r"$K=\dfrac{1}{2}ab\sin C$", fontsize=13)
    ax.set_xlim(-0.5, 5.6)
    ax.set_ylim(-1, 4.2)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("斜邊在底邊方向的投影決定水平分量；垂直分量決定面積", fontsize=14)
    fig.tight_layout()
    return _save(fig, "數2-4-正射影與面積.svg")


def fig_sine_law():
    A = np.array([0.0, 0.0])
    B = np.array([6.0, 0.0])
    C = np.array([2.1, 3.7])
    foot = np.array([C[0], 0.0])
    a = np.linalg.norm(B - C)
    b = np.linalg.norm(A - C)
    angle_A = np.arctan2(C[1], C[0])
    angle_B = np.arctan2(C[1], B[0] - C[0])
    assert np.isclose(b * np.sin(angle_A), a * np.sin(angle_B))
    fig, ax = plt.subplots(figsize=(9.0, 5.7))
    ax.add_patch(Polygon([A, B, C], closed=True, facecolor="#ecfdf5", edgecolor=F.GREEN, lw=2.5))
    _segment(ax, C, foot, color=F.AMBER, lw=2.2, ls="--")
    ax.text(C[0] + 0.15, C[1] / 2, r"$h$", color=F.AMBER, fontsize=12)
    ax.text(-0.25, -0.25, "$A$", fontsize=12)
    ax.text(6.1, -0.25, "$B$", fontsize=12)
    ax.text(C[0], C[1] + 0.2, "$C$", fontsize=12)
    ax.text(4.2, 2.1, "$a$", fontsize=12)
    ax.text(0.75, 2.05, "$b$", fontsize=12)
    ax.text(3, -0.45, "$c$", fontsize=12)
    ax.text(2.9, 4.2, r"$h=b\sin A=a\sin B$", ha="center", fontsize=13)
    ax.text(2.9, 3.78, r"$\Rightarrow\ \dfrac{a}{\sin A}=\dfrac{b}{\sin B}$", ha="center", fontsize=13)
    ax.set_xlim(-0.7, 6.7)
    ax.set_ylim(-0.8, 4.8)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("同一條高把兩個角與各自對邊連在一起", fontsize=15)
    fig.tight_layout()
    return _save(fig, "數2-4-正弦定理推導.svg")


def fig_ssa_cases():
    angle = np.deg2rad(35)
    b = 5.0
    C = b * np.array([np.cos(angle), np.sin(angle)])
    h = C[1]
    radii = (0.75 * h, h, 0.5 * (h + b))
    titles = ("a<h：0 解", "a=h：1 解", "h<a<b：2 解")
    expected = (0, 1, 2)
    fig, axes = plt.subplots(1, 3, figsize=(11.2, 4.8))
    for ax, radius, title, count in zip(axes, radii, titles, expected):
        # 圓心 C 與 x 軸交點。
        discr = radius**2 - C[1] ** 2
        roots = [] if discr < -1e-10 else [C[0]] if np.isclose(discr, 0) else [C[0] - np.sqrt(discr), C[0] + np.sqrt(discr)]
        roots = [root for root in roots if root >= 0]
        assert len(roots) == count
        ax.plot([0, 7], [0, 0], color=F.INK, lw=1.5)
        _segment(ax, (0, 0), C, color=F.BLUE, lw=2.3)
        ax.add_patch(Circle(C, radius, fill=False, edgecolor=F.AMBER, lw=2))
        _segment(ax, C, (C[0], 0), color=F.GREEN, lw=1.6, ls="--")
        if roots:
            ax.scatter(roots, np.zeros(len(roots)), color=F.GREEN, s=70, zorder=5)
            for root in roots:
                _segment(ax, C, (root, 0), color=F.AMBER, lw=1.4, alpha=0.7)
        ax.text(C[0] + 0.12, C[1] / 2, "$h$", color=F.GREEN, fontsize=10)
        ax.set_title(title, fontsize=12)
        ax.set_xlim(-0.5, 8.5)
        ax.set_ylim(-1.3, 7.1)
        ax.set_aspect("equal")
        ax.axis("off")
    fig.suptitle("SSA：固定角 A 與邊 b，再看半徑 a 的圓與底邊相交幾次", fontsize=15)
    fig.tight_layout(rect=(0, 0, 1, 0.9))
    return _save(fig, "數2-4-SSA解的個數.svg")


def fig_cosine_law():
    a, b, C_deg = 5.2, 4.0, 68
    C = np.deg2rad(C_deg)
    P = np.array([a, 0.0])
    Q = b * np.array([np.cos(C), np.sin(C)])
    c = np.linalg.norm(P - Q)
    expected = np.sqrt(a * a + b * b - 2 * a * b * np.cos(C))
    assert np.isclose(c, expected)
    fig, ax = plt.subplots(figsize=(8.8, 5.7))
    ax.add_patch(Polygon([(0, 0), P, Q], closed=True, facecolor="#fef3c7", edgecolor=F.AMBER, lw=2.5))
    _segment(ax, Q, (Q[0], 0), color=F.GREEN, lw=1.8, ls="--")
    ax.text(a / 2, -0.4, "$a$", fontsize=12)
    ax.text(Q[0] / 2 - 0.15, Q[1] / 2, "$b$", fontsize=12)
    ax.text((P[0] + Q[0]) / 2 + 0.15, Q[1] / 2, "$c$", fontsize=12)
    ax.text(Q[0], -0.45, r"$b\cos C$", ha="center", color=F.GREEN, fontsize=11)
    ax.text(Q[0] + 0.15, Q[1] / 2, r"$b\sin C$", color=F.GREEN, fontsize=11)
    ax.text(0.7, 0.25, rf"$C={C_deg}^\circ$", color=F.AMBER, fontsize=11)
    ax.text(3.2, 3.9, r"$c^2=(a-b\cos C)^2+(b\sin C)^2$", fontsize=12)
    ax.text(3.2, 3.45, r"$=a^2+b^2-2ab\cos C$", fontsize=12)
    ax.set_xlim(-0.5, 6.2)
    ax.set_ylim(-0.8, 5.0)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("餘弦定理是水平差與垂直差的距離公式", fontsize=15)
    fig.tight_layout()
    return _save(fig, "數2-4-餘弦定理坐標推導.svg")


def fig_triangulation():
    A = np.array([0.0, 0.0])
    B = np.array([6.0, 0.0])
    alpha = np.deg2rad(48)
    beta = np.deg2rad(63)
    # A+t(cos a,sin a)=B+s(cos(pi-beta),sin(pi-beta))
    matrix = np.c_[[np.cos(alpha), np.sin(alpha)], [-np.cos(np.pi - beta), -np.sin(np.pi - beta)]]
    t, s = np.linalg.solve(matrix, B)
    T = A + t * np.array([np.cos(alpha), np.sin(alpha)])
    assert np.allclose(T, B + s * np.array([np.cos(np.pi - beta), np.sin(np.pi - beta)]))
    assert np.isclose(t / np.sin(beta), 6 / np.sin(np.pi - alpha - beta))
    fig, ax = plt.subplots(figsize=(9.2, 6.0))
    ax.add_patch(Polygon([A, B, T], closed=True, facecolor="#dbeafe", edgecolor=F.BLUE, lw=2.4))
    ax.scatter([A[0], B[0], T[0]], [A[1], B[1], T[1]], color=[F.GREEN, F.GREEN, F.AMBER], s=85)
    ax.text(A[0] - 0.2, A[1] - 0.3, "A", fontsize=12)
    ax.text(B[0] + 0.15, B[1] - 0.3, "B", fontsize=12)
    ax.text(T[0], T[1] + 0.25, "目標 T", ha="center", fontsize=12)
    ax.text(3, -0.45, "已知基線 6 km", ha="center", color=F.GREEN, fontsize=11)
    ax.text(0.7, 0.25, r"$48^\circ$", color=F.AMBER, fontsize=11)
    ax.text(5.1, 0.25, r"$63^\circ$", color=F.AMBER, fontsize=11)
    ax.text(3.1, T[1] + 0.75,
            r"量兩端方向角 $\Rightarrow$ 內角 $\Rightarrow$ 正弦定理求距離", ha="center", fontsize=12)
    ax.set_xlim(-0.7, 6.7)
    ax.set_ylim(-0.8, T[1] + 1.4)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("三角測量用一條可量的基線定位難以直接到達的目標", fontsize=15)
    fig.tight_layout()
    return _save(fig, "數2-4-基線三角測量.svg")


if __name__ == "__main__":
    for entrypoint, _ in FIGURE_OUTPUTS:
        globals()[entrypoint]()
