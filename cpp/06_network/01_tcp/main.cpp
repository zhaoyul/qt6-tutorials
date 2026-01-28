/**
 * Qt6 TCP 通信示例
 *
 * 主要类：
 * - QTcpServer: TCP 服务器
 * - QTcpSocket: TCP 客户端/连接
 *
 * 异步模式 (推荐):
 * - 使用信号槽处理连接和数据
 * - readyRead 信号表示有数据可读
 * - connected/disconnected 信号
 *
 * 官方文档: https://doc.qt.io/qt-6/qtcpsocket.html
 */

#include <QCoreApplication>
#include <QTcpServer>
#include <QTcpSocket>
#include <QTimer>
#include <QDebug>

// 简单的 Echo 服务器
class EchoServer : public QObject
{
    Q_OBJECT

public:
    explicit EchoServer(quint16 port, QObject *parent = nullptr)
        : QObject(parent)
    {
        m_server = new QTcpServer(this);

        connect(m_server, &QTcpServer::newConnection,
                this, &EchoServer::onNewConnection);

        if (m_server->listen(QHostAddress::LocalHost, port)) {
            qDebug() << "[服务器] 监听端口:" << port;
        } else {
            qDebug() << "[服务器] 监听失败:" << m_server->errorString();
        }
    }

    quint16 port() const { return m_server->serverPort(); }

private slots:
    void onNewConnection()
    {
        QTcpSocket *client = m_server->nextPendingConnection();
        qDebug() << "[服务器] 新连接来自:" << client->peerAddress().toString()
                 << ":" << client->peerPort();

        connect(client, &QTcpSocket::readyRead, [this, client]() {
            QByteArray data = client->readAll();
            qDebug() << "[服务器] 收到:" << data;

            // Echo 回去
            client->write("Echo: " + data);
        });

        connect(client, &QTcpSocket::disconnected, [client]() {
            qDebug() << "[服务器] 客户端断开";
            client->deleteLater();
        });
    }

private:
    QTcpServer *m_server;
};

// TCP 客户端
class TcpClient : public QObject
{
    Q_OBJECT

public:
    explicit TcpClient(QObject *parent = nullptr)
        : QObject(parent), m_messageCount(0)
    {
        m_socket = new QTcpSocket(this);

        connect(m_socket, &QTcpSocket::connected,
                this, &TcpClient::onConnected);

        connect(m_socket, &QTcpSocket::disconnected,
                this, &TcpClient::onDisconnected);

        connect(m_socket, &QTcpSocket::readyRead,
                this, &TcpClient::onReadyRead);

        connect(m_socket, &QTcpSocket::errorOccurred,
                this, &TcpClient::onError);
    }

    void connectToServer(const QString &host, quint16 port)
    {
        qDebug() << "[客户端] 连接到" << host << ":" << port;
        m_socket->connectToHost(host, port);
    }

    void sendMessage(const QString &message)
    {
        if (m_socket->state() == QAbstractSocket::ConnectedState) {
            qDebug() << "[客户端] 发送:" << message;
            m_socket->write(message.toUtf8());
        }
    }

private slots:
    void onConnected()
    {
        qDebug() << "[客户端] 已连接到服务器";

        // 发送测试消息
        QTimer *timer = new QTimer(this);
        connect(timer, &QTimer::timeout, [this, timer]() {
            if (m_messageCount < 3) {
                sendMessage(QString("消息 #%1").arg(++m_messageCount));
            } else {
                timer->stop();
                m_socket->disconnectFromHost();
            }
        });
        timer->start(500);
    }

    void onDisconnected()
    {
        qDebug() << "[客户端] 已断开连接";
        QCoreApplication::quit();
    }

    void onReadyRead()
    {
        QByteArray data = m_socket->readAll();
        qDebug() << "[客户端] 收到:" << data;
    }

    void onError(QAbstractSocket::SocketError error)
    {
        qDebug() << "[客户端] 错误:" << error << m_socket->errorString();
    }

private:
    QTcpSocket *m_socket;
    int m_messageCount;
};

int main(int argc, char *argv[])
{
    QCoreApplication app(argc, argv);

    qDebug() << "=== Qt6 TCP 通信示例 ===\n";

    // 创建服务器
    EchoServer server(0);  // 0 = 自动选择端口
    quint16 port = server.port();

    // 创建客户端并连接
    TcpClient client;
    QTimer::singleShot(100, [&client, port]() {
        client.connectToServer("127.0.0.1", port);
    });

    return app.exec();
}

#include "main.moc"
