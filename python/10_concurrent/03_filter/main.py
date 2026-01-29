#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
QtConcurrent::filter demo - Python version

This example demonstrates how to filter elements from a collection
based on a predicate function.

对比:
- QtConcurrent::filtered -> ThreadPoolExecutor + filter
"""

import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from PySide6.QtCore import QCoreApplication


def is_even(value):
    """判断是否为偶数"""
    return value % 2 == 0


def main():
    app = QCoreApplication(sys.argv)

    numbers = list(range(1, 11))  # [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    
    # 使用 ThreadPoolExecutor 替代 QtConcurrent::filtered
    with ThreadPoolExecutor() as executor:
        # 提交所有过滤任务
        futures = {executor.submit(is_even, n): n for n in numbers}
        
        # 收集偶数结果
        even_numbers = []
        for future in as_completed(futures):
            number = futures[future]
            if future.result():
                even_numbers.append(number)
        
        even_numbers.sort()

    print(f"Even numbers: {even_numbers}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
