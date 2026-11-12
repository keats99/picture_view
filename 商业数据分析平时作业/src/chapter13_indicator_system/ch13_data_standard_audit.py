# -*- coding: utf-8 -*-
r"""
第13章 指标体系管理 —— 数据标准自动化质检与指标树构建
运行环境：Windows + PyCharm，项目根目录 D:\Python_code\cda和数据可视化作业\商业数据分析平时作业
依赖：pandas, numpy, matplotlib, networkx, openpyxl
"""

import os
import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# ==================== 0. 路径与字体 ====================
BASE_DIR = r"D:\Python_code\cda和数据可视化作业\商业数据分析平时作业"
DATA_DIR = os.path.join(BASE_DIR, "data", "chapter13_indicator_system")
OUT_DIR = os.path.join(BASE_DIR, "output", "chapter13_indicator_system")
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(OUT_DIR, exist_ok=True)

FILE_BASE_STD = os.path.join(DATA_DIR, "1、基础数据标准编制模板.xlsx")
FILE_METRIC_STD = os.path.join(DATA_DIR, "2、指标数据标准编制模板.xlsx")

FONT_PATH = r"C:\Windows\Fonts\msyh.ttc"
my_font = fm.FontProperties(fname=FONT_PATH)
plt.rcParams["font.sans-serif"] = ["Microsoft YaHei"]
plt.rcParams["axes.unicode_minus"] = False


# ==================== 1. 读取并解析“基础数据标准” ====================
def audit_base_standard():
    print("[Step 1] 读取并质检：基础数据标准（客户为例）...")
    if not os.path.exists(FILE_BASE_STD):
        print(f"[警告] 找不到文件：{FILE_BASE_STD}")
        return None

    try:
        # 表头在第2行(index=1)，前两列是合并的类别，跳过全空列
        df = pd.read_excel(FILE_BASE_STD, sheet_name="客户主题为例", header=1)
        df = df.dropna(how='all')  # 删掉全空行

        # 处理合并表头产生的 Unnamed 列，用前一列填充
        df.columns = [str(c).strip() for c in df.columns]

        # 自动识别列名
        col_id = [c for c in df.columns if '标准编号' in c][0]
        col_name = [c for c in df.columns if '标准中文名称' in c][0]
        col_type = [c for c in df.columns if '标准类型' in c][0]
        col_len = [c for c in df.columns if '长度' in c][0]
        col_sys = [c for c in df.columns if '现有应用业务系统' in c][0]

        # 提取核心质检字段
        audit_df = df[[col_id, col_name, col_type, col_len, col_sys]].copy()
        audit_df.columns = ['标准编号', '标准中文名称', '标准类型', '长度', '应用系统']

        # 剔除说明行，只保留真正的数据行
        audit_df = audit_df.dropna(subset=['标准编号'])

        # --- 质检逻辑 ---
        # 1. 检查编号是否为空
        # 2. 检查长度是否缺失或不是数字
        def check_len(x):
            try:
                val = str(x).strip()
                if val == '/' or val == 'nan': return '未定义'
                int(val)
                return '合规'
            except:
                return '不合规'

        audit_df['长度质检'] = audit_df['长度'].apply(check_len)
        audit_df['编号质检'] = audit_df['标准编号'].apply(lambda x: '缺失' if pd.isna(x) else '合规')

        out_csv = os.path.join(OUT_DIR, "基础数据标准_质检报告.csv")
        audit_df.to_csv(out_csv, index=False, encoding="utf-8-sig")
        print(f"[OK] 基础数据标准质检完成，结果已保存：{out_csv}")
        print(f"     发现有效标准 {len(audit_df)} 条。")
        return audit_df

    except Exception as e:
        print(f"[错误] 读取基础数据标准失败：{e}")
        return None


# ==================== 2. 读取并解析“指标数据标准” ====================
def audit_metric_standard():
    print("\n[Step 2] 读取并质检：指标数据标准...")
    if not os.path.exists(FILE_METRIC_STD):
        print(f"[警告] 找不到文件：{FILE_METRIC_STD}")
        return None

    try:
        df = pd.read_excel(FILE_METRIC_STD, sheet_name="标准定义", header=1)
        df = df.dropna(how='all')
        df.columns = [str(c).strip() for c in df.columns]

        # 自动识别核心列
        col_id = [c for c in df.columns if '编号' in c and '业务' not in c][0]
        col_theme = [c for c in df.columns if '业务主题' in c][0]
        col_l1 = [c for c in df.columns if '一级分类' in c][0]
        col_l2 = [c for c in df.columns if '二级分类' in c][0]
        col_name = [c for c in df.columns if '中文名称' in c][0]
        col_calc = [c for c in df.columns if '业务口径' in c][0]
        col_unit = [c for c in df.columns if '计量单位' in c][0]

        # 整理指标字典
        metric_df = df[[col_id, col_theme, col_l1, col_l2, col_name, col_calc, col_unit]].copy()
        metric_df.columns = ['指标编号', '业务主题', '一级分类', '二级分类', '指标名称', '业务口径', '计量单位']
        metric_df = metric_df.dropna(subset=['指标编号'])

        # --- 质检逻辑 ---
        # 检查口径是否为空
        metric_df['口径质检'] = metric_df['业务口径'].apply(
            lambda x: '缺失' if pd.isna(x) or str(x).strip() == '' else '合规')

        out_csv = os.path.join(OUT_DIR, "指标数据标准_质检报告.csv")
        metric_df.to_csv(out_csv, index=False, encoding="utf-8-sig")
        print(f"[OK] 指标数据标准质检完成，结果已保存：{out_csv}")
        print(f"     发现有效指标标准 {len(metric_df)} 条。")

        return metric_df

    except Exception as e:
        print(f"[错误] 读取指标数据标准失败：{e}")
        return None


