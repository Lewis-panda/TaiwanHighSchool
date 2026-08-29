# -*- coding: utf-8 -*-
"""產生「選化 I-1 化學反應與能量」學生講義章內 SVG。

重繪：.venv/bin/python _tools/fig_content_選化I-1.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, FancyBboxPatch, Rectangle

import figlib as F


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CH = os.path.join(ROOT, "content", "選修化學I", "選化I-1")


FIGURE_OUTPUTS = (
    ("fig_limiting_reagent", "選化I-1-限量試劑粒子帳.svg"),
    ("fig_yield_cascade", "選化I-1-分步產率物料流.svg"),
    ("fig_energy_routes", "選化I-1-能量轉換路徑.svg"),
    ("fig_enthalpy_sign", "選化I-1-焓變符號與能階.svg"),
    ("fig_hess_routes", "選化I-1-赫斯定律路徑.svg"),
    ("fig_calorimetry", "選化I-1-量熱裝置與溫時資料.svg"),
    ("fig_standard_routes", "選化I-1-生成熱與燃燒熱路徑.svg"),
    ("fig_alkane_data", "選化I-1-烷類燃燒熱資料.svg"),
)


def _save(fig, filename):
    assert filename.endswith(".svg")
    return F.save_to(
        fig,
        CH,
        filename[:-4],
        output_subdir="assets",
        write_pdf=False,
    )


def _box(ax, xy, width, height, text, *, face="#f8fafc", edge="#64748b", fs=11.2, lw=1.6):
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


def _atom(ax, x, y, label, color, radius=0.18):
    ax.add_patch(Circle((x, y), radius, facecolor=color, edgecolor="white", lw=0.9, zorder=4))
    ax.text(x, y, label, ha="center", va="center", fontsize=7.8, color="white", weight="bold", zorder=5)


def fig_limiting_reagent():
    """以 2A+B→A2B 的離散粒子帳展示反應進度與剩餘量。"""
    initial_a = 8
    initial_b = 5
    nu_a, nu_b = 2, 1
    extent = min(initial_a // nu_a, initial_b // nu_b)
    left_a = initial_a - nu_a * extent
    left_b = initial_b - nu_b * extent
    products = extent
    assert (extent, left_a, left_b, products) == (4, 0, 1, 4)

    fig, axes = plt.subplots(1, 3, figsize=(12.0, 5.4), gridspec_kw={"width_ratios": [1.1, 0.85, 1.15]})
    titles = ["反應前", "可組成的反應包", "反應完成"]
    for ax, title in zip(axes, titles):
        ax.axis("off")
        ax.set_xlim(-3.0, 3.0)
        ax.set_ylim(-2.5, 2.5)
        ax.set_title(title, fontsize=14, weight="bold")

    left = axes[0]
    a_points = [(-2.15 + 0.72 * (i % 4), 1.05 - 0.72 * (i // 4)) for i in range(initial_a)]
    b_points = [(-1.75 + 0.88 * i, -1.15) for i in range(initial_b)]
    for x, y in a_points:
        _atom(left, x, y, "A", F.BLUE)
    for x, y in b_points:
        _atom(left, x, y, "B", F.AMBER)
    left.text(0, 1.95, "$n_A=8$；$n_B=5$", ha="center", fontsize=12)
    left.text(0, -1.85, "$n_A/2=4$，$n_B/1=5$", ha="center", fontsize=12, weight="bold")

    middle = axes[1]
    for j, y in enumerate(np.linspace(1.35, -1.35, extent)):
        _box(middle, (-1.45, y - 0.27), 2.9, 0.54, f"第 {j + 1} 包：2A＋B", face="#eef4ff", edge=F.BLUE, fs=10.8)
    middle.text(0, 2.02, "較小的商決定 4 包", ha="center", fontsize=11.5, color=F.RED, weight="bold")

    right = axes[2]
    product_centers = [(-1.65, 0.90), (0.25, 0.90), (-1.65, -0.35), (0.25, -0.35)]
    for x, y in product_centers:
        _atom(right, x - 0.25, y, "A", F.BLUE)
        _atom(right, x + 0.12, y + 0.16, "A", F.BLUE)
        _atom(right, x + 0.12, y - 0.16, "B", F.AMBER)
        right.plot([x - 0.08, x + 0.02], [y, y + 0.11], color=F.INK, lw=1.2, zorder=2)
        right.plot([x - 0.08, x + 0.02], [y, y - 0.11], color=F.INK, lw=1.2, zorder=2)
    _atom(right, 2.05, -1.35, "B", F.AMBER)
    right.text(0, 1.95, "$4A_2B$ 生成，$1B$ 剩餘", ha="center", fontsize=12, weight="bold")
    right.text(0, -1.95, "A 是限量試劑；反應進度 $\\xi=4$", ha="center", fontsize=11.6, color=F.RED)
    fig.suptitle("係數把反應物分成固定比例的反應包；最先用完者決定產物上限", fontsize=16, y=0.98)
    fig.subplots_adjust(left=0.025, right=0.975, top=0.82, bottom=0.06, wspace=0.08)
    return _save(fig, "選化I-1-限量試劑粒子帳.svg")


def fig_yield_cascade():
    """以兩步反應的莫耳流展示各步與總產率。"""
    feed = 1.00
    step1_yield = 0.80
    step2_yield = 0.75
    intermediate = feed * step1_yield
    product = intermediate * step2_yield
    overall = product / feed
    assert np.isclose(intermediate, 0.80)
    assert np.isclose(product, 0.60)
    assert np.isclose(overall, step1_yield * step2_yield)

    fig, ax = plt.subplots(figsize=(11.8, 5.8))
    ax.axis("off")
    ax.set_xlim(-6.0, 6.0)
    ax.set_ylim(-3.0, 3.0)
    stages = [
        (-5.2, 1.0, "起始物 A\n$1.00\\ mol$", F.BLUE),
        (-1.25, 0.80, "中間物 B\n$0.80\\ mol$", F.AMBER),
        (3.15, 0.60, "目標產物 C\n$0.60\\ mol$", F.GREEN),
    ]
    for x, amount, label, color in stages:
        height = 1.9 * amount
        ax.add_patch(Rectangle((x, -height / 2), 1.75, height, facecolor=color, edgecolor="white", alpha=0.82))
        ax.text(x + 0.875, 0, label, ha="center", va="center", fontsize=12, color="white", weight="bold")
    F.arrow(ax, (-3.35, 0.52), (-1.45, 0.42), color=F.INK, lw=2.2, mutation=16)
    F.arrow(ax, (0.65, 0.36), (2.92, 0.25), color=F.INK, lw=2.2, mutation=16)
    ax.text(-2.35, 1.06, "第 1 步產率 80%", ha="center", fontsize=12, weight="bold")
    ax.text(1.78, 0.88, "第 2 步產率 75%", ha="center", fontsize=12, weight="bold")
    _box(ax, (-4.65, -2.25), 9.30, 0.80, "總產率 $=0.80\\times0.75=0.60=60\\%$；各步損失依序作用在當步投入量。", face="#f8fafc", edge=F.PURPLE, fs=12.2)
    ax.text(-0.35, 2.35, "理論莫耳數以 1:1:1 為基準", ha="center", fontsize=11, color="#475569")
    fig.suptitle("分步反應的總產率是各步分率的乘積", fontsize=16, y=0.98)
    fig.subplots_adjust(left=0.025, right=0.975, top=0.84, bottom=0.04)
    return _save(fig, "選化I-1-分步產率物料流.svg")


def fig_energy_routes():
    """以三條真實裝置路徑區分能量形式、轉換與散逸。"""
    efficiencies = [0.90, 0.42, 0.78]
    assert all(0 < value <= 1 for value in efficiencies)
    fig, axes = plt.subplots(1, 3, figsize=(12.0, 6.0))
    panels = [
        ("水力發電", ["高處水的\n重力位能", "水流動能", "渦輪機\n機械能", "發電機\n電能"], F.BLUE, "輸電前示意效率 90%"),
        ("燃氣發電", ["燃料\n化學能", "高溫氣體\n內能", "渦輪機\n機械能", "發電機\n電能"], F.RED, "示意電效率 42%"),
        ("電池供電", ["反應物\n化學能", "電荷分離的\n電位能", "外電路\n電能", "馬達\n機械能"], F.GREEN, "電池到馬達示意效率 78%"),
    ]
    for ax, (title, stages, color, note) in zip(axes, panels):
        ax.axis("off")
        ax.set_xlim(-2.8, 2.8)
        ax.set_ylim(-3.0, 3.0)
        ys = [2.05, 0.88, -0.29, -1.46]
        for i, (y, label) in enumerate(zip(ys, stages)):
            _box(ax, (-1.85, y - 0.37), 3.70, 0.74, label, face="#f8fafc", edge=color, fs=10.8)
            if i < 3:
                F.arrow(ax, (0, y - 0.40), (0, ys[i + 1] + 0.42), color=color, lw=1.9, mutation=12)
        ax.text(0, -2.35, note, ha="center", fontsize=10.8, color=color, weight="bold")
        ax.text(0, -2.72, "差額進入周圍環境的熱與聲", ha="center", fontsize=9.9, color="#475569")
        ax.set_title(title, fontsize=14, weight="bold")
    fig.suptitle("裝置只轉換與傳遞能量；輸入、有效輸出與周圍能量共同守恆", fontsize=16, y=0.985)
    fig.subplots_adjust(left=0.02, right=0.98, top=0.85, bottom=0.04, wspace=0.07)
    return _save(fig, "選化I-1-能量轉換路徑.svg")


def fig_enthalpy_sign():
    """用同一參考軸顯示放熱與吸熱的 ΔH 符號。"""
    h_exo_r, h_exo_p = 120.0, 40.0
    h_endo_r, h_endo_p = 30.0, 95.0
    d_exo = h_exo_p - h_exo_r
    d_endo = h_endo_p - h_endo_r
    assert d_exo == -80.0
    assert d_endo == 65.0

    fig, axes = plt.subplots(1, 2, figsize=(11.8, 6.0))
    datasets = [
        (axes[0], h_exo_r, h_exo_p, d_exo, "放熱反應", F.RED),
        (axes[1], h_endo_r, h_endo_p, d_endo, "吸熱反應", F.BLUE),
    ]
    for ax, hr, hp, delta, title, color in datasets:
        ax.set_xlim(0, 5)
        ax.set_ylim(0, 140)
        ax.set_xticks([])
        ax.set_ylabel("系統焓 $H$（共同參考）")
        ax.grid(axis="y", alpha=0.20)
        ax.spines[["top", "right", "bottom"]].set_visible(False)
        ax.hlines(hr, 0.55, 2.00, color=F.INK, lw=3)
        ax.hlines(hp, 3.00, 4.45, color=color, lw=3)
        ax.text(1.28, hr + 6, "反應物", ha="center", fontsize=12, weight="bold")
        ax.text(3.72, hp + 6, "生成物", ha="center", fontsize=12, weight="bold", color=color)
        F.arrow(ax, (2.10, hr), (2.90, hp), color=color, lw=2.3, mutation=15)
        ax.text(2.50, (hr + hp) / 2, f"$\\Delta H={delta:+.0f}$", ha="center", va="center", fontsize=12, color=color, weight="bold", bbox={"facecolor": "white", "edgecolor": "none", "pad": 1.5})
        heat_direction = "系統把熱傳給環境" if delta < 0 else "環境把熱傳給系統"
        _box(ax, (0.52, 5.0), 3.96, 20.0, heat_direction, face="#f8fafc", edge=color, fs=11.5)
        ax.set_title(title, fontsize=14, weight="bold")
    fig.suptitle("反應焓以系統為記帳對象：$\\Delta H=H_{products}-H_{reactants}$", fontsize=16, y=0.985)
    fig.subplots_adjust(left=0.075, right=0.975, top=0.85, bottom=0.08, wspace=0.24)
    return _save(fig, "選化I-1-焓變符號與能階.svg")


def fig_hess_routes():
    """以碳氧化的兩條焓路徑驗證赫斯定律。"""
    direct = -393.5
    step1 = -110.5
    step2 = -283.0
    assert np.isclose(step1 + step2, direct)
    h_top = 0.0
    h_mid = step1
    h_bottom = direct

    fig, ax = plt.subplots(figsize=(10.8, 6.3))
    ax.set_xlim(-1.1, 10.5)
    ax.set_ylim(-440, 55)
    ax.set_xticks([])
    ax.set_ylabel(r"相對焓／$\mathrm{kJ\,mol^{-1}}$")
    ax.grid(axis="y", alpha=0.20)
    ax.spines[["top", "right", "bottom"]].set_visible(False)
    levels = [
        (h_top, 0.40, 4.15, r"$C(s,\ graphite)+O_2(g)$", F.INK),
        (h_mid, 5.60, 9.65, r"$CO(g)+\frac{1}{2}O_2(g)$", F.AMBER),
        (h_bottom, 3.10, 7.50, r"$CO_2(g)$", F.GREEN),
    ]
    for y, x0, x1, label, color in levels:
        ax.hlines(y, x0, x1, color=color, lw=3)
        ax.text((x0 + x1) / 2, y + 17, label, ha="center", fontsize=12.5, color=color, weight="bold")
    F.arrow(ax, (2.10, h_top - 8), (4.15, h_bottom + 10), color=F.RED, lw=2.6, mutation=17)
    ax.text(1.85, -210, "$\\Delta H_1=-393.5$", ha="center", fontsize=11.5, color=F.RED, weight="bold")
    F.arrow(ax, (4.25, h_top - 5), (6.35, h_mid + 8), color=F.BLUE, lw=2.3, mutation=15)
    ax.text(5.55, -48, "$\\Delta H_2=-110.5$", ha="center", fontsize=11.2, color=F.BLUE, weight="bold")
    F.arrow(ax, (7.55, h_mid - 7), (5.90, h_bottom + 8), color=F.AMBER, lw=2.3, mutation=15)
    ax.text(8.35, -250, "$\\Delta H_3=-283.0$", ha="center", fontsize=11.2, color=F.AMBER, weight="bold")
    _box(ax, (0.55, -431), 9.10, 44, r"$-110.5+(-283.0)=-393.5\ \mathrm{kJ\,mol^{-1}}$", face="#f8fafc", edge=F.PURPLE, fs=13)
    fig.suptitle("相同初態與終態具有相同焓變；可行反應路徑的焓變直接相加", fontsize=16, y=0.985)
    fig.subplots_adjust(left=0.09, right=0.975, top=0.87, bottom=0.08)
    return _save(fig, "選化I-1-赫斯定律路徑.svg")


def fig_calorimetry():
    """畫出咖啡杯量熱器與兩組可運算的溫度—時間資料。"""
    neutral_t = np.array([0, 15, 30, 45, 60, 75, 90, 120, 150, 210, 270, 330], dtype=float)
    neutral_temp = np.array([22.0, 22.0, 22.0, 27.6, 28.1, 28.2, 28.2, 28.1, 28.0, 27.8, 27.5, 27.2])
    dissolve_t = np.array([0, 30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330], dtype=float)
    dissolve_temp = np.array([22.0, 22.0, 22.0, 20.9, 19.9, 19.7, 19.6, 19.5, 19.5, 19.4, 19.4, 19.4])
    assert np.isclose(neutral_temp.max() - 22.0, 6.2)
    assert np.isclose(22.0 - dissolve_temp.min(), 2.6)
    assert neutral_temp.argmax() in (3, 4, 5, 6)

    fig, axes = plt.subplots(1, 2, figsize=(12.0, 6.4), gridspec_kw={"width_ratios": [0.82, 1.18]})
    left, right = axes
    left.axis("off")
    left.set_xlim(-3.2, 3.2)
    left.set_ylim(-3.1, 3.1)
    # 外杯、內杯、杯蓋與溫度探針
    left.add_patch(Rectangle((-1.55, -1.75), 3.10, 3.15, facecolor="#f1f5f9", edgecolor="#64748b", lw=2.0))
    left.add_patch(Rectangle((-1.28, -1.52), 2.56, 2.55, facecolor="#dbeafe", edgecolor=F.BLUE, lw=1.6))
    left.add_patch(Rectangle((-1.75, 1.10), 3.50, 0.32, facecolor="#e2e8f0", edgecolor="#64748b", lw=1.5))
    left.plot([0.52, 0.52], [2.30, -0.82], color=F.RED, lw=3.0)
    left.add_patch(Circle((0.52, -0.93), 0.16, facecolor=F.RED, edgecolor="white"))
    left.plot([-0.38, -0.08], [2.10, -0.35], color=F.INK, lw=2.0)
    left.text(-2.15, 2.50, "溫度探針", fontsize=10.7, color=F.RED)
    F.arrow(left, (-1.18, 2.35), (0.36, 2.05), color=F.RED, lw=1.3, mutation=10)
    left.text(-2.55, -2.20, "兩層保麗龍杯＋杯蓋", fontsize=11.2)
    F.arrow(left, (-1.15, -2.05), (-0.98, -1.38), color=F.BLUE, lw=1.4, mutation=10)
    left.text(0, -0.20, "反應溶液", ha="center", fontsize=12, color=F.BLUE, weight="bold")
    _box(left, (-2.70, -2.94), 5.40, 0.53, "持續攪拌；讀取反應後極值或外推混合時刻溫度", face="#fff7dd", edge=F.AMBER, fs=10.6)
    left.set_title("定壓溶液量熱器", fontsize=14, weight="bold")

    right.plot(neutral_t, neutral_temp, "o-", color=F.RED, lw=2.0, ms=4.2, label="中和反應")
    right.plot(dissolve_t, dissolve_temp, "s-", color=F.BLUE, lw=2.0, ms=4.0, label="$KNO_3$ 溶解")
    right.axvline(30, color="#64748b", lw=1.3, ls="--")
    right.text(34, 28.6, "加入／混合", fontsize=10.5, color="#475569")
    right.annotate("最高 $28.2^\\circ C$", xy=(75, 28.2), xytext=(145, 29.1), arrowprops={"arrowstyle": "->", "color": F.RED}, color=F.RED, fontsize=10.8)
    right.annotate("最低 $19.4^\\circ C$", xy=(300, 19.4), xytext=(175, 18.4), arrowprops={"arrowstyle": "->", "color": F.BLUE}, color=F.BLUE, fontsize=10.8)
    right.set_xlim(0, 340)
    right.set_ylim(17.5, 30.0)
    right.set_xlabel("時間／s")
    right.set_ylabel("溫度／$^\\circ C$")
    right.grid(alpha=0.22)
    right.spines[["top", "right"]].set_visible(False)
    right.legend(loc="center right", frameon=False)
    right.set_title("同一裝置的兩種熱流方向", fontsize=14, weight="bold")
    fig.suptitle("溫度變化先給出溶液吸放熱，再以 $q_{rxn}\\approx-q_{solution}$ 換成反應焓", fontsize=16, y=0.985)
    fig.subplots_adjust(left=0.03, right=0.975, top=0.86, bottom=0.10, wspace=0.16)
    return _save(fig, "選化I-1-量熱裝置與溫時資料.svg")


def fig_standard_routes():
    """以共同參考態串連生成焓公式與燃燒循環。"""
    hf_co2 = -393.5
    hf_h2o = -285.8
    hf_methanol = -238.7
    dh_comb = hf_co2 + 2 * hf_h2o - hf_methanol
    assert np.isclose(dh_comb, -726.4)

    fig, axes = plt.subplots(1, 2, figsize=(12.0, 6.4))
    for ax in axes:
        ax.axis("off")
        ax.set_xlim(-3.2, 3.2)
        ax.set_ylim(-3.0, 3.0)
    left, right = axes
    _box(left, (-2.75, 1.45), 5.50, 0.88, r"標準態元素：$C(s,graphite)+2H_2(g)+\frac{1}{2}O_2(g)$", face="#f8fafc", edge=F.INK, fs=11.6)
    _box(left, (-2.15, -0.05), 4.30, 0.88, r"$CH_3OH(l)$", face="#eef4ff", edge=F.BLUE, fs=13)
    F.arrow(left, (0, 1.40), (0, 0.88), color=F.BLUE, lw=2.5, mutation=15)
    left.text(1.62, 0.84, "$\\Delta H_f^\\circ=-238.7$", fontsize=11.4, color=F.BLUE, weight="bold")
    _box(left, (-2.75, -1.70), 5.50, 0.88, "$\\Delta H_f^\\circ$ 以『由標準態元素生成 1 mol 化合物』定義\n標準態元素本身的 $\\Delta H_f^\\circ=0$", face="#e9f8ef", edge=F.GREEN, fs=10.9)
    left.set_title("莫耳生成熱的共同零點", fontsize=14, weight="bold")

    _box(right, (-2.55, 1.63), 5.10, 0.77, r"$CH_3OH(l)+\frac{3}{2}O_2(g)$", face="#eef4ff", edge=F.BLUE, fs=12.5)
    _box(right, (-2.55, -1.80), 5.10, 0.77, r"$CO_2(g)+2H_2O(l)$", face="#e9f8ef", edge=F.GREEN, fs=12.5)
    F.arrow(right, (-1.55, 1.57), (-1.55, -0.95), color=F.RED, lw=2.5, mutation=16)
    right.text(-2.85, 0.05, "$\\Delta H_c^\\circ$", fontsize=12, color=F.RED, weight="bold")
    _box(right, (-0.45, -0.10), 2.80, 0.96, r"$[-393.5+2(-285.8)]$" + "\n" + r"$-[-238.7]=-726.4$", face="#fff7dd", edge=F.AMBER, fs=11.3)
    right.text(0, -2.48, "生成物總生成焓－反應物總生成焓", ha="center", fontsize=11.2, color=F.PURPLE, weight="bold")
    right.set_title("用生成焓計算燃燒焓", fontsize=14, weight="bold")
    fig.suptitle("標準生成焓建立共同參考；反應焓是終態總和減初態總和", fontsize=16, y=0.985)
    fig.subplots_adjust(left=0.025, right=0.975, top=0.86, bottom=0.05, wspace=0.10)
    return _save(fig, "選化I-1-生成熱與燃燒熱路徑.svg")


def fig_alkane_data():
    """從烷類燃燒焓資料估算每增加一個 CH2 的能量增量。"""
    carbon = np.arange(1, 7, dtype=float)
    dh = np.array([-890.3, -1560.0, -2220.0, -2877.0, -3536.0, -4195.0])
    slope, intercept = np.polyfit(carbon, dh, 1)
    predicted_c7 = slope * 7 + intercept
    assert -670 < slope < -650
    assert -4870 < predicted_c7 < -4840
    increments = np.diff(dh)
    assert np.max(np.abs(increments - increments.mean())) < 12

    fig, axes = plt.subplots(1, 2, figsize=(11.8, 6.2), gridspec_kw={"width_ratios": [1.15, 0.85]})
    left, right = axes
    left.scatter(carbon, dh, s=62, color=F.BLUE, zorder=4, label="資料")
    xfit = np.linspace(0.8, 7.2, 100)
    left.plot(xfit, slope * xfit + intercept, color=F.RED, lw=2.0, label="線性趨勢")
    left.scatter([7], [predicted_c7], marker="x", s=85, color=F.RED, zorder=5)
    left.annotate(f"外插 C7：約 {predicted_c7:.0f}", xy=(7, predicted_c7), xytext=(4.2, -4660), arrowprops={"arrowstyle": "->", "color": F.RED}, fontsize=10.8, color=F.RED)
    left.set_xlabel("每個烷分子的碳原子數")
    left.set_ylabel(r"$\Delta H_c^\circ$／$\mathrm{kJ\,mol^{-1}}$")
    left.set_xticks(range(1, 8))
    left.grid(alpha=0.22)
    left.spines[["top", "right"]].set_visible(False)
    left.legend(frameon=False, loc="upper right")
    left.set_title("同系物的莫耳燃燒焓", fontsize=14, weight="bold")

    right.axis("off")
    right.set_xlim(-3.0, 3.0)
    right.set_ylim(-3.0, 3.0)
    slope_text = rf"最佳直線斜率 $\approx {slope:.0f}$" + "\n" + r"$\mathrm{kJ\,mol^{-1}}$／每個碳"
    _box(right, (-2.55, 1.55), 5.10, 0.84, slope_text, face="#eef4ff", edge=F.BLUE, fs=11.8)
    _box(right, (-2.55, 0.15), 5.10, 0.90, "每增加一個 $CH_2$，完全燃燒時\n釋出的能量約增加 $660\\ kJ\\,mol^{-1}$", face="#fff7dd", edge=F.AMBER, fs=11.5)
    _box(right, (-2.55, -1.40), 5.10, 1.02, "莫耳值比較每 mol 分子；\n" + r"燃料質量比較需再除以莫耳質量，得到 $\mathrm{kJ\,g^{-1}}$。", face="#e9f8ef", edge=F.GREEN, fs=11.2)
    right.text(0, -2.38, "圖上趨勢提供估計；表列量測值提供計算依據", ha="center", fontsize=10.7, color="#475569")
    fig.suptitle("同系物資料近似線性；斜率與比較基準決定可說出的結論", fontsize=16, y=0.985)
    fig.subplots_adjust(left=0.07, right=0.975, top=0.86, bottom=0.10, wspace=0.14)
    return _save(fig, "選化I-1-烷類燃燒熱資料.svg")


def main():
    for entrypoint, filename in FIGURE_OUTPUTS:
        assert entrypoint in globals(), f"缺少圖形函式：{entrypoint}"
        globals()[entrypoint]()
        expected = os.path.join(CH, "assets", filename)
        assert os.path.exists(expected), f"圖檔未產生：{expected}"


if __name__ == "__main__":
    main()
