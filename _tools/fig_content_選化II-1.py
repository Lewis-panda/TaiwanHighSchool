# -*- coding: utf-8 -*-
"""產生「選化 II-1 原子構造與性質」學生講義章內 SVG。

重繪：.venv/bin/python _tools/fig_content_選化II-1.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, Ellipse, FancyBboxPatch, Polygon, Rectangle

import figlib as F


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CH = os.path.join(ROOT, "content", "選修化學II", "選化II-1")


FIGURE_OUTPUTS = (
    ("fig_em_spectrum", "選化II-1-電磁波與光子能量.svg"),
    ("fig_photoelectric", "選化II-1-光電效應能量帳.svg"),
    ("fig_spectra", "選化II-1-連續光譜與線光譜.svg"),
    ("fig_hydrogen_levels", "選化II-1-氫原子能階與譜線.svg"),
    ("fig_quantum_tree", "選化II-1-量子數與軌域容量.svg"),
    ("fig_orbitals", "選化II-1-s與p軌域邊界面.svg"),
    ("fig_energy_ordering", "選化II-1-單多電子能階順序.svg"),
    ("fig_filling_rules", "選化II-1-電子填排三原則.svg"),
    ("fig_periodic_blocks", "選化II-1-電子組態與週期表區塊.svg"),
    ("fig_ion_configurations", "選化II-1-原子到離子的電子帳.svg"),
    ("fig_radius", "選化II-1-原子與等電子離子半徑.svg"),
    ("fig_successive_ie", "選化II-1-逐次游離能躍升.svg"),
    ("fig_first_ie", "選化II-1-第一游離能週期趨勢.svg"),
    ("fig_electronegativity", "選化II-1-電負度與鍵極性.svg"),
    ("fig_flame_spectroscopy", "選化II-1-焰色與光譜鑑別.svg"),
)


def _save(fig, filename):
    assert filename.endswith(".svg")
    return F.save_to(fig, CH, filename[:-4], output_subdir="assets", write_pdf=False)


def _box(ax, xy, width, height, text, *, face="#f8fafc", edge="#64748b", fs=10.8, lw=1.5):
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


def _orbital_box(ax, x, y, arrows=(), *, label="", face="#ffffff", edge=F.INK):
    ax.add_patch(Rectangle((x, y), 0.72, 0.82, facecolor=face, edgecolor=edge, lw=1.4))
    for i, direction in enumerate(arrows):
        xpos = x + 0.26 + 0.24 * i
        if direction == "up":
            F.arrow(ax, (xpos, y + 0.12), (xpos, y + 0.68), color=F.BLUE, lw=1.7, mutation=9)
        else:
            F.arrow(ax, (xpos, y + 0.68), (xpos, y + 0.12), color=F.RED, lw=1.7, mutation=9)
    if label:
        ax.text(x + 0.36, y - 0.20, label, ha="center", va="top", fontsize=9.5)


def fig_em_spectrum():
    """以同一組波長、頻率、能量數值連接波形與電磁波譜。"""
    c = 2.99792458e8
    h = 6.62607015e-34
    lam = 500e-9
    nu = c / lam
    energy = h * nu
    assert np.isclose(nu, 5.99584916e14)
    assert np.isclose(energy, 3.9728917e-19, rtol=2e-8)

    fig, axes = plt.subplots(1, 2, figsize=(12.0, 5.8), gridspec_kw={"width_ratios": [0.95, 1.35]})
    ax = axes[0]
    x = np.linspace(0, 4 * np.pi, 400)
    y = np.sin(x)
    ax.plot(x, y, color=F.BLUE, lw=2.5)
    ax.axhline(0, color="#94a3b8", lw=1.0)
    x0, x1 = np.pi / 2, 5 * np.pi / 2
    ax.plot([x0, x1], [1.38, 1.38], color=F.RED, lw=1.5)
    ax.plot([x0, x0], [1.26, 1.50], color=F.RED, lw=1.5)
    ax.plot([x1, x1], [1.26, 1.50], color=F.RED, lw=1.5)
    ax.text((x0 + x1) / 2, 1.55, "一個波長 $\\lambda$", ha="center", color=F.RED, fontsize=11.5)
    ax.text(2 * np.pi, -1.58, "$c=\\lambda\\nu$", ha="center", fontsize=15, weight="bold")
    ax.text(2 * np.pi, -2.05, "同在真空中：波長越短，頻率越高", ha="center", fontsize=10.8)
    ax.set_xlim(0, 4 * np.pi)
    ax.set_ylim(-2.35, 2.05)
    ax.axis("off")
    ax.set_title("波的週期結構", fontsize=13.8, weight="bold")

    ax = axes[1]
    bands = [
        (3e6, 3e9, "無線電波", "#dbeafe"),
        (3e9, 3e11, "微波", "#bfdbfe"),
        (3e11, 4e14, "紅外線", "#fecaca"),
        (4e14, 7.5e14, "可見光", "#fde68a"),
        (7.5e14, 3e16, "紫外線", "#ddd6fe"),
        (3e16, 3e19, "X 射線", "#c4b5fd"),
        (3e19, 3e21, "$\\gamma$ 射線", "#a78bfa"),
    ]
    for lo, hi, name, color in bands:
        xlo, xhi = np.log10(lo), np.log10(hi)
        ax.add_patch(Rectangle((xlo, 0.52), xhi - xlo, 0.94, facecolor=color, edgecolor="white", lw=1.0))
        ax.text((xlo + xhi) / 2, 0.99, name, ha="center", va="center", fontsize=9.2, rotation=90 if xhi - xlo < 0.55 else 0)
    lognu = np.log10(nu)
    ax.axvline(lognu, ymin=0.32, ymax=0.86, color=F.RED, lw=2)
    ax.scatter([lognu], [0.31], color=F.RED, zorder=5)
    ax.text(lognu, 0.17, "$500\\ nm$\n$\\nu=6.00\\times10^{14}\\ Hz$\n$E=3.97\\times10^{-19}\\ J$", ha="center", va="top", fontsize=9.4, color=F.RED)
    ax.text(13.25, -0.78, "$E=h\\nu=hc/\\lambda$", fontsize=15, weight="bold", color=F.BLUE)
    F.arrow(ax, (8.3, 1.78), (20.6, 1.78), color=F.RED, lw=2.0, mutation=13)
    ax.text(14.45, 1.95, "頻率與單一光子能量增加", ha="center", fontsize=10.8, color=F.RED)
    F.arrow(ax, (20.6, -0.45), (8.3, -0.45), color=F.BLUE, lw=2.0, mutation=13)
    ax.text(14.45, -0.62, "波長增加", ha="center", fontsize=10.8, color=F.BLUE)
    ax.set_xlim(6.0, 21.6)
    ax.set_ylim(-1.0, 2.25)
    ax.set_xlabel("$\\log_{10}(\\nu/\\mathrm{Hz})$")
    ax.set_yticks([])
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.set_title("電磁波譜與光子能量", fontsize=13.8, weight="bold")
    fig.suptitle("波長決定頻率，也決定單一光子的能量", fontsize=16, y=0.985)
    fig.subplots_adjust(left=0.03, right=0.985, top=0.82, bottom=0.19, wspace=0.16)
    return _save(fig, "選化II-1-電磁波與光子能量.svg")


def fig_photoelectric():
    """用閾頻與光電子最大動能圖表示光電效應的能量帳。"""
    h = 6.62607015e-34
    e = 1.602176634e-19
    nu0 = 5.50e14
    phi_j = h * nu0
    phi_ev = phi_j / e
    assert np.isclose(phi_ev, 2.2748, rtol=2e-4)

    fig, axes = plt.subplots(1, 2, figsize=(11.8, 5.8))
    ax = axes[0]
    ax.axis("off")
    ax.set_xlim(-3.0, 3.0)
    ax.set_ylim(-2.7, 2.7)
    ax.add_patch(Rectangle((-0.75, -1.30), 2.6, 2.6, facecolor="#e2e8f0", edgecolor=F.INK, lw=1.8))
    ax.text(0.55, -1.72, "金屬表面，逸出功 $\\phi$", ha="center", fontsize=11.5)
    for y0 in (1.35, 0.45, -0.45):
        xs = np.linspace(-2.65, -0.82, 120)
        ys = y0 + 0.13 * np.sin(10 * xs)
        ax.plot(xs, ys, color=F.PURPLE, lw=2.0)
        F.arrow(ax, (-1.02, y0), (-0.76, y0), color=F.PURPLE, lw=1.5, mutation=9)
    ax.text(-1.85, 2.05, "入射光子\n$E=h\\nu$", ha="center", fontsize=11.5, color=F.PURPLE, weight="bold")
    for angle, label in [(30, "$K_{max}$"), (0, "電子"), (-34, "電子")]:
        rad = np.deg2rad(angle)
        start = (1.18, 0.25 * np.sin(rad))
        end = (2.55, 1.35 * np.sin(rad))
        F.arrow(ax, start, end, color=F.BLUE, lw=2.0, mutation=12)
        ax.text(end[0], end[1] + 0.18, label, ha="center", fontsize=10.5, color=F.BLUE)
    _box(ax, (-2.55, -2.45), 5.1, 0.56, "$h\\nu=\\phi+K_{max}$", face="#fff7dd", edge=F.AMBER, fs=14)
    ax.set_title("光子把能量交給單一電子", fontsize=13.8, weight="bold")

    ax = axes[1]
    nu = np.linspace(3.5e14, 9.0e14, 220)
    k_ev = np.maximum(0.0, (h * nu - phi_j) / e)
    ax.plot(nu / 1e14, k_ev, color=F.BLUE, lw=2.6)
    ax.axvline(nu0 / 1e14, color=F.RED, lw=1.5, ls="--")
    ax.scatter([nu0 / 1e14], [0], color=F.RED, zorder=5)
    ax.annotate("閾頻 $\\nu_0=5.50\\times10^{14}\\ Hz$", (5.5, 0), xytext=(4.0, 1.25), arrowprops={"arrowstyle": "->", "color": F.RED}, fontsize=10.2, color=F.RED)
    ax.text(6.9, 0.42, "斜率 $h$", rotation=24, color=F.BLUE, fontsize=11.5)
    ax.set_xlabel("頻率 $\\nu/(10^{14}\\ Hz)$")
    ax.set_ylabel("最大動能 $K_{max}$/eV")
    ax.set_xlim(3.5, 9.0)
    ax.set_ylim(0, 1.65)
    F.clean_grid(ax)
    ax.set_title("頻率決定電子可帶走的最大動能", fontsize=13.8, weight="bold")
    fig.suptitle("光電效應：存在閾頻，且光電子動能隨頻率線性增加", fontsize=16, y=0.985)
    fig.subplots_adjust(left=0.045, right=0.985, top=0.82, bottom=0.13, wspace=0.23)
    return _save(fig, "選化II-1-光電效應能量帳.svg")


def fig_spectra():
    """把分光路徑與連續／線光譜的觀測差異畫在同一圖。"""
    h_lines = np.array([410.2, 434.0, 486.1, 656.3])
    assert np.all(np.diff(h_lines) > 0)
    fig, axes = plt.subplots(2, 1, figsize=(11.8, 6.4), gridspec_kw={"height_ratios": [0.9, 1.1]})
    ax = axes[0]
    ax.axis("off")
    ax.set_xlim(-0.5, 11.5)
    ax.set_ylim(-1.8, 1.8)
    _box(ax, (0.0, -0.58), 1.75, 1.16, "光源／受激原子", face="#eef4ff", edge=F.BLUE, fs=11.5)
    _box(ax, (3.1, -0.58), 1.45, 1.16, "狹縫", face="#f8fafc", edge=F.INK, fs=11.5)
    ax.add_patch(Polygon([[6.0, -0.75], [6.75, 0.95], [7.5, -0.75]], closed=True, facecolor="#e2e8f0", edgecolor=F.INK, lw=1.7))
    ax.text(6.75, -1.15, "稜鏡／光柵", ha="center", fontsize=10.8)
    _box(ax, (9.25, -0.85), 1.55, 1.70, "偵測器\n位置→波長\n強度→亮度", face="#fff7dd", edge=F.AMBER, fs=10.8)
    F.arrow(ax, (1.82, 0), (3.02, 0), color=F.RED, lw=2.0, mutation=12)
    F.arrow(ax, (4.62, 0), (5.88, 0), color=F.RED, lw=2.0, mutation=12)
    for dy, color in [(0.52, "#7c3aed"), (0.17, "#2563eb"), (-0.17, "#16a34a"), (-0.52, "#dc2626")]:
        F.arrow(ax, (7.48, 0), (9.15, dy), color=color, lw=1.8, mutation=10)
    ax.set_title("分光裝置把波長轉成可量測的位置", fontsize=13.8, weight="bold")

    ax = axes[1]
    ax.set_xlim(380, 750)
    ax.set_ylim(-0.2, 2.35)
    colors = ["#6d28d9", "#2563eb", "#0891b2", "#16a34a", "#eab308", "#f97316", "#dc2626"]
    edges = np.linspace(380, 750, len(colors) + 1)
    for lo, hi, color in zip(edges[:-1], edges[1:], colors):
        ax.add_patch(Rectangle((lo, 1.42), hi - lo, 0.55, facecolor=color, edgecolor=color))
    ax.text(372, 1.70, "連續光譜", ha="right", va="center", fontsize=11.2, weight="bold")
    ax.add_patch(Rectangle((380, 0.45), 370, 0.55, facecolor="#111827", edgecolor="#111827"))
    line_colors = ["#7c3aed", "#4338ca", "#06b6d4", "#dc2626"]
    for wavelength, color in zip(h_lines, line_colors):
        ax.plot([wavelength, wavelength], [0.45, 1.0], color=color, lw=5)
        ax.text(wavelength, 0.34, f"{wavelength:.1f}", ha="center", va="top", fontsize=9.0, rotation=35)
    ax.text(372, 0.72, "氫線光譜", ha="right", va="center", fontsize=11.2, weight="bold")
    ax.set_xlabel("波長 / nm")
    ax.set_yticks([])
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.set_title("連續分布與離散譜線是兩種不同資料", fontsize=13.8, weight="bold")
    fig.suptitle("光譜是元素的能階差所留下的波長指紋", fontsize=16, y=0.985)
    fig.subplots_adjust(left=0.10, right=0.985, top=0.88, bottom=0.10, hspace=0.28)
    return _save(fig, "選化II-1-連續光譜與線光譜.svg")


def fig_hydrogen_levels():
    """由波耳能階差計算巴耳末譜線並畫出對應轉移。"""
    rh = 1.0973731568160e7
    upper = np.array([3, 4, 5, 6])
    wavelengths_nm = 1e9 / (rh * (1 / 2**2 - 1 / upper**2))
    assert np.allclose(wavelengths_nm, [656.11, 486.01, 433.94, 410.07], atol=0.05)
    levels = {n: -1312.0 / n**2 for n in range(1, 7)}
    assert np.isclose(levels[1], -1312.0)
    assert np.isclose(levels[2], -328.0)

    fig, axes = plt.subplots(1, 2, figsize=(11.8, 6.3), gridspec_kw={"width_ratios": [1.15, 0.85]})
    ax = axes[0]
    for n, energy in levels.items():
        ax.hlines(energy, 0.6, 5.8, color=F.INK, lw=1.5)
        ax.text(0.35, energy, f"$n={n}$", ha="right", va="center", fontsize=10.3)
        ax.text(5.98, energy, f"{energy:.1f}", ha="left", va="center", fontsize=9.0)
    ax.hlines(0, 0.6, 5.8, color=F.RED, lw=1.7, ls="--")
    ax.text(5.98, 0, "0（游離極限）", ha="left", va="center", fontsize=9.4, color=F.RED)
    colors = ["#dc2626", "#06b6d4", "#4338ca", "#7c3aed"]
    x_positions = [1.3, 2.45, 3.6, 4.75]
    for n, wavelength, x, color in zip(upper, wavelengths_nm, x_positions, colors):
        F.arrow(ax, (x, levels[n]), (x, levels[2] + 7), color=color, lw=2.1, mutation=12)
        ax.text(x + 0.08, (levels[n] + levels[2]) / 2, f"{wavelength:.1f} nm", rotation=90, va="center", fontsize=9.2, color=color)
    ax.set_xlim(0, 7.2)
    ax.set_ylim(-1380, 90)
    ax.set_ylabel("能量 / $\\mathrm{kJ\\,mol^{-1}}$")
    ax.set_xticks([])
    for side in ("top", "right", "bottom"):
        ax.spines[side].set_visible(False)
    ax.set_title("巴耳末系：$n_i=3,4,5,6\\to n_f=2$", fontsize=13.5, weight="bold")

    ax = axes[1]
    ax.set_xlim(380, 700)
    ax.set_ylim(-0.25, 1.65)
    ax.add_patch(Rectangle((380, 0.18), 320, 0.62, facecolor="#111827", edgecolor="#111827"))
    for wavelength, color in zip(wavelengths_nm[::-1], colors[::-1]):
        ax.plot([wavelength, wavelength], [0.18, 0.80], color=color, lw=6)
        ax.text(wavelength, 0.08, f"{wavelength:.1f}", ha="center", va="top", fontsize=9.4, rotation=35)
    ax.text(540, 1.31, r"$E_n=-1312/n^2\ \mathrm{kJ\,mol^{-1}}$", ha="center", fontsize=13.0, weight="bold", color=F.BLUE)
    ax.text(540, 1.02, "$|\\Delta E|=N_Ahc/\\lambda$", ha="center", fontsize=12.5, color=F.RED)
    ax.set_xlabel("波長 / nm")
    ax.set_yticks([])
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.set_title("同一組能階差形成四條可見譜線", fontsize=13.5, weight="bold")
    fig.suptitle("氫原子譜線把離散能階轉成可量測的波長", fontsize=16, y=0.985)
    fig.subplots_adjust(left=0.08, right=0.965, top=0.83, bottom=0.13, wspace=0.25)
    return _save(fig, "選化II-1-氫原子能階與譜線.svg")


def fig_quantum_tree():
    """逐層列出 n、l、m_l 與容量，斷言 n² 與 2n²。"""
    for n in range(1, 5):
        orbitals = sum(2 * ell + 1 for ell in range(n))
        assert orbitals == n**2
        assert 2 * orbitals == 2 * n**2

    fig, ax = plt.subplots(figsize=(12.0, 6.4))
    ax.axis("off")
    ax.set_xlim(-0.2, 12.2)
    ax.set_ylim(-0.2, 6.7)
    _box(ax, (0.15, 2.80), 1.45, 1.05, "主量子數 $n$\n電子層與尺度", face="#eef4ff", edge=F.BLUE, fs=11.2)
    F.arrow(ax, (1.65, 3.32), (2.35, 3.32), color=F.INK, lw=1.8, mutation=11)
    subshell_names = "spdf"
    row_y = [5.35, 4.05, 2.75, 1.45]
    for n, y in zip(range(1, 5), row_y):
        _box(ax, (2.45, y - 0.42), 1.25, 0.84, f"$n={n}$\n第 {n} 層", face="#f8fafc", edge=F.INK, fs=10.5)
        F.arrow(ax, (3.75, y), (4.30, y), color=F.INK, lw=1.5, mutation=10)
        subs = []
        for ell in range(n):
            count = 2 * ell + 1
            subs.append(f"{n}{subshell_names[ell]}：{count} 軌域／{2*count} 電子")
        sub_text = "；".join(subs)
        if n >= 3:
            sub_text = "；".join(subs[:2]) + "\n" + "；".join(subs[2:])
        _box(ax, (4.40, y - 0.48), 4.00, 0.96, sub_text, face="#fff7dd", edge=F.AMBER, fs=8.8)
        F.arrow(ax, (8.48, y), (8.82, y), color=F.INK, lw=1.5, mutation=10)
        _box(ax, (8.92, y - 0.46), 2.78, 0.92, f"本層共 $n^2={n*n}$ 軌域\n最多 $2n^2={2*n*n}$ 電子", face="#ecfdf5", edge=F.GREEN, fs=10.0)
    ax.text(6.15, 6.23, "$l=0,1,2,3\\leftrightarrow s,p,d,f$；每個次層有 $2l+1$ 個軌域", ha="center", fontsize=12.5, weight="bold")
    ax.text(6.15, 0.55, "每個軌域對應一個 $m_l$；每個軌域最多容納 $m_s=+1/2$、$-1/2$ 兩個電子", ha="center", fontsize=11.3, color=F.BLUE)
    fig.suptitle("四個量子數逐層指定電子的量子狀態", fontsize=16, y=0.985)
    fig.subplots_adjust(left=0.02, right=0.985, top=0.88, bottom=0.03)
    return _save(fig, "選化II-1-量子數與軌域容量.svg")


def fig_orbitals():
    """畫出 s、p 軌域的機率邊界面、方向與節面。"""
    fig, axes = plt.subplots(1, 4, figsize=(12.0, 5.4))
    panels = ["1s", "2s", "$2p_x$", "$2p_z$"]
    for ax, title in zip(axes, panels):
        ax.set_aspect("equal")
        ax.axis("off")
        ax.set_xlim(-2.2, 2.2)
        ax.set_ylim(-2.2, 2.2)
        ax.axhline(0, color="#cbd5e1", lw=1.0)
        ax.axvline(0, color="#cbd5e1", lw=1.0)
        ax.add_patch(Circle((0, 0), 0.10, facecolor=F.RED, edgecolor="white", lw=0.6, zorder=6))
        ax.set_title(title, fontsize=13.5, weight="bold")
    axes[0].add_patch(Circle((0, 0), 1.25, facecolor="#93c5fd", edgecolor=F.BLUE, alpha=0.72, lw=1.8))
    axes[0].text(0, -1.68, "球形邊界", ha="center", fontsize=10.3)
    axes[1].add_patch(Circle((0, 0), 1.55, facecolor="#bfdbfe", edgecolor=F.BLUE, alpha=0.62, lw=1.8))
    axes[1].add_patch(Circle((0, 0), 0.63, facecolor="white", edgecolor=F.PURPLE, lw=1.6, ls="--"))
    axes[1].text(0, -1.88, "一個徑向節面", ha="center", fontsize=10.3)
    axes[2].add_patch(Ellipse((-0.82, 0), 1.65, 1.05, facecolor="#93c5fd", edgecolor=F.BLUE, alpha=0.78, lw=1.6, hatch="///"))
    axes[2].add_patch(Ellipse((0.82, 0), 1.65, 1.05, facecolor="#fecaca", edgecolor=F.RED, alpha=0.78, lw=1.6, hatch="\\\\"))
    axes[2].text(-0.82, 0, "+", ha="center", va="center", fontsize=12, weight="bold")
    axes[2].text(0.82, 0, "−", ha="center", va="center", fontsize=12, weight="bold")
    axes[2].plot([0, 0], [-1.65, 1.65], color=F.PURPLE, lw=1.5, ls="--")
    axes[2].text(0, -1.88, "$yz$ 節面", ha="center", fontsize=10.3)
    axes[3].add_patch(Ellipse((0, -0.82), 1.05, 1.65, facecolor="#93c5fd", edgecolor=F.BLUE, alpha=0.78, lw=1.6, hatch="///"))
    axes[3].add_patch(Ellipse((0, 0.82), 1.05, 1.65, facecolor="#fecaca", edgecolor=F.RED, alpha=0.78, lw=1.6, hatch="\\\\"))
    axes[3].text(0, -0.82, "+", ha="center", va="center", fontsize=12, weight="bold")
    axes[3].text(0, 0.82, "−", ha="center", va="center", fontsize=12, weight="bold")
    axes[3].plot([-1.65, 1.65], [0, 0], color=F.PURPLE, lw=1.5, ls="--")
    axes[3].text(0, -1.88, "$xy$ 節面", ha="center", fontsize=10.3)
    fig.text(0.50, 0.055, "邊界面約包住 90% 電子出現機率；斜線方向與＋／−表示波函數相位，節面上的機率密度為 0", ha="center", fontsize=11.0)
    fig.suptitle("軌域描述電子出現機率的空間分布", fontsize=16, y=0.985)
    fig.subplots_adjust(left=0.02, right=0.985, top=0.82, bottom=0.14, wspace=0.08)
    return _save(fig, "選化II-1-s與p軌域邊界面.svg")


def fig_energy_ordering():
    """比較單電子原子與多電子原子的軌域能階。"""
    order = [(1, 0, "1s"), (2, 0, "2s"), (2, 1, "2p"), (3, 0, "3s"), (3, 1, "3p"), (4, 0, "4s"), (3, 2, "3d"), (4, 1, "4p")]
    keys = [(n + ell, n) for n, ell, _ in order]
    assert keys == sorted(keys)
    fig, axes = plt.subplots(1, 2, figsize=(11.8, 6.0))
    ax = axes[0]
    ax.set_xlim(0, 5.5)
    ax.set_ylim(-14.5, 0.8)
    for n in range(1, 5):
        e = -13.6 / n**2
        ax.hlines(e, 0.8, 4.7, color=F.BLUE, lw=2)
        labels = [f"{n}{s}" for s in "spdf"[:n]]
        ax.text(2.75, e + 0.20, " = ".join(labels), ha="center", va="bottom", fontsize=10.7)
    ax.set_xticks([])
    ax.set_ylabel("相對能量 / eV")
    ax.set_title("氫與單電子離子：能量只依 $n$", fontsize=13.5, weight="bold")
    for side in ("top", "right", "bottom"):
        ax.spines[side].set_visible(False)

    ax = axes[1]
    yvals = np.arange(len(order))
    for y, (n, ell, name) in zip(yvals, order):
        color = [F.BLUE, F.GREEN, F.AMBER, F.PURPLE][ell]
        ax.hlines(y, 0.8, 4.8, color=color, lw=2.3)
        ax.text(2.8, y + 0.11, f"{name}　$n+l={n+ell}$", ha="center", va="bottom", fontsize=10.3)
    ax.set_xlim(0, 5.6)
    ax.set_ylim(-0.7, len(order) - 0.15)
    ax.set_xticks([])
    ax.set_yticks([])
    F.arrow(ax, (5.15, 0), (5.15, len(order) - 0.8), color=F.RED, lw=2.0, mutation=12)
    ax.text(5.35, (len(order) - 1) / 2, "能量增加", rotation=90, va="center", fontsize=10.8, color=F.RED)
    ax.set_title("多電子原子：先比 $n+l$，同值再比 $n$", fontsize=13.5, weight="bold")
    for side in ("top", "right", "left", "bottom"):
        ax.spines[side].set_visible(False)
    fig.suptitle("電子間排斥使同一主量子數內的軌域分裂", fontsize=16, y=0.985)
    fig.subplots_adjust(left=0.07, right=0.97, top=0.82, bottom=0.08, wspace=0.18)
    return _save(fig, "選化II-1-單多電子能階順序.svg")


def fig_filling_rules():
    """用軌域方框與箭頭呈現遞建、包立與洪德原則。"""
    fig, axes = plt.subplots(1, 3, figsize=(12.0, 5.6))
    for ax in axes:
        ax.axis("off")
        ax.set_xlim(-0.2, 4.2)
        ax.set_ylim(-0.6, 4.6)

    ax = axes[0]
    levels = [(0.2, 0.2, "1s"), (1.1, 1.1, "2s"), (2.0, 2.0, "2p"), (2.9, 2.9, "3s")]
    for x, y, label in levels:
        _orbital_box(ax, x, y, (), label=label, face="#eef4ff")
    for (x0, y0, _), (x1, y1, _) in zip(levels[:-1], levels[1:]):
        F.arrow(ax, (x0 + 0.73, y0 + 0.55), (x1 - 0.05, y1 + 0.25), color=F.BLUE, lw=1.8, mutation=10)
    ax.text(2.0, 4.15, "遞建原則", ha="center", fontsize=13.5, weight="bold")
    ax.text(2.0, -0.35, "由低能量軌域開始填入", ha="center", fontsize=10.5)

    ax = axes[1]
    _orbital_box(ax, 1.70, 1.75, ("up", "down"), label="1s", face="#fff7dd")
    ax.text(2.06, 4.15, "包立不相容原理", ha="center", fontsize=13.5, weight="bold")
    ax.text(2.06, 0.65, "同一軌域最多兩電子\n自旋量子數相反", ha="center", fontsize=10.8)
    ax.text(2.06, -0.12, "$(n,l,m_l,m_s)$ 四數組不可完全相同", ha="center", fontsize=9.8, color=F.BLUE)

    ax = axes[2]
    for i in range(3):
        _orbital_box(ax, 0.55 + i * 1.05, 1.75, ("up",), label=f"$p_{'xyz'[i]}$", face="#ecfdf5")
    ax.text(2.0, 4.15, "洪德定則", ha="center", fontsize=13.5, weight="bold")
    ax.text(2.0, 0.65, "等能軌域先各放一電子\n且自旋方向平行", ha="center", fontsize=10.8)
    ax.text(2.0, -0.12, "$2p^3$：三個未成對電子", ha="center", fontsize=10.0, color=F.GREEN)
    fig.suptitle("基態電子組態由能量順序與量子狀態限制共同決定", fontsize=16, y=0.985)
    fig.subplots_adjust(left=0.02, right=0.985, top=0.82, bottom=0.06, wspace=0.08)
    return _save(fig, "選化II-1-電子填排三原則.svg")


def fig_periodic_blocks():
    """用簡化週期表連接最後填入次層與 s、p、d、f 區。"""
    fig, ax = plt.subplots(figsize=(12.0, 6.2))
    ax.axis("off")
    ax.set_xlim(-0.8, 19.2)
    ax.set_ylim(-3.3, 8.4)
    block_colors = {"s": "#bfdbfe", "p": "#fecaca", "d": "#fef3c7", "f": "#dcfce7"}
    # 主表：依週期與族畫出實際存在的區塊格。
    for period in range(1, 8):
        y = 7.2 - period
        s_cols = [0] if period == 1 else [0, 1]
        if period == 1:
            s_cols = [0]
        for col in s_cols:
            ax.add_patch(Rectangle((col, y), 0.86, 0.72, facecolor=block_colors["s"], edgecolor="white"))
        if period == 1:
            ax.add_patch(Rectangle((17, y), 0.86, 0.72, facecolor=block_colors["s"], edgecolor="white"))
        if period >= 4:
            for col in range(2, 12):
                ax.add_patch(Rectangle((col, y), 0.86, 0.72, facecolor=block_colors["d"], edgecolor="white"))
        if period >= 2:
            for col in range(12, 18):
                ax.add_patch(Rectangle((col, y), 0.86, 0.72, facecolor=block_colors["p"], edgecolor="white"))
        ax.text(-0.28, y + 0.36, str(period), ha="right", va="center", fontsize=9.5)
    for row, shell in enumerate((4, 5)):
        y = -1.25 - row * 0.95
        ax.text(1.5, y + 0.36, f"{shell}f 系", ha="right", va="center", fontsize=9.5)
        for col in range(14):
            ax.add_patch(Rectangle((2.0 + col, y), 0.86, 0.72, facecolor=block_colors["f"], edgecolor="white"))
    labels = [(0.85, 7.78, "s 區", F.BLUE), (7.0, 4.15, "d 區", F.AMBER), (14.8, 7.05, "p 區", F.RED), (8.2, -2.9, "f 區", F.GREEN)]
    for x, y, text, color in labels:
        ax.text(x, y, text, ha="center", fontsize=12.5, weight="bold", color=color)
    _box(ax, (1.0, -0.05), 4.1, 0.78, "週期＝最高被占用的 $n$", face="#eef4ff", edge=F.BLUE, fs=11.0)
    _box(ax, (6.2, -0.05), 5.2, 0.78, "主族價電子：$ns^a np^b$", face="#fff7dd", edge=F.AMBER, fs=11.0)
    _box(ax, (12.5, -0.05), 5.0, 0.78, "最後填入次層決定區塊", face="#ecfdf5", edge=F.GREEN, fs=11.0)
    assert 2 + 6 + 10 + 14 == 32
    fig.suptitle("週期表的形狀來自各次層可容納的電子數", fontsize=16, y=0.985)
    fig.subplots_adjust(left=0.03, right=0.985, top=0.88, bottom=0.03)
    return _save(fig, "選化II-1-電子組態與週期表區塊.svg")


def fig_ion_configurations():
    """以主族與過渡金屬展示成離子的電子增減順序。"""
    assert 26 - 2 == 24 and 26 - 3 == 23
    fig, axes = plt.subplots(2, 1, figsize=(11.8, 6.4))
    for ax in axes:
        ax.axis("off")
        ax.set_xlim(-0.2, 11.2)
        ax.set_ylim(-1.1, 2.5)
    ax = axes[0]
    boxes = [
        (0.2, "Na\n$[Ne]3s^1$", "失去 $3s$ 的 1 e$^-$", "Na$^+$\n$[Ne]$", F.BLUE),
        (5.8, "Cl\n$[Ne]3s^23p^5$", "得到 1 e$^-$", "Cl$^-$\n$[Ar]$", F.RED),
    ]
    for x, start, action, end, color in boxes:
        _box(ax, (x, 0.15), 2.0, 1.25, start, face="#f8fafc", edge=color, fs=11.5)
        F.arrow(ax, (x + 2.10, 0.78), (x + 3.15, 0.78), color=color, lw=2.0, mutation=12)
        ax.text(x + 2.62, 1.12, action, ha="center", fontsize=9.6, color=color)
        _box(ax, (x + 3.28, 0.15), 1.75, 1.25, end, face="#ecfdf5", edge=color, fs=11.5)
    ax.set_title("主族元素：增減價電子後接近惰性氣體組態", fontsize=13.5, weight="bold")

    ax = axes[1]
    _box(ax, (0.2, 0.15), 2.35, 1.25, "Fe\n$[Ar]4s^23d^6$", face="#f8fafc", edge=F.AMBER, fs=11.5)
    F.arrow(ax, (2.65, 0.78), (4.00, 0.78), color=F.AMBER, lw=2.0, mutation=12)
    ax.text(3.32, 1.20, "先移除最高 $n$ 的 $4s^2$", ha="center", fontsize=9.8, color=F.AMBER)
    _box(ax, (4.12, 0.15), 2.35, 1.25, "Fe$^{2+}$\n$[Ar]3d^6$", face="#fff7dd", edge=F.AMBER, fs=11.5)
    F.arrow(ax, (6.57, 0.78), (7.92, 0.78), color=F.RED, lw=2.0, mutation=12)
    ax.text(7.25, 1.20, "再移除一個 $3d$ 電子", ha="center", fontsize=9.8, color=F.RED)
    _box(ax, (8.04, 0.15), 2.35, 1.25, "Fe$^{3+}$\n$[Ar]3d^5$", face="#fdecec", edge=F.RED, fs=11.5)
    ax.set_title("過渡金屬：成陽離子時先移除最高主量子數電子", fontsize=13.5, weight="bold")
    fig.suptitle("離子的電子組態用電子總數與移除順序共同核對", fontsize=16, y=0.985)
    fig.subplots_adjust(left=0.03, right=0.985, top=0.86, bottom=0.04, hspace=0.38)
    return _save(fig, "選化II-1-原子到離子的電子帳.svg")


def fig_radius():
    """展示原子半徑趨勢與十電子等電子序列。"""
    species = ["O$^{2-}$", "F$^-$", "Ne", "Na$^+$", "Mg$^{2+}$"]
    z = np.array([8, 9, 10, 11, 12])
    radii = np.array([140, 133, 112, 102, 72])
    assert np.all(np.diff(z) == 1)
    assert np.all(np.diff(radii) < 0)
    assert np.all(np.array([10, 10, 10, 10, 10]) == 10)

    fig, axes = plt.subplots(1, 2, figsize=(12.0, 5.9))
    ax = axes[0]
    ax.axis("off")
    ax.set_xlim(-0.5, 8.2)
    ax.set_ylim(-0.5, 6.5)
    for row in range(4):
        for col in range(7):
            ax.add_patch(Rectangle((0.4 + col, 0.6 + row), 0.82, 0.72, facecolor="#e2e8f0", edgecolor="white"))
    F.arrow(ax, (0.7, 5.35), (7.4, 5.35), color=F.RED, lw=2.4, mutation=14)
    ax.text(4.05, 5.70, "同週期：有效核電荷增加，半徑減小", ha="center", fontsize=11.2, color=F.RED)
    F.arrow(ax, (0.05, 4.25), (0.05, 0.72), color=F.BLUE, lw=2.4, mutation=14)
    ax.text(-0.25, 2.45, "電子層增加\n半徑增大", ha="center", va="center", fontsize=10.5, color=F.BLUE, rotation=90)
    _box(ax, (1.45, -0.20), 5.9, 0.58, "同一元素：陽離子 < 原子 < 陰離子", face="#fff7dd", edge=F.AMBER, fs=11.5)
    ax.set_title("原子半徑的兩個競爭因素", fontsize=13.5, weight="bold")

    ax = axes[1]
    x_positions = np.arange(len(species))
    scale = 0.0072
    colors = ["#7dd3fc", "#93c5fd", "#cbd5e1", "#fbbf24", "#fb923c"]
    for x, sp, zi, radius, color in zip(x_positions, species, z, radii, colors):
        ax.add_patch(Circle((x, 1.55), radius * scale, facecolor=color, edgecolor=F.INK, lw=1.2, alpha=0.82))
        ax.text(x, 0.15, f"{sp}\n$Z={zi}$\n{radius} pm", ha="center", va="top", fontsize=9.8)
    F.arrow(ax, (0.0, 3.05), (4.0, 3.05), color=F.RED, lw=2.2, mutation=13)
    ax.text(2.0, 3.35, "皆有 10 電子；核電荷增加，半徑依序減小", ha="center", fontsize=10.8, color=F.RED)
    ax.set_xlim(-0.9, 4.9)
    ax.set_ylim(-0.7, 3.8)
    ax.axis("off")
    ax.set_title("等電子序列只需比較核電荷", fontsize=13.5, weight="bold")
    fig.suptitle("半徑取決於電子層數、遮蔽與電子受到的有效核吸引", fontsize=16, y=0.985)
    fig.subplots_adjust(left=0.035, right=0.985, top=0.82, bottom=0.05, wspace=0.15)
    return _save(fig, "選化II-1-原子與等電子離子半徑.svg")


def fig_successive_ie():
    """用 Mg、Al 逐次游離能的實際型態定位價電子數。"""
    mg = np.array([738, 1451, 7733, 10543, 13630], dtype=float)
    al = np.array([578, 1817, 2745, 11577, 14842], dtype=float)
    assert np.argmax(mg[1:] / mg[:-1]) + 1 == 2
    assert np.argmax(al[1:] / al[:-1]) + 1 == 3
    x = np.arange(1, 6)
    fig, axes = plt.subplots(1, 2, figsize=(11.8, 5.6))
    for ax, values, name, jump, color in [(axes[0], mg, "Mg：$[Ne]3s^2$", 2, F.BLUE), (axes[1], al, "Al：$[Ne]3s^23p^1$", 3, F.RED)]:
        ax.plot(x, values, "o-", color=color, lw=2.4, ms=6)
        for xi, yi in zip(x, values):
            ax.text(xi, yi + 360, f"{int(yi)}", ha="center", fontsize=8.8)
        ax.axvspan(jump + 0.5, jump + 1.5, color="#fde68a", alpha=0.45)
        ax.annotate(f"移除 {jump} 個價電子後\n下一次跨入內層", (jump + 1, values[jump]), xytext=(1.15, 11200), arrowprops={"arrowstyle": "->", "color": F.AMBER}, fontsize=10.2, color=F.AMBER)
        ax.set_xticks(x)
        ax.set_xlabel("依序移除的第 $k$ 個電子")
        ax.set_ylim(0, 16500)
        F.clean_grid(ax)
        ax.set_title(name, fontsize=13.5, weight="bold")
    axes[0].set_ylabel("第 $k$ 游離能 / $\\mathrm{kJ\\,mol^{-1}}$")
    fig.suptitle("逐次游離能的最大躍升定位外層價電子數", fontsize=16, y=0.985)
    fig.subplots_adjust(left=0.08, right=0.98, top=0.82, bottom=0.13, wspace=0.20)
    return _save(fig, "選化II-1-逐次游離能躍升.svg")


def fig_first_ie():
    """用第二週期數據顯示總趨勢與 Be/B、N/O 局部例外。"""
    elements = ["Li", "Be", "B", "C", "N", "O", "F", "Ne"]
    values = np.array([520, 900, 801, 1086, 1402, 1314, 1681, 2081], dtype=float)
    assert values[1] > values[2]
    assert values[4] > values[5]
    fig, ax = plt.subplots(figsize=(11.3, 5.7))
    x = np.arange(len(elements))
    ax.plot(x, values, "o-", color=F.BLUE, lw=2.5, ms=7)
    for xi, element, value in zip(x, elements, values):
        ax.text(xi, value + 75, f"{element}\n{int(value)}", ha="center", fontsize=9.5)
    ax.annotate("Be 的 $2s$ 已填滿", (1, values[1]), xytext=(0.35, 1330), arrowprops={"arrowstyle": "->", "color": F.AMBER}, fontsize=10.2, color=F.AMBER)
    ax.annotate("N 的 $2p^3$ 半滿；O 開始成對", (4.6, 1355), xytext=(3.55, 785), arrowprops={"arrowstyle": "->", "color": F.RED}, fontsize=10.2, color=F.RED)
    ax.set_xticks(x, elements)
    ax.set_ylabel("第一游離能 / $\\mathrm{kJ\\,mol^{-1}}$")
    ax.set_xlabel("第二週期元素")
    ax.set_ylim(350, 2250)
    F.clean_grid(ax)
    ax.set_title("核吸引造成整體上升，次層能量與電子成對造成鋸齒", fontsize=13.8, weight="bold")
    fig.suptitle("第一游離能的週期趨勢需同時讀整體與局部電子組態", fontsize=16, y=0.985)
    fig.subplots_adjust(left=0.09, right=0.985, top=0.82, bottom=0.13)
    return _save(fig, "選化II-1-第一游離能週期趨勢.svg")


def fig_electronegativity():
    """把電負度週期趨勢與鍵內電子偏移方向連起來。"""
    en = {"H": 2.20, "C": 2.55, "O": 3.44, "F": 3.98, "Na": 0.93, "Cl": 3.16}
    assert en["F"] == max(en.values())
    assert np.isclose(en["Cl"] - en["H"], 0.96)
    fig, axes = plt.subplots(1, 2, figsize=(11.8, 5.8))
    ax = axes[0]
    ax.axis("off")
    ax.set_xlim(-0.5, 8.0)
    ax.set_ylim(-0.5, 6.3)
    for row in range(4):
        for col in range(7):
            color = plt.cm.YlOrRd(0.18 + 0.65 * (col / 6) * (1 - 0.12 * row))
            ax.add_patch(Rectangle((0.35 + col, 0.65 + row), 0.82, 0.72, facecolor=color, edgecolor="white"))
    F.arrow(ax, (0.55, 5.30), (7.15, 5.30), color=F.RED, lw=2.3, mutation=13)
    F.arrow(ax, (0.05, 0.85), (0.05, 4.35), color=F.RED, lw=2.3, mutation=13)
    ax.text(3.85, 5.65, "吸引鍵結電子的能力增加", ha="center", fontsize=11.0, color=F.RED)
    ax.text(7.25, 4.10, "F 最高", ha="center", fontsize=10.5, color=F.RED, weight="bold")
    _box(ax, (1.05, -0.15), 5.95, 0.56, "電負度描述成鍵原子對共享電子的相對吸引力", face="#fff7dd", edge=F.AMBER, fs=10.8)
    ax.set_title("週期表上的電負度趨勢", fontsize=13.5, weight="bold")

    ax = axes[1]
    ax.axis("off")
    ax.set_xlim(-0.5, 8.0)
    ax.set_ylim(-0.5, 6.3)
    bonds = [("H", "Cl", 4.75, F.BLUE), ("C", "O", 2.85, F.GREEN), ("H", "F", 0.95, F.RED)]
    for left, right, y, color in bonds:
        x1, x2 = 1.45, 6.05
        ax.add_patch(Circle((x1, y), 0.55, facecolor="#e2e8f0", edgecolor=F.INK, lw=1.4))
        ax.add_patch(Circle((x2, y), 0.55, facecolor="#fecaca", edgecolor=F.INK, lw=1.4))
        ax.text(x1, y, left, ha="center", va="center", fontsize=13, weight="bold")
        ax.text(x2, y, right, ha="center", va="center", fontsize=13, weight="bold")
        ax.plot([x1 + 0.55, x2 - 0.55], [y, y], color=F.INK, lw=2.2)
        F.arrow(ax, (3.0, y + 0.28), (5.15, y + 0.28), color=color, lw=2.0, mutation=12)
        ax.text(3.75, y - 0.63, f"$\\Delta EN={abs(en[right]-en[left]):.2f}$", ha="center", fontsize=10.0, color=color)
        ax.text(x1, y + 0.82, "$\\delta^+$", ha="center", fontsize=10.8)
        ax.text(x2, y + 0.82, "$\\delta^-$", ha="center", fontsize=10.8)
    ax.text(3.75, 5.85, "鍵電子偏向電負度較大的原子", ha="center", fontsize=11.5, weight="bold")
    ax.set_title("鍵極性由兩端電負度差決定", fontsize=13.5, weight="bold")
    fig.suptitle("電負度把電子組態的週期性連到化學鍵中的電荷分布", fontsize=16, y=0.985)
    fig.subplots_adjust(left=0.03, right=0.985, top=0.82, bottom=0.04, wspace=0.15)
    return _save(fig, "選化II-1-電負度與鍵極性.svg")


def fig_flame_spectroscopy():
    """以受控焰色觀察與線光譜把觀察、模型、鑑別連起來。"""
    lines = {
        "Li": [610.4, 670.8],
        "Na": [589.0, 589.6],
        "K": [404.4, 766.5],
        "Cu": [510.5, 515.3, 521.8],
    }
    assert all(380 < wavelength < 780 for seq in lines.values() for wavelength in seq)
    fig, axes = plt.subplots(1, 2, figsize=(12.0, 6.0), gridspec_kw={"width_ratios": [0.92, 1.28]})
    ax = axes[0]
    ax.axis("off")
    ax.set_xlim(-2.8, 2.8)
    ax.set_ylim(-3.0, 3.0)
    ax.add_patch(Rectangle((-0.75, -2.10), 1.50, 1.05, facecolor="#cbd5e1", edgecolor=F.INK, lw=1.5))
    ax.add_patch(Polygon([(-0.55, -1.05), (0.00, 1.55), (0.55, -1.05)], closed=True, facecolor="#60a5fa", edgecolor=F.BLUE, alpha=0.72))
    ax.add_patch(Polygon([(-0.28, -1.05), (0.00, 0.95), (0.28, -1.05)], closed=True, facecolor="#fde68a", edgecolor=F.AMBER, alpha=0.82))
    ax.plot([-1.75, 0.02], [1.45, 0.62], color=F.INK, lw=2.0)
    ax.add_patch(Circle((-1.77, 1.46), 0.17, facecolor="#22c55e", edgecolor=F.INK, lw=1.0))
    ax.text(-1.70, 2.05, "少量樣品進入火焰", ha="center", fontsize=10.8)
    xs = np.linspace(0.2, 2.25, 160)
    ax.plot(xs, 1.55 + 0.12 * np.sin(12 * xs), color=F.PURPLE, lw=2.0)
    F.arrow(ax, (2.05, 1.55), (2.42, 1.55), color=F.PURPLE, lw=1.6, mutation=10)
    ax.text(1.35, 2.15, "受激原子回到較低能階\n放出特定波長", ha="center", fontsize=10.8, color=F.PURPLE)
    _box(ax, (-2.45, -2.78), 4.90, 0.48, "護目鏡、通風、遠離可燃物；金屬鹽廢液分類回收", face="#fdecec", edge=F.RED, fs=9.7)
    ax.set_title("受控焰色觀察的能量流程", fontsize=13.5, weight="bold")

    ax = axes[1]
    ax.set_xlim(380, 780)
    ax.set_ylim(-0.15, 4.65)
    row_colors = {"Li": "#dc2626", "Na": "#eab308", "K": "#7c3aed", "Cu": "#16a34a"}
    for row, (element, wavelengths) in enumerate(lines.items()):
        y = 3.75 - row
        ax.add_patch(Rectangle((380, y - 0.28), 400, 0.56, facecolor="#111827", edgecolor="#111827"))
        for wavelength in wavelengths:
            ax.plot([wavelength, wavelength], [y - 0.28, y + 0.28], color=row_colors[element], lw=5)
        ax.text(368, y, element, ha="right", va="center", fontsize=11.5, weight="bold")
    ax.set_xlabel("波長 / nm")
    ax.set_yticks([])
    ax.text(580, 4.40, "顏色是初步觀察；譜線位置提供較可靠的元素指紋", ha="center", fontsize=11.0, weight="bold")
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.set_title("以譜線位置比對未知樣品", fontsize=13.5, weight="bold")
    fig.suptitle("焰色與放射光譜把電子躍遷轉成元素鑑別資料", fontsize=16, y=0.985)
    fig.subplots_adjust(left=0.055, right=0.985, top=0.82, bottom=0.11, wspace=0.17)
    return _save(fig, "選化II-1-焰色與光譜鑑別.svg")


def main():
    for function_name, filename in FIGURE_OUTPUTS:
        function = globals()[function_name]
        output = function()
        assert os.path.basename(output) == filename


if __name__ == "__main__":
    main()
