/**
 * Qt6 基础控件示例
 *
 * Qt Widgets 提供丰富的桌面UI控件：
 * - 按钮类: QPushButton, QCheckBox, QRadioButton
 * - 输入类: QLineEdit, QTextEdit, QSpinBox, QComboBox
 * - 显示类: QLabel, QProgressBar
 * - 容器类: QGroupBox, QTabWidget
 *
 * 官方文档: https://doc.qt.io/qt-6/qtwidgets-index.html
 */

#include <QApplication>
#include <QWidget>
#include <QVBoxLayout>
#include <QHBoxLayout>
#include <QGridLayout>
#include <QGroupBox>
#include <QLabel>
#include <QPushButton>
#include <QCheckBox>
#include <QRadioButton>
#include <QLineEdit>
#include <QTextEdit>
#include <QSpinBox>
#include <QDoubleSpinBox>
#include <QSlider>
#include <QProgressBar>
#include <QComboBox>
#include <QListWidget>
#include <QDateEdit>
#include <QTimeEdit>
#include <QDial>
#include <QDebug>

class BasicWidgetsDemo : public QWidget
{
    Q_OBJECT

public:
    explicit BasicWidgetsDemo(QWidget *parent = nullptr)
        : QWidget(parent)
    {
        setWindowTitle("Qt6 Basic Widgets Demo");
        resize(700, 600);

        QVBoxLayout *mainLayout = new QVBoxLayout(this);

        // 按钮组
        mainLayout->addWidget(createButtonGroup());

        // 输入组
        mainLayout->addWidget(createInputGroup());

        // 选择组
        mainLayout->addWidget(createSelectionGroup());

        // 数值组
        mainLayout->addWidget(createNumericGroup());
    }

private:
    QGroupBox* createButtonGroup()
    {
        QGroupBox *group = new QGroupBox("按钮控件", this);
        QHBoxLayout *layout = new QHBoxLayout(group);

        // 普通按钮
        QPushButton *normalBtn = new QPushButton("普通按钮", this);
        connect(normalBtn, &QPushButton::clicked, []() {
            qDebug() << "普通按钮被点击";
        });

        // 可选中按钮
        QPushButton *toggleBtn = new QPushButton("可选中按钮", this);
        toggleBtn->setCheckable(true);
        connect(toggleBtn, &QPushButton::toggled, [](bool checked) {
            qDebug() << "按钮选中状态:" << checked;
        });

        // 图标按钮
        QPushButton *iconBtn = new QPushButton("带图标", this);
        iconBtn->setIcon(style()->standardIcon(QStyle::SP_DialogOkButton));

        // 复选框
        QCheckBox *checkbox = new QCheckBox("复选框", this);
        connect(checkbox, &QCheckBox::stateChanged, [](int state) {
            qDebug() << "复选框状态:" << state;
        });

        // 三态复选框
        QCheckBox *triStateCheck = new QCheckBox("三态", this);
        triStateCheck->setTristate(true);

        // 单选按钮组
        QWidget *radioGroup = new QWidget(this);
        QHBoxLayout *radioLayout = new QHBoxLayout(radioGroup);
        radioLayout->setContentsMargins(0, 0, 0, 0);
        QRadioButton *radio1 = new QRadioButton("选项A", this);
        QRadioButton *radio2 = new QRadioButton("选项B", this);
        radio1->setChecked(true);
        radioLayout->addWidget(radio1);
        radioLayout->addWidget(radio2);

        layout->addWidget(normalBtn);
        layout->addWidget(toggleBtn);
        layout->addWidget(iconBtn);
        layout->addWidget(checkbox);
        layout->addWidget(triStateCheck);
        layout->addWidget(radioGroup);

        return group;
    }

