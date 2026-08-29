# -*- coding: utf-8 -*-
"""產生「選化 II-2 物質的性質與化學鍵」學生講義章內 SVG。

重繪：.venv/bin/python _tools/fig_content_選化II-2.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, Ellipse, FancyBboxPatch, Polygon, Rectangle

import figlib as F


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CH = os.path.join(ROOT, "content", "選修化學II", "選化II-2")


FIGURE_OUTPUTS = (
    ("fig_bonding_materials", "選化II-2-鍵結模型與材料性質.svg"),
    ("fig_ionic_lattice", "選化II-2-離子晶格與晶格能.svg"),
    ("fig_metallic_bond", "選化II-2-金屬鍵與材料變形.svg"),
    ("fig_covalent_energy", "選化II-2-共價鍵能量與鍵長.svg"),
    ("fig_sigma_pi", "選化II-2-單鍵多鍵與sigma-pi.svg"),
    ("fig_hybridization", "選化II-2-sp3-sp2-sp混成模型.svg"),
    ("fig_vsepr", "選化II-2-VSEPR電子域與分子形狀.svg"),
    ("fig_dipole_vectors", "選化II-2-鍵偶極向量和.svg"),
    ("fig_intermolecular_forces", "選化II-2-分子間作用力.svg"),
    ("fig_boiling_data", "選化II-2-沸點資料與分子結構.svg"),
)


def _save(fig, filename):
    assert filename.endswith(".svg")
    return F.save_to(fig, CH, filename[:-4], output_subdir="assets", write_pdf=False)


def _box(ax, xy, width, height, text, *, face="#f8fafc", edge="#64748b", fs=10.5, lw=1.5):
    patch = FancyBboxPatch(
        xy,
        width,
        height,
        boxstyle="round,pad=0.035,rounding_size=0.08",
        facecolor=face,
        edgecolor=edge,
        lw=lw,
    )
    ax.add_patch(patch)
    ax.text(xy[0] + width / 2, xy[1] + height / 2, text, ha="center", va="center", fontsize=fs)
    return patch


def _atom(ax, xy, label, *, radius=0.31, face="#eef4ff", edge=F.BLUE, fs=10.5, z=4):
    ax.add_patch(Circle(xy, radius, facecolor=face, edgecolor=edge, lw=1.6, zorder=z))
    ax.text(*xy, label, ha="center", va="center", fontsize=fs, zorder=z + 1)


def _bond(ax, p1, p2, *, count=1, color=F.INK, lw=2.1, offset=0.10, z=2):
    p1 = np.asarray(p1, dtype=float)
    p2 = np.asarray(p2, dtype=float)
    d = p2 - p1
    d /= np.linalg.norm(d)
    normal = np.array([-d[1], d[0]])
    offsets = np.linspace(-(count - 1) * offset / 2, (count - 1) * offset / 2, count)
    for off in offsets:
        q1, q2 = p1 + off * normal, p2 + off * normal
        ax.plot([q1[0], q2[0]], [q1[1], q2[1]], color=color, lw=lw, zorder=z)


def _molecule(ax, center, kind, scale=1.0):
    """畫出本章反覆使用的簡化分子幾何。"""
    cx, cy = center
    if kind == "co2":
        pts = [(cx - 1.05 * scale, cy), (cx, cy), (cx + 1.05 * scale, cy)]
        _bond(ax, pts[0], pts[1], count=2)
        _bond(ax, pts[1], pts[2], count=2)
        _atom(ax, pts[0], "O", radius=0.25 * scale, face="#fee2e2", edge=F.RED)
        _atom(ax, pts[1], "C", radius=0.25 * scale, face="#f1f5f9", edge=F.INK)
        _atom(ax, pts[2], "O", radius=0.25 * scale, face="#fee2e2", edge=F.RED)
    elif kind == "h2o":
        o = (cx, cy + 0.14 * scale)
        h1 = (cx - 0.86 * scale, cy - 0.55 * scale)
        h2 = (cx + 0.86 * scale, cy - 0.55 * scale)
        _bond(ax, o, h1)
        _bond(ax, o, h2)
        _atom(ax, o, "O", radius=0.28 * scale, face="#fee2e2", edge=F.RED)
        _atom(ax, h1, "H", radius=0.20 * scale)
        _atom(ax, h2, "H", radius=0.20 * scale)
    elif kind == "bf3":
        b = np.array([cx, cy])
        for angle in (90, 210, 330):
            rad = np.deg2rad(angle)
            f = b + scale * np.array([np.cos(rad), np.sin(rad)])
            _bond(ax, b, f)
            _atom(ax, f, "F", radius=0.22 * scale, face="#dcfce7", edge=F.GREEN)
        _atom(ax, b, "B", radius=0.25 * scale, face="#fff7dd", edge=F.AMBER)


def fig_bonding_materials():
    """把四種微觀結構與能由結構推得的宏觀性質放在同一張證據圖。"""
    fig, axes = plt.subplots(1, 4, figsize=(13.2, 4.9))
    titles = ["離子晶體", "金屬晶體", "分子物質", "共價網狀固體"]
    notes = [
        "正、負離子週期排列\n熔融或溶解後可導電",
        "金屬陽離子骨架＋離域電子\n可導電、可延展",
        "分子內共價鍵；分子間作用力\n熔、沸點由分子間力控制",
        "原子以共價鍵連成巨網\n通常硬、熔點高",
    ]
    for ax, title, note in zip(axes, titles, notes):
        ax.set_aspect("equal")
        ax.axis("off")
        ax.set_xlim(-2.0, 2.0)
        ax.set_ylim(-2.0, 2.25)
        ax.set_title(title, weight="bold", fontsize=13.0)
        ax.text(0, -1.62, note, ha="center", va="top", fontsize=9.6)

    ax = axes[0]
    charges = []
    for iy, y in enumerate(np.linspace(-0.75, 0.85, 4)):
        for ix, x in enumerate(np.linspace(-1.2, 1.2, 4)):
            plus = (ix + iy) % 2 == 0
            _atom(ax, (x, y), "+" if plus else "−", radius=0.24,
                  face="#dbeafe" if plus else "#fee2e2", edge=F.BLUE if plus else F.RED)
            charges.append(1 if plus else -1)
    assert sum(charges) == 0

    ax = axes[1]
    for y in (-0.65, 0.05, 0.75):
        for x in (-1.15, -0.38, 0.38, 1.15):
            _atom(ax, (x, y), "+", radius=0.22, face="#dbeafe", edge=F.BLUE)
    for x, y in [(-0.80, -0.28), (0.0, -0.30), (0.78, -0.31), (-0.38, 0.40), (0.43, 0.38), (1.15, 0.38)]:
        ax.add_patch(Circle((x, y), 0.075, facecolor=F.AMBER, edgecolor=F.AMBER, zorder=6))
    F.arrow(ax, (-1.35, 1.35), (1.32, 1.35), color=F.AMBER, lw=1.9, mutation=12)
    ax.text(0, 1.60, "電場下電子定向漂移", ha="center", fontsize=9.7, color=F.AMBER)

    ax = axes[2]
    for x, y in [(-0.95, 0.65), (0.75, 0.70), (-0.65, -0.20), (0.95, -0.20)]:
        _bond(ax, (x - 0.28, y), (x + 0.28, y))
        _atom(ax, (x - 0.36, y), "A", radius=0.18)
        _atom(ax, (x + 0.36, y), "B", radius=0.18, face="#fee2e2", edge=F.RED)
    for y in (0.25,):
        ax.plot([-0.25, 0.15], [y, y], ls=(0, (2, 3)), color=F.PURPLE, lw=1.7)
    ax.text(0, 1.45, "分子保持獨立", ha="center", fontsize=9.7)

    ax = axes[3]
    nodes = [(0, 1.10), (-0.90, 0.50), (0.90, 0.50), (-0.90, -0.45), (0.90, -0.45), (0, -0.95), (0, 0.0)]
    edges = [(0, 1), (0, 2), (1, 6), (2, 6), (1, 3), (2, 4), (3, 5), (4, 5), (5, 6)]
    for i, j in edges:
        _bond(ax, nodes[i], nodes[j], color=F.INK, lw=1.8)
    for p in nodes:
        _atom(ax, p, "C", radius=0.19, face="#f1f5f9", edge=F.INK, fs=8.5)
    ax.text(0, 1.55, "鍵延伸到整個晶體", ha="center", fontsize=9.7)

    fig.suptitle("由粒子種類、連接方式與可移動電荷預測材料性質", fontsize=16, y=0.985)
    fig.subplots_adjust(left=0.02, right=0.99, top=0.82, bottom=0.05, wspace=0.12)
    return _save(fig, "選化II-2-鍵結模型與材料性質.svg")


def fig_ionic_lattice():
    """用庫侖強度代理量連結電荷、距離與晶格能量級。"""
    pairs = ["NaCl", "MgO", "NaF", "KCl"]
    zprod = np.array([1, 4, 1, 1], dtype=float)
    r_pm = np.array([276, 212, 231, 314], dtype=float)
    strength = zprod / r_pm
    assert strength[1] > strength[2] > strength[0] > strength[3]

    fig, axes = plt.subplots(1, 2, figsize=(11.8, 5.8), gridspec_kw={"width_ratios": [0.88, 1.12]})
    ax = axes[0]
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_xlim(-2.0, 2.0)
    ax.set_ylim(-2.0, 2.0)
    charges = []
    for iy, y in enumerate(np.linspace(-1.05, 1.05, 4)):
        for ix, x in enumerate(np.linspace(-1.05, 1.05, 4)):
            plus = (ix + iy) % 2 == 0
            _atom(ax, (x, y), "+" if plus else "−", radius=0.23,
                  face="#dbeafe" if plus else "#fee2e2", edge=F.BLUE if plus else F.RED)
            charges.append(1 if plus else -1)
    assert sum(charges) == 0
    F.arrow(ax, (-0.58, 1.62), (0.58, 1.62), color=F.PURPLE, lw=1.7, mutation=10)
    F.arrow(ax, (0.58, 1.62), (-0.58, 1.62), color=F.PURPLE, lw=1.7, mutation=10)
    ax.text(0, 1.88, "最近鄰異號離子互相吸引", ha="center", fontsize=10.3, color=F.PURPLE)
    ax.set_title("晶格中同時有多個吸引與排斥項", fontsize=13.2, weight="bold")

    ax = axes[1]
    colors = [F.BLUE, F.RED, F.GREEN, F.AMBER]
    bars = ax.bar(pairs, strength * 1000, color=colors, alpha=0.82)
    for bar, z, r in zip(bars, zprod, r_pm):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.45,
                rf"$|z_+z_-|={z:.0f}$" + "\n" + rf"$r={r:.0f}\,pm$", ha="center", va="bottom", fontsize=9.4)
    ax.set_ylabel("庫侖強度代理量 $1000|z_+z_-|/r$")
    ax.set_ylim(0, max(strength * 1000) * 1.28)
    F.clean_grid(ax)
    ax.text(0.75, 0.95, r"$|U|\propto\dfrac{|z_+z_-|}{r}$" + "\n同一晶格型式下比較量級",
            transform=ax.transAxes, ha="center", va="top", fontsize=12.2,
            bbox={"boxstyle": "round,pad=0.35", "facecolor": "#fff7dd", "edgecolor": F.AMBER})
    ax.set_title("電荷乘積增大、離子距離縮短，吸引增強", fontsize=13.2, weight="bold")
    fig.suptitle("晶格能來自整個離子晶格的靜電作用", fontsize=16, y=0.985)
    fig.subplots_adjust(left=0.04, right=0.985, top=0.82, bottom=0.14, wspace=0.20)
    return _save(fig, "選化II-2-離子晶格與晶格能.svg")


def fig_metallic_bond():
    """以滑移前後保持吸引與電子漂移，解釋延展性和導電。"""
    fig, axes = plt.subplots(1, 3, figsize=(12.8, 4.9))
    shifts = [0.0, 0.48, 0.0]
    for k, (ax, shift) in enumerate(zip(axes, shifts)):
        ax.set_aspect("equal")
        ax.axis("off")
        ax.set_xlim(-2.0, 2.0)
        ax.set_ylim(-1.7, 1.9)
        for iy, y in enumerate((-0.8, 0.0, 0.8)):
            row_shift = shift if iy == 2 else 0.0
            for x in (-1.2, -0.4, 0.4, 1.2):
                _atom(ax, (x + row_shift, y), "+", radius=0.23, face="#dbeafe", edge=F.BLUE)
        electron_xy = [(-0.8, -0.42), (0.0, -0.40), (0.8, -0.42), (-1.2, 0.40), (-0.4, 0.42), (0.4, 0.40), (1.2, 0.42)]
        for x, y in electron_xy:
            ax.add_patch(Circle((x + (0.15 if k == 2 else 0), y), 0.075, facecolor=F.AMBER, edgecolor=F.AMBER, zorder=5))
        if k == 0:
            ax.set_title("未受力", weight="bold")
            ax.text(0, 1.42, "離域電子分布於整個晶體", ha="center", fontsize=10)
        elif k == 1:
            F.arrow(ax, (-1.7, 1.25), (1.5, 1.25), color=F.RED, lw=2.0, mutation=12)
            ax.set_title("上層原子滑移", weight="bold")
            ax.text(0, -1.35, "電子仍能在新位置提供吸引", ha="center", fontsize=10)
        else:
            F.arrow(ax, (-1.6, 1.30), (1.55, 1.30), color=F.AMBER, lw=2.2, mutation=13)
            ax.text(0, 1.58, "外加電場 $E$", ha="center", fontsize=10.5, color=F.AMBER)
            F.arrow(ax, (0.70, -1.25), (-0.70, -1.25), color=F.PURPLE, lw=2.0, mutation=12)
            ax.text(0, -1.52, "電子平均漂移方向", ha="center", fontsize=10, color=F.PURPLE)
            ax.set_title("導電", weight="bold")
    fig.suptitle("金屬鍵沒有固定兩原子方向：離域電子同時解釋滑移與導電", fontsize=16, y=0.985)
    fig.subplots_adjust(left=0.025, right=0.99, top=0.82, bottom=0.04, wspace=0.08)
    return _save(fig, "選化II-2-金屬鍵與材料變形.svg")


def fig_covalent_energy():
    """以 Morse 位能曲線定量標出平衡鍵長和解離能。"""
    r0 = 154.0
    de = 347.0
    a = 0.022
    r = np.linspace(80.0, 420.0, 900)
    u = de * (1 - np.exp(-a * (r - r0))) ** 2 - de
    i_min = int(np.argmin(u))
    assert abs(r[i_min] - r0) < 0.4
    assert abs(u[i_min] + de) < 0.05

    fig, ax = plt.subplots(figsize=(10.5, 5.9))
    ax.plot(r, u, color=F.BLUE, lw=2.7)
    ax.axhline(0, color="#64748b", lw=1.2)
    ax.axvline(r0, color=F.RED, lw=1.4, ls="--")
    ax.scatter([r0], [-de], color=F.RED, zorder=6)
    F.arrow(ax, (245, -de), (245, 0), color=F.AMBER, lw=2.0, mutation=13)
    ax.text(252, -de/2, r"$D_e=347\ kJ\,mol^{-1}$" + "\n解離需要輸入能量", va="center", fontsize=11, color=F.AMBER)
    ax.annotate(r"平衡鍵長 $r_0=154\ pm$" + "\n吸引與排斥的合力為零", (r0, -de), xytext=(190, -440),
                arrowprops={"arrowstyle": "->", "color": F.RED}, fontsize=10.6, color=F.RED)
    ax.text(
        88,
        255,
        "距離很短：\n電子雲重疊與核間排斥急增",
        ha="left",
        va="top",
        fontsize=10.4,
        bbox={"boxstyle": "round,pad=0.18", "facecolor": "white", "edgecolor": "none", "alpha": 0.88},
    )
    ax.text(350, -42, r"距離很遠：$U\to0$" + "\n兩原子趨近分離", ha="center", fontsize=10.4)
    ax.set_xlim(80, 420)
    ax.set_ylim(-485, 300)
    ax.set_xlabel("核間距 $r$/pm")
    ax.set_ylabel(r"相對位能 $U(r)$/$\mathrm{kJ\,mol^{-1}}$")
    F.clean_grid(ax)
    ax.set_title("共價鍵的穩定距離是位能最低點", fontsize=15.5, weight="bold")
    fig.subplots_adjust(left=0.12, right=0.98, top=0.88, bottom=0.13)
    return _save(fig, "選化II-2-共價鍵能量與鍵長.svg")


def fig_sigma_pi():
    """以軌域重疊方向與 C–C 鍵資料連結 σ/π 數目、轉動和鍵強。"""
    lengths = np.array([154, 134, 120], dtype=float)
    energies = np.array([347, 614, 839], dtype=float)
    assert np.all(np.diff(lengths) < 0)
    assert np.all(np.diff(energies) > 0)
    sigma = [1, 1, 1]
    pi = [0, 1, 2]
    assert [s + p for s, p in zip(sigma, pi)] == [1, 2, 3]

    fig, axes = plt.subplots(2, 3, figsize=(12.2, 7.3), gridspec_kw={"height_ratios": [1.15, 0.85]})
    labels = [("C—C", 1), ("C=C", 2), ("C≡C", 3)]
    for col, (label, order) in enumerate(labels):
        ax = axes[0, col]
        ax.set_aspect("equal")
        ax.axis("off")
        ax.set_xlim(-2.0, 2.0)
        ax.set_ylim(-1.65, 1.75)
        ax.add_patch(Ellipse((-0.57, 0), 1.65, 0.72, facecolor="#bfdbfe", edgecolor=F.BLUE, alpha=0.75))
        ax.add_patch(Ellipse((0.57, 0), 1.65, 0.72, facecolor="#bfdbfe", edgecolor=F.BLUE, alpha=0.75))
        ax.text(0, 0, r"$\sigma$", ha="center", va="center", fontsize=14, weight="bold")
        if order >= 2:
            for y in (-0.76, 0.76):
                ax.add_patch(Ellipse((-0.55, y), 0.76, 0.72, facecolor="#ddd6fe", edgecolor=F.PURPLE, alpha=0.66))
                ax.add_patch(Ellipse((0.55, y), 0.76, 0.72, facecolor="#ddd6fe", edgecolor=F.PURPLE, alpha=0.66))
            ax.text(0, 1.25, r"$\pi_1$", ha="center", color=F.PURPLE, fontsize=11)
        if order == 3:
            # 以軌域截面表示第二組 p 軌域垂直紙面；兩個綠圈的側向重疊發生在紙面前後。
            for xpos, symbol in ((-0.55, "⊙"), (0.55, "⊗")):
                ax.add_patch(Circle((xpos, 0), 0.43, facecolor="#dcfce7", edgecolor=F.GREEN, alpha=0.55, lw=1.5))
                ax.text(xpos, 0, symbol, ha="center", va="center", color=F.GREEN, fontsize=14)
            ax.text(0, -1.25, r"$\pi_2$：另一組 p 軌域垂直紙面", ha="center", color=F.GREEN, fontsize=10.0)
        _atom(ax, (-0.55, 0), "C", radius=0.20, face="#f1f5f9", edge=F.INK, fs=8.5)
        _atom(ax, (0.55, 0), "C", radius=0.20, face="#f1f5f9", edge=F.INK, fs=8.5)
        ax.set_title(f"{label}：1σ + {order-1}π", fontsize=13, weight="bold")

    x = np.arange(3)
    ax = axes[1, 0]
    ax.bar(x, lengths, color=[F.BLUE, F.PURPLE, F.GREEN], alpha=0.82)
    ax.set_xticks(x, ["單鍵", "雙鍵", "三鍵"])
    ax.set_ylabel("C—C 鍵長 / pm")
    ax.set_ylim(0, 180)
    F.clean_grid(ax)
    ax = axes[1, 1]
    ax.bar(x, energies, color=[F.BLUE, F.PURPLE, F.GREEN], alpha=0.82)
    ax.set_xticks(x, ["單鍵", "雙鍵", "三鍵"])
    ax.set_ylabel(r"總鍵能 / $\mathrm{kJ\,mol^{-1}}$")
    ax.set_ylim(0, 920)
    F.clean_grid(ax)
    ax = axes[1, 2]
    ax.axis("off")
    _box(ax, (0.06, 0.58), 0.88, 0.30, "單鍵：繞鍵軸轉動不破壞 σ 重疊", face="#eef4ff", edge=F.BLUE, fs=10.2)
    _box(ax, (0.06, 0.17), 0.88, 0.30, "雙鍵：轉動會破壞 π 側向重疊", face="#f5f3ff", edge=F.PURPLE, fs=10.2)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    fig.suptitle("每對相連原子只有一個 σ 鍵；其餘鍵級由 π 鍵增加", fontsize=16, y=0.985)
    fig.subplots_adjust(left=0.05, right=0.99, top=0.86, bottom=0.08, wspace=0.22, hspace=0.22)
    return _save(fig, "選化II-2-單鍵多鍵與sigma-pi.svg")


def fig_hybridization():
    """同時顯示混成軌域數、剩餘 p 軌域、幾何與碳氫化合物鍵帳。"""
    models = [
        ("sp³", 4, 0, 109.5, r"$CH_4$", "4 個 σ；0 個 π"),
        ("sp²", 3, 1, 120.0, r"$C_2H_4$", "5 個 σ；1 個 π"),
        ("sp", 2, 2, 180.0, r"$C_2H_2$", "3 個 σ；2 個 π"),
    ]
    assert [m[1] + m[2] for m in models] == [4, 4, 4]
    assert [m[3] for m in models] == [109.5, 120.0, 180.0]

    fig, axes = plt.subplots(2, 3, figsize=(12.4, 7.2), gridspec_kw={"height_ratios": [1.1, 0.9]})
    for col, (name, hybrids, p_left, angle, molecule, account) in enumerate(models):
        ax = axes[0, col]
        ax.set_aspect("equal")
        ax.axis("off")
        ax.set_xlim(-2.0, 2.0)
        ax.set_ylim(-1.7, 1.8)
        center = np.array([0.0, 0.0])
        if name == "sp³":
            # 四方向是四面體的二維投影；避免把兩個軌域畫成共線重疊。
            ends = [(-1.10, 0.22), (1.10, 0.22), (-0.44, -1.06), (0.44, 1.06)]
            styles = ["solid", "solid", "dashed", "solid"]
        elif name == "sp²":
            ends = [(0, 1.25), (-1.08, -0.62), (1.08, -0.62)]
            styles = ["solid"] * 3
        else:
            ends = [(-1.35, 0), (1.35, 0)]
            styles = ["solid"] * 2
        for (x, y), style in zip(ends, styles):
            ax.plot([0, x], [0, y], color=F.BLUE, lw=2.0, ls=":" if style == "dashed" else "-")
            ax.add_patch(Ellipse((x*0.72, y*0.72), 0.68, 0.32, angle=np.degrees(np.arctan2(y, x)),
                                 facecolor="#bfdbfe", edgecolor=F.BLUE, alpha=0.85))
        if p_left >= 1:
            for y in (-0.75, 0.75):
                ax.add_patch(Ellipse((0, y), 0.36, 0.86, facecolor="#ddd6fe", edgecolor=F.PURPLE, alpha=0.72))
        if p_left == 2:
            for x in (-0.75, 0.75):
                ax.add_patch(Ellipse((x, 0), 0.86, 0.36, facecolor="#dcfce7", edgecolor=F.GREEN, alpha=0.52))
        _atom(ax, (0, 0), "C", radius=0.24, face="#f1f5f9", edge=F.INK)
        ax.set_title(f"{name}：{hybrids} 個混成軌域", fontsize=13, weight="bold")
        ax.text(0, -1.45, f"剩餘 {p_left} 個未混成 p；理想角 {angle:g}°", ha="center", fontsize=10.1)

        ax2 = axes[1, col]
        ax2.axis("off")
        ax2.set_xlim(0, 1)
        ax2.set_ylim(0, 1)
        _box(ax2, (0.08, 0.60), 0.84, 0.25, f"價軌域帳：{hybrids} 混成 + {p_left} p = 4", face="#f8fafc", edge=F.INK, fs=10.4)
        _box(ax2, (0.08, 0.20), 0.84, 0.25, f"{molecule}：{account}", face="#fff7dd", edge=F.AMBER, fs=10.4)
    fig.suptitle("混成模型重組同一原子的價軌域，以配合成鍵方向與 π 鍵數", fontsize=16, y=0.985)
    fig.subplots_adjust(left=0.03, right=0.99, top=0.84, bottom=0.05, wspace=0.12, hspace=0.06)
    return _save(fig, "選化II-2-sp3-sp2-sp混成模型.svg")


def fig_vsepr():
    """把電子域幾何、AXmEn 記號與實測角度收在同一判斷流程。"""
    molecules = [
        (r"$CO_2$", r"$AX_2$", 2, 0, 180.0, "直線形"),
        (r"$BF_3$", r"$AX_3$", 3, 0, 120.0, "平面三角形"),
        (r"$CH_4$", r"$AX_4$", 4, 0, 109.5, "四面體"),
        (r"$NH_3$", r"$AX_3E$", 4, 1, 107.0, "三角錐"),
        (r"$H_2O$", r"$AX_2E_2$", 4, 2, 104.5, "折線形"),
    ]
    assert molecules[2][4] > molecules[3][4] > molecules[4][4]
    assert [m[2] for m in molecules] == [2, 3, 4, 4, 4]

    fig, axes = plt.subplots(1, 5, figsize=(14.2, 4.8))
    for ax, (formula, axe, domains, lone, angle, shape) in zip(axes, molecules):
        ax.set_aspect("equal")
        ax.axis("off")
        ax.set_xlim(-1.7, 1.7)
        ax.set_ylim(-1.75, 1.75)
        if formula == r"$CO_2$":
            ends = [(-1.1, 0), (1.1, 0)]
        elif formula == r"$BF_3$":
            ends = [(0, 1.12), (-0.97, -0.56), (0.97, -0.56)]
        elif formula == r"$CH_4$":
            ends = [(-0.95, 0.18), (0.95, 0.18), (-0.38, -0.95), (0.38, 0.95)]
        elif formula == r"$NH_3$":
            ends = [(-0.9, -0.55), (0.9, -0.55), (0, 0.95)]
        else:
            ends = [(-0.88, -0.52), (0.88, -0.52)]
        for e in ends:
            _bond(ax, (0, 0), e)
            _atom(ax, e, "X", radius=0.19, face="#eef4ff", edge=F.BLUE, fs=8.8)
        _atom(ax, (0, 0), "A", radius=0.24, face="#fff7dd", edge=F.AMBER, fs=9.4)
        lone_positions = [(0, 1.06), (-0.62, 0.82)]
        for i in range(lone):
            x, y = lone_positions[i]
            ax.add_patch(Ellipse((x, y), 0.62, 0.32, facecolor="#ddd6fe", edgecolor=F.PURPLE, alpha=0.75))
            ax.text(x, y, "••", ha="center", va="center", fontsize=10, color=F.PURPLE)
        ax.text(0, -1.08, f"{shape}\n鍵角約 {angle:g}°", ha="center", va="top", fontsize=9.6)
        ax.set_title(f"{formula}\n{axe}｜{domains} 電子域", fontsize=11.6, weight="bold")
    fig.text(0.5, 0.03, r"四電子域系列：孤電子對占據較大空間，鍵角由 $CH_4$ 109.5° → $NH_3$ 107° → $H_2O$ 104.5°", ha="center", fontsize=11.2, color=F.PURPLE)
    fig.suptitle("VSEPR：先數中心原子的電子域，再由 AXmEn 命名分子形狀", fontsize=16, y=0.985)
    fig.subplots_adjust(left=0.015, right=0.995, top=0.76, bottom=0.13, wspace=0.05)
    return _save(fig, "選化II-2-VSEPR電子域與分子形狀.svg")


def fig_dipole_vectors():
    """以真實方向向量計算對稱分子和彎曲分子的鍵偶極向量和。"""
    co2 = np.array([[1.0, 0.0], [-1.0, 0.0]])
    bf3_angles = np.deg2rad([90, 210, 330])
    bf3 = np.c_[np.cos(bf3_angles), np.sin(bf3_angles)]
    theta = np.deg2rad(104.5 / 2)
    h2o = np.array([[-np.sin(theta), np.cos(theta)], [np.sin(theta), np.cos(theta)]])
    assert np.linalg.norm(co2.sum(axis=0)) < 1e-12
    assert np.linalg.norm(bf3.sum(axis=0)) < 1e-12
    h2o_sum = h2o.sum(axis=0)
    assert h2o_sum[1] > 1.2 and abs(h2o_sum[0]) < 1e-12

    fig, axes = plt.subplots(1, 3, figsize=(12.5, 4.7))
    cases = [(r"$CO_2$", co2, r"對稱相消：$\vec\mu=0$"), (r"$BF_3$", bf3, r"三向量相消：$\vec\mu=0$"), (r"$H_2O$", h2o, r"向量和沿角平分線：$\vec\mu\ne0$")]
    for ax, (name, vectors, result) in zip(axes, cases):
        ax.set_aspect("equal")
        ax.axis("off")
        ax.set_xlim(-1.75, 1.75)
        ax.set_ylim(-1.45, 1.75)
        _atom(ax, (0, 0), "中心", radius=0.24, face="#fff7dd", edge=F.AMBER, fs=8.8)
        for v in vectors:
            F.arrow(ax, (0, 0), tuple(1.08 * v), color=F.BLUE, lw=2.2, mutation=13)
            ax.text(*(1.32 * v), r"$\delta-$", ha="center", va="center", fontsize=9.5, color=F.BLUE)
        total = vectors.sum(axis=0)
        if np.linalg.norm(total) > 1e-8:
            F.arrow(ax, (0, 0), tuple(0.85 * total), color=F.RED, lw=3.0, mutation=15)
            ax.text(*(0.98 * total), r"$\vec\mu_{mol}$", ha="center", va="bottom", color=F.RED, fontsize=10.5)
        else:
            ax.add_patch(Circle((0, 0), 0.10, facecolor="none", edgecolor=F.RED, lw=2.0))
            ax.plot([-0.07, 0.07], [-0.07, 0.07], color=F.RED, lw=1.8)
        ax.set_title(name, fontsize=14, weight="bold")
        ax.text(0, -1.22, result, ha="center", fontsize=10.8)
    fig.suptitle("分子極性取決於所有鍵偶極的向量和，也取決於分子形狀", fontsize=16, y=0.985)
    fig.subplots_adjust(left=0.035, right=0.99, top=0.79, bottom=0.04, wspace=0.10)
    return _save(fig, "選化II-2-鍵偶極向量和.svg")


def fig_intermolecular_forces():
    """以電子分布與供受體位置區分四類分子間作用力。"""
    fig, axes = plt.subplots(1, 4, figsize=(14.2, 4.8))
    headings = ["偶極—偶極力", "偶極—誘發偶極力", "分散力", "氫鍵"]
    for ax, title in zip(axes, headings):
        ax.set_aspect("equal")
        ax.axis("off")
        ax.set_xlim(-2, 2)
        ax.set_ylim(-1.8, 1.8)
        ax.set_title(title, fontsize=12.5, weight="bold")

    ax = axes[0]
    for cx in (-0.85, 0.85):
        ax.add_patch(Ellipse((cx, 0), 1.20, 0.62, facecolor="#eef4ff", edgecolor=F.BLUE, lw=1.5))
        ax.text(cx - 0.33, 0, r"$\delta+$", ha="center", va="center", fontsize=10, color=F.RED)
        ax.text(cx + 0.33, 0, r"$\delta-$", ha="center", va="center", fontsize=10, color=F.BLUE)
    ax.plot([-0.18, 0.18], [0, 0], color=F.PURPLE, lw=2.0, ls=(0, (2, 2)))
    ax.text(0, -0.78, "兩個永久偶極對齊", ha="center", fontsize=9.6)

    ax = axes[1]
    ax.add_patch(Ellipse((-0.85, 0), 1.20, 0.62, facecolor="#eef4ff", edgecolor=F.BLUE, lw=1.5))
    ax.text(-1.18, 0, r"$\delta+$", ha="center", fontsize=10, color=F.RED)
    ax.text(-0.52, 0, r"$\delta-$", ha="center", fontsize=10, color=F.BLUE)
    ax.add_patch(Ellipse((0.85, 0), 1.22, 0.62, facecolor="#f1f5f9", edgecolor=F.INK, lw=1.5))
    ax.add_patch(Ellipse((1.03, 0), 0.70, 0.42, facecolor="#bfdbfe", edgecolor="none", alpha=0.75))
    ax.text(0.51, 0, r"$\delta+$", ha="center", fontsize=10, color=F.RED)
    ax.text(1.18, 0, r"$\delta-$", ha="center", fontsize=10, color=F.BLUE)
    ax.text(0, -0.78, "永久偶極使鄰近電子雲偏移", ha="center", fontsize=9.3)

    ax = axes[2]
    ax.add_patch(Ellipse((-0.82, 0), 1.25, 0.64, facecolor="#f1f5f9", edgecolor=F.INK, lw=1.5))
    ax.add_patch(Ellipse((0.82, 0), 1.25, 0.64, facecolor="#f1f5f9", edgecolor=F.INK, lw=1.5))
    ax.add_patch(Ellipse((-1.02, 0), 0.72, 0.42, facecolor="#bfdbfe", edgecolor="none", alpha=0.75))
    ax.add_patch(Ellipse((0.62, 0), 0.72, 0.42, facecolor="#bfdbfe", edgecolor="none", alpha=0.75))
    ax.text(-0.45, 0, r"$\delta+$", ha="center", fontsize=9.5, color=F.RED)
    ax.text(-1.15, 0, r"$\delta-$", ha="center", fontsize=9.5, color=F.BLUE)
    ax.text(0.35, 0, r"$\delta-$", ha="center", fontsize=9.5, color=F.BLUE)
    ax.text(1.15, 0, r"$\delta+$", ha="center", fontsize=9.5, color=F.RED)
    ax.text(0, -0.78, "瞬時偶極彼此誘發；所有粒子都有", ha="center", fontsize=9.2)

    ax = axes[3]
    _atom(ax, (-1.15, 0), "O", radius=0.28, face="#fee2e2", edge=F.RED)
    _atom(ax, (-0.42, 0), "H", radius=0.21)
    _bond(ax, (-1.15, 0), (-0.42, 0))
    _atom(ax, (0.72, 0), "O", radius=0.28, face="#fee2e2", edge=F.RED)
    ax.plot([-0.20, 0.44], [0, 0], color=F.PURPLE, lw=2.4, ls=(0, (2, 2)))
    ax.text(0.11, 0.28, "H 鍵", ha="center", fontsize=10.2, color=F.PURPLE)
    ax.text(0, -0.78, "供體 X—H···Y 受體\nX、Y 常為 N、O、F", ha="center", fontsize=9.3)
    fig.suptitle("分子靠近後，電荷分布的相關方式決定分子間作用力", fontsize=16, y=0.985)
    fig.subplots_adjust(left=0.015, right=0.995, top=0.80, bottom=0.02, wspace=0.06)
    return _save(fig, "選化II-2-分子間作用力.svg")


def fig_boiling_data():
    """以氫化物與戊烷異構物沸點資料分離氫鍵、質量與形狀效應。"""
    group14 = np.array([-161.5, -111.8, -88.5, -52.0])
    group16 = np.array([100.0, -60.3, -41.5, -2.2])
    periods = np.arange(2, 6)
    pentane_names = ["正戊烷", "異戊烷", "新戊烷"]
    pentane_bp = np.array([36.1, 27.8, 9.5])
    assert np.all(np.diff(group14) > 0)
    assert np.all(np.diff(group16[1:]) > 0)
    assert np.all(np.diff(pentane_bp) < 0)

    fig, axes = plt.subplots(1, 2, figsize=(12.0, 5.7))
    ax = axes[0]
    ax.plot(periods, group14, marker="o", ms=7, lw=2.2, color=F.BLUE, label="第14族氫化物")
    ax.plot(periods, group16, marker="o", ms=7, lw=2.2, color=F.RED, label="第16族氫化物")
    for x, y, label in zip(periods, group14, [r"$CH_4$", r"$SiH_4$", r"$GeH_4$", r"$SnH_4$"]):
        ax.annotate(label, (x, y), xytext=(3, -14), textcoords="offset points", fontsize=9.2)
    for x, y, label in zip(periods, group16, [r"$H_2O$", r"$H_2S$", r"$H_2Se$", r"$H_2Te$"]):
        ax.annotate(label, (x, y), xytext=(3, 6), textcoords="offset points", fontsize=9.2)
    ax.annotate(r"$H_2O$ 形成廣泛氫鍵網路", (2, 100), xytext=(2.45, 65),
                arrowprops={"arrowstyle": "->", "color": F.PURPLE}, color=F.PURPLE, fontsize=10.2)
    ax.set_xticks(periods, ["第二週期", "第三週期", "第四週期", "第五週期"])
    ax.set_ylabel("正常沸點 / °C")
    ax.set_ylim(-185, 125)
    F.clean_grid(ax)
    ax.legend(frameon=False, loc="lower right")
    ax.set_title("同族向下：分散力通常隨電子雲增大", fontsize=12.8, weight="bold")

    ax = axes[1]
    bars = ax.bar(pentane_names, pentane_bp, color=[F.BLUE, F.PURPLE, F.GREEN], alpha=0.84)
    for bar, value in zip(bars, pentane_bp):
        ax.text(bar.get_x() + bar.get_width()/2, value + 1.4, f"{value:.1f}°C", ha="center", fontsize=10)
    ax.set_ylabel("正常沸點 / °C")
    ax.set_ylim(0, 43)
    F.clean_grid(ax)
    ax.text(0.5, 0.92, r"同分子式 $C_5H_{12}$" + "\n支鏈增加 → 接觸面積減少 → 分散力減弱",
            transform=ax.transAxes, ha="center", va="top", fontsize=10.8,
            bbox={"boxstyle": "round,pad=0.35", "facecolor": "#fff7dd", "edgecolor": F.AMBER})
    ax.set_title("同分子量：形狀改變接觸面積", fontsize=12.8, weight="bold")
    fig.suptitle("比較沸點要依序控制氫鍵能力、極性、電子雲大小與分子形狀", fontsize=16, y=0.985)
    fig.subplots_adjust(left=0.07, right=0.985, top=0.82, bottom=0.14, wspace=0.22)
    return _save(fig, "選化II-2-沸點資料與分子結構.svg")


def main():
    generated = []
    for entrypoint, filename in FIGURE_OUTPUTS:
        function = globals()[entrypoint]
        result = function()
        assert os.path.basename(result) == filename
        generated.append(filename)
    assert len(generated) == len(set(generated)) == 10
    assert set(generated) == {name for _, name in FIGURE_OUTPUTS}


if __name__ == "__main__":
    main()
