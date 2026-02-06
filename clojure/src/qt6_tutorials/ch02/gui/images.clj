;; PySide6 图像处理示例 (Clojure + libpython-clj)
;; 注意：macOS GUI 必须在主线程运行，这里使用图像文件操作

(ns qt6_tutorials.ch02.gui.images)

(require '[libpython-clj2.python :as py]
         '[libpython-clj2.require :refer [require-python]])

(py/initialize!)

(require-python :from "02_gui/02_images"
                '[embedded :as py-embedded :bind-ns :reload])

(defn demonstrate-image-creation
  "创建图像"
  []
  (println "\n=== QImage 图像创建 ===")

  ;; 使用 Python 代码创建图像
  (py/call-attr py-embedded "run_block_1")

  (println "图像创建完成"))

(defn demonstrate-image-formats
  "图像格式"
  []
  (println "\n=== 图像格式 ===")

  (py/call-attr py-embedded "run_block_2")

  (println "图像格式演示完成"))

(defn demonstrate-pixel-manipulation
  "像素操作"
  []
  (println "\n=== 像素操作 ===")

  (py/call-attr py-embedded "run_block_3")

  (println "像素操作完成"))

(defn -main
  [& args]
  (println "=== PySide6 图像处理示例 (Clojure) ===")

  (demonstrate-image-creation)
  (demonstrate-image-formats)
  (demonstrate-pixel-manipulation)

  (println "\n=== 图像要点 ===")
  (println "1. QImage: 像素级图像操作")
  (println "2. QPainter: 在图像上绘制")
  (println "3. 支持格式: PNG, JPEG, BMP, GIF")
  (println "4. setPixelColor: 逐像素操作")
  (println "5. save(): 保存为文件")

  (println "\n=== 完成 ==="))
