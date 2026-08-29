# -*- coding: utf-8 -*-
"""產生「選化 I-3 溶液的性質」學生講義章內 SVG。

重繪：.venv/bin/python _tools/fig_content_選化I-3.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, FancyBboxPatch, Polygon, Rectangle

import figlib as F


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CH = os.path.join(ROOT, "content", "選修化學I", "選化I-3")


FIGURE_OUTPUTS = (
    ("fig_concentration_ledger", "選化I-3-濃度分母與轉換.svg"),
    ("fig_henry_law", "選化I-3-亨利定律粒子與數據.svg"),
    ("fig_vapor_boiling", "選化I-3-蒸氣壓與沸點.svg"),
    ("fig_humidity_dewpoint", "選化I-3-相對濕度與露點.svg"),
    ("fig_raoult_solution", "選化I-3-拉午耳定律與氣相組成.svg"),
    ("fig_nonideal_transfer", "選化I-3-非理想偏差與密閉轉移.svg"),
    ("fig_colligative_crossings", "選化I-3-氣壓下降與相轉交點.svg"),
    ("fig_freezing_experiment", "選化I-3-凝固點實驗與冷卻曲線.svg"),
    ("fig_osmosis_reverse", "選化I-3-滲透與逆滲透.svg"),
    ("fig_vant_hoff_particles", "選化I-3-凡特何夫因數粒子帳.svg"),
)


def _save(fig, filename):
    assert filename.endswith(".svg")
    return F.save_to(fig, CH, filename[:-4], output_subdir="assets", write_pdf=False)


def _box(ax, xy, width, height, text, *, face="#f8fafc", edge="#64748b", fs=11.0, lw=1.5):
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


def _particle(ax, x, y, color, label="", radius=0.15):
    ax.add_patch(Circle((x, y), radius, facecolor=color, edgecolor="white", lw=0.8, zorder=4))
    if label:
        ax.text(x, y, label, ha="center", va="center", fontsize=7.0, color="white", weight="bold", zorder=5)


def _antoine_water(temp_c):
    """1–100 °C 水的飽和蒸氣壓（mmHg）。"""
    temp_c = np.asarray(temp_c, dtype=float)
    return 10 ** (8.07131 - 1730.63 / (233.426 + temp_c))


def _antoine_inverse(pressure_mmhg):
    return 1730.63 / (8.07131 - np.log10(pressure_mmhg)) - 233.426


def fig_concentration_ledger():
    """用同一份葡萄糖溶液區分各種濃度的分母。"""
    glucose_g, water_g, solution_ml, molar_mass = 18.0, 180.0, 200.0, 180.0
    glucose_mol = glucose_g / molar_mass
    solution_g = glucose_g + water_g
    mass_percent = glucose_g / solution_g * 100
    molarity = glucose_mol / (solution_ml / 1000)
    molality = glucose_mol / (water_g / 1000)
    water_mol = water_g / 18.0
    mole_fraction = glucose_mol / (glucose_mol + water_mol)
    assert np.isclose(mass_percent, 9.090909)
    assert np.isclose(molarity, 0.5)
    assert np.isclose(molality, 5 / 9)
    assert np.isclose(mole_fraction, 1 / 101)

    fig, ax = plt.subplots(figsize=(12.0, 6.2))
    ax.axis("off")
    ax.set_xlim(-6.0, 6.0)
    ax.set_ylim(-3.1, 3.1)
    _box(ax, (-1.85, 1.75), 3.70, 0.82, "18.0 g 葡萄糖＋180.0 g 水\n配成 200.0 mL 溶液", face="#eef4ff", edge=F.BLUE, fs=12.2)
    items = [
        (-5.45, 0.25, "質量百分率", r"$\frac{18.0}{198.0}\times100\%=9.09\%$", "分母：溶液質量", F.RED),
        (-2.72, 0.25, "體積莫耳濃度", r"$C_M=\frac{0.100}{0.200}=0.500\ M$", "分母：溶液體積", F.BLUE),
        (0.02, 0.25, "重量莫耳濃度", r"$C_m=\frac{0.100}{0.180}=0.556\ m$", "分母：溶劑質量", F.GREEN),
        (2.76, 0.25, "莫耳分率", r"$X_G=\frac{0.100}{0.100+10.0}=0.00990$", "分母：全部粒子莫耳數", F.PURPLE),
    ]
    for x, y, title, equation, denom, color in items:
        _box(ax, (x, y - 1.18), 2.67, 2.36, "", face="#ffffff", edge=color)
        ax.text(x + 1.335, y + 0.72, title, ha="center", fontsize=11.4, weight="bold", color=color)
        ax.text(x + 1.335, y + 0.05, equation, ha="center", fontsize=11.0)
        ax.text(x + 1.335, y - 0.65, denom, ha="center", fontsize=10.2, color="#475569")
        F.arrow(ax, (0, 1.72), (x + 1.335, y + 1.20), color=color, lw=1.5, mutation=10)
    _box(ax, (-4.9, -2.63), 9.8, 0.65, "溶液體積會隨溫度改變；質量、莫耳數與它們形成的比值在密閉系統中保持。", face="#f8fafc", edge=F.AMBER, fs=11.5)
    fig.suptitle("濃度公式的核心是分母所指的整體", fontsize=16, y=0.985)
    fig.subplots_adjust(left=0.02, right=0.98, top=0.87, bottom=0.04)
    return _save(fig, "選化I-3-濃度分母與轉換.svg")


def fig_henry_law():
    """固定溫度下以粒子數與數據線同時表示亨利定律。"""
    pressures = np.array([0.0, 1.0, 2.0, 3.0])
    k_h = 0.032
    concentrations = k_h * pressures
    assert np.allclose(np.diff(concentrations), k_h)
    assert np.isclose(concentrations[-1], 0.096)

    fig, axes = plt.subplots(1, 2, figsize=(12.0, 6.2), gridspec_kw={"width_ratios": [1.35, 1.0]})
    ax = axes[0]
    ax.axis("off")
    ax.set_xlim(-4.2, 4.2)
    ax.set_ylim(-3.0, 3.0)
    for j, (p, n) in enumerate([(1, 4), (2, 8), (3, 12)]):
        x0 = -3.95 + j * 2.72
        ax.add_patch(Rectangle((x0, -1.85), 2.25, 3.65, facecolor="#eff6ff", edgecolor=F.BLUE, lw=1.5))
        ax.axhline(0, xmin=(x0 + 4.2) / 8.4, xmax=(x0 + 2.25 + 4.2) / 8.4, color=F.BLUE, lw=1.1)
        for q in range(6):
            _particle(ax, x0 + 0.35 + 0.75 * (q % 3), 0.45 + 0.58 * (q // 3), F.AMBER)
        for q in range(n):
            _particle(ax, x0 + 0.30 + 0.52 * (q % 4), -0.35 - 0.43 * (q // 4), F.BLUE, radius=0.11)
        ax.text(x0 + 1.125, 2.18, rf"$P={p}\ atm$", ha="center", fontsize=11.5, weight="bold")
        ax.text(x0 + 1.125, -2.23, f"溶解粒子 {n}", ha="center", fontsize=10.5, color=F.BLUE)
    ax.text(0, 2.68, "氣相粒子碰撞液面的頻率隨分壓增加", ha="center", fontsize=12, weight="bold")

    graph = axes[1]
    graph.plot(pressures, concentrations, "o-", color=F.BLUE, lw=2.4, ms=7)
    graph.set_xlim(0, 3.2)
    graph.set_ylim(0, 0.105)
    graph.set_xlabel("氣體分壓 $P$ / atm")
    graph.set_ylabel("平衡溶解濃度 $C$ / M")
    graph.grid(alpha=0.22)
    graph.text(1.55, 0.075, r"$C=k_HP$" + "\n" + r"$k_H=0.032\ M\,atm^{-1}$", fontsize=12, color=F.BLUE, weight="bold")
    graph.text(1.60, 0.009, "固定溫度；低壓、稀溶液\n氣體不與溶劑大量反應", ha="center", fontsize=10.5, color="#475569")
    fig.suptitle("亨利定律連結氣體分壓與液相的平衡溶解量", fontsize=16, y=0.985)
    fig.subplots_adjust(left=0.035, right=0.975, top=0.86, bottom=0.11, wspace=0.20)
    return _save(fig, "選化I-3-亨利定律粒子與數據.svg")


def fig_vapor_boiling():
    """動態平衡、飽和蒸氣壓曲線與沸點交點。"""
    temperatures = np.linspace(20, 100, 321)
    vapor_pressure = _antoine_water(temperatures)
    normal_bp = _antoine_inverse(760.0)
    low_bp = _antoine_inverse(500.0)
    assert abs(normal_bp - 100.0) < 0.2
    assert 88.5 < low_bp < 89.0

    fig, axes = plt.subplots(1, 2, figsize=(12.0, 6.2), gridspec_kw={"width_ratios": [0.92, 1.25]})
    ax = axes[0]
    ax.axis("off")
    ax.set_xlim(-3.0, 3.0)
    ax.set_ylim(-3.0, 3.0)
    ax.add_patch(Rectangle((-2.35, -2.05), 4.70, 3.95, facecolor="#f8fafc", edgecolor=F.INK, lw=1.8))
    ax.add_patch(Rectangle((-2.32, -2.02), 4.64, 1.68, facecolor="#bfdbfe", edgecolor="none"))
    for i in range(28):
        _particle(ax, -2.0 + 0.62 * (i % 7), -0.63 - 0.38 * (i // 7), F.BLUE, radius=0.105)
    for x, y in [(-1.65, 0.25), (-0.45, 1.05), (0.45, 0.25), (1.55, 1.25), (1.50, -0.02)]:
        _particle(ax, x, y, F.BLUE, radius=0.12)
    for x in (-1.15, 0.1, 1.25):
        F.arrow(ax, (x, -0.48), (x + 0.12, 0.18), color=F.RED, lw=1.8, mutation=11)
    for x in (-0.55, 0.85):
        F.arrow(ax, (x, 0.98), (x - 0.12, -0.15), color=F.GREEN, lw=1.8, mutation=11)
    ax.text(0, 2.28, "密閉容器中仍有液相", ha="center", fontsize=12, weight="bold")
    ax.text(-1.55, 0.78, "蒸發", color=F.RED, fontsize=11, weight="bold")
    ax.text(0.95, 0.78, "凝結", color=F.GREEN, fontsize=11, weight="bold")
    ax.text(0, -2.52, "平衡時兩個速率相等\n氣相分壓即飽和蒸氣壓", ha="center", fontsize=10.8)

    graph = axes[1]
    graph.plot(temperatures, vapor_pressure, color=F.BLUE, lw=2.5, label="水的飽和蒸氣壓")
    graph.axhline(760, color=F.RED, lw=1.7, ls="--", label=r"$P_{ext}=760\ mmHg$")
    graph.axhline(500, color=F.AMBER, lw=1.7, ls="--", label=r"$P_{ext}=500\ mmHg$")
    graph.scatter([normal_bp, low_bp], [760, 500], color=[F.RED, F.AMBER], zorder=5)
    graph.vlines([normal_bp, low_bp], 0, [760, 500], colors=[F.RED, F.AMBER], linestyles=":", lw=1.5)
    graph.text(96.8, 690, f"{normal_bp:.1f} °C", ha="right", color=F.RED, fontsize=10.8, weight="bold")
    graph.text(low_bp - 1.0, 430, f"{low_bp:.1f} °C", ha="right", color=F.AMBER, fontsize=10.8, weight="bold")
    graph.set_xlim(20, 103)
    graph.set_ylim(0, 820)
    graph.set_xlabel("溫度 / °C")
    graph.set_ylabel("壓力 / mmHg")
    graph.grid(alpha=0.22)
    graph.legend(loc="upper left", fontsize=9.6)
    graph.text(62, 115, "曲線與外壓線的交點就是沸點", fontsize=10.8, color="#475569")
    fig.suptitle("沸騰發生於飽和蒸氣壓等於外界壓力", fontsize=16, y=0.985)
    fig.subplots_adjust(left=0.035, right=0.975, top=0.86, bottom=0.11, wspace=0.18)
    return _save(fig, "選化I-3-蒸氣壓與沸點.svg")


def fig_humidity_dewpoint():
    """實際水蒸氣分壓橫線與飽和曲線同時給出 RH 與露點。"""
    actual_p = 14.0
    p25 = float(_antoine_water(25.0))
    rh25 = actual_p / p25 * 100
    dewpoint = float(_antoine_inverse(actual_p))
    assert 59.0 < rh25 < 59.2
    assert 16.4 < dewpoint < 16.6
    temp = np.linspace(5, 38, 220)

    fig, ax = plt.subplots(figsize=(10.8, 6.3))
    ax.plot(temp, _antoine_water(temp), color=F.BLUE, lw=2.6, label="水的飽和蒸氣壓")
    ax.axhline(actual_p, color=F.RED, lw=2.0, label="實際水蒸氣分壓 14.0 mmHg")
    ax.vlines([dewpoint, 25.0], 0, [actual_p, p25], colors=[F.GREEN, F.PURPLE], linestyles="--", lw=1.6)
    ax.scatter([dewpoint, 25.0, 25.0], [actual_p, actual_p, p25], color=[F.GREEN, F.RED, F.BLUE], zorder=5)
    ax.annotate(f"露點 {dewpoint:.1f} °C\n此處開始飽和", (dewpoint, actual_p), xytext=(7.5, 26), arrowprops={"arrowstyle": "->", "color": F.GREEN}, fontsize=11, color=F.GREEN, weight="bold")
    ax.annotate(f"25 °C 飽和壓 {p25:.1f} mmHg", (25, p25), xytext=(26.3, 37), arrowprops={"arrowstyle": "->", "color": F.BLUE}, fontsize=10.8, color=F.BLUE)
    _box(ax, (20.8, 3.2), 14.6, 7.2, f"$RH=14.0/{p25:.1f}\\times100\\%={rh25:.1f}\\%$", face="#f8fafc", edge=F.PURPLE, fs=12.5)
    ax.fill_between(temp[temp <= dewpoint], _antoine_water(temp[temp <= dewpoint]), actual_p, color=F.BLUE, alpha=0.10)
    ax.text(9.3, 8.0, "冷卻到此區間時\n多餘水氣凝結", fontsize=10.5, color=F.BLUE)
    ax.set_xlim(5, 38)
    ax.set_ylim(0, 52)
    ax.set_xlabel("空氣溫度 / °C")
    ax.set_ylabel("水蒸氣分壓 / mmHg")
    ax.grid(alpha=0.22)
    ax.legend(loc="upper left", fontsize=9.8)
    fig.suptitle("相對濕度比較當下水氣量與同溫的飽和上限", fontsize=16, y=0.985)
    fig.subplots_adjust(left=0.09, right=0.975, top=0.86, bottom=0.11)
    return _save(fig, "選化I-3-相對濕度與露點.svg")


def fig_raoult_solution():
    """二元理想溶液的分壓、總壓與氣相組成。"""
    p_a_star, p_b_star = 200.0, 80.0
    x_a = np.linspace(0, 1, 101)
    p_a = x_a * p_a_star
    p_b = (1 - x_a) * p_b_star
    p_total = p_a + p_b
    x_mark = 0.40
    p_a_mark = x_mark * p_a_star
    p_b_mark = (1 - x_mark) * p_b_star
    p_mark = p_a_mark + p_b_mark
    y_a = p_a_mark / p_mark
    assert np.isclose(p_mark, 128.0)
    assert np.isclose(y_a, 0.625)

    fig, axes = plt.subplots(1, 2, figsize=(12.0, 6.2), gridspec_kw={"width_ratios": [1.15, 0.85]})
    ax = axes[0]
    ax.plot(x_a, p_a, color=F.BLUE, lw=2.2, label="$P_A=X_AP_A^*$")
    ax.plot(x_a, p_b, color=F.AMBER, lw=2.2, label="$P_B=X_BP_B^*$")
    ax.plot(x_a, p_total, color=F.PURPLE, lw=2.7, label="$P_{total}=P_A+P_B$")
    ax.vlines(x_mark, 0, p_mark, color=F.RED, ls="--", lw=1.5)
    ax.scatter([x_mark] * 3, [p_a_mark, p_b_mark, p_mark], color=[F.BLUE, F.AMBER, F.PURPLE], zorder=5)
    ax.text(x_mark + 0.025, p_mark + 7, "$P_{total}=128$", color=F.PURPLE, fontsize=10.5, weight="bold")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 215)
    ax.set_xlabel("液相莫耳分率 $X_A$")
    ax.set_ylabel("平衡蒸氣壓 / mmHg")
    ax.grid(alpha=0.22)
    ax.legend(loc="upper left", fontsize=9.6)
    ax.set_title("液相組成決定各成分分壓", fontsize=13.5, weight="bold")

    right = axes[1]
    right.axis("off")
    right.set_xlim(-3, 3)
    right.set_ylim(-3, 3)
    right.add_patch(Rectangle((-2.25, -1.8), 4.5, 3.55, facecolor="#f8fafc", edgecolor=F.INK, lw=1.6))
    right.add_patch(Rectangle((-2.22, -1.77), 4.44, 1.45, facecolor="#dbeafe", edgecolor="none"))
    liquid_colors = [F.BLUE] * 8 + [F.AMBER] * 12
    for i, color in enumerate(liquid_colors):
        _particle(right, -1.85 + 0.74 * (i % 5), -0.58 - 0.35 * (i // 5), color, radius=0.12)
    vapor_colors = [F.BLUE] * 5 + [F.AMBER] * 3
    for i, color in enumerate(vapor_colors):
        _particle(right, -1.72 + 1.12 * (i % 4), 0.20 + 0.62 * (i // 4), color, radius=0.14)
    right.text(0, 2.35, "液相 $X_A=0.400$", ha="center", fontsize=12, weight="bold", color=F.BLUE)
    right.text(0, -2.28, "氣相 $y_A=P_A/P_{total}=0.625$", ha="center", fontsize=12, weight="bold", color=F.RED)
    right.text(0, -2.68, "$P_A^*>P_B^*$，氣相富含較易揮發的 A", ha="center", fontsize=10.4, color="#475569")
    fig.suptitle("拉午耳定律先求分壓，道爾頓定律再連到氣相組成", fontsize=16, y=0.985)
    fig.subplots_adjust(left=0.07, right=0.975, top=0.84, bottom=0.11, wspace=0.16)
    return _save(fig, "選化I-3-拉午耳定律與氣相組成.svg")


def fig_nonideal_transfer():
    """將偏差的微觀原因與密閉系統的溶劑轉移放在同圖。"""
    x = np.linspace(0, 1, 101)
    ideal = 80 + 120 * x
    deviation = 42 * x * (1 - x)
    positive = ideal + deviation
    negative = ideal - deviation
    assert np.allclose(positive[[0, -1]], ideal[[0, -1]])
    assert positive[50] > ideal[50] > negative[50]

    fig, axes = plt.subplots(1, 2, figsize=(12.0, 6.2))
    ax = axes[0]
    ax.plot(x, positive, color=F.RED, lw=2.4, label="正偏差：A–B 吸引較弱")
    ax.plot(x, ideal, color=F.INK, lw=1.8, ls="--", label="理想線")
    ax.plot(x, negative, color=F.BLUE, lw=2.4, label="負偏差：A–B 吸引較強")
    ax.fill_between(x, ideal, positive, color=F.RED, alpha=0.10)
    ax.fill_between(x, negative, ideal, color=F.BLUE, alpha=0.10)
    ax.set_xlim(0, 1)
    ax.set_ylim(65, 210)
    ax.set_xlabel("液相莫耳分率 $X_A$")
    ax.set_ylabel("總蒸氣壓（同溫）")
    ax.grid(alpha=0.22)
    ax.legend(fontsize=9.2, loc="upper left")
    ax.text(0.50, 199, r"$\Delta H_{mix}>0$" + " 常對應正偏差", ha="center", fontsize=10.4, color=F.RED)
    ax.text(0.50, 76, r"$\Delta H_{mix}<0$" + " 常對應負偏差", ha="center", fontsize=10.4, color=F.BLUE)
    ax.set_title("分子間作用力改變離開液面的難易", fontsize=13.2, weight="bold")

    right = axes[1]
    right.axis("off")
    right.set_xlim(-4.5, 4.5)
    right.set_ylim(-3.0, 3.0)
    for x0, title, solvent_n, solute_n in [(-4.15, "純溶劑\n$P_A^*$ 較大", 18, 0), (1.10, "溶液\n$X_AP_A^*$ 較小", 12, 6)]:
        right.add_patch(Rectangle((x0, -1.55), 3.05, 3.10, facecolor="#f8fafc", edgecolor=F.INK, lw=1.5))
        right.add_patch(Rectangle((x0 + 0.04, -1.51), 2.97, 1.35, facecolor="#dbeafe", edgecolor="none"))
        for i in range(solvent_n):
            _particle(right, x0 + 0.29 + 0.48 * (i % 6), -0.42 - 0.34 * (i // 6), F.BLUE, radius=0.10)
        for i in range(solute_n):
            _particle(right, x0 + 0.52 + 0.82 * (i % 3), -0.60 - 0.47 * (i // 3), F.AMBER, radius=0.12)
        right.text(x0 + 1.525, 2.10, title, ha="center", fontsize=11.2, weight="bold")
    F.arrow(right, (-0.80, 0.72), (0.82, 0.72), color=F.RED, lw=2.6, mutation=17)
    right.text(0, 1.12, "氣相淨傳遞 A", ha="center", fontsize=11.2, color=F.RED, weight="bold")
    right.text(0, -2.18, "只要純溶劑仍存在，壓差會驅動溶劑向溶液側轉移", ha="center", fontsize=10.6)
    right.text(0, -2.58, "終態取決於初始量與容器體積", ha="center", fontsize=10.1, color="#475569")
    right.set_title("氣相共享但兩個液面的平衡壓不同", fontsize=13.2, weight="bold")
    fig.suptitle("蒸氣壓反映液相粒子的逃脫傾向，也能預測密閉系統的質量轉移", fontsize=15.5, y=0.985)
    fig.subplots_adjust(left=0.065, right=0.975, top=0.82, bottom=0.10, wspace=0.20)
    return _save(fig, "選化I-3-非理想偏差與密閉轉移.svg")


def fig_colligative_crossings():
    """用同一蒸氣壓降低解釋沸點上升與凝固點下降。"""
    temp_b = np.linspace(80, 106, 220)
    pure_b = _antoine_water(temp_b)
    x_solvent = 0.965
    solution_b = x_solvent * pure_b
    pure_bp = float(_antoine_inverse(760))
    solution_bp = float(_antoine_inverse(760 / x_solvent))
    delta_tb = solution_bp - pure_bp
    # 凝固點附近的局部線性模型：純溶劑液相與固相於 0 °C 交會。
    temp_f = np.linspace(-5.0, 3.0, 220)
    p_solid = 4.58 + 0.31 * temp_f
    p_liquid = 4.58 + 0.39 * temp_f
    p_solution = p_liquid - 0.145
    solution_fp = -0.145 / (0.39 - 0.31)
    assert 0.95 < delta_tb < 1.05
    assert np.isclose(solution_fp, -1.8125)

    fig, axes = plt.subplots(1, 2, figsize=(12.0, 6.2))
    ax = axes[0]
    ax.plot(temp_b, pure_b, color=F.BLUE, lw=2.4, label="純溶劑")
    ax.plot(temp_b, solution_b, color=F.RED, lw=2.4, label="含難揮發性溶質的溶液")
    ax.axhline(760, color=F.INK, lw=1.6, ls="--", label="外壓 760 mmHg")
    ax.scatter([pure_bp, solution_bp], [760, 760], color=[F.BLUE, F.RED], zorder=5)
    ax.annotate(f"{pure_bp:.1f} °C", (pure_bp, 760), xytext=(95.0, 690), arrowprops={"arrowstyle": "->", "color": F.BLUE}, color=F.BLUE, fontsize=10.5)
    ax.annotate(f"{solution_bp:.1f} °C", (solution_bp, 760), xytext=(102.2, 625), arrowprops={"arrowstyle": "->", "color": F.RED}, color=F.RED, fontsize=10.5)
    ax.set_xlim(80, 106)
    ax.set_ylim(300, 900)
    ax.set_xlabel("溫度 / °C")
    ax.set_ylabel("蒸氣壓 / mmHg")
    ax.grid(alpha=0.22)
    ax.legend(fontsize=9.2, loc="upper left")
    ax.set_title(rf"沸點上升 $\Delta T_b={delta_tb:.2f}$ °C", fontsize=13.5, weight="bold")

    right = axes[1]
    right.plot(temp_f, p_solid, color=F.AMBER, lw=2.3, label="固態溶劑")
    right.plot(temp_f, p_liquid, color=F.BLUE, lw=2.3, label="純液態溶劑")
    right.plot(temp_f, p_solution, color=F.RED, lw=2.3, label="溶液")
    right.scatter([0, solution_fp], [4.58, 4.58 + 0.31 * solution_fp], color=[F.BLUE, F.RED], zorder=5)
    right.vlines([0, solution_fp], 3.0, [4.58, 4.58 + 0.31 * solution_fp], colors=[F.BLUE, F.RED], linestyles="--", lw=1.4)
    right.text(0.15, 4.64, "0.00 °C", fontsize=10.4, color=F.BLUE)
    right.text(solution_fp - 0.15, 3.75, f"{solution_fp:.2f} °C", ha="right", fontsize=10.4, color=F.RED)
    right.set_xlim(-5, 3)
    right.set_ylim(3.0, 5.8)
    right.set_xlabel("溫度 / °C")
    right.set_ylabel("化學勢的蒸氣壓等價表示（局部模型）")
    right.grid(alpha=0.22)
    right.legend(fontsize=9.2, loc="upper left")
    right.set_title("凝固點由固態溶劑與溶液交點決定", fontsize=13.2, weight="bold")
    fig.suptitle("難揮發性溶質降低液相溶劑的蒸氣壓，兩個相轉交點向相反方向移動", fontsize=15.5, y=0.985)
    fig.subplots_adjust(left=0.07, right=0.975, top=0.84, bottom=0.11, wspace=0.22)
    return _save(fig, "選化I-3-氣壓下降與相轉交點.svg")


def fig_freezing_experiment():
    """凝固點下降實驗裝置、過冷與可取點的冷卻曲線。"""
    time = np.arange(0, 13, dtype=float)
    pure = np.array([8.0, 5.7, 3.4, 1.2, -0.8, -0.1, 0.0, 0.0, 0.0, -0.1, -0.5, -1.1, -1.8])
    solution = np.array([8.0, 5.4, 2.8, 0.5, -1.6, -2.6, -1.9, -2.0, -2.2, -2.5, -2.9, -3.4, -4.0])
    assert pure.min() == -1.8
    assert np.isclose(solution[6], -1.9)
    assert np.all(np.diff(solution[6:]) <= 0)

    fig, axes = plt.subplots(1, 2, figsize=(12.0, 6.5), gridspec_kw={"width_ratios": [0.82, 1.25]})
    ax = axes[0]
    ax.axis("off")
    ax.set_xlim(-3.0, 3.0)
    ax.set_ylim(-3.2, 3.2)
    ax.add_patch(Rectangle((-2.15, -2.25), 4.30, 4.10, facecolor="#dbeafe", edgecolor=F.BLUE, lw=1.8))
    for i in range(30):
        color = "#bfdbfe" if i % 3 else "#f1f5f9"
        ax.add_patch(Polygon([(-1.95 + 0.64 * (i % 6), -2.00 + 0.66 * (i // 6)), (-1.70 + 0.64 * (i % 6), -1.74 + 0.66 * (i // 6)), (-1.44 + 0.64 * (i % 6), -2.02 + 0.66 * (i // 6))], closed=True, facecolor=color, edgecolor="#93c5fd", lw=0.7))
    ax.add_patch(Rectangle((-0.82, -1.78), 1.64, 4.15, facecolor="#ffffff", edgecolor=F.INK, lw=1.8))
    ax.add_patch(Rectangle((-0.78, -1.74), 1.56, 1.85, facecolor="#bfdbfe", edgecolor="none"))
    ax.plot([0.10, 0.10], [2.75, -1.15], color=F.RED, lw=2.3)
    ax.add_patch(Circle((0.10, -1.15), 0.12, facecolor=F.RED, edgecolor="white"))
    ax.plot([-0.45, -0.20], [2.62, -1.30], color=F.INK, lw=1.5)
    ax.text(1.15, 2.62, "溫度探針", fontsize=10.8, color=F.RED)
    F.arrow(ax, (1.00, 2.50), (0.18, 2.25), color=F.RED, lw=1.4, mutation=10)
    ax.text(-2.70, 2.10, "冰–食鹽冷浴", fontsize=10.8, color=F.BLUE, weight="bold")
    ax.text(1.02, -0.55, "小試管：\n水或尿素溶液", fontsize=10.5)
    ax.text(0, -2.72, "持續緩慢攪拌；探針測量液體中央\n避免觸及管壁與管底", ha="center", fontsize=10.4)
    ax.set_title("裝置控制熱傳與測溫位置", fontsize=13.5, weight="bold")

    graph = axes[1]
    graph.plot(time, pure, "o-", color=F.BLUE, lw=2.2, ms=4.5, label="純水")
    graph.plot(time, solution, "o-", color=F.RED, lw=2.2, ms=4.5, label="尿素水溶液")
    graph.axhline(0, color=F.BLUE, ls=":", lw=1.4)
    graph.scatter([4, 5], [-0.8, -0.1], color=F.PURPLE, zorder=5)
    graph.annotate("過冷最低點", (4, -0.8), xytext=(1.2, -3.3), arrowprops={"arrowstyle": "->", "color": F.PURPLE}, fontsize=10.4, color=F.PURPLE)
    graph.annotate("成核後釋放凝固潛熱", (5, -0.1), xytext=(5.8, 2.0), arrowprops={"arrowstyle": "->", "color": F.GREEN}, fontsize=10.4, color=F.GREEN)
    graph.annotate("溶劑結晶使剩餘液相變濃\n因此凝固段仍向下傾斜", (8.5, -2.35), xytext=(7.1, -5.1), arrowprops={"arrowstyle": "->", "color": F.RED}, fontsize=10.2, color=F.RED)
    graph.set_xlim(0, 12)
    graph.set_ylim(-6, 9)
    graph.set_xlabel("時間 / min")
    graph.set_ylabel("溫度 / °C")
    graph.grid(alpha=0.22)
    graph.legend(loc="upper right")
    graph.set_title("曲線形狀比單一最低點更能辨認凝固點", fontsize=13.2, weight="bold")
    fig.suptitle("凝固點實驗同時觀察相轉、過冷與液相組成改變", fontsize=16, y=0.985)
    fig.subplots_adjust(left=0.035, right=0.975, top=0.84, bottom=0.11, wspace=0.18)
    return _save(fig, "選化I-3-凝固點實驗與冷卻曲線.svg")


def fig_osmosis_reverse():
    """半透膜兩側的水化學勢、滲透流與逆滲透操作壓力。"""
    low_particles, high_particles = 3, 10
    osmotic_pressure = 24.5
    applied_pressure = 35.0
    assert high_particles > low_particles
    assert applied_pressure > osmotic_pressure

    fig, axes = plt.subplots(1, 2, figsize=(12.0, 6.2))
    panels = [
        (axes[0], "滲透", "水由低溶質粒子濃度側流向高濃度側", F.BLUE),
        (axes[1], "逆滲透", "在高濃度側施壓，水流向低濃度側", F.RED),
    ]
    for idx, (ax, title, note, color) in enumerate(panels):
        ax.axis("off")
        ax.set_xlim(-4.0, 4.0)
        ax.set_ylim(-3.0, 3.0)
        ax.add_patch(Rectangle((-3.45, -1.62), 6.90, 3.20, facecolor="#dbeafe", edgecolor=F.INK, lw=1.6))
        ax.add_patch(Rectangle((-0.12, -1.62), 0.24, 3.20, facecolor="#f8fafc", edgecolor=F.PURPLE, lw=1.5, hatch="////"))
        for i in range(low_particles):
            _particle(ax, -2.75 + 1.03 * (i % 2), -0.80 + 0.83 * (i // 2), F.AMBER, "+", radius=0.17)
        for i in range(high_particles):
            _particle(ax, 0.62 + 0.72 * (i % 4), -0.95 + 0.72 * (i // 4), F.AMBER, "+", radius=0.15)
        ax.text(-1.72, 1.93, "低溶質粒子濃度", ha="center", fontsize=10.7)
        ax.text(1.72, 1.93, "高溶質粒子濃度", ha="center", fontsize=10.7)
        ax.text(0, -2.03, "半透膜：允許水通過，截留溶質", ha="center", fontsize=10.5, color=F.PURPLE)
        if idx == 0:
            F.arrow(ax, (-2.10, 0.40), (1.55, 0.40), color=color, lw=3.0, mutation=18)
            ax.text(0, 0.78, "水的淨流", ha="center", fontsize=11.5, color=color, weight="bold")
            ax.text(0, -2.57, r"平衡時液柱壓差 $=\pi$", ha="center", fontsize=11.2, weight="bold")
        else:
            F.arrow(ax, (1.55, 0.35), (-2.10, 0.35), color=color, lw=3.0, mutation=18)
            F.arrow(ax, (2.25, 2.72), (2.25, 1.55), color=F.INK, lw=3.2, mutation=18)
            ax.text(2.25, 2.82, r"$P_{applied}=35.0\ bar$", ha="center", fontsize=10.8, weight="bold")
            ax.text(0, 0.75, "產水方向", ha="center", fontsize=11.5, color=color, weight="bold")
            ax.text(0, -2.57, r"$P_{applied}>\pi=24.5\ bar$", ha="center", fontsize=11.2, weight="bold")
        ax.set_title(title, fontsize=14, weight="bold")
        ax.text(0, -2.88, note, ha="center", fontsize=9.8, color="#475569")
    fig.suptitle("流動方向由半透膜選擇性與兩側水的化學勢決定", fontsize=16, y=0.985)
    fig.subplots_adjust(left=0.025, right=0.975, top=0.85, bottom=0.04, wspace=0.12)
    return _save(fig, "選化I-3-滲透與逆滲透.svg")


def fig_vant_hoff_particles():
    """理論離子數、測得 i 與離子對的粒子帳。"""
    species = [
        ("葡萄糖", 1.0, 1.00, [F.BLUE]),
        ("NaCl", 2.0, 1.90, [F.BLUE, F.AMBER]),
        ("K$_2$SO$_4$", 3.0, 2.70, [F.BLUE, F.BLUE, F.RED]),
    ]
    assert species[1][2] < species[1][1]
    assert species[2][2] < species[2][1]
    alpha_nacl = (species[1][2] - 1) / (species[1][1] - 1)
    assert np.isclose(alpha_nacl, 0.90)

    fig, axes = plt.subplots(1, 2, figsize=(12.0, 6.2), gridspec_kw={"width_ratios": [1.28, 0.92]})
    ax = axes[0]
    ax.axis("off")
    ax.set_xlim(-4.7, 4.7)
    ax.set_ylim(-3.0, 3.0)
    rows = [1.55, 0.0, -1.55]
    for y, (name, ideal_i, measured_i, colors) in zip(rows, species):
        _box(ax, (-4.45, y - 0.48), 2.05, 0.96, f"1 mol {name}\n化學式單位", face="#f8fafc", edge=F.INK, fs=10.7)
        F.arrow(ax, (-2.22, y), (-1.20, y), color=F.PURPLE, lw=1.8, mutation=11)
        for repeat in range(3):
            x0 = -0.75 + repeat * 1.48
            for j, color in enumerate(colors):
                _particle(ax, x0 + 0.29 * j, y, color, radius=0.14)
        ax.text(3.85, y + 0.17, f"$i_{{ideal}}={ideal_i:.0f}$", ha="center", fontsize=10.8, weight="bold")
        ax.text(3.85, y - 0.22, f"$i_{{meas}}={measured_i:.2f}$", ha="center", fontsize=10.4, color=F.RED)
    ax.text(0, 2.55, "解離後的獨立粒子數決定依數性", ha="center", fontsize=12, weight="bold")
    ax.text(0, -2.55, "測得 $i$ 偏小常表示離子對、水合與非理想作用\n使獨立運動的有效粒子數減少", ha="center", fontsize=10.5, color="#475569")

    graph = axes[1]
    labels = [s[0] for s in species]
    ideal_vals = [s[1] for s in species]
    measured_vals = [s[2] for s in species]
    positions = np.arange(3)
    width = 0.34
    graph.bar(positions - width / 2, ideal_vals, width, color="#cbd5e1", edgecolor=F.INK, label="理論 $i$")
    graph.bar(positions + width / 2, measured_vals, width, color=F.BLUE, alpha=0.82, label="測得 $i$")
    for x, value in zip(positions + width / 2, measured_vals):
        graph.text(x, value + 0.08, f"{value:.2f}", ha="center", fontsize=10.3, weight="bold")
    graph.set_xticks(positions, labels)
    graph.set_ylim(0, 3.4)
    graph.set_ylabel("凡特何夫因數 $i$")
    graph.grid(axis="y", alpha=0.22)
    graph.legend(fontsize=9.8, loc="upper left")
    _box(graph, (-0.43, 0.22), 1.85, 0.57, r"NaCl：$\alpha=\frac{i-1}{2-1}=0.90$", face="#f8fafc", edge=F.PURPLE, fs=10.4)
    fig.suptitle("凡特何夫因數把「配方中的式量單位」轉成「溶液中的有效粒子」", fontsize=15.5, y=0.985)
    fig.subplots_adjust(left=0.035, right=0.975, top=0.85, bottom=0.10, wspace=0.16)
    return _save(fig, "選化I-3-凡特何夫因數粒子帳.svg")


def main():
    for function_name, expected_filename in FIGURE_OUTPUTS:
        function = globals()[function_name]
        produced = function()
        produced_name = os.path.basename(produced) if isinstance(produced, str) else expected_filename
        assert produced_name == expected_filename, (function_name, produced_name, expected_filename)
    plt.close("all")


if __name__ == "__main__":
    main()
