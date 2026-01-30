def run_block_1():
    exec(r"""
from PySide6.QtCore import QCoreApplication
import sys
if not QCoreApplication.instance():
    _app = QCoreApplication(sys.argv)
""", globals())

def run_block_2():
    exec(r"""
from PySide6.QtGui import QGuiApplication
from PySide6.QtCore import QCoreApplication
import sys

# 注意：需要 QGuiApplication 才能获取屏幕信息
# 这里仅演示代码
print('屏幕信息需要 QGuiApplication')
print('主屏幕几何: 屏幕的像素尺寸')
print('可用几何: 排除菜单栏后的可用区域')
print('DPI: 每英寸点数')
print('设备像素比: 视网膜显示屏为 2.0')""", globals())
