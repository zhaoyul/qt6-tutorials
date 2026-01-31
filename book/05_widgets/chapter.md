# 第5章：Qt Widgets 模块

Qt Widgets 提供了丰富的桌面 UI 控件集，是构建传统桌面应用程序的基础。本章将详细介绍各种控件、布局、对话框和自定义控件的实现。

---

## 5.1 QApplication 和基础控件

### 5.1.1 QApplication

```cpp
// [C++] QApplication
#include <QApplication>

int main(int argc, char *argv[])
{
    // 每个 Widgets 应用只能有一个 QApplication
    QApplication app(argc, argv);
    
    // 设置应用级属性
    app.setApplicationName("MyWidgetsApp");
    app.setApplicationVersion("1.0.0");
    app.setOrganizationName("MyCompany");
    
    // 设置全局样式
    app.setStyle("Fusion");  // Fusion, Windows, macOS
    
    // 设置全局样式表
    app.setStyleSheet("QPushButton { background-color: #3498db; }");
    
    // 设置字体
    app.setFont(QFont("Arial", 10));
    
    return app.exec();
}
```

```python
# [Python] QApplication
from PySide6.QtWidgets import QApplication

app = QApplication([])

# 应用属性
app.setApplicationName("MyWidgetsApp")
app.setApplicationVersion("1.0.0")

# 全局样式
app.setStyle("Fusion")

# 样式表
app.setStyleSheet("""
    QPushButton { 
        background-color: #3498db;
        color: white;
        padding: 8px 16px;
        border-radius: 4px;
    }
""")

app.exec()
```

### 5.1.2 基础控件

```cpp
// [C++] 基础控件示例
#include <QWidget>
#include <QVBoxLayout>
#include <QLabel>
#include <QPushButton>
#include <QLineEdit>
#include <QTextEdit>
#include <QCheckBox>
#include <QRadioButton>
#include <QComboBox>
#include <QSpinBox>
#include <QSlider>
#include <QProgressBar>

class BasicWidgetsDemo : public QWidget
{
public:
    BasicWidgetsDemo(QWidget *parent = nullptr) : QWidget(parent)
    {
        auto *layout = new QVBoxLayout(this);
        
        // 标签
        QLabel *label = new QLabel("<h2>Basic Widgets Demo</h2>");
        label->setAlignment(Qt::AlignCenter);
        layout->addWidget(label);
        
        // 单行输入
        QLineEdit *lineEdit = new QLineEdit();
        lineEdit->setPlaceholderText("Enter text here...");
        lineEdit->setMaxLength(100);
        connect(lineEdit, &QLineEdit::textChanged, this, [](const QString &text) {
            qDebug() << "Text changed:" << text;
        });
        layout->addWidget(lineEdit);
        
        // 多行文本
        QTextEdit *textEdit = new QTextEdit();
        textEdit->setPlaceholderText("Enter multiple lines...");
        textEdit->setMaximumHeight(100);
        layout->addWidget(textEdit);
        
        // 按钮
        QPushButton *button = new QPushButton("Click Me!");
        button->setToolTip("This is a button");
        connect(button, &QPushButton::clicked, this, []() {
            qDebug() << "Button clicked!";
        });
        layout->addWidget(button);
        
        // 复选框
        QCheckBox *checkBox = new QCheckBox("Enable feature");
        checkBox->setChecked(true);
        connect(checkBox, &QCheckBox::stateChanged, this, [](int state) {
            qDebug() << "Checkbox state:" << state;
        });
        layout->addWidget(checkBox);
        
        // 单选按钮组
        QGroupBox *radioGroup = new QGroupBox("Select option");
        QVBoxLayout *radioLayout = new QVBoxLayout();
        QRadioButton *radio1 = new QRadioButton("Option 1");
        QRadioButton *radio2 = new QRadioButton("Option 2");
        radio1->setChecked(true);
        radioLayout->addWidget(radio1);
        radioLayout->addWidget(radio2);
        radioGroup->setLayout(radioLayout);
        layout->addWidget(radioGroup);
        
        // 下拉框
        QComboBox *comboBox = new QComboBox();
        comboBox->addItem("Item 1");
        comboBox->addItem("Item 2");
        comboBox->addItem("Item 3");
        comboBox->setEditable(true);
        connect(comboBox, QOverload<int>::of(&QComboBox::currentIndexChanged),
                this, [](int index) {
            qDebug() << "Selected index:" << index;
        });
        layout->addWidget(comboBox);
        
        // 数字选择器
        QSpinBox *spinBox = new QSpinBox();
        spinBox->setRange(0, 100);
        spinBox->setValue(50);
        spinBox->setSuffix(" %");
        layout->addWidget(spinBox);
        
        // 滑块
        QSlider *slider = new QSlider(Qt::Horizontal);
        slider->setRange(0, 100);
        slider->setValue(50);
        connect(slider, &QSlider::valueChanged, this, [](int value) {
            qDebug() << "Slider value:" << value;
        });
        layout->addWidget(slider);
        
        // 进度条
        QProgressBar *progressBar = new QProgressBar();
        progressBar->setRange(0, 100);
        progressBar->setValue(75);
        layout->addWidget(progressBar);
    }
};
```

