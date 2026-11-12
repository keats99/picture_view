# -*- coding: utf-8 -*-
import pandas as pd
import sqlite3
import os
import warnings

warnings.filterwarnings('ignore')

# ==========================================
# 0. 环境与路径配置
# ==========================================
BASE_DIR = r"D:\Python_code\cda和数据可视化作业\商业数据分析平时作业"
DATA_DIR = os.path.join(BASE_DIR, "data", "chapter08_sql_basics")
SRC_DIR = os.path.join(BASE_DIR, "src", "chapter08_sql_basics")
OUT_DIR = os.path.join(BASE_DIR, "output", "chapter08_sql_basics")

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(SRC_DIR, exist_ok=True)
os.makedirs(OUT_DIR, exist_ok=True)

db_path = os.path.join(OUT_DIR, "chapter8_kdd99.db")
csv_path = os.path.join(DATA_DIR, "kdd99_accounts.csv")

print("=" * 50)
print("开始执行 第8章：SQL基础语法与数据库操作")
print("=" * 50)

# ==========================================
# 1. 准备数据与环境
# ==========================================
try:
    # 1. 尝试用强容错的方式读取 CSV
    # encoding='gbk' 防止中文乱码，on_bad_lines='skip' 防止某一行的列数不对导致报错
    df_accounts = pd.read_csv(csv_path, header=None, names=['account_id', 'frequency', 'date'],
                              encoding='gbk', on_bad_lines='skip')
    print(f"✅ 成功读取 kdd99_accounts.csv，共 {len(df_accounts)} 行")

    # 尝试把日期列转成标准格式，防雷
    df_accounts['date'] = pd.to_datetime(df_accounts['date'], errors='coerce').dt.strftime('%Y-%m-%d')

except Exception as e:
    print(f"❌ 读取 CSV 文件失败，具体错误：{e}")
    raise

# 1.2 创建/连接 SQLite 数据库
if os.path.exists(db_path):
    os.remove(db_path)
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 1.3 将 accounts 写入数据库
df_accounts.to_sql('accounts', conn, index=False)

# 1.4 伪造教材中 SQL 用到的其他表
df_sale = pd.DataFrame({
    'year': [2012, 2012, 2013],
    'market': ['A', 'B', 'A'],
    'sale': [1000, 2000, 1500],
    'profit': [100, 150, 300]
})
df_sale.to_sql('sale', conn, index=False)

df_t1 = pd.DataFrame({'id': [1, 2, 3], 'name': ['Tom', 'Jerry', 'Spike']})
df_t2 = pd.DataFrame({'id': [2, 3, 4], 'age': [20, 25, 30]})
df_t1.to_sql('table1', conn, index=False)
df_t2.to_sql('table2', conn, index=False)

df_trans = pd.DataFrame({
    'account_id': [1, 2, 3, 1, 2],
    'date': ['1998-12-01', '1998-12-15', '1998-12-20', '1998-12-25', '1998-12-31'],
    'bank': ['B1', 'B2', 'B1', 'B2', 'B1'],
    'amount': [100, 500, 200, 300, 400],
    'k_symbol': ['房屋贷款', '房屋贷款', '日常开销', '房屋贷款', '房屋贷款']
})
df_trans.to_sql('trans', conn, index=False)
print("✅ 数据库表初始化完成！\n")

# ==========================================
# 2. 核心 SQL 执行模块
# ==========================================
sql_queries = {
    "01_选择表中指定列": "SELECT year, market, sale, profit FROM sale;",

    "02_删除重复的行": "SELECT DISTINCT year FROM sale;",

    "03_过滤与排序": """
        SELECT * FROM sale 
        WHERE year = 2012 
        ORDER BY sale DESC;
    """,

    "04_用表达式创建新列": """
        SELECT year, market, sale, profit, 
               (profit * 1.0 / sale) AS rate 
        FROM sale;
    """,

    "05_对列重编码_CASE_WHEN": """
        SELECT account_id, 
               date,
               CAST(strftime('%w', date) AS INTEGER) AS weekday,
               (CASE 
                   WHEN CAST(strftime('%w', date) AS INTEGER) IN (0, 6) THEN '周末'
                   ELSE '工作日'
                END) AS is_weekend
        FROM trans
        WHERE date BETWEEN '1998-12-01' AND '1998-12-31'
          AND k_symbol = '房屋贷款';
    """,

    "06_分组与汇总_HAVING": """
        SELECT date, 
               COUNT(account_id) AS count_of_account_id, 
               AVG(amount) AS mean_of_amount, 
               SUM(amount) AS sum_of_amount
        FROM trans
        GROUP BY date
        HAVING COUNT(account_id) > 0;
    """,

    "07_内连接": """
        SELECT * 
        FROM table1, table2
        WHERE table1.id = table2.id;
    """,

    "08_左连接": """
        SELECT * 
        FROM table1 
        LEFT JOIN table2 ON table1.id = table2.id;
    """,

    "09_子查询": """
        SELECT * FROM trans 
        WHERE account_id IN (
            SELECT account_id FROM accounts WHERE frequency > 50
        );
    """,

    "10_集合操作_UNION": """
        SELECT id, name FROM table1
        UNION
        SELECT id, 'Unknown' FROM table2;
    """
}

for query_name, sql in sql_queries.items():
    try:
        # 执行查询
        df_result = pd.read_sql_query(sql, conn)

        print(f"👉 正在执行: {query_name}")
        print(f"--- 查询结果 ({len(df_result)} 行) ---")
        if len(df_result) > 0:
            print(df_result.head(5).to_string(index=False))
        else:
            print("空结果集")
        print("-" * 30)

        # 保存结果
        out_file = os.path.join(OUT_DIR, f"{query_name}.csv")
        df_result.to_csv(out_file, index=False, encoding='gbk')

    except Exception as e:
        print(f"❌ 执行 {query_name} 时报错: {e}")

conn.close()

print("=" * 50)
print(f"🎉 第8章 SQL 基础语法执行完毕！\n所有查询结果 CSV 已保存至：\n{OUT_DIR}")
print("=" * 50)