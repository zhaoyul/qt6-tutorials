def run_block_1():
    exec(r"""
from PySide6.QtCore import QObject, QTimer, QCoreApplication
from PySide6.QtNetwork import QTcpServer, QTcpSocket, QHostAddress, QAbstractSocket
import sys

class EchoServer(QObject):
    def __init__(self, port, parent=None):
        super().__init__(parent)
        self._server = QTcpServer(self)
        self._server.newConnection.connect(self._on_new_connection)
        if self._server.listen(QHostAddress.LocalHost, port):
            print(f'[server] listen {self._server.serverPort()}')
        else:
            print(f'[server] listen failed {self._server.errorString()}')

    def port(self):
        return self._server.serverPort()

    def _on_new_connection(self):
        client = self._server.nextPendingConnection()
        print(f'[server] new {client.peerAddress().toString()}:{client.peerPort()}')

        def on_ready_read():
            data = client.readAll()
            print(f'[server] recv {data.data()}')
            client.write(b'Echo: ' + data)

        def on_disconnected():
            print('[server] disconnected')
            client.deleteLater()

        client.readyRead.connect(on_ready_read)
        client.disconnected.connect(on_disconnected)

class TcpClient(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._socket = QTcpSocket(self)
        self._message_count = 0
        self._socket.connected.connect(self._on_connected)
        self._socket.disconnected.connect(self._on_disconnected)
        self._socket.readyRead.connect(self._on_ready_read)
        self._socket.errorOccurred.connect(self._on_error)

    def connect_to_server(self, host, port):
        print(f'[client] connect {host}:{port}')
        self._socket.connectToHost(host, port)

    def send_message(self, message):
        if self._socket.state() == QAbstractSocket.ConnectedState:
            print(f'[client] send {message}')
            self._socket.write(message.encode())

    def _on_connected(self):
        print('[client] connected')
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._send_next_message)
        self._timer.start(500)

    def _send_next_message(self):
        if self._message_count < 3:
            self._message_count += 1
            self.send_message(f'message #{self._message_count}')
        else:
            self._timer.stop()
            self._socket.disconnectFromHost()

    def _on_disconnected(self):
        print('[client] disconnected')
        QCoreApplication.quit()

    def _on_ready_read(self):
        data = self._socket.readAll()
        print(f'[client] recv {data.data()}')

    def _on_error(self, error):
        print(f'[client] error {error} {self._socket.errorString()}')

app = QCoreApplication(sys.argv)
print('=== PySide6 TCP 通信示例 ===\n')
server = EchoServer(0)
port = server.port()
client = TcpClient()
QTimer.singleShot(100, lambda: client.connect_to_server('127.0.0.1', port))
app.exec()
""", globals())
