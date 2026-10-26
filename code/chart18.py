import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Wedge

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei']
plt.rcParams['axes.unicode_minus'] = False

BG = '#1A1E43'

depts = ['人力部', '行政部', '财务部', '工程部', '采购部', '销售部']
people = [130, 226, 238, 293, 326, 451]
colors = ['#7030A0', '#0070C0', '#37A2DA', '#11A7AD', '#F5C353', '#E74E69']  # 内 → 外
total = 832  # 保持你的原逻辑

# 稍微加宽画布
fig = plt.figure(figsize=(10, 6.8), facecolor=BG)

# 左对齐标题和副标题
fig.text(0.1, 0.88, '2022年上半年各部门人数', color='#FFFFFF', fontsize=22, fontweight='bold', ha='left')
fig.text(0.1, 0.81, '公司总人数1664，销售部人数最多451，占比27%', color='#d1d5db', fontsize=13, ha='left')

# 底部注释
fig.text(0.1, 0.06, '*注：数据来源于公司人力资源系统，统计日期截至2022.06.30',
         color='#9CA3AF', fontsize=11, ha='left')

# 调整坐标轴范围（左边界稍微调到 -1.0 即可，足够放字了）
ax = fig.add_axes([0.05, 0.04, 0.90, 0.75], facecolor=BG)
ax.set_xlim(-1.0, 1.15)  # 左边界从 -1.6 收紧到 -1.0
ax.set_ylim(-1.15, 1.15)
ax.set_aspect('equal')
ax.axis('off')

r_inner = 0.45  # 你的原参数
r_outer = 1.0  # 你的原参数
n = len(depts)
thickness = (r_outer - r_inner) / n

for i in range(n):
    ri = r_inner + i * thickness
    ro = ri + thickness
    angle = people[i] / total * 360
    ax.add_patch(Wedge((0, 0), ro, 90 - angle, 90, width=thickness,
                       facecolor=colors[i], edgecolor=BG, lw=2.0, zorder=2))

    # ✅ 核心修复：x 坐标改为 -0.05，右对齐，这样文字就贴着圆环起点（12点钟方向）了
    ax.text(-0.05, ro, f'{depts[i]} {people[i]}', ha='right', va='center',
            color='#d1d5db', fontsize=12, zorder=4)
plt.show()