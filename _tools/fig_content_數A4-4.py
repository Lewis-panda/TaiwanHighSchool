# -*- coding: utf-8 -*-
"""重生「數A4-4 矩陣」學生講義的章內 SVG。"""

if __name__ == "__main__" and __import__("sys").argv[1:]:
    raise SystemExit("本腳本不接受參數；直接執行即可重生數A4-4章內 SVG。")

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Arc, FancyArrowPatch, Rectangle

import figlib as F


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHAPTER = os.path.join(ROOT, "content", "數學A", "數A4-4")

FIGURE_OUTPUTS = (
    ("fig_gaussian_flow", "數A4-4-高斯消去流程.svg"),
    ("fig_solution_types", "數A4-4-解型分類.svg"),
    ("fig_interpolation", "數A4-4-插值多項式.svg"),
    ("fig_matrix_anatomy", "數A4-4-列行與元素.svg"),
    ("fig_row_column_product", "數A4-4-列乘行.svg"),
    ("fig_data_multiplication", "數A4-4-資料表乘法.svg"),
    ("fig_determinant_area", "數A4-4-行列式與面積.svg"),
    ("fig_inverse_restore", "數A4-4-反方陣復原.svg"),
    ("fig_transition_graph", "數A4-4-轉移狀態圖.svg"),
    ("fig_transition_trend", "數A4-4-轉移長期趨勢.svg"),
    ("fig_basis_transform", "數A4-4-基底決定變換.svg"),
    ("fig_special_transforms", "數A4-4-特殊變換與合成.svg"),
)


def _save(fig, filename):
    stem, extension = os.path.splitext(filename)
    if extension != ".svg" or not stem.startswith("數A4-4-"):
        raise AssertionError("輸出檔名必須是數A4-4章內 SVG")
    return F.save_to(fig, CHAPTER, stem, output_subdir="assets", write_pdf=False)


def _arrow(ax, start, end, color=F.INK, lw=2.0, connectionstyle="arc3"):
    ax.add_patch(FancyArrowPatch(start, end, arrowstyle="-|>", mutation_scale=15,
                                color=color, linewidth=lw, connectionstyle=connectionstyle,
                                shrinkA=2, shrinkB=2))


def _box(ax, xy, width, height, text, edge=F.INK, face="#f6f8fb", fontsize=12):
    x, y = xy
    ax.add_patch(Rectangle((x, y), width, height, facecolor=face, edgecolor=edge, lw=1.8))
    ax.text(x + width / 2, y + height / 2, text, ha="center", va="center", fontsize=fontsize)


def _matrix_text(matrix):
    rows = ["  ".join(f"{v:g}" for v in row) for row in np.asarray(matrix)]
    return "\n".join(rows)


def _clean(ax, xlim=(0, 10), ylim=(0, 6), equal=False):
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    if equal:
        ax.set_aspect("equal", adjustable="box")
    ax.axis("off")


def fig_gaussian_flow():
    initial = np.array([[1, 1, 1, 6], [2, -1, 1, 3], [1, 2, -1, 2]], dtype=float)
    stage1 = initial.copy()
    stage1[1] -= 2 * stage1[0]
    stage1[2] -= stage1[0]
    stage2 = stage1[[0, 2, 1]].copy()
    stage2[2] += 3 * stage2[1]
    assert np.array_equal(stage2, np.array([[1, 1, 1, 6], [0, 1, -2, -4], [0, 0, -7, -21]], dtype=float))
    assert np.allclose(initial[:, :3] @ np.array([1, 2, 3]), initial[:, 3])

    fig, ax = plt.subplots(figsize=(11.0, 5.5))
    _box(ax, (0.3, 1.6), 2.6, 2.6, _matrix_text(initial), F.BLUE, "#eef4ff", 13)
    _box(ax, (4.15, 1.6), 2.6, 2.6, _matrix_text(stage1), F.GREEN, "#eef8f0", 13)
    _box(ax, (8.0, 1.6), 2.6, 2.6, _matrix_text(stage2), F.RED, "#fff0f0", 13)
    _arrow(ax, (2.95, 2.9), (4.05, 2.9), F.INK)
    _arrow(ax, (6.8, 2.9), (7.9, 2.9), F.INK)
    ax.text(3.50, 3.55, r"$R_2\leftarrow R_2-2R_1$", ha="center", fontsize=11)
    ax.text(3.50, 2.15, r"$R_3\leftarrow R_3-R_1$", ha="center", fontsize=11)
    ax.text(7.35, 3.55, r"$R_2\leftrightarrow R_3$", ha="center", fontsize=11)
    ax.text(7.35, 2.15, r"$R_3\leftarrow R_3+3R_2$", ha="center", fontsize=11)
    ax.text(1.6, 1.15, "原增廣矩陣", ha="center", fontsize=12, weight="bold")
    ax.text(5.45, 1.15, "逐行消去", ha="center", fontsize=12, weight="bold")
    ax.text(9.3, 1.15, r"階梯形：$z=3,\ y=2,\ x=1$", ha="center", fontsize=12, weight="bold")
    ax.set_title("高斯消去法以可逆列運算保存解集合，並把係數整理成階梯", fontsize=16)
    _clean(ax, (0, 10.9), (0.6, 5.2))
    fig.tight_layout()
    return _save(fig, "數A4-4-高斯消去流程.svg")


