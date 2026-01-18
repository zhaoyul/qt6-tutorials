/**
 * Qt6 2D绘图系统示例
 *
 * Qt 提供强大的2D绘图能力：
 * - QPainter: 绑定设备
 * - QPaintDevice: 绘图表面 (QImage, QPixmap, QWidget等)
 * - QPen: 线条样式
 * - QBrush: 填充样式
 * - QFont: 文字样式
 *
 * 主要功能：
 * - 基本图形绘制
 * - 路径绘制 (QPainterPath)
 * - 变换 (旋转、缩放、平移)
 * - 抗锯齿
 *
 * 官方文档: https://doc.qt.io/qt-6/paintsystem.html
 */

#include <QGuiApplication>
#include <QImage>
#include <QPainter>
#include <QPen>
#include <QBrush>
#include <QPainterPath>
#include <QLinearGradient>
#include <QRadialGradient>
#include <QDebug>

void drawBasicShapes(QPainter &painter)
{
    // 基本图形
    painter.setPen(QPen(Qt::black, 2));
    painter.setBrush(Qt::cyan);

    // 矩形
    painter.drawRect(10, 10, 80, 60);

    // 圆角矩形
    painter.setBrush(Qt::magenta);
    painter.drawRoundedRect(100, 10, 80, 60, 10, 10);

    // 椭圆/圆
    painter.setBrush(Qt::yellow);
    painter.drawEllipse(200, 10, 80, 60);

    // 圆
    painter.setBrush(Qt::green);
    painter.drawEllipse(QPoint(340, 40), 30, 30);
}

void drawLines(QPainter &painter)
{
    int y = 100;

    // 不同线型
    QPen pen(Qt::blue, 3);

    pen.setStyle(Qt::SolidLine);
    painter.setPen(pen);
    painter.drawLine(10, y, 180, y);

    pen.setStyle(Qt::DashLine);
    painter.setPen(pen);
    painter.drawLine(10, y + 20, 180, y + 20);

    pen.setStyle(Qt::DotLine);
    painter.setPen(pen);
    painter.drawLine(10, y + 40, 180, y + 40);

    pen.setStyle(Qt::DashDotLine);
    painter.setPen(pen);
    painter.drawLine(10, y + 60, 180, y + 60);

    // 线帽样式
    pen.setStyle(Qt::SolidLine);
    pen.setWidth(10);

    pen.setCapStyle(Qt::FlatCap);
    painter.setPen(pen);
    painter.drawLine(200, y, 280, y);

    pen.setCapStyle(Qt::RoundCap);
    painter.setPen(pen);
    painter.drawLine(200, y + 30, 280, y + 30);

    pen.setCapStyle(Qt::SquareCap);
    painter.setPen(pen);
    painter.drawLine(200, y + 60, 280, y + 60);
}

void drawGradients(QPainter &painter)
{
    int y = 200;

    // 线性渐变
    QLinearGradient linearGrad(10, y, 90, y + 60);
    linearGrad.setColorAt(0, Qt::red);
    linearGrad.setColorAt(0.5, Qt::yellow);
    linearGrad.setColorAt(1, Qt::green);
    painter.setBrush(linearGrad);
    painter.drawRect(10, y, 80, 60);

    // 径向渐变
    QRadialGradient radialGrad(150, y + 30, 40);
    radialGrad.setColorAt(0, Qt::white);
    radialGrad.setColorAt(1, Qt::blue);
    painter.setBrush(radialGrad);
    painter.drawEllipse(110, y, 80, 60);

    // 锥形渐变
    QConicalGradient conicalGrad(250, y + 30, 0);
    conicalGrad.setColorAt(0, Qt::red);
    conicalGrad.setColorAt(0.33, Qt::green);
    conicalGrad.setColorAt(0.66, Qt::blue);
    conicalGrad.setColorAt(1, Qt::red);
    painter.setBrush(conicalGrad);
    painter.drawEllipse(210, y, 80, 60);
}

