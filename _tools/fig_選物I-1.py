# -*- coding: utf-8 -*-
"""產生「選物I-1 測量與不確定度」公開講義的 SVG，輸出到 content 章節 assets/。
重繪：  .venv/bin/python _tools/fig_選物I-1.py
"""

import os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyBboxPatch, Rectangle
import figlib as F

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CH = os.path.join(ROOT, "content", "選修物理I", "選物I-1")


def _save(fig, name):
    return F.save_to(fig, CH, name, output_subdir="assets", write_pdf=False)


def fig_error_types():
    """系統誤差 vs 隨機誤差：靶心 + 一維分布雙列示意。"""
    rng = np.random.default_rng(11)
    fig, axes = plt.subplots(2, 2, figsize=(8.6, 6.6))

    # 第一列：靶心圖（呼應準確度/精密度）
    # (標題, 偏移 bias, 散布 spread)
    targets = [
        ("只有隨機誤差\n（準但不夠精密）", (0.0, 0.0), 0.62),
        ("有系統誤差\n（精密但不準，整批偏掉）", (0.95, 0.70), 0.16),
    ]
    for ax, (title, bias, spread) in zip(axes[0], targets):
        for r, col in [
            (1.7, "#eef1f5"),
            (1.2, "#dbe7ff"),
            (0.7, "#bcd3ff"),
            (0.2, F.RED),
        ]:
            ax.add_patch(
                Circle((0, 0), r, facecolor=col, edgecolor="#aab4c2", lw=0.8, zorder=1)
            )
        n = 9
        x = rng.normal(bias[0], spread, n)
        y = rng.normal(bias[1], spread, n)
        ax.scatter(
            x, y, s=46, color=F.INK, edgecolors="white", linewidths=0.8, zorder=5
        )
        # 標出平均落點
        ax.scatter(
            [x.mean()],
            [y.mean()],
            s=120,
            marker="+",
            color=F.GREEN,
            linewidths=2.4,
            zorder=6,
        )
        ax.set_xlim(-2.1, 2.1)
        ax.set_ylim(-2.1, 2.1)
        ax.set_aspect("equal")
        ax.set_xticks([])
        ax.set_yticks([])
        for s in ("top", "right", "bottom", "left"):
            ax.spines[s].set_color("#aab4c2")
        ax.set_title(title, fontsize=11.5)

    # 第二列：一維數線上的分布（真值 vs 測量值散布）
    axes_b = axes[1]
    for ax, kind in zip(axes_b, ["random", "systematic"]):
        true_val = 0.0
        if kind == "random":
            data = rng.normal(0.0, 0.75, 200)
            label = "隨機誤差：散開、但對稱地圍著真值"
            mean = data.mean()
        else:
            data = rng.normal(1.1, 0.28, 200)
            label = "系統誤差：整批被推離真值（綠＝量測平均）"
            mean = data.mean()
        ax.hist(
            data,
            bins=22,
            range=(-2.4, 2.4),
            color=F.BLUE,
            alpha=0.35,
            edgecolor="white",
            lw=0.5,
        )
        ax.axvline(true_val, color=F.RED, lw=2.2, label="真值")
        ax.axvline(mean, color=F.GREEN, lw=2.2, ls="--", label="量測平均")
        ax.set_xlim(-2.4, 2.4)
        ax.set_yticks([])
        ax.set_xlabel("測量值")
        ax.set_title(label, fontsize=10.5)
        ax.legend(loc="upper right", fontsize=8.5, frameon=False)
        for s in ("top", "right", "left"):
            ax.spines[s].set_visible(False)

    fig.suptitle(
        "兩種誤差：隨機誤差讓點「散開」，系統誤差讓整批「偏掉」", fontsize=13.5, y=1.0
    )
    fig.tight_layout(rect=[0, 0, 1, 0.97])
    _save(fig, "選物I-1-誤差類型")


