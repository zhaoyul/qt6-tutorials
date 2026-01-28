#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PySide6 窗口系统示例

QWindow 是 Qt GUI 的底层窗口类：
- 不依赖 Qt Widgets
- 可用于 OpenGL、Vulkan 渲染
- QWidget 内部使用 QWindow

主要功能：
- 窗口属性 (标题、大小、位置)
- 窗口状态 (最大化、最小化、全屏)
- 窗口标志 (无边框、置顶)
- 屏幕信息

官方文档: https://doc.qt.io/qtforpython/PySide6/QtGui/QWindow.html
"""

import sys
from PySide6.QtGui import (
    QGuiApplication,
    QWindow,
    QBackingStore,
    QPainter,
    QKeyEvent,
    QColor,
    QFont
)
from PySide6.QtCore import Qt, QSize, QRect


class DemoWindow(QWindow):
    """演示窗口类"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._backing_store = QBackingStore(self)
        
        # 窗口属性
        self.setTitle("PySide6 Window Demo")
        self.resize(500, 400)
        
        # 设置最小/最大尺寸
        self.setMinimumSize(QSize(300, 200))
        self.setMaximumSize(QSize(800, 600))
        
        # 窗口图标 (如果有)
        # self.setIcon(QIcon("icon.png"))
    
    def show_window_info(self):
        """显示窗口信息"""
        print("\n=== 窗口信息 ===")
        print(f"标题: {self.title()}")
        print(f"大小: {self.size().toTuple()}")
        print(f"位置: {self.position().toTuple()}")
        print(f"几何: {self.geometry().getRect()}")
        print(f"最小大小: {self.minimumSize().toTuple()}")
        print(f"最大大小: {self.maximumSize().toTuple()}")
        print(f"可见: {self.isVisible()}")
        print(f"活跃: {self.isActive()}")
        print(f"窗口状态: {self.windowState()}")
        print(f"窗口类型: {self.type()}")
        print(f"不透明度: {self.opacity()}")
    
    def exposeEvent(self, event):
        """曝光事件"""
        if self.isExposed():
            self.render()
    
    def resizeEvent(self, event):
        """大小改变事件"""
        self._backing_store.resize(event.size())
        if self.isExposed():
            self.render()
    
    def keyPressEvent(self, event: QKeyEvent):
        """键盘按下事件"""
        if event.key() == Qt.Key_1:
            # 普通状态
            self.setWindowState(Qt.WindowNoState)
            print("窗口状态: 普通")
        elif event.key() == Qt.Key_2:
            # 最大化
            self.setWindowState(Qt.WindowMaximized)
            print("窗口状态: 最大化")
        elif event.key() == Qt.Key_3:
            # 最小化
            self.setWindowState(Qt.WindowMinimized)
            print("窗口状态: 最小化")
        elif event.key() == Qt.Key_4:
            # 全屏
            self.setWindowState(Qt.WindowFullScreen)
            print("窗口状态: 全屏")
        elif event.key() == Qt.Key_5:
            # 置顶
            self.setFlags(self.flags() ^ Qt.WindowStaysOnTopHint)
            print("切换置顶")
        elif event.key() == Qt.Key_6:
            # 调整不透明度
            self.setOpacity(0.5 if self.opacity() > 0.5 else 1.0)
            print(f"不透明度: {self.opacity()}")
        elif event.key() == Qt.Key_I:
            self.show_window_info()
        elif event.key() == Qt.Key_Escape:
            if self.windowState() == Qt.WindowFullScreen:
                self.setWindowState(Qt.WindowNoState)
            else:
                self.close()
        
        self.render()
    
    def render(self):
        """渲染窗口"""
        if not self.isExposed():
            return
        
        rect = QRect(0, 0, self.width(), self.height())
        self._backing_store.beginPaint(rect)
        
        painter = QPainter(self._backing_store.paintDevice())
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(rect, QColor(250, 250, 250))
        
        painter.setPen(Qt.darkBlue)
        painter.setFont(QFont("Arial", 18, QFont.Bold))
        painter.drawText(20, 40, "PySide6 Window System Demo")
        
        painter.setPen(Qt.black)
        painter.setFont(QFont("Arial", 12))
        
        y = 80
        painter.drawText(20, y, "按键控制:"); y += 25
        painter.drawText(20, y, "1 - 普通窗口"); y += 20
        painter.drawText(20, y, "2 - 最大化"); y += 20
        painter.drawText(20, y, "3 - 最小化"); y += 20
        painter.drawText(20, y, "4 - 全屏 (ESC 退出)"); y += 20
        painter.drawText(20, y, "5 - 切换置顶"); y += 20
        painter.drawText(20, y, "6 - 切换透明度"); y += 20
        painter.drawText(20, y, "I - 显示窗口信息"); y += 20
        painter.drawText(20, y, "ESC - 退出"); y += 35
        
        # 显示当前状态
        painter.setPen(Qt.darkGreen)
        state_map = {
            Qt.WindowNoState: "普通",
            Qt.WindowMinimized: "最小化",
            Qt.WindowMaximized: "最大化",
            Qt.WindowFullScreen: "全屏"
        }
        state = state_map.get(self.windowState(), "未知")
        painter.drawText(20, y, f"当前状态: {state}"); y += 20
        painter.drawText(20, y, f"窗口大小: {self.width()}x{self.height()}"); y += 20
        painter.drawText(20, y, f"不透明度: {self.opacity()}")
        
        painter.end()
        
        self._backing_store.endPaint()
        self._backing_store.flush(rect)


