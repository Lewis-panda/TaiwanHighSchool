# -*- coding: utf-8 -*-
r"""產生「數A4-2 矩陣」的圖，輸出到該章 sources/。
重繪：  .venv/bin/python _tools/fig_數A4-2.py

注意：mathtext 不支援 \dfrac/\tfrac；圖內中文不放在 $...$ 內。
線性變換圖一律 set_aspect("equal")，畫單位方格變換前後。
"""

import os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, FancyArrowPatch
import figlib as F

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CH = os.path.join(ROOT, "數學", "數學二下（數學A·第四冊）", "數A4-2 矩陣")


def _draw_grid_cells(ax, M, color, alpha=0.10, nx=3, ny=3, lw=1.2):
    """把 [0,nx]x[0,ny] 的單位方格，經過 2x2 矩陣 M 變換後畫出來。"""
    M = np.asarray(M, dtype=float)

    def T(p):
        return M @ np.asarray(p, dtype=float)

    # 填一個代表性單位方格（0,0)-(1,1) 變換後
    cell = np.array([[0, 0], [1, 0], [1, 1], [0, 1]], dtype=float)
    tcell = np.array([T(p) for p in cell])
    ax.add_patch(
        Polygon(
            tcell, closed=True, facecolor=color, alpha=0.30, edgecolor="none", zorder=2
        )
    )
    # 整片方格線
    for i in range(nx + 1):
        p0, p1 = T([i, 0]), T([i, ny])
        ax.plot([p0[0], p1[0]], [p0[1], p1[1]], color=color, lw=lw, alpha=0.9, zorder=1)
    for j in range(ny + 1):
        p0, p1 = T([0, j]), T([nx, j])
        ax.plot([p0[0], p1[0]], [p0[1], p1[1]], color=color, lw=lw, alpha=0.9, zorder=1)
    # 基底像 e1', e2'
    F.arrow(ax, [0, 0], T([1, 0]), color=color, lw=2.6, z=6)
    F.arrow(ax, [0, 0], T([0, 1]), color=color, lw=2.6, z=6)


def fig_linear_transform():
    """單位方格 → 經矩陣變換後（伸縮 + 推移 的綜合範例）。"""
    fig, axes = plt.subplots(1, 2, figsize=(11.4, 5.2))

    # 左：變換前（單位方格 + 基底）
    ax = axes[0]
    ax.set_aspect("equal")
    _draw_grid_cells(ax, [[1, 0], [0, 1]], F.BLUE)
    ax.text(0.5, -0.42, "e1 = (1, 0)", color=F.BLUE, fontsize=12, ha="center")
    ax.text(
        -0.5, 0.5, "e2 =\n(0, 1)", color=F.BLUE, fontsize=12, ha="center", va="center"
    )
    ax.text(0.5, 0.5, "單位\n方格", color=F.INK, fontsize=12, ha="center", va="center")
    ax.set_title("變換前：單位方格", fontsize=14)
    ax.set_xlim(-1.2, 4.0)
    ax.set_ylim(-1.0, 4.0)
    F.clean_grid(ax)

    # 右：經 M = [[1,1],[0,1]] 推移 與 [[2,0],[0,1]] 拉伸 綜合 → [[2,1],[0,1.4]]
    M = [[2, 1], [0, 1.4]]
    ax = axes[1]
    ax.set_aspect("equal")
    _draw_grid_cells(ax, M, F.RED)
    e1 = np.array(M)[:, 0]
    e2 = np.array(M)[:, 1]
    ax.text(
        e1[0] * 0.6,
        e1[1] - 0.42,
        "e1 的像\n(2, 0)",
        color=F.RED,
        fontsize=11,
        ha="center",
        va="top",
    )
    ax.text(
        e2[0] + 0.15,
        e2[1] * 0.55,
        "e2 的像\n(1, 1.4)",
        color=F.RED,
        fontsize=11,
        ha="left",
        va="center",
    )
    ax.text(2.2, 3.4, "M = [[2, 1], [0, 1.4]]", color=F.INK, fontsize=12, ha="center")
    ax.set_title("變換後：方格被拉伸＋推移", fontsize=14)
    ax.set_xlim(-1.2, 5.4)
    ax.set_ylim(-1.0, 4.0)
    F.clean_grid(ax)

    fig.tight_layout()
    F.save_to(fig, CH, "數A4-2-線性變換")


