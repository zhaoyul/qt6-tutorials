def run_block_1():
    exec(r"""
from PySide6.QtCore import QCoreApplication
import sys
if not QCoreApplication.instance():
    _app = QCoreApplication(sys.argv)
""", globals())

def run_block_2():
    exec(r"""
from PySide6.QtCore import QRunnable, QThreadPool, QThread
import threading

class Task(QRunnable):
    def __init__(self, task_id):
        super().__init__()
        self.task_id = task_id
    
    def run(self):
        thread_id = threading.current_thread().ident
        print(f'任务 {self.task_id} 在线程 {thread_id}')
        QThread.msleep(100)
        print(f'任务 {self.task_id} 完成')

# 提交任务
pool = QThreadPool.globalInstance()
for i in range(5):
    pool.start(Task(i))

# 等待完成
pool.waitForDone()
print('所有 Runnable 任务完成')
""", globals())

def run_block_3():
    exec(r"""
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

def compute_square(n):
    time.sleep(0.1)
    return n * n

# 线程池执行
with ThreadPoolExecutor(max_workers=4) as executor:
    # 提交多个任务
    futures = [executor.submit(compute_square, i) for i in range(1, 6)]
    
    # 获取结果
    for future in as_completed(futures):
        result = future.result()
        print(f'结果: {result}')

print('所有计算完成')
""", globals())

def run_block_4():
    exec(r"""
from concurrent.futures import ThreadPoolExecutor
import time

def map_function(x):
    time.sleep(0.05)
    return x * x

def reduce_function(results):
    return sum(results)

# 数据
data = list(range(1, 11))

# Map 阶段
with ThreadPoolExecutor(max_workers=4) as executor:
    mapped = list(executor.map(map_function, data))
    print(f'Map 结果: {mapped}')

# Reduce 阶段
result = reduce_function(mapped)
print(f'Reduce 结果 (平方和): {result}')
""", globals())

def run_block_5():
    exec(r"""
import asyncio

async def async_task(name, delay):
    print(f'任务 {name} 开始')
    await asyncio.sleep(delay)
    print(f'任务 {name} 完成')
    return f'结果-{name}'

async def main():
    # 并发执行多个任务
    tasks = [
        async_task('A', 0.1),
        async_task('B', 0.2),
        async_task('C', 0.15)
    ]
    results = await asyncio.gather(*tasks)
    print(f'所有结果: {results}')

asyncio.run(main())
""", globals())
