# 第4章：Qt GUI 模块

Qt GUI 模块提供了窗口系统集成、事件处理、2D 图形、字体、图像等核心功能。本章将详细介绍这些功能在四种语言中的实现。

---

## 4.1 GUI 应用程序基础

### 4.1.1 QGuiApplication

`QGuiApplication` 是所有 GUI 应用程序的入口点（非 Widgets 应用）。

```cpp
// [C++] QGuiApplication 基础
#include <QGuiApplication>
#include <QWindow>
#include <QDebug>

int main(int argc, char *argv[])
{
    // 初始化 GUI 应用
    QGuiApplication app(argc, argv);
    
    // 设置应用信息
    app.setApplicationName("MyApp");
    app.setApplicationVersion("1.0");
    app.setOrganizationName("MyCompany");
    
    // 获取屏幕信息
    for (QScreen *screen : app.screens()) {
        qDebug() << "Screen:" << screen->name();
        qDebug() << "  Size:" << screen->size();
        qDebug() << "  DPI:" << screen->logicalDotsPerInch();
    }
    
    // 创建窗口
    QWindow window;
    window.setTitle("Hello QWindow");
    window.resize(800, 600);
    window.show();
    
    return app.exec();
}
```

```python
# [Python] QGuiApplication
from PySide6.QtGui import QGuiApplication, QWindow
from PySide6.QtCore import QSize

app = QGuiApplication([])

# 设置应用信息
app.setApplicationName("MyApp")
app.setApplicationVersion("1.0")
app.setOrganizationName("MyCompany")

# 获取屏幕信息
for screen in app.screens():
    print(f"Screen: {screen.name()}")
    print(f"  Size: {screen.size()}")
    print(f"  DPI: {screen.logicalDotsPerInch()}")

# 创建窗口
window = QWindow()
window.setTitle("Hello QWindow")
window.resize(800, 600)
window.show()

app.exec()
```

### 4.1.2 命令行参数处理

```cpp
// [C++] QCommandLineParser
#include <QGuiApplication>
#include <QCommandLineParser>

int main(int argc, char *argv[])
{
    QGuiApplication app(argc, argv);
    
    QCommandLineParser parser;
    parser.setApplicationDescription("My GUI Application");
    parser.addHelpOption();
    parser.addVersionOption();
    
    // 添加自定义选项
    QCommandLineOption verboseOption(QStringList() << "v" << "verbose",
                                     "Enable verbose mode");
    parser.addOption(verboseOption);
    
    QCommandLineOption sizeOption(QStringList() << "s" << "size",
                                  "Window size (WxH)", "size");
    parser.addOption(sizeOption);
    
    parser.process(app);
    
    bool verbose = parser.isSet(verboseOption);
    QString sizeStr = parser.value(sizeOption);
    
    // 处理参数...
    
    return app.exec();
}
```

---

## 4.2 2D 绘图系统（QPainter）

Qt 提供了强大的 2D 绘图系统，基于 `QPainter` 类。

### 4.2.1 基础绘图

```cpp
// [C++] 自定义绘制窗口
#include <QWindow>
#include <QPainter>
#include <QPaintEvent>
#include <QBackingStore>

class PaintWindow : public QWindow
{
public:
    PaintWindow() : m_backingStore(this) {
        setGeometry(100, 100, 800, 600);
    }
    
protected:
    void exposeEvent(QExposeEvent *) override {
        if (isExposed()) {
            render();
        }
    }
    
    void render() {
        QRect rect(0, 0, width(), height());
        m_backingStore.beginPaint(rect);
        
        QPainter painter(m_backingStore.paintDevice());
        
        // 填充背景
        painter.fillRect(rect, Qt::white);
        
        // 绘制基本形状
        painter.setPen(QPen(Qt::red, 2));
        painter.drawRect(10, 10, 100, 80);
        
        painter.setBrush(Qt::green);
        painter.drawEllipse(120, 10, 100, 80);
        
        painter.setPen(QPen(Qt::blue, 3));
        painter.drawLine(10, 100, 220, 100);
        
        // 绘制文本
        painter.setPen(Qt::black);
        painter.setFont(QFont("Arial", 16));
        painter.drawText(10, 150, "Hello QPainter!");
        
        painter.end();
        m_backingStore.endPaint();
        m_backingStore.flush(rect);
    }
    
private:
    QBackingStore m_backingStore;
};
```

