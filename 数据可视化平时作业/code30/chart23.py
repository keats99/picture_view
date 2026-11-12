import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as mpatches
import matplotlib.lines as mlines

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 1. 准备数据
years = ['2017', '2018', '2019', '2020', '2021', '2022']
sales = [1603, 2106, 2406, 3265, 3721, 3921]
growth = [27, 31, 14, 36, 14, 5]
x = np.arange(len(years))

# 2. ✅ 重新校准坐标映射：抬高基线，拉开折线
min_pct, max_pct = 5, 36
# 把基线从 4050 拔高到 4250，起伏比例调整为 550
base_y, height_scale = 4250, 550
y_vis = [base_y + (g - min_pct) / (max_pct - min_pct) * height_scale for g in growth]

# 3. 颜色配置
bg_color = '#191B3B'        # 深藏青背景
text_white = '#FFFFFF'      # 白色文字
text_light = '#C5C9DE'      # 浅灰文字
color_bar = '#0070C0'       # 柱状图蓝色
color_line = '#ED4A64'      # 折线图红色

# 4. 创建画布
fig, ax = plt.subplots(figsize=(10, 6.5))
fig.patch.set_facecolor(bg_color)
ax.set_facecolor(bg_color)

# 5. 绘制柱状图
width = 0.35
bars = ax.bar(x, sales, width=width, color=color_bar, zorder=3)

# 添加柱状图数据标签
for bar, val in zip(bars, sales):
    ax.text(bar.get_x() + bar.get_width()/2, val + 80, str(val),
             ha='center', va='bottom', color=text_white, fontsize=12, zorder=4)

# 6. ✅ 绘制折线图
ax.plot(x, y_vis, color=color_line, linewidth=2, marker='o', markersize=6, zorder=5)

# 添加折线图数据标签
for i, val in enumerate(growth):
    if i == 0:
        # 2017年稍微往左偏
        ax.text(x[i] - 0.15, y_vis[i] + 50, f'{val}%',
                ha='right', va='bottom', color=text_white, fontsize=12, zorder=6)
    elif i == 5:
        # ✅ 2022年（5%）：文字向右上偏移，彻底避开 3921
        ax.text(x[i] + 0.1, y_vis[i] + 60, f'{val}%',
                ha='left', va='bottom', color=text_white, fontsize=12, zorder=6)
    else:
        ax.text(x[i], y_vis[i] + 50, f'{val}%',
                ha='center', va='bottom', color=text_white, fontsize=12, zorder=6)

# 7. 配置坐标轴
ax.set_xticks(x)
ax.set_xticklabels(years, color=text_white, fontsize=12)
ax.tick_params(axis='x', length=0, pad=10)

# 隐藏 Y 轴刻度和所有边框
ax.set_yticks([])
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['bottom'].set_visible(False)

# 设置 Y 轴范围
ax.set_ylim(0, 5400)

# 8. 自定义图例
legend_bar = mpatches.Patch(color=color_bar, label='销售量')
legend_line = mlines.Line2D([], [], color=color_line, marker='o', markersize=5, label='同比', linewidth=2)

ax.legend(handles=[legend_bar, legend_line], loc='upper right', bbox_to_anchor=(0.92, 0.98),
           frameon=False, labelcolor=text_white, fontsize=12,
           ncol=2, handletextpad=0.5, columnspacing=1.5)

# 9. 添加标题、副标题和底部注释
fig.text(0.08, 0.88, '近六年销售量及增长率', color=text_white, fontsize=22, fontweight='bold')
fig.text(0.08, 0.81, '平台销量近6年持续增长，但近两年增长率有所放缓', color=text_light, fontsize=14)
fig.text(0.08, 0.04, '*注：数据来源于公司销售系统', color=text_light, fontsize=11)

# 10. 调整布局
plt.subplots_adjust(top=0.82, bottom=0.12, left=0.08, right=0.92)

plt.show()