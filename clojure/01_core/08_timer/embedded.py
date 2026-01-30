def run_block_1():
    exec(r"""
from PySide6.QtCore import QCoreApplication
import sys
if not QCoreApplication.instance():
    _app = QCoreApplication(sys.argv)
""", globals())

def run_block_2():
    exec(r"""
from PySide6.QtCore import QTimer

def callback():
    print('单次定时器触发!')

QTimer.singleShot(100, callback)
""", globals())

def run_block_3():
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

timer = QTimer()
timer.timeout.connect(on_timeout)
timer.start(100)  # 每100ms触发
""", globals())

def run_block_4():
    exec(r"""
from PySide6.QtCore import QTimer

values = []

def collect_value():
    values.append(len(values))
    print(f'收集值: {len(values) - 1}')

timer = QTimer()
timer.timeout.connect(collect_value)
timer.start(50)

# 300ms后停止
QTimer.singleShot(350, timer.stop)
""", globals())

def run_block_5():
    exec(r"""
from PySide6.QtCore import QElapsedTimer, QCoreApplication
import time

timer = QElapsedTimer()
timer.start()

# 模拟工作
time.sleep(0.1)  # 100ms

elapsed = timer.elapsed()
print(f'经过时间: {elapsed}ms')

timer.restart()
time.sleep(0.05)  # 50ms
print(f'重启后经过: {timer.elapsed()}ms')
""", globals())
