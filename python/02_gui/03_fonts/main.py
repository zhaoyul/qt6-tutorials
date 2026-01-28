#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PySide6 字体系统示例

主要类：
- QFont: 字体选择和配置
- QFontMetrics: 字体度量信息
- QFontDatabase: 系统字体数据库
- QFontInfo: 实际使用的字体信息

官方文档: https://doc.qt.io/qtforpython/PySide6/QtGui/QFont.html
"""

import sys
from PySide6.QtGui import (
    QGuiApplication,
    QFont,
    QFontMetrics,
    QFontDatabase,
    QFontInfo,
    QImage,
    QPainter,
    QColor
)
from PySide6.QtCore import Qt


def explore_system_fonts():
    """系统字体"""
    print("=== 系统字体 ===\n")
    
    # 列出所有字体家族
    families = QFontDatabase.families()
    print(f"系统字体数量: {len(families)}")
    print("\n前10个字体:")
    for i, family in enumerate(families[:10]):
        print(f"  {family}")
    
    # 检查字体样式
    font_family = "Arial"
    if font_family in families:
        print(f"\n{font_family} 的样式:")
        styles = QFontDatabase.styles(font_family)
        for style in styles:
            print(f"  {style}")
    
    # 标准字体
    print("\n标准字体:")
    print(f"系统字体: {QFontDatabase.systemFont(QFontDatabase.GeneralFont).family()}")
    print(f"等宽字体: {QFontDatabase.systemFont(QFontDatabase.FixedFont).family()}")
    print(f"标题字体: {QFontDatabase.systemFont(QFontDatabase.TitleFont).family()}")


def demonstrate_qfont():
    """QFont 配置"""
    print("\n=== QFont 配置 ===\n")
    
    # 基本创建
    font1 = QFont("Arial", 12)
    print(f"基本字体: {font1.family()} {font1.pointSize()}")
    
    # 详细配置
    font2 = QFont()
    font2.setFamily("Times New Roman")
    font2.setPointSize(14)
    font2.setWeight(QFont.Bold)       # 粗细
    font2.setItalic(True)              # 斜体
    font2.setUnderline(True)           # 下划线
    font2.setStrikeOut(False)          # 删除线
    
    print("配置字体:")
    print(f"  家族: {font2.family()}")
    print(f"  大小: {font2.pointSize()} pt")
    print(f"  粗细: {font2.weight()}")
    print(f"  斜体: {font2.italic()}")
    print(f"  下划线: {font2.underline()}")
    
    # 像素大小
    font3 = QFont("Arial")
    font3.setPixelSize(20)  # 像素单位
    print(f"\n像素大小: {font3.pixelSize()} px")
    
    # 字体粗细级别
    print("\n字体粗细级别:")
    print(f"Thin: {QFont.Thin}")
    print(f"Light: {QFont.Light}")
    print(f"Normal: {QFont.Normal}")
    print(f"Medium: {QFont.Medium}")
    print(f"DemiBold: {QFont.DemiBold}")
    print(f"Bold: {QFont.Bold}")
    print(f"ExtraBold: {QFont.ExtraBold}")
    print(f"Black: {QFont.Black}")


def demonstrate_font_metrics():
    """QFontMetrics 度量"""
    print("\n=== QFontMetrics 度量 ===\n")
    
    font = QFont("Arial", 14)
    fm = QFontMetrics(font)
    
    print(f"字体: {font.family()} {font.pointSize()} pt")
    print(f"高度: {fm.height()}")
    print(f"上升部: {fm.ascent()}")
    print(f"下降部: {fm.descent()}")
    print(f"行间距: {fm.leading()}")
    print(f"平均字符宽度: {fm.averageCharWidth()}")
    print(f"最大字符宽度: {fm.maxWidth()}")
    
    # 文字尺寸
    text = "Hello, Qt6!"
    bounding_rect = fm.boundingRect(text)
    print(f"\n文字 \"{text}\" 的尺寸:")
    print(f"  宽度: {fm.horizontalAdvance(text)}")
    print(f"  边界矩形: ({bounding_rect.x()}, {bounding_rect.y()}, "
          f"{bounding_rect.width()}, {bounding_rect.height()})")
    
    # 截断文字
    long_text = "This is a very long text that might need to be elided"
    elided_text = fm.elidedText(long_text, Qt.ElideRight, 150)
    print("\n文字截断 (150px):")
    print(f"  原文: {long_text}")
    print(f"  截断: {elided_text}")


def demonstrate_font_rendering():
    """字体渲染示例"""
    print("\n=== 字体渲染示例 ===\n")
    
    image = QImage(500, 400, QImage.Format_RGB32)
    image.fill(Qt.white)
    
    painter = QPainter(image)
    painter.setRenderHint(QPainter.TextAntialiasing)
    
    y = 30
    
    # 不同大小
    sizes = [10, 14, 18, 24, 32]
    for size in sizes:
        font = QFont("Arial", size)
        painter.setFont(font)
        painter.setPen(Qt.black)
        painter.drawText(10, y, f"Size {size}pt: Hello Qt6")
        y += size + 10
    
    y += 20
    
    # 不同样式
    normal = QFont("Arial", 16)
    bold = QFont("Arial", 16, QFont.Bold)
    italic = QFont("Arial", 16)
    italic.setItalic(True)
    underline = QFont("Arial", 16)
    underline.setUnderline(True)
    
    painter.setFont(normal)
    painter.drawText(10, y, "Normal")
    
    painter.setFont(bold)
    painter.drawText(100, y, "Bold")
    
    painter.setFont(italic)
    painter.drawText(170, y, "Italic")
    
    painter.setFont(underline)
    painter.drawText(250, y, "Underline")
    
    y += 40
    
    # 不同颜色
    color_font = QFont("Arial", 20, QFont.Bold)
    painter.setFont(color_font)
    
    colors = [Qt.red, Qt.green, Qt.blue, Qt.magenta]
    x = 10
    for color in colors:
        painter.setPen(color)
        painter.drawText(x, y, "Color")
        x += 100
    
    y += 40
    
    # 等宽字体 (代码展示)
    mono_font = QFontDatabase.systemFont(QFontDatabase.FixedFont)
    mono_font.setPointSize(12)
    painter.setFont(mono_font)
    painter.setPen(Qt.darkGreen)
    painter.drawText(10, y, "int main() { return 0; }  // Monospace")
    
    y += 40
    
    # 中文字体
    chinese_font = QFont("Arial", 18)  # 系统会回退到支持中文的字体
    painter.setFont(chinese_font)
    painter.setPen(Qt.black)
    painter.drawText(10, y, "中文字体测试 Chinese Font Test")
    
    painter.end()
    
    image.save("fonts_demo.png")
    print("字体渲染示例已保存: fonts_demo.png")


def demonstrate_font_matching():
    """字体匹配"""
    print("\n=== 字体匹配 ===\n")
    
    # 请求字体
    requested_font = QFont("Non Existent Font Family", 12)
    actual_font = QFontInfo(requested_font)
    
    print(f"请求字体: {requested_font.family()}")
    print(f"实际字体: {actual_font.family()}")
    print(f"完全匹配: {actual_font.exactMatch()}")
    
    # 字体替换规则
    print("\n字体回退策略:")
    print("1. Qt 首先尝试完全匹配请求的字体")
    print("2. 如果不存在，使用相似的替代字体")
    print("3. 最后使用系统默认字体")


def main():
    """主函数"""
    app = QGuiApplication(sys.argv)
    
    print("=== PySide6 字体系统示例 ===")
    
    explore_system_fonts()
    demonstrate_qfont()
    demonstrate_font_metrics()
    demonstrate_font_rendering()
    demonstrate_font_matching()
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
