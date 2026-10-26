import matplotlib.pyplot as plt
import numpy as np

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 1. 准备数据（严格按原图从上到下的顺序）
regions = ['华南', '华北', '东北', '西北', '华东']
sales_2022 = [2238, 1531, 1426, 1321, 1215]  # 左侧 2022 数据
sales_2021 = [2066, 1436, 1531, 1265, 1003]  # 右侧 2021 数据

# 2. 坐标轴与颜色配置
y = np.arange(len(regions))
height = 0.4  # 柱子高度

bg_color = '#1A1E43'        # 背景色
text_white = '#FFFFFF'      # 白色文字
color_2022 = '#0F7FCE'      # 2022年蓝色
color_2021 = '#F0526C'      # 2021年红色

# 3. 创建画布
fig, ax = plt.subplots(figsize=(12, 7))
fig.patch.set_facecolor(bg_color)
ax.set_facecolor(bg_color)

# 4. 绘制蝴蝶图
ax.barh(y, [-v for v in sales_2022], height=height, left=-200,
        color=color_2022, edgecolor='none', zorder=3)
ax.barh(y, sales_2021, height=height, left=200,
        color=color_2021, edgecolor='none', zorder=3)

# 5. 添加数据标签和区域名称
for i in range(len(regions)):
    ax.text(-250, y[i], str(sales_2022[i]), ha='right', va='center',
            color=text_white, fontsize=12, fontweight='bold', zorder=5)
    ax.text(250, y[i], str(sales_2021[i]), ha='left', va='center',
            color=text_white, fontsize=12, fontweight='bold', zorder=5)
    ax.text(0, y[i], regions[i], ha='center', va='center',
            color=text_white, fontsize=13, fontweight='bold', zorder=6)

# 6. ✅ 修改点：将年份标签移到最上方
# 放在华南（y=4）的上方，y坐标改为 4.8
ax.text(-1300, 4.8, '2022', ha='center', va='center',
        color=color_2022, fontsize=15, fontweight='bold', zorder=5)
ax.text(1300, 4.8, '2021', ha='center', va='center',
        color=color_2021, fontsize=15, fontweight='bold', zorder=5)

# 7. 添加标题、副标题和底部注释（严格左对齐）
ax.text(0.0, 1.12, '2022年上半年各区域对比去年销量', transform=ax.transAxes,
        color=text_white, fontsize=22, fontweight='bold', ha='left')
ax.text(0.0, 1.05, '2022年整体销量高于2021年，只有东北区域较2021有所下降', transform=ax.transAxes,
        color=text_white, fontsize=13, ha='left')

fig.text(0.08, 0.04, '*注：数据来源于公司销售系统，统计日期截至2022.06.30',
         color=text_white, fontsize=11, ha='left')

# 8. 配置坐标轴格式
ax.set_xlim(-2800, 2800)
# ✅ 修改点：Y轴上限从 4.5 调到 5.5，给顶部的 2022/2021 留出空间
ax.set_ylim(-1.2, 5.5)

# 隐藏刻度与边框
ax.set_xticks([])
ax.set_yticks([])
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['bottom'].set_visible(False)

# 9. 调整布局并显示
plt.subplots_adjust(top=0.85, bottom=0.1, left=0.08, right=0.92)

plt.show()