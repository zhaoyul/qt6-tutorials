#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PySide6 图形视图框架示例

Graphics View Framework 用于管理大量2D图形项：
- QGraphicsScene: 场景 (管理所有图形项)
- QGraphicsView: 视图 (显示场景)
- QGraphicsItem: 图形项基类

内置图形项：
- QGraphicsRectItem, QGraphicsEllipseItem
- QGraphicsLineItem, QGraphicsPathItem
- QGraphicsTextItem, QGraphicsPixmapItem

官方文档: https://doc.qt.io/qtforpython/PySide6/QtWidgets/index.html
"""

import sys
import math
import random
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QGraphicsScene, QGraphicsView,
    QGraphicsRectItem, QGraphicsEllipseItem, QGraphicsLineItem,
    QGraphicsTextItem, QGraphicsPathItem, QGraphicsItemGroup,
    QVBoxLayout, QHBoxLayout, QPushButton, QSlider, QLabel,
    QToolBar, QGraphicsItem
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter, QPen, QBrush, QColor, QFont, QPainterPath


class DraggableRect(QGraphicsRectItem):
    """自定义可拖动图形项"""
    
    def __init__(self, x, y, w, h, parent=None):
        super().__init__(x, y, w, h, parent)
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges)
        self.setAcceptHoverEvents(True)
    
    def hoverEnterEvent(self, event):
        self.setBrush(QBrush(QColor(255, 200, 200)))
        super().hoverEnterEvent(event)
    
    def hoverLeaveEvent(self, event):
        self.setBrush(QBrush(QColor(200, 200, 255)))
        super().hoverLeaveEvent(event)
    
    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemPositionChange:
            print(f"位置变化: {value}")
        return super().itemChange(change, value)


class ZoomableView(QGraphicsView):
    """自定义视图 (支持缩放)"""
    
    def __init__(self, scene, parent=None):
        super().__init__(scene, parent)
        self._scale_factor = 1.0
        self.setRenderHint(QPainter.Antialiasing)
        self.setDragMode(QGraphicsView.RubberBandDrag)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
    
    def zoom_in(self):
        self.scale(1.2, 1.2)
        self._scale_factor *= 1.2
    
    def zoom_out(self):
        self.scale(1/1.2, 1/1.2)
        self._scale_factor /= 1.2
    
    def reset_zoom(self):
        self.resetTransform()
        self._scale_factor = 1.0
    
    def wheelEvent(self, event):
        if event.modifiers() & Qt.ControlModifier:
            if event.angleDelta().y() > 0:
                self.zoom_in()
            else:
                self.zoom_out()
            event.accept()
        else:
            super().wheelEvent(event)


class GraphicsViewDemo(QMainWindow):
    """图形视图演示"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("PySide6 Graphics View Demo")
        self.resize(800, 600)
        
        # 创建场景
        self._scene = QGraphicsScene(-400, -300, 800, 600, self)
        self._scene.setBackgroundBrush(QBrush(QColor(240, 240, 240)))
        
        # 创建视图
        self._view = ZoomableView(self._scene, self)
        self.setCentralWidget(self._view)
        
        # 添加图形项
        self._create_graphics_items()
        
        # 创建工具栏
        self._create_tool_bar()
    
    def add_rectangle(self):
        """添加矩形"""
        rect = DraggableRect(
            random.randint(-50, 50),
            random.randint(-50, 50),
            80, 60)
        rect.setPen(QPen(Qt.black, 2))
        rect.setBrush(QBrush(QColor(200, 200, 255)))
        self._scene.addItem(rect)
    
    def add_ellipse(self):
        """添加椭圆"""
        ellipse = self._scene.addEllipse(
            random.randint(-40, 40),
            random.randint(-40, 40),
            70, 50,
            QPen(Qt.darkGreen, 2),
            QBrush(QColor(200, 255, 200))
        )
        ellipse.setFlag(QGraphicsItem.ItemIsMovable)
        ellipse.setFlag(QGraphicsItem.ItemIsSelectable)
    
    def add_text(self):
        """添加文本"""
        text = self._scene.addText("PySide6 Graphics",
            QFont("Arial", 16, QFont.Bold))
        text.setPos(random.randint(-50, 50), random.randint(-50, 50))
        text.setDefaultTextColor(Qt.darkBlue)
        text.setFlag(QGraphicsItem.ItemIsMovable)
        text.setFlag(QGraphicsItem.ItemIsSelectable)
    
    def delete_selected(self):
        """删除选中项"""
        for item in self._scene.selectedItems():
            self._scene.removeItem(item)
            del item
    
    def clear_all(self):
        """清空所有"""
        self._scene.clear()
        self._create_graphics_items()  # 重新创建初始项目
    
    def _create_graphics_items(self):
        """创建图形项"""
        # 矩形
        rect = self._scene.addRect(-200, -150, 100, 80,
            QPen(Qt.blue, 2), QBrush(Qt.cyan))
        rect.setFlag(QGraphicsItem.ItemIsMovable)
        rect.setFlag(QGraphicsItem.ItemIsSelectable)
        rect.setToolTip("矩形 (可拖动)")
        
        # 椭圆
        ellipse = self._scene.addEllipse(-50, -150, 100, 80,
            QPen(Qt.darkGreen, 2), QBrush(Qt.green))
        ellipse.setFlag(QGraphicsItem.ItemIsMovable)
        ellipse.setFlag(QGraphicsItem.ItemIsSelectable)
        ellipse.setToolTip("椭圆")
        
        # 线条
        line = self._scene.addLine(100, -150, 200, -70,
            QPen(Qt.red, 3))
        line.setFlag(QGraphicsItem.ItemIsMovable)
        line.setFlag(QGraphicsItem.ItemIsSelectable)
        line.setToolTip("线条")
        
        # 文本
        text = self._scene.addText("PySide6 Graphics View",
            QFont("Arial", 20, QFont.Bold))
        text.setPos(-100, 50)
        text.setDefaultTextColor(Qt.darkMagenta)
        text.setFlag(QGraphicsItem.ItemIsMovable)
        text.setToolTip("文本项")
        
        # 路径 (星形)
        star_path = QPainterPath()
        for i in range(5):
            angle = -math.pi / 2 + i * 2 * math.pi / 5
            p = (30 * math.cos(angle), 30 * math.sin(angle))
            if i == 0:
                star_path.moveTo(*p)
            else:
                star_path.lineTo(*p)
            
            angle += math.pi / 5
            inner = (30 * 0.4 * math.cos(angle), 30 * 0.4 * math.sin(angle))
            star_path.lineTo(*inner)
        star_path.closeSubpath()
        
        star = self._scene.addPath(star_path,
            QPen(Qt.darkYellow, 2), QBrush(Qt.yellow))
        star.setPos(-200, 100)
        star.setFlag(QGraphicsItem.ItemIsMovable)
        star.setFlag(QGraphicsItem.ItemIsSelectable)
        star.setToolTip("星形路径")
        
        # 自定义可拖动矩形
        draggable = DraggableRect(100, 50, 100, 80)
        draggable.setPen(QPen(Qt.black, 2))
        draggable.setBrush(QBrush(QColor(200, 200, 255)))
        draggable.setToolTip("悬停变色的矩形")
        self._scene.addItem(draggable)
        
        # 图形组
        group = QGraphicsItemGroup()
        group_rect = QGraphicsRectItem(-20, -15, 40, 30)
        group_rect.setBrush(Qt.lightGray)
        group_ellipse = QGraphicsEllipseItem(-10, -10, 20, 20)
        group_ellipse.setBrush(Qt.darkGray)
        group.addToGroup(group_rect)
        group.addToGroup(group_ellipse)
        group.setPos(0, -50)
        group.setFlag(QGraphicsItem.ItemIsMovable)
        group.setFlag(QGraphicsItem.ItemIsSelectable)
        group.setToolTip("图形组 (一起移动)")
        self._scene.addItem(group)
        
        # 说明文本
        info = self._scene.addText(
            "操作说明:\n"
            "• 拖动图形项移动\n"
            "• Ctrl+滚轮缩放\n"
            "• 点击选择，拖动框选\n"
            "• 使用工具栏按钮添加/删除",
            QFont("Arial", 10))
        info.setPos(-380, 150)
    
    def _create_tool_bar(self):
        """创建工具栏"""
        tool_bar = self.addToolBar("工具")
        
        tool_bar.addAction("添加矩形", self.add_rectangle)
        tool_bar.addAction("添加椭圆", self.add_ellipse)
        tool_bar.addAction("添加文本", self.add_text)
        tool_bar.addSeparator()
        tool_bar.addAction("删除选中", self.delete_selected)
        tool_bar.addAction("清空", self.clear_all)
        tool_bar.addSeparator()
        tool_bar.addAction("放大", self._view.zoom_in)
        tool_bar.addAction("缩小", self._view.zoom_out)
        tool_bar.addAction("重置", self._view.reset_zoom)


def main():
    app = QApplication(sys.argv)
    
    print("=== PySide6 图形视图框架示例 ===\n")
    print("功能:")
    print("- 拖动图形项移动")
    print("- Ctrl+滚轮缩放视图")
    print("- 点击选择，拖动框选多个")
    print("- 工具栏添加/删除图形项\n")
    
    demo = GraphicsViewDemo()
    demo.show()
    
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
