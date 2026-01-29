#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
QtConcurrent::mappedReduced demo - Python version

This example demonstrates the map-reduce pattern:
1. Map: Apply a function to each element in a collection
2. Reduce: Combine the results into a single value

对比:
- QtConcurrent::mappedReduced -> ThreadPoolExecutor.map + sum
"""

import sys
from concurrent.futures import ThreadPoolExecutor
from PySide6.QtCore import QCoreApplication


def square(value):
    """计算平方"""
    return value * value


def main():
    app = QCoreApplication(sys.argv)

    numbers = list(range(1, 11))  # [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    
    # 使用 ThreadPoolExecutor 替代 QtConcurrent::mappedReduced
    with ThreadPoolExecutor() as executor:
        # Map: 并行计算平方
        mapped_results = list(executor.map(square, numbers))
        # Reduce: 求和
        result = sum(mapped_results)

    print(f"Sum of squares: {result}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
