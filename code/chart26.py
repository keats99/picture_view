import matplotlib.pyplot as plt
import numpy as np

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 1. 准备数据
regions = ['华北', '华南', '东北', '西北', '西南', '华东']
sales = [2354, 1902, 3524, 2698, 2896, 2563]
yoy = ['12%', '25%', '16%', '21%', '18%', '25%']
x = np.arange(len(regions))

# 2. 颜色配置
bg_color = '#161935'        # 深藏青背景
text_white = '#FFFFFF'      # 白色文字
text_light = '#D1D5DB'      # 浅灰文字
color_bar = '#F04A66'       # 粉红色柱体
color_bubble = '#1F78D1'    # 蓝色气泡
color_axis = '#40466B'      # 底部轴线颜色

# 3. 创建画布
fig, ax = plt.subplots(figsize=(10, 6.5))
fig.patch.set_facecolor(bg_color)
ax.set_facecolor(bg_color)

# 4. 绘制柱状图
width = 0.28
bars = ax.bar(x, sales, width=width, color=color_bar, zorder=3)

# 5. 添加柱子顶部的销量标签
for bar, val in zip(bars, sales):
    ax.text(bar.get_x() + bar.get_width()/2, val + 80, str(val),
            ha='center', va='bottom', color=text_white, fontsize=12, zorder=4)

# 6. ✅ 绘制悬浮的蓝色圆形气泡与同比标签
bubble_y = 4100  # 气泡所在的统一高度（Y轴坐标）
for i, val in enumerate(yoy):
    # 画蓝色圆（使用 scatter 函数，s 控制面积大小，使其呈现完美的圆形）
    ax.scatter(x[i], bubble_y, s=850, color=color_bubble, zorder=4, edgecolors='none')
    # 在圆心写上白色百分比
    ax.text(x[i], bubble_y, val, ha='center', va='center', color=text_white, fontsize=12, zorder=5)

# 7. 配置坐标轴
ax.set_xticks(x)
ax.set_xticklabels(regions, color=text_white, fontsize=12)
ax.tick_params(axis='x', length=0, pad=10)

# 隐藏Y轴刻度和上、左、右边框
ax.set_yticks([])
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)

# 保留底部轴线并修改颜色
ax.spines['bottom'].set_color(color_axis)
ax.spines['bottom'].set_linewidth(1)

# 设置 Y 轴范围，确保气泡不会顶到标题
ax.set_ylim(0, 4800)

# 8. 添加标题、副标题和底部注释（严格左对齐）
fig.text(0.08, 0.88, '各区域上半年销量以同比', color=text_white, fontsize=22, fontweight='bold')
fig.text(0.08, 0.81, '东北区域销量持续保持第一，华东和华南同比去年增长最多', color=text_white, fontsize=14)
fig.text(0.08, 0.04, '*注：数据来源于公司销售系统，统计日期截至2022.06.30', color=text_light, fontsize=11)

# 9. 调整布局
plt.subplots_adjust(top=0.82, bottom=0.12, left=0.08, right=0.92)

plt.show()