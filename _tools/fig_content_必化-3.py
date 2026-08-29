# -*- coding: utf-8 -*-
"""產生「必化-3 溶液與常見的化學反應」學生講義章內 SVG。

重繪：.venv/bin/python _tools/fig_content_必化-3.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, FancyBboxPatch, Polygon, Rectangle

import figlib as F


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CH = os.path.join(ROOT, "content", "必修化學", "必化-3")


FIGURE_OUTPUTS = (
    ("fig_dispersion_scale", "必化-3-分散粒徑與光路.svg"),
    ("fig_concentration_preparation", "必化-3-濃度與定量配製.svg"),
    ("fig_solubility_curve", "必化-3-溶解度曲線與結晶.svg"),
    ("fig_dynamic_equilibrium", "必化-3-飽和溶液動態平衡.svg"),
    ("fig_acid_base_particles", "必化-3-強弱酸鹼粒子模型.svg"),
    ("fig_ph_indicators", "必化-3-pH與指示劑範圍.svg"),
    ("fig_neutralization_ledger", "必化-3-中和反應粒子帳.svg"),
    ("fig_redox_transfer", "必化-3-氧化還原電子轉移.svg"),
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


def _box(ax, xy, width, height, text, face="#f8fafc", edge="#64748b", fs=11.5):
    patch = FancyBboxPatch(
        xy,
        width,
        height,
        boxstyle="round,pad=0.035,rounding_size=0.10",
        facecolor=face,
        edgecolor=edge,
        lw=1.7,
    )
    ax.add_patch(patch)
    ax.text(xy[0] + width / 2, xy[1] + height / 2, text, ha="center", va="center", fontsize=fs)
    return patch


def _particle(ax, x, y, label, color, radius=0.12, edge="white", text_color="white", z=5):
    patch = Circle((x, y), radius, facecolor=color, edgecolor=edge, lw=1.0, zorder=z)
    ax.add_patch(patch)
    if label:
        ax.text(x, y, label, ha="center", va="center", fontsize=7.5, color=text_color, weight="bold", zorder=z + 1)
    return patch


def _beaker(ax, x, y, width=2.4, height=2.4, liquid_height=1.75, liquid="#dbeafe"):
    ax.add_patch(Rectangle((x, y), width, liquid_height, facecolor=liquid, edgecolor="none", alpha=0.75, zorder=0))
    ax.plot([x, x, x + width, x + width], [y + height, y, y, y + height], color="#475569", lw=2.0, zorder=3)
    ax.plot([x + 0.05, x + width - 0.05], [y + liquid_height, y + liquid_height], color=F.BLUE, lw=1.4, zorder=2)


def fig_dispersion_scale():
    """比較真溶液、膠體與懸浮液的粒徑、光路和重力行為。"""
    fig, axes = plt.subplots(1, 3, figsize=(12.0, 5.9))
    categories = [
        ("真溶液", "粒徑 < 1 nm", 0.045, F.BLUE, "光束路徑不可見\n久置不沉降"),
        ("膠體", "1–1000 nm", 0.105, F.PURPLE, "散射形成明亮光路\n久置通常不沉降"),
        ("懸浮液", "粒徑 > 1000 nm", 0.165, F.AMBER, "強烈散射／遮光\n久置會沉降"),
    ]
    for idx, (title, scale, radius, color, conclusion) in enumerate(categories):
        ax = axes[idx]
        ax.set_aspect("equal")
        ax.axis("off")
        ax.set_xlim(-2.2, 2.2)
        ax.set_ylim(-2.6, 2.7)
        _beaker(ax, -1.45, -1.15, width=2.9, height=2.7, liquid_height=2.0)
        coords = [(-1.05, 0.25), (-0.55, -0.55), (0.0, 0.7), (0.55, -0.25), (1.02, 0.42), (-0.1, -0.72)]
        if idx == 2:
            coords = [(-1.0, -0.7), (-0.48, -0.65), (0.1, -0.72), (0.68, -0.62), (1.02, -0.76)]
        for x, y in coords:
            _particle(ax, x, y, "", color, radius=radius, edge="#334155")
        ax.add_patch(Polygon([(-2.05, 0.75), (-1.48, 0.56), (-1.48, 0.94)], closed=True, facecolor="#fde68a", edgecolor=F.AMBER, lw=1.3))
        beam_alpha = 0.14 if idx == 0 else (0.55 if idx == 1 else 0.82)
        ax.add_patch(Rectangle((-1.45, 0.61), 2.9, 0.25, facecolor="#facc15", edgecolor="none", alpha=beam_alpha, zorder=1))
        if idx >= 1:
            for x, y in coords:
                if 0.45 < y < 0.95:
                    ax.plot([x - 0.15, x + 0.15], [y - 0.15, y + 0.15], color="#f59e0b", lw=1.3)
                    ax.plot([x - 0.15, x + 0.15], [y + 0.15, y - 0.15], color="#f59e0b", lw=1.3)
        ax.text(0, 2.27, title, ha="center", fontsize=14, weight="bold")
        ax.text(0, 1.88, scale, ha="center", fontsize=11.2, color="#475569")
        ax.text(0, -1.70, conclusion, ha="center", va="center", fontsize=11.2)
    lower_nm, upper_nm = 1.0, 1000.0
    assert lower_nm == 1.0 and upper_nm / lower_nm == 1000.0
    fig.suptitle("粒徑決定光的散射與沉降行為", fontsize=16, y=0.98)
    fig.subplots_adjust(left=0.025, right=0.975, top=0.87, bottom=0.04, wspace=0.08)
    return _save(fig, "必化-3-分散粒徑與光路.svg")


def fig_concentration_preparation():
    """以 0.200 M NaCl 250.0 mL 展示濃度資料與定量配製。"""
    target_c = 0.200
    target_v = 0.2500
    molar_mass = 58.44
    moles = target_c * target_v
    mass = moles * molar_mass
    assert np.isclose(moles, 0.05000)
    assert np.isclose(mass, 2.922)

    fig, ax = F.schematic(12.0, 6.2)
    ax.set_xlim(-6.0, 6.0)
    ax.set_ylim(-3.1, 3.1)
    _box(ax, (-5.55, 1.45), 2.65, 1.05, "目標\n$0.200\\ \\mathrm{M}$ NaCl\n$250.0\\ \\mathrm{mL}$", face="#fff7dd", edge=F.AMBER, fs=12.2)
    _box(ax, (-2.28, 1.45), 2.65, 1.05, "$n=CV$\n$=0.200(0.2500)$\n$=0.05000\\ \\mathrm{mol}$", face="#eef4ff", edge=F.BLUE, fs=12.2)
    _box(ax, (1.00, 1.45), 2.65, 1.05, "$m=nM$\n$=0.05000(58.44)$\n$=2.922\\ \\mathrm{g}$", face="#e9f8ef", edge=F.GREEN, fs=12.2)
    _box(ax, (4.27, 1.45), 1.30, 1.05, "量得\n溶質質量", face="#f1ecff", edge=F.PURPLE, fs=12)
    for x1, x2, color in [(-2.78, -2.40, F.BLUE), (0.48, 0.88, F.GREEN), (3.77, 4.15, F.PURPLE)]:
        F.arrow(ax, (x1, 1.98), (x2, 1.98), color=color, lw=2.0, mutation=14)

    steps = [
        (-5.55, -0.75, 2.10, "① 燒杯中溶解\n體積尚未定容", F.BLUE),
        (-2.75, -0.75, 2.10, "② 定量轉移\n洗液一併轉入", F.GREEN),
        (0.05, -0.75, 2.10, "③ 冷卻至室溫\n加水接近刻度", F.PURPLE),
        (2.85, -0.75, 2.10, "④ 滴至凹液面\n最低點切刻度", F.AMBER),
    ]
    for x, y, w, label, color in steps:
        _box(ax, (x, y), w, 1.25, label, face="#f8fafc", edge=color, fs=11.2)
    for x1, x2 in [(-3.34, -2.87), (-0.54, -0.07), (2.26, 2.73)]:
        F.arrow(ax, (x1, -0.12), (x2, -0.12), color="#64748b", lw=1.7, mutation=12)
    _box(ax, (-2.85, -2.55), 5.70, 0.78, "⑤ 塞緊後倒轉混合；最終體積是溶液體積，不是先量 $250.0\\ \\mathrm{mL}$ 水。", face="#fff1e6", edge=F.RED, fs=11.4)
    ax.text(0, 0.93, "$C=n/V_{\\mathrm{solution}}$；容量瓶只在校正溫度附近提供標示體積", ha="center", fontsize=11.5, color="#475569")
    fig.suptitle("莫耳濃度先決定莫耳數，再由容量瓶決定溶液體積", fontsize=16, y=0.98)
    fig.subplots_adjust(left=0.025, right=0.975, top=0.88, bottom=0.04)
    return _save(fig, "必化-3-濃度與定量配製.svg")


def fig_solubility_curve():
    """由一組原創資料畫溶解度曲線並標示冷卻結晶量。"""
    temperatures = np.array([20, 30, 40, 50, 60, 70], dtype=float)
    solubilities = np.array([24, 31, 40, 52, 68, 87], dtype=float)
    assert np.all(np.diff(temperatures) > 0)
    assert np.all(np.diff(solubilities) > 0)
    s60 = float(solubilities[temperatures == 60][0])
    s30 = float(solubilities[temperatures == 30][0])
    solvent_mass = 150.0
    dissolved_60 = s60 / 100.0 * solvent_mass
    dissolved_30 = s30 / 100.0 * solvent_mass
    crystallized = dissolved_60 - dissolved_30
    assert np.isclose(dissolved_60, 102.0)
    assert np.isclose(dissolved_30, 46.5)
    assert np.isclose(crystallized, 55.5)

    fig, axes = plt.subplots(1, 2, figsize=(12.0, 5.7), gridspec_kw={"width_ratios": [1.2, 0.9]})
    ax, ledger = axes
    ax.plot(temperatures, solubilities, marker="o", color=F.BLUE, lw=2.5, ms=6.5)
    ax.fill_between(temperatures, 0, solubilities, color="#dbeafe", alpha=0.65)
    ax.scatter([60, 30], [s60, s30], s=85, color=[F.RED, F.GREEN], zorder=5)
    ax.plot([30, 60], [s60, s60], ls="--", color=F.RED, lw=1.4)
    ax.plot([30, 30], [s30, s60], ls="--", color=F.GREEN, lw=1.4)
    ax.annotate("60 °C 飽和：68 g/100 g 水", (60, s60), xytext=(40, 78), arrowprops=dict(arrowstyle="->", color=F.RED), fontsize=10.5, color=F.RED)
    ax.annotate("30 °C 飽和：31 g/100 g 水", (30, s30), xytext=(36, 22), arrowprops=dict(arrowstyle="->", color=F.GREEN), fontsize=10.5, color=F.GREEN)
    ax.set_xlabel("溫度（°C）")
    ax.set_ylabel("溶解度（g 溶質 / 100 g 水）")
    ax.set_xlim(18, 72)
    ax.set_ylim(0, 100)
    ax.grid(True, alpha=0.22)
    ax.set_title("曲線上的點：該溫度的飽和組成", fontsize=13.5)

    ledger.axis("off")
    ledger.set_xlim(0, 1)
    ledger.set_ylim(0, 1)
    _box(ledger, (0.06, 0.69), 0.88, 0.22, "固定水量：$150.0\\ \\mathrm{g}$\n升降溫時先追蹤溶劑質量", face="#fff7dd", edge=F.AMBER, fs=11.5)
    _box(ledger, (0.06, 0.42), 0.88, 0.20, "$60\\,^\\circ\\mathrm{C}$ 可溶\n$150(68/100)=102.0\\ \\mathrm{g}$", face="#fff1e6", edge=F.RED, fs=11.5)
    _box(ledger, (0.06, 0.17), 0.88, 0.18, "$30\\,^\\circ\\mathrm{C}$ 留在溶液\n$150(31/100)=46.5\\ \\mathrm{g}$", face="#e9f8ef", edge=F.GREEN, fs=11.5)
    ledger.text(0.5, 0.055, "析晶 $=102.0-46.5=55.5\\ \\mathrm{g}$", ha="center", fontsize=12.3, weight="bold", color=F.PURPLE)
    fig.suptitle("冷卻結晶以同一份溶劑為基準比較兩個溫度的可溶量", fontsize=16, y=0.98)
    fig.subplots_adjust(left=0.075, right=0.975, top=0.86, bottom=0.12, wspace=0.20)
    return _save(fig, "必化-3-溶解度曲線與結晶.svg")


def fig_dynamic_equilibrium():
    """顯示飽和溶液中溶解與結晶速率相等，而非粒子停止。"""
    fig, ax = F.schematic(11.8, 5.8)
    ax.set_xlim(-5.9, 5.9)
    ax.set_ylim(-2.9, 2.9)
    _beaker(ax, -4.9, -1.55, width=4.0, height=3.5, liquid_height=2.65, liquid="#dbeafe")
    dissolved = [(-4.45, 0.55), (-3.75, 0.15), (-3.05, 0.72), (-2.35, 0.25), (-1.55, 0.63), (-4.1, -0.48), (-2.85, -0.38), (-1.75, -0.55)]
    for i, (x, y) in enumerate(dissolved):
        _particle(ax, x, y, "+" if i % 2 == 0 else "−", F.BLUE if i % 2 == 0 else F.RED, radius=0.16)
    crystal_positions = [(-4.2, -1.32), (-3.75, -1.32), (-3.30, -1.32), (-2.85, -1.32), (-2.40, -1.32), (-3.98, -0.96), (-3.53, -0.96), (-3.08, -0.96), (-2.63, -0.96)]
    for i, (x, y) in enumerate(crystal_positions):
        _particle(ax, x, y, "+" if i % 2 == 0 else "−", F.BLUE if i % 2 == 0 else F.RED, radius=0.16)
    F.arrow(ax, (-3.55, -0.84), (-3.55, 0.08), color=F.GREEN, lw=2.4, mutation=15)
    F.arrow(ax, (-2.95, 0.08), (-2.95, -0.84), color=F.PURPLE, lw=2.4, mutation=15)
    ax.text(-4.25, -0.10, "溶解", color=F.GREEN, fontsize=11.5, weight="bold")
    ax.text(-2.52, -0.10, "結晶", color=F.PURPLE, fontsize=11.5, weight="bold")
    ax.text(-2.9, 2.18, "飽和溶液＋未溶固體", ha="center", fontsize=14, weight="bold")

    _box(ax, (0.25, 1.35), 4.95, 0.85, "$v_{\\mathrm{dissolve}}=v_{\\mathrm{crystallize}}$", face="#e9f8ef", edge=F.GREEN, fs=15)
    _box(ax, (0.25, 0.23), 4.95, 0.80, "微觀：兩個方向仍持續進行\n粒子在固相與溶液間交換", face="#eef4ff", edge=F.BLUE, fs=11.8)
    _box(ax, (0.25, -0.90), 4.95, 0.80, "巨觀：溶液濃度與固體總量平均不變\n固定溫度下呈現穩定狀態", face="#fff7dd", edge=F.AMBER, fs=11.8)
    _box(ax, (0.25, -2.05), 4.95, 0.80, "加入同種晶種：提供成核表面\n過飽和溶液可快速析晶至飽和", face="#f1ecff", edge=F.PURPLE, fs=11.8)
    n_dissolved = len(dissolved)
    n_crystal = len(crystal_positions)
    assert n_dissolved == 8 and n_crystal == 9
    fig.suptitle("飽和是動態平衡：速率相等使巨觀組成穩定", fontsize=16, y=0.98)
    fig.subplots_adjust(left=0.025, right=0.975, top=0.88, bottom=0.04)
    return _save(fig, "必化-3-飽和溶液動態平衡.svg")


def fig_acid_base_particles():
    """以相同分析濃度比較強酸與弱酸的粒子分布。"""
    fig, axes = plt.subplots(1, 2, figsize=(11.8, 5.7))
    for ax in axes:
        ax.set_aspect("equal")
        ax.axis("off")
        ax.set_xlim(-3.1, 3.1)
        ax.set_ylim(-2.7, 2.7)
        _beaker(ax, -2.15, -1.45, width=4.3, height=3.5, liquid_height=2.7)

    # Strong acid: six formula units represented as six H+ and six A-.
    strong_h = [(-1.60, 0.75), (-0.75, 0.22), (0.10, 0.88), (0.95, 0.18), (1.55, 0.78), (-0.15, -0.62)]
    strong_a = [(-1.45, -0.18), (-0.60, 0.85), (0.25, -0.12), (1.10, 0.88), (1.55, -0.45), (-0.75, -0.72)]
    for x, y in strong_h:
        _particle(axes[0], x, y, "$H^+$", F.RED, radius=0.19)
    for x, y in strong_a:
        _particle(axes[0], x, y, "$A^-$", F.BLUE, radius=0.19)
    axes[0].text(0, 2.20, "強酸 HA：近乎完全游離", ha="center", fontsize=14, weight="bold")
    axes[0].text(0, -2.08, "$HA\\rightarrow H^++A^-$\n$[H^+]\\approx c_{HA}$（一般濃度）", ha="center", fontsize=12)

    # Weak acid: six formula units, one ionized and five neutral HA.
    neutral = [(-1.55, 0.72), (-0.55, 0.30), (0.52, 0.82), (1.45, 0.25), (-0.62, -0.68)]
    for x, y in neutral:
        _particle(axes[1], x - 0.12, y, "H", F.RED, radius=0.15)
        _particle(axes[1], x + 0.12, y, "A", F.BLUE, radius=0.15)
    _particle(axes[1], 1.35, -0.70, "$H^+$", F.RED, radius=0.19)
    _particle(axes[1], 1.78, -0.70, "$A^-$", F.BLUE, radius=0.19)
    axes[1].text(0, 2.20, "弱酸 HA：只有一部分游離", ha="center", fontsize=14, weight="bold")
    axes[1].text(0, -2.08, "$HA\\rightleftharpoons H^++A^-$\n$[H^+]<c_{HA}$", ha="center", fontsize=12)

    total_formula_units = 6
    strong_ionized = len(strong_h)
    weak_ionized = 1
    assert strong_ionized == total_formula_units
    assert len(neutral) + weak_ionized == total_formula_units
    assert strong_ionized > weak_ionized
    fig.suptitle("強弱描述游離程度；濃淡描述每單位體積含多少物質", fontsize=16, y=0.98)
    fig.subplots_adjust(left=0.035, right=0.97, top=0.87, bottom=0.05, wspace=0.12)
    return _save(fig, "必化-3-強弱酸鹼粒子模型.svg")


def fig_ph_indicators():
    """以 pH 軸顯示十倍關係與三種指示劑變色範圍。"""
    fig, axes = plt.subplots(2, 1, figsize=(12.0, 6.2), gridspec_kw={"height_ratios": [1.0, 1.25]})
    top, bottom = axes
    for ax in axes:
        ax.set_xlim(0, 14)
        ax.set_yticks([])
        ax.spines[["left", "right", "top"]].set_visible(False)
        ax.set_xticks(np.arange(0, 15, 1))

    h_values = np.array([1e-2, 1e-3, 1e-4, 1e-5])
    p_h = -np.log10(h_values)
    assert np.allclose(p_h, [2, 3, 4, 5])
    top.plot([2, 5], [0.5, 0.5], color=F.RED, lw=2.5, marker="o")
    for p, c in zip(p_h, h_values):
        top.text(p, 0.67, f"$10^{{-{int(p)}}}$ M", ha="center", fontsize=10.5)
    top.text(3.5, 0.18, "pH 每增加 1，$[H^+]$ 變為原來的 $1/10$", ha="center", fontsize=12, color=F.RED)
    top.set_ylim(0, 1)
    top.set_title("pH 是氫離子濃度的十進對數刻度", fontsize=13.5)

    ranges = [
        ("甲基橙", 3.2, 4.4, F.RED, F.AMBER),
        ("溴瑞香草酚藍（BTB）", 6.0, 7.6, F.AMBER, F.BLUE),
        ("酚酞", 8.2, 10.0, "#f8fafc", "#db2777"),
    ]
    y_positions = [2.5, 1.5, 0.5]
    for (name, lo, hi, left_color, right_color), y in zip(ranges, y_positions):
        bottom.add_patch(Rectangle((0, y - 0.22), lo, 0.44, facecolor=left_color, edgecolor="none", alpha=0.65))
        bottom.add_patch(Rectangle((lo, y - 0.22), hi - lo, 0.44, facecolor=F.PURPLE, edgecolor="none", alpha=0.42))
        bottom.add_patch(Rectangle((hi, y - 0.22), 14 - hi, 0.44, facecolor=right_color, edgecolor="none", alpha=0.55))
        bottom.text(0.12, y + 0.34, name, ha="left", fontsize=11.2, weight="bold")
        bottom.text((lo + hi) / 2, y, f"{lo:.1f}–{hi:.1f}", ha="center", va="center", fontsize=10.5, color="white", weight="bold")
        assert 0 <= lo < hi <= 14
    bottom.axvline(7, color="#334155", lw=1.2, ls="--")
    bottom.text(7, 3.05, "25 °C 中性", ha="center", fontsize=10.5, color="#334155")
    bottom.set_ylim(0, 3.5)
    bottom.set_xlabel("pH")
    bottom.set_title("指示劑提供 pH 範圍；精確讀值由校正儀器量測", fontsize=13.5)
    fig.suptitle("pH 數值與指示劑顏色都必須連回濃度與變色範圍", fontsize=16, y=0.99)
    fig.subplots_adjust(left=0.055, right=0.98, top=0.88, bottom=0.10, hspace=0.44)
    return _save(fig, "必化-3-pH與指示劑範圍.svg")


def fig_neutralization_ledger():
    """以 4 H+ 和 6 OH- 展示中和、剩餘粒子與 pH 判定。"""
    acid_mmol = 4.0
    base_mmol = 6.0
    reacted = min(acid_mmol, base_mmol)
    remaining_oh = base_mmol - reacted
    total_volume_ml = 100.0
    oh_concentration = remaining_oh / total_volume_ml
    p_oh = -np.log10(oh_concentration)
    p_h = 14.0 - p_oh
    assert np.isclose(reacted, 4.0)
    assert np.isclose(remaining_oh, 2.0)
    assert np.isclose(oh_concentration, 0.020)
    assert np.isclose(p_h, 12.3010299957)

    fig, axes = plt.subplots(1, 3, figsize=(12.0, 5.6))
    panels = [
        ("混合前", "酸：4 mmol $H^+$\n鹼：6 mmol $OH^-$"),
        ("反應", "$H^++OH^-\\rightarrow H_2O$\n依 1:1 消耗 4 mmol"),
        ("混合後", "剩 2 mmol $OH^-$\n總體積 100.0 mL"),
    ]
    for ax, (title, note) in zip(axes, panels):
        ax.set_aspect("equal")
        ax.axis("off")
        ax.set_xlim(-2.3, 2.3)
        ax.set_ylim(-2.5, 2.5)
        ax.text(0, 2.12, title, ha="center", fontsize=14, weight="bold")
        ax.text(0, -1.92, note, ha="center", fontsize=11.4)
    for i, y in enumerate([1.2, 0.55, -0.10, -0.75]):
        _particle(axes[0], -0.75, y, "$H^+$", F.RED, radius=0.21)
    for i, (x, y) in enumerate([(-0.05, 1.2), (0.72, 1.2), (-0.05, 0.45), (0.72, 0.45), (-0.05, -0.30), (0.72, -0.30)]):
        _particle(axes[0], x, y, "$OH^-$", F.BLUE, radius=0.24)

    for y in [1.0, 0.35, -0.30, -0.95]:
        _particle(axes[1], -0.58, y, "$H^+$", F.RED, radius=0.20)
        _particle(axes[1], 0.58, y, "$OH^-$", F.BLUE, radius=0.23)
        F.arrow(axes[1], (-0.25, y), (0.25, y), color=F.GREEN, lw=1.5, mutation=11)

    water_centers = [(-0.85, 0.95), (0.55, 0.95), (-0.85, -0.05), (0.55, -0.05)]
    for x, y in water_centers:
        _particle(axes[2], x, y, "O", F.RED, radius=0.19)
        _particle(axes[2], x - 0.29, y + 0.14, "H", F.BLUE, radius=0.13)
        _particle(axes[2], x + 0.29, y + 0.14, "H", F.BLUE, radius=0.13)
    _particle(axes[2], -0.42, -0.83, "$OH^-$", F.BLUE, radius=0.24)
    _particle(axes[2], 0.42, -0.83, "$OH^-$", F.BLUE, radius=0.24)
    axes[2].text(0, -2.42, "$[OH^-]=0.0200\\ \\mathrm{M}$，$pH=12.30$（25 °C）", ha="center", fontsize=10.9, color=F.PURPLE)
    fig.suptitle("先用莫耳數完成中和，再以剩餘強酸或強鹼求 pH", fontsize=16, y=0.98)
    fig.subplots_adjust(left=0.025, right=0.975, top=0.86, bottom=0.05, wspace=0.10)
    return _save(fig, "必化-3-中和反應粒子帳.svg")


def fig_redox_transfer():
    """以鐵置換銅離子顯示電子、電荷、觀察與推論。"""
    electrons = 2
    fe_charge_before, fe_charge_after = 0, 2
    cu_charge_before, cu_charge_after = 2, 0
    assert fe_charge_after - fe_charge_before == electrons
    assert cu_charge_before - cu_charge_after == electrons
    assert fe_charge_before + cu_charge_before == fe_charge_after + cu_charge_after

    fig, axes = plt.subplots(1, 2, figsize=(12.0, 5.9), gridspec_kw={"width_ratios": [1.05, 1.0]})
    left, right = axes
    for ax in axes:
        ax.axis("off")

    left.set_xlim(-3.0, 3.0)
    left.set_ylim(-2.7, 2.7)
    _box(left, (-2.65, 1.25), 2.20, 0.83, "$Fe(s)\\rightarrow Fe^{2+}(aq)+2e^-$", face="#fff1e6", edge=F.RED, fs=12.2)
    _box(left, (0.45, 1.25), 2.20, 0.83, "$Cu^{2+}(aq)+2e^-\\rightarrow Cu(s)$", face="#e9f8ef", edge=F.GREEN, fs=12.2)
    F.arrow(left, (-0.27, 1.65), (0.27, 1.65), color=F.PURPLE, lw=2.6, mutation=16)
    left.text(0, 2.05, "2 個電子", ha="center", fontsize=11.5, color=F.PURPLE, weight="bold")
    _box(left, (-2.65, -0.05), 2.20, 0.82, "Fe 失電子\n被氧化\n還原劑", face="#fff7dd", edge=F.AMBER, fs=11.8)
    _box(left, (0.45, -0.05), 2.20, 0.82, "$Cu^{2+}$ 得電子\n被還原\n氧化劑", face="#eef4ff", edge=F.BLUE, fs=11.8)
    _box(left, (-2.25, -1.72), 4.50, 0.88, "$Fe(s)+Cu^{2+}(aq)\\rightarrow Fe^{2+}(aq)+Cu(s)$\n電子得失與總電荷同時守恆", face="#f1ecff", edge=F.PURPLE, fs=12.0)
    left.set_title("粒子與電子帳", fontsize=14.5)

    right.set_xlim(-3.1, 3.1)
    right.set_ylim(-2.7, 2.7)
    _beaker(right, -2.25, -1.55, width=4.5, height=3.6, liquid_height=2.65, liquid="#bfdbfe")
    right.add_patch(Rectangle((-0.34, -1.25), 0.68, 3.05, facecolor="#64748b", edgecolor="#334155", lw=1.4))
    for x, y in [(-1.65, 0.80), (-1.10, 0.08), (1.15, 0.65), (1.60, -0.15)]:
        _particle(right, x, y, "$Cu^{2+}$", F.BLUE, radius=0.24)
    for x, y in [(-0.52, 0.96), (0.50, 0.62), (-0.54, 0.15), (0.49, -0.28)]:
        _particle(right, x, y, "Cu", "#b45309", radius=0.18, edge="#7c2d12")
    right.text(0, 2.25, "鐵片浸入硫酸銅溶液", ha="center", fontsize=14, weight="bold")
    _box(right, (-2.75, -2.42), 5.50, 0.60, "觀察：藍色變淡、鐵片表面有紅棕固體；推論需由反應式連到 $Cu^{2+}$ 消耗與 Cu 生成。", face="#fff7dd", edge=F.AMBER, fs=10.7)
    right.set_title("巨觀證據", fontsize=14.5)
    fig.suptitle("氧化還原以電子轉移連接粒子變化與可見證據", fontsize=16, y=0.98)
    fig.subplots_adjust(left=0.025, right=0.975, top=0.86, bottom=0.05, wspace=0.12)
    return _save(fig, "必化-3-氧化還原電子轉移.svg")


def main():
    for entrypoint, filename in FIGURE_OUTPUTS:
        assert entrypoint in globals(), f"缺少圖形函式：{entrypoint}"
        globals()[entrypoint]()
        expected = os.path.join(CH, "assets", filename)
        assert os.path.exists(expected), f"圖檔未產生：{expected}"


if __name__ == "__main__":
    main()
