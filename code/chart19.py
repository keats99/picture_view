import matplotlib.pyplot as plt
import numpy as np

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 1. 准备数据
sizes = [29.2, 22.7, 17.5, 13.6, 10.3, 6.7]
# 从12点钟方向顺时针的颜色 (精准提取原图颜色)
colors = ['#E84D68', '#F7C354', '#10A8AD', '#0071C1', '#35A2D9', '#7031A1']

# 2. 创建画布与背景色（标准宽幅比例，深藏青色背景）
fig = plt.figure(figsize=(12, 7), facecolor='#1A1E43')

# ✅ 调整图表位置，使饼图居中（给左侧标题和四周引出线留出空间）
ax = fig.add_axes([0.2, 0.1, 0.6, 0.75], facecolor='#1A1E43')

# 3. 绘制饼图
wedges, texts = ax.pie(
    sizes,
    colors=colors,
    startangle=90,  # 从12点钟方向开始
    counterclock=False,  # 顺时针排列
    wedgeprops={'edgecolor': '#1A1E43', 'linewidth': 1.5}  # 扇区间隙使用背景色
)

# 4. ✅ 精准复刻 Excel 标准引出线 (斜线向外 + 水平线 + 末端小圆点)
for i, wedge in enumerate(wedges):
    # 获取当前扇形的中间角度
    theta1, theta2 = wedge.theta1, wedge.theta2
    mid_angle = np.radians((theta1 + theta2) / 2)

    # 起点：饼图边缘 (半径1.0)
    x1 = np.cos(mid_angle)
    y1 = np.sin(mid_angle)

    # 拐点：向外延伸一段距离 (半径1.15)
    r_bend = 1.15
    x2 = r_bend * np.cos(mid_angle)
    y2 = r_bend * np.sin(mid_angle)

    # 终点：水平延伸 (向左或向右延伸0.25)
    x3 = x2 + 0.25 if x2 > 0 else x2 - 0.25
    y3 = y2

    # 绘制折线 (斜线 + 水平线)
    ax.plot([x1, x2, x3], [y1, y2, y3], color=colors[i], linewidth=1.2, zorder=5)

    # 在水平线末端绘制小圆点
    ax.plot(x3, y3, marker='o', markersize=5, color=colors[i], zorder=10)

# 5. 添加标题、副标题和底部注释（严格左对齐）
fig.text(0.06, 0.88, '2021年各部门人数分布', color='#FFFFFF', fontsize=24, fontweight='bold', ha='left')
fig.text(0.06, 0.81, '公司总人数1664，销售部人数最多451，占比29.2%', color='#D1D5DB', fontsize=15, ha='left')
fig.text(0.06, 0.06, '*注：数据来源于公司人力资源系统，统计日期截至2022.01.01',
         color='#9CA3AF', fontsize=11, ha='left')

# 6. 最终调整，隐藏坐标轴
ax.set_xlim(-1.6, 1.6)
ax.set_ylim(-1.4, 1.4)
ax.axis('off')

plt.show()