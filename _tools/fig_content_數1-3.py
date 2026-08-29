# -*- coding: utf-8 -*-
"""重生「數1-3 多項式函數」學生講義的章內 SVG。"""

if __name__ == "__main__" and __import__("sys").argv[1:]:
    raise SystemExit("本腳本不接受參數；直接執行即可重生數1-3 章內 SVG。")

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import matplotlib.pyplot as plt
import numpy as np

import figlib as F


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHAPTER = os.path.join(ROOT, "content", "必修數學", "數1-3")

FIGURE_OUTPUTS = (
    ("fig_synthetic_division", "數1-3-綜合除法.svg"),
    ("fig_coordinate_symmetry", "數1-3-坐標對稱.svg"),
    ("fig_basic_functions", "數1-3-常數與一次函數.svg"),
    ("fig_quadratic_parameters", "數1-3-二次基本圖形.svg"),
    ("fig_quadratic_vertex", "數1-3-配方與頂點.svg"),
    ("fig_discriminant", "數1-3-判別式三情形.svg"),
    ("fig_interval_extrema", "數1-3-閉區間極值.svg"),
    ("fig_cubic_standard", "數1-3-三次標準形.svg"),
    ("fig_cubic_translation", "數1-3-三次平移與對稱中心.svg"),
    ("fig_local_linear", "數1-3-局部一次近似.svg"),
    ("fig_sign_chart", "數1-3-重根與變號.svg"),
)


def _save(fig, filename):
    stem, extension = os.path.splitext(filename)
    if extension != ".svg" or not stem.startswith("數1-3-"):
        raise AssertionError("輸出檔名必須是數1-3 章內 SVG")
    return F.save_to(fig, CHAPTER, stem, output_subdir="assets", write_pdf=False)


def _axes_at_origin(ax):
    ax.axhline(0, color=F.INK, lw=1.15, zorder=0)
    ax.axvline(0, color=F.INK, lw=1.15, zorder=0)
    F.clean_grid(ax)


def fig_synthetic_division():
    coefficients = np.array([2, -3, 0, 5], dtype=int)
    a = 2
    bottom = [coefficients[0]]
    products = []
    for coefficient in coefficients[1:]:
        products.append(a * bottom[-1])
        bottom.append(int(coefficient + products[-1]))
    assert bottom == [2, 1, 2, 9]
    assert np.polyval(coefficients, a) == bottom[-1]
    assert np.allclose(np.polyadd(np.polymul([1, -a], bottom[:-1]), [bottom[-1]]), coefficients)

    fig, ax = plt.subplots(figsize=(10.6, 4.5))
    ax.set_xlim(-1.4, 5.8)
    ax.set_ylim(-0.7, 3.7)
    ax.axis("off")
    xs = np.array([0.7, 2.0, 3.3, 4.6])
    ax.text(-0.55, 2.60, "$2$", fontsize=18, color=F.AMBER, ha="center")
    ax.plot([-0.15, -0.15], [0.40, 3.05], color=F.INK, lw=1.5)
    ax.plot([-0.15, 5.15], [1.35, 1.35], color=F.INK, lw=1.5)
    for x, value in zip(xs, coefficients):
        ax.text(x, 2.65, f"${value}$", fontsize=18, ha="center", color=F.INK)
    ax.text(xs[0], 0.72, "$2$", fontsize=18, ha="center", color=F.BLUE)
    for index, (product, value) in enumerate(zip(products, bottom[1:]), start=1):
        ax.annotate("", xy=(xs[index] - 0.10, 2.18), xytext=(xs[index - 1] + 0.10, 0.98),
                    arrowprops=dict(arrowstyle="->", color=F.GREEN, lw=1.5))
        ax.text(xs[index], 1.72, f"${product}$", fontsize=15, ha="center", color=F.GREEN)
        ax.text(xs[index], 0.72, f"${value}$", fontsize=18, ha="center",
                color=F.AMBER if index == 3 else F.BLUE)
    ax.text(2.55, 0.12, r"商的係數 $2,1,2$", fontsize=13, color=F.BLUE, ha="center")
    ax.text(4.60, 0.12, r"餘式 $9=f(2)$", fontsize=13, color=F.AMBER, ha="center")
    ax.set_title(r"$2x^3-3x^2+0x+5$ 除以 $x-2$：落下、乘 $2$、相加", fontsize=15)
    fig.tight_layout()
    return _save(fig, "數1-3-綜合除法.svg")


