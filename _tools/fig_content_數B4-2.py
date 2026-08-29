# -*- coding: utf-8 -*-
"""重生「數B4-2 條件機率與貝氏定理」學生講義的章內 SVG。"""

if __name__ == "__main__" and __import__("sys").argv[1:]:
    raise SystemExit("本腳本不接受參數；直接執行即可重生數B4-2章內 SVG。")

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, FancyArrowPatch, Rectangle

import figlib as F


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHAPTER = os.path.join(ROOT, "content", "數學B", "數B4-2")

FIGURE_OUTPUTS = (
    ("fig_conditioned_space", "數B4-2-條件樣本空間.svg"),
    ("fig_two_way_table", "數B4-2-雙向條件表.svg"),
    ("fig_exclusive_independent", "數B4-2-互斥與獨立.svg"),
    ("fig_chain_tree", "數B4-2-序列乘法樹.svg"),
    ("fig_total_probability", "數B4-2-全機率分割.svg"),
    ("fig_bayes_update", "數B4-2-貝氏面積更新.svg"),
    ("fig_natural_frequencies", "數B4-2-快篩自然頻數.svg"),
    ("fig_frequency_convergence", "數B4-2-客觀機率收斂.svg"),
)


def _save(fig, filename):
    stem, extension = os.path.splitext(filename)
    if extension != ".svg" or not stem.startswith("數B4-2-"):
        raise AssertionError("輸出檔名必須是數B4-2章內 SVG")
    return F.save_to(fig, CHAPTER, stem, output_subdir="assets", write_pdf=False)


def _clean(ax, xlim=(0, 10), ylim=(0, 6)):
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_aspect("equal", adjustable="box")
    ax.axis("off")


def _arrow(ax, start, end, color=F.INK, lw=2.0):
    ax.add_patch(FancyArrowPatch(start, end, arrowstyle="-|>", mutation_scale=15,
                                color=color, linewidth=lw, shrinkA=1, shrinkB=1))


def fig_conditioned_space():
    total, a_count, both = 100, 40, 24
    assert np.isclose(both / a_count, 0.6)
    fig, ax = plt.subplots(figsize=(10.0, 5.6))
    ax.add_patch(Rectangle((0.7, 0.7), 8.6, 4.5, facecolor="#f6f8fb", edgecolor=F.INK, lw=1.7))
    ax.add_patch(Circle((4.1, 3.2), 1.75, facecolor="#dcecff", edgecolor=F.BLUE, lw=2.2, alpha=0.9))
    ax.add_patch(Circle((5.5, 3.2), 1.45, facecolor="#e3f3e7", edgecolor=F.GREEN, lw=2.2, alpha=0.82))
    ax.text(1.0, 4.8, "原樣本空間 S：100 人", fontsize=13, weight="bold")
    ax.text(3.0, 4.15, "A：40 人", color=F.BLUE, fontsize=12)
    ax.text(5.7, 4.0, "B", color=F.GREEN, fontsize=12)
    ax.text(4.45, 3.15, r"$A\cap B$", fontsize=13, weight="bold")
    ax.text(4.42, 2.75, "24 人", fontsize=12)
    ax.text(2.5, 0.95, r"給定 A 後，分母改為 40：  $P(B\mid A)=24/40=0.60$", fontsize=13)
    ax.set_title("條件機率把已知事件 A 當成新的樣本空間", fontsize=16)
    _clean(ax)
    fig.tight_layout()
    return _save(fig, "數B4-2-條件樣本空間.svg")


def fig_two_way_table():
    cells = np.array([[24, 16], [6, 54]])
    assert cells.sum() == 100
    assert cells[0].sum() == 40 and cells[:, 0].sum() == 30
    fig, ax = plt.subplots(figsize=(9.8, 5.5))
    x0, y0, w, h = 2.0, 1.1, 1.55, 0.9
    labels = [["24", "16", "40"], ["6", "54", "60"], ["30", "70", "100"]]
    row_names = ["A", "A′", "合計"]
    col_names = ["B", "B′", "合計"]
    for i in range(3):
        for j in range(3):
            face = "#dcecff" if i == 0 else ("#e3f3e7" if j == 0 else "#f5f6f8")
            if i == 2 or j == 2:
                face = "#f1f3f6"
            ax.add_patch(Rectangle((x0+j*w, y0+(2-i)*h), w, h, facecolor=face,
                                   edgecolor="#8d99a6", lw=1.3))
            ax.text(x0+(j+0.5)*w, y0+(2-i+0.5)*h, labels[i][j], ha="center", va="center", fontsize=14)
    for j, name in enumerate(col_names):
        ax.text(x0+(j+0.5)*w, y0+3*h+0.28, name, ha="center", fontsize=13, weight="bold")
    for i, name in enumerate(row_names):
        ax.text(x0-0.35, y0+(2-i+0.5)*h, name, ha="right", va="center", fontsize=13, weight="bold")
    ax.text(7.05, 3.25, r"$P(B\mid A)=\dfrac{24}{40}=0.60$", fontsize=13, color=F.BLUE)
    ax.text(7.05, 2.35, r"$P(A\mid B)=\dfrac{24}{30}=0.80$", fontsize=13, color=F.GREEN)
    ax.text(7.05, 1.45, "同一個交集，分母由條件決定", fontsize=12)
    ax.set_title("雙向表同時保存交集、邊際總數與條件分母", fontsize=16)
    _clean(ax, (0, 11.4), (0, 5.5))
    fig.tight_layout()
    return _save(fig, "數B4-2-雙向條件表.svg")


