/**
 * Qt6 SQL 模型示例 - QSqlTableModel, QSqlQueryModel
 *
 * 主要类：
 * - QSqlQueryModel: 只读查询模型，用于显示查询结果
 * - QSqlTableModel: 可编辑的表格模型，直接操作数据库表
 * - QSqlRelationalTableModel: 关联表格模型（本示例未演示）
 *
 * 本示例演示：
 * - QSqlQueryModel 的只读查询显示
 * - QSqlTableModel 的基本 CRUD 操作
 * - 排序、过滤、数据修改
 * - 提交和回滚修改
 *
 * 注意: 虽然不需要显示 GUI，但模型类属于 Qt::Widgets 模块
 *
 * 官方文档:
 * - https://doc.qt.io/qt-6/qsqlquerymodel.html
 * - https://doc.qt.io/qt-6/qsqltablemodel.html
 */

#include <QCoreApplication>
#include <QSqlDatabase>
#include <QSqlQuery>
#include <QSqlQueryModel>
#include <QSqlTableModel>
#include <QSqlRecord>
#include <QSqlError>
#include <QModelIndex>
#include <QVariant>
#include <QDebug>
#include <QFile>

bool createConnection()
{
    QSqlDatabase db = QSqlDatabase::addDatabase("QSQLITE");
    db.setDatabaseName("models_demo.db");

    if (!db.open()) {
        qDebug() << "数据库连接失败:" << db.lastError().text();
        return false;
    }
    return true;
}

void createTableAndData()
{
    QSqlQuery query;

    // 创建产品表
    query.exec("DROP TABLE IF EXISTS products");
    query.exec(R"(
        CREATE TABLE products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT,
            price REAL,
            stock INTEGER DEFAULT 0,
            description TEXT
        )
    )");

    // 插入测试数据
    query.exec("INSERT INTO products (name, category, price, stock, description) VALUES "
               "('iPhone 15', '手机', 5999.00, 100, '苹果最新款手机')");
    query.exec("INSERT INTO products (name, category, price, stock, description) VALUES "
               "('MacBook Pro', '电脑', 14999.00, 50, '专业级笔记本电脑')");
    query.exec("INSERT INTO products (name, category, price, stock, description) VALUES "
               "('iPad Air', '平板', 4799.00, 80, '轻薄平板电脑')");
    query.exec("INSERT INTO products (name, category, price, stock, description) VALUES "
               "('AirPods Pro', '耳机', 1999.00, 200, '降噪耳机')");
    query.exec("INSERT INTO products (name, category, price, stock, description) VALUES "
               "('小米14', '手机', 3999.00, 150, '高性价比旗舰机')");
    query.exec("INSERT INTO products (name, category, price, stock, description) VALUES "
               "('华为Mate60', '手机', 6999.00, 80, '国产高端手机')");

    // 创建订单表用于联表查询演示
    query.exec("DROP TABLE IF EXISTS orders");
    query.exec(R"(
        CREATE TABLE orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER,
            quantity INTEGER,
            order_date DATE,
            customer_name TEXT
        )
    )");

    query.exec("INSERT INTO orders (product_id, quantity, order_date, customer_name) VALUES "
               "(1, 2, '2024-01-15', '客户A')");
    query.exec("INSERT INTO orders (product_id, quantity, order_date, customer_name) VALUES "
               "(2, 1, '2024-01-16', '客户B')");
    query.exec("INSERT INTO orders (product_id, quantity, order_date, customer_name) VALUES "
               "(1, 3, '2024-01-17', '客户C')");
    query.exec("INSERT INTO orders (product_id, quantity, order_date, customer_name) VALUES "
               "(4, 5, '2024-01-18', '客户D')");
}

