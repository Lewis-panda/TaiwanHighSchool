# -*- coding: utf-8 -*-
"""重生「數B3-1 正弦函數與週期性現象」學生講義的章內 SVG。"""

if __name__ == "__main__" and __import__("sys").argv[1:]:
    raise SystemExit("本腳本不接受參數；直接執行即可重生數B3-1 章內 SVG。")

import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import matplotlib.pyplot as plt
from matplotlib.patches import Arc, Circle, Rectangle, Wedge
import numpy as np

import figlib as F


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHAPTER = os.path.join(ROOT, "content", "數學B", "數B3-1")

FIGURE_OUTPUTS = (
    ("fig_one_radian", "數B3-1-一弧度定義.svg"),
    ("fig_angle_conversion", "數B3-1-度與弧度對照.svg"),
    ("fig_sector", "數B3-1-弧長與扇形面積.svg"),
    ("fig_clock_sweep", "數B3-1-時鐘掃掠.svg"),
    ("fig_discrete_period", "數B3-1-離散週期.svg"),
    ("fig_unit_circle", "數B3-1-單位圓與正弦.svg"),
    ("fig_sine_graph", "數B3-1-正弦關鍵點.svg"),
    ("fig_sine_inequality", "數B3-1-正弦方程與不等式.svg"),
    ("fig_transform", "數B3-1-正弦平移伸縮.svg"),
    ("fig_parameter_model", "數B3-1-週期模型參數.svg"),
    ("fig_ferris_wheel", "數B3-1-摩天輪模型.svg"),
    ("fig_sound_frequency", "數B3-1-聲波週期與頻率.svg"),
)


def _save(fig, filename):
    stem, extension = os.path.splitext(filename)
    if extension != ".svg" or not stem.startswith("數B3-1-"):
        raise AssertionError("輸出檔名必須是數B3-1 章內 SVG")
    return F.save_to(
        fig, CHAPTER, stem, output_subdir="assets", write_pdf=False
    )


def _axes_through_origin(ax):
    ax.spines["left"].set_position("zero")
    ax.spines["bottom"].set_position("zero")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(True, color=F.GRID, lw=.8)
    ax.set_axisbelow(True)


def fig_one_radian():
    radius = 2.4
    theta = 1.0
    arc_length = radius * theta
    assert math.isclose(arc_length / radius, 1.0)

    fig, ax = F.schematic(8.2, 5.5)
    ax.set_xlim(-3.2, 4.7)
    ax.set_ylim(-2.9, 3.0)
    ax.add_patch(Circle((0, 0), radius, fill=False, edgecolor=F.GRID, lw=1.4))
    p0 = np.array([radius, 0.0])
    p1 = radius * np.array([math.cos(theta), math.sin(theta)])
    ax.plot([0, p0[0]], [0, p0[1]], color=F.BLUE, lw=2.5)
    ax.plot([0, p1[0]], [0, p1[1]], color=F.BLUE, lw=2.5)
    angles = np.linspace(0, theta, 120)
    ax.plot(radius * np.cos(angles), radius * np.sin(angles), color=F.RED, lw=5)
    ax.add_patch(Arc((0, 0), 1.45, 1.45, theta1=0,
                     theta2=math.degrees(theta), color=F.AMBER, lw=2.2))
    ax.scatter([0], [0], color=F.INK, s=30, zorder=5)
    ax.text(1.18, -.24, r"半徑 $r$", color=F.BLUE, ha="center")
    mid = theta / 2
    ax.text(radius * math.cos(mid) + .15, radius * math.sin(mid) + .25,
            r"弧長 $s=r$", color=F.RED, ha="center")
    ax.text(.95 * math.cos(mid), .95 * math.sin(mid), r"$1$ 弧度",
            color=F.AMBER, ha="center", va="center")
    ax.text(3.35, .55, r"$\theta=\dfrac{s}{r}=1$", fontsize=15,
            bbox=dict(boxstyle="round,pad=.35", fc="#fff8e6", ec=F.AMBER))
    ax.text(3.35, -.45, "角度由弧長與半徑的比值定義", ha="center", fontsize=11)
    ax.set_title("弧長等於半徑時，圓心角是 1 弧度", fontsize=15)
    fig.tight_layout()
    return _save(fig, "數B3-1-一弧度定義.svg")


