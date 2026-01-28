#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PySide6 基础控件示例

Qt Widgets 提供丰富的桌面UI控件：
- 按钮类: QPushButton, QCheckBox, QRadioButton
- 输入类: QLineEdit, QTextEdit, QSpinBox, QComboBox
- 显示类: QLabel, QProgressBar
- 容器类: QGroupBox, QTabWidget

官方文档: https://doc.qt.io/qtforpython/PySide6/QtWidgets/index.html
"""

import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QGroupBox, QLabel, QPushButton, QCheckBox, QRadioButton,
    QLineEdit, QTextEdit, QSpinBox, QDoubleSpinBox, QSlider,
    QProgressBar, QComboBox, QListWidget, QDateEdit, QTimeEdit, QDial,
    QStyle
)
from PySide6.QtCore import Qt, QDate, QTime


class BasicWidgetsDemo(QWidget):
    """基础控件演示"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("PySide6 Basic Widgets Demo")
        self.resize(700, 600)
        
        main_layout = QVBoxLayout(self)
        
        # 按钮组
        main_layout.addWidget(self.create_button_group())
        
        # 输入组
        main_layout.addWidget(self.create_input_group())
        
        # 选择组
        main_layout.addWidget(self.create_selection_group())
        
        # 数值组
        main_layout.addWidget(self.create_numeric_group())
    
    def create_button_group(self):
        """创建按钮组"""
        group = QGroupBox("按钮控件", self)
        layout = QHBoxLayout(group)
        
        # 普通按钮
        normal_btn = QPushButton("普通按钮", self)
        normal_btn.clicked.connect(lambda: print("普通按钮被点击"))
        
        # 可选中按钮
        toggle_btn = QPushButton("可选中按钮", self)
        toggle_btn.setCheckable(True)
        toggle_btn.toggled.connect(lambda checked: print(f"按钮选中状态: {checked}"))
        
        # 图标按钮
        icon_btn = QPushButton("带图标", self)
        icon_btn.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_DialogOkButton))
        
        # 复选框
        checkbox = QCheckBox("复选框", self)
        checkbox.stateChanged.connect(lambda state: print(f"复选框状态: {state}"))
        
        # 三态复选框
        tri_state_check = QCheckBox("三态", self)
        tri_state_check.setTristate(True)
        
        # 单选按钮组
        radio_group = QWidget(self)
        radio_layout = QHBoxLayout(radio_group)
        radio_layout.setContentsMargins(0, 0, 0, 0)
        radio1 = QRadioButton("选项A", self)
        radio2 = QRadioButton("选项B", self)
        radio1.setChecked(True)
        radio_layout.addWidget(radio1)
        radio_layout.addWidget(radio2)
        
        layout.addWidget(normal_btn)
        layout.addWidget(toggle_btn)
        layout.addWidget(icon_btn)
        layout.addWidget(checkbox)
        layout.addWidget(tri_state_check)
        layout.addWidget(radio_group)
        
        return group
    
    def create_input_group(self):
        """创建输入组"""
        group = QGroupBox("输入控件", self)
        layout = QGridLayout(group)
        
        # 单行输入
        layout.addWidget(QLabel("单行输入:"), 0, 0)
        line_edit = QLineEdit(self)
        line_edit.setPlaceholderText("请输入文字...")
        line_edit.textChanged.connect(lambda text: print(f"输入: {text}"))
        layout.addWidget(line_edit, 0, 1)
        
        # 密码输入
        layout.addWidget(QLabel("密码输入:"), 1, 0)
        password_edit = QLineEdit(self)
        password_edit.setEchoMode(QLineEdit.Password)
        layout.addWidget(password_edit, 1, 1)
        
        # 只读输入
        layout.addWidget(QLabel("只读:"), 2, 0)
        read_only_edit = QLineEdit("不可编辑", self)
        read_only_edit.setReadOnly(True)
        layout.addWidget(read_only_edit, 2, 1)
        
        # 多行文本
        layout.addWidget(QLabel("多行文本:"), 3, 0)
        text_edit = QTextEdit(self)
        text_edit.setPlaceholderText("支持多行和富文本...")
        text_edit.setMaximumHeight(80)
        layout.addWidget(text_edit, 3, 1)
        
        return group
    
    def create_selection_group(self):
        """创建选择组"""
        group = QGroupBox("选择控件", self)
        layout = QGridLayout(group)
        
        # 下拉框
        layout.addWidget(QLabel("下拉框:"), 0, 0)
        combo = QComboBox(self)
        combo.addItems(["选项一", "选项二", "选项三"])
        combo.currentIndexChanged.connect(lambda idx: print(f"选择: {combo.currentText()}"))
        layout.addWidget(combo, 0, 1)
        
        # 可编辑下拉框
        layout.addWidget(QLabel("可编辑:"), 1, 0)
        editable_combo = QComboBox(self)
        editable_combo.setEditable(True)
        editable_combo.addItems(["预设1", "预设2"])
        layout.addWidget(editable_combo, 1, 1)
        
        # 日期选择
        layout.addWidget(QLabel("日期:"), 2, 0)
        date_edit = QDateEdit(QDate.currentDate(), self)
        date_edit.setCalendarPopup(True)
        layout.addWidget(date_edit, 2, 1)
        
        # 时间选择
        layout.addWidget(QLabel("时间:"), 3, 0)
        time_edit = QTimeEdit(QTime.currentTime(), self)
        layout.addWidget(time_edit, 3, 1)
        
        return group
    
    def create_numeric_group(self):
        """创建数值组"""
        group = QGroupBox("数值控件", self)
        layout = QGridLayout(group)
        
        # 整数微调框
        layout.addWidget(QLabel("整数:"), 0, 0)
        spin_box = QSpinBox(self)
        spin_box.setRange(0, 100)
        spin_box.setValue(50)
        spin_box.setSuffix(" 个")
        layout.addWidget(spin_box, 0, 1)
        
        # 浮点微调框
        layout.addWidget(QLabel("浮点数:"), 1, 0)
        double_spin_box = QDoubleSpinBox(self)
        double_spin_box.setRange(0.0, 10.0)
        double_spin_box.setDecimals(2)
        double_spin_box.setSingleStep(0.1)
        layout.addWidget(double_spin_box, 1, 1)
        
        # 滑块
        layout.addWidget(QLabel("滑块:"), 2, 0)
        slider = QSlider(Qt.Horizontal, self)
        slider.setRange(0, 100)
        slider.setValue(50)
        layout.addWidget(slider, 2, 1)
        
        # 进度条
        layout.addWidget(QLabel("进度:"), 3, 0)
        progress_bar = QProgressBar(self)
        progress_bar.setRange(0, 100)
        progress_bar.setValue(75)
        layout.addWidget(progress_bar, 3, 1)
        
        # 连接滑块和进度条
        slider.valueChanged.connect(progress_bar.setValue)
        
        # 旋钮
        layout.addWidget(QLabel("旋钮:"), 4, 0)
        dial = QDial(self)
        dial.setRange(0, 100)
        dial.setMaximumSize(60, 60)
        dial.valueChanged.connect(slider.setValue)
        layout.addWidget(dial, 4, 1, Qt.AlignLeft)
        
        return group


def main():
    app = QApplication(sys.argv)
    
    print("=== PySide6 基础控件示例 ===")
    print("控制台会显示控件交互信息\n")
    
    demo = BasicWidgetsDemo()
    demo.show()
    
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