def fig_distribution():
    """多次測量的直方圖：區分單次散布 s 與平均值的不確定度 u_A。"""
    rng = np.random.default_rng(4)
    # 模擬量某段長度（真值約 10.00 cm），200 次讀數
    data = rng.normal(10.00, 0.08, 200)
    mean = data.mean()
    sd = data.std(ddof=1)

    fig, ax = F.canvas(7.4, 4.4)
    counts, bins, _ = ax.hist(
        data,
        bins=24,
        color=F.BLUE,
        alpha=0.35,
        edgecolor="white",
        lw=0.6,
        label="200 次讀數",
    )
    top = counts.max()

    # 平均值
    ax.axvline(mean, color=F.RED, lw=2.4, label=f"平均值 $\\bar{{x}}$ = {mean:.2f} cm")
    # ±1 樣本標準差帶：只表示單次讀值的散布，不等同平均值的不確定度。
    ax.axvspan(mean - sd, mean + sd, color=F.GREEN, alpha=0.12)
    ax.axvline(mean - sd, color=F.GREEN, lw=1.6, ls="--")
    ax.axvline(
        mean + sd,
        color=F.GREEN,
        lw=1.6,
        ls="--",
        label=f"$\\bar{{x}}\\pm s$（$s={sd:.2f}$ cm）",
    )

    # 標準差雙箭頭
    yarr = top * 0.86
    F.arrow(ax, (mean, yarr), (mean + sd, yarr), color=F.GREEN, lw=1.8, mutation=14)
    F.arrow(ax, (mean, yarr), (mean - sd, yarr), color=F.GREEN, lw=1.8, mutation=14)
    ax.text(
        mean, yarr * 1.06, "單次讀值散布：$s$", ha="center", color=F.GREEN, fontsize=11
    )

    ax.text(
        0.98,
        0.05,
        r"平均值的 A 類不確定度：$u_A=s/\sqrt{N}$",
        transform=ax.transAxes,
        ha="right",
        va="bottom",
        fontsize=10,
        color=F.INK,
        bbox=dict(boxstyle="round,pad=0.35", fc="white", ec="#aab4c2", alpha=0.92),
    )

    ax.set_xlabel("單次測量值 $x_i$ (cm)")
    ax.set_ylabel("出現次數")
    ax.set_title("多次測量：平均值定中心，樣本標準差描述單次讀值的散布")
    F.clean_grid(ax)
    ax.legend(loc="upper left", fontsize=9.5, frameon=False)
    _save(fig, "選物I-1-多次測量分布")


