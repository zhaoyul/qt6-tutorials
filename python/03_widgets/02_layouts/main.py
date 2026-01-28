#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PySide6 布局管理示例

布局管理器自动排列控件：
- QVBoxLayout: 垂直布局
- QHBoxLayout: 水平布局
- QGridLayout: 网格布局
- QFormLayout: 表单布局
- QStackedLayout: 堆叠布局

重要概念：
- 伸缩因子 (Stretch)
- 间距 (Spacing)
- 边距 (Margin)
- 尺寸策略 (Size Policy)

官方文档: https://doc.qt.io/qtforpython/PySide6/QtWidgets/index.html
"""

import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QFormLayout, QStackedLayout, QPushButton, QLabel, QLineEdit,
    QTextEdit, QGroupBox, QTabWidget, QSplitter, QFrame, QSizePolicy
)
from PySide6.QtCore import Qt, QSize


def create_color_label(text, color):
    """创建带颜色背景的标签 (便于观察布局)"""
    label = QLabel(text)
    label.setStyleSheet(f"background-color: {color}; padding: 10px; border: 1px solid gray;")
    label.setAlignment(Qt.AlignCenter)
    return label


def create_vbox_demo():
    """垂直布局示例"""
    widget = QWidget()
    layout = QVBoxLayout(widget)
    
    layout.addWidget(create_color_label("Item 1", "#ffcccc"))
    layout.addWidget(create_color_label("Item 2", "#ccffcc"))
    layout.addWidget(create_color_label("Item 3 (Stretch 2)", "#ccccff"))
    
    # 设置伸缩因子
    layout.setStretch(2, 2)  # 第三个控件占2份
    
    # 添加弹性空间
    layout.addStretch(1)
    
    layout.addWidget(create_color_label("Bottom Item", "#ffccff"))
    
    return widget


def create_hbox_demo():
    """水平布局示例"""
    widget = QWidget()
    layout = QHBoxLayout(widget)
    
    layout.addWidget(create_color_label("Left", "#ffcccc"))
    layout.addStretch(1)  # 中间弹性空间
    layout.addWidget(create_color_label("Center", "#ccffcc"))
    layout.addStretch(1)
    layout.addWidget(create_color_label("Right", "#ccccff"))
    
    return widget


def create_grid_demo():
    """网格布局示例"""
    widget = QWidget()
    layout = QGridLayout(widget)
    
    # 基本网格
    layout.addWidget(create_color_label("(0,0)", "#ffcccc"), 0, 0)
    layout.addWidget(create_color_label("(0,1)", "#ccffcc"), 0, 1)
    layout.addWidget(create_color_label("(0,2)", "#ccccff"), 0, 2)
    
    layout.addWidget(create_color_label("(1,0)", "#ffffcc"), 1, 0)
    layout.addWidget(create_color_label("(1,1-2) 跨列", "#ffccff"), 1, 1, 1, 2)  # 跨2列
    
    layout.addWidget(create_color_label("(2-3,0) 跨行", "#ccffff"), 2, 0, 2, 1)  # 跨2行
    layout.addWidget(create_color_label("(2,1)", "#ffd700"), 2, 1)
    layout.addWidget(create_color_label("(2,2)", "#98fb98"), 2, 2)
    layout.addWidget(create_color_label("(3,1)", "#dda0dd"), 3, 1)
    layout.addWidget(create_color_label("(3,2)", "#f0e68c"), 3, 2)
    
    # 设置列伸缩
    layout.setColumnStretch(1, 1)
    layout.setColumnStretch(2, 2)
    
    return widget


def create_form_demo():
    """表单布局示例"""
    widget = QWidget()
    layout = QFormLayout(widget)
    
    layout.addRow("用户名:", QLineEdit())
    layout.addRow("密码:", QLineEdit())
    layout.addRow("邮箱:", QLineEdit())
    
    bio = QTextEdit()
    bio.setMaximumHeight(80)
    layout.addRow("简介:", bio)
    
    # 表单布局选项
    layout.setLabelAlignment(Qt.AlignRight)
    layout.setFormAlignment(Qt.AlignLeft | Qt.AlignTop)
    
    return widget


def create_nested_demo():
    """嵌套布局示例"""
    widget = QWidget()
    main_layout = QVBoxLayout(widget)
    
    # 顶部水平布局
    top_layout = QHBoxLayout()
    top_layout.addWidget(create_color_label("Logo", "#ffcccc"))
    top_layout.addStretch()
    top_layout.addWidget(QPushButton("按钮1"))
    top_layout.addWidget(QPushButton("按钮2"))
    main_layout.addLayout(top_layout)
    
    # 中间区域
    middle_layout = QHBoxLayout()
    
    # 左侧菜单
    left_layout = QVBoxLayout()
    left_layout.addWidget(QPushButton("菜单1"))
    left_layout.addWidget(QPushButton("菜单2"))
    left_layout.addWidget(QPushButton("菜单3"))
    left_layout.addStretch()
    middle_layout.addLayout(left_layout)
    
    # 右侧内容
    content = QTextEdit("内容区域")
    middle_layout.addWidget(content, 1)
    
    main_layout.addLayout(middle_layout, 1)
    
    # 底部状态栏
    main_layout.addWidget(create_color_label("状态栏", "#cccccc"))
    
    return widget


def create_splitter_demo():
    """分割器示例"""
    splitter = QSplitter(Qt.Horizontal)
    
    left = QTextEdit("左侧面板\n\n拖动分割线调整大小")
    middle = QTextEdit("中间面板")
    right = QTextEdit("右侧面板")
    
    splitter.addWidget(left)
    splitter.addWidget(middle)
    splitter.addWidget(right)
    
    # 设置初始大小比例
    splitter.setSizes([100, 200, 100])
    
    # 设置手柄宽度
    splitter.setHandleWidth(5)
    
    return splitter


def create_size_policy_demo():
    """尺寸策略示例"""
    widget = QWidget()
    layout = QVBoxLayout(widget)
    
    # Fixed: 固定大小
    fixed_btn = QPushButton("Fixed (固定大小)")
    fixed_btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
    layout.addWidget(fixed_btn)
    
    # Minimum: 最小大小
    min_btn = QPushButton("Minimum")
    min_btn.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
    layout.addWidget(min_btn)
    
    # Expanding: 尽量扩展
    expand_btn = QPushButton("Expanding (扩展)")
    expand_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    layout.addWidget(expand_btn)
    
    # 说明
    info = QLabel(
        "尺寸策略:\n"
        "• Fixed: 固定为sizeHint\n"
        "• Minimum: 最小为sizeHint，可以扩大\n"
        "• Maximum: 最大为sizeHint，可以缩小\n"
        "• Preferred: 最佳为sizeHint，可调整\n"
        "• Expanding: 尽量扩展\n"
        "• Ignored: 忽略sizeHint"
    )
    info.setStyleSheet("background-color: #f0f0f0; padding: 10px;")
    layout.addWidget(info)
    
    return widget


def main():
    app = QApplication(sys.argv)
    
    print("=== PySide6 布局管理示例 ===\n")
    
    tab_widget = QTabWidget()
    tab_widget.setWindowTitle("PySide6 Layouts Demo")
    tab_widget.resize(600, 500)
    
    tab_widget.addTab(create_vbox_demo(), "VBox 垂直")
    tab_widget.addTab(create_hbox_demo(), "HBox 水平")
    tab_widget.addTab(create_grid_demo(), "Grid 网格")
    tab_widget.addTab(create_form_demo(), "Form 表单")
    tab_widget.addTab(create_nested_demo(), "嵌套布局")
    tab_widget.addTab(create_splitter_demo(), "分割器")
    tab_widget.addTab(create_size_policy_demo(), "尺寸策略")
    
    tab_widget.show()
    
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
