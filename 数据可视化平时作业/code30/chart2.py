import matplotlib.pyplot as plt
import numpy as np

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 数据
regions = ['华北', '华南', '东北', '西北', '西南', '华东']
sales = [2354, 1902, 3524, 2698, 2896, 2563]
mean_val = np.mean(sales)  # 均值约为 2656

# 配色方案
bg_color = '#0a1128'      # 背景深色
text_light = '#d1d5db'    # 浅色文字
text_white = '#ffffff'    # 白色文字
line_color = '#f0c040'    # 均值线橙黄色
grid_color = '#2a3b5c'    # 网格线颜色
bar_color = '#00b4d8'     # 柱形图纯色

# 创建图表
fig, ax = plt.subplots(figsize=(10, 5.5))
fig.patch.set_facecolor(bg_color)
ax.set_facecolor(bg_color)

x = np.arange(len(regions))
width = 0.5

# 绘制纯色柱形图
bars = ax.bar(x, sales, width=width, color=bar_color, zorder=2)

# ✅ 关键修改：将数值标签放入柱子内部（向下偏移 150，并垂直居中）
for bar, yi in zip(bars, sales):
    ax.text(bar.get_x() + bar.get_width()/2, yi - 150, str(yi),
            ha='center', va='center', color=text_white,
            fontsize=11, fontweight='bold', zorder=3)

# 均值线（橙黄色实线）
ax.axhline(mean_val, color=line_color, linestyle='-', linewidth=1.5, zorder=4)

# ✅ 关键修改：将“平均值”文字移到图表右上角，紧贴均值线之上
# 放在最后一个柱子右侧 (len(regions)-0.4)，抬高 80，右对齐
ax.text(len(regions) - 0.4, mean_val + 80, f'平均值: {int(mean_val)}',
        color=line_color, fontsize=12, fontweight='bold',
        ha='right', va='bottom', zorder=5)

# 添加主标题和副标题
ax.text(0, 1.15, '3月各区域销量分布', transform=ax.transAxes,
        fontsize=20, fontweight='bold', color=text_white, ha='left')
ax.text(0, 1.08, '东北销量最多占总销量的22%，华南销量最低', transform=ax.transAxes,
        fontsize=12, color=text_light, ha='left')

# 设置坐标轴样式
ax.set_xticks(x)
ax.set_xticklabels(regions, color=text_light, fontsize=12)
ax.tick_params(axis='x', length=0, pad=8)
ax.tick_params(axis='y', colors=text_light, labelsize=11)

# Y轴范围稍微调高，给顶部留出空间
ax.set_ylim(0, max(sales) * 1.2)
ax.set_xlim(-0.6, len(regions) - 0.4)

# 隐藏边框
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['bottom'].set_color(grid_color)
ax.set_ylabel('')

# 添加水平虚线网格
ax.yaxis.grid(True, linestyle='--', color=grid_color, alpha=0.5, zorder=1)

# 底部注释（颜色提亮加深）
fig.text(0.1, 0.02, '*注：数据来源于公司销售系统，统计日期截至2022.03.31',
         color='#cbd5e1', fontsize=10, fontweight='bold', ha='left')

# 调整布局
plt.subplots_adjust(top=0.85, bottom=0.15, left=0.1, right=0.95)

plt.show()