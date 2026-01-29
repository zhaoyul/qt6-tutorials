#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Qt6 SQL 模型示例 - QSqlTableModel, QSqlQueryModel

主要类：
- QSqlQueryModel: 只读查询模型，用于显示查询结果
- QSqlTableModel: 可编辑的表格模型，直接操作数据库表
- QSqlRelationalTableModel: 关联表格模型（本示例未演示）

本示例演示：
- QSqlQueryModel 的只读查询显示
- QSqlTableModel 的基本 CRUD 操作
- 排序、过滤、数据修改
- 提交和回滚修改

注意: 虽然不需要显示 GUI，但模型类属于 Qt::Widgets 模块

官方文档:
- https://doc.qt.io/qtforpython/PySide6/QtSql/QSqlQueryModel.html
- https://doc.qt.io/qtforpython/PySide6/QtSql/QSqlTableModel.html
"""

import sys
import os
from PySide6.QtCore import QCoreApplication, Qt, QModelIndex
from PySide6.QtSql import (
    QSqlDatabase, QSqlQuery, QSqlQueryModel, QSqlTableModel,
    QSqlRecord, QSqlError
)


def create_connection():
    """创建数据库连接"""
    db = QSqlDatabase.addDatabase("QSQLITE")
    db.setDatabaseName("models_demo.db")

    if not db.open():
        print(f"数据库连接失败: {db.lastError().text()}")
        return False
    return True


def create_table_and_data():
    """创建表和数据"""
    query = QSqlQuery()

    # 创建产品表
    query.exec("DROP TABLE IF EXISTS products")
    query.exec("""
        CREATE TABLE products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT,
            price REAL,
            stock INTEGER DEFAULT 0,
            description TEXT
        )
    """)

    # 插入测试数据
    query.exec("INSERT INTO products (name, category, price, stock, description) VALUES "
               "('iPhone 15', '手机', 5999.00, 100, '苹果最新款手机')")
    query.exec("INSERT INTO products (name, category, price, stock, description) VALUES "
               "('MacBook Pro', '电脑', 14999.00, 50, '专业级笔记本电脑')")
    query.exec("INSERT INTO products (name, category, price, stock, description) VALUES "
               "('iPad Air', '平板', 4799.00, 80, '轻薄平板电脑')")
    query.exec("INSERT INTO products (name, category, price, stock, description) VALUES "
               "('AirPods Pro', '耳机', 1999.00, 200, '降噪耳机')")
    query.exec("INSERT INTO products (name, category, price, stock, description) VALUES "
               "('小米14', '手机', 3999.00, 150, '高性价比旗舰机')")
    query.exec("INSERT INTO products (name, category, price, stock, description) VALUES "
               "('华为Mate60', '手机', 6999.00, 80, '国产高端手机')")

    # 创建订单表用于联表查询演示
    query.exec("DROP TABLE IF EXISTS orders")
    query.exec("""
        CREATE TABLE orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER,
            quantity INTEGER,
            order_date DATE,
            customer_name TEXT
        )
    """)

    query.exec("INSERT INTO orders (product_id, quantity, order_date, customer_name) VALUES "
               "(1, 2, '2024-01-15', '客户A')")
    query.exec("INSERT INTO orders (product_id, quantity, order_date, customer_name) VALUES "
               "(2, 1, '2024-01-16', '客户B')")
    query.exec("INSERT INTO orders (product_id, quantity, order_date, customer_name) VALUES "
               "(1, 3, '2024-01-17', '客户C')")
    query.exec("INSERT INTO orders (product_id, quantity, order_date, customer_name) VALUES "
               "(4, 5, '2024-01-18', '客户D')")


def demonstrate_sql_query_model():
    """QSqlQueryModel - 只读查询模型"""
    print("\n=== QSqlQueryModel - 只读查询模型 ===\n")

    # QSqlQueryModel 用于执行任意 SQL 查询并显示结果
    # 它是只读的，不能修改数据

    model = QSqlQueryModel()

    # 1. 简单查询
    print("--- 所有产品 (简单查询) ---")
    model.setQuery("SELECT name, category, price, stock FROM products")

    # 检查查询是否成功
    if model.lastError().isValid():
        print(f"查询错误: {model.lastError().text()}")
        return

    # 获取记录数
    row_count = model.rowCount()
    col_count = model.columnCount()
    print(f"记录数: {row_count} 列数: {col_count}")

    # 打印表头
    header = ""
    for col in range(col_count):
        header += model.headerData(col, Qt.Horizontal) + "\t"
    print(header)

    # 遍历数据 - 使用 model.data() 或 model.record()
    for row in range(row_count):
        line = ""
        for col in range(col_count):
            index = model.index(row, col)
            line += str(model.data(index)) + "\t"
        print(line)

    # 2. 复杂查询 - 联表查询
    print("\n--- 订单详情 (联表查询) ---")
    model.setQuery("""
        SELECT 
            o.id as 订单ID,
            p.name as 产品名称,
            o.quantity as 数量,
            p.price as 单价,
            (o.quantity * p.price) as 总价,
            o.customer_name as 客户
        FROM orders o
        JOIN products p ON o.product_id = p.id
        ORDER BY o.id
    """)

    row_count = model.rowCount()
    print(f"订单记录数: {row_count}")

    # 打印表头
    header = ""
    for col in range(model.columnCount()):
        header += model.headerData(col, Qt.Horizontal) + "\t"
    print(header)

    # 遍历数据
    for row in range(row_count):
        line = ""
        for col in range(model.columnCount()):
            line += str(model.data(model.index(row, col))) + "\t"
        print(line)

    # 3. 聚合查询
    print("\n--- 分类统计 (聚合查询) ---")
    model.setQuery("""
        SELECT 
            category as 分类,
            COUNT(*) as 产品数,
            AVG(price) as 平均价格,
            SUM(stock) as 总库存
        FROM products
        GROUP BY category
    """)

    for row in range(model.rowCount()):
        category = model.data(model.index(row, 0))
        count = model.data(model.index(row, 1))
        avg_price = model.data(model.index(row, 2))
        total_stock = model.data(model.index(row, 3))
        print(f"  {category}: {count}种产品, 平均价格 ¥{avg_price:.2f}, 总库存 {total_stock}")

    # 4. 刷新数据
    print("\n--- 刷新数据 ---")
    # 当数据库数据改变时，可以调用 query() 重新执行查询
    model.setQuery(model.query().executedQuery())
    print(f"数据已刷新，当前记录数: {model.rowCount()}")


def demonstrate_sql_table_model():
    """QSqlTableModel - 可编辑表格模型"""
    print("\n=== QSqlTableModel - 可编辑表格模型 ===\n")

    # QSqlTableModel 直接绑定到数据库表
    # 支持读取、编辑、插入、删除操作

    model = QSqlTableModel()
    model.setTable("products")

    # 设置编辑策略
    # OnFieldChange: 字段改变立即提交
    # OnRowChange: 行改变时提交 (默认)
    # OnManualSubmit: 手动提交
    model.setEditStrategy(QSqlTableModel.OnManualSubmit)

    # 选择数据
    model.select()

    print("--- 原始数据 ---")
    print(f"记录数: {model.rowCount()}")

    # 打印数据
    for row in range(model.rowCount()):
        record = model.record(row)
        print(f"  ID:{record.value('id')}, {record.value('name')}, {record.value('category')}, "
              f"¥{record.value('price'):.2f}, 库存:{record.value('stock')}")

    # 1. 修改数据
    print("\n--- 修改数据 ---")
    index = model.index(0, 3)  # 第一行，price 列
    old_price = model.data(index)
    print(f"修改前 iPhone 15 价格: {old_price}")

    model.setData(index, 6299.00)
    print("修改后 iPhone 15 价格: 6299.00 (未提交到数据库)")

    # 提交修改
    if model.submitAll():
        print("修改已提交到数据库")
    else:
        print(f"提交失败: {model.lastError().text()}")

    # 2. 插入新记录
    print("\n--- 插入新记录 ---")
    new_row = model.rowCount()
    model.insertRow(new_row)

    model.setData(model.index(new_row, 1), "iPhone 15 Pro")   # name
    model.setData(model.index(new_row, 2), "手机")             # category
    model.setData(model.index(new_row, 3), 8999.00)           # price
    model.setData(model.index(new_row, 4), 60)                # stock
    model.setData(model.index(new_row, 5), "专业版手机")        # description

    if model.submitAll():
        print("新记录已插入")
        model.select()  # 刷新以获取新ID
    else:
        print(f"插入失败: {model.lastError().text()}")

    # 3. 使用记录方式插入
    print("\n--- 使用 QSqlRecord 插入 ---")
    record = model.record()
    record.setValue("name", "Apple Watch")
    record.setValue("category", "穿戴设备")
    record.setValue("price", 2999.00)
    record.setValue("stock", 120)
    record.setValue("description", "智能手表")

    if model.insertRecord(-1, record):  # -1 表示插入到最后
        model.submitAll()
        print("使用 QSqlRecord 插入成功")

    # 4. 删除记录
    print("\n--- 删除记录 ---")
    # 删除第一条记录
    model.removeRow(0)
    if model.submitAll():
        print("第一条记录已删除")

    # 刷新并显示最终数据
    model.select()
    print(f"\n--- 最终数据 ({model.rowCount()}条) ---")
    for row in range(model.rowCount()):
        r = model.record(row)
        print(f"  {r.value('name')} ({r.value('category')}): "
              f"¥{r.value('price'):.2f}, 库存:{r.value('stock')}")


def demonstrate_filtering_and_sorting():
    """过滤和排序"""
    print("\n=== 过滤和排序 ===\n")

    model = QSqlTableModel()
    model.setTable("products")
    model.setEditStrategy(QSqlTableModel.OnManualSubmit)

    # 1. 过滤 - 只显示手机
    print("--- 过滤: 只显示手机 ---")
    model.setFilter("category = '手机'")
    model.select()

    print(f"手机产品数: {model.rowCount()}")
    for row in range(model.rowCount()):
        record = model.record(row)
        print(f"  {record.value('name')}: ¥{record.value('price'):.2f}")

    # 2. 复杂过滤
    print("\n--- 过滤: 价格大于5000且库存大于50 ---")
    model.setFilter("price > 5000 AND stock > 50")
    model.select()

    for row in range(model.rowCount()):
        record = model.record(row)
        print(f"  {record.value('name')}: ¥{record.value('price'):.2f}, 库存:{record.value('stock')}")

    # 3. 排序
    print("\n--- 排序: 按价格降序 ---")
    model.setFilter("")  # 清除过滤
    model.setSort(3, Qt.DescendingOrder)  # 第3列(price)降序
    model.select()

    for row in range(model.rowCount()):
        record = model.record(row)
        print(f"  {record.value('name')}: ¥{record.value('price'):.2f}")

    # 4. 多字段排序
    print("\n--- 排序: 先按分类，再按价格 ---")
    model.setSort(2, Qt.AscendingOrder)   # category 升序
    # 注意：QSqlTableModel 只支持单字段排序，多字段需要自定义查询
    # 可以使用 setQuery() 配合自定义 SQL

    # 使用 QSqlQueryModel 实现复杂排序
    query_model = QSqlQueryModel()
    query_model.setQuery("""
        SELECT name, category, price, stock 
        FROM products 
        ORDER BY category ASC, price DESC
    """)

    for row in range(query_model.rowCount()):
        print(f"  [{query_model.data(query_model.index(row, 1))}] "
              f"{query_model.data(query_model.index(row, 0))}: "
              f"¥{query_model.data(query_model.index(row, 2)):.2f}")


def demonstrate_batch_operations():
    """批量操作和事务"""
    print("\n=== 批量操作和事务 ===\n")

    model = QSqlTableModel()
    model.setTable("products")
    model.setEditStrategy(QSqlTableModel.OnManualSubmit)  # 必须设为手动提交
    model.select()

    # 批量修改库存
    print("--- 批量修改库存 ---")
    for row in range(model.rowCount()):
        record = model.record(row)
        current_stock = record.value("stock")
        new_stock = current_stock + 10  # 所有产品库存 +10

        model.setData(model.index(row, 4), new_stock)
        print(f"  {record.value('name')}: 库存 {current_stock} -> {new_stock}")

    # 一次性提交所有修改
    if model.submitAll():
        print("\n批量修改已提交")
    else:
        print(f"\n批量修改失败: {model.lastError().text()}")

    # 批量插入
    print("\n--- 批量插入 ---")
    new_products = ["华为平板", "联想笔记本", "索尼耳机"]
    categories = ["平板", "电脑", "耳机"]
    prices = [3299.00, 6999.00, 2499.00]

    for i in range(len(new_products)):
        row = model.rowCount()
        model.insertRow(row)
        model.setData(model.index(row, 1), new_products[i])
        model.setData(model.index(row, 2), categories[i])
        model.setData(model.index(row, 3), prices[i])
        model.setData(model.index(row, 4), 50)

    if model.submitAll():
        print(f"批量插入成功: {len(new_products)}条记录")
        model.select()
        print(f"当前总记录数: {model.rowCount()}")

    # 回滚示例
    print("\n--- 批量回滚示例 ---")
    original_count = model.rowCount()
    print(f"当前记录数: {original_count}")

    # 插入一些临时数据
    model.insertRow(model.rowCount())
    model.setData(model.index(model.rowCount() - 1, 1), "临时产品1")
    model.insertRow(model.rowCount())
    model.setData(model.index(model.rowCount() - 1, 1), "临时产品2")

    print(f"插入2条临时数据后，行数: {model.rowCount()}")

    # 回滚 - 使用 revertAll()
    model.revertAll()
    print(f"回滚后，行数: {model.rowCount()} (应恢复为 {original_count})")


def demonstrate_header_customization():
    """表头自定义"""
    print("\n=== 表头自定义 ===\n")

    model = QSqlTableModel()
    model.setTable("products")

    # 自定义表头显示
    model.setHeaderData(0, Qt.Horizontal, "编号")
    model.setHeaderData(1, Qt.Horizontal, "产品名称")
    model.setHeaderData(2, Qt.Horizontal, "分类")
    model.setHeaderData(3, Qt.Horizontal, "价格(元)")
    model.setHeaderData(4, Qt.Horizontal, "库存数量")
    model.setHeaderData(5, Qt.Horizontal, "产品描述")

    model.select()

    # 打印自定义表头
    print("自定义表头:")
    for col in range(model.columnCount()):
        header = model.headerData(col, Qt.Horizontal)
        original = model.record().fieldName(col)
        print(f"  列{col}: '{header}' (原字段: {original})")


def main():
    app = QCoreApplication(sys.argv)

    print("=== Qt6 SQL 模型示例 (QSqlQueryModel & QSqlTableModel) ===")

    if not create_connection():
        return 1

    create_table_and_data()

    demonstrate_sql_query_model()
    demonstrate_sql_table_model()
    demonstrate_filtering_and_sorting()
    demonstrate_batch_operations()
    demonstrate_header_customization()

    # 清理
    QSqlDatabase.database().close()
    try:
        os.remove("models_demo.db")
        print("\n测试数据库已删除")
    except:
        pass

    return 0


if __name__ == "__main__":
    sys.exit(main())
