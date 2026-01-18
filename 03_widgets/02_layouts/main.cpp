/**
 * Qt6 布局管理示例
 *
 * 布局管理器自动排列控件：
 * - QVBoxLayout: 垂直布局
 * - QHBoxLayout: 水平布局
 * - QGridLayout: 网格布局
 * - QFormLayout: 表单布局
 * - QStackedLayout: 堆叠布局
 *
 * 重要概念：
 * - 伸缩因子 (Stretch)
 * - 间距 (Spacing)
 * - 边距 (Margin)
 * - 尺寸策略 (Size Policy)
 *
 * 官方文档: https://doc.qt.io/qt-6/layout.html
 */

#include <QApplication>
#include <QWidget>
#include <QVBoxLayout>
#include <QHBoxLayout>
#include <QGridLayout>
#include <QFormLayout>
#include <QStackedLayout>
#include <QPushButton>
#include <QLabel>
#include <QLineEdit>
#include <QTextEdit>
#include <QGroupBox>
#include <QTabWidget>
#include <QSplitter>
#include <QFrame>
#include <QDebug>

// 创建带颜色背景的标签 (便于观察布局)
QLabel* createColorLabel(const QString &text, const QString &color)
{
    QLabel *label = new QLabel(text);
    label->setStyleSheet(QString("background-color: %1; padding: 10px; border: 1px solid gray;").arg(color));
    label->setAlignment(Qt::AlignCenter);
    return label;
}

// 垂直布局示例
QWidget* createVBoxDemo()
{
    QWidget *widget = new QWidget;
    QVBoxLayout *layout = new QVBoxLayout(widget);

    layout->addWidget(createColorLabel("Item 1", "#ffcccc"));
    layout->addWidget(createColorLabel("Item 2", "#ccffcc"));
    layout->addWidget(createColorLabel("Item 3 (Stretch 2)", "#ccccff"));

    // 设置伸缩因子
    layout->setStretch(2, 2);  // 第三个控件占2份

    // 添加弹性空间
    layout->addStretch(1);

    layout->addWidget(createColorLabel("Bottom Item", "#ffccff"));

    return widget;
}

// 水平布局示例
QWidget* createHBoxDemo()
{
    QWidget *widget = new QWidget;
    QHBoxLayout *layout = new QHBoxLayout(widget);

    layout->addWidget(createColorLabel("Left", "#ffcccc"));
    layout->addStretch(1);  // 中间弹性空间
    layout->addWidget(createColorLabel("Center", "#ccffcc"));
    layout->addStretch(1);
    layout->addWidget(createColorLabel("Right", "#ccccff"));

    return widget;
}

// 网格布局示例
QWidget* createGridDemo()
{
    QWidget *widget = new QWidget;
    QGridLayout *layout = new QGridLayout(widget);

    // 基本网格
    layout->addWidget(createColorLabel("(0,0)", "#ffcccc"), 0, 0);
    layout->addWidget(createColorLabel("(0,1)", "#ccffcc"), 0, 1);
    layout->addWidget(createColorLabel("(0,2)", "#ccccff"), 0, 2);

    layout->addWidget(createColorLabel("(1,0)", "#ffffcc"), 1, 0);
    layout->addWidget(createColorLabel("(1,1-2) 跨列", "#ffccff"), 1, 1, 1, 2);  // 跨2列

    layout->addWidget(createColorLabel("(2-3,0) 跨行", "#ccffff"), 2, 0, 2, 1);  // 跨2行
    layout->addWidget(createColorLabel("(2,1)", "#ffd700"), 2, 1);
    layout->addWidget(createColorLabel("(2,2)", "#98fb98"), 2, 2);
    layout->addWidget(createColorLabel("(3,1)", "#dda0dd"), 3, 1);
    layout->addWidget(createColorLabel("(3,2)", "#f0e68c"), 3, 2);

    // 设置列伸缩
    layout->setColumnStretch(1, 1);
    layout->setColumnStretch(2, 2);

    return widget;
}

// 表单布局示例
QWidget* createFormDemo()
{
    QWidget *widget = new QWidget;
    QFormLayout *layout = new QFormLayout(widget);

    layout->addRow("用户名:", new QLineEdit);
    layout->addRow("密码:", new QLineEdit);
    layout->addRow("邮箱:", new QLineEdit);

    QTextEdit *bio = new QTextEdit;
    bio->setMaximumHeight(80);
    layout->addRow("简介:", bio);

    // 表单布局选项
    layout->setLabelAlignment(Qt::AlignRight);
    layout->setFormAlignment(Qt::AlignLeft | Qt::AlignTop);

    return widget;
}

