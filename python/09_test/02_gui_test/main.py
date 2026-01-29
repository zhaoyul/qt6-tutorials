#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PySide6 GUI 测试示例

GUI 测试特点：
- 测试 QWidget 的显示/隐藏状态
- 测试 QPushButton 的文本属性
- 使用 unittest 框架

主要方法：
- assertEqual(actual, expected): 比较值
- assertTrue(condition): 验证条件为真
- assertFalse(condition): 验证条件为假

官方文档: https://doc.qt.io/qtforpython/PySide6/QtTest/index.html
"""

import sys
import unittest
from PySide6.QtWidgets import QApplication, QPushButton, QWidget


class TestGuiDemo(unittest.TestCase):
    """GUI 测试类"""
    
    @classmethod
    def setUpClass(cls):
        """类级别初始化"""
        print("=== GUI 测试开始 ===")
        # 确保有 QApplication 实例
        cls.app = QApplication.instance() or QApplication([])
    
    @classmethod
    def tearDownClass(cls):
        """类级别清理"""
        print("=== GUI 测试结束 ===")
    
    def test_button_text(self):
        """测试按钮文本设置"""
        button = QPushButton()
        button.setText("Hello")
        self.assertEqual(button.text(), "Hello")
    
    def test_show_hide_widget(self):
        """测试窗口显示和隐藏"""
        widget = QWidget()
        
        # 测试显示
        widget.show()
        self.assertTrue(widget.isVisible())
        
        # 测试隐藏
        widget.hide()
        self.assertFalse(widget.isVisible())


def main():
    print("=== PySide6 GUI 测试示例 ===\n")
    
    # 运行测试
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # 添加测试类
    suite.addTests(loader.loadTestsFromTestCase(TestGuiDemo))
    
    # 运行
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(main())
