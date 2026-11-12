-- 阿里云零售数据模型星型模型简化版 DDL

-- dim_date

        CREATE TABLE IF NOT EXISTS dim_date (
            date_id INTEGER PRIMARY KEY,
            date_str TEXT,
            year INTEGER,
            month INTEGER,
            day INTEGER,
            is_weekend INTEGER
        );
    

-- dim_customer

        CREATE TABLE IF NOT EXISTS dim_customer (
            customer_id INTEGER PRIMARY KEY,
            customer_name TEXT,
            gender INTEGER, -- 1:男, 2:女
            member_level INTEGER -- 1:普通, 2:高级, 3:VIP
        );
    

-- dim_product

        CREATE TABLE IF NOT EXISTS dim_product (
            product_id INTEGER PRIMARY KEY,
            product_name TEXT,
            category TEXT, -- 类目
            brand TEXT,    -- 品牌
            price REAL     -- 标准售价
        );
    

-- dim_store

        CREATE TABLE IF NOT EXISTS dim_store (
            store_id INTEGER PRIMARY KEY,
            store_name TEXT,
            store_type TEXT, -- 中心店/社区店/大卖场
            city TEXT
        );
    

-- fct_sales

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
    

