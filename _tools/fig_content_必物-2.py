# -*- coding: utf-8 -*-
"""產生必物-2「物質的組成與交互作用」學生講義 SVG。

重繪：.venv/bin/python _tools/fig_content_必物-2.py
"""

import os
import sys
from fractions import Fraction

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, FancyBboxPatch, PathPatch, Polygon, Rectangle
from matplotlib.path import Path

import figlib as F


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CH = os.path.join(ROOT, "content", "必修物理", "必物-2")

FIGURE_OUTPUTS = (
    ("fig_atomic_evidence", "必物-2-原子存在的證據鏈.svg"),
    ("fig_states_particles", "必物-2-物質三態的粒子模型.svg"),
    ("fig_scale_ladder", "必物-2-物質結構尺度階梯.svg"),
    ("fig_rutherford_scattering", "必物-2-拉塞福散射與原子核.svg"),
    ("fig_nuclide_quarks", "必物-2-核素記號與夸克組成.svg"),
    ("fig_gravity_inverse_square", "必物-2-萬有引力與平方反比.svg"),
    ("fig_electric_field", "必物-2-庫侖力與電場線.svg"),
    ("fig_magnetic_field", "必物-2-磁場線與磁化.svg"),
    ("fig_strong_weak", "必物-2-強作用與弱作用.svg"),
    ("fig_four_interactions", "必物-2-四種基本交互作用尺度圖.svg"),
    ("fig_alpha_closest_force", "必物-2-alpha粒子最近點受力.svg"),
    ("fig_surface_particle_forces", "必物-2-星球表面帶電微粒受力.svg"),
)


def _save(fig, name):
    return F.save_to(fig, CH, name, output_subdir="assets", write_pdf=False)


def _rounded(ax, xy, wh, text, fc="#f8fafc", ec=F.INK, fs=11.0, lw=1.5):
    x, y = xy
    w, h = wh
    box = FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.04,rounding_size=0.10",
        facecolor=fc, edgecolor=ec, lw=lw,
    )
    ax.add_patch(box)
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs)
    return box


def _curve_arrow(ax, points, color, lw=1.8, mutation=10):
    verts = [points[0], points[1], points[2], points[3]]
    path = Path(verts, [Path.MOVETO, Path.CURVE4, Path.CURVE4, Path.CURVE4])
    patch = PathPatch(path, fill=False, edgecolor=color, lw=lw)
    ax.add_patch(patch)
    F.arrow(ax, points[2], points[3], color=color, lw=lw, mutation=mutation)


def fig_atomic_evidence():
    """布朗運動：可見微粒的折線軌跡由大量不可見分子的不平衡碰撞造成。"""
    fig, ax = F.canvas(12.0, 6.4)
    ax.axis("off")
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 7.2)

    ax.add_patch(Rectangle((0.35, 1.1), 4.0, 4.7, facecolor="#eff6ff", edgecolor=F.BLUE, lw=1.8))
    pollen = np.array([2.35, 3.45])
    ax.add_patch(Circle(pollen, 0.42, facecolor="#facc15", edgecolor="#a16207", lw=1.8, zorder=5))
    molecule_angles = np.deg2rad([10, 52, 94, 145, 205, 250, 302, 338])
    radii = np.array([1.35, 1.65, 1.25, 1.55, 1.45, 1.72, 1.40, 1.62])
    molecules = pollen + np.c_[np.cos(molecule_angles), np.sin(molecule_angles)] * radii[:, None]
    for i, p in enumerate(molecules):
        ax.add_patch(Circle(p, 0.105, facecolor="#93c5fd", edgecolor=F.BLUE, lw=1.0))
        end = pollen + (pollen - p) * (0.50 if i % 2 == 0 else 0.36)
        F.arrow(ax, p, end, color=F.BLUE if i % 2 == 0 else "#64748b", lw=1.25, mutation=7)
    resultant = np.array([0.58, 0.24])
    F.arrow(ax, pollen, pollen + resultant, color=F.RED, lw=2.4, mutation=12)
    ax.text(2.45, 5.35, "水分子的熱運動\n從各方向撞擊", ha="center", fontsize=12.2, weight="bold")
    ax.text(2.35, 1.42, "瞬間合力通常不完全抵消", ha="center", fontsize=11.2, color=F.RED)

    steps = np.array([
        [0.00, 0.00], [0.38, 0.17], [0.20, 0.53], [0.61, 0.78],
        [0.46, 1.12], [0.92, 1.24], [1.18, 1.02], [1.42, 1.39],
        [1.24, 1.72], [1.68, 1.92], [1.97, 1.66], [2.26, 1.98],
        [2.08, 2.35], [2.51, 2.57], [2.82, 2.36], [3.11, 2.73],
    ])
    x0, y0 = 5.05, 1.35
    path = steps * np.array([1.05, 1.20]) + np.array([x0, y0])
    ax.plot(path[:, 0], path[:, 1], color=F.PURPLE, lw=2.1)
    ax.scatter(path[:, 0], path[:, 1], s=28, color=F.PURPLE, zorder=4)
    ax.scatter([path[0, 0]], [path[0, 1]], s=85, color=F.GREEN, zorder=5)
    ax.scatter([path[-1, 0]], [path[-1, 1]], s=85, color=F.RED, zorder=5)
    ax.text(7.05, 5.65, "顯微鏡下每隔固定時間記錄位置", ha="center", fontsize=12.2, weight="bold")
    ax.text(path[0, 0] - 0.15, path[0, 1] - 0.35, "起點", ha="right", fontsize=10.2, color=F.GREEN)
    ax.text(path[-1, 0] + 0.15, path[-1, 1] + 0.12, "終點", ha="left", fontsize=10.2, color=F.RED)

    _rounded(ax, (9.2, 4.65), (2.45, 1.0), "觀察\n不規則位移", fc="#fef3c7", ec=F.AMBER, fs=11.3)
    _rounded(ax, (9.2, 2.75), (2.45, 1.0), "模型\n分子碰撞", fc="#dbeafe", ec=F.BLUE, fs=11.3)
    _rounded(ax, (9.2, 0.85), (2.45, 1.0), "定量預測與實驗吻合\n支持原子分子存在", fc="#dcfce7", ec=F.GREEN, fs=10.7)
    F.arrow(ax, (10.43, 4.6), (10.43, 3.82), color=F.INK, mutation=9)
    F.arrow(ax, (10.43, 2.70), (10.43, 1.92), color=F.INK, mutation=9)
    ax.text(6.0, 6.85, "布朗運動把不可見的分子熱運動連到可量測的微粒軌跡", ha="center",
            fontsize=14.8, weight="bold")
    assert np.linalg.norm(resultant) > 0
    assert path.shape == (16, 2) and np.all(np.diff(np.arange(len(path))) == 1)
    _save(fig, "必物-2-原子存在的證據鏈")


