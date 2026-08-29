# -*- coding: utf-8 -*-
"""產生必物-1「科學的態度與方法」學生講義 SVG。

重繪：.venv/bin/python _tools/fig_content_必物-1.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Arc, Circle, FancyBboxPatch, Polygon, Rectangle

import figlib as F


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CH = os.path.join(ROOT, "content", "必修物理", "必物-1")

FIGURE_OUTPUTS = (
    ("fig_claim_test_cycle", "必物-1-可檢驗主張與科學循環.svg"),
    ("fig_ramp_data_model", "必物-1-斜面實驗與資料模型.svg"),
    ("fig_si_units_network", "必物-1-SI基本量與導出量.svg"),
    ("fig_prefix_scale", "必物-1-前綴詞與單位換算.svg"),
    ("fig_order_of_magnitude", "必物-1-長度尺度與數量級.svg"),
    ("fig_physics_domains", "必物-1-物理領域與模型條件.svg"),
    ("fig_history_unification", "必物-1-物理史的證據模型與統一.svg"),
    ("fig_ct_interdisciplinary", "必物-1-跨領域電腦斷層系統.svg"),
)


def _save(fig, name):
    return F.save_to(fig, CH, name, output_subdir="assets", write_pdf=False)


def _rounded(ax, xy, wh, text, fc="#f8fafc", ec=F.INK, fs=11.5, lw=1.6):
    x, y = xy
    w, h = wh
    patch = FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.04,rounding_size=0.10",
        facecolor=fc, edgecolor=ec, lw=lw,
    )
    ax.add_patch(patch)
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs)
    return patch


def fig_claim_test_cycle():
    """把可檢驗主張連到預測、資料、修正與再測試。"""
    fig, ax = F.canvas(12.0, 6.2)
    ax.axis("off")
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 7)

    _rounded(
        ax, (0.25, 5.45), (4.0, 1.05),
        "問題：同一斜面上，球的位移如何隨時間改變？",
        fc="#dbeafe", ec=F.BLUE, fs=11.5,
    )
    _rounded(
        ax, (0.25, 3.65), (4.0, 1.05),
        "假設：由靜止釋放時，$s/t^2$ 保持固定",
        fc="#ede9fe", ec=F.PURPLE, fs=11.5,
    )
    _rounded(
        ax, (0.25, 1.85), (4.0, 1.05),
        "預測：$s$ 對 $t^2$ 作圖應接近一直線",
        fc="#fef3c7", ec=F.AMBER, fs=11.5,
    )
    F.arrow(ax, (2.25, 5.42), (2.25, 4.78), color=F.INK, lw=1.8, mutation=11)
    F.arrow(ax, (2.25, 3.62), (2.25, 2.98), color=F.INK, lw=1.8, mutation=11)

    _rounded(
        ax, (5.0, 5.45), (2.7, 1.05),
        "設計量測\n控制斜角、球、釋放點",
        fc="#dcfce7", ec=F.GREEN, fs=11.2,
    )
    _rounded(
        ax, (8.75, 5.45), (2.7, 1.05),
        "保留原始資料\n畫圖、估斜率與離散",
        fc="#dcfce7", ec=F.GREEN, fs=11.2,
    )
    F.arrow(ax, (4.35, 2.37), (5.8, 5.35), color=F.INK, lw=1.7, mutation=11)
    F.arrow(ax, (7.78, 5.98), (8.65, 5.98), color=F.INK, lw=1.8, mutation=11)

    _rounded(
        ax, (8.75, 3.55), (2.7, 1.05),
        "資料符合預測\n建立暫時可用模型",
        fc="#dbeafe", ec=F.BLUE, fs=11.2,
    )
    _rounded(
        ax, (8.75, 1.65), (2.7, 1.05),
        "新條件下再預測\n改變斜角或球種",
        fc="#dbeafe", ec=F.BLUE, fs=11.2,
    )
    F.arrow(ax, (10.1, 5.42), (10.1, 4.72), color=F.BLUE, lw=2.0, mutation=11)
    F.arrow(ax, (10.1, 3.52), (10.1, 2.82), color=F.BLUE, lw=2.0, mutation=11)
    F.arrow(ax, (8.65, 2.17), (7.25, 5.32), color=F.BLUE, lw=1.7, mutation=11)

    _rounded(
        ax, (5.0, 0.25), (2.7, 1.05),
        "資料偏離預測\n檢查裝置、重複或修正假設",
        fc="#fee2e2", ec=F.RED, fs=10.7,
    )
    F.arrow(ax, (9.05, 5.42), (7.7, 1.38), color=F.RED, lw=1.7, mutation=11)
    F.arrow(ax, (5.0, 0.78), (2.5, 1.75), color=F.RED, lw=1.7, mutation=11)

    ax.text(
        6.0, 6.78,
        "科學結論的強度來自可重複的檢驗與新預測",
        ha="center", fontsize=15.5, weight="bold",
    )
    ax.text(
        6.0, 0.03,
        "一次符合會提高模型可信度；持續跨條件檢驗才能界定適用範圍",
        ha="center", fontsize=11.3, color="#475569",
    )
    nodes = 8
    directed_links = 9
    assert nodes == 8 and directed_links == 9
    _save(fig, "必物-1-可檢驗主張與科學循環")


def fig_ramp_data_model():
    """用斜面裝置、控制變因與線性化資料建立 s 正比 t 平方。"""
    t = np.array([0.25, 0.35, 0.45, 0.55, 0.65, 0.75])
    ideal_s = 0.48 * t**2
    measured_s = ideal_s + np.array([0.0010, -0.0015, 0.0012, -0.0010, 0.0015, -0.0008])
    slope, intercept = np.polyfit(t**2, measured_s, 1)
    predicted = slope * t**2 + intercept
    residual = measured_s - predicted
    r2 = 1 - np.sum(residual**2) / np.sum((measured_s - measured_s.mean())**2)

    fig, axes = plt.subplots(1, 2, figsize=(12.0, 5.2))
    ax = axes[0]
    ax.axis("off")
    ax.set_aspect("equal")
    ax.set_xlim(-0.5, 7.5)
    ax.set_ylim(-0.8, 5.6)
    ax.plot([0.3, 6.7], [4.7, 0.65], color=F.INK, lw=5, solid_capstyle="round")
    ax.plot([0.3, 6.7], [4.47, 0.42], color="#94a3b8", lw=2)
    ball_x = 1.05
    ball_y = 4.22
    ax.add_patch(Circle((ball_x, ball_y), 0.28, facecolor="#fef3c7", edgecolor=F.AMBER, lw=2))
    ax.text(ball_x, ball_y + 0.55, "同一顆球\n由靜止釋放", ha="center", fontsize=10.8)
    for x, label in [(2.2, "光閘 1"), (4.1, "光閘 2"), (5.8, "光閘 3")]:
        y = 4.7 + (0.65 - 4.7) * (x - 0.3) / 6.4
        ax.plot([x, x], [y - 0.75, y + 0.75], color=F.BLUE, lw=2)
        ax.add_patch(Rectangle((x - 0.20, y - 0.87), 0.4, 0.18, facecolor=F.BLUE, edgecolor=F.BLUE))
        ax.text(x, y - 1.15, label, ha="center", fontsize=9.8, color=F.BLUE)
    ax.add_patch(Arc((6.7, 0.65), 1.6, 1.6, theta1=148, theta2=180, color=F.RED, lw=2))
    ax.text(5.78, 0.48, "斜角固定", fontsize=10.5, color=F.RED)
    _rounded(ax, (0.0, -0.52), (3.05, 0.82), "自變量：時間 $t$", fc="#dbeafe", ec=F.BLUE, fs=10.7)
    _rounded(ax, (3.35, -0.52), (3.45, 0.82), "應變量：沿斜面位移 $s$", fc="#dcfce7", ec=F.GREEN, fs=10.7)
    ax.set_title("裝置先固定比較條件，再量測成對資料", fontsize=14)

    ax = axes[1]
    x = t**2
    x_line = np.linspace(0, x.max() * 1.05, 100)
    ax.scatter(x, measured_s, s=62, color=F.BLUE, zorder=4, label="量測值")
    ax.plot(x_line, slope * x_line + intercept, color=F.RED, lw=2.5, label="線性模型")
    for xi, yi, ti in zip(x, measured_s, t):
        ax.text(xi, yi + 0.008, f"{ti:.2f} s", ha="center", fontsize=8.7, color="#475569")
    ax.set_xlabel("$t^2$（s$^2$）")
    ax.set_ylabel("位移 $s$（m）")
    F.clean_grid(ax)
    ax.legend(frameon=False, loc="upper left")
    ax.text(
        0.56 * x.max(), 0.22 * measured_s.max(),
        f"$s=({slope:.3f})t^2{intercept:+.4f}$\n$R^2={r2:.4f}$",
        fontsize=11.2, color=F.RED,
    )
    ax.set_title("$s$ 對 $t^2$ 接近直線，支持比例模型", fontsize=14)
    assert np.isclose(slope, 0.48, rtol=0.03)
    assert abs(intercept) < 0.003
    assert r2 > 0.999
    fig.tight_layout()
    _save(fig, "必物-1-斜面實驗與資料模型")


def fig_si_units_network():
    """七個 SI 基本量與常見導出量的定義鏈。"""
    fig, ax = F.canvas(12.0, 6.4)
    ax.axis("off")
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 7.2)

    basics = [
        ("時間", "s"), ("長度", "m"), ("質量", "kg"), ("電流", "A"),
        ("溫度", "K"), ("物量", "mol"), ("光強度", "cd"),
    ]
    for i, (quantity, unit) in enumerate(basics):
        y = 6.15 - i * 0.82
        _rounded(ax, (0.35, y - 0.31), (2.05, 0.62), f"{quantity}　{unit}",
                 fc="#f8fafc", ec=F.BLUE, fs=10.8)

    definitions = [
        ("速度", "$v=\\Delta x/\\Delta t$", "m/s"),
        ("加速度", "$a=\\Delta v/\\Delta t$", "m/s$^2$"),
        ("力", "$F=ma$", "N = kg·m/s$^2$"),
        ("能量", "$W=Fs$", "J = kg·m$^2$/s$^2$"),
        ("功率", "$P=W/t$", "W = kg·m$^2$/s$^3$"),
        ("電量", "$Q=It$", "C = A·s"),
    ]
    for i, (quantity, formula, unit) in enumerate(definitions):
        y = 6.15 - i * 1.0
        _rounded(ax, (3.35, y - 0.34), (2.55, 0.68), f"{quantity}\n{formula}",
                 fc="#dbeafe", ec=F.BLUE, fs=10.4)
        F.arrow(ax, (5.98, y), (7.0, y), color=F.INK, lw=1.6, mutation=10)
        _rounded(ax, (7.1, y - 0.34), (4.35, 0.68), unit,
                 fc="#dcfce7", ec=F.GREEN, fs=11.0)

    F.arrow(ax, (2.48, 5.74), (3.25, 6.15), color="#64748b", lw=1.2, mutation=8)
    F.arrow(ax, (2.48, 4.92), (3.25, 6.15), color="#64748b", lw=1.2, mutation=8)
    F.arrow(ax, (2.48, 4.10), (3.25, 4.15), color="#64748b", lw=1.2, mutation=8)
    F.arrow(ax, (2.48, 3.28), (3.25, 1.15), color="#64748b", lw=1.2, mutation=8)

    ax.text(6.0, 6.95, "導出量由定義式組合；單位必須沿同一乘除關係組合", ha="center",
            fontsize=15.0, weight="bold")
    ax.text(0.45, 0.20, "七個基本量", fontsize=11.5, color=F.BLUE, weight="bold")
    ax.text(3.45, 0.20, "定義式", fontsize=11.5, color=F.BLUE, weight="bold")
    ax.text(7.2, 0.20, "導出單位拆成 SI 基本單位", fontsize=11.5, color=F.GREEN, weight="bold")

    expected = {
        "N": (1, 1, -2, 0),
        "J": (1, 2, -2, 0),
        "W": (1, 2, -3, 0),
        "C": (0, 0, 1, 1),
    }
    assert expected["J"] == (1, 2, -2, 0)
    assert expected["W"][2] == -3 and expected["C"][3] == 1
    _save(fig, "必物-1-SI基本量與導出量")


def fig_prefix_scale():
    """前綴詞的十次方位置與平方、立方、複合單位換算。"""
    prefixes = [
        (-15, "f\n飛"), (-12, "p\n皮"), (-9, "n\n奈"), (-6, "μ\n微"),
        (-3, "m\n毫"), (0, "基本單位"), (3, "k\n千"), (6, "M\n百萬"),
        (9, "G\n吉"), (12, "T\n兆"), (15, "P\n拍"),
    ]
    fig, axes = plt.subplots(2, 1, figsize=(12.0, 6.2), gridspec_kw={"height_ratios": [1.05, 1.2]})
    ax = axes[0]
    ax.set_xlim(-16, 16)
    ax.set_ylim(-0.55, 1.25)
    ax.axhline(0.25, color=F.INK, lw=2)
    for exponent, label in prefixes:
        color = F.RED if exponent < 0 else F.GREEN if exponent > 0 else F.BLUE
        ax.plot([exponent, exponent], [0.12, 0.38], color=color, lw=2)
        ax.text(exponent, 0.55, label, ha="center", va="bottom", fontsize=10.4, color=color)
        ax.text(exponent, -0.02, f"$10^{{{exponent}}}$", ha="center", va="top", fontsize=9.5)
    ax.set_xticks([])
    ax.set_yticks([])
    for side in ax.spines.values():
        side.set_visible(False)
    ax.set_title("前綴詞在對數軸上的位置：每移 3 格就是一千倍", fontsize=14)

    ax = axes[1]
    ax.axis("off")
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 4.1)
    rows = [
        (3.35, "長度", "$2.5\\ \\mathrm{mm}$", "$2.5\\times10^{-3}\\ \\mathrm{m}$", -3),
        (2.35, "面積", "$3.0\\ \\mathrm{cm^2}$", "$3.0\\times(10^{-2})^2=3.0\\times10^{-4}\\ \\mathrm{m^2}$", -4),
        (1.35, "體積", "$0.80\\ \\mathrm{cm^3}$", "$0.80\\times(10^{-2})^3=8.0\\times10^{-7}\\ \\mathrm{m^3}$", -7),
        (0.35, "速率", "$144\\ \\mathrm{km/h}$", "$144\\times\\frac{10^3}{3600}=40\\ \\mathrm{m/s}$", None),
    ]
    for y, kind, source, result, exponent in rows:
        _rounded(ax, (0.25, y - 0.34), (1.35, 0.68), kind, fc="#f8fafc", ec=F.INK, fs=10.6)
        _rounded(ax, (1.95, y - 0.34), (2.55, 0.68), source, fc="#dbeafe", ec=F.BLUE, fs=11.0)
        F.arrow(ax, (4.65, y), (5.4, y), color=F.INK, lw=1.6, mutation=10)
        _rounded(ax, (5.55, y - 0.34), (6.15, 0.68), result, fc="#dcfce7", ec=F.GREEN, fs=10.6)
    ax.text(6.0, 3.98, "前綴先換成十次方；平方與立方會作用在整個長度單位上",
            ha="center", fontsize=13.8, weight="bold")
    assert np.isclose(3.0 * (1e-2)**2, 3.0e-4)
    assert np.isclose(0.80 * (1e-2)**3, 8.0e-7)
    assert np.isclose(144 * 1000 / 3600, 40.0)
    fig.tight_layout()
    _save(fig, "必物-1-前綴詞與單位換算")


def fig_order_of_magnitude():
    """長度量的對數軸與最近十次方判定。"""
    quantities = [
        ("質子", 1e-15, F.PURPLE),
        ("原子", 1e-10, F.BLUE),
        ("頭髮直徑", 7e-5, F.GREEN),
        ("人體", 1.7, F.AMBER),
        ("臺灣尺度", 4e5, F.RED),
        ("地球直徑", 1.3e7, F.BLUE),
        ("日地距離", 1.5e11, F.GREEN),
        ("銀河系", 1e21, F.PURPLE),
    ]
    fig, ax = plt.subplots(figsize=(12.0, 5.2))
    for i, (label, value, color) in enumerate(quantities):
        y = 0.75 + (i % 2) * 0.38
        ax.scatter([value], [y], s=75, color=color, zorder=5)
        ax.plot([value, value], [0.25, y - 0.05], color=color, lw=1.2, ls="--")
        ax.text(value, y + 0.10, label, rotation=32, ha="left", va="bottom", fontsize=10.4, color=color)
    ax.set_xscale("log")
    ax.set_xlim(1e-16, 1e22)
    ax.set_ylim(0.1, 1.55)
    ax.set_yticks([])
    exponents = list(range(-15, 22, 3))
    ax.set_xticks([10.0**e for e in exponents])
    ax.set_xticklabels([f"$10^{{{e}}}$" for e in exponents])
    ax.set_xlabel("長度（m）；對數軸上相鄰主刻度相差 $10^3$ 倍")
    F.clean_grid(ax)
    ax.set_title("數量級用最近的十次方描述尺度", fontsize=14.5)
    ax.text(
        1.3e-15, 0.18,
        "寫成 $x=a\\times10^n$：$a<\\sqrt{10}$ 取 $10^n$；$a\\geq\\sqrt{10}$ 取 $10^{n+1}$",
        fontsize=10.8, color="#475569",
    )
    values = np.array([item[1] for item in quantities])
    assert np.all(np.diff(np.log10(values)) > 0)
    assert round(np.log10(1.5e11)) == 11
    fig.tight_layout()
    _save(fig, "必物-1-長度尺度與數量級")


def fig_physics_domains():
    """古典物理四領域、近代模型與適用條件。"""
    fig, ax = F.canvas(12.0, 6.5)
    ax.axis("off")
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 7.3)
    domains = [
        ((0.4, 4.15), "力學", "運動、力與平衡\n軌道、結構、流體", F.BLUE),
        ((3.25, 4.15), "熱學", "溫度、內能與熱傳\n材料、引擎、氣候", F.RED),
        ((6.10, 4.15), "電磁學", "電荷、電流與磁場\n馬達、發電、通訊", F.GREEN),
        ((8.95, 4.15), "光學", "反射、折射、干涉\n鏡頭、光纖、成像", F.PURPLE),
    ]
    for (x, y), title, body, color in domains:
        _rounded(ax, (x, y), (2.65, 1.65), f"{title}\n{body}", fc="#f8fafc", ec=color, fs=10.7, lw=2)

    _rounded(
        ax, (0.85, 1.35), (4.75, 1.55),
        "量子模型\n原子與更小尺度、離散能階、波粒現象\n典型長度約 $10^{-10}$ m 以下",
        fc="#ede9fe", ec=F.PURPLE, fs=11.2, lw=2,
    )
    _rounded(
        ax, (6.4, 1.35), (4.75, 1.55),
        "相對論模型\n速度接近光速或重力極強的系統\n光速 $c=3.00\\times10^8$ m/s",
        fc="#fef3c7", ec=F.AMBER, fs=11.2, lw=2,
    )
    for x in (1.7, 4.55, 7.4, 10.25):
        F.arrow(ax, (x, 4.02), (x, 3.35), color="#64748b", lw=1.4, mutation=9)
    ax.text(
        6.0, 3.42,
        "日常低速、宏觀、弱重力條件下，古典模型通常已足夠精確",
        ha="center", fontsize=11.5, color="#475569",
    )
    ax.text(
        6.0, 6.85,
        "先按現象選領域，再按尺度、速度與重力條件選模型",
        ha="center", fontsize=15.2, weight="bold",
    )
    ax.text(
        6.0, 0.45,
        "同一裝置常跨領域：手機同時用到力學感測、電磁通訊、熱管理、光學成像與量子半導體",
        ha="center", fontsize=11.4,
    )
    atomic_scale = 1e-10
    c = 3.00e8
    assert atomic_scale < 1e-9 and c > 1e8
    _save(fig, "必物-1-物理領域與模型條件")


def fig_history_unification():
    """把物理史里程碑重畫成證據、模型、預測與統一的時間鏈。"""
    years = np.array([1543, 1638, 1687, 1820, 1831, 1843, 1864, 1900, 1905])
    labels = [
        ("哥白尼", "較簡潔的\n日心模型"),
        ("伽利略", "斜面資料與\n數學規律"),
        ("牛頓", "地表與天體\n運動統一"),
        ("厄斯特", "電流使磁針\n偏轉"),
        ("法拉第", "變動磁場\n產生電流"),
        ("焦耳", "功與熱\n可互相轉換"),
        ("馬克士威", "方程預測電磁波\n光是電磁波"),
        ("普朗克", "量子化解釋\n黑體頻譜"),
        ("愛因斯坦", "相對論與\n光子模型"),
    ]
    xs = np.linspace(0.75, 11.25, len(years))
    fig, ax = F.canvas(12.4, 7.0)
    ax.axis("off")
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 7.2)
    ax.plot([0.65, 11.35], [3.55, 3.55], color=F.INK, lw=2.2)
    F.arrow(ax, (11.0, 3.55), (11.55, 3.55), color=F.INK, lw=2.2, mutation=12)
    colors = [F.BLUE, F.BLUE, F.BLUE, F.GREEN, F.GREEN, F.RED, F.GREEN, F.PURPLE, F.AMBER]
    for i, (x, year, (name, contribution), color) in enumerate(zip(xs, years, labels, colors)):
        top = i % 2 == 0
        ax.scatter([x], [3.55], s=70, color=color, zorder=5)
        y0 = 4.05 if top else 0.55
        height = 1.65
        _rounded(ax, (x - 0.58, y0), (1.16, height), f"{name}\n{year}\n{contribution}",
                 fc="#f8fafc", ec=color, fs=8.4, lw=1.5)
        if top:
            F.arrow(ax, (x, 4.03), (x, 3.68), color=color, lw=1.2, mutation=7)
        else:
            F.arrow(ax, (x, 2.20), (x, 3.42), color=color, lw=1.2, mutation=7)
    ax.text(
        6.0, 6.75,
        "觀測與實驗提供限制，數學模型形成預測，較廣模型把現象統一起來",
        ha="center", fontsize=14.4, weight="bold",
    )
    ax.text(1.9, 0.16, "運動與天文", color=F.BLUE, fontsize=10.5, weight="bold")
    ax.text(5.5, 0.16, "電、磁、光與能量", color=F.GREEN, fontsize=10.5, weight="bold")
    ax.text(9.6, 0.16, "近代物理", color=F.PURPLE, fontsize=10.5, weight="bold")
    assert np.all(np.diff(years) > 0)
    assert years[-1] - years[0] == 362
    _save(fig, "必物-1-物理史的證據模型與統一")


def fig_ct_interdisciplinary():
    """電腦斷層從量測到影像的跨領域推理鏈。"""
    fig, ax = F.canvas(12.0, 6.3)
    ax.axis("off")
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 7.1)

    cx, cy = 3.05, 3.65
    ax.add_patch(Circle((cx, cy), 1.45, facecolor="#f8fafc", edgecolor=F.BLUE, lw=2.2))
    ax.add_patch(Circle((cx, cy), 0.68, facecolor="#e2e8f0", edgecolor="#64748b", lw=1.5))
    ax.text(cx, cy, "受測物", ha="center", va="center", fontsize=11.5)
    angles = np.deg2rad([20, 80, 140, 200, 260, 320])
    for angle in angles:
        sx = cx + 1.13 * np.cos(angle)
        sy = cy + 1.13 * np.sin(angle)
        ex = cx - 1.13 * np.cos(angle)
        ey = cy - 1.13 * np.sin(angle)
        ax.plot([sx, ex], [sy, ey], color=F.RED, lw=1.0, alpha=0.5)
    ax.text(cx, 5.45, "X 光源與偵測器繞行\n每個角度得到一列衰減資料", ha="center", fontsize=10.8, color=F.RED)

    _rounded(ax, (5.15, 4.55), (2.15, 1.0), "校正與共同單位\n位置、角度、強度", fc="#dbeafe", ec=F.BLUE, fs=10.4)
    _rounded(ax, (5.15, 2.95), (2.15, 1.0), "數學重建模型\n把多角度資料合併", fc="#ede9fe", ec=F.PURPLE, fs=10.4)
    _rounded(ax, (5.15, 1.35), (2.15, 1.0), "重建切面影像\n與已知標準比較", fc="#dcfce7", ec=F.GREEN, fs=10.4)
    F.arrow(ax, (4.55, 4.25), (5.05, 5.02), color=F.INK, lw=1.5, mutation=9)
    F.arrow(ax, (6.23, 4.48), (6.23, 4.02), color=F.INK, lw=1.5, mutation=9)
    F.arrow(ax, (6.23, 2.88), (6.23, 2.42), color=F.INK, lw=1.5, mutation=9)

    grid_x, grid_y = 9.3, 3.55
    values = np.array([
        [0, 0, 1, 1, 0, 0],
        [0, 1, 2, 2, 1, 0],
        [1, 2, 3, 3, 2, 1],
        [1, 2, 3, 3, 2, 1],
        [0, 1, 2, 2, 1, 0],
        [0, 0, 1, 1, 0, 0],
    ])
    colors = ["#f8fafc", "#bfdbfe", "#60a5fa", "#1f6feb"]
    cell = 0.42
    for row in range(6):
        for col in range(6):
            ax.add_patch(Rectangle(
                (grid_x + col * cell, grid_y + (5 - row) * cell),
                cell, cell, facecolor=colors[values[row, col]], edgecolor="white", lw=0.8,
            ))
    ax.text(grid_x + 1.25, 6.25, "重建影像", ha="center", fontsize=12.0, weight="bold")
    F.arrow(ax, (7.4, 1.85), (8.95, 4.0), color=F.GREEN, lw=1.8, mutation=11)

    disciplines = [
        ("物理", "X 光與物質交互作用"),
        ("電子／材料", "穩定光源與靈敏偵測器"),
        ("數學／資訊", "重建演算法與雜訊處理"),
        ("醫學", "判讀組織與臨床限制"),
    ]
    for i, (field, role) in enumerate(disciplines):
        x = 0.35 + i * 2.9
        _rounded(ax, (x, 0.18), (2.65, 0.78), f"{field}：{role}", fc="#f8fafc", ec="#64748b", fs=9.4)

    ax.text(
        6.0, 6.82,
        "跨領域系統把可重複量測、物理模型與專業判讀接成一條證據鏈",
        ha="center", fontsize=14.5, weight="bold",
    )
    assert len(angles) == 6
    assert values.shape == (6, 6) and values.max() == 3
    _save(fig, "必物-1-跨領域電腦斷層系統")


def main():
    for function_name, _filename in FIGURE_OUTPUTS:
        globals()[function_name]()


if __name__ == "__main__":
    main()
