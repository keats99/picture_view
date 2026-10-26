import matplotlib.pyplot as plt
import numpy as np
import matplotlib.lines as mlines

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 1. 准备数据
months = ['1月', '2月', '3月', '4月', '5月', '6月']
sales_2021 = [1686, 1345, 1934, 1658, 1865, 1936]
sales_2022 = [1385, 1846, 1654, 1936, 2564, 2236]
x = np.arange(len(months))

# 2. 颜色配置
bg_color = '#1A1E3D'        # 深藏青背景
text_white = '#FFFFFF'      # 白色文字
text_light = '#A0AABF'      # 浅灰文字
grid_color = '#3E466E'      # 网格线颜色
color_2021 = '#E84D68'      # 2021粉红色
color_2022 = '#0F7FCE'      # 2022蓝色

# 3. 创建画布
fig, ax = plt.subplots(figsize=(10, 6.5))
fig.patch.set_facecolor(bg_color)
ax.set_facecolor(bg_color)

# 4. 绘制折线图（带圆点标记）
ax.plot(x, sales_2021, color=color_2021, linewidth=2, marker='o', markersize=5, zorder=3)
ax.plot(x, sales_2022, color=color_2022, linewidth=2, marker='o', markersize=5, zorder=3)

# 5. ✅ 精准放置数据标签（根据原图的高低交错放置，避免重叠）
# 2021年数据标签位置
for i in range(len(x)):
    offset = 80 if i in [0, 2] else -120  # 1月和3月在上方，其余在下方
    ax.text(x[i], sales_2021[i] + offset, str(sales_2021[i]),
            ha='center', va='center', color=text_light, fontsize=11, zorder=5)

# 2022年数据标签位置
for i in range(len(x)):
    offset = 80 if i in [1, 3, 4, 5] else -120  # 2,3,4,6月在上方，1月,3月在下方
    ax.text(x[i], sales_2022[i] + offset, str(sales_2022[i]),
            ha='center', va='center', color=text_white, fontsize=11, zorder=5)

# 6. 自定义图例（右上角，无边框）
# 手动创建带圆点的线图例
legend_2021 = mlines.Line2D([], [], color=color_2021, marker='o', markersize=5, label='2021年', linewidth=2)
legend_2022 = mlines.Line2D([], [], color=color_2022, marker='o', markersize=5, label='2022年', linewidth=2)

# 将图例放在图表内部右上方，去掉边框
ax.legend(handles=[legend_2021, legend_2022], loc='upper right', bbox_to_anchor=(0.9, 0.95),
          frameon=False, labelcolor=text_white, fontsize=11, handlelength=1.5, handletextpad=0.5, ncol=2)

# 7. 添加标题、副标题和底部注释（严格左对齐）
ax.text(0.0, 1.10, '2022年上半年各月同比去年销量', transform=ax.transAxes,
        color=text_white, fontsize=22, fontweight='bold', ha='left')
ax.text(0.0, 1.03, '上半年同比去年增长明显，5月份同比增长最多，增长近40%', transform=ax.transAxes,
        color=text_light, fontsize=13, ha='left')

fig.text(0.08, 0.04, '*注：数据来源于公司销售系统，统计日期截至2022.06.30',
         color=text_light, fontsize=11, ha='left')

# 8. 配置坐标轴与网格
# Y轴刻度
ax.set_yticks([0, 500, 1000, 1500, 2000, 2500, 3000])
ax.set_yticklabels(['0', '500', '1000', '1500', '2000', '2500', '3000'], color=text_light, fontsize=11)

# X轴刻度
ax.set_xticks(x)
ax.set_xticklabels(months, color=text_light, fontsize=12)

# 隐藏刻度线，设置范围
ax.tick_params(axis='x', length=0, pad=10)
ax.tick_params(axis='y', length=0, pad=10)
ax.set_ylim(0, 3200)
ax.set_xlim(-0.5, len(months) - 0.5)

# 隐藏四周的边框线
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['bottom'].set_visible(False)

# 添加水平虚线网格（放在底层）
ax.yaxis.grid(True, linestyle='--', color=grid_color, alpha=0.8, zorder=1)
ax.set_axisbelow(True)

# 9. 调整布局并显示
plt.subplots_adjust(top=0.85, bottom=0.12, left=0.08, right=0.95)
plt.show()