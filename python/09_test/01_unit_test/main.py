#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PySide6 单元测试示例

Qt Test 框架特点：
- 轻量级，易于使用
- 支持数据驱动测试
- 支持基准测试
- 支持 GUI 测试

主要方法：
- assertTrue(condition): 验证条件
- assertEqual(actual, expected): 比较值

注意：在Python中，通常使用Python标准库的unittest，
但PySide6也提供了QtTest模块用于特定功能。

官方文档: https://doc.qt.io/qtforpython/PySide6/QtTest/index.html
"""

import sys
import unittest
from PySide6.QtCore import QObject, Signal


class Calculator:
    """被测试的类"""
    
    def add(self, a, b):
        return a + b
    
    def subtract(self, a, b):
        return a - b
    
    def multiply(self, a, b):
        return a * b
    
    def divide(self, a, b):
        if b == 0:
            raise ValueError("Division by zero")
        return a / b
    
    def format_result(self, value):
        return f"Result: {value}"


class TestCalculator(unittest.TestCase):
    """测试类"""
    
    @classmethod
    def setUpClass(cls):
        """类级别初始化 (所有测试前调用一次)"""
        print("=== 测试套件开始 ===")
        cls.calc = Calculator()
    
    @classmethod
    def tearDownClass(cls):
        """类级别清理 (所有测试后调用一次)"""
        print("=== 测试套件结束 ===")
    
    def setUp(self):
        """每个测试前的初始化"""
        print("--- 测试开始 ---")
    
    def tearDown(self):
        """每个测试后的清理"""
        print("--- 测试结束 ---")
    
    # 基本测试
    def test_add(self):
        """测试加法"""
        self.assertEqual(self.calc.add(2, 3), 5)
        self.assertEqual(self.calc.add(-1, 1), 0)
        self.assertEqual(self.calc.add(0, 0), 0)
    
    def test_subtract(self):
        """测试减法"""
        self.assertEqual(self.calc.subtract(5, 3), 2)
        self.assertEqual(self.calc.subtract(3, 5), -2)
    
    def test_multiply(self):
        """测试乘法"""
        self.assertEqual(self.calc.multiply(3, 4), 12)
        self.assertEqual(self.calc.multiply(-2, 3), -6)
        self.assertEqual(self.calc.multiply(0, 100), 0)
    
    def test_divide(self):
        """测试除法"""
        self.assertEqual(self.calc.divide(10, 2), 5.0)
        self.assertEqual(self.calc.divide(7, 2), 3.5)
        
        # 测试异常
        with self.assertRaises(ValueError):
            self.calc.divide(1, 0)
    
    # 数据驱动测试
    def test_add_data_driven(self):
        """数据驱动测试"""
        test_cases = [
            (2, 3, 5, "positive"),
            (-2, -3, -5, "negative"),
            (-2, 5, 3, "mixed"),
            (0, 0, 0, "zero"),
            (1000000, 2000000, 3000000, "large"),
        ]
        
        for a, b, expected, name in test_cases:
            with self.subTest(name=name, a=a, b=b):
                self.assertEqual(self.calc.add(a, b), expected)
    
    # 字符串测试
    def test_format_result(self):
        """测试格式化结果"""
        result = self.calc.format_result(42)
        
        # 各种验证方式
        self.assertTrue(result)
        self.assertIn("42", result)
        self.assertEqual(result, "Result: 42")
        self.assertTrue(result.startswith("Result"), "Should start with 'Result'")
    
    # 条件跳过
    @unittest.skip("This test is skipped for demonstration")
    def test_skip_example(self):
        """跳过示例"""
        self.fail("Should not reach here")
    
    # 预期失败
    @unittest.expectedFailure
    def test_expected_fail(self):
        """预期失败"""
        self.assertEqual(1, 2)  # 这个会失败，但不会导致测试套件失败
    
    # 比较浮点数
    def test_floating_point(self):
        """测试浮点数比较"""
        result = 0.1 + 0.2
        # 不要用 assertEqual 比较浮点数精确值
        self.assertAlmostEqual(result, 0.3, places=7)
    
    # 基准测试 (使用 timeit)
    def test_benchmark(self):
        """基准测试"""
        import timeit
        
        def benchmark_func():
            for i in range(1000):
                str(i)
        
        elapsed = timeit.timeit(benchmark_func, number=10)
        print(f"\n基准测试耗时: {elapsed:.4f}s")


# PySide6 QtTest 示例
from PySide6.QtTest import QTest


class TestQtSpecific(unittest.TestCase):
    """PySide6/Qt 特定测试"""
    
    def test_qtest_mouse_click(self):
        """测试鼠标点击 (GUI测试示例)"""
        # 注意: 这里只是示例，实际GUI测试需要QApplication
        from PySide6.QtWidgets import QPushButton, QApplication
        
        # 确保有QApplication
        app = QApplication.instance() or QApplication([])
        
        button = QPushButton()
        button.setCheckable(True)
        
        # 使用 QTest 模拟点击
        QTest.mouseClick(button, Qt.LeftButton)
        
        self.assertTrue(button.isChecked())
    
    def test_qtest_key_events(self):
        """测试键盘事件"""
        from PySide6.QtWidgets import QLineEdit, QApplication
        
        app = QApplication.instance() or QApplication([])
        
        line_edit = QLineEdit()
        
        # 模拟按键
        QTest.keyClicks(line_edit, "Hello Qt")
        
        self.assertEqual(line_edit.text(), "Hello Qt")


def main():
    print("=== PySide6 单元测试示例 ===\n")
    print("使用 Python unittest 框架")
    print("也展示了 PySide6.QtTest 的特定功能\n")
    
    # 运行测试
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # 添加测试类
    suite.addTests(loader.loadTestsFromTestCase(TestCalculator))
    suite.addTests(loader.loadTestsFromTestCase(TestQtSpecific))
    
    # 运行
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(main())
