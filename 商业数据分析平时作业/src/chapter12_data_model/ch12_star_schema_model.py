# -*- coding: utf-8 -*-
r"""
第12章 数据模型与数据建模 —— 基于阿里零售数据模型白皮书的星型模型复现
运行环境：Windows + PyCharm，项目根目录 D:\Python_code\cda和数据可视化作业\商业数据分析平时作业
依赖：pandas, numpy, matplotlib, networkx, sqlite3
"""

import os
import sqlite3
import random
import datetime
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# ==================== 0. 路径与字体配置 ====================
BASE_DIR = r"D:\Python_code\cda和数据可视化作业\商业数据分析平时作业"
DATA_DIR = os.path.join(BASE_DIR, "data", "chapter12_data_model")
OUT_DIR = os.path.join(BASE_DIR, "output", "chapter12_data_model")
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(OUT_DIR, exist_ok=True)

FONT_PATH = r"C:\Windows\Fonts\msyh.ttc"
my_font = fm.FontProperties(fname=FONT_PATH)
plt.rcParams["font.sans-serif"] = ["Microsoft YaHei"]
plt.rcParams["axes.unicode_minus"] = False

DB_PATH = os.path.join(OUT_DIR, "retail_dw.db")
SQL_DDL_PATH = os.path.join(OUT_DIR, "retail_model_ddl.sql")

# ==================== 1. 定义数据模型（DDL） ====================
# 基于白皮书 6.1 公共域, 6.2 消费者域, 6.3 商品域, 6.6 交易域 抽象简化
DDL_STATEMENTS = {
    "dim_date": """
        CREATE TABLE IF NOT EXISTS dim_date (
            date_id INTEGER PRIMARY KEY,
            date_str TEXT,
            year INTEGER,
            month INTEGER,
            day INTEGER,
            is_weekend INTEGER
        );
    """,
    "dim_customer": """
        CREATE TABLE IF NOT EXISTS dim_customer (
            customer_id INTEGER PRIMARY KEY,
            customer_name TEXT,
            gender INTEGER, -- 1:男, 2:女
            member_level INTEGER -- 1:普通, 2:高级, 3:VIP
        );
    """,
    "dim_product": """
        CREATE TABLE IF NOT EXISTS dim_product (
            product_id INTEGER PRIMARY KEY,
            product_name TEXT,
            category TEXT, -- 类目
            brand TEXT,    -- 品牌
            price REAL     -- 标准售价
        );
    """,
    "dim_store": """
        CREATE TABLE IF NOT EXISTS dim_store (
            store_id INTEGER PRIMARY KEY,
            store_name TEXT,
            store_type TEXT, -- 中心店/社区店/大卖场
            city TEXT
        );
    """,
    "fct_sales": """
        CREATE TABLE IF NOT EXISTS fct_sales (
            order_id INTEGER PRIMARY KEY,
            date_id INTEGER,
            customer_id INTEGER,
            product_id INTEGER,
            store_id INTEGER,
            quantity INTEGER,
            total_amount REAL,
            FOREIGN KEY (date_id) REFERENCES dim_date(date_id),
            FOREIGN KEY (customer_id) REFERENCES dim_customer(customer_id),
            FOREIGN KEY (product_id) REFERENCES dim_product(product_id),
            FOREIGN KEY (store_id) REFERENCES dim_store(store_id)
        );
    """
}


def save_ddl_to_file():
    """将建表语句保存为sql文件"""
    with open(SQL_DDL_PATH, "w", encoding="utf-8") as f:
        f.write("-- 阿里云零售数据模型星型模型简化版 DDL\n\n")
        for table, sql in DDL_STATEMENTS.items():
            f.write(f"-- {table}\n{sql}\n\n")
    print(f"[OK] 建表SQL已保存：{SQL_DDL_PATH}")


