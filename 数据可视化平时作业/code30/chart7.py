import matplotlib.pyplot as plt
import numpy as np

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei']
plt.rcParams['axes.unicode_minus'] = False
# ✅ 关键设置：调整纹理线条的粗细，使其接近原图的密度
plt.rcParams['hatch.linewidth'] = 1.2

# 1. 准备数据（从上到下：华东、西北、东北、华北、华南）
regions = ['华东', '西北', '东北', '华北', '华南']
sales_2022 = [36, 31, 18, 13, 9]  # 2022年百分比
sales_2021 = [42, 26, 19, 12, 5]  # 2021年百分比

y = np.arange(len(regions))
height = 0.4  # 数据条高度

# 2. 颜色配置
bg_color = '#141A42'  # 深藏青色背景
text_white = '#FFFFFF'  # 白色文字
color_2022 = '#0070C0'  # 2022年蓝色
color_2021 = '#F05060'  # 2021年红色

# 3. 创建画布
fig, ax = plt.subplots(figsize=(12, 7))
fig.patch.set_facecolor(bg_color)
ax.set_facecolor(bg_color)

# 4. ✅ 绘制核心的“条形码”数据条（使用 hatch 生成垂直线，无填充色）
# 左侧 2022 数据条：从中心向左延伸，left=-2 表示起点，宽度为负值
ax.barh(y, [-v for v in sales_2022], left=-2, height=height,
        facecolor='none', edgecolor=color_2022, hatch='|||||', linewidth=0, zorder=3)
# 右侧 2021 数据条：从中心向右延伸，left=2 表示起点，宽度为正值
ax.barh(y, sales_2021, left=2, height=height,
        facecolor='none', edgecolor=color_2021, hatch='|||||', linewidth=0, zorder=3)

# 5. 添加数据标签和区域名称
for i in range(len(regions)):
    # 左侧数字：紧贴中心间隙的左边
    ax.text(-4, y[i], f'{sales_2022[i]}%', ha='right', va='center',
            color=text_white, fontsize=12, fontweight='bold', zorder=5)
    # 右侧数字：紧贴中心间隙的右边
    ax.text(4, y[i], f'{sales_2021[i]}%', ha='left', va='center',
            color=text_white, fontsize=12, fontweight='bold', zorder=5)

    # 中心区域名称：精准居中
    ax.text(0, y[i], regions[i], ha='center', va='center',
            color=text_white, fontsize=13, fontweight='bold', zorder=6)

# 6. 添加标题、副标题和底部注释（严格左对齐，统一白色）
ax.text(0.0, 1.10, '2022年第一季度销售目标完成情况', transform=ax.transAxes,
        color=text_white, fontsize=22, fontweight='bold', ha='left')
ax.text(0.0, 1.04, '华东区域完成率最高达到36%，但是相比去年的42%有所下降', transform=ax.transAxes,
        color=text_white, fontsize=13, ha='left')

fig.text(0.08, 0.04, '*注：数据来源于公司销售系统，统计日期截至2022.03.31',
         color=text_white, fontsize=11, ha='left')

# 7. 配置坐标轴格式
# 设置X轴范围，左侧留出空间，右侧留出空间
ax.set_xlim(-50, 50)
# 设置Y轴范围，留出上下空间
ax.set_ylim(-0.8, len(regions) - 0.2)

# 隐藏刻度与边框
ax.set_xticks([])
ax.set_yticks([])
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['bottom'].set_visible(False)

# 8. 调整布局并显示
plt.subplots_adjust(top=0.85, bottom=0.1, left=0.08, right=0.92)
plt.show()