#!/usr/bin/env clojure -M
;; PySide6 基础控件示例 (Clojure + libpython-clj)
;; 注意：macOS 需要使用 -XstartOnFirstThread JVM 参数运行

(require '[libpython-clj2.python :as py]
         '[libpython-clj2.require :refer [require-python]])

(py/initialize!)

(require-python :from "03_widgets/01_basic_widgets"
                '[embedded :as py-embedded :bind-ns :reload])

(defn demonstrate-widgets
  "演示基础控件"
  []
  (println "\n=== 创建 GUI 窗口演示 ===")

  (py/call-attr py-embedded "run_block_1")

  (println "\n演示完成"))

(defn -main
  [& args]
  (println "=== PySide6 基础控件示例 (Clojure) ===")
  (println "注意: macOS 必须使用 -XstartOnFirstThread JVM 参数")
  (println "      可通过 clojure -M:run 运行")

  (demonstrate-widgets)

  (println "\n=== 完成 ==="))

(-main)
