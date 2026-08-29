# -*- coding: utf-8 -*-
"""產生必物-6「量子現象」學生講義 SVG。

重繪：.venv/bin/python _tools/fig_content_必物-6.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Arc, Circle, FancyBboxPatch, Polygon, Rectangle

import figlib as F


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CH = os.path.join(ROOT, "content", "必修物理", "必物-6")

FIGURE_OUTPUTS = (
    ("fig_blackbody_quantization", "必物-6-黑體輻射與能量量子化.svg"),
    ("fig_photoelectric_apparatus", "必物-6-光電效應裝置與電流電壓.svg"),
    ("fig_photoelectric_controls", "必物-6-光電效應頻率與強度.svg"),
    ("fig_debroglie_diffraction", "必物-6-物質波尺度與電子繞射.svg"),
    ("fig_double_slit_accumulation", "必物-6-單電子雙狹縫累積.svg"),
    ("fig_spectrum_paths", "必物-6-連續吸收與發射光譜.svg"),
    ("fig_energy_level_transitions", "必物-6-能階躍遷與光譜線.svg"),
)


def _save(fig, name):
    return F.save_to(fig, CH, name, output_subdir="assets", write_pdf=False)


def _rounded(ax, xy, wh, text, fc="#f8fafc", ec=F.INK, fs=11.5):
    x, y = xy
    w, h = wh
    patch = FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.04,rounding_size=0.10",
        facecolor=fc, edgecolor=ec, lw=1.6,
    )
    ax.add_patch(patch)
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs)
    return patch


def fig_blackbody_quantization():
    """黑體頻譜的數值曲線與離散能量階梯。"""
    h = 6.62607015e-34
    c = 2.99792458e8
    k = 1.380649e-23
    b_wien = 2.897771955e-3
    wavelength_nm = np.linspace(250, 2600, 1800)
    wavelength_m = wavelength_nm * 1e-9

    def planck(temp):
        exponent = h * c / (wavelength_m * k * temp)
        return (2 * h * c**2 / wavelength_m**5) / np.expm1(exponent)

    temps = [3000, 4000, 5000]
    curves = [planck(t) for t in temps]
    norm = max(curve.max() for curve in curves)

    fig, axes = plt.subplots(1, 2, figsize=(11.8, 4.8))
    ax = axes[0]
    colors = [F.RED, F.AMBER, F.BLUE]
    for temp, curve, color in zip(temps, curves, colors):
        y = curve / norm
        ax.plot(wavelength_nm, y, color=color, lw=2.5, label=f"{temp} K")
        peak_i = int(np.argmax(curve))
        peak_nm = wavelength_nm[peak_i]
        expected_nm = b_wien / temp * 1e9
        ax.scatter([peak_nm], [y[peak_i]], s=38, color=color, zorder=5)
        ax.plot([peak_nm, peak_nm], [0, y[peak_i]], color=color, lw=1.0, ls="--")
        assert np.isclose(peak_nm, expected_nm, rtol=0.015)
    ax.set_xlim(250, 2600)
    ax.set_ylim(0, 1.08)
    ax.set_xlabel("波長 λ（nm）")
    ax.set_ylabel("頻譜輻射率（共同尺度）")
    F.clean_grid(ax)
    ax.legend(frameon=False, loc="upper right")
    ax.set_title("溫度升高：峰值增強並移向短波長", fontsize=14)

    ax = axes[1]
    ax.axis("off")
    ax.set_xlim(0, 10)
    ax.set_ylim(-0.4, 6.2)
    ax.text(2.2, 5.65, "古典連續能量", ha="center", fontsize=13, weight="bold")
    ax.add_patch(Rectangle((0.8, 0.55), 2.8, 4.45, facecolor="#e2e8f0", edgecolor=F.INK, lw=1.5))
    for y in np.linspace(0.8, 4.75, 22):
        ax.plot([0.9, 3.5], [y, y], color="#94a3b8", lw=0.75)
    ax.text(2.2, 2.75, "任意中間值\n皆可取", ha="center", va="center", fontsize=12)

    ax.text(7.25, 5.65, "量子化能量", ha="center", fontsize=13, weight="bold")
    for n in range(5):
        y = 0.8 + n * 0.95
        ax.plot([5.5, 8.9], [y, y], color=F.BLUE, lw=2.3)
        ax.text(9.1, y, f"E = {n}hf", va="center", fontsize=10.7, color=F.BLUE)
    F.arrow(ax, (6.2, 1.0), (6.2, 1.68), color=F.RED, lw=2.2, mutation=13)
    ax.text(6.45, 1.34, "一次改變 hf", va="center", fontsize=11.2, color=F.RED)
    ax.text(5.0, 0.05, "允許值相隔 hf；頻率愈高，每一份能量愈大", ha="center", fontsize=11.4)
    ax.set_title("普朗克以離散能量交換描述輻射", fontsize=14)
    fig.suptitle("黑體實驗促成能量量子化", fontsize=15.5, y=1.0)
    fig.tight_layout()
    _save(fig, "必物-6-黑體輻射與能量量子化")


def fig_photoelectric_apparatus():
    """光電管裝置、偏壓方向與可測得的 I-V 曲線。"""
    phi_ev = 2.0
    photon_ev = 3.1
    kmax_ev = photon_ev - phi_ev
    stopping_v = kmax_ev

    fig, axes = plt.subplots(1, 2, figsize=(11.9, 4.9))
    ax = axes[0]
    ax.axis("off")
    ax.set_aspect("equal")
    ax.set_xlim(-5.2, 5.2)
    ax.set_ylim(-3.3, 3.2)
    ax.add_patch(FancyBboxPatch((-2.65, -1.35), 5.3, 2.7,
                                boxstyle="round,pad=0.08,rounding_size=0.55",
                                facecolor="#f8fafc", edgecolor="#64748b", lw=2.0))
    ax.add_patch(Rectangle((-2.2, -0.9), 0.35, 1.8, facecolor="#94a3b8", edgecolor=F.INK, lw=1.5))
    ax.add_patch(Rectangle((1.85, -0.9), 0.35, 1.8, facecolor="#cbd5e1", edgecolor=F.INK, lw=1.5))
    ax.text(-2.03, 1.14, "發射極 E", ha="center", fontsize=11.5)
    ax.text(2.03, 1.14, "收集極 C", ha="center", fontsize=11.5)
    for y in (0.62, 0.22, -0.18, -0.58):
        F.arrow(ax, (-4.7, y + 0.8), (-2.35, y), color=F.PURPLE, lw=1.8, mutation=10)
    ax.text(-4.0, 2.35, "單色光", ha="center", color=F.PURPLE, fontsize=12, weight="bold")
    rng = np.random.default_rng(6)
    for y in rng.uniform(-0.55, 0.55, 7):
        start = (-1.65, float(y))
        end = (1.55, float(y + rng.normal(0, 0.18)))
        F.arrow(ax, start, end, color=F.BLUE, lw=1.4, mutation=8)
    ax.text(0.0, 0.98, "光電子", ha="center", color=F.BLUE, fontsize=11.5)
    ax.plot([-2.03, -2.03, -3.35, -3.35], [-1.38, -2.35, -2.35, -2.75], color=F.INK, lw=1.7)
    ax.plot([2.03, 2.03, 3.35, 3.35], [-1.38, -2.35, -2.35, -2.75], color=F.INK, lw=1.7)
    _rounded(ax, (-1.1, -3.05), (2.2, 0.75), "可變偏壓 V", fc="#fef3c7", ec=F.AMBER, fs=11.5)
    ax.plot([-3.35, -1.15], [-2.75, -2.68], color=F.INK, lw=1.7)
    ax.plot([1.15, 3.35], [-2.68, -2.75], color=F.INK, lw=1.7)
    ax.add_patch(Circle((3.35, -1.95), 0.42, facecolor="white", edgecolor=F.GREEN, lw=1.8))
    ax.text(3.35, -1.95, "A", ha="center", va="center", fontsize=12, color=F.GREEN, weight="bold")
    ax.text(0, 2.72, "改變偏壓，安培計量到收集的光電子流率", ha="center", fontsize=12.3, weight="bold")
    ax.set_title("光電效應的控制變因與觀測量", fontsize=14)

    ax = axes[1]
    voltage = np.linspace(-2.0, 3.0, 500)
    current = np.where(voltage <= -stopping_v, 0.0,
                       4.0 * (1.0 - np.exp(-(voltage + stopping_v) / 0.75)))
    current = np.clip(current, 0, 4.0)
    ax.plot(voltage, current, color=F.BLUE, lw=2.8)
    ax.axvline(-stopping_v, color=F.RED, lw=1.4, ls="--")
    ax.axhline(4.0, color=F.GREEN, lw=1.2, ls="--")
    ax.scatter([-stopping_v], [0], color=F.RED, s=42, zorder=5)
    ax.text(-stopping_v - 0.05, 0.35, f"遏止電壓\nVs = {stopping_v:.1f} V", ha="right", fontsize=10.7, color=F.RED)
    ax.text(1.25, 4.18, "飽和光電流", fontsize=10.8, color=F.GREEN)
    ax.set_xlim(-2.0, 3.0)
    ax.set_ylim(0, 4.7)
    ax.set_xlabel("收集極相對發射極的電壓 V（V）")
    ax.set_ylabel("光電流 I（示意刻度）")
    F.clean_grid(ax)
    ax.text(0.55, 1.0, "反向偏壓篩除\n動能較小的電子", fontsize=10.8, color="#475569")
    ax.set_title("I-V 圖把電子動能與數目分開量測", fontsize=14)
    assert np.isclose(kmax_ev, 1.1)
    assert np.isclose(stopping_v, kmax_ev)
    fig.tight_layout()
    _save(fig, "必物-6-光電效應裝置與電流電壓")


def fig_photoelectric_controls():
    """頻率控制單顆光子能量，強度控制光子通量。"""
    h_ev_s = 4.135667696e-15
    phi = 2.0
    f0 = phi / h_ev_s
    fig, axes = plt.subplots(1, 3, figsize=(12.6, 4.5))

    ax = axes[0]
    ax.axis("off")
    ax.set_xlim(0, 6)
    ax.set_ylim(0, 6)
    ax.add_patch(Rectangle((0.65, 0.7), 4.7, 0.55, facecolor="#94a3b8", edgecolor=F.INK, lw=1.4))
    ax.text(3.0, 0.35, "金屬表面，功函數 φ = 2.0 eV", ha="center", fontsize=10.8)
    for x in (1.45, 2.05, 2.65):
        F.arrow(ax, (x, 5.15), (x, 1.5), color=F.RED, lw=2.0, mutation=11)
    ax.text(2.05, 5.55, "紅光：每顆 1.65 eV", ha="center", color=F.RED, fontsize=11)
    ax.text(2.05, 2.25, "單顆能量低於 φ", ha="center", fontsize=10.5)
    for x in (4.05, 4.65):
        F.arrow(ax, (x, 5.15), (x, 1.5), color=F.PURPLE, lw=2.0, mutation=11)
    F.arrow(ax, (4.35, 1.15), (4.9, 3.15), color=F.BLUE, lw=2.3, mutation=13)
    ax.text(4.35, 5.55, "紫光：每顆 3.10 eV", ha="center", color=F.PURPLE, fontsize=11)
    ax.text(4.8, 3.45, "電子\n$K_{\\max}=1.10$ eV", ha="center", fontsize=10.5, color=F.BLUE)
    ax.set_title("一顆光子把能量交給一個電子", fontsize=13.5)

    ax = axes[1]
    freq = np.linspace(3.5e14, 1.05e15, 350)
    emitted = freq >= f0
    kmax = h_ev_s * freq[emitted] - phi
    ax.axvspan(3.5, f0 / 1e14, color="#e2e8f0", alpha=0.45)
    ax.plot(freq[emitted] / 1e14, kmax, color=F.BLUE, lw=2.8)
    ax.axvline(f0 / 1e14, color=F.RED, lw=1.4, ls="--")
    ax.text(f0 / 1e14 + 0.12, 2.15, f"底限 $f_0={f0/1e14:.2f}\\times10^{{14}}$ Hz", fontsize=10.2, color=F.RED)
    ax.text(4.12, 0.26, "未產生光電子", ha="center", fontsize=9.8, color="#64748b")
    ax.text(7.1, 1.25, "斜率 = h", fontsize=11.5, color=F.BLUE, rotation=24)
    ax.set_xlim(3.5, 10.5)
    ax.set_ylim(0, 2.6)
    ax.set_xlabel("入射光頻率 f（10¹⁴ Hz）")
    ax.set_ylabel("最大動能 $K_{\\max}$（eV）")
    F.clean_grid(ax)
    ax.set_title("頻率決定光電子最大動能", fontsize=13.5)

    ax = axes[2]
    ax.axis("off")
    ax.set_xlim(0, 6)
    ax.set_ylim(0, 6)
    for y, n, label, color in [(4.35, 4, "較弱", F.BLUE), (1.85, 9, "較強", F.GREEN)]:
        for i in range(n):
            x = 0.75 + (i % 5) * 0.62
            yy = y + (i // 5) * 0.55
            F.arrow(ax, (x, yy), (x + 0.45, yy), color=color, lw=1.5, mutation=7)
        ax.add_patch(Rectangle((4.1, y - 0.6), 0.35, 1.2, facecolor="#94a3b8", edgecolor=F.INK, lw=1.2))
        ax.text(5.0, y, f"{label}光\n光電子數較{'少' if n==4 else '多'}", ha="center", va="center", fontsize=10.7, color=color)
    ax.text(3.0, 0.45, "頻率固定：每顆光子能量相同", ha="center", fontsize=10.8)
    ax.set_title("強度決定每秒抵達的光子數", fontsize=13.5)
    assert np.isclose(f0, 4.83598e14, rtol=1e-4)
    assert np.isclose(3.1 - phi, 1.1)
    fig.tight_layout()
    _save(fig, "必物-6-光電效應頻率與強度")


def fig_debroglie_diffraction():
    """電子晶體繞射裝置與德布羅意尺度。"""
    h = 6.62607015e-34
    m_e = 9.1093837e-31
    v_e = 7.27e6
    p_e = m_e * v_e
    lambda_e = h / p_e
    p_ball = 0.050 * 40.0
    lambda_ball = h / p_ball

    fig, axes = plt.subplots(1, 2, figsize=(11.8, 4.9))
    ax = axes[0]
    ax.axis("off")
    ax.set_aspect("equal")
    ax.set_xlim(-5.4, 5.4)
    ax.set_ylim(-3.1, 3.2)
    _rounded(ax, (-4.9, -0.65), (1.55, 1.3), "電子槍", fc="#dbeafe", ec=F.BLUE, fs=12)
    for y in (-0.18, 0, 0.18):
        F.arrow(ax, (-3.25, y), (-1.0, y), color=F.BLUE, lw=1.8, mutation=10)
    ax.add_patch(Polygon([(-0.75, -1.35), (0.2, -0.85), (0.2, 0.85), (-0.75, 1.35)],
                         closed=True, facecolor="#e2e8f0", edgecolor=F.INK, lw=1.8))
    ax.text(-0.25, 1.65, "薄晶體", ha="center", fontsize=11.5)
    for angle in (-32, -18, 18, 32):
        rad = np.deg2rad(angle)
        F.arrow(ax, (0.25, 0), (3.5*np.cos(rad), 3.5*np.sin(rad)),
                color=F.PURPLE, lw=1.5, mutation=9)
    for radius in (0.65, 1.25, 1.85):
        ax.add_patch(Arc((4.2, 0), 0.55, 2*radius, theta1=80, theta2=280,
                         color=F.GREEN, lw=2.0))
    ax.plot([4.2, 4.2], [-2.35, 2.35], color=F.INK, lw=1.8)
    ax.text(4.35, 2.65, "偵測屏上的繞射環", ha="center", fontsize=11.5, color=F.GREEN)
    ax.text(0, -2.55, "晶格間距與電子波長相近時，散射波在特定方向相長", ha="center", fontsize=11.4)
    ax.set_title("電子晶體繞射：波動性的直接證據", fontsize=14)

    ax = axes[1]
    momentum = np.logspace(-25, 1, 400)
    wavelength = h / momentum
    ax.loglog(momentum, wavelength, color=F.BLUE, lw=2.7)
    ax.scatter([p_e], [lambda_e], s=65, color=F.RED, zorder=5)
    ax.scatter([p_ball], [lambda_ball], s=65, color=F.GREEN, zorder=5)
    ax.text(p_e*2.0, lambda_e*1.5, f"電子\nλ ≈ {lambda_e*1e9:.2f} nm", fontsize=10.7, color=F.RED)
    ax.text(p_ball/1e7, lambda_ball*18, f"棒球\nλ ≈ {lambda_ball:.1e} m", fontsize=10.7, color=F.GREEN)
    ax.axhspan(5e-11, 3e-10, color=F.AMBER, alpha=0.14)
    ax.text(2e-18, 1.45e-10, "晶格間距尺度", fontsize=10.5, color=F.AMBER)
    ax.set_xlabel("動量 p（kg·m/s）")
    ax.set_ylabel("德布羅意波長 λ（m）")
    F.clean_grid(ax)
    ax.set_title("λ = h/p：宏觀物體的波長極短", fontsize=14)
    assert np.isclose(lambda_e, 1.0e-10, rtol=0.01)
    assert np.isclose(lambda_ball, 3.313e-34, rtol=0.01)
    fig.tight_layout()
    _save(fig, "必物-6-物質波尺度與電子繞射")


def fig_double_slit_accumulation():
    """單電子落點累積成干涉機率分布。"""
    y_grid = np.linspace(-3.0, 3.0, 12000)
    density = np.exp(-(y_grid / 2.05)**2) * (0.10 + 0.90 * np.cos(np.pi * y_grid / 0.82)**2)
    density /= np.trapezoid(density, y_grid)
    cdf = np.cumsum(density)
    cdf /= cdf[-1]
    rng = np.random.default_rng(606)
    samples = np.interp(rng.random(5000), cdf, y_grid)

    fig, axes = plt.subplots(1, 4, figsize=(13.2, 4.5), gridspec_kw={"width_ratios": [1.25, 1, 1, 1]})
    ax = axes[0]
    ax.axis("off")
    ax.set_xlim(0, 7)
    ax.set_ylim(-3.4, 3.4)
    _rounded(ax, (0.25, -0.55), (1.45, 1.1), "電子槍", fc="#dbeafe", ec=F.BLUE, fs=11.5)
    F.arrow(ax, (1.8, 0), (3.0, 0), color=F.BLUE, lw=2.1, mutation=11)
    ax.plot([3.15, 3.15], [-3.0, -0.38], color=F.INK, lw=3)
    ax.plot([3.15, 3.15], [0.38, 3.0], color=F.INK, lw=3)
    ax.plot([3.15, 3.15], [-0.16, 0.16], color=F.INK, lw=3)
    ax.text(3.15, 3.18, "雙狹縫", ha="center", fontsize=10.8)
    for ys in (-0.27, 0.27):
        for yt in (-2.4, -1.2, 0, 1.2, 2.4):
            ax.plot([3.25, 6.05], [ys, yt], color=F.PURPLE, alpha=0.18, lw=0.8)
    ax.plot([6.15, 6.15], [-3.0, 3.0], color=F.INK, lw=2.2)
    ax.scatter([6.15], [samples[0]], s=35, color=F.RED, zorder=5)
    ax.text(6.35, samples[0], "一次偵測\n只留一點", va="center", fontsize=10.3, color=F.RED)
    ax.set_title("裝置與單次事件", fontsize=13.5)

    counts = [50, 500, 5000]
    for ax, n in zip(axes[1:], counts):
        ax.hist(samples[:n], bins=45, range=(-3, 3), orientation="horizontal",
                color=F.BLUE, alpha=0.72, edgecolor="white", lw=0.3)
        ax.plot(density * n * (6/45), y_grid, color=F.RED, lw=1.7)
        ax.set_ylim(-3, 3)
        ax.set_xticks([])
        ax.set_yticks([])
        for side in ("top", "right", "bottom", "left"):
            ax.spines[side].set_visible(False)
        ax.set_title(f"累積 N = {n}", fontsize=12.3)
        ax.set_xlabel("落點數", fontsize=10.5)
    fig.suptitle("每次偵測呈現粒子落點；大量落點依干涉機率分布累積", fontsize=15, y=0.99)
    assert density[np.argmin(np.abs(y_grid))] > density[np.argmin(np.abs(y_grid - 0.41))] * 5
    assert len(samples) == 5000 and np.all(np.abs(samples) <= 3.0)
    fig.tight_layout()
    _save(fig, "必物-6-單電子雙狹縫累積")


def _spectrum_strip(ax, x0, x1, y0, y1, kind, lines, line_colors=None):
    if kind in ("continuous", "absorption"):
        # 以向量矩形拼成色帶，避免 SVG 內嵌點陣影像。
        segments = 96
        # 橫軸由 400 nm（紫）排到 700 nm（紅）。
        cmap = plt.get_cmap("turbo")
        dx = (x1 - x0) / segments
        for index in range(segments):
            ax.add_patch(Rectangle(
                (x0 + index * dx, y0), dx * 1.02, y1 - y0,
                facecolor=cmap((index + 0.5) / segments), edgecolor="none",
            ))
        if kind == "absorption":
            for line in lines:
                x = x0 + (line - 400) / 300 * (x1 - x0)
                ax.add_patch(Rectangle((x - 0.025, y0), 0.05, y1-y0, facecolor=F.INK, edgecolor=F.INK))
    else:
        ax.add_patch(Rectangle((x0, y0), x1-x0, y1-y0, facecolor="#111827", edgecolor=F.INK, lw=1))
        colors = line_colors or [F.PURPLE, F.BLUE, F.GREEN, F.RED]
        assert len(colors) >= len(lines)
        for line, color in zip(lines, colors):
            x = x0 + (line - 400) / 300 * (x1 - x0)
            ax.add_patch(Rectangle((x - 0.035, y0), 0.07, y1-y0, facecolor=color, edgecolor=color))


def fig_spectrum_paths():
    """三類光譜的光路、光源條件與譜線位置。"""
    lines = np.array([430.0, 486.0, 546.0, 656.0])
    fig, ax = F.canvas(12.0, 6.2)
    ax.axis("off")
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 7.4)
    rows = [
        (5.55, "連續光譜", "高溫緻密光源", "continuous"),
        (3.35, "吸收光譜", "連續光穿過較低溫氣體", "absorption"),
        (1.15, "發射光譜", "高溫低密度氣體", "emission"),
    ]
    for y, title, source, kind in rows:
        _rounded(ax, (0.25, y-0.48), (2.15, 0.96), source, fc="#f8fafc", ec=F.BLUE, fs=10.7)
        if kind == "absorption":
            _rounded(ax, (2.8, y-0.40), (1.35, 0.80), "較低溫\n同種氣體", fc="#dcfce7", ec=F.GREEN, fs=10.2)
            F.arrow(ax, (2.45, y), (2.72, y), color=F.INK, lw=1.6, mutation=9)
            prism_x = 4.75
            F.arrow(ax, (4.2, y), (4.58, y), color=F.INK, lw=1.6, mutation=9)
        else:
            prism_x = 3.35
            F.arrow(ax, (2.45, y), (3.15, y), color=F.INK, lw=1.6, mutation=9)
        ax.add_patch(Polygon([(prism_x, y-0.5), (prism_x+0.75, y), (prism_x, y+0.5)],
                             closed=True, facecolor="#e0f2fe", edgecolor=F.BLUE, lw=1.4))
        F.arrow(ax, (prism_x+0.8, y), (6.15, y), color=F.INK, lw=1.6, mutation=9)
        _spectrum_strip(ax, 6.35, 11.3, y-0.43, y+0.43, kind, lines)
        ax.text(11.65, y, title, ha="center", va="center", rotation=90, fontsize=11.3, weight="bold")
    ax.text(8.82, 4.2, "同種原子的吸收暗線與發射亮線位置相同", ha="center", fontsize=11.6, weight="bold")
    ax.text(8.82, 0.35, "譜線位置由能階差決定，可作為元素指紋", ha="center", fontsize=11.3, color="#475569")
    normalized = (lines - 400) / 300
    assert np.all((normalized > 0) & (normalized < 1))
    assert len(np.unique(lines)) == 4
    ax.set_title("光源與中間介質決定觀察到的光譜型態", fontsize=15, pad=8)
    _save(fig, "必物-6-連續吸收與發射光譜")


def fig_energy_level_transitions():
    """離散能階、躍遷能量與對應譜線。"""
    levels = {1: -6.0, 2: -3.0, 3: -1.0, 4: -0.5}
    transitions = [(2, 1), (3, 2), (4, 2)]
    energies = [levels[hi] - levels[lo] for hi, lo in transitions]
    wavelengths = [1240.0 / energy for energy in energies]
    colors = [F.PURPLE, F.RED, F.BLUE]

    fig, axes = plt.subplots(1, 2, figsize=(11.9, 5.1))
    ax = axes[0]
    ax.set_xlim(0, 8)
    ax.set_ylim(-6.8, 0.5)
    for n, energy in levels.items():
        ax.plot([0.8, 7.2], [energy, energy], color=F.INK, lw=1.8)
        ax.text(0.55, energy, f"E{n}", ha="right", va="center", fontsize=11.5)
        ax.text(7.4, energy, f"{energy:.1f} eV", va="center", fontsize=10.8)
    x_positions = [2.0, 4.0, 6.0]
    for x, (hi, lo), energy, wavelength, color in zip(x_positions, transitions, energies, wavelengths, colors):
        F.arrow(ax, (x, levels[hi]-0.05), (x, levels[lo]+0.12), color=color, lw=2.4, mutation=14)
        ax.text(x+0.13, (levels[hi]+levels[lo])/2,
                f"ΔE = {energy:.1f} eV\nλ = {wavelength:.0f} nm",
                va="center", fontsize=10.2, color=color)
    ax.set_ylabel("原子能量（eV）")
    ax.set_xticks([])
    F.clean_grid(ax)
    ax.set_title("降階放光：光子能量等於能階差", fontsize=14)

    ax = axes[1]
    ax.axis("off")
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6.2)
    _rounded(ax, (0.35, 3.75), (2.55, 1.25), "吸收\n低能階 → 高能階", fc="#dbeafe", ec=F.BLUE, fs=11.5)
    _rounded(ax, (0.35, 1.15), (2.55, 1.25), "發射\n高能階 → 低能階", fc="#fee2e2", ec=F.RED, fs=11.5)
    F.arrow(ax, (3.05, 4.38), (4.15, 4.38), color=F.BLUE, lw=2.0, mutation=11)
    F.arrow(ax, (3.05, 1.78), (4.15, 1.78), color=F.RED, lw=2.0, mutation=11)
    _spectrum_strip(ax, 4.35, 9.55, 3.95, 4.81, "absorption", np.array(wavelengths))
    _spectrum_strip(
        ax, 4.35, 9.55, 1.35, 2.21, "emission", np.array(wavelengths),
        line_colors=colors,
    )
    ax.text(6.95, 5.35, "同一組 ΔE 產生同位置暗線與亮線", ha="center", fontsize=11.8, weight="bold")
    ax.text(6.95, 0.55, "hf = ΔE，且 λ = hc/ΔE", ha="center", fontsize=12.5, color=F.PURPLE)
    ax.set_title("能階結構把原子種類寫進光譜", fontsize=14)
    assert np.allclose(energies, [3.0, 2.0, 2.5])
    assert np.allclose(wavelengths, [413.333333, 620.0, 496.0], rtol=1e-6)
    fig.tight_layout()
    _save(fig, "必物-6-能階躍遷與光譜線")


def main():
    for function_name, _filename in FIGURE_OUTPUTS:
        globals()[function_name]()


if __name__ == "__main__":
    main()
