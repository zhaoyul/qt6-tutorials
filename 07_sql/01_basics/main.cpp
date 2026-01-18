/**
 * Qt6 SQL 数据库示例
 *
 * 主要类：
 * - QSqlDatabase: 数据库连接
 * - QSqlQuery: SQL 查询
 * - QSqlTableModel: 表格模型
 * - QSqlRelationalTableModel: 关联模型
 *
 * 支持的驱动：
 * - QSQLITE (内置)
 * - QMYSQL, QPSQL, QODBC 等
 *
 * 官方文档: https://doc.qt.io/qt-6/sql-programming.html
 */

#include <QCoreApplication>
#include <QSqlDatabase>
#include <QSqlQuery>
#include <QSqlError>
#include <QSqlRecord>
#include <QSqlField>
#include <QSqlTableModel>
#include <QVariant>
#include <QDebug>
#include <QFile>

void showAvailableDrivers()
{
    qDebug() << "=== 可用数据库驱动 ===\n";
    qDebug() << "驱动列表:" << QSqlDatabase::drivers();
}

bool createConnection()
{
    qDebug() << "\n=== 创建数据库连接 ===\n";

    // 使用 SQLite (内置，无需安装)
    QSqlDatabase db = QSqlDatabase::addDatabase("QSQLITE");
    db.setDatabaseName("demo.db");  // 文件数据库

    // 内存数据库: db.setDatabaseName(":memory:");

    if (!db.open()) {
        qDebug() << "数据库打开失败:" << db.lastError().text();
        return false;
    }

    qDebug() << "数据库连接成功";
    qDebug() << "数据库文件: demo.db";
    return true;
}

void createTables()
{
    qDebug() << "\n=== 创建表 ===\n";

    QSqlQuery query;

    // 删除旧表
    query.exec("DROP TABLE IF EXISTS users");
    query.exec("DROP TABLE IF EXISTS orders");

    // 创建用户表
    bool success = query.exec(R"(
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE,
            age INTEGER,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    )");

    if (success) {
        qDebug() << "users 表创建成功";
    } else {
        qDebug() << "创建失败:" << query.lastError().text();
    }

    // 创建订单表
    success = query.exec(R"(
        CREATE TABLE orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            product TEXT,
            amount REAL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    )");

    if (success) {
        qDebug() << "orders 表创建成功";
    }
}

void insertData()
{
    qDebug() << "\n=== 插入数据 ===\n";

    QSqlQuery query;

    // 方式1: 直接执行
    query.exec("INSERT INTO users (name, email, age) VALUES ('张三', 'zhang@example.com', 25)");
    qDebug() << "插入张三, ID:" << query.lastInsertId().toInt();

    // 方式2: 预处理语句 (推荐，防 SQL 注入)
    query.prepare("INSERT INTO users (name, email, age) VALUES (?, ?, ?)");
    query.addBindValue("李四");
    query.addBindValue("li@example.com");
    query.addBindValue(30);
    query.exec();
    qDebug() << "插入李四, ID:" << query.lastInsertId().toInt();

    // 方式3: 命名参数
    query.prepare("INSERT INTO users (name, email, age) VALUES (:name, :email, :age)");
    query.bindValue(":name", "王五");
    query.bindValue(":email", "wang@example.com");
    query.bindValue(":age", 28);
    query.exec();
    qDebug() << "插入王五, ID:" << query.lastInsertId().toInt();

    // 批量插入订单
    query.prepare("INSERT INTO orders (user_id, product, amount) VALUES (?, ?, ?)");

    QVariantList userIds = {1, 1, 2, 3};
    QVariantList products = {"手机", "电脑", "平板", "耳机"};
    QVariantList amounts = {5999.0, 8999.0, 3299.0, 299.0};

    query.addBindValue(userIds);
    query.addBindValue(products);
    query.addBindValue(amounts);

    if (query.execBatch()) {
        qDebug() << "批量插入订单成功";
    }
}