```python
# [Python] 自定义绘制
from PySide6.QtWidgets import QWidget, QApplication
from PySide6.QtGui import QPainter, QPen, QBrush, QFont
from PySide6.QtCore import Qt, QRect

class PaintWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("QPainter Demo")
        self.resize(800, 600)
    
    def paintEvent(self, event):
        painter = QPainter(self)
        
        # 填充背景
        painter.fillRect(self.rect(), Qt.white)
        
        # 绘制矩形
        painter.setPen(QPen(Qt.red, 2))
        painter.drawRect(10, 10, 100, 80)
        
        # 绘制椭圆
        painter.setBrush(Qt.green)
        painter.drawEllipse(120, 10, 100, 80)
        
        # 绘制线条
        painter.setPen(QPen(Qt.blue, 3))
        painter.drawLine(10, 100, 220, 100)
        
        # 绘制文本
        painter.setPen(Qt.black)
        painter.setFont(QFont("Arial", 16))
        painter.drawText(10, 150, "Hello QPainter!")
        
        painter.end()

app = QApplication([])
widget = PaintWidget()
widget.show()
app.exec()
```

### 4.2.2 高级绘图

```cpp
// [C++] 渐变和变换
void advancedDrawing(QPainter &painter, const QRect &rect)
{
    // 线性渐变
    QLinearGradient linearGradient(0, 0, rect.width(), rect.height());
    linearGradient.setColorAt(0, Qt::red);
    linearGradient.setColorAt(0.5, Qt::green);
    linearGradient.setColorAt(1, Qt::blue);
    painter.fillRect(rect, linearGradient);
    
    // 径向渐变
    QRadialGradient radialGradient(200, 200, 100);
    radialGradient.setColorAt(0, Qt::white);
    radialGradient.setColorAt(1, Qt::black);
    painter.setBrush(radialGradient);
    painter.drawEllipse(150, 150, 100, 100);
    
    // 坐标变换
    painter.save();  // 保存状态
    painter.translate(300, 200);
    painter.rotate(45);
    painter.scale(1.5, 1.5);
    painter.drawRect(-50, -50, 100, 100);
    painter.restore();  // 恢复状态
    
    // 抗锯齿
    painter.setRenderHint(QPainter::Antialiasing, true);
    painter.drawEllipse(400, 200, 80, 80);
    
    // 裁剪路径
    QPainterPath path;
    path.addEllipse(500, 100, 150, 150);
    painter.setClipPath(path);
    painter.fillRect(rect, Qt::yellow);
}
```

---

## 4.3 图像处理

### 4.3.1 QImage 和 QPixmap

```cpp
// [C++] 图像操作
#include <QImage>
#include <QPixmap>
#include <QPainter>
#include <QFile>

void imageOperations()
{
    // 创建图像
    QImage image(400, 300, QImage::Format_ARGB32);
    image.fill(Qt::transparent);
    
    // 在图像上绘制
    QPainter painter(&image);
    painter.setBrush(Qt::red);
    painter.drawEllipse(50, 50, 100, 100);
    painter.end();
    
    // 保存图像
    image.save("output.png", "PNG");
    
    // 加载图像
    QImage loadedImage("input.jpg");
    if (!loadedImage.isNull()) {
        // 缩放
        QImage scaled = loadedImage.scaled(200, 150, 
                                           Qt::KeepAspectRatio, 
                                           Qt::SmoothTransformation);
        
        // 旋转
        QImage rotated = loadedImage.transformed(
            QTransform().rotate(90));
        
        // 镜像
        QImage mirrored = loadedImage.mirrored(true, false);
        
        // 像素操作
        for (int y = 0; y < loadedImage.height(); ++y) {
            for (int x = 0; x < loadedImage.width(); ++x) {
                QColor color = loadedImage.pixelColor(x, y);
                // 转换为灰度
                int gray = qGray(color.rgb());
                loadedImage.setPixelColor(x, y, QColor(gray, gray, gray));
            }
        }
    }
    
    // QPixmap - 针对屏幕显示优化
    QPixmap pixmap = QPixmap::fromImage(image);
}
```