# ==================== 3. 绘制指标体系树状图 ====================
def draw_metric_tree(metric_df):
    if metric_df is None or metric_df.empty:
        print("[跳过] 指标数据为空，跳过画树状图。")
        return

    print("\n[Step 3] 正在绘制“指标分类体系”树状图...")

    # 由于可能有很多指标，我们取前 8 个画图，防止太拥挤
    df_plot = metric_df.head(8)

    G = nx.DiGraph()
    root = "指标标准体系"
    G.add_node(root)

    # 动态添加节点
    for _, row in df_plot.iterrows():
        theme = str(row['业务主题'])
        l1 = str(row['一级分类'])
        l2 = str(row['二级分类'])
        name = str(row['指标名称'])

        # 构建层级路径
        G.add_edge(root, theme)
        G.add_edge(theme, l1)
        if l2 != 'nan':
            G.add_edge(l1, l2)
            G.add_edge(l2, name)
        else:
            G.add_edge(l1, name)

    # 使用分层的拓扑布局
    try:
        pos = nx.nx_agraph.graphviz_layout(G, prog="dot")  # 需要 pygraphviz，如果没有则报错
    except:
        # 如果没有 pygraphviz，使用自带的 multipartite_layout 或 spring_layout
        pos = nx.spring_layout(G, seed=42, k=1.5)
        # 简易手动层级分布 (实际画图效果可看)

    # 为了美观，我们强制手动分层（从左到右）
    # Root x=0, Theme x=1, L1 x=2, L2 x=3, Name x=4
    pos = {}
    layers = {"指标标准体系": 0}
    for node in G.nodes():
        if node == root: continue
        if any(node == str(t) for t in df_plot['业务主题']):
            layers[node] = 1
        elif any(node == str(c) for c in df_plot['一级分类']):
            layers[node] = 2
        elif any(node == str(c) for c in df_plot['二级分类'] if pd.notna(c)):
            layers[node] = 3
        else:
            layers[node] = 4

    # 根据层分配坐标
    layer_counts = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0}
    for node, layer in layers.items():
        x = layer * 2.0
        y = layer_counts[layer] * -1.5
        pos[node] = (x, y)
        layer_counts[layer] += 1

    fig, ax = plt.subplots(figsize=(14, 8))

    # 画边
    nx.draw_networkx_edges(G, pos, edge_color="gray", width=1.5, alpha=0.7, ax=ax)
    # 画节点
    nx.draw_networkx_nodes(G, pos, node_color="lightgreen", node_size=3000,
                           edgecolors="black", node_shape="s", ax=ax)
    # 画标签
    nx.draw_networkx_labels(G, pos, font_size=10, font_family="Microsoft YaHei",
                            font_color="black", ax=ax)

    ax.set_title("指标体系分类树状图 (维度标准化)", fontproperties=my_font, fontsize=18, pad=20)
    ax.axis("off")

    out_path = os.path.join(OUT_DIR, "指标体系分类树状图.png")
    plt.tight_layout()
    plt.savefig(out_path, dpi=200, bbox_inches="tight")
    plt.close()
    print(f"[OK] 树状图已保存：{out_path}")


# ==================== 4. 绘制标准部门分布柱状图 ====================
def draw_dept_distribution():
    print("\n[Step 4] 正在读取“标准分布统计”并绘图...")
    if not os.path.exists(FILE_BASE_STD):
        return

    try:
        # 读取基础数据标准模板的第2个sheet
        df_dist = pd.read_excel(FILE_BASE_STD, sheet_name="标准分布统计", header=2)
        # 清理掉全空行/列
        df_dist = df_dist.dropna(how='all').dropna(axis=1, how='all')

        # 第一个列是主题，最后一列是Grand Total，中间是各部门
        df_dist = df_dist.set_index(df_dist.columns[0])
        df_dist = df_dist.drop(columns=['Grand Total'], errors='ignore')

        # 把各部门的总数加起来
        dept_totals = df_dist.sum().sort_values(ascending=False)

        fig, ax = plt.subplots(figsize=(12, 6))
        bars = ax.bar(dept_totals.index, dept_totals.values, color='skyblue', edgecolor='black')

        # 加数值标签
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2., height,
                    f'{int(height)}', ha='center', va='bottom', fontproperties=my_font)

        ax.set_title("各业务部门数据标准数量分布", fontproperties=my_font, fontsize=16)
        ax.set_ylabel("标准数量", fontproperties=my_font, fontsize=12)
        plt.xticks(rotation=45, ha='right', fontproperties=my_font)
        plt.yticks(fontproperties=my_font)

        out_path = os.path.join(OUT_DIR, "部门数据标准数量分布.png")
        plt.tight_layout()
        plt.savefig(out_path, dpi=200, bbox_inches="tight")
        plt.close()
        print(f"[OK] 部门分布图已保存：{out_path}")

    except Exception as e:
        print(f"[警告] 部门分布统计绘图失败：{e}")


# ==================== 5. 主流程 ====================
if __name__ == "__main__":
    print("=" * 60)
    print("第13章 指标体系管理 —— 数据标准质检与可视化")
    print("=" * 60)

    base_audit = audit_base_standard()
    metric_audit = audit_metric_standard()

    draw_metric_tree(metric_audit)
    draw_dept_distribution()

    print("\n全部任务执行完毕！快去 output 文件夹查收报告和图表吧。")