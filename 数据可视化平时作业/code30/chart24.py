# -*- coding: utf-8 -*-
"""复现：2022年上半年各商品销量完成情况 —— 空心目标柱 + 实际柱（Jupyter 内联显示版）"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.patches import Patch

mpl.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "Noto Sans CJK JP"]
mpl.rcParams["axes.unicode_minus"] = False

BG    = "#1b2340"
C_ACT = "#1e78d8"      # 实际销量蓝
C_OUT = "#b9c0d4"      # 目标空心柱描边

products = ["口红", "面膜", "隔离", "防晒", "精华", "面霜"]
target   = [700, 530, 600, 890, 630, 630]   # 目标（按原图空心柱高度估算）
actual   = [653, 523, 648, 856, 714, 785]   # 实际（原图标注）

fig, ax = plt.subplots(figsize=(9.2, 6.0), facecolor=BG)
ax.set_facecolor(BG)
fig.subplots_adjust(left=0.08, right=0.97, top=0.72, bottom=0.13)

x = np.arange(len(products))
W = 0.15

# 目标：灰色描边空心柱（更宽，在后面）
ax.bar(x, target, width=0.30, facecolor="none", edgecolor=C_OUT,
       lw=1.3, zorder=3, label="目标销量")
# 实际：蓝色实心柱（更窄，在前）
bars = ax.bar(x, actual, width=W, color=C_ACT, zorder=4, label="实际销量")

# 实际销量数值标签
for xi, v in zip(x, actual):
    ax.text(xi, v + 22, str(v), color="white", fontsize=12,
            ha="center", zorder=6)

# ---------- 坐标轴样式 ----------
ax.set_xlim(-0.6, len(products) - 0.4)
ax.set_ylim(0, 950)
ax.set_xticks(x)
ax.set_xticklabels(products, color="white", fontsize=12)
ax.set_yticks([])                       # 原图无 y 轴刻度
ax.tick_params(axis="x", length=0, pad=8)

ax.grid(False)
for s in ax.spines.values():
    s.set_visible(False)
ax.spines["bottom"].set_visible(True)
ax.spines["bottom"].set_color("#5a6488")

# ---------- 图例（空心方块 + 实心方块） ----------
handles = [
    Patch(fc="none", ec=C_OUT, lw=1.3, label="目标销量"),
    Patch(fc=C_ACT, label="实际销量"),
]
ax.legend(handles=handles, ncol=2, loc="upper left", bbox_to_anchor=(-0.03, 1.10),
          frameon=False, fontsize=11, handlelength=1.1, handleheight=1.1,
          columnspacing=1.0, labelcolor="white")

# ---------- 标题 / 副标题 / 脚注 ----------
fig.text(0.06, 0.93, "2022年上半年各商品销量完成情况", color="white",
         fontsize=21, fontweight="bold")
fig.text(0.06, 0.855, "防晒整体销量最好，达到856，面霜远超目标，超额完成30%",
         color="#dfe3f0", fontsize=13)
fig.text(0.05, 0.035, "*注：数据来源于公司销售系统，统计日期截至2022.06.30",
         color="#9aa3bf", fontsize=10)

plt.show()