void drawPath(QPainter &painter)
{
    int y = 300;

    // 自定义路径
    QPainterPath path;
    path.moveTo(10, y + 50);
    path.lineTo(50, y);
    path.lineTo(90, y + 50);
    path.closeSubpath();

    painter.setPen(QPen(Qt::darkGreen, 2));
    painter.setBrush(Qt::lightGray);
    painter.drawPath(path);

    // 贝塞尔曲线
    QPainterPath bezier;
    bezier.moveTo(110, y + 50);
    bezier.cubicTo(130, y, 170, y, 190, y + 50);

    painter.setPen(QPen(Qt::darkMagenta, 3));
    painter.setBrush(Qt::NoBrush);
    painter.drawPath(bezier);

    // 文字路径
    QPainterPath textPath;
    QFont font("Arial", 24, QFont::Bold);
    textPath.addText(210, y + 40, font, "Qt6");

    painter.setPen(Qt::NoPen);
    painter.setBrush(Qt::darkBlue);
    painter.drawPath(textPath);
}

void drawWithTransform(QPainter &painter)
{
    int y = 400;

    painter.save();

    // 平移
    painter.translate(50, y + 30);

    // 绘制原始矩形
    painter.setPen(QPen(Qt::black, 2));
    painter.setBrush(Qt::red);
    painter.drawRect(-20, -15, 40, 30);

    // 旋转
    painter.rotate(30);
    painter.setBrush(QColor(0, 255, 0, 128));  // 半透明
    painter.drawRect(-20, -15, 40, 30);

    painter.restore();

    // 缩放示例
    painter.save();
    painter.translate(150, y + 30);
    painter.scale(1.5, 0.8);
    painter.setBrush(Qt::blue);
    painter.drawEllipse(-25, -25, 50, 50);
    painter.restore();
}

void drawText(QPainter &painter)
{
    int y = 480;

    painter.setPen(Qt::black);

    // 普通文字
    painter.setFont(QFont("Arial", 12));
    painter.drawText(10, y + 20, "Normal Text");

    // 粗体
    painter.setFont(QFont("Arial", 12, QFont::Bold));
    painter.drawText(120, y + 20, "Bold Text");

    // 斜体
    QFont italicFont("Arial", 12);
    italicFont.setItalic(true);
    painter.setFont(italicFont);
    painter.drawText(220, y + 20, "Italic Text");

    // 在矩形内绘制文字
    painter.setFont(QFont("Arial", 10));
    QRect textRect(10, y + 30, 150, 40);
    painter.drawRect(textRect);
    painter.drawText(textRect, Qt::AlignCenter | Qt::TextWordWrap,
                     "Centered text in rectangle");
}

int main(int argc, char *argv[])
{
    QGuiApplication app(argc, argv);

    qDebug() << "=== Qt6 2D绘图系统示例 ===\n";

    // 创建画布
    QImage image(400, 550, QImage::Format_ARGB32);
    image.fill(Qt::white);

    // 创建画家
    QPainter painter(&image);
    painter.setRenderHint(QPainter::Antialiasing);  // 抗锯齿
    painter.setRenderHint(QPainter::TextAntialiasing);

    qDebug() << "绘制基本图形...";
    drawBasicShapes(painter);

    qDebug() << "绘制线条...";
    drawLines(painter);

    qDebug() << "绘制渐变...";
    drawGradients(painter);

    qDebug() << "绘制路径...";
    drawPath(painter);

    qDebug() << "绘制变换...";
    drawWithTransform(painter);

    qDebug() << "绘制文字...";
    drawText(painter);

    painter.end();

    // 保存图像
    QString filename = "painting_demo.png";
    if (image.save(filename)) {
        qDebug() << "\n图像已保存到:" << filename;
    }

    qDebug() << "\n=== 绘图要点 ===";
    qDebug() << "1. QPainter 必须绑定到 QPaintDevice";
    qDebug() << "2. 使用 save()/restore() 保存/恢复状态";
    qDebug() << "3. setRenderHint 启用抗锯齿";
    qDebug() << "4. QPainterPath 用于复杂图形";
    qDebug() << "5. 渐变可用于 QBrush";

    return 0;
}
