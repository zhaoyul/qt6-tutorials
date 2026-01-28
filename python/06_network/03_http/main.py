#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PySide6 HTTP 请求示例

主要类：
- QNetworkAccessManager: 管理网络请求
- QNetworkRequest: 请求配置
- QNetworkReply: 响应

支持的操作：
- GET, POST, PUT, DELETE 等
- HTTPS (SSL/TLS)
- 重定向处理
- Cookie 管理

官方文档: https://doc.qt.io/qtforpython/PySide6/QtNetwork/QNetworkAccessManager.html
"""

import sys
import json
from PySide6.QtCore import QObject, Slot, QTimer, QCoreApplication, QUrl, QUrlQuery
from PySide6.QtNetwork import (
    QNetworkAccessManager, QNetworkRequest, QNetworkReply, QSslError
)


class HttpClient(QObject):
    """HTTP 客户端"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._manager = QNetworkAccessManager(self)
        self._pending_requests = 0
        
        # 处理 SSL 错误 (生产环境应该更严格)
        self._manager.sslErrors.connect(self._on_ssl_errors)
    
    @Slot(QNetworkReply, list)
    def _on_ssl_errors(self, reply, errors):
        print(f"SSL 错误: {errors}")
        reply.ignoreSslErrors()  # 仅用于测试
    
    # GET 请求
    def get(self, url):
        print("\n--- GET 请求 ---")
        print(f"URL: {url.toString()}")
        
        request = QNetworkRequest(url)
        request.setHeader(QNetworkRequest.UserAgentHeader, "PySide6-HTTP-Demo/1.0")
        
        self._pending_requests += 1
        reply = self._manager.get(request)
        reply.finished.connect(lambda: self._handle_reply(reply))
    
    # POST 请求 (JSON)
    def post_json(self, url, data):
        print("\n--- POST JSON 请求 ---")
        print(f"URL: {url.toString()}")
        body = json.dumps(data)
        print(f"Body: {body}")
        
        request = QNetworkRequest(url)
        request.setHeader(QNetworkRequest.ContentTypeHeader, "application/json")
        
        self._pending_requests += 1
        reply = self._manager.post(request, body.encode())
        reply.finished.connect(lambda: self._handle_reply(reply))
    
    # POST 请求 (表单)
    def post_form(self, url, form_data):
        print("\n--- POST Form 请求 ---")
        print(f"URL: {url.toString()}")
        
        request = QNetworkRequest(url)
        request.setHeader(QNetworkRequest.ContentTypeHeader,
                         "application/x-www-form-urlencoded")
        
        data = form_data.toString(QUrl.FullyEncoded).encode()
        
        self._pending_requests += 1
        reply = self._manager.post(request, data)
        reply.finished.connect(lambda: self._handle_reply(reply))
    
    # 带进度的下载
    def download_with_progress(self, url):
        print("\n--- 下载请求 (带进度) ---")
        print(f"URL: {url.toString()}")
        
        request = QNetworkRequest(url)
        
        self._pending_requests += 1
        reply = self._manager.get(request)
        
        def on_progress(received, total):
            if total > 0:
                percent = received * 100 // total
                print(f"下载进度: {received}/{total} ({percent}%)")
        
        reply.downloadProgress.connect(on_progress)
        reply.finished.connect(lambda: self._handle_reply(reply))
    
    def _handle_reply(self, reply):
        print("\n=== 响应 ===")
        
        # 检查错误
        if reply.error() != QNetworkReply.NoError:
            print(f"错误: {reply.errorString()}")
        else:
            # HTTP 状态码
            status_code = reply.attribute(QNetworkRequest.HttpStatusCodeAttribute)
            print(f"状态码: {status_code}")
            
            # 响应头
            content_type = reply.header(QNetworkRequest.ContentTypeHeader)
            print(f"Content-Type: {content_type}")
            
            # 响应体
            data = reply.readAll()
            print(f"响应大小: {len(data)} bytes")
            
            # 尝试解析为 JSON
            try:
                json_data = json.loads(data.data())
                print("JSON 响应:")
                print(json.dumps(json_data, indent=2)[:500])
            except json.JSONDecodeError:
                # 显示原始文本 (截断)
                text = data.data().decode('utf-8', errors='replace')[:200]
                print(f"文本响应: {text}")
        
        reply.deleteLater()
        self._pending_requests -= 1
        
        if self._pending_requests == 0:
            QTimer.singleShot(100, QCoreApplication.quit)


def demonstrate_network_info():
    """网络信息说明"""
    print("=== 网络信息 ===\n")
    print("QNetworkAccessManager 特点:")
    print("- 异步操作，使用信号槽")
    print("- 自动处理重定向")
    print("- 支持 HTTPS")
    print("- 连接池复用")
    print("- Cookie 管理")


def main():
    app = QCoreApplication(sys.argv)
    
    print("=== PySide6 HTTP 请求示例 ===\n")
    
    demonstrate_network_info()
    
    client = HttpClient()
    
    # GET 请求 (使用 httpbin 测试 API)
    client.get(QUrl("https://httpbin.org/get"))
    
    # POST JSON 请求
    client.post_json(QUrl("https://httpbin.org/post"), {
        "name": "PySide6",
        "version": 6
    })
    
    # 注意: 这些请求需要网络连接
    # 如果无法访问外网，请求会失败
    
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
