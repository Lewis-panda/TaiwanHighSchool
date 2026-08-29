# -*- coding: utf-8 -*-
"""重生「數B3-3 平面向量與應用」學生講義的章內 SVG。"""

if __name__ == "__main__" and __import__("sys").argv[1:]:
    raise SystemExit("本腳本不接受參數；直接執行即可重生數B3-3 章內 SVG。")

import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import matplotlib.pyplot as plt
from matplotlib.patches import Arc, Circle, Polygon, Rectangle
import numpy as np

import figlib as F


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHAPTER = os.path.join(ROOT, "content", "數學B", "數B3-3")

FIGURE_OUTPUTS = (
    ("fig_vector_addition", "數B3-3-向量加減與平移.svg"),
    ("fig_coordinate_vector", "數B3-3-坐標向量.svg"),
    ("fig_linear_combination", "數B3-3-線性組合區域.svg"),
    ("fig_division_points", "數B3-3-內分與外分.svg"),
    ("fig_affine_transform", "數B3-3-縮放與平移.svg"),
    ("fig_dot_angle", "數B3-3-夾角與內積.svg"),
    ("fig_dot_expansion", "數B3-3-內積展開與對角線.svg"),
    ("fig_projection", "數B3-3-正射影與分解.svg"),
    ("fig_point_line_distance", "數B3-3-投影點與點線距離.svg"),
    ("fig_normal_vector", "數B3-3-法向量與直線.svg"),
    ("fig_perspective_grid", "數B3-3-單點透視等分.svg"),
    ("fig_perspective_ratio", "數B3-3-透視比例.svg"),
    ("fig_a_series", "數B3-3-A系列紙張.svg"),
    ("fig_fibonacci_ratio", "數B3-3-費氏比值.svg"),
    ("fig_golden_spiral", "數B3-3-黃金分割與方形螺線.svg"),
    ("fig_rounded_corner", "數B3-3-圓角切線幾何.svg"),
)


def _save(fig, filename):
    stem, extension = os.path.splitext(filename)
    if extension != ".svg" or not stem.startswith("數B3-3-"):
        raise AssertionError("輸出檔名必須是數B3-3 章內 SVG")
    return F.save_to(fig, CHAPTER, stem, output_subdir="assets", write_pdf=False)


def _point(ax, p, name, *, color=F.INK, dx=.1, dy=.12):
    ax.scatter([p[0]], [p[1]], color=color, s=38, zorder=8)
    ax.text(p[0] + dx, p[1] + dy, name, color=color, fontsize=11, zorder=9)


def fig_vector_addition():
    a = np.array([3.0, 1.0])
    b = np.array([1.0, 2.0])
    origin = np.array([0.0, 0.0])
    assert np.allclose((origin + a) + b, origin + (a + b))
    assert np.allclose((a + b) - b, a)

    fig, ax = F.canvas(9.4, 5.3, equal=True)
    F.arrow(ax, origin, a, color=F.BLUE)
    F.arrow(ax, a, a + b, color=F.GREEN)
    F.arrow(ax, origin, a + b, color=F.RED)
    F.arrow(ax, b, a + b, color=F.BLUE, ls="--", alpha=.65)
    F.arrow(ax, origin, b, color=F.GREEN, ls="--", alpha=.65)
    _point(ax, origin, "$O$", dx=-.3, dy=-.3)
    _point(ax, a, "$A$")
    _point(ax, b, "$B$", dx=-.35)
    _point(ax, a + b, "$C$")
    ax.text(1.55, .2, r"$\vec a$", color=F.BLUE)
    ax.text(3.35, 1.95, r"$\vec b$", color=F.GREEN)
    ax.text(1.75, 1.75, r"$\vec a+\vec b$", color=F.RED)
    ax.set_xlim(-.6, 4.8); ax.set_ylim(-.6, 3.6)
    F.clean_grid(ax)
    ax.set_title("首尾相接與平行四邊形得到同一個向量和")
    fig.tight_layout()
    return _save(fig, "數B3-3-向量加減與平移.svg")


