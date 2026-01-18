/**
 * Qt6 属性系统示例
 *
 * 属性系统允许在运行时查询和修改对象属性：
 * - Q_PROPERTY 宏声明属性
 * - 支持绑定、通知、设计器集成
 * - Qt6 引入了属性绑定系统
 *
 * Q_PROPERTY 语法:
 * Q_PROPERTY(type name
 *     READ getter
 *     [WRITE setter]
 *     [NOTIFY signal]
 *     [BINDABLE bindable]
 *     [RESET reset]
 *     [DESIGNABLE bool]
 *     [STORED bool]
 *     [CONSTANT]
 *     [FINAL])
 *
 * 官方文档: https://doc.qt.io/qt-6/properties.html
 */

#include <QCoreApplication>
#include <QObject>
#include <QProperty>
#include <QDebug>
#include <QVariant>
#include <QMetaProperty>

class Rectangle : public QObject
{
    Q_OBJECT

    // 基础属性
    Q_PROPERTY(qreal width READ width WRITE setWidth NOTIFY widthChanged)
    Q_PROPERTY(qreal height READ height WRITE setHeight NOTIFY heightChanged)

    // 只读计算属性
    Q_PROPERTY(qreal area READ area NOTIFY areaChanged)
    Q_PROPERTY(qreal perimeter READ perimeter NOTIFY perimeterChanged)

    // 常量属性
    Q_PROPERTY(QString type READ type CONSTANT)

public:
    explicit Rectangle(QObject *parent = nullptr)
        : QObject(parent), m_width(0), m_height(0) {}

    // Width
    qreal width() const { return m_width; }
    void setWidth(qreal w) {
        if (!qFuzzyCompare(m_width, w)) {
            m_width = w;
            emit widthChanged();
            emit areaChanged();
            emit perimeterChanged();
        }
    }

    // Height
    qreal height() const { return m_height; }
    void setHeight(qreal h) {
        if (!qFuzzyCompare(m_height, h)) {
            m_height = h;
            emit heightChanged();
            emit areaChanged();
            emit perimeterChanged();
        }
    }

    // 计算属性
    qreal area() const { return m_width * m_height; }
    qreal perimeter() const { return 2 * (m_width + m_height); }

    // 常量属性
    QString type() const { return "Rectangle"; }

signals:
    void widthChanged();
    void heightChanged();
    void areaChanged();
    void perimeterChanged();

private:
    qreal m_width;
    qreal m_height;
};

// Qt6 QProperty 绑定示例
class BindableRectangle : public QObject
{
    Q_OBJECT

    // Qt6 可绑定属性
    Q_PROPERTY(qreal width READ width WRITE setWidth BINDABLE bindableWidth)
    Q_PROPERTY(qreal height READ height WRITE setHeight BINDABLE bindableHeight)
    Q_PROPERTY(qreal area READ area BINDABLE bindableArea)

public:
    explicit BindableRectangle(QObject *parent = nullptr)
        : QObject(parent)
    {
        // 设置 area 的绑定表达式
        m_area.setBinding([this]() {
            return m_width.value() * m_height.value();
        });
    }

    qreal width() const { return m_width.value(); }
    void setWidth(qreal w) { m_width.setValue(w); }
    QBindable<qreal> bindableWidth() { return &m_width; }

    qreal height() const { return m_height.value(); }
    void setHeight(qreal h) { m_height.setValue(h); }
    QBindable<qreal> bindableHeight() { return &m_height; }

    qreal area() const { return m_area.value(); }
    QBindable<qreal> bindableArea() { return &m_area; }

private:
    Q_OBJECT_BINDABLE_PROPERTY(BindableRectangle, qreal, m_width)
    Q_OBJECT_BINDABLE_PROPERTY(BindableRectangle, qreal, m_height)
    Q_OBJECT_BINDABLE_PROPERTY(BindableRectangle, qreal, m_area)
};

void demonstrateQVariant()
{
    qDebug() << "\n=== QVariant 示例 ===";

    // QVariant 可以存储任意类型
    QVariant v1 = 42;
    QVariant v2 = "Hello";
    QVariant v3 = 3.14;
    QVariant v4 = QStringList{"a", "b", "c"};

    qDebug() << "v1 (int):" << v1.toInt() << "类型:" << v1.typeName();
    qDebug() << "v2 (string):" << v2.toString() << "类型:" << v2.typeName();
    qDebug() << "v3 (double):" << v3.toDouble() << "类型:" << v3.typeName();
    qDebug() << "v4 (list):" << v4.toStringList() << "类型:" << v4.typeName();

    // 类型检查
    qDebug() << "\n类型检查:";
    qDebug() << "v1 可转为 int:" << v1.canConvert<int>();
    qDebug() << "v2 可转为 int:" << v2.canConvert<int>();

    // 类型转换
    QVariant numStr = "123";
    qDebug() << "\n\"123\" 转 int:" << numStr.toInt();
}

int main(int argc, char *argv[])
{
    QCoreApplication app(argc, argv);

    qDebug() << "=== Qt6 属性系统示例 ===\n";

    // ============ 基础属性 ============
    qDebug() << "--- 基础属性演示 ---";
    Rectangle rect;

    // 连接信号
    QObject::connect(&rect, &Rectangle::areaChanged, [&rect]() {
        qDebug() << "面积变化:" << rect.area();
    });

    // 使用 setter
    rect.setWidth(10);
    rect.setHeight(5);

    qDebug() << "宽度:" << rect.width();
    qDebug() << "高度:" << rect.height();
    qDebug() << "面积:" << rect.area();
    qDebug() << "周长:" << rect.perimeter();
    qDebug() << "类型:" << rect.type();

    // ============ 通过属性系统访问 ============
    qDebug() << "\n--- 通过 setProperty/property 访问 ---";
    rect.setProperty("width", 20);
    rect.setProperty("height", 10);

    qDebug() << "width 属性:" << rect.property("width").toDouble();
    qDebug() << "height 属性:" << rect.property("height").toDouble();
    qDebug() << "area 属性:" << rect.property("area").toDouble();

    // ============ Qt6 可绑定属性 ============
    qDebug() << "\n--- Qt6 可绑定属性演示 ---";
    BindableRectangle brect;

    // 属性改变时自动通知
    brect.bindableArea().subscribe([&brect]() {
        qDebug() << "绑定属性 - 面积自动更新为:" << brect.area();
    });

    brect.setWidth(5);
    brect.setHeight(4);

    qDebug() << "绑定矩形面积:" << brect.area();

    // 修改宽度, area 自动更新
    brect.setWidth(10);

    // ============ QVariant ============
    demonstrateQVariant();

    // ============ 列出所有属性 ============
    qDebug() << "\n--- 枚举所有属性 ---";
    const QMetaObject *meta = rect.metaObject();
    for (int i = 0; i < meta->propertyCount(); ++i) {
        QMetaProperty prop = meta->property(i);
        qDebug() << prop.name() << "=" << rect.property(prop.name());
    }

    return 0;
}

#include "main.moc"
