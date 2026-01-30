#!/usr/bin/env clojure -M
;; PySide6 属性系统示例 (Clojure + libpython-clj)

(require '[libpython-clj2.python :as py]
         '[libpython-clj2.require :refer [require-python]])

(py/initialize!)

;; 导入模块
(require-python '[PySide6.QtCore :as QtCore :bind-ns])
(require-python :from "01_core/03_properties"
                '[embedded :as py-embedded :bind-ns :reload])

;; 获取类
(def QObject (py/get-attr QtCore "QObject"))
(def QProperty (py/get-attr QtCore "Property"))
(def QCoreApplication (py/get-attr QtCore "QCoreApplication"))

;; 初始化 QCoreApplication
(py/call-attr py-embedded "run_block_1")

(defn demonstrate-dynamic-properties
  "动态属性操作"
  []
  (println "\n=== 动态属性 ===")
  (let [obj (QObject)]
    ;; 设置属性
    (py/call-attr obj "setProperty" "name" "ClojureObject")
    (py/call-attr obj "setProperty" "count" 100)
    (py/call-attr obj "setProperty" "active" true)
    
    ;; 读取属性
    (println (str "name: " (py/call-attr obj "property" "name")))
    (println (str "count: " (py/call-attr obj "property" "count")))
    (println (str "active: " (py/call-attr obj "property" "active")))
    
    ;; 修改属性
    (py/call-attr obj "setProperty" "count" 200)
    (println (str "count 修改后: " (py/call-attr obj "property" "count")))))

(defn demonstrate-property-notify
  "属性变化通知"
  []
  (println "\n=== 属性变化通知 ===")
  
  ;; 创建带属性的 Python 类
  (py/call-attr py-embedded "run_block_2")
  
  (let [person-class (py/get-attr py-embedded "Person")
        person (person-class)]
    
    ;; 连接信号
    (py/call-attr (py/get-attr person "nameChanged") "connect"
                  (fn [name] (println (str "名字变为: " name))))
    (py/call-attr (py/get-attr person "ageChanged") "connect"
                  (fn [age] (println (str "年龄变为: " age))))
    
    ;; 设置属性
    (py/call-attr person "set_name" "张三")
    (py/call-attr person "set_age" 25)))

(defn -main
  [& args]
  (println "=== PySide6 属性系统示例 (Clojure) ===")
  
  (demonstrate-dynamic-properties)
  (demonstrate-property-notify)
  
  (println "\n=== 完成 ==="))

(-main)
