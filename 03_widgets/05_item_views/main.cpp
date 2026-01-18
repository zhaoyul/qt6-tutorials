/**
 * Qt6 模型/视图示例
 *
 * Qt 的模型/视图架构分离数据和表示：
 * - Model: 数据 (QAbstractItemModel 及其子类)
 * - View: 显示 (QListView, QTableView, QTreeView)
 * - Delegate: 渲染和编辑 (QStyledItemDelegate)
 *
 * 便捷类 (包含内置模型):
 * - QListWidget
 * - QTableWidget
 * - QTreeWidget
 *
 * 官方文档: https://doc.qt.io/qt-6/model-view-programming.html
 */

#include <QApplication>
#include <QMainWindow>
#include <QTabWidget>
#include <QVBoxLayout>
#include <QHBoxLayout>
#include <QPushButton>
#include <QListWidget>
#include <QTableWidget>
#include <QTreeWidget>
#include <QListView>
#include <QTableView>
#include <QTreeView>
#include <QStandardItemModel>
#include <QStringListModel>
#include <QSortFilterProxyModel>
#include <QHeaderView>
#include <QLineEdit>
#include <QLabel>
#include <QDebug>

// QListWidget 示例 (便捷类)
QWidget* createListWidgetDemo()
{
    QWidget *widget = new QWidget;
    QVBoxLayout *layout = new QVBoxLayout(widget);

    QListWidget *listWidget = new QListWidget;

    // 添加项目
    listWidget->addItem("普通项目 1");
    listWidget->addItem("普通项目 2");

    // 带图标的项目
    QListWidgetItem *iconItem = new QListWidgetItem(
        QApplication::style()->standardIcon(QStyle::SP_FileIcon),
        "带图标的项目"
    );
    listWidget->addItem(iconItem);

    // 可选中项目
    QListWidgetItem *checkItem = new QListWidgetItem("可选中项目");
    checkItem->setFlags(checkItem->flags() | Qt::ItemIsUserCheckable);
    checkItem->setCheckState(Qt::Unchecked);
    listWidget->addItem(checkItem);

    // 不同颜色
    QListWidgetItem *colorItem = new QListWidgetItem("彩色项目");
    colorItem->setForeground(Qt::blue);
    colorItem->setBackground(QColor(255, 255, 200));
    listWidget->addItem(colorItem);

    // 设置选择模式
    listWidget->setSelectionMode(QAbstractItemView::ExtendedSelection);

    // 信号连接
    QObject::connect(listWidget, &QListWidget::itemClicked,
                     [](QListWidgetItem *item) {
                         qDebug() << "点击:" << item->text();
                     });

    layout->addWidget(new QLabel("QListWidget - 便捷列表控件"));
    layout->addWidget(listWidget);

    // 操作按钮
    QHBoxLayout *btnLayout = new QHBoxLayout;
    QPushButton *addBtn = new QPushButton("添加");
    QPushButton *removeBtn = new QPushButton("删除选中");

    QObject::connect(addBtn, &QPushButton::clicked, [listWidget]() {
        listWidget->addItem(QString("新项目 %1").arg(listWidget->count() + 1));
    });

    QObject::connect(removeBtn, &QPushButton::clicked, [listWidget]() {
        qDeleteAll(listWidget->selectedItems());
    });

    btnLayout->addWidget(addBtn);
    btnLayout->addWidget(removeBtn);
    layout->addLayout(btnLayout);

    return widget;
}

// QTableWidget 示例 (便捷类)
QWidget* createTableWidgetDemo()
{
    QWidget *widget = new QWidget;
    QVBoxLayout *layout = new QVBoxLayout(widget);

    QTableWidget *tableWidget = new QTableWidget(5, 4);

    // 设置表头
    tableWidget->setHorizontalHeaderLabels({"姓名", "年龄", "城市", "职业"});

    // 填充数据
    QStringList names = {"张三", "李四", "王五", "赵六", "钱七"};
    QStringList ages = {"25", "30", "28", "35", "22"};
    QStringList cities = {"北京", "上海", "广州", "深圳", "杭州"};
    QStringList jobs = {"工程师", "设计师", "产品经理", "数据分析", "运营"};

    for (int row = 0; row < 5; ++row) {
        tableWidget->setItem(row, 0, new QTableWidgetItem(names[row]));
        tableWidget->setItem(row, 1, new QTableWidgetItem(ages[row]));
        tableWidget->setItem(row, 2, new QTableWidgetItem(cities[row]));
        tableWidget->setItem(row, 3, new QTableWidgetItem(jobs[row]));
    }

    // 设置列宽
    tableWidget->horizontalHeader()->setStretchLastSection(true);
    tableWidget->horizontalHeader()->setSectionResizeMode(QHeaderView::Interactive);

    // 启用排序
    tableWidget->setSortingEnabled(true);

    // 交替行颜色
    tableWidget->setAlternatingRowColors(true);

    // 选择整行
    tableWidget->setSelectionBehavior(QAbstractItemView::SelectRows);

    layout->addWidget(new QLabel("QTableWidget - 便捷表格控件"));
    layout->addWidget(tableWidget);

    return widget;
}

