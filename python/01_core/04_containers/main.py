#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PySide6 容器类示例

Python内置了强大的容器类型，与Qt容器对应关系：
- str / QString: Python字符串本身就是Unicode
- list / QList: Python列表功能更丰富
- dict / QMap/QHash: Python字典基于哈希表
- set / QSet: Python集合
- bytes / QByteArray: Python字节类型

注意：
- Python没有隐式共享(Copy-on-Write)机制
- Python容器是引用语义，赋值是引用拷贝
- 需要深拷贝时使用 copy 模块

官方文档: https://docs.python.org/3/tutorial/datastructures.html
"""

import sys
from PySide6.QtCore import QCoreApplication


def demonstrate_string():
    """Python字符串示例（对应QString）"""
    print("=== Python 字符串示例 ===\n")
    
    # 创建
    s1 = "Hello"
    s2 = str("World")
    s3 = "中文支持"  # Python3字符串天然支持Unicode
    
    # 拼接
    combined = s1 + " " + s2
    print(f"拼接: {combined}")
    
    # 格式化 (推荐使用f-string)
    name = "Alice"
    age = 25
    formatted = f"Name: {name}, Age: {age}"
    print(f"格式化 (f-string): {formatted}")
    
    # 使用format方法
    formatted2 = "Name: {}, Age: {}".format(name, age)
    print(f"格式化 (format): {formatted2}")
    
    # %格式化（类似QString::arg）
    formatted3 = "Name: %s, Age: %d" % (name, age)
    print(f"格式化 (%): {formatted3}")
    
    # 查找替换
    text = "Hello World World"
    print(f"包含 World: {'World' in text}")
    print(f"World 位置: {text.index('World')}")
    print(f"替换后: {text.replace('World', 'Qt')}")
    
    # 分割
    csv = "apple,banana,cherry"
    fruits = csv.split(",")
    print(f"分割: {fruits}")
    
    # 连接
    print(f"连接: {' | '.join(fruits)}")
    
    # 大小写
    print(f"大写: {'hello'.upper()}")
    print(f"小写: {'HELLO'.lower()}")
    
    # 裁剪空白
    print(f"裁剪: {'  hello  '.strip()}")
    
    # 数值转换
    print(f"字符串转数字: {int('123')}")
    print(f"数字转字符串: {format(3.14159, '.2f')}")
    
    # 中文
    print(f"中文字符串: {s3}")
    print(f"中文长度: {len(s3)}")


def demonstrate_list():
    """Python列表示例（对应QList）"""
    print("\n=== Python 列表示例 ===\n")
    
    # 创建
    list1 = [1, 2, 3, 4, 5]
    list2 = ["Apple", "Banana", "Cherry"]
    
    # 添加元素
    list1.append(6)           # 末尾添加
    list1.insert(0, 0)        # 在索引0处插入
    list1.extend([7, 8])      # 扩展列表
    
    print(f"list1: {list1}")
    
    # 访问
    print(f"第一个: {list1[0]}")
    print(f"最后一个: {list1[-1]}")
    print(f"索引 3: {list1[3]}")
    
    # 切片
    print(f"切片 [1:4]: {list1[1:4]}")
    print(f"前3个: {list1[:3]}")
    print(f"后3个: {list1[-3:]}")
    
    # 查找
    print(f"包含 5: {5 in list1}")
    print(f"5 的索引: {list1.index(5)}")
    print(f"计数 3: {list1.count(3)}")
    
    # 修改
    list1[0] = 100
    
    # 删除
    list1.pop()        # 删除最后一个
    list1.pop(0)       # 删除索引0
    list1.remove(5)    # 删除第一个匹配项
    
    print(f"修改后: {list1}")
    
    # 遍历
    print("遍历:")
    for value in list1:
        print(f"  {value}")
    
    # 带索引遍历
    print("带索引遍历:")
    for i, value in enumerate(list1):
        print(f"  索引 {i}: {value}")
    
    # 排序
    unsorted = [3, 1, 4, 1, 5, 9, 2, 6]
    sorted_list = sorted(unsorted)
    print(f"排序后: {sorted_list}")
    
    # 原地排序
    unsorted.sort()
    print(f"原地排序: {unsorted}")
    
    # 列表推导式（Python特色）
    squares = [x**2 for x in range(1, 6)]
    print(f"平方列表: {squares}")


def demonstrate_dict():
    """Python字典示例（对应QMap/QHash）"""
    print("\n=== Python 字典示例 (哈希表实现) ===\n")
    
    # 创建
    scores = {}
    
    # 插入
    scores["Alice"] = 95
    scores["Bob"] = 87
    scores["Charlie"] = 92
    scores["David"] = 88
    
    print(f"scores: {scores}")
    
    # 访问
    print(f"Alice 分数: {scores['Alice']}")
    print(f"不存在的键 (get): {scores.get('Unknown', -1)}")  # 默认值
    
    # 检查
    print(f"包含 Bob: {'Bob' in scores}")
    print(f"大小: {len(scores)}")
    
    # 键值列表
    print(f"所有键: {list(scores.keys())}")
    print(f"所有值: {list(scores.values())}")
    print(f"所有项: {list(scores.items())}")
    
    # 遍历
    print("遍历:")
    for key, value in scores.items():
        print(f"  {key}: {value}")
    
    # 删除
    del scores["David"]
    print(f"删除后: {scores}")
    
    # 字典推导式
    squared = {k: v**2 for k, v in scores.items()}
    print(f"分数平方: {squared}")


def demonstrate_set():
    """Python集合示例（对应QSet）"""
    print("\n=== Python 集合示例 ===\n")
    
    # 创建
    set1 = {1, 2, 3, 4, 5}
    set2 = {4, 5, 6, 7, 8}
    
    print(f"set1: {set1}")
    print(f"set2: {set2}")
    
    # 集合操作
    print(f"并集: {set1 | set2}")           # 或 set1.union(set2)
    print(f"交集: {set1 & set2}")           # 或 set1.intersection(set2)
    print(f"差集 (set1 - set2): {set1 - set2}")  # 或 set1.difference(set2)
    print(f"对称差集: {set1 ^ set2}")       # 或 set1.symmetric_difference(set2)
    
    # 添加/删除
    set1.add(10)
    set1.discard(1)  # 删除，不存在不报错
    set1.remove(2)   # 删除，不存在会报错
    print(f"修改后 set1: {set1}")
    
    # 检查
    print(f"包含 3: {3 in set1}")
    
    # 集合推导式
    even_squares = {x**2 for x in range(10) if x % 2 == 0}
    print(f"偶数平方集合: {even_squares}")


def demonstrate_bytes():
    """Python字节示例（对应QByteArray）"""
    print("\n=== Python 字节示例 ===\n")
    
    # 创建
    data = b"Hello, Binary World!"
    
    print(f"数据: {data}")
    print(f"大小: {len(data)}")
    
    # 十六进制
    print(f"十六进制: {data.hex()}")
    
    # Base64
    import base64
    encoded = base64.b64encode(data)
    print(f"Base64 编码: {encoded}")
    print(f"Base64 解码: {base64.b64decode(encoded)}")
    
    # 数值
    num_str = str(12345).encode()  # 数值转字节
    print(f"数值转字节: {num_str}")
    print(f"字节转数值: {int(num_str.decode())}")
    
    # bytearray（可变字节）
    mutable = bytearray(b"hello")
    mutable[0] = ord('H')
    print(f"可变字节数组: {mutable}")


def demonstrate_reference_semantics():
    """展示Python的引用语义（对比Qt的隐式共享）"""
    print("\n=== Python 引用语义示例 ===\n")
    
    # 赋值是引用拷贝
    original = [1, 2, 3]
    reference = original  # 引用同一对象
    
    print(f"original id: {id(original)}")
    print(f"reference id: {id(reference)}")
    print(f"是同一对象: {original is reference}")
    
    # 修改会影响原对象
    reference[0] = 100
    print(f"修改后 original: {original}")
    print(f"修改后 reference: {reference}")
    
    # 浅拷贝
    import copy
    shallow = copy.copy(original)
    shallow[0] = 999
    print(f"浅拷贝修改后 original: {original}")
    print(f"浅拷贝: {shallow}")
    
    # 深拷贝（用于嵌套对象）
    nested = [[1, 2], [3, 4]]
    deep = copy.deepcopy(nested)
    deep[0][0] = 100
    print(f"深拷贝 original nested: {nested}")
    print(f"深拷贝: {deep}")
    
    print("\n提示:")
    print("- Python没有Qt的隐式共享机制")
    print("- 赋值操作是引用拷贝")
    print("- 需要独立副本时使用 copy.copy() 或 copy.deepcopy()")


def main():
    """主函数"""
    app = QCoreApplication(sys.argv)
    
    print("=== PySide6 容器类示例 ===\n")
    
    demonstrate_string()
    demonstrate_list()
    demonstrate_dict()
    demonstrate_set()
    demonstrate_bytes()
    demonstrate_reference_semantics()
    
    print("\n=== Python vs Qt 容器对比 ===")
    print("| Qt       | Python | 说明 |")
    print("|----------|--------|------|")
    print("| QString  | str    | Python字符串功能更强大 |")
    print("| QList    | list   | Python列表更灵活 |")
    print("| QMap     | dict   | dict基于哈希表，O(1)查找 |")
    print("| QHash    | dict   | Python只有dict |")
    print("| QSet     | set    | 功能基本相同 |")
    print("| QByteArray| bytes/bytearray | Python分开不可变/可变 |")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
