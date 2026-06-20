# -*- coding: utf-8 -*-
"""產生「必物-4 電與磁的統一」的圖，輸出到該章 sources/。
重繪：  .venv/bin/python _tools/fig_必物-4.py
"""

import os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon, Arc, Circle, FancyArrowPatch
import figlib as F

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CH = os.path.join(ROOT, "物理", "物理一（必修物理）", "必物-4 電與磁的統一")


def _field_line(ax, start, charge_pts, charges, color, n=400, step=0.025, rev=False):
    """從 start 沿（或逆）電場方向積分一條電力線。"""
    p = np.array(start, dtype=float)
    pts = [p.copy()]
    for _ in range(n):
        E = np.zeros(2)
        for c, q in zip(charge_pts, charges):
            d = p - np.array(c, dtype=float)
            r2 = d.dot(d)
            if r2 < 0.02:  # 太靠近電荷就停
                pts.append(p.copy())
                p = None
                break
            E += q * d / r2**1.5
        if p is None:
            break
        nE = np.hypot(*E)
        if nE < 1e-6:
            break
        d = E / nE * step * (-1 if rev else 1)
        p = p + d
        pts.append(p.copy())
        if np.hypot(*p) > 6:  # 跑出畫面
            break
    pts = np.array(pts)
    ax.plot(pts[:, 0], pts[:, 1], color=color, lw=1.6, zorder=2)
    # 在中段加一個方向箭頭
    if len(pts) > 30:
        i = len(pts) // 2
        F.arrow(ax, pts[i - 1], pts[i + 1], color=color, lw=1.4, mutation=12, z=3)


def fig_field_lines():
    """正點電荷、負點電荷、一對正負電荷（電偶極）的電力線。"""
    fig, axes = plt.subplots(1, 3, figsize=(10.6, 3.9))

    # (1) 單一正電荷：向外輻射
    ax = axes[0]
    C = (0.0, 0.0)
    for ang in range(0, 360, 30):
        a = np.deg2rad(ang)
        s = (C[0] + 0.35 * np.cos(a), C[1] + 0.35 * np.sin(a))
        _field_line(ax, s, [C], [+1], F.RED)
    ax.add_patch(Circle(C, 0.30, color=F.RED, zorder=5))
    ax.text(
        *C,
        "+",
        color="white",
        ha="center",
        va="center",
        fontsize=16,
        zorder=6,
        fontweight="bold",
    )
    ax.set_title("正電荷：電力線向外", fontsize=12)

    # (2) 單一負電荷：向內匯聚
    ax = axes[1]
    for ang in range(0, 360, 30):
        a = np.deg2rad(ang)
        s = (C[0] + 2.6 * np.cos(a), C[1] + 2.6 * np.sin(a))
        _field_line(ax, s, [C], [-1], F.BLUE)
    ax.add_patch(Circle(C, 0.30, color=F.BLUE, zorder=5))
    ax.text(
        *C,
        "−",
        color="white",
        ha="center",
        va="center",
        fontsize=16,
        zorder=6,
        fontweight="bold",
    )
    ax.set_title("負電荷：電力線向內", fontsize=12)

    # (3) 電偶極：正→負
    ax = axes[2]
    P = (-1.3, 0.0)
    N = (1.3, 0.0)
    for ang in list(range(15, 360, 30)):
        a = np.deg2rad(ang)
        s = (P[0] + 0.36 * np.cos(a), P[1] + 0.36 * np.sin(a))
        _field_line(ax, s, [P, N], [+1, -1], F.PURPLE, n=600)
    ax.add_patch(Circle(P, 0.30, color=F.RED, zorder=5))
    ax.text(
        *P,
        "+",
        color="white",
        ha="center",
        va="center",
        fontsize=15,
        zorder=6,
        fontweight="bold",
    )
    ax.add_patch(Circle(N, 0.30, color=F.BLUE, zorder=5))
    ax.text(
        *N,
        "−",
        color="white",
        ha="center",
        va="center",
        fontsize=15,
        zorder=6,
        fontweight="bold",
    )
    ax.set_title("一對正負電荷（電力線正→負）", fontsize=12)

    for ax in axes:
        ax.set_xlim(-3.4, 3.4)
        ax.set_ylim(-3.0, 3.0)
        ax.set_aspect("equal")
        ax.axis("off")
    fig.tight_layout()
    F.save_to(fig, CH, "必物-4-庫侖電力線")


