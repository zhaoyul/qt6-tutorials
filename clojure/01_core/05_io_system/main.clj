#!/usr/bin/env clojure -M
;; PySide6 IO 系统示例 (Clojure + libpython-clj)

(require '[libpython-clj2.python :as py]
         '[libpython-clj2.require :refer [require-python]])

(py/initialize!)

(require-python :from "01_core/05_io_system"
                '[embedded :as py-embedded :bind-ns :reload])

(defn demonstrate-io
  "IO 操作演示"
  []
  (println "\n=== PySide6 IO 系统 ===")

  ;; 使用 Python 代码演示
  (py/call-attr py-embedded "run_block_1")

  (println "\nIO 演示完成"))

(defn -main
  [& args]
  (println "=== PySide6 IO 系统示例 (Clojure) ===")

  (demonstrate-io)

  (println "\n=== 完成 ==="))

(-main)