def fig_rotation_reflection():
    """旋轉與鏡射：對同一個 L 形圖樣作用。"""
    fig, axes = plt.subplots(1, 2, figsize=(11.4, 5.2))

    # 一個不對稱的「L 形」圖樣，方便看出旋轉/鏡射
    shape = np.array(
        [[0, 0], [1.6, 0], [1.6, 0.5], [0.5, 0.5], [0.5, 1.8], [0, 1.8]], dtype=float
    )

    def apply(M, pts):
        M = np.asarray(M, dtype=float)
        return np.array([M @ p for p in pts])

    # 左：旋轉 90 度
    ax = axes[0]
    ax.set_aspect("equal")
    th = np.deg2rad(90)
    R = [[np.cos(th), -np.sin(th)], [np.sin(th), np.cos(th)]]
    ax.add_patch(
        Polygon(
            shape, closed=True, facecolor=F.BLUE, alpha=0.22, edgecolor=F.BLUE, lw=2.0
        )
    )
    ax.add_patch(
        Polygon(
            apply(R, shape),
            closed=True,
            facecolor=F.RED,
            alpha=0.22,
            edgecolor=F.RED,
            lw=2.0,
        )
    )
    ax.text(0.8, 0.2, "原圖", color=F.BLUE, fontsize=12, ha="center")
    ax.text(
        -0.9, 0.8, "旋轉\n90°後", color=F.RED, fontsize=12, ha="center", va="center"
    )
    ax.text(0, -2.0, "R = [[0, -1], [1, 0]]", color=F.INK, fontsize=12, ha="center")
    ax.axhline(0, color=F.GRID, lw=1.0, zorder=0)
    ax.axvline(0, color=F.GRID, lw=1.0, zorder=0)
    ax.set_title("旋轉 90°（繞原點逆時針）", fontsize=14)
    ax.set_xlim(-2.2, 2.2)
    ax.set_ylim(-2.4, 2.4)
    F.clean_grid(ax)

    # 右：對 x 軸鏡射
    ax = axes[1]
    ax.set_aspect("equal")
    S = [[1, 0], [0, -1]]
    ax.add_patch(
        Polygon(
            shape, closed=True, facecolor=F.BLUE, alpha=0.22, edgecolor=F.BLUE, lw=2.0
        )
    )
    ax.add_patch(
        Polygon(
            apply(S, shape),
            closed=True,
            facecolor=F.GREEN,
            alpha=0.22,
            edgecolor=F.GREEN,
            lw=2.0,
        )
    )
    ax.text(0.8, 0.5, "原圖", color=F.BLUE, fontsize=12, ha="center")
    ax.text(0.8, -0.5, "鏡射後", color=F.GREEN, fontsize=12, ha="center")
    ax.axhline(0, color=F.AMBER, lw=1.6, zorder=1)
    ax.text(2.0, 0.12, "鏡射軸 (x 軸)", color=F.AMBER, fontsize=11, ha="right")
    ax.axvline(0, color=F.GRID, lw=1.0, zorder=0)
    ax.text(0, -2.3, "S = [[1, 0], [0, -1]]", color=F.INK, fontsize=12, ha="center")
    ax.set_title("對 x 軸鏡射", fontsize=14)
    ax.set_xlim(-1.0, 2.4)
    ax.set_ylim(-2.6, 2.2)
    F.clean_grid(ax)

    fig.tight_layout()
    F.save_to(fig, CH, "數A4-2-旋轉鏡射")


