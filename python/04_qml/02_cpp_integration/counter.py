#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python 类暴露给 QML

关键装饰器和类型：
- @QmlElement: 自动注册到 QML (PySide6 6.4+)
- @Property: 暴露属性
- @Slot: 暴露方法
- 信号: 自动可用于 QML

对应 C++ 的 counter.h/counter.cpp
"""

from PySide6.QtCore import QObject, Property, Signal, Slot, QEnum
from PySide6.QtQml import QmlElement

# 定义 QML 导入信息 (必须在使用 @QmlElement 之前)
QML_IMPORT_NAME = "com.examples.counter"
QML_IMPORT_MAJOR_VERSION = 1
QML_IMPORT_MINOR_VERSION = 0


# 注册到 QML
# 注意：需要 PySide6 6.4+ 支持 @QmlElement
# 对于旧版本，可以在 main.py 中使用 qmlRegisterType
try:
    @QmlElement
    class Counter(QObject):
        """计数器类 - 暴露给 QML"""
        
        # 定义信号
        valueChanged = Signal()  # 值变化信号
        stepChanged = Signal()   # 步长变化信号
        limitReached = Signal(str)  # 边界信号，带消息参数
        
        def __init__(self, parent=None):
            super().__init__(parent)
            self._value = 0
            self._step = 1
            self._min_value = 0
            self._max_value = 100
        
        # value 属性
        @Property(int, notify=valueChanged)
        def value(self):
            return self._value
        
        @value.setter
        def value(self, val):
            if self._value != val:
                self._value = max(self._min_value, min(val, self._max_value))
                self.valueChanged.emit()
                
                # 检查边界
                if self._value == self._max_value:
                    self.limitReached.emit("已达到最大值!")
                elif self._value == self._min_value:
                    self.limitReached.emit("已达到最小值!")
        
        # step 属性
        @Property(int, notify=stepChanged)
        def step(self):
            return self._step
        
        @step.setter
        def step(self, val):
            if self._step != val:
                self._step = val
                self.stepChanged.emit()
        
        # displayText 只读属性
        @Property(str, notify=valueChanged)
        def displayText(self):
            return f"当前值: {self._value}"
        
        @Slot()
        def increment(self):
            """增加"""
            print("[Python] increment() 被调用")
            self.value = self._value + self._step
        
        @Slot()
        def decrement(self):
            """减少"""
            print("[Python] decrement() 被调用")
            self.value = self._value - self._step
        
        @Slot()
        def reset(self):
            """重置"""
            print("[Python] reset() 被调用")
            self.value = 0
        
        @Slot(str, result=str)
        def formatValue(self, prefix):
            """格式化值"""
            return f"{prefix}: {self._value}"

except ImportError:
    # 如果 @QmlElement 不可用，定义普通类并在 main.py 中注册
    class Counter(QObject):
        """计数器类 - 暴露给 QML"""
        
        valueChanged = Signal()
        stepChanged = Signal()
        limitReached = Signal(str)
        
        def __init__(self, parent=None):
            super().__init__(parent)
            self._value = 0
            self._step = 1
            self._min_value = 0
            self._max_value = 100
        
        @Property(int, notify=valueChanged)
        def value(self):
            return self._value
        
        @value.setter
        def value(self, val):
            if self._value != val:
                self._value = max(self._min_value, min(val, self._max_value))
                self.valueChanged.emit()
                if self._value == self._max_value:
                    self.limitReached.emit("已达到最大值!")
                elif self._value == self._min_value:
                    self.limitReached.emit("已达到最小值!")
        
        @Property(int, notify=stepChanged)
        def step(self):
            return self._step
        
        @step.setter
        def step(self, val):
            if self._step != val:
                self._step = val
                self.stepChanged.emit()
        
        @Property(str, notify=valueChanged)
        def displayText(self):
            return f"当前值: {self._value}"
        
        @Slot()
        def increment(self):
            print("[Python] increment() 被调用")
            self.value = self._value + self._step
        
        @Slot()
        def decrement(self):
            print("[Python] decrement() 被调用")
            self.value = self._value - self._step
        
        @Slot()
        def reset(self):
            print("[Python] reset() 被调用")
            self.value = 0
        
        @Slot(str, result=str)
        def formatValue(self, prefix):
            return f"{prefix}: {self._value}"
