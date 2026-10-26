import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Wedge, Rectangle, Circle
import matplotlib.patheffects as path_effects

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 1. 创建画布
fig, ax = plt.subplots(figsize=(10, 8))
fig.patch.set_facecolor('#1A1E3D')
ax.set_facecolor('#1A1E3D')

ax.set_xlim(-1.6, 1.6)
ax.set_ylim(-1.6, 1.6)
ax.set_aspect('equal')
ax.axis('off')

# 2. 白色正方形底板
rect = Rectangle((-1.25, -1.25), 2.5, 2.5, facecolor='white', edgecolor='none', zorder=1)
ax.add_patch(rect)

# 3. 深蓝色大底板
inner_bg = Circle((0, 0), 1.15, facecolor='#1A1E3D', edgecolor='none', zorder=2)
ax.add_patch(inner_bg)

# 4. 循环绘制环形刻度盘
for i in range(15):
    center_angle = 90 - i * 24
    theta1 = center_angle + 12  # 逆时针边界线（左侧）
    theta2 = center_angle - 12  # 顺时针边界线（右侧）

    # 【外圈蓝色环】
    ax.add_patch(Wedge((0, 0), 1.15, theta2, theta1, width=0.05,
                       facecolor='#0070C0', edgecolor='black', lw=1.2, zorder=3))

    # 中间彩色块和数字
    if i <= 5 or i >= 10:
        if i <= 5:
            val = 100 + i * 10
        else:
            val = 50 + (i - 10) * 10

        if 50 <= val <= 80:
            c = '#0F8B8D'  # 青色
        elif 90 <= val <= 110:
            c = '#F3B229'  # 黄色
        elif 120 <= val <= 150:
            c = '#E84D68'  # 红色

        # 【中间彩色刻度环】
        ax.add_patch(Wedge((0, 0), 1.05, theta2, theta1, width=0.20,
                           facecolor=c, edgecolor='black', lw=1.2, zorder=4))

        # ✅ 核心修改：调整位置，紧靠刻度线
        # 角度靠近左边的分割线 (theta1 - 1度)
        text_angle = theta1 - 1
        # 半径提高到 0.81，紧贴彩色块的下边缘
        r_text = 0.81

        rad = np.radians(text_angle)
        x_text = r_text * np.cos(rad)
        y_text = r_text * np.sin(rad)

        # 使用 ha='right'，让文字右侧顶住刻度线
        text = ax.text(x_text, y_text, str(val), ha='right', va='center',
                       color='#FFFFFF', fontsize=13, fontweight='bold', zorder=6)
        # 加一点深色描边
        text.set_path_effects([path_effects.withStroke(linewidth=2.5, foreground='#1A1E3D')])

# 5. 中心白色圆盘
center_circle = Circle((0, 0), 0.70, facecolor='white', edgecolor='none', zorder=5)
ax.add_patch(center_circle)

# 6. 半透明指针
ax.plot([0, -0.45], [0, 0.45], color='#D3D3D3', linewidth=1.5, alpha=0.7, zorder=7)

# 7. 标题
fig.text(0.5, 0.92, '2022年6月29公司整体运营指数良好', color='white', fontsize=24, fontweight='bold', ha='center')

plt.show()