def fig_exclusive_independent():
    # 右圖以 100 格面積模型：P(A)=0.5、P(B)=0.4、P(A∩B)=0.2。
    assert np.isclose(0.5 * 0.4, 0.2)
    fig, axes = plt.subplots(1, 2, figsize=(10.4, 5.2))
    ax = axes[0]
    ax.add_patch(Rectangle((0.5, 0.7), 4.0, 3.5, facecolor="#f7f8fa", edgecolor=F.INK))
    ax.add_patch(Circle((1.75, 2.4), 0.75, facecolor="#dcecff", edgecolor=F.BLUE, lw=2))
    ax.add_patch(Circle((3.3, 2.4), 0.75, facecolor="#fce4e4", edgecolor=F.RED, lw=2))
    ax.text(1.65, 2.4, "A", fontsize=14, ha="center")
    ax.text(3.3, 2.4, "B", fontsize=14, ha="center")
    ax.text(2.5, 0.30, r"互斥：$P(A\cap B)=0$", ha="center", fontsize=12)
    ax.set_title("交集為空集合", fontsize=14)
    _clean(ax, (0, 5), (0, 4.8))
    ax = axes[1]
    ax.add_patch(Rectangle((0.5, 0.7), 4.0, 3.5, facecolor="#f7f8fa", edgecolor=F.INK))
    ax.add_patch(Rectangle((0.5, 0.7), 2.0, 3.5, facecolor="#dcecff", edgecolor=F.BLUE, lw=2, alpha=0.8))
    ax.add_patch(Rectangle((0.5, 2.8), 4.0, 1.4, facecolor="#e3f3e7", edgecolor=F.GREEN, lw=2, alpha=0.65))
    ax.text(1.0, 1.65, r"$P(A)=0.5$", fontsize=11)
    ax.text(3.0, 3.45, r"$P(B)=0.4$", fontsize=11)
    ax.text(1.55, 3.45, r"$0.2$", fontsize=12, weight="bold")
    ax.text(2.5, 0.30, r"獨立：$P(A\cap B)=P(A)P(B)$", ha="center", fontsize=12)
    ax.set_title("知道 A 不改變 B 的比例", fontsize=14)
    _clean(ax, (0, 5), (0, 4.8))
    fig.suptitle("互斥描述交集；獨立描述條件資訊是否改變比例", fontsize=16)
    fig.tight_layout(rect=(0, 0, 1, 0.93))
    return _save(fig, "數B4-2-互斥與獨立.svg")


def fig_chain_tree():
    p_rr = (3/5) * (2/4)
    assert np.isclose(p_rr, 3/10)
    fig, ax = plt.subplots(figsize=(10.6, 5.8))
    root = (0.8, 3.0)
    nodes = {"R": (3.2, 4.35), "B": (3.2, 1.65), "RR": (6.0, 5.0), "RB": (6.0, 3.7),
             "BR": (6.0, 2.3), "BB": (6.0, 1.0)}
    for end, label, color in ((nodes["R"], "紅  3/5", F.RED), (nodes["B"], "藍  2/5", F.BLUE)):
        _arrow(ax, root, end, color)
        ax.text((root[0]+end[0])/2, (root[1]+end[1])/2+0.18, label, color=color, fontsize=12)
    for start_key, end_key, label, color in (("R","RR","紅  2/4",F.RED),("R","RB","藍  2/4",F.BLUE),
                                              ("B","BR","紅  3/4",F.RED),("B","BB","藍  1/4",F.BLUE)):
        _arrow(ax, nodes[start_key], nodes[end_key], color)
        a, b = nodes[start_key], nodes[end_key]
        ax.text((a[0]+b[0])/2, (a[1]+b[1])/2+0.12, label, color=color, fontsize=11)
    for key in ("R","B","RR","RB","BR","BB"):
        x, y = nodes[key]
        ax.scatter([x], [y], s=42, color=F.INK, zorder=4)
    ax.text(6.5, 5.0, r"$P(RR)=\dfrac{3}{5}\cdot\dfrac{2}{4}=\dfrac{3}{10}$", fontsize=13)
    ax.text(6.5, 3.7, r"$P(RB)=\dfrac{3}{5}\cdot\dfrac{2}{4}$", fontsize=12)
    ax.text(6.5, 2.3, r"$P(BR)=\dfrac{2}{5}\cdot\dfrac{3}{4}$", fontsize=12)
    ax.text(6.5, 1.0, r"$P(BB)=\dfrac{2}{5}\cdot\dfrac{1}{4}$", fontsize=12)
    ax.set_title("不放回抽取：沿路徑相乘，第二層使用已更新的袋中組成", fontsize=16)
    _clean(ax, (0, 10.8), (0.3, 5.7))
    fig.tight_layout()
    return _save(fig, "數B4-2-序列乘法樹.svg")


