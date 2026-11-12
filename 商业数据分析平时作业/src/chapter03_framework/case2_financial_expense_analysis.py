# -*- coding: utf-8 -*-
import pandas as pd
import matplotlib.pyplot as plt
import os
import warnings
import re

warnings.filterwarnings('ignore')

# ==========================================
# 0. 环境与路径配置 (已修改独立输出路径)
# ==========================================
BASE_DIR = r"D:\Python_code\cda和数据可视化作业\商业数据分析平时作业"
DATA_DIR = os.path.join(BASE_DIR, "data", "chapter03_framework")
SRC_DIR = os.path.join(BASE_DIR, "src", "chapter03_framework")
# 修改点：增加 case2_financial_expense 子文件夹
OUT_DIR = os.path.join(BASE_DIR, "output", "chapter03_framework", "case2_financial_expense")

os.makedirs(OUT_DIR, exist_ok=True)
os.makedirs(SRC_DIR, exist_ok=True)

file_path = os.path.join(DATA_DIR, "案例2：财务费用分析-原始数据.xlsx")

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

if not os.path.exists(file_path):
    raise FileNotFoundError(f"❌ 找不到数据文件，请确认路径：\n{file_path}")


# ==========================================
# 1. 数据读取与清洗
# ==========================================
def clean_month(val):
    if pd.isna(val): return val
    val_str = str(val)
    match = re.search(r'\d+', val_str)
    return int(match.group()) if match else val


# 1.1 读取总费用数据
df_total = pd.read_excel(file_path, sheet_name="总费用数据")
df_total['月份'] = df_total['月份'].apply(clean_month)
df_total['金额'] = pd.to_numeric(df_total['金额'], errors='coerce')
df_total = df_total.dropna(subset=['月份', '金额'])
df_total['月份'] = df_total['月份'].astype(int)

# 1.2 读取三大期间费用数据
df_period = pd.read_excel(file_path, sheet_name="财务三大期间费用数据")
df_period['月份'] = df_period['月份'].apply(clean_month)
df_period['金额'] = pd.to_numeric(df_period['金额'], errors='coerce')
df_period = df_period.dropna(subset=['月份', '期间费用项', '金额'])
df_period['月份'] = df_period['月份'].astype(int)

# 1.3 读取管理费用数据
df_mgmt = pd.read_excel(file_path, sheet_name="管理费用数据")
cols_mgmt = df_mgmt.columns.tolist()
if '份' in cols_mgmt:
    df_mgmt = df_mgmt.rename(columns={'份': '月份'})
elif '月份' not in cols_mgmt:
    df_mgmt.columns.values[1] = '月份'

df_mgmt['月份'] = df_mgmt['月份'].apply(clean_month)
df_mgmt['金额'] = pd.to_numeric(df_mgmt['金额'], errors='coerce')
df_mgmt = df_mgmt.dropna(subset=['月份', '管理费用项', '金额'])
df_mgmt['月份'] = df_mgmt['月份'].astype(int)

# ==========================================
# 2. 核心分析与导出
# ==========================================
# --- 步骤 1：总财务费用对比分析 ---
df_total.to_csv(os.path.join(OUT_DIR, "1_总财务费用对比.csv"), index=False, encoding='gbk')

# --- 步骤 2：三大期间财务费用7月较6月增长情况 ---
pivot_period = pd.pivot_table(df_period, index='期间费用项', columns='月份', values='金额', aggfunc='sum').fillna(0)
m_prev, m_curr = 6, 7
if m_prev in pivot_period.columns and m_curr in pivot_period.columns:
    pivot_period['环比差额'] = pivot_period[m_curr] - pivot_period[m_prev]
else:
    sorted_cols = sorted([c for c in pivot_period.columns if isinstance(c, int)])
    if len(sorted_cols) >= 2:
        m_prev, m_curr = sorted_cols[-2], sorted_cols[-1]
        pivot_period['环比差额'] = pivot_period[m_curr] - pivot_period[m_prev]

