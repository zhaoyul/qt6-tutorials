def run_block_1():
    exec(r"""
from PySide6.QtCore import QCoreApplication
import sys
if not QCoreApplication.instance():
    _app = QCoreApplication(sys.argv)
""", globals())

def run_block_2():
    exec(r"""
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
""", globals())

def run_block_3():
    exec(r"""
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
""", globals())

def run_block_4():
    exec(r"""
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
""", globals())
