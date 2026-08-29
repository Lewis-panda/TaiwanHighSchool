# -*- coding: utf-8 -*-
"""產生選物 I-1～I-3 公開學生講義的概念 SVG。

重繪：.venv/bin/python _tools/fig_content_選物I-1_3.py

輸出固定寫入各章 ``content/選修物理I/選物I-*/assets``，只產生 SVG。
"""

import os
import sys
import tempfile

os.environ.setdefault("MPLCONFIGDIR", os.path.join(tempfile.gettempdir(), "highschool-fig-cache"))

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyBboxPatch, Rectangle

import figlib as F


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COURSE = os.path.join(ROOT, "content", "選修物理I")


def _save(fig, chapter, name):
    return F.save_to(
        fig,
        os.path.join(COURSE, chapter),
        name,
        output_subdir="assets",
        write_pdf=False,
    )


def _card(ax, xy, width, height, text, *, edge="#94a3b8", face="#ffffff", fs=12):
    x, y = xy
    ax.add_patch(
        FancyBboxPatch(
            (x, y),
            width,
            height,
            boxstyle="round,pad=0.06,rounding_size=0.08",
            facecolor=face,
            edgecolor=edge,
            lw=1.4,
        )
    )
    ax.text(x + width / 2, y + height / 2, text, ha="center", va="center", fontsize=fs)


def fig_resolution_interval():
    """最小刻度、讀值區間與 B 類標準不確定度。"""
    fig, ax = F.schematic(11.8, 5.1)
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 5.2)
    ax.set_aspect("auto")

    ax.text(6, 4.88, "最小刻度決定讀值區間", ha="center", fontsize=16, weight="bold")
    ax.add_patch(Rectangle((0.65, 2.85), 10.7, 1.45, facecolor="#f8fafc", edgecolor="#cbd5e1", lw=1.4))

    x0, step, y0 = 1.15, 0.86, 3.35
    ax.plot([x0, x0 + 10 * step], [y0, y0], color=F.INK, lw=2.0)
    for i in range(11):
        height = 0.42 if i % 5 else 0.62
        ax.plot([x0 + i * step, x0 + i * step], [y0, y0 + height], color=F.INK, lw=1.5)
    for i, label in [(0, "1.0"), (5, "1.5"), (10, "2.0")]:
        ax.text(x0 + i * step, 3.05, label, ha="center", fontsize=11)
    ax.text(10.25, 3.05, "cm", fontsize=11)

    measured = x0 + 4 * step
    half = step / 2
    ax.add_patch(Rectangle((measured - half, 3.23), 2 * half, 0.95, facecolor="#dbeafe", edgecolor="none", alpha=0.9))
    ax.plot([measured, measured], [3.18, 4.28], color=F.RED, lw=2.5)
    ax.text(measured, 4.43, r"顯示值 $X=1.40\ \mathrm{cm}$", ha="center", fontsize=12.5, color=F.RED)
    ax.text(measured - half, 2.72, "1.35", ha="center", fontsize=10.5, color=F.BLUE)
    ax.text(measured + half, 2.72, "1.45", ha="center", fontsize=10.5, color=F.BLUE)
    ax.annotate("", xy=(measured + half, 2.86), xytext=(measured - half, 2.86), arrowprops=dict(arrowstyle="<->", color=F.BLUE, lw=1.8))
    ax.text(measured, 2.50, r"寬度 $d=0.10\ \mathrm{cm}$", ha="center", fontsize=11.5, color=F.BLUE)

    _card(ax, (0.70, 0.48), 3.15, 1.25, "① 找最小刻度\n" + r"$d=0.10\ \mathrm{cm}$", edge=F.BLUE, face="#eff6ff")
    _card(ax, (4.43, 0.48), 3.15, 1.25, "② 讀值區間\n" + r"$X\pm d/2$", edge=F.PURPLE, face="#f5f3ff")
    _card(ax, (8.15, 0.48), 3.15, 1.25, "③ 均勻分布換算\n" + r"$u_B=d/(2\sqrt{3})$", edge=F.GREEN, face="#f0fdf4")
    F.arrow(ax, (3.90, 1.10), (4.33, 1.10), color="#64748b", lw=1.6, mutation=14)
    F.arrow(ax, (7.63, 1.10), (8.05, 1.10), color="#64748b", lw=1.6, mutation=14)
    ax.text(6, 0.12, r"本例：$u_B=0.10/(2\sqrt{3})\approx0.029\ \mathrm{cm}$", ha="center", fontsize=12)

    fig.subplots_adjust(left=0.025, right=0.975, top=0.98, bottom=0.02)
    _save(fig, "選物I-1", "選物I-1-解析度與讀值區間")


def fig_motion_graph_reading():
    """用同一組等加速度資料連結三張運動圖的斜率與帶號面積。"""
    acceleration = 0.8
    t_mark = 2.5
    time = np.linspace(0.0, 4.0, 401)
    position = 0.5 * acceleration * time**2
    velocity = acceleration * time
    position_mark = 0.5 * acceleration * t_mark**2
    velocity_mark = acceleration * t_mark
    mask = time <= t_mark

    assert np.isclose(velocity_mark, acceleration * t_mark)
    assert np.isclose(position_mark, 0.5 * acceleration * t_mark**2)
    assert np.isclose(np.trapezoid(velocity[mask], time[mask]), position_mark)
    assert np.isclose(np.trapezoid(np.full(mask.sum(), acceleration), time[mask]), velocity_mark)

    fig, axes = plt.subplots(1, 3, figsize=(12.0, 4.5))
    x_ax, v_ax, a_ax = axes

    x_ax.plot(time, position, color=F.BLUE, lw=2.8)
    tangent = position_mark + velocity_mark * (time - t_mark)
    tangent_mask = (time >= 1.3) & (time <= 3.5)
    x_ax.plot(time[tangent_mask], tangent[tangent_mask], color=F.GREEN, lw=2.2)
    x_ax.scatter([t_mark], [position_mark], s=65, color=F.GREEN, edgecolors="white", zorder=5)
    x_ax.text(t_mark + 0.15, position_mark + 0.65, rf"切線斜率 $v={velocity_mark:g}$", color=F.GREEN, fontsize=11)
    x_ax.set_title(r"$x$–$t$：切線斜率是 $v$")
    x_ax.set_ylabel("x (m)")

    v_ax.plot(time, velocity, color=F.RED, lw=2.8)
    v_ax.fill_between(time[mask], 0, velocity[mask], color=F.BLUE, alpha=0.18)
    v_ax.scatter([t_mark], [velocity_mark], s=65, color=F.RED, edgecolors="white", zorder=5)
    v_ax.text(0.30, 1.13, rf"面積 $\Delta x={position_mark:g}\ \mathrm{{m}}$", color=F.BLUE, fontsize=11)
    v_ax.text(2.05, 2.72, rf"斜率 $a={acceleration:g}$", color=F.RED, fontsize=11)
    v_ax.set_title(r"$v$–$t$：斜率是 $a$，面積是 $\Delta x$")
    v_ax.set_ylabel("v (m/s)")

    a_ax.plot(time, np.full_like(time, acceleration), color=F.GREEN, lw=2.8)
    a_ax.fill_between(time[mask], 0, acceleration, color=F.GREEN, alpha=0.18)
    a_ax.text(0.35, 0.40, rf"面積 $\Delta v={velocity_mark:g}\ \mathrm{{m/s}}$", color=F.GREEN, fontsize=11)
    a_ax.set_title(r"$a$–$t$：面積是 $\Delta v$")
    a_ax.set_ylabel("a (m/s²)")

    for ax in axes:
        ax.axvline(t_mark, color="#94a3b8", lw=1.0, ls="--")
        ax.set_xlim(0, 4)
        ax.set_xlabel("t (s)")
        F.clean_grid(ax)
    a_ax.set_ylim(0, 1.15)
    fig.suptitle(r"同一運動：$x=0.4t^2$、$v=0.8t$、$a=0.8$", fontsize=16, y=0.99)
    fig.subplots_adjust(left=0.065, right=0.985, top=0.82, bottom=0.15, wspace=0.34)
    _save(fig, "選物I-2", "選物I-2-圖像讀法")


