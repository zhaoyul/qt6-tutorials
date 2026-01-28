#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PySide6 事件循环示例

Qt 应用的核心是事件循环：
- QCoreApplication: 控制台应用
- QGuiApplication: GUI 应用 (无 Widgets)
- QApplication: Widgets 应用

事件循环处理：
- 系统事件 (鼠标、键盘)
- 定时器事件
- 自定义事件
- 信号槽调用

官方文档: https://doc.qt.io/qtforpython/PySide6/QtCore/QEvent.html
"""

import sys
from PySide6.QtCore import (
    QCoreApplication,
    QObject,
    QEvent,
    QTimer,
    Signal
)


# 注册自定义事件类型
# PySide6中通过QEvent.registerEventType()获取唯一类型ID
CUSTOM_EVENT_TYPE = QEvent.registerEventType()


class CustomEvent(QEvent):
    """
    自定义事件类
    继承QEvent并添加自定义数据
    """
    
    def __init__(self, message: str):
        super().__init__(QEvent.Type(CUSTOM_EVENT_TYPE))
        self._message = message
    
    def message(self) -> str:
        return self._message


class EventReceiver(QObject):
    """
    事件接收者
    重写event()方法处理自定义事件
    """
    
    # 定义信号，当收到自定义事件时发出
    customEventReceived = Signal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
    
    def event(self, event: QEvent) -> bool:
        """重写事件处理方法"""
        if event.type() == QEvent.Type(CUSTOM_EVENT_TYPE):
            # 处理自定义事件
            custom_event = event  # 在Python中不需要强制转换
            if isinstance(custom_event, CustomEvent):
                print(f"收到自定义事件: {custom_event.message()}")
                self.customEventReceived.emit(custom_event.message())
            return True  # 事件已处理
        
        # 其他事件交给父类处理
        return super().event(event)


class EventFilter(QObject):
    """
    事件过滤器
    可以拦截其他对象的事件
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
    
    def eventFilter(self, watched: QObject, event: QEvent) -> bool:
        """过滤事件"""
        if event.type() == QEvent.Type(CUSTOM_EVENT_TYPE):
            obj_name = watched.objectName() or "未命名对象"
            print(f"事件过滤器拦截了来自 {obj_name} 的事件")
            # 返回 True 表示事件已处理，不再传递
            # 返回 False 表示继续传递事件
            return False  # 继续传递
        
        # 其他事件交给父类处理
        return super().eventFilter(watched, event)


def demonstrate_event_posting():
    """事件发送示例"""
    print("\n=== 事件发送示例 ===\n")
    
    receiver = EventReceiver()
    receiver.setObjectName("TestReceiver")
    
    # 安装事件过滤器
    filter_obj = EventFilter()
    receiver.installEventFilter(filter_obj)
    
    # 连接信号槽
    receiver.customEventReceived.connect(
        lambda msg: print(f"信号槽收到: {msg}")
    )
    
    # postEvent: 异步发送 (推荐)
    print("--- postEvent (异步) ---")
    app = QCoreApplication.instance()
    app.postEvent(receiver, CustomEvent("异步消息1"))
    app.postEvent(receiver, CustomEvent("异步消息2"))
    print("事件已投递到队列")
    
    # 处理所有待处理事件
    app.processEvents()
    
    # sendEvent: 同步发送 (立即处理)
    print("\n--- sendEvent (同步) ---")
    sync_event = CustomEvent("同步消息")
    print("发送前")
    app.sendEvent(receiver, sync_event)
    print("发送后 (已处理)")


def demonstrate_queued_invoke():
    """队列调用示例"""
    print("\n=== 队列调用示例 ===\n")
    
    def queued_function():
        print("队列调用执行")
    
    # 使用 QTimer.singleShot(0, ...) 实现队列调用效果
    # 等价于 C++ 的 QMetaObject::invokeMethod(..., Qt::QueuedConnection)
    QTimer.singleShot(0, queued_function)
    
    print("队列调用已安排")
    QCoreApplication.processEvents()


def main():
    """主函数"""
    app = QCoreApplication(sys.argv)
    app.setApplicationName("EventLoopDemo")
    
    print("=== PySide6 事件循环示例 ===")
    
    print("\n应用信息:")
    print(f"应用名称: {QCoreApplication.applicationName()}")
    print(f"应用目录: {QCoreApplication.applicationDirPath()}")
    print(f"应用文件: {QCoreApplication.applicationFilePath()}")
    print(f"参数: {QCoreApplication.arguments()}")
    
    demonstrate_event_posting()
    demonstrate_queued_invoke()
    
    # 延迟退出
    print("\n--- 事件循环控制 ---")
    print("使用 singleShot 延迟操作")
    
    counter = 0
    
    def on_timer_timeout():
        nonlocal counter
        counter += 1
        print(f"定时器触发 #{counter}")
    
    timer = QTimer()
    timer.timeout.connect(on_timer_timeout)
    timer.start(100)  # 每100ms触发
    
    # 500ms 后退出
    def quit_app():
        print("\n500ms 到达，退出事件循环")
        QCoreApplication.quit()
    
    QTimer.singleShot(550, quit_app)
    
    print("进入事件循环...")
    return app.exec()  # 阻塞直到 quit() 被调用


if __name__ == "__main__":
    sys.exit(main())
