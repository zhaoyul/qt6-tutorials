/**
 * C++ 类暴露给 QML
 *
 * 关键宏和类型：
 * - QML_ELEMENT: 自动注册到 QML
 * - Q_PROPERTY: 暴露属性
 * - Q_INVOKABLE: 暴露方法
 * - 信号: 自动可用于 QML
 */

#ifndef COUNTER_H
#define COUNTER_H

#include <QObject>
#include <QtQml/qqmlregistration.h>

class Counter : public QObject
{
    Q_OBJECT
    QML_ELEMENT  // Qt6: 自动注册到 QML

    // 暴露属性给 QML
    Q_PROPERTY(int value READ value WRITE setValue NOTIFY valueChanged)
    Q_PROPERTY(int step READ step WRITE setStep NOTIFY stepChanged)
    Q_PROPERTY(QString displayText READ displayText NOTIFY valueChanged)

public:
    explicit Counter(QObject *parent = nullptr);

    // Getters
    int value() const;
    int step() const;
    QString displayText() const;

    // Setters
    void setValue(int value);
    void setStep(int step);

    // 暴露给 QML 的方法
    Q_INVOKABLE void increment();
    Q_INVOKABLE void decrement();
    Q_INVOKABLE void reset();
    Q_INVOKABLE QString formatValue(const QString &prefix) const;

signals:
    void valueChanged();
    void stepChanged();
    void limitReached(const QString &message);  // 可带参数的信号

private:
    int m_value;
    int m_step;
    int m_minValue;
    int m_maxValue;
};

#endif // COUNTER_H
