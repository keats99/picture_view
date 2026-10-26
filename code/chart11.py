import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyBboxPatch
from scipy.interpolate import PchipInterpolator

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 1. 准备数据
months = ['5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月', '1月', '2月', '3月']
sales = [146, 198, 296, 412, 506, 615, 789, 1021, 3782, 3215, 2936]
x = np.arange(len(months))

# 2. 颜色配置
bg_color = '#171B3C'        # 深藏青背景
text_white = '#FFFFFF'      # 白色文字
text_light = '#D1D5DB'      # 浅灰色文字/轴线
color_line = '#E9653B'      # 橙色折线
color_2021 = '#63D2E0'      # 2021 青色块
color_2022 = '#F6C24B'      # 2022 黄色块

# 3. 创建画布
fig, ax = plt.subplots(figsize=(10, 6))
fig.patch.set_facecolor(bg_color)
ax.set_facecolor(bg_color)

# 4. 绘制平滑折线（使用 PchipInterpolator 防止平滑后过冲产生负数）
# Pchip 能保证曲线严格穿过原始数据点，且保持局部单调性
x_smooth = np.linspace(x.min(), x.max(), 300)
spl = PchipInterpolator(x, sales)
y_smooth = spl(x_smooth)

ax.plot(x_smooth, y_smooth, color=color_line, linewidth=2.5, zorder=3)

# 5. 添加最高点标注（1月份，索引为 8）
max_idx = 8
ax.vlines(x[max_idx], 0, sales[max_idx], colors=color_line, linestyles='--', linewidth=1.5, zorder=2)
ax.text(x[max_idx], sales[max_idx] + 150, str(sales[max_idx]),
        color=text_white, ha='center', va='bottom', fontsize=12)

# 6. 配置坐标轴格式
# Y轴配置（橙色文字，千分位逗号，无刻度线）
ax.set_yticks([0, 1000, 2000, 3000, 4000])
ax.set_yticklabels(['0', '1,000', '2,000', '3,000', '4,000'], color=color_line, fontsize=11)
ax.set_ylim(0, 4500)
ax.tick_params(axis='y', length=0, pad=10)

# X轴配置（浅灰色文字，刻度线朝内）
ax.set_xticks(x)
ax.set_xticklabels(months, color=text_light, fontsize=12)
ax.set_xlim(-0.5, len(months) - 0.5)
ax.tick_params(axis='x', direction='in', length=5, colors=text_light, pad=8)

# 隐藏上、左、右边框，只保留底部轴线
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['bottom'].set_color(text_light)
ax.spines['bottom'].set_linewidth(1.5)

# 7. 添加底部的 2021 和 2022 色块
# 使用 transform=ax.transAxes 将坐标系转换为相对画布的比例，方便定位
# 2021 色块
rect_2021 = FancyBboxPatch((0.03, -0.18), 0.64, 0.08, boxstyle="round,pad=0,rounding_size=0.04",
                           transform=ax.transAxes, facecolor=color_2021, edgecolor='none', clip_on=False)
ax.add_patch(rect_2021)
ax.text(0.35, -0.14, '2021', transform=ax.transAxes, color=text_white, ha='center', va='center', fontsize=14, fontweight='bold')

# 2022 色块
rect_2022 = FancyBboxPatch((0.75, -0.18), 0.23, 0.08, boxstyle="round,pad=0,rounding_size=0.04",
                           transform=ax.transAxes, facecolor=color_2022, edgecolor='none', clip_on=False)
ax.add_patch(rect_2022)
ax.text(0.865, -0.14, '2022', transform=ax.transAxes, color=text_white, ha='center', va='center', fontsize=14, fontweight='bold')

# 8. 添加标题、副标题和底部注释（严格左对齐）
ax.text(0.0, 1.10, '化妆品品类月度销量走势', transform=ax.transAxes,
        color=text_white, fontsize=24, fontweight='bold', ha='left')
ax.text(0.0, 1.03, '2022年销量迅速增加，1月最高，销量达到3782', transform=ax.transAxes,
        color=text_light, fontsize=15, ha='left')

fig.text(0.08, 0.04, '*注：数据来源于公司销售系统，统计日期截至2022.03.31',
         color=text_light, fontsize=11, ha='left')

# 9. 调整布局，留出底部色块和顶部标题的空间
plt.subplots_adjust(top=0.82, bottom=0.22, left=0.1, right=0.95)

plt.show()