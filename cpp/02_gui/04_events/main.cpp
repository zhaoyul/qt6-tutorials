/**
 * Qt6 GUI事件系统示例
 *
 * Qt GUI 事件类型：
 * - QKeyEvent: 键盘事件
 * - QMouseEvent: 鼠标事件
 * - QWheelEvent: 滚轮事件
 * - QResizeEvent: 窗口大小改变
 * - QPaintEvent: 绘制事件
 * - QFocusEvent: 焦点事件
 * - QCloseEvent: 关闭事件
 *
 * 事件处理流程：
 * 1. 事件到达 QGuiApplication
 * 2. 分发到目标窗口
 * 3. 事件过滤器
 * 4. 目标的 event() 方法
 * 5. 特定事件处理器 (keyPressEvent 等)
 *
 * 官方文档: https://doc.qt.io/qt-6/eventsandfilters.html
 */

#include <QGuiApplication>
#include <QWindow>
#include <QBackingStore>
#include <QPainter>
#include <QKeyEvent>
#include <QMouseEvent>
#include <QDebug>

// 自定义窗口，演示事件处理
class EventWindow : public QWindow
{
public:
    explicit EventWindow(QWindow *parent = nullptr)
        : QWindow(parent)
        , m_backingStore(new QBackingStore(this))
    {
        setTitle("Qt6 GUI Events Demo - Press keys, click mouse");
        resize(400, 300);
        setMinimumSize(QSize(200, 150));

        m_lastEvent = "等待事件...";
        m_mousePos = QPoint(0, 0);
    }

protected:
    // 曝光事件 (窗口需要重绘)
    void exposeEvent(QExposeEvent *event) override
    {
        Q_UNUSED(event);
        if (isExposed())
            renderNow();
    }

    // 大小改变事件
    void resizeEvent(QResizeEvent *event) override
    {
        m_backingStore->resize(event->size());
        m_lastEvent = QString("Resize: %1x%2")
            .arg(event->size().width())
            .arg(event->size().height());

        qDebug() << "窗口大小改变:" << event->oldSize() << "->" << event->size();

        if (isExposed())
            renderNow();
    }

    // 键盘按下事件
    void keyPressEvent(QKeyEvent *event) override
    {
        QString keyText = event->text().isEmpty() ?
            QKeySequence(event->key()).toString() : event->text();

        m_lastEvent = QString("KeyPress: %1 (key=%2)")
            .arg(keyText)
            .arg(event->key());

        qDebug() << "键盘按下:";
        qDebug() << "  键值:" << event->key();
        qDebug() << "  文本:" << event->text();
        qDebug() << "  修饰符:" << event->modifiers();
        qDebug() << "  自动重复:" << event->isAutoRepeat();

        // 检查修饰键
        if (event->modifiers() & Qt::ControlModifier) {
            qDebug() << "  Ctrl 被按下";
        }
        if (event->modifiers() & Qt::ShiftModifier) {
            qDebug() << "  Shift 被按下";
        }

        // ESC 关闭窗口
        if (event->key() == Qt::Key_Escape) {
            close();
            return;
        }

        renderNow();
    }

    // 键盘释放事件
    void keyReleaseEvent(QKeyEvent *event) override
    {
        qDebug() << "键盘释放:" << event->key();
    }

    // 鼠标按下事件
    void mousePressEvent(QMouseEvent *event) override
    {
        m_mousePos = event->position().toPoint();
        QString button;
        switch (event->button()) {
            case Qt::LeftButton: button = "Left"; break;
            case Qt::RightButton: button = "Right"; break;
            case Qt::MiddleButton: button = "Middle"; break;
            default: button = "Other";
        }

        m_lastEvent = QString("MousePress: %1 at (%2, %3)")
            .arg(button)
            .arg(m_mousePos.x())
            .arg(m_mousePos.y());

        qDebug() << "鼠标按下:";
        qDebug() << "  按钮:" << event->button();
        qDebug() << "  位置:" << event->position();
        qDebug() << "  全局位置:" << event->globalPosition();
        qDebug() << "  所有按下的按钮:" << event->buttons();

        renderNow();
    }

