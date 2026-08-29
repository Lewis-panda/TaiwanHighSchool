# -*- coding: utf-8 -*-
"""產生「選化 III-1 化學平衡」學生講義章內 SVG。

重繪：.venv/bin/python _tools/fig_content_選化III-1.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, FancyBboxPatch, Rectangle

import figlib as F


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CH = os.path.join(ROOT, "content", "選修化學III", "選化III-1")


FIGURE_OUTPUTS = (
    ("fig_dynamic_equilibrium", "選化III-1-動態平衡濃度與速率.svg"),
    ("fig_q_direction", "選化III-1-反應商判斷方向.svg"),
    ("fig_k_transformations", "選化III-1-反應式與平衡常數.svg"),
    ("fig_ice_extent", "選化III-1-ICE與反應進度.svg"),
    ("fig_heterogeneous", "選化III-1-異相平衡與活性.svg"),
    ("fig_concentration_step", "選化III-1-濃度擾動的瞬間與鬆弛.svg"),
    ("fig_pressure_no2", "選化III-1-壓縮NO2-N2O4平衡.svg"),
    ("fig_temperature_k", "選化III-1-溫度改變平衡常數.svg"),
    ("fig_catalyst_energy", "選化III-1-催化劑與平衡.svg"),
    ("fig_haber_tradeoff", "選化III-1-合成氨條件權衡.svg"),
    ("fig_ksp_stoichiometry", "選化III-1-溶度積與莫耳溶解度.svg"),
    ("fig_common_ion", "選化III-1-同離子與AgCl溶解度.svg"),
    ("fig_precipitation_window", "選化III-1-離子積與選擇沉澱.svg"),
    ("fig_fescn_experiment", "選化III-1-FeSCN平衡常數實驗.svg"),
)


def _save(fig, filename):
    assert filename.endswith(".svg")
    return F.save_to(fig, CH, filename[:-4], output_subdir="assets", write_pdf=False)


def _box(ax, xy, width, height, text, *, face="#f8fafc", edge="#64748b", fs=10.5, lw=1.4):
    patch = FancyBboxPatch(
        xy,
        width,
        height,
        boxstyle="round,pad=0.035,rounding_size=0.06",
        facecolor=face,
        edgecolor=edge,
        lw=lw,
    )
    ax.add_patch(patch)
    ax.text(xy[0] + width / 2, xy[1] + height / 2, text, ha="center", va="center", fontsize=fs)
    return patch


def _molecule(ax, xy, kind, scale=1.0):
    x, y = xy
    if kind == "NO2":
        ax.add_patch(Circle((x, y), 0.12 * scale, facecolor="#c2410c", edgecolor="#7c2d12", lw=1.0))
        ax.text(x, y, r"$NO_2$", ha="center", va="center", fontsize=6.5 * scale, color="white")
    elif kind == "N2O4":
        ax.add_patch(FancyBboxPatch((x - 0.19 * scale, y - 0.09 * scale), 0.38 * scale, 0.18 * scale,
                                    boxstyle="round,pad=0.02", facecolor="#f1f5f9", edgecolor="#64748b"))
        ax.text(x, y, r"$N_2O_4$", ha="center", va="center", fontsize=6.2 * scale)


def fig_dynamic_equilibrium():
    """以可逆一級反應的解析解驗證濃度固定與正逆速率相等。"""
    kf, kr, total = 0.80, 0.40, 1.00
    a0 = 0.90
    aeq = kr * total / (kf + kr)
    beq = total - aeq
    t = np.linspace(0, 8, 500)
    a = aeq + (a0 - aeq) * np.exp(-(kf + kr) * t)
    b = total - a
    vf, vr = kf * a, kr * b
    assert np.allclose(a + b, total)
    assert abs(kf * aeq - kr * beq) < 1e-12
    assert abs(a[-1] - aeq) < 1e-4

    fig, axes = plt.subplots(1, 2, figsize=(12.2, 5.2))
    ax = axes[0]
    ax.plot(t, a, color=F.BLUE, lw=2.5, label="[A]")
    ax.plot(t, b, color=F.RED, lw=2.5, label="[B]")
    ax.axhline(aeq, color=F.BLUE, ls="--", alpha=0.45)
    ax.axhline(beq, color=F.RED, ls="--", alpha=0.45)
    ax.text(7.85, aeq + 0.025, f"{aeq:.3f} M", ha="right", color=F.BLUE, fontsize=9.5)
    ax.text(7.85, beq + 0.025, f"{beq:.3f} M", ha="right", color=F.RED, fontsize=9.5)
    ax.set(xlabel="時間", ylabel="濃度 / M", ylim=(0, 1.02), title="巨觀：各物種濃度趨於固定")
    F.clean_grid(ax)
    ax.legend(frameon=False)

    ax = axes[1]
    ax.plot(t, vf, color=F.GREEN, lw=2.5, label=r"正反應速率 $k_f[A]$")
    ax.plot(t, vr, color=F.PURPLE, lw=2.5, label=r"逆反應速率 $k_r[B]$")
    rateeq = kf * aeq
    ax.scatter([t[-1], t[-1]], [vf[-1], vr[-1]], color=[F.GREEN, F.PURPLE], zorder=5)
    ax.axhline(rateeq, color=F.INK, ls="--", alpha=0.45)
    ax.text(7.85, rateeq + 0.025, f"共同速率 {rateeq:.3f} M/s", ha="right", fontsize=9.5)
    ax.set(xlabel="時間", ylabel="反應速率 / (M s$^{-1}$)", ylim=(0, 0.78), title="微觀：正、逆反應仍持續且速率相等")
    F.clean_grid(ax)
    ax.legend(frameon=False)
    fig.suptitle(r"封閉、定溫系統中的動態平衡：$A\rightleftharpoons B$", fontsize=16, y=0.99)
    fig.subplots_adjust(left=0.07, right=0.985, bottom=0.14, top=0.82, wspace=0.23)
    return _save(fig, "選化III-1-動態平衡濃度與速率.svg")


def fig_q_direction():
    """用 A⇌B、K=4 的三個狀態驗證 Q/K 與淨反應方向。"""
    K = 4.0
    states = [(0.80, 0.20), (0.20, 0.80), (0.10, 0.90)]
    qs = np.array([b / a for a, b in states])
    assert qs[0] < K and np.isclose(qs[1], K) and qs[2] > K

    fig, axes = plt.subplots(1, 3, figsize=(12.6, 4.8))
    labels = ["Q < K\n淨反應向右", "Q = K\n已達平衡", "Q > K\n淨反應向左"]
    colors = [F.BLUE, F.GREEN, F.RED]
    arrows = [(0.18, 0.82), None, (0.82, 0.18)]
    for ax, (a, b), q, label, color, arrow in zip(axes, states, qs, labels, colors, arrows):
        ax.axis("off")
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.add_patch(Rectangle((0.08, 0.30), 0.84, 0.46, facecolor="#f8fafc", edgecolor="#64748b", lw=1.5))
        ax.text(0.28, 0.55, f"A\n{a:.2f} M", ha="center", va="center", fontsize=12, color=F.BLUE)
        ax.text(0.72, 0.55, f"B\n{b:.2f} M", ha="center", va="center", fontsize=12, color=F.RED)
        if arrow is not None:
            F.arrow(ax, (arrow[0] + (0.17 if arrow[0] < arrow[1] else -0.17), 0.42),
                    (arrow[1] + (-0.17 if arrow[0] < arrow[1] else 0.17), 0.42), color=color, lw=2.4)
        else:
            ax.text(0.5, 0.42, r"$v_f=v_r$", ha="center", fontsize=11, color=F.GREEN)
        ax.text(0.5, 0.86, label, ha="center", va="center", fontsize=13, weight="bold", color=color)
        ax.text(0.5, 0.17, rf"$Q=[B]/[A]={q:.2f}$", ha="center", fontsize=11.5)
    fig.suptitle(r"同溫下比較 $Q$ 與 $K=4.00$，直接判斷降低 $Q-K$ 的淨反應方向", fontsize=15.5, y=0.98)
    fig.subplots_adjust(left=0.02, right=0.99, bottom=0.04, top=0.82, wspace=0.05)
    return _save(fig, "選化III-1-反應商判斷方向.svg")


def fig_k_transformations():
    """驗證反應反向、倍乘與相加時 K 的代數轉換。"""
    K1, K2 = 9.0, 2.0
    values = {"原式": K1, "反向": 1 / K1, "係數乘 1/2": np.sqrt(K1), "與第二式相加": K1 * K2}
    assert np.isclose(values["反向"], 1 / 9)
    assert np.isclose(values["係數乘 1/2"], 3)
    assert np.isclose(values["與第二式相加"], 18)

    fig, ax = plt.subplots(figsize=(11.8, 5.6))
    ax.axis("off")
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 6)
    _box(ax, (0.35, 2.25), 2.55, 1.45, r"$A\rightleftharpoons B$" + "\n" + r"$K_1=9$", face="#eef4ff", edge=F.BLUE, fs=13)
    targets = [
        ((4.15, 4.25), r"$B\rightleftharpoons A$" + "\n" + r"$K=1/K_1=1/9$", F.RED),
        ((4.15, 2.25), r"$\frac{1}{2}A\rightleftharpoons\frac{1}{2}B$" + "\n" + r"$K=K_1^{1/2}=3$", F.PURPLE),
        ((8.25, 0.35), r"$A+C\rightleftharpoons B+D$" + "\n" + r"$K=K_1K_2=18$", F.GREEN),
    ]
    for (x, y), text, color in targets:
        _box(ax, (x, y), 3.35, 1.35, text, face="#f8fafc", edge=color, fs=11.2)
    F.arrow(ax, (2.9, 3.15), (4.15, 4.65), color=F.RED, lw=1.9)
    ax.text(3.35, 4.18, "反向", color=F.RED, fontsize=10)
    F.arrow(ax, (2.9, 2.85), (4.15, 2.85), color=F.PURPLE, lw=1.9)
    ax.text(3.30, 3.06, "係數乘 n", color=F.PURPLE, fontsize=10)
    _box(ax, (4.15, 0.35), 3.35, 1.35, r"$C\rightleftharpoons D$" + "\n" + r"$K_2=2$", face="#fff7dd", edge=F.AMBER, fs=11.2)
    F.arrow(ax, (7.50, 1.02), (8.25, 1.02), color=F.GREEN, lw=1.9)
    F.arrow(ax, (5.80, 2.25), (8.55, 1.70), color=F.GREEN, lw=1.9)
    ax.text(7.45, 1.65, "反應式相加", color=F.GREEN, fontsize=10)
    ax.text(6.0, 5.72, "化學計量係數決定指數；改寫反應式必須同步改寫 K", ha="center", fontsize=15, weight="bold")
    return _save(fig, "選化III-1-反應式與平衡常數.svg")


def fig_ice_extent():
    """以 2NO2⇌N2O4 的精確二次解製作 ICE 長條圖。"""
    K = 4.0
    roots = np.roots([4 * K, -(4 * K + 1), K])
    x = float(np.min(roots[(roots > 0) & (roots < 0.5)]))
    no2_eq, n2o4_eq = 1 - 2 * x, x
    assert abs(n2o4_eq / no2_eq**2 - K) < 1e-10
    assert no2_eq > 0 and n2o4_eq > 0

    fig, axes = plt.subplots(1, 2, figsize=(11.8, 5.5), gridspec_kw={"width_ratios": [1.15, 0.85]})
    ax = axes[0]
    rows = ["初始 I", "改變 C", "平衡 E"]
    no2 = [1.0, -2 * x, no2_eq]
    n2o4 = [0.0, x, n2o4_eq]
    y = np.arange(3)
    width = 0.35
    ax.barh(y - width / 2, no2, height=width, color=F.BLUE, alpha=0.82, label=r"$NO_2$")
    ax.barh(y + width / 2, n2o4, height=width, color=F.RED, alpha=0.82, label=r"$N_2O_4$")
    ax.axvline(0, color=F.INK, lw=1)
    ax.set_yticks(y, rows)
    ax.invert_yaxis()
    ax.set_xlabel("濃度 / M（C 列表示帶號變化）")
    ax.set_xlim(-0.82, 1.08)
    F.clean_grid(ax)
    ax.legend(frameon=False, loc="lower right")
    ax.set_title(r"$2NO_2(g)\rightleftharpoons N_2O_4(g)$", weight="bold")

    ax = axes[1]
    ax.axis("off")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    _box(ax, (0.07, 0.64), 0.86, 0.22, r"$K_c=\dfrac{[N_2O_4]}{[NO_2]^2}=4.00$", face="#eef4ff", edge=F.BLUE, fs=13)
    ax.text(0.5, 0.52, rf"$x={x:.4f}\ \mathrm{{M}}$", ha="center", fontsize=13, color=F.PURPLE)
    ax.text(0.5, 0.39, rf"$[NO_2]_e=1.000-2x={no2_eq:.4f}\ \mathrm{{M}}$", ha="center", fontsize=11.5)
    ax.text(0.5, 0.28, rf"$[N_2O_4]_e=x={n2o4_eq:.4f}\ \mathrm{{M}}$", ha="center", fontsize=11.5)
    ax.text(0.5, 0.12, rf"檢查：${n2o4_eq:.4f}/({no2_eq:.4f})^2={K:.2f}$", ha="center", fontsize=11, color=F.GREEN)
    fig.suptitle("ICE 表的 C 列由反應進度與化學計量係數決定", fontsize=16, y=0.985)
    fig.subplots_adjust(left=0.08, right=0.985, top=0.80, bottom=0.15, wspace=0.16)
    return _save(fig, "選化III-1-ICE與反應進度.svg")


def fig_heterogeneous():
    """以 CaCO3 分解說明純固體活性固定且 Kp=P_CO2。"""
    kp = 0.80
    assert np.isclose(kp, 0.80)
    fig, axes = plt.subplots(1, 3, figsize=(12.5, 4.8))
    titles = ["兩種固相共存", "再加入 " + r"$CaCO_3(s)$", "移走部分 " + r"$CaO(s)$"]
    solid_counts = [(5, 4), (8, 4), (5, 2)]
    for ax, title, (n1, n2) in zip(axes, titles, solid_counts):
        ax.axis("off")
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.add_patch(Rectangle((0.16, 0.18), 0.68, 0.62, facecolor="#f8fafc", edgecolor=F.INK, lw=1.5))
        for i in range(n1):
            ax.add_patch(Circle((0.23 + 0.075 * i, 0.25), 0.032, color=F.BLUE, alpha=0.85))
        for i in range(n2):
            ax.add_patch(Circle((0.58 + 0.075 * (i % 4), 0.25 + 0.065 * (i // 4)), 0.032, color=F.AMBER, alpha=0.85))
        for x, y in [(0.28, 0.58), (0.50, 0.67), (0.70, 0.50), (0.62, 0.61)]:
            ax.text(x, y, r"$CO_2$", ha="center", fontsize=8.5, color=F.RED)
        ax.text(0.5, 0.90, title, ha="center", fontsize=12.3, weight="bold")
        ax.text(0.5, 0.08, r"$P_{CO_2}=0.80\,atm$", ha="center", fontsize=11, color=F.GREEN)
    fig.suptitle(r"$CaCO_3(s)\rightleftharpoons CaO(s)+CO_2(g)$：兩純固相都存在時 $K_p=P_{CO_2}$", fontsize=15.2, y=0.98)
    fig.text(0.5, 0.015, "改變純固體的量不改變其活性；相被完全移除後，原來的平衡式適用條件才失效。", ha="center", fontsize=10.5)
    fig.subplots_adjust(left=0.02, right=0.99, top=0.80, bottom=0.10, wspace=0.06)
    return _save(fig, "選化III-1-異相平衡與活性.svg")


def fig_concentration_step():
    """區分加料瞬間與後續平衡移動，驗證 Q 由 2 降為 1 再回到 2。"""
    K = 2.0
    a_before, b_before = 0.40, 0.80
    a_jump, b_jump = 0.80, 0.80
    total_after = a_jump + b_jump
    aeq, beq = total_after / (1 + K), K * total_after / (1 + K)
    assert np.isclose(b_before / a_before, K)
    assert np.isclose(b_jump / a_jump, 1.0) and b_jump / a_jump < K
    assert np.isclose(beq / aeq, K)
    t1 = np.linspace(-3, 0, 80, endpoint=False)
    t2 = np.linspace(0, 6, 300)
    tau = 1.25
    a2 = aeq + (a_jump - aeq) * np.exp(-t2 / tau)
    b2 = total_after - a2

    fig, ax = plt.subplots(figsize=(10.8, 5.6))
    ax.plot(t1, np.full_like(t1, a_before), color=F.BLUE, lw=2.5)
    ax.plot(t1, np.full_like(t1, b_before), color=F.RED, lw=2.5)
    ax.plot([0, 0], [a_before, a_jump], color=F.BLUE, lw=2.5)
    ax.plot(t2, a2, color=F.BLUE, lw=2.5, label="[A]")
    ax.plot(t2, b2, color=F.RED, lw=2.5, label="[B]")
    ax.axvline(0, color=F.INK, ls="--", lw=1.3)
    ax.annotate("在 t=0 加入 A\n只有 [A] 瞬間跳升", xy=(0, a_jump), xytext=(-2.5, 1.25),
                arrowprops={"arrowstyle": "->", "color": F.BLUE}, color=F.BLUE, fontsize=10.5)
    ax.annotate(r"$Q=1<K=2$，之後向右鬆弛", xy=(0.55, b2[28]), xytext=(1.35, 0.40),
                arrowprops={"arrowstyle": "->", "color": F.PURPLE}, color=F.PURPLE, fontsize=10.5)
    ax.text(5.85, aeq - 0.08, f"{aeq:.3f} M", ha="right", color=F.BLUE, fontsize=9.5)
    ax.text(5.85, beq + 0.04, f"{beq:.3f} M", ha="right", color=F.RED, fontsize=9.5)
    ax.set(xlabel="時間", ylabel="濃度 / M", xlim=(-3, 6), ylim=(0.25, 1.35), title=r"$A\rightleftharpoons B$，定溫 $K_c=2.00$")
    F.clean_grid(ax)
    ax.legend(frameon=False, loc="upper right")
    fig.suptitle("外加擾動先改變當下組成，再由淨反應建立新平衡", fontsize=16, y=0.985)
    fig.subplots_adjust(left=0.09, right=0.98, top=0.82, bottom=0.14)
    return _save(fig, "選化III-1-濃度擾動的瞬間與鬆弛.svg")


def fig_pressure_no2():
    """計算壓縮後 Q 的瞬變與 2NO2⇌N2O4 的新平衡。"""
    K = 4.0
    x0 = float(np.min(np.roots([4 * K, -(4 * K + 1), K])))
    no2_0, n2o4_0 = 1 - 2 * x0, x0
    no2_jump, n2o4_jump = 2 * no2_0, 2 * n2o4_0
    q_jump = n2o4_jump / no2_jump**2
    roots = np.roots([4 * K, -(4 * K * no2_jump + 1), K * no2_jump**2 - n2o4_jump])
    y = float(np.min(roots[(roots > 0) & (roots < no2_jump / 2)]))
    no2_new, n2o4_new = no2_jump - 2 * y, n2o4_jump + y
    assert np.isclose(n2o4_0 / no2_0**2, K)
    assert np.isclose(q_jump, K / 2)
    assert np.isclose(n2o4_new / no2_new**2, K)
    assert np.isclose(no2_new + 2 * n2o4_new, no2_jump + 2 * n2o4_jump)

    fig, axes = plt.subplots(1, 3, figsize=(13.0, 5.2))
    states = [
        ("壓縮前平衡", no2_0, n2o4_0, K, 1.0),
        ("體積瞬間減半", no2_jump, n2o4_jump, q_jump, 0.5),
        ("定溫新平衡", no2_new, n2o4_new, K, 0.5),
    ]
    concentration_max = max(max(c1, c2) for _, c1, c2, _, _ in states)
    for ax, (title, c1, c2, q, frac_v) in zip(axes, states):
        ax.axis("off")
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        width = 0.70 * frac_v + 0.18
        left = (1 - width) / 2
        ax.add_patch(Rectangle((left, 0.26), width, 0.46, facecolor="#fff7ed", edgecolor=F.INK, lw=1.5))
        usable = width - 0.10
        ax.add_patch(Rectangle((left + 0.05, 0.53), usable * c1 / concentration_max, 0.08,
                               facecolor="#c2410c", edgecolor="#7c2d12", alpha=0.86))
        ax.add_patch(Rectangle((left + 0.05, 0.37), usable * c2 / concentration_max, 0.08,
                               facecolor="#cbd5e1", edgecolor="#64748b", alpha=0.95))
        ax.text(0.5, 0.64, r"濃度條：$NO_2$（紅棕）", ha="center", fontsize=8.2, color="#9a3412")
        ax.text(0.5, 0.47, r"濃度條：$N_2O_4$（淡色）", ha="center", fontsize=8.2, color="#475569")
        ax.text(0.5, 0.88, title, ha="center", fontsize=12.5, weight="bold")
        ax.text(0.5, 0.17, rf"$[NO_2]={c1:.3f}$ M；$[N_2O_4]={c2:.3f}$ M", ha="center", fontsize=9.4)
        ax.text(0.5, 0.08, rf"$Q_c={q:.2f}$", ha="center", fontsize=11, color=F.GREEN if np.isclose(q, K) else F.RED)
    F.arrow(axes[1], (0.50, 0.80), (0.50, 0.72), color=F.RED, lw=2)
    axes[1].text(0.5, 0.95, "濃度同時加倍", ha="center", fontsize=9.5, color=F.RED)
    axes[2].text(0.5, 0.95, r"$Q<K$：淨生成 $N_2O_4$", ha="center", fontsize=9.5, color=F.PURPLE)
    fig.suptitle(r"$2NO_2(g)\rightleftharpoons N_2O_4(g)$：壓縮使 $Q$ 先降為 $K/2$，再向氣體莫耳數較少的一側移動", fontsize=14.6, y=0.99)
    fig.subplots_adjust(left=0.01, right=0.995, top=0.78, bottom=0.02, wspace=0.04)
    return _save(fig, "選化III-1-壓縮NO2-N2O4平衡.svg")


def fig_temperature_k():
    """用數值模型生成放熱反應 K 隨 T 單調下降的定性曲線。"""
    R = 8.314
    dH = -57_000.0
    T0, K0 = 298.15, 6.90
    T = np.linspace(250, 500, 400)
    K = K0 * np.exp(-dH / R * (1 / T - 1 / T0))
    assert np.all(np.diff(K) < 0)
    assert np.isclose(K[np.argmin(abs(T - T0))], K0, rtol=0.03)

    fig, ax = plt.subplots(figsize=(10.8, 5.7))
    ax.semilogy(T, K, color=F.RED, lw=2.7)
    ax.scatter([T0], [K0], color=F.RED, zorder=5)
    ax.annotate(r"$298\,K, K=6.90$", (T0, K0), xytext=(325, 30),
                arrowprops={"arrowstyle": "->", "color": F.RED}, color=F.RED)
    ax.text(0.64, 0.75, "本章判讀：升溫 → K 減小\n平衡組成偏向反應物", transform=ax.transAxes,
            ha="center", fontsize=12.2, color=F.PURPLE,
            bbox={"boxstyle": "round,pad=0.35", "facecolor": "#f4effa", "edgecolor": F.PURPLE})
    ax.text(0.64, 0.55, "曲線為定性教學模型；不以圖中數值計算 K", transform=ax.transAxes,
            ha="center", fontsize=10.6, color=F.INK)
    ax.set(xlabel="絕對溫度 T / K", ylabel="平衡常數 K（對數尺度）", title="只有溫度改變指定反應的平衡常數")
    F.clean_grid(ax)
    fig.suptitle("把熱量視為反應條件：方向判斷與 K 的變化必須一致", fontsize=16, y=0.985)
    fig.subplots_adjust(left=0.10, right=0.98, top=0.82, bottom=0.14)
    return _save(fig, "選化III-1-溫度改變平衡常數.svg")


def fig_catalyst_energy():
    """建立同一反應的未催化／催化能障，驗證兩端能量不變。"""
    x = np.linspace(0, 1, 500)
    baseline = -30 * x
    unc = baseline + 90 * np.sin(np.pi * x) ** 2
    cat = baseline + 50 * np.sin(np.pi * x) ** 2
    assert np.isclose(unc[0], cat[0]) and np.isclose(unc[-1], cat[-1])
    assert unc.max() > cat.max()
    assert np.isclose(unc[-1] - unc[0], cat[-1] - cat[0])

    fig, ax = plt.subplots(figsize=(10.6, 5.6))
    ax.plot(x, unc, color=F.RED, lw=2.5, label="未催化路徑")
    ax.plot(x, cat, color=F.BLUE, lw=2.5, label="催化路徑")
    ax.hlines([0, -30], [0, 0.82], [0.18, 1], colors=F.INK, lw=1.2)
    ax.text(0.02, 3, "反應物", fontsize=11)
    ax.text(0.83, -27, "產物", fontsize=11)
    F.arrow(ax, (0.88, 0), (0.88, -30), color=F.GREEN, lw=1.8, mutation=12)
    ax.text(0.90, -15, "兩端能量差不變", va="center", fontsize=10.5, color=F.GREEN)
    ax.annotate("正、逆向活化能都降低", xy=(0.50, cat.max()), xytext=(0.58, 58),
                arrowprops={"arrowstyle": "->", "color": F.PURPLE}, color=F.PURPLE, fontsize=10.5)
    ax.set(xlabel="反應進行程度", ylabel="相對能量 / kJ mol$^{-1}$", xlim=(0, 1), ylim=(-42, 78), title="催化劑改變路徑，不改變反應物與產物的能量差")
    ax.set_xticks([])
    F.clean_grid(ax)
    ax.legend(frameon=False)
    fig.suptitle("催化劑使系統更快到達同一平衡組成", fontsize=16, y=0.985)
    fig.subplots_adjust(left=0.10, right=0.97, top=0.81, bottom=0.13)
    return _save(fig, "選化III-1-催化劑與平衡.svg")


def fig_haber_tradeoff():
    """用明示為教學模型的合成氨資料呈現溫度、壓力與速率權衡。"""
    temps = np.array([350, 400, 450, 500, 550])
    yield_100 = np.array([52, 38, 27, 19, 13])
    yield_300 = np.array([78, 65, 51, 38, 28])
    rate_index = np.array([0.18, 0.38, 0.65, 0.86, 1.00])
    assert np.all(np.diff(yield_100) < 0) and np.all(np.diff(yield_300) < 0)
    assert np.all(yield_300 > yield_100) and np.all(np.diff(rate_index) > 0)

    fig, axes = plt.subplots(1, 2, figsize=(12.0, 5.5))
    ax = axes[0]
    ax.plot(temps, yield_100, "o-", color=F.BLUE, lw=2.3, label="100 atm")
    ax.plot(temps, yield_300, "o-", color=F.RED, lw=2.3, label="300 atm")
    ax.set(xlabel="溫度 / °C", ylabel=r"平衡 $NH_3$ 莫耳百分率 / %", ylim=(0, 88), title="放熱、氣體莫耳數減少：低溫高壓提高平衡產率")
    F.clean_grid(ax)
    ax.legend(frameon=False)
    ax = axes[1]
    ax.plot(temps, rate_index, "o-", color=F.AMBER, lw=2.5)
    ax.set(xlabel="溫度 / °C", ylabel="相對反應速率指標", ylim=(0, 1.08), title="降溫同時使達到平衡的時間拉長")
    F.clean_grid(ax)
    ax.axvspan(400, 500, color=F.GREEN, alpha=0.10)
    ax.text(450, 0.10, "工業操作區間示意\n配合催化劑、循環與移除 " + r"$NH_3$", ha="center", fontsize=10.5, color=F.GREEN)
    fig.suptitle(r"合成氨 $N_2+3H_2\rightleftharpoons2NH_3$：平衡、速率、設備成本必須共同最佳化", fontsize=15, y=0.985)
    fig.text(0.5, 0.01, "圖中數值是展示趨勢的教學模型，不是特定工廠設計資料。", ha="center", fontsize=9.8)
    fig.subplots_adjust(left=0.07, right=0.985, top=0.79, bottom=0.15, wspace=0.24)
    return _save(fig, "選化III-1-合成氨條件權衡.svg")


def fig_ksp_stoichiometry():
    """以同一莫耳溶解度驗證 AB 與 AB2 的離子濃度及 Ksp 次方。"""
    s = 1.0e-3
    ab = np.array([s, s])
    ab2 = np.array([s, 2 * s])
    k_ab = ab[0] * ab[1]
    k_ab2 = ab2[0] * ab2[1] ** 2
    assert np.isclose(k_ab, 1e-6)
    assert np.isclose(k_ab2, 4e-9)

    fig, axes = plt.subplots(1, 2, figsize=(11.8, 5.3))
    specs = [
        (axes[0], r"$AB(s)\rightleftharpoons A^+ + B^-$", ab, r"$K_{sp}=s^2=1.0\times10^{-6}$"),
        (axes[1], r"$AB_2(s)\rightleftharpoons A^{2+} + 2B^-$", ab2, r"$K_{sp}=s(2s)^2=4.0\times10^{-9}$"),
    ]
    for ax, title, vals, formula in specs:
        bars = ax.bar(["陽離子", "陰離子"], vals * 1000, color=[F.BLUE, F.RED], alpha=0.82)
        for bar, val in zip(bars, vals):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.06, f"{val:.1e} M", ha="center", fontsize=10)
        ax.set_ylim(0, 2.45)
        ax.set_ylabel(r"濃度 / ($10^{-3}$ M)")
        ax.set_title(title, weight="bold")
        F.clean_grid(ax)
        ax.text(0.5, 0.88, formula, transform=ax.transAxes, ha="center", fontsize=11.5,
                bbox={"boxstyle": "round,pad=0.3", "facecolor": "#fff7dd", "edgecolor": F.AMBER})
    fig.suptitle(r"同為 $s=1.0\times10^{-3}\,M$，化學計量係數使離子濃度與 $K_{sp}$ 形式不同", fontsize=15.2, y=0.985)
    fig.subplots_adjust(left=0.08, right=0.985, top=0.78, bottom=0.14, wspace=0.24)
    return _save(fig, "選化III-1-溶度積與莫耳溶解度.svg")


def fig_common_ion():
    """精確解 s(s+c)=Ksp，驗證 AgCl 溶解度隨外加 Cl− 單調下降。"""
    ksp = 1.8e-10
    chloride = np.logspace(-10, -1, 400)
    s = (-chloride + np.sqrt(chloride**2 + 4 * ksp)) / 2
    pure = np.sqrt(ksp)
    assert np.all(np.diff(s) < 0)
    assert np.isclose(pure, 1.341640786e-5, rtol=1e-8)
    c_mark = 1e-3
    s_mark = (-c_mark + np.sqrt(c_mark**2 + 4 * ksp)) / 2
    assert np.isclose(s_mark * (s_mark + c_mark), ksp)

    fig, ax = plt.subplots(figsize=(10.7, 5.7))
    ax.loglog(chloride, s, color=F.BLUE, lw=2.7)
    ax.axhline(pure, color=F.RED, ls="--", lw=1.4, label=rf"純水中 $s=\sqrt{{K_{{sp}}}}={pure:.2e}$ M")
    ax.scatter([c_mark], [s_mark], color=F.PURPLE, zorder=5)
    ax.annotate(rf"$[Cl^-]_0=10^{{-3}}$ M" + "\n" + rf"$s={s_mark:.2e}$ M", (c_mark, s_mark), xytext=(2e-5, 8e-7),
                arrowprops={"arrowstyle": "->", "color": F.PURPLE}, color=F.PURPLE, fontsize=10.5)
    ax.set(xlabel=r"外加 $[Cl^-]_0$ / M", ylabel="AgCl 莫耳溶解度 s / M", title=r"$AgCl(s)\rightleftharpoons Ag^++Cl^-$，$s(s+[Cl^-]_0)=K_{sp}$")
    F.clean_grid(ax)
    ax.legend(frameon=False, loc="lower left")
    fig.suptitle("同離子增加反應商，溶解反應向固體側移動", fontsize=16, y=0.985)
    fig.subplots_adjust(left=0.11, right=0.98, top=0.81, bottom=0.15)
    return _save(fig, "選化III-1-同離子與AgCl溶解度.svg")


def fig_precipitation_window():
    """同時驗證混合後 Qsp 與 AgCl/Ag2CrO4 的選擇沉澱門檻。"""
    k_agcl, k_ag2cro4 = 1.8e-10, 1.1e-12
    ag_mix, cl_mix = 1.0e-4, 5.0e-4
    q_mix = ag_mix * cl_mix
    cl0, cro40 = 1.0e-2, 1.0e-2
    ag_cl_start = k_agcl / cl0
    ag_cro4_start = np.sqrt(k_ag2cro4 / cro40)
    cl_at_second = k_agcl / ag_cro4_start
    removed = 1 - cl_at_second / cl0
    assert q_mix > k_agcl
    assert ag_cl_start < ag_cro4_start
    assert removed > 0.998

    fig, axes = plt.subplots(1, 2, figsize=(12.4, 5.5))
    ax = axes[0]
    bars = ax.bar([r"$Q_{sp}$", r"$K_{sp}$"], [q_mix, k_agcl], color=[F.RED, F.BLUE], alpha=0.82)
    ax.set_yscale("log")
    ax.set_ylim(1e-11, 1e-7)
    for bar, value in zip(bars, [q_mix, k_agcl]):
        ax.text(bar.get_x() + bar.get_width()/2, value * 1.6, f"{value:.1e}", ha="center", fontsize=10)
    ax.set_title("等體積混合後先稀釋，再算離子積", weight="bold")
    ax.text(0.5, 0.10, r"$[Ag^+]=1.0\times10^{-4}$ M" + "\n" + r"$[Cl^-]=5.0\times10^{-4}$ M" + "\n" + r"$Q_{sp}>K_{sp}$：生成 AgCl(s)",
            transform=ax.transAxes, ha="center", fontsize=10.5, color=F.RED)
    F.clean_grid(ax)

    ax = axes[1]
    ax.set_xscale("log")
    ax.set_xlim(1e-9, 1e-4)
    ax.set_ylim(0, 1)
    ax.axvline(ag_cl_start, color=F.BLUE, lw=2.2)
    ax.axvline(ag_cro4_start, color=F.RED, lw=2.2)
    ax.axvspan(ag_cl_start, ag_cro4_start, color=F.GREEN, alpha=0.14)
    ax.text(ag_cl_start * 1.25, 0.82, "AgCl 開始", color=F.BLUE, fontsize=10)
    ax.text(ag_cro4_start * 0.85, 0.67, r"$Ag_2CrO_4$ 開始", color=F.RED, fontsize=10, ha="right")
    ax.text(np.sqrt(ag_cl_start * ag_cro4_start), 0.42, "選擇沉澱 AgCl 的操作窗", ha="center", fontsize=11, color=F.GREEN)
    ax.text(0.5, 0.13, "第二種鹽剛沉澱時，" + r"$Cl^-$" + f" 已移除 {removed*100:.2f}%", transform=ax.transAxes, ha="center", fontsize=10.5)
    ax.set_xlabel(r"逐漸增加的 $[Ag^+]$ / M")
    ax.set_yticks([])
    ax.set_title("比較各沉澱開始所需的臨界離子濃度", weight="bold")
    F.clean_grid(ax)
    fig.suptitle("沉澱判斷用 Qsp/Ksp；分離設計用各鹽的起始沉澱門檻", fontsize=16, y=0.985)
    fig.subplots_adjust(left=0.08, right=0.985, top=0.79, bottom=0.14, wspace=0.23)
    return _save(fig, "選化III-1-離子積與選擇沉澱.svg")


def fig_fescn_experiment():
    """用等吸光度、不同光徑資料驗證 FeSCN2+ 濃度與 Kc 計算。"""
    c_std, l_std, l_sample = 1.50e-4, 1.00, 3.00
    c_eq = c_std * l_std / l_sample
    fe0, scn0 = 1.00e-3, 2.00e-4
    kc = c_eq / ((fe0 - c_eq) * (scn0 - c_eq))
    assert np.isclose(c_std * l_std, c_eq * l_sample)
    assert np.isclose(c_eq, 5.00e-5)
    assert np.isclose(kc, 350.8771929824561)

    fig, ax = plt.subplots(figsize=(12.4, 5.6))
    ax.axis("off")
    ax.set_xlim(0, 12.4)
    ax.set_ylim(0, 5.6)
    boxes = [
        ((0.25, 2.05), 2.35, 1.55, "配製標準液\n" + r"$Fe^{3+}$ 大量過量" + "\n" + r"$[FeSCN^{2+}]\approx1.50\times10^{-4}$ M", "#eef4ff", F.BLUE),
        ((3.15, 2.05), 2.35, 1.55, "調整光徑比色\n標準 1.00 cm\n樣品 3.00 cm", "#fff7dd", F.AMBER),
        ((6.05, 2.05), 2.35, 1.55, "相同吸光度 A\n" + r"$A=\varepsilon \ell c$" + "\n" + r"$[FeSCN^{2+}]_e=5.00\times10^{-5}$ M", "#f3e8ff", F.PURPLE),
        ((8.95, 2.05), 3.15, 1.55, r"代入平衡組成" + "\n" + r"$K_c=\dfrac{5.00\times10^{-5}}{(9.50\times10^{-4})(1.50\times10^{-4})}$" + "\n" + r"$=3.51\times10^2$", "#ecfdf5", F.GREEN),
    ]
    for (x, y), w, h, txt, face, edge in boxes:
        _box(ax, (x, y), w, h, txt, face=face, edge=edge, fs=10.1)
    for x in (2.60, 5.50, 8.40):
        F.arrow(ax, (x, 2.82), (x + 0.50, 2.82), color=F.INK, lw=1.8, mutation=12)
    ax.text(6.2, 5.25, r"$Fe^{3+}+SCN^-\rightleftharpoons FeSCN^{2+}$", ha="center", fontsize=16, weight="bold")
    ax.text(0.40, 1.35, "觀察", fontsize=11.5, color=F.BLUE, weight="bold")
    ax.text(1.20, 1.35, "兩管紅色深淺相同", fontsize=10.5)
    ax.text(4.35, 1.35, "證據", fontsize=11.5, color=F.PURPLE, weight="bold")
    ax.text(5.15, 1.35, "同波長、同 ε 下，ℓc 相同", fontsize=10.5)
    ax.text(8.65, 1.35, "推論", fontsize=11.5, color=F.GREEN, weight="bold")
    ax.text(9.45, 1.35, "由光徑比求濃度，再由 ICE 求 K", fontsize=10.5)
    ax.text(6.2, 0.55, "控制：溫度、光源／波長、試管潔淨與幾何；限制：標準液近完全反應與肉眼比色造成系統誤差。", ha="center", fontsize=10.3)
    fig.suptitle("比色法把顏色觀察轉成可代入平衡式的濃度證據", fontsize=16, y=0.99)
    return _save(fig, "選化III-1-FeSCN平衡常數實驗.svg")


def main():
    generated = []
    for entrypoint, filename in FIGURE_OUTPUTS:
        function = globals()[entrypoint]
        result = function()
        assert os.path.basename(result) == filename
        generated.append(filename)
    assert len(generated) == len(set(generated)) == 14
    assert set(generated) == {name for _, name in FIGURE_OUTPUTS}


if __name__ == "__main__":
    main()
