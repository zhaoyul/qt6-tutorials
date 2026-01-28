/**
 * Qt6 QML Types Demo
 *
 * Shows basic QML property types and bindings.
 */

#include <QGuiApplication>
#include <QQmlApplicationEngine>
#include <QDebug>

int main(int argc, char *argv[])
{
    QGuiApplication app(argc, argv);

    qDebug() << "=== QML Types Demo ===\n";

    QQmlApplicationEngine engine;
    engine.loadFromModule("QmlTypes", "Main");

    if (engine.rootObjects().isEmpty()) {
        qDebug() << "QML load failed";
        return -1;
    }

    return app.exec();
}