```python
# [Python] 基础控件
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton,
                               QLineEdit, QTextEdit, QCheckBox, QRadioButton,
                               QComboBox, QSpinBox, QSlider, QProgressBar,
                               QGroupBox)
from PySide6.QtCore import Qt

class BasicWidgetsDemo(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        layout = QVBoxLayout(self)
        
        # 标签
        label = QLabel("<h2>Basic Widgets Demo</h2>")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)
        
        # 单行输入
        self.line_edit = QLineEdit()
        self.line_edit.setPlaceholderText("Enter text here...")
        self.line_edit.textChanged.connect(self.on_text_changed)
        layout.addWidget(self.line_edit)
        
        # 多行文本
        self.text_edit = QTextEdit()
        self.text_edit.setPlaceholderText("Enter multiple lines...")
        self.text_edit.setMaximumHeight(100)
        layout.addWidget(self.text_edit)
        
        # 按钮
        button = QPushButton("Click Me!")
        button.clicked.connect(self.on_button_clicked)
        layout.addWidget(button)
        
        # 复选框
        self.checkbox = QCheckBox("Enable feature")
        self.checkbox.setChecked(True)
        self.checkbox.stateChanged.connect(self.on_checkbox_changed)
        layout.addWidget(self.checkbox)
        
        # 单选按钮组
        radio_group = QGroupBox("Select option")
        radio_layout = QVBoxLayout()
        self.radio1 = QRadioButton("Option 1")
        self.radio2 = QRadioButton("Option 2")
        self.radio1.setChecked(True)
        radio_layout.addWidget(self.radio1)
        radio_layout.addWidget(self.radio2)
        radio_group.setLayout(radio_layout)
        layout.addWidget(radio_group)
        
        # 下拉框
        self.combo = QComboBox()
        self.combo.addItems(["Item 1", "Item 2", "Item 3"])
        self.combo.currentIndexChanged.connect(self.on_combo_changed)
        layout.addWidget(self.combo)
        
        # 数字选择器
        self.spin = QSpinBox()
        self.spin.setRange(0, 100)
        self.spin.setValue(50)
        self.spin.setSuffix(" %")
        layout.addWidget(self.spin)
        
        # 滑块
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0, 100)
        self.slider.setValue(50)
        self.slider.valueChanged.connect(self.on_slider_changed)
        layout.addWidget(self.slider)
        
        # 进度条
        self.progress = QProgressBar()
        self.progress.setRange(0, 100)
        self.progress.setValue(75)
        layout.addWidget(self.progress)
    
    def on_text_changed(self, text):
        print(f"Text changed: {text}")
    
    def on_button_clicked(self):
        print("Button clicked!")
    
    def on_checkbox_changed(self, state):
        print(f"Checkbox state: {state}")
    
    def on_combo_changed(self, index):
        print(f"Selected index: {index}")
    
    def on_slider_changed(self, value):
        print(f"Slider value: {value}")
        self.progress.setValue(value)

# 运行
from PySide6.QtWidgets import QApplication
app = QApplication([])
window = BasicWidgetsDemo()
window.show()
app.exec()
```