void demonstrateSqlQueryModel()
{
    qDebug() << "\n=== QSqlQueryModel - 只读查询模型 ===\n";

    // QSqlQueryModel 用于执行任意 SQL 查询并显示结果
    // 它是只读的，不能修改数据

    QSqlQueryModel model;

    // 1. 简单查询
    qDebug() << "--- 所有产品 (简单查询) ---";
    model.setQuery("SELECT name, category, price, stock FROM products");

    // 检查查询是否成功
    if (model.lastError().isValid()) {
        qDebug() << "查询错误:" << model.lastError().text();
        return;
    }

    // 获取记录数
    int rowCount = model.rowCount();
    int colCount = model.columnCount();
    qDebug() << "记录数:" << rowCount << "列数:" << colCount;

    // 打印表头
    QString header;
    for (int col = 0; col < colCount; ++col) {
        header += model.headerData(col, Qt::Horizontal).toString() + "\t";
    }
    qDebug() << header;

    // 遍历数据 - 使用 model.data() 或 model.record()
    for (int row = 0; row < rowCount; ++row) {
        QString line;
        for (int col = 0; col < colCount; ++col) {
            QModelIndex index = model.index(row, col);
            line += model.data(index).toString() + "\t";
        }
        qDebug() << line;
    }

    // 2. 复杂查询 - 联表查询
    qDebug() << "\n--- 订单详情 (联表查询) ---";
    model.setQuery(R"(
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
    )");

    rowCount = model.rowCount();
    qDebug() << "订单记录数:" << rowCount;

    // 打印表头
    header.clear();
    for (int col = 0; col < model.columnCount(); ++col) {
        header += model.headerData(col, Qt::Horizontal).toString() + "\t";
    }
    qDebug() << header;

    // 遍历数据
    for (int row = 0; row < rowCount; ++row) {
        QString line;
        for (int col = 0; col < model.columnCount(); ++col) {
            line += model.data(model.index(row, col)).toString() + "\t";
        }
        qDebug() << line;
    }

    // 3. 聚合查询
    qDebug() << "\n--- 分类统计 (聚合查询) ---";
    model.setQuery(R"(
        SELECT 
            category as 分类,
            COUNT(*) as 产品数,
            AVG(price) as 平均价格,
            SUM(stock) as 总库存
        FROM products
        GROUP BY category
    )");

    for (int row = 0; row < model.rowCount(); ++row) {
        QString category = model.data(model.index(row, 0)).toString();
        int count = model.data(model.index(row, 1)).toInt();
        double avgPrice = model.data(model.index(row, 2)).toDouble();
        int totalStock = model.data(model.index(row, 3)).toInt();
        qDebug() << QString("  %1: %2种产品, 平均价格 ¥%3, 总库存 %4")
                    .arg(category).arg(count).arg(avgPrice, 0, 'f', 2).arg(totalStock);
    }

    // 4. 刷新数据
    qDebug() << "\n--- 刷新数据 ---";
    // 当数据库数据改变时，可以调用 query() 重新执行查询
    model.setQuery(model.query().executedQuery());
    qDebug() << "数据已刷新，当前记录数:" << model.rowCount();
}

void demonstrateSqlTableModel()
{
    qDebug() << "\n=== QSqlTableModel - 可编辑表格模型 ===\n";

    // QSqlTableModel 直接绑定到数据库表
    // 支持读取、编辑、插入、删除操作

    QSqlTableModel model;
    model.setTable("products");

    // 设置编辑策略
    // OnFieldChange: 字段改变立即提交
    // OnRowChange: 行改变时提交 (默认)
    // OnManualSubmit: 手动提交
    model.setEditStrategy(QSqlTableModel::OnManualSubmit);

    // 选择数据
    model.select();

    qDebug() << "--- 原始数据 ---";
    qDebug() << "记录数:" << model.rowCount();

    // 打印数据
    for (int row = 0; row < model.rowCount(); ++row) {
        QSqlRecord record = model.record(row);
        qDebug() << QString("  ID:%1, %2, %3, ¥%4, 库存:%5")
                    .arg(record.value("id").toInt())
                    .arg(record.value("name").toString())
                    .arg(record.value("category").toString())
                    .arg(record.value("price").toDouble(), 0, 'f', 2)
                    .arg(record.value("stock").toInt());
    }

    // 1. 修改数据
    qDebug() << "\n--- 修改数据 ---";
    QModelIndex index = model.index(0, 3); // 第一行，price 列
    double oldPrice = model.data(index).toDouble();
    qDebug() << "修改前 iPhone 15 价格:" << oldPrice;

    model.setData(index, 6299.00);
    qDebug() << "修改后 iPhone 15 价格: 6299.00 (未提交到数据库)";

    // 提交修改
    if (model.submitAll()) {
        qDebug() << "修改已提交到数据库";
    } else {
        qDebug() << "提交失败:" << model.lastError().text();
    }

    // 2. 插入新记录
    qDebug() << "\n--- 插入新记录 ---";
    int newRow = model.rowCount();
    model.insertRow(newRow);

    model.setData(model.index(newRow, 1), "iPhone 15 Pro");  // name
    model.setData(model.index(newRow, 2), "手机");            // category
    model.setData(model.index(newRow, 3), 8999.00);          // price
    model.setData(model.index(newRow, 4), 60);               // stock
    model.setData(model.index(newRow, 5), "专业版手机");       // description

    if (model.submitAll()) {
        qDebug() << "新记录已插入";
        model.select(); // 刷新以获取新ID
    } else {
        qDebug() << "插入失败:" << model.lastError().text();
    }

    // 3. 使用记录方式插入
    qDebug() << "\n--- 使用 QSqlRecord 插入 ---";
    QSqlRecord record = model.record();
    record.setValue("name", "Apple Watch");
    record.setValue("category", "穿戴设备");
    record.setValue("price", 2999.00);
    record.setValue("stock", 120);
    record.setValue("description", "智能手表");

    if (model.insertRecord(-1, record)) {  // -1 表示插入到最后
        model.submitAll();
        qDebug() << "使用 QSqlRecord 插入成功";
    }

    // 4. 删除记录
    qDebug() << "\n--- 删除记录 ---";
    // 删除第一条记录
    model.removeRow(0);
    if (model.submitAll()) {
        qDebug() << "第一条记录已删除";
    }

    // 刷新并显示最终数据
    model.select();
    qDebug() << "\n--- 最终数据 (" << model.rowCount() << "条) ---";
    for (int row = 0; row < model.rowCount(); ++row) {
        QSqlRecord r = model.record(row);
        qDebug() << QString("  %1 (%2): ¥%3, 库存:%4")
                    .arg(r.value("name").toString())
                    .arg(r.value("category").toString())
                    .arg(r.value("price").toDouble(), 0, 'f', 2)
                    .arg(r.value("stock").toInt());
    }
}