    QGroupBox* createInputGroup()
    {
        QGroupBox *group = new QGroupBox("输入控件", this);
        QGridLayout *layout = new QGridLayout(group);

        // 单行输入
        layout->addWidget(new QLabel("单行输入:"), 0, 0);
        QLineEdit *lineEdit = new QLineEdit(this);
        lineEdit->setPlaceholderText("请输入文字...");
        connect(lineEdit, &QLineEdit::textChanged, [](const QString &text) {
            qDebug() << "输入:" << text;
        });
        layout->addWidget(lineEdit, 0, 1);

        // 密码输入
        layout->addWidget(new QLabel("密码输入:"), 1, 0);
        QLineEdit *passwordEdit = new QLineEdit(this);
        passwordEdit->setEchoMode(QLineEdit::Password);
        layout->addWidget(passwordEdit, 1, 1);

        // 只读输入
        layout->addWidget(new QLabel("只读:"), 2, 0);
        QLineEdit *readOnlyEdit = new QLineEdit("不可编辑", this);
        readOnlyEdit->setReadOnly(true);
        layout->addWidget(readOnlyEdit, 2, 1);

        // 多行文本
        layout->addWidget(new QLabel("多行文本:"), 3, 0);
        QTextEdit *textEdit = new QTextEdit(this);
        textEdit->setPlaceholderText("支持多行和富文本...");
        textEdit->setMaximumHeight(80);
        layout->addWidget(textEdit, 3, 1);

        return group;
    }

    QGroupBox* createSelectionGroup()
    {
        QGroupBox *group = new QGroupBox("选择控件", this);
        QGridLayout *layout = new QGridLayout(group);

        // 下拉框
        layout->addWidget(new QLabel("下拉框:"), 0, 0);
        QComboBox *combo = new QComboBox(this);
        combo->addItems({"选项一", "选项二", "选项三"});
        connect(combo, &QComboBox::currentIndexChanged, [combo](int index) {
            qDebug() << "选择:" << combo->currentText();
        });
        layout->addWidget(combo, 0, 1);

        // 可编辑下拉框
        layout->addWidget(new QLabel("可编辑:"), 1, 0);
        QComboBox *editableCombo = new QComboBox(this);
        editableCombo->setEditable(true);
        editableCombo->addItems({"预设1", "预设2"});
        layout->addWidget(editableCombo, 1, 1);

        // 日期选择
        layout->addWidget(new QLabel("日期:"), 2, 0);
        QDateEdit *dateEdit = new QDateEdit(QDate::currentDate(), this);
        dateEdit->setCalendarPopup(true);
        layout->addWidget(dateEdit, 2, 1);

        // 时间选择
        layout->addWidget(new QLabel("时间:"), 3, 0);
        QTimeEdit *timeEdit = new QTimeEdit(QTime::currentTime(), this);
        layout->addWidget(timeEdit, 3, 1);

        return group;
    }

    QGroupBox* createNumericGroup()
    {
        QGroupBox *group = new QGroupBox("数值控件", this);
        QGridLayout *layout = new QGridLayout(group);

        // 整数微调框
        layout->addWidget(new QLabel("整数:"), 0, 0);
        QSpinBox *spinBox = new QSpinBox(this);
        spinBox->setRange(0, 100);
        spinBox->setValue(50);
        spinBox->setSuffix(" 个");
        layout->addWidget(spinBox, 0, 1);

        // 浮点微调框
        layout->addWidget(new QLabel("浮点数:"), 1, 0);
        QDoubleSpinBox *doubleSpinBox = new QDoubleSpinBox(this);
        doubleSpinBox->setRange(0.0, 10.0);
        doubleSpinBox->setDecimals(2);
        doubleSpinBox->setSingleStep(0.1);
        layout->addWidget(doubleSpinBox, 1, 1);

        // 滑块
        layout->addWidget(new QLabel("滑块:"), 2, 0);
        QSlider *slider = new QSlider(Qt::Horizontal, this);
        slider->setRange(0, 100);
        slider->setValue(50);
        layout->addWidget(slider, 2, 1);

        // 进度条
        layout->addWidget(new QLabel("进度:"), 3, 0);
        QProgressBar *progressBar = new QProgressBar(this);
        progressBar->setRange(0, 100);
        progressBar->setValue(75);
        layout->addWidget(progressBar, 3, 1);

        // 连接滑块和进度条
        connect(slider, &QSlider::valueChanged, progressBar, &QProgressBar::setValue);

        // 旋钮
        layout->addWidget(new QLabel("旋钮:"), 4, 0);
        QDial *dial = new QDial(this);
        dial->setRange(0, 100);
        dial->setMaximumSize(60, 60);
        connect(dial, &QDial::valueChanged, slider, &QSlider::setValue);
        layout->addWidget(dial, 4, 1, Qt::AlignLeft);

        return group;
    }
};

int main(int argc, char *argv[])
{
    QApplication app(argc, argv);

    qDebug() << "=== Qt6 基础控件示例 ===";
    qDebug() << "控制台会显示控件交互信息\n";

    BasicWidgetsDemo demo;
    demo.show();

    return app.exec();
}

#include "main.moc"
