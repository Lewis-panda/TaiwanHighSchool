# -*- coding: utf-8 -*-
"""產生「必化-1 物質的分類與組成」學生講義的章內 SVG。

重繪：.venv/bin/python _tools/fig_content_必化-1.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, FancyBboxPatch, Polygon, Rectangle

import figlib as F


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CH = os.path.join(ROOT, "content", "必修化學", "必化-1")


FIGURE_OUTPUTS = (
    ("fig_classification_tree", "必化-1-物質分類決策樹.svg"),
    ("fig_separation_map", "必化-1-分離方法選擇圖.svg"),
    ("fig_separation_apparatus", "必化-1-萃取蒸餾層析裝置.svg"),
    ("fig_states_heating", "必化-1-三態粒子與加熱曲線.svg"),
    ("fig_laws_particles", "必化-1-定比倍比粒子模型.svg"),
    ("fig_mole_bridge", "必化-1-莫耳換算橋.svg"),
    ("fig_atom_periodic", "必化-1-原子結構與週期位置.svg"),
    ("fig_bonding_properties", "必化-1-鍵結結構與性質.svg"),
)


def _save(fig, filename):
    """公開章內圖只輸出 SVG。"""
    assert filename.endswith(".svg")
    return F.save_to(
        fig,
        CH,
        filename[:-4],
        output_subdir="assets",
        write_pdf=False,
    )


def _rounded(ax, xy, width, height, text, face="#eef4ff", edge=F.BLUE, fs=12.0):
    box = FancyBboxPatch(
        xy,
        width,
        height,
        boxstyle="round,pad=0.04,rounding_size=0.10",
        facecolor=face,
        edgecolor=edge,
        lw=1.7,
    )
    ax.add_patch(box)
    ax.text(xy[0] + width / 2, xy[1] + height / 2, text, ha="center", va="center", fontsize=fs)
    return box


def _particle(ax, x, y, color, label=None, radius=0.12, edge="white"):
    circle = Circle((x, y), radius, facecolor=color, edgecolor=edge, lw=1.0, zorder=5)
    ax.add_patch(circle)
    if label:
        ax.text(x, y, label, ha="center", va="center", fontsize=8.5, color="white", weight="bold", zorder=6)
    return circle


def fig_classification_tree():
    """以組成是否固定及能否化學分解，建立物質分類。"""
    fig, ax = F.schematic(10.8, 5.9)
    ax.set_xlim(-5.4, 5.4)
    ax.set_ylim(-3.0, 3.0)

    _rounded(ax, (-1.05, 2.18), 2.1, 0.62, "物質樣品", face="#fff7dd", edge=F.AMBER, fs=14)
    _rounded(ax, (-1.42, 0.90), 2.84, 0.70, "在指定條件下\n組成是否固定？", face="#f8fafc", edge="#64748b")
    _rounded(ax, (-4.82, -0.40), 2.85, 0.72, "否：混合物\n可用物理方法分離", face="#fff1e6", edge=F.AMBER)
    _rounded(ax, (1.97, -0.40), 2.85, 0.72, "是：純物質\n有特徵性質", face="#e9f8ef", edge=F.GREEN)
    _rounded(ax, (1.97, -1.62), 2.85, 0.70, "能否化學分解成\n其他種純物質？", face="#f8fafc", edge="#64748b")
    _rounded(ax, (0.12, -2.76), 2.25, 0.66, "能：化合物\n例：$H_2O$、NaCl", face="#eef4ff", edge=F.BLUE)
    _rounded(ax, (3.00, -2.76), 2.20, 0.66, "不能：元素\n例：$O_2$、Cu", face="#f1ecff", edge=F.PURPLE)

    F.arrow(ax, (0, 2.18), (0, 1.64), color="#64748b", lw=1.8, mutation=14)
    F.arrow(ax, (-0.35, 0.90), (-3.05, 0.34), color=F.AMBER, lw=2.0, mutation=15)
    F.arrow(ax, (0.35, 0.90), (3.05, 0.34), color=F.GREEN, lw=2.0, mutation=15)
    ax.text(-1.68, 0.72, "否", color=F.AMBER, fontsize=11.5, weight="bold")
    ax.text(1.60, 0.72, "是", color=F.GREEN, fontsize=11.5, weight="bold")
    F.arrow(ax, (3.39, -0.40), (3.39, -0.88), color="#64748b", lw=1.8, mutation=14)
    F.arrow(ax, (2.70, -1.62), (1.48, -2.08), color=F.BLUE, lw=1.8, mutation=14)
    F.arrow(ax, (4.08, -1.62), (4.10, -2.08), color=F.PURPLE, lw=1.8, mutation=14)
    ax.text(2.18, -1.84, "能", color=F.BLUE, fontsize=11.5, weight="bold")
    ax.text(4.40, -1.84, "不能", color=F.PURPLE, fontsize=11.5, weight="bold")

    ax.text(-3.40, -0.82, "均相：每一小份組成相同\n非均相：可辨識不同相或區域", ha="center", va="top", fontsize=11, color="#475569")
    fig.suptitle("分類的核心是「組成」與「化學可分解性」", fontsize=16, y=0.98)
    fig.subplots_adjust(left=0.03, right=0.97, top=0.90, bottom=0.04)
    return _save(fig, "必化-1-物質分類決策樹.svg")


def fig_separation_map():
    """以可觀察的物性差異選擇分離方法。"""
    fig, ax = F.schematic(11.3, 5.8)
    ax.set_xlim(-5.7, 5.7)
    ax.set_ylim(-3.0, 3.0)

    _rounded(ax, (-1.25, 2.15), 2.5, 0.62, "混合物的成分差異", face="#fff7dd", edge=F.AMBER, fs=14)
    entries = [
        (-5.30, 0.70, "粒徑／相別", "過濾、傾析、分液", "泥沙水；油與水", F.BLUE),
        (-2.63, 0.70, "沸點差", "蒸餾／分餾", "飲用水淨化；溶劑回收", F.RED),
        (0.05, 0.70, "溶解度隨溫度", "蒸發、結晶、再結晶", "固體純化", F.GREEN),
        (2.72, 0.70, "在兩溶劑中的溶解度", "萃取", "食品香味成分、色素", F.PURPLE),
    ]
    for x, y, prop, method, example, color in entries:
        _rounded(ax, (x, y), 2.48, 0.72, prop, face="#f8fafc", edge=color, fs=11.2)
        _rounded(ax, (x, -0.42), 2.48, 0.72, method, face="#ffffff", edge=color, fs=11.2)
        ax.text(x + 1.24, -1.10, example, ha="center", va="top", fontsize=10.4, color="#475569")
        F.arrow(ax, (x + 1.24, 0.70), (x + 1.24, 0.34), color=color, lw=1.8, mutation=13)
        F.arrow(ax, (0, 2.15), (x + 1.24, 1.44), color=color, lw=1.4, mutation=12)

    _rounded(ax, (-1.50, -2.40), 3.0, 0.76, "固定相吸附與移動相溶解的競合\n→ 層析（依條件比較 $R_f$）", face="#fff1e6", edge=F.AMBER, fs=11.5)
    F.arrow(ax, (0, 2.15), (0, -1.62), color=F.AMBER, lw=1.5, mutation=13)
    ax.text(0, -2.78, "選擇標準：只用題目資料已顯示的性質差異，並先確認各成分不會在操作中發生不期待的反應。", ha="center", fontsize=10.8, color="#475569")
    fig.suptitle("分離混合物：先找成分間可利用的物理性質差異", fontsize=16, y=0.98)
    fig.subplots_adjust(left=0.02, right=0.98, top=0.90, bottom=0.04)
    return _save(fig, "必化-1-分離方法選擇圖.svg")


def fig_separation_apparatus():
    """以三聯圖畫出萃取、蒸餾與 TLC 的物質流向。"""
    fig, axes = plt.subplots(1, 3, figsize=(12.2, 5.3))
    for ax in axes:
        ax.set_aspect("equal")
        ax.axis("off")

    # 萃取
    ax = axes[0]
    funnel = Polygon([(-1.05, 1.45), (1.05, 1.45), (0.42, -0.35), (0.12, -0.85), (-0.12, -0.85), (-0.42, -0.35)], closed=True, facecolor="#f8fafc", edgecolor=F.INK, lw=1.8)
    ax.add_patch(funnel)
    ax.add_patch(Polygon([(-0.77, 0.75), (0.77, 0.75), (0.42, -0.35), (-0.42, -0.35)], closed=True, facecolor="#f7c873", edgecolor="none", alpha=0.75))
    ax.add_patch(Polygon([(-0.94, 1.23), (0.94, 1.23), (0.77, 0.75), (-0.77, 0.75)], closed=True, facecolor="#dbeafe", edgecolor="none", alpha=0.85))
    ax.plot([-0.22, 0.22], [-0.86, -0.86], color=F.INK, lw=3)
    ax.plot([0, 0], [-0.86, -1.35], color=F.INK, lw=1.8)
    F.arrow(ax, (1.28, 0.96), (0.80, 0.96), color=F.BLUE, lw=1.8, mutation=13)
    F.arrow(ax, (1.28, 0.25), (0.62, 0.25), color=F.AMBER, lw=1.8, mutation=13)
    ax.text(1.30, 1.02, "上層：密度較小", ha="left", fontsize=10.3, color=F.BLUE)
    ax.text(1.30, 0.32, "下層：密度較大", ha="left", fontsize=10.3, color=F.AMBER)
    ax.text(0, -1.67, "先靜置分層，再開活栓分液", ha="center", fontsize=10.4)
    ax.set_xlim(-1.55, 2.45)
    ax.set_ylim(-2.0, 2.0)
    ax.set_title("萃取：溶質重新分配", fontsize=13.5)

    # 蒸餾
    ax = axes[1]
    flask = Circle((-1.05, -0.30), 0.72, facecolor="#eef4ff", edgecolor=F.INK, lw=1.8)
    ax.add_patch(flask)
    ax.add_patch(Rectangle((-1.30, 0.20), 0.50, 0.75, facecolor="#ffffff", edgecolor=F.INK, lw=1.6))
    ax.plot([-1.05, -1.05], [0.95, 1.54], color=F.INK, lw=1.7)
    ax.plot([-1.05, 1.00], [0.80, 0.80], color=F.INK, lw=6, solid_capstyle="round")
    ax.plot([-0.88, 0.82], [0.80, 0.80], color="#cbd5e1", lw=2.5)
    ax.plot([1.00, 1.45], [0.80, -0.30], color=F.INK, lw=4)
    ax.add_patch(Polygon([(1.16, -0.25), (1.70, -0.25), (1.55, -1.35), (1.30, -1.35)], closed=True, facecolor="#dbeafe", edgecolor=F.INK, lw=1.5))
    F.arrow(ax, (-0.78, 0.80), (0.62, 0.80), color=F.RED, lw=2.2, mutation=15)
    F.arrow(ax, (0.62, 0.58), (-0.72, 0.58), color=F.BLUE, lw=1.6, mutation=13)
    ax.text(-0.05, 1.15, "蒸氣 →", ha="center", fontsize=10.4, color=F.RED)
    ax.text(-0.05, 0.25, "冷卻水：下進上出", ha="center", fontsize=10.4, color=F.BLUE)
    ax.text(-1.05, -0.34, "低沸點\n成分汽化", ha="center", va="center", fontsize=10)
    ax.text(1.46, -1.62, "餞出液", ha="center", fontsize=10.4)
    ax.set_xlim(-2.05, 2.10)
    ax.set_ylim(-2.0, 2.0)
    ax.set_title("蒸餾：汽化後再冷凝", fontsize=13.5)

    # TLC
    ax = axes[2]
    ax.add_patch(Rectangle((-0.75, -1.45), 1.5, 2.85, facecolor="#fffdf3", edgecolor=F.INK, lw=1.6))
    baseline_y, front_y = -1.05, 1.02
    ax.plot([-0.65, 0.65], [baseline_y, baseline_y], color="#64748b", lw=1.2, ls="--")
    ax.plot([-0.65, 0.65], [front_y, front_y], color=F.BLUE, lw=1.5, ls="--")
    spot_y = np.array([-0.05, 0.55, 0.80])
    colors = [F.RED, F.GREEN, F.PURPLE]
    for y, color in zip(spot_y, colors):
        ax.add_patch(Circle((0, y), 0.11, facecolor=color, edgecolor="white", lw=1))
    solvent_distance = front_y - baseline_y
    distances = spot_y - baseline_y
    rf_values = distances / solvent_distance
    assert np.all((rf_values > 0) & (rf_values < 1))
    assert np.allclose(rf_values, [1.00 / 2.07, 1.60 / 2.07, 1.85 / 2.07])
    F.arrow(ax, (1.08, baseline_y), (1.08, front_y), color=F.BLUE, lw=1.8, mutation=13)
    ax.text(1.18, 0.0, "溶劑前緣距離", rotation=90, va="center", fontsize=10, color=F.BLUE)
    ax.text(-0.83, baseline_y, "起始線", ha="right", va="center", fontsize=10)
    ax.text(-0.83, front_y, "溶劑前緣", ha="right", va="center", fontsize=10, color=F.BLUE)
    ax.text(0, -1.72, "$R_f$ = 色點移動距離 ÷ 溶劑前緣移動距離", ha="center", fontsize=11.2)
    ax.set_xlim(-1.55, 1.85)
    ax.set_ylim(-2.0, 2.0)
    ax.set_title("薄層層析：吸附與溶解的競合", fontsize=13.5)

    fig.suptitle("三種操作的物質流向與測量位置", fontsize=16, y=0.98)
    fig.subplots_adjust(left=0.03, right=0.98, top=0.87, bottom=0.08, wspace=0.20)
    return _save(fig, "必化-1-萃取蒸餾層析裝置.svg")


def fig_states_heating():
    """同時對齊粒子間距與純物質定壓加熱曲線。"""
    fig = plt.figure(figsize=(11.8, 5.8))
    gs = fig.add_gridspec(1, 2, width_ratios=[1.15, 1.45])
    axp = fig.add_subplot(gs[0, 0])
    axh = fig.add_subplot(gs[0, 1])

    axp.set_aspect("equal")
    axp.axis("off")
    states = [
        (-2.7, "固態", [(0, 0), (0.35, 0), (0.70, 0), (0, 0.35), (0.35, 0.35), (0.70, 0.35), (0, 0.70), (0.35, 0.70), (0.70, 0.70)]),
        (0.0, "液態", [(0.05, 0.05), (0.42, 0.10), (0.75, 0.02), (0.18, 0.42), (0.58, 0.36), (0.84, 0.55), (0.02, 0.76), (0.40, 0.72), (0.72, 0.86)]),
        (2.7, "氣態", [(0.05, 0.10), (0.78, 0.06), (0.42, 0.44), (0.08, 0.86), (0.90, 0.78)]),
    ]
    particle_counts = []
    for x0, label, coords in states:
        axp.add_patch(Rectangle((x0 - 0.55, -0.55), 1.10, 1.10, facecolor="#f8fafc", edgecolor="#64748b", lw=1.4))
        for x, y in coords:
            _particle(axp, x0 - 0.45 + x, -0.45 + y, F.BLUE, radius=0.08)
        particle_counts.append(len(coords))
        axp.text(x0, -0.86, label, ha="center", fontsize=12.5, weight="bold")
    assert particle_counts == [9, 9, 5]
    axp.text(-2.7, -1.22, "位置只小幅振動", ha="center", fontsize=9.8, color="#475569")
    axp.text(0.0, -1.22, "仍相互接近，可流動", ha="center", fontsize=9.8, color="#475569")
    axp.text(2.7, -1.22, "間距大，充滿容器", ha="center", fontsize=9.8, color="#475569")
    axp.set_xlim(-3.55, 3.55)
    axp.set_ylim(-1.55, 1.55)
    axp.set_title("粒子模型：排列與間距", fontsize=13.5)

    # 加熱曲線：座標是一致的理想純物質定壓示意。
    time = np.array([0, 2, 5, 8, 12, 15], dtype=float)
    temp = np.array([-20, 0, 0, 100, 100, 135], dtype=float)
    assert np.all(np.diff(time) > 0)
    assert temp[1] == temp[2] and temp[3] == temp[4]
    axh.plot(time, temp, color=F.RED, lw=3.0, marker="o", ms=5)
    labels = ["固態升溫", "熔化", "液態升溫", "汽化", "氣態升溫"]
    mids = [(1, -10), (3.5, 0), (6.5, 50), (10, 100), (13.5, 118)]
    for text_label, (x, y) in zip(labels, mids):
        axh.text(x, y + (9 if "升溫" in text_label else 7), text_label, ha="center", fontsize=10.5)
    axh.annotate("單一相：加入能量主要使粒子平均動能增加", xy=(6.5, 50), xytext=(4.7, 132), arrowprops=dict(arrowstyle="->", color=F.BLUE, lw=1.5), color=F.BLUE, fontsize=10.3)
    axh.annotate("相變平臺：加入能量主要用於改變粒子間作用", xy=(10, 100), xytext=(7.2, 22), arrowprops=dict(arrowstyle="->", color=F.GREEN, lw=1.5), color=F.GREEN, fontsize=10.3)
    axh.set_xlabel("加熱時間（固定功率）")
    axh.set_ylabel("溫度（°C）")
    axh.set_xlim(-0.3, 15.5)
    axh.set_ylim(-30, 150)
    F.clean_grid(axh)
    axh.set_title("純物質在定壓下的加熱曲線", fontsize=13.5)

    fig.suptitle("宏觀的溫度與狀態，對應粒子動能與間距的改變", fontsize=16, y=0.98)
    fig.subplots_adjust(left=0.05, right=0.98, top=0.87, bottom=0.13, wspace=0.28)
    return _save(fig, "必化-1-三態粒子與加熱曲線.svg")


def fig_laws_particles():
    """以可數粒子解釋定比、倍比與質量守恆。"""
    fig, axes = plt.subplots(1, 3, figsize=(12.0, 4.7))
    blue_mass, red_mass = 12, 16
    for ax in axes:
        ax.set_aspect("equal")
        ax.axis("off")

    # 定比
    ax = axes[0]
    molecules = [(-0.85, 0.50), (0.20, 0.50), (-0.85, -0.45), (0.20, -0.45)]
    for x, y in molecules:
        _particle(ax, x, y, F.BLUE, "A")
        _particle(ax, x + 0.28, y, F.RED, "B")
    n_a, n_b = 4, 4
    mass_ratio = n_a * blue_mass / (n_b * red_mass)
    assert np.isclose(mass_ratio, 12 / 16)
    ax.text(-0.20, -1.18, r"每份 $AB$ 皆含 $A:B=1:1$", ha="center", fontsize=11)
    ax.text(-0.20, -1.55, r"質量比 $m_A:m_B=12:16=3:4$", ha="center", fontsize=11, color=F.BLUE)
    ax.set_xlim(-1.45, 1.25)
    ax.set_ylim(-1.8, 1.25)
    ax.set_title("定比定律", fontsize=13.5)

    # 倍比
    ax = axes[1]
    for y, count_b, label in [(0.55, 1, "$AB$"), (-0.45, 2, "$AB_2$")]:
        _particle(ax, -0.45, y, F.BLUE, "A")
        for j in range(count_b):
            _particle(ax, -0.10 + 0.28 * j, y, F.RED, "B")
        ax.text(0.72, y, label, fontsize=12, va="center")
    fixed_a_mass = blue_mass
    b_masses = np.array([red_mass, 2 * red_mass])
    assert np.allclose(b_masses / fixed_a_mass, [4 / 3, 8 / 3])
    assert b_masses[0] / b_masses[1] == 1 / 2
    ax.text(0.0, -1.20, "固定 12 g A，對應的 B 質量", ha="center", fontsize=11)
    ax.text(0.0, -1.55, r"$16:32=1:2$", ha="center", fontsize=12, color=F.PURPLE)
    ax.set_xlim(-1.20, 1.35)
    ax.set_ylim(-1.8, 1.25)
    ax.set_title("倍比定律", fontsize=13.5)

    # 守恆
    ax = axes[2]
    reactants = [(-1.05, 0.45, F.BLUE, "A"), (-0.75, 0.45, F.BLUE, "A"), (-1.00, -0.38, F.RED, "B"), (-0.70, -0.38, F.RED, "B")]
    products = [(0.45, 0.45, F.BLUE, "A"), (0.73, 0.45, F.RED, "B"), (0.45, -0.38, F.BLUE, "A"), (0.73, -0.38, F.RED, "B")]
    for x, y, c, lab in reactants + products:
        _particle(ax, x, y, c, lab)
    F.arrow(ax, (-0.30, 0.05), (0.18, 0.05), color=F.GREEN, lw=2.2, mutation=15)
    reactant_counts = {"A": 2, "B": 2}
    product_counts = {"A": 2, "B": 2}
    assert reactant_counts == product_counts
    ax.text(-0.86, -1.16, "反應前", ha="center", fontsize=11.5)
    ax.text(0.60, -1.16, "反應後", ha="center", fontsize=11.5)
    ax.text(-0.12, -1.55, r"$2A+B_2\rightarrow 2AB$：A、B 原子數各自守恆", ha="center", fontsize=10.8, color=F.GREEN)
    ax.set_xlim(-1.40, 1.35)
    ax.set_ylim(-1.8, 1.25)
    ax.set_title("質量守恆（密閉系統）", fontsize=13.5)

    fig.suptitle("基本定律的共同核心：化學反應是原子的重新排列", fontsize=16, y=0.98)
    fig.subplots_adjust(left=0.03, right=0.98, top=0.83, bottom=0.08, wspace=0.20)
    return _save(fig, "必化-1-定比倍比粒子模型.svg")


def fig_mole_bridge():
    """將質量、莫耳數、粒子數與條件限定的氣體體積連結。"""
    fig, ax = F.schematic(11.2, 5.3)
    ax.set_xlim(-5.6, 5.6)
    ax.set_ylim(-2.65, 2.65)

    nodes = {
        "mass": (-4.85, 0.10, 2.3, 1.0, "質量 $m$\n單位：g"),
        "mole": (-1.15, 0.10, 2.3, 1.0, "莫耳數 $n$\n單位：mol"),
        "particles": (2.55, 0.10, 2.3, 1.0, "粒子數 $N$\n指定原子／分子／離子"),
        "gas": (-1.15, -2.05, 2.3, 0.90, "氣體體積 $V$\n需給定 $T,P$"),
    }
    colors = [F.BLUE, F.GREEN, F.PURPLE, F.AMBER]
    for (x, y, w, h, label), color in zip(nodes.values(), colors):
        _rounded(ax, (x, y), w, h, label, face="#f8fafc", edge=color, fs=12.2)

    # 質量↔莫耳
    F.arrow(ax, (-2.55, 0.78), (-1.22, 0.78), color=F.BLUE, lw=2.0, mutation=14)
    F.arrow(ax, (-1.22, 0.42), (-2.55, 0.42), color=F.BLUE, lw=2.0, mutation=14)
    ax.text(-1.87, 1.22, r"$÷ M$", ha="center", fontsize=12, color=F.BLUE)
    ax.text(-1.87, 0.02, r"$× M$", ha="center", fontsize=12, color=F.BLUE)
    # 莫耳↔粒子
    F.arrow(ax, (1.15, 0.78), (2.48, 0.78), color=F.PURPLE, lw=2.0, mutation=14)
    F.arrow(ax, (2.48, 0.42), (1.15, 0.42), color=F.PURPLE, lw=2.0, mutation=14)
    ax.text(1.82, 1.22, r"$× N_A$", ha="center", fontsize=12, color=F.PURPLE)
    ax.text(1.82, 0.02, r"$÷ N_A$", ha="center", fontsize=12, color=F.PURPLE)
    # 莫耳↔氣體體積
    F.arrow(ax, (-0.20, 0.08), (-0.20, -1.10), color=F.AMBER, lw=2.0, mutation=14)
    F.arrow(ax, (0.20, -1.10), (0.20, 0.08), color=F.AMBER, lw=2.0, mutation=14)
    ax.text(-1.65, -0.67, r"$× V_m(T,P)$", ha="left", fontsize=11.5, color=F.AMBER)
    ax.text(0.38, -0.67, r"$÷ V_m(T,P)$", ha="left", fontsize=11.5, color=F.AMBER)

    avogadro = 6.02214076e23
    assert avogadro == 6.02214076e23
    ax.text(0, 2.08, r"$n=\dfrac{m}{M}=\dfrac{N}{N_A}$", ha="center", fontsize=16, color=F.INK)
    ax.text(0, 1.62, r"$N_A=6.022\,140\,76\times10^{23}\ \mathrm{mol^{-1}}$（精確定義值）", ha="center", fontsize=11.5, color="#475569")
    ax.text(0, -2.50, r"0 °C、1 atm：$V_m\approx22.4\ \mathrm{L/mol}$；25 °C、1 atm：$V_m\approx24.5\ \mathrm{L/mol}$", ha="center", fontsize=11, color="#475569")
    fig.suptitle("所有換算都先回到莫耳數，並檢查單位與氣體條件", fontsize=16, y=0.98)
    fig.subplots_adjust(left=0.02, right=0.98, top=0.88, bottom=0.04)
    return _save(fig, "必化-1-莫耳換算橋.svg")


def fig_atom_periodic():
    """將核素記法、殼層排列與週期位置對齊。"""
    fig = plt.figure(figsize=(11.7, 5.6))
    gs = fig.add_gridspec(1, 2, width_ratios=[1.0, 1.45])
    axa = fig.add_subplot(gs[0, 0])
    axp = fig.add_subplot(gs[0, 1])

    axa.set_aspect("equal")
    axa.axis("off")
    # Na 的殼層模型 2,8,1
    nucleus = Circle((0, 0), 0.34, facecolor=F.RED, edgecolor="white", lw=1.2)
    axa.add_patch(nucleus)
    axa.text(0, 0, "11 p\n12 n", ha="center", va="center", fontsize=9, color="white", weight="bold")
    shell_radii = [0.78, 1.35, 1.92]
    electrons = [2, 8, 1]
    for r, count in zip(shell_radii, electrons):
        axa.add_patch(Circle((0, 0), r, fill=False, edgecolor="#94a3b8", lw=1.2))
        for theta in np.linspace(90, 450, count, endpoint=False):
            rad = np.deg2rad(theta)
            _particle(axa, r * np.cos(rad), r * np.sin(rad), F.BLUE, radius=0.07)
    assert sum(electrons) == 11
    axa.text(0, -2.35, r"$^{23}_{11}\mathrm{Na}$：$p=11, n=12, e=11$", ha="center", fontsize=11.5)
    axa.text(0, -2.72, "殼層排列 2,8,1 → 第 3 週期、第 1 族", ha="center", fontsize=11, color=F.BLUE)
    axa.set_xlim(-2.55, 2.55)
    axa.set_ylim(-3.0, 2.25)
    axa.set_title("原子序決定元素身分", fontsize=13.5)

    axp.axis("off")
    # 簡化前 18 號主族週期表
    groups = [1, 2, 13, 14, 15, 16, 17, 18]
    period_rows = {
        1: {1: "H", 18: "He"},
        2: {1: "Li", 2: "Be", 13: "B", 14: "C", 15: "N", 16: "O", 17: "F", 18: "Ne"},
        3: {1: "Na", 2: "Mg", 13: "Al", 14: "Si", 15: "P", 16: "S", 17: "Cl", 18: "Ar"},
    }
    for col, group in enumerate(groups):
        axp.text(col + 0.5, 3.30, str(group), ha="center", va="center", fontsize=10, color="#64748b")
    for period in [1, 2, 3]:
        axp.text(-0.28, 3.0 - period, f"週期 {period}", ha="right", va="center", fontsize=10, color="#64748b")
        for col, group in enumerate(groups):
            symbol = period_rows[period].get(group, "")
            face = "#ffffff"
            edge = "#cbd5e1"
            if symbol == "Na":
                face, edge = "#fff7dd", F.AMBER
            rect = Rectangle((col, 2.5 - period), 1.0, 1.0, facecolor=face, edgecolor=edge, lw=1.4)
            axp.add_patch(rect)
            if symbol:
                axp.text(col + 0.5, 3.0 - period, symbol, ha="center", va="center", fontsize=12, weight="bold" if symbol == "Na" else None)
    F.arrow(axp, (0.50, -0.85), (0.50, -0.02), color=F.AMBER, lw=2.1, mutation=15)
    axp.text(0.50, -1.12, "Na：外層 1 電子，位於第 1 族", ha="center", fontsize=10.5, color=F.AMBER)
    axp.text(4.0, -1.70, "同週期向右：有效核吸引增強，原子半徑整體趨小", ha="center", fontsize=10.5, color=F.BLUE)
    F.arrow(axp, (0.55, -1.42), (7.40, -1.42), color=F.BLUE, lw=1.8, mutation=14)
    F.arrow(axp, (8.30, 1.95), (8.30, -0.38), color=F.GREEN, lw=1.8, mutation=14)
    axp.text(8.55, 0.75, "同族向下：\n新增電子層\n半徑整體趨大", ha="left", va="center", fontsize=10.5, color=F.GREEN)
    axp.set_xlim(-0.9, 10.05)
    axp.set_ylim(-2.0, 3.55)
    axp.set_title("價層層數對應週期；主族價電子對應族", fontsize=13.5)

    fig.suptitle("從核內的質子數，一路連到電子排列與週期性", fontsize=16, y=0.98)
    fig.subplots_adjust(left=0.04, right=0.98, top=0.86, bottom=0.08, wspace=0.18)
    return _save(fig, "必化-1-原子結構與週期位置.svg")


def fig_bonding_properties():
    """將鍵結的粒子層次直接連到宏觀性質。"""
    fig, axes = plt.subplots(1, 4, figsize=(13.0, 4.8))
    titles = ["離子晶體", "分子物質", "共價網狀固體", "金屬"]
    for ax, title in zip(axes, titles):
        ax.set_aspect("equal")
        ax.axis("off")
        ax.set_title(title, fontsize=13.0)

    # ionic lattice
    ax = axes[0]
    charges = []
    for i in range(4):
        for j in range(4):
            positive = (i + j) % 2 == 0
            x, y = -0.9 + 0.60 * i, -0.45 + 0.60 * j
            _particle(ax, x, y, F.BLUE if positive else F.RED, "+" if positive else "−", radius=0.16)
            charges.append(1 if positive else -1)
    assert sum(charges) == 0
    ax.text(0.0, -1.15, "固態：離子固定，不導電\n熔融／水溶液：離子可移動，可導電", ha="center", va="top", fontsize=9.8)
    ax.set_xlim(-1.3, 1.3)
    ax.set_ylim(-1.7, 2.0)

    # molecular
    ax = axes[1]
    molecule_centers = [(-0.65, 0.95), (0.65, 0.95), (-0.65, -0.05), (0.65, -0.05)]
    for x, y in molecule_centers:
        _particle(ax, x - 0.15, y, F.BLUE, radius=0.14)
        _particle(ax, x + 0.15, y, F.BLUE, radius=0.14)
        ax.plot([x - 0.03, x + 0.03], [y, y], color=F.INK, lw=2.2)
    ax.text(0, 0.48, "分子間作用較弱", ha="center", fontsize=10, color="#64748b")
    ax.text(0.0, -1.15, "相變主要克服分子間作用\n通常熔、沸點較低；多數不導電", ha="center", va="top", fontsize=9.8)
    ax.set_xlim(-1.3, 1.3)
    ax.set_ylim(-1.7, 2.0)

    # covalent network
    ax = axes[2]
    nodes = [(-0.90, 0.15), (-0.45, 0.95), (0.0, 0.15), (0.45, 0.95), (0.90, 0.15), (-0.45, -0.65), (0.45, -0.65)]
    edges = [(0, 1), (1, 2), (2, 3), (3, 4), (0, 5), (5, 2), (2, 6), (6, 4)]
    degrees = [0] * len(nodes)
    for i, j in edges:
        degrees[i] += 1
        degrees[j] += 1
        ax.plot([nodes[i][0], nodes[j][0]], [nodes[i][1], nodes[j][1]], color=F.PURPLE, lw=2.0)
    for x, y in nodes:
        _particle(ax, x, y, F.PURPLE, "C", radius=0.14)
    assert min(degrees) >= 1
    ax.text(0.0, -1.15, "網路中的鍵連續延伸\n熔化需打斷大量共價鍵，熔點高", ha="center", va="top", fontsize=9.8)
    ax.set_xlim(-1.3, 1.3)
    ax.set_ylim(-1.7, 2.0)

    # metallic
    ax = axes[3]
    ions = [(-0.72, 0.85), (0, 0.85), (0.72, 0.85), (-0.72, 0.05), (0, 0.05), (0.72, 0.05)]
    for x, y in ions:
        _particle(ax, x, y, F.AMBER, "+", radius=0.16)
    electron_positions = [(-1.0, 0.48), (-0.35, 0.48), (0.35, 0.48), (1.0, 0.48), (-0.35, 1.18), (0.35, -0.30)]
    for x, y in electron_positions:
        _particle(ax, x, y, F.BLUE, "$e^-$", radius=0.10)
    F.arrow(ax, (-0.95, -0.55), (0.95, -0.55), color=F.BLUE, lw=1.8, mutation=13)
    ax.text(0, -0.78, "非定域電子可移動", ha="center", fontsize=10, color=F.BLUE)
    ax.text(0.0, -1.15, "電子可在晶體中傳遞電荷\n受力滑動後鍵結仍可維持，故有延展性", ha="center", va="top", fontsize=9.8)
    ax.set_xlim(-1.3, 1.3)
    ax.set_ylim(-1.7, 2.0)

    fig.suptitle("性質來自「組成粒子如何排列」與「哪些電荷可以移動」", fontsize=16, y=0.98)
    fig.subplots_adjust(left=0.025, right=0.985, top=0.84, bottom=0.06, wspace=0.20)
    return _save(fig, "必化-1-鍵結結構與性質.svg")


def main():
    for entrypoint, filename in FIGURE_OUTPUTS:
        function = globals().get(entrypoint)
        if not callable(function):
            raise RuntimeError(f"找不到繪圖函式：{entrypoint}")
        output = function()
        if os.path.basename(output) != filename:
            raise RuntimeError(f"輸出不一致：{entrypoint} -> {output}，預期 {filename}")


if __name__ == "__main__":
    main()
