# -*- coding: utf-8 -*-
"""產生「必物-6 量子現象」的圖，輸出到該章 sources/。
重繪：  .venv/bin/python _tools/fig_必物-6.py
"""

import os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import matplotlib.pyplot as plt
import figlib as F

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CH = os.path.join(ROOT, "物理", "物理一（必修物理）", "必物-6 量子現象")

h, c, k = 6.626e-34, 3.0e8, 1.381e-23


def fig_blackbody():
    fig, ax = F.canvas(7.0, 4.4)
    lam = np.linspace(60, 2000, 600) * 1e-9

    def planck(lam, T):
        return (2 * h * c**2 / lam**5) / (np.exp(h * c / (lam * k * T)) - 1)

    peak6000 = planck(np.array([4.8e-7]), 6000)[0]
    # 可見光帶
    ax.axvspan(380, 700, color="#ffe9b0", alpha=0.45, lw=0)
    ax.text(540, peak6000 * 1.02, "可見光", ha="center", color="#9a6700", fontsize=11)
    for T, col in [(4000, F.AMBER), (5000, F.RED), (6000, F.BLUE)]:
        ax.plot(lam * 1e9, planck(lam, T), color=col, lw=2.6, label=f"{T} K（量子論）")
    # 古典 Rayleigh–Jeans（5000K）→ 紫外災難
    rj = 2 * c * k * 5000 / lam**4
    ax.plot(lam * 1e9, rj, color="#6b7280", lw=2.2, ls="--", label="古典理論 (5000 K)")
    F.arrow(ax, (255, peak6000 * 0.60), (130, peak6000 * 1.05), color="#6b7280")
    ax.text(
        150,
        peak6000 * 0.46,
        "紫外災難\n（古典理論發散）",
        color="#6b7280",
        fontsize=11,
        va="center",
        ha="center",
    )
    ax.set_xlim(0, 2000)
    ax.set_ylim(0, peak6000 * 1.35)
    ax.set_xlabel("波長 $\\lambda$ (nm)")
    ax.set_ylabel("輻射強度（任意單位）")
    ax.set_yticks([])
    ax.set_title("黑體輻射：古典理論的破產")
    F.clean_grid(ax)
    ax.legend(loc="upper right", fontsize=10, frameon=False)
    F.save_to(fig, CH, "必物-6-黑體輻射")


def fig_photoelectric():
    fig, ax = F.canvas(6.6, 4.4)
    s = 0.4136  # hν(eV) = 0.4136 × ν(×10^14 Hz)
    nu = np.linspace(0, 12, 200)
    for W, nu0, col, name in [
        (2.0, 2.0 / s, F.BLUE, "金屬 A（$W=2.0$ eV）"),
        (2.9, 2.9 / s, F.RED, "金屬 B（$W=2.9$ eV）"),
    ]:
        ke = np.clip(s * nu - W, 0, None)
        ax.plot(nu, ke, color=col, lw=2.6, label=name)
        ax.plot(nu, s * nu - W, color=col, lw=1.2, ls=":")  # 延伸線
        ax.plot([nu0], [0], "o", color=col, ms=7)
    ax.axhline(0, color=F.INK, lw=1.0)
    ax.annotate(
        "遏止頻率 $\\nu_0$",
        xy=(2.0 / s, 0),
        xytext=(5.6, 0.5),
        color=F.BLUE,
        fontsize=11,
        arrowprops=dict(arrowstyle="->", color=F.BLUE),
    )
    ax.text(
        9.0, s * 9 - 2.0 + 0.15, "斜率 = $h$", color=F.BLUE, fontsize=12, rotation=20
    )
    ax.text(0.2, -2.4, "$y$ 軸截距 $= -W$（功函數）", color=F.INK, fontsize=11)
    ax.set_xlim(0, 12)
    ax.set_ylim(-3.2, 3.0)
    ax.set_xlabel("入射光頻率 $\\nu$（$\\times10^{14}$ Hz）")
    ax.set_ylabel("光電子最大動能 $K_{\\max}$ (eV)")
    ax.set_title("光電效應：$K_{\\max}=h\\nu-W$")
    F.clean_grid(ax)
    ax.legend(loc="upper left", fontsize=10, frameon=False)
    F.save_to(fig, CH, "必物-6-光電效應")


