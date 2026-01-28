#!/usr/bin/env clojure -M
;; PySide6 定时器示例 (Clojure + libpython-clj)

(require '[libpython-clj2.python :as py])

(py/initialize!)

;; 导入模块
(def QtCore (py/import-module "PySide6.QtCore"))

;; 获取类
(def QTimer (py/get-attr QtCore "QTimer"))
(def QCoreApplication (py/get-attr QtCore "QCoreApplication"))

;; 初始化 QCoreApplication
(py/run-simple-string "
from PySide6.QtCore import QCoreApplication
import sys
if not QCoreApplication.instance():
    _app = QCoreApplication(sys.argv)
")

(defn demonstrate-single-shot
  "单次定时器"
  []
  (println "\n=== 单次定时器 ===")
  
  (let [executed (atom false)]
    ;; 使用 Python 代码创建单次定时器
    (py/run-simple-string "
from PySide6.QtCore import QTimer

def callback():
    print('单次定时器触发!')

QTimer.singleShot(100, callback)
")
    (println "单次定时器已设置 (100ms)")
    (Thread/sleep 200)))

(defn demonstrate-repeating-timer
  "重复定时器"
  []
  (println "\n=== 重复定时器 ===")
  
  (py/run-simple-string "
from PySide6.QtCore import QTimer, QCoreApplication

counter = 0

def on_timeout():
    global counter
    counter += 1
    print(f'定时器触发 #{counter}')
    if counter >= 3:
        timer.stop()
        print('定时器停止')

timer = QTimer()
timer.timeout.connect(on_timeout)
timer.start(100)  # 每100ms触发
")
  
  (println "重复定时器已启动 (100ms 间隔)")
  (Thread/sleep 500))  ;; 等待定时器触发几次

(defn demonstrate-lambda-timer
  "Lambda 定时器"
  []
  (println "\n=== Lambda 定时器 ===")
  
  (let [values (atom [])]
    (py/run-simple-string "
from PySide6.QtCore import QTimer

values = []

def collect_value():
    values.append(len(values))
    print(f'收集值: {len(values) - 1}')

timer = QTimer()
timer.timeout.connect(collect_value)
timer.start(50)

# 300ms后停止
QTimer.singleShot(350, timer.stop)
")
    (println "Lambda 定时器运行中...")
    (Thread/sleep 400)))

(defn demonstrate-precise-timer
  "精确计时"
  []
  (println "\n=== 精确计时 ===")
  
  (py/run-simple-string "
from PySide6.QtCore import QElapsedTimer, QCoreApplication
import time

timer = QElapsedTimer()
timer.start()

# 模拟工作
time.sleep(0.1)  # 100ms

elapsed = timer.elapsed()
print(f'经过时间: {elapsed}ms')

timer.restart()
time.sleep(0.05)  # 50ms
print(f'重启后经过: {timer.elapsed()}ms')
")
  
  (println "精确计时完成"))

(defn -main
  [& args]
  (println "=== PySide6 定时器示例 (Clojure) ===")
  
  (demonstrate-single-shot)
  (demonstrate-repeating-timer)
  (demonstrate-lambda-timer)
  (demonstrate-precise-timer)
  
  (println "\n=== 完成 ==="))

(-main)
