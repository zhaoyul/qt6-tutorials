#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Counter 类 - 暴露给 QML 的 Python 类

对应 C++ 的 counter.h/counter.cpp
展示如何使用 Property/Signal/Slot 装饰器将 Python 类暴露给 QML
"""

from PySide6.QtCore import QObject, Property, Signal, Slot


class Counter(QObject):
    """
    计数器类 - 暴露给 QML 使用
    
    功能：
    - 值增加/减少（带步长）
    - 边界检查（0-100）
    - 信号通知
    """
    
    # 信号定义
    valueChanged = Signal()
    stepChanged = Signal()
    limitReached = Signal(str)  # 带参数的信号
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._value = 0
        self._step = 1
        self._min_value = 0
        self._max_value = 100
    
    # === 属性定义 ===
    
    @Property(int, notify=valueChanged)
    def value(self):
        """当前值属性 (0-100)"""
        return self._value
    
    @value.setter
    def value(self, val):
        if self._value != val:
            # 边界限制
            self._value = max(self._min_value, min(val, self._max_value))
            self.valueChanged.emit()
            
            # 检查边界并发射信号
            if self._value == self._max_value:
                self.limitReached.emit("已达到最大值!")
            elif self._value == self._min_value:
                self.limitReached.emit("已达到最小值!")
    
    @Property(int, notify=stepChanged)
    def step(self):
        """步长属性"""
        return self._step
    
    @step.setter
    def step(self, s):
        if self._step != s:
            self._step = s
            self.stepChanged.emit()
    
    @Property(str, notify=valueChanged)
    def displayText(self):
        """只读属性：显示文本"""
        return f"当前值: {self._value}"
    
    # === 槽/方法定义 ===
    
    @Slot()
    def increment(self):
        """增加计数"""
        print("[Python] increment() 被调用")
        self.value = self._value + self._step
    
    @Slot()
    def decrement(self):
        """减少计数"""
        print("[Python] decrement() 被调用")
        self.value = self._value - self._step
    
    @Slot()
    def reset(self):
        """重置计数"""
        print("[Python] reset() 被调用")
        self.value = 0
    
    @Slot(str, result=str)
    def formatValue(self, prefix):
        """格式化显示值
        
        Args:
            prefix: 前缀字符串
            
        Returns:
            格式化后的字符串
        """
        return f"{prefix}: {self._value}"