// QTreeWidget 示例 (便捷类)
QWidget* createTreeWidgetDemo()
{
    QWidget *widget = new QWidget;
    QVBoxLayout *layout = new QVBoxLayout(widget);

    QTreeWidget *treeWidget = new QTreeWidget;
    treeWidget->setHeaderLabels({"名称", "类型", "大小"});
    treeWidget->setColumnCount(3);

    // 根节点
    QTreeWidgetItem *root1 = new QTreeWidgetItem(treeWidget, {"项目A", "文件夹", ""});
    QTreeWidgetItem *root2 = new QTreeWidgetItem(treeWidget, {"项目B", "文件夹", ""});

    // 子节点
    new QTreeWidgetItem(root1, {"main.cpp", "C++ 源文件", "10 KB"});
    new QTreeWidgetItem(root1, {"main.h", "C++ 头文件", "2 KB"});

    QTreeWidgetItem *subFolder = new QTreeWidgetItem(root1, {"src", "文件夹", ""});
    new QTreeWidgetItem(subFolder, {"utils.cpp", "C++ 源文件", "5 KB"});
    new QTreeWidgetItem(subFolder, {"utils.h", "C++ 头文件", "1 KB"});

    new QTreeWidgetItem(root2, {"readme.md", "Markdown", "3 KB"});
    new QTreeWidgetItem(root2, {"config.json", "JSON", "1 KB"});

    // 展开所有
    treeWidget->expandAll();

    // 调整列宽
    treeWidget->header()->setSectionResizeMode(0, QHeaderView::Stretch);

    layout->addWidget(new QLabel("QTreeWidget - 便捷树形控件"));
    layout->addWidget(treeWidget);

    return widget;
}

// 模型/视图分离示例
QWidget* createModelViewDemo()
{
    QWidget *widget = new QWidget;
    QVBoxLayout *layout = new QVBoxLayout(widget);

    layout->addWidget(new QLabel("Model/View 分离 - 一个模型，多个视图"));

    // 创建共享模型
    QStandardItemModel *model = new QStandardItemModel(widget);

    // 填充数据
    QStringList items = {"苹果", "香蕉", "橙子", "葡萄", "西瓜"};
    for (const QString &item : items) {
        QStandardItem *stdItem = new QStandardItem(item);
        stdItem->setIcon(QApplication::style()->standardIcon(QStyle::SP_FileIcon));
        model->appendRow(stdItem);
    }

    // 创建视图
    QHBoxLayout *viewLayout = new QHBoxLayout;

    QListView *listView = new QListView;
    listView->setModel(model);

    QListView *iconView = new QListView;
    iconView->setModel(model);
    iconView->setViewMode(QListView::IconMode);
    iconView->setGridSize(QSize(80, 80));

    viewLayout->addWidget(listView);
    viewLayout->addWidget(iconView);

    layout->addLayout(viewLayout);

    // 说明
    layout->addWidget(new QLabel("两个视图共享同一个模型，修改会同步"));

    return widget;
}

// 代理排序/过滤示例
QWidget* createProxyModelDemo()
{
    QWidget *widget = new QWidget;
    QVBoxLayout *layout = new QVBoxLayout(widget);

    // 搜索框
    QLineEdit *searchEdit = new QLineEdit;
    searchEdit->setPlaceholderText("输入搜索关键词...");
    layout->addWidget(searchEdit);

    // 源模型
    QStringListModel *sourceModel = new QStringListModel(widget);
    sourceModel->setStringList({
        "Apple", "Apricot", "Banana", "Blueberry", "Cherry",
        "Date", "Fig", "Grape", "Kiwi", "Lemon",
        "Mango", "Orange", "Peach", "Pear", "Plum"
    });

    // 代理模型 (用于过滤和排序)
    QSortFilterProxyModel *proxyModel = new QSortFilterProxyModel(widget);
    proxyModel->setSourceModel(sourceModel);
    proxyModel->setFilterCaseSensitivity(Qt::CaseInsensitive);

    // 连接搜索框
    QObject::connect(searchEdit, &QLineEdit::textChanged, [proxyModel](const QString &text) {
        proxyModel->setFilterRegularExpression(text);
    });

    // 视图
    QListView *listView = new QListView;
    listView->setModel(proxyModel);

    layout->addWidget(new QLabel("QSortFilterProxyModel - 过滤和排序"));
    layout->addWidget(listView);

    return widget;
}

int main(int argc, char *argv[])
{
    QApplication app(argc, argv);

    qDebug() << "=== Qt6 模型/视图示例 ===\n";

    QMainWindow mainWindow;
    mainWindow.setWindowTitle("Qt6 Model/View Demo");
    mainWindow.resize(700, 500);

    QTabWidget *tabWidget = new QTabWidget;
    tabWidget->addTab(createListWidgetDemo(), "ListWidget");
    tabWidget->addTab(createTableWidgetDemo(), "TableWidget");
    tabWidget->addTab(createTreeWidgetDemo(), "TreeWidget");
    tabWidget->addTab(createModelViewDemo(), "Model/View");
    tabWidget->addTab(createProxyModelDemo(), "ProxyModel");

    mainWindow.setCentralWidget(tabWidget);
    mainWindow.show();

    return app.exec();
}
