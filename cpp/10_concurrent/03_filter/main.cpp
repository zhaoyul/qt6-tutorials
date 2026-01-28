/**
 * QtConcurrent::filter demo
 */

#include <QCoreApplication>
#include <QtConcurrent>
#include <QFuture>
#include <QList>
#include <QDebug>

static bool isEven(int value)
{
    return value % 2 == 0;
}

int main(int argc, char *argv[])
{
    QCoreApplication app(argc, argv);

    QList<int> numbers = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
    QFuture<int> future = QtConcurrent::filtered(numbers, isEven);

    qDebug() << "Even numbers:" << future.results();
    return 0;
}
