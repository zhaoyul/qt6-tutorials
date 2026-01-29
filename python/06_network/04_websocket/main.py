#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PySide6 WebSocket 客户端示例

主要类：
- QWebSocket: WebSocket 客户端

关键信号：
- connected: 连接成功
- disconnected: 连接断开
- textMessageReceived: 收到文本消息
- binaryMessageReceived: 收到二进制消息
- errorOccurred: 发生错误

官方文档: https://doc.qt.io/qtforpython/PySide6/QtWebSockets/QWebSocket.html
"""

import sys
from PySide6.QtCore import QCoreApplication, QUrl, QTimer
from PySide6.QtWebSockets import QWebSocket
from PySide6.QtNetwork import QAbstractSocket


class WebSocketClient:
    """WebSocket 客户端"""

    def __init__(self):
        self.socket = QWebSocket()
        self.message_count = 0

        # 连接信号
        self.socket.connected.connect(self.on_connected)
        self.socket.disconnected.connect(self.on_disconnected)
        self.socket.textMessageReceived.connect(self.on_text_message)
        self.socket.errorOccurred.connect(self.on_error)
        self.socket.stateChanged.connect(self.on_state_changed)
        self.socket.sslErrors.connect(self.on_ssl_errors)

    def connect_to_server(self, url: QUrl):
        """连接到服务器"""
        self.url = url
        print(f"[WebSocket] 正在连接到: {url.toString()}")
        self.socket.open(url)

    def send_message(self, message: str):
        """发送消息"""
        if self.socket.state() == QAbstractSocket.ConnectedState:
            print(f"[WebSocket] 发送: {message}")
            self.socket.sendTextMessage(message)
        else:
            print("[WebSocket] 无法发送，未连接")

    def close(self):
        """关闭连接"""
        print("[WebSocket] 正在关闭连接...")
        self.socket.close()

    def on_connected(self):
        """连接成功回调"""
        print("[WebSocket] 连接成功!")
        peer = self.socket.peerAddress()
        port = self.socket.peerPort()
        print(f"[WebSocket] 服务器地址: {peer.toString()}:{port}")

        # 发送第一条消息
        self.message_count += 1
        self.send_message(f"Hello WebSocket! Message #{self.message_count}")

        # 设置定时器发送更多消息
        self.timer = QTimer()
        self.timer.timeout.connect(self.send_periodic_message)
        self.timer.start(1500)

    def send_periodic_message(self):
        """定期发送消息"""
        if self.message_count < 3:
            self.message_count += 1
            self.send_message(f"Test message #{self.message_count} from PySide6 WebSocket client")
        else:
            self.timer.stop()
            # 延迟关闭连接
            QTimer.singleShot(1000, self.close)

    def on_disconnected(self):
        """连接断开回调"""
        print("[WebSocket] 连接已断开")
        print(f"[WebSocket] 关闭原因: {self.socket.closeCode()} - {self.socket.closeReason()}")
        QCoreApplication.quit()

    def on_text_message(self, message: str):
        """收到文本消息回调"""
        print(f"[WebSocket] 收到消息: {message}")

    def on_error(self, error: QAbstractSocket.SocketError):
        """错误回调"""
        print(f"[WebSocket] 错误发生: {error} - {self.socket.errorString()}")

    def on_state_changed(self, state: QAbstractSocket.SocketState):
        """状态变化回调"""
        state_names = {
            QAbstractSocket.UnconnectedState: "未连接",
            QAbstractSocket.HostLookupState: "查找主机",
            QAbstractSocket.ConnectingState: "正在连接",
            QAbstractSocket.ConnectedState: "已连接",
            QAbstractSocket.BoundState: "已绑定",
            QAbstractSocket.ListeningState: "监听中",
            QAbstractSocket.ClosingState: "正在关闭"
        }
        print(f"[WebSocket] 状态变化: {state_names.get(state, '未知状态')}")

    def on_ssl_errors(self, errors):
        """SSL 错误回调"""
        print("[WebSocket] SSL 错误 (忽略并继续):")
        for error in errors:
            print(f"  - {error.errorString()}")
        # 测试时忽略 SSL 错误
        self.socket.ignoreSslErrors()


def main():
    """主函数"""
    app = QCoreApplication(sys.argv)

    print("=== PySide6 WebSocket 客户端示例 ===\n")

    client = WebSocketClient()

    # 使用 echo.websocket.org 或类似的服务
    server_url = QUrl("wss://echo.websocket.org/")

    # 如果命令行提供了 URL，使用提供的 URL
    if len(sys.argv) > 1:
        server_url = QUrl(sys.argv[1])

    print(f"使用服务器: {server_url.toString()}")
    print("可以通过命令行参数指定其他服务器，例如:")
    print("  python main.py ws://localhost:8080\n")

    # 延迟连接，让事件循环先启动
    QTimer.singleShot(100, lambda: client.connect_to_server(server_url))

    # 超时处理 (30秒)
    QTimer.singleShot(30000, lambda: (
        print("\n[WebSocket] 超时，关闭连接..."),
        client.close()
    ))

    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