    // 鼠标释放事件
    void mouseReleaseEvent(QMouseEvent *event) override
    {
        qDebug() << "鼠标释放:" << event->button() << "at" << event->position();
    }

    // 鼠标移动事件
    void mouseMoveEvent(QMouseEvent *event) override
    {
        m_mousePos = event->position().toPoint();
        m_lastEvent = QString("MouseMove: (%1, %2)")
            .arg(m_mousePos.x())
            .arg(m_mousePos.y());

        renderNow();
    }

    // 鼠标双击事件
    void mouseDoubleClickEvent(QMouseEvent *event) override
    {
        m_lastEvent = QString("DoubleClick at (%1, %2)")
            .arg(event->position().x())
            .arg(event->position().y());

        qDebug() << "鼠标双击:" << event->position();

        renderNow();
    }

    // 滚轮事件
    void wheelEvent(QWheelEvent *event) override
    {
        QPoint delta = event->angleDelta();
        m_lastEvent = QString("Wheel: delta=(%1, %2)")
            .arg(delta.x())
            .arg(delta.y());

        qDebug() << "滚轮事件:";
        qDebug() << "  角度增量:" << delta;
        qDebug() << "  像素增量:" << event->pixelDelta();

        renderNow();
    }

    // 焦点进入事件
    void focusInEvent(QFocusEvent *event) override
    {
        qDebug() << "获得焦点, 原因:" << event->reason();
        m_lastEvent = "FocusIn";
        renderNow();
    }

    // 焦点离开事件
    void focusOutEvent(QFocusEvent *event) override
    {
        qDebug() << "失去焦点, 原因:" << event->reason();
        m_lastEvent = "FocusOut";
        renderNow();
    }

    // 通用事件处理器
    bool event(QEvent *event) override
    {
        // 可以在这里拦截所有事件
        switch (event->type()) {
            case QEvent::Enter:
                qDebug() << "鼠标进入窗口";
                break;
            case QEvent::Leave:
                qDebug() << "鼠标离开窗口";
                break;
            default:
                break;
        }

        return QWindow::event(event);
    }

private:
    void renderNow()
    {
        if (!isExposed())
            return;

        QRect rect(0, 0, width(), height());
        m_backingStore->beginPaint(rect);

        QPainter painter(m_backingStore->paintDevice());
        painter.setRenderHint(QPainter::Antialiasing);

        // 背景
        painter.fillRect(rect, QColor(240, 240, 240));

        // 标题
        painter.setPen(Qt::darkBlue);
        painter.setFont(QFont("Arial", 16, QFont::Bold));
        painter.drawText(10, 30, "Qt6 GUI Events Demo");

        // 说明
        painter.setPen(Qt::black);
        painter.setFont(QFont("Arial", 11));
        painter.drawText(10, 55, "按键盘、移动鼠标、点击、滚轮来测试事件");
        painter.drawText(10, 75, "按 ESC 退出");

        // 最后事件
        painter.setPen(Qt::darkGreen);
        painter.setFont(QFont("Arial", 14));
        painter.drawText(10, 120, "最后事件: " + m_lastEvent);

        // 鼠标位置
        painter.setPen(Qt::darkRed);
        painter.drawText(10, 150, QString("鼠标位置: (%1, %2)")
                        .arg(m_mousePos.x()).arg(m_mousePos.y()));

        // 绘制鼠标位置标记
        painter.setBrush(Qt::red);
        painter.drawEllipse(m_mousePos, 5, 5);

        // 窗口大小
        painter.setPen(Qt::gray);
        painter.setFont(QFont("Arial", 10));
        painter.drawText(10, height() - 10,
            QString("窗口大小: %1x%2").arg(width()).arg(height()));

        painter.end();

        m_backingStore->endPaint();
        m_backingStore->flush(rect);
    }

    QBackingStore *m_backingStore;
    QString m_lastEvent;
    QPoint m_mousePos;
};

int main(int argc, char *argv[])
{
    QGuiApplication app(argc, argv);

    qDebug() << "=== Qt6 GUI事件系统示例 ===";
    qDebug() << "窗口将显示并响应各种事件";
    qDebug() << "事件信息将打印到控制台\n";

    EventWindow window;
    window.show();

    return app.exec();
}