def fig_stopping_voltage():
    """光電效應實驗：光電流 I 對外加電壓 V 的關係，標出遏止電壓。
    左：兩種亮度（同頻率）→ 飽和電流不同，但遏止電壓相同。"""
    fig, ax = F.canvas(7.0, 4.4)
    Vs = -1.5  # 遏止電壓位置

    def curve(V, Isat):
        # V 從 -Vs 起電流由 0 升到飽和（簡化的平滑曲線）
        y = np.where(V <= Vs, 0.0, Isat * (1 - np.exp(-(V - Vs) / 0.9)))
        return y

    V = np.linspace(-2.5, 4.0, 400)
    ax.plot(V, curve(V, 2.0), color=F.BLUE, lw=2.6, label="較亮（光子數多）")
    ax.plot(V, curve(V, 1.1), color=F.RED, lw=2.6, label="較暗（同頻率）")
    ax.axhline(0, color=F.INK, lw=1.0)
    ax.axvline(0, color="#999", lw=0.9, ls=":")
    # 遏止電壓標記
    ax.plot([Vs], [0], "o", color=F.INK, ms=7)
    ax.annotate(
        "遏止電壓 $-V_s$\n（電流剛好歸零）",
        xy=(Vs, 0),
        xytext=(-2.4, 1.25),
        color=F.INK,
        fontsize=11,
        ha="left",
        arrowprops=dict(arrowstyle="->", color=F.INK),
    )
    ax.text(2.0, 2.12, "飽和電流", color=F.BLUE, fontsize=11, ha="center")
    ax.text(1.6, 0.78, "飽和電流較小", color=F.RED, fontsize=11, ha="center")
    ax.text(
        -2.4,
        2.35,
        "同頻率、不同亮度：遏止電壓相同（$K_{\\max}$ 不變），\n只有飽和電流（電子數目）不同",
        color="#555",
        fontsize=10,
        va="top",
    )
    ax.set_xlim(-2.5, 4.0)
    ax.set_ylim(-0.3, 2.7)
    ax.set_yticks([])
    ax.set_xticks([])
    ax.set_xlabel("外加電壓 $V$（反向 ← 0 → 正向）")
    ax.set_ylabel("光電流 $I$")
    ax.set_title("光電效應：光電流–電壓關係與遏止電壓")
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.legend(loc="lower right", fontsize=10, frameon=False)
    F.save_to(fig, CH, "必物-6-遏止電壓")


def fig_energy_levels():
    fig, ax = F.canvas(6.8, 5.2)
    levels = {1: -13.6, 2: -3.40, 3: -1.51, 4: -0.85, 5: -0.54}
    label_y = {1: -13.6, 2: -3.40, 3: -2.45, 4: -1.35, 5: -0.30}  # 高能階太擠→引線拉開
    for n, E in levels.items():
        ax.hlines(E, 0.10, 0.64, color=F.INK, lw=2.0)
        ly = label_y[n]
        if abs(ly - E) > 0.05:
            ax.plot([0.64, 0.70], [E, ly], color="#999", lw=0.8)
        ax.text(0.72, ly, f"$n={n}$", va="center", fontsize=12)
        if n <= 3:
            ax.text(
                0.07,
                E,
                f"{E:.2f} eV",
                va="center",
                ha="right",
                fontsize=10,
                color="#555",
            )
    ax.hlines(0, 0.10, 0.64, color=F.INK, lw=2.0, ls="--")
    ax.plot([0.64, 0.70], [0, 0.70], color="#999", lw=0.8)
    ax.text(0.72, 0.70, "$n=\\infty$（游離）", va="center", fontsize=11)

    def trans(n_hi, n_lo, x, col):
        F.arrow(
            ax,
            (x, levels.get(n_hi, 0)),
            (x, levels[n_lo]),
            color=col,
            lw=2.0,
            mutation=14,
        )

    # 來曼系（→ n=1，紫外）
    for n, x in [(2, 0.16), (3, 0.21), (4, 0.26)]:
        trans(n, 1, x, F.PURPLE)
    ax.text(0.21, -7.3, "來曼系\n（紫外）", ha="center", color=F.PURPLE, fontsize=11)
    # 巴耳末系（→ n=2，可見光）
    for n, x, col in [(3, 0.40, F.RED), (4, 0.45, "#17a2b8"), (5, 0.50, F.BLUE)]:
        trans(n, 2, x, col)
    ax.text(0.45, -4.6, "巴耳末系（可見光）", ha="center", color=F.INK, fontsize=11)
    ax.set_xlim(0, 1.12)
    ax.set_ylim(-14.5, 1.4)
    ax.set_xticks([])
    ax.set_ylabel("能量 $E$ (eV)")
    ax.set_title("氫原子能階與光譜系列（$E_n=-13.6/n^2$ eV）")
    for sname in ("top", "right", "bottom"):
        ax.spines[sname].set_visible(False)
    F.save_to(fig, CH, "必物-6-氫原子能階")