def fig_angle_conversion():
    degree_values = np.array([0, 30, 45, 60, 90, 120, 180, 270])
    radian_values = np.deg2rad(degree_values)
    assert np.allclose(radian_values, degree_values * math.pi / 180)
    assert math.isclose(np.deg2rad(360), 2 * math.pi)

    fig, ax = F.schematic(10.2, 6.1)
    ax.set_xlim(-3.3, 6.8)
    ax.set_ylim(-3.1, 3.2)
    radius = 2.35
    ax.add_patch(Circle((0, 0), radius, fill=False, edgecolor=F.INK, lw=1.5))
    ax.axhline(0, xmin=.07, xmax=.55, color=F.GRID, lw=1)
    ax.axvline(0, ymin=.12, ymax=.89, color=F.GRID, lw=1)
    labels = [
        (0, r"$0^\circ=0$"),
        (30, r"$30^\circ=\pi/6$"),
        (45, r"$45^\circ=\pi/4$"),
        (60, r"$60^\circ=\pi/3$"),
        (90, r"$90^\circ=\pi/2$"),
        (120, r"$120^\circ=2\pi/3$"),
        (180, r"$180^\circ=\pi$"),
        (270, r"$270^\circ=3\pi/2$"),
    ]
    for degree, label in labels:
        angle = math.radians(degree)
        x, y = radius * math.cos(angle), radius * math.sin(angle)
        ax.plot([0, x], [0, y], color=F.BLUE, alpha=.52, lw=1.25)
        ax.scatter([x], [y], s=25, color=F.BLUE, zorder=4)
        rr = radius + (.63 if degree in (30, 45, 60, 120) else .45)
        ha = "left" if math.cos(angle) > .12 else ("right" if math.cos(angle) < -.12 else "center")
        ax.text(rr * math.cos(angle), rr * math.sin(angle), label,
                ha=ha, va="center", fontsize=9.6)
    ax.text(4.55, 1.15, r"度 $\longrightarrow$ 弧度", ha="center", fontsize=13)
    ax.text(4.55, .55, r"$\alpha^\circ\times\dfrac{\pi}{180}$", ha="center", fontsize=16,
            color=F.BLUE)
    ax.text(4.55, -.45, r"弧度 $\longrightarrow$ 度", ha="center", fontsize=13)
    ax.text(4.55, -1.05, r"$\theta\times\dfrac{180}{\pi}$", ha="center", fontsize=16,
            color=F.RED)
    ax.text(4.55, -2.05, r"一整圈：$360^\circ=2\pi$", ha="center",
            bbox=dict(boxstyle="round,pad=.35", fc="#eef5ff", ec=F.BLUE))
    ax.set_title("同一個角可用度數或弧度表示", fontsize=15)
    fig.tight_layout()
    return _save(fig, "數B3-1-度與弧度對照.svg")


def fig_sector():
    r = 3.0
    theta = 2 * math.pi / 3
    s = r * theta
    area = .5 * r * r * theta
    assert math.isclose(s, 2 * math.pi)
    assert math.isclose(area, 3 * math.pi)
    assert math.isclose(area, .5 * r * s)

    fig, axes = plt.subplots(1, 2, figsize=(11.6, 5.1))
    ax = axes[0]
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_xlim(-3.5, 3.7)
    ax.set_ylim(-1, 3.8)
    ax.add_patch(Wedge((0, 0), r, 0, math.degrees(theta),
                       facecolor="#eaf2ff", edgecolor=F.BLUE, lw=2))
    angles = np.linspace(0, theta, 100)
    ax.plot(r * np.cos(angles), r * np.sin(angles), color=F.RED, lw=4)
    ax.add_patch(Arc((0, 0), 1.2, 1.2, theta1=0, theta2=math.degrees(theta),
                     color=F.AMBER, lw=2))
    ax.text(.82 * math.cos(theta / 2), .82 * math.sin(theta / 2), r"$\theta$",
            color=F.AMBER, ha="center")
    ax.text(1.45, -.25, r"$r$", color=F.BLUE)
    ax.text(r * math.cos(theta / 2) - .15, r * math.sin(theta / 2) + .35,
            r"弧長 $s=r\theta$", color=F.RED, ha="center")
    ax.set_title(r"扇形占整圓的比例是 $\theta/(2\pi)$")

    ax = axes[1]
    ax.axis("off")
    ax.set_xlim(0, 6)
    ax.set_ylim(0, 5)
    formulas = [
        (3.65, r"$s=2\pi r\cdot\dfrac{\theta}{2\pi}=r\theta$", F.BLUE),
        (2.65, r"$A=\pi r^2\cdot\dfrac{\theta}{2\pi}=\dfrac{1}{2}r^2\theta$", F.GREEN),
        (1.65, r"$A=\dfrac{1}{2}rs$", F.PURPLE),
    ]
    for y, text, color in formulas:
        ax.text(3, y, text, ha="center", fontsize=16, color=color,
                bbox=dict(boxstyle="round,pad=.3", fc="white", ec=color))
    ax.text(3, .6, r"例：$r=3,\ \theta=2\pi/3\Rightarrow s=2\pi,\ A=3\pi$",
            ha="center", fontsize=11)
    ax.set_title("弧度讓弧長與面積公式直接保留比例")
    fig.tight_layout()
    return _save(fig, "數B3-1-弧長與扇形面積.svg")


