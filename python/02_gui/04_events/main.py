#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PySide6 GUI事件系统示例

Qt GUI 事件类型：
- QKeyEvent: 键盘事件
- QMouseEvent: 鼠标事件
- QWheelEvent: 滚轮事件
- QResizeEvent: 窗口大小改变
- QPaintEvent: 绘制事件
- QFocusEvent: 焦点事件
- QCloseEvent: 关闭事件

事件处理流程：
1. 事件到达 QGuiApplication
2. 分发到目标窗口
3. 事件过滤器
4. 目标的 event() 方法
5. 特定事件处理器 (keyPressEvent 等)

官方文档: https://doc.qt.io/qtforpython/PySide6/QtGui/QWindow.html
"""

import sys
from PySide6.QtGui import (
    QGuiApplication,
    QWindow,
    QBackingStore,
    QPainter,
    QKeyEvent,
    QMouseEvent,
    QColor,
    QFont
)
from PySide6.QtCore import Qt, QPoint, QEvent, QSize, QRect


class EventWindow(QWindow):
    """
    自定义窗口，演示事件处理
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._backing_store = QBackingStore(self)
        
        self.setTitle("PySide6 GUI Events Demo - Press keys, click mouse")
        self.resize(400, 300)
        self.setMinimumSize(QSize(200, 150))
        
        self._last_event = "等待事件..."
        self._mouse_pos = QPoint(0, 0)
    
    def exposeEvent(self, event):
        """曝光事件 (窗口需要重绘)"""
        if self.isExposed():
            self.render_now()
    
    def resizeEvent(self, event):
        """大小改变事件"""
        self._backing_store.resize(event.size())
        self._last_event = f"Resize: {event.size().width()}x{event.size().height()}"
        
        print(f"窗口大小改变: {event.oldSize().toTuple()} -> {event.size().toTuple()}")
        
        if self.isExposed():
            self.render_now()
    
    def keyPressEvent(self, event: QKeyEvent):
        """键盘按下事件"""
        key_text = event.text() if event.text() else f"Key_{event.key()}"
        
        self._last_event = f"KeyPress: {key_text} (key={event.key()})"
        
        print("键盘按下:")
        print(f"  键值: {event.key()}")
        print(f"  文本: {event.text()}")
        print(f"  修饰符: {event.modifiers()}")
        print(f"  自动重复: {event.isAutoRepeat()}")
        
        # 检查修饰键
        if event.modifiers() & Qt.ControlModifier:
            print("  Ctrl 被按下")
        if event.modifiers() & Qt.ShiftModifier:
            print("  Shift 被按下")
        
        # ESC 关闭窗口
        if event.key() == Qt.Key_Escape:
            self.close()
            return
        
        self.render_now()
    
    def keyReleaseEvent(self, event: QKeyEvent):
        """键盘释放事件"""
        print(f"键盘释放: {event.key()}")
    
    def mousePressEvent(self, event: QMouseEvent):
        """鼠标按下事件"""
        self._mouse_pos = event.position().toPoint()
        
        button_map = {
            Qt.LeftButton: "Left",
            Qt.RightButton: "Right",
            Qt.MiddleButton: "Middle"
        }
        button = button_map.get(event.button(), "Other")
        
        self._last_event = f"MousePress: {button} at ({self._mouse_pos.x()}, {self._mouse_pos.y()})"
        
        print("鼠标按下:")
        print(f"  按钮: {event.button()}")
        print(f"  位置: {event.position().toTuple()}")
        print(f"  全局位置: {event.globalPosition().toTuple()}")
        print(f"  所有按下的按钮: {event.buttons()}")
        
        self.render_now()
    
    def mouseReleaseEvent(self, event: QMouseEvent):
        """鼠标释放事件"""
        print(f"鼠标释放: {event.button()} at {event.position().toTuple()}")
    
    def mouseMoveEvent(self, event: QMouseEvent):
        """鼠标移动事件"""
        self._mouse_pos = event.position().toPoint()
        self._last_event = f"MouseMove: ({self._mouse_pos.x()}, {self._mouse_pos.y()})"
        
        self.render_now()
    
    def mouseDoubleClickEvent(self, event: QMouseEvent):
        """鼠标双击事件"""
        self._last_event = f"DoubleClick at ({event.position().x()}, {event.position().y()})"
        
        print(f"鼠标双击: {event.position().toTuple()}")
        
        self.render_now()
    
    def wheelEvent(self, event):
        """滚轮事件"""
        delta = event.angleDelta()
        self._last_event = f"Wheel: delta=({delta.x()}, {delta.y()})"
        
        print("滚轮事件:")
        print(f"  角度增量: {delta.toTuple()}")
        print(f"  像素增量: {event.pixelDelta().toTuple()}")
        
        self.render_now()
    
    def focusInEvent(self, event):
        """焦点进入事件"""
        print(f"获得焦点, 原因: {event.reason()}")
        self._last_event = "FocusIn"
        self.render_now()
    
    def focusOutEvent(self, event):
        """焦点离开事件"""
        print(f"失去焦点, 原因: {event.reason()}")
        self._last_event = "FocusOut"
        self.render_now()
    
    def event(self, event: QEvent) -> bool:
        """通用事件处理器"""
        # 可以在这里拦截所有事件
        if event.type() == QEvent.Enter:
            print("鼠标进入窗口")
        elif event.type() == QEvent.Leave:
            print("鼠标离开窗口")
        
        return super().event(event)
    
    def render_now(self):
        """立即渲染"""
        if not self.isExposed():
            return
        
        rect = QRect(0, 0, self.width(), self.height())
        self._backing_store.beginPaint(rect)
        
        painter = QPainter(self._backing_store.paintDevice())
        painter.setRenderHint(QPainter.Antialiasing)
        
        # 背景
        painter.fillRect(rect, QColor(240, 240, 240))
        
        # 标题
        painter.setPen(Qt.darkBlue)
        painter.setFont(QFont("Arial", 16, QFont.Bold))
        painter.drawText(10, 30, "PySide6 GUI Events Demo")
        
        # 说明
        painter.setPen(Qt.black)
        painter.setFont(QFont("Arial", 11))
        painter.drawText(10, 55, "按键盘、移动鼠标、点击、滚轮来测试事件")
        painter.drawText(10, 75, "按 ESC 退出")
        
        # 最后事件
        painter.setPen(Qt.darkGreen)
        painter.setFont(QFont("Arial", 14))
        painter.drawText(10, 120, f"最后事件: {self._last_event}")
        
        # 鼠标位置
        painter.setPen(Qt.darkRed)
        painter.drawText(10, 150, f"鼠标位置: ({self._mouse_pos.x()}, {self._mouse_pos.y()})")
        
        # 绘制鼠标位置标记
        painter.setBrush(Qt.red)
        painter.drawEllipse(self._mouse_pos, 5, 5)
        
        # 窗口大小
        painter.setPen(Qt.gray)
        painter.setFont(QFont("Arial", 10))
        painter.drawText(10, self.height() - 10,
                        f"窗口大小: {self.width()}x{self.height()}")
        
        painter.end()
        
        self._backing_store.endPaint()
        self._backing_store.flush(rect)


def main():
    """主函数"""
    app = QGuiApplication(sys.argv)
    
    print("=== PySide6 GUI事件系统示例 ===")
    print("窗口将显示并响应各种事件")
    print("事件信息将打印到控制台\n")
    
    window = EventWindow()
    window.show()
    
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
