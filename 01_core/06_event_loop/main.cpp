/**
 * Qt6 事件循环示例
 *
 * Qt 应用的核心是事件循环：
 * - QCoreApplication: 控制台应用
 * - QGuiApplication: GUI 应用 (无 Widgets)
 * - QApplication: Widgets 应用
 *
 * 事件循环处理：
 * - 系统事件 (鼠标、键盘)
 * - 定时器事件
 * - 自定义事件
 * - 信号槽调用
 *
 * 官方文档: https://doc.qt.io/qt-6/eventsandfilters.html
 */

#include <QCoreApplication>
#include <QObject>
#include <QEvent>
#include <QTimer>
#include <QDebug>

// 自定义事件类型
class CustomEvent : public QEvent
{
public:
    static const QEvent::Type EventType;

    explicit CustomEvent(const QString &message)
        : QEvent(EventType), m_message(message) {}

    QString message() const { return m_message; }

private:
    QString m_message;
};

// 注册自定义事件类型
const QEvent::Type CustomEvent::EventType =
    static_cast<QEvent::Type>(QEvent::registerEventType());

// 事件接收者
class EventReceiver : public QObject
{
    Q_OBJECT

public:
    explicit EventReceiver(QObject *parent = nullptr)
        : QObject(parent) {}

protected:
    // 重写事件处理
    bool event(QEvent *event) override {
        if (event->type() == CustomEvent::EventType) {
            auto *customEvent = static_cast<CustomEvent*>(event);
            qDebug() << "收到自定义事件:" << customEvent->message();
            emit customEventReceived(customEvent->message());
            return true;
        }
        return QObject::event(event);
    }

signals:
    void customEventReceived(const QString &message);
};

// 事件过滤器示例
class EventFilter : public QObject
{
    Q_OBJECT

public:
    explicit EventFilter(QObject *parent = nullptr)
        : QObject(parent) {}

protected:
    bool eventFilter(QObject *watched, QEvent *event) override {
        if (event->type() == CustomEvent::EventType) {
            qDebug() << "事件过滤器拦截了来自" << watched->objectName() << "的事件";
            // 返回 true 表示事件已处理，不再传递
            // 返回 false 表示继续传递事件
            return false;  // 继续传递
        }
        return QObject::eventFilter(watched, event);
    }
};

void demonstrateEventPosting()
{
    qDebug() << "\n=== 事件发送示例 ===\n";

    EventReceiver receiver;
    receiver.setObjectName("TestReceiver");

    // 安装事件过滤器
    EventFilter filter;
    receiver.installEventFilter(&filter);

    QObject::connect(&receiver, &EventReceiver::customEventReceived,
                     [](const QString &msg) {
                         qDebug() << "信号槽收到:" << msg;
                     });

    // postEvent: 异步发送 (推荐)
    qDebug() << "--- postEvent (异步) ---";
    QCoreApplication::postEvent(&receiver,
        new CustomEvent("异步消息1"));
    QCoreApplication::postEvent(&receiver,
        new CustomEvent("异步消息2"));
    qDebug() << "事件已投递到队列";

    // 处理所有待处理事件
    QCoreApplication::processEvents();

    // sendEvent: 同步发送 (立即处理)
    qDebug() << "\n--- sendEvent (同步) ---";
    CustomEvent syncEvent("同步消息");
    qDebug() << "发送前";
    QCoreApplication::sendEvent(&receiver, &syncEvent);
    qDebug() << "发送后 (已处理)";
}

void demonstrateQueuedInvoke()
{
    qDebug() << "\n=== 队列调用示例 ===\n";

    // 在下一次事件循环迭代中执行
    QMetaObject::invokeMethod(
        QCoreApplication::instance(),
        []() {
            qDebug() << "队列调用执行";
        },
        Qt::QueuedConnection
    );

    qDebug() << "队列调用已安排";
    QCoreApplication::processEvents();
}

int main(int argc, char *argv[])
{
    QCoreApplication app(argc, argv);
    app.setApplicationName("EventLoopDemo");

    qDebug() << "=== Qt6 事件循环示例 ===";

    qDebug() << "\n应用信息:";
    qDebug() << "应用名称:" << QCoreApplication::applicationName();
    qDebug() << "应用目录:" << QCoreApplication::applicationDirPath();
    qDebug() << "应用文件:" << QCoreApplication::applicationFilePath();
    qDebug() << "参数:" << QCoreApplication::arguments();

    demonstrateEventPosting();
    demonstrateQueuedInvoke();

    // 延迟退出
    qDebug() << "\n--- 事件循环控制 ---";
    qDebug() << "使用 singleShot 延迟操作";

    int counter = 0;
    QTimer timer;
    QObject::connect(&timer, &QTimer::timeout, [&counter]() {
        qDebug() << "定时器触发 #" << ++counter;
    });
    timer.start(100);  // 每100ms触发

    // 500ms 后退出
    QTimer::singleShot(550, &app, []() {
        qDebug() << "\n500ms 到达，退出事件循环";
        QCoreApplication::quit();
    });

    qDebug() << "进入事件循环...";
    return app.exec();  // 阻塞直到 quit() 被调用
}

#include "main.moc"
