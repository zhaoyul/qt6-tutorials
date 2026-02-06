#!/usr/bin/env clojure -M
;; PySide6 定时器示例 (Clojure + libpython-clj)

(require '[libpython-clj2.python :as py]
         '[libpython-clj2.require :refer [require-python]])

(py/initialize!)

;; 导入模块
(require-python '[PySide6.QtCore :as QtCore :bind-ns])
(require-python :from "01_core/08_timer"
                '[embedded :as py-embedded :bind-ns :reload])

;; 获取类
(def QTimer (py/get-attr QtCore "QTimer"))
(def QCoreApplication (py/get-attr QtCore "QCoreApplication"))

;; 初始化 QCoreApplication
(py/call-attr py-embedded "run_block_1")

(defn demonstrate-single-shot
  "单次定时器"
  []
  (println "\n=== 单次定时器 ===")

  (let [executed (atom false)]
    ;; 使用 Python 代码创建单次定时器
    (py/call-attr py-embedded "run_block_2")
    (println "单次定时器已设置 (100ms)")
    (Thread/sleep 200)))

(defn demonstrate-repeating-timer
  "重复定时器"
  []
  (println "\n=== 重复定时器 ===")

  (py/call-attr py-embedded "run_block_3")

  (println "重复定时器已启动 (100ms 间隔)")
  (Thread/sleep 500))  ;; 等待定时器触发几次

(defn demonstrate-lambda-timer
  "Lambda 定时器"
  []
  (println "\n=== Lambda 定时器 ===")

  (let [values (atom [])]
    (py/call-attr py-embedded "run_block_4")
    (println "Lambda 定时器运行中...")
    (Thread/sleep 400)))

(defn demonstrate-precise-timer
  "精确计时"
  []
  (println "\n=== 精确计时 ===")

  (py/call-attr py-embedded "run_block_5")

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