```python
# [Python] 图像处理
from PySide6.QtGui import QImage, QPixmap, QPainter, QColor, QTransform
from PySide6.QtCore import Qt

def image_operations():
    # 创建图像
    image = QImage(400, 300, QImage.Format_ARGB32)
    image.fill(Qt.transparent)
    
    # 绘制
    painter = QPainter(image)
    painter.setBrush(Qt.red)
    painter.drawEllipse(50, 50, 100, 100)
    painter.end()
    
    # 保存
    image.save("output.png", "PNG")
    
    # 加载和处理
    loaded = QImage("input.jpg")
    if not loaded.isNull():
        # 缩放
        scaled = loaded.scaled(200, 150, 
                               Qt.KeepAspectRatio,
                               Qt.SmoothTransformation)
        
        # 旋转
        transform = QTransform().rotate(90)
        rotated = loaded.transformed(transform)
        
        # 像素操作 - 灰度转换
        for y in range(loaded.height()):
            for x in range(loaded.width()):
                color = loaded.pixelColor(x, y)
                gray = int(0.299 * color.red() + 
                          0.587 * color.green() + 
                          0.114 * color.blue())
                loaded.setPixelColor(x, y, QColor(gray, gray, gray))
```

### 4.3.2 图标和光标

```cpp
// [C++] 图标和光标
#include <QIcon>
#include <QCursor>
#include <QPixmap>

void iconAndCursor()
{
    // 从文件创建图标
    QIcon icon("app-icon.png");
    
    // 添加不同状态的图标
    icon.addFile("icon-normal.png", QSize(16, 16), QIcon::Normal);
    icon.addFile("icon-disabled.png", QSize(16, 16), QIcon::Disabled);
    icon.addFile("icon-active.png", QSize(16, 16), QIcon::Active);
    
    // 获取特定大小和状态的图标
    QPixmap pixmap = icon.pixmap(QSize(32, 32), QIcon::Normal);
    
    // 自定义光标
    QPixmap cursorPixmap("cursor.png");
    QCursor customCursor(cursorPixmap, 0, 0);  // 热点在左上角
    
    // 使用标准光标
    QCursor waitCursor(Qt::WaitCursor);
    QCursor arrowCursor(Qt::ArrowCursor);
}
```

---

## 4.4 字体系统

### 4.4.1 QFont 和 QFontDatabase

```cpp
// [C++] 字体操作
#include <QFont>
#include <QFontDatabase>
#include <QFontMetrics>
#include <QDebug>

void fontOperations()
{
    // 系统字体列表
    QFontDatabase fontDb;
    QStringList families = fontDb.families();
    for (const QString &family : families) {
        qDebug() << "Font family:" << family;
        QStringList styles = fontDb.styles(family);
        for (const QString &style : styles) {
            qDebug() << "  Style:" << style;
        }
    }
    
    // 创建字体
    QFont font("Arial", 12, QFont::Bold, true);  // 名称, 大小, 粗细, 斜体
    font.setPointSize(14);
    font.setWeight(QFont::Normal);
    font.setItalic(false);
    font.setUnderline(true);
    
    // 字体度量
    QFontMetrics metrics(font);
    int width = metrics.horizontalAdvance("Hello World");
    int height = metrics.height();
    int ascent = metrics.ascent();
    int descent = metrics.descent();
    
    qDebug() << "Text width:" << width;
    qDebug() << "Font height:" << height;
    
    // 加载自定义字体
    int fontId = QFontDatabase::addApplicationFont("custom-font.ttf");
    if (fontId != -1) {
        QString family = QFontDatabase::applicationFontFamilies(fontId).at(0);
        QFont customFont(family);
    }
}
```

