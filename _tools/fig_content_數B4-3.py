# -*- coding: utf-8 -*-
"""重生「數B4-3 矩陣」學生講義的章內 SVG。"""

if __name__ == "__main__" and __import__("sys").argv[1:]:
    raise SystemExit("本腳本不接受參數；直接執行即可重生數B4-3 章內 SVG。")

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Rectangle
import numpy as np

import figlib as F


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHAPTER = os.path.join(ROOT, "content", "數學B", "數B4-3")

FIGURE_OUTPUTS = (
    ("fig_matrix_anatomy", "數B4-3-列行與元素.svg"),
    ("fig_table_semantics", "數B4-3-資料表與矩陣索引.svg"),
    ("fig_entrywise_update", "數B4-3-逐項運算與庫存更新.svg"),
    ("fig_row_column_product", "數B4-3-列乘行.svg"),
    ("fig_cost_model", "數B4-3-數量單價總額.svg"),
    ("fig_dimension_chain", "數B4-3-乘法階數鏈.svg"),
    ("fig_order_comparison", "數B4-3-乘法順序比較.svg"),
    ("fig_power_cycle", "數B4-3-矩陣冪週期.svg"),
    ("fig_inverse_mechanism", "數B4-3-二階反方陣機制.svg"),
    ("fig_system_geometry", "數B4-3-方程組解型.svg"),
    ("fig_vector_combination", "數B4-3-向量線性組合.svg"),
    ("fig_affine_calibration", "數B4-3-仿射校正參考點.svg"),
    ("fig_cipher_flow", "數B4-3-編碼與復原.svg"),
)


def _save(fig, filename):
    stem, extension = os.path.splitext(filename)
    if extension != ".svg" or not stem.startswith("數B4-3-"):
        raise AssertionError("輸出檔名必須是數B4-3章內 SVG")
    return F.save_to(fig, CHAPTER, stem, output_subdir="assets", write_pdf=False)


def _clean(ax, xlim=(0, 10), ylim=(0, 6), equal=False):
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    if equal:
        ax.set_aspect("equal", adjustable="box")
    ax.axis("off")


def _arrow(ax, start, end, color=F.INK, lw=2.0, connectionstyle="arc3"):
    ax.add_patch(
        FancyArrowPatch(
            start,
            end,
            arrowstyle="-|>",
            mutation_scale=15,
            color=color,
            linewidth=lw,
            connectionstyle=connectionstyle,
            shrinkA=2,
            shrinkB=2,
        )
    )


def _box(ax, xy, width, height, text, edge=F.INK, face="#f6f8fb", fontsize=12):
    x, y = xy
    ax.add_patch(Rectangle((x, y), width, height, facecolor=face, edgecolor=edge, lw=1.8))
    ax.text(x + width / 2, y + height / 2, text, ha="center", va="center", fontsize=fontsize)


def _matrix_text(matrix, fmt="g"):
    values = np.asarray(matrix)
    return "\n".join("   ".join(format(v, fmt) for v in row) for row in values)


def _axes(ax, lim=(-1, 7, -1, 7)):
    xmin, xmax, ymin, ymax = lim
    ax.axhline(0, color=F.INK, lw=0.9)
    ax.axvline(0, color=F.INK, lw=0.9)
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)
    ax.set_aspect("equal", adjustable="box")
    F.clean_grid(ax)


