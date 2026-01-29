#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PySide6 SQL 数据库连接示例

主要类：
- QSqlDatabase: 数据库连接
- QSqlQuery: SQL 查询
- QSqlTableModel: 表格模型
- QSqlRelationalTableModel: 关联模型

支持的驱动：
- QSQLITE (内置)
- QMYSQL, QPSQL, QODBC 等

官方文档: https://doc.qt.io/qtforpython/PySide6/QtSql/index.html
"""

import sys
import os
from PySide6.QtCore import QCoreApplication
from PySide6.QtSql import (
    QSqlDatabase, QSqlQuery, QSqlError, QSqlRecord
)


def show_available_drivers():
    """显示可用数据库驱动"""
    print("=== 可用数据库驱动 ===\n")
    print(f"驱动列表: {QSqlDatabase.drivers()}")


def create_connection():
    """创建数据库连接"""
    print("\n=== 创建数据库连接 ===\n")
    
    # 使用 SQLite (内置，无需安装)
    db = QSqlDatabase.addDatabase("QSQLITE")
    db.setDatabaseName("demo.db")  # 文件数据库
    
    # 内存数据库: db.setDatabaseName(":memory:")
    
    if not db.open():
        print(f"数据库打开失败: {db.lastError().text()}")
        return False
    
    print("数据库连接成功")
    print("数据库文件: demo.db")
    return True


def create_tables():
    """创建表"""
    print("\n=== 创建表 ===\n")
    
    query = QSqlQuery()
    
    # 删除旧表
    query.exec("DROP TABLE IF EXISTS users")
    query.exec("DROP TABLE IF EXISTS orders")
    
    # 创建用户表
    success = query.exec("""
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE,
            age INTEGER,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    if success:
        print("users 表创建成功")
    else:
        print(f"创建失败: {query.lastError().text()}")
    
    # 创建订单表
    success = query.exec("""
        CREATE TABLE orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            product TEXT,
            amount REAL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)
    
    if success:
        print("orders 表创建成功")


def insert_data():
    """插入数据"""
    print("\n=== 插入数据 ===\n")
    
    query = QSqlQuery()
    
    # 方式1: 直接执行
    query.exec("INSERT INTO users (name, email, age) VALUES ('张三', 'zhang@example.com', 25)")
    print(f"插入张三, ID: {query.lastInsertId()}")
    
    # 方式2: 预处理语句 (推荐，防 SQL 注入)
    query.prepare("INSERT INTO users (name, email, age) VALUES (?, ?, ?)")
    query.addBindValue("李四")
    query.addBindValue("li@example.com")
    query.addBindValue(30)
    query.exec()
    print(f"插入李四, ID: {query.lastInsertId()}")
    
    # 方式3: 命名参数
    query.prepare("INSERT INTO users (name, email, age) VALUES (:name, :email, :age)")
    query.bindValue(":name", "王五")
    query.bindValue(":email", "wang@example.com")
    query.bindValue(":age", 28)
    query.exec()
    print(f"插入王五, ID: {query.lastInsertId()}")
    
    # 批量插入订单
    query.prepare("INSERT INTO orders (user_id, product, amount) VALUES (?, ?, ?)")
    
    user_ids = [1, 1, 2, 3]
    products = ["手机", "电脑", "平板", "耳机"]
    amounts = [5999.0, 8999.0, 3299.0, 299.0]
    
    query.addBindValue(user_ids)
    query.addBindValue(products)
    query.addBindValue(amounts)
    
    if query.execBatch():
        print("批量插入订单成功")


def query_data():
    """查询数据"""
    print("\n=== 查询数据 ===\n")
    
    query = QSqlQuery()
    
    # 简单查询
    print("--- 所有用户 ---")
    query.exec("SELECT * FROM users")
    while query.next():
        user_id = query.value(0)
        name = query.value("name")
        email = query.value("email")
        age = query.value("age")
        print(f"  ID:{user_id}, 姓名:{name}, 邮箱:{email}, 年龄:{age}")
    
    # 条件查询
    print("\n--- 年龄大于25的用户 ---")
    query.prepare("SELECT name, age FROM users WHERE age > ?")
    query.addBindValue(25)
    query.exec()
    while query.next():
        print(f"  {query.value('name')}, {query.value('age')}岁")
    
    # 联表查询
    print("\n--- 用户订单 (JOIN) ---")
    query.exec("""
        SELECT users.name, orders.product, orders.amount
        FROM orders
        JOIN users ON orders.user_id = users.id
        ORDER BY users.name
    """)
    while query.next():
        print(f"  {query.value(0)} 购买了 {query.value(1)}, ¥{query.value(2):.2f}")
    
    # 聚合查询
    print("\n--- 统计信息 ---")
    query.exec("SELECT COUNT(*), AVG(age) FROM users")
    if query.next():
        print(f"  用户数: {query.value(0)}")
        print(f"  平均年龄: {query.value(1)}")
    
    query.exec("SELECT user_id, SUM(amount) as total FROM orders GROUP BY user_id")
    print("\n--- 各用户消费总额 ---")
    while query.next():
        print(f"  用户{query.value(0)}: ¥{query.value(1):.2f}")


def update_and_delete():
    """更新和删除"""
    print("\n=== 更新和删除 ===\n")
    
    query = QSqlQuery()
    
    # 更新
    query.prepare("UPDATE users SET age = age + 1 WHERE name = ?")
    query.addBindValue("张三")
    if query.exec():
        print(f"更新成功, 影响行数: {query.numRowsAffected()}")
    
    # 验证更新
    query.exec("SELECT name, age FROM users WHERE name = '张三'")
    if query.next():
        print(f"张三现在{query.value('age')}岁")
    
    # 删除 (演示，不实际删除)
    print("\n删除语法: DELETE FROM users WHERE id = ?")


def demonstrate_transactions():
    """事务处理"""
    print("\n=== 事务处理 ===\n")
    
    db = QSqlDatabase.database()
    query = QSqlQuery()
    
    # 开始事务
    db.transaction()
    print("事务开始")
    
    query.exec("INSERT INTO users (name, email, age) VALUES ('临时用户', 'temp@example.com', 20)")
    print("插入临时用户")
    
    # 回滚事务
    db.rollback()
    print("事务回滚")
    
    # 验证回滚
    query.exec("SELECT COUNT(*) FROM users WHERE name = '临时用户'")
    if query.next():
        print(f"临时用户数量: {query.value(0)} (应为0)")
    
    # 提交事务示例
    print("\n提交事务语法: db.commit()")


def show_record_info():
    """显示记录信息"""
    print("\n=== 记录信息 ===\n")
    
    query = QSqlQuery("SELECT * FROM users LIMIT 1")
    record = query.record()
    
    print(f"字段数量: {record.count()}")
    for i in range(record.count()):
        field = record.field(i)
        print(f"  字段{i}: {record.fieldName(i)} ({field.typeID()})")


def main():
    app = QCoreApplication(sys.argv)
    
    print("=== PySide6 SQL 数据库连接示例 ===")
    
    show_available_drivers()
    
    if not create_connection():
        return 1
    
    create_tables()
    insert_data()
    query_data()
    update_and_delete()
    demonstrate_transactions()
    show_record_info()
    
    # 清理
    QSqlDatabase.database().close()
    try:
        os.remove("demo.db")
        print("\n测试数据库已删除")
    except:
        pass
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
