import matplotlib.pyplot as plt
import numpy as np

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 1. 准备数据
goods = ['口红', '面膜', '隔离', '防晒', '精华']
sales_2021 = [3568, 4135, 4436, 4106, 4936]
sales_2022 = [2569, 3241, 2965, 3209, 3541]
diff = [a - b for a, b in zip(sales_2021, sales_2022)]  # 计算差值

x = np.arange(len(goods))
width = 0.28  # 柱子宽度

# 2. 颜色与样式配置
bg_color = '#181a35'  # 背景色
color_2021 = '#1072d2'  # 2021年深蓝色
color_2022 = '#7ba3ce'  # 2022年浅灰蓝色
text_white = '#ffffff'  # 白色文字
text_light = '#a3acc8'  # 浅灰文字
grid_color = '#3b4268'  # X轴底线颜色

# 3. 创建画布
fig, ax = plt.subplots(figsize=(10, 7))
fig.patch.set_facecolor(bg_color)
ax.set_facecolor(bg_color)

# 4. 绘制双柱状图
bars_2021 = ax.bar(x - width / 2, sales_2021, width, color=color_2021, zorder=3)
bars_2022 = ax.bar(x + width / 2, sales_2022, width, color=color_2022, zorder=3)

# 5. 添加数据标签和差值箭头
for i in range(len(goods)):
    # 2021年顶部标签（浅灰色）
    ax.text(x[i] - width / 2, sales_2021[i] + 100, str(sales_2021[i]),
            ha='center', va='bottom', color=text_light, fontsize=11, zorder=4)

    # 2022年内部/顶部标签（原图中数字在浅色柱子内部上方）
    ax.text(x[i] + width / 2, sales_2022[i] - 150, str(sales_2022[i]),
            ha='center', va='top', color=text_white, fontsize=11, zorder=4)

    # ✅ 绘制带箭头的垂直差值标注
    # 箭头的起点：2022柱子顶部，终点：2021柱子顶部高度
    ax.annotate('',
                xy=(x[i] + width / 2, sales_2021[i]),  # 箭头指向
                xytext=(x[i] + width / 2, sales_2022[i]),  # 箭头起点
                arrowprops=dict(arrowstyle="-|>", color="white", lw=1.5, mutation_scale=12),
                zorder=5)

    # 差值数字（放在箭头右侧，高度取两柱的中间偏上位置）
    mid_y = sales_2022[i] + (sales_2021[i] - sales_2022[i]) / 2
    ax.text(x[i] + width / 2 + 0.1, mid_y, str(diff[i]),
            ha='left', va='center', color=text_light, fontsize=11, zorder=5)

# 6. 自定义图例（左上角手动绘制方块和文字）
# 画 2021 图例
ax.plot(0.02, 0.95, marker='s', markersize=8, color=color_2021, transform=ax.transAxes)
ax.text(0.05, 0.95, '2021销量', ha='left', va='center', color=text_light, fontsize=11, transform=ax.transAxes)

# 画 2022 图例
ax.plot(0.15, 0.95, marker='s', markersize=8, color=color_2022, transform=ax.transAxes)
ax.text(0.18, 0.95, '2022销量', ha='left', va='center', color=text_light, fontsize=11, transform=ax.transAxes)

# 7. 添加标题、副标题和底部注释（严格左对齐）
ax.text(0.0, 1.08, '2022年商品对比去年销售情况', transform=ax.transAxes,
        color=text_white, fontsize=22, fontweight='bold', ha='left')
ax.text(0.0, 1.02, '商品整体比去年销量有所下降，其中隔离下降最多，下降33%', transform=ax.transAxes,
        color=text_light, fontsize=13, ha='left')

fig.text(0.08, 0.03, '*注：数据来源于公司销售系统，统计日期截至2022.01.01',
         color=text_light, fontsize=11, ha='left')

# 8. 配置坐标轴格式
ax.set_ylim(0, 5600)  # 留出顶部空间
ax.set_xticks(x)
ax.set_xticklabels(goods, color=text_light, fontsize=13)
ax.tick_params(axis='x', length=0, pad=15)  # 隐藏刻度线，拉开与轴线的距离

# 隐藏Y轴刻度
ax.set_yticks([])

# 隐藏顶部、右侧、左侧边框，只保留底部底边线
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['bottom'].set_visible(True)
ax.spines['bottom'].set_color(grid_color)
ax.spines['bottom'].set_linewidth(1.5)

# 9. 调整布局并显示
plt.subplots_adjust(top=0.85, bottom=0.12, left=0.08, right=0.95)

plt.show()