def fig_matrix_anatomy():
    values = np.array([[12, 8, 5, 9], [7, 11, 6, 4], [10, 3, 8, 13]])
    assert values.shape == (3, 4)
    assert values[1, 2] == 6
    fig, ax = plt.subplots(figsize=(10.4, 5.4))
    x0, y0, width, height = 2.1, 1.15, 1.35, 0.95
    for i in range(3):
        for j in range(4):
            face = "#f6f8fb"
            if i == 1:
                face = "#dcecff"
            if j == 2:
                face = "#e3f3e7" if i != 1 else "#d9eee0"
            ax.add_patch(
                Rectangle(
                    (x0 + j * width, y0 + (2 - i) * height),
                    width,
                    height,
                    facecolor=face,
                    edgecolor="#8d99a6",
                    lw=1.2,
                )
            )
            ax.text(
                x0 + (j + 0.5) * width,
                y0 + (2 - i + 0.5) * height,
                str(values[i, j]),
                ha="center",
                va="center",
                fontsize=15,
            )
    ax.add_patch(Rectangle((x0 + 2 * width, y0 + height), width, height, fill=False, edgecolor=F.RED, lw=3))
    ax.text(1.25, y0 + 1.5 * height, "第 2 列", ha="center", va="center", fontsize=13, color=F.BLUE)
    _arrow(ax, (1.72, y0 + 1.5 * height), (2.05, y0 + 1.5 * height), F.BLUE)
    ax.text(x0 + 2.5 * width, 4.62, "第 3 行", ha="center", fontsize=13, color=F.GREEN)
    _arrow(ax, (x0 + 2.5 * width, 4.35), (x0 + 2.5 * width, 4.04), F.GREEN)
    ax.text(8.05, 3.05, r"$A=[a_{ij}]_{3\times4}$", fontsize=14)
    ax.text(8.05, 2.35, r"$a_{23}=6$", fontsize=15, color=F.RED, weight="bold")
    ax.text(8.05, 1.62, "3 列、4 行", fontsize=13)
    ax.set_title("矩陣用列、行與元素位置保存資料結構", fontsize=16)
    _clean(ax, (0, 10.4), (0.65, 5.0))
    fig.tight_layout()
    return _save(fig, "數B4-3-列行與元素.svg")


def fig_table_semantics():
    data = np.array([[28, 16, 12], [25, 20, 15], [31, 18, 14]])
    row_totals = data.sum(axis=1)
    column_totals = data.sum(axis=0)
    assert np.array_equal(row_totals, [56, 60, 63])
    assert np.array_equal(column_totals, [84, 54, 41])
    fig, ax = plt.subplots(figsize=(10.8, 5.6))
    x0, y0, w, h = 2.25, 1.25, 1.45, 0.9
    row_names = ["甲班", "乙班", "丙班"]
    col_names = ["公車", "步行", "單車"]
    for j, name in enumerate(col_names):
        ax.text(x0 + (j + 0.5) * w, y0 + 3.35 * h, name, ha="center", fontsize=12, weight="bold")
    for i, name in enumerate(row_names):
        ax.text(x0 - 0.35, y0 + (2 - i + 0.5) * h, name, ha="right", va="center", fontsize=12, weight="bold")
    for i in range(3):
        for j in range(3):
            ax.add_patch(Rectangle((x0 + j * w, y0 + (2 - i) * h), w, h, facecolor="#eef4ff", edgecolor=F.GRID))
            ax.text(x0 + (j + 0.5) * w, y0 + (2 - i + 0.5) * h, str(data[i, j]), ha="center", va="center", fontsize=14)
    _arrow(ax, (6.95, 2.65), (8.0, 2.65), F.INK)
    _box(ax, (8.05, 1.45), 2.1, 2.45, _matrix_text(data), F.BLUE, "#eef4ff", 14)
    ax.text(4.4, 0.72, f"各班合計：{row_totals.tolist()}；各方式合計：{column_totals.tolist()}", ha="center", fontsize=11.5)
    ax.text(9.1, 0.72, "拿掉標籤後，位置順序仍須固定", ha="center", fontsize=11.5, color=F.RED)
    ax.set_title("資料表轉成矩陣時，列標籤與行標籤決定每個數字的意義", fontsize=16)
    _clean(ax, (0, 10.7), (0.35, 5.0))
    fig.tight_layout()
    return _save(fig, "數B4-3-資料表與矩陣索引.svg")


