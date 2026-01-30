def run_block_1():
    exec(r"""
from PySide6.QtCore import QCoreApplication, QTimer
import sys
if not QCoreApplication.instance():
    _app = QCoreApplication(sys.argv)
""", globals())

def run_block_2():
    exec(r"""
from PySide6.QtCore import QTimer, QCoreApplication

def delayed_task():
    print('延迟任务执行!')
    QCoreApplication.quit()

# 2秒后执行
timer = QTimer()
timer.singleShot(100, delayed_task)
""", globals())

def run_block_3():
    exec(r"""
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
""", globals())

def run_block_4():
    exec(r"""
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
""", globals())
