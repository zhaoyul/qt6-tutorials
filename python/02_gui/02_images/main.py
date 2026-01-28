#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PySide6 图像处理示例

主要类：
- QImage: 独立于硬件的图像表示，支持像素访问
- QPixmap: 优化的屏幕显示图像
- QBitmap: 单色 QPixmap
- QIcon: 多分辨率图标

QImage vs QPixmap:
- QImage: I/O操作、像素操作、非GUI线程
- QPixmap: 屏幕显示、性能优化

官方文档: https://doc.qt.io/qtforpython/PySide6/QtGui/QImage.html
"""

import sys
from PySide6.QtGui import (
    QGuiApplication,
    QImage,
    QImageReader,
    QImageWriter,
    QPixmap,
    QColor,
    QPainter,
    QFont,
    QTransform
)
from PySide6.QtCore import Qt


def create_image_from_scratch():
    """创建图像"""
    print("\n=== 创建图像 ===\n")
    
    # 创建空白图像
    image = QImage(200, 150, QImage.Format_RGB32)
    image.fill(Qt.white)
    
    print(f"尺寸: {image.size().toTuple()}")
    print(f"宽度: {image.width()}")
    print(f"高度: {image.height()}")
    print(f"深度: {image.depth()} bits")
    print(f"格式: {image.format()}")
    print(f"字节数: {image.sizeInBytes()}")
    
    # 直接设置像素
    for y in range(image.height()):
        for x in range(image.width()):
            # 创建渐变效果
            r = int(x * 255 / image.width())
            g = int(y * 255 / image.height())
            b = 128
            image.setPixelColor(x, y, QColor(r, g, b))
    
    image.save("gradient.png")
    print("渐变图像已保存: gradient.png")


def manipulate_pixels():
    """像素操作"""
    print("\n=== 像素操作 ===\n")
    
    image = QImage(100, 100, QImage.Format_ARGB32)
    image.fill(Qt.white)
    
    # 方式1: setPixel (慢，但简单)
    for i in range(50):
        image.setPixelColor(i, i, QColor(255, 0, 0, 255))
    
    # 方式2: scanLine (快，推荐) - 注意：PySide6中处理方式略有不同
    # 使用像素操作替代
    for y in range(50, image.height()):
        for x in range(50, image.width()):
            image.setPixelColor(x, y, QColor(0, 0, 255, 128))  # 半透明蓝
    
    # 读取像素
    color = image.pixelColor(25, 25)
    print(f"像素(25,25) R:{color.red()} G:{color.green()} B:{color.blue()} A:{color.alpha()}")
    
    image.save("pixels.png")
    print("像素操作图像已保存: pixels.png")


def image_transformations():
    """图像变换"""
    print("\n=== 图像变换 ===\n")
    
    # 创建原始图像
    original = QImage(100, 80, QImage.Format_RGB32)
    painter = QPainter(original)
    painter.fillRect(original.rect(), Qt.white)
    painter.setPen(Qt.blue)
    font = QFont("Arial", 20)
    painter.setFont(font)
    painter.drawText(original.rect(), Qt.AlignCenter, "Qt6")
    painter.end()
    
    original.save("original.png")
    
    # 缩放
    scaled = original.scaled(200, 160, Qt.KeepAspectRatio,
                             Qt.SmoothTransformation)
    scaled.save("scaled.png")
    print(f"缩放: 100x80 -> {scaled.size().toTuple()}")
    
    # 镜像
    mirrored = original.mirrored(True, False)  # 水平镜像
    mirrored.save("mirrored.png")
    print("水平镜像已保存")
    
    # 旋转 (通过 QTransform)
    transform = QTransform()
    transform.rotate(45)
    rotated = original.transformed(transform, Qt.SmoothTransformation)
    rotated.save("rotated.png")
    print("旋转45度已保存")
    
    # 裁剪
    cropped = original.copy(10, 10, 50, 40)
    cropped.save("cropped.png")
    print("裁剪已保存")


def image_formats():
    """图像格式"""
    print("\n=== 图像格式 ===\n")
    
    print("支持的读取格式:")
    for fmt in QImageReader.supportedImageFormats():
        print(f"  {fmt.data().decode()}")
    
    print("\n支持的写入格式:")
    for fmt in QImageWriter.supportedImageFormats():
        print(f"  {fmt.data().decode()}")


def color_conversion():
    """颜色与格式转换"""
    print("\n=== 颜色与格式转换 ===\n")
    
    color_image = QImage(100, 100, QImage.Format_ARGB32)
    color_image.fill(QColor(100, 150, 200))
    
    # 转换为灰度
    grayscale = color_image.convertToFormat(QImage.Format_Grayscale8)
    grayscale.save("grayscale.png")
    print("灰度图像已保存")
    
    # 转换为单色
    mono = color_image.convertToFormat(QImage.Format_Mono)
    mono.save("mono.png")
    print("单色图像已保存")
    
    # QColor 操作
    color = QColor(255, 128, 64)
    print("\nQColor 示例:")
    print(f"RGB: {color.red()} {color.green()} {color.blue()}")
    print(f"HSV: {color.hue()} {color.saturation()} {color.value()}")
    print(f"十六进制: {color.name()}")
    
    # 颜色变换
    lighter = color.lighter(150)  # 150% 亮度
    darker = color.darker(150)    # 150% 暗度
    print(f"更亮: {lighter.name()}")
    print(f"更暗: {darker.name()}")


def composite_images():
    """图像合成"""
    print("\n=== 图像合成 ===\n")
    
    # 背景
    background = QImage(200, 150, QImage.Format_ARGB32)
    background.fill(QColor(200, 220, 255))
    
    # 前景 (带透明)
    foreground = QImage(100, 75, QImage.Format_ARGB32)
    foreground.fill(Qt.transparent)
    fp = QPainter(foreground)
    fp.setBrush(QColor(255, 0, 0, 180))
    fp.drawEllipse(foreground.rect())
    fp.end()
    
    # 合成
    painter = QPainter(background)
    painter.setCompositionMode(QPainter.CompositionMode_SourceOver)
    painter.drawImage(50, 37, foreground)
    painter.end()
    
    background.save("composite.png")
    print("合成图像已保存: composite.png")
    
    print("\n常用合成模式:")
    print("- SourceOver: 标准 alpha 混合")
    print("- DestinationOver: 目标在上")
    print("- Clear: 清除")
    print("- Source: 替换")
    print("- Multiply: 正片叠底")
    print("- Screen: 滤色")


def main():
    """主函数"""
    app = QGuiApplication(sys.argv)
    
    print("=== PySide6 图像处理示例 ===")
    
    create_image_from_scratch()
    manipulate_pixels()
    image_transformations()
    image_formats()
    color_conversion()
    composite_images()
    
    print("\n=== 图像处理要点 ===")
    print("1. QImage 用于像素操作")
    print("2. QPixmap 用于屏幕显示")
    print("3. setPixelColor 和 pixelColor 用于像素操作")
    print("4. 使用 Qt.SmoothTransformation 获得好质量")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
