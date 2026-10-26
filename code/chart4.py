import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyBboxPatch, Polygon

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 1. 准备数据
items = ['口红', '面膜', '隔离', '防晒', '精华', '面霜', '眼影', '气垫']
sales = [9221, 5102, 6571, 5760, 6321, 8612, 2645, 5321]

# 2. 颜色配置
colors = [
    '#6dcbd8', '#4a9e9e', '#f36e4e', '#f2b93b',
    '#1289d8', '#1266c1', '#5f59bf', '#4a3e9a'
]

x = np.arange(len(items))
width = 0.5

# 3. 创建画布
bg_color = '#1A1E43'
text_white = '#FFFFFF'
text_light = '#A0AABF'
grid_color = '#2E3D63'

fig, ax = plt.subplots(figsize=(12, 6.5))
fig.patch.set_facecolor(bg_color)
ax.set_facecolor(bg_color)

# 4. 绘制纯色柱形图
bars = ax.bar(x, sales, width=width, color=colors, zorder=3)

# 5. ✅ 核心修改：绘制带向下小三角的数据标签（精准控制尺寸，避免覆盖图形）
for i, (xi, yi) in enumerate(zip(x, sales)):
    # 气泡框的尺寸（按照正常视觉比例设定，避免太大）
    box_width = 0.4  # 框宽
    box_height = 700  # 框高
    tri_width = 0.16  # 三角形宽
    tri_height = 150  # 三角形高

    box_color = colors[i]

    # 1. 绘制圆角矩形背景（下沿距离柱顶 150 的高度）
    rect = FancyBboxPatch((xi - box_width / 2, yi + tri_height), box_width, box_height,
                          boxstyle="round,pad=0,rounding_size=0.05",  # 小圆角
                          facecolor=box_color, edgecolor='none', zorder=4)
    ax.add_patch(rect)

    # 2. 绘制向下的小三角形（尖端刚好指向柱子顶部）
    triangle = Polygon([
        [xi - tri_width / 2, yi + tri_height],  # 左底角
        [xi + tri_width / 2, yi + tri_height],  # 右底角
        [xi, yi]  # 尖端
    ], facecolor=box_color, edgecolor='none', zorder=4)
    ax.add_patch(triangle)

    # 3. 绘制数字文本（在圆角矩形的中心）
    ax.text(xi, yi + tri_height + box_height / 2, str(yi),
            ha='center', va='center',
            color=text_white, fontsize=11, fontweight='bold', zorder=5)

# 6. 添加标题、副标题和底部注释
ax.text(0.02, 1.15, '2021年商品销量情况', transform=ax.transAxes,
        color=text_white, fontsize=24, fontweight='bold', ha='left')
ax.text(0.02, 1.06, '口红销量最好达9221，是眼影最低值2645近3.5倍', transform=ax.transAxes,
        color=text_light, fontsize=14, ha='left')

fig.text(0.08, 0.04, '*注：数据来源于公司销售系统，统计日期截至2022.08.31',
         color=text_light, fontsize=11, ha='left')

# 7. 配置坐标轴格式
ax.set_yticks([0, 2000, 4000, 6000, 8000, 10000])
ax.set_yticklabels(['0', '2000', '4000', '6000', '8000', '10000'],
                   color=text_light, fontsize=11)
ax.set_ylim(0, 11500)

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

# 添加水平虚线网格
ax.yaxis.grid(True, linestyle='--', color=grid_color, alpha=0.8, zorder=1)
ax.set_axisbelow(True)

# 8. 调整布局并显示
plt.subplots_adjust(top=0.8, bottom=0.12, left=0.1, right=0.95)

plt.show()