def fig_solution_types():
    cases = [
        (np.array([[1, 0, 0, 1], [0, 1, 0, 2], [0, 0, 1, 3]]), "唯一解", r"$x=1,\ y=2,\ z=3$", F.BLUE),
        (np.array([[1, 0, 2, 1], [0, 1, -1, 2], [0, 0, 0, 0]]), "無限多組解", r"$z=t$ 為自由變數", F.GREEN),
        (np.array([[1, 0, 2, 1], [0, 1, -1, 2], [0, 0, 0, 1]]), "無解", r"$0=1$ 形成矛盾", F.RED),
    ]
    fig, ax = plt.subplots(figsize=(11.0, 5.2))
    for i, (matrix, title, conclusion, color) in enumerate(cases):
        x = 0.35 + 3.55 * i
        _box(ax, (x, 1.65), 2.9, 2.55, _matrix_text(matrix), color, "#f7f8fa", 13)
        ax.text(x + 1.45, 4.55, title, ha="center", fontsize=14, weight="bold", color=color)
        ax.text(x + 1.45, 1.15, conclusion, ha="center", fontsize=12)
    ax.set_title("消去後最後一列與樞紐數量，直接決定方程組的解型", fontsize=16)
    _clean(ax, (0, 10.9), (0.6, 5.1))
    fig.tight_layout()
    return _save(fig, "數A4-4-解型分類.svg")


def fig_interpolation():
    xs = np.array([0.0, 1.0, 2.0])
    ys = np.array([1.0, 3.0, 9.0])
    design = np.column_stack([xs**2, xs, np.ones_like(xs)])
    coeff = np.linalg.solve(design, ys)
    assert np.allclose(coeff, [2, 0, 1])
    grid = np.linspace(-0.35, 2.35, 300)
    fig, axes = plt.subplots(1, 2, figsize=(10.7, 5.1))
    axes[0].plot(grid, coeff[0] * grid**2 + coeff[1] * grid + coeff[2], color=F.BLUE, lw=2.4)
    axes[0].scatter(xs, ys, s=55, color=F.RED, zorder=4)
    for x, y in zip(xs, ys):
        axes[0].annotate(f"({x:g}, {y:g})", (x, y), xytext=(6, 7), textcoords="offset points")
    axes[0].set_xlabel("x")
    axes[0].set_ylabel("y")
    axes[0].set_title(r"三點決定 $f(x)=2x^2+1$")
    F.clean_grid(axes[0])
    _box(axes[1], (0.8, 1.45), 3.3, 2.65, "0  0  1 │ 1\n1  1  1 │ 3\n4  2  1 │ 9", F.GREEN, "#eef8f0", 14)
    axes[1].text(2.45, 0.95, r"$[a,b,c]^T=[2,0,1]^T$", ha="center", fontsize=13)
    axes[1].set_title("代入資料點後形成線性方程組")
    _clean(axes[1], (0, 5), (0.4, 4.8))
    fig.suptitle("插值把『曲線通過資料點』轉成係數的聯立方程組", fontsize=16)
    fig.tight_layout(rect=(0, 0, 1, 0.92))
    return _save(fig, "數A4-4-插值多項式.svg")


