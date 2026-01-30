#!/usr/bin/env clojure -M
;; PySide6 信号与槽示例 (Clojure + libpython-clj)

(require '[libpython-clj2.python :as py]
         '[libpython-clj2.require :refer [require-python]])

(py/initialize!)

;; 导入模块
(require-python '[PySide6.QtCore :as QtCore :bind-ns])
(require-python :from "01_core/02_signals_slots"
                '[signals_slots :as signals :bind-ns :reload])
(require-python :from "01_core/02_signals_slots"
                '[signals_slots :as signals :bind-ns :reload])

;; 获取类
(def QObject (py/get-attr QtCore "QObject"))
(def QCoreApplication (py/get-attr QtCore "QCoreApplication"))

;; 初始化 QCoreApplication（必须先创建才能使用信号槽）
(py/call-attr signals "ensure_app")

(defn demonstrate-basic-connection
  "基本信号槽连接 - 使用 QObject 的内置信号"
  []
  (println "\n=== 基本信号槽连接 ===")

  (let [obj (QObject)]

    ;; 定义槽函数
    (defn on-destroyed []
      (println "对象将被销毁!"))

    ;; 连接信号到槽
    (py/call-attr (py/get-attr obj "destroyed") "connect" on-destroyed)

    (println "信号连接成功，destroyed 信号已连接到槽函数")

    ;; 断开连接
    (py/call-attr (py/get-attr obj "destroyed") "disconnect" on-destroyed)
    (println "信号已断开")))

(defn demonstrate-custom-signals
  "自定义信号"
  []
  (println "\n=== 自定义信号（通过 Python 类）===")

  ;; 获取类并实例化
  (let [comm-class (py/get-attr signals "Communicate")
        comm (comm-class)]

    ;; 连接信号
    (py/call-attr (py/get-attr comm "speak") "connect"
                  (fn [msg] (println (str "收到消息: " msg))))

    (py/call-attr (py/get-attr comm "countChanged") "connect"
                  (fn [count] (println (str "计数: " count))))

    ;; 触发信号
    (py/call-attr comm "speak_message" "Hello from custom signal!")
    (py/call-attr comm "increment")
    (py/call-attr comm "increment")))

(defn demonstrate-multiple-slots
  "一个信号连接多个槽"
  []
  (println "\n=== 一个信号连接多个槽 ===")

  (let [obj (QObject)]

    (defn slot-1 []
      (println "槽函数 1 被调用"))

    (defn slot-2 []
      (println "槽函数 2 被调用"))

    (defn slot-3 []
      (println "槽函数 3 被调用"))

    ;; 连接多个槽
    (py/call-attr (py/get-attr obj "destroyed") "connect" slot-1)
    (py/call-attr (py/get-attr obj "destroyed") "connect" slot-2)
    (py/call-attr (py/get-attr obj "destroyed") "connect" slot-3)

    (println "一个信号已连接到 3 个槽函数")))

(defn demonstrate-signal-args
  "带参数的信号"
  []
  (println "\n=== 带参数的信号 ===")

  (let [emitter-class (py/get-attr signals "ValueEmitter")
        emitter (emitter-class)]

    ;; 连接带参数的信号
    (py/call-attr (py/get-attr emitter "valueChanged") "connect"
                  (fn [num text]
                    (println (str "收到: num=" num ", text=" text))))

    ;; 触发信号
    (py/call-attr emitter "emit_value" 42 "Hello")
    (py/call-attr emitter "emit_value" 100 "World")))

(defn -main
  [& args]
  (println "=== PySide6 信号与槽示例 (Clojure) ===")

  (demonstrate-basic-connection)
  (demonstrate-custom-signals)
  (demonstrate-multiple-slots)
  (demonstrate-signal-args)

  (println "\n=== 完成 ==="))

(-main)