def fig_entrywise_update():
    opening = np.array([[42, 30], [35, 28]])
    incoming = np.array([[12, 8], [10, 9]])
    sold = np.array([[18, 11], [13, 12]])
    closing = opening + incoming - sold
    assert np.array_equal(closing, np.array([[36, 27], [32, 25]]))
    fig, ax = plt.subplots(figsize=(11.0, 5.2))
    boxes = [
        ((0.25, 1.55), "期初 $S$\n\n42  30\n35  28", F.BLUE, "#eef4ff"),
        ((3.0, 1.55), "進貨 $P$\n\n12   8\n10   9", F.GREEN, "#eef8f0"),
        ((5.75, 1.55), "銷售 $Q$\n\n18  11\n13  12", F.RED, "#fff0f0"),
        ((8.5, 1.55), "期末 $S+P-Q$\n\n36  27\n32  25", F.PURPLE, "#f4effa"),
    ]
    for xy, label, edge, face in boxes:
        _box(ax, xy, 2.2, 2.4, label, edge, face, 12.5)
    ax.text(2.70, 2.75, "+", fontsize=22, ha="center")
    ax.text(5.45, 2.75, "−", fontsize=22, ha="center")
    ax.text(8.20, 2.75, "=", fontsize=22, ha="center")
    ax.text(5.5, 0.85, "同一位置代表同一門市、同一品項，因此逐項相加減", ha="center", fontsize=12)
    ax.set_title("逐項運算把同索引的資料更新成新的資料表", fontsize=16)
    _clean(ax, (0, 11), (0.4, 4.65))
    fig.tight_layout()
    return _save(fig, "數B4-3-逐項運算與庫存更新.svg")


def fig_row_column_product():
    left = np.array([[2, 1, 3], [4, 0, 2]])
    right = np.array([[30, 35], [50, 45], [20, 25]])
    product = left @ right
    assert np.array_equal(product, np.array([[170, 190], [160, 190]]))
    fig, ax = plt.subplots(figsize=(11.0, 5.4))
    _box(ax, (0.35, 1.65), 2.3, 2.35, _matrix_text(left), F.BLUE, "#eef4ff", 14)
    _box(ax, (3.35, 1.15), 2.3, 3.35, _matrix_text(right), F.GREEN, "#eef8f0", 14)
    _box(ax, (8.0, 1.65), 2.3, 2.35, _matrix_text(product), F.RED, "#fff0f0", 14)
    ax.text(2.95, 2.8, "×", fontsize=22, ha="center")
    ax.text(6.25, 2.8, "=", fontsize=22, ha="center")
    ax.text(6.90, 3.62, r"$c_{12}=2(35)+1(45)+3(25)=190$", ha="center", fontsize=12, color=F.RED)
    _arrow(ax, (1.0, 3.45), (7.88, 3.45), F.BLUE, 1.6)
    _arrow(ax, (4.85, 4.15), (7.90, 3.70), F.GREEN, 1.6)
    ax.text(1.5, 1.15, r"$A_{2\times3}$", ha="center", fontsize=13)
    ax.text(4.5, 0.65, r"$B_{3\times2}$", ha="center", fontsize=13)
    ax.text(9.15, 1.15, r"$C_{2\times2}$", ha="center", fontsize=13)
    ax.set_title("乘積第 $(i,j)$ 元由左矩陣第 $i$ 列與右矩陣第 $j$ 行配對", fontsize=16)
    _clean(ax, (0, 10.8), (0.35, 5.05))
    fig.tight_layout()
    return _save(fig, "數B4-3-列乘行.svg")


def fig_cost_model():
    quantities = np.array([[3, 2, 1], [1, 4, 2]])
    prices = np.array([[40, 45], [30, 32], [25, 28]])
    totals = quantities @ prices
    assert np.array_equal(totals, np.array([[205, 227], [210, 229]]))
    fig, ax = plt.subplots(figsize=(11.0, 5.3))
    _box(ax, (0.25, 1.55), 2.7, 2.4, "數量表 $Q$\n\n3   2   1\n1   4   2", F.BLUE, "#eef4ff", 13)
    _box(ax, (3.55, 1.15), 2.7, 3.2, "單價表 $P$\n\n40  45\n30  32\n25  28", F.GREEN, "#eef8f0", 13)
    _box(ax, (7.65, 1.55), 3.0, 2.4, "總額表 $QP$\n\n205   227\n210   229", F.RED, "#fff0f0", 13)
    ax.text(3.25, 2.75, "×", ha="center", fontsize=22)
    ax.text(6.90, 2.75, "=", ha="center", fontsize=22)
    ax.text(1.6, 0.92, "列：學生；行：品項", ha="center", fontsize=11)
    ax.text(4.9, 0.50, "列：品項；行：商店", ha="center", fontsize=11)
    ax.text(9.15, 0.92, "列：學生；行：商店", ha="center", fontsize=11)
    ax.set_title("共享的品項索引被加總，留下學生與商店兩個外部索引", fontsize=16)
    _clean(ax, (0, 10.9), (0.25, 4.9))
    fig.tight_layout()
    return _save(fig, "數B4-3-數量單價總額.svg")


