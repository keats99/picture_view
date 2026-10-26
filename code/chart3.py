import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.patches import FancyBboxPatch

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 1. 准备数据
items = ['口红', '面膜', '隔离', '防晒', '精华', '面霜']
sales = [653, 523, 648, 856, 714, 785]
x = np.arange(len(items))
width = 0.16  # 柱子宽度

# 2. 颜色配置
bg_color = '#1A1E43'  # 背景色
text_white = '#FFFFFF'  # 标题白色
text_light = '#A0AABF'  # 副标题和刻度浅灰
grid_color = '#2E3D63'  # 网格线颜色
line_color = '#5A7BA6'  # 引出线颜色
dot_color = '#3B82F6'  # 顶部小圆点颜色
label_bg = '#1A2A4A'  # 数据标签背景框颜色

# 柱子渐变颜色（底部深蓝 -> 顶部亮青）
cmap = LinearSegmentedColormap.from_list('grad', ['#005bb5', '#00e5ff'])

# 3. 创建画布
fig, ax = plt.subplots(figsize=(12, 6.5))
fig.patch.set_facecolor(bg_color)
ax.set_facecolor(bg_color)

# 4. 绘制上下圆角柱形图（核心修复：使用 FancyBboxPatch 上下圆角）
for xi, yi in zip(x, sales):
    # 生成渐变矩阵
    grad = np.linspace(0, 1, 100).reshape(-1, 1)
    # 绘制渐变图
    im = ax.imshow(grad, extent=[xi - width / 2, xi + width / 2, 0, yi],
                   aspect='auto', cmap=cmap, origin='lower', zorder=3)

    # ✅ 使用圆角矩形，rounding_size 为 width/2，实现上下两端的半圆效果
    box = FancyBboxPatch((xi - width / 2, 0), width, yi,
                         boxstyle=f"round,pad=0,rounding_size={width / 2}",
                         transform=ax.transData, facecolor='none', edgecolor='none')
    ax.add_patch(box)
    im.set_clip_path(box)

# 5. 绘制引出线、圆点和数据标签
offset_y = 70  # 线条长度
for xi, yi in zip(x, sales):
    dot_y = yi + offset_y

    # 引出线（从柱子顶端最高处 yi 向上延伸）
    ax.plot([xi, xi], [yi, dot_y], color=line_color, linewidth=1.5, zorder=4)

    # 顶部小圆点
    ax.plot(xi, dot_y, marker='o', markersize=8,
            color=dot_color, markeredgecolor='#8CA9D6', markeredgewidth=1, zorder=5)

    # 右侧数据标签（带深色背景框）
    ax.text(xi + 0.08, dot_y, str(yi),
            ha='left', va='center',
            color=text_white, fontsize=11, fontweight='bold',
            bbox=dict(boxstyle="round,pad=0.3", fc=label_bg, ec="none", alpha=0.95),
            zorder=6)

# 6. 添加标题、副标题和底部注释
ax.text(0.02, 1.15, '3月商品销量对比', transform=ax.transAxes,
        color=text_white, fontsize=24, fontweight='bold', ha='left')
ax.text(0.02, 1.06, '防晒销量最多，3月销量856；面膜最少，3月销量523', transform=ax.transAxes,
        color=text_light, fontsize=14, ha='left')

fig.text(0.08, 0.04, '*注：数据来源于公司销售系统，统计日期截至2022.03.31',
         color=text_light, fontsize=11, ha='left')

# 7. 配置坐标轴格式
# 设置Y轴刻度和范围
ax.set_yticks([0, 200, 400, 600, 800, 1000, 1200])
ax.set_yticklabels(['0', '200', '400', '600', '800', '1000', '1200'],
                   color=text_light, fontsize=11)
# ✅ 关键修复：Y轴下限设为 -width/2，让柱子底部的半圆能完整显示，不被截断
ax.set_ylim(-width / 2, 1150)

# 设置X轴标签
ax.set_xticks(x)
ax.set_xticklabels(items, color=text_light, fontsize=12)

# 隐藏四周边框
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['bottom'].set_visible(False)

# 隐藏刻度线
ax.tick_params(axis='x', length=0, pad=8)
ax.tick_params(axis='y', length=0, pad=8)

# 添加水平虚线网格（放在柱子底层）
ax.yaxis.grid(True, linestyle='--', color=grid_color, alpha=0.8, zorder=1)
ax.set_axisbelow(True)

# 8. 调整布局并显示
plt.subplots_adjust(top=0.8, bottom=0.12, left=0.1, right=0.95)

plt.show()