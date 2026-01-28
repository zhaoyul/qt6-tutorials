#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PySide6 元对象系统 (Meta-Object System) 示例

元对象系统是Qt的核心特性，提供了：
1. 运行时类型信息 (RTTI)
2. 信号与槽机制
3. 属性系统

关键点：
- 继承 QObject
- 使用 Signal 定义信号
- 使用 @Property 装饰器定义属性
- 使用 @Slot 装饰器定义槽

注意：Python是动态语言，不需要MOC预处理

官方文档: https://doc.qt.io/qtforpython/PySide6/QtCore/index.html
"""

import sys
from PySide6.QtCore import (
    QCoreApplication,
    QObject,
    QMetaObject,
    QMetaProperty,
    QMetaMethod,
    Property,
    Signal,
    Slot
)


class Person(QObject):
    """
    自定义类，展示元对象系统
    在PySide6中，不需要Q_OBJECT宏
    """
    
    # 定义信号 (对应C++的 signals:)
    # 注意：信号在类级别定义
    nameChanged = Signal(str)
    ageChanged = Signal(int)
    
    # 类信息 (Python中没有直接的Q_CLASSINFO等价物，
    # 但可以用类属性或文档字符串来存储元信息)
    __class_info__ = {
        "author": "Qt学习项目",
        "version": "1.0"
    }
    
    def __init__(self, parent=None):
        """构造函数"""
        super().__init__(parent)
        self._name = "Unknown"
        self._age = 0
    
    # Property 装饰器定义属性 (对应C++的 Q_PROPERTY)
    # notify 参数指定当属性变化时发出的信号
    @Property(str, notify=nameChanged)
    def name(self):
        """name属性的getter"""
        return self._name
    
    @name.setter
    def name(self, value):
        """name属性的setter"""
        if self._name != value:
            self._name = value
            self.nameChanged.emit(value)
    
    @Property(int, notify=ageChanged)
    def age(self):
        """age属性的getter"""
        return self._age
    
    @age.setter
    def age(self, value):
        """age属性的setter"""
        if self._age != value:
            self._age = value
            self.ageChanged.emit(value)
    
    # 可调用方法 (对应C++的 Q_INVOKABLE)
    # 在Python中，所有公共方法都是可调用的
    # 使用@Slot装饰器可以明确标记为槽，支持元对象调用
    @Slot()
    def introduce(self):
        """自我介绍"""
        print(f"我是{self._name}, 今年{self._age}岁")
    
    @Slot()
    def onBirthday(self):
        """过生日槽函数"""
        self.age = self._age + 1
        print(f"{self._name}过生日了! 现在{self._age}岁")


def explore_meta_object(obj: QObject):
    """
    探索对象的元对象信息
    对应C++的 exploreMetaObject 函数
    """
    meta = obj.metaObject()
    
    print("\n========== 元对象信息 ==========")
    print(f"类名: {meta.className()}")
    super_class = meta.superClass()
    print(f"父类: {super_class.className() if super_class else '无'}")
    
    # 类信息
    print("\n--- 类信息 ---")
    if hasattr(obj, '__class_info__'):
        for key, value in obj.__class_info__.items():
            print(f"  {key}: {value}")
    
    # 属性
    print("\n--- 属性 (Property) ---")
    # 遍历所有属性
    for i in range(meta.propertyOffset(), meta.propertyCount()):
        prop = meta.property(i)
        print(f"  属性: {prop.name()}")
        print(f"    类型: {prop.typeName()}")
        print(f"    可读: {prop.isReadable()}")
        print(f"    可写: {prop.isWritable()}")
    
    # 方法
    print("\n--- 方法 ---")
    for i in range(meta.methodOffset(), meta.methodCount()):
        method = meta.method(i)
        method_type = method.methodType()
        
        # 方法类型名称映射
        type_names = {
            QMetaMethod.MethodType.Signal: "信号",
            QMetaMethod.MethodType.Slot: "槽",
            QMetaMethod.MethodType.Method: "方法",
            QMetaMethod.MethodType.Constructor: "构造函数"
        }
        type_name = type_names.get(method_type, "未知")
        
        print(f"  {type_name}: {method.methodSignature()}")


def main():
    """主函数"""
    app = QCoreApplication(sys.argv)
    
    print("=== PySide6 元对象系统示例 ===\n")
    
    # 创建对象
    person = Person()
    person.name = "张三"
    person.age = 25
    
    # 探索元对象
    explore_meta_object(person)
    
    # 通过元对象系统调用方法
    print("\n--- 通过 QMetaObject::invokeMethod 调用方法 ---")
    # 注意：PySide6的invokeMethod用法与C++略有不同
    QMetaObject.invokeMethod(person, "introduce")
    
    # 通过属性系统设置值
    print("\n--- 通过属性系统设置值 ---")
    person.setProperty("name", "李四")
    person.setProperty("age", 30)
    
    print(f"读取属性 name: {person.property('name')}")
    print(f"读取属性 age: {person.property('age')}")
    
    # 动态属性 (不需要预先声明)
    print("\n--- 动态属性 ---")
    person.setProperty("hobby", "编程")  # 动态添加
    print(f"动态属性 hobby: {person.property('hobby')}")
    
    # 对象继承检查
    print("\n--- 类型检查 ---")
    print(f"person 是 Person 类型: {person.inherits('Person')}")
    print(f"person 是 QObject 类型: {person.inherits('QObject')}")
    print(f"person 是 QWidget 类型: {person.inherits('QWidget')}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
