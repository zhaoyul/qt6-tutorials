#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PySide6 UDP 通信示例

QUdpSocket 特点：
- 无连接协议
- 数据报 (Datagram) 方式
- 支持广播和组播

主要方法：
- writeDatagram(): 发送数据报
- readDatagram(): 接收数据报
- bind(): 绑定端口接收数据

官方文档: https://doc.qt.io/qtforpython/PySide6/QtNetwork/QUdpSocket.html
"""

import sys
from PySide6.QtCore import QObject, Slot, QTimer, QCoreApplication
from PySide6.QtNetwork import QUdpSocket, QHostAddress, QNetworkDatagram


class UdpReceiver(QObject):
    """UDP 接收端"""
    
    def __init__(self, port, parent=None):
        super().__init__(parent)
        self._socket = QUdpSocket(self)
        self._received_count = 0
        
        if self._socket.bind(QHostAddress.LocalHost, port):
            print(f"[接收端] 绑定端口: {self._socket.localPort()}")
        else:
            print(f"[接收端] 绑定失败: {self._socket.errorString()}")
        
        self._socket.readyRead.connect(self._on_ready_read)
    
    def port(self):
        return self._socket.localPort()
    
    @Slot()
    def _on_ready_read(self):
        while self._socket.hasPendingDatagrams():
            datagram = self._socket.receiveDatagram()
            print(f"[接收端] 收到来自 {datagram.senderAddress().toString()}:"
                  f"{datagram.senderPort()} 的数据: {datagram.data().data()}")
            
            # 回复
            reply = b"ACK: " + datagram.data()
            self._socket.writeDatagram(reply, datagram.senderAddress(), datagram.senderPort())
            
            self._received_count += 1
            if self._received_count >= 3:
                QTimer.singleShot(500, QCoreApplication.quit)


class UdpSender(QObject):
    """UDP 发送端"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._socket = QUdpSocket(self)
        self._send_count = 0
        
        # 绑定以接收回复
        self._socket.bind()
        print(f"[发送端] 绑定端口: {self._socket.localPort()}")
        
        self._socket.readyRead.connect(self._on_ready_read)
    
    @Slot()
    def _on_ready_read(self):
        while self._socket.hasPendingDatagrams():
            datagram = self._socket.receiveDatagram()
            print(f"[发送端] 收到回复: {datagram.data().data()}")
    
    def send_to(self, host, port, data):
        print(f"[发送端] 发送到 {host}:{port} -> {data}")
        self._socket.writeDatagram(data.encode(), QHostAddress(host), port)
    
    def start_sending(self, target_port):
        self._timer = QTimer(self)
        self._target_port = target_port
        self._timer.timeout.connect(self._send_next)
        self._timer.start(300)
    
    def _send_next(self):
        if self._send_count < 3:
            self._send_count += 1
            self.send_to("127.0.0.1", self._target_port, f"UDP消息 #{self._send_count}")
        else:
            self._timer.stop()


def demonstrate_basic_udp():
    """UDP 基本操作说明"""
    print("\n=== UDP 基本操作 ===\n")
    print("UDP 是无连接协议")
    print("可以直接发送数据到任意地址和端口")
    print("数据以数据报形式传输，可能丢失或乱序")


def demonstrate_broadcast():
    """UDP 广播说明"""
    print("\n=== UDP 广播说明 ===\n")
    print("广播地址: QHostAddress.Broadcast (255.255.255.255)")
    print("子网广播: 如 192.168.1.255")
    print("组播地址: 224.0.0.0 - 239.255.255.255")
    print("\n使用 writeDatagram() 发送到广播/组播地址")
    print("使用 joinMulticastGroup() 加入组播组")


def main():
    app = QCoreApplication(sys.argv)
    
    print("=== PySide6 UDP 通信示例 ===")
    
    demonstrate_basic_udp()
    demonstrate_broadcast()
    
    print("\n=== UDP 通信演示 ===\n")
    
    # 创建接收端
    receiver = UdpReceiver(0)  # 自动选择端口
    
    # 创建发送端
    sender = UdpSender()
    
    # 开始发送
    QTimer.singleShot(100, lambda: sender.start_sending(receiver.port()))
    
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
