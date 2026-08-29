# -*- coding: utf-8 -*-
"""產生「選化 V-2 環境化學」章內 SVG。

重繪：.venv/bin/python _tools/fig_content_選化V-2.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, FancyBboxPatch, Polygon, Rectangle

import figlib as F


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CH = os.path.join(ROOT, "content", "選修化學V", "選化V-2")


FIGURE_OUTPUTS = (
    ("fig_green_metrics", "選化V-2-綠色化學物料指標.svg"),
    ("fig_model_cycle", "選化V-2-科學模型證據循環.svg"),
    ("fig_ozone_cycles", "選化V-2-臭氧生成與氯自由基循環.svg"),
    ("fig_ozone_column", "選化V-2-臭氧柱量與杜布森單位.svg"),
    ("fig_oxygen_demand", "選化V-2-溶氧與生化需氧量.svg"),
    ("fig_eutrophication", "選化V-2-優養化因果與資料.svg"),
    ("fig_biomagnification", "選化V-2-生物累積與食物鏈放大.svg"),
    ("fig_water_test", "選化V-2-水質檢測與淨化證據鏈.svg"),
    ("fig_air_network", "選化V-2-一次與二次空氣污染物.svg"),
    ("fig_aqi", "選化V-2-AQI分指標與最大值.svg"),
    ("fig_nitrogen_cycle", "選化V-2-氮循環物種與氧化態.svg"),
    ("fig_nitrogen_budget", "選化V-2-農田氮收支.svg"),
    ("fig_energy_boundary", "選化V-2-能源生命週期邊界.svg"),
)


def _save(fig, filename):
    assert filename.endswith(".svg")
    return F.save_to(
        fig, CH, filename[:-4], output_subdir="assets", write_pdf=False
    )


def _box(ax, xy, w, h, text, *, fc="#f8fafc", ec="#64748b", fs=10.5, lw=1.4):
    patch = FancyBboxPatch(
        xy,
        w,
        h,
        boxstyle="round,pad=0.035,rounding_size=0.05",
        facecolor=fc,
        edgecolor=ec,
        linewidth=lw,
    )
    ax.add_patch(patch)
    ax.text(xy[0] + w / 2, xy[1] + h / 2, text, ha="center", va="center", fontsize=fs)
    return patch


def fig_green_metrics():
    """比較原子經濟率、產率與 E-factor，並驗證物料帳本。"""
    mr_reactants = 180.16
    mr_product = 2 * 46.07
    atom_economy = mr_product / mr_reactants * 100
    actual_product = 78.3
    theoretical_product = mr_product
    yield_percent = actual_product / theoretical_product * 100
    waste = 164.0
    e_factor = waste / actual_product
    assert np.isclose(atom_economy, 51.1423, atol=1e-3)
    assert np.isclose(yield_percent, 84.9794, atol=1e-3)
    assert np.isclose(actual_product + waste, 242.3)

    fig, axes = plt.subplots(1, 3, figsize=(13.0, 5.4))
    data = [
        ("原子經濟率", atom_economy, "平衡式中的理論去向\n只看計量反應物與目標產物", F.BLUE),
        ("產率", yield_percent, "實際產物 ÷ 理論產物\n受轉化率、選擇性與操作損失影響", F.GREEN),
        ("E-factor", e_factor, "廢棄物質量 ÷ 產品質量\n系統邊界要先約定", F.AMBER),
    ]
    for ax, (title, value, note, color) in zip(axes, data):
        ax.axis("off"); ax.set_xlim(0, 1); ax.set_ylim(0, 1)
        ax.add_patch(Circle((0.5, 0.63), 0.22, facecolor="#f8fafc", edgecolor=color, lw=3))
        label = f"{value:.1f}%" if title != "E-factor" else f"{value:.2f}"
        ax.text(0.5, 0.63, label, ha="center", va="center", fontsize=20, color=color, weight="bold")
        ax.text(0.5, 0.92, title, ha="center", fontsize=15, weight="bold")
        ax.text(0.5, 0.27, note, ha="center", va="center", fontsize=10.5)
    fig.suptitle(
        r"葡萄糖發酵：$C_6H_{12}O_6\rightarrow2C_2H_5OH+2CO_2$；三個指標回答不同問題",
        fontsize=15.5,
        y=0.99,
    )
    fig.subplots_adjust(left=0.02, right=0.99, bottom=0.04, top=0.82, wspace=0.06)
    return _save(fig, "選化V-2-綠色化學物料指標.svg")


def fig_model_cycle():
    """呈現模型目的、預測、殘差與修正的證據循環。"""
    observed = np.array([0.98, 0.86, 0.73, 0.57])
    predicted = np.array([1.00, 0.90, 0.80, 0.70])
    residual = observed - predicted
    assert np.all(residual <= 0.0)
    assert abs(residual[-1]) > abs(residual[0])

    fig, axes = plt.subplots(1, 2, figsize=(12.6, 5.8))
    ax = axes[0]
    ax.axis("off"); ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    nodes = [
        ((0.08, 0.65), "目的與尺度\n要預測什麼", F.BLUE),
        ((0.56, 0.65), "假設、變數\n與關係式", F.PURPLE),
        ((0.56, 0.25), "預測與\n不確定範圍", F.AMBER),
        ((0.08, 0.25), "觀測、殘差\n與替代解釋", F.GREEN),
    ]
    for (x, y), text, color in nodes:
        _box(ax, (x, y), 0.34, 0.18, text, fc="#f8fafc", ec=color, fs=11.3, lw=1.8)
    F.arrow(ax, (0.42, 0.74), (0.56, 0.74), color=F.INK, lw=2)
    F.arrow(ax, (0.73, 0.65), (0.73, 0.43), color=F.INK, lw=2)
    F.arrow(ax, (0.56, 0.34), (0.42, 0.34), color=F.INK, lw=2)
    F.arrow(ax, (0.25, 0.43), (0.25, 0.65), color=F.INK, lw=2)
    ax.text(0.5, 0.08, "殘差出現系統性方向時，需檢查假設或加入機制", ha="center", fontsize=10.3, color=F.RED)

    ax = axes[1]
    x = np.arange(1, 5)
    ax.plot(x, predicted, marker="o", lw=2.5, color=F.BLUE, label="模型預測")
    ax.plot(x, observed, marker="s", lw=2.5, color=F.RED, label="觀測")
    for xi, yp, yo in zip(x, predicted, observed):
        ax.plot([xi, xi], [yo, yp], ls="--", color=F.AMBER, lw=1.5)
    ax.set(xlabel="觀測階段", ylabel="相對量", ylim=(0.48, 1.06), title="殘差＝觀測值－模型預測值")
    ax.set_xticks(x); F.clean_grid(ax); ax.legend(frameon=False)
    ax.text(0.04, 0.06, "殘差由 −0.02 增至 −0.13，偏差具有方向性", transform=ax.transAxes, fontsize=10, color=F.RED)
    fig.suptitle("科學模型是有目的與適用尺度的可檢驗表示；修正依據來自證據", fontsize=15.5, y=0.99)
    fig.subplots_adjust(left=0.04, right=0.985, bottom=0.13, top=0.82, wspace=0.15)
    return _save(fig, "選化V-2-科學模型證據循環.svg")


def fig_ozone_cycles():
    """用反應循環顯示臭氧自然循環與氯自由基催化破壞。"""
    ozone_consumed = np.array([1, 1])
    chlorine_net = np.array([0, 0])
    assert ozone_consumed.sum() == 2
    assert chlorine_net.sum() == 0

    fig, axes = plt.subplots(1, 2, figsize=(13.0, 5.8))
    for ax in axes:
        ax.axis("off"); ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    ax = axes[0]
    ax.text(0.5, 0.94, "平流層臭氧的形成與自然消耗", ha="center", fontsize=14.3, weight="bold")
    _box(ax, (0.08, 0.69), 0.34, 0.14, r"$O_2+h\nu\rightarrow2O$", fc="#eef4ff", ec=F.BLUE, fs=12)
    _box(ax, (0.58, 0.69), 0.34, 0.14, r"$O+O_2+M\rightarrow O_3+M$", fc="#e8f5e9", ec=F.GREEN, fs=11.5)
    _box(ax, (0.58, 0.34), 0.34, 0.14, r"$O_3+h\nu\rightarrow O_2+O$", fc="#fff7dd", ec=F.AMBER, fs=11.5)
    _box(ax, (0.08, 0.34), 0.34, 0.14, r"$O+O_3\rightarrow2O_2$", fc="#fdecec", ec=F.RED, fs=11.5)
    F.arrow(ax, (0.42, 0.76), (0.58, 0.76), lw=2)
    F.arrow(ax, (0.75, 0.69), (0.75, 0.48), lw=2)
    F.arrow(ax, (0.58, 0.41), (0.42, 0.41), lw=2)
    F.arrow(ax, (0.25, 0.48), (0.25, 0.69), lw=2)
    ax.text(0.5, 0.13, r"$M$ 帶走碰撞能量；光解波長與高度決定速率", ha="center", fontsize=10.5, color=F.PURPLE)

    ax = axes[1]
    ax.text(0.5, 0.94, "氯自由基的催化循環", ha="center", fontsize=14.3, weight="bold")
    _box(ax, (0.11, 0.69), 0.78, 0.14, r"$Cl\cdot+O_3\rightarrow ClO\cdot+O_2$", fc="#fdecec", ec=F.RED, fs=12)
    _box(ax, (0.11, 0.43), 0.78, 0.14, r"$ClO\cdot+O\rightarrow Cl\cdot+O_2$", fc="#eef4ff", ec=F.BLUE, fs=12)
    F.arrow(ax, (0.50, 0.69), (0.50, 0.57), color=F.INK, lw=2)
    F.arrow(ax, (0.86, 0.43), (0.86, 0.83), color=F.GREEN, lw=2)
    ax.text(0.82, 0.62, r"$Cl\cdot$ 再生", rotation=90, ha="center", fontsize=10.5, color=F.GREEN)
    _box(ax, (0.17, 0.13), 0.66, 0.16, r"總反應：$O_3+O\rightarrow2O_2$" + "\nCl· 在總反應中相消", fc="#f8fafc", ec=F.PURPLE, fs=11.5)
    fig.suptitle("同一個氯自由基可重複參與反應；這就是催化破壞模型的放大機制", fontsize=15.5, y=0.99)
    fig.subplots_adjust(left=0.02, right=0.99, bottom=0.03, top=0.83, wspace=0.08)
    return _save(fig, "選化V-2-臭氧生成與氯自由基循環.svg")


def fig_ozone_column():
    """以同一柱面積連結 DU、分子數與標準狀況厚度。"""
    du = 300.0
    molecules_cm2 = du * 2.69e16
    thickness_mm = du * 0.01
    mol_m2 = molecules_cm2 * 1e4 / 6.02214076e23
    assert np.isclose(molecules_cm2, 8.07e18)
    assert np.isclose(thickness_mm, 3.0)
    assert np.isclose(mol_m2, 0.1340, atol=1e-4)

    fig, ax = plt.subplots(figsize=(11.8, 5.8))
    ax.axis("off"); ax.set_xlim(0, 12); ax.set_ylim(0, 6)
    ax.add_patch(Rectangle((0.8, 0.6), 2.4, 4.7, facecolor="#e0f2fe", edgecolor=F.BLUE, lw=2))
    for i in range(18):
        x = 1.05 + (i % 4) * 0.58
        y = 0.9 + (i // 4) * 0.92
        ax.add_patch(Circle((x, y), 0.08, color=F.PURPLE))
    ax.text(2.0, 5.55, r"大氣柱：底面積 $1\ cm^2$", ha="center", fontsize=12, weight="bold")
    F.arrow(ax, (3.45, 3.0), (5.0, 3.0), color=F.INK, lw=2.2)
    _box(ax, (5.0, 3.95), 2.75, 1.00, "300 DU\n=" + r"$8.07\times10^{18}$ 個 $O_3$/cm$^2$", fc="#eef4ff", ec=F.BLUE, fs=12)
    _box(ax, (5.0, 2.45), 2.75, 1.00, "換成 1 m$^2$\n" + rf"≈ {mol_m2:.3f} mol $O_3$", fc="#e8f5e9", ec=F.GREEN, fs=12)
    _box(ax, (8.35, 3.20), 2.75, 1.20, "壓到標準狀況\n純臭氧厚度 3.00 mm", fc="#fff7dd", ec=F.AMBER, fs=12)
    F.arrow(ax, (7.75, 3.0), (8.35, 3.75), color=F.INK, lw=2)
    ax.text(6.0, 0.75, "DU 是整個垂直氣柱的總量；它不直接給出某一高度的局部濃度", ha="center", fontsize=11, color=F.RED)
    return _save(fig, "選化V-2-臭氧柱量與杜布森單位.svg")


def fig_oxygen_demand():
    """由暗處五日 DO 資料生成 BOD5 圖，並顯示稀釋因子。"""
    days = np.arange(0, 6)
    do_control = np.array([8.7, 8.65, 8.62, 8.60, 8.58, 8.56])
    do_sample = np.array([8.6, 7.7, 6.9, 6.2, 5.6, 5.2])
    fraction = 0.20
    bod5 = (do_sample[0] - do_sample[-1]) / fraction
    assert np.isclose(bod5, 17.0)
    assert np.all(np.diff(do_sample) < 0)

    fig, axes = plt.subplots(1, 2, figsize=(12.3, 5.6))
    ax = axes[0]
    ax.plot(days, do_control, marker="o", lw=2.4, color=F.BLUE, label="稀釋水空白")
    ax.plot(days, do_sample, marker="s", lw=2.4, color=F.RED, label="20% 水樣")
    ax.fill_between(days, do_sample, do_control, color=F.AMBER, alpha=0.17)
    ax.set(xlabel="培養時間 / day", ylabel=r"DO / mg L$^{-1}$", ylim=(4.8, 9.0), title="20°C、暗處：以氧的下降量追蹤微生物氧化")
    F.clean_grid(ax); ax.legend(frameon=False)
    ax.annotate("第 5 日 5.2", (5, 5.2), xytext=(3.3, 5.45), arrowprops={"arrowstyle": "->", "color": F.RED}, color=F.RED)

    ax = axes[1]
    ax.axis("off"); ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    _box(ax, (0.10, 0.73), 0.80, 0.13, r"樣品比例 $P=0.20$", fc="#eef4ff", ec=F.BLUE, fs=13)
    _box(ax, (0.10, 0.48), 0.80, 0.14, r"稀釋瓶 DO 下降：$8.6-5.2=3.4$ mg L$^{-1}$", fc="#fff7dd", ec=F.AMBER, fs=12)
    _box(ax, (0.10, 0.19), 0.80, 0.17, r"$BOD_5=(D_1-D_2)/P=17$ mg L$^{-1}$", fc="#e8f5e9", ec=F.GREEN, fs=13)
    ax.text(0.5, 0.07, "溫度、暗處、培養時間、稀釋與種菌修正都屬方法條件", ha="center", fontsize=10.2, color=F.PURPLE)
    fig.suptitle(r"$BOD_5$ 以規定條件下的溶氧消耗估計可生物分解有機負荷", fontsize=15.5, y=0.99)
    fig.subplots_adjust(left=0.07, right=0.99, bottom=0.14, top=0.82, wspace=0.16)
    return _save(fig, "選化V-2-溶氧與生化需氧量.svg")


def fig_eutrophication():
    """用增肥實驗資料連結限制營養鹽與優養化因果鏈。"""
    treatments = ["對照", "+N", "+P", "+N+P"]
    chlorophyll = np.array([3.0, 4.2, 15.5, 20.4])
    assert chlorophyll[2] > 5 * chlorophyll[0]
    assert chlorophyll[3] > chlorophyll[2]

    fig, axes = plt.subplots(1, 2, figsize=(12.8, 5.8))
    ax = axes[0]
    ax.bar(treatments, chlorophyll, color=["#94a3b8", F.BLUE, F.AMBER, F.GREEN])
    ax.set(ylabel=r"葉綠素 a / μg L$^{-1}$", title="湖水瓶增肥試驗：觀測藻類量的反應")
    F.clean_grid(ax)
    ax.text(0.04, 0.91, "+P 的反應最大，P 是此時此地的重要限制因子", transform=ax.transAxes, fontsize=10.4, color=F.RED)

    ax = axes[1]
    ax.axis("off"); ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    chain = [
        ("N、P 輸入", F.BLUE),
        ("藻類快速增生", F.GREEN),
        ("遮光；藻體死亡", F.AMBER),
        ("分解者耗氧", F.PURPLE),
        ("底層低氧／缺氧", F.RED),
    ]
    for i, (label, color) in enumerate(chain):
        y = 0.83 - i * 0.17
        _box(ax, (0.18, y - 0.055), 0.64, 0.11, label, fc="#f8fafc", ec=color, fs=11.2)
        if i < len(chain) - 1:
            F.arrow(ax, (0.50, y - 0.055), (0.50, y - 0.115), color=F.INK, lw=1.8)
    ax.text(0.5, 0.05, "白天表層光合作用可使 DO 暫升；夜間與底層趨勢可能相反", ha="center", fontsize=10, color=F.RED)
    fig.suptitle("優養化推論需同時有營養鹽反應資料與氧傳輸／分解機制", fontsize=15.3, y=0.99)
    fig.subplots_adjust(left=0.06, right=0.99, bottom=0.11, top=0.82, wspace=0.12)
    return _save(fig, "選化V-2-優養化因果與資料.svg")


def fig_biomagnification():
    """以對數尺度區分生物濃縮與食物鏈放大。"""
    labels = ["水", "浮游生物", "小魚", "大型魚", "魚食鳥"]
    concentration = np.array([0.0002, 0.020, 0.60, 1.50, 3.00])
    factors = concentration[1:] / concentration[:-1]
    assert np.isclose(concentration[1] / concentration[0], 100.0)
    assert np.all(factors > 1)

    fig, axes = plt.subplots(1, 2, figsize=(12.6, 5.5))
    ax = axes[0]
    ax.plot(labels, concentration, marker="o", lw=2.8, color=F.PURPLE)
    ax.set_yscale("log")
    ax.set(ylabel=r"污染物濃度 / mg kg$^{-1}$（示例資料）", title="跨營養階層濃度上升：生物放大")
    F.clean_grid(ax)
    ax.text(0.03, 0.92, "縱軸為對數尺度", transform=ax.transAxes, fontsize=10.5, color=F.RED)

    ax = axes[1]
    ax.axis("off"); ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    _box(ax, (0.08, 0.68), 0.84, 0.17, "生物濃縮\n生物體濃度 ÷ 周遭介質濃度", fc="#eef4ff", ec=F.BLUE, fs=12)
    ax.text(0.5, 0.58, "水 → 浮游生物：0.020 ÷ 0.0002 = 100", ha="center", fontsize=11)
    _box(ax, (0.08, 0.31), 0.84, 0.17, "生物放大\n捕食者濃度 ÷ 食物濃度", fc="#fff7dd", ec=F.AMBER, fs=12)
    ax.text(0.5, 0.20, "小魚 → 大型魚：1.50 ÷ 0.60 = 2.5", ha="center", fontsize=11)
    ax.text(0.5, 0.07, "需同時考慮脂溶性、難分解性、食性、年齡與組織差異", ha="center", fontsize=10, color=F.PURPLE)
    fig.suptitle("同一組濃度資料可回答體內累積與營養階層傳遞兩種不同問題", fontsize=15.3, y=0.99)
    fig.subplots_adjust(left=0.08, right=0.99, bottom=0.15, top=0.82, wspace=0.17)
    return _save(fig, "選化V-2-生物累積與食物鏈放大.svg")


def fig_water_test():
    """整合水質實驗的操作、觀察、推論與電凝電極方向。"""
    voltage = 7.0
    time_min = 3.0
    charge_if_02a = 0.20 * time_min * 60
    assert np.isclose(charge_if_02a, 36.0)
    assert voltage > 0 and time_min > 0

    fig, axes = plt.subplots(1, 3, figsize=(13.4, 6.1))
    for ax in axes:
        ax.axis("off"); ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    ax = axes[0]
    ax.text(0.5, 0.95, "檢測：量的是哪個性質", ha="center", fontsize=14, weight="bold")
    items = [
        ("pH 計（校正後）", "氫離子活度的操作量", F.BLUE),
        ("側向散射光／NTU", "懸浮粒子的光學效應", F.PURPLE),
        ("溶氧比色或電極", "DO 濃度；需記錄溫度", F.GREEN),
    ]
    for i, (a, b, c) in enumerate(items):
        y = 0.75 - i * 0.25
        _box(ax, (0.07, y - 0.07), 0.86, 0.15, a + "\n" + b, fc="#f8fafc", ec=c, fs=10.6)
    ax.text(0.5, 0.08, "目視清澈不代表微生物、離子或溶解有機物合格", ha="center", fontsize=9.8, color=F.RED)

    ax = axes[1]
    ax.text(0.5, 0.95, "明礬混凝＋沉澱＋過濾", ha="center", fontsize=14, weight="bold")
    chain = ["加入明礬並快速混合", r"形成 $Al(OH)_3$ 絮體", "吸附／網捕膠體", "沉澱後再過濾"]
    for i, label in enumerate(chain):
        y = 0.79 - i * 0.20
        _box(ax, (0.10, y - 0.055), 0.80, 0.11, label, fc="#eef4ff" if i % 2 == 0 else "#fff7dd", ec=F.BLUE if i % 2 == 0 else F.AMBER, fs=10.8)
        if i < 3:
            F.arrow(ax, (0.50, y - 0.055), (0.50, y - 0.12), lw=1.7)
    ax.text(0.5, 0.08, "pH 與鹼度影響絮體形成；混凝後仍需後續消毒", ha="center", fontsize=9.8, color=F.RED)

    ax = axes[2]
    ax.text(0.5, 0.95, "電凝：直流約 7 V、3 min", ha="center", fontsize=14, weight="bold")
    ax.add_patch(Rectangle((0.12, 0.23), 0.76, 0.46, fill=False, edgecolor=F.INK, lw=1.8))
    ax.add_patch(Rectangle((0.14, 0.25), 0.72, 0.30, facecolor="#dbeafe", edgecolor="none"))
    ax.add_patch(Rectangle((0.25, 0.34), 0.08, 0.42, facecolor="#94a3b8", edgecolor=F.INK))
    ax.add_patch(Rectangle((0.67, 0.34), 0.08, 0.42, facecolor="#b45309", edgecolor=F.INK))
    ax.text(0.29, 0.81, "Al 陽極（+）", ha="center", fontsize=10.5, color=F.RED)
    ax.text(0.71, 0.81, "Cu 陰極（−）", ha="center", fontsize=10.5, color=F.BLUE)
    ax.text(0.29, 0.14, r"$Al\rightarrow Al^{3+}+3e^-$", ha="center", fontsize=9.8)
    ax.text(0.72, 0.14, r"$2H_2O+2e^-\rightarrow H_2+2OH^-$", ha="center", fontsize=9.6)
    for x in [0.42, 0.50, 0.58]:
        ax.add_patch(Circle((x, 0.40 + 0.10 * (x > 0.5)), 0.035, color=F.AMBER, alpha=0.8))
    ax.text(0.5, 0.04, "生成金屬氫氧化物絮體；氣泡可帶動部分絮體上浮", ha="center", fontsize=9.6, color=F.PURPLE)
    fig.suptitle("水質實驗把檢測與處理分開：操作 → 觀察 → 化學證據 → 推論", fontsize=15.5, y=0.99)
    fig.subplots_adjust(left=0.015, right=0.995, bottom=0.03, top=0.84, wspace=0.05)
    return _save(fig, "選化V-2-水質檢測與淨化證據鏈.svg")


def fig_air_network():
    """用反應網路區分一次排放與二次生成污染物。"""
    atoms_left = {"N": 1, "O": 2}
    atoms_right = {"N": 1, "O": 1 + 1}
    assert atoms_left == atoms_right

    fig, ax = plt.subplots(figsize=(12.8, 6.6))
    ax.axis("off"); ax.set_xlim(0, 12.8); ax.set_ylim(0, 6.6)
    _box(ax, (5.15, 5.18), 2.50, 0.72, "燃燒／交通／工業：一次排放", fc="#f8fafc", ec=F.INK, fs=12)
    primaries = [(r"NO、$NO_2$", 1.60, F.BLUE), (r"$SO_2$", 4.60, F.AMBER), ("CO、VOC", 7.60, F.PURPLE), ("一次 PM", 10.80, F.RED)]
    for label, x, color in primaries:
        _box(ax, (x - 1.00, 3.92), 2.00, 0.72, label, fc="#eef4ff", ec=color, fs=11.5)
        F.arrow(ax, (6.40, 5.18), (x, 4.64), color=color, lw=1.8)
    _box(ax, (0.35, 2.08), 2.80, 1.02, r"$NO_x$＋VOC＋日照" + "\n" + r"$NO_2+h\nu\rightarrow NO+O$" + "\n" + r"$O+O_2\rightarrow O_3$", fc="#fff7dd", ec=F.AMBER, fs=9.9)
    _box(ax, (3.40, 2.08), 2.80, 1.02, r"$SO_2$、$NO_x$ 氧化" + "\n＋水 → 酸性物種", fc="#fdecec", ec=F.RED, fs=10.8)
    _box(ax, (6.45, 2.08), 2.80, 1.02, "VOC 氧化產物凝結\n＋硫酸鹽／硝酸鹽", fc="#f3e8ff", ec=F.PURPLE, fs=10.6)
    _box(ax, (9.50, 2.08), 2.80, 1.02, "一次粒子傳輸、混合\n與乾／濕沉降", fc="#f8fafc", ec=F.RED, fs=10.6)
    for x1, x2 in [(1.60, 1.75), (4.60, 4.80), (7.60, 7.85), (10.80, 10.90)]:
        F.arrow(ax, (x1, 3.92), (x2, 3.10), lw=2)
    _box(ax, (0.35, 0.52), 2.80, 0.68, r"近地面 $O_3$／光化學煙霧", fc="#fff7dd", ec=F.AMBER, fs=11.2)
    _box(ax, (3.40, 0.52), 2.80, 0.68, "酸沉降", fc="#fdecec", ec=F.RED, fs=11.2)
    _box(ax, (6.45, 0.52), 2.80, 0.68, r"二次 $PM_{2.5}$", fc="#f3e8ff", ec=F.PURPLE, fs=11.2)
    _box(ax, (9.50, 0.52), 2.80, 0.68, "受體處一次 PM", fc="#f8fafc", ec=F.RED, fs=11.2)
    for x in [1.75, 4.80, 7.85, 10.90]:
        F.arrow(ax, (x, 2.08), (x, 1.20), lw=2)
    ax.text(6.4, 6.35, "來源清單只告訴排放；反應、光照、濕度與傳輸決定實際暴露", ha="center", fontsize=14.5, weight="bold")
    return _save(fig, "選化V-2-一次與二次空氣污染物.svg")


def fig_aqi():
    """以題目提供的教學斷點做線性內插，驗證 AQI 取最大分指標。"""
    # 教學斷點，不代表現行法規表。
    o3_break = np.array([50.0, 70.0])
    pm_break = np.array([20.0, 35.0])
    i_break = np.array([50.0, 100.0])
    o3_c, pm_c = 62.0, 32.0
    o3_i = (o3_c - o3_break[0]) / np.diff(o3_break)[0] * 50 + 50
    pm_i = (pm_c - pm_break[0]) / np.diff(pm_break)[0] * 50 + 50
    overall = max(o3_i, pm_i)
    assert np.isclose(o3_i, 80.0)
    assert np.isclose(pm_i, 90.0)
    assert np.isclose(overall, 90.0)

    fig, axes = plt.subplots(1, 2, figsize=(12.4, 5.6))
    ax = axes[0]
    c_o3 = np.linspace(50, 70, 100)
    i_o3 = 50 + (c_o3 - 50) / 20 * 50
    c_pm = np.linspace(20, 35, 100)
    i_pm = 50 + (c_pm - 20) / 15 * 50
    o3_line, = ax.plot(
        c_o3,
        i_o3,
        color=F.BLUE,
        lw=2.5,
        linestyle="-",
        marker="o",
        markevery=12,
        markersize=5.2,
        label=r"$O_3$ 教學斷點",
    )
    pm_line, = ax.plot(
        c_pm,
        i_pm,
        color=F.PURPLE,
        lw=2.5,
        linestyle="--",
        marker="s",
        markevery=12,
        markersize=5.2,
        label=r"$PM_{2.5}$ 教學斷點",
    )
    assert o3_line.get_linestyle() != pm_line.get_linestyle()
    assert o3_line.get_marker() != pm_line.get_marker()
    ax.scatter([o3_c], [o3_i], color=F.BLUE, marker="o", s=70, zorder=5)
    ax.scatter([pm_c], [pm_i], color=F.PURPLE, marker="s", s=70, zorder=5)
    ax.set(xlabel="題目給定的濃度數值", ylabel="分指標 I", ylim=(45, 105), title="每一污染物先依自己的斷點換算")
    F.clean_grid(ax); ax.legend(frameon=False)

    ax = axes[1]
    ax.axis("off"); ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    _box(ax, (0.10, 0.73), 0.80, 0.14, rf"$O_3$：62 → 分指標 {o3_i:.0f}", fc="#eef4ff", ec=F.BLUE, fs=13)
    _box(ax, (0.10, 0.51), 0.80, 0.14, rf"$PM_{{2.5}}$：32 → 分指標 {pm_i:.0f}", fc="#f3e8ff", ec=F.PURPLE, fs=13)
    _box(ax, (0.10, 0.23), 0.80, 0.17, f"AQI = max(80, 90) = {overall:.0f}\n" + r"主導污染物：$PM_{2.5}$", fc="#fff7dd", ec=F.AMBER, fs=13)
    ax.text(0.5, 0.08, "AQI 是時空聚合的溝通指標；個人劑量還受停留時間與活動位置影響", ha="center", fontsize=9.9, color=F.RED)
    fig.suptitle("空氣品質指標先標準化各污染物，再以最大分指標代表當時風險等級", fontsize=15.3, y=0.99)
    fig.subplots_adjust(left=0.07, right=0.99, bottom=0.14, top=0.82, wspace=0.17)
    return _save(fig, "選化V-2-AQI分指標與最大值.svg")


def fig_nitrogen_cycle():
    """將主要氮循環過程連到化學物種與平均氧化數。"""
    states = {"N2": 0, "NH4": -3, "NO2": 3, "NO3": 5}
    assert states["NH4"] < states["NO2"] < states["NO3"]
    assert states["N2"] == 0

    fig, ax = plt.subplots(figsize=(12.8, 6.5))
    ax.axis("off"); ax.set_xlim(0, 12.8); ax.set_ylim(0, 6.5)
    positions = {
        r"大氣 $N_2$" + "\nN：0": (5.2, 5.15),
        r"$NH_4^+$" + "\nN：−3": (1.0, 2.95),
        r"$NO_2^-$" + "\nN：+3": (4.0, 2.95),
        r"$NO_3^-$" + "\nN：+5": (7.0, 2.95),
        "生物有機氮": (9.9, 2.95),
    }
    colors = [F.BLUE, F.AMBER, F.PURPLE, F.RED, F.GREEN]
    boxes = {}
    for ((label, (x, y)), color) in zip(positions.items(), colors):
        boxes[label] = _box(ax, (x, y), 1.9, 0.85, label, fc="#f8fafc", ec=color, fs=11.5, lw=1.8)
    F.arrow(ax, (6.15, 5.15), (1.95, 3.80), color=F.BLUE, lw=2.1)
    ax.text(3.45, 4.62, "固氮", fontsize=10.5, color=F.BLUE)
    F.arrow(ax, (2.90, 3.37), (4.0, 3.37), color=F.AMBER, lw=2.1)
    F.arrow(ax, (5.90, 3.37), (7.0, 3.37), color=F.PURPLE, lw=2.1)
    ax.text(4.95, 3.82, "硝化：需氧、氧化", ha="center", fontsize=10.5, color=F.RED)
    F.arrow(ax, (8.90, 3.37), (9.9, 3.37), color=F.GREEN, lw=2.1)
    ax.text(9.38, 3.73, "同化", ha="center", fontsize=10.5, color=F.GREEN)
    F.arrow(ax, (10.55, 2.95), (2.35, 2.45), color=F.AMBER, lw=2.1)
    ax.text(6.2, 2.02, "死亡／排泄後的氨化作用", ha="center", fontsize=10.5, color=F.AMBER)
    F.arrow(ax, (7.95, 3.80), (6.15, 5.15), color=F.BLUE, lw=2.1)
    ax.text(7.45, 4.63, "反硝化：缺氧、還原", fontsize=10.5, color=F.BLUE)
    ax.text(6.4, 0.72, "物質循環不等於能量循環；每一箭頭都有微生物、氧化還原與環境條件", ha="center", fontsize=11.2, color=F.PURPLE)
    ax.text(6.4, 6.15, "氮循環用物種、氧化態與環境條件描述轉化方向", ha="center", fontsize=15.5, weight="bold")
    return _save(fig, "選化V-2-氮循環物種與氧化態.svg")


def fig_nitrogen_budget():
    """以質量平衡驗證農田氮的輸入、輸出與殘差。"""
    input_n = 100.0
    flows = {"作物收穫": 55.0, "反硝化": 15.0, "揮發": 10.0, "土壤暫存": 5.0, "淋洗／逕流": 15.0}
    assert np.isclose(sum(flows.values()), input_n)

    fig, ax = plt.subplots(figsize=(12.5, 5.8))
    ax.axis("off"); ax.set_xlim(0, 12.5); ax.set_ylim(0, 5.8)
    _box(ax, (0.45, 2.15), 2.35, 1.20, r"施肥輸入" + "\n" + r"100 kg N ha$^{-1}$", fc="#eef4ff", ec=F.BLUE, fs=13, lw=2)
    _box(ax, (4.65, 1.85), 2.70, 1.80, "農田控制體\n輸入＝輸出＋暫存\n未知量由差額求得", fc="#e8f5e9", ec=F.GREEN, fs=13, lw=2)
    F.arrow(ax, (2.80, 2.75), (4.65, 2.75), color=F.BLUE, lw=3)
    destinations = [("作物收穫\n55", 9.05, 4.55, F.GREEN), ("氣體：反硝化 15\n＋揮發 10", 9.05, 3.10, F.PURPLE), ("土壤暫存\n5", 9.05, 1.65, F.AMBER), ("淋洗／逕流\n15", 9.05, 0.20, F.RED)]
    for label, x, y, color in destinations:
        _box(ax, (x, y), 2.65, 0.90, label, fc="#f8fafc", ec=color, fs=11.2)
        F.arrow(ax, (7.35, 2.75), (x, y + 0.45), color=color, lw=2)
    ax.text(6.25, 5.48, "尺度固定為每公頃、同一季；所有通量都用 kg N", ha="center", fontsize=14.5, weight="bold")
    ax.text(6.25, 0.25, "若只量輸入與收穫，差額包含多個路徑，不能直接全稱為污染流失", ha="center", fontsize=10.5, color=F.RED)
    return _save(fig, "選化V-2-農田氮收支.svg")


def fig_energy_boundary():
    """比較相同功能單位下的生命週期階段與直接排放。"""
    stages = ["取得／製造", "運輸／建置", "運轉", "退役／回收"]
    gas = np.array([12, 5, 49, 2])
    solar = np.array([34, 8, 1, 4])
    biomass = np.array([25, 12, 10, 8])
    assert gas.sum() == 68 and solar.sum() == 47 and biomass.sum() == 55
    assert solar[2] < gas[2]

    fig, axes = plt.subplots(1, 2, figsize=(13.0, 5.8))
    ax = axes[0]
    bottom = np.zeros(3)
    colors = [F.BLUE, F.AMBER, F.RED, F.GREEN]
    for j, stage in enumerate(stages):
        values = np.array([gas[j], solar[j], biomass[j]])
        ax.bar(["天然氣", "太陽光電", "生質能"], values, bottom=bottom, label=stage, color=colors[j])
        bottom += values
    ax.set(ylabel=r"示例生命週期排放 / g CO$_2$e MJ$^{-1}$", title="功能單位相同，邊界包含四階段")
    F.clean_grid(ax); ax.legend(frameon=False, fontsize=9)

    ax = axes[1]
    ax.axis("off"); ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    _box(ax, (0.08, 0.76), 0.84, 0.12, "功能單位：交付 1 MJ 可用能", fc="#eef4ff", ec=F.BLUE, fs=12)
    chain = ["原料／設備", "運輸與建置", "轉換與運轉", "退役／回收"]
    for i, label in enumerate(chain):
        x = 0.04 + i * 0.24
        _box(ax, (x, 0.45), 0.20, 0.14, label, fc="#f8fafc", ec=colors[i], fs=9.5)
        if i < 3:
            F.arrow(ax, (x + 0.20, 0.52), (x + 0.24, 0.52), lw=1.5)
    _box(ax, (0.12, 0.13), 0.76, 0.18, "另列性能：可調度性、能量密度、土地／水、\n甲烷逸散、材料毒性與不確定度", fc="#fff7dd", ec=F.AMBER, fs=10.8)
    ax.text(0.5, 0.04, "單一排放數值不能代替全部工程與環境判斷", ha="center", fontsize=10, color=F.RED)
    fig.suptitle("能源比較先固定功能單位與系統邊界，再讀取排放、性能與限制", fontsize=15.5, y=0.99)
    fig.subplots_adjust(left=0.06, right=0.99, bottom=0.12, top=0.82, wspace=0.14)
    return _save(fig, "選化V-2-能源生命週期邊界.svg")


def main():
    fig_green_metrics()
    fig_model_cycle()
    fig_ozone_cycles()
    fig_ozone_column()
    fig_oxygen_demand()
    fig_eutrophication()
    fig_biomagnification()
    fig_water_test()
    fig_air_network()
    fig_aqi()
    fig_nitrogen_cycle()
    fig_nitrogen_budget()
    fig_energy_boundary()


if __name__ == "__main__":
    main()
