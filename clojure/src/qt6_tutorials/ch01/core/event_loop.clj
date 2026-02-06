;; PySide6 事件循环示例 (Clojure + libpython-clj)

(ns qt6_tutorials.ch01.core.event_loop)

(require '[libpython-clj2.python :as py]
         '[libpython-clj2.require :refer [require-python]])

(py/initialize!)

;; 导入模块
(require-python '[PySide6.QtCore :as QtCore :bind-ns])
(require-python :from "01_core/06_event_loop"
                '[embedded :as py-embedded :bind-ns :reload])

;; 获取类
(def QCoreApplication (py/get-attr QtCore "QCoreApplication"))
(def QEventLoop (py/get-attr QtCore "QEventLoop"))
(def QTimer (py/get-attr QtCore "QTimer"))
(def QThread (py/get-attr QtCore "QThread"))

(defn demonstrate-timer-events
  "定时器事件"
  []
  (println "\n=== 定时器事件 ===")

  ;; 初始化 QCoreApplication
  (py/call-attr py-embedded "run_block_1")

  (let [counter (atom 0)]
    ;; 创建单次定时器
    (py/call-attr py-embedded "run_block_2")

    (println "定时器已启动，100ms后执行...")
    ;; 事件循环将在定时器回调中退出
    (let [timer (py/get-attr py-embedded "timer")]
      ;; 等待一下让定时器有机会执行
      (Thread/sleep 200))))

(defn demonstrate-custom-events
  "自定义事件"
  []
  (println "\n=== 自定义事件 ===")

  ;; 创建自定义事件类
  (py/call-attr py-embedded "run_block_3")

  (println "自定义事件已发送"))

(defn demonstrate-signal-slot-events
  "信号槽事件处理"
  []
  (println "\n=== 信号槽事件处理 ===")

  (py/call-attr py-embedded "run_block_4")

  (println "信号槽事件处理完成"))

(defn -main
  [& args]
  (println "=== PySide6 事件循环示例 (Clojure) ===")

  (demonstrate-timer-events)
  (demonstrate-custom-events)
  (demonstrate-signal-slot-events)

  (println "\n=== 完成 ==="))
