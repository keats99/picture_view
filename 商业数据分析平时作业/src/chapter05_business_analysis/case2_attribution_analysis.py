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
OUT_DIR = os.path.join(BASE_DIR, "output", "chapter05_business_analysis", "case2_attribution")

os.makedirs(OUT_DIR, exist_ok=True)
os.makedirs(SRC_DIR, exist_ok=True)

file_path = os.path.join(DATA_DIR, "归因分析数据.xlsx")

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

print("=" * 50)
print("开始执行 第5章 案例2：贷款申请归因分析")
print("=" * 50)

if not os.path.exists(file_path):
    raise FileNotFoundError(f"❌ 找不到数据文件：\n{file_path}")

# ==========================================
# 1. 数据读取与清洗
# ==========================================
df = pd.read_excel(file_path, sheet_name="贷款申请表")
df.columns = [c.strip() for c in df.columns]

# 处理日期字段
df['申请日期'] = pd.to_datetime(df['申请日期'], errors='coerce')
df = df.dropna(subset=['申请日期'])

# 提取 年月 字段 (格式: 2021年05月)
df['申请年月'] = df['申请日期'].dt.strftime('%Y年%m月')

# ==========================================
# 2. 核心业务计算
# ==========================================
# 2.1 贷款申请量变化趋势
monthly_trend = df.groupby('申请年月').size().reset_index(name='贷款申请量')
monthly_trend['环比变化率'] = monthly_trend['贷款申请量'].pct_change()
monthly_trend.to_csv(os.path.join(OUT_DIR, "1_贷款申请趋势.csv"), index=False, encoding='gbk')

# 2.2 渠道构成情况（透视表）
channel_pivot = pd.pivot_table(df, index='申请年月', columns='申请渠道', values='申请书编号（主键）', aggfunc='count',
                               fill_value=0)
channel_pivot['总计'] = channel_pivot.sum(axis=1)
channel_pivot.reset_index().to_csv(os.path.join(OUT_DIR, "2_各渠道申请量.csv"), index=False, encoding='gbk')

# 2.3 归因分析 (对比4月和5月)
# 获取指定的两个月
month_prev = '2021年04月'
month_curr = '2021年05月'

if month_prev in channel_pivot.index and month_curr in channel_pivot.index:
    row_prev = channel_pivot.loc[month_prev]
    row_curr = channel_pivot.loc[month_curr]

    total_diff = row_curr['总计'] - row_prev['总计']

    # 计算各渠道差额及贡献度
    attribution = pd.DataFrame({
        '4月申请量': row_prev.drop('总计'),
        '5月申请量': row_curr.drop('总计')
    })
    attribution['差额'] = attribution['5月申请量'] - attribution['4月申请量']
    # 贡献度 = 渠道差额 / 总差额 (注意总差额是负数，负负得正)
    attribution['贡献度'] = attribution['差额'] / total_diff

    attribution = attribution.reset_index()
    attribution.to_csv(os.path.join(OUT_DIR, "3_渠道归因分析.csv"), index=False, encoding='gbk')
    print(f"\n📊 {month_curr} 相比 {month_prev} 总变化量：{total_diff} 笔")
    print(attribution[['申请渠道', '差额', '贡献度']].to_string(index=False))

# ==========================================
# 3. 可视化图表
# ==========================================
print("\n🎨 开始绘制图表...")

# 图1：贷款申请量趋势 (折线图)
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(monthly_trend['申请年月'], monthly_trend['贷款申请量'], marker='o', color='#4C72B0', linewidth=2)
for i, v in enumerate(monthly_trend['贷款申请量']):
    ax.text(i, v + 5, str(v), ha='center', fontsize=10)
ax.set_title('贷款申请量月度趋势', fontsize=14)
ax.set_ylabel('申请量 (笔)', fontsize=12)
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "图1_贷款申请趋势.png"), dpi=300)
plt.close()

# 图2：各渠道申请量分布 (堆叠柱状图)
fig, ax = plt.subplots(figsize=(10, 6))
channel_pivot.drop(columns=['总计']).plot(kind='bar', stacked=True, ax=ax, color=['#4C72B0', '#DD8452', '#55A868'])
ax.set_title('各渠道贷款申请量构成', fontsize=14)
ax.set_ylabel('申请量 (笔)', fontsize=12)
ax.set_xlabel('申请年月', fontsize=12)
plt.xticks(rotation=45)
plt.legend(title='申请渠道')
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "图2_渠道构成图.png"), dpi=300)
plt.close()

# 图3：渠道归因分析 (柱状图)
if 'attribution' in locals():
    fig, ax = plt.subplots(figsize=(8, 5))
    colors = ['#C44E52' if x < 0 else '#55A868' for x in attribution['差额']]
    bars = ax.bar(attribution['申请渠道'], attribution['差额'], color=colors)

    for bar, rate in zip(bars, attribution['贡献度']):
        yval = bar.get_height()
        # 标出具体差额和贡献度
        ax.text(bar.get_x() + bar.get_width() / 2, yval + (1 if yval > 0 else -3),
                f"{int(yval)}笔\n({rate:.1%})", ha='center', va='bottom' if yval > 0 else 'top', fontsize=11)

    ax.set_title(f'{month_curr} 相比 {month_prev} 各渠道变化与贡献度', fontsize=14)
    ax.set_ylabel('差额 (笔)', fontsize=12)
    ax.axhline(0, color='black', linewidth=1)
    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, "图3_渠道归因贡献.png"), dpi=300)
    plt.close()

print(f"🎉 案例2执行完毕！文件已保存至：{OUT_DIR}")
print("=" * 50)