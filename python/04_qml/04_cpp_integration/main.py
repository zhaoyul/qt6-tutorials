#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PySide6 QML 与 Python 集成示例

对应 C++ 的 04_cpp_integration 示例

集成方式：
1. qmlRegisterType 注册类型
2. setContextProperty 暴露对象实例
3. 简单值作为上下文属性

官方文档: https://doc.qt.io/qtforpython/PySide6/QtQml/index.html
"""

import sys
import os
from pathlib import Path
from PySide6.QtGui import QGuiApplication
from PySide6.QtCore import QTimer
from PySide6.QtQml import QQmlApplicationEngine, QQmlContext, qmlRegisterType
from counter import Counter


def main():
    app = QGuiApplication(sys.argv)
    
    print("=== PySide6 QML 与 Python 集成示例 ===\n")
    
    # 注册 Counter 类型到 QML
    # 对应 C++ 的 QML_ELEMENT
    qmlRegisterType(Counter, "QmlCppIntegration", 1, 0, "Counter")
    
    engine = QQmlApplicationEngine()
    
    # 方式1: 通过上下文暴露对象实例
    global_counter = Counter(engine)
    global_counter.value = 50
    engine.rootContext().setContextProperty("globalCounter", global_counter)
    
    # 方式2: 暴露简单值
    engine.rootContext().setContextProperty("appVersion", "1.0.0")
    engine.rootContext().setContextProperty("debugMode", True)
    
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
