def run_block_1():
    exec(r"""
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QPushButton, QCheckBox, QRadioButton,
    QLineEdit, QTextEdit, QProgressBar, QSlider, QSpinBox,
    QGroupBox
)
from PySide6.QtCore import Qt
import sys

# 创建应用
app = QApplication([])

# 创建主窗口
window = QWidget()
window.setWindowTitle('PySide6 基础控件演示 (Clojure)')
window.resize(600, 500)

# 主布局
main_layout = QVBoxLayout(window)

# ===== 按钮组 =====
btn_group = QGroupBox('按钮控件')
btn_layout = QHBoxLayout(btn_group)

# 普通按钮
normal_btn = QPushButton('普通按钮')
normal_btn.clicked.connect(lambda: print('普通按钮被点击'))
btn_layout.addWidget(normal_btn)

# 可选中按钮
toggle_btn = QPushButton('可选中按钮')
toggle_btn.setCheckable(True)
toggle_btn.toggled.connect(lambda checked: print(f'按钮选中状态: {checked}'))
btn_layout.addWidget(toggle_btn)

# 复选框
checkbox = QCheckBox('复选框')
checkbox.stateChanged.connect(lambda state: print(f'复选框状态: {state}'))
btn_layout.addWidget(checkbox)

# 单选按钮
radio1 = QRadioButton('选项A')
radio2 = QRadioButton('选项B')
radio1.setChecked(True)
radio_layout = QHBoxLayout()
radio_layout.addWidget(radio1)
radio_layout.addWidget(radio2)
btn_layout.addLayout(radio_layout)

main_layout.addWidget(btn_group)

# ===== 输入组 =====
input_group = QGroupBox('输入控件')
input_layout = QGridLayout(input_group)

# 单行输入
input_layout.addWidget(QLabel('单行输入:'), 0, 0)
line_edit = QLineEdit()
line_edit.setPlaceholderText('请输入文字...')
line_edit.textChanged.connect(lambda text: print(f'输入: {text}'))
input_layout.addWidget(line_edit, 0, 1)

# 多行输入
input_layout.addWidget(QLabel('多行输入:'), 1, 0)
text_edit = QTextEdit()
text_edit.setPlaceholderText('请输入多行文字...')
text_edit.setMaximumHeight(80)
input_layout.addWidget(text_edit, 1, 1)

main_layout.addWidget(input_group)

# ===== 数值组 =====
num_group = QGroupBox('数值控件')
num_layout = QHBoxLayout(num_group)

# 进度条
progress = QProgressBar()
progress.setRange(0, 100)
progress.setValue(50)
num_layout.addWidget(progress)

# 滑块
slider = QSlider(Qt.Horizontal)
slider.setRange(0, 100)
slider.valueChanged.connect(lambda value: progress.setValue(value))
num_layout.addWidget(slider)

# 数字输入
spinbox = QSpinBox()
spinbox.setRange(0, 100)
spinbox.setValue(25)
spinbox.valueChanged.connect(lambda value: slider.setValue(value))
num_layout.addWidget(spinbox)

main_layout.addWidget(num_group)

# 添加弹性空间
main_layout.addStretch()

# 显示窗口
window.show()
print('窗口已显示，请在 GUI 中操作控件')
print('（关闭窗口退出程序）')

# 运行事件循环
app.exec()
""", globals())
