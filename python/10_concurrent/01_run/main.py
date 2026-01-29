#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
QtConcurrent::run demo - Python version

This example demonstrates how to run a function asynchronously
in a separate thread using ThreadPoolExecutor (Python equivalent
of QtConcurrent::run).

对比:
- QtConcurrent::run -> ThreadPoolExecutor.submit
- QFuture -> Future
"""

import sys
import time
from concurrent.futures import ThreadPoolExecutor
from PySide6.QtCore import QCoreApplication


def heavy_computation(value):
    """耗时计算：模拟耗时操作并返回结果"""
    time.sleep(0.2)  # QThread::msleep(200)
    return value * 2


def main():
    app = QCoreApplication(sys.argv)

    print("Running task...")
    
    # 使用 ThreadPoolExecutor 替代 QtConcurrent::run
    with ThreadPoolExecutor(max_workers=1) as executor:
        future = executor.submit(heavy_computation, 21)
        result = future.result()
        print(f"Result: {result}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
