#!/usr/bin/env clojure -M
;; QtConcurrent::filter demo - Clojure version
;;
;; This example demonstrates how to filter elements from a collection
;; based on a predicate function.

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
  (println "Filter demo")
  
  ;; 使用 ThreadPoolExecutor 替代 QtConcurrent::filtered
  (py/run-simple-string "
from concurrent.futures import ThreadPoolExecutor, as_completed

def is_even(value):
    return value % 2 == 0

numbers = list(range(1, 11))

with ThreadPoolExecutor() as executor:
    futures = {executor.submit(is_even, n): n for n in numbers}
    
    even_numbers = []
    for future in as_completed(futures):
        number = futures[future]
        if future.result():
            even_numbers.append(number)
    
    even_numbers.sort()

print(f'Even numbers: {even_numbers}')
")
  
  (println "Done"))

(-main)
