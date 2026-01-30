#!/usr/bin/env clojure -M
;; PySide6 GUI 测试示例 (Clojure + libpython-clj)

(require '[libpython-clj2.python :as py]
         '[libpython-clj2.require :refer [require-python]])

;; 初始化 Python
(py/initialize!)

;; 导入 PySide6 模块
(require-python '[PySide6.QtWidgets :as QtWidgets :bind-ns])
(require-python :from "09_test/02_gui_test"
                '[embedded :as py-embedded :bind-ns :reload])
(require-python '[unittest :as unittest :bind-ns])

;; 获取类
(def QApplication (py/get-attr QtWidgets "QApplication"))
(def QPushButton (py/get-attr QtWidgets "QPushButton"))
(def QWidget (py/get-attr QtWidgets "QWidget"))
(def TestCase (py/get-attr unittest "TestCase"))

;; 测试应用实例
(def test-app (atom nil))

(defn- macos?
  []
  (.startsWith (System/getProperty "os.name") "Mac"))

(defn- started-on-first-thread?
  []
  (= "1" (System/getenv "JAVA_STARTED_ON_FIRST_THREAD_")))

(defn- ensure-macos-gui-thread
  []
  (when (and (macos?) (not (started-on-first-thread?)))
    (println "macOS 需要使用 -XstartOnFirstThread 运行此 GUI 测试，已跳过。")
    (System/exit 0)))

(defn- setup-class [cls]
  "类级别初始化"
  (println "=== GUI 测试开始 ===")
  ;; 确保有 QApplication 实例
  (let [existing (py/call-attr QApplication "instance")]
    (if existing
      (reset! test-app existing)
      (reset! test-app (QApplication (py/->py-list [])))))
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
(py/call-attr py-embedded "run_block_1")
(def TestGuiDemo (py/get-attr py-embedded "TestGuiDemo"))

(defn -main
  "主函数"
  [& args]
  (println "=== PySide6 GUI 测试示例 (Clojure) ===\n")

  (ensure-macos-gui-thread)
  ;; 创建 QApplication (GUI 程序需要)
  (py/call-attr py-embedded "run_block_2")
  (def app (py/get-attr py-embedded "app"))
  
  ;; 获取测试类
  (def TestGuiDemoClass TestGuiDemo)
  
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