void demonstrateFilteringAndSorting()
{
    qDebug() << "\n=== 过滤和排序 ===\n";

    QSqlTableModel model;
    model.setTable("products");
    model.setEditStrategy(QSqlTableModel::OnManualSubmit);

    // 1. 过滤 - 只显示手机
    qDebug() << "--- 过滤: 只显示手机 ---";
    model.setFilter("category = '手机'");
    model.select();

    qDebug() << "手机产品数:" << model.rowCount();
    for (int row = 0; row < model.rowCount(); ++row) {
        QSqlRecord record = model.record(row);
        qDebug() << QString("  %1: ¥%2")
                    .arg(record.value("name").toString())
                    .arg(record.value("price").toDouble(), 0, 'f', 2);
    }

    // 2. 复杂过滤
    qDebug() << "\n--- 过滤: 价格大于5000且库存大于50 ---";
    model.setFilter("price > 5000 AND stock > 50");
    model.select();

    for (int row = 0; row < model.rowCount(); ++row) {
        QSqlRecord record = model.record(row);
        qDebug() << QString("  %1: ¥%2, 库存:%3")
                    .arg(record.value("name").toString())
                    .arg(record.value("price").toDouble(), 0, 'f', 2)
                    .arg(record.value("stock").toInt());
    }

    // 3. 排序
    qDebug() << "\n--- 排序: 按价格降序 ---";
    model.setFilter("");  // 清除过滤
    model.setSort(3, Qt::DescendingOrder);  // 第3列(price)降序
    model.select();

    for (int row = 0; row < model.rowCount(); ++row) {
        QSqlRecord record = model.record(row);
        qDebug() << QString("  %1: ¥%2")
                    .arg(record.value("name").toString())
                    .arg(record.value("price").toDouble(), 0, 'f', 2);
    }

    // 4. 多字段排序
    qDebug() << "\n--- 排序: 先按分类，再按价格 ---";
    model.setSort(2, Qt::AscendingOrder);   // category 升序
    // 注意：QSqlTableModel 只支持单字段排序，多字段需要自定义查询
    // 可以使用 setQuery() 配合自定义 SQL

    // 使用 QSqlQueryModel 实现复杂排序
    QSqlQueryModel queryModel;
    queryModel.setQuery(R"(
        SELECT name, category, price, stock 
        FROM products 
        ORDER BY category ASC, price DESC
    )");

    for (int row = 0; row < queryModel.rowCount(); ++row) {
        qDebug() << QString("  [%1] %2: ¥%3")
                    .arg(queryModel.data(queryModel.index(row, 1)).toString())
                    .arg(queryModel.data(queryModel.index(row, 0)).toString())
                    .arg(queryModel.data(queryModel.index(row, 2)).toDouble(), 0, 'f', 2);
    }
}

