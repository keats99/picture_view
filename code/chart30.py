import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 1. 准备数据（从上到下：华南到华东）
regions = ['华南', '华北', '东北', '西北', '华东']
pct_2022 = [86, 74, 62, 51, 35]
pct_2021 = [90, 68, 54, 45, 42]

# 2. 颜色配置
bg_color = '#171A3B'
text_white = '#FFFFFF'
text_light = '#D1D5DB'
color_bar_bg = '#6B7280'
color_bar_fg = '#0070C0'
color_dot_2022 = '#0070C0'
color_dot_2021 = '#8B93A5'

# 3. 创建画布
fig, ax = plt.subplots(figsize=(10, 6.5))
fig.patch.set_facecolor(bg_color)
ax.set_facecolor(bg_color)

bar_height = 0.35
bar_max_width = 100
y_positions = np.arange(len(regions))

# 4. 循环绘制每一行
for i in range(len(regions)):
    y = y_positions[i]
    p22 = pct_2022[i]
    p21 = pct_2021[i]

    # 1. 背景灰槽
    bg_rect = patches.FancyBboxPatch(
        (0, y - bar_height / 2), bar_max_width, bar_height,
        boxstyle=f"round,pad=0,rounding_size={bar_height / 2}",
        facecolor=color_bar_bg, edgecolor='none', zorder=2
    )
    ax.add_patch(bg_rect)

    # 2. 前景蓝条
    fg_rect = patches.FancyBboxPatch(
        (0, y - bar_height / 2), p22, bar_height,
        boxstyle=f"round,pad=0,rounding_size={bar_height / 2}",
        facecolor=color_bar_fg, edgecolor='none', zorder=3
    )
    ax.add_patch(fg_rect)

    # 3. 2021 年灰点
    ax.scatter(p21, y, s=280, color=color_dot_2021, edgecolors=text_white, linewidth=2, zorder=4)

    # 4. 2022 年蓝点
    ax.scatter(p22, y, s=280, color=color_dot_2022, edgecolors=text_white, linewidth=2, zorder=5)

    # 5. ✅ 核心修复：百分比文本放在蓝点正上方（y 轴反转后，减号才是向上）
    ax.text(p22, y - 0.32, f'{p22}%', ha='center', va='bottom',
            color=text_white, fontsize=12, zorder=6)

    # 6. 左侧区域标签
    ax.text(-8, y, regions[i], ha='right', va='center',
            color=text_white, fontsize=13, zorder=6)

# 5. 绘制左上角的图例（同样因为 Y 轴反转，用负数坐标放在最顶上）
ax.scatter(0, -1.0, s=180, color=color_dot_2022, edgecolors=text_white, linewidth=1.5, clip_on=False)
ax.text(3, -1.0, '2022完成率', ha='left', va='center', color=text_white, fontsize=12)

ax.scatter(22, -1.0, s=180, color=color_dot_2021, edgecolors=text_white, linewidth=1.5, clip_on=False)
ax.text(25, -1.0, '2021完成率', ha='left', va='center', color=text_white, fontsize=12)

# 6. 反转 Y 轴
ax.invert_yaxis()

# 7. 配置坐标轴范围
ax.set_xlim(0, 110)
ax.set_ylim(len(regions) - 0.2, -1.5)  # 上方留出空间给图例

# 隐藏边框和刻度
ax.set_xticks([])
ax.set_yticks([])
for spine in ax.spines.values():
    spine.set_visible(False)

# 8. 添加标题、副标题和底部注释
fig.text(0.08, 0.88, '2022年上半年销量目标达成率同比去年情况', color=text_white, fontsize=22, fontweight='bold')
fig.text(0.08, 0.81, '华南完成率最高达到86%，华东最低35%，其中华南和华东不及2021年', color=text_light, fontsize=13)
fig.text(0.08, 0.05, '*注：数据来源于公司销售系统，统计日期截至2022.06.30', color=text_light, fontsize=11)

# 9. 调整布局
plt.subplots_adjust(top=0.82, bottom=0.12, left=0.15, right=0.92)

plt.show()