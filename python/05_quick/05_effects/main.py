#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PySide6 Quick Visual Effects 示例

Qt Quick 视觉效果：
- Opacity: 透明度
- Rotation: 旋转
- Scale: 缩放
- DropShadow: 阴影效果
- Blur: 模糊效果
- Brightness/Contrast: 亮度/对比度

官方文档: https://doc.qt.io/qtforpython/PySide6/QtQuick/index.html
"""

import sys
import os
from pathlib import Path
from PySide6.QtGui import QGuiApplication
from PySide6.QtCore import QTimer
from PySide6.QtQml import QQmlApplicationEngine


def main():
    app = QGuiApplication(sys.argv)
    
    print("=== PySide6 Quick Visual Effects 示例 ===\n")
    
    engine = QQmlApplicationEngine()
    
    # 加载 QML 文件
    qml_file = Path(__file__).parent / "Main.qml"
    engine.load(str(qml_file))
    
    if not engine.rootObjects():
        print("QML 加载失败")
        return -1
    
    auto_quit_ms = os.environ.get("QT6_TUTORIAL_AUTOQUIT")
    if auto_quit_ms:
        QTimer.singleShot(int(auto_quit_ms), app.quit)

    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
