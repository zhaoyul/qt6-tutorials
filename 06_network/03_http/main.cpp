/**
 * Qt6 HTTP 请求示例
 *
 * 主要类：
 * - QNetworkAccessManager: 管理网络请求
 * - QNetworkRequest: 请求配置
 * - QNetworkReply: 响应
 *
 * 支持的操作：
 * - GET, POST, PUT, DELETE 等
 * - HTTPS (SSL/TLS)
 * - 重定向处理
 * - Cookie 管理
 *
 * 官方文档: https://doc.qt.io/qt-6/qnetworkaccessmanager.html
 */

#include <QCoreApplication>
#include <QNetworkAccessManager>
#include <QNetworkRequest>
#include <QNetworkReply>
#include <QUrl>
#include <QUrlQuery>
#include <QJsonDocument>
#include <QJsonObject>
#include <QJsonArray>
#include <QTimer>
#include <QDebug>

class HttpClient : public QObject
{
    Q_OBJECT

public:
    explicit HttpClient(QObject *parent = nullptr)
        : QObject(parent), m_pendingRequests(0)
    {
        m_manager = new QNetworkAccessManager(this);

        // 处理 SSL 错误 (生产环境应该更严格)
        connect(m_manager, &QNetworkAccessManager::sslErrors,
                [](QNetworkReply *reply, const QList<QSslError> &errors) {
                    qDebug() << "SSL 错误:" << errors;
                    reply->ignoreSslErrors();  // 仅用于测试
                });
    }

    // GET 请求
    void get(const QUrl &url)
    {
        qDebug() << "\n--- GET 请求 ---";
        qDebug() << "URL:" << url.toString();

        QNetworkRequest request(url);
        request.setHeader(QNetworkRequest::UserAgentHeader, "Qt6-HTTP-Demo/1.0");

        m_pendingRequests++;
        QNetworkReply *reply = m_manager->get(request);
        connect(reply, &QNetworkReply::finished,
                this, [this, reply]() { handleReply(reply); });
    }

    // POST 请求 (JSON)
    void postJson(const QUrl &url, const QJsonObject &json)
    {
        qDebug() << "\n--- POST JSON 请求 ---";
        qDebug() << "URL:" << url.toString();
        qDebug() << "Body:" << QJsonDocument(json).toJson(QJsonDocument::Compact);

        QNetworkRequest request(url);
        request.setHeader(QNetworkRequest::ContentTypeHeader, "application/json");

        QByteArray data = QJsonDocument(json).toJson(QJsonDocument::Compact);

        m_pendingRequests++;
        QNetworkReply *reply = m_manager->post(request, data);
        connect(reply, &QNetworkReply::finished,
                this, [this, reply]() { handleReply(reply); });
    }

    // POST 请求 (表单)
    void postForm(const QUrl &url, const QUrlQuery &formData)
    {
        qDebug() << "\n--- POST Form 请求 ---";
        qDebug() << "URL:" << url.toString();

        QNetworkRequest request(url);
        request.setHeader(QNetworkRequest::ContentTypeHeader,
                         "application/x-www-form-urlencoded");

        QByteArray data = formData.toString(QUrl::FullyEncoded).toUtf8();

        m_pendingRequests++;
        QNetworkReply *reply = m_manager->post(request, data);
        connect(reply, &QNetworkReply::finished,
                this, [this, reply]() { handleReply(reply); });
    }

    // 带进度的下载
    void downloadWithProgress(const QUrl &url)
    {
        qDebug() << "\n--- 下载请求 (带进度) ---";
        qDebug() << "URL:" << url.toString();

        QNetworkRequest request(url);

        m_pendingRequests++;
        QNetworkReply *reply = m_manager->get(request);

        connect(reply, &QNetworkReply::downloadProgress,
                [](qint64 received, qint64 total) {
                    if (total > 0) {
                        qDebug() << "下载进度:" << received << "/" << total
                                 << "(" << (received * 100 / total) << "%)";
                    }
                });

        connect(reply, &QNetworkReply::finished,
                this, [this, reply]() { handleReply(reply); });
    }

private slots:
    void handleReply(QNetworkReply *reply)
    {
        qDebug() << "\n=== 响应 ===";

        // 检查错误
        if (reply->error() != QNetworkReply::NoError) {
            qDebug() << "错误:" << reply->errorString();
        } else {
            // HTTP 状态码
            int statusCode = reply->attribute(
                QNetworkRequest::HttpStatusCodeAttribute).toInt();
            qDebug() << "状态码:" << statusCode;

            // 响应头
            qDebug() << "Content-Type:"
                     << reply->header(QNetworkRequest::ContentTypeHeader).toString();

            // 响应体
            QByteArray data = reply->readAll();
            qDebug() << "响应大小:" << data.size() << "bytes";

            // 尝试解析为 JSON
            QJsonParseError error;
            QJsonDocument doc = QJsonDocument::fromJson(data, &error);
            if (error.error == QJsonParseError::NoError) {
                qDebug() << "JSON 响应:";
                qDebug().noquote() << doc.toJson(QJsonDocument::Indented).left(500);
            } else {
                // 显示原始文本 (截断)
                QString text = QString::fromUtf8(data).left(200);
                qDebug() << "文本响应:" << text;
            }
        }

        reply->deleteLater();
        m_pendingRequests--;

        if (m_pendingRequests == 0) {
            QTimer::singleShot(100, qApp, &QCoreApplication::quit);
        }
    }

private:
    QNetworkAccessManager *m_manager;
    int m_pendingRequests;
};

void demonstrateNetworkInfo()
{
    qDebug() << "=== 网络信息 ===\n";

    qDebug() << "QNetworkAccessManager 特点:";
    qDebug() << "- 异步操作，使用信号槽";
    qDebug() << "- 自动处理重定向";
    qDebug() << "- 支持 HTTPS";
    qDebug() << "- 连接池复用";
    qDebug() << "- Cookie 管理";
}

int main(int argc, char *argv[])
{
    QCoreApplication app(argc, argv);

    qDebug() << "=== Qt6 HTTP 请求示例 ===\n";

    demonstrateNetworkInfo();

    HttpClient client;

    // GET 请求 (使用 httpbin 测试 API)
    client.get(QUrl("https://httpbin.org/get"));

    // POST JSON 请求
    QJsonObject json;
    json["name"] = "Qt6";
    json["version"] = 6;
    client.postJson(QUrl("https://httpbin.org/post"), json);

    // 注意: 这些请求需要网络连接
    // 如果无法访问外网，请求会失败

    return app.exec();
}

#include "main.moc"