def fig_matrix_anatomy():
    values = np.array([[2, -1, 4, 7], [0, 3, 5, 1], [6, 2, -2, 8]])
    fig, ax = plt.subplots(figsize=(9.8, 5.4))
    x0, y0, w, h = 2.1, 1.15, 1.3, 0.95
    for i in range(3):
        for j in range(4):
            face = "#f6f8fb"
            if i == 1:
                face = "#dcecff"
            if j == 2:
                face = "#e3f3e7" if i != 1 else "#d9eee0"
            ax.add_patch(Rectangle((x0+j*w, y0+(2-i)*h), w, h, facecolor=face, edgecolor="#8d99a6", lw=1.2))
            ax.text(x0+(j+0.5)*w, y0+(2-i+0.5)*h, f"{values[i,j]:g}", ha="center", va="center", fontsize=15)
    ax.add_patch(Rectangle((x0+2*w, y0+h), w, h, fill=False, edgecolor=F.RED, lw=3))
    ax.text(1.25, y0+1.5*h, "第 2 列", ha="center", va="center", fontsize=13, color=F.BLUE)
    _arrow(ax, (1.7, y0+1.5*h), (2.05, y0+1.5*h), F.BLUE)
    ax.text(x0+2.5*w, 4.65, "第 3 行", ha="center", fontsize=13, color=F.GREEN)
    _arrow(ax, (x0+2.5*w, 4.35), (x0+2.5*w, 4.05), F.GREEN)
    ax.text(8.1, 2.9, r"$A=[a_{ij}]_{3\times4}$", fontsize=14)
    ax.text(8.1, 2.25, r"$a_{23}=5$", fontsize=15, color=F.RED, weight="bold")
    ax.text(8.1, 1.55, "3 列、4 行", fontsize=13)
    ax.set_title("矩陣用固定的列、行索引保存資料位置", fontsize=16)
    _clean(ax, (0, 10), (0.7, 5.0))
    fig.tight_layout()
    return _save(fig, "數A4-4-列行與元素.svg")


def fig_row_column_product():
    A = np.array([[1, 2, 3], [4, 5, 6]])
    B = np.array([[7, 8], [9, 10], [11, 12]])
    C = A @ B
    assert np.array_equal(C, np.array([[58, 64], [139, 154]]))
    fig, ax = plt.subplots(figsize=(11.0, 5.4))
    _box(ax, (0.35, 1.65), 2.3, 2.35, _matrix_text(A), F.BLUE, "#eef4ff", 14)
    _box(ax, (3.35, 1.15), 2.3, 3.35, _matrix_text(B), F.GREEN, "#eef8f0", 14)
    _box(ax, (8.0, 1.65), 2.3, 2.35, _matrix_text(C), F.RED, "#fff0f0", 14)
    ax.text(2.95, 2.8, "×", fontsize=22, ha="center")
    ax.text(6.25, 2.8, "=", fontsize=22, ha="center")
    ax.text(6.85, 3.55, r"$c_{21}=4(7)+5(9)+6(11)=139$", ha="center", fontsize=12, color=F.RED)
    _arrow(ax, (1.05, 2.10), (7.90, 2.10), F.BLUE, 1.5)
    _arrow(ax, (4.15, 4.15), (7.90, 2.35), F.GREEN, 1.5)
    ax.text(1.5, 1.15, r"$A_{2\times3}$", ha="center", fontsize=13)
    ax.text(4.5, 0.65, r"$B_{3\times2}$", ha="center", fontsize=13)
    ax.text(9.15, 1.15, r"$C_{2\times2}$", ha="center", fontsize=13)
    ax.set_title("乘積的第 $(i,j)$ 元來自 A 的第 i 列與 B 的第 j 行內積", fontsize=16)
    _clean(ax, (0, 10.8), (0.35, 5.05))
    fig.tight_layout()
    return _save(fig, "數A4-4-列乘行.svg")


def fig_data_multiplication():
    quantity = np.array([[10, 4, 2], [6, 8, 3]])
    prices = np.array([[30, 32], [50, 48], [40, 42]])
    totals = quantity @ prices
    assert np.array_equal(totals, np.array([[580, 596], [700, 702]]))
    fig, ax = plt.subplots(figsize=(11.0, 5.3))
    _box(ax, (0.25, 1.55), 2.7, 2.4, "數量表 Q\n\n10   4   2\n 6   8   3", F.BLUE, "#eef4ff", 13)
    _box(ax, (3.55, 1.15), 2.7, 3.2, "單價表 P\n\n30  32\n50  48\n40  42", F.GREEN, "#eef8f0", 13)
    _box(ax, (7.65, 1.55), 3.0, 2.4, "總價表 QP\n\n580   596\n700   702", F.RED, "#fff0f0", 13)
    ax.text(3.25, 2.75, "×", ha="center", fontsize=22)
    ax.text(6.90, 2.75, "=", ha="center", fontsize=22)
    ax.text(1.6, 0.95, "列：班級；行：品項", ha="center", fontsize=11)
    ax.text(4.9, 0.55, "列：品項；行：商家", ha="center", fontsize=11)
    ax.text(9.15, 0.95, "列：班級；行：商家", ha="center", fontsize=11)
    ax.set_title("共享的『品項』索引被加總，矩陣乘法產生每班在各商家的總價", fontsize=16)
    _clean(ax, (0, 10.9), (0.25, 4.9))
    fig.tight_layout()
    return _save(fig, "數A4-4-資料表乘法.svg")


