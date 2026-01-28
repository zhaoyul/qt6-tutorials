/**
 * Qt6 主窗口示例
 *
 * QMainWindow 提供完整的应用程序框架：
 * - 菜单栏 (QMenuBar)
 * - 工具栏 (QToolBar)
 * - 状态栏 (QStatusBar)
 * - 停靠窗口 (QDockWidget)
 * - 中央部件 (Central Widget)
 *
 * QAction 用于定义可重用的用户操作。
 *
 * 官方文档: https://doc.qt.io/qt-6/qmainwindow.html
 */

#include <QApplication>
#include <QMainWindow>
#include <QMenuBar>
#include <QMenu>
#include <QToolBar>
#include <QStatusBar>
#include <QDockWidget>
#include <QAction>
#include <QTextEdit>
#include <QLabel>
#include <QFileDialog>
#include <QMessageBox>
#include <QStyle>
#include <QCloseEvent>
#include <QSettings>
#include <QDebug>

class MainWindowDemo : public QMainWindow
{
    Q_OBJECT

public:
    explicit MainWindowDemo(QWidget *parent = nullptr)
        : QMainWindow(parent)
    {
        setWindowTitle("Qt6 MainWindow Demo");
        resize(800, 600);

        createActions();
        createMenus();
        createToolBars();
        createStatusBar();
        createDockWindows();
        createCentralWidget();

        // 恢复窗口状态
        readSettings();
    }

protected:
    void closeEvent(QCloseEvent *event) override
    {
        if (maybeSave()) {
            writeSettings();
            event->accept();
        } else {
            event->ignore();
        }
    }

private slots:
    void newFile()
    {
        if (maybeSave()) {
            m_textEdit->clear();
            setCurrentFile(QString());
            statusBar()->showMessage("新建文件", 2000);
        }
    }

    void open()
    {
        if (maybeSave()) {
            QString fileName = QFileDialog::getOpenFileName(this);
            if (!fileName.isEmpty()) {
                loadFile(fileName);
            }
        }
    }

    bool save()
    {
        if (m_currentFile.isEmpty()) {
            return saveAs();
        }
        return saveFile(m_currentFile);
    }

    bool saveAs()
    {
        QString fileName = QFileDialog::getSaveFileName(this);
        if (fileName.isEmpty()) {
            return false;
        }
        return saveFile(fileName);
    }

    void about()
    {
        QMessageBox::about(this, "关于",
            "Qt6 MainWindow 示例\n\n"
            "演示 QMainWindow 的主要功能：\n"
            "• 菜单栏和工具栏\n"
            "• 状态栏\n"
            "• 停靠窗口\n"
            "• 文件操作");
    }

    void documentWasModified()
    {
        setWindowModified(m_textEdit->document()->isModified());
    }

private:
    void createActions()
    {
        // 文件操作
        m_newAction = new QAction(style()->standardIcon(QStyle::SP_FileIcon), "新建(&N)", this);
        m_newAction->setShortcuts(QKeySequence::New);
        m_newAction->setStatusTip("创建新文件");
        connect(m_newAction, &QAction::triggered, this, &MainWindowDemo::newFile);

        m_openAction = new QAction(style()->standardIcon(QStyle::SP_DialogOpenButton), "打开(&O)", this);
        m_openAction->setShortcuts(QKeySequence::Open);
        m_openAction->setStatusTip("打开文件");
        connect(m_openAction, &QAction::triggered, this, &MainWindowDemo::open);

        m_saveAction = new QAction(style()->standardIcon(QStyle::SP_DialogSaveButton), "保存(&S)", this);
        m_saveAction->setShortcuts(QKeySequence::Save);
        m_saveAction->setStatusTip("保存文件");
        connect(m_saveAction, &QAction::triggered, this, &MainWindowDemo::save);

        m_saveAsAction = new QAction("另存为(&A)...", this);
        m_saveAsAction->setShortcuts(QKeySequence::SaveAs);
        connect(m_saveAsAction, &QAction::triggered, this, &MainWindowDemo::saveAs);

        m_exitAction = new QAction("退出(&X)", this);
        m_exitAction->setShortcuts(QKeySequence::Quit);
        connect(m_exitAction, &QAction::triggered, this, &QWidget::close);

        // 编辑操作
        m_cutAction = new QAction(style()->standardIcon(QStyle::SP_DialogDiscardButton), "剪切(&T)", this);
        m_cutAction->setShortcuts(QKeySequence::Cut);

        m_copyAction = new QAction("复制(&C)", this);
        m_copyAction->setShortcuts(QKeySequence::Copy);

        m_pasteAction = new QAction("粘贴(&P)", this);
        m_pasteAction->setShortcuts(QKeySequence::Paste);

        // 关于
        m_aboutAction = new QAction("关于(&A)", this);
        connect(m_aboutAction, &QAction::triggered, this, &MainWindowDemo::about);

        m_aboutQtAction = new QAction("关于 Qt", this);
        connect(m_aboutQtAction, &QAction::triggered, qApp, &QApplication::aboutQt);
    }