---

## 5.2 布局管理

### 5.2.1 基础布局

```cpp
// [C++] 布局管理
#include <QHBoxLayout>
#include <QVBoxLayout>
#include <QGridLayout>
#include <QFormLayout>
#include <QPushButton>
#include <QLabel>
#include <QLineEdit>

void layoutDemo(QWidget *parent)
{
    // 水平布局
    QHBoxLayout *hLayout = new QHBoxLayout();
    hLayout->addWidget(new QPushButton("Left"));
    hLayout->addWidget(new QPushButton("Center"));
    hLayout->addWidget(new QPushButton("Right"));
    hLayout->addStretch();  // 弹性空间
    
    // 垂直布局
    QVBoxLayout *vLayout = new QVBoxLayout();
    vLayout->addWidget(new QLabel("Top"));
    vLayout->addWidget(new QLabel("Middle"));
    vLayout->addWidget(new QLabel("Bottom"));
    vLayout->addStretch();
    
    // 网格布局
    QGridLayout *gridLayout = new QGridLayout();
    gridLayout->addWidget(new QLabel("Name:"), 0, 0);
    gridLayout->addWidget(new QLineEdit(), 0, 1);
    gridLayout->addWidget(new QLabel("Email:"), 1, 0);
    gridLayout->addWidget(new QLineEdit(), 1, 1);
    gridLayout->addWidget(new QLabel("Phone:"), 2, 0);
    gridLayout->addWidget(new QLineEdit(), 2, 1);
    
    // 跨列
    gridLayout->addWidget(new QPushButton("Submit"), 3, 0, 1, 2);
    
    // 设置列拉伸因子
    gridLayout->setColumnStretch(1, 1);
    
    // 表单布局
    QFormLayout *formLayout = new QFormLayout();
    formLayout->addRow("Name:", new QLineEdit());
    formLayout->addRow("Email:", new QLineEdit());
    formLayout->addRow("Age:", new QSpinBox());
    formLayout->addRow(new QPushButton("Save"));
}
```

```python
# [Python] 布局管理
from PySide6.QtWidgets import (QHBoxLayout, QVBoxLayout, QGridLayout, 
                               QFormLayout, QPushButton, QLabel, 
                               QLineEdit, QSpinBox)

def create_layouts():
    # 水平布局
    h_layout = QHBoxLayout()
    h_layout.addWidget(QPushButton("Left"))
    h_layout.addWidget(QPushButton("Center"))
    h_layout.addWidget(QPushButton("Right"))
    h_layout.addStretch()
    
    # 垂直布局
    v_layout = QVBoxLayout()
    v_layout.addWidget(QLabel("Top"))
    v_layout.addWidget(QLabel("Middle"))
    v_layout.addWidget(QLabel("Bottom"))
    v_layout.addStretch()
    
    # 网格布局
    grid = QGridLayout()
    grid.addWidget(QLabel("Name:"), 0, 0)
    grid.addWidget(QLineEdit(), 0, 1)
    grid.addWidget(QLabel("Email:"), 1, 0)
    grid.addWidget(QLineEdit(), 1, 1)
    grid.addWidget(QPushButton("Submit"), 2, 0, 1, 2)  # 跨2列
    grid.setColumnStretch(1, 1)
    
    # 表单布局
    form = QFormLayout()
    form.addRow("Name:", QLineEdit())
    form.addRow("Email:", QLineEdit())
    form.addRow("Age:", QSpinBox())
    
    return h_layout, v_layout, grid, form
```

### 5.2.2 分割器和堆叠布局

