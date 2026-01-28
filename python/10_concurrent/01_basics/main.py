#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PySide6 Concurrent 并发编程示例

注意：QtConcurrent 模块在 PySide6 中支持有限。
这个示例展示了 Python 中对应的并发实现方式：

- concurrent.futures.ThreadPoolExecutor: 线程池
- concurrent.futures.ProcessPoolExecutor: 进程池
- asyncio: 异步IO
- multiprocessing: 多进程

对比：
- QtConcurrent::run -> ThreadPoolExecutor.submit
- QtConcurrent::map -> ThreadPoolExecutor.map
- QFuture -> Future

官方文档: 
- PySide6: https://doc.qt.io/qtforpython/PySide6/QtCore/QThreadPool.html
- Python: https://docs.python.org/3/library/concurrent.futures.html
"""

import sys
import time
import math



# 模块级别函数（用于多进程）
def _cpu_intensive(n):
    """CPU密集型计算（模块级别，可被pickle）"""
    result = 0
    for i in range(n):
        result += math.sqrt(i)
    return result


import threading
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed
from os import cpu_count
from PySide6.QtCore import (
    QCoreApplication, QThread, QThreadPool, QRunnable, 
    QObject, Signal, Slot, QTimer
)


def heavy_computation(task_id):
    """耗时计算任务"""
    print(f"任务 {task_id} 开始，线程: {threading.current_thread().ident}")
    time.sleep(0.5)  # 模拟耗时操作
    print(f"任务 {task_id} 完成")
    return f"结果-{task_id}"


def square(n):
    """平方计算"""
    time.sleep(0.05)
    return n * n


def is_even(n):
    """判断偶数"""
    return n % 2 == 0


def demonstrate_thread_pool_executor():
    """演示 ThreadPoolExecutor (对应 QtConcurrent::run)"""
    print("\n=== ThreadPoolExecutor (对应 QtConcurrent::run) ===\n")
    print(f"主线程: {threading.current_thread().ident}")
    
    with ThreadPoolExecutor(max_workers=4) as executor:
        # 方式1: 提交单个任务
        future1 = executor.submit(heavy_computation, 1)
        
        # 方式2: 使用 Lambda
        future2 = executor.submit(lambda: (time.sleep(0.3), 42)[1])
        
        # 方式3: 无返回值
        future3 = executor.submit(lambda: print(f"Lambda 运行在线程: {threading.current_thread().ident}"))
        
        # 等待结果
        print("等待结果...")
        result1 = future1.result()
        result2 = future2.result()
        
        print(f"Future1 结果: {result1}")
        print(f"Future2 结果: {result2}")


def demonstrate_map():
    """演示 map (对应 QtConcurrent::map)"""
    print("\n=== ThreadPoolExecutor.map (对应 QtConcurrent::map) ===\n")
    
    numbers = list(range(1, 11))
    print(f"原始数据: {numbers}")
    
    with ThreadPoolExecutor() as executor:
        # map - 并行处理
        results = list(executor.map(square, numbers))
        print(f"平方结果: {results}")


def demonstrate_filter():
    """演示 filter (对应 QtConcurrent::filter)"""
    print("\n=== filter (对应 QtConcurrent::filter) ===\n")
    
    numbers = list(range(1, 11))
    print(f"原始数据: {numbers}")
    
    # 使用线程池并行过滤
    with ThreadPoolExecutor() as executor:
        # 并行计算判断
        futures = {executor.submit(is_even, n): n for n in numbers}
        
        evens = []
        for future in as_completed(futures):
            n = futures[future]
            if future.result():
                evens.append(n)
        
        evens.sort()
        print(f"偶数过滤结果: {evens}")


def demonstrate_map_reduce():
    """演示 Map-Reduce (对应 QtConcurrent::mappedReduced)"""
    print("\n=== Map-Reduce (对应 QtConcurrent::mappedReduced) ===\n")
    
    numbers = list(range(1, 11))
    print(f"原始数据: {numbers}")
    
    with ThreadPoolExecutor() as executor:
        # Map: 并行计算平方
        squared = list(executor.map(square, numbers))
        print(f"平方结果: {squared}")
        
        # Reduce: 求和
        sum_of_squares = sum(squared)
        print(f"平方和: {sum_of_squares}")
        print("(1² + 2² + ... + 10² = 385)")


def demonstrate_qt_thread_pool():
    """演示 QThreadPool (Qt原生)"""
    print("\n=== QThreadPool 信息 (Qt原生) ===\n")
    
    pool = QThreadPool.globalInstance()
    print(f"最大线程数: {pool.maxThreadCount()}")
    print(f"活跃线程数: {pool.activeThreadCount()}")
    print(f"过期时间: {pool.expiryTimeout()} ms")


class WorkerSignals(QObject):
    """Worker信号"""
    finished = Signal(str)
    progress = Signal(int)


class RunnableTask(QRunnable):
    """Qt Runnable任务 (对应 QRunnable)"""
    
    def __init__(self, task_id):
        super().__init__()
        self.task_id = task_id
        self.signals = WorkerSignals()
    
    def run(self):
        """任务执行"""
        print(f"Runnable 任务 {self.task_id} 在线程 {threading.current_thread().ident} 运行")
        time.sleep(0.3)
        self.signals.finished.emit(f"任务 {self.task_id} 完成")


def demonstrate_qt_runnable():
    """演示 Qt QRunnable"""
    print("\n=== Qt QRunnable (线程池任务) ===\n")
    
    pool = QThreadPool.globalInstance()
    
    # 创建并启动任务
    for i in range(3):
        task = RunnableTask(i + 1)
        pool.start(task)
    
    # 等待所有任务完成
    pool.waitForDone()
    print("所有 Runnable 任务完成")


def demonstrate_asyncio():
    """演示 asyncio (Python异步)"""
    print("\n=== asyncio (Python异步IO) ===\n")
    
    import asyncio
    
    async def async_task(name, delay):
        """异步任务"""
        print(f"异步任务 {name} 开始")
        await asyncio.sleep(delay)
        print(f"异步任务 {name} 完成")
        return f"结果-{name}"
    
    async def main():
        # 并发运行多个任务
        tasks = [
            async_task("A", 0.3),
            async_task("B", 0.2),
            async_task("C", 0.1),
        ]
        results = await asyncio.gather(*tasks)
        print(f"所有异步结果: {results}")
    
    # 运行异步事件循环
    asyncio.run(main())


def demonstrate_multiprocessing():
    """演示多进程 (CPU密集型任务)"""
    print("\n=== ProcessPoolExecutor (多进程) ===\n")
    print(f"CPU核心数: {cpu_count()}")
    
    # 使用模块级别函数 _cpu_intensive
    
    numbers = [1000000, 2000000, 3000000, 4000000]
    
    # 多进程并行
    start = time.time()
    with ProcessPoolExecutor() as executor:
        results = list(executor.map(_cpu_intensive, numbers))
    elapsed = time.time() - start
    
    print(f"多进程计算结果: {results}")
    print(f"耗时: {elapsed:.2f}s")


def main():
    app = QCoreApplication(sys.argv)
    
    print("=== PySide6 Concurrent 并发编程示例 ===")
    print("\n注意：PySide6中QtConcurrent支持有限")
    print("这个示例展示了Python中的对应实现方式\n")
    
    demonstrate_qt_thread_pool()
    demonstrate_qt_runnable()
    demonstrate_thread_pool_executor()
    demonstrate_map()
    demonstrate_filter()
    demonstrate_map_reduce()
    demonstrate_asyncio()
    demonstrate_multiprocessing()
    
    print("\n=== 要点总结 ===")
    print("1. ThreadPoolExecutor.submit() 对应 QtConcurrent::run()")
    print("2. ThreadPoolExecutor.map() 对应 QtConcurrent::map()")
    print("3. concurrent.futures.Future 对应 QFuture")
    print("4. QThreadPool 是 Qt 原生线程池")
    print("5. asyncio 是 Python 原生异步IO")
    print("6. ProcessPoolExecutor 用于 CPU 密集型任务")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
