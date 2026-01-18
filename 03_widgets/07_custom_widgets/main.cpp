/**
 * Qt6 自定义控件示例
 *
 * 自定义控件的方式：
 * 1. 组合现有控件
 * 2. 继承 QWidget 并重写 paintEvent
 * 3. 继承现有控件并修改行为
 *
 * 关键重写方法：
 * - paintEvent(): 绘制
 * - sizeHint(): 建议大小
 * - minimumSizeHint(): 最小大小
 * - mousePressEvent() 等: 事件处理
 *
 * 官方文档: https://doc.qt.io/qt-6/widget-classes.html
 */

#include <QApplication>
#include <QWidget>
#include <QVBoxLayout>
#include <QHBoxLayout>
#include <QPainter>
#include <QPainterPath>
#include <QMouseEvent>
#include <QPropertyAnimation>
#include <QLabel>
#include <QSlider>
#include <QTimer>
#include <QDebug>
#include <cmath>

// 自定义圆形进度条
class CircularProgress : public QWidget
{
    Q_OBJECT
    Q_PROPERTY(int value READ value WRITE setValue NOTIFY valueChanged)

public:
    explicit CircularProgress(QWidget *parent = nullptr)
        : QWidget(parent), m_value(0), m_maximum(100)
    {
        setMinimumSize(100, 100);
    }

    int value() const { return m_value; }
    int maximum() const { return m_maximum; }

    QSize sizeHint() const override { return QSize(120, 120); }

public slots:
    void setValue(int value)
    {
        if (m_value != value) {
            m_value = qBound(0, value, m_maximum);
            emit valueChanged(m_value);
            update();
        }
    }

    void setMaximum(int maximum)
    {
        m_maximum = maximum;
        update();
    }

signals:
    void valueChanged(int value);

protected:
    void paintEvent(QPaintEvent *event) override
    {
        Q_UNUSED(event);

        QPainter painter(this);
        painter.setRenderHint(QPainter::Antialiasing);

        int side = qMin(width(), height());
        QRectF rect((width() - side) / 2.0 + 10,
                    (height() - side) / 2.0 + 10,
                    side - 20, side - 20);

        // 背景圆
        painter.setPen(QPen(QColor(200, 200, 200), 8));
        painter.drawArc(rect, 0, 360 * 16);

        // 进度弧
        int spanAngle = -360 * 16 * m_value / m_maximum;
        painter.setPen(QPen(QColor(0, 150, 255), 8, Qt::SolidLine, Qt::RoundCap));
        painter.drawArc(rect, 90 * 16, spanAngle);

        // 中心文字
        painter.setPen(Qt::black);
        painter.setFont(QFont("Arial", side / 5, QFont::Bold));
        painter.drawText(rect, Qt::AlignCenter,
                        QString("%1%").arg(m_value * 100 / m_maximum));
    }

private:
    int m_value;
    int m_maximum;
};

// 自定义开关按钮
class ToggleSwitch : public QWidget
{
    Q_OBJECT
    Q_PROPERTY(bool checked READ isChecked WRITE setChecked NOTIFY toggled)
    Q_PROPERTY(qreal handlePosition READ handlePosition WRITE setHandlePosition)

public:
    explicit ToggleSwitch(QWidget *parent = nullptr)
        : QWidget(parent), m_checked(false), m_handlePosition(0)
    {
        setFixedSize(60, 30);
        setCursor(Qt::PointingHandCursor);

        m_animation = new QPropertyAnimation(this, "handlePosition", this);
        m_animation->setDuration(150);
    }

    bool isChecked() const { return m_checked; }
    qreal handlePosition() const { return m_handlePosition; }

    QSize sizeHint() const override { return QSize(60, 30); }

public slots:
    void setChecked(bool checked)
    {
        if (m_checked != checked) {
            m_checked = checked;
            m_animation->setStartValue(m_handlePosition);
            m_animation->setEndValue(checked ? 1.0 : 0.0);
            m_animation->start();
            emit toggled(m_checked);
        }
    }

    void setHandlePosition(qreal position)
    {
        m_handlePosition = position;
        update();
    }

signals:
    void toggled(bool checked);

protected:
    void paintEvent(QPaintEvent *event) override
    {
        Q_UNUSED(event);

        QPainter painter(this);
        painter.setRenderHint(QPainter::Antialiasing);

        // 背景
        QColor bgColor = m_checked ?
            QColor(0, 200, 100).lighter(100 + (1 - m_handlePosition) * 50) :
            QColor(200, 200, 200);
        painter.setBrush(bgColor);
        painter.setPen(Qt::NoPen);
        painter.drawRoundedRect(rect(), height() / 2, height() / 2);

        // 滑块
        qreal handleX = 3 + m_handlePosition * (width() - height() - 6 + 6);
        QRectF handleRect(handleX, 3, height() - 6, height() - 6);
        painter.setBrush(Qt::white);
        painter.drawEllipse(handleRect);
    }

    void mousePressEvent(QMouseEvent *event) override
    {
        if (event->button() == Qt::LeftButton) {
            setChecked(!m_checked);
        }
    }

private:
    bool m_checked;
    qreal m_handlePosition;
    QPropertyAnimation *m_animation;
};

// 自定义评分控件
class StarRating : public QWidget
{
    Q_OBJECT
    Q_PROPERTY(int rating READ rating WRITE setRating NOTIFY ratingChanged)

public:
    explicit StarRating(int maxStars = 5, QWidget *parent = nullptr)
        : QWidget(parent), m_rating(0), m_maxStars(maxStars), m_hoverStar(-1)
    {
        setMouseTracking(true);
        setMinimumSize(maxStars * 30, 30);
    }

