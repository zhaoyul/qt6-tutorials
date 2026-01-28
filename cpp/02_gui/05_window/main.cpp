/**
 * Qt6 窗口系统示例
 *
 * QWindow 是 Qt GUI 的底层窗口类：
 * - 不依赖 Qt Widgets
 * - 可用于 OpenGL、Vulkan 渲染
 * - QWidget 内部使用 QWindow
 *
 * 主要功能：
 * - 窗口属性 (标题、大小、位置)
 * - 窗口状态 (最大化、最小化、全屏)
 * - 窗口标志 (无边框、置顶)
 * - 屏幕信息
 *
 * 官方文档: https://doc.qt.io/qt-6/qwindow.html
 */

#include <QGuiApplication>
#include <QWindow>
#include <QScreen>
#include <QBackingStore>
#include <QPainter>
#include <QResizeEvent>
#include <QKeyEvent>
#include <QDebug>

class DemoWindow : public QWindow
{
public:
    explicit DemoWindow(QWindow *parent = nullptr)
        : QWindow(parent)
        , m_backingStore(new QBackingStore(this))
    {
        // 窗口属性
        setTitle("Qt6 Window Demo");
        resize(500, 400);

        // 设置最小/最大尺寸
        setMinimumSize(QSize(300, 200));
        setMaximumSize(QSize(800, 600));

        // 窗口图标 (如果有)
        // setIcon(QIcon("icon.png"));
    }

    void showWindowInfo()
    {
        qDebug() << "\n=== 窗口信息 ===";
        qDebug() << "标题:" << title();
        qDebug() << "大小:" << size();
        qDebug() << "位置:" << position();
        qDebug() << "几何:" << geometry();
        qDebug() << "最小大小:" << minimumSize();
        qDebug() << "最大大小:" << maximumSize();
        qDebug() << "可见:" << isVisible();
        qDebug() << "活跃:" << isActive();
        qDebug() << "窗口状态:" << windowState();
        qDebug() << "窗口类型:" << type();
        qDebug() << "不透明度:" << opacity();
    }

protected:
    void exposeEvent(QExposeEvent *event) override
    {
        Q_UNUSED(event);
        if (isExposed())
            render();
    }

    void resizeEvent(QResizeEvent *event) override
    {
        m_backingStore->resize(event->size());
        if (isExposed())
            render();
    }

    void keyPressEvent(QKeyEvent *event) override
    {
        switch (event->key()) {
            case Qt::Key_1:
                // 普通状态
                setWindowState(Qt::WindowNoState);
                qDebug() << "窗口状态: 普通";
                break;
            case Qt::Key_2:
                // 最大化
                setWindowState(Qt::WindowMaximized);
                qDebug() << "窗口状态: 最大化";
                break;
            case Qt::Key_3:
                // 最小化
                setWindowState(Qt::WindowMinimized);
                qDebug() << "窗口状态: 最小化";
                break;
            case Qt::Key_4:
                // 全屏
                setWindowState(Qt::WindowFullScreen);
                qDebug() << "窗口状态: 全屏";
                break;
            case Qt::Key_5:
                // 置顶
                setFlags(flags() ^ Qt::WindowStaysOnTopHint);
                qDebug() << "切换置顶";
                break;
            case Qt::Key_6:
                // 调整不透明度
                setOpacity(opacity() > 0.5 ? 0.5 : 1.0);
                qDebug() << "不透明度:" << opacity();
                break;
            case Qt::Key_I:
                showWindowInfo();
                break;
            case Qt::Key_Escape:
                if (windowState() == Qt::WindowFullScreen) {
                    setWindowState(Qt::WindowNoState);
                } else {
                    close();
                }
                break;
        }
        render();
    }

private:
    void render()
    {
        if (!isExposed())
            return;

        QRect rect(0, 0, width(), height());
        m_backingStore->beginPaint(rect);

        QPainter painter(m_backingStore->paintDevice());
        painter.setRenderHint(QPainter::Antialiasing);
        painter.fillRect(rect, QColor(250, 250, 250));

        painter.setPen(Qt::darkBlue);
        painter.setFont(QFont("Arial", 18, QFont::Bold));
        painter.drawText(20, 40, "Qt6 Window System Demo");

        painter.setPen(Qt::black);
        painter.setFont(QFont("Arial", 12));

        int y = 80;
        painter.drawText(20, y, "按键控制:"); y += 25;
        painter.drawText(20, y, "1 - 普通窗口"); y += 20;
        painter.drawText(20, y, "2 - 最大化"); y += 20;
        painter.drawText(20, y, "3 - 最小化"); y += 20;
        painter.drawText(20, y, "4 - 全屏 (ESC 退出)"); y += 20;
        painter.drawText(20, y, "5 - 切换置顶"); y += 20;
        painter.drawText(20, y, "6 - 切换透明度"); y += 20;
        painter.drawText(20, y, "I - 显示窗口信息"); y += 20;
        painter.drawText(20, y, "ESC - 退出"); y += 35;

        // 显示当前状态
        painter.setPen(Qt::darkGreen);
        QString state;
        switch (windowState()) {
            case Qt::WindowNoState: state = "普通"; break;
            case Qt::WindowMinimized: state = "最小化"; break;
            case Qt::WindowMaximized: state = "最大化"; break;
            case Qt::WindowFullScreen: state = "全屏"; break;
            default: state = "未知";
        }
        painter.drawText(20, y, QString("当前状态: %1").arg(state)); y += 20;
        painter.drawText(20, y, QString("窗口大小: %1x%2").arg(width()).arg(height())); y += 20;
        painter.drawText(20, y, QString("不透明度: %1").arg(opacity()));

        painter.end();

        m_backingStore->endPaint();
        m_backingStore->flush(rect);
    }