def fig_determinant_area():
    A = np.array([[2.0, 1.0], [1.0, 3.0]])
    det = np.linalg.det(A)
    assert np.isclose(det, 5.0)
    unit = np.array([[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]], dtype=float)
    transformed = unit @ A.T
    fig, axes = plt.subplots(1, 2, figsize=(10.4, 5.2))
    axes[0].fill(unit[:, 0], unit[:, 1], color=F.BLUE, alpha=0.18)
    axes[0].plot(unit[:, 0], unit[:, 1], color=F.BLUE, lw=2.2)
    axes[0].quiver([0, 0], [0, 0], [1, 0], [0, 1], angles="xy", scale_units="xy", scale=1,
                   color=[F.BLUE, F.GREEN], width=0.014)
    axes[0].set_title("單位正方形：面積 1")
    axes[1].fill(transformed[:, 0], transformed[:, 1], color=F.PURPLE, alpha=0.18)
    axes[1].plot(transformed[:, 0], transformed[:, 1], color=F.PURPLE, lw=2.2)
    axes[1].quiver([0, 0], [0, 0], A[0, 0], A[1, 0], angles="xy", scale_units="xy", scale=1,
                   color=F.BLUE, width=0.014)
    axes[1].quiver([0], [0], [A[0, 1]], [A[1, 1]], angles="xy", scale_units="xy", scale=1,
                   color=F.GREEN, width=0.014)
    axes[1].set_title(r"變換後：面積 $|\det A|=5$")
    for ax in axes:
        ax.axhline(0, color=F.INK, lw=0.8)
        ax.axvline(0, color=F.INK, lw=0.8)
        ax.set_aspect("equal", adjustable="box")
        ax.set_xlim(-0.4, 3.5)
        ax.set_ylim(-0.4, 4.5)
        F.clean_grid(ax)
    fig.suptitle("A = [2  1; 1  3] 的兩個直行是基底向量的像；行列式量面積倍率", fontsize=15)
    fig.tight_layout(rect=(0, 0, 1, 0.91))
    return _save(fig, "數A4-4-行列式與面積.svg")


def fig_inverse_restore():
    A = np.array([[2.0, 1.0], [1.0, 3.0]])
    inv = np.linalg.inv(A)
    x = np.array([2.0, 1.0])
    y = A @ x
    restored = inv @ y
    assert np.allclose(inv, np.array([[3, -1], [-1, 2]]) / 5)
    assert np.allclose(y, [5, 5]) and np.allclose(restored, x)
    fig, ax = plt.subplots(figsize=(10.8, 4.9))
    _box(ax, (0.35, 1.45), 2.35, 1.55, "原向量 $X$\n\n$[2,1]^T$", F.BLUE, "#eef4ff", 13)
    _box(ax, (4.2, 1.45), 2.35, 1.55, "觀察值 $Y=AX$\n\n$[5,5]^T$", F.RED, "#fff0f0", 13)
    _box(ax, (8.05, 1.45), 2.35, 1.55, "復原 $A^{-1}Y$\n\n$[2,1]^T$", F.GREEN, "#eef8f0", 13)
    _arrow(ax, (2.75, 2.22), (4.1, 2.22), F.INK)
    _arrow(ax, (6.6, 2.22), (7.95, 2.22), F.INK)
    ax.text(3.42, 3.28, r"$A=[2\ 1;\ 1\ 3]$", ha="center", fontsize=11)
    ax.text(7.28, 3.28, r"$A^{-1}=\frac{1}{5}[3\ {-1};\ {-1}\ 2]$", ha="center", fontsize=10.5)
    ax.text(5.4, 0.75, r"$A^{-1}AX=IX=X$", ha="center", fontsize=14, weight="bold")
    ax.set_title("可逆矩陣保存全部二維資訊；反方陣把變換結果送回原輸入", fontsize=16)
    _clean(ax, (0, 10.8), (0.4, 4.2))
    fig.tight_layout()
    return _save(fig, "數A4-4-反方陣復原.svg")


