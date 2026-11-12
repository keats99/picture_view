# -*- coding: utf-8 -*-
import pandas as pd
import matplotlib.pyplot as plt
import os
import warnings

warnings.filterwarnings('ignore')

# ==========================================
# 0. 环境与路径配置 (已修改独立输出路径)
# ==========================================
BASE_DIR = r"D:\Python_code\cda和数据可视化作业\商业数据分析平时作业"
DATA_DIR = os.path.join(BASE_DIR, "data", "chapter03_framework")
SRC_DIR = os.path.join(BASE_DIR, "src", "chapter03_framework")
# 修改点：增加 case1_income_trend 子文件夹
OUT_DIR = os.path.join(BASE_DIR, "output", "chapter03_framework", "case1_income_trend")

os.makedirs(OUT_DIR, exist_ok=True)
os.makedirs(SRC_DIR, exist_ok=True)

file_path = os.path.join(DATA_DIR, "案例1：收入趋势分析原始数据.xlsx")

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# ==========================================
# 1. 数据读取与清洗
# ==========================================
if not os.path.exists(file_path):
    raise FileNotFoundError(f"❌ 找不到数据文件，请确认路径：\n{file_path}")

df = pd.read_excel(file_path, sheet_name="原始数据")

cols = df.columns.tolist()
col_year = [c for c in cols if '年份' in c][0]
col_month = [c for c in cols if '月份' in c][0]
col_prov = [c for c in cols if '省份' in c][0]
col_sales = [c for c in cols if '销售额' in c][0]

df = df.rename(columns={col_year: '年份', col_month: '月份', col_prov: '省份', col_sales: '销售额'})

df['年份'] = pd.to_numeric(df['年份'], errors='coerce')
df['月份'] = pd.to_numeric(df['月份'], errors='coerce')
df['销售额'] = pd.to_numeric(df['销售额'], errors='coerce')
df = df.dropna(subset=['年份', '月份', '销售额'])

df['年份'] = df['年份'].astype(int)
df['月份'] = df['月份'].astype(int)

# ==========================================
# 2. 核心分析逻辑
# ==========================================
# 步骤 1：年度销售趋势
yearly_sales = df.groupby('年份')['销售额'].sum().reset_index()
yearly_sales.to_csv(os.path.join(OUT_DIR, "1_年度销售趋势.csv"), index=False, encoding='gbk')

# 步骤 2：2020年月销售趋势
df_2020 = df[df['年份'] == 2020]
monthly_sales_2020 = df_2020.groupby('月份')['销售额'].sum().reset_index()
monthly_sales_2020.to_csv(os.path.join(OUT_DIR, "2_2020年月销售趋势.csv"), index=False, encoding='gbk')

# 步骤 3：2020年销售同比增长率趋势分析
df_2019 = df[df['年份'] == 2019]
monthly_sales_2019 = df_2019.groupby('月份')['销售额'].sum().reset_index()

yoy_monthly = pd.merge(monthly_sales_2019, monthly_sales_2020, on='月份', suffixes=('_2019', '_2020'))
yoy_monthly['同比增长率'] = (yoy_monthly['销售额_2020'] - yoy_monthly['销售额_2019']) / yoy_monthly['销售额_2019'].replace(0, pd.NA)
yoy_monthly.to_csv(os.path.join(OUT_DIR, "3_2020年月度同比.csv"), index=False, encoding='gbk')

worst_month = yoy_monthly.loc[yoy_monthly['同比增长率'].idxmin()]
worst_month_num = int(worst_month['月份'])

# 步骤 4：下钻分析 - 异常月份各省份同比
df_worst_month = df[df['月份'] == worst_month_num]
prov_pivot = df_worst_month.pivot_table(index='省份', columns='年份', values='销售额', aggfunc='sum').reset_index()
for y in [2019, 2020]:
    if y not in prov_pivot.columns:
        prov_pivot[y] = 0
prov_pivot = prov_pivot.fillna(0)
prov_pivot['同比增长率'] = (prov_pivot[2020] - prov_pivot[2019]) / prov_pivot[2019].replace(0, pd.NA)
prov_pivot = prov_pivot.sort_values(by='同比增长率', ascending=True)
prov_pivot.to_csv(os.path.join(OUT_DIR, f"4_{worst_month_num}月各省份同比.csv"), index=False, encoding='gbk')

worst_prov = prov_pivot[prov_pivot['同比增长率'].notna() & (prov_pivot[2019] > 0)].iloc[0]['省份']

