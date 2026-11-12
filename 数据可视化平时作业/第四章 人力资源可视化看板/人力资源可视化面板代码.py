# -*- coding: utf-8 -*-
"""
复刻「第四章 人力资源可视化看板.xlsx」——202203人员基础信息
运行前：把 Excel 和本脚本放在同一目录
"""

import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

# ---------- 0. 全局样式 ----------
mpl.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei",
                                   "Noto Sans CJK SC", "PingFang SC",
                                   "WenQuanYi Micro Hei"]
mpl.rcParams["axes.unicode_minus"] = False

C_BLUE, C_ORANGE, C_RED = "#4E79A7", "#F28E2B", "#E15759"
C_GREEN, C_TEAL, C_PURPLE = "#59A14F", "#76B7B2", "#B07AA1"
C_YELLOW, C_GREY = "#EDC948", "#BAB0AC"
PIE_COLORS = [C_BLUE, C_RED, C_ORANGE, C_GREEN, C_TEAL, C_PURPLE, C_YELLOW]

SRC = r"C:\Users\贾媛媛\Desktop\python数据可视化作业\第四章 人力资源可视化看板.xlsx"
SHEET = "202203人员基础信息"

# ---------- 1. 读取数据（只取 A:H 明细列）----------
df = pd.read_excel(SRC, sheet_name=SHEET, usecols="A:H")
df.columns = ["员工编号", "年龄", "性别", "学历", "婚姻状况", "部门", "本月入转调", "年龄段"]
df = df.dropna(subset=["员工编号"]).copy()
df["员工编号"] = df["员工编号"].astype("int64").astype(str)
df["年龄"] = pd.to_numeric(df["年龄"], errors="coerce")

for c in ["性别", "学历", "婚姻状况", "部门", "本月入转调"]:
    df[c] = df[c].astype("string").str.strip().replace("", pd.NA)

# 用年龄重算年龄段（与 Excel 的 18-24 / 25-29 / 30-34 / 35-39 / 40=< 口径一致）
df["年龄段"] = pd.cut(df["年龄"], bins=[0, 24, 29, 34, 39, 200],
                     labels=["18-24", "25-29", "30-34", "35-39", "40=<"])

# ---------- 2. 指标计算（对应 Excel 里的 COUNTIFS / COUNTA）----------
AGE  = ["18-24", "25-29", "30-34", "35-39", "40=<"]
EDU  = ["专科以下", "专科", "本科", "硕士研究生", "博士研究生"]
MAR  = ["单身", "已婚", "离异"]
SEX  = ["男", "女"]
DEPT = ["销售部", "研发部", "信息技术部", "行政部", "人力资源部", "财务部"]
MOVE = ["入职", "转入", "转出"]

total    = len(df)
age_c    = df["年龄段"].value_counts().reindex(AGE, fill_value=0)
edu_c    = df["学历"].value_counts().reindex(EDU, fill_value=0)
mar_c    = df["婚姻状况"].value_counts().reindex(MAR, fill_value=0)
sex_c    = df["性别"].value_counts().reindex(SEX, fill_value=0)
dept_c   = df["部门"].value_counts().reindex(DEPT, fill_value=0)
move_c   = df["本月入转调"].value_counts().reindex(MOVE, fill_value=0)
move_all = int(df["本月入转调"].notna().sum())      # 等价 COUNTA

# 差值校验（原表 N 列逻辑：总数 - 各维度合计，应为 0）
print(pd.Series({
    "总人数": total,
    "年龄差值": total - age_c.sum(),
    "性别差值": total - sex_c.sum(),
    "学历差值": total - edu_c.sum(),
    "婚姻差值": total - mar_c.sum(),
    "部门差值": total - dept_c.sum(),
    "入转调差值": move_all - move_c.sum(),
}))

# ---------- 3. 绘图辅助函数 ----------
def tidy(ax, title):
    ax.set_facecolor("white")
    ax.grid(axis="y", color="#EEF1F5", lw=1)
    ax.set_axisbelow(True)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color("#D5DAE1")
    ax.tick_params(colors="#6B7280", labelsize=10, length=0)
    ax.set_title(title, loc="left", fontsize=15, fontweight="bold",
                 color="#1F2D3D", pad=14)

def draw_card(ax, main, label, accent):
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
    ax.add_patch(FancyBboxPatch((0.005, 0.06), 0.99, 0.88,
                                boxstyle="round,pad=0,rounding_size=0.09",
                                facecolor="white", edgecolor="none"))
    ax.add_patch(FancyBboxPatch((0.005, 0.06), 0.016, 0.88,
                                boxstyle="round,pad=0,rounding_size=0.02",
                                facecolor=accent, edgecolor="none"))
    ax.text(0.055, 0.56, main, fontsize=26, fontweight="bold",
            color="#1F2D3D", va="center", ha="left")
    ax.text(0.055, 0.22, label, fontsize=10.5, color="#8A94A6",
            va="center", ha="left")

# ---------- 4. 画布布局 ----------
fig = plt.figure(figsize=(19, 12), facecolor="#F2F5F9")
gs = fig.add_gridspec(3, 3, height_ratios=[0.30, 1, 1],
                      hspace=0.42, wspace=0.26,
                      left=0.045, right=0.975, top=0.885, bottom=0.055)

fig.text(0.045, 0.955, "人力资源可视化看板", fontsize=25,
         fontweight="bold", color="#1F2D3D")