```python
# [Python] 字体操作
from PySide6.QtGui import QFont, QFontDatabase, QFontMetrics

def font_operations():
    # 系统字体
    font_db = QFontDatabase()
    families = font_db.families()
    for family in families[:10]:  # 只打印前10个
        print(f"Font family: {family}")
    
    # 创建字体
    font = QFont("Arial", 12, QFont.Bold, True)
    font.setPointSize(14)
    font.setUnderline(True)
    
    # 字体度量
    metrics = QFontMetrics(font)
    width = metrics.horizontalAdvance("Hello World")
    height = metrics.height()
    print(f"Text width: {width}, Font height: {height}")
    
    # 加载自定义字体
    font_id = QFontDatabase.addApplicationFont("custom-font.ttf")
    if font_id != -1:
        family = QFontDatabase.applicationFontFamilies(font_id)[0]
        custom_font = QFont(family)
```

---

## 4.5 GUI 事件处理

### 4.5.1 输入事件

```cpp
// [C++] 处理鼠标和键盘事件
#include <QWindow>
#include <QMouseEvent>
#include <QKeyEvent>
#include <QWheelEvent>

class EventWindow : public QWindow
{
public:
    EventWindow() {
        setGeometry(100, 100, 800, 600);
    }
    
protected:
    // 鼠标按下
    void mousePressEvent(QMouseEvent *event) override {
        if (event->button() == Qt::LeftButton) {
            qDebug() << "Left button pressed at:" << event->pos();
        } else if (event->button() == Qt::RightButton) {
            qDebug() << "Right button pressed at:" << event->pos();
        }
    }
    
    // 鼠标移动
    void mouseMoveEvent(QMouseEvent *event) override {
        if (event->buttons() & Qt::LeftButton) {
            qDebug() << "Dragging at:" << event->pos();
        }
    }
    
    // 鼠标释放
    void mouseReleaseEvent(QMouseEvent *event) override {
        qDebug() << "Mouse released at:" << event->pos();
    }
    
    // 滚轮
    void wheelEvent(QWheelEvent *event) override {
        QPoint delta = event->angleDelta();
        qDebug() << "Wheel delta:" << delta.y();
    }
    
    // 键盘
    void keyPressEvent(QKeyEvent *event) override {
        switch (event->key()) {
            case Qt::Key_Escape:
                close();
                break;
            case Qt::Key_Space:
                qDebug() << "Space pressed";
                break;
            case Qt::Key_A:
                if (event->modifiers() & Qt::ControlModifier) {
                    qDebug() << "Ctrl+A pressed";
                }
                break;
        }
    }
    
    // 键盘释放
    void keyReleaseEvent(QKeyEvent *event) override {
        qDebug() << "Key released:" << event->key();
    }
};
```

```python
# [Python] 事件处理
from PySide6.QtWidgets import QWidget, QApplication
from PySide6.QtCore import Qt
from PySide6.QtGui import QMouseEvent, QKeyEvent, QWheelEvent

class EventWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Event Demo")
        self.resize(800, 600)
        self.setMouseTracking(True)  # 开启鼠标追踪
    
    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            print(f"Left button pressed at: {event.pos()}")
        elif event.button() == Qt.RightButton:
            print(f"Right button pressed at: {event.pos()}")
    
    def mouseMoveEvent(self, event: QMouseEvent):
        if event.buttons() & Qt.LeftButton:
            print(f"Dragging at: {event.pos()}")
    
    def mouseReleaseEvent(self, event: QMouseEvent):
        print(f"Mouse released at: {event.pos()}")
    
    def wheelEvent(self, event: QWheelEvent):
        delta = event.angleDelta()
        print(f"Wheel delta: {delta.y()}")
    
    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key_Escape:
            self.close()
        elif event.key() == Qt.Key_Space:
            print("Space pressed")
        elif event.key() == Qt.Key_A and event.modifiers() & Qt.ControlModifier:
            print("Ctrl+A pressed")
    
    def keyReleaseEvent(self, event: QKeyEvent):
        print(f"Key released: {event.key()}")

app = QApplication([])
widget = EventWidget()
widget.show()
app.exec()
```

### 4.5.2 拖拽事件