def fig_clock_sweep():
    minutes = 35
    r = 12.0
    theta = 2 * math.pi * minutes / 60
    path = r * theta
    area = .5 * r * r * theta
    assert math.isclose(theta, 7 * math.pi / 6)
    assert math.isclose(path, 14 * math.pi)
    assert math.isclose(area, 84 * math.pi)

    fig, axes = plt.subplots(1, 2, figsize=(11.4, 5.2))
    ax = axes[0]
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_xlim(-1.2, 1.2)
    ax.set_ylim(-1.2, 1.2)
    ax.add_patch(Circle((0, 0), 1, fill=False, edgecolor=F.INK, lw=1.6))
    for k in range(12):
        a = math.pi / 2 - 2 * math.pi * k / 12
        ax.plot([.90 * math.cos(a), math.cos(a)], [.90 * math.sin(a), math.sin(a)],
                color=F.GRID, lw=2)
    start = math.pi / 2
    end = start - theta
    sweep = np.linspace(start, end, 140)
    ax.fill(np.r_[0, .92 * np.cos(sweep), 0], np.r_[0, .92 * np.sin(sweep), 0],
            color=F.BLUE, alpha=.15)
    ax.plot(.94 * np.cos(sweep), .94 * np.sin(sweep), color=F.RED, lw=4)
    ax.plot([0, .83 * math.cos(start)], [0, .83 * math.sin(start)], color=F.BLUE, lw=2)
    ax.plot([0, .83 * math.cos(end)], [0, .83 * math.sin(end)], color=F.BLUE, lw=2)
    ax.text(0, -1.14, r"分針 35 分鐘掃過 $7\pi/6$ 弧度", ha="center", fontsize=11)
    ax.set_title("分針的角速度固定")

    ax = axes[1]
    ax.axis("off")
    ax.set_xlim(0, 6)
    ax.set_ylim(0, 5)
    ax.text(3, 4.05, r"$\theta=2\pi\times\dfrac{35}{60}=\dfrac{7\pi}{6}$",
            ha="center", fontsize=16, color=F.BLUE)
    ax.text(3, 2.85, r"針尖路程 $s=12\cdot\dfrac{7\pi}{6}=14\pi$ cm",
            ha="center", fontsize=14, color=F.RED)
    ax.text(3, 1.70, r"掃過面積 $A=\dfrac{1}{2}(12)^2\dfrac{7\pi}{6}=84\pi$ cm$^2$",
            ha="center", fontsize=14, color=F.GREEN)
    ax.text(3, .65, "時間比例先換成轉角，再交給扇形公式", ha="center",
            bbox=dict(boxstyle="round,pad=.35", fc="#fff8e6", ec=F.AMBER))
    ax.set_title("半徑決定路程與面積的尺度")
    fig.tight_layout()
    return _save(fig, "數B3-1-時鐘掃掠.svg")


