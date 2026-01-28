/**
 * QtConcurrent::mappedReduced demo
 */

#include <QCoreApplication>
#include <QtConcurrent>
#include <QFuture>
#include <QList>
#include <QDebug>

static int square(int value)
{
    return value * value;
}

static void sumReduce(int &result, int value)
{
    result += value;
}

int main(int argc, char *argv[])
{
    QCoreApplication app(argc, argv);

    QList<int> numbers = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
    QFuture<int> future = QtConcurrent::mappedReduced(numbers, square, sumReduce);

    qDebug() << "Sum of squares:" << future.result();
    return 0;
}