def fig_coordinate_vector():
    a = np.array([-2.0, 1.0])
    b = np.array([4.0, 5.0])
    ab = b - a
    assert np.allclose(ab, [6, 4])
    assert math.isclose(np.linalg.norm(ab), 2 * math.sqrt(13))

    fig, ax = F.canvas(9.5, 5.4, equal=True)
    ax.axhline(0, color=F.INK, lw=1.1); ax.axvline(0, color=F.INK, lw=1.1)
    F.arrow(ax, a, b, color=F.BLUE)
    ax.plot([a[0], b[0]], [a[1], a[1]], color=F.AMBER, ls="--")
    ax.plot([b[0], b[0]], [a[1], b[1]], color=F.AMBER, ls="--")
    _point(ax, a, "$A(-2,1)$", dx=-1.15, dy=.25)
    _point(ax, b, "$B(4,5)$", dx=.1, dy=.2)
    ax.text(.4, .55, r"水平分量 $4-(-2)=6$", color=F.AMBER)
    ax.text(4.15, 3.05, r"鉛直分量 $5-1=4$", color=F.AMBER, rotation=90, va="center")
    ax.text(.1, 3.35, r"$\overrightarrow{AB}=(6,4)$", color=F.BLUE, fontsize=14)
    ax.set_xlim(-3.5, 5.6); ax.set_ylim(-.8, 6.2)
    F.clean_grid(ax)
    ax.set_title("終點坐標減起點坐標，方向由 $A$ 指向 $B$")
    fig.tight_layout()
    return _save(fig, "數B3-3-坐標向量.svg")


def fig_linear_combination():
    a = np.array([3.0, 1.0]); b = np.array([1.0, 2.5])
    vertices = np.array([[0, 0], a, a + b, b])
    area = abs(np.linalg.det(np.column_stack([a, b])))
    assert math.isclose(area, 6.5)
    assert np.allclose(.4 * a + .7 * b, [1.9, 2.15])

    fig, ax = F.canvas(9.3, 5.3, equal=True)
    ax.add_patch(Polygon(vertices, closed=True, facecolor=F.FILL, alpha=.14,
                         edgecolor=F.BLUE, lw=2))
    F.arrow(ax, (0, 0), a, color=F.BLUE)
    F.arrow(ax, (0, 0), b, color=F.GREEN)
    p = .4 * a + .7 * b
    _point(ax, p, r"$P=0.4\vec a+0.7\vec b$", color=F.RED, dx=.12, dy=.2)
    ax.plot([.4*a[0], p[0]], [.4*a[1], p[1]], color=F.GREEN, ls="--")
    ax.plot([0, .4*a[0]], [0, .4*a[1]], color=F.BLUE, ls="--")
    ax.text(2.0, .25, r"$\vec a$", color=F.BLUE)
    ax.text(.25, 1.45, r"$\vec b$", color=F.GREEN)
    ax.text(2.0, 3.25, r"$0\leq s,t\leq1$ 形成平行四邊形", ha="center")
    ax.set_xlim(-.5, 4.8); ax.set_ylim(-.5, 4.2)
    F.clean_grid(ax)
    ax.set_title(r"$\vec{OP}=s\vec a+t\vec b$：係數範圍決定點的區域")
    fig.tight_layout()
    return _save(fig, "數B3-3-線性組合區域.svg")


def fig_division_points():
    a = np.array([1.0, 1.2]); b = np.array([7.0, 3.2])
    m, n = 2.0, 1.0
    p = (n * a + m * b) / (m + n)
    q = (m * b - n * a) / (m - n)
    assert np.allclose(p, [5, 38/15])
    assert math.isclose(np.linalg.norm(p-a) / np.linalg.norm(b-p), m/n)
    assert np.allclose(q, [13, 5.2])
    assert math.isclose(np.linalg.norm(q-a) / np.linalg.norm(q-b), m/n)

    fig, ax = F.canvas(11.0, 4.5, equal=True)
    ax.plot([a[0], q[0]], [a[1], q[1]], color=F.GRID, lw=2)
    F.arrow(ax, a, b, color=F.BLUE)
    F.arrow(ax, b, q, color=F.RED)
    for point, name, color in ((a, "$A$", F.INK), (p, "$P$ 內分", F.BLUE),
                               (b, "$B$", F.INK), (q, "$Q$ 外分", F.RED)):
        _point(ax, point, name, color=color, dx=.05, dy=.25)
    ax.text(3.0, 2.4, "$AP:PB=2:1$", color=F.BLUE)
    ax.text(8.7, 4.05, "$AQ:QB=2:1$", color=F.RED)
    ax.text(5.5, .25, r"$P=\frac{A+2B}{3}$；$Q=\frac{2B-A}{1}$", ha="center")
    ax.set_xlim(0, 14); ax.set_ylim(.2, 6.1)
    ax.axis("off")
    ax.set_title("同一比例在兩個位置成立；先由點的順序判斷內分或外分")
    fig.tight_layout()
    return _save(fig, "數B3-3-內分與外分.svg")


