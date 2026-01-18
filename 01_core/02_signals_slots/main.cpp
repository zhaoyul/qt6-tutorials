/**
 * Qt6 信号与槽机制示例
 *
 * 信号与槽是Qt最重要的特性，用于对象间通信：
 * - 信号 (Signal): 当事件发生时发出
 * - 槽 (Slot): 响应信号的函数
 *
 * 连接方式：
 * 1. Qt5 新语法 (推荐): connect(sender, &Sender::signal, receiver, &Receiver::slot)
 * 2. Lambda 表达式: connect(sender, &Sender::signal, [](){ ... })
 * 3. 旧语法: connect(sender, SIGNAL(signal()), receiver, SLOT(slot()))
 *
 * 官方文档: https://doc.qt.io/qt-6/signalsandslots.html
 */

#include <QCoreApplication>
#include <QObject>
#include <QDebug>
#include <QTimer>

// 发送者类
class Counter : public QObject
{
    Q_OBJECT

public:
    explicit Counter(QObject *parent = nullptr)
        : QObject(parent), m_value(0) {}

    int value() const { return m_value; }

public slots:
    void increment() {
        ++m_value;
        emit valueChanged(m_value);

        if (m_value >= 10) {
            emit limitReached();
        }
    }

    void decrement() {
        --m_value;
        emit valueChanged(m_value);
    }

    void setValue(int value) {
        if (m_value != value) {
            m_value = value;
            emit valueChanged(m_value);
        }
    }

signals:
    void valueChanged(int newValue);
    void limitReached();

private:
    int m_value;
};

// 接收者类
class Display : public QObject
{
    Q_OBJECT

public:
    explicit Display(const QString &name, QObject *parent = nullptr)
        : QObject(parent), m_name(name) {}

public slots:
    void showValue(int value) {
        qDebug() << m_name << "显示值:" << value;
    }

    void onLimitReached() {
        qDebug() << m_name << "警告: 已达到上限!";
    }

private:
    QString m_name;
};

int main(int argc, char *argv[])
{
    QCoreApplication app(argc, argv);

    qDebug() << "=== Qt6 信号与槽示例 ===\n";

    Counter counter;
    Display display1("显示器1");
    Display display2("显示器2");

    // ============ 连接方式1: 函数指针 (推荐) ============
    qDebug() << "--- 方式1: 函数指针连接 ---";
    QObject::connect(&counter, &Counter::valueChanged,
                     &display1, &Display::showValue);

    // ============ 连接方式2: Lambda 表达式 ============
    qDebug() << "\n--- 方式2: Lambda 连接 ---";
    QObject::connect(&counter, &Counter::valueChanged,
                     [](int value) {
                         qDebug() << "Lambda 接收到值:" << value;
                     });

    // ============ 一个信号连接多个槽 ============
    qDebug() << "\n--- 一个信号连接多个槽 ---";
    QObject::connect(&counter, &Counter::valueChanged,
                     &display2, &Display::showValue);

    // ============ 信号连接信号 ============
    Counter counter2;
    QObject::connect(&counter, &Counter::limitReached,
                     &counter2, &Counter::increment);
    QObject::connect(&counter2, &Counter::valueChanged,
                     [](int v) { qDebug() << "Counter2 被触发, 值:" << v; });

    // 测试
    qDebug() << "\n--- 测试增加值 ---";
    counter.increment();  // 1
    counter.increment();  // 2

    qDebug() << "\n--- 测试设置值 ---";
    counter.setValue(9);

    qDebug() << "\n--- 触发 limitReached ---";
    counter.increment();  // 10, 触发 limitReached

    // ============ 断开连接 ============
    qDebug() << "\n--- 断开 display2 的连接 ---";
    QObject::disconnect(&counter, &Counter::valueChanged,
                        &display2, &Display::showValue);
    counter.increment();  // display2 不会显示

    // ============ 连接类型 ============
    qDebug() << "\n--- 连接类型说明 ---";
    qDebug() << "Qt::AutoConnection (默认): 自动选择";
    qDebug() << "Qt::DirectConnection: 直接调用 (同步)";
    qDebug() << "Qt::QueuedConnection: 队列调用 (异步)";
    qDebug() << "Qt::UniqueConnection: 防止重复连接";

    // 使用 UniqueConnection 防止重复连接
    auto conn = QObject::connect(&counter, &Counter::valueChanged,
                                 &display1, &Display::showValue,
                                 Qt::UniqueConnection);
    qDebug() << "重复连接结果:" << (conn ? "成功" : "失败(已存在)");

    // ============ 使用 QTimer 单次触发 ============
    qDebug() << "\n--- QTimer::singleShot 示例 ---";
    QTimer::singleShot(100, []() {
        qDebug() << "100ms 后执行的 Lambda";
        QCoreApplication::quit();
    });

    return app.exec();
}

#include "main.moc"
