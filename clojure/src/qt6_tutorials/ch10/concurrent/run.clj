;; QtConcurrent::run demo - Clojure version
;;
;; This example demonstrates how to run a function asynchronously
;; in a separate thread using Python's ThreadPoolExecutor.

(ns qt6_tutorials.ch10.concurrent.run)

(require '[libpython-clj2.python :as py]
         '[libpython-clj2.require :refer [require-python]])

(py/initialize!)

(require-python :from "10_concurrent/01_run"
                '[embedded :as py-embedded :bind-ns :reload])

;; 初始化 QCoreApplication
(py/call-attr py-embedded "run_block_1")

(defn heavy-computation
  "耗时计算：模拟耗时操作并返回结果"
  [value]
  (py/call-attr py-embedded "run_block_3" value)
  (* value 2))

(defn -main
  [& args]
  (println "Running task...")

  ;; 使用 ThreadPoolExecutor 替代 QtConcurrent::run
  (py/call-attr py-embedded "run_block_2")

  (println "Done"))
