#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PySide6 属性系统示例

属性系统允许在运行时查询和修改对象属性：
- @Property 装饰器声明属性
- 支持通知信号 (notify)
- 支持动态属性

注意：
- PySide6的Property装饰器与C++ Q_PROPERTY类似
- PySide6没有Qt6 C++的QProperty绑定系统
- 在Python中可以用property + 观察者模式实现绑定效果

官方文档: https://doc.qt.io/qtforpython/PySide6/QtCore/Property.html
"""

import sys
from typing import Any
from PySide6.QtCore import (
    QCoreApplication,
    QObject,
    Property,
    Signal,
    Slot
)


class Rectangle(QObject):
    """
    矩形类 - 展示基础属性
    """
    
    # 信号定义
    widthChanged = Signal()
    heightChanged = Signal()
    areaChanged = Signal()
    perimeterChanged = Signal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._width = 0.0
        self._height = 0.0
    
    # Width 属性
    @Property(float, notify=widthChanged)
    def width(self):
        return self._width
    
    @width.setter
    def width(self, w):
        # 使用小容差比较浮点数，避免精度问题
        if abs(self._width - w) > 1e-10:
            self._width = w
            self.widthChanged.emit()
            self.areaChanged.emit()
            self.perimeterChanged.emit()
    
    # Height 属性
    @Property(float, notify=heightChanged)
    def height(self):
        return self._height
    
    @height.setter
    def height(self, h):
        if abs(self._height - h) > 1e-10:
            self._height = h
            self.heightChanged.emit()
            self.areaChanged.emit()
            self.perimeterChanged.emit()
    
    # 只读计算属性 - 面积
    @Property(float, notify=areaChanged)
    def area(self):
        return self._width * self._height
    
    # 只读计算属性 - 周长
    @Property(float, notify=perimeterChanged)
    def perimeter(self):
        return 2 * (self._width + self._height)
    
    # 常量属性 - 没有notify信号
    @Property(str, constant=True)
    def type(self):
        return "Rectangle"


class BindableRectangle(QObject):
    """
    可绑定矩形类
    注意：PySide6没有Qt6 C++的QProperty绑定系统
    这里使用Python的property和观察者模式实现类似效果
    """
    
    widthChanged = Signal()
    heightChanged = Signal()
    areaChanged = Signal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._width = 0.0
        self._height = 0.0
        self._area_bindings = []  # 绑定回调列表
        
        # 连接信号以实现自动计算
        self.widthChanged.connect(self._update_area)
        self.heightChanged.connect(self._update_area)
    
    @Property(float, notify=widthChanged)
    def width(self):
        return self._width
    
    @width.setter
    def width(self, w):
        if abs(self._width - w) > 1e-10:
            self._width = w
            self.widthChanged.emit()
    
    @Property(float, notify=heightChanged)
    def height(self):
        return self._height
    
    @height.setter
    def height(self, h):
        if abs(self._height - h) > 1e-10:
            self._height = h
            self.heightChanged.emit()
    
    @Property(float, notify=areaChanged)
    def area(self):
        """面积 - 自动计算"""
        return self._width * self._height
    
    def _update_area(self):
        """更新面积并通知绑定"""
        self.areaChanged.emit()
        # 调用所有绑定的回调
        for callback in self._area_bindings:
            callback(self.area)
    
    def subscribe_area(self, callback):
        """
        订阅面积变化（模拟Qt6的bindable property subscribe）
        """
        self._area_bindings.append(callback)


def demonstrate_dynamic_typing():
    """
    展示Python的动态类型特性
    对应C++的QVariant示例
    """
    print("\n=== Python 动态类型示例 ===")
    
    # Python是动态类型，变量可以存储任意类型
    v1 = 42
    v2 = "Hello"
    v3 = 3.14
    v4 = ["a", "b", "c"]
    
    print(f"v1 (int): {v1}, 类型: {type(v1).__name__}")
    print(f"v2 (str): {v2}, 类型: {type(v2).__name__}")
    print(f"v3 (float): {v3}, 类型: {type(v3).__name__}")
    print(f"v4 (list): {v4}, 类型: {type(v4).__name__}")
    
    # 类型检查
    print("\n类型检查:")
    print(f"v1 是 int 类型: {isinstance(v1, int)}")
    print(f"v2 是 int 类型: {isinstance(v2, int)}")
    
    # 类型转换
    num_str = "123"
    print(f"\n'123' 转 int: {int(num_str)}")
    
    # Python的Any类型（类似QVariant的概念）
    def print_any(value: Any):
        print(f"任意类型值: {value}, 类型: {type(value).__name__}")
    
    print("\n使用Any类型:")
    print_any(42)
    print_any("Hello")
    print_any([1, 2, 3])


def main():
    """主函数"""
    app = QCoreApplication(sys.argv)
    
    print("=== PySide6 属性系统示例 ===\n")
    
    # ============ 基础属性 ============
    print("--- 基础属性演示 ---")
    rect = Rectangle()
    
    # 连接信号
    rect.areaChanged.connect(lambda: print(f"面积变化: {rect.area}"))
    
    # 使用 setter
    rect.width = 10
    rect.height = 5
    
    print(f"宽度: {rect.width}")
    print(f"高度: {rect.height}")
    print(f"面积: {rect.area}")
    print(f"周长: {rect.perimeter}")
    print(f"类型: {rect.type}")
    
    # ============ 通过属性系统访问 ============
    print("\n--- 通过 setProperty/property 访问 ---")
    rect.setProperty("width", 20)
    rect.setProperty("height", 10)
    
    print(f"width 属性: {rect.property('width')}")
    print(f"height 属性: {rect.property('height')}")
    print(f"area 属性: {rect.property('area')}")
    
    # ============ 可绑定属性 ============
    print("\n--- 可绑定属性演示 (Python实现) ---")
    brect = BindableRectangle()
    
    # 订阅面积变化
    def on_area_changed(area):
        print(f"绑定属性 - 面积自动更新为: {area}")
    
    brect.subscribe_area(on_area_changed)
    brect.areaChanged.connect(lambda: on_area_changed(brect.area))
    
    brect.width = 5
    brect.height = 4
    
    print(f"绑定矩形面积: {brect.area}")
    
    # 修改宽度, area 自动更新
    brect.width = 10
    
    # ============ Python动态类型 ============
    demonstrate_dynamic_typing()
    
    # ============ 列出所有属性 ============
    print("\n--- 枚举所有属性 ---")
    meta = rect.metaObject()
    for i in range(meta.propertyCount()):
        prop = meta.property(i)
        value = rect.property(prop.name())
        print(f"{prop.name()} = {value}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
