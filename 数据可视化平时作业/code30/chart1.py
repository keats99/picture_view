import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.patches import Rectangle

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 数据
regions = ['华北', '华南', '东北', '西北', '西南', '华东']
sales = [2354, 1902, 3524, 2698, 2896, 2563]

# 配色方案
bg_color = '#0a1128'  # 背景深色
text_light = '#d1d5db'  # 浅色文字
text_white = '#ffffff'  # 白色文字
grid_color = '#2a3b5c'  # 网格线颜色

# ✅ 恢复渐变：青蓝色渐变色带（底部深蓝 -> 顶部亮青）
cmap = LinearSegmentedColormap.from_list('grad', ['#0077b6', '#00b4d8', '#90e0ef'])

# 创建图表
fig, ax = plt.subplots(figsize=(10, 5.5))
fig.patch.set_facecolor(bg_color)
ax.set_facecolor(bg_color)

x = np.arange(len(regions))
width = 0.45  # 柱子宽度

# ✅ 使用 imshow + clip_path 绘制渐变柱形图
for xi, yi in zip(x, sales):
    # 生成渐变矩阵
    grad = np.linspace(0, 1, 100).reshape(-1, 1)
    # 绘制渐变图并放置在对应坐标
    im = ax.imshow(grad, extent=[xi - width / 2, xi + width / 2, 0, yi],
                   aspect='auto', cmap=cmap, origin='lower', zorder=3)
    # 创建矩形轮廓，用来裁剪渐变图
    rect = Rectangle((xi - width / 2, 0), width, yi, transform=ax.transData)
    im.set_clip_path(rect)

    # 柱顶外部的白色数值标签
    ax.text(xi, yi + 100, str(yi), ha='center', va='bottom',
            color=text_white, fontsize=11, fontweight='bold', zorder=4)

# 添加主标题和副标题
ax.text(0, 1.15, '3月各区域销量分布', transform=ax.transAxes,
        fontsize=22, fontweight='bold', color=text_white, ha='left')
ax.text(0, 1.08, '东北销量最多占总销量的22%，华南销量最低', transform=ax.transAxes,
        fontsize=13, color=text_light, ha='left')

# ✅ 精确控制Y轴刻度，只保留千位数 (0, 1000, 2000, 3000, 4000)
ax.set_yticks([0, 1000, 2000, 3000, 4000])
ax.set_yticklabels(['0', '1000', '2000', '3000', '4000'], color=text_light, fontsize=11)

# 设置X轴样式
ax.set_xticks(x)
ax.set_xticklabels(regions, color=text_light, fontsize=12)
ax.tick_params(axis='x', length=0, pad=8)
ax.tick_params(axis='y', length=0, pad=8)

# 设置范围
ax.set_ylim(0, 4200)
ax.set_xlim(-0.6, len(regions) - 0.4)

# 隐藏边框
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['bottom'].set_color(grid_color)

# 优化网格线，将其放在柱子底层
ax.yaxis.grid(True, linestyle='--', color=grid_color, alpha=0.7, zorder=1)
ax.set_axisbelow(True)  # 保证网格线在柱子下方

# 底部注释提亮加深
fig.text(0.1, 0.02, '*注：数据来源于公司销售系统，统计日期截至2022.03.31',
         color='#cbd5e1', fontsize=11, fontweight='bold', ha='left')

# 调整布局
plt.subplots_adjust(top=0.85, bottom=0.15, left=0.1, right=0.95)

plt.show()