def fig_equal_time_graphs():
    """同一等加速度運動在位置點與 x-t、v-t、a-t 圖的對照。"""
    fig = plt.figure(figsize=(11.8, 6.4))
    gs = fig.add_gridspec(2, 3, height_ratios=[0.75, 1.45], hspace=0.48, wspace=0.35)
    strip = fig.add_subplot(gs[0, :])
    axes = [fig.add_subplot(gs[1, i]) for i in range(3)]

    strip.set_xlim(-0.5, 9.0)
    strip.set_ylim(-0.9, 1.15)
    strip.axis("off")
    strip.set_title(r"由靜止出發、$a=+1\ \mathrm{m/s^2}$；每隔 $1\ \mathrm{s}$ 取樣", fontsize=14, pad=8)
    strip.annotate("+x", xy=(8.75, 0), xytext=(8.15, 0), arrowprops=dict(arrowstyle="-|>", color=F.INK, lw=1.6), va="center")
    positions = 0.5 * np.arange(5, dtype=float) ** 2
    strip.plot(positions, np.zeros_like(positions), color="#94a3b8", lw=2)
    strip.scatter(positions, np.zeros_like(positions), s=85, color=F.BLUE, edgecolors="white", linewidths=1.0, zorder=4)
    for t, x in enumerate(positions):
        strip.text(x, 0.28, rf"$t={t}$", ha="center", fontsize=10.5)
        strip.text(x, -0.32, rf"${x:g}$ m", ha="center", fontsize=10.5, color=F.BLUE)
    mids = (positions[:-1] + positions[1:]) / 2
    for mid, dx in zip(mids, np.diff(positions)):
        strip.text(mid, -0.72, rf"$\Delta x={dx:g}$", ha="center", fontsize=9.5, color=F.PURPLE)

    t = np.linspace(0, 4, 200)
    series = [0.5 * t**2, t, np.ones_like(t)]
    point_series = [0.5 * np.arange(5) ** 2, np.arange(5), np.ones(5)]
    titles = [r"$x$–$t$：$x=\frac{1}{2}t^2$", r"$v$–$t$：$v=t$", r"$a$–$t$：$a=+1$"]
    ylabels = ["x (m)", "v (m/s)", "a (m/s²)"]
    colors = [F.BLUE, F.GREEN, F.RED]
    for ax, values, points, title, ylabel, color in zip(axes, series, point_series, titles, ylabels, colors):
        ax.plot(t, values, color=color, lw=2.7)
        ax.scatter(np.arange(5), points, s=45, color=color, edgecolors="white", linewidths=0.8, zorder=4)
        for sample in range(5):
            ax.axvline(sample, color="#e2e8f0", lw=0.8, zorder=0)
        ax.set_xlim(0, 4.15)
        ax.set_xticks(range(5))
        ax.set_xlabel("t (s)")
        ax.set_ylabel(ylabel)
        ax.set_title(title, fontsize=12.5)
        F.clean_grid(ax)
    axes[2].set_ylim(0, 1.5)

    fig.suptitle("等時間位置點與三種運動圖描述同一組資料", fontsize=16, y=0.995)
    fig.subplots_adjust(left=0.065, right=0.97, top=0.90, bottom=0.10)
    _save(fig, "選物I-2", "選物I-2-等時間點與運動圖")


def _vertical_sign_panel(ax, *, up_positive):
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis("off")
    sign_a = "−g" if up_positive else "+g"
    ax.set_title(f"{'向上' if up_positive else '向下'}為正：a = {sign_a}", fontsize=14, pad=10)

    if up_positive:
        F.arrow(ax, (1.8, 1.4), (1.8, 8.9), color=F.BLUE, lw=2.4, mutation=17)
        ax.text(1.45, 8.9, "+y", color=F.BLUE, fontsize=12, ha="right")
        signs = [("上升", "v > 0"), ("最高點", "v = 0"), ("下降", "v < 0")]
    else:
        F.arrow(ax, (1.8, 8.9), (1.8, 1.4), color=F.BLUE, lw=2.4, mutation=17)
        ax.text(1.45, 1.2, "+y", color=F.BLUE, fontsize=12, ha="right")
        signs = [("上升", "v < 0"), ("最高點", "v = 0"), ("下降", "v > 0")]

    levels = [2.4, 7.9, 5.0]
    ax.plot([4.0, 4.0], [2.0, 8.2], color="#94a3b8", lw=3.0)
    for (label, sign), y in zip(signs, levels):
        ax.scatter([4.0], [y], s=95, color=F.INK, zorder=4)
        ax.text(4.7, y, f"{label}：{sign}", va="center", fontsize=12.5)
    F.arrow(ax, (3.05, 6.3), (3.05, 3.9), color=F.RED, lw=2.8, mutation=18)
    ax.text(2.75, 5.1, f"a = {sign_a}", color=F.RED, fontsize=12, ha="right", va="center")


def fig_freefall_sign():
    """同一鉛直運動採兩種正方向時的符號對照。"""
    fig, axes = plt.subplots(1, 2, figsize=(11.8, 5.2))
    for ax, flag in zip(axes, [True, False]):
        _vertical_sign_panel(ax, up_positive=flag)
        ax.add_patch(FancyBboxPatch((0.35, 0.6), 9.3, 8.8, boxstyle="round,pad=0.08", fill=False, edgecolor="#cbd5e1", lw=1.3))
    fig.suptitle("同一段鉛直運動：正方向改變，符號隨之改變", fontsize=16, y=0.99)
    fig.text(0.5, 0.035, "最高點只有速度瞬間為零；重力加速度全程向下。", ha="center", fontsize=12.5)
    fig.subplots_adjust(left=0.035, right=0.975, top=0.88, bottom=0.10, wspace=0.12)
    _save(fig, "選物I-2", "選物I-2-自由落體正方向")


def fig_relative_velocity():
    """以位置序列與間距函數呈現一維追及的相對速度。"""
    x_a0, x_b0 = 0.0, 70.0
    v_a, v_b = 25.0, 18.0
    times = np.array([0.0, 5.0, 10.0])
    x_a = x_a0 + v_a * times
    x_b = x_b0 + v_b * times
    gaps = x_b - x_a
    relative_velocity = v_b - v_a

    assert np.allclose(gaps, (x_b0 - x_a0) + relative_velocity * times)
    assert np.allclose(gaps, [70.0, 35.0, 0.0])
    assert np.isclose(np.diff(gaps)[0] / np.diff(times)[0], relative_velocity)

    fig, (sequence, graph) = plt.subplots(
        1,
        2,
        figsize=(12.0, 5.0),
        gridspec_kw={"width_ratios": [1.45, 0.80]},
    )
    sequence.set_xlim(-12, 270)
    sequence.set_ylim(-0.65, 2.65)
    sequence.axis("off")
    for row, (t, xa, xb, gap) in enumerate(zip(times, x_a, x_b, gaps)):
        y = 2.0 - row
        sequence.plot([-5, 262], [y, y], color="#cbd5e1", lw=2.0)
        sequence.scatter([xa], [y], s=175, marker="s", color=F.BLUE, edgecolors="white", zorder=5)
        sequence.scatter([xb], [y], s=175, marker="s", color=F.RED, edgecolors="white", zorder=5)
        sequence.text(-10, y, rf"$t={t:g}\ \mathrm{{s}}$", ha="right", va="center", fontsize=11)
        if gap > 0:
            sequence.text(xa, y + 0.27, "甲", color=F.BLUE, ha="center", fontsize=11.5, weight="bold")
            sequence.text(xb, y + 0.27, "乙", color=F.RED, ha="center", fontsize=11.5, weight="bold")
            sequence.annotate(
                "",
                xy=(xb, y - 0.27),
                xytext=(xa, y - 0.27),
                arrowprops=dict(arrowstyle="<->", color=F.PURPLE, lw=1.8),
            )
            sequence.text((xa + xb) / 2, y - 0.50, rf"間距 ${gap:g}\ \mathrm{{m}}$", color=F.PURPLE, ha="center", fontsize=10.5)
        else:
            sequence.text(xa, y + 0.27, "甲、乙", color=F.PURPLE, ha="center", fontsize=11.5, weight="bold")
            sequence.text(xa + 5, y - 0.40, "追上：間距 0", color=F.PURPLE, ha="left", fontsize=10.5)
    sequence.set_title(r"甲 $25\ \mathrm{m/s}$、乙 $18\ \mathrm{m/s}$：等時間位置序列", fontsize=13)

    dense_time = np.linspace(0, 10, 200)
    dense_gap = (x_b0 - x_a0) + relative_velocity * dense_time
    graph.plot(dense_time, dense_gap, color=F.PURPLE, lw=2.8)
    graph.scatter(times, gaps, s=65, color=F.PURPLE, edgecolors="white", zorder=5)
    graph.set_xlim(0, 10.5)
    graph.set_ylim(0, 76)
    graph.set_xlabel("t (s)")
    graph.set_ylabel(r"$x_B-x_A$ (m)")
    graph.set_title(r"間距斜率 $v_{B/A}=-7\ \mathrm{m/s}$", fontsize=13)
    graph.text(1.1, 18, r"$x_{B/A}=70-7t$", color=F.PURPLE, fontsize=12)
    F.clean_grid(graph)

    fig.suptitle("相對速度是兩物體間距的變化率", fontsize=16, y=0.99)
    fig.subplots_adjust(left=0.055, right=0.975, top=0.82, bottom=0.13, wspace=0.23)
    _save(fig, "選物I-2", "選物I-2-一維相對速度")