def fig_states_particles():
    """三態的形狀與體積由粒子距離、運動自由度及束縛共同決定。"""
    fig, ax = F.canvas(12.0, 6.7)
    ax.axis("off")
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 7.35)

    boxes = [(0.35, F.BLUE, "固體"), (4.25, F.GREEN, "液體"), (8.15, F.RED, "氣體")]
    solid = np.array([(x, y) for y in (1.8, 2.45, 3.10, 3.75) for x in (0.95, 1.60, 2.25, 2.90)])
    liquid = np.array([
        (4.80, 1.72), (5.40, 1.88), (6.05, 1.68), (6.68, 1.92),
        (4.95, 2.38), (5.62, 2.53), (6.28, 2.30), (6.78, 2.58),
        (4.75, 3.04), (5.38, 3.18), (6.03, 3.02), (6.62, 3.23),
    ])
    gas = np.array([
        (8.65, 1.55), (10.85, 1.82), (9.72, 2.25), (8.95, 3.18),
        (10.55, 3.62), (9.55, 4.18), (11.05, 4.65), (8.55, 4.78),
    ])
    sets = [solid, liquid, gas]
    for (x, color, name), pts in zip(boxes, sets):
        ax.add_patch(Rectangle((x, 1.15), 3.5, 4.25, facecolor="#f8fafc", edgecolor=color, lw=1.9))
        for px, py in pts:
            ax.add_patch(Circle((px, py), 0.12, facecolor=color, edgecolor="white", lw=0.8))
        ax.text(x + 1.75, 5.75, name, ha="center", fontsize=15, weight="bold", color=color)

    ax.text(2.10, 0.43, "固定形狀、固定體積\n粒子在平衡位置附近振動", ha="center", fontsize=10.2)
    ax.text(6.00, 0.43, "形狀隨容器、體積近似固定\n粒子可交換鄰近位置", ha="center", fontsize=10.2)
    ax.text(9.90, 0.43, "形狀與體積皆隨容器\n粒子遠離並充分移動", ha="center", fontsize=10.2)
    F.arrow(ax, (3.50, 6.25), (4.42, 6.25), color=F.RED, lw=2.0, mutation=11)
    F.arrow(ax, (7.40, 6.25), (8.32, 6.25), color=F.RED, lw=2.0, mutation=11)
    ax.text(6.0, 6.62, "在指定壓力下加熱：平均動能增加，束縛較難維持", ha="center",
            fontsize=13.5, weight="bold")
    solid_nn = 0.65
    liquid_nn = min(np.linalg.norm(liquid[i] - liquid[j]) for i in range(len(liquid))
                    for j in range(i + 1, len(liquid)))
    gas_nn = min(np.linalg.norm(gas[i] - gas[j]) for i in range(len(gas))
                 for j in range(i + 1, len(gas)))
    assert 0.45 < liquid_nn < 0.75
    assert gas_nn > solid_nn
    assert len(solid) > len(gas)
    _save(fig, "必物-2-物質三態的粒子模型")


