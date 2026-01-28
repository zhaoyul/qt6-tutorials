/**
 * Qt6 字体系统示例
 *
 * 主要类：
 * - QFont: 字体选择和配置
 * - QFontMetrics: 字体度量信息
 * - QFontDatabase: 系统字体数据库
 * - QFontInfo: 实际使用的字体信息
 *
 * 官方文档: https://doc.qt.io/qt-6/qfont.html
 */

#include <QGuiApplication>
#include <QFont>
#include <QFontMetrics>
#include <QFontDatabase>
#include <QFontInfo>
#include <QImage>
#include <QPainter>
#include <QDebug>

void exploreSystemFonts()
{
    qDebug() << "=== 系统字体 ===\n";

    // 列出所有字体家族
    QStringList families = QFontDatabase::families();
    qDebug() << "系统字体数量:" << families.size();
    qDebug() << "\n前10个字体:";
    for (int i = 0; i < qMin(10, families.size()); ++i) {
        qDebug() << "  " << families[i];
    }

    // 检查字体样式
    QString fontFamily = "Arial";
    if (families.contains(fontFamily)) {
        qDebug() << "\n" << fontFamily << "的样式:";
        QStringList styles = QFontDatabase::styles(fontFamily);
        for (const QString &style : styles) {
            qDebug() << "  " << style;
        }
    }

    // 标准字体
    qDebug() << "\n标准字体:";
    qDebug() << "系统字体:" << QFontDatabase::systemFont(QFontDatabase::GeneralFont).family();
    qDebug() << "等宽字体:" << QFontDatabase::systemFont(QFontDatabase::FixedFont).family();
    qDebug() << "标题字体:" << QFontDatabase::systemFont(QFontDatabase::TitleFont).family();
}

void demonstrateQFont()
{
    qDebug() << "\n=== QFont 配置 ===\n";

    // 基本创建
    QFont font1("Arial", 12);
    qDebug() << "基本字体:" << font1.family() << font1.pointSize();

    // 详细配置
    QFont font2;
    font2.setFamily("Times New Roman");
    font2.setPointSize(14);
    font2.setWeight(QFont::Bold);       // 粗细
    font2.setItalic(true);              // 斜体
    font2.setUnderline(true);           // 下划线
    font2.setStrikeOut(false);          // 删除线

    qDebug() << "配置字体:";
    qDebug() << "  家族:" << font2.family();
    qDebug() << "  大小:" << font2.pointSize() << "pt";
    qDebug() << "  粗细:" << font2.weight();
    qDebug() << "  斜体:" << font2.italic();
    qDebug() << "  下划线:" << font2.underline();

    // 像素大小
    QFont font3("Arial");
    font3.setPixelSize(20);  // 像素单位
    qDebug() << "\n像素大小:" << font3.pixelSize() << "px";

    // 字体粗细级别
    qDebug() << "\n字体粗细级别:";
    qDebug() << "Thin:" << QFont::Thin;
    qDebug() << "Light:" << QFont::Light;
    qDebug() << "Normal:" << QFont::Normal;
    qDebug() << "Medium:" << QFont::Medium;
    qDebug() << "DemiBold:" << QFont::DemiBold;
    qDebug() << "Bold:" << QFont::Bold;
    qDebug() << "ExtraBold:" << QFont::ExtraBold;
    qDebug() << "Black:" << QFont::Black;
}

void demonstrateFontMetrics()
{
    qDebug() << "\n=== QFontMetrics 度量 ===\n";

    QFont font("Arial", 14);
    QFontMetrics fm(font);

    qDebug() << "字体:" << font.family() << font.pointSize() << "pt";
    qDebug() << "高度:" << fm.height();
    qDebug() << "上升部:" << fm.ascent();
    qDebug() << "下降部:" << fm.descent();
    qDebug() << "行间距:" << fm.leading();
    qDebug() << "平均字符宽度:" << fm.averageCharWidth();
    qDebug() << "最大字符宽度:" << fm.maxWidth();

    // 文字尺寸
    QString text = "Hello, Qt6!";
    QRect boundingRect = fm.boundingRect(text);
    qDebug() << "\n文字 \"" << text << "\" 的尺寸:";
    qDebug() << "  宽度:" << fm.horizontalAdvance(text);
    qDebug() << "  边界矩形:" << boundingRect;

    // 截断文字
    QString longText = "This is a very long text that might need to be elided";
    QString elidedText = fm.elidedText(longText, Qt::ElideRight, 150);
    qDebug() << "\n文字截断 (150px):";
    qDebug() << "  原文:" << longText;
    qDebug() << "  截断:" << elidedText;
}

