#!/usr/bin/env clojure -M
;; PySide6 事件循环示例 (Clojure + libpython-clj)

(require '[libpython-clj2.python :as py])

(py/initialize!)

;; 导入模块
(def QtCore (py/import-module "PySide6.QtCore"))

;; 获取类
(def QCoreApplication (py/get-attr QtCore "QCoreApplication"))
(def QEventLoop (py/get-attr QtCore "QEventLoop"))
(def QTimer (py/get-attr QtCore "QTimer"))
(def QThread (py/get-attr QtCore "QThread"))

(defn demonstrate-timer-events
  "定时器事件"
  []
  (println "\n=== 定时器事件 ===")
  
  ;; 初始化 QCoreApplication
  (py/run-simple-string "
from PySide6.QtCore import QCoreApplication, QTimer
import sys
if not QCoreApplication.instance():
    _app = QCoreApplication(sys.argv)
")
  
  (let [counter (atom 0)]
    ;; 创建单次定时器
    (py/run-simple-string "
from PySide6.QtCore import QTimer, QCoreApplication

def delayed_task():
    print('延迟任务执行!')
    QCoreApplication.quit()

# 2秒后执行
timer = QTimer()
timer.singleShot(100, delayed_task)
")
    
    (println "定时器已启动，100ms后执行...")
    ;; 事件循环将在定时器回调中退出
    (let [module (py/add-module "__main__")
          timer (py/get-item (py/module-dict module) "timer")]
      ;; 等待一下让定时器有机会执行
      (Thread/sleep 200))))

(defn demonstrate-custom-events
  "自定义事件"
  []
  (println "\n=== 自定义事件 ===")
  
  ;; 创建自定义事件类
  (py/run-simple-string "
from PySide6.QtCore import QObject, QEvent, QCoreApplication

class CustomEvent(QEvent):
    EVENT_TYPE = QEvent.Type(QEvent.User + 1)
    
    def __init__(self, data):
        super().__init__(self.EVENT_TYPE)
        self.data = data

class EventReceiver(QObject):
    def event(self, event):
        if event.type() == CustomEvent.EVENT_TYPE:
            print(f'收到自定义事件: {event.data}')
            return True
        return super().event(event)

# 创建接收器
receiver = EventReceiver()

# 发送自定义事件
event = CustomEvent('Hello from Clojure!')
QCoreApplication.postEvent(receiver, event)
")
  
  (println "自定义事件已发送"))

(defn demonstrate-signal-slot-events
  "信号槽事件处理"
  []
  (println "\n=== 信号槽事件处理 ===")
  
  (py/run-simple-string "
from PySide6.QtCore import QObject, Signal, QCoreApplication, QTimer

class EventEmitter(QObject):
    eventOccurred = Signal(str)
    
    def trigger_event(self, data):
        self.eventOccurred.emit(data)

emitter = EventEmitter()

# 连接槽
def on_event(data):
    print(f'事件处理: {data}')

emitter.eventOccurred.connect(on_event)

# 触发多个事件
emitter.trigger_event('事件 1')
emitter.trigger_event('事件 2')
emitter.trigger_event('事件 3')
")
  
  (println "信号槽事件处理完成"))

(defn -main
  [& args]
  (println "=== PySide6 事件循环示例 (Clojure) ===")
  
  (demonstrate-timer-events)
  (demonstrate-custom-events)
  (demonstrate-signal-slot-events)
  
  (println "\n=== 完成 ==="))

(-main)
