import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 1. 准备数据（按原图从上到下：华南到华东）
regions = ['华南', '华北', '东北', '西北', '华东']
percentages = [86, 74, 62, 51, 35]

# 2. 颜色配置
bg_color = '#171A3B'  # 深藏青背景
text_white = '#FFFFFF'  # 白色文字
text_light = '#D1D5DB'  # 浅灰文字
color_bar_bg = '#6B7280'  # 进度条底色（灰色）
color_bar_fg = '#0070C0'  # 进度条前景（蓝色）
color_dot = '#0070C0'  # 滑块圆点颜色

# 3. 创建画布
fig, ax = plt.subplots(figsize=(10, 6))
fig.patch.set_facecolor(bg_color)
ax.set_facecolor(bg_color)

# 4. 循环绘制每一条进度条
bar_height = 0.4  # 进度条高度
bar_max_width = 100  # 进度条最大宽度（对应100%）
y_positions = np.arange(len(regions))

for i in range(len(regions)):
    y = y_positions[i]
    pct = percentages[i]

    # 1. 绘制背景灰条（圆角矩形）
    bg_rect = patches.FancyBboxPatch(
        (0, y - bar_height / 2), bar_max_width, bar_height,
        boxstyle=f"round,pad=0,rounding_size={bar_height / 2}",
        facecolor=color_bar_bg, edgecolor='none', zorder=2
    )
    ax.add_patch(bg_rect)

    # 2. 绘制前景蓝条（圆角矩形）
    fg_rect = patches.FancyBboxPatch(
        (0, y - bar_height / 2), pct, bar_height,
        boxstyle=f"round,pad=0,rounding_size={bar_height / 2}",
        facecolor=color_bar_fg, edgecolor='none', zorder=3
    )
    ax.add_patch(fg_rect)

    # 3. 绘制末端的带白边滑块圆点
    ax.scatter(pct, y, s=450, color=color_dot, edgecolors=text_white, linewidth=2.5, zorder=5)

    # 4. 添加百分比文本（放在滑块左侧）
    ax.text(pct - 4, y, f'{pct}%', ha='right', va='center',
            color=text_white, fontsize=12, zorder=6)

    # 5. 添加左侧区域标签
    ax.text(-8, y, regions[i], ha='right', va='center',
            color=text_light, fontsize=13, zorder=6)

# 5. ✅ 核心修复：反转 Y 轴，让排名第一的数据显示在最上方
ax.invert_yaxis()

# 6. 配置坐标轴
ax.set_xlim(0, 110)
ax.set_ylim(len(regions) - 0.6, -0.6)  # 反转后的合理边界

# 隐藏所有边框和刻度
ax.set_xticks([])
ax.set_yticks([])
for spine in ax.spines.values():
    spine.set_visible(False)

# 7. 添加标题、副标题和底部注释
fig.text(0.08, 0.88, '2022年上半年产品销量目标达成率情况', color=text_white, fontsize=22, fontweight='bold')
fig.text(0.08, 0.81, '华南完成率最高达到86%，华东最低35%', color=text_light, fontsize=14)
fig.text(0.08, 0.06, '*注：数据来源于公司销售系统，统计日期截至2022.06.30', color=text_light, fontsize=11)

# 8. 调整布局
plt.subplots_adjust(top=0.82, bottom=0.12, left=0.15, right=0.92)

plt.show()