def fig_affine_transform():
    polygon = np.array([[0, 0], [3, 0], [2.3, 1.8], [.4, 1.3]])
    r = 1.5; shift = np.array([5.0, .8])
    transformed = r * polygon + shift
    old_area = .5 * abs(np.dot(polygon[:,0], np.roll(polygon[:,1], -1)) -
                          np.dot(polygon[:,1], np.roll(polygon[:,0], -1)))
    new_area = .5 * abs(np.dot(transformed[:,0], np.roll(transformed[:,1], -1)) -
                          np.dot(transformed[:,1], np.roll(transformed[:,0], -1)))
    assert math.isclose(new_area / old_area, r*r)

    fig, ax = F.canvas(11.0, 5.1, equal=True)
    ax.add_patch(Polygon(polygon, closed=True, facecolor=F.BLUE, alpha=.18,
                         edgecolor=F.BLUE, lw=2))
    ax.add_patch(Polygon(transformed, closed=True, facecolor=F.RED, alpha=.16,
                         edgecolor=F.RED, lw=2))
    F.arrow(ax, polygon[0], transformed[0], color=F.GREEN)
    ax.text(1.3, .7, "原圖", color=F.BLUE)
    ax.text(7.1, 2.25, "縮放 1.5 倍後平移", color=F.RED)
    ax.text(3.2, .1, r"$\vec{OP'}=1.5\vec{OP}+(5,0.8)$", color=F.GREEN)
    ax.text(6.7, 4.1, "長度倍率 1.5；面積倍率 2.25", ha="center")
    ax.set_xlim(-.8, 10.2); ax.set_ylim(-.6, 5.0)
    ax.axis("off")
    ax.set_title("縮放改變長度與面積；平移只改變位置")
    fig.tight_layout()
    return _save(fig, "數B3-3-縮放與平移.svg")


def fig_dot_angle():
    cases = [(35, F.BLUE, "銳角：內積為正"), (90, F.GREEN, "直角：內積為 0"),
             (140, F.RED, "鈍角：內積為負")]
    for degree, _, _ in cases:
        value = math.cos(math.radians(degree))
        assert (degree < 90 and value > 0) or (degree == 90 and abs(value) < 1e-12) or (degree > 90 and value < 0)

    fig, axes = plt.subplots(1, 3, figsize=(12, 4.3))
    for ax, (degree, color, title) in zip(axes, cases):
        ax.set_aspect("equal"); ax.axis("off")
        a = np.array([3.0, 0.0]); b = 2.5*np.array([math.cos(math.radians(degree)), math.sin(math.radians(degree))])
        F.arrow(ax, (0,0), a, color=F.INK)
        F.arrow(ax, (0,0), b, color=color)
        F.angle_arc(ax, (0,0), .65, 0, degree, color=color, text=fr"${degree}^\circ$")
        ax.text(0, -.65, title, color=color, ha="center", fontsize=11)
        ax.set_xlim(-2.6, 3.5); ax.set_ylim(-1.0, 3.0)
    fig.suptitle(r"$\vec a\cdot\vec b=|\vec a||\vec b|\cos\theta$：正負號來自投影方向", fontsize=15)
    fig.tight_layout()
    return _save(fig, "數B3-3-夾角與內積.svg")


