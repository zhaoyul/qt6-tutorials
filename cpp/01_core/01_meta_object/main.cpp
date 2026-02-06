/**
 * Qt6 元对象系统 (Meta-Object System) 示例
 *
 * 元对象系统是Qt的核心特性，提供了：
 * 1. 运行时类型信息 (RTTI)
 * 2. 信号与槽机制
 * 3. 属性系统
 *
 * 关键点：
 * - 继承 QObject
 * - 使用 Q_OBJECT 宏
 * - 通过 MOC (Meta-Object Compiler) 处理
 *
 * 官方文档: https://doc.qt.io/qt-6/metaobjects.html
 */

#include <QCoreApplication>
#include <QObject>
#include <QMetaObject>
#include <QMetaProperty>
#include <QMetaMethod>
#include <QDebug>

// 自定义类，展示元对象系统
class Person : public QObject
{
    Q_OBJECT  // 必须：启用元对象特性

    // 声明属性
    Q_PROPERTY(QString name READ name WRITE setName NOTIFY nameChanged)
    Q_PROPERTY(int age      READ age  WRITE setAge  NOTIFY ageChanged)

    // 类信息
    Q_CLASSINFO("author", "Qt学习项目")
    Q_CLASSINFO("version", "1.0")

public:
    explicit Person(QObject *parent = nullptr)
        : QObject(parent), m_name("Unknown"), m_age(0) {}

    // Getter
    QString name() const { return m_name; }
    int age() const { return m_age; }

    // Setter
    void setName(const QString &name) {
        if (m_name != name) {
            m_name = name;
            emit nameChanged(m_name);
        }
    }

    void setAge(int age) {
        if (m_age != age) {
            m_age = age;
            emit ageChanged(m_age);
        }
    }

    // 可调用方法 (可通过元对象系统调用)
    Q_INVOKABLE void introduce() const {
        qDebug() << "我是" << m_name << ", 今年" << m_age << "岁";
    }

signals:
    void nameChanged(const QString &name);
    void ageChanged(int age);

public slots:
    void onBirthday() {
        setAge(m_age + 1);
        qDebug() << m_name << "过生日了! 现在" << m_age << "岁";
    }

private:
    QString m_name;
    int m_age;
};

void exploreMetaObject(QObject *obj)
{
    const QMetaObject *meta = obj->metaObject();

    qDebug() << "\n========== 元对象信息 ==========";
    qDebug() << "类名:" << meta->className();
    qDebug() << "父类:" << (meta->superClass() ? meta->superClass()->className() : "无");

    // 类信息
    qDebug() << "\n--- 类信息 (Q_CLASSINFO) ---";
    for (int i = meta->classInfoOffset(); i < meta->classInfoCount(); ++i) {
        QMetaClassInfo info = meta->classInfo(i);
        qDebug() << " " << info.name() << ":" << info.value();
    }

    // 属性
    qDebug() << "\n--- 属性 (Q_PROPERTY) ---";
    for (int i = meta->propertyOffset(); i < meta->propertyCount(); ++i) {
        QMetaProperty prop = meta->property(i);
        qDebug() << "  属性:" << prop.name()
                 << "类型:" << prop.typeName()
                 << "可读:" << prop.isReadable()
                 << "可写:" << prop.isWritable();
    }

    // 方法
    qDebug() << "\n--- 方法 ---";
    for (int i = meta->methodOffset(); i < meta->methodCount(); ++i) {
        QMetaMethod method = meta->method(i);
        QString methodType;
        switch (method.methodType()) {
            case QMetaMethod::Signal: methodType = "信号"; break;
            case QMetaMethod::Slot: methodType = "槽"; break;
            case QMetaMethod::Method: methodType = "方法"; break;
            default: methodType = "未知";
        }
        qDebug() << " " << methodType << ":" << method.methodSignature();
    }
}

int main(int argc, char *argv[])
{
    QCoreApplication app(argc, argv);

    qDebug() << "=== Qt6 元对象系统示例 ===\n";

    // 创建对象
    Person person;
    person.setName("张三");
    person.setAge(25);

    // 探索元对象
    exploreMetaObject(&person);

    // 通过元对象系统调用方法
    qDebug() << "\n--- 通过 Q_INVOKABLE 调用方法 ---";
    QMetaObject::invokeMethod(&person, "introduce");

    // 通过属性系统设置值
    qDebug() << "\n--- 通过属性系统设置值 ---";
    person.setProperty("name", "李四");
    person.setProperty("age", 30);

    qDebug() << "读取属性 name:" << person.property("name").toString();
    qDebug() << "读取属性 age:" << person.property("age").toInt();

    // 动态属性 (不需要预先声明)
    qDebug() << "\n--- 动态属性 ---";
    person.setProperty("hobby", "编程");  // 动态添加
    qDebug() << "动态属性 hobby:" << person.property("hobby").toString();

    // 对象继承检查
    qDebug() << "\n--- 类型检查 ---";
    qDebug() << "person 是 Person 类型:" << person.inherits("Person");
    qDebug() << "person 是 QObject 类型:" << person.inherits("QObject");
    qDebug() << "person 是 QWidget 类型:" << person.inherits("QWidget");

    return 0;
}

#include "main.moc"  // 因为 Q_OBJECT 在 cpp 文件中
