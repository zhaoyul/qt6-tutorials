/**
 * QtConcurrent::run demo
 */

#include <QCoreApplication>
#include <QtConcurrent>
#include <QFuture>
#include <QThread>
#include <QDebug>

static int heavyComputation(int value)
{
    QThread::msleep(200);
    return value * 2;
}

int main(int argc, char *argv[])
{
    QCoreApplication app(argc, argv);

    qDebug() << "Running task...";
    QFuture<int> future = QtConcurrent::run(heavyComputation, 21);
    qDebug() << "Result:" << future.result();

    return 0;
}
