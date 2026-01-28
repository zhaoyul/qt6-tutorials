/**
 * Qt6 Multimedia Audio Demo
 *
 * Lists available audio input and output devices.
 */

#include <QCoreApplication>
#include <QMediaDevices>
#include <QAudioDevice>
#include <QDebug>

int main(int argc, char *argv[])
{
    QCoreApplication app(argc, argv);

    qDebug() << "=== Audio Outputs ===";
    const auto outputs = QMediaDevices::audioOutputs();
    for (const QAudioDevice &device : outputs) {
        qDebug() << " -" << device.description();
    }

    qDebug() << "\n=== Audio Inputs ===";
    const auto inputs = QMediaDevices::audioInputs();
    for (const QAudioDevice &device : inputs) {
        qDebug() << " -" << device.description();
    }

    return 0;
}
