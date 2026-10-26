import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, Rectangle

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 1. 数据与颜色配置
percent = 0.65
bg_color = '#1A1E3D'        # 深藏青背景
water_color = '#0073C2'     # 水球蓝色
border_color = '#2196F3'    # 边框亮蓝色
text_white = '#FFFFFF'      # 白色文字
text_light = '#C5C9DE'      # 浅灰文字

# 2. 创建画布
fig = plt.figure(figsize=(10, 6.5), facecolor=bg_color)

# 3. 配置水球绘图区
ax = fig.add_axes([0.3, 0.1, 0.4, 0.65], facecolor=bg_color)
ax.set_xlim(-1.1, 1.1)
ax.set_ylim(-1.1, 1.1)
ax.set_aspect('equal')  # 保证正圆
ax.axis('off')

# 4. ✅ 绘制双层圆环边框
# 外层较粗的边框
outer_ring = Circle((0, 0), 1.0, facecolor='none', edgecolor=border_color, linewidth=2.5, zorder=2)
ax.add_patch(outer_ring)

# 内层稍细的边框
inner_ring = Circle((0, 0), 0.96, facecolor='none', edgecolor=border_color, linewidth=1.5, zorder=2)
ax.add_patch(inner_ring)

# 5. ✅ 绘制底部水平填充的水位
# 水面高度：0%在底部(-1)，100%在顶部(+1)，所以 65% 对应 -1 + 2*0.65 = 0.3
y_level = 2 * percent - 1

# 用矩形画水位，然后用圆形裁剪
water_rect = Rectangle((-1, -1), 2, y_level - (-1), facecolor=water_color, edgecolor='none', zorder=3)
ax.add_patch(water_rect)

# 裁剪成圆形
clip_circle = Circle((0, 0), 0.96, transform=ax.transData)
water_rect.set_clip_path(clip_circle)

# 6. 添加中心文字
ax.text(0, 0, '65%', ha='center', va='center',
        color=text_white, fontsize=50, zorder=4)

# 7. 添加标题、副标题和底部注释（严格左对齐）
fig.text(0.08, 0.88, '2022年上半年目标完成率', color=text_white, fontsize=22, fontweight='bold')
fig.text(0.08, 0.80, '截至6月30日销售目标总体完成率达到65%', color=text_light, fontsize=14)
fig.text(0.08, 0.06, '*注：数据来源于公司销售系统', color='#9CA3AF', fontsize=11)

plt.show()