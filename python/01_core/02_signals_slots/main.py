#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PySide6 信号与槽机制示例

信号与槽是Qt最重要的特性，用于对象间通信：
- 信号 (Signal): 当事件发生时发出
- 槽 (Slot): 响应信号的函数

连接方式：
1. 直接连接: signal.connect(slot)
2. Lambda 表达式: signal.connect(lambda value: ...)
3. 断开连接: signal.disconnect(slot)

注意：PySide6的连接语法比C++更简洁

官方文档: https://doc.qt.io/qtforpython/PySide6/QtCore/Signal.html
"""

import sys
from PySide6.QtCore import (
    QCoreApplication,
    QObject,
    Signal,
    Slot,
    QTimer,
    Qt
)


class Counter(QObject):
    """发送者类 - 计数器"""
    
    # 定义信号
    valueChanged = Signal(int)  # 值变化信号
    limitReached = Signal()      # 达到上限信号
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._value = 0
    
    @property
    def value(self):
        return self._value
    
    @Slot()
    def increment(self):
        """增加计数"""
        self._value += 1
        self.valueChanged.emit(self._value)
        
        if self._value >= 10:
            self.limitReached.emit()
    
    @Slot()
    def decrement(self):
        """减少计数"""
        self._value -= 1
        self.valueChanged.emit(self._value)
    
    @Slot(int)
    def setValue(self, value):
        """设置值"""
        if self._value != value:
            self._value = value
            self.valueChanged.emit(self._value)


class Display(QObject):
    """接收者类 - 显示器"""
    
    def __init__(self, name: str, parent=None):
        super().__init__(parent)
        self._name = name
    
    @Slot(int)
    def showValue(self, value: int):
        """显示值槽函数"""
        print(f"{self._name} 显示值: {value}")
    
    @Slot()
    def onLimitReached(self):
        """上限警告槽函数"""
        print(f"{self._name} 警告: 已达到上限!")


def main():
    """主函数"""
    app = QCoreApplication(sys.argv)
    
    print("=== PySide6 信号与槽示例 ===\n")
    
    counter = Counter()
    display1 = Display("显示器1")
    display2 = Display("显示器2")
    
    # ============ 连接方式1: 直接连接 (推荐) ============
    print("--- 方式1: 直接连接 ---")
    # PySide6语法: signal.connect(slot)
    counter.valueChanged.connect(display1.showValue)
    
    # ============ 连接方式2: Lambda 表达式 ============
    print("--- 方式2: Lambda 连接 ---")
    counter.valueChanged.connect(
        lambda value: print(f"Lambda 接收到值: {value}")
    )
    
    # ============ 一个信号连接多个槽 ============
    print("--- 一个信号连接多个槽 ---")
    counter.valueChanged.connect(display2.showValue)
    
    # ============ 信号连接信号 ============
    counter2 = Counter()
    # 将counter的limitReached连接到counter2的increment
    counter.limitReached.connect(counter2.increment)
    counter2.valueChanged.connect(
        lambda v: print(f"Counter2 被触发, 值: {v}")
    )
    
    # 测试
    print("\n--- 测试增加值 ---")
    counter.increment()  # 1
    counter.increment()  # 2
    
    print("\n--- 测试设置值 ---")
    counter.setValue(9)
    
    print("\n--- 触发 limitReached ---")
    counter.increment()  # 10, 触发 limitReached
    
    # ============ 断开连接 ============
    print("\n--- 断开 display2 的连接 ---")
    counter.valueChanged.disconnect(display2.showValue)
    counter.increment()  # display2 不会显示
    
    # ============ 连接类型 ============
    print("\n--- 连接类型说明 ---")
    print("Qt.AutoConnection (默认): 自动选择")
    print("Qt.DirectConnection: 直接调用 (同步)")
    print("Qt.QueuedConnection: 队列调用 (异步)")
    print("Qt.UniqueConnection: 防止重复连接")
    
    # 使用 UniqueConnection 防止重复连接
    # PySide6中通过传递type参数指定连接类型
    try:
        # 尝试重复连接
        counter.valueChanged.connect(
            display1.showValue,
            type=Qt.UniqueConnection
        )
        print("重复连接结果: 成功")
    except RuntimeError as e:
        # 如果连接已存在，会抛出异常
        print(f"重复连接结果: 失败(已存在) - {e}")
    
    # ============ 使用 QTimer 单次触发 ============
    print("\n--- QTimer.singleShot 示例 ---")
    
    def on_timeout():
        print("100ms 后执行的 Lambda")
        app.quit()
    
    QTimer.singleShot(100, on_timeout)
    # 或者使用lambda: QTimer.singleShot(100, lambda: (print("..."), app.quit()))
    
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
