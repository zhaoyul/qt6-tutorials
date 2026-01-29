#!/usr/bin/env clojure -M
;; PySide6 GUI 测试示例 (Clojure + libpython-clj)

(require '[libpython-clj2.python :as py])

;; 初始化 Python
(py/initialize!)

;; 导入 PySide6 模块
(def QtWidgets (py/import-module "PySide6.QtWidgets"))
(def unittest (py/import-module "unittest"))

;; 获取类
(def QApplication (py/get-attr QtWidgets "QApplication"))
(def QPushButton (py/get-attr QtWidgets "QPushButton"))
(def QWidget (py/get-attr QtWidgets "QWidget"))
(def TestCase (py/get-attr unittest "TestCase"))

;; 测试应用实例
(def test-app (atom nil))

(defn- setup-class [cls]
  "类级别初始化"
  (println "=== GUI 测试开始 ===")
  ;; 确保有 QApplication 实例
  (let [existing (py/call-attr QApplication "instance")]
    (if existing
      (reset! test-app existing)
      (reset! test-app (QApplication []))))
  nil)

(defn- teardown-class [cls]
  "类级别清理"
  (println "=== GUI 测试结束 ===")
  nil)

(defn- test-button-text [self]
  "测试按钮文本设置"
  (let [button (QPushButton)]
    (py/call-attr button "setText" "Hello")
    (py/call-attr self "assertEqual" 
                  (py/call-attr button "text")
                  "Hello")))

(defn- test-show-hide-widget [self]
  "测试窗口显示和隐藏"
  (let [widget (QWidget)]
    ;; 测试显示
    (py/call-attr widget "show")
    (py/call-attr self "assertTrue"
                  (py/call-attr widget "isVisible"))
    
    ;; 测试隐藏
    (py/call-attr widget "hide")
    (py/call-attr self "assertFalse"
                  (py/call-attr widget "isVisible"))))

;; 创建测试类
(def TestGuiDemo
  (py/run-simple-string
   "from PySide6.QtWidgets import QApplication, QPushButton, QWidget
import unittest

class TestGuiDemo(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])
    
    def test_button_text(self):
        button = QPushButton()
        button.setText('Hello')
        self.assertEqual(button.text(), 'Hello')
    
    def test_show_hide_widget(self):
        widget = QWidget()
        widget.show()
        self.assertTrue(widget.isVisible())
        widget.hide()
        self.assertFalse(widget.isVisible())
"))

(defn -main
  "主函数"
  [& args]
  (println "=== PySide6 GUI 测试示例 (Clojure) ===\n")
  
  ;; 创建 QApplication (GUI 程序需要)
  (def app (py/run-simple-string "from PySide6.QtWidgets import QApplication
app = QApplication.instance() or QApplication([])"))
  
  ;; 获取测试类
  (def TestGuiDemoClass (py/get-item (py/import-module "__main__") "TestGuiDemo"))
  
  ;; 运行测试
  (let [loader (py/call-attr unittest "TestLoader")
        suite (py/call-attr unittest "TestSuite")
        runner (py/call-attr unittest "TextTestRunner" nil {"verbosity" 2})]
    
    ;; 加载测试
    (py/call-attr suite "addTests"
                  (py/call-attr loader "loadTestsFromTestCase" TestGuiDemo))
    
    ;; 运行
    (let [result (py/call-attr runner "run" suite)]
      (if (py/call-attr result "wasSuccessful")
        0
        1))))

;; 运行主函数
(-main)
