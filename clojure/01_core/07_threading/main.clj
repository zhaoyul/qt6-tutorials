#!/usr/bin/env clojure -M
;; PySide6 多线程示例 (Clojure + libpython-clj)

(require '[libpython-clj2.python :as py])

(py/initialize!)

;; 导入模块
(def QtCore (py/import-module "PySide6.QtCore"))

;; 获取类
(def QObject (py/get-attr QtCore "QObject"))
(def QThread (py/get-attr QtCore "QThread"))
(def QThreadPool (py/get-attr QtCore "QThreadPool"))
(def QCoreApplication (py/get-attr QtCore "QCoreApplication"))

(defn demonstrate-qthread-inheritance
  "演示继承 QThread 的方式"
  []
  (println "\n=== QThread 继承方式 ===")
  
  ;; 定义 Worker 类（通过 Python）
  (py/run-simple-string "
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
")
  
  (let [worker-module (py/add-module "__main__")
        worker-class (py/get-item (py/module-dict worker-module) "WorkerThread")
        thread (worker-class "Worker1")]
    
    ;; 连接信号
    (py/call-attr (py/get-attr thread "progress") "connect"
                  (fn [value] (println (str "进度: " value "%"))))
    (py/call-attr (py/get-attr thread "resultReady") "connect"
                  (fn [result] (println (str "结果: " result))))
    
    ;; 启动并等待（使用带超时的 wait）
    (py/call-attr thread "start")
    (py/call-attr thread "wait" 2000)))  ;; 最多等待 2 秒

(defn demonstrate-threadpool
  "QThreadPool 使用"
  []
  (println "\n=== QThreadPool 方式 ===")
  
  (py/run-simple-string "
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
")
  
  (let [module (py/add-module "__main__")
        task-class (py/get-item (py/module-dict module) "Task")
        pool (py/call-attr QThreadPool "globalInstance")]
    
    (println (str "最大线程数: " (py/call-attr pool "maxThreadCount")))
    
    ;; 提交任务
    (doseq [i (range 1 6)]
      (py/call-attr pool "start" (task-class i)))
    
    ;; 等待完成（带超时）
    (py/call-attr pool "waitForDone" 3000)  ;; 最多等待 3 秒
    (println "所有任务完成")))

(defn -main
  [& args]
  (println "=== PySide6 多线程示例 (Clojure) ===")
  
  ;; 初始化 QCoreApplication
  (py/run-simple-string "
from PySide6.QtCore import QCoreApplication
import sys
if not QCoreApplication.instance():
    _app = QCoreApplication(sys.argv)
")
  
  (demonstrate-qthread-inheritance)
  (demonstrate-threadpool)
  
  (println "\n=== 线程最佳实践 ===")
  (println "1. 避免继承 QThread, 使用 moveToThread")
  (println "2. 使用信号槽跨线程通信")
  (println "3. 简单任务使用 QThreadPool")
  (println "\n=== 完成 ==="))

(-main)
