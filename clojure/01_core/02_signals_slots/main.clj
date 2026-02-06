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

(def ^:private basic-conn-received? (volatile! false))

(def ^:private on-test-signal-callback
  "用于基本连接演示的槽函数"
  (fn [msg]
    (vreset! basic-conn-received? true)
    (println (str "  [槽函数] 收到: " msg))))

(defn demonstrate-basic-connection
  "基本信号槽连接与断开 - 展示连接时收到消息，断开后收不到
   
   使用 ConnectionHelper 类来处理连接/断开，
   避免 libpython-clj 中函数包装器对象不匹配的问题。"
  []
  (println "\n=== 基本信号槽连接与断开 ===")

  (let [helper-class (py/get-attr signals "ConnectionHelper")
        helper (helper-class)]

    ;; 1. 连接信号到槽
    (py/call-attr helper "connect_slot" on-test-signal-callback)
    (println "1. 信号已连接")
    
    ;; 2. 触发信号 → 应该收到消息
    (println "2. 触发信号（连接状态）...")
    (vreset! basic-conn-received? false)
    (py/call-attr helper "emit_test" "Hello from connected signal!")
    (if @basic-conn-received?
      (println "   ✓ 消息已接收")
      (println "   ✗ 未收到消息（异常）"))
    
    ;; 3. 断开连接
    (py/call-attr helper "disconnect_slot")
    (println "3. 信号已断开")
    
    ;; 4. 再次触发信号 → 不应该收到消息
    (println "4. 再次触发信号（断开状态）...")
    (vreset! basic-conn-received? false)
    (py/call-attr helper "emit_test" "This should NOT be received!")
    (if @basic-conn-received?
      (println "   ✗ 消息仍被接收（断开失败）")
      (println "   ✓ 未收到消息（断开成功）"))))

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
  "一个信号连接多个槽 - 使用可手动触发的自定义信号"
  []
  (println "\n=== 一个信号连接多个槽 ===")

  (let [emitter-class (py/get-attr signals "ValueEmitter")
        emitter (emitter-class)
        slot-1 #(println "  槽函数 1 被调用: " %1 ", " %2)
        slot-2 #(println "  槽函数 2 被调用: " %1 ", " %2)
        slot-3 #(println "  槽函数 3 被调用: " %1 ", " %2)]
    ;; 连接多个槽到同一个信号
    (py/call-attr (py/get-attr emitter "valueChanged") "connect" slot-1)
    (py/call-attr (py/get-attr emitter "valueChanged") "connect" slot-2)
    (py/call-attr (py/get-attr emitter "valueChanged") "connect" slot-3)

    (println "一个信号已连接到 3 个槽函数")
    
    ;; 触发信号 - 所有连接的槽都会被调用
    (println "触发信号...")
    (py/call-attr emitter "emit_value" 42 "Test")
    
    (println "信号触发完成")))

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