def fig_current_magnetic():
    """直導線電流的環形磁場 + 右手定則示意。"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.6, 4.6))

    # 左：俯視，電流出紙面，磁場為同心圓
    ax = ax1
    ax.add_patch(
        Circle((0, 0), 0.34, facecolor="#dbe7ff", edgecolor=F.INK, lw=1.6, zorder=5)
    )
    ax.add_patch(Circle((0, 0), 0.10, color=F.INK, zorder=6))  # 電流出紙面（圓點）
    ax.text(0, -0.62, "電流 $I$（出紙面）", ha="center", color=F.INK, fontsize=11)
    for r in [0.9, 1.5, 2.1]:
        th = np.linspace(0, 2 * np.pi, 200)
        ax.plot(r * np.cos(th), r * np.sin(th), color=F.GREEN, lw=1.7, zorder=2)
        # 逆時針方向箭頭（右手定則：拇指出紙面 → 四指逆時針）
        a = np.deg2rad(40)
        p0 = np.array([r * np.cos(a - 0.06), r * np.sin(a - 0.06)])
        p1 = np.array([r * np.cos(a + 0.06), r * np.sin(a + 0.06)])
        F.arrow(ax, p0, p1, color=F.GREEN, lw=1.4, mutation=13, z=3)
    ax.text(2.25, 2.0, "磁場 $B$\n（同心圓）", color=F.GREEN, fontsize=11, ha="center")
    ax.set_xlim(-2.8, 2.8)
    ax.set_ylim(-2.8, 2.8)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("直導線周圍的磁場", fontsize=13)

    # 右：右手定則（直導線版）—— 導線 + 環繞箭頭
    ax = ax2
    ax.plot([0, 0], [-2.4, 2.4], color=F.RED, lw=3.0, zorder=4)
    F.arrow(ax, (0, 1.8), (0, 2.5), color=F.RED, lw=3.0, mutation=20, z=5)
    ax.text(0.18, 2.4, "電流 $I$", color=F.RED, fontsize=12, ha="left")
    # 環繞磁場（橢圓示意三層）
    for y, w in [(-1.3, 1.7), (0.0, 1.9), (1.3, 1.7)]:
        th = np.linspace(0, 2 * np.pi, 100)
        ax.plot(w * np.cos(th), 0.45 * np.sin(th) + y, color=F.GREEN, lw=1.6, zorder=2)
        F.arrow(
            ax,
            (w * np.cos(-0.2), 0.45 * np.sin(-0.2) + y),
            (w * np.cos(0.05), 0.45 * np.sin(0.05) + y),
            color=F.GREEN,
            lw=1.4,
            mutation=12,
            z=3,
        )
    ax.text(2.05, 0.0, "$B$", color=F.GREEN, fontsize=13, ha="left")
    ax.text(
        0,
        -3.0,
        "右手握住導線：拇指指電流，\n四指環繞方向就是磁場方向",
        ha="center",
        color=F.INK,
        fontsize=11,
    )
    ax.set_xlim(-2.6, 2.6)
    ax.set_ylim(-3.5, 3.0)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("安培右手定則", fontsize=13)

    fig.tight_layout()
    F.save_to(fig, CH, "必物-4-電流磁效應")


def fig_induction():
    """磁鐵插入線圈產生感應電流。"""
    fig, ax = F.schematic(8.2, 4.4)

    # 線圈（一組橢圓）
    cx = 1.6
    for k in range(5):
        x = cx + k * 0.34
        th = np.linspace(0, 2 * np.pi, 120)
        ax.plot(
            x + 0.0 * np.cos(th), 1.1 * np.sin(th), color="#b8742a", lw=2.0, zorder=3
        )
    # 線圈接到檢流計
    ax.plot([cx, cx - 0.8, cx - 0.8], [-1.1, -1.1, -1.8], color="#b8742a", lw=2.0)
    ax.plot(
        [cx + 4 * 0.34, cx + 4 * 0.34 + 0.8, cx + 4 * 0.34 + 0.8],
        [-1.1, -1.1, -1.8],
        color="#b8742a",
        lw=2.0,
    )
    # 檢流計
    gx = (cx - 0.8 + cx + 4 * 0.34 + 0.8) / 2
    ax.add_patch(
        Circle((gx, -2.3), 0.5, facecolor="white", edgecolor=F.INK, lw=1.6, zorder=4)
    )
    ax.text(gx, -2.3, "G", ha="center", va="center", fontsize=14, zorder=5)
    ax.plot([cx - 0.8, gx - 0.5], [-1.8, -2.1], color="#b8742a", lw=2.0)
    ax.plot([cx + 4 * 0.34 + 0.8, gx + 0.5], [-1.8, -2.1], color="#b8742a", lw=2.0)
    F.arrow(
        ax, (gx - 0.25, -2.95), (gx + 0.25, -2.95), color=F.BLUE, lw=1.6, mutation=12
    )
    ax.text(gx, -3.3, "感應電流", ha="center", color=F.BLUE, fontsize=11)

    # 磁鐵（左側，往右插入）
    mx = -1.6
    ax.add_patch(
        Rectangle(
            (mx - 1.2, 0.55),
            1.2,
            0.55,
            facecolor=F.RED,
            edgecolor=F.INK,
            lw=1.4,
            zorder=4,
        )
    )
    ax.add_patch(
        Rectangle(
            (mx - 1.2, 0.0),
            1.2,
            0.55,
            facecolor="#5b6470",
            edgecolor=F.INK,
            lw=1.4,
            zorder=4,
        )
    )
    ax.text(
        mx - 0.6,
        0.82,
        "N",
        color="white",
        ha="center",
        va="center",
        fontsize=13,
        zorder=5,
    )
    ax.text(
        mx - 0.6,
        0.27,
        "S",
        color="white",
        ha="center",
        va="center",
        fontsize=13,
        zorder=5,
    )
    # 運動箭頭
    F.arrow(ax, (mx + 0.1, 0.55), (cx - 0.5, 0.55), color=F.INK, lw=2.0, mutation=18)
    ax.text(
        (mx + cx) / 2 - 0.2,
        0.95,
        "磁鐵插入 $\\rightarrow$",
        color=F.INK,
        fontsize=12,
        ha="center",
    )

    ax.text(cx + 0.6, 1.7, "線圈", color="#8a5a1a", fontsize=12, ha="center")
    ax.set_title("電磁感應：磁鐵運動 $\\Rightarrow$ 線圈產生感應電流", fontsize=13)
    ax.set_xlim(-3.2, 4.6)
    ax.set_ylim(-3.7, 2.2)
    F.save_to(fig, CH, "必物-4-電磁感應")


def fig_em_wave():
    """電磁波：E 與 B 互相垂直、沿傳播方向前進的橫波。"""
    fig = plt.figure(figsize=(8.6, 4.6))
    ax = fig.add_subplot(111, projection="3d")
    x = np.linspace(0, 4 * np.pi, 300)
    E = np.sin(x)
    B = np.sin(x)

    # 傳播軸
    ax.plot(x, np.zeros_like(x), np.zeros_like(x), color=F.INK, lw=1.4)
    # E 場（在 x-z 平面，垂直方向）
    ax.plot(x, np.zeros_like(x), E, color=F.RED, lw=2.6)
    # B 場（在 x-y 平面，水平方向）
    ax.plot(x, B, np.zeros_like(x), color=F.BLUE, lw=2.6)

    # 幾條場向量（梳齒）
    for xi in np.linspace(0, 4 * np.pi, 17):
        e = np.sin(xi)
        ax.plot([xi, xi], [0, 0], [0, e], color=F.RED, lw=1.0, alpha=0.6)
        ax.plot([xi, xi], [0, np.sin(xi)], [0, 0], color=F.BLUE, lw=1.0, alpha=0.6)

    ax.text(4 * np.pi + 0.6, 0, 0, "傳播方向", color=F.INK, fontsize=11)
    ax.text(4 * np.pi * 0.25, 0, 1.25, "電場 $E$", color=F.RED, fontsize=12)
    ax.text(4 * np.pi * 0.25, 1.25, 0, "磁場 $B$", color=F.BLUE, fontsize=12)

    ax.set_xlabel("傳播方向 (x)")
    ax.set_box_aspect((4, 1.3, 1.3))
    ax.set_yticks([])
    ax.set_zticks([])
    ax.set_xticks([])
    ax.set_title("電磁波：$E \\perp B \\perp$ 傳播方向（橫波）", fontsize=13)
    ax.view_init(elev=18, azim=-60)
    ax.grid(False)
    try:
        ax.xaxis.pane.set_visible(False)
        ax.yaxis.pane.set_visible(False)
        ax.zaxis.pane.set_visible(False)
    except Exception:
        pass
    F.save_to(fig, CH, "必物-4-電磁波")


def fig_em_spectrum():
    """電磁波譜：頻率/波長軸排列各波段與應用。"""
    fig, ax = F.canvas(10.2, 3.6)
    # 以 log10(波長/m) 為橫軸，由長到短（左長右短）
    bands = [
        (3, 1, "無線電波", "#7a4fbf", "廣播、電視"),
        (1, -3, "微波", F.BLUE, "微波爐、Wi-Fi、雷達"),
        (-3, -6.3, "紅外線", F.RED, "熱感應、遙控器"),
        (-6.3, -6.85, "可見光", "#1a7f37", "人眼、照明"),
        (-6.85, -8, "紫外線", "#8250df", "殺菌、曬黑"),
        (-8, -11, "X 射線", "#bf8700", "醫學造影"),
        (-11, -13, "$\\gamma$ 射線", "#d1242f", "放射治療"),
    ]
    xmin, xmax = -13, 3
    for lo, hi, name, col, use in bands:
        ax.axvspan(hi, lo, ymin=0.35, ymax=0.75, color=col, alpha=0.35, lw=0)
        xc = (lo + hi) / 2
        ax.text(
            xc,
            0.86,
            name,
            ha="center",
            va="bottom",
            color=col,
            fontsize=11,
            transform=ax.get_xaxis_transform(),
        )
        ax.text(
            xc,
            0.30,
            use,
            ha="center",
            va="top",
            color="#444",
            fontsize=8.5,
            transform=ax.get_xaxis_transform(),
        )
    # 可見光彩條
    vis = np.linspace(-6.85, -6.3, 60)
    for i in range(len(vis) - 1):
        frac = i / (len(vis) - 1)
        col = plt.cm.rainbow(1 - frac)
        ax.axvspan(
            vis[i + 1], vis[i], ymin=0.35, ymax=0.75, color=col, alpha=0.85, lw=0
        )

    ax.set_xlim(xmax, xmin)  # 左長右短
    ax.set_ylim(0, 1)
    ax.set_yticks([])
    ax.set_xlabel("波長（公尺，對數刻度）；越往右波長越短、頻率越高、光子能量越大")
    ax.set_xticks([3, 0, -3, -6, -9, -12])
    ax.set_xticklabels(
        [
            r"$10^{3}$",
            r"$10^{0}$",
            r"$10^{-3}$",
            r"$10^{-6}$",
            r"$10^{-9}$",
            r"$10^{-12}$",
        ]
    )
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    F.arrow(ax, (2.4, 0.12), (-12.4, 0.12), color=F.INK, lw=1.6, mutation=15)
    ax.text(-12, 0.18, "頻率增加 $\\rightarrow$", color=F.INK, fontsize=10, ha="center")
    ax.set_title("電磁波譜（電磁波家族）", fontsize=13)
    fig.tight_layout()
    F.save_to(fig, CH, "必物-4-電磁波譜")


def fig_transverse_longitudinal():
    """橫波 vs 縱波：上圖振動垂直傳播（橫波），下圖振動平行傳播（縱波，疏密相間）。"""
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8.4, 4.8))

    x = np.linspace(0, 4 * np.pi, 400)

    # 上：橫波（繩波）——介質上下振動、波往右傳
    ax = ax1
    y = 0.8 * np.sin(x)
    ax.plot(x, y, color=F.BLUE, lw=2.4, zorder=3)
    # 幾個質點與其上下振動箭頭
    for xi in np.linspace(0.6, 4 * np.pi - 0.6, 7):
        yi = 0.8 * np.sin(xi)
        ax.add_patch(Circle((xi, yi), 0.07, color=F.INK, zorder=5))
        F.arrow(
            ax,
            (xi, 0),
            (xi, yi if abs(yi) > 0.15 else (0.3 if yi >= 0 else -0.3)),
            color=F.RED,
            lw=1.3,
            mutation=10,
            z=4,
        )
    F.arrow(
        ax,
        (4 * np.pi - 1.0, -1.55),
        (4 * np.pi + 0.2, -1.55),
        color=F.INK,
        lw=2.0,
        mutation=16,
    )
    ax.text(4 * np.pi - 0.4, -1.95, "波傳播方向", color=F.INK, fontsize=10, ha="center")
    ax.text(
        0.1,
        1.45,
        "橫波：振動（紅）垂直於傳播（黑）",
        color=F.BLUE,
        fontsize=12,
        ha="left",
    )
    ax.text(
        0.1, -1.75, "例：電磁波、水面波、繩波", color="#555", fontsize=9.5, ha="left"
    )
    ax.set_xlim(-0.4, 4 * np.pi + 1.2)
    ax.set_ylim(-2.3, 1.9)
    ax.set_aspect("auto")
    ax.axis("off")

    # 下：縱波（聲波）——介質前後振動、疏密相間
    ax = ax2
    # 用密度表示疏密：在 x 上以正弦調變一排小點的位置
    base = np.linspace(0.3, 4 * np.pi - 0.3, 90)
    disp = 0.32 * np.sin(base)
    px = base + disp
    for xv in px:
        ax.plot([xv, xv], [-0.55, 0.55], color=F.GREEN, lw=1.3, alpha=0.8, zorder=2)
    # 標一個質點的前後振動
    xi = 4 * np.pi * 0.5
    F.arrow(ax, (xi - 0.45, 0.95), (xi + 0.45, 0.95), color=F.RED, lw=1.4, mutation=11)
    F.arrow(ax, (xi + 0.45, 0.95), (xi - 0.45, 0.95), color=F.RED, lw=1.4, mutation=11)
    ax.text(xi, 1.25, "質點前後振動", color=F.RED, fontsize=9.5, ha="center")
    F.arrow(
        ax,
        (4 * np.pi - 1.0, -1.15),
        (4 * np.pi + 0.2, -1.15),
        color=F.INK,
        lw=2.0,
        mutation=16,
    )
    ax.text(4 * np.pi - 0.4, -1.5, "波傳播方向", color=F.INK, fontsize=10, ha="center")
    ax.text(
        0.1,
        1.55,
        "縱波：振動（紅）平行於傳播（黑），疏密相間",
        color="#1a7f37",
        fontsize=12,
        ha="left",
    )
    ax.text(0.1, -1.35, "例：聲波", color="#555", fontsize=9.5, ha="left")
    ax.set_xlim(-0.4, 4 * np.pi + 1.2)
    ax.set_ylim(-1.7, 2.0)
    ax.set_aspect("auto")
    ax.axis("off")

    fig.tight_layout()
    F.save_to(fig, CH, "必物-4-橫波縱波")


def fig_doppler():
    """運動波源造成的波前壓縮（前方）與拉伸（後方）。"""
    fig, ax = F.schematic(7.6, 4.6)
    # 波源在數個時刻的位置（往右移動），每個時刻發出一個球面波
    v_src = 0.7
    times = [0, 1, 2, 3, 4]
    for i, t in enumerate(times):
        cx = -2.0 + v_src * t
        r = (len(times) - 1 - i) * 0.95 + 0.2  # 越早發出的波，傳得越遠（半徑大）
        th = np.linspace(0, 2 * np.pi, 200)
        ax.plot(cx + r * np.cos(th), r * np.sin(th), color=F.BLUE, lw=1.5, zorder=2)
    # 波源現在的位置
    src_now = -2.0 + v_src * times[-1]
    ax.add_patch(Circle((src_now, 0), 0.16, color=F.RED, zorder=6))
    F.arrow(ax, (src_now, 0), (src_now + 0.9, 0), color=F.RED, lw=2.0, mutation=16, z=6)
    ax.text(src_now + 0.5, -0.45, "波源運動", color=F.RED, fontsize=11, ha="center")

    # 觀察者（用小圓點＋耳朵示意，避免相依字型 emoji）
    ax.add_patch(
        Circle(
            (src_now + 3.3, 0),
            0.18,
            facecolor="#ffe9b0",
            edgecolor=F.INK,
            lw=1.4,
            zorder=6,
        )
    )
    ax.add_patch(
        Circle((-3.8, 0), 0.18, facecolor="#ffe9b0", edgecolor=F.INK, lw=1.4, zorder=6)
    )
    ax.text(
        src_now + 3.3,
        -0.7,
        "前方觀察者\n波長變短 $\\to$ 頻率變高（藍移）",
        color=F.GREEN,
        fontsize=10,
        ha="center",
        va="top",
    )
    ax.text(
        -3.8,
        -0.7,
        "後方觀察者\n波長變長 $\\to$ 頻率變低（紅移）",
        color=F.AMBER,
        fontsize=10,
        ha="center",
        va="top",
    )

    ax.set_title("都卜勒效應：運動波源前方波前壓縮、後方拉伸", fontsize=13)
    ax.set_xlim(-5.2, 5.6)
    ax.set_ylim(-3.4, 3.6)
    F.save_to(fig, CH, "必物-4-都卜勒")


def fig_doppler_observer():
    """情形二：波源不動、觀察者移動。同心圓等間距（波長不變），
    觀察者迎面→單位時間多遇波前→升頻；遠離→少遇→降頻。"""
    fig, ax = F.schematic(7.8, 4.8)
    # 波源固定在原點，發出等間距同心圓（波長不變）
    for r in [0.8, 1.6, 2.4, 3.2, 4.0]:
        th = np.linspace(0, 2 * np.pi, 200)
        ax.plot(r * np.cos(th), r * np.sin(th), color=F.BLUE, lw=1.5, zorder=2)
    ax.add_patch(Circle((0, 0), 0.16, color=F.RED, zorder=6))
    ax.text(0, -0.5, "波源不動", color=F.RED, fontsize=11, ha="center", va="top")
    ax.annotate(
        "波長不變\n（同心圓等間距）",
        xy=(0.4 * np.cos(0.6), 0.4 * 4 + 0.4),
        xytext=(0, 4.55),
        color=F.BLUE,
        fontsize=10.5,
        ha="center",
        va="bottom",
    )

    # 迎面前進的觀察者（右側，朝波源移動）→ 升頻
    obsA = (3.6, 0)
    ax.add_patch(
        Circle(obsA, 0.18, facecolor="#ffe9b0", edgecolor=F.INK, lw=1.4, zorder=6)
    )
    F.arrow(ax, obsA, (obsA[0] - 1.0, 0), color=F.GREEN, lw=2.2, mutation=16, z=6)
    ax.text(
        3.6,
        -0.7,
        "迎面前進去「接」波\n單位時間多遇波前 $\\to$ 頻率變高（藍移）",
        color=F.GREEN,
        fontsize=10,
        ha="center",
        va="top",
    )

    # 順向遠離的觀察者（左側，背離波源移動）→ 降頻
    obsB = (-3.6, 0)
    ax.add_patch(
        Circle(obsB, 0.18, facecolor="#ffe9b0", edgecolor=F.INK, lw=1.4, zorder=6)
    )
    F.arrow(ax, obsB, (obsB[0] - 1.0, 0), color=F.AMBER, lw=2.2, mutation=16, z=6)
    ax.text(
        -3.6,
        -0.7,
        "順向遠離、波前要追上他\n單位時間少遇波前 $\\to$ 頻率變低（紅移）",
        color=F.AMBER,
        fontsize=10,
        ha="center",
        va="top",
    )

    ax.set_title("都卜勒效應：波源不動、觀察者移動（波長不變）", fontsize=13)
    ax.set_xlim(-5.6, 5.6)
    ax.set_ylim(-3.6, 5.2)
    F.save_to(fig, CH, "必物-4-都卜勒觀察者")


if __name__ == "__main__":
    fig_field_lines()
    fig_current_magnetic()
    fig_induction()
    fig_em_wave()
    fig_transverse_longitudinal()
    fig_em_spectrum()
    fig_doppler()
    fig_doppler_observer()
    print("done.")
