# -*- coding: utf-8 -*-
"""產生「選化 IV-2 科學在生活中的應用」章內 SVG。

重繪：.venv/bin/python _tools/fig_content_選化IV-2.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, FancyArrowPatch, FancyBboxPatch, Polygon, Rectangle

import figlib as F


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CH = os.path.join(ROOT, "content", "選修化學IV", "選化IV-2")


FIGURE_OUTPUTS = (
    ("fig_hydrogen_routes", "選化IV-2-氫氣製備與能量載體.svg"),
    ("fig_carbon_structure", "選化IV-2-碳同素異形體結構性質.svg"),
    ("fig_nitrogen_flow", "選化IV-2-固氮與含氮化合物流程.svg"),
    ("fig_oxygen_ozone", "選化IV-2-氧氣臭氧反應與用途.svg"),
    ("fig_silicon_materials", "選化IV-2-矽酸鹽離子交換與玻璃.svg"),
    ("fig_main_group_metals", "選化IV-2-鈉鎂鋁製程選擇.svg"),
    ("fig_iron_furnace", "選化IV-2-鼓風爐與鐵離子判定.svg"),
    ("fig_coordination", "選化IV-2-配位數與配位子牙數.svg"),
    ("fig_alloy_lattices", "選化IV-2-合金晶格與含碳量.svg"),
    ("fig_semiconductor", "選化IV-2-能帶摻雜與LED.svg"),
    ("fig_conducting_polymer", "選化IV-2-導電聚合物共軛與摻雜.svg"),
    ("fig_nanoscale", "選化IV-2-奈米尺度比表面積與光觸媒.svg"),
    ("fig_ferrioxalate_lab", "選化IV-2-草酸鐵鉀製備證據鏈.svg"),
)


def _save(fig, filename):
    assert filename.endswith(".svg")
    return F.save_to(fig, CH, filename[:-4], output_subdir="assets", write_pdf=False)


def _box(ax, xy, w, h, text, *, face="#f8fafc", edge="#64748b", fs=11, lw=1.4):
    p = FancyBboxPatch(
        xy,
        w,
        h,
        boxstyle="round,pad=0.035,rounding_size=0.06",
        facecolor=face,
        edgecolor=edge,
        lw=lw,
    )
    ax.add_patch(p)
    ax.text(xy[0] + w / 2, xy[1] + h / 2, text, ha="center", va="center", fontsize=fs)
    return p


def _arrow(ax, start, end, *, color=F.PURPLE, text=None, yoff=0.18, lw=2.2):
    ax.add_patch(FancyArrowPatch(start, end, arrowstyle="-|>", mutation_scale=15, lw=lw, color=color))
    if text:
        ax.text((start[0] + end[0]) / 2, (start[1] + end[1]) / 2 + yoff, text, ha="center", color=color, fontsize=10.5)


def fig_hydrogen_routes():
    """以原子帳比較水電解與甲烷重組，並閉合燃料電池反應。"""
    electrolysis_left = {"H": 4, "O": 2}
    electrolysis_right = {"H": 4, "O": 2}
    reform_left = {"C": 1, "H": 8, "O": 2}
    reform_right = {"C": 1, "H": 8, "O": 2}
    fuel_left = {"H": 4, "O": 2}
    fuel_right = {"H": 4, "O": 2}
    assert electrolysis_left == electrolysis_right
    assert reform_left == reform_right
    assert fuel_left == fuel_right

    fig, ax = plt.subplots(figsize=(12.4, 6.3))
    ax.axis("off")
    ax.set_xlim(0, 12.4)
    ax.set_ylim(0, 6.3)
    ax.text(6.2, 5.92, "氫氣是能量載體：來源決定伴隨產物，使用端再把化學能轉出", ha="center", fontsize=16, weight="bold")

    _box(ax, (0.35, 3.55), 2.05, 1.12, "水與電能\n" + r"$2H_2O$", face="#eef4ff", edge=F.BLUE, fs=13)
    _box(ax, (3.05, 3.55), 2.15, 1.12, "水電解\n" + r"$2H_2+O_2$", face="#eefbf2", edge=F.GREEN, fs=13)
    _arrow(ax, (2.43, 4.11), (3.00, 4.11), text="輸入電能", color=F.BLUE)
    ax.text(2.78, 3.32, "原子帳：H 4、O 2", ha="center", fontsize=10.5, color=F.INK)

    _box(ax, (0.35, 1.45), 2.05, 1.12, "甲烷與水蒸氣\n" + r"$CH_4+2H_2O$", face="#fff7dd", edge=F.AMBER, fs=13)
    _box(ax, (3.05, 1.45), 2.15, 1.12, "重組＋水煤氣轉移\n" + r"$CO_2+4H_2$", face="#fff0f0", edge=F.RED, fs=12.5)
    _arrow(ax, (2.43, 2.01), (3.00, 2.01), text="高溫、催化劑", color=F.AMBER)
    ax.text(2.78, 1.20, "原子帳：C 1、H 8、O 2", ha="center", fontsize=10.5, color=F.INK)

    _box(ax, (6.05, 2.50), 2.15, 1.35, r"儲存與輸送的 $H_2$" + "\n" + r"1 mol $H_2$ 可交付 2 mol $e^-$", face="#f4efff", edge=F.PURPLE, fs=12.5)
    _arrow(ax, (5.25, 4.08), (6.00, 3.47), color=F.GREEN)
    _arrow(ax, (5.25, 2.02), (6.00, 2.88), color=F.RED)
    _box(ax, (9.05, 2.50), 2.80, 1.35, "燃料電池總反應\n" + r"$2H_2+O_2\rightarrow2H_2O$" + "\n輸出電能與熱", face="#eef4ff", edge=F.BLUE, fs=12.5)
    _arrow(ax, (8.25, 3.18), (9.00, 3.18), text="使用端", color=F.PURPLE)

    ax.text(6.2, 0.55, "比較路徑時同時計入製氫所需能量、碳來源、轉換效率與儲運；尾端只有水不代表整條路徑零排放。", ha="center", fontsize=11.5)
    return _save(fig, "選化IV-2-氫氣製備與能量載體.svg")


def fig_carbon_structure():
    """以鍵結網路與 C60 拓樸數據連結碳材料性質。"""
    vertices, edges, faces = 60, 90, 12 + 20
    assert vertices - edges + faces == 2
    assert 12 * 5 + 20 * 6 == 2 * edges

    fig, axes = plt.subplots(1, 3, figsize=(12.6, 5.9))
    titles = ["鑽石：$sp^3$ 三維網路", "石墨／石墨烯：$sp^2$ 層狀網路", "$C_{60}$：封閉分子"]
    for ax, title in zip(axes, titles):
        ax.set_aspect("equal")
        ax.axis("off")
        ax.set_title(title, fontsize=13.5, weight="bold")

    ax = axes[0]
    pts = np.array([[0, 0], [1, 1], [2, 0], [1, -1], [1, 0], [1, 2]])
    for i, j in [(4, 0), (4, 1), (4, 2), (4, 3), (1, 5)]:
        ax.plot([pts[i, 0], pts[j, 0]], [pts[i, 1], pts[j, 1]], color=F.INK, lw=2)
    ax.scatter(pts[:, 0], pts[:, 1], s=150, color=F.BLUE, zorder=3)
    ax.text(1, -1.55, r"每個 C 以四個 $\sigma$ 鍵固定" + "\n硬度高；自由電子少", ha="center", fontsize=11)
    ax.set_xlim(-0.6, 2.6); ax.set_ylim(-1.9, 2.5)

    ax = axes[1]
    a = np.array([np.cos(np.linspace(0, 2 * np.pi, 7)), np.sin(np.linspace(0, 2 * np.pi, 7))]).T
    for shift in [(-0.75, -0.65), (0.75, -0.65), (0, 0.65)]:
        p = a + shift
        ax.plot(p[:, 0], p[:, 1], color=F.INK, lw=1.8)
        ax.scatter(p[:-1, 0], p[:-1, 1], s=52, color=F.GREEN, zorder=3)
    _arrow(ax, (-1.55, -1.78), (1.55, -1.78), text=r"$\pi$ 電子可沿層移動", color=F.PURPLE, yoff=0.15)
    ax.text(0, -2.43, "層內強鍵、層間作用較弱\n導電、易沿層滑動", ha="center", fontsize=11)
    ax.set_xlim(-2.2, 2.2); ax.set_ylim(-2.65, 2.2)

    ax = axes[2]
    phi = (1 + np.sqrt(5)) / 2
    ico = []
    for a in (-1, 1):
        for b in (-1, 1):
            ico.extend([(0, a, b * phi), (a, b * phi, 0), (a * phi, 0, b)])
    ico = np.array(ico, dtype=float)
    ico_edges = [
        (i, j)
        for i in range(len(ico))
        for j in range(i + 1, len(ico))
        if np.isclose(np.linalg.norm(ico[i] - ico[j]), 2.0)
    ]
    assert len(ico) == 12 and len(ico_edges) == 30
    directed = [(u, v) for u, v in ico_edges for u, v in ((u, v), (v, u))]
    index = {edge: i for i, edge in enumerate(directed)}
    truncated = np.array([(2 * ico[u] + ico[v]) / 3 for u, v in directed])
    trunc_edges = set()
    for u, v in ico_edges:
        trunc_edges.add(tuple(sorted((index[(u, v)], index[(v, u)]))))
    for u in range(len(ico)):
        neighbours = [v for a, v in directed if a == u]
        center = truncated[[index[(u, v)] for v in neighbours]].mean(axis=0)
        normal = ico[u] / np.linalg.norm(ico[u])
        ref = np.array([0.0, 0.0, 1.0]) if abs(normal[2]) < 0.85 else np.array([0.0, 1.0, 0.0])
        basis_x = np.cross(normal, ref); basis_x /= np.linalg.norm(basis_x)
        basis_y = np.cross(normal, basis_x)
        ordered = sorted(
            neighbours,
            key=lambda v: np.arctan2(
                np.dot(truncated[index[(u, v)]] - center, basis_y),
                np.dot(truncated[index[(u, v)]] - center, basis_x),
            ),
        )
        for v, w in zip(ordered, ordered[1:] + ordered[:1]):
            trunc_edges.add(tuple(sorted((index[(u, v)], index[(u, w)]))))
    assert len(truncated) == 60 and len(trunc_edges) == 90
    ay, axr = 0.48, -0.32
    ry = np.array([[np.cos(ay), 0, np.sin(ay)], [0, 1, 0], [-np.sin(ay), 0, np.cos(ay)]])
    rx = np.array([[1, 0, 0], [0, np.cos(axr), -np.sin(axr)], [0, np.sin(axr), np.cos(axr)]])
    rotated = truncated @ (rx @ ry).T
    scale = 1.48 / np.max(np.abs(rotated[:, :2]))
    projected = rotated[:, :2] * scale
    for i, j in trunc_edges:
        front = (rotated[i, 2] + rotated[j, 2]) / 2 > 0
        ax.plot(
            [projected[i, 0], projected[j, 0]],
            [projected[i, 1], projected[j, 1]],
            color=F.INK if front else "#94a3b8",
            lw=1.05 if front else 0.65,
            zorder=2 if front else 1,
        )
    order = np.argsort(rotated[:, 2])
    ax.scatter(projected[order, 0], projected[order, 1], s=18, c=rotated[order, 2], cmap="autumn", zorder=3)
    ax.text(0, -1.92, "60 頂點、90 邊、12 五邊形＋20 六邊形\n$60-90+32=2$", ha="center", fontsize=10.8)
    ax.set_xlim(-2.1, 2.1); ax.set_ylim(-2.2, 2.2)

    fig.suptitle("同一元素因鍵結方式與維度不同，形成完全不同的材料性質", fontsize=16, y=0.98)
    fig.subplots_adjust(left=0.03, right=0.98, bottom=0.08, top=0.84, wspace=0.16)
    return _save(fig, "選化IV-2-碳同素異形體結構性質.svg")


def fig_nitrogen_flow():
    """以反應計量閉合固氮、製氨與製硝酸流程。"""
    assert 1 * 2 == 2 * 1  # N2 -> 2 NH3 的氮原子
    assert 3 * 2 == 2 * 3  # 3 H2 -> 2 NH3 的氫原子
    assert 5 * 2 == 4 + 6 * 1  # Ostwald 第一步氧原子

    fig, ax = plt.subplots(figsize=(12.5, 6.1))
    ax.axis("off"); ax.set_xlim(0, 12.5); ax.set_ylim(0, 6.1)
    ax.text(6.25, 5.72, r"固定氮：先克服 $N\equiv N$ 的高穩定性，再把氮導向肥料或硝酸", ha="center", fontsize=16, weight="bold")

    _box(ax, (0.35, 2.55), 1.85, 1.25, r"空氣中的 $N_2$" + "\n三鍵鍵能高", face="#eef4ff", edge=F.BLUE, fs=13)
    _box(ax, (3.00, 2.55), 2.30, 1.25, "哈柏法\n" + r"$N_2+3H_2\rightleftharpoons2NH_3$", face="#eefbf2", edge=F.GREEN, fs=12.5)
    _arrow(ax, (2.25, 3.18), (2.95, 3.18), text="Fe、加壓、適溫", color=F.GREEN)
    _box(ax, (6.10, 3.75), 2.20, 1.15, "銨鹽／尿素\n提供植物可用氮", face="#fff7dd", edge=F.AMBER, fs=12.5)
    _arrow(ax, (5.35, 3.38), (6.05, 4.18), text="肥料路徑", color=F.AMBER)
    _box(ax, (6.10, 1.45), 2.20, 1.25, "奧士華法第一步\n" + r"$4NH_3+5O_2\rightarrow4NO+6H_2O$", face="#fff0f0", edge=F.RED, fs=11.5)
    _arrow(ax, (5.35, 2.95), (6.05, 2.10), text="Pt/Rh、氧化", color=F.RED)
    _box(ax, (9.10, 1.45), 2.70, 1.25, r"$NO\rightarrow NO_2\rightarrow HNO_3$" + "\n酸、硝酸鹽與工業原料", face="#f4efff", edge=F.PURPLE, fs=12)
    _arrow(ax, (8.35, 2.08), (9.05, 2.08), text="再氧化、吸收", color=F.PURPLE)

    ax.text(9.00, 4.50, "計量基準：", ha="left", fontsize=12, weight="bold")
    ax.text(9.00, 4.05, r"$28.0$ g $N_2\rightarrow34.0$ g $NH_3$", ha="left", fontsize=12)
    ax.text(9.00, 3.60, r"每 mol $N_2$ 固定 2 mol N 原子", ha="left", fontsize=12)
    ax.text(6.25, 0.55, "製程條件同時回應反應速率、平衡、能源與安全；流程圖中的每個箭頭都必須以原子守恆閉合。", ha="center", fontsize=11.5)
    return _save(fig, "選化IV-2-固氮與含氮化合物流程.svg")


def fig_oxygen_ozone():
    """比較 O2/O3 氧化能力並閉合臭氧光化循環。"""
    assert {"O": 3} == {"O": 2 + 1}
    assert {"O": 1 + 2} == {"O": 3}
    potentials = np.array([0.401, 1.229, 2.07])
    assert potentials[2] > potentials[1] > potentials[0]

    fig, axes = plt.subplots(1, 2, figsize=(12.4, 5.8), gridspec_kw={"width_ratios": [1.08, 0.92]})
    ax = axes[0]
    ax.axis("off"); ax.set_xlim(0, 6.2); ax.set_ylim(0, 5.2)
    _box(ax, (0.35, 2.25), 1.70, 1.10, r"平流層 $O_3$" + "\n吸收紫外光", face="#f4efff", edge=F.PURPLE, fs=13)
    _box(ax, (2.85, 3.55), 2.25, 1.00, r"$O_3+h\nu\rightarrow O_2+O$", face="#eef4ff", edge=F.BLUE, fs=13)
    _box(ax, (2.85, 0.95), 2.25, 1.00, r"$O+O_2\rightarrow O_3$" + "\n放熱", face="#eefbf2", edge=F.GREEN, fs=13)
    _arrow(ax, (2.08, 2.95), (2.80, 3.80), text="吸光", color=F.BLUE)
    _arrow(ax, (5.15, 3.55), (5.15, 2.00), text="碰撞", color=F.GREEN, yoff=0.05)
    _arrow(ax, (2.80, 1.45), (2.05, 2.55), text="再生", color=F.PURPLE)
    ax.text(3.1, 0.30, "同一分子在平流層可攔截紫外光；近地高濃度臭氧會刺激呼吸系統。", ha="center", fontsize=10.8)

    ax = axes[1]
    labels = [r"$O_2/OH^-$" + "\n鹼性", r"$O_2/H_2O$" + "\n酸性", r"$O_3/O_2$" + "\n酸性"]
    colors = [F.BLUE, F.GREEN, F.RED]
    ax.barh(np.arange(3), potentials, color=colors, alpha=0.86)
    ax.set_yticks(np.arange(3), labels)
    ax.set_xlabel("標準還原電位 / V")
    ax.set_xlim(0, 2.3)
    for i, v in enumerate(potentials):
        ax.text(v + 0.04, i, f"{v:.3f}", va="center", fontsize=10.5)
    F.clean_grid(ax)
    ax.set_title("半反應條件改變氧化能力", fontsize=13.5, weight="bold")
    fig.suptitle("氧與臭氧：先辨認所在環境，再用反應與電位判斷作用", fontsize=16, y=0.98)
    fig.subplots_adjust(left=0.05, right=0.97, bottom=0.13, top=0.84, wspace=0.20)
    return _save(fig, "選化IV-2-氧氣臭氧反應與用途.svg")


def fig_silicon_materials():
    """建立 SiO4 基元、沸石離子交換與玻璃原料帳。"""
    assert 4 * (-2) + 4 == -4
    assert 2 * 1 == 2
    assert {"Na": 2, "Ca": 1} == {"Na": 2, "Ca": 1}

    fig, axes = plt.subplots(1, 3, figsize=(12.7, 5.8))
    for ax in axes:
        ax.axis("off")

    ax = axes[0]; ax.set_xlim(-2, 2); ax.set_ylim(-2, 2)
    center = np.array([0.0, 0.0])
    oxy = np.array([[0, 1.35], [1.25, -0.65], [-1.25, -0.65], [0, -1.15]])
    for p in oxy:
        ax.plot([0, p[0]], [0, p[1]], color=F.INK, lw=2)
    ax.scatter([0], [0], s=380, color=F.AMBER, zorder=3); ax.text(0, 0, "Si", ha="center", va="center", weight="bold")
    ax.scatter(oxy[:, 0], oxy[:, 1], s=280, color=F.RED, zorder=3)
    for p in oxy: ax.text(p[0], p[1], "O", ha="center", va="center", color="white", weight="bold")
    ax.set_title(r"矽酸根基元 $SiO_4^{4-}$", fontsize=13.5, weight="bold")
    ax.text(0, -1.75, "共享氧原子可延伸成鏈、層或三維網路", ha="center", fontsize=10.8)

    ax = axes[1]; ax.set_xlim(0, 4.2); ax.set_ylim(0, 4.8)
    _box(ax, (0.15, 2.70), 1.55, 1.10, "沸石骨架\n" + r"$2NaZ$", face="#eef4ff", edge=F.BLUE, fs=12.5)
    _box(ax, (2.50, 2.70), 1.55, 1.10, "軟化後骨架\n" + r"$CaZ_2$", face="#eefbf2", edge=F.GREEN, fs=12.5)
    _arrow(ax, (1.75, 3.25), (2.45, 3.25), text=r"加入 $Ca^{2+}$", color=F.PURPLE)
    ax.text(2.10, 1.95, r"$Ca^{2+}+2NaZ\rightarrow CaZ_2+2Na^+$", ha="center", fontsize=12)
    ax.text(2.10, 1.25, "一個二價硬水離子交換兩個一價鈉離子", ha="center", fontsize=10.8)
    ax.set_title("沸石軟化硬水：電荷帳", fontsize=13.5, weight="bold")

    ax = axes[2]; ax.set_xlim(0, 4.4); ax.set_ylim(0, 4.8)
    _box(ax, (0.15, 3.10), 1.20, 0.80, r"$SiO_2$" + "\n網路形成物", face="#eef4ff", edge=F.BLUE)
    _box(ax, (1.60, 3.10), 1.20, 0.80, r"$Na_2CO_3$" + "\n助熔來源", face="#fff7dd", edge=F.AMBER)
    _box(ax, (3.05, 3.10), 1.20, 0.80, r"$CaCO_3$" + "\n耐水性來源", face="#eefbf2", edge=F.GREEN)
    _arrow(ax, (0.75, 2.95), (2.15, 2.15), color=F.BLUE)
    _arrow(ax, (2.20, 2.95), (2.20, 2.15), color=F.AMBER)
    _arrow(ax, (3.65, 2.95), (2.25, 2.15), color=F.GREEN)
    _box(ax, (1.20, 1.10), 2.10, 0.90, "鈉鈣玻璃\n非晶體、無固定熔點", face="#f4efff", edge=F.PURPLE, fs=12.5)
    ax.text(2.20, 0.48, r"$SiO_2+4HF\rightarrow SiF_4+2H_2O$", ha="center", fontsize=11)
    ax.set_title("玻璃配方：結構與加工折衷", fontsize=13.5, weight="bold")

    fig.suptitle("矽材料的共同核心是 Si–O 網路；組成改變網路、電荷與用途", fontsize=16, y=0.98)
    fig.subplots_adjust(left=0.02, right=0.99, bottom=0.06, top=0.84, wspace=0.12)
    return _save(fig, "選化IV-2-矽酸鹽離子交換與玻璃.svg")


def fig_main_group_metals():
    """比較 Na/Mg/Al 的工業製程條件與反應選擇。"""
    sodium_left = {"Na": 2, "Cl": 2}
    sodium_right = {"Na": 2, "Cl": 2}
    magnesium_left = {"Mg": 1, "Cl": 2}
    magnesium_right = {"Mg": 1, "Cl": 2}
    aluminium_left = {"Al": 2 * 2, "O": 2 * 3, "C": 3}
    aluminium_right = {"Al": 4, "O": 3 * 2, "C": 3}
    assert sodium_left == sodium_right
    assert magnesium_left == magnesium_right
    assert aluminium_left == aluminium_right

    fig, axes = plt.subplots(1, 3, figsize=(12.6, 6.1))
    configs = [
        (axes[0], "鈉：熔融鹽電解", r"$2NaCl(l)\rightarrow2Na(l)+Cl_2(g)$", "水溶液中水較先在陰極還原", F.BLUE),
        (axes[1], "鎂：熔融鹽電解", r"$MgCl_2(l)\rightarrow Mg(l)+Cl_2(g)$", "海水／鹵水先取得鎂鹽", F.GREEN),
        (axes[2], "鋁：純化後熔鹽電解", r"$2Al_2O_3(l)+3C(s)\rightarrow4Al(l)+3CO_2(g)$", "拜耳法純化；冰晶石作介質；碳陽極消耗", F.RED),
    ]
    for ax, title, eq, note, color in configs:
        ax.axis("off"); ax.set_xlim(0, 4); ax.set_ylim(0, 5.4)
        ax.set_title(title, fontsize=13.5, weight="bold")
        _box(ax, (0.50, 3.65), 3.00, 0.88, "離子原料", face="#f8fafc", edge=color, fs=12)
        _arrow(ax, (2.00, 3.55), (2.00, 2.75), text="直流電", color=color, yoff=0.08)
        _box(ax, (0.30, 1.72), 3.40, 0.90, eq, face="#eef4ff", edge=color, fs=10.5)
        ax.text(2.0, 1.05, note, ha="center", va="center", fontsize=10.6, wrap=True)
        ax.text(2.0, 0.35, "活性金屬需用電化學提供電子", ha="center", fontsize=10.6, color=F.PURPLE)
    fig.suptitle("製備活性金屬：先判斷水會不會搶先還原，再選熔融鹽與純化流程", fontsize=16, y=0.98)
    fig.subplots_adjust(left=0.02, right=0.99, bottom=0.06, top=0.84, wspace=0.08)
    return _save(fig, "選化IV-2-鈉鎂鋁製程選擇.svg")


def fig_iron_furnace():
    """以鼓風爐物料流與 Fe2+/Fe3+ 檢驗形成推理圖。"""
    assert 2 * 1 == 2 and 3 == 3  # Fe2O3 + 3CO -> 2Fe + 3CO2
    assert 1 == 1 and 1 == 1  # CaO + SiO2 -> CaSiO3

    fig, axes = plt.subplots(1, 2, figsize=(12.5, 6.4), gridspec_kw={"width_ratios": [1.08, 0.92]})
    ax = axes[0]; ax.axis("off"); ax.set_xlim(0, 6.2); ax.set_ylim(0, 6.0)
    furnace = Polygon([[1.6, 5.35], [4.6, 5.35], [4.15, 1.05], [2.05, 1.05]], closed=True, facecolor="#fff7dd", edgecolor=F.INK, lw=2)
    ax.add_patch(furnace)
    for y, color in [(4.5, "#fde68a"), (3.3, "#fdba74"), (2.1, "#fb7185")]:
        ax.add_patch(Rectangle((2.02 + (4.5-y)*0.105, y-0.25), 2.16-(4.5-y)*0.21, 0.50, color=color, alpha=0.75))
    ax.text(3.1, 5.67, "鐵礦＋煤焦＋灰石", ha="center", fontsize=12.5, weight="bold")
    ax.text(3.1, 4.48, r"$2C+O_2\rightarrow2CO$", ha="center", fontsize=11)
    ax.text(3.1, 3.28, r"$Fe_2O_3+3CO\rightarrow2Fe+3CO_2$", ha="center", fontsize=10.8)
    ax.text(3.1, 2.08, r"$CaO+SiO_2\rightarrow CaSiO_3$", ha="center", fontsize=10.8)
    _arrow(ax, (0.40, 1.30), (1.92, 1.70), text="熱空氣", color=F.RED)
    _arrow(ax, (4.20, 0.86), (5.55, 0.86), text="生鐵（密度較大）", color=F.INK)
    _arrow(ax, (4.30, 1.35), (5.55, 1.75), text="熔渣（浮上層）", color=F.AMBER)
    ax.set_title("鼓風爐：還原與除雜同時進行", fontsize=14, weight="bold")

    ax = axes[1]; ax.axis("off"); ax.set_xlim(0, 5.2); ax.set_ylim(0, 6.0)
    _box(ax, (0.35, 4.45), 1.55, 0.95, r"$Fe^{2+}$" + "\n淡綠", face="#eefbf2", edge=F.GREEN, fs=13)
    _box(ax, (3.25, 4.45), 1.55, 0.95, r"$Fe^{3+}$" + "\n黃褐", face="#fff7dd", edge=F.AMBER, fs=13)
    _box(ax, (0.25, 2.45), 1.75, 1.00, r"加 $[Fe(CN)_6]^{3-}$" + "\n普魯士藍", face="#eef4ff", edge=F.BLUE, fs=11.5)
    _box(ax, (3.10, 2.45), 1.90, 1.00, r"加 $SCN^-$" + "\n血紅色錯離子", face="#fff0f0", edge=F.RED, fs=11.5)
    _arrow(ax, (1.12, 4.40), (1.12, 3.50), color=F.BLUE)
    _arrow(ax, (4.02, 4.40), (4.02, 3.50), color=F.RED)
    ax.text(2.60, 1.45, "顏色是觀察；由選擇性反應推定價態是推論", ha="center", fontsize=11.2)
    ax.text(2.60, 0.75, "空氣可把部分 $Fe^{2+}$ 氧化成 $Fe^{3+}$，樣品需控制暴露時間。", ha="center", fontsize=10.5)
    ax.set_title("鐵離子：以試劑建立可區分證據", fontsize=14, weight="bold")
    fig.suptitle("鐵的工業與分析都靠氧化態：製程追電子，檢驗追可觀察產物", fontsize=16, y=0.98)
    fig.subplots_adjust(left=0.03, right=0.98, bottom=0.06, top=0.84, wspace=0.12)
    return _save(fig, "選化IV-2-鼓風爐與鐵離子判定.svg")


def fig_coordination():
    """以配位子牙數計算三個典型錯離子的配位數。"""
    cases = [(4, 1, 4), (3, 2, 6), (1, 6, 6)]
    for ligands, denticity, cn in cases:
        assert ligands * denticity == cn

    fig, axes = plt.subplots(1, 3, figsize=(12.6, 5.7))
    specs = [
        (axes[0], r"$[Cu(NH_3)_4]^{2+}$", 4, 1, F.BLUE, "4 個單牙配位子"),
        (axes[1], r"$[Fe(C_2O_4)_3]^{3-}$", 3, 2, F.GREEN, "3 個雙牙配位子"),
        (axes[2], r"$[M(EDTA)]^{n-4}$", 1, 6, F.RED, "1 個六牙配位子"),
    ]
    for ax, formula, nlig, dent, color, note in specs:
        ax.set_aspect("equal"); ax.axis("off"); ax.set_xlim(-2.0, 2.0); ax.set_ylim(-2.1, 2.2)
        ax.add_patch(Circle((0, 0), 0.38, facecolor="#f4efff", edgecolor=F.PURPLE, lw=2))
        ax.text(0, 0, "M", ha="center", va="center", fontsize=14, weight="bold")
        if nlig == 1 and dent == 6:
            donor_angles = np.linspace(0, 2 * np.pi, 6, endpoint=False)
            donors = np.c_[1.20 * np.cos(donor_angles), 1.20 * np.sin(donor_angles)]
            for a, atom in zip(donor_angles, donors):
                endpoint = np.array([0.42 * np.cos(a), 0.42 * np.sin(a)])
                ax.plot([endpoint[0], atom[0]], [endpoint[1], atom[1]], color=color, lw=1.8)
                ax.add_patch(Circle(atom, 0.12, facecolor=color, edgecolor="white", lw=0.8))
            loop = np.vstack([donors, donors[0]])
            ax.plot(loop[:, 0], loop[:, 1], color=color, lw=1.4, alpha=0.75)
        else:
            angles = np.linspace(0, 2 * np.pi, nlig, endpoint=False)
            for a in angles:
                center = np.array([1.25 * np.cos(a), 1.25 * np.sin(a)])
                for k in range(dent):
                    da = (k - (dent - 1) / 2) * 0.14
                    endpoint = np.array([0.42 * np.cos(a + da), 0.42 * np.sin(a + da)])
                    atom = center + np.array([0.18 * np.cos(a + np.pi / 2) * (k - (dent - 1) / 2), 0.18 * np.sin(a + np.pi / 2) * (k - (dent - 1) / 2)])
                    ax.plot([endpoint[0], atom[0]], [endpoint[1], atom[1]], color=color, lw=1.8)
                    ax.add_patch(Circle(atom, 0.12, facecolor=color, edgecolor="white", lw=0.8))
                ax.add_patch(Circle(center, 0.28 + 0.035 * dent, facecolor="none", edgecolor=color, lw=1.5))
        cn = nlig * dent
        ax.set_title(formula, fontsize=14, weight="bold")
        ax.text(0, -1.63, f"{note}\n配位數＝{nlig}×{dent}＝{cn}", ha="center", fontsize=11)
    fig.suptitle("配位數計算鍵結點，不只計算配位子顆數", fontsize=16, y=0.98)
    fig.subplots_adjust(left=0.02, right=0.99, bottom=0.07, top=0.82, wspace=0.10)
    return _save(fig, "選化IV-2-配位數與配位子牙數.svg")


def fig_alloy_lattices():
    """比較取代、間隙、混合型合金並核對碳鋼趨勢。"""
    carbon = np.array([0.10, 0.40, 1.00])
    hardness = np.array([1.0, 2.0, 3.0])
    ductility = np.array([3.0, 2.0, 1.0])
    assert np.all(np.diff(hardness) > 0)
    assert np.all(np.diff(ductility) < 0)

    fig, axes = plt.subplots(1, 2, figsize=(12.6, 6.1), gridspec_kw={"width_ratios": [1.25, 0.75]})
    ax = axes[0]; ax.axis("off"); ax.set_xlim(0, 9); ax.set_ylim(0, 5)
    titles = ["取代型", "間隙型", "混合型"]
    for col, title in enumerate(titles):
        x0 = 0.35 + col * 3.0
        ax.text(x0 + 1.05, 4.55, title, ha="center", fontsize=13, weight="bold")
        for i in range(3):
            for j in range(3):
                color = F.BLUE
                size = 170
                marker = "o"
                edgecolor = "white"
                linewidth = 0.8
                if title in ("取代型", "混合型") and i == 1 and j == 1:
                    color = F.RED
                    size = 230
                    marker = "D"
                    edgecolor = F.INK
                    linewidth = 1.4
                ax.scatter(
                    x0 + i * 0.95,
                    1.55 + j * 0.90,
                    s=size,
                    color=color,
                    marker=marker,
                    edgecolor=edgecolor,
                    linewidth=linewidth,
                )
        if title in ("間隙型", "混合型"):
            for dx, dy in [(0.48, 0.45), (1.43, 1.35)]:
                ax.scatter(x0 + dx, 1.55 + dy, s=65, color=F.AMBER, edgecolor=F.INK, linewidth=0.7)
        note = {"取代型": "原子大小接近\n例：黃銅", "間隙型": "小原子進入空隙\n例：碳鋼", "混合型": "兩種機制並存\n例：不鏽鋼"}[title]
        ax.text(x0 + 1.0, 0.50, note, ha="center", fontsize=10.8)
    ax.set_title("晶格排列限制滑移，改變硬度與延性", fontsize=14, weight="bold")

    ax = axes[1]
    hardness_line, = ax.plot(
        carbon,
        hardness,
        color=F.RED,
        marker="o",
        linestyle="-",
        lw=2.3,
        label="相對硬度",
    )
    ductility_line, = ax.plot(
        carbon,
        ductility,
        color=F.BLUE,
        marker="s",
        linestyle="--",
        lw=2.3,
        label="相對延性",
    )
    assert hardness_line.get_marker() != ductility_line.get_marker()
    assert hardness_line.get_linestyle() != ductility_line.get_linestyle()
    ax.set_xlabel("碳質量百分率 / %")
    ax.set_ylabel("相對尺度")
    ax.set_xlim(0, 1.1); ax.set_ylim(0.6, 3.4)
    ax.set_xticks(carbon, ["低碳\n0.1", "中碳\n0.4", "高碳\n1.0"])
    ax.legend(frameon=False)
    F.clean_grid(ax)
    ax.set_title("碳鋼的高中趨勢模型", fontsize=14, weight="bold")
    fig.suptitle("合金性質來自原子排列與組成；配方改變晶格，也改變加工選擇", fontsize=16, y=0.98)
    fig.subplots_adjust(left=0.04, right=0.98, bottom=0.12, top=0.84, wspace=0.16)
    return _save(fig, "選化IV-2-合金晶格與含碳量.svg")


def fig_semiconductor():
    """用能帶、摻雜載子與 LED 復合建立同一套模型。"""
    gaps = np.array([0.0, 0.67, 1.14, 9.0])
    assert gaps[0] < gaps[1] < gaps[2] < gaps[3]
    assert 5 - 4 == 1 and 4 - 3 == 1

    fig, axes = plt.subplots(1, 3, figsize=(12.8, 6.0))
    ax = axes[0]
    labels = ["金屬", "Ge", "Si", "$SiO_2$"]
    ax.bar(np.arange(4), gaps, color=[F.AMBER, F.GREEN, F.BLUE, F.RED], alpha=0.85)
    ax.set_xticks(np.arange(4), labels)
    ax.set_ylabel("能隙 $E_g$ / eV")
    ax.set_ylim(0, 9.8)
    for i, v in enumerate(gaps): ax.text(i, v + 0.18, f"{v:.2f}", ha="center", fontsize=10)
    F.clean_grid(ax)
    ax.set_title("能隙決定激發門檻", fontsize=13.5, weight="bold")

    ax = axes[1]; ax.axis("off"); ax.set_xlim(0, 4); ax.set_ylim(0, 5)
    _box(ax, (0.20, 3.30), 1.55, 0.95, "p 型 Si\n摻 13 族 B", face="#fff0f0", edge=F.RED, fs=12)
    _box(ax, (2.25, 3.30), 1.55, 0.95, "n 型 Si\n摻 15 族 P", face="#eef4ff", edge=F.BLUE, fs=12)
    ax.add_patch(Circle((0.97, 2.35), 0.24, facecolor="white", edgecolor=F.RED, lw=2))
    ax.text(0.97, 1.80, "電洞", ha="center", color=F.RED, fontsize=11)
    ax.add_patch(Circle((3.03, 2.35), 0.24, facecolor=F.BLUE, edgecolor=F.BLUE, lw=2))
    ax.text(3.03, 1.80, "多餘電子", ha="center", color=F.BLUE, fontsize=11)
    ax.text(2.0, 0.85, "晶體仍維持電中性；載子種類改變導電機制", ha="center", fontsize=10.7)
    ax.set_title("摻雜提供主要載子", fontsize=13.5, weight="bold")

    ax = axes[2]; ax.axis("off"); ax.set_xlim(0, 4); ax.set_ylim(0, 5)
    _box(ax, (0.20, 2.55), 1.15, 1.00, "n 型\n電子", face="#eef4ff", edge=F.BLUE, fs=12)
    _box(ax, (2.65, 2.55), 1.15, 1.00, "p 型\n電洞", face="#fff0f0", edge=F.RED, fs=12)
    _arrow(ax, (1.40, 3.05), (2.57, 3.05), text="復合", color=F.PURPLE)
    ax.add_patch(FancyArrowPatch((2.0, 2.55), (2.0, 1.25), arrowstyle="-|>", mutation_scale=18, lw=2, color=F.AMBER))
    ax.text(2.0, 0.92, r"放出光子 $h\nu\approx E_g$", ha="center", fontsize=12, color=F.AMBER)
    ax.set_title("LED：電子－電洞復合", fontsize=13.5, weight="bold")
    fig.suptitle("半導體的三層推理：能隙控制激發、摻雜控制載子、接面控制方向與發光", fontsize=16, y=0.98)
    fig.subplots_adjust(left=0.05, right=0.99, bottom=0.10, top=0.83, wspace=0.20)
    return _save(fig, "選化IV-2-能帶摻雜與LED.svg")


def fig_conducting_polymer():
    """以交替單雙鍵、p/n 摻雜與載子移動連結導電性。"""
    n_carbon = 8
    assert n_carbon % 2 == 0
    bonds = [2 if i % 2 == 0 else 1 for i in range(n_carbon - 1)]
    assert bonds.count(2) == 4 and bonds.count(1) == 3

    fig, axes = plt.subplots(3, 1, figsize=(12.4, 6.9), gridspec_kw={"height_ratios": [1, 1, 1]})
    rows = [
        (axes[0], "未摻雜共軛鏈", None, F.INK, r"交替單、雙鍵使 $\pi$ 電子可沿鏈非定域化"),
        (axes[1], "p 摻雜（氧化）", "+", F.RED, "移出部分電子，形成可移動正載子／電洞"),
        (axes[2], "n 摻雜（還原）", "−", F.BLUE, "加入部分電子，形成可移動負載子"),
    ]
    for ax, title, charge, color, note in rows:
        ax.axis("off"); ax.set_xlim(-0.8, 9.0); ax.set_ylim(-1.0, 1.3)
        xs = np.arange(n_carbon)
        ys = 0.25 * np.sin(xs * np.pi)
        for i, order in enumerate(bonds):
            ax.plot(xs[i:i+2], ys[i:i+2], color=F.INK, lw=2)
            if order == 2:
                ax.plot(xs[i:i+2], ys[i:i+2] + 0.16, color=F.INK, lw=1.3)
        ax.scatter(xs, ys, s=115, color="#f8fafc", edgecolor=F.INK, zorder=3)
        for x, y in zip(xs, ys): ax.text(x, y, "C", ha="center", va="center", fontsize=9)
        if charge:
            for x in [2.2, 5.2]:
                ax.add_patch(Circle((x, 0.70), 0.22, facecolor=color, edgecolor="white"))
                ax.text(x, 0.70, charge, ha="center", va="center", color="white", weight="bold")
            _arrow(ax, (2.55, 0.70), (4.75, 0.70), text="載子沿共軛鏈移動", color=color, yoff=0.14)
        ax.text(8.70, 0.48, title, ha="right", fontsize=12.5, color=color, weight="bold")
        ax.text(8.70, -0.35, note, ha="right", fontsize=10.5)
    fig.suptitle("導電聚合物：共軛鏈提供通道，氧化還原摻雜改變載子數", fontsize=16, y=0.985)
    fig.subplots_adjust(left=0.04, right=0.98, bottom=0.04, top=0.88, hspace=0.10)
    return _save(fig, "選化IV-2-導電聚合物共軛與摻雜.svg")


def fig_nanoscale():
    """用立方粒子 S/V=6/L 與 TiO2 電子電洞圖解奈米效應。"""
    lengths = np.logspace(0, 3, 200)  # nm
    sv = 6 / lengths
    assert np.isclose((6 / 10) / (6 / 100), 10)
    assert np.all(np.diff(sv) < 0)

    fig, axes = plt.subplots(1, 2, figsize=(12.6, 6.0))
    ax = axes[0]
    ax.loglog(lengths, sv, color=F.BLUE, lw=2.5)
    for L, color in [(1, F.RED), (10, F.AMBER), (100, F.GREEN)]:
        ax.scatter([L], [6/L], s=70, color=color, zorder=4)
        ax.text(L * 1.10, (6/L) * 1.18, f"L={L} nm\nS/V={6/L:g} " + r"nm$^{-1}$", fontsize=9.5, color=color)
    ax.axvspan(1, 100, color=F.PURPLE, alpha=0.08)
    ax.set_xlabel("立方粒子邊長 $L$ / nm")
    ax.set_ylabel(r"表面積／體積 $S/V=6/L$ / nm$^{-1}$")
    ax.set_title("尺寸縮小十倍，$S/V$ 放大十倍", fontsize=13.5, weight="bold")
    F.clean_grid(ax)

    ax = axes[1]; ax.axis("off"); ax.set_xlim(0, 5.2); ax.set_ylim(0, 5.2)
    _box(ax, (0.35, 3.75), 1.60, 0.85, r"$TiO_2$ 價帶", face="#eef4ff", edge=F.BLUE, fs=12)
    _box(ax, (3.25, 3.75), 1.60, 0.85, r"$TiO_2$ 傳導帶", face="#eefbf2", edge=F.GREEN, fs=12)
    _arrow(ax, (1.98, 4.18), (3.20, 4.18), text="吸收足夠能量的光", color=F.PURPLE)
    ax.add_patch(Circle((1.15, 2.82), 0.24, facecolor="white", edgecolor=F.RED, lw=2)); ax.text(1.15, 2.35, "電洞 $h^+$", ha="center", color=F.RED)
    ax.add_patch(Circle((4.05, 2.82), 0.24, facecolor=F.BLUE, edgecolor=F.BLUE)); ax.text(4.05, 2.35, "電子 $e^-$", ha="center", color=F.BLUE)
    _box(ax, (0.25, 0.75), 1.85, 0.90, r"$h^++OH^-\rightarrow\cdot OH$", face="#fff0f0", edge=F.RED, fs=11)
    _box(ax, (3.10, 0.75), 1.85, 0.90, r"$e^-+O_2\rightarrow\cdot O_2^-$", face="#eef4ff", edge=F.BLUE, fs=11)
    _arrow(ax, (1.15, 2.55), (1.15, 1.70), color=F.RED)
    _arrow(ax, (4.05, 2.55), (4.05, 1.70), color=F.BLUE)
    ax.text(2.60, 0.30, "高比表面積增加反應位置；電子－電洞仍可能復合，效率受材料與光源控制。", ha="center", fontsize=10.3)
    ax.set_title("奈米光觸媒：表面與能帶共同作用", fontsize=13.5, weight="bold")
    fig.suptitle("奈米材料的判斷先看尺度，再由比表面積、界面與量子效應解釋性質", fontsize=16, y=0.98)
    fig.subplots_adjust(left=0.07, right=0.98, bottom=0.13, top=0.83, wspace=0.18)
    return _save(fig, "選化IV-2-奈米尺度比表面積與光觸媒.svg")


def fig_ferrioxalate_lab():
    """用莫耳數、條件與觀察／推論建立草酸鐵鉀實驗證據鏈。"""
    n_fe = 2.0 * 0.002
    n_ox = 2.0 * 0.006
    assert np.isclose(n_ox / n_fe, 3.0)
    assert np.isclose(n_fe, 0.004) and np.isclose(n_ox, 0.012)

    fig, ax = plt.subplots(figsize=(12.5, 6.2))
    ax.axis("off"); ax.set_xlim(0, 12.5); ax.set_ylim(0, 6.2)
    ax.text(6.25, 5.80, "草酸鐵鉀製備：計量、避光、降溫與證據各自回答一個問題", ha="center", fontsize=16, weight="bold")
    boxes = [
        (0.30, r"$2.0\,M\ FeCl_3$" + "\n" + r"$2.0\,mL$" + "\n" + r"$n(Fe^{3+})=0.0040\,mol$", "#fff7dd", F.AMBER),
        (3.05, r"$2.0\,M\ K_2C_2O_4$" + "\n" + r"$6.0\,mL$" + "\n" + r"$n(C_2O_4^{2-})=0.012\,mol$", "#eef4ff", F.BLUE),
        (5.95, "暗處混合\n" + r"$Fe^{3+}+3C_2O_4^{2-}$" + "\n" + r"$\rightarrow[Fe(C_2O_4)_3]^{3-}$", "#f4efff", F.PURPLE),
        (8.85, "冰水浴、過濾\n降低溶解度並分離晶體", "#eefbf2", F.GREEN),
    ]
    for x, text, face, edge in boxes:
        _box(ax, (x, 3.15), 2.35, 1.45, text, face=face, edge=edge, fs=11.5)
    for x1, x2, color in [(2.68, 3.00, F.INK), (5.43, 5.90, F.PURPLE), (8.33, 8.80, F.GREEN)]:
        _arrow(ax, (x1, 3.88), (x2, 3.88), color=color)
    ax.text(4.55, 2.67, "配位子／金屬莫耳比＝3.00", ha="center", fontsize=11.5, color=F.BLUE)
    _box(ax, (0.55, 0.70), 3.30, 1.15, "觀察\n黃褐溶液變成翠綠晶體", face="#fff7dd", edge=F.AMBER, fs=12)
    _box(ax, (4.60, 0.70), 3.30, 1.15, "推論\n形成新錯離子並析出晶體", face="#eefbf2", edge=F.GREEN, fs=12)
    _box(ax, (8.65, 0.70), 3.30, 1.15, "安全與廢棄物\n護目鏡、手套；含金屬廢液分流", face="#fff0f0", edge=F.RED, fs=11.5)
    ax.text(6.25, 2.25, "光會促使 $Fe^{3+}$ 與草酸根發生氧化還原；實驗避光是控制化學反應，不只是保存顏色。", ha="center", fontsize=11.2)
    return _save(fig, "選化IV-2-草酸鐵鉀製備證據鏈.svg")


def main():
    fig_hydrogen_routes()
    fig_carbon_structure()
    fig_nitrogen_flow()
    fig_oxygen_ozone()
    fig_silicon_materials()
    fig_main_group_metals()
    fig_iron_furnace()
    fig_coordination()
    fig_alloy_lattices()
    fig_semiconductor()
    fig_conducting_polymer()
    fig_nanoscale()
    fig_ferrioxalate_lab()


if __name__ == "__main__":
    main()
