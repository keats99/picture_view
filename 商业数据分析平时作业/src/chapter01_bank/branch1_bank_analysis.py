import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import os

# ==========================================
# 0. 基础设置与路径定义
# ==========================================
# 解决图表中文显示为方块的问题
matplotlib.rcParams['font.sans-serif'] = ['SimHei']  # Windows用黑体
matplotlib.rcParams['axes.unicode_minus'] = False    # 正常显示负号

# 【非常重要】请确保这里的路径和你的电脑完全一致！
ROOT_DIR = r'D:\Python_code\cda和数据可视化作业\商业数据分析平时作业'
DATA_DIR = os.path.join(ROOT_DIR, 'data', 'chapter01_bank')
OUTPUT_DIR = os.path.join(ROOT_DIR, 'output', 'chapter01_bank')

# 确保输出文件夹存在
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# ==========================================
# 1. 读取数据 (加上 encoding='gbk')
# ==========================================
print("正在读取数据...")
clients = pd.read_csv(os.path.join(DATA_DIR, 'clients.csv'), encoding='gbk')
trans = pd.read_csv(os.path.join(DATA_DIR, 'trans.csv'), encoding='gbk', low_memory=False)
card = pd.read_csv(os.path.join(DATA_DIR, 'card.csv'), encoding='gbk')
disp = pd.read_csv(os.path.join(DATA_DIR, 'disp.csv'), encoding='gbk')
print("数据读取成功！")

# ==========================================
# 2. 数据合并（关系模型）
# ==========================================
print("正在合并数据表...")
# 图1：card + disp + clients
df_card = pd.merge(card, disp, on='disp_id', how='inner')
df_card = pd.merge(df_card, clients, on='client_id', how='inner')

# 图2：trans + disp + clients
df_trans = pd.merge(trans, disp, on='account_id', how='inner')
df_trans = pd.merge(df_trans, clients, on='client_id', how='inner')
print("数据合并成功！")

# ==========================================
# 3. 画第一张图：sex的计数(按type和sex)
# ==========================================
print("正在绘制图1：卡类型与性别分布...")

# 安全映射性别
df_card['sex_str'] = df_card['sex'].astype(str).str.strip()
sex_map = {'1': '男', '2': '女', '1.0': '男', '2.0': '女', 'M': '男', 'F': '女'}
df_card['sex_cn'] = df_card['sex_str'].map(sex_map).fillna(df_card['sex_str'])

# 安全映射卡类型 (注意：合并后 type 变成了 type_x)
df_card['type_str'] = df_card['type_x'].astype(str).str.strip().str.lower()
type_map = {'classic': '普通卡', 'junior': '青年卡', 'gold': '金卡'}
df_card['type_cn'] = df_card['type_str'].map(type_map).fillna(df_card['type_str'])

# 按类型和性别分组计数
pivot_card = df_card.groupby(['type_cn', 'sex_cn']).size().unstack(fill_value=0)
print("\n--- 图1 数据预览 ---")
print(pivot_card)
print("--------------------\n")

# 开始画图1
plt.figure(figsize=(10, 6))
colors = ['#1FA3FF', '#001F8E'] if len(pivot_card.columns) <= 2 else None
pivot_card.plot(kind='bar', stacked=True, color=colors, ax=plt.gca())

plt.title('sex的计数(按type和sex)')
plt.xlabel('type')
plt.ylabel('sex的计数')
plt.xticks(rotation=0)
plt.legend(title='sex', loc='upper left')
plt.tight_layout()

# 保存图1
save_path1 = os.path.join(OUTPUT_DIR, 'batch1_chart1_card_sex.png')
plt.savefig(save_path1)
print(f"✅ 图1已保存至: {save_path1}")
plt.show()
plt.close() # 关闭画板，释放内存

# ==========================================
# 4. 画第二张图：amount的总和(按年和sex)
# ==========================================
print("正在绘制图2：年度交易金额趋势...")

# 4.1 强力清洗日期：先转字符串，再用 pandas 自动嗅探并转换格式 (兼容 930101 或 19930101 或 93-01-01)
df_trans['date_str'] = df_trans['date'].astype(str).str.strip()
# 为了防止是类似 '930101.0' 这种浮点字符串，去掉 .0
df_trans['date_str'] = df_trans['date_str'].str.replace(r'\.0$', '', regex=True)
df_trans['date_clean'] = pd.to_datetime(df_trans['date_str'], format='mixed', errors='coerce')
# 过滤掉无法解析的日期
df_trans = df_trans.dropna(subset=['date_clean'])
df_trans['year'] = df_trans['date_clean'].dt.year

# 4.2 强力清洗金额：强制转为数字
df_trans['amount'] = pd.to_numeric(df_trans['amount'], errors='coerce')
df_trans = df_trans.dropna(subset=['amount'])

# 4.3 映射性别
df_trans['sex_str'] = df_trans['sex'].astype(str).str.strip()
df_trans['sex_cn'] = df_trans['sex_str'].map(sex_map).fillna(df_trans['sex_str'])

# 4.4 分组求和并换算成百万
pivot_trans = df_trans.groupby(['year', 'sex_cn'])['amount'].sum().unstack(fill_value=0)
pivot_trans = pivot_trans / 1000000

print("\n--- 图2 数据预览 (百万) ---")
print(pivot_trans)
print("---------------------------\n")

# 开始画图2 (堆叠面积图)
plt.figure(figsize=(12, 7))
years = pivot_trans.index
male_amount = pivot_trans.get('男', pd.Series(0, index=years))
female_amount = pivot_trans.get('女', pd.Series(0, index=years))

plt.stackplot(years, male_amount, female_amount, labels=['男', '女'], colors=['#7ECEF4', '#5B6BBF'], alpha=0.9)
# 描边线让图更清晰
plt.plot(years, male_amount, color='#1FA3FF', linewidth=2)
plt.plot(years, male_amount + female_amount, color='#001F8E', linewidth=2)

plt.title('amount的总和(按年和sex)')
plt.xlabel('年')
plt.ylabel('amount的总和')
plt.yticks(plt.yticks()[0], [f'{int(x)} 百万' for x in plt.yticks()[0]])
plt.legend(title='sex', loc='upper left')
plt.grid(axis='y', linestyle='--', alpha=0.5)
plt.tight_layout()

# 保存图2
save_path2 = os.path.join(OUTPUT_DIR, 'batch1_chart2_year_amount.png')
plt.savefig(save_path2)
print(f"✅ 图2已保存至: {save_path2}")
plt.show()

print("🎉 全部完成！请去 output/chapter01_bank 文件夹查看生成的图片。")