```cpp
// [C++] QSplitter 和 QStackedLayout
#include <QSplitter>
#include <QStackedLayout>
#include <QListWidget>
#include <QTextEdit>

void advancedLayouts(QWidget *parent)
{
    // 分割器 - 可调整大小的分割区域
    QSplitter *splitter = new QSplitter(Qt::Horizontal);
    
    QListWidget *listWidget = new QListWidget();
    listWidget->addItem("Item 1");
    listWidget->addItem("Item 2");
    listWidget->addItem("Item 3");
    
    QTextEdit *textEdit = new QTextEdit();
    textEdit->setPlainText("Edit this text...");
    
    splitter->addWidget(listWidget);
    splitter->addWidget(textEdit);
    splitter->setSizes({200, 600});  // 设置初始大小
    
    // 堆叠布局 - 切换显示不同页面
    QStackedLayout *stackedLayout = new QStackedLayout();
    
    QWidget *page1 = new QWidget();
    page1->setLayout(new QVBoxLayout());
    page1->layout()->addWidget(new QLabel("Page 1"));
    
    QWidget *page2 = new QWidget();
    page2->setLayout(new QVBoxLayout());
    page2->layout()->addWidget(new QLabel("Page 2"));
    
    stackedLayout->addWidget(page1);  // index 0
    stackedLayout->addWidget(page2);  // index 1
    
    // 切换页面
    stackedLayout->setCurrentIndex(1);  // 显示 page2
    // 或
    stackedLayout->setCurrentWidget(page1);  // 显示 page1
}
```

---

## 5.3 对话框

### 5.3.1 标准对话框

```cpp
// [C++] 标准对话框
#include <QMessageBox>
#include <QFileDialog>
#include <QInputDialog>
#include <QColorDialog>
#include <QFontDialog>
#include <QProgressDialog>

void standardDialogs(QWidget *parent)
{
    // 消息框
    QMessageBox::information(parent, "Info", "Operation completed!");
    QMessageBox::warning(parent, "Warning", "Something went wrong!");
    QMessageBox::critical(parent, "Error", "Failed to save file!");
    
    // 确认对话框
    QMessageBox::StandardButton reply = QMessageBox::question(
        parent, "Confirm", "Are you sure?",
        QMessageBox::Yes | QMessageBox::No);
    
    if (reply == QMessageBox::Yes) {
        // 用户点击了 Yes
    }
    
    // 文件对话框
    QString fileName = QFileDialog::getOpenFileName(
        parent, "Open File", "/home",
        "Images (*.png *.xpm *.jpg);;Text files (*.txt);;All files (*)");
    
    QString saveFile = QFileDialog::getSaveFileName(
        parent, "Save File", "/home",
        "Text files (*.txt)");
    
    QString dir = QFileDialog::getExistingDirectory(
        parent, "Select Directory", "/home");
    
    // 输入对话框
    bool ok;
    QString text = QInputDialog::getText(
        parent, "Input", "Enter your name:",
        QLineEdit::Normal, "", &ok);
    
    int number = QInputDialog::getInt(
        parent, "Input", "Enter age:",
        25, 0, 150, 1, &ok);
    
    double value = QInputDialog::getDouble(
        parent, "Input", "Enter value:",
        0.00, -10000, 10000, 2, &ok);
    
    QStringList items = {"Red", "Green", "Blue"};
    QString item = QInputDialog::getItem(
        parent, "Input", "Select color:",
        items, 0, false, &ok);
    
    // 颜色对话框
    QColor color = QColorDialog::getColor(
        Qt::red, parent, "Select Color");
    
    if (color.isValid()) {
        qDebug() << "Selected color:" << color.name();
    }
    
    // 字体对话框
    bool fontOk;
    QFont font = QFontDialog::getFont(
        &fontOk, QFont("Arial", 12), parent);
    
    // 进度对话框
    QProgressDialog progress("Copying files...", "Cancel", 0, 100, parent);
    progress.setWindowModality(Qt::WindowModal);
    
    for (int i = 0; i < 100; ++i) {
        progress.setValue(i);
        if (progress.wasCanceled()) {
            break;
        }
        // 执行操作...
    }
}
```