```cpp
// [C++] 拖拽操作
#include <QMimeData>
#include <QDrag>

void dragStart(QWidget *source)
{
    QDrag *drag = new QDrag(source);
    QMimeData *mimeData = new QMimeData;
    
    mimeData->setText("Dragged text");
    mimeData->setUrls({QUrl::fromLocalFile("/path/to/file")});
    
    drag->setMimeData(mimeData);
    
    // 设置拖拽图像
    QPixmap pixmap(100, 50);
    pixmap.fill(Qt::lightGray);
    drag->setPixmap(pixmap);
    
    Qt::DropAction result = drag->exec(Qt::CopyAction | Qt::MoveAction);
    if (result == Qt::CopyAction) {
        qDebug() << "Copied";
    } else if (result == Qt::MoveAction) {
        qDebug() << "Moved";
    }
}

// 接收拖拽
void dragEnterEvent(QDragEnterEvent *event) override {
    if (event->mimeData()->hasText() || 
        event->mimeData()->hasUrls()) {
        event->acceptProposedAction();
    }
}

void dropEvent(QDropEvent *event) override {
    const QMimeData *mimeData = event->mimeData();
    
    if (mimeData->hasText()) {
        QString text = mimeData->text();
        qDebug() << "Dropped text:" << text;
    }
    
    if (mimeData->hasUrls()) {
        QList<QUrl> urls = mimeData->urls();
        for (const QUrl &url : urls) {
            qDebug() << "Dropped file:" << url.toLocalFile();
        }
    }
    
    event->acceptProposedAction();
}
```

---

## 4.6 窗口系统

### 4.6.1 窗口属性

```cpp
// [C++] 窗口控制
#include <QWindow>
#include <QScreen>

void windowOperations(QWindow *window)
{
    // 基本属性
    window->setTitle("My Window");
    window->setIcon(QIcon("app-icon.png"));
    
    // 窗口标志
    window->setFlags(Qt::Window | Qt::WindowTitleHint | 
                     Qt::WindowCloseButtonHint);
    
    // 窗口状态
    window->showNormal();
    window->showMaximized();
    window->showMinimized();
    window->showFullScreen();
    
    // 几何控制
    window->setGeometry(100, 100, 800, 600);
    window->setMinimumSize(400, 300);
    window->setMaximumSize(1920, 1080);
    window->setFixedSize(800, 600);
    
    // 透明度
    window->setOpacity(0.8);  // 80% 不透明
    
    // 屏幕管理
    QScreen *screen = window->screen();
    window->setScreen(screen);
    
    // 移动到其他屏幕
    QList<QScreen*> screens = QGuiApplication::screens();
    if (screens.size() > 1) {
        window->setScreen(screens[1]);
    }
}
```

### 4.6.2 剪切板和拖拽

```cpp
// [C++] 剪切板操作
#include <QClipboard>
#include <QGuiApplication>
#include <QMimeData>

void clipboardOperations()
{
    QClipboard *clipboard = QGuiApplication::clipboard();
    
    // 复制文本
    clipboard->setText("Hello Clipboard");
    
    // 粘贴文本
    QString text = clipboard->text();
    qDebug() << "Clipboard text:" << text;
    
    // 复制图像
    QImage image("image.png");
    clipboard->setImage(image);
    
    // 粘贴图像
    QImage clipboardImage = clipboard->image();
    
    // 复杂 MIME 数据
    QMimeData *mimeData = new QMimeData();
    mimeData->setHtml("<b>Bold</b> and <i>italic</i>");
    mimeData->setText("Bold and italic");
    clipboard->setMimeData(mimeData);
}
```

---

## 4.7 本章小结

本章介绍了 Qt GUI 模块的核心功能：

| 主题 | 关键类 | 主要用途 |
|------|--------|----------|
| GUI 应用 | `QGuiApplication` | 应用入口、屏幕管理 |
| 2D 绘图 | `QPainter` | 绘制基本形状、文本、图像 |
| 图像 | `QImage`, `QPixmap` | 图像加载、处理、保存 |
| 字体 | `QFont`, `QFontDatabase` | 字体管理、度量 |
| 事件 | `QMouseEvent`, `QKeyEvent` | 输入处理 |
| 窗口 | `QWindow` | 窗口管理 |
| 剪切板 | `QClipboard` | 数据共享 |

在下一章中，我们将学习 Qt Widgets 模块，探索丰富的控件库和布局系统。