    void createMenus()
    {
        // 文件菜单
        QMenu *fileMenu = menuBar()->addMenu("文件(&F)");
        fileMenu->addAction(m_newAction);
        fileMenu->addAction(m_openAction);
        fileMenu->addAction(m_saveAction);
        fileMenu->addAction(m_saveAsAction);
        fileMenu->addSeparator();
        fileMenu->addAction(m_exitAction);

        // 编辑菜单
        QMenu *editMenu = menuBar()->addMenu("编辑(&E)");
        editMenu->addAction(m_cutAction);
        editMenu->addAction(m_copyAction);
        editMenu->addAction(m_pasteAction);

        // 视图菜单 (用于控制停靠窗口)
        m_viewMenu = menuBar()->addMenu("视图(&V)");

        // 帮助菜单
        menuBar()->addSeparator();
        QMenu *helpMenu = menuBar()->addMenu("帮助(&H)");
        helpMenu->addAction(m_aboutAction);
        helpMenu->addAction(m_aboutQtAction);
    }

    void createToolBars()
    {
        // 文件工具栏
        QToolBar *fileToolBar = addToolBar("文件");
        fileToolBar->setObjectName("fileToolBar");
        fileToolBar->addAction(m_newAction);
        fileToolBar->addAction(m_openAction);
        fileToolBar->addAction(m_saveAction);

        // 编辑工具栏
        QToolBar *editToolBar = addToolBar("编辑");
        editToolBar->setObjectName("editToolBar");
        editToolBar->addAction(m_cutAction);
        editToolBar->addAction(m_copyAction);
        editToolBar->addAction(m_pasteAction);

        // 添加到视图菜单
        m_viewMenu->addAction(fileToolBar->toggleViewAction());
        m_viewMenu->addAction(editToolBar->toggleViewAction());
    }

    void createStatusBar()
    {
        // 主状态消息
        statusBar()->showMessage("就绪");

        // 永久部件
        QLabel *permanentLabel = new QLabel("Qt6 Demo");
        statusBar()->addPermanentWidget(permanentLabel);
    }

    void createDockWindows()
    {
        // 左侧停靠窗口
        QDockWidget *leftDock = new QDockWidget("导航", this);
        leftDock->setObjectName("leftDock");
        leftDock->setAllowedAreas(Qt::LeftDockWidgetArea | Qt::RightDockWidgetArea);
        QTextEdit *navEdit = new QTextEdit("导航面板\n\n这是一个停靠窗口");
        navEdit->setReadOnly(true);
        leftDock->setWidget(navEdit);
        addDockWidget(Qt::LeftDockWidgetArea, leftDock);

        // 右侧停靠窗口
        QDockWidget *rightDock = new QDockWidget("属性", this);
        rightDock->setObjectName("rightDock");
        rightDock->setAllowedAreas(Qt::LeftDockWidgetArea | Qt::RightDockWidgetArea);
        QTextEdit *propEdit = new QTextEdit("属性面板\n\n可以拖动到不同位置");
        propEdit->setReadOnly(true);
        rightDock->setWidget(propEdit);
        addDockWidget(Qt::RightDockWidgetArea, rightDock);

        // 底部停靠窗口
        QDockWidget *bottomDock = new QDockWidget("输出", this);
        bottomDock->setObjectName("bottomDock");
        bottomDock->setAllowedAreas(Qt::BottomDockWidgetArea | Qt::TopDockWidgetArea);
        QTextEdit *outputEdit = new QTextEdit("输出面板\n\n停靠窗口可以浮动或关闭");
        outputEdit->setReadOnly(true);
        bottomDock->setWidget(outputEdit);
        addDockWidget(Qt::BottomDockWidgetArea, bottomDock);

        // 添加到视图菜单
        m_viewMenu->addSeparator();
        m_viewMenu->addAction(leftDock->toggleViewAction());
        m_viewMenu->addAction(rightDock->toggleViewAction());
        m_viewMenu->addAction(bottomDock->toggleViewAction());
    }

