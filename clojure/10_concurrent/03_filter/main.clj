#!/usr/bin/env clojure -M
;; QtConcurrent::filter demo - Clojure version
;;
;; This example demonstrates how to filter elements from a collection
;; based on a predicate function.

(require '[libpython-clj2.python :as py]
         '[libpython-clj2.require :refer [require-python]])

(py/initialize!)

(require-python :from "10_concurrent/03_filter"
                '[embedded :as py-embedded :bind-ns :reload])

;; 初始化 QCoreApplication
(py/call-attr py-embedded "run_block_1")

(defn -main
  [& args]
  (println "Filter demo")

  ;; 使用 ThreadPoolExecutor 替代 QtConcurrent::filtered
  (py/call-attr py-embedded "run_block_2")

  (println "Done"))

(-main)