def fig_total_probability():
    priors = np.array([0.50, 0.30, 0.20])
    rates = np.array([0.02, 0.04, 0.08])
    joints = priors * rates
    total = joints.sum()
    assert np.isclose(total, 0.038)
    fig, ax = plt.subplots(figsize=(10.8, 5.8))
    colors = [F.BLUE, F.GREEN, F.AMBER]
    y_positions = [4.6, 3.0, 1.4]
    for i, (p, r, j, y, c) in enumerate(zip(priors, rates, joints, y_positions, colors), start=1):
        ax.add_patch(Rectangle((0.7, y-0.42), 1.8, 0.84, facecolor="#f4f7fb", edgecolor=c, lw=2))
        ax.text(1.6, y, f"來源 A{i}\n{p:.0%}", ha="center", va="center", fontsize=12)
        _arrow(ax, (2.55, y), (5.0, y), c)
        ax.text(3.75, y+0.18, f"瑕疵率 {r:.0%}", ha="center", fontsize=11, color=c)
        ax.add_patch(Rectangle((5.1, y-0.35), 1.55, 0.70, facecolor="#fff2f2", edgecolor=F.RED, lw=1.5))
        ax.text(5.88, y, f"聯合 {j:.1%}", ha="center", va="center", fontsize=11)
        _arrow(ax, (6.7, y), (8.2, 3.0), F.INK, 1.5)
    ax.add_patch(Rectangle((8.25, 2.3), 2.0, 1.4, facecolor="#fce7e7", edgecolor=F.RED, lw=2))
    ax.text(9.25, 3.0, "瑕疵\n3.8%", ha="center", va="center", fontsize=14, weight="bold")
    ax.text(5.35, 0.55, r"$P(D)=\sum_i P(A_i)P(D\mid A_i)=0.010+0.012+0.016=0.038$", ha="center", fontsize=13)
    ax.set_title("全機率公式把互斥來源的聯合機率相加", fontsize=16)
    _clean(ax, (0, 10.9), (0, 5.8))
    fig.tight_layout()
    return _save(fig, "數B4-2-全機率分割.svg")


def fig_bayes_update():
    joints = np.array([0.010, 0.012, 0.016])
    posterior = joints / joints.sum()
    assert np.isclose(posterior.sum(), 1.0)
    fig, axes = plt.subplots(1, 2, figsize=(10.6, 5.3))
    colors = [F.BLUE, F.GREEN, F.AMBER]
    axes[0].bar(["A1", "A2", "A3"], [0.50, 0.30, 0.20], color=colors)
    axes[0].set_ylim(0, 0.58)
    axes[0].set_ylabel("機率")
    axes[0].set_title("觀察前：來源比例")
    axes[0].grid(axis="y", alpha=0.22)
    axes[1].bar(["A1", "A2", "A3"], posterior, color=colors)
    axes[1].set_ylim(0, 0.58)
    axes[1].set_title("已知瑕疵後：來源後驗比例")
    axes[1].grid(axis="y", alpha=0.22)
    for ax, values in ((axes[0], [0.50,0.30,0.20]), (axes[1], posterior)):
        for i, v in enumerate(values):
            ax.text(i, v+0.018, f"{v:.1%}", ha="center", fontsize=11)
    fig.suptitle("貝氏更新：先取『來源且瑕疵』的面積，再在全部瑕疵中重新正規化", fontsize=15)
    fig.text(0.5, 0.025, r"$P(A_i\mid D)=\dfrac{P(A_i)P(D\mid A_i)}{P(D)}$", ha="center", fontsize=14)
    fig.tight_layout(rect=(0, 0.08, 1, 0.91))
    return _save(fig, "數B4-2-貝氏面積更新.svg")


