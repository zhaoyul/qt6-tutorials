/**
 * Qt6 容器类示例
 *
 * Qt 提供了一套模板容器类，特点：
 * - 隐式共享 (Copy-on-Write)
 * - 跨平台一致性
 * - 与 STL 兼容
 *
 * 主要容器:
 * - QList (Qt6 中 QVector 是 QList 的别名)
 * - QMap / QMultiMap (红黑树)
 * - QHash / QMultiHash (哈希表)
 * - QSet (基于 QHash)
 * - QString (Unicode 字符串)
 * - QByteArray (字节数组)
 *
 * 官方文档: https://doc.qt.io/qt-6/containers.html
 */

#include <QCoreApplication>
#include <QString>
#include <QStringList>
#include <QList>
#include <QMap>
#include <QHash>
#include <QSet>
#include <QByteArray>
#include <QDebug>

void demonstrateQString()
{
    qDebug() << "=== QString 示例 ===\n";

    // 创建
    QString s1 = "Hello";
    QString s2 = QString("World");
    QString s3 = QString::fromUtf8("中文支持");

    // 拼接
    QString combined = s1 + " " + s2;
    qDebug() << "拼接:" << combined;

    // 格式化
    QString formatted = QString("Name: %1, Age: %2").arg("Alice").arg(25);
    qDebug() << "格式化:" << formatted;

    // 查找替换
    QString text = "Hello World World";
    qDebug() << "包含 World:" << text.contains("World");
    qDebug() << "World 位置:" << text.indexOf("World");
    qDebug() << "替换后:" << text.replace("World", "Qt");

    // 分割
    QString csv = "apple,banana,cherry";
    QStringList fruits = csv.split(",");
    qDebug() << "分割:" << fruits;

    // 连接
    qDebug() << "连接:" << fruits.join(" | ");

    // 大小写
    qDebug() << "大写:" << QString("hello").toUpper();
    qDebug() << "小写:" << QString("HELLO").toLower();

    // 裁剪空白
    qDebug() << "裁剪:" << QString("  hello  ").trimmed();

    // 数值转换
    qDebug() << "字符串转数字:" << QString("123").toInt();
    qDebug() << "数字转字符串:" << QString::number(3.14159, 'f', 2);

    // 中文
    qDebug() << "中文字符串:" << s3;
    qDebug() << "中文长度:" << s3.length();
}

void demonstrateQList()
{
    qDebug() << "\n=== QList 示例 ===\n";

    // 创建
    QList<int> list1 = {1, 2, 3, 4, 5};
    QList<QString> list2 = {"Apple", "Banana", "Cherry"};

    // 添加元素
    list1.append(6);
    list1.prepend(0);
    list1 << 7 << 8;  // 流式添加

    qDebug() << "list1:" << list1;

    // 访问
    qDebug() << "第一个:" << list1.first();
    qDebug() << "最后一个:" << list1.last();
    qDebug() << "索引 3:" << list1.at(3);
    qDebug() << "索引 3 (operator[]):" << list1[3];

    // 查找
    qDebug() << "包含 5:" << list1.contains(5);
    qDebug() << "5 的索引:" << list1.indexOf(5);
    qDebug() << "计数 3:" << list1.count(3);

    // 修改
    list1[0] = 100;
    list1.replace(1, 200);

    // 删除
    list1.removeFirst();
    list1.removeLast();
    list1.removeAt(0);
    list1.removeOne(5);  // 删除第一个匹配项

    qDebug() << "修改后:" << list1;

    // 遍历 - Java 风格
    qDebug() << "遍历 (range-for):";
    for (const int &value : list1) {
        qDebug() << "  " << value;
    }

    // 遍历 - STL 风格
    qDebug() << "遍历 (iterator):";
    for (auto it = list1.begin(); it != list1.end(); ++it) {
        qDebug() << "  " << *it;
    }

    // 排序
    QList<int> unsorted = {3, 1, 4, 1, 5, 9, 2, 6};
    std::sort(unsorted.begin(), unsorted.end());
    qDebug() << "排序后:" << unsorted;
}