# 步骤 5：下钻分析 - 异常省份全年同比
df_prov = df[df['省份'] == worst_prov]
prov_monthly_pivot = df_prov.pivot_table(index='月份', columns='年份', values='销售额', aggfunc='sum').reset_index()
prov_monthly_pivot.to_csv(os.path.join(OUT_DIR, f"5_{worst_prov}全年月度对比.csv"), index=False, encoding='gbk')

# ==========================================
# 3. 可视化制图
# ==========================================
# 图1：年度销售趋势
plt.figure(figsize=(8, 5))
plt.bar(yearly_sales['年份'].astype(str), yearly_sales['销售额'], color='#4C72B0', width=0.5)
for i, v in enumerate(yearly_sales['销售额']):
    plt.text(i, v + 50000, f"{v/10000:.1f}万", ha='center', va='bottom', fontsize=10)
plt.title('2017-2020年 年度销售额趋势', fontsize=14)
plt.xlabel('年份', fontsize=12)
plt.ylabel('销售额', fontsize=12)
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "图1_年度销售趋势.png"), dpi=300)
plt.close()

# 图2：2020年月度销售趋势
plt.figure(figsize=(10, 5))
plt.plot(monthly_sales_2020['月份'], monthly_sales_2020['销售额'], marker='o', color='#DD8452', linewidth=2)
plt.title('2020年 1-12月 销售额趋势', fontsize=14)
plt.xlabel('月份', fontsize=12)
plt.ylabel('销售额', fontsize=12)
plt.xticks(monthly_sales_2020['月份'])
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "图2_2020年月度趋势.png"), dpi=300)
plt.close()

# 图3：2020年各月同比增速
fig, ax1 = plt.subplots(figsize=(12, 6))
width = 0.35
ax1.bar(yoy_monthly['月份'] - width/2, yoy_monthly['销售额_2019'], width, label='2019年', color='#55A868', alpha=0.8)
ax1.bar(yoy_monthly['月份'] + width/2, yoy_monthly['销售额_2020'], width, label='2020年', color='#4C72B0', alpha=0.8)
ax1.set_xlabel('月份', fontsize=12)
ax1.set_ylabel('销售额', fontsize=12)
ax1.set_xticks(yoy_monthly['月份'])

ax2 = ax1.twinx()
ax2.plot(yoy_monthly['月份'], yoy_monthly['同比增长率'], color='red', marker='o', label='同比增长率')
ax2.set_ylabel('同比增长率', color='red', fontsize=12)
ax2.tick_params(axis='y', labelcolor='red')
ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:.0%}".format(x)))

ax1.axvspan(worst_month_num - 0.5, worst_month_num + 0.5, color='red', alpha=0.1)
fig.suptitle('2020年 月度销售额及同比增速趋势', fontsize=16)
fig.legend(loc="upper left", bbox_to_anchor=(0.1, 0.9))
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "图3_2020年月度同比.png"), dpi=300)
plt.close()

# 图4：异常月份各省份同比 (已修复报错问题)
fig, ax = plt.subplots(figsize=(10, 10))
prov_plot = prov_pivot.dropna(subset=['同比增长率']).head(15)
colors = ['#C44E52' if x < 0 else '#55A868' for x in prov_plot['同比增长率']]
ax.barh(prov_plot['省份'], prov_plot['同比增长率'], color=colors)
ax.set_title(f'2020年{worst_month_num}月 各省份同比增长率 (Top15 异常省份)', fontsize=14)
ax.set_xlabel('同比增长率', fontsize=12)
ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:.0%}".format(x)))
ax.grid(axis='x', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "图4_异常月份各省份同比.png"), dpi=300)
plt.close()

# 图5：异常省份全年月度对比
plt.figure(figsize=(10, 5))
if 2019 in prov_monthly_pivot.columns:
    plt.plot(prov_monthly_pivot['月份'], prov_monthly_pivot[2019], marker='o', label='2019年', color='#55A868')
if 2020 in prov_monthly_pivot.columns:
    plt.plot(prov_monthly_pivot['月份'], prov_monthly_pivot[2020], marker='s', label='2020年', color='#4C72B0')
plt.title(f'{worst_prov} 2019 vs 2020 月度销售额对比', fontsize=14)
plt.xlabel('月份', fontsize=12)
plt.ylabel('销售额', fontsize=12)
plt.xticks(prov_monthly_pivot['月份'])
plt.legend()
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, f"图5_{worst_prov}月度对比.png"), dpi=300)
plt.close()

print(f"🎉 案例1执行完毕！所有结果已保存至：{OUT_DIR}")