def fig_scale_ladder():
    """用同一對數軸呈現分子、原子、原子核、核子與基本粒子的尺度。"""
    fig, ax = F.canvas(12.0, 5.7)
    ax.set_xscale("log")
    ax.set_xlim(1e-19, 3e0)
    ax.set_ylim(0, 5.6)
    ax.set_yticks([])
    ax.set_xlabel("典型長度尺度（m）", fontsize=11.5)
    F.clean_grid(ax)
    levels = [
        ("人", 1.7, 4.3, F.BLUE),
        ("紅血球", 8e-6, 3.55, F.RED),
        ("分子", 1e-9, 2.80, F.GREEN),
        ("原子", 1e-10, 2.05, F.PURPLE),
        ("原子核", 1e-15, 1.30, F.AMBER),
        ("質子／中子", 8.5e-16, 0.62, "#0f766e"),
        ("電子、夸克\n尚未見內部結構", 1e-18, 4.55, "#475569"),
    ]
    for label, value, y, color in levels:
        ax.scatter([value], [y], s=90, color=color, zorder=5)
        ax.text(value * 1.18, y, f"{label}\n{value:.1e} m", ha="left", va="center", fontsize=10.3, color=color)
    ax.annotate(
        "", xy=(1e-10, 1.60), xytext=(1e-15, 1.60),
        arrowprops=dict(arrowstyle="<->", color=F.INK, lw=1.7),
    )
    ax.text(3.2e-13, 1.78, "原子尺度約為原子核的 $10^5$ 倍", ha="center", fontsize=11.2, weight="bold")
    ax.set_title("對數尺度把跨越多個數量級的結構放在同一軸", fontsize=14.5, weight="bold")
    atom, nucleus = 1e-10, 1e-15
    assert atom / nucleus == 1e5
    assert 0.03e-9 <= atom <= 0.3e-9
    _save(fig, "必物-2-物質結構尺度階梯")


def fig_rutherford_scattering():
    """金箔散射的裝置、觀測與模型推論。"""
    fig, ax = F.canvas(12.0, 6.8)
    ax.axis("off")
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 7.4)

    ax.add_patch(Rectangle((0.45, 2.65), 1.05, 1.55, facecolor="#e2e8f0", edgecolor=F.INK, lw=1.6))
    ax.text(0.98, 3.43, "$\\alpha$ 源", ha="center", va="center", fontsize=11.5)
    ax.add_patch(Rectangle((1.85, 2.85), 0.28, 1.15, facecolor=F.INK))
    ax.add_patch(Rectangle((2.45, 2.85), 0.28, 1.15, facecolor=F.INK))
    ax.text(2.30, 2.43, "準直狹縫", ha="center", fontsize=10.4)
    ax.add_patch(Rectangle((4.35, 1.70), 0.10, 3.45, facecolor="#facc15", edgecolor="#a16207", lw=1.2))
    ax.text(4.40, 1.36, "金箔", ha="center", fontsize=10.4)
    theta = np.linspace(-1.18, 1.18, 140)
    ax.plot(4.40 + 1.72 * np.cos(theta), 3.42 + 1.72 * np.sin(theta), color=F.GREEN, lw=3.0)
    ax.text(5.65, 5.15, "閃爍屏", color=F.GREEN, fontsize=10.6)
    for y in (3.18, 3.42, 3.66):
        F.arrow(ax, (1.50, y), (4.20, y), color=F.BLUE, lw=1.5, mutation=8)

    nucleus = np.array([8.45, 3.42])
    ax.add_patch(Circle(nucleus, 0.22, facecolor=F.RED, edgecolor="#991b1b", lw=1.4, zorder=5))
    ax.text(8.45, 2.95, "小而帶正電的原子核", ha="center", fontsize=10.5, color=F.RED)
    trajectories = [
        [(6.35, 4.65), (7.30, 4.62), (8.18, 4.80), (9.55, 5.35)],
        [(6.35, 4.03), (7.42, 4.02), (8.12, 4.20), (9.48, 4.62)],
        [(6.35, 3.68), (7.40, 3.68), (8.02, 3.82), (9.40, 4.12)],
        [(6.35, 3.42), (7.25, 3.42), (7.88, 3.42), (6.80, 2.55)],
        [(6.35, 2.96), (7.45, 2.96), (8.12, 2.72), (9.52, 2.12)],
    ]
    for i, pts in enumerate(trajectories):
        _curve_arrow(ax, pts, F.BLUE if i != 3 else F.RED, lw=1.6)
    ax.text(8.75, 5.80, "多數近直行、少數偏折、極少數大角度反彈", ha="center", fontsize=11.5, weight="bold")
    _rounded(ax, (6.20, 0.55), (1.65, 0.92), "比例示意 986／1000\n近直行", fc="#dcfce7", ec=F.GREEN, fs=9.7)
    _rounded(ax, (8.05, 0.55), (1.65, 0.92), "比例示意 13／1000\n明顯偏折", fc="#fef3c7", ec=F.AMBER, fs=9.7)
    _rounded(ax, (9.90, 0.55), (1.65, 0.92), "比例示意 1／1000\n大角反彈", fc="#fee2e2", ec=F.RED, fs=9.7)
    ax.text(6.0, 6.95, "散射角分布決定原子內正電與質量的空間分布", ha="center", fontsize=14.7, weight="bold")
    counts = np.array([986, 13, 1])
    assert counts.sum() == 1000 and counts[0] > counts[1] > counts[2]
    assert np.linalg.norm(nucleus - np.array([8.45, 3.42])) == 0
    _save(fig, "必物-2-拉塞福散射與原子核")