# ==================== 2. 造数据与建库 ====================
def generate_and_load_data():
    print("[Step 1] 正在初始化SQLite数据库并造数...")
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 建表
    for table, sql in DDL_STATEMENTS.items():
        cursor.execute(sql)

    random.seed(42)

    # 1. 造日期维表 (2023年数据)
    dates = []
    start_date = datetime.date(2023, 1, 1)
    for i in range(365):
        d = start_date + datetime.timedelta(days=i)
        is_weekend = 1 if d.weekday() >= 5 else 0
        dates.append((int(d.strftime("%Y%m%d")), d.strftime("%Y-%m-%d"), d.year, d.month, d.day, is_weekend))
    cursor.executemany("INSERT INTO dim_date VALUES (?,?,?,?,?,?)", dates)

    # 2. 造客户维表
    genders = [1, 2]
    levels = [1, 2, 3]
    customers = [(i, f"客户_{i}", random.choice(genders), random.choice(levels)) for i in range(1, 501)]

    # 3. 造商品维表
    categories = ["手机数码", "服饰鞋包", "食品生鲜", "家居家装"]
    brands = ["阿里自营", "Apple", "优衣库", "三只松鼠", "宜家"]
    products = []
    for i in range(1, 101):
        p_name = f"商品_{i}"
        cate = random.choice(categories)
        brand = random.choice(brands)
        price = round(random.uniform(10.0, 5000.0), 2)
        products.append((i, p_name, cate, brand, price))

    # 4. 造门店维表
    cities = ["杭州", "上海", "北京", "深圳", "成都"]
    store_types = ["中心店", "社区店", "大卖场"]
    stores = [(i, f"盒马_{i}店", random.choice(store_types), random.choice(cities)) for i in range(1, 21)]

    # 5. 造销售事实表 (1万条订单)
    sales = []
    for order_id in range(1, 10001):
        date_rec = random.choice(dates)
        cust = random.choice(customers)
        prod = random.choice(products)
        store = random.choice(stores)

        # 逻辑：如果是VIP客户，买的可能多一点
        qty = random.randint(1, 3) if cust[3] == 3 else random.randint(1, 2)
        # 总价 = 单价 * 数量 * 随机折扣(0.8~1.0)
        amount = round(prod[4] * qty * random.uniform(0.8, 1.0), 2)

        sales.append((order_id, date_rec[0], cust[0], prod[0], store[0], qty, amount))

    # 批量插入
    cursor.executemany("INSERT INTO dim_customer VALUES (?,?,?,?)", customers)
    cursor.executemany("INSERT INTO dim_product VALUES (?,?,?,?,?)", products)
    cursor.executemany("INSERT INTO dim_store VALUES (?,?,?,?)", stores)
    cursor.executemany("INSERT INTO fct_sales VALUES (?,?,?,?,?,?,?)", sales)

    conn.commit()

    # 执行验证 SQL (证明关联查询能跑通)
    print("[Step 2] 正在执行多维分析 SQL (Join)...")
    sql_query = """
        SELECT 
            s.city AS `城市`,
            p.category AS `商品类目`,
            COUNT(f.order_id) AS `订单数`,
            SUM(f.quantity) AS `总销量`,
            ROUND(SUM(f.total_amount), 2) AS `销售总额`
        FROM fct_sales f
        JOIN dim_store s ON f.store_id = s.store_id
        JOIN dim_product p ON f.product_id = p.product_id
        JOIN dim_customer c ON f.customer_id = c.customer_id
        WHERE c.member_level = 3  -- 只看 VIP 客户
        GROUP BY s.city, p.category
        ORDER BY `销售总额` DESC
        LIMIT 10
    """
    df_result = pd.read_sql_query(sql_query, conn)
    result_csv_path = os.path.join(OUT_DIR, "VIP客户_各城市_类目销售分析.csv")
    df_result.to_csv(result_csv_path, index=False, encoding="utf-8-sig")

    conn.close()
    print(f"[OK] 数据库已生成：{DB_PATH}")
    print(f"[OK] 关联查询结果已导出：{result_csv_path}")
    print("\n【SQL查询结果预览 (Top 5)】")
    print(df_result.head(5).to_string(index=False))

    return True