def fig_propagation():
    """獨立量的不確定度傳遞：加減與乘除都以平方和開根號組合。"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.6, 4.4))

    # ---- 左：加減，絕對不確定度以 RSS 組合 ----
    ax1.set_xlim(0, 12)
    ax1.set_ylim(0, 6)
    ax1.axis("off")
    ax1.set_title("加減：絕對不確定度 RSS", fontsize=12.5)

    def bar(ax, y, x0, val, unc, color, name):
        ax.plot(
            [x0 + val - unc, x0 + val + unc],
            [y, y],
            color=color,
            lw=3.0,
            solid_capstyle="butt",
        )
        ax.plot([x0 + val, x0 + val], [y - 0.18, y + 0.18], color=color, lw=2.4)
        for e in (-unc, unc):
            ax.plot(
                [x0 + val + e, x0 + val + e], [y - 0.13, y + 0.13], color=color, lw=2.0
            )
        ax.text(x0 + val, y + 0.42, name, ha="center", color=color, fontsize=11)

    bar(ax1, 5.0, 1.0, 3.0, 0.15, F.BLUE, "$X = 3.00 \\pm 0.15$")
    bar(ax1, 3.6, 1.0, 4.0, 0.16, F.RED, "$Y = 4.00 \\pm 0.16$")
    ax1.plot([0.6, 11.4], [2.6, 2.6], color="#cbd2da", lw=1.0)
    combined = np.sqrt(0.15**2 + 0.16**2)
    bar(ax1, 1.7, 1.0, 7.0, combined, F.GREEN, "$Z=X+Y = 7.00 \\pm 0.22$")
    ax1.text(
        6.0,
        0.65,
        r"$u_z=\sqrt{u_x^2+u_y^2}=\sqrt{0.15^2+0.16^2}\approx0.22$",
        ha="center",
        color=F.INK,
        fontsize=10.5,
    )

    # ---- 右：乘除，相對不確定度以 RSS 組合 ----
    ax2.set_xlim(0, 10)
    ax2.set_ylim(0, 6)
    ax2.axis("off")
    ax2.set_title("乘除：相對不確定度 RSS", fontsize=12.5)

    def relbar(ax, y, frac, color, name):
        x0, w = 1.0, 7.0
        ax.add_patch(
            Rectangle(
                (x0, y - 0.22),
                w,
                0.44,
                facecolor="#eef1f5",
                edgecolor="#aab4c2",
                lw=0.8,
            )
        )
        ax.add_patch(
            Rectangle(
                (x0, y - 0.22),
                w * min(frac / 0.10, 1.0),
                0.44,
                facecolor=color,
                alpha=0.55,
                edgecolor="none",
            )
        )
        ax.text(
            x0 + 0.18, y, name, ha="left", va="center", color=F.INK, fontsize=10.5
        )

    relbar(ax2, 5.0, 0.05, F.BLUE, "$u_x/|X|=5\\%$")
    relbar(ax2, 3.8, 0.04, F.RED, "$u_y/|Y|=4\\%$")
    ax2.plot([0.7, 9.3], [3.0, 3.0], color="#cbd2da", lw=1.0)
    relative = np.sqrt(0.05**2 + 0.04**2)
    relbar(ax2, 2.0, relative, F.GREEN, "$u_z/|Z|=6.4\\%$")
    ax2.text(
        5.0,
        0.7,
        r"$\frac{u_z}{|Z|}=\sqrt{(u_x/|X|)^2+(u_y/|Y|)^2}$",
        ha="center",
        color=F.INK,
        fontsize=9.5,
    )

    fig.suptitle(
        "獨立測量量的標準不確定度：各貢獻以平方和開根號組合", fontsize=13, y=1.0
    )
    fig.tight_layout(rect=[0.01, 0, 0.99, 0.95])
    _save(fig, "選物I-1-不確定度傳遞")


def fig_standard_uncertainty():
    """A 類、B 類與標準不確定度的依賴關係。"""
    fig, ax = plt.subplots(figsize=(8.8, 4.3))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 6)
    ax.axis("off")

    boxes = [
        (0.5, 3.1, 3.2, 1.7, F.BLUE, "重複測量", r"$u_A=s/\sqrt{N}$"),
        (0.5, 0.8, 3.2, 1.7, F.RED, "儀器解析度", r"$u_B=d/(2\sqrt{3})$"),
        (7.4, 2.0, 4.0, 2.0, F.GREEN, "標準不確定度", r"$u=\sqrt{u_A^2+u_B^2}$"),
    ]
    for x, y, w, h, color, title, formula in boxes:
        ax.add_patch(
            FancyBboxPatch(
                (x, y),
                w,
                h,
                boxstyle="round,pad=0.04,rounding_size=0.14",
                facecolor=color,
                alpha=0.12,
                edgecolor=color,
                linewidth=1.5,
            )
        )
        ax.text(x + w / 2, y + h * 0.68, title, ha="center", va="center", color=F.INK, fontsize=12)
        ax.text(x + w / 2, y + h * 0.30, formula, ha="center", va="center", color=color, fontsize=15)

    F.arrow(ax, (3.8, 3.95), (7.2, 3.25), color=F.BLUE, lw=1.8, mutation=14)
    F.arrow(ax, (3.8, 1.65), (7.2, 2.75), color=F.RED, lw=1.8, mutation=14)
    ax.text(5.55, 3.75, "統計資訊", ha="center", color=F.BLUE, fontsize=10)
    ax.text(5.55, 1.85, "非重複測量資訊", ha="center", color=F.RED, fontsize=10)
    ax.text(
        6.0,
        0.25,
        "即使多次讀數完全相同，儀器解析度仍使 $u_B$ 不為零。",
        ha="center",
        color=F.INK,
        fontsize=10.5,
    )
    fig.suptitle("一次完整的測量報告，要同時納入 A 類與 B 類資訊", fontsize=13.5, y=0.98)
    fig.tight_layout(rect=[0, 0.02, 1, 0.93])
    _save(fig, "選物I-1-標準不確定度組合")


def fig_dimension_check():
    """用等加速度公式示範因次齊一性。"""
    fig, ax = plt.subplots(figsize=(8.8, 4.2))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 6)
    ax.axis("off")

    ax.text(0.8, 4.85, r"$[x]=L$", fontsize=14, color=F.BLUE)
    ax.text(0.8, 3.90, r"$[v]=LT^{-1}$", fontsize=14, color=F.BLUE)
    ax.text(0.8, 2.95, r"$[a]=LT^{-2}$", fontsize=14, color=F.BLUE)
    ax.text(0.8, 2.00, r"$[t]=T$", fontsize=14, color=F.BLUE)

    ax.add_patch(
        FancyBboxPatch(
            (3.3, 3.25), 8.0, 2.1,
            boxstyle="round,pad=0.06,rounding_size=0.14",
            facecolor=F.GREEN, alpha=0.10, edgecolor=F.GREEN, linewidth=1.5,
        )
    )
    ax.text(7.3, 4.75, r"$x=v_0t+\frac{1}{2}at^2$", ha="center", fontsize=17, color=F.INK)
    ax.text(
        7.3, 3.85,
        r"$L=(LT^{-1})T+(LT^{-2})T^2=L+L$",
        ha="center", fontsize=14, color=F.GREEN,
    )

    ax.add_patch(
        FancyBboxPatch(
            (3.3, 0.55), 8.0, 1.8,
            boxstyle="round,pad=0.06,rounding_size=0.14",
            facecolor=F.RED, alpha=0.09, edgecolor=F.RED, linewidth=1.5,
        )
    )
    ax.text(7.3, 1.75, r"$x=v_0+at$", ha="center", fontsize=16, color=F.INK)
    ax.text(7.3, 1.05, r"$L\ne LT^{-1}+LT^{-1}$", ha="center", fontsize=14, color=F.RED)
    fig.suptitle("因次檢核：物理等式的每一項必須具有相同因次", fontsize=13.5, y=0.98)
    fig.tight_layout(rect=[0, 0.01, 1, 0.92])
    _save(fig, "選物I-1-因次檢核")


def 選物I_1_two_axes():
    """誤差的兩條獨立分類軸：四大來源（縱）× 兩種性質（橫）對照矩陣。
    重點是呈現「來源」與「性質」彼此正交——同一個來源常可同時製造
    系統與隨機兩種性質的誤差，破除「儀器誤差＝系統誤差」的混淆。"""
    fig, ax = plt.subplots(figsize=(9.4, 5.6))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 9.2)
    ax.axis("off")

    # 欄（性質）與列（來源）的幾何
    x_src = 0.3  # 來源標籤欄左緣
    w_src = 3.0  # 來源標籤欄寬
    x_col0 = x_src + w_src + 0.2
    col_w = 4.0
    col_gap = 0.2
    rows = [
        (
            "被測物本身\n(measurand)",
            "邊緣有毛邊、隨溫度脹縮\n而固定偏向（如總是偏大）",
            "毛邊／不規則造成每次\n對齊點忽前忽後",
        ),
        (
            "儀器\n(instrument)",
            "沒歸零、刻度本身不準、\n碼表走得偏快",
            "內部電子雜訊使讀數抖動",
        ),
        (
            "測量者\n(observer)",
            "固定的讀數習慣\n（總是斜著看而偏一邊）",
            "估讀最後一位的判斷、\n按碼表的反應時間不定",
        ),
        (
            "環境\n(environment)",
            "室溫長期偏高使尺持續\n熱脹（固定方向）",
            "氣流、振動、電壓波動\n造成的隨機擾動",
        ),
    ]
    n = len(rows)
    top = 7.6
    bottom = 1.1  # 列底保留空間給最下方說明
    row_h = (top - bottom) / n

    col_colors = [F.RED, F.BLUE]
    col_titles = [
        "系統誤差（systematic）\n整批偏同一方向、多測無效",
        "隨機誤差（random）\n上下亂跳、多測取平均可壓低",
    ]

    # 欄標題列
    ax.text(
        x_src + w_src / 2,
        top + 0.85,
        "來源 ＼ 性質",
        ha="center",
        va="center",
        fontsize=12.5,
        color=F.INK,
        fontweight="bold",
    )
    for j, (ct, cc) in enumerate(zip(col_titles, col_colors)):
        cx = x_col0 + j * (col_w + col_gap)
        ax.add_patch(
            Rectangle(
                (cx, top + 0.18),
                col_w,
                1.25,
                facecolor=cc,
                alpha=0.16,
                edgecolor=cc,
                lw=1.2,
            )
        )
        ax.text(
            cx + col_w / 2,
            top + 0.80,
            ct,
            ha="center",
            va="center",
            fontsize=10.5,
            color=cc,
            fontweight="bold",
        )

    # 各列
    for i, (src, syst, rand) in enumerate(rows):
        y0 = top - (i + 1) * row_h
        yc = y0 + row_h / 2
        # 來源標籤
        ax.add_patch(
            Rectangle(
                (x_src, y0 + 0.06),
                w_src,
                row_h - 0.12,
                facecolor="#eef1f5",
                edgecolor="#aab4c2",
                lw=1.0,
            )
        )
        ax.text(
            x_src + w_src / 2,
            yc,
            src,
            ha="center",
            va="center",
            fontsize=11,
            color=F.INK,
            fontweight="bold",
        )
        # 兩格範例
        for j, (txt, cc) in enumerate(zip((syst, rand), col_colors)):
            cx = x_col0 + j * (col_w + col_gap)
            ax.add_patch(
                Rectangle(
                    (cx, y0 + 0.06),
                    col_w,
                    row_h - 0.12,
                    facecolor="white",
                    edgecolor=cc,
                    lw=1.0,
                    alpha=0.9,
                )
            )
            ax.text(
                cx + col_w / 2,
                yc,
                txt,
                ha="center",
                va="center",
                fontsize=8.8,
                color=F.INK,
            )

    ax.text(
        6.0,
        0.42,
        "同一個來源（每一列）兩格幾乎都填得出來：來源與性質是兩條獨立的軸，"
        "別把「儀器誤差」一律當成系統誤差。",
        ha="center",
        va="center",
        fontsize=9.8,
        color=F.INK,
    )

    fig.suptitle(
        "誤差的兩條分類軸：四大來源（從哪來）× 兩種性質（能不能靠多測消）",
        fontsize=13,
        y=0.99,
    )
    fig.tight_layout(rect=[0, 0.02, 1, 0.96])
    _save(fig, "選物I-1-兩條分類軸")


if __name__ == "__main__":
    fig_distribution()
    fig_propagation()
    fig_standard_uncertainty()
    fig_dimension_check()
    print("done.")