def fig_incline_experiment_data():
    """114 實驗 1A：斜面臺車、打點紙帶與 x/v/a 三圖資料鏈。"""
    frequency = 50.0
    intervals_per_sample = 5
    dt = intervals_per_sample / frequency
    acceleration = 0.80
    time = np.arange(0.0, 0.51, dt)
    position = 0.5 * acceleration * time**2
    displacement = np.diff(position)
    interval_time = (time[:-1] + time[1:]) / 2
    interval_velocity = displacement / dt
    acceleration_time = (interval_time[:-1] + interval_time[1:]) / 2
    interval_acceleration = np.diff(interval_velocity) / dt

    assert np.isclose(dt, 0.10)
    assert np.allclose(np.diff(displacement), acceleration * dt**2)
    assert np.allclose(interval_velocity, acceleration * interval_time)
    assert np.allclose(interval_acceleration, acceleration)

    fig = plt.figure(figsize=(12.0, 6.2))
    gs = fig.add_gridspec(
        2, 4,
        width_ratios=[1.38, 1.0, 1.0, 1.0],
        height_ratios=[1.05, 0.95],
        hspace=0.48,
        wspace=0.38,
    )
    setup = fig.add_subplot(gs[:, 0])
    tape = fig.add_subplot(gs[0, 1:])
    x_ax = fig.add_subplot(gs[1, 1])
    v_ax = fig.add_subplot(gs[1, 2])
    a_ax = fig.add_subplot(gs[1, 3])

    setup.set_xlim(0, 7.0)
    setup.set_ylim(0, 9.2)
    setup.axis("off")
    setup.plot([0.65, 6.35], [7.55, 3.25], color="#64748b", lw=3.2)
    setup.plot([0.65, 6.35], [7.08, 2.78], color="#cbd5e1", lw=1.4)
    setup.add_patch(
        FancyBboxPatch(
            (0.35, 7.15), 1.65, 1.10,
            boxstyle="round,pad=0.05", facecolor="#f1f5f9",
            edgecolor="#64748b", lw=1.5,
        )
    )
    setup.text(1.18, 7.70, "打點計時器", ha="center", va="center", fontsize=11.2)
    setup.text(1.18, 7.28, r"$f=50\ \mathrm{Hz}$", ha="center", fontsize=10.5, color=F.PURPLE)

    cart_center = np.array([4.45, 4.65])
    setup.add_patch(
        FancyBboxPatch(
            (cart_center[0] - 0.75, cart_center[1] - 0.42), 1.50, 0.84,
            boxstyle="round,pad=0.04", facecolor="#dbeafe",
            edgecolor=F.BLUE, lw=1.8,
        )
    )
    setup.text(*cart_center, "力學臺車", ha="center", va="center", fontsize=11.5)
    setup.plot([1.95, cart_center[0] - 0.72], [7.20, cart_center[1] + 0.20], color=F.PURPLE, lw=2.4)
    setup.text(2.65, 6.30, "長紙帶", color=F.PURPLE, fontsize=11, rotation=-36)
    F.arrow(setup, (3.55, 5.56), (5.70, 3.95), color=F.BLUE, lw=2.5, mutation=17)
    setup.text(5.45, 4.70, r"$+x$", color=F.BLUE, fontsize=12)
    setup.text(3.45, 1.55, "先啟動計時器\n再釋放臺車", ha="center", fontsize=11.5)
    setup.text(3.45, 0.65, "重複更換紙帶", ha="center", fontsize=11.5, color=F.GREEN)
    setup.set_title("斜面臺車與打點紙帶", fontsize=13.5)

    base_time = np.arange(0.0, 0.501, 1 / frequency)
    base_position = 0.5 * acceleration * base_time**2
    scale_x = 0.45 + 9.0 * base_position / base_position[-1]
    tape.set_xlim(0, 10)
    tape.set_ylim(0, 3.3)
    tape.axis("off")
    tape.plot([0.35, 9.65], [1.45, 1.45], color="#94a3b8", lw=3.0)
    tape.scatter(scale_x, np.full_like(scale_x, 1.45), s=18, color="#64748b", zorder=3)
    sample_index = np.arange(0, len(base_time), intervals_per_sample)
    tape.scatter(scale_x[sample_index], np.full_like(sample_index, 1.45, dtype=float), s=78, color=F.PURPLE, edgecolors="white", zorder=5)
    for idx, source_idx in enumerate(sample_index):
        tape.text(scale_x[source_idx], 0.88 if idx % 2 == 0 else 0.54, rf"$x_{idx}$", ha="center", fontsize=10.2, color=F.PURPLE)
    tape.text(5.0, 2.65, r"小點：每 $1/f=0.020\ \mathrm{s}$；大點：每 5 個間隔取樣", ha="center", fontsize=12)
    tape.text(5.0, 2.18, r"$\Delta t=5/f=0.10\ \mathrm{s}$", ha="center", fontsize=12, color=F.PURPLE)
    tape.text(5.0, 0.08, r"$x_i\rightarrow\Delta x_i\rightarrow\bar v_i=\Delta x_i/\Delta t\rightarrow\bar a_i=\Delta v_i/\Delta t$", ha="center", fontsize=12)
    tape.set_title("固定頻率紙帶轉成等時距資料", fontsize=13.5)

    x_ax.plot(time, position, color=F.BLUE, lw=2.5)
    x_ax.scatter(time, position, s=42, color=F.BLUE, edgecolors="white", zorder=5)
    x_ax.set_title(r"$x$–$t$：拋物線", fontsize=12)
    x_ax.set_xlabel("t (s)")
    x_ax.set_ylabel("x (m)")

    v_ax.plot(interval_time, interval_velocity, color=F.GREEN, lw=2.5)
    v_ax.scatter(interval_time, interval_velocity, s=42, color=F.GREEN, edgecolors="white", zorder=5)
    v_ax.set_title(r"$v$–$t$：直線", fontsize=12)
    v_ax.set_xlabel("中點時刻 (s)")
    v_ax.set_ylabel("v (m/s)")

    a_ax.plot(acceleration_time, interval_acceleration, color=F.RED, lw=2.5)
    a_ax.scatter(acceleration_time, interval_acceleration, s=42, color=F.RED, edgecolors="white", zorder=5)
    a_ax.set_title(r"$a$–$t$：水平線", fontsize=12)
    a_ax.set_xlabel("t (s)")
    a_ax.set_ylabel("a (m/s²)")
    a_ax.set_ylim(0, 1.05)

    for ax in (x_ax, v_ax, a_ax):
        F.clean_grid(ax)

    fig.suptitle("實驗 1A：由斜面臺車紙帶建立位置、速度與加速度圖", fontsize=16, y=0.995)
    fig.subplots_adjust(left=0.035, right=0.975, top=0.90, bottom=0.09)
    _save(fig, "選物I-2", "選物I-2-斜面實驗資料")


