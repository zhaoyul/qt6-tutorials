#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PySide6 Quick 基础元素示例

Qt Quick 基础元素：
- Rectangle: 矩形元素
- Text: 文本元素
- Image: 图像元素
- MouseArea: 鼠标交互区域

官方文档: https://doc.qt.io/qtforpython/PySide6/QtQuick/index.html
"""

import sys
from pathlib import Path
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine


def main():
    app = QGuiApplication(sys.argv)
    
    print("=== PySide6 Quick 基础元素示例 ===\n")
    
    engine = QQmlApplicationEngine()
    
    # 加载 QML 文件
    qml_file = Path(__file__).parent / "Main.qml"
    engine.load(str(qml_file))
    
    if not engine.rootObjects():
        print("QML 加载失败")
        return -1
    
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
