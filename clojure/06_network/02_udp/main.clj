#!/usr/bin/env clojure -M
;; PySide6 UDP 通信示例 (Clojure + libpython-clj)

(require '[libpython-clj2.python :as py])

(py/initialize!)

(defn -main
  [& args]
  (println "=== PySide6 UDP 通信示例 (Clojure) ===")

  (py/run-simple-string "
from PySide6.QtCore import QObject, QTimer, QCoreApplication
from PySide6.QtNetwork import QUdpSocket, QHostAddress
import sys

class UdpReceiver(QObject):
    def __init__(self, port, parent=None):
        super().__init__(parent)
        self._socket = QUdpSocket(self)
        self._received_count = 0
        if self._socket.bind(QHostAddress.LocalHost, port):
            print(f'[recv] bound {self._socket.localPort()}')
        else:
            print(f'[recv] bind failed {self._socket.errorString()}')
        self._socket.readyRead.connect(self._on_ready_read)

    def port(self):
        return self._socket.localPort()

    def _on_ready_read(self):
        while self._socket.hasPendingDatagrams():
            datagram = self._socket.receiveDatagram()
            print(f'[recv] from {datagram.senderAddress().toString()}:{datagram.senderPort()} data {datagram.data().data()}')
            reply = b'ACK: ' + datagram.data()
            self._socket.writeDatagram(reply, datagram.senderAddress(), datagram.senderPort())
            self._received_count += 1
            if self._received_count >= 3:
                QTimer.singleShot(500, QCoreApplication.quit)

class UdpSender(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._socket = QUdpSocket(self)
        self._send_count = 0
        self._socket.bind()
        print(f'[send] bound {self._socket.localPort()}')
        self._socket.readyRead.connect(self._on_ready_read)

    def _on_ready_read(self):
        while self._socket.hasPendingDatagrams():
            datagram = self._socket.receiveDatagram()
            print(f'[send] reply {datagram.data().data()}')

    def send_to(self, host, port, data):
        print(f'[send] {host}:{port} -> {data}')
        self._socket.writeDatagram(data.encode(), QHostAddress(host), port)

    def start_sending(self, target_port):
        self._target_port = target_port
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._send_next)
        self._timer.start(300)

    def _send_next(self):
        if self._send_count < 3:
            self._send_count += 1
            self.send_to('127.0.0.1', self._target_port, f'UDP #{self._send_count}')
        else:
            self._timer.stop()

app = QCoreApplication(sys.argv)
print('=== PySide6 UDP 通信示例 ===\\n')
receiver = UdpReceiver(0)
sender = UdpSender()
QTimer.singleShot(100, lambda: sender.start_sending(receiver.port()))
app.exec()
")

  (println "\n=== 完成 ==="))

(-main)
