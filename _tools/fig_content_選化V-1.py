# -*- coding: utf-8 -*-
"""產生「選化 V-1 有機化學」學生講義的章內 SVG。

重繪：.venv/bin/python _tools/fig_content_選化V-1.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyBboxPatch, Rectangle

import figlib as F


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CH = os.path.join(ROOT, "content", "選修化學V", "選化V-1")


FIGURE_OUTPUTS = (
    ("fig_structure_isomers", "選化V-1-結構表示與異構判斷.svg"),
    ("fig_combustion_analysis", "選化V-1-燃燒分析裝置與資料流.svg"),
    ("fig_functional_groups", "選化V-1-官能基分類圖譜.svg"),
    ("fig_naming_flow", "選化V-1-有機命名流程.svg"),
    ("fig_hydrocarbon_reactions", "選化V-1-烴類反應路線.svg"),
    ("fig_interactions_boiling", "選化V-1-分子間作用力與沸點.svg"),
    ("fig_alcohol_oxidation", "選化V-1-醇氧化與官能基檢驗.svg"),
    ("fig_carbonyl_acid_ester", "選化V-1-羰基羧酸酯反應網.svg"),
    ("fig_aspirin", "選化V-1-阿司匹靈製備與純度.svg"),
    ("fig_acid_base_extraction", "選化V-1-酸鹼萃取流程.svg"),
    ("fig_polymerization", "選化V-1-加成與縮合聚合.svg"),
    ("fig_reverse_monomer", "選化V-1-聚合物反推單體.svg"),
    ("fig_natural_polymers", "選化V-1-天然聚合物鍵結.svg"),
    ("fig_synthetic_polymers", "選化V-1-人造聚合物結構與用途.svg"),
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


def _blank(title, *, width=12.0, height=5.8):
    fig, ax = plt.subplots(figsize=(width, height))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 6)
    ax.axis("off")
    ax.set_title(title, fontsize=16, weight="bold", pad=12)
    return fig, ax


def _box(ax, x, y, w, h, text, *, face="#f8fafc", edge="#64748b", fs=11.0, lw=1.5):
    patch = FancyBboxPatch(
        (x, y),
        w,
        h,
        boxstyle="round,pad=0.035,rounding_size=0.08",
        facecolor=face,
        edgecolor=edge,
        linewidth=lw,
    )
    ax.add_patch(patch)
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs)
    return patch


def _arrow(ax, start, end, text="", *, color=F.BLUE, yoff=0.22):
    F.arrow(ax, start, end, color=color, lw=2.0, mutation=16)
    if text:
        ax.text(
            (start[0] + end[0]) / 2,
            (start[1] + end[1]) / 2 + yoff,
            text,
            ha="center",
            va="bottom",
            color=color,
            fontsize=10.0,
        )


def _section(ax, x, title, lines, *, color=F.BLUE, width=3.45):
    _box(ax, x, 0.55, width, 4.75, "", face="#ffffff", edge=color, lw=1.8)
    ax.add_patch(Rectangle((x, 4.48), width, 0.82, facecolor=color, edgecolor=color))
    ax.text(x + width / 2, 4.89, title, ha="center", va="center", color="white", fontsize=12.5, weight="bold")
    y = 3.92
    for text, shade in lines:
        _box(ax, x + 0.24, y - 0.52, width - 0.48, 0.72, text, face=shade, edge="#cbd5e1", fs=10.1, lw=1.0)
        y -= 1.02


def fig_structure_isomers():
    c, h, o = 4, 8, 1
    dbe = (2 * c + 2 - h) / 2
    assert dbe == 1
    fig, ax = _blank("結構表示先守住原子數，再用 DBE 與連接方式分類")
    _section(
        ax,
        0.25,
        "同一分子：三種表示",
        [
            (r"分子式  $C_4H_8O$", "#eff6ff"),
            (r"簡式  $CH_3CH_2CH_2CHO$", "#f8fafc"),
            ("鍵線式：端點／折點數碳\n依四價補氫", "#f0fdf4"),
        ],
        color=F.BLUE,
    )
    _section(
        ax,
        4.28,
        r"DBE $=1$ 的約束",
        [
            ("一個羰基雙鍵", "#fff7dd"),
            ("或一個碳碳雙鍵", "#fff7dd"),
            ("或一個環；仍需官能基證據", "#fff7dd"),
        ],
        color=F.AMBER,
    )
    _section(
        ax,
        8.30,
        "同分異構分類",
        [
            ("butanal ↔ 2-methylpropanal：鏈異構", "#fdf2f8"),
            ("butanal ↔ butan-2-one：官能基異構", "#fdf2f8"),
            ("順反條件：雙鍵兩碳各接兩種取代基", "#fdf2f8"),
        ],
        color=F.PURPLE,
    )
    _arrow(ax, (3.76, 2.94), (4.20, 2.94), "檢查")
    _arrow(ax, (7.78, 2.94), (8.22, 2.94), "列舉", color=F.PURPLE)
    return _save(fig, "選化V-1-結構表示與異構判斷.svg")


def fig_combustion_analysis():
    m_sample = 0.600
    m_co2 = 0.880
    m_h2o = 0.360
    n_c = m_co2 / 44.0
    n_h = 2 * m_h2o / 18.0
    m_o = m_sample - 12.0 * n_c - 1.0 * n_h
    n_o = m_o / 16.0
    assert np.allclose([n_c, n_h, n_o], [0.0200, 0.0400, 0.0200])
    fig, ax = _blank("燃燒分析：吸收瓶質量增量直接給 C、H 的物質的量")
    _box(ax, 0.25, 2.13, 1.75, 1.45, "有機樣品\n0.600 g", face="#eff6ff", edge=F.BLUE, fs=12.2)
    _arrow(ax, (2.02, 2.86), (2.88, 2.86), r"$O_2$、加熱", color=F.RED)
    _box(ax, 2.90, 2.13, 1.75, 1.45, "燃燒管\n完全燃燒", face="#fff7dd", edge=F.AMBER, fs=12.2)
    _arrow(ax, (4.67, 2.86), (5.50, 2.86), "氣流")
    _box(ax, 5.52, 3.27, 2.05, 1.30, "$H_2O$ 吸收瓶\n增重 0.360 g", face="#e0f2fe", edge=F.BLUE, fs=11.5)
    _box(ax, 5.52, 1.13, 2.05, 1.30, "$CO_2$ 吸收瓶\n增重 0.880 g", face="#f0fdf4", edge=F.GREEN, fs=11.5)
    _arrow(ax, (7.60, 3.92), (8.42, 3.92), r"$2n(H_2O)$", color=F.BLUE)
    _arrow(ax, (7.60, 1.78), (8.42, 1.78), r"$n(CO_2)$", color=F.GREEN)
    _box(ax, 8.45, 3.27, 3.20, 1.30, r"$n(H)=0.0400\ mol$", face="#e0f2fe", edge=F.BLUE, fs=12.0)
    _box(ax, 8.45, 1.13, 3.20, 1.30, r"$n(C)=0.0200\ mol$", face="#f0fdf4", edge=F.GREEN, fs=12.0)
    _box(ax, 8.45, 0.10, 3.20, 0.72, r"質量差：$n(O)=0.0200\ mol$", face="#fdf2f8", edge=F.PURPLE, fs=11.0)
    ax.text(3.85, 0.42, r"原子比 $C:H:O=1:2:1$；再以分子量決定倍數", fontsize=12.4, ha="center", color=F.INK)
    return _save(fig, "選化V-1-燃燒分析裝置與資料流.svg")


def fig_functional_groups():
    groups = [
        ("$C=C$", "烯", "加成／褪色", "#eff6ff"),
        ("$R-OH$", "醇", "氫鍵／氧化", "#e0f2fe"),
        ("$R-CHO$", "醛", "銀鏡", "#f0fdf4"),
        ("$R-CO-R'$", "酮", "羰基", "#f8fafc"),
        ("$R-COOH$", "羧酸", "$HCO_3^-$ 放氣", "#fff7dd"),
        ("$R-COOR'$", "酯", "水解", "#fef3c7"),
        ("$RNH_2$", "胺", "受質子／成鹽", "#fdf2f8"),
        ("$RCONH_2$", "醯胺", "氫鍵／水解", "#f3e8ff"),
    ]
    assert len(groups) == 8
    fig, ax = _blank("官能基把結構特徵連到物性與可觀察反應", height=6.4)
    for index, (formula, name, evidence, face) in enumerate(groups):
        row, col = divmod(index, 4)
        x = 0.25 + col * 2.95
        y = 3.18 - row * 2.50
        _box(ax, x, y, 2.55, 1.98, "", face=face, edge=F.BLUE if row == 0 else F.PURPLE, lw=1.4)
        ax.text(x + 1.275, y + 1.48, formula, ha="center", va="center", fontsize=15)
        ax.text(x + 1.275, y + 0.93, name, ha="center", va="center", fontsize=12.2, weight="bold")
        ax.text(x + 1.275, y + 0.40, evidence, ha="center", va="center", fontsize=10.4)
    ax.text(6, 0.18, "先辨認官能基，再選試劑；顏色、氣體或沉澱需有空白與陽性對照", ha="center", fontsize=11.4)
    return _save(fig, "選化V-1-官能基分類圖譜.svg")


def fig_naming_flow():
    steps = [
        ("1", "主要官能基", "決定詞尾"),
        ("2", "最長主鏈", "必須包含主官能基"),
        ("3", "編號方向", "主官能基位碼最小"),
        ("4", "雙／三鍵", "標出位置"),
        ("5", "取代基", "位碼、數目、字母序"),
        ("6", "組合名稱", "位碼＋取代基\n＋母體＋詞尾"),
    ]
    assert len(steps) == 6
    fig, ax = _blank("有機命名是一條有優先順序的結構演算法", height=5.5)
    for i, (number, title, note) in enumerate(steps):
        x = 0.25 + 1.94 * i
        color = [F.BLUE, F.BLUE, F.PURPLE, F.AMBER, F.GREEN, F.RED][i]
        _box(ax, x, 2.02, 1.55, 1.88, "", face="#ffffff", edge=color, lw=1.8)
        ax.text(x + 0.78, 3.54, number, ha="center", va="center", fontsize=18, weight="bold", color=color)
        ax.text(x + 0.78, 2.93, title, ha="center", va="center", fontsize=11.1, weight="bold")
        ax.text(x + 0.78, 2.42, note, ha="center", va="center", fontsize=8.9)
        if i < 5:
            _arrow(ax, (x + 1.57, 2.96), (x + 1.90, 2.96), color=F.GRID, yoff=0)
    _box(
        ax,
        2.00,
        0.42,
        8.00,
        0.95,
        r"$CH_3CH=C(CH_3)CH_2OH\ \longrightarrow\ 2$-methylbut-$2$-en-$1$-ol",
        face="#eff6ff",
        edge=F.BLUE,
        fs=13.5,
    )
    return _save(fig, "選化V-1-有機命名流程.svg")


def fig_hydrocarbon_reactions():
    fig, ax = _blank("烴類反應先辨認鍵結，再套用相應條件")
    _section(
        ax,
        0.25,
        "烷：取代",
        [
            (r"$CH_4+Cl_2$", "#eff6ff"),
            (r"$h\nu:\ CH_3Cl+HCl$", "#f8fafc"),
            ("一個 C–H 換成 C–Cl", "#f0fdf4"),
        ],
        color=F.BLUE,
    )
    _section(
        ax,
        4.28,
        "烯：加成",
        [
            (r"$CH_3CH=CH_2+HBr$", "#fff7dd"),
            (r"$\longrightarrow CH_3CHBrCH_3$", "#f8fafc"),
            (r"$\pi$ 鍵轉為兩個新 $\sigma$ 鍵", "#f0fdf4"),
        ],
        color=F.AMBER,
    )
    _section(
        ax,
        8.30,
        "苯：保留芳香性取代",
        [
            (r"$C_6H_6+Br_2$", "#fdf2f8"),
            (r"$FeBr_3:\ C_6H_5Br+HBr$", "#f8fafc"),
            ("室溫無催化：溴水保色", "#f0fdf4"),
        ],
        color=F.PURPLE,
    )
    return _save(fig, "選化V-1-烴類反應路線.svg")


def fig_interactions_boiling():
    boiling = np.array([78.4, -24.8, -42.1])
    labels = ["ethanol", "dimethyl ether", "propane"]
    solubility = np.array([7.9, 2.7, 0.59])
    assert boiling[0] > boiling[1] > boiling[2]
    assert np.all(np.diff(solubility) < 0)
    fig, axes = plt.subplots(1, 2, figsize=(12, 5.7))
    ax = axes[0]
    colors = [F.BLUE, F.PURPLE, F.AMBER]
    ax.bar(labels, boiling, color=colors, width=0.62)
    ax.axhline(0, color=F.INK, lw=1.0)
    ax.set_ylabel("正常沸點 / °C")
    ax.set_title("分子量接近：能形成分子間氫鍵者沸點最高", weight="bold")
    ax.text(0, 83, "$O-H\\cdots O$ 氫鍵", ha="center", color=F.BLUE, fontsize=11)
    F.clean_grid(ax)
    ax = axes[1]
    alcohols = ["1-butanol", "1-pentanol", "1-hexanol"]
    ax.plot(alcohols, solubility, marker="o", lw=2.5, color=F.GREEN)
    for x, y in zip(alcohols, solubility):
        ax.text(x, y + 0.35, f"{y:g}", ha="center", fontsize=10)
    ax.set_ylabel("約略水溶解度 / (g per 100 g water)")
    ax.set_title("同系列碳鏈增長：疏水骨架占比上升", weight="bold")
    ax.set_ylim(0, 9.2)
    F.clean_grid(ax)
    fig.suptitle("結構先決定分子間作用力，再反映在沸點與溶解度", fontsize=16, y=0.99)
    fig.subplots_adjust(left=0.08, right=0.98, bottom=0.18, top=0.80, wspace=0.30)
    return _save(fig, "選化V-1-分子間作用力與沸點.svg")


def fig_alcohol_oxidation():
    fig, ax = _blank("羥基碳上的 H 決定溫和氧化能否形成羰基")
    _section(
        ax,
        0.25,
        "一級醇",
        [
            (r"$RCH_2OH$", "#eff6ff"),
            (r"$[O]:\ RCHO$", "#f8fafc"),
            ("再氧化 → $RCOOH$；醛可呈銀鏡", "#f0fdf4"),
        ],
        color=F.BLUE,
    )
    _section(
        ax,
        4.28,
        "二級醇",
        [
            (r"$R_2CHOH$", "#fff7dd"),
            (r"$[O]:\ R_2C=O$", "#f8fafc"),
            ("產物為酮；通常無銀鏡", "#f0fdf4"),
        ],
        color=F.AMBER,
    )
    _section(
        ax,
        8.30,
        "三級醇",
        [
            (r"$R_3COH$", "#fdf2f8"),
            ("羥基碳上 0 個 H", "#f8fafc"),
            ("不斷 C–C 鍵的溫和氧化無羰基產物", "#f0fdf4"),
        ],
        color=F.PURPLE,
    )
    return _save(fig, "選化V-1-醇氧化與官能基檢驗.svg")


def fig_carbonyl_acid_ester():
    fig, ax = _blank("含氧官能基反應網：箭頭條件決定產物形態")
    _box(ax, 0.35, 3.55, 2.35, 1.05, r"一級醇  $RCH_2OH$", face="#eff6ff", edge=F.BLUE, fs=12.0)
    _box(ax, 3.35, 3.55, 2.15, 1.05, r"醛  $RCHO$", face="#f0fdf4", edge=F.GREEN, fs=12.5)
    _box(ax, 6.25, 3.55, 2.30, 1.05, r"羧酸  $RCOOH$", face="#fff7dd", edge=F.AMBER, fs=12.0)
    _box(ax, 9.35, 3.55, 2.25, 1.05, r"酯  $RCOOR'$", face="#fdf2f8", edge=F.PURPLE, fs=12.0)
    _arrow(ax, (2.72, 4.08), (3.30, 4.08), "[O]", color=F.BLUE)
    _arrow(ax, (5.52, 4.08), (6.20, 4.08), "[O]", color=F.GREEN)
    _arrow(ax, (8.57, 4.08), (9.30, 4.08), r"$+R'OH,\ H^+$", color=F.AMBER)
    _box(ax, 1.10, 1.05, 2.70, 1.10, "Tollens：銀鏡\n醛被氧化", face="#f8fafc", edge=F.GREEN, fs=11.0)
    _box(ax, 4.65, 1.05, 2.70, 1.10, r"$+HCO_3^-$：$CO_2\uparrow$" + "\n羧酸形成羧酸鹽", face="#f8fafc", edge=F.AMBER, fs=11.0)
    _box(ax, 8.20, 1.05, 2.70, 1.10, r"$+OH^-,\Delta$" + "\n羧酸鹽＋醇", face="#f8fafc", edge=F.PURPLE, fs=11.0)
    _arrow(ax, (4.42, 3.50), (2.55, 2.20), "檢驗", color=F.GREEN)
    _arrow(ax, (7.35, 3.50), (6.35, 2.20), "酸鹼證據", color=F.AMBER)
    _arrow(ax, (10.42, 3.50), (9.58, 2.20), "鹼化", color=F.PURPLE)
    return _save(fig, "選化V-1-羰基羧酸酯反應網.svg")


def fig_aspirin():
    theoretical = (1.38 / 138.0) * 180.0
    actual = 1.44
    yield_percent = actual / theoretical * 100
    assert np.isclose(theoretical, 1.80)
    assert np.isclose(yield_percent, 80.0)
    fig, ax = _blank("阿司匹靈：合成流程與純度證據需同時閉合")
    steps = [
        ("水楊酸 1.38 g\n＋過量醋酸酐", "#eff6ff", F.BLUE),
        ("酸催化、加熱\n酚性 OH 乙醯化", "#fff7dd", F.AMBER),
        ("加水、冷卻\n結晶、減壓過濾", "#f0fdf4", F.GREEN),
        ("再結晶、乾燥\n阿司匹靈 1.44 g", "#fdf2f8", F.PURPLE),
    ]
    for i, (text, face, edge) in enumerate(steps):
        x = 0.25 + i * 2.95
        _box(ax, x, 3.28, 2.35, 1.34, text, face=face, edge=edge, fs=11.2, lw=1.7)
        if i < 3:
            _arrow(ax, (x + 2.37, 3.95), (x + 2.88, 3.95), color=edge, yoff=0)
    _box(ax, 0.55, 1.02, 3.25, 1.15, "計量\n理論 1.80 g；產率 80.0%", face="#eff6ff", edge=F.BLUE, fs=11.7)
    _box(ax, 4.35, 1.02, 3.25, 1.15, "$FeCl_3$：紫色愈淡\n酚性水楊酸殘留愈少", face="#fdf2f8", edge=F.PURPLE, fs=11.2)
    _box(ax, 8.15, 1.02, 3.25, 1.15, "熔點區間窄且接近標準\n支持整體純度較高", face="#f0fdf4", edge=F.GREEN, fs=11.2)
    ax.text(6, 0.34, "通風櫥＋護目鏡＋手套；有機母液、酸性水相、固體殘渣分流", ha="center", fontsize=11.0, color=F.RED)
    return _save(fig, "選化V-1-阿司匹靈製備與純度.svg")


def fig_acid_base_extraction():
    fig, ax = _blank("酸鹼萃取：改變電荷，改變所在液相")
    _box(ax, 0.25, 3.62, 2.55, 1.15, "乙醚層\naniline＋benzoic acid＋naphthalene", face="#fff7dd", edge=F.AMBER, fs=10.5)
    _arrow(ax, (2.83, 4.18), (4.05, 4.18), "稀 HCl", color=F.BLUE)
    _box(ax, 4.08, 3.62, 3.15, 1.15, "水層：$C_6H_5NH_3^+$\n有機層：酸＋萘", face="#eff6ff", edge=F.BLUE, fs=11.0)
    _arrow(ax, (7.25, 4.18), (8.47, 4.18), "$NaHCO_3$", color=F.GREEN)
    _box(ax, 8.50, 3.62, 3.15, 1.15, "水層：$C_6H_5COO^-$\n有機層：萘", face="#f0fdf4", edge=F.GREEN, fs=11.0)
    _box(ax, 0.75, 1.10, 2.65, 1.15, "胺鹽水層＋$OH^-$\n→ aniline", face="#fdf2f8", edge=F.PURPLE, fs=11.0)
    _box(ax, 4.68, 1.10, 2.65, 1.15, "benzoate 水層＋$H^+$\n→ benzoic acid", face="#fff7dd", edge=F.AMBER, fs=11.0)
    _box(ax, 8.62, 1.10, 2.65, 1.15, "有機層除去乙醚\n→ naphthalene", face="#f8fafc", edge="#64748b", fs=11.0)
    _arrow(ax, (5.15, 3.55), (2.68, 2.30), "分層後復原", color=F.PURPLE)
    _arrow(ax, (9.20, 3.55), (6.38, 2.30), "酸化", color=F.AMBER)
    _arrow(ax, (10.65, 3.55), (9.96, 2.30), "蒸除溶劑", color=F.INK)
    ax.text(6, 0.35, "$NaHCO_3$ 放出 $CO_2$：分液漏斗每次振盪後朝無人方向洩壓", ha="center", fontsize=11.2, color=F.RED)
    return _save(fig, "選化V-1-酸鹼萃取流程.svg")


def fig_polymerization():
    molecules = 100
    links = molecules - 1
    assert links == 99
    fig, ax = _blank("兩種聚合反應的原子帳與副產物帳")
    _section(
        ax,
        0.45,
        "加成聚合",
        [
            (r"$n\,CH_2=CHR$", "#eff6ff"),
            (r"$\longrightarrow[-CH_2-CH(R)-]_n$", "#f8fafc"),
            (r"打開 $\pi$ 鍵；理想式無小分子副產物", "#f0fdf4"),
        ],
        color=F.BLUE,
        width=5.25,
    )
    _section(
        ax,
        6.30,
        "縮合聚合",
        [
            ("二元酸＋二元醇／二元胺", "#fff7dd"),
            ("形成酯鍵／醯胺鍵＋小分子", "#f8fafc"),
            ("100 個分子接一條鏈：99 個鍵、99 個水", "#f0fdf4"),
        ],
        color=F.AMBER,
        width=5.25,
    )
    return _save(fig, "選化V-1-加成與縮合聚合.svg")


def fig_reverse_monomer():
    unit_mass = 2 * 12.0 + 3 * 1.0 + 35.5
    degree = 1.25e5 / unit_mass
    assert np.isclose(unit_mass, 62.5)
    assert np.isclose(degree, 2000)
    fig, ax = _blank("由重複單元反推單體：先判主鏈來源")
    _box(ax, 0.35, 3.42, 3.05, 1.32, r"$[-CH_2-CHCl-]_n$", face="#eff6ff", edge=F.BLUE, fs=17)
    _arrow(ax, (3.43, 4.08), (4.42, 4.08), "兩主鏈碳間恢復雙鍵", color=F.BLUE)
    _box(ax, 4.45, 3.42, 2.65, 1.32, r"$CH_2=CHCl$", face="#f0fdf4", edge=F.GREEN, fs=17)
    _arrow(ax, (7.13, 4.08), (8.12, 4.08), "加成聚合", color=F.GREEN)
    _box(ax, 8.15, 3.42, 3.35, 1.32, "vinyl chloride\n側基 Cl 保留", face="#fdf2f8", edge=F.PURPLE, fs=12.0)
    _box(ax, 1.12, 1.12, 4.15, 1.20, r"重複單元式量 $=62.5\ g\,mol^{-1}$", face="#fff7dd", edge=F.AMBER, fs=12.5)
    _box(ax, 6.48, 1.12, 4.15, 1.20, r"$\bar n=(1.25\times10^5)/62.5=2000$", face="#fff7dd", edge=F.AMBER, fs=12.5)
    return _save(fig, "選化V-1-聚合物反推單體.svg")


def fig_natural_polymers():
    amino_acids = 20
    peptide_bonds = amino_acids - 1
    assert peptide_bonds == 19
    fig, ax = _blank("天然聚合物：單體相同，鍵結方向、分支與交聯仍可改變功能", height=6.3)
    panels = [
        ("天然橡膠", "cis-1,4-polyisoprene\n柔軟鏈＋少量硫交聯\n→ 可伸展並回復", F.BLUE),
        ("多醣", "$\\alpha$ 鍵＋分支：儲能\n$\\beta(1\\to4)$ 直鏈：纖維\n→ 酵素選擇性不同", F.GREEN),
        ("蛋白質", "$n$ 個胺基酸\n→ $n-1$ 個肽鍵＋水\n20-mer：19 個水", F.AMBER),
        ("核酸", "磷酸二酯主鏈\nA–T、G–C 互補\n→ 序列與複製", F.PURPLE),
    ]
    for i, (title, body, color) in enumerate(panels):
        x = 0.25 + i * 2.95
        _box(ax, x, 1.10, 2.55, 3.98, "", face="#ffffff", edge=color, lw=1.8)
        ax.add_patch(Rectangle((x, 4.18), 2.55, 0.90, facecolor=color, edgecolor=color))
        ax.text(x + 1.275, 4.63, title, ha="center", va="center", color="white", fontsize=12.2, weight="bold")
        ax.text(x + 1.275, 2.82, body, ha="center", va="center", fontsize=11.0, linespacing=1.55)
    ax.text(6, 0.38, "結構層級：單體 → 共價鍵結 → 鏈形與分支 → 鏈間作用 → 巨觀功能", ha="center", fontsize=11.4)
    return _save(fig, "選化V-1-天然聚合物鍵結.svg")


def fig_synthetic_polymers():
    swelling = np.array([38.0, 8.0])
    assert swelling[1] < swelling[0]
    fig, axes = plt.subplots(1, 2, figsize=(12, 5.8), gridspec_kw={"width_ratios": [1.28, 0.92]})
    ax = axes[0]
    ax.axis("off")
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    rows = [
        ("PE", "非極性柔軟主鏈", "薄膜／絕緣", "#eff6ff"),
        ("PET", "芳香環＋酯基", "瓶材／纖維", "#f0fdf4"),
        ("nylon", "醯胺氫鍵", "耐磨纖維", "#fff7dd"),
        ("熱固樹脂", "高密度交聯", "耐熱定形", "#fdf2f8"),
    ]
    for i, (name, structure, use, face) in enumerate(rows):
        y = 8.2 - i * 2.0
        _box(ax, 0.30, y, 2.0, 1.25, name, face=face, edge=F.BLUE, fs=12.0)
        _box(ax, 2.65, y, 3.1, 1.25, structure, face="#ffffff", edge="#94a3b8", fs=10.8)
        _arrow(ax, (5.78, y + 0.63), (6.62, y + 0.63), "決定", color=F.GREEN, yoff=0.15)
        _box(ax, 6.65, y, 2.8, 1.25, use, face=face, edge=F.GREEN, fs=11.2)
    ax.set_title("主鏈、側基與交聯連到用途", fontsize=14, weight="bold")
    ax = axes[1]
    bars = ax.bar(["SBR", "NBR"], swelling, color=[F.AMBER, F.PURPLE], width=0.62)
    ax.bar_label(bars, labels=["38%", "8%"], padding=4, fontsize=11)
    ax.set_ylabel("浸機油 24 h 的質量增加率")
    ax.set_ylim(0, 44)
    ax.set_title("極性腈基降低非極性油膨潤", fontsize=13.5, weight="bold")
    F.clean_grid(ax)
    fig.suptitle("人造聚合物的結構—性質—用途—回收是一條連續推理鏈", fontsize=16, y=0.99)
    fig.subplots_adjust(left=0.04, right=0.98, bottom=0.14, top=0.82, wspace=0.20)
    return _save(fig, "選化V-1-人造聚合物結構與用途.svg")


def main():
    fig_structure_isomers()
    fig_combustion_analysis()
    fig_functional_groups()
    fig_naming_flow()
    fig_hydrocarbon_reactions()
    fig_interactions_boiling()
    fig_alcohol_oxidation()
    fig_carbonyl_acid_ester()
    fig_aspirin()
    fig_acid_base_extraction()
    fig_polymerization()
    fig_reverse_monomer()
    fig_natural_polymers()
    fig_synthetic_polymers()


if __name__ == "__main__":
    main()
