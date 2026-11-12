import matplotlib.pyplot as plt
import numpy as np

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 1. 准备数据
quarters = ['2021Q1', 'Q2', 'Q3', 'Q4', '2022Q1', 'Q2']
sales = [3121, 4086, 4321, 4601, 4936, 4231]
profit = [1020, 1421, 1502, 1623, 1781, 1432]

x = np.arange(len(quarters))

# ✅ 修改点1：缩小柱宽并拉大偏移量，防止柱子粘连
width = 0.25
offset = 0.14

# 2. 颜色配置
bg_color = '#1A1E43'       # 背景色
text_white = '#FFFFFF'      # 白色文字
text_light = '#A0AABF'      # 浅灰文字
grid_color = '#2E3D63'      # 网格线颜色
sales_color = '#0F7FCE'     # 销售额蓝色
profit_color = '#EE4760'    # 利润额红色

# 3. 创建画布
fig, ax = plt.subplots(figsize=(12, 6.5))
fig.patch.set_facecolor(bg_color)
ax.set_facecolor(bg_color)

# 4. 绘制分组柱形图
# 销售额柱子（左）
bars1 = ax.bar(x - offset, sales, width, color=sales_color, zorder=3)
# 利润额柱子（右）
bars2 = ax.bar(x + offset, profit, width, color=profit_color, zorder=3)

# 5. 添加数据标签（纯白数字）
for bar, yi in zip(bars1, sales):
    ax.text(bar.get_x() + bar.get_width()/2, yi + 80, str(yi),
            ha='center', va='bottom', color=text_white, fontsize=11, zorder=5)
for bar, yi in zip(bars2, profit):
    ax.text(bar.get_x() + bar.get_width()/2, yi + 80, str(yi),
            ha='center', va='bottom', color=text_white, fontsize=11, zorder=5)

# 6. ✅ 修改点2：图例精准叠在最后一组柱子上
# 最后一组柱子的 x 坐标是 5（即 2022Q2）
legend_x = 5
legend_y1 = 3800 # 销售额图例高度
legend_y2 = 3100 # 利润额图例高度

# 绘制带蓝色边框的“销售额”图例（带深色背景框，zorder=10 保证盖在柱子上）
ax.text(legend_x, legend_y1, '销售额', ha='center', va='center',
        color=text_white, fontsize=12,
        bbox=dict(boxstyle="square,pad=0.4", facecolor=bg_color, edgecolor=sales_color, linewidth=1.5),
        zorder=10)

# 绘制带红色边框的“利润额”图例
ax.text(legend_x, legend_y2, '利润额', ha='center', va='center',
        color=text_white, fontsize=12,
        bbox=dict(boxstyle="square,pad=0.4", facecolor=bg_color, edgecolor=profit_color, linewidth=1.5),
        zorder=10)

# 7. 添加标题、副标题和底部注释
ax.text(0.02, 1.15, '2021年至今季度销售额(万)和利润额(万)', transform=ax.transAxes,
        color=text_white, fontsize=22, fontweight='bold', ha='left')
ax.text(0.02, 1.06, '2022年第二季度销售额首次出现下降，降幅达到15%', transform=ax.transAxes,
        color=text_light, fontsize=14, ha='left')

fig.text(0.08, 0.04, '*注：数据来源于公司销售系统，统计日期截至2022.06.30',
         color=text_light, fontsize=11, ha='left')

# 8. 配置坐标轴格式
ax.set_yticks([0, 2000, 4000, 6000])
ax.set_yticklabels(['0', '2000', '4000', '6000'],
                   color=text_light, fontsize=11)
ax.set_ylim(0, 5800)

ax.set_xticks(x)
ax.set_xticklabels(quarters, color=text_light, fontsize=12)

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

# 9. 调整布局并显示
plt.subplots_adjust(top=0.8, bottom=0.12, left=0.08, right=0.95)

plt.show()