```python
# [Python] 标准对话框
from PySide6.QtWidgets import (QMessageBox, QFileDialog, QInputDialog,
                               QColorDialog, QFontDialog, QProgressDialog)
from PySide6.QtCore import Qt

def standard_dialogs(parent):
    # 消息框
    QMessageBox.information(parent, "Info", "Operation completed!")
    
    # 确认对话框
    reply = QMessageBox.question(
        parent, "Confirm", "Are you sure?",
        QMessageBox.Yes | QMessageBox.No)
    
    if reply == QMessageBox.Yes:
        print("User clicked Yes")
    
    # 文件对话框
    file_name, _ = QFileDialog.getOpenFileName(
        parent, "Open File", "/home",
        "Images (*.png *.jpg);;All files (*)")
    
    # 输入对话框
    text, ok = QInputDialog.getText(
        parent, "Input", "Enter your name:")
    
    if ok and text:
        print(f"Name: {text}")
    
    # 颜色对话框
    color = QColorDialog.getColor(Qt.red, parent, "Select Color")
    if color.isValid():
        print(f"Selected color: {color.name()}")
```

### 5.3.2 自定义对话框

```cpp
// [C++] 自定义对话框
#include <QDialog>
#include <QDialogButtonBox>

class LoginDialog : public QDialog
{
    Q_OBJECT
    
public:
    LoginDialog(QWidget *parent = nullptr) : QDialog(parent)
    {
        setWindowTitle("Login");
        setModal(true);  // 模态对话框
        
        QFormLayout *formLayout = new QFormLayout(this);
        
        m_usernameEdit = new QLineEdit();
        m_passwordEdit = new QLineEdit();
        m_passwordEdit->setEchoMode(QLineEdit::Password);
        
        formLayout->addRow("Username:", m_usernameEdit);
        formLayout->addRow("Password:", m_passwordEdit);
        
        QDialogButtonBox *buttonBox = new QDialogButtonBox(
            QDialogButtonBox::Ok | QDialogButtonBox::Cancel);
        
        connect(buttonBox, &QDialogButtonBox::accepted, this, &QDialog::accept);
        connect(buttonBox, &QDialogButtonBox::rejected, this, &QDialog::reject);
        
        formLayout->addRow(buttonBox);
    }
    
    QString username() const { return m_usernameEdit->text(); }
    QString password() const { return m_passwordEdit->text(); }
    
private:
    QLineEdit *m_usernameEdit;
    QLineEdit *m_passwordEdit;
};

// 使用
LoginDialog dlg(this);
if (dlg.exec() == QDialog::Accepted) {
    qDebug() << "Username:" << dlg.username();
    qDebug() << "Password:" << dlg.password();
}
```

---

## 5.4 主窗口（QMainWindow）

### 5.4.1 主窗口组件