def fig_discrete_period():
    cycle = ["鼠", "牛", "虎", "兔", "龍"]
    sequence = [cycle[n % len(cycle)] for n in range(16)]
    assert all(sequence[n + 5] == sequence[n] for n in range(11))
    assert sequence[13] == "兔"

    fig, ax = plt.subplots(figsize=(11.2, 4.5))
    xs = np.arange(len(sequence))
    for n, item in enumerate(sequence):
        face = "#eaf2ff" if n < 5 else ("#f0f8f1" if n < 10 else "#fff8e6")
        ax.add_patch(Rectangle((n - .43, -.38), .86, .76, facecolor=face,
                               edgecolor=F.BLUE if n % 5 == 0 else F.GRID, lw=1.4))
        ax.text(n, 0, item, ha="center", va="center", fontsize=11)
    for start in (0, 5, 10):
        ax.annotate("", xy=(start + 4.35, .78), xytext=(start - .35, .78),
                    arrowprops=dict(arrowstyle="<->", color=F.RED, lw=1.8))
        ax.text(start + 2, .98, "5 項", color=F.RED, ha="center", fontsize=10)
    ax.set_xlim(-.8, 15.7)
    ax.set_ylim(-.9, 1.55)
    ax.set_xticks(xs)
    ax.set_xticklabels([str(n) for n in xs])
    ax.set_yticks([])
    ax.set_xlabel("索引 $n$")
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.set_title(r"離散資料的週期：$a_{n+5}=a_n$（這個例子的最小正週期是 5）")
    fig.tight_layout()
    return _save(fig, "數B3-1-離散週期.svg")


def fig_unit_circle():
    theta = 2 * math.pi / 3
    point = np.array([math.cos(theta), math.sin(theta)])
    assert np.allclose(point, [-.5, math.sqrt(3) / 2])

    fig, axes = plt.subplots(1, 2, figsize=(11.5, 5.1))
    ax = axes[0]
    ax.set_aspect("equal")
    ax.set_xlim(-1.35, 1.35)
    ax.set_ylim(-1.25, 1.35)
    _axes_through_origin(ax)
    ax.add_patch(Circle((0, 0), 1, fill=False, edgecolor=F.BLUE, lw=2))
    ax.plot([0, point[0]], [0, point[1]], color=F.PURPLE, lw=2.4)
    ax.plot([point[0], point[0]], [0, point[1]], color=F.RED, ls="--", lw=2)
    ax.scatter([point[0]], [point[1]], color=F.RED, s=65, zorder=5)
    ax.add_patch(Arc((0, 0), .65, .65, theta1=0, theta2=120, color=F.AMBER, lw=2))
    ax.text(.45, .28, r"$\theta$", color=F.AMBER)
    ax.text(point[0] - .08, point[1] + .12,
            r"$P=(\cos\theta,\sin\theta)$", color=F.RED, ha="center")
    ax.text(point[0] - .09, point[1] / 2, r"高度 $\sin\theta$", color=F.RED,
            ha="right", va="center")
    ax.set_xticks([-1, -.5, 0, 1])
    ax.set_yticks([-1, 0, math.sqrt(3) / 2, 1])
    ax.set_yticklabels(["−1", "0", r"$\sqrt{3}/2$", "1"])
    ax.set_title(r"單位圓上的高度就是 $\sin\theta$")

    ax = axes[1]
    x = np.linspace(0, 2 * math.pi, 800)
    y = np.sin(x)
    ax.plot(x, y, color=F.BLUE, lw=2.5)
    ax.scatter([theta], [point[1]], color=F.RED, s=65, zorder=5)
    ax.plot([theta, theta], [0, point[1]], color=F.RED, ls="--")
    ax.plot([0, theta], [point[1], point[1]], color=F.RED, ls="--")
    ax.text(theta + .12, point[1] + .08, r"$(2\pi/3,\sqrt{3}/2)$", color=F.RED)
    ax.set_xlim(0, 2 * math.pi)
    ax.set_ylim(-1.25, 1.25)
    ax.set_xticks([0, math.pi / 2, math.pi, 3 * math.pi / 2, 2 * math.pi])
    ax.set_xticklabels(["0", r"$\pi/2$", r"$\pi$", r"$3\pi/2$", r"$2\pi$"])
    ax.set_yticks([-1, 0, 1])
    F.clean_grid(ax)
    ax.set_title("角度前進時，高度留下正弦圖形")
    fig.tight_layout()
    return _save(fig, "數B3-1-單位圓與正弦.svg")


