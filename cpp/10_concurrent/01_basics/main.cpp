/**
 * Qt6 Concurrent 并发编程示例
 *
 * QtConcurrent 提供高级并发 API：
 * - QtConcurrent::run: 在线程池运行函数
 * - QtConcurrent::map: 并行 map
 * - QtConcurrent::filter: 并行过滤
 * - QtConcurrent::mappedReduced: Map-Reduce
 *
 * QFuture 用于获取异步结果：
 * - result(): 等待并获取结果
 * - waitForFinished(): 等待完成
 * - isFinished(): 检查是否完成
 *
 * 官方文档: https://doc.qt.io/qt-6/qtconcurrent-index.html
 */

#include <QCoreApplication>
#include <QtConcurrent>
#include <QFuture>
#include <QFutureWatcher>
#include <QPromise>
#include <QThread>
#include <QDebug>
#include <cmath>

// 普通函数
QString heavyComputation(int id)
{
    qDebug() << "任务" << id << "开始，线程:" << QThread::currentThreadId();
    QThread::msleep(500);  // 模拟耗时操作
    qDebug() << "任务" << id << "完成";
    return QString("结果-%1").arg(id);
}

// 用于 map 的函数
int square(int n)
{
    QThread::msleep(50);
    return n * n;
}

// 用于 filter 的谓词
bool isEven(int n)
{
    return n % 2 == 0;
}

// 用于 reduce 的函数
void sumReduce(int &result, int value)
{
    result += value;
}

void demonstrateRun()
{
    qDebug() << "\n=== QtConcurrent::run ===\n";
    qDebug() << "主线程:" << QThread::currentThreadId();

    // 方式1: 运行普通函数
    QFuture<QString> future1 = QtConcurrent::run(heavyComputation, 1);

    // 方式2: 运行 Lambda
    QFuture<int> future2 = QtConcurrent::run([]() {
        qDebug() << "Lambda 运行在线程:" << QThread::currentThreadId();
        QThread::msleep(300);
        return 42;
    });

    // 方式3: 无返回值
    QFuture<void> future3 = QtConcurrent::run([]() {
        qDebug() << "无返回值任务运行在线程:" << QThread::currentThreadId();
    });

    // 等待结果
    qDebug() << "等待结果...";
    QString result1 = future1.result();
    int result2 = future2.result();
    future3.waitForFinished();

    qDebug() << "Future1 结果:" << result1;
    qDebug() << "Future2 结果:" << result2;
}

void demonstrateMap()
{
    qDebug() << "\n=== QtConcurrent::map ===\n";

    QList<int> numbers = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
    qDebug() << "原始数据:" << numbers;

    // 原地修改 (map)
    QFuture<void> mapFuture = QtConcurrent::map(numbers, [](int &n) {
        n = n * n;
    });
    mapFuture.waitForFinished();
    qDebug() << "原地平方后:" << numbers;

    // 返回新列表 (mapped)
    numbers = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
    QFuture<int> mappedFuture = QtConcurrent::mapped(numbers, square);
    QList<int> squared = mappedFuture.results();
    qDebug() << "mapped 结果:" << squared;
}

void demonstrateFilter()
{
    qDebug() << "\n=== QtConcurrent::filter ===\n";

    QList<int> numbers = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
    qDebug() << "原始数据:" << numbers;

    // 原地过滤
    QList<int> toFilter = numbers;
    QFuture<void> filterFuture = QtConcurrent::filter(toFilter, isEven);
    filterFuture.waitForFinished();
    qDebug() << "过滤偶数 (原地):" << toFilter;

    // 返回新列表
    QFuture<int> filteredFuture = QtConcurrent::filtered(numbers, isEven);
    QList<int> evens = filteredFuture.results();
    qDebug() << "filtered 结果:" << evens;
}

void demonstrateMapReduce()
{
    qDebug() << "\n=== QtConcurrent::mappedReduced ===\n";

    QList<int> numbers = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
    qDebug() << "原始数据:" << numbers;

    // 计算平方和
    QFuture<int> future = QtConcurrent::mappedReduced(
        numbers,
        square,      // map 函数
        sumReduce    // reduce 函数
    );

    int sumOfSquares = future.result();
    qDebug() << "平方和:" << sumOfSquares;
    qDebug() << "(1² + 2² + ... + 10² = 385)";

    // 使用 Lambda
    QFuture<int> future2 = QtConcurrent::mappedReduced(
        numbers,
        [](int n) { return n * n; },
        [](int &result, int value) { result += value; }
    );
    qDebug() << "Lambda 版本结果:" << future2.result();
}

void demonstrateFutureWatcher()
{
    qDebug() << "\n=== QFutureWatcher (异步通知) ===\n";

    QEventLoop loop;

    QFuture<QString> future = QtConcurrent::run([]() {
        QThread::msleep(300);
        return QString("异步完成");
    });

    QFutureWatcher<QString> watcher;

    QObject::connect(&watcher, &QFutureWatcher<QString>::finished, [&]() {
        qDebug() << "Watcher 通知: 任务完成";
        qDebug() << "结果:" << watcher.result();
        loop.quit();
    });

    QObject::connect(&watcher, &QFutureWatcher<QString>::progressValueChanged, [](int value) {
        qDebug() << "进度:" << value;
    });

    watcher.setFuture(future);
    qDebug() << "等待 Watcher 通知...";

    loop.exec();
}

void demonstratePromise()
{
    qDebug() << "\n=== QPromise (手动控制 Future) ===\n";

    // QPromise 允许手动控制 Future 的结果
    auto runWithPromise = []() {
        QPromise<int> promise;
        QFuture<int> future = promise.future();

        // 在另一个线程中设置结果
        QtConcurrent::run([promise = std::move(promise)]() mutable {
            promise.start();

            for (int i = 0; i <= 100; i += 20) {
                QThread::msleep(100);
                promise.setProgressValue(i);
            }

            promise.addResult(42);
            promise.finish();
        });

        return future;
    };

    QFuture<int> future = runWithPromise();

    // 等待并获取结果
    future.waitForFinished();
    qDebug() << "Promise 结果:" << future.result();
}

void demonstrateThreadPool()
{
    qDebug() << "\n=== QThreadPool 信息 ===\n";

    QThreadPool *pool = QThreadPool::globalInstance();
    qDebug() << "最大线程数:" << pool->maxThreadCount();
    qDebug() << "活跃线程数:" << pool->activeThreadCount();
    qDebug() << "过期时间:" << pool->expiryTimeout() << "ms";

    // 可以调整线程池大小
    // pool->setMaxThreadCount(8);
}

int main(int argc, char *argv[])
{
    QCoreApplication app(argc, argv);

    qDebug() << "=== Qt6 Concurrent 并发编程示例 ===";

    demonstrateThreadPool();
    demonstrateRun();
    demonstrateMap();
    demonstrateFilter();
    demonstrateMapReduce();
    demonstrateFutureWatcher();
    demonstratePromise();

    qDebug() << "\n=== 要点总结 ===";
    qDebug() << "1. QtConcurrent::run() 运行任意函数";
    qDebug() << "2. map/filter/reduce 实现并行数据处理";
    qDebug() << "3. QFuture 获取异步结果";
    qDebug() << "4. QFutureWatcher 提供信号槽通知";
    qDebug() << "5. QPromise 手动控制 Future";

    return 0;
}
