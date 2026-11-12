# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import warnings
import matplotlib.font_manager as fm
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from statsmodels.tsa.seasonal import seasonal_decompose

warnings.filterwarnings('ignore')

# ==========================================
# 0. 环境与路径配置 (彻底解决中文乱码)
# ==========================================
BASE_DIR = r"D:\Python_code\cda和数据可视化作业\商业数据分析平时作业"
DATA_DIR = os.path.join(BASE_DIR, "data", "chapter10_time_series")
SRC_DIR = os.path.join(BASE_DIR, "src", "chapter10_time_series")
OUT_DIR = os.path.join(BASE_DIR, "output", "chapter10_time_series")

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(OUT_DIR, exist_ok=True)
os.makedirs(SRC_DIR, exist_ok=True)

# 强制加载微软雅黑，解决图表中文乱码
font_path = r"C:\Windows\Fonts\msyh.ttc"
if os.path.exists(font_path):
    my_font = fm.FontProperties(fname=font_path)
else:
    my_font = fm.FontProperties(family='SimHei')
plt.rcParams['axes.unicode_minus'] = False

print("="*50)
print("开始执行 第10章：时间序列预测与效应分解")
print("="*50)

# ==========================================
# 1. 数据读取与暴力清洗
# ==========================================
file_path = os.path.join(DATA_DIR, "AirPassengers.csv")
if not os.path.exists(file_path):
    raise FileNotFoundError(f"❌ 找不到文件：\n{file_path}")

# 暴力读取，忽略表头格式问题
df = pd.read_csv(file_path)
# 直接提取前两列，强制重命名，不跟它猜列名了
df = df.iloc[:, :2]
df.columns = ['Month', 'Passengers']

# 转换日期和数值
df['Month'] = pd.to_datetime(df['Month'], errors='coerce')
df['Passengers'] = pd.to_numeric(df['Passengers'], errors='coerce')
df = df.dropna()

# 将月份设为索引，并按时间排序
df.set_index('Month', inplace=True)
df = df.sort_index()
df = df.asfreq('MS')  # 确保频率为月初

# 增加一列取对数 (教材参考图2)
df['ln_Passengers'] = np.log(df['Passengers'])

print(f"✅ 数据加载成功，共 {len(df)} 个月份数据")

# ==========================================
# 2. 核心算法：Holt-Winters 预测
# ==========================================
print("⏳ 正在进行 Holt-Winters 预测...")
# 预测未来 24 个月
forecast_steps = 24

# 原始数据预测 (乘法模型)
model_orig = ExponentialSmoothing(
    df['Passengers'],
    seasonal_periods=12,
    trend='add',
    seasonal='mul',
    initialization_method="estimated"
).fit()
forecast_orig = model_orig.forecast(forecast_steps)
# 获取预测置信区间
pred_orig = model_orig.predict(start=0, end=len(df)+forecast_steps-1)
resid_std_orig = np.std(model_orig.resid)
conf_int_orig = 1.96 * resid_std_orig # 95% 置信区间

# 取对数数据预测 (加法模型)
model_ln = ExponentialSmoothing(
    df['ln_Passengers'],
    seasonal_periods=12,
    trend='add',
    seasonal='add',
    initialization_method="estimated"
).fit()
forecast_ln = model_ln.forecast(forecast_steps)
pred_ln = model_ln.predict(start=0, end=len(df)+forecast_steps-1)
resid_std_ln = np.std(model_ln.resid)
conf_int_ln = 1.96 * resid_std_ln

# 保存预测数据
pred_df = pd.DataFrame({
    '原始数据_预测': pred_orig,
    '对数数据_预测': pred_ln
})
pred_df.to_csv(os.path.join(OUT_DIR, "1_未来预测结果.csv"), encoding='utf-8-sig')

# ==========================================
# 3. 时间序列效应分解 (经典四图)
# ==========================================
print("⏳ 正在进行时间序列乘法分解...")
decomposition = seasonal_decompose(df['Passengers'], model='multiplicative', period=12)
trend = decomposition.trend
seasonal = decomposition.seasonal
residual = decomposition.resid

