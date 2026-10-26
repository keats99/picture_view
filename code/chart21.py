# -*- coding: utf-8 -*-
"""复现：2021年各部门人数分布 —— 爆炸式玫瑰图（Jupyter 内联显示版）"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

# Windows 常用中文字体（按顺序尝试，找不到会自动跳到下一个）
mpl.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "Noto Sans CJK JP", "Arial Unicode MS"]
mpl.rcParams["axes.unicode_minus"] = False

BG = "#1b2340"                               # 深蓝背景
labels = ["销售部", "技术部", "运营部", "产品部", "人事部", "财务部"]
values = [451, 380, 320, 250, 150, 113]      # 合计 1664
colors = ["#e8506a", "#f5c24b", "#2fb3a4", "#4aa8e8", "#1f4f9e", "#7b5bd6"]

total = sum(values)
N = len(values)

fig = plt.figure(figsize=(9, 6.4), facecolor=BG)
ax = fig.add_subplot(111, polar=True)
ax.set_facecolor(BG)
ax.set_position([0.27, 0.09, 0.46, 0.80])

ax.set_xticks([]); ax.set_yticks([])
ax.spines["polar"].set_visible(False)
ax.set_theta_zero_location("N")
ax.set_theta_direction(-1)          # 顺时针
ax.set_ylim(0, 1.3)

gap = np.deg2rad(1.0)               # 扇形间缝隙
theta_acc = np.deg2rad(3)           # 从 12 点钟略偏右开始
start_angles, spans = [], []
for v in values:
    span = v / total * 2 * np.pi
    start_angles.append(theta_acc)
    spans.append(span)
    theta_acc += span

# 半径缩放：半径也随人数变化，突出销售部/技术部
scale_r = {0: 1.25, 1: 1.05, 2: 0.70, 3: 0.55, 4: 0.40, 5: 0.32}

for i in range(N):
    th0 = start_angles[i] + gap / 2
    th1 = start_angles[i] + spans[i] - gap / 2
    theta = np.linspace(th0, th1, 100)
    ax.fill_between(theta, 0, scale_r[i], color=colors[i], zorder=3 + N - i)
    ax.plot([th0, th0], [0, scale_r[i]], color=BG, lw=1.2, zorder=10)
    ax.plot([th1, th1], [0, scale_r[i]], color=BG, lw=1.2, zorder=10)

# ---------- 引导线 ----------
cx, cy = 0.50, 0.49                 # 极坐标圆心在 figure 中的位置
def edge_pt(i, r):
    """扇形中线、半径 r 处的 figure 坐标"""
    a = start_angles[i] + spans[i] / 2      # 弧度
    return (cx + r * 0.23 * np.sin(a), cy + r * 0.40 * np.cos(a))

def leader(i, r_dot, corner_x, end):
    p_out = edge_pt(i, r_dot)
    corner = (corner_x, end[1])
    xs, ys = zip(p_out, corner, end)
    fig.lines.append(mpl.lines.Line2D(xs, ys, transform=fig.transFigure,
                                      color=colors[i], lw=1.6, zorder=20, clip_on=False))
    fig.patches.append(mpl.patches.Circle(p_out, 0.006, transform=fig.transFigure,
                                          color=colors[i], zorder=21, clip_on=False))

leader(0, 1.16, 0.78, (0.93, 0.62))   # 销售部 → 右
leader(1, 1.00, 0.76, (0.93, 0.20))   # 技术部 → 右下
leader(2, 0.68, 0.28, (0.12, 0.28))   # 运营部 → 左
leader(3, 0.54, 0.28, (0.12, 0.44))   # 产品部 → 左
leader(4, 0.40, 0.32, (0.14, 0.60))   # 人事部 → 左上
leader(5, 0.34, 0.40, (0.20, 0.74))   # 财务部 → 左上

# ---------- 标题 / 副标题 / 脚注 ----------
fig.text(0.07, 0.92, "2021年各部门人数分布", color="white", fontsize=22, fontweight="bold")
fig.text(0.07, 0.855, "公司总人数1664，销售部人数最多451，占比29.2%",
         color="#dfe3f0", fontsize=13)
fig.text(0.045, 0.035, "*注：数据来源于公司人力资源系统，统计日期截至2022.01.01",
         color="#9aa3bf", fontsize=10)

plt.show()          # Jupyter 中直接内联显示