def fig_coordinate_symmetry():
    point = np.array([3.0, 2.0])
    images = {
        "原點": -point,
        "$x$ 軸": point * [1, -1],
        "$y$ 軸": point * [-1, 1],
        "$y=x$": point[::-1],
    }
    assert np.allclose(images["原點"], [-3, -2])
    assert np.allclose(images["$y=x$"], [2, 3])
    assert np.isclose(np.linalg.norm(point), np.linalg.norm(images["原點"]))

    fig, ax = plt.subplots(figsize=(8.0, 6.6))
    _axes_at_origin(ax)
    ax.plot([-4.2, 4.2], [-4.2, 4.2], ls="--", lw=1.5, color=F.GRID)
    ax.scatter(*point, s=85, color=F.BLUE, zorder=4)
    ax.text(point[0] + .12, point[1] + .12, "$P(3,2)$", color=F.BLUE, fontsize=11)
    colors = [F.AMBER, F.GREEN, F.GREEN, F.AMBER]
    for (label, image), color in zip(images.items(), colors):
        ax.scatter(*image, s=72, color=color, zorder=4)
        ax.plot([point[0], image[0]], [point[1], image[1]], ls=":", color=color, lw=1.2)
        ax.annotate(label, image, xytext=(7, 7), textcoords="offset points", fontsize=10, color=color)
    ax.text(3.20, 3.55, "$y=x$", color=F.INK, fontsize=11)
    ax.set_xlim(-4.2, 4.2)
    ax.set_ylim(-4.0, 4.2)
    ax.set_aspect("equal", adjustable="box")
    ax.set_title("坐標對稱由鏡射或旋轉直接決定坐標", fontsize=15)
    fig.tight_layout()
    return _save(fig, "數1-3-坐標對稱.svg")


def fig_basic_functions():
    x = np.linspace(-4, 4, 401)
    lines = (
        (np.full_like(x, 2.0), r"$y=2$", F.AMBER),
        (0.75 * x - 1, r"$y=0.75x-1$", F.BLUE),
        (-1.25 * x + 2, r"$y=-1.25x+2$", F.GREEN),
    )
    assert np.isclose(lines[1][0][200], -1)
    assert np.isclose((lines[1][0][-1] - lines[1][0][0]) / (x[-1] - x[0]), .75)
    assert np.isclose((lines[2][0][-1] - lines[2][0][0]) / (x[-1] - x[0]), -1.25)

    fig, ax = plt.subplots(figsize=(9.5, 5.4))
    for y, label, color in lines:
        ax.plot(x, y, lw=2.5, color=color, label=label)
    _axes_at_origin(ax)
    ax.scatter([0, 0, 0], [2, -1, 2], s=45, color=[F.AMBER, F.BLUE, F.GREEN], zorder=4)
    ax.set_xlim(-4, 4)
    ax.set_ylim(-4, 6)
    ax.set_xlabel("$x$")
    ax.set_ylabel("$y$")
    ax.legend(frameon=False, ncol=3, loc="upper center")
    ax.set_title("常數函數固定輸出；一次函數的斜率控制每單位變化量", fontsize=15)
    fig.tight_layout()
    return _save(fig, "數1-3-常數與一次函數.svg")


def fig_quadratic_parameters():
    x = np.linspace(-2.4, 2.4, 401)
    specs = ((1.0, F.BLUE), (2.0, F.GREEN), (-1.0, F.AMBER))
    fig, ax = plt.subplots(figsize=(9.5, 5.5))
    for a, color in specs:
        y = a * x**2
        assert np.isclose(y[200], 0)
        assert np.allclose(a * (-x)**2, y)
        label = "$y=x^2$" if a == 1 else "$y=-x^2$" if a == -1 else rf"$y={a:g}x^2$"
        ax.plot(x, y, lw=2.5, color=color, label=label)
    _axes_at_origin(ax)
    ax.set_xlim(-2.4, 2.4)
    ax.set_ylim(-5.5, 8.5)
    ax.set_xlabel("$x$")
    ax.set_ylabel("$y$")
    ax.legend(frameon=False, ncol=3, loc="upper center")
    ax.set_title(r"$a$ 決定開口方向；$|a|$ 決定同一高度所需的水平距離", fontsize=15)
    fig.tight_layout()
    return _save(fig, "數1-3-二次基本圖形.svg")


