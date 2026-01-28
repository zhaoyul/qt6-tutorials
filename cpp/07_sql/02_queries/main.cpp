/**
 * Qt6 SQL 查询示例 - QSqlQuery
 *
 * 主要类：
 * - QSqlQuery: SQL 查询执行
 * - QSqlError: 错误处理
 *
 * 本示例演示：
 * - INSERT 插入数据（多种参数绑定方式）
 * - UPDATE 更新数据
 * - DELETE 删除数据
 * - SELECT 查询数据
 * - 批量操作
 * - 事务处理
 *
 * 官方文档: https://doc.qt.io/qt-6/sql-sqlstatements.html
 */

#include <QCoreApplication>
#include <QSqlDatabase>
#include <QSqlQuery>
#include <QSqlError>
#include <QVariant>
#include <QDebug>
#include <QFile>

bool createConnection()
{
    QSqlDatabase db = QSqlDatabase::addDatabase("QSQLITE");
    db.setDatabaseName("queries_demo.db");

    if (!db.open()) {
        qDebug() << "数据库连接失败:" << db.lastError().text();
        return false;
    }
    return true;
}

void createTable()
{
    QSqlQuery query;
    query.exec("DROP TABLE IF EXISTS employees");
    query.exec(R"(
        CREATE TABLE employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            department TEXT,
            salary REAL,
            hire_date DATE
        )
    )");
}

void demonstrateInsert()
{
    qDebug() << "\n=== INSERT 插入数据 ===\n";

    QSqlQuery query;

    // 方式1: 直接执行 SQL 语句
    query.exec("INSERT INTO employees (name, department, salary, hire_date) "
               "VALUES ('张三', '技术部', 15000.00, '2023-01-15')");
    qDebug() << "直接执行: 插入张三, ID:" << query.lastInsertId().toInt();

    // 方式2: 位置参数绑定 (?) - 防止 SQL 注入
    query.prepare("INSERT INTO employees (name, department, salary, hire_date) VALUES (?, ?, ?, ?)");
    query.addBindValue("李四");
    query.addBindValue("市场部");
    query.addBindValue(12000.00);
    query.addBindValue("2023-03-20");
    query.exec();
    qDebug() << "位置参数绑定: 插入李四, ID:" << query.lastInsertId().toInt();

    // 方式3: 命名参数绑定 (:name) - 更清晰易读
    query.prepare("INSERT INTO employees (name, department, salary, hire_date) "
                  "VALUES (:name, :dept, :salary, :hire_date)");
    query.bindValue(":name", "王五");
    query.bindValue(":dept", "财务部");
    query.bindValue(":salary", 13000.00);
    query.bindValue(":hire_date", "2023-06-10");
    query.exec();
    qDebug() << "命名参数绑定: 插入王五, ID:" << query.lastInsertId().toInt();

    // 方式4: 批量插入 - 使用 bindValue 设置参数值
    query.prepare("INSERT INTO employees (name, department, salary, hire_date) VALUES (?, ?, ?, ?)");

    QVariantList names;
    names << "赵六" << "孙七" << "周八";
    QVariantList departments;
    departments << "技术部" << "人事部" << "技术部";
    QVariantList salaries;
    salaries << 18000.00 << 9000.00 << 16000.00;
    QVariantList hireDates;
    hireDates << "2023-08-01" << "2023-09-15" << "2023-11-20";

    query.addBindValue(names);
    query.addBindValue(departments);
    query.addBindValue(salaries);
    query.addBindValue(hireDates);

    if (query.execBatch()) {
        qDebug() << "批量插入成功: 插入了" << names.size() << "条记录";
    } else {
        qDebug() << "批量插入失败:" << query.lastError().text();
    }
}

