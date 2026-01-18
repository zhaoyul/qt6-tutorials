/**
 * Qt6 QML 基础示例
 *
 * QML 是 Qt 的声明式 UI 语言：
 * - 类似 JSON 的语法
 * - 与 JavaScript 无缝集成
 * - 属性绑定
 * - 状态和转换
 *
 * 官方文档: https://doc.qt.io/qt-6/qmlapplications.html
 */

#include <QGuiApplication>
#include <QQmlApplicationEngine>
#include <QDebug>

int main(int argc, char *argv[])
{
    QGuiApplication app(argc, argv);

    qDebug() << "=== Qt6 QML 基础示例 ===\n";

    QQmlApplicationEngine engine;

    // 加载 QML
    engine.loadFromModule("QmlBasics", "Main");

    if (engine.rootObjects().isEmpty()) {
        qDebug() << "QML 加载失败";
        return -1;
    }

    qDebug() << "QML 已加载，窗口应该已显示";

    return app.exec();
}