def fig_natural_frequencies():
    population, ill = 10000, 200
    healthy = population - ill
    tp, fn, fp, tn = 180, 20, 490, 9310
    assert tp + fn == ill and fp + tn == healthy and tp + fp == 670
    posterior = tp / (tp + fp)
    fig, ax = plt.subplots(figsize=(10.8, 6.0))
    boxes = [
        (0.5, 2.45, 1.6, 1.0, "10,000 人", "#f4f6f9", F.INK),
        (3.0, 4.25, 1.75, 1.0, "帶原 200", "#fde8e8", F.RED),
        (3.0, 1.15, 1.75, 1.0, "未帶原 9,800", "#e7f3e9", F.GREEN),
        (6.0, 4.8, 1.55, 0.85, "陽性 180", "#fde8e8", F.RED),
        (6.0, 3.45, 1.55, 0.85, "陰性 20", "#f4f6f9", F.INK),
        (6.0, 1.75, 1.55, 0.85, "陽性 490", "#fff2dc", F.AMBER),
        (6.0, 0.4, 1.55, 0.85, "陰性 9,310", "#e7f3e9", F.GREEN),
    ]
    for x,y,w,h,label,face,edge in boxes:
        ax.add_patch(Rectangle((x,y),w,h,facecolor=face,edgecolor=edge,lw=1.8))
        ax.text(x+w/2,y+h/2,label,ha="center",va="center",fontsize=11)
    _arrow(ax,(2.1,2.95),(3.0,4.75),F.RED); _arrow(ax,(2.1,2.95),(3.0,1.65),F.GREEN)
    _arrow(ax,(4.75,4.75),(6.0,5.22),F.RED); _arrow(ax,(4.75,4.75),(6.0,3.88),F.INK)
    _arrow(ax,(4.75,1.65),(6.0,2.18),F.AMBER); _arrow(ax,(4.75,1.65),(6.0,0.82),F.GREEN)
    ax.text(2.35,4.18,"盛行率 2%",fontsize=10,color=F.RED)
    ax.text(4.95,5.2,"靈敏度 90%",fontsize=10,color=F.RED)
    ax.text(4.85,2.35,"偽陽率 5%",fontsize=10,color=F.AMBER)
    ax.add_patch(Rectangle((8.1,2.0),2.25,1.85,facecolor="#eef4ff",edgecolor=F.BLUE,lw=2))
    ax.text(9.23,3.25,"陽性共 670",ha="center",fontsize=12,weight="bold")
    ax.text(9.23,2.72,"P(帶原｜陽性)",ha="center",fontsize=11)
    ax.text(9.23,2.27,f"= 180 / 670\n= {posterior:.1%}",ha="center",fontsize=12)
    ax.set_title("自然頻數把盛行率、靈敏度與偽陽率放回同一群人", fontsize=16)
    _clean(ax, (0, 10.9), (0, 6.0))
    fig.tight_layout()
    return _save(fig, "數B4-2-快篩自然頻數.svg")


def fig_frequency_convergence():
    rng = np.random.default_rng(20260829)
    p = 0.35
    trials = rng.binomial(1, p, size=2000)
    freq = np.cumsum(trials) / np.arange(1, len(trials)+1)
    assert 0 <= freq.min() <= freq.max() <= 1
    assert abs(freq[-1] - p) < 0.03
    fig, ax = plt.subplots(figsize=(10.2, 5.5))
    ax.plot(np.arange(1, 2001), freq, color=F.BLUE, lw=1.7, label="累積相對次數")
    ax.axhline(p, color=F.RED, lw=2, linestyle="--", label="模型機率 0.35")
    ax.set_xlim(1, 2000)
    ax.set_ylim(0.25, 0.48)
    ax.set_xlabel("累積試驗次數")
    ax.set_ylabel("事件 A 的累積相對次數")
    ax.grid(alpha=0.22)
    ax.legend(frameon=False, loc="upper right")
    ax.set_title("客觀機率以重複資料估計；樣本增加時波動幅度通常縮小", fontsize=15)
    fig.tight_layout()
    return _save(fig, "數B4-2-客觀機率收斂.svg")


def main():
    written = []
    for func_name, filename in FIGURE_OUTPUTS:
        result = globals()[func_name]()
        written.append(result)
        print(f"wrote {result}")
    assert len(written) == len(FIGURE_OUTPUTS)


if __name__ == "__main__":
    main()