void demonstrateSelect()
{
    qDebug() << "\n=== SELECT 查询数据 ===\n";

    QSqlQuery query;

    // 1. 简单查询 - 查询所有员工
    qDebug() << "--- 所有员工 ---";
    query.exec("SELECT id, name, department, salary FROM employees");
    while (query.next()) {
        int id = query.value(0).toInt();                    // 通过索引获取
        QString name = query.value("name").toString();      // 通过字段名获取
        QString dept = query.value("department").toString();
        double salary = query.value("salary").toDouble();
        qDebug() << QString("  ID:%1, 姓名:%2, 部门:%3, 薪资:%4")
                    .arg(id).arg(name).arg(dept).arg(salary, 0, 'f', 2);
    }

    // 2. 条件查询 - 使用参数绑定
    qDebug() << "\n--- 技术部员工 (参数绑定) ---";
    query.prepare("SELECT name, salary FROM employees WHERE department = :dept AND salary > :min_salary");
    query.bindValue(":dept", "技术部");
    query.bindValue(":min_salary", 15000.00);
    query.exec();
    while (query.next()) {
        qDebug() << QString("  %1: ¥%2")
                    .arg(query.value("name").toString())
                    .arg(query.value("salary").toDouble(), 0, 'f', 2);
    }

    // 3. 模糊查询 - LIKE
    qDebug() << "\n--- 姓名包含 '三' 的员工 ---";
    query.prepare("SELECT name, department FROM employees WHERE name LIKE :pattern");
    query.bindValue(":pattern", "%三%");
    query.exec();
    while (query.next()) {
        qDebug() << QString("  %1 - %2")
                    .arg(query.value("name").toString())
                    .arg(query.value("department").toString());
    }

    // 4. 聚合查询
    qDebug() << "\n--- 部门统计 ---";
    query.exec("SELECT department, COUNT(*) as cnt, AVG(salary) as avg_salary "
               "FROM employees GROUP BY department ORDER BY avg_salary DESC");
    while (query.next()) {
        qDebug() << QString("  %1: %2人, 平均薪资 ¥%3")
                    .arg(query.value("department").toString())
                    .arg(query.value("cnt").toInt())
                    .arg(query.value("avg_salary").toDouble(), 0, 'f', 2);
    }

    // 5. 排序和分页
    qDebug() << "\n--- 薪资最高的3名员工 ---";
    query.exec("SELECT name, salary FROM employees ORDER BY salary DESC LIMIT 3");
    int rank = 1;
    while (query.next()) {
        qDebug() << QString("  第%1名: %2 - ¥%3")
                    .arg(rank++)
                    .arg(query.value("name").toString())
                    .arg(query.value("salary").toDouble(), 0, 'f', 2);
    }
}

void demonstrateUpdate()
{
    qDebug() << "\n=== UPDATE 更新数据 ===\n";

    QSqlQuery query;

    // 更新前查询
    qDebug() << "更新前:";
    query.exec("SELECT name, salary FROM employees WHERE name = '张三'");
    if (query.next()) {
        qDebug() << QString("  %1 当前薪资: ¥%2")
                    .arg(query.value("name").toString())
                    .arg(query.value("salary").toDouble(), 0, 'f', 2);
    }

    // 方式1: 直接更新
    query.exec("UPDATE employees SET salary = salary + 2000 WHERE name = '张三'");
    qDebug() << "直接更新: 张三加薪2000, 影响行数:" << query.numRowsAffected();

    // 方式2: 参数绑定更新
    query.prepare("UPDATE employees SET salary = :new_salary, department = :new_dept WHERE id = :id");
    query.bindValue(":new_salary", 14000.00);
    query.bindValue(":new_dept", "研发部");
    query.bindValue(":id", 2);
    if (query.exec()) {
        qDebug() << "参数绑定更新: 李四信息更新, 影响行数:" << query.numRowsAffected();
    }

    // 批量更新
    query.prepare("UPDATE employees SET salary = salary * 1.1 WHERE department = ?");
    query.addBindValue("技术部");
    query.exec();
    qDebug() << "批量更新: 技术部全员涨薪10%, 影响行数:" << query.numRowsAffected();

    // 更新后查询
    qDebug() << "\n更新后所有员工:";
    query.exec("SELECT name, department, salary FROM employees ORDER BY id");
    while (query.next()) {
        qDebug() << QString("  %1 (%2): ¥%3")
                    .arg(query.value("name").toString())
                    .arg(query.value("department").toString())
                    .arg(query.value("salary").toDouble(), 0, 'f', 2);
    }
}