// 嵌套布局示例
QWidget* createNestedDemo()
{
    QWidget *widget = new QWidget;
    QVBoxLayout *mainLayout = new QVBoxLayout(widget);

    // 顶部水平布局
    QHBoxLayout *topLayout = new QHBoxLayout;
    topLayout->addWidget(createColorLabel("Logo", "#ffcccc"));
    topLayout->addStretch();
    topLayout->addWidget(new QPushButton("按钮1"));
    topLayout->addWidget(new QPushButton("按钮2"));
    mainLayout->addLayout(topLayout);

    // 中间区域
    QHBoxLayout *middleLayout = new QHBoxLayout;

    // 左侧菜单
    QVBoxLayout *leftLayout = new QVBoxLayout;
    leftLayout->addWidget(new QPushButton("菜单1"));
    leftLayout->addWidget(new QPushButton("菜单2"));
    leftLayout->addWidget(new QPushButton("菜单3"));
    leftLayout->addStretch();
    middleLayout->addLayout(leftLayout);

    // 右侧内容
    QTextEdit *content = new QTextEdit("内容区域");
    middleLayout->addWidget(content, 1);

    mainLayout->addLayout(middleLayout, 1);

    // 底部状态栏
    mainLayout->addWidget(createColorLabel("状态栏", "#cccccc"));

    return widget;
}

// 分割器示例
QWidget* createSplitterDemo()
{
    QSplitter *splitter = new QSplitter(Qt::Horizontal);

    QTextEdit *left = new QTextEdit("左侧面板\n\n拖动分割线调整大小");
    QTextEdit *middle = new QTextEdit("中间面板");
    QTextEdit *right = new QTextEdit("右侧面板");

    splitter->addWidget(left);
    splitter->addWidget(middle);
    splitter->addWidget(right);

    // 设置初始大小比例
    splitter->setSizes({100, 200, 100});

    // 设置手柄宽度
    splitter->setHandleWidth(5);

    return splitter;
}

// 尺寸策略示例
QWidget* createSizePolicyDemo()
{
    QWidget *widget = new QWidget;
    QVBoxLayout *layout = new QVBoxLayout(widget);

    // Fixed: 固定大小
    QPushButton *fixedBtn = new QPushButton("Fixed (固定大小)");
    fixedBtn->setSizePolicy(QSizePolicy::Fixed, QSizePolicy::Fixed);
    layout->addWidget(fixedBtn);

    // Minimum: 最小大小
    QPushButton *minBtn = new QPushButton("Minimum");
    minBtn->setSizePolicy(QSizePolicy::Minimum, QSizePolicy::Fixed);
    layout->addWidget(minBtn);

    // Expanding: 尽量扩展
    QPushButton *expandBtn = new QPushButton("Expanding (扩展)");
    expandBtn->setSizePolicy(QSizePolicy::Expanding, QSizePolicy::Expanding);
    layout->addWidget(expandBtn);

    // 说明
    QLabel *info = new QLabel(
        "尺寸策略:\n"
        "• Fixed: 固定为sizeHint\n"
        "• Minimum: 最小为sizeHint，可以扩大\n"
        "• Maximum: 最大为sizeHint，可以缩小\n"
        "• Preferred: 最佳为sizeHint，可调整\n"
        "• Expanding: 尽量扩展\n"
        "• Ignored: 忽略sizeHint"
    );
    info->setStyleSheet("background-color: #f0f0f0; padding: 10px;");
    layout->addWidget(info);

    return widget;
}

int main(int argc, char *argv[])
{
    QApplication app(argc, argv);

    qDebug() << "=== Qt6 布局管理示例 ===\n";

    QTabWidget *tabWidget = new QTabWidget;
    tabWidget->setWindowTitle("Qt6 Layouts Demo");
    tabWidget->resize(600, 500);

    tabWidget->addTab(createVBoxDemo(), "VBox 垂直");
    tabWidget->addTab(createHBoxDemo(), "HBox 水平");
    tabWidget->addTab(createGridDemo(), "Grid 网格");
    tabWidget->addTab(createFormDemo(), "Form 表单");
    tabWidget->addTab(createNestedDemo(), "嵌套布局");
    tabWidget->addTab(createSplitterDemo(), "分割器");
    tabWidget->addTab(createSizePolicyDemo(), "尺寸策略");

    tabWidget->show();

    return app.exec();
}