```cpp
// [C++] QMainWindow
#include <QMainWindow>
#include <QMenuBar>
#include <QToolBar>
#include <QStatusBar>
#include <QDockWidget>
#include <QTextEdit>
#include <QAction>

class MainWindow : public QMainWindow
{
    Q_OBJECT
    
public:
    MainWindow(QWidget *parent = nullptr) : QMainWindow(parent)
    {
        setWindowTitle("MainWindow Demo");
        resize(1024, 768);
        
        // 中央部件
        QTextEdit *textEdit = new QTextEdit();
        setCentralWidget(textEdit);
        
        createMenuBar();
        createToolBar();
        createStatusBar();
        createDockWindows();
    }
    
private:
    void createMenuBar()
    {
        // 文件菜单
        QMenu *fileMenu = menuBar()->addMenu("&File");
        
        QAction *newAct = new QAction("&New", this);
        newAct->setShortcut(QKeySequence::New);
        newAct->setStatusTip("Create new file");
        connect(newAct, &QAction::triggered, this, &MainWindow::onNew);
        fileMenu->addAction(newAct);
        
        QAction *openAct = new QAction("&Open...", this);
        openAct->setShortcut(QKeySequence::Open);
        connect(openAct, &QAction::triggered, this, &MainWindow::onOpen);
        fileMenu->addAction(openAct);
        
        fileMenu->addSeparator();
        
        QAction *exitAct = new QAction("E&xit", this);
        exitAct->setShortcut(QKeySequence::Quit);
        connect(exitAct, &QAction::triggered, this, &QWidget::close);
        fileMenu->addAction(exitAct);
        
        // 编辑菜单
        QMenu *editMenu = menuBar()->addMenu("&Edit");
        editMenu->addAction("&Cut", this, &MainWindow::onCut, QKeySequence::Cut);
        editMenu->addAction("&Copy", this, &MainWindow::onCopy, QKeySequence::Copy);
        editMenu->addAction("&Paste", this, &MainWindow::onPaste, QKeySequence::Paste);
        
        // 帮助菜单
        QMenu *helpMenu = menuBar()->addMenu("&Help");
        helpMenu->addAction("&About", this, &MainWindow::onAbout);
    }
    
    void createToolBar()
    {
        QToolBar *fileToolBar = addToolBar("File");
        fileToolBar->addAction(QIcon("new.png"), "New", this, &MainWindow::onNew);
        fileToolBar->addAction(QIcon("open.png"), "Open", this, &MainWindow::onOpen);
        fileToolBar->addSeparator();
        fileToolBar->addAction(QIcon("save.png"), "Save", this, &MainWindow::onSave);
        
        // 添加控件到工具栏
        QComboBox *zoomCombo = new QComboBox();
        zoomCombo->addItems({"50%", "75%", "100%", "150%", "200%"});
        zoomCombo->setCurrentText("100%");
        fileToolBar->addWidget(zoomCombo);
    }
    
    void createStatusBar()
    {
        statusBar()->showMessage("Ready");
        
        // 永久消息
        QLabel *permanentLabel = new QLabel("Version 1.0");
        statusBar()->addPermanentWidget(permanentLabel);
    }
    
    void createDockWindows()
    {
        // 左侧停靠窗口
        QDockWidget *dock = new QDockWidget("Explorer", this);
        QListWidget *listWidget = new QListWidget();
        listWidget->addItems({"File 1", "File 2", "File 3"});
        dock->setWidget(listWidget);
        addDockWidget(Qt::LeftDockWidgetArea, dock);
        
        // 右侧停靠窗口
        QDockWidget *propDock = new QDockWidget("Properties", this);
        propDock->setWidget(new QLabel("Properties here"));
        addDockWidget(Qt::RightDockWidgetArea, propDock);
        
        // 允许停靠窗口拖拽交换
        tabifyDockWidget(dock, propDock);
    }
    
private slots:
    void onNew() { qDebug() << "New"; }
    void onOpen() { qDebug() << "Open"; }
    void onSave() { qDebug() << "Save"; }
    void onCut() { qDebug() << "Cut"; }
    void onCopy() { qDebug() << "Copy"; }
    void onPaste() { qDebug() << "Paste"; }
    void onAbout() { QMessageBox::about(this, "About", "Demo Application"); }
};
```