def fig_quadratic_vertex():
    x = np.linspace(-.5, 4.5, 501)
    y = 2 * x**2 - 8 * x + 5
    h, k = 2.0, -3.0
    roots = np.sort(np.roots([2, -8, 5]))
    assert np.isclose(np.polyval([2, -8, 5], h), k)
    assert np.allclose(np.polyval([2, -8, 5], roots), 0, atol=1e-10)
    assert np.allclose(roots, [2 - np.sqrt(6) / 2, 2 + np.sqrt(6) / 2])

    fig, ax = plt.subplots(figsize=(9.5, 5.5))
    ax.plot(x, y, color=F.BLUE, lw=2.8, label=r"$y=2x^2-8x+5=2(x-2)^2-3$")
    ax.axvline(h, color=F.GRID, ls="--", lw=1.4)
    ax.scatter([h], [k], s=95, color=F.AMBER, zorder=5)
    ax.scatter(roots, [0, 0], s=65, color=F.GREEN, zorder=5)
    ax.annotate("頂點 $(2,-3)$", (h, k), xytext=(22, -2), textcoords="offset points",
                arrowprops=dict(arrowstyle="->", color=F.AMBER), color=F.AMBER, fontsize=11)
    ax.text(h + .08, 8.2, "對稱軸 $x=2$", fontsize=10, color=F.INK)
    _axes_at_origin(ax)
    ax.set_xlim(-.5, 4.5)
    ax.set_ylim(-4.2, 10)
    ax.legend(frameon=False, loc="upper center")
    ax.set_title("配方把垂直位移、水平位移與伸縮直接寫入方程", fontsize=15)
    fig.tight_layout()
    return _save(fig, "數1-3-配方與頂點.svg")


def fig_discriminant():
    x = np.linspace(-2.7, 2.7, 501)
    specs = (
        (x**2 - 1, "$D>0$：穿越兩次", F.BLUE, [-1, 1]),
        ((x - .5)**2, "$D=0$：相切一次", F.GREEN, [.5]),
        (x**2 + 1, "$D<0$：沒有交點", F.AMBER, []),
    )
    fig, axes = plt.subplots(1, 3, figsize=(11.3, 4.1), sharey=True)
    for ax, (y, title, color, roots) in zip(axes, specs):
        ax.plot(x, y, lw=2.5, color=color)
        _axes_at_origin(ax)
        if roots:
            ax.scatter(roots, np.zeros(len(roots)), s=55, color=color, zorder=4)
        ax.set_xlim(-2.7, 2.7)
        ax.set_ylim(-1.5, 5.2)
        ax.set_title(title, fontsize=12)
    assert np.allclose(np.sort(np.roots([1, 0, -1])), [-1, 1])
    assert np.isclose(np.roots([1, -1, .25])[0], .5)
    assert not np.isreal(np.roots([1, 0, 1])).any()
    fig.suptitle("判別式控制拋物線與 $x$ 軸的交點數", fontsize=15)
    fig.tight_layout(rect=(0, 0, 1, .91))
    return _save(fig, "數1-3-判別式三情形.svg")


def fig_interval_extrema():
    x = np.linspace(-.5, 3.5, 401)
    y = (x - 2)**2 - 3
    candidates = np.array([0., 2., 3.])
    values = (candidates - 2)**2 - 3
    assert np.allclose(values, [1, -3, -2])
    assert values.min() == -3 and values.max() == 1

    fig, ax = plt.subplots(figsize=(9.5, 5.2))
    ax.plot(x, y, color=F.GRID, lw=1.8)
    mask = (x >= 0) & (x <= 3)
    ax.plot(x[mask], y[mask], color=F.BLUE, lw=3.4, label=r"限制在 $[0,3]$")
    ax.scatter(candidates, values, s=[75, 100, 75], color=[F.GREEN, F.AMBER, F.GREEN], zorder=5)
    for cx, cy, label in zip(candidates, values, ["左端點：1", "頂點：-3", "右端點：-2"]):
        ax.annotate(label, (cx, cy), xytext=(6, 10), textcoords="offset points", fontsize=10)
    _axes_at_origin(ax)
    ax.set_xlim(-.5, 3.5)
    ax.set_ylim(-4, 4)
    ax.legend(frameon=False)
    ax.set_title("閉區間上的二次極值來自可取到的頂點與兩個端點", fontsize=15)
    fig.tight_layout()
    return _save(fig, "數1-3-閉區間極值.svg")


