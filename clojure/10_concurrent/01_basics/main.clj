#!/usr/bin/env clojure -M
;; PySide6 并发编程示例 (Clojure + libpython-clj)

(require '[libpython-clj2.python :as py]
         '[libpython-clj2.require :refer [require-python]])

(py/initialize!)

;; 导入模块
(require-python '[PySide6.QtCore :as QtCore :bind-ns])
(require-python :from "10_concurrent/01_basics"
                '[embedded :as py-embedded :bind-ns :reload])

;; 获取类
(def QThreadPool (py/get-attr QtCore "QThreadPool"))
(def QRunnable (py/get-attr QtCore "QRunnable"))
(def QThread (py/get-attr QtCore "QThread"))
(def QTimer (py/get-attr QtCore "QTimer"))
(def QCoreApplication (py/get-attr QtCore "QCoreApplication"))

;; 初始化 QCoreApplication
(py/call-attr py-embedded "run_block_1")

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
  
  (py/call-attr py-embedded "run_block_2")
  
  (println "Runnable 任务演示完成"))

(defn demonstrate-concurrent-futures
  "使用 Python concurrent.futures"
  []
  (println "\n=== concurrent.futures (Python) ===")
  
  (py/call-attr py-embedded "run_block_3")
  
  (println "concurrent.futures 演示完成"))

(defn demonstrate-map-reduce
  "Map-Reduce 模式"
  []
  (println "\n=== Map-Reduce 模式 ===")
  
  (py/call-attr py-embedded "run_block_4")
  
  (println "Map-Reduce 演示完成"))

(defn demonstrate-asyncio
  "Python asyncio 对比"
  []
  (println "\n=== asyncio (Python 异步IO) ===")
  
  (py/call-attr py-embedded "run_block_5")
  
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
