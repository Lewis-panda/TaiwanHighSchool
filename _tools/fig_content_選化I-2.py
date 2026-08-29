# -*- coding: utf-8 -*-
"""產生「選化 I-2 氣體」學生講義章內 SVG。

重繪：.venv/bin/python _tools/fig_content_選化I-2.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, FancyBboxPatch, Rectangle, Polygon

import figlib as F


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CH = os.path.join(ROOT, "content", "選修化學I", "選化I-2")


FIGURE_OUTPUTS = (
    ("fig_particle_pressure", "選化I-2-粒子碰撞與氣壓.svg"),
    ("fig_manometers", "選化I-2-開閉口壓力計.svg"),
    ("fig_boyle", "選化I-2-波以耳裝置與圖形.svg"),
    ("fig_charles", "選化I-2-查理定律與絕對零度.svg"),
    ("fig_avogadro", "選化I-2-亞佛加厥粒子模型.svg"),
    ("fig_ideal_state", "選化I-2-理想氣體狀態帳.svg"),
    ("fig_real_gas", "選化I-2-真實氣體壓縮因子.svg"),
    ("fig_density", "選化I-2-氣體密度與莫耳質量.svg"),
    ("fig_dalton", "選化I-2-分壓的粒子帳.svg"),
    ("fig_connected_vessels", "選化I-2-連通容器混合.svg"),
    ("fig_water_collection", "選化I-2-排水集氣壓力修正.svg"),
    ("fig_gas_experiment", "選化I-2-二氧化碳集氣實驗.svg"),
)


def _save(fig, filename):
    assert filename.endswith(".svg")
    return F.save_to(fig, CH, filename[:-4], output_subdir="assets", write_pdf=False)


def _box(ax, xy, width, height, text, *, face="#f8fafc", edge="#64748b", fs=11.0, lw=1.6):
    patch = FancyBboxPatch(
        xy,
        width,
        height,
        boxstyle="round,pad=0.035,rounding_size=0.09",
        facecolor=face,
        edgecolor=edge,
        lw=lw,
    )
    ax.add_patch(patch)
    ax.text(xy[0] + width / 2, xy[1] + height / 2, text, ha="center", va="center", fontsize=fs)
    return patch


def _particle(ax, x, y, color=F.BLUE, label=""):
    ax.add_patch(Circle((x, y), 0.12, facecolor=color, edgecolor="white", lw=0.7, zorder=4))
    if label:
        ax.text(x, y, label, ha="center", va="center", fontsize=6.7, color="white", weight="bold", zorder=5)


def _container(ax, x, y, w, h, *, face="#f8fafc", edge=F.INK, lw=1.7):
    ax.add_patch(Rectangle((x, y), w, h, facecolor=face, edgecolor=edge, lw=lw))


def fig_particle_pressure():
    """以同數粒子在不同體積中的撞壁頻率建立壓力模型。"""
    n_particles = 12
    large_area, small_area = 16.0, 8.0
    density_ratio = (n_particles / small_area) / (n_particles / large_area)
    assert np.isclose(density_ratio, 2.0)

    fig, axes = plt.subplots(1, 3, figsize=(12.0, 5.7), gridspec_kw={"width_ratios": [1, 1, 0.95]})
    configs = [
        (axes[0], (-2.1, -1.7, 4.2, 3.4), "較大體積", 1.0),
        (axes[1], (-1.05, -1.7, 2.1, 3.4), "壓縮至一半", 2.0),
    ]
    base = np.array([
        [-0.78, 0.70], [-0.38, 0.42], [0.03, 0.73], [0.57, 0.41],
        [-0.70, 0.12], [-0.19, 0.05], [0.36, 0.11], [0.76, -0.08],
        [-0.64, -0.47], [-0.18, -0.62], [0.29, -0.46], [0.67, -0.70],
    ])
    for ax, (x, y, w, h), title, scale in configs:
        ax.axis("off")
        ax.set_xlim(-2.8, 2.8)
        ax.set_ylim(-2.6, 2.6)
        _container(ax, x, y, w, h)
        for px, py in base:
            _particle(ax, px * w * 0.43, py * h * 0.44)
        for yy in (-1.10, -0.30, 0.55, 1.16):
            start = (x + w * 0.72, yy)
            F.arrow(ax, start, (x + w - 0.08, yy + 0.12), color=F.RED, lw=1.5, mutation=10)
        ax.text(0, 2.02, title, ha="center", fontsize=14, weight="bold")
        ax.text(0, -2.08, f"同為 {n_particles} 個粒子\n相對撞壁頻率約 ×{scale:.0f}", ha="center", fontsize=11.3)

    ax = axes[2]
    ax.axis("off")
    ax.set_xlim(-3, 3)
    ax.set_ylim(-3, 3)
    _box(ax, (-2.55, 1.45), 5.1, 0.92, "粒子撞牆時改變動量\n牆受到反作用力", face="#eef4ff", edge=F.BLUE, fs=11.5)
    F.arrow(ax, (0, 1.38), (0, 0.65), color=F.INK, lw=2.0, mutation=13)
    _box(ax, (-2.55, -0.18), 5.1, 0.92, "單位面積、單位時間內\n動量傳遞量決定壓力", face="#fff7dd", edge=F.AMBER, fs=11.5)
    F.arrow(ax, (0, -0.25), (0, -0.98), color=F.INK, lw=2.0, mutation=13)
    _box(ax, (-2.55, -1.80), 5.1, 0.92, "定溫、定量壓縮\n撞壁更頻繁，壓力上升", face="#fdecec", edge=F.RED, fs=11.5)
    ax.text(0, -2.45, "壓力是大量碰撞的平均效果", ha="center", fontsize=10.8, color="#475569")
    fig.suptitle("氣體壓力來自粒子對器壁的動量傳遞", fontsize=16, y=0.985)
    fig.subplots_adjust(left=0.02, right=0.98, top=0.84, bottom=0.05, wspace=0.08)
    return _save(fig, "選化I-2-粒子碰撞與氣壓.svg")


def fig_manometers():
    """以三個液面狀態顯示開口、閉口壓力計的判讀。"""
    patm = 760.0
    dh_open = 120.0
    p_high = patm + dh_open
    p_low = patm - dh_open
    p_closed = 380.0
    assert (p_high, p_low, p_closed) == (880.0, 640.0, 380.0)

    fig, axes = plt.subplots(1, 3, figsize=(12.0, 5.8))
    panels = [
        ("開口式：氣體端較低", 0.65, 1.35, "$P_g=P_{atm}+120=880\\ mmHg$", F.RED),
        ("開口式：氣體端較高", 1.35, 0.65, "$P_g=P_{atm}-120=640\\ mmHg$", F.BLUE),
        ("閉口式：上端近真空", 0.55, 1.45, "$P_g=380\\ mmHg$", F.GREEN),
    ]
    for i, (ax, (title, left_level, right_level, equation, color)) in enumerate(zip(axes, panels)):
        ax.axis("off")
        ax.set_xlim(-2.5, 2.5)
        ax.set_ylim(-2.7, 2.7)
        ax.plot([-1.10, -1.10, -1.10, 1.10, 1.10, 1.10], [1.95, -1.45, -1.80, -1.80, -1.45, 1.95], color=F.INK, lw=5, solid_capstyle="round")
        ax.plot([-1.10, -1.10, -1.10, 1.10, 1.10, 1.10], [left_level, -1.45, -1.62, -1.62, -1.45, right_level], color="#94a3b8", lw=3, solid_capstyle="butt")
        ax.fill_between([-1.25, -0.95], [-1.45, -1.45], [left_level, left_level], color="#cbd5e1")
        ax.fill_between([0.95, 1.25], [-1.45, -1.45], [right_level, right_level], color="#cbd5e1")
        ax.text(-1.56, left_level, "氣體", ha="right", va="center", fontsize=10.8, color=color, weight="bold")
        if i < 2:
            ax.text(1.43, 2.00, "大氣", ha="left", va="center", fontsize=10.8)
        else:
            ax.add_patch(Rectangle((0.91, 1.78), 0.38, 0.22, facecolor=F.INK, edgecolor=F.INK))
            ax.text(1.42, 2.02, "封閉、近真空", ha="left", va="center", fontsize=9.8)
        xdim = 1.72
        ax.plot([xdim, xdim], [left_level, right_level], color=color, lw=1.6)
        ax.plot([xdim - 0.13, xdim + 0.13], [left_level, left_level], color=color, lw=1.6)
        ax.plot([xdim - 0.13, xdim + 0.13], [right_level, right_level], color=color, lw=1.6)
        ax.text(1.94, (left_level + right_level) / 2, "$h$", ha="left", va="center", fontsize=12, color=color)
        ax.text(0, -2.08, equation, ha="center", fontsize=11.2, color=color, weight="bold")
        ax.set_title(title, fontsize=13.2, weight="bold")
    fig.suptitle("同一液體、同一水平面壓力相等；液面較低的一側壓力較大", fontsize=16, y=0.985)
    fig.subplots_adjust(left=0.02, right=0.98, top=0.83, bottom=0.05, wspace=0.07)
    return _save(fig, "選化I-2-開閉口壓力計.svg")


def fig_boyle():
    """從活塞壓縮連到 P–V 與 V–1/P 的數值圖。"""
    k = 6.0
    p = np.linspace(0.75, 3.0, 160)
    v = k / p
    assert np.allclose(p * v, k)
    marked_p = np.array([1.0, 2.0, 3.0])
    marked_v = k / marked_p
    assert np.allclose(marked_v, [6.0, 3.0, 2.0])

    fig, axes = plt.subplots(1, 3, figsize=(12.0, 5.8), gridspec_kw={"width_ratios": [0.9, 1.05, 1.05]})
    ax = axes[0]
    ax.axis("off")
    ax.set_xlim(-2.4, 2.4)
    ax.set_ylim(-2.8, 2.8)
    for x, piston_y, label, color in [(-1.25, 1.65, "$P=1\\ atm$\n$V=6\\ L$", F.BLUE), (1.25, 0.15, "$P=2\\ atm$\n$V=3\\ L$", F.RED)]:
        _container(ax, x - 0.62, -1.70, 1.24, 3.5)
        ax.add_patch(Rectangle((x - 0.62, piston_y), 1.24, 0.16, facecolor=color, edgecolor=F.INK, lw=1.2))
        ax.plot([x, x], [piston_y + 0.16, 2.25], color=F.INK, lw=2)
        for yy in np.linspace(-1.25, piston_y - 0.35, 6):
            _particle(ax, x + 0.26 * np.sin(6 * yy), yy, color=color)
        ax.text(x, -2.20, label, ha="center", fontsize=11.1, color=color, weight="bold")
    F.arrow(ax, (-0.12, 1.65), (0.65, 1.12), color=F.INK, lw=2.1, mutation=14)
    ax.set_title("定溫、定量壓縮", fontsize=13.5, weight="bold")

    ax = axes[1]
    ax.plot(v, p, color=F.BLUE, lw=2.4)
    ax.scatter(marked_v, marked_p, color=F.RED, zorder=4)
    for pi, vi in zip(marked_p, marked_v):
        ax.annotate(f"({vi:g}, {pi:g})", (vi, pi), xytext=(5, 7), textcoords="offset points", fontsize=9.5)
    ax.set_xlabel("$V$/L")
    ax.set_ylabel("$P$/atm")
    ax.set_xlim(0, 8.5)
    ax.set_ylim(0, 3.4)
    F.clean_grid(ax)
    ax.set_title("$P=k/V$：雙曲線", fontsize=13.5, weight="bold")

    ax = axes[2]
    inv_p = 1 / p
    ax.plot(inv_p, v, color=F.GREEN, lw=2.4)
    ax.scatter(1 / marked_p, marked_v, color=F.RED, zorder=4)
    ax.set_xlabel("$1/P$ / $\\mathrm{atm^{-1}}$")
    ax.set_ylabel("$V$/L")
    ax.set_xlim(0, 1.15)
    ax.set_ylim(0, 8.5)
    F.clean_grid(ax)
    ax.set_title("$V=k(1/P)$：過原點直線", fontsize=13.5, weight="bold")
    fig.suptitle("波以耳定律：溫度與莫耳數固定時，$PV$ 為常數", fontsize=16, y=0.985)
    fig.subplots_adjust(left=0.045, right=0.985, top=0.82, bottom=0.14, wspace=0.28)
    return _save(fig, "選化I-2-波以耳裝置與圖形.svg")


def fig_charles():
    """以攝氏與絕對溫度雙軸解釋查理定律與外插。"""
    celsius = np.array([-100.0, 0.0, 100.0, 200.0])
    kelvin = celsius + 273.15
    slope = 1.20 / 273.15
    volume = slope * kelvin
    assert np.isclose(volume[1], 1.20)
    assert np.isclose(-volume[1] / slope, -273.15)

    fig, axes = plt.subplots(1, 2, figsize=(11.8, 5.9))
    ax = axes[0]
    ax.plot(celsius, volume, color=F.BLUE, lw=2.4)
    ax.plot([-273.15, -100], [0, volume[0]], color=F.BLUE, lw=1.8, ls="--")
    ax.scatter(celsius, volume, color=F.RED, zorder=4)
    ax.scatter([-273.15], [0], color=F.PURPLE, zorder=5)
    ax.annotate("外插：$-273.15^\\circ C$", (-273.15, 0), xytext=(-210, 0.45), arrowprops={"arrowstyle": "->", "color": F.PURPLE}, fontsize=10.5, color=F.PURPLE)
    ax.set_xlabel("攝氏溫度 $t/{}^\\circ C$")
    ax.set_ylabel("$V$/L")
    ax.set_xlim(-300, 230)
    ax.set_ylim(0, 2.3)
    F.clean_grid(ax)
    ax.set_title("攝氏軸：直線外插到零體積", fontsize=13.5, weight="bold")

    ax = axes[1]
    t = np.linspace(0, 500, 100)
    ax.plot(t, slope * t, color=F.GREEN, lw=2.4)
    ax.scatter(kelvin, volume, color=F.RED, zorder=4)
    ax.set_xlabel("絕對溫度 $T$/K")
    ax.set_ylabel("$V$/L")
    ax.set_xlim(0, 520)
    ax.set_ylim(0, 2.3)
    F.clean_grid(ax)
    _box(ax, (55, 1.55), 400, 0.44, "$V/T=1.20/273.15=4.39\\times10^{-3}\\ L\\,K^{-1}$", face="#eef4ff", edge=F.GREEN, fs=11.0)
    ax.set_title("絕對溫度軸：比例直線過原點", fontsize=13.5, weight="bold")
    fig.suptitle("查理定律：壓力與莫耳數固定時，體積與絕對溫度成正比", fontsize=16, y=0.985)
    fig.subplots_adjust(left=0.07, right=0.975, top=0.82, bottom=0.13, wspace=0.23)
    return _save(fig, "選化I-2-查理定律與絕對零度.svg")


def fig_avogadro():
    """用相同粒子密度展示同溫同壓下 V 與 n 的比例。"""
    counts = [6, 12, 18]
    volumes = [1.0, 2.0, 3.0]
    ratios = [n / v for n, v in zip(counts, volumes)]
    assert ratios == [6.0, 6.0, 6.0]

    fig, axes = plt.subplots(1, 3, figsize=(12.0, 5.6))
    for ax, n, v, color in zip(axes, counts, volumes, [F.BLUE, F.GREEN, F.PURPLE]):
        ax.axis("off")
        ax.set_xlim(-2.8, 2.8)
        ax.set_ylim(-2.7, 2.7)
        h = 1.25 * v
        _container(ax, -1.65, -1.75, 3.3, h)
        cols = 3
        rows = int(np.ceil(n / cols))
        ys = np.linspace(-1.40, -1.75 + h - 0.35, rows)
        xs = [-0.85, 0, 0.85]
        for j in range(n):
            _particle(ax, xs[j % cols], ys[j // cols], color=color)
        ax.text(0, 2.30, f"$n={v:.0f}n_0$，$V={v:.0f}V_0$", ha="center", fontsize=12.2, color=color, weight="bold")
        ax.text(0, -2.20, f"粒子數 {n}；$n/V=6$", ha="center", fontsize=11.0)
    fig.suptitle("亞佛加厥定律：同溫同壓下，等比例增加粒子數與容器體積", fontsize=16, y=0.985)
    fig.subplots_adjust(left=0.03, right=0.97, top=0.82, bottom=0.05, wspace=0.08)
    return _save(fig, "選化I-2-亞佛加厥粒子模型.svg")


def fig_ideal_state():
    """用兩個狀態卡與四個變數的因果關係建立理想氣體方程。"""
    r = 0.082057
    n1, t1, v1 = 1.00, 300.0, 24.6171
    p1 = n1 * r * t1 / v1
    n2, t2, v2 = 1.50, 400.0, 20.0
    p2 = n2 * r * t2 / v2
    assert np.isclose(p1, 1.0, atol=1e-4)
    assert np.isclose(p2, 2.46171, atol=1e-5)
    assert np.isclose(p1 * v1 / (n1 * t1), p2 * v2 / (n2 * t2), r)

    fig, ax = plt.subplots(figsize=(11.8, 6.1))
    ax.axis("off")
    ax.set_xlim(-6, 6)
    ax.set_ylim(-3.2, 3.2)
    _box(ax, (-5.45, 0.65), 4.35, 1.70, "$P_1=1.000\\ atm$\n$V_1=24.617\\ L$\n$n_1=1.000\\ mol$，$T_1=300.0\\ K$", face="#eef4ff", edge=F.BLUE, fs=11.8)
    _box(ax, (1.10, 0.65), 4.35, 1.70, "$P_2=2.462\\ atm$\n$V_2=20.00\\ L$\n$n_2=1.500\\ mol$，$T_2=400.0\\ K$", face="#fdecec", edge=F.RED, fs=11.8)
    F.arrow(ax, (-0.85, 1.50), (0.85, 1.50), color=F.INK, lw=2.3, mutation=15)
    ax.text(0, 2.00, "改變量、溫度與體積", ha="center", fontsize=11.3, weight="bold")
    _box(ax, (-4.95, -1.80), 9.90, 1.18, "$PV=nRT$　⇔　$P=\\dfrac{nRT}{V}$\n$P$ 隨 $n$、$T$ 增加而增大，隨 $V$ 增加而減小", face="#fff7dd", edge=F.AMBER, fs=13.0)
    ax.text(0, -2.40, "$R=0.082057\\ L\\,atm\\,mol^{-1}\\,K^{-1}$；單位組必須成套", ha="center", fontsize=11.5, color=F.PURPLE, weight="bold")
    fig.suptitle("理想氣體狀態帳把壓力、體積、莫耳數與絕對溫度放在同一式中", fontsize=16, y=0.985)
    fig.subplots_adjust(left=0.025, right=0.975, top=0.85, bottom=0.04)
    return _save(fig, "選化I-2-理想氣體狀態帳.svg")


def fig_real_gas():
    """以原創函數呈現吸引作用與排除體積造成的 Z 偏差。"""
    p = np.linspace(0.0, 120.0, 241)
    z_high_t = 1.0 - 0.06 * (p / 35.0) * np.exp(-p / 35.0) + 0.0007 * p
    z_mid_t = 1.0 - 0.23 * (p / 28.0) * np.exp(-p / 28.0) + 0.0010 * p
    z_low_t = 1.0 - 0.42 * (p / 23.0) * np.exp(-p / 23.0) + 0.0013 * p
    for z in (z_high_t, z_mid_t, z_low_t):
        assert np.isclose(z[0], 1.0)
        assert np.all(z > 0.5)
    assert np.min(z_low_t) < np.min(z_mid_t) < np.min(z_high_t)
    assert z_low_t[-1] > 1.0

    fig, ax = plt.subplots(figsize=(10.8, 6.2))
    ax.axhline(1.0, color=F.INK, lw=1.7, ls="--", label="理想氣體 $Z=1$")
    ax.plot(p, z_high_t, color=F.RED, lw=2.2, label="高溫")
    ax.plot(p, z_mid_t, color=F.BLUE, lw=2.2, label="中溫")
    ax.plot(p, z_low_t, color=F.PURPLE, lw=2.2, label="低溫")
    ax.fill_between(p, z_low_t, 1.0, where=z_low_t < 1, color=F.BLUE, alpha=0.08)
    ax.fill_between(p, z_low_t, 1.0, where=z_low_t > 1, color=F.RED, alpha=0.08)
    ax.annotate("吸引作用較明顯\n$Z<1$", xy=(28, z_low_t[np.searchsorted(p, 28)]), xytext=(8, 0.69), arrowprops={"arrowstyle": "->", "color": F.BLUE}, color=F.BLUE, fontsize=10.8)
    ax.annotate("高壓下排除體積較明顯\n$Z>1$", xy=(108, z_low_t[np.searchsorted(p, 108)]), xytext=(73, 1.12), arrowprops={"arrowstyle": "->", "color": F.RED}, color=F.RED, fontsize=10.8)
    ax.set_xlabel("壓力（相對尺度）")
    ax.set_ylabel("壓縮因子 $Z=PV/(nRT)$")
    ax.set_xlim(0, 120)
    ax.set_ylim(0.60, 1.25)
    F.clean_grid(ax)
    ax.legend(frameon=False, ncol=2, loc="lower right")
    ax.set_title("曲線為定性模型；用來判讀方向，不代替特定氣體量測表", fontsize=11.2, color="#475569")
    fig.suptitle("真實氣體的粒子有體積且彼此作用；高溫、低壓時通常較接近理想模型", fontsize=16, y=0.985)
    fig.subplots_adjust(left=0.09, right=0.975, top=0.84, bottom=0.13)
    return _save(fig, "選化I-2-真實氣體壓縮因子.svg")


def fig_density():
    """同溫同壓等體積容器以質量差連到莫耳質量。"""
    p, v, r, t = 1.0, 10.0, 0.082057, 300.0
    n = p * v / (r * t)
    m_he = n * 4.00
    m_co2 = n * 44.0
    d_he, d_co2 = m_he / v, m_co2 / v
    assert np.isclose(m_co2 / m_he, 11.0)
    assert np.isclose(d_co2 / d_he, 11.0)

    fig, axes = plt.subplots(1, 2, figsize=(11.8, 5.8))
    for ax, name, mass, density, color in [
        (axes[0], "$He$", m_he, d_he, F.BLUE),
        (axes[1], "$CO_2$", m_co2, d_co2, F.RED),
    ]:
        ax.axis("off")
        ax.set_xlim(-3, 3)
        ax.set_ylim(-3, 3)
        _container(ax, -1.75, -0.95, 3.5, 2.6, face="#f8fafc", edge=color, lw=2)
        for x, y in [(-1.05, 0.95), (0, 1.05), (1.05, 0.92), (-0.65, 0.15), (0.55, 0.22), (-0.05, -0.52)]:
            _particle(ax, x, y, color=color)
        ax.text(0, 2.25, name, ha="center", fontsize=16, color=color, weight="bold")
        ax.text(0, -1.42, "$P=1.00\\ atm$，$V=10.0\\ L$，$T=300\\ K$", ha="center", fontsize=11.0)
        ax.text(0, -2.10, f"$n={n:.3f}\\ mol$\n$m={mass:.2f}\\ g$，$d={density:.3f}\\ g\\,L^{{-1}}$", ha="center", fontsize=11.2, color=color, weight="bold")
    fig.text(0.50, 0.055, "$d=\\dfrac{m}{V}=\\dfrac{PM}{RT}$；同溫同壓時，密度比等於莫耳質量比", ha="center", fontsize=13.0, color=F.PURPLE, weight="bold")
    fig.suptitle("等溫、等壓、等體積氣體含相同莫耳數；質量差由莫耳質量決定", fontsize=16, y=0.985)
    fig.subplots_adjust(left=0.03, right=0.97, top=0.82, bottom=0.14, wspace=0.12)
    return _save(fig, "選化I-2-氣體密度與莫耳質量.svg")


def fig_dalton():
    """以相同 V、T 下的分子數比例建立分壓與莫耳分率。"""
    counts = {"A": 6, "B": 3, "C": 1}
    total = sum(counts.values())
    pt = 5.0
    partial = {key: value / total * pt for key, value in counts.items()}
    assert partial == {"A": 3.0, "B": 1.5, "C": 0.5}
    assert np.isclose(sum(partial.values()), pt)

    fig, axes = plt.subplots(1, 2, figsize=(11.8, 5.9), gridspec_kw={"width_ratios": [1.05, 0.95]})
    ax = axes[0]
    ax.axis("off")
    ax.set_xlim(-3.2, 3.2)
    ax.set_ylim(-3, 3)
    _container(ax, -2.45, -1.65, 4.9, 3.5)
    specs = [("A", counts["A"], F.BLUE), ("B", counts["B"], F.AMBER), ("C", counts["C"], F.PURPLE)]
    points = [(-1.75, 1.15), (-0.55, 1.15), (0.65, 1.15), (1.70, 1.10), (-1.40, 0.10), (-0.15, 0.20), (1.15, 0.05), (-1.15, -0.90), (0.20, -0.85), (1.50, -0.72)]
    k = 0
    for label, count, color in specs:
        for _ in range(count):
            _particle(ax, *points[k], color=color, label=label)
            k += 1
    ax.text(0, 2.35, "$n_A:n_B:n_C=6:3:1$", ha="center", fontsize=13.0, weight="bold")
    ax.text(0, -2.20, "$X_A=0.60$，$X_B=0.30$，$X_C=0.10$", ha="center", fontsize=11.5)
    ax.set_title("同一容器中的粒子帳", fontsize=13.5, weight="bold")

    ax = axes[1]
    names = ["A", "B", "C"]
    vals = [partial[name] for name in names]
    colors = [F.BLUE, F.AMBER, F.PURPLE]
    bars = ax.bar(names, vals, color=colors, width=0.58)
    for bar, value in zip(bars, vals):
        ax.text(bar.get_x() + bar.get_width() / 2, value + 0.08, f"{value:.1f} atm", ha="center", fontsize=11.2, weight="bold")
    ax.axhline(pt, color=F.RED, ls="--", lw=1.7)
    ax.text(2.42, pt + 0.08, "$P_t=5.0\\ atm$", ha="right", fontsize=10.5, color=F.RED)
    ax.set_ylabel("分壓／atm")
    ax.set_ylim(0, 5.6)
    F.clean_grid(ax)
    ax.set_title("$P_i=X_iP_t$；柱高總和為總壓", fontsize=13.5, weight="bold")
    fig.suptitle("道耳頓分壓定律：互不反應的氣體各自撞壁，分壓按粒子數比例分配", fontsize=16, y=0.985)
    fig.subplots_adjust(left=0.045, right=0.98, top=0.82, bottom=0.11, wspace=0.15)
    return _save(fig, "選化I-2-分壓的粒子帳.svg")


def fig_connected_vessels():
    """兩容器開閥後以共同總體積重算各分壓。"""
    pa, va = 2.0, 3.0
    pb, vb = 1.0, 2.0
    vt = va + vb
    pa_final = pa * va / vt
    pb_final = pb * vb / vt
    pt_final = pa_final + pb_final
    assert np.isclose(pa_final, 1.2)
    assert np.isclose(pb_final, 0.4)
    assert np.isclose(pt_final, 1.6)

    fig, axes = plt.subplots(1, 2, figsize=(11.8, 5.8))
    for ax in axes:
        ax.axis("off")
        ax.set_xlim(-5.0, 5.0)
        ax.set_ylim(-3.0, 3.0)
    ax = axes[0]
    _box(ax, (-4.50, -0.90), 3.20, 1.80, "$A$\n$P_A=2.0\\ atm$\n$V_A=3.0\\ L$", face="#eef4ff", edge=F.BLUE, fs=11.4)
    _box(ax, (1.30, -0.90), 3.20, 1.80, "$B$\n$P_B=1.0\\ atm$\n$V_B=2.0\\ L$", face="#fff7dd", edge=F.AMBER, fs=11.4)
    ax.plot([-1.28, 1.28], [0, 0], color=F.INK, lw=3)
    ax.add_patch(Rectangle((-0.20, -0.30), 0.40, 0.60, facecolor="#94a3b8", edgecolor=F.INK))
    ax.text(0, 0.60, "閥門關閉", ha="center", fontsize=10.7)
    ax.text(0, -1.75, "同溫、兩氣體互不反應", ha="center", fontsize=11.0, color="#475569")
    ax.set_title("開閥前：各有自己的 $P,V$", fontsize=13.5, weight="bold")

    ax = axes[1]
    _box(ax, (-4.50, -0.90), 9.00, 1.80, "$A$、$B$ 均勻分布在 $V_t=5.0\\ L$\n$P_A'=2.0\\times3.0/5.0=1.2\\ atm$\n$P_B'=1.0\\times2.0/5.0=0.4\\ atm$", face="#e9f8ef", edge=F.GREEN, fs=11.3)
    ax.plot([0, 0], [-0.90, 0.90], color=F.GREEN, lw=1.2, ls="--", alpha=0.7)
    for x, y, color in [(-4.0, 0.55, F.BLUE), (-3.4, -0.55, F.BLUE), (-2.4, 0.60, F.BLUE), (2.35, -0.55, F.BLUE), (3.25, 0.58, F.BLUE), (4.05, -0.48, F.BLUE), (-2.7, -0.60, F.AMBER), (2.75, 0.58, F.AMBER), (3.75, 0.48, F.AMBER)]:
        _particle(ax, x, y, color=color)
    ax.text(0, -1.75, "$P_t'=1.2+0.4=1.6\\ atm$", ha="center", fontsize=12.0, color=F.RED, weight="bold")
    ax.set_title("開閥後：每種氣體都使用共同體積", fontsize=13.5, weight="bold")
    fig.suptitle("連通容器混合：先讓每種氣體膨脹到總體積，再把分壓相加", fontsize=16, y=0.985)
    fig.subplots_adjust(left=0.025, right=0.975, top=0.82, bottom=0.05, wspace=0.08)
    return _save(fig, "選化I-2-連通容器混合.svg")


def fig_water_collection():
    """排水集氣三種液面狀態與乾氣壓力修正。"""
    patm = 755.0
    ph2o = 24.0
    hwater = 136.0
    h_hg = hwater / 13.6
    p_inside_equal = patm
    p_inside_low = patm + h_hg
    p_inside_high = patm - h_hg
    dry = [p_inside_equal - ph2o, p_inside_low - ph2o, p_inside_high - ph2o]
    assert np.isclose(h_hg, 10.0)
    assert np.allclose(dry, [731.0, 741.0, 721.0])

    fig, axes = plt.subplots(1, 3, figsize=(12.0, 6.1))
    panels = [
        ("內外水面等高", 0.0, p_inside_equal, dry[0], F.GREEN),
        ("瓶內水面較低 136 mm", -0.60, p_inside_low, dry[1], F.RED),
        ("瓶內水面較高 136 mm", 0.60, p_inside_high, dry[2], F.BLUE),
    ]
    for ax, (title, offset, pinside, pdry, color) in zip(axes, panels):
        ax.axis("off")
        ax.set_xlim(-2.8, 2.8)
        ax.set_ylim(-3.0, 3.0)
        ax.fill_between([-2.5, 2.5], [-1.65, -1.65], [0.15, 0.15], color="#dbeafe")
        # 倒置集氣瓶下端開口且浸在水中；只畫上緣與兩側。
        ax.add_patch(Rectangle((-1.25, -0.90 + offset), 2.5, 3.1, facecolor="#f8fafc", edgecolor="none"))
        ax.plot([-1.25, -1.25, 1.25, 1.25], [-0.90 + offset, 2.20 + offset, 2.20 + offset, -0.90 + offset], color=F.INK, lw=1.8)
        ax.fill_between([-1.23, 1.23], [-0.88 + offset, -0.88 + offset], [0.15 + offset, 0.15 + offset], color="#bfdbfe")
        for x, y in [(-0.7, 1.55), (0.0, 1.38), (0.72, 1.62)]:
            _particle(ax, x, y + offset, color=color)
        ax.text(0, 0.85 + offset, "乾氣＋水蒸氣", ha="center", fontsize=10.5, color=color, weight="bold")
        ax.text(0, 2.52, title, ha="center", fontsize=12.3, weight="bold")
        ax.text(0, -2.08, f"$P_{{inside}}={pinside:.0f}\\ mmHg$\n$P_{{dry}}={pinside:.0f}-24={pdry:.0f}\\ mmHg$", ha="center", fontsize=10.8, color=color, weight="bold")
    fig.suptitle("排水集氣先用水面高低求瓶內總壓，再扣除同溫的飽和水蒸氣壓", fontsize=16, y=0.985)
    fig.text(0.50, 0.035, "$136\\ mmH_2O=136/13.6=10.0\\ mmHg$；水面較低的一側壓力較大", ha="center", fontsize=11.5, color=F.PURPLE, weight="bold")
    fig.subplots_adjust(left=0.02, right=0.98, top=0.82, bottom=0.11, wspace=0.07)
    return _save(fig, "選化I-2-排水集氣壓力修正.svg")


def fig_gas_experiment():
    """安全的 CaCO3–稀鹽酸排水集氣裝置與原創資料。"""
    time = np.array([0, 20, 40, 60, 80, 100, 120], dtype=float)
    volume = np.array([0, 38, 70, 96, 113, 121, 123], dtype=float)
    increments = np.diff(volume)
    assert np.all(increments >= 0)
    assert np.all(np.diff(increments) <= 0)
    assert volume[-1] == 123

    fig, axes = plt.subplots(1, 2, figsize=(12.0, 6.1), gridspec_kw={"width_ratios": [1.1, 0.9]})
    ax = axes[0]
    ax.axis("off")
    ax.set_xlim(-4.7, 4.7)
    ax.set_ylim(-3.1, 3.1)
    # 反應瓶
    ax.add_patch(Polygon([(-4.0, -1.55), (-3.25, -0.10), (-3.25, 1.55), (-2.55, 1.55), (-2.55, -0.10), (-1.80, -1.55)], closed=True, facecolor="#f8fafc", edgecolor=F.INK, lw=1.8))
    ax.fill_between([-3.78, -2.02], [-1.43, -1.43], [-0.72, -0.72], color="#fde68a")
    for x, y in [(-3.45, -1.05), (-2.95, -1.18), (-2.50, -0.98)]:
        ax.add_patch(Circle((x, y), 0.16, facecolor="#cbd5e1", edgecolor="#64748b"))
    ax.text(-2.90, -0.42, "$CaCO_3(s)$＋稀 $HCl(aq)$", ha="center", fontsize=10.5)
    ax.plot([-2.90, -2.90, 0.35, 0.35], [1.55, 2.10, 2.10, -0.35], color=F.INK, lw=2.0)
    F.arrow(ax, (-1.55, 2.10), (-0.65, 2.10), color=F.BLUE, lw=1.7, mutation=11)
    ax.text(-1.10, 2.42, "$CO_2$ 流向", ha="center", fontsize=10.4, color=F.BLUE, weight="bold")
    # 水槽與量筒
    ax.fill_between([-0.55, 4.25], [-1.70, -1.70], [0.00, 0.00], color="#dbeafe")
    # 倒置量筒下端開口，導管末端伸入筒內後氣泡上升。
    ax.add_patch(Rectangle((1.05, -1.10), 2.15, 3.05, facecolor="#f8fafc", edgecolor="none"))
    ax.plot([1.05, 1.05, 3.20, 3.20], [-1.10, 1.95, 1.95, -1.10], color=F.INK, lw=1.8)
    ax.fill_between([1.08, 3.17], [-1.08, -1.08], [-0.15, -0.15], color="#bfdbfe")
    ax.plot([0.35, 0.35, 2.05], [-0.35, -0.88, -0.88], color=F.INK, lw=2.0)
    F.arrow(ax, (2.05, -0.82), (2.05, 0.02), color=F.BLUE, lw=1.7, mutation=11)
    for y in (0.20, 0.55, 0.90):
        ax.add_patch(Circle((2.05, y), 0.08, facecolor="white", edgecolor=F.BLUE, lw=1.0))
    ax.text(2.12, 1.48, "倒置量筒\n讀取氣體體積", ha="center", fontsize=10.4)
    _box(ax, (-4.35, -2.65), 8.70, 0.58, "護目鏡、實驗衣、手套；導氣系統保持通暢；酸性廢液與殘渣依實驗室規範收集", face="#fdecec", edge=F.RED, fs=9.8)
    ax.set_title("裝置、試劑位置與氣流方向", fontsize=13.5, weight="bold")

    ax = axes[1]
    ax.plot(time, volume, color=F.BLUE, lw=2.4, marker="o", ms=5)
    ax.set_xlabel("時間／s")
    ax.set_ylabel("收集氣體體積／mL")
    ax.set_xlim(0, 125)
    ax.set_ylim(0, 135)
    F.clean_grid(ax)
    ax.axhline(123, color=F.RED, ls="--", lw=1.4)
    ax.text(119, 126, "平台約 123 mL", ha="right", fontsize=10.2, color=F.RED)
    ax.text(57, 48, "斜率逐漸變小\n表示產氣速率下降", ha="center", fontsize=10.5, color=F.PURPLE)
    ax.set_title("原創量測資料：觀察量是體積與時間", fontsize=13.5, weight="bold")
    fig.suptitle("碳酸鈣與稀鹽酸產生二氧化碳：由裝置與資料分開記錄觀察和推論", fontsize=16, y=0.985)
    fig.subplots_adjust(left=0.04, right=0.98, top=0.82, bottom=0.12, wspace=0.22)
    return _save(fig, "選化I-2-二氧化碳集氣實驗.svg")


def main():
    for entrypoint, filename in FIGURE_OUTPUTS:
        assert entrypoint in globals(), f"缺少圖形函式：{entrypoint}"
        globals()[entrypoint]()
        expected = os.path.join(CH, "assets", filename)
        assert os.path.exists(expected), f"圖檔未產生：{expected}"


if __name__ == "__main__":
    main()
