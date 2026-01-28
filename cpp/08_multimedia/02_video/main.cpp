/**
 * Qt6 Multimedia Video Demo
 *
 * Lists available video input devices.
 */

#include <QCoreApplication>
#include <QMediaDevices>
#include <QCameraDevice>
#include <QDebug>

int main(int argc, char *argv[])
{
    QCoreApplication app(argc, argv);

    qDebug() << "=== Video Inputs ===";
    const auto cameras = QMediaDevices::videoInputs();
    if (cameras.isEmpty()) {
        qDebug() << "No video devices found.";
        return 0;
    }

    for (const QCameraDevice &camera : cameras) {
        qDebug() << " -" << camera.description();
    }

    return 0;
}
