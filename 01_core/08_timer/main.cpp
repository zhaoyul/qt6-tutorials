/**
 * Qt6 定时器示例
 *
 * Qt 提供多种定时功能：
 * - QTimer: 高级定时器类
 * - QObject::startTimer: 基础定时器
 * - QElapsedTimer: 计时器 (测量时间)
 * - QDeadlineTimer: 截止时间
 *
 * 定时器类型：
 * - Qt::PreciseTimer: 精确定时
 * - Qt::CoarseTimer: 粗略定时 (节能)
 * - Qt::VeryCoarseTimer: 非常粗略
 *
 * 官方文档: https://doc.qt.io/qt-6/timers.html
 */

#include <QCoreApplication>
#include <QObject>
#include <QTimer>
#include <QElapsedTimer>
#include <QDeadlineTimer>
#include <QThread>
#include <QDebug>

class TimerDemo : public QObject
{
    Q_OBJECT

public:
    explicit TimerDemo(QObject *parent = nullptr)
        : QObject(parent), m_count(0) {}

    void demonstrateQTimer()
    {
        qDebug() << "\n=== QTimer 示例 ===\n";

        // 重复定时器
        m_repeatTimer = new QTimer(this);
        connect(m_repeatTimer, &QTimer::timeout, this, &TimerDemo::onRepeatTimeout);
        m_repeatTimer->start(100);  // 100ms 间隔

        qDebug() << "重复定时器已启动 (100ms 间隔)";
    }

    void demonstrateSingleShot()
    {
        qDebug() << "\n=== singleShot 示例 ===\n";

        // 方式1: 静态方法 + Lambda
        QTimer::singleShot(200, []() {
            qDebug() << "singleShot Lambda 执行";
        });

        // 方式2: 静态方法 + 对象槽
        QTimer::singleShot(300, this, &TimerDemo::onSingleShotTimeout);

        // 方式3: 使用 QTimer 对象
        QTimer *timer = new QTimer(this);
        timer->setSingleShot(true);
        connect(timer, &QTimer::timeout, []() {
            qDebug() << "QTimer singleShot 执行";
        });
        timer->start(250);

        qDebug() << "单次定时器已安排";
    }

    void demonstrateTimerTypes()
    {
        qDebug() << "\n=== 定时器类型 ===\n";

        QTimer *preciseTimer = new QTimer(this);
        preciseTimer->setTimerType(Qt::PreciseTimer);
        qDebug() << "精确定时器: 误差 < 1ms";

        QTimer *coarseTimer = new QTimer(this);
        coarseTimer->setTimerType(Qt::CoarseTimer);
        qDebug() << "粗略定时器: 误差 ~5%，节省电量";

        QTimer *veryCoarseTimer = new QTimer(this);
        veryCoarseTimer->setTimerType(Qt::VeryCoarseTimer);
        qDebug() << "非常粗略定时器: 整秒级别";
    }

protected:
    // 基础定时器 (QObject 内置)
    void timerEvent(QTimerEvent *event) override
    {
        if (event->timerId() == m_basicTimerId) {
            qDebug() << "基础定时器触发";
        }
    }

public slots:
    void onRepeatTimeout()
    {
        ++m_count;
        qDebug() << "重复定时器 #" << m_count;

        if (m_count >= 5) {
            m_repeatTimer->stop();
            qDebug() << "重复定时器已停止";

            // 停止所有定时器后退出
            QTimer::singleShot(100, qApp, &QCoreApplication::quit);
        }
    }

    void onSingleShotTimeout()
    {
        qDebug() << "singleShot 槽执行";
    }

    void startBasicTimer()
    {
        qDebug() << "\n=== 基础定时器 (startTimer) ===\n";
        m_basicTimerId = startTimer(150);
        qDebug() << "基础定时器 ID:" << m_basicTimerId;

        // 停止基础定时器
        QTimer::singleShot(400, this, [this]() {
            killTimer(m_basicTimerId);
            qDebug() << "基础定时器已停止";
        });
    }

private:
    QTimer *m_repeatTimer = nullptr;
    int m_basicTimerId = 0;
    int m_count;
};

void demonstrateElapsedTimer()
{
    qDebug() << "\n=== QElapsedTimer (计时) ===\n";

    QElapsedTimer timer;
    timer.start();

    // 模拟工作
    volatile int sum = 0;
    for (int i = 0; i < 1000000; ++i) {
        sum += i;
    }

    qDebug() << "耗时:" << timer.elapsed() << "ms";
    qDebug() << "耗时 (纳秒):" << timer.nsecsElapsed() << "ns";

    // 重启计时
    timer.restart();
    QThread::msleep(50);
    qDebug() << "sleep 50ms 实际耗时:" << timer.elapsed() << "ms";

    // 检查是否过期
    timer.restart();
    qDebug() << "已过去 100ms:" << timer.hasExpired(100);
}

void demonstrateDeadlineTimer()
{
    qDebug() << "\n=== QDeadlineTimer (截止时间) ===\n";

    // 设置 100ms 截止时间
    QDeadlineTimer deadline(100);

    qDebug() << "剩余时间:" << deadline.remainingTime() << "ms";
    qDebug() << "已过期:" << deadline.hasExpired();

    QThread::msleep(50);
    qDebug() << "50ms 后剩余:" << deadline.remainingTime() << "ms";

    QThread::msleep(60);
    qDebug() << "110ms 后已过期:" << deadline.hasExpired();

    // 永不过期
    QDeadlineTimer neverExpires(QDeadlineTimer::Forever);
    qDebug() << "永不过期定时器已过期:" << neverExpires.hasExpired();
}

int main(int argc, char *argv[])
{
    QCoreApplication app(argc, argv);

    qDebug() << "=== Qt6 定时器示例 ===";

    demonstrateElapsedTimer();
    demonstrateDeadlineTimer();

    TimerDemo demo;
    demo.demonstrateTimerTypes();
    demo.demonstrateQTimer();
    demo.demonstrateSingleShot();
    demo.startBasicTimer();

    qDebug() << "\n--- 进入事件循环 ---\n";

    return app.exec();
}

#include "main.moc"