decomp_df = pd.DataFrame({
    'Original': df['Passengers'],
    'Trend': trend,
    'Seasonality': seasonal,
    'Residual': residual
})
decomp_df.to_csv(os.path.join(OUT_DIR, "2_时间序列效应分解结果.csv"), encoding='utf-8-sig')

# ==========================================
# 4. 可视化制图 (完全复刻 PowerBI 的效果)
# ==========================================
print("🎨 开始绘制图表...")

# 图1：原始数据的时序图 + 预测区间
plt.figure(figsize=(12, 6))
plt.plot(df.index, df['Passengers'], color='#0078D7', linewidth=2, label='实际值')
plt.plot(pred_orig.index, pred_orig, color='black', linestyle='--', linewidth=1.5, label='预测趋势')
# 画预测区间的阴影 (仅预测部分)
plt.fill_between(
    pred_orig.index,
    pred_orig - conf_int_orig,
    pred_orig + conf_int_orig,
    color='gray', alpha=0.3, label='95%置信区间'
)
plt.title('AIR 的总和 (按 DATE) - 原始数据预测', fontproperties=my_font, fontsize=16)
plt.xlabel('年份', fontproperties=my_font, fontsize=12)
plt.ylabel('乘客数量', fontproperties=my_font, fontsize=12)
plt.xticks(fontproperties=my_font)
plt.yticks(fontproperties=my_font)
plt.legend(prop=my_font)
plt.grid(True, linestyle=':', alpha=0.7)
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "图1_原始数据预测.png"), dpi=300)
plt.close()

# 图2：取对数后的时序图 + 预测区间
plt.figure(figsize=(12, 6))
plt.plot(df.index, df['ln_Passengers'], color='#0078D7', linewidth=2, label='实际值(Log)')
plt.plot(pred_ln.index, pred_ln, color='black', linestyle='--', linewidth=1.5, label='预测趋势')
plt.fill_between(
    pred_ln.index,
    pred_ln - conf_int_ln,
    pred_ln + conf_int_ln,
    color='gray', alpha=0.3, label='95%置信区间'
)
plt.title('ln_AIR 的总和 (按 年 和 月份) - 取对数预测', fontproperties=my_font, fontsize=16)
plt.xlabel('年份', fontproperties=my_font, fontsize=12)
plt.ylabel('乘客数量 (取对数)', fontproperties=my_font, fontsize=12)
plt.xticks(fontproperties=my_font)
plt.yticks(fontproperties=my_font)
plt.legend(prop=my_font)
plt.grid(True, linestyle=':', alpha=0.7)
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "图2_对数数据预测.png"), dpi=300)
plt.close()

# 图3：综合效应分解图
fig, axes = plt.subplots(4, 1, figsize=(12, 12), sharex=True)

axes[0].plot(df['Passengers'], color='#0078D7', linewidth=2)
axes[0].set_title('原始数据 (Original)', fontproperties=my_font, fontsize=14)
axes[0].grid(True, linestyle=':', alpha=0.6)

axes[1].plot(trend, color='#DD8452', linewidth=2)
axes[1].set_title('趋势项 (Trend)', fontproperties=my_font, fontsize=14)
axes[1].grid(True, linestyle=':', alpha=0.6)

axes[2].plot(seasonal, color='#55A868', linewidth=2)
axes[2].set_title('季节项 (Seasonality)', fontproperties=my_font, fontsize=14)
axes[2].grid(True, linestyle=':', alpha=0.6)

axes[3].scatter(residual.index, residual, color='#C44E52', s=15)
axes[3].axhline(1, color='black', linestyle='--', linewidth=1)
axes[3].set_title('残差项 (Residual)', fontproperties=my_font, fontsize=14)
axes[3].grid(True, linestyle=':', alpha=0.6)

# 给所有子图的坐标轴打上中文字体
for ax in axes:
    for label in ax.get_xticklabels() + ax.get_yticklabels():
        label.set_fontproperties(my_font)

plt.suptitle('时间序列乘法分解 (Multiplicative Decomposition)', fontproperties=my_font, fontsize=18)
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "图3_时间序列分解.png"), dpi=300, bbox_inches='tight')
plt.close()

print(f"🎉 第10章执行完毕！图表和预测 CSV 已保存至：\n{OUT_DIR}")
print("="*50)