# -*- coding: utf-8 -*-
import pandas as pd
import matplotlib.pyplot as plt
import os
import warnings
import glob

warnings.filterwarnings('ignore')

# ==========================================
# 0. 环境与路径配置 (已修改独立输出路径)
# ==========================================
BASE_DIR = r"D:\Python_code\cda和数据可视化作业\商业数据分析平时作业"
DATA_DIR = os.path.join(BASE_DIR, "data", "chapter03_framework")
SRC_DIR = os.path.join(BASE_DIR, "src", "chapter03_framework")
# 修改点：增加 case3_ecommerce_marketing 子文件夹
OUT_DIR = os.path.join(BASE_DIR, "output", "chapter03_framework", "case3_ecommerce_marketing")

os.makedirs(OUT_DIR, exist_ok=True)
os.makedirs(SRC_DIR, exist_ok=True)

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# ==========================================
# 1. 智能搜索数据文件
# ==========================================
if not os.path.exists(DATA_DIR):
    raise FileNotFoundError(f"❌ 找不到数据文件夹，请确认路径：\n{DATA_DIR}")

possible_files = glob.glob(os.path.join(DATA_DIR, "案例3*.xlsx"))

if not possible_files:
    files_in_dir = os.listdir(DATA_DIR)
    raise FileNotFoundError(f"❌ 在 {DATA_DIR} 中没有找到以 '案例3' 开头的 xlsx 文件！\n"
                            f"当前文件夹里的文件有：{files_in_dir}")

file_path = [f for f in possible_files if "原始" in f][0] if any("原始" in f for f in possible_files) else possible_files[0]
print(f"✅ 自动找到数据文件：{file_path}")

# ==========================================
# 2. 数据读取与清洗
# ==========================================
xls = pd.ExcelFile(file_path)
sheet_name = xls.sheet_names[0]
df = pd.read_excel(file_path, sheet_name=sheet_name)

df.columns = [c.strip() for c in df.columns]

df['年龄'] = pd.to_numeric(df['年龄'], errors='coerce')
df['数量'] = pd.to_numeric(df['数量'], errors='coerce')
df = df.dropna(subset=['年龄', '性别', '品类', '支付方式'])

bins = [17, 25, 35, 49, 100]
labels = ['18-25岁', '26-35岁', '36-49岁', '50岁以上']
df['客户年龄段'] = pd.cut(df['年龄'], bins=bins, labels=labels, right=True)

# ==========================================
# 3. 核心分析与导出
# ==========================================
# --- 步骤 1：购买客户的性别分布 ---
gender_counts = df['性别'].value_counts().reset_index()
gender_counts.columns = ['性别', '客户数']
gender_counts.to_csv(os.path.join(OUT_DIR, "1_性别分布.csv"), index=False, encoding='gbk')

# --- 步骤 2：女性消费客户的年龄段分布 ---
df_female = df[df['性别'] == 'Female']
age_counts = df_female['客户年龄段'].value_counts().reindex(labels).reset_index()
age_counts.columns = ['年龄段', '客户数']
age_counts.to_csv(os.path.join(OUT_DIR, "2_女性年龄段分布.csv"), index=False, encoding='gbk')

# --- 步骤 3：50岁以上的女性客户的消费品类分布 ---
df_50_female = df_female[df_female['客户年龄段'] == '50岁以上']
category_counts = df_50_female['品类'].value_counts().reset_index()
category_counts.columns = ['品类', '客户数']
category_counts.to_csv(os.path.join(OUT_DIR, "3_50岁以上女性品类分布.csv"), index=False, encoding='gbk')

# --- 步骤 4：50岁以上女性，服饰和护肤品消费人群的支付方式分布 ---
df_50_female_cloth_cosm = df_50_female[df_50_female['品类'].isin(['Clothing', 'Cosmetics'])]
pay_counts = df_50_female_cloth_cosm['支付方式'].value_counts().reset_index()
pay_counts.columns = ['支付方式', '客户数']
pay_counts.to_csv(os.path.join(OUT_DIR, "4_支付方式分布.csv"), index=False, encoding='gbk')

# ==========================================
# 4. 可视化制图
# ==========================================
# 图1：性别分布
fig, ax = plt.subplots(figsize=(8, 5))
ax.bar(gender_counts['性别'], gender_counts['客户数'], color=['#C44E52', '#4C72B0'], width=0.4)
for i, v in zip(gender_counts['性别'], gender_counts['客户数']):
    ax.text(i, v + 30, str(v), ha='center', va='bottom', fontsize=12)
ax.set_title('购买客户的性别分布', fontsize=14)
ax.set_ylabel('客户数', fontsize=12)
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "图1_性别分布.png"), dpi=300)
plt.close()

# 图2：女性年龄段分布
fig, ax = plt.subplots(figsize=(8, 5))
ax.bar(age_counts['年龄段'].astype(str), age_counts['客户数'], color='#55A868', width=0.5)
for i, v in enumerate(age_counts['客户数']):
    ax.text(i, v + 10, str(v), ha='center', va='bottom', fontsize=12)
ax.set_title('女性消费客户的年龄段分布', fontsize=14)
ax.set_ylabel('客户数', fontsize=12)
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "图2_女性年龄段分布.png"), dpi=300)
plt.close()

# 图3：50岁以上女性品类分布
fig, ax = plt.subplots(figsize=(10, 5))
category_counts = category_counts.sort_values(by='客户数', ascending=False)
ax.bar(category_counts['品类'], category_counts['客户数'], color='#DD8452', width=0.6)
for i, v in enumerate(category_counts['客户数']):
    ax.text(i, v + 5, str(v), ha='center', va='bottom', fontsize=10)
ax.set_title('50岁以上女性客户的消费品类分布', fontsize=14)
ax.set_ylabel('客户数', fontsize=12)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "图3_50岁以上女性品类分布.png"), dpi=300)
plt.close()

# 图4：支付方式分布
fig, ax = plt.subplots(figsize=(8, 5))
pay_counts = pay_counts.sort_values(by='客户数', ascending=False)
ax.bar(pay_counts['支付方式'], pay_counts['客户数'], color='#8172B3', width=0.5)
for i, v in enumerate(pay_counts['客户数']):
    ax.text(i, v + 5, str(v), ha='center', va='bottom', fontsize=12)
ax.set_title('50岁以上女性(服饰+护肤品)支付方式分布', fontsize=14)
ax.set_ylabel('客户数', fontsize=12)
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "图4_支付方式分布.png"), dpi=300)
plt.close()

print(f"🎉 案例3执行完毕！所有结果已保存至：{OUT_DIR}")