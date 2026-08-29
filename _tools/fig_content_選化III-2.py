# -*- coding: utf-8 -*-
"""產生「選化 III-2 酸鹼反應」學生講義章內 SVG。

重繪：.venv/bin/python _tools/fig_content_選化III-2.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, FancyBboxPatch, Polygon, Rectangle

import figlib as F


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CH = os.path.join(ROOT, "content", "選修化學III", "選化III-2")


FIGURE_OUTPUTS = (
    ("fig_proton_transfer", "選化III-2-質子轉移與共軛對.svg"),
    ("fig_acid_strength_direction", "選化III-2-酸鹼強度與反應方向.svg"),
    ("fig_kw_temperature", "選化III-2-Kw溫度與中性pH.svg"),
    ("fig_weak_acid_dissociation", "選化III-2-弱酸解離濃度與百分比.svg"),
    ("fig_conjugate_ka_kb", "選化III-2-共軛酸鹼KaKb.svg"),
    ("fig_common_ion", "選化III-2-同離子效應濃度帳.svg"),
    ("fig_diprotic_distribution", "選化III-2-二質子酸物種分布.svg"),
    ("fig_salt_hydrolysis", "選化III-2-鹽類水解與pH.svg"),
    ("fig_buffer_response", "選化III-2-緩衝液加入酸鹼.svg"),
    ("fig_buffer_capacity", "選化III-2-緩衝比例與容量.svg"),
    ("fig_titration_apparatus", "選化III-2-滴定裝置與數據.svg"),
    ("fig_titration_curves", "選化III-2-三類滴定曲線.svg"),
    ("fig_weak_acid_titration_regions", "選化III-2-弱酸滴定分區與物種.svg"),
)


def _save(fig, filename):
    assert filename.endswith(".svg")
    return F.save_to(fig, CH, filename[:-4], output_subdir="assets", write_pdf=False)


def _box(ax, xy, width, height, text, *, face="#f8fafc", edge="#64748b", fs=11, lw=1.4):
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


def _positive_root(a, b, c):
    roots = np.roots([a, b, c])
    valid = roots[np.isreal(roots) & (np.real(roots) >= 0)]
    assert len(valid) >= 1
    return float(np.min(np.real(valid)))


def _weak_acid_h(ka, c0):
    x = _positive_root(1.0, ka, -ka * c0)
    assert 0 <= x <= c0
    assert np.isclose(x * x / (c0 - x), ka, rtol=1e-9, atol=1e-15)
    return x


def _weak_base_oh(kb, c0):
    return _weak_acid_h(kb, c0)


def fig_proton_transfer():
    """用粒子與電荷帳驗證 HCl/H2O 的質子轉移和共軛對。"""
    atoms_left = {"H": 3, "Cl": 1, "O": 1}
    atoms_right = {"H": 3, "Cl": 1, "O": 1}
    charges_left = 0
    charges_right = 1 - 1
    assert atoms_left == atoms_right and charges_left == charges_right == 0

    fig, ax = plt.subplots(figsize=(12.2, 5.3))
    ax.axis("off")
    ax.set_xlim(0, 12.2)
    ax.set_ylim(0, 5.3)

    _box(ax, (0.35, 2.10), 2.15, 1.35, r"$HCl$" + "\n提供 $H^+$", face="#fff0f0", edge=F.RED, fs=14)
    _box(ax, (3.05, 2.10), 2.15, 1.35, r"$H_2O$" + "\n接受 $H^+$", face="#eef4ff", edge=F.BLUE, fs=14)
    _box(ax, (7.05, 2.10), 2.15, 1.35, r"$H_3O^+$" + "\n可再提供 $H^+$", face="#fff7dd", edge=F.AMBER, fs=14)
    _box(ax, (9.70, 2.10), 2.15, 1.35, r"$Cl^-$" + "\n可再接受 $H^+$", face="#eefbf2", edge=F.GREEN, fs=14)
    ax.text(2.76, 2.78, "+", fontsize=22, ha="center", va="center")
    ax.text(9.46, 2.78, "+", fontsize=22, ha="center", va="center")
    F.arrow(ax, (5.45, 2.78), (6.75, 2.78), color=F.PURPLE, lw=2.6)
    ax.text(6.10, 3.18, "$H^+$ 轉移", ha="center", fontsize=12, color=F.PURPLE)

    ax.plot([0.55, 2.30], [1.18, 1.18], color=F.RED, lw=2.0)
    ax.plot([9.88, 11.62], [1.18, 1.18], color=F.GREEN, lw=2.0)
    ax.text(6.08, 0.93, r"共軛酸鹼對：$HCl/Cl^-$（只差一個 $H^+$）", ha="center", fontsize=12)
    ax.plot([3.26, 4.98], [0.42, 0.42], color=F.BLUE, lw=2.0)
    ax.plot([7.25, 8.98], [0.42, 0.42], color=F.AMBER, lw=2.0)
    ax.text(6.08, 0.17, r"共軛酸鹼對：$H_3O^+/H_2O$（只差一個 $H^+$）", ha="center", fontsize=12)
    ax.text(6.1, 4.72, r"$HCl+H_2O\rightarrow H_3O^++Cl^-$：原子數與總電荷同時守恆", ha="center", fontsize=16, weight="bold")
    return _save(fig, "選化III-2-質子轉移與共軛對.svg")


def fig_acid_strength_direction():
    """以 pKa 軸驗證質子轉移偏向較弱酸與較弱鹼。"""
    names = [r"$H_3O^+$", r"$CH_3COOH$", r"$H_2CO_3$", r"$NH_4^+$", r"$H_2O$"]
    pka = np.array([-1.7, 4.76, 6.35, 9.25, 14.0])
    assert np.all(np.diff(pka) > 0)
    k_rxn = 10 ** (9.25 - 4.76)
    assert 3.0e4 < k_rxn < 3.2e4

    fig, axes = plt.subplots(1, 2, figsize=(12.4, 5.5), gridspec_kw={"width_ratios": [0.80, 1.20]})
    ax = axes[0]
    y = np.arange(len(names))
    ax.scatter(pka, y, s=90, color=[F.RED, F.RED, F.AMBER, F.BLUE, F.BLUE], zorder=4)
    for x, yy, name in zip(pka, y, names):
        ax.text(x + 0.28, yy, name, va="center", fontsize=12)
    ax.set_yticks([])
    ax.set_xlabel(r"$pK_a$（向右愈大，酸愈弱）")
    ax.set_xlim(-2.8, 16.2)
    ax.set_ylim(-0.7, len(names) - 0.3)
    ax.invert_yaxis()
    F.clean_grid(ax)
    ax.set_title("酸的相對強度", weight="bold")

    ax = axes[1]
    ax.axis("off")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    _box(ax, (0.04, 0.62), 0.92, 0.22, r"$CH_3COOH+NH_3\rightleftharpoons CH_3COO^-+NH_4^+$", face="#f8fafc", edge=F.PURPLE, fs=14)
    ax.text(0.50, 0.51, r"反應物酸：$pK_a=4.76$", ha="center", fontsize=12, color=F.RED)
    ax.text(0.50, 0.42, r"產物酸：$pK_a=9.25$", ha="center", fontsize=12, color=F.BLUE)
    ax.text(0.50, 0.29, rf"$K\approx10^{{9.25-4.76}}={k_rxn:.1e}$", ha="center", fontsize=14, color=F.GREEN)
    F.arrow(ax, (0.31, 0.16), (0.69, 0.16), color=F.GREEN, lw=2.5)
    ax.text(0.50, 0.08, "質子主要移向較弱酸、較弱鹼的一側", ha="center", fontsize=12.5)
    fig.suptitle("以共軛酸的 $pK_a$ 比較質子轉移方向", fontsize=16, y=0.985)
    fig.subplots_adjust(left=0.07, right=0.985, bottom=0.14, top=0.82, wspace=0.18)
    return _save(fig, "選化III-2-酸鹼強度與反應方向.svg")


def fig_kw_temperature():
    """依課本 Kw 表計算不同溫度下的中性 pH。"""
    temperature = np.array([0.0, 25.0, 50.0, 75.0, 100.0])
    kw = np.array([1.1e-15, 1.0e-14, 5.5e-14, 2.0e-13, 5.6e-13])
    pkw = -np.log10(kw)
    neutral_ph = pkw / 2
    assert np.all(np.diff(kw) > 0)
    assert np.all(np.diff(neutral_ph) < 0)
    assert np.isclose(neutral_ph[1], 7.0)

    fig, axes = plt.subplots(1, 2, figsize=(12.0, 5.4))
    ax = axes[0]
    ax.plot(temperature, neutral_ph, marker="o", lw=2.5, color=F.BLUE)
    for t, ph in zip(temperature, neutral_ph):
        ax.text(t, ph + 0.08, f"{ph:.2f}", ha="center", fontsize=9.5)
    ax.set(xlabel="溫度 / °C", ylabel="中性 pH", ylim=(5.9, 7.75), title=r"中性條件：$[H^+]=[OH^-]=\sqrt{K_w}$")
    F.clean_grid(ax)

    ax = axes[1]
    ax.axis("off")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    t = 50.0
    kw50 = kw[2]
    phn = neutral_ph[2]
    _box(ax, (0.08, 0.68), 0.84, 0.18, rf"$50\,^\circ C:\ K_w={kw50:.1e}$", face="#eef4ff", edge=F.BLUE, fs=14)
    _box(ax, (0.08, 0.43), 0.84, 0.18, rf"中性 pH $=\frac{{1}}{{2}}pK_w={phn:.2f}$", face="#eefbf2", edge=F.GREEN, fs=14)
    ax.text(0.50, 0.30, "pH 7.00 在此溫度呈鹼性", ha="center", fontsize=13, color=F.PURPLE)
    ax.text(0.50, 0.20, r"判準是 $[H^+]$ 與 $[OH^-]$ 的大小", ha="center", fontsize=12)
    ax.text(0.50, 0.10, "中性 pH 會隨溫度改變", ha="center", fontsize=12)
    fig.suptitle(r"$K_w=[H^+][OH^-]$ 隨溫度改變；中性不固定等於 pH 7", fontsize=16, y=0.985)
    fig.subplots_adjust(left=0.08, right=0.985, bottom=0.14, top=0.82, wspace=0.20)
    return _save(fig, "選化III-2-Kw溫度與中性pH.svg")


def fig_weak_acid_dissociation():
    """精確解弱酸二次式，核對濃度、pH 與解離百分比。"""
    ka = 1.8e-5
    c0 = np.logspace(-4, 0, 300)
    h = np.array([_weak_acid_h(ka, c) for c in c0])
    alpha = h / c0 * 100
    assert np.all(np.diff(h) > 0)
    assert np.all(np.diff(alpha) < 0)
    c_mark = 0.10
    h_mark = _weak_acid_h(ka, c_mark)
    alpha_mark = 100 * h_mark / c_mark
    assert np.isclose(h_mark * h_mark / (c_mark - h_mark), ka, rtol=1e-10)

    fig, axes = plt.subplots(1, 2, figsize=(12.0, 5.4))
    ax = axes[0]
    ax.loglog(c0, h, color=F.RED, lw=2.5, label="精確二次解")
    ax.loglog(c0, np.sqrt(ka * c0), color=F.BLUE, ls="--", lw=1.8, label=r"$\sqrt{K_aC_0}$ 近似")
    ax.scatter([c_mark], [h_mark], color=F.PURPLE, s=60, zorder=5)
    ax.text(c_mark * 0.85, h_mark * 1.6, rf"$C_0=0.10$ M\n$[H^+]={h_mark:.2e}$ M", ha="right", fontsize=9.5)
    ax.set(xlabel=r"弱酸分析濃度 $C_0$ / M", ylabel=r"平衡 $[H^+]$ / M", title=r"濃度升高，$[H^+]$ 升高")
    F.clean_grid(ax)
    ax.legend(frameon=False, fontsize=9.5)

    ax = axes[1]
    ax.semilogx(c0, alpha, color=F.GREEN, lw=2.5)
    ax.scatter([c_mark], [alpha_mark], color=F.PURPLE, s=60, zorder=5)
    ax.axhline(5, color=F.AMBER, ls="--", lw=1.4)
    ax.text(c_mark * 1.15, alpha_mark, f"{alpha_mark:.2f}%", va="center", fontsize=10)
    ax.set(xlabel=r"弱酸分析濃度 $C_0$ / M", ylabel="解離百分比 / %", title="稀釋時，解離百分比上升")
    ax.set_ylim(0, min(45, alpha.max() * 1.08))
    F.clean_grid(ax)
    fig.suptitle(r"$K_a=1.8\times10^{-5}$ 的單質子弱酸：$K_a=x^2/(C_0-x)$", fontsize=16, y=0.985)
    fig.subplots_adjust(left=0.08, right=0.985, bottom=0.14, top=0.82, wspace=0.22)
    return _save(fig, "選化III-2-弱酸解離濃度與百分比.svg")


def fig_conjugate_ka_kb():
    """驗證兩組共軛酸鹼的 KaKb=Kw。"""
    kw = 1.0e-14
    pairs = [
        (r"$CH_3COOH/CH_3COO^-$", 1.8e-5, kw / 1.8e-5),
        (r"$NH_4^+/NH_3$", kw / 1.8e-5, 1.8e-5),
        (r"$H_2CO_3/HCO_3^-$", 4.3e-7, kw / 4.3e-7),
    ]
    for _, ka, kb in pairs:
        assert np.isclose(ka * kb, kw, rtol=1e-12)

    fig, ax = plt.subplots(figsize=(11.4, 5.6))
    y = np.arange(len(pairs))
    pka = [-np.log10(p[1]) for p in pairs]
    pkb = [-np.log10(p[2]) for p in pairs]
    ax.barh(y - 0.18, pka, height=0.34, color=F.RED, alpha=0.82, label=r"$pK_a$")
    ax.barh(y + 0.18, pkb, height=0.34, color=F.BLUE, alpha=0.82, label=r"$pK_b$")
    for yy, a, b in zip(y, pka, pkb):
        ax.text(a + 0.14, yy - 0.18, f"{a:.2f}", va="center", fontsize=10)
        ax.text(b + 0.14, yy + 0.18, f"{b:.2f}", va="center", fontsize=10)
        ax.text(13.85, yy, f"和 = {a+b:.2f}", ha="right", va="center", fontsize=10.5, color=F.GREEN)
    ax.set_yticks(y, [p[0] for p in pairs])
    ax.set_xlim(0, 14.5)
    ax.invert_yaxis()
    ax.set_xlabel("常數的負對數")
    ax.set_title(r"25 °C：每組共軛酸鹼都滿足 $K_aK_b=K_w$，即 $pK_a+pK_b=14.00$", weight="bold")
    F.clean_grid(ax)
    ax.legend(frameon=False, loc="lower right")
    fig.subplots_adjust(left=0.22, right=0.97, bottom=0.15, top=0.84)
    return _save(fig, "選化III-2-共軛酸鹼KaKb.svg")


def fig_common_ion():
    """精確解醋酸/醋酸根的同離子平衡並與純弱酸比較。"""
    ka = 1.8e-5
    ha0, a0 = 0.050, 0.100
    x = _positive_root(1.0, a0 + ka, -ka * ha0)
    h_buffer = x
    ha_eq, a_eq = ha0 - x, a0 + x
    assert np.isclose(h_buffer * a_eq / ha_eq, ka, rtol=1e-10)
    h_pure = _weak_acid_h(ka, ha0)
    assert h_buffer < h_pure / 10

    fig, axes = plt.subplots(1, 2, figsize=(12.0, 5.5), gridspec_kw={"width_ratios": [1.15, 0.85]})
    ax = axes[0]
    rows = ["初始", "改變", "平衡"]
    vals = np.array([[ha0, a0, 0.0], [-x, x, x], [ha_eq, a_eq, h_buffer]])
    colors = [F.RED, F.BLUE, F.PURPLE]
    labels = [r"$HA$", r"$A^-$", r"$H^+$"]
    y = np.arange(3)
    for j in range(3):
        ax.barh(y + (j - 1) * 0.22, vals[:, j], height=0.20, color=colors[j], alpha=0.82, label=labels[j])
    ax.axvline(0, color=F.INK, lw=1)
    ax.set_yticks(y, rows)
    ax.invert_yaxis()
    ax.set_xlabel("濃度 / M（改變列保留正負號）")
    ax.set_title(r"$HA\rightleftharpoons H^++A^-$：加入 $A^-$ 後的濃度帳")
    F.clean_grid(ax)
    ax.legend(frameon=False, ncol=3, loc="lower right")

    ax = axes[1]
    labels2 = ["0.050 M\n純弱酸", "0.050 M $HA$\n+ 0.100 M $A^-$"]
    hvals = [h_pure, h_buffer]
    ax.bar(labels2, hvals, color=[F.RED, F.GREEN], alpha=0.82)
    ax.set_yscale("log")
    ax.set_ylabel(r"平衡 $[H^+]$ / M")
    ax.set_title("同離子壓低弱酸解離")
    F.clean_grid(ax)
    for i, v in enumerate(hvals):
        ax.text(i, v * 1.25, f"{v:.2e}", ha="center", fontsize=10)
    fig.suptitle(rf"$K_a={ka:.1e}$；混合系的精確解為 $[H^+]={h_buffer:.2e}$ M", fontsize=16, y=0.985)
    fig.subplots_adjust(left=0.08, right=0.985, bottom=0.16, top=0.80, wspace=0.24)
    return _save(fig, "選化III-2-同離子效應濃度帳.svg")


def fig_diprotic_distribution():
    """以解析分率式驗證二質子酸的三種主要物種分布。"""
    ka1, ka2 = 1.0e-4, 1.0e-8
    ph = np.linspace(1, 12, 700)
    h = 10 ** (-ph)
    den = h * h + ka1 * h + ka1 * ka2
    a0 = h * h / den
    a1 = ka1 * h / den
    a2 = ka1 * ka2 / den
    assert np.allclose(a0 + a1 + a2, 1.0, atol=1e-12)
    for pka in (4.0, 8.0):
        idx = int(np.argmin(abs(ph - pka)))
        if pka == 4.0:
            assert abs(a0[idx] - a1[idx]) < 0.02
        else:
            assert abs(a1[idx] - a2[idx]) < 0.02

    fig, ax = plt.subplots(figsize=(11.2, 5.6))
    ax.plot(ph, a0, lw=2.6, color=F.RED, label=r"$H_2A$")
    ax.plot(ph, a1, lw=2.6, color=F.BLUE, label=r"$HA^-$")
    ax.plot(ph, a2, lw=2.6, color=F.GREEN, label=r"$A^{2-}$")
    ax.axvline(4.0, color=F.PURPLE, ls="--", lw=1.4)
    ax.axvline(8.0, color=F.PURPLE, ls="--", lw=1.4)
    ax.text(4.0, 1.03, r"$pK_{a1}=4$", ha="center", fontsize=10.5, color=F.PURPLE)
    ax.text(8.0, 1.03, r"$pK_{a2}=8$", ha="center", fontsize=10.5, color=F.PURPLE)
    ax.set(xlabel="pH", ylabel="物種分率", xlim=(1, 12), ylim=(0, 1.08), title=r"二質子酸 $H_2A$ 的物種分布（$K_{a1}=10^{-4}$、$K_{a2}=10^{-8}$）")
    F.clean_grid(ax)
    ax.legend(frameon=False, ncol=3, loc="upper center")
    fig.subplots_adjust(left=0.08, right=0.985, bottom=0.14, top=0.86)
    return _save(fig, "選化III-2-二質子酸物種分布.svg")


def fig_salt_hydrolysis():
    """計算四種代表鹽的 pH，驗證水解方向與酸鹼性。"""
    kw = 1.0e-14
    c0 = 0.10
    ka_acetic = 1.8e-5
    kb_ammonia = 1.8e-5
    oh_acetate = _weak_base_oh(kw / ka_acetic, c0)
    h_ammonium = _weak_acid_h(kw / kb_ammonia, c0)
    pka1_carbonic, pka2_carbonic = -np.log10(4.3e-7), -np.log10(5.6e-11)
    ph_bicarbonate = 0.5 * (pka1_carbonic + pka2_carbonic)
    ph = np.array([7.0, -np.log10(h_ammonium), 14 + np.log10(oh_acetate), ph_bicarbonate])
    assert ph[1] < 7 < ph[2]
    assert 8.2 < ph[3] < 8.5

    fig, ax = plt.subplots(figsize=(11.6, 5.7))
    labels = ["$NaCl$\n強酸＋強鹼", "$NH_4Cl$\n弱鹼的共軛酸", "$CH_3COONa$\n弱酸的共軛鹼", "$NaHCO_3$\n兩性陰離子"]
    colors = ["#64748b", F.RED, F.BLUE, F.GREEN]
    bars = ax.bar(labels, ph, color=colors, alpha=0.82)
    ax.axhline(7.0, color=F.INK, ls="--", lw=1.4)
    ax.text(3.42, 7.12, "25 °C 中性 pH", ha="right", fontsize=10)
    for bar, value in zip(bars, ph):
        ax.text(bar.get_x() + bar.get_width() / 2, value + 0.18, f"{value:.2f}", ha="center", fontsize=11)
    ax.set_ylim(4.2, 10.0)
    ax.set_ylabel("近似 pH（0.10 M）")
    ax.set_title("先判斷哪些離子與水反應，再用共軛常數計算", weight="bold")
    F.clean_grid(ax)
    fig.text(0.5, 0.03, r"$CH_3COO^-+H_2O\rightleftharpoons CH_3COOH+OH^-$；$NH_4^++H_2O\rightleftharpoons NH_3+H_3O^+$", ha="center", fontsize=11.5)
    fig.subplots_adjust(left=0.08, right=0.985, bottom=0.17, top=0.86)
    return _save(fig, "選化III-2-鹽類水解與pH.svg")


def fig_buffer_response():
    """以莫耳帳驗證等量醋酸/醋酸根緩衝液加入酸鹼後的 pH。"""
    ka = 1.8e-5
    pka = -np.log10(ka)
    n0 = 1.000
    delta = 0.020
    states = {
        "原緩衝液": (n0, n0),
        "加入 0.020 mol HCl": (n0 + delta, n0 - delta),
        "加入 0.020 mol NaOH": (n0 - delta, n0 + delta),
    }
    ph = np.array([pka + np.log10(base / acid) for acid, base in states.values()])
    assert np.isclose(ph[0], pka)
    assert ph[1] < ph[0] < ph[2]
    assert max(abs(ph - ph[0])) < 0.03

    fig, axes = plt.subplots(1, 2, figsize=(12.4, 5.5), gridspec_kw={"width_ratios": [1.25, 0.75]})
    ax = axes[0]
    x = np.arange(3)
    acid = [v[0] for v in states.values()]
    base = [v[1] for v in states.values()]
    width = 0.35
    acid_bars = ax.bar(
        x - width / 2,
        acid,
        width,
        color=F.RED,
        alpha=0.82,
        edgecolor=F.INK,
        linewidth=1.0,
        hatch="///",
        label=r"$CH_3COOH$",
    )
    base_bars = ax.bar(
        x + width / 2,
        base,
        width,
        color=F.BLUE,
        alpha=0.82,
        edgecolor=F.INK,
        linewidth=1.0,
        hatch="xx",
        label=r"$CH_3COO^-$",
    )
    assert all(bar.get_hatch() == "///" for bar in acid_bars)
    assert all(bar.get_hatch() == "xx" for bar in base_bars)
    ax.set_xticks(x, ["原液", "+HCl", "+NaOH"])
    ax.set_ylabel("反應後莫耳數 / mol")
    ax.set_ylim(0, 1.18)
    ax.set_title("先完成強酸／強鹼的計量反應")
    F.clean_grid(ax)
    ax.legend(frameon=False)

    ax = axes[1]
    colors = [F.PURPLE, F.RED, F.GREEN]
    ax.bar(np.arange(3), ph, color=colors, alpha=0.82)
    ax.set_xticks(np.arange(3), ["原液", "+HCl", "+NaOH"])
    ax.set_ylim(4.65, 4.83)
    ax.set_ylabel("pH")
    ax.set_title("再由共軛比求 pH")
    F.clean_grid(ax)
    for i, v in enumerate(ph):
        ax.text(i, v + 0.006, f"{v:.2f}", ha="center", fontsize=11)
    fig.suptitle(r"1.000 mol $CH_3COOH$ / 1.000 mol $CH_3COO^-$：少量強酸鹼改變的是共軛比", fontsize=15.5, y=0.985)
    fig.subplots_adjust(left=0.07, right=0.985, bottom=0.14, top=0.80, wspace=0.23)
    return _save(fig, "選化III-2-緩衝液加入酸鹼.svg")


def fig_buffer_capacity():
    """驗證 Henderson–Hasselbalch 比例與近似緩衝容量的峰值。"""
    pka = 4.76
    ka = 10 ** (-pka)
    ph = np.linspace(2.6, 6.9, 500)
    h = 10 ** (-ph)
    ratio = ka / h
    ctot = 0.20
    beta = 2.303 * ctot * ka * h / (ka + h) ** 2
    imax = int(np.argmax(beta))
    assert abs(ph[imax] - pka) < 0.01
    assert np.isclose(10 ** ((pka + 1) - pka), 10.0)

    fig, axes = plt.subplots(1, 2, figsize=(12.0, 5.4))
    ax = axes[0]
    ax.semilogy(ph, ratio, color=F.BLUE, lw=2.5)
    ax.axvspan(pka - 1, pka + 1, color=F.BLUE, alpha=0.10)
    ax.axvline(pka, color=F.PURPLE, ls="--", lw=1.4)
    ax.scatter([pka - 1, pka, pka + 1], [0.1, 1, 10], color=F.PURPLE, zorder=5)
    ax.set(xlabel="pH", ylabel=r"$[A^-]/[HA]$", title=r"$pH=pK_a+\log([A^-]/[HA])$")
    ax.set_xlim(2.6, 6.9)
    F.clean_grid(ax)
    ax.text(pka, 20, "有效範圍約為比例 0.1～10", ha="center", fontsize=10.5)

    ax = axes[1]
    ax.plot(ph, beta, color=F.GREEN, lw=2.5)
    ax.axvline(pka, color=F.PURPLE, ls="--", lw=1.4)
    ax.scatter([ph[imax]], [beta[imax]], color=F.PURPLE, s=60, zorder=5)
    ax.set(xlabel="pH", ylabel="近似緩衝容量 / (mol L$^{-1}$ pH$^{-1}$)", title="共軛對接近等量時容量最大")
    ax.set_xlim(2.6, 6.9)
    F.clean_grid(ax)
    fig.suptitle(r"醋酸／醋酸根緩衝系：目標 pH 決定比例，總濃度決定容量", fontsize=16, y=0.985)
    fig.subplots_adjust(left=0.08, right=0.985, bottom=0.14, top=0.82, wspace=0.23)
    return _save(fig, "選化III-2-緩衝比例與容量.svg")


def fig_titration_apparatus():
    """繪製可操作的滴定裝置並驗證 KHP 標定數據。"""
    mass_khp = 0.408
    molar_mass_khp = 204.0
    volume_naoh_l = 0.0200
    n_khp = mass_khp / molar_mass_khp
    c_naoh = n_khp / volume_naoh_l
    assert np.isclose(n_khp, 0.00200)
    assert np.isclose(c_naoh, 0.100)

    fig, axes = plt.subplots(1, 2, figsize=(12.4, 6.0), gridspec_kw={"width_ratios": [0.78, 1.22]})
    ax = axes[0]
    ax.axis("off")
    ax.set_xlim(0, 6)
    ax.set_ylim(0, 8)
    ax.plot([1.1, 1.1], [0.65, 7.5], color=F.INK, lw=3)
    ax.plot([0.35, 2.1], [0.65, 0.65], color=F.INK, lw=3)
    ax.plot([1.1, 3.8], [5.9, 5.9], color=F.INK, lw=2)
    ax.add_patch(Rectangle((3.35, 2.95), 0.48, 4.15, facecolor="#eef4ff", edgecolor=F.BLUE, lw=1.6))
    ax.add_patch(Rectangle((3.35, 4.15), 0.48, 2.95, facecolor="#b9dcff", edgecolor="none"))
    ax.text(4.10, 6.65, "已標定 NaOH\n滴定液", ha="left", va="center", fontsize=11, color=F.BLUE)
    ax.plot([3.59, 3.59], [2.45, 2.95], color=F.INK, lw=2)
    ax.plot([3.22, 3.95], [2.57, 2.57], color=F.INK, lw=2)
    ax.plot([3.59, 4.05], [2.57, 2.57], color=F.INK, lw=2)
    ax.plot([3.59, 3.59], [2.25, 2.45], color=F.BLUE, lw=1.6)
    ax.add_patch(Circle((3.59, 2.12), 0.055, facecolor=F.BLUE, edgecolor=F.BLUE))
    flask = Polygon([[2.65, 0.78], [4.45, 0.78], [4.00, 1.65], [3.82, 2.10], [3.36, 2.10], [3.18, 1.65]], closed=True, facecolor="#fff0f5", edgecolor=F.RED, lw=1.8)
    ax.add_patch(flask)
    ax.text(3.58, 1.18, "KHP 待測液\n＋酚酞", ha="center", va="center", fontsize=10.5)
    ax.text(3.58, 7.55, "滴定管保持垂直", ha="center", fontsize=12, weight="bold")
    ax.text(3.58, 0.26, "錐形瓶持續旋搖；近終點逐滴加入", ha="center", fontsize=10.5)

    ax = axes[1]
    ax.axis("off")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    _box(ax, (0.06, 0.72), 0.88, 0.18, r"$n_{KHP}=0.408/204=0.00200\ \mathrm{mol}$", face="#eef4ff", edge=F.BLUE, fs=14)
    _box(ax, (0.06, 0.49), 0.88, 0.18, r"$KHP+OH^-\rightarrow KP^-+H_2O$（1：1）", face="#eefbf2", edge=F.GREEN, fs=13.5)
    _box(ax, (0.06, 0.26), 0.88, 0.18, r"$C_{NaOH}=0.00200/0.0200=0.100\ \mathrm{M}$", face="#fff7dd", edge=F.AMBER, fs=14)
    ax.text(0.50, 0.17, "觀察：淡粉紅維持約 30 秒", ha="center", fontsize=11.5, color=F.RED)
    ax.text(0.50, 0.09, "推論：指示劑終點已落在當量點附近", ha="center", fontsize=11.5)
    fig.suptitle("酸鹼滴定：裝置、量測與標定數據形成同一條證據鏈", fontsize=16, y=0.985)
    fig.subplots_adjust(left=0.04, right=0.985, bottom=0.08, top=0.88, wspace=0.12)
    return _save(fig, "選化III-2-滴定裝置與數據.svg")


def _strong_acid_curve(vb_ml, ca=0.10, va_ml=25.0, cb=0.10):
    va = va_ml / 1000
    n0 = ca * va
    ph = np.empty_like(vb_ml, dtype=float)
    for i, vb in enumerate(vb_ml / 1000):
        noh = cb * vb
        vt = va + vb
        if abs(noh - n0) < 1e-12:
            ph[i] = 7.0
        elif noh < n0:
            ph[i] = -np.log10((n0 - noh) / vt)
        else:
            ph[i] = 14 + np.log10((noh - n0) / vt)
    return ph


def _weak_acid_curve(vb_ml, ca=0.10, va_ml=25.0, cb=0.10, ka=1.8e-5):
    va = va_ml / 1000
    n0 = ca * va
    veq = n0 / cb
    pka = -np.log10(ka)
    ph = np.empty_like(vb_ml, dtype=float)
    for i, vb_l in enumerate(vb_ml / 1000):
        noh = cb * vb_l
        vt = va + vb_l
        if vb_l == 0:
            ph[i] = -np.log10(_weak_acid_h(ka, ca))
        elif abs(vb_l - veq) < 1e-12:
            csalt = n0 / vt
            oh = _weak_base_oh(1e-14 / ka, csalt)
            ph[i] = 14 + np.log10(oh)
        elif vb_l < veq:
            ph[i] = pka + np.log10(noh / (n0 - noh))
        else:
            ph[i] = 14 + np.log10((noh - n0) / vt)
    return ph


def _weak_base_curve(va_added_ml, cb=0.10, vb0_ml=25.0, ca=0.10, kb=1.8e-5):
    vb0 = vb0_ml / 1000
    n0 = cb * vb0
    veq = n0 / ca
    pka = -np.log10(1e-14 / kb)
    ph = np.empty_like(va_added_ml, dtype=float)
    for i, va_l in enumerate(va_added_ml / 1000):
        nh = ca * va_l
        vt = vb0 + va_l
        if va_l == 0:
            oh = _weak_base_oh(kb, cb)
            ph[i] = 14 + np.log10(oh)
        elif abs(va_l - veq) < 1e-12:
            csalt = n0 / vt
            h = _weak_acid_h(1e-14 / kb, csalt)
            ph[i] = -np.log10(h)
        elif va_l < veq:
            ph[i] = pka + np.log10((n0 - nh) / nh)
        else:
            ph[i] = -np.log10((nh - n0) / vt)
    return ph


def fig_titration_curves():
    """數值生成強酸、弱酸、弱鹼三種滴定曲線並核對特徵點。"""
    volumes = np.linspace(0, 50, 501)
    hcl = _strong_acid_curve(volumes)
    hac = _weak_acid_curve(volumes)
    nh3 = _weak_base_curve(volumes)
    idx_half = int(np.argmin(abs(volumes - 12.5)))
    idx_eq = int(np.argmin(abs(volumes - 25.0)))
    assert np.isclose(hcl[idx_eq], 7.0)
    assert np.isclose(hac[idx_half], -np.log10(1.8e-5), atol=1e-10)
    assert hac[idx_eq] > 7.0 and nh3[idx_eq] < 7.0

    fig, axes = plt.subplots(1, 3, figsize=(13.2, 5.4), sharey=True)
    configs = [
        (axes[0], hcl, "NaOH 滴定 HCl", F.BLUE, [(4.2, 6.3, "甲基紅"), (8.2, 10.0, "酚酞")]),
        (axes[1], hac, r"NaOH 滴定 $CH_3COOH$", F.RED, [(8.2, 10.0, "酚酞")]),
        (axes[2], nh3, r"HCl 滴定 $NH_3$", F.GREEN, [(4.2, 6.3, "甲基紅")]),
    ]
    for ax, curve, title, color, ranges in configs:
        ax.plot(volumes, curve, color=color, lw=2.5)
        ax.axvline(25.0, color=F.INK, ls="--", lw=1.2)
        for lo, hi, label in ranges:
            ax.axhspan(lo, hi, color=F.AMBER, alpha=0.12)
            ax.text(49, (lo + hi) / 2, label, ha="right", va="center", fontsize=8.8, color=F.AMBER)
        ax.scatter([25.0], [curve[idx_eq]], color=F.PURPLE, s=45, zorder=5)
        ax.text(25.0, curve[idx_eq] + (0.45 if curve[idx_eq] < 10 else -0.8), f"當量點\npH {curve[idx_eq]:.2f}", ha="center", fontsize=9.2, color=F.PURPLE)
        ax.set(xlabel="滴定液體積 / mL", xlim=(0, 50), ylim=(0, 14), title=title)
        F.clean_grid(ax)
    axes[0].set_ylabel("pH")
    axes[1].scatter([12.5], [hac[idx_half]], color=F.BLUE, s=42, zorder=5)
    axes[1].text(12.5, hac[idx_half] + 0.45, r"半當量點 $pH=pK_a$", ha="center", fontsize=9.2, color=F.BLUE)
    fig.suptitle("同濃度、同體積樣品的三類滴定曲線：當量體積相同，當量點 pH 由生成物決定", fontsize=15.5, y=0.985)
    fig.subplots_adjust(left=0.055, right=0.992, bottom=0.14, top=0.82, wspace=0.10)
    return _save(fig, "選化III-2-三類滴定曲線.svg")


def fig_weak_acid_titration_regions():
    """以莫耳數追蹤弱酸滴定的五個計算區段。"""
    ca, va_ml, cb = 0.10, 25.0, 0.10
    n0_mmol = ca * va_ml
    volumes = np.linspace(0, 50, 401)
    noh_mmol = cb * volumes
    nha = np.maximum(n0_mmol - noh_mmol, 0)
    na = np.where(noh_mmol <= n0_mmol, noh_mmol, n0_mmol)
    excess = np.maximum(noh_mmol - n0_mmol, 0)
    assert np.allclose(nha + na, n0_mmol)
    assert np.isclose(nha[100], na[100])  # 12.5 mL
    assert np.isclose(nha[200], 0) and np.isclose(na[200], n0_mmol)

    fig, ax = plt.subplots(figsize=(11.8, 5.8))
    ax.plot(volumes, nha, color=F.RED, lw=2.5, label=r"剩餘 $HA$")
    ax.plot(volumes, na, color=F.BLUE, lw=2.5, label=r"生成 $A^-$")
    ax.plot(volumes, excess, color=F.GREEN, lw=2.5, label=r"過量 $OH^-$")
    for x, label in [(0, "起點\n弱酸平衡"), (12.5, "半當量\n共軛對等量"), (25, "當量點\n鹽類水解"), (40, "過量鹼\n剩餘 $OH^-$")]:
        ax.axvline(x, color=F.PURPLE, ls="--", lw=1.0)
        ax.text(x + 0.5, 4.65, label, ha="left", va="top", fontsize=9.5, color=F.PURPLE)
    ax.set(xlabel="加入 0.100 M NaOH 體積 / mL", ylabel="主要物種莫耳數 / mmol", xlim=(0, 50), ylim=(0, 5.0), title="0.100 M、25.0 mL 單質子弱酸的滴定物種帳")
    F.clean_grid(ax)
    ax.legend(frameon=False, ncol=3, loc="lower center")
    fig.text(0.5, 0.025, "每個區段先完成中和莫耳帳，再選弱酸、緩衝、水解或過量強鹼模型。", ha="center", fontsize=11.5)
    fig.subplots_adjust(left=0.08, right=0.985, bottom=0.16, top=0.86)
    return _save(fig, "選化III-2-弱酸滴定分區與物種.svg")


def main():
    fig_proton_transfer()
    fig_acid_strength_direction()
    fig_kw_temperature()
    fig_weak_acid_dissociation()
    fig_conjugate_ka_kb()
    fig_common_ion()
    fig_diprotic_distribution()
    fig_salt_hydrolysis()
    fig_buffer_response()
    fig_buffer_capacity()
    fig_titration_apparatus()
    fig_titration_curves()
    fig_weak_acid_titration_regions()


if __name__ == "__main__":
    main()
