import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import numpy as np

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 1. 准备数据
tasks = ['制定计划', '方案设计', '资源调配', '第一阶段', '第二阶段', '第三阶段', '项目总结']
start_dates = ['2022-03-01', '2022-03-13', '2022-03-22', '2022-04-02', '2022-04-16', '2022-05-11', '2022-05-26']
durations = [11, 8, 10, 13, 24, 14, 7]
percentages = [51, 32, 21, 85, 36, 68, 68]

# 转换日期格式
start_dts = [datetime.strptime(d, '%Y-%m-%d') for d in start_dates]
start_nums = [mdates.date2num(d) for d in start_dts]

# 2. 颜色配置
bg_color = '#15193B'  # 背景色
color_dark_blue = '#00549F'  # 深蓝色（代表未完成/总周期）
color_light_blue = '#009FE3'  # 亮蓝色（代表已完成）
text_white = '#FFFFFF'  # 白色文字
text_light = '#D1D5DB'  # 浅灰文字
grid_color = '#3E466E'  # 网格线颜色

# 3. 创建画布
fig, ax = plt.subplots(figsize=(10, 6))
fig.patch.set_facecolor(bg_color)
ax.set_facecolor(bg_color)

# Y轴位置（反转Y轴让第一项在最上面）
y_pos = np.arange(len(tasks))
ax.invert_yaxis()

# 4. ✅ 绘制双色进度条与百分比文字
for i in range(len(tasks)):
    # 计算已完成的天数（总天数 * 完成率）
    completed_days = durations[i] * (percentages[i] / 100)

    # 1. 绘制底层深蓝条（总长度）
    ax.barh(y_pos[i], durations[i], left=start_nums[i], height=0.45,
            color=color_dark_blue, edgecolor='none', zorder=3)

    # 2. 绘制顶层亮蓝条（已完成长度）
    ax.barh(y_pos[i], completed_days, left=start_nums[i], height=0.45,
            color=color_light_blue, edgecolor='none', zorder=4)

    # 3. 在总长度的正中间添加百分比文字
    ax.text(start_nums[i] + durations[i] / 2, y_pos[i], f'{percentages[i]}%',
            ha='center', va='center', color=text_white, fontsize=11, fontweight='bold', zorder=5)

# 5. 配置顶部的 X 轴（日期）
x_ticks_dates = ['2022/3/1', '2022/3/16', '2022/3/31', '2022/4/15', '2022/4/30', '2022/5/15', '2022/5/30', '2022/6/14']
x_ticks_dts = [datetime.strptime(d, '%Y/%m/%d') for d in x_ticks_dates]
x_ticks_num = [mdates.date2num(d) for d in x_ticks_dts]

# 将X轴移到顶部
ax.xaxis.tick_top()
ax.xaxis.set_label_position('top')
ax.set_xticks(x_ticks_num)
ax.set_xticklabels(x_ticks_dates, color=text_light, fontsize=11)
ax.tick_params(axis='x', length=0, pad=15)

# 6. 配置左侧的 Y 轴（任务名称）
ax.set_yticks(y_pos)
ax.set_yticklabels(tasks, color=text_light, fontsize=12)
ax.tick_params(axis='y', length=0, pad=15)

# 7. 添加垂直虚线网格
for x_tick in x_ticks_num:
    ax.axvline(x=x_tick, color=grid_color, linestyle='--', linewidth=1.5, zorder=1)

# 8. 设置坐标轴范围与隐藏边框
ax.set_xlim(mdates.date2num(datetime(2022, 2, 15)), mdates.date2num(datetime(2022, 6, 25)))
ax.set_ylim(len(tasks) - 0.5, -0.5)

for spine in ax.spines.values():
    spine.set_visible(False)

# 9. 添加顶部居中标题
ax.set_title('2022年化妆品类目采购项目进度', color=text_white, fontsize=20, fontweight='bold', pad=30)

plt.tight_layout()

plt.show()