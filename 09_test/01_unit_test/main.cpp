/**
 * Qt6 单元测试示例
 *
 * Qt Test 框架特点：
 * - 轻量级，易于使用
 * - 支持数据驱动测试
 * - 支持基准测试
 * - 支持 GUI 测试
 *
 * 主要宏：
 * - QVERIFY(condition): 验证条件
 * - QCOMPARE(actual, expected): 比较值
 * - QTEST_MAIN: 生成 main 函数
 *
 * 官方文档: https://doc.qt.io/qt-6/qttest-index.html
 */

#include <QTest>
#include <QString>
#include <QList>

// 被测试的类
class Calculator
{
public:
    int add(int a, int b) { return a + b; }
    int subtract(int a, int b) { return a - b; }
    int multiply(int a, int b) { return a * b; }
    double divide(double a, double b) {
        if (b == 0) throw std::invalid_argument("Division by zero");
        return a / b;
    }

    QString formatResult(int value) {
        return QString("Result: %1").arg(value);
    }
};

// 测试类
class TestCalculator : public QObject
{
    Q_OBJECT

private:
    Calculator calc;

private slots:
    // 初始化/清理 (每个测试前后调用)
    void init()
    {
        qDebug() << "--- 测试开始 ---";
    }

    void cleanup()
    {
        qDebug() << "--- 测试结束 ---";
    }

    // 类级别初始化/清理 (所有测试前后调用一次)
    void initTestCase()
    {
        qDebug() << "=== 测试套件开始 ===";
    }

    void cleanupTestCase()
    {
        qDebug() << "=== 测试套件结束 ===";
    }

    // 基本测试
    void testAdd()
    {
        QCOMPARE(calc.add(2, 3), 5);
        QCOMPARE(calc.add(-1, 1), 0);
        QCOMPARE(calc.add(0, 0), 0);
    }

    void testSubtract()
    {
        QCOMPARE(calc.subtract(5, 3), 2);
        QCOMPARE(calc.subtract(3, 5), -2);
    }

    void testMultiply()
    {
        QCOMPARE(calc.multiply(3, 4), 12);
        QCOMPARE(calc.multiply(-2, 3), -6);
        QCOMPARE(calc.multiply(0, 100), 0);
    }

    void testDivide()
    {
        QCOMPARE(calc.divide(10, 2), 5.0);
        QCOMPARE(calc.divide(7, 2), 3.5);

        // 测试异常
        QVERIFY_THROWS_EXCEPTION(std::invalid_argument, calc.divide(1, 0));
    }

    // 数据驱动测试
    void testAdd_data()
    {
        // 定义测试数据列
        QTest::addColumn<int>("a");
        QTest::addColumn<int>("b");
        QTest::addColumn<int>("expected");

        // 添加测试数据行
        QTest::newRow("positive") << 2 << 3 << 5;
        QTest::newRow("negative") << -2 << -3 << -5;
        QTest::newRow("mixed") << -2 << 5 << 3;
        QTest::newRow("zero") << 0 << 0 << 0;
        QTest::newRow("large") << 1000000 << 2000000 << 3000000;
    }

    void testAddDataDriven()
    {
        // 获取测试数据
        QFETCH(int, a);
        QFETCH(int, b);
        QFETCH(int, expected);

        QCOMPARE(calc.add(a, b), expected);
    }

    // 字符串测试
    void testFormatResult()
    {
        QString result = calc.formatResult(42);

        // 各种验证方式
        QVERIFY(!result.isEmpty());
        QVERIFY(result.contains("42"));
        QCOMPARE(result, QString("Result: 42"));

        // 使用 QVERIFY2 提供失败消息
        QVERIFY2(result.startsWith("Result"), "Should start with 'Result'");
    }

    // 条件跳过
    void testSkipExample()
    {
        QSKIP("This test is skipped for demonstration");
        QFAIL("Should not reach here");
    }

    // 预期失败
    void testExpectedFail()
    {
        QEXPECT_FAIL("", "This is expected to fail", Continue);
        QCOMPARE(1, 2);  // 这个会失败，但不会导致测试失败

        // 测试继续执行
        QCOMPARE(1, 1);  // 这个应该通过
    }

    // 警告测试
    void testWarning()
    {
        // 验证警告消息
        QTest::ignoreMessage(QtWarningMsg, "Test warning message");
        qWarning() << "Test warning message";
    }

    // 基准测试
    void testBenchmark()
    {
        QString str;

        QBENCHMARK {
            for (int i = 0; i < 1000; ++i) {
                str = QString::number(i);
            }
        }
    }

    // 比较浮点数
    void testFloatingPoint()
    {
        double result = 0.1 + 0.2;
        // 不要用 QCOMPARE 比较浮点数精确值
        QVERIFY(qFuzzyCompare(result, 0.3));
    }
};

// 如果只有一个测试类，使用 QTEST_MAIN
// 如果有多个测试类，需要自定义 main

QTEST_MAIN(TestCalculator)
#include "main.moc"