pivot_period = pivot_period.reset_index()
pivot_period.to_csv(os.path.join(OUT_DIR, "2_三大期间费用环比.csv"), index=False, encoding='gbk')

# --- 步骤 3：管理费用项7月较6月增长分析 ---
pivot_mgmt = pd.pivot_table(df_mgmt, index='管理费用项', columns='月份', values='金额', aggfunc='sum').fillna(0)
if m_prev in pivot_mgmt.columns and m_curr in pivot_mgmt.columns:
    pivot_mgmt['环比增长率'] = (pivot_mgmt[m_curr] - pivot_mgmt[m_prev]) / pivot_mgmt[m_prev].replace(0, pd.NA)
else:
    pivot_mgmt['环比增长率'] = (pivot_mgmt[m_curr] - pivot_mgmt[m_prev]) / pivot_mgmt[m_prev].replace(0, pd.NA)

pivot_mgmt = pivot_mgmt.reset_index().sort_values(by='环比增长率', ascending=False)
pivot_mgmt.to_csv(os.path.join(OUT_DIR, "3_管理费用项环比.csv"), index=False, encoding='gbk')

# ==========================================
# 3. 可视化制图
# ==========================================
# 图1：总财务费用对比分析
fig, ax = plt.subplots(figsize=(8, 5))
bars = ax.bar(df_total['月份'].astype(str) + '月', df_total['金额'], color=['#4C72B0', '#DD8452'], width=0.4)
for bar in bars:
    yval = bar.get_height()
    ax.text(bar.get_x() + bar.get_width() / 2, yval + 20000, f"{yval / 10000:.1f}万", ha='center', va='bottom',
            fontsize=11)
ax.set_title('总财务费用对比分析', fontsize=14)
ax.set_xlabel('月份', fontsize=12)
ax.set_ylabel('金额', fontsize=12)
ax.set_ylim(0, max(df_total['金额']) * 1.15)
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "图1_总财务费用对比.png"), dpi=300)
plt.close()

# 图2：三大期间费用6月与7月对比
fig, ax = plt.subplots(figsize=(10, 6))
x = range(len(pivot_period))
width = 0.35
ax.bar([i - width / 2 for i in x], pivot_period[m_prev], width, label=f'{m_prev}月', color='#55A868')
ax.bar([i + width / 2 for i in x], pivot_period[m_curr], width, label=f'{m_curr}月', color='#C44E52')
ax.set_xticks(x)
ax.set_xticklabels(pivot_period['期间费用项'])
ax.set_title('三大期间财务费用环比对比', fontsize=14)
ax.set_ylabel('金额', fontsize=12)
ax.legend()
for i, v in enumerate(pivot_period[m_prev]):
    ax.text(i - width / 2, v + 10000, f"{v / 10000:.1f}万", ha='center', fontsize=9)
for i, v in enumerate(pivot_period[m_curr]):
    ax.text(i + width / 2, v + 10000, f"{v / 10000:.1f}万", ha='center', fontsize=9)
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "图2_三大期间费用环比.png"), dpi=300)
plt.close()

# 图3：管理费用各项环比增长率
fig, ax = plt.subplots(figsize=(10, 6))
colors = ['#C44E52' if x < 0 else '#55A868' for x in pivot_mgmt['环比增长率']]
ax.barh(pivot_mgmt['管理费用项'], pivot_mgmt['环比增长率'], color=colors)
ax.set_title('管理费用各明细项环比增长率', fontsize=14)
ax.set_xlabel('环比增长率', fontsize=12)
ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:.2%}".format(x)))
ax.grid(axis='x', linestyle='--', alpha=0.7)
for i, v in enumerate(pivot_mgmt['环比增长率']):
    if pd.notna(v):
        ax.text(v + 0.001 if v >= 0 else v - 0.001, i, f"{v:.2%}", va='center', ha='left' if v >= 0 else 'right',
                fontsize=10)
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "图3_管理费用明细环比.png"), dpi=300)
plt.close()

print(f"🎉 案例2执行完毕！所有结果已保存至：{OUT_DIR}")