def run_block_1():
    exec(r"""
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
""", globals())

def run_block_2():
    exec(r"""
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
""", globals())
