#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PySide6 定时器示例

Qt 提供多种定时功能：
- QTimer: 高级定时器类
- QObject.startTimer: 基础定时器
- QElapsedTimer: 计时器 (测量时间)
- QDeadlineTimer: 截止时间

定时器类型：
- Qt.PreciseTimer: 精确定时
- Qt.CoarseTimer: 粗略定时 (节能)
- Qt.VeryCoarseTimer: 非常粗略

官方文档: https://doc.qt.io/qtforpython/PySide6/QtCore/QTimer.html
"""

import sys
import time
from PySide6.QtCore import (
    QCoreApplication,
    QObject,
    QTimer,
    QElapsedTimer,
    QDeadlineTimer,
    QThread,
    Qt,
    Signal,
    Slot
)


class TimerDemo(QObject):
    """定时器演示类"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._repeat_timer = None
        self._basic_timer_id = 0
        self._count = 0
    
    def demonstrate_qtimer(self):
        """QTimer 重复定时器示例"""
        print("\n=== QTimer 示例 ===\n")
        
        # 创建重复定时器
        self._repeat_timer = QTimer(self)
        self._repeat_timer.timeout.connect(self.on_repeat_timeout)
        self._repeat_timer.start(100)  # 100ms 间隔
        
        print("重复定时器已启动 (100ms 间隔)")
    
    def demonstrate_single_shot(self):
        """singleShot 单次定时示例"""
        print("\n=== singleShot 示例 ===\n")
        
        # 方式1: 静态方法 + Lambda
        QTimer.singleShot(200, lambda: print("singleShot Lambda 执行"))
        
        # 方式2: 静态方法 + 槽函数
        QTimer.singleShot(300, self.on_single_shot_timeout)
        
        # 方式3: 使用 QTimer 对象
        timer = QTimer(self)
        timer.setSingleShot(True)
        timer.timeout.connect(lambda: print("QTimer singleShot 执行"))
        timer.start(250)
        
        print("单次定时器已安排")
    
    def demonstrate_timer_types(self):
        """定时器类型示例"""
        print("\n=== 定时器类型 ===\n")
        
        precise_timer = QTimer(self)
        precise_timer.setTimerType(Qt.PreciseTimer)
        print("精确定时器: 误差 < 1ms")
        
        coarse_timer = QTimer(self)
        coarse_timer.setTimerType(Qt.CoarseTimer)
        print("粗略定时器: 误差 ~5%，节省电量")
        
        very_coarse_timer = QTimer(self)
        very_coarse_timer.setTimerType(Qt.VeryCoarseTimer)
        print("非常粗略定时器: 整秒级别")
    
    def timerEvent(self, event):
        """
        基础定时器事件处理
        重写 QObject.timerEvent 方法
        """
        if event.timerId() == self._basic_timer_id:
            print("基础定时器触发")
        super().timerEvent(event)
    
    @Slot()
    def on_repeat_timeout(self):
        """重复定时器超时处理"""
        self._count += 1
        print(f"重复定时器 #{self._count}")
        
        if self._count >= 5:
            self._repeat_timer.stop()
            print("重复定时器已停止")
            
            # 停止所有定时器后退出
            QTimer.singleShot(100, QCoreApplication.instance().quit)
    
    @Slot()
    def on_single_shot_timeout(self):
        """单次定时器槽函数"""
        print("singleShot 槽执行")
    
    def start_basic_timer(self):
        """启动基础定时器"""
        print("\n=== 基础定时器 (startTimer) ===\n")
        self._basic_timer_id = self.startTimer(150)
        print(f"基础定时器 ID: {self._basic_timer_id}")
        
        # 停止基础定时器
        def stop_basic():
            self.killTimer(self._basic_timer_id)
            print("基础定时器已停止")
        
        QTimer.singleShot(400, stop_basic)


def demonstrate_elapsed_timer():
    """QElapsedTimer 计时器示例"""
    print("\n=== QElapsedTimer (计时) ===\n")
    
    timer = QElapsedTimer()
    timer.start()
    
    # 模拟工作
    total = 0
    for i in range(1000000):
        total += i
    
    print(f"耗时: {timer.elapsed()} ms")
    print(f"耗时 (纳秒): {timer.nsecsElapsed()} ns")
    
    # 重启计时
    timer.restart()
    QThread.msleep(50)
    print(f"sleep 50ms 实际耗时: {timer.elapsed()} ms")
    
    # 检查是否过期
    timer.restart()
    print(f"已过去 100ms: {timer.hasExpired(100)}")


def demonstrate_deadline_timer():
    """QDeadlineTimer 截止时间示例"""
    print("\n=== QDeadlineTimer (截止时间) ===\n")
    
    # 设置 100ms 截止时间
    deadline = QDeadlineTimer(100)
    
    print(f"剩余时间: {deadline.remainingTime()} ms")
    print(f"已过期: {deadline.hasExpired()}")
    
    QThread.msleep(50)
    print(f"50ms 后剩余: {deadline.remainingTime()} ms")
    
    QThread.msleep(60)
    print(f"110ms 后已过期: {deadline.hasExpired()}")
    
    # 永不过期
    never_expires = QDeadlineTimer(QDeadlineTimer.Forever)
    print(f"永不过期定时器已过期: {never_expires.hasExpired()}")


def demonstrate_python_time():
    """Python time 模块对比"""
    print("\n=== Python time 模块对比 ===\n")
    
    # time.time() 获取当前时间戳
    start = time.time()
    
    # 模拟工作
    total = sum(range(1000000))
    
    elapsed = (time.time() - start) * 1000
    print(f"Python time 耗时: {elapsed:.2f} ms")
    
    # time.perf_counter() 高精度计时
    start = time.perf_counter()
    time.sleep(0.05)  # 50ms
    elapsed = (time.perf_counter() - start) * 1000
    print(f"Python sleep 50ms 实际: {elapsed:.2f} ms")
    
    print("\n对比总结:")
    print("- QTimer: 与Qt事件循环集成，GUI应用首选")
    print("- Python time: 简单脚本适用，不依赖Qt")


def main():
    """主函数"""
    app = QCoreApplication(sys.argv)
    
    print("=== PySide6 定时器示例 ===")
    
    demonstrate_elapsed_timer()
    demonstrate_deadline_timer()
    demonstrate_python_time()
    
    demo = TimerDemo()
    demo.demonstrate_timer_types()
    demo.demonstrate_qtimer()
    demo.demonstrate_single_shot()
    demo.start_basic_timer()
    
    print("\n--- 进入事件循环 ---\n")
    
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
