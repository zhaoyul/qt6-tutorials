/**
 * Qt6 Multimedia Camera Demo
 *
 * Shows basic camera device information.
 */

#include <QCoreApplication>
#include <QMediaDevices>
#include <QCameraDevice>
#include <QDebug>

static const char *positionToString(QCameraDevice::Position pos)
{
    switch (pos) {
    case QCameraDevice::FrontFace:
        return "Front";
    case QCameraDevice::BackFace:
        return "Back";
    default:
        return "Unspecified";
    }
}

int main(int argc, char *argv[])
{
    QCoreApplication app(argc, argv);

    const auto cameras = QMediaDevices::videoInputs();
    if (cameras.isEmpty()) {
        qDebug() << "No camera devices found.";
        return 0;
    }

    const QCameraDevice camera = cameras.first();
    qDebug() << "Default camera:" << camera.description();
    qDebug() << "Position:" << positionToString(camera.position());
    qDebug() << "Supports photo resolutions:" << camera.photoResolutions().size();
    qDebug() << "Supports video formats:" << camera.videoFormats().size();

    return 0;
}
