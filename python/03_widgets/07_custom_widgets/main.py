#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PySide6 自定义控件示例

自定义控件的方式：
1. 组合现有控件
2. 继承 QWidget 并重写 paintEvent
3. 继承现有控件并修改行为

关键重写方法：
- paintEvent(): 绘制
- sizeHint(): 建议大小
- minimumSizeHint(): 最小大小
- mousePressEvent() 等: 事件处理

官方文档: https://doc.qt.io/qtforpython/PySide6/QtWidgets/index.html
"""

import sys
import math
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QSlider, QLabel
)
from PySide6.QtCore import Qt, QPropertyAnimation, Property, Signal, QSize
from PySide6.QtGui import QPainter, QPen, QBrush, QColor, QFont, QPainterPath


class CircularProgress(QWidget):
    """自定义圆形进度条"""
    
    valueChanged = Signal(int)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._value = 0
        self._maximum = 100
        self.setMinimumSize(100, 100)
    
    @Property(int, notify=valueChanged)
    def value(self):
        return self._value
    
    @value.setter
    def value(self, val):
        if self._value != val:
            self._value = max(0, min(val, self._maximum))
            self.valueChanged.emit(self._value)
            self.update()
    
    def setValue(self, val):
        """兼容 QSlider 的 setValue 接口"""
        self.value = val
    
    @Property(int)
    def maximum(self):
        return self._maximum
    
    @maximum.setter
    def maximum(self, val):
        self._maximum = val
        self.update()
    
    def sizeHint(self):
        return QSize(120, 120)
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        side = min(self.width(), self.height())
        rect = (
            (self.width() - side) / 2.0 + 10,
            (self.height() - side) / 2.0 + 10,
            side - 20, side - 20
        )
        
        # 背景圆
        painter.setPen(QPen(QColor(200, 200, 200), 8))
        painter.drawArc(*[int(x) for x in rect], 0, 360 * 16)
        
        # 进度弧
        span_angle = -360 * 16 * self._value // self._maximum
        painter.setPen(QPen(QColor(0, 150, 255), 8, Qt.SolidLine, Qt.RoundCap))
        painter.drawArc(*[int(x) for x in rect], 90 * 16, span_angle)
        
        # 中心文字
        painter.setPen(Qt.black)
        painter.setFont(QFont("Arial", side // 5, QFont.Bold))
        painter.drawText(self.rect(), Qt.AlignCenter,
                        f"{self._value * 100 // self._maximum}%")


class ToggleSwitch(QWidget):
    """自定义开关按钮"""
    
    toggled = Signal(bool)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._checked = False
        self._handle_position = 0.0
        self.setFixedSize(60, 30)
        self.setCursor(Qt.PointingHandCursor)
        
        self._animation = QPropertyAnimation(self, b"handlePosition", self)
        self._animation.setDuration(150)
    
    @Property(bool, notify=toggled)
    def checked(self):
        return self._checked
    
    @checked.setter
    def checked(self, val):
        if self._checked != val:
            self._checked = val
            self._animation.setStartValue(self._handle_position)
            self._animation.setEndValue(1.0 if val else 0.0)
            self._animation.start()
            self.toggled.emit(val)
    
    @Property(float)
    def handlePosition(self):
        return self._handle_position
    
    @handlePosition.setter
    def handlePosition(self, pos):
        self._handle_position = pos
        self.update()
    
    def sizeHint(self):
        return QSize(60, 30)
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # 背景
        if self._checked:
            bg_color = QColor(0, 200, 100).lighter(100 + int((1 - self._handle_position) * 50))
        else:
            bg_color = QColor(200, 200, 200)
        painter.setBrush(bg_color)
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(self.rect(), self.height() // 2, self.height() // 2)
        
        # 滑块
        handle_x = 3 + self._handle_position * (self.width() - self.height())
        handle_rect = (handle_x, 3, self.height() - 6, self.height() - 6)
        painter.setBrush(Qt.white)
        painter.drawEllipse(*[int(x) for x in handle_rect])
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.checked = not self._checked


class StarRating(QWidget):
    """自定义评分控件"""
    
    ratingChanged = Signal(int)
    
    def __init__(self, max_stars=5, parent=None):
        super().__init__(parent)
        self._rating = 0
        self._max_stars = max_stars
        self._hover_star = -1
        self.setMouseTracking(True)
        self.setMinimumSize(max_stars * 30, 30)
    
    @Property(int, notify=ratingChanged)
    def rating(self):
        return self._rating
    
    @rating.setter
    def rating(self, val):
        if self._rating != val:
            self._rating = max(0, min(val, self._max_stars))
            self.ratingChanged.emit(self._rating)
            self.update()
    
    @Property(int)
    def maxStars(self):
        return self._max_stars
    
    def sizeHint(self):
        return QSize(self._max_stars * 30, 30)
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        star_size = min(self.width() // self._max_stars, self.height()) - 4
        
        for i in range(self._max_stars):
            star_rect = (i * (star_size + 4) + 2, 2, star_size, star_size)
            filled = (i < self._rating) or (self._hover_star >= 0 and i <= self._hover_star)
            self._draw_star(painter, star_rect, filled)
    
    def mouseMoveEvent(self, event):
        star_size = min(self.width() // self._max_stars, self.height()) - 4
        self._hover_star = event.position().x() // (star_size + 4)
        self.update()
    
    def leaveEvent(self, event):
        self._hover_star = -1
        self.update()
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            star_size = min(self.width() // self._max_stars, self.height()) - 4
            clicked_star = int(event.position().x() // (star_size + 4))
            self.rating = clicked_star + 1
    
    def _draw_star(self, painter, rect, filled):
        path = QPainterPath()
        center = (rect[0] + rect[2] / 2, rect[1] + rect[3] / 2)
        r = rect[2] / 2
        
        for i in range(5):
            angle = -math.pi / 2 + i * 2 * math.pi / 5
            p = (center[0] + r * math.cos(angle), center[1] + r * math.sin(angle))
            if i == 0:
                path.moveTo(*p)
            else:
                path.lineTo(*p)
            
            angle += math.pi / 5
            inner = (center[0] + r * 0.4 * math.cos(angle),
                    center[1] + r * 0.4 * math.sin(angle))
            path.lineTo(*inner)
        path.closeSubpath()
        
        painter.setPen(QPen(Qt.darkYellow, 1))
        painter.setBrush(Qt.yellow if filled else Qt.white)
        painter.drawPath(path)


class CustomWidgetsDemo(QWidget):
    """自定义控件演示"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("PySide6 Custom Widgets Demo")
        self.resize(400, 400)
        
        layout = QVBoxLayout(self)
        
        # 圆形进度条
        layout.addWidget(QLabel("圆形进度条:"))
        progress = CircularProgress(self)
        layout.addWidget(progress, 0, Qt.AlignCenter)
        
        slider = QSlider(Qt.Horizontal, self)
        slider.setRange(0, 100)
        slider.valueChanged.connect(progress.setValue)
        layout.addWidget(slider)
        
        # 自动递增
        from PySide6.QtCore import QTimer
        timer = QTimer(self)
        timer.timeout.connect(lambda: slider.setValue((slider.value() + 1) % 101))
        timer.start(100)
        
        layout.addSpacing(20)
        
        # 开关按钮
        layout.addWidget(QLabel("开关按钮:"))
        switch_layout = QHBoxLayout()
        toggle = ToggleSwitch(self)
        status_label = QLabel("关闭", self)
        toggle.toggled.connect(lambda checked: status_label.setText("开启" if checked else "关闭"))
        switch_layout.addWidget(toggle)
        switch_layout.addWidget(status_label)
        switch_layout.addStretch()
        layout.addLayout(switch_layout)
        
        layout.addSpacing(20)
        
        # 星级评分
        layout.addWidget(QLabel("星级评分 (点击选择):"))
        rating_layout = QHBoxLayout()
        rating = StarRating(5, self)
        rating_label = QLabel("0 星", self)
        rating.ratingChanged.connect(lambda r: rating_label.setText(f"{r} 星"))
        rating_layout.addWidget(rating)
        rating_layout.addWidget(rating_label)
        rating_layout.addStretch()
        layout.addLayout(rating_layout)
        
        layout.addStretch()


def main():
    app = QApplication(sys.argv)
    
    print("=== PySide6 自定义控件示例 ===\n")
    print("展示了三种自定义控件:")
    print("1. 圆形进度条 (重写 paintEvent)")
    print("2. 开关按钮 (带动画)")
    print("3. 星级评分 (鼠标交互)\n")
    
    demo = CustomWidgetsDemo()
    demo.show()
    
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
