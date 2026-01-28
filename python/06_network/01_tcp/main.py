#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PySide6 TCP 通信示例

主要类：
- QTcpServer: TCP 服务器
- QTcpSocket: TCP 客户端/连接

异步模式 (推荐):
- 使用信号槽处理连接和数据
- readyRead 信号表示有数据可读
- connected/disconnected 信号

官方文档: https://doc.qt.io/qtforpython/PySide6/QtNetwork/QTcpSocket.html
"""

import sys
from PySide6.QtCore import QObject, Signal, Slot, QTimer, QCoreApplication
from PySide6.QtNetwork import QTcpServer, QTcpSocket, QHostAddress, QAbstractSocket


class EchoServer(QObject):
    """简单的 Echo 服务器"""
    
    def __init__(self, port, parent=None):
        super().__init__(parent)
        self._server = QTcpServer(self)
        
        self._server.newConnection.connect(self._on_new_connection)
        
        if self._server.listen(QHostAddress.LocalHost, port):
            print(f"[服务器] 监听端口: {self._server.serverPort()}")
        else:
            print(f"[服务器] 监听失败: {self._server.errorString()}")
    
    def port(self):
        return self._server.serverPort()
    
    @Slot()
    def _on_new_connection(self):
        client = self._server.nextPendingConnection()
        print(f"[服务器] 新连接来自: {client.peerAddress().toString()}:{client.peerPort()}")
        
        def on_ready_read():
            data = client.readAll()
            print(f"[服务器] 收到: {data.data()}")
            # Echo 回去
            client.write(b"Echo: " + data)
        
        def on_disconnected():
            print("[服务器] 客户端断开")
            client.deleteLater()
        
        client.readyRead.connect(on_ready_read)
        client.disconnected.connect(on_disconnected)


class TcpClient(QObject):
    """TCP 客户端"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._socket = QTcpSocket(self)
        self._message_count = 0
        
        self._socket.connected.connect(self._on_connected)
        self._socket.disconnected.connect(self._on_disconnected)
        self._socket.readyRead.connect(self._on_ready_read)
        self._socket.errorOccurred.connect(self._on_error)
    
    def connect_to_server(self, host, port):
        print(f"[客户端] 连接到 {host}:{port}")
        self._socket.connectToHost(host, port)
    
    def send_message(self, message):
        if self._socket.state() == QAbstractSocket.ConnectedState:
            print(f"[客户端] 发送: {message}")
            self._socket.write(message.encode())
    
    @Slot()
    def _on_connected(self):
        print("[客户端] 已连接到服务器")
        
        # 发送测试消息
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._send_next_message)
        self._timer.start(500)
    
    def _send_next_message(self):
        if self._message_count < 3:
            self._message_count += 1
            self.send_message(f"消息 #{self._message_count}")
        else:
            self._timer.stop()
            self._socket.disconnectFromHost()
    
    @Slot()
    def _on_disconnected(self):
        print("[客户端] 已断开连接")
        QCoreApplication.quit()
    
    @Slot()
    def _on_ready_read(self):
        data = self._socket.readAll()
        print(f"[客户端] 收到: {data.data()}")
    
    @Slot(QAbstractSocket.SocketError)
    def _on_error(self, error):
        print(f"[客户端] 错误: {error} {self._socket.errorString()}")


def main():
    app = QCoreApplication(sys.argv)
    
    print("=== PySide6 TCP 通信示例 ===\n")
    
    # 创建服务器
    server = EchoServer(0)  # 0 = 自动选择端口
    port = server.port()
    
    # 创建客户端并连接
    client = TcpClient()
    QTimer.singleShot(100, lambda: client.connect_to_server("127.0.0.1", port))
    
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
