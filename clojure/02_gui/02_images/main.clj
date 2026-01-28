#!/usr/bin/env clojure -M
;; PySide6 图像处理示例 (Clojure + libpython-clj)
;; 注意：macOS GUI 必须在主线程运行，这里使用图像文件操作

(require '[libpython-clj2.python :as py])

(py/initialize!)

(defn demonstrate-image-creation
  "创建图像"
  []
  (println "\n=== QImage 图像创建 ===")
  
  ;; 使用 Python 代码创建图像
  (py/run-simple-string "
from PySide6.QtGui import QImage, QColor, QPainter, QPen, QBrush
from PySide6.QtCore import Qt

# 创建空白图像
image = QImage(400, 300, QImage.Format_RGB32)
image.fill(QColor(240, 240, 240))

# 使用 QPainter 绘制
painter = QPainter(image)

# 绘制矩形
painter.setPen(QPen(QColor(255, 0, 0), 2))
painter.setBrush(QBrush(QColor(255, 200, 200)))
painter.drawRect(50, 50, 100, 80)

# 绘制椭圆
painter.setPen(QPen(QColor(0, 0, 255), 2))
painter.setBrush(QBrush(QColor(200, 200, 255)))
painter.drawEllipse(200, 50, 100, 80)

# 绘制圆角矩形（代替文字）
painter.setPen(QPen(QColor(0, 128, 0), 2))
painter.setBrush(QBrush(QColor(200, 255, 200)))
painter.drawRoundedRect(50, 180, 280, 40, 10, 10)

# 绘制线条装饰
painter.setPen(QPen(QColor(100, 100, 100), 1))
for i in range(5):
    painter.drawLine(50, 240 + i*10, 330, 240 + i*10)

painter.end()

# 保存
if image.save('/tmp/clojure_image.png'):
    print('图像已保存: /tmp/clojure_image.png')
    print(f'大小: {image.width()}x{image.height()}')
else:
    print('保存失败')
")
  
  (println "图像创建完成"))

(defn demonstrate-image-formats
  "图像格式"
  []
  (println "\n=== 图像格式 ===")
  
  (py/run-simple-string "
from PySide6.QtGui import QImage, QImageWriter

# 支持的格式
formats = QImageWriter.supportedImageFormats()
print('支持的图像格式:')
for fmt in formats:
    print(f'  .{fmt.data().decode()}')

# 创建不同格式的图像
image = QImage(100, 100, QImage.Format_RGB32)
image.fill(Qt.red)

# 保存为不同格式
image.save('/tmp/test.png')
image.save('/tmp/test.jpg')
image.save('/tmp/test.bmp')

print('\\n已保存为 PNG, JPEG, BMP 格式')
")
  
  (println "图像格式演示完成"))

(defn demonstrate-pixel-manipulation
  "像素操作"
  []
  (println "\n=== 像素操作 ===")
  
  (py/run-simple-string "
from PySide6.QtGui import QImage, QColor

# 创建图像
image = QImage(200, 200, QImage.Format_RGB32)

# 逐像素设置颜色
for x in range(200):
    for y in range(200):
        # 创建渐变效果
        r = int(255 * x / 200)
        g = int(255 * y / 200)
        b = 128
        image.setPixelColor(x, y, QColor(r, g, b))

# 保存
image.save('/tmp/clojure_gradient.png')
print('渐变图像已保存')
print(f'像素 (100,100) 颜色: {image.pixelColor(100, 100).name()}')
")
  
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

(-main)