def fig_dot_expansion():
    a = np.array([3.0, .5]); b = np.array([1.0, 2.5])
    diag_plus = a+b; diag_minus = a-b
    assert math.isclose(np.dot(diag_plus, diag_plus), np.dot(a,a)+2*np.dot(a,b)+np.dot(b,b))
    assert math.isclose(np.dot(diag_minus, diag_minus), np.dot(a,a)-2*np.dot(a,b)+np.dot(b,b))
    assert math.isclose(np.dot(diag_plus, diag_plus)+np.dot(diag_minus, diag_minus), 2*(np.dot(a,a)+np.dot(b,b)))

    fig, ax = F.canvas(9.5, 5.3, equal=True)
    vertices = np.array([[0,0], a, a+b, b])
    ax.add_patch(Polygon(vertices, closed=True, fill=False, edgecolor=F.INK, lw=1.8))
    F.arrow(ax, (0,0), a, color=F.BLUE)
    F.arrow(ax, (0,0), b, color=F.GREEN)
    F.arrow(ax, (0,0), diag_plus, color=F.RED)
    F.arrow(ax, b, a, color=F.PURPLE)
    ax.text(1.7, .05, r"$\vec a$", color=F.BLUE)
    ax.text(.25, 1.25, r"$\vec b$", color=F.GREEN)
    ax.text(2.25, 1.75, r"$\vec a+\vec b$", color=F.RED)
    ax.text(1.7, 1.8, r"$\vec a-\vec b$", color=F.PURPLE)
    ax.text(1.8, 3.55, r"$|a+b|^2+|a-b|^2=2|a|^2+2|b|^2$", ha="center")
    ax.set_xlim(-.5, 4.8); ax.set_ylim(-.5, 4.2)
    ax.axis("off")
    ax.set_title("兩條對角線的長度可由內積展開，不必另求角度")
    fig.tight_layout()
    return _save(fig, "數B3-3-內積展開與對角線.svg")


def fig_projection():
    a = np.array([5.0, 4.0]); b = np.array([4.0, 1.0])
    proj = np.dot(a,b)/np.dot(b,b)*b
    perp = a-proj
    assert np.allclose(proj, [96/17, 24/17])
    assert abs(np.dot(perp,b)) < 1e-12
    assert np.allclose(proj+perp, a)

    fig, ax = F.canvas(9.4, 5.4, equal=True)
    line_t = np.linspace(-.2, 1.7, 2)
    ax.plot(line_t*b[0], line_t*b[1], color=F.GRID, lw=2)
    F.arrow(ax, (0,0), a, color=F.BLUE)
    F.arrow(ax, (0,0), proj, color=F.GREEN)
    F.arrow(ax, proj, a, color=F.RED)
    _point(ax, a, "$A$", color=F.BLUE)
    _point(ax, proj, "$H$", color=F.GREEN)
    ax.text(2.4, 2.55, r"$\vec a$", color=F.BLUE)
    ax.text(3.7, .65, r"$\operatorname{proj}_{\vec b}\vec a$", color=F.GREEN)
    ax.text(5.55, 2.8, r"$\vec a-\operatorname{proj}_{\vec b}\vec a$", color=F.RED, rotation=73, ha="center")
    ax.text(3.2, 4.75, r"$\vec a=\vec v+\vec u,\quad \vec v\parallel\vec b,\ \vec u\perp\vec b$", ha="center")
    ax.set_xlim(-.7, 7.2); ax.set_ylim(-.7, 5.4)
    ax.axis("off")
    ax.set_title("正射影給出平行分量，剩餘向量是垂直分量")
    fig.tight_layout()
    return _save(fig, "數B3-3-正射影與分解.svg")


def fig_point_line_distance():
    p = np.array([5.0, 5.0]); a = np.array([0.0, 1.0]); d = np.array([4.0, 2.0])
    h = a + np.dot(p-a, d)/np.dot(d,d)*d
    residual = p-h
    assert np.allclose(h, [5.6, 3.8])
    assert abs(np.dot(residual,d)) < 1e-12
    assert math.isclose(np.linalg.norm(residual), 3/math.sqrt(5))

    fig, ax = F.canvas(9.5, 5.5, equal=True)
    t = np.linspace(-.4, 1.8, 2); line = a[None,:]+t[:,None]*d
    ax.plot(line[:,0], line[:,1], color=F.INK, lw=2, label=r"$L$ 的方向 $(4,2)$")
    F.arrow(ax, a, p, color=F.BLUE)
    F.arrow(ax, a, h, color=F.GREEN)
    F.arrow(ax, h, p, color=F.RED)
    _point(ax, p, "$P(5,5)$", color=F.BLUE)
    _point(ax, h, "$H(5.6,3.8)$", color=F.GREEN)
    _point(ax, a, "$A(0,1)$", dx=-.8, dy=.2)
    ax.text(3.0, 2.15, r"投影後到達 $H$", color=F.GREEN)
    ax.text(5.55, 4.35, r"$PH=3/\sqrt{5}$", color=F.RED)
    ax.set_xlim(-1, 7.4); ax.set_ylim(-.2, 6.2)
    F.clean_grid(ax); ax.legend(loc="upper left")
    ax.set_title("投影點在直線上，點線距離是垂直剩餘分量的長度")
    fig.tight_layout()
    return _save(fig, "數B3-3-投影點與點線距離.svg")


