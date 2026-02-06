;; PySide6 字体示例 (Clojure + libpython-clj)
;; 注意：QFontDatabase 需要 QGuiApplication，这里仅演示基础字体属性

(ns qt6_tutorials.ch02.gui.fonts)

(require '[libpython-clj2.python :as py]
         '[libpython-clj2.require :refer [require-python]])

(py/initialize!)

(require-python :from "02_gui/03_fonts"
                '[embedded :as py-embedded :bind-ns :reload])

(defn demonstrate-font-properties
  "字体属性"
  []
  (println "\n=== 字体属性 ===")

  ;; 使用 Python 代码演示
  (py/call-attr py-embedded "run_block_1")

  (println "字体属性演示完成"))

(defn demonstrate-font-weights
  "字体字重"
  []
  (println "\n=== 字体字重 ===")

  (py/call-attr py-embedded "run_block_2")

  (println "字体字重演示完成"))

(defn demonstrate-font-styles
  "字体样式"
  []
  (println "\n=== 字体样式 ===")

  (py/call-attr py-embedded "run_block_3")

  (println "字体样式演示完成"))

(defn -main
  [& args]
  (println "=== PySide6 字体示例 (Clojure) ===")

  (demonstrate-font-properties)
  (demonstrate-font-weights)
  (demonstrate-font-styles)

  (println "\n=== 字体要点 ===")
  (println "1. QFont: 字体类")
  (println "2. 属性: family, pointSize, bold, italic")
  (println "3. 字重: Thin, Normal, Bold, Black")
  (println "4. Hinting: 字体渲染提示策略")
  (println "5. QFontDatabase 需要 QGuiApplication（GUI 模式）")

  (println "\n=== 完成 ==="))