def fig_double_slit():
    rng = np.random.default_rng(7)
    xs = np.linspace(-1, 1, 2000)
    # 干涉條紋 × 單縫包絡
    inten = (np.cos(9 * np.pi * xs / 2) ** 2) * (np.sinc(xs / 0.45) ** 2)
    p = inten / inten.sum()
    fig, axes = plt.subplots(2, 2, figsize=(8.2, 5.0))
    for ax, N in zip(axes.ravel(), [40, 400, 4000, 40000]):
        x = rng.choice(xs, size=N, p=p)
        y = rng.uniform(0, 1, N)
        ax.scatter(x, y, s=2, c=F.INK, alpha=0.55, edgecolors="none", rasterized=True)
        ax.set_xlim(-1, 1)
        ax.set_ylim(0, 1)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_title(f"$N = {N:,}$ 個電子", fontsize=12)
        for sname in ("top", "right", "bottom", "left"):
            ax.spines[sname].set_color("#999")
    fig.suptitle("單電子雙狹縫：一個一個打，仍累積出干涉條紋", fontsize=13)
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    F.save_to(fig, CH, "必物-6-雙狹縫累積")


def fig_modes():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.4, 4.6))
    L = 1.0
    x = np.linspace(0, L, 400)
    for n in [1, 2, 3, 4, 5]:
        off = (5 - n) * 1.7
        ax1.hlines(off, 0, L, color="#d8dde3", lw=1.0)
        ax1.plot(x, off + 0.7 * np.sin(n * np.pi * x / L), color=F.BLUE, lw=2.2)
        ax1.text(-0.04, off, f"$n={n}$", ha="right", va="center", fontsize=12)
        ax1.text(
            L + 0.05,
            off,
            rf"$\lambda=2L/{n}$",
            ha="left",
            va="center",
            fontsize=10,
            color="#666",
        )
    ax1.axvline(0, color=F.INK, lw=2.5)
    ax1.axvline(L, color=F.INK, lw=2.5)
    ax1.set_xlim(-0.24, L + 0.34)
    ax1.set_ylim(-1.35, 4 * 1.7 + 1.1)
    ax1.axis("off")
    ax1.set_title("空腔裡的「振動模式」（1D 駐波示意）", fontsize=13)
    ax1.text(
        L / 2,
        -1.08,
        "只有「整數個半波長」剛好塞得進盒子",
        ha="center",
        color=F.INK,
        fontsize=11,
    )

    nu = np.linspace(0, 10, 200)
    N = nu**3
    ax2.plot(nu, N, color=F.RED, lw=2.8)
    ax2.fill_between(nu, 0, N, color=F.RED, alpha=0.08)
    ax2.set_xlim(0, 10)
    ax2.set_ylim(0, 1080)
    ax2.set_xticks([])
    ax2.set_yticks([])
    ax2.set_xlabel("頻率 ν（∝ 1/λ）→", fontsize=12)
    ax2.set_ylabel("模式總數（短於此波長）→", fontsize=12)
    ax2.set_title("波長越短，模式越多（3D 空腔，沒有上限）", fontsize=13)
    ax2.annotate(
        "短波長端\n模式急速暴增",
        xy=(9.2, 9.2**3),
        xytext=(2.0, 830),
        color=F.RED,
        fontsize=11,
        ha="center",
        arrowprops=dict(arrowstyle="->", color=F.RED),
    )
    for s in ("top", "right"):
        ax2.spines[s].set_visible(False)
    fig.tight_layout()
    F.save_to(fig, CH, "必物-6-振動模式")


