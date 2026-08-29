# -*- coding: utf-8 -*-
"""產生必物-5「能量」學生講義 SVG。

重繪：.venv/bin/python _tools/fig_content_必物-5.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Arc, Circle, FancyBboxPatch, Polygon, Rectangle

import figlib as F


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CH = os.path.join(ROOT, "content", "必修物理", "必物-5")

FIGURE_OUTPUTS = (
    ("fig_work_geometry_and_area", "必物-5-功的方向與力位移面積.svg"),
    ("fig_energy_and_reference", "必物-5-動能位能與零位面.svg"),
    ("fig_power_and_efficiency", "必物-5-功率與效率能流.svg"),
    ("fig_internal_energy_particles", "必物-5-溫度內能與粒子數.svg"),
    ("fig_kelvin_scale", "必物-5-攝氏克氏與平均動能.svg"),
    ("fig_mechanical_conservation", "必物-5-軌道力學能守恆.svg"),
    ("fig_joule_calorimetry", "必物-5-作功加熱與熱量.svg"),
    ("fig_friction_energy_account", "必物-5-摩擦下的能量帳.svg"),
    ("fig_storage_conversion_chain", "必物-5-抽蓄發電能量轉換鏈.svg"),
    ("fig_mass_energy_scale", "必物-5-質量虧損與能量尺度.svg"),
    ("fig_fission_and_powerplant", "必物-5-核分裂連鎖與發電.svg"),
    ("fig_radiation_shielding", "必物-5-游離輻射與屏蔽.svg"),
    ("fig_fusion_reaction", "必物-5-核融合反應與高溫條件.svg"),
)


def _save(fig, name):
    return F.save_to(fig, CH, name, output_subdir="assets", write_pdf=False)


def _box(ax, xy, wh, text, fc="#f8fafc", ec=F.INK, fs=11.2, radius=0.08):
    x, y = xy
    w, h = wh
    patch = FancyBboxPatch(
        (x, y), w, h,
        boxstyle=f"round,pad=0.04,rounding_size={radius}",
        facecolor=fc, edgecolor=ec, lw=1.5,
    )
    ax.add_patch(patch)
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs)
    return patch


def _bar(ax, x, values, colors, labels, width=0.64, base=0.0, scale=0.045):
    bottom = base
    for value, color, label in zip(values, colors, labels):
        height = value * scale
        ax.add_patch(Rectangle((x - width / 2, bottom), width, height,
                               facecolor=color, edgecolor="white", lw=1.2))
        if value > 6:
            ax.text(x, bottom + height / 2, f"{label}\n{value:g} J",
                    ha="center", va="center", fontsize=9.5, color="white", weight="bold")
        bottom += height
    return bottom


def fig_work_geometry_and_area():
    """常力功的幾何意義與變力功的面積。"""
    fig, axes = plt.subplots(1, 2, figsize=(11.5, 4.8))

    ax = axes[0]
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_xlim(-0.8, 6.2)
    ax.set_ylim(-1.05, 3.8)
    ax.plot([-0.55, 5.75], [0, 0], color="#64748b", lw=1.8)
    ax.add_patch(Rectangle((0.15, 0.05), 1.15, 0.72, facecolor="#dbeafe", edgecolor=F.INK, lw=1.6))
    F.arrow(ax, (0.75, 0.98), (2.15, 3.405), color=F.RED, lw=2.8, mutation=17)
    F.arrow(ax, (0.75, -0.28), (5.25, -0.28), color=F.BLUE, lw=2.6, mutation=16)
    F.arrow(ax, (0.75, 0.98), (2.15, 0.98), color=F.GREEN, lw=2.2, ls="--", mutation=14)
    F.angle_arc(ax, (0.75, 0.98), 0.85, 0, 60, color=F.AMBER, text="$60^\\circ$")
    ax.text(1.72, 2.55, "$F=10\\,\\mathrm{N}$", color=F.RED, fontsize=12.5)
    ax.text(2.10, 0.64, "$F_x=F\\cos60^\\circ=5\\,\\mathrm{N}$", color=F.GREEN, fontsize=11.5, ha="center")
    ax.text(3.0, -0.72, "$s=5\\,\\mathrm{m}$", color=F.BLUE, fontsize=12.5, ha="center")
    ax.text(2.55, 3.55, "$W=Fs\\cos\\theta=25\\,\\mathrm{J}$", ha="center", fontsize=13, weight="bold")
    ax.set_title("只有沿位移方向的分量作功", fontsize=14)

    ax = axes[1]
    x = np.array([0.0, 2.0, 4.0])
    force = np.array([4.0, 4.0, 0.0])
    ax.plot(x, force, color=F.RED, lw=2.8, marker="o")
    ax.fill_between([0, 2], [4, 4], color=F.BLUE, alpha=0.22)
    xx = np.linspace(2, 4, 60)
    ax.fill_between(xx, 8 - 2 * xx, color=F.AMBER, alpha=0.27)
    ax.set_xlim(0, 4.35)
    ax.set_ylim(0, 5.0)
    ax.set_xlabel("位置 $x$（m）")
    ax.set_ylabel("沿運動方向的力 $F_x$（N）")
    F.clean_grid(ax)
    ax.text(1, 2.0, "矩形\n$8\\,\\mathrm{J}$", ha="center", va="center", color=F.BLUE, fontsize=11.5)
    ax.text(3, 1.08, "三角形\n$4\\,\\mathrm{J}$", ha="center", va="center", color=F.AMBER, fontsize=11.5)
    ax.text(2.1, 4.55, "$W=$ 曲線下帶號面積 $=12\\,\\mathrm{J}$", ha="center", fontsize=12.5, weight="bold")
    ax.set_title("力隨位置改變時，以 $F_x-x$ 面積求功", fontsize=14)

    theta = np.deg2rad(60)
    force_vector = np.array([2.15, 3.405]) - np.array([0.75, 0.98])
    assert np.isclose(np.rad2deg(np.arctan2(force_vector[1], force_vector[0])), 60.0, atol=0.02)
    assert np.isclose(10 * 5 * np.cos(theta), 25.0)
    assert np.isclose(4 * 2 + 0.5 * 2 * 4, 12.0)
    fig.suptitle("功把力與位移連成同一個能量帳", fontsize=15.5, y=1.0)
    fig.tight_layout()
    _save(fig, "必物-5-功的方向與力位移面積")


def fig_energy_and_reference():
    """動能、重力位能與零位面的選擇。"""
    fig, axes = plt.subplots(1, 2, figsize=(11.4, 4.9))
    ax = axes[0]
    ax.axis("off")
    ax.set_xlim(-0.6, 5.6)
    ax.set_ylim(-0.8, 5.9)
    ax.plot([-0.2, 5.2], [0, 0], color=F.INK, lw=2)
    ax.plot([-0.2, 5.2], [2, 2], color=F.BLUE, lw=1.6, ls="--")
    ax.text(5.25, 0, "零位面 A", va="center", fontsize=10.5)
    ax.text(5.25, 2, "零位面 B", va="center", fontsize=10.5, color=F.BLUE)
    ax.add_patch(Circle((2.0, 5.0), 0.30, facecolor="#fee2e2", edgecolor=F.RED, lw=1.6))
    F.arrow(ax, (2.0, 4.6), (2.0, 0.15), color="#94a3b8", lw=1.5, mutation=11)
    ax.text(1.65, 2.55, "$h_A=5\\,\\mathrm{m}$", rotation=90, ha="center", va="center", fontsize=11.5)
    F.arrow(ax, (2.75, 4.6), (2.75, 2.15), color=F.BLUE, lw=1.5, mutation=11)
    ax.text(3.1, 3.45, "$h_B=3\\,\\mathrm{m}$", rotation=90, ha="center", va="center", fontsize=11.5, color=F.BLUE)
    ax.text(2.0, 5.55, "$m=1\\,\\mathrm{kg}$", ha="center", fontsize=12)
    ax.text(2.45, -0.55, "零位面改變，各位置的 $U$ 同加一常數；$\\Delta U$ 不變", ha="center", fontsize=11.3)
    ax.set_title("重力位能必須連同零位面說明", fontsize=14)

    ax = axes[1]
    ax.axis("off")
    ax.set_xlim(-0.3, 6.4)
    ax.set_ylim(-0.55, 4.2)
    _bar(ax, 1.4, [50, 0], [F.BLUE, F.AMBER], ["$U$", "$K$"])
    _bar(ax, 3.3, [0, 50], [F.BLUE, F.AMBER], ["$U$", "$K$"])
    _bar(ax, 5.2, [30, 20], [F.BLUE, F.AMBER], ["$U$", "$K$"])
    for x, label in [(1.4, "A：高處靜止"), (3.3, "B：最低點"), (5.2, "C：中途")]:
        ax.text(x, -0.30, label, ha="center", fontsize=11)
        ax.plot([x - 0.45, x + 0.45], [2.42, 2.42], color=F.INK, lw=1.2)
    ax.text(3.3, 3.08, "$K+U=50\\,\\mathrm{J}$", ha="center", fontsize=13, weight="bold")
    ax.text(3.3, 3.68, "$K=\\frac{1}{2}mv^2\\geq0$；$U=mgh$ 可隨零位面平移", ha="center", fontsize=12)
    ax.set_title("同一系統的能量可在 $K$ 與 $U$ 間轉移", fontsize=14)
    assert 1 * 10 * 5 == 50
    assert 30 + 20 == 50
    fig.tight_layout()
    _save(fig, "必物-5-動能位能與零位面")


def fig_power_and_efficiency():
    """功率比較與效率的能量分流。"""
    fig, axes = plt.subplots(1, 2, figsize=(11.4, 4.7))
    ax = axes[0]
    ax.axis("off")
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.text(5, 5.45, "兩台機器都提升 $120\\,\\mathrm{kJ}$", ha="center", fontsize=13, weight="bold")
    for y, t, c in [(3.75, 30, F.BLUE), (1.55, 60, F.GREEN)]:
        ax.add_patch(Rectangle((1, y - 0.45), 6, 0.9, facecolor="#e2e8f0", edgecolor=F.INK, lw=1.3))
        ax.add_patch(Rectangle((1, y - 0.45), 6, 0.9, facecolor=c, alpha=0.75, edgecolor=c))
        ax.text(4.0, y, f"耗時 {t} s", ha="center", va="center", fontsize=11.5, color="white", weight="bold")
        ax.text(8.9, y, f"$P={120/t:g}\\,\\mathrm{{kW}}$", ha="center", va="center", fontsize=12, color=c, weight="bold")
    ax.text(5, 0.4, "功率描述能量轉移的快慢：$P=\\Delta E/\\Delta t$", ha="center", fontsize=11.8)
    ax.set_title("相同能量，所需時間較短者功率較大", fontsize=14)

    ax = axes[1]
    ax.axis("off")
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    _box(ax, (0.3, 2.35), (2.2, 1.2), "輸入能量\n$1000\\,\\mathrm{J}$", fc="#ede9fe", ec=F.PURPLE, fs=12)
    _box(ax, (4.0, 3.75), (2.4, 1.2), "有用輸出\n$800\\,\\mathrm{J}$", fc="#dcfce7", ec=F.GREEN, fs=12)
    _box(ax, (4.0, 0.95), (2.4, 1.2), "環境得到\n$200\\,\\mathrm{J}$", fc="#ffedd5", ec=F.AMBER, fs=12)
    F.arrow(ax, (2.55, 2.95), (3.85, 4.35), color=F.GREEN, lw=2.7)
    F.arrow(ax, (2.55, 2.95), (3.85, 1.55), color=F.AMBER, lw=2.7)
    ax.text(7.95, 3.25, "$\\eta=\\dfrac{E_{\\rm useful}}{E_{\\rm in}}=0.80$", ha="center", fontsize=13, weight="bold")
    ax.text(7.95, 2.45, "總能量：$1000=800+200$", ha="center", fontsize=11.5)
    ax.set_title("效率是有用輸出占輸入的比例", fontsize=14)
    assert np.isclose(120e3 / 30, 4000)
    assert np.isclose(800 / 1000, 0.8)
    fig.tight_layout()
    _save(fig, "必物-5-功率與效率能流")


def _particles(ax, center, n, speed, seed, title, color):
    rng = np.random.default_rng(seed)
    cx, cy = center
    w, h = 3.2, 2.35
    ax.add_patch(FancyBboxPatch((cx - w/2, cy - h/2), w, h,
                                boxstyle="round,pad=0.04,rounding_size=0.13",
                                facecolor="#f8fafc", edgecolor=color, lw=1.8))
    points = rng.uniform([cx-w/2+0.28, cy-h/2+0.28], [cx+w/2-0.28, cy+h/2-0.28], (n, 2))
    angles = rng.uniform(0, 2*np.pi, n)
    for p, a in zip(points, angles):
        ax.add_patch(Circle(p, 0.075, facecolor=color, edgecolor=color))
        d = speed * np.array([np.cos(a), np.sin(a)])
        F.arrow(ax, p, p+d, color=color, lw=1.0, mutation=6, alpha=0.7, z=3)
    ax.text(cx, cy+h/2+0.22, title, ha="center", fontsize=11.2, weight="bold")
    return np.full(n, speed)


def fig_internal_energy_particles():
    """溫度對平均動能、粒子數對總內能的影響。"""
    fig, ax = F.canvas(11.7, 5.9)
    ax.axis("off")
    ax.set_aspect("equal")
    ax.set_xlim(-0.2, 12.2)
    ax.set_ylim(-0.3, 6.2)
    v1 = _particles(ax, (2.0, 4.2), 8, 0.18, 1, "同為 8 個粒子：較低溫", F.BLUE)
    v2 = _particles(ax, (6.1, 4.2), 8, 0.42, 2, "同為 8 個粒子：較高溫", F.RED)
    v3 = _particles(ax, (6.1, 1.35), 16, 0.26, 3, "同一溫度：16 個粒子", F.GREEN)
    v4 = _particles(ax, (10.2, 1.35), 8, 0.26, 4, "同一溫度：8 個粒子", F.PURPLE)
    ax.text(10.2, 4.15, "溫度 $T$\n對應每個粒子的\n平均平移動能", ha="center", va="center", fontsize=13, color=F.RED, weight="bold")
    ax.text(2.0, 1.35, "理想氣體內能 $U$\n是全部粒子動能的總和\n因此還與粒子數有關", ha="center", va="center", fontsize=12.5, color=F.GREEN, weight="bold")
    assert v2.mean() > v1.mean()
    assert len(v3) == 2 * len(v4) and np.isclose(v3.mean(), v4.mean())
    ax.set_title("溫度看平均，內能看總和", fontsize=15.5, pad=10)
    _save(fig, "必物-5-溫度內能與粒子數")


def fig_kelvin_scale():
    """攝氏、克氏溫標與理想氣體平均動能。"""
    fig, axes = plt.subplots(1, 2, figsize=(11.3, 4.7))
    ax = axes[0]
    ax.axis("off")
    ax.set_xlim(0, 7)
    ax.set_ylim(-0.4, 6.4)
    for x, title, vals, color in [
        (2.0, "攝氏溫標", [(-273.15, 0), (0, 3), (100, 4.1)], F.BLUE),
        (5.1, "克氏溫標", [(0, 0), (273.15, 3), (373.15, 4.1)], F.RED),
    ]:
        ax.plot([x, x], [0, 5.1], color=color, lw=5, solid_capstyle="round")
        ax.text(x, 5.75, title, ha="center", fontsize=13, weight="bold", color=color)
        for val, y in vals:
            ax.plot([x-0.22, x+0.22], [y, y], color=F.INK, lw=1.6)
            ax.text(x+0.35, y, f"{val:g}°{'C' if x<3 else 'K'}" if x<3 else f"{val:g} K", va="center", fontsize=11)
    for y in (0, 3, 4.1):
        ax.plot([2.25, 4.85], [y, y], color="#94a3b8", lw=1.0, ls="--")
    ax.text(3.55, 1.35, "$T(\\mathrm{K})=t(^\\circ\\mathrm{C})+273.15$", ha="center", fontsize=12.5, weight="bold")
    ax.set_title("同一溫度可用不同零點表示", fontsize=14)

    ax = axes[1]
    t = np.linspace(0, 650, 100)
    ax.plot(t, t, color=F.RED, lw=2.7)
    for x, label in [(273.15, "$T_1$"), (546.3, "$T_2=2T_1$")]:
        ax.scatter([x], [x], s=55, color=F.BLUE, zorder=5)
        ax.plot([x, x], [0, x], color=F.BLUE, lw=1, ls="--")
        ax.plot([0, x], [x, x], color=F.BLUE, lw=1, ls="--")
        ax.text(x+10, x-45, label, fontsize=11.2)
    ax.set_xlim(0, 650)
    ax.set_ylim(0, 650)
    ax.set_xlabel("絕對溫度 $T$（K）")
    ax.set_ylabel("理想氣體平均動能（比例刻度）")
    F.clean_grid(ax)
    ax.text(315, 555, "$\\overline{K}\\propto T$", fontsize=14, color=F.RED, weight="bold")
    ax.set_title("比例比較必須使用克氏溫標", fontsize=14)
    assert np.isclose(0 + 273.15, 273.15)
    assert np.isclose(546.3/273.15, 2.0)
    fig.tight_layout()
    _save(fig, "必物-5-攝氏克氏與平均動能")


def fig_mechanical_conservation():
    """光滑軌道三個狀態的幾何與能量帳。"""
    fig, axes = plt.subplots(1, 2, figsize=(12.0, 5.0))
    ax = axes[0]
    ax.axis("off")
    ax.set_aspect("equal")
    ax.set_xlim(-5.4, 5.3)
    ax.set_ylim(-0.9, 6.2)
    x1 = np.linspace(-4.8, 0, 150)
    y1 = 5*(x1/4.8)**2
    x2 = np.linspace(0, 4.4, 150)
    y2 = 3*(x2/4.4)**2
    ax.plot(np.r_[x1, x2], np.r_[y1, y2], color=F.INK, lw=4)
    states = [(-4.8, 5, "A", F.RED), (0, 0, "B", F.BLUE), (4.4, 3, "C", F.GREEN)]
    for x, y, label, color in states:
        ax.add_patch(Circle((x, y+0.28), 0.28, facecolor=color, edgecolor="white", lw=1.2, zorder=5))
        ax.text(x, y+0.85, label, ha="center", fontsize=13, weight="bold", color=color)
        ax.plot([x, x], [0, y], color=color, lw=1.2, ls="--")
    ax.plot([-5.1, 5.0], [0, 0], color="#64748b", lw=1.2, ls="--")
    ax.text(-2.9, 2.45, "$h_A=5\\,\\mathrm{m}$", rotation=90, ha="center", fontsize=11)
    ax.text(3.3, 1.45, "$h_C=3\\,\\mathrm{m}$", rotation=90, ha="center", fontsize=11)
    ax.text(0, -0.55, "零位面", ha="center", fontsize=10.5)
    ax.text(0, 5.85, "軌道光滑，支持力始終垂直瞬時位移", ha="center", fontsize=12)
    ax.set_title("先由圖確定高度與系統", fontsize=14)

    ax = axes[1]
    ax.axis("off")
    ax.set_xlim(0, 7)
    ax.set_ylim(-0.6, 4.6)
    vals = [(50, 0, "A\n$v=0$"), (0, 50, "B\n$v=10\\,\\mathrm{m/s}$"), (30, 20, "C\n$v=\\sqrt{40}\\,\\mathrm{m/s}$")]
    for i, (u, k, label) in enumerate(vals):
        x = 1.2 + 2.2*i
        _bar(ax, x, [u, k], [F.BLUE, F.AMBER], ["$U$", "$K$"])
        ax.text(x, -0.35, label, ha="center", fontsize=10.8)
    ax.text(3.4, 3.02, "$E=K+U=50\\,\\mathrm{J}$", ha="center", fontsize=13, weight="bold")
    ax.text(3.4, 3.65, "$\\frac{1}{2}mv_A^2+mgh_A=\\frac{1}{2}mv^2+mgh$", ha="center", fontsize=12.5)
    ax.set_title("只有重力作功時，$K+U$ 保持不變", fontsize=14)
    g = 10.0
    assert np.isclose(np.sqrt(2*g*5), 10.0)
    assert np.isclose(0.5*np.sqrt(40)**2 + g*3, 50.0)
    fig.tight_layout()
    _save(fig, "必物-5-軌道力學能守恆")


def fig_joule_calorimetry():
    """焦耳攪水實驗與量熱計算的能量路徑。"""
    fig, axes = plt.subplots(1, 2, figsize=(11.8, 5.0))
    ax = axes[0]
    ax.axis("off")
    ax.set_aspect("equal")
    ax.set_xlim(-4.8, 4.8)
    ax.set_ylim(-2.5, 3.2)
    ax.add_patch(Rectangle((-1.5, -1.5), 3.0, 2.5, facecolor="#dbeafe", edgecolor=F.BLUE, lw=2))
    ax.text(0, -0.2, "水", fontsize=16, ha="center", color=F.BLUE, weight="bold")
    ax.plot([0, 0], [0.9, 2.2], color=F.INK, lw=2.3)
    for y in (-0.85, -0.25, 0.35):
        ax.plot([-0.9, 0.9], [y, y], color=F.AMBER, lw=3)
    ax.add_patch(Circle((0, 2.25), 0.42, fill=False, edgecolor=F.INK, lw=2))
    ax.plot([-3.2, 3.2], [2.25, 2.25], color=F.INK, lw=1.6)
    for x in (-3.2, 3.2):
        ax.plot([x, x], [2.25, -0.25], color=F.INK, lw=1.6)
        ax.add_patch(Rectangle((x-0.35, -0.85), 0.7, 0.6, facecolor="#e2e8f0", edgecolor=F.INK, lw=1.4))
        F.arrow(ax, (x, 0.95), (x, 0.05), color=F.RED, lw=2.4)
    F.arrow(ax, (0.65, 1.55), (1.35, 1.05), color=F.GREEN, lw=2.2)
    ax.text(1.45, 1.55, "葉片轉動", fontsize=11.3, color=F.GREEN)
    ax.text(0, -2.05, "重物重力位能下降 $\\rightarrow$ 葉片對水作功 $\\rightarrow$ 水內能增加", ha="center", fontsize=11.5)
    ax.set_title("焦耳實驗：作功與加熱都能改變內能", fontsize=14)

    ax = axes[1]
    ax.axis("off")
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    _box(ax, (0.25, 2.35), (2.3, 1.3), "電能輸入\n$8400\\,\\mathrm{J}$", fc="#ede9fe", ec=F.PURPLE, fs=12)
    _box(ax, (3.8, 3.75), (2.5, 1.3), "水吸收熱量\n$Q=7560\\,\\mathrm{J}$", fc="#dbeafe", ec=F.BLUE, fs=11.7)
    _box(ax, (3.8, 0.95), (2.5, 1.3), "傳給容器與環境\n$840\\,\\mathrm{J}$", fc="#ffedd5", ec=F.AMBER, fs=11.5)
    F.arrow(ax, (2.65, 3.0), (3.65, 4.4), color=F.BLUE, lw=2.5)
    F.arrow(ax, (2.65, 3.0), (3.65, 1.6), color=F.AMBER, lw=2.5)
    ax.text(8.15, 4.15, "$Q=mc\\Delta T$", ha="center", fontsize=15, weight="bold")
    ax.text(8.15, 3.35, "$m=0.100\\,\\mathrm{kg}$", ha="center", fontsize=11.5)
    ax.text(8.15, 2.75, "$c=4200\\,\\mathrm{J/(kg\\cdot{}^\\circ C)}$", ha="center", fontsize=11.5)
    ax.text(8.15, 1.75, "$\\Delta T=18.0^\\circ\\mathrm{C}$", ha="center", fontsize=13, color=F.BLUE, weight="bold")
    ax.set_title("量熱式是水這個系統的能量帳", fontsize=14)
    q = 0.9*8400
    assert np.isclose(q, 7560)
    assert np.isclose(q/(0.1*4200), 18.0)
    fig.tight_layout()
    _save(fig, "必物-5-作功加熱與熱量")


def fig_friction_energy_account():
    """摩擦存在時的機械能與總能量帳。"""
    fig, axes = plt.subplots(1, 2, figsize=(11.7, 4.8))
    ax = axes[0]
    ax.axis("off")
    ax.set_aspect("equal")
    ax.set_xlim(-0.5, 8)
    ax.set_ylim(-0.8, 5.3)
    slope = Polygon([(0.4, 4.2), (6.8, 0), (0.4, 0)], closed=True,
                    facecolor="#f1f5f9", edgecolor=F.INK, lw=2)
    ax.add_patch(slope)
    ax.add_patch(Rectangle((1.0, 3.35), 0.9, 0.62, angle=-33,
                           facecolor="#fee2e2", edgecolor=F.RED, lw=1.5))
    F.arrow(ax, (2.0, 3.05), (4.55, 1.38), color=F.BLUE, lw=2.8)
    F.arrow(ax, (3.75, 1.68), (2.65, 2.40), color=F.AMBER, lw=2.6)
    ax.text(3.04, 2.76, "$f_k$", color=F.AMBER, fontsize=13)
    ax.text(4.45, 2.15, "$\\vec v$", color=F.BLUE, fontsize=13)
    for x, y in [(3.5, 1.58), (4.2, 1.10), (4.9, 0.72)]:
        ax.text(x, y, "≈", color=F.RED, rotation=-33, fontsize=14, ha="center")
    ax.text(3.6, -0.48, "接觸面微觀形變與振動增加，系統的熱能增加", ha="center", fontsize=11.5)
    ax.set_title("先在圖上標出摩擦與能量去向", fontsize=14)

    ax = axes[1]
    ax.axis("off")
    ax.set_xlim(0, 7)
    ax.set_ylim(-0.5, 4.7)
    _bar(ax, 1.35, [40], [F.BLUE], ["$U_g$"])
    _bar(ax, 3.5, [10, 10, 20], [F.BLUE, F.GREEN, F.AMBER], ["$U_g$", "$K$", "$E_{th}$"])
    ax.text(1.35, -0.22, "初態", ha="center", fontsize=11.5)
    ax.text(3.5, -0.22, "末態", ha="center", fontsize=11.5)
    F.arrow(ax, (2.0, 2.25), (2.8, 2.25), color=F.INK, lw=2.0)
    ax.text(5.65, 3.40, "機械能：$40\\rightarrow20\\,\\mathrm{J}$", ha="center", fontsize=11.5)
    ax.text(5.65, 2.65, "熱能：$0\\rightarrow20\\,\\mathrm{J}$", ha="center", fontsize=11.5, color=F.AMBER)
    ax.text(5.65, 1.75, "總能量仍為 $40\\,\\mathrm{J}$", ha="center", fontsize=12.5, weight="bold")
    ax.set_title("機械能減少量成為熱能", fontsize=14)
    assert 40 == 10+10+20
    fig.tight_layout()
    _save(fig, "必物-5-摩擦下的能量帳")


def fig_storage_conversion_chain():
    """抽蓄發電的雙向轉換與逐段效率。"""
    fig, ax = F.canvas(12.0, 5.0)
    ax.axis("off")
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 6)
    nodes = [
        (0.25, "離峰電能\n100 MJ", "#ede9fe", F.PURPLE),
        (2.7, "馬達與抽水\n85 MJ", "#dbeafe", F.BLUE),
        (5.15, "上水庫位能\n76.5 MJ", "#dcfce7", F.GREEN),
        (7.6, "水輪機\n68.9 MJ", "#fef3c7", F.AMBER),
        (10.05, "尖峰電能\n65.4 MJ", "#fee2e2", F.RED),
    ]
    for x, text, fc, ec in nodes:
        _box(ax, (x, 2.35), (1.7, 1.2), text, fc=fc, ec=ec, fs=11)
    efficiencies = [0.85, 0.90, 0.90, 0.95]
    for i, eta in enumerate(efficiencies):
        x0 = nodes[i][0] + 1.75
        x1 = nodes[i+1][0] - 0.08
        F.arrow(ax, (x0, 2.95), (x1, 2.95), color=F.INK, lw=1.8, mutation=12)
        ax.text((x0+x1)/2, 3.35, f"η = {100*eta:.0f}%", ha="center", fontsize=10.5)
    ax.text(6, 4.7, "充電：電能提升水的重力位能；放電：水的位能帶動發電機", ha="center", fontsize=13, weight="bold")
    ax.text(6, 1.35, "每一段都有能量流向環境；往返效率 $=0.85\\times0.90\\times0.90\\times0.95\\approx65\\%$", ha="center", fontsize=12)
    ax.text(6, 0.65, "儲能改變能量可用的時間，不會創造能量", ha="center", fontsize=11.5, color="#475569")
    recovered = 100*np.prod(efficiencies)
    assert np.isclose(recovered, 65.4075)
    ax.set_title("用能量鏈追蹤每一次轉換", fontsize=15, pad=10)
    _save(fig, "必物-5-抽蓄發電能量轉換鏈")


def fig_mass_energy_scale():
    """質量虧損經 c² 對應到能量。"""
    fig, axes = plt.subplots(1, 2, figsize=(11.5, 4.8))
    ax = axes[0]
    ax.axis("off")
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    _box(ax, (0.4, 2.35), (2.3, 1.25), "反應前後\n質量差 $\\Delta m$", fc="#dbeafe", ec=F.BLUE, fs=12)
    _box(ax, (4.0, 2.35), (2.0, 1.25), "$c^2$\n$9.0\\times10^{16}$", fc="#fef3c7", ec=F.AMBER, fs=12)
    _box(ax, (7.35, 2.35), (2.2, 1.25), "釋放能量\n$E=\\Delta mc^2$", fc="#fee2e2", ec=F.RED, fs=12)
    F.arrow(ax, (2.8, 2.98), (3.85, 2.98), color=F.INK, lw=2.3)
    F.arrow(ax, (6.1, 2.98), (7.2, 2.98), color=F.INK, lw=2.3)
    ax.text(5, 4.7, "核反應前後的總質量差很小，$c^2$ 的尺度很大", ha="center", fontsize=13, weight="bold")
    ax.set_title("質能關係是反應系統的能量帳", fontsize=14)

    ax = axes[1]
    dm = np.array([1e-12, 1e-9, 1e-6])
    energy = dm*(3e8)**2
    labels = ["$1\\,\\mathrm{ng}$?\n$10^{-12}\\,\\mathrm{kg}$", "$1\\,\\mathrm{\\mu g}$\n$10^{-9}\\,\\mathrm{kg}$", "$1\\,\\mathrm{mg}$\n$10^{-6}\\,\\mathrm{kg}$"]
    # 第一標籤只陳述 kg，避免不同語系對 ng 的輸入誤讀。
    labels[0] = "$10^{-12}\\,\\mathrm{kg}$"
    bars = ax.bar(np.arange(3), energy, color=[F.BLUE, F.GREEN, F.RED], width=0.62)
    ax.set_yscale("log")
    ax.set_ylim(1e4, 2e11)
    ax.set_xticks(np.arange(3), labels)
    ax.set_ylabel("對應能量（J，對數刻度）")
    F.clean_grid(ax)
    for b, e in zip(bars, energy):
        ax.text(b.get_x()+b.get_width()/2, e*1.35, f"${e:.0e}\\,\\mathrm{{J}}$", ha="center", fontsize=10.8)
    ax.set_title("小質量差也可對應可觀能量", fontsize=14)
    assert np.allclose(energy, [9e4, 9e7, 9e10])
    fig.tight_layout()
    _save(fig, "必物-5-質量虧損與能量尺度")


def fig_fission_and_powerplant():
    """核分裂的粒子帳與核能發電能量鏈。"""
    fig, axes = plt.subplots(1, 2, figsize=(12.0, 5.0))
    ax = axes[0]
    ax.axis("off")
    ax.set_aspect("equal")
    ax.set_xlim(-4.8, 5.0)
    ax.set_ylim(-3.0, 3.4)
    ax.add_patch(Circle((-2.2, 0), 0.95, facecolor="#ede9fe", edgecolor=F.PURPLE, lw=2))
    ax.text(-2.2, 0, "$^{235}_{92}\\mathrm{U}$", ha="center", va="center", fontsize=15, weight="bold")
    ax.add_patch(Circle((-4.15, 0), 0.18, facecolor=F.BLUE, edgecolor=F.BLUE))
    F.arrow(ax, (-3.9, 0), (-3.25, 0), color=F.BLUE, lw=2.5)
    ax.text(-4.15, 0.42, "$n$", ha="center", fontsize=12)
    ax.add_patch(Circle((0.55, 0.85), 0.72, facecolor="#fee2e2", edgecolor=F.RED, lw=1.7))
    ax.add_patch(Circle((0.55, -0.95), 0.62, facecolor="#dcfce7", edgecolor=F.GREEN, lw=1.7))
    ax.text(0.55, 0.85, "$^{141}_{56}\\mathrm{Ba}$", ha="center", va="center", fontsize=12)
    ax.text(0.55, -0.95, "$^{92}_{36}\\mathrm{Kr}$", ha="center", va="center", fontsize=12)
    F.arrow(ax, (-1.1, 0.25), (-0.2, 0.75), color=F.RED, lw=2.0)
    F.arrow(ax, (-1.1, -0.25), (-0.2, -0.75), color=F.GREEN, lw=2.0)
    for y in (-1.7, 0, 1.7):
        ax.add_patch(Circle((2.45, y), 0.16, facecolor=F.BLUE, edgecolor=F.BLUE))
        F.arrow(ax, (1.35, y*0.55), (2.2, y), color=F.BLUE, lw=1.8)
    ax.text(3.2, 0, "$3n$ 可再引發分裂", rotation=90, ha="center", va="center", fontsize=11.5, color=F.BLUE)
    ax.text(0, -2.45, "質量數：$1+235=141+92+3$；原子序：$92=56+36$", ha="center", fontsize=11.3)
    ax.set_title("核反應式先核對質量數與原子序", fontsize=14)

    ax = axes[1]
    ax.axis("off")
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    chain = [
        (0.15, "核分裂\n核能", "#ede9fe", F.PURPLE),
        (2.55, "反應爐與冷卻劑\n內能", "#fee2e2", F.RED),
        (5.05, "蒸汽與渦輪\n動能", "#dbeafe", F.BLUE),
        (7.55, "發電機\n電能", "#dcfce7", F.GREEN),
    ]
    for x, text, fc, ec in chain:
        _box(ax, (x, 2.4), (2.0, 1.25), text, fc=fc, ec=ec, fs=11.3)
    for i in range(3):
        F.arrow(ax, (chain[i][0]+2.05, 3.02), (chain[i+1][0]-0.08, 3.02), color=F.INK, lw=2.0)
    ax.text(5, 4.75, "控制棒調節可持續連鎖反應；冷卻系統把能量帶出反應爐", ha="center", fontsize=11.8, weight="bold")
    ax.text(5, 1.15, "能量來源在核反應；渦輪與發電機負責把能量轉成可輸送的電能", ha="center", fontsize=11.5)
    ax.set_title("核電廠仍以蒸汽推動渦輪", fontsize=14)
    assert 1+235 == 141+92+3
    assert 92 == 56+36
    fig.tight_layout()
    _save(fig, "必物-5-核分裂連鎖與發電")


def fig_radiation_shielding():
    """α、β、γ 的穿透與安全控制。"""
    fig, axes = plt.subplots(1, 2, figsize=(11.8, 4.8))
    ax = axes[0]
    ax.axis("off")
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 6)
    ax.add_patch(Rectangle((3.25, 0.65), 0.28, 4.4, facecolor="#f8fafc", edgecolor=F.INK, lw=1.5))
    ax.add_patch(Rectangle((6.05, 0.65), 0.55, 4.4, facecolor="#cbd5e1", edgecolor=F.INK, lw=1.5))
    ax.add_patch(Rectangle((9.0, 0.65), 1.0, 4.4, facecolor="#64748b", edgecolor=F.INK, lw=1.5))
    ax.text(3.39, 5.4, "紙", ha="center", fontsize=11)
    ax.text(6.32, 5.4, "鋁", ha="center", fontsize=11)
    ax.text(9.5, 5.4, "厚鉛／混凝土", ha="center", fontsize=11)
    rays = [(4.4, 3.35, F.RED, "$\\alpha$"), (3.0, 6.32, F.BLUE, "$\\beta$"), (1.6, 9.7, F.PURPLE, "$\\gamma$")]
    for y, end, color, label in rays:
        F.arrow(ax, (0.7, y), (end, y), color=color, lw=3.1, mutation=14)
        ax.text(0.25, y, label, va="center", fontsize=14, color=color, weight="bold")
    ax.text(5.5, 0.12, "穿透距離比較須在相同介質與能量條件下解讀", ha="center", fontsize=10.8, color="#475569")
    ax.set_title("屏蔽材料依輻射種類選擇", fontsize=14)

    ax = axes[1]
    ax.axis("off")
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    _box(ax, (0.4, 3.55), (2.4, 1.25), "縮短時間\n減少累積劑量", fc="#fee2e2", ec=F.RED, fs=12)
    _box(ax, (3.8, 3.55), (2.4, 1.25), "增加距離\n降低照射強度", fc="#dbeafe", ec=F.BLUE, fs=12)
    _box(ax, (7.2, 3.55), (2.4, 1.25), "適當屏蔽\n吸收或散射輻射", fc="#dcfce7", ec=F.GREEN, fs=12)
    ax.text(5, 2.55, "外照射控制", ha="center", fontsize=13, weight="bold")
    ax.text(5, 1.45, "$\\alpha$ 外部穿透弱，若放射性物質進入體內，短程內可造成密集游離", ha="center", fontsize=11.5)
    ax.text(5, 0.65, "有效劑量以西弗（Sv）表示，評估時還須考慮器官與輻射種類", ha="center", fontsize=11.2)
    ax.set_title("安全策略同時考慮暴露途徑", fontsize=14)
    fig.tight_layout()
    _save(fig, "必物-5-游離輻射與屏蔽")


def fig_fusion_reaction():
    """氘氚融合的核子帳與高溫條件。"""
    fig, axes = plt.subplots(1, 2, figsize=(11.8, 4.8))
    ax = axes[0]
    ax.axis("off")
    ax.set_aspect("equal")
    ax.set_xlim(-5, 5)
    ax.set_ylim(-2.8, 3.1)
    for x, label, color in [(-3.6, "$^{2}_{1}\\mathrm{H}$", F.BLUE), (-1.5, "$^{3}_{1}\\mathrm{H}$", F.GREEN)]:
        ax.add_patch(Circle((x, 0), 0.68, facecolor="white", edgecolor=color, lw=2.3))
        ax.text(x, 0, label, ha="center", va="center", fontsize=14, color=color, weight="bold")
        F.arrow(ax, (x-0.75 if x>-2 else x+0.75, 0), (x-0.2 if x>-2 else x+0.2, 0), color=color, lw=2)
    F.arrow(ax, (-0.5, 0), (0.45, 0), color=F.INK, lw=2.3)
    ax.add_patch(Circle((1.5, 0.55), 0.82, facecolor="#fee2e2", edgecolor=F.RED, lw=2))
    ax.text(1.5, 0.55, "$^{4}_{2}\\mathrm{He}$", ha="center", va="center", fontsize=14, color=F.RED, weight="bold")
    ax.add_patch(Circle((3.55, -0.55), 0.22, facecolor=F.PURPLE, edgecolor=F.PURPLE))
    F.arrow(ax, (2.28, 0.15), (3.25, -0.42), color=F.PURPLE, lw=2.2)
    ax.text(3.55, -1.05, "$n$", ha="center", fontsize=13, color=F.PURPLE)
    ax.text(0, -2.0, "質量數：$2+3=4+1$；原子序：$1+1=2+0$", ha="center", fontsize=11.5)
    ax.set_title("氘氚反應同時守恆核子帳", fontsize=14)

    ax = axes[1]
    r = np.linspace(0.6, 5, 300)
    barrier = 1/r
    ax.plot(r, barrier, color=F.RED, lw=2.6)
    ax.fill_between(r, 0, barrier, color=F.RED, alpha=0.13)
    ax.axhline(0.52, color=F.BLUE, lw=2, ls="--")
    ax.axhline(1.15, color=F.GREEN, lw=2, ls="--")
    ax.text(3.15, 0.55, "較低溫：可接近的粒子比例小", fontsize=10.8, color=F.BLUE)
    ax.text(2.25, 1.20, "約 $10^8\\,\\mathrm{K}$：更多粒子能接近", fontsize=10.8, color=F.GREEN)
    ax.text(0.88, 1.48, "同號核間\n電斥力障壁", ha="center", fontsize=11.3, color=F.RED, weight="bold")
    ax.set_xlim(0.6, 5)
    ax.set_ylim(0, 1.8)
    ax.set_xlabel("兩核距離（示意刻度）")
    ax.set_ylabel("電位能障壁（示意刻度）")
    F.clean_grid(ax)
    ax.set_title("高溫提高克服電斥力的粒子比例", fontsize=14)
    assert 2+3 == 4+1
    assert 1+1 == 2+0
    fig.tight_layout()
    _save(fig, "必物-5-核融合反應與高溫條件")


def main():
    for function_name, _filename in FIGURE_OUTPUTS:
        globals()[function_name]()


if __name__ == "__main__":
    main()
