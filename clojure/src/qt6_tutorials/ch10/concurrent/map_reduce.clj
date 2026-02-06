;; QtConcurrent::mappedReduced demo - Clojure version
;;
;; This example demonstrates the map-reduce pattern:
;; 1. Map: Apply a function to each element in a collection
;; 2. Reduce: Combine the results into a single value

(ns qt6_tutorials.ch10.concurrent.map_reduce)

(require '[libpython-clj2.python :as py]
         '[libpython-clj2.require :refer [require-python]])

(py/initialize!)

(require-python :from "10_concurrent/02_map_reduce"
                '[embedded :as py-embedded :bind-ns :reload])

;; 初始化 QCoreApplication
(py/call-attr py-embedded "run_block_1")

(defn -main
  [& args]
  (println "Map-Reduce demo")

  ;; 使用 ThreadPoolExecutor 替代 QtConcurrent::mappedReduced
  (py/call-attr py-embedded "run_block_2")

  (println "Done"))