def show_screen_info():
    """显示屏幕信息"""
    print("=== 屏幕信息 ===\n")
    
    screens = QGuiApplication.screens()
    print(f"屏幕数量: {len(screens)}")
    
    for i, screen in enumerate(screens):
        print(f"\n屏幕 {i + 1}:")
        print(f"  名称: {screen.name()}")
        print(f"  几何: {screen.geometry().getRect()}")
        print(f"  可用几何: {screen.availableGeometry().getRect()}")
        print(f"  虚拟几何: {screen.virtualGeometry().getRect()}")
        print(f"  物理尺寸: {screen.physicalSize().toTuple()} mm")
        print(f"  逻辑 DPI: {screen.logicalDotsPerInch()}")
        print(f"  物理 DPI: {screen.physicalDotsPerInch()}")
        print(f"  设备像素比: {screen.devicePixelRatio()}")
        print(f"  刷新率: {screen.refreshRate()} Hz")
        print(f"  色深: {screen.depth()} bits")
        print(f"  方向: {screen.orientation()}")
    
    primary = QGuiApplication.primaryScreen()
    print(f"\n主屏幕: {primary.name()}")


def show_window_types():
    """显示窗口类型"""
    print("\n=== 窗口类型 (Qt.WindowType) ===\n")
    
    print("Qt.Window - 独立窗口")
    print("Qt.Dialog - 对话框")
    print("Qt.Sheet - macOS 表单")
    print("Qt.Popup - 弹出菜单")
    print("Qt.Tool - 工具窗口")
    print("Qt.ToolTip - 提示框")
    print("Qt.SplashScreen - 启动画面")
    
    print("\n=== 窗口标志 (Qt.WindowFlags) ===\n")
    
    print("Qt.FramelessWindowHint - 无边框")
    print("Qt.WindowStaysOnTopHint - 置顶")
    print("Qt.WindowStaysOnBottomHint - 置底")
    print("Qt.WindowTransparentForInput - 穿透点击")
    print("Qt.WindowMinMaxButtonsHint - 最小化/最大化按钮")
    print("Qt.WindowCloseButtonHint - 关闭按钮")


def main():
    """主函数"""
    app = QGuiApplication(sys.argv)
    
    print("=== PySide6 窗口系统示例 ===")
    
    show_screen_info()
    show_window_types()
    
    window = DemoWindow()
    window.show()
    
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