fig.text(0.045, 0.922,
         f"数据口径：{SHEET}　|　统计月份：2022-03　|　样本量：{total} 人",
         fontsize=11, color="#8A94A6")

# --- 卡片区 ---
draw_card(fig.add_subplot(gs[0, 0]), f"{total}", "总人数（人）", C_BLUE)
draw_card(fig.add_subplot(gs[0, 1]), f"{df['年龄'].mean():.1f}",
          "平均年龄（岁）", C_PURPLE)
draw_card(fig.add_subplot(gs[0, 2]),
          f"{move_c['入职']} / {move_c['转入']} / {move_c['转出']}",
          "本月入转调（入职 / 转入 / 转出）", C_ORANGE)

# --- ① 年龄分布 ---
ax1 = fig.add_subplot(gs[1, 0])
v = age_c.values.astype(int)
c = [C_BLUE] * len(v); c[int(np.argmax(v))] = C_ORANGE
b = ax1.bar(AGE, v, color=c, width=0.6, zorder=3)
for r, n in zip(b, v):
    ax1.text(r.get_x() + r.get_width() / 2, n + v.max() * 0.03, str(n),
             ha="center", va="bottom", fontsize=11, fontweight="bold", color="#374151")
ax1.set_ylim(0, v.max() * 1.22)
tidy(ax1, "① 年龄段分布")

# --- ② 性别构成 ---
ax2 = fig.add_subplot(gs[1, 1])
sv = sex_c.values.astype(int)
w, _, at = ax2.pie(sv, colors=[C_BLUE, C_RED], startangle=90, counterclock=False,
                   autopct="%.1f%%", pctdistance=0.78, radius=0.85,
                   wedgeprops=dict(width=0.40, edgecolor="white", linewidth=2))
for t in at:
    t.set_color("white"); t.set_fontsize(11); t.set_fontweight("bold")
ax2.legend(w, [f"{k}  {n} 人" for k, n in zip(SEX, sv)],
           loc="center left", bbox_to_anchor=(0.95, 0.5),
           frameon=False, fontsize=10.5)
ax2.set_title("② 性别构成", loc="left", fontsize=15, fontweight="bold",
              color="#1F2D3D", pad=14)

# --- ③ 学历分布 ---
ax3 = fig.add_subplot(gs[1, 2])
ev = edu_c.values.astype(int)
c = [C_BLUE] * len(ev); c[int(np.argmax(ev))] = C_ORANGE
b = ax3.bar(EDU, ev, color=c, width=0.58, zorder=3)
for r, n in zip(b, ev):
    ax3.text(r.get_x() + r.get_width() / 2, n + ev.max() * 0.03, str(n),
             ha="center", va="bottom", fontsize=11, fontweight="bold", color="#374151")
ax3.set_ylim(0, ev.max() * 1.22)
ax3.tick_params(axis="x", labelsize=9)
tidy(ax3, "③ 学历分布")

# --- ④ 婚姻状况 ---
ax4 = fig.add_subplot(gs[2, 0])
mv = mar_c.values.astype(int)
w, _, at = ax4.pie(mv, colors=[C_BLUE, C_GREEN, C_ORANGE], startangle=90,
                   counterclock=False, autopct="%.1f%%", pctdistance=0.78, radius=0.85,
                   wedgeprops=dict(width=0.40, edgecolor="white", linewidth=2))
for t in at:
    t.set_color("white"); t.set_fontsize(11); t.set_fontweight("bold")
ax4.legend(w, [f"{k}  {n} 人" for k, n in zip(MAR, mv)],
           loc="center left", bbox_to_anchor=(0.95, 0.5),
           frameon=False, fontsize=10.5)
ax4.set_title("④ 婚姻状况", loc="left", fontsize=15, fontweight="bold",
              color="#1F2D3D", pad=14)

# --- ⑤ 部门分布（横向条形，越大的排越上）---
ax5 = fig.add_subplot(gs[2, 1])
dv = dept_c.values.astype(int)[::-1]
dl = DEPT[::-1]
c = [C_BLUE] * len(dv); c[int(np.argmax(dv))] = C_ORANGE
b = ax5.barh(dl, dv, color=c, height=0.58, zorder=3)
for r, n in zip(b, dv):
    ax5.text(n + dv.max() * 0.02, r.get_y() + r.get_height() / 2, str(n),
             va="center", ha="left", fontsize=10.5, fontweight="bold", color="#374151")
ax5.set_xlim(0, dv.max() * 1.18)
ax5.grid(axis="x", color="#EEF1F5", lw=1); ax5.grid(axis="y", visible=False)
tidy(ax5, "⑤ 部门人员分布")
ax5.grid(axis="x", color="#EEF1F5", lw=1)
ax5.grid(axis="y", visible=False)

# --- ⑥ 本月入转调 ---
ax6 = fig.add_subplot(gs[2, 2])
tv = move_c.values.astype(int)
b = ax6.bar(MOVE, tv, color=[C_GREEN, C_BLUE, C_RED], width=0.5, zorder=3)
for r, n in zip(b, tv):
    ax6.text(r.get_x() + r.get_width() / 2, n + max(tv.max(), 1) * 0.04, str(n),
             ha="center", va="bottom", fontsize=11, fontweight="bold", color="#374151")
ax6.set_ylim(0, max(tv.max(), 1) * 1.25)
tidy(ax6, "⑥ 本月入转调人数")

plt.savefig("人力资源看板_202203.png", dpi=160, facecolor=fig.get_facecolor())
plt.show()