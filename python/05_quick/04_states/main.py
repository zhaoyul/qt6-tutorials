#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PySide6 Quick States & Transitions 示例

Qt Quick 状态机：
- State: 状态定义
- PropertyChanges: 属性变化
- Transition: 过渡动画
- AnchorChanges: 锚点变化

官方文档: https://doc.qt.io/qtforpython/PySide6/QtQuick/index.html
"""

import sys
from pathlib import Path
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine


def main():
    app = QGuiApplication(sys.argv)
    
    print("=== PySide6 Quick States & Transitions 示例 ===\n")
    
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