def fig_freefall_experiment_data():
    """114 實驗 1B：固定第一閘、移動第二閘並消去共同初速。"""
    s1, t1 = 0.400, 0.200
    s2, t2 = 1.200, 0.400
    gravity = 2 * (s2 * t1 - s1 * t2) / (t1 * t2 * (t2 - t1))
    v0_from_1 = (s1 - 0.5 * gravity * t1**2) / t1
    v0_from_2 = (s2 - 0.5 * gravity * t2**2) / t2
    assert np.isclose(gravity, 10.0)
    assert np.isclose(v0_from_1, v0_from_2)

    fig, (setup, derivation) = plt.subplots(
        1, 2, figsize=(12.0, 6.0), gridspec_kw={"width_ratios": [0.92, 1.08]}
    )
    setup.set_xlim(0, 8)
    setup.set_ylim(0, 11)
    setup.axis("off")
    F.arrow(setup, (0.85, 9.85), (0.85, 0.75), color=F.BLUE, lw=2.2, mutation=17)
    setup.text(0.52, 0.42, "+y", color=F.BLUE, fontsize=12)

    setup.add_patch(Rectangle((3.0, 9.65), 2.0, 0.70, facecolor="#f1f5f9", edgecolor="#64748b", lw=1.5))
    setup.text(4.0, 10.0, "電磁鐵", ha="center", va="center", fontsize=11.5)
    setup.scatter([4.0], [9.15], s=190, color=F.RED, edgecolors="white", zorder=5)
    setup.text(4.55, 9.15, "小鐵球", va="center", fontsize=11)

    y_first, y_second_1, y_second_2 = 7.55, 5.05, 2.15

    def gate(ax, y, label, *, color):
        ax.add_patch(Rectangle((2.25, y - 0.18), 3.50, 0.36, facecolor="#e2e8f0", edgecolor="#64748b", lw=1.4))
        ax.plot([3.05, 4.95], [y, y], color=color, lw=2.4)
        ax.text(6.0, y, label, va="center", fontsize=11.2)

    gate(setup, y_first, "第一光電閘（固定）", color=F.GREEN)
    gate(setup, y_second_1, "第二閘位置 1", color=F.PURPLE)
    gate(setup, y_second_2, "第二閘位置 2", color=F.PURPLE)

    setup.annotate("", xy=(1.65, y_first), xytext=(1.65, y_second_1), arrowprops=dict(arrowstyle="<->", color=F.PURPLE, lw=1.8))
    setup.text(1.38, (y_first + y_second_1) / 2, r"$S_1,t_1$", rotation=90, ha="center", va="center", color=F.PURPLE, fontsize=11.5)
    setup.annotate("", xy=(1.15, y_first), xytext=(1.15, y_second_2), arrowprops=dict(arrowstyle="<->", color=F.BLUE, lw=1.8))
    setup.text(0.88, (y_first + y_second_2) / 2, r"$S_2,t_2$", rotation=90, ha="center", va="center", color=F.BLUE, fontsize=11.5)

    F.arrow(setup, (6.35, y_second_1 - 0.25), (6.35, y_second_2 + 0.25), color=F.PURPLE, lw=2.0, mutation=16)
    setup.text(6.68, 3.60, "移動第二閘", rotation=90, ha="center", va="center", color=F.PURPLE, fontsize=11)
    setup.text(4.0, 0.50, r"兩次都從第一閘開始計時，共用 $v_0$", ha="center", fontsize=11.5)
    setup.set_title("固定起始閘，改變終止閘位置", fontsize=13.5)

    derivation.set_xlim(0, 10)
    derivation.set_ylim(0, 11)
    derivation.axis("off")
    _card(
        derivation, (0.55, 8.15), 8.9, 1.55,
        r"① 兩段等加速度式" + "\n" + r"$S_1=v_0t_1+\frac{1}{2}gt_1^2$　$S_2=v_0t_2+\frac{1}{2}gt_2^2$",
        edge=F.BLUE, face="#eff6ff", fs=12.2,
    )
    _card(
        derivation, (0.55, 5.65), 8.9, 1.55,
        r"② 分別除以時間" + "\n" + r"$S_1/t_1=v_0+\frac{1}{2}gt_1$　$S_2/t_2=v_0+\frac{1}{2}gt_2$",
        edge=F.GREEN, face="#f0fdf4", fs=12.2,
    )
    _card(
        derivation, (0.55, 3.15), 8.9, 1.55,
        r"③ 第二式減第一式，消去共同 $v_0$" + "\n" + r"$S_2/t_2-S_1/t_1=\frac{1}{2}g(t_2-t_1)$",
        edge=F.PURPLE, face="#f5f3ff", fs=12.0,
    )
    _card(
        derivation, (0.55, 0.55), 8.9, 1.65,
        r"④ 可測量量給出" + "\n" + r"$g=\dfrac{2(S_2t_1-S_1t_2)}{t_1t_2(t_2-t_1)}$",
        edge=F.RED, face="#fff1f2", fs=12.4,
    )
    for y_start, y_end in [(8.10, 7.30), (5.60, 4.80), (3.10, 2.25)]:
        F.arrow(derivation, (5.0, y_start), (5.0, y_end), color="#64748b", lw=1.6, mutation=14)
    derivation.set_title("由兩次量測消去未知初速", fontsize=13.5)

    fig.suptitle("實驗 1B：固定第一光電閘，以兩組距離與時間求 $g$", fontsize=16, y=0.995)
    fig.subplots_adjust(left=0.035, right=0.975, top=0.89, bottom=0.06, wspace=0.12)
    _save(fig, "選物I-2", "選物I-2-自由落體實驗")


def fig_vector_components():
    """左上向量的分量正負與量值。"""
    fig, (left, right) = plt.subplots(1, 2, figsize=(11.8, 5.1), gridspec_kw={"width_ratios": [1.05, 0.95]})
    left.set_xlim(-5.0, 1.4)
    left.set_ylim(-1.2, 4.8)
    left.set_aspect("equal")
    left.axis("off")
    F.arrow(left, (-4.4, 0), (1.0, 0), color="#64748b", lw=1.6, mutation=14)
    F.arrow(left, (0, -0.7), (0, 4.35), color="#64748b", lw=1.6, mutation=14)
    left.text(1.1, -0.25, "+x", fontsize=11)
    left.text(0.18, 4.35, "+y", fontsize=11)
    end = (-3.7, 2.8)
    F.arrow(left, (0, 0), end, color=F.PURPLE, lw=3.2, mutation=20)
    left.plot([end[0], end[0]], [0, end[1]], color="#94a3b8", ls="--", lw=1.5)
    left.plot([0, end[0]], [end[1], end[1]], color="#94a3b8", ls="--", lw=1.5)
    F.arrow(left, (0, 0), (end[0], 0), color=F.BLUE, lw=2.8, mutation=18)
    F.arrow(left, (0, 0), (0, end[1]), color=F.GREEN, lw=2.8, mutation=18)
    left.text(-1.85, -0.48, r"$A_x<0$", color=F.BLUE, fontsize=13, ha="center")
    left.text(0.28, 1.45, r"$A_y>0$", color=F.GREEN, fontsize=13, va="center")
    left.text(-2.05, 1.72, r"$\vec A$", color=F.PURPLE, fontsize=15, weight="bold")
    F.angle_arc(left, (0, 0), 0.95, 143, 180, color=F.INK, text=r"$37^\circ$")
    left.set_title("先由箭頭方向判斷正負", fontsize=14)

    right.set_xlim(0, 10)
    right.set_ylim(0, 10)
    right.axis("off")
    _card(right, (0.7, 6.3), 8.6, 2.1, "① 方向\n向左，所以 $A_x<0$；向上，所以 $A_y>0$", edge=F.BLUE, face="#eff6ff", fs=13)
    _card(right, (0.7, 3.4), 8.6, 2.1, "② 量值\n" + r"$|A_x|=A\cos37^\circ$；$|A_y|=A\sin37^\circ$", edge=F.GREEN, face="#f0fdf4", fs=13)
    _card(right, (0.7, 0.5), 8.6, 2.1, "③ 合併\n" + r"$A_x=-A\cos37^\circ$；$A_y=+A\sin37^\circ$", edge=F.PURPLE, face="#f5f3ff", fs=13)
    right.set_title("再用直角三角形求量值", fontsize=14)

    fig.suptitle(r"分解向量：正負由座標方向決定，$\sin$、$\cos$ 給分量量值", fontsize=16, y=0.99)
    fig.subplots_adjust(left=0.04, right=0.975, top=0.88, bottom=0.06, wspace=0.08)
    _save(fig, "選物I-3", "選物I-3-向量分解與正負")


def fig_vector_construction():
    """首尾相接、平行四邊形與減法的幾何作圖。"""
    fig, axes = plt.subplots(1, 3, figsize=(12.0, 4.6))
    a = np.array([2.8, 1.0])
    b = np.array([1.1, 2.2])
    colors = [F.BLUE, F.GREEN, F.PURPLE]

    for ax in axes:
        ax.set_xlim(-2.0, 4.7)
        ax.set_ylim(-2.0, 4.4)
        ax.set_aspect("equal")
        ax.axis("off")
        ax.axhline(0, color="#e2e8f0", lw=1.0)
        ax.axvline(0, color="#e2e8f0", lw=1.0)

    left, middle, right = axes
    F.arrow(left, (0, 0), a, color=colors[0], lw=2.7, mutation=17)
    F.arrow(left, a, a + b, color=colors[1], lw=2.7, mutation=17)
    F.arrow(left, (0, 0), a + b, color=colors[2], lw=3.0, mutation=18)
    left.text(*(a * 0.52 + np.array([0.0, -0.35])), r"$\vec A$", color=colors[0], fontsize=12)
    left.text(*(a + b * 0.55 + np.array([0.18, 0.0])), r"$\vec B$", color=colors[1], fontsize=12)
    left.text(*(0.52 * (a + b) + np.array([-0.42, 0.16])), r"$\vec A+\vec B$", color=colors[2], fontsize=12)
    left.set_title("首尾相接", fontsize=13.5)

    F.arrow(middle, (0, 0), a, color=colors[0], lw=2.7, mutation=17)
    F.arrow(middle, (0, 0), b, color=colors[1], lw=2.7, mutation=17)
    middle.plot([a[0], a[0] + b[0]], [a[1], a[1] + b[1]], color="#94a3b8", ls="--", lw=1.4)
    middle.plot([b[0], a[0] + b[0]], [b[1], a[1] + b[1]], color="#94a3b8", ls="--", lw=1.4)
    F.arrow(middle, (0, 0), a + b, color=colors[2], lw=3.0, mutation=18)
    middle.text(*(a * 0.55 + np.array([0.0, -0.35])), r"$\vec A$", color=colors[0], fontsize=12)
    middle.text(*(b * 0.55 + np.array([-0.40, 0.05])), r"$\vec B$", color=colors[1], fontsize=12)
    middle.text(*(0.56 * (a + b) + np.array([-0.30, 0.18])), r"$\vec A+\vec B$", color=colors[2], fontsize=12)
    middle.set_title("平行四邊形", fontsize=13.5)

    minus_b = -b
    F.arrow(right, (0, 0), a, color=colors[0], lw=2.7, mutation=17)
    F.arrow(right, a, a + minus_b, color=F.RED, lw=2.7, mutation=17)
    F.arrow(right, (0, 0), a - b, color=colors[2], lw=3.0, mutation=18)
    right.text(*(a * 0.48 + np.array([0.0, 0.25])), r"$\vec A$", color=colors[0], fontsize=12)
    right.text(*(a + minus_b * 0.55 + np.array([0.18, 0.0])), r"$-\vec B$", color=F.RED, fontsize=12)
    right.text(*(0.50 * (a - b) + np.array([0.05, -0.38])), r"$\vec A-\vec B$", color=colors[2], fontsize=12)
    right.set_title(r"減法 $\vec A-\vec B=\vec A+(-\vec B)$", fontsize=13.5)

    fig.suptitle("向量作圖保持量值與方向；平移箭頭不改變向量", fontsize=16, y=0.99)
    fig.subplots_adjust(left=0.025, right=0.985, top=0.82, bottom=0.05, wspace=0.05)
    _save(fig, "選物I-3", "選物I-3-向量作圖")