void demonstrateFontRendering()
{
    qDebug() << "\n=== 字体渲染示例 ===\n";

    QImage image(500, 400, QImage::Format_RGB32);
    image.fill(Qt::white);

    QPainter painter(&image);
    painter.setRenderHint(QPainter::TextAntialiasing);

    int y = 30;

    // 不同大小
    QList<int> sizes = {10, 14, 18, 24, 32};
    for (int size : sizes) {
        QFont font("Arial", size);
        painter.setFont(font);
        painter.setPen(Qt::black);
        painter.drawText(10, y, QString("Size %1pt: Hello Qt6").arg(size));
        y += size + 10;
    }

    y += 20;

    // 不同样式
    QFont normal("Arial", 16);
    QFont bold("Arial", 16, QFont::Bold);
    QFont italic("Arial", 16);
    italic.setItalic(true);
    QFont underline("Arial", 16);
    underline.setUnderline(true);

    painter.setFont(normal);
    painter.drawText(10, y, "Normal");

    painter.setFont(bold);
    painter.drawText(100, y, "Bold");

    painter.setFont(italic);
    painter.drawText(170, y, "Italic");

    painter.setFont(underline);
    painter.drawText(250, y, "Underline");

    y += 40;

    // 不同颜色
    QFont colorFont("Arial", 20, QFont::Bold);
    painter.setFont(colorFont);

    QList<QColor> colors = {Qt::red, Qt::green, Qt::blue, Qt::magenta};
    int x = 10;
    for (const QColor &color : colors) {
        painter.setPen(color);
        painter.drawText(x, y, "Color");
        x += 100;
    }

    y += 40;

    // 等宽字体 (代码展示)
    QFont monoFont = QFontDatabase::systemFont(QFontDatabase::FixedFont);
    monoFont.setPointSize(12);
    painter.setFont(monoFont);
    painter.setPen(Qt::darkGreen);
    painter.drawText(10, y, "int main() { return 0; }  // Monospace");

    y += 40;

    // 中文字体
    QFont chineseFont("Arial", 18);  // 系统会回退到支持中文的字体
    painter.setFont(chineseFont);
    painter.setPen(Qt::black);
    painter.drawText(10, y, "中文字体测试 Chinese Font Test");

    painter.end();

    image.save("fonts_demo.png");
    qDebug() << "字体渲染示例已保存: fonts_demo.png";
}

void demonstrateFontMatching()
{
    qDebug() << "\n=== 字体匹配 ===\n";

    // 请求字体
    QFont requestedFont("Non Existent Font Family", 12);
    QFontInfo actualFont(requestedFont);

    qDebug() << "请求字体:" << requestedFont.family();
    qDebug() << "实际字体:" << actualFont.family();
    qDebug() << "完全匹配:" << actualFont.exactMatch();

    // 字体替换规则
    qDebug() << "\n字体回退策略:";
    qDebug() << "1. Qt 首先尝试完全匹配请求的字体";
    qDebug() << "2. 如果不存在，使用相似的替代字体";
    qDebug() << "3. 最后使用系统默认字体";
}

int main(int argc, char *argv[])
{
    QGuiApplication app(argc, argv);

    qDebug() << "=== Qt6 字体系统示例 ===";

    exploreSystemFonts();
    demonstrateQFont();
    demonstrateFontMetrics();
    demonstrateFontRendering();
    demonstrateFontMatching();

    return 0;
}
