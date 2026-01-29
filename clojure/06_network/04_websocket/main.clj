#!/usr/bin/env clojure -M
;; PySide6 WebSocket 客户端示例 (Clojure + libpython-clj)

(require '[libpython-clj2.python :as py])

(py/initialize!)

(defn- create-websocket-client
  "创建 WebSocket 客户端"
  []
  (py/run-simple-string "
from PySide6.QtCore import QUrl, QTimer, QCoreApplication
from PySide6.QtWebSockets import QWebSocket
from PySide6.QtNetwork import QAbstractSocket

class WebSocketClient:
    def __init__(self):
        self.socket = QWebSocket()
        self.message_count = 0
        self.timer = None
        
        # 连接信号
        self.socket.connected.connect(self.on_connected)
        self.socket.disconnected.connect(self.on_disconnected)
        self.socket.textMessageReceived.connect(self.on_text_message)
        self.socket.errorOccurred.connect(self.on_error)
        self.socket.stateChanged.connect(self.on_state_changed)
        self.socket.sslErrors.connect(self.on_ssl_errors)
    
    def connect_to_server(self, url):
        self.url = url
        print(f'[WebSocket] 正在连接到: {url.toString()}')
        self.socket.open(url)
    
    def send_message(self, message):
        if self.socket.state() == QAbstractSocket.ConnectedState:
            print(f'[WebSocket] 发送: {message}')
            self.socket.sendTextMessage(message)
        else:
            print('[WebSocket] 无法发送，未连接')
    
    def close(self):
        print('[WebSocket] 正在关闭连接...')
        self.socket.close()
    
    def on_connected(self):
        print('[WebSocket] 连接成功!')
        peer = self.socket.peerAddress()
        port = self.socket.peerPort()
        print(f'[WebSocket] 服务器地址: {peer.toString()}:{port}')
        
        # 发送第一条消息
        self.message_count += 1
        self.send_message(f'Hello WebSocket! Message #{self.message_count}')
        
        # 设置定时器发送更多消息
        self.timer = QTimer()
        self.timer.timeout.connect(self.send_periodic_message)
        self.timer.start(1500)
    
    def send_periodic_message(self):
        if self.message_count < 3:
            self.message_count += 1
            self.send_message(f'Test message #{self.message_count} from Clojure WebSocket client')
        else:
            self.timer.stop()
            QTimer.singleShot(1000, self.close)
    
    def on_disconnected(self):
        print('[WebSocket] 连接已断开')
        print(f'[WebSocket] 关闭原因: {self.socket.closeCode()} - {self.socket.closeReason()}')
        QCoreApplication.quit()
    
    def on_text_message(self, message):
        print(f'[WebSocket] 收到消息: {message}')
    
    def on_error(self, error):
        print(f'[WebSocket] 错误发生: {error} - {self.socket.errorString()}')
    
    def on_state_changed(self, state):
        state_names = {
            QAbstractSocket.UnconnectedState: '未连接',
            QAbstractSocket.HostLookupState: '查找主机',
            QAbstractSocket.ConnectingState: '正在连接',
            QAbstractSocket.ConnectedState: '已连接',
            QAbstractSocket.BoundState: '已绑定',
            QAbstractSocket.ListeningState: '监听中',
            QAbstractSocket.ClosingState: '正在关闭'
        }
        print(f'[WebSocket] 状态变化: {state_names.get(state, \"未知状态\")}')
    
    def on_ssl_errors(self, errors):
        print('[WebSocket] SSL 错误 (忽略并继续):')
        for error in errors:
            print(f'  - {error.errorString()}')
        self.socket.ignoreSslErrors()

# 创建客户端实例
client = WebSocketClient()
")
  
  (py/run-simple-string "client"))

(defn- get-client
  "获取 Python 客户端对象"
  []
  (py/run-simple-string "client"))

(defn -main
  [& args]
  (println "=== PySide6 WebSocket 客户端示例 (Clojure) ===\n")
  
  ;; 创建客户端
  (create-websocket-client)
  
  ;; 获取服务器 URL
  (let [server-url (if (seq args)
                     (first args)
                     "wss://echo.websocket.org/")]
    
    (println (str "使用服务器: " server-url))
    (println "可以通过命令行参数指定其他服务器，例如:")
    (println "  clojure -M:run 06_network/04_websocket/main.clj ws://localhost:8080\n")
    
    ;; 设置服务器 URL 并连接
    (py/run-simple-string (str "
from PySide6.QtCore import QUrl, QTimer

server_url = QUrl('" server-url "')

# 延迟连接，让事件循环先启动
QTimer.singleShot(100, lambda: client.connect_to_server(server_url))

# 超时处理 (30秒)
QTimer.singleShot(30000, lambda: (
    print('\\n[WebSocket] 超时，关闭连接...'),
    client.close()
))
"))
    
    ;; 启动事件循环
    (py/run-simple-string "
from PySide6.QtCore import QCoreApplication
import sys

app = QCoreApplication.instance() or QCoreApplication(sys.argv)
app.exec()
")))

(-main)