    int rating() const { return m_rating; }
    int maxStars() const { return m_maxStars; }

    QSize sizeHint() const override { return QSize(m_maxStars * 30, 30); }

public slots:
    void setRating(int rating)
    {
        if (m_rating != rating) {
            m_rating = qBound(0, rating, m_maxStars);
            emit ratingChanged(m_rating);
            update();
        }
    }

signals:
    void ratingChanged(int rating);

protected:
    void paintEvent(QPaintEvent *event) override
    {
        Q_UNUSED(event);

        QPainter painter(this);
        painter.setRenderHint(QPainter::Antialiasing);

        int starSize = qMin(width() / m_maxStars, height()) - 4;

        for (int i = 0; i < m_maxStars; ++i) {
            QRectF starRect(i * (starSize + 4) + 2, 2, starSize, starSize);

            bool filled = (i < m_rating) || (m_hoverStar >= 0 && i <= m_hoverStar);
            drawStar(&painter, starRect, filled);
        }
    }

    void mouseMoveEvent(QMouseEvent *event) override
    {
        int starSize = qMin(width() / m_maxStars, height()) - 4;
        m_hoverStar = event->position().x() / (starSize + 4);
        update();
    }

    void leaveEvent(QEvent *event) override
    {
        Q_UNUSED(event);
        m_hoverStar = -1;
        update();
    }

    void mousePressEvent(QMouseEvent *event) override
    {
        if (event->button() == Qt::LeftButton) {
            int starSize = qMin(width() / m_maxStars, height()) - 4;
            int clickedStar = event->position().x() / (starSize + 4);
            setRating(clickedStar + 1);
        }
    }

private:
    void drawStar(QPainter *painter, const QRectF &rect, bool filled)
    {
        QPainterPath path;
        QPointF center = rect.center();
        qreal r = rect.width() / 2;

        for (int i = 0; i < 5; ++i) {
            qreal angle = -M_PI / 2 + i * 2 * M_PI / 5;
            QPointF p(center.x() + r * cos(angle), center.y() + r * sin(angle));
            if (i == 0)
                path.moveTo(p);
            else
                path.lineTo(p);

            angle += M_PI / 5;
            QPointF inner(center.x() + r * 0.4 * cos(angle),
                         center.y() + r * 0.4 * sin(angle));
            path.lineTo(inner);
        }
        path.closeSubpath();

        painter->setPen(QPen(Qt::darkYellow, 1));
        painter->setBrush(filled ? Qt::yellow : Qt::white);
        painter->drawPath(path);
    }

    int m_rating;
    int m_maxStars;
    int m_hoverStar;
};

// 主窗口
class CustomWidgetsDemo : public QWidget
{
    Q_OBJECT

public:
    explicit CustomWidgetsDemo(QWidget *parent = nullptr)
        : QWidget(parent)
    {
        setWindowTitle("Qt6 Custom Widgets Demo");
        resize(400, 400);

        QVBoxLayout *layout = new QVBoxLayout(this);

        // 圆形进度条
        layout->addWidget(new QLabel("圆形进度条:"));
        CircularProgress *progress = new CircularProgress(this);
        layout->addWidget(progress, 0, Qt::AlignCenter);

        QSlider *slider = new QSlider(Qt::Horizontal, this);
        slider->setRange(0, 100);
        connect(slider, &QSlider::valueChanged, progress, &CircularProgress::setValue);
        layout->addWidget(slider);

        // 自动递增
        QTimer *timer = new QTimer(this);
        connect(timer, &QTimer::timeout, [slider]() {
            slider->setValue((slider->value() + 1) % 101);
        });
        timer->start(100);

        layout->addSpacing(20);

        // 开关按钮
        layout->addWidget(new QLabel("开关按钮:"));
        QHBoxLayout *switchLayout = new QHBoxLayout;
        ToggleSwitch *toggle = new ToggleSwitch(this);
        QLabel *statusLabel = new QLabel("关闭", this);
        connect(toggle, &ToggleSwitch::toggled, [statusLabel](bool checked) {
            statusLabel->setText(checked ? "开启" : "关闭");
        });
        switchLayout->addWidget(toggle);
        switchLayout->addWidget(statusLabel);
        switchLayout->addStretch();
        layout->addLayout(switchLayout);

        layout->addSpacing(20);

        // 星级评分
        layout->addWidget(new QLabel("星级评分 (点击选择):"));
        QHBoxLayout *ratingLayout = new QHBoxLayout;
        StarRating *rating = new StarRating(5, this);
        QLabel *ratingLabel = new QLabel("0 星", this);
        connect(rating, &StarRating::ratingChanged, [ratingLabel](int r) {
            ratingLabel->setText(QString("%1 星").arg(r));
        });
        ratingLayout->addWidget(rating);
        ratingLayout->addWidget(ratingLabel);
        ratingLayout->addStretch();
        layout->addLayout(ratingLayout);

        layout->addStretch();
    }
};

int main(int argc, char *argv[])
{
    QApplication app(argc, argv);

    qDebug() << "=== Qt6 自定义控件示例 ===\n";
    qDebug() << "展示了三种自定义控件:";
    qDebug() << "1. 圆形进度条 (重写 paintEvent)";
    qDebug() << "2. 开关按钮 (带动画)";
    qDebug() << "3. 星级评分 (鼠标交互)\n";

    CustomWidgetsDemo demo;
    demo.show();

    return app.exec();
}

#include "main.moc"
