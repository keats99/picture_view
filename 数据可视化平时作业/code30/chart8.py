import matplotlib.pyplot as plt
import numpy as np

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 1. 准备数据（从上到下）
regions = ['华东', '西南', '西北', '东北', '华南', '华北']
sales = [2109, 1369, 1872, 1536, 1946, 4321]
yoy = ['-5.8%', '-17.9%', '-15.9%', '-9.3%', '-20.8%', '-13.6%']

max_sales = max(sales)  # 4321

# 2. 颜色配置
bg_color = '#171a3c'  # 背景色
color_dark_blue = '#003785'  # 深蓝色（销量）
color_light_blue = '#7fa8d6'  # 浅蓝色（占位）
color_red = '#96323e'  # 红色（同比）
text_white = '#ffffff'  # 白色文字
text_light = '#d1d5db'  # 浅灰文字

# 3. 创建画布
fig, ax = plt.subplots(figsize=(10, 6.5))
fig.patch.set_facecolor(bg_color)
ax.set_facecolor(bg_color)

y_pos = np.arange(len(regions))
height = 0.6

# 设定红色块的固定宽度
red_width = 1200

# 4. 循环绘制每一行的条形图
for i, (region, s, y_val) in enumerate(zip(regions, sales, yoy)):
    # 绘制深蓝色块
    w1 = s
    ax.barh(y_pos[i], w1, height=height, left=0, color=color_dark_blue, zorder=3)

    # 绘制浅蓝色块（如果没达到最大销量，就用浅蓝填补差值）
    w2 = max_sales - w1
    if w2 > 0:
        ax.barh(y_pos[i], w2, height=height, left=w1, color=color_light_blue, zorder=3)

    # 绘制固定宽度的红色块
    ax.barh(y_pos[i], red_width, height=height, left=max_sales, color=color_red, zorder=3)

    # 添加销量数字（在深蓝块内部靠右）
    ax.text(w1 - 100, y_pos[i], str(s), ha='right', va='center', color=text_white, fontsize=12, zorder=4)

    # 添加同比百分比（在红色块正中心）
    ax.text(max_sales + red_width / 2, y_pos[i], y_val, ha='center', va='center', color=text_white, fontsize=12,
            zorder=4)

    # 添加左侧区域名称
    ax.text(-300, y_pos[i], region, ha='right', va='center', color=text_white, fontsize=13, zorder=4)

# 反转Y轴，让“华东”显示在最上面
ax.invert_yaxis()

# 5. 添加标题、副标题和底部注释（严格左对齐）
ax.text(0.0, 1.10, '2021年各区域销量及同比情况', transform=ax.transAxes,
        color=text_white, fontsize=22, fontweight='bold', ha='left')
ax.text(0.0, 1.03, '各区域商品销量同比去年均有下降，其中华南下降最多，同比下降20.8%', transform=ax.transAxes,
        color=text_white, fontsize=13, ha='left')

fig.text(0.08, 0.04, '*注：数据来源于公司销售系统，统计日期截至2022.01.01',
         color=text_light, fontsize=11, ha='left')

# 6. 配置坐标轴格式
ax.set_xlim(-1800, 6000)
ax.set_ylim(len(regions) - 0.5, -0.5)

# 隐藏所有边框和刻度
ax.axis('off')

# 7. 调整布局并显示
plt.subplots_adjust(top=0.85, bottom=0.1, left=0.08, right=0.95)

plt.show()