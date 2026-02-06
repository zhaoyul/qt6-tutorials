;; PySide6 绘制示例 (Clojure + libpython-clj)
;; 注意：macOS GUI 必须在主线程运行，这里使用图像绘制演示

(ns qt6_tutorials.ch02.gui.painting)

(require '[libpython-clj2.python :as py]
         '[libpython-clj2.require :refer [require-python]])

(py/initialize!)

(require-python :from "02_gui/01_painting"
                '[embedded :as py-embedded :bind-ns :reload])

(defn demonstrate-painting
  "QPainter 绘制演示"
  []
  (println "\n=== QPainter 绘制演示 ===")

  ;; 使用 Python 代码创建图像并绘制
  (py/call-attr py-embedded "run_block_1")

  (println "绘制演示完成"))

(defn demonstrate-drawing-primitives
  "绘制基本图形"
  []
  (println "\n=== 绘制基本图形 ===")

  (py/call-attr py-embedded "run_block_2")

  (println "基本图形演示完成"))

(defn -main
  [& args]
  (println "=== PySide6 绘制示例 (Clojure) ===")
  (println "注意: 使用 QImage + QPainter 进行离屏绘制")

  (demonstrate-painting)
  (demonstrate-drawing-primitives)

  (println "\n=== 绘制要点 ===")
  (println "1. QPainter: 2D 绘制类")
  (println "2. QImage: 内存图像（无需 GUI 应用）")
  (println "3. 基本形状: drawRect, drawEllipse, drawArc")
  (println "4. 画笔: QPen (边框), QBrush (填充)")
  (println "5. 颜色: QColor(r, g, b)")

  (println "\n=== 完成 ==="))