```python
# [Python] QMainWindow
from PySide6.QtWidgets import (QMainWindow, QTextEdit, QMenuBar, QToolBar,
                               QStatusBar, QDockWidget, QListWidget, QLabel,
                               QAction, QComboBox, QMessageBox)
from PySide6.QtCore import Qt
from PySide6.QtGui import QKeySequence, QIcon

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.setWindowTitle("MainWindow Demo")
        self.resize(1024, 768)
        
        # 中央部件
        self.text_edit = QTextEdit()
        self.setCentralWidget(self.text_edit)
        
        self.create_menu_bar()
        self.create_tool_bar()
        self.create_status_bar()
        self.create_dock_windows()
    
    def create_menu_bar(self):
        # 文件菜单
        file_menu = self.menuBar().addMenu("&File")
        
        new_act = QAction("&New", self)
        new_act.setShortcut(QKeySequence.New)
        new_act.triggered.connect(self.on_new)
        file_menu.addAction(new_act)
        
        open_act = QAction("&Open...", self)
        open_act.setShortcut(QKeySequence.Open)
        open_act.triggered.connect(self.on_open)
        file_menu.addAction(open_act)
        
        file_menu.addSeparator()
        
        exit_act = QAction("E&xit", self)
        exit_act.setShortcut(QKeySequence.Quit)
        exit_act.triggered.connect(self.close)
        file_menu.addAction(exit_act)
        
        # 编辑菜单
        edit_menu = self.menuBar().addMenu("&Edit")
        edit_menu.addAction("Cu&t", self.on_cut, QKeySequence.Cut)
        edit_menu.addAction("&Copy", self.on_copy, QKeySequence.Copy)
        edit_menu.addAction("&Paste", self.on_paste, QKeySequence.Paste)
    
    def create_tool_bar(self):
        toolbar = self.addToolBar("File")
        toolbar.addAction("New", self.on_new)
        toolbar.addAction("Open", self.on_open)
        toolbar.addSeparator()
        toolbar.addAction("Save", self.on_save)
        
        # 添加控件
        self.zoom_combo = QComboBox()
        self.zoom_combo.addItems(["50%", "75%", "100%", "150%", "200%"])
        self.zoom_combo.setCurrentText("100%")
        toolbar.addWidget(self.zoom_combo)
    
    def create_status_bar(self):
        self.statusBar().showMessage("Ready")
        self.statusBar().addPermanentWidget(QLabel("Version 1.0"))
    
    def create_dock_windows(self):
        # 左侧停靠窗口
        dock = QDockWidget("Explorer", self)
        list_widget = QListWidget()
        list_widget.addItems(["File 1", "File 2", "File 3"])
        dock.setWidget(list_widget)
        self.addDockWidget(Qt.LeftDockWidgetArea, dock)
    
    def on_new(self): print("New")
    def on_open(self): print("Open")
    def on_save(self): print("Save")
    def on_cut(self): print("Cut")
    def on_copy(self): print("Copy")
    def on_paste(self): print("Paste")
```

---

## 5.5 视图组件

### 5.5.1 Model/View 架构

```cpp
// [C++] Model/View 架构
#include <QTableView>
#include <QListView>
#include <QTreeView>
#include <QStandardItemModel>

void modelViewDemo(QWidget *parent)
{
    // 标准项模型
    QStandardItemModel *model = new QStandardItemModel(4, 2, parent);
    model->setHorizontalHeaderLabels({"Name", "Value"});
    
    // 填充数据
    for (int row = 0; row < 4; ++row) {
        QStandardItem *nameItem = new QStandardItem(QString("Item %1").arg(row));
        QStandardItem *valueItem = new QStandardItem(QString::number(row * 10));
        model->setItem(row, 0, nameItem);
        model->setItem(row, 1, valueItem);
    }
    
    // 表格视图
    QTableView *tableView = new QTableView();
    tableView->setModel(model);
    tableView->setSelectionBehavior(QAbstractItemView::SelectRows);
    tableView->setAlternatingRowColors(true);
    tableView->resizeColumnsToContents();
    
    // 列表视图
    QStringListModel *listModel = new QStringListModel();
    listModel->setStringList({"Apple", "Banana", "Cherry", "Date"});
    
    QListView *listView = new QListView();
    listView->setModel(listModel);
    listView->setEditTriggers(QAbstractItemView::DoubleClicked);
    
    // 树形视图
    QStandardItemModel *treeModel = new QStandardItemModel();
    treeModel->setHorizontalHeaderLabels({"Name", "Description"});
    
    QStandardItem *root = treeModel->invisibleRootItem();
    QStandardItem *folder = new QStandardItem("Folder 1");
    folder->appendRow({new QStandardItem("File 1"), new QStandardItem("Desc 1")});
    folder->appendRow({new QStandardItem("File 2"), new QStandardItem("Desc 2")});
    root->appendRow({folder, new QStandardItem("Folder")});
    
    QTreeView *treeView = new QTreeView();
    treeView->setModel(treeModel);
    treeView->expandAll();
}
```

