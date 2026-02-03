/**
 * Qt6 QML JavaScript 集成示例
 *
 * 展示 QML 中 JavaScript 的使用：
 * - 内联 JavaScript 函数
 * - 导入外部 JS 文件
 * - 信号处理
 * - 属性绑定中的 JS
 *
 * 官方文档: https://doc.qt.io/qt-6/qtqml-javascript-topic.html
 */

#include <QGuiApplication>
#include <QQmlApplicationEngine>
#include <QDebug>

int main(int argc, char *argv[])
{
    QGuiApplication app(argc, argv);

    qDebug() << "=== Qt6 QML JavaScript 集成示例 ===\n";

    QQmlApplicationEngine engine;

    // 加载 QML
    engine.loadFromModule("QmlJavaScript", "Main");

    if (engine.rootObjects().isEmpty()) {
        qDebug() << "QML 加载失败";
        return -1;
    }

    qDebug() << "QML 已加载，窗口应该已显示";

    return app.exec();
}