    void createCentralWidget()
    {
        m_textEdit = new QTextEdit(this);
        m_textEdit->setPlaceholderText("在此输入内容...\n\n这是中央部件 (Central Widget)");
        setCentralWidget(m_textEdit);

        connect(m_textEdit->document(), &QTextDocument::contentsChanged,
                this, &MainWindowDemo::documentWasModified);

        // 连接编辑操作
        connect(m_cutAction, &QAction::triggered, m_textEdit, &QTextEdit::cut);
        connect(m_copyAction, &QAction::triggered, m_textEdit, &QTextEdit::copy);
        connect(m_pasteAction, &QAction::triggered, m_textEdit, &QTextEdit::paste);
    }

    void readSettings()
    {
        QSettings settings("QtDemo", "MainWindow");
        restoreGeometry(settings.value("geometry").toByteArray());
        restoreState(settings.value("windowState").toByteArray());
    }

    void writeSettings()
    {
        QSettings settings("QtDemo", "MainWindow");
        settings.setValue("geometry", saveGeometry());
        settings.setValue("windowState", saveState());
    }

    bool maybeSave()
    {
        if (!m_textEdit->document()->isModified())
            return true;

        QMessageBox::StandardButton ret = QMessageBox::warning(this, "保存更改?",
            "文档已修改。\n是否保存更改?",
            QMessageBox::Save | QMessageBox::Discard | QMessageBox::Cancel);

        if (ret == QMessageBox::Save)
            return save();
        if (ret == QMessageBox::Cancel)
            return false;
        return true;
    }

    void loadFile(const QString &fileName)
    {
        QFile file(fileName);
        if (file.open(QFile::ReadOnly | QFile::Text)) {
            m_textEdit->setPlainText(file.readAll());
            setCurrentFile(fileName);
            statusBar()->showMessage("文件已加载", 2000);
        }
    }

    bool saveFile(const QString &fileName)
    {
        QFile file(fileName);
        if (file.open(QFile::WriteOnly | QFile::Text)) {
            file.write(m_textEdit->toPlainText().toUtf8());
            setCurrentFile(fileName);
            statusBar()->showMessage("文件已保存", 2000);
            return true;
        }
        return false;
    }

    void setCurrentFile(const QString &fileName)
    {
        m_currentFile = fileName;
        m_textEdit->document()->setModified(false);
        setWindowModified(false);

        QString title = fileName.isEmpty() ? "未命名" : QFileInfo(fileName).fileName();
        setWindowTitle(title + "[*] - MainWindow Demo");
    }

    QTextEdit *m_textEdit;
    QString m_currentFile;
    QMenu *m_viewMenu;

    QAction *m_newAction;
    QAction *m_openAction;
    QAction *m_saveAction;
    QAction *m_saveAsAction;
    QAction *m_exitAction;
    QAction *m_cutAction;
    QAction *m_copyAction;
    QAction *m_pasteAction;
    QAction *m_aboutAction;
    QAction *m_aboutQtAction;
};

int main(int argc, char *argv[])
{
    QApplication app(argc, argv);

    qDebug() << "=== Qt6 主窗口示例 ===\n";
    qDebug() << "功能:";
    qDebug() << "- 菜单栏: 文件、编辑、视图、帮助";
    qDebug() << "- 工具栏: 可拖动、隐藏";
    qDebug() << "- 停靠窗口: 可拖动、浮动、关闭";
    qDebug() << "- 状态栏: 显示消息";
    qDebug() << "- 窗口状态: 自动保存和恢复\n";

    MainWindowDemo mainWindow;
    mainWindow.show();

    return app.exec();
}

#include "main.moc"
