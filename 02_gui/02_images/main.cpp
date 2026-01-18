/**
 * Qt6 图像处理示例
 *
 * 主要类：
 * - QImage: 独立于硬件的图像表示，支持像素访问
 * - QPixmap: 优化的屏幕显示图像
 * - QBitmap: 单色 QPixmap
 * - QIcon: 多分辨率图标
 *
 * QImage vs QPixmap:
 * - QImage: I/O操作、像素操作、非GUI线程
 * - QPixmap: 屏幕显示、性能优化
 *
 * 官方文档: https://doc.qt.io/qt-6/qimage.html
 */

#include <QGuiApplication>
#include <QImage>
#include <QImageReader>
#include <QImageWriter>
#include <QPixmap>
#include <QColor>
#include <QPainter>
#include <QDebug>

void createImageFromScratch()
{
    qDebug() << "\n=== 创建图像 ===\n";

    // 创建空白图像
    QImage image(200, 150, QImage::Format_RGB32);
    image.fill(Qt::white);

    qDebug() << "尺寸:" << image.size();
    qDebug() << "宽度:" << image.width();
    qDebug() << "高度:" << image.height();
    qDebug() << "深度:" << image.depth() << "bits";
    qDebug() << "格式:" << image.format();
    qDebug() << "字节数:" << image.sizeInBytes();

    // 直接设置像素
    for (int y = 0; y < image.height(); ++y) {
        for (int x = 0; x < image.width(); ++x) {
            // 创建渐变效果
            int r = x * 255 / image.width();
            int g = y * 255 / image.height();
            int b = 128;
            image.setPixel(x, y, qRgb(r, g, b));
        }
    }

    image.save("gradient.png");
    qDebug() << "渐变图像已保存: gradient.png";
}

void manipulatePixels()
{
    qDebug() << "\n=== 像素操作 ===\n";

    QImage image(100, 100, QImage::Format_ARGB32);
    image.fill(Qt::white);

    // 方式1: setPixel (慢，但简单)
    for (int i = 0; i < 50; ++i) {
        image.setPixel(i, i, qRgba(255, 0, 0, 255));
    }

    // 方式2: scanLine (快，推荐)
    for (int y = 0; y < image.height(); ++y) {
        QRgb *line = reinterpret_cast<QRgb*>(image.scanLine(y));
        for (int x = 50; x < 100; ++x) {
            if (y >= 50) {
                line[x] = qRgba(0, 0, 255, 128);  // 半透明蓝
            }
        }
    }

    // 读取像素
    QRgb pixel = image.pixel(25, 25);
    qDebug() << "像素(25,25) R:" << qRed(pixel)
             << "G:" << qGreen(pixel)
             << "B:" << qBlue(pixel)
             << "A:" << qAlpha(pixel);

    image.save("pixels.png");
    qDebug() << "像素操作图像已保存: pixels.png";
}

void imageTransformations()
{
    qDebug() << "\n=== 图像变换 ===\n";

    // 创建原始图像
    QImage original(100, 80, QImage::Format_RGB32);
    QPainter p(&original);
    p.fillRect(original.rect(), Qt::white);
    p.setPen(Qt::blue);
    p.setFont(QFont("Arial", 20));
    p.drawText(original.rect(), Qt::AlignCenter, "Qt6");
    p.end();

    original.save("original.png");

    // 缩放
    QImage scaled = original.scaled(200, 160, Qt::KeepAspectRatio,
                                    Qt::SmoothTransformation);
    scaled.save("scaled.png");
    qDebug() << "缩放: 100x80 -> " << scaled.size();

    // 镜像
    QImage mirrored = original.mirrored(true, false);  // 水平镜像
    mirrored.save("mirrored.png");
    qDebug() << "水平镜像已保存";

    // 旋转 (通过 QTransform)
    QTransform transform;
    transform.rotate(45);
    QImage rotated = original.transformed(transform, Qt::SmoothTransformation);
    rotated.save("rotated.png");
    qDebug() << "旋转45度已保存";

    // 裁剪
    QImage cropped = original.copy(10, 10, 50, 40);
    cropped.save("cropped.png");
    qDebug() << "裁剪已保存";
}

void imageFormats()
{
    qDebug() << "\n=== 图像格式 ===\n";

    qDebug() << "支持的读取格式:";
    for (const QByteArray &format : QImageReader::supportedImageFormats()) {
        qDebug() << "  " << format;
    }

    qDebug() << "\n支持的写入格式:";
    for (const QByteArray &format : QImageWriter::supportedImageFormats()) {
        qDebug() << "  " << format;
    }
}

void colorConversion()
{
    qDebug() << "\n=== 颜色与格式转换 ===\n";

    QImage colorImage(100, 100, QImage::Format_ARGB32);
    colorImage.fill(QColor(100, 150, 200));

    // 转换为灰度
    QImage grayscale = colorImage.convertToFormat(QImage::Format_Grayscale8);
    grayscale.save("grayscale.png");
    qDebug() << "灰度图像已保存";

    // 转换为单色
    QImage mono = colorImage.convertToFormat(QImage::Format_Mono);
    mono.save("mono.png");
    qDebug() << "单色图像已保存";

    // QColor 操作
    QColor color(255, 128, 64);
    qDebug() << "\nQColor 示例:";
    qDebug() << "RGB:" << color.red() << color.green() << color.blue();
    qDebug() << "HSV:" << color.hue() << color.saturation() << color.value();
    qDebug() << "十六进制:" << color.name();

    // 颜色变换
    QColor lighter = color.lighter(150);  // 150% 亮度
    QColor darker = color.darker(150);    // 150% 暗度
    qDebug() << "更亮:" << lighter.name();
    qDebug() << "更暗:" << darker.name();
}

void compositeImages()
{
    qDebug() << "\n=== 图像合成 ===\n";

    // 背景
    QImage background(200, 150, QImage::Format_ARGB32);
    background.fill(QColor(200, 220, 255));

    // 前景 (带透明)
    QImage foreground(100, 75, QImage::Format_ARGB32);
    foreground.fill(Qt::transparent);
    QPainter fp(&foreground);
    fp.setBrush(QColor(255, 0, 0, 180));
    fp.drawEllipse(foreground.rect());
    fp.end();

    // 合成
    QPainter painter(&background);
    painter.setCompositionMode(QPainter::CompositionMode_SourceOver);
    painter.drawImage(50, 37, foreground);
    painter.end();

    background.save("composite.png");
    qDebug() << "合成图像已保存: composite.png";

    qDebug() << "\n常用合成模式:";
    qDebug() << "- SourceOver: 标准 alpha 混合";
    qDebug() << "- DestinationOver: 目标在上";
    qDebug() << "- Clear: 清除";
    qDebug() << "- Source: 替换";
    qDebug() << "- Multiply: 正片叠底";
    qDebug() << "- Screen: 滤色";
}

int main(int argc, char *argv[])
{
    QGuiApplication app(argc, argv);

    qDebug() << "=== Qt6 图像处理示例 ===";

    createImageFromScratch();
    manipulatePixels();
    imageTransformations();
    imageFormats();
    colorConversion();
    compositeImages();

    qDebug() << "\n=== 图像处理要点 ===";
    qDebug() << "1. QImage 用于像素操作";
    qDebug() << "2. QPixmap 用于屏幕显示";
    qDebug() << "3. scanLine() 比 pixel() 快";
    qDebug() << "4. 使用 Qt::SmoothTransformation 获得好质量";

    return 0;
}