    QBackingStore *m_backingStore;
};

void showScreenInfo()
{
    qDebug() << "=== 屏幕信息 ===\n";

    QList<QScreen*> screens = QGuiApplication::screens();
    qDebug() << "屏幕数量:" << screens.size();

    for (int i = 0; i < screens.size(); ++i) {
        QScreen *screen = screens[i];
        qDebug() << "\n屏幕" << i + 1 << ":";
        qDebug() << "  名称:" << screen->name();
        qDebug() << "  几何:" << screen->geometry();
        qDebug() << "  可用几何:" << screen->availableGeometry();
        qDebug() << "  虚拟几何:" << screen->virtualGeometry();
        qDebug() << "  物理尺寸:" << screen->physicalSize() << "mm";
        qDebug() << "  逻辑 DPI:" << screen->logicalDotsPerInch();
        qDebug() << "  物理 DPI:" << screen->physicalDotsPerInch();
        qDebug() << "  设备像素比:" << screen->devicePixelRatio();
        qDebug() << "  刷新率:" << screen->refreshRate() << "Hz";
        qDebug() << "  色深:" << screen->depth() << "bits";
        qDebug() << "  方向:" << screen->orientation();
    }

    QScreen *primary = QGuiApplication::primaryScreen();
    qDebug() << "\n主屏幕:" << primary->name();
}

void showWindowTypes()
{
    qDebug() << "\n=== 窗口类型 (Qt::WindowType) ===\n";

    qDebug() << "Qt::Window - 独立窗口";
    qDebug() << "Qt::Dialog - 对话框";
    qDebug() << "Qt::Sheet - macOS 表单";
    qDebug() << "Qt::Popup - 弹出菜单";
    qDebug() << "Qt::Tool - 工具窗口";
    qDebug() << "Qt::ToolTip - 提示框";
    qDebug() << "Qt::SplashScreen - 启动画面";

    qDebug() << "\n=== 窗口标志 (Qt::WindowFlags) ===\n";

    qDebug() << "Qt::FramelessWindowHint - 无边框";
    qDebug() << "Qt::WindowStaysOnTopHint - 置顶";
    qDebug() << "Qt::WindowStaysOnBottomHint - 置底";
    qDebug() << "Qt::WindowTransparentForInput - 穿透点击";
    qDebug() << "Qt::WindowMinMaxButtonsHint - 最小化/最大化按钮";
    qDebug() << "Qt::WindowCloseButtonHint - 关闭按钮";
}

int main(int argc, char *argv[])
{
    QGuiApplication app(argc, argv);

    qDebug() << "=== Qt6 窗口系统示例 ===";

    showScreenInfo();
    showWindowTypes();

    DemoWindow window;
    window.show();

    return app.exec();
}
