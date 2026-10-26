# -*- coding: utf-8 -*-
"""17 玉玦图 —— 完美复刻 Excel 仪表盘布局"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Wedge

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 配色方案与数据
BG = '#1A1E43'
ages = ['>=50', '[40,50)', '[30,40)', '[20,30)']
shares = [0.125, 0.2083333, 0.2916667, 0.375]
colors = ['#37A2DA', '#11A7AD', '#F5C353', '#E74E69']  # 内圈 -> 外圈
percent_labels = ['12.5%', '20.8%', '29.2%', '37.5%']

fig = plt.figure(figsize=(9, 6), facecolor=BG)

# 主标题与副标题（左对齐）
fig.text(0.1, 0.88, '2022年上半年龄分布', color='#FFFFFF', fontsize=22, fontweight='bold', ha='left')
fig.text(0.1, 0.81, '公司平均年龄32.5，23-30员工比例最高', color='#d1d5db', fontsize=13, ha='left')

# 底部注释
fig.text(0.1, 0.06, '*注：数据来源于公司人力资源系统，统计日期截至2022.06.30',
         color='#9CA3AF', fontsize=11, ha='left')

# 图表区域（适配宽画布，留出左侧空间给类别标签）
ax = fig.add_axes([0.3, 0.12, 0.4, 0.65], facecolor=BG)
# 调整X轴范围，给左侧的标签留出位置 (从 -1.5 到 1.15)
ax.set_xlim(-1.5, 1.15)
ax.set_ylim(-1.15, 1.15)
ax.set_aspect('equal')
ax.axis('off')

r_inner = 0.35  # 内孔径
r_outer = 1.0  # 外半径
n = len(ages)
thickness = (r_outer - r_inner) / n

# 绘制玉玦图
for i in range(n):
    ri = r_inner + i * thickness
    ro = ri + thickness
    # 计算角度：占比 / 0.5 * 360 (因为只画半圆/缺口圆)
    angle = shares[i] / 0.5 * 360

    # 1. 绘制圆环扇形（从12点钟方向顺时针绘制）
    ax.add_patch(Wedge((0, 0), ro, 90 - angle, 90, width=thickness,
                       facecolor=colors[i], edgecolor=BG, lw=1.5, zorder=2))

    # 计算该圆环的中线半径
    mid_r = (ri + ro) / 2

    # 2. 在圆环末端标注百分比 (末端角度为 90 - angle)
    th_end = np.radians(90 - angle)
    # 稍微向外偏移一点 (mid_r + 0.08)，避免文字压住圆环
    ax.text((mid_r + 0.00) * np.cos(th_end - 0.08), (mid_r + 0.08) * np.sin(th_end - 0.08),
            percent_labels[i], ha='center', va='center',
            color='#FFFFFF', fontsize=12, fontweight='bold', zorder=4)

    # 3. 在左侧缺口处标注数据范围 (垂直堆叠，与圆环中线对齐)
    # 放在 x = -0.05 位置，右对齐
    ax.text(-0.05, mid_r, ages[i], ha='right', va='center',
            color='#d1d5db', fontsize=13, zorder=4)

plt.show()