def run_block_1():
    exec(r"""
from PySide6.QtCore import QCoreApplication
import sys
if not QCoreApplication.instance():
    _app = QCoreApplication(sys.argv)
""", globals())

def run_block_2():
    exec(r"""
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkRequest
from PySide6.QtCore import QUrl, QEventLoop
import json

manager = QNetworkAccessManager()

# 创建请求
url = QUrl('https://httpbin.org/get')
request = QNetworkRequest(url)

# 发送 GET 请求
reply = manager.get(request)

# 等待完成
loop = QEventLoop()
reply.finished.connect(loop.quit)
loop.exec()

# 读取响应
if reply.error() == QNetworkReply.NoError:
    data = reply.readAll().data()
    print(f'响应数据: {data[:200]}...')
else:
    print(f'请求失败: {reply.errorString()}')
""", globals())

def run_block_3():
    exec(r"""
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkRequest
from PySide6.QtCore import QUrl, QEventLoop

manager = QNetworkAccessManager()

# 创建请求
url = QUrl('https://httpbin.org/post')
request = QNetworkRequest(url)
request.setHeader(QNetworkRequest.ContentTypeHeader, 'application/json')

# POST 数据
data = b'{"name": "Clojure", "version": 6}'

# 发送 POST 请求
reply = manager.post(request, data)

# 等待完成
loop = QEventLoop()
reply.finished.connect(loop.quit)
loop.exec()

if reply.error() == QNetworkReply.NoError:
    print('POST 请求成功')
else:
    print(f'POST 失败: {reply.errorString()}')
""", globals())

def run_block_4():
    exec(r"""
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkRequest
from PySide6.QtCore import QUrl

class HttpClient:
    def __init__(self):
        self.manager = QNetworkAccessManager()
        self.manager.finished.connect(self.on_finished)
    
    def get(self, url):
        request = QNetworkRequest(QUrl(url))
        self.manager.get(request)
    
    def on_finished(self, reply):
        if reply.error() == QNetworkReply.NoError:
            print(f'异步请求成功: {reply.url().toString()[:40]}')
        else:
            print(f'异步请求失败')
        reply.deleteLater()

# 使用
client = HttpClient()
client.get('https://httpbin.org/get')

# 等待响应
from PySide6.QtCore import QTimer
QTimer.singleShot(3000, QCoreApplication.quit)
""", globals())

def run_block_5():
    exec(r"""
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkRequest
from PySide6.QtCore import QUrl

manager = QNetworkAccessManager()
request = QNetworkRequest(QUrl('https://httpbin.org/headers'))

# 设置自定义头
request.setRawHeader(b'X-Custom-Header', b'ClojureValue')
request.setRawHeader(b'Authorization', b'Bearer token123')

reply = manager.get(request)

# 等待
from PySide6.QtCore import QEventLoop
loop = QEventLoop()
reply.finished.connect(loop.quit)
loop.exec()

if reply.error() == QNetworkReply.NoError:
    print('带自定义头的请求成功')
""", globals())
