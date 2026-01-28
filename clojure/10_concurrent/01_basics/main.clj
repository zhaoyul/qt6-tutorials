#!/usr/bin/env clojure -M
;; PySide6 并发编程示例 (Clojure + libpython-clj)

(require '[libpython-clj2.python :as py])

(py/initialize!)

;; 导入模块
(def QtCore (py/import-module "PySide6.QtCore"))

;; 获取类
(def QThreadPool (py/get-attr QtCore "QThreadPool"))
(def QRunnable (py/get-attr QtCore "QRunnable"))
(def QThread (py/get-attr QtCore "QThread"))
(def QTimer (py/get-attr QtCore "QTimer"))
(def QCoreApplication (py/get-attr QtCore "QCoreApplication"))

;; 初始化 QCoreApplication
(py/run-simple-string "
from PySide6.QtCore import QCoreApplication
import sys
if not QCoreApplication.instance():
    _app = QCoreApplication(sys.argv)
")

(defn demonstrate-threadpool-info
  "线程池信息"
  []
  (println "\n=== QThreadPool 信息 ===")
  (let [pool (py/call-attr QThreadPool "globalInstance")]
    (println (str "最大线程数: " (py/call-attr pool "maxThreadCount")))
    (println (str "活跃线程数: " (py/call-attr pool "activeThreadCount")))
    (println (str "过期时间: " (py/call-attr pool "expiryTimeout") " ms"))))

(defn demonstrate-runnable-tasks
  "Runnable 任务"
  []
  (println "\n=== Runnable 任务 ===")
  
  (py/run-simple-string "
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
")
  
  (println "Runnable 任务演示完成"))

(defn demonstrate-concurrent-futures
  "使用 Python concurrent.futures"
  []
  (println "\n=== concurrent.futures (Python) ===")
  
  (py/run-simple-string "
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
")
  
  (println "concurrent.futures 演示完成"))

(defn demonstrate-map-reduce
  "Map-Reduce 模式"
  []
  (println "\n=== Map-Reduce 模式 ===")
  
  (py/run-simple-string "
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
")
  
  (println "Map-Reduce 演示完成"))

(defn demonstrate-asyncio
  "Python asyncio 对比"
  []
  (println "\n=== asyncio (Python 异步IO) ===")
  
  (py/run-simple-string "
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
")
  
  (println "asyncio 演示完成"))

(defn -main
  [& args]
  (println "=== PySide6 并发编程示例 (Clojure) ===")
  
  (demonstrate-threadpool-info)
  (demonstrate-runnable-tasks)
  (demonstrate-concurrent-futures)
  (demonstrate-map-reduce)
  (demonstrate-asyncio)
  
  (println "\n=== 并发要点 ===")
  (println "1. QThreadPool: Qt 原生线程池")
  (println "2. QRunnable: 轻量级任务")
  (println "3. ThreadPoolExecutor: Python 线程池")
  (println "4. asyncio: Python 原生异步IO")
  (println "5. Map-Reduce: 数据并行处理")
  
  (println "\n=== 完成 ==="))

(-main)