def fig_cubic_standard():
    x = np.linspace(-2.4, 2.4, 701)
    specs = ((1, 2, F.BLUE), (1, -2, F.GREEN), (-1, 2, F.AMBER), (-1, -2, F.RED))
    fig, axes = plt.subplots(2, 2, figsize=(10.6, 7.8), sharex=True, sharey=True)
    for ax, (a, p, color) in zip(axes.flat, specs):
        y = a * x**3 + p * x
        assert np.allclose(a * (-x)**3 + p * (-x), -y)
        assert np.sign(y[-1]) == np.sign(a) and np.sign(y[0]) == -np.sign(a)
        ax.plot(x, y, color=color, lw=2.5)
        _axes_at_origin(ax)
        ax.set_xlim(-2.4, 2.4)
        ax.set_ylim(-9, 9)
        cubic = "x^3" if a == 1 else "-x^3"
        linear = f"+{p:g}x" if p > 0 else f"{p:g}x"
        ax.set_title(rf"$y={cubic}{linear}$", fontsize=12)
    fig.suptitle(r"三次標準形 $y=ax^3+px$：關於原點點對稱，兩端由 $a$ 決定", fontsize=15)
    fig.tight_layout(rect=(0, 0, 1, .94))
    return _save(fig, "數1-3-三次標準形.svg")


def fig_cubic_translation():
    u = np.linspace(-2.7, 2.7, 601)
    g = u**3 - 3 * u
    x = u + 1
    f = x**3 - 3 * x**2 + 2
    assert np.allclose(f, g)
    assert np.isclose(np.polyval([1, -3, 0, 2], 1), 0)
    paired_u = np.array([-1.5, -.8, .8, 1.5])
    paired_y = paired_u**3 - 3 * paired_u
    assert np.allclose(paired_y[:2], -paired_y[:1:-1])

    fig, ax = plt.subplots(figsize=(9.7, 5.6))
    ax.plot(u, g, color=F.GRID, lw=2, ls="--", label=r"$g(u)=u^3-3u$")
    ax.plot(x, f, color=F.BLUE, lw=2.8, label=r"$f(x)=g(x-1)=x^3-3x^2+2$")
    ax.scatter([0, 1], [0, 0], color=[F.GRID, F.AMBER], s=[55, 95], zorder=5)
    ax.annotate("對稱中心 $(1,0)$", (1, 0), xytext=(18, 28), textcoords="offset points",
                arrowprops=dict(arrowstyle="->", color=F.AMBER), color=F.AMBER, fontsize=11)
    ax.annotate("向右平移 1", xy=(1.0, 5.4), xytext=(0.0, 5.4),
                arrowprops=dict(arrowstyle="->", color=F.GREEN, lw=1.8),
                ha="center", va="bottom", color=F.GREEN, fontsize=11)
    _axes_at_origin(ax)
    ax.set_xlim(-2.8, 3.8)
    ax.set_ylim(-7, 7)
    ax.legend(frameon=False, loc="lower right")
    ax.set_title("消去二次項後，平移量同時給出三次圖形的對稱中心", fontsize=15)
    fig.tight_layout()
    return _save(fig, "數1-3-三次平移與對稱中心.svg")


