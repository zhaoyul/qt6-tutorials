/**
 * Qt6 GUI Test Demo
 */

#include <QtTest/QtTest>
#include <QPushButton>
#include <QWidget>

class GuiTestDemo : public QObject
{
    Q_OBJECT

private slots:
    void buttonText()
    {
        QPushButton button;
        button.setText("Hello");
        QCOMPARE(button.text(), QString("Hello"));
    }

    void showHideWidget()
    {
        QWidget widget;
        widget.show();
        QVERIFY(widget.isVisible());
        widget.hide();
        QVERIFY(!widget.isVisible());
    }
};

QTEST_MAIN(GuiTestDemo)
#include "main.moc"
