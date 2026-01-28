/**
 * Qt6 多线程示例
 *
 * Qt 提供多种多线程方式：
 * 1. QThread: 线程类
 * 2. QRunnable + QThreadPool: 任务池
 * 3. QtConcurrent: 高级并发 (见 10_concurrent)
 * 4. QMutex, QReadWriteLock: 同步原语
 *
 * 重要概念：
 * - 线程亲和性 (Thread Affinity)
 * - moveToThread 模式
 * - 跨线程信号槽
 *
 * 官方文档: https://doc.qt.io/qt-6/threads.html
 */

#include <QCoreApplication>
#include <QThread>
#include <QRunnable>
#include <QThreadPool>
#include <QMutex>
#include <QMutexLocker>
#include <QReadWriteLock>
#include <QWaitCondition>
#include <QTimer>
#include <QDebug>

// ============ 方式1: 继承 QThread ============
class WorkerThread : public QThread
{
    Q_OBJECT

public:
    explicit WorkerThread(const QString &name, QObject *parent = nullptr)
        : QThread(parent), m_name(name), m_abort(false) {}

    void abort() { m_abort = true; }

signals:
    void progress(int value);
    void resultReady(const QString &result);

protected:
    void run() override {
        qDebug() << m_name << "开始工作，线程ID:" << QThread::currentThreadId();

        for (int i = 1; i <= 5 && !m_abort; ++i) {
            QThread::msleep(100);  // 模拟工作
            emit progress(i * 20);
        }

        emit resultReady(m_name + " 完成");
        qDebug() << m_name << "工作完成";
    }

private:
    QString m_name;
    bool m_abort;
};

// ============ 方式2: Worker + moveToThread ============
class Worker : public QObject
{
    Q_OBJECT

public:
    explicit Worker(QObject *parent = nullptr) : QObject(parent) {}

public slots:
    void doWork(const QString &task) {
        qDebug() << "Worker 执行任务:" << task << "线程:" << QThread::currentThreadId();

        for (int i = 0; i < 3; ++i) {
            QThread::msleep(100);
            emit progress(task, (i + 1) * 33);
        }

        emit finished(task + " 结果");
    }

signals:
    void progress(const QString &task, int percent);
    void finished(const QString &result);
};

// ============ 方式3: QRunnable ============
class Task : public QRunnable
{
public:
    explicit Task(int id) : m_id(id) {}

    void run() override {
        qDebug() << "Task" << m_id << "运行在线程:" << QThread::currentThreadId();
        QThread::msleep(50);
        qDebug() << "Task" << m_id << "完成";
    }

private:
    int m_id;
};

// ============ 互斥锁示例 ============
class Counter
{
public:
    void increment() {
        QMutexLocker locker(&m_mutex);  // RAII 锁
        ++m_value;
    }

    int value() const {
        QMutexLocker locker(&m_mutex);
        return m_value;
    }

private:
    mutable QMutex m_mutex;
    int m_value = 0;
};

// ============ 读写锁示例 ============
class SharedData
{
public:
    QString read() const {
        QReadLocker locker(&m_lock);  // 多读
        return m_data;
    }

    void write(const QString &data) {
        QWriteLocker locker(&m_lock);  // 独写
        m_data = data;
    }

private:
    mutable QReadWriteLock m_lock;
    QString m_data;
};

void demonstrateQThread()
{
    qDebug() << "\n=== QThread 继承方式 ===\n";
    qDebug() << "主线程 ID:" << QThread::currentThreadId();

    WorkerThread thread("Worker1");

    QObject::connect(&thread, &WorkerThread::progress,
                     [](int value) { qDebug() << "进度:" << value << "%"; });

    QObject::connect(&thread, &WorkerThread::resultReady,
                     [](const QString &result) { qDebug() << "结果:" << result; });

    thread.start();
    thread.wait();  // 等待完成
}

void demonstrateMoveToThread()
{
    qDebug() << "\n=== moveToThread 方式 (推荐) ===\n";

    QThread workerThread;
    Worker worker;
    worker.moveToThread(&workerThread);

    QObject::connect(&workerThread, &QThread::started,
                     &worker, [&worker]() { worker.doWork("任务A"); });

    QObject::connect(&worker, &Worker::progress,
                     [](const QString &task, int p) {
                         qDebug() << task << "进度:" << p << "%";
                     });

    QObject::connect(&worker, &Worker::finished,
                     [](const QString &result) { qDebug() << "完成:" << result; });

    QObject::connect(&worker, &Worker::finished,
                     &workerThread, &QThread::quit);

    workerThread.start();
    workerThread.wait();
}

void demonstrateThreadPool()
{
    qDebug() << "\n=== QThreadPool 方式 ===\n";

    QThreadPool *pool = QThreadPool::globalInstance();
    qDebug() << "最大线程数:" << pool->maxThreadCount();

    // 提交任务
    for (int i = 1; i <= 5; ++i) {
        pool->start(new Task(i));  // 自动管理内存
    }

    // 等待所有任务完成
    pool->waitForDone();
    qDebug() << "所有任务完成";
}

void demonstrateSynchronization()
{
    qDebug() << "\n=== 同步原语 ===\n";

    Counter counter;

    // 多线程增加计数
    QList<QThread*> threads;
    for (int i = 0; i < 5; ++i) {
        auto *thread = QThread::create([&counter]() {
            for (int j = 0; j < 100; ++j) {
                counter.increment();
            }
        });
        threads.append(thread);
        thread->start();
    }

    for (auto *thread : threads) {
        thread->wait();
        delete thread;
    }

    qDebug() << "计数结果 (应为500):" << counter.value();
}

int main(int argc, char *argv[])
{
    QCoreApplication app(argc, argv);

    qDebug() << "=== Qt6 多线程示例 ===";

    demonstrateQThread();
    demonstrateMoveToThread();
    demonstrateThreadPool();
    demonstrateSynchronization();

    qDebug() << "\n=== 线程最佳实践 ===";
    qDebug() << "1. 避免继承 QThread, 使用 moveToThread";
    qDebug() << "2. 使用信号槽跨线程通信";
    qDebug() << "3. 使用 QMutexLocker 自动管理锁";
    qDebug() << "4. 简单任务使用 QThreadPool";
    qDebug() << "5. 高级并发使用 QtConcurrent";

    return 0;
}

#include "main.moc"