def fig_local_linear():
    h = -2.0
    x = np.linspace(h - .75, h + .75, 601)
    u = x - h
    exact = 2 * x**3 + 6 * x**2 + 3 * x - 3
    linear = 3 * u - 1
    remainder = exact - linear
    assert np.allclose(exact, 2 * u**3 - 6 * u**2 + 3 * u - 1)
    assert np.isclose(exact[300], linear[300])
    assert np.isclose(remainder[np.argmin(abs(u - .1))], 2 * .1**3 - 6 * .1**2, atol=1e-9)

    fig, axes = plt.subplots(1, 2, figsize=(11.2, 4.6))
    axes[0].plot(x, exact, color=F.BLUE, lw=2.7, label="$f(x)$")
    axes[0].plot(x, linear, color=F.AMBER, lw=2.2, ls="--", label=r"$3(x+2)-1$")
    axes[0].scatter([h], [-1], s=80, color=F.GREEN, zorder=5)
    axes[0].axvline(h, color=F.GRID, lw=1.2, ls=":")
    axes[0].set_xlabel("$x$")
    axes[0].set_ylabel("函數值")
    axes[0].legend(frameon=False)
    axes[0].set_title("在 $x=-2$ 附近保留常數項與一次項", fontsize=12)
    F.clean_grid(axes[0])
    axes[1].plot(u, np.abs(remainder), color=F.GREEN, lw=2.7)
    axes[1].axvline(0, color=F.GRID, lw=1.2)
    axes[1].set_xlabel(r"距中心的位移 $u=x+2$")
    axes[1].set_ylabel(r"近似誤差 $|f(x)-(3u-1)|$")
    axes[1].set_title("高次項隨 $|u|$ 縮小而迅速減弱", fontsize=12)
    F.clean_grid(axes[1])
    fig.suptitle("連續綜合除法把局部一次近似與剩餘高次項分開", fontsize=15)
    fig.tight_layout(rect=(0, 0, 1, .92))
    return _save(fig, "數1-3-局部一次近似.svg")


def fig_sign_chart():
    roots = np.array([-2., 1., 3.])
    samples = np.array([-3., -1., 2., 4.])
    polynomial = lambda z: (z + 2) * (z - 1)**2 * (z - 3)
    signs = np.sign(polynomial(samples)).astype(int)
    assert signs.tolist() == [1, -1, -1, 1]
    assert np.isclose(polynomial(1), 0)
    assert np.sign(polynomial(.9)) == np.sign(polynomial(1.1))
    assert np.sign(polynomial(-2.1)) != np.sign(polynomial(-1.9))

    fig, axes = plt.subplots(2, 1, figsize=(10.6, 6.2), gridspec_kw={"height_ratios": [2.2, 1]})
    x = np.linspace(-3.5, 4.5, 1001)
    y = polynomial(x)
    axes[0].plot(x, y, color=F.BLUE, lw=2.5)
    axes[0].scatter(roots, np.zeros(3), s=[70, 95, 70], color=[F.GREEN, F.AMBER, F.GREEN], zorder=5)
    axes[0].annotate("偶重根：接觸後留在同側", (1, 0), xytext=(1.35, 35),
                     arrowprops=dict(arrowstyle="->", color=F.AMBER), color=F.AMBER, fontsize=10)
    axes[0].set_xlim(-3.5, 4.5)
    axes[0].set_ylim(-45, 80)
    axes[0].set_title(r"$P(x)=(x+2)(x-1)^2(x-3)$", fontsize=13)
    _axes_at_origin(axes[0])
    ax = axes[1]
    ax.set_xlim(-3.5, 4.5)
    ax.set_ylim(-.6, .8)
    ax.axhline(0, color=F.INK, lw=1.8)
    for root, multiplicity in zip(roots, [1, 2, 1]):
        ax.scatter([root], [0], s=75, color=F.AMBER if multiplicity == 2 else F.GREEN, zorder=5)
        ax.text(root, -.34, f"{root:g}\n重數 {multiplicity}", ha="center", fontsize=9)
    for left, right, sign in zip([-3.5, -2, 1, 3], [-2, 1, 3, 4.5], signs):
        color = F.BLUE if sign > 0 else F.RED
        ax.plot([left, right], [.28, .28], lw=7, color=color, solid_capstyle="butt")
        ax.text((left + right) / 2, .48, "+" if sign > 0 else "−", ha="center", color=color, fontsize=14)
    ax.axis("off")
    fig.suptitle("奇重根穿越並變號；偶重根相切且不變號", fontsize=15)
    fig.tight_layout(rect=(0, 0, 1, .94))
    return _save(fig, "數1-3-重根與變號.svg")


if __name__ == "__main__":
    for entrypoint, filename in FIGURE_OUTPUTS:
        output = globals()[entrypoint]()
        if os.path.basename(output) != filename:
            raise AssertionError(f"{entrypoint} 輸出與 FIGURE_OUTPUTS 不一致")
