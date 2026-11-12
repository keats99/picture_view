# -*- coding: utf-8 -*-
import pandas as pd
import matplotlib.pyplot as plt
import os
import warnings

warnings.filterwarnings('ignore')

# ==========================================
# 0. 环境与路径配置
# ==========================================
BASE_DIR = r"D:\Python_code\cda和数据可视化作业\商业数据分析平时作业"
DATA_DIR = os.path.join(BASE_DIR, "data", "chapter05_business_analysis")
SRC_DIR = os.path.join(BASE_DIR, "src", "chapter05_business_analysis")
OUT_DIR = os.path.join(BASE_DIR, "output", "chapter05_business_analysis", "case1_bank_dashboard")

os.makedirs(OUT_DIR, exist_ok=True)
os.makedirs(SRC_DIR, exist_ok=True)

file_path = os.path.join(DATA_DIR, "银行案例数据 - 学员用.xlsx")

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

print("="*50)
print("开始执行 第5章 案例1：银行理财产品BI看板")
print("="*50)

if not os.path.exists(file_path):
    raise FileNotFoundError(f"❌ 找不到数据文件：\n{file_path}")

# ==========================================
# 1. 读取数据与维度表关联
# ==========================================
# 读取各个维表
df_risk = pd.read_excel(file_path, sheet_name="风险偏好说明表")
df_category = pd.read_excel(file_path, sheet_name="品类说明表")
df_edu = pd.read_excel(file_path, sheet_name="学历说明表")
df_sales = pd.read_excel(file_path, sheet_name="销售数据")

# 清洗列名空格
for df in [df_risk, df_category, df_edu, df_sales]:
    df.columns = [c.strip() for c in df.columns]

# 将维表转换为字典进行映射（类似VLOOKUP）
dict_risk = dict(zip(df_risk['风险编号'], df_risk['风险说明']))
dict_category = dict(zip(df_category['品类编号'], df_category['品类名称']))
dict_edu = dict(zip(df_edu['学历编号'], df_edu['学历名称']))

# 应用映射
df_sales['风险说明'] = df_sales['风险编号'].map(dict_risk)
df_sales['品类名称'] = df_sales['品类编号'].map(dict_category)
df_sales['学历名称'] = df_sales['学历编号'].map(dict_edu)

# 类型转换防雷
df_sales['购买金额'] = pd.to_numeric(df_sales['购买金额'], errors='coerce')
df_sales = df_sales.dropna(subset=['购买金额'])

# ==========================================
# 2. 核心业务指标计算
# ==========================================
target_amount = 25000000  # 本月目标 2500 万
current_amount = df_sales['购买金额'].sum()
completion_rate = current_amount / target_amount

print(f"💰 当前销售额：{current_amount:,.2f} 元")
print(f"🎯 本月目标额：{target_amount:,.2f} 元")
print(f"📈 目标完成率：{completion_rate:.2%}")

# 维度汇总
risk_summary = df_sales.groupby('风险说明')['购买金额'].sum().reset_index()
category_summary = df_sales.groupby('品类名称')['购买金额'].sum().reset_index()
age_summary = df_sales.groupby('年龄')['购买金额'].sum().reset_index()
purpose_summary = df_sales.groupby('购买目的')['购买金额'].sum().reset_index()

# 导出 CSV
risk_summary.to_csv(os.path.join(OUT_DIR, "1_风险偏好销售额.csv"), index=False, encoding='gbk')
category_summary.to_csv(os.path.join(OUT_DIR, "2_品类销售额.csv"), index=False, encoding='gbk')
age_summary.to_csv(os.path.join(OUT_DIR, "3_年龄段销售额.csv"), index=False, encoding='gbk')
purpose_summary.to_csv(os.path.join(OUT_DIR, "4_购买目的销售额.csv"), index=False, encoding='gbk')

# ==========================================
# 3. 可视化图表
# ==========================================
print("🎨 开始绘制图表...")

# 图1：目标完成率（柱状图展示进度）
fig, ax = plt.subplots(figsize=(8, 5))
ax.bar(['已完成', '未完成'], [current_amount, max(0, target_amount - current_amount)], color=['#55A868', '#C44E52'])
ax.set_title(f'本月销售目标完成情况 (完成率: {completion_rate:.1%})', fontsize=14)
ax.set_ylabel('金额 (元)', fontsize=12)
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, loc: f"{x/10000:.0f}万"))
for i, v in enumerate([current_amount, max(0, target_amount - current_amount)]):
    ax.text(i, v + 500000, f"{v/10000:.1f}万", ha='center', fontsize=12)
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "图1_目标完成率.png"), dpi=300)
plt.close()

# 图2：风险偏好销售额 (饼图)
fig, ax = plt.subplots(figsize=(8, 6))
ax.pie(risk_summary['购买金额'], labels=risk_summary['风险说明'], autopct='%1.1f%%', startangle=90, colors=['#4C72B0', '#DD8452', '#55A868'])
ax.set_title('客户风险偏好分布', fontsize=14)
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "图2_风险偏好分布.png"), dpi=300)
plt.close()

# 图3：各品类销售额 (条形图)
fig, ax = plt.subplots(figsize=(10, 6))
category_summary = category_summary.sort_values(by='购买金额', ascending=True)
ax.barh(category_summary['品类名称'], category_summary['购买金额'], color='#4C72B0')
ax.set_title('各理财产品品类销售额', fontsize=14)
ax.set_xlabel('金额 (元)', fontsize=12)
ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, loc: f"{x/10000:.0f}万"))
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "图3_品类销售额.png"), dpi=300)
plt.close()

# 图4：各年龄段销售额 (柱状图)
fig, ax = plt.subplots(figsize=(8, 5))
ax.bar(age_summary['年龄'], age_summary['购买金额'], color='#DD8452', width=0.5)
ax.set_title('各年龄段销售额', fontsize=14)
ax.set_ylabel('金额 (元)', fontsize=12)
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, loc: f"{x/10000:.0f}万"))
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "图4_年龄段销售额.png"), dpi=300)
plt.close()

print(f"🎉 案例1执行完毕！文件已保存至：{OUT_DIR}")
print("="*50)