def fig_dimension_chain():
    shapes = [(4, 3), (3, 2), (2, 5)]
    assert shapes[0][1] == shapes[1][0]
    assert shapes[1][1] == shapes[2][0]
    assert (shapes[0][0], shapes[2][1]) == (4, 5)
    fig, ax = plt.subplots(figsize=(10.8, 4.8))
    labels = [(r"$A_{4\times3}$", 0.45, F.BLUE), (r"$B_{3\times2}$", 3.45, F.GREEN), (r"$C_{2\times5}$", 6.45, F.RED)]
    for label, x, color in labels:
        _box(ax, (x, 1.55), 2.05, 1.55, label, color, "#f7f8fa", 16)
    ax.text(2.95, 2.35, "×", fontsize=22, ha="center")
    ax.text(5.95, 2.35, "×", fontsize=22, ha="center")
    _arrow(ax, (1.45, 1.15), (4.45, 1.15), F.PURPLE, 1.7, "arc3,rad=0.22")
    _arrow(ax, (4.45, 0.80), (7.45, 0.80), F.PURPLE, 1.7, "arc3,rad=0.22")
    ax.text(2.95, 0.48, "內側 3 相等", ha="center", color=F.PURPLE, fontsize=11.5)
    ax.text(5.95, 0.15, "內側 2 相等", ha="center", color=F.PURPLE, fontsize=11.5)
    _box(ax, (9.05, 1.55), 1.35, 1.55, "$4\\times5$", F.INK, "#fff8e8", 16)
    ax.text(8.75, 2.35, "→", fontsize=22, ha="center")
    ax.text(5.4, 3.72, r"$(AB)C=A(BC)$；兩條路都得到 $4\times5$", ha="center", fontsize=13)
    ax.set_title("矩陣相乘先配對內側階數，乘積保留外側階數", fontsize=16)
    _clean(ax, (0, 10.7), (-0.05, 4.25))
    fig.tight_layout()
    return _save(fig, "數B4-3-乘法階數鏈.svg")


def fig_order_comparison():
    first = np.array([[1, 2], [0, 1]])
    second = np.array([[2, 0], [1, 1]])
    ab = first @ second
    ba = second @ first
    assert np.array_equal(ab, np.array([[4, 2], [1, 1]]))
    assert np.array_equal(ba, np.array([[2, 4], [1, 3]]))
    assert not np.array_equal(ab, ba)
    fig, ax = plt.subplots(figsize=(10.8, 5.0))
    _box(ax, (0.4, 2.35), 2.05, 1.55, "$A$\n\n1  2\n0  1", F.BLUE, "#eef4ff", 13)
    _box(ax, (3.05, 2.35), 2.05, 1.55, "$B$\n\n2  0\n1  1", F.GREEN, "#eef8f0", 13)
    _arrow(ax, (5.35, 3.12), (7.0, 3.12), F.INK)
    _box(ax, (7.1, 2.35), 2.55, 1.55, "$AB$\n\n4  2\n1  1", F.RED, "#fff0f0", 13)
    _box(ax, (0.4, 0.25), 2.05, 1.55, "$B$\n\n2  0\n1  1", F.GREEN, "#eef8f0", 13)
    _box(ax, (3.05, 0.25), 2.05, 1.55, "$A$\n\n1  2\n0  1", F.BLUE, "#eef4ff", 13)
    _arrow(ax, (5.35, 1.02), (7.0, 1.02), F.INK)
    _box(ax, (7.1, 0.25), 2.55, 1.55, "$BA$\n\n2  4\n1  3", F.PURPLE, "#f4effa", 13)
    ax.text(10.05, 2.05, "$AB\\ne BA$", fontsize=17, color=F.RED, weight="bold", rotation=90, va="center")
    ax.set_title("矩陣乘法的順序保留操作先後，因此兩種乘積通常不同", fontsize=16)
    _clean(ax, (0, 10.6), (0, 4.5))
    fig.tight_layout()
    return _save(fig, "數B4-3-乘法順序比較.svg")


