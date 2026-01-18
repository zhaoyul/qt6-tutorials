/**
 * Qt6 QML 与 C++ 集成示例
 *
 * 集成方式：
 * 1. QML_ELEMENT 宏自动注册
 * 2. qmlRegisterType 手动注册
 * 3. Context Property 上下文属性
 * 4. QQmlEngine::setObjectOwnership 控制所有权
 */

#include <QGuiApplication>
#include <QQmlApplicationEngine>
#include <QQmlContext>
#include "counter.h"
#include <QDebug>

int main(int argc, char *argv[])
{
    QGuiApplication app(argc, argv);

    qDebug() << "=== Qt6 QML 与 C++ 集成示例 ===\n";

    QQmlApplicationEngine engine;

    // 方式1: QML_ELEMENT 自动注册 (在 counter.h 中)
    // Counter 类型自动可用

    // 方式2: 通过上下文暴露对象实例
    Counter *globalCounter = new Counter(&engine);
    globalCounter->setValue(50);
    engine.rootContext()->setContextProperty("globalCounter", globalCounter);

    // 方式3: 暴露简单值
    engine.rootContext()->setContextProperty("appVersion", "1.0.0");
    engine.rootContext()->setContextProperty("debugMode", true);

    // 加载 QML
    engine.loadFromModule("QmlCppIntegration", "Main");

    if (engine.rootObjects().isEmpty()) {
        qDebug() << "QML 加载失败";
        return -1;
    }

    return app.exec();
}
