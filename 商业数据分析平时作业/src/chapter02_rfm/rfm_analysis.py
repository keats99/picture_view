import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import os
import numpy as np

# ==========================================
# 0. 基础设置与路径定义
# ==========================================
# 解决图表中文显示问题
matplotlib.rcParams['font.sans-serif'] = ['SimHei']  # Windows用黑体
matplotlib.rcParams['axes.unicode_minus'] = False    # 正常显示负号

# 【重要】请确认这里的路径和你的电脑一致
ROOT_DIR = r'D:\Python_code\cda和数据可视化作业\商业数据分析平时作业'
DATA_DIR = os.path.join(ROOT_DIR, 'data', 'chapter02_rfm')
OUTPUT_DIR = os.path.join(ROOT_DIR, 'output', 'chapter02_rfm')

# 确保输出文件夹存在
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

print("正在读取Excel数据...")
file_path = os.path.join(DATA_DIR, '1-2RFM模型.xlsx')

# 读取指定Sheet
df = pd.read_excel(file_path, sheet_name='原始数据')

# ==========================================
# 1. 数据预处理
# ==========================================
# 把日期列转为时间格式
df['销售日期'] = pd.to_datetime(df['销售日期'])
# 把销售金额转为数值格式
df['销售金额'] = pd.to_numeric(df['销售金额'], errors='coerce')

# 设定一个观察的“当前时间”，通常设为数据中最后一次销售日期的后一天
current_date = df['销售日期'].max() + pd.Timedelta(days=1)
print(f"数据中的最后一次销售日期是：{df['销售日期'].max().date()}，我们将以此作为计算R的基准。")

# ==========================================
# 2. 计算 R、F、M 三大核心指标
# ==========================================
# 按用户编号分组计算
rfm = df.groupby('用户编号').agg({
    '销售日期': lambda x: (current_date - x.max()).days,  # R：最近一次购买距今的天数
    '流水号': 'nunique',                                  # F：消费次数（去重计算流水号）
    '销售金额': 'sum'                                      # M：累计消费金额
}).reset_index()

# 重命名列名方便看
rfm.columns = ['用户编号', 'R(最近购买天数)', 'F(消费频次)', 'M(消费金额)']

# ==========================================
# 3. 指标打分与客户分类 (基于业务背景的高低规则)
# ==========================================
# 我们用均值（或者中位数）来区分“高”和“低”。大于等于均值为“高”，否则为“低”。
r_mean = rfm['R(最近购买天数)'].mean()
f_mean = rfm['F(消费频次)'].mean()
m_mean = rfm['M(消费金额)'].mean()

# 注意：R是越小越好（最近买过），所以小于均值为“高”价值
rfm['R_Score'] = np.where(rfm['R(最近购买天数)'] <= r_mean, '高', '低')
rfm['F_Score'] = np.where(rfm['F(消费频次)'] >= f_mean, '高', '低')
rfm['M_Score'] = np.where(rfm['M(消费金额)'] >= m_mean, '高', '低')

# 定义一个函数，根据R、F、M的高低组合，映射出那8种客户类型
def classify_customer(row):
    r, f, m = row['R_Score'], row['F_Score'], row['M_Score']
    if r == '高' and f == '高' and m == '高': return '重要价值用户'
    elif r == '高' and f == '低' and m == '高': return '重要发展用户'
    elif r == '低' and f == '高' and m == '高': return '重要保持用户'
    elif r == '低' and f == '低' and m == '高': return '重要挽留用户'
    elif r == '高' and f == '高' and m == '低': return '一般价值用户'
    elif r == '高' and f == '低' and m == '低': return '一般发展用户'
    elif r == '低' and f == '高' and m == '低': return '一般保持用户'
    else: return '一般挽留用户'

# 应用这个分类函数
rfm['用户类别'] = rfm.apply(classify_customer, axis=1)

# 打乱一下顺序，挑前5行预览一下
print("\n--- RFM计算与分类结果预览 ---")
print(rfm[['用户编号', 'R(最近购买天数)', 'F(消费频次)', 'M(消费金额)', '用户类别']].head())

# ==========================================
# 4. 保存结果到 CSV
# ==========================================
csv_output_path = os.path.join(OUTPUT_DIR, 'RFM结果表.csv')
rfm.to_csv(csv_output_path, index=False, encoding='utf-8-sig') # utf-8-sig 防止Excel打开乱码
print(f"\n✅ 客户分类明细表已保存至：{csv_output_path}")

# ==========================================
# 5. 绘制客户分类分布图
# ==========================================
print("正在绘制用户类别分布图...")

# 统计每种用户类别的数量
category_counts = rfm['用户类别'].value_counts()

plt.figure(figsize=(10, 6))
# 按照数量从高到低排序并画柱状图
bars = plt.bar(category_counts.index, category_counts.values, color='#5B6BBF', alpha=0.8)

# 在柱子上标出具体数字
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval + 0.5, int(yval), ha='center', va='bottom')

plt.title('用户类别数量分布 (RFM模型)')
plt.xlabel('用户类别')
plt.ylabel('用户数量（人）')
plt.xticks(rotation=15) # 文字稍微倾斜一点防重叠
plt.grid(axis='y', linestyle='--', alpha=0.5)
plt.tight_layout()

# 保存图片
img_output_path = os.path.join(OUTPUT_DIR, 'rfm_customer_distribution.png')
plt.savefig(img_output_path)
print(f"✅ 图表已保存至：{img_output_path}")

plt.show()
print("🎉 第2章 RFM模型实验全部完成！")