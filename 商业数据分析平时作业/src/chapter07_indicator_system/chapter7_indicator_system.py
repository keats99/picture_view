# -*- coding: utf-8 -*-
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
import os
import warnings
import matplotlib.font_manager as fm  # 新增：专门处理字体

warnings.filterwarnings('ignore')

# ==========================================
# 0. 环境与路径配置
# ==========================================
BASE_DIR = r"D:\Python_code\cda和数据可视化作业\商业数据分析平时作业"
DATA_DIR = os.path.join(BASE_DIR, "data", "chapter07_indicator_system")
SRC_DIR = os.path.join(BASE_DIR, "src", "chapter07_indicator_system")
OUT_DIR = os.path.join(BASE_DIR, "output", "chapter07_indicator_system")

os.makedirs(OUT_DIR, exist_ok=True)
os.makedirs(SRC_DIR, exist_ok=True)

file_path = os.path.join(DATA_DIR, "1、指标体系设计模板.xlsx")

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 显式加载 Windows 系统自带的黑体文件（终极防乱码）
try:
    font_path = r"C:\Windows\Fonts\simhei.ttf"
    my_font = fm.FontProperties(fname=font_path)
except:
    my_font = fm.FontProperties(family='SimHei') # 如果找不到路径，尝试按名字加载

print("="*50)
print("开始执行 第7章：指标体系设计")
print("="*50)

if not os.path.exists(file_path):
    raise FileNotFoundError(f"❌ 找不到数据文件，请确认路径：\n{file_path}")

# ==========================================
# 1. 读取 Step2 (指标字典) 并进行数据清洗
# ==========================================
df_step2 = pd.read_excel(file_path, sheet_name="Step2", header=1)

# 自动识别并重命名第一列
cols = df_step2.columns.tolist()
cols[0] = '指标层级'
df_step2.columns = cols
df_step2.columns = [str(c).strip() for c in df_step2.columns]

# 清洗第一列（前向填充）和空值
df_step2['指标层级'] = df_step2['指标层级'].ffill()
df_step2 = df_step2.fillna("")

step2_out_path = os.path.join(OUT_DIR, "Step2_清洗后的指标字典.csv")
df_step2.to_csv(step2_out_path, index=False, encoding='gbk')
print(f"✅ Step2 指标字典已清洗完成，共包含 {len(df_step2)} 个指标。")

# ==========================================
# 2. 生成 Step1 (业务分析框架)
# ==========================================
step1_data = [
    {
        "组名": "第1组",
        "业务场景描述": "金融信贷APP的贷款转化流程",
        "核心目标": "提升贷款放款金额",
        "制定策略": "提高各环节转化率",
        "指标拆分": "注册->进件->审核->放款->复贷",
        "明确口径": "以成功放款金额及漏斗各节点人数为准",
        "明确分析维度": "新老客、渠道、时间"
    }
]
df_step1 = pd.DataFrame(step1_data)
step1_out_path = os.path.join(OUT_DIR, "Step1_业务分析框架.csv")
df_step1.to_csv(step1_out_path, index=False, encoding='gbk')
print("✅ Step1 业务分析框架已生成。")

# ==========================================
# 3. 可视化：绘制金融贷款漏斗指标树状图
# ==========================================
print("🎨 开始绘制金融贷款指标体系树状图...")

G = nx.DiGraph()

# 构建节点和边的关系
G.add_edge("核心目标:\n提升放款金额", "一级指标:\n注册用户数")
G.add_edge("核心目标:\n提升放款金额", "一级指标:\n进件用户数")

G.add_edge("一级指标:\n注册用户数", "二级指标:\n30天内新客\n进件转化率")
G.add_edge("二级指标:\n30天内新客\n进件转化率", "一级指标:\n进件用户数")
G.add_edge("一级指标:\n进件用户数", "其他指标:\n审核通过用户数")
G.add_edge("其他指标:\n审核通过用户数", "其他指标:\n放款用户数")
G.add_edge("其他指标:\n放款用户数", "其他指标:\n放款金额")

G.add_edge("一级指标:\n进件用户数", "其他指标:\n审核通过率")
G.add_edge("一级指标:\n进件用户数", "其他指标:\n机器审核\n通过率")
G.add_edge("一级指标:\n进件用户数", "其他指标:\n人工审核\n通过率")
G.add_edge("其他指标:\n放款用户数", "其他指标:\n放款件均")
G.add_edge("其他指标:\n放款用户数", "其他指标:\n30天内\n复贷转化率")

# 绘制图形设置
fig, ax = plt.subplots(figsize=(16, 12))

# 手动定义坐标 (调整了 Y 轴间距，防止重叠)
pos = {}
pos["核心目标:\n提升放款金额"] = (0.5, 1.0)

pos["一级指标:\n注册用户数"] = (0.2, 0.8)
pos["一级指标:\n进件用户数"] = (0.6, 0.8)

pos["二级指标:\n30天内新客\n进件转化率"] = (0.1, 0.55)
pos["其他指标:\n审核通过率"] = (0.4, 0.55)
pos["其他指标:\n机器审核\n通过率"] = (0.6, 0.55)
pos["其他指标:\n人工审核\n通过率"] = (0.8, 0.55)

pos["其他指标:\n审核通过用户数"] = (0.6, 0.35)

pos["其他指标:\n放款件均"] = (0.3, 0.15)
pos["其他指标:\n放款用户数"] = (0.6, 0.15)
pos["其他指标:\n30天内\n复贷转化率"] = (0.9, 0.15)

pos["其他指标:\n放款金额"] = (0.6, -0.05)

# 设置节点颜色
node_colors = []
for node in G.nodes():
    if "核心目标" in node:
        node_colors.append('#C44E52')  # 红色
    elif "一级指标" in node:
        node_colors.append('#DD8452')  # 橙色
    elif "二级指标" in node:
        node_colors.append('#4C72B0')  # 蓝色
    else:
        node_colors.append('#55A868')  # 绿色

# 1. 先画节点和边 (关闭 nx 自带的 labels)
nx.draw_networkx_nodes(G, pos, node_size=5500, node_color=node_colors, alpha=0.9, ax=ax)
nx.draw_networkx_edges(G, pos, edge_color='gray', arrows=True, arrowstyle='-|>', arrowsize=25, width=2, ax=ax)

# 2. 手动绘制文字，彻底解决中文乱码报错问题
for node, (x, y) in pos.items():
    ax.text(x, y, node,
            fontproperties=my_font,
            fontsize=11,
            ha='center', va='center',
            color='white', fontweight='bold', zorder=10)

ax.set_title("金融信贷指标拆解漏斗图", fontproperties=my_font, fontsize=20, fontweight='bold', pad=20)
ax.axis('off')
plt.tight_layout()

# 保存图片
tree_img_path = os.path.join(OUT_DIR, "图1_金融信贷指标拆解图.png")
plt.savefig(tree_img_path, dpi=300, bbox_inches='tight', facecolor='#F0F0F0')
plt.close()

# ==========================================
# 4. 打印预览
# ==========================================
print("\n📊 核心指标预览 (前5个):")
if '指标名称（KPI)' in df_step2.columns and '计算规则' in df_step2.columns:
    print(df_step2[['指标层级', '指标名称（KPI)', '计算规则', '指标类型']].head(5).to_string(index=False))
else:
    print(df_step2.head(5))

print(f"\n🎉 执行完毕！所有文件已保存至：\n{OUT_DIR}")
print("="*50)