def fig_power_cycle():
    rotation = np.array([[0, -1], [1, 0]], dtype=int)
    point = np.array([2, 1], dtype=int)
    points = [np.linalg.matrix_power(rotation, n) @ point for n in range(5)]
    assert np.array_equal(np.linalg.matrix_power(rotation, 4), np.eye(2, dtype=int))
    assert np.array_equal(points[-1], point)
    fig, ax = plt.subplots(figsize=(7.4, 6.4))
    _axes(ax, (-3.2, 3.2, -3.2, 3.2))
    colors = [F.BLUE, F.GREEN, F.RED, F.PURPLE, F.BLUE]
    for n, (p, color) in enumerate(zip(points, colors)):
        ax.scatter([p[0]], [p[1]], s=60, color=color, zorder=4)
        ax.text(p[0] + 0.12, p[1] + 0.14, f"$R^{n}v=({p[0]},{p[1]})$", fontsize=10.5, color=color)
        if n < 4:
            q = points[n + 1]
            _arrow(ax, p + 0.08 * (q - p), q - 0.08 * (q - p), color, 1.7, "arc3,rad=0.18")
    ax.set_title(r"$R=[0\ {-1};1\ 0]$ 每次逆時針轉 $90^\circ$，且 $R^4=I$", fontsize=15)
    fig.tight_layout()
    return _save(fig, "數B4-3-矩陣冪週期.svg")


def fig_inverse_mechanism():
    a, b, c, d = 3, 1, 2, 1
    matrix = np.array([[a, b], [c, d]], dtype=float)
    delta = a * d - b * c
    adjugate = np.array([[d, -b], [-c, a]], dtype=float)
    inverse = adjugate / delta
    assert delta == 1
    assert np.allclose(matrix @ adjugate, delta * np.eye(2))
    assert np.allclose(inverse @ matrix, np.eye(2))
    fig, ax = plt.subplots(figsize=(10.8, 5.0))
    _box(ax, (0.35, 1.55), 2.25, 2.1, "$A$\n\n3   1\n2   1", F.BLUE, "#eef4ff", 14)
    _box(ax, (3.35, 1.55), 2.25, 2.1, "$A^{\\star}$\n\n1  −1\n−2   3", F.GREEN, "#eef8f0", 14)
    _box(ax, (7.95, 1.55), 2.25, 2.1, "$(ad-bc)I$\n\n1   0\n0   1", F.RED, "#fff0f0", 14)
    ax.text(2.98, 2.55, "×", fontsize=22, ha="center")
    ax.text(6.10, 2.55, "=", fontsize=22, ha="center")
    _arrow(ax, (5.75, 2.55), (7.85, 2.55), F.INK)
    ax.text(5.4, 0.85, r"$A^{-1}=\dfrac{1}{ad-bc}A^{\star}$；本例 $ad-bc=1$", ha="center", fontsize=13)
    ax.set_title("交換主對角線、另兩項變號，乘積會化成 $(ad-bc)I$", fontsize=16)
    _clean(ax, (0, 10.6), (0.35, 4.35))
    fig.tight_layout()
    return _save(fig, "數B4-3-二階反方陣機制.svg")


