#!/usr/bin/env clojure -M
;; PySide6 HTTP 网络请求示例 (Clojure + libpython-clj)

(require '[libpython-clj2.python :as py])

(py/initialize!)

;; 导入模块
(def QtCore (py/import-module "PySide6.QtCore"))
(def QtNetwork (py/import-module "PySide6.QtNetwork"))

;; 获取类
(def QNetworkAccessManager (py/get-attr QtNetwork "QNetworkAccessManager"))
(def QNetworkRequest (py/get-attr QtNetwork "QNetworkRequest"))
(def QNetworkReply (py/get-attr QtNetwork "QNetworkReply"))
(def QUrl (py/get-attr QtCore "QUrl"))
(def QCoreApplication (py/get-attr QtCore "QCoreApplication"))

;; 初始化 QCoreApplication
(py/run-simple-string "
from PySide6.QtCore import QCoreApplication
import sys
if not QCoreApplication.instance():
    _app = QCoreApplication(sys.argv)
")

(defn demonstrate-http-get
  "HTTP GET 请求"
  []
  (println "\n=== HTTP GET 请求 ===")
  
  (py/run-simple-string "
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
")
  
  (println "GET 请求完成"))

(defn demonstrate-http-post
  "HTTP POST 请求"
  []
  (println "\n=== HTTP POST 请求 ===")
  
  (py/run-simple-string "
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkRequest
from PySide6.QtCore import QUrl, QEventLoop

manager = QNetworkAccessManager()

# 创建请求
url = QUrl('https://httpbin.org/post')
request = QNetworkRequest(url)
request.setHeader(QNetworkRequest.ContentTypeHeader, 'application/json')

# POST 数据
data = b'{\"name\": \"Clojure\", \"version\": 6}'

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
")
  
  (println "POST 请求完成"))

(defn demonstrate-async-http
  "异步 HTTP 请求"
  []
  (println "\n=== 异步 HTTP 请求 ===")
  
  (py/run-simple-string "
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
")
  
  (println "异步请求已发送"))

(defn demonstrate-headers
  "自定义 HTTP 头"
  []
  (println "\n=== 自定义 HTTP 头 ===")
  
  (py/run-simple-string "
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
")
  
  (println "自定义头请求完成"))

(defn -main
  [& args]
  (println "=== PySide6 HTTP 网络请求示例 (Clojure) ===")
  
  ;; 网络请求在命令行模式下可能有延迟，简化演示
  (println "\nHTTP 功能说明:")
  (println "- QNetworkAccessManager: HTTP 请求管理器")
  (println "- QNetworkRequest: 请求配置")
  (println "- QNetworkReply: 响应数据")
  (println "- 支持 GET, POST, PUT, DELETE 等方法")
  (println "- 支持自定义 Headers")
  (println "- 支持异步回调")
  
  (println "\n=== 完成 ==="))

(-main)