void demonstrateQMap()
{
    qDebug() << "\n=== QMap 示例 (有序) ===\n";

    QMap<QString, int> scores;

    // 插入
    scores.insert("Alice", 95);
    scores.insert("Bob", 87);
    scores["Charlie"] = 92;
    scores["David"] = 88;

    qDebug() << "scores:" << scores;

    // 访问
    qDebug() << "Alice 分数:" << scores.value("Alice");
    qDebug() << "不存在的键:" << scores.value("Unknown", -1);  // 默认值

    // 检查
    qDebug() << "包含 Bob:" << scores.contains("Bob");
    qDebug() << "大小:" << scores.size();

    // 键值列表
    qDebug() << "所有键:" << scores.keys();
    qDebug() << "所有值:" << scores.values();

    // 遍历
    qDebug() << "遍历:";
    for (auto it = scores.begin(); it != scores.end(); ++it) {
        qDebug() << "  " << it.key() << ":" << it.value();
    }

    // 删除
    scores.remove("David");
    qDebug() << "删除后:" << scores;
}

void demonstrateQHash()
{
    qDebug() << "\n=== QHash 示例 (无序,更快) ===\n";

    QHash<QString, QString> capitals;

    capitals["China"] = "Beijing";
    capitals["Japan"] = "Tokyo";
    capitals["France"] = "Paris";
    capitals["Germany"] = "Berlin";

    qDebug() << "capitals:" << capitals;
    qDebug() << "China 首都:" << capitals.value("China");

    // QHash vs QMap:
    // - QHash: O(1) 查找，无序
    // - QMap: O(log n) 查找，有序
}

void demonstrateQSet()
{
    qDebug() << "\n=== QSet 示例 ===\n";

    QSet<int> set1 = {1, 2, 3, 4, 5};
    QSet<int> set2 = {4, 5, 6, 7, 8};

    qDebug() << "set1:" << set1;
    qDebug() << "set2:" << set2;

    // 集合操作
    qDebug() << "并集:" << (set1 | set2);
    qDebug() << "交集:" << (set1 & set2);
    qDebug() << "差集 (set1 - set2):" << (set1 - set2);

    // 添加/删除
    set1.insert(10);
    set1.remove(1);
    qDebug() << "修改后 set1:" << set1;

    // 检查
    qDebug() << "包含 3:" << set1.contains(3);
}

void demonstrateQByteArray()
{
    qDebug() << "\n=== QByteArray 示例 ===\n";

    QByteArray data = "Hello, Binary World!";

    qDebug() << "数据:" << data;
    qDebug() << "大小:" << data.size();

    // 十六进制
    qDebug() << "十六进制:" << data.toHex();

    // Base64
    QByteArray encoded = data.toBase64();
    qDebug() << "Base64 编码:" << encoded;
    qDebug() << "Base64 解码:" << QByteArray::fromBase64(encoded);

    // 数值
    QByteArray num = QByteArray::number(12345);
    qDebug() << "数值转字节:" << num;
    qDebug() << "字节转数值:" << num.toInt();
}

int main(int argc, char *argv[])
{
    QCoreApplication app(argc, argv);

    qDebug() << "=== Qt6 容器类示例 ===";

    demonstrateQString();
    demonstrateQList();
    demonstrateQMap();
    demonstrateQHash();
    demonstrateQSet();
    demonstrateQByteArray();

    qDebug() << "\n=== 隐式共享示例 ===";
    QList<int> original = {1, 2, 3};
    QList<int> copy = original;  // 浅拷贝，共享数据
    qDebug() << "拷贝前共享数据 (相同地址)";
    copy[0] = 100;  // 此时才真正复制 (Copy-on-Write)
    qDebug() << "original:" << original;
    qDebug() << "copy:" << copy;

    return 0;
}