---

## 5.6 自定义控件

### 5.6.1 继承现有控件

```cpp
// [C++] 自定义控件
#include <QWidget>
#include <QPainter>

class CustomButton : public QWidget
{
    Q_OBJECT
    Q_PROPERTY(QString text READ text WRITE setText NOTIFY textChanged)
    
public:
    explicit CustomButton(QWidget *parent = nullptr) 
        : QWidget(parent), m_pressed(false)
    {
        setSizePolicy(QSizePolicy::Minimum, QSizePolicy::Fixed);
        setMinimumSize(80, 32);
    }
    
    QString text() const { return m_text; }
    void setText(const QString &text) {
        if (m_text != text) {
            m_text = text;
            emit textChanged(text);
            update();
        }
    }
    
signals:
    void clicked();
    void textChanged(const QString &text);
    
protected:
    void paintEvent(QPaintEvent *) override {
        QPainter painter(this);
        painter.setRenderHint(QPainter::Antialiasing);
        
        // 绘制背景
        QColor bgColor = m_pressed ? QColor(0, 100, 200) : QColor(0, 120, 215);
        painter.fillRect(rect(), bgColor);
        
        // 绘制边框
        painter.setPen(QPen(QColor(0, 90, 180), 1));
        painter.drawRect(rect().adjusted(0, 0, -1, -1));
        
        // 绘制文本
        painter.setPen(Qt::white);
        painter.drawText(rect(), Qt::AlignCenter, m_text);
    }
    
    void mousePressEvent(QMouseEvent *) override {
        m_pressed = true;
        update();
    }
    
    void mouseReleaseEvent(QMouseEvent *) override {
        m_pressed = false;
        update();
        emit clicked();
    }
    
private:
    QString m_text;
    bool m_pressed;
};
```

```python
# [Python] 自定义控件
from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QColor, QPen
from PySide6.QtCore import Qt, Signal

class CustomButton(QWidget):
    clicked = Signal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._text = ""
        self._pressed = False
        self.setMinimumSize(80, 32)
    
    def text(self):
        return self._text
    
    def setText(self, text):
        if self._text != text:
            self._text = text
            self.update()
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # 背景
        bg_color = QColor(0, 100, 200) if self._pressed else QColor(0, 120, 215)
        painter.fillRect(self.rect(), bg_color)
        
        # 边框
        painter.setPen(QPen(QColor(0, 90, 180), 1))
        painter.drawRect(self.rect().adjusted(0, 0, -1, -1))
        
        # 文本
        painter.setPen(Qt.white)
        painter.drawText(self.rect(), Qt.AlignCenter, self._text)
        
        painter.end()
    
    def mousePressEvent(self, event):
        self._pressed = True
        self.update()
    
    def mouseReleaseEvent(self, event):
        self._pressed = False
        self.update()
        self.clicked.emit()
```

---

## 5.7 本章小结

本章介绍了 Qt Widgets 模块的核心内容：

| 主题 | 关键类 | 主要用途 |
|------|--------|----------|
| 基础控件 | `QPushButton`, `QLabel`, `QLineEdit` | 用户输入/输出 |
| 布局 | `QVBoxLayout`, `QHBoxLayout`, `QGridLayout` | 界面排列 |
| 对话框 | `QMessageBox`, `QFileDialog` | 交互弹窗 |
| 主窗口 | `QMainWindow` | 应用主界面 |
| 视图 | `QTableView`, `QListView`, `QTreeView` | 数据展示 |
| 自定义控件 | `QWidget` | 扩展控件库 |

在下一章中，我们将学习 QML 和 Qt Quick，探索现代声明式 UI 开发。
