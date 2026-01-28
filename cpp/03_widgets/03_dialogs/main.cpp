/**
 * Qt6 对话框示例
 *
 * 标准对话框：
 * - QMessageBox: 消息框
 * - QFileDialog: 文件对话框
 * - QColorDialog: 颜色对话框
 * - QFontDialog: 字体对话框
 * - QInputDialog: 输入对话框
 * - QProgressDialog: 进度对话框
 *
 * 自定义对话框：
 * - 继承 QDialog
 * - 模态 vs 非模态
 *
 * 官方文档: https://doc.qt.io/qt-6/dialogs.html
 */

#include <QApplication>
#include <QWidget>
#include <QVBoxLayout>
#include <QPushButton>
#include <QLabel>
#include <QMessageBox>
#include <QFileDialog>
#include <QColorDialog>
#include <QFontDialog>
#include <QInputDialog>
#include <QProgressDialog>
#include <QDialog>
#include <QDialogButtonBox>
#include <QLineEdit>
#include <QFormLayout>
#include <QTimer>
#include <QThread>
#include <QDebug>

// 自定义对话框
class CustomDialog : public QDialog
{
    Q_OBJECT

public:
    explicit CustomDialog(QWidget *parent = nullptr)
        : QDialog(parent)
    {
        setWindowTitle("自定义对话框");
        setModal(true);

        QVBoxLayout *layout = new QVBoxLayout(this);

        // 表单内容
        QFormLayout *form = new QFormLayout;
        m_nameEdit = new QLineEdit(this);
        m_emailEdit = new QLineEdit(this);
        form->addRow("姓名:", m_nameEdit);
        form->addRow("邮箱:", m_emailEdit);
        layout->addLayout(form);

        // 标准按钮
        QDialogButtonBox *buttonBox = new QDialogButtonBox(
            QDialogButtonBox::Ok | QDialogButtonBox::Cancel, this);
        connect(buttonBox, &QDialogButtonBox::accepted, this, &QDialog::accept);
        connect(buttonBox, &QDialogButtonBox::rejected, this, &QDialog::reject);
        layout->addWidget(buttonBox);
    }

    QString name() const { return m_nameEdit->text(); }
    QString email() const { return m_emailEdit->text(); }

private:
    QLineEdit *m_nameEdit;
    QLineEdit *m_emailEdit;
};

class DialogsDemo : public QWidget
{
    Q_OBJECT

public:
    explicit DialogsDemo(QWidget *parent = nullptr)
        : QWidget(parent)
    {
        setWindowTitle("Qt6 Dialogs Demo");
        resize(400, 500);

        QVBoxLayout *layout = new QVBoxLayout(this);

        m_resultLabel = new QLabel("结果将显示在这里", this);
        m_resultLabel->setStyleSheet("background-color: #f0f0f0; padding: 10px;");
        m_resultLabel->setWordWrap(true);
        layout->addWidget(m_resultLabel);

        // 消息框按钮
        layout->addWidget(createButton("信息框", [this]() { showInfoDialog(); }));
        layout->addWidget(createButton("警告框", [this]() { showWarningDialog(); }));
        layout->addWidget(createButton("错误框", [this]() { showErrorDialog(); }));
        layout->addWidget(createButton("确认框", [this]() { showQuestionDialog(); }));

        // 选择对话框
        layout->addWidget(createButton("打开文件", [this]() { showFileOpenDialog(); }));
        layout->addWidget(createButton("保存文件", [this]() { showFileSaveDialog(); }));
        layout->addWidget(createButton("选择目录", [this]() { showDirectoryDialog(); }));
        layout->addWidget(createButton("选择颜色", [this]() { showColorDialog(); }));
        layout->addWidget(createButton("选择字体", [this]() { showFontDialog(); }));

        // 输入对话框
        layout->addWidget(createButton("输入文本", [this]() { showTextInputDialog(); }));
        layout->addWidget(createButton("输入数字", [this]() { showIntInputDialog(); }));
        layout->addWidget(createButton("选择项目", [this]() { showItemInputDialog(); }));

        // 进度对话框
        layout->addWidget(createButton("进度对话框", [this]() { showProgressDialog(); }));

        // 自定义对话框
        layout->addWidget(createButton("自定义对话框", [this]() { showCustomDialog(); }));

        layout->addStretch();
    }

private:
    QPushButton* createButton(const QString &text, std::function<void()> callback)
    {
        QPushButton *btn = new QPushButton(text, this);
        connect(btn, &QPushButton::clicked, callback);
        return btn;
    }

    void showInfoDialog()
    {
        QMessageBox::information(this, "信息", "这是一条信息消息。");
        m_resultLabel->setText("显示了信息框");
    }

    void showWarningDialog()
    {
        QMessageBox::warning(this, "警告", "这是一条警告消息！");
        m_resultLabel->setText("显示了警告框");
    }

