import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 配色方案 (与之前深色仪表盘风格统一)
BG = '#171c45'        # 深蓝色背景 (贴合右图)
EMPTY = '#0a1128'     # 空球部分（更深的蓝色，形成对比）
WATER = '#1a56db'     # 水的颜色 (亮蓝色)
EDGE = '#2b7aee'      # 圆框边缘颜色

percent = 0.65

# 创建画布
fig = plt.figure(figsize=(10, 5.5), facecolor=BG)

# 1. 添加左对齐的主标题和副标题
fig.text(0.1, 0.85, '本科及以上学历员占比', color='#FFFFFF', fontsize=22, fontweight='bold', ha='left')
fig.text(0.1, 0.78, '6月30日最新统计数据本科及以上员工占比65%', color='#d1d5db', fontsize=13, ha='left')

# 2. 调整水球在画布中的位置 (留出顶部标题和底部备注的空间)
ax = fig.add_axes([0.3, 0.05, 0.4, 0.65], facecolor=BG)
ax.set_xlim(-1.15, 1.15)
ax.set_ylim(-1.15, 1.15)
ax.set_aspect('equal')
ax.axis('off')

# 3. 绘制球体边框 (亮蓝色细边框，深色内部)
ball = Circle((0, 0), 1.0, facecolor=EMPTY, edgecolor=EDGE, lw=2, zorder=1)
ax.add_patch(ball)

# 4. 水面正弦波计算
# 水位高度：0%在底部(-1)，100%在顶部(+1)
y_level = 2 * percent - 1
x = np.linspace(-1, 1, 1000)
# 调整波浪频率和振幅，使其接近右图（波峰波谷明显，平滑）
wave = y_level + 0.04 * np.sin(x * 2 * np.pi / 0.8)

# 5. 水体积填充与裁剪
clip = Circle((0, 0), 1.0, transform=ax.transData)
water = ax.fill_between(x, -1.0, wave, color=WATER, zorder=2)
water.set_clip_path(clip)

# 水面不需要描边，去掉原来的 plot 线条即可

# 6. 中心大号文字 (只保留65%)
ax.text(0, -0.05, '65%', ha='center', va='center',
        color='#FFFFFF', fontsize=50, fontweight='bold', zorder=4)

# 7. 底部数据来源备注
fig.text(0.1, 0.05, '*注：数据来源于公司人力资源系统',
         color='#9CA3AF', fontsize=11, ha='left')

plt.show()