def fig_sine_graph():
    x = np.linspace(-2 * math.pi, 2 * math.pi, 1601)
    y = np.sin(x)
    assert np.isclose(y.max(), 1, atol=1e-8)
    assert np.isclose(y.min(), -1, atol=1e-8)
    assert np.allclose(np.sin(x + 2 * math.pi), y)
    assert np.allclose(np.sin(-x), -y)

    fig, ax = plt.subplots(figsize=(11.6, 5.1))
    ax.plot(x, y, color=F.BLUE, lw=2.7, label=r"$y=\sin x$")
    zeros = np.arange(-2, 3) * math.pi
    maxima = np.array([-3 * math.pi / 2, math.pi / 2])
    minima = np.array([-math.pi / 2, 3 * math.pi / 2])
    ax.scatter(zeros, np.zeros_like(zeros), color=F.INK, s=35, zorder=4, label="零點")
    ax.scatter(maxima, np.ones_like(maxima), color=F.RED, s=55, zorder=4, label="最高點")
    ax.scatter(minima, -np.ones_like(minima), color=F.GREEN, s=55, zorder=4, label="最低點")
    ax.annotate(r"相隔 $2\pi$", xy=(-3 * math.pi / 2, 1.12),
                xytext=(math.pi / 2, 1.12), ha="center",
                arrowprops=dict(arrowstyle="<->", color=F.RED, lw=1.8), color=F.RED)
    ax.set_xlim(-2 * math.pi - .25, 2 * math.pi + .25)
    ax.set_ylim(-1.38, 1.42)
    ticks = np.arange(-4, 5) * math.pi / 2
    labels = [r"$-2\pi$", r"$-3\pi/2$", r"$-\pi$", r"$-\pi/2$", "0",
              r"$\pi/2$", r"$\pi$", r"$3\pi/2$", r"$2\pi$"]
    ax.set_xticks(ticks)
    ax.set_xticklabels(labels)
    ax.set_yticks([-1, 0, 1])
    F.clean_grid(ax)
    ax.legend(loc="lower left", ncol=4, fontsize=9)
    ax.set_title(r"正弦函數的值域是 $[-1,1]$，最小正週期是 $2\pi$")
    fig.tight_layout()
    return _save(fig, "數B3-1-正弦關鍵點.svg")


def fig_sine_inequality():
    c = .5
    roots = np.array([math.asin(c), math.pi - math.asin(c)])
    assert np.allclose(roots, [math.pi / 6, 5 * math.pi / 6])
    assert np.allclose(np.sin(roots), c)

    x = np.linspace(0, 2 * math.pi, 1200)
    y = np.sin(x)
    mask = y >= c
    fig, ax = plt.subplots(figsize=(10.8, 5.0))
    ax.plot(x, y, color=F.BLUE, lw=2.6, label=r"$y=\sin x$")
    ax.axhline(c, color=F.RED, lw=2, label=r"$y=1/2$")
    ax.fill_between(x, c, y, where=mask, interpolate=True, color=F.GREEN, alpha=.24)
    ax.scatter(roots, [c, c], color=F.RED, s=65, zorder=5)
    ax.annotate(r"$\pi/6$", (roots[0], c), xytext=(roots[0] - .25, .78),
                arrowprops=dict(arrowstyle="->", color=F.RED), color=F.RED)
    ax.annotate(r"$5\pi/6$", (roots[1], c), xytext=(roots[1] + .1, .78),
                arrowprops=dict(arrowstyle="->", color=F.RED), color=F.RED)
    ax.text(math.pi / 2, .65, r"$\sin x\geq 1/2$", ha="center", color=F.GREEN, fontsize=12)
    ax.set_xlim(0, 2 * math.pi)
    ax.set_ylim(-1.25, 1.25)
    ax.set_xticks([0, math.pi / 6, math.pi / 2, 5 * math.pi / 6, math.pi,
                   3 * math.pi / 2, 2 * math.pi])
    ax.set_xticklabels(["0", r"$\pi/6$", r"$\pi/2$", r"$5\pi/6$", r"$\pi$",
                        r"$3\pi/2$", r"$2\pi$"])
    ax.set_yticks([-1, -.5, 0, .5, 1])
    F.clean_grid(ax)
    ax.legend(loc="lower left")
    ax.set_title(r"在 $[0,2\pi]$ 上，以交點切出 $\sin x\geq 1/2$ 的區間")
    fig.tight_layout()
    return _save(fig, "數B3-1-正弦方程與不等式.svg")


