#!/usr/bin/env clojure -M
;; PySide6 元对象系统示例 (Clojure + libpython-clj)

(require '[libpython-clj2.python :as py]
         '[libpython-clj2.require :refer [require-python]])

;; 初始化 Python
(py/initialize!)

;; 导入 PySide6 模块与类
(require-python '[PySide6.QtCore :as QtCore :bind-ns])
(def QObject (py/get-attr QtCore "QObject"))
(def QCoreApplication (py/get-attr QtCore "QCoreApplication"))

(defn print-meta-object-info
  "打印 QObject 的元对象信息"
  [obj]
  (let [meta (py/call-attr obj "metaObject")]
    (println "\n=== 元对象信息 ===")
    (println (str "类名: " (py/call-attr meta "className")))
    (let [super-class (py/call-attr meta "superClass")]
      (println (str "父类: " (if super-class (py/get-attr super-class "className") "None"))))
    (println (str "方法数量: " (py/call-attr meta "methodCount")))
    (println (str "属性数量: " (py/call-attr meta "propertyCount")))))

(defn demonstrate-dynamic-properties
  "演示动态属性操作"
  []
  (println "\n=== 动态属性 ===")
  (let [obj (QObject)]
    ;; 设置动态属性
    (py/call-attr obj "setProperty" "customProp" "Hello from Clojure")
    (py/call-attr obj "setProperty" "number" 42)

    ;; 获取属性
    (println (str "customProp: " (py/call-attr obj "property" "customProp")))
    (println (str "number: " (py/call-attr obj "property" "number")))

    ;; 列出所有动态属性名
    (println (str "动态属性名: " (py/call-attr obj "dynamicPropertyNames")))))

(defn demonstrate-signals
  "演示信号的元信息"
  []
  (println "\n=== 信号信息 ===")
  (let [obj (QObject)
        meta (py/call-attr obj "metaObject")]
    (println "\n所有方法:")
    (doseq [i (range (py/call-attr meta "methodCount"))]
      (let [method (py/call-attr meta "method" i)
            name (py/call-attr method "name")]
        (println (str "  Method: " name))))))


(def ^:private on-destroyed-callback
  (fn [obj]
    (println (str "对象被销毁: " obj))))


(defn demonstrate-signal-connection
  "演示信号连接

   注意：PySide6 信号断开连接在 libpython-clj 中有已知限制。
   Clojure 函数每次传递给 Python 时会创建不同的包装器对象，
   导致 disconnect 无法找到原始连接。这里使用 try-catch 忽略此警告。"
  []
  (println "\n=== 信号连接测试 ===")
  (let [sender (QObject)
        ;; 使用 volatile 来存储连接状态
        connected? (volatile! false)]


    ;; 连接信号
    (py/call-attr (py/get-attr sender "destroyed") "connect" on-destroyed-callback)
    (vreset! connected? true)
    (println "信号连接成功!")

    ;; 尝试断开连接（可能因 libpython-clj 限制而失败）
    (try
      (py/call-attr (py/get-attr sender "destroyed") "disconnect" on-destroyed-callback)
      (vreset! connected? false)
      (println "信号断开成功!")
      (catch Exception e
        ;; 忽略断开连接失败，这是 libpython-clj + PySide6 的已知限制
        (println "信号断开: 使用 libpython-clj 时的预期行为（非错误）")))))

(defn -main
  "主函数"
  [& args]
  (println "=== PySide6 元对象系统示例 (Clojure) ===")

  ;; 创建 QCoreApplication (控制台程序，无 GUI)
  (let [app (QCoreApplication (py/->py-list []))
        obj (QObject)]
    (print-meta-object-info obj))

  (demonstrate-dynamic-properties)
  (demonstrate-signals)
  (demonstrate-signal-connection)

  (println "\n=== 完成 ==="))

;; 运行主函数
(-main)