void demonstrateDelete()
{
    qDebug() << "\n=== DELETE 删除数据 ===\n";

    QSqlQuery query;

    // 删除前统计
    query.exec("SELECT COUNT(*) FROM employees");
    if (query.next()) {
        qDebug() << "删除前员工总数:" << query.value(0).toInt();
    }

    // 方式1: 直接删除
    query.exec("DELETE FROM employees WHERE name = '周八'");
    qDebug() << "直接删除: 删除周八, 影响行数:" << query.numRowsAffected();

    // 方式2: 参数绑定删除
    query.prepare("DELETE FROM employees WHERE salary < :min_salary");
    query.bindValue(":min_salary", 10000.00);
    if (query.exec()) {
        qDebug() << "条件删除: 删除薪资低于10000的员工, 影响行数:" << query.numRowsAffected();
    }

    // 删除后统计
    query.exec("SELECT COUNT(*) FROM employees");
    if (query.next()) {
        qDebug() << "删除后员工总数:" << query.value(0).toInt();
    }
}

void demonstrateTransaction()
{
    qDebug() << "\n=== 事务中的增删改查 ===\n";

    QSqlDatabase db = QSqlDatabase::database();
    QSqlQuery query;

    // 事务回滚示例
    qDebug() << "--- 事务回滚示例 ---";
    db.transaction();
    qDebug() << "事务开始";

    query.exec("INSERT INTO employees (name, department, salary) VALUES ('临时员工1', '测试部', 5000)");
    qDebug() << "插入临时员工1";

    query.exec("INSERT INTO employees (name, department, salary) VALUES ('临时员工2', '测试部', 6000)");
    qDebug() << "插入临时员工2";

    query.exec("UPDATE employees SET salary = salary + 1000 WHERE department = '测试部'");
    qDebug() << "更新测试部薪资";

    db.rollback();
    qDebug() << "事务回滚 - 所有操作撤销";

    // 验证回滚
    query.exec("SELECT COUNT(*) FROM employees WHERE department = '测试部'");
    if (query.next()) {
        qDebug() << "测试部员工数:" << query.value(0).toInt() << "(应为0)";
    }

    // 事务提交示例
    qDebug() << "\n--- 事务提交示例 ---";
    db.transaction();
    qDebug() << "事务开始";

    query.prepare("INSERT INTO employees (name, department, salary, hire_date) VALUES (?, ?, ?, ?)");
    query.addBindValue("新员工A");
    query.addBindValue("产品部");
    query.addBindValue(11000.00);
    query.addBindValue("2024-01-01");
    query.exec();
    qDebug() << "插入新员工A";

    query.prepare("INSERT INTO employees (name, department, salary, hire_date) VALUES (?, ?, ?, ?)");
    query.addBindValue("新员工B");
    query.addBindValue("产品部");
    query.addBindValue(12000.00);
    query.addBindValue("2024-01-01");
    query.exec();
    qDebug() << "插入新员工B";

    db.commit();
    qDebug() << "事务提交 - 所有操作生效";

    // 验证提交
    query.exec("SELECT COUNT(*) FROM employees WHERE department = '产品部'");
    if (query.next()) {
        qDebug() << "产品部员工数:" << query.value(0).toInt() << "(应为2)";
    }
}

void demonstrateErrorHandling()
{
    qDebug() << "\n=== 错误处理 ===\n";

    QSqlQuery query;

    // 尝试执行错误的 SQL
    if (!query.exec("SELECT * FROM non_existent_table")) {
        qDebug() << "查询失败:";
        qDebug() << "  错误文本:" << query.lastError().text();
        qDebug() << "  错误类型:" << query.lastError().type();
        qDebug() << "  数据库错误:" << query.lastError().databaseText();
    }

    // 违反约束错误
    query.prepare("INSERT INTO employees (name, department, salary) VALUES (:name, :dept, :salary)");
    query.bindValue(":name", QVariant());  // NULL 值
    query.bindValue(":dept", "测试部");
    query.bindValue(":salary", 10000.00);
    if (!query.exec()) {
        qDebug() << "\n插入失败 (name 为 NULL):" << query.lastError().text();
    }
}

int main(int argc, char *argv[])
{
    QCoreApplication app(argc, argv);

    qDebug() << "=== Qt6 SQL 查询示例 (QSqlQuery) ===";

    if (!createConnection()) {
        return 1;
    }

    createTable();
    demonstrateInsert();
    demonstrateSelect();
    demonstrateUpdate();
    demonstrateDelete();
    demonstrateTransaction();
    demonstrateErrorHandling();

    // 清理
    QSqlDatabase::database().close();
    QFile::remove("queries_demo.db");
    qDebug() << "\n测试数据库已删除";

    return 0;
}
