/**
 * Qt6 I/O 系统示例
 *
 * Qt 提供跨平台的文件和I/O操作：
 * - QFile: 文件读写
 * - QDir: 目录操作
 * - QFileInfo: 文件信息
 * - QTextStream: 文本流
 * - QDataStream: 二进制流
 * - QIODevice: I/O 基类
 *
 * 官方文档: https://doc.qt.io/qt-6/io.html
 */

#include <QCoreApplication>
#include <QFile>
#include <QDir>
#include <QFileInfo>
#include <QTextStream>
#include <QDataStream>
#include <QTemporaryFile>
#include <QStandardPaths>
#include <QDebug>

void demonstrateQFile()
{
    qDebug() << "=== QFile 示例 ===\n";

    // 写入文本文件
    QString fileName = "test.txt";

    QFile writeFile(fileName);
    if (writeFile.open(QIODevice::WriteOnly | QIODevice::Text)) {
        QTextStream out(&writeFile);
        out << "Hello, Qt6!\n";
        out << "这是中文内容\n";
        out << "Line 3\n";
        writeFile.close();
        qDebug() << "文件写入成功:" << fileName;
    }

    // 读取文本文件
    QFile readFile(fileName);
    if (readFile.open(QIODevice::ReadOnly | QIODevice::Text)) {
        QTextStream in(&readFile);
        qDebug() << "\n文件内容:";
        while (!in.atEnd()) {
            QString line = in.readLine();
            qDebug() << "  " << line;
        }
        readFile.close();
    }

    // 一次性读取
    if (readFile.open(QIODevice::ReadOnly | QIODevice::Text)) {
        qDebug() << "\n全部内容:" << readFile.readAll();
        readFile.close();
    }

    // 追加模式
    if (writeFile.open(QIODevice::Append | QIODevice::Text)) {
        QTextStream out(&writeFile);
        out << "追加的内容\n";
        writeFile.close();
        qDebug() << "内容已追加";
    }
}

void demonstrateQDataStream()
{
    qDebug() << "\n=== QDataStream (二进制) 示例 ===\n";

    QString binFileName = "data.bin";

    // 写入二进制
    QFile writeFile(binFileName);
    if (writeFile.open(QIODevice::WriteOnly)) {
        QDataStream out(&writeFile);
        out.setVersion(QDataStream::Qt_6_0);

        // 写入各种类型
        out << QString("Hello");
        out << (qint32)12345;
        out << (double)3.14159;
        out << QStringList{"Apple", "Banana", "Cherry"};

        writeFile.close();
        qDebug() << "二进制写入成功";
    }

    // 读取二进制
    QFile readFile(binFileName);
    if (readFile.open(QIODevice::ReadOnly)) {
        QDataStream in(&readFile);
        in.setVersion(QDataStream::Qt_6_0);

        QString str;
        qint32 num;
        double dbl;
        QStringList list;

        in >> str >> num >> dbl >> list;

        qDebug() << "读取字符串:" << str;
        qDebug() << "读取整数:" << num;
        qDebug() << "读取浮点:" << dbl;
        qDebug() << "读取列表:" << list;

        readFile.close();
    }
}

void demonstrateQDir()
{
    qDebug() << "\n=== QDir 示例 ===\n";

    QDir currentDir = QDir::current();

    qDebug() << "当前目录:" << currentDir.absolutePath();
    qDebug() << "主目录:" << QDir::homePath();
    qDebug() << "临时目录:" << QDir::tempPath();
    qDebug() << "根目录:" << QDir::rootPath();

    // 列出文件
    qDebug() << "\n当前目录文件:";
    QStringList files = currentDir.entryList(QDir::Files);
    for (const QString &file : files) {
        qDebug() << "  " << file;
    }

    // 列出子目录
    qDebug() << "\n子目录:";
    QStringList dirs = currentDir.entryList(QDir::Dirs | QDir::NoDotAndDotDot);
    for (const QString &dir : dirs) {
        qDebug() << "  " << dir;
    }

    // 过滤文件
    qDebug() << "\nC++ 文件:";
    QStringList cppFiles = currentDir.entryList({"*.cpp", "*.h"}, QDir::Files);
    for (const QString &file : cppFiles) {
        qDebug() << "  " << file;
    }

    // 创建目录
    if (currentDir.mkdir("test_dir")) {
        qDebug() << "\n创建目录成功: test_dir";
        currentDir.rmdir("test_dir");
        qDebug() << "删除目录成功: test_dir";
    }
}

void demonstrateQFileInfo()
{
    qDebug() << "\n=== QFileInfo 示例 ===\n";

    QFileInfo info("test.txt");

    if (info.exists()) {
        qDebug() << "文件名:" << info.fileName();
        qDebug() << "完整路径:" << info.absoluteFilePath();
        qDebug() << "目录:" << info.absolutePath();
        qDebug() << "后缀:" << info.suffix();
        qDebug() << "基本名:" << info.baseName();
        qDebug() << "大小:" << info.size() << "bytes";
        qDebug() << "是文件:" << info.isFile();
        qDebug() << "是目录:" << info.isDir();
        qDebug() << "可读:" << info.isReadable();
        qDebug() << "可写:" << info.isWritable();
        qDebug() << "创建时间:" << info.birthTime().toString();
        qDebug() << "修改时间:" << info.lastModified().toString();
    }
}

void demonstrateStandardPaths()
{
    qDebug() << "\n=== QStandardPaths 示例 ===\n";

    qDebug() << "桌面:" << QStandardPaths::writableLocation(QStandardPaths::DesktopLocation);
    qDebug() << "文档:" << QStandardPaths::writableLocation(QStandardPaths::DocumentsLocation);
    qDebug() << "下载:" << QStandardPaths::writableLocation(QStandardPaths::DownloadLocation);
    qDebug() << "音乐:" << QStandardPaths::writableLocation(QStandardPaths::MusicLocation);
    qDebug() << "图片:" << QStandardPaths::writableLocation(QStandardPaths::PicturesLocation);
    qDebug() << "视频:" << QStandardPaths::writableLocation(QStandardPaths::MoviesLocation);
    qDebug() << "缓存:" << QStandardPaths::writableLocation(QStandardPaths::CacheLocation);
    qDebug() << "配置:" << QStandardPaths::writableLocation(QStandardPaths::ConfigLocation);
    qDebug() << "数据:" << QStandardPaths::writableLocation(QStandardPaths::AppDataLocation);
}

void demonstrateTemporaryFile()
{
    qDebug() << "\n=== QTemporaryFile 示例 ===\n";

    QTemporaryFile tempFile;
    if (tempFile.open()) {
        qDebug() << "临时文件:" << tempFile.fileName();
        tempFile.write("临时内容");
        // 默认关闭时自动删除
    }

    // 保留临时文件
    QTemporaryFile persistentTemp;
    persistentTemp.setAutoRemove(false);
    if (persistentTemp.open()) {
        qDebug() << "持久临时文件:" << persistentTemp.fileName();
    }
}

int main(int argc, char *argv[])
{
    QCoreApplication app(argc, argv);

    qDebug() << "=== Qt6 I/O 系统示例 ===";

    demonstrateQFile();
    demonstrateQDataStream();
    demonstrateQDir();
    demonstrateQFileInfo();
    demonstrateStandardPaths();
    demonstrateTemporaryFile();

    // 清理测试文件
    QFile::remove("test.txt");
    QFile::remove("data.bin");

    qDebug() << "\n测试文件已清理";

    return 0;
}
