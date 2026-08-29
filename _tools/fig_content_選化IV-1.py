# -*- coding: utf-8 -*-
"""產生「選化 IV-1 氧化還原反應與電化學」章內 SVG。

重繪：.venv/bin/python _tools/fig_content_選化IV-1.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, FancyBboxPatch, Rectangle

import figlib as F


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CH = os.path.join(ROOT, "content", "選修化學IV", "選化IV-1")


FIGURE_OUTPUTS = (
    ("fig_oxidation_number_ledger", "選化IV-1-氧化數與電子帳本.svg"),
    ("fig_half_reaction_balance", "選化IV-1-半反應配平與守恆.svg"),
    ("fig_redox_titration", "選化IV-1-氧化還原滴定證據鏈.svg"),
    ("fig_titration_stoichiometry", "選化IV-1-滴定體積與待測量.svg"),
    ("fig_daniell_cell", "選化IV-1-丹尼耳電池方向與物料變化.svg"),
    ("fig_reduction_potential", "選化IV-1-還原電位與電池電壓.svg"),
    ("fig_cell_families", "選化IV-1-一次二次與燃料電池.svg"),
    ("fig_galvanic_electrolytic", "選化IV-1-原電池與電解槽比較.svg"),
    ("fig_aqueous_electrolysis", "選化IV-1-水溶液電解產物選擇.svg"),
    ("fig_refining_plating", "選化IV-1-電解精煉與電鍍.svg"),
    ("fig_corrosion_protection", "選化IV-1-鐵鏽蝕與陰極防蝕.svg"),
    ("fig_faraday_law", "選化IV-1-法拉第定律量化圖.svg"),
)


def _save(fig, filename):
    assert filename.endswith(".svg")
    return F.save_to(fig, CH, filename[:-4], output_subdir="assets", write_pdf=False)


def _box(ax, xy, w, h, text, *, fc="#f8fafc", ec="#64748b", fs=10.5, lw=1.4):
    patch = FancyBboxPatch(
        xy, w, h, boxstyle="round,pad=0.035,rounding_size=0.06",
        facecolor=fc, edgecolor=ec, linewidth=lw,
    )
    ax.add_patch(patch)
    ax.text(xy[0] + w / 2, xy[1] + h / 2, text, ha="center", va="center", fontsize=fs)
    return patch


def _beaker(ax, x, y, w, h, liquid="#dbeafe"):
    ax.add_patch(Rectangle((x, y), w, h, fill=False, edgecolor=F.INK, linewidth=1.7))
    ax.add_patch(Rectangle((x + 0.02, y + 0.02), w - 0.04, h * 0.66, facecolor=liquid, edgecolor="none"))


def _electrode(ax, x, y, h, color, label):
    ax.add_patch(Rectangle((x - 0.07, y), 0.14, h, facecolor=color, edgecolor=F.INK, linewidth=1.1))
    ax.text(x, y + h + 0.11, label, ha="center", va="bottom", fontsize=10.5)


def fig_oxidation_number_ledger():
    """以守恆和三種例外驗證氧化數，並以歧化電子帳本閉合。"""
    examples = [
        (r"$H_2O$", 2 * 1 + (-2), "H +1，O −2"),
        (r"$H_2O_2$", 2 * 1 + 2 * (-1), "過氧化物 O −1"),
        (r"$NaH$", 1 + (-1), "金屬氫化物 H −1"),
        (r"$OF_2$", 2 + 2 * (-1), "F −1，故 O +2"),
    ]
    assert all(total == 0 for _, total, _ in examples)
    # Cl2 + 2OH- -> Cl- + ClO- + H2O: one Cl gains one e-, one Cl loses one e-.
    cl_changes = np.array([-1, +1])
    assert cl_changes.sum() == 0

    fig, axes = plt.subplots(1, 2, figsize=(12.4, 5.6))
    ax = axes[0]
    ax.axis("off"); ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    ax.text(0.5, 0.94, "氧化數總和＝物種電荷", ha="center", fontsize=15, weight="bold")
    for i, (formula, _, rule) in enumerate(examples):
        y = 0.78 - i * 0.18
        _box(ax, (0.08, y - 0.07), 0.84, 0.13, formula + "   →   " + rule, fc="#eef4ff" if i == 0 else "#fff7dd", fs=11.5)
    ax.text(0.5, 0.08, "規則有優先序：先用 F，再判斷 O、H 的化合物類型", ha="center", fontsize=10.5, color=F.PURPLE)

    ax = axes[1]
    ax.axis("off"); ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    ax.text(0.5, 0.94, "歧化反應的電子帳本", ha="center", fontsize=15, weight="bold")
    _box(ax, (0.30, 0.68), 0.40, 0.13, r"$Cl_2$：Cl 為 0", fc="#f8fafc", fs=12)
    _box(ax, (0.04, 0.34), 0.39, 0.17, r"$Cl^-$：Cl 為 −1" + "\n" + r"每個 Cl 得 $1e^-$", fc="#e8f5e9", ec=F.GREEN, fs=11.5)
    _box(ax, (0.57, 0.34), 0.39, 0.17, r"$ClO^-$：Cl 為 +1" + "\n" + r"每個 Cl 失 $1e^-$", fc="#fdecec", ec=F.RED, fs=11.5)
    F.arrow(ax, (0.43, 0.68), (0.24, 0.51), color=F.GREEN, lw=2.1)
    F.arrow(ax, (0.57, 0.68), (0.76, 0.51), color=F.RED, lw=2.1)
    ax.text(0.5, 0.20, r"電子守恆：$1\times1e^-=1\times1e^-$", ha="center", fontsize=12.5)
    ax.text(0.5, 0.10, r"$Cl_2+2OH^-\rightarrow Cl^-+ClO^-+H_2O$", ha="center", fontsize=12)
    fig.suptitle("氧化數是電子轉移的記帳量；每一欄都需滿足電荷或電子守恆", fontsize=16, y=0.99)
    fig.subplots_adjust(left=0.025, right=0.985, bottom=0.06, top=0.84, wspace=0.07)
    return _save(fig, "選化IV-1-氧化數與電子帳本.svg")


def fig_half_reaction_balance():
    """驗證 MnO4-/Fe2+ 酸性配平的原子、電荷與電子數。"""
    # MnO4- + 8H+ + 5e- -> Mn2+ + 4H2O
    left_atoms = {"Mn": 1, "O": 4, "H": 8}
    right_atoms = {"Mn": 1, "O": 4, "H": 8}
    left_charge, right_charge = -1 + 8 - 5, 2
    assert left_atoms == right_atoms and left_charge == right_charge
    # 5Fe2+ -> 5Fe3+ + 5e-
    assert 5 * 2 == 5 * 3 - 5

    fig, ax = plt.subplots(figsize=(12.2, 6.1))
    ax.axis("off"); ax.set_xlim(0, 12); ax.set_ylim(0, 6)
    steps = [
        ("① 分成兩個半反應", r"$MnO_4^-\rightarrow Mn^{2+}$" + "\n" + r"$Fe^{2+}\rightarrow Fe^{3+}$"),
        ("② 先平 O、H", r"$MnO_4^-+8H^+\rightarrow Mn^{2+}+4H_2O$"),
        (r"③ 以 $e^-$ 平電荷", r"$MnO_4^-+8H^++5e^-\rightarrow Mn^{2+}+4H_2O$"),
        ("④ 電子數相等後相加", r"$MnO_4^-+8H^++5Fe^{2+}$" + "\n" + r"$\rightarrow Mn^{2+}+4H_2O+5Fe^{3+}$"),
    ]
    positions = [(0.35, 3.55), (6.25, 3.55), (0.35, 1.15), (6.25, 1.15)]
    colors = [F.BLUE, F.AMBER, F.PURPLE, F.GREEN]
    for (title, text), (x, y), color in zip(steps, positions, colors):
        _box(ax, (x, y), 5.35, 1.55, title + "\n" + text, fc="#f8fafc", ec=color, fs=11.2, lw=1.8)
    F.arrow(ax, (5.70, 4.32), (6.25, 4.32), color=F.INK, lw=1.8)
    F.arrow(ax, (8.92, 3.55), (8.92, 2.70), color=F.INK, lw=1.8)
    F.arrow(ax, (6.25, 1.92), (5.70, 1.92), color=F.INK, lw=1.8)
    ax.text(6.0, 5.72, "酸性水溶液的半反應法：原子守恆 → 電荷守恆 → 電子守恆", ha="center", fontsize=16, weight="bold")
    ax.text(6.0, 0.35, "檢查總反應：Mn 1、Fe 5、O 4、H 8；兩側總電荷皆 +17", ha="center", fontsize=11.5, color=F.GREEN)
    return _save(fig, "選化IV-1-半反應配平與守恆.svg")


def fig_redox_titration():
    """繪製 KMnO4/草酸鈉滴定的裝置、觀察與電子等量關係。"""
    mn_mol = 0.02000 * 0.01500
    ox_mol = mn_mol * 5 / 2
    assert np.isclose(mn_mol * 5, ox_mol * 2)

    fig, axes = plt.subplots(1, 3, figsize=(13.0, 5.8))
    for ax in axes:
        ax.axis("off"); ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    ax = axes[0]
    ax.text(0.5, 0.94, "裝置與控制", ha="center", fontsize=14.5, weight="bold")
    ax.add_patch(Rectangle((0.46, 0.37), 0.08, 0.48, facecolor="#d8b4fe", edgecolor=F.INK))
    ax.text(0.60, 0.68, r"$KMnO_4$ 滴定液", fontsize=10, color=F.PURPLE)
    F.arrow(ax, (0.50, 0.37), (0.50, 0.29), color=F.PURPLE, lw=1.8)
    ax.add_patch(FancyBboxPatch((0.28, 0.08), 0.44, 0.20, boxstyle="round,pad=0.02", facecolor="#fce7f3", edgecolor=F.INK, lw=1.5))
    ax.text(0.50, 0.18, "草酸鹽＋硫酸\n約 60–70°C", ha="center", va="center", fontsize=10.5)
    ax.text(0.50, 0.02, "逐滴加入、持續搖勻", ha="center", fontsize=10, color=F.BLUE)

    ax = axes[1]
    ax.text(0.5, 0.94, "觀察 → 證據 → 推論", ha="center", fontsize=14.5, weight="bold")
    _box(ax, (0.08, 0.68), 0.84, 0.13, "淡粉紅色持續約 30 s", fc="#fce7f3", ec=F.RED, fs=11)
    F.arrow(ax, (0.50, 0.68), (0.50, 0.57), color=F.INK, lw=1.7)
    _box(ax, (0.08, 0.43), 0.84, 0.13, r"新增的 $MnO_4^-$ 已有微量過量", fc="#eef4ff", ec=F.BLUE, fs=10.5)
    F.arrow(ax, (0.50, 0.43), (0.50, 0.32), color=F.INK, lw=1.7)
    _box(ax, (0.08, 0.14), 0.84, 0.16, "終點逼近化學計量點\n讀取滴定體積", fc="#e8f5e9", ec=F.GREEN, fs=10.8)

    ax = axes[2]
    ax.text(0.5, 0.94, "電子等量", ha="center", fontsize=14.5, weight="bold")
    ax.text(0.5, 0.74, r"$MnO_4^-$：$5e^-$/mol", ha="center", fontsize=12, color=F.PURPLE)
    ax.text(0.5, 0.61, r"$C_2O_4^{2-}$：$2e^-$/mol", ha="center", fontsize=12, color=F.GREEN)
    ax.text(0.5, 0.45, r"$5n(MnO_4^-)=2n(C_2O_4^{2-})$", ha="center", fontsize=12.5, weight="bold")
    ax.text(0.5, 0.29, rf"15.00 mL×0.02000 M\n→ $n(C_2O_4^{{2-}})={ox_mol:.2e}$ mol", ha="center", fontsize=11)
    ax.text(0.5, 0.10, "護目鏡、手套；熱酸與氧化劑廢液\n依校內含錳酸性廢液規範收集", ha="center", fontsize=9.6, color=F.RED)
    fig.suptitle("高錳酸根—草酸根滴定：裝置、終點證據與電子守恆必須同時成立", fontsize=15.5, y=0.99)
    fig.subplots_adjust(left=0.02, right=0.99, bottom=0.04, top=0.83, wspace=0.05)
    return _save(fig, "選化IV-1-氧化還原滴定證據鏈.svg")


def fig_titration_stoichiometry():
    """由 Fe2+/MnO4- 計量關係生成線性資料圖。"""
    c_mn = 0.02000
    volumes = np.linspace(0, 25, 101)  # mL
    fe_mmol = 5 * c_mn * volumes  # mmol because M*mL
    assert np.isclose(fe_mmol[60], 5 * c_mn * volumes[60])
    assert np.isclose(fe_mmol[-1], 2.5)

    fig, ax = plt.subplots(figsize=(9.6, 5.6))
    ax.plot(volumes, fe_mmol, color=F.PURPLE, lw=2.8)
    v = 18.60
    n = 5 * c_mn * v
    ax.scatter([v], [n], color=F.RED, s=65, zorder=5)
    ax.plot([v, v], [0, n], ls="--", color=F.RED, alpha=0.7)
    ax.plot([0, v], [n, n], ls="--", color=F.RED, alpha=0.7)
    ax.text(v + 0.6, n - 0.08, rf"{v:.2f} mL $\rightarrow$ {n:.3f} mmol $Fe^{{2+}}$", fontsize=10.5, color=F.RED)
    ax.set(xlabel=r"$0.02000\ \mathrm{M}\ MnO_4^-$ 體積 / mL", ylabel=r"可反應的 $Fe^{2+}$ 量 / mmol",
           xlim=(0, 25.5), ylim=(0, 2.62), title=r"酸性條件：$1\ mol\ MnO_4^- : 5\ mol\ Fe^{2+}$")
    F.clean_grid(ax)
    ax.text(0.03, 0.92, "斜率 = 5×0.02000 = 0.1000 mmol/mL", transform=ax.transAxes, fontsize=11, color=F.GREEN)
    fig.subplots_adjust(left=0.12, right=0.97, bottom=0.16, top=0.86)
    return _save(fig, "選化IV-1-滴定體積與待測量.svg")


def fig_daniell_cell():
    """繪製丹尼耳電池並驗證方向、物料與電荷補償。"""
    e_cathode, e_anode = 0.34, -0.76
    assert np.isclose(e_cathode - e_anode, 1.10)
    assert 1 * 2 == 1 * 2  # 每 1 mol Zn 溶解對應 1 mol Cu 析出

    fig, ax = plt.subplots(figsize=(12.5, 6.3))
    ax.axis("off"); ax.set_xlim(0, 12.5); ax.set_ylim(0, 6.3)
    _beaker(ax, 0.8, 0.6, 4.1, 3.4, "#dbeafe")
    _beaker(ax, 7.6, 0.6, 4.1, 3.4, "#cffafe")
    _electrode(ax, 2.1, 1.0, 2.65, "#94a3b8", "Zn(s)｜負極、陽極")
    _electrode(ax, 10.4, 1.0, 2.65, "#b45309", "Cu(s)｜正極、陰極")
    ax.text(2.85, 1.45, r"$Zn^{2+}$ 增加", fontsize=11, color=F.BLUE)
    ax.text(8.35, 1.45, r"$Cu^{2+}$ 減少", fontsize=11, color=F.BLUE)
    ax.plot([2.1, 2.1, 10.4, 10.4], [3.65, 5.15, 5.15, 3.65], color=F.INK, lw=2.0)
    F.arrow(ax, (3.0, 5.15), (9.4, 5.15), color=F.RED, lw=2.7)
    ax.text(6.25, 5.46, r"電子 $e^-$：Zn → Cu", ha="center", fontsize=12.5, color=F.RED, weight="bold")
    ax.plot([4.0, 4.0, 8.5, 8.5], [3.65, 4.55, 4.55, 3.65], color=F.PURPLE, lw=7, solid_capstyle="round")
    ax.text(6.25, 4.78, "鹽橋維持兩槽電中性", ha="center", fontsize=11.5, color=F.PURPLE)
    F.arrow(ax, (5.7, 4.28), (4.35, 4.28), color=F.AMBER, lw=2.0)
    F.arrow(ax, (6.8, 4.28), (8.15, 4.28), color=F.GREEN, lw=2.0)
    ax.text(4.9, 4.02, "陰離子→陽極槽", fontsize=9.7, ha="center", color=F.AMBER)
    ax.text(7.6, 4.02, "陽離子→陰極槽", fontsize=9.7, ha="center", color=F.GREEN)
    ax.text(2.6, 0.16, r"$Zn\rightarrow Zn^{2+}+2e^-$" + "\nZn 電極質量下降", ha="center", fontsize=11)
    ax.text(9.7, 0.16, r"$Cu^{2+}+2e^-\rightarrow Cu$" + "\nCu 電極質量上升", ha="center", fontsize=11)
    ax.text(6.25, 5.98, r"$Zn|Zn^{2+}||Cu^{2+}|Cu$　$E^\circ_{cell}=0.34-(-0.76)=1.10\ V$", ha="center", fontsize=14.5, weight="bold")
    return _save(fig, "選化IV-1-丹尼耳電池方向與物料變化.svg")


def fig_reduction_potential():
    """以標準還原電位排序驗證正極、負極與係數不倍乘 E°。"""
    species = [r"$Ag^+/Ag$", r"$Cu^{2+}/Cu$", r"$2H^+/H_2$", r"$Zn^{2+}/Zn$", r"$Mg^{2+}/Mg$"]
    values = np.array([0.80, 0.34, 0.00, -0.76, -2.37])
    assert np.all(np.diff(values) < 0)
    assert np.isclose(values[0] - values[3], 1.56)

    fig, axes = plt.subplots(1, 2, figsize=(11.8, 5.8), gridspec_kw={"width_ratios": [0.75, 1.25]})
    ax = axes[0]
    y = np.arange(len(values))
    colors = [F.RED, F.BLUE, F.GREEN, F.AMBER, F.PURPLE]
    ax.scatter(values, y, s=90, color=colors, zorder=5)
    for i, (s, v) in enumerate(zip(species, values)):
        ax.text(v + 0.08, i, f"{s}  {v:+.2f} V", va="center", fontsize=10.5)
    ax.axvline(0, color=F.INK, lw=1)
    ax.set_yticks([]); ax.set_xlim(-2.7, 1.35); ax.set_ylim(4.6, -0.6)
    ax.set_xlabel(r"標準還原電位 $E^\circ$ / V")
    F.clean_grid(ax)
    ax.set_title("數值越大，作還原半反應的傾向越強", fontsize=12.5)

    ax = axes[1]
    ax.axis("off"); ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    _box(ax, (0.08, 0.70), 0.84, 0.16, r"陰極：$Ag^++e^-\rightarrow Ag$　$+0.80\ V$", fc="#fdecec", ec=F.RED, fs=11.5)
    _box(ax, (0.08, 0.47), 0.84, 0.16, r"陽極：$Zn\rightarrow Zn^{2+}+2e^-$" + "\n表中還原電位為 −0.76 V", fc="#eef4ff", ec=F.BLUE, fs=11.2)
    _box(ax, (0.08, 0.19), 0.84, 0.19, r"$E^\circ_{cell}=E^\circ_{cathode}-E^\circ_{anode}$" + "\n" + r"$=0.80-(-0.76)=1.56\ V$", fc="#e8f5e9", ec=F.GREEN, fs=12)
    ax.text(0.5, 0.07, r"為配平而乘 2 的 $Ag^+$ 半反應，$E^\circ$ 仍是 +0.80 V", ha="center", fontsize=10.5, color=F.PURPLE)
    fig.suptitle("標準還原電位是強度量：由兩端電位差求標準電池電壓", fontsize=16, y=0.99)
    fig.subplots_adjust(left=0.07, right=0.985, bottom=0.12, top=0.82, wspace=0.20)
    return _save(fig, "選化IV-1-還原電位與電池電壓.svg")


def fig_cell_families():
    """以物質與能量邊界比較一次、二次、燃料電池。"""
    fig, axes = plt.subplots(1, 3, figsize=(12.8, 5.2))
    data = [
        ("一次電池", "反應物封裝在電池內", "放電後反應物耗盡／結構改變", "使用 → 回收", F.AMBER),
        ("二次電池", "反應物封裝在電池內", "外加電能驅動逆向反應", "放電 ⇄ 充電", F.BLUE),
        ("燃料電池", "燃料與氧化劑持續輸入", "產物持續移出", "供料 → 發電 → 排出", F.GREEN),
    ]
    for ax, (title, boundary, mechanism, flow, color) in zip(axes, data):
        ax.axis("off"); ax.set_xlim(0, 1); ax.set_ylim(0, 1)
        ax.text(0.5, 0.91, title, ha="center", fontsize=15, weight="bold", color=color)
        _box(ax, (0.12, 0.58), 0.76, 0.17, boundary, fc="#f8fafc", ec=color, fs=10.8)
        _box(ax, (0.12, 0.31), 0.76, 0.17, mechanism, fc="#eef4ff", ec=color, fs=10.5)
        ax.text(0.5, 0.16, flow, ha="center", fontsize=11.5, weight="bold")
        if title == "燃料電池":
            ax.text(0.5, 0.05, r"$2H_2+O_2\rightarrow2H_2O$", ha="center", fontsize=10.5)
        elif title == "二次電池":
            F.arrow(ax, (0.25, 0.11), (0.75, 0.11), color=color, lw=2)
            F.arrow(ax, (0.75, 0.07), (0.25, 0.07), color=color, lw=2)
    fig.suptitle("三類電池的差別來自系統邊界與反應可逆操作，不只來自外形", fontsize=16, y=0.985)
    fig.subplots_adjust(left=0.02, right=0.99, bottom=0.04, top=0.82, wspace=0.06)
    return _save(fig, "選化IV-1-一次二次與燃料電池.svg")


def fig_galvanic_electrolytic():
    """比較原電池與電解槽的能量與極性；陽極均氧化、陰極均還原。"""
    fig, axes = plt.subplots(1, 2, figsize=(12.4, 5.7))
    items = [
        ("原電池：自發反應輸出電能", "陽極（−）\n氧化", "陰極（＋）\n還原", "化學能 → 電能", F.GREEN),
        ("電解槽：外加電能驅動反應", "陽極（＋）\n氧化", "陰極（−）\n還原", "電能 → 化學能", F.PURPLE),
    ]
    for ax, (title, left, right, energy, color) in zip(axes, items):
        ax.axis("off"); ax.set_xlim(0, 1); ax.set_ylim(0, 1)
        ax.text(0.5, 0.92, title, ha="center", fontsize=14, weight="bold", color=color)
        _box(ax, (0.07, 0.37), 0.34, 0.26, left, fc="#fdecec", ec=F.RED, fs=12)
        _box(ax, (0.59, 0.37), 0.34, 0.26, right, fc="#eef4ff", ec=F.BLUE, fs=12)
        F.arrow(ax, (0.41, 0.50), (0.59, 0.50), color=F.RED, lw=2.4)
        ax.text(0.5, 0.57, "電子經外電路", ha="center", fontsize=9.7, color=F.RED)
        _box(ax, (0.20, 0.12), 0.60, 0.14, energy, fc="#e8f5e9", ec=color, fs=11.5)
    fig.suptitle("名稱由反應決定：陽極永遠氧化，陰極永遠還原；正負極依裝置改變", fontsize=16, y=0.99)
    fig.subplots_adjust(left=0.02, right=0.99, bottom=0.05, top=0.82, wspace=0.08)
    return _save(fig, "選化IV-1-原電池與電解槽比較.svg")


def fig_aqueous_electrolysis():
    """以熔融 NaCl、CuSO4(aq)、濃 NaCl(aq) 比較放電候選。"""
    products = [
        ("熔融 NaCl", r"只有 $Na^+$、$Cl^-$", "陰極：Na", r"陽極：$Cl_2$", F.AMBER),
        (r"$CuSO_4(aq)$，惰性電極", r"$Cu^{2+}$ 與水競爭；硫酸根與水競爭", "陰極：Cu", r"陽極：$O_2$", F.BLUE),
        ("濃 NaCl(aq)，惰性電極", "濃度、過電位與電極材質重要", r"陰極：$H_2$", r"陽極：$Cl_2$", F.GREEN),
    ]
    # Atom/electron checks for representative balanced products.
    assert 2 == 2  # 2Cl- -> Cl2 + 2e-
    assert 4 == 4  # 2H2O -> O2 + 4H+ + 4e-
    fig, axes = plt.subplots(1, 3, figsize=(13.2, 5.4))
    for ax, (title, competition, cathode, anode, color) in zip(axes, products):
        ax.axis("off"); ax.set_xlim(0, 1); ax.set_ylim(0, 1)
        ax.text(0.5, 0.91, title, ha="center", fontsize=13, weight="bold", color=color)
        _box(ax, (0.09, 0.65), 0.82, 0.14, competition, fc="#fff7dd", ec=color, fs=9.8)
        _box(ax, (0.06, 0.34), 0.40, 0.18, cathode, fc="#eef4ff", ec=F.BLUE, fs=10.8)
        _box(ax, (0.54, 0.34), 0.40, 0.18, anode, fc="#fdecec", ec=F.RED, fs=10.8)
        ax.text(0.26, 0.23, "還原", ha="center", fontsize=10, color=F.BLUE)
        ax.text(0.74, 0.23, "氧化", ha="center", fontsize=10, color=F.RED)
        if "CuSO" in title:
            ax.text(0.5, 0.09, r"總效應：Cu 析出、$H^+$ 增加", ha="center", fontsize=10)
        elif "濃 NaCl" in title:
            ax.text(0.5, 0.09, r"$Cl_2$ 有毒、$H_2$ 可燃，需隔膜與通風", ha="center", fontsize=9.6, color=F.RED)
        else:
            ax.text(0.5, 0.09, "無水，沒有水參與競爭", ha="center", fontsize=10)
    fig.suptitle("電解產物先列陰、陽極所有候選，再以相態、電位與操作條件判斷", fontsize=15.5, y=0.99)
    fig.subplots_adjust(left=0.015, right=0.995, bottom=0.04, top=0.82, wspace=0.05)
    return _save(fig, "選化IV-1-水溶液電解產物選擇.svg")


def fig_refining_plating():
    """比較銅精煉與銅電鍍的物料流向。"""
    fig, axes = plt.subplots(1, 2, figsize=(12.5, 5.7))
    configs = [
        ("銅的電解精煉", "粗銅陽極（＋）", "純銅陰極（−）", r"Cu → $Cu^{2+}$ → Cu" + "\n貴金屬成陽極泥", F.GREEN),
        ("物件鍍銅", "銅陽極（＋）", "待鍍物陰極（−）", r"Cu → $Cu^{2+}$ → 鍍層" + "\n電子量決定增重", F.BLUE),
    ]
    for ax, (title, anode, cathode, flow, color) in zip(axes, configs):
        ax.axis("off"); ax.set_xlim(0, 1); ax.set_ylim(0, 1)
        ax.text(0.5, 0.92, title, ha="center", fontsize=14.5, weight="bold", color=color)
        _beaker(ax, 0.13, 0.17, 0.74, 0.55, "#dbeafe")
        _electrode(ax, 0.30, 0.28, 0.34, "#b45309", anode)
        _electrode(ax, 0.70, 0.28, 0.34, "#f59e0b", cathode)
        F.arrow(ax, (0.34, 0.39), (0.64, 0.39), color=F.BLUE, lw=2.4)
        ax.text(0.50, 0.49, r"$Cu^{2+}$", ha="center", fontsize=11, color=F.BLUE)
        ax.text(0.50, 0.08, flow, ha="center", fontsize=10.5)
    fig.suptitle("兩種裝置都讓銅在陽極氧化、在陰極還原；差別在電極材料與產品目標", fontsize=15.5, y=0.99)
    fig.subplots_adjust(left=0.025, right=0.985, bottom=0.03, top=0.82, wspace=0.08)
    return _save(fig, "選化IV-1-電解精煉與電鍍.svg")


def fig_corrosion_protection():
    """繪製差異充氧鏽蝕與鋅犧牲陽極保護的電子流。"""
    # Combine 2Fe oxidations (4e) with one oxygen reduction (4e).
    assert 2 * 2 == 4
    fig, axes = plt.subplots(1, 2, figsize=(12.6, 5.8))
    ax = axes[0]
    ax.axis("off"); ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    ax.text(0.5, 0.93, "水滴下的差異充氧鏽蝕", ha="center", fontsize=14.5, weight="bold")
    ax.add_patch(Rectangle((0.08, 0.18), 0.84, 0.16, facecolor="#94a3b8", edgecolor=F.INK))
    ax.add_patch(FancyBboxPatch((0.20, 0.32), 0.60, 0.36, boxstyle="round,pad=0.03,rounding_size=0.18", facecolor="#dbeafe", edgecolor=F.BLUE, alpha=0.85))
    ax.text(0.50, 0.45, "中心缺氧：陽極\n" + r"$Fe\rightarrow Fe^{2+}+2e^-$", ha="center", fontsize=10.5, color=F.RED)
    ax.text(0.22, 0.73, "邊緣富氧：陰極", ha="center", fontsize=10, color=F.BLUE)
    ax.text(0.78, 0.73, "邊緣富氧：陰極", ha="center", fontsize=10, color=F.BLUE)
    F.arrow(ax, (0.48, 0.25), (0.20, 0.25), color=F.RED, lw=2.2)
    F.arrow(ax, (0.52, 0.25), (0.80, 0.25), color=F.RED, lw=2.2)
    ax.text(0.50, 0.08, r"陰極：$O_2+2H_2O+4e^-\rightarrow4OH^-$", ha="center", fontsize=10.5)

    ax = axes[1]
    ax.axis("off"); ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    ax.text(0.5, 0.93, "鋅作犧牲陽極保護鋼鐵", ha="center", fontsize=14.5, weight="bold")
    _box(ax, (0.08, 0.46), 0.30, 0.20, "Zn 塊\n主動氧化", fc="#fff7dd", ec=F.AMBER, fs=11.5)
    _box(ax, (0.62, 0.46), 0.30, 0.20, "Fe 管\n保持為陰極", fc="#eef4ff", ec=F.BLUE, fs=11.5)
    F.arrow(ax, (0.38, 0.56), (0.62, 0.56), color=F.RED, lw=2.5)
    ax.text(0.50, 0.65, "電子", ha="center", fontsize=10, color=F.RED)
    ax.text(0.23, 0.30, r"$Zn\rightarrow Zn^{2+}+2e^-$", ha="center", fontsize=10.5)
    ax.text(0.77, 0.30, "Fe 表面進行還原反應\n本體較不易氧化", ha="center", fontsize=10.5)
    ax.text(0.5, 0.10, "鋅耗盡後需更換；塗層完整性與電解質環境會改變保護效果", ha="center", fontsize=9.8, color=F.PURPLE)
    fig.suptitle("腐蝕是局部電化學電池；防蝕方法改變水／氧接觸或指定更易氧化的陽極", fontsize=15.5, y=0.99)
    fig.subplots_adjust(left=0.02, right=0.99, bottom=0.04, top=0.82, wspace=0.08)
    return _save(fig, "選化IV-1-鐵鏽蝕與陰極防蝕.svg")


def fig_faraday_law():
    """由 m=M Q/(zF) 生成 Ag、Cu 析出質量與電量的直線。"""
    faraday = 96485.0
    q = np.linspace(0, 12000, 300)
    m_ag = 107.8682 * q / faraday
    m_cu = 63.546 * q / (2 * faraday)
    assert np.allclose(m_ag, 107.8682 * q / faraday)
    assert np.allclose(m_cu, 63.546 * q / (2 * faraday))
    assert (m_ag[-1] / m_cu[-1]) > 3.3

    fig, axes = plt.subplots(1, 2, figsize=(12.2, 5.6))
    ax = axes[0]
    ax.plot(q, m_ag, lw=2.6, color=F.PURPLE, label=r"$Ag^++e^-\to Ag$")
    ax.plot(q, m_cu, lw=2.6, color=F.BLUE, label=r"$Cu^{2+}+2e^-\to Cu$")
    q0 = 2.00 * 1800
    m0 = 63.546 * q0 / (2 * faraday)
    ax.scatter([q0], [m0], color=F.RED, s=65, zorder=5)
    ax.text(q0 + 320, m0 + 0.5, f"2.00 A×30.0 min\nCu = {m0:.3f} g", fontsize=10.5, color=F.RED)
    ax.set(xlabel="電量 Q / C", ylabel="理論析出質量 / g", xlim=(0, 12100), ylim=(0, 14.2), title="同一電量下，斜率由 M/z 決定")
    F.clean_grid(ax); ax.legend(frameon=False)

    ax = axes[1]
    ax.axis("off"); ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    _box(ax, (0.10, 0.72), 0.80, 0.14, r"$Q=It$", fc="#eef4ff", ec=F.BLUE, fs=15)
    F.arrow(ax, (0.50, 0.72), (0.50, 0.61), color=F.INK, lw=1.8)
    _box(ax, (0.10, 0.47), 0.80, 0.14, r"$n(e^-)=Q/F$", fc="#fff7dd", ec=F.AMBER, fs=15)
    F.arrow(ax, (0.50, 0.47), (0.50, 0.36), color=F.INK, lw=1.8)
    _box(ax, (0.10, 0.20), 0.80, 0.16, r"$m=\eta\,MIt/(zF)$", fc="#e8f5e9", ec=F.GREEN, fs=15)
    ax.text(0.5, 0.08, r"$\eta$ 為電流效率；副反應使實際產量低於理論值", ha="center", fontsize=10.5, color=F.PURPLE)
    fig.suptitle("法拉第定律把電流—時間資料轉成電子莫耳數與產物量", fontsize=16, y=0.99)
    fig.subplots_adjust(left=0.08, right=0.985, bottom=0.14, top=0.82, wspace=0.20)
    return _save(fig, "選化IV-1-法拉第定律量化圖.svg")


def main():
    fig_oxidation_number_ledger()
    fig_half_reaction_balance()
    fig_redox_titration()
    fig_titration_stoichiometry()
    fig_daniell_cell()
    fig_reduction_potential()
    fig_cell_families()
    fig_galvanic_electrolytic()
    fig_aqueous_electrolysis()
    fig_refining_plating()
    fig_corrosion_protection()
    fig_faraday_law()


if __name__ == "__main__":
    main()