def fig_normal_vector():
    normal = np.array([2.0, -3.0]); direction = np.array([3.0, 2.0])
    point = np.array([1.0, 2.0])
    assert abs(np.dot(normal,direction)) < 1e-12
    assert math.isclose(np.dot(normal, point), -4)

    fig, ax = F.canvas(9.2, 5.5, equal=True)
    t = np.linspace(-1.4, 1.4, 2); line = point[None,:]+t[:,None]*direction
    ax.plot(line[:,0], line[:,1], color=F.BLUE, lw=2.4, label=r"$2x-3y+4=0$")
    F.arrow(ax, point, point+normal, color=F.RED)
    F.arrow(ax, point, point+direction, color=F.GREEN)
    _point(ax, point, "$P(1,2)$")
    ax.text(1.35, .85, r"法向量 $\vec n=(2,-3)$", color=F.RED)
    ax.text(3.0, 3.4, r"方向向量 $(3,2)$", color=F.GREEN)
    ax.text(-1.3, 5.3, r"$(2,-3)\cdot(3,2)=0$", fontsize=13)
    ax.set_xlim(-3.5, 5.6); ax.set_ylim(-1.0, 6.0)
    F.clean_grid(ax); ax.legend(loc="lower right")
    ax.set_title("直線方程式的 $x,y$ 係數組成法向量")
    fig.tight_layout()
    return _save(fig, "數B3-3-法向量與直線.svg")


def fig_perspective_grid():
    vanishing = np.array([5.0, 4.5])
    front_left = np.array([1.0, .6]); front_right = np.array([9.0, .6])
    depths = [0, .28, .52, .72, .88]
    crossbars = []
    for t in depths:
        left = (1-t)*front_left+t*vanishing
        right = (1-t)*front_right+t*vanishing
        crossbars.append((left,right))
        assert math.isclose(np.linalg.norm(right-left), (1-t)*8)

    fig, ax = F.schematic(10.4, 5.3)
    ax.plot([front_left[0], vanishing[0]], [front_left[1], vanishing[1]], color=F.INK, lw=2)
    ax.plot([front_right[0], vanishing[0]], [front_right[1], vanishing[1]], color=F.INK, lw=2)
    for i,(left,right) in enumerate(crossbars):
        ax.plot([left[0],right[0]],[left[1],right[1]], color=F.BLUE, lw=1.7)
        ax.text(right[0]+.12,right[1],f"$L_{i}$",fontsize=10)
    _point(ax, vanishing, "$V$ 消失點", color=F.RED, dx=.12, dy=.18)
    ax.plot([0,10],[4.5,4.5],color=F.AMBER,ls="--",label="地平線")
    ax.text(1.2, 4.72, "地平線", color=F.AMBER)
    ax.text(5, .12, "橫線保持平行；向深處的線在 $V$ 相交", ha="center")
    ax.set_xlim(0,10); ax.set_ylim(0,5.2)
    ax.set_title("單點透視把深度方向的平行線投向同一消失點")
    fig.tight_layout()
    return _save(fig, "數B3-3-單點透視等分.svg")


