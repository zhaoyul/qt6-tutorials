/**
 * Qt6 UDP 通信示例
 *
 * QUdpSocket 特点：
 * - 无连接协议
 * - 数据报 (Datagram) 方式
 * - 支持广播和组播
 *
 * 主要方法：
 * - writeDatagram(): 发送数据报
 * - readDatagram(): 接收数据报
 * - bind(): 绑定端口接收数据
 *
 * 官方文档: https://doc.qt.io/qt-6/qudpsocket.html
 */

#include <QCoreApplication>
#include <QUdpSocket>
#include <QNetworkDatagram>
#include <QTimer>
#include <QDebug>

class UdpReceiver : public QObject
{
    Q_OBJECT

public:
    explicit UdpReceiver(quint16 port, QObject *parent = nullptr)
        : QObject(parent), m_receivedCount(0)
    {
        m_socket = new QUdpSocket(this);

        if (m_socket->bind(QHostAddress::LocalHost, port)) {
            qDebug() << "[接收端] 绑定端口:" << port;
        } else {
            qDebug() << "[接收端] 绑定失败:" << m_socket->errorString();
        }

        connect(m_socket, &QUdpSocket::readyRead,
                this, &UdpReceiver::onReadyRead);
    }

    quint16 port() const { return m_socket->localPort(); }

private slots:
    void onReadyRead()
    {
        while (m_socket->hasPendingDatagrams()) {
            QNetworkDatagram datagram = m_socket->receiveDatagram();
            qDebug() << "[接收端] 收到来自"
                     << datagram.senderAddress().toString()
                     << ":" << datagram.senderPort()
                     << "的数据:" << datagram.data();

            // 回复
            QByteArray reply = "ACK: " + datagram.data();
            m_socket->writeDatagram(datagram.makeReply(reply));

            if (++m_receivedCount >= 3) {
                QTimer::singleShot(500, qApp, &QCoreApplication::quit);
            }
        }
    }

private:
    QUdpSocket *m_socket;
    int m_receivedCount;
};

class UdpSender : public QObject
{
    Q_OBJECT

public:
    explicit UdpSender(QObject *parent = nullptr)
        : QObject(parent), m_sendCount(0)
    {
        m_socket = new QUdpSocket(this);

        // 绑定以接收回复
        m_socket->bind();
        qDebug() << "[发送端] 绑定端口:" << m_socket->localPort();

        connect(m_socket, &QUdpSocket::readyRead, [this]() {
            while (m_socket->hasPendingDatagrams()) {
                QNetworkDatagram datagram = m_socket->receiveDatagram();
                qDebug() << "[发送端] 收到回复:" << datagram.data();
            }
        });
    }

    void sendTo(const QString &host, quint16 port, const QByteArray &data)
    {
        qDebug() << "[发送端] 发送到" << host << ":" << port << "->" << data;
        m_socket->writeDatagram(data, QHostAddress(host), port);
    }

    void startSending(quint16 targetPort)
    {
        QTimer *timer = new QTimer(this);
        connect(timer, &QTimer::timeout, [this, timer, targetPort]() {
            if (m_sendCount < 3) {
                sendTo("127.0.0.1", targetPort,
                       QString("UDP消息 #%1").arg(++m_sendCount).toUtf8());
            } else {
                timer->stop();
            }
        });
        timer->start(300);
    }

private:
    QUdpSocket *m_socket;
    int m_sendCount;
};

void demonstrateBasicUdp()
{
    qDebug() << "\n=== UDP 基本操作 ===\n";

    QUdpSocket socket;

    // 发送数据报 (不需要连接)
    qDebug() << "UDP 是无连接协议";
    qDebug() << "可以直接发送数据到任意地址和端口";
    qDebug() << "数据以数据报形式传输，可能丢失或乱序";
}

void demonstrateBroadcast()
{
    qDebug() << "\n=== UDP 广播说明 ===\n";

    qDebug() << "广播地址: QHostAddress::Broadcast (255.255.255.255)";
    qDebug() << "子网广播: 如 192.168.1.255";
    qDebug() << "组播地址: 224.0.0.0 - 239.255.255.255";
    qDebug() << "\n使用 writeDatagram() 发送到广播/组播地址";
    qDebug() << "使用 joinMulticastGroup() 加入组播组";
}

int main(int argc, char *argv[])
{
    QCoreApplication app(argc, argv);

    qDebug() << "=== Qt6 UDP 通信示例 ===";

    demonstrateBasicUdp();
    demonstrateBroadcast();

    qDebug() << "\n=== UDP 通信演示 ===\n";

    // 创建接收端
    UdpReceiver receiver(0);  // 自动选择端口

    // 创建发送端
    UdpSender sender;

    // 开始发送
    QTimer::singleShot(100, [&sender, &receiver]() {
        sender.startSending(receiver.port());
    });

    return app.exec();
}

#include "main.moc"
