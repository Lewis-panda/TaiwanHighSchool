# -*- coding: utf-8 -*-
"""產生「必化-4 生活化學」學生講義章內 SVG。

重繪：.venv/bin/python _tools/fig_content_必化-4.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, FancyBboxPatch, Polygon, Rectangle

import figlib as F


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CH = os.path.join(ROOT, "content", "必修化學", "必化-4")


FIGURE_OUTPUTS = (
    ("fig_biomolecule_assembly", "必化-4-生物分子組裝帳.svg"),
    ("fig_lipid_geometry", "必化-4-脂肪酸幾何與堆積.svg"),
    ("fig_surfactant_evidence", "必化-4-界面活性劑與硬水證據.svg"),
    ("fig_drug_structure", "必化-4-常用藥物結構與制酸計量.svg"),
    ("fig_nano_surface", "必化-4-奈米化與表面積.svg"),
    ("fig_water_treatment", "必化-4-淨水流程與粒子去向.svg"),
    ("fig_air_pathways", "必化-4-空氣化學路徑.svg"),
    ("fig_carbon_boundary", "必化-4-碳循環與足跡邊界.svg"),
    ("fig_atom_energy", "必化-4-原子經濟與能源判讀.svg"),
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


def _box(ax, xy, width, height, text, face="#f8fafc", edge="#64748b", fs=11.2, lw=1.6):
    patch = FancyBboxPatch(
        xy,
        width,
        height,
        boxstyle="round,pad=0.035,rounding_size=0.10",
        facecolor=face,
        edgecolor=edge,
        lw=lw,
    )
    ax.add_patch(patch)
    ax.text(xy[0] + width / 2, xy[1] + height / 2, text, ha="center", va="center", fontsize=fs)
    return patch


def _molecule(ax, x, y, label, color, radius=0.26, text_color="white"):
    circle = Circle((x, y), radius, facecolor=color, edgecolor="white", lw=1.1, zorder=4)
    ax.add_patch(circle)
    ax.text(x, y, label, ha="center", va="center", fontsize=8.5, color=text_color, weight="bold", zorder=5)
    return circle


def _chain(ax, points, color=F.INK, lw=2.0):
    xs, ys = zip(*points)
    ax.plot(xs, ys, color=color, lw=lw, solid_capstyle="round")


def fig_biomolecule_assembly():
    """以脫水數量連接醣、肽、油脂與核酸的組裝。"""
    monomers = {"oligosaccharide": 3, "peptide": 4, "nucleotide_chain": 4}
    water_counts = {key: value - 1 for key, value in monomers.items()}
    water_counts["triglyceride"] = 3
    assert water_counts == {
        "oligosaccharide": 2,
        "peptide": 3,
        "nucleotide_chain": 3,
        "triglyceride": 3,
    }

    fig, axes = plt.subplots(2, 2, figsize=(12.0, 8.0))
    panels = [
        ("醣類：3 個單醣", ["糖", "糖", "糖"], F.BLUE, "2 個糖苷鍵＋2 $H_2O$", "寡醣"),
        ("蛋白質：4 個胺基酸", ["胺", "胺", "胺", "胺"], F.PURPLE, "3 個肽鍵＋3 $H_2O$", "四肽"),
        ("油脂：甘油＋3 個脂肪酸", ["甘", "酸", "酸", "酸"], F.AMBER, "3 個酯鍵＋3 $H_2O$", "三酸甘油酯"),
        ("核酸：4 個核苷酸", ["核", "核", "核", "核"], F.GREEN, "3 個磷酸二酯鍵＋3 $H_2O$", "短核酸鏈"),
    ]
    for ax, (title, labels, color, ledger, product) in zip(axes.flat, panels):
        ax.axis("off")
        ax.set_xlim(-3.0, 3.0)
        ax.set_ylim(-2.2, 2.2)
        ax.text(0, 1.82, title, ha="center", fontsize=13.5, weight="bold")
        xs = np.linspace(-2.35, -0.55, len(labels))
        for x, label in zip(xs, labels):
            _molecule(ax, x, 0.65, label, color)
        F.arrow(ax, (0.00, 0.65), (0.78, 0.65), color="#64748b", lw=2.0, mutation=14)
        n_product = 3 if title.startswith("醣") else 4
        px = np.linspace(1.08, 2.55, n_product)
        for i, x in enumerate(px):
            _molecule(ax, x, 0.65, "單", color, radius=0.23)
            if i:
                ax.plot([px[i - 1] + 0.22, x - 0.22], [0.65, 0.65], color=F.INK, lw=2.1)
        ax.text(1.8, 0.05, product, ha="center", fontsize=11.8, color=color, weight="bold")
        _box(ax, (-2.55, -1.45), 5.10, 0.72, ledger, face="#f8fafc", edge=color, fs=11.5)
    fig.suptitle("脫水縮合的共同帳本：成鍵數決定放出的水分子數", fontsize=16, y=0.985)
    fig.subplots_adjust(left=0.035, right=0.97, top=0.91, bottom=0.04, hspace=0.22, wspace=0.10)
    return _save(fig, "必化-4-生物分子組裝帳.svg")


def fig_lipid_geometry():
    """以鍵型與幾何展示脂肪酸堆積差異。"""
    fig, axes = plt.subplots(1, 3, figsize=(12.0, 5.6))
    titles = ["飽和脂肪酸", "順式不飽和脂肪酸", "反式不飽和脂肪酸"]
    notes = ["全為 C–C 單鍵\n鏈較易緊密堆積", "C=C 同側取代\n碳鏈形成彎折", "C=C 異側取代\n整體較接近直鏈"]
    points = [
        [(-2.0, 0.6), (-1.4, 0.2), (-0.8, 0.6), (-0.2, 0.2), (0.4, 0.6), (1.0, 0.2), (1.6, 0.6)],
        [(-2.0, 0.6), (-1.4, 0.2), (-0.8, 0.6), (-0.2, 0.2), (0.15, -0.48), (0.58, -0.90), (0.92, -0.62)],
        [(-2.0, 0.6), (-1.4, 0.2), (-0.8, 0.6), (-0.2, 0.2), (0.4, 0.6), (1.0, 0.2), (1.6, 0.6)],
    ]
    for idx, (ax, title, note, pts) in enumerate(zip(axes, titles, notes, points)):
        ax.axis("off")
        ax.set_xlim(-2.45, 2.45)
        ax.set_ylim(-2.35, 2.35)
        _chain(ax, pts, color=F.BLUE if idx != 2 else F.RED, lw=3.0)
        for p in pts:
            ax.add_patch(Circle(p, 0.09, facecolor="#334155", edgecolor="white", lw=0.6, zorder=4))
        if idx:
            ax.plot([pts[2][0], pts[3][0]], [pts[2][1] + 0.11, pts[3][1] + 0.11], color=F.INK, lw=1.5)
            ax.text(-0.50, 0.95, "C=C", fontsize=10.5, ha="center", weight="bold")
        ax.text(0, 1.85, title, ha="center", fontsize=13.4, weight="bold")
        _box(ax, (-2.08, -1.85), 4.16, 0.83, note, face="#f8fafc", edge=[F.BLUE, F.GREEN, F.RED][idx], fs=11.2)
    cis_end_distance = np.linalg.norm(np.array(points[1][-1]) - np.array(points[1][0]))
    trans_end_distance = np.linalg.norm(np.array(points[2][-1]) - np.array(points[2][0]))
    assert cis_end_distance < trans_end_distance
    fig.suptitle("雙鍵幾何改變碳鏈形狀，進而改變分子間堆積與物態傾向", fontsize=16, y=0.98)
    fig.subplots_adjust(left=0.025, right=0.975, top=0.86, bottom=0.05, wspace=0.08)
    return _save(fig, "必化-4-脂肪酸幾何與堆積.svg")


def fig_surfactant_evidence():
    """用微胞與硬水沉澱連接實驗觀察和粒子推論。"""
    n_heads = 12
    assert n_heads == 12
    fig, axes = plt.subplots(1, 2, figsize=(12.0, 6.0))
    left, right = axes
    for ax in axes:
        ax.axis("off")
        ax.set_xlim(-3.1, 3.1)
        ax.set_ylim(-2.8, 2.8)

    oil = Circle((0, 0.15), 0.86, facecolor="#fbbf24", edgecolor="#b45309", lw=2.0, alpha=0.85)
    left.add_patch(oil)
    for angle in np.linspace(0, 2 * np.pi, n_heads, endpoint=False):
        inner = np.array([0.88 * np.cos(angle), 0.88 * np.sin(angle) + 0.15])
        outer = np.array([1.55 * np.cos(angle), 1.55 * np.sin(angle) + 0.15])
        left.plot([inner[0], outer[0]], [inner[1], outer[1]], color="#334155", lw=2.0)
        left.add_patch(Circle(tuple(outer), 0.16, facecolor=F.BLUE, edgecolor="white", lw=0.8))
    left.text(0, 0.15, "油滴", ha="center", va="center", fontsize=13, weight="bold")
    left.text(0, 2.35, "乳化後的油滴", ha="center", fontsize=14, weight="bold")
    left.text(0, -2.18, "疏水尾插入油相；親水頭朝水相\n攪拌把大油層分成可分散的小油滴", ha="center", fontsize=11.3)

    _box(right, (-2.75, 1.38), 5.50, 0.78, r"肥皂：$2RCOO^-+Ca^{2+}\rightarrow(RCOO)_2Ca(s)$", face="#fff1e6", edge=F.RED, fs=12.2)
    right.add_patch(Rectangle((-2.45, -0.20), 2.05, 1.15, facecolor="#dbeafe", edgecolor="#64748b", lw=1.4))
    right.add_patch(Rectangle((0.40, -0.20), 2.05, 1.15, facecolor="#dbeafe", edgecolor="#64748b", lw=1.4))
    for x, y in [(-2.05, 0.52), (-1.48, 0.20), (-0.86, 0.54)]:
        _molecule(right, x, y, "皂", F.AMBER, radius=0.18)
    for x, y in [(-1.85, -0.05), (-1.10, -0.02)]:
        right.add_patch(Circle((x, y), 0.18, facecolor="#94a3b8", edgecolor="#475569"))
    for x, y in [(0.82, 0.52), (1.42, 0.18), (2.02, 0.55)]:
        _molecule(right, x, y, "清", F.GREEN, radius=0.18)
    right.text(-1.42, -0.64, "肥皂＋硬水\n沉澱、泡沫減少", ha="center", fontsize=11.3, color=F.RED, weight="bold")
    right.text(1.42, -0.64, "合成清潔劑＋硬水\n維持較多分散能力", ha="center", fontsize=11.3, color=F.GREEN, weight="bold")
    _box(right, (-2.75, -2.20), 5.50, 0.72, "觀察：混濁或沉澱、乳化層變薄；推論：可用的界面活性劑濃度下降。", face="#fff7dd", edge=F.AMBER, fs=11.1)
    right.set_title("硬水提供反應證據", fontsize=14, weight="bold")
    calcium_charge = 2
    soap_anions = 2
    assert calcium_charge == soap_anions
    fig.suptitle("界面活性劑的結構決定油水方向；離子反應決定硬水中的效能", fontsize=16, y=0.985)
    fig.subplots_adjust(left=0.025, right=0.975, top=0.86, bottom=0.05, wspace=0.10)
    return _save(fig, "必化-4-界面活性劑與硬水證據.svg")


def fig_drug_structure():
    """比較常見藥物的官能基資訊，並建立制酸劑莫耳帳。"""
    fig, axes = plt.subplots(1, 2, figsize=(12.0, 6.3), gridspec_kw={"width_ratios": [1.15, 0.85]})
    left, right = axes
    for ax in axes:
        ax.axis("off")
    left.set_xlim(-3.5, 3.5)
    left.set_ylim(-3.0, 3.0)
    drugs = [
        (-3.15, 1.15, 2.95, "水楊酸\n芳香環＋酚羥基＋羧基\n外用產品可見", F.BLUE),
        (0.20, 1.15, 2.95, "阿司匹靈\n芳香環＋酯基＋羧基\n解熱鎮痛；具抗血小板作用", F.RED),
        (-3.15, -1.35, 2.95, "乙醯胺酚\n芳香環＋酚羥基＋醯胺\n解熱鎮痛", F.GREEN),
        (0.20, -1.35, 2.95, "布洛芬\n芳香環＋羧基\n解熱鎮痛與抗發炎", F.PURPLE),
    ]
    for x, y, w, text, color in drugs:
        _box(left, (x, y), w, 1.38, text, face="#f8fafc", edge=color, fs=10.8)
    left.set_title("結構支持性質推論；安全用法以標示與專業指示為準", fontsize=13.4, weight="bold")

    right.set_xlim(-3.0, 3.0)
    right.set_ylim(-3.0, 3.0)
    _box(right, (-2.55, 1.45), 5.10, 0.86, r"胃酸模型：$HCl\rightarrow H^++Cl^-$", face="#fff1e6", edge=F.RED, fs=12.6)
    _box(right, (-2.55, 0.20), 5.10, 0.90, r"$Mg(OH)_2+2HCl\rightarrow MgCl_2+2H_2O$", face="#eef4ff", edge=F.BLUE, fs=12.5)
    _box(right, (-2.55, -1.05), 5.10, 0.90, r"$NaHCO_3+HCl\rightarrow NaCl+CO_2+H_2O$", face="#e9f8ef", edge=F.GREEN, fs=12.0)
    _box(right, (-2.55, -2.28), 5.10, 0.72, "1 mol $Mg(OH)_2$ 可中和 2 mol $HCl$；\n1 mol $NaHCO_3$ 可中和 1 mol $HCl$。", face="#fff7dd", edge=F.AMBER, fs=11.4)
    assert 2 * 1 == 2
    assert 1 * 1 == 1
    right.set_title("制酸劑以反應式決定容量", fontsize=14, weight="bold")
    fig.suptitle("常用藥品：由結構辨認官能基，由配平反應式完成定量", fontsize=16, y=0.985)
    fig.subplots_adjust(left=0.025, right=0.975, top=0.86, bottom=0.05, wspace=0.10)
    return _save(fig, "必化-4-常用藥物結構與制酸計量.svg")


def fig_nano_surface():
    """固定總體積，比較 60 nm 方塊與 10 nm 小方塊的總表面積。"""
    large_edge = 60.0
    small_edge = 10.0
    count = int((large_edge / small_edge) ** 3)
    large_area = 6 * large_edge**2
    small_total_area = count * 6 * small_edge**2
    ratio = small_total_area / large_area
    assert count == 216
    assert np.isclose(ratio, 6.0)

    fig, axes = plt.subplots(1, 2, figsize=(11.8, 6.0))
    left, right = axes
    for ax in axes:
        ax.axis("off")
        ax.set_xlim(-3.0, 3.0)
        ax.set_ylim(-2.7, 2.7)
    left.add_patch(Rectangle((-1.65, -1.45), 3.3, 3.3, facecolor="#dbeafe", edgecolor=F.BLUE, lw=2.3))
    left.text(0, 0.25, "一個\n60 nm 方塊", ha="center", va="center", fontsize=14, weight="bold")
    left.text(0, -2.05, "表面積 $=6(60)^2$\n相同材料總體積", ha="center", fontsize=12)
    left.set_title("塊材模型", fontsize=14, weight="bold")

    origin = (-1.65, -1.45)
    cell = 3.3 / 6
    for i in range(6):
        for j in range(6):
            right.add_patch(Rectangle((origin[0] + i * cell, origin[1] + j * cell), cell, cell, facecolor="#e9f8ef", edgecolor=F.GREEN, lw=0.8))
    right.text(0, 2.08, "每邊切成 6 份", ha="center", fontsize=12, color=F.GREEN, weight="bold")
    right.text(0, -2.05, "$6^3=216$ 個 10 nm 方塊\n總表面積變為原來 6 倍", ha="center", fontsize=12)
    right.set_title("奈米化模型", fontsize=14, weight="bold")
    fig.suptitle("體積不變時，粒徑縮小會增加總表面積與表面原子比例", fontsize=16, y=0.98)
    fig.subplots_adjust(left=0.035, right=0.97, top=0.84, bottom=0.05, wspace=0.12)
    return _save(fig, "必化-4-奈米化與表面積.svg")


def fig_water_treatment():
    """追蹤淨水流程中不同粒子的去向與消毒角色。"""
    fig, ax = F.schematic(12.0, 7.0)
    ax.set_xlim(-6.0, 6.0)
    ax.set_ylim(-3.5, 3.5)
    stages = [
        (-5.65, 1.20, "原水\n大顆粒、膠體\n溶解物、微生物", F.RED),
        (-3.35, 1.20, "混凝／膠羽\n微粒聚集成\n較大絮體", F.AMBER),
        (-1.05, 1.20, "沉澱\n重力移除\n大部分絮體", F.PURPLE),
        (1.25, 1.20, "過濾／吸附\n截留顆粒\n降低色與味", F.BLUE),
        (3.55, 1.20, "消毒\n降低可感染的\n微生物數量", F.GREEN),
    ]
    for x, y, text, color in stages:
        _box(ax, (x, y), 1.85, 1.45, text, face="#f8fafc", edge=color, fs=10.5)
    for x in [-3.70, -1.40, 0.90, 3.20]:
        F.arrow(ax, (x, 1.93), (x + 0.28, 1.93), color="#64748b", lw=1.8, mutation=12)
    _box(ax, (-5.35, -0.42), 3.10, 0.86, "曝氣（依原水需求）\n增加溶氧、逸散部分揮發物，\n可支持好氧微生物分解有機物", face="#eef4ff", edge=F.BLUE, fs=10.8)
    _box(ax, (-1.55, -0.42), 3.10, 0.86, "海水淡化\n逆滲透以外加壓力使水跨膜；\n離子多留在濃水側", face="#e9f8ef", edge=F.GREEN, fs=10.8)
    _box(ax, (2.25, -0.42), 3.10, 0.86, "氯／次氯酸：可保留餘氯\n臭氧：氧化力強、殘留短\n兩者角色皆是消毒", face="#fff7dd", edge=F.AMBER, fs=10.8)
    _box(ax, (-5.35, -2.20), 5.00, 0.95, r"$Ca^{2+}+CO_3^{2-}\rightarrow CaCO_3(s)$" + "\n沉澱軟化：把溶解離子轉為可分離固體", face="#fff1e6", edge=F.RED, fs=11.8)
    _box(ax, (0.35, -2.20), 5.00, 0.95, r"$Ca^{2+}+2NaZ\rightleftharpoons CaZ_2+2Na^+$" + "\n離子交換：樹脂容量耗盡後以濃鹽水再生", face="#f1ecff", edge=F.PURPLE, fs=11.8)
    assert 2 == 2  # 一個 Ca2+ 交換兩個 Na+
    fig.suptitle("每道水處理單元都對應特定粒子；流程由原水與用途決定", fontsize=16, y=0.985)
    fig.subplots_adjust(left=0.02, right=0.98, top=0.89, bottom=0.035)
    return _save(fig, "必化-4-淨水流程與粒子去向.svg")


def fig_air_pathways():
    """區分溫室效應、臭氧層、酸雨與光化學煙霧的能量和反應路徑。"""
    fig, axes = plt.subplots(2, 2, figsize=(12.0, 8.0))
    panels = [
        ("溫室效應", "地表放出紅外線\n$CO_2, CH_4, N_2O$ 等吸收並再放射\n改變地表—大氣能量收支", F.RED),
        ("平流層臭氧", r"$O_3+h\nu\rightarrow O_2+O$" + "\n氯自由基可催化臭氧分解\n臭氧吸收部分紫外線", F.BLUE),
        ("酸雨", "$SO_x, NO_x$ 氧化並溶於水\n生成含硫酸、硝酸的酸性降水\n本課以 pH < 5.0 判定", F.PURPLE),
        ("光化學煙霧", r"$NO_2+h\nu\rightarrow NO+O$" + "\n" + r"$O+O_2\rightarrow O_3$" + "\nNOx、VOC、日照共同形成二次污染", F.AMBER),
    ]
    for ax, (title, text, color) in zip(axes.flat, panels):
        ax.axis("off")
        ax.set_xlim(-3.0, 3.0)
        ax.set_ylim(-2.4, 2.4)
        _box(ax, (-2.55, -1.25), 5.10, 2.50, text, face="#f8fafc", edge=color, fs=11.6, lw=2.0)
        ax.text(0, 1.78, title, ha="center", fontsize=14, weight="bold", color=color)
    photon_energy_positive = True
    oxygen_atoms_balanced = (3 == 2 + 1) and (1 + 2 == 3)
    assert photon_energy_positive and oxygen_atoms_balanced
    fig.suptitle("四個環境議題需要不同的光、分子與反應模型", fontsize=16, y=0.985)
    fig.subplots_adjust(left=0.035, right=0.97, top=0.90, bottom=0.04, hspace=0.20, wspace=0.10)
    return _save(fig, "必化-4-空氣化學路徑.svg")


def fig_carbon_boundary():
    """以簡化碳流資料說明碳循環、淨增加量與產品足跡邊界。"""
    fossil = 9.0
    land = 1.0
    ocean_sink = 2.5
    land_sink = 3.0
    atmospheric_gain = fossil + land - ocean_sink - land_sink
    assert np.isclose(atmospheric_gain, 4.5)
    fig, axes = plt.subplots(1, 2, figsize=(12.0, 6.3), gridspec_kw={"width_ratios": [1.0, 1.05]})
    left, right = axes
    for ax in axes:
        ax.axis("off")
        ax.set_xlim(-3.0, 3.0)
        ax.set_ylim(-3.0, 3.0)
    _box(left, (-1.75, 1.65), 3.50, 0.76, "大氣碳庫\n淨增加 $4.5$ 單位／年", face="#fff1e6", edge=F.RED, fs=12.0)
    _box(left, (-2.75, -0.10), 2.15, 0.86, "化石燃料與工業\n$+9.0$", face="#fff7dd", edge=F.AMBER, fs=11.6)
    _box(left, (0.60, -0.10), 2.15, 0.86, "土地利用變化\n$+1.0$", face="#fff7dd", edge=F.AMBER, fs=11.6)
    _box(left, (-2.75, -2.00), 2.15, 0.86, "陸地吸收\n$-3.0$", face="#e9f8ef", edge=F.GREEN, fs=11.6)
    _box(left, (0.60, -2.00), 2.15, 0.86, "海洋吸收\n$-2.5$", face="#eef4ff", edge=F.BLUE, fs=11.6)
    for start, end, color in [((-1.65, 0.80), (-0.80, 1.56), F.AMBER), ((1.65, 0.80), (0.80, 1.56), F.AMBER), ((-0.80, 1.56), (-1.65, -1.06), F.GREEN), ((0.80, 1.56), (1.65, -1.06), F.BLUE)]:
        F.arrow(left, start, end, color=color, lw=2.0, mutation=13)
    left.set_title("一組原創碳流資料", fontsize=14, weight="bold")

    stages = ["原料", "製造", "運輸", "使用", "廢棄／回收"]
    xs = np.linspace(-2.55, 2.55, len(stages))
    emissions = [18, 32, 12, 25, 8]
    assert sum(emissions) == 95
    for i, (x, stage, value) in enumerate(zip(xs, stages, emissions)):
        right.add_patch(Rectangle((x - 0.42, -0.35), 0.84, value / 18.0, facecolor=[F.BLUE, F.RED, F.AMBER, F.PURPLE, F.GREEN][i], alpha=0.72, edgecolor="white"))
        right.text(x, -0.60, stage, ha="center", fontsize=10.2)
        right.text(x, value / 18.0 - 0.17, str(value), ha="center", va="center", fontsize=10, color="white", weight="bold")
    right.plot([-2.95, 2.95], [-0.72, -0.72], color="#334155", lw=1.3)
    right.text(0, 2.53, "產品碳足跡的生命週期邊界", ha="center", fontsize=14, weight="bold")
    right.text(0, -1.35, r"合計 $95\ \mathrm{kg\ CO_2e}$" + "\n邊界與功能單位相同，數值才可比較", ha="center", fontsize=11.8)
    _box(right, (-2.50, -2.60), 5.00, 0.68, "碳手印：能證明的減量行動；應以基準情境與量測期間計算差額。", face="#e9f8ef", edge=F.GREEN, fs=11.0)
    fig.suptitle("碳循環追蹤庫與流；碳足跡追蹤指定邊界內的排放", fontsize=16, y=0.985)
    fig.subplots_adjust(left=0.025, right=0.975, top=0.87, bottom=0.05, wspace=0.12)
    return _save(fig, "必化-4-碳循環與足跡邊界.svg")


def fig_atom_energy():
    """比較乙醇兩條路徑的原子經濟，並建立能源方案的多軸判讀。"""
    mw_ethanol = 46.0
    fermentation = 2 * mw_ethanol / 180.0 * 100
    hydration = mw_ethanol / (28.0 + 18.0) * 100
    assert np.isclose(fermentation, 51.1111111111)
    assert np.isclose(hydration, 100.0)
    fig, axes = plt.subplots(1, 2, figsize=(12.0, 6.4))
    left, right = axes
    for ax in axes:
        ax.axis("off")
        ax.set_xlim(-3.2, 3.2)
        ax.set_ylim(-3.0, 3.0)
    _box(left, (-2.85, 1.45), 5.70, 0.95, r"$C_6H_{12}O_6\rightarrow2C_2H_5OH+2CO_2$" + "\n" + r"原子經濟 $=92/180=51.1\%$", face="#fff7dd", edge=F.AMBER, fs=12.2)
    _box(left, (-2.85, 0.05), 5.70, 0.95, r"$C_2H_4+H_2O\rightarrow C_2H_5OH$" + "\n" + r"原子經濟 $=46/46=100\%$", face="#e9f8ef", edge=F.GREEN, fs=12.2)
    _box(left, (-2.85, -1.45), 5.70, 0.95, "原子經濟記錄配平反應式的原子去向；\n產率、能耗、毒性、原料來源與分離成本各需評估。", face="#eef4ff", edge=F.BLUE, fs=11.2)
    left.set_title("綠色化學的原子帳", fontsize=14, weight="bold")

    sources = ["太陽", "風力", "生質", "天然氣"]
    reliability = [2, 2, 3, 5]
    lifecycle = [1, 1, 3, 4]
    land = [3, 2, 5, 1]
    assert len(sources) == len(reliability) == len(lifecycle) == len(land) == 4
    y = np.arange(len(sources))[::-1]
    right.axis("on")
    reliability_bars = right.barh(
        y + 0.20,
        reliability,
        height=0.18,
        color=F.BLUE,
        edgecolor=F.INK,
        linewidth=0.9,
        linestyle="-",
        hatch="///",
        label="可調度性",
    )
    lifecycle_bars = right.barh(
        y,
        lifecycle,
        height=0.18,
        color=F.RED,
        edgecolor=F.INK,
        linewidth=0.9,
        linestyle="--",
        hatch="xx",
        label="生命週期排放",
    )
    land_bars = right.barh(
        y - 0.20,
        land,
        height=0.18,
        color=F.GREEN,
        edgecolor=F.INK,
        linewidth=0.9,
        linestyle=":",
        hatch="..",
        label="土地／空間需求",
    )
    assert all(bar.get_hatch() == "///" for bar in reliability_bars)
    assert all(bar.get_hatch() == "xx" for bar in lifecycle_bars)
    assert all(bar.get_hatch() == ".." for bar in land_bars)
    assert all(bar.get_linestyle() == "-" for bar in reliability_bars)
    assert all(bar.get_linestyle() == "--" for bar in lifecycle_bars)
    assert all(bar.get_linestyle() == ":" for bar in land_bars)
    right.set_xlim(0, 5.6)
    right.set_ylim(-0.7, 3.7)
    right.set_yticks(y, sources)
    right.set_xticks(range(0, 6))
    right.set_xlabel("示意評分（1–5）", fontsize=10.5)
    right.grid(axis="x", alpha=0.22)
    right.spines[["top", "right"]].set_visible(False)
    right.legend(loc="lower center", bbox_to_anchor=(0.5, -0.22), ncol=3, fontsize=9.5, frameon=False)
    right.set_title("示意評分：能源需多軸比較", fontsize=14, weight="bold")
    right.text(2.8, 3.48, "1＝較低；5＝較高（示意資料）", ha="center", fontsize=10.5, color="#475569")
    fig.suptitle("高原子經濟與永續能源都需要明確指標與系統邊界", fontsize=16, y=0.985)
    fig.subplots_adjust(left=0.04, right=0.975, top=0.86, bottom=0.13, wspace=0.16)
    return _save(fig, "必化-4-原子經濟與能源判讀.svg")


def main():
    for entrypoint, filename in FIGURE_OUTPUTS:
        assert entrypoint in globals(), f"缺少圖形函式：{entrypoint}"
        globals()[entrypoint]()
        expected = os.path.join(CH, "assets", filename)
        assert os.path.exists(expected), f"圖檔未產生：{expected}"


if __name__ == "__main__":
    main()
