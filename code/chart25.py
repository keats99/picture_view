# -*- coding: utf-8 -*-
"""复现：2022年上半年各商品销量完成情况 —— 子弹图（Jupyter 内联显示版）"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.patches import Patch, Rectangle
from matplotlib.lines import Line2D

mpl.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "Noto Sans CJK JP"]
mpl.rcParams["axes.unicode_minus"] = False

BG      = "#1b2340"
C_PASS  = "#8fb6e8"   # 及格
C_GOOD  = "#3fa8c9"   # 良好
C_EXC   = "#1a6fb5"   # 优秀
C_ACT   = "#2e6be6"   # 实际
C_TGT   = "#f5c24b"   # 目标

products = ["口红", "面膜", "隔离", "防晒", "精华", "面霜"]
actual   = [650, 500, 600, 856, 710, 780]
target   = [700, 520, 620, 910, 610, 600]
pass_v, good_v, exc_v = 600, 800, 1000     # 及格/良好/优秀 分档

fig, ax = plt.subplots(figsize=(9.2, 6.0), facecolor=BG)
ax.set_facecolor(BG)
fig.subplots_adjust(left=0.09, right=0.97, top=0.72, bottom=0.13)

x = np.arange(len(products))
W_BG, W_ACT, W_TGT = 0.42, 0.24, 0.30      # 背景条/实际条/目标刻度宽度

for i in range(len(products)):
    # 背景分档堆叠条（及格 → 良好 → 优秀）
    ax.bar(x[i], pass_v, width=W_BG, color=C_PASS, zorder=3)
    ax.bar(x[i], good_v - pass_v, bottom=pass_v, width=W_BG, color=C_GOOD, zorder=3)
    ax.bar(x[i], exc_v - good_v, bottom=good_v, width=W_BG, color=C_EXC, zorder=3)
    # 实际销量（细条叠加）
    ax.bar(x[i], actual[i], width=W_ACT, color=C_ACT, zorder=4)
    # 目标（黄色短横线）
    ax.plot([x[i] - W_TGT / 2, x[i] + W_TGT / 2], [target[i], target[i]],
            color=C_TGT, lw=4, zorder=5, solid_capstyle="butt")

# ---------- 坐标轴样式 ----------
ax.set_xlim(-0.6, len(products) - 0.4)
ax.set_ylim(0, 1200)
ax.set_yticks(range(0, 1201, 200))
ax.set_xticks(x)
ax.set_xticklabels(products, color="white", fontsize=12)
ax.tick_params(axis="y", colors="#9aa3bf", labelsize=10, length=0)
ax.tick_params(axis="x", length=0, pad=8)

ax.grid(axis="y", color="#323b5c", lw=0.8, zorder=0)
for s in ax.spines.values():
    s.set_visible(False)
ax.spines["bottom"].set_visible(True)
ax.spines["bottom"].set_color("#5a6488")

# ---------- 图例 ----------
handles = [
    Patch(fc=C_PASS, label="及格"), Patch(fc=C_GOOD, label="良好"),
    Patch(fc=C_EXC, label="优秀"), Patch(fc=C_ACT, label="实际"),
    Line2D([0], [0], color=C_TGT, lw=3, label="目标"),
]
leg = ax.legend(handles=handles, ncol=5, loc="upper left",
                bbox_to_anchor=(-0.06, 1.13), frameon=False,
                fontsize=11, handlelength=1.2, handleheight=1.0,
                columnspacing=1.2, labelcolor="white")

# ---------- 标题 / 副标题 / 脚注 ----------
fig.text(0.06, 0.93, "2022年上半年各商品销量完成情况", color="white",
         fontsize=21, fontweight="bold")
fig.text(0.06, 0.855, "防晒整体销量最好，达到856，面霜远超目标，超额完成30%",
         color="#dfe3f0", fontsize=13)
fig.text(0.05, 0.035, "*注：数据来源于公司销售系统，统计日期截至2022.06.30",
         color="#9aa3bf", fontsize=10)

plt.show()