def fig_tangent_normal_acceleration():
    """以速度差與方向分量說明曲線運動，不引入下一章的量值公式。"""
    fig, axes = plt.subplots(1, 2, figsize=(11.8, 5.2))
    for ax in axes:
        ax.set_xlim(-0.5, 6.1)
        ax.set_ylim(-0.6, 5.5)
        ax.set_aspect("equal")
        ax.axis("off")

    left, right = axes

    # 左：把兩個等長速度平移到共同起點，直接看見 Δv 來自方向改變。
    origin = np.array([0.65, 0.85])
    v1 = np.array([4.0, 0.0])
    angle = np.deg2rad(45.0)
    v2 = 4.0 * np.array([np.cos(angle), np.sin(angle)])
    assert np.isclose(np.linalg.norm(v1), np.linalg.norm(v2))
    delta_v = v2 - v1
    assert np.allclose(origin + v1 + delta_v, origin + v2)

    left.plot([origin[0], origin[0] + v2[0]], [origin[1], origin[1] + v2[1]], color="#cbd5e1", lw=1.2, ls="--")
    F.arrow(left, origin, origin + v1, color=F.BLUE, lw=3.0, mutation=18)
    F.arrow(left, origin, origin + v2, color=F.GREEN, lw=3.0, mutation=18)
    F.arrow(left, origin + v1, origin + v2, color=F.RED, lw=3.0, mutation=18)
    left.scatter([origin[0]], [origin[1]], s=55, color=F.INK, zorder=6)
    left.text(origin[0] + 2.0, origin[1] - 0.38, r"$\vec v_1$", color=F.BLUE, fontsize=13, ha="center")
    left.text(origin[0] + 1.35, origin[1] + 1.75, r"$\vec v_2$", color=F.GREEN, fontsize=13, ha="center")
    left.text(origin[0] + 3.55, origin[1] + 1.62, r"$\Delta\vec v$", color=F.RED, fontsize=13, ha="center")
    left.text(2.8, 5.10, "等長速度仍可具有速度變化", ha="center", fontsize=14, weight="bold")
    left.text(2.8, -0.30, r"$|\vec v_1|=|\vec v_2|$；$\Delta\vec v$ 使方向改變", ha="center", fontsize=11.5)

    # 右：在軌跡上一點，以速度方向為基準分解同一個加速度向量。
    x_curve = np.linspace(0.15, 5.85, 180)
    y_curve = 1.55 + 0.17 * (x_curve - 2.35) ** 2
    right.plot(x_curve, y_curve, color="#94a3b8", lw=2.2)
    point = np.array([2.35, 1.55])
    right.scatter([point[0]], [point[1]], s=90, color=F.INK, edgecolors="white", zorder=6)

    velocity = np.array([2.25, 0.0])
    parallel = np.array([-1.10, 0.0])
    perpendicular = np.array([0.0, 1.60])
    total = parallel + perpendicular
    assert np.isclose(np.dot(parallel, perpendicular), 0.0)
    assert np.allclose(total, parallel + perpendicular)

    F.arrow(right, point, point + velocity, color=F.BLUE, lw=3.0, mutation=18)
    F.arrow(right, point, point + parallel, color=F.GREEN, lw=2.8, mutation=17)
    F.arrow(right, point, point + perpendicular, color=F.RED, lw=2.8, mutation=17)
    F.arrow(right, point, point + total, color=F.PURPLE, lw=3.1, mutation=18)
    right.plot([point[0] - 0.22, point[0] - 0.22, point[0]], [point[1], point[1] + 0.22, point[1] + 0.22], color="#64748b", lw=1.2)
    right.text(point[0] + 1.95, point[1] - 0.34, r"$\vec v$", color=F.BLUE, fontsize=13, ha="center")
    right.text(point[0] - 0.62, point[1] - 0.38, r"$\vec a_{\parallel}$", color=F.GREEN, fontsize=12.5, ha="center")
    right.text(point[0] + 0.18, point[1] + 1.50, r"$\vec a_{\perp}$", color=F.RED, fontsize=12.5, va="center")
    right.text(point[0] - 1.35, point[1] + 1.55, r"$\vec a$", color=F.PURPLE, fontsize=13, ha="center")
    right.text(2.8, 5.10, "以速度方向分解加速度", ha="center", fontsize=14, weight="bold")
    right.text(2.8, -0.30, "平行分量改變速率；垂直分量改變方向", ha="center", fontsize=11.5)

    fig.suptitle("曲線運動：由速度差判斷加速度的方向作用", fontsize=16, y=0.99)
    fig.subplots_adjust(left=0.03, right=0.98, top=0.84, bottom=0.08, wspace=0.10)
    _save(fig, "選物I-3", "選物I-3-切向與法向加速度")


def fig_projectile_decomposition():
    """以速度空間的向量三角形與位置空間的等時間點建立拋體分解。"""
    speed = 10.0
    theta = np.deg2rad(40.0)
    gravity = 9.8
    vx0 = speed * np.cos(theta)
    vy0 = speed * np.sin(theta)
    flight_time = 2 * vy0 / gravity
    sample_time = np.linspace(0.0, flight_time, 5)
    sample_x = vx0 * sample_time
    sample_y = vy0 * sample_time - 0.5 * gravity * sample_time**2
    apex_time = vy0 / gravity
    apex = np.array([vx0 * apex_time, vy0 * apex_time - 0.5 * gravity * apex_time**2])

    assert np.allclose(np.array([vx0, vy0]), speed * np.array([np.cos(theta), np.sin(theta)]))
    assert np.allclose(sample_y, vy0 * sample_time - 0.5 * gravity * sample_time**2)
    assert np.isclose(apex[1], vy0**2 / (2 * gravity))
    assert np.isclose(vy0 - gravity * apex_time, 0.0)

    fig, (vectors, trajectory_ax) = plt.subplots(
        1,
        2,
        figsize=(12.0, 5.1),
        gridspec_kw={"width_ratios": [0.85, 1.35]},
    )

    vectors.set_aspect("equal")
    vectors.set_xlim(-0.8, 9.2)
    vectors.set_ylim(-0.8, 8.0)
    vectors.axis("off")
    F.arrow(vectors, (0, 0), (8.5, 0), color="#64748b", lw=1.5, mutation=13)
    F.arrow(vectors, (0, 0), (0, 7.4), color="#64748b", lw=1.5, mutation=13)
    endpoint = np.array([vx0, vy0])
    F.arrow(vectors, (0, 0), endpoint, color=F.PURPLE, lw=3.0, mutation=19)
    F.arrow(vectors, (0, 0), (vx0, 0), color=F.BLUE, lw=2.7, mutation=17)
    F.arrow(vectors, (vx0, 0), endpoint, color=F.RED, lw=2.7, mutation=17)
    vectors.plot([0, endpoint[0]], [endpoint[1], endpoint[1]], color="#94a3b8", lw=1.2, ls="--")
    vectors.text(endpoint[0] / 2, -0.55, r"$v_{0x}=v_0\cos\theta$", color=F.BLUE, ha="center", fontsize=11.5)
    vectors.text(endpoint[0] + 0.24, endpoint[1] / 2, r"$v_{0y}=v_0\sin\theta$", color=F.RED, va="center", fontsize=11.5)
    vectors.text(endpoint[0] * 0.47, endpoint[1] * 0.58, r"$\vec v_0$", color=F.PURPLE, fontsize=13)
    vectors.set_title("初速度先分成兩個正交分量", fontsize=13.5)

    dense_time = np.linspace(0.0, flight_time, 300)
    dense_x = vx0 * dense_time
    dense_y = vy0 * dense_time - 0.5 * gravity * dense_time**2
    trajectory_ax.plot(dense_x, dense_y, color=F.PURPLE, lw=2.8)
    trajectory_ax.scatter(sample_x, sample_y, s=70, color=F.PURPLE, edgecolors="white", zorder=5)
    for t, x, y in zip(sample_time, sample_x, sample_y):
        trajectory_ax.plot([x, x], [0, y], color="#cbd5e1", lw=1.0, ls="--")
        assert np.isclose(y, vy0 * t - 0.5 * gravity * t**2)
    velocity_scale = 0.18
    acceleration_scale = 0.12
    F.arrow(trajectory_ax, apex, apex + velocity_scale * np.array([vx0, 0.0]), color=F.BLUE, lw=2.6, mutation=16)
    F.arrow(trajectory_ax, apex, apex + acceleration_scale * np.array([0.0, -gravity]), color=F.RED, lw=2.6, mutation=16)
    trajectory_ax.text(*(apex + np.array([0.85, 0.16])), r"$v_x$ 不變", color=F.BLUE, fontsize=11.5)
    trajectory_ax.text(*(apex + np.array([0.20, -0.78])), r"$a_y=-g$", color=F.RED, fontsize=11.5)
    trajectory_ax.set_xlim(-0.25, sample_x[-1] + 0.45)
    trajectory_ax.set_ylim(-0.15, apex[1] + 0.70)
    trajectory_ax.set_xlabel("x (m)")
    trajectory_ax.set_ylabel("y (m)")
    trajectory_ax.set_title("同一時間連結水平等速度與鉛直等加速度", fontsize=13.5)
    F.clean_grid(trajectory_ax)

    fig.suptitle(r"理想拋體：$x=v_{0x}t$，$y=v_{0y}t-\frac{1}{2}gt^2$", fontsize=16, y=0.99)
    fig.subplots_adjust(left=0.055, right=0.975, top=0.82, bottom=0.13, wspace=0.22)
    _save(fig, "選物I-3", "選物I-3-拋體分解")


