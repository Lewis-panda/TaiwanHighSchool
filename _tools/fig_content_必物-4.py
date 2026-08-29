# -*- coding: utf-8 -*-
"""產生必物-4「電與磁的統一」公開學生講義 SVG。

重繪：.venv/bin/python _tools/fig_content_必物-4.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Arc, Circle, FancyBboxPatch, Polygon, Rectangle

import figlib as F


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CH = os.path.join(ROOT, "content", "必修物理", "必物-4")

FIGURE_OUTPUTS = (
    ("fig_current_magnetic_fields", "必物-4-直導線與線圈磁場.svg"),
    ("fig_motor_force_pair", "必物-4-馬達線圈受力.svg"),
    ("fig_induction_lenz", "必物-4-電磁感應與冷次定律.svg"),
    ("fig_induction_applications", "必物-4-發電機與變壓器.svg"),
    ("fig_household_safety", "必物-4-家用電路與保護.svg"),
    ("fig_electromagnetic_wave", "必物-4-電磁波正交結構.svg"),
    ("fig_electromagnetic_spectrum", "必物-4-電磁波譜.svg"),
    ("fig_periodic_wave", "必物-4-週期波參數與質點運動.svg"),
    ("fig_reflection_refraction", "必物-4-反射與折射光路.svg"),
    ("fig_huygens_wavefronts", "必物-4-惠更斯波前.svg"),
    ("fig_interference_diffraction", "必物-4-干涉與繞射.svg"),
    ("fig_doppler_wavefronts", "必物-4-都卜勒波前.svg"),
)


def _save(fig, name):
    return F.save_to(fig, CH, name, output_subdir="assets", write_pdf=False)


def _arc_arrow(ax, center, radius, theta1, theta2, color=F.BLUE, lw=2.0):
    """畫弧線與終點切向箭頭，theta 以度為單位。"""
    ax.add_patch(
        Arc(
            center,
            2 * radius,
            2 * radius,
            theta1=theta1,
            theta2=theta2,
            color=color,
            lw=lw,
        )
    )
    angle = np.deg2rad(theta2)
    point = np.asarray(center) + radius * np.array([np.cos(angle), np.sin(angle)])
    tangent = np.array([-np.sin(angle), np.cos(angle)])
    if theta2 < theta1:
        tangent *= -1
    F.arrow(
        ax,
        point - 0.17 * tangent,
        point + 0.02 * tangent,
        color=color,
        lw=lw,
        mutation=12,
    )


def fig_current_magnetic_fields():
    """直導線與圓形線圈的電流、磁場方向對應。"""
    fig, axes = plt.subplots(1, 2, figsize=(11.2, 4.8))
    for ax in axes:
        ax.set_aspect("equal")
        ax.axis("off")

    ax = axes[0]
    center = np.array([0.0, 0.0])
    ax.add_patch(Circle(center, 0.23, facecolor="white", edgecolor=F.INK, lw=1.8))
    ax.add_patch(Circle(center, 0.065, facecolor=F.RED, edgecolor=F.RED))
    ax.text(0.0, -0.48, "電流 $I$ 穿出紙面", ha="center", fontsize=12)
    for r in (0.70, 1.18, 1.66):
        _arc_arrow(ax, center, r, 28, 330, color=F.BLUE, lw=2.0)
    point = np.array([1.18, 0.0])
    F.arrow(ax, point, point + np.array([0.0, 0.58]), color=F.GREEN, lw=2.8)
    ax.text(1.34, 0.48, "$B_P$", color=F.GREEN, fontsize=12)
    ax.text(1.28, -0.23, "$P$", fontsize=12)
    ax.text(0.0, 1.96, "直導線：磁場是同心圓", ha="center", fontsize=14, weight="bold")
    ax.text(0.0, -1.95, "拇指指電流，四指環繞指磁場", ha="center", fontsize=11.5, color="#64748b")
    ax.set_xlim(-2.15, 2.15)
    ax.set_ylim(-2.2, 2.25)

    ax = axes[1]
    coil_center = np.array([0.0, 0.0])
    radius = 1.35
    ax.add_patch(Circle(coil_center, radius, fill=False, edgecolor=F.INK, lw=3.0))
    for start, end in ((15, 108), (135, 228), (255, 348)):
        _arc_arrow(ax, coil_center, radius, start, end, color=F.RED, lw=2.8)
    ax.add_patch(Circle(coil_center, 0.18, facecolor="white", edgecolor=F.BLUE, lw=1.7))
    ax.add_patch(Circle(coil_center, 0.055, facecolor=F.BLUE, edgecolor=F.BLUE))
    ax.text(0.0, 0.31, "$B$ 穿出紙面", ha="center", color=F.BLUE, fontsize=12)
    ax.text(0.0, -0.33, "電流由紙面看為逆時針", ha="center", fontsize=11.5)
    ax.text(0.0, 1.96, "圓形線圈：四指順電流", ha="center", fontsize=14, weight="bold")
    ax.text(0.0, -1.95, "拇指指向線圈中心軸的磁場", ha="center", fontsize=11.5, color="#64748b")
    ax.set_xlim(-2.15, 2.15)
    ax.set_ylim(-2.2, 2.25)

    # 幾何檢查：P 在 +x 方向，逆時針切向為 +y。
    radial = point / np.linalg.norm(point)
    tangent = np.array([-radial[1], radial[0]])
    assert np.allclose(tangent, [0.0, 1.0])
    assert np.isclose(np.dot(radial, tangent), 0.0)

    fig.suptitle("安培右手定則：同一電流方向唯一決定磁場方向", fontsize=15, y=0.98)
    fig.subplots_adjust(left=0.03, right=0.97, top=0.86, bottom=0.04, wspace=0.10)
    _save(fig, "必物-4-直導線與線圈磁場")


def fig_motor_force_pair():
    """載流導線在匀強磁場中的受力與轉矩。"""
    fig, ax = F.canvas(10.8, 4.9)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_xlim(-5.2, 5.2)
    ax.set_ylim(-2.25, 2.25)

    # 外加磁場由 N 指向 S，也就是 +x。
    ax.add_patch(Rectangle((-4.85, -1.55), 0.72, 3.1, facecolor="#fee2e2", edgecolor=F.RED, lw=1.7))
    ax.add_patch(Rectangle((4.13, -1.55), 0.72, 3.1, facecolor="#dbeafe", edgecolor=F.BLUE, lw=1.7))
    ax.text(-4.49, 0.0, "N", ha="center", va="center", fontsize=22, weight="bold", color=F.RED)
    ax.text(4.49, 0.0, "S", ha="center", va="center", fontsize=22, weight="bold", color=F.BLUE)
    for y in (-1.0, -0.5, 0.0, 0.5, 1.0):
        F.arrow(ax, (-3.95, y), (3.95, y), color="#64748b", lw=1.3, mutation=10, z=1)
    ax.text(0.0, 1.35, "均勻磁場 $\\vec B$", ha="center", fontsize=12.5, color="#64748b")

    left = np.array([-1.45, 0.0])
    right = np.array([1.45, 0.0])
    ax.plot([left[0], right[0]], [1.15, 1.15], color=F.INK, lw=2.3)
    ax.plot([left[0], right[0]], [-1.15, -1.15], color=F.INK, lw=2.3)
    for point in (left, right):
        ax.add_patch(Circle(point, 0.28, facecolor="white", edgecolor=F.INK, lw=2.0, zorder=5))
    # 左邊電流入紙面，右邊電流出紙面。
    ax.plot([left[0] - 0.12, left[0] + 0.12], [left[1] - 0.12, left[1] + 0.12], color=F.RED, lw=2.3, zorder=6)
    ax.plot([left[0] - 0.12, left[0] + 0.12], [left[1] + 0.12, left[1] - 0.12], color=F.RED, lw=2.3, zorder=6)
    ax.add_patch(Circle(right, 0.075, facecolor=F.GREEN, edgecolor=F.GREEN, zorder=6))
    ax.text(left[0], -0.48, "$I$ 入紙面", ha="center", color=F.RED, fontsize=11.5)
    ax.text(right[0], -0.48, "$I$ 出紙面", ha="center", color=F.GREEN, fontsize=11.5)
    F.arrow(ax, left, left + np.array([0.0, -1.55]), color=F.PURPLE, lw=3.0, mutation=19)
    F.arrow(ax, right, right + np.array([0.0, 1.55]), color=F.PURPLE, lw=3.0, mutation=19)
    ax.text(left[0] - 0.18, -1.82, "$\\vec F$", color=F.PURPLE, fontsize=13)
    ax.text(right[0] + 0.12, 1.74, "$\\vec F$", color=F.PURPLE, fontsize=13)
    ax.add_patch(Arc((0.0, 0.0), 1.35, 1.35, theta1=-70, theta2=70, color=F.AMBER, lw=2.0))
    F.arrow(ax, (0.61, 0.45), (0.49, 0.61), color=F.AMBER, lw=2.0, mutation=13)
    ax.text(0.0, -1.93, "兩力大小相等、方向相反，作用線不同，因而產生轉動效果", ha="center", fontsize=11.7)

    current_in = np.array([0.0, 0.0, -1.0])
    current_out = np.array([0.0, 0.0, 1.0])
    field = np.array([1.0, 0.0, 0.0])
    assert np.allclose(np.cross(current_in, field), [0.0, -1.0, 0.0])
    assert np.allclose(np.cross(current_out, field), [0.0, 1.0, 0.0])
    ax.set_title("馬達的核心：磁場對線圈兩邊施以反向磁力", fontsize=15, pad=12)
    _save(fig, "必物-4-馬達線圈受力")


def _draw_bar_magnet(ax, center=(-2.15, 0.0), width=1.55, height=0.72):
    x, y = center
    ax.add_patch(Rectangle((x - width / 2, y - height / 2), width / 2, height, facecolor="#dbeafe", edgecolor=F.INK, lw=1.4))
    ax.add_patch(Rectangle((x, y - height / 2), width / 2, height, facecolor="#fee2e2", edgecolor=F.INK, lw=1.4))
    ax.text(x - width / 4, y, "S", ha="center", va="center", fontsize=13, color=F.BLUE, weight="bold")
    ax.text(x + width / 4, y, "N", ha="center", va="center", fontsize=13, color=F.RED, weight="bold")


def _draw_coil_side(ax, x=1.0, y=0.0, color=F.INK):
    for dx in (-0.18, -0.06, 0.06, 0.18):
        ax.add_patch(Arc((x + dx, y), 0.48, 1.62, theta1=85, theta2=275, color=color, lw=1.7))


def fig_induction_lenz():
    """用三個時間狀態分開磁通量變化與感應電流。"""
    fig, axes = plt.subplots(1, 3, figsize=(12.0, 4.5))
    states = [
        ("磁鐵靠近", "+", "向右磁通量增加", "感應磁場向左", "從磁棒側看：逆時針"),
        ("磁鐵靜止", "0", "磁通量不變", "感應電流為 0", "檢流計回到零點"),
        ("磁鐵遠離", "-", "向右磁通量減少", "感應磁場向右", "從磁棒側看：順時針"),
    ]
    for ax, (title, motion, flux_text, induced_text, current_text) in zip(axes, states):
        ax.set_aspect("equal")
        ax.axis("off")
        _draw_bar_magnet(ax)
        _draw_coil_side(ax)
        for y in (-0.22, 0.0, 0.22):
            F.arrow(ax, (-1.15, y), (0.55, y), color="#94a3b8", lw=1.2, mutation=9, z=1)
        if motion == "+":
            F.arrow(ax, (-2.15, 0.78), (-1.15, 0.78), color=F.GREEN, lw=2.6, mutation=16)
            F.arrow(ax, (0.65, -0.85), (-0.25, -0.85), color=F.PURPLE, lw=2.4, mutation=15)
        elif motion == "-":
            F.arrow(ax, (-1.15, 0.78), (-2.15, 0.78), color=F.GREEN, lw=2.6, mutation=16)
            F.arrow(ax, (-0.25, -0.85), (0.65, -0.85), color=F.PURPLE, lw=2.4, mutation=15)
        else:
            ax.text(-2.15, 0.78, "$v=0$", ha="center", va="center", color=F.GREEN, fontsize=11.8, weight="bold")
        ax.text(-0.45, 1.30, title, ha="center", fontsize=13.2, weight="bold")
        ax.text(-0.45, -1.27, flux_text, ha="center", fontsize=10.7)
        ax.text(-0.45, -1.58, induced_text, ha="center", fontsize=10.7, color=F.PURPLE)
        ax.text(-0.45, -1.89, current_text, ha="center", fontsize=10.5, color="#475569")
        ax.set_xlim(-3.05, 2.05)
        ax.set_ylim(-2.12, 1.62)

    # 朝右為外加磁場正向，增加時感應場朝左；減少時朝右。
    external = np.array([1.0, 0.0])
    induced_when_increasing = np.array([-1.0, 0.0])
    induced_when_decreasing = np.array([1.0, 0.0])
    assert np.dot(external, induced_when_increasing) < 0
    assert np.dot(external, induced_when_decreasing) > 0

    fig.suptitle("冷次定律：感應磁場抵抗「磁通量的變化」", fontsize=15, y=0.98)
    fig.subplots_adjust(left=0.02, right=0.98, top=0.86, bottom=0.04, wspace=0.03)
    _save(fig, "必物-4-電磁感應與冷次定律")


def fig_induction_applications():
    """發電機與變壓器的能量、磁場與電流鏈。"""
    fig, axes = plt.subplots(1, 2, figsize=(11.8, 4.9))
    for ax in axes:
        ax.set_aspect("equal")
        ax.axis("off")

    ax = axes[0]
    ax.add_patch(Rectangle((-2.25, -1.12), 0.72, 2.24, facecolor="#fee2e2", edgecolor=F.RED, lw=1.6))
    ax.add_patch(Rectangle((1.53, -1.12), 0.72, 2.24, facecolor="#dbeafe", edgecolor=F.BLUE, lw=1.6))
    ax.text(-1.89, 0, "N", fontsize=17, weight="bold", ha="center", color=F.RED)
    ax.text(1.89, 0, "S", fontsize=17, weight="bold", ha="center", color=F.BLUE)
    for y in (-0.55, 0.0, 0.55):
        F.arrow(ax, (-1.43, y), (1.43, y), color="#94a3b8", lw=1.3, mutation=9)
    loop = Polygon([(-0.72, -0.85), (0.72, -0.52), (0.72, 0.85), (-0.72, 0.52)], closed=True, fill=False, edgecolor=F.INK, lw=2.5)
    ax.add_patch(loop)
    ax.plot([-1.10, 1.10], [0.0, 0.0], color=F.INK, lw=1.6, ls="--")
    F.arrow(ax, (0.0, 1.25), (0.85, 1.12), color=F.GREEN, lw=2.4, mutation=15)
    ax.text(0.0, 1.63, "外力轉動線圈", ha="center", fontsize=12.5, weight="bold")
    ax.text(0.0, -1.55, "磁通量持續變化", ha="center", fontsize=11.5, color=F.PURPLE)
    ax.text(0.0, -1.90, "力學能 $\\rightarrow$ 電能", ha="center", fontsize=12.5, color=F.GREEN)
    ax.set_xlim(-2.65, 2.65)
    ax.set_ylim(-2.18, 2.02)
    ax.set_title("發電機", fontsize=14, pad=9)

    ax = axes[1]
    core = FancyBboxPatch((-1.72, -1.22), 3.44, 2.44, boxstyle="round,pad=0.05,rounding_size=0.13", facecolor="#e2e8f0", edgecolor="#64748b", lw=2.0)
    hole = Rectangle((-0.92, -0.62), 1.84, 1.24, facecolor="white", edgecolor="#64748b", lw=1.2)
    ax.add_patch(core)
    ax.add_patch(hole)
    for y in np.linspace(-0.82, 0.82, 7):
        ax.add_patch(Arc((-1.65, y), 0.55, 0.50, theta1=70, theta2=290, color=F.RED, lw=1.8))
    for y in np.linspace(-0.72, 0.72, 4):
        ax.add_patch(Arc((1.65, y), 0.55, 0.56, theta1=-110, theta2=110, color=F.BLUE, lw=1.8))
    F.arrow(ax, (-0.65, 0.88), (0.65, 0.88), color=F.PURPLE, lw=2.0, mutation=13)
    ax.text(0.0, 1.51, "交流 $I_p(t)$ 建立變動磁場", ha="center", fontsize=11.7)
    ax.text(-2.13, 0.0, "主線圈\n$N_p$", ha="center", va="center", fontsize=11.5, color=F.RED)
    ax.text(2.13, 0.0, "副線圈\n$N_s$", ha="center", va="center", fontsize=11.5, color=F.BLUE)
    ax.text(0.0, -1.62, "共用變動磁通量，副線圈感應交流電壓", ha="center", fontsize=11.2)
    ax.text(0.0, -1.96, r"$\dfrac{V_s}{V_p}\approx\dfrac{N_s}{N_p}$（理想變壓器）", ha="center", fontsize=12.3, color=F.PURPLE)
    ax.set_xlim(-2.7, 2.7)
    ax.set_ylim(-2.2, 2.02)
    ax.set_title("變壓器", fontsize=14, pad=9)

    fig.suptitle("電磁感應裝置都需要隨時間變化的磁通量", fontsize=15, y=0.99)
    fig.subplots_adjust(left=0.03, right=0.97, top=0.84, bottom=0.03, wspace=0.10)
    _save(fig, "必物-4-發電機與變壓器")


def fig_household_safety():
    """家用並聯電路的總電流、過電流保護與接地。"""
    fig, axes = plt.subplots(1, 2, figsize=(12.0, 4.9))
    for ax in axes:
        ax.axis("off")

    ax = axes[0]
    ax.set_xlim(-0.5, 8.4)
    ax.set_ylim(-0.3, 5.5)
    ax.plot([0.4, 7.8], [4.35, 4.35], color=F.RED, lw=2.4)
    ax.plot([0.4, 7.8], [0.75, 0.75], color=F.BLUE, lw=2.4)
    ax.text(0.35, 4.68, "火線", color=F.RED, fontsize=11.5)
    ax.text(0.35, 0.32, "中性線", color=F.BLUE, fontsize=11.5)
    ax.add_patch(Rectangle((1.05, 4.02), 1.25, 0.66, facecolor="#fef3c7", edgecolor=F.AMBER, lw=1.7))
    ax.text(1.68, 4.35, "15 A\n斷路器", ha="center", va="center", fontsize=10.5)
    for x, power, current in ((3.25, "880 W", "8 A"), (5.15, "660 W", "6 A"), (7.05, "440 W", "4 A")):
        ax.plot([x, x], [4.35, 3.45], color=F.INK, lw=1.7)
        ax.plot([x, x], [1.65, 0.75], color=F.INK, lw=1.7)
        ax.add_patch(FancyBboxPatch((x - 0.58, 1.65), 1.16, 1.80, boxstyle="round,pad=0.04", facecolor="#f8fafc", edgecolor="#64748b", lw=1.4))
        ax.text(x, 2.76, power, ha="center", fontsize=10.8)
        ax.text(x, 2.25, current, ha="center", fontsize=11.5, color=F.PURPLE, weight="bold")
        F.arrow(ax, (x - 0.22, 4.18), (x - 0.22, 3.60), color=F.GREEN, lw=1.6, mutation=10)
    total_current = 8 + 6 + 4
    assert total_current == 18
    ax.text(4.85, 5.08, r"$I_{\rm total}=8+6+4=18\ \mathrm{A}>15\ \mathrm{A}$", ha="center", fontsize=12.2, color=F.PURPLE)
    ax.text(4.85, -0.02, "並聯支路電流相加，斷路器在導線過熱前切斷", ha="center", fontsize=11.2)
    ax.set_title("過載保護", fontsize=14, pad=8)

    ax = axes[1]
    ax.set_xlim(-0.8, 7.8)
    ax.set_ylim(-0.4, 5.5)
    ax.add_patch(FancyBboxPatch((2.2, 1.55), 2.7, 2.3, boxstyle="round,pad=0.05", facecolor="#e2e8f0", edgecolor="#64748b", lw=1.7))
    ax.text(3.55, 3.55, "金屬外殼電器", ha="center", fontsize=12.5, weight="bold")
    ax.plot([0.1, 2.75], [4.65, 4.65], color=F.RED, lw=2.3)
    ax.text(0.05, 4.95, "火線", color=F.RED, fontsize=11.5)
    ax.plot([2.75, 3.25], [4.65, 3.85], color=F.RED, lw=2.0)
    ax.scatter([3.25], [3.85], s=70, color=F.RED, zorder=5)
    ax.text(3.95, 4.35, "絕緣破損\n火線碰外殼", ha="center", fontsize=10.6, color=F.RED)
    ax.plot([3.55, 3.55], [1.55, 0.72], color=F.GREEN, lw=2.5)
    ax.plot([3.55, 1.05], [0.72, 0.72], color=F.GREEN, lw=2.5)
    F.arrow(ax, (3.55, 1.37), (3.55, 0.88), color=F.GREEN, lw=2.5, mutation=14)
    ax.plot([1.05, 1.05], [0.72, 0.25], color=F.GREEN, lw=2.2)
    for y, w in ((0.25, 0.72), (0.02, 0.48), (-0.18, 0.26)):
        ax.plot([1.05 - w / 2, 1.05 + w / 2], [y, y], color=F.GREEN, lw=1.8)
    ax.text(2.12, 0.26, "低電阻接地路徑", ha="center", fontsize=11.2, color=F.GREEN)
    ax.add_patch(Rectangle((5.55, 2.03), 1.35, 1.22, facecolor="#fef3c7", edgecolor=F.AMBER, lw=1.6))
    ax.text(6.23, 2.64, "漏電\n斷路器", ha="center", va="center", fontsize=11.5)
    F.arrow(ax, (4.95, 2.64), (5.48, 2.64), color=F.AMBER, lw=2.0, mutation=12)
    ax.text(3.55, 1.10, "故障電流導向大地", ha="center", fontsize=11.1)
    ax.text(4.05, -0.18, "接地與漏電保護縮短人體承受危險電壓的時間", ha="center", fontsize=11.2)
    ax.set_title("漏電與接地", fontsize=14, pad=8)

    fig.suptitle("生活用電保護同時管理導線過熱與人體觸電", fontsize=15, y=0.99)
    fig.subplots_adjust(left=0.03, right=0.98, top=0.84, bottom=0.03, wspace=0.08)
    _save(fig, "必物-4-家用電路與保護")


def fig_electromagnetic_wave():
    """用同一相位的 E、B 樣本表示電磁橫波。"""
    wavelength = 4.0
    x = np.linspace(0.0, 8.0, 800)
    phase = 2 * np.pi * x / wavelength
    electric = np.sin(phase)
    magnetic = 0.68 * np.sin(phase)
    assert np.allclose(np.sign(electric[np.abs(electric) > 1e-6]), np.sign(magnetic[np.abs(magnetic) > 1e-6]))
    assert np.isclose(wavelength, x[np.argmin(np.abs(x - wavelength))], atol=0.02)

    fig, ax = F.canvas(11.3, 5.0)
    ax.axis("off")
    ax.set_xlim(-0.45, 9.25)
    ax.set_ylim(-2.55, 2.55)
    ax.plot(x, 1.05 + electric, color=F.RED, lw=2.7)
    ax.plot(x, -1.05 + magnetic, color=F.BLUE, lw=2.7)
    ax.plot([0, 8.75], [0, 0], color=F.INK, lw=1.5)
    F.arrow(ax, (7.85, 0.0), (8.75, 0.0), color=F.INK, lw=2.2, mutation=15)
    ax.text(8.78, -0.25, "傳播方向", ha="right", fontsize=11.5)
    ax.text(-0.25, 1.82, "$E_y$", color=F.RED, fontsize=14, weight="bold")
    ax.text(-0.25, -0.75, "$B_z$", color=F.BLUE, fontsize=14, weight="bold")
    ax.text(4.0, 2.24, "電場與磁場同相位振盪，並且都與傳播方向垂直", ha="center", fontsize=12.3)

    # 在整數倍 1/4 波長處加入方向標記。
    sample_x = np.arange(0.0, 8.01, 1.0)
    sample_values = np.sin(2 * np.pi * sample_x / wavelength)
    for sx, value in zip(sample_x, sample_values):
        if value > 0.5:
            F.arrow(ax, (sx, 1.05), (sx, 1.82), color=F.RED, lw=1.5, mutation=10)
            ax.add_patch(Circle((sx, -1.05), 0.07, color=F.BLUE))
        elif value < -0.5:
            F.arrow(ax, (sx, 1.05), (sx, 0.28), color=F.RED, lw=1.5, mutation=10)
            ax.plot([sx - 0.07, sx + 0.07], [-1.12, -0.98], color=F.BLUE, lw=1.5)
            ax.plot([sx - 0.07, sx + 0.07], [-0.98, -1.12], color=F.BLUE, lw=1.5)
    ax.text(4.0, -2.22, r"$\vec E\perp\vec B\perp\vec k$；真空中 $c=f\lambda\approx3.00\times10^8\ \mathrm{m/s}$", ha="center", fontsize=12.5)
    ax.set_title("電磁波的橫波結構", fontsize=15, pad=12)
    _save(fig, "必物-4-電磁波正交結構")


def fig_electromagnetic_spectrum():
    """對數頻率軸上的電磁波譜與兩個實例點。"""
    c = 3.00e8
    frequency_edges = np.array([1e5, 3e8, 3e11, 4e14, 7.5e14, 3e16, 3e19, 1e21])
    labels = ["無線電波", "微波", "紅外線", "可見光", "紫外線", "X 射線", "$\\gamma$ 射線"]
    colors = ["#dbeafe", "#bfdbfe", "#fecaca", "#fde68a", "#ddd6fe", "#c4b5fd", "#a78bfa"]
    assert np.all(np.diff(frequency_edges) > 0)
    wavelengths = c / frequency_edges
    assert np.all(np.diff(wavelengths) < 0)
    wifi_frequency = 2.4e9
    wifi_wavelength = c / wifi_frequency
    green_wavelength = 550e-9
    green_frequency = c / green_wavelength
    assert np.isclose(wifi_wavelength, 0.125)
    assert 5.4e14 < green_frequency < 5.5e14

    fig, ax = F.canvas(12.0, 4.8)
    ax.set_xscale("log")
    ax.set_xlim(frequency_edges[0], frequency_edges[-1])
    ax.set_ylim(0, 3.05)
    ax.set_yticks([])
    for side in ("left", "right", "top"):
        ax.spines[side].set_visible(False)
    for low, high, label, color in zip(frequency_edges[:-1], frequency_edges[1:], labels, colors):
        ax.axvspan(low, high, ymin=0.32, ymax=0.78, color=color, ec="#64748b", lw=0.7)
        center = np.sqrt(low * high)
        rotation = 90 if label == "可見光" else 0
        ax.text(center, 1.68, label, ha="center", va="center", fontsize=10.5, rotation=rotation)
    ax.set_xlabel("頻率 $f$ (Hz) 由左向右增加", labelpad=10)
    ax.text(1.15e5, 2.75, "波長 $\\lambda=c/f$ 由左向右減少", fontsize=12.2, ha="left")
    ax.scatter([wifi_frequency], [0.62], s=75, color=F.RED, edgecolors="white", zorder=5)
    ax.text(wifi_frequency, 0.25, "Wi-Fi 2.4 GHz\n$\\lambda=0.125$ m", ha="center", fontsize=10.1, color=F.RED)
    ax.scatter([green_frequency], [2.50], s=75, color=F.GREEN, edgecolors="white", zorder=5)
    ax.text(green_frequency, 2.88, "550 nm 綠光", ha="center", fontsize=10.4, color=F.GREEN)
    ax.text(2e16, 0.20, "高頻端的 X、$\\gamma$ 射線屬於游離輻射主要區域", ha="center", fontsize=10.8, color=F.PURPLE)
    ax.set_title("電磁波譜：各波段共用同一個 $c=f\\lambda$", fontsize=15, pad=14)
    fig.subplots_adjust(left=0.07, right=0.98, top=0.83, bottom=0.19)
    _save(fig, "必物-4-電磁波譜")


def fig_periodic_wave():
    """週期波的 A、lambda 與右行波質點運動方向。"""
    amplitude = 2.0
    wavelength = 4.0
    x = np.linspace(0.0, 8.0, 600)
    y = amplitude * np.sin(2 * np.pi * x / wavelength)
    p_x = 2.0
    p_y = amplitude * np.sin(2 * np.pi * p_x / wavelength)
    slope_at_p = amplitude * (2 * np.pi / wavelength) * np.cos(2 * np.pi * p_x / wavelength)
    vertical_velocity_sign = -np.sign(slope_at_p)
    assert np.isclose(p_y, 0.0, atol=1e-12)
    assert slope_at_p < 0
    assert vertical_velocity_sign > 0

    fig, ax = F.canvas(11.4, 5.0)
    ax.plot(x, y, color=F.BLUE, lw=2.8)
    ax.axhline(0, color=F.INK, lw=1.2)
    F.arrow(ax, (6.80, 2.45), (7.75, 2.45), color=F.GREEN, lw=2.5, mutation=15)
    ax.text(7.28, 2.72, "波形向右", ha="center", fontsize=11.7, color=F.GREEN)

    # 振幅
    ax.annotate("", xy=(1.0, amplitude), xytext=(1.0, 0), arrowprops=dict(arrowstyle="<->", color=F.RED, lw=1.8))
    ax.text(0.70, amplitude / 2, "$A=2.0$ cm", color=F.RED, fontsize=11.5, ha="right")
    # 波長：相鄰波峰 x=1 與 x=5。
    ax.annotate("", xy=(5.0, 2.10), xytext=(1.0, 2.10), arrowprops=dict(arrowstyle="<->", color=F.PURPLE, lw=1.8))
    ax.text(3.0, 2.32, "$\\lambda=4.0$ m", color=F.PURPLE, fontsize=11.5, ha="center")
    ax.scatter([p_x], [p_y], s=70, color=F.AMBER, edgecolors="white", zorder=6)
    F.arrow(ax, (p_x, p_y), (p_x, 1.28), color=F.AMBER, lw=2.6, mutation=16)
    ax.text(p_x + 0.18, 0.82, "質點 $P$\n此刻向上", color=F.AMBER, fontsize=11.2)
    ax.text(5.65, -2.35, "右行波：質點運動方向與當地波形斜率相反", ha="center", fontsize=11.5)
    ax.text(0.25, -2.35, "媒質質點上下振動", ha="left", fontsize=11.5, color="#64748b")
    ax.set_xlim(-0.15, 8.20)
    ax.set_ylim(-2.75, 3.05)
    ax.set_xlabel("位置 $x$ (m)")
    ax.set_ylabel("位移 $y$ (cm)")
    F.clean_grid(ax)
    ax.set_title("波形傳播能量，媒質質點在平衡位置附近振動", fontsize=15, pad=12)
    fig.subplots_adjust(left=0.09, right=0.98, top=0.84, bottom=0.15)
    _save(fig, "必物-4-週期波參數與質點運動")


def fig_reflection_refraction():
    """由司乃耳定律數值產生反射與折射光路。"""
    n1 = 1.00
    n2 = 1.50
    theta_i = np.deg2rad(45.0)
    theta_r = theta_i
    theta_t = np.arcsin(n1 * np.sin(theta_i) / n2)
    assert np.isclose(np.rad2deg(theta_t), 28.1255057, atol=1e-5)
    assert theta_t < theta_i
    assert np.isclose(n1 * np.sin(theta_i), n2 * np.sin(theta_t))

    origin = np.array([0.0, 0.0])
    incident_start = origin + 3.5 * np.array([-np.sin(theta_i), np.cos(theta_i)])
    reflected_end = origin + 3.1 * np.array([np.sin(theta_r), np.cos(theta_r)])
    transmitted_end = origin + 3.5 * np.array([np.sin(theta_t), -np.cos(theta_t)])
    incident_direction = (origin - incident_start) / np.linalg.norm(origin - incident_start)
    transmitted_direction = transmitted_end / np.linalg.norm(transmitted_end)

    fig, ax = F.canvas(10.6, 5.3)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.add_patch(Rectangle((-4.4, 0), 8.8, 3.4, facecolor="#f8fafc", edgecolor="none"))
    ax.add_patch(Rectangle((-4.4, -3.2), 8.8, 3.2, facecolor="#dbeafe", edgecolor="none"))
    ax.plot([-4.4, 4.4], [0, 0], color=F.INK, lw=1.7)
    ax.plot([0, 0], [-3.0, 3.0], color="#64748b", lw=1.2, ls="--")
    F.arrow(ax, incident_start, origin, color=F.RED, lw=3.0, mutation=18)
    F.arrow(ax, origin, reflected_end, color=F.GREEN, lw=3.0, mutation=18)
    F.arrow(ax, origin, transmitted_end, color=F.BLUE, lw=3.0, mutation=18)
    ax.text(-3.85, 2.75, "介質 1：$n_1=1.00$", fontsize=12)
    ax.text(-3.85, -2.80, "介質 2：$n_2=1.50$", fontsize=12)
    ax.text(-2.02, 2.10, "入射光", color=F.RED, fontsize=12)
    ax.text(1.70, 2.05, "反射光", color=F.GREEN, fontsize=12)
    ax.text(1.70, -2.05, "折射光", color=F.BLUE, fontsize=12)
    F.angle_arc(ax, origin, 0.82, 90, 135, color=F.RED, text=r"$45^\circ$")
    F.angle_arc(ax, origin, 1.12, 45, 90, color=F.GREEN, text=r"$45^\circ$")
    F.angle_arc(ax, origin, 0.90, 270, 270 + np.rad2deg(theta_t), color=F.BLUE, text=r"$28.1^\circ$")

    # 先異於光線的短線表示波前，會自動與光線垂直。
    for base, direction, color in (
        (incident_start + 0.85 * (origin - incident_start), incident_direction, F.RED),
        (0.58 * transmitted_end, transmitted_direction, F.BLUE),
    ):
        normal = np.array([-direction[1], direction[0]])
        assert np.isclose(np.dot(direction, normal), 0.0)
        for shift in (-0.38, 0.0, 0.38):
            point = base + shift * direction
            p1 = point - 0.38 * normal
            p2 = point + 0.38 * normal
            ax.plot([p1[0], p2[0]], [p1[1], p2[1]], color=color, lw=1.0, alpha=0.65)
    ax.text(3.92, -2.76, r"$n_1\sin\theta_i=n_2\sin\theta_t$", ha="right", fontsize=12.5, color=F.PURPLE)
    ax.text(3.92, -3.08, "進入慢介質：波速、波長減少，頻率不變", ha="right", fontsize=10.8)
    ax.set_xlim(-4.4, 4.4)
    ax.set_ylim(-3.25, 3.35)
    ax.set_title("反射角等於入射角；折射角由兩介質波速決定", fontsize=15, pad=12)
    _save(fig, "必物-4-反射與折射光路")


def fig_huygens_wavefronts():
    """用等半徑子波包絡線作出新波前。"""
    dt = 1.0
    speed = 1.35
    radius = speed * dt
    source_y = np.linspace(-2.0, 2.0, 7)
    assert np.isclose(radius, 1.35)

    fig, ax = F.canvas(11.0, 5.0)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_xlim(-1.15, 6.9)
    ax.set_ylim(-2.75, 2.75)
    ax.plot([0, 0], [-2.30, 2.30], color=F.BLUE, lw=2.7)
    ax.text(-0.18, 2.48, "舊波前", ha="right", fontsize=12.5, color=F.BLUE)
    for sy in source_y:
        ax.add_patch(Circle((0.0, sy), 0.055, color=F.BLUE, zorder=5))
        ax.add_patch(Arc((0.0, sy), 2 * radius, 2 * radius, theta1=-90, theta2=90, color="#94a3b8", lw=1.2))
    ax.plot([radius, radius], [-2.30, 2.30], color=F.RED, lw=2.7)
    ax.text(radius + 0.18, 2.48, "新波前", ha="left", fontsize=12.5, color=F.RED)
    F.arrow(ax, (0.0, -2.48), (radius, -2.48), color=F.GREEN, lw=2.2, mutation=14)
    ax.text(radius / 2, -2.68, "$v\\Delta t$", ha="center", fontsize=12, color=F.GREEN)

    ax.add_patch(FancyBboxPatch((2.25, -1.82), 4.20, 3.64, boxstyle="round,pad=0.16,rounding_size=0.15", facecolor="#f8fafc", edgecolor="#cbd5e1", lw=1.5))
    ax.text(4.35, 1.36, "惠更斯建構", ha="center", fontsize=14, weight="bold")
    statements = [
        "1. 舊波前上每一點成為子波源",
        "2. 同一 $\\Delta t$ 內，每個子波半徑皆為 $v\\Delta t$",
        "3. 子波的前方包絡線就是新波前",
        "4. 傳播方向始終與波前垂直",
    ]
    for y, text in zip((0.78, 0.18, -0.42, -1.02), statements):
        ax.text(2.58, y, text, ha="left", va="center", fontsize=11.4)
    ax.set_title("惠更斯原理用子波的包絡線預測下一時刻的波前", fontsize=15, pad=12)
    _save(fig, "必物-4-惠更斯波前")


def fig_interference_diffraction():
    """以雙狹縫中央亮紋與單狹縫子波表示疊加。"""
    fig, axes = plt.subplots(1, 2, figsize=(12.0, 5.0))
    for ax in axes:
        ax.set_aspect("equal")
        ax.axis("off")

    ax = axes[0]
    slit_x = 0.0
    screen_x = 4.6
    d = 1.20
    s1 = np.array([slit_x, d / 2])
    s2 = np.array([slit_x, -d / 2])
    p0 = np.array([screen_x, 0.0])
    r1 = np.linalg.norm(p0 - s1)
    r2 = np.linalg.norm(p0 - s2)
    assert np.isclose(r1, r2)
    assert np.isclose(abs(r1 - r2), 0.0)
    ax.plot([slit_x, slit_x], [-2.25, -0.86], color=F.INK, lw=4.0)
    ax.plot([slit_x, slit_x], [-0.34, 0.34], color=F.INK, lw=4.0)
    ax.plot([slit_x, slit_x], [0.86, 2.25], color=F.INK, lw=4.0)
    ax.plot([screen_x, screen_x], [-2.25, 2.25], color="#64748b", lw=2.0)
    ax.scatter([s1[0], s2[0]], [s1[1], s2[1]], s=55, color=F.RED, zorder=5)
    ax.text(-0.20, s1[1], "$S_1$", ha="right", fontsize=11.5)
    ax.text(-0.20, s2[1], "$S_2$", ha="right", fontsize=11.5)
    ax.plot([s1[0], p0[0]], [s1[1], p0[1]], color=F.BLUE, lw=1.6)
    ax.plot([s2[0], p0[0]], [s2[1], p0[1]], color=F.GREEN, lw=1.6)
    ax.scatter([p0[0]], [p0[1]], s=75, color=F.AMBER, edgecolors="white", zorder=6)
    ax.text(p0[0] + 0.16, p0[1], "$P_0$", fontsize=11.5, color=F.AMBER)
    for y in np.linspace(-1.65, 1.65, 9):
        width = 0.30 if abs(y) < 0.15 else 0.16
        color = F.AMBER if abs(y) < 0.15 else "#cbd5e1"
        ax.add_patch(Rectangle((screen_x - 0.06, y - width / 2), 0.12, width, color=color, ec="none"))
    ax.text(2.30, -2.05, r"中央點：$r_1=r_2$，$\Delta r=0$，建設性干涉", ha="center", fontsize=11.2)
    ax.text(2.30, 2.40, "雙狹縫干涉", ha="center", fontsize=13.7, weight="bold")
    ax.set_xlim(-0.85, 5.35)
    ax.set_ylim(-2.55, 2.65)

    ax = axes[1]
    slit_x = 0.0
    slit_half = 0.42
    ax.plot([slit_x, slit_x], [-2.25, -slit_half], color=F.INK, lw=4.0)
    ax.plot([slit_x, slit_x], [slit_half, 2.25], color=F.INK, lw=4.0)
    source_y = np.linspace(-slit_half, slit_half, 7)
    radii = (0.75, 1.45, 2.15, 2.85)
    for sy in source_y:
        ax.add_patch(Circle((slit_x, sy), 0.045, color=F.BLUE, zorder=5))
    for radius in radii:
        ax.add_patch(Arc((slit_x, 0.0), 2 * radius, 2 * radius, theta1=-75, theta2=75, color=F.RED, lw=1.7))
    F.arrow(ax, (-2.45, 0.0), (-0.20, 0.0), color=F.BLUE, lw=2.4, mutation=14)
    for x in (-2.2, -1.55, -0.90):
        ax.plot([x, x], [-1.45, 1.45], color=F.BLUE, lw=1.2)
    ax.text(1.62, -2.02, "狹縫寬度與波長同量級時，新波前向後方廣泛擴展", ha="center", fontsize=11.1)
    ax.text(0.35, 2.40, "單狹縫繞射", ha="center", fontsize=13.7, weight="bold")
    ax.set_xlim(-2.75, 3.35)
    ax.set_ylim(-2.55, 2.65)

    fig.suptitle("干涉由路徑差決定疊加；繞射來自狹縫內各子波的擴展與疊加", fontsize=14.6, y=0.99)
    fig.subplots_adjust(left=0.02, right=0.98, top=0.86, bottom=0.03, wspace=0.08)
    _save(fig, "必物-4-干涉與繞射")


def fig_doppler_wavefronts():
    """使用等時間發波模型驗證移動波源前後波長。"""
    wave_speed = 1.0
    source_speed = 0.30
    emission_times = np.arange(0.0, 4.0, 1.0)
    observation_time = 4.0
    centers = source_speed * emission_times
    radii = wave_speed * (observation_time - emission_times)
    front_positions = centers + radii
    back_positions = centers - radii
    front_spacing = abs(np.diff(front_positions)[0])
    back_spacing = abs(np.diff(back_positions)[0])
    assert np.allclose(abs(np.diff(front_positions)), wave_speed - source_speed)
    assert np.allclose(abs(np.diff(back_positions)), wave_speed + source_speed)
    assert np.isclose(front_spacing, 0.70)
    assert np.isclose(back_spacing, 1.30)

    fig, ax = F.canvas(11.8, 5.0)
    ax.set_aspect("equal")
    ax.axis("off")
    for center, radius in zip(centers, radii):
        ax.add_patch(Circle((center, 0.0), radius, fill=False, edgecolor=F.BLUE, lw=1.45, alpha=0.78))
        ax.add_patch(Circle((center, 0.0), 0.055, color="#94a3b8", zorder=4))
    source_now = source_speed * observation_time
    ax.add_patch(FancyBboxPatch((source_now - 0.35, -0.24), 0.70, 0.48, boxstyle="round,pad=0.03", facecolor="#fee2e2", edgecolor=F.RED, lw=1.5, zorder=6))
    ax.text(source_now, 0.0, "S", ha="center", va="center", fontsize=13, color=F.RED, weight="bold", zorder=7)
    F.arrow(ax, (source_now - 0.25, 0.55), (source_now + 0.90, 0.55), color=F.GREEN, lw=2.5, mutation=15)
    ax.text(source_now + 0.30, 0.84, "$v_s=0.30v$", ha="center", fontsize=11.5, color=F.GREEN)
    ax.scatter([-4.65, 4.65], [0, 0], s=85, color=F.AMBER, zorder=6)
    ax.text(-4.65, -0.38, "後方觀察者", ha="center", fontsize=11.2)
    ax.text(4.65, -0.38, "前方觀察者", ha="center", fontsize=11.2)
    ax.annotate("", xy=(front_positions[-2], -2.0), xytext=(front_positions[-1], -2.0), arrowprops=dict(arrowstyle="<->", color=F.RED, lw=1.8))
    ax.text(np.mean(front_positions[-2:]), -2.27, r"$\lambda_{\rm front}=0.70\,vT$", ha="center", fontsize=11.3, color=F.RED)
    ax.annotate("", xy=(back_positions[1], -1.38), xytext=(back_positions[0], -1.38), arrowprops=dict(arrowstyle="<->", color=F.PURPLE, lw=1.8))
    ax.text(np.mean(back_positions[:2]), -1.66, r"$\lambda_{\rm back}=1.30\,vT$", ha="center", fontsize=11.3, color=F.PURPLE)
    ax.text(0.0, 2.40, "波源每隔相同的 $T$ 發出一個波前，中心依次向右移動", ha="center", fontsize=12.1)
    ax.text(0.0, -2.80, "前方波長較短、頻率較高；後方波長較長、頻率較低", ha="center", fontsize=12.3)
    ax.set_xlim(-5.25, 5.25)
    ax.set_ylim(-3.05, 2.78)
    ax.set_title("移動波源的都卜勒效應", fontsize=15, pad=12)
    _save(fig, "必物-4-都卜勒波前")


def main():
    fig_current_magnetic_fields()
    fig_motor_force_pair()
    fig_induction_lenz()
    fig_induction_applications()
    fig_household_safety()
    fig_electromagnetic_wave()
    fig_electromagnetic_spectrum()
    fig_periodic_wave()
    fig_reflection_refraction()
    fig_huygens_wavefronts()
    fig_interference_diffraction()
    fig_doppler_wavefronts()


if __name__ == "__main__":
    main()