def fig_perspective_ratio():
    eye = np.array([0.0, 2.0]); screen_x = 3.0; object_x = 6.0
    bottom = np.array([object_x, 0.0]); top = np.array([object_x, 5.0])
    scale = screen_x/object_x
    screen_bottom = eye + scale*(bottom-eye)
    screen_top = eye + scale*(top-eye)
    assert np.allclose(screen_bottom, [3,1])
    assert np.allclose(screen_top, [3,3.5])
    assert math.isclose(screen_top[1]-screen_bottom[1], scale*5)

    fig, ax = F.canvas(10.0, 5.1, equal=True)
    ax.plot([0,6.5],[0,0],color=F.INK)
    ax.plot([screen_x,screen_x],[0,4.3],color=F.AMBER,lw=3,label="畫面")
    ax.plot([object_x,object_x],[0,5],color=F.BLUE,lw=5,label="實物高度 5")
    ax.plot([eye[0],top[0]],[eye[1],top[1]],color=F.RED,ls="--")
    ax.plot([eye[0],bottom[0]],[eye[1],bottom[1]],color=F.RED,ls="--")
    ax.plot([screen_x,screen_x],[screen_bottom[1],screen_top[1]],color=F.GREEN,lw=7,label="畫面高度 2.5")
    _point(ax, eye, "$E$", color=F.RED, dx=-.4, dy=.2)
    ax.text(1.5,.35,"距離 3",ha="center"); ax.text(4.5,.35,"距離 3",ha="center")
    ax.text(.45,4.55,r"相似三角形倍率 $3/6=1/2$",fontsize=13)
    ax.set_xlim(-.5,7); ax.set_ylim(-.2,5.4)
    ax.axis("off"); ax.legend(loc="upper center", ncol=3, fontsize=10)
    ax.set_title("透視尺寸由觀察距離的相似比決定")
    fig.tight_layout()
    return _save(fig, "數B3-3-透視比例.svg")


def fig_a_series():
    short = 1.0; long = math.sqrt(2)
    half = np.array([long/2, short])
    assert math.isclose(long/short, short/(long/2))
    assert math.isclose(short*long/2, (short*long)/2)

    fig, axes = plt.subplots(1, 2, figsize=(10.8, 4.6))
    for ax in axes: ax.set_aspect("equal"); ax.axis("off")
    axes[0].add_patch(Rectangle((0,0), short, long, facecolor=F.BLUE, alpha=.15, edgecolor=F.BLUE,lw=2))
    axes[0].plot([0,short],[long/2,long/2],color=F.RED,ls="--",lw=2)
    axes[0].text(.5,long+.08,r"短邊 $1$",ha="center")
    axes[0].text(-.08,long/2,r"長邊 $\sqrt{2}$",ha="right",va="center",rotation=90)
    axes[0].set_xlim(-.5,1.5); axes[0].set_ylim(-.2,1.75)
    axes[0].set_title("沿長邊對半裁切")
    axes[1].add_patch(Rectangle((0,0), short, long/2, facecolor=F.RED, alpha=.14, edgecolor=F.RED,lw=2))
    axes[1].text(.5,long/2+.08,r"長邊 $1$",ha="center")
    axes[1].text(-.08,long/4,r"短邊 $1/\sqrt{2}$",ha="right",va="center",rotation=90)
    axes[1].set_xlim(-.5,1.5); axes[1].set_ylim(-.2,1.75)
    axes[1].set_title(r"旋轉後比例仍為 $\sqrt{2}:1$")
    fig.suptitle("A 系列紙張以相似性固定長寬比，每裁一次面積減半",fontsize=15)
    fig.tight_layout()
    return _save(fig, "數B3-3-A系列紙張.svg")


def fig_fibonacci_ratio():
    f = [1,1]
    for _ in range(10): f.append(f[-1]+f[-2])
    n = np.arange(2,len(f)+1)
    ratios = np.array([f[i]/f[i-1] for i in range(1,len(f))])
    phi = (1+math.sqrt(5))/2
    assert abs(ratios[-1]-phi) < .001
    assert f[-1] == 144

    fig, ax = plt.subplots(figsize=(10.4, 5.0))
    ax.plot(n,ratios,marker="o",color=F.BLUE,lw=2.2,label=r"$F_n/F_{n-1}$")
    ax.axhline(phi,color=F.RED,ls="--",lw=2,label=fr"$\varphi={phi:.6f}$")
    for x,y in zip(n[-4:],ratios[-4:]): ax.text(x,y+.025,f"{y:.3f}",ha="center",fontsize=9)
    ax.set_xlabel("項次 $n$"); ax.set_ylabel("相鄰兩項比")
    ax.set_ylim(1.45,1.72); ax.legend(loc="upper right")
    F.clean_grid(ax)
    ax.set_title("費氏數列相鄰比在黃金比例上下交替接近")
    fig.tight_layout()
    return _save(fig, "數B3-3-費氏比值.svg")