void demonstrateBatchOperations()
{
    qDebug() << "\n=== 批量操作和事务 ===\n";

    QSqlTableModel model;
    model.setTable("products");
    model.setEditStrategy(QSqlTableModel::OnManualSubmit);  // 必须设为手动提交
    model.select();

    // 批量修改库存
    qDebug() << "--- 批量修改库存 ---";
    for (int row = 0; row < model.rowCount(); ++row) {
        QSqlRecord record = model.record(row);
        int currentStock = record.value("stock").toInt();
        int newStock = currentStock + 10;  // 所有产品库存 +10

        model.setData(model.index(row, 4), newStock);
        qDebug() << QString("  %1: 库存 %2 -> %3")
                    .arg(record.value("name").toString())
                    .arg(currentStock).arg(newStock);
    }

    // 一次性提交所有修改
    if (model.submitAll()) {
        qDebug() << "\n批量修改已提交";
    } else {
        qDebug() << "\n批量修改失败:" << model.lastError().text();
    }

    // 批量插入
    qDebug() << "\n--- 批量插入 ---";
    QStringList newProducts = {"华为平板", "联想笔记本", "索尼耳机"};
    QStringList categories = {"平板", "电脑", "耳机"};
    QList<double> prices = {3299.00, 6999.00, 2499.00};

    for (int i = 0; i < newProducts.size(); ++i) {
        int row = model.rowCount();
        model.insertRow(row);
        model.setData(model.index(row, 1), newProducts[i]);
        model.setData(model.index(row, 2), categories[i]);
        model.setData(model.index(row, 3), prices[i]);
        model.setData(model.index(row, 4), 50);
    }

    if (model.submitAll()) {
        qDebug() << "批量插入成功: " << newProducts.size() << "条记录";
        model.select();
        qDebug() << "当前总记录数:" << model.rowCount();
    }

    // 回滚示例
    qDebug() << "\n--- 批量回滚示例 ---";
    int originalCount = model.rowCount();
    qDebug() << "当前记录数:" << originalCount;

    // 插入一些临时数据
    model.insertRow(model.rowCount());
    model.setData(model.index(model.rowCount() - 1, 1), "临时产品1");
    model.insertRow(model.rowCount());
    model.setData(model.index(model.rowCount() - 1, 1), "临时产品2");

    qDebug() << "插入2条临时数据后，行数:" << model.rowCount();

    // 回滚 - 使用 revertAll()
    model.revertAll();
    qDebug() << "回滚后，行数:" << model.rowCount() << "(应恢复为" << originalCount << ")";
}

void demonstrateHeaderCustomization()
{
    qDebug() << "\n=== 表头自定义 ===\n";

    QSqlTableModel model;
    model.setTable("products");

    // 自定义表头显示
    model.setHeaderData(0, Qt::Horizontal, "编号");
    model.setHeaderData(1, Qt::Horizontal, "产品名称");
    model.setHeaderData(2, Qt::Horizontal, "分类");
    model.setHeaderData(3, Qt::Horizontal, "价格(元)");
    model.setHeaderData(4, Qt::Horizontal, "库存数量");
    model.setHeaderData(5, Qt::Horizontal, "产品描述");

    model.select();

    // 打印自定义表头
    qDebug() << "自定义表头:";
    for (int col = 0; col < model.columnCount(); ++col) {
        QString header = model.headerData(col, Qt::Horizontal).toString();
        QString original = model.record().fieldName(col);
        qDebug() << QString("  列%1: '%2' (原字段: %3)")
                    .arg(col).arg(header).arg(original);
    }
}

int main(int argc, char *argv[])
{
    QCoreApplication app(argc, argv);

    qDebug() << "=== Qt6 SQL 模型示例 (QSqlQueryModel & QSqlTableModel) ===";

    if (!createConnection()) {
        return 1;
    }

    createTableAndData();

    demonstrateSqlQueryModel();
    demonstrateSqlTableModel();
    demonstrateFilteringAndSorting();
    demonstrateBatchOperations();
    demonstrateHeaderCustomization();

    // 清理
    QSqlDatabase::database().close();
    QFile::remove("models_demo.db");
    qDebug() << "\n测试数据库已删除";

    return 0;
}
