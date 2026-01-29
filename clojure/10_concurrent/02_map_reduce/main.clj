#!/usr/bin/env clojure -M
;; QtConcurrent::mappedReduced demo - Clojure version
;;
;; This example demonstrates the map-reduce pattern:
;; 1. Map: Apply a function to each element in a collection
;; 2. Reduce: Combine the results into a single value

(require '[libpython-clj2.python :as py])

(py/initialize!)

;; 初始化 QCoreApplication
(py/run-simple-string "
from PySide6.QtCore import QCoreApplication
import sys
if not QCoreApplication.instance():
    _app = QCoreApplication(sys.argv)
")

(defn -main
  [& args]
  (println "Map-Reduce demo")
  
  ;; 使用 ThreadPoolExecutor 替代 QtConcurrent::mappedReduced
  (py/run-simple-string "
from concurrent.futures import ThreadPoolExecutor

def square(value):
    return value * value

numbers = list(range(1, 11))

with ThreadPoolExecutor() as executor:
    # Map phase
    mapped_results = list(executor.map(square, numbers))
    # Reduce phase
    result = sum(mapped_results)

print(f'Sum of squares: {result}')
")
  
  (println "Done"))

(-main)