def fig_projectile_velocity_components():
    """拋體三個時刻的水平、鉛直速度分量。"""
    fig, ax = F.schematic(11.8, 5.3)
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 6.0)
    ax.set_aspect("auto")
    F.arrow(ax, (0.75, 0.85), (11.35, 0.85), color="#64748b", lw=1.6, mutation=14)
    F.arrow(ax, (0.75, 0.85), (0.75, 5.45), color="#64748b", lw=1.6, mutation=14)
    ax.text(11.48, 0.68, "+x", fontsize=11)
    ax.text(0.48, 5.47, "+y", fontsize=11, ha="right")

    def trajectory(x):
        return 1.0 + 0.18 * (x - 1) * (11 - x)

    xs = np.linspace(1.0, 11.0, 300)
    ys = trajectory(xs)
    ax.plot(xs, ys, color="#64748b", lw=2.5, ls="--")
    point_x = [3.2, 6.0, 8.8]
    points = [
        (point_x[0], trajectory(point_x[0]), "上升", 1),
        (point_x[1], trajectory(point_x[1]), "最高點", 0),
        (point_x[2], trajectory(point_x[2]), "下降", -1),
    ]
    assert all(np.isclose(y, trajectory(x)) for x, y, _, _ in points)
    for x, y, label, vy_sign in points:
        ax.scatter([x], [y], s=85, color=F.INK, zorder=6)
        F.arrow(ax, (x, y), (x + 1.15, y), color=F.BLUE, lw=2.7, mutation=17)
        ax.text(x + 0.58, y + 0.22, r"$v_x$", color=F.BLUE, fontsize=12, ha="center")
        if vy_sign > 0:
            F.arrow(ax, (x, y), (x, y + 1.05), color=F.GREEN, lw=2.7, mutation=17)
            ax.text(x - 0.18, y + 0.72, r"$v_y>0$", color=F.GREEN, fontsize=11.5, ha="right")
        elif vy_sign < 0:
            F.arrow(ax, (x, y), (x, y - 1.05), color=F.GREEN, lw=2.7, mutation=17)
            ax.text(x + 0.18, y - 0.82, r"$v_y<0$", color=F.GREEN, fontsize=11.5)
        else:
            ax.text(x, y - 0.48, r"$v_y=0$", color=F.GREEN, fontsize=11.5, ha="center")
        F.arrow(ax, (x - 0.42, y - 0.2), (x - 0.42, y - 1.0), color=F.RED, lw=2.4, mutation=16)
        ax.text(x - 0.58, y - 1.10, r"$a_y=-g$", color=F.RED, fontsize=10.8, ha="right")
        ax.text(x, 0.25, label, fontsize=12.5, weight="bold", ha="center")

    ax.text(6.0, 5.72, "水平分量不變；鉛直分量每秒減少 $g$", ha="center", fontsize=16, weight="bold")
    ax.text(6.0, 0.02, r"$v_x=v_0\cos\theta$　　$v_y=v_0\sin\theta-gt$", ha="center", fontsize=13)
    fig.subplots_adjust(left=0.025, right=0.975, top=0.98, bottom=0.03)
    _save(fig, "選物I-3", "選物I-3-拋體速度分量")


