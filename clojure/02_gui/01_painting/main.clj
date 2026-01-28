#!/usr/bin/env clojure -M
;; PySide6 绘制示例 (Clojure + libpython-clj)
;; 注意：macOS GUI 必须在主线程运行，这里使用图像绘制演示

(require '[libpython-clj2.python :as py])

(py/initialize!)

(defn demonstrate-painting
  "QPainter 绘制演示"
  []
  (println "\n=== QPainter 绘制演示 ===")
  
  ;; 使用 Python 代码创建图像并绘制
  (py/run-simple-string "
from PySide6.QtGui import QPainter, QColor, QPen, QBrush, QImage, QPolygon
from PySide6.QtCore import Qt, QPoint

# 创建图像
image = QImage(400, 300, QImage.Format_RGB32)
image.fill(Qt.white)

# 创建画家
painter = QPainter(image)

# 绘制红色矩形
painter.setPen(QPen(QColor(255, 0, 0), 2))
painter.setBrush(QBrush(QColor(255, 200, 200)))
painter.drawRect(20, 20, 100, 80)

# 绘制蓝色椭圆
painter.setPen(QPen(QColor(0, 0, 255), 2))
painter.setBrush(QBrush(QColor(200, 200, 255)))
painter.drawEllipse(140, 20, 100, 80)

# 绘制绿色圆形
painter.setPen(QPen(QColor(0, 255, 0), 2))
painter.setBrush(QBrush(QColor(200, 255, 200)))
painter.drawEllipse(260, 20, 80, 80)

# 绘制线条
painter.setPen(QPen(QColor(255, 0, 255), 3))
painter.drawLine(20, 150, 380, 150)

# 绘制多边形
points = QPolygon([QPoint(50, 200), QPoint(100, 250), QPoint(150, 200), QPoint(100, 150)])
painter.setPen(QPen(QColor(0, 0, 0), 2))
painter.setBrush(QBrush(QColor(255, 255, 200)))
painter.drawPolygon(points)

painter.end()

# 保存图像
if image.save('/tmp/clojure_paint.png'):
    print('图像已保存到 /tmp/clojure_paint.png')
    print(f'图像大小: {image.width()}x{image.height()}')
else:
    print('保存失败')
")
  
  (println "绘制演示完成"))

(defn demonstrate-drawing-primitives
  "绘制基本图形"
  []
  (println "\n=== 绘制基本图形 ===")
  
  (py/run-simple-string "
from PySide6.QtGui import QPainter, QColor, QImage
from PySide6.QtCore import Qt, QRect

image = QImage(300, 200, QImage.Format_RGB32)
image.fill(Qt.white)

painter = QPainter(image)

# 绘制基本形状
painter.drawRect(10, 10, 80, 60)           # 矩形
painter.drawEllipse(100, 10, 80, 60)       # 椭圆
painter.drawArc(190, 10, 80, 60, 0, 5760)  # 弧形

# 绘制点
for i in range(0, 300, 20):
    painter.drawPoint(i, 100)

# 绘制多条线
for i in range(5):
    painter.drawLine(10, 120 + i*15, 290, 120 + i*15)

painter.end()
image.save('/tmp/clojure_shapes.png')
print('基本图形已保存到 /tmp/clojure_shapes.png')
")
  
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

(-main)
