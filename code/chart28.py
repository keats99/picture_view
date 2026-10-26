import matplotlib.pyplot as plt
import numpy as np

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 1. 准备数据
months = ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月']
monthly_sales = [2354, 1902, 3524, 2698, 2896, 2563, 3156, 2896, 3621, 2635, 2963, 2789]
quarterly_sales = [7780, 8157, 9673, 8387]

x = np.arange(len(months))
x_q = [1, 4, 7, 10]  # 四个季度的中心点坐标

# 2. 颜色配置
bg_color = '#171A3B'        # 深藏青背景
text_white = '#FFFFFF'      # 白色文字
text_light = '#D1D5DB'      # 浅灰文字

# 季度大柱子的暗色系
color_q1 = '#283477' # 深蓝
color_q2 = '#4F3232' # 深棕
color_q3 = '#4B3B25' # 深橄榄
color_q4 = '#3D254A' # 深紫

# 月度小柱子的亮色系
color_m1 = '#4A73DF' # 亮蓝
color_m2 = '#F05B0A' # 橙色
color_m3 = '#F5B500' # 金黄
color_m4 = '#C04682' # 粉紫

# 3. 创建画布
fig, ax = plt.subplots(figsize=(10, 6.5))
fig.patch.set_facecolor(bg_color)
ax.set_facecolor(bg_color)

# 4. ✅ 绘制底层大柱子（季度总销量）
width_q = 2.8
ax.bar(x_q[0], quarterly_sales[0], width=width_q, color=color_q1, zorder=2)
ax.bar(x_q[1], quarterly_sales[1], width=width_q, color=color_q2, zorder=2)
ax.bar(x_q[2], quarterly_sales[2], width=width_q, color=color_q3, zorder=2)
ax.bar(x_q[3], quarterly_sales[3], width=width_q, color=color_q4, zorder=2)

# 5. ✅ 绘制顶层小柱子（单月销量）
width_m = 0.4
for i in range(12):
    if i < 3: c = color_m1
    elif i < 6: c = color_m2
    elif i < 9: c = color_m3
    else: c = color_m4
    ax.bar(x[i], monthly_sales[i], width=width_m, color=c, zorder=3)

# 6. 添加数据标签
# 季度总销量标签
for i in range(4):
    ax.text(x_q[i], quarterly_sales[i] + 100, str(quarterly_sales[i]),
            ha='center', va='bottom', color=text_white, fontsize=12, zorder=4)

# 单月销量标签
for i in range(12):
    ax.text(x[i], monthly_sales[i] + 100, str(monthly_sales[i]),
            ha='center', va='bottom', color=text_white, fontsize=11, zorder=5)

# 7. 配置坐标轴
ax.set_xticks(x)
ax.set_xticklabels(months, color=text_light, fontsize=12)
ax.tick_params(axis='x', length=0, pad=10)

# 隐藏 Y 轴刻度和所有边框
ax.set_yticks([])
for spine in ax.spines.values():
    spine.set_visible(False)

# 设置 Y 轴范围，给顶部标签留出空间
ax.set_ylim(0, 11000)
ax.set_xlim(-0.8, 11.8)

# 8. 添加标题、副标题和底部注释（严格左对齐）
fig.text(0.08, 0.88, '2021年各月化妆品销量走势', color=text_white, fontsize=22, fontweight='bold')
fig.text(0.08, 0.81, '2021年第三季度销量最多9673，9月单月销量最大3621', color=text_light, fontsize=14)
fig.text(0.08, 0.04, '*注：数据来源于公司销售系统，统计日期截至2021.12.31', color=text_light, fontsize=11)

# 9. 调整布局
plt.subplots_adjust(top=0.82, bottom=0.12, left=0.08, right=0.92)

plt.show()