def fig_three_cases():
    """二元一次方程組解的三種情況：交於一點 / 重合 / 平行。"""
    fig, axes = plt.subplots(1, 3, figsize=(13.2, 4.6))
    x = np.linspace(-1, 5, 200)

    # (1) 唯一解：兩線交於一點
    ax = axes[0]
    ax.set_aspect("equal")
    # x + y = 4 ; x - y = 0  -> 交於 (2,2)
    ax.plot(x, 4 - x, color=F.BLUE, lw=2.4, label="x + y = 4")
    ax.plot(x, x, color=F.RED, lw=2.4, label="x − y = 0")
    ax.plot([2], [2], "o", color=F.INK, ms=9, zorder=6)
    ax.text(2.25, 2.1, "(2, 2)", color=F.INK, fontsize=12)
    ax.set_title("唯一解：交於一點\n(行列式 ≠ 0)", fontsize=13)
    ax.legend(loc="lower left", fontsize=10)

    # (2) 無窮多解：兩線重合
    ax = axes[1]
    ax.set_aspect("equal")
    ax.plot(x, 4 - x, color=F.BLUE, lw=5.0, alpha=0.45)
    ax.plot(x, 4 - x, color=F.RED, lw=2.0, ls="--")
    ax.text(2.2, 2.6, "兩線重合", color=F.INK, fontsize=12, ha="center")
    ax.set_title("無窮多解：兩線重合\n(行列式 = 0，相容)", fontsize=13)

    # (3) 無解：兩線平行不相交
    ax = axes[2]
    ax.set_aspect("equal")
    ax.plot(x, 4 - x, color=F.BLUE, lw=2.4, label="x + y = 4")
    ax.plot(x, 2 - x, color=F.RED, lw=2.4, label="x + y = 2")
    ax.text(2.4, 3.1, "平行\n不相交", color=F.INK, fontsize=12, ha="center")
    ax.set_title("無解：兩線平行\n(行列式 = 0，矛盾)", fontsize=13)
    ax.legend(loc="lower left", fontsize=10)

    for ax in axes:
        ax.set_xlim(-1, 5)
        ax.set_ylim(-1, 5)
        ax.axhline(0, color=F.GRID, lw=1.0, zorder=0)
        ax.axvline(0, color=F.GRID, lw=1.0, zorder=0)
        F.clean_grid(ax)

    fig.tight_layout()
    F.save_to(fig, CH, "數A4-2-方程組三情況")


def fig_markov():
    """二階轉移方陣：狀態分布隨步數演化，趨向穩定分布。"""
    fig, ax = F.canvas(7.2, 4.6)
    # 轉移矩陣（行向量為機率分布，左乘列向量習慣這裡用 v_{n+1}=P v_n）
    # 晴->晴 0.8, 晴->雨 0.2 ; 雨->晴 0.4, 雨->雨 0.6
    P = np.array([[0.8, 0.4], [0.2, 0.6]])
    v = np.array([1.0, 0.0])  # 第 0 天：晴
    steps = 8
    sunny, rainy = [], []
    for n in range(steps + 1):
        sunny.append(v[0])
        rainy.append(v[1])
        v = P @ v
    ns = np.arange(steps + 1)
    ax.plot(ns, sunny, "o-", color=F.BLUE, lw=2.4, ms=7, label="晴天機率")
    ax.plot(ns, rainy, "s-", color=F.AMBER, lw=2.4, ms=7, label="雨天機率")
    # 穩定值 (2/3, 1/3)
    ax.axhline(2 / 3, color=F.BLUE, lw=1.2, ls="--", alpha=0.7)
    ax.axhline(1 / 3, color=F.AMBER, lw=1.2, ls="--", alpha=0.7)
    ax.text(steps, 2 / 3 + 0.03, "穩定 2/3", color=F.BLUE, fontsize=11, ha="right")
    ax.text(steps, 1 / 3 + 0.03, "穩定 1/3", color=F.AMBER, fontsize=11, ha="right")
    ax.set_xlabel("第 n 天", fontsize=12)
    ax.set_ylabel("機率", fontsize=12)
    ax.set_ylim(0, 1.05)
    ax.set_title("轉移方陣：天氣狀態趨向穩定分布", fontsize=14)
    ax.legend(loc="center right", fontsize=11)
    F.clean_grid(ax)
    F.save_to(fig, CH, "數A4-2-轉移方陣")


if __name__ == "__main__":
    fig_linear_transform()
    fig_rotation_reflection()
    fig_three_cases()
    fig_markov()
    print("done.")