void queryData()
{
    qDebug() << "\n=== 查询数据 ===\n";

    QSqlQuery query;

    // 简单查询
    qDebug() << "--- 所有用户 ---";
    query.exec("SELECT * FROM users");
    while (query.next()) {
        int id = query.value(0).toInt();
        QString name = query.value("name").toString();
        QString email = query.value("email").toString();
        int age = query.value("age").toInt();
        qDebug() << QString("  ID:%1, 姓名:%2, 邮箱:%3, 年龄:%4")
                    .arg(id).arg(name).arg(email).arg(age);
    }

    // 条件查询
    qDebug() << "\n--- 年龄大于25的用户 ---";
    query.prepare("SELECT name, age FROM users WHERE age > ?");
    query.addBindValue(25);
    query.exec();
    while (query.next()) {
        qDebug() << "  " << query.value("name").toString()
                 << "," << query.value("age").toInt() << "岁";
    }

    // 联表查询
    qDebug() << "\n--- 用户订单 (JOIN) ---";
    query.exec(R"(
        SELECT users.name, orders.product, orders.amount
        FROM orders
        JOIN users ON orders.user_id = users.id
        ORDER BY users.name
    )");
    while (query.next()) {
        qDebug() << QString("  %1 购买了 %2, ¥%3")
                    .arg(query.value(0).toString())
                    .arg(query.value(1).toString())
                    .arg(query.value(2).toDouble(), 0, 'f', 2);
    }

    // 聚合查询
    qDebug() << "\n--- 统计信息 ---";
    query.exec("SELECT COUNT(*), AVG(age) FROM users");
    if (query.next()) {
        qDebug() << "  用户数:" << query.value(0).toInt();
        qDebug() << "  平均年龄:" << query.value(1).toDouble();
    }

    query.exec("SELECT user_id, SUM(amount) as total FROM orders GROUP BY user_id");
    qDebug() << "\n--- 各用户消费总额 ---";
    while (query.next()) {
        qDebug() << QString("  用户%1: ¥%2")
                    .arg(query.value(0).toInt())
                    .arg(query.value(1).toDouble(), 0, 'f', 2);
    }
}

void updateAndDelete()
{
    qDebug() << "\n=== 更新和删除 ===\n";

    QSqlQuery query;

    // 更新
    query.prepare("UPDATE users SET age = age + 1 WHERE name = ?");
    query.addBindValue("张三");
    if (query.exec()) {
        qDebug() << "更新成功, 影响行数:" << query.numRowsAffected();
    }

    // 验证更新
    query.exec("SELECT name, age FROM users WHERE name = '张三'");
    if (query.next()) {
        qDebug() << "张三现在" << query.value("age").toInt() << "岁";
    }

    // 删除 (演示，不实际删除)
    qDebug() << "\n删除语法: DELETE FROM users WHERE id = ?";
}

void demonstrateTransactions()
{
    qDebug() << "\n=== 事务处理 ===\n";

    QSqlDatabase db = QSqlDatabase::database();
    QSqlQuery query;

    // 开始事务
    db.transaction();
    qDebug() << "事务开始";

    query.exec("INSERT INTO users (name, email, age) VALUES ('临时用户', 'temp@example.com', 20)");
    qDebug() << "插入临时用户";

    // 回滚事务
    db.rollback();
    qDebug() << "事务回滚";

    // 验证回滚
    query.exec("SELECT COUNT(*) FROM users WHERE name = '临时用户'");
    if (query.next()) {
        qDebug() << "临时用户数量:" << query.value(0).toInt() << "(应为0)";
    }

    // 提交事务示例
    qDebug() << "\n提交事务语法: db.commit()";
}

void showRecordInfo()
{
    qDebug() << "\n=== 记录信息 ===\n";

    QSqlQuery query("SELECT * FROM users LIMIT 1");
    QSqlRecord record = query.record();

    qDebug() << "字段数量:" << record.count();
    for (int i = 0; i < record.count(); ++i) {
        qDebug() << QString("  字段%1: %2 (%3)")
                    .arg(i)
                    .arg(record.fieldName(i))
                    .arg(QVariant::typeToName(record.field(i).metaType().id()));
    }
}

int main(int argc, char *argv[])
{
    QCoreApplication app(argc, argv);

    qDebug() << "=== Qt6 SQL 数据库示例 ===";

    showAvailableDrivers();

    if (!createConnection()) {
        return 1;
    }

    createTables();
    insertData();
    queryData();
    updateAndDelete();
    demonstrateTransactions();
    showRecordInfo();

    // 清理
    QSqlDatabase::database().close();
    QFile::remove("demo.db");
    qDebug() << "\n测试数据库已删除";

    return 0;
}