def _wavelength_to_rgb(lam_nm):
    """把可見光波長 (nm) 轉成近似 RGB 顏色，用於畫連續光譜色帶。"""
    w = float(lam_nm)
    if w < 380 or w > 750:
        r = g = b = 0.0
    elif w < 440:
        r, g, b = -(w - 440) / (440 - 380), 0.0, 1.0
    elif w < 490:
        r, g, b = 0.0, (w - 440) / (490 - 440), 1.0
    elif w < 510:
        r, g, b = 0.0, 1.0, -(w - 510) / (510 - 490)
    elif w < 580:
        r, g, b = (w - 510) / (580 - 510), 1.0, 0.0
    elif w < 645:
        r, g, b = 1.0, -(w - 645) / (645 - 580), 0.0
    else:
        r, g, b = 1.0, 0.0, 0.0
    # 邊緣亮度衰減
    if w < 420:
        f = 0.3 + 0.7 * (w - 380) / (420 - 380)
    elif w > 700:
        f = 0.3 + 0.7 * (750 - w) / (750 - 700)
    else:
        f = 1.0
    return (r * f, g * f, b * f)


def fig_spectra():
    """發射光譜（黑底亮線）vs 吸收光譜（連續彩虹背景上的暗線）對照。
    亮線與暗線位置完全重合——同一組氫原子巴耳末系能階差。"""
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8.4, 4.0))

    lam_lo, lam_hi = 390.0, 700.0
    # 氫原子巴耳末系可見譜線（n→2）：Hα, Hβ, Hγ, Hδ
    lines = [
        (656.3, "H$\\alpha$"),
        (486.1, "H$\\beta$"),
        (434.0, "H$\\gamma$"),
        (410.2, "H$\\delta$"),
    ]
    line_w = 2.4  # 譜線視覺寬度 (nm)

    # ---- 上：發射光譜（黑底＋幾條亮線）----
    ax1.set_facecolor("black")
    ax1.set_xlim(lam_lo, lam_hi)
    ax1.set_ylim(0, 1)
    for lam, name in lines:
        ax1.axvspan(lam - line_w, lam + line_w, color=_wavelength_to_rgb(lam), lw=0)
        ax1.text(lam, 1.05, name, ha="center", va="bottom", fontsize=9, color=F.INK)
    ax1.set_yticks([])
    ax1.set_xticks([])
    ax1.text(
        lam_lo + 5,
        0.5,
        "發射光譜",
        color="white",
        fontsize=12,
        ha="left",
        va="center",
        fontweight="bold",
    )
    ax1.set_title("發射光譜（emission）：黑底上的亮線", fontsize=12, pad=20)

    # ---- 下：吸收光譜（連續彩虹背景＋幾條暗線）----
    grad = np.linspace(lam_lo, lam_hi, 600)
    band = np.array([_wavelength_to_rgb(w) for w in grad]).reshape(1, -1, 3)
    ax2.imshow(
        band,
        extent=[lam_lo, lam_hi, 0, 1],
        aspect="auto",
        origin="lower",
        interpolation="bilinear",
        zorder=0,
    )
    for lam, _ in lines:
        ax2.axvspan(lam - line_w, lam + line_w, color="black", lw=0, zorder=2)
    ax2.set_xlim(lam_lo, lam_hi)
    ax2.set_ylim(0, 1)
    ax2.set_yticks([])
    ax2.set_xlabel("波長 $\\lambda$ (nm)")
    ax2.text(
        lam_lo + 5,
        0.5,
        "吸收光譜",
        color="black",
        fontsize=12,
        ha="left",
        va="center",
        fontweight="bold",
    )
    ax2.set_title("吸收光譜（absorption）：連續彩虹背景上的暗線", fontsize=12, pad=4)

    for ax in (ax1, ax2):
        for s in ("top", "right", "bottom", "left"):
            ax.spines[s].set_visible(False)

    fig.text(
        0.5,
        0.49,
        "亮線與暗線位置完全重合（同一組能階差）",
        ha="center",
        va="center",
        fontsize=10,
        color=F.RED,
        bbox=dict(boxstyle="round,pad=0.25", fc="white", ec=F.RED, lw=1.0),
    )
    fig.tight_layout()
    fig.subplots_adjust(hspace=0.95)
    F.save_to(fig, CH, "必物-6-發射吸收光譜")


if __name__ == "__main__":
    fig_blackbody()
    fig_photoelectric()
    fig_stopping_voltage()
    fig_energy_levels()
    fig_double_slit()
    fig_modes()
    fig_spectra()
    print("done.")
