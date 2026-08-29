# -*- coding: utf-8 -*-
"""產生「選化 II-3 化學反應速率」學生講義章內 SVG。

重繪：.venv/bin/python _tools/fig_content_選化II-3.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, FancyBboxPatch, Rectangle

import figlib as F


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CH = os.path.join(ROOT, "content", "選修化學II", "選化II-3")


FIGURE_OUTPUTS = (
    ("fig_rate_slopes", "選化II-3-濃度時間與速率斜率.svg"),
    ("fig_stoichiometric_rates", "選化II-3-化學計量速率關係.svg"),
    ("fig_initial_rates", "選化II-3-初速率比較法.svg"),
    ("fig_orders_half_life", "選化II-3-零級一級與半生期.svg"),
    ("fig_effective_collision", "選化II-3-有效碰撞的能量與位向.svg"),
    ("fig_energy_distribution", "選化II-3-粒子動能分布與溫度.svg"),
    ("fig_reaction_energy", "選化II-3-正逆反應能量圖.svg"),
    ("fig_mechanism", "選化II-3-多步反應機構.svg"),
    ("fig_concentration_surface", "選化II-3-濃度與接觸面積.svg"),
    ("fig_catalyst", "選化II-3-催化途徑與反應熱.svg"),
    ("fig_iodine_clock_setup", "選化II-3-碘鐘反應裝置與終點.svg"),
    ("fig_iodine_clock_data", "選化II-3-碘鐘反應資料.svg"),
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


def _double_arrow(ax, start, end, text, *, color=F.RED, fs=10.5, offset=(0, 0)):
    ax.annotate(
        "",
        xy=end,
        xytext=start,
        arrowprops={"arrowstyle": "<->", "color": color, "lw": 1.8},
    )
    ax.text(
        (start[0] + end[0]) / 2 + offset[0],
        (start[1] + end[1]) / 2 + offset[1],
        text,
        color=color,
        fontsize=fs,
        ha="center",
        va="center",
    )


def _atom(ax, xy, color, label, radius=0.28, *, edge=F.INK, text_color="white", z=4):
    atom = Circle(xy, radius, facecolor=color, edgecolor=edge, lw=1.3, zorder=z)
    ax.add_patch(atom)
    ax.text(xy[0], xy[1], label, color=text_color, ha="center", va="center", fontsize=9.5, weight="bold", zorder=z + 1)
    return atom


def fig_rate_slopes():
    """用同一條濃度曲線建立平均、瞬時與初速率。"""
    t = np.linspace(0, 12, 500)
    concentration = 0.80 * np.exp(-0.18 * t)
    t1, t2, ti = 2.0, 8.0, 5.0
    c1 = 0.80 * np.exp(-0.18 * t1)
    c2 = 0.80 * np.exp(-0.18 * t2)
    ci = 0.80 * np.exp(-0.18 * ti)
    average_slope = (c2 - c1) / (t2 - t1)
    instantaneous_slope = -0.18 * ci
    assert average_slope < 0 and instantaneous_slope < 0
    assert np.isclose(concentration[0], 0.80)

    fig, axes = plt.subplots(1, 2, figsize=(12.0, 5.6))
    ax = axes[0]
    ax.plot(t, concentration, color=F.BLUE, lw=2.8)
    ax.scatter([t1, t2], [c1, c2], color=F.RED, zorder=5)
    ax.plot([t1, t2], [c1, c2], color=F.RED, lw=2.0, ls="--")
    ax.vlines([t1, t2], 0, [c1, c2], color=F.GRID, lw=1.1)
    ax.hlines([c1, c2], 0, [t1, t2], color=F.GRID, lw=1.1)
    ax.text(5.2, 0.66, r"割線斜率 $=\Delta[A]/\Delta t$", color=F.RED, fontsize=11.2)
    ax.fill_between([t1, t2], [c2, c2], [c1, c1], color=F.RED, alpha=0.08)
    ax.set_xlabel("時間 $t$/min")
    ax.set_ylabel("$[A]$/M")
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 0.86)
    F.clean_grid(ax)
    ax.set_title("一段時間：平均消耗速率取割線斜率絕對值", fontsize=13.2, weight="bold")

    ax = axes[1]
    ax.plot(t, concentration, color=F.BLUE, lw=2.8)
    tangent_t = np.linspace(2.0, 8.0, 80)
    tangent = ci + instantaneous_slope * (tangent_t - ti)
    ax.plot(tangent_t, tangent, color=F.PURPLE, lw=2.2, ls="--")
    ax.scatter([ti], [ci], color=F.PURPLE, zorder=5)
    ax.annotate(
        f"$t={ti:.0f}\\ min$ 切線\n$-d[A]/dt={-instantaneous_slope:.3f}\\ M\\,min^{{-1}}$",
        (ti, ci),
        xytext=(7.0, 0.68),
        arrowprops={"arrowstyle": "->", "color": F.PURPLE},
        fontsize=10.8,
        color=F.PURPLE,
    )
    initial_slope = -0.18 * concentration[0]
    ax.plot([0, 3.0], concentration[0] + initial_slope * np.array([0, 3.0]), color=F.GREEN, lw=1.8, ls=":")
    ax.text(0.65, 0.58, "在 $t=0$ 的切線給初速率", color=F.GREEN, fontsize=10.5)
    ax.set_xlabel("時間 $t$/min")
    ax.set_ylabel("$[A]$/M")
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 0.86)
    F.clean_grid(ax)
    ax.set_title("一個時刻：瞬時速率取切線斜率絕對值", fontsize=13.2, weight="bold")
    fig.suptitle("濃度－時間圖上的斜率就是濃度變化速率", fontsize=16, y=0.99)
    fig.subplots_adjust(left=0.08, right=0.98, bottom=0.15, top=0.82, wspace=0.25)
    return _save(fig, "選化II-3-濃度時間與速率斜率.svg")


def fig_stoichiometric_rates():
    """用反應進度產生三條濃度曲線並核對係數歸一化速率。"""
    t = np.linspace(0, 10, 200)
    extent = 0.025 * t
    no = 0.70 - 2 * extent
    oxygen = 0.50 - extent
    nitrogen_dioxide = 0.10 + 2 * extent
    assert np.all(no >= 0)
    slopes = np.array([-0.05, -0.025, 0.05])
    normalized = np.array([-slopes[0] / 2, -slopes[1], slopes[2] / 2])
    assert np.allclose(normalized, 0.025)

    fig, axes = plt.subplots(1, 2, figsize=(12.0, 5.7), gridspec_kw={"width_ratios": [1.15, 0.95]})
    ax = axes[0]
    ax.plot(t, no, color=F.BLUE, lw=2.6, label="$[NO]$")
    ax.plot(t, oxygen, color=F.PURPLE, lw=2.6, label="$[O_2]$")
    ax.plot(t, nitrogen_dioxide, color=F.RED, lw=2.6, label="$[NO_2]$")
    ax.set_xlabel("時間 $t$/s")
    ax.set_ylabel("濃度/M")
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 0.72)
    ax.legend(frameon=False, ncol=3, loc="upper center")
    F.clean_grid(ax)
    ax.set_title(r"$2NO+O_2\rightarrow2NO_2$：濃度斜率按係數成比例", fontsize=13.2, weight="bold")

    ax = axes[1]
    ax.axis("off")
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    _box(ax, (0.7, 7.7), 8.6, 1.25, r"$2NO(g)+O_2(g)\rightarrow2NO_2(g)$", face="#eff6ff", edge=F.BLUE, fs=16)
    rows = [
        (r"$NO$", r"$-\Delta[NO]/\Delta t$", r"$0.050\ M\,s^{-1}$", r"$\div2$"),
        (r"$O_2$", r"$-\Delta[O_2]/\Delta t$", r"$0.025\ M\,s^{-1}$", r"$\div1$"),
        (r"$NO_2$", r"$+\Delta[NO_2]/\Delta t$", r"$0.050\ M\,s^{-1}$", r"$\div2$"),
    ]
    for index, (species, raw, value, divide) in enumerate(rows):
        y = 6.5 - 1.45 * index
        _box(ax, (0.55, y), 1.25, 0.82, species, face="#f8fafc", fs=12.5)
        _box(ax, (2.0, y), 3.2, 0.82, raw, face="#ffffff", fs=11.0)
        _box(ax, (5.4, y), 2.25, 0.82, value, face="#fff7dd", edge=F.AMBER, fs=10.8)
        _box(ax, (7.85, y), 1.15, 0.82, divide, face="#f0fdf4", edge=F.GREEN, fs=12.0)
    _box(
        ax,
        (0.8, 0.65),
        8.4,
        1.2,
        r"$r=-\dfrac{1}{2}\dfrac{\Delta[NO]}{\Delta t}"
        r"=-\dfrac{\Delta[O_2]}{\Delta t}"
        r"=\dfrac{1}{2}\dfrac{\Delta[NO_2]}{\Delta t}"
        r"=0.025\ \mathrm{M\,s^{-1}}$",
        face="#fdf2f8",
        edge=F.RED,
        fs=13.0,
    )
    ax.set_title("除以化學計量係數後，各物質給同一反應速率", fontsize=13.2, weight="bold")
    fig.suptitle("係數把不同物質的濃度變化換成共同的反應進度", fontsize=16, y=0.985)
    fig.subplots_adjust(left=0.07, right=0.985, bottom=0.13, top=0.82, wspace=0.15)
    return _save(fig, "選化II-3-化學計量速率關係.svg")


def fig_initial_rates():
    """以原創初速率資料呈現控制變因比較與級數求法。"""
    a = np.array([0.10, 0.20, 0.10, 0.20])
    b = np.array([0.10, 0.10, 0.20, 0.20])
    k = 3.00
    rate = k * a**2 * b
    assert np.allclose(rate, [0.003, 0.012, 0.006, 0.024])
    assert np.isclose(rate[1] / rate[0], 4)
    assert np.isclose(rate[2] / rate[0], 2)

    fig, axes = plt.subplots(1, 2, figsize=(12.0, 5.8), gridspec_kw={"width_ratios": [1.22, 0.95]})
    ax = axes[0]
    ax.axis("off")
    columns = ["實驗", r"$[A]_0$/M", r"$[B]_0$/M", r"$r_0/(M\,s^{-1})$"]
    data = [[str(i + 1), f"{a[i]:.2f}", f"{b[i]:.2f}", f"{rate[i]:.3f}"] for i in range(4)]
    table = ax.table(cellText=data, colLabels=columns, loc="center", cellLoc="center", colLoc="center")
    table.auto_set_font_size(False)
    table.set_fontsize(11.5)
    table.scale(1.0, 1.85)
    for (row, col), cell in table.get_celld().items():
        cell.set_edgecolor("#94a3b8")
        if row == 0:
            cell.set_facecolor("#dbeafe")
            cell.set_text_props(weight="bold")
        elif row in (1, 2):
            cell.set_facecolor("#fff7dd")
        elif row == 3:
            cell.set_facecolor("#f0fdf4")
    ax.set_title("每次只比較一個濃度變因", fontsize=13.5, weight="bold", pad=16)

    ax = axes[1]
    ax.axis("off")
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    _box(ax, (0.6, 7.6), 8.8, 1.35, "實驗 1 → 2：$[A]$ 加倍、$[B]$ 固定\n速率變 $4$ 倍，故 $2^m=4\\Rightarrow m=2$", face="#fff7dd", edge=F.AMBER, fs=12.2)
    _box(ax, (0.6, 5.6), 8.8, 1.35, "實驗 1 → 3：$[B]$ 加倍、$[A]$ 固定\n速率變 $2$ 倍，故 $2^n=2\\Rightarrow n=1$", face="#f0fdf4", edge=F.GREEN, fs=12.2)
    _box(ax, (0.8, 3.2), 8.4, 1.45, "$r=k[A]^2[B]$\n總反應級數 $=2+1=3$", face="#eff6ff", edge=F.BLUE, fs=16)
    _box(ax, (1.25, 0.75), 7.5, 1.35, r"$k=\dfrac{0.003}{(0.10)^2(0.10)}"
         r"=3.00\ \mathrm{M^{-2}\,s^{-1}}$", face="#fdf2f8", edge=F.RED, fs=13.5)
    ax.set_title("倍率直接決定濃度指數", fontsize=13.5, weight="bold")
    fig.suptitle("速率定律的指數由初速率實驗決定", fontsize=16, y=0.985)
    fig.subplots_adjust(left=0.045, right=0.985, bottom=0.08, top=0.82, wspace=0.12)
    return _save(fig, "選化II-3-初速率比較法.svg")


def fig_orders_half_life():
    """並列零級與一級的濃度、速率及半生期特徵。"""
    t = np.linspace(0, 60, 301)
    a0 = 0.80
    k0 = 0.010
    k1 = np.log(2) / 15.0
    zero = np.maximum(a0 - k0 * t, 0)
    first = a0 * np.exp(-k1 * t)
    assert np.isclose(zero[150], 0.50)
    assert np.isclose(zero[300], 0.20)
    assert np.isclose(first[75], 0.40)
    assert np.isclose(first[150], 0.20)
    assert np.isclose(np.log(2) / k1, 15.0)

    fig, axes = plt.subplots(2, 2, figsize=(11.5, 8.0))
    ax = axes[0, 0]
    ax.plot(t, zero, color=F.BLUE, lw=2.6)
    ax.scatter([0, 30, 60], [0.8, 0.5, 0.2], color=F.BLUE)
    ax.text(33, 0.65, "等時間減去等量", color=F.BLUE, fontsize=10.5)
    ax.set_title("零級：$[A]=[A]_0-kt$")
    ax.set_xlabel("$t$/min")
    ax.set_ylabel("$[A]$/M")
    ax.set_ylim(0, 0.86)
    F.clean_grid(ax)

    ax = axes[0, 1]
    ax.plot(t, first, color=F.PURPLE, lw=2.6)
    half_times = np.array([0, 15, 30, 45, 60])
    half_values = a0 * (0.5 ** np.arange(5))
    ax.scatter(half_times, half_values, color=F.PURPLE, zorder=5)
    for x, y in zip(half_times[:4], half_values[:4]):
        ax.text(x + 1.0, y + 0.025, f"{y:.2f}", fontsize=9.2, color=F.PURPLE)
    ax.text(31, 0.62, r"每 $15\ min$ 乘上 $1/2$", color=F.PURPLE, fontsize=10.5)
    ax.set_title("一級：$[A]=[A]_0e^{-kt}$")
    ax.set_xlabel("$t$/min")
    ax.set_ylabel("$[A]$/M")
    ax.set_ylim(0, 0.86)
    F.clean_grid(ax)

    concentrations = np.linspace(0, 0.8, 100)
    ax = axes[1, 0]
    ax.plot(concentrations, np.full_like(concentrations, k0), color=F.BLUE, lw=2.6, label="零級 $r=k$")
    ax.plot(concentrations, k1 * concentrations, color=F.PURPLE, lw=2.6, label="一級 $r=k[A]$")
    ax.set_xlabel("$[A]$/M")
    ax.set_ylabel(r"$r/(M\,min^{-1})$")
    ax.legend(frameon=False)
    F.clean_grid(ax)
    ax.set_title("速率－濃度圖可直接辨識級數")

    ax = axes[1, 1]
    ax.axis("off")
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    _box(ax, (0.65, 6.65), 8.7, 1.75, "零級半生期\n$t_{1/2}=[A]_0/(2k)$\n隨初濃度改變", face="#eff6ff", edge=F.BLUE, fs=13.5)
    _box(ax, (0.65, 3.85), 8.7, 1.75, "一級半生期\n$t_{1/2}=\\ln2/k=0.693/k$\n與初濃度無關", face="#f3e8ff", edge=F.PURPLE, fs=13.5)
    _box(ax, (1.3, 1.15), 7.4, 1.25, "$N=N_0(1/2)^{t/t_{1/2}}$", face="#fff7dd", edge=F.AMBER, fs=16)
    ax.set_title("半生期公式須先確認反應級數", fontsize=13.2, weight="bold")
    fig.suptitle("零級與一級反應的圖形和半生期互相對應", fontsize=16, y=0.99)
    fig.subplots_adjust(left=0.08, right=0.98, bottom=0.08, top=0.89, hspace=0.34, wspace=0.27)
    return _save(fig, "選化II-3-零級一級與半生期.svg")


def fig_effective_collision():
    """以 CO 與 NO2 的碰撞方向表示能量和位向兩個條件。"""
    fig, axes = plt.subplots(1, 3, figsize=(12.5, 4.8))
    titles = ("有效碰撞", "位向不合", "動能不足")
    subtitles = (r"O 端接近 C，且 $E_k\geq E_{min}$", "N 端接近 C，鍵重組方向不利", r"位向適當，但 $E_k<E_{min}$")
    outcomes = ("形成 $CO_2+NO$", "分開後仍為反應物", "分開後仍為反應物")
    arrow_colors = (F.GREEN, F.RED, F.AMBER)

    for index, ax in enumerate(axes):
        ax.axis("off")
        ax.set_xlim(-4.2, 4.2)
        ax.set_ylim(-2.5, 2.7)
        # CO：C 在右端，向右移動。
        _atom(ax, (-2.85, 0.25), "#64748b", "O")
        _atom(ax, (-2.25, 0.25), "#111827", "C")
        ax.plot([-2.58, -2.52], [0.25, 0.25], color=F.INK, lw=4)
        F.arrow(ax, (-1.85, 0.25), (-0.75, 0.25), color=arrow_colors[index], lw=2.2, mutation=12)
        # NO2：依 panel 改變面向或速率。
        if index == 1:
            centers = [(2.10, 0.25, "#2563eb", "N"), (2.70, 0.72, "#64748b", "O"), (2.70, -0.22, "#64748b", "O")]
            target = (0.82, 0.25)
        else:
            centers = [(2.70, 0.25, "#2563eb", "N"), (2.10, 0.72, "#64748b", "O"), (2.10, -0.22, "#64748b", "O")]
            target = (0.72, 0.25)
        for x, y, color, label in centers:
            _atom(ax, (x, y), color, label)
        ax.plot([centers[0][0] - 0.25, centers[1][0] + 0.05], [centers[0][1], centers[1][1]], color=F.INK, lw=2)
        ax.plot([centers[0][0] - 0.25, centers[2][0] + 0.05], [centers[0][1], centers[2][1]], color=F.INK, lw=2)
        mutation = 12 if index != 2 else 7
        F.arrow(ax, (1.65, 0.25), target, color=arrow_colors[index], lw=2.2, mutation=mutation)
        ax.add_patch(Circle((0, 0.25), 0.48, facecolor=arrow_colors[index], edgecolor="none", alpha=0.10))
        symbol = "✓" if index == 0 else "×"
        ax.text(0, 0.25, symbol, color=arrow_colors[index], fontsize=24, weight="bold", ha="center", va="center")
        _box(ax, (-3.65, -2.08), 7.3, 0.72, outcomes[index], face="#f8fafc", edge=arrow_colors[index], fs=10.8)
        ax.set_title(titles[index], fontsize=13.2, weight="bold", color=arrow_colors[index], pad=8)
        ax.text(0, 1.85, subtitles[index], ha="center", fontsize=9.7)

    fig.suptitle(r"$CO+NO_2\rightarrow CO_2+NO$：碰撞要同時具備足夠動能與適當位向", fontsize=15.5, y=0.985)
    fig.subplots_adjust(left=0.025, right=0.985, bottom=0.07, top=0.78, wspace=0.06)
    return _save(fig, "選化II-3-有效碰撞的能量與位向.svg")


def fig_energy_distribution():
    """數值產生兩溫度粒子動能分布與超過活化能的面積。"""
    energy = np.linspace(0.02, 80.0, 1600)

    def distribution(e, theta):
        raw = np.sqrt(e) * np.exp(-e / theta)
        return raw / np.trapezoid(raw, e)

    low = distribution(energy, 10.0)
    high = distribution(energy, 18.0)
    ea = 40.0
    mask = energy >= ea
    low_tail = np.trapezoid(low[mask], energy[mask])
    high_tail = np.trapezoid(high[mask], energy[mask])
    assert np.isclose(np.trapezoid(low, energy), 1.0)
    assert np.isclose(np.trapezoid(high, energy), 1.0)
    assert high_tail > low_tail > 0

    fig, axes = plt.subplots(1, 2, figsize=(12.0, 5.7))
    ax = axes[0]
    ax.plot(energy, low, color=F.BLUE, lw=2.6, label="$T_1$（較低溫）")
    ax.plot(energy, high, color=F.RED, lw=2.6, label="$T_2$（較高溫）")
    ax.fill_between(energy[mask], high[mask], color=F.RED, alpha=0.22)
    ax.fill_between(energy[mask], low[mask], color=F.BLUE, alpha=0.30)
    ax.axvline(ea, color=F.INK, lw=1.7, ls="--")
    ax.text(ea + 1.5, max(high) * 0.89, "$E_a=E_{min}$", fontsize=11.0)
    ax.annotate(
        "較高溫的尾端面積較大",
        (52, high[np.searchsorted(energy, 52)]),
        xytext=(47, max(high) * 0.58),
        arrowprops={"arrowstyle": "->", "color": F.RED},
        fontsize=10.5,
        color=F.RED,
    )
    ax.set_xlabel("粒子動能 $E$")
    ax.set_ylabel("粒子比例密度")
    ax.set_xlim(0, 80)
    ax.set_ylim(0, max(low) * 1.12)
    ax.legend(frameon=False)
    F.clean_grid(ax)
    ax.set_title("升溫改變整條分布，$E_a$ 位置不變", fontsize=13.2, weight="bold")

    ax = axes[1]
    ax.axis("off")
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    _box(ax, (0.65, 7.65), 8.7, 1.35, "曲線下總面積 $=1$\n表示全部粒子", face="#eff6ff", edge=F.BLUE, fs=13.0)
    _box(
        ax,
        (0.65, 5.25),
        8.7,
        1.45,
        f"$E\\geq E_a$ 的面積\n$T_1:\\ {low_tail:.3f}\\qquad T_2:\\ {high_tail:.3f}$",
        face="#fdf2f8",
        edge=F.RED,
        fs=13.0,
    )
    _box(ax, (0.65, 2.85), 8.7, 1.45, "升溫的主要效果\n超過低限能的粒子比例增加", face="#fff7dd", edge=F.AMBER, fs=13.0)
    _box(ax, (0.9, 0.6), 8.2, 1.25, r"有效碰撞頻率增加 $\Rightarrow$ 反應速率上升", face="#f0fdf4", edge=F.GREEN, fs=14.0)
    ax.set_title("曲線面積直接連到有效碰撞比例", fontsize=13.2, weight="bold")
    fig.suptitle("溫度影響反應速率的主要機制", fontsize=16, y=0.985)
    fig.subplots_adjust(left=0.08, right=0.985, bottom=0.14, top=0.82, wspace=0.15)
    return _save(fig, "選化II-3-粒子動能分布與溫度.svg")


def fig_reaction_energy():
    """用一致能量數值建立正、逆活化能與反應熱。"""
    coordinate = np.linspace(0, 1, 500)
    reactant_energy = 40.0
    product_energy = 10.0
    transition_energy = 140.0
    baseline = reactant_energy + (product_energy - reactant_energy) * coordinate
    profile = baseline + 115.0 * np.exp(-((coordinate - 0.50) / 0.18) ** 2)
    peak_index = int(np.argmax(profile))
    peak_x = coordinate[peak_index]
    profile += transition_energy - profile[peak_index]
    peak = float(np.max(profile))
    ea_forward = peak - reactant_energy
    ea_reverse = peak - product_energy
    delta_h = product_energy - reactant_energy
    assert np.isclose(peak, transition_energy)
    assert np.isclose(ea_forward, 100.0)
    assert np.isclose(ea_reverse, 130.0)
    assert np.isclose(ea_forward - ea_reverse, delta_h)

    fig, ax = plt.subplots(figsize=(10.5, 6.0))
    ax.plot(coordinate, profile, color=F.PURPLE, lw=3.0)
    ax.hlines([reactant_energy, product_energy, transition_energy], [0, 0.72, peak_x], [0.27, 1.0, peak_x + 0.16], colors=["#94a3b8", "#94a3b8", F.GRID], linestyles=["--", "--", ":"])
    ax.scatter([0.02, peak_x, 0.98], [reactant_energy, peak, product_energy], color=[F.BLUE, F.PURPLE, F.RED], zorder=5)
    ax.text(0.03, reactant_energy + 6, r"反應物 $40\ kJ\,mol^{-1}$", fontsize=11.5, color=F.BLUE)
    ax.text(0.98, product_energy - 12, r"產物 $10\ kJ\,mol^{-1}$", fontsize=11.5, color=F.RED, ha="right")
    ax.text(peak_x, peak + 8, r"活化複合體 $140\ kJ\,mol^{-1}$", fontsize=11.5, color=F.PURPLE, ha="center")
    _double_arrow(ax, (0.18, reactant_energy), (0.18, peak), "$E_a=100$", color=F.BLUE, offset=(-0.08, 0))
    _double_arrow(ax, (0.82, product_energy), (0.82, peak), "$E_a'=130$", color=F.RED, offset=(0.08, 0))
    _double_arrow(ax, (0.93, reactant_energy), (0.93, product_energy), r"$\Delta H=-30$", color=F.GREEN, offset=(-0.09, 0))
    ax.text(0.50, -7, r"$\Delta H=E_a-E_a'=100-130=-30\ \mathrm{kJ\,mol^{-1}}$", ha="center", fontsize=13.0, weight="bold")
    ax.set_xlabel("反應進行方向")
    ax.set_ylabel(r"位能 $(\mathrm{kJ\,mol^{-1}})$")
    ax.set_xlim(0, 1)
    ax.set_ylim(-18, 160)
    ax.set_xticks([])
    F.clean_grid(ax)
    ax.set_title("正反應與逆反應跨越同一個活化複合體", fontsize=15, weight="bold")
    fig.subplots_adjust(left=0.12, right=0.97, bottom=0.15, top=0.88)
    return _save(fig, "選化II-3-正逆反應能量圖.svg")


def fig_mechanism():
    """用兩步能量圖與物種帳辨識慢步驟、中間物和催化劑。"""
    x = np.linspace(0, 2, 900)
    baseline = np.piecewise(x, [x <= 1, x > 1], [lambda z: 30 + 10 * z, lambda z: 40 - 15 * (z - 1)])
    profile = baseline + 92 * np.exp(-((x - 0.42) / 0.18) ** 2) + 48 * np.exp(-((x - 1.46) / 0.20) ** 2)
    first_peak = float(np.max(profile[x < 0.9]))
    intermediate = float(profile[np.argmin(abs(x - 1.0))])
    second_peak = float(np.max(profile[x > 1.1]))
    assert first_peak - 30 > second_peak - intermediate

    fig, axes = plt.subplots(1, 2, figsize=(12.2, 5.8), gridspec_kw={"width_ratios": [1.2, 1.0]})
    ax = axes[0]
    ax.plot(x, profile, color=F.PURPLE, lw=2.8)
    ax.scatter([0.02, 1.0, 1.98], [profile[0], intermediate, profile[-1]], color=[F.BLUE, F.AMBER, F.RED], zorder=5)
    ax.text(0.03, profile[0] + 7, "$A+C+B$", color=F.BLUE, fontsize=11.5)
    ax.text(1.0, intermediate - 18, "$I+B$\n中間物谷底", color=F.AMBER, fontsize=10.8, ha="center")
    ax.text(1.97, profile[-1] + 7, "$D+B$", color=F.RED, fontsize=11.5, ha="right")
    ax.text(0.42, first_peak + 7, "第一步峰較高\n速率決定步驟", ha="center", fontsize=10.8, color=F.RED)
    ax.text(1.47, second_peak + 7, "第二步峰", ha="center", fontsize=10.5, color=F.PURPLE)
    ax.set_xlabel("反應進行方向")
    ax.set_ylabel("位能")
    ax.set_xticks([])
    F.clean_grid(ax)
    ax.set_title("每一個基本步驟對應一個能障峰", fontsize=13.2, weight="bold")

    ax = axes[1]
    ax.axis("off")
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    _box(ax, (0.65, 7.55), 8.7, 1.25, r"步驟 1（慢）：$A+B\rightarrow I$", face="#fdf2f8", edge=F.RED, fs=14.0)
    _box(ax, (0.65, 5.45), 8.7, 1.25, r"步驟 2（快）：$I+C\rightarrow D+B$", face="#f3e8ff", edge=F.PURPLE, fs=14.0)
    F.arrow(ax, (5.0, 5.1), (5.0, 4.25), color=F.INK, lw=1.8, mutation=11)
    _box(ax, (0.9, 2.85), 8.2, 1.15, "相加並消去兩邊都有的物種", face="#fff7dd", edge=F.AMBER, fs=12.2)
    _box(ax, (0.65, 0.65), 8.7, 1.35, "全反應：$A+C\\rightarrow D$\n$B$ 先消耗後再生＝催化劑；$I$ 先生成後消耗＝中間物", face="#f0fdf4", edge=F.GREEN, fs=12.5)
    ax.set_title("反應機構要同時通過物種帳與速率檢查", fontsize=13.2, weight="bold")
    fig.suptitle("多步反應的最高能障通常控制整體速率", fontsize=16, y=0.985)
    fig.subplots_adjust(left=0.08, right=0.985, bottom=0.14, top=0.82, wspace=0.16)
    return _save(fig, "選化II-3-多步反應機構.svg")


def fig_concentration_surface():
    """把勻相濃度效應與不勻相接觸面積用可計算模型表示。"""
    t = np.linspace(0, 10, 300)
    product_low = 1 - np.exp(-0.25 * t)
    product_high = 1 - np.exp(-0.60 * t)
    assert product_high[40] > product_low[40]
    assert np.isclose(product_high[-1], 0.9975, atol=0.002)

    fig, axes = plt.subplots(1, 2, figsize=(12.3, 5.8))
    ax = axes[0]
    ax.plot(t, product_low, color=F.BLUE, lw=2.6, label="較低濃度")
    ax.plot(t, product_high, color=F.RED, lw=2.6, label="較高濃度")
    ax.axhline(1.0, color="#94a3b8", lw=1.2, ls="--")
    ax.annotate("初始斜率較大", (0.8, product_high[np.searchsorted(t, 0.8)]), xytext=(3.0, 0.45), arrowprops={"arrowstyle": "->", "color": F.RED}, color=F.RED, fontsize=10.8)
    ax.text(4.6, 0.93, "反應物總量相同時，最終產量相同", fontsize=10.5, color=F.INK)
    ax.set_xlabel("時間")
    ax.set_ylabel("累積產物量（相對值）")
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 1.08)
    ax.legend(frameon=False)
    F.clean_grid(ax)
    ax.set_title("勻相：提高濃度增加單位體積碰撞頻率", fontsize=13.0, weight="bold")

    ax = axes[1]
    ax.axis("off")
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    # 左側一個邊長 2 的立方體投影。
    ax.add_patch(Rectangle((0.65, 5.45), 2.35, 2.35, facecolor="#dbeafe", edgecolor=F.BLUE, lw=2.0))
    ax.plot([0.65, 1.25, 3.60, 3.0], [7.8, 8.4, 8.4, 7.8], color=F.BLUE, lw=1.7)
    ax.plot([3.0, 3.6], [7.8, 8.4], color=F.BLUE, lw=1.7)
    ax.plot([3.6, 3.6], [8.4, 6.05], color=F.BLUE, lw=1.7)
    ax.text(2.1, 4.85, "原立方體邊長 $2\\ cm$\n表面積 $6(2^2)=24\\ cm^2$", ha="center", fontsize=11.2)
    # 右側 8 個邊長 1 的小立方體，以方格表示。
    start_x, start_y = 6.25, 5.65
    for row in range(2):
        for col in range(4):
            ax.add_patch(Rectangle((start_x + col * 0.78, start_y + row * 0.95), 0.68, 0.68, facecolor="#fee2e2", edgecolor=F.RED, lw=1.4))
    ax.text(7.75, 4.85, "切成 $8$ 個邊長 $1\\ cm$ 小立方體\n總表面積 $8\\times6(1^2)=48\\ cm^2$", ha="center", fontsize=11.2)
    F.arrow(ax, (3.85, 6.75), (5.65, 6.75), color=F.AMBER, lw=2.1, mutation=12)
    ax.text(4.75, 7.05, "切碎", color=F.AMBER, fontsize=11.5, ha="center")
    _box(ax, (0.85, 1.65), 8.3, 1.55, "體積與物質的量不變\n總接觸面積變 $48/24=2$ 倍", face="#fff7dd", edge=F.AMBER, fs=14.0)
    _box(ax, (1.2, 0.15), 7.6, 0.95, "不勻相反應只在界面發生；可用界面越多，速率越快", face="#f0fdf4", edge=F.GREEN, fs=11.5)
    ax.set_title("不勻相：粒徑減小使總接觸面積增加", fontsize=13.0, weight="bold")
    fig.suptitle("碰撞機會可由濃度或可用界面增加", fontsize=16, y=0.985)
    fig.subplots_adjust(left=0.075, right=0.985, bottom=0.13, top=0.82, wspace=0.15)
    return _save(fig, "選化II-3-濃度與接觸面積.svg")


def fig_catalyst():
    """以相同初終能量比較無催化與催化途徑。"""
    x = np.linspace(0, 1, 500)
    reactant = 45.0
    product = 5.0
    progress = 3 * x**2 - 2 * x**3
    baseline = reactant + (product - reactant) * progress
    uncatalyzed = baseline + 123.5 * np.exp(-((x - 0.48) / 0.20) ** 2)
    catalyzed = baseline + 65.45 * np.exp(-((x - 0.34) / 0.14) ** 2) + 56 * np.exp(-((x - 0.70) / 0.14) ** 2)
    # 高斯尾在圖形邊界不嚴格為零，因此將初、終態錨定在同一對能階。
    uncatalyzed[0], uncatalyzed[-1] = reactant, product
    catalyzed[0], catalyzed[-1] = reactant, product
    ea_uncat = float(np.max(uncatalyzed) - reactant)
    ea_cat = float(np.max(catalyzed) - reactant)
    delta_h = product - reactant
    assert ea_uncat > ea_cat > 0
    assert np.isclose(ea_uncat, 105.0, atol=0.2)
    assert np.isclose(ea_cat, 55.0, atol=0.2)
    assert np.isclose(delta_h, -40.0)
    assert np.isclose(uncatalyzed[0], reactant)
    assert np.isclose(catalyzed[0], reactant)
    assert np.isclose(uncatalyzed[-1], product)
    assert np.isclose(catalyzed[-1], product)
    assert np.all(np.diff(uncatalyzed[: int(np.argmax(uncatalyzed)) + 1]) >= 0)

    fig, axes = plt.subplots(1, 2, figsize=(12.0, 5.8), gridspec_kw={"width_ratios": [1.2, 0.9]})
    ax = axes[0]
    ax.plot(x, uncatalyzed, color=F.RED, lw=2.8, label="無催化途徑")
    ax.plot(x, catalyzed, color=F.GREEN, lw=2.8, label="催化途徑")
    ax.scatter([0, 1], [reactant, product], color=[F.BLUE, F.PURPLE], zorder=5)
    ax.hlines([reactant, product], [0, 0.78], [0.23, 1.0], color="#94a3b8", lw=1.1, ls="--")
    _double_arrow(ax, (0.12, reactant), (0.12, float(np.max(uncatalyzed))), f"$E_a={ea_uncat:.0f}$", color=F.RED, offset=(-0.05, 0))
    _double_arrow(ax, (0.83, reactant), (0.83, float(np.max(catalyzed))), f"$E_{{a,cat}}={ea_cat:.0f}$", color=F.GREEN, offset=(0.05, 0))
    _double_arrow(ax, (0.94, reactant), (0.94, product), r"$\Delta H=-40$", color=F.PURPLE, offset=(-0.08, 0))
    ax.set_xlabel("反應進行方向")
    ax.set_ylabel(r"位能 $(\mathrm{kJ\,mol^{-1}})$")
    ax.set_xlim(0, 1)
    ax.set_ylim(-10, 164)
    ax.set_xticks([])
    ax.legend(frameon=False, loc="upper right")
    F.clean_grid(ax)
    ax.set_title("催化劑提供另一條較低能障的多步途徑", fontsize=13.2, weight="bold")

    ax = axes[1]
    ax.axis("off")
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    _box(ax, (0.6, 7.45), 8.8, 1.45, "改變：反應機構、活化複合體、$E_a$、速率常數 $k$", face="#f0fdf4", edge=F.GREEN, fs=12.2)
    _box(ax, (0.6, 5.15), 8.8, 1.45, r"保持：反應物與產物能量、$\Delta H$、平衡組成", face="#eff6ff", edge=F.BLUE, fs=12.5)
    _box(ax, (0.6, 2.85), 8.8, 1.45, "正、逆反應都沿較低能障途徑進行\n兩方向都加速", face="#f3e8ff", edge=F.PURPLE, fs=12.5)
    _box(ax, (0.9, 0.65), 8.2, 1.25, "催化劑參與基本步驟，反應完成後再生", face="#fff7dd", edge=F.AMBER, fs=13.0)
    ax.set_title("能量圖決定可改變與保持不變的量", fontsize=13.2, weight="bold")
    fig.suptitle("催化途徑降低最高能障，同時保留反應熱", fontsize=16, y=0.985)
    fig.subplots_adjust(left=0.08, right=0.985, bottom=0.14, top=0.82, wspace=0.16)
    return _save(fig, "選化II-3-催化途徑與反應熱.svg")


def fig_iodine_clock_setup():
    """建立碘鐘反應的溶液、操作、終點與安全關係。"""
    fig, ax = plt.subplots(figsize=(12.0, 6.0))
    ax.axis("off")
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 9)

    # Solution A flask.
    ax.add_patch(Rectangle((0.9, 4.35), 2.6, 2.3, facecolor="#dbeafe", edgecolor=F.BLUE, lw=2.0))
    ax.add_patch(Rectangle((1.65, 6.65), 1.1, 0.75, facecolor="white", edgecolor=F.BLUE, lw=2.0))
    ax.text(2.2, 5.55, "溶液 A\n$KIO_3(aq)$", ha="center", va="center", fontsize=13, color=F.BLUE, weight="bold")
    ax.text(2.2, 3.85, "量取固定體積", ha="center", fontsize=10.5)

    # Solution B flask.
    ax.add_patch(Rectangle((4.25, 4.35), 2.6, 2.3, facecolor="#f3e8ff", edgecolor=F.PURPLE, lw=2.0))
    ax.add_patch(Rectangle((5.0, 6.65), 1.1, 0.75, facecolor="white", edgecolor=F.PURPLE, lw=2.0))
    ax.text(5.55, 5.55, "溶液 B\n$NaHSO_3$＋稀 $H_2SO_4$\n＋澱粉", ha="center", va="center", fontsize=11.5, color=F.PURPLE, weight="bold")
    ax.text(5.55, 3.85, "同溫達熱平衡", ha="center", fontsize=10.5)

    ax.annotate(
        "",
        xy=(7.55, 5.85),
        xytext=(3.5, 6.15),
        arrowprops={"arrowstyle": "->", "color": F.AMBER, "lw": 2.1, "connectionstyle": "arc3,rad=-0.28"},
    )
    F.arrow(ax, (6.85, 5.0), (7.55, 5.0), color=F.AMBER, lw=2.1, mutation=12)
    ax.text(9.2, 7.45, "混合瞬間啟動碼錶", color=F.AMBER, fontsize=11.3, ha="center", weight="bold")

    # Mixing vessel, colorless then blue endpoint.
    ax.add_patch(FancyBboxPatch((7.7, 4.0), 3.0, 3.0, boxstyle="round,pad=0.04,rounding_size=0.18", facecolor="#f8fafc", edgecolor=F.INK, lw=2.0))
    ax.text(9.2, 5.65, "反應進行\n$I_2$ 一生成就被\n$HSO_3^-$ 消耗", ha="center", va="center", fontsize=11.0)
    ax.text(9.2, 4.45, "溶液維持無色", ha="center", color="#64748b", fontsize=10.8)
    F.arrow(ax, (10.75, 5.45), (12.0, 5.45), color=F.BLUE, lw=2.2, mutation=12)
    ax.text(11.4, 6.05, "$HSO_3^-$ 耗盡", ha="center", fontsize=10.8, color=F.BLUE)
    ax.add_patch(FancyBboxPatch((12.15, 4.0), 2.9, 3.0, boxstyle="round,pad=0.04,rounding_size=0.18", facecolor="#1e3a8a", edgecolor=F.BLUE, lw=2.0))
    ax.text(13.6, 5.65, "終點\n$I_2$－澱粉\n藍色錯合物", ha="center", va="center", fontsize=12.0, color="white", weight="bold")
    ax.text(13.6, 3.6, "停止碼錶，記錄 $t$", ha="center", fontsize=11.0, color=F.BLUE)

    _box(ax, (0.65, 1.75), 6.9, 1.05, r"固定生成同一終點量時：$r_{relative}\propto1/t$", face="#fff7dd", edge=F.AMBER, fs=13.0)
    _box(ax, (8.0, 1.75), 7.35, 1.05, "觀察：顏色突變時間　推論：相對速率", face="#f0fdf4", edge=F.GREEN, fs=12.5)
    _box(ax, (0.65, 0.25), 14.7, 0.95, "護目鏡、實驗衣、耐化學手套；使用安全吸球；酸性含碘廢液依無機酸廢液回收", face="#fef2f2", edge=F.RED, fs=11.0)
    ax.set_title("碘鐘反應：以固定顏色終點比較濃度與溫度對速率的影響", fontsize=15.5, weight="bold", pad=10)
    fig.subplots_adjust(left=0.02, right=0.985, bottom=0.04, top=0.91)
    return _save(fig, "選化II-3-碘鐘反應裝置與終點.svg")


def fig_iodine_clock_data():
    """以原創碘鐘資料核對 1/t 與濃度、溫度的單調關係。"""
    concentrations = np.array([0.004, 0.006, 0.008, 0.010])
    times_c = np.array([88.0, 60.0, 45.0, 36.0])
    temperatures = np.array([10.0, 20.0, 30.0, 40.0])
    times_t = np.array([83.0, 52.0, 34.0, 23.0])
    relative_c = 1 / times_c
    relative_t = 1 / times_t
    assert np.all(np.diff(relative_c) > 0)
    assert np.all(np.diff(relative_t) > 0)
    slope, intercept = np.polyfit(concentrations, relative_c, 1)
    assert slope > 0
    assert abs(intercept) < 0.001

    fig, axes = plt.subplots(1, 2, figsize=(11.8, 5.7))
    ax = axes[0]
    ax.scatter(concentrations, relative_c, color=F.BLUE, s=55, zorder=5)
    grid = np.linspace(0.0035, 0.0105, 100)
    ax.plot(grid, slope * grid + intercept, color=F.BLUE, lw=2.2)
    for x, y, seconds in zip(concentrations, relative_c, times_c):
        ax.annotate(f"{seconds:.0f} s", (x, y), xytext=(4, 7), textcoords="offset points", fontsize=9.2)
    ax.set_xlabel("混合後 $[KIO_3]$/M")
    ax.set_ylabel("相對速率 $1/t$ $(s^{-1})$")
    ax.set_xlim(0.0034, 0.0106)
    ax.set_ylim(0, 0.031)
    F.clean_grid(ax)
    ax.set_title("只改變 $[KIO_3]$：濃度越高，$1/t$ 越大", fontsize=12.8, weight="bold")

    ax = axes[1]
    ax.scatter(temperatures, relative_t, color=F.RED, s=55, zorder=5)
    ax.plot(temperatures, relative_t, color=F.RED, lw=2.2)
    for x, y, seconds in zip(temperatures, relative_t, times_t):
        ax.annotate(f"{seconds:.0f} s", (x, y), xytext=(4, 7), textcoords="offset points", fontsize=9.2)
    ax.set_xlabel("反應溫度/°C")
    ax.set_ylabel("相對速率 $1/t$ $(s^{-1})$")
    ax.set_xlim(7, 43)
    ax.set_ylim(0, 0.050)
    F.clean_grid(ax)
    ax.set_title("固定濃度：溫度越高，$1/t$ 越大", fontsize=12.8, weight="bold")
    fig.suptitle("終點量固定時，顏色出現越快代表反應越快", fontsize=16, y=0.985)
    fig.subplots_adjust(left=0.085, right=0.985, bottom=0.15, top=0.82, wspace=0.26)
    return _save(fig, "選化II-3-碘鐘反應資料.svg")


def main():
    functions = {
        "fig_rate_slopes": fig_rate_slopes,
        "fig_stoichiometric_rates": fig_stoichiometric_rates,
        "fig_initial_rates": fig_initial_rates,
        "fig_orders_half_life": fig_orders_half_life,
        "fig_effective_collision": fig_effective_collision,
        "fig_energy_distribution": fig_energy_distribution,
        "fig_reaction_energy": fig_reaction_energy,
        "fig_mechanism": fig_mechanism,
        "fig_concentration_surface": fig_concentration_surface,
        "fig_catalyst": fig_catalyst,
        "fig_iodine_clock_setup": fig_iodine_clock_setup,
        "fig_iodine_clock_data": fig_iodine_clock_data,
    }
    assert len(functions) == len(FIGURE_OUTPUTS)
    for function_name, filename in FIGURE_OUTPUTS:
        assert function_name in functions
        output = functions[function_name]()
        assert os.path.basename(output) == filename


if __name__ == "__main__":
    main()