def fig_nuclide_quarks():
    """核素記號與質子、中子的夸克電荷總和。"""
    fig, ax = F.canvas(12.0, 6.2)
    ax.axis("off")
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 7)
    ax.text(2.55, 5.85, r"$^{23}_{11}\mathrm{Na}^{+}$", ha="center", fontsize=34, color=F.BLUE)
    _rounded(ax, (0.45, 3.70), (2.00, 1.02), "$Z=11$\n質子 11", fc="#fee2e2", ec=F.RED, fs=12.0)
    _rounded(ax, (2.65, 3.70), (2.00, 1.02), "$N=A-Z=12$\n中子 12", fc="#e2e8f0", ec="#64748b", fs=12.0)
    _rounded(ax, (1.55, 2.20), (2.00, 1.02), "電荷 $+1$\n電子 $11-1=10$", fc="#dbeafe", ec=F.BLUE, fs=11.5)
    ax.text(2.55, 1.35, "元素由質子數決定；同位素可有不同中子數", ha="center", fontsize=11.3, weight="bold")

    def baryon(cx, cy, title, labels, charges, color):
        ax.add_patch(Circle((cx, cy), 1.35, facecolor="#f8fafc", edgecolor=color, lw=2.0))
        positions = [(cx, cy + 0.54), (cx - 0.52, cy - 0.36), (cx + 0.52, cy - 0.36)]
        for (px, py), label, charge in zip(positions, labels, charges):
            fc = F.RED if label == "u" else F.BLUE
            ax.add_patch(Circle((px, py), 0.35, facecolor=fc, edgecolor="white", lw=1.2))
            ax.text(px, py + 0.03, label, ha="center", va="center", fontsize=14, color="white", weight="bold")
            ax.text(px, py - 0.52, charge, ha="center", fontsize=9.8, color=fc)
        ax.text(cx, cy + 1.70, title, ha="center", fontsize=13.0, weight="bold", color=color)

    baryon(7.15, 3.55, "質子：uud", ["u", "u", "d"],
           [r"$+\frac{2}{3}e$", r"$+\frac{2}{3}e$", r"$-\frac{1}{3}e$"], F.RED)
    baryon(10.25, 3.55, "中子：udd", ["u", "d", "d"],
           [r"$+\frac{2}{3}e$", r"$-\frac{1}{3}e$", r"$-\frac{1}{3}e$"], F.BLUE)
    ax.text(7.15, 1.38, r"$\frac{2}{3}+\frac{2}{3}-\frac{1}{3}=+1$", ha="center", fontsize=13.0, color=F.RED)
    ax.text(10.25, 1.38, r"$\frac{2}{3}-\frac{1}{3}-\frac{1}{3}=0$", ha="center", fontsize=13.0, color=F.BLUE)
    ax.text(8.70, 6.45, "夸克分率電荷相加，得到核子的整數電荷", ha="center", fontsize=14.2, weight="bold")
    assert 23 - 11 == 12 and 11 - 1 == 10
    assert 2 * Fraction(2, 3) - Fraction(1, 3) == 1
    assert Fraction(2, 3) - 2 * Fraction(1, 3) == 0
    _save(fig, "必物-2-核素記號與夸克組成")