    void showErrorDialog()
    {
        QMessageBox::critical(this, "错误", "发生了一个错误！");
        m_resultLabel->setText("显示了错误框");
    }

    void showQuestionDialog()
    {
        QMessageBox::StandardButton result = QMessageBox::question(
            this, "确认",
            "你确定要继续吗？",
            QMessageBox::Yes | QMessageBox::No | QMessageBox::Cancel,
            QMessageBox::No  // 默认按钮
        );

        QString text;
        switch (result) {
            case QMessageBox::Yes: text = "选择了: Yes"; break;
            case QMessageBox::No: text = "选择了: No"; break;
            case QMessageBox::Cancel: text = "选择了: Cancel"; break;
            default: text = "未知";
        }
        m_resultLabel->setText(text);
    }

    void showFileOpenDialog()
    {
        QString fileName = QFileDialog::getOpenFileName(
            this, "打开文件",
            QDir::homePath(),
            "文本文件 (*.txt);;所有文件 (*.*)"
        );

        if (!fileName.isEmpty()) {
            m_resultLabel->setText("选择的文件: " + fileName);
        } else {
            m_resultLabel->setText("取消选择");
        }
    }

    void showFileSaveDialog()
    {
        QString fileName = QFileDialog::getSaveFileName(
            this, "保存文件",
            QDir::homePath() + "/untitled.txt",
            "文本文件 (*.txt);;所有文件 (*.*)"
        );

        if (!fileName.isEmpty()) {
            m_resultLabel->setText("保存到: " + fileName);
        }
    }

    void showDirectoryDialog()
    {
        QString dir = QFileDialog::getExistingDirectory(
            this, "选择目录",
            QDir::homePath()
        );

        if (!dir.isEmpty()) {
            m_resultLabel->setText("选择的目录: " + dir);
        }
    }

    void showColorDialog()
    {
        QColor color = QColorDialog::getColor(
            Qt::white, this, "选择颜色"
        );

        if (color.isValid()) {
            m_resultLabel->setText(QString("选择的颜色: %1").arg(color.name()));
            m_resultLabel->setStyleSheet(
                QString("background-color: %1; padding: 10px;").arg(color.name())
            );
        }
    }

    void showFontDialog()
    {
        bool ok;
        QFont font = QFontDialog::getFont(&ok, this->font(), this, "选择字体");

        if (ok) {
            m_resultLabel->setFont(font);
            m_resultLabel->setText(QString("选择的字体: %1, %2pt")
                .arg(font.family()).arg(font.pointSize()));
        }
    }

    void showTextInputDialog()
    {
        bool ok;
        QString text = QInputDialog::getText(
            this, "输入文本",
            "请输入你的名字:",
            QLineEdit::Normal,
            "默认值",
            &ok
        );

        if (ok && !text.isEmpty()) {
            m_resultLabel->setText("输入的文本: " + text);
        }
    }

    void showIntInputDialog()
    {
        bool ok;
        int value = QInputDialog::getInt(
            this, "输入数字",
            "请输入年龄:",
            25,     // 默认值
            0,      // 最小值
            150,    // 最大值
            1,      // 步长
            &ok
        );

        if (ok) {
            m_resultLabel->setText(QString("输入的数字: %1").arg(value));
        }
    }

    void showItemInputDialog()
    {
        QStringList items = {"选项一", "选项二", "选项三", "选项四"};
        bool ok;
        QString item = QInputDialog::getItem(
            this, "选择项目",
            "请选择:",
            items,
            0,      // 默认选中
            false,  // 不可编辑
            &ok
        );

        if (ok && !item.isEmpty()) {
            m_resultLabel->setText("选择的项目: " + item);
        }
    }

    void showProgressDialog()
    {
        QProgressDialog progress("正在处理...", "取消", 0, 100, this);
        progress.setWindowModality(Qt::WindowModal);
        progress.setMinimumDuration(0);  // 立即显示

        for (int i = 0; i <= 100; ++i) {
            progress.setValue(i);
            QApplication::processEvents();

            if (progress.wasCanceled()) {
                m_resultLabel->setText("进度被取消");
                return;
            }

            QThread::msleep(30);  // 模拟工作
        }

        m_resultLabel->setText("进度完成!");
    }

    void showCustomDialog()
    {
        CustomDialog dialog(this);

        if (dialog.exec() == QDialog::Accepted) {
            m_resultLabel->setText(QString("姓名: %1\n邮箱: %2")
                .arg(dialog.name()).arg(dialog.email()));
        } else {
            m_resultLabel->setText("对话框被取消");
        }
    }

    QLabel *m_resultLabel;
};

int main(int argc, char *argv[])
{
    QApplication app(argc, argv);

    qDebug() << "=== Qt6 对话框示例 ===\n";

    DialogsDemo demo;
    demo.show();

    return app.exec();
}

#include "main.moc"
