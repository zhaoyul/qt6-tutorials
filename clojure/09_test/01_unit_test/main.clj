#!/usr/bin/env clojure -M
;; PySide6 单元测试示例 (Clojure + libpython-clj)
;;
;; 使用 Python 的 unittest 框架进行单元测试
;; 展示了数据驱动测试、异常测试、基准测试等特性

(require '[libpython-clj2.python :as py])

;; 初始化 Python
(py/initialize!)

;; 导入 Python 模块
(def unittest (py/import-module "unittest"))
(def timeit (py/import-module "timeit"))
(def QtWidgets (py/import-module "PySide6.QtWidgets"))
(def QtTest (py/import-module "PySide6.QtTest"))
(def QtCore (py/import-module "PySide6.QtCore"))

;; 获取类
(def TestCase (py/get-attr unittest "TestCase"))
(def QApplication (py/get-attr QtWidgets "QApplication"))
(def QPushButton (py/get-attr QtWidgets "QPushButton"))
(def QLineEdit (py/get-attr QtWidgets "QLineEdit"))
(def QTest (py/get-attr QtTest "QTest"))
(def Qt (py/get-attr QtCore "Qt"))

;; ========== 被测试的类 ==========

(defn- calc-add [self a b]
  "加法"
  (+ a b))

(defn- calc-subtract [self a b]
  "减法"
  (- a b))

(defn- calc-multiply [self a b]
  "乘法"
  (* a b))

(defn- calc-divide [self a b]
  "除法"
  (if (= b 0)
    (throw (py/->py-exception Exception "Division by zero"))
    (/ a b)))

(defn- calc-format-result [self value]
  "格式化结果"
  (str "Result: " value))

;; 创建 Calculator 类
(def Calculator
  (py/run-simple-string
   "class Calculator:
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
"))

;; ========== 测试类 ==========

(defn- setup-class [cls]
  "类级别初始化 (所有测试前调用一次)"
  (println "=== 测试套件开始 ===")
  (py/set-attr! cls "calc" (Calculator))
  nil)

(defn- teardown-class [cls]
  "类级别清理 (所有测试后调用一次)"
  (println "=== 测试套件结束 ===")
  nil)

(defn- setup [self]
  "每个测试前的初始化"
  (println "--- 测试开始 ---")
  nil)

(defn- teardown [self]
  "每个测试后的清理"
  (println "--- 测试结束 ---")
  nil)

;; 基本测试
(defn- test-add [self]
  "测试加法"
  (let [calc (py/get-attr self "calc")]
    (py/call-attr self "assertEqual" (py/call-attr calc "add" 2 3) 5)
    (py/call-attr self "assertEqual" (py/call-attr calc "add" -1 1) 0)
    (py/call-attr self "assertEqual" (py/call-attr calc "add" 0 0) 0)))

(defn- test-subtract [self]
  "测试减法"
  (let [calc (py/get-attr self "calc")]
    (py/call-attr self "assertEqual" (py/call-attr calc "subtract" 5 3) 2)
    (py/call-attr self "assertEqual" (py/call-attr calc "subtract" 3 5) -2)))

(defn- test-multiply [self]
  "测试乘法"
  (let [calc (py/get-attr self "calc")]
    (py/call-attr self "assertEqual" (py/call-attr calc "multiply" 3 4) 12)
    (py/call-attr self "assertEqual" (py/call-attr calc "multiply" -2 3) -6)
    (py/call-attr self "assertEqual" (py/call-attr calc "multiply" 0 100) 0)))

(defn- test-divide [self]
  "测试除法"
  (let [calc (py/get-attr self "calc")]
    (py/call-attr self "assertEqual" (py/call-attr calc "divide" 10 2) 5.0)
    (py/call-attr self "assertEqual" (py/call-attr calc "divide" 7 2) 3.5)
    ;; 测试异常
    (py/call-attr self "assertRaises" ValueError 
                  (py/->py-fn (fn [] (py/call-attr calc "divide" 1 0))))))

;; 数据驱动测试
(defn- test-add-data-driven [self]
  "数据驱动测试"
  (let [calc (py/get-attr self "calc")
        test-cases [[2 3 5 "positive"]
                    [-2 -3 -5 "negative"]
                    [-2 5 3 "mixed"]
                    [0 0 0 "zero"]
                    [1000000 2000000 3000000 "large"]]]
    (doseq [[a b expected name] test-cases]
      (let [result (py/call-attr calc "add" a b)]
        (py/call-attr self "assertEqual" result expected
                      (str "Failed for case: " name))))))

;; 字符串测试
(defn- test-format-result [self]
  "测试格式化结果"
  (let [calc (py/get-attr self "calc")
        result (py/call-attr calc "format_result" 42)]
    ;; 各种验证方式
    (py/call-attr self "assertTrue" (boolean result))
    (py/call-attr self "assertIn" "42" result)
    (py/call-attr self "assertEqual" result "Result: 42")
    (py/call-attr self "assertTrue" (.startsWith result "Result")
                   "Should start with 'Result'")))

;; 比较浮点数
(defn- test-floating-point [self]
  "测试浮点数比较"
  (let [result (+ 0.1 0.2)]
    ;; 不要用 assertEqual 比较浮点数精确值
    (py/call-attr self "assertAlmostEqual" result 0.3 7)))

;; 基准测试
(defn- test-benchmark [self]
  "基准测试"
  (let [benchmark-fn (py/->py-fn 
                       (fn []
                         (doseq [i (range 1000)]
                           (str i))))
        timer (py/call-attr timeit "Timer" benchmark-fn)
        elapsed (py/call-attr timer "timeit" 10)]
    (println (format "\n基准测试耗时: %.4fs" elapsed))))

;; ========== 创建测试类 (使用 Python 代码) ==========

(def TestCalculator
  (py/run-simple-string
   "import unittest

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
        self.assertTrue(result.startswith('Result'), 'Should start with \"Result\"')
    
    def test_floating_point(self):
        result = 0.1 + 0.2
        self.assertAlmostEqual(result, 0.3, places=7)
    
    def test_benchmark(self):
        import timeit
        def benchmark_func():
            for i in range(1000):
                str(i)
        elapsed = timeit.timeit(benchmark_func, number=10)
        print(f'\\n基准测试耗时: {elapsed:.4f}s')
"))

;; ========== PySide6/Qt 特定测试 ==========

(defn- test-qtest-mouse-click [self]
  "测试鼠标点击 (GUI测试示例)"
  (let [existing (py/call-attr QApplication "instance")
        app (or existing (QApplication []))
        button (QPushButton)]
    (py/call-attr button "setCheckable" true)
    ;; 使用 QTest 模拟点击
    (py/call-attr QTest "mouseClick" button (py/get-attr Qt "LeftButton"))
    (py/call-attr self "assertTrue" (py/call-attr button "isChecked"))))

(defn- test-qtest-key-events [self]
  "测试键盘事件"
  (let [existing (py/call-attr QApplication "instance")
        app (or existing (QApplication []))
        line-edit (QLineEdit)]
    ;; 模拟按键
    (py/call-attr QTest "keyClicks" line-edit "Hello Qt")
    (py/call-attr self "assertEqual" 
                  (py/call-attr line-edit "text")
                  "Hello Qt")))

;; 创建 Qt 特定测试类
(def TestQtSpecific
  (py/run-simple-string
   "from PySide6.QtWidgets import QApplication, QPushButton, QLineEdit
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
"))

;; ========== 主函数 ==========

(defn -main
  "主函数"
  [& args]
  (println "=== PySide6 单元测试示例 (Clojure) ===\n")
  (println "使用 Python unittest 框架")
  (println "也展示了 PySide6.QtTest 的特定功能\n")
  
  ;; 确保 QApplication 存在 (某些 Qt 测试需要)
  (let [existing (py/call-attr QApplication "instance")]
    (when-not existing
      (QApplication [])))
  
  ;; 获取测试类
  (def TestCalculatorClass (py/get-item (py/import-module "__main__") "TestCalculator"))
  (def TestQtSpecificClass (py/get-item (py/import-module "__main__") "TestQtSpecific"))
  
  ;; 运行测试
  (let [loader (py/call-attr unittest "TestLoader")
        suite (py/call-attr unittest "TestSuite")
        runner (py/call-attr unittest "TextTestRunner" nil {"verbosity" 2})]
    
    ;; 加载测试类
    (py/call-attr suite "addTests"
                  (py/call-attr loader "loadTestsFromTestCase" TestCalculator))
    (py/call-attr suite "addTests"
                  (py/call-attr loader "loadTestsFromTestCase" TestQtSpecific))
    
    ;; 运行
    (let [result (py/call-attr runner "run" suite)]
      (if (py/call-attr result "wasSuccessful")
        (do (println "\n✅ 所有测试通过!")
            0)
        (do (println "\n❌ 测试失败!")
            1)))))

;; 运行主函数
(-main)