def fig_golden_spiral():
    phi = (1+math.sqrt(5))/2
    assert math.isclose(phi*phi,phi+1)
    rect = np.array([[0,0],[phi,0],[phi,1],[0,1]])
    fig, ax = F.schematic(9.5, 5.6)
    ax.add_patch(Polygon(rect,closed=True,fill=False,edgecolor=F.INK,lw=2))
    ax.plot([1,1],[0,1],color=F.BLUE,lw=2)
    ax.add_patch(Arc((1,1),2,2,theta1=180,theta2=270,color=F.RED,lw=2.5))
    ax.add_patch(Arc((1,1/phi),2/phi,2/phi,theta1=270,theta2=360,color=F.RED,lw=2.5))
    ax.text(.5,.5,"正方形\n" + r"$1\times1$",ha="center",va="center")
    ax.text(1+(phi-1)/2,.5,"餘下矩形\n仍相似",ha="center",va="center")
    ax.text(phi/2,-.2,r"長邊 $\varphi$",ha="center")
    ax.text(-.12,.5,"短邊 1",rotation=90,va="center",ha="right")
    ax.text(phi/2,1.28,r"$\varphi^2=\varphi+1$ 使切除正方形後仍保持比例",ha="center",fontsize=13)
    ax.set_xlim(-.5,phi+.6); ax.set_ylim(-.5,1.7)
    ax.set_title("黃金矩形中的四分之一圓弧形成方形螺線近似")
    fig.tight_layout()
    return _save(fig, "數B3-3-黃金分割與方形螺線.svg")


def fig_rounded_corner():
    radius = 1.6; center = np.array([radius,radius])
    tangent_x = np.array([radius,0.0]); tangent_y = np.array([0.0,radius])
    assert math.isclose(np.linalg.norm(center-tangent_x),radius)
    assert math.isclose(np.dot(center-tangent_x,[1,0]),0)
    assert math.isclose(np.dot(center-tangent_y,[0,1]),0)
    arc_length = radius*math.pi/2
    assert math.isclose(arc_length,.8*math.pi)

    fig, ax = F.canvas(8.2, 5.5, equal=True)
    ax.plot([0,4.7],[0,0],color=F.INK,lw=3)
    ax.plot([0,0],[0,4.7],color=F.INK,lw=3)
    ax.add_patch(Arc(center,2*radius,2*radius,theta1=180,theta2=270,color=F.RED,lw=4))
    ax.plot([0,center[0]],[0,center[1]],color=F.AMBER,ls="--",label="角平分線")
    ax.plot([center[0],tangent_x[0]],[center[1],tangent_x[1]],color=F.BLUE,ls="--")
    ax.plot([center[0],tangent_y[0]],[center[1],tangent_y[1]],color=F.BLUE,ls="--")
    _point(ax, center, "$C(r,r)$", color=F.BLUE)
    _point(ax, tangent_x, "$T_1$", color=F.RED,dx=.1,dy=-.35)
    _point(ax, tangent_y, "$T_2$", color=F.RED,dx=-.6,dy=.1)
    ax.text(2.45,2.45,"圓心在角平分線上",color=F.AMBER)
    ax.text(2.35,.8,r"$CT_1\perp$ 邊",color=F.BLUE)
    ax.text(.6,2.55,r"$CT_2\perp$ 邊",color=F.BLUE,rotation=90)
    ax.set_xlim(-.5,5); ax.set_ylim(-.5,5)
    ax.axis("off")
    ax.set_title(r"直角圓角：切點距頂點皆為 $r$，弧長為 $\pi r/2$")
    fig.tight_layout()
    return _save(fig, "數B3-3-圓角切線幾何.svg")


def main():
    functions = {name: globals()[name] for name, _ in FIGURE_OUTPUTS}
    assert len(functions) == len(FIGURE_OUTPUTS)
    outputs = []
    for function_name, filename in FIGURE_OUTPUTS:
        path = functions[function_name]()
        assert os.path.basename(path) == filename
        outputs.append(path)
    assert len(outputs) == len(set(outputs)) == len(FIGURE_OUTPUTS)
    print(f"verified {len(outputs)} chapter SVG files; write_pdf=False")


if __name__ == "__main__":
    main()
