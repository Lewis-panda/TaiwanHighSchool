# -*- coding: utf-8 -*-
"""產生「必化-2 化學式與化學計量」學生講義的章內 SVG。

重繪：.venv/bin/python _tools/fig_content_必化-2.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, FancyBboxPatch, Polygon, Rectangle

import figlib as F


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CH = os.path.join(ROOT, "content", "必修化學", "必化-2")


FIGURE_OUTPUTS = (
    ("fig_formula_layers", "必化-2-化學式資訊層次.svg"),
    ("fig_combustion_analysis", "必化-2-燃燒分析證據流.svg"),
    ("fig_balancing_ledger", "必化-2-反應式配平守恆帳.svg"),
    ("fig_stoichiometry_bridge", "必化-2-化學計量莫耳橋.svg"),
    ("fig_limiting_particles", "必化-2-限量試劑粒子模型.svg"),
    ("fig_gas_collection", "必化-2-產氣計量量測.svg"),
    ("fig_enthalpy_calorimetry", "必化-2-反應能量與量熱.svg"),
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


def _atom(ax, x, y, label, color, radius=0.16):
    patch = Circle((x, y), radius, facecolor=color, edgecolor="white", lw=1.0, zorder=5)
    ax.add_patch(patch)
    ax.text(x, y, label, ha="center", va="center", color="white", fontsize=8.5, weight="bold", zorder=6)
    return patch


def _bond(ax, p1, p2, color=F.INK, lw=2.0):
    ax.plot([p1[0], p2[0]], [p1[1], p2[1]], color=color, lw=lw, zorder=2)


def fig_formula_layers():
    """用同一組成的兩種連接方式，區分實驗式、分子式與示性式。"""
    fig, ax = F.schematic(11.7, 5.9)
    ax.set_xlim(-5.85, 5.85)
    ax.set_ylim(-3.0, 3.0)

    _box(ax, (-5.42, 1.50), 2.45, 0.94, "實驗式 $CH_3O$\n最簡整數比 1:3:1", face="#fff7dd", edge=F.AMBER, fs=12.5)
    _box(ax, (-1.23, 1.50), 2.46, 0.94, "分子式 $C_2H_6O_2$\n實際原子數 2:6:2", face="#eef4ff", edge=F.BLUE, fs=12.5)
    _box(ax, (2.95, 1.50), 2.47, 0.94, "示性式／縮寫結構\n保留關鍵連接資訊", face="#e9f8ef", edge=F.GREEN, fs=12.3)
    F.arrow(ax, (-2.88, 1.97), (-1.35, 1.97), color=F.BLUE, lw=2.0, mutation=15)
    F.arrow(ax, (1.35, 1.97), (2.82, 1.97), color=F.GREEN, lw=2.0, mutation=15)
    ax.text(-2.11, 2.22, "$\\times 2$", ha="center", color=F.BLUE, fontsize=12)
    ax.text(2.10, 2.22, "加入連接方式", ha="center", color=F.GREEN, fontsize=11.5)

    # Two constitutional isomers, both C2H6O2.
    structures = [
        (-2.55, "HO–CH$_2$–CH$_2$–OH", "乙二醇：兩端各一個 –OH"),
        (2.45, "CH$_3$–O–O–CH$_3$", "過氧化物：含 O–O 連接"),
    ]
    for x0, formula, caption in structures:
        y = -0.18
        atoms = [
            (x0 - 1.00, y, "C", F.BLUE),
            (x0, y, "C", F.BLUE),
            (x0 - 1.58, y, "O", F.RED),
            (x0 + 0.58, y, "O", F.RED),
        ] if x0 < 0 else [
            (x0 - 1.20, y, "C", F.BLUE),
            (x0 - 0.38, y, "O", F.RED),
            (x0 + 0.38, y, "O", F.RED),
            (x0 + 1.20, y, "C", F.BLUE),
        ]
        ordered = sorted(atoms, key=lambda item: item[0])
        for left, right in zip(ordered[:-1], ordered[1:]):
            _bond(ax, (left[0], left[1]), (right[0], right[1]))
        for x, yy, label, color in atoms:
            _atom(ax, x, yy, label, color)
        ax.text(x0, -0.75, formula, ha="center", fontsize=13, weight="bold")
        ax.text(x0, -1.20, caption, ha="center", fontsize=10.7, color="#475569")

    atom_counts = {"left": {"C": 2, "H": 6, "O": 2}, "right": {"C": 2, "H": 6, "O": 2}}
    assert atom_counts["left"] == atom_counts["right"]
    _box(ax, (-4.72, -2.35), 9.44, 0.63, "同一分子式可以有不同連接方式；連接方式改變，官能基與性質也可能改變。", face="#f1ecff", edge=F.PURPLE, fs=11.5)
    fig.suptitle("化學式回答的問題不同：比例、原子數、連接方式", fontsize=16, y=0.98)
    fig.subplots_adjust(left=0.025, right=0.975, top=0.89, bottom=0.04)
    return _save(fig, "必化-2-化學式資訊層次.svg")


def fig_combustion_analysis():
    """畫出 CHO 化合物燃燒分析的選擇性吸收與質量推論。"""
    fig, ax = F.schematic(12.0, 5.8)
    ax.set_xlim(-6.0, 6.0)
    ax.set_ylim(-2.9, 2.9)

    _box(ax, (-5.55, 0.65), 2.35, 1.15, "含 C、H、O 的樣品\n已知樣品質量 $m_s$\n完全燃燒", face="#fff7dd", edge=F.AMBER, fs=12)
    _box(ax, (-2.35, 0.65), 2.55, 1.15, "第一吸收管\n只量測生成的 $H_2O$\n增重 $m_w$", face="#eef4ff", edge=F.BLUE, fs=12)
    _box(ax, (0.95, 0.65), 2.55, 1.15, "第二吸收管\n量測生成的 $CO_2$\n增重 $m_c$", face="#e9f8ef", edge=F.GREEN, fs=12)
    _box(ax, (4.10, 0.65), 1.45, 1.15, "乾燥尾氣\n確認吸收完整", face="#f8fafc", edge="#64748b", fs=11.3)
    F.arrow(ax, (-3.12, 1.22), (-2.47, 1.22), color=F.RED, lw=2.2, mutation=15)
    F.arrow(ax, (0.32, 1.22), (0.83, 1.22), color=F.BLUE, lw=2.2, mutation=15)
    F.arrow(ax, (3.62, 1.22), (3.98, 1.22), color=F.GREEN, lw=2.2, mutation=15)
    ax.text(-2.80, 1.58, "$H_2O+CO_2$", ha="center", color=F.RED, fontsize=11.2)
    ax.text(0.56, 1.58, "去除 $H_2O$", ha="center", color=F.BLUE, fontsize=10.8)
    ax.text(3.80, 1.58, "去除 $CO_2$", ha="center", color=F.GREEN, fontsize=10.8)

    _box(ax, (-5.35, -1.18), 3.15, 0.77, "$n(H)=2\\,m_w/18$\n$m(H)=m_w\\times 2/18$", face="#eef4ff", edge=F.BLUE, fs=12)
    _box(ax, (-1.58, -1.18), 3.15, 0.77, "$n(C)=m_c/44$\n$m(C)=m_c\\times 12/44$", face="#e9f8ef", edge=F.GREEN, fs=12)
    _box(ax, (2.22, -1.18), 3.15, 0.77, "若樣品只含 C、H、O：\n$m(O)=m_s-m(C)-m(H)$", face="#fff1e6", edge=F.AMBER, fs=11.8)
    F.arrow(ax, (-1.08, 0.53), (-3.77, -0.30), color=F.BLUE, lw=1.6, mutation=13)
    F.arrow(ax, (2.22, 0.53), (0.0, -0.30), color=F.GREEN, lw=1.6, mutation=13)
    ax.text(0, -2.15, "前提：完全燃燒、吸收劑具選擇性、系統無漏氣；吸收順序使後一管不把水也算進二氧化碳。", ha="center", fontsize=10.9, color="#475569")
    fig.suptitle("燃燒分析把『增重』轉成碳、氫、氧的莫耳數", fontsize=16, y=0.98)
    fig.subplots_adjust(left=0.025, right=0.975, top=0.89, bottom=0.05)
    return _save(fig, "必化-2-燃燒分析證據流.svg")


def fig_balancing_ledger():
    """以配平後的乙烷燃燒展示原子與電荷守恆。"""
    fig, axes = plt.subplots(1, 2, figsize=(11.8, 5.5), gridspec_kw={"width_ratios": [1.12, 1.0]})
    ax, table_ax = axes
    for a in axes:
        a.axis("off")

    ax.set_xlim(-3.2, 3.2)
    ax.set_ylim(-2.6, 2.6)
    _box(ax, (-2.80, 1.45), 5.60, 0.72, "$C_2H_6 + O_2 \\rightarrow CO_2 + H_2O$", face="#fff7dd", edge=F.AMBER, fs=14)
    steps = [
        (0.55, "① 先平衡 C：右側放 $2CO_2$", F.BLUE),
        (-0.15, "② 再平衡 H：右側放 $3H_2O$", F.GREEN),
        (-0.85, "③ 右側共有 7 個 O：左側放 $\\frac{7}{2}O_2$", F.PURPLE),
        (-1.55, "④ 全式乘 2，化為最簡整數係數", F.RED),
    ]
    for y, text, color in steps:
        ax.text(-2.70, y, text, ha="left", va="center", fontsize=11.4, color=color)
    _box(ax, (-2.88, -2.38), 5.76, 0.58, "$2C_2H_6 + 7O_2 \\rightarrow 4CO_2 + 6H_2O$", face="#e9f8ef", edge=F.GREEN, fs=14)

    table_ax.set_xlim(0, 1)
    table_ax.set_ylim(0, 1)
    table_ax.text(0.5, 0.92, "守恆帳", ha="center", fontsize=14, weight="bold")
    columns = [0.10, 0.38, 0.66, 0.90]
    headers = ["元素", "反應物側", "產物側", "差"]
    rows = [("C", 4, 4), ("H", 12, 12), ("O", 14, 14), ("總電荷", 0, 0)]
    for x, header in zip(columns, headers):
        table_ax.text(x, 0.80, header, ha="center", fontsize=11.5, weight="bold")
    for i, (symbol, left, right) in enumerate(rows):
        y = 0.66 - i * 0.14
        values = [symbol, str(left), str(right), str(left - right)]
        for x, value in zip(columns, values):
            table_ax.text(x, y, value, ha="center", fontsize=11.8, color=F.GREEN if value == "0" else F.INK)
        table_ax.plot([0.04, 0.96], [y - 0.065, y - 0.065], color="#d8dde3", lw=0.9)
    counts_left = {"C": 2 * 2, "H": 2 * 6, "O": 7 * 2}
    counts_right = {"C": 4, "H": 6 * 2, "O": 4 * 2 + 6}
    assert counts_left == counts_right == {"C": 4, "H": 12, "O": 14}
    table_ax.text(0.5, 0.12, "係數改變整份物質的數量；\n下標仍描述每一份物質的組成。", ha="center", fontsize=11.1, color="#475569")
    fig.suptitle("配平是在找同時滿足原子數與總電荷守恆的係數", fontsize=16, y=0.98)
    fig.subplots_adjust(left=0.035, right=0.97, top=0.87, bottom=0.06, wspace=0.12)
    return _save(fig, "必化-2-反應式配平守恆帳.svg")


def fig_stoichiometry_bridge():
    """把質量、粒子數、溶液與氣體資料統一轉成莫耳。"""
    fig, ax = F.schematic(12.0, 5.8)
    ax.set_xlim(-6.0, 6.0)
    ax.set_ylim(-2.9, 2.9)

    left_entries = [
        (-5.55, 1.55, "質量 $m$", "$n=m/M$", F.BLUE),
        (-5.55, 0.35, "粒子數 $N$", "$n=N/N_A$", F.GREEN),
        (-5.55, -0.85, "溶液 $C,V$", "$n=CV$（$V$ 用 L）", F.PURPLE),
        (-5.55, -2.05, "氣體 $P,V,T$", "$n=PV/RT$", F.AMBER),
    ]
    for x, y, label, formula, color in left_entries:
        _box(ax, (x, y), 2.35, 0.72, f"{label}\n{formula}", face="#f8fafc", edge=color, fs=11.3)
        F.arrow(ax, (x + 2.35, y + 0.36), (-1.40, 0.36), color=color, lw=1.6, mutation=13)

    _box(ax, (-1.28, -0.30), 2.56, 1.32, "已知物質\n莫耳數 $n_A$", face="#fff7dd", edge=F.AMBER, fs=14)
    _box(ax, (2.15, -0.30), 2.56, 1.32, "目標物質\n莫耳數 $n_B$", face="#e9f8ef", edge=F.GREEN, fs=14)
    F.arrow(ax, (1.42, 0.36), (2.00, 0.36), color=F.RED, lw=2.8, mutation=17)
    ax.text(1.72, 0.76, "$n_B=n_A\\,\\dfrac{\\nu_B}{\\nu_A}$", ha="center", fontsize=13.5, color=F.RED)
    ax.text(1.72, -0.64, "只在中間使用\n平衡係數比", ha="center", fontsize=10.8, color="#475569")

    _box(ax, (2.15, -2.12), 3.15, 0.72, "再換回題目要求的\n質量、粒子數、濃度或體積", face="#eef4ff", edge=F.BLUE, fs=11.5)
    F.arrow(ax, (3.43, -0.43), (3.43, -1.28), color=F.BLUE, lw=2.0, mutation=15)
    ax.text(0, 2.52, "例：$2Al+3Cl_2\\rightarrow2AlCl_3$，故 $n(AlCl_3)=n(Al)\\times2/2$", ha="center", fontsize=11.8)
    fig.suptitle("化學計量的共同語言是莫耳；係數比只連接莫耳數", fontsize=16, y=0.98)
    fig.subplots_adjust(left=0.025, right=0.975, top=0.87, bottom=0.04)
    return _save(fig, "必化-2-化學計量莫耳橋.svg")


def fig_limiting_particles():
    """以 5 個 H2 與 2 個 O2 展示限量試劑與剩餘量。"""
    fig, axes = plt.subplots(1, 2, figsize=(11.7, 5.3))
    for ax in axes:
        ax.set_aspect("equal")
        ax.axis("off")
        ax.set_xlim(-3.2, 3.2)
        ax.set_ylim(-2.5, 2.5)

    ax = axes[0]
    h2_centers = [(-2.2, 1.2), (-0.9, 1.2), (0.4, 1.2), (1.7, 1.2), (-1.55, -0.2)]
    o2_centers = [(0.15, -0.25), (1.55, -0.25)]
    for x, y in h2_centers:
        _bond(ax, (x - 0.15, y), (x + 0.15, y), color=F.BLUE, lw=2.3)
        _atom(ax, x - 0.15, y, "H", F.BLUE, 0.13)
        _atom(ax, x + 0.15, y, "H", F.BLUE, 0.13)
    for x, y in o2_centers:
        _bond(ax, (x - 0.17, y), (x + 0.17, y), color=F.RED, lw=2.6)
        _atom(ax, x - 0.17, y, "O", F.RED, 0.15)
        _atom(ax, x + 0.17, y, "O", F.RED, 0.15)
    ax.text(0, -1.15, "$n(H_2)/2=5/2=2.5$\n$n(O_2)/1=2$", ha="center", fontsize=12.2)
    ax.text(0, -2.0, "$O_2$ 的比值較小，反應進度最多為 2", ha="center", fontsize=11.2, color=F.RED)
    ax.set_title("反應前：$5H_2+2O_2$", fontsize=14)

    ax = axes[1]
    product_centers = [(-2.0, 0.85), (-0.65, 0.85), (0.70, 0.85), (2.05, 0.85)]
    for x, y in product_centers:
        _bond(ax, (x - 0.30, y + 0.15), (x, y), color=F.INK, lw=1.7)
        _bond(ax, (x, y), (x + 0.30, y + 0.15), color=F.INK, lw=1.7)
        _atom(ax, x, y, "O", F.RED, 0.16)
        _atom(ax, x - 0.30, y + 0.15, "H", F.BLUE, 0.12)
        _atom(ax, x + 0.30, y + 0.15, "H", F.BLUE, 0.12)
    x, y = 0, -0.45
    _bond(ax, (x - 0.15, y), (x + 0.15, y), color=F.BLUE, lw=2.3)
    _atom(ax, x - 0.15, y, "H", F.BLUE, 0.13)
    _atom(ax, x + 0.15, y, "H", F.BLUE, 0.13)
    ax.text(0, -1.15, "生成 $4H_2O$；剩餘 $1H_2$", ha="center", fontsize=12.2)
    ax.text(0, -1.78, "反應式：$2H_2+O_2\\rightarrow2H_2O$", ha="center", fontsize=11.5, color="#475569")
    ax.set_title("反應後：限量試劑耗盡", fontsize=14)

    initial = {"H": 5 * 2, "O": 2 * 2}
    final = {"H": 4 * 2 + 1 * 2, "O": 4}
    assert initial == final == {"H": 10, "O": 4}
    fig.suptitle("限量試劑決定最大反應進度；剩餘量由守恆算回", fontsize=16, y=0.98)
    fig.subplots_adjust(left=0.03, right=0.98, top=0.84, bottom=0.06, wspace=0.10)
    return _save(fig, "必化-2-限量試劑粒子模型.svg")


def fig_gas_collection():
    """畫出鎂與稀鹽酸產氫的安全小量量測與資料修正。"""
    fig, ax = F.schematic(11.7, 5.8)
    ax.set_xlim(-5.85, 5.85)
    ax.set_ylim(-2.9, 2.9)

    # Reaction flask and vented delivery line.
    ax.add_patch(Circle((-3.75, -0.35), 0.82, facecolor="#eef4ff", edgecolor=F.INK, lw=1.8))
    ax.add_patch(Rectangle((-4.05, 0.25), 0.60, 0.83, facecolor="white", edgecolor=F.INK, lw=1.6))
    ax.plot([-3.75, -3.75, -1.15], [1.08, 1.55, 1.55], color=F.INK, lw=2.0)
    ax.plot([-1.15, -1.15], [1.55, 0.75], color=F.INK, lw=2.0)
    ax.text(-3.75, -0.20, "$Mg+2HCl$\n$\\rightarrow MgCl_2+H_2$", ha="center", va="center", fontsize=10.8)
    for x, y in [(-4.05, -0.70), (-3.65, -0.60), (-3.90, -0.25)]:
        ax.add_patch(Circle((x, y), 0.055, facecolor=F.BLUE, edgecolor="none"))

    # Gas syringe.
    ax.add_patch(Rectangle((-1.70, -0.35), 4.55, 1.10, facecolor="#f8fafc", edgecolor=F.INK, lw=1.8))
    ax.add_patch(Rectangle((1.75, -0.30), 0.16, 1.00, facecolor="#cbd5e1", edgecolor="#64748b", lw=1.0))
    ax.plot([1.91, 4.15], [0.20, 0.20], color=F.INK, lw=2.2)
    ax.add_patch(Rectangle((4.15, -0.15), 0.18, 0.70, facecolor="#cbd5e1", edgecolor=F.INK, lw=1.3))
    for i in range(9):
        x = -1.35 + i * 0.38
        ax.plot([x, x], [0.75, 0.58 if i % 2 else 0.50], color="#64748b", lw=0.9)
    F.arrow(ax, (-0.95, 0.20), (1.45, 0.20), color=F.BLUE, lw=2.2, mutation=15)
    ax.text(0.25, -0.02, "$H_2$ 推動活塞", ha="center", fontsize=11, color=F.BLUE)
    ax.text(0.45, -0.82, "待氣泡停止且裝置回到室溫，再讀取氣體體積", ha="center", fontsize=11.2)

    _box(ax, (-5.35, -2.35), 3.15, 0.72, "觀察：鎂逐漸變小、產生氣泡、\n氣體體積上升後達平臺", face="#fff7dd", edge=F.AMBER, fs=10.8)
    _box(ax, (-1.65, -2.35), 3.15, 0.72, "推論：反應進行並產氣；\n氣體身分需另有證據", face="#e9f8ef", edge=F.GREEN, fs=10.8)
    _box(ax, (2.05, -2.35), 3.15, 0.72, "修正：扣除死體積，記錄 $T,P$；\n量具解析度與漏氣會影響結果", face="#f1ecff", edge=F.PURPLE, fs=10.6)
    ax.text(0, 2.42, "護目鏡、實驗衣、耐酸手套；遠離火焰與火花；保持導氣路徑通暢。", ha="center", fontsize=11.5, color=F.RED)
    fig.suptitle("產氣反應把化學計量連到可量測的氣體體積", fontsize=16, y=0.98)
    fig.subplots_adjust(left=0.025, right=0.975, top=0.87, bottom=0.05)
    return _save(fig, "必化-2-產氣計量量測.svg")


def fig_enthalpy_calorimetry():
    """並列放熱／吸熱能階與量熱器的能量帳。"""
    fig, axes = plt.subplots(1, 2, figsize=(11.8, 5.6), gridspec_kw={"width_ratios": [1.2, 1.0]})

    ax = axes[0]
    x = np.array([0.8, 3.0, 4.8])
    exo = np.array([4.0, 4.0, 1.6])
    endo = np.array([0.8, 0.8, 3.2])
    ax.plot(x[:2], exo[:2], color=F.RED, lw=3)
    ax.plot(x[1:], exo[1:], color=F.RED, lw=3)
    ax.plot(x[:2], endo[:2], color=F.BLUE, lw=3)
    ax.plot(x[1:], endo[1:], color=F.BLUE, lw=3)
    ax.text(1.65, 4.20, "反應物", ha="center", color=F.RED, fontsize=11)
    ax.text(4.15, 1.25, "產物", ha="center", color=F.RED, fontsize=11)
    ax.text(1.65, 0.45, "反應物", ha="center", color=F.BLUE, fontsize=11)
    ax.text(4.15, 3.45, "產物", ha="center", color=F.BLUE, fontsize=11)
    F.arrow(ax, (3.70, 3.85), (3.70, 1.75), color=F.RED, lw=2.1, mutation=14)
    F.arrow(ax, (3.15, 1.05), (3.15, 2.95), color=F.BLUE, lw=2.1, mutation=14)
    ax.text(3.88, 2.80, "$\\Delta H<0$\n放熱", ha="left", va="center", color=F.RED, fontsize=11.5)
    ax.text(2.95, 2.00, "$\\Delta H>0$\n吸熱", ha="right", va="center", color=F.BLUE, fontsize=11.5)
    assert exo[-1] - exo[0] < 0 and endo[-1] - endo[0] > 0
    ax.set_xlim(0.3, 5.2)
    ax.set_ylim(0.0, 4.8)
    ax.set_ylabel("系統焓 $H$")
    ax.set_xticks([])
    F.clean_grid(ax)
    ax.set_title("反應前後的焓差", fontsize=14)

    ax = axes[1]
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_xlim(-2.6, 2.6)
    ax.set_ylim(-2.5, 2.5)
    ax.add_patch(Rectangle((-1.45, -1.05), 2.9, 2.15, facecolor="#eef4ff", edgecolor=F.BLUE, lw=1.8))
    ax.add_patch(Circle((0, 0.05), 0.48, facecolor="#fff7dd", edgecolor=F.AMBER, lw=1.8))
    ax.text(0, 0.05, "反應\n系統", ha="center", va="center", fontsize=11.5)
    ax.text(0, 0.82, "水＋量熱器（環境）", ha="center", fontsize=11.2, color=F.BLUE)
    F.arrow(ax, (0.52, 0.05), (1.25, 0.05), color=F.RED, lw=2.4, mutation=16)
    ax.text(0.92, 0.36, "放熱時", ha="center", color=F.RED, fontsize=10.8)
    F.arrow(ax, (-1.25, -0.35), (-0.52, -0.10), color=F.BLUE, lw=2.4, mutation=16)
    ax.text(-1.00, -0.67, "吸熱時", ha="center", color=F.BLUE, fontsize=10.8)
    _box(ax, (-2.25, -2.05), 4.50, 0.62, "$q_{rxn}+q_{water}+q_{cal}=0$\n$q_{water}=mc\\Delta T$", face="#f8fafc", edge="#64748b", fs=12)
    ax.text(0, 1.70, "測得 $\\Delta T$，先算環境吸收／放出的熱，\n再用能量守恆回推反應熱。", ha="center", fontsize=11.2)
    ax.set_title("量熱器的能量帳", fontsize=14)

    fig.suptitle("$\\Delta H$ 描述系統能量改變；溫度變化是環境端的量測", fontsize=16, y=0.98)
    fig.subplots_adjust(left=0.055, right=0.98, top=0.86, bottom=0.08, wspace=0.20)
    return _save(fig, "必化-2-反應能量與量熱.svg")


def main():
    for entrypoint, filename in FIGURE_OUTPUTS:
        function = globals().get(entrypoint)
        if not callable(function):
            raise RuntimeError(f"找不到繪圖函式：{entrypoint}")
        output = function()
        if os.path.basename(output) != filename:
            raise RuntimeError(f"輸出不一致：{entrypoint} -> {output}，預期 {filename}")


if __name__ == "__main__":
    main()