def fig_transform():
    h = math.pi / 3
    d = 1.0
    x = np.linspace(-math.pi, 3 * math.pi, 1400)
    parent = np.sin(x)
    transformed = np.sin(x - h) + d
    assert math.isclose(np.sin(math.pi / 2), 1)
    assert math.isclose(np.sin((math.pi / 2 + h) - h) + d, 2)
    assert np.allclose(np.sin((x + 2 * math.pi) - h) + d, transformed)

    fig, ax = plt.subplots(figsize=(11.5, 5.2))
    ax.plot(x, parent, color=F.GRID, lw=2.0, label=r"母圖 $y=\sin x$")
    ax.plot(x, transformed, color=F.BLUE, lw=2.7,
            label=r"$y=\sin(x-\pi/3)+1$")
    ax.axhline(d, color=F.AMBER, ls="--", lw=1.6, label="中線 $y=1$")
    p0 = (math.pi / 2, 1)
    p1 = (math.pi / 2 + h, 2)
    ax.scatter([p0[0], p1[0]], [p0[1], p1[1]], color=[F.INK, F.RED], s=60, zorder=5)
    ax.annotate(r"右移 $\pi/3$、上移 1", xy=p1, xytext=(p0[0] + .2, 2.65),
                arrowprops=dict(arrowstyle="->", color=F.RED), color=F.RED)
    ax.set_xlim(-math.pi, 3 * math.pi)
    ax.set_ylim(-1.5, 3.05)
    ax.set_xticks([-math.pi, 0, math.pi, 2 * math.pi, 3 * math.pi])
    ax.set_xticklabels([r"$-\pi$", "0", r"$\pi$", r"$2\pi$", r"$3\pi$"])
    F.clean_grid(ax)
    ax.legend(loc="lower left", ncol=3, fontsize=9)
    ax.set_title(r"平移改變位置與中線，週期仍為 $2\pi$")
    fig.tight_layout()
    return _save(fig, "數B3-1-正弦平移伸縮.svg")


def fig_parameter_model():
    amplitude, frequency_factor, shift, midline = 3.0, 2.0, math.pi / 6, 2.0
    period = 2 * math.pi / frequency_factor
    x = np.linspace(-.5, 2 * math.pi + .5, 1600)
    y = midline + amplitude * np.sin(frequency_factor * (x - shift))
    assert math.isclose(period, math.pi)
    assert np.isclose(y.max(), 5, atol=2e-5)
    assert np.isclose(y.min(), -1, atol=2e-5)
    assert np.allclose(
        midline + amplitude * np.sin(frequency_factor * ((x + period) - shift)), y
    )

    fig, ax = plt.subplots(figsize=(11.5, 5.2))
    ax.plot(x, y, color=F.BLUE, lw=2.7,
            label=r"$y=2+3\sin(2(x-\pi/6))$")
    ax.axhline(midline, color=F.AMBER, ls="--", lw=1.6, label="中線 $y=2$")
    peak1 = shift + math.pi / (2 * frequency_factor)
    peak2 = peak1 + period
    ax.scatter([peak1, peak2], [5, 5], color=F.RED, s=55, zorder=4)
    ax.annotate(r"週期 $\pi$", xy=(peak1, 5.35), xytext=(peak2, 5.35), ha="center",
                arrowprops=dict(arrowstyle="<->", color=F.RED, lw=1.8), color=F.RED)
    ax.annotate("振幅 3", xy=(shift + .05, 5), xytext=(shift + .05, 2), ha="left",
                arrowprops=dict(arrowstyle="<->", color=F.GREEN, lw=1.8), color=F.GREEN)
    ax.text(5.05, -1.35, "值域 $[-1,5]$", color=F.PURPLE,
            bbox=dict(boxstyle="round,pad=.25", fc="white", ec=F.PURPLE))
    ax.set_xlim(-.25, 2 * math.pi + .25)
    ax.set_ylim(-1.7, 6)
    ax.set_xticks([0, math.pi / 2, math.pi, 3 * math.pi / 2, 2 * math.pi])
    ax.set_xticklabels(["0", r"$\pi/2$", r"$\pi$", r"$3\pi/2$", r"$2\pi$"])
    F.clean_grid(ax)
    ax.legend(loc="lower left")
    ax.set_title(r"$y=d+A\sin(B(x-C))$ 的四個參數各有幾何意義")
    fig.tight_layout()
    return _save(fig, "數B3-1-週期模型參數.svg")