def fig_system_geometry():
    grid = np.linspace(-2.5, 4.0, 300)
    cases = [
        (2 * grid - 3, -grid + 3, "唯一解", (2, 1), F.BLUE, F.GREEN),
        (2 * grid - 1, 2 * grid + 1, "無解：平行", None, F.BLUE, F.RED),
        (2 * grid - 1, 2 * grid - 1, "無限多解：重合", None, F.BLUE, F.PURPLE),
    ]
    assert np.allclose(np.linalg.solve(np.array([[2, -1], [1, 1]], dtype=float), np.array([3, 3], dtype=float)), [2, 1])
    fig, axes = plt.subplots(1, 3, figsize=(12.0, 4.25))
    for ax, (line1, line2, title, point, color1, color2) in zip(axes, cases):
        ax.plot(grid, line1, color=color1, lw=2.2)
        ax.plot(grid, line2, color=color2, lw=2.2, ls="--" if title != "唯一解" else "-")
        if point is not None:
            ax.scatter([point[0]], [point[1]], s=55, color=F.RED, zorder=4)
            ax.annotate("$(2,1)$", point, xytext=(6, 7), textcoords="offset points")
        ax.set_xlim(-2.2, 3.8)
        ax.set_ylim(-3.0, 5.2)
        ax.set_aspect("equal", adjustable="box")
        F.clean_grid(ax)
        ax.set_title(title, fontsize=12)
    fig.suptitle("係數矩陣可逆時兩直線交於一點；不可逆時需再看常數項", fontsize=15)
    fig.tight_layout(rect=(0, 0, 1, 0.91))
    return _save(fig, "數B4-3-方程組解型.svg")


def fig_vector_combination():
    first = np.array([2.0, 1.0])
    second = np.array([1.0, 2.0])
    x, y = 2.0, -0.5
    target = x * first + y * second
    coefficients = np.linalg.solve(np.column_stack([first, second]), target)
    assert np.allclose(target, [3.5, 1.0])
    assert np.allclose(coefficients, [x, y])
    fig, ax = plt.subplots(figsize=(8.0, 6.2))
    _axes(ax, (-1.0, 5.2, -1.0, 4.6))
    origin = np.zeros(2)
    _arrow(ax, origin, first, F.BLUE, 2.4)
    _arrow(ax, origin, second, F.GREEN, 2.4)
    _arrow(ax, origin, x * first, F.BLUE, 2.0)
    _arrow(ax, x * first, target, F.GREEN, 2.0)
    _arrow(ax, origin, target, F.RED, 3.0)
    ax.plot([second[0] * y, target[0]], [second[1] * y, target[1]], color=F.GRID, ls="--")
    ax.plot([x * first[0], target[0]], [x * first[1], target[1]], color=F.GRID, ls="--")
    ax.text(2.05, 1.05, r"$\vec a=(2,1)$", color=F.BLUE, fontsize=11)
    ax.text(1.08, 2.05, r"$\vec b=(1,2)$", color=F.GREEN, fontsize=11)
    ax.text(3.60, 1.12, r"$\vec c=(3.5,1)$", color=F.RED, fontsize=11)
    ax.text(1.65, 3.72, r"$\vec c=2\vec a-\frac{1}{2}\vec b$", fontsize=13, weight="bold")
    ax.set_title("向量線性組合等同以兩個向量作為矩陣的兩個直行", fontsize=15)
    fig.tight_layout()
    return _save(fig, "數B4-3-向量線性組合.svg")


