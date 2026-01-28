#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PySide6 QML 与 Python 集成示例

集成方式：
1. @QmlElement 装饰器自动注册 (PySide6 6.4+)
2. qmlRegisterType 手动注册
3. Context Property 上下文属性
4. setObjectOwnership 控制所有权

对应 C++ 版本，但使用 Python 实现
"""

import sys
from pathlib import Path
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine, QQmlContext
from PySide6.QtCore import QObject

# 导入 Counter 类
try:
    from counter import Counter
except ImportError:
    # 如果 counter.py 在相同目录
    import importlib.util
    spec = importlib.util.spec_from_file_location("counter", 
                                                   Path(__file__).parent / "counter.py")
    counter_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(counter_module)
    Counter = counter_module.Counter


def main():
    app = QGuiApplication(sys.argv)
    
    print("=== PySide6 QML 与 Python 集成示例 ===\n")
    
    engine = QQmlApplicationEngine()
    
    # 方式1: 尝试使用 @QmlElement 自动注册
    # 如果 Counter 类使用了 @QmlElement 装饰器，它会自动注册
    # 否则需要在下面手动注册
    
    try:
        from PySide6.QtQml import qmlRegisterType
        # 手动注册类型 (如果 @QmlElement 不可用)
        qmlRegisterType(Counter, "PythonCounter", 1, 0, "Counter")
        print("手动注册 Counter 类型到 QML")
    except Exception as e:
        print(f"类型注册信息: {e}")
    
    # 方式2: 通过上下文暴露对象实例
    global_counter = Counter(engine)
    global_counter.value = 50
    engine.rootContext().setContextProperty("globalCounter", global_counter)
    
    # 方式3: 暴露简单值
    engine.rootContext().setContextProperty("appVersion", "1.0.0 (Python)")
    engine.rootContext().setContextProperty("debugMode", True)
    
    # 加载 QML 文件
    qml_file = Path(__file__).parent / "Main.qml"
    
    # 修改 QML 导入以使用 Python 注册的模块
    # 读取原始 QML 并替换导入
    qml_content = qml_file.read_text(encoding='utf-8')
    # 替换模块导入 (从 C++ 模块到 Python 模块)
    qml_content = qml_content.replace(
        'import QmlCppIntegration',
        'import PythonCounter 1.0'
    )
    
    # 写入临时文件或直接使用 loadData
    engine.loadData(qml_content.encode('utf-8'), str(qml_file))
    
    if not engine.rootObjects():
        print("QML 加载失败，尝试直接加载原始文件...")
        # 如果修改后加载失败，尝试原始文件
        engine.load(str(qml_file))
        
    if not engine.rootObjects():
        print("QML 加载失败")
        return -1
    
    print("QML 已加载，窗口应该已显示")
    print("\n功能:")
    print("- 本地 Counter 实例 (注册类型)")
    print("- 全局 Counter 实例 (上下文属性)")
    print("- 信号和槽的交互")
    
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
