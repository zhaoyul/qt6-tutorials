;; PySide6 主窗口示例 (Clojure + libpython-clj)
;; 注意：macOS 需要使用 -XstartOnFirstThread JVM 参数运行

(ns qt6_tutorials.ch03.widgets.main_window)

(require '[libpython-clj2.python :as py]
         '[libpython-clj2.require :refer [require-python]])

(py/initialize!)

(require-python :from "03_widgets/04_main_window"
                '[embedded :as py-embedded :bind-ns :reload])

(defn -main
  [& args]
  (println "=== PySide6 主窗口示例 (Clojure) ===")

  (py/call-attr py-embedded "run_block_1")

  (println "\n=== 完成 ==="))
