# -*- coding: utf-8 -*-
"""复现：2022年上半年各年龄段人数分布 —— 环形图（Jupyter 内联显示版）"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.patches import Wedge

mpl.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "Noto Sans CJK JP"]
mpl.rcParams["axes.unicode_minus"] = False

BG = "#1b2340"

labels = ["[20,30)", "[30,40)", "[40,50)", ">=50"]
pcts   = [37.5, 29.2, 20.8, 12.5]
colors = ["#5b3fd4", "#4f74e8", "#4fc0d8", "#f5c24b"]

fig, ax = plt.subplots(figsize=(9, 6.2), facecolor=BG)
ax.set_facecolor(BG)
ax.set_xlim(-1.75, 1.75)
ax.set_ylim(-1.5, 1.5)
ax.set_aspect("equal")
ax.axis("off")

R0, R1 = 0.62, 1.05
GAP = 1.5
start = 90
explode_idx = 0
exploded = 0.07

mid_angles = []
for i, (lab, p, c) in enumerate(zip(labels, pcts, colors)):
    span = p / 100 * 360
    th0, th1 = start - GAP, start - span + GAP
    off = exploded if i == explode_idx else 0.0
    mid = start - span / 2
    dx, dy = off * np.cos(np.deg2rad(mid)), off * np.sin(np.deg2rad(mid))
    ax.add_patch(Wedge((dx, dy), R1 + off, th1, th0, width=R1 - R0,
                       facecolor=c, edgecolor=BG, lw=1.5, zorder=3))
    mid_angles.append(mid)
    start -= span

# 环内细微同心弧纹理
for r in np.linspace(R0 + 0.07, R1 - 0.06, 5):
    ax.add_patch(Wedge((0, 0), R1, 0, 360, width=R1 - R0, facecolor="none",
                       edgecolor="#ffffff", lw=0.6, alpha=0.05, zorder=4))

# ---------- 引导线 + 标签 ----------
def pol(ang_deg, r):
    a = np.deg2rad(ang_deg)
    return (r * np.cos(a), r * np.sin(a))

def annotate_slice(i, dot_r, kink, tx, side):
    """灰色折线 + 彩色圆点 + 两行彩色文字；side='left'/'right'"""
    off = exploded if i == explode_idx else 0.0
    dot = pol(mid_angles[i], dot_r + off)
    ax.plot([dot[0], kink[0], tx], [dot[1], kink[1], kink[1]],
            color="#c8cde0", lw=1.4, zorder=5)
    ax.plot(*dot, marker="o", ms=6, color=colors[i], zorder=6)
    ha = "left" if side == "right" else "right"
    ax.text(tx, kink[1] + 0.14, labels[i], color=colors[i], fontsize=12,
            ha=ha, va="bottom", zorder=6)
    ax.text(tx, kink[1] + 0.02, f"{pcts[i]}%", color=colors[i], fontsize=13,
            fontweight="bold", ha=ha, va="bottom", zorder=6)

annotate_slice(0, R1 + 0.02, (1.18, 0.80), 1.26, "right")    # [20,30) 右上
annotate_slice(1, R1 + 0.02, (0.55, -1.24), 0.63, "right")   # [30,40) 右下
annotate_slice(2, R1 + 0.02, (-1.30, 0.30), -1.38, "left")   # [40,50) 左
annotate_slice(3, R1 + 0.02, (-0.75, 0.98), -0.67, "left")   # >=50 左上

# ---------- 标题 / 副标题 / 脚注 ----------
fig.text(0.07, 0.93, "2022年上半年各年龄段人数分布", color="white", fontsize=21, fontweight="bold")
fig.text(0.07, 0.862, "公司平均年龄32.5， 20-30员工比例最高占比37.5%",
         color="#dfe3f0", fontsize=13)
fig.text(0.05, 0.035, "*注：数据来源于公司人力资源系统，统计日期截至2022.06.30",
         color="#9aa3bf", fontsize=10)

plt.show()