def fig_affine_calibration():
    matrix = np.array([[2.0, 1.0], [-1.0, 2.0]])
    shift = np.array([4.0, 3.0])
    references = np.array([[0.0, 0.0], [2.0, 0.0], [0.0, 2.0]])
    outputs = references @ matrix.T + shift
    target = np.array([3.0, 1.0])
    observed = matrix @ target + shift
    restored = np.linalg.inv(matrix) @ (observed - shift)
    assert np.allclose(outputs, [[4, 3], [8, 1], [6, 7]])
    assert np.allclose(observed, [11, 2])
    assert np.allclose(restored, target)
    fig, axes = plt.subplots(1, 2, figsize=(10.8, 5.2))
    _axes(axes[0], (-1, 4.5, -1, 3.5))
    _axes(axes[1], (2, 12.5, 0, 8.5))
    axes[0].scatter(references[:, 0], references[:, 1], s=65, color=[F.INK, F.BLUE, F.GREEN])
    axes[0].scatter([target[0]], [target[1]], s=70, color=F.RED)
    for label, point in zip(["$P_0$", "$P_1$", "$P_2$"], references):
        axes[0].annotate(label, point, xytext=(6, 7), textcoords="offset points")
    axes[0].annotate("$X=(3,1)$", target, xytext=(6, 7), textcoords="offset points", color=F.RED)
    axes[0].set_title("原坐標")
    axes[1].scatter(outputs[:, 0], outputs[:, 1], s=65, color=[F.INK, F.BLUE, F.GREEN])
    axes[1].scatter([observed[0]], [observed[1]], s=70, color=F.RED)
    for label, point in zip(["$P'_0=(4,3)$", "$P'_1=(8,1)$", "$P'_2=(6,7)$"], outputs):
        axes[1].annotate(label, point, xytext=(6, 7), textcoords="offset points")
    axes[1].annotate("$Y=(11,2)$", observed, xytext=(6, 7), textcoords="offset points", color=F.RED)
    axes[1].set_title(r"觀測坐標 $Y=AX+t$")
    fig.suptitle(r"三個不共線參考點決定二維仿射校正；$X=A^{-1}(Y-t)$ 復原位置", fontsize=15)
    fig.tight_layout(rect=(0, 0, 1, 0.91))
    return _save(fig, "數B4-3-仿射校正參考點.svg")


def fig_cipher_flow():
    key = np.array([[2, 1], [1, 1]], dtype=int)
    inverse = np.array([[1, -1], [-1, 2]], dtype=int)
    plain = np.array([[3, 1, 20], [1, 20, 0]], dtype=int)
    encoded = key @ plain
    decoded = inverse @ encoded
    assert round(np.linalg.det(key)) == 1
    assert np.array_equal(inverse @ key, np.eye(2, dtype=int))
    assert np.array_equal(decoded, plain)
    fig, ax = plt.subplots(figsize=(11.0, 5.1))
    _box(ax, (0.25, 1.45), 2.6, 2.3, "原始矩陣 $X$\n\n3   1  20\n1  20   0", F.BLUE, "#eef4ff", 13)
    _box(ax, (4.2, 1.45), 2.6, 2.3, "傳送矩陣 $Y=KX$\n\n7  22  40\n4  21  20", F.RED, "#fff0f0", 13)
    _box(ax, (8.15, 1.45), 2.6, 2.3, "復原 $K^{-1}Y$\n\n3   1  20\n1  20   0", F.GREEN, "#eef8f0", 13)
    _arrow(ax, (2.92, 2.6), (4.10, 2.6), F.INK)
    _arrow(ax, (6.87, 2.6), (8.05, 2.6), F.INK)
    ax.text(3.52, 3.48, r"$K=[2\ 1;1\ 1]$", ha="center", fontsize=11.5)
    ax.text(7.48, 3.48, r"$K^{-1}=[1\ {-1};{-1}\ 2]$", ha="center", fontsize=11.5)
    ax.text(5.5, 0.72, "可逆性保證每個傳送矩陣恰好對應一個原始矩陣", ha="center", fontsize=12)
    ax.set_title("矩陣乘法可示範編碼與解碼；線性規則本身不等於現代資安", fontsize=16)
    _clean(ax, (0, 11), (0.35, 4.5))
    fig.tight_layout()
    return _save(fig, "數B4-3-編碼與復原.svg")


def main():
    generated = []
    for function_name, filename in FIGURE_OUTPUTS:
        function = globals()[function_name]
        generated.append(os.path.basename(function()))
    expected = [filename for _, filename in FIGURE_OUTPUTS]
    if generated != expected:
        raise AssertionError(f"圖檔輸出順序不符：{generated!r}")
    if len(generated) != len(set(generated)):
        raise AssertionError("圖檔名稱重複")


if __name__ == "__main__":
    main()