def fig_linear_motion_solution_panels():
    """章末第 3、7、17 題：圖像面積、鉛直符號與追車分段狀態。"""
    # Panel A：第 3 題的 v–t 圖。
    t_graph = np.linspace(0.0, 5.0, 501)
    v_graph = -4.0 + 2.0 * t_graph
    zero_time = 2.0
    negative_mask = t_graph <= zero_time
    positive_mask = t_graph >= zero_time
    negative_area = np.trapezoid(v_graph[negative_mask], t_graph[negative_mask])
    positive_area = np.trapezoid(v_graph[positive_mask], t_graph[positive_mask])
    graph_slope = (v_graph[-1] - v_graph[0]) / (t_graph[-1] - t_graph[0])
    assert np.isclose(-4.0 + 2.0 * zero_time, 0.0)
    assert np.isclose(graph_slope, 2.0)
    assert np.isclose(negative_area, -4.0)
    assert np.isclose(positive_area, 9.0)
    assert np.isclose(negative_area + positive_area, 5.0)
    assert np.isclose(abs(negative_area) + abs(positive_area), 13.0)

    # Panel B：第 7 題，全程取向上為正。
    launch_speed, gravity = 24.5, 9.8
    apex_time = launch_speed / gravity
    state_times = np.array([0.0, apex_time, 4.0])
    state_y = launch_speed * state_times - 0.5 * gravity * state_times**2
    state_v = launch_speed - gravity * state_times
    assert np.isclose(apex_time, 2.5)
    assert np.allclose(state_y, [0.0, 30.625, 19.6])
    assert np.allclose(state_v, [24.5, 0.0, -14.7])
    assert np.all(np.array([-gravity, -gravity, -gravity]) < 0)

    # Panel C：第 17 題，以相對速度面積追蹤間距。
    initial_gap = 60.0
    cruise_duration = 2.0
    initial_relative_speed = 10.0
    relative_acceleration = -2.0
    equal_speed_tau = -initial_relative_speed / relative_acceleration
    equal_speed_time = cruise_duration + equal_speed_tau
    first_closure = initial_relative_speed * cruise_duration
    braking_closure = 0.5 * initial_relative_speed * equal_speed_tau
    gap_after_cruise = initial_gap - first_closure
    minimum_gap = gap_after_cruise - braking_closure
    assert np.isclose(equal_speed_tau, 5.0)
    assert np.isclose(equal_speed_time, 7.0)
    assert np.isclose(first_closure, 20.0)
    assert np.isclose(braking_closure, 25.0)
    assert np.isclose(gap_after_cruise, 40.0)
    assert np.isclose(minimum_gap, 15.0) and minimum_gap > 0

    fig = plt.figure(figsize=(12.0, 8.0))
    grid = fig.add_gridspec(2, 2, height_ratios=[1.0, 0.92], hspace=0.43, wspace=0.27)
    graph_ax = fig.add_subplot(grid[0, 0])
    vertical_ax = fig.add_subplot(grid[0, 1])
    chase_ax = fig.add_subplot(grid[1, :])

    graph_ax.plot(t_graph, v_graph, color=F.PURPLE, lw=2.8)
    graph_ax.axhline(0, color=F.INK, lw=1.2)
    graph_ax.fill_between(
        t_graph[negative_mask], v_graph[negative_mask], 0,
        color=F.RED, alpha=0.20,
    )
    graph_ax.fill_between(
        t_graph[positive_mask], 0, v_graph[positive_mask],
        color=F.BLUE, alpha=0.20,
    )
    graph_ax.scatter([0, zero_time, 5], [-4, 0, 6], s=58, color=F.PURPLE, edgecolors="white", zorder=5)
    graph_ax.axvline(zero_time, color="#94a3b8", lw=1.0, ls="--")
    graph_ax.text(0.38, -2.2, r"$A_-=-4\ \mathrm{m}$", color=F.RED, fontsize=11.2)
    graph_ax.text(3.15, 2.3, r"$A_+=+9\ \mathrm{m}$", color=F.BLUE, fontsize=11.2)
    graph_ax.text(2.48, 4.75, r"斜率 $a=+2\ \mathrm{m/s^2}$", color=F.PURPLE, fontsize=11.2)
    graph_ax.text(zero_time + 0.10, -0.75, r"$t=2\ \mathrm{s}$ 轉向", fontsize=10.6)
    graph_ax.set_xlim(0, 5.15)
    graph_ax.set_ylim(-4.8, 6.8)
    graph_ax.set_xlabel("t (s)")
    graph_ax.set_ylabel("v (m/s)")
    graph_ax.set_title("A｜第 3 題：斜率與帶號面積", fontsize=13.5)
    F.clean_grid(graph_ax)

    vertical_ax.set_xlim(-2.2, 3.6)
    vertical_ax.set_ylim(-3.0, 35.0)
    vertical_ax.axis("off")
    F.arrow(vertical_ax, (-1.45, -0.8), (-1.45, 33.3), color=F.BLUE, lw=2.0, mutation=15)
    vertical_ax.text(-1.70, 33.1, "+y", color=F.BLUE, ha="right", fontsize=11.5)
    vertical_ax.plot([0, 0], [0, state_y[1]], color="#94a3b8", lw=2.2)
    state_labels = [r"$t=0$", r"$t=2.50\ \mathrm{s}$", r"$t=4.00\ \mathrm{s}$"]
    x_offsets = [0.0, 0.0, 0.0]
    velocity_scale = 0.23
    acceleration_arrow = 2.3
    for t_state, y_state, v_state, label, x_offset in zip(state_times, state_y, state_v, state_labels, x_offsets):
        point = (x_offset, y_state)
        vertical_ax.scatter([point[0]], [point[1]], s=78, color=F.INK, edgecolors="white", zorder=6)
        vertical_ax.text(point[0] + 0.34, point[1] + 0.35, label, fontsize=10.5)
        if v_state > 0:
            end = (point[0], point[1] + velocity_scale * v_state)
            assert end[1] > point[1]
            F.arrow(vertical_ax, point, end, color=F.GREEN, lw=2.5, mutation=16)
            vertical_ax.text(point[0] + 0.18, end[1] - 0.35, r"$v=+24.5$", color=F.GREEN, fontsize=10.3)
        elif v_state < 0:
            end = (point[0], point[1] + velocity_scale * v_state)
            assert end[1] < point[1]
            F.arrow(vertical_ax, point, end, color=F.GREEN, lw=2.5, mutation=16)
            vertical_ax.text(point[0] + 0.18, end[1] - 0.25, r"$v=-14.7$", color=F.GREEN, fontsize=10.3)
        else:
            vertical_ax.text(point[0] + 0.34, point[1] - 1.25, r"$v=0$", color=F.GREEN, fontsize=10.5)
        a_end = (point[0] - 0.55, point[1] - acceleration_arrow)
        assert a_end[1] < point[1]
        F.arrow(vertical_ax, (point[0] - 0.55, point[1]), a_end, color=F.RED, lw=2.1, mutation=14)
    vertical_ax.text(2.1, 4.2, r"全程 $a=-9.8\ \mathrm{m/s^2}$", color=F.RED, fontsize=11.0, ha="center")
    vertical_ax.text(2.1, 1.7, r"$y(4.0)=+19.6\ \mathrm{m}$", color=F.PURPLE, fontsize=11.0, ha="center")
    vertical_ax.set_title("B｜第 7 題：向上為正的三個時間狀態", fontsize=13.5)

    t_chase = np.linspace(0.0, equal_speed_time, 701)
    v_relative = np.where(
        t_chase <= cruise_duration,
        initial_relative_speed,
        initial_relative_speed + relative_acceleration * (t_chase - cruise_duration),
    )
    assert np.isclose(np.trapezoid(v_relative, t_chase), first_closure + braking_closure)
    chase_ax.plot(t_chase, v_relative, color=F.PURPLE, lw=2.8)
    chase_ax.fill_between(t_chase[t_chase <= cruise_duration], 0, v_relative[t_chase <= cruise_duration], color=F.BLUE, alpha=0.20)
    brake_mask = t_chase >= cruise_duration
    chase_ax.fill_between(t_chase[brake_mask], 0, v_relative[brake_mask], color=F.GREEN, alpha=0.20)
    chase_ax.axhline(0, color=F.INK, lw=1.2)
    for moment in [0.0, cruise_duration, equal_speed_time]:
        chase_ax.axvline(moment, color="#94a3b8", lw=1.0, ls="--")
    chase_ax.scatter([0, cruise_duration, equal_speed_time], [10, 10, 0], s=58, color=F.PURPLE, edgecolors="white", zorder=5)
    chase_ax.text(0.65, 4.1, r"面積 $20\ \mathrm{m}$", color=F.BLUE, fontsize=11.2)
    chase_ax.text(4.1, 3.0, r"面積 $25\ \mathrm{m}$", color=F.GREEN, fontsize=11.2)
    chase_ax.text(3.1, 8.2, r"斜率 $a_{R/F}=-2.0\ \mathrm{m/s^2}$", color=F.PURPLE, fontsize=11.2)
    chase_ax.text(0.03, -2.0, r"$d=60\ \mathrm{m}$", fontsize=10.8, ha="left")
    chase_ax.text(cruise_duration, -2.0, r"$d=40\ \mathrm{m}$", fontsize=10.8, ha="center")
    chase_ax.text(equal_speed_time, -2.0, r"$d_{\min}=15\ \mathrm{m}$", fontsize=10.8, ha="right")
    chase_ax.set_xlim(0, 7.15)
    chase_ax.set_ylim(-2.7, 11.5)
    chase_ax.text(cruise_duration + 0.10, 10.55, "開始煞車", fontsize=10.5, ha="left")
    chase_ax.text(equal_speed_time - 0.08, 0.55, "同速", fontsize=10.5, ha="right")
    chase_ax.set_xticks([0, 2, 7])
    chase_ax.set_xticklabels([r"$0$", r"$2$", r"$7$"])
    chase_ax.set_xlabel("t (s)")
    chase_ax.set_ylabel(r"$v_{R/F}$ (m/s)")
    chase_ax.set_title("C｜第 17 題：相對速度面積是追近距離", fontsize=13.5)
    F.clean_grid(chase_ax)

    fig.suptitle("章末列式圖：直線運動的圖像、符號與分段時間", fontsize=16, y=0.995)
    fig.subplots_adjust(left=0.065, right=0.975, top=0.91, bottom=0.085)
    _save(fig, "選物I-2", "選物I-2-章末列式圖")


