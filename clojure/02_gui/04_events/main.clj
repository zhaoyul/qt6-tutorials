#!/usr/bin/env clojure -M
;; PySide6 GUI 事件系统示例 (Clojure + libpython-clj)
;; 注意：macOS GUI 必须在主线程运行，这里使用 QtCore 演示事件机制

(require '[libpython-clj2.python :as py]
         '[libpython-clj2.require :refer [require-python]])

(py/initialize!)

;; 导入模块
(require-python '[PySide6.QtCore :as QtCore :bind-ns])
(require-python :from "02_gui/04_events"
                '[embedded :as py-embedded :bind-ns :reload])

;; 获取类
(def QObject (py/get-attr QtCore "QObject"))
(def QCoreApplication (py/get-attr QtCore "QCoreApplication"))
(def QEvent (py/get-attr QtCore "QEvent"))
(def QTimer (py/get-attr QtCore "QTimer"))

;; 初始化 QCoreApplication
(py/call-attr py-embedded "run_block_1")

(defn demonstrate-timer-events
  "定时器事件"
  []
  (println "\n=== 定时器事件 ===")
  
  ;; 使用 Python 代码演示
  (py/call-attr py-embedded "run_block_2")
  
  ;; 等待定时器执行
  (Thread/sleep 2000)
  (println "定时器演示完成"))

(defn demonstrate-custom-events
  "自定义事件"
  []
  (println "\n=== 自定义事件 ===")
  
  (py/call-attr py-embedded "run_block_3")
  
  (println "自定义事件演示完成"))

(defn demonstrate-signal-events
  "信号作为事件"
  []
  (println "\n=== 信号事件处理 ===")
  
  (py/call-attr py-embedded "run_block_4")
  
  (println "信号事件演示完成"))

(defn -main
  [& args]
  (println "=== PySide6 事件系统示例 (Clojure) ===")
  
  (demonstrate-timer-events)
  (demonstrate-custom-events)
  (demonstrate-signal-events)
  
  (println "\n=== 事件要点 ===")
  (println "1. QTimer: 定时器事件")
  (println "2. QEvent: 基础事件类")
  (println "3. postEvent: 异步发送事件")
  (println "4. Signal: 信号槽机制")
  
  (println "\n=== 完成 ==="))

(-main)
