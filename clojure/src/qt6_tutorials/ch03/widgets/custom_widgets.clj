;; PySide6 自定义控件示例 (Clojure + libpython-clj)
;; 展示了三种自定义控件:
;; 1. 圆形进度条 (重写 paintEvent)
;; 2. 开关按钮 (带动画)
;; 3. 星级评分 (鼠标交互)
;; 注意：macOS 需要使用 -XstartOnFirstThread JVM 参数运行

(ns qt6_tutorials.ch03.widgets.custom_widgets)

(require '[libpython-clj2.python :as py]
         '[libpython-clj2.require :refer [require-python]])

(py/initialize!)

(require-python :from "03_widgets/07_custom_widgets"
                '[embedded :as py-embedded :bind-ns :reload])

(defn demonstrate-custom-widgets
  "演示自定义控件"
  []
  (println "\n=== 创建自定义控件 GUI 窗口 ===")

  (py/call-attr py-embedded "run_block_1")

  (println "\n演示完成"))

(defn -main
  [& args]
  (println "=== PySide6 自定义控件示例 (Clojure) ===")
  (println "注意: macOS 必须使用 -XstartOnFirstThread JVM 参数")
  (println "      可通过 clj -M:ch03-widgets-custom-widgets 运行")

  (demonstrate-custom-widgets)

  (println "\n=== 完成 ==="))