def fig_ferris_wheel():
    radius = 18.0
    center_height = 20.0
    period = 15.0
    t = np.linspace(0, 30, 1201)
    height = center_height + radius * np.sin(
        2 * math.pi * (t - period / 4) / period
    )
    cosine_form = center_height - radius * np.cos(2 * math.pi * t / period)
    assert np.allclose(height, cosine_form)
    assert math.isclose(height[0], 2.0)
    assert np.isclose(height.max(), 38.0)
    assert np.isclose(height.min(), 2.0)
    assert np.allclose(
        center_height - radius * np.cos(2 * math.pi * (t + period) / period), height
    )

    fig, axes = plt.subplots(1, 2, figsize=(11.8, 5.2))
    ax = axes[0]
    ax.set_aspect("equal")
    ax.set_xlim(-21, 21)
    ax.set_ylim(0, 41)
    ax.add_patch(Circle((0, center_height), radius, fill=False, edgecolor=F.BLUE, lw=2.3))
    ax.plot([0, 0], [center_height, 2], color=F.RED, lw=2.2)
    ax.scatter([0, 0], [center_height, 2], color=[F.INK, F.RED], s=55, zorder=4)
    ax.axhline(0, color=F.INK, lw=1.5)
    ax.text(1.2, 11, "半徑 18 m", color=F.RED)
    ax.text(1.2, center_height + .8, "中心高 20 m", color=F.INK)
    ax.text(0, .5, "地面", ha="center")
    ax.set_title("乘客從最低點出發")
    ax.axis("off")

    ax = axes[1]
    ax.plot(t, height, color=F.BLUE, lw=2.6)
    ax.axhline(center_height, color=F.AMBER, ls="--", lw=1.5)
    ax.scatter([0, 7.5, 15], [2, 38, 2], color=F.RED, s=55, zorder=5)
    ax.annotate("一圈 15 分鐘", xy=(0, 40), xytext=(15, 40), ha="center",
                arrowprops=dict(arrowstyle="<->", color=F.RED), color=F.RED)
    ax.set_xlim(0, 30)
    ax.set_ylim(0, 42)
    ax.set_xticks([0, 3.75, 7.5, 11.25, 15, 22.5, 30])
    ax.set_xlabel("時間 $t$（分鐘）")
    ax.set_ylabel("高度 $h$（公尺）")
    F.clean_grid(ax)
    ax.set_title(r"$h(t)=20+18\sin(2\pi(t-15/4)/15)$")
    fig.tight_layout()
    return _save(fig, "數B3-1-摩天輪模型.svg")


def fig_sound_frequency():
    frequencies = (440.0, 880.0)
    periods = tuple(1 / f for f in frequencies)
    assert math.isclose(periods[0], 2 * periods[1])
    assert math.isclose(2 * math.pi * frequencies[0], 880 * math.pi)

    t = np.linspace(0, .006, 1500)
    fig, axes = plt.subplots(2, 1, figsize=(11.3, 5.6), sharex=True)
    colors = (F.BLUE, F.RED)
    for ax, f, color, period in zip(axes, frequencies, colors, periods):
        y = np.sin(2 * math.pi * f * t)
        ax.plot(1000 * t, y, color=color, lw=2)
        ax.axhline(0, color=F.GRID, lw=1)
        ax.annotate(f"週期 {1000 * period:.3f} ms", xy=(0, 1.15),
                    xytext=(1000 * period, 1.15), ha="center",
                    arrowprops=dict(arrowstyle="<->", color=color), color=color)
        ax.set_ylim(-1.35, 1.45)
        ax.set_yticks([-1, 0, 1])
        ax.set_ylabel("振幅")
        ax.grid(True, color=F.GRID, lw=.8)
        ax.set_title(f"{int(f)} Hz：每秒 {int(f)} 次循環", fontsize=12)
    axes[-1].set_xlabel("時間（毫秒）")
    fig.suptitle("頻率加倍時，週期減半；圖形在同一段時間完成兩倍循環", fontsize=15)
    fig.tight_layout()
    return _save(fig, "數B3-1-聲波週期與頻率.svg")


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
