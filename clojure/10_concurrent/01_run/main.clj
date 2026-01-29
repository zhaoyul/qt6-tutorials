#!/usr/bin/env clojure -M
;; QtConcurrent::run demo - Clojure version
;;
;; This example demonstrates how to run a function asynchronously
;; in a separate thread using Python's ThreadPoolExecutor.

(require '[libpython-clj2.python :as py])

(py/initialize!)

;; 初始化 QCoreApplication
(py/run-simple-string "
from PySide6.QtCore import QCoreApplication
import sys
if not QCoreApplication.instance():
    _app = QCoreApplication(sys.argv)
")

(defn heavy-computation
  "耗时计算：模拟耗时操作并返回结果"
  [value]
  (py/run-simple-string (str "
import time
result = " value " * 2
time.sleep(0.2)
"))
  (* value 2))

(defn -main
  [& args]
  (println "Running task...")
  
  ;; 使用 ThreadPoolExecutor 替代 QtConcurrent::run
  (py/run-simple-string "
from concurrent.futures import ThreadPoolExecutor
import time

def heavy_computation(value):
    time.sleep(0.2)
    return value * 2

with ThreadPoolExecutor(max_workers=1) as executor:
    future = executor.submit(heavy_computation, 21)
    result = future.result()
    print(f'Result: {result}')
")
  
  (println "Done"))

(-main)
