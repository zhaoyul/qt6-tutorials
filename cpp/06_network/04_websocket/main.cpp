/**
 * Qt6 WebSocket 客户端示例
 *
 * 主要类：
 * - QWebSocket: WebSocket 客户端
 *
 * 关键信号：
 * - connected: 连接成功
 * - disconnected: 连接断开
 * - textMessageReceived: 收到文本消息
 * - binaryMessageReceived: 收到二进制消息
 * - errorOccurred: 发生错误
 *
 * 官方文档: https://doc.qt.io/qt-6/qwebsocket.html
 */

#include <QCoreApplication>
#include <QWebSocket>
#include <QTimer>
#include <QDebug>
#include <QUrl>

// WebSocket 客户端
class WebSocketClient : public QObject
{
    Q_OBJECT

public:
    explicit WebSocketClient(QObject *parent = nullptr)
        : QObject(parent), m_messageCount(0)
    {
        m_socket = new QWebSocket(QString(), QWebSocketProtocol::VersionLatest, this);

        // 连接信号
        connect(m_socket, &QWebSocket::connected,
                this, &WebSocketClient::onConnected);

        connect(m_socket, &QWebSocket::disconnected,
                this, &WebSocketClient::onDisconnected);

        connect(m_socket, &QWebSocket::textMessageReceived,
                this, &WebSocketClient::onTextMessageReceived);

        connect(m_socket, QOverload<QAbstractSocket::SocketError>::of(&QWebSocket::errorOccurred),
                this, &WebSocketClient::onError);

        connect(m_socket, &QWebSocket::stateChanged,
                this, &WebSocketClient::onStateChanged);

        // SSL 错误处理 (测试服务器可能需要)
        connect(m_socket, &QWebSocket::sslErrors,
                this, &WebSocketClient::onSslErrors);
    }

    void connectToServer(const QUrl &url)
    {
        m_url = url;
        qDebug() << "[WebSocket] 正在连接到:" << url.toString();
        m_socket->open(url);
    }

    void sendMessage(const QString &message)
    {
        if (m_socket->state() == QAbstractSocket::ConnectedState) {
            qDebug() << "[WebSocket] 发送:" << message;
            m_socket->sendTextMessage(message);
        } else {
            qDebug() << "[WebSocket] 无法发送，未连接";
        }
    }

    void close()
    {
        qDebug() << "[WebSocket] 正在关闭连接...";
        m_socket->close();
    }

private slots:
    void onConnected()
    {
        qDebug() << "[WebSocket] 连接成功!";
        qDebug() << "[WebSocket] 服务器地址:" << m_socket->peerAddress().toString()
                 << ":" << m_socket->peerPort();

        // 发送第一条消息
        sendMessage(QString("Hello WebSocket! Message #%1").arg(++m_messageCount));

        // 设置定时器发送更多消息
        QTimer *timer = new QTimer(this);
        connect(timer, &QTimer::timeout, [this, timer]() {
            if (m_messageCount < 3) {
                sendMessage(QString("Test message #%1 from Qt WebSocket client").arg(++m_messageCount));
            } else {
                timer->stop();
                timer->deleteLater();

                // 延迟关闭连接
                QTimer::singleShot(1000, this, &WebSocketClient::close);
            }
        });
        timer->start(1500);
    }

    void onDisconnected()
    {
        qDebug() << "[WebSocket] 连接已断开";
        qDebug() << "[WebSocket] 关闭原因:" << m_socket->closeCode()
                 << "-" << m_socket->closeReason();
        QCoreApplication::quit();
    }

    void onTextMessageReceived(const QString &message)
    {
        qDebug() << "[WebSocket] 收到消息:" << message;
    }

    void onError(QAbstractSocket::SocketError error)
    {
        qDebug() << "[WebSocket] 错误发生:" << error
                 << "-" << m_socket->errorString();
    }

    void onStateChanged(QAbstractSocket::SocketState state)
    {
        static const QHash<QAbstractSocket::SocketState, QString> stateNames = {
            {QAbstractSocket::UnconnectedState, "未连接"},
            {QAbstractSocket::HostLookupState, "查找主机"},
            {QAbstractSocket::ConnectingState, "正在连接"},
            {QAbstractSocket::ConnectedState, "已连接"},
            {QAbstractSocket::BoundState, "已绑定"},
            {QAbstractSocket::ListeningState, "监听中"},
            {QAbstractSocket::ClosingState, "正在关闭"}
        };
        qDebug() << "[WebSocket] 状态变化:" << stateNames.value(state, "未知状态");
    }

    void onSslErrors(const QList<QSslError> &errors)
    {
        qDebug() << "[WebSocket] SSL 错误 (忽略并继续):";
        for (const auto &error : errors) {
            qDebug() << "  -" << error.errorString();
        }
        // 测试时忽略 SSL 错误
        m_socket->ignoreSslErrors();
    }

private:
    QWebSocket *m_socket;
    QUrl m_url;
    int m_messageCount;
};

int main(int argc, char *argv[])
{
    QCoreApplication app(argc, argv);

    qDebug() << "=== Qt6 WebSocket 客户端示例 ===\n";

    WebSocketClient client;

    // 使用 echo.websocket.org 或类似的服务
    // 注意: wss://echo.websocket.org/ 可能已经下线，可以尝试其他 echo 服务
    // 备选: wss://echo.websocket.in/ (可能需要更新)
    QUrl serverUrl("wss://echo.websocket.org/");

    // 如果命令行提供了 URL，使用提供的 URL
    if (argc > 1) {
        serverUrl = QUrl(QString::fromLocal8Bit(argv[1]));
    }

    qDebug() << "使用服务器:" << serverUrl.toString();
    qDebug() << "可以通过命令行参数指定其他服务器，例如:";
    qDebug() << "  ./websocket_demo ws://localhost:8080\n";

    // 延迟连接，让事件循环先启动
    QTimer::singleShot(100, [&client, serverUrl]() {
        client.connectToServer(serverUrl);
    });

    // 超时处理 (30秒)
    QTimer::singleShot(30000, [&client]() {
        qDebug() << "\n[WebSocket] 超时，关闭连接...";
        client.close();
    });

    return app.exec();
}

#include "main.moc"