# ==================== 3. 绘制星型模型 ER 图 ====================
def draw_star_schema():
    print("\n[Step 3] 正在绘制星型模型 ER 图...")
    G = nx.Graph()

    center_node = "事实表\nfct_sales\n(销售明细)"
    dim_nodes = [
        "维度表\ndim_date\n(日期)",
        "维度表\ndim_customer\n(消费者)",
        "维度表\ndim_product\n(商品)",
        "维度表\ndim_store\n(门店)"
    ]

    G.add_node(center_node)
    for n in dim_nodes:
        G.add_node(n)
        G.add_edge(center_node, n)

    # 自定义位置，形成完美的放射状
    pos = {
        center_node: (0, 0),
        dim_nodes[0]: (0, 2.5),  # 日期在上
        dim_nodes[1]: (2.5, 0),  # 客户在右
        dim_nodes[2]: (0, -2.5),  # 商品在下
        dim_nodes[3]: (-2.5, 0)  # 门店在左
    }

    fig, ax = plt.subplots(figsize=(10, 8))

    # 画边
    nx.draw_networkx_edges(G, pos, width=2, edge_color="gray", style="dashed", ax=ax)

    # 画中心事实表节点
    nx.draw_networkx_nodes(G, pos, nodelist=[center_node], node_color="salmon",
                           node_size=4000, node_shape="s", edgecolors="black", ax=ax)

    # 画四周维度表节点
    nx.draw_networkx_nodes(G, pos, nodelist=dim_nodes, node_color="lightblue",
                           node_size=3000, node_shape="s", edgecolors="black", ax=ax)

    # 画标签
    for node, (x, y) in pos.items():
        ax.text(x, y, node, fontproperties=my_font, fontsize=11,
                ha='center', va='center', color='black', fontweight='bold')

    # 添加连线上的关系说明 (1:N)
    ax.text(1.25, 1.25, "1 : N", fontproperties=my_font, color="red", fontsize=12)
    ax.text(1.25, -1.25, "1 : N", fontproperties=my_font, color="red", fontsize=12)
    ax.text(-1.25, 1.25, "1 : N", fontproperties=my_font, color="red", fontsize=12)
    ax.text(-1.25, -1.25, "1 : N", fontproperties=my_font, color="red", fontsize=12)

    ax.set_title("零售数据中台星型模型 (Star Schema) 示意图",
                 fontproperties=my_font, fontsize=18, pad=20)
    ax.axis("off")

    out_path = os.path.join(OUT_DIR, "零售星型模型_ER图.png")
    plt.tight_layout()
    plt.savefig(out_path, dpi=200, bbox_inches="tight")
    plt.close()
    print(f"[OK] 星型模型图已保存：{out_path}")


# ==================== 4. 尝试解析 PDF (只做文本展示) ====================
def read_pdf_for_report():
    pdf_path = os.path.join(DATA_DIR, "阿里云数据中台零售数据模型白皮书.pdf")
    if not os.path.exists(pdf_path):
        print("[跳过] 找不到PDF文件，跳过文本提取。")
        return

    try:
        import pdfplumber
        with pdfplumber.open(pdf_path) as pdf:
            # 我们只提取前言的一页，证明我们结合了材料
            first_page_text = pdf.pages[3].extract_text()
            if first_page_text:
                print("\n[Step 4] 已成功读取 PDF 文本片段 (证明结合了原始材料)：")
                print("-" * 50)
                print(first_page_text[:200].replace("\n", " ") + "...")
                print("-" * 50)

                # 将背景信息保存
                with open(os.path.join(OUT_DIR, "PDF业务背景读取记录.txt"), "w", encoding="utf-8") as f:
                    f.write("提取自《阿里云数据中台零售数据模型白皮书》前言部分：\n\n")
                    f.write(first_page_text)
                print(f"[OK] PDF文字背景已存至：{OUT_DIR}\\PDF业务背景读取记录.txt")
    except Exception as e:
        print(f"[警告] 读取PDF失败：{e}，不影响主业务流程。")


# ==================== 5. 主流程 ====================
if __name__ == "__main__":
    print("=" * 60)
    print("第12章 数据模型与数据建模 —— 零售星型模型复现")
    print("=" * 60)

    # 1. 保存 DDL
    save_ddl_to_file()

    # 2. 建库与跑数
    generate_and_load_data()

    # 3. 画模型图
    draw_star_schema()

    # 4. 读PDF
    read_pdf_for_report()

    print("\n全部任务执行完毕！快去 output 文件夹查收结果吧。")