def fig_transition_graph():
    A = np.array([[0.8, 0.3], [0.2, 0.7]])
    assert np.allclose(A.sum(axis=0), 1)
    fig, ax = plt.subplots(figsize=(9.8, 5.2))
    centers = {"甲": (2.5, 2.6), "乙": (7.2, 2.6)}
    for name, (x, y) in centers.items():
        ax.add_patch(plt.Circle((x, y), 0.72, facecolor="#eef4ff" if name == "甲" else "#eef8f0",
                                edgecolor=F.BLUE if name == "甲" else F.GREEN, lw=2.2))
        ax.text(x, y, name, ha="center", va="center", fontsize=16, weight="bold")
    _arrow(ax, (3.2, 2.95), (6.5, 2.95), F.RED, 2.0, "arc3,rad=-0.16")
    _arrow(ax, (6.5, 2.25), (3.2, 2.25), F.PURPLE, 2.0, "arc3,rad=-0.16")
    ax.text(4.85, 3.62, r"甲 $\to$ 乙：0.20", ha="center", color=F.RED, fontsize=12)
    ax.text(4.85, 1.58, r"乙 $\to$ 甲：0.30", ha="center", color=F.PURPLE, fontsize=12)
    ax.add_patch(Arc((2.5, 2.6), 2.2, 2.4, theta1=65, theta2=295, color=F.BLUE, lw=2))
    _arrow(ax, (1.68, 3.32), (1.82, 3.55), F.BLUE, 2.0)
    ax.add_patch(Arc((7.2, 2.6), 2.2, 2.4, theta1=-115, theta2=115, color=F.GREEN, lw=2))
    _arrow(ax, (8.02, 1.88), (7.88, 1.65), F.GREEN, 2.0)
    ax.text(1.15, 4.25, r"甲 $\to$ 甲：0.80", color=F.BLUE, fontsize=12)
    ax.text(7.15, 4.25, r"乙 $\to$ 乙：0.70", color=F.GREEN, fontsize=12)
    ax.text(4.85, 0.75, "A = [0.8  0.3; 0.2  0.7]；每一行（直行）總和為 1", ha="center", fontsize=13)
    ax.set_title("轉移矩陣的第 $(i,j)$ 元記錄『目前在 j，下一期到 i』的機率", fontsize=16)
    _clean(ax, (0, 9.8), (0.35, 4.8), equal=True)
    fig.tight_layout()
    return _save(fig, "數A4-4-轉移狀態圖.svg")


def fig_transition_trend():
    A = np.array([[0.8, 0.3], [0.2, 0.7]])
    x = np.array([1.0, 0.0])
    values = [x.copy()]
    for _ in range(12):
        x = A @ x
        values.append(x.copy())
    values = np.array(values)
    assert np.allclose(values.sum(axis=1), 1)
    assert np.allclose(A @ np.array([0.6, 0.4]), [0.6, 0.4])
    fig, ax = plt.subplots(figsize=(10.4, 5.2))
    n = np.arange(len(values))
    ax.plot(n, values[:, 0], marker="o", color=F.BLUE, lw=2.2, label="甲狀態比例")
    ax.plot(n, values[:, 1], marker="s", color=F.GREEN, lw=2.2, label="乙狀態比例")
    ax.axhline(0.6, color=F.BLUE, ls="--", alpha=0.75)
    ax.axhline(0.4, color=F.GREEN, ls="--", alpha=0.75)
    ax.set_xticks(n)
    ax.set_ylim(0, 1.02)
    ax.set_xlabel("期數 n")
    ax.set_ylabel("狀態比例")
    ax.legend()
    F.clean_grid(ax)
    ax.set_title(r"反覆使用 $X_{n+1}=AX_n$；本例逐步接近穩定向量 $[0.6,0.4]^T$", fontsize=15)
    fig.tight_layout()
    return _save(fig, "數A4-4-轉移長期趨勢.svg")


