import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Wedge
import matplotlib.colors as mcolors

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 1. 颜色配置
bg_color = '#171A38'        # 深藏青背景
color_unfinished = '#2D3352'# 未完成部分（深灰蓝）
color_text = '#FFFFFF'      # 主文字
color_subtext = '#C5C9DE'   # 浅灰文字

# 2. 创建画布
fig = plt.figure(figsize=(10, 6.5), facecolor=bg_color)

# 3. 配置圆环绘图区（✅ 增大画布空间，居中显示）
# [左边距, 底边距, 宽度, 高度]
ax = fig.add_axes([0.3, 0.05, 0.45, 0.75], facecolor=bg_color)
ax.set_xlim(-1.1, 1.1)
ax.set_ylim(-1.1, 1.1)
ax.set_aspect('equal')  # 保证绝对正圆
ax.axis('off')

# 4. ✅ 纯矢量绘制渐变圆环
cmap = mcolors.LinearSegmentedColormap.from_list('custom', ['#E84D68', '#7A2E9E'])
start_angle = 154
end_angle = 360 + 100
n_segments = 200

# 把圆环宽度从 0.15 加粗到 0.18
ring_width = 0.18

for i in range(n_segments):
    a1 = start_angle + (end_angle - start_angle) * i / n_segments
    a2 = start_angle + (end_angle - start_angle) * (i + 1) / n_segments
    t = i / n_segments
    color = cmap(t)
    ax.add_patch(Wedge((0, 0), 1.0, a1, a2, width=ring_width, facecolor=color, edgecolor='none', zorder=2))

# 5. 绘制未完成的 15% 缺口
unfinished = Wedge((0, 0), 1.0, 100, 154, width=ring_width, facecolor=color_unfinished, edgecolor='none', zorder=3)
ax.add_patch(unfinished)

# 6. 添加中心文字（字体稍微放大，配合大圆环）
ax.text(0, 0.05, '85%', ha='center', va='center', color=color_text, fontsize=56)
ax.text(0, -0.28, '目标完成率', ha='center', va='center', color=color_subtext, fontsize=15)

# 7. 添加标题、副标题和底部注释
fig.text(0.08, 0.88, '2022年上半年目标完成率', color=color_text, fontsize=22, fontweight='bold')
fig.text(0.08, 0.80, '截至6月30日销售目标总体完成率达到85%', color=color_subtext, fontsize=14)

fig.text(0.08, 0.06, '*注：数据来源于公司销售系统', color='#9CA3AF', fontsize=11)

plt.show()