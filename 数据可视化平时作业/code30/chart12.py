import matplotlib.pyplot as plt
import numpy as np

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 1. 准备数据
months = ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月']
rates = [0.536, 0.498, 0.527, 0.708, 0.609, 0.496, 0.586, 0.704]
x = np.arange(len(months))

# 2. 颜色配置
bg_color = '#1A1E3D'        # 深藏青色背景
color_line = '#EA435F'      # 粉红色线条和菱形
text_white = '#FFFFFF'      # 主标题白色
text_light = '#C5C9DE'      # 副标题、标签浅灰
axis_color = '#40466B'      # 底部轴线深灰紫色

# 3. 创建画布
fig, ax = plt.subplots(figsize=(10, 6.5))
fig.patch.set_facecolor(bg_color)
ax.set_facecolor(bg_color)

# 4. ✅ 绘制棒棒糖图
# 画垂直细线（从 y=0 开始，到对应的数值）
ax.vlines(x, 0, rates, color=color_line, linewidth=1.5, zorder=3)

# 画顶部的空心菱形（markerfacecolor='none' 表示内部透明）
ax.plot(x, rates, linestyle='none', marker='d', markersize=10,
        markerfacecolor='none', markeredgecolor=color_line, markeredgewidth=2, zorder=4)

# 5. 添加数据标签（在菱形上方）
for i, rate in enumerate(rates):
    ax.text(x[i], rate + 0.025, f'{rate:.2%}', ha='center', va='bottom',
            color=text_white, fontsize=11, zorder=5)

# 6. 添加标题、副标题和底部注释（严格左对齐）
ax.text(0.0, 1.10, '2022年1-8月公司计划完成率', transform=ax.transAxes,
        color=text_white, fontsize=22, fontweight='bold', ha='left')
ax.text(0.0, 1.04, '公司整体完成率55%，4月和8月超过70%，2月和6月较低未过半', transform=ax.transAxes,
        color=text_light, fontsize=13, ha='left')

fig.text(0.08, 0.04, '*注：数据来源于公司销售系统，统计日期截至2022.08.31',
         color=text_light, fontsize=11, ha='left')

# 7. 配置坐标轴格式
# Y轴：完全隐藏刻度和边框
ax.set_yticks([])
ax.spines['left'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# X轴：保留底部轴线，修改颜色，隐藏刻度线
ax.spines['bottom'].set_color(axis_color)
ax.spines['bottom'].set_linewidth(1.5)
ax.set_xticks(x)
ax.set_xticklabels(months, color=text_light, fontsize=12)
ax.tick_params(axis='x', length=0, pad=10)

# 设置Y轴范围，留出顶部标注的空间
ax.set_ylim(0, 0.85)

# 8. 调整布局并显示
plt.subplots_adjust(top=0.85, bottom=0.12, left=0.08, right=0.95)

plt.show()