def fig_basis_transform():
    A = np.array([[2.0, 1.0], [1.0, 2.0]])
    e1, e2 = np.eye(2)
    assert np.allclose(A @ e1, A[:, 0]) and np.allclose(A @ e2, A[:, 1])
    fig, axes = plt.subplots(1, 2, figsize=(10.4, 5.2))
    for ax in axes:
        ax.axhline(0, color=F.INK, lw=0.8)
        ax.axvline(0, color=F.INK, lw=0.8)
        ax.set_xlim(-0.5, 3.6)
        ax.set_ylim(-0.5, 3.6)
        ax.set_aspect("equal", adjustable="box")
        F.clean_grid(ax)
    axes[0].quiver([0, 0], [0, 0], [1, 0], [0, 1], angles="xy", scale_units="xy", scale=1,
                   color=[F.BLUE, F.GREEN], width=0.015)
    axes[0].text(1.08, 0.05, r"$e_1$", color=F.BLUE)
    axes[0].text(0.05, 1.08, r"$e_2$", color=F.GREEN)
    axes[0].set_title("輸入基底")
    axes[1].quiver([0, 0], [0, 0], A[0, :], A[1, :], angles="xy", scale_units="xy", scale=1,
                   color=[F.BLUE, F.GREEN], width=0.015)
    axes[1].text(2.05, 1.05, r"$Ae_1=(2,1)$", color=F.BLUE)
    axes[1].text(1.05, 2.08, r"$Ae_2=(1,2)$", color=F.GREEN)
    axes[1].set_title("矩陣的兩個直行就是基底的像")
    fig.suptitle(r"任意 $(x,y)=xe_1+ye_2$，所以 $A(x,y)=xAe_1+yAe_2$", fontsize=16)
    fig.tight_layout(rect=(0, 0, 1, 0.91))
    return _save(fig, "數A4-4-基底決定變換.svg")


def fig_special_transforms():
    polygon = np.array([[0, 0], [1.8, 0], [1.4, 0.8], [0.6, 1.5], [0, 0.8], [0, 0]], dtype=float)
    transforms = [
        ("原圖", np.eye(2)),
        ("伸縮", np.array([[1.5, 0], [0, 0.7]])),
        ("對 y=x 鏡射", np.array([[0, 1], [1, 0]])),
        ("逆時針 45°", np.array([[np.sqrt(2)/2, -np.sqrt(2)/2], [np.sqrt(2)/2, np.sqrt(2)/2]])),
        ("水平推移", np.array([[1, 0.8], [0, 1]])),
    ]
    transforms.append(("先伸縮再旋轉", transforms[3][1] @ transforms[1][1]))
    assert np.isclose(abs(np.linalg.det(transforms[1][1])), 1.05)
    assert np.isclose(np.linalg.det(transforms[2][1]), -1)
    assert np.isclose(np.linalg.det(transforms[3][1]), 1)
    assert np.isclose(np.linalg.det(transforms[4][1]), 1)
    fig, axes = plt.subplots(2, 3, figsize=(11.0, 7.0))
    for ax, (title, matrix) in zip(axes.flat, transforms):
        points = polygon @ matrix.T
        ax.fill(points[:, 0], points[:, 1], color=F.BLUE, alpha=0.18, hatch="//")
        ax.plot(points[:, 0], points[:, 1], color=F.BLUE, lw=2.1)
        ax.scatter(points[:-1, 0], points[:-1, 1], color=F.RED, s=22)
        ax.axhline(0, color=F.INK, lw=0.7)
        ax.axvline(0, color=F.INK, lw=0.7)
        ax.set_xlim(-1.8, 3.2)
        ax.set_ylim(-1.2, 3.0)
        ax.set_aspect("equal", adjustable="box")
        ax.set_title(title, fontsize=12)
        ax.set_xticks([])
        ax.set_yticks([])
    fig.suptitle("基本線性變換由矩陣控制；合成時右側矩陣先作用", fontsize=16)
    fig.tight_layout(rect=(0, 0, 1, 0.94))
    return _save(fig, "數A4-4-特殊變換與合成.svg")


def main():
    generated = []
    for function_name, filename in FIGURE_OUTPUTS:
        function = globals()[function_name]
        result = function()
        generated.append(os.path.basename(result))
    expected = [filename for _, filename in FIGURE_OUTPUTS]
    if generated != expected:
        raise AssertionError(f"圖檔輸出順序不符：{generated!r}")
    if len(set(generated)) != len(generated):
        raise AssertionError("圖檔名稱重複")


if __name__ == "__main__":
    main()
