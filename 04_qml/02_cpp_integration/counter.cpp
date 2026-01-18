#include "counter.h"
#include <QDebug>

Counter::Counter(QObject *parent)
    : QObject(parent)
    , m_value(0)
    , m_step(1)
    , m_minValue(0)
    , m_maxValue(100)
{
}

int Counter::value() const
{
    return m_value;
}

int Counter::step() const
{
    return m_step;
}

QString Counter::displayText() const
{
    return QString("当前值: %1").arg(m_value);
}

void Counter::setValue(int value)
{
    if (m_value != value) {
        m_value = qBound(m_minValue, value, m_maxValue);
        emit valueChanged();

        // 检查边界
        if (m_value == m_maxValue) {
            emit limitReached("已达到最大值!");
        } else if (m_value == m_minValue) {
            emit limitReached("已达到最小值!");
        }
    }
}

void Counter::setStep(int step)
{
    if (m_step != step) {
        m_step = step;
        emit stepChanged();
    }
}

void Counter::increment()
{
    qDebug() << "[C++] increment() 被调用";
    setValue(m_value + m_step);
}

void Counter::decrement()
{
    qDebug() << "[C++] decrement() 被调用";
    setValue(m_value - m_step);
}

void Counter::reset()
{
    qDebug() << "[C++] reset() 被调用";
    setValue(0);
}

QString Counter::formatValue(const QString &prefix) const
{
    return QString("%1: %2").arg(prefix).arg(m_value);
}
