#!/usr/bin/env clojure -M
;; PySide6 自定义控件示例 (Clojure + libpython-clj)
;; 展示了三种自定义控件:
;; 1. 圆形进度条 (重写 paintEvent)
;; 2. 开关按钮 (带动画)
;; 3. 星级评分 (鼠标交互)
;; 注意：macOS 需要使用 -XstartOnFirstThread JVM 参数运行

(require '[libpython-clj2.python :as py])

(py/initialize!)

(defn demonstrate-custom-widgets
  "演示自定义控件"
  []
  (println "\n=== 创建自定义控件 GUI 窗口 ===")
  
  (py/run-simple-string "
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QSlider
)
from PySide6.QtCore import Qt, QTimer, QPropertyAnimation, Property
from PySide6.QtGui import QPainter, QPen, QColor, QFont, QPainterPath
import math
import sys

# ========== 自定义圆形进度条 ==========
class CircularProgress(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._value = 0
        self._maximum = 100
        self.setMinimumSize(100, 100)
    
    def value(self):
        return self._value
    
    def setValue(self, value):
        if self._value != value:
            self._value = max(0, min(value, self._maximum))
            self.update()
    
    def maximum(self):
        return self._maximum
    
    def setMaximum(self, maximum):
        self._maximum = maximum
        self.update()
    
    def sizeHint(self):
        from PySide6.QtCore import QSize
        return QSize(120, 120)
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        side = min(self.width(), self.height())
        rect_x = (self.width() - side) / 2.0 + 10
        rect_y = (self.height() - side) / 2.0 + 10
        rect_w = side - 20
        rect_h = side - 20
        
        from PySide6.QtCore import QRectF
        rect = QRectF(rect_x, rect_y, rect_w, rect_h)
        
        # 背景圆
        painter.setPen(QPen(QColor(200, 200, 200), 8))
        painter.drawArc(rect, 0, 360 * 16)
        
        # 进度弧
        span_angle = -360 * 16 * self._value / self._maximum
        painter.setPen(QPen(QColor(0, 150, 255), 8, Qt.SolidLine, Qt.RoundCap))
        painter.drawArc(rect, 90 * 16, int(span_angle))
        
        # 中心文字
        painter.setPen(Qt.black)
        font = QFont('Arial', int(side / 5))
        font.setBold(True)
        painter.setFont(font)
        painter.drawText(rect, Qt.AlignCenter, f'{int(self._value * 100 / self._maximum)}%')


# ========== 自定义开关按钮 ==========
class ToggleSwitch(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._checked = False
        self._handle_position = 0.0
        self.setFixedSize(60, 30)
        self.setCursor(Qt.PointingHandCursor)
        
        self._animation = QPropertyAnimation(self, b'handlePosition')
        self._animation.setDuration(150)
    
    def isChecked(self):
        return self._checked
    
    def setChecked(self, checked):
        if self._checked != checked:
            self._checked = checked
            self._animation.setStartValue(self._handle_position)
            self._animation.setEndValue(1.0 if checked else 0.0)
            self._animation.start()
            # 触发信号
            self.toggled.emit(checked)
    
    toggled = None  # 将在下面创建
    
    def handlePosition(self):
        return self._handle_position
    
    def setHandlePosition(self, position):
        self._handle_position = position
        self.update()
    
    # 定义属性
    handlePosition = Property(float, handlePosition, setHandlePosition)
    
    def sizeHint(self):
        from PySide6.QtCore import QSize
        return QSize(60, 30)
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # 背景
        if self._checked:
            bg_color = QColor(0, 200, 100).lighter(int(100 + (1 - self._handle_position) * 50))
        else:
            bg_color = QColor(200, 200, 200)
        painter.setBrush(bg_color)
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(self.rect(), self.height() / 2, self.height() / 2)
        
        # 滑块
        handle_x = 3 + self._handle_position * (self.width() - self.height() - 6 + 6)
        from PySide6.QtCore import QRectF
        handle_rect = QRectF(handle_x, 3, self.height() - 6, self.height() - 6)
        painter.setBrush(Qt.white)
        painter.drawEllipse(handle_rect)
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.setChecked(not self._checked)

# 创建信号
from PySide6.QtCore import pyqtSignal
ToggleSwitch.toggled = pyqtSignal(bool)


# ========== 自定义评分控件 ==========
class StarRating(QWidget):
    ratingChanged = None  # 将在下面创建
    
    def __init__(self, max_stars=5, parent=None):
        super().__init__(parent)
        self._rating = 0
        self._max_stars = max_stars
        self._hover_star = -1
        self.setMouseTracking(True)
        self.setMinimumSize(max_stars * 30, 30)
    
    def rating(self):
        return self._rating
    
    def setRating(self, rating):
        if self._rating != rating:
            self._rating = max(0, min(rating, self._max_stars))
            self.ratingChanged.emit(self._rating)
            self.update()
    
    def maxStars(self):
        return self._max_stars
    
    def sizeHint(self):
        from PySide6.QtCore import QSize
        return QSize(self._max_stars * 30, 30)
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        star_size = min(self.width() // self._max_stars, self.height()) - 4
        
        for i in range(self._max_stars):
            from PySide6.QtCore import QRectF
            star_rect = QRectF(i * (star_size + 4) + 2, 2, star_size, star_size)
            filled = (i < self._rating) or (self._hover_star >= 0 and i <= self._hover_star)
            self.draw_star(painter, star_rect, filled)
    
    def draw_star(self, painter, rect, filled):
        path = QPainterPath()
        center = rect.center()
        r = rect.width() / 2
        
        for i in range(5):
            angle = -math.pi / 2 + i * 2 * math.pi / 5
            p_x = center.x() + r * math.cos(angle)
            p_y = center.y() + r * math.sin(angle)
            if i == 0:
                path.moveTo(p_x, p_y)
            else:
                path.lineTo(p_x, p_y)
            
            angle += math.pi / 5
            inner_x = center.x() + r * 0.4 * math.cos(angle)
            inner_y = center.y() + r * 0.4 * math.sin(angle)
            path.lineTo(inner_x, inner_y)
        
        path.closeSubpath()
        painter.setPen(QPen(Qt.darkYellow, 1))
        painter.setBrush(Qt.yellow if filled else Qt.white)
        painter.drawPath(path)
    
    def mouseMoveEvent(self, event):
        star_size = min(self.width() // self._max_stars, self.height()) - 4
        self._hover_star = int(event.position().x() / (star_size + 4))
        self.update()
    
    def leaveEvent(self, event):
        self._hover_star = -1
        self.update()
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            star_size = min(self.width() // self._max_stars, self.height()) - 4
            clicked_star = int(event.position().x() / (star_size + 4))
            self.setRating(clicked_star + 1)

# 创建信号
StarRating.ratingChanged = pyqtSignal(int)


# ========== 主窗口 ==========
class CustomWidgetsDemo(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('PySide6 Custom Widgets Demo (Clojure)')
        self.resize(400, 450)
        
        layout = QVBoxLayout(self)
        
        # 圆形进度条
        layout.addWidget(QLabel('圆形进度条:'))
        self.progress = CircularProgress(self)
        layout.addWidget(self.progress, 0, Qt.AlignCenter)
        
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0, 100)
        self.slider.valueChanged.connect(self.progress.setValue)
        layout.addWidget(self.slider)
        
        # 自动递增定时器
        self.timer = QTimer()
        self.timer.timeout.connect(self.auto_increment)
        self.timer.start(100)
        
        layout.addSpacing(20)
        
        # 开关按钮
        layout.addWidget(QLabel('开关按钮:'))
        switch_layout = QHBoxLayout()
        self.toggle = ToggleSwitch(self)
        self.status_label = QLabel('关闭', self)
        self.toggle.toggled.connect(self.update_status)
        switch_layout.addWidget(self.toggle)
        switch_layout.addWidget(self.status_label)
        switch_layout.addStretch()
        layout.addLayout(switch_layout)
        
        layout.addSpacing(20)
        
        # 星级评分
        layout.addWidget(QLabel('星级评分 (点击选择):'))
        rating_layout = QHBoxLayout()
        self.rating = StarRating(5, self)
        self.rating_label = QLabel('0 星', self)
        self.rating.ratingChanged.connect(self.update_rating)
        rating_layout.addWidget(self.rating)
        rating_layout.addWidget(self.rating_label)
        rating_layout.addStretch()
        layout.addLayout(rating_layout)
        
        layout.addStretch()
    
    def auto_increment(self):
        new_value = (self.slider.value() + 1) % 101
        self.slider.setValue(new_value)
    
    def update_status(self, checked):
        self.status_label.setText('开启' if checked else '关闭')
    
    def update_rating(self, rating):
        self.rating_label.setText(f'{rating} 星')


# 创建应用
print('=== PySide6 自定义控件示例 (Clojure) ===')
print('展示了三种自定义控件:')
print('1. 圆形进度条 (重写 paintEvent)')
print('2. 开关按钮 (带动画)')
print('3. 星级评分 (鼠标交互)')
print()

app = QApplication(sys.argv)
demo = CustomWidgetsDemo()
demo.show()
print('窗口已显示，请在 GUI 中操作自定义控件')
print('（关闭窗口退出程序）')
app.exec()
")
  
  (println "\n演示完成"))

(defn -main
  [& args]
  (println "=== PySide6 自定义控件示例 (Clojure) ===")
  (println "注意: macOS 必须使用 -XstartOnFirstThread JVM 参数")
  (println "      可通过 clojure -M:run 运行")
  
  (demonstrate-custom-widgets)
  
  (println "\n=== 完成 ==="))

(-main)