def fig_gravity_inverse_square():
    """萬有引力方向與距離平方反比。"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.8, 5.6))
    for ax in (ax1, ax2):
        ax.set_facecolor("white")

    ax1.axis("off")
    ax1.set_xlim(0, 10)
    ax1.set_ylim(0, 7)
    c1, c2 = np.array([2.0, 3.7]), np.array([8.0, 3.7])
    ax1.add_patch(Circle(c1, 0.72, facecolor="#dbeafe", edgecolor=F.BLUE, lw=2.0))
    ax1.add_patch(Circle(c2, 1.02, facecolor="#fee2e2", edgecolor=F.RED, lw=2.0))
    ax1.text(*c1, "$m_1$", ha="center", va="center", fontsize=16)
    ax1.text(*c2, "$m_2$", ha="center", va="center", fontsize=16)
    F.arrow(ax1, (2.72, 3.7), (4.52, 3.7), color=F.BLUE, lw=2.2, mutation=12)
    F.arrow(ax1, (6.98, 3.7), (5.18, 3.7), color=F.RED, lw=2.2, mutation=12)
    ax1.text(3.65, 4.08, "$F_{21}$", ha="center", fontsize=13, color=F.BLUE)
    ax1.text(6.05, 4.08, "$F_{12}$", ha="center", fontsize=13, color=F.RED)
    ax1.annotate("", xy=(8.0, 1.55), xytext=(2.0, 1.55),
                 arrowprops=dict(arrowstyle="<->", color=F.INK, lw=1.7))
    ax1.text(5.0, 1.12, "中心距離 $r$", ha="center", fontsize=12)
    ax1.text(5.0, 6.10, "兩力沿連心線、大小相等、各自指向對方", ha="center",
             fontsize=12.0, weight="bold")
    ax1.text(5.0, 0.42, r"$F=G\frac{m_1m_2}{r^2}$", ha="center", fontsize=17, color=F.PURPLE)

    x = np.linspace(0.80, 3.2, 240)
    y = 1 / x**2
    ax2.plot(x, y, color=F.PURPLE, lw=2.5)
    pts = np.array([1.0, 2.0, 3.0])
    vals = 1 / pts**2
    ax2.scatter(pts, vals, s=58, color=[F.RED, F.BLUE, F.GREEN], zorder=5)
    for px, py, label in zip(pts, vals, ("$F_0$", "$F_0/4$", "$F_0/9$")):
        ax2.text(px + 0.05, py + 0.06, label, fontsize=10.5)
    ax2.set_xlabel("$r/r_0$")
    ax2.set_ylabel("$F/F_0$")
    ax2.set_xlim(0.75, 3.25)
    ax2.set_ylim(0, 1.65)
    ax2.set_title("質量固定時的平方反比", fontsize=13.0, weight="bold")
    F.clean_grid(ax2)
    fig.tight_layout(w_pad=2.0)
    assert np.allclose(vals, [1.0, 0.25, 1 / 9])
    assert np.isclose(np.linalg.norm(c2 - c1), 6.0)
    _save(fig, "必物-2-萬有引力與平方反比")


def fig_electric_field():
    """庫侖力方向、作用反作用與正負點電荷的電場線。"""
    fig, ax = F.canvas(12.0, 6.6)
    ax.axis("off")
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 7.2)

    qpos, qneg = np.array([2.0, 4.55]), np.array([5.25, 4.55])
    ax.add_patch(Circle(qpos, 0.38, facecolor=F.RED, edgecolor="#991b1b", lw=1.5))
    ax.add_patch(Circle(qneg, 0.38, facecolor=F.BLUE, edgecolor="#1d4ed8", lw=1.5))
    ax.text(*qpos, "$+q$", ha="center", va="center", fontsize=13, color="white", weight="bold")
    ax.text(*qneg, "$-Q$", ha="center", va="center", fontsize=13, color="white", weight="bold")
    F.arrow(ax, (2.38, 4.55), (3.38, 4.55), color=F.RED, lw=2.2, mutation=12)
    F.arrow(ax, (4.87, 4.55), (3.87, 4.55), color=F.BLUE, lw=2.2, mutation=12)
    ax.annotate("", xy=(5.25, 3.52), xytext=(2.0, 3.52),
                arrowprops=dict(arrowstyle="<->", color=F.INK, lw=1.5))
    ax.text(3.63, 3.18, "$r$", ha="center", fontsize=12)
    ax.text(3.63, 5.37, "異號相吸；兩力大小相等、方向相反", ha="center", fontsize=11.7, weight="bold")
    ax.text(3.63, 2.15, r"$F=k\frac{|qQ|}{r^2}$", ha="center", fontsize=16, color=F.PURPLE)

    centers = [(8.15, 4.45, +1, F.RED, "$+Q$"), (10.45, 4.45, -1, F.BLUE, "$-Q$")]
    for cx, cy, sign, color, label in centers:
        ax.add_patch(Circle((cx, cy), 0.30, facecolor=color, edgecolor="white", lw=1.0, zorder=5))
        ax.text(cx, cy, label, ha="center", va="center", fontsize=11.5, color="white", weight="bold")
        for deg in range(0, 360, 45):
            ang = np.deg2rad(deg)
            inner = np.array([cx, cy]) + 0.38 * np.array([np.cos(ang), np.sin(ang)])
            outer = np.array([cx, cy]) + 1.00 * np.array([np.cos(ang), np.sin(ang)])
            start, end = (inner, outer) if sign > 0 else (outer, inner)
            F.arrow(ax, start, end, color=color, lw=1.25, mutation=7)
    ax.text(9.30, 6.05, "正試驗電荷的受力方向定義電場方向", ha="center", fontsize=11.5, weight="bold")
    ax.text(9.30, 2.72, "正電荷向外；負電荷向內", ha="center", fontsize=11.3)
    ax.text(9.30, 1.28, r"$\vec E=\vec F/q_0\quad(q_0>0)$", ha="center", fontsize=15, color=F.GREEN)
    scale = (2 * 3) / (2**2)
    assert np.isclose(scale, 1.5)
    assert np.isclose(1 / 2**2, 0.25)
    _save(fig, "必物-2-庫侖力與電場線")


def fig_magnetic_field():
    """棒磁鐵的閉合場線與鐵磁物的感應磁化。"""
    fig, ax = F.canvas(12.0, 6.4)
    ax.axis("off")
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 7.1)

    ax.add_patch(Rectangle((1.55, 3.05), 1.75, 0.90, facecolor=F.RED, edgecolor=F.INK, lw=1.6))
    ax.add_patch(Rectangle((3.30, 3.05), 1.75, 0.90, facecolor=F.BLUE, edgecolor=F.INK, lw=1.6))
    ax.text(2.42, 3.50, "N", ha="center", va="center", color="white", fontsize=17, weight="bold")
    ax.text(4.18, 3.50, "S", ha="center", va="center", color="white", fontsize=17, weight="bold")
    for lift in (0.80, 1.45, 2.05):
        _curve_arrow(
            ax,
            [(2.35, 3.98), (2.25, 3.98 + lift), (4.35, 3.98 + lift), (4.25, 3.98)],
            F.GREEN, lw=1.45,
        )
        _curve_arrow(
            ax,
            [(2.35, 3.02), (2.25, 3.02 - lift), (4.35, 3.02 - lift), (4.25, 3.02)],
            F.GREEN, lw=1.45,
        )
    F.arrow(ax, (4.65, 3.50), (1.95, 3.50), color="#f8fafc", lw=1.7, mutation=8)
    ax.text(3.30, 6.42, "外部場線 N→S；磁鐵內部 S→N，構成閉合曲線", ha="center",
            fontsize=11.8, weight="bold")

    ax.add_patch(Rectangle((7.05, 3.45), 1.55, 0.85, facecolor=F.RED, edgecolor=F.INK, lw=1.5))
    ax.add_patch(Rectangle((8.60, 3.45), 1.55, 0.85, facecolor=F.BLUE, edgecolor=F.INK, lw=1.5))
    ax.text(7.82, 3.88, "N", ha="center", va="center", color="white", fontsize=15, weight="bold")
    ax.text(9.38, 3.88, "S", ha="center", va="center", color="white", fontsize=15, weight="bold")
    ax.add_patch(Rectangle((6.10, 1.70), 0.42, 2.15, facecolor="#cbd5e1", edgecolor="#475569", lw=1.3))
    ax.text(6.31, 3.42, "S", ha="center", va="center", fontsize=11, color=F.BLUE, weight="bold")
    ax.text(6.31, 2.05, "N", ha="center", va="center", fontsize=11, color=F.RED, weight="bold")
    F.arrow(ax, (6.56, 3.88), (7.00, 3.88), color=F.RED, lw=2.0, mutation=10)
    ax.text(8.15, 5.15, "鐵磁材料靠近 N 極", ha="center", fontsize=11.6, weight="bold")
    ax.text(8.15, 1.10, "近端感應成 S 極，因此受到吸引", ha="center", fontsize=11.4)
    ax.text(6.0, 6.85, "磁場方向由小磁針 N 極指向決定；磁化改變材料內部磁區排列", ha="center",
            fontsize=14.2, weight="bold")
    assert 7.05 < 8.60 < 10.15
    assert 6.31 < 7.05
    _save(fig, "必物-2-磁場線與磁化")


def fig_strong_weak():
    """強作用維持核子與原子核；弱作用使粒子種類改變。"""
    fig, ax = F.canvas(12.0, 6.7)
    ax.axis("off")
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 7.3)

    center = np.array([2.75, 3.75])
    nucleons = [
        (-0.62, 0.50, "p", F.RED), (0.00, 0.64, "n", F.BLUE), (0.62, 0.46, "p", F.RED),
        (-0.72, -0.16, "n", F.BLUE), (0.00, -0.10, "p", F.RED), (0.72, -0.20, "n", F.BLUE),
        (-0.32, -0.72, "p", F.RED), (0.38, -0.68, "n", F.BLUE),
    ]
    for dx, dy, label, color in nucleons:
        p = center + np.array([dx, dy])
        ax.add_patch(Circle(p, 0.32, facecolor=color, edgecolor="white", lw=1.0, zorder=4))
        ax.text(*p, label, ha="center", va="center", color="white", fontsize=12, weight="bold", zorder=5)
    F.arrow(ax, center + np.array([-0.60, 0.50]), center + np.array([0.48, 0.46]),
            color=F.GREEN, lw=2.3, mutation=9)
    F.arrow(ax, center + np.array([0.47, 0.46]), center + np.array([-0.48, 0.50]),
            color=F.GREEN, lw=2.3, mutation=9)
    ax.text(2.75, 5.62, "殘餘強作用在約 $10^{-15}$ m 內束縛核子", ha="center",
            fontsize=11.7, weight="bold", color=F.GREEN)
    ax.text(2.75, 0.62, "核內質子仍有電斥力\n穩定性由核力、核子比例與能量共同決定",
            ha="center", fontsize=10.4)

    _rounded(ax, (5.35, 4.42), (1.35, 0.98), "中子 $n$\n電荷 0", fc="#dbeafe", ec=F.BLUE, fs=11.4)
    _rounded(ax, (7.55, 5.12), (1.35, 0.98), "質子 $p$\n電荷 $+e$", fc="#fee2e2", ec=F.RED, fs=11.1)
    _rounded(ax, (7.55, 3.70), (1.35, 0.98), "電子 $e^-$\n電荷 $-e$", fc="#dbeafe", ec=F.BLUE, fs=11.1)
    _rounded(ax, (7.55, 2.28), (1.35, 0.98), "反微中子\n$\\bar\\nu_e$", fc="#f3e8ff", ec=F.PURPLE, fs=11.1)
    for end in ((7.48, 5.60), (7.48, 4.18), (7.48, 2.76)):
        F.arrow(ax, (6.78, 4.90), end, color=F.PURPLE, lw=1.7, mutation=9)
    ax.text(7.18, 6.58, r"$n\rightarrow p+e^-+\bar{\nu}_e$", ha="center", fontsize=15.5,
            color=F.PURPLE, weight="bold")
    ax.text(7.35, 0.62, "弱作用會改變粒子種類\n典型作用尺度約 $10^{-18}$ m", ha="center",
            fontsize=10.7, weight="bold")

    _rounded(ax, (9.45, 2.32), (2.05, 3.20),
             "太陽 pp 鏈第一步\n\n$p+p\\rightarrow d+e^++\\nu_e$\n\n其中一個質子\n轉成中子",
             fc="#fef3c7", ec=F.AMBER, fs=11.0)
    charge_initial = 2
    charge_final = 1 + 1 + 0
    assert charge_initial == charge_final
    assert 1e-18 < 1e-15
    _save(fig, "必物-2-強作用與弱作用")


def fig_four_interactions():
    """比較四種基本交互作用的尺度、相對強度與直接現象。"""
    fig, ax = F.canvas(12.0, 6.8)
    ax.axis("off")
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 7.4)
    rows = [
        ("強作用", F.GREEN, "$\\sim10^{-15}$ m", "$10^2$", "夸克成核子；核子成原子核"),
        ("電磁作用", F.BLUE, "可達無限遠", "$1$", "原子、分子、接觸力、光與電磁現象"),
        ("弱作用", F.PURPLE, "$\\sim10^{-18}$ m", "$10^{-4}$", "β 衰變；太陽 pp 鏈的粒子轉換"),
        ("重力", F.RED, "可達無限遠", "$10^{-37}$", "落體、行星、恆星與星系"),
    ]
    headers = ["基本交互作用", "典型作用範圍", "相對強度\n（教材尺度）", "本章可直接辨認的現象"]
    xs = [0.35, 2.55, 5.10, 7.00]
    widths = [2.05, 2.40, 1.75, 4.60]
    for x, w, h in zip(xs, widths, headers):
        _rounded(ax, (x, 5.92), (w, 0.88), h, fc="#e2e8f0", ec="#475569", fs=10.5)
    for i, (name, color, scope, strength, role) in enumerate(rows):
        y = 4.68 - i * 1.22
        vals = [name, scope, strength, role]
        for x, w, val in zip(xs, widths, vals):
            _rounded(ax, (x, y), (w, 0.96), val, fc="#f8fafc", ec=color, fs=10.5)
    ax.text(6.0, 7.05, "同一現象先辨認對象與尺度，再判斷主導交互作用", ha="center",
            fontsize=15.0, weight="bold")
    ax.text(6.0, 0.12,
            "相對強度是用固定比較尺度得到的近似值；判斷天體時，巨量質量使微弱的重力累積成主導作用。",
            ha="center", fontsize=10.4, color="#475569")
    strengths = np.array([1e2, 1.0, 1e-4, 1e-37])
    assert strengths[0] > strengths[1] > strengths[2] > strengths[3]
    assert 1e-18 < 1e-15
    _save(fig, "必物-2-四種基本交互作用尺度圖")


def fig_alpha_closest_force():
    """正原子核上方的 alpha 粒子：由幾何先定受力方向，再比較平方反比。"""
    fig, ax = F.canvas(12.0, 6.2)
    ax.axis("off")
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 7)

    nucleus = np.array([2.85, 1.55])
    alpha = np.array([2.85, 4.20])
    radial = alpha - nucleus
    r = np.linalg.norm(radial)
    unit = radial / r
    velocity_unit = np.array([1.0, 0.0])

    ax.add_patch(Circle(nucleus, 0.45, facecolor=F.RED, edgecolor="#991b1b", lw=1.7))
    ax.text(*nucleus, "+Ze", ha="center", va="center", color="white", fontsize=12, weight="bold")
    ax.add_patch(Circle(alpha, 0.34, facecolor=F.AMBER, edgecolor="#a16207", lw=1.6, zorder=5))
    ax.text(*alpha, "$+2e$", ha="center", va="center", fontsize=10.5, weight="bold")
    ax.plot([nucleus[0], alpha[0]], [nucleus[1], alpha[1]], ls="--", color="#64748b", lw=1.5)
    ax.text(3.10, 2.92, "$r$", ha="left", fontsize=13, color="#475569")

    incoming_y = alpha[1]
    F.arrow(ax, (0.35, incoming_y), (2.42, incoming_y), color=F.BLUE, lw=1.9, mutation=10)
    ax.text(1.65, incoming_y + 0.35, "入射速度", ha="center", fontsize=10.8, color=F.BLUE)
    force_end = alpha + 1.35 * unit
    F.arrow(ax, alpha + 0.24 * unit, force_end, color=F.PURPLE, lw=2.5, mutation=13)
    ax.text(force_end[0] + 0.08, force_end[1] + 0.10, "$\\vec F_e$", fontsize=13, color=F.PURPLE)
    ax.text(3.20, 6.28, "最近點：速度與核—粒子連線垂直；斥力方向遠離原子核", ha="center",
            fontsize=12.0, weight="bold")

    _rounded(ax, (7.45, 4.45), (1.55, 1.05), "距離 $r$\n力量值 $F_0$",
             fc="#dbeafe", ec=F.BLUE, fs=11.2)
    _rounded(ax, (9.75, 4.45), (1.55, 1.05), "距離 $r/2$\n力量值 $4F_0$",
             fc="#fee2e2", ec=F.RED, fs=11.2)
    F.arrow(ax, (9.08, 4.98), (9.66, 4.98), color=F.INK, lw=1.7, mutation=9)
    ax.text(9.37, 5.30, "距離減半", ha="center", fontsize=9.8)
    ax.text(9.38, 3.28, r"$F_e=k\dfrac{|(+Ze)(+2e)|}{r^2}$", ha="center",
            fontsize=15.0, color=F.PURPLE)
    ax.text(9.38, 2.30, r"$F(r/2)/F(r)=4$", ha="center", fontsize=15.0, weight="bold")
    ax.text(9.38, 1.22, "最近距離愈小，斥力與偏折通常愈大", ha="center", fontsize=11.5)

    cross = radial[0] * unit[1] - radial[1] * unit[0]
    assert np.isclose(cross, 0.0)
    assert np.isclose(np.dot(radial, velocity_unit), 0.0)
    assert np.dot(force_end - alpha, radial) > 0
    assert np.isclose((1 / (r / 2) ** 2) / (1 / r**2), 4.0)
    _save(fig, "必物-2-alpha粒子最近點受力")


def fig_surface_particle_forces():
    """星球表面正帶電微粒的重力、電力與淨力。"""
    fig, ax = F.canvas(12.0, 6.2)
    ax.axis("off")
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 7)

    planet_center = np.array([4.20, -3.55])
    planet_radius = 5.15
    ax.add_patch(Circle(planet_center, planet_radius, facecolor="#dbeafe", edgecolor=F.BLUE, lw=2.0))
    surface_y = planet_center[1] + planet_radius
    ax.plot([0.30, 8.10], [surface_y, surface_y], color=F.BLUE, lw=2.0)
    ax.text(1.38, 0.62, "星球表面", fontsize=11, color=F.BLUE)

    particle = np.array([4.20, 3.55])
    ax.add_patch(Circle(particle, 0.34, facecolor=F.AMBER, edgecolor="#a16207", lw=1.6, zorder=5))
    ax.text(*particle, "$+q$", ha="center", va="center", fontsize=11.0, weight="bold")
    ax.plot([particle[0], particle[0]], [surface_y, particle[1] - 0.34], ls=":", color="#64748b", lw=1.3)

    fe = 1.0e-8
    fg = 9.8e-9
    force_scale = 1.55 / fe
    up_start = particle + np.array([0.0, 0.35])
    up_end = up_start + np.array([0.0, fe * force_scale])
    down_start = particle - np.array([0.0, 0.35])
    down_end = down_start - np.array([0.0, fg * force_scale])
    F.arrow(ax, up_start, up_end,
            color=F.RED, lw=2.5, mutation=13)
    F.arrow(ax, down_start, down_end,
            color=F.BLUE, lw=2.5, mutation=13)
    ax.text(4.48, 5.12, "$F_e=qE=1.0\\times10^{-8}$ N（向上）", fontsize=11.5, color=F.RED)
    ax.text(4.48, 2.26, "$F_g=mg=9.8\\times10^{-9}$ N（向下）", fontsize=11.5, color=F.BLUE)

    _rounded(ax, (8.20, 4.62), (3.25, 1.12),
             "$M=4M_\\oplus,\\ R=2R_\\oplus$\n$g/g_\\oplus=4/2^2=1$",
             fc="#f8fafc", ec=F.BLUE, fs=11.7)
    _rounded(ax, (8.20, 2.65), (3.25, 1.12),
             "$E=5.0$ N/C 向上\n$q=+2.0\\times10^{-9}$ C",
             fc="#fef3c7", ec=F.AMBER, fs=11.3)
    _rounded(ax, (8.20, 0.68), (3.25, 1.12),
             "$F_{\\rm net}=2.0\\times10^{-10}$ N\n方向向上",
             fc="#dcfce7", ec=F.GREEN, fs=11.5)
    ax.text(6.0, 6.55, "先由圖固定兩力方向，再比較量值", ha="center", fontsize=14.6, weight="bold")

    assert fe > fg > 0
    assert np.isclose(fe - fg, 2.0e-10)
    assert np.isclose((4.0) / (2.0**2), 1.0)
    assert down_end[1] > surface_y
    assert np.isclose(np.linalg.norm(up_end - up_start) / np.linalg.norm(down_end - down_start), fe / fg)
    _save(fig, "必物-2-星球表面帶電微粒受力")


def main():
    for function_name, _filename in FIGURE_OUTPUTS:
        globals()[function_name]()


if __name__ == "__main__":
    main()
