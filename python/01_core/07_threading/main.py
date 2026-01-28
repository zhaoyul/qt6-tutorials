#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PySide6 多线程示例

Qt 提供多种多线程方式：
1. QThread: 线程类
2. QRunnable + QThreadPool: 任务池
3. QtConcurrent: 高级并发 (见 10_concurrent)
4. QMutex, QReadWriteLock: 同步原语

重要概念：
- 线程亲和性 (Thread Affinity)
- moveToThread 模式
- 跨线程信号槽

注意：Python有GIL（全局解释器锁）
- 对于CPU密集型任务，考虑使用多进程（multiprocessing）
- 对于I/O密集型任务，多线程仍然有效

官方文档: https://doc.qt.io/qtforpython/PySide6/QtCore/QThread.html
"""

import sys
import time
import threading
from PySide6.QtCore import (
    QCoreApplication,
    QObject,
    QThread,
    QRunnable,
    QThreadPool,
    QMutex,
    QMutexLocker,
    QReadWriteLock,
    QReadLocker,
    QWriteLocker,
    Signal,
    Slot
)


# ============ 方式1: 继承 QThread ============
class WorkerThread(QThread):
    """
    继承QThread的工作线程
    重写run()方法
    """
    
    progress = Signal(int)
    resultReady = Signal(str)
    
    def __init__(self, name: str, parent=None):
        super().__init__(parent)
        self._name = name
        self._abort = False
    
    def abort(self):
        self._abort = True
    
    def run(self):
        """线程执行体"""
        print(f"{self._name} 开始工作，线程ID: {threading.current_thread().ident}")
        
        for i in range(1, 6):
            if self._abort:
                break
            QThread.msleep(100)  # 模拟工作
            self.progress.emit(i * 20)
        
        self.resultReady.emit(f"{self._name} 完成")
        print(f"{self._name} 工作完成")


# ============ 方式2: Worker + moveToThread ============
class Worker(QObject):
    """
    工作对象
    推荐使用moveToThread方式
    """
    
    progress = Signal(str, int)  # task, percent
    finished = Signal(str)       # result
    
    @Slot(str)
    def doWork(self, task: str):
        """执行工作任务"""
        print(f"Worker 执行任务: {task} 线程: {threading.current_thread().ident}")
        
        for i in range(3):
            QThread.msleep(100)
            self.progress.emit(task, (i + 1) * 33)
        
        self.finished.emit(f"{task} 结果")


# ============ 方式3: QRunnable ============
class Task(QRunnable):
    """
    可运行任务
    适合短任务，自动管理内存
    """
    
    def __init__(self, task_id: int):
        super().__init__()
        self._id = task_id
    
    def run(self):
        """任务执行体"""
        print(f"Task {self._id} 运行在线程: {threading.current_thread().ident}")
        QThread.msleep(50)
        print(f"Task {self._id} 完成")


# ============ 互斥锁示例 ============
class Counter:
    """带互斥锁的计数器"""
    
    def __init__(self):
        self._mutex = QMutex()
        self._value = 0
    
    def increment(self):
        """原子增加"""
        with QMutexLocker(self._mutex):  # 使用上下文管理器（类似RAII）
            self._value += 1
    
    def value(self):
        """获取值"""
        with QMutexLocker(self._mutex):
            return self._value


# ============ 读写锁示例 ============
class SharedData:
    """带读写锁的共享数据"""
    
    def __init__(self):
        self._lock = QReadWriteLock()
        self._data = ""
    
    def read(self) -> str:
        """读取数据（允许多读）"""
        with QReadLocker(self._lock):
            return self._data
    
    def write(self, data: str):
        """写入数据（独占写）"""
        with QWriteLocker(self._lock):
            self._data = data


def demonstrate_qthread():
    """QThread 继承方式"""
    print("\n=== QThread 继承方式 ===\n")
    print(f"主线程 ID: {threading.current_thread().ident}")
    
    thread = WorkerThread("Worker1")
    thread.progress.connect(lambda value: print(f"进度: {value}%"))
    thread.resultReady.connect(lambda result: print(f"结果: {result}"))
    
    thread.start()
    thread.wait()  # 等待完成


def demonstrate_move_to_thread():
    """moveToThread 方式（推荐）"""
    print("\n=== moveToThread 方式 (推荐) ===\n")
    
    worker_thread = QThread()
    worker = Worker()
    worker.moveToThread(worker_thread)
    
    # 线程启动时开始工作
    worker_thread.started.connect(lambda: worker.doWork("任务A"))
    
    worker.progress.connect(
        lambda task, p: print(f"{task} 进度: {p}%")
    )
    worker.finished.connect(
        lambda result: print(f"完成: {result}")
    )
    
    # 工作完成时退出线程
    worker.finished.connect(worker_thread.quit)
    
    worker_thread.start()
    
    # 使用本地事件循环等待线程完成，避免阻塞信号处理
    from PySide6.QtCore import QEventLoop
    loop = QEventLoop()
    worker_thread.finished.connect(loop.quit)
    loop.exec()  # 线程结束时退出事件循环


def demonstrate_thread_pool():
    """QThreadPool 方式"""
    print("\n=== QThreadPool 方式 ===\n")
    
    pool = QThreadPool.globalInstance()
    print(f"最大线程数: {pool.maxThreadCount()}")
    
    # 提交任务
    for i in range(1, 6):
        pool.start(Task(i))  # 自动管理内存
    
    # 等待所有任务完成
    pool.waitForDone()
    print("所有任务完成")


def demonstrate_synchronization():
    """同步原语演示"""
    print("\n=== 同步原语 ===\n")
    
    counter = Counter()
    
    # 创建多个线程增加计数
    threads = []
    for i in range(5):
        def worker():
            for _ in range(100):
                counter.increment()
        
        # 使用 WorkThread 替代 QThread.create (兼容性)
        class TempThread(QThread):
            def run(self):
                worker()
        thread = TempThread()
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.wait()
    
    print(f"计数结果 (应为500): {counter.value()}")


def demonstrate_python_threading():
    """Python标准库threading对比"""
    print("\n=== Python threading 对比 ===\n")
    
    import threading
    
    result = []
    
    def worker():
        thread_id = threading.current_thread().ident
        print(f"Python线程 ID: {thread_id}")
        time.sleep(0.1)
        result.append(thread_id)
    
    threads = []
    for i in range(3):
        t = threading.Thread(target=worker, name=f"PythonThread-{i}")
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join()
    
    print(f"所有Python线程完成，结果数: {len(result)}")
    
    print("\n对比总结:")
    print("- PySide6 QThread: 与Qt事件循环集成，跨线程信号槽")
    print("- Python threading: 标准库，更轻量，适合非Qt代码")


def main():
    """主函数"""
    app = QCoreApplication(sys.argv)
    
    print("=== PySide6 多线程示例 ===")
    
    demonstrate_qthread()
    demonstrate_move_to_thread()
    demonstrate_thread_pool()
    demonstrate_synchronization()
    demonstrate_python_threading()
    
    print("\n=== 线程最佳实践 ===")
    print("1. 避免继承 QThread, 使用 moveToThread")
    print("2. 使用信号槽跨线程通信")
    print("3. 使用 QMutexLocker/QReadLocker 自动管理锁")
    print("4. 简单任务使用 QThreadPool")
    print("5. CPU密集型任务考虑Python multiprocessing")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
