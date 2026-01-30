def run_block_1():
    exec(r"""
from PySide6.QtCore import QThread, Signal
import time

class WorkerThread(QThread):
    progress = Signal(int)
    resultReady = Signal(str)
    
    def __init__(self, name, parent=None):
        super().__init__(parent)
        self._name = name
        self._abort = False
    
    def run(self):
        print(f'{self._name} 开始工作')
        for i in range(1, 6):
            if self._abort:
                break
            self.msleep(100)
            self.progress.emit(i * 20)
        self.resultReady.emit(f'{self._name} 完成')
        print(f'{self._name} 工作完成')
""", globals())

def run_block_2():
    exec(r"""
from PySide6.QtCore import QRunnable, QThread

class Task(QRunnable):
    def __init__(self, task_id):
        super().__init__()
        self._id = task_id
    
    def run(self):
        import threading
        print(f'Task {self._id} 运行在线程: {threading.current_thread().ident}')
        QThread.msleep(50)
        print(f'Task {self._id} 完成')
""", globals())

def run_block_3():
    exec(r"""
from PySide6.QtCore import QCoreApplication
import sys
if not QCoreApplication.instance():
    _app = QCoreApplication(sys.argv)
""", globals())
