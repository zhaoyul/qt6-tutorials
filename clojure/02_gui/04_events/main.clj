#!/usr/bin/env clojure -M
;; PySide6 GUI 事件系统示例 (Clojure + libpython-clj)
;; 注意：macOS GUI 必须在主线程运行，这里使用 QtCore 演示事件机制

(require '[libpython-clj2.python :as py])

(py/initialize!)

;; 导入模块
(def QtCore (py/import-module "PySide6.QtCore"))

;; 获取类
(def QObject (py/get-attr QtCore "QObject"))
(def QCoreApplication (py/get-attr QtCore "QCoreApplication"))
(def QEvent (py/get-attr QtCore "QEvent"))
(def QTimer (py/get-attr QtCore "QTimer"))

;; 初始化 QCoreApplication
(py/run-simple-string "
from PySide6.QtCore import QCoreApplication
import sys
if not QCoreApplication.instance():
    _app = QCoreApplication(sys.argv)
")

(defn demonstrate-timer-events
  "定时器事件"
  []
  (println "\n=== 定时器事件 ===")
  
  ;; 使用 Python 代码演示
  (py/run-simple-string "
from PySide6.QtCore import QTimer, QCoreApplication

counter = 0

def on_timeout():
    global counter
    counter += 1
    print(f'定时器触发 #{counter}')
    if counter >= 3:
        timer.stop()
        print('定时器停止')

# 创建定时器
timer = QTimer()
timer.timeout.connect(on_timeout)
timer.start(500)  # 500ms 间隔

print('定时器已启动 (500ms)')
")
  
  ;; 等待定时器执行
  (Thread/sleep 2000)
  (println "定时器演示完成"))

(defn demonstrate-custom-events
  "自定义事件"
  []
  (println "\n=== 自定义事件 ===")
  
  (py/run-simple-string "
from PySide6.QtCore import QObject, QEvent, QCoreApplication

# 定义自定义事件类型
class CustomEvent(QEvent):
    EVENT_TYPE = QEvent.Type(QEvent.User + 1)
    
    def __init__(self, message):
        super().__init__(self.EVENT_TYPE)
        self.message = message

# 事件接收器
class EventReceiver(QObject):
    def event(self, event):
        if event.type() == CustomEvent.EVENT_TYPE:
            print(f'收到自定义事件: {event.message}')
            return True
        return super().event(event)

# 创建接收器并发送事件
receiver = EventReceiver()
event = CustomEvent('Hello from Clojure!')
QCoreApplication.postEvent(receiver, event)

print('自定义事件已发送')
")
  
  (println "自定义事件演示完成"))

(defn demonstrate-signal-events
  "信号作为事件"
  []
  (println "\n=== 信号事件处理 ===")
  
  (py/run-simple-string "
from PySide6.QtCore import QObject, Signal, QTimer

class EventEmitter(QObject):
    eventOccurred = Signal(str)
    
    def trigger(self, data):
        self.eventOccurred.emit(data)

emitter = EventEmitter()

# 连接多个槽
def handler1(data):
    print(f'处理器1: {data}')

def handler2(data):
    print(f'处理器2: {data}')

emitter.eventOccurred.connect(handler1)
emitter.eventOccurred.connect(handler2)

# 触发事件
emitter.trigger('事件 A')
emitter.trigger('事件 B')
")
  
  (println "信号事件演示完成"))

(defn -main
  [& args]
  (println "=== PySide6 事件系统示例 (Clojure) ===")
  
  (demonstrate-timer-events)
  (demonstrate-custom-events)
  (demonstrate-signal-events)
  
  (println "\n=== 事件要点 ===")
  (println "1. QTimer: 定时器事件")
  (println "2. QEvent: 基础事件类")
  (println "3. postEvent: 异步发送事件")
  (println "4. Signal: 信号槽机制")
  
  (println "\n=== 完成 ==="))

(-main)
