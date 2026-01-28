#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PySide6 2D绘图系统示例

Qt 提供强大的2D绘图能力：
- QPainter: 绑定设备
- QPaintDevice: 绘图表面 (QImage, QPixmap, QWidget等)
- QPen: 线条样式
- QBrush: 填充样式
- QFont: 文字样式

主要功能：
- 基本图形绘制
- 路径绘制 (QPainterPath)
- 变换 (旋转、缩放、平移)
- 抗锯齿

官方文档: https://doc.qt.io/qtforpython/PySide6/QtGui/QPainter.html
"""

import sys
from PySide6.QtGui import (
    QGuiApplication,
    QImage,
    QPainter,
    QPen,
    QBrush,
    QPainterPath,
    QLinearGradient,
    QRadialGradient,
    QConicalGradient,
    QFont,
    QColor
)
from PySide6.QtCore import Qt, QPoint, QRect


def draw_basic_shapes(painter: QPainter):
    """绘制基本图形"""
    # 基本图形
    painter.setPen(QPen(Qt.black, 2))
    painter.setBrush(Qt.cyan)
    
    # 矩形
    painter.drawRect(10, 10, 80, 60)
    
    # 圆角矩形
    painter.setBrush(Qt.magenta)
    painter.drawRoundedRect(100, 10, 80, 60, 10, 10)
    
    # 椭圆/圆
    painter.setBrush(Qt.yellow)
    painter.drawEllipse(200, 10, 80, 60)
    
    # 圆
    painter.setBrush(Qt.green)
    painter.drawEllipse(QPoint(340, 40), 30, 30)


def draw_lines(painter: QPainter):
    """绘制线条"""
    y = 100
    
    # 不同线型
    pen = QPen(Qt.blue, 3)
    
    pen.setStyle(Qt.SolidLine)
    painter.setPen(pen)
    painter.drawLine(10, y, 180, y)
    
    pen.setStyle(Qt.DashLine)
    painter.setPen(pen)
    painter.drawLine(10, y + 20, 180, y + 20)
    
    pen.setStyle(Qt.DotLine)
    painter.setPen(pen)
    painter.drawLine(10, y + 40, 180, y + 40)
    
    pen.setStyle(Qt.DashDotLine)
    painter.setPen(pen)
    painter.drawLine(10, y + 60, 180, y + 60)
    
    # 线帽样式
    pen.setStyle(Qt.SolidLine)
    pen.setWidth(10)
    
    pen.setCapStyle(Qt.FlatCap)
    painter.setPen(pen)
    painter.drawLine(200, y, 280, y)
    
    pen.setCapStyle(Qt.RoundCap)
    painter.setPen(pen)
    painter.drawLine(200, y + 30, 280, y + 30)
    
    pen.setCapStyle(Qt.SquareCap)
    painter.setPen(pen)
    painter.drawLine(200, y + 60, 280, y + 60)


def draw_gradients(painter: QPainter):
    """绘制渐变"""
    y = 200
    
    # 线性渐变
    linear_grad = QLinearGradient(10, y, 90, y + 60)
    linear_grad.setColorAt(0, Qt.red)
    linear_grad.setColorAt(0.5, Qt.yellow)
    linear_grad.setColorAt(1, Qt.green)
    painter.setBrush(linear_grad)
    painter.drawRect(10, y, 80, 60)
    
    # 径向渐变
    radial_grad = QRadialGradient(150, y + 30, 40)
    radial_grad.setColorAt(0, Qt.white)
    radial_grad.setColorAt(1, Qt.blue)
    painter.setBrush(radial_grad)
    painter.drawEllipse(110, y, 80, 60)
    
    # 锥形渐变
    conical_grad = QConicalGradient(250, y + 30, 0)
    conical_grad.setColorAt(0, Qt.red)
    conical_grad.setColorAt(0.33, Qt.green)
    conical_grad.setColorAt(0.66, Qt.blue)
    conical_grad.setColorAt(1, Qt.red)
    painter.setBrush(conical_grad)
    painter.drawEllipse(210, y, 80, 60)


def draw_path(painter: QPainter):
    """绘制路径"""
    y = 300
    
    # 自定义路径
    path = QPainterPath()
    path.moveTo(10, y + 50)
    path.lineTo(50, y)
    path.lineTo(90, y + 50)
    path.closeSubpath()
    
    painter.setPen(QPen(Qt.darkGreen, 2))
    painter.setBrush(Qt.lightGray)
    painter.drawPath(path)
    
    # 贝塞尔曲线
    bezier = QPainterPath()
    bezier.moveTo(110, y + 50)
    bezier.cubicTo(130, y, 170, y, 190, y + 50)
    
    painter.setPen(QPen(Qt.darkMagenta, 3))
    painter.setBrush(Qt.NoBrush)
    painter.drawPath(bezier)
    
    # 文字路径
    text_path = QPainterPath()
    font = QFont("Arial", 24, QFont.Bold)
    text_path.addText(210, y + 40, font, "Qt6")
    
    painter.setPen(Qt.NoPen)
    painter.setBrush(Qt.darkBlue)
    painter.drawPath(text_path)


def draw_with_transform(painter: QPainter):
    """绘制变换"""
    y = 400
    
    painter.save()
    
    # 平移
    painter.translate(50, y + 30)
    
    # 绘制原始矩形
    painter.setPen(QPen(Qt.black, 2))
    painter.setBrush(Qt.red)
    painter.drawRect(-20, -15, 40, 30)
    
    # 旋转
    painter.rotate(30)
    painter.setBrush(QColor(0, 255, 0, 128))  # 半透明
    painter.drawRect(-20, -15, 40, 30)
    
    painter.restore()
    
    # 缩放示例
    painter.save()
    painter.translate(150, y + 30)
    painter.scale(1.5, 0.8)
    painter.setBrush(Qt.blue)
    painter.drawEllipse(-25, -25, 50, 50)
    painter.restore()


def draw_text(painter: QPainter):
    """绘制文字"""
    y = 480
    
    painter.setPen(Qt.black)
    
    # 普通文字
    painter.setFont(QFont("Arial", 12))
    painter.drawText(10, y + 20, "Normal Text")
    
    # 粗体
    painter.setFont(QFont("Arial", 12, QFont.Bold))
    painter.drawText(120, y + 20, "Bold Text")
    
    # 斜体
    italic_font = QFont("Arial", 12)
    italic_font.setItalic(True)
    painter.setFont(italic_font)
    painter.drawText(220, y + 20, "Italic Text")
    
    # 在矩形内绘制文字
    painter.setFont(QFont("Arial", 10))
    text_rect = QRect(10, y + 30, 150, 40)
    painter.drawRect(text_rect)
    painter.drawText(text_rect, Qt.AlignCenter | Qt.TextWordWrap,
                     "Centered text in rectangle")


def main():
    """主函数"""
    app = QGuiApplication(sys.argv)
    
    print("=== PySide6 2D绘图系统示例 ===\n")
    
    # 创建画布
    image = QImage(400, 550, QImage.Format_ARGB32)
    image.fill(Qt.white)
    
    # 创建画家
    painter = QPainter(image)
    painter.setRenderHint(QPainter.Antialiasing)  # 抗锯齿
    painter.setRenderHint(QPainter.TextAntialiasing)
    
    print("绘制基本图形...")
    draw_basic_shapes(painter)
    
    print("绘制线条...")
    draw_lines(painter)
    
    print("绘制渐变...")
    draw_gradients(painter)
    
    print("绘制路径...")
    draw_path(painter)
    
    print("绘制变换...")
    draw_with_transform(painter)
    
    print("绘制文字...")
    draw_text(painter)
    
    painter.end()
    
    # 保存图像
    filename = "painting_demo.png"
    if image.save(filename):
        print(f"\n图像已保存到: {filename}")
    
    print("\n=== 绘图要点 ===")
    print("1. QPainter 必须绑定到 QPaintDevice")
    print("2. 使用 save()/restore() 保存/恢复状态")
    print("3. setRenderHint 启用抗锯齿")
    print("4. QPainterPath 用于复杂图形")
    print("5. 渐变可用于 QBrush")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
