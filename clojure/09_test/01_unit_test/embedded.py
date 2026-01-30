def run_block_1():
    exec(r"""class Calculator:
    def __init__(self):
        pass
    
    def add(self, a, b):
        return a + b
    
    def subtract(self, a, b):
        return a - b
    
    def multiply(self, a, b):
        return a * b
    
    def divide(self, a, b):
        if b == 0:
            raise ValueError('Division by zero')
        return a / b
    
    def format_result(self, value):
        return f'Result: {value}'
""", globals())

def run_block_2():
    exec(r"""import unittest

class TestCalculator(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print('=== 测试套件开始 ===')
        cls.calc = Calculator()
    
    @classmethod
    def tearDownClass(cls):
        print('=== 测试套件结束 ===')
    
    def setUp(self):
        print('--- 测试开始 ---')
    
    def tearDown(self):
        print('--- 测试结束 ---')
    
    def test_add(self):
        self.assertEqual(self.calc.add(2, 3), 5)
        self.assertEqual(self.calc.add(-1, 1), 0)
        self.assertEqual(self.calc.add(0, 0), 0)
    
    def test_subtract(self):
        self.assertEqual(self.calc.subtract(5, 3), 2)
        self.assertEqual(self.calc.subtract(3, 5), -2)
    
    def test_multiply(self):
        self.assertEqual(self.calc.multiply(3, 4), 12)
        self.assertEqual(self.calc.multiply(-2, 3), -6)
        self.assertEqual(self.calc.multiply(0, 100), 0)
    
    def test_divide(self):
        self.assertEqual(self.calc.divide(10, 2), 5.0)
        self.assertEqual(self.calc.divide(7, 2), 3.5)
        with self.assertRaises(ValueError):
            self.calc.divide(1, 0)
    
    def test_add_data_driven(self):
        test_cases = [
            (2, 3, 5, 'positive'),
            (-2, -3, -5, 'negative'),
            (-2, 5, 3, 'mixed'),
            (0, 0, 0, 'zero'),
            (1000000, 2000000, 3000000, 'large'),
        ]
        for a, b, expected, name in test_cases:
            with self.subTest(name=name, a=a, b=b):
                self.assertEqual(self.calc.add(a, b), expected)
    
    def test_format_result(self):
        result = self.calc.format_result(42)
        self.assertTrue(result)
        self.assertIn('42', result)
        self.assertEqual(result, 'Result: 42')
        self.assertTrue(result.startswith('Result'), 'Should start with "Result"')
    
    def test_floating_point(self):
        result = 0.1 + 0.2
        self.assertAlmostEqual(result, 0.3, places=7)
    
    def test_benchmark(self):
        import timeit
        def benchmark_func():
            for i in range(1000):
                str(i)
        elapsed = timeit.timeit(benchmark_func, number=10)
        print(f'\n基准测试耗时: {elapsed:.4f}s')
""", globals())

def run_block_3():
    exec(r"""from PySide6.QtWidgets import QApplication, QPushButton, QLineEdit
from PySide6.QtTest import QTest
from PySide6.QtCore import Qt
import unittest

class TestQtSpecific(unittest.TestCase):
    def test_qtest_mouse_click(self):
        app = QApplication.instance() or QApplication([])
        button = QPushButton()
        button.setCheckable(True)
        QTest.mouseClick(button, Qt.LeftButton)
        self.assertTrue(button.isChecked())
    
    def test_qtest_key_events(self):
        app = QApplication.instance() or QApplication([])
        line_edit = QLineEdit()
        QTest.keyClicks(line_edit, 'Hello Qt')
        self.assertEqual(line_edit.text(), 'Hello Qt')
""", globals())