def fig_projectile_solution_panels():
    """章末第 4、5、15 題：水平拋、斜拋與影片資料重建。"""
    gravity = 10.0

    # Panel A：第 4 題水平拋。
    horizontal_height, horizontal_speed = 45.0, 8.0
    horizontal_time = np.sqrt(2 * horizontal_height / gravity)
    horizontal_range = horizontal_speed * horizontal_time
    horizontal_v = np.array([horizontal_speed, -gravity * horizontal_time])
    horizontal_angle = np.degrees(np.arctan2(abs(horizontal_v[1]), horizontal_v[0]))
    assert np.isclose(horizontal_time, 3.0)
    assert np.isclose(horizontal_range, 24.0)
    assert np.allclose(horizontal_v, [8.0, -30.0])
    assert horizontal_v[0] > 0 and horizontal_v[1] < 0
    assert np.isclose(horizontal_angle, np.degrees(np.arctan(30 / 8)))

    # Panel B：第 5 題同高斜拋。
    oblique_v = np.array([15.0, 20.0])
    apex_time = oblique_v[1] / gravity
    flight_time = 2 * apex_time
    oblique_range = oblique_v[0] * flight_time
    state_times = np.array([0.0, apex_time, flight_time])
    state_x = oblique_v[0] * state_times
    state_y = oblique_v[1] * state_times - 0.5 * gravity * state_times**2
    state_vy = oblique_v[1] - gravity * state_times
    assert np.isclose(apex_time, 2.0)
    assert np.isclose(flight_time, 4.0)
    assert np.isclose(oblique_range, 60.0)
    assert np.allclose(state_x, [0.0, 30.0, 60.0])
    assert np.allclose(state_y, [0.0, 20.0, 0.0])
    assert np.allclose(state_vy, [20.0, 0.0, -20.0])

    # Panel C：第 15 題的等時距位置資料。
    data_time = np.array([0.0, 0.2, 0.4, 0.6])
    data_x = np.array([0.0, 1.6, 3.2, 4.8])
    data_y = np.array([0.0, 1.0, 1.6, 1.8])
    dt = data_time[1] - data_time[0]
    dx = np.diff(data_x)
    dy = np.diff(data_y)
    second_y = data_y[2:] - 2 * data_y[1:-1] + data_y[:-2]
    reconstructed_ax = np.diff(dx) / dt**2
    reconstructed_ay = second_y / dt**2
    assert np.allclose(np.diff(data_time), dt)
    assert np.allclose(dx, 1.6)
    assert np.allclose(dy, [1.0, 0.6, 0.2])
    assert np.allclose(reconstructed_ax, 0.0)
    assert np.allclose(second_y, -0.4)
    assert np.allclose(reconstructed_ay, -10.0)

    fig = plt.figure(figsize=(12.0, 8.2))
    grid = fig.add_gridspec(2, 2, height_ratios=[1.0, 0.90], hspace=0.43, wspace=0.24)
    horizontal_ax = fig.add_subplot(grid[0, 0])
    oblique_ax = fig.add_subplot(grid[0, 1])
    data_ax = fig.add_subplot(grid[1, :])

    sample_t = np.arange(0.0, horizontal_time + 0.01, 1.0)
    sample_x = horizontal_speed * sample_t
    sample_y = horizontal_height - 0.5 * gravity * sample_t**2
    dense_t = np.linspace(0.0, horizontal_time, 240)
    horizontal_ax.plot(horizontal_speed * dense_t, horizontal_height - 0.5 * gravity * dense_t**2, color=F.PURPLE, lw=2.8)
    horizontal_ax.scatter(sample_x, sample_y, s=58, color=F.PURPLE, edgecolors="white", zorder=5)
    horizontal_ax.axhline(0, color=F.INK, lw=1.2)
    for index, (t_state, x_state, y_state) in enumerate(zip(sample_t, sample_x, sample_y)):
        if index == len(sample_t) - 1:
            horizontal_ax.text(x_state - 0.65, y_state + 3.0, rf"${t_state:g}\ \mathrm{{s}}$", fontsize=9.7, ha="right")
        else:
            horizontal_ax.text(x_state + 0.35, y_state + 1.0, rf"${t_state:g}\ \mathrm{{s}}$", fontsize=9.7)
    # 落地速度分量使用同一縮尺：0.18 圖軸單位 / (m/s)。
    velocity_scale = 0.18
    landing = np.array([horizontal_range, 0.0])
    vx_end = landing + velocity_scale * np.array([horizontal_v[0], 0.0])
    vy_end = landing + velocity_scale * np.array([0.0, horizontal_v[1]])
    resultant_end = landing + velocity_scale * horizontal_v
    assert np.isclose(np.linalg.norm(resultant_end - landing), velocity_scale * np.linalg.norm(horizontal_v))
    assert vx_end[0] > landing[0] and np.isclose(vx_end[1], landing[1])
    assert vy_end[1] < landing[1] and np.isclose(vy_end[0], landing[0])
    F.arrow(horizontal_ax, landing, vx_end, color=F.BLUE, lw=2.4, mutation=15)
    F.arrow(horizontal_ax, landing, vy_end, color=F.RED, lw=2.4, mutation=15)
    F.arrow(horizontal_ax, landing, resultant_end, color=F.GREEN, lw=2.7, mutation=16)
    horizontal_ax.text(27.0, 0.75, r"$v_x=8$", color=F.BLUE, fontsize=10.3)
    horizontal_ax.text(22.1, -3.6, r"$v_y=-30$", color=F.RED, fontsize=10.3, ha="right")
    horizontal_ax.text(25.4, -4.6, rf"${horizontal_angle:.1f}^\circ$ 向下", color=F.GREEN, fontsize=10.3)
    horizontal_ax.text(2.0, 5.0, r"$45=\frac{1}{2}gT^2\Rightarrow T=3.0\ \mathrm{s}$", fontsize=10.8)
    horizontal_ax.text(2.0, 1.5, r"$R=v_xT=24\ \mathrm{m}$", fontsize=10.8)
    horizontal_ax.set_xlim(-1.0, 31.0)
    horizontal_ax.set_ylim(-6.5, 48.5)
    horizontal_ax.set_aspect("equal", adjustable="box")
    horizontal_ax.set_xlabel("x (m)")
    horizontal_ax.set_ylabel("y (m)")
    horizontal_ax.set_title("A｜第 4 題：水平拋的共同飛行時間", fontsize=13.2)
    F.clean_grid(horizontal_ax)

    dense_t = np.linspace(0.0, flight_time, 300)
    oblique_ax.plot(oblique_v[0] * dense_t, oblique_v[1] * dense_t - 0.5 * gravity * dense_t**2, color=F.PURPLE, lw=2.8)
    oblique_ax.scatter(state_x, state_y, s=62, color=F.PURPLE, edgecolors="white", zorder=5)
    state_text = [r"$t=0$", r"$t=2.0\ \mathrm{s}$", r"$t=4.0\ \mathrm{s}$"]
    for t_state, x_state, y_state, vy_state, label in zip(state_times, state_x, state_y, state_vy, state_text):
        oblique_ax.text(x_state, y_state + 2.2, label, fontsize=10.2, ha="center")
        arrow_scale = 0.23
        start = np.array([x_state, y_state])
        end_x = start + arrow_scale * np.array([oblique_v[0], 0.0])
        assert end_x[0] > start[0]
        F.arrow(oblique_ax, start, end_x, color=F.BLUE, lw=2.2, mutation=14)
        if not np.isclose(vy_state, 0.0):
            end_y = start + arrow_scale * np.array([0.0, vy_state])
            assert np.sign(end_y[1] - start[1]) == np.sign(vy_state)
            F.arrow(oblique_ax, start, end_y, color=F.RED, lw=2.2, mutation=14)
    oblique_ax.text(30.0, 15.0, r"$v_y=0$", color=F.RED, fontsize=10.5, ha="center")
    oblique_ax.text(30.0, 3.8, r"$x=v_{0x}t$ 與 $y=v_{0y}t-\frac{1}{2}gt^2$ 共用 $t$", fontsize=10.8, ha="center")
    oblique_ax.text(30.0, 0.8, r"$v_{0x}=15$,　$v_{0y}=20\ \mathrm{m/s}$", fontsize=10.8, ha="center")
    oblique_ax.axhline(0, color=F.INK, lw=1.2)
    oblique_ax.set_xlim(-2.0, 64.0)
    oblique_ax.set_ylim(-6.0, 26.0)
    oblique_ax.set_aspect("equal", adjustable="box")
    oblique_ax.set_xlabel("x (m)")
    oblique_ax.set_ylabel("y (m)")
    oblique_ax.set_title("B｜第 5 題：斜拋分量的同一時間", fontsize=13.2)
    F.clean_grid(oblique_ax)

    reconstructed_vx = dx[0] / dt
    reconstructed_vy0 = (data_y[1] - data_y[0] - 0.5 * reconstructed_ay[0] * dt**2) / dt
    dense_data_time = np.linspace(data_time[0], data_time[-1], 240)
    dense_data_x = reconstructed_vx * dense_data_time
    dense_data_y = reconstructed_vy0 * dense_data_time + 0.5 * reconstructed_ay[0] * dense_data_time**2
    assert np.isclose(reconstructed_vx, 8.0)
    assert np.isclose(reconstructed_vy0, 6.0)
    assert np.allclose(
        reconstructed_vy0 * data_time + 0.5 * reconstructed_ay[0] * data_time**2,
        data_y,
    )
    data_ax.plot(dense_data_x, dense_data_y, color=F.PURPLE, lw=2.6)
    data_ax.scatter(data_x, data_y, s=66, color=F.PURPLE, edgecolors="white", zorder=5)
    for idx, (t_state, x_state, y_state) in enumerate(zip(data_time, data_x, data_y)):
        data_ax.text(x_state, y_state + 0.17, rf"$t={t_state:.1f}\ \mathrm{{s}}$", fontsize=10.0, ha="center")
        if idx < len(dx):
            mid_x = (data_x[idx] + data_x[idx + 1]) / 2
            mid_y = (data_y[idx] + data_y[idx + 1]) / 2
            data_ax.text(mid_x, mid_y - 0.28, rf"$\Delta y={dy[idx]:.1f}$", color=F.RED, fontsize=10.2, ha="center")
    data_ax.text(0.05, 2.35, r"$\Delta x=1.6\ \mathrm{m}$ 每段相同 $\Rightarrow v_x=8.0\ \mathrm{m/s}$", color=F.BLUE, fontsize=11.0)
    data_ax.text(0.05, -0.55, r"$\Delta^2y=-0.4\ \mathrm{m}$ 且 $\Delta t=0.20\ \mathrm{s}$", color=F.RED, fontsize=11.0)
    data_ax.text(3.0, -0.55, r"$a_y=\Delta^2y/(\Delta t)^2=-10\ \mathrm{m/s^2}$", color=F.PURPLE, fontsize=11.0)
    data_ax.set_xlim(-0.25, 5.1)
    data_ax.set_ylim(-0.82, 2.70)
    data_ax.set_xlabel("x (m)")
    data_ax.set_ylabel("y (m)")
    data_ax.set_title("C｜第 15 題：等時距位置點重建加速度", fontsize=13.5)
    F.clean_grid(data_ax)

    fig.suptitle("章末列式圖：拋體分量、共同時間與資料重建", fontsize=16, y=0.995)
    fig.subplots_adjust(left=0.065, right=0.975, top=0.91, bottom=0.085)
    _save(fig, "選物I-3", "選物I-3-章末列式圖")


if __name__ == "__main__":
    fig_resolution_interval()
    fig_motion_graph_reading()
    fig_equal_time_graphs()
    fig_freefall_sign()
    fig_relative_velocity()
    fig_incline_experiment_data()
    fig_freefall_experiment_data()
    fig_vector_components()
    fig_vector_construction()
    fig_tangent_normal_acceleration()
    fig_projectile_decomposition()
    fig_projectile_velocity_components()
    fig_linear_motion_solution_panels()
    fig_projectile_solution_panels()
    print("done.")
