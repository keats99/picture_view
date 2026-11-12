import matplotlib.pyplot as plt
import numpy as np

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 1. 准备数据（根据原图提取）
regions = ['华北', '华南', '东北', '西北', '西南', '华东']
sales_2022 = [2354, 1902, 3524, 2698, 2896, 2563]
sales_2021 = [2021, 1563, 3213, 2531, 2631, 2361]
yoy = [16, 22, 10, 7, 10, 9]  # 同比百分比

x = np.arange(len(regions))
width = 0.25  # 柱子较细，且两柱之间有微小间隙

# 2. 颜色配置
bg_color = '#171A3B'  # 深藏青背景
text_white = '#FFFFFF'  # 白色文字
text_light = '#D1D5DB'  # 浅灰文字
color_2022 = '#0070C0'  # 2022年蓝色
color_2021 = '#F0526C'  # 2021年红色
color_line = '#F3B229'  # 折线黄色
color_axis = '#40466B'  # 底部轴线颜色

# 3. 创建画布
fig, ax = plt.subplots(figsize=(10, 6.5))
fig.patch.set_facecolor(bg_color)
ax.set_facecolor(bg_color)

# 4. 绘制双柱状图
# 左柱（2022），右柱（2021）
bars1 = ax.bar(x - width / 2 - 0.01, sales_2022, width, color=color_2022, zorder=3)
bars2 = ax.bar(x + width / 2 + 0.01, sales_2021, width, color=color_2021, zorder=3)

# 添加柱状图数据标签
for bar, val in zip(bars1, sales_2022):
    ax.text(bar.get_x() + bar.get_width() / 2, val + 50, str(val),
            ha='center', va='bottom', color=text_white, fontsize=11, zorder=4)

for bar, val in zip(bars2, sales_2021):
    ax.text(bar.get_x() + bar.get_width() / 2, val + 50, str(val),
            ha='center', va='bottom', color=text_white, fontsize=11, zorder=4)

# 5. ✅ 绘制折线图（将百分比映射到悬浮的视觉高度）
# 根据原图，折线最低点(7%)也远高于最高柱子(3524)，所以强行映射到 3800~4500 区间
min_yoy, max_yoy = 7, 22
base_y, height_scale = 3800, 600
y_vis = [base_y + (val - min_yoy) / (max_yoy - min_yoy) * height_scale for val in yoy]

# 画折线与圆点
ax.plot(x, y_vis, color=color_line, linewidth=2, marker='o', markersize=5, zorder=5)

# 添加折线数据标签
for i, val in enumerate(yoy):
    ax.text(x[i], y_vis[i] + 60, f'{val}%',
            ha='center', va='bottom', color=text_white, fontsize=11, zorder=6)

# 6. ✅ 绘制自定义图例（放在最后一组柱子的右侧上方）
legend_x = 5.4  # 靠近最后一个柱子的右边
legend_y1 = 2000  # 2022图例高度
legend_y2 = 1600  # 2021图例高度

# 2022图例（蓝框）
ax.text(legend_x, legend_y1, '2022', ha='center', va='center',
        color=text_white, fontsize=11,
        bbox=dict(boxstyle="square,pad=0.3", facecolor=bg_color, edgecolor=color_2022, linewidth=1.5), zorder=10)

# 2021图例（红框）
ax.text(legend_x, legend_y2, '2021', ha='center', va='center',
        color=text_white, fontsize=11,
        bbox=dict(boxstyle="square,pad=0.3", facecolor=bg_color, edgecolor=color_2021, linewidth=1.5), zorder=10)

# 7. 配置坐标轴
ax.set_xticks(x)
ax.set_xticklabels(regions, color=text_white, fontsize=12)
ax.tick_params(axis='x', length=0, pad=10)

# 隐藏Y轴刻度和边框
ax.set_yticks([])
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)

# 保留底部轴线
ax.spines['bottom'].set_color(color_axis)
ax.spines['bottom'].set_linewidth(1)

# 设置 Y 轴范围
ax.set_ylim(0, 5000)
ax.set_xlim(-0.6, 6.0)  # X轴范围稍微拉宽一点，给图例留空间

# 8. 添加标题、副标题和底部注释
fig.text(0.08, 0.88, '上半年各月商品销量同比去年情况', color=text_white, fontsize=22, fontweight='bold')
fig.text(0.08, 0.81, '2022年相比于2021年销量都有提升，半年整体提升17%', color=text_white, fontsize=13)
fig.text(0.08, 0.04, '*注：数据来源于公司销售系统，统计日期截至2022.06.30', color=text_light, fontsize=11)

# 9. 调整布局
plt.subplots_adjust(top=0.82, bottom=0.12, left=0.08, right=0.92)

plt.show()