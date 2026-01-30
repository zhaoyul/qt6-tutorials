def run_block_1():
    exec(r"""
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
""", globals())

def run_block_2():
    exec(r"""
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

print('\n已保存为 PNG, JPEG, BMP 格式')
""", globals())

def run_block_3():
    exec(r"""
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
""", globals())
